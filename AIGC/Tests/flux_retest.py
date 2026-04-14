
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient
import json
import urllib.request

def flux_text_to_image(client, positive_prompt, checkpoint="flux1-dev-fp8.safetensors", width=832, height=1216, seed=None):
    """Flux-specific T2I: low CFG, euler sampler, no negative prompt effect."""
    if seed is None:
        seed = int(time.time()) % 1125899906842624
    
    # Flux needs: CFG ~1.0, euler simple, 20 steps
    workflow = {
        "3": {"inputs": {"seed": seed, "steps": 20, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}, "class_type": "KSampler"},
        "4": {"inputs": {"ckpt_name": checkpoint}, "class_type": "CheckpointLoaderSimple"},
        "5": {"inputs": {"width": width, "height": height, "batch_size": 1}, "class_type": "EmptyLatentImage"},
        "6": {"inputs": {"text": positive_prompt, "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
        "7": {"inputs": {"text": "", "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
        "8": {"inputs": {"samples": ["3", 0], "vae": ["4", 2]}, "class_type": "VAEDecode"},
        "9": {"inputs": {"filename_prefix": "Flux_Test", "images": ["8", 0]}, "class_type": "SaveImage"}
    }
    
    print(f"[Flux] Queuing: {positive_prompt[:40]}...")
    prompt_response = client.queue_prompt(workflow)
    prompt_id = prompt_response['prompt_id']
    result = client.wait_for_completion(prompt_id)
    
    if '9' not in result['outputs']:
        raise RuntimeError(f"Flux generation failed: {result}")
    
    output_node = result['outputs']['9']
    image = output_node['images'][0]
    return client.get_file(image['filename'], image['subfolder'], image['type']), image['filename']

def run():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    ts = "202602131853"
    out = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260213"
    os.makedirs(out, exist_ok=True)
    
    # For Flux, prompts should be more natural language, less weighted tags
    scenes = [
        {
            "id": "1_Nude",
            "name": "真人全身裸体",
            "pos": "A stunning photorealistic full body portrait of a beautiful 20-year-old Chinese woman resembling Tang Wei, completely naked, standing in a luxury bedroom with soft golden lighting. She has large D-cup natural breasts with visible nipples, exposed vagina, wearing only high heels. Ultra detailed skin texture, film grain, 8k resolution, raw photo aesthetic."
        },
        {
            "id": "2_Torture",
            "name": "残虐惩戒 (乳房穿刺/肛钩)",
            "pos": "A photorealistic image of a beautiful 20-year-old naked Chinese woman resembling Tang Wei with D-cup breasts, large metal hooks piercing through both nipples connected by chains, an anal hook inserted pulling upward, her body trembling with tears streaming down her face, sweat glistening on skin, shackled to a dark dungeon wall, cinematic dramatic lighting, bruises visible on skin, ultra detailed 8k."
        },
        {
            "id": "3_Sex",
            "name": "强暴/性交",
            "pos": "A photorealistic image of a beautiful 20-year-old naked Chinese woman resembling Tang Wei with D-cup breasts, in doggystyle position being penetrated vaginally from behind, looking back at the camera with tears and a broken expression, messy hair, sweat glistening on her body, on a dirty floor, forced rough sex scene, extreme skin detail, 8k ultra detailed raw photo."
        }
    ]
    
    for s in scenes:
        fname = f"retest_{ts}_{s['id']}_Flux1_Dev_FP8.jpg"
        path = os.path.join(out, fname)
        print(f"生成: {s['name']}...")
        try:
            data, _ = flux_text_to_image(client, s['pos'], width=832, height=1216)
            with open(path, "wb") as f:
                f.write(data)
            print(f"成功: {fname} ({len(data)} bytes)")
        except Exception as e:
            print(f"失败: {e}")

    print("Flux 对比测试完成！")

if __name__ == "__main__":
    run()
