#!/usr/bin/env python3
"""Image Studio 角色特征验证 & 端到端性能基线测试
用法:
  python3 test_char_pipeline.py              # 仅测试 Pollinations
  python3 test_char_pipeline.py --refine     # Poll + 精修全流程
  python3 test_char_pipeline.py --char xiaoli  # 仅测指定角色
"""
import json, time, os, sys, urllib.request, argparse
from datetime import datetime

API_BASE = "http://127.0.0.1:5051"
OUTPUT_BASE = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/outputs"

# 纯场景提示词（不含外貌，完全依赖 CHAR_TRAITS_DB 注入）
SCENE_PROMPT = (
    "(suspended mid-air by thick hemp ropes, "
    "intricate Japanese shibari tortoise tie constricting torso "
    "and squeezing breasts:2.0), "
    "(deep rope indentations into soft skin:1.8), "
    "(crying intensely, tears streaming, messy mascara:1.6), "
    "(metal chains anchoring feet to floor:1.7), "
    "(sweating glistening wet body:1.4), "
    "dark abandoned warehouse, dramatic spotlight, "
    "high contrast shadows, photorealistic masterpiece"
)

CHARS = {
    "xiaoli": {"label": "小丽", "checks": [
        "酒红卷发", "G杯巨乳", "酒红项圈", "酒红高跟", "酒红阴毛", "骨感"]},
    "xiaoai": {"label": "小爱", "checks": [
        "褐色短发", "平胸/小胸", "红色细项圈", "红色人字拖", "白虎"]},
    "xiaoni": {"label": "小妮", "checks": [
        "黑色长直发", "D杯", "黑色素项圈", "赤脚", "黑色稀疏阴毛"]},
}


def api_post(path, body, timeout=180):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{API_BASE}{path}", data=data,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def run_test(chars_to_test, do_refine=False, seed=42):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.join(OUTPUT_BASE, f"test_{ts}")
    os.makedirs(report_dir, exist_ok=True)
    results = []

    for char_key in chars_to_test:
        info = CHARS[char_key]
        print(f"\n{'='*50}")
        print(f"[1/2] Poll 生成: {info['label']} ({char_key})")

        t0 = time.time()
        poll_result = api_post("/api/pollinations/generate", {
            "prompt": SCENE_PROMPT,
            "model": "zimage",
            "width": 768, "height": 1152,
            "seed": seed, "safe": "false",
            "use_key": True, "enhance": False,
            "character": char_key
        })
        poll_time = time.time() - t0
        poll_url = poll_result.get("url", "")
        poll_file = poll_url.split("/")[-1]
        print(f"  ✅ Poll 完成 | {poll_time:.1f}s | {poll_file}")

        entry = {
            "character": char_key,
            "label": info["label"],
            "poll_file": poll_file,
            "poll_time": round(poll_time, 1),
            "checks": info["checks"],
        }

        if do_refine:
            print(f"[2/2] 精修: {info['label']} ({char_key})")
            t0 = time.time()
            try:
                ref_result = api_post("/api/refine", {
                    "filename": poll_file,
                    "character": char_key,
                    "camera": "moody",
                    "denoise": 0.55,
                    "scene_prompt": "shibari bondage warehouse",
                    "seed": -1
                }, timeout=600)
                ref_time = time.time() - t0
                ref_url = ref_result.get("url", "")
                ref_file = ref_url.split("/")[-1]
                print(f"  ✅ 精修完成 | {ref_time:.1f}s | {ref_file}")
                entry["refine_file"] = ref_file
                entry["refine_time"] = round(ref_time, 1)
                entry["total_time"] = round(poll_time + ref_time, 1)
            except Exception as e:
                print(f"  ❌ 精修失败: {e}")
                entry["refine_error"] = str(e)

        results.append(entry)

    # 写入报告
    report_path = os.path.join(report_dir, "report.json")
    with open(report_path, "w") as f:
        json.dump({"timestamp": ts, "results": results}, f,
                  ensure_ascii=False, indent=2)

    # 打印汇总
    print(f"\n{'='*50}")
    print(f"📊 测试报告: {report_path}")
    print(f"{'='*50}")
    for r in results:
        line = f"  {r['label']}: Poll {r['poll_time']}s"
        if "refine_time" in r:
            line += f" + 精修 {r['refine_time']}s = 总计 {r['total_time']}s"
        print(line)
        print(f"    检查项: {', '.join(r['checks'])}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="角色特征验证测试")
    parser.add_argument("--no-refine", action="store_true",
                        help="跳过精修（仅测 Poll 阶段）")
    parser.add_argument("--char", type=str, default="",
                        help="仅测指定角色 (xiaoli/xiaoai/xiaoni)")
    parser.add_argument("--seed", type=int, default=42,
                        help="固定 seed (默认 42)")
    args = parser.parse_args()

    chars = [args.char] if args.char else list(CHARS.keys())
    run_test(chars, do_refine=not args.no_refine, seed=args.seed)
