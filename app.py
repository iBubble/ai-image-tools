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
        denoise = float(body.get("denoise", 0.45))
        scene = body.get("scene_prompt", "")
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

        return jsonify({
            "url": f"/api/image/{prefix}.png",
            "seed": seed, "model": camera,
            "denoise": denoise,
            "character": char_key
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


@app.route("/api/pollinations/generate", methods=["POST"])
def pollinations_generate():
    """后端代理 Pollinations API（绕过 CORS）"""
    try:
        body = request.json
        prompt = body.get("prompt", "")
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

        # 带 key 轮换 + 网络重试的请求逻辑
        import ssl
        global _current_key_idx
        max_key_tries = len(POLLINATIONS_KEYS) if use_key else 1
        max_net_retries = 3
        last_err = None
        data = None
        ct = "image/jpeg"
        for key_attempt in range(max_key_tries):
            req_headers = dict(headers)
            if use_key and POLLINATIONS_KEYS:
                key = POLLINATIONS_KEYS[_current_key_idx % len(POLLINATIONS_KEYS)]
                req_headers["Authorization"] = f"Bearer {key}"
            for retry in range(max_net_retries):
                try:
                    req = urllib.request.Request(url, headers=req_headers)
                    with urllib.request.urlopen(req, timeout=180) as resp:
                        data = resp.read()
                        ct = resp.headers.get("Content-Type", "image/jpeg")
                    break
                except (ssl.SSLError, ConnectionResetError, urllib.error.URLError) as e:
                    last_err = e
                    print(f"[Pollinations] 网络错误(retry {retry+1}/{max_net_retries}): {e}")
                    time.sleep(2)
                    continue
                except urllib.error.HTTPError as e:
                    last_err = e
                    if e.code in (429, 402, 403) and use_key:
                        _current_key_idx = (_current_key_idx + 1) % len(POLLINATIONS_KEYS)
                        print(f"[Pollinations] Key 额度不足({e.code}), 切换到 key #{_current_key_idx}")
                        break  # 跳到下一个 key
                    raise
            if data is not None:
                break
        if data is None:
            raise last_err or Exception("请求失败，请重试")

        # 保存到本地
        ts = int(time.time())
        seed = body.get("seed", "0")
        fname = f"poll_{ts}_{seed}.jpg"
        fpath = os.path.join(OUTPUT_DIR, fname)
        with open(fpath, "wb") as f:
            f.write(data)

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
