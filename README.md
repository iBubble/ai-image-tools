# AI Image Tools

> AI-powered image generation and refinement studio.

## Features

- **Dual Engine**: Pollinations (fast) + ComfyUI (high quality)
- **Character Presets**: Auto-inject character-specific prompts
- **img2img Refine**: Upload and refine with LoRA models
- **Multi-Key Rotation**: Auto-switch API keys on quota limits
- **HD Resolution**: Up to 1920x1080 / 1080x1920
- **Push Notifications**: Feishu / Lab integration

## Quick Start

```bash
pip install flask Pillow
python app.py
# http://localhost:5050
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/pollinations/generate` | Pollinations generation |
| POST | `/api/comfyui/generate` | ComfyUI generation |
| POST | `/api/refine` | img2img refinement |
| POST | `/api/upload` | Upload image |
| POST | `/api/push/feishu` | Push to Feishu |
| GET | `/api/characters` | Character presets |

## License

MIT
