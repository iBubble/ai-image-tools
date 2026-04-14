import json
import urllib.request
import urllib.parse
import time
import uuid
import os

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

    def generate_image(self, positive_prompt, negative_prompt, checkpoint="realvisxl_v5.safetensors", width=1024, height=1024, seed=None):
        if seed is None:
            seed = int(time.time()) % 1125899906842624
            
        # Basic SDXL Workflow
        workflow = {
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": 25,
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
                    "filename_prefix": "ComfyUI_Antigravity",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            }
        }

        print(f"Submitting prompt: {positive_prompt[:50]}...")
        prompt_id = self.queue_prompt(workflow)['prompt_id']
        
        # Poll for completion
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

if __name__ == "__main__":
    # Test generation
    client = ComfyUIClient()
    pos = "A masterpiece photorealistic photo of a stunning 20yo Chinese woman, long black hair, realistic skin, server room, 8k"
    neg = "nsfw, low quality, bad anatomy"
    img, name = client.generate_image(pos, neg)
    if img:
        with open(f"test_comfy_{name}", "wb") as f:
            f.write(img)
        print(f"Success: test_comfy_{name}")
