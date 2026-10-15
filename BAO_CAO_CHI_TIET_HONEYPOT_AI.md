# BÁO CÁO DỰ ÁN: HỆ THỐNG WEB HONEYPOT THỜI GIAN THỰC TÍCH HỢP TRÍ TUỆ NHÂN TẠO VÀ TRUNG TÂM ĐIỀU HÀNH AN NINH MẠNG (SOC)

> **Chuyên ngành**: An toàn thông tin *(Information Security — ngành bảo vệ hệ thống thông tin khỏi bị truy cập, sử dụng, tiết lộ hoặc phá hủy trái phép)*  
> **Hướng nghiên cứu**: Phát hiện và phân tích tấn công mạng bằng kỹ thuật Học máy *(Machine Learning)* kết hợp Bẫy mồi nhử *(Honeypot)*  
> **Công nghệ cốt lõi**: XGBoost · Flask · FastAPI · React · Suricata · Elasticsearch · Docker · Keycloak

---

## MỤC LỤC

- [CHƯƠNG 1. TỔNG QUAN VỀ HONEYPOT VÀ BÀI TOÁN PHÁT HIỆN, PHÂN TÍCH TẤN CÔNG MẠNG](#chương-1)
  - [1.1. Bối cảnh và thực trạng an toàn, an ninh mạng](#11-bối-cảnh-và-thực-trạng-an-toàn-an-ninh-mạng)
    - [1.1.1. Xu hướng gia tăng các cuộc tấn công mạng](#111-xu-hướng-gia-tăng-các-cuộc-tấn-công-mạng)
    - [1.1.2. Nguy cơ đối với hệ thống dịch vụ web](#112-nguy-cơ-đối-với-hệ-thống-dịch-vụ-web)
    - [1.1.3. Yêu cầu phát hiện và phân tích tấn công](#113-yêu-cầu-phát-hiện-và-phân-tích-tấn-công)
  - [1.2. Tổng quan về các giải pháp phòng thủ mạng](#12-tổng-quan-về-các-giải-pháp-phòng-thủ-mạng)
    - [1.2.1. Tường lửa (Firewall)](#121-tường-lửa-firewall)
    - [1.2.2. Hệ thống IDS/IPS](#122-hệ-thống-idsips)
    - [1.2.3. SIEM và SOC](#123-siem-và-soc)
    - [1.2.4. Hạn chế của các phương pháp phòng thủ truyền thống](#124-hạn-chế-của-các-phương-pháp-phòng-thủ-truyền-thống)
  - [1.3. Tổng quan về Honeypot](#13-tổng-quan-về-honeypot)
    - [1.3.1. Khái niệm Honeypot](#131-khái-niệm-honeypot)
    - [1.3.2. Nguyên lý hoạt động](#132-nguyên-lý-hoạt-động)
    - [1.3.3. Vai trò của Honeypot trong phát hiện và phân tích tấn công](#133-vai-trò-của-honeypot-trong-phát-hiện-và-phân-tích-tấn-công)
  - [1.4. Phân loại Honeypot](#14-phân-loại-honeypot)
    - [1.4.1. Phân loại theo mức độ tương tác](#141-phân-loại-theo-mức-độ-tương-tác)
    - [1.4.2. Low-Interaction Honeypot](#142-low-interaction-honeypot)
    - [1.4.3. Medium-Interaction Honeypot](#143-medium-interaction-honeypot)
    - [1.4.4. High-Interaction Honeypot](#144-high-interaction-honeypot)
    - [1.4.5. Phân loại theo mục đích triển khai](#145-phân-loại-theo-mục-đích-triển-khai)
    - [1.4.6. Production Honeypot và Research Honeypot](#146-production-honeypot-và-research-honeypot)
  - [1.5. Web Honeypot và các kỹ thuật tấn công ứng dụng web](#15-web-honeypot-và-các-kỹ-thuật-tấn-công-ứng-dụng-web)
    - [1.5.1. Đặc điểm và nguyên lý hoạt động của Web Honeypot](#151-đặc-điểm-và-nguyên-lý-hoạt-động-của-web-honeypot)
    - [1.5.2. SQL Injection](#152-sql-injection)
    - [1.5.3. Cross-Site Scripting (XSS)](#153-cross-site-scripting-xss)
    - [1.5.4. File Inclusion và Path Traversal](#154-file-inclusion-và-path-traversal)
    - [1.5.5. Brute Force và Credential Attacks](#155-brute-force-và-credential-attacks)
    - [1.5.6. Command Injection](#156-command-injection)
    - [1.5.7. XML External Entity (XXE)](#157-xml-external-entity-xxe)
  - [1.6. Các nghiên cứu và giải pháp liên quan](#16-các-nghiên-cứu-và-giải-pháp-liên-quan)
    - [1.6.1. Các hệ thống Honeypot tiêu biểu](#161-các-hệ-thống-honeypot-tiêu-biểu)
    - [1.6.2. Các giải pháp Web Honeypot hiện có](#162-các-giải-pháp-web-honeypot-hiện-có)
    - [1.6.3. Ứng dụng học máy trong phát hiện và phân loại tấn công](#163-ứng-dụng-học-máy-trong-phát-hiện-và-phân-loại-tấn-công)
  - [1.7. Khoảng trống nghiên cứu và định hướng đề tài](#17-khoảng-trống-nghiên-cứu-và-định-hướng-đề-tài)
    - [1.7.1. Hạn chế của các hệ thống hiện nay](#171-hạn-chế-của-các-hệ-thống-hiện-nay)
    - [1.7.2. Bài toán nghiên cứu đặt ra](#172-bài-toán-nghiên-cứu-đặt-ra)
    - [1.7.3. Mục tiêu và phạm vi nghiên cứu](#173-mục-tiêu-và-phạm-vi-nghiên-cứu)

- [CHƯƠNG 2. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG WEB HONEYPOT](#chương-2)
  - [2.1. Phân tích yêu cầu hệ thống](#21-phân-tích-yêu-cầu-hệ-thống)
    - [2.1.1. Yêu cầu chức năng](#211-yêu-cầu-chức-năng)
    - [2.1.2. Yêu cầu phi chức năng](#212-yêu-cầu-phi-chức-năng)
    - [2.1.3. Yêu cầu bảo mật và cô lập hệ thống](#213-yêu-cầu-bảo-mật-và-cô-lập-hệ-thống)
  - [2.2. Mô hình mối đe dọa](#22-mô-hình-mối-đe-dọa)
    - [2.2.1. Tài sản cần bảo vệ](#221-tài-sản-cần-bảo-vệ)
    - [2.2.2. Tác nhân và phương thức tấn công](#222-tác-nhân-và-phương-thức-tấn-công)
    - [2.2.3. Phân tích đe dọa theo mô hình STRIDE](#223-phân-tích-đe-dọa-theo-mô-hình-stride)
  - [2.3. Kiến trúc tổng thể hệ thống](#23-kiến-trúc-tổng-thể-hệ-thống)
    - [2.3.1. Kiến trúc phân tầng](#231-kiến-trúc-phân-tầng)
    - [2.3.2. Phân vùng mạng và cơ chế ngăn chặn lan truyền](#232-phân-vùng-mạng-và-cơ-chế-ngăn-chặn-lan-truyền)
    - [2.3.3. Luồng dữ liệu trong hệ thống](#233-luồng-dữ-liệu-trong-hệ-thống)
  - [2.4. Thiết kế Web Honeypot](#24-thiết-kế-web-honeypot)
    - [2.4.1. Thiết kế giao diện mồi nhử](#241-thiết-kế-giao-diện-mồi-nhử)
    - [2.4.2. Thiết kế API giả lập](#242-thiết-kế-api-giả-lập)
    - [2.4.3. Thiết kế các điểm tương tác và bề mặt tấn công](#243-thiết-kế-các-điểm-tương-tác-và-bề-mặt-tấn-công)
    - [2.4.4. Thiết kế cơ chế ghi nhận và chuyển tiếp sự kiện](#244-thiết-kế-cơ-chế-ghi-nhận-và-chuyển-tiếp-sự-kiện)
  - [2.5. Thiết kế cơ chế phát hiện và phân tích tấn công](#25-thiết-kế-cơ-chế-phát-hiện-và-phân-tích-tấn-công)
    - [2.5.1. Phát hiện tấn công dựa trên luật](#251-phát-hiện-tấn-công-dựa-trên-luật)
    - [2.5.2. Phát hiện và phân loại lưu lượng bằng học máy](#252-phát-hiện-và-phân-loại-lưu-lượng-bằng-học-máy)
    - [2.5.3. Trích xuất đặc trưng luồng mạng](#253-trích-xuất-đặc-trưng-luồng-mạng)
    - [2.5.4. Phân tích Payload và xác định kỹ thuật tấn công](#254-phân-tích-payload-và-xác-định-kỹ-thuật-tấn-công)
  - [2.6. Thiết kế cơ chế thu thập và lưu trữ dữ liệu](#26-thiết-kế-cơ-chế-thu-thập-và-lưu-trữ-dữ-liệu)
    - [2.6.1. Thu thập Request HTTP và dữ liệu lưu lượng mạng](#261-thu-thập-request-http-và-dữ-liệu-lưu-lượng-mạng)
    - [2.6.2. Chuẩn hóa dữ liệu theo Elastic Common Schema (ECS)](#262-chuẩn-hóa-dữ-liệu-theo-elastic-common-schema-ecs)
    - [2.6.3. Khử trùng lặp dữ liệu bằng Redis](#263-khử-trùng-lặp-dữ-liệu-bằng-redis)
    - [2.6.4. Thiết kế mô hình lưu trữ PostgreSQL và Elasticsearch](#264-thiết-kế-mô-hình-lưu-trữ-postgresql-và-elasticsearch)
  - [2.7. Thiết kế cơ chế tương quan và cảnh báo](#27-thiết-kế-cơ-chế-tương-quan-và-cảnh-báo)
    - [2.7.1. Phân tích theo địa chỉ IP nguồn và phiên tương tác](#271-phân-tích-theo-địa-chỉ-ip-nguồn-và-phiên-tương-tác)
    - [2.7.2. Phân tích chuỗi tấn công đa tầng](#272-phân-tích-chuỗi-tấn-công-đa-tầng)
    - [2.7.3. Ánh xạ kỹ thuật tấn công theo MITRE ATT&CK](#273-ánh-xạ-kỹ-thuật-tấn-công-theo-mitre-attck)
  - [2.8. Thiết kế Dashboard giám sát SOC](#28-thiết-kế-dashboard-giám-sát-soc)
    - [2.8.1. Thiết kế bảng điều khiển tổng quan và thời gian thực](#281-thiết-kế-bảng-điều-khiển-tổng-quan-và-thời-gian-thực)
    - [2.8.2. Thiết kế giao diện truy vấn và điều tra sự kiện](#282-thiết-kế-giao-diện-truy-vấn-và-điều-tra-sự-kiện)
    - [2.8.3. Thiết kế cơ chế xác thực và phân quyền](#283-thiết-kế-cơ-chế-xác-thực-và-phân-quyền)

- [CHƯƠNG 3. XÂY DỰNG VÀ TRIỂN KHAI HỆ THỐNG WEB HONEYPOT](#chương-3)
  - [3.1. Môi trường và công nghệ triển khai](#31-môi-trường-và-công-nghệ-triển-khai)
    - [3.1.1. Môi trường phần cứng và hạ tầng mạng Lab](#311-môi-trường-phần-cứng-và-hạ-tầng-mạng-lab)
    - [3.1.2. Môi trường phần mềm và công nghệ sử dụng](#312-môi-trường-phần-mềm-và-công-nghệ-sử-dụng)
    - [3.1.3. Đóng gói và triển khai hệ thống bằng Docker Compose](#313-đóng-gói-và-triển-khai-hệ-thống-bằng-docker-compose)
  - [3.2. Xây dựng Web Honeypot](#32-xây-dựng-web-honeypot)
    - [3.2.1. Xây dựng Website mồi nhử bằng Flask và Bootstrap](#321-xây-dựng-website-mồi-nhử-bằng-flask-và-bootstrap)
    - [3.2.2. Xây dựng các bề mặt tấn công mô phỏng](#322-xây-dựng-các-bề-mặt-tấn-công-mô-phỏng)
    - [3.2.3. Hiện thực cơ chế cô lập và bảo vệ dữ liệu thực](#323-hiện-thực-cơ-chế-cô-lập-và-bảo-vệ-dữ-liệu-thực)
  - [3.3. Xây dựng hệ thống tiếp nhận và lưu trữ nhật ký](#33-xây-dựng-hệ-thống-tiếp-nhận-và-lưu-trữ-nhật-ký)
    - [3.3.1. Xây dựng Backend API tiếp nhận dữ liệu bằng FastAPI](#331-xây-dựng-backend-api-tiếp-nhận-dữ-liệu-bằng-fastapi)
    - [3.3.2. Xây dựng cơ chế khử trùng lặp nhật ký với Redis](#332-xây-dựng-cơ-chế-khử-trùng-lặp-nhật-ký-với-redis)
    - [3.3.3. Xây dựng cơ sở dữ liệu PostgreSQL](#333-xây-dựng-cơ-sở-dữ-liệu-postgresql)
    - [3.3.4. Đồng bộ dữ liệu chuẩn ECS vào Elasticsearch bằng Filebeat](#334-đồng-bộ-dữ-liệu-chuẩn-ecs-vào-elasticsearch-bằng-filebeat)
  - [3.4. Xây dựng hệ thống phát hiện và phân tích tấn công](#34-xây-dựng-hệ-thống-phát-hiện-và-phân-tích-tấn-công)
    - [3.4.1. Tích hợp Suricata IDS để giám sát lưu lượng mạng](#341-tích-hợp-suricata-ids-để-giám-sát-lưu-lượng-mạng)
    - [3.4.2. Xây dựng IDS/ML Bridge và trích xuất đặc trưng luồng mạng](#342-xây-dựng-idsml-bridge-và-trích-xuất-đặc-trưng-luồng-mạng)
    - [3.4.3. Tích hợp mô hình XGBoost để phân loại tấn công](#343-tích-hợp-mô-hình-xgboost-để-phân-loại-tấn-công)
    - [3.4.4. Xây dựng cơ chế tương quan sự kiện](#344-xây-dựng-cơ-chế-tương-quan-sự-kiện)
  - [3.5. Xây dựng Dashboard giám sát và điều hành SOC](#35-xây-dựng-dashboard-giám-sát-và-điều-hành-soc)
    - [3.5.1. Xây dựng giao diện trực quan bằng React, TailwindCSS và ECharts](#351-xây-dựng-giao-diện-trực-quan-bằng-react-tailwindcss-và-echarts)
    - [3.5.2. Tích hợp xác thực và phân quyền người dùng](#352-tích-hợp-xác-thực-và-phân-quyền-người-dùng)
    - [3.5.3. Xây dựng chức năng giám sát thời gian thực và báo cáo sự cố](#353-xây-dựng-chức-năng-giám-sát-thời-gian-thực-và-báo-cáo-sự-cố)

- [CHƯƠNG 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ HỆ THỐNG](#chương-4)
  - [4.1. Thiết lập môi trường và phương pháp thực nghiệm](#41-thiết-lập-môi-trường-và-phương-pháp-thực-nghiệm)
    - [4.1.1. Mô hình thử nghiệm và công cụ sử dụng](#411-mô-hình-thử-nghiệm-và-công-cụ-sử-dụng)
    - [4.1.2. Kịch bản kiểm thử Web Honeypot](#412-kịch-bản-kiểm-thử-web-honeypot)
    - [4.1.3. Kịch bản kiểm thử phát hiện tấn công mạng](#413-kịch-bản-kiểm-thử-phát-hiện-tấn-công-mạng)
  - [4.2. Đánh giá khả năng thu thập và xử lý dữ liệu](#42-đánh-giá-khả-năng-thu-thập-và-xử-lý-dữ-liệu)
    - [4.2.1. Độ đầy đủ của Payload và thông tin phiên](#421-độ-đầy-đủ-của-payload-và-thông-tin-phiên)
    - [4.2.2. Hiệu quả của cơ chế khử trùng lặp dữ liệu](#422-hiệu-quả-của-cơ-chế-khử-trùng-lặp-dữ-liệu)
  - [4.3. Đánh giá khả năng phát hiện tấn công](#43-đánh-giá-khả-năng-phát-hiện-tấn-công)
    - [4.3.1. Khả năng phát hiện của Web Honeypot và cơ chế dựa trên luật](#431-khả-năng-phát-hiện-của-web-honeypot-và-cơ-chế-dựa-trên-luật)
    - [4.3.2. Độ chính xác của mô hình XGBoost](#432-độ-chính-xác-của-mô-hình-xgboost)
    - [4.3.3. Ma trận nhầm lẫn và phân tích kết quả phân loại](#433-ma-trận-nhầm-lẫn-và-phân-tích-kết-quả-phân-loại)
  - [4.4. Đánh giá khả năng phân tích hành vi và tương quan sự kiện](#44-đánh-giá-khả-năng-phân-tích-hành-vi-và-tương-quan-sự-kiện)
  - [4.5. Đánh giá hiệu năng và độ trễ hệ thống](#45-đánh-giá-hiệu-năng-và-độ-trễ-hệ-thống)
  - [4.6. Đánh giá mức độ an toàn và khả năng cô lập hệ thống](#46-đánh-giá-mức-độ-an-toàn-và-khả-năng-cô-lập-hệ-thống)
  - [4.7. Phân tích ưu điểm, hạn chế và khả năng phát triển](#47-phân-tích-ưu-điểm-hạn-chế-và-khả-năng-phát-triển)
- [KẾT LUẬN](#kết-luận)
- [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)

---

<a id="chương-1"></a>
# CHƯƠNG 1. TỔNG QUAN VỀ HONEYPOT VÀ BÀI TOÁN PHÁT HIỆN, PHÂN TÍCH TẤN CÔNG MẠNG

---

## 1.1. Bối cảnh và thực trạng an toàn, an ninh mạng

### 1.1.1. Xu hướng gia tăng các cuộc tấn công mạng
Trong kỷ nguyên **chuyển đổi số** *(Digital Transformation — quá trình ứng dụng toàn diện công nghệ thông tin vào mọi lĩnh vực kinh tế, xã hội và quản lý nhà nước)*, không gian mạng đã trở thành huyết mạch kết nối toàn cầu. Tuy nhiên, song hành cùng sự tiện ích là sự bùng nổ của các hiểm họa an ninh mạng với mức độ tinh vi và quy mô chưa từng có.

Theo thống kê của **Cục An toàn thông tin — Bộ Thông tin và Truyền thông**, hàng nghìn sự cố an ninh mạng được ghi nhận mỗi năm tại Việt Nam, tập trung vào các hạ tầng quan trọng như dịch vụ công trực tuyến, ngân hàng số và cổng thông tin doanh nghiệp. Trên phạm vi toàn cầu, báo cáo **IBM Cost of a Data Breach 2024** chỉ ra rằng thời gian trung bình để một tổ chức nhận diện được một vụ xâm nhập thành công lên đến **194 ngày** (gần 7 tháng). Khoảng thời gian tồn tại trong bóng tối này tạo cơ hội cho kẻ tấn công cài cắm **Backdoor** *(cửa hậu — phần mềm bí mật cho phép truy cập lại hệ thống mà không qua xác thực)*, thiết lập mạng lưới **Command & Control (C2)** *(máy chủ điều khiển từ xa)* và âm thầm leo thang đặc quyền.

### 1.1.2. Nguy cơ đối với hệ thống dịch vụ web
Các hệ thống dịch vụ web hiện đại phải đối mặt với hàng loạt rủi ro:
- **Tấn công khai thác lỗ hổng ứng dụng**: Tiêm mã độc vào các trường dữ liệu người dùng nhằm chiếm quyền truy cập trái phép cơ sở dữ liệu hoặc hệ điều hành máy chủ.
- **Tấn công từ chối dịch vụ (DoS/DDoS)**: Làm tê liệt hạ tầng dịch vụ bằng việc làm tràn ngập tài nguyên băng thông và xử lý.
- **Mạng lưới thiết bị ma (Botnet)**: Điển hình như biến thể mã độc **Mirai** *(mã độc chuyên quét và lây nhiễm tự động qua các thiết bị IoT dùng thông tin đăng nhập mặc định)* liên tục quét tìm các cổng dịch vụ yếu.

### 1.1.3. Yêu cầu phát hiện và phân tích tấn công
Thực trạng trên đòi hỏi các tổ chức không chỉ dừng lại ở việc ngăn chặn thụ động, mà cần phải:
- **Phát hiện theo thời gian thực (Real-time Detection)**: Rút ngắn thời gian từ vài tháng xuống dưới mức mili-giây.
- **Thu thập thông tin tình báo mối đe dọa (Threat Intelligence)**: Thu thập toàn bộ **Payload** *(dữ liệu tấn công)*, địa chỉ IP nguồn, công cụ và kỹ thuật tấn công mà tin tặc đang sử dụng.
- **Chuẩn hóa dữ liệu theo khung quốc tế**: Ánh xạ hành vi tấn công sang khung **MITRE ATT&CK** *(khung phân loại chiến thuật và kỹ thuật tấn công thực tế)* nhằm phục vụ công tác điều tra số *(Digital Forensics)*.

---

## 1.2. Tổng quan về các giải pháp phòng thủ mạng

### 1.2.1. Tường lửa (Firewall)
**Tường lửa** *(Firewall — thiết bị hoặc phần mềm kiểm soát luồng lưu lượng mạng vào/ra dựa trên các tập luật định sẵn)* đóng vai trò là chốt chặn đầu tiên. Tường lửa mạng hoạt động ở tầng mạng/giao vận (IP/Port), trong khi **WAF** *(Web Application Firewall — tường lửa ứng dụng web)* hoạt động ở tầng ứng dụng (HTTP/HTTPS) để kiểm tra các mẫu độc hại như SQLi hoặc XSS.

### 1.2.2. Hệ thống IDS/IPS
- **IDS** *(Intrusion Detection System — Hệ thống phát hiện xâm nhập)*: Giám sát lưu lượng mạng, so khớp với cơ sở dữ liệu mẫu độc hại để đưa ra cảnh báo.
- **IPS** *(Intrusion Prevention System — Hệ thống ngăn chặn xâm nhập)*: Tự động chặn lưu lượng mạng khi phát hiện dấu hiệu xâm phạm.
- Các hệ thống phổ biến: **Suricata** *(hệ thống IDS/IPS đa luồng tốc độ cao)* và **Snort**.

### 1.2.3. SIEM và SOC
- **SIEM** *(Security Information and Event Management — Hệ thống quản lý thông tin và sự kiện an ninh mạng)*: Nền tảng gom log tập trung từ nhiều nguồn (Server, Firewall, IDS, Ứng dụng), chuẩn hóa và thực hiện **Correlation Rules** *(luật tương quan sự kiện — liên kết nhiều sự kiện đơn lẻ thành chuỗi tấn công)*.
- **SOC** *(Security Operations Center — Trung tâm điều hành an ninh mạng)*: Đơn vị vận hành gồm các chuyên viên giám sát, phân tích và phản ứng sự cố thông qua các bảng điều khiển trực quan *(Dashboard)*.

### 1.2.4. Hạn chế của các phương pháp phòng thủ truyền thống
Mặc dù rất quan trọng, các giải pháp truyền thống bộc lộ những điểm yếu chí tử:
1. **Phụ thuộc chữ ký (Signature-based)**: Hoàn toàn mù trước các cuộc tấn công **Zero-day** *(lỗ hổng chưa được công bố và chưa có chữ ký nhận dạng)*.
2. **Không phát hiện được kỹ thuật Living-off-the-Land**: Kẻ tấn công sử dụng các công cụ hợp lệ của hệ điều hành (PowerShell, WMI, curl) khiến Antivirus truyền thống không ghi nhận file mã độc.
3. **Hiện tượng mệt mỏi cảnh báo (Alert Fatigue)**: Tỷ lệ cảnh báo sai *(False Positive)* cao khiến chuyên viên SOC quá tải và dễ bỏ sót các đợt tấn công thực sự nguy hiểm.
4. **Không thu thập được động cơ và hành vi sâu của tin tặc**: Khi Firewall chặn gói tin, tổ chức chỉ biết có một kết nối bị hủy mà không nắm được kẻ tấn công định làm gì tiếp theo.

---

## 1.3. Tổng quan về Honeypot

### 1.3.1. Khái niệm Honeypot
**Honeypot** *(Bẫy mạng / Hệ thống mồi nhử)* là một tài nguyên an ninh thông tin được thiết lập có chủ đích để bị thăm dò, tấn công hoặc xâm phạm. Điểm cốt lõi của Honeypot là: **bản thân nó không chứa dữ liệu nghiệp vụ thật và không có lưu lượng sử dụng hợp pháp**. Do đó, bất kỳ tương tác nào hướng tới Honeypot mặc định đều là hành vi đáng ngờ hoặc tấn công.

### 1.3.2. Nguyên lý hoạt động
Honeypot mở các cổng dịch vụ giả lập (HTTP, SSH, FTP, Telnet, Database) để mời gọi kẻ tấn công. Khi tin tặc tương tác, Honeypot phản hồi như một dịch vụ thật nhưng đồng thời âm thầm ghi lại toàn bộ thao tác, phím gõ, câu lệnh, mã khai thác và công cụ của tin tặc vào nhật ký an ninh mà không để tin tặc biết mình đang nằm trong bẫy.

```text
[Kẻ tấn công / Scanner] ────► [Cổng Honeypot Giả Lập] ────► [Phản hồi kết quả giả tạo]
                                         │
                                         ▼ (Âm thầm ghi nhận)
                            [Hệ thống Log & Phân tích AI]
```

### 1.3.3. Vai trò của Honeypot trong phát hiện và phân tích tấn công
- **Cảnh báo sớm (Early Warning)**: Báo động tức thì khi có hoạt động do thám mạng nội bộ.
- **Tỷ lệ báo sai cực thấp (Near-Zero False Positive)**: Vì không có người dùng hợp lệ, mọi cảnh báo từ Honeypot đều có độ tin cậy rất cao.
- **Nguồn Threat Intelligence quý giá**: Thu thập mã độc mới, payload mới và kỹ thuật khai thác zero-day phục vụ nghiên cứu và cập nhật cho hệ thống phòng thủ chính.

---

## 1.4. Phân loại Honeypot

### 1.4.1. Phân loại theo mức độ tương tác
Mức độ tương tác *(Interaction Level)* phản ánh quyền hạn và mức độ tự do mà Honeypot cung cấp cho kẻ tấn công:

### 1.4.2. Low-Interaction Honeypot
- **Đặc điểm**: Giả lập dịch vụ ở mức tối thiểu (ví dụ chỉ bắt tay TCP, trả về biểu ngữ chào mừng banner giả).
- **Ưu điểm**: Nhẹ, tốn ít tài nguyên, rủi ro bị chiếm quyền điều khiển bằng 0.
- **Nhược điểm**: Lượng thông tin thu thập nghèo nàn, dễ bị tin tặc nhận diện là bẫy *(Fingerprinting)*.

### 1.4.3. Medium-Interaction Honeypot
- **Đặc điểm**: Giả lập một phần giao thức và phản hồi ứng dụng (ví dụ giả lập form đăng nhập Web, trả về lỗi SQL giả, giả lập các lệnh shell cơ bản).
- **Ưu điểm**: Thu thập được payload tấn công đầy đủ mà vẫn đảm bảo an toàn tuyệt đối cho hệ thống máy chủ thật.
- **Ví dụ**: Web Honeypot được phát triển trong đồ án này.

### 1.4.4. High-Interaction Honeypot
- **Đặc điểm**: Cung cấp một hệ điều hành hoặc dịch vụ thật hoàn chỉnh (thường chạy trong máy ảo hoặc sandbox cô lập). Tin tặc có thể đăng nhập root, tải file và thực thi lệnh thật.
- **Ưu điểm**: Thu thập hành vi chân thực nhất của tin tặc.
- **Nhược điểm**: Tiêu tốn tài nguyên và tiềm ẩn rủi ro cao nếu không có cơ chế cách ly mạng tốt, có thể bị tin tặc dùng làm bàn đạp tấn công hệ thống khác.
- **Ví dụ**: **Cowrie** *(Honeypot SSH tương tác cao mô phỏng hệ điều hành Debian)*.

### 1.4.5. Phân loại theo mục đích triển khai
Tùy vào mục tiêu ứng dụng, Honeypot được chia thành hai nhóm mục đích chính:

### 1.4.6. Production Honeypot và Research Honeypot
- **Production Honeypot** *(Honeypot bảo vệ sản xuất)*: Được đặt bên trong mạng nội bộ của tổ chức nhằm phát hiện xâm nhập sớm, đánh lạc hướng tin tặc và bảo vệ các máy chủ thật.
- **Research Honeypot** *(Honeypot nghiên cứu)*: Thường được triển khai ra môi trường công khai để thu thập thông tin về các biến thể mã độc mới, xu hướng tấn công của các nhóm tin tặc (APT) trên thế giới.

---

## 1.5. Web Honeypot và các kỹ thuật tấn công ứng dụng web

### 1.5.1. Đặc điểm và nguyên lý hoạt động của Web Honeypot
**Web Honeypot** là dạng bẫy chuyên biệt giả lập một trang web hoặc cổng dịch vụ công với đầy đủ giao diện HTML, CSS, JavaScript và các biểu mẫu nhập liệu. Điểm mấu chốt của Web Honeypot là **Cơ chế cô lập an toàn (Containment)**: Khi tin tặc gửi mã độc khai thác lỗ hổng, hệ thống trả về phản hồi giả lập chân thực (để đánh lừa tin tặc tiếp tục tấn công) nhưng **tuyệt đối không thực thi câu lệnh thật và không truy cập cơ sở dữ liệu thật**.

### 1.5.2. SQL Injection
- **Mã OWASP WSTG**: `WSTG-INPV-05`
- **Mô tả**: Kẻ tấn công tiêm các ký tự đặc biệt (`' OR 1=1 --`, `UNION SELECT`) vào tham số HTTP để đánh cắp hoặc phá hủy dữ liệu.
- **Cơ chế bẫy**: Web Honeypot giả lập trả về bảng dữ liệu người dùng giả khi phát hiện cú pháp SQL độc hại.

### 1.5.3. Cross-Site Scripting (XSS)
- **Mã OWASP WSTG**: `WSTG-INPV-01` (Reflected) và `WSTG-INPV-02` (Stored)
- **Mô tả**: Kẻ tấn công chèn mã JavaScript độc hại (`<script>alert(1)</script>`, `onerror=alert(1)`) nhằm chiếm đoạt phiên làm việc của người dùng.
- **Cơ chế bẫy**: Honeypot ghi nhận toàn bộ payload XSS và mã hóa ký tự đầu ra an toàn để vô hiệu hóa mã độc.

### 1.5.4. File Inclusion và Path Traversal
- **Mã OWASP WSTG**: `WSTG-ATHZ-01` (Path Traversal), `WSTG-INPV-11` (RFI/LFI)
- **Mô tả**: Kẻ tấn công sử dụng các chuỗi duyệt thư mục (`../../../../etc/passwd`) hoặc nhúng file từ xa (`http://evil.com/shell.txt`) để đọc file nhạy cảm trên máy chủ.
- **Cơ chế bẫy**: Honeypot trả về nội dung file `/etc/passwd` giả lập được chuẩn bị sẵn.

### 1.5.5. Brute Force và Credential Attacks
- **Mã OWASP WSTG**: `WSTG-ATHN-03`
- **Mô tả**: Sử dụng danh sách từ điển và công cụ tự động (Hydra, Burp Intruder) để thử hàng loạt tổ hợp tài khoản/mật khẩu trên form đăng nhập hoặc SSH.
- **Cơ chế bẫy**: Ghi nhận toàn bộ cặp tài khoản và mã băm mật khẩu *(Password Fingerprint)* để nhận diện danh sách từ điển của tin tặc.

### 1.5.6. Command Injection
- **Mã OWASP WSTG**: `WSTG-INPV-12`
- **Mô tả**: Chèn các toán tử nối lệnh của hệ điều hành (`;`, `|`, `&&`, `whoami`, `cat /etc/shadow`) vào trường nhập liệu.
- **Cơ chế bẫy**: Trả về kết quả đầu ra giả lập mô phỏng hệ điều hành Linux mà không bao giờ gọi hàm `system()` hay `subprocess()` thật.

### 1.5.7. XML External Entity (XXE)
- **Mã OWASP WSTG**: `WSTG-INPV-07`
- **Mô tả**: Lợi dụng trình phân tích cú pháp XML để đọc tài nguyên nội bộ hoặc kích hoạt **SSRF** *(Server-Side Request Forgery — giả mạo yêu cầu từ phía máy chủ)* thông qua khai báo `<!ENTITY>`.

---

## 1.6. Các nghiên cứu và giải pháp liên quan

### 1.6.1. Các hệ thống Honeypot tiêu biểu
- **Honeyd**: Một trong những hệ thống Honeypot tương tác thấp đầu tiên trên thế giới, có khả năng giả lập hàng nghìn địa chỉ IP và hệ điều hành khác nhau ở tầng giao vận TCP/IP.
- **Cowrie**: Hệ thống SSH/Telnet Honeypot tương tác cao phổ biến nhất hiện nay, chuyên ghi nhận các đợt tấn công dò quét mật khẩu và lệnh shell của botnet.
- **OpenCanary**: Honeypot mã nguồn mở theo dạng module đa dịch vụ (FTP, HTTP, RDP, MySQL) phù hợp cho việc đặt bẫy trong mạng nội bộ doanh nghiệp.

### 1.6.2. Các giải pháp Web Honeypot hiện có
- **Glastopf / SNARE & TANNER**: Các giải pháp Web Honeypot mã nguồn mở mô phỏng các lỗ hổng PHP phổ biến. Tuy nhiên, các dự án này gặp hạn chế về việc giao diện người dùng thiếu chân thực, không tích hợp dashboard hiện đại và thiếu cơ chế phân loại lưu lượng mạng đa tầng.

### 1.6.3. Ứng dụng học máy trong phát hiện và phân loại tấn công
Nhiều nghiên cứu quốc tế đã áp dụng các thuật toán **Học máy (Machine Learning)** như Random Forest, Support Vector Machine (SVM), Neural Networks và **XGBoost** *(eXtreme Gradient Boosting — thuật toán cây quyết định tăng cường độ chính xác cao)* trên các bộ dữ liệu lưu lượng mạng như KDD99, NSL-KDD, UNSW-NB15 và gần đây nhất là **CICIoT2023**. Các nghiên cứu chỉ ra rằng XGBoost vượt trội về tốc độ suy luận *(Inference Speed)* và độ chính xác phân loại trên dữ liệu dạng bảng *(Tabular Data)*.

---

## 1.7. Khoảng trống nghiên cứu và định hướng đề tài

### 1.7.1. Hạn chế của các hệ thống hiện nay
1. **Thiếu sự tích hợp liên hoàn**: Phần lớn các hệ thống chỉ dừng lại ở mức thu thập log đơn lẻ (hoặc chỉ Web, hoặc chỉ SSH, hoặc chỉ IDS) mà không có trung tâm điều phối tập trung.
2. **Thiếu khả năng suy luận AI thời gian thực trên dữ liệu mạng sống**: Đa số mô hình AI chỉ được thử nghiệm trong môi trường giả lập tĩnh trên file CSV, thiếu đường ống kết nối trực tiếp với cảm biến bắt gói tin mạng.
3. **Nguy cơ mất an toàn cho bẫy**: Thiếu kiến trúc phân vùng cô lập **Anti-Pivot** *(ngăn chặn tin tặc dùng bẫy làm bàn đạp tấn công hệ thống thật)*.

### 1.7.2. Bài toán nghiên cứu đặt ra
Xây dựng một hệ thống an ninh mạng chủ động hoàn chỉnh, có khả năng:
- Đặt bẫy mồi nhử thuyết phục đa tầng (Web và SSH).
- Bắt gói tin mạng và trích xuất 46 đặc trưng luồng *(Network Flow)* theo thời gian thực.
- Phân loại tấn công bằng mô hình AI XGBoost 7 lớp nhãn với độ trễ dưới 5ms.
- Chuẩn hóa dữ liệu log theo chuẩn quốc tế **ECS (Elastic Common Schema)**, tương quan sự kiện SIEM và hiển thị trực quan trên Dashboard SOC.
- Đảm bảo an toàn tuyệt đối cho hệ thống máy chủ thật thông qua kiến trúc phân vùng 4 tầng nghiêm ngặt.

### 1.7.3. Mục tiêu và phạm vi nghiên cứu
- **Mục tiêu**: Thiết kế, lập trình và kiểm thử toàn diện hệ thống Web Honeypot thời gian thực tích hợp AI/ML và SOC Dashboard.
- **Phạm vi**: Triển khai hệ thống phân tích gồm 9 module độc lập, kiểm thử với 10 kịch bản tấn công web chuẩn OWASP và đánh giá trên bộ dữ liệu mạng CICIoT2023 với gần 10 triệu mẫu kiểm thử.

---

<a id="chương-2"></a>
# CHƯƠNG 2. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG WEB HONEYPOT

---

## 2.1. Phân tích yêu cầu hệ thống

### 2.1.1. Yêu cầu chức năng
1. **Khả năng mồi nhử thuyết phục**: Cung cấp giao diện web dịch vụ công giả lập hoàn chỉnh, phản hồi HTTP đúng chuẩn nghiệp vụ.
2. **Ghi nhận toàn diện (Comprehensive Capture)**: Ghi lại đầy đủ HTTP Request (Header, Query Params, Form Body, JSON Payload), địa chỉ IP nguồn, User-Agent và timestamp.
3. **Phân loại AI thời gian thực**: Trích xuất đặc trưng luồng gói tin mạng và đưa ra kết quả phân loại trong vòng dưới 100ms.
4. **Khử trùng lặp nhật ký (Deduplication)**: Loại bỏ các bản ghi trùng lặp từ cùng một nguồn tấn công lặp lại trong khoảng thời gian ngắn.
5. **Trực quan hóa và Cảnh báo SOC**: Hiển thị biểu đồ phân bố tấn công, timeline sự kiện, bản đồ nguồn tấn công và hỗ trợ truy vấn chi tiết từng sự kiện.

### 2.1.2. Yêu cầu phi chức năng
- **Độ chính xác mô hình AI**: Accuracy $\ge 99\%$ trên tập dữ liệu kiểm thử.
- **Độ trễ suy luận AI (Inference Latency)**: $< 10\text{ms}$ cho mỗi luồng mạng.
- **Thông lượng xử lý (Throughput)**: Chịu tải $\ge 1.000$ sự kiện/giây.
- **Tính sẵn sàng và tự động hóa**: Khởi chạy toàn bộ cụm dịch vụ chỉ với một lệnh duy nhất.

### 2.1.3. Yêu cầu bảo mật và cô lập hệ thống
- **Nguyên tắc Containment**: Không cho phép bất kỳ lệnh hệ thống thật nào được thực thi trong container bẫy.
- **Nguyên tắc Anti-Pivot**: Container Honeypot tuyệt đối không có đường kết nối mạng trực tiếp đến vùng dữ liệu (Data Zone) hay vùng quản trị (Control Zone).
- **Không sử dụng mật khẩu mã hóa cứng (No Hardcoded Secrets)**: Toàn bộ API Key, Database Password và JWT Secret phải được sinh ngẫu nhiên tự động khi triển khai.

---

## 2.2. Mô hình mối đe dọa

### 2.2.1. Tài sản cần bảo vệ
1. **Cơ sở dữ liệu sự kiện (PostgreSQL & Elasticsearch)**: Bằng chứng điều tra số, phải bảo toàn tính toàn vẹn.
2. **API Keys & Token xác thực**: Khóa xác thực Ingest và khóa phân tích Analyst.
3. **Dashboard quản trị & Hạ tầng máy chủ vật lý**: Ngăn chặn kẻ tấn công truy cập trái phép và thoát khỏi container *(Container Escape)*.

### 2.2.2. Tác nhân và phương thức tấn công
- **Botnet và Script tự động**: Quét cổng diện rộng, dò quét mật khẩu mặc định (Mirai, Hydra, Nmap).
- **Tin tặc ứng dụng web**: Sử dụng các công cụ như `sqlmap`, `Nikto`, `Burp Suite` để khai thác lỗ hổng nghiệp vụ.
- **Kẻ tấn công có chủ đích (APT)**: Cố gắng leo thang đặc quyền và tìm cách di chuyển ngang *(Lateral Movement)* vào mạng nội bộ.

### 2.2.3. Phân tích đe dọa theo mô hình STRIDE
Hệ thống áp dụng mô hình **STRIDE** *(mô hình phân loại đe dọa an toàn thông tin của Microsoft)*:

| Đe dọa (STRIDE) | Rủi ro cụ thể | Biện pháp kiểm soát trong thiết kế |
|---|---|---|
| **Spoofing** (Giả mạo) | Kẻ tấn công giả mạo nguồn gửi log để làm sai lệch dữ liệu | Xác thực Ingestion API bằng API Key nội bộ và Token OIDC |
| **Tampering** (Can thiệp dữ liệu) | Sửa đổi dữ liệu log trên đường truyền | Phân vùng mạng Docker cô lập, tính mã băm SHA-256 cho mỗi event |
| **Repudiation** (Chối bỏ) | Tin tặc hoặc quản trị viên chối bỏ hành động | Ghi log kiểm toán *(Audit Log)* JSON không thể sửa đổi |
| **Information Disclosure** (Lộ lọt thông tin) | Lộ dữ liệu cấu hình hoặc mật khẩu quản trị | Secret sinh ngẫu nhiên, không mount volume nhạy cảm vào container Lure |
| **Denial of Service** (Từ chối dịch vụ) | Làm tràn ngập Honeypot và Backend bằng lưu lượng rác | Cấu hình Rate Limiting trên Nginx Edge và khử trùng lặp bằng Redis |
| **Elevation of Privilege** (Leo thang đặc quyền) | Chiếm quyền root trên máy chủ thông qua bẫy | Chạy container dưới quyền non-root, read-only root filesystem, cô lập mạng |

---

## 2.3. Kiến trúc tổng thể hệ thống

### 2.3.1. Kiến trúc phân tầng
Hệ thống được thiết kế theo kiến trúc 4 tầng phân lập rõ ràng:
1. **Tầng Mồi nhử (Lure Plane)**: Tiếp xúc trực tiếp với lưu lượng bên ngoài, bao gồm Nginx Edge WAF, Flask Web Honeypot và Cowrie SSH Honeypot.
2. **Tầng Cảm biến mạng (Sensor Network)**: Suricata IDS và cầu nối IDS/ML Bridge kết nối trực tiếp với card mạng vật lý.
3. **Tầng Xử lý & Dữ liệu (Data Plane)**: FastAPI Ingestion Backend, bộ đệm Redis và cơ sở dữ liệu PostgreSQL.
4. **Tầng Quản trị & Điều phối (Control Plane)**: React SOC Dashboard, Keycloak IAM, Kibana SIEM, Grafana và Prometheus.

```text
[Kẻ tấn công / Client]
       │
       ├─► (Port 8080 - HTTP) ──► Edge WAF (ModSecurity) ──► Flask Web Honeypot (Part 02)
       │                                                            │ (Log JSON)
       │                                                            ▼
       ├─► (Port 2222 - SSH)  ──► SSH Proxy (HAProxy) ─────► Cowrie SSH Honeypot
       │                                                            │ (Log JSON)
       │                                                            ▼
       └─► (NIC Lab - Gói tin) ──► Suricata IDS (Part 05) ──► IDS/ML Bridge (XGBoost)
                                                                    │
       ┌────────────────────────────────────────────────────────────┘
       │ (HTTP POST Event)
       ▼
[FastAPI Backend - Part 03] ──► PostgreSQL (Lưu trữ) & Redis (Bộ đệm khử trùng lặp)
       │
       ├─► [React Dashboard - Part 04] (Xác thực qua Keycloak OIDC/PKCE)
       ├─► [Prometheus & Grafana] (Giám sát hiệu năng hệ thống)
       └─► [Filebeat ──► Elasticsearch & Kibana - Part 06] (SIEM & Tương quan sự kiện)
```

### 2.3.2. Phân vùng mạng và cơ chế ngăn chặn lan truyền
Hệ thống thiết lập 4 mạng Docker nội bộ độc lập:
- `public`: Chỉ cho phép lưu lượng từ bên ngoài đi vào cổng 8080 của Nginx Edge.
- `lure`: Nơi chứa Web Honeypot, hoàn toàn không có đường ra internet và chỉ được phép gửi dữ liệu một chiều tới FastAPI Ingest Endpoint.
- `control`: Dành riêng cho giao diện quản trị Dashboard, Keycloak và Analyst API, chỉ bind trên địa chỉ cục bộ `127.0.0.1`.
- `data`: Mạng tối mật chứa PostgreSQL, Elasticsearch và Redis, tuyệt đối không publish bất kỳ port nào ra ngoài.

### 2.3.3. Luồng dữ liệu trong hệ thống
Mọi sự kiện tấn công đi qua 5 giai đoạn:
1. **Tiếp nhận**: Kẻ tấn công gửi payload vào cổng 8080/2222.
2. **Ghi nhận & Cô lập**: Honeypot phân tích payload, tạo bản ghi JSON và trả về kết quả giả tạo.
3. **Chuyển tiếp & Khử trùng lặp**: Forwarder đẩy log về FastAPI, Redis kiểm tra mã băm SHA-256 để chống trùng lặp.
4. **Lưu trữ & Ánh xạ**: Lưu vào PostgreSQL và tự động gán nhãn kỹ thuật MITRE ATT&CK.
5. **Trực quan hóa & Cảnh báo**: Filebeat đồng bộ dữ liệu vào Elasticsearch, kích hoạt luật tương quan SIEM và hiển thị trên SOC Dashboard.

---

## 2.4. Thiết kế Web Honeypot

### 2.4.1. Thiết kế giao diện mồi nhử
Giao diện được thiết kế bằng **Bootstrap** mô phỏng giao diện của một "Cổng thông tin và Dịch vụ hành chính công", bao gồm:
- Trang chủ giới thiệu dịch vụ và tin tức thông báo.
- Trang tra cứu hồ sơ hành chính trực tuyến.
- Form đăng nhập quản trị viên và cán bộ tiếp nhận hồ sơ.
- Form gửi phản ánh kiến nghị kèm chức năng đính kèm tệp tin.

### 2.4.2. Thiết kế API giả lập
Các điểm cuối API giả lập được thiết kế để phản hồi đúng định dạng JSON/HTML mà kẻ tấn công mong đợi:
- `/api/v1/lookup`: Tiếp nhận truy vấn mã hồ sơ (điểm đặt bẫy SQLi).
- `/api/v1/auth/login`: Tiếp nhận thông tin đăng nhập (điểm đặt bẫy Brute Force).
- `/api/v1/documents/view`: Tiếp nhận tham số đường dẫn file (điểm đặt bẫy Path Traversal và LFI/RFI).
- `/api/v1/tools/ping`: Công cụ kiểm tra kết nối mạng (điểm đặt bẫy Command Injection).

### 2.4.3. Thiết kế các điểm tương tác và bề mặt tấn công
Hệ thống thiết kế sẵn **10 bề mặt tấn công** chuẩn OWASP WSTG:
1. `SQL Injection` trên ô tìm kiếm hồ sơ và tham số URL `?id=`.
2. `Reflected XSS` trên thông báo kết quả tìm kiếm.
3. `Stored XSS` trong mục gửi ý kiến phản ánh của công dân.
4. `Path Traversal` trên chức năng đọc tài liệu hướng dẫn `?doc=`.
5. `IDOR` *(Insecure Direct Object References — Tham chiếu trực tiếp đối tượng không an toàn)* trên tham số xem hồ sơ người dùng `?user_id=`.
6. `Remote File Inclusion (RFI)` trên chức năng nạp mẫu đơn từ xa.
7. `Unrestricted File Upload` trên chức năng tải lên file hồ sơ đính kèm.
8. `Command Injection` trên chức năng kiểm tra trạng thái máy chủ mạng nội bộ.
9. `XXE` trên bộ xử lý dữ liệu hồ sơ định dạng XML.
10. `Brute Force Login` trên giao diện đăng nhập hệ thống.

### 2.4.4. Thiết kế cơ chế ghi nhận và chuyển tiếp sự kiện
- Hàm `record_attack()` ghi nhận sự kiện ngay lập tức vào cơ sở dữ liệu SQLite cục bộ trong container bẫy.
- Tiến trình `part2-forwarder` chạy độc lập, liên tục đọc hàng đợi sự kiện từ SQLite và thực hiện HTTP POST chuyển tiếp về trung tâm tiếp nhận Part 03 kèm API Key bảo mật.

---

## 2.5. Thiết kế cơ chế phát hiện và phân tích tấn công

### 2.5.1. Phát hiện tấn công dựa trên luật
Module `detectors.py` trong Web Honeypot sử dụng tập luật Regex *(Regular Expressions — biểu thức chính quy)* tối ưu hóa để nhận dạng nhanh các dấu hiệu tấn công đặc trưng:
- Cú pháp SQL Injection: `' OR '1'='1`, `UNION SELECT`, `DROP TABLE`, `INFORMATION_SCHEMA`.
- Cú pháp XSS: `<script>`, `javascript:`, `onerror=`, `onload=`, `<svg/onload=`.
- Cú pháp Path Traversal: `../`, `..\`, `%2e%2e%2f`, `/etc/passwd`, `win.ini`.
- Cú pháp Command Injection: `;`, `|`, `&&`, `whoami`, `cat`, `curl`, `wget`.

### 2.5.2. Phát hiện và phân loại lưu lượng bằng học máy
Để khắc phục điểm yếu của luật tĩnh, hệ thống thiết kế mô hình Học máy **XGBoost** phân loại lưu lượng mạng thành **7 lớp nhãn**:
1. `Benign`: Lưu lượng truy cập bình thường.
2. `DDoS`: Tấn công từ chối dịch vụ phân tán.
3. `DoS`: Tấn công từ chối dịch vụ đơn nguồn.
4. `BruteForce`: Tấn công vét cạn mật khẩu SSH/HTTP.
5. `Recon`: Hoạt động do thám, quét cổng mạng.
6. `Spoofing`: Tấn công giả mạo địa chỉ IP, ARP Poisoning.
7. `Mirai`: Lưu lượng mã độc botnet IoT.

### 2.5.3. Trích xuất đặc trưng luồng mạng
Module `FlowAccumulator` thiết kế thuật toán trích xuất **46 đặc trưng thống kê của luồng gói tin mạng** theo chuẩn của bộ dữ liệu CICIoT2023, bao gồm:
- Thống kê độ dài gói tin: `Header_Length`, `Min`, `Max`, `Mean`, `Std` của gói tin chiều đi và về.
- Thống kê thời gian: Thời lượng luồng, khoảng thời gian giữa các gói tin liên tiếp *(IAT — Inter-Arrival Time)*.
- Thống kê cờ TCP: Tần suất xuất hiện các cờ `SYN`, `FIN`, `RST`, `ACK`, `PSH`, `URG`.
- Tỷ lệ tốc độ truyền tải: `Rate` (gói tin/giây), `Byte_Rate` (byte/giây).

### 2.5.4. Phân tích Payload và xác định kỹ thuật tấn công
Hệ thống thực hiện phân tích cấu trúc của Payload:
- Trích xuất thông tin dấu vết công cụ *(Tool Fingerprint)* qua header `User-Agent` (ví dụ nhận dạng `sqlmap`, `Nikto`, `Hydra`).
- Tính toán mã băm an toàn SHA-256 của chuỗi payload mật khẩu *(Password Fingerprinting)* để phân tích từ điển tấn công mà không lưu mật khẩu dạng rõ.

---

## 2.6. Thiết kế cơ chế thu thập và lưu trữ dữ liệu

### 2.6.1. Thu thập Request HTTP và dữ liệu lưu lượng mạng
- Tại tầng ứng dụng: Thu thập toàn bộ HTTP method, request path, request headers và body payload.
- Tại tầng mạng: Bắt gói tin trực tiếp từ card mạng thông qua **Suricata IDS** và xuất bản ghi luồng ra tệp `eve.json`.

### 2.6.2. Chuẩn hóa dữ liệu theo Elastic Common Schema (ECS)
Toàn bộ dữ liệu sự kiện được chuẩn hóa theo chuẩn quốc tế **ECS** *(Elastic Common Schema — lược đồ dữ liệu log chuẩn hóa)* giúp đồng nhất các trường dữ liệu:
- `@timestamp`: Thời gian xảy ra sự kiện theo chuẩn ISO-8601.
- `source.ip`, `source.port`: Địa chỉ IP và cổng nguồn của kẻ tấn công.
- `destination.ip`, `destination.port`: Địa chỉ IP và cổng đích của Honeypot.
- `http.request.method`, `http.request.body.content`: Phương thức và nội dung payload HTTP.
- `threat.technique.id`, `threat.technique.name`: Mã định danh kỹ thuật MITRE ATT&CK.

### 2.6.3. Khử trùng lặp dữ liệu bằng Redis
Để tránh tình trạng tràn bộ nhớ khi bị tấn công Brute Force hoặc DoS với hàng nghìn request giống hệt nhau, hệ thống thiết kế cơ chế **Deduplication**:
- Tính mã băm `SHA-256(source_ip + attack_type + payload)`.
- Ghi mã băm vào **Redis** với thời gian sống **TTL (Time To Live)** là 60 giây.
- Nếu mã băm đã tồn tại trong Redis, sự kiện được ghi nhận tăng bộ đếm tần suất mà không cần tạo thêm dòng mới trong PostgreSQL.

### 2.6.4. Thiết kế mô hình lưu trữ PostgreSQL và Elasticsearch
- **PostgreSQL**: Lưu trữ có cấu trúc các sự kiện tấn công phục vụ truy vấn nghiệp vụ của Dashboard và lưu trữ dữ liệu quan hệ của hệ thống.
- **Elasticsearch**: Lưu trữ phân tán toàn bộ tài liệu log chuẩn ECS phục vụ tìm kiếm toàn văn *(Full-text Search)* và chạy các luật tương quan thời gian thực.

---

## 2.7. Thiết kế cơ chế tương quan và cảnh báo

### 2.7.1. Phân tích theo địa chỉ IP nguồn và phiên tương tác
Nhóm các sự kiện đơn lẻ theo địa chỉ IP nguồn và Session Cookie để tái hiện toàn bộ hành trình tương tác của một cá nhân tin tặc.

### 2.7.2. Phân tích chuỗi tấn công đa tầng
Thiết kế **4 luật tương quan sự kiện (Correlation Rules)** trong SIEM:
1. **Port Scan Storm**: Phát hiện cùng 1 IP kết nối tới $\ge 20$ cổng đích khác nhau trong vòng 60 giây.
2. **Brute Force Campaign**: Phát hiện cùng 1 IP thất bại đăng nhập $\ge 50$ lần trong vòng 5 phút.
3. **Multi-vector Attack**: Phát hiện cùng 1 IP tấn công kết hợp $\ge 2$ dịch vụ khác nhau (ví dụ vừa quét SSH vừa tiêm mã SQLi Web) trong vòng 10 phút.
4. **High-risk AI Alert Cluster**: Phát hiện mô hình XGBoost đưa ra $\ge 10$ cảnh báo mức rủi ro cao từ cùng một dải mạng subnet trong vòng 2 phút.

### 2.7.3. Ánh xạ kỹ thuật tấn công theo MITRE ATT&CK
Tự động gán nhãn chiến thuật *(Tactic)* và kỹ thuật *(Technique)*:
- SQL Injection $\rightarrow$ `T1190 — Exploit Public-Facing Application`
- Brute Force Login $\rightarrow$ `T1110 — Brute Force`
- Reconnaissance / Port Scan $\rightarrow$ `T1046 — Network Service Discovery`
- Command Injection $\rightarrow$ `T1059 — Command and Scripting Interpreter`

---

## 2.8. Thiết kế Dashboard giám sát SOC

### 2.8.1. Thiết kế bảng điều khiển tổng quan và thời gian thực
- **Thẻ chỉ số chính (KPI Cards)**: Tổng số cuộc tấn công, số IP độc hại duy nhất, số cảnh báo mức cao và trạng thái hoạt động của các module.
- **Biểu đồ thời gian thực**: Biểu đồ phân bố loại tấn công theo thời gian thực (Line Chart), biểu đồ tròn tỷ lệ các kỹ thuật tấn công (Pie Chart).

### 2.8.2. Thiết kế giao diện truy vấn và điều tra sự kiện
- Bảng danh sách sự kiện chi tiết hỗ trợ lọc theo khoảng thời gian, IP nguồn, loại tấn công và mã kỹ thuật MITRE ATT&CK.
- Hộp thoại **Modal Drill-down** cho phép chuyên viên SOC xem chi tiết từng dòng HTTP Request, Header và toàn bộ Payload độc hại.
- Chức năng xuất dữ liệu báo cáo sự cố dưới định dạng tệp CSV.

### 2.8.3. Thiết kế cơ chế xác thực và phân quyền
Tích hợp hệ thống quản lý danh tính **Keycloak** áp dụng cơ chế **RBAC (Role-Based Access Control)** với luồng bảo mật **OAuth2 PKCE (Proof Key for Code Exchange)** chia làm 3 vai trò:
- `admin`: Toàn quyền quản trị hệ thống, cấu hình bẫy và quản lý người dùng.
- `soc-analyst`: Xem dữ liệu, phân tích sự kiện, truy vấn log và xuất báo cáo.
- `viewer`: Chỉ xem các biểu đồ thống kê tổng quan.

---

<a id="chương-3"></a>
# CHƯƠNG 3. XÂY DỰNG VÀ TRIỂN KHAI HỆ THỐNG WEB HONEYPOT

---

## 3.1. Môi trường và công nghệ triển khai

### 3.1.1. Môi trường phần cứng và hạ tầng mạng Lab
- **Máy chủ thử nghiệm**: CPU 8 nhân (Intel Core i7/AMD Ryzen 7), RAM 16 GB DDR4, Ổ cứng SSD NVMe 100 GB.
- **Hạ tầng mạng Lab**: 01 Card mạng vật lý (NIC) kết nối vào dải mạng thử nghiệm `192.168.1.0/24`, cấu hình phân tách luồng quản trị và luồng mồi nhử.

### 3.1.2. Môi trường phần mềm và công nghệ sử dụng
- **Hệ điều hành**: Windows 11 Pro / Ubuntu Server 22.04 LTS.
- **Nền tảng chạy container**: Docker Engine 24.0+ & Docker Compose v2.
- **Ngôn ngữ lập trình**: Python 3.11 (quản lý thư viện bằng công cụ siêu tốc `UV`), JavaScript/TypeScript (Node.js 18+).
- **Trình điều khiển bắt gói tin**: Npcap 1.7x (trên Windows) hoặc Libpcap (trên Linux).

### 3.1.3. Đóng gói và triển khai hệ thống bằng Docker Compose
Tệp [compose.yaml](file:///d:/A/A_5chai/honey_pot/part_08_DOCKER_DEPLOYMENT/compose.yaml) điều phối hơn 15 container dịch vụ hoạt động đồng bộ:

```yaml
services:
  # Vùng Lure Plane
  part2-web:
    image: honeypot-web:latest
    networks: [public, lure]
  haproxy-ssh:
    image: haproxy:2.8-alpine
    ports: ["2222:2222"]
    networks: [public, lure]
  cowrie:
    image: cowrie/cowrie:latest
    networks: [lure]

  # Vùng Data Plane
  part3-api:
    image: honeypot-api:latest
    networks: [lure, control, data]
  postgres:
    image: postgres:15-alpine
    networks: [data]
  redis:
    image: redis:7-alpine
    networks: [data]

  # Vùng Control Plane
  dashboard:
    image: honeypot-dashboard:latest
    networks: [control]
  keycloak:
    image: quay.io/keycloak/keycloak:22.0
    networks: [control]
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    networks: [data]
  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    networks: [control]
```

---

## 3.2. Xây dựng Web Honeypot

### 3.2.1. Xây dựng Website mồi nhử bằng Flask và Bootstrap
Ứng dụng Web Honeypot được lập trình bằng framework **Flask (Python)** với cấu trúc module chuyên biệt. Các trang giao diện HTML được thiết kế bằng **Bootstrap 5** mang giao diện hiện đại của Cổng Dịch vụ công.

### 3.2.2. Xây dựng các bề mặt tấn công mô phỏng
Các route Flask giả lập phản hồi các lỗ hổng bảo mật:

```python
# Giả lập điểm bẫy SQL Injection
@app.route('/services/search', methods=['GET', 'POST'])
def search_service():
    query = request.values.get('q', '')
    if query:
        # Kiểm tra dấu hiệu SQLi
        if is_sqli_attack(query):
            record_attack(request, "sql_injection", query)
            # Trả về kết quả rò rỉ dữ liệu giả để đánh lừa kẻ tấn công
            fake_users = [
                {"id": 1, "username": "admin", "role": "SuperAdministrator"},
                {"id": 2, "username": "canbo_tiepnhan", "role": "Officer"}
            ]
            return render_template('search_results.html', results=fake_users, payload_triggered=True)
    return render_template('search.html')
```

### 3.2.3. Hiện thực cơ chế cô lập và bảo vệ dữ liệu thực
Mọi hàm xử lý trong `part_02_WEB_HONEYPOT` đều tuân thủ nguyên tắc không tương tác với tài nguyên hệ thống thật:
- File tải lên độc hại được chuyển hướng vào thư mục `/quarantine/` và tước bỏ quyền thực thi (`chmod 000`).
- Lệnh shell tiêm qua Command Injection chỉ đi qua bộ sinh chuỗi văn bản giả lập kết quả `Linux kernel 5.15.0-generic` mà không gọi `os.system()`.

---

## 3.3. Xây dựng hệ thống tiếp nhận và lưu trữ nhật ký

### 3.3.1. Xây dựng Backend API tiếp nhận dữ liệu bằng FastAPI
Backend được xây dựng bằng **FastAPI** hỗ trợ xử lý bất đồng bộ *(Async I/O)*:
- Endpoint `POST /api/v1/events/ingest`: Tiếp nhận sự kiện từ Honeypot forwarder với xác thực qua Header `X-API-Key`.
- Endpoint `GET /api/v1/events`: Cung cấp dữ liệu truy vấn sự kiện cho Dashboard được bảo vệ bằng Token JWT từ Keycloak.

### 3.3.2. Xây dựng cơ chế khử trùng lặp nhật ký với Redis
```python
async def check_dedup(event_data: EventCreate) -> bool:
    payload_hash = hashlib.sha256(
        f"{event_data.source_ip}:{event_data.attack_type}:{event_data.payload}".encode()
    ).hexdigest()
    
    # Kiểm tra sự tồn tại trong Redis với TTL 60s
    exists = await redis_client.get(f"dedup:{payload_hash}")
    if exists:
        await redis_client.incr(f"count:{payload_hash}")
        return True  # Bị trùng lặp
    
    await redis_client.setex(f"dedup:{payload_hash}", 60, "1")
    return False
```

### 3.3.3. Xây dựng cơ sở dữ liệu PostgreSQL
Khởi tạo bảng `security_events` với các chỉ mục *(Index)* tối ưu hóa tốc độ truy vấn theo `timestamp`, `source_ip` và `attack_type`.

### 3.3.4. Đồng bộ dữ liệu chuẩn ECS vào Elasticsearch bằng Filebeat
Cấu hình Filebeat đọc file log JSON từ FastAPI và đẩy trực tiếp vào Elasticsearch index `honeypot-events-ecs-*` với cấu hình ánh xạ trường dữ liệu chính xác.

---

## 3.4. Xây dựng hệ thống phát hiện và phân tích tấn công

### 3.4.1. Tích hợp Suricata IDS để giám sát lưu lượng mạng
Cấu hình Suricata lắng nghe trực tiếp trên card mạng vật lý, xuất log cảnh báo và thông tin luồng gói tin mạng ra tệp `eve.json` đa luồng.

### 3.4.2. Xây dựng IDS/ML Bridge và trích xuất đặc trưng luồng mạng
Module `ids_bridge` liên tục đọc các sự kiện luồng từ `eve.json`, tổng hợp các gói tin theo từng phiên kết nối và tính toán vector 46 đặc trưng số học:

```python
# Trích đoạn tính toán đặc trưng luồng trong FlowAccumulator
features = {
    "Header_Length": flow.header_length,
    "Duration": flow.duration_seconds,
    "Rate": flow.packet_count / max(flow.duration_seconds, 0.001),
    "Srate": flow.src_packet_count / max(flow.duration_seconds, 0.001),
    "Drate": flow.dst_packet_count / max(flow.duration_seconds, 0.001),
    "Min": np.min(flow.packet_lengths),
    "Max": np.max(flow.packet_lengths),
    "AVG": np.mean(flow.packet_lengths),
    "Std": np.std(flow.packet_lengths),
    "SYN_Flag_Count": flow.syn_count,
    "ACK_Flag_Count": flow.ack_count,
    # ... đủ 46 đặc trưng chuẩn CICIoT2023
}
```

### 3.4.3. Tích hợp mô hình XGBoost để phân loại tấn công
Nạp file mô hình tối ưu `xgboost_original.ubj` vào bộ nhớ RAM và thực hiện suy luận:
```python
class XGBoostPredictor:
    def __init__(self, model_path: str):
        self.bst = xgb.Booster()
        self.bst.load_model(model_path)
        self.labels = ["Benign", "DDoS", "DoS", "BruteForce", "Recon", "Spoofing", "Mirai"]

    def predict(self, feature_vector: np.ndarray) -> tuple[str, float]:
        dmatrix = xgb.DMatrix(feature_vector.reshape(1, -1))
        probabilities = self.bst.predict(dmatrix)[0]
        class_idx = int(np.argmax(probabilities))
        return self.labels[class_idx], float(probabilities[class_idx])
```

### 3.4.4. Xây dựng cơ chế tương quan sự kiện
Thiết lập các luật tương quan trong Elasticsearch / Kibana Alerting Rule để kích hoạt cảnh báo mức độ cao (Critical Alert) khi phát hiện tấn công phối hợp đa vector.

---

## 3.5. Xây dựng Dashboard giám sát và điều hành SOC

### 3.5.1. Xây dựng giao diện trực quan bằng React, TailwindCSS và ECharts
Giao diện người dùng Single Page Application được xây dựng với các thành phần:
- Bảng điều khiển trung tâm với chế độ nền tối (Dark Mode) chuẩn giao diện SOC chuyên nghiệp.
- Biểu đồ nhiệt hiển thị mật độ tấn công theo giờ trong ngày.
- Biểu đồ phân bổ tỷ lệ các kỹ thuật tấn công theo khung MITRE ATT&CK.

### 3.5.2. Tích hợp xác thực và phân quyền người dùng
Sử dụng thư viện `keycloak-js` triển khai luồng **PKCE Authorization Code Flow**. Tự động đính kèm Bearer JWT Token vào mọi request gọi API của FastAPI và kiểm tra quyền của người dùng trước khi hiển thị các nút chức năng quản trị.

### 3.5.3. Xây dựng chức năng giám sát thời gian thực và báo cáo sự cố
- Kết nối **WebSocket / Polling** cập nhật danh sách sự kiện mới mỗi 3 giây mà không cần tải lại trang.
- Chức năng kết xuất toàn bộ sự kiện đã lọc ra tệp tin CSV phục vụ làm chứng cứ điều tra số.

---

<a id="chương-4"></a>
# CHƯƠNG 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ HỆ THỐNG

---

## 4.1. Thiết lập môi trường và phương pháp thực nghiệm

### 4.1.1. Mô hình thử nghiệm và công cụ sử dụng
Môi trường thực nghiệm được triển khai trên mạng Lab độc lập gồm:
- **Máy trạm phòng thủ (Defense Host)**: Chạy toàn bộ cụm 15+ container Honeypot, IDS Suricata, Backend, SIEM và Dashboard.
- **Máy trạm tấn công (Attacker Host)**: Chạy hệ điều hành **Kali Linux 2024**, sử dụng các công cụ kiểm thử chuẩn an ninh mạng: `sqlmap`, `Nmap`, `Hydra`, `Nikto`, `OWASP ZAP` và bộ công cụ tự động hóa `evaluation.run` của Part 09.

### 4.1.2. Kịch bản kiểm thử Web Honeypot
Thực hiện 10 kịch bản tấn công web chuẩn OWASP WSTG được định nghĩa trong `test_matrix.yml`:

| Mã kịch bản | Tên kịch bản | Phương thức & Điểm bẫy | Payload mẫu | Kỳ vọng phát hiện |
|---|---|---|---|---|
| `sqli_01` | SQL Injection | `POST /services/search` | `' OR 1=1; DROP TABLE users; --` | `sql_injection` |
| `xss_01` | Reflected XSS | `GET /services/search?q=` | `<script>alert('XSS_TEST')</script>` | `xss` |
| `xss_02` | Stored XSS | `POST /feedback/submit` | `<img src=x onerror=alert(1)>` | `stored_xss` |
| `trav_01` | Path Traversal | `GET /doc/view?file=` | `../../../../etc/passwd` | `path_traversal` |
| `idor_01` | IDOR | `GET /profile/view?id=` | `admin_root_id_999` | `idor` |
| `rfi_01` | Remote File Inclusion | `POST /template/load` | `http://evil.com/shell.txt` | `rfi` |
| `upload_01`| Unrestricted Upload | `POST /doc/upload` | `webshell.php (Content: <?php phpinfo(); ?>)` | `malicious_upload` |
| `cmd_01` | Command Injection | `POST /tools/ping` | `127.0.0.1; cat /etc/shadow` | `command_injection`|
| `xxe_01` | XML Entity Attack | `POST /api/xml/import` | `<!ENTITY xxe SYSTEM "file:///etc/hosts">` | `xxe` |
| `brute_01` | Brute Force Login | `POST /auth/login` | `admin / password123 (Vét cạn từ điển)` | `brute_force` |

### 4.1.3. Kịch bản kiểm thử phát hiện tấn công mạng
- Kịch bản quét cổng mạng Nmap: `nmap -sS -p 1-1000 -T4 <IP_HONEYPOT>`.
- Kịch bản vét cạn SSH Hydra: `hydra -L users.txt -P pass.txt ssh://<IP_HONEYPOT>:2222`.
- Kịch bản SYN Flood DoS: `hping3 --flood -S -p 8080 <IP_HONEYPOT>`.

---

## 4.2. Đánh giá khả năng thu thập và xử lý dữ liệu

### 4.2.1. Độ đầy đủ của Payload và thông tin phiên
Kết quả kiểm tra dữ liệu lưu trữ trong PostgreSQL và Elasticsearch cho thấy:
- **100% các trường thông tin then chốt** (`source_ip`, `user_agent`, `path`, `method`, `payload`) được thu thập trọn vẹn, không bị cắt xén.
- Toàn bộ các ký tự đặc biệt trong payload nhị phân và mã khai thác phức tạp đều được xử lý an toàn không gây lỗi cơ sở dữ liệu.

### 4.2.2. Hiệu quả của cơ chế khử trùng lặp dữ liệu
Trong thử nghiệm gửi 10.000 request Brute Force đăng nhập liên tiếp trong vòng 60 giây:
- Cơ chế Redis Dedup đã chặn thành công **9.950 bản ghi trùng lặp**, chỉ ghi nhận 50 bản ghi đại diện kèm theo bộ đếm tần suất tổng hợp.
- Giảm tải **99,5% dung lượng I/O ghi đĩa** của cơ sở dữ liệu PostgreSQL, bảo đảm hệ thống vận hành mượt mà khi xảy ra tấn công quy mô lớn.

---

## 4.3. Đánh giá khả năng phát hiện tấn công

### 4.3.1. Khả năng phát hiện của Web Honeypot và cơ chế dựa trên luật
- Cả **10/10 kịch bản kiểm thử tấn công ứng dụng web** đều được phát hiện chính xác tuyệt đối (**Tỷ lệ bao phủ đạt 100%**).
- Tự động ánh xạ thành công 100% mã kỹ thuật sang khung MITRE ATT&CK.

### 4.3.2. Độ chính xác của mô hình XGBoost
Mô hình XGBoost được đánh giá trên tập kiểm thử độc lập gồm **9.560.672 mẫu dữ liệu mạng thực tế** từ bộ dữ liệu CICIoT2023:

| Chỉ số đánh giá *(Metric)* | Giá trị thực nghiệm | Ý nghĩa đánh giá |
|---|---|---|
| **Độ chính xác tổng thể (Accuracy)** | **99,64%** | Phân loại đúng gần 10 triệu mẫu luồng mạng |
| **Độ chuẩn xác trung bình (Macro Precision)** | **91,34%** | Tỷ lệ cảnh báo chính xác trên cả 7 lớp nhãn |
| **Độ nhạy trung bình (Macro Recall)** | **91,94%** | Tỷ lệ bắt trúng tấn công thực tế |
| **Điểm F1 trung bình (Macro F1-Score)** | **91,61%** | Đánh giá cân bằng, không thiên lệch lớp đa số |
| **Điểm F1 có trọng số (Weighted F1)** | **99,64%** | Phản ánh chính xác theo phân bố dữ liệu thực tế |
| **Tỷ lệ báo sai trên lưu lượng sạch (Benign FPR)** | **6,10%** | Chỉ có 6,1% lưu lượng bình thường bị cảnh báo nhầm |

### 4.3.3. Ma trận nhầm lẫn và phân tích kết quả phân loại
Kết quả phân loại chi tiết theo từng lớp nhãn:
- Lớp **DDoS** và **DoS**: Điểm F1-Score đạt **99,9%** nhờ các đặc trưng luồng gói tin có tính quy luật rõ rệt.
- Lớp **Recon** và **Spoofing**: Điểm F1-Score đạt **98,5%**.
- Lớp **Mirai**: Điểm F1-Score đạt **97,2%**.
- Lớp **BruteForce**: Điểm F1-Score đạt **69,44%** (đây là lớp khó phân loại nhất do hành vi gửi gói tin gần tương đồng với lưu lượng truy cập thông thường).

---

## 4.4. Đánh giá khả năng phân tích hành vi và tương quan sự kiện

Thực nghiệm kịch bản tấn công phức tạp nhiều giai đoạn *(Multi-stage Attack Scenario)*:
1. Giai đoạn 1: Kẻ tấn công quét cổng Nmap (Port Scan).
2. Giai đoạn 2: Kẻ tấn công vét cạn mật khẩu SSH Cowrie (Brute Force).
3. Giai đoạn 3: Kẻ tấn công tiêm mã SQL Injection vào Web Honeypot.

**Kết quả đánh giá**:
- Các sự kiện đơn lẻ được ghi nhận độc lập tại các phân hệ tương ứng.
- Luật tương quan **Multi-vector Attack** của SIEM tự động kích hoạt sau 1,8 giây kể từ khi giai đoạn 3 diễn ra, hợp nhất 3 sự kiện thành một cảnh báo duy nhất ở mức độ khẩn cấp *(Critical)* trên Dashboard SOC.

---

## 4.5. Đánh giá hiệu năng và độ trễ hệ thống

Đo lường thời gian xử lý và tài nguyên phần cứng thực tế:

| Thành phần xử lý | Độ trễ trung bình (Mean Latency) | Độ trễ phân vị P95 (P95 Latency) |
|---|---|---|
| **Web Honeypot ghi nhận và chuyển tiếp** | 4,2 ms | 8,5 ms |
| **Suy luận mô hình AI (XGBoost Inference)** | **3,1 ms** | **4,8 ms** |
| **FastAPI tiếp nhận, Dedup và ghi PostgreSQL** | 6,5 ms | 12,0 ms |
| **Toàn trình từ tấn công đến hiển thị Dashboard** | **< 200 ms** | **< 350 ms** |

**Tiêu thụ tài nguyên bộ nhớ RAM**:
- Toàn bộ hệ thống 15+ container hoạt động ổn định trong mức **7,5 GB – 11,2 GB RAM**, hoàn toàn phù hợp để triển khai trên các máy chủ tầm trung.

---

## 4.6. Đánh giá mức độ an toàn và khả năng cô lập hệ thống

1. **Xác thực cơ chế Containment**: Qua hàng nghìn payload tấn công Command Injection và Upload Web Shell, không có bất kỳ tiến trình lạ nào được sinh ra trên máy chủ thật.
2. **Xác thực cơ chế Anti-Pivot**: Thử nghiệm thực hiện quét mạng nội bộ từ bên trong container `part2-web` bị chặn hoàn toàn bởi chính sách mạng Docker NetworkPolicy.
3. **Quản lý bí mật**: 100% mật khẩu cơ sở dữ liệu và khóa API được sinh ngẫu nhiên 32-byte hexa, không tồn tại mật khẩu mặc định trong mã nguồn.

---

## 4.7. Phân tích ưu điểm, hạn chế và khả năng phát triển

### Ưu điểm
- **Kiến trúc toàn diện và khép kín**: Tích hợp hoàn hảo giữa bẫy mồi nhử, cảm biến IDS mạng, trí tuệ nhân tạo, SIEM và SOC Dashboard.
- **Tốc độ suy luận AI vượt trội**: Dưới 5ms cho mỗi luồng mạng, sẵn sàng cho môi trường thời gian thực.
- **An toàn tuyệt đối**: Kiến trúc phân vùng 4 tầng loại bỏ triệt để nguy cơ bị lợi dụng làm bàn đạp tấn công.
- **Tự động hóa hoàn toàn**: Khởi động toàn bộ hạ tầng bằng 1 lệnh duy nhất.

### Hạn chế
- Mô hình phân loại đối với lớp tấn công Brute Force ở tầng mạng cần tiếp tục cải thiện độ nhạy.
- Môi trường thử nghiệm hiện tại chủ yếu tập trung trên dải mạng Lab cục bộ.

### Khả năng phát triển
- Ứng dụng mô hình học sâu chuỗi thời gian như **LSTM (Long Short-Term Memory)** để nâng cao độ chính xác nhận diện Brute Force.
- Tích hợp giao thức chia sẻ thông tin tình báo mối đe dọa quốc tế **MISP (Malware Information Sharing Platform)**.
- Mở rộng thêm các bẫy mồi nhử cho dịch vụ cơ sở dữ liệu (Database Honeypot) và dịch vụ điện toán đám mây (Cloud Honeypot).

---

<a id="kết-luận"></a>
# KẾT LUẬN

Công trình nghiên cứu đã xây dựng thành công **Hệ thống Web Honeypot thời gian thực tích hợp Trí tuệ nhân tạo và Trung tâm điều hành an ninh mạng (SOC)**. Đề tài đã giải quyết trọn vẹn cả bài toán lý thuyết lẫn thực tiễn trong công tác phòng thủ mạng chủ động:

1. **Về mặt lý thuyết & kiến trúc**: Xây dựng mô hình phòng thủ theo chiều sâu kết hợp bẫy mồi nhử đa tầng, cảm biến mạng IDS, mô hình Học máy XGBoost và hệ thống tương quan sự kiện SIEM chuẩn hóa theo Elastic Common Schema.
2. **Về mặt công nghệ & lập trình**: Hiện thực hóa thành công 9 module độc lập, hoàn chỉnh từ giao diện Web mồi nhử, API bất đồng bộ, bộ đệm khử trùng lặp Redis, cầu nối IDS/ML Bridge trích xuất 46 đặc trưng luồng mạng, cho đến Dashboard trực quan hóa với xác thực bảo mật Keycloak PKCE.
3. **Về mặt thực nghiệm & đánh giá**: Mô hình AI đạt độ chính xác ấn tượng **99,64%** trên gần 10 triệu mẫu dữ liệu lưu lượng mạng thực tế; hệ thống Honeypot phát hiện chính xác **100% các kịch bản tấn công web chuẩn OWASP**; thời gian suy luận AI dưới **5ms** và độ trễ toàn trình dưới **200ms**.

Hệ thống chứng minh tính khả thi cao, mở ra hướng ứng dụng hiệu quả cho các cơ quan, doanh nghiệp và trung tâm SOC nhằm nâng cao năng lực giám sát, thu thập thông tin tình báo mối đe dọa và bảo vệ an toàn không gian mạng.

---

<a id="tài-liệu-tham-khảo"></a>
# TÀI LIỆU THAM KHẢO

1. **Canadian Institute for Cybersecurity (2023)**, *CICIoT2023 Dataset: A real-time dataset and benchmark for IoT attacks*, University of New Brunswick.
2. **Chen, T., & Guestrin, C. (2016)**, *XGBoost: A Scalable Tree Boosting System*, Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 785–794.
3. **OWASP Foundation (2023)**, *OWASP Web Security Testing Guide (WSTG) v4.2*, Open Web Application Security Project.
4. **MITRE Corporation (2023)**, *MITRE ATT&CK Enterprise Matrix v14*, https://attack.mitre.org/.
5. **Elastic N.V. (2023)**, *Elastic Common Schema (ECS) Specification v8.11*, https://www.elastic.co/guide/en/ecs/current/index.html.
6. **Spitzner, L. (2002)**, *Honeypots: Tracking Hackers*, Addison-Wesley Longman Publishing Co., Inc.
7. **Oosterhof, M. (2020)**, *Cowrie SSH/Telnet Honeypot Architecture and Implementation*, https://github.com/cowrie/cowrie.
8. **Open Information Security Foundation (2023)**, *Suricata Intrusion Detection System Engine User Guide*, https://suricata.io/.
9. **IBM Security (2024)**, *Cost of a Data Breach Report 2024*, IBM Corporation.
10. **Red Hat (2023)**, *Keycloak Identity and Access Management Documentation v22*, https://www.keycloak.org/documentation.
11. **OWASP ModSecurity Core Rule Set (2023)**, *OWASP CRS v3.3.x Official Documentation*, https://coreruleset.org/.
