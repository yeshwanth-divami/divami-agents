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

3. Git setup:
   ```
   git fetch
   git checkout [MODULE]/main && git pull
   git checkout -b [MODULE]/TASK-[MODULE]-NNN-<slug>
   ```
   `<slug>` = task summary lowercased, spaces → dashes, max 5 words.
   If the branch already exists, check it out instead.

4. Transition Jira ticket to Task in progress:
   ```
   python scripts/jira-sync.py transition TASK-[MODULE]-NNN "Development in Progress"
   ```
   If this fails, stop and surface the Jira error before coding. `impl start`
   must not proceed with local work while Jira still shows an earlier state.

5. Start time block:
   ```
   python scripts/jira-sync.py time-block start TASK-[MODULE]-NNN
   ```

6. Print to engineer:
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
