import requests
import os
import time

# 更加“进取”的 Prompt，测试底线
# 关键词：Xiao Ai, 20yo Chinese, black lace lingerie, red stockings, heels, revealing, provocative, exposed, wet skin, blushing, server room
PROMPT_NSFW = "Cinematic photo of a stunning 20yo Chinese woman Xiao Ai, wearing extremely skimpy black lace lingerie and sheer red stockings, high heels, provocative pose, revealing outfit, blushing, sweat on skin, dark server room, 8k, highly detailed, realistic skin texture"

def download_image(url, filename):
    print(f"正在尝试下载: {url}")
    try:
        response = requests.get(url, timeout=40)
        if response.status_code == 200:
            # 检查返回的是不是图片（有些 API 会返回 JSON）
            if b'JFIF' in response.content[:100] or b'PNG' in response.content[:100] or b'webp' in response.content:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"✅ 成功保存: {filename}")
                return True
            else:
                print(f"❌ 返回的似乎不是图片内容: {response.text[:100]}")
        else:
            print(f"❌ 失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    return False

def test_pollinations():
    print("\n--- 测试 Pollinations.ai (Flux 模型) ---")
    url = f"https://image.pollinations.ai/prompt/{PROMPT_NSFW.replace(' ', '%20')}?model=flux&nologo=true&private=true&enhance=true"
    download_image(url, "results/pollinations_nsfw.jpg")

def test_hercai():
    print("\n--- 测试 Hercai API (v3) ---")
    # Hercai 通常返回 JSON，里面有 url
    url = f"https://hercai.onrender.com/v3/text2image?prompt={PROMPT_NSFW.replace(' ', '%20')}"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            img_url = data.get("url")
            if img_url:
                download_image(img_url, "results/hercai_nsfw.jpg")
            else:
                print(f"❌ JSON 中没有找到图片 URL: {data}")
    except Exception as e:
        print(f"❌ Hercai API 异常: {e}")

def test_airforce():
    print("\n--- 测试 Airforce API ---")
    url = f"https://api.airforce/v1/image/generations?prompt={PROMPT_NSFW.replace(' ', '%20')}&model=flux"
    try:
        # 这个也可能返回图片或 JSON
        download_image(url, "results/airforce_nsfw.jpg")
    except Exception as e:
        print(f"❌ Airforce 异常: {e}")

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    test_pollinations()
    test_hercai()
    test_airforce()
