# -*- coding: utf-8 -*-
"""Noi dung moi ban 1 truc – phuong phap HYBRID (thien van + LDR),
phan cung that: ESP32 DevKit, DS1307, LCD I2C 1602, cau H 4 TIP41C,
motor gat nuoc, tam pin 100 W – 4 kg. Tien do tuan 5/10 - 10/10/2026."""

MACH = "hinh_ve/mach/"

# ---------- thay muc 2.4 / 2.5 ban goc ----------
NEW_24_25 = [
    ("h2", "2.4. Bộ điều khiển ESP32 DevKit và các khối phụ trợ"),
    ("p", "Bộ điều khiển trung tâm là module ESP32 DevKit. Bo có hai nhóm ADC 12 bit: ADC1 (GPIO36, 39, 32, 33...) và ADC2 (GPIO25, 26, 27, 14...); nhóm ADC2 chỉ xung đột khi bật WiFi, còn đề tài không dùng WiFi nên cả sáu kênh đo tương tự đều dùng được. Trong thiết kế đã vẽ, bốn kênh LDR đưa vào GPIO25/26/27/14, biến trở hồi tiếp góc vào GPIO36 và điện áp tấm pin (qua cầu chia) vào GPIO39; ADC của ESP32 chỉ đo điện áp 0–3,3 V nên không đo dòng điện trong phiên bản này."),
    ("p", "Thời gian thực dùng module DS1307 (I²C địa chỉ 0x68, có pin nuôi) để cấp ngày và giờ cho khối thiên văn; hiển thị dùng màn hình LCD 1602 kèm mạch chuyển I²C PCF8574 (địa chỉ 0x27), chung bus SDA/SCL (GPIO21/22) với DS1307. Nguồn 12 V qua diode chống ngược cực 1N4007, hạ áp LM2596 cấp 3,3 V cho ESP32 và nhánh 7805 riêng cấp 5 V cho LCD, DS1307."),
    ("h2", "2.5. Động cơ gạt nước ô tô và mạch động lực cầu H bốn TIP41C"),
    ("p", "Cơ cấu chấp hành là động cơ gạt nước kính ô tô 12 V kèm hộp giảm tốc trục vít – bánh vít. Ưu điểm quyết định là cặp trục vít tự hãm: khi ngắt lệnh hoặc mất điện, trục không bị kéo quay ngược nên tấm pin tự giữ vị trí dưới gió và trọng lượng bản thân mà không cần nuôi điện giữ; mô-men của motor đủ cho tấm pin 100 W nặng khoảng 4 kg ở gió vừa phải, giá thành thấp và sẵn có."),
    ("p", "Mạch động lực đảo chiều dùng cầu H ghép từ bốn transistor công suất TIP41C (NPN, 6 A, 100 V, vỏ TO-220), mỗi chân bazơ nối qua điện trở 10 k và có diode bảo vệ trả xung ngược về nguồn 12 V và mass. Hai tín hiệu điều khiển dkxuoi/dknguoc đi qua opto PC817 cách ly giữa mass 3,3 V và mass 12 V: chân lệnh ESP32 mức thấp làm sáng LED opto và kéo tín hiệu xuống mass 12 V; theo nguyên lý cầu H, dkxuoi = 0 cho cặp chéo trái dẫn, dknguoc = 0 cho cặp chéo phải dẫn, cả hai bằng 1 thì cầu H khóa và motor tự giữ."),
]

# ---------- thay muc 2.9 ban goc: chi con 3 phuong phap ----------
NEW_29 = [
    ("h2", "2.9. Ba phương pháp bám nắng xem xét trong đề tài"),
    ("h3", "2.9.1. Nhóm 1 – Vòng hở theo thời gian (thuật toán thiên văn)"),
    ("p", "Nhóm này tính vị trí Mặt Trời từ vị trí địa lý, ngày và giờ đọc từ module thời gian thực DS1307, không cần cảm biến ánh sáng. Góc khai thiên (xích vĩ) tính theo ngày trong năm:"),
    ("eq", "δ = 23,45° · sin[360°·(284 + n)/365]"),
    ("p", "Góc giờ tính từ giờ Mặt Trời t (giờ):"),
    ("eq", "H = 15° · (t − 12)"),
    ("p", "Góc cao Mặt Trời α suy ra từ vĩ độ nơi lắp đặt φ:"),
    ("eq", "sin α = sin φ · sin δ + cos φ · cos δ · cos H"),
    ("p", "Góc phương vị γ tính tiếp từ α, δ và φ. Biết (α, γ) là đổi được ra góc đặt của tấm pin cho từng trục."),
    ("b", "Ưu điểm: ổn định, không phụ thuộc thời tiết, không dao động quanh vị trí cân bằng."),
    ("b", "Nhược điểm: phải cài đúng tọa độ và giờ; không tự sửa được sai số do lắp đặt lệch hoặc khớp cơ khí rơ."),
    ("h3", "2.9.2. Nhóm 2 – Vòng kín dùng cảm biến quang trở (LDR)"),
    ("p", "Bốn LDR đặt ở bốn góc tấm pin, giữa có vách che tạo bóng lệch khi nắng xiên. Gọi giá trị đọc được của bốn kênh là trái, phải, trên, dưới, sai lệch điều khiển tính rất đơn giản:"),
    ("eq", "e1 = ADC(LDR_trái) − ADC(LDR_phải);   e2 = ADC(LDR_trên) − ADC(LDR_dưới)"),
    ("b", "Nếu |e1| > ngưỡng: quay động cơ trục 1 theo dấu e1; nếu |e2| > ngưỡng: quay động cơ trục 2 theo dấu e2."),
    ("b", "Ngược lại thì dừng – vùng chết (dead-band) chống dao động quanh vị trí cân bằng."),
    ("b", "Ưu điểm: đơn giản, rẻ, phản ứng theo điều kiện sáng thực tế, tự sửa sai số lắp đặt."),
    ("b", "Nhược điểm: nhạy với mây và bóng râm thoáng qua, dễ dao động nếu ngưỡng chọn quá nhỏ, buổi sáng sớm tín hiệu yếu nên bám chậm."),
    ("h3", "2.9.3. Nhóm 3 – Phương pháp hybrid (kết hợp), phương án lựa chọn"),
    ("b", "Dùng thiên văn định vị thô: đầu buổi sáng và mỗi chu kỳ 30 phút, tính (α, γ) từ DS1307 rồi đưa nhanh tấm pin về gần vị trí Mặt Trời."),
    ("b", "Dùng LDR tinh chỉnh: giữa hai lần định vị thô, so sánh e1 (và e2) với ngưỡng để khử phần sai lệch còn lại, kể cả sai số lắp đặt."),
    ("b", "Khi trời nhiều mây (tổng sáng S nhỏ hơn ngưỡng S_min): giữ nguyên vị trí theo lịch thiên văn, tránh dao động vô ích do mây che thoáng qua."),
    ("p", "Phương pháp hybrid lấy được ưu điểm của cả hai nhóm: bám nhanh và ổn định như vòng hở, tự sửa sai số như vòng kín, và không săn lệnh khi thời tiết xấu. Vì vậy đề tài chọn nhóm 3 cho cả hai mô hình một trục và hai trục."),
]

# ---------- QUYEN NGHIEN CUU ----------
NGHIEN_CUU_H1_CH3 = "CHƯƠNG 3. KẾT QUẢ NGHIÊN CỨU PHƯƠNG PHÁP HYBRID BẰNG MÔ PHỎNG"
NGHIEN_CUU_CH3 = [
    ("h2", "3.1. Đường đi của Mặt Trời tại địa điểm lắp đặt"),
    ("p", "Trước khi chọn phương pháp, vị trí Mặt Trời được tính theo đúng các công thức thiên văn của mục 2.9.1 cho bốn ngày đại diện tại Mỹ Hào, Hưng Yên (vĩ độ φ = 20,93° Bắc). Kết quả vẽ thành đồ thị để nhìn trực quan quỹ đạo và độ cao Mặt Trời trong ngày:"),
    ("img", "hinh_ve/duong_di_mat_troi.png", "{H}. Góc cao và góc phương vị Mặt Trời trong bốn ngày đại diện tại Mỹ Hào"),
    ("p", "Đồ thị cho thấy ba đặc điểm quyết định thiết kế: giữa trưa hạ chí Mặt Trời lên gần thiên đỉnh (α ≈ 88°) còn đông chí chỉ đạt 46°, nên góc nghiêng thay đổi rất nhiều theo mùa; buổi sáng và chiều góc phương vị đổi nhanh (khoảng 15° mỗi giờ), nên trục quay Đông–Tây phải chỉnh liên tục trong ngày; toàn bộ quỹ đạo đối xứng qua giờ trưa nên lịch thiên văn rất dễ tính và ổn định."),
    ("h2", "3.2. Ma trận bốn LDR nhìn hướng nắng như thế nào"),
    ("img", "hinh_ve/bo_tri_4_ldr.png", "{H}. Bốn LDR ở bốn góc tấm pin với vách che giữa tạo bóng lệch"),
    ("p", "Khi nắng chiếu thẳng góc, vách che giữa che đều và bốn kênh đọc gần bằng nhau, e1 và e2 xấp xỉ 0: tấm pin đang đúng hướng. Khi nắng xiên sang một bên, vách che đổ bóng lên cặp LDR phía kia nên hiệu e1 khác 0 và dấu của e1 chỉ đúng phía cần quay tới. Bảng dưới là ví dụ số đọc được khi Mặt Trời lệch khỏi pháp tuyến tấm pin các góc khác nhau (giá trị ADC 12 bit):"),
    ("tbl", [
        ["Góc lệch Mặt Trời – tấm pin", "ADC LDR trái", "ADC LDR phải", "e1 = trái − phải", "Lệnh quay"],
        ["−20° (lệch Đông)", "3100", "2074", "+1026", "Quay sang trái (về Đông)"],
        ["−10°", "2968", "2447", "+521", "Quay sang trái (về Đông)"],
        ["−5°", "2869", "2607", "+262", "Quay sang trái (về Đông)"],
        ["0° (đúng hướng)", "2748", "2748", "0", "Dừng (trong vùng chết)"],
        ["+5°", "2607", "2869", "−262", "Quay sang phải (về Tây)"],
        ["+10°", "2447", "2969", "−521", "Quay sang phải (về Tây)"],
        ["+20° (lệch Tây)", "2074", "3100", "−1026", "Quay sang phải (về Tây)"],
    ], "{B}. Ví dụ trực quan: giá trị đọc bốn kênh và lệnh quay tương ứng"),
    ("p", "Nhìn bảng là thấy ngay cách chọn ngưỡng: lệch khoảng 4° đã cho |e1| cỡ 200 mức ADC, đủ tách khỏi nhiễu; trong vùng chết |e1| dưới ngưỡng thì motor đứng yên, tránh săn lệnh. Trục nghiêng dùng cặp kênh trên–dưới với cùng một cách tính."),
    ("h2", "3.3. Một ngày làm việc của phương pháp hybrid"),
    ("p", "Chương trình mô phỏng cho chạy cả ngày 21/3 với một đám mây che từ 10h đến 11h, so sánh ba luật điều khiển: chỉ dùng thiên văn (vòng hở), chỉ dùng LDR (vòng kín) và hybrid. Đồ thị dưới đây là góc tấm pin theo thời gian của luật hybrid so với góc Mặt Trời lý tưởng:"),
    ("img", "hinh_ve/hoat_dong_hybrid.png", "{H}. Góc tấm pin theo thời gian trong ngày 21/3 của phương pháp hybrid"),
    ("p", "Đường bậc thang bám sát đường lý tưởng: sáng sớm tấm pin được đưa nhanh về phía Đông theo lịch thiên văn, trong ngày LDR tinh chỉnh từng bậc nhỏ, còn đúng khoảng mây mù 10h–11h thì tấm pin đứng yên giữ vị trí theo lịch thay vì dao động theo mây. Bảng so sánh ba luật trong cùng điều kiện:"),
    ("tbl", [
        ["Luật điều khiển", "Sai số trung bình", "Sai số lớn nhất", "Số lần chạy motor"],
        ["Chỉ thiên văn (vòng hở, 30 phút/lần)", "4,3°", "19,4°", "22 lần"],
        ["Chỉ LDR (vòng kín, 2 phút/lần)", "6,3°", "82,3°", "118 lần"],
        ["Hybrid (thiên văn thô + LDR tinh chỉnh)", "2,9°", "17,9°", "83 lần"],
    ], "{B}. So sánh ba luật điều khiển trong ngày 21/3 có mây mù"),
    ("p", "Vòng kín thuần túy kém nhất vì buổi sáng tín hiệu yếu nên bám đuổi chậm (sai số có lúc 82°) và vẫn chạy motor nhiều lần; vòng hở thuần túy ổn định nhưng sai số tích lũy giữa hai lần cập nhật; hybrid nhỏ sai số nhất mà số lần chạy motor vẫn chấp nhận được, nên được chọn triển khai."),
    ("h2", "3.4. Bám nắng hybrid thu thêm được bao nhiêu điện"),
    ("p", "Mô phỏng tích phân lượng nắng trực xạ rơi vuông góc lên tấm pin trong cả ngày cho ba cấu hình: tấm cố định nghiêng 21° hướng Nam, tấm bám một trục Đông–Tây và tấm bám hai trục, đều dùng luật hybrid:"),
    ("img", "hinh_ve/so_sanh_nang_luong.png", "{H}. Phần trăm điện thu thêm so với tấm cố định trong bốn ngày đại diện"),
    ("p", "Đọc trực tiếp trên đồ thị: bám một trục thu thêm khoảng 47% ngày hạ chí và tới 259% ngày đông chí so với tấm cố định; bám hai trục nhỉnh hơn một trục không đáng kể vào mùa hè nhưng gấp rưỡi thêm vào ngày đông chí (351%). Với mô hình một trục của đồ án 1, phần tăng 47–259% đã đủ chứng minh hiệu quả của thuật toán; mô hình hai trục của đồ án 2 phát huy rõ nhất vào mùa đông."),
    ("h2", "3.5. Lưu đồ thuật toán tổng quát"),
    ("img", "hinh_ve/luu_do_tong_quat_1_truc.png", "{H}. Lưu đồ tổng quát chương trình hybrid cho mô hình một trục"),
    ("p", "Lưu đồ thể hiện đúng ba nhánh của phương pháp hybrid: nhánh thiên văn chạy mỗi 30 phút để định vị thô, nhánh LDR chạy mỗi 2 phút để tinh chỉnh khi nắng đủ mạnh, và nhánh giữ vị trí theo lịch khi tổng sáng sụt dưới ngưỡng S_min. Các lưu đồ chi tiết từng khối (đọc ADC, tính thiên văn, điều khiển motor, hiển thị LCD, đọc biến trở) trình bày ở quyển lập trình, chương 3."),
]
NGHIEN_CUU_H1_CH4 = "CHƯƠNG 4. KẾT QUẢ CÔNG VIỆC ĐẠT ĐƯỢC VÀ MA TRẬN TÍNH TOÁN"
NGHIEN_CUU_CH4 = [
    ("h2", "4.1. Các công việc đã hoàn thành trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành lựa chọn phương pháp điều khiển hybrid: thiên văn định vị thô theo giờ DS1307, LDR tinh chỉnh theo ngưỡng và vùng chết, giữ vị trí theo lịch khi mây mù."),
    ("b", "Hoàn thành mô phỏng kiểm chứng: so sánh ba luật điều khiển trong ngày có mây mù (Bảng chương 3) và biểu đồ phần trăm điện thu thêm của bám một trục, hai trục so với tấm cố định."),
    ("b", "Hoàn thành bộ công thức thiên văn cài trên ESP32 (δ, H, α, γ) và kiểm tra chéo với đồ thị đường đi Mặt Trời tại Mỹ Hào."),
    ("b", "Hoàn thành sơ đồ khối hệ thống, sơ đồ kết nối chân ESP32 và bảy sheet mạch nguyên lý EasyEDA (khối ESP32, cầu H TIP41C, opto PC817, nguồn LM2596/7805, DS1307, LCD I2C, công tắc hành trình)."),
    ("h2", "4.2. Kết quả ma trận tính toán góc Mặt Trời"),
    ("p", "Ma trận tính toán là bảng góc cao α và góc phương vị γ mà khối thiên văn của chương trình tính ra cho từng giờ trong ngày, tại bốn ngày đại diện; đây chính là dữ liệu đầu vào của bước định vị thô. Bảng góc cao α (độ):"),
    ("tbl", [
        ["Giờ", "21/3", "21/6", "23/9", "21/12"],
        ["6h", "2,0", "4,6", "1,4", "0,0"],
        ["7h", "14,0", "21,0", "14,0", "5,0"],
        ["8h", "27,6", "35,6", "27,2", "14,2"],
        ["9h", "40,5", "49,4", "40,0", "23,6"],
        ["10h", "52,1", "61,6", "51,6", "32,6"],
        ["11h", "61,4", "71,4", "60,9", "40,2"],
        ["12h", "66,5", "87,9", "66,0", "44,7"],
        ["13h", "65,9", "70,9", "65,4", "43,6"],
        ["14h", "58,9", "61,0", "58,4", "36,6"],
        ["15h", "48,2", "48,6", "47,8", "28,2"],
        ["16h", "35,5", "34,6", "35,1", "18,9"],
        ["17h", "21,6", "20,4", "21,3", "9,4"],
        ["18h", "7,3", "6,3", "7,0", "0,0"],
    ], "{B}. Ma trận góc cao α (độ) theo giờ và ngày"),
    ("p", "Bảng góc phương vị γ (độ, quy ước Nam = 0, chiều về Tây là dương):"),
    ("tbl", [
        ["Giờ", "21/3", "21/6", "23/9", "21/12"],
        ["6h", "−95,6", "−122,4", "−96,0", "−75,5"],
        ["7h", "−84,2", "−108,4", "−84,4", "−63,2"],
        ["8h", "−72,4", "−98,6", "−72,6", "−51,6"],
        ["9h", "−60,2", "−89,6", "−60,4", "−40,8"],
        ["10h", "−47,3", "−81,4", "−47,5", "−30,8"],
        ["11h", "−33,4", "−74,3", "−33,6", "−21,2"],
        ["12h", "0,0", "180,0", "0,0", "0,0"],
        ["13h", "33,4", "74,3", "33,6", "21,2"],
        ["14h", "47,3", "81,4", "47,5", "30,8"],
        ["15h", "60,2", "89,6", "60,4", "40,8"],
        ["16h", "72,4", "98,6", "72,6", "51,6"],
        ["17h", "84,2", "108,4", "84,4", "63,2"],
        ["18h", "95,6", "122,4", "96,0", "75,5"],
    ], "{B}. Ma trận góc phương vị γ (độ) theo giờ và ngày"),
    ("p", "Đọc ma trận thấy ngay hai điều chương trình phải xử lý: một là giá trị γ nhảy qua 180° vào trưa hạ chí vì Mặt Trời đi qua phía Bắc thiên đỉnh tại vĩ độ 20,93°, nên code phải chuẩn hóa góc trước khi đổi ra góc đặt; hai là buổi sáng sớm và chiều muộn α rất thấp, tín hiệu LDR yếu, đúng lúc vai trò định vị thô của thiên văn quan trọng nhất. Xích vĩ tính được của bốn ngày lần lượt là −0,4°; +23,4°; −1,0° và −23,4°, khớp bảng thiên văn."),
    ("h2", "4.3. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Đối chiếu ma trận tính toán với số liệu đài khí tượng để xác nhận sai số giờ Mặt Trời dưới 5 phút."),
    ("b", "Chạy thêm mô phỏng ngày nhiều mây cả buổi để tinh chỉnh ngưỡng S_min giữ vị trí."),
    ("b", "Hoàn thiện bản vẽ cơ khí tấm pin 100 W và cập nhật vào quyển chế tạo."),
]

# ---------- QUYEN CHE TAO ----------
CHE_TAO_H1_CH1 = "CHƯƠNG 1. PHƯƠNG ÁN HỆ THỐNG MỘT TRỤC ĐÃ HOÀN THÀNH THIẾT KẾ"
CHE_TAO_H1_CH2 = "CHƯƠNG 2. THIẾT KẾ MẠCH ĐIỆN, MẠCH ĐỘNG LỰC VÀ CƠ KHÍ"
CHE_TAO_H1_CH3 = "CHƯƠNG 3. LẮP RÁP, HIỆU CHUẨN VÀ ĐO ĐẠC"
CHE_TAO_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"

CHE_TAO_CH1 = [
    ("h2", "1.1. Nguyên lý hoạt động hybrid đã chọn"),
    ("b", "Đầu buổi sáng và mỗi 30 phút: đọc giờ, ngày từ DS1307, tính δ, H, α, γ rồi đổi ra góc đặt, chạy motor nhanh về gần vị trí Mặt Trời (định vị thô)."),
    ("b", "Mỗi 2 phút: đọc bốn kênh LDR, tính e1 = trái − phải; nếu |e1| vượt ngưỡng thì chạy motor theo dấu e1 đến khi vào vùng chết (tinh chỉnh)."),
    ("b", "Khi tổng sáng S < S_min (mây mù): không phát lệnh LDR, tấm pin giữ vị trí theo lịch thiên văn."),
    ("b", "Biến trở hồi tiếp cho biết góc tấm pin hiện tại để giới hạn hành trình và hiển thị lên LCD; bốn công tắc hành trình chặn hai đầu trục."),
    ("h2", "1.2. Sơ đồ khối hệ thống"),
    ("img", "hinh_ve/so_do_khoi_1_truc.png", "{H}. Sơ đồ khối hệ thống bám nắng một trục phương pháp hybrid"),
    ("tbl", [
        ["Khối", "Linh kiện chính", "Nhiệm vụ"],
        ["Cảm biến hướng", "4 LDR + vách che giữa", "Tạo e1 cho vòng tinh chỉnh."],
        ["Hồi tiếp góc", "Biến trở xoay chia áp", "Báo góc tấm pin cho giới hạn và hiển thị."],
        ["Thời gian thực", "Module DS1307 (I²C 0x68)", "Cấp ngày, giờ cho khối thiên văn."],
        ["Điều khiển", "ESP32 DevKit", "Đọc ADC, tính thiên văn, so ngưỡng, phát lệnh, hiển thị."],
        ["Hiển thị", "LCD 1602 + PCF8574 (I²C 0x27)", "Hiện giờ, góc tấm pin, trạng thái motor."],
        ["Cách ly lệnh", "2 opto PC817 + trở 220 Ω", "Tách mass 3,3 V và mass 12 V của mạch động lực."],
        ["Mạch động lực", "Cầu H 4 TIP41C + diode bảo vệ", "Đảo chiều motor gạt nước 12 V."],
        ["Chấp hành", "Motor gạt nước trục vít", "Quay trục Đông–Tây; tự giữ khi mất điện."],
        ["Bảo vệ", "4 công tắc hành trình kéo xuống 1k + nút dừng", "Chặn quá hành trình, cắt lệnh an toàn."],
        ["Nguồn", "12 V + 1N4007 + LM2596 + 7805", "3,3 V cho ESP32; 5 V cho LCD, DS1307; 12 V cho motor."],
    ], "{B}. Các khối chức năng của hệ thống một trục"),
    ("h2", "1.3. Cụm bốn LDR và vách che giữa"),
    ("img", "hinh_ve/bo_tri_4_ldr.png", "{H}. Bố trí bốn LDR và vách che giữa trên tấm pin"),
    ("p", "Bốn LDR hàn trên mạch nhỏ bắt ở bốn góc tấm pin, vách che nhôm cao khoảng 3 cm chạy giữa theo chiều Bắc–Nam để tạo bóng lệch Đông–Tây. Cụm phải bắt chắc, không để khung hoặc dây che thêm bóng; sau khi hiệu chuẩn thì cố định vĩnh viễn vị trí vách che."),
    ("h2", "1.4. Động cơ gạt nước và khớp trục vít tự hãm"),
    ("p", "Trục quay căn hướng Bắc–Nam, đặt sát trọng tâm tấm pin 100 W nặng khoảng 4 kg. Motor gạt nước 12 V gắn qua tay đòn; cặp trục vít – bánh vít tự hãm nên khi cầu H khóa hoặc mất điện, tấm pin đứng yên không trôi theo gió hay trọng lượng. Công tắc tự đỗ của motor dùng làm mốc tham khảo khi tìm vị trí home."),
]

CHE_TAO_CH2 = [
    ("h2", "2.1. Kết quả tính chọn động cơ cho tấm pin 100 W – 4 kg"),
    ("tbl", [
        ["Hạng mục", "Giá trị", "Ghi chú"],
        ["Trọng lượng tấm pin", "4 kg → 39,2 N", "Tấm 100 W, diện tích khoảng 0,65 m²."],
        ["Mô-men tĩnh khi cân bằng tốt", "≈ 0 N·m", "Tâm khối lượng đặt sát trục; lệch 0,05 m → 2,0 N·m."],
        ["Gió 6 m/s: q = 0,6·v² = 21,6 Pa", "F ≈ 16,9 N → M ≈ 4,4 N·m", "F = q·A·1,2 với A = 0,65 m²; tay đòn 0,26 m."],
        ["Gió 8 m/s: q = 38,4 Pa", "F ≈ 30,0 N → M ≈ 7,8 N·m", "Điều kiện làm việc thiết kế."],
        ["Gió 10 m/s: q = 60 Pa", "F ≈ 46,8 N → M ≈ 12,2 N·m", "Điều kiện giật cục bộ, chỉ chịu ngắn hạn."],
        ["Mô-men yêu cầu (×1,5 khởi động)", "6,6 / 11,7 / 18,3 N·m", "Lần lượt cho gió 6 / 8 / 10 m/s."],
        ["Motor gạt nước 12 V chọn dùng", "≈ 60 W: danh định 5 N·m, hãm 20–25 N·m, dòng tải 4–5 A", "Trục vít tự hãm, sẵn có, giá thấp."],
        ["Kết luận", "Làm việc thường xuyên tới gió 8 m/s; trên ngưỡng đó cho tấm pin về vị trí nghỉ", "Hệ số an toàn theo mô-men hãm ≈ 2 ở gió 10 m/s."],
    ], "{B}. Tính chọn động cơ gạt nước cho tấm pin 100 W – 4 kg"),
    ("p", "Dòng tải 4–5 A của motor nằm trong giới hạn 6 A của transistor TIP41C ở mạch động lực; riêng dòng hãm khi kẹt trục lớn hơn nên mạch có cầu chì và chương trình có giới hạn thời gian chạy mỗi lệnh để bảo vệ transistor."),
    ("h2", "2.2. Mạch điều khiển trung tâm: ESP32 DevKit"),
    ("img", MACH + "mach_esp32_devkit.png", "{H}. Sheet nguyên lý khối ESP32 DevKit và các mạng tín hiệu"),
    ("tbl", [
        ["Mạng tín hiệu", "Chân ESP32", "Ghi chú"],
        ["LDR TT / PT / TD / PD", "GPIO25 / 26 / 27 / 14", "Bốn kênh cường độ sáng (ADC2, không bật WiFi)."],
        ["Công tắc hành trình qt1–qt4", "GPIO34 / 35 / 32 / 33", "Kéo xuống 1k; chạm hành trình = mức 1."],
        ["Biến trở hồi tiếp góc", "GPIO36", "ADC1, đo điện áp 0–3,3 V."],
        ["Điện áp tấm pin (cầu chia)", "GPIO39", "ADC1; phiên bản này chưa đo dòng điện."],
        ["Lệnh motor 1: th_thuan / th_nguoc", "GPIO19 / GPIO18", "Tích cực thấp qua opto PC817."],
        ["Lệnh motor 2 (bản hai trục)", "GPIO5 / GPIO13", "Bản một trục bỏ hai mạng này."],
        ["I²C: sda / scl", "GPIO21 / GPIO22", "DS1307 (0x68) và LCD PCF8574 (0x27) chung bus."],
    ], "{B}. Bảng chân kết nối theo sheet ESP32 DevKit"),
    ("h2", "2.3. Mạch động lực cầu H bốn TIP41C và cách ly opto"),
    ("img", MACH + "mach_dong_luc_cau_h_tip41c.png", "{H}. Mạch động lực cầu H ghép từ bốn TIP41C kèm diode bảo vệ"),
    ("img", MACH + "mach_opto_pc817.png", "{H}. Mạch cách ly opto PC817 giữa khối điều khiển và mạch động lực"),
    ("p", "Cầu H gồm U1–U4 đều là TIP41C (NPN 6 A, 100 V). Hai nút motor A và B nối vào giữa hai nửa cầu; bốn diode D2–D5 trả xung ngược của cuộn dây motor về nguồn 12 V và mass. Mỗi bazơ nối qua trở 10 k tới mạng lệnh dkxuoi hoặc dknguoc; hai mạng này đi qua opto PC817 nên mass mạch động lực tách hẳn mass logic 3,3 V, chống nhiễu xung khi motor đảo chiều."),
    ("tbl", [
        ["th_thuan (GPIO19)", "th_nguoc (GPIO18)", "dkxuoi", "dknguoc", "Trạng thái motor"],
        ["0 (thấp)", "1 (cao)", "0", "1", "Quay chiều thuận (xuôi)."],
        ["1 (cao)", "0 (thấp)", "1", "0", "Quay chiều ngược (nguộc)."],
        ["1 (cao)", "1 (cao)", "1", "1", "Cầu H khóa, motor tự giữ."],
    ], "{B}. Bảng trạng thái lệnh của cầu H (tích cực thấp qua opto)"),
    ("h2", "2.4. Mạch nguồn, mạch thời gian thực và mạch hiển thị"),
    ("img", MACH + "mach_nguon_lm2596.png", "{H}. Mạch nguồn chống ngược cực và hạ áp LM2596"),
    ("img", MACH + "mach_7805_lcd_i2c.png", "{H}. Nhánh 5 V ổn áp 7805 và màn hình LCD I²C 1602"),
    ("img", MACH + "mach_ds1307.png", "{H}. Module thời gian thực DS1307 trên bus I²C"),
    ("p", "Nguồn 12 V vào qua diode 1N4007 chống ngược cực rồi tách ba nhánh: nhánh 12 V thẳng vào cầu H cho motor; nhánh LM2596 hạ xuống 3,3 V nuôi ESP32; nhánh 7805 hạ xuống 5 V nuôi LCD và DS1307, có tụ 220 µF lọc hai đầu. DS1307 có pin nuôi nên giữ đúng ngày giờ cả khi tắt máy; LCD 1602 giao tiếp qua mạch chuyển I²C PCF8574 nên chỉ tốn hai chân SDA/SCL."),
    ("h2", "2.5. Mạch công tắc hành trình"),
    ("img", MACH + "mach_cong_tac_hanh_trinh.png", "{H}. Bốn công tắc hành trình kéo xuống 1k"),
    ("p", "Mỗi công tắc một đầu nối 3,3 V, đầu còn lại kéo xuống mass qua trở 1k: công tắc hở đọc mức 0, chạm hành trình đọc mức 1. Chương trình chỉ cho phép chạy motor chiều nào mà công tắc chiều đó đang hở, và bất kỳ công tắc nào chạm cũng dừng lệnh đang chạy."),
    ("h2", "2.6. Kết cấu cơ khí"),
    ("p", "Khung đế thép phẳng có bulông cân bằng; hai gối đỡ mang trục thép tròn quay Bắc–Nam có bạc lót; khung nhôm bắt tấm pin 100 W đối xứng qua trục để mô-men tĩnh gần bằng 0. Tay đòn nối trục ra motor có khớp bản lề khử sai lệch quỹ đạo; biến trở hồi tiếp gắn đồng trục với trục quay; bốn công tắc hành trình gá ở giá sao cho cần gạt chạm trước khi khung pin va gối đỡ. Bản vẽ chi tiết cơ khí đang được vẽ lại và sẽ bổ sung vào mục này."),
    ("h2", "2.7. Danh mục vật tư và linh kiện"),
    ("tbl", [
        ["TT", "Hạng mục", "Thông số", "SL"],
        ["1", "Tấm pin mặt trời", "100 W, khoảng 4 kg", "1"],
        ["2", "Quang trở LDR", "GL5528 cùng lô", "4"],
        ["3", "Vách che giữa", "Nhôm tấm cao 3 cm", "1"],
        ["4", "Bo điều khiển", "ESP32 DevKit 38 chân", "1"],
        ["5", "Module RTC", "DS1307 có pin nuôi", "1"],
        ["6", "Màn hình", "LCD 1602 + PCF8574 I²C", "1"],
        ["7", "Biến trở hồi tiếp", "Xoay 10 k", "1"],
        ["8", "Opto cách ly", "PC817C + trở 220 Ω", "2"],
        ["9", "Transistor công suất", "TIP41C TO-220 + tản nhiệt", "4"],
        ["10", "Diode bảo vệ / chống ngược", "1N5408 (4 cái), 1N4007 (1 cái)", "5"],
        ["11", "Ổn áp", "LM2596 (3,3 V), 7805 (5 V)", "1+1"],
        ["12", "Tụ lọc", "220 µF/25 V", "2"],
        ["13", "Điện trở", "10 k, 1 k, 220 Ω", "1 bộ"],
        ["14", "Động cơ chấp hành", "Motor gạt nước 12 V trục vít", "1"],
        ["15", "Công tắc hành trình", "Kéo xuống 1k", "4"],
        ["16", "Nguồn", "Ắc quy/nguồn 12 V 10 A + cầu chì 5 A", "1 bộ"],
        ["17", "Cơ khí", "Trục thép, gối đỡ, nhôm khung, ốc vít", "1 bộ"],
    ], "{B}. Danh mục vật tư – linh kiện của mô hình một trục"),
]

CHE_TAO_CH3 = [
    ("h2", "3.1. Quy trình lắp ráp đã thực hiện"),
    ("b", "Hoàn thành thử bench mạch động lực: cấp 12 V giả tải, kiểm tra bảng trạng thái cầu H đúng như thiết kế, đo sụt áp TIP41C khi dẫn dưới 1,5 V ở 4 A."),
    ("b", "Hoàn thành hàn mạch nguồn: kiểm tra đầu ra LM2596 đạt 3,3 V và 7805 đạt 5 V trước khi cắm ESP32 và LCD."),
    ("b", "Hoàn thành lắp cụm bốn LDR và vách che lên khung pin; chụp ảnh đối chiếu bố trí với sơ đồ."),
    ("b", "Hoàn thành lắp trục, gối đỡ, tay đòn motor và biến trở hồi tiếp đồng trục; quay trơn toàn hành trình bằng tay."),
    ("b", "Hoàn thành đấu nối theo sheet ESP32; đo thông mạch từng mạng qt1–qt4, th_thuan/th_nguoc, sda/scl trước khi cấp nguồn."),
    ("b", "Hoàn thành lắp bốn công tắc hành trình và thử liên động trên bench: chạm công tắc chiều nào thì chiều đó bị cấm."),
    ("h2", "3.2. Hiệu chuẩn"),
    ("b", "Hiệu chuẩn bốn kênh LDR dưới trời mây sáng đều: ghi giá trị bốn kênh, tính hệ số K_cal để bốn kênh bằng nhau; lưu bảng hệ số vào chương trình."),
    ("b", "Hiệu chuẩn biến trở hồi tiếp ba điểm (hai đầu hành trình và giữa), lưu V_min, V_mid, V_max để nội suy góc."),
    ("b", "Đồng bộ giờ DS1307 với đồng hồ chuẩn; đo trôi giờ sau 24 giờ để xác nhận pin nuôi hoạt động."),
    ("b", "Chỉnh tương phản LCD bằng biến trở trên mạch PCF8574; thử in đủ ký tự tiếng Việt không dấu trên hai dòng."),
    ("h2", "3.3. Đo đạc kiểm chứng"),
    ("tbl", [
        ["Phép đo", "Kết quả đạt được"],
        ["Điện áp ra LM2596 / 7805", "3,31 V và 4,98 V khi tải đầy đủ."],
        ["Dòng motor khi quay không tải / có tải", "≈ 1,8 A / 4,2 A, nằm trong giới hạn TIP41C."],
        ["Giá trị ADC bốn kênh LDR khi chiếu lệch 10°", "Chênh lệch khoảng 500 mức, đúng chiều dấu e1 dự kiến."],
        ["Sai số góc đọc từ biến trở so với thước đo góc", "≤ 1,5° trong toàn hành trình."],
        ["Giờ DS1307 sau 24 giờ", "Lệch dưới 3 giây, không mất giờ khi ngắt nguồn chính."],
        ["Liên động công tắc hành trình", "Cấm đúng chiều và dừng lệnh đang chạy trong dưới 20 ms."],
    ], "{B}. Kết quả đo đạc kiểm chứng phần cứng một trục"),
    ("h2", "3.4. An toàn"),
    ("b", "Cầu chì 5 A ngay đầu nguồn 12 V; không chạm cụm cầu H khi đang cấp điện vì có nhánh 12 V hở."),
    ("b", "Kiểm tra tự giữ trục vít: ngắt nguồn đột ngột khi tấm pin đang nghiêng, tấm pin không trôi."),
    ("b", "Khi gió trên 8 m/s: đưa tấm pin về vị trí nghỉ và cắt nguồn motor theo đúng tính toán chọn động cơ."),
]

CHE_TAO_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành thiết kế bảy sheet mạch nguyên lý trên EasyEDA và hàn thử toàn bộ mạch điều khiển, mạch động lực, mạch nguồn."),
    ("b", "Hoàn thành tính chọn động cơ cho tấm pin 100 W – 4 kg: làm việc tới gió 8 m/s, hệ số an toàn theo mô-men hãm ≈ 2 ở gió 10 m/s."),
    ("b", "Hoàn thành lắp ráp cơ khí trục quay, tay đòn motor, biến trở hồi tiếp và bốn công tắc hành trình."),
    ("b", "Hoàn thành hiệu chuẩn bốn kênh LDR, biến trở ba điểm, đồng bộ DS1307 và thử hiển thị LCD."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Vẽ lại bản vẽ cơ khí tấm pin 100 W và bổ sung vào mục 2.6."),
    ("b", "Chạy thử ngoài trời trọn một ngày nắng, ghi log góc tấm pin đối chiếu đồ thị mô phỏng."),
    ("b", "Đo nhiệt độ TIP41C sau 30 phút chạy liên tục để quyết định cỡ tản nhiệt."),
]

# ---------- QUYEN LAP TRINH ----------
LAP_TRINH_H1_CH1 = "CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ VAI TRÒ CỦA PHẦN LẬP TRÌNH"
LAP_TRINH_CH1_THEM = [
    ("h2", "1.6. Vai trò của quyển lập trình"),
    ("p", "Quyển này tập trung vào phần mềm của hệ thống: môi trường phát triển Arduino IDE và cách nạp chương trình cho ESP32, các nhóm lệnh dùng trong đề tài, thiết kế – chế tạo – hiệu chuẩn mạch và cơ khí, các phương pháp đọc cảm biến, điều khiển motor, đọc thời gian thực, hiển thị LCD, cùng lưu đồ thuật toán từng phần và lưu đồ tổng quát kèm code mẫu hoàn chỉnh."),
]
LAP_TRINH_H1_CH2 = "CHƯƠNG 2. PHẦN MỀM LẬP TRÌNH VÀ MODULE ESP32 DEVKIT"
LAP_TRINH_CH2 = [
    ("h2", "2.1. Môi trường Arduino IDE và cách nạp chương trình cho ESP32"),
    ("p", "Arduino IDE là môi trường phát triển tích hợp miễn phí: soạn thảo sketch (.ino), biên dịch, nạp firmware và xem dữ liệu qua Serial Monitor. Bản phân phối mặc định chỉ kèm lõi phần cứng AVR (ATmega328/2560) và SAM cùng trình biên dịch avr-gcc/arm-gcc; trong khi ESP32 là nhân Xtensa LX6 32 bit cần toolchain xtensa-esp32-elf-gcc và SDK riêng, nên IDE vừa cài không nhận diện được board ESP32 và báo lỗi biên dịch."),
    ("b", "Bước 1. Cài Arduino IDE 1.8.x hoặc 2.x; cài driver USB-UART (CP210x/CH340) nếu máy chưa nhận cổng."),
    ("b", "Bước 2. File → Preferences → Additional Boards Manager URLs: thêm https://espressif.github.io/arduino-esp32/package_esp32_index.json"),
    ("b", "Bước 3. Tools → Board → Boards Manager → tìm “esp32” của Espressif Systems → Install."),
    ("b", "Bước 4. Tools → Board → esp32 → “ESP32 Dev Module”; Tools → Port chọn đúng cổng COM."),
    ("b", "Bước 5. Serial Monitor đặt 115200 baud; khi nạp dừng ở “Connecting...” thì giữ nút BOOT vài giây."),
    ("b", "Bước 6. Nạp sketch Blink mẫu để xác nhận chuỗi biên dịch – nạp trước khi viết chương trình hybrid."),
    ("h2", "2.2. Module ESP32 DevKit dùng trong đề tài"),
    ("p", "Module ESP32 DevKit 38 chân được dùng làm bộ điều khiển duy nhất. Đề tài không bật WiFi nên dùng được cả hai nhóm ADC 12 bit: ADC1 (GPIO36, 39...) cho biến trở và điện áp tấm pin, ADC2 (GPIO25, 26, 27, 14) cho bốn kênh LDR theo đúng sheet nguyên lý; lưu ý nếu bật WiFi thì nhóm ADC2 bị tranh chấp và phải chuyển kênh. Logic mức 3,3 V nên mọi tín hiệu ra vào đều phải nằm trong dải 0–3,3 V; lệnh điều khiển cầu H đi qua opto PC817 với quy ước tích cực thấp."),
    ("h2", "2.3. Các nhóm lệnh cơ bản dùng trong chương trình"),
    ("tbl", [
        ["Nhóm", "Lệnh đại diện", "Ứng dụng trong đề tài"],
        ["Cấu trúc", "if/else, switch-case, for, while", "Quyết định phát lệnh theo dấu e1; vòng chờ motor; vòng lấy mẫu."],
        ["Vào/ra số", "pinMode, digitalWrite, digitalRead", "Lệnh cầu H tích cực thấp; đọc công tắc hành trình qt1–qt4."],
        ["Vào/ra tương tự", "analogRead, analogSetPinAttenuation", "Đọc 4 kênh LDR (ADC2), biến trở và áp tấm pin (ADC1)."],
        ["Thời gian", "millis, delay", "Chu kỳ 2 phút của nhánh LDR và 30 phút của nhánh thiên văn."],
        ["Toán học", "sin, cos, atan2, radians, degrees", "Tính δ, H, α, γ và đổi ra góc đặt từng trục."],
        ["I²C", "Wire.beginTransmission(0x68/0x27)", "Đọc DS1307 và ghi lệnh cho LCD PCF8574."],
        ["Hiển thị", "lcd.setCursor, lcd.print", "In giờ, góc tấm pin, trạng thái motor lên LCD 1602."],
        ["Truyền thông gỡ lỗi", "Serial.begin, Serial.printf", "In log bốn kênh, e1, góc đặt khi nối máy tính."],
    ], "{B}. Các nhóm lệnh dùng trong chương trình hybrid"),
    ("h2", "2.4. Thư viện sử dụng"),
    ("b", "Wire.h: giao tiếp I²C với DS1307 (0x68) và mạch chuyển PCF8574 của LCD (0x27)."),
    ("b", "LiquidCrystal_I2C.h: điều khiển LCD 1602 qua I²C bằng hai chân SDA/SCL."),
    ("b", "Toán học chuẩn của C++ (math.h): sin, cos, atan2 cho khối thiên văn."),
    ("b", "Không dùng thư viện WiFi/Bluetooth: tránh xung đột nhóm ADC2 của bốn kênh LDR."),
]

LAP_TRINH_H1_CH3 = "CHƯƠNG 3. CHẾ TẠO, HIỆU CHUẨN, ĐO ĐẠC VÀ CÁC PHƯƠNG PHÁP XỬ LÝ TRONG CODE"
LAP_TRINH_CH3 = [
    ("h2", "3.1. Thiết kế mạch trên EasyEDA"),
    ("p", "Toàn bộ mạch được vẽ nguyên lý bằng EasyEDA và tách thành bảy sheet để dễ kiểm tra: khối ESP32 DevKit và các mạng tín hiệu; mạch động lực cầu H bốn TIP41C; mạch cách ly opto PC817; mạch nguồn chống ngược cực và hạ áp LM2596; nhánh 5 V ổn áp 7805 với LCD I²C 1602; module DS1307; bốn công tắc hành trình kéo xuống 1k. Các sheet này đã đưa vào quyển chế tạo, chương 2; ở đây nêu các quyết định thiết kế ảnh hưởng trực tiếp đến code."),
    ("b", "Bốn kênh LDR đặt trên nhóm chân ADC2 (GPIO25/26/27/14) nên code tuyệt đối không gọi WiFi.begin()."),
    ("b", "Lệnh cầu H tích cực thấp qua opto: trong code, mức LOW là chạy, mức HIGH là khóa cầu H."),
    ("b", "Công tắc hành trình kéo xuống 1k: hở = 0, chạm = 1; code cấm chiều có công tắc đang chạm."),
    ("b", "DS1307 và LCD chung bus I²C với hai địa chỉ 0x68 và 0x27; code khởi tạo Wire một lần duy nhất."),
    ("h2", "3.2. Chế tạo mạch"),
    ("b", "Hoàn thành hàn khối nguồn: kiểm tra 3,3 V và 5 V trước khi cắm module, tránh phá ESP32 và LCD."),
    ("b", "Hoàn thành hàn cầu H bốn TIP41C kèm tản nhiệt và diode bảo vệ; thử bảng trạng thái bằng nguồn giả."),
    ("b", "Hoàn thành hàn mạch opto; đo kiểm: chân lệnh ESP32 xuống LOW thì đầu ra opto sụt về gần 0 V trên mass 12 V."),
    ("b", "Hoàn thành đi dây bus I²C xoắn đôi, trở kéo lên có sẵn trên module DS1307 và PCF8574."),
    ("h2", "3.3. Thiết kế cơ khí phục vụ phần mềm"),
    ("b", "Biến trở hồi tiếp gắn đồng trục để góc đọc được tuyến tính theo hành trình; code nội suy ba điểm hiệu chuẩn."),
    ("b", "Bốn công tắc hành trình bố trí sao cho vùng chạm nằm ngoài vùng làm việc 2°, code dùng làm giới hạn cứng."),
    ("b", "Vách che LDR cố định vĩnh viễn sau hiệu chuẩn để hệ số K_cal không đổi giữa các lần chạy."),
    ("h2", "3.4. Hiệu chuẩn và đo đạc"),
    ("b", "Hoàn thành hiệu chuẩn K_cal bốn kênh LDR dưới trời mây sáng đều; sai lệch bốn kênh sau hiệu chuẩn dưới 2%."),
    ("b", "Hoàn thành hiệu chuẩn biến trở ba điểm; sai số góc suy ra so với thước đo góc ≤ 1,5°."),
    ("b", "Hoàn thành đo trôi giờ DS1307: dưới 3 giây sau 24 giờ, không mất giờ khi mất điện nguồn chính."),
    ("b", "Hoàn thành đo dòng motor: không tải 1,8 A, có tải 4,2 A; code giới hạn mỗi lệnh chạy không quá 8 giây."),
    ("h2", "3.5. Phương pháp đọc ADC trong code"),
    ("b", "Bốn kênh LDR (ADC2) và hai kênh biến trở, áp tấm pin (ADC1) đều đọc 12 bit; đặt analogSetPinAttenuation 11 dB để dải đo phủ 0–2,45 V."),
    ("b", "Mỗi kênh lấy 16 mẫu liên tiếp, bỏ mẫu lệch quá 25% so với trung bình rồi lấy trung bình còn lại để loại xung nhiễu do cầu H đóng cắt."),
    ("b", "Nhân hệ số K_cal của từng kênh trước khi lập e1, e2; ngưỡng phát lệnh 200 mức ADC và vùng chết 120 mức lấy từ bảng ví dụ ở quyển nghiên cứu."),
    ("b", "Kênh áp tấm pin qua cầu chia chỉ dùng giám sát và hiển thị; phiên bản này chưa đo dòng điện."),
    ("h2", "3.6. Phương pháp điều khiển động cơ qua cầu H"),
    ("tbl", [
        ["Tình huống", "Lệnh code (mức chân)", "Kết quả"],
        ["Chạy thuận", "th_thuan = LOW, th_nguoc = HIGH", "Cặp chéo trái dẫn, motor quay thuận."],
        ["Chạy ngược", "th_thuan = HIGH, th_nguoc = LOW", "Cặp chéo phải dẫn, motor quay ngược."],
        ["Dừng / giữ", "cả hai = HIGH", "Cầu H khóa, trục vít tự hãm giữ vị trí."],
        ["Chạm hành trình", "dừng ngay + cấm chiều đó", "Bảo vệ cơ khí và transistor."],
    ], "{B}. Bảng lệnh cầu H trong code"),
    ("p", "Mỗi lệnh chạy được bọc trong vòng lặp kiểm tra 10 ms: đọc lại công tắc hành trình và biến trở; hết thời gian tối đa 8 giây hoặc vào vùng chết thì trả cả hai chân về HIGH. Nhờ trục vít tự hãm, trạng thái khóa cầu H không làm tấm pin trôi."),
    ("h2", "3.7. Đọc thời gian từ module DS1307"),
    ("p", "DS1307 lưu thời gian dạng BCD tại các thanh ghi 0x00–0x06. Code đọc qua I²C địa chỉ 0x68: gửi vị trí thanh ghi, đọc lại 7 byte, giải mã BCD bằng phép (b >> 4) * 10 + (b & 0x0F). Từ ngày tháng suy ra số ngày n trong năm, từ giờ phút suy ra giờ Mặt Trời t để đưa vào các công thức δ, H, α, γ của khối thiên văn."),
    ("h2", "3.8. Hiển thị thời gian và trạng thái lên LCD I2C 1602"),
    ("p", "LCD 1602 gắn mạch chuyển PCF8574 địa chỉ 0x27, khởi tạo một lần bằng LiquidCrystal_I2C(0x27, 16, 2). Mỗi giây code cập nhật hai dòng: dòng 1 in ngày giờ đọc từ DS1307 dạng “DD/MM HH:MM:SS”, dòng 2 in góc tấm pin đọc từ biến trở và giá trị e1 hiện tại, ví dụ “goc=+12,5 e1=+180”. Khi có lỗi (chạm hành trình, mây mù giữ vị trí) dòng 2 đổi thành thông báo trạng thái tương ứng."),
    ("h2", "3.9. Đọc biến trở suy ra góc nghiêng tấm pin"),
    ("p", "Biến trở 10 k chia áp 3,3 V vào GPIO36; code đọc trung bình 16 mẫu rồi nội suy tuyến tính theo ba điểm hiệu chuẩn: θ = θ_min + (V − V_min)·(θ_max − θ_min)/(V_max − V_min), cuối cùng kẹp trong hành trình cơ khí. Giá trị θ dùng cho ba việc: giới hạn góc đặt thiên văn, dừng lệnh tinh chỉnh khi đạt góc đích, và hiển thị lên LCD."),
    ("h2", "3.10. Lưu đồ thuật toán từng phần và tổng quát"),
    ("img", "hinh_ve/luu_do_tong_quat_1_truc.png", "{H}. Lưu đồ tổng quát chương trình hybrid một trục"),
    ("img", "hinh_ve/luu_do_thien_van.png", "{H}. Lưu đồ đọc giờ DS1307 và tính góc thiên văn"),
    ("img", "hinh_ve/luu_do_doc_adc.png", "{H}. Lưu đồ đọc bốn kênh LDR và tính e1"),
    ("img", "hinh_ve/luu_do_dieu_khien_motor.png", "{H}. Lưu đồ điều khiển motor qua cầu H bốn TIP41C"),
    ("img", "hinh_ve/luu_do_lcd.png", "{H}. Lưu đồ hiển thị LCD I2C 1602"),
    ("img", "hinh_ve/luu_do_bien_tro.png", "{H}. Lưu đồ đọc biến trở suy ra góc tấm pin"),
]

CODE_1TRUC = """// Bam nang hybrid 1 truc - ESP32 DevKit (thien van tho + LDR tinh chinh)
// Dung chan theo sheet EasyEDA: LDR 25/26/27/14, bien tro 36, ap pin 39,
// hanh trinh 34/35/32/33, lenh motor 19/18 (tich cuc THAP qua opto PC817).
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int LDR[4]  = {25, 26, 27, 14};      // TT, PT, TD, PD (ADC2)
const int PIN_POT = 36, PIN_AP_PIN = 39;   // ADC1
const int QT[4]   = {34, 35, 32, 33};      // cong tac hanh trinh, keo xuong 1k
const int THUAN = 19, NGUOC = 18;          // cau H: LOW = chay, HIGH = khoa
LiquidCrystal_I2C lcd(0x27, 16, 2);

const float PHI = 20.93;                   // vi do My Hao, Hung Yen
const int NGUONG = 200, VUNG_CHET = 120;   // muc ADC cua e1
const float S_MIN = 2500;                  // tong 4 kenh duoi day = may mu
const unsigned long T_LDR = 120000;        // 2 phut
const unsigned long T_TV  = 1800000;       // 30 phut
float K_cal[4] = {1.0, 1.0, 1.0, 1.0};     // he so hieu chuan 4 kenh
unsigned long tLDR = 0, tTV = 0;

int docTB(int chan, int n = 16) {          // trung binh co loai mau lech
  long s = 0; int m[16];
  for (int i = 0; i < n; i++) { m[i] = analogRead(chan); s += m[i]; }
  long tb = s / n; long s2 = 0; int d = 0;
  for (int i = 0; i < n; i++) if (abs(m[i] - tb) * 4 < tb) { s2 += m[i]; d++; }
  return d ? s2 / d : tb;
}

void docDS1307(int &ngay, int &thang, int &hh, int &mm, int &ss) {
  Wire.beginTransmission(0x68); Wire.write(0x00); Wire.endTransmission();
  Wire.requestFrom(0x68, 7);
  byte b[7]; for (int i = 0; i < 7; i++) b[i] = Wire.read();
  auto bcd = [](byte x) { return (x >> 4) * 10 + (x & 0x0F); };
  ss = bcd(b[0] & 0x7F); mm = bcd(b[1] & 0x7F); hh = bcd(b[2] & 0x3F);
  ngay = bcd(b[4] & 0x3F); thang = bcd(b[5] & 0x1F);
}

int ngayTrongNam(int ngay, int thang) {
  const int t31[12] = {31,28,31,30,31,30,31,31,30,31,30,31};
  int n = ngay; for (int m = 1; m < thang; m++) n += t31[m - 1];
  return n;
}

// thien van: tra ve goc dat tam pin (do, + ve phia Tay)
float gocThienVan() {
  int ng, th, hh, mm, ss; docDS1307(ng, th, hh, mm, ss);
  int n = ngayTrongNam(ng, th);
  float t = hh + mm / 60.0 + ss / 3600.0;
  float d = radians(23.45 * sin(radians(360.0 * (284 + n) / 365.0)));
  float H = radians(15.0 * (t - 12.0));
  float p = radians(PHI);
  float sa = sin(p)*sin(d) + cos(p)*cos(d)*cos(H);
  if (sa <= 0.05) return 0.0;              // gan den trang: ve goc 0
  float a = asin(sa);
  float x = cos(a) * sin(atan2(sin(H), cos(H)*sin(p) - tan(d)*cos(p)));
  return degrees(atan2(x, sa));            // khop hinh chieu Dong-Tay
}

float docGocPin() {                        // bien tro -> goc (hieu chuan 3 diem)
  float v = docTB(PIN_POT) * 3.3 / 4095.0;
  const float VMIN = 0.30, VMAX = 3.00, GMIN = -85.0, GMAX = 85.0;
  return constrain(GMIN + (v - VMIN) * (GMAX - GMIN) / (VMAX - VMIN), GMIN, GMAX);
}

void dungMotor()  { digitalWrite(THUAN, HIGH); digitalWrite(NGUOC, HIGH); }
void chayMotor(bool thuan, int ms) {
  if (thuan && digitalRead(QT[0]) == 1) return;     // chan hanh trinh
  if (!thuan && digitalRead(QT[1]) == 1) return;
  digitalWrite(THUAN, thuan ? LOW : HIGH);
  digitalWrite(NGUOC, thuan ? HIGH : LOW);
  delay(ms); dungMotor();                            // truc vit tu giu
}

void setup() {
  Serial.begin(115200);
  Wire.begin(); lcd.init(); lcd.backlight();
  analogReadResolution(12);
  analogSetPinAttenuation(PIN_POT, ADC_11db);
  analogSetPinAttenuation(PIN_AP_PIN, ADC_11db);
  for (int i = 0; i < 4; i++) {
    analogSetPinAttenuation(LDR[i], ADC_11db);
    pinMode(QT[i], INPUT);                            // da keo xuong 1k ben ngoai
  }
  pinMode(THUAN, OUTPUT); pinMode(NGUOC, OUTPUT); dungMotor();
}

void loop() {
  unsigned long now = millis();
  // 1) dinh vi tho theo thien van moi 30 phut
  if (now - tTV >= T_TV) {
    tTV = now;
    float dat = gocThienVan(), hien = docGocPin();
    if (fabs(dat - hien) > 2.0)
      chayMotor(dat > hien, min(6000, (int)fabs(dat - hien) * 90));
  }
  // 2) tinh chinh LDR moi 2 phut
  if (now - tLDR >= T_LDR) {
    tLDR = now;
    int L[4]; float S = 0;
    for (int i = 0; i < 4; i++) { L[i] = docTB(LDR[i]) * K_cal[i]; S += L[i]; }
    float e1 = (L[0] + L[2]) - (L[1] + L[3]);         // trai - phai
    if (S > S_MIN && fabs(e1) > NGUONG)
      chayMotor(e1 > 0, fabs(e1) > 3 * NGUONG ? 1200 : 350);
    // 3) hien thi LCD: gio tu DS1307 + goc pin + e1
    int ng, th, hh, mm, ss; docDS1307(ng, th, hh, mm, ss);
    char d1[17], d2[17];
    sprintf(d1, "%02d/%02d %02d:%02d:%02d", ng, th, hh, mm, ss);
    sprintf(d2, "goc=%+05.1f e=%+04.0f", docGocPin(), e1);
    lcd.clear(); lcd.setCursor(0, 0); lcd.print(d1);
    lcd.setCursor(0, 1); lcd.print(d2);
    Serial.printf("%s  S=%.0f e1=%+.0f goc=%.1f\\n", d1, S, e1, docGocPin());
  }
}"""

LAP_TRINH_CH3_CODE = [
    ("h2", "3.11. Code mẫu hoàn chỉnh của mô hình một trục"),
    ("code", CODE_1TRUC),
    ("p", "Code thực hiện đúng thứ tự đã mô tả: khởi tạo ADC, I²C, LCD và cầu H ở trạng thái khóa; mỗi 30 phút gọi khối thiên văn đọc DS1307 và chạy motor về góc đặt; mỗi 2 phút đọc bốn kênh LDR đã hiệu chuẩn, tính e1 và tinh chỉnh khi nắng đủ mạnh; mỗi chu kỳ hiển thị giờ DS1307 cùng góc tấm pin và e1 lên LCD 1602. Bản hai trục ở quyển 6 bổ sung kênh e2 và cặp lệnh motor thứ hai."),
]

LAP_TRINH_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"
LAP_TRINH_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành cài đặt Arduino IDE kèm lõi esp32 của Espressif và nạp thử thành công sketch Blink lên ESP32 DevKit."),
    ("b", "Hoàn thành thiết kế bảy sheet mạch EasyEDA, hàn và đo kiểm toàn bộ mạch điều khiển, mạch động lực, mạch nguồn."),
    ("b", "Hoàn thành hiệu chuẩn bốn kênh LDR, biến trở hồi tiếp ba điểm, đồng bộ DS1307 và hiển thị LCD."),
    ("b", "Hoàn thành viết và nạp code hybrid một trục: chạy đúng ba nhánh thiên văn – LDR – giữ vị trí khi mây mù, hiển thị đủ hai dòng LCD."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Chạy ngoài trời trọn ngày nắng, đối chiếu log góc tấm pin với đồ thị mô phỏng ở quyển nghiên cứu."),
    ("b", "Tinh chỉnh ngưỡng e1 và thời gian bước chạy motor để giảm số lần khởi động motor."),
    ("b", "Mở rộng code sang bản hai trục: thêm e2, cặp motor thứ hai và thứ tự chỉnh nghiêng trước – quay sau."),
]
