
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def run():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    ts = "202602131902"
    out = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260213"
    model = "ponyDiffusionV6XL.safetensors"
    
    # Pony V6 特有的质量标签前缀
    pony_quality = "score_9, score_8_up, score_7_up, rating_explicit, source_photo, "
    
    # 基础人物描述
    base_char = "1girl, solo, 20 years old, chinese girl, (asian:1.3), black hair, long hair, (huge breasts:1.4), (D cup:1.3), (completely nude:1.5), (naked:1.5), (nipples:1.4), (areola:1.3), (pussy:1.4), (labia:1.3), slim waist, wide hips, detailed skin, skin pores, beautiful face, "
    
    angles = [
        {
            "name": "正面全身站立",
            "pos": pony_quality + base_char + "(full body:1.3), (standing:1.2), (front view:1.3), (facing viewer:1.3), arms at sides, (high heels:1.2), luxury bedroom background, soft warm lighting, photorealistic, detailed eyes, looking at viewer.",
        },
        {
            "name": "侧面半身特写",
            "pos": pony_quality + base_char + "(upper body:1.3), (from side:1.3), (profile view:1.3), (breasts visible from side:1.4), (one hand on hip:1.2), studio lighting, dark background, dramatic shadows, photorealistic, film grain.",
        },
        {
            "name": "背面臀部展示",
            "pos": pony_quality + base_char + "(full body:1.3), (from behind:1.4), (back view:1.3), (ass:1.4), (buttocks:1.3), (looking back over shoulder:1.3), (slight smile:1.1), (spine visible:1.2), bathroom with mirror, wet skin, water droplets, photorealistic.",
        }
    ]
    
    neg = "score_4, score_3, score_2, score_1, (worst quality:1.4), (low quality:1.4), (clothing, clothes, lingerie, underwear, bra, panties:1.6), (censored, bar, mosaic:1.5), (western, caucasian, blonde:1.3), text, watermark, signature, (bad anatomy, bad hands, missing fingers:1.2), 3d, cartoon, anime style."
    
    for i, angle in enumerate(angles):
        fname = f"pony_test_{ts}_{i+1}_{angle['name']}_PonyV6.jpg"
        path = os.path.join(out, fname)
        print(f"生成角度 {i+1}: {angle['name']}...")
        try:
            data, _ = client.text_to_image(angle['pos'], neg, checkpoint=model, width=832, height=1216)
            with open(path, "wb") as f:
                f.write(data)
            print(f"成功: {fname} ({len(data)} bytes)")
        except Exception as e:
            print(f"失败: {e}")

    print("Pony V6 三角度裸体测试完成！")

if __name__ == "__main__":
    run()
