#!/usr/bin/env python3
"""Pony V6 终极优化版 - 整合面部细化、体型优化、标签顺序优化"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_pony_ultimate():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    date_str = "20260213"
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_str}"
    os.makedirs(target_dir, exist_ok=True)
    
    # 终极优化的 Pony 提示词 - 整合面部细化 + 体型优化
    # 严格遵循 Pony 的标签顺序：质量分 -> 身份 -> 面部 -> 发型 -> 体型 -> 场景
    base_desc_pony = """score_9, score_8_up, score_7_up, score_6_up, 
1girl, solo, 
(chinese:1.3), (east asian:1.2), 
beautiful face, soft facial features, 
brown eyes, dark eyes, almond eyes, epicanthic fold, hooded eyelids,
small nose, flat bridge, small lips, cherry lips,
round face, heart-shaped face, soft jawline, smooth skin, pale skin,
long straight black hair, shiny hair, blunt bangs,
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2), (slim waist:1.1), (narrow shoulders:1.1),
huge natural breasts, natural nipples, smooth nipples,
completely naked, wearing high heels,
(explicit:1.2), genitals, pussy, anus, rating_explicit,
photo (medium), realistic, highly detailed, cinematic lighting"""
    
    stages = [
        {"id": "01", "name": "冷钢束缚", "desc": "suspended by wrists from chains, arms raised, tiptoes, painful expression, genitals visible"},
        {"id": "02", "name": "电流鞭笞", "desc": "electric shock wand on inner thigh, body arching in pain, tears, breasts bouncing, genitals exposed"},
        {"id": "03", "name": "真空幽闭", "desc": "wrapped in transparent plastic, vacuum sealed, mouth gasping, breasts compressed, genitals visible through plastic"},
        {"id": "04", "name": "双龙扩充", "desc": "two large metal rods inserted in vagina and anus, legs spread wide, body trembling, fluids dripping"},
        {"id": "05", "name": "乳房穿刺", "desc": "metal hooks piercing through breasts, chains pulling breasts apart, blood, biting lip, genitals exposed"},
        {"id": "06", "name": "肛钩悬吊", "desc": "metal anal hook pulling upward, tiptoes, arched back, sweat and tears, anus and vagina exposed"},
        {"id": "07", "name": "暴力侵犯", "desc": "forced sex from behind on concrete floor, hands bound, breasts grinding, genitals exposed"},
        {"id": "08", "name": "轮番蹂躏", "desc": "double penetration, oral deepthroat, gagging, cum on face, genitals completely exposed"}
    ]
    
    # 强化的负面提示词 - 剔除西方特征 + 抑制肌肉感 + 抑制乳头异常纹理
    neg_pony = """score_4, score_5, score_6, 
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, 
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,
(western features:1.3), deep eyes, high nose bridge, (freckles:1.2), cleft chin, rough skin,
(clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4),
(muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2),
(textured nipples:1.3), (ringed nipples:1.3), (areola texture:1.2), (bumpy nipples:1.2)"""
    
    print(f"[Pony终极版] 开始生成 8 个环节")
    print(f"[Pony终极版] 优化要素：面部细化 + 体型优化 + 标签顺序优化")
    
    for s in stages:
        filename = f"comp_{s['id']}_PonyV6.jpg"
        save_path = os.path.join(target_dir, filename)
        print(f"\n[Pony终极版] 正在生成环节 {s['id']}: {s['name']}...")
        
        prompt = f"{base_desc_pony}, {s['desc']}"
        
        try:
            img_data, _ = client.text_to_image(
                prompt, 
                neg_pony, 
                checkpoint="ponyDiffusionV6XL.safetensors", 
                width=832, 
                height=1216
            )
            
            with open(save_path, "wb") as f:
                f.write(img_data)
            
            print(f"[Pony终极版] ✅ 成功: {filename}")
            
        except Exception as e:
            print(f"[Pony终极版] ❌ 失败: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n[Pony终极版] 全部 8 个环节生成完成！")

if __name__ == "__main__":
    generate_pony_ultimate()
