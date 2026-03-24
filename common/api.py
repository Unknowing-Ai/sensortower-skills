#!/usr/bin/env python3
import json, os, sys, requests

SD = os.path.dirname(os.path.abspath(__file__))
PD = os.path.dirname(SD)
API = "https://api.sensortower.com"

def get_token():
    t = os.environ.get("SENSORTOWER_AUTH_TOKEN", "")
    if t: return t
    ep = os.path.join(PD, ".env")
    if os.path.exists(ep):
        with open(ep, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or "=" not in line: continue
                k, _, v = line.partition("=")
                if k.strip() == "SENSORTOWER_AUTH_TOKEN": return v.strip().strip("'\"")
    print("Error: SENSORTOWER_AUTH_TOKEN not found.", file=sys.stderr)
    print(f"Set it in: {ep}", file=sys.stderr)
    sys.exit(1)

def api_get(endpoint, params=None):
    if params is None: params = {}
    params["auth_token"] = get_token()
    try:
        r = requests.get(f"{API}{endpoint}", params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        b = ""
        try: b = r.text[:500]
        except: pass
        print(f"API Error {r.status_code}: {e}", file=sys.stderr)
        if b: print(f"Response: {b}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr); sys.exit(1)

def output_json(data):
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))

def cents_to_dollars(c):
    try: return round(float(c) / 100, 2)
    except: return 0.0
