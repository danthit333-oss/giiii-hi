import urllib.request
import json
import os

key_path = r"d:\A\A_5chai\honey_pot\part_08_DOCKER_DEPLOYMENT\secrets\part3_analyst_api_key.txt"
with open(key_path, "r", encoding="utf-8") as f:
    key = f.read().strip()

req = urllib.request.Request(
    "http://127.0.0.1:8088/api/v1/events?limit=15",
    headers={"X-API-Key": key}
)

with urllib.request.urlopen(req, timeout=5) as resp:
    data = json.loads(resp.read().decode())
    print("Total items returned:", len(data.get("items", [])))
    for it in data.get("items", [])[:10]:
        print(f"ID: {it.get('id')} | Sensor: {it.get('sensor_id')} | Vuln: {it.get('vulnerability')} | Sev: {it.get('severity')} | Path: {it.get('path')} | Hash: {it.get('event_sha256')[:12]}...")
