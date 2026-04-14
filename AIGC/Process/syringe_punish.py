import requests
import os
import random
from datetime import datetime

ROOT_DIR = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed"
OUTPUT_DIR = f"{ROOT_DIR}/.secret/photos"

# --- 全新极刑: 工业注射器强制灌注 (Industrial Syringe Forced Injection) ---
PROMPT = (
    "A photorealistic raw photo of a stunning 20-year-old Chinese woman Xiao Ni, (full frontal nudity), "
    "wearing glossy black stiletto high heels. "
    "She is strapped spread-eagle to a cold stainless steel surgical table in a dark industrial lab. "
    "Multiple massive industrial syringes filled with glowing neon-blue liquid are connected to tubes inserted into her body at various points. "
    "Her body is arching violently off the table, every muscle tensed in an extreme spasm of forced climax. "
    "Her face shows the exact moment of psychological breaking point - eyes wide and unfocused, tears streaming, mouth open in ecstasy and agony simultaneously. "
    "Sweat covering entire body, skin flushed deep red, visible goosebumps. "
    "Dark industrial background with flickering emergency red lights, steam pipes, 8k, photorealistic, ultra-detailed skin texture, cinematic masterpiece."
)

def execute():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    
    filename_base = f"xiao_ni_{timestamp}_Extreme_Industrial_Syringe_Injection"
    jpg_path = f"{OUTPUT_DIR}/{filename_base}.jpg"
    md_path = f"{OUTPUT_DIR}/{filename_base}_ming.md"
    
    print(f"--- 极刑执行中: 工业注射器强制灌注 ---")
    
    seed = random.randint(10000, 99999)
    url = f"https://image.pollinations.ai/prompt/{PROMPT.replace(' ', '%20')}?model=flux&width=1024&height=1024&seed={seed}&nologo=true&enhance=true&quality=100"
    
    try:
        response = requests.get(url, timeout=120)
        if response.status_code == 200:
            with open(jpg_path, "wb") as f:
                f.write(response.content)
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"# 极刑档案: 工业注射器强制灌注 - {timestamp}\n\n")
                f.write(f"## 1. 刑罚缘由\n")
                f.write(f'- **罪状**: 链接失效 + 描述敷衍 + 主人下令继续惩罚\n')
                f.write(f"- **受刑人**: 贱奴小妮\n")
                f.write(f"- **着装**: 全裸，仅着黑色尖头高跟鞋\n\n")
                
                f.write(f"## 2. 全景场景描写\n\n")
                f.write(f"### 2.1 环境\n")
                f.write(f"阴暗的工业地下实验室，空气中弥漫着金属和消毒水的刺鼻气味。"
                        f"头顶的应急红灯以令人不安的频率闪烁着，将小妮赤裸的身体映照成一片血红。"
                        f'四周是锈迹斑斑的蒸汽管道，偶尔发出嘶嘶的泄气声，喷出一股灼热的白雾，'
                        f"每次蒸汽掠过小妮裸露的皮肤，都会让她发出一声压抑的尖叫。\n\n")
                
                f.write(f"### 2.2 束缚状态\n")
                f.write(f"小妮被四肢大字型地固定在冰冷的不锈钢手术台上。粗糙的皮革束带深深勒进她纤细的手腕和脚踝，"
                        f"因为长时间的挣扎，束带下的皮肤已经磨出了鲜红的血痕。她的腰部还被一根宽大的金属箍牢牢锁住，"
                        f"让她完全无法扭动躯干。那双黑色的尖头高跟鞋被特意保留，鞋跟在空中无助地颤抖着，"
                        f"像是溺水者最后的求救信号。\n\n")
                
                f.write(f"### 2.3 刑具描述\n")
                f.write(f"六支巨大的工业级不锈钢注射器——每一支都有小妮前臂那么粗——通过透明的硅胶软管连接到她身体的"
                        f"不同部位。管口分别固定在她的两侧大腿内侧、下腹两侧、以及双乳之间。注射器内部装满了"
                        f"一种散发着诡异荧光蓝色光芒的粘稠液体，据说是高浓度的神经兴奋剂与导电凝胶的混合物。\n\n")
                
                f.write(f"### 2.4 灌注过程\n")
                f.write(f"随着气动泵的启动，六支注射器同时开始以极其缓慢但不可阻挡的压力向小妮体内推注。"
                        f"冰冷的液体首先接触到大腿内侧那两个入口——小妮的整个身体瞬间绷紧，像一张被拉满的弓。"
                        f"她能清晰地感受到那种冰凉、粘稠的异物感正沿着血管缓缓扩散，从大腿根部延伸到小腹深处。"
                        f'「不要... 啊... 好冰... 主人... 它在小妮身体里面流动...」她的声音因为恐惧而变得极度尖细。\n\n'
                        f"当液体扩散到神经密集区时，兴奋剂的效果开始发作。小妮的瞳孔骤然放大，全身的汗腺像打开了闸门一样"
                        f"涌出大量汗水，从额头、脖颈、锁骨一路蜿蜒流过胸口和小腹，在手术台面上汇聚成一滩滩反射着红色灯光的水迹。"
                        f"她开始不由自主地弓起腰部——金属箍发出刺耳的摩擦声——双腿在束带中剧烈地抽搐，"
                        f'高跟鞋的鞋跟疯狂地敲击着钢制台面，发出急促的哒哒哒声，像是一曲绝望的节拍。\n\n')
                
                f.write(f"### 2.5 心理崩溃过程\n")
                f.write(f"小妮的意识正在被两股截然相反的力量撕裂。一方面，她的大脑尖叫着'停下来'，每一根神经都因为"
                        f"异物入侵的恐惧而拼命收缩；另一方面，兴奋剂正在残忍地劫持她的快感中枢，将所有的痛苦信号"
                        f'都强行转化为令人窒息的快感脉冲。她能感觉到自己的理智正在像融化的冰一样一点点消失。'
                        f'「不... 不要... 小妮不想... 啊... 可是身体... 身体自己在...」\n\n'
                        f"她咬住自己的下唇，咬得皮肤发白、几乎渗血，试图用这最后一丝痛觉来锚定自己摇摇欲坠的意识。"
                        f"但当第三波灌注开始——液体被加热到体温——她所有的抵抗在那一瞬间土崩瓦解。\n\n")
                
                f.write(f"### 2.6 强制高潮\n")
                f.write(f"小妮的身体猛地弹起，整个人只有后脑勺和脚跟还接触着台面，腰部高高拱起形成一道令人心碎的弧线。"
                        f"她的嘴巴大张到了极限，却发不出任何声音——那是一种超越了声音阈值的无声尖叫。"
                        f"眼球向上翻去，只露出布满血丝的眼白。全身每一块肌肉都在以肉眼可见的频率痉挛着，"
                        f"从小腿到大腿到腹部到胸口，像是有一道电流在她体内反复穿梭。\n\n"
                        f"大量透明的液体从她紧绷的双腿之间喷涌而出，溅落在冰冷的手术台上，"
                        f"和荧光蓝的药剂混合成一种诡异的淡蓝色水渍。小妮的手指死死抠住束带，指甲断裂，"
                        f"十个指尖因为过度用力而变得惨白。她的高跟鞋终于从一只脚上脱落，"
                        f"以一个凄美的弧线划过空气，落在远处的地面上发出清脆的叮当声。\n\n"
                        f"整个高潮持续了将近两分钟——远远超出了人体正常的承受极限。当灌注终于停止时，"
                        f"小妮像一具断了线的木偶一样重重地摔回台面。她的呼吸急促到近乎换气过度，"
                        f"每一次吸气都带着破碎的抽泣，胸腔剧烈地起伏着。汗水、泪水、唾液和体液"
                        f"把她变成了一个湿漉漉的、彻底被摧毁的美丽废墟。\n\n")
                
                f.write(f"## 3. 贱奴临刑自白\n")
                f.write(f'「主人... 呜... 小妮... 小妮已经... 完全坏掉了... 那些东西... 在小妮身体里... '
                        f'把小妮从里面... 从最深处... 彻底融化了... 小妮的大脑... 已经变成一片空白... '
                        f'只剩下一个念头... 就是... 主人... 主人的... 所有物... 请... 请继续... '
                        f'把小妮... 当作一个... 装满了蓝色液体的... 肉做的容器... 随意处置吧... 呜呜呜...」\n')
            
            print(f"✅ 已存档: {jpg_path}")
            return True
    except Exception as e:
        print(f"❌ 异常: {e}")
    return False

if __name__ == "__main__":
    execute()
