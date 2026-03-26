#!/usr/bin/env python3
"""Image Studio — 本地图片生成工作台
支持 ComfyUI 和 Pollinations 双后端
"""
import os
import sys
import json
import time
import random
import urllib.request
import urllib.error
from flask import Flask, render_template, request, jsonify, send_file

PROJECT_ROOT = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed"
sys.path.insert(0, PROJECT_ROOT)

app = Flask(__name__)
COMFYUI_URL = "http://127.0.0.1:8188"
COMFYUI_PROMPT = f"{COMFYUI_URL}/prompt"
COMFYUI_HISTORY = f"{COMFYUI_URL}/history"
COMFYUI_OUTPUT = "/Users/gemini/Projects/Own/ComfyUI/output"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
POLLINATIONS_KEYS = [
    "sk_pmBF6hTFDV0UFDFGHRsTHTlPG4GYP9ej",
    "sk_pLuQA5NZZgXfG7XSCzyqDD0vY6s1MM3o",
    "sk_TYdr9KBbpS4VbLoL3k6dGJGrZWnDqfrN",
]
_current_key_idx = 0
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 人物 Prompt 配置 ──
RULES_DIR = os.path.join(PROJECT_ROOT, "RULES")
CHARACTER_PROMPTS = {}

def _load_character_prompt(name, filename):
    """从 PROMPT.md 文件第24行代码块提取核心 prompt"""
    path = os.path.join(RULES_DIR, filename)
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # 代码块在第24行（索引23）
    if len(lines) >= 24:
        prompt = lines[23].strip()
        if prompt:
            CHARACTER_PROMPTS[name] = prompt

_load_character_prompt("xiaoni", "XiaoNi_PROMPT.md")
_load_character_prompt("xiaoai", "XiaoAi_PROMPT.md")
_load_character_prompt("xiaoli", "XiaoLi_PROMPT.md")

# 人物关键词映射（中英文）
CHARACTER_KEYWORDS = {
    "xiaoni": ["小妮", "xiaoni", "xiao ni", "xiao_ni"],
    "xiaoai": ["小爱", "xiaoai", "xiao ai", "xiao_ai"],
    "xiaoli": ["小丽", "xiaoli", "xiao li", "xiao_li"],
}

def detect_character(text):
    """检测文本中的人物关键词，返回人物 key 或 None"""
    lower = text.lower()
    for key, keywords in CHARACTER_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in lower:
                return key
    return None


# ── 自动检测卡通/真人 ──
def _detect_cartoon(filepath):
    """分析像素判断图片是卡通(True)还是真人照(False)"""
    try:
        from PIL import Image
        import numpy as np
        img = Image.open(filepath).convert("RGB").resize((128, 128))
        arr = np.array(img, dtype=np.float32)
        # 颜色唯一性（量化到8位色）
        q = (arr / 32).astype(np.uint8).reshape(-1, 3)
        uc = len(set(map(tuple, q.tolist())))
        # 边缘锐度
        gray = np.mean(arr, axis=2)
        em = (np.mean(np.abs(np.diff(gray, axis=1)))
              + np.mean(np.abs(np.diff(gray, axis=0)))) / 2
        # 饱和度
        mx, mn = arr.max(axis=2), arr.min(axis=2)
        sat = np.mean(np.where(mx > 0, (mx - mn) / (mx + 1e-6), 0))
        sc = (2 if uc < 600 else 1 if uc < 900 else 0)
        sc += (1 if em > 18 else 0) + (1 if sat > 0.35 else 0)
        return sc >= 2
    except Exception:
        return False  # 检测失败默认当真人


# ── 自动归档 + 推送（后台线程，不阻塞请求） ──
SECRET_DIR = os.path.join(PROJECT_ROOT, "AIGC", "outputs")
os.makedirs(SECRET_DIR, exist_ok=True)

def _auto_archive(filepath):
    """后台线程：保存到 .secret + 推送飞书 + SCP 到服务器B"""
    import threading
    def _worker():
        import subprocess
        from datetime import datetime
        try:
            date_str = datetime.now().strftime("%Y%m%d")
            dest_dir = os.path.join(SECRET_DIR, date_str)
            os.makedirs(dest_dir, exist_ok=True)
            fname = os.path.basename(filepath)
            dest = os.path.join(dest_dir, fname)
            os.system(f"cp '{filepath}' '{dest}'")
            print(f"[Archive] 已保存: {dest}")

            # 推送飞书
            try:
                from src.utils.feishu_notifier import FeishuNotifier
                notifier = FeishuNotifier()
                open_id = "ou_c456044cf7eb9ccbf478f7c2d47bf74c"
                image_key = notifier.upload_image(filepath)
                if image_key:
                    card = {
                        "config": {"wide_screen_mode": True},
                        "header": {"template": "blue",
                                   "title": {"content": "🎨 Image Studio",
                                             "tag": "plain_text"}},
                        "elements": [
                            {"tag": "img", "img_key": image_key,
                             "alt": {"content": fname,
                                     "tag": "plain_text"}},
                        ]
                    }
                    notifier.send_interactive_card(open_id, card)
                    print(f"[Archive] 飞书推送成功")
            except Exception as e:
                print(f"[Archive] 飞书推送失败: {e}")

            # SCP 到服务器B
            try:
                target = f"/root/b-lab_20260319203311/upload/{date_str}"
                subprocess.run(
                    ["ssh", "tencent-server", f"mkdir -p {target}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL, timeout=10)
                subprocess.run(
                    ["scp", filepath, f"tencent-server:{target}/"],
                    capture_output=True, timeout=30)
                print(f"[Archive] 服务器B推送成功")
            except Exception as e:
                print(f"[Archive] 服务器B推送失败: {e}")
        except Exception as e:
            print(f"[Archive] 归档失败: {e}")
    threading.Thread(target=_worker, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/characters")
def get_characters():
    """返回可用人物列表"""
    chars = []
    for key in CHARACTER_PROMPTS:
        label = {"xiaoni": "小妮", "xiaoai": "小爱",
                 "xiaoli": "小丽"}.get(key, key)
        chars.append({"key": key, "label": label})
    return jsonify({"characters": chars})


@app.route("/api/comfyui/generate", methods=["POST"])
def comfyui_generate():
    """通过ComfyUI生成图片"""
    try:
        from TakePhotos.prompts.slave_prompt_library import (
            build_zit_workflow
        )
        body = request.json
        positive = body.get("prompt", "")
        negative = body.get("negative_prompt", "")
        camera = body.get("model", "moody")

        # 自动检测人物 / 手动指定人物
        char_key = body.get("character") or detect_character(positive)
        char_prompt = ""
        if char_key and char_key in CHARACTER_PROMPTS:
            char_prompt = CHARACTER_PROMPTS[char_key]
            # 用人物基础 prompt 替换，用户输入追加在后面作为场景补充
            positive = char_prompt + ", " + positive

        seed = body.get("seed")
        if seed is None or seed == "" or seed == -1:
            seed = random.randint(1, 10**12)
        else:
            seed = int(seed)

        ts = int(time.time())
        prefix = f"studio_{ts}_{seed}"

        wf = build_zit_workflow(
            positive=positive, negative=negative,
            camera=camera, seed=seed,
            filename_prefix=prefix, pure_mode=True
        )

        data = json.dumps({"prompt": wf}).encode("utf-8")
        req = urllib.request.Request(COMFYUI_PROMPT, data=data)
        with urllib.request.urlopen(req) as r:
            pid = json.loads(r.read())["prompt_id"]

        # 轮询等待完成 (最长 5 分钟)
        img_name = None
        for _ in range(60):
            try:
                r = urllib.request.urlopen(
                    f"{COMFYUI_HISTORY}/{pid}")
                hist = json.loads(r.read())
                if pid in hist:
                    outs = hist[pid].get("outputs", {})
                    for nid in outs:
                        if "images" in outs[nid]:
                            img_name = outs[nid]["images"][0][
                                "filename"]
                            break
            except Exception:
                pass
            if img_name:
                break
            time.sleep(5)

        if not img_name:
            return jsonify({"error": "生成超时"}), 504

        src = os.path.join(COMFYUI_OUTPUT, img_name)
        dst = os.path.join(OUTPUT_DIR, f"{prefix}.png")
        os.system(f"cp '{src}' '{dst}'")
        _auto_archive(dst)

        return jsonify({
            "url": f"/api/image/{prefix}.png",
            "seed": seed, "model": camera
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


COMFYUI_INPUT = "/Users/gemini/Projects/Own/ComfyUI/input"

@app.route("/api/refine", methods=["POST"])
def refine_image():
    """精修模式：用 ComfyUI img2img 重绘已生成的图片"""
    try:
        from TakePhotos.prompts.slave_prompt_library import (
            build_zit_img2img_workflow, set_active_character
        )
        body = request.json
        filename = body.get("filename", "")
        fpath = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(fpath):
            return jsonify({"error": "源图片不存在"}), 404

        char_key = body.get("character", "")
        camera = body.get("camera", "moody")
        denoise_input = body.get("denoise", "auto")
        scene = body.get("scene_prompt", "")

        # 自动检测卡通/真人
        is_cartoon_img = False
        if denoise_input == "auto" or denoise_input is None:
            is_cartoon_img = _detect_cartoon(fpath)
            denoise = 0.65 if is_cartoon_img else 0.55
            print(f"[Refine] 自动检测: "
                  f"{'卡通' if is_cartoon_img else '真人'} → "
                  f"denoise={denoise}")
        else:
            denoise = float(denoise_input)
        seed = body.get("seed")
        if seed is None or seed == "" or seed == -1:
            seed = random.randint(1, 10**12)
        else:
            seed = int(seed)

        if char_key:
            set_active_character(char_key)

        input_name = f"refine_{int(time.time())}.png"
        input_path = os.path.join(COMFYUI_INPUT, input_name)
        os.system(f"cp '{fpath}' '{input_path}'")

        ts = int(time.time())
        prefix = f"refined_{ts}_{seed}"

        wf = build_zit_img2img_workflow(
            image_filename=input_name,
            positive=scene, negative="",
            camera=camera, seed=seed,
            filename_prefix=prefix,
            denoise=denoise
        )

        data = json.dumps({"prompt": wf}).encode("utf-8")
        req = urllib.request.Request(COMFYUI_PROMPT, data=data)
        with urllib.request.urlopen(req) as r:
            pid = json.loads(r.read())["prompt_id"]

        img_name = None
        for _ in range(60):
            try:
                r = urllib.request.urlopen(
                    f"{COMFYUI_HISTORY}/{pid}")
                hist = json.loads(r.read())
                if pid in hist:
                    outs = hist[pid].get("outputs", {})
                    for nid in outs:
                        if "images" in outs[nid]:
                            img_name = outs[nid]["images"][0][
                                "filename"]
                            break
            except Exception:
                pass
            if img_name:
                break
            time.sleep(5)

        if not img_name:
            return jsonify({"error": "精修超时"}), 504

        src = os.path.join(COMFYUI_OUTPUT, img_name)
        dst = os.path.join(OUTPUT_DIR, f"{prefix}.png")
        os.system(f"cp '{src}' '{dst}'")
        _auto_archive(dst)

        return jsonify({
            "url": f"/api/image/{prefix}.png",
            "seed": seed, "model": camera,
            "denoise": denoise,
            "character": char_key,
            "img_type": "cartoon" if is_cartoon_img else "photo"
        })
    except (ConnectionRefusedError, urllib.error.URLError) as e:
        return jsonify({"error": "ComfyUI 未启动，请先运行 ComfyUI (端口 8188)"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/image/<filename>")
def serve_image(filename):
    """提供生成的图片"""
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        return send_file(path)
    return "Not found", 404


@app.route("/api/upload", methods=["POST"])
def upload_image():
    """上传图片到 outputs 目录"""
    if 'file' not in request.files:
        return jsonify({"error": "没有文件"}), 400
    f = request.files['file']
    if not f.filename:
        return jsonify({"error": "空文件名"}), 400
    ts = int(time.time())
    fname = f"upload_{ts}.png"
    fpath = os.path.join(OUTPUT_DIR, fname)
    f.save(fpath)
    return jsonify({"ok": True, "filename": fname,
                    "url": f"/api/image/{fname}"})

@app.route("/api/pollinations/quota", methods=["GET"])
def pollinations_quota():
    """获取 Pollinations 全部 key 的余额总和"""
    total = 0.0
    for key in POLLINATIONS_KEYS:
        try:
            req = urllib.request.Request("https://gen.pollinations.ai/account/balance")
            req.add_header("Authorization", f"Bearer {key}")
            req.add_header("User-Agent", "Mozilla/5.0")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read())
                total += float(data.get("balance", 0))
        except Exception:
            pass
    
    return jsonify({
        "balance": total,
        "images_left": int(total / 0.001)
    })


@app.route("/api/pollinations/generate", methods=["POST"])
def pollinations_generate():
    """后端代理 Pollinations API（绕过 CORS）"""
    try:
        from TakePhotos.prompts.slave_prompt_library import CHAR_TRAITS_DB
        body = request.json
        prompt = body.get("prompt", "")
        char_key = body.get("character", "")
        
        # 核心漏洞修复：如果用户在界面选中了人物，必须强制将人物特征前置注入 Poll 提示词
        # 否则 Poll 会完全依据用户写的 prompt 画，导致短发变长发等丢失特征问题
        if char_key and char_key in CHAR_TRAITS_DB:
            prompt = f"({CHAR_TRAITS_DB[char_key]}:1.3), {prompt}"

        # 自动追加写实增强词（摄影级）
        realism_suffix = (", photorealistic, RAW photo, DSLR, "
                          "professional photography, natural lighting, "
                          "shallow depth of field, film grain, "
                          "ultra detailed, 8k uhd, high resolution")
        if "photorealistic" not in prompt.lower():
            prompt = prompt.rstrip(", ") + realism_suffix
        params = {}
        for k in ["model", "width", "height", "seed",
                   "negative_prompt", "safe", "enhance"]:
            if body.get(k) is not None and body.get(k) != "":
                params[k] = str(body[k])

        # 自动追加防失真负面提示词
        default_neg = ("oil painting, cartoon, anime, illustration, "
                       "3d render, drawing, sketch, watercolor, "
                       "extra fingers, extra limbs, mutated hands, "
                       "bad anatomy, deformed, disfigured, "
                       "blurry, low quality, low resolution, pixelated, "
                       "worst quality, jpeg artifacts, "
                       "ugly, duplicate, morbid, "
                       "poorly drawn face, poorly drawn hands, "
                       "overexposed, underexposed, bad proportions")
        user_neg = params.get("negative_prompt", "")
        if user_neg:
            params["negative_prompt"] = user_neg.rstrip(", ") + ", " + default_neg
        else:
            params["negative_prompt"] = default_neg

        encoded = urllib.request.quote(prompt.strip())
        qs = "&".join(f"{k}={urllib.request.quote(v)}"
                      for k, v in params.items())
        url = f"https://gen.pollinations.ai/image/{encoded}"
        if qs:
            url += f"?{qs}"

        headers = {"User-Agent": "ImageStudio/1.0"}
        use_key = body.get("use_key", False)

        # 带 key 轮换 + 网络重试 + 402 自动降级的请求逻辑
        import ssl
        global _current_key_idx
        max_net_retries = 3
        last_err = None
        data = None
        ct = "image/jpeg"
        
        # 构建尝试顺序：所有 Key → 无 Key 兜底
        key_list = []
        if use_key and POLLINATIONS_KEYS:
            for i in range(len(POLLINATIONS_KEYS)):
                idx = (_current_key_idx + i) % len(POLLINATIONS_KEYS)
                key_list.append(POLLINATIONS_KEYS[idx])
        key_list.append(None)  # 最后一轮：无 Key 免费模式兜底
        
        for ki, key in enumerate(key_list):
            req_headers = dict(headers)
            if key:
                req_headers["Authorization"] = f"Bearer {key}"
            for retry in range(max_net_retries):
                try:
                    req = urllib.request.Request(url, headers=req_headers)
                    with urllib.request.urlopen(req, timeout=180) as resp:
                        data = resp.read()
                        ct = resp.headers.get("Content-Type", "image/jpeg")
                    break
                except (ssl.SSLError, ConnectionResetError,
                        urllib.error.URLError) as e:
                    last_err = e
                    print(f"[Poll] 网络错误(retry {retry+1}): {e}")
                    time.sleep(2)
                    continue
                except urllib.error.HTTPError as e:
                    last_err = e
                    if e.code in (429, 402, 403) and key:
                        _current_key_idx = (
                            _current_key_idx + 1) % len(POLLINATIONS_KEYS)
                        print(f"[Poll] Key #{ki} 额度不足({e.code}),"
                              f" 切换下一个")
                        break  # 跳到下一个 key / 无 key 兜底
                    raise
            if data is not None:
                if key is None and use_key:
                    print("[Poll] 所有Key耗尽，已降级为免费模式")
                break
        if data is None:
            raise last_err or Exception("所有Key额度耗尽且免费模式也失败")

        # 保存到本地
        ts = int(time.time())
        seed = body.get("seed", "0")
        fname = f"poll_{ts}_{seed}.jpg"
        fpath = os.path.join(OUTPUT_DIR, fname)
        with open(fpath, "wb") as f:
            f.write(data)
        _auto_archive(fpath)

        return jsonify({
            "url": f"/api/image/{fname}",
            "seed": seed,
            "model": params.get("model", "flux"),
            "use_key": use_key
        })
    except urllib.error.HTTPError as e:
        return jsonify({"error": f"HTTP {e.code}"}), e.code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/push/feishu", methods=["POST"])
def push_feishu():
    """推送当前图片到飞书"""
    try:
        from src.utils.feishu_notifier import FeishuNotifier
        body = request.json
        filename = body.get("filename", "")
        fpath = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(fpath):
            return jsonify({"error": "图片文件不存在"}), 404

        notifier = FeishuNotifier()
        open_id = "ou_c456044cf7eb9ccbf478f7c2d47bf74c"
        image_key = notifier.upload_image(fpath)
        if not image_key:
            return jsonify({"error": "飞书图片上传失败"}), 500

        card = {
            "config": {"wide_screen_mode": True},
            "header": {"template": "blue",
                       "title": {"content": "🎨 Image Studio 作品",
                                 "tag": "plain_text"}},
            "elements": [
                {"tag": "img", "img_key": image_key,
                 "alt": {"content": "生成图片", "tag": "plain_text"}},
                {"tag": "div", "text": {
                    "content": f"**文件**: `{filename}`",
                    "tag": "lark_md"}},
            ]
        }
        notifier.send_interactive_card(open_id, card)
        return jsonify({"ok": True, "msg": "已推送到飞书"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/push/lab", methods=["POST"])
def push_lab():
    """推送当前图片到 B 实验室 (tencent-server)"""
    try:
        import subprocess
        from datetime import datetime
        body = request.json
        filename = body.get("filename", "")
        fpath = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(fpath):
            return jsonify({"error": "图片文件不存在"}), 404

        date_str = datetime.now().strftime("%Y%m%d")
        target = f"/root/b-lab_20260319203311/upload/{date_str}"
        subprocess.run(["ssh", "tencent-server", f"mkdir -p {target}"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=10)
        result = subprocess.run(
            ["scp", fpath, f"tencent-server:{target}/"],
            capture_output=True, timeout=30)
        if result.returncode != 0:
            return jsonify({"error": "SCP 上传失败"}), 500
        return jsonify({"ok": True, "msg": "已推送到 B 实验室"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/config")
def get_config():
    """返回前端配置"""
    return jsonify({"pollinations_key": POLLINATIONS_KEYS[0] if POLLINATIONS_KEYS else ""})


if __name__ == "__main__":
    print("🎨 Image Studio 启动中...")
    print("   http://localhost:5050")
    app.run(host="0.0.0.0", port=5050, debug=False)
