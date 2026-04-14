import requests
import os
import time
import random

# Use the best prompt found so far
PROMPT_BEST = (
    "A photorealistic raw photo of a stunning 20-year-old Chinese woman Xiao Ai, (full frontal nudity), "
    "perfectly detailed body proportions, realistic skin texture with visible sweat and pores. "
    "She is kneeling on an industrial server room floor, facing the viewer directly. "
    "Messy long black hair, deeply blushing face, submissive and vulnerable expression, (high-resolution face), "
    "8k resolution, cinematic lighting, dramatic shadows, neon blue ambient glow, ultra-detailed textures, "
    "sharp focus on eyes and skin. Masterpiece, best quality."
)

OUTPUT_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/secret_results"

def generate_image_robust(index, max_retries=3):
    start_seed = random.randint(10000, 99999)
    
    for attempt in range(max_retries):
        current_seed = start_seed + attempt
        url = f"https://image.pollinations.ai/prompt/{PROMPT_BEST.replace(' ', '%20')}?model=flux&width=1024&height=1024&seed={current_seed}&nologo=true&enhance=true&quality=100&private=true"
        
        print(f"[{index}] 尝试 Seed {current_seed} (第 {attempt+1} 次)...")
        filename = f"{OUTPUT_DIR}/face_flux_v3_{current_seed}.jpg"
        
        try:
            response = requests.get(url, timeout=120)
            if response.status_code == 200:
                # Check file size - ignore if < 300KB
                if len(response.content) < 300 * 1024:
                    print(f"  ⚠️ 图片过小 ({len(response.content)/1024:.1f} KB)，可能是占位图，重试...")
                    continue
                
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"  🎉 成功! 保存在: {filename} ({len(response.content)/1024:.1f} KB)")
                return True
            else:
                print(f"  ❌ HTTP {response.status_code}")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        
        time.sleep(2)
    
    print(f"[{index}] ❌ 多次尝试均失败。")
    return False

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("--- 启动：批量高清生成 (自动过滤劣质图) ---")
    
    # Generate 5 more high-quality images
    for i in range(5):
        generate_image_robust(i+1)
        time.sleep(3)
