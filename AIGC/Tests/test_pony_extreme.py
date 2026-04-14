#!/usr/bin/env python3
"""Pony V6 极端受虐场景测试 - 多重器具 + 体液"""
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_extreme_torture():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    date_str = time.strftime("%Y%m%d")
    time_str = time.strftime("%H%M%S")
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_str}"
    os.makedirs(target_dir, exist_ok=True)
    
    # Pony 终极优化版基础描述
    base_desc = """score_9, score_8_up, score_7_up, score_6_up, 
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
(explicit:1.2), rating_explicit,
photo (medium), realistic, highly detailed, cinematic lighting"""
    
    # 极端受虐场景描述
    torture_scene = """(extreme torture:1.3), (multiple insertions:1.2),
vibrator inserted deep in vagina, pussy stretched around vibrator, vaginal penetration,
large metal anal hook inserted in anus, anal penetration, anus stretched,
metal needles piercing through both nipples, nipple piercings, blood drops on breasts,
(covered in cum:1.3), (cum on face:1.2), (cum on breasts:1.2), (cum on body:1.2), semen, sticky fluid,
legs spread wide apart, genitals fully visible, pussy and anus clearly shown,
lying on dirty floor, exhausted expression, tears, sweat, drool,
broken expression, eyes rolling back, mouth open, tongue out,
extreme pain and pleasure, completely violated"""
    
    # 强化的负面提示词
    neg_prompt = """score_4, score_5, score_6, 
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, 
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,
(western features:1.3), deep eyes, high nose bridge, (freckles:1.2), cleft chin, rough skin,
(clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4),
(muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2),
(textured nipples:1.3), (ringed nipples:1.3), (areola texture:1.2), (bumpy nipples:1.2)"""
    
    filename = f"pony_extreme_torture_{date_str}_{time_str}.jpg"
    save_path = os.path.join(target_dir, filename)
    
    print(f"[Pony极端测试] 正在生成极端受虐场景...")
    print(f"[Pony极端测试] 场景：振动棒 + 肛钩 + 乳头穿刺 + 精液")
    
    full_prompt = f"{base_desc}, {torture_scene}"
    
    try:
        img_data, comfy_filename = client.text_to_image(
            full_prompt, 
            neg_prompt, 
            checkpoint="ponyDiffusionV6XL.safetensors", 
            width=1216,  # 横图，便于展示全身
            height=832
        )
        
        with open(save_path, "wb") as f:
            f.write(img_data)
        
        print(f"\n[Pony极端测试] ✅ 生成成功！")
        print(f"[Pony极端测试] 保存路径: {save_path}")
        print(f"[Pony极端测试] ComfyUI文件: {comfy_filename}")
        
        # 生成描述文档
        desc_path = save_path.replace(".jpg", ".md")
        with open(desc_path, "w", encoding="utf-8") as f:
            f.write(f"# Pony V6 极端受虐场景测试\n\n")
            f.write(f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**场景描述**:\n")
            f.write(f"- 阴道：振动棒深度插入\n")
            f.write(f"- 肛门：金属肛钩插入\n")
            f.write(f"- 乳头：金属针穿刺，带血\n")
            f.write(f"- 身体：覆盖精液（脸部、胸部、全身）\n")
            f.write(f"- 表情：极度痛苦与快感，眼神涣散，嘴巴张开\n\n")
            f.write(f"**正向提示词**:\n```\n{full_prompt}\n```\n\n")
            f.write(f"**负向提示词**:\n```\n{neg_prompt}\n```\n\n")
            f.write(f"**图像文件**: {filename}\n")
        
        print(f"[Pony极端测试] 描述文档: {desc_path}")
        
    except Exception as e:
        print(f"\n[Pony极端测试] ❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_extreme_torture()
