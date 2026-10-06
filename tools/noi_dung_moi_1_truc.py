# -*- coding: utf-8 -*-
"""Noi dung BO SUNG (moi) cho ban 1 truc.

Noi dung goc (Chuong 1, 2, 3 cua ban Word cu) duoc trich nguyen van boi
trich_xuat.py; o day chi chua cac khoi viet moi va cac khoi tien do.
Chu thich dung cho {H} / {B} de bo dem tu dong danh so hinh / bang.
"""

# ---------------- QUYEN CHE TAO ----------------
CHE_TAO_H1_CH1 = "CHƯƠNG 1. PHƯƠNG ÁN THIẾT KẾ HỆ THỐNG"
CHE_TAO_H1_CH2 = "CHƯƠNG 2. THIẾT KẾ CƠ KHÍ, MẠCH ĐIỆN VÀ DANH MỤC VẬT TƯ"
CHE_TAO_H1_CH3 = "CHƯƠNG 3. LẮP RÁP, HIỆU CHUẨN VÀ AN TOÀN"
CHE_TAO_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN TỚI"

# hinh chen vao cuoi cac muc nguyen van
INJECT = {
    "3.1": [("img", "hinh_ve/so_do_khoi_1_truc.png", "{H}. Sơ đồ khối hệ thống bám nắng một trục")],
    "3.2": [("img", "hinh_ve/bo_tri_4_ldr.png",
             "{H}. Bố trí 4 LDR ở bốn góc tấm pin và mặt cắt góc gá β_s")],
    "3.3": [("img", "hinh_ve/mo_hinh_co_khi_1_truc.png",
             "{H}. Mặt cắt mô hình cơ khí một trục: trục ngang Bắc – Nam, actuator và hai công tắc hành trình")],
}

CHE_TAO_CH2 = [
    ("h2", "2.1. Kết cấu cơ khí và truyền động"),
    ("p", "Trục quay được căn theo hướng Bắc – Nam thật (xác định bằng la bàn kết hợp đối chiếu giờ Mặt Trời) và đặt gần trọng tâm tấm pin để giảm mô-men. Hai gối đỡ cố định trên đế phẳng có bulông điều chỉnh cân bằng; trục dùng thép tròn hoặc trục nhôm có bạc lót/ổ bi để giảm ma sát. Tấm pin bắt lên khung đỡ qua các tai bắt vít, bảo đảm tâm khối lượng nằm sát trục để giảm tải giữ cho cơ cấu chấp hành."),
    ("p", "Cơ cấu chấp hành đề xuất là linear actuator hoặc servo mô-men cao gắn qua tay đòn vào khung pin; khớp nối phải có độ rơ nhỏ để tránh dao động khi đổi chiều. Nếu dùng servo, cần kiểm tra mô-men giữ ở điện áp thực tế và thêm gối đỡ chịu lực dọc trục. Dây dẫn từ phần quay sang phần tĩnh đi qua trục rỗng hoặc chừa dư chiều dài cho toàn bộ hành trình để tránh vướng khi quay."),
    ("p", "Hai đầu hành trình được xác định theo va chạm cơ khí, dây dẫn và khả năng quay của actuator; góc đặt phần mềm phải nằm bên trong giới hạn cứng. Công tắc hành trình được đặt sao cho cơ cấu chạm công tắc trước khi va vào khung; khi công tắc ở đầu Đông tác động, chương trình chỉ cấm chuyển động tiếp về phía Đông và cho phép lệnh quay ngược để rời công tắc."),
    ("h2", "2.2. Mạch điện chi tiết"),
    ("p", "Mỗi LDR mắc thành một cầu phân áp riêng theo cấu hình 3,3 V → điện trở cố định R_f → nút ADC → LDR → GND. Vi điều khiển đọc điện áp tại nút giữa rồi quy đổi điện trở theo công thức:"),
    ("eq", "R_LDR = R_f × V_ADC / (3,3 − V_ADC)"),
    ("p", "Chọn R_f cỡ trung bình nhân của dải điện trở LDR trong điều kiện làm việc dự kiến để độ nhạy trải đều; thêm tụ 100 nF tại nút ADC để lọc nhiễu và bố trí bốn kênh giống hệt nhau để dễ bù sai khác. Nếu đảo vị trí LDR và R_f thì phải đổi công thức quy đổi tương ứng."),
    ("p", "BH1750 và DS3231 cùng dùng bus I²C (SDA/SCL) với điện trở kéo lên phù hợp; hai thiết bị có địa chỉ khác nhau nên không xung đột. BH1750 chỉ làm kênh tham chiếu tương đối nếu dải đo đáp ứng; dưới nắng trực tiếp cảm biến độ rọi phổ thông có thể bão hòa. DS3231 có pin nuôi để giữ giờ khi mất điện, bảo đảm đường tham chiếu thiên văn không bị lệch sau khi khởi động lại."),
    ("p", "Nguồn actuator không được làm sụt nguồn điều khiển: dùng nguồn riêng cho tải động cơ, nối mass tham chiếu chung tại một điểm, đặt tụ lọc gần driver và tách đường dây motor khỏi đường tín hiệu ADC. Bảo vệ chân ADC khỏi quá áp bằng cầu chia áp hoặc mạch chuyển mức; thêm cầu chì và khóa nguồn tổng cho mô hình."),
    ("h2", "2.3. Sơ đồ kết nối chân đề xuất"),
    ("img", "hinh_ve/so_do_ket_noi_1_truc.png", "{H}. Sơ đồ kết nối cảm biến và cơ cấu với ESP32"),
    ("tbl", [
        ["Chân ESP32", "Tín hiệu", "Thiết bị / ghi chú"],
        ["GPIO36, 39, 34, 35 (ADC1)", "4 kênh analog", "L_TT, L_PT, L_TD, L_PD qua cầu phân áp + tụ lọc."],
        ["GPIO21 / GPIO22", "I²C (SDA/SCL)", "BH1750 và DS3231 dùng chung bus, có trở kéo lên."],
        ["GPIO32, GPIO33 (ADC1)", "2 kênh analog", "Cầu chia áp đo U pin và cảm biến dòng ACS712."],
        ["GPIO26 (LEDC_PWM)", "PWM điều khiển", "Driver/servo cơ cấu chấp hành một trục."],
        ["GPIO4, GPIO5", "Ngõ vào số pull-up", "Công tắc hành trình đầu Đông và đầu Tây."],
        ["GPIO18", "Ngõ vào số pull-up", "Nút dừng khẩn cấp."],
        ["USB-UART", "Serial", "Serial Monitor, ghi log trong quá trình thử nghiệm."],
    ], "{B}. Bảng chân kết nối đề xuất cho mô hình một trục"),
    ("h2", "2.4. Danh mục vật tư và linh kiện dự kiến"),
    ("tbl", [
        ["TT", "Hạng mục", "Thông số đề xuất", "SL"],
        ["1", "Tấm pin mặt trời nhỏ", "6 V – 10 W, kèm khung bắt vít", "1"],
        ["2", "Quang trở LDR", "GL5528 hoặc tương đương, cùng lô", "4"],
        ["3", "Điện trở cầu phân áp R_f", "10 kΩ ±1%, tụ lọc 100 nF", "4 bộ"],
        ["4", "Cảm biến độ rọi BH1750", "Module I²C", "1"],
        ["5", "Đồng hồ thời gian thực", "Module DS3231 có pin nuôi", "1"],
        ["6", "Bo điều khiển", "ESP32 DevKit 38 chân", "1"],
        ["7", "Cơ cấu chấp hành", "Servo mô-men cao (≥10 kg·cm) hoặc linear actuator 12 V", "1"],
        ["8", "Driver/nguồn chấp hành", "Theo cơ cấu chọn, có bảo vệ quá dòng", "1"],
        ["9", "Công tắc hành trình", "Loại cần gạt, tiếp điểm NC", "2"],
        ["10", "Nút dừng khẩn cấp", "Nút nhấn tự giữ/khóa", "1"],
        ["11", "Cảm biến dòng", "ACS712 5 A hoặc shunt + khuếch đại", "1"],
        ["12", "Vật liệu cơ khí", "Nhôm hộp/thép tròn trục, gối đỡ, ốc vít, đế gỗ hoặc nhôm", "1 bộ"],
        ["13", "Nguồn", "12 V/5 A cho tải, 5 V/2 A cho logic", "2"],
        ["14", "Phụ trợ", "Board mạch, jack, dây dẫn, tụ lọc, cầu chì, hộp chống ẩm", "1 bộ"],
    ], "{B}. Danh mục vật tư – linh kiện dự kiến"),
    ("p", "Danh mục trên là cấu hình đề xuất để lập dự trù; khi mua thực tế cần đối chiếu thông số datasheet (đặc biệt mô-men servo, dòng driver và dải đo cảm biến dòng) và ghi lại mã linh kiện đã dùng để bảo đảm tính lặp lại của phép thử."),
]

CHE_TAO_CH3_NEW = [
    ("h2", "3.1. Quy trình lắp ráp mô hình"),
    ("b", "Bước 1. Kiểm tra linh kiện rời: đo điện trở từng LDR dưới cùng nguồn sáng, thử BH1750 và DS3231 trên breadboard, thử servo/actuator không tải."),
    ("b", "Bước 2. Gia công đế và hai gối đỡ; căn trục ngang theo hướng Bắc – Nam thật và kiểm tra cân bằng bằng nivô."),
    ("b", "Bước 3. Lắp trục, bạc lót/ổ bi và khung đỡ tấm pin; quay thử bằng tay toàn hành trình để phát hiện điểm kẹt."),
    ("b", "Bước 4. Lắp cơ cấu chấp hành và tay đòn; đánh dấu vị trí giữa hành trình làm mốc zero cơ khí."),
    ("b", "Bước 5. Lắp hai công tắc hành trình và nút dừng khẩn cấp; kiểm tra bằng đồng hồ đo thông mạch từng tiếp điểm."),
    ("b", "Bước 6. Hàn/ghép mạch cầu phân áp bốn kênh và mạch nguồn; kiểm tra ngắn mạch trước khi cấp điện."),
    ("b", "Bước 7. Lắp cụm bốn LDR lên bốn góc tấm pin theo đúng ký hiệu và góc gá β_s đã chọn; chụp ảnh ghi nhận bố trí."),
    ("b", "Bước 8. Đấu nối theo bảng chân ở Chương 2; đi dây tách khối công suất và khối tín hiệu, cố định dây tránh vướng chuyển động."),
    ("b", "Bước 9. Cấp điện thử không tải: chạy quét chậm hai đầu hành trình, xác nhận công tắc chặn đúng chiều và cho phép quay ngược để thoát."),
    ("b", "Bước 10. Lắp tấm pin lên khung, siết ốc đối xứng, kiểm tra lại cân bằng trục và độ vững của đế trước khi thử có tải."),
    ("h2", "3.2. Hiệu chuẩn và kiểm tra trước vận hành"),
    ("b", "Hiệu chuẩn độ lệch/độ lợi của bốn kênh LDR dưới cùng một nguồn sáng khuếch tán; lưu bảng hệ số cho chương trình ở quyển lập trình."),
    ("b", "Chiếu sáng riêng từng hướng trái, phải, trên, dưới để xác nhận thứ tự kênh ADC và chiều dấu của e_quay, e_nghiêng."),
    ("b", "Thử góc gá β_s trong nhiều hướng sáng, kiểm tra ánh sáng bị khung che, rồi xác định vùng chết để cơ cấu không rung khi sai lệch nhỏ."),
    ("b", "Đối chiếu giờ của DS3231 với giờ chuẩn và thiết lập múi giờ, tọa độ nơi đặt mô hình."),
    ("b", "Chạy thử chế độ an toàn: tốc độ thấp, có người giám sát, nút dừng khẩn cấp luôn ở trạng thái sẵn sàng tác động."),
    ("b", "Ghi một phiên log ngắn (tín hiệu bốn kênh, S, e, góc đặt) để làm dữ liệu nền trước khi thử thuật toán."),
    ("h2", "3.3. An toàn khi chế tạo và vận hành"),
    ("b", "Không cấp nguồn công suất cho cơ cấu khi chưa kiểm tra ngắn mạch và chiều phân cực nguồn."),
    ("b", "Không chạm tay vào cụm trục đang chạy; tháo tấm pin trước khi chỉnh cơ khí."),
    ("b", "Giữ khu vực thử khô ráo; nếu thử ngoài trời phải có hộp chống ẩm cho mạch và ngắt nguồn khi mưa."),
    ("b", "Mọi thay đổi kết cấu, thay linh kiện hoặc đổi chân đều phải ghi vào nhật ký chế tạo để bảo đảm lặp lại được."),
]

CHE_TAO_CH4 = [
    ("h2", "4.1. Các công việc đã làm được"),
    ("b", "Xây dựng chỉ tiêu kỹ thuật và cấu trúc tổng thể mô hình một trục (Chương 1)."),
    ("b", "Thiết kế phương án cơ khí: trục ngang Bắc – Nam, gối đỡ, tay đòn, giới hạn hành trình và vị trí công tắc (Chương 1, Chương 2)."),
    ("b", "Thiết kế mạch cảm biến bốn kênh, mạch tham chiếu I²C, phương án nguồn – chống nhiễu và bảng chân kết nối (Chương 2)."),
    ("b", "Lập danh mục vật tư dự kiến, quy trình lắp ráp 10 bước và danh mục hiệu chuẩn, kiểm tra an toàn (Chương 2, Chương 3)."),
    ("h2", "4.2. Các công việc sẽ làm trong tuần tới (12/10 – 18/10/2026)"),
    ("b", "Mua/chuẩn bị linh kiện theo danh mục vật tư; đo kiểm từng LDR và cầu phân áp trước khi hàn mạch chính thức."),
    ("b", "Gia công đế, gối đỡ và trục quay; lắp khung pin và quay thử không tải toàn hành trình."),
    ("b", "Lắp mạch cảm biến, đọc thử bốn kênh ADC và kiểm tra chiều dấu e_quay trên giá quay có chiếu sáng kiểm soát."),
    ("b", "Hiệu chuẩn góc gá β_s và vùng chết sơ bộ; lắp công tắc hành trình và thử liên động chặn/quay ngược."),
    ("b", "Ghi nhật ký chế tạo và chụp ảnh các bước để bổ sung vào báo cáo hoàn chỉnh."),
]

# ---------------- QUYEN LAP TRINH ----------------
LAP_TRINH_H1_CH1 = "CHƯƠNG 1. MÔI TRƯỜNG LẬP TRÌNH ARDUINO"
LAP_TRINH_H1_CH2 = "CHƯƠNG 2. CÁC NHÓM LỆNH CƠ BẢN TRONG LẬP TRÌNH ARDUINO"
LAP_TRINH_H1_CH3 = "CHƯƠNG 3. TỔ CHỨC CHƯƠNG TRÌNH VÀ THUẬT TOÁN ĐIỀU KHIỂN"
LAP_TRINH_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN TỚI"

LAP_TRINH_CH1 = [
    ("h2", "1.1. Tổng quan về Arduino IDE"),
    ("p", "Arduino IDE là môi trường phát triển tích hợp miễn phí do Arduino.cc cung cấp, dùng ngôn ngữ C/C++ đã rút gọn cùng các hàm thư viện sẵn có cho nhập/xuất, thời gian và truyền thông. Một chương trình trong Arduino IDE gọi là sketch, gồm một tệp .ino chính và các tệp thư viện/tab phụ. IDE đảm nhận biên dịch, liên kết với lõi (core) của bo mạch được chọn, nạp firmware qua cổng nối tiếp và cung cấp Serial Monitor/Serial Plotter để quan sát dữ liệu thời gian thực."),
    ("p", "Các thành phần chính của giao diện gồm: thanh công cụ (Verify/Compile, Upload, Serial Monitor), cửa sổ soạn thảo sketch, khung chọn Board và Port, cửa sổ console hiển thị lỗi biên dịch và dung lượng bộ nhớ sau khi nạp. Với đồ án này, Arduino IDE là môi trường lập trình thống nhất cho cả hai cấu hình bo mạch: Arduino Mega 2560 và ESP32 (thông qua gói bo mạch do Espressif cung cấp)."),
    ("h2", "1.2. Cài đặt và cấu hình cho bo mạch ESP32"),
    ("b", "Cài Arduino IDE (bản 1.8.x hoặc 2.x) từ trang chủ Arduino; cài driver chuyển đổi USB-UART (CP210x/CH340) theo mạch nạp thực tế."),
    ("b", "Mở File → Preferences, thêm địa chỉ boards manager của Espressif vào mục “Additional Boards Manager URLs”."),
    ("b", "Mở Tools → Board → Boards Manager, tìm gói “esp32” của Espressif Systems và cài đặt; sau đó chọn Tools → Board → ESP32 Arduino → ESP32 Dev Module."),
    ("b", "Chọn Tools → Port đúng cổng COM của mạch; đặt tốc độ nạp và CPU Frequency theo mặc định khuyến nghị; bật Serial Monitor ở 115200 baud khi gỡ lỗi."),
    ("b", "Khi nạp cho một số mạch ESP32 cần giữ nút BOOT trong lúc IDE báo “Connecting...”; thao tác cụ thể tùy mạch nên ghi lại vào nhật ký."),
    ("h2", "1.3. Cấu trúc một chương trình (sketch)"),
    ("p", "Một sketch luôn có hai hàm bắt buộc: setup() chạy một lần ngay sau khi cấp điện hoặc reset, dùng để khởi tạo chân, thư viện, biến và tham số; loop() chạy lặp lại vô hạn sau setup(), chứa toàn bộ logic đọc cảm biến – tính toán – phát lệnh. Ngoài ra có phần khai báo toàn cục ở đầu tệp (hằng số, biến, đối tượng thư viện, prototype hàm tự viết) và các hàm tự định nghĩa được gọi từ loop()."),
    ("p", "Vòng đời vận hành của chương trình trong đề tài: khởi tạo một lần trong setup() (chân ADC, PWM, I²C, Serial, nạp tham số hiệu chuẩn) → vào loop() thực hiện chu kỳ: đọc mẫu – lọc – tính sai lệch – đánh giá chất lượng tín hiệu – phát lệnh có giới hạn – ghi log – chờ đủ chu kỳ bằng millis(). Cách tổ chức này giúp mọi tham số nằm ở một khối đầu chương trình, dễ hiệu chỉnh mà không phải sửa rải rác."),
    ("h2", "1.4. Thư viện sử dụng trong đề tài"),
    ("tbl", [
        ["Thư viện", "Vai trò trong đề tài"],
        ["Servo.h", "Phát xung điều khiển servo vị trí (nếu dùng servo làm cơ cấu chấp hành)."],
        ["Wire.h", "Giao tiếp I²C với BH1750 và DS3231."],
        ["RTClib (hoặc hàm Wire tự viết)", "Đọc ngày/giờ thực từ DS3231 phục vụ đường tham chiếu thiên văn."],
        ["Hàm ADC/PWM nội tại của lõi ESP32", "analogRead, analogReadResolution, analogSetPinAttenuation, ledcWrite cho kênh PWM."],
    ], "{B}. Các thư viện dự kiến dùng trong chương trình"),
]

LAP_TRINH_CH2 = [
    ("h2", "2.1. Nhóm lệnh cấu trúc chương trình và điều khiển luồng"),
    ("tbl", [
        ["Lệnh / cấu trúc", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["setup()", "void setup() { ... }", "Khởi tạo chân ADC, PWM, I²C, Serial và nạp tham số hiệu chuẩn."],
        ["loop()", "void loop() { ... }", "Vòng lặp chính: đọc cảm biến, chạy thuật toán, phát lệnh, ghi log."],
        ["if / else if / else", "if (dieukien) { ... } else { ... }", "Rẽ nhánh theo vùng chết, theo trạng thái công tắc hành trình, theo chất lượng ánh sáng."],
        ["switch – case", "switch (trangthai) { case 1: ... break; }", "Máy trạng thái: CHỜ – BÁM – GIỮ – AN_TOÀN."],
        ["for", "for (int i = 0; i < N; i++) { ... }", "Lấy N mẫu ADC liên tiếp để lọc trung vị/trung bình."],
        ["while", "while (digitalRead(pinCTHT) == LOW) { ... }", "Chờ có kiểm soát khi thoát khỏi công tắc hành trình (kèm giới hạn thời gian)."],
        ["break / continue", "break; continue;", "Thoát vòng lấy mẫu khi đủ điều kiện; bỏ qua mẫu đột biến."],
        ["return", "return giatri;", "Hàm tự viết trả về sai lệch, góc đặt hoặc trạng thái liên động."],
    ], "{B}. Nhóm lệnh cấu trúc và điều khiển luồng"),
    ("h2", "2.2. Nhóm lệnh vào/ra số (digital I/O)"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["pinMode", "pinMode(chan, INPUT_PULLUP);", "Cấu hình chân công tắc hành trình, nút dừng khẩn cấp (pull-up nội)."],
        ["digitalRead", "digitalRead(chanCTHT);", "Đọc trạng thái công tắc hành trình đầu Đông/Tây và nút dừng."],
        ["digitalWrite", "digitalWrite(chan, HIGH);", "Điều khiển đèn báo trạng thái, rơ-le cắt nguồn cơ cấu khi dừng khẩn cấp."],
    ], "{B}. Nhóm lệnh vào/ra số"),
    ("h2", "2.3. Nhóm lệnh vào/ra tương tự và PWM"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["analogRead", "analogRead(36);", "Đọc điện áp cầu phân áp của từng LDR và kênh đo U, I."],
        ["analogReadResolution (ESP32)", "analogReadResolution(12);", "Đặt độ phân giải ADC 12 bit phù hợp dải tín hiệu LDR."],
        ["analogSetPinAttenuation (ESP32)", "analogSetPinAttenuation(36, ADC_11db);", "Chọn suy giảm đầu vào để tránh bão hòa khi nắng gắt."],
        ["analogWrite / ledcWrite", "ledcWrite(kenhPWM, dutycycle);", "Phát PWM cho driver/servo của cơ cấu chấp hành một trục."],
        ["analogReference", "analogReference(DEFAULT);", "Tham chiếu ADC (với bo Arduino); ESP32 dùng attenuation thay cho reference."],
    ], "{B}. Nhóm lệnh vào/ra tương tự và PWM"),
    ("h2", "2.4. Nhóm lệnh thời gian"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["millis()", "unsigned long t = millis();", "Đo chu kỳ lấy mẫu T_mẫu và thời gian chờ đọc lại mà không chặn vòng loop."],
        ["delay", "delay(20);", "Chỉ dùng khi khởi tạo hoặc thử nghiệm nhanh; tránh dùng trong loop chính."],
        ["delayMicroseconds", "delayMicroseconds(50);", "Tạo khoảng cách giữa các lần đọc ADC liên tiếp trong một chu kỳ lấy mẫu."],
        ["micros()", "micros();", "Đo thời gian thực hiện một khối lọc khi tối ưu tốc độ vòng lặp."],
    ], "{B}. Nhóm lệnh thời gian"),
    ("h2", "2.5. Nhóm lệnh toán học và biến đổi"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["map", "map(giaTriADC, 0, 4095, 0, 3300);", "Quy đổi số ADC sang milivôn hoặc thang phần trăm."],
        ["constrain", "constrain(goc, GOC_MIN, GOC_MAX);", "Hiện thực hàm sat(): giới hạn góc đặt trong hành trình an toàn."],
        ["abs / min / max", "abs(e_quay);", "So sánh sai lệch với vùng chết δ, chọn biên độ bước."],
        ["round / floor / ceil", "round(PWM);", "Làm tròn giá trị PWM trước khi phát lệnh."],
        ["pow / sqrt / atan2", "atan2(y, x);", "Tính góc tham chiếu thiên văn R* từ các thành phần vectơ Mặt Trời."],
    ], "{B}. Nhóm lệnh toán học và biến đổi"),
    ("h2", "2.6. Nhóm lệnh truyền thông"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["Serial.begin", "Serial.begin(115200);", "Mở cổng nối tiếp tốc độ 115200 baud để gỡ lỗi và ghi log."],
        ["Serial.print / println / printf", "Serial.printf(...);", "In bảng số liệu S, e_quay, góc đặt, trạng thái theo định dạng cột."],
        ["Serial Plotter (hỗ trợ IDE)", "In nhiều kênh cách nhau bằng dấu cách/tab", "Quan sát trực quan bốn kênh LDR và sai lệch khi hiệu chuẩn."],
        ["Wire.begin / beginTransmission / requestFrom", "Wire.requestFrom(DS3231_ADDR, 7);", "Đọc thanh ghi giờ của DS3231 và dữ liệu độ rọi của BH1750."],
    ], "{B}. Nhóm lệnh truyền thông UART và I²C"),
    ("h2", "2.7. Nhóm lệnh ngắt và biến tự nguyện"),
    ("tbl", [
        ["Lệnh / từ khóa", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["attachInterrupt", "attachInterrupt(digitalPinToInterrupt(chan), hamISR, CHANGE);", "Đếm xung encoder hoặc bắt sự kiện nút dừng khẩn cấp (nếu cấu hình dùng ngắt)."],
        ["detachInterrupt", "detachInterrupt(digitalPinToInterrupt(chan));", "Tạm ngừng ngắt khi hiệu chuẩn để tránh đếm xung nhiễu."],
        ["volatile", "volatile unsigned long soXung;", "Biến dùng chung giữa ISR và loop phải khai báo volatile để tránh tối ưu sai."],
    ], "{B}. Nhóm lệnh ngắt"),
    ("h2", "2.8. Kiểu dữ liệu, hằng số và toán tử"),
    ("p", "Chương trình dùng các kiểu int/long cho đếm mẫu và thời gian millis(), float cho sai lệch chuẩn hóa và góc, bool cho cờ trạng thái, const và #define cho tham số cố định (chân, địa chỉ I²C, giới hạn góc). Các toán tử số học (+, −, *, /, %), so sánh (==, !=, >, <, >=, <=), logic (&&, ||, !) và toán tử gộp (+=, −=) được dùng để viết gọn các biểu thức lọc và cập nhật góc đặt. Quy ước đặt tên rõ ràng (L_TT, e_quay, delta, K_a, theta_dat) giúp đối chiếu trực tiếp giữa công thức ở Chương 1 quyển nghiên cứu và chương trình."),
]

LAP_TRINH_CH3_PRE = [
    ("h2", "3.1. Tổ chức chương trình điều khiển"),
    ("img", "hinh_ve/so_do_khoi_chuong_trinh.png", "{H}. Sơ đồ khối chức năng của chương trình điều khiển"),
    ("p", "Góc gá β_s, hệ số hiệu chuẩn, chu kỳ lấy mẫu, hệ số lọc, vùng chết và giới hạn góc cần được lưu thành tham số ở đầu chương trình để có thể hiệu chỉnh mà không sửa nhiều vị trí trong mã nguồn. Nếu dùng ESP32, bảo vệ chân ADC khỏi quá áp và nhiễu; nguồn actuator không được làm sụt nguồn điều khiển."),
]

LAP_TRINH_CH3_POST = [
    ("h2", "3.3. Logic đánh giá chất lượng tín hiệu trong phương án lai"),
    ("b", "Điều kiện độ sáng: S nằm trong dải làm việc [S_min, S_max]; ngoài dải thì không dùng hiệu chỉnh quang."),
    ("b", "Điều kiện ổn định: độ biến động của S trong cửa sổ trượt nhỏ hơn ngưỡng cho phép."),
    ("b", "Điều kiện không bão hòa: không kênh nào chạm trần/đáy ADC."),
    ("b", "Điều kiện nhất quán: |e_chéo| nhỏ hơn ngưỡng, loại trừ trường hợp che bóng hoặc hỏng một kênh."),
    ("b", "Chuyển chế độ có trễ: ngưỡng bật và ngưỡng tắt khác nhau (hysteresis) để tránh lật trạng thái liên tục khi mây lướt qua."),
    ("h2", "3.4. So sánh bốn phương án thuật toán khảo sát"),
    ("tbl", [
        ["Phương án", "Nội dung luật điều khiển", "Đặc điểm"],
        ["A1", "Đóng–ngắt: quay một bước cố định khi |e_a| vượt ngưỡng.", "Đơn giản, dễ rung nếu ngưỡng nhỏ."],
        ["A2", "Tỷ lệ: bước quay tỷ lệ với |e_a|.", "Bước lớn khi lệch nhiều, nhỏ dần khi gần đích."],
        ["A3", "Tỷ lệ + lọc + bù độ lợi + vùng chết.", "Giảm nhiễu và chuyển động thừa; cần hiệu chuẩn."],
        ["A4 (đề xuất)", "Lai: dùng hiệu chỉnh LDR khi tín hiệu đủ tin cậy; khi mây che hoặc cảm biến lỗi thì bám góc thiên văn R* hoặc giữ vị trí.", "Ổn định khi thời tiết xấu; cần logic đánh giá tín hiệu."],
    ], "{B}. Các phương án thuật toán khảo sát cho mô hình một trục"),
    ("h2", "3.5. Lưu đồ thuật toán"),
    ("img", "hinh_ve/luu_do_thuat_toan_1_truc.png", "{H}. Lưu đồ thuật toán lai thiên văn – cảm biến cho mô hình một trục"),
    ("b", "Khởi tạo: cấu hình ADC/PWM/I²C/Serial, nạp tham số δ, K_a, θ_min, θ_max, T_mẫu và bảng hệ số hiệu chuẩn bốn kênh."),
    ("b", "Đọc RTC và tính góc tham chiếu thiên văn R* từ ngày, giờ, vĩ độ – kinh độ đã lưu."),
    ("b", "Đọc bốn LDR, lọc mẫu đột biến, tính S, e_quay, e_nghiêng, e_chéo."),
    ("b", "Đánh giá độ tin cậy tín hiệu theo năm điều kiện ở mục 3.3: nếu đạt thì θ* = sat(R* + K_a·f(e_a, δ)); nếu không đạt thì θ* = R* (bám thiên văn thuần) hoặc giữ vị trí."),
    ("b", "Kiểm tra liên động công tắc hành trình trước khi phát lệnh: hướng đang bị chặn thì hủy lệnh hướng đó, chỉ cho phép quay ngược để thoát."),
    ("b", "Phát lệnh PWM/servo, ghi log toàn bộ tín hiệu và trạng thái, chờ hết chu kỳ T_mẫu rồi lặp lại."),
    ("h2", "3.6. Tham số chương trình và hướng hiệu chỉnh"),
    ("tbl", [
        ["Tham số", "Ý nghĩa", "Cách hiệu chỉnh"],
        ["δ (vùng chết)", "Ngưỡng sai lệch không phát lệnh.", "Tăng dần đến khi cơ cấu hết rung lúc trời nắng đều."],
        ["K_a", "Hệ số góc trên mỗi chu kỳ.", "Giảm nếu cơ cấu vọt lố, tăng nếu bám chậm."],
        ["θ_min, θ_max", "Giới hạn mềm của góc đặt.", "Đặt lùi vào trong so với giới hạn cứng của công tắc."],
        ["T_mẫu", "Chu kỳ lấy mẫu và phát lệnh.", "Chọn theo tốc độ cơ cấu và mức nhiễu tín hiệu."],
        ["S_min, S_max", "Dải tổng sáng cho phép dùng tín hiệu quang.", "Xác định từ log đo lúc trời râm và lúc nắng gắt."],
        ["Ngưỡng hysteresis", "Chênh lệch ngưỡng bật/tắt chế độ.", "Đủ lớn để mây thoáng không gây lật chế độ."],
        ["β_s, bảng bù kênh", "Góc gá và hệ số hiệu chuẩn 4 kênh.", "Hiệu chuẩn một lần trên giá quay, lưu thành hằng số."],
    ], "{B}. Bảng tham số cần hiệu chỉnh của chương trình"),
    ("h2", "3.7. Quy trình kiểm thử chương trình"),
    ("b", "Thử khối đọc: in bốn kênh ADC và S lên Serial Plotter, che từng cảm biến để xác nhận thứ tự kênh và chiều dấu."),
    ("b", "Thử khối lọc: so sánh tín hiệu trước/sau lọc khi tạo nhiễu bằng tay (bật tắt đèn nhanh)."),
    ("b", "Thử khối phát lệnh: chạy chế độ giả tải (không nối cơ cấu), in θ* và lệnh PWM để kiểm tra sat() và vùng chết."),
    ("b", "Thử liên động: tác động từng công tắc hành trình bằng tay, xác nhận lệnh bị chặn đúng hướng và quay ngược thoát được."),
    ("b", "Thử chế độ lai: giả lập S thấp (che cụm cảm biến) để xác nhận chuyển sang bám R* và trở lại có trễ."),
    ("b", "Chạy bán tự động ngoài trời thời gian ngắn, ghi log đầy đủ trước khi cho chạy tự động dài ngày."),
]

LAP_TRINH_CH4 = [
    ("h2", "4.1. Các công việc đã làm được"),
    ("b", "Giới thiệu môi trường lập trình Arduino IDE, quy trình cài đặt và cấu hình gói bo mạch ESP32 (Chương 1)."),
    ("b", "Hệ thống hóa 8 nhóm lệnh cơ bản kèm bảng cú pháp và ứng dụng trực tiếp trong đề tài (Chương 2)."),
    ("b", "Xây dựng sơ đồ khối chức năng chương trình và quy ước tổ chức tham số, dữ liệu ghi log (Chương 3)."),
    ("b", "Hoàn thiện lưu đồ thuật toán lai thiên văn – cảm biến và bảng tham số cần hiệu chỉnh (Chương 3)."),
    ("h2", "4.2. Các công việc sẽ làm trong tuần tới (12/10 – 18/10/2026)"),
    ("b", "Viết sketch hoàn chỉnh trên Arduino IDE cho ESP32 theo đúng lưu đồ (code sẽ bổ sung ở báo cáo hoàn chỉnh)."),
    ("b", "Kiểm thử từng khối trên bàn: đọc 4 kênh ADC, Serial Plotter, chiều lệnh cơ cấu, liên động công tắc hành trình."),
    ("b", "Hiệu chỉnh δ, K_a, T_mẫu bằng dữ liệu log thu được từ mô hình ở quyển chế tạo."),
    ("b", "Chạy thử bán tự động ngoài trời và đối chiếu góc đặt với đường tham chiếu thiên văn R*."),
]

# ---------------- QUYEN NGHIEN CUU: chuong tien do ----------------
NGHIEN_CUU_H1_CH3 = "CHƯƠNG 3. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN TỚI"
NGHIEN_CUU_CH3 = [
    ("h2", "3.1. Các công việc đã làm được"),
    ("b", "Xác định tên đề tài, mục tiêu, đối tượng và phạm vi nghiên cứu cho mô hình bám nắng một trục (Chương 1)."),
    ("b", "Tổng hợp đầy đủ cơ sở lý thuyết: pin quang điện, LDR, photodiode, ESP32/Arduino, servo và công tắc hành trình (Chương 2)."),
    ("b", "Nghiên cứu hình học Mặt Trời (góc cao, phương vị, xích vĩ, góc giờ) và công thức góc đặt R* cho trục ngang Bắc – Nam (Chương 2)."),
    ("b", "Khảo sát và lập bảng so sánh toàn bộ các nhóm phương pháp bám nắng; xác định tiêu chí lựa chọn phương án (Chương 2)."),
    ("b", "Định hướng bốn phương án thuật toán A1–A4 và chọn phương án lai thiên văn – cảm biến làm phương án đề xuất."),
    ("h2", "3.2. Các công việc sẽ làm trong tuần tới (12/10 – 18/10/2026)"),
    ("b", "Hoàn thiện danh mục tài liệu tham khảo và trích dẫn theo đúng mẫu của trường."),
    ("b", "Chuẩn bị bộ công thức/thư viện tính vị trí Mặt Trời (SPA, pvlib) làm đường tham chiếu để đối chiếu khi mô phỏng."),
    ("b", "Xin góp ý của giảng viên hướng dẫn cho quyển nghiên cứu và chỉnh sửa theo nhận xét."),
    ("b", "Phối hợp với quyển chế tạo để chốt danh mục linh kiện phục vụ mua sắm và chế tạo trong tuần."),
]
