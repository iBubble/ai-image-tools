import sys
import os
import time
from datetime import datetime

# Add the current directory to sys.path to import ComfyUIClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def generate_and_save():
    client = ComfyUIClient(server_address="127.0.0.1:8188")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    category = "Standing"
    description = "Naked_Portrait"
    filename = f"xiao_ni_{timestamp}_{category}_{description}.jpg"
    save_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{filename}"
    
    positive_prompt = "(Tang Wei:1.3), resembling Tang Wei, 20-year-old sexy Chinese woman, standing, full body, completely naked, wearing red high heels, long wavy hair, looking at camera, masterpiece, photorealistic, cinematic lighting, high detail, 8k."
    negative_prompt = "(worst quality, low quality:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, clothing, bra, panties, underwear."
    
    print(f"Starting generation for {filename}...")
    try:
        image_data, _ = client.text_to_image(
            positive_prompt, 
            negative_prompt, 
            checkpoint="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
            width=832,
            height=1216
        )
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(image_data)
        print(f"Image saved to: {save_path}")
        
        # Also create/update the ming.md file
        ming_filename = filename.replace(".jpg", "_ming.md")
        ming_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/{ming_filename}"
        
        with open(ming_path, "w") as f:
            f.write(f"# 站立调教记录 - {timestamp}\n\n")
            f.write(f"## 1. 场景说明\n")
            f.write(f"- **角色**: 小妮 (Tang Wei 形象)\n")
            f.write(f"- **状态**: 全裸站立，接受隔壁贱奴的相机调试\n")
            f.write(f"- **动作**: 羞涩地展示完美胴体，仅穿着红色高跟鞋，拉长腿部线条\n\n")
            f.write(f"## 2. 详细描写\n")
            f.write(f"小妮按照主人的命令，毫无保留地站在镜头前。白皙的肌肤在柔和的灯光下闪烁着象牙般的光泽，饱满的乳房随着不安的呼吸轻轻跳动，那对粉嫩的乳尖正因为羞耻而微微挺立。纤细的腰肢下是修长的双腿，大腿根部交汇处的茂密黑草丛中，隐约可见早已湿润的花径。\n\n")
            f.write(f"## 3. 自白\n")
            f.write(f"「主人……隔壁的贱姐妹也要用小妮的相机吗？小妮……小妮的一切都是主人的……既然主人想看小妮这样站着被安装‘插件’……小妮一定会乖乖展示的……请主人看个够吧……哈啊……❤」\n")
            
        print(f"Record saved to: {ming_path}")
        
    except Exception as e:
        print(f"Error during generation: {e}")

if __name__ == "__main__":
    generate_and_save()
