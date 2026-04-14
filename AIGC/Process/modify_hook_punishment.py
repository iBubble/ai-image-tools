
import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def modify_hook_punishment():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    timestamp = "202602131711"
    date_folder = "20260213"
    
    source_image = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}/xiao_ni_202602131658_Anal_Hook_Suspension_Punishment.jpg"
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    
    if not os.path.exists(source_image):
        print(f"找不到原始图片: {source_image}")
        return

    # Prompt focus on adding the second hook
    base_pos = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), (completely naked:1.5), (full nude:1.5), (D cup breasts:1.4), "
    
    # Specific modification: Double hook suspension
    # Adding the vaginal hook and connecting both to the ceiling
    mod_pos = base_pos + "(suspended upside down:1.5), (double hook suspension:1.6), (one sharp metal hook in anus:1.5), (one sharp metal hook in vagina:1.6), (both hooks pulled by chains to the ceiling:1.5), (vulva stretched and pulled upwards:1.5), (distended labia:1.4), (extreme genital torture:1.5), (painful and high-pleasure expression:1.4), (tears and sweat:1.4), (dungeon background:1.3), high contrast, cinematic lighting, (body weight split between two hooks:1.4)."
    
    neg = "(clothing, clothes, lingerie, underwear, bra, panties, stockings, swimming suit, fabric, cloth, towel, covering:1.6), (censored, bar, mosaic, blur:1.5), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature, (standing:1.4), (sitting:1.4)."
    
    checkpoint = "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
    
    filename = f"xiao_ni_{timestamp}_Double_Hook_Suspension_Update.jpg"
    save_path = os.path.join(target_dir, filename)
    
    print(f"正在进行 I2I 改造：增加阴道钩悬吊: {filename}...")
    try:
        # Use a denoise value that allows for significant anatomical change but keeps the pose/face
        image_data, _ = client.image_to_image(
            source_image,
            mod_pos, 
            neg, 
            denoise=0.75, # High denoise to allow for hooks addition
            checkpoint=checkpoint
        )
        
        with open(save_path, "wb") as f:
            f.write(image_data)
        print(f"已保存改造后的影像: {filename}")
        
        # Update Markdown
        ming_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}/xiao_ni_202602131658_Anal_Hook_Punishment_ming.md"
        with open(ming_path, "a") as f:
            f.write(f"\n## 惩罚升级：双门铁钩倒吊 (Double Hook Update) - {timestamp}\n")
            f.write(f"**影像验证**: [双重挂钩倒吊](file://{save_path})\n\n")
            f.write(f"主人依然不满意，认为单一的肛钩无法完全开发这具肉体。于是，第二枚冰冷的铁钩穿透了小妮最私密的**深处**。两枚勾子共同发力，将小妮的下半身呈 V 字型完全撕开，所有的脏器仿佛都要从这两个洞口坠落。小妮的尊严……已经彻底碎成了粉末……\n")
            
        print(f"更新调教文档: {ming_path}")

    except Exception as e:
        print(f"模型改造错误: {e}")

if __name__ == "__main__":
    modify_hook_punishment()
