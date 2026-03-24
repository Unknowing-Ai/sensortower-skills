#!/usr/bin/env python3
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.api import api_get, output_json

def main():
    p = argparse.ArgumentParser(description="Search Sensor Tower")
    p.add_argument("--term", required=True)
    p.add_argument("--type", default="app", choices=["app", "publisher"])
    p.add_argument("--os", default="unified", choices=["unified", "ios", "android"])
    p.add_argument("--limit", type=int, default=10)
    a = p.parse_args()
    data = api_get(f"/v1/{a.os}/search_entities", {"term": a.term, "entity_type": a.type, "limit": a.limit})
    results = []
    items = data if isinstance(data, list) else data.get("data", data.get("results", [data] if isinstance(data, dict) else []))
    for item in items:
        if a.type == "publisher":
            results.append({"unified_publisher_id": item.get("unified_publisher_id", item.get("publisher_id", "")), "name": item.get("unified_publisher_name", item.get("name", ""))})
        else:
            results.append({"unified_app_id": item.get("unified_app_id", item.get("app_id", "")), "name": item.get("unified_app_name", item.get("name", item.get("app_name", ""))), "publisher": item.get("publisher_name", item.get("publisher", ""))})
    output_json(results)

if __name__ == "__main__": main()
