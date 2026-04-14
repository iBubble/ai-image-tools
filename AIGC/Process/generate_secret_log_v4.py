
import os
import re
import json
import shutil

PUNISHMENTS_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments"
OUTPUT_FILE = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/index.html"

def parse_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Title
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.basename(md_path)

    # Date and Time extraction
    dir_name = os.path.basename(os.path.dirname(md_path))
    date_part = dir_name if re.match(r'^\d{8}$', dir_name) else "Unknown"
    
    filename = os.path.basename(md_path)
    ts_match = re.search(r'(\d{12})', filename)
    full_timestamp = ts_match.group(1) if ts_match else (date_part + "0000" if date_part != "Unknown" else "000000000000")
    
    time_str = full_timestamp[8:12] if len(full_timestamp) >= 12 else "0000"
    time_display = f"{time_str[0:2]}:{time_str[2:4]}"

    # Background
    bg_match = re.search(r'\*\*惩罚背景\*\*:\s*(.*?)(?=\n|\r|$)', content)
    background = bg_match.group(1).strip() if bg_match else ""
    if not background:
        bg_match = re.search(r'\*\*测试背景\*\*:\s*(.*?)(?=\n|\r|$)', content)
        background = bg_match.group(1).strip() if bg_match else ""

    # All Images
    images = []
    # Search for all image paths in the markdown
    # Matches: [alt](file:///path), [alt](punishments/path), file:///path
    pattern = r'(?:file:///Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/|file://)?(/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/)?([\w/.-]+\.(?:jpg|png|jpeg))'
    # Actually, let's keep it simple: any string that starts withpunishments/ and ends with .jpg inside the MD
    img_pattern = r'punishments/(\d{8}/[\w.-]+\.(?:jpg|png|jpeg))'
    img_matches = re.finditer(img_pattern, content)
    for m in img_matches:
        rel_path = "punishments/" + m.group(1)
        full_path = os.path.join(PUNISHMENTS_DIR, m.group(1))
        if os.path.exists(full_path):
            if rel_path not in images:
                images.append(rel_path)
    
    # Also find Absolute paths and convert
    abs_pattern = r'(/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/(\d{8}/[\w.-]+\.(?:jpg|png|jpeg)))'
    abs_matches = re.finditer(abs_pattern, content)
    for m in abs_matches:
        full_path = m.group(1)
        rel_path = "punishments/" + m.group(2)
        if os.path.exists(full_path):
             if rel_path not in images:
                images.append(rel_path)

    return {
        "title": title,
        "timestamp": full_timestamp,
        "time_display": time_display,
        "background": background[:150] + "..." if len(background) > 150 else background,
        "full_content": content,
        "images": images,
        "date": date_part
    }

def generate_log_v4():
    all_data = []
    if not os.path.exists(PUNISHMENTS_DIR):
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

    all_data.sort(key=lambda x: x['timestamp'], reverse=True)
    dates = sorted(list(set(d['date'] for d in all_data if d['date'] != "Unknown")), reverse=True)
    if any(d['date'] == "Unknown" for d in all_data):
        dates.append("Unknown")

    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ANTIGRAVITY | 调教执行日志</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&family=Outfit:wght@300;600&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #040406; --sidebar: #0a0a0d; --card: #111115; --gold: #c5a059; --dim: #777780; --border: rgba(255,255,255,0.06); }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: var(--bg); color: #d1d1d6; font-family: 'Noto Sans SC', sans-serif; display: flex; height: 100vh; overflow: hidden; }}
        .sidebar {{ width: 240px; background: var(--sidebar); border-right: 1px solid var(--border); display: flex; flex-direction: column; }}
        .logo {{ padding: 35px 25px; font-family: 'Outfit'; font-weight: 600; letter-spacing: 3px; color: var(--gold); font-size: 1.4rem; text-align: center; }}
        .nav-list {{ flex: 1; overflow-y: auto; }}
        .nav-item {{ padding: 16px 25px; color: var(--dim); font-size: 0.9rem; cursor: pointer; transition: 0.2s; display: flex; justify-content: space-between; }}
        .nav-item:hover {{ color: #fff; background: rgba(255,255,255,0.03); }}
        .nav-item.active {{ color: var(--gold); background: rgba(197, 160, 89, 0.08); border-right: 2px solid var(--gold); }}
        .main {{ flex: 1; padding: 60px; overflow-y: auto; background: radial-gradient(circle at top right, #0d0d1a 0%, #040406 60%); }}
        h1 {{ font-size: 2.2rem; color: #fff; margin-bottom: 40px; font-weight: 300; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 25px; }}
        .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; cursor: pointer; transition: 0.3s; overflow: hidden; display: flex; height: 160px; }}
        .card:hover {{ border-color: var(--gold); transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.6); }}
        .card-thumb {{ width: 130px; background-size: cover; background-position: center; background-color: #000; }}
        .card-info {{ flex: 1; padding: 20px; display: flex; flex-direction: column; }}
        .card-title {{ color: var(--gold); font-weight: 600; font-size: 1rem; margin-bottom: 8px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
        .card-meta {{ font-family: 'Outfit'; font-size: 0.75rem; color: var(--dim); margin-bottom: 10px; }}
        .card-bg {{ font-size: 0.8rem; color: var(--dim); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
        #modal {{ position: fixed; inset: 0; background: rgba(0,0,0,0.95); z-index: 1000; display: none; padding: 30px; }}
        .modal-body {{ max-width: 1400px; margin: 0 auto; height: 100%; display: flex; background: #08080a; border: 1px solid var(--gold); border-radius: 20px; overflow: hidden; }}
        .modal-gallery {{ flex: 1.6; background: #000; display: flex; flex-direction: column; position: relative; }}
        .main-viewer {{ flex: 1; display: flex; align-items: center; justify-content: center; padding: 20px; }}
        #fullImg {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
        .thumb-strip {{ height: 100px; background: rgba(0,0,0,0.8); display: flex; gap: 10px; padding: 10px; overflow-x: auto; border-top: 1px solid var(--border); }}
        .mini-thumb {{ height: 100%; aspect-ratio: 1; background-size: cover; background-position: center; cursor: pointer; border: 2px solid transparent; opacity: 0.5; transition: 0.2s; }}
        .mini-thumb.active {{ opacity: 1; border-color: var(--gold); }}
        .modal-info {{ flex: 1; padding: 50px; overflow-y: auto; border-left: 1px solid var(--border); line-height: 1.8; }}
        .modal-info h2 {{ color: var(--gold); margin-bottom: 25px; font-size: 1.6rem; }}
        .md-content {{ color: #ccc; font-size: 0.95rem; }}
        .md-content strong {{ color: #e54; }}
        .md-content b {{ color: var(--gold); display: block; margin-top: 25px; font-size: 1.1rem; border-bottom: 1px solid var(--border); padding-bottom: 5px; }}
        .close-x {{ position: absolute; top: 25px; right: 25px; color: #fff; font-size: 2.2rem; cursor: pointer; z-index: 1001; }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">ANTIGRAVITY</div>
        <div class="nav-list" id="navList"></div>
    </div>
    <div class="main">
        <h1 id="pageTitle">档案库读取中...</h1>
        <div class="grid" id="grid"></div>
    </div>
    <div id="modal">
        <span class="close-x" onclick="closeModal()">&times;</span>
        <div class="modal-body">
            <div class="modal-gallery">
                <div class="main-viewer"><img id="fullImg" src=""></div>
                <div class="thumb-strip" id="thumbStrip"></div>
            </div>
            <div class="modal-info">
                <h2 id="modalTitle"></h2>
                <div class="md-content" id="modalMd"></div>
            </div>
        </div>
    </div>
    <script>
        const store = {json.dumps(all_data)};
        const dates = {json.dumps(dates)};
        function formatD(d) {{ return d === "Unknown" ? "未知日期" : d.substr(0,4)+"/"+d.substr(4,2)+"/"+d.substr(6,2); }}
        function init() {{
            const nav = document.getElementById('navList');
            dates.forEach(d => {{
                const count = store.filter(x => x.date === d).length;
                const div = document.createElement('div');
                div.className = 'nav-item';
                div.innerHTML = `<span>${{formatD(d)}}</span> <span>${{count}}</span>`;
                div.onclick = () => renderDate(d, div);
                nav.appendChild(div);
            }});
            if (dates.length > 0) renderDate(dates[0], nav.firstChild);
        }}
        function renderDate(date, el) {{
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            el.classList.add('active');
            document.getElementById('pageTitle').innerText = formatD(date) + " 调教档案记录";
            const grid = document.getElementById('grid');
            grid.innerHTML = '';
            store.filter(x => x.date === date).forEach(p => {{
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => showDetail(p);
                const thumb = p.images.length > 0 ? p.images[0] : '';
                card.innerHTML = `<div class="card-thumb" style="background-image: url('${{thumb}}')"></div>
                    <div class="card-info"><div class="card-title">${{p.title}}</div>
                    <div class="card-meta">${{p.time_display}} | ID: ${{p.timestamp}}</div>
                    <div class="card-bg">${{p.background}}</div></div>`;
                grid.appendChild(card);
            }});
        }}
        function showDetail(p) {{
            document.getElementById('modalTitle').innerText = p.title;
            const md = p.full_content.replace(/\\n/g, '<br>').replace(/#+\\s+(.*)/g, '<b>$1</b>').replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>').replace(/(file:\\/\\/\\/\\S+)/g, '');
            document.getElementById('modalMd').innerHTML = md;
            const strip = document.getElementById('thumbStrip');
            strip.innerHTML = '';
            if (p.images.length > 0) {{
                p.images.forEach((img, i) => {{
                    const t = document.createElement('div');
                    t.className = 'mini-thumb' + (i === 0 ? ' active' : '');
                    t.style.backgroundImage = `url('${{img}}')`;
                    t.onclick = () => {{
                        document.querySelectorAll('.mini-thumb').forEach(x => x.classList.remove('active'));
                        t.classList.add('active');
                        document.getElementById('fullImg').src = img;
                    }};
                    strip.appendChild(t);
                }});
                document.getElementById('mainImg')?.src ? (document.getElementById('mainImg').src = p.images[0]) : (document.getElementById('fullImg').src = p.images[0]);
            }}
            document.getElementById('modal').style.display = 'block';
        }}
        function closeModal() {{ document.getElementById('modal').style.display = 'none'; }}
        init();
    </script>
</body>
</html>
    """

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Web V4 generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_log_v4()
