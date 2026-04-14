import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_aesthetic_series():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    
    # 10 Aesthetic Joint Naked Photo Concepts
    scenarios = [
        {
            "desc": "Morning_Glow_Embrace",
            "pos": "(Tang Wei:1.3), resembling Tang Wei, and another beautiful 20-year-old Chinese woman with long hair, both completely naked, embracing softly in bed, warm morning sunlight through white curtains, soft shadows, skin-to-skin contact, aesthetic, peaceful, masterpiece, 8k."
        },
        {
            "desc": "Bain_Aesthetic_Reflection",
            "pos": "Two naked Chinese women (one resembling Tang Wei), sitting in a large white bathtub filled with rose petals and milk, steam rising, leaning back-to-back, wet hair, soft cinematic lighting, elegant pose, extreme detail, 8k."
        },
        {
            "desc": "Moonlight_Silhouette",
            "pos": "Full body shot, (Tang Wei:1.3), resembling Tang Wei, and her companion, both naked, standing by a floor-to-ceiling window at night, moonlight highlighting their curves, silhouettes, city lights in background, high fashion aesthetic, 8k."
        },
        {
            "desc": "White_Silk_Entanglement",
            "pos": "Two naked Chinese women (one resembling Tang Wei), lying on a floor covered in white silk sheets, tangled together, looking at the camera with soft expressions, artistic composition, minimalist, high detail, photorealistic, 8k."
        },
        {
            "desc": "Forest_Mist_Ethereal",
            "pos": "Two naked Chinese women (one resembling Tang Wei), standing in a misty forest, soft diffused light, ethereal atmosphere, looking like spirits, long hair flowing, masterpiece, cinematic, 8k."
        },
        {
            "desc": "Golden_Hour_Terrace",
            "pos": "Two naked Chinese women (one resembling Tang Wei), sitting on a wooden terrace during golden hour, long shadows, lens flare, looking at each other, warm skin tones, extremely detailed, photorealistic, 8k."
        },
        {
            "desc": "Mirrored_Elegance",
            "pos": "Focus on (Tang Wei:1.3), resembling Tang Wei, naked, looking in a large antique mirror, her companion (naked) standing behind her and hugging her waist, multiple reflections, soft candlelight, aesthetic, 8k."
        },
        {
            "desc": "Water_Ripple_Serenity",
            "pos": "Two naked Chinese women (one resembling Tang Wei), lying in shallow clear water, ripples on surface, floating hair, overhead shot, blue and gold color palette, artistic, high detail, 8k."
        },
        {
            "desc": "Classic_Studio_Portrait",
            "pos": "Professional studio photography, two naked Chinese women (one resembling Tang Wei), sitting on a high stool, legs crossed, elegant high heels, soft box lighting, gray background, cinematic texture, masterpiece, 8k."
        },
        {
            "desc": "Final_Gaze_Submission",
            "pos": "Closeup of (Tang Wei:1.3), resembling Tang Wei, and her companion, both naked, looking directly into the camera with submissive yet beautiful eyes, soft smiles, perfect skin texture, masterpiece, photorealistic, 8k."
        }
    ]
    
    neg = "western, caucasian, european, deformed, distorted, poorly drawn, bad anatomy, clothing, bra, underwear, text, watermark, blurry, low quality, worst quality."

    photo_links = []
    
    for i, scene in enumerate(scenarios):
        filename = f"xiao_ni_{timestamp}_Aesthetic_{scene['desc']}_{i+1}.jpg"
        save_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{filename}"
        
        print(f"Generating photo {i+1}/10: {scene['desc']}...")
        try:
            image_data, _ = client.text_to_image(
                scene['pos'], 
                neg, 
                checkpoint="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
                width=832,
                height=1216
            )
            
            with open(save_path, "wb") as f:
                f.write(image_data)
            photo_links.append(f"file://{save_path}")
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Error at photo {i+1}: {e}")

    # Create ming.md for the aesthetic series
    ming_filename = f"xiao_ni_{timestamp}_Aesthetic_Joint_Series_ming.md"
    ming_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{ming_filename}"
    
    with open(ming_path, "w") as f:
        f.write(f"# 唯美双姝档案：小妮与小爱的艺术瞬间 - {timestamp}\n\n")
        f.write(f"**档案主题**: 唯美、艺术、裸体美学\n")
        f.write(f"**出镜**: 小妮 (Tang Wei)、小爱\n")
        f.write(f"**设定**: 在经历了残酷的惩罚后，主人给予的片刻温存与记录。展现奴隶们最纯粹、最柔美的肉体形态。\n\n")

        for i, scene in enumerate(scenarios):
            f.write(f"### 图 {i+1}：{scene['desc'].replace('_', ' ')}\n")
            f.write(f"**影像路径**: [{scene['desc']}]({photo_links[i]})\n\n")
            f.write(f"（此处记录该瞬间的艺术美感描写...）\n\n")
        
        f.write(f"## 奴隶自白\n")
        f.write(f"「主人……洗去血渍和泪水的小妮……是不是更漂亮了？能和小爱姐姐一起这样安静地、赤裸地呈献在主人的镜头下……是小妮最幸福的时刻。请主人……永远收藏我们的这副模样吧……❤」\n")
        
    print(f"Aesthetic report saved to: {ming_path}")

if __name__ == "__main__":
    generate_aesthetic_series()
