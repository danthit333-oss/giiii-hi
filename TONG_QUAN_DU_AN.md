# TỔNG QUAN CHI TIẾT HỆ THỐNG WEB HONEYPOT VÀ PHÂN TÍCH TẤN CÔNG ĐA LỚP

Tài liệu này cung cấp cái nhìn toàn diện, chuyên sâu và chi tiết về cấu trúc kiến trúc, luồng xử lý dữ liệu, công nghệ sử dụng, cùng cơ chế vận hành của toàn bộ hệ thống Honeypot (hệ thống bẫy/mồi nhử phát hiện tấn công mạng).

---

## 1. Dự án này là gì?

Dự án này là một **Hệ thống Web Honeypot (hệ thống bẫy/mồi nhử phát hiện tấn công mạng)** tích hợp **Trí tuệ nhân tạo (AI/ML - Machine Learning)**, **Hệ thống phát hiện xâm nhập (IDS - Intrusion Detection System)**, **Hệ thống giám sát bảo mật & cảnh báo (SIEM - Security Information and Event Management)** và **Bảng điều khiển trực quan (Dashboard)**.

Mục tiêu chính của hệ thống:
- Đặt ra các bề mặt web và dịch vụ SSH giả lập nhằm thu hút kẻ tấn công mạng.
- Ghi nhận lại toàn bộ hành vi, phân tích dấu hiệu xâm nhập bằng cả luật tĩnh (Rule-based IDS) và mô hình Học máy (Machine Learning).
- Cách ly hoàn toàn môi trường mồi nhử (Lure plane) với môi trường quản trị và lưu trữ dữ liệu (Control/Data plane) để đảm bảo an toàn tuyệt đối cho hệ thống thật.

---

## 2. Kiến trúc tổng thể & Luồng dữ liệu (Data Flow)

### Sơ đồ luồng dữ liệu dạng Text:

```text
[Kẻ tấn công / Client]
       │
       ├─► (Port 8080 - HTTP) ──► Edge WAF (ModSecurity CRS) ──► Flask Web Honeypot (Part 02)
       │                                                                │ (Log JSON)
       │                                                                ▼
       ├─► (Port 2222 - SSH)  ──► SSH Proxy (HAProxy) ───────► Cowrie SSH Honeypot
       │                                                                │ (Log JSON)
       │                                                                ▼
       └─► (NIC Lab - Gói tin) ──► Suricata IDS (Part 05) ──► IDS/ML Bridge (XGBoost)
                                                                        │
       ┌────────────────────────────────────────────────────────────────┘
       │ (Gửi event qua HTTP API)
       ▼
[FastAPI Backend - Part 03] ──► PostgreSQL (Lưu trữ) & Redis (Bộ đệm khử trùng lặp - Dedup)
       │
       ├─► [React Dashboard - Part 04] (Xác thực qua Keycloak OIDC/PKCE)
       ├─► [Prometheus & Grafana] (Giám sát chỉ số hiệu năng - Metrics)
       └─► [Filebeat ──► Elasticsearch & Kibana - Part 06] (Truy vấn & Tương quan sự kiện - SIEM)
```

### Sơ đồ phân vùng kiến trúc (Mermaid Diagram):

```mermaid
flowchart TD
    subgraph LurePlane ["Vùng mồi nhử (Lure Plane - Phân vùng cách ly)"]
        AttackerWeb["Kẻ tấn công Web"] -->|Port 8080 / HTTP| EdgeWAF["Nginx Edge + ModSecurity WAF (Tường lửa ứng dụng web)"]
        EdgeWAF -->|Chuyển tiếp an toàn| WebHoneypot["Flask Web Honeypot (Part 02)"]
        
        AttackerSSH["Kẻ tấn công SSH"] -->|Port 2222 / SSH| SSHProxy["HAProxy (Bộ cân bằng tải/ủy quyền TCP)"]
        SSHProxy --> Cowrie["Cowrie SSH Honeypot (Bẫy SSH mồi)"]
    end

    subgraph SensorNetwork ["Thu thập & Phân tích mạng (Network Sensor)"]
        NIC["Card mạng Lab (Network Interface)"] --> Suricata["Suricata IDS (Hệ thống phát hiện xâm nhập)"]
        Suricata -->|eve.json log| Bridge["IDS / ML Bridge (Part 05)"]
        Bridge -->|Chấm điểm luồng mạng| ML["Mô hình XGBoost 7 lớp (Part 01)"]
    end

    subgraph DataPlane ["Vùng xử lý & Lưu trữ trung tâm (Data Plane)"]
        WebHoneypot -->|Log chuyển tiếp| ForwarderWeb["Log Forwarder"]
        Cowrie -->|Log chuyển tiếp| ForwarderSSH["Cowrie Forwarder"]
        
        ForwarderWeb -->|HTTP POST JSON| FastAPI["FastAPI Backend (Part 03)"]
        ForwarderSSH -->|HTTP POST JSON| FastAPI
        Bridge -->|HTTP POST Event| FastAPI
        
        FastAPI -->|Lưu trữ lâu dài| Postgres[("PostgreSQL Database")]
        FastAPI -->|Khử trùng lặp (Dedup) & Cache| Redis[("Redis in-memory store")]
        FastAPI -->|Chỉ số hệ thống /metrics| Prometheus["Prometheus Monitor"]
    end

    subgraph ControlPlane ["Vùng quản trị & Giám sát (Control Plane - Bind 127.0.0.1)"]
        Admin["Quản trị viên / SOC Analyst"] -->|Port 8088| ControlEdge["Nginx Control Reverse Proxy"]
        ControlEdge --> Dashboard["React Dashboard (Part 04)"]
        Dashboard -->|Xác thực OIDC / PKCE| Keycloak["Keycloak IAM / SSO (Hệ thống quản lý danh tính)"]
        Dashboard -->|Gọi REST API| FastAPI
        
        ControlEdge --> Grafana["Grafana Dashboard (Biểu đồ hiệu năng)"]
        Prometheus --> Grafana
        
        Suricata -.->|Filebeat thu thập| Elastic[("Elasticsearch")]
        FastAPI -.->|Filebeat thu thập| Elastic
        Elastic --> Kibana["Kibana SIEM (Truy vấn sự kiện chuyên sâu)"]
    end
```

---

## 3. Chi tiết các thành phần trong dự án (Có những gì và đã làm những gì?)

Dự án được chia thành **9 phần (Parts)** độc lập nhưng liên kết chặt chẽ qua các giao thức chuẩn:

### [Part 01: AI/ML Detection Engine](file:///d:/A/A_5chai/honey_pot/part_01_AI_ML) (Mô hình Học máy phát hiện tấn công)
- **Đã làm:**
  - Xây dựng mô hình phân loại tấn công mạng dựa trên thuật toán **XGBoost (thuật toán cây quyết định tăng cường độ chính xác cao)** gồm **7 lớp nhãn** (Bình thường - Normal, Do thám - Recon, Tấn công từ chối dịch vụ - DoS, Khai thác lỗ hổng Web - Web Exploit, Brute Force mật khẩu, Leo thang đặc quyền - Privilege Escalation, Mã độc - Malware).
  - Tối ưu và xuất mô hình sang định dạng nhị phân **UBJ (Universal Binary JSON)** để tối ưu tốc độ dự đoán thời gian thực.
  - Chuẩn hóa bộ đặc trưng (Feature vector gồm 46 chiều) tương thích trực tiếp với dữ liệu luồng mạng từ IDS.

### [Part 02: Web Honeypot](file:///d:/A/A_5chai/honey_pot/part_02_WEB_HONEYPOT) (Hệ thống Web mồi nhử)
- **Đã làm:**
  - Viết ứng dụng Web mồi nhử giả lập giao diện bằng Python/Flask và Bootstrap.
  - Cung cấp **10 bề mặt tương tác giả lập lỗi bảo mật** (như SQL Injection - tiêm mã truy vấn SQL, XSS - chèn mã độc JavaScript, LFI/RFI - đọc ghi file nội bộ/từ xa, Command Injection - chèn lệnh hệ điều hành, Upload file độc hại, v.v.).
  - Áp dụng cơ chế **Containment (cô lập an toàn)**: Không thực thi lệnh thật, không kết nối database thật; mọi hành vi tấn công đều bị ghi lại dưới dạng JSON log và gửi về Backend thông qua bộ chuyển tiếp log (`part2-forwarder`).

### [Part 03: API & Centralized Logging](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING) (Trung tâm tiếp nhận dữ liệu & API)
- **Đã làm:**
  - Xây dựng dịch vụ Backend bằng **FastAPI (framework Python tốc độ cao)**.
  - Tích hợp xác thực qua **OIDC (OpenID Connect - giao thức xác thực danh tính dựa trên OAuth2)** kết hợp với **Keycloak** và API Key nội bộ.
  - Cơ chế **Deduplication (khử trùng lặp log)** bằng **Redis (hệ thống lưu trữ tạm trong RAM)** trước khi ghi vào cơ sở dữ liệu quan hệ **PostgreSQL**.
  - Cung cấp các điểm cuối (Endpoints) phục vụ truy vấn dữ liệu sự kiện, thống kê cho Dashboard và xuất chỉ số `/metrics` cho **Prometheus (công cụ thu thập số liệu giám sát)**.

### [Part 04: Dashboard Analytics](file:///d:/A/A_5chai/honey_pot/part_04_DASHBOARD_ANALYTICS) (Giao diện Quản trị & Phân tích)
- **Đã làm:**
  - Xây dựng giao diện Single Page Application bằng **React, TailwindCSS và ECharts (thư viện biểu đồ trực quan)**.
  - Tích hợp luồng xác thực bảo mật **Keycloak PKCE (Proof Key for Code Exchange - kỹ thuật chống đánh cắp mã ủy quyền trên frontend)**.
  - Cho phép lọc sự kiện, xem chi tiết payload (dữ liệu truyền tải của cuộc tấn công), theo dõi tấn công thời gian thực và xuất báo cáo dưới dạng tệp CSV.

### [Part 05: IDS & ML Real-time Bridge](file:///d:/A/A_5chai/honey_pot/part_05_IDS_ML_DETECTION) (Cầu nối IDS mạng và Học máy)
- **Đã làm:**
  - Tích hợp **Suricata (hệ thống phát hiện/ngăn chặn xâm nhập mạng nguồn mở)** để bắt gói tin mạng trên card mạng (NIC).
  - Viết bộ xử lý dữ liệu (`ids_bridge`) đọc log `eve.json` của Suricata, trích xuất đúng **46 đặc trưng luồng (Flow Features)** và nạp vào mô hình XGBoost của Part 01 để chấm điểm và phân loại rủi ro trực tiếp.
  - Hỗ trợ chạy native trên Windows (thông qua trình điều khiển Npcap) lẫn Docker trên Linux.

### [Part 06: SIEM & Correlation Rules](file:///d:/A/A_5chai/honey_pot/part_06_SIEM_ALERTING) (Hệ thống Quản lý Sự kiện & Cảnh báo Bảo mật)
- **Đã làm:**
  - Chuẩn hóa toàn bộ cấu trúc log theo chuẩn **ECS (Elastic Common Schema - lược đồ dữ liệu chuẩn hóa của Elastic)**.
  - Sử dụng **Filebeat (công cụ chuyển phát log)** đẩy log vào **Elasticsearch (cơ sở dữ liệu tìm kiếm và phân tích phân tán)** và trực quan hóa qua **Kibana**.
  - Xây dựng **4 luật tương quan sự kiện (Correlation Rules)** để tự động cảnh báo các đợt tấn công nguy hiểm (như dò quét diện rộng, tấn công vét cạn nhiều cổng cùng lúc).

### [Part 07: Security Hardening & Isolation](file:///d:/A/A_5chai/honey_pot/part_07_SECURITY_HARDENING) (Gia cố an toàn & Phân vùng mạng)
- **Đã làm:**
  - Cấu hình **Nginx Reverse Proxy (máy chủ ủy quyền ngược)** kết hợp **ModSecurity WAF (Web Application Firewall - tường lửa ứng dụng web)** với bộ luật **OWASP CRS (Core Rule Set - bộ quy tắc cốt lõi nhận diện tấn công web)**.
  - Lập mô hình đe dọa [THREAT_MODEL.md](file:///d:/A/A_5chai/honey_pot/part_07_SECURITY_HARDENING/THREAT_MODEL.md) và cấu hình **NetworkPolicy (chính sách phân vùng mạng)** nhằm đảm bảo container Honeypot nếu bị xâm nhập cũng không thể quét hoặc tấn công ngược sang Backend/Database/Keycloak.

### [Part 08: Docker Deployment & IAM](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT) (Triển khai tổng thể & Quản lý danh tính)
- **Đã làm:**
  - File [compose.yaml](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT/compose.yaml) hoàn chỉnh điều phối toàn bộ cụm dịch vụ gồm hơn 15 container (Web Honeypot, Cowrie SSH, HAProxy, FastAPI, Postgres, Redis, Dashboard, Nginx Edge, Keycloak, Prometheus, Grafana, Elasticsearch, Kibana, Filebeat).
  - Thiết lập **IAM / RBAC (Role-Based Access Control - kiểm soát quyền truy cập dựa trên vai trò)** trong **Keycloak** (phân quyền quản trị viên, chuyên viên phân tích SOC, người chỉ xem).
  - Cung cấp kịch bản khởi chạy tự động [run.bat](file:///d:/A/A_5chai/honey_pot/run.bat), [start-system.ps1](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT/start-system.ps1), [local-up.ps1](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT/local-up.ps1), tự động sinh mật khẩu bí mật (secrets) ngẫu nhiên.

### [Part 09: Test Matrix & Evaluation Report](file:///d:/A/A_5chai/honey_pot/part_09_TEST_REPORT) (Kiểm thử tự động & Đánh giá)
- **Đã làm:**
  - Xây dựng **10 kịch bản kiểm thử tấn công tự động** (SQLi, XSS, Path Traversal, Brute Force, Scanning, v.v.).
  - Hệ thống tự động ghi nhận kết quả và xuất báo cáo đa định dạng (JSON, Markdown, CSV và đồ thị PNG) phục vụ việc đánh giá độ hiệu quả phát hiện của Honeypot, IDS và mô hình AI.

---

## 4. Tóm tắt ma trận các phần (Parts Breakdown Matrix)

| Part | Tên thành phần | Công nghệ chính | Chức năng & Kết quả chính |
|---|---|---|---|
| 01 | **AI/ML** | Python, XGBoost, Scikit-learn, UBJ | Mô hình cây quyết định 7 lớp nhãn, phân loại nguy cơ với 46 đặc trưng luồng mạng |
| 02 | **Web Honeypot** | Python, Flask, Bootstrap | Website giả lập 10 bề mặt lỗi, cơ chế cô lập an toàn, xuất JSON log |
| 03 | **API & Logging** | FastAPI, PostgreSQL, Redis, OIDC | Trung tâm gom log, khử trùng lặp (Dedup), bảo vệ bằng Keycloak, xuất metric |
| 04 | **Dashboard** | React 18, TailwindCSS, ECharts, Vite | Giao diện giám sát thời gian thực, xem chi tiết payload đòn tấn công, xuất CSV |
| 05 | **IDS & ML** | Suricata, Npcap, Python Bridge | Bắt gói tin card mạng, trích xuất đặc trưng luồng nạp vào XGBoost thời gian thực |
| 06 | **SIEM** | Elasticsearch, Kibana, Filebeat, ECS | Chuẩn hóa định dạng log, thiết lập 4 luật tương quan sự kiện cảnh báo chuỗi tấn công |
| 07 | **Hardening** | Nginx, ModSecurity CRS, NetworkPolicy | Tường lửa WAF, mô hình đe dọa THREAT_MODEL, cách ly container chống rò rỉ |
| 08 | **Deployment** | Docker Compose, Keycloak RBAC, HAProxy | Điều phối 15+ container, phân quyền vai trò người dùng, sinh secret tự động |
| 09 | **Evaluation** | Python, Pytest, Matplotlib, OWASP ZAP | Bộ 10 kịch bản kiểm thử tự động, xuất báo cáo đa định dạng đánh giá hiệu năng |

---

## 5. Các công nghệ và thuật ngữ chuyên ngành giải thích

- **Honeypot (Hệ thống mồi nhử/bẫy mạng)**: Môi trường giả lập các ứng dụng dễ bị tổn thương để nhử kẻ tấn công truy cập vào, nhằm ghi lại hành vi và nghiên cứu kỹ thuật tấn công mà không gây nguy hiểm cho tài sản số thật.
- **IDS (Intrusion Detection System - Hệ thống phát hiện xâm nhập)**: Hệ thống giám sát lưu lượng mạng, phân tích dấu hiệu nhận dạng của các cuộc tấn công dựa trên các chữ ký mẫu (Signature-based) hoặc sự bất thường.
- **WAF (Web Application Firewall - Tường lửa ứng dụng web)**: Lớp bảo vệ nằm phía trước ứng dụng web nhằm lọc bỏ và phát hiện các request (yêu cầu) chứa mã độc như SQL Injection hay XSS.
- **XGBoost (Extreme Gradient Boosting)**: Một thuật toán Học máy tối ưu dựa trên cây quyết định, có tốc độ xử lý nhanh và độ chính xác phân loại cao trên dữ liệu có cấu trúc.
- **SIEM (Security Information and Event Management - Hệ thống quản lý thông tin và sự kiện bảo mật)**: Nền tảng thu thập, tổng hợp log từ nhiều nguồn khác nhau, phục vụ điều tra, truy vấn và phát hiện đe dọa bảo mật theo thời gian thực.
- **OIDC & PKCE (OpenID Connect & Proof Key for Code Exchange)**: Chuẩn giao thức xác thực danh tính người dùng hiện đại, kết hợp cơ chế chống tấn công đánh cắp mã ủy thác (Authorization Code) trên các ứng dụng Frontend.
- **RBAC (Role-Based Access Control - Kiểm soát quyền dựa trên vai trò)**: Cơ chế phân quyền trong hệ thống dựa trên vai trò của người dùng (ví dụ: Admin, Phân tích viên SOC, Người chỉ xem).
- **Containment (Cơ chế cô lập)**: Kỹ thuật giam hãm kẻ tấn công trong một môi trường giả lập kín, phản hồi kết quả trông như thật nhưng không cho phép thực thi bất kỳ câu lệnh hệ điều hành hoặc truy vấn database thực tế nào.

---

## 6. Danh mục cổng kết nối (Port Matrix) & Địa chỉ dịch vụ

| Cổng (Port) | Giao thức | Dịch vụ | Mục đích | Ranh giới bảo mật |
|---|---|---|---|---|
| **8080** | HTTP | Edge WAF -> Flask Honeypot | Cổng mở cho mạng LAN thử nghiệm tấn công mồi nhử | Mở cho dải mạng cục bộ (`LocalSubnet`) |
| **2222** | SSH | HAProxy -> Cowrie SSH | Cổng bẫy mồi nhử SSH ghi lại hành vi đăng nhập/lệnh | Chỉ bind `127.0.0.1` (hoặc mở có kiểm soát) |
| **8088** | HTTP | Control Edge Nginx | Cổng quản trị duy nhất: React Dashboard & API | Chỉ bind `127.0.0.1` |
| **8180** | HTTP | Keycloak IAM Admin | Giao diện quản lý người dùng và cấp quyền | Chỉ bind `127.0.0.1` |
| **3000** | HTTP | Grafana Monitoring | Giám sát hiệu năng CPU/RAM/Request qua Prometheus | Chỉ bind `127.0.0.1` |
| **5601** | HTTP | Kibana UI | Truy vấn dữ liệu log tập trung và luật tương quan SIEM | Chỉ bind `127.0.0.1` |

---

## 7. Hướng dẫn khởi chạy nhanh hệ thống (Quick Start)

### Trên môi trường Windows:
1. Mở PowerShell hoặc Command Prompt với quyền Administrator.
2. Di chuyển vào thư mục dự án và chạy file [run.bat](file:///d:/A/A_5chai/honey_pot/run.bat):
   ```bat
   .\run.bat
   ```
   *Script sẽ tự động: Khởi động Docker Desktop, tạo các khóa bí mật (secrets), bật Docker Compose, thiết lập tường lửa Windows cho cổng 8080 LAN, và khởi chạy Suricata + XGBoost Bridge trên card mạng chính.*

### Trên môi trường Linux Server:
1. Cấp quyền thực thi và chạy script triển khai:
   ```bash
   cd part_08_DOCKER_DEPLOYMENT
   chmod +x linux-up.sh linux-down.sh
   ./linux-up.sh
   ```
2. Kiểm tra trạng thái các container:
   ```bash
   docker compose ps
   ```

---

## 8. Trạng thái hiện tại và tài liệu liên quan

- Toàn bộ 9 phần đã được lập trình hoàn thiện, có cấu hình và test riêng biệt cho từng phần (`pytest`, `tests/`).
- Môi trường triển khai đã sẵn sàng chạy được trên cả Windows và Linux thông qua Docker và PowerShell/Bash scripts.
- Toàn bộ tài liệu hướng dẫn vận hành chi tiết bằng tiếng Việt đã được biên soạn tại [HUONG_DAN_SU_DUNG.md](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT/HUONG_DAN_SU_DUNG.md) và [KEYCLOAK_RBAC.md](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT/KEYCLOAK_RBAC.md).
- Mô hình đe dọa & Phân tích rủi ro: [THREAT_MODEL.md](file:///d:/A/A_5chai/honey_pot/part_07_SECURITY_HARDENING/THREAT_MODEL.md).
- Kịch bản demo kiểm thử tấn công: [demo-all.ps1](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT/demo-all.ps1).
