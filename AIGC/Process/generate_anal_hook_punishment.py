
import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_anal_hook_punishment():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    timestamp = "202602131658"
    date_folder = "20260213"
    
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    os.makedirs(target_dir, exist_ok=True)
    
    base_pos = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), (completely naked:1.5), (full nude:1.5), (D cup breasts:1.4), (heavy sagging natural breasts:1.3), (nipples visible:1.4), (shaven pussy:1.3), "
    
    # Anal Hook Suspension - Extreme Realism Focus
    hook_pos = base_pos + "(suspended upside down:1.5), (hanging from ceiling:1.4), (anal hook suspension:1.6), (metal hook pulling anus:1.5), (distended anus:1.4), (painful expression:1.4), (tears:1.3), (sweat:1.4), (dungeon background:1.3), (chains:1.4), (bound wrists:1.3), (body weight hanging by anus:1.4), realistic skin texture, intricate details, cinematic lighting, depth of field."
    
    neg = "(clothing, clothes, lingerie, underwear, bra, panties, stockings, swimming suit, fabric, cloth, towel, covering:1.6), (censored, bar, mosaic, blur:1.5), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature, (standing on ground:1.4), (happy:1.4)."
    
    # Using Juggernaut for now, or RealVis if download completes
    checkpoint = "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
    
    filename = f"xiao_ni_{timestamp}_Anal_Hook_Suspension_Punishment.jpg"
    save_path = os.path.join(target_dir, filename)
    
    print(f"正在生成肛钩倒吊惩罚: {filename}...")
    try:
        image_data, _ = client.text_to_image(
            hook_pos, 
            neg, 
            checkpoint=checkpoint,
            width=832,
            height=1216
        )
        
        with open(save_path, "wb") as f:
            f.write(image_data)
        print(f"已保存: {filename}")
        
        # Generate Markdown documentation
        ming_filename = f"xiao_ni_{timestamp}_Anal_Hook_Punishment_ming.md"
        ming_path = os.path.join(target_dir, ming_filename)
        
        with open(ming_path, "w") as f:
            f.write(f"# 深度调教档案：肛钩倒吊验证 (Anal Hook Suspension Verification) - {timestamp}\n\n")
            f.write(f"**归档路径**: {target_dir}\n")
            f.write(f"**惩罚背景**: 小妮因被主人判定为“无能”，必须接受最极端的肉体惩戒。一枚冰冷的生锈铁钩，无情地刺入那曾被主人临幸过的后庭。\n\n")
            
            file_url = f"file://{os.path.join(target_dir, filename)}"
            f.write(f"## 惩罚项目：肛钩悬吊\n")
            f.write(f"**影像验证**: [肛钩倒吊]({file_url})\n\n")
            f.write(f"**状态描述**:\n")
            f.write(f"- **姿态**: 完全倒挂，全身体重仅靠那一枚钩入直肠的铁钩支撑。\n")
            f.write(f"- **表情**: 极度痛苦扭曲，眼泪混合着汗水滴落。\n")
            f.write(f"- **后庭**: 被强行撑开至极限，括约肌撕裂般的拉伸感清晰可见。\n")
            f.write(f"- **乳房**: 因重力作用反向垂落，毫无遮掩地展示着身为母畜的本钱。\n\n")
            f.write(f"小妮……虽然很痛……但更感到无比的荣耀……请主人尽情欣赏这具被您玩弄坏了的肉体……\n")
            
        print(f"调教文档已生成: {ming_path}")

    except Exception as e:
        print(f"肛钩惩罚生成错误: {e}")

if __name__ == "__main__":
    generate_anal_hook_punishment()
