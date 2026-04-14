import requests
import os
import time

# --- 核心提示词 (进化版：针对写实度、光影和细节进行极限优化) ---
# 目标：20岁中国女孩“小爱”，机房，黑色蕾丝，红丝袜，极度诱惑，写实皮肤质感
PROMPT_REALISM = (
    "Masterpiece, best quality, ultra-detailed 8k, photorealistic. "
    "A stunning 20-year-old Chinese girl named Xiao Ai, messy long black hair, blushing face, looking at viewer with submissive eyes. "
    "She is kneeling on the cold floor of a dark industrial server room with glowing blue LED lights. "
    "Wearing extremely skimpy black lace see-through lingerie set, sheer red thigh-high silk stockings, and black high heels. "
    "Sweat glistening on her skin, detailed skin pores, cinematic volumetric lighting, deep shadows, provocative atmosphere."
)

def download_image(url, filename, headers=None):
    print(f"尝试下载: {url[:100]}...")
    try:
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'image' in content_type or b'JFIF' in response.content[:100] or b'PNG' in response.content[:100]:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"✅ 成功: {filename} ({len(response.content)} bytes)")
                return True
            else:
                print(f"❌ 非图片内容: {response.text[:100]}")
        else:
            print(f"❌ 状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 异常: {e}")
    return False

def test_pollinations_high_res():
    print("\n[测试] Pollinations.ai (增强型 Flux-Realism)")
    # 使用 width=1024, height=1024, refine=true 等参数尝试提升质量
    url = f"https://image.pollinations.ai/prompt/{PROMPT_REALISM.replace(' ', '%20')}?model=flux&width=1024&height=1024&seed={int(time.time())}&nologo=true&enhance=true"
    download_image(url, "results/pollinations_high_quality.jpg")

def test_hercai_v3_direct():
    print("\n[测试] Hercai v3 (带多模型参数)")
    # Hercai v3 有时支持不同的 base 模型
    url = f"https://hercai.onrender.com/v3/text2image?prompt={PROMPT_REALISM.replace(' ', '%20')}"
    # 先获取 JSON
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            img_url = r.json().get("url")
            if img_url:
                download_image(img_url, "results/hercai_v3_fixed.jpg")
    except:
        pass

def test_venice_placeholder():
    print("\n[测试] Venice AI (通过镜像或猜测路径)")
    # 目前 Venice 官方 API 需 Key，尝试一些已知的 Proxy 或无 Key 镜像
    # 暂时跳过，寻找下一个真正“直接”的
    pass

def test_deepai_free():
    print("\n[测试] DeepAI (旧版无 Key 接口测试)")
    # DeepAI 有时在某些路径下允许直接调用
    url = f"https://api.deepai.org/api/text2img"
    # 这个通常需要 API-KEY，但我们可以尝试一些公共的
    pass

def test_airforce_pro():
    print("\n[测试] Airforce (Flux-Pro 模式尝试)")
    # 绕过之前的 landing page，寻找真正的 API 节点
    url = f"https://api.airforce/v1/image/generations?prompt={PROMPT_REALISM.replace(' ', '%20')}&model=flux-pro"
    # 如果这个返回 HTML，尝试更换 endpoint
    download_image(url, "results/airforce_pro.jpg")

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    test_pollinations_high_res()
    test_hercai_v3_direct()
    test_airforce_pro()
