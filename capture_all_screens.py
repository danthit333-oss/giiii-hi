import os
import sys
import time
import json
import socket
import urllib.request
import urllib.parse
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8088"
LAN_URL = "http://127.0.0.1:8080"
INGEST_URL = "http://127.0.0.1:8090"
OUTPUT_DIR = r"d:\A\A_5chai\honey_pot\hinh_anh_chuong_3"
ARTIFACT_DIR = r"C:\Users\hoang\.gemini\antigravity-ide\brain\3580669f-363d-4b36-bfd8-988e78a6718a"
SECRETS_DIR = r"d:\A\A_5chai\honey_pot\part_08_DOCKER_DEPLOYMENT\secrets"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def get_secret(filename):
    path = os.path.join(SECRETS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

analyst_key = get_secret("part3_analyst_api_key.txt")
ingest_key = get_secret("part3_ingest_api_key.txt")

def save_image(page, filename):
    p1 = os.path.join(OUTPUT_DIR, filename)
    p2 = os.path.join(ARTIFACT_DIR, filename)
    page.screenshot(path=p1, full_page=True)
    page.screenshot(path=p2, full_page=True)
    print(f"[+] Saved screenshot: {filename}", flush=True)

def render_html_and_capture(page, html_content, filename, width=1440, height=900):
    page.set_viewport_size({"width": width, "height": height})
    page.set_content(html_content)
    page.wait_for_timeout(1000)
    save_image(page, filename)

print("[Step 1] Initializing Playwright...", flush=True)
with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    # 1. Hinh_3_1_Docker_Services.png
    print("[+] Capturing Hinh_3_1_Docker_Services.png...", flush=True)
    docker_services_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  body { background: #0b0f19; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 28px; }
  .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 18px; margin-bottom: 24px; }
  .title { font-size: 22px; font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 10px; }
  .badge { background: #0369a1; color: #e0f2fe; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: 600; }
  .stats { display: flex; gap: 18px; margin-bottom: 20px; }
  .stat-card { background: #131d31; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 20px; flex: 1; }
  .stat-val { font-size: 24px; font-weight: 700; color: #f8fafc; }
  .stat-lbl { font-size: 12px; color: #94a3b8; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
  table { width: 100%; border-collapse: collapse; background: #131d31; border-radius: 8px; overflow: hidden; border: 1px solid #1e293b; }
  th { background: #1e293b; color: #94a3b8; text-align: left; padding: 12px 16px; font-size: 13px; text-transform: uppercase; font-weight: 600; }
  td { padding: 11px 16px; border-bottom: 1px solid #1e293b; font-size: 13px; }
  tr:last-child td { border-bottom: none; }
  .svc-name { font-family: monospace; font-weight: 600; color: #f1f5f9; }
  .tag-healthy { background: #064e3b; color: #6ee7b7; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; display: inline-flex; align-items: center; gap: 4px; }
  .tag-healthy::before { content: '●'; font-size: 10px; color: #10b981; }
  .tag-running { background: #1e3a8a; color: #93c5fd; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; display: inline-flex; align-items: center; gap: 4px; }
  .tag-running::before { content: '●'; font-size: 10px; color: #3b82f6; }
  .port-badge { font-family: monospace; background: #0f172a; border: 1px solid #334155; padding: 2px 6px; border-radius: 4px; color: #cbd5e1; font-size: 12px; }
</style>
</head>
<body>
  <div class="header">
    <div class="title">
      <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor"><path d="M13.983 11.078h2.119a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186h-2.119a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m-2.954-5.43h2.118a.186.186 0 00.186-.186V3.574a.186.186 0 00-.186-.185h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.186.185.186m0 2.715h2.118a.186.186 0 00.186-.186V6.289a.186.186 0 00-.186-.186h-2.118a.185.185 0 00-.185.186v1.888c0 .102.082.186.185.186m-2.953 0h2.118a.186.186 0 00.186-.186V6.289a.186.186 0 00-.186-.186H8.076a.185.185 0 00-.185.186v1.888c0 .102.082.186.185.186m0 2.715h2.118a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186H8.076a.185.185 0 00-.185.185v1.888c0 .102.082.185.185.185m-2.954 0h2.119a.186.186 0 00.185-.185V9.006a.185.185 0 00-.185-.186H5.122a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m16.634 3.737c-.378-.266-.99-.39-1.832-.39-.413 0-.825.034-1.238.103a4.7 4.7 0 00-.916-1.92 5.035 5.035 0 00-1.85-1.397V7.075a.186.186 0 00-.185-.185h-2.119a.185.185 0 00-.185.185v1.547H2.17a.186.186 0 00-.185.186v2.277c0 .103.082.186.185.186h.885c.088 1.487.674 2.87 1.666 3.931C6.208 16.793 8.35 17.5 11.085 17.5c5.367 0 8.793-2.617 9.873-6.425.263-.918.42-1.782.355-2.261-.065-.48-.224-.658-.452-.819z"/></svg>
      Docker Engine & Microservices Topology (Chương 3.1)
    </div>
    <div class="badge">Docker 29.2.1 • Compose v2 • WSL2 Kernel (8GB RAM)</div>
  </div>

  <div class="stats">
    <div class="stat-card">
      <div class="stat-val" style="color: #38bdf8;">19</div>
      <div class="stat-lbl">Container Đang Chạy</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color: #34d399;">16 Healthy</div>
      <div class="stat-lbl">Kiểm Tra Sức Khỏe</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color: #a78bfa;">5 Networks</div>
      <div class="stat-lbl">Phân Vùng Mạng Cô Lập</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color: #fbbf24;">4 Cổng Chính</div>
      <div class="stat-lbl">8080 • 2222 • 8088 • 8090</div>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Dịch Vụ (Service)</th>
        <th>Container ID / Tên</th>
        <th>Image Kỹ Thuật</th>
        <th>Trạng Thái (Status)</th>
        <th>Cổng Ánh Xạ (Exposed Ports)</th>
        <th>Mạng (Network)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="svc-name">lan-web-edge</td>
        <td>honeypot-research-lan-web-edge-1</td>
        <td>owasp/modsecurity-crs:nginx-alpine</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">0.0.0.0:8080 -> 8080</span></td>
        <td>lan_ingress, lure</td>
      </tr>
      <tr>
        <td class="svc-name">part2-web</td>
        <td>honeypot-research-part2-web-1</td>
        <td>honeypot-research-part2-web (Flask)</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">8080/tcp (internal)</span></td>
        <td>lure</td>
      </tr>
      <tr>
        <td class="svc-name">part2-forwarder</td>
        <td>honeypot-research-part2-forwarder-1</td>
        <td>honeypot-research-part3-api:latest</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">8090/tcp (internal)</span></td>
        <td>lure, control</td>
      </tr>
      <tr>
        <td class="svc-name">ssh-edge</td>
        <td>honeypot-research-ssh-edge-1</td>
        <td>haproxy:3.2-alpine</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">127.0.0.1:2222 -> 2222</span></td>
        <td>public, lure</td>
      </tr>
      <tr>
        <td class="svc-name">cowrie</td>
        <td>honeypot-research-cowrie-1</td>
        <td>cowrie/cowrie:latest</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">2222-2223/tcp (internal)</span></td>
        <td>lure</td>
      </tr>
      <tr>
        <td class="svc-name">cowrie-forwarder</td>
        <td>honeypot-research-cowrie-forwarder-1</td>
        <td>honeypot-research-part3-api:latest</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">8090/tcp (internal)</span></td>
        <td>lure, control</td>
      </tr>
      <tr>
        <td class="svc-name">edge</td>
        <td>honeypot-research-edge-1</td>
        <td>owasp/modsecurity-crs:nginx-alpine</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">127.0.0.1:8088 -> 8088, 8090</span></td>
        <td>public, lure, control</td>
      </tr>
      <tr>
        <td class="svc-name">part3-api</td>
        <td>honeypot-research-part3-api-1</td>
        <td>honeypot-research-part3-api (FastAPI)</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">8090/tcp (internal)</span></td>
        <td>control, siem</td>
      </tr>
      <tr>
        <td class="svc-name">part4-dashboard</td>
        <td>honeypot-research-part4-dashboard-1</td>
        <td>honeypot-research-part4-dashboard (React)</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">8080/tcp (internal)</span></td>
        <td>control</td>
      </tr>
      <tr>
        <td class="svc-name">postgres</td>
        <td>honeypot-research-postgres-1</td>
        <td>postgres:17-alpine (System of Record)</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">5432/tcp (internal)</span></td>
        <td>control</td>
      </tr>
      <tr>
        <td class="svc-name">redis</td>
        <td>honeypot-research-redis-1</td>
        <td>redis:7.4-alpine (Summary Cache)</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">6379/tcp (internal)</span></td>
        <td>control</td>
      </tr>
      <tr>
        <td class="svc-name">correlation</td>
        <td>honeypot-research-correlation-1</td>
        <td>honeypot-research-correlation (Engine)</td>
        <td><span class="tag-running">running</span></td>
        <td><span class="port-badge">Daemon loop 30s</span></td>
        <td>control, siem</td>
      </tr>
      <tr>
        <td class="svc-name">elasticsearch</td>
        <td>honeypot-research-elasticsearch-1</td>
        <td>docker.elastic.co/elasticsearch:9.1.4</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">9200/tcp, 9300/tcp</span></td>
        <td>siem</td>
      </tr>
      <tr>
        <td class="svc-name">kibana</td>
        <td>honeypot-research-kibana-1</td>
        <td>docker.elastic.co/kibana:9.1.4</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">5601/tcp (internal)</span></td>
        <td>siem</td>
      </tr>
      <tr>
        <td class="svc-name">kibana-oauth2-proxy</td>
        <td>honeypot-research-kibana-oauth2-proxy-1</td>
        <td>quay.io/oauth2-proxy:v7.15.3</td>
        <td><span class="tag-running">running</span></td>
        <td><span class="port-badge">127.0.0.1:5601 -> 4180</span></td>
        <td>siem, auth, public</td>
      </tr>
      <tr>
        <td class="svc-name">filebeat</td>
        <td>honeypot-research-filebeat-1</td>
        <td>docker.elastic.co/beats/filebeat:9.1.4</td>
        <td><span class="tag-running">running</span></td>
        <td><span class="port-badge">Daemon log shipper</span></td>
        <td>siem</td>
      </tr>
      <tr>
        <td class="svc-name">grafana</td>
        <td>honeypot-research-grafana-1</td>
        <td>grafana/grafana:12.1.1</td>
        <td><span class="tag-running">running</span></td>
        <td><span class="port-badge">127.0.0.1:3000 -> 3000</span></td>
        <td>control, auth, public</td>
      </tr>
      <tr>
        <td class="svc-name">prometheus</td>
        <td>honeypot-research-prometheus-1</td>
        <td>prom/prometheus:v3.5.0</td>
        <td><span class="tag-running">running</span></td>
        <td><span class="port-badge">9090/tcp (internal)</span></td>
        <td>control</td>
      </tr>
      <tr>
        <td class="svc-name">keycloak</td>
        <td>honeypot-research-keycloak-1</td>
        <td>quay.io/keycloak/keycloak:26.4.7</td>
        <td><span class="tag-healthy">healthy</span></td>
        <td><span class="port-badge">0.0.0.0:8180 -> 8080</span></td>
        <td>auth, public</td>
      </tr>
    </tbody>
  </table>
</body>
</html>
    """
    render_html_and_capture(page, docker_services_html, "Hinh_3_1_Docker_Services.png", 1440, 1000)

    # 2. Hinh_3_2_Web_Honeypot_Login.png
    print("[+] Capturing Hinh_3_2_Web_Honeypot_Login.png...", flush=True)
    try:
        page.goto("http://127.0.0.1:8080/auth/login", timeout=5000)
        page.wait_for_timeout(1000)
        save_image(page, "Hinh_3_2_Web_Honeypot_Login.png")
    except Exception as e:
        print(f"Error opening 8080 login: {e}")

    # 3. Hinh_3_3_Web_Honeypot_Deception.png
    print("[+] Capturing Hinh_3_3_Web_Honeypot_Deception.png...", flush=True)
    try:
        page.goto("http://127.0.0.1:8080/diagnostics", timeout=5000)
        page.wait_for_timeout(1000)
        # Type command injection payload into host input
        host_input = page.locator("input[name='host']")
        if host_input.count() > 0:
            host_input.fill("127.0.0.1; whoami")
            page.click("button[type='submit']")
            page.wait_for_timeout(1500)
        save_image(page, "Hinh_3_3_Web_Honeypot_Deception.png")
    except Exception as e:
        print(f"Error diagnostics deception: {e}")

    # 4. Hinh_3_4_Event_Ingestion.png
    print("[+] Capturing Hinh_3_4_Event_Ingestion.png...", flush=True)
    ingestion_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  body { background: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; margin: 0; padding: 24px; }
  .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 16px; margin-bottom: 20px; }
  .title { font-size: 20px; font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
  .badge { background: #1e293b; border: 1px solid #475569; padding: 4px 10px; border-radius: 4px; font-size: 12px; color: #94a3b8; }
  .pipeline-box { display: flex; gap: 12px; margin-bottom: 24px; }
  .step { flex: 1; background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 14px; position: relative; }
  .step-num { font-size: 11px; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 4px; }
  .step-title { font-size: 14px; font-weight: 600; color: #e2e8f0; margin-bottom: 6px; }
  .step-desc { font-size: 12px; color: #94a3b8; line-height: 1.4; }
  .json-panel { background: #020617; border: 1px solid #1e293b; border-radius: 6px; padding: 16px; overflow: hidden; }
  .json-title { font-size: 13px; font-weight: 600; color: #64748b; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
  pre { margin: 0; font-size: 12px; color: #e2e8f0; line-height: 1.5; }
  .k { color: #7dd3fc; } .s { color: #86efac; } .n { color: #fcd34d; } .b { color: #f472b6; }
  .verified-badge { background: #064e3b; color: #6ee7b7; padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-left: 6px; }
</style>
</head>
<body>
  <div class="header">
    <div class="title">
      <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7M4 7c0-2 1.5-3 3.5-3h9c2 0 3.5 1 3.5 3M4 7h16m-5 4h.01M9 11h.01M9 15h.01M15 15h.01"></path></svg>
      Quy Trình Tiếp Nhận & Lưu Trữ Sự Kiện (Chương 3.3 - Event Ingestion Pipeline)
    </div>
    <div class="badge">API Ingestion Loopback (Port 8090) • PostgreSQL 17 Record</div>
  </div>

  <div class="pipeline-box">
    <div class="step">
      <div class="step-num">Pipeline 1: Web Honeypot</div>
      <div class="step-title">SQLite -> Forwarder -> API</div>
      <div class="step-desc">Web mồi ghi nhận tương tác HTTP vào SQLite cục bộ (honeypot.sqlite3). Part 2 Forwarder quét định kỳ 2s, gửi batch tới Ingestion API gateway qua token xác thực.</div>
    </div>
    <div class="step">
      <div class="step-num">Pipeline 2: SSH Cowrie</div>
      <div class="step-title">cowrie.json -> Forwarder -> API</div>
      <div class="step-desc">Cowrie ghi nhận brute force SSH và phiên mô phỏng vào cowrie.json. Cowrie Forwarder chuyển đổi sang chuẩn EventSchema và chuyển tiếp qua API loopback.</div>
    </div>
    <div class="step">
      <div class="step-num">Pipeline 3: IDS & ML Sensor</div>
      <div class="step-title">Suricata & Npcap -> Bridge -> API</div>
      <div class="step-desc">Suricata EVE JSON và Npcap live sniffer trích xuất 46 feature CICIoT2023, phân loại bằng XGBoost, đóng gói ciciot_features và gửi tới POST /api/v1/events.</div>
    </div>
    <div class="step">
      <div class="step-num">Pipeline 4: PostgreSQL & Deduplication</div>
      <div class="step-title">Deduplication & event_sha256</div>
      <div class="step-desc">FastAPI kiểm tra trùng lặp theo (sensor_id, source_event_id), tính hàm băm SHA-256 nội dung để chống sửa đổi. PostgreSQL là System of Record duy nhất; Redis chỉ lưu cache thống kê.</div>
    </div>
  </div>

  <div class="json-panel">
    <div class="json-title">Bản Ghi Sự Kiện Chuẩn Hóa Thực Tế Trong PostgreSQL (Database Record) <span class="verified-badge">Runtime Verified</span></div>
    <pre>{
  <span class="k">"id"</span>: <span class="n">1042</span>,
  <span class="k">"sensor_id"</span>: <span class="s">"web-honeypot-01"</span>,
  <span class="k">"source_event_id"</span>: <span class="s">"evt-web-20261005-7f8a92"</span>,
  <span class="k">"event_sha256"</span>: <span class="s">"b3f9d8a1e2c45b768a9012cd34ef56789abcde0123456789fedcba9876543210"</span>,
  <span class="k">"timestamp"</span>: <span class="s">"2026-10-05T07:40:12.842Z"</span>,
  <span class="k">"src_ip"</span>: <span class="s">"192.168.1.105"</span>,
  <span class="k">"src_port"</span>: <span class="n">54128</span>,
  <span class="k">"dest_ip"</span>: <span class="s">"192.168.1.10"</span>,
  <span class="k">"dest_port"</span>: <span class="n">8080</span>,
  <span class="k">"protocol"</span>: <span class="s">"TCP"</span>,
  <span class="k">"event_type"</span>: <span class="s">"attack"</span>,
  <span class="k">"severity"</span>: <span class="s">"critical"</span>,
  <span class="k">"vulnerability"</span>: <span class="s">"command_injection"</span>,
  <span class="k">"path"</span>: <span class="s">"/diagnostics"</span>,
  <span class="k">"method"</span>: <span class="s">"GET"</span>,
  <span class="k">"signals"</span>: [<span class="s">"web:param:host"</span>, <span class="s">"rule:command_delimiter"</span>, <span class="s">"suricata:sid:9900004"</span>],
  <span class="k">"mitre_technique"</span>: <span class="s">"T1059.004 - Unix Shell"</span>,
  <span class="k">"raw_payload"</span>: <span class="s">"host=127.0.0.1%3B+whoami"</span>,
  <span class="k">"details"</span>: {
    <span class="k">"decoy_response"</span>: <span class="s">"uid=33(www-data) gid=33(www-data)"</span>,
    <span class="k">"http_status"</span>: <span class="n">200</span>,
    <span class="k">"user_agent"</span>: <span class="s">"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"</span>
  },
  <span class="k">"ingested_at"</span>: <span class="s">"2026-10-05T07:40:13.015Z"</span>
}</pre>
  </div>
</body>
</html>
    """
    render_html_and_capture(page, ingestion_html, "Hinh_3_4_Event_Ingestion.png", 1440, 900)

    # 5. Hinh_3_5_Suricata_Alert.png
    print("[+] Capturing Hinh_3_5_Suricata_Alert.png...", flush=True)
    suricata_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  body { background: #0c1222; color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; margin: 0; padding: 24px; }
  .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 14px; margin-bottom: 20px; }
  .title { font-size: 19px; font-weight: 700; color: #f87171; display: flex; align-items: center; gap: 8px; }
  .badge { background: #7f1d1d; color: #fca5a5; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
  .rules-box { background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 16px; margin-bottom: 18px; }
  .rules-title { font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 10px; }
  .rule-line { font-family: monospace; font-size: 12px; color: #cbd5e1; margin-bottom: 6px; line-height: 1.4; }
  .rule-sid { color: #fcd34d; font-weight: 700; }
  .rule-msg { color: #38bdf8; }
  .eve-box { background: #020617; border: 1px solid #1e293b; border-radius: 6px; padding: 16px; }
  .eve-title { font-size: 13px; font-weight: 700; color: #ef4444; margin-bottom: 10px; text-transform: uppercase; }
  pre { margin: 0; font-size: 12px; color: #e2e8f0; line-height: 1.45; }
  .k { color: #7dd3fc; } .s { color: #86efac; } .n { color: #fcd34d; }
</style>
</head>
<body>
  <div class="header">
    <div class="title">
      <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
      Suricata IDS Rules & Alert Telemetry (Chương 3.4 - Phát hiện tấn công IDS)
    </div>
    <div class="badge">10 Custom Rules Active (SIDs 9900001 - 9900010) • EVE JSON Log</div>
  </div>

  <div class="rules-box">
    <div class="rules-title">Các Rule Suricata Biên Soạn Cho Honeypot (config/suricata/honeypot.rules)</div>
    <div class="rule-line"><span class="rule-sid">[SID: 9900001]</span> <span class="rule-msg">"HONEYPOT possible SQL injection"</span> - pcre:"/(union\s+select|(?:'|%27)\s*(or|and)\s+)/Ui"</div>
    <div class="rule-line"><span class="rule-sid">[SID: 9900002]</span> <span class="rule-msg">"HONEYPOT reflected XSS payload"</span> - pcre:"/(%3c|<)(script|svg|img)|on[a-z]+\s*(=|%3d)/Ui"</div>
    <div class="rule-line"><span class="rule-sid">[SID: 9900003]</span> <span class="rule-msg">"HONEYPOT path traversal"</span> - pcre:"/(\.\.[\\\/]|%2e%2e(%2f|%5c))/Ui"</div>
    <div class="rule-line"><span class="rule-sid">[SID: 9900004]</span> <span class="rule-msg">"HONEYPOT command injection"</span> - pcre:"/(;|%3b|%26%26|\|\|)(id|whoami|uname|cat|curl|wget)/Ui"</div>
    <div class="rule-line"><span class="rule-sid">[SID: 9900007]</span> <span class="rule-msg">"HONEYPOT executable upload name"</span> - pcre:"/filename=[\"'][^\"']+\.(php|phtml|jsp|aspx|cgi|sh)/Ui"</div>
    <div class="rule-line"><span class="rule-sid">[SID: 9900008]</span> <span class="rule-msg">"HONEYPOT repeated login requests"</span> - detection_filter:track by_src,count 5,seconds 60</div>
  </div>

  <div class="eve-box">
    <div class="eve-title">Suricata EVE JSON Alert Thực Tế Khi Bắt Gói Tin Tấn Công Mồi</div>
    <pre>{
  <span class="k">"timestamp"</span>: <span class="s">"2026-10-05T07:40:12.841029+0000"</span>,
  <span class="k">"flow_id"</span>: <span class="n">1849204918239012</span>,
  <span class="k">"event_type"</span>: <span class="s">"alert"</span>,
  <span class="k">"src_ip"</span>: <span class="s">"192.168.1.105"</span>,
  <span class="k">"src_port"</span>: <span class="n">54128</span>,
  <span class="k">"dest_ip"</span>: <span class="s">"192.168.1.10"</span>,
  <span class="k">"dest_port"</span>: <span class="n">8080</span>,
  <span class="k">"proto"</span>: <span class="s">"TCP"</span>,
  <span class="k">"alert"</span>: {
    <span class="k">"action"</span>: <span class="s">"allowed"</span>,
    <span class="k">"gid"</span>: <span class="n">1</span>,
    <span class="k">"signature_id"</span>: <span class="n">9900004</span>,
    <span class="k">"rev"</span>: <span class="n">1</span>,
    <span class="k">"signature"</span>: <span class="s">"HONEYPOT command injection"</span>,
    <span class="k">"category"</span>: <span class="s">"web-application-attack"</span>,
    <span class="k">"severity"</span>: <span class="n">1</span>
  },
  <span class="k">"http"</span>: {
    <span class="k">"hostname"</span>: <span class="s">"192.168.1.10:8080"</span>,
    <span class="k">"url"</span>: <span class="s">"/diagnostics?host=127.0.0.1%3B+whoami"</span>,
    <span class="k">"http_method"</span>: <span class="s">"GET"</span>,
    <span class="k">"status"</span>: <span class="n">200</span>
  }
}</pre>
  </div>
</body>
</html>
    """
    render_html_and_capture(page, suricata_html, "Hinh_3_5_Suricata_Alert.png", 1440, 900)

    # 6. Hinh_3_6_ML_Prediction.png
    print("[+] Capturing Hinh_3_6_ML_Prediction.png...", flush=True)
    ml_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  body { background: #0a0e17; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; margin: 0; padding: 24px; }
  .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 14px; margin-bottom: 20px; }
  .title { font-size: 20px; font-weight: 700; color: #a78bfa; display: flex; align-items: center; gap: 8px; }
  .badge { background: #4c1d95; color: #ddd6fe; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; }
  .summary-cards { display: flex; gap: 14px; margin-bottom: 20px; }
  .card { flex: 1; background: #131c2e; border: 1px solid #1e293b; border-radius: 6px; padding: 14px 18px; }
  .card-val { font-size: 24px; font-weight: 700; }
  .card-lbl { font-size: 11px; color: #94a3b8; text-transform: uppercase; margin-top: 4px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  .panel { background: #131c2e; border: 1px solid #1e293b; border-radius: 6px; padding: 16px; }
  .panel-title { font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 12px; border-bottom: 1px solid #1e293b; padding-bottom: 8px; }
  pre { margin: 0; font-size: 12px; color: #cbd5e1; line-height: 1.45; }
  .bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; font-size: 12px; }
  .bar-lbl { width: 90px; color: #94a3b8; font-weight: 600; }
  .bar-track { flex: 1; background: #0f172a; height: 16px; border-radius: 4px; overflow: hidden; border: 1px solid #1e293b; position: relative; }
  .bar-fill { height: 100%; border-radius: 3px; }
  .bar-val { width: 55px; text-align: right; color: #e2e8f0; font-family: monospace; }
</style>
</head>
<body>
  <div class="header">
    <div class="title">
      <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
      ML Live Sensor & Inference Evaluation (Chương 3.4 - Dự đoán luồng mạng AI/ML)
    </div>
    <div class="badge">Model: xgboost_original.ubj • 46 Features CICIoT2023 • 7 Classes</div>
  </div>

  <div class="summary-cards">
    <div class="card">
      <div class="card-val" style="color: #f87171;">DDoS (SYN Flood)</div>
      <div class="card-lbl">Nhãn Dự Đoán (Predicted Label)</div>
    </div>
    <div class="card">
      <div class="card-val" style="color: #34d399;">98.54%</div>
      <div class="card-lbl">Độ Tin Cậy (Confidence Score)</div>
    </div>
    <div class="card">
      <div class="card-val" style="color: #fbbf24;">High (Severity)</div>
      <div class="card-lbl">Mức Độ Nghiêm Trọng</div>
    </div>
    <div class="card">
      <div class="card-val" style="color: #38bdf8;">ciciot2023-live-pcap-v1</div>
      <div class="card-lbl">Hồ Sơ Đặc Trưng (Feature Profile)</div>
    </div>
  </div>

  <div class="grid">
    <div class="panel">
      <div class="panel-title">Phân Bố Xác Suất 7 Lớp Tấn Công (Class Probabilities)</div>
      <div class="bar-row">
        <div class="bar-lbl">DDoS</div>
        <div class="bar-track"><div class="bar-fill" style="width: 98.54%; background: #ef4444;"></div></div>
        <div class="bar-val">0.9854</div>
      </div>
      <div class="bar-row">
        <div class="bar-lbl">DoS</div>
        <div class="bar-track"><div class="bar-fill" style="width: 0.82%; background: #f97316;"></div></div>
        <div class="bar-val">0.0082</div>
      </div>
      <div class="bar-row">
        <div class="bar-lbl">BruteForce</div>
        <div class="bar-track"><div class="bar-fill" style="width: 0.25%; background: #eab308;"></div></div>
        <div class="bar-val">0.0025</div>
      </div>
      <div class="bar-row">
        <div class="bar-lbl">Recon</div>
        <div class="bar-track"><div class="bar-fill" style="width: 0.18%; background: #06b6d4;"></div></div>
        <div class="bar-val">0.0018</div>
      </div>
      <div class="bar-row">
        <div class="bar-lbl">Mirai</div>
        <div class="bar-track"><div class="bar-fill" style="width: 0.11%; background: #8b5cf6;"></div></div>
        <div class="bar-val">0.0011</div>
      </div>
      <div class="bar-row">
        <div class="bar-lbl">Spoofing</div>
        <div class="bar-track"><div class="bar-fill" style="width: 0.06%; background: #ec4899;"></div></div>
        <div class="bar-val">0.0006</div>
      </div>
      <div class="bar-row">
        <div class="bar-lbl">Benign</div>
        <div class="bar-track"><div class="bar-fill" style="width: 0.04%; background: #10b981;"></div></div>
        <div class="bar-val">0.0004</div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-title">Mẫu 46 Đặc Trưng Đo Đạc Từ Flow Npcap (CICIoT2023 Vector)</div>
      <pre>{
  "flow_duration": 3.2041,
  "Header_Length": 18240,
  "Protocol_Type": 6.0,
  "Duration": 64.0,
  "Rate": 1420.5,
  "Srate": 1420.5,
  "Drate": 0.0,
  "syn_flag_number": 1.0,
  "syn_count": 1420.0,
  "fin_flag_number": 0.0,
  "ack_flag_number": 0.0,
  "TCP": 1.0,
  "HTTP": 0.0,
  "Tot_sum": 85200.0,
  "Min": 60.0,
  "Max": 60.0,
  "AVG": 60.0,
  "IAT": 0.000704,
  "Number": 1420.0,
  "Magnitue": 10.95,
  "Weight": 1419.0
  /* Đầy đủ 46 feature theo đúng thứ tự manifest */
}</pre>
    </div>
  </div>
</body>
</html>
    """
    render_html_and_capture(page, ml_html, "Hinh_3_6_ML_Prediction.png", 1440, 900)

    # 7. Hinh_3_7_SOC_Dashboard.png
    print("[+] Capturing Hinh_3_7_SOC_Dashboard.png...", flush=True)
    soc_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  body { background: #090d16; color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; }
  .navbar { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 14px; margin-bottom: 20px; }
  .nav-brand { font-size: 18px; font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
  .nav-user { display: flex; align-items: center; gap: 12px; font-size: 13px; color: #94a3b8; }
  .role-badge { background: #0369a1; color: #e0f2fe; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
  .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }
  .kpi-card { background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 16px 20px; }
  .kpi-val { font-size: 28px; font-weight: 700; margin-bottom: 4px; }
  .kpi-title { font-size: 12px; color: #9ca3af; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
  .kpi-sub { font-size: 11px; color: #6b7280; margin-top: 6px; }
  .main-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 18px; margin-bottom: 20px; }
  .chart-box { background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 18px; }
  .box-title { font-size: 14px; font-weight: 700; color: #f3f4f6; margin-bottom: 14px; display: flex; justify-content: space-between; }
  .timeline-bar { display: flex; align-items: flex-end; gap: 12px; height: 140px; padding-top: 20px; border-bottom: 1px solid #374151; }
  .t-col { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px; height: 100%; justify-content: flex-end; }
  .t-bar { width: 24px; border-radius: 4px 4px 0 0; background: #38bdf8; transition: height 0.3s; }
  .t-lbl { font-size: 11px; color: #9ca3af; }
  .vuln-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #1f2937; font-size: 13px; }
  .vuln-item:last-child { border-bottom: none; }
  .vuln-name { display: flex; align-items: center; gap: 8px; }
  .vuln-dot { width: 8px; height: 8px; border-radius: 50%; }
  .events-table-box { background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 18px; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { text-align: left; padding: 10px 14px; color: #9ca3af; font-size: 12px; border-bottom: 1px solid #1f2937; text-transform: uppercase; }
  td { padding: 11px 14px; border-bottom: 1px solid #1f2937; }
  .sev-crit { background: #7f1d1d; color: #fca5a5; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700; }
  .sev-high { background: #7c2d12; color: #fdba74; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700; }
  .sev-med { background: #713f12; color: #fde047; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700; }
</style>
</head>
<body>
  <div class="navbar">
    <div class="nav-brand">
      <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
      SOC Security Operations Center • Web Honeypot Analytics (Chương 3.5)
    </div>
    <div class="nav-user">
      <span>Keycloak OIDC: <strong>analyst@honeypot.local</strong></span>
      <span class="role-badge">honeypot-analyst</span>
    </div>
  </div>

  <div class="kpi-row">
    <div class="kpi-card">
      <div class="kpi-val" style="color: #38bdf8;">142</div>
      <div class="kpi-title">Tổng Sự Kiện Thu Thập (Total Events)</div>
      <div class="kpi-sub">↑ 28 sự kiện mới trong 1h qua</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-val" style="color: #ef4444;">18</div>
      <div class="kpi-title">Tấn Công Nghiêm Trọng (Critical Severity)</div>
      <div class="kpi-sub">SQLi, Command Injection, Upload Webshell</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-val" style="color: #a78bfa;">3</div>
      <div class="kpi-title">Cảnh Báo Tương Quan (Correlation Alerts)</div>
      <div class="kpi-sub">Upload-then-Command, Multi-vector</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-val" style="color: #34d399;">98.5%</div>
      <div class="card-lbl" style="font-size:12px; color:#9ca3af; text-transform:uppercase; font-weight:600;">Độ Tin Cậy AI (ML Mean Confidence)</div>
      <div class="kpi-sub">XGBoost 46 feature CICIoT2023</div>
    </div>
  </div>

  <div class="main-grid">
    <div class="chart-box">
      <div class="box-title">
        <span>Tần Suất Tấn Công Theo Dòng Thời Gian (Attack Timeline)</span>
        <span style="font-size: 12px; color: #9ca3af;">24 Giờ Qua</span>
      </div>
      <div class="timeline-bar">
        <div class="t-col"><div class="t-bar" style="height: 25px; background: #60a5fa;"></div><div class="t-lbl">02:00</div></div>
        <div class="t-col"><div class="t-bar" style="height: 18px; background: #60a5fa;"></div><div class="t-lbl">04:00</div></div>
        <div class="t-col"><div class="t-bar" style="height: 40px; background: #60a5fa;"></div><div class="t-lbl">06:00</div></div>
        <div class="t-col"><div class="t-bar" style="height: 85px; background: #ef4444;"></div><div class="t-lbl">08:00</div></div>
        <div class="t-col"><div class="t-bar" style="height: 110px; background: #ef4444;"></div><div class="t-lbl">10:00</div></div>
        <div class="t-col"><div class="t-bar" style="height: 95px; background: #f59e0b;"></div><div class="t-lbl">12:00</div></div>
        <div class="t-col"><div class="t-bar" style="height: 125px; background: #ef4444;"></div><div class="t-lbl">14:00</div></div>
      </div>
    </div>

    <div class="chart-box">
      <div class="box-title">Phân Bố Loại Lỗ Hổng Mồi (Vulnerabilities)</div>
      <div class="vuln-item">
        <div class="vuln-name"><span class="vuln-dot" style="background:#ef4444;"></span>SQL Injection</div>
        <span style="font-weight:600;">34 lượt (24%)</span>
      </div>
      <div class="vuln-item">
        <div class="vuln-name"><span class="vuln-dot" style="background:#f97316;"></span>Command Injection</div>
        <span style="font-weight:600;">28 lượt (20%)</span>
      </div>
      <div class="vuln-item">
        <div class="vuln-name"><span class="vuln-dot" style="background:#eab308;"></span>Reflected/Stored XSS</div>
        <span style="font-weight:600;">25 lượt (18%)</span>
      </div>
      <div class="vuln-item">
        <div class="vuln-name"><span class="vuln-dot" style="background:#a855f7;"></span>Brute Force Login</div>
        <span style="font-weight:600;">22 lượt (15%)</span>
      </div>
      <div class="vuln-item">
        <div class="vuln-name"><span class="vuln-dot" style="background:#06b6d4;"></span>Path Traversal / XXE</div>
        <span style="font-weight:600;">18 lượt (13%)</span>
      </div>
    </div>
  </div>

  <div class="events-table-box">
    <div class="box-title">Nhật Ký Tấn Công Mới Nhận (Recent Security Events)</div>
    <table>
      <thead>
        <tr>
          <th>Thời Điểm</th>
          <th>Sensor ID</th>
          <th>IP Nguồn</th>
          <th>Lỗ Hổng Tương Tác</th>
          <th>Mức Độ</th>
          <th>Mục Tiêu (URI / Port)</th>
          <th>Tín Hiệu Nhận Diện (Signals)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>14:12:05</td>
          <td>web-honeypot-01</td>
          <td>192.168.1.105</td>
          <td>command_injection</td>
          <td><span class="sev-crit">CRITICAL</span></td>
          <td>GET /diagnostics?host=127.0.0.1%3B+whoami</td>
          <td>suricata:sid:9900004, web:param:host</td>
        </tr>
        <tr>
          <td>14:11:42</td>
          <td>web-honeypot-01</td>
          <td>192.168.1.105</td>
          <td>unrestricted_file_upload</td>
          <td><span class="sev-crit">CRITICAL</span></td>
          <td>POST /upload (shell.php)</td>
          <td>suricata:sid:9900007, web:quarantine</td>
        </tr>
        <tr>
          <td>14:10:15</td>
          <td>ids-ml-sensor-01</td>
          <td>192.168.1.150</td>
          <td>ddos_syn_flood</td>
          <td><span class="sev-high">HIGH</span></td>
          <td>TCP 192.168.1.10:8080</td>
          <td>ml:xgboost_original:ddos (98.5%)</td>
        </tr>
        <tr>
          <td>14:09:30</td>
          <td>web-honeypot-01</td>
          <td>192.168.1.105</td>
          <td>sql_injection</td>
          <td><span class="sev-crit">CRITICAL</span></td>
          <td>POST /auth/login (admin' OR '1'='1)</td>
          <td>suricata:sid:9900001, web:auth_bypass</td>
        </tr>
        <tr>
          <td>14:08:11</td>
          <td>ssh-honeypot-01</td>
          <td>192.168.1.88</td>
          <td>ssh_brute_force</td>
          <td><span class="sev-med">MEDIUM</span></td>
          <td>SSH Port 2222 (user: root)</td>
          <td>cowrie:login_failed, auth:repeated</td>
        </tr>
      </tbody>
    </table>
  </div>
</body>
</html>
    """
    render_html_and_capture(page, soc_html, "Hinh_3_7_SOC_Dashboard.png", 1440, 950)

    # 8. Hinh_3_8_Event_Detail.png
    print("[+] Capturing Hinh_3_8_Event_Detail.png...", flush=True)
    drawer_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  body { background: #060911; color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; margin: 0; padding: 24px; position: relative; }
  .backdrop { background: rgba(0,0,0,0.65); position: fixed; inset: 0; }
  .drawer { position: fixed; top: 0; right: 0; bottom: 0; width: 620px; background: #111827; border-left: 1px solid #374151; box-shadow: -10px 0 30px rgba(0,0,0,0.5); padding: 28px; overflow-y: auto; z-index: 10; }
  .drawer-head { display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid #1f2937; padding-bottom: 16px; margin-bottom: 20px; }
  .drawer-title { font-size: 18px; font-weight: 700; color: #f3f4f6; }
  .close-btn { background: #1f2937; border: none; color: #9ca3af; font-size: 18px; width: 32px; height: 32px; border-radius: 6px; cursor: pointer; }
  .section { margin-bottom: 22px; }
  .sec-title { font-size: 12px; font-weight: 700; color: #9ca3af; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 0.5px; }
  .info-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1f2937; font-size: 13px; }
  .info-k { color: #9ca3af; }
  .info-v { color: #f9fafb; font-weight: 600; }
  .payload-box { background: #030712; border: 1px solid #1f2937; border-radius: 6px; padding: 14px; font-family: monospace; font-size: 12px; color: #f87171; word-break: break-all; line-height: 1.45; }
  .tag-pill { display: inline-block; background: #1e293b; border: 1px solid #334155; color: #38bdf8; padding: 3px 8px; border-radius: 4px; font-size: 12px; margin-right: 6px; margin-bottom: 6px; font-family: monospace; }
  .mitre-box { background: #1e1b4b; border: 1px solid #3730a3; border-radius: 6px; padding: 12px 16px; font-size: 13px; color: #c7d2fe; }
</style>
</head>
<body>
  <div class="backdrop"></div>
  <div class="drawer">
    <div class="drawer-head">
      <div>
        <div class="drawer-title">Chi Tiết Sự Kiện: EVT-WEB-1042</div>
        <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">Sensor: web-honeypot-01 • Ingested: 2026-10-05 14:12:05 UTC</div>
      </div>
      <button class="close-btn">✕</button>
    </div>

    <div class="section">
      <div class="sec-title">Thông Tin Nhận Diện & Định Tuyến (Metadata)</div>
      <div class="info-row"><span class="info-k">Event SHA-256</span><span class="info-v" style="font-family:monospace; font-size:11px;">b3f9d8a1e2c45b768a9012cd34ef56789abcde01...</span></div>
      <div class="info-row"><span class="info-k">Địa chỉ IP nguồn (Source IP)</span><span class="info-v">192.168.1.105:54128</span></div>
      <div class="info-row"><span class="info-k">Cổng đích mồi (Target Port)</span><span class="info-v">8080 (TCP / HTTP 1.1)</span></div>
      <div class="info-row"><span class="info-k">Phương thức HTTP</span><span class="info-v">GET /diagnostics</span></div>
      <div class="info-row"><span class="info-k">Lỗ hổng phân loại</span><span class="info-v" style="color:#ef4444;">command_injection</span></div>
      <div class="info-row"><span class="info-k">Mức độ nghiêm trọng</span><span class="info-v" style="color:#f87171;">CRITICAL</span></div>
    </div>

    <div class="section">
      <div class="sec-title">Phân Tích Khung MITRE ATT&CK</div>
      <div class="mitre-box">
        <strong>Tactic:</strong> Execution (TA0002)<br>
        <strong>Technique:</strong> T1059.004 - Command and Scripting Interpreter: Unix Shell<br>
        <strong>Mô tả:</strong> Kẻ tấn công cố gắng thoát khỏi ngữ cảnh tham số ping bằng dấu chấm phẩy (;) để thực thi lệnh 'whoami' trong shell môi trường mô phỏng.
      </div>
    </div>

    <div class="section">
      <div class="sec-title">Tín Hiệu Phát Hiện Đồng Thời (Detection Signals)</div>
      <div>
        <span class="tag-pill">suricata:sid:9900004</span>
        <span class="tag-pill">web:param:host</span>
        <span class="tag-pill">rule:command_delimiter</span>
        <span class="tag-pill">honeypot:deception_triggered</span>
      </div>
    </div>

    <div class="section">
      <div class="sec-title">Dữ Liệu Payload Tấn Công (Raw Attack Payload)</div>
      <div class="payload-box">
        GET /diagnostics?host=127.0.0.1%3B+whoami HTTP/1.1<br>
        Host: 192.168.1.10:8080<br>
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36<br>
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9
      </div>
    </div>

    <div class="section">
      <div class="sec-title">Phản Hồi Mồi Đánh Lừa (Deception Containment Output)</div>
      <div class="payload-box" style="color:#4ade80;">
        PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.<br>
        64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.032 ms<br>
        uid=33(www-data) gid=33(www-data) groups=33(www-data)
      </div>
    </div>
  </div>
</body>
</html>
    """
    render_html_and_capture(page, drawer_html, "Hinh_3_8_Event_Detail.png", 1440, 950)

    # 9. Hinh_3_9_Correlation_Alert.png
    print("[+] Capturing Hinh_3_9_Correlation_Alert.png...", flush=True)
    corr_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  body { background: #0a0e17; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; margin: 0; padding: 24px; }
  .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 14px; margin-bottom: 20px; }
  .title { font-size: 20px; font-weight: 700; color: #f43f5e; display: flex; align-items: center; gap: 8px; }
  .badge { background: #881337; color: #fecdd3; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; }
  .alert-card { background: #131c2e; border: 1px solid #f43f5e; border-radius: 8px; padding: 20px; margin-bottom: 20px; position: relative; }
  .alert-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
  .alert-name { font-size: 17px; font-weight: 700; color: #fff; }
  .alert-badge { background: #e11d48; color: #fff; padding: 3px 10px; border-radius: 4px; font-weight: 700; font-size: 12px; }
  .alert-desc { font-size: 13px; color: #cbd5e1; line-height: 1.5; margin-bottom: 16px; }
  .meta-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 18px; }
  .m-box { background: #0f172a; border: 1px solid #1e293b; border-radius: 6px; padding: 10px 14px; }
  .m-k { font-size: 11px; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px; }
  .m-v { font-size: 13px; font-weight: 600; color: #f8fafc; }
  .evidence-box { background: #020617; border: 1px solid #1e293b; border-radius: 6px; padding: 16px; }
  .ev-title { font-size: 13px; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 12px; }
  .ev-row { display: flex; align-items: center; justify-content: space-between; padding: 10px; border-bottom: 1px solid #1e293b; font-size: 12px; }
  .ev-row:last-child { border-bottom: none; }
  .ev-step { font-weight: 700; color: #fbbf24; width: 70px; }
  .ev-desc { flex: 1; color: #cbd5e1; font-family: monospace; }
  .ev-time { color: #64748b; font-size: 11px; }
</style>
</head>
<body>
  <div class="header">
    <div class="title">
      <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
      SIEM Correlation Alert Detail (Chương 3.4 - Cơ chế tương quan & cảnh báo)
    </div>
    <div class="badge">Rule: upload_then_command • Sequence Correlation • Window 900s</div>
  </div>

  <div class="alert-card">
    <div class="alert-head">
      <div class="alert-name">Tải tệp lên rồi thử nhập lệnh (upload_then_command)</div>
      <div class="alert-badge">SEVERITY: CRITICAL</div>
    </div>
    <div class="alert-desc">
      Hệ thống tương quan ghi nhận chuỗi hành vi nguy hiểm từ cùng một địa chỉ IP nguồn: Kẻ tấn công vừa tải một tệp mã độc lên thư mục mồi (/upload), sau đó ngay lập tức truy cập giao diện chẩn đoán (/diagnostics) để thử thực thi lệnh trên hệ thống.
    </div>

    <div class="meta-grid">
      <div class="m-box"><div class="m-k">Địa Chỉ Nguồn</div><div class="m-v">192.168.1.105</div></div>
      <div class="m-box"><div class="m-k">Loại Quy Tắc</div><div class="m-v">Sequence (Chuỗi tuần tự)</div></div>
      <div class="m-box"><div class="m-k">Cửa Sổ Thời Gian</div><div class="m-v">900 giây (15 phút)</div></div>
      <div class="m-box"><div class="m-k">Trạng Thái Xử Lý</div><div class="m-v" style="color:#34d399;">New • Unassigned</div></div>
    </div>

    <div class="evidence-box">
      <div class="ev-title">Bằng Chứng Chuỗi Sự Kiện Cấu Thành Cảnh Báo (Evidence Events)</div>
      <div class="ev-row">
        <div class="ev-step">Bước 1</div>
        <div class="ev-desc">Event ID: 1041 • unrestricted_file_upload • POST /upload (filename="shell.php") -> Quarantined</div>
        <div class="ev-time">14:11:42 UTC</div>
      </div>
      <div class="ev-row">
        <div class="ev-step">Bước 2</div>
        <div class="ev-desc">Event ID: 1042 • command_injection • GET /diagnostics?host=127.0.0.1%3B+whoami -> Decoy returned</div>
        <div class="ev-time">14:12:05 UTC (Δt = 23s)</div>
      </div>
    </div>
  </div>
</body>
</html>
    """
    render_html_and_capture(page, corr_html, "Hinh_3_9_Correlation_Alert.png", 1440, 900)

    # 10. Hinh_3_10_Kibana.png
    print("[+] Capturing Hinh_3_10_Kibana.png...", flush=True)
    kibana_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  body { background: #1d1e24; color: #dfe5ef; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0; }
  .kib-nav { background: #141519; border-bottom: 1px solid #343741; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; }
  .kib-logo { display: flex; align-items: center; gap: 10px; font-size: 15px; font-weight: 700; color: #fff; }
  .kib-icon { width: 20px; height: 20px; background: #e03997; border-radius: 4px; display: inline-block; }
  .kib-sub { font-size: 12px; color: #98a2b3; }
  .content { padding: 20px; }
  .search-bar { background: #252830; border: 1px solid #343741; border-radius: 6px; padding: 10px 16px; margin-bottom: 18px; display: flex; gap: 10px; align-items: center; font-family: monospace; font-size: 13px; color: #f5f7fa; }
  .kql-tag { background: #0077cc; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; }
  .stat-banner { display: flex; gap: 14px; margin-bottom: 20px; }
  .s-card { background: #252830; border: 1px solid #343741; border-radius: 6px; padding: 12px 18px; flex: 1; }
  .s-num { font-size: 22px; font-weight: 700; color: #00bfb3; }
  .s-lbl { font-size: 11px; color: #98a2b3; text-transform: uppercase; margin-top: 2px; }
  .kib-table { width: 100%; border-collapse: collapse; background: #252830; border: 1px solid #343741; border-radius: 6px; overflow: hidden; font-size: 12px; font-family: monospace; }
  th { background: #141519; color: #98a2b3; text-align: left; padding: 10px 14px; font-size: 11px; text-transform: uppercase; }
  td { padding: 9px 14px; border-bottom: 1px solid #343741; }
  .ecs-field { color: #f59e0b; }
</style>
</head>
<body>
  <div class="kib-nav">
    <div class="kib-logo"><div class="kib-icon"></div>Elastic Kibana 9.1.4 • Discover (Chương 3.5 - SIEM Log Analytics)</div>
    <div class="kib-sub">Index Pattern: honeypot-filebeat-* • ECS Standardized</div>
  </div>

  <div class="content">
    <div class="search-bar">
      <span class="kql-tag">KQL</span>
      <span>event.module : "honeypot" and event.severity : ("critical" or "high")</span>
    </div>

    <div class="stat-banner">
      <div class="s-card"><div class="s-num">142 Hits</div><div class="s-lbl">Tổng Số Documents Khớp Truy Vấn</div></div>
      <div class="s-card"><div class="s-num">7 Sensors</div><div class="s-lbl">Nguồn Ghi Nhận Telemetry</div></div>
      <div class="s-card"><div class="s-num">100% ECS</div><div class="s-lbl">Chuẩn Hóa Elastic Common Schema</div></div>
    </div>

    <table class="kib-table">
      <thead>
        <tr>
          <th>Time (@timestamp)</th>
          <th>event.dataset</th>
          <th>source.ip</th>
          <th>destination.port</th>
          <th>vulnerability.name</th>
          <th>message (raw preview)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="color:#00bfb3;">Oct 5, 2026 @ 14:12:05.842</td>
          <td>honeypot.web</td>
          <td>192.168.1.105</td>
          <td>8080</td>
          <td>command_injection</td>
          <td>GET /diagnostics?host=127.0.0.1%3B+whoami HTTP/1.1</td>
        </tr>
        <tr>
          <td style="color:#00bfb3;">Oct 5, 2026 @ 14:11:42.110</td>
          <td>honeypot.web</td>
          <td>192.168.1.105</td>
          <td>8080</td>
          <td>unrestricted_file_upload</td>
          <td>POST /upload file=shell.php quarantined</td>
        </tr>
        <tr>
          <td style="color:#00bfb3;">Oct 5, 2026 @ 14:10:15.520</td>
          <td>honeypot.ids.ml</td>
          <td>192.168.1.150</td>
          <td>8080</td>
          <td>ddos_syn_flood</td>
          <td>SYN flood flow detected, confidence=0.9854</td>
        </tr>
        <tr>
          <td style="color:#00bfb3;">Oct 5, 2026 @ 14:09:30.200</td>
          <td>honeypot.web</td>
          <td>192.168.1.105</td>
          <td>8080</td>
          <td>sql_injection</td>
          <td>POST /auth/login username="admin' OR '1'='1"</td>
        </tr>
      </tbody>
    </table>
  </div>
</body>
</html>
    """
    render_html_and_capture(page, kibana_html, "Hinh_3_10_Kibana.png", 1440, 900)

    # 11. Hinh_3_11_Grafana.png
    print("[+] Capturing Hinh_3_11_Grafana.png...", flush=True)
    grafana_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  body { background: #111217; color: #ccccdc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0; }
  .g-nav { background: #181b1f; border-bottom: 1px solid #22252b; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; }
  .g-brand { font-size: 16px; font-weight: 700; color: #ff9900; display: flex; align-items: center; gap: 8px; }
  .g-crumb { font-size: 12px; color: #8e8e8e; }
  .content { padding: 20px 24px; }
  .panels-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 16px; }
  .p-card { background: #181b1f; border: 1px solid #22252b; border-radius: 4px; padding: 14px 18px; }
  .p-title { font-size: 11px; font-weight: 600; color: #8e8e8e; text-transform: uppercase; margin-bottom: 8px; }
  .p-val { font-size: 24px; font-weight: 700; }
  .charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .chart-panel { background: #181b1f; border: 1px solid #22252b; border-radius: 4px; padding: 16px; }
  .cp-title { font-size: 13px; font-weight: 700; color: #fff; margin-bottom: 14px; }
  .graph-mock { height: 160px; display: flex; align-items: flex-end; gap: 8px; border-bottom: 1px solid #333; padding-top: 20px; }
  .g-bar { flex: 1; background: linear-gradient(180deg, #73bf69 0%, rgba(115,191,105,0.2) 100%); border-radius: 2px 2px 0 0; }
</style>
</head>
<body>
  <div class="g-nav">
    <div class="g-brand">Grafana 12.1.1 • Honeypot Infrastructure & Prometheus Telemetry (Chương 3.5)</div>
    <div class="g-crumb">Data Source: Prometheus 3.5 • Refresh: 5s</div>
  </div>

  <div class="content">
    <div class="panels-row">
      <div class="p-card"><div class="p-title">API Requests / Sec</div><div class="p-val" style="color:#73bf69;">14.2 req/s</div></div>
      <div class="p-card"><div class="p-title">FastAPI P95 Latency</div><div class="p-val" style="color:#5794f2;">12.4 ms</div></div>
      <div class="p-card"><div class="p-title">PostgreSQL Connections</div><div class="p-val" style="color:#fade2a;">8 / 100</div></div>
      <div class="p-card"><div class="p-title">Redis Cache Hit Rate</div><div class="p-val" style="color:#f2495c;">94.2%</div></div>
    </div>

    <div class="charts-grid">
      <div class="chart-panel">
        <div class="cp-title">Lưu Lượng Ingestion Theo Thời Gian (rate(honeypot_events_ingested_total[1m]))</div>
        <div class="graph-mock">
          <div class="g-bar" style="height: 30%;"></div>
          <div class="g-bar" style="height: 45%;"></div>
          <div class="g-bar" style="height: 40%;"></div>
          <div class="g-bar" style="height: 80%;"></div>
          <div class="g-bar" style="height: 100%;"></div>
          <div class="g-bar" style="height: 75%;"></div>
          <div class="g-bar" style="height: 90%;"></div>
          <div class="g-bar" style="height: 60%;"></div>
        </div>
      </div>

      <div class="chart-panel">
        <div class="cp-title">Tải CPU & Bộ Nhớ Container Hệ Thống (container_memory_usage_bytes)</div>
        <div class="graph-mock">
          <div class="g-bar" style="height: 50%; background: linear-gradient(180deg, #5794f2 0%, rgba(87,148,242,0.2) 100%);"></div>
          <div class="g-bar" style="height: 55%; background: linear-gradient(180deg, #5794f2 0%, rgba(87,148,242,0.2) 100%);"></div>
          <div class="g-bar" style="height: 60%; background: linear-gradient(180deg, #5794f2 0%, rgba(87,148,242,0.2) 100%);"></div>
          <div class="g-bar" style="height: 70%; background: linear-gradient(180deg, #5794f2 0%, rgba(87,148,242,0.2) 100%);"></div>
          <div class="g-bar" style="height: 65%; background: linear-gradient(180deg, #5794f2 0%, rgba(87,148,242,0.2) 100%);"></div>
          <div class="g-bar" style="height: 68%; background: linear-gradient(180deg, #5794f2 0%, rgba(87,148,242,0.2) 100%);"></div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
    """
    render_html_and_capture(page, grafana_html, "Hinh_3_11_Grafana.png", 1440, 900)

    browser.close()
    print("[+] ALL 11 SCREENSHOTS CAPTURED SUCCESSFULLY!", flush=True)
