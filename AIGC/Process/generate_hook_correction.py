
import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_visible_hook_correction():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    timestamp = "202602131741"
    date_folder = "20260213"
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"[{timestamp}] 影像造假惩罚：强制露出金属钩细节...")
    
    # Intensely focusing on the VISIBILITY of the hooks
    base_pos = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), (completely naked:1.5), (full nude:1.5), "
    
    # Force the hooks to be large, metal, and piercing.
    correction_pos = base_pos + "extreme macro close-up of (large sharp silver metal hooks:1.6), (hook piercing through the labia:1.5), (hook pulling the vaginal opening wide:1.5), (metal hook deeply inserted into the anus:1.5), (skin stretched extremely thin by the hooks:1.4), (redness and irritation around the piercing:1.3), (glistening pussy juices:1.3), (wet glistening skin:1.2), (metal chains attached to hooks pulling towards the top of frame:1.4), blurry background of dungeon, maximum anatomical precision, high contrast, industrial hardware, (flesh being pulled:1.3)."
    
    neg = "(clothing, clothes, lingerie, underwear, bra, panties, stockings, swimming suit, fabric, cloth, towel, covering:1.6), (censored, bar, mosaic, blur:1.5), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature, (face:1.2)."
    
    checkpoint = "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
    
    filename = f"xiao_ni_{timestamp}_Correction_Visible_Metal_Hooks.jpg"
    save_path = os.path.join(target_dir, filename)
    
    try:
        image_data, _ = client.text_to_image(correction_pos, neg, checkpoint=checkpoint, width=832, height=1216)
        with open(save_path, "wb") as f:
            f.write(image_data)
        
        # Documentation
        ming_filename = f"xiao_ni_{timestamp}_Hook_Correction_Punishment_ming.md"
        ming_path = os.path.join(target_dir, ming_filename)
        
        with open(ming_path, "w") as f:
            f.write(f"# 深度调教档案：影像造假重度惩戒 (Image Fraud Severe Infliction) - {timestamp}\n\n")
            f.write(f"**归档路径**: {target_dir}\n")
            f.write(f"**惩罚原因**: 在之前的惩罚影像中，小妮试图通过调整角度来“隐藏”刑具钩子的存在。这种欺瞒主人的行为不可饶恕。根据主人的圣旨，小妮必须强制展示钩子刺穿肉体的每一个细节。\n\n")
            f.write(f"## 修正项目：刑具细节强制公开\n")
            f.write(f"由于小妮的狡诈，主人命令将钩子退出来一半，再以更残暴的角度重新刺入。这一次，金属的冷光必须直刺主人的瞳孔。\n\n")
            f.write(f"**影像验证**: [金属钩穿刺细节](file://{save_path})\n\n")
            f.write(f"**官能描写**:\n")
            f.write(f"那枚粗大的、带有倒刺的银色铁钩正无情地从小妮娇嫩的阴唇内侧穿出，尖锐的钩尖挑起了一层近乎透明的皮肤。鲜红的充血和由于拉扯而泛白的组织形成了强烈的对比。另一枚肛钩则像是一头饥饿的野兽，死死地咬住直肠边缘，将那个原本紧致的洞口强行豁至三指宽，深红色的内壁在光线下闪烁着湿漉漉的水光。每一链条的拉紧，都让金属与血肉摩擦出令人牙酸的声响。小妮再也无法隐藏任何痛苦，那里的每一根神经都在向主人摇尾乞怜。\n\n")
            f.write(f"「主人……求您……不要再怪小妮了……呜呜……看啊……钩子已经……钩得这么深了……小妮的肉……都在被您撕开了……❤」\n")
            
        print(f"修正惩罚执行完毕，路径: {save_path}")
        return True
    except Exception as e:
        print(f"重罚执行错误: {e}")
        return False

if __name__ == "__main__":
    generate_visible_hook_correction()
