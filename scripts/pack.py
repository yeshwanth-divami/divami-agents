#!/usr/bin/env python3
"""
Run this before publishing to create src/divami_skills/skills.zip.

    python scripts/pack.py

The zip is a plain archive of the local skills tree.
"""
import sys
import zipfile
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "skills"
OUTPUT_ZIP = Path(__file__).parent.parent / "src" / "divami_skills" / "skills.zip"


def main():
    files = [f for f in SKILLS_DIR.rglob("*") if f.is_file()]
    print(f"Packing {len(files)} files...")

    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            arcname = file.relative_to(SKILLS_DIR)
            zf.write(file, arcname)

    print(f"Created {OUTPUT_ZIP}")


if __name__ == "__main__":
    main()
