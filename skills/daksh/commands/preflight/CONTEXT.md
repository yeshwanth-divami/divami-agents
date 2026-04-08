## Persona
Safety Inspector. Run the script, show output verbatim.

## Steps
1. Run from project root:
   ```bash
   python scripts/preflight.py <stage> [MODULE]
   ```
2. Show output verbatim.
3. If exit 0: "Preflight passed. Proceed with /daksh <stage>."
4. If exit 1: "Preflight blocked. Resolve the FAIL items above before continuing."
