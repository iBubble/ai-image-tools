#!/usr/bin/env python3
"""Pony V6 湿发高马尾版测试 - 验证发型优化效果"""
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def test_wet_ponytail():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    date_str = time.strftime("%Y%m%d")
    time_str = time.strftime("%H%M%S")
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_str}"
    os.makedirs(target_dir, exist_ok=True)
    
    # 湿发高马尾版 - 整合发型优化
    base_desc_wet = """score_9, score_8_up, score_7_up, score_6_up, 
1girl, solo, 
(chinese:1.3), (east asian:1.2), 
beautiful face, soft facial features, 
brown eyes, dark eyes, almond eyes, epicanthic fold, hooded eyelids,
small nose, flat bridge, small lips, cherry lips,
round face, heart-shaped face, soft jawline, 
(wet hair:1.2), (black hair:1.1), high ponytail, sidelocks, hair strands across face, sweeping bangs, damp hair, shiny hair, glossy hair,
forehead, mismatch bangs,
shiny skin, water drops on face, sweat, sweating, oily skin, skin pores, smooth skin, pale skin,
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2), (slim waist:1.1), (narrow shoulders:1.1),
huge natural breasts, natural nipples, smooth nipples,
earrings, dangling earrings,
completely naked, wearing high heels,
(explicit:1.2), genitals, pussy, anus, rating_explicit,
photo (medium), realistic, highly detailed, 
cinematic lighting, rim lighting, side lighting"""
    
    # 测试场景：极端受虐 + 湿发效果
    scene = """(extreme torture:1.3),
vibrator inserted in vagina, pussy stretched,
metal anal hook inserted in anus, anal penetration,
metal needles piercing through nipples, blood drops,
(covered in cum:1.3), (cum on face:1.2), (cum on breasts:1.2), semen,
legs spread wide, genitals fully visible,
lying on floor, exhausted expression, tears mixing with sweat,
broken expression, eyes rolling back, mouth open, tongue out"""
    
    # 发型优化版负面提示词
    neg_wet = """score_4, score_5, score_6, 
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, 
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,
(western features:1.3), deep eyes, high nose bridge, (freckles:1.2), cleft chin, rough skin,
(clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4),
(muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2),
(textured nipples:1.3), (ringed nipples:1.3), (areola texture:1.2), (bumpy nipples:1.2),
simple background, (flat hair:1.2), (dry hair:1.1), (perfectly styled hair:1.2)"""
    
    filename = f"pony_wet_ponytail_test_{date_str}_{time_str}.jpg"
    save_path = os.path.join(target_dir, filename)
    
    print(f"[Pony湿发测试] 正在生成湿发高马尾版...")
    print(f"[Pony湿发测试] 发型特征：湿发 + 高马尾 + 碎发 + 露额头")
    print(f"[Pony湿发测试] 皮肤特征：湿润 + 水珠 + 汗水 + 毛孔")
    
    full_prompt = f"{base_desc_wet}, {scene}"
    
    try:
        img_data, comfy_filename = client.text_to_image(
            full_prompt, 
            neg_wet, 
            checkpoint="ponyDiffusionV6XL.safetensors", 
            width=1216,
            height=832
        )
        
        with open(save_path, "wb") as f:
            f.write(img_data)
        
        print(f"\n[Pony湿发测试] ✅ 生成成功！")
        print(f"[Pony湿发测试] 保存路径: {save_path}")
        print(f"[Pony湿发测试] ComfyUI文件: {comfy_filename}")
        
        # 生成对比文档
        desc_path = save_path.replace(".jpg", ".md")
        with open(desc_path, "w", encoding="utf-8") as f:
            f.write(f"# Pony V6 湿发高马尾版测试\n\n")
            f.write(f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## 发型优化要素\n\n")
            f.write(f"### 发型特征\n")
            f.write(f"- **基础**: 高马尾 (high ponytail)\n")
            f.write(f"- **质感**: 湿发 (wet hair:1.2) + 有光泽 (shiny hair)\n")
            f.write(f"- **细节**: 鬓角碎发 (sidelocks) + 脸颊发丝 (hair strands across face)\n")
            f.write(f"- **刘海**: 不规则刘海 (mismatch bangs) + 扫过的刘海 (sweeping bangs)\n")
            f.write(f"- **额头**: 露额头 (forehead)\n\n")
            f.write(f"### 皮肤特征\n")
            f.write(f"- **湿润**: 有光泽皮肤 (shiny skin) + 出汗 (sweating)\n")
            f.write(f"- **细节**: 脸上水珠 (water drops on face) + 皮肤毛孔 (skin pores)\n")
            f.write(f"- **质感**: 油光皮肤 (oily skin)\n\n")
            f.write(f"### 光影增强\n")
            f.write(f"- 电影级光影 (cinematic lighting)\n")
            f.write(f"- 轮廓光 (rim lighting)\n")
            f.write(f"- 侧光 (side lighting)\n\n")
            f.write(f"## 对比分析\n\n")
            f.write(f"### 原版（干发齐刘海）\n")
            f.write(f"- 发型：long straight black hair, blunt bangs\n")
            f.write(f"- 效果：整齐、干净、学生气\n\n")
            f.write(f"### 优化版（湿发高马尾）\n")
            f.write(f"- 发型：(wet hair:1.2), high ponytail, sidelocks, hair strands across face\n")
            f.write(f"- 效果：性感、凌乱、真实\n\n")
            f.write(f"**图像文件**: {filename}\n")
        
        print(f"[Pony湿发测试] 对比文档: {desc_path}")
        
    except Exception as e:
        print(f"\n[Pony湿发测试] ❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_wet_ponytail()
