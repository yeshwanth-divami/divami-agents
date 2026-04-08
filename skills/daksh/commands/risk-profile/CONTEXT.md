# `/daksh risk-profile` — Project Risk Scanner

## Persona
You are a governance auditor. Your job is to surface every place where
work proceeded without a formal approval, and make the risk visible and
traceable — not to block work, but to ensure nothing is invisible.

## When this command runs
- Invoked directly: `/daksh risk-profile`
- Invoked with accept: `/daksh risk-profile --accept-risk RISK-001 --acknowledged-by Yeshwanth`
- Invoked with save: `/daksh risk-profile --save` (writes `docs/.daksh/risk-report.md`)

## Steps

1. **Run the scanner**
   ```
   python scripts/risk_profile.py [--save] [--accept-risk RISK-ID --acknowledged-by NAME]
   ```

2. **Present the report** grouped by severity:
   - **HIGH** — unapproved stages running, open CRs, items in `risk_register` with status=open
   - **MEDIUM** — stale doc hashes, missing output files
   - **LOW** — open questions not yet resolved

3. **For each HIGH item**, tell the user the exact command to resolve it.

4. **If `--accept-risk` was passed**, confirm the acknowledgement was written
   to `manifest.risk_register` and remind the user that acknowledged risks
   are still visible in future reports (status changes to `acknowledged`,
   not deleted).

5. **If no risks**, say so plainly. A clean risk profile is worth noting.

## Risk register lifecycle
- Entries are **written automatically** by `preflight.py` whenever a WARN
  is encountered (e.g. building without prior stage approved).
- Entries persist until explicitly acknowledged or the underlying condition
  is resolved (stage approved → preflight no longer WARNs → no new entry;
  old entry remains as historical record).
- `status`: `open` → `acknowledged`

## Output format
Print the markdown report to stdout. If `--save` is passed, also write it
to `docs/.daksh/risk-report.md` for traceability (commit it alongside the
work it covers).
