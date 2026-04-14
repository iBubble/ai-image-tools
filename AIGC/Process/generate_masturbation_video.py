
import json
import urllib.request
import urllib.parse
import time
import uuid
import os

class ComfyUIVideoClient:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())

    def upload_image(self, image_path):
        url = f"http://{self.server_address}/upload/image"
        boundary = '----WebKitFormBoundary' + uuid.uuid4().hex
        with open(image_path, 'rb') as f:
            file_data = f.read()
            filename = os.path.basename(image_path)
        body = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'
            f'Content-Type: image/jpeg\r\n\r\n'
        ).encode('utf-8') + file_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')
        headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}
        req = urllib.request.Request(url, data=body, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read()).get("name")

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())

    def get_history(self, prompt_id):
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def get_file(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}") as response:
            return response.read()

def main():
    client = ComfyUIVideoClient()
    input_image = "/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png"
    timestamp = time.strftime("%Y%m%d%H%M")
    
    print("Step 1: Uploading source image...")
    uploaded_name = client.upload_image(input_image)
    print(f"Uploaded as: {uploaded_name}")
    
    seed = int(time.time()) % 1125899906842624
    
    # Correct SVD_XT Workflow
    workflow = {
        "1": {
            "inputs": {
                "ckpt_name": "svd_xt.safetensors"
            },
            "class_type": "ImageOnlyCheckpointLoader"
        },
        "2": {
            "inputs": {
                "image": uploaded_name,
                "upload": "image"
            },
            "class_type": "LoadImage"
        },
        "3": {
            "inputs": {
                "width": 512,
                "height": 512,
                "video_frames": 25,
                "motion_bucket_id": 180,
                "fps": 8,
                "augmentation_level": 0.0,
                "clip_vision": ["1", 1],
                "init_image": ["2", 0],
                "vae": ["1", 2]
            },
            "class_type": "SVD_img2vid_Conditioning"
        },
        "4": {
            "inputs": {
                "seed": seed,
                "steps": 20,
                "cfg": 2.5,
                "sampler_name": "euler",
                "scheduler": "karras",
                "denoise": 1.0,
                "model": ["1", 0],
                "positive": ["3", 0],
                "negative": ["3", 1],
                "latent_image": ["3", 2]
            },
            "class_type": "KSampler"
        },
        "5": {
            "inputs": {
                "samples": ["4", 0],
                "vae": ["1", 2]
            },
            "class_type": "VAEDecode"
        },
        "6": {
            "inputs": {
                "frame_rate": 8,
                "loop_count": 0,
                "filename_prefix": "XiaoNi_Video",
                "format": "video/h264-mp4",
                "pingpong": False,
                "save_output": True,
                "pix_fmt": "yuv420p",
                "crf": 19,
                "save_metadata": True,
                "trim_to_audio": False,
                "images": ["5", 0]
            },
            "class_type": "VHS_VideoCombine"
        }
    }
    
    print("Step 2: Queuing SVD video generation...")
    try:
        result = client.queue_prompt(workflow)
        prompt_id = result['prompt_id']
        print(f"Prompt ID: {prompt_id}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_body}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return
    
    print("Step 3: Waiting for video generation (M4 Max, ~2-5 min)...")
    start_time = time.time()
    while True:
        try:
            history = client.get_history(prompt_id)
            if prompt_id in history:
                break
        except:
            pass
        elapsed = time.time() - start_time
        print(f"  Waiting... {elapsed:.0f}s elapsed", end="\r")
        time.sleep(3)
    
    elapsed = time.time() - start_time
    print(f"\nGeneration completed in {elapsed:.1f}s!")
    
    print("Step 4: Extracting video...")
    outputs = history[prompt_id]['outputs']
    saved = False
    for node_id in outputs:
        node_output = outputs[node_id]
        if 'gifs' in node_output:
            for vid in node_output['gifs']:
                video_data = client.get_file(vid['filename'], vid['subfolder'], vid['type'])
                video_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/xiao_ni_{timestamp}_Masturbation_Video.mp4"
                with open(video_path, "wb") as f:
                    f.write(video_data)
                print(f"Video saved: {video_path}")
                saved = True
                
                md_path = f"/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/photos/xiao_ni_{timestamp}_Masturbation_Video_ming.md"
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(f"# 视频记录: 小妮自慰 - {timestamp}\n\n")
                    f.write(f"- **视频文件**: [xiao_ni_{timestamp}_Masturbation_Video.mp4](file://{video_path})\n")
                    f.write(f"- **基准形象**: [xiao_ni.jpg](file:///Users/gemini/Projects/Own/Antigravity/AntigravityFixed/RULES/XiaoNi_FINAL_01_standing_FIX_A_00001_.png)\n")
                    f.write(f"- **技术**: SVD_XT 图生视频, 25帧, 8fps, 约3秒循环\n")
                    f.write(f"- **渲染时间**: {elapsed:.1f}秒\n\n")
                    f.write(f"- **场景描写**: 基于小妮的原始形象，SVD赋予了她细微而淫靡的动态。画面中小妮正在自我抚慰，身体因快感而颤抖。\n")
                    f.write(f'- **小妮自白**: "主人... 小妮的动态... 被永久录制了... 每一帧都是无法抹去的羞耻..."\n')
                print(f"Description saved: {md_path}")
                break
    
    if not saved:
        print("No video found in output. Dumping:")
        print(json.dumps(outputs, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
