---
name: excavation-guide
description: How to extract raw facts from project artifacts — code, docs, transcripts, commit history. The archaeologist's field manual.
type: reference
---

# Excavation Guide

The evidence already exists. Your job is to find it, categorize it, and surface it — not to invent or embellish.

---

## Where to Dig

| Artifact type | What to extract | Where to find it |
|---|---|---|
| README / project docs | Problem statement, tech stack,<br/>architecture overview | Root dir, `docs/` |
| Source code | Tech stack (languages, frameworks),<br/>architecture patterns,<br/>integration points | `src/`, `app/`, `lib/`,<br/>`package.json`, `requirements.txt`,<br/>`Cargo.toml`, etc. |
| Commit history | Timeline, key milestones,<br/>major pivots, contributors | `git log --oneline -50` |
| Meeting transcripts | Client pain points (their words),<br/>decisions made, constraints stated | `*.md`, `*.txt` in `docs/`,<br/>`transcripts/`, `meetings/` |
| Google Docs | PRDs, proposals, client feedback,<br/>scope documents | User will provide access |
| Design files / links | UX decisions, before/after | References in docs or README |
| CI/CD config | Deployment complexity,<br/>environments, testing strategy | `.github/`, `Dockerfile`,<br/>`docker-compose.yml` |

---

## Extraction Categories

For each category, extract raw facts. Do not synthesize yet — that's the narrative stage's job.

### 1. Client Problem
- What was broken, slow, or missing?
- Who was affected? (end users, internal teams, leadership)
- What was the business cost of the status quo?
- **Look for:** kickoff transcripts, PRDs, the "why" sections of proposals

### 2. Constraints
- Budget, timeline, regulatory, technical debt, legacy systems
- What the team could NOT do (often more revealing than what they did)
- **Look for:** meeting notes, scope documents, ADRs

### 3. Approach Taken
- Methodology (agile sprints, design-first, prototype-then-build)
- Key architectural decisions and their rationale
- Tools, frameworks, integrations chosen and why
- **Look for:** ADRs, commit history patterns, code architecture

### 4. Tech Stack
- Languages, frameworks, databases, infrastructure
- Notable libraries or tools that solved specific problems
- **Look for:** dependency files, config files, Dockerfiles

### 5. Outcomes / Metrics
- Performance improvements (load time, throughput, error rates)
- Business metrics (conversion, revenue, cost reduction, time saved)
- User metrics (adoption, satisfaction, task completion)
- **Look for:** analytics configs, monitoring dashboards mentioned in docs, client feedback transcripts
- **Critical:** if a metric has no source, flag it — do not state it as fact

### 6. Notable Quotes
- Client's own words describing the problem or the result
- Anything that captures the pain or the relief authentically
- **Look for:** transcripts, email threads, feedback docs
- Always note the speaker's role (not name) for attribution

### 7. Domain Glossary
- Terms a non-expert leadership reader would not know
- Every named role, platform, or concept used in the docs without a plain-English definition must be flagged here
- **Look for:** jargon used without definition in docs, transcripts, code comments
- **Rule:** if a leadership reader might ask "what is that?" — flag it here. The narrative stage will define these on first use.

### 8. Failure Mode Catalog
- Every distinct root cause the system is designed to detect
- Enumerated explicitly, not just implied by architecture stages
- **Look for:** validation logic, runbooks, troubleshooting docs, system prompt rules
- Name each failure mode in plain language. Leadership will ask: "what exactly can go wrong?"

### 9. System Boundaries
- What the system explicitly does NOT do
- What the natural next extension would be (e.g. reactive → proactive, single-order → batch monitoring)
- What inputs the system accepts and why those specific inputs (not alternatives)
- **Look for:** scope decisions in meeting notes, ADRs, system prompt constraints, what's missing from the feature list

### 10. Deployment Configurability
- What changes per tenant, client environment, or deployment
- What is runtime-configurable vs hard-coded
- LLM / model provider flexibility — can the system swap models per client?
- **Look for:** .env files, config files, multi-tenant architecture docs, raw_file_map.json-style mappings

### 11. Agent Architecture
- Is this a single agent or multi-agent system? If multi-agent, what are the distinct agents and their roles?
- Distinguish: sequential architectural generations (V1, V2, V3) from concurrent system components
- **Look for:** agent definitions in source, system prompt role assignments, any orchestration logic
- Flag explicitly if the "three versions" are sequential iterations, not parallel agents running simultaneously

---

## Excavation Rules

1. **Never invent.** Every fact must trace to an artifact. If you infer something, mark it as inference.
2. **Preserve client language.** Their words for the problem are more powerful than your paraphrase.
3. **Flag gaps explicitly.** Missing metrics, unclear attribution, ambiguous scope — these become open questions, not silent omissions.
4. **Separate fact from interpretation.** "The API response time dropped from 3s to 200ms" is a fact. "The API became blazing fast" is interpretation. Extract facts.
5. **Cast a wide net first.** Read broadly before categorizing. The most valuable insight is often in an artifact you didn't expect.
