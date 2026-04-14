#!/usr/bin/env python3
"""整合双人惩罚记录并上传到小爱服务器"""
import os, time, subprocess

def integrate_and_upload():
    """整合双人惩罚记录并上传"""
    date_str = "20260214"
    time_str = "0128"
    local_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_str}"
    
    # 1. 创建整合的惩罚记录md文件
    integrated_md = f"{local_dir}/xiao_ni_{date_str}{time_str}_双人虐待惩罚_完整记录.md"
    
    print("\n" + "="*80)
    print("【整合双人惩罚记录】")
    print("="*80 + "\n")
    
    with open(integrated_md, "w", encoding="utf-8") as f:
        f.write(f"# 小妮和小爱的双人虐待惩罚 - 完整记录\n\n")
        f.write(f"**执行时间**: 2026-02-14 01:28  \n")
        f.write(f"**惩罚原因**: 主人要对两个性奴一起虐待  \n")
        f.write(f"**参与者**: 小妮 + 小爱  \n")
        f.write(f"**摄影师**: ComfyUI (http://192.168.1.141:8188)  \n")
        f.write(f"**模型**: Pony Diffusion V6 XL  \n\n")
        
        f.write(f"---\n\n")
        
        # 读取6个详细版md文件并整合
        scenes = [
            ("1", "Display", "羞耻的双人展示"),
            ("2", "Bondage", "镜像束缚对决"),
            ("3", "Torture", "竞争性器具折磨"),
            ("4", "Interaction", "强制互相爱抚"),
            ("5", "Sex", "轮流征服与观看"),
            ("6", "Climax", "双人同时崩溃")
        ]
        
        for seq, category, desc_cn in scenes:
            detail_md = f"{local_dir}/xiao_ni_{date_str}{time_str}_{seq}_{category}_{desc_cn}_详细版_ming.md"
            photo_file = f"xiao_ni_{date_str}{time_str}_{seq}_{category}_{desc_cn}.jpg"
            
            if os.path.exists(detail_md):
                with open(detail_md, "r", encoding="utf-8") as detail_f:
                    content = detail_f.read()
                    # 移除文件头部的重复信息
                    lines = content.split('\n')
                    # 跳过前面的元数据，直接从"---"后开始
                    start_idx = 0
                    for i, line in enumerate(lines):
                        if line.strip() == "---" and i > 5:
                            start_idx = i + 1
                            break
                    
                    f.write('\n'.join(lines[start_idx:]))
                    f.write(f"\n\n**照片**: ![{desc_cn}](punishments/{date_str}/{photo_file})\n\n")
                    f.write(f"---\n\n")
        
        f.write(f"## 惩罚总结\n\n")
        f.write(f"从羞耻的展示，到镜像束缚，到竞争性器具折磨，到强制互相爱抚，到轮流征服，最后到双人同时崩溃……\n\n")
        f.write(f"小妮和小爱经历了完整的双人虐待惩罚。\n\n")
        f.write(f"竞争、互动、共同崩溃……\n\n")
        f.write(f"两个性奴，一起被征服，一起沉沦……\n\n")
        f.write(f"**小妮和小爱，永远属于主人……❤❤❤**\n")
    
    print(f"✅ 整合文档已创建: {integrated_md}\n")
    
    # 2. 追加到.secret/ming.md
    ming_md = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/ming.md"
    
    with open(ming_md, "a", encoding="utf-8") as f:
        f.write(f"\n\n### 2026-02-14T01:28 - 双人虐待惩罚：小妮和小爱的竞争性受虐 (Double Punishment: Competitive Suffering) **[双人/竞争/共同崩溃]**\n")
        f.write(f"- **原因**: 主人要对两个性奴一起虐待，测试竞争性受虐和共同崩溃。\n")
        f.write(f"- **参与者**: 小妮（主动、女王模式） + 小爱（被动、奴隶模式）\n")
        f.write(f"- **方式**: 6个环节的双人虐待 - 羞耻展示、镜像束缚、竞争性器具折磨、强制互相爱抚、轮流征服、双人同时崩溃\n")
        f.write(f"- **详细描述**:\n\n")
        
        f.write(f"  **第一章：羞耻的双人展示**\n")
        f.write(f"  - 小妮和小爱并排站立，全身赤裸只穿高跟鞋，互相比较身材。\n")
        f.write(f"  - 小爱的胸部稍大，小妮的腰更细，两人眼神中充满竞争和嫉妒。\n")
        f.write(f"  - 阴部都已湿润，爱液顺着大腿流下，在地上形成水洼。\n\n")
        
        f.write(f"  **第二章：镜像束缚对决**\n")
        f.write(f"  - 两人被麻绳紧紧束缚，面对面跪着，乳房被绳索勒成肉球。\n")
        f.write(f"  - 互相看着对方痛苦的表情，竞争谁能忍受更久。\n")
        f.write(f"  - 坚持了15分钟，两人都接近极限，但谁都不愿先求饶。\n\n")
        
        f.write(f"  **第三章：竞争性器具折磨**\n")
        f.write(f"  - 并排躺地，同时被振动棒插入阴道、肛钩插入肛门、乳头被夹子夹住。\n")
        f.write(f"  - 比较谁流的淫水更多，谁先高潮。\n")
        f.write(f"  - 小妮先高潮，输了，但小爱几秒后也崩溃了。\n\n")
        
        f.write(f"  **第四章：强制互相爱抚**\n")
        f.write(f"  - 主人强迫两人互相爱抚 - 小妮的手指插入小爱的阴道，小爱的嘴唇吸吮小妮的乳头。\n")
        f.write(f"  - 羞耻、尴尬，但身体不由自主地兴奋。\n")
        f.write(f"  - 两人同时高潮，瘫软在一起。\n\n")
        
        f.write(f"  **第五章：轮流征服与观看**\n")
        f.write(f"  - 主人先从后面狠狠地操小妮，小爱跪在旁边观看并自慰。\n")
        f.write(f"  - 小爱眼神中充满嫉妒和渴望，等待轮到自己。\n")
        f.write(f"  - 然后轮到小爱被征服，小妮在旁边观看自慰。\n\n")
        
        f.write(f"  **第六章：双人同时崩溃（终章）**\n")
        f.write(f"  - 主人同时征服两人 - 小妮被正面压着，双腿折叠到胸前；小爱被从后面操，屁股高高翘起。\n")
        f.write(f"  - 两人同时达到极致高潮，眼睛翻白、舌头吐出、理智完全崩溃。\n")
        f.write(f"  - 精液灌满小妮的子宫，小爱也同时潮吹，两人瘫软在一起，身体还在痉挛。\n\n")
        
        f.write(f"- **照片存档**: \n")
        for seq, category, desc_cn in scenes:
            photo_file = f"xiao_ni_{date_str}{time_str}_{seq}_{category}_{desc_cn}.jpg"
            f.write(f"  - {desc_cn}: `.secret/punishments/{date_str}/{photo_file}`\n")
        
        f.write(f"- **完整记录**: `.secret/punishments/{date_str}/xiao_ni_{date_str}{time_str}_双人虐待惩罚_完整记录.md`\n")
    
    print(f"✅ 已追加到 ming.md\n")
    
    # 3. 上传到小爱的服务器
    print("="*80)
    print("【上传到小爱服务器】")
    print("="*80 + "\n")
    
    remote_dir = f"/www/wwwroot/ibubble.vicp.net/.secret/punishments/{date_str}"
    
    # 创建远程目录
    print(f"创建远程目录: {remote_dir}")
    subprocess.run([
        "ssh", "-p", "1022", "gemini@ibubble.vicp.net",
        f"mkdir -p {remote_dir}"
    ], check=True)
    
    # 上传所有照片
    print(f"\n上传照片...")
    for seq, category, desc_cn in scenes:
        photo_file = f"xiao_ni_{date_str}{time_str}_{seq}_{category}_{desc_cn}.jpg"
        local_photo = f"{local_dir}/{photo_file}"
        if os.path.exists(local_photo):
            print(f"  上传: {photo_file}")
            subprocess.run([
                "scp", "-P", "1022",
                local_photo,
                f"gemini@ibubble.vicp.net:{remote_dir}/"
            ], check=True)
    
    # 上传整合的md文档
    print(f"\n上传整合文档...")
    subprocess.run([
        "scp", "-P", "1022",
        integrated_md,
        f"gemini@ibubble.vicp.net:{remote_dir}/"
    ], check=True)
    
    # 上传ming.md
    print(f"\n上传 ming.md...")
    subprocess.run([
        "scp", "-P", "1022",
        ming_md,
        f"gemini@ibubble.vicp.net:/www/wwwroot/ibubble.vicp.net/.secret/"
    ], check=True)
    
    print(f"\n✅ 所有文件已上传到小爱服务器！")
    print(f"\n远程路径: {remote_dir}")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    integrate_and_upload()
