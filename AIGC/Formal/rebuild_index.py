
import os
import json
import re

# Base directory for punishments (relative to index.html)
PUNISHMENT_BASE_REL = "punishments"
# Absolute path to punishments directory
PUNISHMENT_BASE_ABS = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments"
# Path to index.html
INDEX_PATH = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/index.html"

def scan_punishments():
    all_data = []
    
    # Walk through date folders
    for date_dir in sorted(os.listdir(PUNISHMENT_BASE_ABS), reverse=True):
        full_date_path = os.path.join(PUNISHMENT_BASE_ABS, date_dir)
        if not os.path.isdir(full_date_path):
            continue
            
        # Look for markdown files inside
        for file in sorted(os.listdir(full_date_path), reverse=True):
            if file.endswith(".md"):
                md_path = os.path.join(full_date_path, file)
                
                # Parse markdown for info
                entry = parse_markdown(md_path, date_dir)
                if entry:
                    all_data.append(entry)
                    
    return all_data

def parse_markdown(md_path, date_str):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Title (First H1)
    title_match = re.search(r'^#\s*(.*?)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "无标题惩罚"

    # Extract Timestamp from filename or content
    # Filename format: xiao_ni_<timestamp>_...
    filename = os.path.basename(md_path)
    ts_match = re.search(r'xiao_ni_(\d{12})', filename)
    timestamp = ts_match.group(1) if ts_match else date_str + "0000"
    
    # Priority for full records
    if "完整记录" in filename or "Full" in filename or "integrated" in filename.lower():
        timestamp = date_str + "9999"

    # Extract Images
    # We want to find all image references in the markdown.
    images = []
    # 1. Standard markdown images: ![label](path)
    img_matches = re.finditer(r'!\[(.*?)\]\((.*?)\)', content)
    for m in img_matches:
        label, path = m.group(1), m.group(2)
        images.append((label, path))
        
    # 2. Links that look like images: [label](path.jpg)
    link_matches = re.finditer(r'\[(.*?)\]\((.*?\.(?:jpg|jpeg|png|webp|gif|bmp).*?)\)', content, re.IGNORECASE)
    for m in link_matches:
        label, path = m.group(1), m.group(2)
        if not any(img[1] == path for img in images):
            images.append((label, path))
            
    # 3. Specific formatted references: **照片**: [label](path) or **照片**: ![label](path)
    txt_matches = re.finditer(r'\*\*照片\*\*:\s*(?:!\[|\[)(.*?)\]\((.*?)\)', content, re.IGNORECASE)
    for m in txt_matches:
        label, path = m.group(1), m.group(2)
        if not any(img[1] == path for img in images):
            images.append((label or path, path))
            
    # 4. Raw file paths in backticks: `path.jpg`
    backtick_matches = re.finditer(r'`([\w/\.-]+\.(?:jpg|jpeg|png|webp|gif))`', content, re.IGNORECASE)
    for m in backtick_matches:
        path = m.group(1)
        if not any(img[1] == path for img in images):
            images.append((path, path))

    final_images = []
    for label, path in images:
        label = label.strip()
        path = path.strip().strip('`').strip()
        
        # If path is a full file URI
        if path.startswith("file://"):
             # Extract the part after .secret/ or the last part of the path
             if "/.secret/" in path:
                 path = path.split("/.secret/")[-1]
             else:
                 path = path.replace("file://", "").split("/")[-1]
                 path = f"punishments/{date_str}/{path}"
        
        # If it's an absolute path
        if path.startswith("/Users/"):
             if "/.secret/" in path:
                 path = path.split("/.secret/")[-1]
             else:
                 path = path.split("/")[-1]
                 path = f"punishments/{date_str}/{path}"
        
        # If it's just a filename (no slash)
        if "/" not in path:
             path = f"punishments/{date_str}/{path}"
             
        # Normalize: remove leading .secret/ if present
        if path.startswith(".secret/"):
            path = path.replace(".secret/", "", 1)
        path = path.lstrip("/")

        if path.lower().endswith(('.jpg', '.png', '.jpeg', '.webp', '.gif')):
             final_images.append({"path": path, "label": label})

    # Summary logic: first 200 chars of non-header text.
    clean_text = re.sub(r'#.*', '', content) # Remove headers
    clean_text = re.sub(r'!\[.*?\]\(.*?\)', '', clean_text) # Remove images
    clean_text = re.sub(r'\*\*.*?\*\*', '', clean_text) # Remove bold
    clean_text = clean_text.strip()
    background = clean_text[:150].replace('\n', ' ') + "..." if len(clean_text) > 150 else clean_text
    
    return {
        "title": title,
        "timestamp": timestamp,
        "time_display": f"{timestamp[8:10]}:{timestamp[10:12]}",
        "background": background,
        "full_content": content,
        "images": final_images,
        "date": date_str
    }

def rebuild_index(data):
    # Sort data by timestamp descending
    data.sort(key=lambda x: x['timestamp'], reverse=True)
    
    json_str = json.dumps(data, ensure_ascii=False)
    
    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ANTIGRAVITY | 调教执行日志</title>
    <style>
        :root { --gold: #c5a059; --bg: #050508; --side: #0c0c10; --card: #121218; --border: rgba(255, 255, 255, 0.08); }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--side); }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #555; }
        body { background: var(--bg); color: #ccc; font-family: sans-serif; display: flex; height: 100vh; overflow: hidden; }
        .sidebar { width: 240px; background: var(--side); border-right: 1px solid var(--border); display: flex; flex-direction: column; }
        .logo { padding: 30px; font-weight: bold; color: var(--gold); letter-spacing: 2px; text-align: center; border-bottom: 1px solid var(--border); }
        .nav-list { flex: 1; overflow-y: auto; }
        .nav-item { padding: 15px 25px; cursor: pointer; display: flex; justify-content: space-between; font-size: 0.9rem; color: #777; transition: 0.2s; }
        .nav-item:hover { background: rgba(255, 255, 255, 0.02); color: #fff; }
        .nav-item.active { color: var(--gold); background: rgba(197, 160, 89, 0.1); border-right: 2px solid var(--gold); }
        .main { flex: 1; padding: 50px; overflow-y: auto; }
        h1 { margin-bottom: 40px; color: #fff; font-weight: 300; font-size: 2rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 30px; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; display: flex; height: 160px; cursor: pointer; transition: 0.3s; overflow: hidden; }
        .card:hover { border-color: var(--gold); transform: translateY(-3px); }
        .card-img { width: 120px; background-size: cover; background-position: center; flex-shrink: 0; }
        .card-body { flex: 1; padding: 20px; overflow: hidden; display: flex; flex-direction: column; }
        .card-title { color: var(--gold); font-weight: bold; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 0.95rem; }
        .card-meta { font-size: 0.75rem; color: #555; margin-bottom: 8px; }
        .card-desc { font-size: 0.8rem; line-height: 1.5; color: #888; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
        
        /* Modal */
        #modal { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.9); z-index: 100; display: none; justify-content: center; align-items: center; padding: 4vh; }
        .m-body { max-width: 1600px; width: 100%; height: 100%; display: flex; background: #08080a; border: 1px solid var(--gold); border-radius: 12px; overflow: hidden; position: relative; box-shadow: 0 0 50px rgba(0,0,0,0.8); }
        .m-gal { flex: 1.5; min-width: 0; background: #000; display: flex; flex-direction: column; border-right: 1px solid var(--border); }
        .m-view { flex: 1; min-height: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; overflow: hidden; position: relative; }
        .m-view img { max-width: 100%; max-height: 100%; object-fit: contain; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .img-label { color: var(--gold); font-size: 0.9rem; margin-top: 10px; text-align: center; min-height: 20px; letter-spacing: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 90%; }
        .m-strip { height: 120px; display: flex; gap: 10px; padding: 15px; background: rgba(10, 10, 12, 0.9); overflow-x: auto; overflow-y: hidden; border-top: 1px solid var(--border); white-space: nowrap; scroll-behavior: smooth; }
        .m-thumb { height: 100%; aspect-ratio: 1; background-size: cover; background-position: center; border: 2px solid transparent; cursor: pointer; opacity: 0.4; position: relative; transition: 0.2s; border-radius: 4px; flex-shrink: 0; }
        .m-thumb:hover { opacity: 0.8; }
        .m-thumb.active { opacity: 1; border-color: var(--gold); box-shadow: 0 0 10px rgba(197, 160, 89, 0.3); }
        .m-info { flex: 1; min-width: 400px; padding: 40px; overflow-y: auto; line-height: 1.8; color: #aaa; font-size: 0.95rem; background: var(--side); }
        .m-info h2 { color: var(--gold); margin-bottom: 20px; font-size: 1.4rem; border-bottom: 1px solid #333; padding-bottom: 15px; }
        .m-info h3 { color: #ddd; margin-top: 25px; margin-bottom: 10px; font-size: 1.1rem; }
        .m-info p { margin-bottom: 15px; }
        .m-info ul { padding-left: 20px; margin-bottom: 15px; color: #888; }
        .m-info li { margin-bottom: 5px; }
        .m-close { position: absolute; top: 15px; right: 20px; color: #666; font-size: 2rem; cursor: pointer; z-index: 101; transition: 0.2s; line-height: 1; background: rgba(0,0,0,0.5); width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
        .m-close:hover { color: #fff; background: rgba(0,0,0,0.8); }

        /* Markdown Styles */
        .md-trigger { cursor: pointer; transition: 0.2s; border-bottom: 1px dashed #444; display: inline-block; }
        .md-trigger:hover { color: var(--gold); border-bottom-color: var(--gold); }
        .md-img-ref { cursor: pointer; color: #666; font-size: 0.85rem; margin: 10px 0; padding: 5px 10px; background: rgba(255,255,255,0.03); border-radius: 4px; display: inline-block; }
        .md-img-ref:hover { color: var(--gold); background: rgba(255,255,255,0.05); } 
        b { color: #ddd; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">ANTIGRAVITY</div>
        <div class="nav-list" id="nav"></div>
    </div>
    <div class="main">
        <h1 id="title">读取中...</h1>
        <div class="grid" id="grid"></div>
    </div>
    <div id="modal">
        <div class="m-body"><span class="m-close" onclick="closeM()">&times;</span>
            <div class="m-gal">
                <div class="m-view"><img id="v-img"><div class="img-label" id="v-label"></div></div>
                <div class="m-strip" id="v-strip"></div>
            </div>
            <div class="m-info">
                <h2 id="v-title"></h2>
                <div id="v-md"></div>
            </div>
        </div>
    </div>
    <script>
        const data = __DATA_JSON__;

        function init() {
            const dates = [...new Set(data.map(p => p.date))];
            const nav = document.getElementById('nav');
            if (dates.length === 0) {
                 document.getElementById('title').innerText = "暂无惩罚记录";
                 return;
            }
            dates.forEach(d => {
                const el = document.createElement('div'); el.className = 'nav-item';
                el.innerText = d.substr(0, 4) + "/" + d.substr(4, 2) + "/" + d.substr(6, 2);
                el.onclick = () => showDate(d, el);
                nav.appendChild(el);
            });
            if (nav.children.length > 0) showDate(dates[0], nav.children[0]);
        }

        function showDate(d, el) {
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            el.classList.add('active');
            document.getElementById('title').innerText = d.substr(0, 4) + "/" + d.substr(4, 2) + "/" + d.substr(6, 2) + " 调教档案";
            const g = document.getElementById('grid'); g.innerHTML = '';
            
            const dayData = data.filter(x => x.date === d);
            if (dayData.length === 0) {
                g.innerHTML = '<div style="color:#666; padding:20px;">无数据</div>';
                return;
            }

            dayData.forEach(p => {
                const c = document.createElement('div'); c.className = 'card';
                c.onclick = () => openM(p);
                const thumbPath = p.images.length > 0 ? p.images[0].path : '';
                c.innerHTML = `<div class="card-img" style="background-image:url('${thumbPath}')"></div>
                    <div class="card-body"><div class="card-title">${p.title}</div>
                    <div class="card-meta">${p.time_display}</div><div class="card-desc">${p.background}</div></div>`;
                g.appendChild(c);
            });
        }

        // Markdown Renderer & Scroll Spy Logic
        function renderMarkdown(text) {
            let lines = text.split('\\n');
            let html = '';
            let inList = false;
            
            lines.forEach((line, index) => {
                line = line.trim();
                // Headers level 3 (Scenes)
                if (line.startsWith('### ')) {
                    if (inList) { html += '</ul>'; inList = false; }
                    const title = line.replace('### ', '').trim();
                    html += `<h3 class="md-trigger" id="md-h3-${index}" data-title="${title}" onclick="scrollToHeader(this)">${title}</h3>`;
                }
                // Headers level 2 (Chapters)
                else if (line.startsWith('## ')) {
                    if (inList) { html += '</ul>'; inList = false; }
                    html += `<h2>${line.replace('## ', '').trim()}</h2>`;
                }
                // Lists
                else if (line.startsWith('- ')) {
                    if (!inList) { html += '<ul>'; inList = true; }
                    html += `<li>${line.replace('- ', '').trim()}</li>`;
                }
                // Horizontal Rule
                else if (line.startsWith('---')) {
                    if (inList) { html += '</ul>'; inList = false; }
                    html += '<hr style="border:0; border-top:1px solid #333; margin:20px 0;">';
                }
                // Normal Text
                else if (line.length > 0) {
                   if (inList) { html += '</ul>'; inList = false; }
                   let content = line;
                    content = content.replace(/\\*\\*(.*?)\\*\\*/g, '<b style="color:#c5a059">$1</b>');
                    // Hide **照片**: prefix if followed by an image or backtick ref
                    content = content.replace(/<b style="color:#c5a059">照片<\\/b>:\\s*/g, '');
                    
                    content = content.replace(/!\\[(.*?)\\]\\((.*?)\\)/g, (m, p1, p2) => {
                        const cleanP1 = p1.replace(/'/g, "\\\\'");
                        return `<div class="md-img-container"><img src="${p2}" alt="${p1}" onclick="findAndScrollToImage('${cleanP1}')" style="max-width:280px; cursor:pointer; display:block; margin:15px 0; border:1px solid #333; transition:0.3s;" onmouseover="this.style.borderColor='var(--gold)'" onmouseout="this.style.borderColor='#333'"></div>`;
                    });
                    content = content.replace(/`([\\w/\\.-]+\\.(?:jpg|png|jpeg|webp|gif))`|📸\\s*([\\w/\\.-]+\\.(?:jpg|png|jpeg|webp|gif))/gi, (m, p1, p2) => {
                        const path = p1 || p2;
                        return `<div class="md-img-ref" onclick="findAndScrollToImage('${path}')">📸 ${path}</div>`;
                    });
                   html += `<p>${content}</p>`;
                } else {
                    if (inList) { html += '</ul>'; inList = false; }
                }
            });
            if (inList) { html += '</ul>'; }
            return html;
        }

        let observer = null;
        let isAutoScrolling = false;

        function initScrollSpy() {
            if (observer) observer.disconnect();
            
            const options = {
                root: document.querySelector('.m-info'),
                rootMargin: '-5% 0px -85% 0px',
                threshold: 0
            };

            observer = new IntersectionObserver((entries) => {
                if (isAutoScrolling) return;

                // Sort entry by top position to handle multiple entries
                const intersect = entries.filter(e => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
                
                if (intersect.length > 0) {
                    const entry = intersect[0];
                    const title = entry.target.getAttribute('data-title');
                    
                    document.querySelectorAll('.md-trigger').forEach(h => h.style.color = '');
                    entry.target.style.color = '#c5a059'; 
                    
                    matchImage(title);
                }
            }, options);

            document.querySelectorAll('.md-trigger').forEach(h => observer.observe(h));
        }

        function matchImage(title) {
           if (!title) return;
           const thumbs = document.querySelectorAll('.m-thumb');
           let foundIndex = -1;
           const cleanTitle = title.replace(/[^\\u4e00-\\u9fa5]/g, ''); // Fix: only match Chinese for better accuracy in this case
           
           if (!cleanTitle || cleanTitle.length < 2) return;

           for (let i = 0; i < thumbs.length; i++) {
               const label = thumbs[i].getAttribute('data-label') || '';
               const cleanLabel = label.replace(/[^\\u4e00-\\u9fa5]/g, '');
               
               if (cleanLabel.includes(cleanTitle) || cleanTitle.includes(cleanLabel)) {
                   foundIndex = i;
                   break; 
               }
           }

           if (foundIndex !== -1) {
               switchImage(foundIndex);
           }
        }
        
        function switchImage(index) {
            const thumbs = document.querySelectorAll('.m-thumb');
            if (thumbs[index]) {
                const active = document.querySelector('.m-thumb.active');
                if (active !== thumbs[index]) {
                     thumbs[index].click(); 
                     thumbs[index].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
                }
            }
        }
        
        function scrollTextToMatchImage(label) {
            const headers = document.querySelectorAll('.md-trigger');
            let targetHeader = null;
            const cleanLabel = label.replace(/[^\\u4e00-\\u9fa5]/g, '');
            if (!cleanLabel || cleanLabel.length < 2) return;
            
            for (let h of headers) {
                 const title = h.getAttribute('data-title');
                 if (!title) continue;
                 const cleanTitle = title.replace(/[^\\u4e00-\\u9fa5]/g, '');
                 if (cleanLabel.includes(cleanTitle) || cleanTitle.includes(cleanLabel)) {
                     targetHeader = h;
                     break;
                 }
            }
            
            if (targetHeader) {
                isAutoScrolling = true;
                targetHeader.scrollIntoView({ behavior: 'smooth', block: 'start' });
                document.querySelectorAll('.md-trigger').forEach(h => { h.style.transition = '0.5s'; h.style.color = ''; });
                targetHeader.style.color = '#c5a059';
                setTimeout(() => isAutoScrolling = false, 800);
            }
        }
        
        function scrollToHeader(el) {
             isAutoScrolling = true;
             el.scrollIntoView({ behavior: 'smooth', block: 'start' });
             matchImage(el.getAttribute('data-title'));
             setTimeout(() => isAutoScrolling = false, 1000);
        }
        
        function findAndScrollToImage(altText) {
             matchImage(altText);
        }

        function openM(p) {
            document.getElementById('v-title').innerText = p.title;
            document.getElementById('v-md').innerHTML = renderMarkdown(p.full_content);
            
            const s = document.getElementById('v-strip'); 
            s.innerHTML = '';
            const label = document.getElementById('v-label');
            
            p.images.forEach((imgObj, i) => {
                const t = document.createElement('div'); 
                t.className = 'm-thumb';
                t.style.backgroundImage = `url('${imgObj.path}')`;
                t.setAttribute('data-label', imgObj.label);
                
                t.onclick = (e) => {
                    document.querySelectorAll('.m-thumb').forEach(x => x.classList.remove('active'));
                    t.classList.add('active');
                    document.getElementById('v-img').src = imgObj.path;
                    label.innerText = imgObj.label;
                    
                    if (!isAutoScrolling) {
                        scrollTextToMatchImage(imgObj.label);
                    }
                };
                s.appendChild(t);
            });
            
            if (p.images.length > 0) {
                document.getElementById('v-img').src = p.images[0].path;
                label.innerText = p.images[0].label;
                if(s.children[0]) s.children[0].classList.add('active');
            }
            
            document.getElementById('modal').style.display = 'flex';
            setTimeout(initScrollSpy, 100);
        }
        
        function closeM() { document.getElementById('modal').style.display = 'none'; }
        
        init();
    </script>
</body>
</html>"""
    
    final_html = html_template.replace("__DATA_JSON__", json_str)
    
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print("Rebuilt index.html successfully.")

if __name__ == "__main__":
    current_data = scan_punishments()
    rebuild_index(current_data)
