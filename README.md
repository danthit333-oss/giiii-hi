# Hệ thống Web Honeypot và phân tích tấn công

Dự án được chia thành chín phần độc lập nhưng dùng chung một luồng dữ liệu. Các dự án Python được quản lý bằng UV và có `pyproject.toml` cùng `uv.lock` riêng.

| Part | Vai trò | Kết quả chính |
|---|---|---|
| 01 | AI/ML | XGBoost gốc, 7 lớp, model UBJ và báo cáo đánh giá |
| 02 | Web Honeypot | Website Bootstrap có 10 bề mặt tương tác được containment |
| 03 | API & Logging | FastAPI, OIDC/API key, dedup, PostgreSQL và Redis cache |
| 04 | Dashboard | React, Tailwind, ECharts, Keycloak PKCE, CSV và chi tiết event |
| 05 | IDS & ML | Chuẩn hóa Suricata/Zeek, rule IDS và hợp đồng 46 feature |
| 06 | SIEM | ECS, Elasticsearch và bốn correlation rule |
| 07 | Hardening | Nginx, ModSecurity CRS, NetworkPolicy và threat model |
| 08 | Deployment | Docker Compose, Keycloak SSO/RBAC, secret, health check, network tách vùng |
| 09 | Evaluation | 10 kịch bản kiểm thử và báo cáo JSON/Markdown/CSV/PNG |

## Luồng dữ liệu

```text
HTTP client -> Edge WAF -> Flask Honeypot --+
SSH client  -> SSH edge -> Cowrie -----------+-> Part 03 -> Dashboard
                                             +-> Filebeat -> Elasticsearch/Kibana
Suricata/Zeek -> Part 05 --------------------+-> Prometheus -> Grafana
                                             +-> Part 09 report
```

Part 02 là mồi nhử và không truy cập dữ liệu thật. Part 07–08 cô lập lure plane khỏi control/data plane. Part 09 mặc định chỉ cho phép chạy kịch bản trên loopback.

## Chạy toàn bộ stack

Trên Windows, chạy `run.bat` tại thư mục gốc hoặc double-click file này. Script tự mở Docker Desktop, dựng core, monitoring, SIEM, mở Web Honeypot TCP `8080` cho `LocalSubnet`, rồi chạy Suricata + XGBoost trên card mạng có default gateway. Sensor mặc định chỉ bắt TCP đi vào Web Honeypot `8080` hoặc SSH mồi `2222`; control plane `8088` không được capture:

```bat
run.bat
```

Chọn adapter khác khi Honeypot được publish trên card mạng đó:

```bat
run.bat "Ethernet"
```

Không chạy sensor mạng hoặc không tự mở trình duyệt:

```bat
run.bat -NoSensor -NoBrowser
```

Chạy core thủ công:

```powershell
cd part_08_DOCKER_DEPLOYMENT
.\local-up.ps1
```

Script sinh secret ngẫu nhiên trong thư mục Git-ignore và không tạo traffic tấn công hoặc dữ liệu mẫu. Máy cùng LAN truy cập Web Honeypot qua `http://<IP-LAN-MÁY-HONEYPOT>:8080`; Dashboard/API vẫn chỉ ở `127.0.0.1:8088`, SSH Cowrie vẫn chỉ ở `127.0.0.1:2222`. Dashboard, Grafana, Kibana và Prometheus dùng chung tài khoản Keycloak với RBAC theo nhiệm vụ. Hướng dẫn đầy đủ nằm trong `part_08_DOCKER_DEPLOYMENT/HUONG_DAN_SU_DUNG.md`; ma trận quyền nằm trong `part_08_DOCKER_DEPLOYMENT/KEYCLOAK_RBAC.md`. Trên Windows, Suricata chạy native bằng Npcap; container Suricata trong profile `network` dành cho Linux.

Không đưa cấu hình lab trực tiếp lên Internet, không nối với dữ liệu nghiệp vụ, và chỉ thử nghiệm trên hệ thống do bạn sở hữu hoặc được cấp phép rõ ràng.
