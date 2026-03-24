#!/usr/bin/env python3
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.api import api_get, output_json

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--publisher-id", required=True)
    p.add_argument("--os", default="unified", choices=["unified", "ios", "android"])
    a = p.parse_args()
    eo = "itunes" if a.os == "ios" else a.os
    data = api_get(f"/v1/{eo}/publisher_apps", {"publisher_id": a.publisher_id})
    items = data if isinstance(data, list) else data.get("data", data.get("apps", []))
    results = [{"unified_app_id": i.get("unified_app_id", i.get("app_id", "")), "name": i.get("app_name", i.get("name", "")), "os": i.get("os", ""), "category": i.get("category", "")} for i in items]
    output_json(results)

if __name__ == "__main__": main()
