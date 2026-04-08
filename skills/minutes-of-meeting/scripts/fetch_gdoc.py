#!/usr/bin/env python3
"""
Fetch a Google Doc and write its plain text to a file.

Usage:
    gws docs documents get --params '{"documentId": "<ID>"}' 2>&1 | python3 fetch_gdoc.py -o <output.txt>
    python3 fetch_gdoc.py --doc-id <ID> -o <output.txt>

Arguments:
    --doc-id   Google Doc document ID (optional; if omitted, reads JSON from stdin)
    -o         Output file path (optional; defaults to stdout)
"""
import argparse
import json
import subprocess
import sys


def extract_text(content):
    text = []
    for elem in content:
        if "paragraph" in elem:
            for pe in elem["paragraph"].get("elements", []):
                if "textRun" in pe:
                    text.append(pe["textRun"]["content"])
        elif "table" in elem:
            for row in elem["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    text.extend(extract_text(cell.get("content", [])))
    return text


def parse_gws_output(raw: str) -> dict:
    lines = raw.split("\n")
    json_start = next(i for i, l in enumerate(lines) if l.strip().startswith("{"))
    return json.loads("\n".join(lines[json_start:]))


def fetch_doc(doc_id: str) -> str:
    result = subprocess.run(
        ["gws", "docs", "documents", "get", "--params", json.dumps({"documentId": doc_id})],
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    data = parse_gws_output(combined)
    return "".join(extract_text(data["body"]["content"]))


def main():
    parser = argparse.ArgumentParser(description="Fetch a Google Doc as plain text.")
    parser.add_argument("--doc-id", help="Google Doc document ID")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    args = parser.parse_args()

    if args.doc_id:
        text = fetch_doc(args.doc_id)
    else:
        raw = sys.stdin.read()
        data = parse_gws_output(raw)
        text = "".join(extract_text(data["body"]["content"]))

    if args.output:
        with open(args.output, "w") as f:
            f.write(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
