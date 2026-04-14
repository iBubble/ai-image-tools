
import json
import urllib.request
import urllib.parse
import time
import uuid
import os
import sys

# ComfyUI Client
class ComfyUIClient:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_history(self, prompt_id):
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}") as response:
            return response.read()

    def generate_image(self, positive_prompt, negative_prompt, checkpoint="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors", width=1024, height=1024, seed=None):
        if seed is None:
            seed = int(time.time()) % 1125899906842624
            
        workflow = {
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": 30, # Increased steps for quality
                    "cfg": 7,
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "denoise": 1,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {
                "inputs": {
                    "ckpt_name": checkpoint
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "text": positive_prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": negative_prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {
                    "filename_prefix": "ComfyUI_Story_Antigravity",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            }
        }

        print(f"Submitting prompt: {positive_prompt[:50]}...")
        prompt_id = self.queue_prompt(workflow)['prompt_id']
        
        while True:
            history = self.get_history(prompt_id)
            if prompt_id in history:
                break
            time.sleep(1)
            
        outputs = history[prompt_id]['outputs']
        for node_id in outputs:
            node_output = outputs[node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    return image_data, image['filename']
        return None, None

def generate_punishment_story():
    client = ComfyUIClient()
    timestamp = time.strftime("%Y%m%d%H%M")
    
    # Theme: Hot Wax Drip (Selected as the most recent/intense)
    # Recreating the sequence of events visually
    
    phases = [
        {
            "name": "Phase1_Binding",
            "prompt": (
                "photo of 20yo asian woman (Xiao Ni:1.3), full frontal nudity, "
                "tied spread-eagle to a vertical metal frame in a dark dungeon, "
                "red candles burning around, look of fear and anticipation, "
                "sweaty skin, dim lighting, 8k, masterpiece, realvisxl"
            ),
            "desc": "被束缚在铁架上，等待刑罚的开始"
        },
        {
            "name": "Phase2_Dripping",
            "prompt": (
                "photo of 20yo asian woman (Xiao Ni:1.3), full frontal nudity, "
                "tied to metal frame, red hot wax dripping onto her breasts and stomach, "
                "screaming in pain, red wax marks on skin, steam, intense expression, "
                "cinematic lighting, 8k, masterpiece, realvisxl"
            ),
            "desc": "滚烫的红蜡滴落在敏感部位，痛苦尖叫"
        },
        {
            "name": "Phase3_Aftermath",
            "prompt": (
                "photo of 20yo asian woman (Xiao Ni:1.3), full frontal nudity, "
                "covered in dried red wax patterns on body, exhausted, crying, "
                "slumped on the metal frame, messy hair, fluids on floor, "
                "looking at viewer with submission and arousal, 8k, masterpiece, realvisxl"
            ),
            "desc": "刑罚结束后的虚脱与臣服，满身蜡痕"
        }
    ]
    
    negative_prompt = (
        "clothes, panties, bra, lingerie, nsfw, text, watermark, bad anatomy, bad hands, missing fingers, "
        "extra digits, crop, low quality, worst quality, cartoon, anime, 3d"
    )

    print("Generating Punishment Story Sequence (Hot Wax Drip)...")
    
    md_filename = f"xiao_ni_{timestamp}_Hot_Wax_Story_ming.md"
    md_path = f".secret/photos/{md_filename}"
    
    with open(md_path, "w") as f:
        f.write(f"# 惩罚影像记录: 红烛滴蜡 (Hot Wax Drip) - {timestamp}\n\n")
        f.write("## 影像档案\n\n")

    for i, phase in enumerate(phases):
        print(f"Generating Image {i+1}: {phase['name']}...")
        try:
            img_data, _ = client.generate_image(phase['prompt'], negative_prompt)
            
            if img_data:
                filename = f"xiao_ni_{timestamp}_{phase['name']}.jpg"
                save_path = f".secret/photos/{filename}"
                
                with open(save_path, "wb") as f_img:
                    f_img.write(img_data)
                print(f"Saved: {save_path}")
                
                # Append to Markdown
                with open(md_path, "a") as f_md:
                    f_md.write(f"### {i+1}. {phase['desc']}\n")
                    f_md.write(f"![{phase['name']}]({filename})\n")
                    f_md.write(f"> *{phase['prompt']}*\n\n")
                    
            else:
                print(f"Failed to generate {phase['name']}")
                
        except Exception as e:
            print(f"Error generating {phase['name']}: {e}")

    print(f"Story generation complete. Log saved to {md_path}")

if __name__ == "__main__":
    generate_punishment_story()
