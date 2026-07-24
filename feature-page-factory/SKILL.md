---
name: feature-page-factory
description: Build GLB GPT/OMS feature page drafts from one or more keywords. In the feature页面工厂agent project, use automatically when the user gives only a keyword, seed term, or short phrase, and start the feature-page workflow without needing an explicit "use this skill" reminder. Keep using this skill when the user adds mid-workflow requirements, corrections, examples, or questions; treat those as additive constraints unless the user explicitly pauses/stops/switches tasks. Also use when creating or updating OMS feature pages, researching feature-page keywords, drafting page modules, generating WebP image assets, generating Agnes video assets, preparing upload manifests, filling shared-login Chrome OMS tab lanes, checking social links, or running feature page QA.
---

# Feature Page Factory Skill

This is the authority for the GLB GPT OMS feature-page factory workflow in this workspace.

## Project Startup Contract

In the `feature页面工厂agent` workspace, this skill is mandatory for feature-page work.

- If the user sends only a keyword, seed term, or short phrase, start this workflow immediately.
- Do not wait for the user to say "use the skill", "follow the workflow", or "continue the skill".
- Do not let side questions, corrections, login issues, browser issues, image/upload questions, or timing questions replace the active feature-page workflow.
- After answering or applying any side request, return to the Completion Gate.
- A feature-page task is unfinished until the Completion Gate is satisfied or a blocker is explicitly reported.
- OMS work must use the shared-login Chrome tab-lane workflow on port `9222` with `--wait-login` by default.
- Do not create separate Chrome profiles or extra debug ports for OMS lanes unless the user explicitly asks in the current conversation.

## Goal

Turn one or more user-provided keywords into complete OMS feature-page draft(s), local backup draft(s), image/video assets, media manifests, and QA handoff reports.

By default, the agent does not upload images, does not publish pages, does not bypass the OMS editor, and does not call hidden APIs to modify page content.

## Core Rules

- Draft first: all pages remain `draft` unless the user explicitly asks to publish a specific path in the current conversation.
- No destructive OMS actions: do not click publish, unpublish, delete, or similar actions unless explicitly requested.
- Use one shared-login Chrome OMS browser on port `9222` with one shared profile. Default OMS lanes are 7 separate tabs inside that same logged-in browser.
- OMS filling can run in parallel across different tab lanes for different page paths. Never edit the same page/path in more than one tab lane at the same time.
- Use the Fastest Workflow: local research, page plan, backup draft, assets, WebP conversion for images, Agnes generation for videos when needed, manifest, then focused OMS filling.
- Do not paste full copy, image lists, FAQ, prompts, social links, or JSON into New via AI. New via AI is only for creating or previewing a draft skeleton, and it now requires a separate `Confirm 写草稿` step before OMS writes anything.
- Fill visible OMS editor fields with automation; do not type character-by-character when `fill()` style input is available.
- Do not invent social URLs. If no clean qualified social source is available, remove the public social block by leaving the social module `links` empty and record why; do not delete the required module object from the saved OMS config.
- Do not add root-level `modelConfig`; model settings belong inside `tool-workspace.modelPicker`.
- Time every feature-page run. Record total duration and rough duration for three main stages: copy generation, image/video generation, and OMS filling.
- Final generated image assets must be WebP files no larger than 100KB each before OMS filling, upload handoff, or final handoff.
- Final generated video assets do not have a hard file-size cap. Keep videos as small as practical while preserving clear motion, readable subject detail, stable frames, and the intended visual effect.
- Once a feature-page workflow has started, later user requirements are additive constraints inside the same workflow unless the user explicitly says to stop, pause, switch tasks, or only answer the new request.

## Workflow Persistence

Never treat a mid-workflow user message as replacing the feature-page task by default.

- If the user adds a rule, preference, correction, question, or example, apply it to the active feature-page workflow and keep going.
- If the user asks a quick question during a page build, answer briefly, then continue the workflow.
- If the user reports a bug in the workflow, fix or record the rule, then continue the workflow from the correct stage.
- If the user says only a new keyword while a previous page is incomplete, finish or clearly checkpoint the active page before starting the new keyword, unless the user explicitly says to switch.
- Do not end the turn as if the side request were the whole task while the active feature-page workflow remains incomplete.
- Only pause the workflow when the user explicitly says `stop`, `pause`, `先别做`, `只回答这个`, `切换任务`, or equivalent.

## Default Page Intake

If the user gives only a keyword, seed term, or short phrase in this project, immediately treat it as a request to create a feature page draft with this workflow. Do not ask the user to confirm that the skill should be used unless the phrase is clearly unrelated to feature-page work.

Before selecting the primary keyword or slug, check the user's keyword for spelling, grammar, and intent accuracy:

- If it is clearly correct, continue.
- If there is an obvious typo, silently normalize it and note the correction in the draft/handoff.
- If multiple corrections or meanings are plausible, ask the user to confirm before continuing.
- If the term is a competitor brand, overly broad, sensitive, or not suitable for a feature page, suggest a more accurate feature-page keyword before continuing.

Use these defaults only as provisional values before SERP intent research:

- `path`: slug from keyword, for example `ai-menu-generator`
- `template`: decide after SERP intent research; use exactly one Tool Workspace template: `image-template-1`, `video-template-1`, or `document-template-1` (LLM/document mode)
- `category` / ability: decide after SERP intent research; usually `image`, `video`, or `document`
- `language`: English
- `status`: draft

## Research

For each page, research the SERP, competitors, user discussions, X/Reddit/YouTube signals, prompt shares, trends, and internal related feature pages.

Use SEO skills when relevant. Keyword metrics must be labeled as `Measured`, `User-provided`, `Estimated`, or `N/A`; do not present estimates as measured data.

## SERP Intent And Page-Type Decision

After receiving a keyword and checking spelling/intent accuracy, run a live SERP intent check before choosing the final page type, template, modules, examples, and asset plan. Do not rely on memory for current SERP or competitor expectations.

Decide and record:

- Dominant user intent: image generation, video generation, document/text generation, style transfer, editing, inspiration/examples, comparison, or mixed.
- Best OMS template: exactly one of `image-template-1`, `video-template-1`, or `document-template-1` (LLM/document mode).
- Best category/ability: usually `image`, `video`, or `document`/`llm`, matching the chosen primary Tool Workspace mode.
- Competitor expectations: what top competing pages offer, including input controls, examples, media types, model options, before/after results, social proof, and page structure.
- Required page factory features to beat competitors: highlights, examples, model options, size options, model comparison, benchmark, YouTube/social proof, FAQ, related links, and media assets.
- Gaps or blockers: anything the current feature page factory cannot support well enough to beat the SERP competitors.

The page plan must aim to exceed competitor pages, not merely match the minimum template. If the current OMS feature-page factory cannot support a competitor-critical feature, tell the user before OMS filling and record the gap in the backup draft and final handoff.

Selection guidance:

- Use `image-template-1` when SERP intent is static image generation, image editing, filters, posters, cards, avatars, product images, or style transformation.
- Use `video-template-1` when SERP intent is motion/video generation, animation, image-to-video, text-to-video, video effects, or when top competitors clearly satisfy the query with video outputs.
- Use `document-template-1` when SERP intent is LLM text generation, document, article, email, report, resume, script, prompt text, or structured written output.
- Do not bind `model-comparison` to LLM/document mode. Use `model-comparison` only when the keyword, SERP intent, competitor expectations, user prompt, or page strategy makes model choice useful.
- Tool Workspace is single-mode. A single `tool-workspace` module cannot mix LLM + image + video controls in the same interactive generator; it has one `template` field and changing templates rewrites the mode-specific fields.
- If intent is mixed, choose the template that satisfies the strongest conversion intent and use other modules to cover secondary intent. For example, an image-primary page can still use video examples or YouTube/social proof outside Tool Workspace, and a video-primary page can still use static images in Hero/How To/Examples. If true mixed interactive generation is competitor-critical, report this as a feature-factory limitation before OMS filling.
- If the user prompt explicitly asks for a model comparison, model ranking, model picker explanation, or competitor/model alternative positioning, add `model-comparison` and consider `benchmark`.

## Page-Level Format Mixing Strategy

Use keyword search intent to flexibly combine image, video, and LLM/document content at the page level, while keeping Tool Workspace itself single-mode.

- Choose the Tool Workspace primary mode from the user's strongest conversion intent: image, video, or LLM/document.
- Then choose supporting modules to satisfy secondary intent and make the page more useful than competing pages.
- Image-primary pages can use static image Hero, 4:3 Tool Workspace materials, image Examples, plus video examples, YouTube links, or motion-focused FAQ when users also expect animation or effects.
- Video-primary pages can use video Tool Workspace materials, video Examples, and duration/quality options, plus static Hero/How-to images when they help explain the prompt, reference image, before/after setup, or visual style.
- LLM/document-primary pages can use document presets in Tool Workspace, plus image/video examples when users need visual inspiration, output previews, screenshots, or use-case demonstrations.
- If an Example item's media format does not match the Tool Workspace primary mode, do not force a generation jump. For example, when Tool Workspace is LLM/document but an Example is an image-only inspiration card, leave `buttonText` and `buttonUrl` empty unless there is a clearly relevant non-misleading action. Avoid sending image/video examples to an LLM workspace if users would expect to generate that visual.
- Mixed-intent pages must record a `formatMixPlan` in the local draft: primary workspace mode, secondary formats, which modules carry each secondary format, and why this mix best satisfies SERP intent.
- Do not over-mix formats just because the fields exist. Add secondary media only when it improves search-intent satisfaction, conversion, competitor coverage, or user comprehension.
- If competitors offer true multi-format generation in one unified tool and that capability is essential to win the query, report the current Tool Workspace limitation before OMS filling instead of pretending the secondary modules are equivalent.

## Page Modules

The current OMS feature factory editor requires the saved `modules` array to keep exactly these 14 module objects, in this order:

1. `promo-bar`
2. `tool-workspace`
3. `hero`
4. `how-to`
5. `examples`
6. `feature-highlights`
7. `model-comparison`
8. `testimonials`
9. `benchmark`
10. `youtube`
11. `twitter`
12. `reddit`
13. `faq`
14. `related-links`

Do not delete module objects from the draft config. The OMS compatibility check blocks save if the module count is not 14, if a required module is missing, if a module is duplicated, or if an unsupported module type appears.

This 14-item list is the OMS schema/save compatibility order, not the preferred public reading order. If OMS supports a separate public display order, use the Recommended Public Reading Order below. If the frontend renders strictly by the saved `modules` array and cannot separate display order from schema order, keep the saved schema order for compatibility, then report this as a feature-factory limitation because it prevents the best landing-page reading flow.

## Recommended Public Reading Order

Use this order when planning, previewing, or setting public display order. It is based on tool-page reading behavior: users should see the interactive tool first, immediately understand the value through hero context, then inspect outputs/proof, benefits, guidance, trust, objections, and related navigation.

1. `promo-bar`, only when there is a real short announcement or offer.
2. `tool-workspace`, for the primary conversion action or live generation experience.
3. `hero`, for the value proposition, primary visual, and main promise.
4. `examples`, because AI feature users usually want to see expected outputs before reading details.
5. `feature-highlights`, for concise benefits and differentiators.
6. `how-to`, to reduce friction after users understand the value and examples.
7. `model-comparison`, only when required or useful for model choice, model quality comparison, alternatives, rankings, or workflow selection.
8. `testimonials`, as User Feedback / trust support.
9. `benchmark`, only when relevant and supported.
10. `youtube`, only when strong qualified video proof exists.
11. `twitter`, only when at least 4 qualified links exist.
12. `reddit`, only when at least 4 qualified links exist.
13. `faq`, for objections and long-tail questions near the end.
14. `related-links`, always last as the final internal navigation/SEO module.

Tool Workspace and Hero should both be treated as first-screen priorities, with Tool Workspace before Hero by default. If the layout cannot fit both above the fold, Tool Workspace should appear first and Hero should immediately follow to explain the value, use case, and visual promise.

When a page uses `model-comparison` or `benchmark`, move that decision support earlier because model trust is part of the conversion decision. Recommended order when these modules are enabled:

1. `promo-bar`, only when useful.
2. `tool-workspace`
3. `hero`
4. `model-comparison`, when enabled.
5. `benchmark`, when a relevant supported benchmark exists.
6. `examples`
7. `feature-highlights`
8. `how-to`
9. `testimonials`
10. `youtube`, only when qualified.
11. `twitter`, only when qualified.
12. `reddit`, only when qualified.
13. `faq`
14. `related-links`

Feature Highlights must remain before FAQ, and Related Links must remain the final public/internal-link module.

Default useful public modules for most image feature pages:

- Tool Workspace
- Hero
- Examples
- Feature Highlights
- How To
- User Feedback / Testimonials
- FAQ
- Related Links
- Twitter/X, only if qualified
- Reddit, only if qualified

Keep non-useful required modules present but empty or disabled:

- `promo-bar`: keep `{ "type": "promo-bar" }` or empty text unless specifically needed; the current frontend may not display it.
- `feature-highlights`: always fill this module with useful page-specific highlights. Do not leave it empty.
- `feature-highlights`: use exactly 3 or exactly 6 items. Default to 3 for narrow/simple intent pages, and use 6 only when the topic is broad or competitive enough to justify more differentiators.
- Treat public sections titled `Why Choose`, `Why choose this tool`, `Why this workflow works`, or similar as the `feature-highlights` module. They must also contain exactly 3 or exactly 6 visible items, never 4 or 5.
- `testimonials`: mandatory User Feedback module. Fill it for every feature page.
- `model-comparison`: keep the required module object, but fill it only when the keyword, SERP intent, user prompt, competitor expectations, or frontend strategy justifies model choice or comparison.
- `benchmark` and `youtube`: leave empty/disabled unless the topic, SERP intent, user prompt, or frontend behavior justifies them.
- `twitter` and `reddit`: keep the module object, but set `links: []` when no qualified links exist so the public block is effectively removed.

YouTube is not a default required module. Add it only when the page topic has a strong qualified video source and the OMS/frontend behavior is confirmed.

Use as much of the current page factory as is helpful for beating competitors, while keeping the page coherent and not padded:

- Always use `feature-highlights` for concrete differentiators, such as output quality, edit control, speed, style range, privacy, or use cases.
- Always use `testimonials` as User Feedback to show plausible user value for the exact feature.
- Use `model-comparison` when the keyword, SERP, or user prompt implies model choice, model quality comparison, "best model", alternatives, ranking, or side-by-side capability differences.
- Do not use `model-comparison` merely because the Tool Workspace uses `document-template-1`; LLM/document pages should include it only when model choice helps the search intent or conversion path.
- Use `benchmark` only when there is a relevant supported leaderboard category and it helps the page compete.
- Use `youtube` only when strong video intent or a strong qualified video source exists.

## Current OMS Editor Schema

Observed from the updated OMS feature factory frontend on 2026-07-05.

Page-level visible fields:

- `path`
- `tdk.title` as SEO Title
- `tdk.description` as SEO Description
- `tdk.keywords` split by newline, comma, or Chinese comma
- `primaryKeyword`
- `navTopGroupCode`
- `navBottomGroupCode`

All modules share optional common fields:

- `title`
- `subtitle`
- `buttonText`
- `buttonUrl`

Module-specific fields:

- `promo-bar`: `text`
- `tool-workspace`: template-driven fields and child lists; see Tool Workspace Template Modes below
- `hero`: `heroImages` URL list
- `how-to`: `demoMediaUrl`; `steps[]` with `title`, `description`
- `examples`: `categories[]`; `items[]` with `title`, `category`, `prompt`, `imageUrl`, `videoUrl`, `buttonText`, `buttonUrl`
- `feature-highlights`: `items[]` with `title`, `description`
- `model-comparison`: `models[]` with `key`, `name`; `rows[]` with `label`, `values` JSON
- `testimonials`: `items[]` with `userName`, `rating`, `content`
- `benchmark`: `sourceKey`, `selectedModelName`, `limit`
- `youtube`: `links[]`
- `twitter`: `links[]`
- `reddit`: `links[]`
- `faq`: `items[]` with `question`, `answer`
- `related-links`: `links[]` with `name`, `url`

URL validation:

- Media URLs and normal URL fields must be `http://` or `https://`.
- `buttonUrl` and fields named `url` also allow site-relative `/...` paths and page `#anchor` links.
- Only GLB GPT homepage and model homepage conversion links require the current page inviter query: `?inviter=features_<current-page-slug>&login=1`. Ordinary editorial/internal links such as `/hub/...`, `/features/...`, Related Links, and same-page anchors do not get inviter tracking.
- Use the page slug without `/features/` as `<current-page-slug>`. Examples: `/home?inviter=features_ai-menu-generator&login=1` and `/home/gpt-image-2?inviter=features_ai-menu-generator&login=1`.
- If a homepage/model URL already has a query string, append `&inviter=features_<current-page-slug>&login=1`; if it has a hash, place the query before the hash.
- Apply this to homepage/model module `buttonUrl`, model CTA links, and cross-format model-page links. Do not apply it to `/hub/...` blog links, `/features/...` related links, ordinary tool/article navigation, static media URLs, external competitor/research/social URLs, or OMS/static upload URLs.
- Bare GLB GPT homepage/model links such as `https://www.glbgpt.com`, `/home`, or `/home/<model-slug>` fail QA unless they are pure non-clickable text examples. Tracked `/hub/...` links also fail QA because blog/article links should remain clean.
- Do not add inviter parameters to pure same-page anchors such as `#tool-workspace`, static media URLs, external competitor/research/social URLs, or OMS/static upload URLs.
- Do not save root-level `modelConfig`; the editor will reject it. Normalize old `modelConfig` into `tool-workspace.modelPicker`.
- The editor normalizes old `sections` to `modules`, old `hero.imageUrl/images` to `hero.heroImages`, and old social-proof links into `youtube`/`twitter`/`reddit`.

Example button/link behavior:

- `examples.items[].buttonText` and `buttonUrl` are optional.
- Each Example item must represent one output media type. Do not put both `imageUrl` and `videoUrl` on the same Example item for the same prompt.
- If the same concept needs both an image example and a video example, split it into two Example items with separate titles/categories and only one media URL each. The prompts can be related, but the image item should only have `imageUrl` and the video item should only have `videoUrl`.
- Use `Try This Prompt` with a clean `/features/<path>` link only when the Example's media/output format matches the Tool Workspace primary mode and the click will satisfy the user's expectation. Do not add inviter tracking to `/features/...` links.
- If Tool Workspace is LLM/document and an Example is image-only or video-only inspiration, usually leave `buttonText` and `buttonUrl` empty so the card works as a visual/reference example instead of a misleading generator jump.
- If Tool Workspace is image/video and an Example is text-only or document-only inspiration, also avoid forced generator jumps unless the link/action is explicitly useful.
- A cross-format Example may link only when the button text names the real action, such as `Use This Brief`, `Draft This Prompt`, or `View Workflow`, and the destination genuinely supports that action.
- If a cross-format Example should convert users into the correct generation workflow, link to a sitemap-confirmed same-format GLB GPT destination instead of the current page. For image Examples on an LLM/document page, a suitable destination can be an image model page such as `/image-generator/gpt-image-2`, `/image-generator/nano-banana-2`, `/image-generator/flux-2-pro`, or `/image-generator/ideogram-3-0-quality`, chosen by the image style and intent.
- For cross-format model-page links, use explicit button text such as `Open Image Generator`, `Generate an Image`, `Try GPT Image 2`, or `Use Nano Banana 2`; do not use `Try This Prompt` unless the destination will actually use that example prompt in the same output mode.

## Tool Workspace Template Modes

Observed from the updated OMS feature factory frontend on 2026-07-05. The current Tool Workspace module supports three single-select template modes:

- `image-template-1`
- `video-template-1`
- `document-template-1` (LLM/document mode)

The UI may describe the three high-level formats as Image, Video, and LLM. Internally the LLM/text format still uses `document-template-1`.

Tool Workspace does not currently support mixing several formats inside one interactive workspace. It exposes one `template` value, and the frontend schema switches all mode-specific child lists based on that value:

- Image mode uses image material groups, image size options, and image models.
- Video mode uses video material groups, video size/duration/quality options, optional `referenceImageUrl`, and video models.
- LLM/document mode uses document preset groups, prompt placeholder/description, generation instructions, demo document content, and LLM models.

Do not create a Tool Workspace draft that tries to include image and video and LLM fields at the same time. The editor's template switcher deletes irrelevant fields when modes change, so mixed fields are unstable and should be treated as unsupported for the primary interactive tool.

Use `image-template-1` and `category: "image"` for ordinary feature image pages unless the user explicitly asks for video or document features.

For `image-template-1`, Tool Workspace fields are:

- `template`
- `materialGroups[]`: `name`, `prompt`, `imageUrl`
- `sizeOptions[]`: `label`, `value`
- `modelPicker.models[]`: `modelId`, `label`, `freeTrialCount`, `enabled`, `locked`

Current OMS default image models:

- `nano-banana-2`, label `Nano Banana 2`, `freeTrialCount: 1`, `locked: false`, `enabled: true`
- `gpt-image-2`, label `GPT Image 2`, `freeTrialCount: 0`, `locked: true`, `enabled: true`
- `flux-2-pro`, label `FLUX.2 Pro`, `freeTrialCount: 0`, `locked: true`, `enabled: true`
- `ideogram-3-quality`, label `Ideogram 3.0 Quality`, `freeTrialCount: 0`, `locked: true`, `enabled: true`

For `video-template-1`, Tool Workspace fields are:

- `template`
- `description`
- `referenceImageUrl`
- `materialGroups[]`: `name`, `prompt`, `videoUrl`
- `sizeOptions[]`
- `durationOptions[]`
- `qualityOptions[]`
- `modelPicker.models[]`

Current OMS default video model:

- `grok-imagine-video-1.5`, label `Grok Imagine Video 1.5`, `freeTrialCount: 1`, `locked: false`, `enabled: true`

For `document-template-1` (LLM/document mode), Tool Workspace fields are:

- `template`
- `description`
- `promptPlaceholder`
- `materialGroups[]`: `name`, `prompt`, `generationInstruction`, `documentDemoContent`
- `modelPicker.models[]`

Current OMS default document model:

- `gemini-3.5-flash`, label `Gemini 3.5 Flash`, `freeTrialCount: 1`, `locked: false`, `enabled: true`

LLM/document pages may fill `model-comparison` when model choice is useful:

- If enabled, include the selected/default Tool Workspace model, usually `gemini-3.5-flash`.
- Add relevant alternative models only when they are available in OMS, help the user's decision, or can be accurately represented by the current page factory.
- Rows should compare task-relevant dimensions such as writing quality, instruction following, structure, speed, best use case, output style, or free-trial availability.
- Keep values concise and user-facing; do not invent benchmark scores or unsupported claims.

## Model Comparison And Benchmark

Use `model-comparison` to help users choose the right generation path, not as decorative copy.

`model-comparison` filling logic:

- Fill common fields only when useful: `title`, `subtitle`, `buttonText`, and `buttonUrl`. Use `#tool-workspace` for same-page actions, or an inviter-tagged internal URL for navigation.
- Add rows through the OMS child-list controls `新增对比模型列` and `新增对比项`; do not stop after common fields.
- `models[]` must include stable model keys and readable names, for example `{ "key": "gemini-3.5-flash", "name": "Gemini 3.5 Flash" }`.
- `models[].key` should be lowercase/slug-like and must exactly match the keys used inside every `rows[].values` JSON object.
- `rows[]` should compare task-relevant dimensions such as `Best role on this page`, `Strongest output type`, `Use it when`, `Prompt tip`, `Speed`, `Control`, `Free trial`, or `Best fit`.
- `rows[].values` must be valid JSON mapping every model key to a concise user-facing string.
- Every comparison row must include every model key; do not leave partial JSON values.
- Do not invent leaderboard scores, external rankings, pricing, or unsupported performance claims. Use qualitative, task-specific comparisons unless a source is available.
- For LLM/document pages where `model-comparison` is enabled, include the default Tool Workspace LLM and compare it with relevant alternatives or cross-workflow models that help the page intent.
- For image/video pages, add model comparison only when SERP intent, keyword wording, or competitor pages make model choice important.

Example row shape:

```json
{
  "label": "Best role on this page",
  "values": {
    "gemini-3.5-flash": "Draft structured briefs, prompts, and written variants.",
    "gpt-image-2": "Create polished still images from the refined brief.",
    "grok-imagine-video-1.5": "Animate short scenes when the page intent needs motion."
  }
}
```

`benchmark` filling logic:

- Enable `benchmark` only when a supported leaderboard category directly matches the page mode or helps the page compete.
- If enabled, fill `sourceKey`, `selectedModelName`, and `limit`; use a small display count such as `5` or `10`.
- If not enabled, keep `sourceKey: ""`, `selectedModelName: ""`, and `limit: 0`, and record the reason in the local draft.
- `selectedModelName` should match the current/default Tool Workspace model label when that model is being positioned.
- Do not fabricate benchmark ranks or scores. The module should point the frontend to an existing supported leaderboard source.

Supported `benchmark.sourceKey` values:

- `arena-overall-leaderboard`
- `arena-agent-leaderboard`
- `arena-text-leaderboard`
- `arena-webdev-leaderboard`
- `arena-image-to-webdev-leaderboard`
- `arena-text-to-image-leaderboard`
- `arena-image-edit-leaderboard`
- `arena-text-to-video-leaderboard`
- `arena-image-to-video-leaderboard`
- `arena-video-edit-leaderboard`
- `arena-vision-leaderboard`
- `arena-document-leaderboard`
- `arena-search-leaderboard`

Category guidance:

- LLM/document pages: consider `arena-text-leaderboard`, `arena-document-leaderboard`, `arena-search-leaderboard`, or `arena-agent-leaderboard` depending on search intent.
- Image pages: consider `arena-text-to-image-leaderboard` or `arena-image-edit-leaderboard`.
- Video pages: consider `arena-text-to-video-leaderboard`, `arena-image-to-video-leaderboard`, or `arena-video-edit-leaderboard`.
- Vision/image-understanding pages: consider `arena-vision-leaderboard`.
- Leave Benchmark disabled when none of these categories naturally supports the keyword.

## Copy Standards

- Primary keyword density target: 1%-2%, without stuffing.
- SEO correctness is the floor, not the finish line. Feature-page copy must also create desire, urgency, and a clear reason to try the tool now.
- Use the SEO content-writing principle: answer the dominant search intent above the fold before selling, then sell through specific outcomes, examples, and low-friction CTAs.
- Use the meta/CTR principle: front-load the keyword, make the value proposition concrete, and include a clear action. Titles and descriptions should be specific enough to beat generic competitor snippets.
- `tool-workspace` main title must be short, usually the tool name.
- `feature-highlights` is mandatory. Use concise, specific benefits tied to the keyword and SERP intent; avoid generic claims.
- `feature-highlights` must contain exactly 3 or exactly 6 items; never use 1, 2, 4, 5, or more than 6.
- Any visible `Why Choose` section is a feature-highlights presentation and must also use exactly 3 or exactly 6 items. If the copy naturally wants 4 or 5, consolidate to 3 stronger benefits or expand to 6 non-redundant benefits before OMS save.
- Use the Recommended Public Reading Order when planning or setting public display order: Tool Workspace, Hero, Examples, Feature Highlights, How To, Model Comparison when needed, User Feedback, optional proof/social modules, FAQ, then Related Links.
- When Model Comparison or Benchmark is enabled, use the earlier model-trust order: Tool Workspace, Hero, Model Comparison, Benchmark when relevant, Examples, Feature Highlights, How To, User Feedback, optional proof/social modules, FAQ, then Related Links.
- Feature Highlights belongs before FAQ, and Related Links belongs last.
- `How To` should use 3 steps.
- FAQ should have at most 5 items.
- When `model-comparison` is enabled, fill it with task-relevant rows, not an empty placeholder.
- Related Links: use exactly 4 sitemap-confirmed `/features/...` URLs. Do not use model pages, `/home/...`, `/models`, `/image-generator/...`, `/video-generator/...`, pricing pages, resource posts, or non-feature destinations in Related Links.
- Related Links must be selected for keyword/search-intent relevance and next-action relevance. Do not choose pages because they are new, recently published, easy to find, or merely available in the sitemap.
- User Feedback / Testimonials is mandatory. Use exactly 3 feedback items by default unless OMS/frontend layout clearly supports more.
- User Feedback must be keyword-specific and scenario-specific; do not use generic praise that could fit any AI tool.
- User Feedback `userName` should be a realistic, human-like fictional name, not a role or identity label.
- X/Twitter: use 0 links or at least 4 qualified links.
- Reddit: use 0 links or at least 4 qualified links.
- Do not keep 1-3 weak/filler social links.
- Filter social links for competitor ads, competitor product tags, and other product `.ai` promotions.
- Social links must use canonical desktop URLs that OMS/frontend parsing can recognize.
- Reddit links must use the standard comments format, such as `https://www.reddit.com/r/midjourney/comments/11bxrqn/anime_character_sheet/`.
- Do not directly use Reddit mobile share short links like `https://www.reddit.com/r/southpark/s/OYGWTn3enh`; expand them to the canonical comments URL first, or skip them if they cannot be expanded.
- If no qualified social links exist, leave that social module's `links` array empty and explain why the public social block is absent in the final handoff.

## Conversion Copywriting Standards

Every feature page must pass a conversion copy pass after the SEO/content pass.

Core copy angle:

- Write for the user's job-to-be-done, not for the module schema. Identify what the user wants to make, fix, compare, publish, share, or decide.
- Lead with the concrete outcome the user gets, such as a finished poster, realistic portrait, clean product shot, prompt-ready brief, short video effect, or polished document.
- Make the page feel useful immediately: show what to type, what result to expect, and why this tool is easier or better than starting from a blank prompt.
- Prefer specific benefits over generic AI claims. Avoid bland phrases like `powerful AI`, `easy to use`, `high quality results`, or `unlock creativity` unless they are followed by a concrete use case.
- Use lightweight marketing energy: confident, vivid, useful, and benefit-led. Do not use hype, unsupported superlatives, fake urgency, all caps, excessive punctuation, or claims that need evidence.
- When a user likely has an objection, answer it in copy: quality, realism, speed, prompt difficulty, style control, aspect ratio, commercial use, editing control, privacy, or cost.
- Keep keyword density natural. If a sentence sounds written for a crawler instead of a person, rewrite it.

Recommended copy frameworks:

- `AIDA`: hook attention, prove relevance, create desire through outcome/examples, then give one clear action.
- `PAS`: name the user's problem, clarify the friction, then position the tool as the simple next step.
- `Benefit-Proof-CTA`: state the benefit, support it with examples/features/user feedback, then point to the tool.

Module-level copy rules:

- `tdk.title`: primary keyword near the front, plus a concrete benefit or format signal. Target 50-60 English characters when possible; do not exceed visible SERP limits without a reason.
- `tdk.description`: include the primary keyword, a clear value proposition, and a CTA. Make it read like a useful promise, not a keyword list.
- `tool-workspace.title`: short tool name only. Use `subtitle`/description for the value promise.
- `hero.title`: can be more expressive than the tool title. It should answer "What can I make here?" or "Why use this now?"
- `hero.subtitle`: include the user outcome, the friction removed, and one reason to trust or try the workflow.
- `buttonText`: use action-specific CTAs such as `Create Your Image`, `Generate a Video`, `Draft My Brief`, `Try This Prompt`, or `Start Creating`. Avoid vague `Learn More` unless the destination is informational.
- `examples`: titles should sell the result, not just label the category. Pair each example with a prompt that helps the user imagine using it.
- `feature-highlights`: each item should pair a benefit with a concrete mechanism or use case, for example `Clean Style Control` plus `Lock in lighting, ratio, and mood before generation`.
- `how-to`: keep 3 steps, but make each step feel easy and progress-oriented. Use verbs like choose, describe, refine, generate, download, share.
- `testimonials`: write scenario-specific feedback that reflects believable user value, not generic praise.
- `faq`: answer objections directly first, then add nuance. Keep answers useful enough to win snippets without sounding defensive.

Required copy QA:

- Above-the-fold copy must make the tool's outcome clear without needing the user to scroll.
- The first screen must contain one clear CTA matched to the page type.
- The page must include at least one line that differentiates this GLB GPT workflow from a generic prompt box or competitor page.
- Every main module should add a new reason to try the tool; do not repeat the same benefit in Hero, Highlights, How To, and FAQ.
- If the draft feels accurate but flat, rewrite the Hero, TDK, Highlights, and CTA before OMS filling.

## User Feedback / Testimonials

The `testimonials` module is mandatory for every feature page.

- Use exactly 3 items by default.
- Each item should have `userName`, `rating`, and `content`.
- `userName` should look like a plausible real person's name, such as `Maya Chen`, `Alex Rivera`, `Jordan Lee`, or `Priya Shah`.
- Do not use role or identity labels as `userName`, such as `Content Creator`, `Marketing Designer`, `Small Business Owner`, or `Video Editor`.
- If a role is useful, mention it naturally in the feedback content, not in `userName`.
- Ratings should usually be 5 unless there is a product-approved reason to vary them.
- Feedback content must be tied to the page's exact search intent, output type, and user workflow.
- Treat unsourced feedback names as fictional/pseudonymous UI copy. Do not claim they are real users.
- Do not invent real user identities, company names, revenue claims, speed numbers, conversion rates, or external endorsements.
- If a clean sourced testimonial exists, it may be used with its source recorded in the local draft.
- If no clean source exists, write product-approved generic feedback as pseudonymous UX copy, not as a verifiable external quote.

## Social Link Relevance Tiers

Choose social links by keyword search intent, not by surface word overlap.

- Tier 1: strongly related to the exact keyword and its AI/creative generation intent. Prefer these.
- Tier 2: highly related to the keyword topic or creative use case, but not specifically about AI. Use these only when they naturally help the search intent and do not look strange on an AI feature page.
- Never use links connected to competitor AI platforms, competitor AI tools, competitor product tags, sponsored AI promotions, or other product `.ai` promotions.
- If a topic can naturally exist outside AI, Tier 2 non-AI inspiration links are acceptable. Example: for a `father's day card` feature, non-AI social posts about card ideas, handmade designs, messages, or creative inspiration can be useful because users may want card concepts and examples.
- If the keyword intent is mainly an AI-only effect or generated visual that would be odd without AI, do not use loosely related non-AI links. Example: for a `basketball on fire` effect/generator, ordinary basketball posts or fire-related posts are not useful because the intent is a generated visual effect.
- When in doubt, ask: "Would this social post help a user decide what to generate for this exact feature?" If not, skip it.
- If only Tier 2 links are available, they must still be highly relevant, clean, non-competitor, and coherent with the page examples.

## Related Link Selection

Related Links are an internal navigation and SEO relevance module, not a recency module.

- Select exactly 4 related links.
- Every related link must be sitemap-confirmed and use a `/features/...` URL unless a same-intent model page is explicitly justified elsewhere in the draft.
- Prioritize pages that share the same user intent, generation mode, asset type, style family, or use case.
- Do not include "latest", newest, recently updated, or recently created pages unless they are also one of the 4 most relevant choices for the keyword.
- Do not pad with weakly related pages just to fill a topic cluster. If fewer than 4 truly relevant internal pages exist, record the blocker/gap instead of inventing loose links.
- The local draft should include a short relevance note for each selected related link.

## Size Options

OMS size options use a display name and a size value. Use this format when planning generated assets and filling fields:

- `Square` = `1:1`
- `Portrait` = `3:4`
- `Landscape` = `4:3`
- `Widescreen` = `16:9`
- `Cinema Wide` = `21:9`
- `Vertical` = `9:16`
- `Tall Portrait` = `9:21`

The current OMS default `image-template-1` size options are:

- `Square` = `1:1`
- `Landscape` = `16:9`
- `Portrait` = `9:16`
- `Classic` = `4:3`

Add extra size options such as `21:9`, `3:4`, or `9:21` only when they are needed for the page or requested by the user. When the page needs 4:3 tool-workspace material, use `Classic = 4:3` in the OMS size options even though our asset planning may call the same ratio `Landscape`.

When calling `openai-next-image`, prefer explicit pixel sizes for feature assets instead of the script shortcuts `landscape` or `portrait`, because those shortcuts may map to 3:2 or 2:3 rather than the OMS-required ratios.

Use these explicit generation sizes by default:

- `1:1` = `1024x1024`
- `3:4` = `1152x1536`
- `4:3` = `1536x1152`
- `16:9` = `1824x1026`
- `21:9` = `1792x768`
- `9:16` = `1026x1824`
- `9:21` = `768x1792`

## Image And Asset Rules

## Image Generation API Policy

For feature-page assets, use the `openai-next-image` skill and its `scripts/generate.py` workflow by default.

- The configured provider is `https://anywhere.broly.ai/v1` unless `OPENAI_NEXT_BASE_URL` overrides it.
- The default image model is `nano-banana-2` unless `OPENAI_NEXT_MODEL` overrides it.
- The script can fall back through `OPENAI_NEXT_MODELS` or the built-in order: `nano-banana-2,nano-banana-pro,nano-banana,gpt-image-2,gpt-image-1.5`.
- Use `OPENAI_NEXT_API_KEY` for this third-party endpoint. Do not send `OPENAI_API_KEY` to `anywhere.broly.ai` or any other third-party image endpoint.
- If `OPENAI_NEXT_API_KEY` is missing but `OPENAI_API_KEY` is set, this is an image-generation blocker for the third-party endpoint, not permission to use the fallback.
- In that case, ask the user to set a dedicated `OPENAI_NEXT_API_KEY` or explicitly switch to an official OpenAI image workflow. Do not silently downgrade to PIL-generated placeholder assets.
- For `nano-banana*` models, the script submits async tasks to `POST /v1/tasks`, then polls `/v1/tasks/{task_id}` before trying any provider-specific fallback task status URL.
- Keep `--api-format auto` unless the provider documents a specific required shape; use `--extra-json` only for documented provider-specific fields.
- The script handles Windows proxy auto-detection and retries transient failures such as stale proxy `WinError 10061`, `RemoteDisconnected`, DNS hiccups, upstream `429/500/502/503/504`, and hard timeouts.
- Local PIL/vector/poster generation is allowed only for utility overlays, text cleanup, contact sheets, resizing/padding, or explicit fallback placeholders after the API fails with a real provider/network error.
- If the API is blocked, record the exact error class, attempted endpoint, and whether a sandbox-external retry was attempted. Do not mark the image/video generation stage complete with PIL placeholders or fake videos unless the user explicitly accepts that fallback.
- Keep image-generation blockers separate from OMS blockers. If New via AI or OMS skeleton creation fails, release the OMS lane and record the OMS blocker, but do not downgrade, skip, or replace the image generation stage because of that OMS issue.
- If the sandbox or network policy blocks the provider, rerun the same `openai-next-image/scripts/generate.py` command with approved sandbox-external execution. Do not rewrite API code or switch to local placeholder generation.

## Video Generation API Policy

For feature-page video assets, use the `agnes-video` skill and its `scripts/generate.py` workflow by default. The skill now uses the Broly/New API Kling video integration by default.

- The configured provider is `https://anywhere.broly.ai/v1` unless `AGNES_BASE_URL` or `OPENAI_NEXT_BASE_URL` overrides it.
- Read the API key from `AGNES_API_KEY`; if absent, the video skill may use `OPENAI_NEXT_API_KEY`.
- The default video model is `kling-v3`, unless `AGNES_MODEL` or `--model` overrides it.
- Use `veo3.1-fast` for premium or high-stakes feature pages when output quality matters more than cost/time.
- Use `scripts/generate.py`; do not rewrite the Agnes task API flow for ordinary feature video requests.
- Do not create fake local videos as a substitute for failed API output. If Agnes fails, report the real provider error and mark the video asset as blocked or retryable.
- Text-to-video omits `--image`.
- Image-to-video passes one public HTTPS image URL with `--image`.
- Keyframe animation passes two or more public HTTPS image URLs with repeated `--image`.
- Multi-reference video passes two or more public HTTPS image URLs plus `--agnes-mode reference`.
- Agnes does not accept local image files in this workflow. For image-to-video based on local generated images, first generate the still image, convert/upload it through the normal static URL workflow, then use the public HTTPS static URL as the Agnes reference.
- Default video options are `duration: 5`, `aspect_ratio: 16:9`, `resolution: 720p`, and output path like `outputs/kling-video.mp4` unless the page intent requires another supported value.
- Supported durations are `3`, `5`, `10`, and `18` seconds.
- Supported video aspect ratios are `16:9`, `9:16`, `1:1`, `4:3`, and `3:4`.
- Supported resolutions are `480p`, `720p`, and `1080p`.
- The script submits tasks to `POST /v1/tasks`, polls `GET /v1/tasks/{task_id}`, downloads `result_url` on `SUCCESS`, and saves a local video file.
- Download the final `result_url` without sending API keys to the CDN.
- After generation, verify the output file exists and has nonzero size; inspect metadata when practical.
- Do not enforce a fixed maximum video size for feature-page video assets. Optimize for the smallest practical file that still looks clear and useful on the landing page. Prefer short clips, efficient motion, 480p or 720p when sufficient, and compact encoding. If compression visibly hurts clarity, stability, or the intended effect, keep the clearer version and record the file-size tradeoff in the manifest or handoff.

## Image Lighting And Brightness

Default visual direction for feature-page assets is bright, clear, and easy to inspect.

- Unless the user or keyword explicitly asks for a special style, default to realistic, natural, photo-real image generation.
- Default prompts should use terms such as `photorealistic`, `realistic photography`, `natural texture`, `real-world lighting`, `authentic scene`, and `camera-real composition` when appropriate.
- Use stylized, illustrated, anime, cartoon, 3D, vector, collage, poster, paper-cut, clay, or graphic-design styles only when the keyword, page type, visual audit, or user request specifically calls for that style.
- If the keyword itself is a style feature, such as Ghibli, JoJo, GTA, Snoopy, silhouette, infographic, poster, card, or classical portrait, follow that style while still keeping the image polished, bright, and easy to inspect.
- Prefer bright midday sunlight, clear daytime, clean natural daylight, high-key studio light, airy white backgrounds, or sunny outdoor scenes.
- Avoid dark cinematic lighting, night scenes, dusk, sunset, golden hour, twilight, moody shadows, heavy contrast, smoky arenas, black backgrounds, and underexposed interiors unless the user explicitly asks for that mood.
- For posters and stylized graphics, use bright paper, clean white space, cheerful daylight palettes, and legible subject silhouettes.
- For photo-real assets, describe `bright noon daylight`, `clear sky`, `even exposure`, and `soft minimal shadows`.
- If an image candidate looks too dark, mark it below 8/10 and reroll with a brighter daylight prompt.

## Pre-Generation Visual Audit

Before generating images for any feature page, inspect existing GLB GPT feature-page imagery and local asset history for the same or similar topic.

Check, when available:

- The existing published feature page or OMS preview for the target path.
- Closely related live `/features/...` pages.
- Local folders under `素材库/` for similar page types, modules, styles, or user intent.
- Recent rejected or problematic examples from the project, especially images that were too dark, wrong ratio, too repetitive, low-quality, fake-text heavy, or visually confusing.

Record a short visual audit in the backup draft and/or manifest before writing prompts:

- `goodReferences`: what looks good and should be repeated, such as bright daylight, clean composition, strong subject, useful variation, polished style, correct ratio.
- `badReferences`: what should be avoided, such as dark scenes, dusk/sunset, smoky arenas, crowded unreadable posters, weak subject, fake text, wrong ratio, UI-looking tool-workspace images.
- `promptImplications`: concrete prompt rules derived from the audit.

Do not generate new images until this audit is done or explicitly blocked. If no relevant existing page or local reference exists, record `N/A` with the search locations checked.

Before generating any image or video, create an explicit asset specification for every media slot. Each slot must include:

- module
- category
- filename
- target `aspectRatio`
- intended size option label when relevant, such as `Landscape` or `Widescreen`
- prompt that states the same ratio in plain text
- media type: `image` or `video`
- generation workflow: `openai-next-image`, `agnes-video text-to-video`, `agnes-video image-to-video`, `agnes-video keyframes`, or `manual/source`

Media URLs are prefilled before upload:

```text
https://static.futureshareai.com/glb_features/<filename>.webp
https://static.futureshareai.com/glb_features/<filename>.mp4
```

The user later uploads the same-named WebP or video files in OMS, and the static URLs match automatically.

This is mandatory. Do not leave image/media URL fields empty when saving the OMS draft if the local media filename is known. The saved OMS draft should already contain every planned static media URL before the user uploads files, so after upload the user can review and publish without waiting for URL backfill.

Final assets go under:

```text
素材库/<page-slug>/selected/
```

Optional candidates go under:

```text
素材库/<page-slug>/candidates/
```

Filenames must be lowercase English, short, descriptive, hyphen-separated, and use the final upload extension. Images end in `.webp`; videos usually end in `.mp4`, for example:

- `modern-menu-card.webp`
- `restaurant-menu-board.webp`
- `wedding-menu-design.webp`
- `sunny-product-demo.mp4`
- `birthday-card-animation.mp4`

Do not name images by module position such as `example-black-and-white.webp`.

Generate PNG image candidates under the page asset folder, convert selected PNGs to WebP with `python .\convert_assets_to_webp.py`, and delete source PNG files after successful conversion. The conversion script deletes PNG files by default and enforces a 100KB maximum per final WebP image unless explicitly overridden for a non-feature-page task.

Every final selected image asset must be no larger than 100KB. Apply this in order: WebP compression, light proportional downscaling while preserving the exact intended aspect ratio, then regenerate a simpler/cleaner image if the file still cannot meet the cap without falling below landing-page quality. Do not ask the user to upload oversized images, and do not mark the asset stage complete while any selected WebP exceeds 100KB.

For video candidates, generate directly into the page asset folder as `.mp4` when possible. Do not convert video to WebP. Compress selected videos only when it preserves the intended clarity and effect; do not damage the output merely to hit an arbitrary size. If a video needs compression or format conversion, record the command and final dimensions/duration/file size in the manifest.

Every selected manifest item must include `mediaType` and `aspectRatio`. Do not rely on the filename, module name, or prompt alone to imply ratio.

Mandatory default ratios:

- Hero: `16:9` unless the user or page layout explicitly requires `21:9`.
- Tool Workspace: `4:3` only. These are pure result/content images, not UI operation screenshots.
- Examples: `3:4` by default; `9:16`, `9:21`, or `4:3` are allowed only when the example category and OMS/page layout specifically call for that size. The manifest must record the exact ratio.

For each selected image, record actual pixel dimensions and file size in bytes/KB in the manifest after WebP conversion when possible.

For each selected video, record actual width, height, duration, resolution, aspect ratio, file size in bytes/KB/MB, local path, static URL, and upload status in the manifest when possible.

## Image And Video Counts And QA

- Hero: 1 image, usually 16:9.
- Image Tool Workspace: at least 4 images, 4 styles/use cases, 4:3, pure result/content images.
- Video Tool Workspace: use video material groups when the page is video-primary; default to at least 3 video materials when feasible, with prompt/use-case variety and matching duration/aspect options.
- Image Examples: at least 10 images across at least 4 categories; vertical portrait is preferred when useful.
- Video Examples: use enough videos to demonstrate the motion intent clearly. If generating many videos is too slow or costly, use fewer video examples plus supporting still images, and record the limitation.
- For each image asset slot, generate 3 candidates by default.
- For each video asset slot, generate 1-2 candidates by default because video generation is slower and more expensive; reroll only when the result is visibly off-intent or technically broken.
- Selected images must score at least 8/10.
- Selected videos must score at least 8/10 for prompt match, motion clarity, visual quality, stability, and absence of broken frames.
- Reroll below-8 images up to 2 rounds.
- Reroll below-8 videos up to 1 round by default, unless the page requires stronger video proof.
- Images and videos must be keyword relevant, landing-page quality, clearly composed, visually stable, no logo, no readable text, adult, fully clothed, non-sexual, and free of obvious face/hand/eye/body defects.
- `tool-workspace` 4:3 material images must be pure result/content images, not UI mockups, workflow diagrams, or operation screenshots.
- Hero images may include operation/workspace demonstrations when useful.

Each page needs an asset manifest recording:

- keyword
- path
- module
- title
- category
- prompt
- mediaType
- aspectRatio
- actual width and height after conversion
- fileSizeBytes and fileSizeKB for every selected image
- duration for video
- fileSizeBytes and fileSizeMB for every selected video
- score
- reroll count
- local path
- static URL
- upload status

Before OMS filling or final handoff, run asset ratio and media validation:

```powershell
python .\validate_asset_ratios.py ".\素材库\<page-slug>"
```

If validation fails, fix or regenerate the wrong-ratio, missing, empty, or oversized image media before continuing. Do not ask the user to upload wrong-ratio assets, WebP images over 100KB, or empty/broken videos. Do not mark the feature page complete while asset validation is failing.

## Timing Tracker

For every feature-page run, track total time and rough stage time. Keep timing simple and record only these main stages:

- Copy generation: keyword check, research, page plan, copy, links, FAQ, and local draft.
- Image/video generation: prompts, OpenAI Next image generation, Agnes video generation when needed, QA/rerolls, WebP conversion for images, video metadata checks, manifest, and static URL mapping.
- OMS filling: OMS skeleton creation, visible field filling, save, version/status check, and final QA.

Store timing data in the local backup draft. For batch work, keep per-page timing and total batch timing.

## Upload Page

OMS upload URL:

```text
https://oms.broly.ai/seoManage/upload
```

The primary feature media workflow is not upload-first. Prepare local WebP image files and MP4/video files, prefill static URLs in OMS, then ask the user to upload the same-named files.

Upload request timing:

- Ask the user to upload only after OMS has been filled and saved with the matching static URLs.
- The upload checklist is for making those prefilled URLs live, not for collecting URLs to paste later.
- Do not ask the user to upload while OMS image/video URL fields are still blank.

Upload UI reference:

1. Select `图片上传` or `视频上传`.
2. Click or drag files into the upload area.
3. After upload, use `最近上传结果`.
4. `复制链接` copies `fileUrl` first, then `s3Key`.
5. If a fallback manual-copy URL is needed, paste that copied http(s) URL into the matching media field.

Upload limits:

- Images: `jpeg`, `png`, `gif`, `bmp`, `webp`; max 10 MB per file.
- Videos: `mp4`, `avi`, `mov`, `wmv`, `flv`, `webm`, `ogg`, `mkv`; max 1000 MB per file.

Feature-page image handoff uses a stricter internal cap than OMS: each final selected WebP image must be 100KB or smaller even though OMS allows larger uploads. Video handoff has no fixed internal cap; keep videos as small as practical while preserving clarity and effect.

When asking the user to upload assets, list each local media path on its own line so it can be copied one by one. Include WebP images and video files separately.

## Local Folders And Backups

Use these project folders:

- Draft backups: `草稿备份`
- Final selected assets: `素材库/<page-slug>/selected/`
- Optional candidates: `素材库/<page-slug>/candidates/`
- Asset manifest: `素材库/<page-slug>/manifest.json`

For every feature-page task, save a complete local backup draft under `草稿备份`.

- Name the backup after the page URL or slug.
- Use a filesystem-safe filename if the full URL contains Windows-invalid characters.
- Prefer `.json` for full page factory drafts.
- Save the backup before or while filling OMS.
- Update the backup after static media URLs and QA status are finalized.

## OMS New Via AI Prompt

Use a short skeleton prompt like:

```text
Create a new Features page draft with the required modules.
Path exactly: ai-menu-generator
Template: image-template-1
Ability: image
Primary keyword: ai menu generator
Public reading order: Tool Workspace, Hero, Examples, Feature Highlights, How To, User Feedback, Twitter/X and Reddit when qualified, FAQ, Related Links.
When Model Comparison or Benchmark is enabled, public reading order should move them before Examples.
Modules must keep the required OMS schema objects; public display should keep Feature Highlights before FAQ, and Related Links last.
Include Model Comparison only when search intent, competitor expectations, or the user prompt makes model choice useful.
Save as draft only. Do not publish.
```

Then fill the real content in visible editor fields.

Current OMS AI drawer behavior:

1. Click `New via AI` for a new page, or `AI Edit` for an existing page.
2. Send a short skeleton prompt only.
3. Wait for the AI response to reach `preview` status with operations.
4. Review the moduleized preview. It can be adjusted before writing.
5. Click the `Confirm write draft` button (`Confirm 写草稿` in the OMS UI) to write the draft.
6. If the operation is delete or unpublish, OMS requires an explicit destructive-action checkbox. Do not use those operations unless the user explicitly requested them in the current conversation.

Because the AI drawer can modify or create content only after the confirm-write step, do not assume sending a prompt has saved a draft. The safer agent path remains: create a minimal skeleton via AI, then fill visible editor fields in the regular edit drawer.

## OMS Visible Editing

- Before opening or editing OMS, acquire an OMS tab lane with `python .\oms_lock.py acquire --owner "<thread/page>" --path "<page-slug>" --open-tab --launch-browser --wait-login`.
- If one lane is acquired, use only that lane's returned `target_id`, `debug_url`, and tab for this page.
- If all configured tab lanes are busy, either increase `--lanes` or continue local draft/assets and leave the page at `ready_for_oms_lane`.
- For a single page, default to one OMS lane, one browser tab, one edit drawer, and one final save after all local draft/media fields are ready. Do not open extra OMS windows/tabs for the same page just to check fields.
- Extra OMS opens or extra saves are allowed only for real recovery or QA needs: skeleton creation failure, save validation failure, dynamic-list read-back failure, stale OMS form-list items, login/session loss, or a new user requirement after the first fill.
- Avoid saving after each module. Fill all visible fields in one focused pass, read back dynamic lists before save, then save once and do post-save status/version checks.
- Use visible form fields.
- Use Playwright-style `fill()` where possible.
- Do not type field content character by character.
- Do not enter JSON page details as the main edit method.
- Do not call APIs or use console scripts to secretly modify content.
- For dynamic modules such as `feature-highlights`, `examples`, `testimonials`, `faq`, and `related-links`, prefer card-scoped field selection over global field indexes. Global indexes drift when optional items are added, removed, or normalized.
- When selecting OMS cards or fields in browser automation, scope all DOM queries to the currently visible edit drawer, preferably the last visible `.ant-drawer`. Do not run dynamic-list checks against global `.ant-drawer` selectors, because Ant Design may keep old hidden drawer DOM in the page.
- Before saving dynamic list modules, normalize the visible item count first, then fill, then read the same card back from the DOM and assert the exact count and required non-empty fields. If the read-back check fails, do not save.
- For `feature-highlights`, the read-back check must confirm exactly 3 or exactly 6 visible items, and every visible item must have both a non-empty title and a non-empty description. A card with only titles filled is a blocking QA failure.
- For `related-links`, the read-back check must confirm exactly 4 visible links. Overwriting the first 4 fields is not enough; any extra visible related-link item must be deleted before saving.
- If visible dynamic-list deletion appears to work before save but the item returns after reopening the saved draft, treat it as an OMS form-list persistence bug. Use the visible `AI Edit` drawer with a narrow prompt that changes only that module, click `Confirm 写草稿`, then reopen the draft and verify the stale visible item labels are gone.
- Use current visible button text such as `保存草稿`, `编辑`, `新增功能亮点`, and `新增相关链接` when available. Do not rely only on mojibake button text captured from older logs.
- URL modules should use `新增 URL`.
- The updated editor also exposes preview and HTML download actions in the edit drawer. Use preview/download only for QA when useful; they do not replace saving the OMS draft.
- Save is blocked by frontend compatibility validation. Before saving, ensure the draft keeps the 14 required module objects, has no duplicate/unsupported module type, all URL fields pass the URL rules, and root `modelConfig` is absent.
- Every image/video media field with a known local filename must be filled with the matching `https://static.futureshareai.com/glb_features/<filename>.<ext>` URL before saving.
- After saving, check path, status, version, and any dynamic-list modules changed in this pass. If the page was saved after editing `feature-highlights` or `related-links`, verify the public/preview or OMS read-back does not show blank highlight descriptions or more than 4 related links.
- Release the tab lane with `python .\oms_lock.py release --owner "<thread/page>"` after save/check, or when abandoning the OMS session.

## Shared-Login OMS Tab Lanes

Use one logged-in Chrome profile and multiple isolated OMS tabs. This avoids repeated OMS login while still allowing concurrent OMS filling.

- Lane files: `.oms-lanes/oms-tab-lane-<n>.json`
- Shared Chrome port: `9222`
- Shared profile: `%USERPROFILE%\.codex\oms-shared-chrome-profile`
- Default lane count: `7`
- The user logs into OMS once in this shared Chrome profile; all OMS tabs share that session.
- If OMS shows a login page, keep the task running and wait for the user to log in once in the shared browser. Do not require the user to return to every conversation and say login is complete.
- Different page paths may fill OMS simultaneously in different tab lanes.
- The same page/path must not be edited in two tab lanes at once.
- If all 7 default tab lanes are busy and speed matters, increase the lane count with `--lanes 10` or another suitable number.
- Do not force-release an active tab lane.
- If a tab lane is stale because the previous thread crashed, it can be replaced only after checking the timestamp and owner. The helper script treats lane files older than 4 hours as stale by default.
- Record lane wait/setup time inside the `OMS filling` timing stage when relevant.

Recommended commands:

```powershell
python .\oms_lock.py acquire --owner "thread-or-page-name" --path "ai-menu-generator" --open-tab --launch-browser --wait-login
python .\oms_lock.py status
python .\oms_lock.py release --owner "thread-or-page-name"
```

Fastest path: use `acquire --open-tab --launch-browser --wait-login` so the shared browser launches if needed, a new OMS tab opens, login is reused or awaited, and the tab lane is reserved in one step.

If the shared browser only needs to be opened, use:

```powershell
python .\oms_lock.py launch
curl.exe http://127.0.0.1:9222/json/list
```

## Shared Chrome OMS Browser On Windows

Use one dedicated Chrome profile for all OMS tab lanes. A Windows PowerShell launch command can be adapted like this:

```powershell
$port = 9222
$profile = "$env:USERPROFILE\.codex\oms-shared-chrome-profile"
New-Item -ItemType Directory -Force -Path $profile
Start-Process chrome.exe -ArgumentList "--remote-debugging-port=$port", "--user-data-dir=$profile", "https://oms.broly.ai/seoManage/featuresFactory"
```

Check control:

```powershell
curl.exe http://127.0.0.1:$port/json/list
```

If the shared browser is not logged in, the user logs in once in this browser. Do not create separate Chrome profiles for each feature page unless the user explicitly wants separate sessions.

## Single-Page Workflow

Before drafting copy or assets, complete the SERP intent and competitor check. Use that result to choose one primary Tool Workspace mode: `image-template-1`, `video-template-1`, or `document-template-1` (LLM/document mode). Decide whether `model-comparison` or `benchmark` is needed from keyword intent, competitor expectations, model-choice value, and user prompts; do not add `model-comparison` merely because the page uses LLM/document mode. Create a `formatMixPlan` for any secondary image/video/LLM formats that should appear in non-workspace modules, and report any feature-factory limitation that prevents the page from beating competitors.

1. Start the timing tracker.
2. User provides one related seed term.
3. Check keyword spelling, grammar, and intent accuracy; normalize obvious typos or ask for confirmation when ambiguous.
4. Select one target keyword for the feature page.
5. Research SERP, competitors, user discussions, social signals, prompt shares, trends, and internal related feature pages.
6. Create the page plan and full local draft, including the Tool Workspace primary mode and any page-level `formatMixPlan`.
7. Run a conversion copy pass on TDK, Hero, Tool Workspace subtitle/description, CTAs, Examples, Feature Highlights, Testimonials, and FAQ before image generation or OMS filling.
7. Before image generation, run the Pre-Generation Visual Audit and record good/bad references plus prompt implications.
7. Save the local backup under `草稿备份`.
8. Generate candidate images and/or videos into `素材库/<page-slug>/candidates/` when useful.
9. Select final media, convert selected images to WebP, keep selected videos in their final upload format, and place them in `素材库/<page-slug>/selected/`.
10. Create or update the asset manifest and static URLs.
11. Run `python .\validate_asset_ratios.py ".\素材库\<page-slug>"` and fix any wrong-ratio, over-100KB image, or empty/broken video assets before OMS filling.
11. Acquire an OMS tab lane.
12. Use the acquired shared-login OMS tab to create the OMS draft skeleton and fill visible fields in one focused pass.
13. Prefill media fields with matching `https://static.futureshareai.com/glb_features/<filename>.<ext>` URLs.
14. Save the OMS draft with all known image/media URLs already filled.
15. Release the OMS tab lane after save/check.
16. Tell the user which same-named WebP and/or video files to upload through OMS upload.
17. Final check draft content, module completeness, links, static media URLs, draft status, version, timing, and QA report.
18. User publishes manually.

## Fastest Workflow

Use this flow to avoid long, fragile OMS sessions:

Fastest does not mean skipping SERP intent. Before local drafting, do the keyword spelling check, SERP intent check, competitor expectation scan, template/category decision, and feature-factory gap check. The local draft must include Feature Highlights and should use any useful current page-factory modules needed to beat competitors.

1. Start the timing tracker.
2. Check and normalize the user seed term for spelling, grammar, and intent accuracy.
3. Pick one primary keyword from the corrected/approved seed term.
4. Draft the full page locally first, including modules, copy, prompts, related links, FAQ, static media URLs, and social removal reasons.
5. Run the conversion copy pass locally: sharpen the value proposition, CTA, hero promise, example titles, feature benefits, and objection-handling FAQ before OMS work.
5. Before image generation, run the Pre-Generation Visual Audit and record good/bad references plus prompt implications.
5. Save the backup under `草稿备份` before touching OMS.
6. Generate and select all needed images and/or videos, then convert selected PNG images to WebP while keeping selected videos in final upload format.
7. Update the backup with final filenames, static URLs, image/video QA scores, timing data, and upload checklist.
8. Run `python .\validate_asset_ratios.py ".\素材库\<page-slug>"` and fix any wrong-ratio, over-100KB image, or empty/broken video assets.
9. Only after local draft and assets are complete and ratio validation passes, acquire/open an OMS tab lane with `python .\oms_lock.py acquire --owner "<page-slug>" --path "<page-slug>" --open-tab --launch-browser --wait-login`.
9. Open the acquired shared-login OMS tab lane and fill the draft in one focused pass.
10. Save OMS with all known static image/media URLs already filled.
11. Release the OMS tab lane after save/check.
12. At the upload checkpoint, list each WebP or video file path on its own line for the user; do not ask for returned URLs unless a fallback manual URL is truly needed.
13. Run final checks and hand off for manual upload/review/publish with timing summary.

Avoid:

- Do not interleave keyword research, page writing, image prompting, and OMS editing in one long browser session.
- Do not wait inside OMS while generating images.
- Do not over-collect related links; choose 4.
- Do not choose related links by latest/newest page order; choose the 4 most relevant sitemap-confirmed internal links.
- Do not keep weak social modules with only 1-3 links.
- Do not use mobile social share short links in OMS, especially Reddit `/s/<share_id>` links.
- Do not use the in-app browser for long OMS filling if the shared-login Chrome OMS browser is available.
- Do not fill OMS without holding an OMS tab lane.

Estimated timing after process stabilization:

- Simple feature with limited examples: 60-90 minutes to ready-for-upload draft.
- Feature with 3+ example subcategories and many images: 90-150 minutes to ready-for-upload draft.
- Final check after user upload: usually 10-20 minutes.

## Batch Workflow

When the user provides multiple keywords, enter batch mode.

Parallelizable:

- SERP intent and competitor checks
- Research
- Page plans
- Social link search
- Image/video generation
- Image/video candidate QA

Sequential only:

- OMS draft creation
- OMS saving

Before batch work, check:

- Project directory exists.
- Paths are not duplicates.
- The shared-login Chrome browser is controllable on port `9222`, or it can be launched.
- OMS tab is open and logged in, or the agent is actively waiting for the shared browser login to complete.
- No active lane is editing the same path.
- No CAPTCHA or global browser blocker is present.

Each page tracker should include:

- keyword
- path
- SERP intent
- template/category decision
- competitor gap or advantage note
- stage
- started at
- ended at
- total duration
- copy generation duration
- image/video generation duration
- OMS filling duration
- OMS status
- version
- asset folder
- media count
- keyword density
- X URL count
- Reddit URL count
- FAQ count
- blocker
- upload status

If one page fails, record the blocker and continue to the next page. Stop the whole batch only for global blockers such as login wait timeout, CAPTCHA, no controllable shared-login Chrome browser, OMS unavailable, or browser state stolen.

## QA Checklist

Before handoff, verify:

- Path exactly matches the approved slug.
- Status is draft.
- Version changes after save.
- SERP intent decision is recorded, including chosen template/category and why.
- Tool Workspace primary mode is recorded as exactly one of Image, Video, or LLM/document; any secondary media formats are documented as non-workspace support modules, not mixed Tool Workspace controls.
- If `model-comparison` is enabled, it is filled with task-relevant model rows.
- If the page uses more than one format, `formatMixPlan` explains the primary mode, secondary formats, carrying modules, and search-intent reason.
- Competitor expectations are recorded, along with how this page exceeds them.
- Any feature-factory limitation that prevents exceeding competitors is reported to the user.
- Keyword density is 1%-2%.
- Conversion copy pass is complete: above-the-fold outcome is clear, TDK/Hero/CTA are compelling, and main modules sell distinct user benefits without hype.
- TDK title and description front-load the keyword, state a concrete value proposition, and include a clear reason to click or try.
- Hero copy answers the user's search intent and gives a specific reason to use GLB GPT instead of a generic prompt box or competitor page.
- Feature Highlights is filled with specific, keyword-relevant benefits.
- Feature Highlights has exactly 3 or exactly 6 items.
- Every visible Feature Highlights item has both a non-empty title and a non-empty description after OMS read-back or preview/public QA.
- Recommended Public Reading Order is used when OMS/frontend supports separate display order, or a feature-factory limitation is recorded if display order cannot differ from save schema order.
- Public display order places Tool Workspace before Hero when supported.
- Public display order places Model Comparison and Benchmark before Examples when those modules are enabled.
- Feature Highlights appears before FAQ in the public/module plan.
- User Feedback / Testimonials is filled with 3 keyword-specific feedback items by default.
- User Feedback `userName` values are realistic human-like fictional names, not roles or identity labels.
- User Feedback does not claim unsourced names are real users and does not invent company names, precise metrics, or external endorsements unless sourced.
- Pre-Generation Visual Audit exists in the backup draft or manifest, including goodReferences, badReferences, and promptImplications.
- Media URLs match local selected filenames and final extensions.
- Every selected manifest item has `mediaType` and `aspectRatio`.
- Actual image dimensions, WebP file sizes, and video existence/non-empty checks pass `python .\validate_asset_ratios.py ".\素材库\<page-slug>"`.
- Every selected WebP image is no larger than 100KB, and oversized images are recompressed, proportionally downscaled, or regenerated before upload handoff.
- Every selected image manifest item records actual dimensions plus `fileSizeBytes`/`fileSizeKB`.
- Selected video files have nonzero size, record width, height, duration, resolution, aspect ratio, and `fileSizeBytes`/`fileSizeMB` when practical, and are compressed only as far as quality allows.
- All known image/media URL fields are prefilled before the user upload request.
- Hero has 1 image.
- Image Workspace has at least 4 images across 4 styles/use cases when the page is image-primary.
- Video Workspace has enough video materials to demonstrate the motion workflow when the page is video-primary; record any intentional reduction caused by video cost/time.
- Image Examples have at least 10 images across at least 4 categories when the page is image-primary.
- Video Examples demonstrate the motion intent clearly when the page is video-primary; supporting still images are allowed when noted in the draft.
- Example categories match media categories.
- Each Example item has only one output media URL type: either `imageUrl` or `videoUrl`, not both. If a concept needs both image and video, it is split into separate Example items.
- Cross-format Example cards do not have misleading `buttonUrl` jumps. If an Example's media format differs from the Tool Workspace primary mode, its button is empty or its button text/action clearly matches the real supported workflow.
- Cross-format Example links, when used, point to sitemap-confirmed same-format GLB GPT destinations such as image model pages for image examples, not to an incompatible current-page workspace.
- GLB GPT homepage/model conversion links include `inviter=features_<current-page-slug>&login=1`; `/hub/...`, `/features/...`, Related Links, tool/article navigation, and pure same-page anchors such as `#tool-workspace` remain untracked.
- FAQ has at most 5 items.
- Related Links is the final public/internal-link module.
- Related Links contains exactly 4 sitemap-confirmed links, each with a keyword/search-intent relevance reason.
- Related Links must be feature pages only; `model-comparison` does not create an exception for model or generator URLs.
- Related Links are not selected by latest/newest page order.
- X/Twitter has 0 or at least 4 qualified links.
- Reddit has 0 or at least 4 qualified links.
- Social links are Tier 1 or acceptable Tier 2 by search intent, not merely surface-related.
- Social links use canonical desktop URLs; Reddit `/s/<share_id>` mobile share links are not present.
- Each selected image or video scores at least 8/10, or the reroll/blocker reason is recorded.
- No unauthorized publish or destructive action occurred.
- OMS filling was done while holding an OMS tab lane, or the page is explicitly left at `ready_for_oms_lane`.
- OMS dynamic-list QA passed after save for any edited dynamic module: no blank Feature Highlights descriptions, no extra Related Links beyond 4, and no stale visible list items left from older drafts.
- Root `modelConfig` is not present; model config is under `tool-workspace.modelPicker` if used.
- The local backup exists and matches the OMS draft intent.
- The upload checklist lists one media file path per line.
- The handoff does not require the user to send returned upload URLs when filenames/static URLs already match.

## Completion Gate

A feature-page task is not complete until all applicable items below are true or an explicit blocker is reported:

- Keyword spelling, grammar, and intent accuracy have been checked.
- One primary keyword and slug/path have been chosen.
- SERP intent and competitor research have been completed before choosing the final template/category.
- Tool Workspace has exactly one primary template selected; if mixed LLM/image/video interactive controls are needed to beat competitors, the unsupported mixed-workspace limitation is explicitly reported before OMS filling.
- If `model-comparison` is enabled, it is filled and explains the selected/default model or workflow against relevant alternatives.
- Mixed-format pages include a `formatMixPlan` that uses secondary modules to satisfy image/video/LLM intent without mixing Tool Workspace controls.
- Example items do not combine `imageUrl` and `videoUrl`; same-concept image/video outputs are split into separate items.
- Cross-format Examples either omit `buttonText`/`buttonUrl` or use a non-misleading action that matches the Tool Workspace's real primary mode.
- If a cross-format Example links to another GLB GPT page, that destination is sitemap-confirmed, same-format, and named by accurate button text.
- All GLB GPT homepage/model conversion links include `?inviter=features_<current-page-slug>&login=1` or `&inviter=features_<current-page-slug>&login=1`; `/hub/...`, `/features/...`, and Related Links remain clean unless the user explicitly provides a tracked URL.
- The page plan states how the page will exceed competitor pages, or clearly reports which competitor-critical requirement the current feature factory cannot support.
- Page copy and modules have been drafted according to this skill.
- Conversion copy pass has been completed and recorded in the local draft or QA notes.
- Above-the-fold copy contains a clear outcome, a concrete value proposition, and one page-type-matched CTA.
- The page plan follows the Recommended Public Reading Order when supported, or records the OMS/frontend limitation if only schema order can be rendered.
- Public display order places Tool Workspace before Hero when supported.
- If `model-comparison` or `benchmark` is enabled, public display order places those modules before `examples`.
- Feature Highlights is filled and not left empty.
- Feature Highlights has exactly 3 or exactly 6 items and appears before FAQ.
- Feature Highlights has been read back from OMS/preview/public output after save when edited, and every visible item has both title and description.
- User Feedback / Testimonials is filled with 3 keyword-specific items by default; `userName` values are realistic human-like fictional names, not roles, with no unsourced real-user claims or precise claims.
- Exactly four sitemap-confirmed related links are selected for keyword/search-intent and next-action relevance, not because they are latest/newest.
- Related Links must be feature pages only; `model-comparison` does not create an exception for model or generator URLs.
- Related Links is the final public/internal-link module.
- Related Links has been read back from OMS/preview/public output after save when edited, and there are exactly 4 visible links with no stale extra links from older drafts.
- Social modules are either filled with qualified links or kept as empty `links: []` modules with a clear public-removal reason.
- Pre-Generation Visual Audit has been completed before image generation, or an explicit no-reference blocker/N/A note is recorded.
- Required media assets are generated, QA checked, converted to final upload format, and stored under `素材库/<page-slug>/selected/`.
- Selected images are converted to WebP; selected videos remain in their final video upload format such as MP4.
- Asset manifest exists and maps each selected media file to its static URL.
- Asset manifest includes `mediaType`, `aspectRatio`, actual dimensions and file size for selected images, and video width/height/duration/file size when practical.
- Asset ratio and media validation passes before OMS filling and before asking the user to upload.
- Every selected WebP image is 100KB or smaller.
- Every selected video is clear enough for the landing page and as small as practical without visible quality loss.
- Local backup draft exists under `草稿备份`.
- OMS is filled through a shared-login Chrome OMS tab lane using visible fields.
- All known image/media URLs are prefilled with matching `https://static.futureshareai.com/glb_features/<filename>.<ext>` URLs before the user upload request.
- OMS draft is saved, status/version/path are checked, and no publish/delete/unpublish action was taken.
- Upload checklist lists one media path per line.
- Timing summary includes copy generation, image/video generation, OMS filling, and total duration.

If a user message adds new requirements before this gate is reached, incorporate the requirement and continue toward this gate.

## Final Handoff

For a single page, report:

- OMS path
- draft status
- version
- SERP intent decision and chosen template/category
- competitor-exceeding strategy and any feature-factory limitation
- module completion
- public display order status, including any OMS/frontend limitation if schema order cannot be separated from reading order
- conversion copy pass status, including TDK/Hero/CTA strength and any remaining weak-copy notes
- local asset folder
- manifest path
- prefilled static URLs
- image/video QA scores
- pre-generation visual audit summary
- asset ratio and media validation result
- keyword density report
- timing summary: copy generation, image/video generation, OMS filling, and total duration
- upload pending reminder
- blockers or confirmations

For batch work, report a table with keyword, path, status, version, asset folder, upload status, density, image/video QA, total duration, slowest stage, and notes.

## Retrospective Lessons

From the first two pages in this project, the most expensive steps were:

1. OMS/browser overhead.
   Complete local draft and assets first, then use OMS only for focused filling and checking.
2. Image/video generation and asset mapping.
   Use an asset manifest with field/module, category, filename, local path, static URL, score, and upload status.
3. Related links and social filtering.
   Keep related links to 4 sitemap-confirmed URLs. Remove weak social modules instead of forcing links.
4. Schema/detail corrections.
   Start from this skill and the known template conventions. Keep `modelPicker` under `tool-workspace`.

## Feature Factory Product Improvements

Recommended OMS improvements that help agent-assisted generation while preserving manual editing:

1. Add JSON import/export for full drafts.
2. Add schema validation with actionable errors.
3. Add an asset manifest panel with media field, ratio, filename, upload status, and final URL.
4. Add filename-based URL mapping for same-named uploads.
5. Add a related-link picker from sitemap-confirmed `/features/...` URLs with 4 selected by default.
6. Add social link quality controls for clean, competitor/ad, irrelevant, or removed.
7. Add a draft readiness checklist for density, how-to steps, related links, image URLs, social modules, and backup/export.
8. Add a template/clone mode for known good feature page schema.
9. Add a lightweight agent mode alongside manual field editing.
10. Keep publish manual.
