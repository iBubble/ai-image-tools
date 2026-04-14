
import os
import time
import datetime
import subprocess

RECORDS_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/Records"
PROJECT_ROOT = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed"

def get_running_processes():
    try:
        # Check for batch_generate_v2.py
        ps = subprocess.check_output(["ps", "aux"]).decode('utf-8')
        if "batch_generate_v2.py" in ps:
            return "AIGC/batch_generate_v2.py (Running)"
        return "None"
    except:
        return "Unknown"

def record():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    human_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = os.path.join(RECORDS_DIR, f"status_{timestamp}.md")
    
    proc_status = get_running_processes()
    
    content = f"""# 自动工作状态记录 - {human_time}

## 当前状态
- **持续任务**: {proc_status}
- **项目根目录**: {PROJECT_ROOT}

## 任务概况
- 正在执行批量图片生成任务，使用 Pony Diffusion V6 XL 并应用身份锚点。
- 网页交互性修复已完成，待最终验证。
- 身份锚点：Tang Wei 形象，左眼下泪痣，湿发高马尾。

## 备注
- 此记录由自动脚本生成，每10分钟更新一次。
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{human_time}] Status recorded to {filename}")

if __name__ == "__main__":
    if not os.path.exists(RECORDS_DIR):
        os.makedirs(RECORDS_DIR)
        
    while True:
        record()
        time.sleep(600) # 10 minutes
