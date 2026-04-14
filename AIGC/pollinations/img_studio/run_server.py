#!/usr/bin/env python3
"""服务器端启动脚本 — 纯展示模式 (Demo Mode)

在远程服务器上运行 Image Studio 时，ComfyUI / 飞书 / SCP 等
本地专属功能均不可用。本脚本仅保留 Pollinations 文生图能力，
作为对外展示用的 Live Demo。
"""
import os
import sys
import json
import time
import random
import urllib.request
import urllib.error
import ssl
import base64
import re
from flask import Flask, render_template, request, jsonify, send_file

# ── 基准路径 ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = Flask(__name__)

# ── Pollinations API Keys ──
POLLINATIONS_KEYS = [
    "sk_pmBF6hTFDV0UFDFGHRsTHTlPG4GYP9ej",
]
_current_key_idx = 0

# ── 角色特征数据库 (简化版，无需读取 RULES/) ──
CHARACTER_PROMPTS = {
    "xiaoai": "brown short hair, young face, slim body",
    "xiaoni": "black long hair, sharp features, slender",
    "xiaoli": "wine-red wavy hair, tall, mature elegance",
}

# ── 页面路由 ──
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/config")
def get_config():
    return jsonify({"pollinations_key": "", "demo_mode": True})


@app.route("/api/random-prompt")
def random_prompt():
    """多维度组合式随机提示词生成器"""
    from prompt_generator import generate_random_prompt_with_meta
    theme = request.args.get("theme")
    result = generate_random_prompt_with_meta(theme=theme)
    return jsonify(result)


@app.route("/api/characters")
def get_characters():
    chars = [
        {"key": "xiaoai", "label": "小爱"},
        {"key": "xiaoni", "label": "小妮"},
        {"key": "xiaoli", "label": "小丽"},
    ]
    return jsonify({"characters": chars})


# ── ComfyUI 桩接口 (服务器无 GPU) ──
@app.route("/api/comfyui/status")
def comfyui_status():
    return jsonify({"status": "stopped"})


@app.route("/api/comfyui/start", methods=["POST"])
def comfyui_start():
    return jsonify({"error": "Demo 模式不支持 ComfyUI"}), 503


@app.route("/api/comfyui/stop", methods=["POST"])
def comfyui_stop():
    return jsonify({"ok": True})


# ── Pollinations 额度查询 ──
@app.route("/api/pollinations/quota")
def pollinations_quota():
    total = 0.0
    for key in POLLINATIONS_KEYS:
        try:
            req = urllib.request.Request(
                "https://gen.pollinations.ai/account/balance"
            )
            req.add_header("Authorization", f"Bearer {key}")
            req.add_header("User-Agent", "Mozilla/5.0")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
                total += float(data.get("balance", 0))
        except Exception:
            pass
    return jsonify({
        "balance": total,
        "images_left": int(total / 0.001),
    })


# ── Pollinations 文生图 ──
@app.route("/api/pollinations/generate", methods=["POST"])
def pollinations_generate():
    global _current_key_idx
    try:
        body = request.json
        prompt = body.get("prompt", "")
        char_key = body.get("character", "")

        # 人物特征注入
        if char_key and char_key in CHARACTER_PROMPTS:
            prompt = (
                f"((solo, 1girl, one person only:2.0)), "
                f"({CHARACTER_PROMPTS[char_key]}:1.3), "
                f"(chinese identity, young face:1.5), "
                f"{prompt.strip(', ')}"
            )
        else:
            prompt = (
                f"((solo, 1girl, one person only:2.0)), "
                f"(a young beautiful Chinese girl:1.5), "
                f"{prompt.strip(', ')}"
            )

        # 写实增强
        realism = (
            ", Cinematic, film still, Masterpiece, high quality, "
            "Highly detailed, photorealistic, RAW photo, DSLR, "
            "professional photography, Shallow depth of field, "
            "Bokeh, natural lighting, film grain, "
            "ultra detailed, 8k uhd, high resolution"
        )
        if "photorealistic" not in prompt.lower():
            prompt = prompt.rstrip(", ") + realism

        # 参数
        params = {}
        for k in ["model", "width", "height", "seed",
                   "negative_prompt", "safe", "enhance"]:
            if body.get(k) is not None and body.get(k) != "":
                params[k] = str(body[k])

        default_neg = (
            "oil painting, cartoon, anime, illustration, "
            "2girls, 3girls, multiple people, "
            "3d render, drawing, sketch, watercolor, "
            "extra fingers, extra limbs, mutated hands, "
            "bad anatomy, deformed, disfigured, "
            "blurry, low quality, pixelated, worst quality"
        )
        user_neg = params.get("negative_prompt", "")
        if user_neg:
            params["negative_prompt"] = (
                user_neg.rstrip(", ") + ", " + default_neg
            )
        else:
            params["negative_prompt"] = default_neg

        # JSON payload
        payload = {
            "prompt": prompt,
            "model": params.get("model", "flux"),
            "size": (
                f"{params.get('width', 1024)}"
                f"x{params.get('height', 1024)}"
            ),
            "response_format": "b64_json",
        }
        if "seed" in params:
            payload["seed"] = int(params["seed"])
        if "negative_prompt" in params:
            payload["negative_prompt"] = params["negative_prompt"]
        if "enhance" in params:
            payload["enhance"] = (
                str(params["enhance"]).lower() == "true"
            )
        if "safe" in params:
            payload["safe"] = str(params["safe"]).lower() == "true"

        json_data = json.dumps(payload).encode("utf-8")
        url = "https://gen.pollinations.ai/v1/images/generations"
        req_headers = {
            "User-Agent": "ImageStudio/1.0",
            "Content-Type": "application/json",
        }

        use_key = body.get("use_key", False)
        key_list = []
        if use_key and POLLINATIONS_KEYS:
            for i in range(len(POLLINATIONS_KEYS)):
                idx = (_current_key_idx + i) % len(POLLINATIONS_KEYS)
                key_list.append(POLLINATIONS_KEYS[idx])
        key_list.append(None)  # 免费兜底

        data = None
        last_err = None
        for ki, key in enumerate(key_list):
            run_headers = dict(req_headers)
            if key:
                run_headers["Authorization"] = f"Bearer {key}"
            for retry in range(3):
                try:
                    req = urllib.request.Request(
                        url, data=json_data,
                        headers=run_headers, method="POST"
                    )
                    with urllib.request.urlopen(
                        req, timeout=180
                    ) as resp:
                        res_json = json.loads(resp.read())
                        b64_str = (
                            res_json.get("data", [{}])[0]
                            .get("b64_json")
                        )
                        if b64_str:
                            data = base64.b64decode(b64_str)
                    break
                except urllib.error.HTTPError as e:
                    last_err = e
                    if e.code in (401, 429, 402, 403) and key:
                        _current_key_idx = (
                            (_current_key_idx + 1)
                            % len(POLLINATIONS_KEYS)
                        )
                        break
                    raise
                except (ssl.SSLError, ConnectionResetError,
                        urllib.error.URLError) as e:
                    last_err = e
                    time.sleep(2)
            if data is not None:
                break

        if data is None:
            raise last_err or Exception("生成失败")

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
            "use_key": use_key,
        })
    except urllib.error.HTTPError as e:
        return jsonify({"error": f"HTTP {e.code}"}), e.code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── 图片服务 ──
@app.route("/api/image/<filename>")
def serve_image(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        return send_file(path)
    return "Not found", 404


# ── 上传图片 ──
@app.route("/api/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "没有文件"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "空文件名"}), 400
    ts = int(time.time())
    fname = f"upload_{ts}.png"
    fpath = os.path.join(OUTPUT_DIR, fname)
    f.save(fpath)
    return jsonify({
        "ok": True, "filename": fname,
        "url": f"/api/image/{fname}",
    })


# ── 精修/推送/换脸 桩接口 ──
@app.route("/api/refine", methods=["POST"])
def refine_stub():
    return jsonify({
        "error": "Demo 模式 — 精修功能需要本地 GPU"
    }), 503


@app.route("/api/swap", methods=["POST"])
def swap_stub():
    return jsonify({
        "error": "Demo 模式 — 换脸功能需要本地 GPU"
    }), 503


@app.route("/api/push/feishu", methods=["POST"])
def push_feishu_stub():
    return jsonify({
        "error": "Demo 模式 — 飞书推送不可用"
    }), 503


@app.route("/api/push/lab", methods=["POST"])
def push_lab_stub():
    return jsonify({
        "error": "Demo 模式 — 实验室推送不可用"
    }), 503


if __name__ == "__main__":
    print("=" * 50)
    print("Image Studio — Demo Mode (Server)")
    print(f"Output Dir: {OUTPUT_DIR}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5051, debug=False)
