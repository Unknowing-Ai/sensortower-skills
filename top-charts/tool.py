#!/usr/bin/env python3
import argparse, os, sys
from datetime import datetime, timedelta
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.api import api_get, output_json, cents_to_dollars

def main():
    td = datetime.now().strftime("%Y-%m-%d")
    a30 = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    p = argparse.ArgumentParser()
    p.add_argument("--measure", default="revenue", choices=["revenue", "units", "DAU", "WAU", "MAU"])
    p.add_argument("--countries", default="US"); p.add_argument("--category", default=None)
    p.add_argument("--limit", type=int, default=100)
    p.add_argument("--start", default=a30); p.add_argument("--end", default=td)
    p.add_argument("--os", default="unified", choices=["unified", "ios", "android"])
    a = p.parse_args()
    params = {"measure": a.measure, "countries": a.countries, "limit": a.limit, "start_date": a.start, "end_date": a.end}
    if a.category: params["category"] = a.category
    eo = "itunes" if a.os == "ios" else a.os
    data = api_get(f"/v1/{eo}/top_charts", params)
    results = []
    items = data if isinstance(data, list) else data.get("data", data.get("results", []))
    for i, item in enumerate(items, 1):
        e = {"rank": i, "app_name": item.get("app_name", item.get("name", "")), "app_id": item.get("unified_app_id", item.get("app_id", "")), "publisher": item.get("publisher_name", item.get("publisher", ""))}
        if a.measure == "revenue": e["revenue_usd"] = cents_to_dollars(item.get("revenue", item.get("r", 0)) or 0)
        elif a.measure == "units": e["downloads"] = item.get("downloads", item.get("units", item.get("u", 0))) or 0
        else: e[a.measure.lower()] = item.get(a.measure.lower(), item.get("active_users", 0)) or 0
        results.append(e)
    output_json(results)

if __name__ == "__main__": main()
