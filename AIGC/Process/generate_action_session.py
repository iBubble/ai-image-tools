import json
import urllib.request
import time
import random
import os
from datetime import datetime

# 配置
REPO_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed"
OUTPUT_BASE = os.path.join(REPO_DIR, ".secret/punishments/20260227/Action")
os.makedirs(OUTPUT_BASE, exist_ok=True)

# 核心肉体盘 (长发波浪 + 狐尾肛塞 + 跳蛋)
POSITIVE_CORE = (
    "score_9, score_8_up, 1girl, solo, (chinese_identity:1.4), (long wavy black hair:1.5), 20 years old, beautiful realistic face, adult chinese female, "
    "(soft smooth skin:1.5), (wet body, sweaty, glistening skin, oily skin:1.4), "
    "(large breasts, D-cup, perky breasts, full breasts:1.3), (tiny pink areolas:1.5), (very small areolas:1.4), virgin areolas, erect nipples, "
    "(slender body:1.4), (thin waist:1.4), (full buttocks:1.3), wide hips, long straight legs, 168cm tall, completely naked, "
    "(sparse pubic hair:1.4), (fine short pubic hair:1.3), (a few scattered pubic hairs:1.4), (detailed pussy:1.5), realistic vulva, detailed labia, pink labia, "
    "(tightly contracted and completely closed small anus:1.6), (flat against skin:1.4), (no protrusion:1.5), "
    "detailed skin wrinkles, highly detailed, photorealistic, RAW photo, "
    "(fox tail anal plug:1.4), (fluffy fox tail:1.3), (vibrating egg in vagina:1.4), "
    "detailed rope bondage, tight red rope, shibari, rope cutting into skin"
)

NEGATIVE_CORE = (
    "score_4, score_3, score_2, score_1, (anime, cartoon, 3d render, painting:1.5), deformed, ugly, "
    "(skeletal, gaunt, emaciated:1.8), fleshy, thick legs, chubby, fat, "
    "(prolapsed, wide open anus:1.8), (eyepatch, sunglasses, mask:2.0), (large areolas:1.6), (shaved pussy:1.8), (anal hook:2.0)"
)

# 专项动作
ACTIONS = [
    {
        "desc": "kneeling on floor, bound with red ropes, (penis in mouth:1.6), (oral sex:1.5), forced deep throat, looking up with tears, saliva dripping, holding cock", 
        "suffix": "blowjob"
    },
    {
        "desc": "on all fours, doggy style, (pulling hair from behind:1.6), (long wavy hair being pulled:1.5), (penis in vagina:1.6), (vaginal penetration:1.5), arching back in pain and pleasure, crying, shaking", 
        "suffix": "doggy_hairpull"
    },
    {
        "desc": "extreme facial climax, (ahegao:1.6), rolling eyes, (body covered in thick white semen:1.8), (cum on face:1.6), (cum on breasts:1.6), (cum on belly:1.5), (splashed with semen:1.7), messy hair, exhausted", 
        "suffix": "orgasm_cumshot"
    }
]

MODELS = [
    {"name": "moodyV900001.ewMB.safetensors", "short": "moody"},
    {"name": "pornmasterZImage_turboV1.safetensors", "short": "pornmaster"}
]

def submit_session():
    server_address = "127.0.0.1:8188"
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    
    for action in ACTIONS:
        # 每个动作拍两次
        for copy_idx in [1, 2]:
            for model in MODELS:
                seed = random.randint(0, 0xffffffff)
                print(f"--- Submitting: {model['short']} | {action['suffix']} | #{copy_idx} ---")
                
                workflow = {
                    "1": {"inputs": {"unet_name": model['name'], "weight_dtype": "default"}, "class_type": "UNETLoader"},
                    "2": {"inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}, "class_type": "CLIPLoader"},
                    "3": {"inputs": {"vae_name": "ae.safetensors"}, "class_type": "VAELoader"},
                    "4": {"inputs": {"model": ["1", 0], "shift": 3.0}, "class_type": "ModelSamplingAuraFlow"},
                    "10": {"inputs": {"text": f"{POSITIVE_CORE}, {action['desc']}", "clip": ["2", 0]}, "class_type": "CLIPTextEncode"},
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
                    "50": {"inputs": {"filename_prefix": f"STORY_{model['short']}_{action['suffix']}_{timestamp}_{copy_idx}", "images": ["40", 0]}, "class_type": "SaveImage"}
                }

                p = {"prompt": workflow, "client_id": "ni_session"}
                data = json.dumps(p).encode('utf-8')
                req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
                try:
                    urllib.request.urlopen(req)
                except Exception as e:
                    print(f"Failed to submit: {e}")
                time.sleep(0.5)

if __name__ == "__main__":
    submit_session()
