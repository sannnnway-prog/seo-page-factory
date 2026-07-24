# Troubleshooting

<!-- shared:login -->
## "Not signed in"

The user must run `glbgpt login` themselves — it opens a browser. On a headless box
or over SSH, `glbgpt login --code` prints a URL instead: the user opens it on any
machine with a browser, authorizes there, and pastes the code the page shows back
into the terminal. Do not
attempt to authenticate for them.
<!-- /shared:login -->

## "No prompt provided"

`--file` takes one or more paths (`--file <path...>`) and keeps eating positionals
until it hits a flag, so a prompt written after it is swallowed as another file path.
Put the prompt first: `glbgpt exec "summarise the decisions" --file notes.md`, not
`glbgpt exec --file notes.md "summarise the decisions"`.

## Not enough credits, or a plan restriction

The command reports a payment problem instead of running the delegation. Show the
user `glbgpt account` (balance and membership) and stop — do not retry, and do not
try a different model hoping it is cheaper unless the user asks.

## "Unknown model"

The catalog is server-driven and the name you used no longer exists (or never did).
Run `glbgpt model list chat` and use a name it prints.

## The delegate's code does not compile

The delegate cannot run your build. Treat its output as a draft: fix or re-delegate
with the error text attached (`--file` the build log, prompt first).
