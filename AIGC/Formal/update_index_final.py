
import json
import re
import os

# Paths
metadata_path = "generated_images_metadata.json"
html_path = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/index.html"
markdown_path = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260214/xiao_ni_202602140128_双人虐待惩罚_完整记录.md"

def main():
    if not os.path.exists(metadata_path):
        print("Metadata file not found. Wait for generation to finish.")
        return

    with open(metadata_path, 'r', encoding='utf-8') as f:
        images_meta = json.load(f)
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    with open(markdown_path, 'r', encoding='utf-8') as f:
        full_markdown = f.read()

    # Find data variable
    match = re.search(r'const data = (\[.*?\]);', html_content, re.DOTALL)
    if not match:
        print("Could not find data variable.")
        return

    json_str = match.group(1)
    try:
        data = json.loads(json_str)
    except Exception as e:
        print(f"JSON error: {e}")
        return

    target_timestamp = "202602140128"
    
    # Construct images array for HTML
    # Format: {"path": "...", "label": "..."}
    images_array = []
    for img in images_meta:
        images_array.append({
            "path": img['path'], # relative path for web
            "label": f"[{img['chapter_index']}] {img['action_name']}"
        })
        
    # Update data
    updated = False
    for item in data:
        if item.get("timestamp") == target_timestamp:
            item['images'] = images_array
            item['full_content'] = full_markdown
            # Update thumbnail to the first image of the new set
            if len(images_array) > 0:
                # We don't store thumb path explicitly in item root usually, 
                # logic in HTML uses images[0].path
                pass
            updated = True
            print(f"Updated entry {target_timestamp} with {len(images_array)} images.")
            break
            
    if not updated:
        print("Entry not found!")
        return

    # specific fix for html rendering issues if any
    # Re-dump
    new_json_str = json.dumps(data, ensure_ascii=False)
    new_html = html_content.replace(json_str, new_json_str)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print("index.html updated successfully.")

if __name__ == "__main__":
    main()
