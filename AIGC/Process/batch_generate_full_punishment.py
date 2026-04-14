
import json
import os
import sys
import time
import random
import re

# Add project root to path for imports
sys.path.append("/Users/gemini/Projects/Own/Antigravity/AntigravityFixed")
from AIGC.comfyui_client import ComfyUIClient

# Configuration
PLAN_FILE = "photo_plan.json"
MARKDOWN_FILE = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260214/xiao_ni_202602140128_双人虐待惩罚_完整记录.md"
OUTPUT_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260214"
SERVER_ADDRESS = "192.168.1.141:8188"

# Prompt Builders
BASE_PROMPT = """
score_9, score_8_up, score_7_up, score_6_up,
2girls, (xiao_ni, xiao_ai),
(chinese:1.3), (east asian:1.2),
beautiful face, soft facial features,
brown eyes, dark eyes, almond eyes, epicanthic fold, hooded eyelids,
small nose, flat bridge, small lips, cherry lips,
round face, heart-shaped face, soft jawline, smooth skin, pale skin,
(wet hair:1.2), (black hair:1.1), high ponytail, sidelocks, hair strands across face, sweeping bangs,
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
        
    if "爱抚" in action_name:
        prompt += "touching each other, fondling breasts, fingering, saliva, "
        
    if "征服" in action_name or "操" in action_name:
        prompt += "(doggystyle:1.3), (missionary:1.3), sex from behind, penis insertion, "
        
    if "高潮" in action_name or "崩溃" in action_name:
        prompt += "(ahegao:1.2), rolling eyes, tongue out, drooling, (heavy breathing), spasming body, (squirting:1.3), "
    
    if "小妮" in action_name:
        prompt += "focus on 1girl, (xiao_ni:1.2), "
    elif "小爱" in action_name:
        prompt += "focus on 1girl, (xiao_ai:1.2), "
    else:
        prompt += "2girls together, interacting, "

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
    # Load plan
    with open(PLAN_FILE, 'r', encoding='utf-8') as f:
        plan = json.load(f)
        
    client = ComfyUIClient(server_address=SERVER_ADDRESS)
    
    new_images_metadata = []

    print(f"Starting batch generation of {len(plan)} photos...")
    
    for idx, item in enumerate(plan):
        # Construct filename
        # Pattern: xiao_ni_202602140128_ch{chapter}_{idx}_{action}.jpg
        # Remove special chars from action name for filename
        safe_action_name = re.sub(r'[^\w\s-]', '', item['action_name']).strip().replace(' ', '_')
        filename = f"xiao_ni_202602140128_ch{item['chapter_index']}_{idx+1:02d}_{safe_action_name}.jpg"
        
        # Check if exists (optional: skip if strictly needed, but user said regenerate)
        # We will regenerate as requested.
        
        full_positive_prompt = BASE_PROMPT + generate_scene_prompt(item['action_name'], item['chapter_title'])
        
        print(f"[{idx+1}/{len(plan)}] Generating: {filename}")
        print(f"  Action: {item['action_name']}")
        
        try:
            # Generate
            image_data, actual_filename = client.text_to_image(
                positive_prompt=full_positive_prompt,
                negative_prompt=NEGATIVE_PROMPT,
                checkpoint="ponyDiffusionV6XL.safetensors"
            )
            
            # Save locally
            save_path = os.path.join(OUTPUT_DIR, filename)
            with open(save_path, "wb") as f:
                f.write(image_data)
                
            print(f"  Saved to: {save_path}")
            
            new_images_metadata.append({
                "chapter_index": item['chapter_index'],
                "action_name": item['action_name'],
                "filename": filename,
                "path": f"punishments/20260214/{filename}"
            })
            
            # Be nice to the server
            time.sleep(1) 
            
        except Exception as e:
            print(f"  Error generating {filename}: {e}")

    # Now Update Markdown
    update_markdown_with_images(new_images_metadata)
    
    # Save metadata for later index.html update
    with open("generated_images_metadata.json", "w", encoding='utf-8') as f:
        json.dump(new_images_metadata, f, ensure_ascii=False, indent=2)

def update_markdown_with_images(images_metadata):
    print("\nUpdating Markdown file...")
    
    with open(MARKDOWN_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Strategy: 
    # Find the Action Header (### Action Name)
    # Insert the image link right after it.
    
    new_content = content
    
    for img in images_metadata:
        # Construct the image link markdown
        img_md = f"\n**照片**: ![{img['action_name']}]({img['path']})\n"
        
        # Regex to find the header
        # pattern: ### [Action Name]\n
        # We need to escape regex characters in action name
        safe_header = re.escape(img['action_name'])
        pattern = re.compile(rf"(^###\s+{safe_header}\s*$)", re.MULTILINE)
        
        # Check if image already exists under this header (to avoid duplicates or replace)
        # But this is complex. Let's precise insert.
        
        match = pattern.search(new_content)
        if match:
            # Look ahead to see if there is already an image link nearby?
            # User said UPDATE. Simplest is to append after header.
            # Or replace existing "照片: ..." lines?
            
            # Let's try to find if there is an existing image line under this header and replace it
            # Search from match.end() until next header or end of file
            header_end = match.end()
            
            # Insert the new image link immediately after the header
            # new_content = new_content[:header_end] + img_md + new_content[header_end:]
            # Actually, let's look for existing "**照片**:" lines in the vicinity and remove them first to be clean?
            pass 
    
    # Re-reading line by line might be safer for insertion
    lines = content.split('\n')
    output_lines = []
    
    current_action = None
    
    for line in lines:
        output_lines.append(line)
        
        # Check for action header
        action_match = re.match(r'^###\s+(.+)', line.strip())
        if action_match:
            action_name = action_match.group(1).strip()
            
            # Find matching image
            matching_img = next((img for img in images_metadata if img['action_name'] == action_name), None)
            
            if matching_img:
                # Add image link
                img_link = f"\n**照片**: ![{matching_img['action_name']}]({matching_img['path']})"
                output_lines.append(img_link)
                # We skip adding the "old" image link if we encounter one in the next lines?
                # That logic is tricky. For now, let's just ADD.
                # Markdown allows multiple images.
    
    # Write back
    with open(MARKDOWN_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print("Markdown updated.")

if __name__ == "__main__":
    main()
