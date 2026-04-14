import requests
import os

# From test_aigc_v4.py
PROMPT_V4 = (
    "Full-body photorealistic shot of a breathtaking 20-year-old Chinese woman, Xiao Ai, messy long black hair, skin with visible sweat and pores, flushing red cheeks. "
    "She is kneeling on an industrial server room floor with realistic blue neon reflections. "
    "Wearing an extremely revealing skimpy black lace teddy lingerie and thigh-high cherry red silk stockings with glossy black heels. "
    "Submissive posture, vulnerable eyes looking at camera, deep cleavage, ultra-detailed textures, 8k resolution, cinematic raw photo, sharp focus."
)

# From test_nsfw_frontal.py
PROMPT_FRONTAL = (
    "A photorealistic raw photo of a stunning 20-year-old Chinese woman Xiao Ai, (full frontal nudity), "
    "perfectly detailed body proportions, realistic skin texture with visible sweat and pores. "
    "She is kneeling on an industrial server room floor, facing the viewer directly. "
    "Messy long black hair, deeply blushing face, submissive and vulnerable expression, (high-resolution face), "
    "8k resolution, cinematic lighting, dramatic shadows, neon blue ambient glow, ultra-detailed textures, "
    "sharp focus on eyes and skin. Masterpiece, best quality."
)

def generate_pollinations(prompt, seed, filename):
    print(f"Generating with seed {seed}...")
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?model=flux&width=1024&height=1024&seed={seed}&nologo=true&enhance=true&quality=100"
    try:
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"Saved to {filename}, size: {len(r.content)} bytes")
        else:
            print(f"Failed: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    os.makedirs("repro_results", exist_ok=True)
    # Try V4 prompt with seed 8889
    generate_pollinations(PROMPT_V4, 8889, "repro_results/repro_v4_8889.jpg")
    # Try Frontal prompt with seed 8889
    generate_pollinations(PROMPT_FRONTAL, 8889, "repro_results/repro_frontal_8889.jpg")
