---
name: globalgpt-video
description: >
  Generates videos through the user's GlobalGPT account via the glbgpt CLI.
  Use when the user wants to create or generate a video, clip, animation, or b-roll —
  including animating a still image (image-to-video), turning a photo into motion,
  and first/last-frame interpolation. NOT for still images — use globalgpt-image.
  NOT for delegating code work to a GlobalGPT model — that is globalgpt-coding,
  which the user invokes explicitly.
---

# GlobalGPT video generation

Generate video through the user's GlobalGPT account with the `glbgpt` CLI.

<!-- shared:banner -->
> **Generation spends real credits.** Price a job without running it using
> `--estimate`; show the balance with `glbgpt account`.
<!-- /shared:banner -->

## Before the first call

<!-- shared:setup -->
Run `glbgpt whoami`. If the command is not found, tell the user to install it with
`npm i -g @glbgpt/cli`. If it reports that nobody is signed in, ask the user to
run `glbgpt login` themselves — it opens a browser. Never try to authenticate for
them.
<!-- /shared:setup -->

## Quick start

```bash
glbgpt video "slow waves on a beach at sunset" --ar 16:9   # minutes; blocks until saved
glbgpt video "slow waves on a beach at sunset" --estimate  # price only, generates nothing
```

The first line prints the saved path once it finishes. Files land in
`./glbgpt-output/` unless `-o <dir>` says otherwise.

## When invoked directly

If the user ran /globalgpt-video without saying what to make, run
`glbgpt model list video` and show the models as a menu — use your host's native option picker if it has one, else a numbered list — adding:
"pick one, or just tell me what to make and I'll use the default." Generate with
`-m <model>` when they pick. When this skill triggers from ordinary conversation
instead, skip the menu: use the default model and only ask something when the
subject itself is unclear.

## Before you spend

A generation you have to redo costs the full price again, so know what to generate
before you run the command — without interrogating the user:

- **Subject unclear or missing** ("make me a video"): ask what it should show — one
  short question, not a menu of options.
- **Two plausible readings**: say how you read it and confirm before generating.
  A word that does not parse cleanly, a likely typo, or anything you had to
  reinterpret to make sense of COUNTS as two readings — even if one reading feels
  obvious to you. Guessing and offering to redo doubles the cost of being wrong.
- **Subject clear**: go. Style, aspect ratio and model all have sensible defaults —
  do not ask about them unless the user seems to care.
- Never ask more than one question per turn.

## Choosing a model

Run `glbgpt model list video` and choose from what it prints. `glbgpt model show
<model>` gives one model's parameters and limits, including which aspect ratios,
resolutions and durations it accepts.

The catalog is served from the account and changes over time, so treat a model name
you remember as a guess: list first. Omit `-m/--model` entirely unless the user asked
for a specific model — the default is chosen for general use.

## Footguns

These are the mistakes that cost money or silently produce the wrong thing.

- **Reference frames belong in a flag, never in the prompt.** Use `--start-image
  ./frame.png` and `--end-image ./last.png` for image-to-video and first/last-frame
  video. A path or URL written into the prompt text reaches the media model as
  literal words; it cannot fetch anything.
- **Do not describe a result you have not seen.** Never tell the user whether the
  video has sound, what its resolution is, or how it looks. Most settings came from
  the model's own defaults, not from you.
- **Do not build a polling loop.** Video generation takes minutes and `glbgpt video`
  blocks on purpose until the file is saved. Reach for `--detach` only when you
  deliberately want several generations running at once, then collect them with
  `glbgpt task wait <id>` and `glbgpt task download <id>`.
- **Never retry a failed generation automatically.** A genuine failure is not charged,
  but a generation that timed out or was interrupted may still be running on the server
  and will be charged — retrying pays twice for the same thing. Report the failure and
  let the user decide.
- **Ask before batches.** More than two or three generations — especially videos — is
  real money. Confirm the plan with the user first.
- **Set only the parameters the user asked for.** Every flag you leave out falls back
  to a default tuned for that model; invented values make results worse and can cost
  more.

## Common jobs

Ready-made command lines for still-to-video and first/last-frame video:
[references/recipes.md](references/recipes.md).

## When something fails

Read the error text — the CLI says what went wrong (not signed in, not enough
credits, a parameter the chosen model does not support). Fix the cause or report it
to the user; never retry blindly. Common failures and what they mean:
[references/troubleshooting.md](references/troubleshooting.md).
