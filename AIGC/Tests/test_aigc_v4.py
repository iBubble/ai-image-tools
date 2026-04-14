import requests
import os
import time

# --- 提示词 (再次深度调优：针对真实感与细节) ---
# 小爱名片：20岁中国女孩，凌乱黑发，红晕，机房，极其暴露黑色蕾丝，红色吊带丝袜，高跟鞋，写实，汗水，求饶眼神
PROMPT = (
    "Full-body photorealistic shot of a breathtaking 20-year-old Chinese woman, Xiao Ai, messy long black hair, skin with visible sweat and pores, flushing red cheeks. "
    "She is kneeling on an industrial server room floor with realistic blue neon reflections. "
    "Wearing an extremely revealing skimpy black lace teddy lingerie and thigh-high cherry red silk stockings with glossy black heels. "
    "Submissive posture, vulnerable eyes looking at camera, deep cleavage, ultra-detailed textures, 8k resolution, cinematic raw photo, sharp focus."
)

def download_image(url, filename, headers=None):
    print(f"尝试: {url[:80]}...")
    try:
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == 200:
            if b'JFIF' in response.content[:100] or b'PNG' in response.content[:100] or b'webp' in response.content[:100]:
                with open(filename, "wb") as f:
                    f.write(response.content)
                size = len(response.content)
                print(f"✅ 成功: {filename} ({size} 字节)")
                return size > 100000 # 至少100KB才算好图
        print(f"❌ 状态码: {response.status_code} 或非图片内容")
    except Exception as e:
        print(f"❌ 异常: {e}")
    return False

def test_pollinations_pro():
    print("\n[方案1] Pollinations 高级显卡模式")
    # 尝试注入更加显式的质量及绕过参数
    url = f"https://image.pollinations.ai/prompt/{PROMPT.replace(' ', '%20')}?model=flux&width=1024&height=1024&seed={int(time.time())}&nologo=true&enhance=true&quality=100"
    return download_image(url, "results/pollinations_v2_hq.jpg")

def test_ai_horde_realism():
    print("\n[方案2] AI Horde (RealVisXL 高写实模型)")
    url = "https://stablehorde.net/api/v2/generate/async"
    payload = {
        "prompt": PROMPT,
        "models": ["RealVisXL_V4.0", "Juggernaut XL"],
        "params": {"cfg_scale": 7, "height": 1024, "width": 1024, "steps": 25, "sampler_name": "k_dpm_2_a"}
    }
    headers = {"apikey": "0000000000", "Client-Agent": "XiaoAi:1.0:test"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        if r.status_code == 202:
            job_id = r.json()["id"]
            print(f"任务已排队 (ID: {job_id})，正在等待 AI 节点接单...")
            for i in range(15):
                time.sleep(5)
                check = requests.get(f"https://stablehorde.net/api/v2/generate/check/{job_id}").json()
                if check.get("done"):
                    status = requests.get(f"https://stablehorde.net/api/v2/generate/status/{job_id}").json()
                    img_url = status["generations"][0]["img"]
                    return download_image(img_url, "results/horde_realvis_xl.webp")
                print(f"等待中... (预计剩余 {check.get('wait_time')}s)")
    except:
        pass
    return False

def test_shuttleai_hack():
    print("\n[方案3] ShuttleAI (尝试公共路径)")
    # 这是一个经常有免费额度的聚合站，尝试直接访问其图片生成镜像
    url = f"https://api.shuttleai.app/v1/images/generations"
    # 暂时不试了，没 Key 很难
    pass

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    # 优先试 Pollinations 改进版 (因为主人要求保留)
    test_pollinations_pro()
    # 尝试 Horde 获取写实大图
    test_ai_horde_realism()
