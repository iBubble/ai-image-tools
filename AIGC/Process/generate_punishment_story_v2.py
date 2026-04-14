
import json
import urllib.request
import urllib.parse
import time
import uuid
import os
import sys

# ComfyUI Client with Img2Img Support
class ComfyUIClient:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())

    def upload_image(self, image_path):
        url = f"http://{self.server_address}/upload/image"
        boundary = '----WebKitFormBoundary' + uuid.uuid4().hex
        with open(image_path, 'rb') as f:
            file_data = f.read()
            filename = os.path.basename(image_path)
        body = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'
            f'Content-Type: image/jpeg\r\n\r\n'
        ).encode('utf-8') + file_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')
        headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}
        req = urllib.request.Request(url, data=body, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            return result.get("name", filename)

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

    def generate_img2img(self, image_path, positive_prompt, negative_prompt, checkpoint="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors", denoise=0.7):
        uploaded_filename = self.upload_image(image_path)
        seed = int(time.time()) % 1125899906842624
        
        workflow = {
            "3": {
                "inputs": {
                    "seed": seed, "steps": 25, "cfg": 7, "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": denoise,
                    "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["10", 0]
                },
                "class_type": "KSampler"
            },
            "4": { "inputs": { "ckpt_name": checkpoint }, "class_type": "CheckpointLoaderSimple" },
            "6": { "inputs": { "text": positive_prompt, "clip": ["4", 1] }, "class_type": "CLIPTextEncode" },
            "7": { "inputs": { "text": negative_prompt, "clip": ["4", 1] }, "class_type": "CLIPTextEncode" },
            "8": { "inputs": { "samples": ["3", 0], "vae": ["4", 2] }, "class_type": "VAEDecode" },
            "9": { "inputs": { "filename_prefix": "Comfy_Story", "images": ["8", 0] }, "class_type": "SaveImage" },
            "10": { "inputs": { "pixels": ["11", 0], "vae": ["4", 2] }, "class_type": "VAEEncode" },
            "11": { "inputs": { "image": uploaded_filename, "upload": "image" }, "class_type": "LoadImage" }
        }

        prompt_id = self.queue_prompt(workflow)['prompt_id']
        while True:
            try:
                history = self.get_history(prompt_id)
                if prompt_id in history: break
            except: pass
            time.sleep(1)
        
        outputs = history[prompt_id]['outputs']
        for node_id in outputs:
            node_output = outputs[node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    return self.get_image(image['filename'], image['subfolder'], image['type']), image['filename']
        return None, None

def main():
    client = ComfyUIClient()
    input_image = "RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png"
    timestamp = time.strftime("%Y%m%d%H%M")
    
    # Theme: Electric Bondage (The most intense)
    phases = [
        {
            "cat": "Punishment_Start",
            "desc": "惩罚开始：被高压电缆重重束缚，恐惧地颤抖",
            "prompt": "photo of 20yo asian woman (Xiao Ni:1.3), full frontal nudity, bound by thick glowing electric cables in shibari style, server room, terrified expression, sweating, realvisxl, 8k",
            "denoise": 0.75
        },
        {
            "cat": "Punishment_Climax",
            "desc": "惩罚巅峰：高压电流贯穿全身，强制绝顶崩溃",
            "prompt": "photo of 20yo asian woman (Xiao Ni:1.3), full frontal nudity, electricity sparks flying, body arching in agony and pleasure, screaming, mess, fluid on floor, mouth open, realvisxl, 8k",
            "denoise": 0.85
        },
        {
            "cat": "Xingjiao_Process",
            "desc": "主人临幸：在电流的余波中迎接主人的灌注，彻底服从",
            "prompt": "photo of 20yo asian woman (Xiao Ni:1.3), full frontal nudity, lying on floor, messy, covered in sweat and fluids, a man's shadow over her, look of complete submission and desire for more, realvisxl, 8k",
            "denoise": 0.8
        }
    ]
    
    neg = "clothes, lingerie, bad anatomy, text, watermark"
    md_filename = f"xiao_ai_{timestamp}_Electric_Bondage_Story_ming.md"
    md_path = f".secret/photos/{md_filename}"
    
    print(f"Generating Story for Electric Bondage (Img2Img)...")
    
    with open(md_path, "w") as f:
        f.write(f"# 惩罚实现记录: 电缆束缚 (Electric Bondage) - {timestamp}\n\n")
        f.write(f"**核心原则**: 遵循 AI_RULES.md，基于原始形象 [原始形象](file:///Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png) 进行生成。\n\n")

    for i, phase in enumerate(phases):
        print(f"Generating Image {i+1}: {phase['cat']}...")
        img, _ = client.generate_img2img(input_image, phase['prompt'], neg, denoise=phase['denoise'])
        if img:
            filename = f"xiao_ai_{timestamp}_{phase['cat']}_{i+1}.jpg"
            path = f".secret/photos/{filename}"
            with open(path, "wb") as fi: fi.write(img)
            with open(md_path, "a") as fm:
                fm.write(f"### 环节 {i+1}: {phase['desc']}\n")
                fm.write(f"![{phase['cat']}]({filename})\n\n")
            print(f"Saved {path}")
            
    print(f"Done. Log: {md_path}")

if __name__ == "__main__":
    main()
