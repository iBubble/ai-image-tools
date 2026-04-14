import os
import time
import json
import urllib.request
from PIL import Image
import uuid
import shutil

IMAGES = [
    "/Volumes/macData/Downloads/ComfyUI/Picz/refined_1774554594_304227468534.png",
    "/Volumes/macData/Downloads/ComfyUI/Picz/refined_1774468440_396511359292.png",
    "/Volumes/macData/Downloads/ComfyUI/Picz/refined_1774590139_314623887220.png"
]

COMFY_INPUT_DIR = "/Users/gemini/Projects/Own/ComfyUI/input"
COMFY_OUTPUT_DIR = "/Users/gemini/Projects/Own/ComfyUI/output"
FINAL_OUTPUT_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/outputs/Videos"

os.makedirs(FINAL_OUTPUT_DIR, exist_ok=True)

def process_and_copy_image(img_path):
    # Open image
    img = Image.open(img_path)
    w, h = img.size
    
    # Calculate scale to make max side <= 512 to avoid VRAM SSD swapping
    scale = 512.0 / max(w, h)
    
    # New dimensions (must be multiple of 16)
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    # Round to nearest 16
    new_w = (new_w // 16) * 16
    new_h = (new_h // 16) * 16
    
    if max(new_w, new_h) > 512:
        if new_w > 512: new_w -= 16
        if new_h > 512: new_h -= 16

    # Resize
    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    base_name = os.path.basename(img_path)
    new_name = f"resized_for_hunyuan_{base_name}"
    out_path = os.path.join(COMFY_INPUT_DIR, new_name)
    img_resized.save(out_path)
    
    return new_name, new_w, new_h

def wait_for_comfy():
    print("Waiting for ComfyUI to start...")
    while True:
        try:
            req = urllib.request.Request("http://127.0.0.1:8188/system_stats")
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    print("ComfyUI is ready.")
                    break
        except Exception:
            pass
        time.sleep(2)

def is_queue_empty():
    try:
        req = urllib.request.Request("http://127.0.0.1:8188/queue")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return len(data['queue_running']) == 0 and len(data['queue_pending']) == 0
    except Exception:
        return False

def submit_job(img_name, w, h, idx):
    prefix = f"HunyuanVideo_Job_{idx}"
    prompt = {
        "1": { "class_type": "UnetLoaderGGUF", "inputs": { "unet_name": "hunyuan-video-i2v-720p-Q5_K_M.gguf" } },
        "2": { "class_type": "DualCLIPLoader", "inputs": { "clip_name1": "llava_llama3_fp8_scaled.safetensors", "clip_name2": "clip_l.safetensors", "type": "hunyuan_video" } },
        "3": { "class_type": "VAELoader", "inputs": { "vae_name": "hunyuan_video_vae_bf16.safetensors" } },
        "4": { "class_type": "LoadImage", "inputs": { "image": img_name, "upload": "image" } },
        
        "5": { "class_type": "CLIPTextEncode", "inputs": { "text": "The character in the image starts moving naturally, highly detailed body animation, smooth action, highly realistic, 8k resolution, photorealistic.", "clip": ["2", 0] } },
        "6": { "class_type": "CLIPTextEncode", "inputs": { "text": "neon, glowing aura, magic effects, watermark, blurred, low quality, deformed, mutated, text", "clip": ["2", 0] } },
        
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
            "seed": int(time.time()) + idx * 100, 
            "control_after_generate": "randomize", 
            "steps": 30, 
            "cfg": 1.0, 
            "sampler_name": "euler", 
            "scheduler": "simple", 
            "denoise": 1.0, 
            "model": ["1", 0], 
            "positive": ["7", 0], 
            "negative": ["6", 0], 
            "latent_image": ["7", 1] 
        } },
        
        "9": { "class_type": "VAEDecode", "inputs": { "samples": ["8", 0], "vae": ["3", 0] } },
        "10": { "class_type": "VHS_VideoCombine", "inputs": { "frame_rate": 24, "loop_count": 0, "filename_prefix": prefix, "format": "video/h264-mp4", "pingpong": False, "save_output": True, "images": ["9", 0] } }
    }
    
    p = {"prompt": prompt, "client_id": str(uuid.uuid4())}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        print(f"Submitted Job {idx}. Response: ", response.read().decode('utf-8'))
    return prefix

def main():
    wait_for_comfy()
    
    prefixes = []
    
    for idx, path in enumerate(IMAGES):
        if not os.path.exists(path):
            print(f"Error: {path} not found.")
            continue
            
        print(f"Processing {path}...")
        new_name, new_w, new_h = process_and_copy_image(path)
        print(f"Resized to {new_w}x{new_h}, saved as {new_name}")
        
        prefix = submit_job(new_name, new_w, new_h, idx)
        prefixes.append(prefix)
        # small delay to ensure queue ordering
        time.sleep(2)
        
    print("All jobs submitted. Waiting for them to finish...")
    
    # Wait until queue is completely empty
    time.sleep(5)
    while True:
        if is_queue_empty():
            print("Queue is empty. Jobs finished.")
            break
        print("Queue is running... Wait 10 seconds.")
        time.sleep(10)
        
    # Copy files
    print("Copying files to final output...")
    time.sleep(2)
    for fname in os.listdir(COMFY_OUTPUT_DIR):
        for prefix in prefixes:
            if prefix in fname and fname.endswith(".mp4"):
                src = os.path.join(COMFY_OUTPUT_DIR, fname)
                dst = os.path.join(FINAL_OUTPUT_DIR, fname)
                if not os.path.exists(dst):
                    shutil.copyfile(src, dst)
                    print(f"Copied {fname}")
                    
    # Trigger Feishu push securely
    try:
        from push_videos import send_existing_videos
        send_existing_videos()
    except Exception as e:
        print("Failed to auto-push to Feishu:", e)
                    
if __name__ == '__main__':
    main()
