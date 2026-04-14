# Pony Diffusion V6 中国女性生成优化指南

## 📋 核心原则

Pony Diffusion V6 是基于 Booru 标签系统训练的模型，对**标签顺序**和**权重设置**极其敏感。要生成高质量的中国女性图像，必须遵循以下优化策略。

---

## 🎯 一、标签顺序规范（Critical）

Pony 模型的最佳标签顺序：

```
质量评分 → 身份标签 → 面部细节 → 发型 → 体型 → 场景/动作 → 风格标签
```

### 示例结构：
```
score_9, score_8_up, score_7_up, score_6_up,
1girl, solo,
(chinese:1.3), (east asian:1.2),
[面部细节标签],
[发型标签],
[体型标签],
[场景动作],
photo (medium), realistic, highly detailed
```

---

## 🧬 二、面部细化标签库

### 1. 族群定位（必填）
```
(chinese:1.3), (east asian:1.2)
```
- 权重建议：1.2-1.3
- 两个标签组合使用效果最佳

### 2. 眼部特征（核心）
```
brown eyes, dark eyes, 
almond eyes,           # 杏眼
epicanthic fold,       # 内眦赘皮（典型东亚特征）
hooded eyelids         # 内双
```

### 3. 鼻部特征
```
small nose, 
flat bridge            # 较平缓的鼻梁
```

### 4. 唇部特征
```
small lips, 
cherry lips            # 樱桃小嘴
```

### 5. 脸型轮廓
```
round face,            # 圆脸
heart-shaped face,     # 心形脸
soft jawline,          # 柔和的下颌线
smooth skin, 
pale skin              # 白皙皮肤
```

---

## 💇 三、发型标签

### 基础发质
```
long straight black hair, 
shiny hair
```

### 发型风格
```
blunt bangs,           # 齐刘海（强烈推荐）
hime cut,              # 姬发式
```

### 装饰（可选）
```
hair ornament, 
hairpin,               # 发簪
flower hair ornament
```

---

## 🏃 四、体型优化标签

### 纤细骨架系列
```
(petite body:1.2), 
(slender frame:1.3), 
(delicate bone structure:1.2), 
(slim waist:1.1), 
(narrow shoulders:1.1)
```

### 胸部描述
```
huge natural breasts,  # 或 large breasts, D-cup breasts
detailed nipples
```

---

## ❌ 五、负面提示词（Negative Prompt）

### 核心负面标签
```
score_4, score_5, score_6,
lowres, bad anatomy, bad hands, text, error, 
missing fingers, extra digit, fewer digits, cropped,
worst quality, low quality, normal quality, 
jpeg artifacts, signature, watermark, username, blurry
```

### 西方特征抑制（Critical）
```
(western features:1.3),
deep eyes,             # 深邃眼睛
high nose bridge,      # 高鼻梁
(freckles:1.2),        # 雀斑
cleft chin,            # 下巴裂痕
rough skin
```

### 体型抑制
```
(muscular:1.3), 
(athletic build:1.2), 
(broad shoulders:1.3), 
(thick bones:1.2), 
(large frame:1.2)
```

### 遮挡/审查抑制
```
(clothing, clothes:1.6), 
(censored:1.5), 
(mutation, body horror:1.4)
```

---

## 📝 六、完整提示词模板

### 正向提示词（Positive Prompt）
```
score_9, score_8_up, score_7_up, score_6_up, 
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
[场景动作描述],
photo (medium), realistic, highly detailed, cinematic lighting
```

### 负向提示词（Negative Prompt）
```
score_4, score_5, score_6, 
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, 
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,
(western features:1.3), deep eyes, high nose bridge, (freckles:1.2), cleft chin, rough skin,
(clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4),
(muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2)
```

---

## 🔧 七、进阶技巧

### 1. 解决"混血脸"问题
- **方法1**：提高权重 `(chinese:1.4)` 或添加 `(detailed asian face:1.2)`
- **方法2**：使用 ADetailer/FaceDetailer 节点进行二次面部精修

### 2. ComfyUI 工作流优化
```python
# 在 ComfyUI 中使用 FaceDetailer 节点
# Detailer Prompt 只写面部描述：
score_9, 1girl, chinese, brown eyes, epicanthic fold, 
small nose, smooth skin, blunt bangs
```

### 3. LoRA 推荐（可选）
- **Asian Face / Chinese Girl LoRA**：强度 0.4-0.7
- **Skin Detailer LoRA**：增强皮肤质感

### 4. 参数建议
- **CFG Scale**: 7.0
- **Sampler**: dpmpp_2m
- **Scheduler**: karras
- **Steps**: 25-30
- **Resolution**: 832x1216 (竖图) 或 1216x832 (横图)

---

## ⚠️ 常见问题与解决方案

### Q1: 生成的面孔还是偏西方
**A**: 
1. 检查标签顺序，确保 `(chinese:1.3)` 在身份标签区
2. 提高负面提示词中 `(western features:1.3)` 的权重
3. 添加 `epicanthic fold` 和 `hooded eyelids`

### Q2: 眼睛太大或太深邃
**A**: 
1. 添加 `almond eyes` 和 `epicanthic fold`
2. 负面提示词中添加 `deep eyes, large eyes`

### Q3: 鼻子太高
**A**: 
1. 使用 `small nose, flat bridge`
2. 负面提示词中添加 `high nose bridge, sharp nose`

### Q4: 皮肤粗糙或有雀斑
**A**: 
1. 正向添加 `smooth skin, pale skin`
2. 负面添加 `(freckles:1.2), rough skin, blemishes`

---

## 📊 成功案例参考

### 案例：冷钢束缚场景
**正向提示词**：
```
score_9, score_8_up, score_7_up, score_6_up, 
1girl, solo, 
(chinese:1.3), (east asian:1.2), 
beautiful face, soft facial features, 
brown eyes, dark eyes, almond eyes, epicanthic fold, hooded eyelids,
small nose, flat bridge, small lips, cherry lips,
round face, soft jawline, smooth skin, pale skin,
long straight black hair, shiny hair, blunt bangs,
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2),
huge natural breasts, detailed nipples,
completely naked, wearing high heels,
suspended by wrists from chains, arms raised, tiptoes, painful expression, genitals visible,
photo (medium), realistic, highly detailed, cinematic lighting
```

**效果**：
- ✅ 典型东亚面孔（内双、杏眼、齐刘海）
- ✅ 纤细骨架
- ✅ 白皙光滑皮肤
- ✅ 显式内容无遮挡

---

## 🎓 总结

Pony V6 生成中国女性的关键：
1. **严格遵循标签顺序**
2. **使用专业的面部细化标签**（epicanthic fold, almond eyes 等）
3. **强化负面提示词**以抑制西方特征
4. **权重设置合理**（chinese:1.3, western features:1.3）
5. **整合体型优化标签**以符合东方审美

---

**最后更新**: 2026-02-14  
**验证状态**: ✅ 已在实际生成中验证有效  
**适用模型**: Pony Diffusion V6 XL 及其衍生模型
