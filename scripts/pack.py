#!/usr/bin/env python3
"""
Run this before publishing to create divami_skills/skills.zip.

    python scripts/pack.py

The zip is AES-256 encrypted and NOT committed to git.
"""
import getpass
import os
import sys
from pathlib import Path

import pyzipper

SKILLS_DIR = Path(__file__).parent.parent / "skills"
OUTPUT_ZIP = Path(__file__).parent.parent / "divami_skills" / "skills.zip"


def main():
    password = os.environ.get("SKILLS_PASSWORD")
    if not password:
        password = getpass.getpass("Password for skills.zip: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords don't match.", file=sys.stderr)
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
