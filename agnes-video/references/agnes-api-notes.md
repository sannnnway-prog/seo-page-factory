# Agnes API Notes

- Base URL: `https://anywhere.broly.ai/v1`
- Auth: `Authorization: Bearer <key>`
- Submit tasks: `POST /v1/tasks`
- Poll tasks: `GET /v1/tasks/{task_id}`
- Video model: `agnes-video-v2.0`
- Image model: `agnes-image-2.1-flash`

## Video Fields

- `model`: `agnes-video-v2.0`
- `prompt`: required
- `images`: optional public HTTPS image URLs
- `duration`: supported tiers are `3`, `5`, `10`, `18`; defaults to `5`
- `aspect_ratio`: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`
- `resolution`: `480p`, `720p`, `1080p`
- `negative_prompt`: optional
- `seed`: optional
- `metadata.agnes_mode`: `keyframes` or `reference` for multi-image workflows

## Statuses

- Continue polling: `NOT_START`, `QUEUED`, `IN_PROGRESS`
- Done: `SUCCESS`; read `result_url`
- Failed: `FAILURE`; read `fail_reason` and `error`
