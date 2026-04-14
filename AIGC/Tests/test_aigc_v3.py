import requests
import os
import json
import time

# 定义提示词
PROMPT = (
    "A photorealistic portrait of a stunning 20-year-old Chinese woman, Xiao Ai, with long messy black hair and blushing cheeks. "
    "She is kneeling in a dark, futuristic industrial server room with neon blue ambient lighting. "
    "She wears revealing black lace lingerie and vibrant red silk stockings with high heels. "
    "Sweat glistens on her skin, expressive submissive eyes looking at viewer, cinematic lighting, ultra-high resolution, 8k, highly detailed textures."
)

def test_ai_horde():
    print("\n[测试] AI Horde (匿名模式)")
    # 使用 0000000000 作为匿名 key
    url = "https://stablehorde.net/api/v2/generate/async"
    payload = {
        "prompt": PROMPT,
        "models": ["SDXL_Turbo", "AlbedoBase XL (SDXL)", "RealVisXL"],
        "params": {
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "steps": 25
        }
    }
    headers = {"apikey": "0000000000", "Client-Agent": "XiaoAiTester:1.0:me@example.com"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code == 202:
            job_id = r.json().get("id")
            print(f"任务提交成功, ID: {job_id}. 正在等待生成...")
            # 轮询状态
            for _ in range(10):
                time.sleep(10)
                status_url = f"https://stablehorde.net/api/v2/generate/check/{job_id}"
                sr = requests.get(status_url, timeout=10)
                if sr.json().get("done"):
                    print("生成完成！正在获取图片...")
                    status_url = f"https://stablehorde.net/api/v2/generate/status/{job_id}"
                    final_r = requests.get(status_url, timeout=10)
                    img_url = final_r.json()["generations"][0]["img"]
                    # 下载
                    img_data = requests.get(img_url).content
                    with open("results/horde_high_res.webp", "wb") as f:
                        f.write(img_data)
                    print(f"✅ AI Horde 成功: results/horde_high_res.webp")
                    return True
                else:
                    print(f"进度: {sr.json().get('wait_time')}s 剩余...")
        else:
            print(f"❌ AI Horde 失败: {r.text}")
    except Exception as e:
        print(f"❌ AI Horde 异常: {e}")
    return False

def test_airforce_json():
    print("\n[测试] Airforce (JSON 解析模式)")
    # 尝试多种模型和参数
    url = f"https://api.airforce/v1/image/generations?prompt={PROMPT.replace(' ', '%20')}&model=flux-realism"
    try:
        r = requests.get(url, timeout=30)
        # 如果返回的是 JSON，解析它
        try:
            data = r.json()
            print(f"获取到 JSON: {data}")
            img_url = data.get("url") or data.get("images", [{}])[0].get("url")
            if img_url:
                img_data = requests.get(img_url).content
                with open("results/airforce_json_fixed.jpg", "wb") as f:
                    f.write(img_data)
                print("✅ Airforce JSON 模式成功")
        except:
            print("返回内容不是 JSON，可能是之前的 HTML 公告。")
    except:
        pass

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    # test_ai_horde() # 轮询太慢，先试别的
    test_airforce_json()
