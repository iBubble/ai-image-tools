
import os
import re
import json
import shutil
from datetime import datetime

PUNISHMENTS_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments"
OUTPUT_FILE = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/index.html"

def parse_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Title
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.basename(md_path)

    # Timestamp and Date extraction
    # Try directory name first (YYYYMMDD)
    dir_name = os.path.basename(os.path.dirname(md_path))
    date_str = dir_name if re.match(r'\\d{8}', dir_name) else "Unknown"
    
    # Try filename for HHMM
    filename = os.path.basename(md_path)
    time_match = re.search(r'\\d{8}(\\d{4})', filename)
    time_str = time_match.group(1) if time_match else "0000"
    
    full_timestamp = (date_str + time_str) if date_str != "Unknown" else "000000000000"

    # Background
    bg_match = re.search(r'\*\*惩罚背景\*\*:\s*(.*?)(?=\\n|\\r|$)', content)
    background = bg_match.group(1).strip() if bg_match else ""
    if not background:
        bg_match = re.search(r'\*\*测试背景\*\*:\s*(.*?)(?=\\n|\\r|$)', content)
        background = bg_match.group(1).strip() if bg_match else ""

    # Images extraction - improved
    images = []
    # Match markdown style: ![alt](path)
    img_matches = re.finditer(r'!?\\[.*?\\]\\((.*?)\\)', content)
    for m in img_matches:
        raw_path = m.group(1).strip()
        # Clean file:// and other prefixes
        clean_path = raw_path.replace('file://', '').split('?')[0]
        if os.path.exists(clean_path) and clean_path.endswith(('.jpg', '.png', '.jpeg')):
            rel_path = "punishments/" + os.path.relpath(clean_path, PUNISHMENTS_DIR)
            if rel_path not in images:
                images.append(rel_path)

    # Secondary check for raw file:// links not in markdown syntax
    raw_links = re.finditer(r'file://(/Users/[^\\s\\n\\r)]+)', content)
    for m in raw_links:
        clean_path = m.group(1).strip()
        if os.path.exists(clean_path) and clean_path.endswith(('.jpg', '.png', '.jpeg')):
            rel_path = "punishments/" + os.path.relpath(clean_path, PUNISHMENTS_DIR)
            if rel_path not in images:
                images.append(rel_path)

    return {
        "title": title,
        "timestamp": full_timestamp,
        "background": background[:150] + "..." if len(background) > 150 else background,
        "full_content": content,
        "images": images,
        "date": date_str
    }

def generate_log():
    all_data = []
    if not os.path.exists(PUNISHMENTS_DIR):
        print("Punishments directory not found.")
        return

    for root, dirs, files in os.walk(PUNISHMENTS_DIR):
        for file in files:
            if file.endswith("_ming.md"):
                full_path = os.path.join(root, file)
                try:
                    data = parse_markdown(full_path)
                    all_data.append(data)
                except Exception as e:
                    print(f"Error parsing {file}: {e}")

    # Sort
    all_data.sort(key=lambda x: x['timestamp'], reverse=True)
    dates = sorted(list(set(d['date'] for d in all_data if d['date'] != "Unknown")), reverse=True)
    if any(d['date'] == "Unknown" for d in all_data):
        dates.append("Unknown")

    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ANTIGRAVITY | 深度调教日志</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&family=Outfit:wght@300;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: #050507;
            --sidebar-bg: #0c0c0f;
            --card-bg: rgba(20, 20, 25, 0.8);
            --accent-gold: #c5a059;
            --accent-red: #c43232;
            --text-main: #d1d1d6;
            --text-dim: #8e8e93;
            --glass-border: rgba(255, 255, 255, 0.08);
            --active-item: rgba(197, 160, 89, 0.15);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Noto Sans SC', sans-serif;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}

        /* Sidebar */
        .sidebar {{
            width: 240px;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--glass-border);
            display: flex;
            flex-direction: column;
            z-index: 10;
        }}

        .logo {{
            padding: 30px;
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--accent-gold);
            letter-spacing: 3px;
            text-align: center;
            border-bottom: 1px solid var(--glass-border);
        }}

        .date-list {{
            flex: 1;
            overflow-y: auto;
            padding: 20px 0;
        }}

        .date-item {{
            padding: 15px 30px;
            cursor: pointer;
            transition: 0.2s;
            color: var(--text-dim);
            font-size: 0.9rem;
            display: flex;
            justify-content: space-between;
        }}

        .date-item:hover {{ color: #fff; background: var(--glass-border); }}
        .date-item.active {{
            background: var(--active-item);
            color: var(--accent-gold);
            border-right: 2px solid var(--accent-gold);
        }}

        /* Main Content */
        .main-content {{
            flex: 1;
            overflow-y: auto;
            padding: 50px;
            position: relative;
        }}

        .main-content::before {{
            content: '';
            position: fixed;
            top: 0; right: 0;
            width: 400px; height: 400px;
            background: radial-gradient(circle, rgba(197, 160, 89, 0.05) 0%, transparent 70%);
            pointer-events: none;
        }}

        header {{ margin-bottom: 50px; }}
        h1 {{ font-size: 2.5rem; letter-spacing: -1px; margin-bottom: 10px; color: #fff; }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 30px;
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            overflow: hidden;
            cursor: pointer;
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
        }}

        .card:hover {{
            transform: translateY(-8px);
            border-color: var(--accent-gold);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}

        .thumb {{
            height: 200px;
            background-color: #000;
            background-size: cover;
            background-position: center;
            position: relative;
        }}

        .thumb::after {{
            content: '';
            position: absolute;
            bottom: 0; left: 0; width: 100%; height: 50%;
            background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
        }}

        .card-body {{ padding: 25px; }}
        .card-title {{
            color: var(--accent-gold);
            font-weight: 700;
            font-size: 1.15rem;
            margin-bottom: 10px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .card-meta {{ font-size: 0.8rem; color: var(--text-dim); margin-bottom: 15px; font-family: 'Outfit'; }}
        .card-desc {{ font-size: 0.85rem; color: var(--text-dim); line-height: 1.6; }}

        /* Modal / Detail View */
        #modal {{
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.95);
            display: none;
            z-index: 100;
            padding: 40px;
            overflow-y: auto;
        }}

        .modal-content {{
            max-width: 1200px;
            margin: 0 auto;
            background: #111;
            border-radius: 20px;
            border: 1px solid var(--glass-border);
            overflow: hidden;
            display: flex;
            min-height: 80vh;
        }}

        .gallery {{
            flex: 1;
            background: #000;
            display: flex;
            flex-direction: column;
            position: relative;
        }}

        .main-img-container {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}

        #mainImg {{ max-width: 100%; max-height: 70vh; object-fit: contain; }}

        .thumbnail-bar {{
            height: 100px;
            background: rgba(255,255,255,0.05);
            display: flex;
            gap: 10px;
            padding: 10px;
            overflow-x: auto;
            justify-content: center;
        }}

        .small-thumb {{
            height: 100%;
            width: 80px;
            background-size: cover;
            background-position: center;
            border: 2px solid transparent;
            cursor: pointer;
            opacity: 0.6;
        }}

        .small-thumb.active {{ opacity: 1; border-color: var(--accent-gold); }}

        .info-panel {{
            width: 450px;
            padding: 50px;
            overflow-y: auto;
            border-left: 1px solid var(--glass-border);
            line-height: 1.8;
        }}

        .info-panel h2 {{ font-size: 1.8rem; color: var(--accent-gold); margin-bottom: 30px; }}
        .markdown-body {{ font-size: 0.95rem; color: var(--text-main); }}
        .markdown-body strong {{ color: var(--accent-red); }}

        .close-btn {{
            position: fixed;
            top: 20px; right: 20px;
            font-size: 2.5rem;
            color: #fff;
            cursor: pointer;
            z-index: 101;
        }}
    </style>
</head>
<body>
    <aside class="sidebar">
        <div class="logo">ANTIGRAVITY</div>
        <div class="date-list" id="dateList"></div>
    </aside>

    <main class="main-content">
        <header>
            <h1 id="topTitle">档案库读取中...</h1>
        </header>
        <div class="grid" id="grid"></div>
    </main>

    <div id="modal">
        <span class="close-btn" onclick="closeModal()">&times;</span>
        <div class="modal-content">
            <div class="gallery">
                <div class="main-img-container">
                    <img id="mainImg" src="" alt="惩罚验证">
                </div>
                <div class="thumbnail-bar" id="thumbBar"></div>
            </div>
            <div class="info-panel">
                <h2 id="detailTitle"></h2>
                <div class="markdown-body" id="detailContent"></div>
            </div>
        </div>
    </div>

    <script>
        const rawData = {json.dumps(all_data)};
        const dates = {json.dumps(dates)};

        function formatDisplayDate(d) {{
            if (d === "Unknown") return "未知日期";
            return `${{d.substring(0,4)}}/${{d.substring(4,6)}}/${{d.substring(6,8)}}`;
        }}

        function initSidebar() {{
            const list = document.getElementById('dateList');
            dates.forEach(d => {{
                const count = rawData.filter(item => item.date === d).length;
                const div = document.createElement('div');
                div.className = 'date-item';
                div.innerHTML = `<span>${{formatDisplayDate(d)}}</span> <span>(${{count}})</span>`;
                div.onclick = () => selectDate(d, div);
                list.appendChild(div);
            }});
            if (dates.length > 0) selectDate(dates[0], list.firstChild);
        }}

        function selectDate(date, el) {{
            document.querySelectorAll('.date-item').forEach(i => i.classList.remove('active'));
            el.classList.add('active');
            
            document.getElementById('topTitle').innerText = formatDisplayDate(date) + " 调教档案";
            
            const grid = document.getElementById('grid');
            grid.innerHTML = '';
            
            const filtered = rawData.filter(item => item.date === date);
            filtered.forEach(p => {{
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => openDetail(p);
                
                const thumb = p.images.length > 0 ? p.images[0] : '';
                const timeStr = p.timestamp.length >= 12 ? `${{p.timestamp.substring(8,10)}}:${{p.timestamp.substring(10,12)}}` : 'Unknown';
                
                card.innerHTML = `
                    <div class="thumb" style="background-image: url('${{thumb}}')"></div>
                    <div class="card-body">
                        <div class="card-title">${{p.title}}</div>
                        <div class="card-meta">${{timeStr}} | 归档 ID: ${{p.timestamp}}</div>
                        <div class="card-desc">${{p.background}}</div>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        function openDetail(p) {{
            document.getElementById('detailTitle').innerText = p.title;
            const content = p.full_content
                .replace(/\\n/g, '<br>')
                .replace(/#+\\s+(.*)/g, '<b>$1</b>')
                .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                .replace(/(file:\\/\\/\\/\\S+)/g, ''); // Clear internal file paths from text
                
            document.getElementById('detailContent').innerHTML = content;
            
            const bar = document.getElementById('thumbBar');
            bar.innerHTML = '';
            
            if (p.images.length > 0) {{
                p.images.forEach((img, idx) => {{
                    const div = document.createElement('div');
                    div.className = 'small-thumb' + (idx === 0 ? ' active' : '');
                    div.style.backgroundImage = `url('${{img}}')`;
                    div.onclick = () => {{
                        document.querySelectorAll('.small-thumb').forEach(t => t.classList.remove('active'));
                        div.classList.add('active');
                        document.getElementById('mainImg').src = img;
                    }};
                    bar.appendChild(div);
                }});
                document.getElementById('mainImg').src = p.images[0];
            }} else {{
                document.getElementById('mainImg').src = '';
            }}
            
            document.getElementById('modal').style.display = 'block';
        }}

        function closeModal() {{
            document.getElementById('modal').style.display = 'none';
        }}

        initSidebar();
    </script>
</body>
</html>
    """

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Log generated successfully at {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_log()
