#!/usr/bin/env python3
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.api import api_get, output_json, cents_to_dollars

def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--app-id", help="iOS numeric ID or Android package name")
    g.add_argument("--publisher-id", help="Publisher ID")
    p.add_argument("--os", default="ios", choices=["ios", "android"])
    p.add_argument("--countries", required=True)
    p.add_argument("--start", required=True); p.add_argument("--end", required=True)
    p.add_argument("--granularity", default="monthly", choices=["daily", "weekly", "monthly", "quarterly"])
    a = p.parse_args()

    # Build URL with array param manually
    token_mod = __import__("common.api", fromlist=["get_token"])
    token = token_mod.get_token()
    import requests, json
    url = f"https://api.sensortower.com/v1/{a.os}/sales_report_estimates"
    params = {
        "auth_token": token,
        "date_granularity": a.granularity,
        "start_date": a.start,
        "end_date": a.end,
    }
    # countries as array
    for c in a.countries.split(","):
        params.setdefault("countries[]", [])
        if not isinstance(params.get("countries[]"), list):
            params["countries[]"] = [params["countries[]"]]
        params["countries[]"] = a.countries.split(",")
    # app_ids or publisher_ids as array
    if a.app_id:
        params["app_ids[]"] = a.app_id
    else:
        params["publisher_ids[]"] = a.publisher_id

    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        try: print(f"Response: {r.text[:500]}", file=sys.stderr)
        except: pass
        sys.exit(1)

    results = []
    if isinstance(data, list):
        for r in data:
            results.append({
                "app_id": r.get("aid", ""),
                "country": r.get("cc", ""),
                "date": r.get("d", ""),
                "iphone_downloads": r.get("iu", 0) or 0,
                "ipad_downloads": r.get("au", 0) or 0,
                "iphone_revenue_usd": cents_to_dollars(r.get("ir", 0) or 0),
                "ipad_revenue_usd": cents_to_dollars(r.get("ar", 0) or 0),
                "android_downloads": r.get("u", 0) or 0,
                "android_revenue_usd": cents_to_dollars(r.get("r", 0) or 0),
            })
    output_json(results)

if __name__ == "__main__": main()
