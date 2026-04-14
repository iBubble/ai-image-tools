import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.feishu_notifier import FeishuNotifier

def send_existing_videos():
    COMFY_OUTPUT_DIR = "/Users/gemini/Projects/Own/ComfyUI/output"
    FINAL_OUTPUT_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/outputs/Videos"
    
    notifier = FeishuNotifier()
    mobile = "18008840680"
    open_id = notifier.get_user_id_by_mobile(mobile)
    
    if not open_id:
        print("Failed to get Open ID")
        return
        
    print(f"Ready to push to open_id: {open_id}")
    
    sent_log = os.path.join(FINAL_OUTPUT_DIR, ".sent_to_feishu.log")
    sent_files = set()
    if os.path.exists(sent_log):
        with open(sent_log, "r") as f:
            sent_files = set(f.read().splitlines())
    
    # Push from comfy output directly since they might not be copied yet
    for fname in sorted(os.listdir(COMFY_OUTPUT_DIR)):
        if "HunyuanVideo_Job_" in fname and fname.endswith(".mp4"):
            if fname not in sent_files:
                file_path = os.path.join(COMFY_OUTPUT_DIR, fname)
                print(f"Pushing {fname} to Feishu...")
                
                # Upload
                file_key = notifier.upload_file(file_path, file_type="media") # Feishu stream media
                if not file_key:
                    file_key = notifier.upload_file(file_path, file_type="stream")
                
                if file_key:
                    # Send text context
                    notifier.send_text(open_id, f"✅ 您的视频任务执行完毕：{fname}出锅啦！")
                    # Send media
                    res = notifier.send_file(open_id, file_key)
                    if res:
                        sent_files.add(fname)
                        with open(sent_log, "a") as f:
                            f.write(fname + "\n")
                    time.sleep(2)

if __name__ == "__main__":
    send_existing_videos()
