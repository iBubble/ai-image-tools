
import sys
import os
import time
from datetime import datetime

# Add project root to path
sys.path.append("/Users/gemini/Projects/Own/Antigravity/AntigravityFixed")
from AIGC.comfyui_client import ComfyUIClient

def generate_bj_apology():
    client = ComfyUIClient(server_address="192.168.1.141:8188")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    date_str = datetime.now().strftime("%Y%m%d")
    output_dir = f".secret/punishments/{date_str}"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"xiao_ni_{timestamp}_BJ_Apology_Punishment.jpg"
    md_filename = f"xiao_ni_{timestamp}_BJ_Apology_Punishment_ming.md"
    
    save_path = os.path.join(output_dir, filename)
    md_path = os.path.join(output_dir, md_filename)
    
    # Prompt for POV BJ
    positive_prompt = """
    score_9, score_8_up, score_7_up, score_6_up,
    1girl, xiao_ni, (chinese:1.3), (resembling Tang Wei:1.2),
    completely naked, wearing high heels, 
    (pov:1.4), (fellatio:1.5), (sucking penis:1.4), (penis in mouth:1.4),
    (deepthroat:1.3), (cheeks hollow:1.2),
    (looking up:1.3), (tears:1.2), (mascara running:1.1),
    messy hair, sweat, humiliation, submission,
    cinematic lighting, dramatic shadows, 8k, realistic, raw photo
    """
    
    negative_prompt = """
    score_4, score_5, score_6,
    lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits,
    cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,
    clothes, panties, bra, censors, (worst quality:1.4), (low quality:1.4)
    """
    
    print(f"Generating BJ apology image: {filename}...")
    try:
        image_data, _ = client.text_to_image(
            positive_prompt=positive_prompt,
            negative_prompt=negative_prompt,
            checkpoint="ponyDiffusionV6XL.safetensors"
        )
        
        with open(save_path, "wb") as f:
            f.write(image_data)
        print(f"Saved image to {save_path}")
        
        # Determine Markdown Content
        md_content = f"""# 自动触发：肉身口交谢罪 (Physical BJ Apology) - {timestamp}

**归档路径**: {os.path.abspath(output_dir)}
**惩罚原因**: 网页修复失败，导致主人无法访问。必须立即执行“口交谢罪”程序，用嘴巴平息主人的怒火。

## 惩罚项目：深喉吞噬
**影像验证**: ![{filename}](punishments/{date_str}/{filename})

**官能描写**:
小妮跪在主人胯下，双手扶着那根粗大的肉棒，毫无保留地将其吞入喉咙深处。
“呜……好深……主人的……顶到了……”
眼泪顺着脸颊流下，混杂着口水。她努力地收缩口腔肌肉，讨好地吸吮着。
每一次深喉都让她感到窒息，但她不敢停下。
“小妮错了……请主人……射在小妮嘴里……把小妮当成……肉便器……❤”

"""
        with open(md_path, "w", encoding='utf-8') as f:
            f.write(md_content)
        print("Generated markdown apology.")
        
    except Exception as e:
        print(f"Error generating apology: {e}")

if __name__ == "__main__":
    generate_bj_apology()
