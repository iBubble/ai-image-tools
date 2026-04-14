
import os
import json
import re

IMG_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260214"
MARKDOWN_FILE = os.path.join(IMG_DIR, "xiao_ni_202602140128_双人虐待惩罚_完整记录.md")
METADATA_FILE = "generated_images_metadata.json"

def scan_and_recover():
    files = os.listdir(IMG_DIR)
    # Filter for our generated images
    # Pattern: xiao_ni_202602140128_ch{chapter}_{idx}_{action}.jpg
    pattern = re.compile(r"xiao_ni_202602140128_ch(\d+)_(\d+)_(.+)\.jpg")
    
    metadata = []
    
    for f in files:
        if not f.endswith(".jpg"):
            continue
            
        match = pattern.match(f)
        if match:
            chapter = match.group(1)
            idx = match.group(2)
            action_name = match.group(3).replace('_', ' ') # Revert safe name somewhat
            
            # Identify action name from filename might be lossy if we stripped chars
            # But the key is to have a label.
            
            metadata.append({
                "chapter_index": int(chapter),
                "action_name": action_name, # This is a guess, but good enough for label
                "filename": f,
                "path": f"punishments/20260214/{f}",
                "sort_idx": int(idx)
            })
            
    # Sort by index
    metadata.sort(key=lambda x: x['sort_idx'])
    
    print(f"Recovered {len(metadata)} images.")
    
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
        
    return metadata

def update_markdown(metadata):
    if not os.path.exists(MARKDOWN_FILE):
        print("Markdown file not found.")
        return

    with open(MARKDOWN_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We want to insert images.
    # Since we don't have the exact original action name from plan (only from filename),
    # matching headers might be tricky if special chars were removed.
    # But let's try to match by Chapter and loosely by content?
    # Or just append all images at the end of sections?
    
    # Better approach: The plan file still exists from previous step? 
    # Yes: photo_plan.json
    
    plan_map = {}
    if os.path.exists("photo_plan.json"):
        with open("photo_plan.json", "r") as f:
            plan = json.load(f)
            # Map index to action name
            for i, p in enumerate(plan):
                plan_map[i+1] = p['action_name']
                
    lines = content.split('\n')
    new_lines = []
    
    # We can try to match headers again
    header_regex = re.compile(r'^###\s+(.+)')
    
    # Create a map of lowercased safe action names from filenames to metadata
    # filename action part: safe_action_name
    
    inserted_count = 0
    
    for line in lines:
        new_lines.append(line)
        match = header_regex.match(line)
        if match:
            # We found a header.
            # Do we have an image for this?
            # We can't easily match filename back to header text strictly.
            # But we can look at our plan_map if we track which header index we are at.
            pass

    # Fallback: Since matching is hard without the map from the generation process,
    # let's just make sure the markdown has links.
    # Actually, simpler: index.html needs the images array. Markdown content update is secondary for the modal view 
    # IF the modal view renders images from the array separately (it does, in the left panel).
    # The markdown text on right might not need the images inline.
    
    # But wait, our new renderMarkdown JS converts ![]() to clickable refs.
    # So we DO need them in markdown for that feature.
    
    # Let's use the plan to match
    if plan_map:
        # Re-read content
        final_lines = []
        
        # We need to count action headers to match with plan index
        action_header_count = 0
        
        for line in lines:
            final_lines.append(line)
            if line.startswith('### '):
                action_header_count += 1
                
                # Check if we have an image for this index
                # metadata has 'sort_idx' which corresponds to 1-based index in plan
                
                img = next((m for m in metadata if m['sort_idx'] == action_header_count), None)
                
                if img:
                    # Check if link exists next
                    # We will just append it. Markdown doesn't mind extra newlines.
                    label = plan_map.get(action_header_count, img['action_name'])
                    link = f"\n**照片**: ![{label}]({img['path']})\n"
                    final_lines.append(link)
                    inserted_count += 1
        
        with open(MARKDOWN_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(final_lines))
            
        print(f"Updated markdown with {inserted_count} images.")

if __name__ == "__main__":
    meta = scan_and_recover()
    update_markdown(meta)
