import os
import shutil
import re

base_dir = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments"
date_pattern = re.compile(r"(\d{8})")

def scan_and_move(current_dir):
    if not os.path.exists(current_dir):
        return
    
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        
        if os.path.isfile(item):
            match = date_pattern.search(item)
            if match:
                date_str = match.group(1)
                target_dir = os.path.join(base_dir, date_str)
                os.makedirs(target_dir, exist_ok=True)
                
                target_path = os.path.join(target_dir, item)
                if item_path != target_path:
                    print(f"Moving {item} to {date_str}/")
                    shutil.move(item_path, target_path)
        elif os.path.isdir(item_path):
            # Recurse into subdirectories (like 20260213) to find misplaced files
            for root, dirs, files in os.walk(item_path):
                for file in files:
                    if file.startswith('.'): continue
                    match = date_pattern.search(file)
                    if match:
                        date_str = match.group(1)
                        target_dir = os.path.join(base_dir, date_str)
                        os.makedirs(target_dir, exist_ok=True)
                        
                        src_path = os.path.join(root, file)
                        dst_path = os.path.join(target_dir, file)
                        
                        if src_path != dst_path:
                            print(f"Relocating {file} to {date_str}/")
                            shutil.move(src_path, dst_path)

if __name__ == "__main__":
    scan_and_move(base_dir)
    # Also scan the base folder in case files are leaking there
    # Cleanup empty folders
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            print(f"Cleaning up empty folder: {folder}")
            os.rmdir(folder_path)

print("Reorganization and cleanup complete.")
