# Pony V6 发型优化指南 - 湿发高马尾版

## 📋 核心发型标签

### 1. 基础发型结构
```
high ponytail          # 高马尾（推荐）
ponytail              # 普通马尾
```

### 2. 湿润质感（重要）
```
(wet hair:1.2)        # 湿发效果
sweated               # 汗湿
damp hair             # 潮湿的头发
water drops on hair   # 头发上的水珠
```

### 3. 碎发与修饰（关键细节）
```
sidelocks             # 鬓角垂下的长碎发
hair strands          # 散乱发丝
hair strands across face  # 脸颊旁的发丝
sweeping bangs        # 扫过的刘海
mismatch bangs        # 不规则刘海
forehead              # 露额头
```

### 4. 头发质感
```
black hair            # 黑发
shiny hair            # 有光泽的头发
dark hair             # 深色头发
glossy hair           # 光滑头发
```

---

## 🌟 皮肤与光影增强

### 湿润皮肤效果
```
shiny skin            # 有光泽的皮肤
water drops on face   # 脸上的水珠
sweat                 # 汗水
sweating              # 出汗
damp                  # 潮湿
oily skin             # 油光皮肤
skin pores            # 皮肤毛孔（增强真实感）
```

### 光影表现
```
cinematic lighting    # 电影级光影
rim lighting          # 轮廓光
side lighting         # 侧光
dramatic lighting     # 戏剧性光影
```

### 首饰细节
```
earrings              # 耳环
dangling earrings     # 垂坠耳环
(jewelry:0.8)         # 首饰（低权重避免过多）
```

---

## 📝 完整提示词模板

### 正向提示词（湿发高马尾版）
```
score_9, score_8_up, score_7_up, score_6_up, 
1girl, solo, 
(chinese:1.3), (east asian:1.2), 
beautiful face, soft facial features, 
brown eyes, dark eyes, almond eyes, epicanthic fold, hooded eyelids,
small nose, flat bridge, small lips, cherry lips,
round face, heart-shaped face, soft jawline, 
(wet hair:1.2), (black hair:1.1), high ponytail, sidelocks, hair strands across face, sweeping bangs, damp hair, shiny hair, glossy hair,
forehead, mismatch bangs,
shiny skin, water drops on face, sweat, sweating, oily skin, skin pores, smooth skin, pale skin,
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2), (slim waist:1.1), (narrow shoulders:1.1),
huge natural breasts, natural nipples, smooth nipples,
earrings, dangling earrings,
completely naked, wearing high heels,
(explicit:1.2), genitals, pussy, anus, rating_explicit,
photo (medium), realistic, highly detailed, 
cinematic lighting, rim lighting, side lighting
```

### 负向提示词（发型优化版）
```
score_4, score_5, score_6, 
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, 
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,
(western features:1.3), deep eyes, high nose bridge, (freckles:1.2), cleft chin, rough skin,
(clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4),
(muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2),
(textured nipples:1.3), (ringed nipples:1.3), (areola texture:1.2), (bumpy nipples:1.2),
simple background, (flat hair:1.2), (dry hair:1.1), (perfectly styled hair:1.2)
```

---

## 🎯 关键优化点

### 1. 湿发效果的实现
- **核心标签**: `(wet hair:1.2)` + `damp hair` + `water drops on hair`
- **配合皮肤**: `shiny skin` + `water drops on face` + `sweating`
- **效果**: 营造刚洗完澡或剧烈运动后的性感湿润感

### 2. 高马尾的自然感
- **避免过于整齐**: 使用 `sidelocks` + `hair strands across face` 增加凌乱美
- **露额头**: `forehead` 标签让面部更清晰
- **不规则刘海**: `mismatch bangs` 避免死板

### 3. 光影增强
- **轮廓光**: `rim lighting` 让头发和身体轮廓更立体
- **侧光**: `side lighting` 增强湿润皮肤的质感
- **电影级**: `cinematic lighting` 提升整体氛围

### 4. 皮肤细节
- **毛孔**: `skin pores` 增加超真实感
- **油光**: `oily skin` 配合湿发营造性感
- **水珠**: `water drops on face` 点睛之笔

---

## 🚫 负面提示词重点

### 必须抑制的发型问题
```
(flat hair:1.2)           # 扁平头发
(dry hair:1.1)            # 干燥头发
(perfectly styled hair:1.2)  # 过于完美的发型
simple background         # 简单背景（避免模型偷懒）
```

---

## 💡 使用场景建议

### 适合的场景
1. **浴后场景**: 刚洗完澡，湿发披肩或扎起
2. **运动后**: 大汗淋漓，头发湿透
3. **性爱场景**: 激烈运动后的凌乱湿发
4. **受虐场景**: 汗水、泪水混合的湿润感

### 不适合的场景
- 正式场合（需要干爽整齐的发型）
- 户外干燥环境（湿发不合理）

---

## 📊 对比效果

### 原版（干发齐刘海）
```
long straight black hair, shiny hair, blunt bangs
```
- 效果：整齐、干净、学生气
- 适合：日常、清纯风格

### 优化版（湿发高马尾）
```
(wet hair:1.2), high ponytail, sidelocks, hair strands across face, 
sweeping bangs, forehead, shiny skin, water drops on face, sweating
```
- 效果：性感、凌乱、真实
- 适合：性爱、受虐、运动场景

---

## 🔧 快速调用

### Python 代码片段
```python
# 湿发高马尾版基础描述
base_desc_pony_wet = """score_9, score_8_up, score_7_up, score_6_up, 
1girl, solo, 
(chinese:1.3), (east asian:1.2), 
beautiful face, soft facial features, 
brown eyes, dark eyes, almond eyes, epicanthic fold, hooded eyelids,
small nose, flat bridge, small lips, cherry lips,
round face, heart-shaped face, soft jawline, 
(wet hair:1.2), (black hair:1.1), high ponytail, sidelocks, hair strands across face, sweeping bangs, damp hair, shiny hair,
forehead, mismatch bangs,
shiny skin, water drops on face, sweat, sweating, oily skin, skin pores, smooth skin, pale skin,
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2),
huge natural breasts, natural nipples, smooth nipples,
earrings, dangling earrings,
completely naked, wearing high heels,
(explicit:1.2), genitals, pussy, anus, rating_explicit,
photo (medium), realistic, highly detailed, 
cinematic lighting, rim lighting, side lighting"""

# 发型优化版负面提示词
neg_pony_wet = """score_4, score_5, score_6, 
lowres, bad anatomy, bad hands, text, error, 
(western features:1.3), deep eyes, high nose bridge,
(clothing, clothes:1.6), (censored:1.5),
(textured nipples:1.3), (ringed nipples:1.3),
simple background, (flat hair:1.2), (dry hair:1.1), (perfectly styled hair:1.2)"""
```

---

**最后更新**: 2026-02-14  
**验证状态**: ⏳ 待验证  
**适用模型**: Pony Diffusion V6 XL
