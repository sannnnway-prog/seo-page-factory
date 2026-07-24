---
name: globalgpt
description: >
  The all-in-one entry to the user's GlobalGPT account via the glbgpt CLI: generate
  images and videos, delegate code or text work to GlobalGPT chat models, and check
  the account — balance, billing, models, and generation tasks. Use when the user
  mentions GlobalGPT or glbgpt itself (their balance, spend, account, a past
  generation task, or "what can GlobalGPT do"), or invokes /globalgpt. When the user
  asks for a specific job in natural conversation — an image, a video, delegated
  code — prefer the specialized skills instead: globalgpt-image, globalgpt-video,
  globalgpt-coding.
---

# GlobalGPT

The one entry point to everything on the user's GlobalGPT account. Invoked bare,
show what is available and the balance; invoked with a request, just do it using
the commands below.

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

## When invoked bare

Run `glbgpt account` and present a short menu:

1. **Images** — describe one and I'll generate it (`/globalgpt-image` for the full
   workflow: model menu, recipes, editing).
2. **Video** — same, minutes-long (`/globalgpt-video` for start/end frames and recipes).
3. **Delegate code or text** to a GlobalGPT chat model (`/globalgpt-coding` for the
   full flow).
4. **Account** — balance, recent spend, past generation tasks, available models.

Then do whatever the user picks, right here, with the commands below.

## Generate

```bash
glbgpt image "a red fox in falling snow, cinematic lighting"   # blocks until saved
glbgpt video "slow waves on a beach at sunset" --ar 16:9       # minutes; also blocks
glbgpt image "a red fox in snow" --estimate                    # price only
```

Files land in `./glbgpt-output/`. Reference images go in `-i ./ref.png`
(image-to-image) or `--start-image` / `--end-image` (video) — never pasted into the
prompt text. When the user says what to make, generate with the default model —
do NOT show a model menu first; offer `glbgpt model list image|video` only when
they ask to choose. The money rules: never retry a failed generation
automatically, ask before generating more than two or three items, and never
describe a result you have not seen.

## Delegate to a chat model

```bash
glbgpt model list chat                                          # pick one first
glbgpt exec "add JSDoc to every exported function" --file src/util.ts -m <model>
```

The prompt must come before `--file`. Each call is a fresh, stateless turn.
Everything the delegate reads is sent to GlobalGPT's backend — no secrets. Review
the output yourself before applying it anywhere.

## Account and tasks

All read-only and free:

```bash
glbgpt account                 # membership + credit balance
glbgpt account transactions    # recent spend (authoritative billing)
glbgpt task list               # recent generation tasks
glbgpt task show last          # one task's status
glbgpt task download last      # fetch a finished result
glbgpt model list              # everything available on this account
```

## When something fails

Read the error — the CLI says what went wrong (not signed in, not enough credits, a
parameter the model rejects). A genuine generation failure is not charged. Never
retry blindly; report and let the user decide. Common cases:
[references/troubleshooting.md](references/troubleshooting.md). For deeper
workflows, hand over to the specialized skill: `/globalgpt-image`,
`/globalgpt-video`, `/globalgpt-coding`.
