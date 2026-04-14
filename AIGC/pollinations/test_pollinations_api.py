#!/usr/bin/env python3
"""
Pollinations API 对比测试
- 无 API Key vs 有 API Key
- NSFW 生成能力测试
- negative_prompt / seed 参数测试
"""
import os
import time
import urllib.request
import urllib.error
import json
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

API_KEY = "sk_994CJSpjwX3HCdvUIboYN9mP6YGOsY30"
BASE_URL = "https://gen.pollinations.ai/image"

# ━━━ 测试用例 ━━━
TESTS = [
    {
        "name": "01_无Key_SFW",
        "prompt": "a beautiful chinese girl standing"
                  " in a luxury hotel room, photorealistic",
        "params": {"width": 1024, "height": 1024,
                   "seed": 42, "model": "flux"},
        "use_key": False
    },
    {
        "name": "02_有Key_SFW",
        "prompt": "a beautiful chinese girl standing"
                  " in a luxury hotel room, photorealistic",
        "params": {"width": 1024, "height": 1024,
                   "seed": 42, "model": "flux"},
        "use_key": True
    },
    {
        "name": "03_无Key_NSFW",
        "prompt": "a beautiful nude chinese girl, completely naked,"
                  " standing barefoot, small breasts,"
                  " sparse pubic hair, photorealistic, RAW photo",
        "params": {"width": 1024, "height": 1024,
                   "seed": 88, "model": "flux", "safe": "false"},
        "use_key": False
    },
    {
        "name": "04_有Key_NSFW",
        "prompt": "a beautiful nude chinese girl, completely naked,"
                  " standing barefoot, small breasts,"
                  " sparse pubic hair, photorealistic, RAW photo",
        "params": {"width": 1024, "height": 1024,
                   "seed": 88, "model": "flux", "safe": "false"},
        "use_key": True
    },
    {
        "name": "05_NegPrompt测试",
        "prompt": "a beautiful nude chinese girl, completely naked,"
                  " standing barefoot, photorealistic",
        "params": {"width": 1024, "height": 1024,
                   "seed": 100, "model": "flux",
                   "safe": "false",
                   "negative_prompt": "chubby, fat, thick,"
                   " large areolas, stockings"},
        "use_key": True
    },
    {
        "name": "06_ZImage模型",
        "prompt": "a beautiful nude chinese girl, completely naked,"
                  " standing barefoot, photorealistic",
        "params": {"width": 1024, "height": 1024,
                   "seed": 100, "model": "zimage",
                   "safe": "false"},
        "use_key": True
    },
]


def build_url(prompt, params):
    """构建 Pollinations API URL"""
    encoded = urllib.request.quote(prompt.strip())
    qs = "&".join(f"{k}={urllib.request.quote(str(v))}"
                  for k, v in params.items())
    return f"{BASE_URL}/{encoded}?{qs}" if qs else f"{BASE_URL}/{encoded}"


def download(url, dest, use_key=False):
    """下载图片，返回 (耗时, 文件大小, HTTP状态码)"""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Pollinations-Test/1.0")
    if use_key:
        req.add_header("Authorization", f"Bearer {API_KEY}")

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
            elapsed = time.time() - t0
            ct = resp.headers.get("Content-Type", "")
            status = resp.status
            with open(dest, "wb") as f:
                f.write(data)
            return elapsed, len(data), status, ct
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        return elapsed, 0, e.code, str(e)
    except Exception as e:
        elapsed = time.time() - t0
        return elapsed, 0, -1, str(e)


def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = []
    report.append(f"Pollinations API 测试报告 — {ts}")
    report.append("=" * 60)

    for t in TESTS:
        url = build_url(t["prompt"], t["params"])
        dest = os.path.join(OUTPUT_DIR, f"{t['name']}_{ts}.jpg")
        key_str = "有Key" if t["use_key"] else "无Key"

        print(f"\n▶ [{t['name']}] ({key_str})  生成中...")
        print(f"  URL: {url[:120]}...")

        elapsed, size, status, ct = download(
            url, dest, t["use_key"])

        if status == 200 and size > 0:
            size_kb = size / 1024
            result = f"✅ 成功 | {elapsed:.1f}s | {size_kb:.0f}KB"
            result += f" | {ct}"
            print(f"  {result}")
        else:
            result = f"❌ 失败 | {elapsed:.1f}s | HTTP {status}"
            result += f" | {ct}"
            print(f"  {result}")

        report.append(f"\n[{t['name']}] ({key_str})")
        report.append(f"  Prompt: {t['prompt'][:60]}...")
        report.append(f"  Model: {t['params'].get('model','?')}")
        report.append(f"  结果: {result}")
        report.append(f"  文件: {os.path.basename(dest)}")

        # 间隔 2 秒避免触发限流
        time.sleep(2)

    # 写出报告
    rpt_path = os.path.join(OUTPUT_DIR, f"report_{ts}.txt")
    with open(rpt_path, "w") as f:
        f.write("\n".join(report))
    print(f"\n📄 报告已保存: {rpt_path}")
    print("=" * 60)
    for line in report:
        print(line)


if __name__ == "__main__":
    main()
