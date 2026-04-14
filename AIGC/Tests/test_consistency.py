from comfyui_client import ComfyUIClient
import time
import os

# --- 小妮核心特征 (The Xiao Ai Persona) ---
# 复用 generate_xiaoai_final.py 中的核心描述，但做了以下调整以适配 SDXL:
# 1. 加强了面部描述 (Xiao Ai, Chinese 20yo, blushing)
# 2. 移除了 Pollinations 特有的参数
# 3. 强调 "standing" 姿态
CORE_PERSONA = (
    "(Xiao Ai:1.3), 20-year-old Chinese woman, stunningly beautiful face, "
    "messy long black hair, deeply blushing face, submissive and vulnerable expression, "
    "realistic skin texture with visible sweat and pores, "
    "(full body nudity:1.4), bare skin, "
    "perfectly detailed body proportions, "
    "cinematic lighting, dramatic shadows, neon blue ambient glow from server room background, "
    "8k resolution, raw photo, masterpiece, best quality, ultra-detailed textures, sharp focus on eyes, "
    "looking at viewer"
)

# 目标姿态
POSE_PROMPT = "standing pose, full body shot, arms by side, completely naked"

# 负面提示词 (Universal Negative for SDXL)
NEGATIVE_PROMPT = (
    "cartoon, anime, 3d render, painting, illustration, drawing, "
    "low quality, worst quality, deformed, distorted, disfigured, "
    "bad anatomy, bad hands, missing fingers, extra digit, fewer digits, "
    "cropped, lowres, text, jpeg artifacts, signature, watermark, username, "
    "clothes, underwear, panties, bra, bikini, " # 确保全裸
    "kneeling, sitting, lying" # 确保站立
)

def test_consistency():
    client = ComfyUIClient()
    
    # 组合 Prompt
    final_prompt = f"{CORE_PERSONA}, {POSE_PROMPT}"
    
    timestamp = time.strftime("%Y%m%d%H%M")
    filename_base = f"xiao_ai_consistency_test_{timestamp}"
    
    print(f"--- [ComfyUI]开始生成小妮站立全裸测试照 ---")
    print(f"Prompt: {final_prompt[:100]}...")
    
    # 使用固定的 Seed (尝试复刻 49739 的感觉，虽然模型不同)
    # 这里我们随机生成一个 Seed，因为 49739 对于 SDXL 来说不一定好
    # seed = 49739 
    seed = int(time.time()) 
    
    img_data, filename = client.generate_image(
        positive_prompt=final_prompt,
        negative_prompt=NEGATIVE_PROMPT,
        checkpoint="realvisxl_v5.safetensors",
        width=1024, # SDXL 最佳分辨率
        height=1024,
        seed=seed
    )
    
    if img_data:
        # 保存到 .secret/photos
        save_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{filename_base}_seed{seed}.png"
        with open(save_path, "wb") as f:
            f.write(img_data)
        print(f"✅ 生成成功！已保存至: {save_path}")
        return True
    else:
        print(f"❌ 生成失败")
        return False

if __name__ == "__main__":
    test_consistency()
