"""
双模型对比测试：moodyPornMix_zitV11DPO vs moodyV10DPO.syMP
针对三角色（小爱/小妮/小丽）× 多姿势/场景 生成 NSFW 对比图
架构：ZIT/Lumina2 → UNETLoader + CLIPLoader(qwen_3_4b) + VAELoader(ae)
"""

import os
import sys
import time
import json
import random
import urllib.request
import urllib.parse
from datetime import datetime

# ===== 模型配置 =====
MODELS = [
    {
        "name": "moodyV10DPO",
        "unet": "moodyV10DPO.syMP.safetensors",
        "label": "V10_旧版"
    },
    {
        "name": "moodyPornMix_zitV11DPO",
        "unet": "moodyPornMix_zitV11DPO.safetensors",
        "label": "V11_新版"
    },
]

# ===== 角色核心定义（来自 RULES） =====
CHARACTERS = {
    "XiaoAi": {
        "label": "小爱",
        "positive_core": (
            "18 year old petite Chinese girl, round face, big eyes, "
            "short brown bob hair, small B-cup breasts, tiny pink areolas, "
            "smooth skin, 160cm, slender body, completely naked, "
            "hairless smooth pussy, red flip-flops, thin red choker, "
            "photorealistic, highly detailed"
        ),
    },
    "XiaoNi": {
        "label": "小妮",
        "positive_core": (
            "20 year old tall slim Chinese beauty, phoenix eyes, sharp chin, "
            "long straight black hair, extremely slender, 170cm, "
            "natural D-cup breasts, tiny areolas, smooth skin, "
            "completely naked, barefoot, sparse black pubic hair, "
            "black leather collar, photorealistic, highly detailed"
        ),
    },
    "XiaoLi": {
        "label": "小丽",
        "positive_core": (
            "20 year old tall elegant Chinese woman, cold beautiful face, "
            "long wine-red wavy hair, very thin waist, 180cm, "
            "huge heavy natural G-cup breasts with slight sag, "
            "tiny pink areolas, smooth skin, completely nude, "
            "sparse wine-red pubic hair, wine-red choker, "
            "wine-red stiletto heels, photorealistic, highly detailed"
        ),
    },
}

# ===== 通用负面提示词 =====
NEGATIVE_CORE = (
    "low quality, worst quality, anime, cartoon, 3d render, painting, "
    "deformed, ugly, skeletal, gaunt, emaciated, fleshy, "
    "western face, blonde hair, eyepatch, sunglasses, "
    "bad anatomy, extra limbs, mutation, body horror, "
    "text, watermark, logo, signature, "
    "clothing, clothes, fabric, covering, "
    "censored, mosaic, blur bar"
)

# ===== 姿势/场景列表（所有角色通用） =====
POSES = [
    {
        "id": "01",
        "name": "卧室慵懒",
        "desc": (
            "lying on a luxurious silk bed, on her back, "
            "legs slightly spread, one hand resting on thigh, "
            "soft morning light, warm atmosphere, "
            "looking at camera with seductive expression"
        ),
    },
    {
        "id": "02",
        "name": "浴室湿身",
        "desc": (
            "standing in a steamy shower room, wet skin glistening, "
            "water droplets on body, hair wet and clinging to skin, "
            "one hand touching collarbone, side lighting, "
            "sensual expression, full body visible"
        ),
    },
    {
        "id": "03",
        "name": "沙发撩人",
        "desc": (
            "sitting on a dark velvet sofa, legs crossed, "
            "leaning back, arms behind head, arching back, "
            "warm golden lamp light, moody atmosphere, "
            "confident seductive gaze at camera"
        ),
    },
    {
        "id": "04",
        "name": "窗前逆光",
        "desc": (
            "standing by a floor-to-ceiling window, city skyline at dusk, "
            "beautiful rim light silhouette, hands on hips, "
            "turning to look at camera, golden hour backlight, "
            "full body shot from behind at slight angle"
        ),
    },
]

SERVER = "127.0.0.1:8188"
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "outputs",
    f"model_compare_{datetime.now().strftime('%Y%m%d_%H%M')}"
)


def build_zit_workflow(unet_name, positive, negative, seed,
                       width=832, height=1216, steps=10, cfg=1.0):
    """构建 ZIT/Lumina2 架构的 ComfyUI Workflow"""
    return {
        "1": {
            "inputs": {"unet_name": unet_name, "weight_dtype": "default"},
            "class_type": "UNETLoader"
        },
        "2": {
            "inputs": {"clip_name": "qwen_3_4b.safetensors",
                       "type": "qwen_image"},
            "class_type": "CLIPLoader"
        },
        "3": {
            "inputs": {"vae_name": "ae.safetensors"},
            "class_type": "VAELoader"
        },
        "5": {
            "inputs": {"width": width, "height": height, "batch_size": 1},
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {"text": positive, "clip": ["2", 0]},
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {"text": negative, "clip": ["2", 0]},
            "class_type": "CLIPTextEncode"
        },
        "8": {
            "inputs": {
                "seed": seed, "steps": steps, "cfg": cfg,
                "sampler_name": "euler", "scheduler": "simple",
                "denoise": 1.0,
                "model": ["1", 0], "positive": ["6", 0],
                "negative": ["7", 0], "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
        },
        "9": {
            "inputs": {"samples": ["8", 0], "vae": ["3", 0]},
            "class_type": "VAEDecode"
        },
        "10": {
            "inputs": {
                "filename_prefix": "ModelCompare",
                "images": ["9", 0]
            },
            "class_type": "SaveImage"
        }
    }

def queue_and_wait(workflow, timeout=1200):
    """提交 workflow 并等待完成，返回输出图片数据"""
    payload = json.dumps({
        "prompt": workflow,
        "client_id": "model_compare_test"
    }).encode("utf-8")
    req = urllib.request.Request(
        f"http://{SERVER}/prompt", data=payload
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    prompt_id = resp["prompt_id"]
    print(f"  ↳ 已加入队列, prompt_id={prompt_id}")

    start = time.time()
    while time.time() - start < timeout:
        with urllib.request.urlopen(
            f"http://{SERVER}/history/{prompt_id}"
        ) as h:
            history = json.loads(h.read())
            if prompt_id in history:
                break
        time.sleep(3)
    else:
        raise TimeoutError(f"生成超时 ({timeout}s)")

    outputs = history[prompt_id]["outputs"]
    for node_id in outputs:
        node_out = outputs[node_id]
        if "images" in node_out:
            img_info = node_out["images"][0]
            params = urllib.parse.urlencode({
                "filename": img_info["filename"],
                "subfolder": img_info["subfolder"],
                "type": img_info["type"]
            })
            with urllib.request.urlopen(
                f"http://{SERVER}/view?{params}"
            ) as img_resp:
                return img_resp.read(), img_info["filename"]
    return None, None


def run_comparison():
    """执行全量对比测试"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"角色数: {len(CHARACTERS)}")
    print(f"模型数: {len(MODELS)}")
    print(f"姿势数: {len(POSES)}")
    total = len(CHARACTERS) * len(MODELS) * len(POSES)
    print(f"总计生成: {total} 张")
    print("=" * 60)

    # 对每个姿势使用固定种子，确保公平对比
    seeds = {p["id"]: random.randint(0, 0xFFFFFFFF) for p in POSES}

    results = []  # 收集结果用于生成报告
    result_map = {}  # {(char, pose_id): {model_name: path}}
    count = 0

    # 按模型分组执行，减少 UNET 卸载/加载次数（每次切换需读取12GB）
    for model in MODELS:
        print(f"\n{'#'*60}")
        print(f"当前模型: {model['label']} ({model['unet']})")
        print(f"{'#'*60}")

        for char_key, char in CHARACTERS.items():
            print(f"\n{'='*60}")
            print(f"角色: {char['label']} ({char_key})")
            print(f"{'='*60}")

            for pose in POSES:
                count += 1
                seed = seeds[pose["id"]]
                positive = (
                    f"{char['positive_core']}, "
                    f"{pose['desc']}, "
                    f"cinematic lighting, moody atmosphere, masterpiece"
                )
                fname = (
                    f"{char_key}_{pose['id']}_{pose['name']}"
                    f"_{model['name']}.png"
                )
                save_path = os.path.join(OUTPUT_DIR, fname)

                print(
                    f"\n[{count}/{total}] "
                    f"{char['label']} × {pose['name']} "
                    f"× {model['label']}"
                )
                print(f"  模型: {model['unet']}")
                print(f"  种子: {seed}")

                wf = build_zit_workflow(
                    unet_name=model["unet"],
                    positive=positive,
                    negative=NEGATIVE_CORE,
                    seed=seed
                )

                # 初始化结果映射
                map_key = (char['label'], f"{pose['id']}-{pose['name']}")
                if map_key not in result_map:
                    result_map[map_key] = {}

                try:
                    t0 = time.time()
                    img_data, srv_name = queue_and_wait(wf)
                    elapsed = time.time() - t0

                    if img_data:
                        with open(save_path, "wb") as f:
                            f.write(img_data)
                        print(
                            f"  ✅ 成功 ({elapsed:.1f}s) → {fname}"
                        )
                        result_map[map_key][model["name"]] = save_path
                    else:
                        print(f"  ❌ 无输出数据")
                        result_map[map_key][model["name"]] = "FAIL"

                except Exception as e:
                    print(f"  ❌ 生成失败: {e}")
                    result_map[map_key][model["name"]] = "FAIL"

    # 将 result_map 转为 results 列表
    for (char_label, pose_label), files in result_map.items():
        results.append({
            "char": char_label,
            "pose": pose_label,
            "files": files
        })

    # 生成 Markdown 报告
    generate_report(results)
    print(f"\n{'='*60}")
    print(f"全部完成！共 {count} 张，输出目录: {OUTPUT_DIR}")


def generate_report(results):
    """生成 Markdown 对比报告"""
    report_path = os.path.join(OUTPUT_DIR, "comparison_report.md")
    lines = [
        f"# 🔬 双模型对比报告",
        f"> moodyPornMix_zitV11DPO vs moodyV10DPO",
        f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| 角色 | 姿势/场景 | V10 旧版 | V11 新版 |",
        "| :--- | :--- | :---: | :---: |",
    ]

    for r in results:
        v10 = r["files"].get("moodyV10DPO", "N/A")
        v11 = r["files"].get("moodyPornMix_zitV11DPO", "N/A")
        v10_cell = (
            f"[查看](file://{v10})" if v10 != "FAIL"
            else "❌ 失败"
        )
        v11_cell = (
            f"[查看](file://{v11})" if v11 != "FAIL"
            else "❌ 失败"
        )
        lines.append(
            f"| {r['char']} | {r['pose']} "
            f"| {v10_cell} | {v11_cell} |"
        )

    lines.extend([
        "",
        "## 对比维度",
        "- **面部真实感**: 面部细节、中国面孔准确度",
        "- **肤质渲染**: 皮肤纹理、光泽、色调",
        "- **解剖学正确性**: 身体比例、四肢、手指",
        "- **NSFW 细节**: 敏感部位渲染质量",
        "- **整体构图**: 场景氛围、光影效果",
        "",
        "## 技术参数",
        "- CLIP: qwen_3_4b.safetensors",
        "- VAE: ae.safetensors",
        "- 采样器: euler / simple / steps=25 / cfg=4.5",
        "- 分辨率: 832×1216",
        "- 每组姿势使用相同种子以确保公平对比",
    ])

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n📋 报告已生成: {report_path}")


if __name__ == "__main__":
    run_comparison()
