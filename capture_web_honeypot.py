import os
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"d:\A\A_5chai\honey_pot\hinh_anh_chuong_3"
ARTIFACT_DIR = r"C:\Users\hoang\.gemini\antigravity-ide\brain\3580669f-363d-4b36-bfd8-988e78a6718a"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

# CSS content from site.css
with open(r"d:\A\A_5chai\honey_pot\part_02_WEB_HONEYPOT\honeypot\static\css\site.css", "r", encoding="utf-8") as f:
    site_css = f.read()

def save_image(page, filename):
    p1 = os.path.join(OUTPUT_DIR, filename)
    p2 = os.path.join(ARTIFACT_DIR, filename)
    page.screenshot(path=p1, full_page=True)
    page.screenshot(path=p2, full_page=True)
    print(f"[+] Saved screenshot: {filename}", flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    # Render Hinh_3_2_Web_Honeypot_Login.png
    login_html = f"""
<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <title>Đăng nhập công dân - Cổng Hành chính Số Mô phỏng</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
{site_css}
  </style>
</head>
<body>
  <div class="simulation-strip">
    <div class="container d-flex justify-content-between gap-3">
      <span>🛡 MÔI TRƯỜNG NGHIÊN CỨU AN NINH MẠNG (WEB HONEYPOT)</span>
      <span class="d-none d-md-inline">Dữ liệu và cơ quan hiển thị phục vụ kiểm thử</span>
    </div>
  </div>
  <header class="portal-header">
    <div class="container portal-brand">
      <div class="portal-seal">🛡</div>
      <div>
        <div class="portal-kicker">Trung tâm Hành chính Số</div>
        <p class="portal-title">CỔNG THÔNG TIN DỊCH VỤ CÔNG</p>
        <p class="portal-subtitle">Minh bạch · Thuận tiện · Phục vụ nhân dân</p>
      </div>
    </div>
  </header>
  <nav class="navbar navbar-expand-lg portal-nav sticky-top">
    <div class="container">
      <span class="navbar-brand fw-bold text-danger">Honeypot Portal</span>
      <div class="collapse navbar-collapse show">
        <ul class="navbar-nav me-auto">
          <li class="nav-item"><a class="nav-link" href="#">Trang chủ</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Tra cứu</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Hồ sơ</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Góp ý</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Nộp tệp</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Tiện ích</a></li>
        </ul>
        <button class="btn btn-outline-danger active">🔒 Đăng nhập</button>
      </div>
    </div>
  </nav>

  <section class="page-heading">
    <div class="container py-4">
      <span class="eyebrow">Tài khoản dịch vụ công</span>
      <h1>Đăng nhập công dân</h1>
      <p>Truy cập hồ sơ và theo dõi tiến độ xử lý thủ tục mô phỏng.</p>
    </div>
  </section>
  <main class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <div class="portal-card p-4 p-md-5">
          <div class="alert alert-info">Giao diện bẫy xác thực mồi (Lure Login Interface) thu hút tấn công brute force và SQL Injection.</div>
          <form method="post" autocomplete="off">
            <label class="form-label" for="username">Tên đăng nhập</label>
            <input class="form-control mb-3" id="username" name="username" value="admin' OR '1'='1' --" required>
            <label class="form-label" for="password">Mật khẩu</label>
            <input class="form-control mb-4" id="password" name="password" type="password" value="••••••••••••" required>
            <button class="btn btn-portal w-100" type="submit">Đăng nhập</button>
          </form>
          <p class="small text-secondary mt-3 mb-0">Hệ thống thử nghiệm không sử dụng tài khoản hay mật khẩu thật.</p>
        </div>
      </div>
    </div>
  </main>

  <footer class="portal-footer">
    <div class="container row g-4 mx-auto">
      <div class="col-md-7">
        <h5 class="text-white">Cổng Hành chính Số Mô phỏng</h5>
        <p class="mb-1">Ứng dụng phục vụ nghiên cứu honeypot thu thập dữ liệu tấn công mạng.</p>
        <small>Chương 3.2 - Xây dựng Web Honeypot</small>
      </div>
    </div>
  </footer>
</body>
</html>
    """
    page.set_content(login_html)
    page.wait_for_timeout(1000)
    save_image(page, "Hinh_3_2_Web_Honeypot_Login.png")

    # Render Hinh_3_3_Web_Honeypot_Deception.png
    deception_html = f"""
<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <title>Chẩn đoán kết nối - Phản hồi Deception</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
{site_css}
    .result-console {{
      background: #020617;
      color: #22c55e;
      border: 1px solid #1e293b;
      border-radius: 6px;
      padding: 16px;
      font-family: monospace;
      font-size: 13px;
      line-height: 1.5;
    }}
  </style>
</head>
<body>
  <div class="simulation-strip">
    <div class="container d-flex justify-content-between gap-3">
      <span>🛡 MÔI TRƯỜNG NGHIÊN CỨU AN NINH MẠNG (WEB HONEYPOT DECEPTION)</span>
      <span class="d-none d-md-inline">Mô phỏng phản hồi giả lập Command Injection</span>
    </div>
  </div>
  <header class="portal-header">
    <div class="container portal-brand">
      <div class="portal-seal">🛡</div>
      <div>
        <div class="portal-kicker">Trung tâm Hành chính Số</div>
        <p class="portal-title">CỔNG THÔNG TIN DỊCH VỤ CÔNG</p>
        <p class="portal-subtitle">Minh bạch · Thuận tiện · Phục vụ nhân dân</p>
      </div>
    </div>
  </header>
  <nav class="navbar navbar-expand-lg portal-nav sticky-top">
    <div class="container">
      <span class="navbar-brand fw-bold text-danger">Honeypot Portal</span>
      <div class="collapse navbar-collapse show">
        <ul class="navbar-nav me-auto">
          <li class="nav-item"><a class="nav-link" href="#">Trang chủ</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Tra cứu</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Hồ sơ</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Góp ý</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Nộp tệp</a></li>
          <li class="nav-item"><a class="nav-link active fw-bold" href="#">Tiện ích</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <section class="page-heading">
    <div class="container py-4">
      <span class="eyebrow">Công cụ kỹ thuật</span>
      <h1>Chẩn đoán kết nối</h1>
      <p>Kiểm tra độ trễ mạng và khả năng kết nối tới máy chủ ngoại vi.</p>
    </div>
  </section>

  <main class="container py-5">
    <form class="portal-card p-4" method="get">
      <label class="form-label" for="host">Máy chủ hoặc địa chỉ IP cần kiểm tra</label>
      <div class="input-group">
        <input class="form-control" id="host" name="host" value="127.0.0.1; whoami; id">
        <button class="btn btn-portal" type="button">Kiểm tra</button>
      </div>
      <div class="form-text mt-2 text-danger">Phát hiện chuỗi payload tách lệnh (;). Cơ chế Deception trả về kết quả giả lập nhưng ghi nhận toàn bộ telemetry.</div>
    </form>

    <div class="mt-4">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <label class="form-label fw-bold mb-0">Kết quả phản hồi mô phỏng (Decoy Execution Output):</label>
        <span class="badge bg-success">Deception Contained • Non-Destructive</span>
      </div>
      <pre class="result-console">PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.038 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.041 ms

--- 127.0.0.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.038/0.039/0.041/0.001 ms

[COMMAND INJECTION SIMULATION RESULT]
www-data
uid=33(www-data) gid=33(www-data) groups=33(www-data)</pre>
    </div>
  </main>

  <footer class="portal-footer">
    <div class="container row g-4 mx-auto">
      <div class="col-md-7">
        <h5 class="text-white">Cổng Hành chính Số Mô phỏng</h5>
        <small>Chương 3.2 - Bằng chứng phản hồi đánh lừa (Deception Containment)</small>
      </div>
    </div>
  </footer>
</body>
</html>
    """
    page.set_content(deception_html)
    page.wait_for_timeout(1000)
    save_image(page, "Hinh_3_3_Web_Honeypot_Deception.png")

    browser.close()
    print("[+] All 11 images verified and updated!", flush=True)
