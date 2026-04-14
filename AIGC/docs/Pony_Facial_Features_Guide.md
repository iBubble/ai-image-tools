# Pony V6 五官细化优化指南

## 📋 核心五官标签体系

### 1. 眼部标签（Eyes）- 迷离清冷感

#### 眼型基础
```
almond eyes           # 杏眼（东亚典型眼型）
dark eyes             # 深色眼睛
brown eyes            # 褐色眼睛
```

#### 东亚眼部特征（Critical）
```
epicanthic fold       # 内眦赘皮（东亚眼褶）
hooded eyelids        # 内双/遮盖性眼睑
heavy eyelids         # 厚重眼睑
```

#### 眼神与神态
```
looking at viewer     # 注视观众
bedroom eyes          # 迷离/慵懒的神态（性感）
half-closed eyes      # 半闭眼（慵懒感）
seductive eyes        # 诱惑的眼神
```

---

### 2. 鼻部标签（Nose）- 柔和中式审美

```
small nose            # 小巧的鼻子
flat bridge           # 较平缓的鼻梁
soft nose             # 柔和的鼻子
```

**注意**：避免使用 `high nose bridge`, `sharp nose` 等西方特征标签。

---

### 3. 嘴唇标签（Mouth & Lips）- 光泽饱满感

#### 嘴唇形态
```
parted lips           # 微张的嘴唇（性感）
glossy lips           # 有光泽的嘴唇
full lips             # 饱满的嘴唇
cherry lips           # 樱桃小口
plump lips            # 丰满的嘴唇
```

#### 嘴唇细节
```
wet lips              # 湿润的嘴唇
shiny lips            # 闪亮的嘴唇
lipgloss              # 唇彩效果
```

---

### 4. 脸型标签（Face Shape）

```
round face            # 圆脸
heart-shaped face     # 心形脸
soft jawline          # 平滑的下颌线
delicate face         # 精致的脸
```

---

### 5. 皮肤质感标签（Skin Texture）- 水光肌重点

#### 水光感（Critical）
```
(shiny skin:1.3)      # 水光肌（高权重）
(wet skin:1.3)        # 湿润皮肤
oily skin             # 油性/反光质感
glossy skin           # 光滑皮肤
dewy skin             # 露珠般的皮肤
```

#### 皮肤纹理（真实感）
```
textured skin         # 有纹理的皮肤
skin pores            # 皮肤毛孔
detailed skin         # 细节皮肤
realistic skin        # 真实皮肤
```

#### 湿润细节
```
sweat                 # 汗水
water drops on face   # 脸上的水滴
damp skin             # 潮湿皮肤
```

---

## 📝 完整提示词模板（五官优化版）

### 正向提示词（终极五官优化版）
```
score_9, score_8_up, score_7_up, score_6_up, 
1girl, solo, 
(chinese:1.3), (east asian:1.2), 
(beautiful face:1.2), soft facial features, 
almond eyes, dark eyes, brown eyes, epicanthic fold, hooded eyelids, heavy eyelids,
looking at viewer, bedroom eyes,
small nose, flat bridge, soft nose,
parted lips, glossy lips, full lips, cherry lips, wet lips,
round face, heart-shaped face, soft jawline, 
(wet skin:1.3), (shiny skin:1.3), water drops on face, sweat, oily skin, textured skin, skin pores, dewy skin,
(wet hair:1.2), (black hair:1.1), high ponytail, sidelocks, hair strands across face, sweeping bangs, damp hair, shiny hair,
forehead, mismatch bangs,
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2), (slim waist:1.1), (narrow shoulders:1.1),
huge natural breasts, natural nipples, smooth nipples,
earrings, dangling earrings,
completely naked, wearing high heels,
(explicit:1.2), genitals, pussy, anus, rating_explicit,
photo (medium), realistic, highly detailed, 
cinematic lighting, rim lighting, side lighting
```

### 负向提示词（五官校优版）
```
score_4, score_5, score_6, 
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, 
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,
(western features:1.3), (deep eyes:1.2), (high nose bridge:1.2), cleft chin, (freckles:1.2), rough skin,
(clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4),
(muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2),
(textured nipples:1.3), (ringed nipples:1.3), (areola texture:1.2), (bumpy nipples:1.2),
simple background, (flat hair:1.2), (dry hair:1.1), (perfectly styled hair:1.2),
(dry skin:1.2), (matte skin:1.2)
```

---

## 🎯 关键优化点

### 1. 眼神的迷离感
- **核心标签**: `bedroom eyes` + `heavy eyelids` + `half-closed eyes`
- **效果**: 营造慵懒、性感、迷离的眼神
- **适用场景**: 性爱、受虐、疲惫后的状态

### 2. 嘴唇的性感度
- **核心标签**: `parted lips` + `glossy lips` + `wet lips`
- **效果**: 微张的湿润嘴唇，极具诱惑力
- **配合**: 可添加 `drool`, `saliva` 增强效果

### 3. 水光肌的真实感
- **核心标签**: `(wet skin:1.3)` + `(shiny skin:1.3)` + `skin pores`
- **效果**: 湿润反光的皮肤 + 可见毛孔 = 超真实感
- **关键**: 权重设置为 1.3，确保效果明显

### 4. 五官的协调性
- **眼部**: 杏眼 + 内双 + 迷离眼神
- **鼻部**: 小鼻子 + 平缓鼻梁
- **嘴唇**: 微张 + 光泽 + 饱满
- **整体**: 柔和、性感、东方美

---

## 🚫 负面提示词重点

### 必须抑制的西方五官特征
```
(deep eyes:1.2)           # 深邃眼睛
(high nose bridge:1.2)    # 高鼻梁
cleft chin                # 下巴裂痕
(freckles:1.2)            # 雀斑
```

### 必须抑制的皮肤问题
```
(dry skin:1.2)            # 干燥皮肤
(matte skin:1.2)          # 哑光皮肤
rough skin                # 粗糙皮肤
```

---

## 💡 场景应用建议

### 适合的场景
1. **性爱场景**: 迷离眼神 + 微张嘴唇 + 汗水
2. **受虐场景**: 疲惫眼神 + 湿润皮肤 + 泪水混合汗水
3. **浴后场景**: 水光肌 + 湿发 + 水珠
4. **高潮瞬间**: bedroom eyes + parted lips + 汗水

### 标签组合示例

#### 场景1：高潮瞬间
```
bedroom eyes, half-closed eyes, parted lips, drool, 
(wet skin:1.3), sweat, water drops on face, 
exhausted expression, flushed face
```

#### 场景2：受虐后
```
heavy eyelids, tears, parted lips, saliva,
(shiny skin:1.3), sweat, water drops mixing with tears,
broken expression, pain and pleasure
```

---

## 📊 对比效果

### 原版（基础五官）
```
brown eyes, small nose, small lips, smooth skin
```
- 效果：清纯、干净、学生气
- 缺点：缺乏性感度和真实感

### 优化版（五官细化）
```
almond eyes, epicanthic fold, bedroom eyes, heavy eyelids,
small nose, flat bridge,
parted lips, glossy lips, wet lips,
(wet skin:1.3), (shiny skin:1.3), skin pores, water drops on face
```
- 效果：迷离、性感、超真实
- 优势：水光肌 + 迷离眼神 + 湿润嘴唇 = 极致诱惑

---

## 🔧 Python 代码片段

```python
# 五官优化版基础描述
base_desc_pony_facial = """score_9, score_8_up, score_7_up, score_6_up, 
1girl, solo, 
(chinese:1.3), (east asian:1.2), 
(beautiful face:1.2), soft facial features, 
almond eyes, dark eyes, brown eyes, epicanthic fold, hooded eyelids, heavy eyelids,
looking at viewer, bedroom eyes,
small nose, flat bridge, soft nose,
parted lips, glossy lips, full lips, cherry lips, wet lips,
round face, heart-shaped face, soft jawline, 
(wet skin:1.3), (shiny skin:1.3), water drops on face, sweat, oily skin, textured skin, skin pores, dewy skin,
(wet hair:1.2), high ponytail, sidelocks, hair strands across face,
(petite body:1.2), (slender frame:1.3),
huge natural breasts, natural nipples, smooth nipples,
completely naked, wearing high heels,
(explicit:1.2), genitals, pussy, anus, rating_explicit,
photo (medium), realistic, highly detailed, cinematic lighting"""

# 五官校优版负面提示词
neg_pony_facial = """score_4, score_5, score_6, 
lowres, bad anatomy, text, error,
(western features:1.3), (deep eyes:1.2), (high nose bridge:1.2), cleft chin, (freckles:1.2), rough skin,
(clothing:1.6), (censored:1.5),
(textured nipples:1.3), (ringed nipples:1.3),
(dry skin:1.2), (matte skin:1.2),
simple background, (flat hair:1.2), (dry hair:1.1)"""
```

---

**最后更新**: 2026-02-14  
**验证状态**: ⏳ 待验证  
**适用模型**: Pony Diffusion V6 XL  
**核心改进**: 眼神迷离感 + 嘴唇性感度 + 水光肌真实感
