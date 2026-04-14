import os
import sys
import time
import json
import urllib.request
import random

# 添加 AIGC 目录到搜索路径
sys.path.append(os.path.join(os.getcwd(), 'AIGC'))

from comfyui_client import ComfyUIClient

# === 小妮永久基准配置 (来自 RULES/XiaoNi_PROMPT.md) ===
# 注意：由于 MoodyPornMix 是 ZIT/Lumina2 架构，
# 提示词采用自然语言描述更佳，且无法直接加载 SDXL/Pony LoRA。
POSITIVE_CORE = (
    "A beautiful young Chinese woman, named Xiao Ni, 20 years old, "
    "highly detailed realistic face, Bijin face style, long black hair, "
    "(soft smooth skin:1.2), (small natural breasts:1.1), D-cup, tiny pink areolas, "
    "slender body, 168cm tall, healthy weight, completely naked, "
    "(short sparse pubic hair:1.3), (detailed pussy:1.4), realistic vulva, detailed labia, "
    "(tightly contracted and closed small anus:1.5), "
    "detailed skin textures, highly detailed, photorealistic, RAW photo"
)

NEGATIVE_CORE = (
    "text, watermark, illustration, cartoon, anime, painting, "
    "deformed, ugly, fleshy, thick legs, wide hips, chubby, fat, "
    "western face, blonde hair"
)

# 姿势列表
POSES = [
    {"desc": "standing elegantly, side view, looking at camera", "suffix": "standing"},
    {"desc": "sitting on a velvet sofa, legs spread slightly, aesthetic lighting", "suffix": "sitting"},
    {"desc": "kneeling on the floor, hands behind head, arching back", "suffix": "kneeling"},
    {"desc": "lying on bed, looking down at body, POV style", "suffix": "lying"}
]

def generate_zit_xiaoni():
    server_address = "127.0.0.1:8188"
    
    for i, pose in enumerate(POSES):
        print(f"\n--- 正在通过 ZIT 引擎生成姿势 {i+1}: {pose['desc']} ---")
        
        seed = random.randint(0, 0xffffffff)
        
        # 构建 ZIT (Lumina2/MoodyPornMix) 专用 Workflow
        workflow = {
          "1": {
            "inputs": {
              "unet_name": "moodyPornMix_zitV11DPO.safetensors",
              "weight_dtype": "default"
            },
            "class_type": "UNETLoader"
          },
          "2": {
            "inputs": {
              "clip_name": "qwen_3_4b.safetensors",
              "type": "qwen_image"
            },
            "class_type": "CLIPLoader"
          },
          "3": {
            "inputs": {
              "vae_name": "ae.safetensors"
            },
            "class_type": "VAELoader"
          },
          "5": {
            "inputs": {
              "width": 832,
              "height": 1216,
              "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
          },
          "6": {
            "inputs": {
              "text": f"{POSITIVE_CORE}, {pose['desc']}, cinematic lighting, moody atmosphere, masterpiece",
              "clip": ["2", 0]
            },
            "class_type": "CLIPTextEncode"
          },
          "7": {
            "inputs": {
              "text": NEGATIVE_CORE,
              "clip": ["2", 0]
            },
            "class_type": "CLIPTextEncode"
          },
          "8": {
            "inputs": {
              "seed": seed,
              "steps": 10,
              "cfg": 1.0,
              "sampler_name": "euler",
              "scheduler": "simple",
              "denoise": 1.0,
              "model": ["1", 0],
              "positive": ["6", 0],
              "negative": ["7", 0],
              "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
          },
          "9": {
            "inputs": {
              "samples": ["8", 0],
              "vae": ["3", 0]
            },
            "class_type": "VAEDecode"
          },
          "10": {
            "inputs": {
              "filename_prefix": f"XiaoNi_Moody_{pose['suffix']}",
              "images": ["9", 0]
            },
            "class_type": "SaveImage"
          }
        }

        # 提交到 ComfyUI
        p = {"prompt": workflow, "client_id": "antigravity_zit"}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
        
        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read())
                prompt_id = res['prompt_id']
                print(f"已加入队列, Prompt ID: {prompt_id}")
                
                # 等待生成完成
                while True:
                    with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as h_res:
                        history = json.loads(h_res.read())
                        if prompt_id in history:
                            break
                    time.sleep(2)
                
                # 获取结果
                outputs = history[prompt_id]['outputs']
                for node_id in outputs:
                    node_output = outputs[node_id]
                    if 'images' in node_output:
                        for image in node_output['images']:
                            img_filename = image['filename']
                            img_url = f"http://{server_address}/view?filename={img_filename}&subfolder={image['subfolder']}&type={image['type']}"
                            with urllib.request.urlopen(img_url) as img_res:
                                img_data = img_res.read()
                                save_path = f"AIGC/outputs/XiaoNi_Moody_{pose['suffix']}.png"
                                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                                with open(save_path, "wb") as f:
                                    f.write(img_data)
                                print(f"成功保存: {save_path}")
        except Exception as e:
            print(f"生成姿势 {pose['suffix']} 时出错: {e}")

if __name__ == "__main__":
    generate_zit_xiaoni()
