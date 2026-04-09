---
name: 04-scope-export
description: Context for Phase 4 — incrementally building scope.tree in three approval-gated steps before Excel generation.
stage: 4
---

# Phase 4 — Scope Draft

## Goal

Build `scope.tree` in three approval-gated steps. Never advance to the next step without explicit user sign-off on the current one. The file is written only after all three steps are approved.

The scope.tree is the last human checkpoint. Once approved and committed to file, `generate excel` treats it as locked.

---

## Extraction Source

Read `analysis.md` before starting Step 1. Map its content:

| scope.tree level | Source in analysis.md |
|---|---|
| **[Module]** | Major components from Architecture; top-level spine nodes from Build Order |
| **Feature** | Sub-components or named capabilities within each module |
| **Sub Feature** | Named screens, flows, or API endpoints per feature |
| **Complexity** | Derived from "What Is Hard" + Feasibility Verdict time horizons |
| **Component** | FE if UI-only, BE if API/data-only, FS if both |
| **Form Factor** | R (Responsive) unless analysis explicitly names mobile-native or web-only |
| **Phase** | Spine nodes 1–2 = P1, 3–4 = P2, bulges = P2/P3 |

---

## Complexity Mapping

| Label | What it means |
|---|---|
| XS | Single screen or endpoint, no business logic, no external dependency |
| S | 2–3 screens or endpoints, minor state, one external call |
| M | Multi-step flow, stateful, 2+ integrations, or non-trivial business logic |
| L | Cross-cutting concern, ML/AI pipeline, or 5+ interdependent components |
| XL | Platform-level, distributed system, or requires original research |

When in doubt, go one size up. Undersized items blow timelines.

---

## What NOT to Include

- Infra, DevOps, CI/CD — cross-cutting, not scope rows
- Research / spike items — open questions, not deliverables
- Anything in the "Open Questions" section of analysis.md

---

## Three-Step Approval Flow

### Step 1 — Modules

Present a flat numbered list of proposed modules. Nothing else — no features, no attributes.

Example format:
```
Proposed modules:

1. Registration
2. Identification
3. Discovery
4. Account Profile
5. Notifications

Add, remove, or rename. Say "ok" to continue.
```

Wait for approval. Do not proceed until user confirms.
Incorporate any additions, removals, or renames before Step 2.

---

### Step 2 — Features per Module

For each approved module, list its features (sub-groupings). Present all modules together in one message — indented, no attributes yet.

Example format:
```
Features per module:

Registration
    Registration

Discovery
    Discovery
    Global Search

Account Profile
    Account Profile
    User Profile
```

Wait for approval. User may add, remove, rename, or move features between modules.
Incorporate all changes before Step 3.

---

### Step 3 — Sub-features + Attributes

For each approved module → feature, list sub-features with full attributes. Present all at once.

Use the scope.tree column format exactly:
```
Registration
    Registration
        Email Signup                    XS  FE  R  P1
        Google Signup                   XS  FE  R  P2
        Invite-Based Registration       XS  FE  R  P3

Discovery
    Discovery
        Unified Search Bar              XS  FE  R  P1
        AI Semantic Search              S   FE  R  P2
    Global Search
        People to Follow                XS  FE  R  P3
```

Call out every L or XL item explicitly after the block:
> "Flagged for review: [item] assigned L — [one-line reason from analysis]"

Wait for approval. User may change complexity, component, form factor, phase, or sub-feature names.
Incorporate all changes.

---

## Writing the File

Only after Step 3 is approved:

1. Write `tech-feasibility-analyses/<codename>/scope.tree` with the standard header:
```
# <codename>
# <date>
# output_purpose: <client evaluation | internal architecture review | implementation planning>
```
followed by the approved content.

2. Confirm: "Written to `tech-feasibility-analyses/<codename>/scope.tree`. Say `generate excel <codename>` when ready."

Do not print the full file contents in chat after writing.
