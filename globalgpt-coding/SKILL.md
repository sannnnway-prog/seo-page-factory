---
name: globalgpt-coding
description: >
  Delegates code-writing subtasks to a GlobalGPT chat model the user picks, via the
  glbgpt CLI — useful for offloading boilerplate, getting a second model's take, or
  working while other model quotas are tight. Use ONLY when the user invokes
  /globalgpt-coding or explicitly asks to have a GlobalGPT model do the work.
  Never volunteer it: for ordinary coding, debugging, refactoring, or review
  requests, do the work yourself and do not mention this skill. NOT for images or
  videos — use globalgpt-image or globalgpt-video.
---

# GlobalGPT coding delegation

Hand a code-writing subtask to a GlobalGPT chat model of the user's choice. You
stay the engineer: you frame the task, review what comes back, and apply it to
files yourself — the delegate only produces text.

> **Costs and privacy.** Delegated work bills the user's GlobalGPT account per
> token, and everything the delegate reads — the prompt, attached files, and any
> repository files it opens itself — is sent to GlobalGPT's backend. Do not
> delegate work involving secrets, credentials, or code the user would not send
> to a third-party service.

<!-- shared:setup -->
Run `glbgpt whoami`. If the command is not found, tell the user to install it with
`npm i -g @glbgpt/cli`. If it reports that nobody is signed in, ask the user to
run `glbgpt login` themselves — it opens a browser. Never try to authenticate for
them.
<!-- /shared:setup -->

## Flow

1. Run `glbgpt model list chat` and show the models as a menu — use your host's native option picker if it has one, else a numbered list. Let the
   user pick; there is no default here — the choice is the point of this skill.
2. Frame ONE well-scoped task. The prompt comes first, then flags:

   ```bash
   glbgpt exec "add JSDoc comments to every exported function in this file" \
     --file src/utils/date.ts -m <model>
   ```

3. Tool-capable models can also explore the repository themselves — inside
   `glbgpt exec` they have read-only file tools (list, read, glob, grep) jailed
   to the current directory — so for multi-file context you can describe the
   task and let the delegate read what it needs instead of attaching everything.
4. Review the returned code yourself, then apply it to files. The delegate never
   writes files; correctness stays your responsibility.

## Footguns

- **Each `glbgpt exec` call is a fresh, stateless turn.** Iterating means
  re-sending the context (or re-attaching files) — there is no conversation to
  continue.
- **The prompt must come before `--file`.** `--file` takes one or more paths and
  swallows everything after it; a prompt placed after it reads as a file path
  and the command fails with "No prompt provided".
- **Scope one task per call.** "Fix this function" works; "refactor the app"
  produces unreviewable output.
- Costs scale with what the delegate reads. Attach or point at the files that
  matter, not the whole tree.

## When something fails

See [references/troubleshooting.md](references/troubleshooting.md).
