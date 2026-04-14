
import os
import re
import json
import shutil
from datetime import datetime

PUNISHMENTS_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments"
OUTPUT_FILE = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/index.html"
IMAGE_WEB_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/web_assets"

def parse_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Title
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(md_path)

    # Timestamp from title or filename
    ts_match = re.search(r'(\\d{12})', title)
    timestamp = ts_match.group(1) if ts_match else ""
    if not timestamp:
        ts_match = re.search(r'(\\d{12})', md_path)
        timestamp = ts_match.group(1) if ts_match else ""

    # Background
    bg_match = re.search(r'\*\*惩罚背景\*\*:\s*(.*)', content)
    background = bg_match.group(1) if bg_match else ""
    if not background:
        bg_match = re.search(r'\*\*测试背景\*\*:\s*(.*)', content)
        background = bg_match.group(1) if bg_match else ""

    # Images
    images = []
    # Match both Markdown links and raw file paths
    img_matches = re.finditer(r'!?\\[.*?\\]\\((file://)?(.*?)\\)', content)
    for m in img_matches:
        img_path = m.group(3)
        if os.path.exists(img_path):
            # Extract relative path for web
            rel_path = os.path.join("punishments", os.path.relpath(img_path, PUNISHMENTS_DIR))
            images.append(rel_path)

    # If no images found via markdown syntax, look for raw file:// links
    if not images:
        raw_links = re.finditer(r'file://(/Users/.*?\\.jpg)', content)
        for m in raw_links:
            img_path = m.group(1)
            if os.path.exists(img_path):
                 rel_path = os.path.join("punishments", os.path.relpath(img_path, PUNISHMENTS_DIR))
                 images.append(rel_path)

    return {
        "title": title,
        "timestamp": timestamp,
        "background": background[:100] + "..." if len(background) > 100 else background,
        "full_content": content,
        "images": images,
        "date": timestamp[:8] if timestamp else "Unknown"
    }

def generate_log():
    all_data = []
    for root, dirs, files in os.walk(PUNISHMENTS_DIR):
        for file in files:
            if file.endswith("_ming.md"):
                full_path = os.path.join(root, file)
                try:
                    data = parse_markdown(full_path)
                    all_data.append(data)
                except Exception as e:
                    print(f"Error parsing {file}: {e}")

    # Sort by timestamp descending
    all_data.sort(key=lambda x: x['timestamp'], reverse=True)

    # Group by date
    dates = sorted(list(set(d['date'] for d in all_data)), reverse=True)
    
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小妮的深度调教记录档案</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&family=Outfit:wght@300;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: #0a0a0c;
            --sidebar-bg: #121216;
            --card-bg: rgba(30, 30, 38, 0.7);
            --accent-gold: #d4af37;
            --accent-red: #8b0000;
            --text-main: #e0e0e0;
            --text-dim: #a0a0a0;
            --glass: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.1);
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
            width: 260px;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--glass-border);
            display: flex;
            flex-direction: column;
            padding: 20px 0;
        }}

        .logo {{
            padding: 0 25px 30px;
            font-family: 'Outfit', sans-serif;
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--accent-gold);
            letter-spacing: 2px;
            border-bottom: 1px solid var(--glass-border);
            margin-bottom: 20px;
        }}

        .date-list {{
            flex: 1;
            overflow-y: auto;
        }}

        .date-item {{
            padding: 12px 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: var(--text-dim);
            font-size: 0.95rem;
            display: flex;
            align-items: center;
        }}

        .date-item:hover, .date-item.active {{
            background: var(--glass);
            color: var(--accent-gold);
            border-left: 4px solid var(--accent-gold);
        }}

        .date-item span {{ margin-left: auto; font-size: 0.8rem; opacity: 0.5; }}

        /* Main Content */
        .main-content {{
            flex: 1;
            overflow-y: auto;
            padding: 40px;
            background: radial-gradient(circle at top right, #1a1a2e, #0a0a0c);
        }}

        .header {{
            margin-bottom: 40px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}

        h1 {{ font-size: 2.2rem; font-weight: 700; color: #fff; }}

        .punishment-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 25px;
        }}

        .card {{
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid var(--glass-border);
            overflow: hidden;
            display: flex;
            transition: transform 0.3s ease, border-color 0.3s ease;
            cursor: pointer;
            height: 180px;
        }}

        .card:hover {{
            transform: translateY(-5px);
            border-color: var(--accent-gold);
        }}

        .card-img {{
            width: 140px;
            background-size: cover;
            background-position: center;
            border-right: 1px solid var(--glass-border);
        }}

        .card-body {{
            padding: 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }}

        .card-title {{
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 8px;
            color: var(--accent-gold);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .card-ts {{
            font-size: 0.8rem;
            color: var(--text-dim);
            margin-bottom: 12px;
            font-family: 'Outfit', sans-serif;
        }}

        .card-desc {{
            font-size: 0.85rem;
            line-height: 1.5;
            color: var(--text-dim);
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        /* Modal */
        #modal {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.9);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            backdrop-filter: blur(5px);
        }}

        .modal-content {{
            width: 90%;
            height: 90%;
            background: var(--sidebar-bg);
            border-radius: 24px;
            border: 1px solid var(--accent-gold);
            display: flex;
            overflow: hidden;
            box-shadow: 0 0 50px rgba(0,0,0,0.5);
        }}

        .modal-view {{
            flex: 1.2;
            background: #000;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }}

        .modal-view img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}

        .modal-info {{
            flex: 0.8;
            padding: 40px;
            overflow-y: auto;
            line-height: 1.8;
            border-left: 1px solid var(--glass-border);
        }}

        .modal-info h2 {{ color: var(--accent-gold); margin-bottom: 30px; }}
        .modal-info p {{ margin-bottom: 20px; color: var(--text-main); font-size: 0.95rem; }}
        .close-btn {{
            position: absolute;
            top: 20px; right: 20px;
            font-size: 2rem;
            cursor: pointer;
            color: #fff;
            background: rgba(255,255,255,0.1);
            width: 40px; height: 40px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            z-index: 1001;
        }}
    </style>
</head>
<body>
    <aside class="sidebar">
        <div class="logo">ANTIGRAVITY</div>
        <div class="date-list" id="dateList">
            <!-- Dates will be injected here -->
        </div>
    </aside>

    <main class="main-content">
        <header class="header">
            <h1 id="currentDateTitle">最新档案记录</h1>
            <div id="statusCount"></div>
        </header>

        <div class="punishment-grid" id="punishmentGrid">
            <!-- Cards will be injected here -->
        </div>
    </main>

    <div id="modal">
        <span class="close-btn" onclick="closeModal()">&times;</span>
        <div class="modal-content">
            <div class="modal-view">
                <img id="modalImg" src="" alt="惩罚验证">
            </div>
            <div class="modal-info" id="modalInfo">
                <!-- Detailed markdown content -->
            </div>
        </div>
    </div>

    <script>
        const data = {json.dumps(all_data)};
        const dates = {json.dumps(dates)};

        function renderDateList() {{
            const list = document.getElementById('dateList');
            dates.forEach(date => {{
                const count = data.filter(d => d.date === date).length;
                const div = document.createElement('div');
                div.className = 'date-item';
                div.innerHTML = `${{date.substring(0,4)}}/${{date.substring(4,6)}}/${{date.substring(6,8)}} <span>(${{count}})</span>`;
                div.onclick = () => filterByDate(date, div);
                list.appendChild(div);
            }});
            
            if (dates.length > 0) {{
                filterByDate(dates[0], list.firstChild);
            }}
        }}

        function filterByDate(date, el) {{
            document.querySelectorAll('.date-item').forEach(i => i.classList.remove('active'));
            el.classList.add('active');
            
            document.getElementById('currentDateTitle').innerText = `${{date.substring(0,4)}}年${{date.substring(4,6)}}月${{date.substring(6,8)}}日 调教记录`;
            
            const filtered = data.filter(d => d.date === date);
            const grid = document.getElementById('punishmentGrid');
            grid.innerHTML = '';
            
            filtered.forEach(p => {{
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => openModal(p);
                
                const imgUrl = p.images.length > 0 ? p.images[0] : '';
                
                card.innerHTML = `
                    <div class="card-img" style="background-image: url('${{imgUrl}}')"></div>
                    <div class="card-body">
                        <div class="card-title">${{p.title}}</div>
                        <div class="card-ts">${{formatTs(p.timestamp)}}</div>
                        <div class="card-desc">${{p.background}}</div>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        function formatTs(ts) {{
            if (!ts) return "Unknown";
            return `${{ts.substring(8,10)}}:${{ts.substring(10,12)}}`;
        }}

        function openModal(p) {{
            const modal = document.getElementById('modal');
            const img = document.getElementById('modalImg');
            const info = document.getElementById('modalInfo');
            
            img.src = p.images.length > 0 ? p.images[0] : '';
            info.innerHTML = p.full_content.replace(/\\n/g, '<br>').replace(/file:\\/\\/.*?\\.jpg/g, '');
            
            modal.style.display = 'flex';
        }}

        function closeModal() {{
            document.getElementById('modal').style.display = 'none';
        }}

        window.onclick = function(event) {{
            if (event.target == document.getElementById('modal')) closeModal();
        }}

        renderDateList();
    </script>
</body>
</html>
    """

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Log generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_log()
