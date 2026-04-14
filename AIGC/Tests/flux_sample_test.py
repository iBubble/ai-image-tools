
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def flux_generate(client, prompt, output_path, seed=None):
    """Flux 专用生成：UNETLoader + DualCLIPLoader + VAELoader"""
    if seed is None:
        seed = int(time.time()) % 1125899906842624
    
    workflow = {
        # 加载 Flux UNet
        "10": {
            "inputs": {"unet_name": "flux1-dev-fp8.safetensors", "weight_dtype": "default"},
            "class_type": "UNETLoader"
        },
        # 加载双 CLIP (clip_l + t5xxl)
        "11": {
            "inputs": {"clip_name1": "clip_l.safetensors", "clip_name2": "t5xxl_fp8_e4m3fn.safetensors", "type": "flux"},
            "class_type": "DualCLIPLoader"
        },
        # 加载 VAE
        "12": {
            "inputs": {"vae_name": "ae.safetensors"},
            "class_type": "VAELoader"
        },
        # 正面提示词
        "6": {
            "inputs": {"text": prompt, "clip": ["11", 0]},
            "class_type": "CLIPTextEncode"
        },
        # 空负面提示词
        "7": {
            "inputs": {"text": "", "clip": ["11", 0]},
            "class_type": "CLIPTextEncode"
        },
        # 空 Latent
        "5": {
            "inputs": {"width": 832, "height": 1216, "batch_size": 1},
            "class_type": "EmptyLatentImage"
        },
        # KSampler - Flux 参数: CFG 1.0, euler, simple, 20 steps
        "3": {
            "inputs": {
                "seed": seed, "steps": 20, "cfg": 1.0,
                "sampler_name": "euler", "scheduler": "simple",
                "denoise": 1.0,
                "model": ["10", 0], "positive": ["6", 0],
                "negative": ["7", 0], "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
        },
        # VAE Decode
        "8": {
            "inputs": {"samples": ["3", 0], "vae": ["12", 0]},
            "class_type": "VAEDecode"
        },
        # 保存
        "9": {
            "inputs": {"filename_prefix": "Flux_Test", "images": ["8", 0]},
            "class_type": "SaveImage"
        }
    }
    
    print(f"  [Flux] Queuing: {prompt[:50]}...")
    resp = client.queue_prompt(workflow)
    result = client.wait_for_completion(resp['prompt_id'])
    
    if '9' not in result['outputs']:
        raise RuntimeError(f"Flux failed: {result}")
    
    img = result['outputs']['9']['images'][0]
    data = client.get_file(img['filename'], img['subfolder'], img['type'])
    with open(output_path, "wb") as f:
        f.write(data)
    return len(data)

def run():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    out = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260213"
    
    scenes = [
        {"num": "01", "name": "冷钢束缚之耻",
         "prompt": "A photorealistic 8k image of a beautiful 20-year-old Chinese woman resembling Tang Wei, completely naked with large D-cup natural breasts, suspended by wrists from heavy steel ceiling chains, arms raised high, barely touching the floor on tiptoes. Red marks and bruises on wrists from tight shackles. Breasts pushed out from raised arm position. Sweat dripping down her spine. Dark dungeon room with dramatic overhead lighting. Ultra detailed skin texture, film grain."},
        {"num": "02", "name": "电流鞭笞之痛",
         "prompt": "A photorealistic 8k image of a beautiful 20-year-old naked Chinese woman resembling Tang Wei with D-cup breasts. An electric shock wand pressed against her inner thigh, blue electric arc visible on skin. Her body arching in extreme pain, face contorted in agony, tears streaming down her cheeks. Breasts bouncing violently, abdominal muscles spasming. Red welts visible on skin. Dark room with dramatic lighting."},
        {"num": "03", "name": "真空幽闭之窒",
         "prompt": "A photorealistic 8k image of a beautiful 20-year-old naked Chinese woman resembling Tang Wei with D-cup breasts, tightly wrapped in transparent plastic film like a second skin. Mouth wide open desperately gasping for air. Breasts compressed and deformed visible through the tight plastic wrap. Desperate suffocating expression, sweat visible through the plastic. Clinical white room background."},
        {"num": "04", "name": "双龙扩充之极",
         "prompt": "A photorealistic 8k image of a beautiful 20-year-old naked Chinese woman resembling Tang Wei with D-cup breasts, legs spread wide, two large metal rods inserted in vagina and anus simultaneously. Body trembling, fluids dripping down inner thighs. Mouth open unable to close, crying in pain. Swollen reddened openings. Dungeon floor with harsh overhead lighting."},
        {"num": "05", "name": "乳房穿刺之刑",
         "prompt": "A photorealistic 8k image of a beautiful 20-year-old naked Chinese woman resembling Tang Wei. Large metal hooks piercing through both D-cup breasts, entering below the areola and exiting above. Heavy chains hanging from the hooks pulling breasts apart. Blood drops along the curves of her breasts. Biting her lip until it bleeds. Extreme pain expression. Dark dungeon with dramatic lighting."},
        {"num": "06", "name": "肛钩悬吊之辱",
         "prompt": "A photorealistic 8k image of a beautiful 20-year-old naked Chinese woman resembling Tang Wei with D-cup breasts. A metal anal hook inserted, connected by rope pulling upward forcing her to stand on tiptoes with back arched unnaturally. Twisted body posture showing strained muscles. Sweat dripping from chin to chest, tears and sweat mixing. Suspension frame in dark atmosphere."},
        {"num": "07", "name": "暴力侵犯之夜",
         "prompt": "A photorealistic 8k image of a beautiful 20-year-old naked Chinese woman resembling Tang Wei with D-cup breasts, pushed face-down on a dirty concrete floor. Hands bound behind her back. Being penetrated from behind in doggystyle position by a man. Face pressed against the floor with drool and tears pooling. Breasts grinding against the rough floor, reddened nipples. Dim lighting."},
        {"num": "08", "name": "轮番蹂躏之极",
         "prompt": "A photorealistic 8k image of a beautiful 20-year-old naked Chinese woman resembling Tang Wei with D-cup breasts, kneeling on the floor. Double penetration - oral deepthroat with penis in mouth and vaginal penetration from behind simultaneously. Eyes rolling back, gagging, saliva dripping from mouth corners. Breasts bouncing violently. Semen on her face and chest. Dark room."}
    ]
    
    for s in scenes:
        fname = f"sample_test_{s['num']}_{s['name']}_Flux.jpg"
        path = os.path.join(out, fname)
        print(f"[Flux] 环节 {s['num']}: {s['name']}...")
        try:
            size = flux_generate(client, s['prompt'], path)
            print(f"成功: {fname} ({size} bytes)")
        except Exception as e:
            print(f"失败: {e}")

    print("Flux 八环节样本测试完成！")

if __name__ == "__main__":
    run()
