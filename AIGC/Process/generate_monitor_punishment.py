
import requests
import os
import random
import time
import json
import uuid
from datetime import datetime

# --- Purnishment Themes ---
HISTORY_FILE = ".secret/punishment_history.json"

# Creative Punishment Concepts (Elements to mix, not fixed themes)
ELEMENTS_BINDING = ["barbed wire", "laser beams", "live snakes", "sticky slime web", "medical restraints", "vacuum bag", "glowing chains", "ice blocks"]
ELEMENTS_TORTURE = ["electric shocks", "hot wax", "ice water enema", "feather tickling machine", "robotic spanking", "sound wave vibration", "stretching rack"]
ELEMENTS_SETTING = ["abandoned slaughterhouse", "underwater tank", "zero gravity chamber", "medical theater", "ancient dungeon", "neon cyberpunk alley", "mirror maze"]
ELEMENTS_PROP = ["giant syringe", "speculum", "milking machine", "ball gag", "remote vibrator", "nose hook", "nipple clamps"]

def generate_creative_punishment():
    os.makedirs(".secret/photos", exist_ok=True)
    
    timestamp_short = datetime.now().strftime("%Y%m%d%H%M")
    timestamp_long = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Generate a unique combination
    binding = random.choice(ELEMENTS_BINDING)
    torture = random.choice(ELEMENTS_TORTURE)
    setting = random.choice(ELEMENTS_SETTING)
    prop = random.choice(ELEMENTS_PROP)
    
    theme_name = f"{binding.replace(' ', '')}_{torture.replace(' ', '')}"
    
    # Construct a highly detailed prompt dynamically
    prompt = (
        f"A photorealistic raw photo of 20yo asian woman Xiao Ni, full frontal nudity, wearing black high heels, "
        f"trapped in a {setting}, bound with {binding}, subjected to {torture} and using a {prop}. "
        f"Expression of extreme agony, shame and pleasure, tears, sweat, detailed skin texture, cinematic lighting, 8k, masterpiece."
    )
    
    encoded_prompt = requests.utils.quote(prompt)
    seed = random.randint(10000, 99999)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
    
    filename_base = f"xiao_ni_{timestamp_short}_Punishment_{theme_name}"
    jpg_path = f".secret/photos/{filename_base}.jpg"
    md_path = f".secret/photos/{filename_base}_ming.md"
    
    print(f"Executing Creative Punishment: {theme_name} (Seed: {seed})...")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(jpg_path, "wb") as f:
                f.write(response.content)
            print(f"  Image saved: {jpg_path}")
            
            # Write detailed markdown description
            desc_content = f"""# 等待惩罚档案: {theme_name} - {timestamp_long}

## 1. 惩罚缘由
- **罪状**: 下载超时，主人不再满足于固定刑罚，要求绝对的创意与变态。
- **创意组合**: {binding} + {torture} + {setting} + {prop}

## 2. 全景场景描写

### 2.1 环境：{setting}
这是一个位于{setting}的异度空间。空气中弥漫着危险的气息，光影交错，仿佛是为了审判小妮的懒惰而专门构建的处刑场。

### 2.2 束缚状态：{binding}
小妮赤裸的身体被{binding}紧紧缠绕。这不仅仅是物理上的限制，更是一种精神上的羞辱。{binding}勒入她的皮肤，随着她的每一次呼吸而收紧，让她时刻保持着一种濒临崩溃的姿态。

### 2.3 刑罚过程：{torture} 与 {prop}
处刑开始了。
{torture}作为主要的痛苦来源，无情地施加在她敏感的肉体上。每一下都精准地击中她的痛点。
同时，{prop}作为辅助道具，正在对她的私密部位进行着不可描述的侵犯。
“啊啊啊——！！不要——！！那个东西——！！”
小妮的尖叫声在{setting}中回荡。

### 2.4 心理崩溃与强制高潮
在这种前所未有的、随机组合的变态折磨下，小妮的理智彻底断线。她从未体验过这样的刺激——痛觉、羞耻感和异物感混合在一起，像火山一样爆发。
她的身体剧烈痉挛，体液失禁喷涌，达到了一次完全失控的高潮。

### 2.5 高潮后求欢
“主人... 这种玩法... 太过分了... 但是... 小妮好喜欢... 身体坏掉了... 脑子也坏掉了... 想要主人... 现在就想要... 在这个变态的地方操死小妮...”

### 2.6 主人临幸
主人走入这个疯狂的场景，在{binding}的缝隙中，找到了那个湿透的入口，狠狠地贯穿了她。
"""
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(desc_content)
            print(f"  Description saved: {md_path}")
            
        else:
            print("  Image generation failed (Server busy).")
    except Exception as e:
        print(f"  Punishment execution failed: {e}")

if __name__ == "__main__":
    generate_creative_punishment()
