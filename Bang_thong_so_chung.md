# BẢNG THÔNG SỐ CHUNG – HỆ THỐNG BÁM NẮNG
Phiên bản 1.0 · lập trước khi hiệu chỉnh sáu quyển · 07/10/2026

| Hạng mục | Quy ước / giá trị thống nhất |
|---|---|
| Quy ước dấu | x dương về Tây; H dương sau giờ Mặt Trời 12h. beta là cao độ của pháp tuyến tấm pin đo từ mặt phẳng ngang (không phải độ nghiêng của mặt phẳng pin); mặt pin nghiêng 90°−beta so với ngang. |
| Phương vị | gamma=0° hướng Nam; gamma>0 về Tây, gamma<0 về Đông; giữ atan2 trong (-180°,180°]. Khớp azimuth giới hạn ±120° (giả thiết). |
| Hai trục | alpha là cao độ Mặt Trời; beta là cao độ pháp tuyến tấm pin đo từ mặt phẳng ngang (mặt phẳng pin nghiêng 90°−beta), nên beta lý tưởng=alpha và beta_cmd=clamp(alpha,0°…75°). Gamma thô không gập qua ±90°; vượt ±120° thì chỉ tiếp cận biên nếu cách <=60° ở lần đầu, sau đó latch đến đêm. |
| Bốn LDR / sai lệch | ET, WT, EB, WB: e1=(ET+EB)-(WT+WB) (Đông-Tây); e2=(ET+WT)-(EB+WB) (trên-dưới). e1<0 yêu cầu quay Tây; e2>0 yêu cầu nâng. |
| Lấy mẫu/lọc | Mỗi kênh lấy 16 mẫu ADC 12-bit; bỏ 2 mẫu thấp nhất và 2 cao nhất, trung bình 12 mẫu còn lại. K_cal chưa hiệu chuẩn: tạm dùng 1,0. |
| Dải ADC / pin | Mã 0…4095, điện áp chân <=3,3 V. LDR ET/WT/EB/WB: GPIO25/26/27/14 (ADC2, tắt Wi-Fi); biến trở azimuth GPIO36; biến trở nghiêng GPIO4 (không dùng GPIO2 vì strap lúc khởi động); đo áp pin GPIO39. GPIO34–39 chỉ input và không có pull-up/down nội; limit GPIO34/35 cần điện trở bias ngoài. |
| Ngưỡng / vùng chết | Bắt đầu lệnh khi /e/>=200 count; dừng khi /e/<=120 count (hysteresis); S_min=2500 count tổng bốn kênh là ngưỡng sơ bộ, cần hiệu chuẩn. |
| Động cơ | Một trục: 1 motor gạt mưa 12 V trục vít cho phương vị. Hai trục: thêm 1 motor cùng loại cho nâng. Nhãn 60 W chưa xác minh; chưa có mô-men/dòng đo. |
| Tải gió / tay đòn | Giả thiết: A=0,65 m²; rho=1,2 kg/m³; Cd=1,2; r_az=0,30 m; r_tilt=0,20 m; mô-men trọng lực dư nghiêng 3 N·m; hệ số thiết kế 1,5. Chưa kiểm chứng CAD/đo lực. |
| Chu kỳ / giới hạn lệnh | Kiểm tra tổng sáng 1 giây để khóa khi thiếu sáng; hiệu chỉnh góc theo LDR 2 phút; cập nhật thiên văn 30 phút; LCD 1 giây (timer độc lập). Motor kiểm tra hồi tiếp/limit mỗi 10 ms, lệnh tối đa 8 s; break-before-make 25 ms khi đảo chiều. Chưa thử phần cứng. |
| Cầu H / E-stop | AZ_THUAN/AZ_NGUOC (GPIO19/18), thêm TILT_LEN/TILT_XUONG (16/13); opto active-low: LOW/HIGH chạy, HIGH/HIGH khóa, LOW/LOW cấm. GPIO5 tránh. E-stop GPIO23: NC kéo GND, bình thường LOW; nhấn/đứt dây HIGH; cần liên động cắt nguồn/enable phần cứng, chưa xác minh. |
| Dòng motor | Nếu nhãn 60 W/12 V là công suất điện vào: khoảng 5 A/motor; một trục 1 motor, hai trục 2 motor (ước lượng 10 A tổng). Chưa đo dòng khởi động/kẹt. TIP41C 6 A max không chứng minh mạch đủ tải. |
| RTC/LCD | DS1307 0x68: đọc 7 thanh ghi BCD 0x00…0x06; kiểm tra ACK, đủ byte, CH, 24-hour và miền ngày/giờ. RTC lưu giờ dân dụng Việt Nam; dùng UTC+7, lambda tham chiếu ≈106,10°E và EoT để đổi giờ Mặt Trời. LCD1602/PCF8574 địa chỉ tham khảo 0x27 trên I²C GPIO21/22, cập nhật mỗi 1 giây. |
| Trạng thái bằng chứng | Chỉ tính/mô phỏng phần mềm đã chạy. Chưa xác nhận lắp ráp, hiệu chuẩn, đo dòng/mô-men, thử ngoài trời hoặc kiểm tra trên ESP32/RTC/motor thật; dự kiến hoàn tất trước 10/10/2026. |

**Tải gió tham khảo:** q=0,5 rho V²; F=q·Cd·A; M_az=1,5·F·0,30; M_tilt=1,5·(F·0,20+3). 20 N·m chỉ là mô-men kẹt giả định, không phải kết quả đo hay mô-men liên tục.

**Mức xác minh:** chưa có phép đo, hiệu chuẩn hoặc thử nghiệm phần cứng được xác nhận. Các giới hạn/giá trị thiết kế phải được xác minh trước khi vận hành.
