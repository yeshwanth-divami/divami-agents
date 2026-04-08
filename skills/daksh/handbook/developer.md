# Developer Handbook

This guide records the system contracts and extension points that matter when Daksh is maintained by future engineers or by LLMs working through Vyasa.

## Preflight Validator
`scripts/preflight.py` exists to stop a Daksh stage from consuming context on stale or missing inputs. Its current responsibility is narrow: load the manifest, resolve the stage key using the same `STAGE_MAP` contract as `scripts/approve.py`, verify the prior gate is approved, and surface missing or drifted prior outputs before the target stage runs.

`commands/preflight/CONTEXT.md` is the command-layer contract that sits in front of that script. It deliberately stays thin: run `python scripts/preflight.py <stage> [MODULE]` from the project root, show the script output verbatim, and route the next action purely from the exit code. Keep this file aligned with the script interface; if the CLI shape or success-blocked messaging changes, the command context must change in the same task.

The important boundary is that preflight is read-only. It reports state through `[PASS]`, `[WARN]`, and `[FAIL]` lines plus a final result line, but it does not mutate docs, rewrite hashes, or repair the manifest. Downstream stage contexts depend on that contract because they can call preflight safely without risking side effects.

Implementation-stage preflight is stricter than document-stage preflight. Once the resolved key is a stage 50 module key, missing prior outputs and hash drift become blocking failures instead of warnings because Daksh treats code work on top of stale approved docs as workflow corruption, not editorial drift.

Stage 50 also adds two module-scoped guards. The first runs `git status --porcelain` and blocks if the working tree is dirty, which keeps `/daksh impl start` from layering task work on top of unrelated edits. The second parses each task's `Depends on:` line from the module `tasks.md` file and checks those task ids against `manifest.traceability`; any dependency not recorded as `done` is a blocking failure.

When extending this validator, preserve the shared stage-resolution behavior with `approve.py` unless both commands are changed together. Add new checks only when the PRD or TRD says they are part of the gate, and be explicit about whether a failure is blocking or advisory because that changes Daksh workflow semantics.

Current known failure modes are straightforward: missing manifest means the pipeline has not been initialized in the current project, unknown stage means the invocation or routing is wrong, and hash drift means an approved upstream document changed after approval. Unit coverage for the current slice lives in `tests/test_preflight.py`.

All seven check rows from the TRD check matrix have at least one passing and one failing test. Every test uses in-memory manifest dicts and `tempfile.TemporaryDirectory` — no test reads the real `docs/.daksh/manifest.json`. Real `git` subprocess calls are eliminated by mocking `preflight.git_working_tree_clean` at the module level. When adding a new check to the script, add a corresponding test that exercises both the pass path and the failure path; a check with only a happy-path test gives the wrong confidence signal.

`tests/test_preflight_integration.py` is the self-hosting gate. It runs the real `scripts/preflight.py` binary as a subprocess against the real `docs/.daksh/manifest.json` — no mocking, no fixture manifest. The parametrized stages (`brd`, `roadmap`, `tasks PREFLIGHT`) are the stages that were approved at the time this sprint closed. If this test fails after a manifest change, the failure is real: a hash has drifted, an approval is missing, or the script has regressed. Do not suppress or skip the failure; diagnose it. Tests are marked `@pytest.mark.integration` and live in a separate file so unit tests can run without hitting the filesystem or spawning subprocesses: `python -m pytest tests/test_preflight.py`. The `pytest.ini` at the project root registers the `integration` mark to avoid warnings.

## Jira Sync
`scripts/jira-sync.py` is the manifest-to-Jira bridge. Its contract is simple: `push` writes Jira keys into `manifest.jira.ticket_map`, `pull` maps Jira workflow status back into `manifest.traceability` plus the `Status` column in module `tasks.md`, `status` reports sync health, `transition` walks the workflow graph in `docs/.daksh/jira-workflow.json`, and `time-block` records local time first, then submits worklogs only when a Jira key exists.

The state boundary matters. Jira metadata lives under `manifest.jira` (`project_key`, `board_id`, `done_statuses`, `ticket_map`, `user_map`, `synced_at`), while execution history lives under `manifest.traceability`. That split keeps sync configuration separate from delivery evidence; future changes should preserve it.

`push` now resolves sprints before stories and assigns each created or force-updated ticket to the sprint named in `tasks.md`. If you change sprint parsing, keep the rule that task docs remain the source of truth and that dry-run stays side-effect free. `commands/jira/CONTEXT.md` is intentionally a thin wrapper over this script; if the CLI shape changes, update the command contract in the same task.

`scripts/list-tasks.py` depends on the traceability object form, not the old flat-string shape. `--name` is exact match, case-insensitive; `--open` treats missing traceability as `not_started`; and the expanded output with `Assigned to` and `Status` only appears when `--name` is used. Changing those semantics without updating the handbook will create quiet operator mistakes.

The JIRA test surface lives in `tests/test_jira_sync.py` and `tests/test_jira_sync_integration.py`. The unit file uses the import shim `scripts/jira_sync.py` because Python cannot import a hyphenated module directly; if you rename the CLI file or move its public helpers, keep the shim or replace it with an equally stable import path so tests do not collapse.

## Changelog
- 2026-03-28: Added the initial preflight validator scaffold and its first unit-test coverage.
- 2026-03-29: Added implementation-stage blocking rules for dirty git state, task dependency status, and stricter prior-doc validation.
- 2026-03-29: Documented the preflight command-layer contract so future maintainers treat `commands/preflight/CONTEXT.md` as a thin wrapper over `scripts/preflight.py`.
- 2026-03-29: Expanded unit tests to cover all 7 TRD check matrix rows with both pass and fail paths; fixed two stale tests that diverged from updated dependency message format and pending-approval check additions.
- 2026-03-29: Added integration test suite (`tests/test_preflight_integration.py`) — self-hosting gate against real manifest; added `pytest.ini` with integration mark registration.
- 2026-03-29: Documented Jira sync, traceability-backed task listing, the command wrapper contract, and the dedicated JIRA test surface.
