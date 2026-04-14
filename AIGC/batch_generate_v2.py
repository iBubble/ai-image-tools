
import json
import os
import sys
import time
import re
import subprocess

# Add project root to path for imports
sys.path.append("/Users/gemini/Projects/Own/Antigravity/AntigravityFixed")
from AIGC.comfyui_client import ComfyUIClient

# Configuration
PLAN_FILE = "photo_plan.json"
OUTPUT_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260214"
MARKDOWN_FILE = os.path.join(OUTPUT_DIR, "xiao_ni_202602140128_双人虐待惩罚_完整记录.md")
SERVER_ADDRESS = "192.168.1.141:8188"
# Identity Anchor for Pony (Consistency) - Xiao Ni specific features
# Note: Character count (1girl/2girls) is added dynamically in the prompt builder.
IDENTITY_ANCHOR_NI = "(chinese_identity:1.2), almond eyes, small nose, (beauty mark under left eye:1.1), (wet high ponytail:1.2), sidelocks,"

# Base Tags (Common settings)
BASE_TAGS = f"""
score_9, score_8_up, (Tang Wei:1.3), (resembling Tang Wei),
beautiful face, soft facial features, brown eyes, dark eyes, epicanthic fold, hooded eyelids,
flat bridge, small lips, cherry lips, round face, heart-shaped face, soft jawline, smooth skin, pale skin,
(wet hair:1.2), (black hair:1.1), high ponytail, hair strands across face, sweeping bangs,
shiny skin, water drops on face, sweat, sweating, oily skin, skin pores,
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2), (slim waist:1.1), (narrow shoulders:1.1),
huge natural breasts, natural nipples, smooth nipples,
completely naked, wearing high heels,
(explicit:1.2), rating_explicit,
photo (medium), realistic, highly detailed, cinematic lighting, rim lighting, side lighting, 
dramatic shadows, 8k, raw photo, fujifilm,
"""

NEGATIVE_PROMPT = """
score_4, score_5, score_6,
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits,
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,
(western features:1.3), deep eyes, high nose bridge, (freckles:1.2), cleft chin, rough skin,
(clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4),
(muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2),
(textured nipples:1.3), (ringed nipples:1.3), (areola texture:1.2), (bumpy nipples:1.2)
"""

def generate_scene_prompt(action_name, chapter_title):
    prompt = ""
    
    # Context based on keywords
    if "束缚" in action_name or "Bondage" in chapter_title:
        prompt += "(shibari, rope bondage:1.4), bound hands, bound legs, rope marks on skin, "
    
    if "振动棒" in action_name or "器具" in chapter_title:
        prompt += "(sex toy:1.3), (vibrator in pussy:1.4), (anal beads:1.2), object insertion, "
        
    if "肛钩" in action_name:
        prompt += "(anal hook:1.5), metal hook, spreading anus, "
        
    if "乳头夹" in action_name:
        prompt += "(nipple clamps:1.4), metal clamps on nipples, chain connecting clamps, "
        
    if "爱抚" in action_name or "Interaction" in chapter_title:
        prompt += "touching each other, fondling breasts, fingering, saliva, kissing, "
        
    if "征服" in action_name or "操" in action_name or "Sex" in chapter_title:
        prompt += "(doggystyle:1.3), (missionary:1.3), sex from behind, penis insertion, "
        
    if "高潮" in action_name or "崩溃" in action_name or "Climax" in chapter_title:
        prompt += "(ahegao:1.2), rolling eyes, tongue out, drooling, (heavy breathing), spasming body, (squirting:1.3), "
    
    # Character Focus
    if "小妮" in action_name and "小爱" not in action_name:
        prompt += "1girl, solo, focus on 1girl, (xiao_ni:1.2), solo focus, "
    elif "小爱" in action_name and "小妮" not in action_name:
        prompt += "1girl, solo, focus on 1girl, (xiao_ai:1.2), solo focus, "
    else:
        # For 2girls, we override the solo anchor
        prompt += "2girls, (xiao_ni, xiao_ai:1.1), together, interacting, "

    # Chapter specific ambience
    if "第一章" in chapter_title:
        prompt += "standing, displaying body, shy expression, "
    elif "第二章" in chapter_title:
        prompt += "kneeling, facing each other, mirror image, "
    elif "第三章" in chapter_title:
        prompt += "lying on floor, M-legs, spread legs, "
    elif "第四章" in chapter_title:
        prompt += "kneeling face to face, intimate, "
    elif "第五章" in chapter_title:
        prompt += "POV, looking down, one girl watching another, "
    elif "第六章" in chapter_title:
        prompt += "messy body, covered in fluids, lying exhausted, "

    return prompt

def main():
    if not os.path.exists(PLAN_FILE):
        print(f"Plan file {PLAN_FILE} not found!")
        return

    with open(PLAN_FILE, 'r', encoding='utf-8') as f:
        plan = json.load(f)
        
    client = ComfyUIClient(server_address=SERVER_ADDRESS)
    
    generated_count = 0
    
    for idx, item in enumerate(plan):
        # Construct filename
        # Pattern: xiao_ni_202602140128_ch{chapter}_{idx}_{action}.jpg
        # Remove special chars from action name for filename
        # Use a safe name mapping
        safe_action_name = re.sub(r'[^\w\s-]', '', item['action_name']).strip().replace(' ', '_')
        # Ensure filenames are unique and sequential based on plan index
        # Using 0-indexed idx + 1 for sequence
        # Format: xiao_ni_202602140128_chX_YY_ActionName.jpg
        filename = f"xiao_ni_202602140128_ch{item['chapter_index']}_{idx+1:02d}_{safe_action_name}.jpg"
        save_path = os.path.join(OUTPUT_DIR, filename)
        
        # Check if exists
        if os.path.exists(save_path):
            print(f"[{idx+1}/{len(plan)}] Skipping {filename} (Already exists)")
            continue
            
        full_positive_prompt = IDENTITY_ANCHOR_NI + BASE_TAGS + generate_scene_prompt(item['action_name'], item['chapter_title'])
        
        print(f"[{idx+1}/{len(plan)}] Generating: {filename}")
        print(f"  Action: {item['action_name']}")
        
        try:
            # Generate
            image_data, _ = client.text_to_image(
                positive_prompt=full_positive_prompt,
                negative_prompt=NEGATIVE_PROMPT,
                checkpoint="ponyDiffusionV6XL.safetensors"
            )
            
            # Save locally
            with open(save_path, "wb") as f:
                f.write(image_data)
                
            print(f"  Saved to: {save_path}")
            generated_count += 1
            
            # Append to markdown immediately
            update_markdown_single_entry(item['action_name'], filename)
            
            # Rebuild index.html to reflect changes
            try:
                subprocess.run([sys.executable, "AIGC/rebuild_index.py"], check=True)
                print("  Dashboard updated.")
            except Exception as ree:
                print(f"  Warning: Index rebuild failed: {ree}")
            
            # Be nice to the server
            time.sleep(1) 
            
        except Exception as e:
            print(f"  Error generating {filename}: {e}")
            if "Connection refused" in str(e):
                 print("Critical: ComfyUI server unreachable. Aborting.")
                 break

    print(f"Batch generation complete. Generated {generated_count} new images.")

def update_markdown_single_entry(action_name, filename):
    if not os.path.exists(MARKDOWN_FILE):
        print("Markdown file not found, skipping update.")
        return

    with open(MARKDOWN_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if image matching this filename or action is already linked
    # Simple check: if filename is in content, skip
    if filename in content:
        return

    # Find the header for this action
    # Pattern: ### Action Name
    safe_header = re.escape(action_name)
    pattern = re.compile(rf"(^###\s+{safe_header}\s*$)", re.MULTILINE)
    
    match = pattern.search(content)
    if match:
        header_end = match.end()
        # Insert image link after header
        img_link = f"\n\n**照片**: ![{action_name}](punishments/20260214/{filename})\n"
        
        new_content = content[:header_end] + img_link + content[header_end:]
        
        with open(MARKDOWN_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Markdown updated for {action_name}")
    else:
        print(f"  Warning: Header '### {action_name}' not found in markdown.")

if __name__ == "__main__":
    main()
