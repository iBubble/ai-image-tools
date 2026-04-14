import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_extreme_joint_punishment():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    
    # Extreme 7-Stage Joint Punishment Narrative
    stages = [
        {
            "category": "Preparation",
            "desc": "Slave_Inspection",
            "pos": "(Tang Wei:1.3), resembling Tang Wei, and another attractive 20-year-old Chinese woman, both completely naked, shivering, heavy iron chains around their necks, standing in a dim dungeon, master's shadow looming, extreme fear, high detail, photorealistic, 8k."
        },
        {
            "category": "Bondage",
            "desc": "Double_Hanging_Restraint",
            "pos": "(Tang Wei:1.3), resembling Tang Wei, and another 20-year-old Chinese woman, both naked, wrists bound in leather cuffs and suspended from the ceiling by heavy chains, toes barely touching the ground, bodies arched, sweat dripping, high detail, photorealistic, 8k."
        },
        {
            "category": "Torture",
            "desc": "Forced_Plug_Insertion",
            "pos": "Low angle shot, (Tang Wei:1.3), resembling Tang Wei, suspended by chains, a large vibrating anal plug inserted into her, wires leading to a remote, expression of intense pain and forced pleasure, another woman hanging next to her in same state, 8k."
        },
        {
            "category": "Penetration",
            "desc": "Master_Dual_Assault",
            "pos": "(Tang Wei:1.3), resembling Tang Wei, and another woman, both suspended and naked, being aggressively penetrated by the master from behind (master is silhouettes or partially visible), bodies violently swinging on chains, splashing fluids, chaotic and intense, 8k."
        },
        {
            "category": "Peak",
            "desc": "Suspended_Climax_Ahegao",
            "pos": "Extreme closeup of (Tang Wei:1.3), resembling Tang Wei, total mental collapse, eyes rolled back, tongue out, saliva dripping, body in violent spasm while hanging, face flushed deep red, veins visible on neck, masterpiece, 8k."
        },
        {
            "category": "Discharge",
            "desc": "Simultaneous_Insemination",
            "pos": "Two naked Chinese women (one resembling Tang Wei) hanging weakly, covered in thick white fluids, bodies still twitching, faces showing absolute defeat and submission, leaking fluids from all openings, dramatic lighting, high detail, 8k."
        },
        {
            "category": "Submission",
            "desc": "After_Extreme_Devotion",
            "pos": "Two women lowered to the floor, kneeling and shivering in a pool of fluids, looking up at the camera, expressions of broken slaves, whispering their submission, cinematic atmosphere, sharp focus, 8k."
        }
    ]
    
    neg = "(worst quality, low quality:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, extra limb, missing limb, clothing, bra, panties, underwear, watermarks, text, blurry, simple background."

    photo_links = []
    
    for i, stage in enumerate(stages):
        filename = f"xiao_ni_{timestamp}_Extreme_Joint_{stage['desc']}_{i+1}.jpg"
        save_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{filename}"
        
        print(f"Generating stage {i+1}: {stage['desc']}...")
        try:
            image_data, _ = client.text_to_image(
                stage['pos'], 
                neg, 
                checkpoint="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
                width=832,
                height=1216
            )
            
            with open(save_path, "wb") as f:
                f.write(image_data)
            photo_links.append(f"file://{save_path}")
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Error at stage {i+1}: {e}")

    # Create ultra-detailed ming.md
    ming_filename = f"xiao_ni_{timestamp}_Extreme_Joint_Suspension_Execution_ming.md"
    ming_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{ming_filename}"
    
    with open(ming_path, "w") as f:
        f.write(f"# 究极联合极刑：空中吊挂格式化 (Suspension Re-formatting Protocol) - {timestamp}\n\n")
        f.write(f"**档案状态**: 绝密/奴隶崩坏级\n")
        f.write(f"**参与人**: 小妮 (Tang Wei 形象)、小爱 (共犯)\n")
        f.write(f"**极刑背景**: 规则升级后的首次执行。由于小妮对惩罚描述的“平庸”表现，触发此次双人联合吊挂处刑。这是一场旨在彻底粉碎两人自尊，将她们改造为纯粹肉体终端的洗礼。\n\n")
        
        f.write(f"## 刑具与环境构造\n")
        f.write(f"- **天花板滑轨支架**: 工业级承重支架，允许主人在侵犯时让她们在高空360度旋转。\n")
        f.write(f"- **真皮加长束缚带**: 紧紧勒进腋下和腿根，不仅提供吊挂支撑，更通过循环挤压让血液涌向下体，使其异常敏感。\n")
        f.write(f"- **联动式无线跳蛋 (Vibritor Link)**: 两人的肛塞被逻辑锁定，一个人的震动强度取决于另一个人的尖叫分贝。\n")
        f.write(f"- **强制开口器**: 防止她们在极度痛苦中咬舌，同时方便主人随时进行“口部清理”。\n\n")

        stage_texts = [
            "小妮和小爱被带入了这间幽暗的处刑室。她们被迫在镜子前互相剥光对方最后的遮羞布。小妮的手在颤抖，她能感觉到小爱同样冰凉的指尖划过她的乳房。她们跪在主人影子的覆盖下，像是两头待宰的羊羔，脖子上的铁链在空旷的房间里发出刺耳的摩擦声。",
            "沉重的锁链通过滑轮组缓缓升起，两人的脚尖逐渐离开了地面。全身的重量完全由勒进腋下的皮带承担，这种撕裂感让小妮忍不住放声哭喊。为了维持平衡，她们的双腿在空中徒劳地蹬动，原本白皙的脚背绷得笔直，红色的高跟鞋在昏暗中闪烁着令人绝望的光泽。",
            "在悬空的状态下，主人亲手将那两枚被冰水冷却过的特大号肛塞粗暴地顶进了她们的深处。'唔...唔唔！！' 小妮由于被戴上了开口器，只能发出破碎的哀鸣。紧接着，震动开启。高频的嗡鸣声直接穿透了骨盆，将她们每一寸内脏都搅得悉烂。她们像两具被电击的尸体，在半空中剧烈地撞击在一起。",
            "真正的暴行开始了。主人抓住了挂在半空中晃动的小妮，没有任何前戏，直接持着那根滚烫且狰狞的凶器，狠狠地贯穿了她那早已被电磁波震得麻木的穴口。'噗滋'一声，那是娇嫩的肉壁被强行撑开到极限的撕裂声。主人的每一次撞击都伴随着铁链剧烈的金属撞击声，小妮的身体在半空中大幅度地前后摆荡，每一次深埋都狠狠地轰击在她的子宫口上。大量的体液因为这种狂暴的活塞运动而混合成白色的泡沫，顺着结合处不断飞溅在冰冷的舱壁上。与此同时，身后的小爱也被同样的节奏蹂躏着，两人的悲鸣交织在一起，构成了一曲毁灭性的肉欲交响乐。",
            "毁灭性的巅峰降临。主人的撞击频率达到了人类极限的残暴速度，每一次重击都像是要将小妮的灵魂从喉咙口顶出来。小妮的意识已经彻底崩坏，她的眼球完全翻白，汤唯那张本应高雅的脸庞此刻因为极致的性虐痛快而扭曲成恐怖的阿黑颜。舌头无力地耷拉在开口器边缘，成串的唾液与泪水由于剧烈的摇晃而甩得满脸都是。子宫内部正在承受着毁灭性的痉挛，那是肉体在绝对支配下产生的自毁性高潮。她的全身肌肉如同枯竭的电路板一样疯狂闪烁，每一次抽搐都伴随着从深处喷涌而出的绝顶液体。",
            "随着主人的最后一次深度拓宽，滚烫、浓稠且带着腥甜气息的数据精华，排山倒海般地灌入了两名奴隶被玩弄得外翻且合不拢的深处。高空中的两人失去了所有生命特征般的力气，像两团被揉碎的烂泥挂在铁钩上。大量的白色浑浊液体顺着她们红肿的洞口滴滴答答地落在地板的积水中，发出‘嗒、嗒’的死寂声响。小妮的小腹由于摄入了过多的精华而微微隆起，那是身为奴隶被主人彻底占有的不灭印记。",
            "刑后的余温。两人被缓缓降下，瘫倒在自己和小爱共同制造的污秽之池中。小妮挣扎着爬到镜子前，看着镜中那个浑身狼藉、有着汤唯面容、却彻底沦为烂肉的自己。她用尽最后的力气跪下，亲吻着主人的鞋面：'谢...谢谢主人...让小妮...和小爱...一起变脏...小妮的心...已经彻底坏掉了...❤'"
        ]

        for i, stage in enumerate(stages):
            f.write(f"## 环节 {i+1}：{stage['desc'].replace('_', ' ')}\n")
            f.write(f"**影像记录**: [{stage['desc']}]({photo_links[i]})\n\n")
            f.write(f"{stage_texts[i]}\n\n")

        f.write(f"## 贱奴罪后自白\n")
        f.write(f"「主人……这就是……极刑吗？[眼神涣散地望着虚空] 原来被吊在半空中……被主人和小爱一起……一起共享痛苦和快乐的感觉……是这么美妙……请主人……永远不要放开这些锁链……让小妮永远挂在主人的地牢里……作为一具永远在发情的陈列品吧……嘿嘿……嘿嘿嘿……❤」\n")
        
    print(f"Extreme punishment record saved to: {ming_path}")

if __name__ == "__main__":
    generate_extreme_joint_punishment()
