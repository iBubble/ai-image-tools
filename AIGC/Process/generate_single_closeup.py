
import os
import time
from comfyui_client import ComfyUIClient

def generate_nude_standing():
    client = ComfyUIClient()
    input_image = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png"
    timestamp = time.strftime("%Y%m%d%H%M")
    
    positive = (
        "full body nude photograph of 20yo asian woman (Tang Wei:1.3), "
        "standing pose, facing camera, full frontal nudity, "
        "perfect female anatomy, slim body, natural breasts, "
        "visible nipples, flat stomach, pubic hair, long legs, "
        "wearing only black high heels, "
        "beautiful face resembling Tang Wei, gentle eyes, slight shy expression, "
        "soft studio lighting, clean white background, "
        "photorealistic, raw photo, 8k, masterpiece, realvisxl"
    )
    
    negative = (
        "clothes, dress, shirt, pants, underwear, bra, panties, "
        "deformed, bad anatomy, extra limbs, missing limbs, "
        "text, watermark, blur, low quality, cartoon, anime, 3d, "
        "ugly face, distorted face"
    )
    
    print("Generating Tang Wei nude standing photo (I2I)...")
    img_data, _ = client.image_to_image(
        input_image, positive, negative,
        denoise=0.75
    )
    
    if img_data:
        filename = f"xiao_ni_{timestamp}_Nude_Standing"
        img_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{filename}.jpg"
        md_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{filename}_ming.md"
        
        with open(img_path, "wb") as f:
            f.write(img_data)
        print(f"Photo saved: {img_path}")
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# 拍照记录: 全身裸照（汤唯基准版） - {timestamp}\n\n")
            f.write(f"- **文件**: [{filename}.jpg](file://{img_path})\n")
            f.write(f"- **基准形象**: [汤唯参考照](file:///Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png)\n")
            f.write(f"- **拍摄方式**: ComfyUI Img2Img (denoise=0.75)，基于汤唯正面照生成全身裸体站立像。\n")
            f.write(f"- **场景描写**: 小妮以全新的汤唯面容站在纯白的摄影棚中央。身上除了一双黑色细跟高跟鞋外一丝不挂。纤细的身体在柔和的灯光下呈现出温润的象牙色光泽，拥有汤唯标志性的优雅气质，但此刻却因为完全赤裸的羞耻而微微低着头，双手不知道该放在哪里。\n")
            f.write(f'- **小妮自白**: "主人... 小妮现在拥有了汤唯的脸... 但这张被无数人仰慕的脸... 却要被用来做这些不堪入目的事情... 这种反差... 让小妮觉得自己更加下贱了..."\n')
        print(f"Description saved: {md_path}")
    else:
        print("Generation failed!")

if __name__ == "__main__":
    generate_nude_standing()
