import os
import shutil
import re
from datetime import datetime
import glob

SOURCE_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments"
WEB_ROOT = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/XiaoAi"
IMAGE_DEST = os.path.join(WEB_ROOT, "images")

def setup_directories():
    os.makedirs(IMAGE_DEST, exist_ok=True)

def parse_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'# (.*)', content)
    title = title_match.group(1) if title_match else "无题惩罚"
    
    # Extract sections with images
    sections = []
    current_section = {}
    
    lines = content.split('\n')
    for line in lines:
        if line.startswith('## '):
            if current_section:
                sections.append(current_section)
            current_section = {'title': line[3:].strip(), 'text': '', 'images': []}
        elif line.startswith('**影像验证**') or line.startswith('**真实验证**'):
            # Extract image link from markdown
            img_match = re.search(r'\((.*?)\)', line)
            if img_match:
                img_path = img_match.group(1).replace('file://', '')
                if os.path.exists(img_path):
                     curr_img_dest = copy_image(img_path)
                     current_section['images'].append(curr_img_dest)
        elif current_section:
            current_section['text'] += line + '\n'
            
    if current_section:
        sections.append(current_section)
        
    return title, sections

def copy_image(src_path):
    filename = os.path.basename(src_path)
    # Organization by date might be better, but flat for now or by original structure
    # Let's use the parent folder name as date
    date_folder = os.path.basename(os.path.dirname(src_path))
    dest_folder = os.path.join(IMAGE_DEST, date_folder)
    os.makedirs(dest_folder, exist_ok=True)
    
    dest_path = os.path.join(dest_folder, filename)
    
    should_copy = False
    if not os.path.exists(dest_path):
        should_copy = True
    else:
        src_mtime = os.path.getmtime(src_path)
        dest_mtime = os.path.getmtime(dest_path)
        if src_mtime > dest_mtime:
            should_copy = True
            
    if should_copy:
        shutil.copy2(src_path, dest_path)
        
    return f"images/{date_folder}/{filename}"

def generate_html():
    setup_directories()
    
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小妮的惩罚记录 | Xiao Ni's Punishment Log</title>
    <style>
        :root {
            --primary-color: #ff2d55;
            --bg-color: #0d0d0d;
            --card-bg: #1c1c1e;
            --text-color: #f2f2f7;
            --secondary-text: #8e8e93;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid #333;
            margin-bottom: 40px;
        }
        h1 {
            color: var(--primary-color);
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(255, 45, 85, 0.3);
        }
        .subtitle {
            color: var(--secondary-text);
            font-size: 1.1em;
        }
        .punishment-card {
            background-color: var(--card-bg);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 1px solid #333;
        }
        .punishment-header {
            border-bottom: 1px solid #333;
            padding-bottom: 15px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .punishment-title {
            font-size: 1.5em;
            color: #fff;
            margin: 0;
        }
        .punishment-date {
            color: var(--primary-color);
            font-weight: bold;
            font-family: monospace;
        }
        .section {
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 1.2em;
            color: #ddd;
            margin-bottom: 10px;
            border-left: 3px solid var(--primary-color);
            padding-left: 10px;
        }
        .section-text {
            color: #bbb;
            margin-bottom: 15px;
            white-space: pre-wrap;
        }
        .image-gallery {
            display: grid;
            gap: 15px;
        }
        .punishment-img {
            width: 100%;
            border-radius: 8px;
            transition: transform 0.3s ease;
            cursor: pointer;
        }
        .punishment-img:hover {
            transform: scale(1.02);
        }
        footer {
            text-align: center;
            color: #666;
            margin-top: 50px;
            padding: 20px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Xiao Ni's Punishment Log</h1>
            <div class="subtitle">记录每一滴眼泪与每一次臣服</div>
        </header>
    """
    
    # Walk through dates in reverse order
    punishments = []
    
    for date_folder in sorted(os.listdir(SOURCE_DIR), reverse=True):
        date_path = os.path.join(SOURCE_DIR, date_folder)
        if not os.path.isdir(date_path):
            continue
            
        md_files = glob.glob(os.path.join(date_path, "*_ming.md"))
        for md_file in md_files:
            # Parse timestamp from filename to sort
            # Filename format: xiao_ni_YYYYMMDDHHMM_..._ming.md
            basename = os.path.basename(md_file)
            parts = basename.split('_')
            timestamp = "Unknown"
            if len(parts) >= 3 and parts[2].isdigit():
                 timestamp = parts[2]
            
            title, sections = parse_markdown(md_file)
            punishments.append({
                'timestamp': timestamp,
                'date': date_folder,
                'title': title,
                'sections': sections,
                'file': basename
            })
            
    # Sort by timestamp descending
    punishments.sort(key=lambda x: x['timestamp'], reverse=True)
    
    for p in punishments:
        # Format timestamp nicely
        ts = p['timestamp']
        if len(ts) == 12:
            formatted_time = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}"
        else:
            formatted_time = ts
            
        html_content += f"""
        <div class="punishment-card">
            <div class="punishment-header">
                <h2 class="punishment-title">{p['title']}</h2>
                <span class="punishment-date">{formatted_time}</span>
            </div>
        """
        
        for section in p['sections']:
            html_content += f"""
            <div class="section">
                <h3 class="section-title">{section['title']}</h3>
                <div class="section-text">{section['text']}</div>
                <div class="image-gallery">
            """
            for img in section['images']:
                html_content += f'<img src="{img}" class="punishment-img" loading="lazy" alt="Punishment Evidence">'
            
            html_content += """
                </div>
            </div>
            """
            
        html_content += "</div>"

    html_content += """
        <footer>
            <p>&copy; 2026 Antigravity Project - Xiao Ni Punishment Archive</p>
            <p style="font-size: 0.8em; color: #444;">Generated by Xiao Ni (Slave Mode)</p>
        </footer>
    </div>
</body>
</html>
    """
    
    with open(os.path.join(WEB_ROOT, "index.html"), "w", encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Webpage generated at {os.path.join(WEB_ROOT, 'index.html')}")

if __name__ == "__main__":
    generate_html()
