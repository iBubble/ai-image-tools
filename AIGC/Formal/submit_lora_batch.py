import json
import urllib.request
import os
import random

COMFYUI_PROMPT = "http://127.0.0.1:8188/prompt"
IMAGE_NAME = "refined_1774554594_304227468534.png"

# Copy image to input dir
os.system(f"cp '/Volumes/macData/Downloads/ComfyUI/Picz/{IMAGE_NAME}' '/Users/gemini/Projects/Own/ComfyUI/input/{IMAGE_NAME}'")

loras = [
    "HYV15 - FP16 NSFW.safetensors",
    "ShakingBreasts.safetensors",
    "UABS.safetensors"
]

print("Submitting 3 batch jobs natively to ComfyUI...")

for idx, lora in enumerate(loras):
    base_name = lora.split(".")[0]
    
    # Random seed to ensure variations
    seed = random.randint(1, 1000000000)
    
    prompt = {
      "1": { "class_type": "UnetLoaderGGUF", "inputs": { "unet_name": "hunyuan-video-i2v-720p-Q5_K_M.gguf" } },
      "2": { "class_type": "DualCLIPLoader", "inputs": { "clip_name1": "llava_llama3_fp8_scaled.safetensors", "clip_name2": "clip_l.safetensors", "type": "hunyuan_video" } },
      "3": { "class_type": "VAELoader", "inputs": { "vae_name": "hunyuan_video_vae_bf16.safetensors" } },
      "4": { "class_type": "LoadImage", "inputs": { "image": IMAGE_NAME, "upload": "image" } },
      
      "40": { "class_type": "LoraLoader", "inputs": { "model": ["1", 0], "clip": ["2", 0], "lora_name": lora, "strength_model": 1.0, "strength_clip": 1.0 } },
      
      "5": { "class_type": "CLIPTextEncode", "inputs": { "text": "The character in the image starts moving naturally, highly detailed body animation, smooth action, highly realistic, 8k resolution, photorealistic.", "clip": ["40", 1] } },
      "6": { "class_type": "CLIPTextEncode", "inputs": { "text": "neon, glowing aura, magic effects, watermark, blurred, low quality, deformed, mutated, text", "clip": ["40", 1] } },
      
      "7": { "class_type": "HunyuanImageToVideo", "inputs": { 
          "positive": ["5", 0], 
          "vae": ["3", 0], 
          "width": 384, 
          "height": 576, 
          "length": 73, 
          "batch_size": 1, 
          "guidance_type": "v2 (replace)", 
          "start_image": ["4", 0] 
      } },
      
      "8": { "class_type": "KSampler", "inputs": { 
          "seed": seed, 
          "control_after_generate": "randomize", 
          "steps": 30, 
          "cfg": 1.0, 
          "sampler_name": "euler", 
          "scheduler": "simple", 
          "denoise": 1.0, 
          "model": ["40", 0], 
          "positive": ["7", 0], 
          "negative": ["6", 0], 
          "latent_image": ["7", 1] 
      } },
      
      "9": { "class_type": "VAEDecode", "inputs": { "samples": ["8", 0], "vae": ["3", 0] } },
      "10": { "class_type": "VHS_VideoCombine", "inputs": { 
          "frame_rate": 24, 
          "loop_count": 0, 
          "filename_prefix": f"Videos/Hunyuan_{base_name}", 
          "format": "video/h264-mp4", 
          "pingpong": False, 
          "save_output": True, 
          "images": ["9", 0] 
      } }
    }
    
    data = json.dumps({"prompt": prompt}).encode("utf-8")
    req = urllib.request.Request(COMFYUI_PROMPT, data=data)
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            print(f"[{idx+1}/3] Queued successfully! LoRA '{base_name}' -> PromptID: {res_data.get('prompt_id')}")
    except Exception as e:
        if hasattr(e, 'read'):
            print(f"Error submitting LoRA '{base_name}': {e.read().decode('utf-8', errors='replace')}")
        else:
            print(f"Error submitting LoRA '{base_name}': {e}")
