#!/usr/bin/env python3
"""
Run this before publishing to create src/divami_skills/skills.zip.

    python scripts/pack.py

The zip is AES-encrypted for GitHub release distribution.
"""
import os
import sys
from pathlib import Path

import pyzipper

SKILLS_DIR = Path(__file__).parent.parent / "skills"
OUTPUT_ZIP = Path(__file__).parent.parent / "src" / "divami_skills" / "skills.zip"


def main():
    password = os.environ.get("DIVAMI_AGENTS_PASSWORD")
    if not password:
        print("Error: DIVAMI_AGENTS_PASSWORD is required.", file=sys.stderr)
        sys.exit(1)

    files = [f for f in SKILLS_DIR.rglob("*") if f.is_file()]
    print(f"Packing {len(files)} files...")

    with pyzipper.AESZipFile(
        OUTPUT_ZIP,
        "w",
        compression=pyzipper.ZIP_LZMA,
        encryption=pyzipper.WZ_AES,
    ) as zf:
        zf.setpassword(password.encode())
        for file in files:
            arcname = file.relative_to(SKILLS_DIR)
            zf.write(file, arcname)

    print(f"Created {OUTPUT_ZIP}")


if __name__ == "__main__":
    main()
