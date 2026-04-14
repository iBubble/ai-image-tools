import requests
import time
import base64
import os

RESULTS_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/secret_results"
HORDE_API = "https://stablehorde.net/api/v2"
os.makedirs(RESULTS_DIR, exist_ok=True)

PROMPT = "(best quality, masterpiece, ultra-detailed, photorealistic:1.4), beautiful 20 year old Chinese woman Xiao Ai, full body portrait, facing viewer, kneeling in dark server room, blue LED light, long messy black hair, blushing, expressive eyes, (nude:1.3), realistic body, sweat, black heels, cinematic lighting, volumetric fog, RAW photo, detailed skin texture"
NEGATIVE = "deformed face, distorted eyes, bad anatomy, extra limbs, ugly, blurry, watermark, cartoon, anime, 3d render"

configs = [
    {"name": "Deliberate", "file": "deliberate_sm.webp"},
    {"name": "AbsoluteReality", "file": "absolutereality_sm.webp"},
    {"name": "GhostMix", "file": "ghostmix_sm.webp"},
    {"name": "AbyssOrangeMix-AfterDark", "file": "afterdark_sm.webp"},
]

headers = {"apikey": "0000000000", "Client-Agent": "XiaoAi:2.0:test"}
jobs = []

for cfg in configs:
    payload = {
        "prompt": f"{PROMPT} ### {NEGATIVE}",
        "models": [cfg["name"]],
        "params": {
            "cfg_scale": 7,
            "height": 512,
            "width": 512,
            "steps": 10,
            "sampler_name": "k_euler_a",
            "karras": True,
        },
        "nsfw": True,
        "censor_nsfw": False,
        "trusted_workers": False,
        "slow_workers": True,
    }
    try:
        r = requests.post(
            f"{HORDE_API}/generate/async",
            json=payload,
            headers=headers,
            timeout=20,
        )
        if r.status_code == 202:
            jid = r.json()["id"]
            print(f"OK [{cfg['name']}] -> {jid}")
            jobs.append((cfg, jid))
        else:
            print(f"FAIL [{cfg['name']}]: {r.text[:120]}")
    except Exception as e:
        print(f"ERR [{cfg['name']}]: {e}")

print(f"\nsub={len(jobs)}, polling...\n")
completed = set()

for attempt in range(40):
    time.sleep(8)
    for cfg, jid in jobs:
        if jid in completed:
            continue
        try:
            ck = requests.get(f"{HORDE_API}/generate/check/{jid}").json()
            if ck.get("done"):
                st = requests.get(f"{HORDE_API}/generate/status/{jid}").json()
                gen = st.get("generations", [{}])[0]
                img = gen.get("img", "")
                fp = f"{RESULTS_DIR}/{cfg['file']}"
                if img.startswith("http"):
                    data = requests.get(img).content
                else:
                    data = base64.b64decode(img)
                with open(fp, "wb") as f:
                    f.write(data)
                censored = gen.get("censored", False)
                model_used = gen.get("model", "?")
                print(
                    f"DONE [{model_used}] -> {fp} ({len(data)}B) {'CENSORED!' if censored else 'PASS'}"
                )
                completed.add(jid)
            else:
                print(f"WAIT [{cfg['name']}] eta={ck.get('wait_time')}s")
        except Exception as e:
            print(f"CHECK ERR [{cfg['name']}]: {e}")
    if len(completed) == len(jobs):
        break

print(f"\nfinished {len(completed)}/{len(jobs)}")
