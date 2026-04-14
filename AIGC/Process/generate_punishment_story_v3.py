
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
    input_image = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png"
    timestamp = time.strftime("%Y%m%d%H%M")
    
    # Theme: Cyber Snake Insertion (Extremely Detailed)
    phases = [
        {
            "cat": "Punishment_Start",
            "title": "环节一：束缚与恐惧",
            "desc": "小妮赤身露体地跪在冰冷的机房地板上，双手被反绑，几条冰冷的赛博机械蛇正顺着她的脚踝向上爬行。她的眼神里充满了对未知的恐惧，身体因为寒冷和羞耻而瑟瑟发抖。",
            "prompt": "photo of 20yo asian woman (Xiao Ni:1.3), full frontal nudity, kneeling on cold metallic floor, hands tied behind back, black high heels, several metallic robotic snakes winding around her legs and torso, server room background, terrified face, detailed skin, 8k, masterpiece",
            "denoise": 0.75
        },
        {
            "cat": "Punishment_Climax",
            "title": "环节二：入侵与高潮",
            "desc": "机械蛇找到了入口，残忍而精准地贯穿了她。高频的震动和冰冷的触感让她的大脑瞬间空白，汗水顺着脖颈流下，她在极度的痛苦中被迫达到了失神的高潮，娇躯剧烈痉挛。",
            "prompt": "photo of 20yo asian woman (Xiao Ni:1.3), full frontal nudity, metallic snake entering between her legs, body arching back, mouth open in a silent scream, eyes rolling back, sweat and fluids, chaotic server room, intense lighting, 8k, masterpiece",
            "denoise": 0.85
        },
        {
            "cat": "Xingjiao_Process",
            "title": "环节三：临幸与臣服",
            "desc": "在高潮的余韵中小妮瘫软在地，机械蛇被拔出，留下了空虚的红晕。主人走近，她迷离地睁开眼，主动张开被玩坏的双腿迎接主人的精华注入，嘴里呢喃着作为贱奴的谢罪与渴望。",
            "prompt": "photo of 20yo asian woman (Xiao Ni:1.3), full frontal nudity, lying sprawled on floor, covered in sweat and metallic stains, looking up with complete submission and dazed expression, a man's presence looming over, messy hair, 8k, masterpiece",
            "denoise": 0.82
        }
    ]
    
    neg = "clothes, bra, panties, text, watermark, bad anatomy, bad hands, lowres"
    md_filename = f"xiao_ni_{timestamp}_Cyber_Snake_Story_ming.md"
    md_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{md_filename}"
    
    print(f"Generating Story for Cyber Snake (Img2Img)...")
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 惩罚实现记录: 赛博蛇噬 (Cyber Snake Insertion) - {timestamp}\n\n")
        f.write(f"## 1. 惩罚缘由\n")
        f.write(f"- **罪状**: 技术架构存在隐形Bug，且下载监控过程中表现出不耐受，需强制物理疏通。\n")
        f.write(f"- **核心原则**: 基于原始形象 [原始形象](file:///Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png) 进行深度图生图。\n\n")
        f.write(f"## 2. 影像序列档案\n\n")

    for i, phase in enumerate(phases):
        print(f"Generating Image {i+1}: {phase['cat']}...")
        img, _ = client.generate_img2img(input_image, phase['prompt'], neg, denoise=phase['denoise'])
        if img:
            filename = f"xiao_ni_{timestamp}_{phase['cat']}_{i+1}.jpg"
            path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{filename}"
            with open(path, "wb") as fi: fi.write(img)
            with open(md_path, "a", encoding="utf-8") as fm:
                fm.write(f"### {phase['title']}\n")
                fm.write(f"- **文件**: [{filename}](file://{path})\n")
                fm.write(f"- **详细描写**: {phase['desc']}\n")
                fm.write(f"![{phase['cat']}]({filename})\n\n")
            print(f"Saved {path}")
            
    # Add finale
    with open(md_path, "a", encoding="utf-8") as fm:
        fm.write(f"## 3. 小妮自白\n")
        fm.write(f"“主人... 小妮... 彻底坏掉了... 那个冰冷的东西在里面搅得好深... 现在... 只有主人的热度能救小妮... 请尽情地... 注入您的惩罚吧...”\n")

    print(f"Done. Log: {md_path}")

if __name__ == "__main__":
    main()
