import requests
import json

CIVITAI_API_KEY = "483685b6d52d7084198cfd79394e67e8"
headers = {"Authorization": f"Bearer {CIVITAI_API_KEY}"}

def search_civitai(query):
    url = "https://civitai.com/api/v1/models"
    params = {
        "query": query,
        "limit": 10,
        "sort": "Highest Rated",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Civitai error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

print("=== 正在查询 Civitai LTX-Video NSFW ===")
items = search_civitai("LTX Video NSFW")
for item in items:
    if "LTX" in str(item.get("tags", [])) or "LTX" in item.get("name", ""):
        print(f"Found LTX: {item.get('name')} | URL: https://civitai.com/models/{item.get('id')}")
        v = item.get("modelVersions")
        if v:
            print(f"  --> DL: {v[0].get('downloadUrl')}?token=[HIDDEN]")

print("\n=== 正在查询 Civitai HunyuanVideo NSFW ===")
items = search_civitai("Hunyuan Video NSFW")
for item in items:
    if "Hunyuan" in str(item.get("tags", [])) or "Hunyuan" in item.get("name", "") or "hunyuan" in item.get("name", "").lower():
        print(f"Found Hunyuan: {item.get('name')} | URL: https://civitai.com/models/{item.get('id')}")
        v = item.get("modelVersions")
        if v:
            if v[0].get("downloadUrl"):
                print(f"  --> DL: {v[0].get('downloadUrl')}?token=[HIDDEN]")


print("\n=== 检查 Kijai 的 VAE 目录 (适配 ComfyUI 的版本) ===")
hf_api_url = "https://huggingface.co/api/models/Kijai/HunyuanVideo_comfy/tree/main"
hf_res = requests.get(hf_api_url)
if hf_res.status_code == 200:
    for x in hf_res.json():
        if "vae" in x['path'].lower():
            print("FOUND VAE:", x['path'])
else:
    print("Failed to query Kijai repo.")

print("\n=== 检查原厂 Tencent 的 VAE 目录 ===")
hf_api_url2 = "https://huggingface.co/api/models/tencent/HunyuanVideo/tree/main"
hf_res2 = requests.get(hf_api_url2)
if hf_res2.status_code == 200:
    for x in hf_res2.json():
        print("FOUND ROOT ITEM:", x['path'])
