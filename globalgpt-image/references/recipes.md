# Recipes

Intent → command. Check `glbgpt model list image` for what is available before
picking a model; these recipes deliberately leave `-m` off so the default applies.

## Images

**Square social image**
```bash
glbgpt image "<subject>, <style>" --ar 1:1
```

**Wide thumbnail or cover**
```bash
glbgpt image "<subject>, bold composition, high contrast" --ar 16:9
```

**Product shot on a clean background**
```bash
glbgpt image "<product>, studio lighting, plain white background, product photography" --ar 1:1 --res 2K
```

**Edit or restyle an existing image**
```bash
glbgpt image "<what to change>" -i ./original.png
```

**Avoid something specific**
```bash
glbgpt image "<subject>" --negative-prompt "text, watermark, extra fingers"
```

**Reproducible output** — reuse a seed the user gives you:
```bash
glbgpt image "<subject>" --seed 12345
```

## Pricing a job first

```bash
glbgpt image "<subject>" --estimate     # prints the price, generates nothing
```

## Several at once

Only when the user has agreed to the batch:
```bash
glbgpt image "<a>" --detach           # prints a task id immediately
glbgpt image "<b>" --detach
glbgpt task list                      # ids and status
glbgpt task download <id>             # fetch a finished result
```
