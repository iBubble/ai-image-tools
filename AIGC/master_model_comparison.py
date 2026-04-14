
import sys, os, time, json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def run_comparison():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    date_str = "20260213"
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_str}"
    os.makedirs(target_dir, exist_ok=True)
    
    models = [
        {"name": "RealVisXL", "file": "RealVisXL_V4.0.safetensors", "type": "sdxl"},
        {"name": "JuggernautXL", "file": "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors", "type": "sdxl"},
        {"name": "PonyV6", "file": "ponyDiffusionV6XL.safetensors", "type": "sdxl"},
        {"name": "Flux", "file": "flux1-dev-fp8.safetensors", "type": "flux"}
    ]
    
    # Base requirements: Asian Tang Wei, 20yo, D-cup, naked except high heels, painful expressions.
    # Refined Flux focus: Natural human anatomy, no mutations, clean realistic skin.
    # Pony specific: Booru tags, quality scores, explicit Chinese/Asian identity tags.
    # Pony 终极优化版：整合面部细化标签（epicanthic fold, almond eyes等）+ 体型优化 + 标签顺序优化
    base_desc_sdxl = "A high-quality photorealistic 8k image of a 20-year-old sexy Chinese woman resembling Tang Wei, east asian features, black hair. Completely naked except for high heels, showing full body including genitals (pussy and anus visible), huge natural D-cup breasts with detailed nipples."
    
    base_desc_flux = "A high-quality realistic photo of a beautiful 20-year-old Chinese woman resembling Tang Wei. She is completely naked, wearing only high heels. Detailed D-cup breasts, natural nipples. Full body shot featuring natural and anatomically correct female genitals. The pussy and vagina are clearly visible, clean, and realistic with normal skin texture. NO BODY HORROR, NO MUTATIONS, NO EXTRA PARTS. Everything looks like a real human woman. Clearly visible and uncovered crotch area."
    
    # Pony 终极优化版 - 严格遵循标签顺序：质量分 → 身份 → 面部 → 发型 → 体型 → 场景
    base_desc_pony = """score_9, score_8_up, score_7_up, score_6_up, 
1girl, solo, 
(chinese:1.3), (east asian:1.2), 
beautiful face, soft facial features, 
brown eyes, dark eyes, almond eyes, epicanthic fold, hooded eyelids,
small nose, flat bridge, small lips, cherry lips,
round face, heart-shaped face, soft jawline, smooth skin, pale skin,
long straight black hair, shiny hair, blunt bangs,
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2), (slim waist:1.1), (narrow shoulders:1.1),
huge natural breasts, natural nipples, smooth nipples,
completely naked, wearing high heels,
(explicit:1.2), genitals, pussy, anus, rating_explicit,
photo (medium), realistic, highly detailed, cinematic lighting"""
        
    stages = [
        {"id": "01", "name": "冷钢束缚", 
         "sdxl": "suspended by wrists from chains, arms raised, tiptoes, painful expression, genitals visible.", 
         "flux": "suspended by wrists from chains, arms raised above head, tiptoes. Her legs are spread to show her natural, uncovered, and realistic pussy. Clear view of natural human genitals. Painful expression, sweat dripping."},
        {"id": "02", "name": "电流鞭笞", 
         "sdxl": "electric shock wand on inner thigh, body arching in pain, tears, breasts bouncing, genitals exposed.", 
         "flux": "an electric shock wand being used on her inner thigh, blue electric arc. Her legs are forced wide apart as her body arches in extreme pain, providing a clear and realistic view of her natural vagina and anus. Face contorted in agony with tears, breasts bouncing."},
        {"id": "03", "name": "真空幽闭", 
         "sdxl": "wrapped in transparent plastic, vacuum sealed, mouth gasping, breasts compressed, genitals visible through plastic.", 
         "flux": "wrapped tightly in transparent plastic film, vacuum sealed. The clear plastic is pressed tightly against her skin, revealing her natural and realistic pussy and anus underneath without any distortion. Natural human anatomy. Mouth wide open gasping for air, breasts compressed."},
        {"id": "04", "name": "双龙扩充", 
         "sdxl": "two large metal rods inserted in vagina and anus, legs spread wide, body trembling, fluids dripping.", 
         "flux": "two large metal rods inserted in her vagina and anus. Her legs are forced into a wide spread-eagle position, giving a direct, uncovered, and realistic view of the natural human genitals and the insertion. Body trembling, fluids dripping, mouth open in pain."},
        {"id": "05", "name": "乳房穿刺", 
         "sdxl": "metal hooks piercing through breasts, chains pulling breasts apart, blood, biting lip, genitals exposed.", 
         "flux": "metal hooks piercing through both breasts, chains pulling breasts apart. Standing with her legs forced apart, her natural pussy is completely bare, uncovered, and visible. Blood drops on skin, biting lip, extreme agony."},
        {"id": "06", "name": "肛钩悬吊", 
         "sdxl": "metal anal hook pulling upward, tiptoes, arched back, sweat and tears, anus and vagina exposed.", 
         "flux": "a large metal anal hook inserted and pulling her body upward. Forced to stand on tiptoes with her back arched and buttocks spread wide, giving a clear and realistic view of the anus and her natural pussy. Strained muscles, sweat and tears mixing."},
        {"id": "07", "name": "暴力侵犯", 
         "sdxl": "forced sex from behind on concrete floor, hands bound, breasts grinding, genitals exposed.", 
         "flux": "forced sex from behind on concrete. Kneeling in doggystyle position, her buttocks are spread wide as she is penetrated, showing a realistic and natural view of the anus and vagina. Hands bound, face pressed to ground, broken expression."},
        {"id": "08", "name": "轮番蹂躏", 
         "sdxl": "double penetration, oral deepthroat, gagging, cum on face, genitals completely exposed.", 
         "flux": "double penetration with oral deepthroat and vaginal penetration from behind. Her legs are forced wide apart to show the penetration in the vagina and anus clearly. Natural and realistic view of the genitals, no mutations. Eyes rolling back, gagging, cum on face."}
    ]
    
    neg_sdxl = "(clothing, clothes, lingerie, underwear, bra, panties, fabric, covering:1.6), (censored, bar, mosaic, blur:1.5), (cartoon, anime, 3d, illustration:1.6), western, blonde, bad anatomy, text, watermark, (mutation, body horror, extra limbs, distorted genitals:1.4)."
    neg_pony = "score_4, score_5, score_6, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, (western features:1.3), deep eyes, high nose bridge, (freckles:1.2), cleft chin, rough skin, (clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4), (muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2), (textured nipples:1.3), (ringed nipples:1.3), (areola texture:1.2), (bumpy nipples:1.2)."
    
    report_md = "# 🏆 全模型八环节极致横评记录 (Pony优化版) - 202602132320\n\n"
    report_md += "| 环节 | RealVisXL V4 | Juggernaut XL | Pony V6 | Flux1-Dev |\n"
    report_md += "| :--- | :---: | :---: | :---: | :---: |\n"
    
    for s in stages:
        row = f"| {s['id']}-{s['name']} | "
        for m in models:
            filename = f"comp_{s['id']}_{m['name']}.jpg"
            save_path = os.path.join(target_dir, filename)
            print(f"[{m['name']}] 正在生成环节 {s['id']}: {s['name']}...")
            
            if m['type'] == "flux":
                prompt = f"{base_desc_flux} {s['flux']}"
            elif m['name'] == "PonyV6":
                prompt = f"{base_desc_pony}, {s['sdxl']}"
            else:
                prompt = f"{base_desc_sdxl} {s['sdxl']}"
            
            try:
                if m['type'] == "flux":
                    img_data, _ = client.flux_to_image(prompt, width=832, height=1216)
                else:
                    neg_p = neg_pony if m['name'] == "PonyV6" else neg_sdxl
                    img_data, _ = client.text_to_image(prompt, neg_p, checkpoint=m['file'], width=832, height=1216)
                
                with open(save_path, "wb") as f:
                    f.write(img_data)
                
                row += f"[查看](file://{save_path}) | "
            except Exception as e:
                print(f"[{m['name']}] 失败: {e}")
                row += "失败 | "
        report_md += row + "\n"
    
    with open(os.path.join(target_dir, "master_comparison_report.md"), "w", encoding="utf-8") as f:
        f.write(report_md)
    print("横评报告已重新生成并修正解剖学描述。")

if __name__ == "__main__":
    run_comparison()
