# Active Evidence Workflow

Use this reference when the user authorizes active evidence collection for an article optimization task: GSC is open, Google Trends is open, Chrome pages are ready, testing pages are split-screened, or the user asks the agent to test, screenshot, process images, and produce the final HTML package.

## 1. Browser Authorization

Proceed when the user clearly says any equivalent of:

- "GSC我已经打开了，你去看一下"
- "Chrome浏览器给你打开了"
- "测评页面我已经开好了"
- "你自己去测试/截图/处理图片"
- "按照截图矩阵去截"

Rules:

- Work only in the authorized browser/page surfaces.
- Do not inspect cookies, local storage, passwords, unrelated tabs, browser profiles, or private account settings.
- If login or permission blocks the task, ask the user to sign in or expose the needed page.
- Do not replace a blocked logged-in page with search-engine guesses when the user specifically asked to use that page.

## 2. GSC Evidence Checklist

Use GSC as planning evidence, not public article copy by default.

Capture or record:

| Field | Required |
|---|---|
| Property | Yes |
| Date range | Yes |
| URL/page rows | Yes |
| Query rows | Yes |
| Clicks | Yes |
| Impressions | Yes |
| CTR | Yes |
| Average position | Yes |
| Filter/scope used | Yes |

Use GSC to decide:

- Which URL should be canonical.
- Whether duplicate URLs should be merged or redirected.
- Which queries need H2, FAQ, quick answer, tests, images, or internal links.
- Whether the main issue is impressions without CTR, weak ranking, cannibalization, or outdated intent.
- Which page cluster should be monitored after publication.

For consolidation decisions, output:

| URL | Clicks | Impressions | CTR | Avg position | Decision |
|---|---:|---:|---:|---:|---|

## 3. Google Trends Evidence Checklist

Use Google Trends when trend, freshness, year, geography, or query expansion matters.

Capture or record:

| Field | Required |
|---|---|
| Compared terms | Yes |
| Region | Yes |
| Time range | Yes |
| Category/search type | If changed |
| Trend direction | Yes |
| Related topics | When useful |
| Related/rising queries | When useful |

Use Trends to support:

- Title year/freshness choices.
- Which entity or model name deserves more prominence.
- Regional angle.
- FAQ additions.
- Screenshot/test dimensions when a rising query points to a specific use case.

Do not overstate Trends. Treat it as directional evidence unless exact values are exported and recorded.

## 4. Official And Benchmark Evidence

Use primary sources for dynamic facts:

- Official model announcements.
- Official docs/model overview.
- Pricing and plan pages.
- Release notes.
- Official API docs.
- Benchmark original pages or official leaderboards.

For each evidence screenshot, record:

| Field | Required |
|---|---|
| Article section | Yes |
| Claim supported | Yes |
| Source URL | Yes |
| Page/source title | Yes |
| Browser-visible locator | Yes |
| Capture area | Yes |
| Filename | Yes |
| Alt text | Yes |
| Caption | Yes |
| Insertion point | Yes |
| Priority | Must / Recommended / Optional |
| Status | Planned / Captured / Processed / Inserted / Skipped |

Use exact benchmark numbers only when they are clearly captured or extracted from a primary source. If not, phrase qualitatively and point readers to the official table.

## 5. Hands-On Test Design

Do not use a fixed test template. Build the test matrix from:

- Search intent.
- GSC queries.
- Google Trends related/rising queries.
- User concerns.
- Competitor coverage gaps.
- Official model/product positioning.
- Model-specific strengths.
- Article type.

Every test set should cover:

| Layer | What it means |
|---|---|
| Baseline capability | Correctness, instruction following, output usability, reasoning/explanation quality, verification awareness |
| Model/product strengths | Long context, agentic coding, web search, multimodal, UI generation, speed, low cost, safety review, tool use, or other claimed strengths |
| Search demand | Actual user questions from GSC/Trends/SERP/competitors |

For coding articles, debugging, refactoring, multi-file reasoning, unit tests, and security review are candidate dimensions only. Use them when they fit the query set and model claims; add or replace dimensions when the article needs other evidence.

For each hands-on test, record:

| Field | Required |
|---|---|
| Date | Yes |
| Venue | Yes |
| Models tested | Yes |
| Exact prompt | Yes |
| User task simulated | Yes |
| Evaluation dimension | Yes |
| Raw output location or summary | Yes |
| Observed differences | Yes |
| Practical article takeaway | Yes |
| Screenshot/comparison image | Yes when authorized |
| Status | Planned / Run / Captured / Processed / Inserted / Skipped |

Public copy should say "In the test..." or "In the picture..." rather than exposing internal screenshot language.

## 6. Screenshot Matrix Execution

Before execution, produce the matrix. After execution, update status.

Minimum matrix:

| # | Article section | Evidence type | Claim/task | Source or venue | Locator/prompt | Capture area | Filename | Alt | Caption | Insertion point | Priority | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Evidence types:

- GSC/Trends planning evidence.
- Official/source proof.
- Benchmark proof.
- Hands-on model output.
- Pricing/access proof.
- Contact sheet/review-only asset.

Do not put FAQ, final verdict, or general editorial sections into the screenshot matrix unless they need visual evidence.

## 7. Image Processing

After screenshots are captured:

- Keep raw captures when useful.
- Convert text-heavy screenshots to clear WebP.
- Use short descriptive filenames.
- Keep hands-on images separate from official/benchmark images when useful.
- Generate contact sheets for review when many images exist.
- Create an image asset index.

Image index fields:

| Field | Required |
|---|---|
| Filename | Yes |
| Dimensions | Yes |
| Type | Yes |
| Source | Yes |
| Alt text | Yes |
| Caption | Yes |
| Article insertion point | Yes |
| Required/optional | Yes |

Before final HTML, verify every `<img src="...">` exists locally.

## 8. Final Article Package

For a full evidence-backed article refresh, deliver:

| Artifact | Required contents |
|---|---|
| `*-body.html` | Pure public article HTML, target language, H1, TOC, H2 ids, real figures, tables, FAQ, natural links, no editor notes |
| `*-seo-workbench.html` | Chinese operation console, body copy link/zone, meta/OG/Twitter, canonical/redirect, TOC anchor map, screenshot matrix, image table, internal-link table, schema, CSS, QA |
| `image-asset-index.md` | All image files, dimensions, type, source, alt/caption, insertion point, priority |
| `memory/content/*-retro.md` | What worked, reusable rules, QA lessons, artifacts |

## 9. Final QA

Run these checks before saying the package is complete:

- All body image paths exist.
- Every TOC `href="#..."` matches an H2 `id="..."`.
- Heading anchor values omit `#`; TOC links include `#`.
- FAQ schema questions and answers match visible FAQ exactly.
- Article schema uses real image URLs or clearly marked publish-time replacements, not the article URL as image.
- Internal links in the body match the internal-link table.
- Public body has no Chinese editor notes.
- Public body has no backend terms: `GSC`, `URL A`, `URL B`, `screenshot matrix`, `placeholder`, `proof image`, `image insertion`, `alt text`.
- SEO workbench includes meta/OG, canonical/redirect, TOC map, image matrix, internal-link table, schema, CSS, and publish QA.
- Any skipped evidence item has a reason.
