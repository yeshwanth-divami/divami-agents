---
description: "Start or complete an implementation task — git setup, time tracking, handbook patch, PR creation, Jira transition."
---

# Command: /daksh impl

## Syntax
```
/daksh impl start TASK-[MODULE]-NNN
/daksh impl done  TASK-[MODULE]-NNN
```

---

## impl start

1. Run preflight with the task ID for scoped dependency checks:
   ```
   python scripts/preflight.py impl [MODULE] --task TASK-[MODULE]-NNN
   ```
   Stop if non-zero.

2. Read the task from `docs/implementation/[MODULE]/tasks.md`: summary, ACs, decision budget, dependencies.
   Confirm all dependencies are Done. If any are not, stop and name the blocker.

3. **DR surface scan** — read the TRD section(s) referenced in the task. Extract every
   external code path, service, schema, or API the TRD touches that lives outside
   `docs/implementation/[MODULE]/`. For each:

   - Check if a Daksh spec exists: `docs/implementation/[OTHER-MODULE]/trd.md` present
     **and** the manifest stage for that module is `mode: greenfield`.
   - If no spec exists (file is inherited or pre-Daksh), it is a DR candidate.

   Also check `manifest.discovery_records` for any OPEN DRs on this module.

   If any candidates or open DRs are found, print a risk table before proceeding:

   ```
   DR Surface — review before implementing
   ───────────────────────────────────────
   legacy/order_service.py     no Daksh spec  (inherited)
   shared/audit_log.py         no Daksh spec  (inherited)
   DR-002                      OPEN — unresolved constraint on payments schema
   ```

   Ask: "Acknowledge and proceed, or stop to raise a DR?"
   Do not proceed to git setup until the engineer explicitly acknowledges.
   If the engineer stops to raise a DR, follow the DR procedure in
   `stages/50-implementation/CONTEXT.md` before returning here.

4. **CR surface scan** — using the TRD sections already loaded, identify the key design
   assumptions: data flow, service dependencies, interfaces, performance expectations,
   capacity constraints. For each assumption, check the relevant codebase paths.

   Flag any where the codebase contradicts or materially complicates the TRD:

   - A service or method the TRD depends on is missing, renamed, or has a different interface
   - A shared resource (connection pool, queue, cache) the TRD ignores will be contended
   - A performance assumption (row count, latency, throughput) is invalidated by actual code
   - A constraint (rate limit, transaction boundary, auth scope) exists that the TRD doesn't mention

   Also check `manifest.change_records` for any OPEN CRs on this module.

   If any candidates or open CRs are found, print a risk table before proceeding:

   ```
   CR Surface — review before implementing
   ───────────────────────────────────────
   TRD: stream CSV from DB        shared connection pool (src/db/pool.py, 10 conns)
   TRD: use existing auth         auth.py missing scope() — interface changed
   CR-003                         OPEN — payments schema change pending approval
   ```

   Ask: "Acknowledge and proceed, or stop to raise a CR?"
   Do not proceed to git setup until the engineer explicitly acknowledges.
   If the engineer stops to raise a CR, run `/daksh change [MODULE]` before returning here.

5. **Git setup:**
   ```
   git fetch
   git checkout [MODULE]/main && git pull
   git checkout -b [MODULE]/TASK-[MODULE]-NNN-<slug>
   ```
   `<slug>` = task summary lowercased, spaces → dashes, max 5 words.
   If the branch already exists, check it out instead.

6. Transition Jira ticket to Task in progress:
   ```
   python scripts/jira-sync.py transition TASK-[MODULE]-NNN "Development in Progress"
   ```
   If this fails, stop and surface the Jira error before coding. `impl start`
   must not proceed with local work while Jira still shows an earlier state.

7. Start time block:
   ```
   python scripts/jira-sync.py time-block start TASK-[MODULE]-NNN
   ```

8. Print to engineer:
   - Task summary and description
   - Decision budget
   - Acceptance criteria (numbered list)
   - TRD section(s) to follow

---

## impl done

1. Walk through each AC. Ask: "AC N: [text] — confirmed?" for each.
   Refuse to continue if any AC is unconfirmed.

2. Stop time block:
   ```
   python scripts/jira-sync.py time-block stop TASK-[MODULE]-NNN
   ```

3. Patch handbook (skip silently if `handbook/` does not exist yet):
   - Infer target section(s) from task signals using the audience signal mapping in
     `commands/handbook/CONTEXT.md`.
   - Run `/daksh handbook [section]` for each matched section.
   - Stage and commit handbook changes to the task branch:
     ```
     git add handbook/[section].md
     git commit -m "TASK-[MODULE]-NNN: docs — handbook patch"
     ```

4. Transition Jira ticket to Dev Internal Review:
   ```
   python scripts/jira-sync.py transition TASK-[MODULE]-NNN "Dev Internal Review"
   ```
   If this fails, warn and continue — the PR matters more than the Jira state.

5. Create PR:
   ```
   gh pr create \
     --base [MODULE]/main \
     --head [MODULE]/TASK-[MODULE]-NNN-<slug> \
     --title "TASK-[MODULE]-NNN: [summary]" \
     --body "..."
   ```
   PR body must include: task summary, ACs as a checklist, and the handbook
   section(s) updated (if any). Print the PR URL when done.
