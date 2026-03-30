import os
import random
import time
import requests

TARGET_DIRS = [
    "/Volumes/macData/Downloads/ComfyUI/HardCore",
    "/Volumes/macData/Downloads/ComfyUI/SourcePics"
]

CHARS = ['xiaoni', 'xiaoai', 'xiaoli']

def main():
    print("🚀 开始后台精修任务...")
    for d in TARGET_DIRS:
        if not os.path.exists(d):
            print(f"❌ 目录不存在: {d}")
            continue
            
        print(f"📂 扫描目录: {d}")
        for root, dirs, files in os.walk(d):
            for file in files:
                if not file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    continue
                fpath = os.path.join(root, file)
                print(f"\n📸 处理图片: {file}")
                
                # 1. 上传图片到 Image Studio (这一步也可以避免污染原始路径)
                try:
                    with open(fpath, "rb") as f:
                        r = requests.post("http://127.0.0.1:5050/api/upload", files={"file": f})
                    
                    if r.status_code != 200 or not r.json().get("ok"):
                        print(f"  ❌ 上传失败: {r.text}")
                        continue
                        
                    up_filename = r.json()["filename"]
                except Exception as e:
                    print(f"  ❌ 上传请求异常: {e}")
                    continue
                
                # 2. 提交精修 (调用 api/refine)
                # app.py 里面的 denoise 为 auto 就会自动走我们刚刚上的 CLIP 模型
                c = random.choice(CHARS)
                payload = {
                    "filename": up_filename,
                    "character": c,
                    "camera": "moody",
                    "denoise": "auto",
                    "scene_prompt": "",
                    "seed": -1
                }
                print(f"  🔄 提交精修 (随机扮演: {c})...")
                try:
                    # ComfyUI 处理一张图可能需要 30～100秒，设个10分钟的大时限
                    ref = requests.post("http://127.0.0.1:5050/api/refine", json=payload, timeout=600)
                    if ref.status_code == 200:
                        data = ref.json()
                        if data.get("error"):
                            print("  ❌ 精修报错: ", data["error"])
                        else:
                            print(f"  ✅ 精修成功! 识别类型: {data.get('img_type')}, Denoise: {data.get('denoise')}")
                    else:
                        print(f"  ❌ 精修失败 (HTTP {ref.status_code}): ", ref.text)
                except Exception as e:
                    print(f"  ❌ 精修请求超时或异常: {e}")
                
                # 防止请求过猛，休息 3 秒
                time.sleep(3)
                
    print("\n🎉 所有目录扫描处理完毕！")

if __name__ == "__main__":
    main()
