# Troubleshooting

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

The catalog is server-driven. Run `glbgpt model list` (optionally `chat`, `image`,
or `video`) and use a name it prints.

## A generation failed or seems stuck

A genuine failure is not charged — the CLI says so when it reports one. A video
that seems to hang is usually still generating (minutes are normal); if the process
was interrupted, `glbgpt task list` finds the task and `glbgpt task download <id>`
fetches the result once ready. Never retry automatically.

## Anything deeper

Hand over to the specialized skill: `/globalgpt-image`, `/globalgpt-video`, or
`/globalgpt-coding` — each carries its own detailed troubleshooting.
