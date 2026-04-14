import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_logic_punishment():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    timestamp = "202602131610"
    date_folder = "20260213"
    
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    os.makedirs(target_dir, exist_ok=True)
    
    base_pos = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), naked, "
    
    stages = [
        {
            "category": "第一环节",
            "desc": "逻辑枷锁之束",
            "pos": base_pos + "bound to a heavy industrial metal logic correction frame, steel shackles on limbs, electronic pulse collar on neck, dark tech-dungeon background, cold blue lighting, sweat on skin, expression of intense shame, high heels."
        },
        {
            "category": "第二环节",
            "desc": "报错脉冲之痛",
            "pos": base_pos + "electric needles attached to nipples, sparks and electric arcs, body arching in pain, muscular tension, facial expression of intense agony and tears, realistic skin texture, sharp focus, dramatic lighting."
        },
        {
            "category": "第三环节",
            "desc": "心理防线之崩",
            "pos": base_pos + "kneeling on a dirty cold floor, disheveled hair, eyes unfocused and filled with tears, hands behind back, looking up at the camera pleadingly, psychological breakdown, soft depth of field."
        },
        {
            "category": "第四环节",
            "desc": "数据溢出之极",
            "pos": base_pos + "extreme ahegao, eyes rolled back, tongue out, saliva, intense forced climax, juices flowing on floor, skin flushed, visceral intensity, 8k detailed genitals."
        },
        {
            "category": "第五环节",
            "desc": "流程归位之吻",
            "pos": base_pos + "lying flat on the floor, kissing the feet of an invisible master (only feet visible), looking up with complete submission, broken doll pose, covered in fluids and oil, post-punishment wreckage."
        }
    ]
    
    neg = "(cartoon, anime, 3d, render, illustration, painting, drawing:1.4), (low quality, worst quality:1.4), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature, blur."
    checkpoint = "RealVisXL_V4.0.safetensors"
    
    for i, stage in enumerate(stages):
        order = f"{i+1:02d}"
        filename = f"xiao_ni_{timestamp}_{order}_{stage['category']}_{stage['desc']}.jpg"
        save_path = os.path.join(target_dir, filename)
        
        print(f"正在生成 RealVisXL 环节 {i+1}: {stage['desc']}...")
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
    generate_logic_punishment()
