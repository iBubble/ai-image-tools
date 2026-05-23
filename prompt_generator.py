#!/usr/bin/env python3
"""多维度组合式提示词引擎 — Prompt Generator v2

设计理念：8大维度 × 每维度15-30选项 = 数千万种不重复组合
维度：场景环境、姿态动作、束缚方式、表情状态、服饰状态、光影氛围、镜头角度、辅助道具

使用方式：
    from prompt_generator import generate_random_prompt
    prompt = generate_random_prompt()       # 全随机
    prompt = generate_random_prompt(theme="gothic")  # 指定主题
"""

import random
from typing import Optional


# ━━━━━━━━━━━━━━━━━ 维度定义 ━━━━━━━━━━━━━━━━━
# 每个维度都是一个列表，随机抽取1-2个元素组合

# 维度1：场景环境 (Asian/JAV Focus)
SCENES = [
    "love hotel pink room, rotating bed, ceiling mirror",
    "traditional tatami room, futon on floor, shoji screens",
    "hot spring onsen, outdoor bath, steam rising, bamboo fence",
    "empty classroom after school, sunset light, student desks",
    "crowded Tokyo subway interior, last train atmosphere",
    "office cubicle, late night overtime, documents scattered",
    "clinic office, medical equipment",
    "AV studio, filming set, camera equipment visible, studio lights",
    "magic mirror bus interior, one-way mirror, hidden camera feel",
    "convenience store back room, cardboard boxes, fluorescent light",
    "karaoke booth, neon lights, tambourine on table",
    "gym storage room, sports equipment, mats",
    "rooftop at night, city skyline background, chain link fence",
    "private onsen bath, wooden bucket, steamy atmosphere",
    "manga cafe private booth, computer screen glow",
    "dressing room, costume rack, vanity mirror",
    "audition room, casting sofa, video camera on tripod",
    "narrow back alley, neon signs, wet pavement",
    "high-rise apartment balcony, night city lights",
    "shrine quarters, wooden corridor, paper lanterns",
    "interrogation room, single hanging light, metal table",
    "underground club VIP room, dark leather sofa",
    "abandoned warehouse, industrial chains, concrete floor",
    "luxury hotel suite, city view, velvet curtains",
    "public bath sento, tiled walls, washing stools",
]

# 维度2：姿态动作 (Functional Categories)
POSES = [
    "kneeling, head bowed, submissive posture",
    "kneeling, wrists bound behind back, looking up",
    "on all fours, back arched, presenting, looking over shoulder",
    "sitting with legs spread wide, one hand on thigh",
    "lying on back, legs raised and spread, helpless",
    "standing pressed against wall, hands above head",
    "sitting on edge of bed, leaning back on elbows",
    "kneeling between legs, mouth open, tongue out",
    "lying on stomach, face down ass up, pillow under hips",
    "squatting, looking at camera, hands between knees",
    "standing bent over desk, presenting from behind",
    "sitting on lap, arms wrapped around neck",
    "suspended in air by ropes, body arched",
    "m-shape leg spread, sitting on floor, exposed",
    "kneeling, forehead touching floor, deep submissive bow",
    "standing on tiptoe, back arched, arms tied to ceiling",
    "lying on side, fetal position, rope bound",
    "crawling toward viewer, seductive gaze",
    "sitting on desk, legs dangling, knees spread wide",
    "standing in shower, water running down body, looking up",
]

# 维度3：束缚方式 (Kinbaku & Modern)
BONDAGE = [
    "intricate Japanese shibari, hemp rope patterns, tight knots",
    "suspension bondage, hanging from ceiling, elaborate rope harness",
    "heavy leather straps, metal buckles, black leather",
    "silver chains and handcuffs, clinking metal",
    "red silk ribbons, elegant bow ties",
    "intricate latex wrapping straps, body compression restraints",
    "medical bandages, wrapped from head to toe",
    "wooden kokeshi-style stocks, restricted movement",
    "nylon zip ties, clinical and cold",
    "transparent cling wrap bondage, shimmering plastic",
    "gold chains, luxury jewelry bondage",
    "velvet padded restraints, soft but firm",
    "intricate shell-shaped rope tie, chest harness",
    "hogtie, wrists and ankles bound together behind back",
    "cleave gag, leather strap across mouth",
]

# 维度4：表情状态 (11 Emotional Categories)
EXPRESSIONS = [
    "shy expression, blushing cheeks, looking away",
    "sultry gaze, bedroom eyes, seductive smile",
    "ecstatic expression, pleasure face, eyes rolling back",
    "submissive look, pleading eyes, awaiting command",
    "playful smile, winking, tongue out playfully",
    "pained expression, grimacing, biting lip to endure",
    "shocked expression, caught off guard, eyes wide in panic",
    "dazed expression, glazed eyes, post-orgasm stupor",
    "biting back moans, tensed jaw, hand over mouth",
    "bored expression, deadpan face, mechanical compliance",
    "innocent face but aroused body, shy smile but legs spread",
    "heavily blushing, ears turning red, unable to hold eye contact",
    "lust-blind stare, wanton expression, nympho smile",
    "tearful eyes from pleasure, mascara smudged",
    "half-lidded bedroom eyes,慵懒而危险",
]

# 维度5：服饰状态 (彻底全裸化)
OUTFITS = [
    "completely naked",
    "completely nude",
    "nude",
    "nude body",
    "completely bare and naked",
    "exposed nude body",
]

# 维度6：光影氛围 (Erotic & Professional)
LIGHTING = [
    "warm golden hour sunlight, Tyndall effect beams",
    "neon pink and blue split lighting, cyberpunk vibe",
    "moody low-key lighting, deep shadows, single spotlight",
    "soft window light, gentle morning glow",
    "flickering candlelight, warm dancing shadows",
    "harsh interrogation light, stark white contrast",
    "rim light highlighting body curves, dark background",
    "red club lighting, hazy atmosphere, smoke",
    "moonlight filtering through shoji screens",
    "cinematic film lighting, softbox diffusion",
]

# 维度7：镜头角度 & 景别 (Combined)
CAMERA = [
    "(full body shot:1.4), eye level, neutral angle",
    "(waist-up medium shot:1.3), low angle, looking up",
    "(face close-up:1.5), shallow depth of field, focus on eyes",
    "(bird's eye view:1.3), looking down from above",
    "(POV perspective:1.5), first person view, immersive",
    "(voyeuristic angle:1.4), peeping through crack, hidden camera",
    "(upskirt angle:1.3), low camera position, looking up",
    "(between legs shot:1.4), crotch-level view",
    "(over the shoulder:1.2), intimate perspective",
    "(dutch angle:1.2), tilted frame, tension",
]

# 维度8：辅助道具 & 细节
PROPS = [
    "ball gag and leather mask",
    "cat ears and bell collar",
    "wax dripping marks on skin",
    "riding crop and paddle",
    "blindfold, sensory deprivation",
    "vibrator attached to sensitive areas",
    "nipple clamps with fine chains",
    "handcuffs and ankle restraints",
    "rope coils on floor, messy environment",
    "pillows scattered on messy bed",
    "smartphone in hand, taking selfie",
    "video camera on tripod in background",
]

# 维度9：真实感细节 (Realism / Imperfections)
REALISM = [
    "visible skin pores, subtle freckles on nose",
    "beauty mark above lip, small mole on neck",
    "faint stretch marks on hips, natural skin texture",
    "sweat beads on forehead, glistening skin",
    "flushed cheeks, friction redness on inner thighs",
    "stray hair strands across face, messy bedhead",
    "rope indent marks on shoulders and skin",
    "faint scar on thigh, blue veins visible on breast",
]

# 维度10：液体系统 (Controlled Quantity)
LIQUIDS = [
    "single drop of translucent fluid on nipple",
    "thin cum streak on inner thigh, glistening",
    "faint saliva trail from mouth corner",
    "subtle wetness on inner labia, glistening",
    "small beads of sweat rolling down cleavage",
    "tiny milk droplet forming at nipple tip",
    "thin glistening trail of arousal",
]

# 维度11：拍摄设备 & 画质 (Equipment Data)
EQUIPMENT = [
    {"name": "iPhone photo, selfie", "quality": "high quality, smartphone photography"},
    {"name": "DSLR photo, professional camera", "quality": "masterpiece, best quality, 8k, photorealistic"},
    {"name": "35mm film camera, analog photo", "quality": "film grain, vintage color, analog style"},
    {"name": "CCTV surveillance footage, grainy", "quality": "low resolution, security camera, timestamp"},
    {"name": "hidden spy camera, pinhole lens", "quality": "grainy, hidden camera feel, wide angle distortion"},
    {"name": "Polaroid instant film", "quality": "faded colors, polaroid border, instant film texture"},
]

# 维度12：胶片风格 (Film Styles)
FILM_STYLES = [
    "Kodak Portra 400, warm skin tones, fine grain",
    "Fuji Superia, slightly green shadows, nostalgic",
    "Classic Negative, retro muted colors, 90s feel",
    "Kodak Gold 200, golden hour warmth, snapshot vibe",
    "Ilford HP5, high contrast black and white, gritty grain",
    "Agfa Vista, vibrant reds and blues, saturated",
]


# ━━━━━━━━━━━━━━━━━ 主题模板 ━━━━━━━━━━━━━━━━━
# 可选主题模式，约束某些维度的范围
THEMES = {
    "jav_audition": {
        "scene_filter": ["audition room", "AV studio", "dressing room"],
        "extra": "casting couch, nervous atmosphere, high contrast studio lighting",
    },
    "love_hotel": {
        "scene_filter": ["love hotel", "pink room", "tatami"],
        "extra": "neon glow, messy sheets, erotic atmosphere",
    },
    "office_lady": {
        "scene_filter": ["office cubicle", "interrogation room"],
        "extra": "corporate atmosphere, workplace taboo, desk bondage",
    },
    "school_girl": {
        "scene_filter": ["classroom", "gym storage", "rooftop"],
        "extra": "after school, youthful atmosphere, nostalgic sunset light",
    },
    "hospital": {
        "scene_filter": ["nurse office", "hospital bed"],
        "extra": "clinical setting, medical play, cold fluorescent lighting",
    },
    "onsen": {
        "scene_filter": ["onsen", "private onsen", "tatami"],
        "extra": "steamy atmosphere, wet skin, traditional Japanese aesthetic",
    },
    "gothic": {
        "scene_filter": ["abandoned warehouse", "underground club"],
        "extra": "dark aesthetic, heavy ropes, kinbaku mastery",
    },
}


# ━━━━━━━━━━━━━━━━━ 去重历史（内存LRU） ━━━━━━━━━━━━━━━━━
_recent_combos = []  # 最近50次生成的组合指纹
_MAX_HISTORY = 50


def _combo_fingerprint(indices: dict) -> str:
    """生成组合指纹，用于去重"""
    return "|".join(f"{k}:{v}" for k, v in sorted(indices.items()))


def _pick_unique(pool: list, count: int = 1) -> list:
    """从池中随机抽取不重复的元素"""
    count = min(count, len(pool))
    return random.sample(pool, count)


def _filter_by_keywords(pool: list, keywords: list) -> list:
    """按关键词过滤，返回包含任一关键词的元素"""
    filtered = [item for item in pool
                if any(kw.lower() in str(item).lower() for kw in keywords)]
    return filtered if filtered else pool  # 无匹配时退化为全池


def generate_random_prompt(
    theme: Optional[str] = None,
    max_retries: int = 10
) -> str:
    """生成随机提示词"""
    result = generate_random_prompt_with_meta(theme, max_retries)
    return result["prompt"]


def generate_random_prompt_with_meta(
    theme: Optional[str] = None,
    max_retries: int = 10
) -> dict:
    """生成随机提示词（带元数据） - 采用亚洲/JAV专业组装逻辑"""
    global _recent_combos

    theme_cfg = THEMES.get(theme) if theme else None

    for attempt in range(max_retries):
        # 1. 场景过滤
        scene_pool = SCENES
        if theme_cfg and theme_cfg.get("scene_filter"):
            scene_pool = _filter_by_keywords(SCENES, theme_cfg["scene_filter"])
        scene = random.choice(scene_pool)

        # 2. 服饰过滤
        outfit_pool = OUTFITS
        if theme_cfg and theme_cfg.get("outfit_filter"):
            outfit_pool = _filter_by_keywords(OUTFITS, theme_cfg["outfit_filter"])
        outfit = random.choice(outfit_pool)

        # 3. 基础维度随机抽取
        pose = random.choice(POSES)
        bondage = random.choice(BONDAGE)
        expression = random.choice(EXPRESSIONS)
        lighting = random.choice(LIGHTING)
        camera = random.choice(CAMERA)
        realism = random.choice(REALISM)
        
        # 4. 拍摄设备与画质联动
        equipment = random.choice(EQUIPMENT)
        film = random.choice(FILM_STYLES)

        # 5. 道具与液体（概率触发）
        prop = random.choice(PROPS) if random.random() < 0.7 else ""
        liquid = random.choice(LIQUIDS) if random.random() < 0.4 else ""

        # 生成指纹检查重复
        indices = {
            "s": scene,
            "o": outfit,
            "p": pose,
            "b": bondage,
        }
        fp = _combo_fingerprint(indices)
        if fp not in _recent_combos:
            _recent_combos.append(fp)
            if len(_recent_combos) > _MAX_HISTORY:
                _recent_combos = _recent_combos[-_MAX_HISTORY:]
            break

    # 6. 按照专业顺序组装 (Assembly Line Order)
    parts = []
    parts.append(camera)
    parts.append(f"in {scene}")
    parts.append(equipment["name"])
    parts.append(outfit)
    parts.append(realism)
    parts.append(pose)
    parts.append(expression)
    parts.append(bondage)
    if prop: parts.append(prop)
    if liquid: parts.append(liquid)
    parts.append(lighting)
    parts.append(film)
    
    if theme_cfg and theme_cfg.get("extra"):
        parts.append(theme_cfg["extra"])
        
    parts.append(equipment["quality"])

    prompt = ", ".join([p for p in parts if p])

    dimensions = {
        "scene": scene,
        "pose": pose,
        "bondage": bondage,
        "expression": expression,
        "outfit": outfit,
        "lighting": lighting,
        "camera": camera,
        "props": prop,
        "realism": realism,
        "liquid": liquid,
        "equipment": equipment["name"],
        "film": film
    }

    return {
        "prompt": prompt,
        "theme": theme,
        "dimensions": dimensions,
    }
