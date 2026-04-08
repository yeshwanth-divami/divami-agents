#!/usr/bin/env python3
import argparse, json, pathlib, re, subprocess

def mk_alias(name, used):
    parts = re.findall(r"[A-Za-z]+", name)
    base = "".join(p[0].upper() for p in parts[:2]) or "SP"
    code, width = base, 3
    while code in used and used[code] != name:
        code = "".join(p[0].upper() for p in parts[:width]) or f"{base}{width}"
        width += 1
    used[code] = name
    return code

def iter_tabs(tabs):
    for tab in tabs:
        yield tab
        yield from iter_tabs(tab.get("childTabs", []))

def extract(items, out):
    for item in items:
        if "paragraph" in item:
            for el in item["paragraph"].get("elements", []):
                if "textRun" in el: out.append(el["textRun"]["content"])
                elif "person" in el: out.append(el["person"]["personProperties"]["name"])
                elif "dateElement" in el: out.append(el["dateElement"]["dateElementProperties"]["displayText"])
                elif "richLink" in el: out.append(el["richLink"]["richLinkProperties"].get("title", ""))
        elif "table" in item:
            for row in item["table"].get("tableRows", []):
                for cell in row.get("tableCells", []): extract(cell.get("content", []), out)

ap = argparse.ArgumentParser()
ap.add_argument("source")
ap.add_argument("output")
ap.add_argument("--tab-id")
ap.add_argument("--tab-title", default="Transcript")
a = ap.parse_args()
doc_id = re.search(r"/d/([A-Za-z0-9_-]+)", a.source)
data = subprocess.run(["gws", "docs", "documents", "get", "--params", json.dumps({"documentId": doc_id.group(1) if doc_id else a.source, "includeTabsContent": True})], capture_output=True, text=True, check=True)
obj, _ = json.JSONDecoder().raw_decode((data.stdout + data.stderr)[(data.stdout + data.stderr).find("{"):])
tab = next((t for t in iter_tabs(obj.get("tabs", [])) if t.get("tabProperties", {}).get("tabId") == a.tab_id), None) if a.tab_id else None
tab = tab or next((t for t in iter_tabs(obj.get("tabs", [])) if t.get("tabProperties", {}).get("title", "").lower() == a.tab_title.lower()), None)
if not tab: raise SystemExit("Transcript tab not found")
out = []
extract(tab["documentTab"]["body"]["content"], out)
lines = "".join(out).replace("\u000b", "\n").splitlines()
names = list(dict.fromkeys(m.group(1) for line in lines if (m := re.match(r"([A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+)+):", line))))
used = {}; aliases = {name: mk_alias(name, used) for name in names}
body = [next((f"{code}:{line[len(name)+1:]}" for name, code in aliases.items() if line.startswith(f"{name}:")), line) for line in lines]
header = ["Aliases:"] + [f"{code} = {name}" for name, code in aliases.items()] + [""]
path = pathlib.Path(a.output); path.parent.mkdir(parents=True, exist_ok=True); path.write_text("\n".join(header + body) + "\n")
