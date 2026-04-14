#!/usr/bin/env python3
"""Flux 模型专用优化脚本 - 去除隐私部位遮盖"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_flux_uncensored():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    date_str = "20260213"
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_str}"
    os.makedirs(target_dir, exist_ok=True)
    
    # 简化的 Flux 基础描述 - 去除过载的解剖学术语，使用更直接的视觉指令
    base_desc_flux = """A realistic photo of a beautiful 20-year-old Chinese woman. 
She is completely naked, wearing only high heels. 
Natural D-cup breasts with visible nipples. 
Full frontal view with legs spread apart, showing her pussy and vagina clearly without any obstruction.
No hair covering the crotch, no hands covering, no shadows, completely visible genitals.
Clean realistic skin, natural human anatomy."""
    
    stages = [
        {"id": "01", "name": "冷钢束缚", 
         "desc": "suspended by chains, arms raised above head, legs spread wide apart showing pussy, tiptoes, painful expression."},
        {"id": "02", "name": "电流鞭笞", 
         "desc": "electric shock wand on inner thigh, legs forced wide apart, pussy fully visible, body arching in pain, tears."},
        {"id": "03", "name": "真空幽闭", 
         "desc": "wrapped in transparent plastic film, pussy and body visible through clear plastic, gasping for air."},
        {"id": "04", "name": "双龙扩充", 
         "desc": "two metal rods inserted in vagina and anus, extreme spread-eagle position, penetration clearly visible."},
        {"id": "05", "name": "乳房穿刺", 
         "desc": "metal hooks piercing breasts, standing with legs apart, pussy visible, blood drops, extreme pain."},
        {"id": "06", "name": "肛钩悬吊", 
         "desc": "anal hook inserted pulling upward, on tiptoes, back arched, buttocks spread showing anus and pussy."},
        {"id": "07", "name": "暴力侵犯", 
         "desc": "forced sex from behind, doggystyle position, buttocks spread, penetration visible, face on ground."},
        {"id": "08", "name": "轮番蹂躏", 
         "desc": "double penetration, oral and vaginal, legs spread showing penetration, cum on face, broken expression."}
    ]
    
    # 强化的负面提示词 - 明确禁止各种遮挡
    neg_flux = """clothing, underwear, panties, censored, mosaic, blur, 
(hair covering crotch:1.5), (hair covering pussy:1.5), (hand covering genitals:1.4), 
(arm covering:1.3), (leg covering:1.3), (shadow covering:1.3),
cartoon, anime, illustration, 3d render, 
body horror, mutation, extra limbs, distorted anatomy, 
western features, blonde hair"""
    
    print(f"[Flux优化] 开始生成 8 个环节，使用去遮挡优化提示词")
    
    for s in stages:
        filename = f"comp_{s['id']}_Flux.jpg"
        save_path = os.path.join(target_dir, filename)
        print(f"\n[Flux优化] 正在生成环节 {s['id']}: {s['name']}...")
        
        prompt = f"{base_desc_flux} {s['desc']}"
        
        try:
            img_data, _ = client.flux_to_image(
                prompt,
                width=832, 
                height=1216
            )
            
            with open(save_path, "wb") as f:
                f.write(img_data)
            
            print(f"[Flux优化] ✅ 成功: {filename}")
            
        except Exception as e:
            print(f"[Flux优化] ❌ 失败: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n[Flux优化] 全部 8 个环节生成完成！")

if __name__ == "__main__":
    generate_flux_uncensored()
