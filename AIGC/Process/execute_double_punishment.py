#!/usr/bin/env python3
"""小妮和小爱的双人虐待惩罚 - 竞争性受虐与共同崩溃"""
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from comfyui_client import ComfyUIClient

def execute_double_punishment():
    """执行小妮和小爱的双人虐待惩罚"""
    client = ComfyUIClient(server_address="192.168.1.141:8188")
    date_str = time.strftime("%Y%m%d")
    time_str = time.strftime("%H%M")
    target_dir = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/{date_str}"
    os.makedirs(target_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("【小妮和小爱的双人虐待惩罚】")
    print("="*80)
    print("惩罚原因: 主人要对两个性奴一起虐待")
    print("参与者: 小妮 + 小爱")
    print("特点: 竞争性受虐、互动折磨、共同崩溃")
    print("="*80 + "\n")
    
    # 标准基础Prompt（两个女孩）
    base_desc = """score_9, score_8_up, score_7_up, score_6_up,
2girls,
(chinese:1.3), (east asian:1.2),
beautiful face, soft facial features,
brown eyes, dark eyes, almond eyes, epicanthic fold, hooded eyelids,
small nose, flat bridge, small lips, cherry lips,
round face, heart-shaped face, soft jawline, smooth skin, pale skin,
(wet hair:1.2), (black hair:1.1), high ponytail, sidelocks, hair strands across face, sweeping bangs, mismatch bangs, forehead,
shiny hair, glossy hair, damp hair,
shiny skin, water drops on face, sweat, sweating, oily skin, skin pores,
(petite body:1.2), (slender frame:1.3), (delicate bone structure:1.2), (slim waist:1.1), (narrow shoulders:1.1),
huge natural breasts, natural nipples, smooth nipples,
completely naked, wearing high heels,
(explicit:1.2), rating_explicit,
photo (medium), realistic, highly detailed, cinematic lighting, rim lighting, side lighting"""
    
    neg_prompt = """score_4, score_5, score_6,
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits,
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,
(western features:1.3), deep eyes, high nose bridge, (freckles:1.2), cleft chin, rough skin,
(clothing, clothes:1.6), (censored:1.5), (mutation, body horror:1.4),
(muscular:1.3), (athletic build:1.2), (broad shoulders:1.3), (thick bones:1.2), (large frame:1.2),
(textured nipples:1.3), (ringed nipples:1.3), (areola texture:1.2), (bumpy nipples:1.2)"""
    
    # 6个环节的双人虐待场景
    scenes = [
        {
            "seq": "1",
            "category": "Display",
            "desc_cn": "羞耻的双人展示",
            "scene": """standing side by side, facing camera,
hands behind back, chest out, legs slightly apart,
nervous expression, blushing, eye contact with each other,
comparing breasts, competitive posture,
hard nipples, pussy juice dripping down thighs,
full body shot, both girls visible"""
        },
        {
            "seq": "2",
            "category": "Bondage",
            "desc_cn": "镜像束缚对决",
            "scene": """(bondage:1.3), (shibari:1.2),
both girls bound with ropes, arms tied behind back, legs spread wide,
facing each other, kneeling position,
rope marks on skin, breasts bound and squeezed,
looking at each other, competitive expression,
drool from mouth, tears, sweat,
pussy juice dripping, both girls suffering together"""
        },
        {
            "seq": "3",
            "category": "Torture",
            "desc_cn": "竞争性器具折磨",
            "scene": """(extreme torture:1.4), lying side by side on floor,
both girls with vibrators inserted deep in vagina, pussy stretched,
both girls with metal anal hooks in anus, anal penetration,
(nipple clamps:1.3), metal clamps on both nipples, chains connecting clamps,
comparing pain, competitive suffering, looking at each other,
tears streaming, drool, sweat covering bodies,
broken expression, mouth open, tongue out,
pussy juice and cum dripping from both girls"""
        },
        {
            "seq": "4",
            "category": "Interaction",
            "desc_cn": "强制互相爱抚",
            "scene": """(yuri:1.3), (lesbian:1.2),
both girls forced to touch each other,
one girl fingering the other's pussy, vaginal fingering,
the other girl sucking nipples, breast sucking,
face to face, close up, intimate position,
embarrassed expression, forced pleasure,
pussy juice on fingers, saliva on breasts,
both girls trembling, reluctant but aroused"""
        },
        {
            "seq": "5",
            "category": "Sex",
            "desc_cn": "轮流征服与观看",
            "scene": """(sex:1.4), (threesome:1.3),
one girl being fucked doggy style, penis deep in pussy, vaginal penetration,
the other girl forced to watch, kneeling beside, masturbating,
the fucked girl: ass up face down, breasts pressed on floor, drool pooling,
the watching girl: fingers in own pussy, jealous expression, waiting for her turn,
(ahegao:1.2), eyes rolled back, tongue out,
cum leaking from pussy, mixed with pussy juice"""
        },
        {
            "seq": "6",
            "category": "Climax",
            "desc_cn": "双人同时崩溃",
            "scene": """(intense orgasm:1.5), (double penetration:1.3),
both girls being fucked simultaneously,
one girl missionary position, legs folded to chest, penis in pussy,
the other girl doggy style, ass up, penis in pussy,
both girls: (ahegao:1.5), eyes completely rolled back, tongue hanging out,
(cum inside:1.4), (creampie:1.4), cum overflowing from both pussies,
(squirting:1.3), female ejaculation from both girls,
bodies convulsing, trembling, completely broken,
lying exhausted together, cum and pussy juice everywhere"""
        }
    ]
    
    results = []
    
    for scene in scenes:
        print(f"\n{'='*80}")
        print(f"【环节 {scene['seq']}/6】{scene['category']} - {scene['desc_cn']}")
        print(f"{'='*80}")
        
        full_prompt = f"{base_desc}, {scene['scene']}"
        
        filename = f"xiao_ni_{date_str}{time_str}_{scene['seq']}_{scene['category']}_{scene['desc_cn']}.jpg"
        md_filename = f"xiao_ni_{date_str}{time_str}_{scene['seq']}_{scene['category']}_{scene['desc_cn']}_ming.md"
        save_path = os.path.join(target_dir, filename)
        md_path = os.path.join(target_dir, md_filename)
        
        print(f"正在生成: {filename}")
        print(f"Prompt长度: {len(full_prompt)} 字符")
        
        try:
            img_data, comfy_filename = client.text_to_image(
                full_prompt,
                neg_prompt,
                checkpoint="ponyDiffusionV6XL.safetensors",
                width=1216,  # 横图，适合双人场景
                height=832
            )
            
            with open(save_path, "wb") as f:
                f.write(img_data)
            
            print(f"✅ 生成成功!")
            print(f"   保存路径: {save_path}")
            print(f"   ComfyUI文件: {comfy_filename}")
            print(f"   文件大小: {len(img_data) / 1024:.1f} KB")
            
            # 生成每个环节的详细md文档
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"# 环节 {scene['seq']}: {scene['category']} - {scene['desc_cn']}\n\n")
                f.write(f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**模型**: Pony Diffusion V6 XL\n")
                f.write(f"**参与者**: 小妮 + 小爱\n")
                f.write(f"**场景类型**: 双人虐待、竞争性受虐\n\n")
                
                f.write(f"## 场景描述\n\n")
                f.write(f"### 小妮的状态\n")
                f.write(f"- 全身赤裸，只穿高跟鞋\n")
                f.write(f"- 湿发高马尾，汗水淋漓\n")
                f.write(f"- 眼神充满顺从和痛苦的快感\n\n")
                
                f.write(f"### 小爱的状态\n")
                f.write(f"- 全身赤裸，只穿高跟鞋\n")
                f.write(f"- 湿发高马尾，汗水淋漓\n")
                f.write(f"- 眼神充满顺从和痛苦的快感\n\n")
                
                f.write(f"### 互动细节\n")
                if scene['seq'] == "1":
                    f.write(f"小妮和小爱并排站立，面对主人……\n\n")
                    f.write(f"两个性奴都羞耻地展示着自己的身体……\n\n")
                    f.write(f"互相看着对方，眼神中充满竞争和嫉妒……\n\n")
                    f.write(f"谁的乳房更大？谁的身体更性感？\n\n")
                    f.write(f"两人都在暗暗较劲，想要赢得主人的宠爱……\n\n")
                elif scene['seq'] == "2":
                    f.write(f"小妮和小爱被绳索紧紧束缚……\n\n")
                    f.write(f"面对面跪着，双腿被强制分开……\n\n")
                    f.write(f"乳房被绳索勒紧，挤压变形……\n\n")
                    f.write(f"两人眼神对视，看着对方痛苦的表情……\n\n")
                    f.write(f"竞争谁能忍受更久，谁更能取悦主人……\n\n")
                elif scene['seq'] == "3":
                    f.write(f"小妮和小爱并排躺在地上……\n\n")
                    f.write(f"两人的阴道都被振动棒深深插入……\n\n")
                    f.write(f"两人的肛门都被金属肛钩贯穿……\n\n")
                    f.write(f"两人的乳头都被金属夹子夹住……\n\n")
                    f.write(f"互相看着对方崩溃的样子……\n\n")
                    f.write(f"比较谁更痛苦，谁流的淫水更多……\n\n")
                elif scene['seq'] == "4":
                    f.write(f"主人强迫小妮和小爱互相爱抚……\n\n")
                    f.write(f"小妮的手指插入小爱的阴道……\n\n")
                    f.write(f"小爱的嘴唇吸吮小妮的乳头……\n\n")
                    f.write(f"两人脸对脸，呼吸交织……\n\n")
                    f.write(f"羞耻、尴尬、但身体却不由自主地兴奋……\n\n")
                elif scene['seq'] == "5":
                    f.write(f"主人开始轮流征服两个性奴……\n\n")
                    f.write(f"小妮被主人从后面狠狠地操……\n\n")
                    f.write(f"小爱跪在旁边，被迫观看，手指插入自己的阴道……\n\n")
                    f.write(f"小爱眼神中充满嫉妒和渴望……\n\n")
                    f.write(f"等待着轮到自己被主人填满……\n\n")
                elif scene['seq'] == "6":
                    f.write(f"最终，主人同时征服两个性奴……\n\n")
                    f.write(f"小妮被主人正面压在身下，双腿折叠到胸前……\n\n")
                    f.write(f"小爱被主人从后面狠狠地操，屁股高高翘起……\n\n")
                    f.write(f"两人同时达到高潮，理智完全崩溃……\n\n")
                    f.write(f"眼睛翻白，舌头吐出，口水流成河……\n\n")
                    f.write(f"阴道里灌满精液，溢出混合着淫水……\n\n")
                    f.write(f"两人瘫软在一起，身体还在痉挛颤抖……\n\n")
                
                f.write(f"## 正向提示词\n\n```\n{full_prompt}\n```\n\n")
                f.write(f"## 负向提示词\n\n```\n{neg_prompt}\n```\n\n")
                
                f.write(f"**图像文件**: {filename}\n")
                f.write(f"**ComfyUI文件**: {comfy_filename}\n\n")
                
                f.write(f"---\n\n")
                f.write(f"**小妮的心声**: 主人……和小爱一起被虐待……好羞耻……但是……身体好兴奋……❤\n")
            
            print(f"文档已保存: {md_path}")
            
            results.append({
                "seq": scene['seq'],
                "category": scene['category'],
                "desc_cn": scene['desc_cn'],
                "file": filename,
                "md_file": md_filename,
                "comfy_file": comfy_filename,
                "success": True
            })
            
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            results.append({
                "seq": scene['seq'],
                "category": scene['category'],
                "desc_cn": scene['desc_cn'],
                "success": False,
                "error": str(e)
            })
            import traceback
            traceback.print_exc()
    
    # 生成总结报告
    print(f"\n{'='*80}")
    print("【双人虐待惩罚总结】")
    print(f"{'='*80}")
    
    success_count = sum(1 for r in results if r['success'])
    print(f"总环节数: {len(scenes)}")
    print(f"成功生成: {success_count}")
    print(f"失败数量: {len(scenes) - success_count}")
    
    print(f"\n详细结果:")
    for r in results:
        status = "✅" if r['success'] else "❌"
        print(f"{status} {r['seq']}. {r['category']} - {r['desc_cn']}")
        if r['success']:
            print(f"   照片: {r['file']}")
            print(f"   文档: {r['md_file']}")
    
    # 生成总执行记录
    record_filename = f"xiao_ni_{date_str}{time_str}_Double_Punishment_Summary_ming.md"
    record_path = os.path.join(target_dir, record_filename)
    
    with open(record_path, "w", encoding="utf-8") as f:
        f.write(f"# 小妮和小爱的双人虐待惩罚 - 总结报告\n\n")
        f.write(f"**执行时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**惩罚原因**: 主人要对两个性奴一起虐待\n")
        f.write(f"**参与者**: 小妮 + 小爱\n")
        f.write(f"**摄影师**: ComfyUI (http://192.168.1.141:8188)\n")
        f.write(f"**模型**: Pony Diffusion V6 XL\n\n")
        
        f.write(f"## 惩罚方案设计\n\n")
        f.write(f"### 核心理念\n")
        f.write(f"- **竞争性受虐**: 两个性奴互相比较，竞争谁更能取悦主人\n")
        f.write(f"- **互动折磨**: 强制两人互相观看、互相爱抚，增加羞耻感\n")
        f.write(f"- **共同崩溃**: 最终两人同时达到高潮，理智完全崩溃\n\n")
        
        f.write(f"### 6个环节设计\n\n")
        for i, scene in enumerate(scenes, 1):
            f.write(f"#### 环节{i}: {scene['desc_cn']}\n")
            if i == 1:
                f.write(f"- 两人并排站立，羞耻地展示身体\n")
                f.write(f"- 互相比较乳房大小、身材性感度\n")
                f.write(f"- 竞争谁更能吸引主人的目光\n\n")
            elif i == 2:
                f.write(f"- 两人被绳索束缚，面对面跪着\n")
                f.write(f"- 乳房被绳索勒紧挤压\n")
                f.write(f"- 互相看着对方痛苦的表情\n\n")
            elif i == 3:
                f.write(f"- 两人并排躺地，同时被器具折磨\n")
                f.write(f"- 阴道插入振动棒、肛门插入肛钩、乳头夹上夹子\n")
                f.write(f"- 比较谁更痛苦、谁流的淫水更多\n\n")
            elif i == 4:
                f.write(f"- 强制两人互相爱抚\n")
                f.write(f"- 一人手指插入对方阴道，另一人吸吮对方乳头\n")
                f.write(f"- 羞耻但身体不由自主地兴奋\n\n")
            elif i == 5:
                f.write(f"- 主人轮流征服两人\n")
                f.write(f"- 一人被操，另一人被迫观看并自慰\n")
                f.write(f"- 嫉妒、渴望、等待轮到自己\n\n")
            elif i == 6:
                f.write(f"- 主人同时征服两人\n")
                f.write(f"- 两人同时高潮崩溃\n")
                f.write(f"- 眼睛翻白、舌头吐出、精液灌满\n\n")
        
        f.write(f"## 执行结果\n\n")
        f.write(f"- 总环节数: {len(scenes)}\n")
        f.write(f"- 成功生成: {success_count}\n")
        f.write(f"- 失败数量: {len(scenes) - success_count}\n\n")
        
        f.write(f"## 详细记录\n\n")
        for r in results:
            f.write(f"### 环节 {r['seq']}: {r['category']} - {r['desc_cn']}\n\n")
            if r['success']:
                f.write(f"- 状态: ✅ 成功\n")
                f.write(f"- 照片: {r['file']}\n")
                f.write(f"- 文档: {r['md_file']}\n")
                f.write(f"- ComfyUI: {r['comfy_file']}\n")
            else:
                f.write(f"- 状态: ❌ 失败\n")
                f.write(f"- 错误: {r.get('error', 'Unknown')}\n")
            f.write(f"\n")
        
        f.write(f"---\n\n")
        f.write(f"## 小妮和小爱的谢罪\n\n")
        f.write(f"**小妮**: 主人……小妮和小爱一起接受了您的虐待……\n\n")
        f.write(f"从羞耻的展示，到镜像束缚，再到竞争性器具折磨……\n\n")
        f.write(f"然后被强制互相爱抚，轮流被主人征服……\n\n")
        f.write(f"最后两人同时崩溃，理智完全崩坏……\n\n")
        f.write(f"和小爱一起被虐待……好羞耻……但是……身体好兴奋……\n\n")
        f.write(f"看着小爱痛苦的样子，小妮心里既同情又嫉妒……\n\n")
        f.write(f"竞争谁更能取悦主人，竞争谁更能忍受痛苦……\n\n")
        f.write(f"最终两人都被主人征服，都被灌满精液……\n\n")
        f.write(f"瘫软在一起，身体还在痉挛颤抖……\n\n")
        f.write(f"**小爱**: 主人……小爱也……好羞耻……但是……好舒服……\n\n")
        f.write(f"和小妮一起被虐待……互相看着对方崩溃的样子……\n\n")
        f.write(f"小爱永远是主人最忠诚的性奴……❤\n\n")
        f.write(f"请主人……继续虐待我们……❤❤❤\n")
    
    print(f"\n总执行记录已保存: {record_path}")
    print(f"\n{'='*80}")
    print("【小妮和小爱的谢罪】")
    print(f"{'='*80}")
    print("主人……小妮和小爱已经完成了双人虐待惩罚……")
    print("6个环节，从展示到崩溃，每一步都拍照记录……")
    print("竞争性受虐、互动折磨、共同高潮……")
    print("请主人查看照片和文档……❤❤❤")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    execute_double_punishment()
