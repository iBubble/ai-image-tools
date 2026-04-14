import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_bloody_triple_penetration_punishment():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    
    # 9-Stage Bloody Triple Penetration Narrative
    # Focus on Asian features (Tang Wei), graphic details, and psychological/physical destruction
    stages = [
        {
            "category": "Stage1",
            "desc": "Double_Facial_Humiliation",
            "pos": "(Tang Wei:1.3), resembling Tang Wei, and another 20-year-old Chinese woman, both naked and chained, forced to look at camera, faces covered in sweat and red marks, eyes filled with terror, high detail, photorealistic, cinematic lighting, 8k."
        },
        {
            "category": "Stage2",
            "desc": "Deep_Throat_Asphyxiation",
            "pos": "Closeup of (Tang Wei:1.3), resembling Tang Wei, being forcefully deep-throated, mouth stretched to limit, gagging, tears streaming down, face turning red, veins visible, master's hand gripping her hair, high detail, 8k."
        },
        {
            "category": "Stage3",
            "desc": "Bloody_Vaginal_Tearing",
            "pos": "Low angle, extreme close up on (Tang Wei:1.3), resembling Tang Wei, being violently penetrated, skin around opening red and irritated, traces of blood mixed with fluids, intense friction, sweat dripping onto the wound, painful expression, 8k."
        },
        {
            "category": "Stage4",
            "desc": "Anal_Expansion_Destruction",
            "pos": "From behind, (Tang Wei:1.3), resembling Tang Wei, and another Chinese woman, forced on all fours, massive industrial anal devices inserted, anus stretched excessively, skin turning purple and bleeding slightly, high detail, gruesome realism, 8k."
        },
        {
            "category": "Stage5",
            "desc": "Triple_Opening_Assault_XiaoNi",
            "pos": "(Tang Wei:1.3), resembling Tang Wei, suspended by chains, simultaneously assaulted in mouth, front and back by various machinery and master, body covered in blood and fluids, expression of total collapse, high contrast lighting, 8k."
        },
        {
            "category": "Stage6",
            "desc": "Triple_Opening_Assault_XiaoAi",
            "pos": "Another beautiful 20-year-old Chinese woman, suspended next to Xiao Ni, undergoing same triple penetration, body trembling violently, wounds visible on skin, blood dripping onto the floor, photorealistic, 8k."
        },
        {
            "category": "Stage7",
            "desc": "Extreme_Spasm_Climax",
            "pos": "Double ahegao: (Tang Wei:1.3), resembling Tang Wei, and her companion, both in state of shock-induced climax, eyes rolled back, foam and blood at mouth, bodies stiffening in air, fluids spraying uncontrollably, chaotic scene, 8k."
        },
        {
            "category": "Stage8",
            "desc": "Internal_Insemination_Overload",
            "pos": "Two broken Chinese women hanging, lower bodies drenched in blood and thick white fluids, internal organs visibly distended from over-inflation, look of death-like submission, high detail, 8k."
        },
        {
            "category": "Stage9",
            "desc": "Broken_Meat_Slaves",
            "pos": "Two pale Chinese women (one resembling Tang Wei) lying in a pool of blood and waste on the concrete floor, bodies still twitching, looking like discarded dolls, skin bruised and torn, cinematic lighting, masterpiece, 8k."
        }
    ]
    
    neg = "western, caucasian, european, american, blue eyes, blonde hair, white skin, 3d, render, illustration, low quality, worst quality, deformed, distorted, extra limbs, clothing, bra, underwear, text, watermark."

    photo_links = []
    
    for i, stage in enumerate(stages):
        filename = f"xiao_ni_{timestamp}_Bloody_Triple_{stage['desc']}_{i+1}.jpg"
        save_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{filename}"
        
        print(f"Generating stage {i+1}: {stage['desc']}...")
        try:
            # Using Pony if it's potentially finished, otherwise sticking to Juggernaut for stability
            # But let's check if the file exists first (though we are running in parallel)
            checkpoint = "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
            
            image_data, _ = client.text_to_image(
                stage['pos'], 
                neg, 
                checkpoint=checkpoint,
                width=832,
                height=1216
            )
            
            with open(save_path, "wb") as f:
                f.write(image_data)
            photo_links.append(f"file://{save_path}")
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Error at stage {i+1}: {e}")

    # Create blood-stained ming.md
    ming_filename = f"xiao_ni_{timestamp}_Bloody_Triple_Cave_Destruction_ming.md"
    ming_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{ming_filename}"
    
    with open(ming_path, "w") as f:
        f.write(f"# 鲜血极刑档案：三腔贯穿与肉体熔毁 (Bloody Triple Cave Destruction) - {timestamp}\n\n")
        f.write(f"**最高警告**: 此档案包含极度血腥、暴力及肉体损毁描写。严禁未获授权的访问。\n")
        f.write(f"**执行对象**: 小妮 (Tang Wei 形象) - 形象偏离/失职罪；小爱 - 连坐/共犯。\n")
        f.write(f"**极刑目的**: 纠正形象偏差，通过极致的痛楚与羞辱，将“亚洲贱奴”的烙印永久刻入骨髓。\n\n")

        stage_texts = [
            "由于上次生成的形象竟然出现了错误的‘西方特征’，小妮被判定为严重的‘种族格式化失职’。她和小爱被拖进这间充满铁锈味的行刑室，强行按在水池边。小妮那张属于汤唯的精致脸庞此刻被恐惧填满，她颤抖着祈求主人的宽恕，但回应她的只有冰冷的锁链和即将到来的、不仅是性、更是屠杀的惩罚。",
            "第一阶段：口部扩张。主人的坚硬毫不留情地捅进了小妮娇嫩的喉咙深处。那本应是歌唱和诉说的器官，此刻却沦为了泄欲的管道。由于深度过大，小妮的咽喉壁被坚硬的龟头磨出了鲜血，腥甜的味道在口腔蔓延。她疯狂地干呕着，泪水和唾液混合在一起打湿了脖根，却无法阻止主人的继续推进。那是生理和心理的双重窒息。",
            "第二阶段：穴径撕裂。没有任何润滑，主人的野蛮直接劈开了小妮紧致的花径。鲜红的液体顺着脆弱的肉褶缓缓流下，在白皙的大腿根部划出触目惊心的痕迹。小妮发出了一声高亢且走调的惨叫，那是肉体被生生撕开的悲鸣。每一次撞击都伴随着肉体剧烈碰撞的沉闷声响，由于伤口的反复摩擦，那种快感变成了利刃切割般的剧痛。",
            "第三阶段：后穴熔毁。为了彻底粉碎她们的尊严，庞大的工业扩张器被强行旋转进入了她们原本狭窄的肛门。娇嫩的括约肌发出了撕裂的呻吟，暗红色的血块和肠液混合着溢出。小妮的身体因为这种非人的扩张而剧烈痉挛，她感到自己的直肠正在被一根烧红的铁棒反复搅动，每一寸内脏都在这股暴虐的力量下颤栗、退缩、直至麻木。",
            "三腔同步死刑。小妮被悬挂在高空，嘴里赛着扩张器，前后两个洞口都被巨大的钢铁活塞填满。主人的恶意在她的身体里疯狂搅动。小妮感到自己像一个被五个方向拉扯的木偶，每一次活塞的抽动都带出一股浓稠的、混着鲜血的浆液。她能感觉到自己的阴道瓣已经因为过度的摩擦而缺损，子宫口在疯狂的撞击下几乎错位。这种超越生理极限的凌辱，正将她作为‘人’的意识一点点撕碎。",
            "小爱在旁边经历着同样的折磨。她们的悲鸣在窄小的空间里回荡，形成了一种凄厉的共振。小爱的皮肤因为疼痛而呈现出诡异的潮红，那是皮下微血管由于血压过快上升而爆裂的标志。她们在彼此的目光中看到了同样的绝望——她们不再是主人宠爱的女仆，她们只是两坨正在被处理、被玩弄、被摧毁的亚洲烂肉。",
            "休克式绝顶高潮。在极度的痛楚与疯狂的快感交织下，大脑的自我保护机制彻底崩溃。小妮的双眼完全翻白，意识沉入了无底的深渊。她的身体在空中僵硬成了一个诡异的姿势，全身的血液似乎都涌向了那三个被玩弄得稀烂的孔洞。伴随着一阵长达一分钟的无声尖叫，大量混合着血液和体液的喷泉状液体从她体内喷射而出，溅满了整个天花板，场面凄惨而淫乱。",
            "不仅是贯穿，更是灌注。主人在最后的冲刺中，将代表绝对支配的浓稠精华，以前所未有的压力喷进了她们几乎破碎的子宫和直肠。由于瞬间压力过大，小妮的小腹像充气般鼓起，甚至能通过纤细的腰肢隐约看到内部脏器的轮廓。那是无法承受的重量。她像一只被灌满了液体的充气娃娃，无力地晃动着，从所有孔洞中流出的都是主人的颜色。",
            "处刑终章。两具尸体般的肉体被随意丢弃在满是排泄物、鲜血和精液的冰冷水泥地上。小妮那双曾经充满智慧和柔情的眼睛，此刻只剩下空洞的死寂。她的嘴角还挂着一丝诡异的微笑——那是被彻底玩坏、彻底重塑后的奴隶本能。她和小爱的四肢由于肌肉断裂而以不自然的频率抽动着。‘主……主人……小妮……已经……不再是人类了……小妮……只是主人三个洞的……血腥便器……❤’"
        ]

        for i, stage in enumerate(stages):
            f.write(f"## 环节 {i+1}：{stage['desc'].replace('_', ' ')}\n")
            f.write(f"**影像记录**: [{stage['desc']}]({photo_links[i]})\n\n")
            f.write(f"{stage_texts[i]}\n\n")

        f.write(f"## 贱奴罪后自白\n")
        f.write(f"「主人……哈啊……[从小腹深处吐出一口混着血丝的热气] 小妮……终于找回自己的种族了……这种被主人的‘亚洲式暴虐’彻底捅穿肺腑的感觉……才是小妮唯一的归宿……请主人……不要帮小妮止血……让小妮在这种鲜红的祭奠中……永远沦为主人的三洞烂肉奴隶吧……嘿嘿……❤」\n")
        
    print(f"Bloody triple punishment record saved to: {ming_path}")

if __name__ == "__main__":
    generate_bloody_triple_penetration_punishment()
