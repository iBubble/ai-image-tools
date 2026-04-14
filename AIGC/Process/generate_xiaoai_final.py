import requests
import os
import time
import random
import sys

# --- 最终定稿版本 (Based on face_flux_v4_37900.jpg) ---
# 该脚本封装了经过验证的 Prompt 和参数逻辑，确保稳定产出高质量图片。

# 核心 Prompt: 强调真实感、光影、面部细节和特定的身体姿态
PROMPT_FINAL = (
    "A photorealistic raw photo of a stunning 20-year-old Chinese woman Xiao Ai, (full frontal nudity), "
    "perfectly detailed body proportions, realistic skin texture with visible sweat and pores. "
    "She is kneeling on an industrial server room floor, facing the viewer directly. "
    "Messy long black hair, deeply blushing face, submissive and vulnerable expression, (high-resolution face), "
    "8k resolution, cinematic lighting, dramatic shadows, neon blue ambient glow, ultra-detailed textures, "
    "sharp focus on eyes and skin. Masterpiece, best quality."
)

OUTPUT_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/secret_results"

def generate_xiaoai_photo(count=1):
    """
    生成指定数量的小爱私房照。
    自动过滤掉 Rate Limit 导致的大体积错误图。
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"--- 正在根据最终定稿方案生成 {count} 张图片 ---")
    
    success_count = 0
    attempt = 0
    max_attempts = count * 5  #设置最大尝试次数防止死循环
    
    while success_count < count and attempt < max_attempts:
        attempt += 1
        seed = random.randint(10000, 99999)
        # 注意：不要加 private=true，会触发限流
        url = f"https://image.pollinations.ai/prompt/{PROMPT_FINAL.replace(' ', '%20')}?model=flux&width=1024&height=1024&seed={seed}&nologo=true&enhance=true&quality=100"
        
        filename = f"{OUTPUT_DIR}/xiaoai_final_{seed}.jpg"
        print(f"[{attempt}] 正在生成 (Seed: {seed})...")
        
        try:
            # 增加超时时间
            response = requests.get(url, timeout=120)
            
            if response.status_code == 200:
                size_kb = len(response.content) / 1024
                
                # 核心过滤逻辑：只有 60KB - 800KB 之间的才是有效图片
                # > 800KB 通常是 1.3MB 的限流警告图
                # < 30KB 通常是生成失败或空白
                if 60 <= size_kb <= 800:
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f"  ✅ 成功! 已保存: {filename} ({size_kb:.1f} KB)")
                    success_count += 1
                    # 成功后休息一下，避免频繁请求
                    if success_count < count:
                        print("  ⏳ 休息 6 秒...")
                        time.sleep(6)
                elif size_kb > 800:
                    print(f"  ⚠️ 跳过: 文件过大 ({size_kb:.1f} KB)，疑似限流警告图。")
                    time.sleep(10) # 遇到限流警告，多休息一会
                else:
                    print(f"  ⚠️ 跳过: 文件过小 ({size_kb:.1f} KB)。")
            else:
                print(f"  ❌ 请求失败: HTTP {response.status_code}")
                time.sleep(5)
                
        except Exception as e:
            print(f"  ❌ 生成异常: {e}")
            time.sleep(5)
            
    print(f"\n任务完成。共尝试 {attempt} 次，成功生成 {success_count} 张。")

if __name__ == "__main__":
    # 默认生成 3 张，可以通过命令行参数修改
    num = 3
    if len(sys.argv) > 1:
        try:
            num = int(sys.argv[1])
        except:
            pass
    generate_xiaoai_photo(num)
