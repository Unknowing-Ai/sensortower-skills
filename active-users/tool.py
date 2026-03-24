#!/usr/bin/env python3
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.api import api_get, output_json

def qau(ot, params):
    eo = "itunes" if ot == "ios" else ot
    try:
        data = api_get(f"/v1/{eo}/active_users", params)
        if isinstance(data, list): return [{"platform": ot, **r} for r in data]
        return [{"platform": ot, "data": data}]
    except SystemExit: return []

def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--app-id"); g.add_argument("--ios-id"); g.add_argument("--android-id")
    p.add_argument("--metric", default="DAU", choices=["DAU", "WAU", "MAU"])
    p.add_argument("--countries", required=True)
    p.add_argument("--start", required=True); p.add_argument("--end", required=True)
    a = p.parse_args()
    base = {"metric": a.metric.lower(), "countries": a.countries, "start_date": a.start, "end_date": a.end}
    results = []
    if a.app_id:
        for ot in ["ios", "android"]: results.extend(qau(ot, {**base, "app_id": a.app_id}))
    elif a.ios_id: results = qau("ios", {**base, "app_id": a.ios_id})
    else: results = qau("android", {**base, "app_id": a.android_id})
    output_json(results)

if __name__ == "__main__": main()
