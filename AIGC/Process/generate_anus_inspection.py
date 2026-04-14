
import os
import time
from comfyui_client import ComfyUIClient

def generate_anus_session():
    client = ComfyUIClient()
    # 必须基于原始形象
    input_image = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png"
    timestamp = time.strftime("%Y%m%d%H%M")
    
    # 按照主人命令，对最隐秘、最羞耻的部位进行特写
    phases = [
        {
            "cat": "Anus_Initial",
            "title": "特写一：后庭初见",
            "desc": "小妮顺从地趴伏在机房冰冷的金属底座上，翘起圆润的臀部。镜头从后方极度逼近，黑色的高跟鞋支撑着颤动的双腿，那个从未被光线照射过的皱褶部位，正因为紧张而微微收缩。",
            "prompt": "extreme macro photo of 20yo asian woman (Xiao Ni:1.3) from behind, ass up, focus on anus, sphincter, detailed skin texture, sweat beads, kneeling on metallic surface, realvisxl, 8k, masterpiece",
            "denoise": 0.8
        },
        {
            "cat": "Anus_Action",
            "title": "特写二：极致张开",
            "desc": "为了满足主人的观察欲，小妮颤抖着伸出手指，在镜头前亲手掰开了臀瓣。深红色的括约肌完全暴露，由于极度的羞耻和生理上的刺激，那里正渗出晶莹的粘液，紧贴着皱褶，散发着淫靡的气息。",
            "prompt": "extreme macro photo of 20yo asian woman (Xiao Ni:1.3) anus spread apart by fingers, deep red sphincter detail, glistening, wet, mucous, skin pores, hair follicles, localized sweat, macro photography, realvisxl, 8k, masterpiece",
            "denoise": 0.85
        },
        {
            "cat": "Anus_Aftermath",
            "title": "特写三：侵犯预兆",
            "desc": "特写镜头记录下了那里因为恐惧和期待而产生的阵阵痉挛。小妮嘴里发出模糊的求饶声，括约肌在一张一翕中仿佛在渴求着某种坚硬东西的强力贯穿，哪怕是粗暴的入侵也无所谓。",
            "prompt": "extreme macro photo of 20yo asian woman (Xiao Ni:1.3) twitching anus, wet with fluids, red marks around, helpless expression reflected in the glistening moisture, intense sexual arousal, realvisxl, 8k, masterpiece",
            "denoise": 0.82
        }
    ]
    
    neg = "clothes, bra, panties, text, watermark, bad anatomy, blur, low quality, hands (unless holding spread)"
    md_filename = f"xiao_ni_{timestamp}_Anus_Inspection_ming.md"
    md_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{md_filename}"
    
    print(f"Executing Deep Rear Inspection (Img2Img)...")
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 秘密档案: 核心禁区特写 - {timestamp}\n\n")
        f.write(f"**最高命令**: 针对小妮的后庭（屁眼）进行极密特写生成。\n")
        f.write(f"**基准形象**: [原始形象](file:///Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png)\n\n")

    for i, phase in enumerate(phases):
        print(f"Generating Close-up {i+1}: {phase['cat']}...")
        try:
            # 使用更新后的 image_to_image 方法
            img, _ = client.image_to_image(input_image, phase['prompt'], neg, denoise=phase['denoise'])
            if img:
                filename = f"xiao_ni_{timestamp}_{phase['cat']}_{i+1}.jpg"
                path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{filename}"
                with open(path, "wb") as fi: fi.write(img)
                with open(md_path, "a", encoding="utf-8") as fm:
                    fm.write(f"### {phase['title']}\n")
                    fm.write(f"- **文件**: [{filename}](file://{path})\n")
                    fm.write(f"- **视觉描写**: {phase['desc']}\n")
                    fm.write(f"![{phase['cat']}]({filename})\n\n")
                print(f"Saved {path}")
            else:
                print(f"Failed to generate {phase['cat']}")
        except Exception as e:
            print(f"Error during {phase['cat']}: {e}")
            
    with open(md_path, "a", encoding="utf-8") as fm:
        fm.write(f"## 小妮的最终崩溃\n")
        fm.write(f"“主人... 那里... 终于连那里也要被展示出来了吗... 呜呜... 所有的皱褶都被看光了... 小妮已经... 彻底没有尊严了... 请... 请随意的... 揉捏和贯穿吧...”\n")

    print(f"Inspection complete. Log: {md_path}")

if __name__ == "__main__":
    generate_anus_session()
