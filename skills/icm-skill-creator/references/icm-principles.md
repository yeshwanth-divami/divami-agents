---
name: icm-principles
description: The five core ICM design principles and the five-layer context hierarchy. Layer 0 reference for any skill built with this methodology.
type: reference
---

# ICM Principles

Source: arxiv.org/html/2603.16021

---

## Five Design Principles

### 1. One Stage, One Job
Each workflow step handles exactly one transformation. A stage that does two things is two stages pretending to be one. Split it.

### 2. Plain Text Interface
All context is Markdown or JSON. Any human with a text editor can read, edit, and debug every artifact in the pipeline — no framework knowledge required.

### 3. Layered Context Loading
Agents receive only stage-relevant context. The "lost in the middle" problem is a loading problem. Solve it by not loading irrelevant context in the first place.

### 4. Edit Surfaces
Every intermediate output is a file. A human can open it, change it, and let the next stage consume the edited version. No black boxes between stages.

### 5. Factory Configuration
Set up once. Run many times. The workspace structure and references stay fixed; only the per-run working artifacts change.

---

## Five-Layer Context Hierarchy

| Layer | Name | What lives here | Changes? |
|---|---|---|---|
| 0 | Identity | SKILL.md — workspace orientation, routing table | Never |
| 1 | Routing | Which stage handles what input signal | Rarely |
| 2 | Stage Contracts | Inputs/process/outputs for one stage | Per skill version |
| 3 | References | Stable knowledge: conventions, rules, guides | Never per run |
| 4 | Working Artifacts | Per-run content: templates with `{{placeholders}}` | Every run |

**Key rule:** Layer 3 (reference) and Layer 4 (working) must remain structurally separate. Reference files constrain; working files are transformed.

---

## Token Budget by Layer

| Layer | Target token range |
|---|---|
| 0 | 200–800 |
| 3 (per file) | 300–1500 |
| 4 (per template) | 100–800 |
| Full context per stage | 2000–8000 |

Monolithic prompts run 30,000–50,000 tokens and degrade model performance. ICM keeps stages lean and focused.

---

## When NOT to Use ICM

ICM targets sequential workflows with human review gates. Do not force it on:
- Real-time multi-agent collaboration
- High-concurrency parallel execution
- Complex automated branching with no human checkpoints
- Single-step, trivially simple tasks
