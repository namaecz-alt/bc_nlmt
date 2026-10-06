# -*- coding: utf-8 -*-
"""Noi dung moi ban 2 truc: ket qua mo phong, code mau 2 truc, dong co gat mua,
tien do tuan 5/10 - 10/10/2026."""

# ---------- thay the muc 2.4 va 2.5 ban goc (bo Arduino Mega khoi mach) ----------
NEW_24_25 = [
    ("h2", "2.4. Bộ điều khiển ESP32"),
    ("p", "Toàn bộ mạch điều khiển dùng một bo ESP32 duy nhất (kiến trúc Xtensa LX6 hai nhân, 240 MHz, 4 MB flash). Bo có 18 kênh ADC 12 bit, trong đó tám kênh ADC1 (GPIO36, 39, 34, 35, 32, 33, 25, 26) hoạt động ổn định cả khi bật WiFi, đủ cho bốn kênh LDR của ma trận và hai biến trở hồi tiếp góc của hai trục; LEDC cung cấp PWM; hai bus I²C/UART phục vụ RTC DS3231 và module ADS1115 đo U–I. Logic 3,3 V nên tín hiệu từ mạch công suất phải qua chia áp hoặc chuyển mức; nguồn logic lọc tách khỏi nhiễu động cơ [8]."),
    ("p", "ESP32 dư năng lực tính atan ngay trong vòng điều khiển, nhờ đó thực hiện được phương pháp suy ra góc cần quay từ ma trận LDR cho cả hai trục thay vì dò bước theo thời gian. Báo cáo không dùng bo Arduino nào trong mạch; Arduino chỉ xuất hiện với vai trò môi trường phát triển IDE ở quyển lập trình."),
    ("h2", "2.5. Động cơ gạt nước ô tô trục vít và hồi tiếp vị trí"),
    ("p", "Cả hai trục dùng động cơ gạt nước kính ô tô 12 V kèm hộp giảm tốc trục vít – bánh vít. Ưu điểm quyết định: cặp trục vít tự hãm nên khi ngắt điện hoặc dừng lệnh, tấm pin tự giữ vị trí dưới gió và trọng lượng bản thân mà không cần nuôi điện giữ — đặc biệt quan trọng với trục nghiêng luôn chịu mô-men trọng trường. Động cơ có mô-men danh định lớn (khoảng 8–12 N·m), giá thấp, sẵn có, kèm công tắc tự đỗ hữu ích khi tìm mốc home."),
    ("p", "Hạn chế cần xử lý: tốc độ cố định, dòng 3–6 A nên đóng cắt bằng module relay hoặc cầu H MOSFET kèm cầu chì riêng mỗi trục; mỗi trục lắp thêm biến trở xoay đồng trục làm hồi tiếp vị trí; chiều quay đảo bằng đổi cực qua hai kênh relay cho mỗi motor."),
]

# ---------- QUYEN NGHIEN CUU ----------
NGHIEN_CUU_H1_CH3 = "CHƯƠNG 3. KẾT QUẢ NGHIÊN CỨU VÀ KIỂM CHỨNG PHƯƠNG PHÁP BẰNG MÔ PHỎNG SỐ"
NGHIEN_CUU_CH3 = [
    ("h2", "3.1. Cấu hình mô phỏng"),
    ("p", "Phương pháp đề xuất được kiểm chứng bằng mô phỏng số viết bằng Python (tools/mo_phong.py trong kho báo cáo). Vị trí Mỹ Hào, Hưng Yên (20,93° Bắc; 106,06° Đông); bốn ngày đại diện 21/3, 21/6, 23/9, 21/12; bước thời gian 1–5 phút. Vectơ Mặt Trời tính từ xích vĩ và góc giờ; năng lượng trực xạ thu được tỉ lệ cosin góc tới; tấm đối chứng cố định nghiêng 21° hướng Nam."),
    ("p", "Cụm bốn LDR mô hình hóa đúng cấu hình gá β_s: trong mỗi mặt phẳng, cặp cảm biến lệch ±β_s so với pháp tuyến nên đáp ứng tỉ lệ với cos(Δ ∓ β_s); trên đó đặt thêm sai khác độ lợi ±5%, nhiễu đọc 2% và thành phần khuếch tán 15%. Trục nghiêng và trục phương vị dùng cùng một công thức suy góc với sai lệch của cặp kênh tương ứng."),
    ("h2", "3.2. Kết quả hiệu suất thu trực xạ của từng cấu hình"),
    ("tbl", [
        ["Ngày đại diện", "Tấm cố định 21°", "Bám 1 trục", "Tăng so cố định", "Bám 2 trục", "Tăng so 1 trục"],
        ["21/3", "67,5", "138,1", "+104,5%", "143,0", "+3,6%"],
        ["21/6", "104,0", "155,1", "+49,1%", "159,0", "+2,5%"],
        ["23/9", "66,5", "137,7", "+107,1%", "143,0", "+3,8%"],
        ["21/12", "29,1", "102,2", "+251,3%", "129,0", "+26,2%"],
    ], "{B}. Năng lượng trực xạ thu được trong ngày (đơn vị tương đối cos·dt)"),
    ("p", "Bám một trục Đông–Tây tăng 49–251% năng lượng trực xạ so với tấm cố định tùy mùa. Cấu hình hai trục — đúng đối tượng của báo cáo này — nhỉnh hơn một trục 2,5–3,8% quanh phân điểm nhưng tới 26,2% ngày đông chí, vì mùa đông Mặt Trời vừa đi thấp vừa lệch Nam, chỉ chỉnh phương vị thì không bù được độ cao. Đây là căn cứ định lượng chốt phạm vi chế tạo hai trục."),
    ("h2", "3.3. Kết quả độ chính xác của phép suy góc từ ma trận LDR"),
    ("p", "Với đáp ứng cos(Δ ∓ β_s), sai lệch chuẩn hóa của mỗi trục liên hệ đóng với góc lệch: e = tan Δ · tan β_s, suy ra Δ = atan(e/tan β_s). Khảo sát Monte Carlo 400 lần, góc lệch ban đầu 2–12°:"),
    ("tbl", [
        ["Điều kiện tín hiệu", "Sai số RMSE của góc suy ra"],
        ["Lý tưởng (kênh đồng đều, không nhiễu)", "0,00°"],
        ["Sai khác độ lợi ±5% giữa các kênh, chưa hiệu chuẩn", "1,98°"],
        ["Sai khác độ lợi ±5%, đã hiệu chuẩn hệ số kênh", "0,00°"],
        ["Nhiễu đọc 2%", "1,29°"],
        ["Thành phần khuếch tán 15%", "1,09°"],
        ["Tổng hợp cả ba, đã hiệu chuẩn hệ số kênh", "1,65°"],
    ], "{B}. Sai số của phép suy góc cần quay từ ma trận 4 LDR (β_s = 30°)"),
    ("p", "Hai quyết định thiết kế được chốt từ bảng: bắt buộc hiệu chuẩn hệ số độ lợi bốn kênh dưới sáng khuếch tán; chọn β_s = 30° vì tan β_s = 0,577 đủ nhạy (Δ = 3° cho e ≈ 0,030, lớn hơn nhiều nhiễu đọc) mà không bão hòa trong dải lệch ±40°. Kết quả áp dụng cho cả hai trục vì công thức suy góc là như nhau."),
    ("h2", "3.4. So sánh với phương pháp bám bước theo thời gian"),
    ("p", "Vòng kín cả ngày được mô phỏng cho luật cũ (dịch một bước góc cố định mỗi lần vượt ngưỡng — quay theo thời gian) và luật mới (suy góc từ ma trận, quay tới góc đích theo hồi tiếp biến trở), cùng chịu nhiễu 1%, lệch độ lợi 3%, khuếch tán 10%. Bảng dưới là kết quả trên trục phương vị; trục nghiêng có hành vi tương tự vì cùng công thức:"),
    ("tbl", [
        ["Ngày", "Ma trận δ=3°: sai số TB / số lần chạy", "Bước theo thời gian: sai số TB / số lần chạy"],
        ["21/3", "1,14° / 46 lần", "2,95° / 111 lần"],
        ["21/6", "1,10° / 48 lần", "2,65° / 110 lần"],
        ["23/9", "1,13° / 46 lần", "2,94° / 111 lần"],
        ["21/12", "1,14° / 47 lần", "3,17° / 110 lần"],
    ], "{B}. So sánh luật suy góc từ ma trận và luật bám bước theo thời gian"),
    ("img", "hinh_ve/ket_qua_mo_phong_1_truc.png", "{H}. Góc bám và sai số trong ngày 21/6 của phương pháp ma trận LDR"),
    ("p", "Phương pháp ma trận giảm sai số bám trung bình từ 2,65–3,17° xuống 1,10–1,14° và giảm số lần khởi động động cơ từ 110–111 xuống 46–48 lần mỗi ngày (−58%), có ý nghĩa trực tiếp với độ bền hai cụm trục vít của mô hình hai trục."),
    ("h2", "3.5. Phương pháp chốt cho mô hình hai trục"),
    ("b", "Đọc ma trận bốn LDR mỗi chu kỳ; tính e_nghiêng từ cặp trên–dưới và e_quay từ cặp trái–phải."),
    ("b", "Suy hai góc lệch bằng Δ = atan(e/tan β_s); chỉnh trục nghiêng trước, tới phiên trục phương vị, mỗi trục quay tới góc đích đọc từ biến trở hồi tiếp riêng."),
    ("b", "Vùng chết δ = 3° cho cả hai trục; β_s = 30°; không quay theo thời gian ở bất kỳ nhánh nào."),
    ("b", "Bắt buộc hiệu chuẩn hệ số độ lợi bốn kênh; kiểm tra tổng sáng, bão hòa và biến động trước khi phát lệnh; trục vít tự hãm giữ vị trí khi ngắt điện."),
]
NGHIEN_CUU_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"
NGHIEN_CUU_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Chốt phương pháp điều khiển hai trục: ma trận bốn LDR suy ra đồng thời Δ_nghiêng và Δ_quay bằng quan hệ đóng Δ = atan(e/tan β_s); bỏ hoàn toàn cách quay bước theo thời gian."),
    ("b", "Chạy mô phỏng số: chứng minh cấu hình hai trục vượt một trục 26,2% năng lượng trực xạ ngày đông chí; sai số suy góc sau hiệu chuẩn còn 1,65° ở điều kiện tổng hợp (Chương 3)."),
    ("b", "Chốt tham số: β_s = 30°, vùng chết δ = 3°, thứ tự chỉnh nghiêng trước – phương vị sau."),
    ("b", "Chốt phần cứng: ESP32 là vi điều khiển duy nhất cho cả hai trục; hai động cơ gạt nước ô tô trục vít tự giữ vị trí khi ngắt điện; hai biến trở hồi tiếp góc."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Đối chiếu vectơ Mặt Trời mô phỏng với SPA/pvlib, yêu cầu sai số hình học dưới 0,5°."),
    ("b", "Chế giá thử β_s và đo kiểm chứng đáp ứng cos(Δ ∓ β_s) với cụm LDR thực."),
    ("b", "Mở rộng mô phỏng vòng kín cho đồng thời hai trục để xác nhận thứ tự nghiêng–phương vị."),
    ("b", "Gửi quyển nghiên cứu xin góp ý của giảng viên hướng dẫn."),
]

# ---------- QUYEN CHE TAO ----------
CHE_TAO_H1_CH1 = "CHƯƠNG 1. PHƯƠNG ÁN THIẾT KẾ HỆ HAI TRỤC ĐÃ CHỐT"
CHE_TAO_H1_CH2 = "CHƯƠNG 2. THIẾT KẾ CƠ KHÍ, MẠCH ĐIỆN VÀ DANH MỤC VẬT TƯ"
CHE_TAO_H1_CH3 = "CHƯƠNG 3. LẮP RÁP, HIỆU CHUẨN VÀ AN TOÀN"
CHE_TAO_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"

CHE_TAO_CH1 = [
    ("h2", "1.1. Phương pháp điều khiển chốt: ma trận LDR suy ra hai góc quay"),
    ("p", "Bốn LDR gắn ở bốn góc tấm pin: trên-trái (L_TT), trên-phải (L_PT), dưới-trái (L_TD), dưới-phải (L_PD); mỗi cảm biến gá chếch ra ngoài góc β_s = 30° như nhau. Ma trận sáng được rút thành các đại lượng chuẩn hóa:"),
    ("eq", "S = L_TT + L_PT + L_TD + L_PD"),
    ("eq", "e_quay = [(L_PT + L_PD) − (L_TT + L_TD)] / S"),
    ("eq", "e_nghiêng = [(L_TT + L_PT) − (L_TD + L_PD)] / S"),
    ("p", "Với đáp ứng mỗi kênh tỉ lệ cos(Δ ∓ β_s) trong mặt phẳng của trục tương ứng, hai góc lệch được suy ra ngay trong một lần đọc:"),
    ("eq", "Δ_quay = atan(e_quay / tan β_s);   Δ_nghiêng = atan(e_nghiêng / tan β_s)"),
    ("p", "Góc đích của mỗi trục tính từ biến trở hồi tiếp riêng và giới hạn trong hành trình: θ_đích = sat(θ + Δ, θ_min, θ_max). Động cơ chỉ chạy khi |Δ| > δ = 3° và dừng khi hồi tiếp báo tới góc đích; trục nghiêng chỉnh trước rồi mới tới trục phương vị. Hộp giảm tốc trục vít tự hãm giữ tấm pin đứng yên khi ngắt điện — ưu điểm bắt buộc phải có ở trục nghiêng vốn luôn chịu mô-men trọng lượng."),
    ("h2", "1.2. Cấu trúc tổng thể hệ thống"),
    ("img", "hinh_ve/so_do_khoi_2_truc.png", "{H}. Sơ đồ khối hệ thống bám nắng hai trục dùng ESP32"),
    ("tbl", [
        ["Khối", "Cấu hình chốt", "Nhiệm vụ"],
        ["Cảm biến hướng", "4 LDR gá β_s = 30° ở 4 góc", "Lập ma trận sáng, tạo e_quay và e_nghiêng."],
        ["Hồi tiếp vị trí", "2 biến trở xoay 10 k đồng trục", "Báo góc hiện tại từng trục để dừng đúng góc đích."],
        ["Điều khiển", "ESP32 DevKit + RTC DS3231", "ADC 12 bit, lọc trung vị, suy hai góc, liên động, ghi log."],
        ["Đo kiểm", "ADS1115 (I²C, 16 bit)", "Đo U, I tấm pin phục vụ tính năng lượng."],
        ["Chấp hành", "2 motor gạt nước 12 V trục vít + 4 kênh relay", "Quay phương vị và nâng/hạ góc nghiêng; tự giữ khi mất điện."],
        ["Bảo vệ", "4 công tắc hành trình + nút dừng khẩn cấp", "Chặn quá hành trình từng trục, cắt lệnh an toàn."],
    ], "{B}. Các khối chức năng của hệ thống hai trục"),
    ("h2", "1.3. Bố trí cụm cảm biến và góc gá β_s"),
    ("img", "hinh_ve/bo_tri_4_ldr.png", "{H}. Bố trí 4 LDR ở bốn góc tấm pin và mặt cắt góc gá β_s"),
    ("p", "Góc gá β_s = 30° chốt từ mô phỏng tuần 5/10–10/10: Δ = 3° đã tạo e ≈ 0,030 (đủ nhạy) mà không bão hòa trong dải lệch ±40°. Bốn giá gá phải cùng mẫu, cùng góc, không bị khung hoặc dây che; sau hiệu chuẩn phải cố định chắc và ghi lại góc thực tế để cập nhật tan β_s trong chương trình."),
    ("h2", "1.4. Cơ cấu chấp hành và hồi tiếp vị trí"),
    ("p", "Trục phương vị đặt thẳng đứng trên đế xoay, trục nghiêng vuông góc qua khớp nâng hạ; cả hai đặt gần trọng tâm tấm pin. Mỗi trục một động cơ gạt nước ô tô 12 V nối tay đòn khớp bản lề; mỗi trục một biến trở xoay 10 k đồng trục chia áp về một kênh ADC1; bốn công tắc hành trình đặt trước điểm va chạm cơ khí ở hai đầu mỗi trục. Công tắc tự đỗ của motor phương vị dùng làm mốc home sau mỗi lần mất điện."),
]

CHE_TAO_CH2 = [
    ("h2", "2.1. Kết cấu cơ khí"),
    ("img", "hinh_ve/mo_hinh_co_khi_2_truc.png", "{H}. Mặt cắt mô hình cơ khí hai trục với hai động cơ gạt nước trục vít"),
    ("p", "Đế phẳng có bulông cân bằng; cụm đế xoay phương vị mang trục thép có bạc lót; khung nâng hạ gắn vuông góc, mang trục nghiêng và tai bắt tấm pin. Hai tay đòn nối hai motor với hai trục đều có khớp bản lề để khử sai lệch quỹ đạo; dây dẫn chừa dư theo hành trình cả hai trục; bốn công tắc hành trình gá sao cho cần gạt chạm trước khi cơ cấu va chạm cứng."),
    ("h2", "2.2. Kết quả tính chọn động cơ"),
    ("tbl", [
        ["Hạng mục", "Trục nghiêng", "Trục phương vị"],
        ["Mô-men trọng lượng tấm pin 0,9 kg", "≈ 1,3 N·m (lệch tâm 0,15 m)", "≈ 0 N·m (cân bằng quanh trục)"],
        ["Mô-men gió v = 10 m/s", "≈ 0,54 N·m", "≈ 1,1 N·m (cánh tay 0,3 m)"],
        ["Mô-men yêu cầu (×2,5 khởi động/ma sát trục vít)", "≈ 4,6 N·m", "≈ 2,8 N·m"],
        ["Motor gạt nước 12 V điển hình", "8 – 12 N·m", "8 – 12 N·m"],
        ["Hệ số an toàn", "≈ 2 – 2,5 lần", "≈ 3 – 4 lần"],
        ["Tự giữ khi ngắt điện", "Trục vít tự hãm — không trôi", "Trục vít tự hãm — không trôi"],
    ], "{B}. Tính chọn hai động cơ gạt nước cho hệ hai trục"),
    ("p", "Trục nghiêng là trục chịu tải nặng nhất vì luôn cõng mô-men trọng lượng; motor gạt nước vẫn dư mô-men với hệ số an toàn 2–2,5 lần và đặc biệt không trôi vị trí khi mất điện. Tốc độ trục ra chậm (1–2 vòng/phút) phù hợp vì mỗi lần hiệu chỉnh chỉ quay vài độ."),
    ("h2", "2.3. Mạch điện và phương pháp đọc ADC"),
    ("p", "Mạch chia áp bốn LDR và hai biến trở do sinh viên tự chế, tự hiệu chuẩn; báo cáo chốt phần xử lý tín hiệu phía ESP32: ADC1 12 bit suy hao 11 dB; mỗi kênh lấy 64 mẫu, lấy trung vị rồi trung bình nửa giữa; đổi sang milivôn theo hệ số hiệu chuẩn của bo. ADS1115 16 bit qua I²C đo U tấm pin (qua cầu chia) và dòng (qua ACS712) phục vụ tính năng lượng. Hai motor đóng cắt bằng hai module relay 2 kênh (hoặc hai cầu H MOSFET), mỗi motor một cầu chì 10 A; nguồn động cơ 12 V tách khối nguồn logic 5 V, mass chung một điểm."),
    ("img", "hinh_ve/so_do_ket_noi_2_truc.png", "{H}. Sơ đồ kết nối ESP32 của mô hình hai trục"),
    ("tbl", [
        ["Chân ESP32", "Tín hiệu", "Thiết bị / ghi chú"],
        ["GPIO36, 39, 34, 35 (ADC1)", "4 kênh analog", "Ma trận LDR: L_TT, L_PT, L_TD, L_PD."],
        ["GPIO32 (ADC1_CH4)", "1 kênh analog", "Biến trở hồi tiếp góc phương vị."],
        ["GPIO33 (ADC1_CH5)", "1 kênh analog", "Biến trở hồi tiếp góc nghiêng."],
        ["GPIO21 / GPIO22", "I²C", "ADS1115 đo U–I và RTC DS3231 chung bus."],
        ["GPIO26, GPIO27", "2 ngõ ra", "Hai kênh relay motor phương vị (đảo chiều)."],
        ["GPIO14, GPIO13", "2 ngõ ra", "Hai kênh relay motor nghiêng (đảo chiều)."],
        ["GPIO4, GPIO5", "Ngõ vào pull-up", "Công tắc hành trình hai đầu trục nghiêng."],
        ["GPIO18, GPIO19", "Ngõ vào pull-up", "Công tắc hành trình hai đầu trục phương vị."],
        ["GPIO25", "Ngõ vào pull-up", "Nút dừng khẩn cấp."],
        ["USB-UART", "Serial 115200", "Serial Monitor và ghi log thử nghiệm."],
    ], "{B}. Bảng chân kết nối chốt cho mô hình hai trục"),
    ("h2", "2.4. Danh mục vật tư và linh kiện"),
    ("tbl", [
        ["TT", "Hạng mục", "Thông số chốt", "SL"],
        ["1", "Tấm pin mặt trời", "6 V – 10 W kèm khung", "1"],
        ["2", "Quang trở LDR", "GL5528 cùng lô", "4"],
        ["3", "Mạch chia áp LDR + biến trở", "Sinh viên tự chế; biến trở xoay 10 k", "1 bộ"],
        ["4", "Bo điều khiển", "ESP32 DevKit 38 chân", "1"],
        ["5", "Module ADC 16 bit", "ADS1115 I²C", "1"],
        ["6", "Cảm biến dòng", "ACS712 5 A", "1"],
        ["7", "RTC", "DS3231 có pin nuôi", "1"],
        ["8", "Động cơ chấp hành", "Motor gạt nước ô tô 12 V trục vít", "2"],
        ["9", "Đóng cắt động cơ", "Module relay 2 kênh 10 A hoặc cầu H MOSFET", "2"],
        ["10", "Công tắc hành trình", "Cần gạt, tiếp điểm NC", "4"],
        ["11", "Nút dừng khẩn cấp", "Nút nhấn khóa", "1"],
        ["12", "Nguồn", "Ắc quy/nguồn 12 V 15 A + mạch hạ 5 V", "1 bộ"],
        ["13", "Vật liệu cơ khí", "Đế xoay, khớp nâng hạ, thép tròn, nhôm hộp, ốc vít", "1 bộ"],
        ["14", "Phụ trợ", "2 cầu chì 10 A, dây dẫn, hộp chống ẩm", "1 bộ"],
    ], "{B}. Danh mục vật tư – linh kiện đã chốt"),
]

CHE_TAO_CH3 = [
    ("h2", "3.1. Quy trình lắp ráp"),
    ("b", "Bước 1. Thử riêng hai động cơ gạt nước trên bàn: chiều quay, dòng không tải, công tắc tự đỗ, kiểm tra tự giữ khi ngắt điện đột ngột."),
    ("b", "Bước 2. Gia công đế xoay phương vị: lắp bạc lót, kiểm tra quay trơn 360°, căn hướng Bắc – Nam bằng la bàn."),
    ("b", "Bước 3. Gia công khớp nâng hạ trục nghiêng: vuông góc trục phương vị, không rơ lắc; đánh dấu mốc zero hai trục."),
    ("b", "Bước 4. Lắp hai tay đòn khớp nối motor – trục; siết vừa, bôi mỡ trục vít."),
    ("b", "Bước 5. Lắp hai biến trở hồi tiếp đồng trục; đo điện áp ba điểm (hai đầu + giữa) mỗi trục để lập bảng quy đổi góc."),
    ("b", "Bước 6. Lắp bốn công tắc hành trình và nút dừng khẩn cấp; đo thông mạch từng tiếp điểm."),
    ("b", "Bước 7. Chế và thử mạch chia áp bốn LDR cùng hai mạch biến trở; kiểm tra ngắn mạch trước khi cấp nguồn."),
    ("b", "Bước 8. Gá cụm LDR đúng ký hiệu và β_s = 30°; chụp ảnh ghi nhận bố trí."),
    ("b", "Bước 9. Đấu nối theo bảng chân; tách khối nguồn động cơ – nguồn logic; cố định dây theo hành trình cả hai trục."),
    ("b", "Bước 10. Cấp điện chạy không tải từng trục: quét chậm hai đầu, xác nhận liên động chặn đúng chiều và thoát ngược được."),
    ("b", "Bước 11. Chạy phối hợp hai trục theo lệnh thử: nghiêng trước – phương vị sau; xác nhận không cộng hưởng rung."),
    ("b", "Bước 12. Lắp tấm pin, siết ốc đối xứng, thử tự giữ khi ngắt điện rồi mới đưa ra ngoài trời."),
    ("h2", "3.2. Hiệu chuẩn bắt buộc trước khi chạy thuật toán"),
    ("b", "Hiệu chuẩn hệ số độ lợi bốn kênh LDR dưới nguồn sáng khuếch tán; lưu bảng hệ số vào chương trình (mô phỏng cho thấy bước này khử trọn sai số 1,98° do lệch kênh)."),
    ("b", "Kiểm tra chiều dấu hai sai lệch: chiếu mạnh phía phải thì e_quay dương, chiếu mạnh phía trên thì e_nghiêng dương theo quy ước lệnh; nếu ngược thì đảo hệ số trong bảng hiệu chuẩn."),
    ("b", "Hiệu chuẩn từng biến trở hồi tiếp ba điểm; ghi giới hạn điện áp hai đầu hành trình vào hằng số chương trình."),
    ("b", "Xác nhận vùng chết δ = 3° cho cả hai trục: che mờ đều cụm cảm biến, bảo đảm không phát lệnh."),
    ("h2", "3.3. An toàn"),
    ("b", "Mỗi motor một cầu chì 10 A ngay đầu nguồn 12 V; không chạm cụm trục khi đang cấp điện."),
    ("b", "Kiểm tra tự giữ của cả hai trục vít trước khi lắp pin: ngắt điện đột ngột khi trục nghiêng đang nâng, trục không được trôi xuống."),
    ("b", "Ngoài trời phải có hộp chống ẩm cho ESP32 và relay; gió mạnh thì ngắt nguồn và đưa tấm pin về vị trí nghỉ nằm ngang."),
]

CHE_TAO_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Chốt cơ cấu chấp hành hai trục là hai động cơ gạt nước ô tô trục vít; tính xong mô-men yêu cầu từng trục với hệ số an toàn 2–4 lần (Bảng chương 2); xác nhận tự giữ khi ngắt điện."),
    ("b", "Chốt sơ đồ khối, sơ đồ kết nối ESP32 hai trục và bảng chân đầy đủ (4 LDR + 2 biến trở + 4 relay + 4 hành trình)."),
    ("b", "Chốt danh mục vật tư 14 hạng mục và quy trình lắp ráp 12 bước có bước chạy phối hợp nghiêng trước – phương vị sau."),
    ("b", "Lập danh mục hiệu chuẩn bắt buộc: hệ số độ lợi bốn kênh, chiều dấu hai sai lệch, biến trở ba điểm, vùng chết δ = 3°."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Mua hai động cơ gạt nước, hai module relay, hai biến trở xoay, ADS1115 theo danh mục."),
    ("b", "Gia công đế xoay và khớp nâng hạ; thử bench từng motor kèm relay."),
    ("b", "Chế mạch chia áp bốn LDR và hai mạch biến trở; đo đặc tuyến từng kênh dưới đèn kiểm soát."),
    ("b", "Lập bảng quy đổi góc ba điểm cho cả hai biến trở hồi tiếp."),
]

# ---------- QUYEN LAP TRINH ----------
LAP_TRINH_H1_CH1 = "CHƯƠNG 1. MÔI TRƯỜNG LẬP TRÌNH ARDUINO IDE VÀ CÁCH NẠP CHO ESP32"
LAP_TRINH_H1_CH2 = "CHƯƠNG 2. CÁC NHÓM LỆNH CƠ BẢN DÙNG TRONG CHƯƠNG TRÌNH"
LAP_TRINH_H1_CH3 = "CHƯƠNG 3. PHƯƠNG PHÁP ĐỌC MA TRẬN LDR, SUY HAI GÓC VÀ CODE MẪU HAI TRỤC"
LAP_TRINH_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"

LAP_TRINH_CH1 = [
    ("h2", "1.1. Arduino IDE là gì"),
    ("p", "Arduino IDE là môi trường phát triển tích hợp miễn phí của Arduino.cc: soạn thảo sketch (tệp .ino), biên dịch, nạp firmware và quan sát dữ liệu qua Serial Monitor/Serial Plotter. Ngôn ngữ là C/C++ kèm hệ thống hàm và thư viện quản lý sẵn. Giao diện gồm thanh công cụ Verify/Upload/Serial Monitor, cửa sổ soạn thảo, khung chọn Board và Port, console báo lỗi và dung lượng bộ nhớ."),
    ("h2", "1.2. Vì sao không thể lập trình ESP32 trực tiếp trên Arduino IDE vừa cài"),
    ("b", "Bản phân phối Arduino IDE chỉ kèm lõi phần cứng AVR (ATmega328/2560) và SAM; trình biên dịch đi kèm chỉ là avr-gcc/arm-gcc."),
    ("b", "ESP32 là nhân Xtensa LX6 32 bit, khác hoàn toàn AVR 8 bit: tập lệnh, bản đồ bộ nhớ, trình biên dịch (xtensa-esp32-elf-gcc) và SDK thành phần (driver ADC, LEDC, WiFi, bootloader nạp qua UART) đều riêng."),
    ("b", "Chưa cài lõi thì IDE không nhận diện board ESP32, báo lỗi biên dịch; các hàm đặc thù như analogSetPinAttenuation, ledcWrite cũng không tồn tại trong lõi AVR."),
    ("b", "Giải pháp: cài lõi esp32 của Espressif vào chính Arduino IDE qua Boards Manager; sau đó sketch viết bằng ngữ pháp Arduino quen thuộc được biên dịch cho ESP32 mà không đổi thói quen lập trình."),
    ("h2", "1.3. Hướng dẫn cài bo ESP32 vào Arduino IDE"),
    ("b", "Bước 1. Cài Arduino IDE 1.8.x hoặc 2.x; cài driver USB-UART (CP210x/CH340) nếu máy chưa nhận cổng."),
    ("b", "Bước 2. File → Preferences → Additional Boards Manager URLs: thêm https://espressif.github.io/arduino-esp32/package_esp32_index.json."),
    ("b", "Bước 3. Tools → Board → Boards Manager → tìm “esp32” của Espressif Systems → Install (IDE tự tải toolchain Xtensa)."),
    ("b", "Bước 4. Tools → Board → esp32 → “ESP32 Dev Module”; Tools → Port chọn đúng COM; giữ Flash Frequency 80 MHz, Upload Speed 921600."),
    ("b", "Bước 5. Serial Monitor đặt 115200 baud; khi nạp dừng ở “Connecting...” thì giữ nút BOOT vài giây."),
    ("b", "Bước 6. Nạp sketch Blink mẫu xác nhận chuỗi biên dịch – nạp hoạt động trước khi viết chương trình hai trục."),
    ("h2", "1.4. Cấu trúc sketch và thư viện dùng trong đề tài"),
    ("p", "Sketch gồm khai báo toàn cục (chân, ngưỡng, bảng hiệu chuẩn), setup() chạy một lần (ADC, bốn kênh relay, I²C, Serial) và loop() thực hiện chu kỳ: đọc ma trận → suy hai góc → chỉnh nghiêng trước, phương vị sau → ghi log. Thư viện: Wire.h cho ADS1115 và DS3231; các hàm ADC/LEDC nội tại của lõi esp32; không cần thư viện Servo vì chấp hành là motor gạt nước đóng cắt bằng relay."),
]

LAP_TRINH_CH2 = [
    ("h2", "2.1. Nhóm cấu trúc và điều khiển luồng"),
    ("tbl", [
        ["Lệnh / cấu trúc", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["setup() / loop()", "void setup() { } void loop() { }", "Khởi tạo một lần; vòng lặp đọc ma trận – suy hai góc – quay hai trục."],
        ["if / else if / else", "if (fabs(dNghieng) > DEAD) { ... }", "Quyết định phát lệnh cho từng trục hay giữ vị trí."],
        ["switch – case", "switch (trangThai) { ... }", "Máy trạng thái mỗi motor: DỪNG – CHIỀU A – CHIỀU B."],
        ["for", "for (int i = 0; i < 64; i++) { ... }", "Lấy 64 mẫu ADC mỗi kênh để lọc trung vị."],
        ["while", "while (fabs(goc - gocDich) > 0.5) { ... }", "Vòng chờ motor tới góc đích, vẫn giám sát hành trình."],
        ["break / continue / return", "break;", "Thoát vòng lấy mẫu, bỏ mẫu lỗi, hàm trả về góc lệch."],
    ], "{B}. Nhóm lệnh cấu trúc và điều khiển luồng"),
    ("h2", "2.2. Nhóm vào/ra số và tương tự trên ESP32"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["pinMode", "pinMode(MOT_NG_A, OUTPUT);", "Cấu hình 4 chân relay, 4 hành trình, nút dừng."],
        ["digitalWrite / digitalRead", "digitalWrite(MOT_NG_A, HIGH);", "Đảo chiều hai motor; đọc công tắc hành trình."],
        ["analogRead", "analogRead(36);", "Đọc 4 kênh LDR và 2 biến trở hồi tiếp (ADC1)."],
        ["analogSetPinAttenuation", "analogSetPinAttenuation(36, ADC_11db);", "Dải đo 0 – 2,45 V không bão hòa."],
        ["analogReadResolution", "analogReadResolution(12);", "Độ phân giải 12 bit (4096 mức)."],
    ], "{B}. Nhóm lệnh vào/ra dùng cho ma trận LDR và hai motor"),
    ("h2", "2.3. Nhóm thời gian, toán học và truyền thông"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["millis()", "if (millis() - tPrev >= T_MAU)", "Định chu kỳ đọc ma trận không chặn vòng lặp."],
        ["atan / tan", "atan(e / tan(BETA_S));", "Công thức lõi suy hai góc lệch từ sai lệch chuẩn hóa."],
        ["constrain / fabs", "constrain(th, TH_MIN, TH_MAX);", "Hàm sat() giới hạn góc đích trong hành trình từng trục."],
        ["sort (mảng mẫu)", "sort(mau, mau + 64);", "Trung vị 64 mẫu loại đột biến nhiễu relay."],
        ["Serial.begin / printf", "Serial.printf(...)", "In bảng 4 kênh, e, hai Δ, góc đích để log và gỡ lỗi."],
        ["Wire.requestFrom", "Wire.requestFrom(0x48, 2);", "Đọc thanh ghi chuyển đổi của ADS1115."],
    ], "{B}. Nhóm lệnh thời gian, toán học và truyền thông"),
]

CODE_2TRUC = """// Doc ma tran 4 LDR, suy 2 goc va quay 2 truc - ESP32
// Nghieng truoc, phuong vi sau; moi truc 1 bien tro hoi tiep + 1 motor gat nuoc.
#include <Arduino.h>
#include <Wire.h>

const int PIN_LDR[4] = {36, 39, 34, 35};   // L_TT, L_PT, L_TD, L_PD (ADC1)
const int PIN_POT_NG = 32, PIN_POT_PV = 33;
const int MOT_NG_A = 26, MOT_NG_B = 27;    // motor nghien
const int MOT_PV_A = 14, MOT_PV_B = 13;    // motor phuong vi
const int LS_NG_1 = 4, LS_NG_2 = 5, LS_PV_1 = 18, LS_PV_2 = 19, NUT_DUNG = 25;

const float BETA_S = 0.5236;               // beta_s = 30 do (rad)
const float DEAD   = 0.0524;               // vung chet delta = 3 do
const float TH_MIN = -0.6981, TH_MAX = 1.2217;   // -40..+70 do (nghieng)
const float AZ_MIN = -1.0472, AZ_MAX = 1.0472;   // +/-60 do (phuong vi)
const float POT_MIN_V = 0.30, POT_MAX_V = 3.00;
const int N_MAU = 64;
const unsigned long T_MAU = 2000;
float K_cal[4] = {1.0, 1.0, 1.0, 1.0};
unsigned long tPrev = 0;

float docKenh(int chan) {                  // 64 mau, trung vi roi TB nua giua
  int mau[N_MAU];
  for (int i = 0; i < N_MAU; i++) { mau[i] = analogRead(chan); delayMicroseconds(40); }
  for (int i = 0; i < N_MAU - 1; i++)
    for (int j = i + 1; j < N_MAU; j++)
      if (mau[j] < mau[i]) { int t = mau[i]; mau[i] = mau[j]; mau[j] = t; }
  float s = 0; for (int i = 16; i < 48; i++) s += mau[i];
  return s / 32.0;
}

float docGoc(int chanPot, float gMin, float gMax) {
  float v = docKenh(chanPot) * 3.3 / 4095.0;
  return gMin + (v - POT_MIN_V) * (gMax - gMin) / (POT_MAX_V - POT_MIN_V);
}

bool lienDong(int ls1, int ls2) {
  return digitalRead(ls1) == LOW || digitalRead(ls2) == LOW ||
         digitalRead(NUT_DUNG) == LOW;
}

// quay mot truc toi goc dich, dung dung 0.5 do, giam sat hanh trinh
void quayTruc(int chanPot, int motA, int motB, int ls1, int ls2,
              float dGoc, float gMin, float gMax) {
  if (fabs(dGoc) <= DEAD) return;          // vung chet: giu vi tri
  float gocDich = constrain(docGoc(chanPot, gMin, gMax) + dGoc, gMin, gMax);
  bool chieuA = (dGoc > 0);
  if (lienDong(ls1, ls2)) return;          // chanh lien dong
  digitalWrite(motA, chieuA ? HIGH : LOW);
  digitalWrite(motB, chieuA ? LOW : HIGH);
  while (fabs(docGoc(chanPot, gMin, gMax) - gocDich) > 0.0087) {
    if (lienDong(ls1, ls2)) break;
    delay(10);
  }
  digitalWrite(motA, LOW); digitalWrite(motB, LOW);  // truc vit tu giu
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  for (int i = 0; i < 4; i++) analogSetPinAttenuation(PIN_LDR[i], ADC_11db);
  analogSetPinAttenuation(PIN_POT_NG, ADC_11db);
  analogSetPinAttenuation(PIN_POT_PV, ADC_11db);
  pinMode(MOT_NG_A, OUTPUT); pinMode(MOT_NG_B, OUTPUT);
  pinMode(MOT_PV_A, OUTPUT); pinMode(MOT_PV_B, OUTPUT);
  digitalWrite(MOT_NG_A, LOW); digitalWrite(MOT_NG_B, LOW);
  digitalWrite(MOT_PV_A, LOW); digitalWrite(MOT_PV_B, LOW);
  pinMode(LS_NG_1, INPUT_PULLUP); pinMode(LS_NG_2, INPUT_PULLUP);
  pinMode(LS_PV_1, INPUT_PULLUP); pinMode(LS_PV_2, INPUT_PULLUP);
  pinMode(NUT_DUNG, INPUT_PULLUP);
}

void loop() {
  if (millis() - tPrev < T_MAU) return;
  tPrev = millis();
  float L[4]; for (int i = 0; i < 4; i++) L[i] = docKenh(PIN_LDR[i]) * K_cal[i];
  float S = L[0] + L[1] + L[2] + L[3];
  if (S < 400 || S > 15000) { Serial.printf("S ngoai dai: %.0f\\n", S); return; }
  float eNghieng = ((L[0] + L[1]) - (L[2] + L[3])) / S;
  float eQuay    = ((L[1] + L[3]) - (L[0] + L[2])) / S;
  float dNghieng = atan(eNghieng / tan(BETA_S));
  float dQuay    = atan(eQuay / tan(BETA_S));
  // nghien truoc, phuong vi sau
  quayTruc(PIN_POT_NG, MOT_NG_A, MOT_NG_B, LS_NG_1, LS_NG_2,
           dNghieng, TH_MIN, TH_MAX);
  quayTruc(PIN_POT_PV, MOT_PV_A, MOT_PV_B, LS_PV_1, LS_PV_2,
           dQuay, AZ_MIN, AZ_MAX);
  Serial.printf("S=%.0f eNg=%+.3f eQuay=%+.3f dNg=%+5.1f dQuay=%+5.1f do\\n",
                S, eNghieng, eQuay, degrees(dNghieng), degrees(dQuay));
}"""

LAP_TRINH_CH3 = [
    ("h2", "3.1. Vì sao ma trận bốn LDR suy ra được hai góc cần quay"),
    ("p", "Trong mỗi mặt phẳng của từng trục, cặp cảm biến hai phía có trục cảm quang lệch ±β_s so với pháp tuyến, nên khi hướng Mặt Trời lệch góc Δ khỏi pháp tuyến, đáp ứng hai kênh tỉ lệ với cos(Δ ∓ β_s). Lập tỉ số sai lệch:"),
    ("eq", "e = (L_cùng_trục_dương − L_cùng_trục_âm)/(tổng cặp) = tan Δ · tan β_s"),
    ("p", "Đảo lại được góc lệch cần bù ngay trong một lần đọc, áp dụng đồng thời cho hai trục:"),
    ("eq", "Δ_quay = atan(e_quay / tan β_s);   Δ_nghiêng = atan(e_nghiêng / tan β_s)"),
    ("p", "Không còn nhánh dò bước theo thời gian. Mô phỏng Monte Carlo 400 lần (quyển nghiên cứu, Chương 3) cho thấy sau hiệu chuẩn hệ số kênh, sai số phép suy góc còn 1,65° với nhiễu 2% và khuếch tán 15% — dùng chung cho cả hai trục."),
    ("h2", "3.2. Phương pháp đọc ADC trên ESP32 và ví dụ so sánh giá trị"),
    ("b", "Dùng ADC1 (36, 39, 34, 35 cho LDR; 32, 33 cho hai biến trở) vì ADC2 bị tranh chấp khi bật WiFi; đặt analogReadResolution(12), analogSetPinAttenuation(…, ADC_11db) cho dải tuyến tính 0,15 – 2,45 V."),
    ("b", "Mỗi kênh lấy 64 mẫu cách nhau 40 µs, sắp xếp lấy trung vị rồi trung bình 32 giá trị giữa để loại xung nhiễu do bốn kênh relay đóng cắt."),
    ("b", "Nhân hệ số hiệu chuẩn K_cal[i] đo dưới sáng khuếch tán để bốn kênh cùng thang trước khi lập ma trận."),
    ("p", "Ví dụ lúc 9h30 ngày mùa đông (mức ADC): L_TT = 2450, L_PT = 1380, L_TD = 2260, L_PD = 1590. S = 7680; e_nghiêng = [(2450+1380) − (2260+1590)]/7680 = −0,0026 → Δ_nghiêng = −0,3° (trong vùng chết, không chỉnh); e_quay = [(1380+1590) − (2450+2260)]/7680 = −0,227 → Δ_quay = atan(−0,227/0,577) = −21,5°: phát lệnh quay trục phương vị 21,5° về phía Đông, đọc biến trở và dừng đúng góc đích. Hai trục được quyết định độc lập từ cùng một lần đọc ma trận."),
    ("h2", "3.3. Phương pháp quay tấm pin hai trục"),
    ("b", "Đọc biến trở hồi tiếp từng trục; θ_đích = sat(θ + Δ, θ_min, θ_max) với giới hạn riêng: nghiêng −40°…+70°, phương vị ±60°."),
    ("b", "Chỉnh trục nghiêng trước rồi tới trục phương vị để tránh cộng hưởng rung và để sai lệch phương vị đo sau khi mặt pin đã đúng độ cao."),
    ("b", "Mỗi trục chỉ chạy khi |Δ| > δ = 3°; vòng while đọc biến trở mỗi 10 ms, dừng khi |θ − θ_đích| ≤ 0,5°; bốn công tắc hành trình và nút dừng khẩn cấp phá vòng bất cứ lúc nào."),
    ("b", "Ngắt cả bốn kênh relay khi tới đích: hai hộp trục vít tự hãm giữ tấm pin đứng yên không tốn điện."),
    ("img", "hinh_ve/so_do_khoi_chuong_trinh.png", "{H}. Sơ đồ khối chương trình đọc ma trận LDR và suy ra góc quay"),
    ("img", "hinh_ve/luu_do_ma_tran_2_truc.png", "{H}. Lưu đồ thuật toán ma trận LDR cho mô hình hai trục"),
    ("h2", "3.4. Code mẫu hai trục (ESP32, Arduino IDE)"),
    ("code", CODE_2TRUC),
    ("p", "Hàm quayTruc() gói toàn bộ logic một trục: so vùng chết, tính góc đích có sat(), chặn liên động, chạy relay đúng chiều, vòng chờ hồi tiếp 0,5° và ngắt relay để trục vít tự giữ. loop() chỉ việc đọc ma trận, suy hai góc và gọi hàm theo thứ tự nghiêng trước – phương vị sau; chuyển về mô hình một trục chỉ là bỏ bớt một lần gọi hàm."),
    ("h2", "3.5. Kết quả kiểm thử chương trình bằng số liệu mô phỏng"),
    ("tbl", [
        ["Phép thử", "Kết quả"],
        ["Suy góc với tín hiệu lý tưởng", "Sai số 0,00° (khớp công thức đóng)."],
        ["Suy góc khi lệch độ lợi ±5%, đã hiệu chuẩn K_cal", "Sai số 0,00°; chưa hiệu chuẩn: 1,98°."],
        ["Vòng kín cả ngày, δ = 3° (trục phương vị)", "Sai số TB 1,10 – 1,14°; 46 – 48 lần chạy motor."],
        ["Vòng kín cả ngày, luật cũ bám bước theo thời gian", "Sai số 2,65 – 3,17°; 110 – 111 lần chạy motor."],
        ["Kiểm tra liên động trong code", "Hàm quayTruc hủy lệnh đúng trục khi một trong bốn công tắc tác động."],
        ["Năng lượng thu thêm của cấu hình hai trục", "+2,5…3,8% so 1 trục quanh phân điểm; +26,2% ngày đông chí."],
    ], "{B}. Kết quả kiểm thử logic chương trình trên dữ liệu mô phỏng"),
    ("img", "hinh_ve/ket_qua_mo_phong_1_truc.png", "{H}. Góc bám và sai số ngày 21/6 của phương pháp ma trận (trục phương vị)"),
]

LAP_TRINH_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Viết xong code mẫu hai trục: đọc ma trận 4 LDR, suy Δ_nghiêng và Δ_quay bằng atan, hàm quayTruc dùng chung cho hai motor có hồi tiếp biến trở và liên động bốn hành trình."),
    ("b", "Mô phỏng kiểm chứng logic: sai số bám 1,10–1,14° và 46–48 lần chạy motor mỗi ngày, tốt hơn rõ luật quay theo thời gian (Bảng mục 3.5)."),
    ("b", "Trình bày vì sao Arduino IDE không nạp được ESP32 khi chưa cài lõi Espressif và hướng dẫn cài bo từng bước (Chương 1)."),
    ("b", "Hệ thống hóa nhóm lệnh ESP32 thực dùng: ADC1 + attenuation, trung vị 64 mẫu, bốn kênh relay, millis, atan, constrain (Chương 2)."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Nạp code hai trục lên ESP32 thật; in bảng 4 kênh, e_nghiêng, e_quay ra Serial Monitor đối chiếu ví dụ mục 3.2."),
    ("b", "Hiệu chuẩn K_cal bốn kênh dưới sáng khuếch tán; hiệu chuẩn hai biến trở ba điểm và cập nhật hằng số giới hạn điện áp."),
    ("b", "Kiểm tra vòng while từng trục dừng đúng 0,5° và liên động phá vòng khi kéo tay công tắc hành trình."),
    ("b", "Thử trình tự nghiêng trước – phương vị sau ngoài trời một ngày đầy đủ, ghi log đối chiếu mô phỏng."),
]
