#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PREAMBLE = Path(__file__).with_name("readme-preamble.md")
SKILLS = sorted((ROOT / "skills").glob("*/SKILL.md"))

def desc(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^(?:`{3,}[^\n]*\n)?---\n(.*?)\n---\n", text, re.S)
    if not m:
        return ""
    for line in m.group(1).splitlines():
        if line.startswith("description:"):
            return re.sub(r'^["\']|["\']$', "", line.split(":", 1)[1].strip())
    return ""

rows = [
    "| Skill | Description |",
    "| --- | --- |",
    *[f"| [{p.parent.name}]({p.relative_to(ROOT).as_posix()}) | {desc(p)} |" for p in SKILLS],
]
preamble = PREAMBLE.read_text(encoding="utf-8").rstrip()
ROOT.joinpath("README.md").write_text(preamble + "\n\n" + "\n".join(rows) + "\n", encoding="utf-8")
