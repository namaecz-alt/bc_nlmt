# Bộ báo cáo đồ án hệ thống bám nắng mặt trời

Sáu quyển: hai cấu hình **một trục / hai trục**, mỗi cấu hình gồm **Nghiên cứu – Chế tạo – Lập trình**. Nội dung được sinh từ một nguồn Python chung; `Bang_thong_so_chung` là nguồn chuẩn cho dấu góc, giới hạn cơ khí, pin, chu kỳ và trạng thái xác minh.

## Phân công nội dung

- **Nghiên cứu 1:** quy ước tọa độ, công thức thiên văn, mô hình một trục, ma trận góc và proxy hình học.
- **Chế tạo 1:** giao diện phần cứng một trục, tải/góc phương vị, kế hoạch chế tạo/đo.
- **Lập trình 1:** ADC/LDR, bộ lọc, `K_cal`, `e1/e2` và kiểm tra số học.
- **Nghiên cứu 2:** mô hình hai khớp, `beta_cmd`, giới hạn azimuth/latch và mô phỏng hai trục.
- **Chế tạo 2:** giao diện cơ khí–điện hai trục, tải riêng từng khớp, GPIO và kế hoạch xác minh.
- **Lập trình 2:** DS1307/giờ Mặt Trời, điều khiển motor, limit/E-stop, LCD và chu kỳ tích hợp.

Nội dung chuyên môn trùng được thay bằng dẫn chiếu; công thức thiên văn chung không chép lại ở quyển hai trục. Sơ đồ/phần cứng trong báo cáo là phương án đề xuất nếu không có bằng chứng as-built. Chưa xác nhận lắp ráp, hiệu chuẩn, đo dòng/mô-men, thử ngoài trời hoặc chạy ESP32; các việc chưa làm được ghi kèm kế hoạch dự kiến.

## Các quy ước đáng chú ý

- `alpha` tính từ chân trời; `gamma=0°` hướng Nam, dương về Tây. Nhánh `atan2` trong `(-180°,180°]` được giữ nguyên.
- `beta` là cao độ pháp tuyến tấm pin từ phương ngang (mặt phẳng pin nghiêng `90°−beta`): `beta_cmd=clamp(alpha, 0°…75°)`. 21/6 giờ trưa tại tọa độ tham chiếu cần khoảng 87,5° nên lệnh bị kẹp ở 75° (chênh khoảng 12,5°). Azimuth có hành trình giả thiết `±120°`; vượt giới hạn thì giữ/latch, không quét vòng qua 180°.
- Ban đêm, thiếu sáng hoặc RTC lỗi: dừng cầu H và giữ góc hồi tiếp, không phát lệnh `(0,0)`.
- LDR: ET/WT/EB/WB trên GPIO25/26/27/14 (ADC2, tắt Wi-Fi); `e1=(ET+EB)-(WT+WB)`, `e2=(ET+WT)-(EB+WB)`. Mỗi kênh 16 mẫu, bỏ 2 thấp + 2 cao; `K_cal=1,0` chỉ là placeholder chưa hiệu chuẩn.
- Chu kỳ thống nhất: LCD 1 s (timer độc lập); kiểm tra tổng sáng để khóa khi thiếu sáng 1 s; hiệu chỉnh góc LDR 2 phút; cập nhật thiên văn 30 phút; giám sát motor/limit/E-stop 10 ms; một lệnh motor tối đa 8 s.
- GPIO2 bị loại do chân strapping; phương án POT nghiêng là GPIO4 (ADC2). GPIO5 tránh. E-stop GPIO23 dự kiến NC-to-GND, HIGH khi nhấn/đứt dây; cần liên động phần cứng độc lập.
- Các kích thước/tải gió/mô-men và nhãn motor chưa đo được ghi rõ là giả thiết. Proxy trực xạ không phải kWh hoặc phép đo điện.

## Dựng và kiểm tra

Dùng Python trong `/tmp/bc-env/bin/python`:

```bash
/tmp/bc-env/bin/python -m pip install -r requirements.txt
/tmp/bc-env/bin/python tools/export_common_spec.py
/tmp/bc-env/bin/python tools/mo_phong.py
/tmp/bc-env/bin/python tools/ve_hinh.py
/tmp/bc-env/bin/python tools/build_bao_cao.py
/tmp/bc-env/bin/python tools/xuat_pdf.py
/tmp/bc-env/bin/python tools/test_project.py
```

Kết quả chính:

- `Bang_thong_so_chung.md`, `.docx`, `.pdf` (PDF một trang).
- Sáu `Bao_cao_{1,2}_truc_{Nghien_cuu,Che_tao,Lap_trinh}.docx/.pdf`.
- `Bao_cao_day_du_6_phan.pdf`, bắt đầu bằng bảng thông số chung rồi đến sáu quyển.
- `Bao_cao_pdf_*.pdf` là tên tương thích lịch sử, được đồng bộ từ sáu PDF hiện hành (không phải bản nội dung khác).
- `hinh_ve/ket_qua_mo_phong.json` và các đồ thị mô phỏng/flowchart.
- `firmware/ldr_module.h` chỉ là giao diện chung giữa hai phần lập trình; chưa có firmware production hoặc xác nhận nạp phần cứng.

Mục lục Word là trường tự động; nếu Word chưa cập nhật, chọn **Update Field → Update entire table**. PDF được sinh từ cùng nguồn nội dung với mục lục liên kết.

**Lưu ý về nghiệm thu:** lệnh AI cũ được yêu cầu ở tiêu chí dự án hiện chưa có trong checkout hoặc nội dung nhận xét. Không tự đoán/thay lệnh đó bằng một lệnh khác; cần cung cấp đúng lệnh để chạy kiểm tra cuối cùng. `test_project.py` là unit/regression test nội bộ, không được coi là lệnh AI nghiệm thu.
