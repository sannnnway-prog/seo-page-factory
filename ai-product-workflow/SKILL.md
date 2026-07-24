---
name: ai-product-workflow
description: Guide modular AI-product work from problem framing through research, product-plan design, high-fidelity Demo/PRD specification, and read-only prototype acceptance. Use when users ask to plan, research, define, specify, validate, or iterate an AI product, agent, workflow, or clickable Demo, especially when prior Markdown artifacts, design references, or source code must inform the next stage.
---

# AI Product Workflow

Run one explicitly approved module at a time. Treat every module output as an input to later work.

## Activation gate

When the request semantically matches this skill, identify the likely module from the prompt and current conversation, then ask whether to start this skill before reading files, researching, writing deliverables, or changing code. State the proposed module in one sentence.

After the user confirms, execute the selected module. If the user declines, continue only with the ordinary request; do not present the skill workflow as active.

Do not infer approval merely because the user described an AI-product task. If the user has explicitly named the skill, still make the activation state visible; a concise confirmation is sufficient.

## Non-negotiable operating rules

1. Read the previous completed module's artifact in full before asking substantive questions. Also read every directly relevant current artifact, supplied reference, and—during acceptance—source file needed to verify a claim.
2. Do not repeat information already established in those artifacts. Ask one question at a time only for a gap that would materially affect scope, evidence, constraints, or the quality of the current deliverable.
3. Keep reading and questioning both present. Do not skip reading because the user gave a summary; do not skip gap questions because files exist.
4. Separate facts, evidence-backed inferences, assumptions, and recommendations. Mark confidence, source limits, and unresolved questions where relevant.
5. Default to a Chinese Markdown artifact in the current project directory. Use English for technical identifiers, state names, routes, schemas, and code examples unless the user requests another convention.
6. Complete only the approved module. Deliver its artifact, summarize the decision-relevant outcome, name the next recommended module, and stop until the user explicitly starts another module.
7. Preserve the user's files. In the acceptance module, inspect and verify only; never edit implementation code unless the user separately authorizes a change.

Read [references/artifact-standards.md](references/artifact-standards.md) before drafting an artifact. Use its structure as a baseline, adapting sections only when the project makes them inapplicable.

## Module router

Choose the narrowest module that matches the user's current need. If the user has not selected one, identify the likely module at the activation gate and ask for confirmation.

| Module | Use for | Required predecessor |
|---|---|---|
| 1. Problem and boundary framing | A new AI-product idea, unclear target user, outcome, agent role, or risk boundary | User brief and any existing product context |
| 2. User, market, and workflow research | Evidence about users, jobs, operational workflow, pain points, competitors, or platform constraints | Latest framing artifact |
| 3. Product plan and operating model | Turning evidence into an object-centered product plan, scope, workflow, data/permission boundaries, and metrics | Latest framing and research artifacts |
| 4. Demo / PRD specification | A high-fidelity clickable-Demo or implementation specification | Latest plan plus relevant visual references |
| 5. Demo source acceptance | Checking whether a generated prototype actually implements its specification and stated interactions | Latest specification and the prototype source |

### 1. Problem and boundary framing

Establish the product outcome, target segment, job or workflow, context, constraints, success evidence, and the AI system's role. For agents or workstations, define the durable business object that connects modules; do not automatically impose a linear end-to-end workflow.

Define allowed actions, confirmation gates, human responsibility, data availability, and prohibited behavior. Distinguish a workflow internal to one feature from the product's overall information architecture.

Write the framing artifact and stop. Do not start external research or solution design unless those are the approved module.

### 2. User, market, and workflow research

Start from the framing artifact. Define the research question, population, geography, product stage, and evidence threshold before searching.

Use primary platform documentation for rules, interfaces, and policies; use credible research, surveys, and user voices for behavior and pain points. Cite every material external claim with publisher, title, URL, publication or survey date when available, access date, and the precise supporting evidence. Never present overlapping survey adoption rates as mutually exclusive market share.

Produce a fact report, not a disguised product proposal. Keep a dedicated section that maps verified workflow facts to existing product questions without prescribing a solution.

### 3. Product plan and operating model

Read the framing and research artifacts first. Translate evidence into a coherent plan with a target user, product positioning, scope, explicit non-goals, information architecture, durable core objects, module relationships, interaction and confirmation boundaries, data provenance, metrics, and safety guardrails.

For an AI agent, define whether each capability may observe, explain, draft, recommend, confirm, execute, or verify. Require evidence and a user confirmation record for consequential writes. Do not turn uncertain AI outputs or inaccessible competitor data into facts.

Model a workstation as independently enterable modules connected through shared objects, evidence, tasks, and history when that fits the product. Do not call this a linear workflow unless the user explicitly wants one.

### 4. Demo / PRD specification

Read the current product plan, research evidence, and supplied visual references. Clarify the intended reviewer, decision, fidelity, platform, language, and mock-versus-real boundary only after reviewing them.

Specify a coherent mock scenario, information architecture, routes/views, durable objects, state transitions, key interactions, confirmations, loading/error/empty states, cross-module navigation, acceptance checks, design constraints, and explicit exclusions. Make each high-risk or write-like action visibly simulated unless the user authorizes an integration.

Write a spec that a prototype generator or development team can implement without guessing. Do not implement code in this module.

### 5. Demo source acceptance

Read the specification before inspecting code. Trace each required journey through the relevant source, mock data, state updates, UI action handlers, and any existing tests or build configuration.

Report each requirement as `implemented`, `partially implemented`, `mocked only`, `missing`, or `unverifiable`. Cite source paths and exact line numbers. Test only with safe, existing commands; do not trigger dependency installation, modify files, or repair failures. If verification is blocked, record the cause and the strongest available static evidence.

Assess both behavior and boundaries: distinguish a real state mutation from a toast, modal, or visual placeholder; distinguish a mocked integration from a real one; verify that confirmation gates and prohibited automated actions are actually enforced.

## Handoff discipline

End every artifact with: decisions made, evidence limits, explicit assumptions, open questions, and the exact inputs the next module must read. Link or name the predecessor artifacts so the next module can inspect them rather than rely on conversation memory.

