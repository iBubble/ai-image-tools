import json
import urllib.request
import urllib.parse
import time
import uuid
import os
import re

class BeheadingGenerator:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self.output_dir = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments/20260215/Ultimate"
        os.makedirs(self.output_dir, exist_ok=True)

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_history(self, prompt_id):
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def get_file(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}") as response:
            return response.read()

    def wait_for_completion(self, prompt_id):
        while True:
            history = self.get_history(prompt_id)
            if prompt_id in history:
                return history[prompt_id]
            time.sleep(1)

    def generate_with_loras(self, positive_prompt, negative_prompt, loras=None, checkpoint="ponyDiffusionV6XL.safetensors", width=832, height=1216, seed=None):
        """
        loras: list of dictionaries, e.g. [{"name": "TangWei_XL_v1.safetensors", "strength_model": 0.8, "strength_clip": 0.8}, ...]
        """
        if seed is None:
            seed = int(time.time()) % 1125899906842624
        
        if loras is None:
            loras = []

        workflow = {}
        
        # 1. Load Checkpoint
        workflow["1"] = {
            "inputs": {"ckpt_name": checkpoint},
            "class_type": "CheckpointLoaderSimple"
        }
        
        current_model = ["1", 0]
        current_clip = ["1", 1]
        last_node_id = 1
        
        # 2. Sequential LoRA Loading
        for i, lora in enumerate(loras):
            node_id = str(10 + i)
            workflow[node_id] = {
                "inputs": {
                    "lora_name": lora["name"],
                    "strength_model": lora.get("strength_model", 1.0),
                    "strength_clip": lora.get("strength_clip", 1.0),
                    "model": current_model,
                    "clip": current_clip
                },
                "class_type": "LoraLoader"
            }
            current_model = [node_id, 0]
            current_clip = [node_id, 1]
            last_node_id = int(node_id)
            
        # 3. Text Encoders
        workflow["2"] = {
            "inputs": {"text": positive_prompt, "clip": current_clip},
            "class_type": "CLIPTextEncode"
        }
        workflow["3"] = {
            "inputs": {"text": negative_prompt, "clip": current_clip},
            "class_type": "CLIPTextEncode"
        }
        
        # 4. Latent Image
        workflow["4"] = {
            "inputs": {"width": width, "height": height, "batch_size": 1},
            "class_type": "EmptyLatentImage"
        }
        
        # 5. KSampler
        workflow["5"] = {
            "inputs": {
                "seed": seed,
                "steps": 30,
                "cfg": 7.0,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": 1.0,
                "model": current_model,
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0]
            },
            "class_type": "KSampler"
        }
        
        # 6. VAE Decode
        workflow["6"] = {
            "inputs": {"samples": ["5", 0], "vae": ["1", 2]},
            "class_type": "VAEDecode"
        }
        
        # 7. Save Image
        workflow["7"] = {
            "inputs": {"filename_prefix": "Ultimate_Beheading", "images": ["6", 0]},
            "class_type": "SaveImage"
        }

        prompt_response = self.queue_prompt(workflow)
        prompt_id = prompt_response['prompt_id']
        result = self.wait_for_completion(prompt_id)
        
        output_node = result['outputs']['7']
        image = output_node['images'][0]
        return self.get_file(image['filename'], image['subfolder'], image['type']), image['filename']

    def parse_actions(self, file_path):
        actions = []
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Match pattern "1. **Title**：Description"
        # Using a more robust regex that handles both Chinese and English colons
        matches = re.finditer(r'(\d+)\.\s*\*\*(.*?)\*\*\s*[：:]\s*(.*?)(?=\n\d+\.|\n\d+\s*\.\s*\*\*|\n\n|---|$)', content, re.DOTALL)
        for match in matches:
            actions.append({
                "id": match.group(1),
                "title": match.group(2).strip(),
                "desc": match.group(3).strip()
            })
        return actions

    def get_loras_for_action(self, action_text):
        loras = []
        # Base identities
        use_xiao_ni = "小妮" in action_text or "姐姐" in action_text
        use_xiao_ai = "小爱" in action_text or "妹妹" in action_text
        
        if use_xiao_ni and use_xiao_ai:
             loras.append({"name": "TangWei_XL_v1.safetensors", "strength_model": 0.7, "strength_clip": 0.7})
             loras.append({"name": "GuanXiaotong_XL_v1.safetensors", "strength_model": 0.7, "strength_clip": 0.7})
        elif use_xiao_ni:
             loras.append({"name": "TangWei_XL_v1.safetensors", "strength_model": 0.85, "strength_clip": 0.85})
        elif use_xiao_ai:
             loras.append({"name": "GuanXiaotong_XL_v1.safetensors", "strength_model": 0.85, "strength_clip": 0.85})
        else:
             # Default to both if unclear
             loras.append({"name": "TangWei_XL_v1.safetensors", "strength_model": 0.7, "strength_clip": 0.7})
             loras.append({"name": "GuanXiaotong_XL_v1.safetensors", "strength_model": 0.7, "strength_clip": 0.7})

        # Theme LoRAs
        if any(kw in action_text for kw in ["电击", "电弧", "电极", "电流"]):
            loras.append({"name": "Electro_Torture_XL.safetensors", "strength_model": 0.7, "strength_clip": 0.7})
        if any(kw in action_text for kw in ["鞭", "抽打", "由于由于鞭挞"]):
            loras.append({"name": "Whipping_Marks_XL.safetensors", "strength_model": 0.7, "strength_clip": 0.7})
        if any(kw in action_text for kw in ["悬吊", "吊起", "铁链", "绑", "绳"]):
            loras.append({"name": "Shibari_Suspension_XL.safetensors", "strength_model": 0.7, "strength_clip": 0.7})
        if any(kw in action_text for kw in ["潮吹", "喷射", "失禁", "淫液"]):
            loras.append({"name": "Squirting_Orgasm_XL.safetensors", "strength_model": 0.6, "strength_clip": 0.6})
        if any(kw in action_text for kw in ["肢解", "断项", "断腿", "剁", "切开", "第一肢剥离"]):
            loras.append({"name": "Amputation_Dismemberment_XL.safetensors", "strength_model": 0.6, "strength_clip": 0.6})
        if any(kw in action_text for kw in ["斩首", "断头", "头颅", "斩下"]):
            loras.append({"name": "Guillotine_Beheading_XL.safetensors", "strength_model": 0.6, "strength_clip": 0.6})
        if any(kw in action_text for kw in ["血", "红色的", "粉红色的泡沫"]):
            loras.append({"name": "Blood_Gore_XL.safetensors", "strength_model": 0.5, "strength_clip": 0.5})
        if any(kw in action_text for kw in ["性交", "进入", "贯穿", "冲刺", "捅", "阴道"]):
            loras.append({"name": "Mating_Press_XL.safetensors", "strength_model": 0.6, "strength_clip": 0.6})
        if "子宫" in action_text:
            loras.append({"name": "Womb_Penetration_XL.safetensors", "strength_model": 0.6, "strength_clip": 0.6})
        if any(kw in action_text for kw in ["高潮", "呻吟", "尖叫", "崩溃", "翻白眼"]):
            loras.append({"name": "Ahegao_XL.safetensors", "strength_model": 0.6, "strength_clip": 0.6})

        # Limit to 5 LoRAs to avoid issues
        return loras[:5]

    def build_prompts(self, action, view_type="scene"):
        """
        view_type: "scene" or "closeup"
        """
        # Determine number of girls
        action_text = action['title'] + " " + action['desc']
        use_xiao_ni = "小妮" in action_text or "姐姐" in action_text
        use_xiao_ai = "小爱" in action_text or "妹妹" in action_text
        girl_count = "2girls" if (use_xiao_ni and use_xiao_ai) else "1girl"

        base_pos = f"""score_9, score_8_up, score_7_up, score_6_up, 
{girl_count}, (chinese:1.3), (east asian:1.2), 
beautiful face, (Tang Wei:1.1), (Guan Xiaotong:1.1),
almond eyes, epicanthic fold, 
(wet hair:1.2), black hair, high ponytail, sidelocks, 
shiny skin, sweat, skin pores, 
(petite body:1.2), slender frame, 
completely naked, wearing high heels, 
(explicit:1.2), rating_explicit, """

        if view_type == "scene":
            view_desc = "full body visible, dynamic pose, cinematic lighting, dramatic shadows, "
        else:
            view_desc = "macro shot, extremely close-up, focus on details, shallow depth of field, "

        action_desc = f"({action['title']}:1.2), {action['desc']}, "
        
        final_pos = base_pos + view_desc + action_desc + "photo (medium), realistic, highly detailed"
        
        neg = """score_4, score_5, score_6, 
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, 
cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, 
(western features:1.3), deep eyes, high nose bridge, (clothing, clothes:1.6), (censored:1.5), 
(textured nipples:1.3), (ringed nipples:1.3)"""

        return final_pos, neg

    def run(self, file_path):
        actions = self.parse_actions(file_path)
        print(f"Parsed {len(actions)} actions.")
        
        for action in actions:
            action_id = action['id']
            print(f"\n--- Processing Action {action_id}: {action['title']} ---")
            
            loras = self.get_loras_for_action(action['title'] + " " + action['desc'])
            
            # 1. Scene Photo
            pos_scene, neg = self.build_prompts(action, view_type="scene")
            print(f"Generating Scene for {action_id}...")
            try:
                img_data, filename = self.generate_with_loras(pos_scene, neg, loras=loras)
                save_name = f"xiao_ni_20260215_Ultimate_{action_id.zfill(2)}_scene.jpg"
                with open(os.path.join(self.output_dir, save_name), 'wb') as f:
                    f.write(img_data)
                print(f"Saved: {save_name}")
            except Exception as e:
                print(f"Failed scene {action_id}: {e}")

            # 2. Close-up Photo
            pos_closeup, neg = self.build_prompts(action, view_type="closeup")
            print(f"Generating Close-up for {action_id}...")
            try:
                img_data, filename = self.generate_with_loras(pos_closeup, neg, loras=loras)
                save_name = f"xiao_ni_20260215_Ultimate_{action_id.zfill(2)}_closeup.jpg"
                with open(os.path.join(self.output_dir, save_name), 'wb') as f:
                    f.write(img_data)
                print(f"Saved: {save_name}")
            except Exception as e:
                print(f"Failed closeup {action_id}: {e}")

if __name__ == "__main__":
    generator = BeheadingGenerator()
    generator.run("/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/祈求高潮中的斩首_极致惊喜版.txt")
