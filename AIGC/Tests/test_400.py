
import json, urllib.request

def test_realvis():
    url = "http://127.0.0.1:8188/prompt"
    workflow = {
        "3": {"inputs": {"seed": 1, "steps": 20, "cfg": 7, "sampler_name": "euler", "scheduler": "karras", "denoise": 1, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}, "class_type": "KSampler"},
        "4": {"inputs": {"ckpt_name": "RealVisXL_V4.0.safetensors"}, "class_type": "CheckpointLoaderSimple"},
        "5": {"inputs": {"width": 512, "height": 512, "batch_size": 1}, "class_type": "EmptyLatentImage"},
        "6": {"inputs": {"text": "a cute cat", "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
        "7": {"inputs": {"text": "", "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
        "8": {"inputs": {"samples": ["3", 0], "vae": ["4", 2]}, "class_type": "VAEDecode"},
        "9": {"inputs": {"filename_prefix": "Test", "images": ["8", 0]}, "class_type": "SaveImage"}
    }
    p = {"prompt": workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req) as f:
            print("Success:", f.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code)
        print("Response:", e.read().decode('utf-8'))

if __name__ == "__main__":
    test_realvis()
