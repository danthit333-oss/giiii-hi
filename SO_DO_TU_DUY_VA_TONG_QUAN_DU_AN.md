# 🛡️ TỔNG QUAN HỆ THỐNG HONEYPOT THỜI GIAN THỰC KẾT HỢP TRÍ TUỆ NHÂN TẠO (AI) & TRUNG TÂM ĐIỀU HÀNH SOC

> **Báo cáo Phân tích Cấu trúc & Đồ thị Mối liên hệ Hệ thống**  
> *Được trích xuất và ánh xạ dựa trên công cụ phân tích đồ thị mã nguồn **Graphify** (715 Nodes, 1290 Edges, 58 Communities).*

---

## 📑 MỤC LỤC
1. [Giới thiệu Chung & Mục tiêu Dự án](#1-giới-thiệu-chung--mục-tiêu-dự-án)
2. [Sơ đồ Tư duy Vận hành Hệ thống (Mindmap)](#2-sơ-đồ-tư-duy-vận-hành-hệ-thống-mindmap)
3. [Sơ đồ Mối liên hệ 9 Module & Luồng Dữ liệu (Architecture & Data Flow)](#3-sơ-đồ-mối-liên-hệ-9-module--luồng-dữ-liệu)
4. [Phân tích Chi tiết 9 Module (Part 01 - Part 09)](#4-phân-tích-chi-tiết-9-module)
5. [Các Điểm Nút Trung tâm Cốt lõi (God Nodes được Graphify phát hiện)](#5-các-điểm-nút-trung-tâm-cốt-lõi-god-nodes)
6. [Bảng Giải thích Thuật ngữ An toàn Thông tin Chuyên ngành](#6-bảng-giải-thích-thuật-ngữ-chuyên-ngành)

---

## 1. GIỚI THIỆU CHUNG & MỤC TIÊU DỰ ÁN

Dự án là một hệ thống **Honeypot** *(Cạm bẫy mật - hệ thống mồi nhử an ninh mạng)* thế hệ mới, kết hợp chặt chẽ giữa:
1. **Bẫy mồi nhử đa tầng**: Dụ dỗ tin tặc tấn công vào Web mô phỏng Cổng Dịch vụ công (HTTP) và Máy chủ Linux giả lập (SSH Cowrie).
2. **Cảm biến Mạng & Trí tuệ Nhân tạo (AI IDS)**: Sử dụng mô hình **XGBoost** với 47 đặc trưng mạng để nhận diện và phân loại đòn tấn công thời gian thực trong mili-giây.
3. **Trung tâm Điều hành An ninh mạng (SOC Dashboard)**: Trực quan hóa dữ liệu, đối chiếu kỹ thuật tấn công theo tiêu chuẩn quốc tế **MITRE ATT&CK**, và hỗ trợ xuất báo cáo sự cố an ninh.
4. **Phòng thủ & Cách ly Toàn diện (Security Hardening)**: Tường lửa WAF (ModSecurity) và chính sách phân vùng mạng (Network Segmentation) đảm bảo tin tặc bị cô lập hoàn toàn, không thể dùng bẫy làm bàn đạp tấn công máy chủ thật (**Anti-Pivot**).

---

## 2. SƠ ĐỒ TƯ DUY VẬN HÀNH HỆ THỐNG (MINDMAP)

> 💡 **Xem Trực quan Tương tác (Có thể Click phóng to, thu nhỏ, bung mở nhánh y hệt ảnh mẫu)**:  
> 👉 Hãy mở tệp: [SO_DO_TU_DUY_INTERACTIVE.html](file:///d:/A/A_5chai/honey_pot/SO_DO_TU_DUY_INTERACTIVE.html) trên trình duyệt Chrome!

### 🌲 Sơ đồ Cây Phân Nhánh Ngang (Horizontal Node Tree):

```mermaid
graph LR
    classDef root fill:#2b6cb0,stroke:#63b3ed,stroke-width:2px,color:#fff,rx:8px,ry:8px;
    classDef branch fill:#2d3748,stroke:#4a5568,stroke-width:1.5px,color:#e2e8f0,rx:6px,ry:6px;
    classDef leaf fill:#1a202c,stroke:#2d3748,stroke-width:1px,color:#cbd5e0,rx:4px,ry:4px;

    ROOT["🛡️ Honeypot AI & SOC Project"]:::root

    %% Nhánh cấp 1
    ROOT --> B1["🕸️ Bẫy Mồi Nhử (Lure Layer)"]:::branch
    ROOT --> B2["🧠 Trí Tuệ Nhân Tạo (AI / ML)"]:::branch
    ROOT --> B3["👁️ Cảm Biến Thời Gian Thực (IDS)"]:::branch
    ROOT --> B4["⚡ Trung Tâm Xử Lý (Backend)"]:::branch
    ROOT --> B5["📊 Trực Quan Hóa (SOC UI)"]:::branch
    ROOT --> B6["🛡️ Bảo Mật & Vận Hành (Ops)"]:::branch

    %% Nhánh cấp 2: Bẫy
    B1 --> B1_1["Part 02: Web Honeypot (Flask)"]:::leaf
    B1_1 --> B1_1_1["Lỗ hổng SQLi, XSS, File Upload, Traversal"]:::leaf
    B1_1 --> B1_1_2["Thư mục cách ly Quarantine"]:::leaf
    B1 --> B1_2["Part 08: SSH Honeypot (Cowrie)"]:::leaf
    B1_2 --> B1_2_1["Bẫy Terminal Cổng 2222"]:::leaf
    B1_2 --> B1_2_2["Ghi lại từng ký tự gõ Shell"]:::leaf

    %% Nhánh cấp 2: AI
    B2 --> B2_1["Part 01: XGBoost Engine"]:::leaf
    B2_1 --> B2_1_1["Tập dữ liệu CICIoT2023"]:::leaf
    B2_1 --> B2_1_2["Trích xuất 47 đặc trưng mạng"]:::leaf
    B2_1 --> B2_1_3["Lấy mẫu Reservoir Sampling"]:::leaf
    B2 --> B2_2["7 Lớp Phân Loại"]:::leaf
    B2_2 --> B2_2_1["Benign, DDoS, DoS, BruteForce, Recon, Mirai, Spoofing"]:::leaf

    %% Nhánh cấp 2: Cảm biến
    B3 --> B3_1["Part 05: Real-time IDS"]:::leaf
    B3_1 --> B3_1_1["Suricata Packet Sniffer"]:::leaf
    B3_1 --> B3_1_2["FlowAccumulator (Tính 47 chỉ số)"]:::leaf
    B3_1 --> B3_1_3["Suy luận AI trong mili-giây"]:::leaf

    %% Nhánh cấp 2: Trung tâm xử lý
    B4 --> B4_1["Part 03: FastAPI Logging"]:::leaf
    B4_1 --> B4_1_1["Chuẩn hóa Khung MITRE ATT&CK"]:::leaf
    B4_1 --> B4_1_2["Cơ sở dữ liệu PostgreSQL & Redis"]:::leaf
    B4 --> B4_2["Part 06: SIEM Analytics"]:::leaf
    B4_2 --> B4_2_1["Elasticsearch & Kibana"]:::leaf
    B4_2 --> B4_2_2["Tương quan sự kiện APT"]:::leaf

    %% Nhánh cấp 2: UI
    B5 --> B5_1["Part 04: SOC React Dashboard"]:::leaf
    B5_1 --> B5_1_1["Biểu đồ đòn tấn công Real-time"]:::leaf
    B5_1 --> B5_1_2["Xuất báo cáo sự cố an ninh"]:::leaf
    B5 --> B5_2["Part 08: Grafana Monitoring"]:::leaf
    B5_2 --> B5_2_1["Giám sát tài nguyên CPU, RAM, API metrics"]:::leaf

    %% Nhánh cấp 2: Bảo mật
    B6 --> B6_1["Part 07: Security Hardening"]:::leaf
    B6_1 --> B6_1_1["WAF ModSecurity CRS + Anti-Pivot"]:::leaf
    B6 --> B6_2["Part 08: Keycloak IAM & SSO"]:::leaf
    B6_2 --> B6_2_1["Phân quyền người dùng theo vai trò RBAC"]:::leaf
    B6 --> B6_3["Part 09: Hồ Sơ Tài Liệu ADR"]:::leaf

---

## 3. SƠ ĐỒ MỐI LIÊN HỆ 9 MODULE & LUỒNG DỮ LIỆU

```mermaid
graph TD
    subgraph ATTACKERS ["🌐 TIN TẶC / HACKER"]
        A1["Tấn công Web (HTTP:8088)"]
        A2["Tấn công SSH (Port:2222)"]
        A3["Quét gói tin Mạng (Raw Traffic)"]
    end

    subgraph PART7 ["🛡️ PART 07: BẢO MẬT & CÁCH LY"]
        WAF["WAF ModSecurity + Nginx Edge"]
        HA["HAProxy (SSH Edge Port 2222)"]
    end

    subgraph PART2_8 ["🕸️ BẪY MỒI NHỬ (PARTS 02 & 08)"]
        P2["Part 02: Web Honeypot (Flask)"]
        COW["Part 08: SSH Honeypot (Cowrie)"]
    end

    subgraph PART1_5 ["🧠 CẢM BIẾN AI (PARTS 01 & 05)"]
        SUR["Suricata Packet Sniffer"]
        AI_ENG["Part 01: XGBoost Model (.ubj)"]
        P5["Part 05: LiveFlowSensor Engine"]
    end

    subgraph PART3 ["⚡ PART 03: TRUNG TÂM XỬ LÝ DỮ LIỆU"]
        API["FastAPI Event Ingestion API"]
        MITRE["MITRE ATT&CK Mapper"]
        DB[("PostgreSQL")]
        REDIS[("Redis Cache")]
    end

    subgraph PART6 ["🔍 PART 06: SIEM & TƯƠNG QUAN"]
        FB["Filebeat"]
        ES[("Elasticsearch")]
        KIB["Kibana Analytics"]
    end

    subgraph PART4_8 ["📊 TRỰC QUAN HÓA & VẬN HÀNH (PARTS 04 & 08)"]
        DASH["Part 04: SOC React Dashboard"]
        KC["Keycloak SSO (IAM / RBAC)"]
        GRAF["Grafana Monitoring"]
    end

    %% Luồng kết nối
    A1 -->|Lọc qua WAF| WAF -->|Chuyển tiếp mồi nhử| P2
    A2 -->|Lọc qua Proxy| HA -->|Chuyển tiếp phiên ảo| COW
    A3 -->|Gói tin thô| SUR

    P2 -->|Part 02 Forwarder| API
    COW -->|Cowrie Forwarder| API
    SUR -->|Trích xuất 47 đặc trưng| P5
    AI_ENG -.->|Nạp mô hình| P5
    P5 -->|Gửi cảnh báo AI| API

    API --> MITRE --> DB
    API --> REDIS
    API -.->|Thu gom Log| FB --> ES --> KIB

    KC -->|Cấp phát Token| DASH
    KC -->|Cấp quyền OAuth2| GRAF
    DASH <-->|Truy vấn REST API| API
    GRAF <-->|Đo lường Metrics| API
```

---

## 4. PHÂN TÍCH CHI TIẾT 9 MODULE

### 🧠 [Part 01: AI / Machine Learning (AI_ML)](file:///d:/A/A_5chai/honey_pot/part_01_AI_ML)
- **Nhiệm vụ**: Huấn luyện mô hình trí tuệ nhân tạo **XGBoost (eXtreme Gradient Boosting)** trên tập dữ liệu chuẩn quốc tế **CICIoT2023**.
- **Cơ chế hoạt động**:
  - `cleaner.py`: Làm sạch dữ liệu, xử lý giá trị vô cực (`inf`), giá trị rỗng (`NaN`) và loại bỏ dòng trùng lặp.
  - `sampler.py`: Dùng thuật toán **Reservoir Sampling** lấy mẫu ngẫu nhiên có trọng số (100.000 dòng/lớp) để cân bằng dữ liệu lớn mà không tốn RAM.
  - `train.py`: Dựng 300 cây quyết định tăng cường (`hist` method) và xuất ra file mô hình tối ưu `xgboost_original.ubj`.
  - `evaluate.py`: Đo lường khoa học các chỉ số `Precision`, `Recall`, `F1-score` và `False Positive Rate (FPR)`.

### 🕸️ [Part 02: Web Honeypot (WEB_HONEYPOT)](file:///d:/A/A_5chai/honey_pot/part_02_WEB_HONEYPOT)
- **Nhiệm vụ**: Đóng vai trò là Cổng Dịch vụ công mô phỏng để dụ dỗ tin tặc thực hiện các đòn tấn công ứng dụng web.
- **Cơ chế hoạt động**:
  - Chứa sẵn các điểm yếu giả lập: **SQL Injection (SQLi)**, **Cross-Site Scripting (XSS)**, **Path Traversal**, **Command Injection** và **Unrestricted File Upload**.
  - `detectors.py`: Tự động nhận diện chữ ký mã độc trong payload và băm vân tay mật khẩu (`password_fingerprint`).
  - Ghi toàn bộ dữ liệu truy cập vào SQLite cục bộ và lưu trữ tệp nghi ngờ vào thư mục cách ly `quarantine/`.

### ⚡ [Part 03: API Logging & Processing (API_LOGGING)](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING)
- **Nhiệm vụ**: Trái tim tiếp nhận và chuẩn hóa dữ liệu tập trung viết bằng **FastAPI**, lưu trữ trên **PostgreSQL** và **Redis**.
- **Cơ chế hoạt động**:
  - Cung cấp Ingestion API bảo mật cho Part 02, Cowrie và Part 05 đẩy dữ liệu về.
  - Tự động đối chiếu hành vi của tin tặc với ma trận **MITRE ATT&CK** *(ví dụ: T1059 Command Execution, T1110 Brute Force, T1190 Exploit Public-Facing App)*.
  - Cung cấp các endpoint REST API bảo vệ bằng xác thực JWT (Keycloak) cho Dashboard truy vấn.

### 📊 [Part 04: Dashboard Analytics (DASHBOARD_ANALYTICS)](file:///d:/A/A_5chai/honey_pot/part_04_DASHBOARD_ANALYTICS)
- **Nhiệm vụ**: Bảng điều khiển trung tâm SOC hiện đại dành cho Chuyên viên An ninh mạng viết bằng **React, Vite và TailwindCSS**.
- **Cơ chế hoạt động**:
  - Đăng nhập bảo mật qua **Keycloak SSO (OpenID Connect / PKCE S256)**.
  - Hiển thị biểu đồ phân bố đòn tấn công, danh sách IP nguồn, chi tiết các lệnh SSH tin tặc đã gõ.
  - Cho phép xuất báo cáo sự cố an ninh (Incident Report) phục vụ công tác điều tra.

### 👁️ [Part 05: IDS & ML Detection (IDS_ML_DETECTION)](file:///d:/A/A_5chai/honey_pot/part_05_IDS_ML_DETECTION)
- **Nhiệm vụ**: Cảm biến mạng thời gian thực kết hợp giữa **Suricata IDS** và mô hình **XGBoost AI**.
- **Cơ chế hoạt động**:
  - `LiveFlowSensor`: Lắng nghe trực tiếp các gói tin đi qua card mạng máy chủ.
  - `FlowAccumulator`: Tính toán và trích xuất đúng **47 đặc trưng kỹ thuật** của luồng mạng (độ dài, thời lượng, cờ TCP, tốc độ gói tin).
  - Đưa vào mô hình XGBoost để suy luận (Inference) và đẩy ngay cảnh báo về Part 03 trong mili-giây.

### 🔍 [Part 06: SIEM & Alerting (SIEM_ALERTING)](file:///d:/A/A_5chai/honey_pot/part_06_SIEM_ALERTING)
- **Nhiệm vụ**: Hệ thống phân tích tương quan sự kiện an ninh cấp độ doanh nghiệp (**Elasticsearch, Kibana, Filebeat**).
- **Cơ chế hoạt động**:
  - Thu gom toàn bộ log hệ thống vào Elasticsearch để tìm kiếm siêu tốc.
  - Chạy các kịch bản tương quan (Correlation Engine) để phát hiện các chiến dịch tấn công diện rộng (**APT**).

### 🛡️ [Part 07: Security Hardening (SECURITY_HARDENING)](file:///d:/A/A_5chai/honey_pot/part_07_SECURITY_HARDENING)
- **Nhiệm vụ**: Thiết lập áo giáp bảo vệ và cách ly an toàn cho chính Honeypot.
- **Cơ chế hoạt động**:
  - Triển khai **Tường lửa Web ModSecurity WAF** với bộ luật OWASP CRS.
  - Phân vùng mạng nội bộ (Internal Networks) ngăn không cho tin tặc nhảy từ Honeypot sang máy thật (**Anti-Pivot**).

### 🐳 [Part 08: Docker Deployment (DOCKER_DEPLOYMENT)](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT)
- **Nhiệm vụ**: Đóng gói và tự động hóa toàn bộ hệ thống bằng **Docker Compose**.
- **Cơ chế hoạt động**:
  - Quản lý dịch vụ định danh **Keycloak IAM**, máy chủ proxy SSH **HAProxy**, giám sát **Grafana & Prometheus**.
  - Cung cấp script khởi động thông minh [run.bat](file:///d:/A/A_5chai/honey_pot/run.bat) và [start-system.ps1](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT/start-system.ps1) giúp chạy mượt mà trên môi trường Windows.

### 📚 [Part 09: Documentation (DOCUMENTATION)](file:///d:/A/A_5chai/honey_pot/part_09_DOCUMENTATION)
- **Nhiệm vụ**: Hồ sơ tài liệu khoa học, kiến trúc hệ thống và hướng dẫn vận hành toàn diện.

---

## 5. CÁC ĐIỂM NÚT TRUNG TÂM CỐT LÕI (GOD NODES)

Dựa trên phân tích mạng lưới kết nối của công cụ **Graphify**, đây là **10 điểm nút quan trọng nhất** quyết định toàn bộ hoạt động của dự án:

| Điểm nút (Node) | Module | Số lượng liên kết | Ý nghĩa & Vai trò cốt lõi |
| :--- | :--- | :---: | :--- |
| **`feature_names`** | Part 01 & 05 | **47 edges** | Bộ 47 đặc trưng lưu lượng mạng làm cầu nối giữa dữ liệu thô và mô hình AI. |
| **`FlowAccumulator`** | Part 05 | **21 edges** | Bộ gom nhóm và tính toán các chỉ số thống kê mạng thời gian thực. |
| **`Settings`** | Part 03 | **18 edges** | Cấu hình bảo mật trung tâm của toàn bộ Backend API và cơ sở dữ liệu. |
| **`prepare_labeled_chunk()`** | Part 01 | **15 edges** | Hàm tiền xử lý làm sạch và chuẩn hóa schema dữ liệu trước khi huấn luyện. |
| **`XGBoostPredictor`** | Part 05 | **13 edges** | Đối tượng thực thi nạp mô hình AI và thực hiện phán đoán trực tiếp trên gói tin. |
| **`record_attack()`** | Part 02 | **13 edges** | Hàm cốt lõi của Web Honeypot bắt giữ payload và bóc tách dấu vết kẻ tấn công. |
| **`FlowTable`** | Part 05 | **12 edges** | Bảng quản lý trạng thái các luồng kết nối mạng IP/Port đang diễn ra. |
| **`Event`** | Part 03 | **12 edges** | Cấu trúc dữ liệu chuẩn hóa của mọi sự kiện an ninh trong toàn bộ hệ thống. |
| **`LiveFlowSensor`** | Part 05 | **11 edges** | Cảm biến lắng nghe lưu lượng card mạng và kích hoạt suy luận AI. |
| **`ClassReservoirSampler`**| Part 01 | **10 edges** | Thuật toán lấy mẫu dữ liệu lớn cân bằng lớp chống tràn bộ nhớ RAM. |

---

## 6. BẢNG GIẢI THÍCH THUẬT NGỮ CHUYÊN NGÀNH

- **Honeypot**: Hệ thống mồi nhử an ninh mạng được thiết kế có chủ đích để dụ tin tặc tấn công nhằm thu thập thông tin và phân tích kỹ thuật của kẻ tấn công.
- **XGBoost (eXtreme Gradient Boosting)**: Thuật toán học máy kết hợp nhiều cây quyết định với độ chính xác và tốc độ xử lý hàng đầu hiện nay.
- **IDS (Intrusion Detection System)**: Hệ thống giám sát lưu lượng mạng và đưa ra cảnh báo khi phát hiện dấu hiệu xâm nhập đáng ngờ.
- **WAF (Web Application Firewall)**: Tường lửa bảo vệ ứng dụng web khỏi các đòn tấn công phổ biến như SQLi, XSS.
- **SIEM (Security Information and Event Management)**: Hệ thống quản lý và tương quan các sự kiện an ninh từ nhiều nguồn dữ liệu khác nhau.
- **MITRE ATT&CK**: Khung phân loại và chuẩn hóa các chiến thuật, kỹ thuật tấn công của tin tặc dựa trên các quan sát thực tế trên thế giới.
- **SSO (Single Sign-On) & RBAC**: Cơ chế đăng nhập 1 lần cho nhiều dịch vụ và phân quyền truy cập dựa trên vai trò chức vụ của người dùng.
- **Anti-Pivot**: Biện pháp bảo mật cách ly mạng nhằm ngăn chặn tin tặc sau khi chiếm được bẫy Honeypot dùng nó làm bàn đạp tấn công sang các máy chủ khác.
- **Reservoir Sampling**: Thuật toán lấy mẫu ngẫu nhiên đồng đều trên một luồng dữ liệu cực lớn mà không cần nạp toàn bộ vào bộ nhớ RAM.
