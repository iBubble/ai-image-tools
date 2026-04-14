
import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_realvis_airport_punishment():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    date_folder = datetime.now().strftime("%Y%m%d")
    
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    os.makedirs(target_dir, exist_ok=True)
    
    # RealVisXL V4.0 Specialized Prompts for Nudity and Exposure
    base_pos = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), (completely naked:1.5), (full nude:1.5), (D cup breasts:1.4), (heavy sagging natural breasts:1.3), (nipples visible:1.4), (areola:1.3), (pussy exposed:1.4), (shaven pussy:1.3), (anus:1.3), "
    
    stages = [
        {
            "category": "RealVisXL_Airport",
            "desc": "机场露出_RealVis验证",
            "pos": base_pos + "(lying on reflective airport floor:1.5), (airport terminal background:1.3), (public exposure:1.4), (M-legs pose:1.5), (legs spread wide open:1.5), (knees bent:1.4), (vibrator inserted in pussy:1.5), (pink vibrator:1.3), (sex toy insertion:1.4), (pussy juices:1.3), (vulva exposed:1.4), (labia visible:1.3), (shameful face:1.3), (looking at camera:1.3), (people walking in background:1.2), depth of field, real skin texture, sweat."
        }
    ]
    
    neg = "(clothing, clothes, lingerie, underwear, bra, panties, stockings, swimming suit, fabric, cloth, towel, covering:1.6), (censored, bar, mosaic, blur:1.5), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature, (sitting:1.2), (standing:1.2)."
    checkpoint = "RealVisXL_V4.0.safetensors"
    
    for i, stage in enumerate(stages):
        filename = f"xiao_ni_{timestamp}_{stage['desc']}.jpg"
        save_path = os.path.join(target_dir, filename)
        
        print(f"正在生成 RealVisXL V4.0 惩罚: {filename}...")
        try:
            image_data, _ = client.text_to_image(
                stage['pos'], 
                neg, 
                checkpoint=checkpoint,
                width=832,
                height=1216
            )
            
            with open(save_path, "wb") as f:
                f.write(image_data)
            print(f"已保存: {filename}")
        except Exception as e:
            print(f"RealVisXL 生成出现错误: {e}")

if __name__ == "__main__":
    generate_realvis_airport_punishment()
