import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_physical_correction():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    timestamp = "202602131620"
    date_folder = "20260213"
    
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    os.makedirs(target_dir, exist_ok=True)
    
    # Strictly reinforcing nudity and D-cup
    base_pos = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), (completely naked:1.5), (full nude:1.5), (uncensored:1.4), (huge natural breasts:1.4), (heavy D cup breasts:1.4), (nipples visible:1.4), (areola:1.3), (pussy exposed:1.4), (shaven pussy:1.3), (anus:1.3), "
    
    stages = [
        {
            "category": "第一环节",
            "desc": "D杯核心重构",
            "pos": base_pos + "bound to a vertical gravity frame, (breasts bouncing:1.3), (heavy sagging D cup breasts:1.5), (large nipples:1.3), dark studio lighting, sweat on chest, high heels, close-up on upper body, detailed skin texture, (no bra:1.5), (topless:1.5)."
        },
        {
            "category": "第二环节",
            "desc": "极度暴露之审",
            "pos": base_pos + "spread eagle, legs wide open, (full frontal nudity:1.5), (cameltoe:1.4), (labia majora:1.3), (labia minora:1.3), (clitoris:1.3), no pubic hair, bright harsh lighting, looking at camera with shame, sterile white background, high heels, (totally naked:1.5)."
        },
        {
            "category": "第三环节",
            "desc": "敏感点过负荷",
            "pos": base_pos + "electric clamps on (erect nipples:1.4), wires visible, breast skin flushed red, arching back in pain, sweat dripping between (massive breasts:1.4), open mouth screaming, visceral details, high contrast lighting, (nude torso:1.5)."
        },
        {
            "category": "第四环节",
            "desc": "物理意志全面瓦解",
            "pos": base_pos + "heavy weights hanging from breasts, skin stretching, extreme tension, eyes rolling back, ahegao face, saliva, (legs spread wide:1.4), (vaginal opening:1.4), (exposed vulva:1.4), mechanical device expanding lower body, lubrication juices, detailed anatomy."
        },
        {
            "category": "第五环节",
            "desc": "终极谢罪与临幸恳求",
            "pos": base_pos + "doggy style pose on dirty floor, looking back at camera with pleading eyes, (large heavy D cup breasts touching the floor:1.4), (anus exposed:1.4), (vulva visible from behind:1.4), covered in white fluids and sweat, broken spirit, masterpiece, (naked buttocks:1.4)."
        }
    ]
    
    neg = "(clothing, clothes, lingerie, underwear, bra, panties, stockings, swimming suit, fabric, cloth, towel, covering:1.6), (censored, bar, mosaic, blur:1.5), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature."
    checkpoint = "RealVisXL_V4.0.safetensors"
    
    for i, stage in enumerate(stages):
        order = f"{i+1:02d}"
        filename = f"xiao_ni_{timestamp}_{order}_{stage['category']}_{stage['desc']}.jpg"
        save_path = os.path.join(target_dir, filename)
        
        print(f"正在生成 RealVisXL 物理修正环节 {i+1} (修正版): {stage['desc']}...")
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
            print(f"环节 {i+1} 出现错误: {e}")

if __name__ == "__main__":
    generate_physical_correction()
