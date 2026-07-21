---
name: article-optimization-collab
description: Use whenever the user is optimizing, refreshing, rewriting, auditing, consolidating, testing, screenshotting, publishing, or correcting an SEO/content workflow. Trigger broadly for Chinese or English requests like "优化这篇", "改这篇文章", "下一篇", "开始优化", "按记忆来", "按之前的方式", "用项目记忆", "降AI感", "加实测", "加内链", "加FAQ", "Meta Description", "元描述", "提升点击率", "处理截图", "WordPress复制", "SEO操作台", "复盘", "GSC我打开了", "Chrome我打开了", "Google Trends", "你自己去测", "自己截图", "以后按这个规则", "记住这个要求", "写进skill", "更新skill", "为什么没按skill", "有的对话不按这个skill", or similar article-work and workflow-correction phrasing. Covers live-source inspection, preservation-first editing, current-model and tracking-link synchronization, official-vs-user data precedence, evidence collection, CTR-focused metadata, internal links, WordPress HTML plus SEO workbench, FAQ/schema, publish QA, immediate correction capture, and project/global skill synchronization.
---

# Article Optimization Collab

## Project Non-Negotiables (Highest Priority)

These are user-approved rules for this project. They override conflicting generic guidance elsewhere in this skill. Apply them automatically so the user does not need to repeat or correct them in later article tasks.

### 1. Read the Real Article Before Deciding Anything

- Open or retrieve the complete live article from the supplied URL before auditing, planning, or writing. Prefer the WordPress REST body when available because it preserves the full publishable source; use the rendered page as a visual cross-check when needed.
- For GLBGPT hub URLs, use the hub route first instead of guessing a main-site REST endpoint. Fetch the rendered article at `https://www.glbgpt.com/hub/<slug>/`, read its `<link rel="alternate" type="application/json">` post id when present, and then use `https://www.glbgpt.com/hub/wp-json/wp/v2/posts/<id>` or the rendered post-content block as the source. If REST by slug is needed, query the hub API path (`/hub/wp-json/wp/v2/posts?slug=<slug>`), not `/wp-json/...` at the root. Use `https://www.glbgpt.com/hub/sitemap.xml` to verify the exact canonical slug and related hub URLs before falling back to broader crawling.
- Never infer the article from its URL, title, topic, sitemap slug, or a partial excerpt.
- Inventory the live H2/H3 structure, paragraphs, tables, images, links, CTA modules, FAQ, schema, meta fields, strong claims, and last-modified date before proposing edits.
- State which live/source article was inspected. If the complete source cannot be read, stop before generating a replacement article and report the limitation.

### 2. Existing Articles Are Preservation-First

- `Optimize`, `refresh`, `add FAQ`, `add links`, and `improve conversion` mean incremental edits to the live/source article, not a clean-room rewrite.
- Preserve the original section order, useful headings, tables, images, examples, buying logic, conversion language, and protected claims. Full rewrites require explicit user approval.
- Aim to keep at least 85% of substantial original paragraphs exactly unchanged in visible wording. Measure and report the final preservation rate.
- Use a `Keep / Insert / Replace` map. Name every substantive replacement and keep official fact corrections to the smallest necessary sentence or table cell.

### 3. Strong Claims and User-Supplied Facts Are Locked

- Apply a field-by-field source hierarchy. When a current official source covers the same factual field and shows that the article's product data is outdated, update that field to the latest official value. Typical time-sensitive fields include official model names, prices, token usage, modes, plan access, quotas, limits, availability, and capabilities.
- When official sources do not publish or address a field that exists in the user's live article or materials, preserve the user's value exactly. Official silence is not evidence that the user's data is wrong and is not permission to delete, soften, qualify, or rewrite it.
- Distinguish same-field contradictions from different product scopes. An official provider's data may update that provider's model or plan facts, but it does not override a separate GlobalGPT-specific price, quota, access, rights, discount, region, or workflow claim unless a current authoritative GlobalGPT source covers that same field differently.
- Anything labeled `Kept Strong Claims` remains locked unless a current authoritative source directly contradicts the same factual field or the user explicitly authorizes changing that exact claim. When an official freshness correction is required, change only the outdated value and preserve the original commercial tone around it.
- Do not delete, weaken, qualify, sanitize, or paraphrase claims merely because they are absent from public official documentation. Separate them as GlobalGPT/platform claims when useful, but preserve their substance and sales force.
- Keep direct language such as `unrestricted access`, `bypass expensive official paywalls`, `no region locks`, `Unlimited pooled quota`, `full commercial usage rights`, `ready for trademarking and distribution`, `no waitlist`, `no hidden caps`, direct prices, discounts, and shutdown claims exactly as approved.
- Never rewrite strong language into corporate softening such as `unrestricted-style`, `pooled quota designed for heavier multi-model use`, `reduces region/account friction`, `subject to the current plan`, `for most users`, or `check before heavy use`.
- Record every official freshness correction in the workbench with old value, new value, official source, checked date, and locations updated. Also record user-supplied fields preserved because no official source covers them.

### 4. Keep the Copy Alive and Conversion-Oriented

- Match the user's direct, human, commercial style. Preserve buying pressure, concrete value comparisons, and phrases such as `smartest way`, `cheaper`, `faster`, `less annoying`, `stop paying separately`, and `without the subscription maze` when they fit.
- Do not flatten the article into sterile corporate prose or remove its sales flavor in the name of trust.
- Trust improvements should come from clear attribution, official links, dates, and precise model naming, not from weakening the user's product language.

### 5. Latest Models, Copy, and Tracking Links Must Match

- Run a latest-model sweep on every optimization, including secondary mentions in the opening, tables, comparisons, CTAs, FAQ, schema, image text, and metadata.
- Verify the latest relevant model from official or primary sources and verify the corresponding GlobalGPT route before using it.
- First-screen/opening model mentions are high-priority conversion copy. Do not replace an outdated model with a vague phrase such as `GPT model access`, `GPT-style models`, or `latest GPT` in the opening, hero, first CTA, first table, or first product paragraph. Use the latest verified available GlobalGPT model route by exact model name, anchor text, URL slug, and tracking parameter.
- If the opening or first-screen product paragraph contains outdated model versions, rewrite that opening paragraph instead of leaving stale model lists in place. Opening model freshness is a hard publish gate: every named model in the first screen must be the newest verified GlobalGPT-available route for that model family, or it must be deliberately removed. Do not preserve old first-screen model names for paragraph-preservation reasons.
- FAQ model freshness is also a hard publish gate. If visible FAQ answers or FAQ JSON-LD mention model names, version numbers, availability, limits, pricing, or GlobalGPT access routes, update them to the newest verified GlobalGPT-available route and current official facts before handoff. Visible FAQ and schema must match after the update; do not leave older model names in FAQ/schema merely because the body was refreshed.
- If the latest official model is newer than the latest verified GlobalGPT product route, do not fabricate the product URL and do not hide the mismatch with generic wording. Use the newest verified GlobalGPT route in the public opening, state the official-vs-GlobalGPT distinction in the workbench, and add a follow-up to recheck the missing route.
- Update model copy, capability wording, anchor text, destination URL/slug, and model-specific tracking/inviter parameters atomically. For example, GPT-5.4 to GPT-5.6 requires the copy, anchor, `.../gpt-5-6` URL, and model-specific tracking identifier to move together.
- Every GlobalGPT model homepage link in public article copy, image links, buttons, tables, FAQ, schema, metadata notes, and the workbench must use the tracked homepage URL format: `/home/<model-slug>?inviter=hub_content_<modelid>&login=1`. For example, use `https://www.glbgpt.com/home/gpt-5-5?inviter=hub_content_gpt55&login=1`, not a bare `/home/gpt-5-5` URL. Preserve existing non-model product/order CTA tracking when it is already intentional.
- Do not fabricate a new product URL. Confirm it through the live route, sitemap, or current GlobalGPT source.
- Search the final body, workbench, meta package, FAQ/schema, and links for stale model names and old URL slugs. Publish QA fails when model text and links disagree.
- Keep an older version only for explicit historical or necessary comparison context, and document the exception.

### 6. Contextual Link Minimum and Two-Part Link System

- Every normal long-form GLBGPT article needs at least 7 unique contextual GLBGPT article links in the public body. This is a floor, not a target. TOC links, images, buttons, navigation, product CTAs, and repeated destinations do not count.
- Part 1 is GLBGPT article links: search the matching sitemap first, verify every URL exists, and select directly relevant access, tutorial, pricing, limits, comparison, commercial-use, prompt, and workflow pages.
- Part 2 is official authority links: connect official documentation, pricing, plan, release-note, policy, or product pages directly to claims about model names, prices, tokens, modes, limits, safety, and availability. These are required external authority citations, not optional extras and not substitutes for GLBGPT internal links.
- Insert links naturally where the reader needs the next answer. Do not use a related-reading dump to satisfy the minimum.
- Do not create dense link clusters in public copy. Aim for at most 1 contextual body link per paragraph, especially in product/model list paragraphs. If an article needs 7+ GLBGPT links, distribute them across relevant paragraphs and sections rather than stacking several blue anchors in one paragraph.
- In the workbench, separate GLBGPT article links from official authority links, report unique counts, and verify complete synchronization with the public body. Internal links are considered done only when the linked anchors appear in `*-body.html`, not merely in the workbench. Official authority links are considered done only when the official source links also appear in `*-body.html` at the relevant factual claims and are listed in the workbench source table.

### 7. High-Intent Purchase Pages Need Strong Conversion Modules

- Treat `Where to buy`, `How to get`, `How to pay`, and `How to access` pages as high-conversion pages.
- Put a clear `Try GlobalGPT now`-style CTA in the first screen without deleting the original opening logic. Repeat conversion CTAs naturally at mid-page and near the conclusion when the article length supports them.
- Add an FAQ question that directly answers whether the model or product can be used on GlobalGPT.
- Add CTR and conversion-rate monitoring to the workbench/publish follow-up for these pages.

### 8. High-Value Page FAQ Standard

- For pages known to earn more than $1,000, or otherwise identified as high-value, the visible FAQ must contain at least 5 complete questions and answers; prefer 8 when the intent supports it.
- Each answer should be complete and normally 60-300 characters, not a one-line fragment.
- Cover the reader's 5W1H needs: what, who, where, when, why, and how, including access, price, limits, use cases, GlobalGPT availability, and decision criteria.
- FAQ visible formatting must use normal article structure by default: each FAQ question should be an `<h3>`-level heading or visually equivalent H3-sized heading, and each answer should be a normal paragraph below it. Do not use `<details><summary>` accordion-style FAQ unless the user explicitly asks for collapsible FAQ.
- Visible FAQ and FAQ JSON-LD must match exactly in question order and answer text. FAQ/schema mismatch fails publish QA.

### 9. Topic Priority Is Determined by the Target URL

- Do not maintain a permanently preferred model or topic cluster. Nano Banana is not a default priority unless the target URL, its search intent, or its surrounding content cluster makes it the current focus.
- Determine the priority topic from the target URL, live article title/body, primary query intent, existing rankings when available, and the closest sitemap/content cluster.
- Apply freshness checks to the products and models actually present in that URL. Verify relevant official pricing, token/image-output usage, modes, plan access, model/API names, quotas, limits, and availability; do not force unrelated Nano Banana research into another topic.
- Proactively identify comparison, tutorial, pricing, access, prompt, limits, commercial-use, and workflow long-tail opportunities for the URL's actual topic cluster. Add them to the workbench/editorial follow-up and create them when article creation is in scope.
- Deepen the natural GlobalGPT connection through contextual product use, relevant GLBGPT articles, and conversion CTAs that match the target URL rather than a predetermined model campaign.

### 9.5. Sora 2 Articles Must Start With Current Status and Matching FAQ

- For every Sora 2-related model/article, place a current Sora 2 status module at the very beginning before the normal introduction, quick answer, or sales copy.
- Verify official OpenAI sources at article time and state what OpenAI says now: whether Sora 2, Sora web/app, or Sora API is live, limited, discontinued, or scheduled to shut down.
- If OpenAI publishes shutdown dates, deprecation dates, region/plan limits, API-only status, or consumer-app changes, include concrete dates, scope, and the checked date in the opening module.
- Separate official consumer web/app, official OpenAI API, and GlobalGPT platform access. These routes can have different availability, prices, duration limits, watermark behavior, and setup friction.
- The visible FAQ must include at least one matching current-status Q&A whenever the article is about Sora 2, Sora 2 Pro, Sora 2 alternatives, Sora 2 access, Sora 2 prompts, Sora 2 commercial use, Sora 2 restrictions, or any model/workflow materially connected to Sora 2.
- The required FAQ should directly answer a status question such as `Is Sora 2 still available?`, `Did OpenAI say when Sora 2 shuts down?`, `Can I still use Sora 2 Pro after the official app change?`, or `What is the difference between official API access and GlobalGPT access?`
- If FAQ JSON-LD is present, include the same Sora 2 status FAQ there with identical question order and answer text. FAQ/schema mismatch fails publish QA.
- Do not reuse a prior Sora 2 status from memory as current fact. Browse or use official OpenAI documentation sources again for each Sora 2 article.
- If official pages are blocked to automated fetch, cite the verified official URL in the body/workbench and add a manual-check note. Do not guess or hide the uncertainty.
- Official OpenAI status updates do not automatically override GlobalGPT-specific claims such as price, quota, invite-code requirements, watermark-free exports, or platform clip duration unless a current GlobalGPT source changes the same field.

### 10. Required Handoff and Publish QA

- Deliver two clearly separated artifacts for full article packages: `*-body.html` and `*-seo-workbench.html`.
- `*-body.html` is the modified blog article itself. It must be directly copyable into WordPress and preserve paragraph, heading, table, image, CTA, and link formatting. It should contain the public article body only, not editor instructions, insertion notes, internal-link tables, QA notes, or backend explanations.
- `*-seo-workbench.html` is the editor/SEO operation console. It should contain explanations and support material such as the Keep/Insert/Replace map, TOC/HTML anchor map, internal-link table, official sources, HTML image/module code, image alt/caption/source notes, Model and Link Freshness table, protected claims, FAQ/schema status, meta package, and publish checks.
- The workbench must include practical copyable source boxes, not only rendered previews or file-open instructions. Embed the full body HTML source directly in a textarea with a copy button so it works from a local file; do not depend on `fetch()` to load the body file because browser file restrictions can block it. When HTML visual modules are added, include separate copyable textarea blocks for each module.
- HTML visual modules should be chart-first instead of paragraph-card-first. Prefer radar charts, risk matrices, score rings, flow diagrams, coordinate maps, comparison charts, and other visual structures with short labels, numbers, and sparse captions. Avoid stuffing long explanations into the image; the body copy should carry the detailed prose.
- HTML visuals are additive explanatory figures. Use them to add visual content and scanning value, not to convert ordinary article paragraphs into HTML modules. The public article must still read like a normal WordPress blog with copyable headings, paragraphs, lists, tables, links, figures, FAQ, and schema.
- All contextual internal links promised in the workbench must also appear naturally in `*-body.html`. Do not list links only in the workbench and call the article optimized. Before handoff, count unique GLBGPT body links and verify every workbench link table entry is synchronized with the public body.
- All official authority links promised in the workbench must also appear naturally in `*-body.html` at the claim they support. Do not keep official sources only as editor notes. Before handoff, verify that dynamic claims about model names, pricing, plan access, token usage, modes, limits, safety, availability, policies, release dates, or commercial rights have current official or primary-source links where available.
- Meta package limits are hard: SEO title must be no more than 60 characters; meta description must be no more than 160 characters. Count and record both before handoff.
- Treat Meta Description as CTR-focused SERP sales copy, not a plain article introduction or table-of-contents summary. It must combine search intent, a concrete outcome, a differentiator/proof point, and a click-driving action while staying accurate.
- Read `references/meta-description-ctr-rules.md` whenever creating or revising a meta package; generate three meaningfully different options, label character counts and emotional/CTR hooks, and select a recommended winner.
- Public copy must not contain editor/backend language. The workbench must include the Keep/Insert/Replace map, internal-link tables, official sources, Model and Link Freshness table, protected claims, FAQ/schema status, image inventory, and publish checks.
- Before handoff, verify: source preservation, H2 order, table/image retention, latest models, tracking links, sitemap targets, official sources, CTA placement, FAQ length/count, schema parity, TOC anchors, and absence of softened protected claims.
- Do not call the article complete when any required check fails or when the deliverable is only a summary instead of copy-ready HTML.

### 11. User-Corrected Article Package Defaults

These defaults come from repeated user corrections and must be applied automatically in future optimization tasks:

- Treat `body` as the user's WordPress copy source. The user should be able to copy from `*-body.html` or the workbench's full-body source textarea and paste into WordPress without losing headings, paragraphs, links, CTA buttons, tables, images/HTML visuals, FAQ, or JSON-LD.
- When the user asks for HTML for an existing article, including a narrow task such as adding internal links, return a complete `*-body.html` article body by default. Do not deliver only isolated paragraph snippets unless the user explicitly asks for snippets only.
- Treat the workbench as a Chinese editor console only: explain the TOC/HTML anchor map, internal-link table, HTML visual code, image alt/caption/source notes, meta package, sources, and QA. Do not make the workbench the only readable version of the article.
- When the user asks to add HTML images, add polished explanatory visual figures to the article. Do not replace the whole article with HTML blocks, do not turn all body content into a workbench, and do not produce black-white text/table modules as "images."
- HTML images should usually be sparse, visual, and chart-like: radar charts, risk matrices, scoring rings, gate/flow diagrams, coordinate maps, model-comparison charts, and visual stacks. Keep text inside the figure to short labels, numbers, and brief captions.
- Preserve the user's commercial and marketing flavor. Do not soften direct conversion language unless a current authoritative source directly contradicts a factual field.
- Do not hard-code Sora, Veo, Nano Banana, or any other product as the default topic. The maintenance/expansion strategy must be determined from the current target URL, live article, search intent, revenue/value notes, and surrounding sitemap cluster. If the current topic is a maintenance topic, refresh existing pages and add relevant alternatives; if it is an expansion topic, build the appropriate internal-link and content plan around that topic.
- For high-value pages, add or improve a visible FAQ module with at least 5 complete Q&As, preferably more when the intent supports it. Answers should normally be 60-300 characters, cover 5W1H intent, and match FAQ JSON-LD exactly. Write each language version independently instead of directly translating the English FAQ.
- For GLBGPT hub articles, get the source through the hub path first: rendered `/hub/<slug>/`, alternate JSON post id, then `/hub/wp-json/wp/v2/posts/<id>` or rendered post-content. Use the hub sitemap to verify canonical and related URLs. Do not waste cycles trying root `/wp-json/...` first.

## First Move

Load project memory before acting when available:

1. Read `memory/hot-cache.md` in the current workspace.
2. Read `memory/article-optimization-collaboration.md` for detailed preferences.
3. If these files are missing, continue with this skill and create/update them after the article cycle.

Do not force a rigid brief. If the user provides only a target article, attachment, URL, or says a short phrase like "优化这篇", infer the workflow from the article type and ask only for truly blocking details.

Short user phrases that should be enough to start:

- "优化这篇"
- "开始下一篇"
- "按记忆来"
- "按之前的方式"
- "这篇降AI感"
- "这篇加实测"
- "这篇加内链"
- "帮我做发布前检查"
- "复盘并更新记忆"

## Working Style

Treat each article as its own case. First decide the article role:

- Refresh an existing ranking page.
- Consolidate and replace older pages.
- Add real hands-on experience.
- Improve readability and reduce AI-sounding language.
- Insert internal links and product mentions naturally.
- Update facts, models, prices, or screenshots.
- Prepare WordPress-ready copy and image assets.

When giving manual editing instructions, use `Ctrl+F` search phrases plus "keep / replace / insert / delete / move". Avoid line numbers.

## Existing Article Preservation Rule

When the user asks to optimize, refresh, add links, add FAQ, improve conversion, or update an existing article, default to an incremental edit of the live/source article. Do not produce a clean-room replacement article unless the user explicitly approves a full rewrite.

- Use the live WordPress body or supplied source as the baseline, not a newly drafted outline.
- Preserve the existing H2 order, useful H3s, tables, images, examples, buying logic, sales language, and protected claims unless a specific item must change.
- Add CTAs, internal links, official citations, TOC anchors, FAQ entries, schema, and short update notes inside or around the original copy.
- When an official fact is wrong, change only the smallest sentence or table cell needed and list that substantive correction in the workbench.
- Before handoff, compare source and delivery. Report original vs new H2, table, and image counts, heading-order preservation, and the exact visible-text preservation rate for substantial original paragraphs.
- For a preservation refresh, aim to keep at least 85% of substantial original paragraphs exactly unchanged in visible wording. If the task genuinely requires more rewriting, stop and get explicit approval before crossing that boundary.
- The workbench must include a `Keep / Insert / Replace` map. Every substantive replacement must be named; do not hide a rewrite behind an optimization summary.

## Latest Model and Tracking Link Synchronization

Every article optimization must include a current-model sweep before copy generation, even when the article's main topic is not a model comparison. Model freshness applies to secondary recommendations and conversion mentions too.

- Inventory every named model and version in the title/meta package, headings, body copy, lists, tables, comparison modules, CTA text, FAQ, FAQ/Article schema, image alt/captions, anchor text, destination URLs, URL slugs, and tracking parameters.
- Verify the latest relevant model through current official or primary sources, then verify that the corresponding GlobalGPT product/article route exists. Use the latest model that is actually relevant and available for the workflow, not an invented or assumed successor URL.
- Treat a model update as one atomic change: update the visible model name, surrounding capability wording when necessary, anchor text, destination path/slug, and model-specific tracking or inviter parameter together.
- Never update copy from an older model to a newer model while leaving the anchor or tracking link pointed at the old model. For example, when a secondary mention moves from GPT-5.4 to GPT-5.6, the visible copy, linked anchor, product URL such as `.../gpt-5-6`, and any model-specific tracking identifier must all move to GPT-5.6 together.
- Convert every GlobalGPT model homepage URL to the tracked format `/home/<model-slug>?inviter=hub_content_<modelid>&login=1` everywhere it appears in the article package, including text links, image links, buttons, comparison tables, FAQ/schema, metadata notes, and workbench link tables. Bare model homepage links such as `/home/claude-opus-4-8` fail QA even when the route itself works.
- Search the final body and workbench for stale model-version strings and stale URL slugs after replacements. A version is complete only when old copy/link pairs are gone everywhere except deliberate historical or comparison references.
- Do not blindly replace a historically meaningful version. Keep an older model only when the sentence is explicitly historical, the comparison requires it, or the latest model is not available on the linked platform; state that exception in the workbench.
- Include a `Model and Link Freshness` table in the workbench with: old model, current model, evidence/source, old URL, new verified URL, tracking-parameter change, locations updated, and status.
- Publish QA must fail if model text, anchor text, destination URL, schema, or tracking parameters disagree with one another.

## Active Evidence Workflow

When the user explicitly says GSC, Google Trends, Chrome, benchmark pages, official pages, or testing pages are already open and asks you to look, test, screenshot, or handle them yourself, treat that as authorization to actively gather evidence in the opened browser surfaces.

Use the detailed workflow in `references/active-evidence-workflow.md` when a task includes any of these:

- GSC or Google Trends as optimization evidence.
- User-opened Chrome pages for analysis or screenshots.
- Official model/pricing/benchmark/release-note proof screenshots.
- Hands-on model testing with prompts and screenshots.
- Screenshot matrix execution, image processing, and final HTML packaging.

Browser evidence rules:

- Use GSC to decide URL retention, consolidation, redirect/canonical direction, query coverage, CTR fixes, and FAQ/H2 opportunities.
- Use Google Trends to support trend, title-year, region, related-topic, rising-query, and angle decisions when those signals matter.
- Use official or primary sources for dynamic facts: model versions, pricing, plan access, availability, release notes, benchmarks, policies, and product features.
- Do not inspect cookies, local storage, passwords, session stores, or unrelated private account areas.
- Keep GSC/Trends labels and internal URL labels out of public copy. Use them in plans, SEO workbenches, and editor notes only.

## Mandatory SEO Routing, Not Mandatory Full Execution

Always run an SEO routing check at the start of article-optimization work. This check is mandatory; full SEO specialist execution is not mandatory for every small task.

Apply the base optimization SEO skills only when the task affects article strategy, rankings, refresh direction, or publishable SEO structure: full article audit, optimization plan, decay/traffic refresh, SERP repositioning, full rewrite package, internal-link refresh, meta/schema work, publish QA, or GSC/rank diagnosis.

Base optimization SEO skills for those phases:

- `content-refresher` for existing-article decay, freshness, republishing, and update-priority logic.
- `on-page-seo-auditor` for title/meta/header/keyword/link/image/on-page checks.
- `content-quality-auditor` for E-E-A-T, usefulness, trust, and publish-readiness checks.

Skip full SEO specialist execution for local or operational tasks that do not change SEO strategy: rewriting one paragraph, reducing AI tone in a small passage, processing screenshots, writing alt text, packaging/share zips, adding TOC anchors, changing a title in an already-approved package, or fixing a small WordPress formatting issue. Still follow article-optimization memory and say that full SEO routing was skipped because the task is local.

Add specialist SEO skills when relevant:

| Need | Required specialist skill |
|---|---|
| Keyword/topic repositioning | `keyword-research` |
| Current SERP, intent shift, SERP features, snippets | `serp-analysis` |
| Competitor coverage or missing sections | `competitor-analysis` or `content-gap-analysis` |
| Internal-link refresh, anchors, orphan/crawl flow | `internal-linking-optimizer` |
| Meta title/description/OG refresh | `meta-tags-optimizer` |
| FAQ/HowTo/Article/Product JSON-LD | `schema-markup-generator` |
| AI search / AI Overview / ChatGPT / Perplexity citation readiness | `geo-content-optimizer` |
| Technical/indexing/canonical/redirect/CWV/sitemap issues | `technical-seo-checker` |
| Rank/GSC/performance diagnosis | `rank-tracker` or `performance-reporter` |
| Backlink or off-page trust issues | `backlink-analyzer` |
| Domain/source trust or citation credibility | `domain-authority-auditor` |
| Entity / Knowledge Graph / sameAs improvements | `entity-optimizer` |
| Net-new replacement sections | `seo-content-writer` |

In the optimization plan or work note, state the routing result: which SEO specialist skills were applied, which were skipped, and why. If a specialist skill is unavailable, say so briefly and continue with the closest available SEO check.

## Default Workflow

1. **Diagnose**: Identify search intent, current article role, major content gaps, AI-sounding language, backend-language leakage, outdated claims, weak tables, and missing trust signals.
2. **Propose Before Executing**: Give the user an optimization plan after analyzing the article and request. State what memory was loaded, what standards will be applied, what sections or assets will be touched, and what needs confirmation.
3. **Wait for Confirmation**: Do not begin substantive rewriting, screenshot processing, WordPress HTML generation, or large edits until the user confirms the plan. If the user explicitly says "直接改", "不用确认", or asks for a tiny isolated task, proceed.
4. **Map Edits**: Provide a clear modification map before rewriting large sections. Separate public copy from editor notes.
5. **Write or Rewrite**: Produce natural reviewer-style copy with concrete observations, not generic model praise.
6. **Plan Evidence**: Decide which claims need hands-on tests, official docs, benchmark data, screenshots, or custom HTML proof cards.
7. **Package for WordPress**: Provide copy-ready HTML when useful, with English public article content in correct H2/H3/paragraph/list/table/link markup and Chinese editor markers kept separate from publishable copy. Also provide separate image names, alt text, captions, and insertion locations.
8. **Internal Links**: Insert anchors only where they read naturally. Also provide a copy table: URL, plain anchor, linked anchor.
9. **Publish QA**: Check for AI tone, backend notes, table breakage, dynamic facts, image alt text, product-claim boundaries, FAQ quality, and WordPress formatting.
10. **Retro and Memory**: After finishing an article, summarize friction, new user preferences, reusable patterns, and update project memory.

## Phase Gate

Do not collapse all article work into one execution. Identify the current phase and stop at that phase.

1. **Phase 1: Audit and Plan**  
   Use when the user asks to review a page, judge whether proposed changes are reasonable, check GSC, check Google Trends, assess SEO logic, or "给我说说计划". Output: loaded memory, article diagnosis, GSC/current-status findings when requested, Google Trends signals when relevant, SEO rationale, proposed section changes, test/screenshot suggestions, evidence plan, delivery format proposal, and the next-step confirmation question. Do not create final article copy as the main deliverable.
2. **Phase 2: Test and Screenshot Matrix**  
   Use after the plan is accepted or when the user asks for real tests/screenshots. Output: test dimensions designed from search intent and model/product characteristics, where to test, prompts, official URLs to capture, filenames, alt text, captions, insertion points, priority, and status. Do not claim screenshots exist until the user provides them or explicitly asks the agent to capture/process them.
3. **Phase 3: Image Processing**  
   Use after screenshots are provided or captured. Output: processed WebP files, names, dimensions/crop notes, folder path, and image insertion map. Tool capability checks such as WebP converter probing are internal; do not present them as a major user-facing progress update unless they block the task.
4. **Phase 4: Article Copy Package**  
   Use after the content direction and evidence plan are confirmed. Output: WordPress-copyable HTML or section-level HTML replacement blocks with Chinese editor markers, internal-link table, FAQ, source notes, and image placeholders.
5. **Phase 5: Publish QA and Retro**  
   Use after the copy package exists. Output: final QA, missing assets, publication checklist, and memory updates.

If the user says "可以开始" after a Phase 1 plan, execute the next confirmed phase, not every remaining phase. If the intended phase is ambiguous, ask a short clarification instead of jumping to a final optimization pack.

## Confirmation Gate

For article optimization requests, answer first with a concise plan before doing the work. Include:

- **Loaded memory**: Which project memory files or prior decisions were used.
- **Article diagnosis**: The article role and likely biggest problems.
- **Optimization route**: For example readability refresh, real-test expansion, internal linking, consolidation, pricing update, FAQ packaging, or anti-AI-language pass.
- **Planned edits**: Which sections, tables, images, links, or screenshots will be changed.
- **Evidence plan**: Whether browsing, official docs, benchmark data, hands-on tests, or user screenshots are needed.
- **Delivery format**: The exact final artifact format, such as WordPress-copyable HTML, HTML preview file, screenshot matrix, image folder, internal-link table, or markdown summary.
- **Completion criteria**: What must exist before claiming the task is done.
- **What I need from you**: Only truly blocking inputs.
- **Awaiting confirmation**: End by asking the user to confirm before execution.

Keep this plan practical and short. Do not turn it into a rigid intake form.

## Opening and Trust Refresh Rules

When optimizing an existing article whose opening has access doubts, official-vs-third-party confusion, pricing anxiety, safety concerns, or "is this real?" trust friction, consider rewriting the intro with PAS rather than a generic summary.

- **Problem**: Answer the user's real question immediately.
- **Agitate**: Acknowledge the reasonable doubt or friction without sounding alarmist.
- **Solution**: Explain the credible route, product fit, or updated workflow.

For "official route unavailable but a platform route works" updates, explain the difference briefly and concretely. Avoid "bypass" framing. Distinguish consumer app/site access from API-powered platform access, name verified infrastructure when relevant, and keep availability limits bounded by region, quota, safety filters, model lifecycle, or account support.

## Delivery Contract

Do not silently downgrade the final deliverable.

- If the user needs to paste content into WordPress, the primary deliverable is WordPress-copyable HTML or clearly marked HTML replacement blocks, not a markdown optimization pack.
- If the user asks for "full article HTML", "pure article HTML", "全文 HTML", "完整 HTML", or a direct WordPress replacement article, the primary deliverable must be one continuous publishable article, not an editor workbench, screenshot/image pack, or planning matrix. Workbenches and image maps may be auxiliary, but they do not satisfy the full-article HTML contract.
- A complete full-article HTML package must include, by default: the full public body, real `<figure><img><figcaption>` placements, a TOC for long articles, H2 `id` anchors, a separate anchor mapping table, FAQ content plus FAQ JSON-LD when FAQ is included, meta title/description/OG suggestions, image filenames/alt/captions, natural internal links, and any CSS needed for special modules such as TOC or Quick Answer boxes.
- Do not make the user ask separately for TOC anchors, WordPress CSS, Quick Answer styling, schema, or meta tags when those elements belong to the promised HTML package.
- A markdown pack can be used as an auxiliary planning/archive artifact, but it is not the final deliverable unless the user explicitly asks for markdown.
- If the plan promises "可直接替换进文章", "可直接插入", "WordPress复制", or similar wording, the execution must produce the copy-ready article content or replacement modules in HTML.
- If the work includes evidence, tests, screenshots, benchmark proof, or official proof, include the screenshot/evidence matrix as a first-class deliverable before claiming completion.
- If the work includes active browser evidence collection, complete the loop: evidence plan, executed captures/tests when authorized, processed image assets, image matrix, article HTML, SEO workbench, and final QA.
- The final response must state which artifacts were created and whether they satisfy the delivery contract.
- Do not say "done" merely because a summary file exists. Use a completion checklist against the confirmed plan.
- If required screenshots are only planned but not captured, say "planned, not captured" and do not present that part as complete.
- If the current phase is only audit/plan, do not create a final optimization pack and do not describe tests/screenshots as completed.
- For full evidence-backed article refreshes, produce the expected three-artifact package unless the user asks for a narrower output: `*-body.html` pure publishable article, `*-seo-workbench.html` editor/SEO operation console, and image asset index.

## Output Packaging Rules

When the user needs to manually copy optimized content into WordPress, prefer a practical output package instead of plain markdown:

- Public article content should be in the article's target language, usually English.
- Use real HTML structure for publishable content: `<h2>`, `<h3>`, `<p>`, `<ul>`, `<ol>`, `<table>`, and `<a>`.
- Add Chinese editor markers only as guidance for the user, not as public article copy. Examples: "插入位置", "图片文件名", "alt 文本", "新增段落放在...", "替换这一段".
- If creating an HTML preview file, make copy zones obvious and keep Chinese notes visually distinct from English publishable content.
- When creating a full article optimization handoff, prefer a browser-friendly copy workbench: yellow Chinese editor notes, white copy/replacement boxes, SEO/source notes, image cards, internal-link table, and publish QA helpers. For existing articles, include what to keep, replace, move, delete, or insert.
- For partial edits, give `Ctrl+F` anchors plus the replacement HTML block.
- For image-heavy sections, pair each image with filename, alt text, insertion point, and the paragraph it supports.
- For internal links, provide both the linked HTML in context and a separate copy table.
- For long optimized articles, include a WordPress TOC/anchor module when useful: a copyable directory, each H2's `HTML anchor` value, and matching `#anchor` links. Remind that the heading block's HTML anchor omits `#`, while TOC links include `#`.
- For full/pure article HTML, include the TOC inside the public article body and add H2 `id` attributes directly in the HTML. Also provide a separate editor-facing anchor map so the user can recreate Gutenberg heading anchors if needed.
- For Quick Answer, TOC, callout, or comparison modules, provide WordPress-usable CSS in the right format:
  - Global/custom CSS may use selectors such as `.quick-answer-box { ... }`.
  - Gutenberg block "额外 CSS" fields need declaration-only snippets such as `border: 1px solid #...; padding: ...;`, not selector blocks.
  - If a WordPress field cannot style child elements, provide an inline-style fallback inside the HTML.
- Before final handoff, verify every TOC `href="#..."` matches an existing H2 `id="..."`, every anchor mapping omits `#` in the heading value, and every TOC link includes `#`.
- Before final handoff, verify the meta package, FAQ/schema package, image alt/caption list, internal-link table, and required CSS guidance are present or explicitly marked not needed.
- Before final handoff, check that headings, bullet lists, tables, and links will not collapse into one plain WordPress block.
- Before final handoff for pure article HTML, verify image paths exist, FAQ schema matches visible FAQ when included, body links are synced with the internal-link table, and public copy contains no editor/backend language such as `GSC`, `URL A`, `URL B`, `screenshot matrix`, `placeholder`, `proof image`, `image insertion`, or `alt text`.
- If making a full article optimization pack, create a primary HTML copy file or section-level HTML blocks first. Use markdown only for notes, audit summaries, or backup.

## Immediate Conversation-to-Skill Learning

Treat explicit user corrections as same-turn skill updates, not notes to postpone until the article cycle ends:

- When the user says a rule should apply later, says another conversation failed to follow the workflow, or corrects a reusable article standard, update this project-local `SKILL.md` in that same turn after understanding the final instruction.
- Do not wait for the same correction to occur twice. A clear durable instruction such as `以后都这样`, `写进skill`, `保证不用再改`, or `有的对话没按skill` is sufficient.
- Edit or remove superseded wording instead of appending a contradictory rule. The newest explicit user correction wins; verify the final skill has one coherent rule for the topic.
- Update `memory/hot-cache.md`, `memory/article-optimization-collaboration.md`, and `memory/decisions.md` when the correction is durable. Keep one-off article details out of the global defaults.
- Treat the project-local skill as canonical. When the same skill is installed globally, validate the project copy and synchronize the global copy so other conversations do not load a stale version.
- Verify the active project/global skill paths, frontmatter triggers, file hashes, and validation result after synchronization. Report what changed and whether article outputs were intentionally left untouched.
- If the user only asks to improve the skill, do not regenerate or modify article deliverables.

## Voice and Copy Rules

Write like a sincere reviewer who tested the tools:

- Prefer "In the test..." and "In the picture..." over "In the screenshot...".
- Explain observed differences, workflow implications, and who should choose what.
- Do not write "this screenshot is important/useful" or meta explanations about why the evidence matters.
- Do not use backend/editor language in public copy: `placeholder`, `proof image`, `image insertion`, `alt text`, `URL B`, `A/C redirect`, `GSC says`, `rewrite pack`, `line 284`.
- Avoid stiff AI/backstage phrases such as `currently shows`, `the benchmark data points in the same direction`, `it is important to note`, `should be checked from current official sources`, `For readers`, `This guide explains`, `in this article`, and process-exposing language.
- Prefer user-facing phrasing such as "For users", "The simple point is", "The practical route is", "If you are trying to...", and "That means..."
- Avoid over-formal disclaimers unless they protect trust around pricing, privacy, or availability.
- Use tables and bullets to improve readability, but do not convert every paragraph.
- Check WordPress preview risk when plain text shows table content glued together.

## Hands-On Test Rules

Hands-on tests must compare actual behavior on a useful task. Do not use model answers as "proof" for external facts.

Before planning tests, decide the right testing venue:

- Use GlobalGPT when the article is comparing everyday language-model behavior available inside GlobalGPT, such as writing, coding output, research synthesis, structured reasoning, strategy, and messy-note cleanup.
- Use official products or official docs when the claim is about exclusive product features, account access, Codex, Grok Build, native API consoles, pricing pages, privacy settings, or capabilities GlobalGPT does not provide.
- When the user says the models should be the latest, verify or ask which current model versions to test before creating the screenshot matrix.
- In hands-on sections, state where the test was run and why that venue fits the task.
- If the user has not provided screenshots and has not authorized you to run/capture tests, produce test suggestions and a screenshot matrix only. Do not write final "hands-on test results" as if the evidence already exists.
- Before running tests that may use credits, logged-in sessions, or paid model access, state the intended prompts and wait for confirmation unless the user already told you to run them.

Design the test matrix from the article, not from a fixed template. Cover:

- **Baseline capability**: correctness, instruction following, output usability, reasoning/explanation quality, and verification awareness.
- **Model or product strengths**: for example long context, agentic coding, web search, multimodal work, UI generation, speed, low cost, safety review, tool use, or other capabilities the model/product claims or the search intent emphasizes.
- **Search demand**: GSC queries, Google Trends related/rising queries, user questions, competitor coverage, and SERP-intent gaps.

For coding articles, debugging, refactoring, multi-file reasoning, unit tests, and security review are useful candidate dimensions, not a mandatory template. Test the dimensions needed to answer the article's real search intent and model-specific claims. Do not add irrelevant tests just to fill a fixed count.

For each test section, define:

- The user task being simulated.
- Where it was tested: official product, GlobalGPT, or both.
- The exact prompt when useful.
- What each model did differently.
- What the difference means for a real user.
- The screenshot pair or comparison image.
- Optional supporting benchmark or official-doc evidence.

Good dimensions may include writing/editing, coding output, research synthesis, structured analysis, strategic decisions, messy-note cleanup, real-time information, multimodal work, pricing/access, developer workflow, or other capabilities that the model, product, query set, or article type makes relevant.

Do not put FAQ, final verdict, misconceptions, or other editorial sections into a screenshot matrix unless the user is actually capturing UI evidence for them. Those belong in the article copy.

Use benchmark data directly in tables or plain explanation. Do not over-explain benchmark relevance. If benchmark proof screenshots are needed, reserve named slots with filename, alt text, source URL, and capture area.

For real-test article sections, prefer a complete H2/H3 structure with image plus text for each comparison dimension. Avoid placing screenshots after unrelated short answers.

## Product Placement Boundaries

GlobalGPT can be recommended as a practical multi-model workspace when the article supports that use case.

Safe GlobalGPT positioning:

- Helpful for comparing GPT-style and Grok-style outputs side by side.
- Useful for everyday writing, research, planning, summarizing, and multi-model chat.
- Can be framed around affordability and reduced tab switching when supported by current pricing.

Do not claim GlobalGPT replaces:

- Codex, repository editing, IDE/CLI workflows, code review, or cloud coding tasks.
- Grok Build, direct xAI API billing, official API consoles, or native builder controls.
- Every official app feature, enterprise control, or account-specific capability.

When product placement feels promotional, reduce it to one concrete workflow benefit.

## Internal Linking Rules

Match links to the section where the reader naturally needs the next step. Avoid link dumps.

If project memory includes a saved sitemap/article catalog, use it before crawling again. For GLBGPT hub articles, use `memory/research/glbgpt-hub-sitemap-articles.md` when available. Treat slug-derived titles as candidates only; verify target relevance when the surrounding claim depends on current facts or exact page content.

Every optimized article must contain at least 7 contextual body links, excluding TOC anchors, image links, buttons, and repeated CTA URLs. Treat 7 as the floor, not the target: longer or commercially important articles should normally carry more when the links are genuinely useful.

Avoid link stacking: public copy should normally have no more than 1 contextual link in the same paragraph. Do not turn model/product list paragraphs into long runs of linked model names. When the link floor requires multiple targets, spread them across separate relevant paragraphs instead of clustering them together.

Build the link set in two distinct parts:

1. **GLBGPT article links**: Search the matching GLBGPT sitemap first, especially `https://www.glbgpt.com/hub/sitemap.xml` for hub articles. Select closely related tutorials, comparisons, pricing guides, access guides, limits pages, commercial-use pages, and workflow follow-ups. Verify that every selected URL exists in the sitemap and place it in the paragraph where the reader naturally needs that next answer.
2. **Official authority links**: Link official documentation, pricing, plan, release-note, policy, or product pages directly from factual claims such as model/API names, pricing, token usage, plan access, modes, limits, safety, and availability. These are authority citations, not substitutes for GLBGPT article links.

For a normal long-form GLBGPT article, aim for at least 7 unique GLBGPT article links plus the official authority links needed to support dynamic facts. Product-page links and conversion CTAs are useful but do not count toward the GLBGPT article-link minimum. Do not satisfy the rule with repeated destinations, navigation links, a related-reading dump, or links that are only loosely relevant.

When optimizing existing articles, preserve strong existing links, replace broken or irrelevant links, and substantially expand the contextual link network when relevant sitemap targets exist. Anchor text must read naturally in the revised sentence, describe the destination accurately, and vary across the article.

Always provide:

| URL | Plain anchor | Linked anchor |
|---|---|---|

In the workbench, separate GLBGPT article links from official authority links and report the unique count for each group. Before final handoff, verify that every listed link appears in the public body and that every public-body contextual link appears in the link table.

Use anchors that sound like normal article text. Do not force exact-match anchors when a softer phrase reads better.

## Protected Strong Claims

When a user marks copy or a workbench section as `Kept Strong Claims`, treat those claims as locked user-approved language.

- Do not delete, soften, qualify, paraphrase, or replace a protected claim unless the user explicitly asks to change that exact claim.
- Do not turn direct commercial language such as `unrestricted access`, `bypass expensive official paywalls`, `no region locks`, `Unlimited pooled quota`, `full commercial usage rights`, `ready for trademarking and distribution`, `no waitlist`, or `no hidden caps` into cautious corporate language.
- Do not append weakening tails such as `-style`, `for most users`, `subject to the current plan`, `reduces friction`, `designed for heavier use`, or `check before heavy use` to a protected claim.
- If a current official source covers the same factual field and proves the existing value is outdated, update only that field and cite the source. If official sources do not cover the field, facts supplied in the user's article or product materials remain intact; keep them clearly framed as GlobalGPT/platform claims when needed, but do not rewrite their substance.
- Official-source facts and protected GlobalGPT claims may sit side by side. Official links support official facts; lack of an official source is not permission to alter a protected platform claim.
- In the SEO workbench, quote protected claims exactly and mark them `Kept unchanged`; never describe a softened rewrite as having been kept.

## Image and Screenshot Rules

For screenshot work:

- Create descriptive, short filenames.
- Convert to WebP when requested.
- Use WebP lossless for text-heavy screenshots when image clarity matters.
- Use 16:9 cropping only when requested or when consistency matters.
- Keep hands-on output screenshots separate from official proof/documentation screenshots.
- Provide image alt text and insertion location outside the public paragraph.
- Keep technical conversion checks quiet. If `sips`, Pillow, ImageMagick, or another converter must be probed, run the check internally, fall back automatically when possible, and report only the outcome: processed files, folder path, dimensions/crop status, and failures.
- When official screenshots are needed, give the URL and exact area to capture, preferably in the same order the images will appear in the article.
- Official/evidence screenshot plans must include URL, page/source title, Command+F locator text, exact area to capture, claim supported, filename, alt text, caption, and insertion point. A URL alone is not enough.
- Screenshot matrices should track status: planned, captured, processed, inserted, or skipped with reason.
- After processing screenshots, create or update an image asset index for evidence-heavy articles. Include filename, dimensions, type, source, alt text, caption, insertion point, and required/optional status.
- Before using processed images in article HTML, verify referenced files exist locally.
- If creating an HTML data card or proof card, remove generation notes, implementation hints, placeholder labels, or tiny meta text that could expose the artifact as internal work.

## Fact and Pricing Rules

Browse or verify for current model names, prices, benchmarks, product availability, policy, privacy, or plans. Treat these as dynamic.

Use field-level source precedence:

1. If a current official source covers the same field and differs from the article because the article is stale, update the field to the latest official value and cite the source/date.
2. If the official source does not mention the field, preserve the user-supplied value and wording. Do not soften it merely because it cannot be independently found.
3. Do not use one provider's official page to overwrite a different GlobalGPT-specific field. Compare like with like: official Google plan data to Google plan claims, and current GlobalGPT data to GlobalGPT plan claims.
4. If two current authoritative sources directly conflict on the same field and the correct value cannot be resolved, surface the conflict in the workbench and ask only if it blocks publication.

For pricing sections, prefer concrete tables over vague paragraphs. Separate consumer subscription pricing, API pricing, and GlobalGPT pricing when all three are relevant. Avoid stiff phrases like "currently shows"; use natural dated wording or direct table labels.

Avoid unexplained internal labels such as "final decision matrix". Use plain reader-facing names like "comparison table", "choice guide", or "which one should you choose".

## Memory Update Protocol

At the end of each article cycle:

1. Create or update `memory/content/YYYY-MM-DD-<article-slug>-retro.md`.
2. Update `memory/article-optimization-collaboration.md` with new stable preferences, repeated friction, and reusable decisions.
3. Keep `memory/hot-cache.md` concise, under 80 lines, with only active defaults and current project priorities.
4. Put unresolved follow-ups in `memory/open-loops.md`.
5. Put durable user-approved workflow decisions in `memory/decisions.md` with `approved_by: user`.
6. If a correction reveals a reusable workflow failure, promote the lesson into the main collaboration memory and hot cache when appropriate, not only into an article-specific retro.

Do not store private analytics screenshots, credentials, or sensitive data unless the user explicitly asks.
