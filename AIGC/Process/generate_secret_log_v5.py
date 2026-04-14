
import os
import re
import json

PUNISHMENTS_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments"
OUTPUT_FILE = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/index.html"

def parse_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.basename(md_path)

    dir_name = os.path.basename(os.path.dirname(md_path))
    date_part = dir_name if re.match(r'^\d{8}$', dir_name) else "Unknown"
    
    filename = os.path.basename(md_path)
    ts_match = re.search(r'(\d{12})', filename)
    full_timestamp = ts_match.group(1) if ts_match else (date_part + "0000" if date_part != "Unknown" else "000000000000")
    
    time_str = full_timestamp[8:12] if len(full_timestamp) >= 12 else "0000"
    time_display = f"{time_str[0:2]}:{time_str[2:4]}"

    bg_match = re.search(r'\*\*惩罚背景\*\*:\s*(.*?)(?=\n|\r|$)', content)
    background = bg_match.group(1).strip() if bg_match else ""

    images = []
    # Force search for all JPGs mentioned in the file, regardless of markdown tags
    # This catches file:/// paths and other raw links
    img_candidates = re.findall(r'(/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/\d{8}/[\w.-]+\.(?:jpg|png|jpeg))', content)
    for path in img_candidates:
        if os.path.exists(path):
            rel = "punishments/" + os.path.relpath(path, PUNISHMENTS_DIR)
            if rel not in images:
                images.append(rel)

    return {
        "title": title,
        "timestamp": full_timestamp,
        "time_display": time_display,
        "background": background[:150] + "...",
        "full_content": content,
        "images": images,
        "date": date_part
    }

def generate_log_v5():
    all_data = []
    for root, dirs, files in os.walk(PUNISHMENTS_DIR):
        for file in files:
            if file.endswith("_ming.md"):
                try:
                    all_data.append(parse_markdown(os.path.join(root, file)))
                except: pass

    all_data.sort(key=lambda x: x['timestamp'], reverse=True)
    dates = sorted(list(set(d['date'] for d in all_data if d['date'] != "Unknown")), reverse=True)

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ANTIGRAVITY | 调教执行日志</title>
    <style>
        :root {{ --gold: #c5a059; --bg: #050508; --side: #0c0c10; --card: #121218; --border: rgba(255,255,255,0.08); }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: var(--bg); color: #ccc; font-family: sans-serif; display: flex; height: 100vh; overflow: hidden; }}
        .sidebar {{ width: 240px; background: var(--side); border-right: 1px solid var(--border); display: flex; flex-direction: column; }}
        .logo {{ padding: 30px; font-weight: bold; color: var(--gold); letter-spacing: 2px; text-align: center; border-bottom: 1px solid var(--border); }}
        .nav-list {{ flex: 1; overflow-y: auto; }}
        .nav-item {{ padding: 15px 25px; cursor: pointer; display: flex; justify-content: space-between; font-size: 0.9rem; color: #777; }}
        .nav-item:hover {{ background: rgba(255,255,255,0.02); color: #fff; }}
        .nav-item.active {{ color: var(--gold); background: rgba(197,160,89,0.1); border-right: 2px solid var(--gold); }}
        .main {{ flex: 1; padding: 50px; overflow-y: auto; }}
        h1 {{ margin-bottom: 40px; color: #fff; font-weight: 300; font-size: 2rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 30px; }}
        .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; display: flex; height: 160px; cursor: pointer; transition: 0.3s; }}
        .card:hover {{ border-color: var(--gold); transform: translateY(-3px); }}
        .card-img {{ width: 120px; background-size: cover; background-position: center; }}
        .card-body {{ flex: 1; padding: 20px; overflow: hidden; }}
        .card-title {{ color: var(--gold); font-weight: bold; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .card-meta {{ font-size: 0.75rem; color: #555; margin-bottom: 10px; }}
        .card-desc {{ font-size: 0.8rem; line-height: 1.5; color: #888; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
        #modal {{ position: fixed; inset: 0; background: rgba(0,0,0,0.95); z-index: 100; display: none; padding: 40px; }}
        .m-body {{ max-width: 1400px; margin: 0 auto; height: 100%; display: flex; background: #08080a; border: 1px solid var(--gold); border-radius: 20px; overflow: hidden; position: relative; }}
        .m-gal {{ flex: 1.5; background: #000; display: flex; flex-direction: column; border-right: 1px solid var(--border); }}
        .m-view {{ flex: 1; display: flex; align-items: center; justify-content: center; padding: 20px; overflow: hidden; }}
        .m-view img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
        .m-strip {{ height: 100px; display: flex; gap: 10px; padding: 10px; background: rgba(0,0,0,0.5); overflow-x: auto; border-top: 1px solid var(--border); }}
        .m-thumb {{ height: 100%; aspect-ratio: 1; background-size: cover; background-position: center; border: 2px solid transparent; cursor: pointer; opacity: 0.5; }}
        .m-thumb.active {{ opacity: 1; border-color: var(--gold); }}
        .m-info {{ flex: 1; padding: 60px; overflow-y: auto; line-height: 1.8; }}
        .m-info h2 {{ color: var(--gold); margin-bottom: 30px; }}
        .m-close {{ position: absolute; top: 20px; right: 20px; color: #fff; font-size: 2.5rem; cursor: pointer; z-index: 101; }}
    </style>
</head>
<body>
    <div class="sidebar"><div class="logo">ANTIGRAVITY</div><div class="nav-list" id="nav"></div></div>
    <div class="main"><h1 id="title">读取中...</h1><div class="grid" id="grid"></div></div>
    <div id="modal"><div class="m-body"><span class="m-close" onclick="closeM()">&times;</span>
        <div class="m-gal"><div class="m-view"><img id="v-img"></div><div class="m-strip" id="v-strip"></div></div>
        <div class="m-info"><h2 id="v-title"></h2><div id="v-md"></div></div>
    </div></div>
    <script>
        const data = {json.dumps(all_data)};
        const dates = {json.dumps(dates)};
        function init() {{
            const n = document.getElementById('nav');
            dates.forEach(d => {{
                const div = document.createElement('div');
                div.className = 'nav-item';
                div.innerHTML = `<span>${{d.substr(0,4)}}/${{d.substr(4,2)}}/${{d.substr(6,2)}}</span> <span>${{data.filter(x=>x.date===d).length}}</span>`;
                div.onclick = () => showDate(d, div);
                n.appendChild(div);
            }});
            if(dates.length) showDate(dates[0], n.firstChild);
        }}
        function showDate(d, el) {{
            document.querySelectorAll('.nav-item').forEach(i=>i.classList.remove('active'));
            el.classList.add('active');
            document.getElementById('title').innerText = d.substr(0,4)+"/"+d.substr(4,2)+"/"+d.substr(6,2)+" 调教档案";
            const g = document.getElementById('grid'); g.innerHTML = '';
            data.filter(x=>x.date===d).forEach(p => {{
                const c = document.createElement('div'); c.className = 'card';
                c.onclick = () => openM(p);
                c.innerHTML = `<div class="card-img" style="background-image:url('${{p.images[0]||""}}')"></div>
                    <div class="card-body"><div class="card-title">${{p.title}}</div>
                    <div class="card-meta">${{p.time_display}}</div><div class="card-desc">${{p.background}}</div></div>`;
                g.appendChild(c);
            }});
        }}
        function openM(p) {{
            document.getElementById('v-title').innerText = p.title;
            document.getElementById('v-md').innerHTML = p.full_content.replace(/\\n/g,'<br>').replace(/\\*\\*(.*?)\\*\\*/g,'<b style="color:#e54">$1</b>');
            const s = document.getElementById('v-strip'); s.innerHTML = '';
            p.images.forEach((img, i) => {{
                const t = document.createElement('div'); t.className = 'm-thumb'+(i===0?' active':'');
                t.style.backgroundImage = `url('${{img}}')`;
                t.onclick = () => {{
                    document.querySelectorAll('.m-thumb').forEach(x=>x.classList.remove('active'));
                    t.classList.add('active'); document.getElementById('v-img').src = img;
                }};
                s.appendChild(t);
            }});
            document.getElementById('v-img').src = p.images[0] || '';
            document.getElementById('modal').style.display = 'block';
        }}
        function closeM() {{ document.getElementById('modal').style.display = 'none'; }}
        init();
    </script>
</body>
</html>
    """
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f: f.write(html)
    print("V5 Final Generated.")

if __name__ == "__main__": generate_log_v5()
