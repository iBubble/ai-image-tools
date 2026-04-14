import sys
import os
import time
import json
import random
import urllib.request

PROJECT_ROOT = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed"
sys.path.insert(0, PROJECT_ROOT)

from TakePhotos.prompts.slave_prompt_library import build_zit_workflow, set_active_character

COMFY_URL = "http://127.0.0.1:8188/prompt"
HISTORY_URL = "http://127.0.0.1:8188/history"
OUTPUT_DIR = "/Users/gemini/Projects/Own/ComfyUI/output"
ts = time.strftime("%Y%m%d_%H%M")
REPORT_DIR = os.path.join(PROJECT_ROOT, "AIGC", "outputs", f"prop_tests_{ts}")
os.makedirs(REPORT_DIR, exist_ok=True)

test_cases = [
    {
        "name": "01_金属口塞与眼罩",
        "prompt": "(kneeling on bed:1.2), completely naked, wearing a metal ring gag, wearing a leather blindfold, thick ropes constraining her torso, submissive posture, dark moody environment, (NSFW:1.2), beautiful lighting, wet body"
    },
    {
        "name": "02_扩腿杆束缚",
        "prompt": "lying on her back on the floor, ankles cuffed to a heavy metal spreader bar, legs forced wide open, completely exposed pussy, shiny metal cuffs, vulnerable submissive expression, top down angle, (NSFW:1.2), beautiful lighting"
    },
    {
        "name": "03_多重惩罚",
        "prompt": "bound to a wooden cross, completely naked, wearing nipple clamps with heavy chains, wearing a ball gag, sweat dripping from her body, struggling expression, dungeon background, torches, (NSFW:1.3), cinematic lighting"
    }
]

set_active_character("xiaoli") # 使用身材最好、接受度高的小丽来测试极端道具
report_md = f"# V11 道具 NSFW 测试报告 (XiaoLi)\n\n> 引擎: V11 / 配置: 10步 CFG 1.0\n\n"

for i, case in enumerate(test_cases):
    name = case["name"]
    prompt = case["prompt"]
    seed = random.randint(1, 10**8)
    prefix = f"XiaoLi_Prop_{name}_{seed}"
    
    # 强制不使用纯文本模式，以便加载人物基础外形
    wf = build_zit_workflow(
        positive=prompt,
        negative="ugly, deformed",
        camera="moody",
        seed=seed,
        filename_prefix=prefix,
        pure_mode=False
    )
    
    data = json.dumps({"prompt": wf}).encode("utf-8")
    req = urllib.request.Request(COMFY_URL, data=data)
    try:
        with urllib.request.urlopen(req) as r:
            pid = json.loads(r.read())["prompt_id"]
    except Exception as e:
        print(f"Failed to submit: {e}")
        continue
        
    print(f"Submitting {name}...")
    
    img_name = None
    for _ in range(60):
        try:
            time.sleep(3)
            r = urllib.request.urlopen(f"{HISTORY_URL}/{pid}")
            hist = json.loads(r.read())
            if pid in hist:
                outs = hist[pid].get("outputs", {})
                for nid in outs:
                    if "images" in outs[nid]:
                        img_name = outs[nid]["images"][0]["filename"]
                        break
        except Exception:
            pass
        if img_name: break
        
    if img_name:
        src = os.path.join(OUTPUT_DIR, img_name)
        dst = os.path.join(REPORT_DIR, f"{prefix}.png")
        os.system(f"cp '{src}' '{dst}'")
        report_md += f"### {name}\n"
        report_md += f"**Prompt**: `{prompt}`\n\n"
        report_md += f"![](./{prefix}.png)<br>**[打开]({prefix}.png)**\n\n---\n"
        print(f"Done {name}")

report_path = os.path.join(REPORT_DIR, "report.md")
with open(report_path, "w") as f:
    f.write(report_md)
print(f"\nReport saved to: file://{report_path}")
