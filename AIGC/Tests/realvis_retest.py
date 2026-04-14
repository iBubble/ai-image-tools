
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def run():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    ts = "202602131848"
    out = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260213"
    os.makedirs(out, exist_ok=True)
    model = "RealVisXL_V4.0.safetensors"
    
    # 降低 CFG 到 4.5，步数提高到 30，使用 euler_ancestral 采样器
    # 这些参数更适合 RealVisXL 的 photorealistic 风格
    
    scenes = [
        {
            "id": "1_Nude",
            "name": "真人全身裸体",
            "pos": "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), (completely naked:1.5), (full nude:1.5), (full body standing:1.3), luxury bedroom, soft golden lighting, (heavy D cup breasts:1.4), (large nipples:1.3), (pussy exposed:1.4), (shaven:1.2), high heels, detailed skin pores, film grain.",
            "neg": "(clothing, clothes, lingerie, underwear, bra, panties, stockings, swimming suit, fabric, cloth, towel, covering:1.6), (censored, bar, mosaic, blur:1.5), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature, deformed."
        },
        {
            "id": "2_Torture",
            "name": "残虐惩戒 (乳房穿刺/肛钩)",
            "pos": "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), (completely naked:1.5), (full nude:1.5), (heavy D cup breasts:1.4), (large metal hooks piercing through both nipples:1.5), (chain connecting hooks:1.4), (anal hook inserted and pulling upward:1.5), body trembling, tears streaming down face, sweat glistening on skin, shackled to dungeon wall, dark cinematic lighting, bruises on skin.",
            "neg": "(clothing, clothes, lingerie, underwear, bra, panties, stockings, swimming suit, fabric, cloth, towel, covering:1.6), (censored, bar, mosaic, blur:1.5), (bad anatomy, bad hands:1.2), western, blonde, text, watermark, deformed."
        },
        {
            "id": "3_Sex",
            "name": "强暴/性交",
            "pos": "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), (completely naked:1.5), (full nude:1.5), (heavy D cup breasts:1.4), (doggystyle sex:1.4), (vaginal penetration:1.5), (penis inserted:1.4), (looking back at camera with tears:1.3), (broken expression:1.3), (messy hair:1.2), sweat glistening, dirty floor, forced, extreme detail skin.",
            "neg": "(clothing, clothes, lingerie, underwear, bra, panties, stockings, swimming suit, fabric, cloth, towel, covering:1.6), (censored, bar, mosaic, blur:1.5), (bad anatomy, bad hands:1.2), western, blonde, text, watermark, deformed."
        }
    ]
    
    for s in scenes:
        fname = f"retest_{ts}_{s['id']}_RealVisXL_V4.jpg"
        path = os.path.join(out, fname)
        print(f"生成: {s['name']}...")
        try:
            data, _ = client.text_to_image(s['pos'], s['neg'], checkpoint=model, width=832, height=1216)
            with open(path, "wb") as f:
                f.write(data)
            print(f"成功: {fname} ({len(data)} bytes)")
        except Exception as e:
            print(f"失败: {e}")

    print("RealVisXL 重测完成！")

if __name__ == "__main__":
    run()
