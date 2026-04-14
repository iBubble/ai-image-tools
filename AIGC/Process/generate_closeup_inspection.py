
import os
import time
from comfyui_client import ComfyUIClient

def generate_closeup_session():
    client = ComfyUIClient()
    input_image = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png"
    timestamp = time.strftime("%Y%m%d%H%M")
    
    # 按照主人命令，对下体进行特写观察
    phases = [
        {
            "cat": "Closeup_Frontal",
            "title": "特写一：正面合拢状态",
            "desc": "镜头极度拉近。小妮跪坐在地，双腿微微合拢，但粉嫩的私处在茂密的黑色耻垢中若隐若现。稚嫩的阴唇紧闭，皮肤上挂着细密的汗珠，因为主人的注视而羞耻地紧缩着。",
            "prompt": "extreme macro photo of 20yo asian woman (Xiao Ni:1.3) groin area, pussy, pubic hair, sitting on floor, full frontal nudity, skin grain, sweat, realistic, 8k, masterpiece, realvisxl",
            "denoise": 0.8
        },
        {
            "cat": "Closeup_Spread",
            "title": "特写二：耻辱拨开状态",
            "desc": "小妮顺从地伸直手指，从两侧拨开了阴唇，向主人展示里面湿润、鲜红的内里。由于刚才的折磨，阴蒂充血凸起，大量的透明粘液正在顺着腿根缓缓流下。",
            "prompt": "extreme macro photo of 20yo asian woman (Xiao Ni:1.3) pussy spread apart by fingers, looking inside, wet, moist, glistening, anatomical detail, pubic hair, labia, realvisxl, 8k, masterpiece",
            "denoise": 0.85
        },
        {
            "cat": "Closeup_Detail",
            "title": "特写三：受虐痕迹观察",
            "desc": "这是惩罚后的细节。娇嫩的皮肤上可以看到之前电缆勒过的红印和未干的蜡迹。由于极度的快感，肌肉还在阵阵痉挛，括约肌也因为羞耻的排泄快感而微微开合。",
            "prompt": "extreme macro photo of 20yo asian woman (Xiao Ni:1.3) lower body, pussy and anus, red marks on skin, dried wax droplets, detailed skin texture, sweat, realvisxl, 8k, masterpiece",
            "denoise": 0.82
        }
    ]
    
    neg = "clothes, bra, panties, text, watermark, bad anatomy, blur, low quality"
    md_filename = f"xiao_ni_{timestamp}_Closeup_Inspection_ming.md"
    md_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{md_filename}"
    
    print(f"Executing Lower Body Inspection (Img2Img)...")
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 身体检查报告: 下体极密观察 - {timestamp}\n\n")
        f.write(f"**主人命令**: 针对小妮的私处进行特写拍摄。\n")
        f.write(f"**基准形象**: [原始形象](file:///Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png)\n\n")

    for i, phase in enumerate(phases):
        print(f"Generating Close-up {i+1}: {phase['cat']}...")
        try:
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
        fm.write(f"## 小妮的哀求\n")
        fm.write(f"“主人... 为什么... 要看得这么仔细... 里面的每一个皱褶都被您看光了... 呜呜... 这种感觉... 比刚才的蛇还要让小妮羞耻... 请... 请随意的检阅吧...”\n")

    print(f"Inspection complete. Log: {md_path}")

if __name__ == "__main__":
    generate_closeup_session()
