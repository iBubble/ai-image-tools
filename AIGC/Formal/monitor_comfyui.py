import time
import subprocess
import re
import os

LOG_FILE = "/Users/gemini/Projects/Own/ComfyUI/comfy_i2v_run.log"

def notify(msg, title="Video Render Status"):
    script = f'display notification "{msg}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

def get_latest_progress():
    try:
        with open(LOG_FILE, "rb") as f:
            # Read last chunk to handle long lines
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(size - 4096, 0))
            content = f.read().decode("utf-8", errors="replace")
            
            # Split by either \r or \n
            parts = re.split(r'[\r\n]+', content)
            
            for line in reversed(parts):
                # Pattern matching: 17%|...| 5/30 [08:46<43:21, 104.06s/it]
                match = re.search(r"(\d+)%\|.*?\|\s*(\d+)/(\d+)\s+\[.*?<(.*?)(?:,\])", line)
                
                # Sometime there is no comma if it's completed? 
                # Let's use a simpler pattern just tracking the numbers
                # e.g.: 5/30 [08:46<43:21,
                match = re.search(r"(\d+)/(\d+)\s+\[([^<]+)<([^,]+)", line)
                if match:
                    step = int(match.group(1))
                    total = int(match.group(2))
                    elapsed = match.group(3)
                    eta = match.group(4)
                    return step, total, eta
    except Exception as e:
        pass
    return None, None, None

notify("后端进程监控已启动，将在后台实时播报渲染进度！")
last_notified_step = -1

while True:
    step, total, eta = get_latest_progress()
    if step is not None:
        # Notify at specific steps or if it has progressed by at least 3 steps since last notification
        if step > last_notified_step and (step % 5 == 0 or step == total or last_notified_step == -1):
            last_notified_step = step
            percent = int((step / total) * 100)
            
            if step == total:
                notify(f"渲染 100% 结束！即将进入输出编码阶段", "🎉 Hunyuan 渲染已全部推演完成")
                break
            else:
                notify(f"当前推演进度: {percent}% ({step}/{total})\\n剩余预估耗时: {eta}", "📺 Hunyuan 新影片演算中")
            
    time.sleep(15)
