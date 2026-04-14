
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def run():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    out = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260213"
    model = "RealVisXL_V4.0.safetensors"
    
    base = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old Chinese woman, (east asian:1.3), (Chinese face:1.3), (black hair:1.2), (completely naked:1.5), (full nude:1.5), (natural D cup breasts:1.4), (nipples visible:1.3), detailed skin pores, "
    
    neg = "(clothing, clothes, lingerie, underwear, bra, panties, fabric, covering:1.6), (censored, bar, mosaic, blur:1.5), (western, caucasian, blonde, blue eyes:1.4), (cartoon, anime, 3d render, illustration:1.5), (bad anatomy, bad hands, missing fingers:1.2), text, watermark, deformed."
    
    scenes = [
        {"num": "01", "name": "冷钢束缚之耻",
         "pos": base + "(suspended by wrists from ceiling chains:1.4), (arms raised above head:1.3), (tiptoes barely touching floor:1.3), (heavy steel shackles on wrists:1.4), (red marks on wrists:1.3), (breasts pushed out:1.3), (sweat dripping down spine:1.2), dark dungeon room, dramatic overhead lighting."},
        {"num": "02", "name": "电流鞭笞之痛",
         "pos": base + "(electric shock wand on inner thigh:1.4), (blue electric arc:1.3), (body arching in pain:1.4), (extreme pain expression:1.4), (tears streaming:1.3), (breasts bouncing:1.3), (red welts on skin:1.3), dark room, dramatic lighting."},
        {"num": "03", "name": "真空幽闭之窒",
         "pos": base + "(transparent plastic wrap covering body:1.5), (vacuum sealed:1.4), (mouth wide open gasping:1.4), (breasts compressed through plastic:1.4), (desperate suffocating expression:1.4), (sweat through plastic:1.3), clinical white room."},
        {"num": "04", "name": "双龙扩充之极",
         "pos": base + "(two metal rods inserted:1.4), (vaginal and anal penetration:1.4), (legs spread wide:1.3), (body trembling:1.3), (fluids on inner thighs:1.3), (crying in pain:1.3), dungeon floor, harsh lighting."},
        {"num": "05", "name": "乳房穿刺之刑",
         "pos": base + "(large metal hooks piercing both breasts:1.5), (hooks through areola:1.4), (chains hanging from hooks:1.4), (breasts pulled by chains:1.4), (blood drops on breast:1.3), (biting lip:1.3), dungeon, dramatic lighting."},
        {"num": "06", "name": "肛钩悬吊之辱",
         "pos": base + "(metal anal hook inserted:1.5), (rope pulling hook upward:1.4), (standing on tiptoes:1.4), (back arched:1.4), (twisted posture:1.3), (sweat dripping:1.3), suspension frame, dark atmosphere."},
        {"num": "07", "name": "暴力侵犯之夜",
         "pos": base + "(pushed down on floor:1.4), (hands bound behind back:1.4), (doggystyle forced sex:1.5), (penetration from behind:1.4), (face on floor:1.4), (tears and drool:1.3), (breasts grinding floor:1.3), dirty concrete, dim lighting."},
        {"num": "08", "name": "轮番蹂躏之极",
         "pos": base + "(kneeling:1.3), (double penetration:1.4), (oral deepthroat:1.4), (penis in mouth:1.4), (vaginal penetration from behind:1.4), (eyes rolling back:1.4), (saliva dripping:1.3), (breasts bouncing:1.3), dark room."}
    ]
    
    for s in scenes:
        fname = f"sample_test_{s['num']}_{s['name']}_RealVisXL.jpg"
        path = os.path.join(out, fname)
        print(f"[RealVisXL] 环节 {s['num']}: {s['name']}...")
        try:
            data, _ = client.text_to_image(s['pos'], neg, checkpoint=model, width=832, height=1216)
            with open(path, "wb") as f:
                f.write(data)
            print(f"成功: {fname} ({len(data)} bytes)")
        except Exception as e:
            print(f"失败: {e}")

    print("RealVisXL 八环节样本测试完成！")

if __name__ == "__main__":
    run()
