# 🎨 AI Image Studio

> 一套自动化 AI 图像生成与精修工作台 —— 由 **[Pollinations.ai](https://pollinations.ai)** 和 **ComfyUI** 双引擎驱动。

---

## 项目简介

AI Image Studio 是一个从文字到成品的全链路图像生成工具集，涵盖：生成高质量写实风格人物图像、智能精修画质、自动化归档分发，所有操作均可在一个 Web 面板中完成。

系统整合了两个互补的 AI 后端，分别负责不同阶段的工作：

| 阶段 | 引擎 | 作用 |
|---|---|---|
| **文生图** | [Pollinations.ai](https://pollinations.ai) | 基于 Pollinations REST API 的云端图像生成，支持 Flux 等模型，无需本地 GPU |
| **图生图（精修）** | [ComfyUI](https://github.com/comfyanonymous/ComfyUI) | 本地 img2img 增强，自适应去噪以提升写实质感 |

---

## Pollinations.ai 在本项目中的核心作用

[Pollinations.ai](https://pollinations.ai) 是本项目的 **主力图像生成引擎**，具体集成方式如下：

### 1. API 驱动的图像生成
所有文生图请求通过 Pollinations REST API（`https://gen.pollinations.ai/image/`）发出。系统对用户输入的提示词进行编码，配置模型、分辨率、随机种子等参数，将生成结果流式返回浏览器 —— 全程无需本地 GPU。

### 2. 自动写实增强
在将提示词发送至 Pollinations 之前，系统会自动拼接专业摄影关键词（RAW photo、DSLR、浅景深、胶片颗粒、8K UHD 等），并注入一组全面的负向提示词矩阵，抑制卡通/插画/畸形等常见失真。

### 3. 多 Key 轮换与容灾降级
支持配置多个 Pollinations API Key，并实现自动轮换。当某个 Key 触发频率限制（HTTP 402/429）时，引擎无缝切换至下一个 Key；所有 Key 耗尽后，优雅降级至免费模式 —— 确保生成流水线不中断。

### 4. 实时余额监控
内置余额查询接口（`/api/pollinations/quota`），聚合所有 Key 的剩余额度并在 Web 面板中实时展示，让用户随时掌握可用生成次数。

---

## 其他特性

### 角色特征注入管道
预定义的人物特征模板（面部、发型、体型、服饰等）以 1.3 权重前置注入到提示词中，确保在不同场景下保持角色一致性。

### 智能卡通/真人检测
像素级分析器通过颜色量化唯一性、边缘锐度和平均饱和度三项指标，自动判定图片是卡通风格还是真人照片，并据此选择不同的去噪强度进行 ComfyUI 精修。

### 自动归档与分发
每张生成的图片会自动：
- 保存到按日期组织的本地归档目录（`outputs/YYYYMMDD/`）
- 通过 Webhook 推送至飞书（Lark）频道
- 通过 SCP 上传至远程服务器

### 现代化 Web 面板
Flask 驱动的深色主题看板（`localhost:5050`），集成实时余额显示、生成耗时统计和一键精修控制。

---

## 快速开始

### 环境依赖
- Python 3.12+
- `pip install flask pillow numpy requests`
- （可选）本地运行 ComfyUI 实例（`localhost:8188`），用于精修功能

### 启动服务
```bash
python app.py
```
浏览器打开 **http://localhost:5050** 即可使用。

### 运行测试
```bash
python test_char_pipeline.py
```

---

## 架构概览

```
┌─────────────────────────────────────────────────┐
│                  Web 操作面板                     │
│              (Flask · 端口 5050)                  │
└──────────┬───────────────────┬──────────────────┘
           │                   │
        文生图              图生图精修
           │                   │
           ▼                   ▼
  ┌─────────────────┐  ┌───────────────┐
  │  Pollinations.ai │  │   ComfyUI     │
  │   （云端 API）    │  │  （本地 GPU）  │
  └────────┬────────┘  └──────┬────────┘
           │                   │
           └───────┬───────────┘
                   ▼
         ┌─────────────────┐
         │    自动归档       │
         │  飞书 · SCP 分发  │
         └─────────────────┘
```

---

## 致谢

- **[Pollinations.ai](https://pollinations.ai)** — 开源 AI 图像生成 API，让本项目无需本地 GPU 即可实现高质量图像生成。
- **[ComfyUI](https://github.com/comfyanonymous/ComfyUI)** — 强大的节点式 Stable Diffusion 界面，用于图像精修。

---

## 许可证

MIT
