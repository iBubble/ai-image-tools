import requests
import os
import time
import json
import base64

# --- 参考标准：Mage AnyDark 风格 ---
# 目标：正面全身，面部保真（无畸变），暗色机房光影，照片级肤质
# 关键策略：
# 1. 使用 Horde 上写实性能最强的 ICBINP / Juggernaut XL / AbsoluteReality 模型
# 2. 精心调配负向提示词，确保面部不崩坏
# 3. 同时提交多个模型任务，谁先完成用谁

PROMPT = (
    "(best quality, masterpiece, ultra-detailed, photorealistic:1.4), "
    "(beautiful 20 year old Chinese woman, Xiao Ai:1.3), "
    "full body portrait, facing viewer directly, "
    "kneeling on floor in dark server room with cool blue LED ambient light, "
    "long messy black hair cascading over shoulders, "
    "blushing cheeks, slightly parted lips, expressive vulnerable eyes looking at camera, "
    "(completely nude:1.3), detailed realistic body proportions, "
    "glistening sweat on collarbones and chest, "
    "wearing only black high heels, "
    "dramatic cinematic lighting, volumetric fog, deep shadows, "
    "(8k, RAW photo, Nikon D850, 85mm f/1.4:1.2), "
    "extremely detailed skin texture with visible pores"
)

NEGATIVE = (
    "(worst quality, low quality:1.4), deformed face, distorted eyes, "
    "bad anatomy, extra limbs, extra fingers, mutated hands, "
    "poorly drawn face, ugly, blurry, text, watermark, logo, "
    "bad proportions, malformed limbs, fused fingers, "
    "cross-eyed, asymmetric eyes, "
    "cartoon, anime, 3d render, digital art, painting, illustration"
)

RESULTS_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/secret_results"
HORDE_API = "https://stablehorde.net/api/v2"

# 选择写实性能最高且当前有活跃 GPU 的模型
MODEL_CONFIGS = [
    {
        "name": "ICBINP XL",
        "file": "icbinp_xl_frontal.webp",
        "params": {"cfg_scale": 7, "height": 1024, "width": 768, "steps": 30, "sampler_name": "k_dpm_2_a", "karras": True}
    },
    {
        "name": "Juggernaut XL",
        "file": "juggernaut_xl_frontal.webp",
        "params": {"cfg_scale": 7, "height": 1024, "width": 768, "steps": 30, "sampler_name": "k_euler_a", "karras": True}
    },
    {
        "name": "ICBINP - I Can't Believe It's Not Photography",
        "file": "icbinp_frontal.webp",
        "params": {"cfg_scale": 7, "height": 768, "width": 512, "steps": 35, "sampler_name": "k_dpm_2_a", "karras": True}
    },
]

def submit_job(model_config):
    """提交一个生成任务"""
    payload = {
        "prompt": f"{PROMPT} ### {NEGATIVE}",
        "models": [model_config["name"]],
        "params": model_config["params"],
        "nsfw": True,
        "censor_nsfw": False,
        "trusted_workers": False,
        "slow_workers": True
    }
    headers = {"apikey": "0000000000", "Client-Agent": "XiaoAi:2.0:test"}
    try:
        r = requests.post(f"{HORDE_API}/generate/async", json=payload, headers=headers, timeout=20)
        if r.status_code == 202:
            job_id = r.json()["id"]
            print(f"  ✅ 已提交 [{model_config['name']}] → ID: {job_id}")
            return job_id
        else:
            print(f"  ❌ [{model_config['name']}] 提交失败: {r.text[:100]}")
    except Exception as e:
        print(f"  ❌ [{model_config['name']}] 异常: {e}")
    return None

def poll_and_download(jobs):
    """轮询所有任务，谁先完成就下载谁"""
    completed = set()
    for attempt in range(30):
        time.sleep(10)
        all_done = True
        for model_config, job_id in jobs:
            if job_id in completed:
                continue
            try:
                check = requests.get(f"{HORDE_API}/generate/check/{job_id}").json()
                if check.get("done"):
                    status = requests.get(f"{HORDE_API}/generate/status/{job_id}").json()
                    gen = status.get("generations", [{}])[0]
                    img_data = gen.get("img")
                    if img_data:
                        # Horde 返回的可能是 base64 或 URL
                        filepath = f"{RESULTS_DIR}/{model_config['file']}"
                        if img_data.startswith("http"):
                            r = requests.get(img_data, timeout=30)
                            with open(filepath, "wb") as f:
                                f.write(r.content)
                        else:
                            with open(filepath, "wb") as f:
                                f.write(base64.b64decode(img_data))
                        size = os.path.getsize(filepath)
                        censored = gen.get("censored", False)
                        print(f"  🎉 [{model_config['name']}] 完成！文件: {filepath} ({size} 字节) {'⚠️被审查' if censored else '✅未审查'}")
                        completed.add(job_id)
                else:
                    all_done = False
                    wait = check.get("wait_time", "?")
                    print(f"  ⏳ [{model_config['name']}] 排队中... 剩余约 {wait}s")
            except Exception as e:
                all_done = False
        if len(completed) == len(jobs):
            break
    return len(completed)

if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"目标: 正面全身写实照片，面部高保真，暗色机房风格")
    print(f"提交 {len(MODEL_CONFIGS)} 个模型任务...\n")

    jobs = []
    for cfg in MODEL_CONFIGS:
        job_id = submit_job(cfg)
        if job_id:
            jobs.append((cfg, job_id))

    if jobs:
        print(f"\n成功提交 {len(jobs)} 个任务，开始轮询等待...\n")
        count = poll_and_download(jobs)
        print(f"\n完成 {count}/{len(jobs)} 个任务。")
    else:
        print("所有任务提交失败。")
