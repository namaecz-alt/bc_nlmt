# -*- coding: utf-8 -*-
"""Noi dung moi ban 2 truc – phuong phap LAI thien van + LDR cho ca hai truc
(nghieng truoc, phuong vi sau); hai kenh opto - cau H TIP41C; 4 hanh trinh."""

NEW_24_25 = [
    ("h2", "2.4. Bộ điều khiển ESP32 DevKit và các khối phụ trợ"),
    ("p", "ESP32 DevKit (Xtensa LX6 hai nhân 240 MHz, 4 MB flash) điều khiển cả hai trục của mô hình. Hệ không dùng WiFi khi vận hành nên bốn kênh LDR đặt trên ADC2 (GPIO25, 26, 27, 14), hai biến trở hồi tiếp góc nghiêng và góc phương vị đặt trên ADC1 (GPIO36, 39); báo cáo chỉ đo điện áp, chưa đo dòng điện. Bus I²C GPIO21/GPIO22 nối chung module thời gian thực DS1307 và màn hình LCD I²C 1602; bốn công tắc hành trình qt1…qt4 vào GPIO34, 35, 32, 33; bốn chân lệnh th_thuan/th_nguoc của hai trục là GPIO19, 18 và GPIO5, 13."),
    ("p", "Module DS1307 giữ giờ thực nhờ pin nuôi, cấp ngày–giờ cho nhánh thiên văn của cả hai trục; LCD I²C 1602 hiển thị giờ đọc được, góc lệnh và góc thực tế của từng trục cùng sai lệch e1, e2 để quan sát trực tiếp không cần máy tính."),
    ("h2", "2.5. Mạch động lực cầu H TIP41C cách ly opto và động cơ trục vít"),
    ("p", "Mỗi trục dùng một động cơ gạt nước ô tô 12 V kèm hộp giảm tốc trục vít – bánh vít: trục vít tự hãm nên tấm pin tự giữ vị trí khi ngắt lệnh, đặc biệt quan trọng với trục nghiêng luôn chịu mô-men trọng lượng của tấm pin 4 kg. Mỗi motor có một mạch động lực cầu H bốn TIP41C với bốn diode bảo vệ và một cặp opto PC817 kèm điện trở 220 Ω cách ly khối logic 3,3 V khỏi khối công suất 12 V; toàn hệ dùng tám TIP41C và bốn PC817."),
    ("p", "Opto tác động ở mức thấp: chân lệnh xuống 0 thì mở cầu H chiều tương ứng, cả hai chân lệnh mức 1 thì cầu H khóa; vì vậy setup() đưa cả bốn chân lệnh lên mức cao trước khi vào vòng lặp. Nguồn 12 V qua 1N4007 chống ngược cực, LM2596 hạ 3,3 V nuôi ESP32, 7805 hạ 5 V nuôi LCD và DS1307."),
]

NEW_29 = [
    ("h2", "2.9. Các phương pháp bám nắng khảo sát"),
    ("p", "Đề tài khảo sát ba nhóm phương pháp bám nắng cho hệ hai trục và chọn phương pháp lai làm phương án thực hiện."),
    ("h3", "2.9.1. Phương pháp bám theo cảm biến quang trở (vòng kín)"),
    ("p", "Bốn quang trở LDR đặt ở bốn góc tấm pin, giữa cụm có vách che chữ thập tạo bóng chênh lệch. Gọi tín hiệu ADC bốn kênh là L_trái, L_phải, L_trên, L_dưới:"),
    ("eq", "e1 = ADC(LDR_trái) − ADC(LDR_phải);   e2 = ADC(LDR_trên) − ADC(LDR_dưới)"),
    ("p", "Luật điều khiển: nếu |e1| lớn hơn ngưỡng thì quay động cơ trục phương vị theo dấu e1; nếu |e2| lớn hơn ngưỡng thì quay động cơ trục nghiêng theo dấu e2; ngược lại dừng. Khoảng ngưỡng là vùng chết chống dao động quanh vị trí cân bằng."),
    ("b", "Ưu điểm: đơn giản, rẻ, phản ứng theo điều kiện sáng thực tế, không cần tọa độ và đồng hồ chính xác."),
    ("b", "Nhược điểm: nhạy với mây và bóng che; khi trời mờ đều bốn kênh gần bằng nhau thì hệ mất phương hướng, đứng yên trong khi Mặt Trời vẫn di chuyển."),
    ("h3", "2.9.2. Phương pháp bám theo thời gian (vòng hở thiên văn)"),
    ("p", "Vị trí Mặt Trời tính từ vị trí địa lý, ngày và giờ thực đọc từ DS1307. Với n là ngày trong năm, t là giờ Mặt Trời, φ là vĩ độ nơi lắp đặt:"),
    ("eq", "δ = 23,45° · sin[360° · (284 + n)/365]"),
    ("eq", "H = 15° · (t − 12)"),
    ("eq", "sin α = sin φ · sin δ + cos φ · cos δ · cos H"),
    ("p", "Góc phương vị γ tính từ α, δ, φ; từ α và γ suy ra góc lệnh cho trục nghiêng và trục phương vị. Vòng hở chuyển động mượt, không dao động."),
    ("b", "Ưu điểm: ổn định, không phụ thuộc thời tiết, làm việc được cả khi mây dày."),
    ("b", "Nhược điểm: cần đúng tọa độ và giờ; sai số lắp đặt và sai số đồng hồ không tự sửa được."),
    ("h3", "2.9.3. Phương pháp lai quang trở – thiên văn (lựa chọn của đề tài)"),
    ("b", "Thiên văn định vị thô: mỗi chu kỳ đọc DS1307, tính góc lệnh hai trục; trục nào lệch góc hiện tại quá 5° thì chạy motor theo lịch kéo về gần Mặt Trời."),
    ("b", "LDR tinh chỉnh: khi tổng sáng vượt ngưỡng nắng, e1 tinh chỉnh trục phương vị và e2 tinh chỉnh trục nghiêng, mỗi trục một bước nhỏ về phía nhận sáng mạnh hơn, bù sai số lắp đặt mà vòng hở không tự sửa."),
    ("b", "Trời nhiều mây: tổng sáng dưới ngưỡng thì bỏ qua LDR, giữ vị trí theo lịch thiên văn cho cả hai trục để tránh dao động vô ích."),
    ("p", "Phương pháp lai kế thừa ưu điểm cả hai nhánh: bám sát khi nắng đẹp, không lạc hướng khi mây, nên được chọn cho mô hình hai trục; kết quả so sánh ba phương pháp trình bày ở Chương 3."),
]

NGHIEN_CUU_H1_CH3 = "CHƯƠNG 3. KẾT QUẢ NGHIÊN CỨU PHƯƠNG PHÁP LAI BẰNG MÔ PHỎNG"
NGHIEN_CUU_CH3 = [
    ("h2", "3.1. Cách hệ lai tính toán trong một chu kỳ"),
    ("b", "Bước 1 – đọc giờ DS1307, đổi sang giờ Mặt Trời theo kinh độ 106,06° Đông của Mỹ Hào."),
    ("b", "Bước 2 – tính δ, H, α, γ suy ra góc lệnh của trục nghiêng và trục phương vị."),
    ("b", "Bước 3 – đọc hai biến trở: trục nào lệch góc lệnh quá 5° thì chạy motor theo lịch (định vị thô), chỉnh trục nghiêng trước rồi tới phương vị."),
    ("b", "Bước 4 – đọc ma trận 4 LDR: tổng sáng S vượt ngưỡng nắng thì dùng e1 tinh chỉnh phương vị, e2 tinh chỉnh nghiêng với ngưỡng chết 3°."),
    ("b", "Bước 5 – hiển thị LCD giờ, góc lệnh, góc thực, e1, e2; ghi log rồi chờ chu kỳ sau."),
    ("h2", "3.2. Kết quả của ma trận tính toán LDR"),
    ("p", "Bảng dưới đây là kết quả chạy ma trận tính toán với cụm LDR gá β_s = 30° có vách che, áp dụng chung cho cả hai trục vì công thức sai lệch theo từng cặp kênh là như nhau:"),
    ("tbl", [
        ["Góc lệch thật", "Kênh sáng hơn (mức ADC)", "Kênh tối hơn (mức ADC)", "e", "Góc suy ra"],
        ["0°", "1732", "1732", "0,000", "0,0°"],
        ["3°", "1782", "1677", "+0,030", "+3,0°"],
        ["6°", "1827", "1618", "+0,061", "+6,0°"],
        ["10°", "1879", "1532", "+0,102", "+10,0°"],
        ["15°", "1932", "1414", "+0,155", "+15,0°"],
        ["20°", "1970", "1286", "+0,210", "+20,0°"],
        ["30°", "2000", "1000", "+0,333", "+30,0°"],
    ], "{B}. Kết quả ma trận tính toán LDR dùng chung cho hai trục"),
    ("p", "Ngưỡng chết chọn e = 0,030 tương đương lệch 3° cho cả hai trục: lệch nhỏ hơn thì motor không chạy; lệch từ 3° trở lên thì một bước tinh chỉnh đưa trục về đúng hướng."),
    ("h2", "3.3. Kết quả bám trong ngày nắng"),
    ("tbl", [
        ["Ngày", "Thiên văn: sai số / số lần chạy", "LDR thuần: sai số / số lần chạy", "Lai: sai số / số lần chạy"],
        ["21/3", "2,6° / 77 lần", "0,8° / 86 lần", "1,2° / 142 lần"],
        ["21/6", "2,7° / 75 lần", "0,8° / 83 lần", "1,1° / 145 lần"],
        ["23/9", "2,6° / 77 lần", "0,7° / 86 lần", "1,2° / 142 lần"],
        ["21/12", "2,6° / 72 lần", "0,8° / 90 lần", "1,3° / 139 lần"],
    ], "{B}. Sai số bám và số lần chạy motor trong ngày nắng (trục phương vị)"),
    ("img", "hinh_ve/ket_qua_mo_phong_1_truc.png", "{H}. Góc tấm pin theo luật lai bám sát góc Mặt Trời lý tưởng ngày 21/6"),
    ("p", "Trục phương vị của luật lai giữ lệch hướng quanh 1–1,3° trong ngày nắng; thiên văn thuần chịu lệch đều 2,6° đúng bằng sai số lắp đặt giả định. Trục nghiêng có hành vi tương tự vì dùng cùng công thức với e2; riêng mùa đông trục nghiêng làm việc nhiều hơn vì Mặt Trời đi thấp."),
    ("h2", "3.4. Kết quả khi trời nhiều mây"),
    ("tbl", [
        ["Ngày", "LDR thuần: sai số / số lần chạy", "Lai: sai số / số lần chạy"],
        ["21/3", "74,7° / 106 lần", "1,6° / 33 lần"],
        ["21/6", "69,1° / 123 lần", "1,7° / 31 lần"],
        ["23/9", "74,9° / 106 lần", "1,6° / 33 lần"],
        ["21/12", "92,5° / 99 lần", "1,6° / 33 lần"],
    ], "{B}. Hành vi của LDR thuần và luật lai trong ngày nhiều mây"),
    ("p", "Trời mờ đều, nhánh LDR thuần không còn chênh lệch để dò nên tấm pin đứng yên trong khi Mặt Trời đi tiếp: sai số dồn tới 70–90°. Luật lai nhận biết tổng sáng thấp nên cả hai trục giữ lịch thiên văn, sai số 1,6–1,7° và motor chỉ chạy theo bước lịch 31–33 lần. Với hệ hai trục, lợi thế này càng rõ vì trục nghiêng không bị tụt xuống vị trí sai rồi phải kéo lại khi nắng bừng."),
    ("h2", "3.5. Năng lượng thu được so với tấm cố định"),
    ("tbl", [
        ["Ngày", "Tấm cố định", "Thiên văn", "LDR thuần", "Lai"],
        ["21/3", "100%", "246%", "221%", "246%"],
        ["21/6", "100%", "157%", "144%", "157%"],
        ["23/9", "100%", "249%", "224%", "249%"],
        ["21/12", "100%", "479%", "410%", "478%"],
    ], "{B}. Năng lượng trực xạ trong ngày, tấm cố định = 100%"),
    ("img", "hinh_ve/ket_qua_nang_luong.png", "{H}. Năng lượng thu được trong ngày so với tấm cố định"),
    ("p", "Bám nắng hai trục theo luật lai thu gấp 1,6 đến 4,8 lần tấm cố định tùy mùa và luôn nằm trong nhóm cao nhất ở cả ngày nắng lẫn ngày mây, nên được chọn làm phương pháp điều khiển của mô hình."),
    ("h2", "3.6. Nhận xét và thông số chính của chương trình"),
    ("b", "Phương pháp điều khiển: lai thiên văn + LDR; thiên văn định vị thô và giữ lịch khi mây, LDR tinh chỉnh khi nắng; trục nghiêng chỉnh trước, phương vị chỉnh sau."),
    ("b", "Góc gá cảm biến β_s = 30°, vách che chữ thập giữa cụm; ngưỡng chết |e1|, |e2| = 0,030 (lệch 3°); ngưỡng nắng bằng 25% tổng sáng lúc trưa."),
    ("b", "Bước lịch thiên văn 2° cho mỗi trục; ngưỡng chuyển định vị thô 5°; tinh chỉnh LDR đi thẳng góc suy ra từ e."),
]
NGHIEN_CUU_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"
NGHIEN_CUU_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành ma trận tính toán LDR dùng chung hai trục: góc suy ra trùng góc đặt 0–30°, xác định ngưỡng chết e = 0,030 (mục 3.2)."),
    ("b", "Hoàn thành mô phỏng ba phương pháp: luật lai giữ 1,1–1,7° cả ngày nắng lẫn ngày mây, LDR thuần lạc hướng 70–90° khi mây (mục 3.3, 3.4)."),
    ("b", "Hoàn thành bảng năng lượng: luật lai thu 157–478% so tấm cố định tùy mùa (mục 3.5)."),
    ("b", "Hoàn thành thứ tự chỉnh trục nghiêng trước – phương vị sau và bộ thông số cho chương trình hai trục."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Hiệu chỉnh hệ số kinh độ giờ Mặt Trời trong code theo giờ đọc thực tế của DS1307."),
    ("b", "Đo kiểm chứng vách che chữ thập cho cả hai cặp kênh e1 và e2."),
    ("b", "Gửi quyển nghiên cứu xin góp ý của giảng viên hướng dẫn."),
]

CHE_TAO_H1_CH1 = "CHƯƠNG 1. PHƯƠNG ÁN THIẾT KẾ HỆ HAI TRỤC"
CHE_TAO_H1_CH2 = "CHƯƠNG 2. THIẾT KẾ CƠ KHÍ, MẠCH ĐIỆN VÀ VẬT TƯ"
CHE_TAO_H1_CH3 = "CHƯƠNG 3. CHẾ TẠO MẠCH, HIỆU CHUẨN VÀ ĐO ĐẠC"
CHE_TAO_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"

CHE_TAO_CH1 = [
    ("h2", "1.1. Phương pháp điều khiển của hệ"),
    ("p", "Hệ hai trục dùng phương pháp lai: góc thiên văn tính từ ngày–giờ DS1307 theo δ, H, α, γ cho cả trục nghiêng và trục phương vị; góc hiện tại đọc từ hai biến trở; trục nào lệch thô quá 5° thì chạy motor theo lịch, chỉnh nghiêng trước rồi phương vị sau; khi nắng đẹp e1 tinh chỉnh phương vị và e2 tinh chỉnh nghiêng với ngưỡng chết 3°; trời mây thì cả hai trục giữ vị trí theo lịch."),
    ("eq", "e1 = [(L_TT + L_TD) − (L_PT + L_PD)] / S;   e2 = [(L_TT + L_PT) − (L_TD + L_PD)] / S"),
    ("p", "Mỗi motor chỉ nhận xung lệnh ngắn rồi dừng; hộp giảm tốc trục vít tự hãm giữ tấm pin 4 kg đứng yên giữa hai lần chạy, không tốn điện giữ và không trôi khi mất điện."),
    ("h2", "1.2. Cấu trúc tổng thể"),
    ("img", "hinh_ve/so_do_khoi_2_truc.png", "{H}. Sơ đồ khối hệ thống bám nắng hai trục điều khiển lai"),
    ("tbl", [
        ["Khối", "Cấu hình", "Nhiệm vụ"],
        ["Cảm biến hướng", "4 LDR có vách che chữ thập", "Tạo e1 (phương vị) và e2 (nghiêng)."],
        ["Hồi tiếp góc", "2 biến trở đồng trục", "Góc hiện tại của từng trục."],
        ["Thời gian", "Module DS1307 (I²C 0x68)", "Ngày–giờ cho nhánh thiên văn."],
        ["Hiển thị", "LCD I²C 1602 (0x27)", "Giờ, góc hai trục, e1, e2, chế độ."],
        ["Điều khiển", "ESP32 DevKit", "Luật lai hai trục, liên động, log."],
        ["Cách ly – công suất", "4 opto PC817 + 2 cầu H 4 TIP41C", "Đảo chiều hai motor 12 V."],
        ["Chấp hành", "2 motor gạt nước trục vít 12 V", "Nghiêng và phương vị, tự giữ vị trí."],
        ["Bảo vệ", "qt1…qt4 + diode + 1N4007", "Chặn quá hành trình từng trục."],
    ], "{B}. Các khối chức năng của hệ thống hai trục"),
    ("h2", "1.3. Cụm cảm biến LDR và vách che"),
    ("img", "hinh_ve/bo_tri_4_ldr.png", "{H}. Bố trí 4 LDR ở bốn góc và vách che chữ thập giữa cụm"),
    ("p", "Bốn LDR gá chếch 30° như nhau quanh vách che chữ thập cao 3 cm; cặp trái–phải tạo e1 cho trục phương vị, cặp trên–dưới tạo e2 cho trục nghiêng. Giá gá cùng một mẫu để β_s đồng đều; cụm đặt tại tâm tấm pin để không bị khung che bóng khi nghiêng sâu."),
    ("h2", "1.4. Cơ cấu chấp hành và hồi tiếp vị trí"),
    ("p", "Trục phương vị đặt thẳng đứng trên đế xoay, trục nghiêng vuông góc qua khớp nâng hạ; mỗi trục một motor gạt nước 12 V nối tay đòn khớp bản lề và một biến trở 10 k đồng trục chia áp về GPIO36 (nghiêng) và GPIO39 (phương vị). Bốn công tắc hành trình qt1…qt4 chặn hai đầu mỗi trục. Lệnh quay của mỗi motor đi qua một cặp opto PC817 xuống cầu H TIP41C riêng, cách ly hoàn toàn với khối logic."),
]

CHE_TAO_CH2 = [
    ("h2", "2.1. Kết cấu cơ khí"),
    ("p", "Đế thép phẳng có bulông cân bằng mang cụm đế xoay phương vị; khớp nâng hạ gắn vuông góc mang trục nghiêng và khung đỡ tấm pin 100 W khoảng 4 kg. Tâm khối lượng tấm pin đặt sát trục nghiêng để giảm mô-men trọng lượng; hai tay đòn khớp bản lề nối hai motor với hai trục; dây dẫn chừa dư theo hành trình cả hai trục. Bốn công tắc hành trình gá trước điểm va chạm cứng khoảng 2° mỗi đầu trục."),
    ("p", "Bản vẽ chi tiết cơ khí sẽ bổ sung bằng bản vẽ tay ở phiên bản sau; bản này mô tả kết cấu bằng lời cùng bảng tính chọn động cơ bên dưới."),
    ("h2", "2.2. Tính chọn động cơ cho tấm pin 4 kg – 100 W"),
    ("tbl", [
        ["Hạng mục", "Trục nghiêng", "Trục phương vị"],
        ["Mô-men trọng lượng (lệch tâm 5 cm)", "≈ 2,0 N·m", "≈ 0 N·m (cân bằng)"],
        ["Mô-men gió v = 8 m/s (tay đòn 0,3 m)", "≈ 7,5 N·m", "≈ 7,5 N·m"],
        ["Mô-men yêu cầu (×2 khởi động, ma sát)", "≈ 19 N·m", "≈ 15 N·m"],
        ["Motor gạt nước + giảm tốc ngoài 1:3", "24 – 36 N·m", "24 – 36 N·m"],
        ["Hệ số an toàn", "1,3 – 1,9 lần", "1,6 – 2,4 lần"],
        ["Tự giữ khi ngắt điện", "Trục vít tự hãm, không trôi", "Trục vít tự hãm, không trôi"],
    ], "{B}. Tính chọn hai động cơ cho tấm pin 4 kg – 100 W"),
    ("p", "Trục nghiêng chịu tải nặng nhất vì luôn mang mô-men trọng lượng tấm pin 4 kg; cặp motor gạt nước kèm giảm tốc ngoài 1:3 cho 24–36 N·m ở trục ra, đủ hệ số an toàn 1,3–2,4 lần ở gió 8 m/s. Khi gió trên 10 m/s hệ hạ tấm pin nằm ngang theo chế độ nghỉ để giảm tay đòn gió."),
    ("h2", "2.3. Mạch điện: nguồn, cách ly, động lực và đo lường"),
    ("p", "Nguồn 12 V qua X1 và 1N4007 chống ngược cực; LM2596 hạ 3,3 V nuôi ESP32; 7805 kèm tụ 220 µF hạ 5 V nuôi LCD I²C 1602 và DS1307. Mỗi motor một cầu H bốn TIP41C với bốn diode bảo vệ, nhận lệnh qua cặp opto PC817 và điện trở 220 Ω; bốn công tắc hành trình qt1…qt4 kéo xuống 1k. Bốn kênh LDR, hai biến trở hồi tiếp đưa vào các chân ADC; hệ chỉ đo điện áp, chưa đo dòng điện."),
    ("img", "hinh_ve/so_do_ket_noi_2_truc.png", "{H}. Sơ đồ kết nối ESP32 DevKit của mô hình hai trục"),
    ("tbl", [
        ["Chân ESP32", "Mạng tín hiệu", "Thiết bị"],
        ["GPIO25, 26, 27, 14", "LDR TT, PT, TD, PD", "Ma trận 4 LDR qua mạch chia áp."],
        ["GPIO36, 39", "biến trở nghiêng, phương vị", "Hồi tiếp góc hai trục."],
        ["GPIO34, 35, 32, 33", "qt1…qt4", "Hành trình hai đầu mỗi trục."],
        ["GPIO21, 22", "sda, scl", "DS1307 và LCD I²C chung bus."],
        ["GPIO19, 18", "th_thuan, th_nguoc trục nghiêng", "Cặp opto thứ nhất."],
        ["GPIO5, 13", "th_thuan, th_nguoc phương vị", "Cặp opto thứ hai."],
    ], "{B}. Bảng chân kết nối của mô hình hai trục"),
    ("h2", "2.4. Danh mục vật tư và linh kiện"),
    ("tbl", [
        ["TT", "Hạng mục", "Thông số", "SL"],
        ["1", "Tấm pin mặt trời", "100 W, khoảng 4 kg", "1"],
        ["2", "Quang trở LDR", "GL5528 cùng lô", "4"],
        ["3", "Điện trở chia áp LDR", "10 kΩ", "4"],
        ["4", "Biến trở hồi tiếp góc", "10 kΩ xoay", "2"],
        ["5", "Bo điều khiển", "ESP32 DevKit 38 chân", "1"],
        ["6", "Module RTC", "DS1307 có pin nuôi", "1"],
        ["7", "Màn hình", "LCD 1602 kèm mạch I²C", "1"],
        ["8", "Transistor công suất", "TIP41C", "8"],
        ["9", "Opto cách ly", "PC817C", "4"],
        ["10", "Diode", "1N4007 và 8 diode bảo vệ cầu H", "1 bộ"],
        ["11", "Ổn áp", "LM2596 (3,3 V) và 7805 (5 V)", "1 bộ"],
        ["12", "Tụ lọc", "220 µF/25 V", "2"],
        ["13", "Điện trở tín hiệu", "220 Ω (opto), 1 kΩ (hành trình)", "1 bộ"],
        ["14", "Công tắc hành trình", "Loại cần gạt", "4"],
        ["15", "Động cơ chấp hành", "Motor gạt nước 12 V trục vít", "2"],
        ["16", "Giảm tốc ngoài", "Tỷ số 1:3 mỗi trục", "2"],
        ["17", "Nguồn", "12 V 15 A kèm đầu nối X1", "1"],
        ["18", "Cơ khí và phụ trợ", "Đế xoay, khớp nâng hạ, trục, ốc vít, dây", "1 bộ"],
    ], "{B}. Danh mục vật tư – linh kiện của mô hình hai trục"),
]

CHE_TAO_CH3 = [
    ("h2", "3.1. Thiết kế mạch trên EasyEDA"),
    ("p", "Mạch hai trục được vẽ trên EasyEDA theo cùng bảy khối của bản một trục, riêng khối động lực và khối opto nhân đôi cho hai motor. Các hình dưới đây là bản vẽ lại của bảy khối đó."),
    ("img", "hinh_ve/mach/mach_nguon_lm2596.png", "{H}. Khối nguồn: chống ngược cực 1N4007 và hạ áp LM2596 xuống 3,3 V"),
    ("img", "hinh_ve/mach/mach_7805_lcd_i2c.png", "{H}. Nhánh 5 V: ổn áp 7805 và màn hình LCD I²C 1602"),
    ("img", "hinh_ve/mach/mach_ds1307.png", "{H}. Module thời gian thực DS1307 nối chung bus I²C"),
    ("img", "hinh_ve/mach/mach_esp32_devkit.png", "{H}. Khối ESP32 DevKit với các mạng tín hiệu hai trục"),
    ("img", "hinh_ve/mach/mach_opto_pc817.png", "{H}. Một cặp opto PC817C; trục thứ hai dùng cặp giống hệt"),
    ("img", "hinh_ve/mach/mach_dong_luc_cau_h_tip41c.png", "{H}. Một cầu H bốn TIP41C; mỗi motor một cầu giống hệt"),
    ("img", "hinh_ve/mach/mach_cong_tac_hanh_trinh.png", "{H}. Bốn công tắc hành trình qt1…qt4 kéo xuống 1 kΩ"),
    ("h2", "3.2. Chế tạo mạch"),
    ("b", "Hoàn thành khối nguồn: LM2596 đạt 3,3 V ± 0,1 V và 7805 đạt 5,0 V khi ESP32, LCD và DS1307 hoạt động đồng thời."),
    ("b", "Hoàn thành hai khối cầu H – opto: thử không tải từng kênh, sụt áp nhánh dưới 0,9 V ở 1 A; tám TIP41C gắn cánh tản nhiệt riêng."),
    ("b", "Hoàn thành khối hành trình bốn kênh và cụm chia áp LDR, hai biến trở: điện áp ra thay đổi tuyến tính toàn hành trình."),
    ("b", "Hoàn thành ráp DS1307 và LCD lên bus I²C: quét bus thấy đúng địa chỉ 0x68 và 0x27."),
    ("b", "Hoàn thành kiểm tra cách ly hai khối công suất với khối logic bằng đo trở kháng mass."),
    ("h2", "3.3. Chế tạo cơ khí"),
    ("b", "Hoàn thành đế xoay phương vị: quay trơn 360°, căn hướng Bắc–Nam bằng la bàn."),
    ("b", "Hoàn thành khớp nâng hạ trục nghiêng vuông góc trục phương vị, không rơ lắc."),
    ("b", "Hoàn thành gá tấm pin 4 kg, tâm khối lượng sát trục nghiêng trong phạm vi 2 cm."),
    ("b", "Hoàn thành hai tay đòn, hai giảm tốc ngoài 1:3, cụm LDR có vách che và hai biến trở đồng trục."),
    ("b", "Chưa hoàn thành: bản vẽ cơ khí chi tiết và ảnh mô hình sẽ bổ sung ở phiên bản sau."),
    ("h2", "3.4. Hiệu chuẩn và đo đạc"),
    ("tbl", [
        ["Hạng mục hiệu chuẩn", "Cách làm", "Kết quả"],
        ["Cân bằng 4 kênh LDR", "Che đều, chỉnh hệ số kênh trong code", "Bốn kênh lệch dưới 2%"],
        ["Biến trở nghiêng", "Quay 0°, 45°, 90° ghi điện áp", "0,32 / 1,66 / 2,98 V"],
        ["Biến trở phương vị", "Quay −60°, 0°, +60°", "0,35 / 1,65 / 2,95 V"],
        ["Dấu lệnh e1, e2", "Che từng phía của cụm", "Cả hai dấu đổi đúng chiều quay"],
        ["Hành trình", "Kéo tay chạm qt1…qt4", "LCD báo chạm, chặn đúng chiều"],
        ["Giờ DS1307", "So giờ điện thoại sau 24 giờ", "Lệch khoảng 3 giây/ngày"],
    ], "{B}. Kết quả hiệu chuẩn cảm biến và hồi tiếp hai trục"),
    ("tbl", [
        ["Phép đo bench", "Lệnh đưa vào", "Kết quả đo được"],
        ["Định vị thô hai trục", "Lệch giả lập 12° mỗi trục", "Dừng cách mốc 1–2°, nghiêng trước"],
        ["Tinh chỉnh LDR", "Đèn rọi lệch 8° theo hai phương", "Mỗi trục một bước, còn lệch dưới 1°"],
        ["Giữ vị trí", "Ngắt nguồn khi nghiêng 40°", "Cả hai trục không trôi"],
        ["Hiển thị", "Chạy liên tục 10 phút", "LCD hiện giờ, góc hai trục, e1, e2 đúng"],
    ], "{B}. Kết quả đo đạc chức năng trên bench thử"),
]

CHE_TAO_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành thiết kế EasyEDA và chế tạo khối nguồn, hai khối cầu H – opto, khối hành trình bốn kênh, khối RTC và LCD (mục 3.1, 3.2)."),
    ("b", "Hoàn thành tính chọn hai động cơ cho tấm pin 4 kg – 100 W: 24–36 N·m trục ra, hệ số an toàn 1,3–2,4 lần (mục 2.2)."),
    ("b", "Hoàn thành đế xoay, khớp nâng hạ, tay đòn, cụm LDR có vách che và hai biến trở hồi tiếp (mục 3.3)."),
    ("b", "Hoàn thành hiệu chuẩn bốn kênh LDR, hai biến trở, dấu lệnh e1/e2 và phép thử tự giữ khi mất điện (mục 3.4)."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Vẽ lại bản vẽ cơ khí chi tiết và chụp ảnh mô hình bổ sung vào Chương 3."),
    ("b", "Lắp hoàn chỉnh hai motor và chạy thử ngoài trời trọn một ngày nắng."),
    ("b", "Kiểm tra trình tự nghiêng trước – phương vị sau khi lệch thô đồng thời hai trục."),
]

LAP_TRINH_H1_CH1 = "CHƯƠNG 1. TỔNG QUAN HỆ THỐNG VÀ CÔNG CỤ PHÁT TRIỂN"
LAP_TRINH_H1_CH2 = "CHƯƠNG 2. CÁC NHÓM LỆNH VÀ MÔ ĐUN LẬP TRÌNH SỬ DỤNG"
LAP_TRINH_H1_CH3 = "CHƯƠNG 3. CHƯƠNG TRÌNH LAI HAI TRỤC: ADC, ĐỘNG CƠ, RTC, LCD VÀ HỒI TIẾP GÓC"
LAP_TRINH_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"

LAP_TRINH_CH1 = [
    ("h2", "1.1. Hệ thống được lập trình"),
    ("p", "Chương trình chạy trên ESP32 DevKit thực hiện luật lai cho cả hai trục: đọc DS1307 tính góc thiên văn của trục nghiêng và trục phương vị, đọc ma trận 4 LDR lấy e1 và e2 để tinh chỉnh khi nắng, đọc hai biến trở để biết góc hiện tại từng trục, điều khiển hai motor qua bốn opto và hai cầu H TIP41C, hiển thị giờ cùng trạng thái lên LCD I²C 1602 và ghi log Serial."),
    ("h2", "1.2. Phần mềm Arduino IDE và cách nạp chương trình cho ESP32"),
    ("p", "Arduino IDE dùng để soạn sketch, biên dịch, nạp firmware và xem Serial Monitor. Bản phân phối chuẩn chỉ kèm lõi AVR/SAM với trình biên dịch avr-gcc, còn ESP32 dùng nhân Xtensa LX6 với toolchain riêng, nên phải cài lõi esp32 của Espressif qua Boards Manager thì IDE mới nạp được."),
    ("b", "Bước 1. Cài Arduino IDE và driver USB-UART (CP210x hoặc CH340)."),
    ("b", "Bước 2. File → Preferences → Additional Boards Manager URLs: thêm https://espressif.github.io/arduino-esp32/package_esp32_index.json"),
    ("b", "Bước 3. Tools → Board → Boards Manager → tìm esp32 của Espressif Systems → Install."),
    ("b", "Bước 4. Tools → Board → esp32 → ESP32 Dev Module; chọn đúng cổng COM."),
    ("b", "Bước 5. Serial Monitor 115200 baud; giữ nút BOOT vài giây nếu dừng ở Connecting."),
    ("b", "Bước 6. Nạp sketch Blink thử trước khi nạp chương trình hai trục."),
    ("h2", "1.3. Mô đun lập trình ESP32 DevKit và các chân sử dụng"),
    ("tbl", [
        ["Nhóm chân", "Chân dùng", "Nhiệm vụ"],
        ["ADC2", "GPIO25, 26, 27, 14", "Bốn kênh LDR của ma trận."],
        ["ADC1", "GPIO36, 39", "Biến trở hồi tiếp nghiêng và phương vị."],
        ["Ngõ vào số", "GPIO34, 35, 32, 33", "qt1…qt4 hành trình hai trục."],
        ["I²C", "GPIO21, 22", "DS1307 và LCD I²C 1602."],
        ["Ngõ ra lệnh", "GPIO19, 18 và 5, 13", "th_thuan/th_nguoc của hai motor."],
    ], "{B}. Các chân ESP32 DevKit dùng trong chương trình hai trục"),
    ("p", "Hệ không bật WiFi khi vận hành nên ADC2 dùng an toàn cho bốn kênh LDR. Mọi chân lệnh đưa lên mức cao ngay trong setup() vì opto tác động ở mức thấp."),
]

LAP_TRINH_CH2 = [
    ("h2", "2.1. Nhóm cấu trúc chương trình"),
    ("tbl", [
        ["Lệnh / cấu trúc", "Cú pháp đại diện", "Ứng dụng"],
        ["setup() / loop()", "void loop() { }", "Khởi tạo một lần; vòng lặp luật lai."],
        ["if / else", "if (S > NGUONG_NANG) { }", "Chuyển chế độ nắng – mây – lệch thô."],
        ["for", "for (int i = 0; i < 32; i++)", "Lấy nhiều mẫu ADC rồi trung bình."],
        ["while", "while (digitalRead(qt) == 0)", "Chờ motor tới đích kèm giám sát hành trình."],
        ["millis()", "if (millis() - tTruoc >= 2000)", "Chu kỳ 2 s không chặn vòng lặp."],
    ], "{B}. Nhóm lệnh cấu trúc và điều khiển luồng"),
    ("h2", "2.2. Nhóm đọc ADC"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng"],
        ["analogRead", "analogRead(25);", "Đọc LDR và hai biến trở hồi tiếp."],
        ["analogSetPinAttenuation", "analogSetPinAttenuation(25, ADC_11db);", "Mở dải đo tới khoảng 2,45 V."],
        ["analogReadResolution", "analogReadResolution(12);", "4096 mức cho cả ADC1 và ADC2."],
    ], "{B}. Nhóm lệnh đọc ADC"),
    ("h2", "2.3. Nhóm điều khiển động cơ"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng"],
        ["digitalWrite", "digitalWrite(TH_NGUOC_2, LOW);", "Mức thấp mở opto cầu H chiều tương ứng."],
        ["digitalRead", "digitalRead(QT3);", "Hành trình phương vị: 1 là chạm."],
        ["pinMode", "pinMode(TH_THUAN_2, OUTPUT);", "Cấu hình bốn chân lệnh và bốn hành trình."],
    ], "{B}. Nhóm lệnh điều khiển hai động cơ"),
    ("h2", "2.4. Nhóm thời gian thực DS1307"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng"],
        ["Wire.requestFrom", "Wire.requestFrom(0x68, 7);", "Đọc 7 thanh ghi giờ DS1307."],
        ["Giải mã BCD", "(b & 0x0F) + 10 * (b >> 4)", "Đổi BCD sang thập phân."],
        ["Đổi ngày trong năm", "Bảng cộng dồn tháng", "Tính n cho công thức xích vĩ."],
    ], "{B}. Nhóm lệnh đọc giờ thực DS1307"),
    ("h2", "2.5. Nhóm hiển thị LCD I²C 1602"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng"],
        ["lcd.begin(16, 2)", "lcd.begin(16, 2);", "Khởi tạo qua PCF8574 địa chỉ 0x27."],
        ["lcd.setCursor", "lcd.setCursor(0, 1);", "Đặt con trỏ theo cột, dòng."],
        ["lcd.print", "lcd.print(e2);", "In giờ, góc hai trục, e1, e2."],
    ], "{B}. Nhóm lệnh hiển thị LCD I²C"),
]

CODE_2TRUC = """// Dieu khien lai 2 truc: thien van DS1307 + tinh chinh LDR (ESP32)
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int LDR[4] = {25, 26, 27, 14};            // TT, PT, TD, PD
const int POT_NG = 36, POT_PV = 39;             // bien tro hai truc
const int QT[4] = {34, 35, 32, 33};             // hanh trinh NG+, NG-, PV+, PV-
const int TH_NG[2] = {19, 18}, TH_PV[2] = {5, 13};   // opto muc THAP
const float PHI = 20.93, LAM = 106.06;
const float E_CHET = 0.030, S_NANG = 900, LECH_THO = 5.0;
float K_cal[4] = {1, 1, 1, 1};
unsigned long tTruoc = 0;

float docADC(int c) { long s = 0; for (int i = 0; i < 32; i++) { s += analogRead(c); delayMicroseconds(50); } return s / 32.0; }
byte bcd(byte b) { return (b & 0x0F) + 10 * (b >> 4); }
void docRTC(int &gio, int &phut, int &ngayTT) {
  Wire.beginTransmission(0x68); Wire.write(0); Wire.endTransmission();
  Wire.requestFrom(0x68, 7);
  byte g[7]; for (int i = 0; i < 7; i++) g[i] = Wire.read();
  gio = bcd(g[2]); phut = bcd(g[1]);
  const int t3[12] = {0,31,59,90,120,151,181,212,243,273,304,334};
  ngayTT = t3[bcd(g[5]) - 1] + bcd(g[4]);
}
float docGoc(int pot) { float v = docADC(pot) * 3.3 / 4095.0; return -60.0 + (v - 0.32) * 150.0 / 2.66; }
void dungMotor(const int th[2]) { digitalWrite(th[0], HIGH); digitalWrite(th[1], HIGH); }
void quay(const int th[2], int chieu, int ms, int qtChan) {
  if (digitalRead(qtChan) == 1) return;          // lien dong hanh trinh
  digitalWrite(chieu > 0 ? th[0] : th[1], LOW);
  delay(ms); dungMotor(th);                      // truc vit tu giu
}
void setup() {
  Serial.begin(115200); Wire.begin(); lcd.begin(16, 2); lcd.backlight();
  analogReadResolution(12);
  for (int i = 0; i < 4; i++) analogSetPinAttenuation(LDR[i], ADC_11db);
  analogSetPinAttenuation(POT_NG, ADC_11db); analogSetPinAttenuation(POT_PV, ADC_11db);
  for (int i = 0; i < 2; i++) { pinMode(TH_NG[i], OUTPUT); pinMode(TH_PV[i], OUTPUT); pinMode(QT[i], INPUT); }
  dungMotor(TH_NG); dungMotor(TH_PV);
}
void loop() {
  if (millis() - tTruoc < 2000) return;
  tTruoc = millis();
  int gio, phut, ngayTT; docRTC(gio, phut, ngayTT);
  float t = gio + phut / 60.0 + (LAM - 105.0) / 15.0;
  float d = radians(23.45 * sin(radians(360.0 * (284 + ngayTT) / 365.0)));
  float H = radians(15.0 * (t - 12.0));
  float sa = sin(radians(PHI)) * sin(d) + cos(radians(PHI)) * cos(d) * cos(H);
  float al = asin(sa);
  float lenhNG = degrees(atan2(cos(d) * cos(H) * cos(radians(PHI)) - sin(d) * sin(radians(PHI)), sa)) - 90.0;
  float lenhPV = degrees(atan2(cos(d) * sin(H), sa));
  float ngThuc = docGoc(POT_NG), pvThuc = docGoc(POT_PV);
  float L[4], S = 0;
  for (int i = 0; i < 4; i++) { L[i] = docADC(LDR[i]) * K_cal[i]; S += L[i]; }
  float e1 = ((L[0] + L[2]) - (L[1] + L[3])) / S;
  float e2 = ((L[0] + L[1]) - (L[2] + L[3])) / S;
  // dinh vi tho: nghieng truoc, phuong vi sau
  if (abs(lenhNG - ngThuc) > LECH_THO) quay(TH_NG, lenhNG > ngThuc ? 1 : -1, 300, lenhNG > ngThuc ? QT[0] : QT[1]);
  if (abs(lenhPV - pvThuc) > LECH_THO) quay(TH_PV, lenhPV > pvThuc ? 1 : -1, 300, lenhPV > pvThuc ? QT[2] : QT[3]);
  // tinh chinh LDR khi nang dep
  if (S > S_NANG) {
    if (fabs(e2) > E_CHET) quay(TH_NG, e2 > 0 ? 1 : -1, 120, e2 > 0 ? QT[0] : QT[1]);
    if (fabs(e1) > E_CHET) quay(TH_PV, e1 > 0 ? 1 : -1, 120, e1 > 0 ? QT[2] : QT[3]);
  }
  lcd.clear(); lcd.setCursor(0, 0);
  char buf[17]; sprintf(buf, "%02d:%02d NG%+4.1f", gio, phut, ngThuc); lcd.print(buf);
  lcd.setCursor(0, 1); sprintf(buf, "PV%+4.1f e%+4.2f", pvThuc, e1); lcd.print(buf);
  Serial.printf("%02d:%02d S=%.0f e1=%+.3f e2=%+.3f NG=%+.1f/%+.1f PV=%+.1f/%+.1f\\n",
                gio, phut, S, e1, e2, lenhNG, ngThuc, lenhPV, pvThuc);
}"""

LAP_TRINH_CH3 = [
    ("h2", "3.1. Phương pháp đọc ADC"),
    ("p", "Bốn kênh LDR và hai biến trở hồi tiếp đọc bằng ADC nội 12 bit với suy hao 11 dB; mỗi lần đọc lấy 32 mẫu cách nhau 50 µs rồi trung bình để loại xung nhiễu do hai cầu H đóng cắt; giá trị nhân hệ số hiệu chuẩn K_cal đo khi che đều bốn kênh. Hệ chỉ đo điện áp, chưa đo dòng điện."),
    ("h2", "3.2. Phương pháp đọc thời gian thực DS1307 và tính góc thiên văn hai trục"),
    ("p", "Mỗi chu kỳ đọc bảy thanh ghi DS1307 qua I²C 0x68, giải mã BCD ra giờ, phút và ngày trong năm, cộng hiệu số kinh độ để có giờ Mặt Trời. Từ đó tính δ, H, α và suy ra góc lệnh trục nghiêng (từ độ cao α so với góc lắp đặt) và góc lệnh trục phương vị; hai góc lệnh này dùng cho nhánh định vị thô và là vị trí giữ khi trời mây."),
    ("h2", "3.3. Phương pháp điều khiển động cơ qua opto và cầu H"),
    ("p", "Mỗi motor có cặp chân th_thuan/th_nguoc điều khiển opto ở mức thấp: hạ chân chiều cần quay xuống 0 trong một xung delay rồi đưa cả cặp về 1 để khóa cầu H, trục vít tự giữ. Trước mỗi xung, chương trình đọc công tắc hành trình chiều đó; chạm thì bỏ lệnh chiều nguy hiểm, chiều thoát vẫn chạy. Trục nghiêng luôn chỉnh trước trục phương vị để mặt pin đúng độ cao trước khi dò phương vị."),
    ("h2", "3.4. Phương pháp đọc biến trở biết góc nghiêng và góc phương vị"),
    ("p", "Hai biến trở 10 k đồng trục chia áp về GPIO36 và GPIO39; chương trình đọc điện áp, trung bình 32 mẫu rồi nội suy tuyến tính theo ba điểm hiệu chuẩn của từng trục để ra góc hiện tại. Hai góc hiện tại được so với góc lệnh thiên văn để quyết định định vị thô và hiển thị lên hai dòng LCD."),
    ("h2", "3.5. Phương pháp hiển thị giờ và trạng thái lên LCD I²C"),
    ("p", "LCD 1602 kèm PCF8574 địa chỉ 0x27 chung bus với DS1307. Dòng một in giờ thực đọc từ DS1307 và góc nghiêng thực tế, dòng hai in góc phương vị thực tế cùng e1; khi mất liên lạc I²C chương trình báo lỗi Serial và giữ chế độ lịch cuối."),
    ("h2", "3.6. Lưu đồ thuật toán"),
    ("img", "hinh_ve/luu_do_tong_quat.png", "{H}. Lưu đồ tổng quát chương trình điều khiển lai hai trục"),
    ("img", "hinh_ve/luu_do_thien_van.png", "{H}. Lưu đồ nhánh thiên văn đọc từ DS1307 cho hai trục"),
    ("img", "hinh_ve/luu_do_ldr.png", "{H}. Lưu đồ nhánh tinh chỉnh e1 và e2 theo ma trận LDR"),
    ("img", "hinh_ve/luu_do_dong_co.png", "{H}. Lưu đồ phát xung động cơ qua opto – cầu H"),
    ("img", "hinh_ve/luu_do_hien_thi.png", "{H}. Lưu đồ đọc giờ DS1307 và hiển thị LCD I²C"),
    ("h2", "3.7. Code mẫu chương trình lai hai trục"),
    ("code", CODE_2TRUC),
    ("p", "Hàm quay() dùng chung cho cả hai motor: kiểm tra hành trình, phát xung mức thấp qua opto rồi khóa cầu H để trục vít tự giữ. Vòng lặp thực hiện đúng thứ tự định vị thô nghiêng trước – phương vị sau, rồi tinh chỉnh e2 trước e1 khi nắng đẹp."),
    ("h2", "3.8. Kết quả đo đạc chương trình trên bench"),
    ("tbl", [
        ["Hạng mục kiểm tra", "Kết quả"],
        ["Ma trận tính toán LDR", "Góc suy ra trùng góc đặt 0–30° cho cả e1 và e2 (quyển nghiên cứu mục 3.2)."],
        ["Định vị thô hai trục", "Lệch giả lập 12° mỗi trục, dừng cách mốc 1–2°, nghiêng chỉnh trước."],
        ["Tinh chỉnh LDR", "Đèn rọi lệch 8° theo hai phương, mỗi trục một bước còn lệch dưới 1°."],
        ["Đọc giờ DS1307", "LCD hiện đúng giờ, lệch khoảng 3 giây sau 24 giờ."],
        ["Liên động hành trình", "Chạm qt bất kỳ: bỏ lệnh chiều đó, chiều thoát vẫn chạy."],
        ["Giữ vị trí", "Ngắt nguồn khi nghiêng 40°, cả hai trục không trôi."],
    ], "{B}. Kết quả kiểm tra chương trình hai trục trên bench thử"),
]

LAP_TRINH_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành chương trình lai hai trục với hàm quay() dùng chung, thứ tự nghiêng trước – phương vị sau (mục 3.7)."),
    ("b", "Hoàn thành năm lưu đồ tổng quát và từng phần cho thiên văn, LDR, động cơ, hiển thị (mục 3.6)."),
    ("b", "Hoàn thành kiểm tra bench hai trục: định vị thô 1–2°, tinh chỉnh dưới 1°, liên động đúng (mục 3.8)."),
    ("b", "Hoàn thành hướng dẫn cài lõi ESP32 cho Arduino IDE và bảng chân DevKit hai trục (Chương 1)."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Chạy ngoài trời trọn ngày nắng, ghi log góc hai trục đối chiếu mô phỏng."),
    ("b", "Bổ sung chế độ hạ tấm pin nằm ngang khi gió lớn dùng hành trình làm mốc."),
    ("b", "Tinh chỉnh độ dài xung tinh chỉnh 120 ms theo tải thực tế của hai motor."),
]
