# Artifact standards

Use the smallest structure that preserves decision context and enables the next module to read the work without relying on chat history.

## Common front matter

Start each artifact with its title, version or date, intended reader, current module, predecessor files read, and delivery boundary. End it with decisions, evidence limits, assumptions, open questions, and next-module inputs.

## 1. Framing artifact

Include: product context; target user and job; desired outcome; current workflow; product and AI role; durable core object; in-scope and out-of-scope behavior; action authority and confirmation gates; data and integration assumptions; success signals; risks; open questions.

## 2. Research report

Include: research question and scope; methodology and limitations; target-user or market structure; observed workflow; pain points and evidence; constraints and platform facts; evidence-to-product-question mapping; source table with citation metadata; unanswered questions. Keep product recommendations out of the factual findings.

## 3. Product plan

Include: positioning; target user and assumptions; product scope and non-goals; core objects and information architecture; independently enterable modules and their relationships; AI action boundaries; data provenance; confirmation/audit model; workflows inside features; metrics and guardrails; release boundary if requested. Preserve the distinction between a product workstation and a forced linear flow.

## 4. Demo / PRD spec

Include: scope precedence; demo goal and reviewer decision; mock scenario and data; visual constraints; routes/views; global interactions; page and component requirements; object model and state transitions; key journeys; loading/error/empty states; acceptance checklist; implementation constraints; explicit exclusions; a concise generator/developer handoff prompt if useful.

## 5. Demo acceptance report

Include: verification scope and source inspected; spec-to-implementation matrix; journey traces; actual state mutations; mock/integration boundary; confirmation and automation-boundary checks; visual/reference coverage; test/build evidence; findings ordered by materiality with file and line references; blocked checks; recommended next actions. Do not change source code.

