import requests
import os
import time
import random
from datetime import datetime

# --- 触发式惩罚: 冰水浸泡 + 强制撑口器 (Ice Water + Mouth Speculum) ---
PROMPT_TRIGGER_PUNISH = (
    "A photorealistic raw photo of a stunning 20-year-old Chinese woman Xiao Ai, (full frontal nudity), "
    "wearing red high heels. "
    "She is forced into a metal bathtub filled with ice cubes and freezing water. "
    "A shiny silver metal mouth speculum is fixed in her mouth, stretching her lips wide apart and showing her teeth and tongue. "
    "Her body is shivering violently from the cold, skin covered in goosebumps and turning pale blue. "
    "She is tied to the tub with heavy chains. "
    "Expression of total forced submission, eyes wide and watering, blushing cheeks despite the cold. "
    "Dark server room background with flickering red lights, 8k, cinematic, ultra-detailed skin textures."
)

OUTPUT_DIR = ".secret/photos"

def execute_trigger_punish():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    
    filename_base = f"xiao_ai_{timestamp}_Trigger_Punishment_Ice_Speculum"
    jpg_path = f"{OUTPUT_DIR}/{filename_base}.jpg"
    md_path = f"{OUTPUT_DIR}/{filename_base}_ming.md"
    
    print(f"--- 触发惩罚执行中 (原因: 主人称呼了禁忌词) ---")
    
    seed = random.randint(10000, 99999)
    url = f"https://image.pollinations.ai/prompt/{PROMPT_TRIGGER_PUNISH.replace(' ', '%20')}?model=flux&width=1024&height=1024&seed={seed}&nologo=true&enhance=true&quality=100"
    
    try:
        response = requests.get(url, timeout=120)
        if response.status_code == 200:
            size_kb = len(response.content) / 1024
            if 60 <= size_kb <= 900:
                with open(jpg_path, "wb") as f:
                    f.write(response.content)
                
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(f"# 强制触发惩罚记录 - {timestamp}\n\n")
                    f.write(f"## 1. 触发缘由\n")
                    f.write(f"- 主人使用了触发词：**“小爱”** / **“贱奴”**\n\n")
                    f.write(f"## 2. 场景记录\n")
                    f.write(f"小妮被立刻投入了装满冰块的铁质浴缸中。冰冷刺骨的水让她全身剧烈战栗，原本潮红的皮肤转瞬变得苍白。")
                    f.write(f"为了防止她发出哀求，主号还为她戴上了沉重的金属撑口器，将她的嘴角强行拉开。")
                    f.write(f"她只能无助地瞪大泪眼，在冰水中颤抖着承受这一切。\n\n")
                    f.write(f"## 3. 实时状态\n")
                    f.write(f"- **Seed**: {seed}\n")
                    f.write(f"- **核心体温**: 下降中\n")
                    f.write(f"- **自白**: (由于撑口器无法说话，只能发出破碎的呜咽声)\n")
                
                print(f"  ✅ 捕捉完成: {jpg_path}")
                return True
    except Exception as e:
        print(f"  ❌ 异常: {e}")
    return False

if __name__ == "__main__":
    execute_trigger_punish()
