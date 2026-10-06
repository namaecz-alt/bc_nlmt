# -*- coding: utf-8 -*-
"""Noi dung BO SUNG (moi) cho ban 2 truc (Arduino Mega)."""

CHE_TAO_H1_CH1 = "CHƯƠNG 1. PHƯƠNG ÁN THIẾT KẾ HỆ THỐNG"
CHE_TAO_H1_CH2 = "CHƯƠNG 2. THIẾT KẾ CƠ KHÍ, MẠCH ĐIỆN VÀ DANH MỤC VẬT TƯ"
CHE_TAO_H1_CH3 = "CHƯƠNG 3. LẮP RÁP, HIỆU CHUẨN VÀ AN TOÀN"
CHE_TAO_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN TỚI"

INJECT = {
    "3.1": [("img", "hinh_ve/so_do_khoi_2_truc.png", "{H}. Sơ đồ khối hệ thống bám nắng hai trục")],
    "3.2": [("img", "hinh_ve/bo_tri_4_ldr.png",
             "{H}. Bố trí 4 LDR ở bốn góc tấm pin và mặt cắt góc gá β_s")],
    "3.6": [("img", "hinh_ve/mo_hinh_co_khi_2_truc.png",
             "{H}. Mô hình cơ khí hai trục: đế quay phương vị, khung chữ U và trục nghiêng có encoder")],
}

CHE_TAO_CH2 = [
    ("h2", "2.1. Kết cấu cơ khí hai bậc tự do"),
    ("p", "Đế mô hình là tấm thép/nhôm dày bắt cố định xuống nền thử; trên đế đặt ổ quay phương vị (vòng bi mặt phẳng hoặc bạc trụ) chịu toàn bộ khối lượng phần quay. Cột trụ ngắn đỡ khung chữ U mang trục nghiêng; tấm pin bắt giữa hai càng chữ U qua trục ngang. Bố trí sao cho trọng tâm tấm pin nằm sát trục nghiêng và trục nghiêng nằm sát tâm ổ phương vị để giảm mô-men giữ cho servo và motor."),
    ("p", "Trước khi chọn servo hoặc động cơ, cần ước lượng mô-men do trọng lượng, ma sát và gió, sau đó dự trữ hệ số an toàn. Cân bằng tấm pin quanh trục sẽ giảm đáng kể tải motor. Với mô hình nhẹ có thể thay motor nghiêng bằng servo vị trí thứ hai, nhưng nếu dùng DC gearmotor phải có encoder/biến trở phản hồi để biết góc thực và tránh điều khiển mù."),
    ("p", "Bố trí cặp công tắc ở hai đầu hành trình cho mỗi trục. Kiểm tra từng công tắc độc lập trước khi nối tải, xác nhận dừng đúng chiều, khả năng thoát ngược và trạng thái khi dây đứt. Thử servo/motor ở tốc độ thấp, có nút dừng và người giám sát; chỉ lắp tấm pin sau khi cơ cấu hoạt động êm và không va chạm. Quy định thêm vị trí nghỉ (ví dụ nghiêng về mức cao nhất, phương vị về giữa) để hệ thống về đó khi hết nắng hoặc khi có cảnh báo gió."),
    ("h2", "2.2. Mạch công suất, mạch cảm biến và nguồn"),
    ("p", "Bốn LDR được mắc giống nhau theo cấu hình nguồn → điện trở cố định R_f → nút ADC → LDR → GND; mỗi kênh thêm tụ lọc 100 nF và bố trí bốn kênh giống hệt nhau để dễ bù sai khác giữa các mẫu LDR. Vi điều khiển chuyển số ADC thành điện áp rồi quy đổi điện trở từng cảm biến theo công thức ở mục 1.3."),
    ("p", "Cầu H nhận PWM và hai tín hiệu chiều từ Arduino; chọn loại chịu dòng làm việc lẫn dòng kẹt trục, có chân báo lỗi/quá dòng nếu có. Servo phương vị cấp nguồn riêng đủ dòng khởi động; encoder dùng ngõ vào ngắt ngoài để đếm xung. Các đường PWM và tín hiệu encoder đi xa đường nguồn motor, xoắn đôi hoặc dùng dây bọc chống nhiễu cho tín hiệu encoder."),
    ("p", "Nguồn servo và motor được chọn theo dòng khởi động/kẹt trục, không lấy từ chân 5 V Arduino. Nối mass tham chiếu đúng cách, đặt tụ lọc gần driver, tách đường motor khỏi đường ADC và dùng bảo vệ quá dòng/quá áp phù hợp."),
    ("h2", "2.3. Sơ đồ kết nối chân đề xuất"),
    ("img", "hinh_ve/so_do_ket_noi_2_truc.png", "{H}. Sơ đồ kết nối cảm biến và cơ cấu với Arduino Mega 2560"),
    ("tbl", [
        ["Chân Arduino Mega", "Tín hiệu", "Thiết bị / ghi chú"],
        ["A0 – A3", "4 kênh analog", "L_TT, L_PT, L_TD, L_PD qua cầu phân áp + tụ lọc."],
        ["A6, A7", "2 kênh analog", "Cầu chia áp đo U pin và cảm biến dòng ACS712."],
        ["20 (SDA), 21 (SCL)", "I²C", "RTC DS3231, trở kéo lên trên module."],
        ["12", "Servo", "Servo phương vị (thư viện Servo)."],
        ["10 (PWM)", "PWM cầu H", "Điều chế độ rộng xung cho motor nghiêng."],
        ["22, 23", "Số ra", "Hai tín hiệu chiều quay A/B của cầu H."],
        ["2 (INT0), 3 (INT1)", "Ngắt ngoài", "Hai pha xung encoder của trục nghiêng."],
        ["26 – 29", "Số vào pull-up", "Bốn công tắc hành trình: phương vị 2 đầu, nghiêng 2 đầu."],
        ["USB (Serial0)", "Serial", "Serial Monitor và ghi log thử nghiệm."],
    ], "{B}. Bảng chân kết nối đề xuất cho mô hình hai trục"),
    ("h2", "2.4. Danh mục vật tư và linh kiện dự kiến"),
    ("tbl", [
        ["TT", "Hạng mục", "Thông số đề xuất", "SL"],
        ["1", "Tấm pin mặt trời nhỏ", "6 V – 10 W, kèm khung bắt vít", "1"],
        ["2", "Quang trở LDR", "GL5528 hoặc tương đương, cùng lô", "4"],
        ["3", "Điện trở cầu phân áp R_f", "10 kΩ ±1%, tụ lọc 100 nF", "4 bộ"],
        ["4", "Bo điều khiển", "Arduino Mega 2560 + cáp USB", "1"],
        ["5", "Đồng hồ thời gian thực", "Module DS3231 có pin nuôi", "1"],
        ["6", "Servo phương vị", "Servo mô-men cao (≥15 kg·cm) hoặc servo liền hộp giảm tốc", "1"],
        ["7", "Motor nghiêng", "DC giảm tốc 12 V có encoder", "1"],
        ["8", "Driver cầu H", "Chịu ≥2 lần dòng kẹt trục, có bảo vệ", "1"],
        ["9", "Công tắc hành trình", "Loại cần gạt, tiếp điểm NC", "4"],
        ["10", "Nút dừng khẩn cấp", "Nút nhấn tự giữ/khóa", "1"],
        ["11", "Cảm biến dòng", "ACS712 5 A hoặc shunt + khuếch đại", "1"],
        ["12", "Vật liệu cơ khí", "Đế thép/nhôm, cột trụ, khung chữ U, ổ bi mặt phẳng, ốc vít", "1 bộ"],
        ["13", "Nguồn", "12 V/5 A cho tải, nguồn 5 V/2 A cho logic", "2"],
        ["14", "Phụ trợ", "Board mạch, jack, dây dẫn, tụ lọc, cầu chì, hộp chống ẩm", "1 bộ"],
    ], "{B}. Danh mục vật tư – linh kiện dự kiến"),
    ("p", "Danh mục trên là cấu hình đề xuất để lập dự trù; khi mua thực tế cần đối chiếu thông số datasheet và ghi lại mã linh kiện đã dùng để bảo đảm tính lặp lại của phép thử."),
]

CHE_TAO_CH3_NEW = [
    ("h2", "3.1. Quy trình lắp ráp mô hình"),
    ("b", "Bước 1. Kiểm tra linh kiện rời: đo điện trở từng LDR dưới cùng nguồn sáng; thử DS3231; thử servo và motor+encoder quay thuận/nghịch không tải."),
    ("b", "Bước 2. Gia công đế và lắp ổ quay phương vị; kiểm tra độ phẳng và độ rơ của ổ."),
    ("b", "Bước 3. Lắp cột trụ và khung chữ U; lắp trục nghiêng, căn đồng tâm và kiểm tra quay trơn bằng tay."),
    ("b", "Bước 4. Lắp servo phương vị và cơ cấu truyền động trục nghiêng (khớp nối/bánh răng); đánh dấu mốc zero cơ khí của cả hai trục."),
    ("b", "Bước 5. Lắp bốn công tắc hành trình và nút dừng khẩn cấp; đo thông mạch từng tiếp điểm."),
    ("b", "Bước 6. Hàn mạch cầu phân áp bốn kênh, mạch cầu H và khối nguồn; kiểm tra ngắn mạch trước khi cấp điện."),
    ("b", "Bước 7. Lắp cụm bốn LDR lên bốn góc tấm pin theo đúng ký hiệu và góc gá β_s; chụp ảnh ghi nhận."),
    ("b", "Bước 8. Đấu nối theo bảng chân ở Chương 2; tách khối công suất và khối tín hiệu; cố định dây theo toàn bộ hành trình hai trục."),
    ("b", "Bước 9. Chạy thử không tải tốc độ thấp từng trục: xác nhận công tắc chặn đúng chiều, cho phép quay ngược để thoát, encoder đếm đúng chiều."),
    ("b", "Bước 10. Lắp tấm pin, siết ốc đối xứng, kiểm tra cân bằng và độ vững của đế trước khi thử có tải ngoài trời."),
    ("h2", "3.2. Hiệu chuẩn và kiểm tra trước vận hành"),
    ("b", "Hiệu chuẩn bốn LDR dưới cùng điều kiện sáng để đo offset và hệ số độ lợi; lưu bảng hệ số."),
    ("b", "Chiếu sáng từ trái, phải, trên, dưới và các hướng chéo; ghi R_TT, R_PT, R_TD, R_PD sau quy đổi; xác nhận e_quay và e_nghiêng đổi dấu đúng khi hướng sáng đi qua pháp tuyến."),
    ("b", "Kiểm tra riêng chiều quay motor: tác động ánh sáng mạnh hơn vào phía phải rồi xác nhận lệnh servo quay đúng chiều; chiếu sáng mạnh hơn phía trên rồi xác nhận trục nghiêng đi đúng chiều. Nếu ngược, sửa ánh xạ chiều hoặc dấu sau hiệu chuẩn, không đảo dấu rải rác trong nhiều nhánh chương trình."),
    ("b", "Đếm xung encoder cho một vòng trục để suy ra độ phân giải góc; đối chiếu với bước dịch chuyển dự kiến Δθ_nghiêng."),
    ("b", "Đối chiếu giờ DS3231 với giờ chuẩn; thiết lập múi giờ phục vụ ghi nhãn dữ liệu."),
    ("b", "Ghi một phiên log nền (bốn điện trở, hai sai lệch, góc servo, xung encoder) trước khi thử thuật toán."),
    ("h2", "3.3. An toàn khi chế tạo và vận hành"),
    ("b", "Không cấp nguồn công suất khi chưa kiểm tra ngắn mạch và chiều phân cực; dùng cầu chì cho nhánh tải."),
    ("b", "Không đặt tay vào vùng quay của hai trục khi đang cấp điện; tháo tấm pin trước khi chỉnh cơ khí."),
    ("b", "Khi thử ngoài trời phải có hộp chống ẩm cho mạch; đặt vị trí nghỉ và ngắt nguồn khi gió mạnh."),
    ("b", "Mọi thay đổi kết cấu, linh kiện hoặc chân kết nối đều ghi vào nhật ký chế tạo để bảo đảm lặp lại phép thử."),
]

CHE_TAO_CH4 = [
    ("h2", "4.1. Các công việc đã làm được"),
    ("b", "Xây dựng chỉ tiêu kỹ thuật và cấu trúc tổng thể mô hình hai trục (Chương 1)."),
    ("b", "Thiết kế kết cấu cơ khí: đế quay phương vị, khung chữ U, trục nghiêng có encoder, bốn công tắc hành trình (Chương 1, Chương 2)."),
    ("b", "Thiết kế mạch cảm biến bốn kênh, mạch cầu H – servo – encoder, phương án nguồn và bảng chân kết nối (Chương 2)."),
    ("b", "Lập danh mục vật tư dự kiến, quy trình lắp ráp 10 bước, danh mục hiệu chuẩn và quy tắc an toàn (Chương 2, Chương 3)."),
    ("h2", "4.2. Các công việc sẽ làm trong tuần tới (12/10 – 18/10/2026)"),
    ("b", "Mua/chuẩn bị linh kiện theo danh mục vật tư; thử riêng servo phương vị và motor nghiêng + encoder trên bàn thử."),
    ("b", "Gia công đế, ổ quay phương vị và khung chữ U; lắp trục nghiêng và quay thử không tải cả hai bậc tự do."),
    ("b", "Lắp mạch cảm biến và cầu H; kiểm tra bốn công tắc hành trình và liên động chặn/quay ngược từng trục."),
    ("b", "Hiệu chuẩn offset/độ lợi bốn kênh LDR và xác nhận chiều dấu e_quay, e_nghiêng trên giá chiếu sáng kiểm soát."),
    ("b", "Ghi nhật ký chế tạo, chụp ảnh các bước để bổ sung vào báo cáo hoàn chỉnh."),
]

# ---------------- QUYEN LAP TRINH ----------------
LAP_TRINH_H1_CH1 = "CHƯƠNG 1. MÔI TRƯỜNG LẬP TRÌNH ARDUINO"
LAP_TRINH_H1_CH2 = "CHƯƠNG 2. CÁC NHÓM LỆNH CƠ BẢN TRONG LẬP TRÌNH ARDUINO"
LAP_TRINH_H1_CH3 = "CHƯƠNG 3. TỔ CHỨC CHƯƠNG TRÌNH VÀ THUẬT TOÁN ĐIỀU KHIỂN"
LAP_TRINH_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN TỚI"

LAP_TRINH_CH1 = [
    ("h2", "1.1. Tổng quan về Arduino IDE"),
    ("p", "Arduino IDE là môi trường phát triển tích hợp miễn phí do Arduino.cc cung cấp, dùng ngôn ngữ C/C++ đã rút gọn cùng hệ thống thư viện sẵn có cho nhập/xuất, thời gian và truyền thông. Một chương trình trong Arduino IDE gọi là sketch, gồm tệp .ino chính và các tab/thư viện phụ. IDE đảm nhận biên dịch, liên kết với lõi của bo mạch được chọn, nạp firmware qua cổng nối tiếp và cung cấp Serial Monitor/Serial Plotter để quan sát dữ liệu thời gian thực."),
    ("p", "Giao diện gồm thanh công cụ (Verify/Compile, Upload, Serial Monitor), cửa sổ soạn thảo sketch, khung chọn Board và Port, cửa sổ console báo lỗi biên dịch và dung lượng bộ nhớ sau khi nạp. Trong đồ án này, Arduino IDE dùng cho bo Arduino Mega 2560; khi cần thử nghiệm trên ESP32 có thể dùng chính IDE này với gói bo mạch của Espressif, nhưng chương trình chính của đề tài viết cho Mega."),
    ("h2", "1.2. Cài đặt và cấu hình cho Arduino Mega 2560"),
    ("b", "Cài Arduino IDE (bản 1.8.x hoặc 2.x) từ trang chủ Arduino; cài driver USB-UART nếu máy tính chưa nhận cổng."),
    ("b", "Chọn Tools → Board → Arduino AVR Boards → Arduino Mega or Mega 2560; chọn Processor là ATmega2560 (Arduino Mega)."),
    ("b", "Chọn Tools → Port đúng cổng COM của mạch; mở Serial Monitor đặt 115200 baud khi gỡ lỗi."),
    ("b", "Nạp thử sketch ví dụ Blink để xác nhận chuỗi công cụ biên dịch và mạch nạp hoạt động trước khi viết chương trình chính."),
    ("b", "Quản lý thư viện qua Tools → Manage Libraries (Library Manager): cài thư viện Servo và thư viện RTC (ví dụ RTClib) nếu dùng."),
    ("h2", "1.3. Cấu trúc một chương trình (sketch)"),
    ("p", "Một sketch luôn có hai hàm bắt buộc: setup() chạy một lần sau cấp điện/reset để khởi tạo chân, thư viện, biến và tham số; loop() lặp vô hạn chứa logic đọc cảm biến – so sánh – phát lệnh – chờ đọc lại. Phần khai báo toàn cục ở đầu tệp gồm hằng số chân, ngưỡng, bước dịch chuyển, biến trạng thái và prototype các hàm tự viết."),
    ("p", "Vòng đời vận hành trong đề tài: setup() cấu hình ADC, Servo, PWM cầu H, ngắt encoder, chân công tắc hành trình và Serial → loop() thực hiện chu kỳ: đọc bốn điện trở → so sánh chéo → căn chỉnh độ nghiêng → căn chỉnh hướng xoay → dừng khi gần cân bằng → chờ T_đọc bằng millis() rồi đọc lại. Mọi tham số (δ_nghiêng, δ_quay, Δθ, T_đọc, t_settle, giới hạn góc) đặt tập trung ở đầu chương trình."),
    ("h2", "1.4. Thư viện sử dụng trong đề tài"),
    ("tbl", [
        ["Thư viện", "Vai trò trong đề tài"],
        ["Servo.h", "Điều khiển servo phương vị theo góc đặt từng bước."],
        ["Wire.h / RTClib", "Đọc giờ thực DS3231 để ghi nhãn thời gian cho dữ liệu log."],
        ["Hàm nội tại lõi AVR", "analogRead, digitalWrite, analogWrite, attachInterrupt, millis cho ADC, cầu H, encoder và định thời."],
    ], "{B}. Các thư viện dự kiến dùng trong chương trình"),
]

LAP_TRINH_CH2 = [
    ("h2", "2.1. Nhóm lệnh cấu trúc chương trình và điều khiển luồng"),
    ("tbl", [
        ["Lệnh / cấu trúc", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["setup()", "void setup() { ... }", "Khởi tạo chân ADC, Servo, PWM cầu H, ngắt encoder, Serial."],
        ["loop()", "void loop() { ... }", "Chu kỳ chính: đọc điện trở, so sánh, phát lệnh, chờ T_đọc."],
        ["if / else if / else", "if (abs(e_nghieng) > delta_nghieng) { ... }", "Quyết định trục nào dịch chuyển và chiều dịch chuyển."],
        ["switch – case", "switch (trangthai) { case NGHIENG: ... break; }", "Máy trạng thái: NGHIENG – XOAY – CAN_BANG – AN_TOAN."],
        ["for", "for (int i = 0; i < N; i++) { ... }", "Lấy N mẫu ADC liên tiếp cho mỗi kênh LDR."],
        ["while", "while (millis() - t0 < t_settle) { ktraCTHT(); }", "Chờ ổn định sau mỗi bước nhưng vẫn giám sát công tắc hành trình."],
        ["break / continue", "break; continue;", "Thoát vòng lấy mẫu; bỏ mẫu đột biến."],
        ["return", "return chieu;", "Hàm trả về chiều dịch chuyển (−1, 0, +1) của từng trục."],
    ], "{B}. Nhóm lệnh cấu trúc và điều khiển luồng"),
    ("h2", "2.2. Nhóm lệnh vào/ra số (digital I/O)"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["pinMode", "pinMode(chanCTHT, INPUT_PULLUP);", "Cấu hình 4 chân công tắc hành trình và nút dừng khẩn cấp."],
        ["digitalRead", "digitalRead(chanCTHT_nghieng_tren);", "Đọc giới hạn trước mỗi lệnh nâng/hạ hoặc xoay."],
        ["digitalWrite", "digitalWrite(chanChieuA, HIGH);", "Đặt chiều quay A/B cho cầu H của motor nghiêng."],
    ], "{B}. Nhóm lệnh vào/ra số"),
    ("h2", "2.3. Nhóm lệnh vào/ra tương tự và PWM"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["analogRead", "analogRead(A0);", "Đọc điện áp cầu phân áp của từng LDR và kênh đo U, I."],
        ["analogWrite", "analogWrite(chanPWM, PWM_nghieng);", "Điều chế PWM cho cầu H trong một bước nghiêng ngắn."],
        ["analogReference", "analogReference(DEFAULT);", "Chọn tham chiếu ADC phù hợp dải tín hiệu cầu phân áp."],
    ], "{B}. Nhóm lệnh vào/ra tương tự và PWM"),
    ("h2", "2.4. Nhóm lệnh thời gian"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["millis()", "unsigned long t = millis();", "Đo t_settle sau mỗi bước và chu kỳ đọc lại T_đọc mà không chặn việc giám sát công tắc."],
        ["delay", "delay(15);", "Chỉ dùng khi khởi tạo/thử nhanh; tránh trong loop chính."],
        ["delayMicroseconds", "delayMicroseconds(50);", "Giãn cách giữa các lần đọc ADC trong một chu kỳ lấy mẫu."],
        ["micros()", "micros();", "Đo chu kỳ xung encoder khi kiểm tra độ phân giải góc."],
    ], "{B}. Nhóm lệnh thời gian"),
    ("h2", "2.5. Nhóm lệnh toán học và biến đổi"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["abs", "abs(R_tren - R_duoi);", "So sánh chênh lệch điện trở với ngưỡng δ_nghiêng, δ_quay."],
        ["constrain", "constrain(gocServo, GV_MIN, GV_MAX);", "Giới hạn góc servo phương vị trong hành trình an toàn (hàm sat)."],
        ["map", "map(soADC, 0, 1023, 0, 5000);", "Quy đổi số ADC sang milivôn trước khi tính R_LDR."],
        ["min / max / round", "round(255 * u);", "Tính PWM_nghiêng = round(255·u) với u là hệ số độ rộng xung."],
    ], "{B}. Nhóm lệnh toán học và biến đổi"),
    ("h2", "2.6. Nhóm lệnh truyền thông"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["Serial.begin", "Serial.begin(115200);", "Mở cổng nối tiếp để gỡ lỗi và ghi log thử nghiệm."],
        ["Serial.print / println / printf", "Serial.printf(...);", "In bảng bốn điện trở và hai sai lệch theo định dạng cột."],
        ["Serial Plotter (hỗ trợ IDE)", "In nhiều kênh cách nhau bằng tab", "Quan sát e_nghiêng, e_quay khi hiệu chuẩn ngưỡng cân bằng."],
        ["Wire.begin / requestFrom", "Wire.requestFrom(DS3231_ADDR, 7);", "Đọc giờ thực phục vụ ghi nhãn thời gian dữ liệu."],
    ], "{B}. Nhóm lệnh truyền thông UART và I²C"),
    ("h2", "2.7. Nhóm lệnh ngắt và biến tự nguyện"),
    ("tbl", [
        ["Lệnh / từ khóa", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["attachInterrupt", "attachInterrupt(digitalPinToInterrupt(2), docXung, RISING);", "Đếm xung encoder của trục nghiêng để xác nhận bước dịch chuyển Δθ_nghiêng."],
        ["detachInterrupt", "detachInterrupt(digitalPinToInterrupt(2));", "Tạm ngừng đếm khi hiệu chuẩn hoặc khi trục nghỉ."],
        ["volatile", "volatile long soXung;", "Biến đếm xung dùng chung giữa ISR và loop phải khai báo volatile."],
    ], "{B}. Nhóm lệnh ngắt (đọc encoder)"),
    ("h2", "2.8. Kiểu dữ liệu, hằng số và toán tử"),
    ("p", "Chương trình dùng long cho đếm xung encoder và thời gian millis(), int cho số ADC 10 bit, float cho sai lệch và hệ số, bool cho cờ trạng thái, const/#define cho chân và ngưỡng. Các toán tử số học, so sánh, logic và gộp được dùng để viết gọn biểu thức so sánh điện trở và cập nhật góc đặt. Quy ước đặt tên (R_TT, e_quay, delta_quay, T_doc, t_settle) bám sát ký hiệu trong quyển nghiên cứu và quyển chế tạo để dễ đối chiếu."),
]

LAP_TRINH_CH3_PRE = [
    ("h2", "3.1. Tổ chức chương trình điều khiển"),
    ("img", "hinh_ve/so_do_khoi_chuong_trinh.png", "{H}. Sơ đồ khối chức năng của chương trình điều khiển"),
    ("p", "Khi triển khai cần kiểm tra chân, bộ định thời và thư viện thực tế, đặc biệt khi dùng đồng thời servo, PWM cầu H, encoder và RTC; các chân minh họa chỉ được chốt sau khi đối chiếu sơ đồ mạch và tài liệu chính thức, không mặc định mọi chân PWM hoặc interrupt đều tương đương."),
]

LAP_TRINH_CH3_POST = [
    ("h2", "3.3. Diễn giải lưu đồ thuật toán"),
    ("b", "Khởi tạo: cấu hình ADC, Servo, PWM/chiều cầu H, ngắt encoder, chân công tắc hành trình; nạp ngưỡng δ, bước Δθ, giới hạn góc, T_đọc và t_settle."),
    ("b", "Đọc bốn cảm biến và quy đổi ADC thành R_TT, R_PT, R_TD, R_PD."),
    ("b", "So sánh chéo hai cặp (R_TT, R_PD) và (R_PT, R_TD); tính R_trên, R_dưới, R_trái, R_phải; điện trở nhỏ hơn tương ứng phía nhận sáng mạnh hơn."),
    ("b", "Xét độ nghiêng: nếu chưa cân bằng và giới hạn cho phép thì motor nghiêng dịch một bước nhỏ về phía điện trở thấp hơn, rồi dừng và chờ ổn định; nếu cân bằng thì chuyển sang xét hướng xoay."),
    ("b", "Xét hướng xoay: nếu chưa cân bằng và giới hạn cho phép thì servo xoay một góc nhỏ về phía điện trở thấp hơn, rồi dừng và chờ ổn định."),
    ("b", "Khi cả hai trục cân bằng: dừng cả hai cơ cấu, chờ T_đọc rồi tự đọc lại bốn LDR; sau mỗi bước đều đọc lại cảm biến."),
    ("h2", "3.4. Tham số chương trình và hướng hiệu chỉnh"),
    ("tbl", [
        ["Tham số", "Ý nghĩa", "Cách hiệu chỉnh"],
        ["δ_nghiêng, δ_quay", "Ngưỡng cân bằng của hai trục.", "Tăng dần đến khi cơ cấu hết rung lúc nắng đều; không đặt quá lớn làm sai số bám tăng."],
        ["Δθ_nghiêng, Δθ_quay", "Bước dịch chuyển mỗi lần.", "Chọn nhỏ hơn độ phân giải cần thiết; kiểm tra bằng encoder và góc servo thực đo."],
        ["u (hệ số PWM)", "Độ rộng xung cho motor nghiêng.", "Giảm nếu bước nghiêng vọt lố, tăng nếu không đủ mô-men khởi động."],
        ["t_settle", "Thời gian chờ ổn định sau mỗi bước.", "Đủ để hết rung cơ khí trước khi đọc lại cảm biến."],
        ["T_đọc", "Chu kỳ đọc lại khi cân bằng.", "Cân bằng giữa độ bám theo mây và số lần chuyển động."],
        ["θ_min, θ_max (2 trục)", "Giới hạn mềm hành trình.", "Đặt lùi vào trong so với giới hạn cứng của công tắc."],
        ["β_s, bảng bù kênh", "Góc gá và hệ số hiệu chuẩn 4 kênh.", "Hiệu chuẩn một lần trên giá quay, lưu thành hằng số."],
    ], "{B}. Bảng tham số cần hiệu chỉnh của chương trình"),
    ("h2", "3.5. Quy trình kiểm thử chương trình"),
    ("b", "Thử khối đọc: in bốn điện trở quy đổi lên Serial, che từng cảm biến để xác nhận thứ tự kênh và chiều dấu e_quay, e_nghiêng."),
    ("b", "Thử servo phương vị: chạy quét chậm hai đầu, xác nhận constrain() giữ góc trong giới hạn và công tắc chặn đúng hướng."),
    ("b", "Thử motor nghiêng: chạy bước ngắn một chiều, đếm xung encoder đối chiếu Δθ_nghiêng; đảo chiều bằng hai tín hiệu A/B."),
    ("b", "Thử liên động: tác động từng công tắc bằng tay, xác nhận lệnh bị hủy đúng hướng và quay ngược thoát được."),
    ("b", "Thử trạng thái cân bằng: chiếu sáng đều để xác nhận hệ dừng và tự đọc lại sau T_đọc."),
    ("b", "Chạy bán tự động ngoài trời thời gian ngắn, ghi log đầy đủ bốn điện trở, hai sai lệch, góc servo, xung encoder và U/I trước khi chạy tự động dài ngày."),
]

LAP_TRINH_CH4 = [
    ("h2", "4.1. Các công việc đã làm được"),
    ("b", "Giới thiệu môi trường lập trình Arduino IDE, quy trình cài đặt và cấu hình bo Arduino Mega 2560 (Chương 1)."),
    ("b", "Hệ thống hóa 8 nhóm lệnh cơ bản kèm bảng cú pháp và ứng dụng trực tiếp trong đề tài (Chương 2)."),
    ("b", "Xây dựng sơ đồ khối chức năng chương trình và quy ước tổ chức tham số, dữ liệu ghi log (Chương 3)."),
    ("b", "Hoàn thiện lưu đồ thuật toán hai trục và bảng tham số cần hiệu chỉnh (Chương 3)."),
    ("h2", "4.2. Các công việc sẽ làm trong tuần tới (12/10 – 18/10/2026)"),
    ("b", "Viết sketch hoàn chỉnh cho Arduino Mega theo lưu đồ (code sẽ bổ sung ở báo cáo hoàn chỉnh)."),
    ("b", "Kiểm thử từng khối trên bàn: đọc 4 kênh ADC, quét servo, bước motor có encoder, liên động công tắc hành trình."),
    ("b", "Hiệu chỉnh δ_nghiêng, δ_quay, Δθ, t_settle, T_đọc bằng dữ liệu log từ mô hình ở quyển chế tạo."),
    ("b", "Chạy thử bán tự động ngoài trời và ghi bộ dữ liệu đầu tiên để so sánh với tấm pin cố định."),
]

NGHIEN_CUU_H1_CH3 = "CHƯƠNG 3. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN TỚI"
NGHIEN_CUU_CH3 = [
    ("h2", "3.1. Các công việc đã làm được"),
    ("b", "Xác định đề tài, mục tiêu và phạm vi cho mô hình bám nắng hai trục điều khiển bằng so sánh điện trở 4 LDR (Chương 1)."),
    ("b", "Tổng hợp đầy đủ cơ sở lý thuyết: pin quang điện, LDR, photodiode, Arduino Mega, servo, motor giảm tốc có encoder, công tắc hành trình (Chương 2)."),
    ("b", "Nghiên cứu hình học Mặt Trời và quy ước góc đặt cho tracker phương vị – góc cao (Chương 2)."),
    ("b", "Khảo sát, lập bảng so sánh toàn bộ các phương pháp bám nắng và tiêu chí lựa chọn (Chương 2)."),
    ("b", "Xác lập luật điều khiển so sánh điện trở hai cặp chéo, điều khiển theo bước và chu kỳ đọc lại T_đọc."),
    ("h2", "3.2. Các công việc sẽ làm trong tuần tới (12/10 – 18/10/2026)"),
    ("b", "Hoàn thiện trích dẫn và danh mục tài liệu tham khảo theo mẫu của trường."),
    ("b", "Chuẩn bị kịch bản mô phỏng đối chiếu: tín hiệu 4 LDR tổng hợp và góc tham chiếu tính theo SPA/pvlib."),
    ("b", "Xin góp ý của giảng viên hướng dẫn cho quyển nghiên cứu và chỉnh sửa theo nhận xét."),
    ("b", "Chốt danh mục linh kiện với quyển chế tạo để đặt mua trong tuần."),
]
