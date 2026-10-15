# BẢNG ĐỐI CHIẾU VÀ ĐÍNH CHÍNH KỸ THUẬT (CHAPTER 3 CORRECTIONS)

Bản tài liệu này rà soát, kiểm tra trực tiếp mã nguồn và môi trường runtime *(thời gian chạy thực tế)* của toàn bộ dự án nhằm giải quyết dứt điểm các điểm mâu thuẫn, đính chính các nhận định chưa chuẩn xác giữa lý thuyết, cấu hình và triển khai thực tế.

---

### 1. PostgreSQL có bảng `alerts` riêng hay chỉ có bảng `events`?
- **Kết luận**: **KHÔNG CÓ bảng `alerts` riêng**. Database PostgreSQL chỉ có **DUY NHẤT một bảng là `events`**.
- **File đối chiếu**: [part_03_API_LOGGING/app/models.py](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING/app/models.py)
- **Đoạn code thực tế (Dòng 18–25)**:
  ```python
  class Event(Base):
      __tablename__ = "events"
      __table_args__ = (
          UniqueConstraint("sensor_id", "source_event_id", name="uq_sensor_source_event"),
          Index("ix_events_observed_at", "observed_at"),
          Index("ix_events_vulnerability", "vulnerability"),
          Index("ix_events_source_ip", "source_ip"),
      )
  ```
- **Trạng thái**: `[Source Verified Only]` & `[Runtime Verified]`.
- **CORRECTION**: Báo cáo trước có đoạn ghi "lưu vào bảng events và alerts". **Đính chính**: Hệ thống chỉ định nghĩa và khởi tạo duy nhất bảng `events`. Mọi thực thể cảnh báo đều được chuẩn hóa thành một Event.

---

### 2. Correlation alert lưu vào bảng nào?
- **Kết luận**: Correlation alert được lưu trực tiếp vào bảng **`events`** thông qua API `POST /api/v1/events`.
- **File đối chiếu**: 
  - [part_06_SIEM_ALERTING/siem/run.py](file:///d:/A/A_5chai/honey_pot/part_06_SIEM_ALERTING/siem/run.py) (Dòng 40–44)
  - [part_06_SIEM_ALERTING/siem/correlation.py](file:///d:/A/A_5chai/honey_pot/part_06_SIEM_ALERTING/siem/correlation.py) (Dòng 27–43)
- **Đoạn code thực tế**:
  Trong `siem/run.py`:
  ```python
  result = post_part3_alerts(args.part3_url, args.ingest_key, [alert.to_part3_event() for alert in alerts])
  ```
  Trong `siem/correlation.py`:
  ```python
  def to_part3_event(self) -> dict[str, object]:
      evidence = ",".join(self.evidence_ids)
      source_id = hashlib.sha256(f"{self.rule_id}|{self.source_ip}|{evidence}".encode()).hexdigest()
      return {
          "source_event_id": f"correlation-{source_id}",
          "observed_at": self.observed_at,
          "event_type": "alert",
          "vulnerability": self.rule_id,
          "severity": self.severity,
          "source_ip": self.source_ip,
          "method": "CORRELATE",
          "path": "siem://correlation",
          "payload": self.description,
          "signals": [f"correlation:{self.rule_id}"],
          "outcome": "analyst_review_required",
          "request_metadata": {"title": self.title, "evidence_ids": list(self.evidence_ids)},
      }
  ```
- **Trạng thái**: `[Source Verified Only]`.
- **CORRECTION**: Cảnh báo tương quan không có bảng lưu riêng mà đóng vai trò là một sự kiện có `event_type = "alert"`, `method = "CORRELATE"`, `path = "siem://correlation"` và được lưu trong bảng `events`.

---

### 3. Redis TTL là 30 hay 60 giây?
- **Kết luận**: Giá trị mặc định thực tế là **30 giây**.
- **File đối chiếu**: [part_03_API_LOGGING/app/config.py](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING/app/config.py) (Dòng 40)
- **Đoạn code thực tế**:
  ```python
  redis_cache_ttl_seconds: int = Field(default=30, ge=1, le=3600)
  ```
  Trong `part_08_DOCKER_DEPLOYMENT/compose.yaml` không thiết lập đè biến môi trường `PART3_REDIS_CACHE_TTL_SECONDS`.
- **Trạng thái**: `[Config Only]` & `[Source Verified Only]`.
- **CORRECTION**: Báo cáo trước ghi "TTL 60 giây". **Đính chính**: Cấu hình chuẩn trong mã nguồn là **30 giây** (`default=30`).

---

### 4. Dashboard dùng ECharts hay Chart.js?
- **Kết luận**: Dashboard sử dụng thư viện **Apache ECharts** (`echarts`), **KHÔNG** sử dụng Chart.js.
- **File đối chiếu**: 
  - [part_04_DASHBOARD_ANALYTICS/package.json](file:///d:/A/A_5chai/honey_pot/part_04_DASHBOARD_ANALYTICS/package.json) (Dòng 15)
  - [part_04_DASHBOARD_ANALYTICS/src/components/EChart.jsx](file:///d:/A/A_5chai/honey_pot/part_04_DASHBOARD_ANALYTICS/src/components/EChart.jsx) (Dòng 1–15)
- **Đoạn code thực tế**:
  Trong `package.json`:
  ```json
  "dependencies": {
    "@tailwindcss/vite": "latest",
    "@vitejs/plugin-react": "latest",
    "echarts": "latest",
    "keycloak-js": "latest",
    "react": "latest",
    "react-dom": "latest",
    "tailwindcss": "latest",
    "vite": "latest"
  }
  ```
  Trong `EChart.jsx`:
  ```javascript
  import * as echarts from "echarts";
  ```
- **Trạng thái**: `[Source Verified Only]`.
- **CORRECTION**: Báo cáo trước nhắc đến "Chart.js". **Đính chính**: Toàn bộ biểu đồ phân tích thời gian và phân bố lỗ hổng trên Dashboard được render bằng component `EChart.jsx` bọc quanh thư viện `echarts`.

---

### 5. Database/event schema có trường `mitre_technique` không?
- **Kết luận**: **KHÔNG CÓ**. Cả schema Pydantic và model SQLAlchemy đều không có cột/thuộc tính `mitre_technique`. Cấu hình schema đặt `extra="forbid"`, nếu client gửi trường này sẽ bị lỗi `422 Unprocessable Entity`.
- **File đối chiếu**: 
  - [part_03_API_LOGGING/app/schemas.py](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING/app/schemas.py) (Dòng 15–42)
  - [part_03_API_LOGGING/app/models.py](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING/app/models.py) (Dòng 27–46)
- **Đoạn code thực tế**:
  ```python
  class EventIn(BaseModel):
      model_config = ConfigDict(extra="forbid", populate_by_name=True)
      source_event_id: str
      observed_at: datetime
      event_type: EventType
      vulnerability: str | None
      severity: Severity
      source_ip: str
      forwarded_for: str
      method: str
      path: str
      status_code: int | None
      payload: str
      signals: list[str]
      outcome: str
      request_metadata: dict[str, object]
  ```
- **Trạng thái**: `[Source Verified Only]`.
- **CORRECTION**: Khóa luận không được ghi `mitre_technique` là một trường cơ sở dữ liệu. Nếu cần đưa thông tin kỹ thuật ATT&CK vào, hệ thống chỉ có thể lưu trong mảng `signals` (ví dụ: `signals: ["attack:t1059.004"]`) hoặc trong `request_metadata`.

---

### 6. Event Drawer có thực sự hiển thị MITRE ATT&CK không?
- **Kết luận**: **KHÔNG**. Component `EventDrawer.jsx` hoàn toàn không có giao diện hiển thị MITRE ATT&CK.
- **File đối chiếu**: [part_04_DASHBOARD_ANALYTICS/src/components/EventDrawer.jsx](file:///d:/A/A_5chai/honey_pot/part_04_DASHBOARD_ANALYTICS/src/components/EventDrawer.jsx) (Dòng 11–26)
- **Đoạn code thực tế**:
  `EventDrawer.jsx` chỉ render các trường:
  - `Event ID` (`event.id`)
  - `Thời gian` (`event.observed_at`)
  - `Nguồn truy cập` (`event.source_ip`)
  - `Nguồn theo dõi` (`sensorLabel(event.sensor_id)`)
  - `Hoạt động` (`event.method event.path`)
  - `Mức độ` (`event.severity`)
  - `Kết quả` (`event.outcome`)
  - `Dấu hiệu` (`event.signals`)
  - Thông số AI nếu có: `Mô hình AI`, `Độ tin cậy`, `Số packet`, `Giao thức` (lấy từ `metadata`)
  - `Nội dung đã ghi nhận` (`event.payload`)
  - `Thông tin kỹ thuật` (`JSON.stringify(metadata, null, 2)`)
- **Trạng thái**: `[Source Verified Only]`.
- **CORRECTION**: Báo cáo trước mô tả Event Drawer có khung phân tích MITRE ATT&CK. **Đính chính**: Đây là điểm khác biệt giữa ý tưởng thiết kế và mã nguồn thực tế. Giao diện thực tế chỉ hiển thị các trường chuẩn trên.

---

### 7. Field chuẩn là `source_ip` hay `src_ip`?
- **Kết luận**: Tên trường chuẩn trong toàn bộ Part 3 API, Database models và schemas là **`source_ip`**.
- **File đối chiếu**: 
  - [part_03_API_LOGGING/app/models.py](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING/app/models.py) (Dòng 37)
  - [part_03_API_LOGGING/app/schemas.py](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING/app/schemas.py) (Dòng 30)
- **Đoạn code thực tế**:
  ```python
  source_ip: Mapped[str] = mapped_column(String(64), nullable=False)
  ```
  *(Lưu ý: Tên trường `src_ip` chỉ xuất hiện trong log thô EVE JSON của Suricata. Khi qua bộ chuyển đổi `ids_bridge/normalizers.py`, nó được ánh xạ bắt buộc thành `source_ip`)*.
- **Trạng thái**: `[Source Verified Only]`.
- **CORRECTION**: Chuẩn hóa toàn bộ văn bản và tài liệu kỹ thuật sang `source_ip`, không dùng `src_ip` khi nói về cơ sở dữ liệu và API trung tâm.

---

### 8. Payload chuẩn là `payload` hay `raw_payload`?
- **Kết luận**: Tên trường chuẩn trong Database models và API schemas là **`payload`**.
- **File đối chiếu**: 
  - [part_03_API_LOGGING/app/models.py](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING/app/models.py) (Dòng 42)
  - [part_03_API_LOGGING/app/schemas.py](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING/app/schemas.py) (Dòng 35)
- **Đoạn code thực tế**:
  ```python
  payload: Mapped[str] = mapped_column(Text, default="", nullable=False)
  ```
- **Trạng thái**: `[Source Verified Only]`.
- **CORRECTION**: Báo cáo trước có chỗ viết `raw_payload`. **Đính chính**: Tên thuộc tính trong mã nguồn thực tế là `payload`.

---

### 9. `part2-forwarder` có checkpoint bền vững hay cursor chỉ nằm trong RAM?
- **Kết luận**: Cursor **CHỈ NẰM TRONG RAM**, hoàn toàn **KHÔNG có checkpoint bền vững** lưu xuống đĩa hoặc database.
- **File đối chiếu**: [part_03_API_LOGGING/scripts/forward_part2.py](file:///d:/A/A_5chai/honey_pot/part_03_API_LOGGING/scripts/forward_part2.py) (Dòng 109–131)
- **Đoạn code thực tế**:
  ```python
  cursor_time = ""
  cursor_id = ""
  total = 0
  while True:
      rows = read_batch(
          database,
          cursor_time=cursor_time,
          cursor_id=cursor_id,
          limit=args.batch_size,
      )
      if rows:
          ...
          cursor_time = rows[-1]["created_at"]
          cursor_id = rows[-1]["id"]
          continue
  ```
  Khi tiến trình `forward_part2` bị khởi động lại, `cursor_time` và `cursor_id` bị reset về rỗng `""`. Tiến trình sẽ đọc lại toàn bộ từ đầu bảng `events` của SQLite. Tuy nhiên, API Part 3 có cơ chế Deduplication dựa trên cặp khóa `(sensor_id, source_event_id)` nên các sự kiện cũ sẽ bị coi là duplicate và bỏ qua, không gây lỗi hệ thống.
- **Trạng thái**: `[Source Verified Only]`.
- **CORRECTION**: Báo cáo trước ghi "cơ chế checkpoint ghi nhớ vị trí". **Đính chính**: Không có tệp checkpoint bền vững trên ổ đĩa. Vị trí đọc chỉ lưu trong biến bộ nhớ RAM của tiến trình Python và dựa hoàn toàn vào cơ chế deduplication ở phía API khi có sự cố khởi động lại.

---

### 10. Hệ thống thực tế có bao nhiêu Docker network?
- **Kết luận**: Hệ thống định nghĩa chính xác **7 Docker networks** (trong đó có 5 mạng nội bộ `internal: true`).
- **File đối chiếu**: [part_08_DOCKER_DEPLOYMENT/compose.yaml](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT/compose.yaml) (Dòng 656–668)
- **Đoạn code thực tế**:
  ```yaml
  networks:
    public: {}
    lan_ingress: {}
    lure:
      internal: true
    control:
      internal: true
    data:
      internal: true
    siem:
      internal: true
    auth:
      internal: true
  ```
- **Trạng thái**: `[Config Only]`.
- **CORRECTION**: Báo cáo trước ghi "5 Networks". **Đính chính**: Có tổng cộng **7 networks** được khai báo tường minh trong `compose.yaml`.
