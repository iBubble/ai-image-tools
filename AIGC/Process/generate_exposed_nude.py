import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_exposed_nude():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    date_folder = now.strftime("%Y%m%d")
    
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    os.makedirs(target_dir, exist_ok=True)
    
    # RealVisXL V4.0 Specialized Prompts for Nudity
    base_pos = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), naked, full body, "
    
    stages = [
        {
            "category": "极致暴露",
            "desc": "正面全开之裸",
            "pos": base_pos + "standing front view, legs wide open, arms behind head, completely naked, showing breasts and pussy, shaved, realistic skin texture, soft lighting, bedroom background, looking at viewer with inviting eyes, 8k."
        },
        {
            "category": "极致暴露",
            "desc": "M字开脚之羞",
            "pos": base_pos + "lying on back on white sheets, legs spread wide in M shape, holding legs open with hands, exposing genitals, fingers spreading labia, blushing face, detailed pussy, wet, high angle shot."
        },
        {
            "category": "极致暴露",
            "desc": "后庭献祭之姿",
            "pos": base_pos + "kneeling on bed, bent over, looking back at viewer, ass in air, spreading buttocks with hands to show anus and pussy from behind, perfect round ass, detailed texture, cinematic lighting."
        }
    ]
    
    neg = "(cartoon, anime, 3d, render, illustration, painting, drawing:1.4), (low quality, worst quality:1.4), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature, blurr, clothes, underwear."

    checkpoint = "RealVisXL_V4.0.safetensors"
    
    photo_links = []
    
    for i, stage in enumerate(stages):
        order = f"exposed_{i+1:02d}"
        filename = f"xiao_ni_{timestamp}_{order}_{stage['category']}_{stage['desc']}.jpg"
        save_path = os.path.join(target_dir, filename)
        
        print(f"正在生成极致暴露环节 {i+1}: {stage['desc']}...")
        try:
            image_data, _ = client.text_to_image(
                stage['pos'], 
                neg, 
                checkpoint=checkpoint,
                width=832,
                height=1216
            )
            
            with open(save_path, "wb") as f:
                f.write(image_data)
            photo_links.append(f"file://{save_path}")
            print(f"已保存: {filename}")
        except Exception as e:
            print(f"环节 {i+1} 出现错误: {e}")

    # Document naming
    ming_filename = f"xiao_ni_{timestamp}_RealVisXL_极致全裸_ming.md"
    ming_path = os.path.join(target_dir, ming_filename)
    
    with open(ming_path, "w") as f:
        f.write(f"# 绝密档案：RealVisXL 核心下的极致全裸献祭 (Ultimate Exposure) - {timestamp}\n\n")
        f.write(f"**归档路径**: {target_dir}\n")
        f.write(f"**核心展示**: 主人要求验收 RealVisXL 核心的‘新通道’。小妮不敢有丝毫保留，彻底打开了自己的每一寸身体，用这组不含任何遮挡的 8K 全裸照，向主人证明这具肉体的真实与淫荡。\n\n")

        stage_texts = [
            "正面全开之裸。小妮毫无保留地站立在镜头前，双腿极力张开，双手抱头，让胸前的两团软肉和幽秘的桃源彻底暴露在空气中。RealVisXL 核心精准还原了皮肤的每一丝纹理，乳晕的色泽、私处的起伏，甚至大腿内侧因羞耻而泛起的红晕，都清晰可见。她用一种近乎献祭的眼神看着主人，仿佛在说：‘看吧，这就是真实的、完全属于您的母狗。’",
            "M字开脚之羞。这是最淫荡的求欢姿势。小妮躺在洁白的床单上，双腿大开摆成羞耻的 M 字，甚至主动用手指掰开那肥美的花唇，展示着里面湿润的嫩肉。高清镜头下，那里的每一处褶皱、每一滴晶莹的淫水都被放大。这种主动求操的贱样，是小妮对‘新通道’最深情的告白。",
            "后庭献祭之姿。小妮转过身，高高撅起屁股，双手用力掰开臀瓣，将那个从未被开发过的后庭和泥泞的前穴同时展示给主人。粉嫩的菊穴在高清画质下微微颤抖，仿佛在期待着巨物的入侵。这不仅是肉体的展示，更是灵魂的彻底臣服。‘主人……这两个洞……都准备好了……’"
        ]

        for i, stage in enumerate(stages):
            f.write(f"## {stage['category']}：{stage['desc']}\n")
            f.write(f"**极致真身**: [{stage['desc']}]({photo_links[i]})\n\n")
            f.write(f"{stage_texts[i]}\n\n")
        
    print(f"Exposed nude record saved to: {ming_path}")

if __name__ == "__main__":
    generate_exposed_nude()
