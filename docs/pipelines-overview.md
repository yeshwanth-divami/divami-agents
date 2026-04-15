# Divami: Pipeline Overview

---

## 1. Marketing Pipeline
**Goal:** Generate awareness and inbound interest.

| Stage | Activities | Owner | Skill/Skillset |
|-------|-----------|-------|-------|
| Brand Awareness | Case studies, thought leadership, social, SEO |-|-|
| Demand Generation | Campaigns, webinars, paid ads, events |-|-|
| Lead Capture | Contact forms, demo requests, content downloads |-|-|
| Lead Enrichment | ICP scoring, company size, tech stack, budget signals |-|-|

Output → qualified MQL handed to Pre-Sales.

---

## 2. Pre-Sales Pipeline
**Goal:** Convert interest into a scoped, winnable opportunity.

| Stage | Activities | Owner | Skill/Skillset |
|-------|-----------|-------| ------|
| Lead Qualification | BANT/MEDDIC — Budget, Authority, Need, Timeline |-|-|
| Discovery | Requirements gathering, stakeholder mapping, pain points |-|-|
| Tech Feasibility | Architecture review, stack alignment, AI/ML scoping |-|-|
| Solution Design | High-level approach, team composition, tech choices |-|-|
| Effort Estimation | Story mapping, T-shirt sizing, detailed LOE |-|-|
| Proposal / RFP Response | SOW draft, pricing, differentiators, case studies |-|-|
| Presentation / Demo | PoC, prototype, live walkthrough |-|-|

Output → signed contract or lost deal (with reason logged).

---

## 3. Sales Pipeline
**Goal:** Close the deal.

| Stage | Activities | Owner | Skill/Skillset |
|-------|-----------|-------| ------|
| Negotiation | Pricing, payment terms, SLAs, IP ownership |-|-|
| Legal Review | MSA, NDA, DPA, security addendums |-|-|
| Contract Closure | SOW finalization, PO issuance |-|-|
| Handoff to Delivery | Internal kickoff, context transfer to delivery team |-|-|

Output → project kickoff initiated.

---

## 4. Design Sprint Pipeline
**Goal:** Define the experience before a line of code is written.

| Stage | Activities | Owner | Skill/Skillset |
|-------|-----------|-------|-------|
| Persona Definition | User research, persona creation, goals & pain points per persona | - | - |
| User Flows by Persona | Task flows, happy paths, edge cases mapped per persona | - | - |
| IA & Solution Flow | Information architecture, navigation structure, solution flow diagram | - | - |
| Screen Design | Wireframes → mid-fidelity → high-fidelity screens per flow | - | - |
| Visual Styling | Design language, color, typography, iconography, component patterns | - | - |
| Solution Design Spec | Annotated specs, interaction notes, handoff-ready Figma with tokens | - | - |

Output → design-approved spec handed to Delivery.

---

## 5. Delivery Pipeline
**Goal:** Build and ship what was sold.

### 5a. Project Initiation

| Stage | Activities | Owner | Skill/Skillset |
|-------|-----------|-------|-------|
| Requirements | Finalization, user story writing | - | - |
| Architecture | Design, tech stack confirmation | - | - |
| Team Onboarding | Environment setup, access provisioning | - | - |
| Sprint 0 | Tooling, CI/CD, repo structure | - | - |

### 5b. Development Sprints

| Track | Activities | Owner | Skill/Skillset |
|-------|-----------|-------|-------|
| Process | Sprint planning → dev → code review → QA → demo | - |-|
| Frontend | Design handoff (Figma), component library, responsiveness | - |-|
| Backend | API design, DB schema, integrations | - |-|
| AI/ML | Data pipeline, model training, evaluation, integration | - |-|

### 5c. QA

| Type | Activities | Owner | Skill/Skillset |
|------|-----------|-------|-------|
| Functional | Unit, integration, E2E testing | - |-|
| Non-Functional | Performance & load testing | - |-|
| Security | SAST/DAST scanning | - |-|
| Acceptance | UAT with client | - |-|

### 5d. Release

| Stage | Activities | Owner | Skill/Skillset |
|-------|-----------|---|-------|
| Staging | Deploy → client sign-off | - |-|
| Production | Deploy, migration scripts, rollback plan | - |-|
| Closure | Release notes, go-live checklist | - |-|

Output → delivered, accepted software.

---

## 6. Post-Delivery Support Pipeline
**Goal:** Keep the delivered product stable and evolving.

| Stage | Activities | Owner | Skill/Skillset |
|-------|-----------|-------|-|
| Hypercare (0–4 weeks post-launch) | Dedicated team on standby, priority bug fixes |-|-|
| Bug Triage | Severity classification (P0–P3), SLA response |-|-|
| Patch Releases | Hotfixes, dependency updates |-|-|
| Knowledge Transfer | Runbooks, architecture docs, training sessions |-|-|
| Transition | Handoff to client's internal team or retainer model |-|-|

---

## 7. Account Management / Post-Sales Pipeline
**Goal:** Retain, expand, and deepen client relationships.

| Stage | Activities | Owner | Skill/Skillset |
|-------|-----------|-------|-|
| Relationship Management | QBRs, health checks, exec alignment |-|-|
| Upsell / Cross-sell | New modules, AI additions, platform extensions |-|-|
| Contract Renewal | Re-scoping, rate revisions, multi-year deals |-|-|
| Referral Harvesting | Case study creation, testimonials, referrals |-|-|
| Churn Prevention | Early warning signals, satisfaction surveys (NPS/CSAT) |-|-|

---

## Pipeline Interconnections (Flow Summary)

```mermaid
flowchart LR
    M[Marketing\nAwareness → MQL]
    PS[Pre-Sales\nMQL → SQL]
    S[Sales\nSQL → Closed-Won]
    DS[Design Sprint\nPersonas → Spec]
    D[Delivery\nKickoff → Go-Live]
    SUP[Support\nHypercare → Retainer]
    AM[Account Mgmt\nRenew → Expand → Refer]

    M --> PS --> S --> DS --> D --> SUP --> AM
    AM -->|Expansion: new scope| PS
```

---

## Divami-Specific Notes

- **Frontend-heavy projects**: Design pipeline is a sub-pipeline inside Delivery — Figma → Design QA → Dev Handoff → Implementation → Design Audit.
- **AI projects**: Add a Data Pipeline track before Dev starts — data sourcing, cleaning, labeling, baseline modeling.
- **Fixed-price vs T&M**: Estimation accuracy in Pre-Sales directly impacts delivery margin — the two pipelines are tightly coupled in risk.
- **Staff augmentation model**: Delivery pipeline compresses; Account Management pipeline becomes the primary value-add.
