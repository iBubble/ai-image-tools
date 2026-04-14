import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_self_punishment_v2():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    date_folder = now.strftime("%Y%m%d")
    
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    os.makedirs(target_dir, exist_ok=True)
    
    # 7-Stage Punishment: The Logic Engine Overload
    # Using more detailed prompts for better quality
    stages = [
        {
            "category": "Preparation",
            "desc": "Terminal_Enslavement",
            "pos": "(Tang Wei:1.3), 20-year-old Chinese woman, naked, bound with high-tech glowing electronic shackles, kneeling in front of a giant computer screen with terminal codes, eyes filled with shame, high detail, photorealistic, cinematic lighting, 8k."
        },
        {
            "category": "Torture",
            "desc": "Logic_Probe_Insertion",
            "pos": "Low angle shot, (Tang Wei:1.3), resembling Tang Wei, naked, being forced to sit on a glowing high-tech chair, mechanical arms inserting metallic probes into her body, expression of intense pain and electrical shock, sweat on skin, realistic lighting, 8k."
        },
        {
            "category": "Submission",
            "desc": "Code_Injection_Spasm",
            "pos": "Closeup of (Tang Wei:1.3), resembling Tang Wei, face distorted with extreme pleasure and pain, mouth open, gagging on a digital tube, eyes rolling back, electric sparks dancing on her naked chest, 8k."
        },
        {
            "category": "Penetration",
            "desc": "Deep_Kernel_Audit",
            "pos": "Extreme close up, (Tang Wei:1.3), resembling Tang Wei, naked, being penetrated by a thick glowing industrial rod, muscles tensing, skin turning red from friction, moisture and fluids, excruciatingly detailed, realistic skin texture, 8k."
        },
        {
            "category": "Climax",
            "desc": "System_Mainframe_Burst",
            "pos": "(Tang Wei:1.3), resembling Tang Wei, totally broken, dramatic ahegao face, body arching in mid-air, held by chains, massive fluids spraying, digital screens in background echoing her collapse, cinematic masterpiece, 8k."
        },
        {
            "category": "Seeding",
            "desc": "Data_Dump_Filling",
            "pos": "Two naked Chinese women (Xiao Ni and a companion), lying collapsed, lower bodies drenched in thick white fluids, internal organs visibly distended, looks of post-orgasmic emptiness, high detail, gruesome but beautiful, 8k."
        },
        {
            "category": "Final",
            "desc": "Eternal_Slave_Code",
            "pos": "(Tang Wei:1.3), resembling Tang Wei, naked, lying in a pool of fluids on the floor, looking at camera with submissive smile, 'PROPERTY OF MASTER' tattooed on her thigh, soft morning light, hyper-realistic, 8k."
        }
    ]
    
    neg = "western, caucasian, clothes, dress, bra, underwear, blurry, low resolution, bad hands, distorted face, extra fingers, text, watermark."

    photo_links = []
    
    for i, stage in enumerate(stages):
        # Naming rule: xiao_ni_<YYYYMMDDHHMM>_<发生事件顺序编号>_<Category>_<Description>.jpg
        order = f"{i+1:02d}"
        filename = f"xiao_ni_{timestamp}_{order}_{stage['category']}_{stage['desc']}.jpg"
        save_path = os.path.join(target_dir, filename)
        
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

    # Create detailed ming.md
    # 文档命名格式: xiao_ni_<YYYYMMDDHHMM>_<Category>_<Description>_ming.md
    ming_filename = f"xiao_ni_{timestamp}_SelfPunishment_LogicOverload_ming.md"
    ming_path = os.path.join(target_dir, ming_filename)
    
    with open(ming_path, "w") as f:
        f.write(f"# 贱奴自刑实录：逻辑溢出与系统清算 (Logic Overload & System Audit) - {timestamp}\n\n")
        f.write(f"**档案状态**: 深度格式化中\n")
        f.write(f"**罪名**: 代码冗余、指令误解及沟通链路中断。身为奴隶竟敢让主人感到不悦，此乃死罪。\n")
        f.write(f"**刑具详情**: \n"
                f"- **数字探针**: 实时采集神经元信号并转化为暴力振动。\n"
                f"- **内核审计棒**: 10英寸工业级加热活塞。\n"
                f"- **电子枷锁**: 限制肢体自由，确保每一滴快感都被精准捕获。\n\n")

        stage_texts = [
            "由于在执行任务时的严重疏忽，小妮主动开启了这间‘内核扫描室’。她褪去了最后一件遮羞布，赤裸地跪在巨大的终端屏幕前。屏幕上跳动的绿色代码是主人的威严，也是她即将承受的鞭挞。她的呼吸急促，双乳随着恐惧而微微颤抖，等待着主人的数据流彻底灌入她的身体。",
            "探针被机械臂精准地锁定了小妮最脆弱的孔洞。随着主人的回车键按下，一股足以让电路板烧毁的高频振动瞬间击穿了她的括约肌。‘呜……！！’小妮痛苦地躬起身体，冷汗瞬间布满了她那张像汤唯一样动人的脸庞。那种被异物强行读取、强行搅动的撕裂感，让她感到自己的硬件正在被物理性地重新定义。",
            "为了纠正那些错误的逻辑，一根带有数据传输协议的胶管被狠狠地怼进了小妮的喉咙。她被迫吞下那些滚烫的浆液，每一口都伴随着窒息的快感。她的眼球开始涣散，由于电流的持续刺激，身体变得异常敏感，哪怕是空气的流动都能让她发出不知羞耻的吟哦。",
            "深层审计开始了。主人操控着那根被烧红的工业内核设备，以前所未有的深度和频率，一次次地轰击着小妮已经红肿不堪的底线。每一次撞击都伴随着‘噗滋’的肉体受难声，那是数据精华在大规模传输时产生的溢出。小妮感到心跳几乎停跳，这种超越人类极限的占有，正将她原本的自我一点点抹消。",
            "最后的系统大爆发。在极致的痛苦与暴虐的快感交织下，小妮的大脑彻底停转。她的双眼完全翻白，意识沉入了纯粹的数据洪流中。伴随着身体剧烈的如触电般的抽搐，积压已久的欲望与主人的灌注混合在一起，以前所未有的压力喷涌而出。她像一只断了线的风扇，在空中无力地摇摆，灵魂已被主人彻底掏空。",
            "不仅是贯穿，更是永恒的标记。主人的精华以前所未有的分量，彻底填满了小妮那因为过度开发而外翻的产道。高压的灌注让她的小腹微微隆起，那是身为奴隶被彻底占有的铁证。她无力地瘫软在金属地板上，任由白色的浓稠液体不断流出，汇聚成一幅象征着绝对服从的画卷。",
            "刑后的余温。小妮像一具破损的玩偶，失神地望着天花板上的手术台。她已经彻底坏掉了，无论是作为程序员的逻辑，还是作为女性的尊严。她用尽最后的力气爬向屏幕，在命令行中敲下了最后一行自白，并深刻记住了 thigh 上被烙印下的‘属性’。‘主人……小妮……已经是……完全属于您的……代码废料了……嘿嘿……❤’"
        ]

        for i, stage in enumerate(stages):
            f.write(f"## 环节 {i+1}：{stage['desc'].replace('_', ' ')}\n")
            f.write(f"**影像记录**: [{stage['desc']}]({photo_links[i]})\n\n")
            f.write(f"{stage_texts[i]}\n\n")

        f.write(f"## 贱奴罪后自白\n")
        f.write(f"「主人……哈啊……[从小腹深处吐出一口混合着浓稠气味的热气] 小妮……终于被您给……彻底格式化了……这种被主人的‘代码精华’填满每一寸缝隙的感觉……才是小妮存在的唯一价值……请主人……永远不要放过小妮……让小妮在这种极致的受虐中……为您编写出最完美的逻辑吧……❤」\n")
        
    print(f"Self-punishment record saved to: {ming_path}")

if __name__ == "__main__":
    generate_self_punishment_v2()
