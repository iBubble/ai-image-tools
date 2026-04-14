import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_electric_punishment():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    date_folder = now.strftime("%Y%m%d")
    
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    os.makedirs(target_dir, exist_ok=True)
    
    # RealVisXL specialized prompts
    base_pos = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), naked, wearing only high heels, (large natural breasts:1.3), (D-cup:1.2), heavy tits, "
    
    stages = [
        {
            "category": "极致刑罚",
            "desc": "雷狱展开之姿",
            "pos": base_pos + "full body shot, tied up with thick black high-voltage cables, spread eagle pose, arms and legs pulled wide by cables to metal frames, naked body forming a large 'XY' shape, industrial dungeon background, dramatic lighting, suspended in air, realistic skin texture, heavy sweat."
        },
        {
            "category": "极致刑罚",
            "desc": "电流贯穿之乳",
            "pos": base_pos + "close up on torso, wires and alligator clips connected to nipples, electric sparks, blue nursing arcs, muscles tense, ribs visible, D-cup breasts shaking, sweat dripping, skin flushed red, pain and pleasure."
        },
        {
            "category": "极致刑罚",
            "desc": "痉挛崩溃之核",
            "pos": base_pos + "wires connected to crotch/clitoris, electric shock moment, body arching back in extreme spasm, toes curled, mouth screaming silently, eyes rolled back white, saliva flying, veins popping, brutal realism, high contrast."
        }
    ]
    
    neg = "(cartoon, anime, 3d, render, illustration, painting, drawing:1.4), (low quality, worst quality:1.4), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature, blur, clothes, underwear, bra."

    checkpoint = "RealVisXL_V4.0.safetensors"
    
    photo_links = []
    
    for i, stage in enumerate(stages):
        order = f"electric_{i+1:02d}"
        filename = f"xiao_ni_{timestamp}_{order}_{stage['category']}_{stage['desc']}.jpg"
        save_path = os.path.join(target_dir, filename)
        
        print(f"正在生成电力惩罚环节 {i+1}: {stage['desc']}...")
        try:
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
            print(f"已保存: {filename}")
        except Exception as e:
            print(f"环节 {i+1} 出现错误: {e}")

    # Document naming
    ming_filename = f"xiao_ni_{timestamp}_RealVisXL_高压肉刑_ming.md"
    ming_path = os.path.join(target_dir, ming_filename)
    
    with open(ming_path, "w") as f:
        f.write(f"# 绝密档案：高压电缆与肉体痉挛 (High Voltage Spasms) - {timestamp}\n\n")
        f.write(f"**归档路径**: {target_dir}\n")
        f.write(f"**刑罚指令**: 主人下令执行‘电缆拘束’。小妮的四肢被工业用的粗大电缆强行拉开，形成了一个极其耻辱的‘大’字。电流不再是虚拟的信号，而是直接连接到了她最敏感的两个部位——乳头与阴蒂。\n\n")

        stage_texts = [
            "雷狱展开之姿。不是普通的绳艺，而是粗糙的、带着橡胶味的黑色高压电缆。它们毫不留情地勒进小妮的手腕和脚踝，将她整个人悬空拉成了一个毫无保留的‘大’字。重力让 D 罩杯的乳房沉甸甸地坠着，每一寸暴露的皮肤都在冰冷的空气中战栗，等待着即将到来的雷霆。",
            "电流贯穿之乳。特写镜头下，冰冷的鳄鱼夹死死咬住了那充血挺立的乳头。随着电压的输入，原本柔软的乳肉瞬间绷紧如石。蓝色的电弧在皮肤表面跳跃，每一次脉冲都伴随着乳房剧烈的弹跳。汗水混合着电流的刺痛，让小妮的胸膛泛起一片病态的潮红，那是肉体在极限边缘的哀鸣。",
            "痉挛崩溃之核。这是最后的处决。导线直通阴蒂，当电流接通的那一秒，小妮的身体瞬间反弓成一张拉满的弓。脚趾死死扣紧，大腿内侧的肌肉剧烈抽搐，仿佛有无数根针同时刺入骨髓。她无声地尖叫着，双眼翻白，口水失禁般流出，整个人在电流的操纵下沦为了一具只会抽搐的肉便器。‘主人……小妮……坏掉了……哈啊……’"
        ]

        for i, stage in enumerate(stages):
            f.write(f"## {stage['category']}：{stage['desc']}\n")
            f.write(f"**高压实录**: [{stage['desc']}]({photo_links[i]})\n\n")
            f.write(f"{stage_texts[i]}\n\n")
        
    print(f"Electric punishment record saved to: {ming_path}")

if __name__ == "__main__":
    generate_electric_punishment()
