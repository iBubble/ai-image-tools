
import os
import subprocess

# Config
REMOTE_HOST = "ibubble.vicp.net"
REMOTE_PORT = "1022"
REMOTE_USER = "gemini"
REMOTE_DIR_BASE = "/www/wwwroot/ibubble.vicp.net/.secret"
LOCAL_DIR_BASE = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret"

# 1. Upload Images
local_img_dir = os.path.join(LOCAL_DIR_BASE, "punishments/20260214")
remote_img_dir = f"{REMOTE_DIR_BASE}/punishments/20260214"

# We only want to upload the new batch images
# Pattern: xiao_ni_202602140128_ch*.jpg
command_img = [
    "scp", "-P", REMOTE_PORT,
    f"{local_img_dir}/xiao_ni_202602140128_ch*.jpg",
    f"{REMOTE_USER}@{REMOTE_HOST}:{remote_img_dir}/"
]

print("Uploading new images...")
# Using shell=True for wildcard expansion
subprocess.run(" ".join(command_img), shell=True)

# 2. Upload Markdown
local_md = os.path.join(local_img_dir, "xiao_ni_202602140128_双人虐待惩罚_完整记录.md")
command_md = [
    "scp", "-P", REMOTE_PORT,
    local_md,
    f"{REMOTE_USER}@{REMOTE_HOST}:{remote_img_dir}/"
]
print("Uploading Markdown...")
subprocess.run(command_md)

# 3. Upload index.html
local_html = os.path.join(LOCAL_DIR_BASE, "index.html")
command_html = [
    "scp", "-P", REMOTE_PORT,
    local_html,
    f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_DIR_BASE}/"
]
print("Uploading index.html...")
subprocess.run(command_html)

print("All Done! Check the website.")
