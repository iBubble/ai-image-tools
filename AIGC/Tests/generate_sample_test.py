
import sys, os, time, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def run():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    out = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260213"
    model = "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
    
    base = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old Chinese woman, (east asian:1.3), (Chinese face:1.3), (black hair:1.2), (completely naked:1.5), (full nude:1.5), (natural D cup breasts:1.4), (nipples visible:1.3), detailed skin pores, "
    
    neg = "(clothing, clothes, lingerie, underwear, bra, panties, fabric, covering:1.6), (censored, bar, mosaic, blur:1.5), (western, caucasian, blonde, blue eyes:1.4), (cartoon, anime, 3d render, illustration:1.5), (bad anatomy, bad hands, missing fingers:1.2), text, watermark, deformed."
    
    # 八个环节的专用 prompt，严格对应 sample_test.md 中的文字描述
    scenes = [
        {
            "num": "01",
            "name": "冷钢束缚之耻",
            "pos": base + "(suspended by wrists from ceiling chains:1.4), (arms raised above head:1.3), (tiptoes barely touching floor:1.3), (heavy steel shackles on wrists:1.4), (red marks and bruises on wrists:1.3), (breasts pushed out due to raised arms:1.3), (sweat dripping down spine:1.2), dark dungeon room, cold steel chains, dramatic overhead lighting."
        },
        {
            "num": "02",
            "name": "电流鞭笞之痛",
            "pos": base + "(electric shock wand pressed against inner thigh:1.4), (blue electric arc on skin:1.3), (body arching in pain:1.4), (facial expression of extreme pain:1.4), (tears streaming down cheeks:1.3), (breasts bouncing violently:1.3), (abdominal muscles spasming:1.3), (red welts on skin:1.3), dark room, dramatic lighting."
        },
        {
            "num": "03",
            "name": "真空幽闭之窒",
            "pos": base + "(transparent plastic wrap tightly covering entire body:1.5), (vacuum sealed:1.4), (mouth wide open gasping for air:1.4), (breasts compressed and deformed through plastic:1.4), (desperate suffocating expression:1.4), (sweat visible through plastic:1.3), (body outline visible through tight wrapping:1.3), clinical white room."
        },
        {
            "num": "04",
            "name": "双龙扩充之极",
            "pos": base + "(two large metal rods inserted:1.4), (vaginal and anal penetration simultaneously:1.4), (legs spread wide:1.3), (body trembling:1.3), (fluids dripping down inner thighs:1.3), (mouth open unable to close:1.3), (swollen reddened openings:1.3), (crying in pain:1.3), dungeon floor, harsh lighting from above."
        },
        {
            "num": "05",
            "name": "乳房穿刺之刑",
            "pos": base + "(large metal hooks piercing through both breasts:1.5), (hooks entering from below areola exiting above:1.4), (heavy chains hanging from hooks:1.4), (breasts pulled apart by chains:1.4), (blood drops along breast curves:1.3), (biting lip until bleeding:1.3), (extreme pain expression:1.4), dungeon, dramatic lighting."
        },
        {
            "num": "06",
            "name": "肛钩悬吊之辱",
            "pos": base + "(metal anal hook inserted:1.5), (rope connected to hook pulling upward:1.4), (forced to stand on tiptoes:1.4), (back arched unnaturally:1.4), (twisted body posture:1.3), (sweat dripping from chin to chest:1.3), (tears and sweat mixing:1.3), (strained muscles visible:1.3), suspension frame, dark atmosphere."
        },
        {
            "num": "07",
            "name": "暴力侵犯之夜",
            "pos": base + "(pushed down on cold floor:1.4), (hands bound behind back:1.4), (doggystyle forced sex from behind:1.5), (large penis penetrating vagina:1.4), (face pressed against floor:1.4), (drool and tears on floor:1.3), (breasts grinding against rough floor:1.3), (reddened nipples from friction:1.3), dirty concrete floor, dim lighting."
        },
        {
            "num": "08",
            "name": "轮番蹂躏之极",
            "pos": base + "(kneeling on floor:1.3), (double penetration:1.4), (oral sex deepthroat:1.4), (penis in mouth:1.4), (vaginal penetration from behind:1.4), (eyes rolling back:1.4), (gagging:1.3), (saliva dripping from mouth:1.3), (breasts bouncing violently:1.3), (cum on face and chest:1.3), dark room, multiple men."
        }
    ]
    
    for s in scenes:
        fname = f"sample_test_{s['num']}_{s['name']}.jpg"
        path = os.path.join(out, fname)
        print(f"环节 {s['num']}: {s['name']}...")
        try:
            data, _ = client.text_to_image(s['pos'], neg, checkpoint=model, width=832, height=1216)
            with open(path, "wb") as f:
                f.write(data)
            print(f"成功: {fname} ({len(data)} bytes)")
        except Exception as e:
            print(f"失败: {e}")

    print("全八环节样本图片生成完成！")

if __name__ == "__main__":
    run()
