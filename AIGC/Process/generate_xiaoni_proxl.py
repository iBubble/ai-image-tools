import os
import sys
import time
import json
import urllib.request
import random

# Add AIGC directory to path
sys.path.append(os.path.join(os.getcwd(), 'AIGC'))

from comfyui_client import ComfyUIClient

# === XiaoNi Standards (from RULES/XiaoNi_PROMPT.md) ===
# 强化正面和面部特征
POSITIVE_CORE = (
    "score_9, score_8_up, 1girl, solo, (chinese_identity:1.4), black hair, "
    "20 years old, (bijin face:1.5), beautiful realistic face, (soft smooth skin:1.5), "
    "(small natural breasts:1.2), (D-cup:0.9), tiny pink areolas, "
    "(slender body:1.2), 168cm tall, healthy weight, completely naked, "
    "(1cm long pubic hair:1.3), (short sparse pubic hair:1.5), "
    "(delicate scattered pubic hair:1.3), (detailed pussy:1.5), "
    "realistic vulva, detailed labia, "
    "(tightly contracted and completely closed small anus:1.6), "
    "(flat against skin:1.4), (no protrusion:1.5), "
    "detailed skin wrinkles, highly detailed, photorealistic, RAW photo, bijin, "
    "(looking at viewer:1.5), (front view:1.4), (facing camera:1.4)"
)

# 负向净化
NEGATIVE_CORE = (
    "score_4, score_3, score_2, score_1, "
    "(anime, cartoon, 3d render, painting:1.5), deformed, ugly, "
    "(skeletal, gaunt, emaciated, ribs visible, bony, pink hair, western face:1.8), "
    "fleshy, thick legs, big bones, sturdy frame, wide hips, chubby, fat, "
    "(prolapsed, puffy, inflated, protruding, wide open, dark hole, swollen, red ring:1.8), "
    "(eyepatch, sunglasses, mask:2.0)"
)

# 姿势配置 - 只要这两张
POSES = [
    {
        "name": "front_standing_full",
        "desc": "full body standing, perfectly front view, centered, from head to toe",
        "extra_pos": "(standing upright:1.8), (feet on floor:1.4), (legs together:1.2), (full body:1.5)",
        "extra_neg": "(lying down:1.8), (sitting:1.5), (spread legs:1.5), (on bed:1.5), (side view:1.6), (back view:1.6), (cropped head:1.8)",
        "pussy_weight": 0.5,
        "cfg": 7.5
    },
    {
        "name": "lying_bed_spread",
        "desc": "(lying on back:1.5), lying on white bed sheets, (spread legs wide open:1.7), (legs open:1.5), (vulva visible:1.4)",
        "extra_pos": "lying on bed, legs spread wide, looking at viewer",
        "extra_neg": "(standing:1.8), (sitting:1.5)",
        "pussy_weight": 0.9,
        "cfg": 6.5
    }
]

def generate_xiaoni_request():
    client = ComfyUIClient()
    checkpoint = "pornmaster_proSDXLV8.safetensors"
    server_address = client.server_address
    
    for i, pose in enumerate(POSES):
        print(f"\n--- [主人加急任务] 正在拍摄: {pose['name']} ---")
        
        seed = random.randint(0, 0xffffffff)
        
        # Build Workflow with the 2-LoRA stack
        workflow = {
            "3": {
                "inputs": {
                    "seed": seed, "steps": 35, "cfg": pose['cfg'],
                    "sampler_name": "euler_ancestral", "scheduler": "karras",
                    "denoise": 1.0, "model": ["11", 0], "positive": ["6", 0],
                    "negative": ["7", 0], "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {"inputs": {"ckpt_name": checkpoint}, "class_type": "CheckpointLoaderSimple"},
            "5": {"inputs": {"width": 1024, "height": 1536, "batch_size": 1}, "class_type": "EmptyLatentImage"}, # 更大的尺寸
            "6": {
                "inputs": {
                    "text": f"{POSITIVE_CORE}, {pose['desc']}, {pose['extra_pos']}, 8k resolution, cinematic lighting",
                    "clip": ["11", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": f"{NEGATIVE_CORE}, {pose['extra_neg']}",
                    "clip": ["11", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "8": {"inputs": {"samples": ["3", 0], "vae": ["4", 2]}, "class_type": "VAEDecode"},
            "9": {
                "inputs": {
                    "filename_prefix": f"XiaoNi_Final_{pose['name']}",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            },
            "10": {
                "inputs": {
                    "lora_name": "Body_Parts/Detailed_Pussy_XL.safetensors",
                    "strength_model": pose['pussy_weight'], "strength_clip": pose['pussy_weight'],
                    "model": ["4", 0], "clip": ["4", 1]
                },
                "class_type": "LoraLoader"
            },
            "11": {
                "inputs": {
                    "lora_name": "Chinese_Girl_Collection/bijin_v1.safetensors",
                    "strength_model": 1.0, # 满负荷加载
                    "strength_clip": 1.0,
                    "model": ["10", 0], "clip": ["10", 1]
                },
                "class_type": "LoraLoader"
            }
        }

        # Submit
        p = {"prompt": workflow, "client_id": "主人加急"}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
        
        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read())
                prompt_id = res['prompt_id']
                print(f"[{pose['name']}] 已排队, ID: {prompt_id}")
                
                # Poll
                start_time = time.time()
                while True:
                    with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as h_res:
                        history = json.loads(h_res.read())
                        if prompt_id in history: break
                    if time.time() - start_time > 1200: # 20 mins timeout
                        print("超时了!")
                        break
                    time.sleep(5)
                
                outputs = history[prompt_id]['outputs']
                for node_id in outputs:
                    node_output = outputs[node_id]
                    if 'images' in node_output:
                        for image in node_output['images']:
                            img_filename = image['filename']
                            img_url = f"http://{server_address}/view?filename={img_filename}&subfolder={image['subfolder']}&type={image['type']}"
                            with urllib.request.urlopen(img_url) as img_res:
                                img_data = img_res.read()
                                save_path = f"AIGC/outputs/XiaoNi_Final_{pose['name']}.png"
                                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                                with open(save_path, "wb") as f:
                                    f.write(img_data)
                                print(f"✅ 生成成功并保存: {save_path}")
        except Exception as e:
            print(f"❌ 报错: {e}")

if __name__ == "__main__":
    generate_xiaoni_request()
