import os
import shutil
import re

source_dir = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos"
target_base_dir = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments"

os.makedirs(target_base_dir, exist_ok=True)

# Corrected regex for matching dates in filenames
date_pattern = re.compile(r"(\d{8})")

if os.path.exists(source_dir):
    files = os.listdir(source_dir)
    for file in files:
        if file.startswith('.'): continue
        match = date_pattern.search(file)
        if match:
            date_str = match.group(1)
            target_dir = os.path.join(target_base_dir, date_str)
            os.makedirs(target_dir, exist_ok=True)
            
            src_path = os.path.join(source_dir, file)
            dst_path = os.path.join(target_dir, file)
            
            print(f"Moving {file} to {date_str}...")
            shutil.move(src_path, dst_path)

print("Reorganization complete.")
