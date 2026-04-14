
import os
import re

html_path = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new JS logic
new_js = """
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
                    // Add ID for potential scrolling and data-title for intersection observer
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
                    html += '<hr>';
                }
                // Normal Text
                else if (line.length > 0) {
                   if (inList) { html += '</ul>'; inList = false; }
                   let content = line;
                   // Bold
                   content = content.replace(/\*\*(.*?)\*\*/g, '<b style="color:#c5a059">$1</b>');
                   // Images
                   content = content.replace(/!\[(.*?)\]\((.*?)\)/g, '<div class="md-img-ref" onclick="findAndScrollToImage(\\'$1\\')">📸 $1</div>');
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
                rootMargin: '-10% 0px -70% 0px',
                threshold: 0
            };

            observer = new IntersectionObserver((entries) => {
                if (isAutoScrolling) return;

                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const title = entry.target.getAttribute('data-title');
                        matchImage(title);
                        
                        document.querySelectorAll('.md-trigger').forEach(h => h.style.color = '');
                        entry.target.style.color = '#c5a059'; 
                    }
                });
            }, options);

            document.querySelectorAll('.md-trigger').forEach(h => observer.observe(h));
        }

        function matchImage(title) {
           const thumbs = document.querySelectorAll('.m-thumb');
           let foundIndex = -1;
           const cleanTitle = title.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, ''); 
           
           thumbs.forEach((thumb, i) => {
               const label = thumb.getAttribute('data-label') || '';
               const cleanLabel = label.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '');
               
               if (cleanLabel.includes(cleanTitle) || cleanTitle.includes(cleanLabel)) {
                   foundIndex = i;
               }
           });

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
                     // IMPORTANT: Passing false to avoid loop if click handler calls scroll
                     // Actually click handler is what we trigger. 
                     // We need to differentiate user click vs auto switch.
                     // But here we rely on the click handler to update the view.
                     thumbs[index].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
                }
            }
        }
        
        // Scroll text to header matching the image label
        function scrollTextToMatchImage(label) {
            const headers = document.querySelectorAll('.md-trigger');
            let targetHeader = null;
            const cleanLabel = label.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '');
            
            for (let h of headers) {
                 const title = h.getAttribute('data-title');
                 const cleanTitle = title.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '');
                 if (cleanLabel.includes(cleanTitle) || cleanTitle.includes(cleanLabel)) {
                     targetHeader = h;
                     break;
                 }
            }
            
            if (targetHeader) {
                isAutoScrolling = true;
                targetHeader.scrollIntoView({ behavior: 'smooth', block: 'center' });
                document.querySelectorAll('.md-trigger').forEach(h => h.style.color = '');
                targetHeader.style.color = '#c5a059';
                setTimeout(() => isAutoScrolling = false, 1000);
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
                
                const tip = document.createElement('div'); 
                tip.className = 'tip'; 
                tip.innerText = imgObj.label;
                t.appendChild(tip);
                
                t.onclick = (e) => {
                    // Check if this was a programmatic click (from scroll spy) or user click
                    // But we can't easily distinguish event source here without custom args.
                    // Instead, we check the global isAutoScrolling flag? 
                    // No, click() triggers this synchronously.
                    
                    document.querySelectorAll('.m-thumb').forEach(x => x.classList.remove('active'));
                    t.classList.add('active');
                    document.getElementById('v-img').src = imgObj.path;
                    label.innerText = imgObj.label;
                    
                    // Only scroll text if NOT auto-scrolling (meaning user clicked image)
                    // If isAutoScrolling is true, it means the scroll spy triggered this image switch
                    // So we DON'T want to scroll the text again (circular loop).
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
            
            document.getElementById('modal').style.display = 'block';
            
            if (!document.getElementById('md-style')) {
                const st = document.createElement('style');
                st.id = 'md-style';
                st.textContent = `
                    .md-trigger { cursor: pointer; transition: 0.2s; border-bottom: 1px dashed #333; display: inline-block; }
                    .md-trigger:hover { color: #c5a059 !important; border-bottom-color: #c5a059; }
                    .md-img-ref { cursor: pointer; color: #666; font-size: 0.8em; margin: 5px 0; }
                    .md-img-ref:hover { color: #c5a059; }
                    .m-info h3 { margin-top: 30px; margin-bottom: 15px; font-size: 1.3em; color: #ddd; }
                    .m-info h2 { border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 40px; }
                    .m-info ul { padding-left: 20px; color: #999; }
                    .m-info p { margin-bottom: 10px; line-height: 1.6; }
                `;
                document.head.appendChild(st);
            }
            
            setTimeout(initScrollSpy, 100);
        }
"""

pattern = r"function openM\(p\) \{[\s\S]*?(?=function closeM\(\))"

if re.search(pattern, content):
    new_content = re.sub(pattern, new_js, content)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully patched index.html with bidirectional sync logic.")
else:
    print("Could not find openM function to patch.")
