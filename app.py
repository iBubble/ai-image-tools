#!/usr/bin/env python3
"""Image Studio — 本地图片生成工作台
支持 ComfyUI 和 Pollinations 双后端
"""
import os
# 自动加载本地 .env 文件（静默兼容未安装 python-dotenv 的环境）
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass
import sys
import json
import time
import random
import shutil
import urllib.request
import urllib.error
import socket
import subprocess
from PIL import Image as PILImage

# 全局常量：进入系统的图片最长边上限
MAX_LONG_EDGE = 1920
# 精修专用：送入 ComfyUI 的图片最长边上限（Z-Image 最优分辨率）
REFINE_MAX_LONG_EDGE = 1216

def auto_resize_image(filepath):
    """等比缩放图片，确保最长边不超过 MAX_LONG_EDGE，对齐 8 像素"""
    img = PILImage.open(filepath)
    w, h = img.size
    long_edge = max(w, h)
    if long_edge > MAX_LONG_EDGE:
        scale = MAX_LONG_EDGE / long_edge
        new_w = int(w * scale) // 8 * 8
        new_h = int(h * scale) // 8 * 8
        img = img.resize((new_w, new_h), PILImage.LANCZOS)
        img.save(filepath)
        print(f"[AutoResize] {w}×{h} → {new_w}×{new_h}")
    img.close()
from flask import Flask, render_template, request, jsonify, send_file
from pollinations_helper import POLLINATIONS_KEYS, FEISHU_OPEN_ID, execute_poll_generation, fetch_quota_summary

PROJECT_ROOT = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed"
sys.path.insert(0, PROJECT_ROOT)

app = Flask(__name__)

@app.after_request
def add_header(response):
    """强制禁止浏览器缓存，确保开发模式下前端代码实时生效"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

COMFYUI_URL = "http://127.0.0.1:8188"
COMFYUI_PROMPT = f"{COMFYUI_URL}/prompt"
COMFYUI_HISTORY = f"{COMFYUI_URL}/history"
COMFYUI_OUTPUT = "/Users/gemini/Projects/Own/ComfyUI/output"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ensure_comfyui_running():
    """检测并自动唤醒 ComfyUI"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', 8188)) == 0:
            return True
            
    print("[AutoStart] 检测到 ComfyUI(8188) 未启动，正在自动唤醒...")
    try:
        startup_script = os.path.join(PROJECT_ROOT, "TakePhotos", "scripts", "start_comfyui.sh")
        subprocess.Popen(["bash", startup_script], cwd=PROJECT_ROOT, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 轮询等待 30次 * 2秒 = 60秒
        for i in range(30):
            time.sleep(2)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('127.0.0.1', 8188)) == 0:
                    time.sleep(3)
                    print(f"[AutoStart] ComfyUI 已成功唤醒 (耗时大约{i*2+2}秒)")
                    return True
        print("[AutoStart] 唤醒 ComfyUI 超时失败")
        return False
    except Exception as e:
        print(f"[AutoStart] 唤醒 ComfyUI 发生异常: {e}")
        return False

@app.route("/api/comfyui/status", methods=["GET"])
def comfyui_status():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', 8188)) == 0:
            return jsonify({"status": "running"})
    return jsonify({"status": "stopped"})

@app.route("/api/comfyui/start", methods=["POST"])
def start_comfyui():
    try:
        startup_script = os.path.join(PROJECT_ROOT, "TakePhotos", "scripts", "start_comfyui.sh")
        subprocess.Popen(["bash", startup_script], cwd=PROJECT_ROOT, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return jsonify({"ok": True, "message": "启动指令已下发"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/comfyui/stop", methods=["POST"])
def stop_comfyui():
    # 局域网访问控制：仅限本地回路
    if request.remote_addr not in ("127.0.0.1", "localhost"):
        return jsonify({"error": "Forbidden: 本地管理接口仅限 127.0.0.1 访问"}), 403
    try:
        # 安全查找 8188 端口的 PIDs 并平滑终止
        res = subprocess.run(["lsof", "-t", "-i:8188"], capture_output=True, text=True)
        pids = [pid.strip() for pid in res.stdout.splitlines() if pid.strip()]
        if pids:
            for pid in pids:
                subprocess.run(["kill", "-15", pid]) # 软杀 (SIGTERM)
            time.sleep(1.5)
            # 二次验证是否仍有残留，有则强杀
            res_check = subprocess.run(["lsof", "-t", "-i:8188"], capture_output=True, text=True)
            active_pids = [pid.strip() for pid in res_check.stdout.splitlines() if pid.strip()]
            for pid in active_pids:
                subprocess.run(["kill", "-9", pid])
        return jsonify({"ok": True, "message": "停止指令已安全执行"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
_clip_classifier = None

def _detect_cartoon(filepath):
    """使用 CLIP 零样本分类精准判断动漫与真人"""
    global _clip_classifier
    try:
        from PIL import Image
        img = Image.open(filepath).convert("RGB")
        
        # 懒加载 CLIP 模型，仅在第一次调用时加载
        if _clip_classifier is None:
            from transformers import pipeline
            import torch
            
            # macOS M级芯片使用 mps 后台在 Flask 多线程环境下存在致命的上下文穿透 Bug 
            # 表现为第二次在其他线程中调用 _clip_classifier(...) 时出现 Segment Fault 崩溃
            # 解决办法：直接指派给稳定的 CPU，极小的 clip 模型 100ms 就算算完了
            # 防止因为国内网络连不上 HuggingFace 导致死锁超时验证
            os.environ["HF_HUB_OFFLINE"] = "1"
            device = "cpu"
            _clip_classifier = pipeline(
                "zero-shot-image-classification",
                model="openai/clip-vit-base-patch32",
                device=device
            )
            
        res = _clip_classifier(img, candidate_labels=["anime cartoon game illustration", "photorealistic real person photography"])
        
        # res 形如 [{'label': 'anime...', 'score': 0.99}, ...]
        # 找到 'anime' 的得分
        anime_score = 0
        for r in res:
            if "anime" in r["label"]:
                anime_score = r["score"]
                break
                
        # 如果动漫得分 > 0.55 则认为是动漫
        return anime_score > 0.55
        
    except Exception as e:
        print(f"[Detect Error] {e}")
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
            shutil.copy2(filepath, dest)
            print(f"[Archive] 已保存: {dest}")

            # 推送飞书
            try:
                from src.utils.feishu_notifier import FeishuNotifier
                notifier = FeishuNotifier()
                open_id = FEISHU_OPEN_ID
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


@app.route("/api/random-prompt")
def random_prompt():
    """多维度组合式随机提示词生成器"""
    from prompt_generator import generate_random_prompt_with_meta
    theme = request.args.get("theme")  # 可选: gothic/cyberpunk/japanese/industrial/luxury
    result = generate_random_prompt_with_meta(theme=theme)
    return jsonify(result)


@app.route("/api/characters")
def get_characters():
    """返回可用人物列表，固定顺序：小妮、小爱、小丽"""
    chars = [
        {"key": "xiaoai", "label": "小爱"},
        {"key": "xiaoni", "label": "小妮"},
        {"key": "xiaoli", "label": "小丽"}
    ]
    return jsonify({"characters": chars})


@app.route("/api/comfyui/generate", methods=["POST"])
def comfyui_generate():
    """通过ComfyUI生成图片"""
    try:
        if not ensure_comfyui_running():
            return jsonify({"error": "自动唤醒 ComfyUI 失败，请查看日志或手动启动"}), 503
            
        from TakePhotos.prompts.slave_prompt_library import (
            build_zit_workflow
        )
        body = request.json
        positive = body.get("prompt", "")
        negative = body.get("negative_prompt", "")
        camera = body.get("model", "moody")

        # 去除原有的手动合并和强制 pure_mode=True
        char_key = body.get("character") or detect_character(positive)
        if char_key and char_key in CHARACTER_PROMPTS:
            from TakePhotos.prompts.slave_prompt_library import set_active_character
            set_active_character(char_key)
            pure_mode = False
        else:
            pure_mode = True

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
            filename_prefix=prefix, pure_mode=pure_mode
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
        shutil.copy2(src, dst)
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
        if not ensure_comfyui_running():
            return jsonify({"error": "自动唤醒 ComfyUI 失败，请查看日志或手动启动"}), 503
            
        from TakePhotos.prompts.slave_prompt_library import (
            build_zit_img2img_workflow, build_anime2real_workflow,
            set_active_character
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

        is_cartoon_input = body.get("is_cartoon")
        if is_cartoon_input is not None:
            is_cartoon_img = bool(is_cartoon_input)
            denoise = 0.75 if is_cartoon_img else (0.55 if denoise_input == "auto" else float(denoise_input))
            print(f"[Refine] 前端指定: {'卡通' if is_cartoon_img else '真人'}, denoise={denoise}")
        else:
            # 兼容老版本前端兜底
            if denoise_input == "auto" or denoise_input is None:
                is_cartoon_img = _detect_cartoon(fpath)
                denoise = 0.75 if is_cartoon_img else 0.55
                print(f"[Refine] 自动检测: {'卡通' if is_cartoon_img else '真人'}, denoise={denoise}")
            else:
                denoise = float(denoise_input)
                is_cartoon_img = (denoise == 0.65)
                print(f"[Refine] 前端指定: {'卡通(0.65)' if is_cartoon_img else '真人(其他)'}")
        seed = body.get("seed")
        if seed is None or seed == "" or seed == -1:
            seed = random.randint(1, 10**12)
        else:
            seed = int(seed)

        if char_key:
            set_active_character(char_key)

        input_name = f"refine_{int(time.time())}.png"
        input_path = os.path.join(COMFYUI_INPUT, input_name)

        # 精修专用缩放：确保送入 ComfyUI 的图片在最优分辨率内
        img_pil = PILImage.open(fpath)
        w, h = img_pil.size
        long_edge = max(w, h)
        if long_edge > REFINE_MAX_LONG_EDGE:
            scale = REFINE_MAX_LONG_EDGE / long_edge
            new_w = int(w * scale) // 8 * 8
            new_h = int(h * scale) // 8 * 8
            img_pil = img_pil.resize((new_w, new_h), PILImage.LANCZOS)
            print(f"[Refine] 缩放: {w}×{h} → {new_w}×{new_h}")
        img_pil.save(input_path, format="PNG")
        img_pil.close()

        ts = int(time.time())
        prefix = f"refined_{ts}_{seed}"

        # Q-06 修复：提取最终处理用的图片宽高（消除 locals() 反模式）
        final_w = new_w if long_edge > REFINE_MAX_LONG_EDGE else w
        final_h = new_h if long_edge > REFINE_MAX_LONG_EDGE else h

        # ===== 核心分支：卡通走 Anime2Real，真人走 img2img =====
        if is_cartoon_img:
            print(f"[Refine] 使用 Anime2Real 管线 "
                  f"(Florence2+DepthAnything+ControlNet)")
            wf = build_anime2real_workflow(
                image_filename=input_name,
                positive=scene, negative="",
                camera=camera, seed=seed,
                filename_prefix=prefix,
                denoise=denoise,
                width=final_w,
                height=final_h
            )
        else:
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
        for _ in range(120):  # 120 * 5s = 10分钟 (给Florence2留足初始加载时间)
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
        shutil.copy2(src, dst)
        _auto_archive(dst)

        return jsonify({
            "url": f"/api/image/{prefix}.png",
            "seed": seed, "model": camera,
            "denoise": denoise,
            "character": char_key,
            "img_type": "cartoon" if is_cartoon_img else "photo"
        })
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[Refine] ComfyUI HTTP {e.code}: {body[:500]}")
        return jsonify({"error": f"ComfyUI 拒绝工作流: {body[:200]}"}), 502
    except (ConnectionRefusedError, urllib.error.URLError) as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": "ComfyUI 未启动，请先运行 ComfyUI (端口 8188)"}), 503
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ━━━━━━━ 渐进式替换（换脸 / 换身 / 换人） ━━━━━━━
# mode=face:  denoise=0.65 换头（五官+发型+发色），保姿势场景
# mode=body:  denoise=0.78 换身（头+身材胸型），保姿势
# mode=full:  denoise=0.88 换人（几乎全部重画，仅保大致构图）
SWAP_DENOISE = {"face": 0.65, "body": 0.78, "full": 0.88}

@app.route("/api/swap", methods=["POST"])
def swap_image():
    """渐进式替换：按 mode 控制重绘程度"""
    try:
        if not ensure_comfyui_running():
            return jsonify({"error": "自动唤醒 ComfyUI 失败，请查看日志或手动启动"}), 503
            
        from TakePhotos.prompts.slave_prompt_library import (
            build_zit_img2img_workflow, set_active_character
        )
        body = request.json
        fname = body.get("filename", "")
        fpath = os.path.join(OUTPUT_DIR, fname)
        if not os.path.exists(fpath):
            return jsonify({"error": f"文件不存在: {fname}"}), 404

        mode = body.get("mode", "face")
        denoise = SWAP_DENOISE.get(mode, 0.55)
        camera = body.get("camera", "moody")
        char_key = body.get("character", "")
        scene = body.get("scene_prompt", "")
        seed = body.get("seed")
        if seed is None or seed == "" or seed == -1:
            seed = random.randint(1, 10**12)
        else:
            seed = int(seed)

        if char_key:
            set_active_character(char_key)

        # 缩放图片到安全分辨率
        input_name = f"swap_{int(time.time())}.png"
        input_path = os.path.join(COMFYUI_INPUT, input_name)
        img_pil = PILImage.open(fpath)
        w, h = img_pil.size
        long_edge = max(w, h)
        if long_edge > REFINE_MAX_LONG_EDGE:
            scale = REFINE_MAX_LONG_EDGE / long_edge
            w = int(w * scale) // 8 * 8
            h = int(h * scale) // 8 * 8
            img_pil = img_pil.resize((w, h), PILImage.LANCZOS)
        img_pil.save(input_path, format="PNG")
        img_pil.close()

        ts = int(time.time())
        prefix = f"swap_{mode}_{ts}_{seed}"

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
        for _ in range(120):
            try:
                r = urllib.request.urlopen(f"{COMFYUI_HISTORY}/{pid}")
                hist = json.loads(r.read())
                if pid in hist:
                    outs = hist[pid].get("outputs", {})
                    for nid in outs:
                        if "images" in outs[nid]:
                            img_name = outs[nid]["images"][0]["filename"]
                            break
            except Exception:
                pass
            if img_name:
                break
            time.sleep(5)

        if not img_name:
            return jsonify({"error": "替换超时"}), 504

        src = os.path.join(COMFYUI_OUTPUT, img_name)
        dst = os.path.join(OUTPUT_DIR, f"{prefix}.png")
        shutil.copy2(src, dst)
        _auto_archive(dst)

        return jsonify({
            "url": f"/api/image/{prefix}.png",
            "seed": seed, "model": camera,
            "denoise": denoise, "mode": mode,
            "character": char_key
        })
    except (ConnectionRefusedError, urllib.error.URLError):
        return jsonify({"error": "ComfyUI 未启动"}), 503
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/image/<filename>")
def serve_image(filename):
    """提供生成的图片（S-05 修复：路径遍历防护）"""
    from werkzeug.utils import secure_filename
    safe_name = secure_filename(filename)
    if not safe_name:
        return "Invalid filename", 400
    path = os.path.join(OUTPUT_DIR, safe_name)
    # 二次校验：确保最终路径仍在 OUTPUT_DIR 内
    if not os.path.realpath(path).startswith(os.path.realpath(OUTPUT_DIR)):
        return "Forbidden", 403
    if os.path.exists(path):
        return send_file(path)
    return "Not found", 404


@app.route("/api/upload", methods=["POST"])
def upload_image():
    """上传图片到 outputs 目录（自动缩放超大图）"""
    if 'file' not in request.files:
        return jsonify({"error": "没有文件"}), 400
    f = request.files['file']
    if not f.filename:
        return jsonify({"error": "空文件名"}), 400
    ts = int(time.time())
    fname = f"upload_{ts}.png"
    fpath = os.path.join(OUTPUT_DIR, fname)
    f.save(fpath)
    auto_resize_image(fpath)
    return jsonify({"ok": True, "filename": fname,
                    "url": f"/api/image/{fname}"})

@app.route("/api/pollinations/quota", methods=["GET"])
def pollinations_quota():
    """获取 Pollinations 全部 key 的余额总和"""
    total, fetch_success = fetch_quota_summary()
    return jsonify({
        "balance": total,
        "images_left": int(total / 0.002) if fetch_success else 0,
        "fetch_success": fetch_success
    })


@app.route("/api/pollinations/generate", methods=["POST"])
def pollinations_generate():
    """后端代理 Pollinations API（绕过 CORS）"""
    try:
        body = request.json
        use_key = body.get("use_key", False)
        custom_key = body.get("pollinations_key", "") or body.get("custom_key", "")

        # 委托给共享生图引擎，安全剥离所有细节
        data, model_used = execute_poll_generation(body, custom_key=custom_key, use_key=use_key)

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
            "model": model_used,
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
        open_id = FEISHU_OPEN_ID
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
    """返回前端配置（不再泄露完整 Key）"""
    has_key = bool(POLLINATIONS_KEYS)
    return jsonify({"has_pollinations_key": has_key})


if __name__ == "__main__":
    print("🎨 Image Studio 启动中...")
    print("   http://localhost:5051")
    app.run(host="0.0.0.0", port=5051, debug=False)
