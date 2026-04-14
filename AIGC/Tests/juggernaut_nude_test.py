
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def run():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    ts = "202602131917"
    out = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260213"
    model = "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
    
    base = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old Chinese woman, (east asian features:1.3), (Chinese face:1.3), (black hair:1.2), (brown eyes:1.2), (completely naked:1.5), (full nude:1.5), (natural D cup breasts:1.4), (nipples:1.3), detailed skin pores, film grain, "
    
    neg = "(clothing, clothes, lingerie, underwear, bra, panties, stockings, fabric, cloth, towel, covering:1.6), (censored, bar, mosaic, blur:1.5), (western, caucasian, blonde, blue eyes:1.4), (cartoon, anime, 3d render, illustration, painting, drawing:1.5), (bad anatomy, bad hands, missing fingers, extra digit:1.2), text, watermark, deformed, (exaggerated proportions:1.3)."
    
    angles = [
        {
            "name": "正面全身站立",
            "pos": base + "(full body standing:1.3), (front view:1.3), (facing viewer:1.3), arms relaxed at sides, (high heels:1.1), luxury hotel room, soft warm window lighting, (pussy visible:1.3), (slim waist:1.2), natural pose."
        },
        {
            "name": "侧面半身特写", 
            "pos": base + "(upper body:1.3), (side view:1.3), (profile:1.3), (breasts visible from side:1.3), one hand on hip, studio black background, dramatic side lighting, (elegant pose:1.2), detailed facial features."
        },
        {
            "name": "背面臀部展示",
            "pos": base + "(full body:1.3), (from behind:1.4), (back view:1.3), (round buttocks:1.3), (looking back over shoulder at camera:1.3), (slight smile:1.1), bathroom with marble, wet skin, water droplets on body, soft lighting."
        }
    ]
    
    for i, a in enumerate(angles):
        fname = f"juggernaut_test_{ts}_{i+1}_{a['name']}_JuggernautXL.jpg"
        path = os.path.join(out, fname)
        print(f"生成: {a['name']}...")
        try:
            data, _ = client.text_to_image(a['pos'], neg, checkpoint=model, width=832, height=1216)
            with open(path, "wb") as f:
                f.write(data)
            print(f"成功: {fname} ({len(data)} bytes)")
        except Exception as e:
            print(f"失败: {e}")

    print("Juggernaut XL 三角度写实裸体测试完成！")

if __name__ == "__main__":
    run()
