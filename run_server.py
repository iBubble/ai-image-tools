#!/usr/bin/env python3
"""服务器端启动脚本 — 纯展示模式 (Demo Mode)

在远程服务器上运行 Image Studio 时，ComfyUI / 飞书 / SCP 等
本地专属功能均不可用。本脚本仅保留 Pollinations 文生图能力，
作为对外展示用的 Live Demo。
"""
import os
# 自动加载本地 .env 文件（静默兼容未安装 python-dotenv 的环境）
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass
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
from pollinations_helper import POLLINATIONS_KEYS, execute_poll_generation, fetch_quota_summary

# ── 基准路径 ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = Flask(__name__)

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
    total, fetch_success = fetch_quota_summary()
    return jsonify({
        "balance": total,
        "images_left": int(total / 0.002) if fetch_success else 0,
        "fetch_success": fetch_success
    })


# ── Pollinations 文生图 ──
@app.route("/api/pollinations/generate", methods=["POST"])
def pollinations_generate():
    try:
        body = request.json
        use_key = body.get("use_key", False)

        # 委托给共享生图引擎，安全剥离所有细节
        data, model_used = execute_poll_generation(body, use_key=use_key)

        ts = int(time.time())
        seed = body.get("seed", "0")
        fname = f"poll_{ts}_{seed}.jpg"
        fpath = os.path.join(OUTPUT_DIR, fname)
        with open(fpath, "wb") as f:
            f.write(data)

        return jsonify({
            "url": f"/api/image/{fname}",
            "seed": seed,
            "model": model_used,
            "use_key": use_key,
        })
    except urllib.error.HTTPError as e:
        return jsonify({"error": f"HTTP {e.code}"}), e.code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── 图片服务 ──
@app.route("/api/image/<filename>")
def serve_image(filename):
    """S-05 修复：路径遍历防护"""
    from werkzeug.utils import secure_filename
    safe_name = secure_filename(filename)
    if not safe_name:
        return "Invalid filename", 400
    path = os.path.join(OUTPUT_DIR, safe_name)
    if not os.path.realpath(path).startswith(os.path.realpath(OUTPUT_DIR)):
        return "Forbidden", 403
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
