# Mode: Review

Input: an existing document (paste the content or provide the file path).

For each section, check against these failure modes:
- Document opens with a heading or diagram before any prose → missing context seed
- A diagram appears before the prose that explains it → narrative-before-diagram violation
- Unresolved decisions are buried in prose or comments → missing unresolved-decisions section
- Related docs are listed in a footer block → inline link violation
- A domain-specific term appears without a link to the glossary → glossary link violation
- A table of fields, steps, or choices has no justification → missing justification section
- Downstream document repeats the full system context from the root doc → seed variation violation
- A manual sends the reader to another page before the first complete happy path or before the first blocked-state recovery → navigation-before-action failure

Output: a numbered list of issues. For each, show the **before** (the failing text) and the **after** (the fix). Do not describe the problem without showing the solution.
