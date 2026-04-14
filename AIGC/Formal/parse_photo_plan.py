
import re
import os
import json

# File paths
markdown_path = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260214/xiao_ni_202602140128_双人虐待惩罚_完整记录.md"

def parse_markdown_structure(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    structure = []
    current_chapter = None
    current_chapter_index = 0
    
    # Regex for chapters and actions
    chapter_pattern = re.compile(r'^##\s+(第.+章[：:].+)')
    action_pattern = re.compile(r'^###\s+(.+)')
    
    for line in lines:
        line = line.strip()
        
        # Match Chapter
        chapter_match = chapter_pattern.match(line)
        if chapter_match:
            current_chapter = chapter_match.group(1)
            current_chapter_index += 1
            print(f"Found Chapter {current_chapter_index}: {current_chapter}")
            continue
            
        # Match Action (only if inside a chapter)
        if current_chapter:
            action_match = action_pattern.match(line)
            if action_match:
                action_name = action_match.group(1)
                
                # Filter out non-visual sections usually found in this format
                if any(x in action_name for x in ["生理反应", "心理状态", "心声", "总结"]):
                    continue
                    
                print(f"  - Found Action: {action_name}")
                
                structure.append({
                    "chapter_index": current_chapter_index,
                    "chapter_title": current_chapter,
                    "action_name": action_name,
                    # We will assume the text following this header describes the prompt
                    # For now just capturing the structure
                })

    return structure

structure = parse_markdown_structure(markdown_path)
print(f"Total photos to generate: {len(structure)}")

# Save structure for the next step (generation script)
with open("photo_plan.json", "w", encoding='utf-8') as f:
    json.dump(structure, f, ensure_ascii=False, indent=2)
