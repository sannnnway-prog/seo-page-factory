---
name: openai-next-image
description: Default image generation/editing skill for this user. Use for short Chinese or English requests like 生图, 画图, 生成图片, 做图, 图片生成, generate an image, draw, create an image, render, edit image, or make a picture. Uses the user's OpenAI-compatible third-party endpoint at anywhere.broly.ai with model seedream-5.0-pro and a custom base URL. Prefer this over the built-in imagegen or official gpt-image skill unless the user explicitly asks for native imagegen, official OpenAI Platform API, or another named provider.
---

# OpenAI Next Image

Use this skill for image generation through a custom OpenAI-compatible image endpoint.

## Runtime Contract

- Do not store or print API keys.
- Read the API key from `OPENAI_NEXT_API_KEY`.
- Do not send `OPENAI_API_KEY` to this third-party endpoint. If only `OPENAI_API_KEY` is present, stop and ask the user to set a dedicated `OPENAI_NEXT_API_KEY` or use an official OpenAI image workflow.
- Read the base URL from `OPENAI_NEXT_BASE_URL`; default to `https://anywhere.broly.ai/v1`.
- Read the model from `OPENAI_NEXT_MODEL`; default to `seedream-5.0-pro`.
- If the default model fails, the script can try fallback models from `OPENAI_NEXT_MODELS` or the built-in order:
  `seedream-5.0-pro,seedream-5.0-lite,nano-banana-2,gpt-image-2`.
- For seedream and nano-banana models, the script submits generation jobs to `POST /v1/tasks`, then polls `GET /v1/tasks/{task_id}` until `SUCCESS` or `FAILURE`.
- Provider-specific request fields can be passed via `OPENAI_NEXT_EXTRA_JSON` or `--extra-json '{"field":"value"}'`.
- Async image tasks are polled through `/v1/tasks/{task_id}` first. Set `OPENAI_NEXT_TASK_URL` to override the task status URL; use `{task_id}` as a placeholder.
- Network mode is automatic on Windows: if the user system proxy is enabled and its local port is reachable, use it; otherwise use direct mode.
- Set `OPENAI_NEXT_USE_PROXY=0` to force direct mode, `OPENAI_NEXT_USE_PROXY=1` to force proxy auto-detection, or `OPENAI_NEXT_PROXY=http://127.0.0.1:7897` to force a specific proxy.
- Read request timeout from `OPENAI_NEXT_TIMEOUT`; default to `600` seconds.
- Use `scripts/generate.py`; do not rewrite API code for ordinary image requests.

## Quick Command

```powershell
python "$env:USERPROFILE\.codex\skills\openai-next-image\scripts\generate.py" `
  -p "A tasteful high-fashion editorial portrait of an adult woman, fully clothed" `
  -f "outputs\image.png" `
  --size portrait `
  --quality medium
```

## Environment Setup

Use a dedicated key variable so this skill does not conflict with official OpenAI tooling:

```powershell
[Environment]::SetEnvironmentVariable("OPENAI_NEXT_API_KEY", "your-key", "User")
[Environment]::SetEnvironmentVariable("OPENAI_NEXT_BASE_URL", "https://anywhere.broly.ai/v1", "User")
[Environment]::SetEnvironmentVariable("OPENAI_NEXT_MODEL", "seedream-5.0-pro", "User")
[Environment]::SetEnvironmentVariable("OPENAI_NEXT_TIMEOUT", "600", "User")
```

If the provider says the base URL should not include `/v1`, set `OPENAI_NEXT_BASE_URL` to the exact documented API base URL. If the bare host returns HTML, it is not the image API and should not be used as a fallback.

## Workflow

1. Classify the request as text-to-image or image edit.
2. Choose a concise prompt, explicit safety constraints, size, quality, and output path.
3. Run `scripts/generate.py`.
4. The script automatically retries transient failures:
   - stale Windows proxy / `WinError 10061`
   - `RemoteDisconnected`
   - temporary DNS failures
   - upstream `429/500/502/503/504`
   - requests that exceed the hard timeout
5. For `seedream-*` and `nano-banana*`, the script submits to `POST /v1/tasks` with `model` and `prompt`. If the provider returns `task_id`, it polls Broly/New API's `/v1/tasks/{task_id}` endpoint first, then `/api/task/self?task_id=...`, and downloads `result_url` or embedded image data when the task finishes.
   - On Broly/New API, `/api/task/self` may require web-login `UserAuth` instead of API-key `TokenAuth`; `/v1/tasks` is the preferred API-key task endpoint.
6. If the first model or API format fails, the script tries the configured fallback models and reports a compact per-model error summary if all fail.
7. For `-n` batch requests, the script generates images one at a time because providers can hang or disconnect on server-side batch generation.
8. Report the output file path or the provider error. Do not substitute local placeholder images for failed API output.

## Flags

- `-p, --prompt`: required prompt.
- `-f, --file`: output file path.
- `-i, --image`: optional reference image; repeatable.
- `-m, --mask`: optional mask for inpainting.
- `--model`: override model.
- `--models`: comma-separated fallback model order, for example `seedream-5.0-pro,seedream-5.0-lite,nano-banana-2,gpt-image-2`.
- `--api-format`: `auto`, `openai-image`, `task`, `gemini`, or `chat`. Keep `auto`; use `task` for Broly seedream/nano-banana task submission.
- `--extra-json`: merge provider-specific JSON fields into the request, for example `{"background":"sync"}` if Broly documents such a switch.
- `--base-url`: override base URL.
- `--size`: `1k`, `2k`, `4k`, `portrait`, `landscape`, `square`, or a literal size.
- `--quality`: `low`, `medium`, `high`, or `auto`.
- `--format`: `png`, `jpeg`, or `webp`.
- `--timeout`: hard timeout per API attempt in seconds; defaults to `OPENAI_NEXT_TIMEOUT` or `600`.

## Failure Handling

- `401`: key is rejected by that provider; ask the user to verify the key belongs to that endpoint.
- `404`: base URL path is likely wrong; try adding or removing `/v1`.
- `model_not_found`: set `OPENAI_NEXT_MODEL` or `--model` to the provider's model name.
- `WinError 10061`: usually a stale local proxy. The script uses the proxy only when the configured local port is reachable; otherwise it falls back to direct mode.
- `RemoteDisconnected`, DNS failure, or upstream `500`: transient provider/network failure; the script retries automatically and then reports the provider error if all attempts fail.
- `502 Bad Gateway`: the provider gateway or upstream model route is unavailable. Retry later; do not switch to a local placeholder image.
- `404` with `openai_error` / `bad_response_status_code` on a model that appears in `/v1/models`: the model is visible but not routed to that API shape. Ask Broly for the correct endpoint/request body for that model.
- `success=false` / `Failed to parse request`: the provider accepted the HTTP request but rejected the body shape. Try `--api-format auto`; if that fails, Broly needs to provide the required payload schema.
- Async task timeout: the provider accepted the request but did not publish a result through `/api/task/self` before the timeout.
- Async task auth failure: Broly accepted `/v1/images/generations`, but task result endpoints rejected the API key. Confirm `/v1/tasks` details or set `OPENAI_NEXT_TASK_URL`.
- Missing key: ask the user to set `OPENAI_NEXT_API_KEY`; do not request they paste it into chat, and do not fall back to `OPENAI_API_KEY` for this third-party endpoint.
