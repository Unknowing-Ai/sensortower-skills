#!/usr/bin/env python3
import argparse, os, sys
from datetime import datetime, timedelta
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.api import api_get, output_json

def main():
    td = datetime.now().strftime("%Y-%m-%d")
    a30 = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    p = argparse.ArgumentParser()
    p.add_argument("--action", required=True, choices=["overview", "top-advertisers", "creatives"])
    p.add_argument("--app-id"); p.add_argument("--countries", default="US")
    p.add_argument("--category"); p.add_argument("--limit", type=int, default=20)
    p.add_argument("--start", default=a30); p.add_argument("--end", default=td)
    p.add_argument("--networks")
    a = p.parse_args()
    if a.action in ("overview", "creatives") and not a.app_id:
        print(f"Error: --app-id required for {a.action}", file=sys.stderr); sys.exit(1)
    params = {"start_date": a.start, "end_date": a.end, "countries": a.countries, "limit": a.limit}
    if a.app_id: params["app_id"] = a.app_id
    if a.category: params["category"] = a.category
    if a.networks: params["networks"] = a.networks
    eps = {"overview": "/v1/unified/ad_intel/overview", "top-advertisers": "/v1/unified/ad_intel/top_advertisers", "creatives": "/v1/unified/ad_intel/creatives"}
    output_json(api_get(eps[a.action], params))

if __name__ == "__main__": main()
