import urllib.request
import json
import uuid

prompt = {
  "1": { "class_type": "UnetLoaderGGUF", "inputs": { "unet_name": "hunyuan-video-i2v-720p-Q5_K_M.gguf" } },
  "2": { "class_type": "DualCLIPLoader", "inputs": { "clip_name1": "llava_llama3_fp8_scaled.safetensors", "clip_name2": "clip_l.safetensors", "type": "hunyuan_video" } },
  "3": { "class_type": "VAELoader", "inputs": { "vae_name": "hunyuan_video_vae_bf16.safetensors" } },
  "4": { "class_type": "LoadImage", "inputs": { "image": "refined_1774547434_346485706515.png", "upload": "image" } },
  
  "40": { "class_type": "LoraLoader", "inputs": { "model": ["1", 0], "clip": ["2", 0], "lora_name": "side-missionary-e125-az420.safetensors", "strength_model": 1.0, "strength_clip": 1.0 } },
  
  "5": { "class_type": "CLIPTextEncode", "inputs": { "text": "The character in the image starts moving naturally, highly detailed body animation, smooth action, highly realistic, 8k resolution, photorealistic.", "clip": ["40", 1] } },
  "6": { "class_type": "CLIPTextEncode", "inputs": { "text": "neon, glowing aura, magic effects, watermark, blurred, low quality, deformed, mutated, text", "clip": ["40", 1] } },
  
  "7": { "class_type": "HunyuanImageToVideo", "inputs": { 
      "positive": ["5", 0], 
      "vae": ["3", 0], 
      "width": 384, 
      "height": 512, 
      "length": 49, 
      "batch_size": 1, 
      "guidance_type": "v2 (replace)", 
      "start_image": ["4", 0] 
  } },
  
  "8": { "class_type": "KSampler", "inputs": { 
      "seed": 99815, 
      "control_after_generate": "randomize", 
      "steps": 30, 
      "cfg": 1.5, 
      "sampler_name": "euler", 
      "scheduler": "simple", 
      "denoise": 1.0, 
      "model": ["40", 0], 
      "positive": ["7", 0], 
      "negative": ["6", 0], 
      "latent_image": ["7", 1] 
  } },
  
  "9": { "class_type": "VAEDecode", "inputs": { "samples": ["8", 0], "vae": ["3", 0] } },
  "10": { "class_type": "VHS_VideoCombine", "inputs": { "frame_rate": 24, "loop_count": 0, "filename_prefix": "videos/Hunyuan_NSFW", "format": "video/h264-mp4", "pingpong": False, "save_output": True, "images": ["9", 0] } }
}

client_id = str(uuid.uuid4())
p = {"prompt": prompt, "client_id": client_id}
data = json.dumps(p).encode('utf-8')
req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data)
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except Exception as e:
    import traceback
    print("API Error:", e)
    try:
        print(e.read().decode('utf-8'))
    except:
        pass
