#!/usr/bin/env python3
"""Pollinations 共享服务助手 — pollination_helper.py
高度内聚 Pollinations API 处理，支持密钥轮询与容灾、强力提示词清洗及动态依赖退避。
"""
import os
import re
import ssl
import json
import time
import base64
import urllib.request
import urllib.error

# 1. 密钥与配置管理
_env_key = os.environ.get("POLLINATIONS_API_KEY", "")
POLLINATIONS_KEYS = [k.strip() for k in _env_key.split(",") if k.strip()] if _env_key else []
_current_key_idx = 0

# 2. 飞书推送配置
FEISHU_OPEN_ID = os.environ.get("FEISHU_OPEN_ID", "ou_c456044cf7eb9ccbf478f7c2d47bf74c")

# 3. 动态加载人物特征库（优先从项目核心库引入，不存在则使用内置兜底）
CHAR_TRAITS_DB = {}
CHAR_NEG_PATCH = {}
_has_slave_lib = False

try:
    from TakePhotos.prompts.slave_prompt_library import CHAR_TRAITS_DB, CHAR_NEG_PATCH, apply_rope_protection
    _has_slave_lib = True
except ImportError:
    # 远程展示模式 (Demo Mode) 兜底特征库
    CHAR_TRAITS_DB = {
        "xiaoai": "brown short hair, young face, slim body, completely hairless smooth pussy",
        "xiaoni": "black long hair, sharp features, slender, sparse black pubic hair",
        "xiaoli": "wine-red wavy hair, tall, mature elegance, completely hairless smooth pussy",
    }
    CHAR_NEG_PATCH = {
        "xiaoai": "large breasts, big breasts, huge breasts, cleavage, heels",
        "xiaoni": "shoes, heels, sandals",
        "xiaoli": "pubic hair, any pubic hair, bush, sparse hair, stubble",
    }

def clean_clothing_words(prompt):
    """强力全局特征防卫：清除场景提示词中任何脑补的衣服/裙子词汇"""
    _clothing_words = [r'\bskirt\b', r'\bdress\b', r'\bclothes\b', r'\bclothing\b', r'\bshirt\b', r'\byukata\b', r'\bkimono\b']
    for cw in _clothing_words:
        prompt = re.sub(cw, "", prompt, flags=re.IGNORECASE)
    return prompt

def prepare_prompt_payload(prompt, char_key, body):
    """组装经过中国年轻女孩强制约束、写实增强和防衣服污染清洗后的正反向 Prompt"""
    # 清洗外国籍冲突词
    _conflicts = [r'\bcaucasian\b', r'\bwhite\s+girl\b', r'\beuropean\b',
                  r'\bkorean\b', r'\bjapanese\b', r'\bwestern\b',
                  r'\bolder\s+woman\b', r'\bmature\s+woman\b', r'\bforeign\b',
                  r'\bblonde\b', r'\blatina\b', r'\bafrican\b']
    for cp in _conflicts:
        prompt = re.sub(cp, "", prompt, flags=re.IGNORECASE)

    # 注入独享角色特征与基本国籍
    if char_key and char_key in CHAR_TRAITS_DB:
        prompt = f"((solo, 1girl, one person only:2.0)), ({CHAR_TRAITS_DB[char_key]}:1.3), (chinese identity, young face:1.5), {prompt.strip(', ')}"
    else:
        prompt = f"((solo, 1girl, one person only:2.0)), (a young beautiful Chinese girl:1.5), {prompt.strip(', ')}"

    # 电影感摄影写实增强词
    realism_suffix = (", Cinematic, film still, Masterpiece, high quality, "
                      "Highly detailed, Cinematic lighting, photorealistic, RAW photo, DSLR, "
                      "professional photography, Shallow depth of field, Bokeh, "
                      "natural lighting, film grain, ultra detailed, 8k uhd, high resolution")
    if "photorealistic" not in prompt.lower():
        prompt = prompt.rstrip(", ") + realism_suffix

    # 追加死锁防衣物负向补丁
    default_neg = ("oil painting, cartoon, anime, illustration, "
                   "2girls, 3girls, multiple people, second person, background people, "
                   "3d render, drawing, sketch, watercolor, "
                   "extra fingers, extra limbs, mutated hands, "
                   "bad anatomy, deformed, disfigured, blurry, low quality, low resolution, pixelated, "
                   "worst quality, jpeg artifacts, ugly, duplicate, morbid, poorly drawn face, poorly drawn hands, "
                   "overexposed, underexposed, bad proportions, "
                   "skirt, dress, clothing, clothes, shirt, bra, panties, pantyhose, "
                   "socks, underwear, undergarment, yukata, kimono, uniform")
    
    user_neg = body.get("negative_prompt", "")
    neg_prompt = f"{user_neg.rstrip(', ')}, {default_neg}" if user_neg else default_neg

    if char_key and char_key in CHAR_NEG_PATCH:
        neg_prompt = f"{neg_prompt.rstrip(', ')}, {CHAR_NEG_PATCH[char_key]}"

    # 如果有 slave_prompt_library，调用高阶防卫罩彻底隔离红皮束具污染
    if _has_slave_lib:
        prompt, neg_prompt = apply_rope_protection(prompt, neg_prompt)

    prompt = clean_clothing_words(prompt)
    return prompt, neg_prompt

def fetch_quota_summary():
    """获取所有 API Key 的额度余额与剩余生成张数"""
    total = 0.0
    fetch_success = False
    for key in POLLINATIONS_KEYS:
        try:
            req = urllib.request.Request("https://gen.pollinations.ai/account/balance")
            req.add_header("Authorization", f"Bearer {key}")
            req.add_header("User-Agent", "Mozilla/5.0")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read())
                if data.get("success") is not False:
                    total += float(data.get("balance", 0))
                    fetch_success = True
        except Exception:
            pass
    return total, fetch_success

def execute_poll_generation(body, custom_key=None, use_key=False):
    """带 Key 轮询容灾与免费自动降级降噪生图引擎"""
    global _current_key_idx
    prompt = body.get("prompt", "")
    char_key = body.get("character", "")
    
    final_prompt, final_neg = prepare_prompt_payload(prompt, char_key, body)
    
    payload = {
        "prompt": final_prompt,
        "model": body.get("model", "flux"),
        "size": f"{body.get('width', 1024)}x{body.get('height', 1024)}",
        "response_format": "b64_json"
    }
    if body.get("seed") is not None and body.get("seed") != "":
        payload["seed"] = int(body["seed"])
    if final_neg:
        payload["negative_prompt"] = final_neg
    if body.get("enhance") is not None:
        payload["enhance"] = str(body["enhance"]).lower() == 'true'
    if body.get("safe") is not None:
        payload["safe"] = str(body["safe"]).lower() == 'true'

    json_data = json.dumps(payload).encode('utf-8')
    url = "https://gen.pollinations.ai/v1/images/generations"
    req_headers = {
        "User-Agent": "ImageStudio/1.0",
        "Content-Type": "application/json"
    }

    key_list = []
    if use_key:
        if custom_key:
            key_list.append(custom_key)
        if POLLINATIONS_KEYS:
            for i in range(len(POLLINATIONS_KEYS)):
                idx = (_current_key_idx + i) % len(POLLINATIONS_KEYS)
                key_list.append(POLLINATIONS_KEYS[idx])
    key_list.append(None) # 兜底免费模式

    data = None
    last_err = None
    ct = "image/jpeg"

    for ki, key in enumerate(key_list):
        run_headers = dict(req_headers)
        if key:
            run_headers["Authorization"] = f"Bearer {key}"
        
        # 指数退避重试 (最大3次网络重试)
        for retry in range(3):
            try:
                req = urllib.request.Request(url, data=json_data, headers=run_headers, method="POST")
                with urllib.request.urlopen(req, timeout=120) as resp:
                    res_json = json.loads(resp.read())
                    b64_str = res_json.get('data', [{}])[0].get('b64_json')
                    if b64_str:
                        data = base64.b64decode(b64_str)
                break
            except urllib.error.HTTPError as e:
                last_err = e
                if e.code in (401, 429, 402, 403) and key:
                    _current_key_idx = (_current_key_idx + 1) % len(POLLINATIONS_KEYS)
                    print(f"[Helper] Key #{ki} 额度不足/越权({e.code}), 轮换至下一 Key")
                    break # 跳至下个 Key
                raise
            except Exception as e:
                last_err = e
                print(f"[Helper] 生图网络错误 (重试 {retry+1}): {e}")
                time.sleep(2)
                continue
        if data is not None:
            if key is None and use_key:
                print("[Helper] 本地已启用金钥额度但已全部耗尽，降级免费模式生图")
            break
            
    if data is None:
        raise last_err or Exception("生成服务无响应，所有 Key 额度耗尽且免费降级通道阻塞")

    return data, payload["model"]
