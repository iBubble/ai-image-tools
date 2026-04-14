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

    def upload_image(self, image_path):
        """Uploads a local image to ComfyUI server and returns the filename."""
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
            print(f"[ComfyUI] Image uploaded: {result.get('name')}")
            return result.get("name")

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_history(self, prompt_id):
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def get_file(self, filename, subfolder, folder_type):
        """Generic method to get file data (images or videos)."""
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}") as response:
            return response.read()

    def wait_for_completion(self, prompt_id):
        """Polls history until the prompt is finished."""
        while True:
            history = self.get_history(prompt_id)
            if prompt_id in history:
                return history[prompt_id]
            time.sleep(1)

    # --- Feature Methods ---

    def text_to_image(self, positive_prompt, negative_prompt, checkpoint="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors", width=1024, height=1024, seed=None, steps=25, cfg=7.0, sampler_name="dpmpp_2m", scheduler="karras"):
        """Classic Text-to-Image (T2I) using SDXL."""
        if seed is None: seed = int(time.time()) % 1125899906842624
            
        workflow = {
            "3": {"inputs": {"seed": seed, "steps": steps, "cfg": cfg, "sampler_name": sampler_name, "scheduler": scheduler, "denoise": 1.0, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}, "class_type": "KSampler"},
            "4": {"inputs": {"ckpt_name": checkpoint}, "class_type": "CheckpointLoaderSimple"},
            "5": {"inputs": {"width": width, "height": height, "batch_size": 1}, "class_type": "EmptyLatentImage"},
            "6": {"inputs": {"text": positive_prompt, "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
            "7": {"inputs": {"text": negative_prompt, "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
            "8": {"inputs": {"samples": ["3", 0], "vae": ["4", 2]}, "class_type": "VAEDecode"},
            "9": {"inputs": {"filename_prefix": "T2I_Antigravity", "images": ["8", 0]}, "class_type": "SaveImage"}
        }

        print(f"[ComfyUI] Queuing T2I ({checkpoint}): {positive_prompt[:30]}...")
        prompt_response = self.queue_prompt(workflow)
        prompt_id = prompt_response['prompt_id']
        result = self.wait_for_completion(prompt_id)
        
        if '9' not in result['outputs']:
             raise RuntimeError(f"Generation failed. Output node 9 not found in result: {result}")

        output_node = result['outputs']['9']
        image = output_node['images'][0]
        return self.get_file(image['filename'], image['subfolder'], image['type']), image['filename']

    def flux_to_image(self, prompt, width=832, height=1216, seed=None):
        """Flux-specific generation using UNETLoader and DualCLIPLoader."""
        if seed is None: seed = int(time.time()) % 1125899906842624
        
        workflow = {
            "10": {"inputs": {"unet_name": "flux1-dev-fp8.safetensors", "weight_dtype": "default"}, "class_type": "UNETLoader"},
            "11": {"inputs": {"clip_name1": "clip_l.safetensors", "clip_name2": "t5xxl_fp8_e4m3fn.safetensors", "type": "flux"}, "class_type": "DualCLIPLoader"},
            "12": {"inputs": {"vae_name": "ae.safetensors"}, "class_type": "VAELoader"},
            "6": {"inputs": {"text": prompt, "clip": ["11", 0]}, "class_type": "CLIPTextEncode"},
            "7": {"inputs": {"text": "", "clip": ["11", 0]}, "class_type": "CLIPTextEncode"},
            "5": {"inputs": {"width": width, "height": height, "batch_size": 1}, "class_type": "EmptyLatentImage"},
            "3": {"inputs": {"seed": seed, "steps": 20, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0, "model": ["10", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}, "class_type": "KSampler"},
            "8": {"inputs": {"samples": ["3", 0], "vae": ["12", 0]}, "class_type": "VAEDecode"},
            "9": {"inputs": {"filename_prefix": "Flux_Master", "images": ["8", 0]}, "class_type": "SaveImage"}
        }

        print(f"[ComfyUI] Queuing Flux: {prompt[:30]}...")
        prompt_response = self.queue_prompt(workflow)
        prompt_id = prompt_response['prompt_id']
        result = self.wait_for_completion(prompt_id)
        
        output_node = result['outputs']['9']
        image = output_node['images'][0]
        return self.get_file(image['filename'], image['subfolder'], image['type']), image['filename']

    def image_to_image(self, image_path, positive_prompt, negative_prompt, denoise=0.7, checkpoint="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors", seed=None):
        """Image-to-Image (I2I) using SDXL."""
        input_name = self.upload_image(image_path)
        if seed is None: seed = int(time.time()) % 1125899906842624
            
        workflow = {
            "3": {"inputs": {"seed": seed, "steps": 25, "cfg": 7, "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": denoise, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["10", 0]}, "class_type": "KSampler"},
            "4": {"inputs": {"ckpt_name": checkpoint}, "class_type": "CheckpointLoaderSimple"},
            "6": {"inputs": {"text": positive_prompt, "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
            "7": {"inputs": {"text": negative_prompt, "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
            "8": {"inputs": {"samples": ["3", 0], "vae": ["4", 2]}, "class_type": "VAEDecode"},
            "9": {"inputs": {"filename_prefix": "I2I_Antigravity", "images": ["8", 0]}, "class_type": "SaveImage"},
            "10": {"inputs": {"pixels": ["11", 0], "vae": ["4", 2]}, "class_type": "VAEEncode"},
            "11": {"inputs": {"image": input_name, "upload": "image"}, "class_type": "LoadImage"}
        }

        print(f"[ComfyUI] Queuing I2I based on {input_name}...")
        prompt_id = self.queue_prompt(workflow)['prompt_id']
        result = self.wait_for_completion(prompt_id)
        
        output_node = result['outputs']['9']
        image = output_node['images'][0]
        return self.get_file(image['filename'], image['subfolder'], image['type']), image['filename']

    def image_to_video(self, image_path, svd_model="svd.safetensors", width=1024, height=576, fps=12, motion_bucket_id=127, seed=None):
        """Image-to-Video (I2V) using SVD (Stable Video Diffusion)."""
        input_name = self.upload_image(image_path)
        if seed is None: seed = int(time.time()) % 1125899906842624

        workflow = {
            "1": {"inputs": {"ckpt_name": svd_model}, "class_type": "ImageOnlyCheckpointLoader"},
            "2": {"inputs": {"image": input_name, "upload": "image"}, "class_type": "LoadImage"},
            "3": {"inputs": {"width": width, "height": height, "video_frames": 25, "motion_bucket_id": motion_bucket_id, "fps": fps, "augmentation_level": 0, "clip_vision": ["1", 1], "init_image": ["2", 0]}, "class_type": "SVD_img2vid_Conditioning"},
            "4": {"inputs": {"seed": seed, "steps": 20, "cfg": 2.5, "sampler_name": "euler", "scheduler": "karras", "denoise": 1, "model": ["1", 0], "positive": ["3", 0], "negative": ["3", 1], "latent_image": ["3", 2]}, "class_type": "KSampler"},
            "5": {"inputs": {"samples": ["4", 0], "vae": ["1", 2]}, "class_type": "VAEDecode"},
            "6": {"inputs": {"filename_prefix": "I2V_Antigravity", "fps": fps, "lossless": False, "quality": 85, "method": "real-time", "images": ["5", 0]}, "class_type": "VideoCombine"} # Requires ComfyUI-VideoHelperSuite or similar
        }

        print(f"[ComfyUI] Queuing I2V (SVD) based on {input_name}...")
        prompt_id = self.queue_prompt(workflow)['prompt_id']
        result = self.wait_for_completion(prompt_id)
        
        # Note: Video output node structure might vary depending on the custom node used
        # Assuming VideoCombine from VideoHelperSuite
        for node_id in result['outputs']:
            node_output = result['outputs'][node_id]
            if 'gifs' in node_output: # VideoCombine often outputs in 'gifs' list even for mp4
                video_info = node_output['gifs'][0]
                return self.get_file(video_info['filename'], video_info['subfolder'], video_info['type']), video_info['filename']
        
        return None, "Video generation finished, check output folder."

    # Legacy support
    def generate_image(self, pos, neg, **kwargs):
        return self.text_to_image(pos, neg, **kwargs)

if __name__ == "__main__":
    client = ComfyUIClient()
    print("ComfyUI Client Library Enhanced.")
