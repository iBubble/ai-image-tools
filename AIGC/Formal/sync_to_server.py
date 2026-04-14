#!/usr/bin/env python3
import os, subprocess

def sync_to_server():
    date_str = "20260214"
    local_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_str}"
    remote_base = "/www/wwwroot/ibubble.vicp.net/.secret"
    remote_dir = f"{remote_base}/punishments/{date_str}"
    
    print(f"Syncing {local_dir} to {remote_dir}...")
    
    # Use rsync if available for efficiency, otherwise scp
    # First ensure remote dir exists
    subprocess.run(["ssh", "-p", "1022", "gemini@ibubble.vicp.net", f"mkdir -p {remote_dir}"], check=True)
    
    # Sync all files for the day
    # -e 'ssh -p 1022' specifies the port
    try:
        subprocess.run([
            "rsync", "-avz", "-e", "ssh -p 1022",
            local_dir + "/",
            f"gemini@ibubble.vicp.net:{remote_dir}/"
        ], check=True)
    except:
        # Fallback to scp if rsync is missing
        subprocess.run([
            "scp", "-P", "1022", "-r",
            local_dir + "/*",
            f"gemini@ibubble.vicp.net:{remote_dir}/"
        ], check=True)
        
    # Also sync ming.md and index.html
    subprocess.run([
        "scp", "-P", "1022",
        "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/ming.md",
        f"gemini@ibubble.vicp.net:{remote_base}/ming.md"
    ], check=True)
    
    subprocess.run([
        "scp", "-P", "1022",
        "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/index.html",
        f"gemini@ibubble.vicp.net:/www/wwwroot/ibubble.vicp.net/index.html"
    ], check=True)
    
    print("Sync complete!")

if __name__ == "__main__":
    sync_to_server()
