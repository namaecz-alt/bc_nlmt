# -*- coding: utf-8 -*-
"""Noi dung moi ban 1 truc: ket qua mo phong, code mau, dong co gat mua,
tien do tuan 5/10 - 10/10/2026. Khoi ("code", ...) la listing chen nguyen dong."""

# ---------- thay the muc 2.4 va 2.5 ban goc (bo Arduino khoi mach) ----------
NEW_24_25 = [
    ("h2", "2.4. Bộ điều khiển ESP32"),
    ("p", "ESP32 (kiến trúc Xtensa LX6 hai nhân, 240 MHz, 4 MB flash) được chọn làm bộ điều khiển duy nhất của mô hình. Bo có 18 kênh ADC 12 bit, trong đó 8 kênh ADC1 (GPIO36, 39, 34, 35, 32, 33, 25, 26) ổn định ngay cả khi bật WiFi, đủ cho bốn kênh LDR và hai biến trở hồi tiếp; khối LEDC cung cấp PWM; các bus I²C/UART dùng cho RTC và module đo U–I. Mức logic 3,3 V nên không đưa tín hiệu 5 V trực tiếp vào chân ESP32 khi chưa có mạch chia áp hoặc chuyển mức; nguồn logic phải lọc tách khỏi nhiễu do động cơ [8]."),
    ("p", "So với các bo AVR 8 bit, ESP32 dư năng lực tính các hàm lượng giác (atan) ngay trong vòng điều khiển, nhờ đó thực hiện được phương pháp suy ra góc cần quay từ ma trận LDR mà không phải dò bước theo thời gian. Báo cáo không dùng bo Arduino nào trong mạch; Arduino chỉ xuất hiện với vai trò môi trường phát triển IDE ở quyển lập trình."),
    ("h2", "2.5. Động cơ gạt nước ô tô trục vít và hồi tiếp vị trí"),
    ("p", "Cơ cấu chấp hành đề xuất là động cơ gạt nước kính ô tô 12 V kèm hộp giảm tốc trục vít – bánh vít. Ưu điểm quyết định của lựa chọn này là cặp trục vít tự hãm: khi ngắt điện hoặc dừng cấp lệnh, trục vít không bị bánh vít kéo quay ngược, nên tấm pin tự giữ nguyên vị trí dưới tác động của gió và trọng lượng bản thân mà không cần nuôi điện giữ; động cơ còn có mô-men danh định lớn (khoảng 8–12 N·m), giá thành thấp, sẵn có và có công tắc tự đỗ (auto-park) hữu ích khi tìm mốc home."),
    ("p", "Hạn chế cần xử lý: tốc độ quay cố định, dòng làm việc 3–6 A nên phải đóng cắt bằng module relay hoặc cầu H MOSFET kèm cầu chì riêng; động cơ không tự báo góc nên phải lắp thêm biến trở xoay đồng trục làm hồi tiếp vị trí để chương trình biết góc hiện tại và dừng đúng góc đích. Chiều quay được đảo bằng cách đổi cực qua hai kênh relay."),
]

# ---------- QUYEN NGHIEN CUU: chuong ket qua ----------
NGHIEN_CUU_H1_CH3 = "CHƯƠNG 3. KẾT QUẢ NGHIÊN CỨU VÀ KIỂM CHỨNG PHƯƠNG PHÁP BẰNG MÔ PHỎNG SỐ"
NGHIEN_CUU_CH3 = [
    ("h2", "3.1. Cấu hình mô phỏng"),
    ("p", "Phương pháp đề xuất được kiểm chứng bằng mô phỏng số viết bằng Python (tools/mo_phong.py trong kho báo cáo), không suy diễn bằng tay. Vị trí mô phỏng là Mỹ Hào, Hưng Yên (20,93° Bắc; 106,06° Đông); bốn ngày đại diện 21/3, 21/6, 23/9 và 21/12; bước thời gian 1–5 phút từ 5h đến 19h giờ Mặt Trời. Vectơ Mặt Trời tính từ xích vĩ và góc giờ; thành phần trực xạ thu được tỉ lệ với cosin góc tới; tấm cố định đối chứng nghiêng 21° hướng Nam."),
    ("p", "Cụm bốn LDR được mô hình hóa đúng cấu hình gá: trong mặt phẳng quay, cảm biến bên phải có trục cảm quang lệch +β_s và bên trái lệch −β_s so với pháp tuyến, nên đáp ứng tỉ lệ với cos(Δ ∓ β_s) với Δ là góc lệch giữa hướng Mặt Trời và pháp tuyến. Trên mô hình này lần lượt đặt thêm sai khác độ lợi ±5% giữa các kênh, nhiễu đọc 2% và thành phần khuếch tán 15% để khảo sát độ bền của phương pháp."),
    ("h2", "3.2. Kết quả hiệu suất thu trực xạ của từng cấu hình"),
    ("tbl", [
        ["Ngày đại diện", "Tấm cố định 21°", "Bám 1 trục", "Tăng so cố định", "Bám 2 trục", "Tăng so 1 trục"],
        ["21/3", "67,5", "138,1", "+104,5%", "143,0", "+3,6%"],
        ["21/6", "104,0", "155,1", "+49,1%", "159,0", "+2,5%"],
        ["23/9", "66,5", "137,7", "+107,1%", "143,0", "+3,8%"],
        ["21/12", "29,1", "102,2", "+251,3%", "129,0", "+26,2%"],
    ], "{B}. Năng lượng trực xạ thu được trong ngày (đơn vị tương đối cos·dt)"),
    ("p", "Kết quả cho thấy bám một trục Đông–Tây đã thu thêm 49% đến 251% năng lượng trực xạ so với tấm cố định tùy mùa, mùa đông chênh lệch lớn nhất vì Mặt Trời đi thấp và lệch Nam; hệ hai trục nhỉnh hơn một trục 2,5–3,8% vào các ngày gần phân điểm nhưng tới 26,2% ngày đông chí. Đây là căn cứ định lượng để chốt phạm vi cơ khí: mô hình một trục đủ đại diện cho phần thuật toán, còn cấu hình hai trục dùng khi cần khảo sát mùa đông."),
    ("h2", "3.3. Kết quả độ chính xác của phép suy góc từ ma trận LDR"),
    ("p", "Từ mô hình đáp ứng cos(Δ ∓ β_s), quan hệ chính xác giữa đại lượng đo được và góc lệch là e = (L_phải − L_trái)/(L_phải + L_trái) = tan Δ·tan β_s, suy ra Δ = atan(e/tan β_s). Phép suy góc này được khảo sát Monte Carlo 400 lần với góc lệch ban đầu 2–12°:"),
    ("tbl", [
        ["Điều kiện tín hiệu", "Sai số RMSE của góc suy ra"],
        ["Lý tưởng (kênh đồng đều, không nhiễu)", "0,00°"],
        ["Sai khác độ lợi ±5% giữa các kênh, chưa hiệu chuẩn", "1,98°"],
        ["Sai khác độ lợi ±5%, đã hiệu chuẩn hệ số kênh", "0,00°"],
        ["Nhiễu đọc 2%", "1,29°"],
        ["Thành phần khuếch tán 15%", "1,09°"],
        ["Tổng hợp cả ba, đã hiệu chuẩn hệ số kênh", "1,65°"],
    ], "{B}. Sai số của phép suy góc cần quay từ ma trận 4 LDR (β_s = 30°)"),
    ("p", "Bảng trên chốt hai quyết định thiết kế: một là bắt buộc hiệu chuẩn hệ số độ lợi bốn kênh dưới nguồn sáng khuếch tán (khử trọn sai số do lệch kênh); hai là chọn góc gá β_s = 30° vì tan β_s = 0,577 đủ lớn để góc lệch 3° đã tạo e ≈ 0,030, lớn hơn nhiều mức nhiễu đọc, nhưng chưa gây bão hòa cảm biến trong dải lệch ±40°. Với vùng chết δ = 3°, sai số dư sau hiệu chuẩn khoảng 1,65° là chấp nhận được so với sai số cơ khí của khớp trục vít."),
    ("h2", "3.4. So sánh với phương pháp bám bước theo thời gian"),
    ("p", "Vòng kín cả ngày được mô phỏng cho hai luật điều khiển: luật cũ dịch chuyển một bước góc cố định mỗi lần sai lệch vượt ngưỡng (quay theo thời gian) và luật mới suy góc trực tiếp từ ma trận rồi quay tới góc đích có hồi tiếp biến trở. Cả hai cùng chịu nhiễu 1%, lệch độ lợi 3% và khuếch tán 10%:"),
    ("tbl", [
        ["Ngày", "Ma trận δ=3°: sai số TB / số lần chạy", "Bước theo thời gian: sai số TB / số lần chạy"],
        ["21/3", "1,14° / 46 lần", "2,95° / 111 lần"],
        ["21/6", "1,10° / 48 lần", "2,65° / 110 lần"],
        ["23/9", "1,13° / 46 lần", "2,94° / 111 lần"],
        ["21/12", "1,14° / 47 lần", "3,17° / 110 lần"],
    ], "{B}. So sánh luật suy góc từ ma trận và luật bám bước theo thời gian"),
    ("img", "hinh_ve/ket_qua_mo_phong_1_truc.png", "{H}. Góc bám và sai số trong ngày 21/6 của phương pháp ma trận LDR"),
    ("p", "Phương pháp ma trận giảm sai số bám trung bình từ 2,65–3,17° xuống còn 1,10–1,14°, đồng thời giảm số lần khởi động động cơ từ 110–111 lần xuống 46–48 lần mỗi ngày, tức giảm khoảng 58% số lần chạy và hao mòn cơ khí. Đồ thị cho thấy đường góc bám trùm gần sát đường góc lý tưởng và sai số chỉ nhô lên vào lúc sáng sớm khi tín hiệu còn yếu."),
    ("h2", "3.5. Phương pháp chốt cho hai mô hình"),
    ("b", "Mô hình một trục: dùng e_quay của ma trận bốn LDR suy ra Δ_quay = atan(e_quay/tan β_s); quay tấm pin tới góc đích θ + Δ_quay đọc từ biến trở hồi tiếp; vùng chết δ = 3°; β_s = 30°."),
    ("b", "Mô hình hai trục: dùng cả e_nghiêng và e_quay suy ra hai góc lệch; chỉnh trục nghiêng trước rồi tới trục phương vị, mỗi trục một biến trở hồi tiếp và một động cơ gạt nước trục vít."),
    ("b", "Cả hai mô hình không quay theo thời gian: động cơ chỉ chạy khi |Δ| > δ và tự dừng khi hồi tiếp báo tới góc đích; trục vít tự hãm giữ vị trí khi ngắt điện."),
    ("b", "Bắt buộc hiệu chuẩn hệ số độ lợi bốn kênh và lưu bảng hệ số trong chương trình; kiểm tra chất lượng tín hiệu (tổng sáng, bão hòa, biến động) trước khi phát lệnh."),
]
NGHIEN_CUU_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"
NGHIEN_CUU_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Chốt phương pháp điều khiển cho cả hai mô hình: đọc ma trận bốn LDR và suy ra góc cần quay bằng quan hệ Δ = atan(e/tan β_s), thay thế hoàn toàn cách quay bước theo thời gian."),
    ("b", "Xây dựng và chạy mô phỏng số (tools/mo_phong.py): thu được bảng hiệu suất trực xạ cố định/1 trục/2 trục, bảng sai số suy góc Monte Carlo 400 lần và bảng so sánh với luật bám bước (Chương 3)."),
    ("b", "Chốt tham số cảm biến và điều khiển từ số liệu mô phỏng: β_s = 30°, vùng chết δ = 3°, bắt buộc hiệu chuẩn hệ số kênh."),
    ("b", "Chốt linh kiện điều khiển và chấp hành: ESP32 là vi điều khiển duy nhất, động cơ gạt nước ô tô trục vít tự giữ vị trí khi ngắt điện, hồi tiếp góc bằng biến trở xoay."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Đối chiếu vectơ Mặt Trời của mô phỏng với thuật toán SPA/pvlib để xác nhận sai số hình học dưới 0,5°."),
    ("b", "Chế giá thử góc gá β_s và đo kiểm chứng đáp ứng cos(Δ ∓ β_s) của cụm LDR thực tế."),
    ("b", "Gửi quyển nghiên cứu xin góp ý của giảng viên hướng dẫn và chỉnh sửa theo nhận xét."),
]

# ---------- QUYEN CHE TAO ----------
CHE_TAO_H1_CH1 = "CHƯƠNG 1. PHƯƠNG ÁN THIẾT KẾ HỆ THỐNG ĐÃ CHỐT"
CHE_TAO_H1_CH2 = "CHƯƠNG 2. THIẾT KẾ CƠ KHÍ, MẠCH ĐIỆN VÀ DANH MỤC VẬT TƯ"
CHE_TAO_H1_CH3 = "CHƯƠNG 3. LẮP RÁP, HIỆU CHUẨN VÀ AN TOÀN"
CHE_TAO_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"

CHE_TAO_CH1 = [
    ("h2", "1.1. Phương pháp điều khiển chốt: ma trận LDR suy ra góc quay"),
    ("p", "Bốn LDR gắn ở bốn góc tấm pin, ký hiệu trên-trái (L_TT), trên-phải (L_PT), dưới-trái (L_TD), dưới-phải (L_PD), mỗi cảm biến gá chếch ra ngoài một góc β_s = 30° như nhau. Tổng và các sai lệch chuẩn hóa của ma trận được tính:"),
    ("eq", "S = L_TT + L_PT + L_TD + L_PD"),
    ("eq", "e_quay = [(L_PT + L_PD) − (L_TT + L_TD)] / S"),
    ("eq", "e_nghiêng = [(L_TT + L_PT) − (L_TD + L_PD)] / S"),
    ("p", "Vì đáp ứng mỗi kênh tỉ lệ với cos(Δ ∓ β_s) trong mặt phẳng tương ứng, sai lệch chuẩn hóa liên hệ trực tiếp với góc lệch Δ giữa hướng Mặt Trời và pháp tuyến tấm pin:"),
    ("eq", "Δ_quay = atan(e_quay / tan β_s);   Δ_nghiêng = atan(e_nghiêng / tan β_s)"),
    ("p", "Như vậy mỗi lần đọc ma trận cho ngay góc cần quay, không phải dò bước theo thời gian. Góc đích được tính từ hồi tiếp vị trí và giới hạn trong hành trình:"),
    ("eq", "θ_đích = sat(θ_hiện tại + Δ, θ_min, θ_max)"),
    ("p", "Động cơ chỉ chạy khi |Δ| > δ = 3° và dừng khi biến trở hồi tiếp báo θ đạt θ_đích; nhờ hộp giảm tốc trục vít tự hãm, tấm pin giữ nguyên vị trí khi dừng hoặc mất điện. Sai lệch chéo e_chéo = [(L_TT + L_PD) − (L_PT + L_TD)]/S chỉ dùng kiểm tra che bóng bất đối xứng, không tham gia phát lệnh."),
    ("h2", "1.2. Cấu trúc tổng thể hệ thống"),
    ("img", "hinh_ve/so_do_khoi_1_truc.png", "{H}. Sơ đồ khối hệ thống bám nắng một trục dùng ESP32"),
    ("tbl", [
        ["Khối", "Cấu hình chốt", "Nhiệm vụ"],
        ["Cảm biến hướng", "4 LDR gá β_s = 30° ở 4 góc", "Lập ma trận sáng, tạo e_quay."],
        ["Hồi tiếp vị trí", "Biến trở xoay 10 k đồng trục", "Báo góc hiện tại để dừng đúng góc đích."],
        ["Điều khiển", "ESP32 DevKit + RTC DS3231", "ADC 12 bit, lọc trung vị, suy góc, liên động, ghi log."],
        ["Đo kiểm", "ADS1115 (I²C, 16 bit)", "Đo U, I tấm pin phục vụ tính năng lượng."],
        ["Chấp hành", "Motor gạt nước 12 V trục vít + relay 2 kênh", "Quay trục Đông–Tây; tự giữ khi mất điện."],
        ["Bảo vệ", "2 công tắc hành trình + nút dừng khẩn cấp", "Chặn quá hành trình, cắt lệnh an toàn."],
    ], "{B}. Các khối chức năng của hệ thống một trục"),
    ("h2", "1.3. Bố trí cụm cảm biến và góc gá β_s"),
    ("img", "hinh_ve/bo_tri_4_ldr.png", "{H}. Bố trí 4 LDR ở bốn góc tấm pin và mặt cắt góc gá β_s"),
    ("tbl", [
        ["Vị trí", "Ký hiệu", "Hướng gá"],
        ["Trên – trái", "L_TT", "Chếch ra ngoài về phía trên-trái."],
        ["Trên – phải", "L_PT", "Chếch ra ngoài về phía trên-phải."],
        ["Dưới – trái", "L_TD", "Chếch ra ngoài về phía dưới-trái."],
        ["Dưới – phải", "L_PD", "Chếch ra ngoài về phía dưới-phải."],
    ], "{B}. Ký hiệu và hướng gá của bốn cảm biến"),
    ("p", "Góc gá β_s = 30° được chốt từ kết quả mô phỏng tuần 5/10–10/10: đủ độ nhạy (Δ = 3° đã cho e ≈ 0,030) mà chưa bão hòa trong dải lệch ±40°. Giá gá bốn cảm biến phải cùng một mẫu, cùng góc, không bị khung hoặc dây che; sau hiệu chuẩn phải cố định chắc và ghi lại góc thực tế."),
    ("h2", "1.4. Cơ cấu chấp hành và hồi tiếp vị trí"),
    ("p", "Trục quay căn hướng Bắc – Nam thật, đặt gần trọng tâm tấm pin. Động cơ gạt nước ô tô 12 V gắn qua tay đòn; cặp trục vít – bánh vít tự hãm nên cơ cấu không trôi khi ngắt điện, không cần nuôi điện giữ vị trí. Biến trở xoay 10 k gắn đồng trục với trục quay, chia áp về một kênh ADC1 để chương trình đọc góc hiện tại; hai công tắc hành trình đặt trước điểm va chạm cơ khí ở hai đầu Đông – Tây."),
]

CHE_TAO_CH2 = [
    ("h2", "2.1. Kết cấu cơ khí"),
    ("img", "hinh_ve/mo_hinh_co_khi_1_truc.png", "{H}. Mặt cắt mô hình cơ khí một trục với động cơ gạt nước trục vít"),
    ("p", "Khung đế phẳng có bulông cân bằng; hai gối đỡ mang trục thép tròn có bạc lót; tấm pin bắt lên khung đỡ qua tai bắt vít sao cho tâm khối lượng sát trục. Tay đòn nối trục vít của động cơ với khung pin có khớp bản lề để khử sai lệch quỹ đạo; dây dẫn chừa dư theo toàn hành trình. Hai công tắc hành trình gắn ở giá sao cho cần gạt chạm trước khi khung pin va gối đỡ."),
    ("h2", "2.2. Kết quả tính chọn động cơ"),
    ("tbl", [
        ["Hạng mục", "Giá trị tính toán", "Ghi chú"],
        ["Khối lượng tấm pin 10 W", "≈ 0,9 kg", "Lắp cân bằng quanh trục nên mô-men tĩnh ≈ 0."],
        ["Tải gió v = 10 m/s", "q = 0,6·v² ≈ 60 Pa; F ≈ 3,6 N với S = 0,06 m²", "Tác dụng lên mặt pin."],
        ["Mô-men gió lớn nhất", "M ≈ F × 0,15 m ≈ 0,54 N·m", "Cánh tay đòn tới trục."],
        ["Mô-men yêu cầu (×3 khởi động/ma sát)", "≈ 1,6 N·m", "Hệ số dự trữ cho khớp trục vít."],
        ["Motor gạt nước 12 V điển hình", "8 – 12 N·m, dòng 3 – 6 A", "Kèm trục vít tự hãm và công tắc tự đỗ."],
        ["Hệ số an toàn đạt được", "5 – 7 lần", "Đủ cho thử ngoài trời có gió giật nhẹ."],
    ], "{B}. Tính chọn động cơ gạt nước cho trục quay một trục"),
    ("p", "Với hệ số an toàn 5–7 lần, động cơ gạt nước đủ mô-men kể cả khi khớp trục vít có hiệu suất thấp; đổi lại tốc độ quay chậm (khoảng 1–2 vòng/phút ở trục ra) lại phù hợp với bám nắng vì mỗi lần hiệu chỉnh chỉ quay vài độ."),
    ("h2", "2.3. Mạch điện và phương pháp đọc ADC"),
    ("p", "Mạch chia áp của bốn LDR và của biến trở hồi tiếp do sinh viên tự chế và tự hiệu chuẩn; báo cáo chốt phần xử lý tín hiệu phía ESP32: dùng ADC1 12 bit với suy hao 11 dB, mỗi kênh lấy 64 mẫu, loại đột biến bằng trung vị rồi lấy trung bình nửa giữa; giá trị được đổi sang milivôn theo hệ số hiệu chuẩn của bo. Module ADS1115 16 bit qua I²C đo điện áp tấm pin (qua cầu chia) và dòng điện (qua cảm biến ACS712) phục vụ tính năng lượng. Động cơ đóng cắt bằng module relay 2 kênh (hoặc cầu H MOSFET) có cầu chì 10 A riêng; nguồn động cơ 12 V tách khỏi nguồn logic 5 V, nối mass chung một điểm."),
    ("img", "hinh_ve/so_do_ket_noi_1_truc.png", "{H}. Sơ đồ kết nối ESP32 của mô hình một trục"),
    ("tbl", [
        ["Chân ESP32", "Tín hiệu", "Thiết bị / ghi chú"],
        ["GPIO36, 39, 34, 35 (ADC1)", "4 kênh analog", "Ma trận LDR: L_TT, L_PT, L_TD, L_PD."],
        ["GPIO32 (ADC1_CH4)", "1 kênh analog", "Biến trở hồi tiếp góc trục quay."],
        ["GPIO21 / GPIO22", "I²C", "ADS1115 đo U–I và RTC DS3231 chung bus."],
        ["GPIO26, GPIO27", "2 ngõ ra", "Hai kênh relay đảo chiều motor gạt nước."],
        ["GPIO4, GPIO5", "Ngõ vào pull-up", "Công tắc hành trình đầu Đông và đầu Tây."],
        ["GPIO18", "Ngõ vào pull-up", "Nút dừng khẩn cấp."],
        ["USB-UART", "Serial 115200", "Serial Monitor và ghi log thử nghiệm."],
    ], "{B}. Bảng chân kết nối chốt cho mô hình một trục"),
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
        ["8", "Động cơ chấp hành", "Motor gạt nước ô tô 12 V trục vít", "1"],
        ["9", "Đóng cắt động cơ", "Module relay 2 kênh 10 A hoặc cầu H MOSFET", "1"],
        ["10", "Công tắc hành trình", "Cần gạt, tiếp điểm NC", "2"],
        ["11", "Nút dừng khẩn cấp", "Nút nhấn khóa", "1"],
        ["12", "Nguồn", "Ắc quy/nguồn 12 V 10 A + mạch hạ 5 V", "1 bộ"],
        ["13", "Vật liệu cơ khí", "Thép tròn trục, gối đỡ, nhôm hộp, ốc vít", "1 bộ"],
        ["14", "Phụ trợ", "Cầu chì 10 A, dây dẫn, hộp chống ẩm", "1 bộ"],
    ], "{B}. Danh mục vật tư – linh kiện đã chốt"),
]

CHE_TAO_CH3 = [
    ("h2", "3.1. Quy trình lắp ráp"),
    ("b", "Bước 1. Thử riêng động cơ gạt nước trên bàn: cấp 12 V qua relay, kiểm tra chiều quay, dòng không tải và chức năng tự đỗ."),
    ("b", "Bước 2. Gia công đế, gối đỡ và trục; căn hướng Bắc – Nam bằng la bàn; kiểm tra quay trơn toàn hành trình bằng tay."),
    ("b", "Bước 3. Lắp tay đòn khớp nối động cơ – khung pin; đánh dấu mốc zero cơ khí."),
    ("b", "Bước 4. Lắp biến trở hồi tiếp đồng trục; đo điện áp ra tại hai đầu hành trình để lập bảng quy đổi góc."),
    ("b", "Bước 5. Lắp công tắc hành trình và nút dừng khẩn cấp; đo thông mạch từng tiếp điểm."),
    ("b", "Bước 6. Chế và thử mạch chia áp bốn LDR cùng mạch biến trở; kiểm tra ngắn mạch trước khi cấp nguồn."),
    ("b", "Bước 7. Gá cụm LDR đúng ký hiệu và β_s = 30°; chụp ảnh ghi nhận bố trí."),
    ("b", "Bước 8. Đấu nối theo bảng chân; tách khối nguồn động cơ và nguồn logic; cố định dây theo hành trình."),
    ("b", "Bước 9. Cấp điện chạy không tải: quét chậm hai đầu, xác nhận liên động chặn đúng chiều và thoát ngược được."),
    ("b", "Bước 10. Lắp tấm pin, siết ốc đối xứng, kiểm tra tự giữ vị trí khi ngắt điện rồi mới thử ngoài trời."),
    ("h2", "3.2. Hiệu chuẩn bắt buộc trước khi chạy thuật toán"),
    ("b", "Hiệu chuẩn hệ số độ lợi bốn kênh LDR dưới nguồn sáng khuếch tán: chỉnh để bốn kênh cùng một giá trị khi chiếu đều; lưu bảng hệ số vào chương trình (mô phỏng cho thấy bước này khử trọn sai số 1,98° do lệch kênh)."),
    ("b", "Kiểm tra chiều dấu e_quay: chiếu mạnh phía phải thì e_quay phải dương theo quy ước lệnh; nếu ngược thì đảo hệ số trong bảng hiệu chuẩn, không sửa rải rác trong code."),
    ("b", "Hiệu chuẩn biến trở hồi tiếp: quay trục tới hai đầu hành trình và vị trí giữa, ghi ba điểm để nội suy tuyến tính góc."),
    ("b", "Xác nhận vùng chết δ = 3°: che mờ đều cụm cảm biến, bảo đảm lệnh không phát khi |Δ| tính ra dưới ngưỡng."),
    ("h2", "3.3. An toàn"),
    ("b", "Cầu chì 10 A ngay đầu nguồn 12 V; không chạm cụm trục khi đang cấp điện."),
    ("b", "Kiểm tra chức năng tự giữ của trục vít trước khi lắp pin: ngắt điện đột ngột khi trục đang nghiêng, trục không được trôi."),
    ("b", "Ngoài trời phải có hộp chống ẩm; ngắt nguồn và đặt tấm pin về vị trí nghỉ khi gió mạnh."),
]

CHE_TAO_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Chốt cơ cấu chấp hành là động cơ gạt nước ô tô trục vít; tính toán mô-men tải gió và hệ số an toàn 5–7 lần (Bảng chương 2)."),
    ("b", "Chốt sơ đồ khối, sơ đồ kết nối ESP32 và bảng chân cho mô hình một trục; chốt danh mục vật tư 14 hạng mục."),
    ("b", "Chốt phương án hồi tiếp vị trí bằng biến trở xoay đồng trục để dừng đúng góc đích, thay cho việc canh thời gian chạy motor."),
    ("b", "Lập quy trình lắp ráp 10 bước và danh mục hiệu chuẩn bắt buộc, kèm phép thử tự giữ vị trí khi ngắt điện."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Mua động cơ gạt nước, relay 2 kênh, biến trở xoay và ADS1115 theo danh mục."),
    ("b", "Gia công khung, gối đỡ và trục; thử bench động cơ kèm relay trước khi lắp tải."),
    ("b", "Chế mạch chia áp bốn LDR và đo đặc tuyến từng kênh dưới đèn kiểm soát."),
    ("b", "Lắp biến trở hồi tiếp và lập bảng quy đổi góc ba điểm."),
]

# ---------- QUYEN LAP TRINH ----------
LAP_TRINH_H1_CH1 = "CHƯƠNG 1. MÔI TRƯỜNG LẬP TRÌNH ARDUINO IDE VÀ CÁCH NẠP CHO ESP32"
LAP_TRINH_H1_CH2 = "CHƯƠNG 2. CÁC NHÓM LỆNH CƠ BẢN DÙNG TRONG CHƯƠNG TRÌNH"
LAP_TRINH_H1_CH3 = "CHƯƠNG 3. PHƯƠNG PHÁP ĐỌC MA TRẬN LDR, SUY GÓC VÀ CODE MẪU"
LAP_TRINH_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"

LAP_TRINH_CH1 = [
    ("h2", "1.1. Arduino IDE là gì"),
    ("p", "Arduino IDE là môi trường phát triển tích hợp miễn phí của Arduino.cc: soạn thảo sketch (tệp .ino), biên dịch, nạp firmware và quan sát dữ liệu qua Serial Monitor/Serial Plotter. Ngôn ngữ lập trình là C/C++ kèm hệ thống hàm và thư viện quản lý sẵn. Giao diện gồm thanh công cụ Verify/Upload/Serial Monitor, cửa sổ soạn thảo, khung chọn Board và Port, cửa sổ console báo lỗi và dung lượng bộ nhớ."),
    ("h2", "1.2. Vì sao không thể lập trình ESP32 trực tiếp trên Arduino IDE vừa cài"),
    ("b", "Arduino IDE phân phối sẵn chỉ kèm các lõi (core) phần cứng AVR (ATmega328, ATmega2560) và SAM; trình biên dịch đi kèm cũng chỉ là avr-gcc/arm-gcc cho các lõi đó."),
    ("b", "ESP32 dùng nhân Xtensa LX6 32 bit hoàn toàn khác kiến trúc AVR 8 bit: tập lệnh khác, bản đồ bộ nhớ khác, trình biên dịch phải là xtensa-esp32-elf-gcc, lại cần SDK thành phần (driver ADC, LEDC, WiFi, bootloader nạp qua UART ở chế độ ROM)."),
    ("b", "Vì vậy nếu chọn board ESP32 khi chưa cài lõi, IDE sẽ báo lỗi không nhận diện board/không tìm thấy công cụ biên dịch; các hàm đặc thù như analogSetPinAttenuation hay ledcWrite cũng không tồn tại trong lõi AVR."),
    ("b", "Giải pháp là cài thêm lõi esp32 của Espressif vào chính Arduino IDE qua Boards Manager: IDE tải về trình biên dịch Xtensa và SDK, sau đó sketch viết bằng ngữ pháp Arduino quen thuộc sẽ được biên dịch cho ESP32 mà không đổi thói quen lập trình."),
    ("h2", "1.3. Hướng dẫn cài bo ESP32 vào Arduino IDE"),
    ("b", "Bước 1. Cài Arduino IDE 1.8.x hoặc 2.x; cài driver USB-UART (CP210x/CH340) nếu máy chưa nhận cổng."),
    ("b", "Bước 2. File → Preferences → Additional Boards Manager URLs: thêm https://espressif.github.io/arduino-esp32/package_esp32_index.json (có thể ngăn cách nhiều URL bằng dấu phẩy)."),
    ("b", "Bước 3. Tools → Board → Boards Manager → tìm “esp32” của Espressif Systems → Install (IDE tự tải toolchain Xtensa)."),
    ("b", "Bước 4. Tools → Board → esp32 → “ESP32 Dev Module”; Tools → Port chọn đúng cổng COM; giữ nguyên Flash Frequency 80 MHz, Upload Speed 921600 mặc định."),
    ("b", "Bước 5. Mở Serial Monitor đặt 115200 baud; khi nạp nếu IDE dừng ở “Connecting...” thì giữ nút BOOT trên mạch vài giây."),
    ("b", "Bước 6. Nạp sketch Blink mẫu để xác nhận chuỗi biên dịch – nạp hoạt động trước khi viết chương trình ma trận LDR."),
    ("h2", "1.4. Cấu trúc sketch và thư viện dùng trong đề tài"),
    ("p", "Sketch gồm phần khai báo toàn cục (hằng số chân, ngưỡng, bảng hệ số hiệu chuẩn), hàm setup() chạy một lần (cấu hình ADC, relay, I²C, Serial) và hàm loop() lặp vô hạn thực hiện chu kỳ đọc ma trận – suy góc – phát lệnh – ghi log. Thư viện dùng: Wire.h (I²C cho ADS1115 và DS3231), các hàm ADC/LEDC nội tại của lõi esp32; không cần thư viện Servo vì chấp hành là motor gạt nước đóng cắt bằng relay."),
]

LAP_TRINH_CH2 = [
    ("h2", "2.1. Nhóm cấu trúc và điều khiển luồng"),
    ("tbl", [
        ["Lệnh / cấu trúc", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["setup() / loop()", "void setup() { } void loop() { }", "Khởi tạo một lần và vòng lặp đọc ma trận – suy góc – quay pin."],
        ["if / else if / else", "if (fabs(dQuay) > DEAD) { ... }", "Quyết định phát lệnh quay hay giữ vị trí."],
        ["switch – case", "switch (trangThai) { case CHAY_DONG: ... }", "Máy trạng thái motor: DỪNG – QUAY ĐÔNG – QUAY TÂY."],
        ["for", "for (int i = 0; i < 64; i++) { ... }", "Lấy 64 mẫu ADC mỗi kênh để lọc trung vị."],
        ["while", "while (fabs(gocHienTai - gocDich) > 0.5) { ... }", "Vòng chờ motor tới góc đích, vẫn giám sát công tắc hành trình."],
        ["break / continue / return", "break;", "Thoát vòng lấy mẫu, bỏ mẫu lỗi, hàm trả về góc lệch."],
    ], "{B}. Nhóm lệnh cấu trúc và điều khiển luồng"),
    ("h2", "2.2. Nhóm vào/ra số và tương tự trên ESP32"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["pinMode", "pinMode(MOT_A, OUTPUT);", "Cấu hình chân relay, nút dừng, đèn báo."],
        ["digitalWrite / digitalRead", "digitalWrite(MOT_A, HIGH);", "Đóng cắt hai kênh relay đảo chiều motor; đọc công tắc hành trình."],
        ["analogRead", "analogRead(36);", "Đọc kênh LDR và biến trở hồi tiếp (ADC1)."],
        ["analogSetPinAttenuation", "analogSetPinAttenuation(36, ADC_11db);", "Đặt suy hao 11 dB để dải đo phủ 0 – 2,45 V không bão hòa."],
        ["analogReadResolution", "analogReadResolution(12);", "Đặt độ phân giải 12 bit (4096 mức)."],
    ], "{B}. Nhóm lệnh vào/ra dùng cho ma trận LDR và relay"),
    ("h2", "2.3. Nhóm thời gian, toán học và truyền thông"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng trong đề tài"],
        ["millis()", "if (millis() - tPrev >= T_MAU)", "Định chu kỳ đọc ma trận không chặn vòng lặp."],
        ["atan / tan", "atan(e / tan(BETA_S));", "Công thức lõi suy góc cần quay từ sai lệch chuẩn hóa."],
        ["constrain / fabs", "constrain(th, TH_MIN, TH_MAX);", "Hàm sat() giới hạn góc đích trong hành trình."],
        ["sort (mảng mẫu)", "sort(mau, mau + 64);", "Lấy trung vị 64 mẫu loại đột biến."],
        ["Serial.begin / printf", "Serial.printf(...)", "In bảng 4 kênh, e, Δ, góc đích để ghi log và gỡ lỗi."],
        ["Wire.requestFrom", "Wire.requestFrom(0x48, 2);", "Đọc thanh ghi chuyển đổi của ADS1115."],
    ], "{B}. Nhóm lệnh thời gian, toán học và truyền thông"),
]

CODE_1TRUC = """// Doc ma tran 4 LDR va suy ra goc quay - mo hinh 1 truc (ESP32)
// Phuong phap: e_quay = (phai - trai)/S  ->  dQuay = atan(e_quay / tan(beta_s))
// Khong quay theo thoi gian: motor chi chay toi goc dich doc tu bien tro.
#include <Arduino.h>
#include <Wire.h>

const int PIN_LDR[4] = {36, 39, 34, 35};   // L_TT, L_PT, L_TD, L_PD (ADC1)
const int PIN_POT = 32;                    // bien tro hoi tiep goc truc
const int MOT_A = 26, MOT_B = 27;          // 2 kenh relay cua motor gat nuoc
const int LS_DONG = 4, LS_TAY = 5, NUT_DUNG = 18;

const float BETA_S = 0.5236;               // beta_s = 30 do (rad)
const float DEAD   = 0.0524;               // vung chet delta = 3 do (rad)
const float TH_MIN = -1.0472, TH_MAX = 1.0472;   // +/- 60 do
const float GOC_MIN_POT = 0.30, GOC_MAX_POT = 3.00;  // V bien tro tai 2 dau
const int N_MAU = 64;
const unsigned long T_MAU = 2000;          // chu ky doc ma tran (ms)
float K_cal[4] = {1.0, 1.0, 1.0, 1.0};     // he so hieu chuan do loi 4 kenh
unsigned long tPrev = 0;

// doc 1 kenh: 64 mau, trung vi roi trung binh nua giua
float docKenh(int chan) {
  int mau[N_MAU];
  for (int i = 0; i < N_MAU; i++) { mau[i] = analogRead(chan); delayMicroseconds(40); }
  for (int i = 0; i < N_MAU - 1; i++)
    for (int j = i + 1; j < N_MAU; j++)
      if (mau[j] < mau[i]) { int t = mau[i]; mau[i] = mau[j]; mau[j] = t; }
  float s = 0; for (int i = 16; i < 48; i++) s += mau[i];
  return s / 32.0;
}

float docGocTruc() {   // quy doi V bien tro thanh rad (tuyen tinh 3 diem)
  float v = docKenh(PIN_POT) * 3.3 / 4095.0;
  return TH_MIN + (v - GOC_MIN_POT) * (TH_MAX - TH_MIN) / (GOC_MAX_POT - GOC_MIN_POT);
}

void dungMotor()  { digitalWrite(MOT_A, LOW);  digitalWrite(MOT_B, LOW); }
void quayMotChieu(bool sangDong) {
  digitalWrite(MOT_A, sangDong ? HIGH : LOW);
  digitalWrite(MOT_B, sangDong ? LOW : HIGH);
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  for (int i = 0; i < 4; i++) analogSetPinAttenuation(PIN_LDR[i], ADC_11db);
  analogSetPinAttenuation(PIN_POT, ADC_11db);
  pinMode(MOT_A, OUTPUT); pinMode(MOT_B, OUTPUT); dungMotor();
  pinMode(LS_DONG, INPUT_PULLUP); pinMode(LS_TAY, INPUT_PULLUP);
  pinMode(NUT_DUNG, INPUT_PULLUP);
}

void loop() {
  if (millis() - tPrev < T_MAU) return;
  tPrev = millis();
  // 1) doc ma tran 4 LDR da hieu chuan
  float L[4]; for (int i = 0; i < 4; i++) L[i] = docKenh(PIN_LDR[i]) * K_cal[i];
  float S = L[0] + L[1] + L[2] + L[3];
  if (S < 400 || S > 15000) { dungMotor();          // troi qua toi / bao hoa
    Serial.printf("S ngoai dai: %.0f\\n", S); return; }
  // 2) sai lech chuan hoa va goc can quay
  float eQuay = ((L[1] + L[3]) - (L[0] + L[2])) / S;
  float dQuay = atan(eQuay / tan(BETA_S));
  // 3) so sanh voi vung chet roi quay toi goc dich
  if (fabs(dQuay) > DEAD) {
    float thHienTai = docGocTruc();
    float thDich = constrain(thHienTai + dQuay, TH_MIN, TH_MAX);
    bool sangDong = (dQuay < 0);
    if ((sangDong && digitalRead(LS_DONG) == LOW) ||
        (!sangDong && digitalRead(LS_TAY) == LOW) ||
        digitalRead(NUT_DUNG) == LOW) {
      dungMotor(); Serial.println("chanh lien dong"); return;
    }
    quayMotChieu(sangDong);
    while (fabs(docGocTruc() - thDich) > 0.0087) {   // 0.5 do
      if (digitalRead(LS_DONG) == LOW || digitalRead(LS_TAY) == LOW ||
          digitalRead(NUT_DUNG) == LOW) break;
      delay(10);
    }
    dungMotor();   // truc vit tu giu vi tri khi ngat lenh
  }
  // 4) ghi log day du de kiem tra lai
  Serial.printf("L=%.0f %.0f %.0f %.0f S=%.0f e=%+.3f dQuay=%+6.2f do\\n",
                L[0], L[1], L[2], L[3], S, eQuay, degrees(dQuay));
}"""

LAP_TRINH_CH3 = [
    ("h2", "3.1. Vì sao ma trận bốn LDR suy ra được góc cần quay"),
    ("p", "Trong mặt phẳng quay, trục cảm quang của cảm biến phía phải lệch +β_s và phía trái lệch −β_s so với pháp tuyến tấm pin, nên khi hướng Mặt Trời lệch khỏi pháp tuyến một góc Δ, đáp ứng hai kênh tỉ lệ với cos(Δ − β_s) và cos(Δ + β_s). Lập tỉ số sai lệch:"),
    ("eq", "e = (L_phải − L_trái)/(L_phải + L_trái) = [cos(Δ−β_s) − cos(Δ+β_s)] / [cos(Δ−β_s) + cos(Δ+β_s)] = tan Δ · tan β_s"),
    ("p", "Đảo lại ta được góc lệch cần bù ngay trong một lần đọc, không phải thử sai từng bước:"),
    ("eq", "Δ_quay = atan(e_quay / tan β_s)"),
    ("p", "Cặp kênh trên–dưới cho công thức tương tự với trục nghiêng. Mô phỏng Monte Carlo 400 lần (quyển nghiên cứu, Chương 3) cho thấy sau hiệu chuẩn hệ số kênh, sai số của phép suy góc còn 1,65° ở điều kiện nhiễu 2% và khuếch tán 15%."),
    ("h2", "3.2. Phương pháp đọc ADC trên ESP32 và ví dụ so sánh giá trị"),
    ("b", "Dùng ADC1 (chân 36, 39, 34, 35) vì nhóm ADC2 bị tranh chấp khi bật WiFi; đặt analogReadResolution(12) và analogSetPinAttenuation(…, ADC_11db) để dải tuyến tính phủ khoảng 0,15 – 2,45 V."),
    ("b", "Mỗi kênh lấy 64 mẫu cách nhau 40 µs, sắp xếp lấy trung vị rồi trung bình 32 giá trị giữa: loại được xung nhiễu do relay và động cơ đóng cắt."),
    ("b", "Nhân hệ số hiệu chuẩn K_cal[i] đo dưới nguồn sáng khuếch tán để bốn kênh cùng thang trước khi lập ma trận."),
    ("p", "Ví dụ so sánh giá trị lúc 10h nắng rõ (đơn vị mức ADC): L_TT = 2280, L_PT = 1490, L_TD = 2200, L_PD = 1560. Tổng S = 7530; e_quay = [(1490+1560) − (2280+2200)]/7530 = −0,190; suy ra Δ_quay = atan(−0,190/0,577) = −18,2°: mặt pin đang thừa 18,2° về phía Tây nên lệnh quay là 18,2° về phía Đông, đọc từ biến trở rồi dừng đúng góc đích — toàn bộ suy ra từ một lần đọc ma trận."),
    ("h2", "3.3. Phương pháp quay tấm pin"),
    ("b", "Đọc biến trở hồi tiếp để biết góc hiện tại θ; tính θ_đích = sat(θ + Δ_quay, θ_min, θ_max)."),
    ("b", "Nếu |Δ_quay| ≤ δ = 3° thì không phát lệnh (vùng chết); nếu lớn hơn thì đóng relay chiều tương ứng."),
    ("b", "Trong khi motor chạy, vòng while đọc biến trở mỗi 10 ms và dừng khi |θ − θ_đích| ≤ 0,5°; công tắc hành trình và nút dừng khẩn cấp có quyền phá vòng bất cứ lúc nào."),
    ("b", "Ngắt cả hai kênh relay khi tới đích: hộp trục vít tự hãm giữ tấm pin đứng yên không tốn điện."),
    ("img", "hinh_ve/so_do_khoi_chuong_trinh.png", "{H}. Sơ đồ khối chương trình đọc ma trận LDR và suy ra góc quay"),
    ("img", "hinh_ve/luu_do_ma_tran_1_truc.png", "{H}. Lưu đồ thuật toán ma trận LDR cho mô hình một trục"),
    ("h2", "3.4. Code mẫu đọc ma trận và quay pin (ESP32, Arduino IDE)"),
    ("code", CODE_1TRUC),
    ("p", "Đoạn code trên thực hiện đúng chuỗi: đọc 64 mẫu/kênh → trung vị → nhân hệ số hiệu chuẩn → lập S và e_quay → suy Δ_quay bằng atan → so vùng chết → đọc biến trở → chạy relay tới góc đích → ngắt relay và ghi log. Muốn chuyển sang mô hình hai trục chỉ cần thêm kênh biến trở thứ hai, cặp relay thứ hai và lặp lại khối suy góc với e_nghiêng trước khi xử lý e_quay."),
    ("h2", "3.5. Kết quả kiểm thử chương trình bằng số liệu mô phỏng"),
    ("tbl", [
        ["Phép thử", "Kết quả"],
        ["Suy góc với tín hiệu lý tưởng", "Sai số 0,00° (khớp công thức đóng)."],
        ["Suy góc khi lệch độ lợi ±5%, đã hiệu chuẩn K_cal", "Sai số 0,00°; chưa hiệu chuẩn: 1,98°."],
        ["Vòng kín cả ngày, δ = 3°", "Sai số trung bình 1,10 – 1,14°; 46 – 48 lần chạy motor."],
        ["Vòng kín cả ngày, luật cũ bám bước theo thời gian", "Sai số 2,65 – 3,17°; 110 – 111 lần chạy motor."],
        ["Kiểm tra liên động trong code", "Lệnh bị hủy đúng chiều khi công tắc tác động; motor dừng ngay."],
    ], "{B}. Kết quả kiểm thử logic chương trình trên dữ liệu mô phỏng"),
    ("img", "hinh_ve/ket_qua_mo_phong_1_truc.png", "{H}. Góc bám và sai số ngày 21/6 của chương trình phương pháp ma trận"),
]

LAP_TRINH_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Viết xong và mô phỏng kiểm chứng code mẫu đọc ma trận 4 LDR, suy góc bằng atan và quay tới góc đích có hồi tiếp biến trở (mục 3.4)."),
    ("b", "Trình bày rõ vì sao Arduino IDE không nạp được ESP32 khi chưa cài lõi Espressif và hướng dẫn cài bo ESP32 từng bước (Chương 1)."),
    ("b", "Hệ thống hóa các nhóm lệnh thực dùng trên ESP32 cho đề tài: ADC1 + attenuation, trung vị 64 mẫu, relay, millis, atan, constrain (Chương 2)."),
    ("b", "Lập lưu đồ và sơ đồ khối chương trình theo phương pháp suy góc, bỏ hoàn toàn nhánh quay theo thời gian (mục 3.3)."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Nạp code mẫu lên ESP32 thật, in bảng 4 kênh và e_quay ra Serial Monitor đối chiếu với ví dụ số ở mục 3.2."),
    ("b", "Đo hiệu chuẩn K_cal bốn kênh dưới nguồn sáng khuếch tán và lưu vào K_cal trong code."),
    ("b", "Hiệu chuẩn biến trở hồi tiếp ba điểm; kiểm tra vòng while dừng motor đúng 0,5°."),
    ("b", "Mở rộng code sang phiên bản hai trục (thêm e_nghiêng, biến trở và cặp relay thứ hai)."),
]
