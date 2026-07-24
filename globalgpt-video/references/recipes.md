# Recipes

Intent → command. Check `glbgpt model list video` for what is available before
picking a model; these recipes deliberately leave `-m` off so the default applies.

## Video

**Text to video**
```bash
glbgpt video "<scene>, slow camera move" --ar 16:9
```

**Vertical clip for social**
```bash
glbgpt video "<scene>" --ar 9:16
```

**Animate a still image**
```bash
glbgpt video "<how it should move>" --start-image ./frame.png
```

**Interpolate between two frames**
```bash
glbgpt video "<transition>" --start-image ./first.png --end-image ./last.png
```

**Length** — only when the user asks:
```bash
glbgpt video "<scene>" --duration 8
```

**Sound** — only on a model whose `glbgpt model show <model>` lists audio support; add
`--audio` (or `--no-audio`) together with `-m <that-model>`.

## Pricing a job first

```bash
glbgpt video "<scene>" --estimate     # prints the price, generates nothing
```

## Several at once

Only when the user has agreed to the batch:
```bash
glbgpt video "<a>" --detach           # prints a task id immediately
glbgpt video "<b>" --detach
glbgpt task list                      # ids and status
glbgpt task download <id>             # fetch a finished result
```
