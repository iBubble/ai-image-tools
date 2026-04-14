import os
import requests
import sys
import urllib.parse
import glob

API_KEY = "sk_pmBF6hTFDV0UFDFGHRsTHTlPG4GYP9ej"

# 1. 精准化寻找本地图片
target_filename = "poll_1776020344_1054217240.jpg"
file_path = None
# 递归查找该文件所在的确切路径
found_files = glob.glob(f"**/{target_filename}", recursive=True)
if found_files:
    file_path = os.path.abspath(found_files[0])
else:
    # 尝试在特定目录强制匹配
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fallback_path = os.path.join(base_dir, "outputs", "20260413", target_filename)
    if os.path.exists(fallback_path):
        file_path = fallback_path

if not file_path:
    print(f"❌ 找不到图片文件: {target_filename}")
    sys.exit(1)

print(f"[*] 🔍 已找到本地图源: {file_path}")

# 2. 上传图片到 Pollinations 内置存储节点
upload_url = "https://media.pollinations.ai/upload"
headers = {"Authorization": f"Bearer {API_KEY}"}

print("[*] 🌐 正在将本地图片隐秘上传至 Pollinations 媒体服务器...")
online_url = None
try:
    with open(file_path, "rb") as f:
        # 使用 multipart/form-data 方式上传
        upload_resp = requests.post(upload_url, headers=headers, files={"file": f})
        
        if upload_resp.status_code == 200:
            upload_data = upload_resp.json()
            online_url = upload_data.get("url")
            print(f"[+] ✅ 上传成功！CDN 地址: P链 ({upload_data.get('size')} bytes)")
        else:
            print(f"❌ 上传失败，状态码: {upload_resp.status_code}")
            print(upload_resp.text)
            sys.exit(1)
except Exception as e:
    print(f"❌ 上传崩溃: {e}")
    sys.exit(1)


# 3. 使用该公网 URL 作为 Image 参考，请求高动态视频
PROMPT = "The character in the image starts moving dynamically, continuously waving hands, turning head naturally, smiling, eyes opening and closing, highly detailed body animation, smooth action."
# 核心纠错：ltx-2 在平台底层只接了 Prompt，静默丢弃了 Image 参！
# 必须更换为阿里开源、官方明确打上 text/image-to-video 支持标签的 wan 框架
MODEL = "wan"
DURATION = 2

safe_prompt = urllib.parse.quote(PROMPT)
gen_url = f"https://gen.pollinations.ai/image/{safe_prompt}"

params = {
    "model": MODEL,
    "image": online_url,
    "duration": DURATION
}

print("=" * 50)
print(f"[*] 🚀 正在拉取图生视频进行 {DURATION}秒 动作渲染...")
print(f"[*] 🎬 使用模型: {MODEL}")
print(f"[*] 💡 提示词: {PROMPT}")
print("[*] ⏳ 长轮询渲染中，这通常需要 1 到 2 分钟，请主子稍等...")

try:
    response = requests.get(gen_url, params=params, headers=headers)
    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "")
        ext = "mp4" if "video" in content_type else "jpg"
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"test_{MODEL}_custom2s.{ext}")
        
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        print(f"\n[+] 🎉 渲染出炉！视频已完美落盘至: {save_path}")
        print("\n[-] 📊 本次扣费信息: ")
        for k, v in response.headers.items():
            if "x-usage" in k.lower():
                print(f"    - {k}: {v}")
    else:
        print(f"\n[!] ❌ 渲染请求失败！状态码: {response.status_code}")
        print("详细:", response.text[:200])
except Exception as e:
    print(f"\n[!] 💥 请求异常: {e}")
