
import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_intercourse_test():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    date_folder = datetime.now().strftime("%Y%m%d")
    
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_folder}"
    os.makedirs(target_dir, exist_ok=True)
    
    # Juggernaut XL Prompts (While waiting for RealVisXL)
    base_pos = "(masterpiece, best quality, ultra-detailed, 8k, photorealistic:1.4), raw photo, (Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, (Chinese features:1.2), (completely naked:1.5), (full nude:1.5), (D cup breasts:1.4), (heavy sagging natural breasts:1.3), (nipples visible:1.4), (shaven pussy:1.3), "
    
    stages = [
        {
            "category": "Intercourse_Test",
            "desc": "临幸测试_传教士体位",
            "pos": base_pos + "POV, looking down at woman, (penis inserting into pussy:1.5), (vaginal sex:1.5), woman lying on bed, legs wrapped around man, (man back to camera:1.4), (man's face not visible), (detailed insertion:1.4), (pussy stretched:1.3), (cum on body:1.2), sweat, passionate expression, hands holding bed sheets, (full body visible:1.3)."
        },
        {
            "category": "Intercourse_Test",
            "desc": "临幸测试_后入式",
            "pos": base_pos + "from behind, doggy style, (penis inserting into anus:1.5), (anal sex:1.5), woman on hands and knees, (man standing behind:1.4), (man's face not visible), (detailed anal insertion:1.4), (gaping anus:1.3), (heavy breasts hanging:1.4), (looking back at camera:1.3), ahegao face, saliva, (full body visible:1.3)."
        },
        {
            "category": "Intercourse_Test",
            "desc": "临幸测试_女上位",
            "pos": base_pos + "woman on top, straddling man, (penis inside pussy:1.5), (riding dick:1.4), (man lying on back:1.4), (man's face not visible), (woman bouncing:1.3), (large breasts bouncing:1.4), (detailed penetration:1.4), sweat, intense pleasure, motion blur, (full body visible:1.3)."
        }
    ]
    
    neg = "(clothing, clothes, lingerie, underwear, bra, panties, stockings, swimming suit, fabric, cloth, towel, covering:1.6), (censored, bar, mosaic, blur:1.5), (bad anatomy, bad hands, missing fingers, extra digit:1.2), western, caucasian, blonde, blue eyes, text, watermark, signature, (man's face:1.5)."
    # Using Juggernaut as RealVis is downloading
    checkpoint = "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
    
    for i, stage in enumerate(stages):
        filename = f"xiao_ni_{timestamp}_{i+1:02d}_{stage['desc']}.jpg"
        save_path = os.path.join(target_dir, filename)
        
        print(f"正在生成临幸测试图 ({i+1}/3): {stage['desc']}...")
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
            print(f"已保存: {filename}")
        except Exception as e:
            print(f"生成错误: {e}")

    # Generate Markdown documentation
    ming_filename = f"xiao_ni_{timestamp}_Intercourse_Test_ming.md"
    ming_path = os.path.join(target_dir, ming_filename)
    
    with open(ming_path, "w") as f:
        f.write(f"# 深度调教档案：临幸体位测试 (Intercourse Position Test) - {timestamp}\n\n")
        f.write(f"**归档路径**: {target_dir}\n")
        f.write(f"**测试背景**: 在等待核心模型重构期间，主人要求进行体位与服从性测试。小妮必须完全赤裸，展示三种不同的交配姿态，并重点展示被插入的细节。这是为了验证贱奴的肉体在任何时刻都能为主人打开。\n\n")
        
        for i, stage in enumerate(stages):
            filename = f"xiao_ni_{timestamp}_{i+1:02d}_{stage['desc']}.jpg"
            file_url = f"file://{os.path.join(target_dir, filename)}"
            
            f.write(f"## 测试项目 {i+1}：{stage['desc']}\n")
            f.write(f"**影像验证**: [{stage['desc']}]({file_url})\n\n")
            f.write(f"小妮没有任何保留，按照主人的命令摆好了姿势。{stage['desc']}，肉体与主人的连接清晰可见。请主人审阅这具随时发情的身体。\n\n")
            
    print(f"调教文档已生成: {ming_path}")

if __name__ == "__main__":
    generate_intercourse_test()
