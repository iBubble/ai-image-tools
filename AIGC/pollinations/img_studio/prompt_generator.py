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

# 维度1：场景环境
SCENES = [
    "废弃教堂内部, 彩色玻璃窗透射圣光",
    "雨夜东京霓虹巷弄, 积水倒影",
    "古堡地下石室, 铁链悬挂墙壁",
    "日式温泉旅馆, 榻榻米与竹帘",
    "工业废墟, 锈蚀钢梁与碎玻璃",
    "暗红丝绒歌剧院包厢",
    "月光下荒芜墓园, 枯树与迷雾",
    "极简白色摄影棚, 柔光箱环绕",
    "蒸汽朋克飞艇内舱, 齿轮与黄铜管道",
    "冰雪覆盖的北欧木屋壁炉旁",
    "赛博朋克霓虹酒吧, 全息投影吧台",
    "中式祠堂, 红烛与牌位",
    "荒漠黄昏, 废弃公路与生锈路牌",
    "深海潜艇指挥室, 蓝绿冷光",
    "维多利亚风格阁楼, 蕾丝窗帘与古董镜",
    "地下格斗场, 铁笼与射灯",
    "废弃游泳池, 龟裂瓷砖与枯叶",
    "哥特式图书馆, 旋转铁梯与皮革古籍",
    "暴风雨中的灯塔顶层, 旋转透镜",
    "昏暗的审讯室, 单灯照射",
    "樱花飘落的京都庭院, 石灯笼",
    "午夜高速公路天桥下, 汽车尾灯拖影",
    "废弃医院走廊, 闪烁的荧光灯",
    "奢华红色密室, 天鹅绒墙面与金色镜框",
    "暴雨倾盆的天台, 城市灯火为背景",
    "迷幻夜总会舞池, 激光与烟雾",
    "古罗马浴场遗迹, 残破石柱与藤蔓",
    "潮湿的地下隧道, 滴水与回声",
    "落地窗前的高层套房, 城市夜景180度环绕",
    "竹林深处的禅修小屋, 焚香缭绕",
    # ── 室外 / 广场 / 夜景 ──
    "深夜无人的城市广场, 喷泉水雾与路灯光晕",
    "废弃游乐场旋转木马前, 锈蚀彩灯闪烁",
    "月光下的海边栈桥, 潮水拍打木桩",
    "雨后街头十字路口, 湿润柏油路面反射霓虹",
    "午夜空旷停车场, 单盏路灯投射孤独光圈",
    "城市天台泳池边, 无边际水面倒映星空",
    "荒野铁路交叉口, 废弃信号灯与生锈道轨",
    "热带雨林瀑布下, 水雾弥漫岩石湿滑",
    "夜晚摩天轮最高处车厢内, 俯瞰万家灯火",
    "废弃加油站, 荒漠与破碎的霓虹招牌",
    "月色下的欧式石桥, 河面波光粼粼",
    "暴风雪中的旷野, 白茫茫一片只剩身体轮廓",
    "夜樱隧道, 花瓣纷飞与地面灯带",
    "码头集装箱阵列间, 工业吊臂与海风",
    "深夜公园长椅旁, 老式路灯与梧桐落叶",
    "悬崖边废弃瞭望台, 脚下是万丈深渊与云海",
    "午夜街头涂鸦墙前, 荧光喷漆与铁丝网",
    "沙漠绿洲月夜, 棕榈树影与星轨",
    "雾中森林空地, 枯木与苔藓覆盖石碑",
    "都市立交桥下, 车流光轨与混凝土柱阵",
]

# 维度2：姿态动作
POSES = [
    "双臂高举过头反绑, 被迫踮脚站立",
    "跪伏于地, 额头贴地臀部高翘",
    "悬吊于空中, 身体呈弓形后仰",
    "M字开腿固定在木架上, 完全暴露",
    "倒悬于绳索, 长发垂落触地",
    "背缚双手, 被迫弯腰前倾",
    "四肢展开大字型固定于十字架",
    "侧卧蜷缩, 双膝并拢被绳缚住",
    "单腿高悬, 身体旋转失去平衡",
    "骑跨于三角木马, 双手反绑身后",
    "后仰悬吊, 头部低垂发丝散乱",
    "蹲踞姿势, 双腕绑于脚踝",
    "站立展示, 双手被缚于背后高举",
    "匍匐爬行姿态, 项圈连接牵引链",
    "坐于椅上, 四肢分别固定于椅腿",
    "半悬空状态, 仅臀部着地",
    "倚墙站立, 双臂被铁链高挂",
    "趴伏于桌面, 上半身悬空探出",
    "劈叉姿势, 双腿被固定杆撑开",
    "单膝跪地, 另一腿被绳索向后拉起",
    "双手合十被缚, 呈祈祷姿势跪坐",
    "仰面朝天, 身体架于两张桌子之间",
    "蜷缩于铁笼内, 身体扭曲挤压",
    "高跪姿势, 脊背挺直双手扣于颈后",
]

# 维度3：束缚方式
BONDAGE = [
    "精密日式麻绳龟甲缚, 绳痕深陷肌肤",
    "厚重黑色皮革束缚带, 金属锁扣闪光",
    "银色锁链与铁镣, 叮当碰撞",
    "透明渔网紧身束缚, 网格勒入柔软肌肤",
    "红色丝绸绑缚, 蝴蝶结点缀",
    "黑色乳胶包裹束缚, 反光材质紧贴身体",
    "荆棘铁丝交织缠绕, 危险与美感并存",
    "古旧粗麻绳捆缚, 沧桑质感",
    "医疗级白色绷带层层缠绕",
    "金色锁链与宝石装饰束缚, 奢华感",
    "电击项圈配合导线连接四肢",
    "木制枷锁框架, 中世纪刑具风格",
    "多层彩色绳艺编织, 艺术感十足",
    "钢制固定夹具与可调节支架组合",
    "柔软天鹅绒手铐与脚铐套装",
    "弹力绷带紧密包裹, 限制活动但不勒痕",
    "链条与钩环组合, 工业感吊缚",
    "藤条编织束缚, 自然质感",
    "荧光绳索, 在紫外灯下发光",
    "皮带与金属环扣复合束缚系统",
]

# 维度4：表情状态
EXPRESSIONS = [
    "含泪隐忍, 咬住下唇不让声音泄出",
    "迷离涣散的目光, 意识模糊的陶醉",
    "倔强不屈的凝视, 眼含怒火",
    "羞耻性潮红, 不敢直视镜头",
    "嘴角微微上扬的受虐快感",
    "惊恐与期待交织的表情",
    "完全放空, 灵魂出窍般的失神",
    "痛苦扭曲但强忍的极限表情",
    "妩媚挑逗的斜眼凝视, 明显在享受",
    "汗水淋漓, 呼吸急促的喘息",
    "泪痕满面但嘴唇翘起的矛盾微笑",
    "紧闭双眼, 牙关紧咬承受中",
    "half-lidded bedroom eyes, 慵懒而危险",
    "绝望的哀求眼神, 无声呐喊",
    "冷漠而傲慢, 即使被缚仍不屈服",
    "面无表情的空洞, 如同人偶",
    "极度羞耻到脸颊绯红延至耳根颈部",
    "嘴被堵住, 只能发出呜咽的鼻音",
    "挑衅的笑容, 仿佛一切尽在掌控",
    "恍惚中的微笑, 进入subspace深层空间",
]

# 维度5：服饰状态
OUTFITS = [
    "残破的白色衬衫, 扣子崩开露出线条",
    "黑色蕾丝内衣, 若隐若现",
    "全透明薄纱睡裙, 什么都遮不住",
    "JK制服, 百褶裙被撩起",
    "修女服被撕裂, 禁忌与亵渎",
    "紧身旗袍开叉到腰, 东方诱惑",
    "完全赤裸, 仅余项圈与脚环",
    "银色金属内衣, 未来感铠甲",
    "破损的芭蕾舞裙, 蕾丝花边脱落",
    "浴衣松散敞开, 腰带半解",
    "黑色紧身皮衣, 拉链半开",
    "哥特洛丽塔长裙, 层叠蕾丝与缎带",
    "护士制服, 被剪开暴露",
    "办公室西装套裙, 被粗暴扯乱",
    "中国古典肚兜, 红色丝绸薄如蝉翼",
    "和服被扒至肩下, 露出锁骨与肩胛",
    "军装外套半搭, 内里真空",
    "拉拉队制服, 百褶短裙与紧身上衣",
    "全身渔网袜与高跟鞋, 别无其他",
    "白色婚纱, 被绳索勒出痕迹",
    "女仆装束, 围裙被扯歪蕾丝头饰歪斜",
    "淋湿的白T恤, 完全透明贴合身体",
]

# 维度6：光影氛围
LIGHTING = [
    "单一红色聚光灯, 强烈明暗对比",
    "柔和的壁炉暖光, 金色氛围",
    "冷蓝月光从高窗倾泻, 银白阴影",
    "霓虹粉紫双色交叉照明",
    "蜡烛摇曳的微光, 阴影不断游移",
    "刺目的审讯灯, 白到失真",
    "暴风雨闪电照亮瞬间, 剧烈明暗交替",
    "日式和纸灯笼散射的暖橙光",
    "紫外灯黑光, 荧光元素发光",
    "逆光剪影效果, 只能看到身体轮廓",
    "柔和的自然窗光, 丁达尔效应光束",
    "多色舞台追光, 戏剧感拉满",
    "深夜台灯微弱光芒, 大面积暗影",
    "水下透光效果, 波光粼粼投射身体",
    "伦勃朗布光, 半脸明半脸暗的经典画意",
    "环形灯正面照射, 瞳孔中映射光环",
    "火焰光影, 跳动的橙红色映照全身",
    "冰蓝与暖橙撕裂式双色光",
]

# 维度7：镜头角度
CAMERA = [
    "(全身正面镜头:1.5), 从头到脚完整展示",
    "(低角度仰拍:1.3), 强调压迫感与气势",
    "(俯瞰鸟瞰:1.3), 从上方审视",
    "(特写面部:1.4), 捕捉微表情",
    "(侧面剪影:1.3), 优美曲线",
    "(45度斜侧全身:1.4), 黄金视角",
    "(广角透视:1.3), 场景与人物并重",
    "(背面回眸:1.3), 性感脊背线条",
    "(dutch angle 倾斜构图:1.2), 不安定感",
    "(极近距离微距:1.3), 皮肤纹理与绳痕",
    "(全身侧面轮廓:1.4), 曲线分明",
    "(从下方透过玻璃地板仰拍:1.2), 独特视角",
    "(鱼眼镜头:1.2), 画面畸变张力",
    "(中景半身:1.3), 从腰部以上特写",
    "(360度环绕感:1.2), 多角度呈现",
    "(对角线构图:1.3), 动态平衡",
]

# 维度8：辅助道具
PROPS = [
    "口球与皮质面罩",
    "猫耳发箍与铃铛项圈",
    "蜡烛与滴蜡痕迹",
    "皮鞭与教鞭搭配",
    "眼罩蒙眼, 感官剥夺",
    "冰块与热蜡对比刺激",
    "口枷与涎水流淌",
    "兔尾肛塞与兔耳头箍",
    "振动棒固定在敏感部位",
    "乳夹与细链连接",
    "玫瑰花瓣散落全身",
    "蝴蝶结贴纸装饰身体",
    "手持式电击棒, 蓝色电弧",
    "羽毛与冰块, 温柔折磨",
    "金属肛钩与绳索连接后脑",
    "尾巴插件随身体晃动",
    "皮质狗牌项圈刻有主人名字",
    "丝带缠绕手指与脚趾",
    "棉绳在口中勒出深痕",
    "木制打板与红肿印痕",
    "透明亚克力固定架",
    "古典铁制脚镣与地面锚点",
    "绣有名字的皮质颈带",
    "双头牵引链连接项圈与腰带",
]


# ━━━━━━━━━━━━━━━━━ 主题模板 ━━━━━━━━━━━━━━━━━
# 可选主题模式，约束某些维度的范围

THEMES = {
    "gothic": {
        "scene_filter": ["教堂", "墓园", "古堡", "图书馆", "维多利亚", "哥特"],
        "extra": "哥特美学, 暗黑浪漫, 荆棘与玫瑰元素",
    },
    "cyberpunk": {
        "scene_filter": ["赛博", "霓虹", "夜总会", "潜艇", "高速"],
        "extra": "赛博朋克2077风格, 机械义体, 全息HUD投影",
    },
    "japanese": {
        "scene_filter": ["日式", "温泉", "京都", "竹林", "樱花"],
        "extra": "日式绳艺美学, 侘寂意境, 浮世绘配色",
    },
    "industrial": {
        "scene_filter": ["工业", "废墟", "地下", "格斗", "审讯", "隧道"],
        "extra": "工业废土风, 铁锈质感, 粗粝的美",
    },
    "luxury": {
        "scene_filter": ["奢华", "歌剧", "高层", "密室", "丝绒", "泳池"],
        "extra": "极致奢华, 金箔与钻石, 名媛堕落",
    },
    "urban_night": {
        "scene_filter": ["街头", "广场", "停车场", "立交桥", "涂鸦", "霓虹",
                         "天台", "公园", "摩天轮", "十字路口", "高速"],
        "extra": "都市暗夜美学, 湿润柏油路面反光, 孤独而危险的氛围",
    },
    "wilderness": {
        "scene_filter": ["荒漠", "瀑布", "悬崖", "森林", "雪", "海边",
                         "旷野", "铁路", "绿洲", "栈桥"],
        "extra": "旷野求生感, 人与自然的极限对抗, 原始野性",
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
                if any(kw in item for kw in keywords)]
    return filtered if filtered else pool  # 无匹配时退化为全池


def generate_random_prompt(
    theme: Optional[str] = None,
    max_retries: int = 10
) -> str:
    """生成随机提示词

    Args:
        theme: 可选主题 (gothic/cyberpunk/japanese/industrial/luxury)
        max_retries: 去重最大重试次数

    Returns:
        组合好的中文提示词字符串
    """
    result = generate_random_prompt_with_meta(theme, max_retries)
    return result["prompt"]


def generate_random_prompt_with_meta(
    theme: Optional[str] = None,
    max_retries: int = 10
) -> dict:
    """生成随机提示词（带元数据）

    Returns:
        dict: {
            "prompt": str,      # 完整提示词
            "theme": str|None,  # 使用的主题
            "dimensions": dict, # 各维度选中内容
        }
    """
    global _recent_combos

    theme_cfg = THEMES.get(theme) if theme else None

    for attempt in range(max_retries):
        # 场景（主题过滤）
        scene_pool = SCENES
        if theme_cfg and theme_cfg.get("scene_filter"):
            scene_pool = _filter_by_keywords(
                SCENES, theme_cfg["scene_filter"]
            )
        scene = random.choice(scene_pool)

        # 各维度随机抽取
        pose = random.choice(POSES)
        bondage = random.choice(BONDAGE)
        expression = random.choice(EXPRESSIONS)
        outfit = random.choice(OUTFITS)
        lighting = random.choice(LIGHTING)
        camera = random.choice(CAMERA)

        # 道具：有30%概率选2个，增加丰富度
        if random.random() < 0.3:
            props_picked = _pick_unique(PROPS, 2)
            prop = ", ".join(props_picked)
        else:
            prop = random.choice(PROPS)

        # 生成指纹检查重复
        indices = {
            "s": SCENES.index(scene) if scene in SCENES else -1,
            "p": POSES.index(pose),
            "b": BONDAGE.index(bondage),
            "e": EXPRESSIONS.index(expression),
            "o": OUTFITS.index(outfit),
        }
        fp = _combo_fingerprint(indices)
        if fp not in _recent_combos:
            _recent_combos.append(fp)
            if len(_recent_combos) > _MAX_HISTORY:
                _recent_combos = _recent_combos[-_MAX_HISTORY:]
            break
    # 即使重试耗尽也返回（极低概率）

    # 组装提示词
    parts = [
        camera,
        scene,
        outfit,
        pose,
        bondage,
        expression,
        prop,
        lighting,
    ]

    # 追加主题修饰词
    if theme_cfg and theme_cfg.get("extra"):
        parts.append(theme_cfg["extra"])

    # 追加品质增强词
    quality = ("电影质感, 极致细节, 超高画质, "
               "专业摄影级, 浅景深虚化, 胶片颗粒感")
    parts.append(quality)

    prompt = ", ".join(parts)

    dimensions = {
        "scene": scene,
        "pose": pose,
        "bondage": bondage,
        "expression": expression,
        "outfit": outfit,
        "lighting": lighting,
        "camera": camera,
        "props": prop,
    }

    return {
        "prompt": prompt,
        "theme": theme,
        "dimensions": dimensions,
    }
