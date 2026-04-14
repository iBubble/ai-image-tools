
#!/usr/bin/env python3
"""监控 punishments 目录变化，自动更新 index.html"""
import time, os, subprocess, sys

WATCH_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments"
SCRIPT = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/generate_secret_log_v6.py"
PYTHON = "/opt/anaconda3/bin/python3"
COOLDOWN = 5  # 防抖秒数

def get_dir_state(path):
    """获取目录下所有文件的 mtime 快照"""
    state = {}
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                state[fp] = os.path.getmtime(fp)
            except:
                pass
    return state

def sync_to_remote():
    """同步本地 .secret 目录至远程服务器"""
    local_dir = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/"
    remote_host = "gemini-server-Antigravity"
    remote_dir = "/www/wwwroot/ibubble.vicp.net/.secret/"
    
    print(f"[Watcher] 正在同步 {local_dir} -> {remote_host}:{remote_dir} ...")
    
    # 构建 rsync 命令，排除不必要的文件，只同步 punishments 和 index.html
    # 注意：exclude 规则可能会很复杂，这里为了简单直接同步整个 .secret/punishments 和 index.html
    # 或者分开同步两个路径
    
    try:
        # 同步 punishments 目录 (递归)
        cmd_punishments = [
            "rsync", "-avz", 
            "--exclude", ".DS_Store",
            os.path.join(local_dir, "punishments/"),
            f"{remote_host}:{os.path.join(remote_dir, 'punishments/')}"
        ]
        subprocess.run(cmd_punishments, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        
        # 同步 index.html (单独文件)
        cmd_index = [
            "rsync", "-avz",
            os.path.join(local_dir, "index.html"),
            f"{remote_host}:{remote_dir}"
        ]
        subprocess.run(cmd_index, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        
        print("[Watcher] 同步完成 ✅")
    except subprocess.CalledProcessError as e:
        print(f"[Watcher] 同步失败 ❌: {e.stderr.decode().strip() if e.stderr else str(e)}")
    except Exception as e:
        print(f"[Watcher] 同步异常 ❌: {e}")

def main():
    print(f"[Watcher] 开始监控 {WATCH_DIR} ...")
    print(f"[Watcher] 轮询间隔: 3s, 防抖: {COOLDOWN}s")
    
    prev_state = get_dir_state(WATCH_DIR)
    last_rebuild = 0
    
    while True:
        time.sleep(3)
        curr_state = get_dir_state(WATCH_DIR)
        
        if curr_state != prev_state:
            now = time.time()
            if now - last_rebuild >= COOLDOWN:
                # 找出变化的文件
                new_files = set(curr_state.keys()) - set(prev_state.keys())
                changed_files = [f for f in curr_state if f in prev_state and curr_state[f] != prev_state[f]]
                
                ts = time.strftime("%H:%M:%S")
                if new_files:
                    print(f"[Watcher {ts}] 新增: {[os.path.basename(f) for f in new_files]}")
                if changed_files:
                    print(f"[Watcher {ts}] 变更: {[os.path.basename(f) for f in changed_files]}")
                
                print(f"[Watcher {ts}] 正在重建 index.html ...")
                subprocess.run([PYTHON, SCRIPT], capture_output=True)
                print(f"[Watcher {ts}] index.html 已更新 ✅")
                
                # 触发远程同步
                sync_to_remote()
                
                last_rebuild = now
            
            prev_state = curr_state

if __name__ == "__main__":
    main()
