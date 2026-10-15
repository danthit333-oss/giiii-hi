import urllib.request

urls = [
    'http://127.0.0.1:8088/',
    'http://127.0.0.1:8088/api-health',
    'http://127.0.0.1:8088/dashboard/',
    'http://127.0.0.1:8088/api-docs/docs',
    'http://127.0.0.1:8090/healthz',
    'http://127.0.0.1:3000/api/health',
    'http://127.0.0.1:8180/realms/honeypot',
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as r:
            print(f"{u} -> {r.status}", flush=True)
    except Exception as e:
        print(f"{u} -> ERROR: {e}", flush=True)
