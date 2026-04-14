# 🎨 AI Image & Video Tools (AIGC Core Suite)

> 一套自动化 AI 图像与视频生成、精修与业务归档工作流组合架构。
> 由 **[Pollinations.ai](https://pollinations.ai)** 与 **ComfyUI (Hunyuan/Flux/Pony)** 双引擎驱动。

---

## 📂 架构概览 (Directory Structure)

本仓库包含了本机的核心 AIGC 调度流与业务逻辑，已分为以下几大功能区以保证绝对安全与模块隔离：

### 1. `Formal/` (核心通用库与常驻程序)
存放具有底层框架支撑性质的文件：
*   **通信与对接层**: `comfyui_client.py`, `submit_*.py` 等，负责封装到底层显卡的 HTTP REST 请求。
*   **守护进程**: `watch_and_update.*` 等文件维持队列的健康。
*   **后处理流**: `push_videos.py` 等飞书 Webhook 自动化推流器和同步服务器。

### 2. `Process/` (生成业务链路与历史脚本)
存放过往针对各类精细化图生图、视频生成以及复杂业务场景（包含各类 NSFW 或肢体强校对）的一次性或阶段性构建脚本。
包含上百个 `generate_*.py` 和对应日志，这是沉淀下来的“配方库”。

### 3. `Tests/` (测试探针区)
包含所有 `test_*.py` 及各种输出的 `.mp4` 基础基准测试资产，用于验证网络、GGUF 张量完整度以及流匹配。

### 4. `pollinations/` (Web 轻量化看板)
包含了原来的 `AI Image Studio`，一个基于 Flask 驱动的、具有真实余额监控的纯云端 Web 端操作面板。

### 5. `outputs/`
所有流转完毕的精炼图片和视频均落地与此。

---

## 🚀 核心工作流引擎说明

系统整合了两个互补的 AI 后端，分别负责不同阶段的工作：

| 阶段 | 引擎 | 作用 |
|---|---|---|
| **文生图 (云端)** | [Pollinations.ai](https://pollinations.ai) | 基于 Pollinations REST API 的云端图像生成，零本地 GPU 负担。在 `pollinations/img_studio` 面板 (Port: 5051) 执行。 |
| **图生视频 (I2V)** | HunyuanVideo (GGUF) | 利用本地 48GB 统一内存加载 Q5_K_M 的 Hunyuan 视频核心，摒弃冲突 LoRA，利用纯底层推演实现 0 闪烁重绘。 |
| **细分图生图** | ComfyUI 流 | 本地各种针对肢体、动作、高曝光的重绘约束。 |

---

## 🛠 最佳实践与防护墙

- **关于 LoRA 的 GGUF 兼容性**：任何时候生成视频时，目前由于 GGUF 张量的 1D 加载限制，标准 Safetensors 模块已被强制隔离阻断。后续新增动态全靠 CFG 调教！
- **IDE 端口死锁提醒**：Pollinations 大盘的侦听端口请永远设定在 `5051`，避免与主编辑器 IDE 产生代理流量环路死锁。 

---
_Auto-synced and maintained continuously for core AI deployments._
