# Pony V6 优化配置快速参考

## 核心配置（已固化）

### 正向提示词结构
```python
base_desc_pony = """score_9, score_8_up, score_7_up, score_6_up, 
1girl, solo, 
(chinese:1.3), (east asian:1.2), 
beautiful face, soft facial features, 
brown eyes, dark eyes, almond eyes, epicanthic fold, hooded eyelids,
small nose, flat bridge, small lips, cherry lips,
round face, heart-shaped face, soft jawline, smooth skin, pale skin,
long straight black hair, shiny hair, blunt bangs,
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2), (slim waist:1.1), (narrow shoulders:1.1),
huge natural breasts, detailed nipples,
completely naked, wearing high heels,
(explicit:1.2), genitals, pussy, anus, rating_explicit,
photo (medium), realistic, highly detailed, cinematic lighting"""
```

### 负向提示词
```python
neg_pony = """score_4, score_5, score_6, 
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, 
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,
(western features:1.3), deep eyes, high nose bridge, (freckles:1.2), cleft chin, rough skin,
(clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4),
(muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2)"""
```

## 关键标签说明

### 面部特征（必须包含）
- `epicanthic fold` - 内眦赘皮（东亚眼部特征）
- `almond eyes` - 杏眼
- `hooded eyelids` - 内双
- `flat bridge` - 平缓鼻梁
- `blunt bangs` - 齐刘海

### 体型优化（必须包含）
- `(petite body:1.2)` - 娇小身材
- `(slender frame:1.3)` - 纤细骨架
- `(delicate bone structure:1.2)` - 精致骨架
- `(narrow shoulders:1.1)` - 窄肩

### 西方特征抑制（必须包含）
- `(western features:1.3)` - 西方特征
- `deep eyes` - 深邃眼睛
- `high nose bridge` - 高鼻梁
- `(freckles:1.2)` - 雀斑

## 使用位置

### 已固化到的文件
1. `/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/master_model_comparison.py`
   - 主横评脚本
   - 用于 4 模型对比生成

2. `/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/generate_pony_ultimate.py`
   - Pony 专用生成脚本
   - 用于单独生成 Pony 的 8 个环节

3. `/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/docs/Pony_Chinese_Female_Guide.md`
   - 完整优化指南
   - 包含详细说明和进阶技巧

## 验证状态

✅ **已验证有效** - 2026-02-14 00:01
- 环节 01（冷钢束缚）生成成功
- 面部特征：典型东亚面孔（内双、杏眼、齐刘海）
- 体型特征：纤细骨架、窄肩、细腰
- 显式内容：无遮挡、解剖学正确

## 快速使用

### 单独生成 Pony
```bash
/opt/anaconda3/bin/python3 AIGC/generate_pony_ultimate.py
```

### 完整横评（包含 Pony）
```bash
/opt/anaconda3/bin/python3 AIGC/master_model_comparison.py
```

## 注意事项

1. **标签顺序不可打乱**：Pony 模型对顺序极其敏感
2. **权重设置**：chinese:1.3, western features:1.3 是经过验证的最佳值
3. **负面提示词**：必须包含西方特征抑制，否则容易出现混血脸
4. **发型标签**：`blunt bangs` 对东方审美非常重要

## 更新日志

- 2026-02-14 00:16: 初始固化，整合面部细化 + 体型优化
- 验证通过：环节 01 生成效果完美
