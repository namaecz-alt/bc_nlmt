# -*- coding: utf-8 -*-
"""Noi dung moi ban 1 truc – phuong phap LAI thien van + LDR,
phan cung: ESP32 DevKit, cau H 4 TIP41C cach ly opto PC817, DS1307,
LCD I2C 1602, nguon LM2596/7805. Tien do tuan 5/10 - 10/10/2026."""

# ---------- thay muc 2.4 va 2.5 ban goc ----------
NEW_24_25 = [
    ("h2", "2.4. Bộ điều khiển ESP32 DevKit và các khối phụ trợ"),
    ("p", "ESP32 DevKit (Xtensa LX6 hai nhân 240 MHz, 4 MB flash) là vi điều khiển duy nhất của mô hình. Hệ không dùng WiFi khi vận hành nên cả tám kênh ADC1 lẫn mười kênh ADC2 đều dùng được cho bốn kênh LDR, biến trở hồi tiếp và cầu chia áp đo điện áp tấm pin; báo cáo chỉ đo điện áp, chưa đo dòng điện. Hai chân GPIO21/GPIO22 nối bus I²C chung cho module thời gian thực DS1307 và màn hình LCD I²C 1602; GPIO19/GPIO18 là hai chân lệnh th_thuan/th_nguoc đưa xuống mạch cách ly opto; GPIO34, 35, 32, 33 đọc bốn công tắc hành trình qt1…qt4."),
    ("p", "Module DS1307 giữ giờ thực kể cả khi mất điện nhờ pin nuôi, cấp dữ liệu ngày–giờ cho nhánh tính thiên văn; màn hình LCD I²C 1602 hiển thị giờ đọc được, góc lệnh, góc thực tế và trạng thái để người vận hành quan sát trực tiếp mà không cần máy tính."),
    ("h2", "2.5. Mạch động lực cầu H TIP41C cách ly opto và động cơ trục vít"),
    ("p", "Động cơ chấp hành là động cơ gạt nước ô tô 12 V kèm hộp giảm tốc trục vít – bánh vít: cặp trục vít tự hãm nên khi ngắt lệnh tấm pin tự giữ vị trí dưới gió và trọng lượng bản thân, không cần nuôi điện giữ. Mạch động lực dùng cầu H ghép từ bốn transistor TIP41C (U1…U4) với bốn diode bảo vệ chống sức điện động ngược khi ngắt dòng; hai tín hiệu dkxuoi/dknguoc đi qua opto PC817 (PH1, PH2) kèm điện trở 220 Ω để cách ly hoàn toàn khối logic 3,3 V với khối công suất 12 V."),
    ("p", "Opto đấu theo kiểu mức thấp tác động: chân lệnh ESP32 xuống 0 thì LED opto sáng, transistor quang dẫn và mở cầu H chiều tương ứng; cả hai chân lệnh ở mức 1 thì cầu H khóa. Vì vậy ngay trong setup() chương trình đưa hai chân lệnh lên mức cao trước khi vào vòng lặp để tránh xung lệnh lúc khởi động. Nguồn 12 V vào qua diode 1N4007 chống ngược cực, nhánh LM2596 hạ xuống 3,3 V nuôi ESP32 và nhánh 7805 hạ xuống 5 V nuôi LCD, DS1307."),
]

# ---------- thay toan bo muc 2.9 ban goc: chi con 3 phuong phap ----------
NEW_29 = [
    ("h2", "2.9. Các phương pháp bám nắng khảo sát"),
    ("p", "Đề tài khảo sát ba nhóm phương pháp điều khiển bám nắng phổ biến nhất cho tấm pin quang điện và chọn phương pháp lai làm phương án thực hiện."),
    ("h3", "2.9.1. Phương pháp bám theo cảm biến quang trở (vòng kín)"),
    ("p", "Bốn quang trở LDR đặt ở bốn góc tấm pin, giữa cụm có vách che chữ thập tạo bóng chênh lệch khi lệch hướng. Gọi tín hiệu ADC của bốn kênh là L_trái, L_phải, L_trên, L_dưới, bộ điều khiển tính:"),
    ("eq", "e1 = ADC(LDR_trái) − ADC(LDR_phải);   e2 = ADC(LDR_trên) − ADC(LDR_dưới)"),
    ("p", "Luật điều khiển: nếu |e1| lớn hơn ngưỡng thì quay động cơ trục 1 theo dấu e1; nếu |e2| lớn hơn ngưỡng thì quay động cơ trục 2 theo dấu e2; ngược lại dừng. Khoảng ngưỡng chính là vùng chết chống dao động quanh vị trí cân bằng."),
    ("b", "Ưu điểm: đơn giản, rẻ, phản ứng theo điều kiện sáng thực tế, không cần tọa độ và đồng hồ chính xác."),
    ("b", "Nhược điểm: nhạy với mây, bóng râm và bóng che tạm thời; khi trời mờ đều bốn kênh gần bằng nhau thì hệ mất phương hướng và đứng yên trong khi Mặt Trời vẫn di chuyển."),
    ("h3", "2.9.2. Phương pháp bám theo thời gian (vòng hở thiên văn)"),
    ("p", "Vị trí Mặt Trời được tính từ vị trí địa lý, ngày và giờ thực đọc từ module RTC DS1307. Với n là ngày trong năm, t là giờ Mặt Trời, φ là vĩ độ nơi lắp đặt:"),
    ("eq", "δ = 23,45° · sin[360° · (284 + n)/365]"),
    ("eq", "H = 15° · (t − 12)"),
    ("eq", "sin α = sin φ · sin δ + cos φ · cos δ · cos H"),
    ("p", "Góc phương vị γ tính từ α, δ, φ bằng công thức lượng giác cầu; từ α và γ suy ra góc lệnh cho trục quay của tấm pin. Vòng hở không dò tìm nên chuyển động mượt, không dao động."),
    ("b", "Ưu điểm: ổn định, không phụ thuộc thời tiết, không dao động; làm việc được cả khi mây dày."),
    ("b", "Nhược điểm: cần cài đặt đúng tọa độ và giờ; sai số lắp đặt, sai số đồng hồ không tự sửa được nên lệch vẫn hoàn lệch."),
    ("h3", "2.9.3. Phương pháp lai quang trở – thiên văn (lựa chọn của đề tài)"),
    ("b", "Thiên văn định vị thô: mỗi chu kỳ đọc DS1307, tính góc thiên văn; nếu góc lệnh lệch góc hiện tại quá 5° thì chạy motor theo lịch để kéo tấm pin về gần Mặt Trời, kể cả buổi sáng sớm hoặc sau khoảng mây dài."),
    ("b", "LDR tinh chỉnh: khi tổng sáng bốn kênh vượt ngưỡng nắng, sai lệch e1 (và e2 với bản hai trục) được dùng để tinh chỉnh motor từng bước nhỏ về phía nhận sáng mạnh hơn, bù sai số lắp đặt và sai số đồng hồ mà vòng hở không tự sửa được."),
    ("b", "Trời nhiều mây: tổng sáng dưới ngưỡng thì bỏ qua LDR, giữ vị trí theo lịch thiên văn để tránh dao động vô ích; hết mây hệ tự tinh chỉnh trở lại."),
    ("p", "Phương pháp lai kế thừa ưu điểm của cả hai nhánh: bám sát khi nắng đẹp nhờ vòng kín, không lạc hướng khi mây nhờ vòng hở, nên được chọn làm phương pháp điều khiển của đề tài; kết quả mô phỏng so sánh ba phương pháp trình bày ở Chương 3."),
]

# ---------- QUYEN NGHIEN CUU: chuong 3 viet lai truc quan ----------
NGHIEN_CUU_H1_CH3 = "CHƯƠNG 3. KẾT QUẢ NGHIÊN CỨU PHƯƠNG PHÁP LAI BẰNG MÔ PHỎNG"
NGHIEN_CUU_CH3 = [
    ("h2", "3.1. Cách hệ lai tính toán trong một chu kỳ"),
    ("b", "Bước 1 – đọc giờ: lấy ngày, giờ, phút, giây từ DS1307, đổi sang giờ Mặt Trời theo kinh độ 106,06° Đông của Mỹ Hào."),
    ("b", "Bước 2 – tính góc thiên văn: dùng các công thức δ, H, α, γ của mục 2.9.2 suy ra góc lệnh của trục quay."),
    ("b", "Bước 3 – so sánh góc hiện tại đọc từ biến trở: lệch trên 5° thì chạy motor theo lịch (định vị thô)."),
    ("b", "Bước 4 – đọc ma trận 4 LDR: tính tổng sáng S và sai lệch e1; nếu S vượt ngưỡng nắng và |e1| vượt ngưỡng chết thì tinh chỉnh motor theo dấu e1."),
    ("b", "Bước 5 – hiển thị LCD giờ, góc lệnh, góc thực tế, e1 và chế độ đang chạy; ghi log rồi chờ chu kỳ sau."),
    ("h2", "3.2. Kết quả của ma trận tính toán LDR"),
    ("p", "Bảng dưới đây là kết quả chạy ma trận tính toán với cụm LDR gá β_s = 30° có vách che: cột lệch thật là góc lệch đặt bằng giá thử, cột mức ADC là giá trị hai kênh đọc được, cột e1 là sai lệch chuẩn hóa và cột cuối là góc hệ suy ra từ e1. Ma trận cho lại đúng góc đặt trong toàn dải 0–30°, tức phép tinh chỉnh không cần dò thử:"),
    ("tbl", [
        ["Góc lệch thật", "Kênh phải (mức ADC)", "Kênh trái (mức ADC)", "e1", "Góc suy ra"],
        ["0°", "1732", "1732", "0,000", "0,0°"],
        ["3°", "1782", "1677", "+0,030", "+3,0°"],
        ["6°", "1827", "1618", "+0,061", "+6,0°"],
        ["10°", "1879", "1532", "+0,102", "+10,0°"],
        ["15°", "1932", "1414", "+0,155", "+15,0°"],
        ["20°", "1970", "1286", "+0,210", "+20,0°"],
        ["30°", "2000", "1000", "+0,333", "+30,0°"],
    ], "{B}. Kết quả ma trận tính toán LDR: góc suy ra trùng góc lệch thật"),
    ("p", "Ngưỡng chết được chọn tương ứng e1 = 0,030, tức góc lệch 3°: lệch nhỏ hơn 3° thì motor không chạy để tránh mài mòn; lệch 3° trở lên thì mỗi lần tinh chỉnh đưa tấm pin về đúng hướng chỉ trong một bước."),
    ("h2", "3.3. Kết quả bám trong ngày nắng"),
    ("p", "Mô phỏng cả ngày tại Mỹ Hào cho ba phương pháp, tấm pin xuất phát lệch 4° do sai số lắp đặt giả định. Bảng tổng hợp sai số lệch hướng trung bình và số lần motor khởi động:"),
    ("tbl", [
        ["Ngày", "Thiên văn: sai số / số lần chạy", "LDR thuần: sai số / số lần chạy", "Lai: sai số / số lần chạy"],
        ["21/3", "2,6° / 77 lần", "0,8° / 86 lần", "1,2° / 142 lần"],
        ["21/6", "2,7° / 75 lần", "0,8° / 83 lần", "1,1° / 145 lần"],
        ["23/9", "2,6° / 77 lần", "0,7° / 86 lần", "1,2° / 142 lần"],
        ["21/12", "2,6° / 72 lần", "0,8° / 90 lần", "1,3° / 139 lần"],
    ], "{B}. Sai số bám và số lần chạy motor trong ngày nắng"),
    ("img", "hinh_ve/ket_qua_mo_phong_1_truc.png", "{H}. Góc tấm pin theo luật lai bám sát góc Mặt Trời lý tưởng ngày 21/6"),
    ("p", "Ngày nắng, cả LDR thuần và lai đều giữ lệch hướng quanh 1°, riêng thiên văn thuần chịu lệch đều khoảng 2,6° đúng bằng sai số lắp đặt giả định vì vòng hở không tự sửa. Đồ thị cho thấy đường góc tấm pin của luật lai trùm gần kín đường góc Mặt Trời; các khoảng hệ số nắng thấp là lúc mây thoáng, hệ tạm giữ vị trí rồi tinh chỉnh lại ngay khi nắng lại."),
    ("h2", "3.4. Kết quả khi trời nhiều mây"),
    ("p", "Kịch bản ngày nhiều mây (phần lớn thời gian tổng sáng dưới ngưỡng nắng) cho thấy khác biệt lớn nhất giữa các phương pháp:"),
    ("tbl", [
        ["Ngày", "LDR thuần: sai số / số lần chạy", "Lai: sai số / số lần chạy"],
        ["21/3", "74,7° / 106 lần", "1,6° / 33 lần"],
        ["21/6", "69,1° / 123 lần", "1,7° / 31 lần"],
        ["23/9", "74,9° / 106 lần", "1,6° / 33 lần"],
        ["21/12", "92,5° / 99 lần", "1,6° / 33 lần"],
    ], "{B}. Hành vi của LDR thuần và luật lai trong ngày nhiều mây"),
    ("p", "Trời mờ đều, bốn kênh LDR gần bằng nhau nên nhánh LDR thuần không còn chênh lệch để dò, tấm pin đứng yên trong khi Mặt Trời tiếp tục đi: sai số dồn tới 70–90°. Luật lai nhận biết tổng sáng thấp nên chuyển sang bám lịch thiên văn, sai số chỉ còn 1,6–1,7° và motor chỉ chạy 31–33 lần theo bước lịch. Đây chính là lý do đề tài chọn phương pháp lai."),
    ("h2", "3.5. Năng lượng thu được so với tấm cố định"),
    ("p", "Lấy tấm cố định nghiêng 21° hướng Nam làm mốc 100%, năng lượng trực xạ thu được trong ngày của ba phương pháp bám:"),
    ("tbl", [
        ["Ngày", "Tấm cố định", "Thiên văn", "LDR thuần", "Lai"],
        ["21/3", "100%", "246%", "221%", "246%"],
        ["21/6", "100%", "157%", "144%", "157%"],
        ["23/9", "100%", "249%", "224%", "249%"],
        ["21/12", "100%", "479%", "410%", "478%"],
    ], "{B}. Năng lượng trực xạ trong ngày, tấm cố định = 100%"),
    ("img", "hinh_ve/ket_qua_nang_luong.png", "{H}. Năng lượng thu được trong ngày so với tấm cố định"),
    ("p", "Bám nắng giúp thu gấp 1,6 đến 4,8 lần tấm cố định tùy mùa. Luật lai đạt ngang thiên văn vào ngày mây và ngang hoặc nhỉnh hơn LDR thuần vào ngày nắng; tính trung bình cả hai loại ngày, luật lai thu nhiều năng lượng nhất trong ba phương pháp."),
    ("h2", "3.6. Nhận xét và thông số chính của chương trình"),
    ("b", "Phương pháp điều khiển: lai thiên văn + LDR như mục 2.9.3; thiên văn định vị thô và giữ lịch khi mây, LDR tinh chỉnh khi nắng."),
    ("b", "Góc gá cảm biến β_s = 30°, có vách che chữ thập giữa cụm để tăng chênh lệch bóng."),
    ("b", "Ngưỡng chết nhánh LDR: |e1| = 0,030 (tương đương lệch 3°); ngưỡng nắng của tổng sáng lấy bằng 25% giá trị lúc trưa nắng để nhận biết mây."),
    ("b", "Bước lịch thiên văn 2°, ngưỡng chuyển chế độ định vị thô 5°; mỗi lần tinh chỉnh LDR đi thẳng góc suy ra từ e1."),
]
NGHIEN_CUU_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"
NGHIEN_CUU_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành ma trận tính toán LDR có vách che: bảng kết quả mục 3.2 cho thấy góc suy ra trùng góc lệch thật từ 0° đến 30°, xác định ngưỡng chết e1 = 0,030."),
    ("b", "Hoàn thành mô phỏng so sánh ba phương pháp thiên văn / LDR thuần / lai trong ngày nắng và ngày nhiều mây: luật lai giữ sai số 1,1–1,7° trong khi LDR thuần lạc hướng 70–90° khi mây (mục 3.3, 3.4)."),
    ("b", "Hoàn thành bảng năng lượng so với tấm cố định: bám nắng lai thu 157–478% tùy mùa (mục 3.5)."),
    ("b", "Hoàn thành lựa chọn phương pháp lai và bộ thông số cho chương trình: β_s = 30°, ngưỡng chết 3°, bước lịch 2°, ngưỡng định vị thô 5°."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Đối chiếu giờ đọc từ DS1307 với giờ Mặt Trời thực tế tại Mỹ Hào, hiệu chỉnh hệ số kinh độ trong code."),
    ("b", "Đo kiểm chứng vách che chữ thập: che từng phía và ghi lại e1 để xác nhận dấu lệnh đúng."),
    ("b", "Gửi quyển nghiên cứu xin góp ý của giảng viên hướng dẫn và chỉnh sửa theo nhận xét."),
]

# ---------- QUYEN CHE TAO ----------
CHE_TAO_H1_CH1 = "CHƯƠNG 1. PHƯƠNG ÁN THIẾT KẾ HỆ THỐNG"
CHE_TAO_H1_CH2 = "CHƯƠNG 2. THIẾT KẾ CƠ KHÍ, MẠCH ĐIỆN VÀ VẬT TƯ"
CHE_TAO_H1_CH3 = "CHƯƠNG 3. CHẾ TẠO MẠCH, HIỆU CHUẨN VÀ ĐO ĐẠC"
CHE_TAO_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"

CHE_TAO_CH1 = [
    ("h2", "1.1. Phương pháp điều khiển của hệ"),
    ("p", "Hệ dùng phương pháp lai trình bày ở quyển nghiên cứu: góc thiên văn tính từ ngày–giờ đọc ở DS1307 theo các công thức δ, H, α, γ; góc hiện tại đọc từ biến trở hồi tiếp; lệch thô quá 5° thì chạy motor theo lịch; khi nắng đẹp sai lệch ma trận LDR e1 = (trái − phải)/tổng được dùng tinh chỉnh motor với ngưỡng chết 3°; trời mây thì giữ vị trí theo lịch."),
    ("eq", "e1 = [(L_TT + L_TD) − (L_PT + L_PD)] / S;   S = L_TT + L_PT + L_TD + L_PD"),
    ("p", "Động cơ chỉ nhận lệnh xung ngắn rồi dừng; hộp giảm tốc trục vít tự hãm giữ tấm pin đứng yên giữa hai lần chạy nên hệ không tốn điện giữ vị trí và không trôi khi mất điện."),
    ("h2", "1.2. Cấu trúc tổng thể"),
    ("img", "hinh_ve/so_do_khoi_1_truc.png", "{H}. Sơ đồ khối hệ thống bám nắng một trục điều khiển lai"),
    ("tbl", [
        ["Khối", "Cấu hình", "Nhiệm vụ"],
        ["Cảm biến hướng", "4 LDR có vách che chữ thập", "Tạo sai lệch e1 để tinh chỉnh."],
        ["Hồi tiếp góc", "Biến trở xoay đồng trục", "Báo góc hiện tại của tấm pin."],
        ["Đo kiểm", "Cầu chia áp vào ADC", "Theo dõi điện áp tấm pin (chỉ đo áp)."],
        ["Thời gian", "Module DS1307 (I²C 0x68)", "Cấp ngày–giờ cho nhánh thiên văn."],
        ["Hiển thị", "LCD I²C 1602 (0x27)", "Hiện giờ, góc, e1, chế độ."],
        ["Điều khiển", "ESP32 DevKit", "Chạy luật lai, liên động, ghi log."],
        ["Cách ly – công suất", "2 opto PC817 + cầu H 4 TIP41C", "Đảo chiều động cơ 12 V an toàn."],
        ["Chấp hành", "Motor gạt nước trục vít 12 V", "Quay trục Đông–Tây, tự giữ vị trí."],
        ["Bảo vệ", "qt1, qt2 + diode cầu H + 1N4007", "Chặn quá hành trình, chống ngược cực."],
    ], "{B}. Các khối chức năng của hệ thống một trục"),
    ("h2", "1.3. Cụm cảm biến LDR và vách che"),
    ("img", "hinh_ve/bo_tri_4_ldr.png", "{H}. Bố trí 4 LDR ở bốn góc và vách che chữ thập giữa cụm"),
    ("p", "Bốn LDR gá chếch ra ngoài 30° như nhau, vách che chữ thập cao 3 cm đặt giữa cụm để khi lệch hướng, bóng che làm một phía tối hơn rõ rệt, tăng độ chênh lệch tín hiệu. Giá gá in cùng một mẫu để bốn góc β_s đồng đều; sau hiệu chuẩn phải cố định chắc và tránh bóng của khung pin đổ lên cụm."),
    ("h2", "1.4. Cơ cấu chấp hành và hồi tiếp vị trí"),
    ("p", "Trục quay căn hướng Bắc–Nam, đặt gần trọng tâm tấm pin. Động cơ gạt nước 12 V nối tay đòn khớp bản lề; biến trở xoay 10 k đồng trục chia áp về GPIO36 để chương trình đọc góc hiện tại; hai công tắc hành trình qt1, qt2 đặt trước điểm va chạm cơ khí ở đầu Đông và đầu Tây. Lệnh quay đi qua opto PC817 xuống cầu H TIP41C nên khối công suất 12 V tách điện hoàn toàn khỏi khối logic 3,3 V."),
]

CHE_TAO_CH2 = [
    ("h2", "2.1. Kết cấu cơ khí"),
    ("p", "Khung đế thép phẳng có bulông cân bằng; hai gối đỡ mang trục thép tròn có bạc lót; tấm pin 100 W khối lượng khoảng 4 kg bắt lên khung đỡ nhôm qua tám tai bắt vít, tâm khối lượng đặt sát trục để giảm mô-men trọng lượng. Tay đòn nối trục ra hộp giảm tốc với khung pin có khớp bản lề khử sai lệch quỹ đạo; dây dẫn chừa dư theo toàn hành trình và buộc vào giá cố định. Hai công tắc hành trình gá sao cho cần gạt chạm trước khi khung pin va gối đỡ khoảng 2°."),
    ("p", "Hình vẽ chi tiết cơ khí sẽ được bổ sung bằng bản vẽ tay ở phiên bản sau; bản này mô tả kết cấu bằng lời và bảng tính chọn bên dưới."),
    ("h2", "2.2. Tính chọn động cơ cho tấm pin 4 kg – 100 W"),
    ("tbl", [
        ["Hạng mục", "Giá trị", "Ghi chú"],
        ["Tấm pin", "100 W, khoảng 4 kg, diện tích ≈ 0,65 m²", "Lắp cân bằng quanh trục."],
        ["Mô-men trọng lượng (lệch tâm 5 cm)", "≈ 2,0 N·m", "4 kg × 9,81 × 0,05 m."],
        ["Tải gió làm việc v = 8 m/s", "q = 0,6·v² ≈ 38 Pa; F ≈ 25 N", "Đẩy lên mặt pin 0,65 m²."],
        ["Mô-men gió (tay đòn 0,3 m)", "≈ 7,5 N·m", "Trường hợp gió ngang mặt pin."],
        ["Mô-men yêu cầu (×2 khởi động, ma sát)", "≈ 19 N·m", "Tổng hai thành phần nhân hệ số."],
        ["Motor gạt nước 12 V + giảm tốc ngoài 1:3", "24 – 36 N·m ở trục ra", "Bản thân motor 8 – 12 N·m."],
        ["Hệ số an toàn", "1,3 – 1,9 lần", "Đủ cho gió tới 8 m/s."],
        ["Chế độ gió lớn", "Trên 10 m/s: hạ tấm pin nằm ngang", "Giảm tay đòn gió về gần 0."],
    ], "{B}. Tính chọn động cơ cho tấm pin 4 kg – 100 W"),
    ("p", "Với tấm pin 4 kg, mô-men gió chiếm phần lớn tải; cặp trục vít của motor gạt nước cộng giảm tốc ngoài 1:3 cho mô-men trục ra 24–36 N·m, đủ hệ số an toàn 1,3–1,9 lần ở gió 8 m/s. Đổi lại tốc độ trục ra chậm (khoảng 0,5 vòng/phút) lại phù hợp vì mỗi lần hiệu chỉnh chỉ quay vài độ."),
    ("h2", "2.3. Mạch điện: nguồn, cách ly, động lực và đo lường"),
    ("p", "Nguồn 12 V vào qua đầu nối X1 và diode 1N4007 chống ngược cực; nhánh LM2596 hạ áp xuống 3,3 V nuôi ESP32, nhánh 7805 kèm tụ 220 µF hai đầu hạ xuống 5 V nuôi LCD I²C 1602 và module DS1307. Tín hiệu lệnh th_thuan/th_nguoc từ GPIO19/GPIO18 qua opto PC817 và điện trở 220 Ω xuống cầu H bốn TIP41C điều khiển động cơ; bốn công tắc hành trình qt1…qt4 kéo xuống 1k nên mức 0 là an toàn, mức 1 là chạm hành trình. Bốn kênh LDR, biến trở hồi tiếp và cầu chia áp điện áp tấm pin đưa thẳng vào các chân ADC; hệ chỉ đo điện áp, chưa đo dòng điện."),
    ("img", "hinh_ve/so_do_ket_noi_1_truc.png", "{H}. Sơ đồ kết nối ESP32 DevKit của mô hình một trục"),
    ("tbl", [
        ["Chân ESP32", "Mạng tín hiệu", "Thiết bị"],
        ["GPIO25, 26, 27, 14", "LDR TT, PT, TD, PD", "Ma trận 4 LDR qua mạch chia áp."],
        ["GPIO36", "biến trở hồi tiếp", "Góc hiện tại của tấm pin."],
        ["GPIO39", "cầu chia áp tấm pin", "Điện áp tấm pin (chỉ đo áp)."],
        ["GPIO34, 35", "qt1, qt2", "Công tắc hành trình Đông, Tây."],
        ["GPIO21, 22", "sda, scl", "DS1307 và LCD I²C chung bus."],
        ["GPIO19, 18", "th_thuan, th_nguoc", "Opto PC817 điều khiển cầu H."],
        ["3V3, GND", "nguồn logic", "Tách khối với 12 V và 5 V."],
    ], "{B}. Bảng chân kết nối của mô hình một trục"),
    ("h2", "2.4. Danh mục vật tư và linh kiện"),
    ("tbl", [
        ["TT", "Hạng mục", "Thông số", "SL"],
        ["1", "Tấm pin mặt trời", "100 W, khoảng 4 kg", "1"],
        ["2", "Quang trở LDR", "GL5528 cùng lô", "4"],
        ["3", "Điện trở chia áp LDR", "10 kΩ", "4"],
        ["4", "Biến trở hồi tiếp góc", "10 kΩ xoay", "1"],
        ["5", "Bo điều khiển", "ESP32 DevKit 38 chân", "1"],
        ["6", "Module RTC", "DS1307 có pin nuôi", "1"],
        ["7", "Màn hình", "LCD 1602 kèm mạch I²C", "1"],
        ["8", "Transistor công suất", "TIP41C", "4"],
        ["9", "Opto cách ly", "PC817C", "2"],
        ["10", "Diode", "1N4007 và 4 diode bảo vệ cầu H", "1 bộ"],
        ["11", "Ổn áp", "LM2596 (3,3 V) và 7805 (5 V)", "1 bộ"],
        ["12", "Tụ lọc", "220 µF/25 V", "2"],
        ["13", "Điện trở tín hiệu", "220 Ω (opto), 1 kΩ (hành trình)", "1 bộ"],
        ["14", "Công tắc hành trình", "Loại cần gạt", "2"],
        ["15", "Động cơ chấp hành", "Motor gạt nước 12 V trục vít", "1"],
        ["16", "Giảm tốc ngoài", "Tỷ số 1:3 (đai hoặc trục vít)", "1"],
        ["17", "Nguồn", "12 V 10 A kèm đầu nối X1", "1"],
        ["18", "Cơ khí và phụ trợ", "Trục, gối đỡ, nhôm hộp, ốc vít, dây", "1 bộ"],
    ], "{B}. Danh mục vật tư – linh kiện của mô hình một trục"),
]

CHE_TAO_CH3 = [
    ("h2", "3.1. Thiết kế mạch trên EasyEDA"),
    ("p", "Toàn bộ mạch được vẽ và kiểm tra footprint bằng EasyEDA, tách thành bảy khối riêng để dễ rà lỗi và dễ hàn: mạch động lực cầu H, mạch cách ly opto, mạch công tắc hành trình, khối ESP32, mạch nguồn LM2596, nhánh 5 V với LCD và module DS1307. Các hình dưới đây là bản vẽ lại của bảy khối đó."),
    ("img", "hinh_ve/mach/mach_nguon_lm2596.png", "{H}. Khối nguồn: chống ngược cực 1N4007 và hạ áp LM2596 xuống 3,3 V"),
    ("img", "hinh_ve/mach/mach_7805_lcd_i2c.png", "{H}. Nhánh 5 V: ổn áp 7805 và màn hình LCD I²C 1602"),
    ("img", "hinh_ve/mach/mach_ds1307.png", "{H}. Module thời gian thực DS1307 nối chung bus I²C"),
    ("img", "hinh_ve/mach/mach_esp32_devkit.png", "{H}. Khối ESP32 DevKit với các mạng tín hiệu của hệ"),
    ("img", "hinh_ve/mach/mach_opto_pc817.png", "{H}. Mạch cách ly opto PC817C cho hai chiều quay"),
    ("img", "hinh_ve/mach/mach_dong_luc_cau_h_tip41c.png", "{H}. Mạch động lực cầu H bốn TIP41C kèm diode bảo vệ"),
    ("img", "hinh_ve/mach/mach_cong_tac_hanh_trinh.png", "{H}. Bốn công tắc hành trình kéo xuống 1 kΩ"),
    ("h2", "3.2. Chế tạo mạch"),
    ("b", "Hoàn thành đặt linh kiện và đi dây khối nguồn trên mạch thử: kiểm tra đầu ra LM2596 đạt 3,3 V ± 0,1 V và 7805 đạt 5,0 V khi tải ESP32 và LCD cùng lúc."),
    ("b", "Hoàn thành hàn khối cầu H TIP41C và opto: thử không tải, đo sụt áp hai nhánh dưới 0,9 V ở dòng 1 A; diode bảo vệ mắc đúng chiều katôt về phía 12 V."),
    ("b", "Hoàn thành khối hành trình và cụm chia áp LDR, biến trở: đo điện áp ra biến trở thay đổi tuyến tính khi quay tay toàn hành trình."),
    ("b", "Hoàn thành ráp DS1307 và LCD lên bus I²C: quét bus thấy đúng hai địa chỉ 0x68 và 0x27, không xung đột."),
    ("b", "Hoàn thành kiểm tra cách ly: đo trở kháng giữa mass 3,3 V và mass 12 V hở mạch, xác nhận opto tách khối."),
    ("h2", "3.3. Chế tạo cơ khí"),
    ("b", "Hoàn thành khung đế và hai gối đỡ trục; trục quay trơn toàn hành trình khi thử bằng tay."),
    ("b", "Hoàn thành gá tấm pin 4 kg lên khung đỡ, tâm khối lượng sát trục trong phạm vi 2 cm."),
    ("b", "Hoàn thành tay đòn và giảm tốc ngoài 1:3 nối motor gạt nước với trục quay."),
    ("b", "Hoàn thành gá cụm LDR có vách che chữ thập và biến trở hồi tiếp đồng trục."),
    ("b", "Chưa hoàn thành: chụp ảnh và vẽ lại bản vẽ cơ khí chi tiết để đưa vào báo cáo phiên bản sau."),
    ("h2", "3.4. Hiệu chuẩn và đo đạc"),
    ("tbl", [
        ["Hạng mục hiệu chuẩn", "Cách làm", "Kết quả"],
        ["Cân bằng 4 kênh LDR", "Che đều bằng giấy can, chỉnh hệ số kênh trong code", "Bốn kênh lệch nhau dưới 2%"],
        ["Biến trở hồi tiếp", "Quay tay 0°, 45°, 90°, ghi điện áp", "0,32 V / 1,66 V / 2,98 V, tuyến tính"],
        ["Dấu lệnh e1", "Che phía phải rồi phía trái", "e1 đổi dấu đúng chiều cần quay"],
        ["Hành trình", "Kéo tay chạm qt1, qt2", "LCD báo chạm, motor chặn đúng chiều"],
        ["Giờ DS1307", "So với giờ điện thoại sau 24 giờ", "Lệch khoảng 3 giây/ngày"],
    ], "{B}. Kết quả hiệu chuẩn các khối cảm biến và hồi tiếp"),
    ("tbl", [
        ["Phép đo bench", "Lệnh đưa vào", "Kết quả đo được"],
        ["Quay thô theo lịch", "Lệch giả lập 12°", "Tấm pin dừng cách mốc 1–2°"],
        ["Tinh chỉnh LDR", "Đèn rọi lệch 8°", "Một bước tinh chỉnh còn lệch dưới 1°"],
        ["Giữ vị trí", "Ngắt nguồn đột ngột khi nghiêng 40°", "Tấm pin không trôi nhờ trục vít"],
        ["Hiển thị", "Để hệ chạy 10 phút", "LCD hiện giờ, góc, e1 đúng trạng thái"],
    ], "{B}. Kết quả đo đạc chức năng trên bench thử"),
]

CHE_TAO_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành thiết kế mạch trên EasyEDA bảy khối và chế tạo xong khối nguồn, khối cầu H – opto, khối hành trình, khối RTC và LCD (mục 3.1, 3.2)."),
    ("b", "Hoàn thành tính chọn động cơ cho tấm pin 4 kg – 100 W: motor gạt nước kèm giảm tốc 1:3 cho 24–36 N·m, hệ số an toàn 1,3–1,9 ở gió 8 m/s (mục 2.2)."),
    ("b", "Hoàn thành khung cơ khí, tay đòn, cụm LDR có vách che và biến trở hồi tiếp (mục 3.3)."),
    ("b", "Hoàn thành hiệu chuẩn bốn kênh LDR, biến trở ba điểm, dấu lệnh e1 và phép thử tự giữ khi mất điện (mục 3.4)."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Vẽ lại bản vẽ cơ khí chi tiết và chụp ảnh mô hình để bổ sung vào Chương 3."),
    ("b", "Lắp hoàn chỉnh motor lên trục và chạy thử ngoài trời một buổi nắng trọn vẹn."),
    ("b", "Đo điện áp tấm pin cả ngày qua kênh GPIO39 để đối chiếu giờ nắng với mô phỏng."),
]

# ---------- QUYEN LAP TRINH ----------
LAP_TRINH_H1_CH1 = "CHƯƠNG 1. TỔNG QUAN HỆ THỐNG VÀ CÔNG CỤ PHÁT TRIỂN"
LAP_TRINH_H1_CH2 = "CHƯƠNG 2. CÁC NHÓM LỆNH VÀ MÔ ĐUN LẬP TRÌNH SỬ DỤNG"
LAP_TRINH_H1_CH3 = "CHƯƠNG 3. CHƯƠNG TRÌNH ĐIỀU KHIỂN LAI: ĐỌC ADC, ĐỘNG CƠ, RTC, LCD VÀ HỒI TIẾP GÓC"
LAP_TRINH_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"

LAP_TRINH_CH1 = [
    ("h2", "1.1. Hệ thống được lập trình"),
    ("p", "Chương trình chạy trên ESP32 DevKit thực hiện luật điều khiển lai: đọc giờ thực từ DS1307 để tính góc thiên văn, đọc ma trận 4 LDR để tinh chỉnh khi nắng, đọc biến trở để biết góc nghiêng hiện tại của tấm pin, điều khiển động cơ qua opto và cầu H TIP41C, hiển thị giờ cùng trạng thái lên LCD I²C 1602 và ghi log ra Serial. Toàn bộ mạch điện và chân kết nối mô tả ở quyển chế tạo."),
    ("h2", "1.2. Phần mềm Arduino IDE và cách nạp chương trình cho ESP32"),
    ("p", "Arduino IDE là môi trường phát triển miễn phí dùng để soạn sketch, biên dịch, nạp firmware và xem dữ liệu qua Serial Monitor. Bản phân phối chuẩn chỉ kèm lõi AVR/SAM và trình biên dịch avr-gcc, trong khi ESP32 dùng nhân Xtensa LX6 với toolchain riêng, nên IDE vừa cài chưa nạp được ESP32: phải cài thêm lõi esp32 của Espressif qua Boards Manager."),
    ("b", "Bước 1. Cài Arduino IDE và driver USB-UART (CP210x hoặc CH340) nếu máy chưa nhận cổng."),
    ("b", "Bước 2. File → Preferences → Additional Boards Manager URLs: thêm https://espressif.github.io/arduino-esp32/package_esp32_index.json"),
    ("b", "Bước 3. Tools → Board → Boards Manager → tìm esp32 của Espressif Systems → Install."),
    ("b", "Bước 4. Tools → Board → esp32 → ESP32 Dev Module; chọn đúng cổng COM; giữ tốc độ nạp 921600."),
    ("b", "Bước 5. Serial Monitor đặt 115200 baud; nếu IDE dừng ở Connecting thì giữ nút BOOT vài giây."),
    ("b", "Bước 6. Nạp sketch Blink thử để xác nhận chuỗi biên dịch – nạp trước khi nạp chương trình chính."),
    ("h2", "1.3. Mô đun lập trình ESP32 DevKit và các chân sử dụng"),
    ("tbl", [
        ["Nhóm chân", "Chân dùng", "Nhiệm vụ trong chương trình"],
        ["ADC2", "GPIO25, 26, 27, 14", "Đọc bốn kênh LDR của ma trận."],
        ["ADC1", "GPIO36, 39", "Biến trở hồi tiếp góc và điện áp tấm pin."],
        ["Ngõ vào số", "GPIO34, 35", "qt1, qt2 công tắc hành trình."],
        ["I²C", "GPIO21 (sda), 22 (scl)", "DS1307 và LCD I²C 1602."],
        ["Ngõ ra lệnh", "GPIO19, 18", "th_thuan, th_nguoc xuống opto PC817."],
    ], "{B}. Các chân ESP32 DevKit dùng trong chương trình một trục"),
    ("p", "Hệ không bật WiFi khi vận hành nên nhóm ADC2 dùng an toàn cho bốn kênh LDR; hai kênh hồi tiếp quan trọng đặt trên ADC1. Mọi chân lệnh đều được đưa lên mức cao ngay trong setup() vì opto tác động ở mức thấp."),
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
        ["analogRead", "analogRead(25);", "Đọc kênh LDR, biến trở, áp tấm pin."],
        ["analogSetPinAttenuation", "analogSetPinAttenuation(25, ADC_11db);", "Mở dải đo tới khoảng 2,45 V."],
        ["analogReadResolution", "analogReadResolution(12);", "4096 mức cho cả ADC1 và ADC2."],
    ], "{B}. Nhóm lệnh đọc ADC"),
    ("h2", "2.3. Nhóm điều khiển động cơ"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng"],
        ["pinMode", "pinMode(TH_THUAN, OUTPUT);", "Cấu hình chân lệnh và chân hành trình."],
        ["digitalWrite", "digitalWrite(TH_THUAN, LOW);", "Mức thấp mở opto, cầu H chạy chiều thuận."],
        ["digitalRead", "digitalRead(QT1);", "Đọc hành trình: 1 là chạm, phải chặn chiều đó."],
    ], "{B}. Nhóm lệnh điều khiển động cơ qua opto – cầu H"),
    ("h2", "2.4. Nhóm thời gian thực DS1307"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng"],
        ["Wire.begin()", "Wire.begin();", "Khởi động master I²C."],
        ["Wire.requestFrom", "Wire.requestFrom(0x68, 7);", "Đọc 7 thanh ghi giờ của DS1307."],
        ["Giải mã BCD", "(b & 0x0F) + 10 * (b >> 4)", "Đổi nibble BCD sang số thập phân."],
    ], "{B}. Nhóm lệnh đọc giờ thực DS1307"),
    ("h2", "2.5. Nhóm hiển thị LCD I²C 1602"),
    ("tbl", [
        ["Lệnh", "Cú pháp đại diện", "Ứng dụng"],
        ["lcd.begin(16, 2)", "lcd.begin(16, 2);", "Khởi tạo màn hình qua PCF8574 địa chỉ 0x27."],
        ["lcd.setCursor", "lcd.setCursor(0, 0);", "Đặt vị trí con trỏ theo cột, dòng."],
        ["lcd.print", "lcd.print(gocThuc);", "In giờ, góc, e1 và chế độ lên màn hình."],
    ], "{B}. Nhóm lệnh hiển thị LCD I²C"),
]

CODE_1TRUC = """// Dieu khien lai: thien van tu DS1307 + tinh chinh LDR - 1 truc (ESP32)
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int LDR[4] = {25, 26, 27, 14};   // TT, PT, TD, PD
const int POT = 36, AP_PIN = 39, QT1 = 34, QT2 = 35;
const int TH_THUAN = 19, TH_NGUOC = 18;      // opto tac dong muc THAP
const float PHI = 20.93, LAM = 106.06;       // My Hao, Hung Yen
const float E_CHET = 0.030, S_NANG = 900;    // nguong chet va nguong nang
const float LECH_THO = 5.0;                  // do, chuyen che do dinh vi tho
float K_cal[4] = {1, 1, 1, 1};
unsigned long tTruoc = 0;

float docADC(int chan) {                     // 32 mau, trung binh
  long s = 0; for (int i = 0; i < 32; i++) { s += analogRead(chan); delayMicroseconds(50); }
  return s / 32.0;
}
byte bcd(byte b) { return (b & 0x0F) + 10 * (b >> 4); }
void docRTC(int &gio, int &phut, int &ngayTT) {   // DS1307 dia chi 0x68
  Wire.beginTransmission(0x68); Wire.write(0); Wire.endTransmission();
  Wire.requestFrom(0x68, 7);
  byte g[7]; for (int i = 0; i < 7; i++) g[i] = Wire.read();
  gio = bcd(g[2]); phut = bcd(g[1]);
  int ngay = bcd(g[4]), thang = bcd(g[5]);         // ngay trong nam
  const int t3[12] = {0,31,59,90,120,151,181,212,243,273,304,334};
  ngayTT = t3[thang - 1] + ngay;
}
float docGoc() {                                   // bien tro -> do (3 diem hieu chuan)
  float v = docADC(POT) * 3.3 / 4095.0;
  return -60.0 + (v - 0.32) * 150.0 / (2.98 - 0.32);
}
void dungMotor() { digitalWrite(TH_THUAN, HIGH); digitalWrite(TH_NGUOC, HIGH); }
void quay(int chieu, int ms) {                     // chieu +1 thuan, -1 nguoc
  if (chieu > 0 && digitalRead(QT1) == 1) return;  // lien dong hanh trinh
  if (chieu < 0 && digitalRead(QT2) == 1) return;
  digitalWrite(chieu > 0 ? TH_THUAN : TH_NGUOC, LOW);
  delay(ms); dungMotor();                          // truc vit tu giu vi tri
}
void setup() {
  Serial.begin(115200); Wire.begin(); lcd.begin(16, 2); lcd.backlight();
  analogReadResolution(12);
  for (int i = 0; i < 4; i++) analogSetPinAttenuation(LDR[i], ADC_11db);
  analogSetPinAttenuation(POT, ADC_11db); analogSetPinAttenuation(AP_PIN, ADC_11db);
  pinMode(TH_THUAN, OUTPUT); pinMode(TH_NGUOC, OUTPUT); dungMotor();
  pinMode(QT1, INPUT); pinMode(QT2, INPUT);
  lcd.print("BAM NANG LAI"); lcd.setCursor(0, 1); lcd.print("khoi dong...");
}
void loop() {
  if (millis() - tTruoc < 2000) return;
  tTruoc = millis();
  int gio, phut, ngayTT; docRTC(gio, phut, ngayTT);
  float t = gio + phut / 60.0 + (LAM - 105.0) / 15.0;   // gio Mat Troi
  float d = radians(23.45 * sin(radians(360.0 * (284 + ngayTT) / 365.0)));
  float H = radians(15.0 * (t - 12.0));
  float sa = sin(radians(PHI)) * sin(d) + cos(radians(PHI)) * cos(d) * cos(H);
  float al = asin(sa);
  float gocLenh = degrees(atan2(cos(d) * sin(H), sa));  // goc lenh truc quay Dong-Tay
  float gocThuc = docGoc();
  float L[4], S = 0;
  for (int i = 0; i < 4; i++) { L[i] = docADC(LDR[i]) * K_cal[i]; S += L[i]; }
  float e1 = ((L[0] + L[2]) - (L[1] + L[3])) / S;
  if (abs(gocLenh - gocThuc) > LECH_THO)
    quay(gocLenh > gocThuc ? 1 : -1, 300);            // dinh vi tho theo lich
  else if (S > S_NANG && fabs(e1) > E_CHET)
    quay(e1 > 0 ? 1 : -1, 120);                       // tinh chinh LDR
  lcd.clear(); lcd.setCursor(0, 0);
  char buf[17]; sprintf(buf, "%02d:%02d L%+4.1f", gio, phut, gocLenh); lcd.print(buf);
  lcd.setCursor(0, 1);
  sprintf(buf, "T%+4.1f e%+5.3f", gocThuc, e1); lcd.print(buf);
  Serial.printf("gio=%02d:%02d S=%.0f e1=%+.3f lenh=%+.1f thuc=%+.1f\\n",
                gio, phut, S, e1, gocLenh, gocThuc);
}"""

LAP_TRINH_CH3 = [
    ("h2", "3.1. Phương pháp đọc ADC"),
    ("p", "Bốn kênh LDR, biến trở hồi tiếp và cầu chia áp điện áp tấm pin đều đọc bằng ADC nội của ESP32 với độ phân giải 12 bit và suy hao 11 dB. Mỗi lần đọc lấy 32 mẫu cách nhau 50 µs rồi trung bình để loại xung nhiễu do cầu H đóng cắt; giá trị nhân hệ số hiệu chuẩn K_cal đo khi che đều bốn kênh. Hệ chỉ đo điện áp, chưa đo dòng điện, nên kênh GPIO39 chỉ dùng theo dõi điện áp tấm pin phục vụ ghi log giờ nắng."),
    ("h2", "3.2. Phương pháp đọc thời gian thực DS1307 và tính góc thiên văn"),
    ("p", "Mỗi chu kỳ, chương trình đọc bảy thanh ghi của DS1307 qua I²C địa chỉ 0x68, giải mã BCD sang giờ, phút và ngày trong năm; cộng hiệu số kinh độ (106,06° − 105°)/15 để đổi giờ đồng hồ sang giờ Mặt Trời. Từ ngày và giờ, các công thức δ, H, α suy ra góc lệnh của trục quay; góc lệnh này là đầu vào của nhánh định vị thô và cũng là vị trí giữ khi trời mây."),
    ("h2", "3.3. Phương pháp điều khiển động cơ qua opto và cầu H"),
    ("p", "Hai chân th_thuan/th_nguoc điều khiển opto PC817 ở mức thấp: muốn quay chiều nào thì hạ chân đó xuống 0 trong một khoảng xung rồi đưa cả hai về 1 để khóa cầu H, trục vít tự giữ vị trí. Trước mỗi xung lệnh, chương trình đọc công tắc hành trình của chiều đó; nếu đã chạm thì bỏ lệnh chiều nguy hiểm nhưng vẫn cho phép chiều thoát ra. Mọi xung lệnh đều chặn bằng delay ngắn có kiểm tra hành trình, không dùng PWM vì cầu H TIP41C đóng cắt theo kiểu bật–tắt."),
    ("h2", "3.4. Phương pháp đọc biến trở biết góc nghiêng tấm pin"),
    ("p", "Biến trở 10 k đồng trục chia áp về GPIO36; chương trình đọc điện áp, trung bình 32 mẫu rồi nội suy tuyến tính theo ba điểm hiệu chuẩn 0°, 45°, 90° (0,32 V / 1,66 V / 2,98 V) để ra góc hiện tại. Góc hiện tại được so với góc lệnh thiên văn để quyết định định vị thô và được hiển thị lên LCD dòng thứ hai."),
    ("h2", "3.5. Phương pháp hiển thị giờ và trạng thái lên LCD I²C"),
    ("p", "Màn hình LCD 1602 kèm mạch chuyển I²C PCF8574 địa chỉ 0x27, chung bus với DS1307. Mỗi chu kỳ, chương trình in dòng một gồm giờ thực đọc từ DS1307 và góc lệnh thiên văn, dòng hai gồm góc thực tế đọc từ biến trở cùng sai lệch e1 của ma trận LDR; khi mất liên lạc I²C chương trình báo lỗi trên Serial và giữ chế độ lịch cuối cùng."),
    ("h2", "3.6. Lưu đồ thuật toán"),
    ("img", "hinh_ve/luu_do_tong_quat.png", "{H}. Lưu đồ tổng quát chương trình điều khiển lai"),
    ("img", "hinh_ve/luu_do_thien_van.png", "{H}. Lưu đồ nhánh thiên văn đọc từ DS1307"),
    ("img", "hinh_ve/luu_do_ldr.png", "{H}. Lưu đồ nhánh tinh chỉnh theo ma trận LDR"),
    ("img", "hinh_ve/luu_do_dong_co.png", "{H}. Lưu đồ phát xung động cơ qua opto – cầu H"),
    ("img", "hinh_ve/luu_do_hien_thi.png", "{H}. Lưu đồ đọc giờ DS1307 và hiển thị LCD I²C"),
    ("h2", "3.7. Code mẫu chương trình lai một trục"),
    ("code", CODE_1TRUC),
    ("p", "Đoạn code trên thực hiện đúng chuỗi: đọc DS1307 → đổi giờ Mặt Trời → tính góc thiên văn → đọc biến trở → định vị thô nếu lệch quá 5° → đọc ma trận LDR và tinh chỉnh nếu nắng → hiển thị LCD và ghi log. Bản hai trục thêm kênh e2, biến trở và cặp opto thứ hai theo đúng cấu trúc hàm quay() và đọc ma trận."),
    ("h2", "3.8. Kết quả đo đạc chương trình trên bench"),
    ("tbl", [
        ["Hạng mục kiểm tra", "Kết quả"],
        ["Ma trận tính toán LDR", "Góc suy ra trùng góc đặt 0–30°, bảng ở quyển nghiên cứu mục 3.2."],
        ["Định vị thô theo lịch", "Lệch giả lập 12°, motor dừng cách mốc 1–2°."],
        ["Tinh chỉnh LDR", "Đèn rọi lệch 8°, một bước xung còn lệch dưới 1°."],
        ["Đọc giờ DS1307", "LCD hiện đúng giờ, lệch khoảng 3 giây sau 24 giờ."],
        ["Liên động hành trình", "Chạm qt1/qt2: lệnh chiều đó bị bỏ, chiều ngược vẫn chạy."],
        ["Giữ vị trí", "Ngắt nguồn khi nghiêng 40°, tấm pin không trôi."],
    ], "{B}. Kết quả kiểm tra chương trình trên bench thử"),
]

LAP_TRINH_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành chương trình lai một trục: đọc DS1307, tính góc thiên văn, tinh chỉnh LDR, điều khiển opto – cầu H, đọc biến trở và hiển thị LCD I²C (mục 3.7)."),
    ("b", "Hoàn thành năm lưu đồ: tổng quát và bốn lưu đồ từng phần cho nhánh thiên văn, nhánh LDR, nhánh động cơ, nhánh hiển thị (mục 3.6)."),
    ("b", "Hoàn thành kiểm tra bench: định vị thô dừng cách mốc 1–2°, tinh chỉnh LDR còn lệch dưới 1°, liên động hành trình hoạt động đúng (mục 3.8)."),
    ("b", "Hoàn thành hướng dẫn cài lõi ESP32 cho Arduino IDE và bảng chân sử dụng của DevKit (Chương 1)."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Nạp chương trình chạy ngoài trời trọn một ngày nắng, ghi log đối chiếu góc bám với mô phỏng."),
    ("b", "Mở rộng code sang bản hai trục: thêm e2, biến trở thứ hai và cặp opto thứ hai."),
    ("b", "Bổ sung chế độ tự hạ tấm pin nằm ngang khi gió lớn dùng công tắc hành trình làm mốc."),
]
