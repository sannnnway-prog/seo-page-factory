# Troubleshooting

<!-- shared:troubleshooting-common -->
<!-- shared:login -->
## "Not signed in"

The user must run `glbgpt login` themselves — it opens a browser. On a headless box
or over SSH, `glbgpt login --code` prints a URL instead: the user opens it on any
machine with a browser, authorizes there, and pastes the code the page shows back
into the terminal. Do not
attempt to authenticate for them.
<!-- /shared:login -->

## Not enough credits, or a plan restriction

The command reports a payment problem instead of generating. Show the user
`glbgpt account` (balance and membership) and stop — do not retry, and do not try a
different model hoping it is cheaper unless the user asks.

## "Unknown model"

The catalog is server-driven and the name you used no longer exists (or never did).
Run `glbgpt model list image` or `glbgpt model list video` and use a name it prints.

## A parameter is rejected

Support differs per model — aspect ratios, resolutions, durations, audio and
reference-image behaviour are all per-model. Run `glbgpt model show <model>` and use a
value it lists, or drop the flag entirely so the model's default applies.

## The generation failed after submitting

A genuine failure is not charged — the CLI says so when it reports one. Report the
failure and its reason to the user and let them decide what to do; never retry
automatically, because a task that timed out or was interrupted may still be running
and would then be charged again. `glbgpt task show <id>` gives the status and reason
for a specific task, and `glbgpt task list` shows recent ones.

## The command seems to hang

Video generation takes minutes and the command blocks on purpose. Wait for it. If the
process was interrupted, the task keeps running on the server: `glbgpt task list`
finds it, `glbgpt task download <id>` fetches the result once it is ready.

## The file is not where you expected

Results are saved under `./glbgpt-output/` relative to the working directory unless
`-o <dir>` was passed. The command prints the absolute path when it finishes.
<!-- /shared:troubleshooting-common -->
