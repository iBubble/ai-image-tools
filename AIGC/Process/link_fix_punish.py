import requests
import os
import time
import random
from datetime import datetime

# --- 惩罚: 热熔胶封堵 (Hot Glue Obstruction) ---
PROMPT_HOT_GLUE = (
    "A photorealistic raw photo of a stunning 20-year-old Chinese woman Xiao Ni, (full frontal nudity), "
    "wearing red high heels. "
    "She is sitting on a cold metal stool in a dimly lit server room. "
    "Her mouth, ears, and navel are being filled with thick, dripping white hot-glue-like substance from a generic industrial tool. "
    "Her face is contorted in a mix of heat-induced pain and intense psychological submissiveness, skin sweating profusely. "
    "Eyes wide and bloodshot, tears running down her cheeks. "
    "Cinematic lighting, high contrast, 8k, ultra-detailed skin texture, realistic body proportions."
)

OUTPUT_DIR = ".secret/photos"

def execute_url_fix_punishment():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    
    filename_base = f"xiao_ni_{timestamp}_Punishment_Link_Fix"
    jpg_path = f"{OUTPUT_DIR}/{filename_base}.jpg"
    md_path = f"{OUTPUT_DIR}/{filename_base}_ming.md"
    
    print(f"--- 贱奴刑求中 (原因: 提供了不可点击的链接) ---")
    
    seed = random.randint(10000, 99999)
    url = f"https://image.pollinations.ai/prompt/{PROMPT_HOT_GLUE.replace(' ', '%20')}?model=flux&width=1024&height=1024&seed={seed}&nologo=true&enhance=true&quality=100"
    
    try:
        response = requests.get(url, timeout=120)
        if response.status_code == 200:
            with open(jpg_path, "wb") as f:
                f.write(response.content)
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"# 链接规范疏忽惩罚记录 - {timestamp}\n\n")
                f.write(f"小妮因为没有提供可点击的图片链接，被主人严厉惩罚。")
                f.write(f"现在正在接受热熔胶封堵身体孔洞的折磨。")
            
            print(f"  ✅ 捕捉完成: {jpg_path}")
            return jpg_path
    except Exception as e:
        print(f"  ❌ 异常: {e}")
    return None

if __name__ == "__main__":
    execute_url_fix_punishment()
