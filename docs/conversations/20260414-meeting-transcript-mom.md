---
title: Divami AI Strategy — 1+1 Squad, Skills Infrastructure, SDLC Pipeline
date: 2026-04-14
participants: Satyasri Prabhakar Mantripragada (SP), Yeshwanth Reddy Yerraguntla (YR)
transcript_local: docs/conversations/20260414-meeting-transcript.txt
transcript_source: https://docs.google.com/document/d/1M12svKSq0yMG4fV9nQ4HQppEaccnoJ2_4BIM2XjKzt0/edit?tab=t.po6u86pz790x
segment: 02:45:48 – 04:34:20
---

# Divami AI Strategy — 1+1 Squad, Skills Infrastructure, SDLC Pipeline

## Participants

**SP** — Satyasri Prabhakar Mantripragada
**YR** — Yeshwanth Reddy Yerraguntla

Late-evening session. SP laid out the full company transformation thesis — six learning tracks, a 1+1 squad delivery model, and a Dec 31 capability deadline. YR stress-tested it: agent quality at org scale, the need for specialized guardrails, and whether grassroots skill-building is a realistic expectation. The second half became an SDLC pipeline planning session, with concrete action items around a skills spreadsheet, GitHub access, and the Diwami-agents repo.

---

## Act I — Six Tracks and the 1+1 Squad Vision (~02:45 – ~02:57)

SP opened by laying out the six learning tracks Divami is building:

1. **Business & Spec** — from vision statement to detailed product spec and TRD
2. **Backend Engineering** — fundamentals, architecture, database; taught in both Node and Java
3. **QA** — test specs, automation, endpoint/load/performance testing (GenAI-augmented)
4. **GenAI & LLM** — prompt engineering, agent workflows, AI-native architecture
5. **Soft Skills / Advanced** — communication, presentation, DevOps, security, advanced DB
6. **Design** — required for all engineers, not just designers

The goal these tracks are pointing at is the **1+1 squad**: one business-savvy person (functioning as DM + PO + scrum master, very tech-aware) and one business-aware engineer (capable of full-stack delivery, code review, architecture, and spec writing). With consulting help from an architect, designer, and DevOps, this squad should deliver a mid-size project — defined as something like HRX, without deep AI-native architecture — in **two months end-to-end** instead of the current six.

> *"One month is going to be spent purely on gathering requirements, really defining the business problem, really speccing out detailed specs, validating requirements with the customer, perhaps with prototyping, perhaps with showing them mockups. Then one month is the core build time."*
> — SP _(~02:50:23)_

The build month breaks down as: one week spinning up agents and building; one week bulletproofing (tests, load, performance, standards); two weeks UAT. The timeline for how many people reach 1+1 capability:

- **3 months**: 10 people
- **6 months**: 30 more
- **9 months**: 30 more (total ~70)
- **Dec 31**: those outside X+Y+Z% are no longer required

---

## Act II — YR's Reality Check: Org-Scale Agent Quality (~02:55 – ~03:14)

YR pushed back immediately on the bullish framing. The argument was not against agents but against complacency:

> *"Even the most intelligent, like Opus — it sometimes makes the stupidest mistakes. If you try to scale it over an entire organization, that 5% probability will naturally blow to 95% over the organization."*
> — YR _(~03:01:23)_

YR's core point: the culture has to be that leaders are **actively maintaining skills**, everyone understands that AI is not a fire-and-forget system, and people know what is about to happen before they let an agent run. He named the risk of complacency explicitly — people will not learn if they assume the setup is good enough to go for a walk and come back to a finished product.

> *"The culture should not be in the sense that I have enough tokens, let me just spin up enough agents, it's going to work and I'll blindly go for a walk and come back and I know it's going to be done."*
> — YR _(~03:02:46)_

SP clarified: the one-week build window assumes a human actively in the loop — verifying integration, reviewing quality, writing cleanup tasks when the agent generates redundant components. Post-task, pre-commit, human review is not optional.

YR introduced the concept of **pre-implementation awareness** — the human needs to be in control of what is *about to* happen, not just reviewing after the fact. He referenced "harness engineering" and the idea that with the right guardrails (test-on-fail, retry, loop-detection), autonomous operation becomes more viable, but it requires iteration:

> *"I don't think Divami is in a position where we can come up with the right instructions even in the first month. We need to go through at least 50 iterations to come up with something that is 50% decent."*
> — YR _(~03:05:00)_

SP agreed on the review obligation and raised the deeper motivation for the engineering track: if people don't understand backend fundamentals, they can't review whether the agent is doing it correctly. He gave a concrete example — putting a query in a loop when a single SQL join would suffice — and said the engineering track exists precisely to build that review capability, not to replace the agent.

> *"The whole point of SQL is that you never have to put a query in a loop. You shouldn't. You have to figure out a SQL that doesn't need a loop."*
> — SP _(~03:10:42)_

---

## Act III — Specialized Task Agents and the Pipeline Architecture (~02:57 – ~03:26)

SP argued that the current "one task implementation agent" model is too blunt. The agent needs to be task-type-aware:

- **CRUD service tasks** → default guardrails: all attributes filterable, sort orders defined, no hardcoded values, lookup tables for enums, basic validations
- **Business logic service tasks** → different guardrails for complexity, side effects, consistency
- **Database design tasks** → prefix tables by module, no string enums, specific indexing conventions
- **Frontend component tasks** → find existing components first; if writing pages, behave one way; if pop-ups/overlays, another; no redundant API calls; cache metadata; use state management correctly

> *"There is not just one task implementation agent. The task implementation agent has specializations. If the task is database design, then you look up some instructions."*
> — SP _(~02:59:07)_

The problem with embedding all guardrails in the TRD: the agent follows the spec at the TRD level but reverts to bad patterns at the task level. Skills (as codex instructions) solve this — they persist across context resets and apply at the right granularity.

SP also described the **reverse pipeline**: a parallel agent continuously reviewing code, identifying patterns like duplicated utility logic across three services, logging issues, and producing a running list of corrections. The forward pipeline builds; the reverse pipeline reviews and raises new cleanup tasks. Together they form a continuous cycle rather than a single pass.

> *"On one side you have the execution agents. On the other side there is another agent which is continuously reviewing code. It is saying, hey in this particular module you used the same code in three different services — why are you not using a utility?"*
> — SP _(~02:56:42)_

The 300-instruction problem came up: when you put all guidelines in one prompt, the agent follows roughly 10 of them. Task-specific context windows solve this — small, targeted instructions for the exact task type being executed. SP also flagged that Playwright (or equivalent) tests should be generated in the same flow as the feature, since lint, build errors, and unit test generation are already happening automatically.

---

## Act IV — Skills Culture Debate: Top-Down vs. Grassroots (~03:26 – ~03:56)

YR presented the current Diwami skills inventory and meta-skills:

- **Skill-creation skill** — guides LLMs on what makes a good skill (stages, reviewability, intermediate checkpoints)
- **Retrospect skill** — when something goes wrong, traces which lines in the skill caused the bad assumption and updates the skill so the same mistake doesn't recur across all 10 squads
- **Personal conversation skills** — per-person preferences (multi-agent on first go vs. slow; educational vs. execution; verbose planning vs. direct)
- **Scoping & estimation skill** — iterative Q&A to produce a module/feature tree, intermediate markdown format (not Excel), then Python script converts to the standard estimation Excel format

> *"My goal is: can we make our work possible with the most stupid LLM? That is when we as a company will be really successful — when the process is so good that even the dumbest LLM can achieve it."*
> — YR _(~04:32:23)_

SP asked directly: of the 50 people they forced to use Daksh, how many opened the skills files to understand how they work? YR estimated five. SP's reaction was blunt — curiosity is not trainable; the A+ engineer doesn't need to be told to explore; if that baseline isn't there, the person is not useful. He sketched a four-tier model:

- **A+**: explores without being told; comes back and fixes what's wrong in the tooling
- **A**: fixes it for themselves, doesn't report back
- **A−**: identifies blockers, works around them, doesn't fix the root cause
- **B+**: hit by blockers, can't even get the tools working

> *"I don't want to waste time with them trying to say, look guys, you need to be more curious. If they still haven't opened that file, I don't want to waste time on that."*
> — SP _(~03:38:34)_

YR's counter: 5 people developing skills for 100 is fundamentally different in quality from 70 people chipping in — it's a paradigm difference, not just a magnitude difference. SP agreed on the ideal but pushed back: don't wait for that scenario; get a solid baseline of skills built by the 5, let the rest consume, and accept whoever organically contributes.

The resolution: YR will build baseline skills and a contribution framework; SP will not mandate skill-writing in the courses (that is not his core problem — his core problem is delivering the 1+1 squad capability); whoever contributes above the baseline is a bonus.

---

## Act V — SDLC Pipeline Mapping and Spreadsheet Action (~03:57 – ~04:15)

YR offered to deliver the 10–15 key AI workflow pipelines. SP walked the SDLC to identify where the gaps are:

| Stage | Status |
|---|---|
| Vision → Roadmap → BRD | Reasonably handled |
| PRD / product spec | Done; worth a deep review against Amazon's "AC" framework |
| TRD generation | Needs improvement — structure and missing elements |
| Task breakdown + implementation | Most work needed; specialized agents + guardrails |
| Review / validation | Reverse pipeline not yet built |
| Testing | Unit tests happening; E2E (Playwright) not yet in flow |

SP asked YR to create a **spreadsheet** that maps:
- All task types (backend: CRUD, service, DTO, API, DB design; frontend: components, pages, overlays; QA: unit, E2E, load, performance; GenAI; design)
- Owner for each type's guardrail development
- Markdown guideline files per type, structured for agent consumption

> *"Set up a spreadsheet where all the type of skills necessary for core development — what is needed for a core engineer to build, post breakdown of tasks. What are the types of backend work that need different thought processes? What are the different types of frontend work?"*
> — SP _(~04:03:35)_

SP flagged the **Amazon "AC" framework** (has a white paper internally) as a reference for what a mature product definition process looks like. He wants to run a gap analysis between AC and Divami's current Daksh PRD stage.

On the **repo**: YR demoed the `divami-agents` repo and proposed it as the central home for all Diwami skills going forward. SP agreed — move everything there; don't publish experiments out of personal repos. SP committed to getting YR **org-level GitHub repo creation access** (to be arranged with Gopal). For non-technical contributors: raise a GitHub issue with the improvement prompt; someone technical picks it up and opens a PR.

---

## Act VI — Ambition Check and Closing (~04:15 – ~04:34)

**Ambition check**: YR asked directly whether 1+1 is too ambitious. The honest concern — people at Divami don't yet write English sentences that communicate what they mean to another human; expecting them to prompt an agent precisely enough to deliver quality is a large leap.

> *"We may have to start somewhere — maybe this opportunity — but I would suggest we should not put high stakes on it. Experiment with one or two squads and then see."*
> — SP _(~04:18:46)_

YR flagged the human cost: pressure turning into frustration. SP agreed on a soft start — 1–2 experimental squads, no mandate across all 100 people yet.

**Claude Code source leak**: YR observed that the leaked Claude Code source is architecturally poor — features taped together, no structural care. His read: Anthropic is betting that future model capability will outpace the code quality debt; they don't need beautiful code if the model rewrites everything. The implication for Divami: if the world's best AI shop is writing code that badly, assuming internal teams will write good AI-assisted code without rigorous process and review is "70–80% fantasy."

SP closed with the note that Claude's output quality is still better than others, even if token consumption is high. The meeting ended with an agreement to reconvene the next day (Saturday).

---

## Todos

- [ ] YR: Create spreadsheet of all skill types × task categories (backend CRUD/service/DTO/API/DB, frontend components/pages/overlays, QA, GenAI) with owner assignments and markdown guideline file stubs | author: Yeshwanth Reddy Yerraguntla | deadline: 2026-04-21
- [ ] SP: Pass Amazon "AC" framework white paper to YR for gap analysis against Daksh PRD stage | author: Satyasri Prabhakar Mantripragada | deadline: 2026-04-21
- [ ] SP / Gopal: Grant YR org-level GitHub repo creation access in Divami GitHub org | author: Satyasri Prabhakar Mantripragada | deadline: 2026-04-15
- [ ] YR: Migrate divami-agents skills repo to Divami org GitHub (pending access grant) | author: Yeshwanth Reddy Yerraguntla | deadline: 2026-04-18
- [ ] YR: Build forward pipeline (task-type-aware specialized agents) and reverse pipeline (continuous code review agent) infrastructure for multi-agent development | author: Yeshwanth Reddy Yerraguntla | deadline: 2026-05-15
- [ ] YR: Saturday class — demo QA skills automation to squads so they understand they are no longer bottlenecked on QA resources | author: Yeshwanth Reddy Yerraguntla | deadline: 2026-04-19
- [ ] SP: Identify 1–2 pilot squads for 1+1 experiment; no pressure on all 100 people yet | author: Satyasri Prabhakar Mantripragada | deadline: 2026-04-28
