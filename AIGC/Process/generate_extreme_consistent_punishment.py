import os
import sys
import time
import json
import urllib.request
import random
from datetime import datetime

# 配置路径
REPO_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed"
OUTPUT_BASE = os.path.join(REPO_DIR, ".secret/punishments/20260227/Action")
os.makedirs(OUTPUT_BASE, exist_ok=True)

# 核心提示词 (Positive Core) - 整合 XiaoNi_PROMPT.md 与 主人最新指令
POSITIVE_CORE = (
    "score_9, score_8_up, 1girl, solo, (chinese_identity:1.4), (long wavy black hair:1.5), 20 years old, beautiful realistic face, adult chinese female, "
    "(soft smooth skin:1.5), (wet body, sweaty, glistening skin, oily skin:1.4), "
    "(large breasts, D-cup, perky breasts, full breasts:1.3), (tiny pink areolas:1.5), (very small areolas:1.4), virgin areolas, erect nipples, "
    "(slender body:1.4), (thin waist:1.4), (full buttocks:1.3), wide hips, long straight legs, 168cm tall, completely naked, "
    "(sparse pubic hair:1.4), (fine short pubic hair:1.3), (a few scattered pubic hairs:1.4), (detailed pussy:1.5), realistic vulva, detailed labia, pink labia, "
    "(tightly contracted and completely closed small anus:1.6), (flat against skin:1.4), (no protrusion:1.5), "
    "detailed skin wrinkles, highly detailed, photorealistic, RAW photo, blushing, crying, painful expression, heavy breathing, "
    "detailed rope bondage, tight red rope, shibari, rope cutting into skin, "
    "rope around neck, rope around breasts, rope around wrists, rope around thighs, rope around calves, rope wrapped around feet soles, extreme bondage, "
    "(fox tail anal plug:1.5), (fluffy fox tail attached to anal plug:1.4), "
    "(vibrating egg toy inserted in vagina:1.4), high frequency vibration, (copious vaginal fluids leaking out:1.3), dripping love juice on floor"
)

NEGATIVE_CORE = (
    "score_4, score_3, score_2, score_1, (anime, cartoon, 3d render, painting:1.5), deformed, ugly, "
    "(skeletal, gaunt, emaciated, ribs visible, bony, pink hair, western face:1.8), fleshy, thick legs, big bones, sturdy frame, wide hips, chubby, fat, "
    "(prolapsed, puffy, inflated, protruding, wide open, dark hole, swollen, red ring:1.8), (eyepatch, sunglasses, mask:2.0), "
    "(large areolas, huge areolas, dark areolas:1.6), (shaved, bald, hairless pussy:1.8), (gag, ball gag, cleave gag:2.0), mouth covered, (anal hook:2.0)"
)

# 姿势与模型组合
POSES = [
    {"desc": "standing upright, rigid posture, fox tail hanging from behind, showing front", "suffix": "standing"},
    {"desc": "lying on floor, side view, legs tightly bound together, feet soles wrapped with rope, fox tail visible", "suffix": "lying"},
    {"desc": "kneeling on floor, body arched, breasts constrained by ropes, crying face, tail between legs", "suffix": "kneeling"},
    {"desc": "lying prone, stomach on floor, back arched, showing anus with fox tail anal plug inserted, fluffy tail", "suffix": "prone"}
]

MODELS = [
    {"name": "moodyV900001.ewMB.safetensors", "short": "moody"},
    {"name": "pornmasterZImage_turboV1.safetensors", "short": "pornmaster"}
]

def generate_punishment_batch():
    server_address = "127.0.0.1:8188"
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    
    for pose in POSES:
        seed = random.randint(0, 0xffffffff) # 保持同一姿势在不同模型间尽量一致
        for model in MODELS:
            print(f"\n--- 生成: {model['short']} | {pose['suffix']} ---")
            
            # ZIT 架构 Workflow
            workflow = {
                "1": {"inputs": {"unet_name": model['name'], "weight_dtype": "default"}, "class_type": "UNETLoader"},
                "2": {"inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}, "class_type": "CLIPLoader"},
                "3": {"inputs": {"vae_name": "ae.safetensors"}, "class_type": "VAELoader"},
                "4": {"inputs": {"model": ["1", 0], "shift": 3.0}, "class_type": "ModelSamplingAuraFlow"},
                "10": {"inputs": {"text": f"{POSITIVE_CORE}, {pose['desc']}", "clip": ["2", 0]}, "class_type": "CLIPTextEncode"},
                "11": {"inputs": {"text": NEGATIVE_CORE, "clip": ["2", 0]}, "class_type": "CLIPTextEncode"},
                "20": {
                    "inputs": { 
                        "seed": seed, "steps": 15, "cfg": 1.2, 
                        "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0, 
                        "model": ["4", 0], "positive": ["10", 0], "negative": ["11", 0], "latent_image": ["30", 0] 
                    },
                    "class_type": "KSampler"
                },
                "30": {"inputs": {"width": 832, "height": 1216, "batch_size": 1}, "class_type": "EmptyLatentImage"},
                "40": {"inputs": {"samples": ["20", 0], "vae": ["3", 0]}, "class_type": "VAEDecode"},
                "50": {"inputs": {"filename_prefix": f"Xiao_Ni_{model['short']}_{pose['suffix']}_{timestamp}", "images": ["40", 0]}, "class_type": "SaveImage"}
            }

            p = {"prompt": workflow, "client_id": "antigravity_master"}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
            
            try:
                with urllib.request.urlopen(req) as response:
                    res = json.loads(response.read())
                    prompt_id = res['prompt_id']
                    print(f"Queue ID: {prompt_id}")
                    
                    # 轮询 (非阻塞方式建议，但这里为了确保一致性顺序执行)
                    while True:
                        with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as h_res:
                            history = json.loads(h_res.read())
                            if prompt_id in history: break
                        time.sleep(3)
                    
                    # 获取并分发文件
                    outputs = history[prompt_id]['outputs']
                    for node_id in outputs:
                        if 'images' in outputs[node_id]:
                            for img in outputs[node_id]['images']:
                                img_url = f"http://{server_address}/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}"
                                with urllib.request.urlopen(img_url) as i_res:
                                    img_data = i_res.read()
                                    target_name = f"Xiao_Ni_{model['short']}_{pose['suffix']}_{timestamp}.png"
                                    target_path = os.path.join(OUTPUT_BASE, target_name)
                                    with open(target_path, "wb") as f:
                                        f.write(img_data)
                                    print(f"Saved to: {target_path}")
            except Exception as e:
                print(f"Error generating {model['short']}_{pose['suffix']}: {e}")

if __name__ == "__main__":
    generate_punishment_batch()
