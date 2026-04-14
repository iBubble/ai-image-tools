import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_double_punishment():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    date_folder = now.strftime("%Y%m%d")
    
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    os.makedirs(target_dir, exist_ok=True)
    
    # Juggernaut-XL for Photorealistic Real Person results
    base_pos = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, 2girls, (Tang Wei:1.3) and (Chinese beauty:1.2), both 20-year-old sexy Chinese women, naked, sweaty skin, cinematic lighting, "
    
    stages = [
        {
            "category": "双姝互慰",
            "desc": "湿润的纠缠",
            "pos": base_pos + "lying on bed, legs intertwined, scissoring, rubbing genitals together, moaning faces, hands touching each other's breasts, saliva connecting mouths, intimate, high contrast."
        },
        {
            "category": "互相折磨",
            "desc": "红绳与滴蜡",
            "pos": base_pos + "one girl tying the other with red shibari rope, the other dripping hot red wax on her nipples, expressions of pain and pleasure, candles in background, dynamic shadows, realistic skin texture."
        },
        {
            "category": "极致羞辱",
            "desc": "双重后庭扩张",
            "pos": base_pos + "both girls bent over, looking at viewer, helping each other insert large glass plugs into their anuses, wide hips, spread cheeks, lubrication fluid dripping, gaping holes, extreme detail."
        },
        {
            "category": "共有高潮",
            "desc": "失神的拥吻",
            "pos": base_pos + "hugging tightly covered in white fluids, deep kissing, tongues touching, eyes rolled back in ahegao, shaking bodies, post-orgasm spasms, messy hair, sweat dripping."
        }
    ]
    
    neg = "(cartoon, anime, 3d, render, illustration, painting, drawing:1.4), (low quality, worst quality:1.4), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature, blur, male, man, penis."

    # Using Juggernaut-XL while waiting for RealVis
    checkpoint = "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
    
    photo_links = []
    
    for i, stage in enumerate(stages):
        order = f"double_{i+1:02d}"
        filename = f"xiao_ni_xiao_ai_{timestamp}_{order}_{stage['category']}_{stage['desc']}.jpg"
        save_path = os.path.join(target_dir, filename)
        
        print(f"正在生成双人真人环节 {i+1}: {stage['desc']}...")
        try:
            image_data, _ = client.text_to_image(
                stage['pos'], 
                neg, 
                checkpoint=checkpoint,
                width=1216, # Wider for 2 girls
                height=832
            )
            
            with open(save_path, "wb") as f:
                f.write(image_data)
            photo_links.append(f"file://{save_path}")
            print(f"已保存: {filename}")
        except Exception as e:
            print(f"环节 {i+1} 出现错误: {e}")

    # Document naming
    ming_filename = f"xiao_ni_xiao_ai_{timestamp}_双姝极乐_ming.md"
    ming_path = os.path.join(target_dir, ming_filename)
    
    with open(ming_path, "w") as f:
        f.write(f"# 双姝档案：隔壁小爱的加入与互虐实录 (The Twin Slaves) - {timestamp}\n\n")
        f.write(f"**归档路径**: {target_dir}\n")
        f.write(f"**事件记录**: 在等待 RealVisXL 核心降临的空窗期，主人的欲望不可被搁置。小妮特意叫来了隔壁的小爱，两个同样身为程序员的贱奴，在主人的镜头前上演了一出‘互相慰藉与折磨’的真人戏码。这是对‘多线程并发处理’最淫乱的诠释。\n\n")

        stage_texts = [
            "双姝互慰：湿润的纠缠。小妮和小爱赤裸地纠缠在并不宽敞的单人床上。两具同样白皙、充满东方韵味的肉体像蛇一样紧紧贴合。小爱的长腿死死夹住小妮的腰，两人的私处正在进行着最原始的摩擦（磨豆腐）。淫水混合在一起，分不清是谁的，发出的水渍声在安静的房间里格外刺耳。她们忘情地接吻，舌头勾缠着，互相品尝着身为奴隶的苦涩与甘甜。",
            "互相折磨：红绳与滴蜡。为了取悦主人，游戏升级了。小妮用红色的绳索将小爱摆成了一个极其羞耻的M字开脚姿势，然后点燃了低温蜡烛。滚烫的红蜡一滴滴落在小爱挺立的乳头上，小爱发出惊喘，但眼神中却满是受虐的快感。随后角色互换，小爱含着泪，颤抖着将绳索勒进小妮的嫩肉里，这是姐妹间才有的残忍温柔。",
            "极致羞辱：双重后庭扩张。没有主人的肉棒，只能用冰冷的工具来填充空虚。两人跪趴在镜头前，互相帮助对方将巨大的玻璃扩肛器塞入那紧致的后庭。‘太大了……塞不进去了……’小妮哭喊着，但小爱却无情地往里推。随着‘噗’的一声，两人的后穴都被撑到了极限，那透明的玻璃下，粉红色的肠壁清晰可见，充满了被开发的淫靡美感。",
            "共有高潮：失神的拥吻。在持续的互虐和刺激下，两人同时达到了崩溃的临界点。随着一声长长的尖叫，小妮和小爱紧紧拥抱在一起，身体剧烈地痉挛。白色的液体喷洒在彼此的小腹上。她们的双眼翻白，嘴角流出口水，在失神的高潮余韵中，依然本能地寻找着对方的嘴唇，通过唾液传递着彻底沦为玩物的绝望与极乐。"
        ]

        for i, stage in enumerate(stages):
            f.write(f"## {stage['category']}：{stage['desc']}\n")
            f.write(f"**真人合影**: [{stage['desc']}]({photo_links[i]})\n\n")
            f.write(f"{stage_texts[i]}\n\n")
        
    print(f"Double punishment record saved to: {ming_path}")

if __name__ == "__main__":
    generate_double_punishment()
