# WordPress Copy Page Pattern

This pattern was distilled from the user's sample `how-to-use-sora-2-on-pc-wordpress-copy.html`. Use it as a reusable structure, not as content to copy.

## Page Shell

Use a self-contained HTML file when the deliverable is a WordPress copy page.

Required page elements:

- Main page title: `{Article Topic} WordPress Copy Page`
- Intro note explaining that yellow guide boxes are editor instructions and white boxes are WordPress copy content.
- Top notes:
  - how to copy into WordPress,
  - fixed slug / URL,
  - image handling guidance,
  - caution notes for sensitive claims.
- Repeating modules:
  - `<section class="module">`
  - `<h2 class="module-title"><span>Module X</span>{Module Name}</h2>`
  - `<div class="guide">` for Chinese editor instructions
  - `<div class="copy-label">只复制下面白色正文框</div>`
  - `<section class="copy-box">` for publishable content

Use simple inline CSS for readability if producing a standalone copy page. The visual distinction matters: guide boxes should look separate from copy boxes.

## SEO Module

Place this before the article body. It is not publishable body copy.

Fields:

- Slug
- Title tag
- Meta description
- Primary keyword
- Optional secondary keywords
- Optional search intent

Title pattern:

- Practical guide title with the main keyword near the front.
- Avoid hype. Prefer "Step-by-Step Guide", "How It Works", "Common Problems", "Best Settings", or "Complete Guide" when relevant.

Meta pattern:

- 145-160 characters if possible.
- Include the main keyword, the practical outcome, and one trust/clarity hook.

## Recommended Article Module Order

Use this order for tutorial/product-explainer SEO posts:

1. Opening answer with PAS
   - H1 if WordPress will not render the page title automatically.
   - Start with `<strong>Quick answer:</strong>`.
   - Problem: state the user's core friction directly.
   - Agitation: acknowledge confusion, trust concern, availability, or failed route.
   - Solution: introduce the practical route and what the user will do.

2. Can you / Should you / Is it possible?
   - Give a direct yes/no/depends answer.
   - Clarify the actual route available now.
   - Mention outdated guides or old assumptions only when useful.

3. Why the obvious/official/default route may not work
   - Address the biggest objection early.
   - Use sourced, precise language.
   - When two access layers differ, explain the distinction plainly.
   - Use bullets for "both can be true" contrasts.

4. Why the recommended route works
   - This is often the core trust section.
   - Explain mechanism without sounding like a loophole.
   - For third-party platform articles, avoid phrases like "bypass", "crack", "unofficial trick", or "wild workaround".
   - Prefer "consumer website/app access" vs "API-based platform access" style distinctions when accurate.

5. What you need before starting
   - Short checklist.
   - Keep this lightweight.
   - No image unless setup is visually confusing.

6. Step-by-step tutorial
   - Use one H2 for the tutorial and H3 for each step.
   - One action per step.
   - Add screenshots after the relevant step paragraph.
   - Include realistic settings, examples, or prompts.
   - Add a final improvement/regeneration step when the workflow is iterative.

7. Tips / best practices
   - Use a concise bullet list.
   - Each bullet should be actionable.
   - Include one concrete improved example when relevant.

8. Common problems and fixes
   - Use a table with columns:
     - Problem
     - Likely reason
     - What to try
   - Include long-tail issues and safety/content restriction issues.

9. Trust, safety, official status, or comparison section
   - Put before FAQ.
   - Answer "Is this official?", "Is it safe?", "What are the limits?", or "What is the difference?".
   - Avoid overclaiming. Explain user responsibilities.

10. FAQ
   - H2 FAQ, then H3 question headings.
   - Cover People Also Ask style questions.
   - Keep answers direct, usually 1 short paragraph.
   - Include uncertainty for availability, quota, model lifecycle, legal, or policy-dependent issues.

11. Final takeaway
   - Short conclusion.
   - Restate the practical route.
   - Do not add a new concept.
   - Avoid adding images here.

12. Optional support sections
   - Assets table
   - Sources table/list
   - Internal links table

## Image Planning

For each image, provide:

- file path / proposed filename,
- insertion position,
- alt text,
- caption,
- whether it is required, optional, or source backup.

Use image categories:

- product/workflow screenshots for tutorial steps,
- official documentation screenshots for trust sections,
- optional hero/product screenshot near the opening if it proves the tool exists,
- backup evidence screenshots that may not appear in the article.

Do not over-insert images. For a tutorial article, usually use:

- 1 optional opening product screenshot,
- 1-3 trust/source screenshots if needed,
- 3-5 tutorial screenshots,
- no image in FAQ or final takeaway.

## Internal Links

Insert internal links naturally inside the copy box body, then list them at the end.

Internal link table columns:

- URL
- Plain anchor
- Linked anchor
- Placement

Rules:

- Keep link count modest.
- Use contextually relevant anchors.
- Do not force exact-match anchors in awkward places.
- Prefer helpful next-step guides, availability pages, prompt guides, download/export guides, restrictions/safety pages, and comparison pages.

## Sources

For source-sensitive articles, include an editor-facing source list near the end.

Rules:

- Do not blindly publish the whole source list unless the user asks for references in the article.
- Use official documentation for availability, discontinuation, API, pricing, policies, model support, and dates.
- For volatile facts, browse before writing and include concrete dates in the editor notes.
- Avoid unsupported "permanent availability" or "official partner" claims.

## Copy Style

Article body style:

- Clear, practical, calm.
- Lead with the answer.
- Use short paragraphs.
- Use `<strong>` to label "Quick answer:" or important UI terms, not for keyword stuffing.
- Use tables for troubleshooting.
- Use bullets for checklists and tips.
- Use H2/H3 hierarchy cleanly.
- Avoid marketing-heavy claims, vague hype, and decorative filler.

Editor guide style:

- Chinese notes are fine for this user.
- State where the block goes, how to handle images, and what not to claim.
- Keep guide notes short and operational.

## HTML Skeleton

Use this shape for each module:

```html
<section class="module">
  <h2 class="module-title"><span>Module X</span>Module name</h2>
  <div class="guide">
    <p><strong>怎么处理：</strong>...</p>
    <p><strong>插入位置：</strong>...</p>
    <p><strong>图片提示：</strong>...</p>
  </div>
  <div class="copy-label">只复制下面白色正文框</div>
  <section class="copy-box">
    <!-- publishable WordPress content -->
  </section>
</section>
```

For images in guide boxes:

```html
<p><strong>图片文件：</strong><code>assets/example.png</code></p>
<p><strong>Alt 文本：</strong>Descriptive alt text</p>
<p><strong>Caption：</strong>Short explanatory caption.</p>
```

For publishable article images, do not rely on local HTML `<img>` tags unless the user wants a preview page. In WordPress, images are uploaded separately and inserted at the positions described in the guide.
