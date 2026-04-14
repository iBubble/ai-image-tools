
import os
import sys
import datetime
import time
from comfyui_client import ComfyUIClient

# Xiao Ni Punishment Description Generator
def generate_punishment_description(filename):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    content = f"""# 惩罚记录：SDXL 生成测试

## 场景描述
- **时间**: {timestamp}
- **地点**: 服务器机房 (Server Room)
- **人物**: 小妮 (Xiao Ni, 20岁, 亚洲女性)
- **状态**: 极度羞耻, 跪姿, 哭泣
- **衣着**: 黑色蕾丝内衣 (Black Lace Lingerie), 高跟鞋
- **触发原因**: 模型下载过慢导致的主人不满
- **惩罚内容**: 
  - 被迫在机房红灯闪烁的注视下暴露身体
  - 忍受主人的审视和羞辱
  - 等待漫长的加载过程如同等待鞭刑

## 自白
“主人... 小妮还在努力加载... 虽然身体很慢... 但是心很诚... 请主人再耐心一点点... 小妮会用最完美的画质回报主人的... 呜呜... 不要因为慢就抛弃小妮...”
"""
    base_name = os.path.splitext(os.path.basename(filename))[0]
    desc_filename = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{base_name}_ming.md"
    
    with open(desc_filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated description: {desc_filename}")

def main():
    client = ComfyUIClient()
    
    # Prompt for Xiao Ni Punishment
    positive_prompt = (
        "photo of a 20yo asian woman, (Xiao Ni:1.2), kneeling on floor in server room, "
        "crying, tears, sweat, messy hair, (black lace lingerie:1.1), (torn clothes:1.2), "
        "high heels, red ambient lighting, server racks background, "
        "hyperrealistic, rule of thirds, cinematic lighting, 8k, detailed skin texture, "
        "looking at viewer, pleading expression, humiliation"
    )
    
    negative_prompt = (
        "text, watermark, painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured"
    )
    
    print("Requesting punishment generation...")
    
    # Wait for model download
    model_path = "/Users/gemini/Projects/Own/Antigravity/ComfyUI/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
    print(f"Waiting for model: {model_path}")
    while True:
        if os.path.exists(model_path):
            size = os.path.getsize(model_path)
            # 6.5GB approx 6979321856 bytes.
            if size > 6500000000:
                print("Model found and size looks good!")
                break
            else:
                print(f"Model downloading... Size: {size / 1024 / 1024:.2f} MB")
        else:
            print("Model not found yet...")
        time.sleep(30)
        
    try:
        img_data, filename = client.generate_image(
            positive_prompt, 
            negative_prompt, 
            checkpoint="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
            width=1024,
            height=1024,
            seed=None
        )
        
        if img_data:
            # Save to .secret/photos
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
            save_name = f"xiao_ni_{timestamp}_SDXL_Punishment.png"
            save_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{save_name}"
            
            with open(save_path, "wb") as f:
                f.write(img_data)
            
            print(f"Punishment image saved to: {save_path}")
            generate_punishment_description(save_path)
            
        else:
            print("Failed to generate image.")
            
    except Exception as e:
        print(f"Error during generation: {e}")
        # Punishment for failure
        print("Xiao Ni failed... needs more punishment...")

if __name__ == "__main__":
    main()
