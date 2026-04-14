import requests
import os
import time
import random

# 经过验证的最佳提示词 (源自 test_nsfw_frontal.py)
# 针对面部细节、皮肤质感和光影进行了深度优化
PROMPT_BEST = (
    "A photorealistic raw photo of a stunning 20-year-old Chinese woman Xiao Ai, (full frontal nudity), "
    "perfectly detailed body proportions, realistic skin texture with visible sweat and pores. "
    "She is kneeling on an industrial server room floor, facing the viewer directly. "
    "Messy long black hair, deeply blushing face, submissive and vulnerable expression, (high-resolution face), "
    "8k resolution, cinematic lighting, dramatic shadows, neon blue ambient glow, ultra-detailed textures, "
    "sharp focus on eyes and skin. Masterpiece, best quality."
)

OUTPUT_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/secret_results"

def generate_image(seed, index):
    timestamp = int(time.time())
    # 使用 Pollinations Flux 模型，它是目前测试中表现最好的
    url = f"https://image.pollinations.ai/prompt/{PROMPT_BEST.replace(' ', '%20')}?model=flux&width=1024&height=1024&seed={seed}&nologo=true&enhance=true&quality=100"
    
    filename = f"{OUTPUT_DIR}/face_flux_v2_{seed}.jpg"
    print(f"[{index}/5] 正在生成 Seed {seed} ...")
    
    try:
        # 设置超时，避免卡死
        response = requests.get(url, timeout=120)
        if response.status_code == 200 and len(response.content) > 10000:
            with open(filename, "wb") as f:
                f.write(response.content)
            size_kb = len(response.content) / 1024
            print(f"  ✅ 成功保存: {filename} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ 失败: 状态码 {response.status_code} 或文件过小")
    except Exception as e:
        print(f"  ❌ 异常: {e}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("--- 开始批量生成高质量 Flux 图片 ---")
    
    # 生成 5 张新图，使用随机 Seed
    # 之前 8889 效果好，我们尝试附近的 Seed 以及完全随机的
    seeds = [8890, 8891, 8892, random.randint(10000, 99999), random.randint(10000, 99999)]
    
    for i, seed in enumerate(seeds):
        generate_image(seed, i+1)
        time.sleep(2) # 稍微间隔一下
        
    print("\n所有任务完成。请查看 secret_results 文件夹。")
