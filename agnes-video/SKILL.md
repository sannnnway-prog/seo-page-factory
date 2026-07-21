---
name: agnes-video
description: Generate videos through the user's Broly/New API video integration, defaulting to Kling v3. Use when the user asks for 视频生成, 生成视频, 文生视频, 图生视频, video generation, text-to-video, image-to-video, keyframe animation, reference-image video, Agnes video, or agnes-video-v2.0. Uses POST /v1/tasks and polls GET /v1/tasks/{task_id}; saves the returned result_url as a local video file.
---

# Broly Kling Video

Use this skill for video generation through Broly/New API's unified task endpoint, using Kling v3 by default.

## Runtime Contract

- Do not store or print API keys.
- Read the API key from `AGNES_API_KEY`; if absent, use `OPENAI_NEXT_API_KEY`.
- Read the base URL from `AGNES_BASE_URL`; if absent, use `OPENAI_NEXT_BASE_URL`; default to `https://anywhere.broly.ai/v1`.
- Default model is `kling-v3`. Use `veo3.1-fast` for premium/high-stakes feature pages when quality matters more than cost.
- Use `scripts/generate.py`; do not rewrite the API flow for ordinary video requests.
- Do not use local fake videos. If the API fails, report the real provider error.
- Input images must be public HTTPS URLs. The Agnes task API does not accept local image file uploads in this workflow.
- Download `result_url` without sending the API key to the CDN; only use ordinary download headers such as `User-Agent`.

## Workflow

1. Convert the user's request into a concise video prompt.
2. Choose defaults unless the user specifies otherwise:
   - `duration`: `5`
   - `aspect_ratio`: `16:9`
   - `resolution`: `720p`
   - output file: `outputs/kling-video.mp4`
3. Run `scripts/generate.py`.
4. The script submits:
   `POST {base_url}/tasks`
5. It polls:
   `GET {base_url}/tasks/{task_id}`
6. When status is `SUCCESS`, download `result_url` and save the video.
7. Verify the output file exists and has nonzero size. If practical, inspect file metadata.

## Modes

- Text-to-video: omit `--image`.
- Image-to-video: pass one public image URL with `--image`.
- Keyframe animation: pass two or more public image URLs with `--image`.
- Multi-reference video: pass two or more public image URLs and `--agnes-mode reference`.

## Command

```powershell
python "$env:USERPROFILE\.codex\skills\agnes-video\scripts\generate.py" `
  -p "A cinematic shot of a cat walking on a beach at sunset" `
  -f "outputs\kling-video.mp4" `
  --duration 5 `
  --aspect-ratio 16:9 `
  --resolution 720p
```

## Flags

- `-p, --prompt`: required prompt.
- `-f, --file`: output video path.
- `--model`: default `kling-v3`.
- `--base-url`: default from env or `https://anywhere.broly.ai/v1`.
- `--image`: public image URL; repeat for multiple images.
- `--duration`: seconds; recommended `3`, `5`, `10`, or `18`.
- `--aspect-ratio`: `16:9`, `9:16`, `1:1`, `4:3`, or `3:4`.
- `--resolution`: `480p`, `720p`, or `1080p`.
- `--negative-prompt`: optional negative prompt.
- `--seed`: optional integer seed.
- `--agnes-mode`: `keyframes` or `reference` for multi-image workflows.
- `--timeout`: total polling timeout in seconds; default `1200`.
- `--poll-interval`: seconds between polls; default `8`.
- `--extra-json`: provider-specific JSON object merged into the task payload.

## Failure Handling

- `401`: API key is rejected by Broly.
- `404`: base URL or task endpoint is wrong.
- `FAILURE`: report `fail_reason` and any `error.message`.
- Timeout: report the last task status and task id.
- Download failure: report the `result_url` and HTTP/download error.
