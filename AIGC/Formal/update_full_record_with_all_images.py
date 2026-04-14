#!/usr/bin/env python3
import os
import re

def update_full_record():
    date_str = "20260214"
    time_str = "0128"
    base_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_str}"
    md_file = os.path.join(base_dir, f"xiao_ni_{date_str}{time_str}_双人虐待惩罚_完整记录.md")
    
    if not os.path.exists(md_file):
        print(f"Error: {md_file} not found")
        return

    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Scan for all action images
    # Pattern: xiao_ni_202602140128_chX_YY_ActionName.jpg
    image_pattern = re.compile(rf"xiao_ni_{date_str}{time_str}_ch(\d+)_(\d+)_(.*?)\.jpg")
    action_to_img = {}
    for f in os.listdir(base_dir):
        m = image_pattern.match(f)
        if m:
            ch, seq, action = m.groups()
            action_to_img[action] = f

    new_lines = []
    current_chapter = 0
    
    for line in lines:
        new_lines.append(line)
        
        # Match headers: ### ActionName
        header_match = re.match(r'^###\s*(.*?)$', line.strip())
        if header_match:
            action = header_match.group(1).strip()
            # Try to match action to image
            if action in action_to_img:
                img_file = action_to_img[action]
                # Insert image right after header
                new_lines.append(f"\n**照片**: ![{action}](punishments/{date_str}/{img_file})\n")
    
    with open(md_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print(f"Updated {md_file} with {len(action_to_img)} action images.")

if __name__ == "__main__":
    update_full_record()
