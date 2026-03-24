#!/usr/bin/env python3
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.api import api_get, output_json, cents_to_dollars

def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--app-id"); g.add_argument("--ios-id"); g.add_argument("--android-id")
    p.add_argument("--countries", required=True)
    p.add_argument("--start", required=True); p.add_argument("--end", required=True)
    p.add_argument("--granularity", default="monthly", choices=["daily", "weekly", "monthly"])
    a = p.parse_args()
    params = {"countries": a.countries, "start_date": a.start, "end_date": a.end, "date_granularity": a.granularity}
    if a.app_id: ot, params["unified_app_id"] = "unified", a.app_id
    elif a.ios_id: ot, params["app_id"] = "itunes", a.ios_id
    else: ot, params["app_id"] = "android", a.android_id
    data = api_get(f"/v1/{ot}/sales_report", params)
    results = []
    if isinstance(data, list):
        for r in data:
            e = {"date": r.get("d", r.get("date", "")), "country": r.get("cc", r.get("country_code", ""))}
            if ot == "unified":
                idl = (r.get("iu", 0) or 0) + (r.get("au", 0) or 0)
                adl = r.get("u", 0) or 0
                irv = (r.get("ir", 0) or 0) + (r.get("ar", 0) or 0)
                arv = r.get("r", 0) or 0
                e.update({"ios_downloads": idl, "android_downloads": adl, "total_downloads": idl + adl, "ios_revenue_usd": cents_to_dollars(irv), "android_revenue_usd": cents_to_dollars(arv), "total_revenue_usd": cents_to_dollars(irv + arv)})
            else:
                e.update({"downloads": r.get("u", r.get("units", 0)) or 0, "revenue_usd": cents_to_dollars(r.get("r", r.get("revenue", 0)) or 0)})
            results.append(e)
    else: results = data
    output_json(results)

if __name__ == "__main__": main()
