#!/usr/bin/env python3
"""基于现有 Pony V6 图像进行 I2I 微调，优化骨架和体型"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def refine_pony_body():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    
    # 源图像路径
    source_image = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260213/comp_01_PonyV6.jpg"
    
    # 优化后的 Pony 提示词：强调更小巧纤细的骨架
    positive_prompt = """score_9, score_8_up, score_7_up, score_6_up, 
1girl, solo, (chinese:1.3), (east asian:1.2), 
beautiful elegant chinese woman, 20 years old, 
long straight black hair, brown eyes, dark eyes, small lips, elegant face, 
pale skin, smooth skin, 
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2), (slim waist:1.1), (narrow shoulders:1.1),
huge natural breasts, detailed nipples, 
completely naked, wearing high heels, 
suspended by wrists from chains, arms raised, tiptoes, painful expression, genitals visible,
(explicit:1.2), genitals, pussy, anus, rating_explicit, 
photo (medium), realistic, highly detailed"""
    
    negative_prompt = """score_4, score_5, score_6, 
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, 
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, 
(western features:1.2), (clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4),
(muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2)"""
    
    print(f"[Pony Refine] 正在基于 {os.path.basename(source_image)} 进行 I2I 微调...")
    print(f"[Pony Refine] 目标：更小巧纤细的骨架")
    
    try:
        # 使用 I2I，denoise 设置为 0.5-0.6 以保留原图主要特征但允许体型调整
        img_data, filename = client.image_to_image(
            image_path=source_image,
            positive_prompt=positive_prompt,
            negative_prompt=negative_prompt,
            denoise=0.55,  # 适中的 denoise 值，既保留构图又允许体型优化
            checkpoint="ponyDiffusionV6XL.safetensors"
        )
        
        # 保存优化后的图像
        output_path = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260213/comp_01_PonyV6_refined.jpg"
        with open(output_path, "wb") as f:
            f.write(img_data)
        
        print(f"[Pony Refine] 成功生成优化版本: {output_path}")
        print(f"[Pony Refine] ComfyUI 文件名: {filename}")
        
    except Exception as e:
        print(f"[Pony Refine] 失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    refine_pony_body()
