---
name: ark-seedream-image
description: Generate images through Volcengine Ark Seedream. Use when the user asks for Ark, 火山方舟, 豆包 Seedream, Seedream 5.0 Pro, doubao-seedream, or wants to generate images with the user's direct Volcengine Ark key instead of Broly.
---

# Ark Seedream Image

Use this skill for direct image generation through Volcengine Ark.

## Runtime Contract

- Do not store or print API keys.
- Read the API key from `ARK_API_KEY`.
- Read the base URL from `ARK_BASE_URL`; default to `https://ark.cn-beijing.volces.com/api/v3`.
- Read the model from `ARK_IMAGE_MODEL`; default to `doubao-seedream-5-0-pro-260628`.
- Use `scripts/generate.py`; do not rewrite the API flow for ordinary image requests.
- The script calls `POST {base_url}/images/generations`.
- Download returned image URLs without sending the API key.
- If the API fails, report the real Ark error. Do not create placeholder images.

## Defaults

- model: `doubao-seedream-5-0-pro-260628`
- size: `1024x1024`
- response_format: `url`
- output: `outputs/ark-seedream.png`

## Command

```powershell
python "$env:USERPROFILE\.codex\skills\ark-seedream-image\scripts\generate.py" `
  -p "A clean product photo of a red apple on a white table, no text, no watermark" `
  -f "outputs\ark-seedream.png" `
  --size 1024x1024
```

## Flags

- `-p, --prompt`: required prompt.
- `-f, --file`: output image path.
- `-i, --image`: optional local reference image; repeat for multi-image input. The script sends local images as data URLs in the Ark `image` field.
- `--model`: override model.
- `--base-url`: override Ark base URL.
- `--size`: image size, for example `1024x1024`, `1536x1024`, or `1024x1536`.
- `--response-format`: `url` or `b64_json`.
- `--timeout`: request/download timeout in seconds.
- `--extra-json`: JSON object merged into the request payload.
