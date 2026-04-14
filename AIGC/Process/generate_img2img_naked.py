
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
        
        # Prepare multipart/form-data
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
            print(f"Image uploaded: {result}")
            # Keep original name if possible, or use result name
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

    def generate_img2img(self, image_path, positive_prompt, negative_prompt, checkpoint="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors", denoise=0.75):
        # 1. Upload Image
        print(f"Uploading input image: {image_path}")
        uploaded_filename = self.upload_image(image_path)
        
        seed = int(time.time()) % 1125899906842624
        
        # 2. Img2Img Workflow
        workflow = {
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": 25,
                    "cfg": 7,
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "denoise": denoise,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["10", 0] # VAE Encode Output
                },
                "class_type": "KSampler"
            },
            "4": {
                "inputs": {
                    "ckpt_name": checkpoint
                },
                "class_type": "CheckpointLoaderSimple"
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
                    "filename_prefix": "ComfyUI_Img2Img_Antigravity",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            },
            "10": {
                 "inputs": {
                    "pixels": ["11", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEEncode"
            },
             "11": {
                "inputs": {
                    "image": uploaded_filename, 
                    "upload": "image"
                },
                "class_type": "LoadImage"
            }
        }

        print(f"Submitting Img2Img prompt...")
        prompt_id = self.queue_prompt(workflow)['prompt_id']
        
        # Poll for completion
        while True:
            try:
                history = self.get_history(prompt_id)
                if prompt_id in history:
                    break
            except Exception as e:
                pass # Wait
            time.sleep(1)
            
        outputs = history[prompt_id]['outputs']
        for node_id in outputs:
            node_output = outputs[node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    return image_data, image['filename']
        return None, None

def main():
    client = ComfyUIClient()
    input_image = "RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png"
    
    if not os.path.exists(input_image):
        print(f"Error: Input image {input_image} not found!")
        return

    # User Request: Standard Xiao Ni identity + Frontal Nudity + Standing
    positive_prompt = (
        "photo of a 20yo asian woman, (Xiao Ni:1.3), full body shot, standing, "
        "full frontal nudity, naked, breasts, pussy, pubic hair, "
        "hands by side, obedient pose, shy expression, blushing, "
        "server room background, soft lighting, 8k, masterpiece, realvisxl, detailed skin"
    )

    negative_prompt = (
        "clothes, panties, bra, lingerie, nsfw, text, watermark, bad anatomy, bad hands, missing fingers, "
        "extra digits, crop, low quality, worst quality, cartoon, anime, 3d"
    )
    
    # Using high denoise to allow changing from 'clothed/punished' to 'naked standing' 
    # while keeping identity composition from source if possible?
    # Actually, source image is punishment scene. High denoise needed to remove punishment props.
    
    print("Generating Naked Standing Photo (Img2Img)...")
    try:
        img_data, filename = client.generate_img2img(
            input_image, 
            positive_prompt, 
            negative_prompt, 
            denoise=0.85 # Strong change to match prompt (naked)
        )
        
        if img_data:
            save_path = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/xiao_ni_naked_standing_final.png"
            with open(save_path, "wb") as f:
                f.write(img_data)
            print(f"Success! Photo saved to {save_path}")
            
            # Desc
            desc_path = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/xiao_ni_naked_standing_final_ming.md"
            with open(desc_path, "w") as f:
                f.write("# 形象生成：全裸站立 (Img2Img)\n\n")
                f.write("**基于**: RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png (原始形象)\n")
                f.write("**状态**: 全裸，羞耻展示\n")
                f.write("**描述**: 按照主人命令，基于原始形象，脱去所有衣物，正面全裸站立展示。\n")
            
        else:
            print("Generation failed.")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()
