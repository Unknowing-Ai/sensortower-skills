#!/usr/bin/env python3
import argparse, json, os, re, sys

def parse_desc(text):
    parts = text.split("---", 2)
    if len(parts) < 3: return ""
    m = re.search(r'description\s*:\s*["\x27]?(.+?)["\x27]?\s*$', parts[1], re.MULTILINE)
    return m.group(1) if m else ""

SD = os.path.dirname(os.path.abspath(__file__))

def search(bd, kws):
    res, kl = [], [k.lower() for k in kws]
    rs = os.path.normpath(os.path.join(bd, "SKILL.md"))
    for root, _, files in os.walk(bd):
        if "SKILL.md" not in files: continue
        fp = os.path.join(root, "SKILL.md")
        if os.path.normpath(fp) == rs: continue
        try:
            with open(fp, encoding="utf-8", errors="replace") as f: c = f.read()
        except: continue
        if any(k in c.lower() for k in kl):
            res.append({"path": os.path.relpath(fp, bd).replace("\\", "/"), "description": parse_desc(c)})
    return res

def main():
    p = argparse.ArgumentParser()
    p.add_argument("keywords", nargs="+")
    p.add_argument("--base-dir", default=SD)
    a = p.parse_args()
    r = search(a.base_dir, a.keywords)
    if not r: print("No matching skills.", file=sys.stderr)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(r, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
