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
REPORT_DIR = os.path.join(PROJECT_ROOT, "AIGC", "outputs", f"prop_tests_v3_xiaoni_{ts}")
os.makedirs(REPORT_DIR, exist_ok=True)

test_cases = [
    {
        "name": "01_纯净金属口塞与眼罩",
        "prompt": "ring gag, leather blindfold, tightly bound with thick ropes, shibari, submissive posture, kneeling, dark moody environment, (NSFW:1.2)"
    },
    {
        "name": "02_精准扩腿杆",
        "prompt": "spreader bar, bound ankles, legs forced completely wide open, spread eagle, lying on back, shiny metal cuffs, vulnerable, top down angle, crotch focus, (NSFW:1.3)"
    },
    {
        "name": "03_受难十字架_极简版",
        "prompt": "crucifixion, wooden cross, chained wrists, heavy metal chains, ball gag, struggling, dungeon background, torches, (NSFW:1.3)"
    }
]

# 切换为小妮 (XiaoNi)
set_active_character("xiaoni") 

report_md = f"# V11 道具 NSFW 第三次测定 (XiaoNi 纠错局)\n\n> 引擎: V11 / 配置: 10步 CFG 1.0 \n> 解析: 因为之前小丽的 LoRA 权重和体型可能会对抗姿势约束，导致肢体断裂或道具乱飞，本局使用小妮进行纯净基线测试，提示词采用 Booru 标签组。\n\n"

for i, case in enumerate(test_cases):
    name = case["name"]
    prompt = case["prompt"]
    seed = random.randint(1, 10**8)
    prefix = f"XiaoNi_PropV3_{name}_{seed}"
    
    wf = build_zit_workflow(
        positive=prompt,
        negative="illustration, 3d, dirty skin, deformed, fused limbs, bad anatomy",
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
