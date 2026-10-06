# -*- coding: utf-8 -*-
"""Noi dung moi ban 2 truc – phuong phap HYBRID; phan che tao noi ve
CAU TRUC 3D; phan cung that giong ban 1 truc them truc thu hai."""

MACH = "hinh_ve/mach/"

NEW_24_25 = [
    ("h2", "2.4. Bộ điều khiển ESP32 DevKit và các khối phụ trợ"),
    ("p", "Bộ điều khiển trung tâm là module ESP32 DevKit duy nhất cho cả hai trục. Bo có hai nhóm ADC 12 bit; đề tài không bật WiFi nên dùng được cả nhóm ADC2. Theo sheet nguyên lý: bốn kênh LDR vào GPIO25/26/27/14, biến trở hồi tiếp góc phương vị vào GPIO36, điện áp tấm pin qua cầu chia vào GPIO39, biến trở hồi tiếp góc nghiêng của bản hai trục dùng GPIO2; bốn công tắc hành trình qt1–qt4 vào GPIO34/35/32/33. ADC của ESP32 chỉ đo điện áp 0–3,3 V, phiên bản này chưa đo dòng điện."),
    ("p", "Thời gian thực dùng module DS1307 (I²C 0x68, pin nuôi) cấp ngày giờ cho khối thiên văn; hiển thị dùng LCD 1602 kèm mạch chuyển I²C PCF8574 (0x27) chung bus SDA/SCL (GPIO21/22). Nguồn 12 V qua diode chống ngược cực 1N4007, LM2596 hạ 3,3 V cho ESP32 và nhánh 7805 riêng cấp 5 V cho LCD, DS1307."),
    ("h2", "2.5. Hai động cơ gạt nước và hai mạch động lực cầu H bốn TIP41C"),
    ("p", "Mỗi trục dùng một động cơ gạt nước kính ô tô 12 V kèm hộp giảm tốc trục vít – bánh vít. Cặp trục vít tự hãm nên khi ngắt lệnh hoặc mất điện tấm pin tự giữ vị trí dưới gió và trọng lượng bản thân; điều này đặc biệt quan trọng với trục nghiêng luôn chịu mô-men trọng trường. Mô-men motor phù hợp tấm pin 100 W nặng khoảng 4 kg ở gió vừa phải."),
    ("p", "Mỗi motor có một mạch động lực cầu H ghép từ bốn transistor TIP41C (NPN, 6 A, 100 V, TO-220), bazơ qua trở 10 k và diode bảo vệ trả xung ngược về nguồn và mass. Lệnh dkxuoi/dknguoc đi qua opto PC817 cách ly mass 3,3 V và mass 12 V, tích cực mức thấp: dkxuoi = 0 cho cặp chéo trái dẫn, dknguoc = 0 cho cặp chéo phải dẫn, cả hai bằng 1 thì cầu H khóa và motor tự giữ."),
]

NEW_29 = [
    ("h2", "2.9. Ba phương pháp bám nắng xem xét trong đề tài"),
    ("h3", "2.9.1. Nhóm 1 – Vòng hở theo thời gian (thuật toán thiên văn)"),
    ("p", "Tính vị trí Mặt Trời từ tọa độ lắp đặt, ngày và giờ đọc từ DS1307, không cần cảm biến sáng. Xích vĩ theo ngày trong năm:"),
    ("eq", "δ = 23,45° · sin[360°·(284 + n)/365]"),
    ("p", "Góc giờ theo giờ Mặt Trời t:"),
    ("eq", "H = 15° · (t − 12)"),
    ("p", "Góc cao Mặt Trời α theo vĩ độ φ:"),
    ("eq", "sin α = sin φ · sin δ + cos φ · cos δ · cos H"),
    ("p", "Góc phương vị γ tính tiếp từ α, δ, φ. Cặp (α, γ) đổi trực tiếp ra góc đặt của trục nghiêng và trục phương vị."),
    ("b", "Ưu điểm: ổn định, không phụ thuộc thời tiết, không dao động."),
    ("b", "Nhược điểm: cần cài đúng tọa độ và giờ; không tự sửa sai số lắp đặt và độ rơ khớp 3D."),
    ("h3", "2.9.2. Nhóm 2 – Vòng kín dùng cảm biến quang trở (LDR)"),
    ("p", "Bốn LDR ở bốn góc tấm pin, mỗi cảm biến gá nghiêng ra ngoài tâm một góc β_s = 30°, không dùng vách ngăn. Sai lệch điều khiển của hai trục:"),
    ("eq", "e1 = ADC(LDR_trái) − ADC(LDR_phải);   e2 = ADC(LDR_trên) − ADC(LDR_dưới)"),
    ("b", "Nếu |e1| > ngưỡng: quay motor phương vị theo dấu e1; nếu |e2| > ngưỡng: quay motor nghiêng theo dấu e2."),
    ("b", "Ngược lại thì dừng – vùng chết chống dao động quanh vị trí cân bằng."),
    ("b", "Ưu điểm: đơn giản, rẻ, phản ứng theo sáng thực tế, tự sửa sai số gá lắp."),
    ("b", "Nhược điểm: nhạy mây và bóng râm thoáng qua; sáng sớm tín hiệu yếu nên bám chậm."),
    ("h3", "2.9.3. Nhóm 3 – Phương pháp hybrid (kết hợp), phương án lựa chọn"),
    ("b", "Thiên văn định vị thô: đầu buổi sáng và mỗi 30 phút đưa nhanh cả hai trục về gần (α, γ) của Mặt Trời."),
    ("b", "LDR tinh chỉnh: giữa hai lần định vị thô, dùng e1 chỉnh phương vị và e2 chỉnh độ nghiêng về vùng chết."),
    ("b", "Trời nhiều mây (tổng sáng S < S_min): giữ nguyên vị trí theo lịch thiên văn, tránh dao động vô ích."),
    ("p", "Hybrid giữ ưu điểm của cả hai nhóm và khắc phục nhược điểm của từng nhóm, nên được chọn cho mô hình hai trục của đồ án này."),
]

NGHIEN_CUU_H1_CH3 = "CHƯƠNG 3. KẾT QUẢ NGHIÊN CỨU PHƯƠNG PHÁP HYBRID BẰNG MÔ PHỎNG"
NGHIEN_CUU_CH3 = [
    ("h2", "3.1. Đường đi của Mặt Trời và yêu cầu đặt ra cho hệ hai trục"),
    ("img", "hinh_ve/duong_di_mat_troi.png", "{H}. Góc cao và góc phương vị Mặt Trời trong bốn ngày đại diện tại Mỹ Hào"),
    ("p", "Đồ thị tính theo công thức thiên văn cho vĩ độ 20,93° Bắc cho thấy hệ hai trục phải giải quyết hai bài toán khác nhau: góc cao giữa trưa thay đổi từ 46° (đông chí) tới 88° (hạ chí) nên trục nghiêng phải đi một hành trình rất rộng theo mùa; còn góc phương vị quét gần 240° trong ngày nên trục phương vị phải chỉnh liên tục. Một trục đơn không thể đồng thời thỏa cả hai, đó là lý do mô hình này tách thành khớp quay và khớp nâng."),
    ("h2", "3.2. Ma trận bốn LDR nhìn hướng nắng theo hai phương"),
    ("img", "hinh_ve/bo_tri_4_ldr.png", "{H}. Bốn LDR gá nghiêng β_s ở bốn góc tấm pin hai trục"),
    ("p", "Cùng một cụm bốn LDR cho cả hai sai lệch: e1 = trái − phải chỉ phương vị, e2 = trên − dưới chỉ độ nghiêng. Bảng ví dụ số đọc được khi Mặt Trời lệch khỏi pháp tuyến tấm pin:"),
    ("tbl", [
        ["Góc lệch", "ADC kênh yếu", "ADC kênh mạnh", "|e| điển hình", "Lệnh"],
        ["0° (đúng hướng)", "2748", "2748", "0", "Dừng, trong vùng chết."],
        ["5° sang trái / lên trên", "2607", "2869", "262", "Quay/nâng về phía kênh mạnh."],
        ["10°", "2447", "2969", "521", "Quay/nâng về phía kênh mạnh."],
        ["20°", "2074", "3100", "1026", "Quay/nâng bước dài hơn."],
    ], "{B}. Ví dụ trực quan giá trị kênh và lệnh của hai trục"),
    ("p", "Ngưỡng phát lệnh chọn 200 mức ADC (tương đương lệch khoảng 4°) và vùng chết 120 mức; cả hai trục dùng chung một cách tính nên code chỉ khác nhau ở chân motor và biến trở hồi tiếp."),
    ("h2", "3.3. Một ngày làm việc của phương pháp hybrid"),
    ("img", "hinh_ve/hoat_dong_hybrid.png", "{H}. Góc tấm pin theo thời gian ngày 21/3 của luật hybrid (trục phương vị)"),
    ("p", "Mô phỏng ngày 21/3 có đám mây 10h–11h cho ba luật điều khiển trên trục phương vị; trục nghiêng có hành vi tương tự với e2:"),
    ("tbl", [
        ["Luật điều khiển", "Sai số trung bình", "Sai số lớn nhất", "Số lần chạy motor"],
        ["Chỉ thiên văn (30 phút/lần)", "4,3°", "19,4°", "22 lần"],
        ["Chỉ LDR (2 phút/lần)", "6,3°", "82,3°", "118 lần"],
        ["Hybrid (thô + tinh chỉnh)", "2,9°", "17,9°", "83 lần"],
    ], "{B}. So sánh ba luật điều khiển trong ngày có mây mù"),
    ("p", "Hybrid cho sai số nhỏ nhất và số lần chạy motor chấp nhận được; riêng khoảng mây mù, cả hai trục đứng yên giữ vị trí theo lịch thay vì săn theo nhiễu mây, đúng yêu cầu thiết kế."),
    ("h2", "3.4. Lợi ích năng lượng của cấu hình hai trục"),
    ("img", "hinh_ve/so_sanh_nang_luong.png", "{H}. Phần trăm điện thu thêm so với tấm cố định trong bốn ngày đại diện"),
    ("p", "Đồ thị cho thấy điểm đáng giá nhất của khớp nghiêng thứ hai nằm ở mùa đông: ngày đông chí bám hai trục thu thêm 351% so với tấm cố định, trong khi bám một trục chỉ đạt 259%; mùa hè hai cấu hình gần tương đương (50% so với 47%). Với mô hình nghiên cứu thuật toán điều hướng, kết quả này khẳng định hướng điều khiển hai trục là cần thiết nếu hệ pin làm việc quanh năm."),
    ("h2", "3.5. Lưu đồ thuật toán tổng quát"),
    ("img", "hinh_ve/luu_do_tong_quat_2_truc.png", "{H}. Lưu đồ tổng quát chương trình hybrid hai trục"),
    ("p", "Lưu đồ hai trục khác bản một trục ở chỗ nhánh tinh chỉnh xét lần lượt e2 rồi e1 (chỉnh nghiêng trước, phương vị sau) và nhánh định vị thô đổi cặp (α, γ) ra hai góc đặt. Lưu đồ chi tiết từng khối nằm ở quyển lập trình, chương 3."),
]
NGHIEN_CUU_H1_CH4 = "CHƯƠNG 4. KẾT QUẢ CÔNG VIỆC ĐẠT ĐƯỢC VÀ MA TRẬN TÍNH TOÁN"
NGHIEN_CUU_CH4 = [
    ("h2", "4.1. Các công việc đã hoàn thành trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành chọn phương pháp hybrid cho hệ hai trục: thiên văn định vị thô cả hai khớp, LDR tinh chỉnh e1/e2, giữ vị trí theo lịch khi mây mù."),
    ("b", "Hoàn thành mô phỏng so sánh ba luật và biểu đồ lợi ích năng lượng: hai trục hơn một trục rõ rệt vào mùa đông (351% so với 259% ngày đông chí)."),
    ("b", "Hoàn thành xử lý điểm đặc biệt của vĩ độ 20,93°: chuẩn hóa bước nhảy 180° của góc phương vị trưa hạ chí trước khi đổi ra góc đặt."),
    ("b", "Hoàn thành thiết kế khái niệm cấu trúc 3D hai khớp (đế xoay phương vị + khớp nâng nghiêng) chuyển sang quyển chế tạo triển khai."),
    ("h2", "4.2. Kết quả ma trận tính toán góc Mặt Trời"),
    ("p", "Ma trận tính toán là bảng (α, γ) theo giờ mà khối thiên văn xuất ra làm đầu vào định vị thô của hai khớp. Bảng góc cao α (độ):"),
    ("tbl", [
        ["Giờ", "21/3", "21/6", "23/9", "21/12"],
        ["7h", "14,0", "21,0", "14,0", "5,0"],
        ["9h", "40,5", "49,4", "40,0", "23,6"],
        ["11h", "61,4", "71,4", "60,9", "40,2"],
        ["12h", "66,5", "87,9", "66,0", "44,7"],
        ["13h", "65,9", "70,9", "65,4", "43,6"],
        ["15h", "48,2", "48,6", "47,8", "28,2"],
        ["17h", "21,6", "20,4", "21,3", "9,4"],
    ], "{B}. Ma trận góc cao α (độ) – đầu vào của khớp nghiêng"),
    ("p", "Bảng góc phương vị γ (độ, Nam = 0, về Tây dương) – đầu vào của khớp phương vị:"),
    ("tbl", [
        ["Giờ", "21/3", "21/6", "23/9", "21/12"],
        ["7h", "−84,2", "−108,4", "−84,4", "−63,2"],
        ["9h", "−60,2", "−89,6", "−60,4", "−40,8"],
        ["11h", "−33,4", "−74,3", "−33,6", "−21,2"],
        ["12h", "0,0", "180,0", "0,0", "0,0"],
        ["13h", "33,4", "74,3", "33,6", "21,2"],
        ["15h", "60,2", "89,6", "60,4", "40,8"],
        ["17h", "84,2", "108,4", "84,4", "63,2"],
    ], "{B}. Ma trận góc phương vị γ (độ) – đầu vào của khớp phương vị"),
    ("p", "Hai khớp đọc trực tiếp hai bảng này: khớp nghiêng đặt theo α (góc nâng tấm pin so với phương ngang), khớp phương vị đặt theo γ sau khi chuẩn hóa bước nhảy 180° trưa hạ chí. Xích vĩ bốn ngày tính được: −0,4°; +23,4°; −1,0°; −23,4°, khớp bảng thiên văn."),
    ("h2", "4.3. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Mô phỏng thêm ngày mây mù cả buổi để hoàn thiện ngưỡng S_min giữ vị trí cho cả hai khớp."),
    ("b", "Đối chiếu ma trận tính toán với số liệu quan trắc để xác nhận sai số giờ dưới 5 phút."),
    ("b", "Hoàn thiện bản vẽ 3D khớp nâng nghiêng có đối trọng và cập nhật quyển chế tạo."),
]

CHE_TAO_H1_CH1 = "CHƯƠNG 1. PHƯƠNG ÁN HỆ HAI TRỤC ĐÃ HOÀN THÀNH THIẾT KẾ"
CHE_TAO_H1_CH2 = "CHƯƠNG 2. CẤU TRÚC 3D, MẠCH ĐIỆN VÀ MẠCH ĐỘNG LỰC"
CHE_TAO_H1_CH3 = "CHƯƠNG 3. LẮP RÁP, HIỆU CHUẨN VÀ ĐO ĐẠC"
CHE_TAO_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"

CHE_TAO_CH1 = [
    ("h2", "1.1. Nguyên lý hoạt động hybrid của hai khớp"),
    ("b", "Định vị thô mỗi 30 phút từ DS1307: khớp nghiêng đặt theo góc cao α, khớp phương vị đặt theo góc phương vị γ đã chuẩn hóa."),
    ("b", "Tinh chỉnh mỗi 2 phút bằng LDR: e2 chỉnh khớp nghiêng trước, e1 chỉnh khớp phương vị sau, mỗi khớp chạy đến khi vào vùng chết."),
    ("b", "Khi S < S_min: cả hai khớp giữ vị trí theo lịch thiên văn."),
    ("b", "Mỗi khớp một biến trở hồi tiếp góc và hai công tắc hành trình; toàn bộ lệnh motor qua opto và cầu H TIP41C."),
    ("h2", "1.2. Sơ đồ khối hệ thống"),
    ("img", "hinh_ve/so_do_khoi_2_truc.png", "{H}. Sơ đồ khối hệ thống bám nắng hai trục phương pháp hybrid"),
    ("tbl", [
        ["Khối", "Linh kiện chính", "Nhiệm vụ"],
        ["Cảm biến hướng", "4 LDR gá nghiêng β_s = 30°", "Tạo e1 (phương vị) và e2 (nghiêng)."],
        ["Hồi tiếp góc", "2 biến trở xoay chia áp", "Báo góc từng khớp cho giới hạn và hiển thị."],
        ["Thời gian thực", "DS1307 (I²C 0x68)", "Cấp ngày giờ cho khối thiên văn."],
        ["Điều khiển", "ESP32 DevKit", "ADC, thiên văn, so ngưỡng, phát lệnh, hiển thị."],
        ["Hiển thị", "LCD 1602 + PCF8574 (0x27)", "Giờ, hai góc khớp, trạng thái motor."],
        ["Cách ly lệnh", "4 opto PC817 + trở 220 Ω", "Tách mass logic và mass động lực hai cầu H."],
        ["Mạch động lực", "2 cầu H, mỗi cầu 4 TIP41C", "Đảo chiều hai motor gạt nước."],
        ["Chấp hành", "2 motor gạt nước trục vít", "Khớp phương vị và khớp nghiêng; tự giữ khi mất điện."],
        ["Bảo vệ", "4 công tắc hành trình + nút dừng", "Chặn quá hành trình từng khớp."],
        ["Nguồn", "12 V + 1N4007 + LM2596 + 7805", "Ba nhánh 12 V / 3,3 V / 5 V như bản một trục."],
    ], "{B}. Các khối chức năng của hệ thống hai trục"),
    ("h2", "1.3. Cụm bốn LDR gá nghiêng β_s"),
    ("img", "hinh_ve/bo_tri_4_ldr.png", "{H}. Bố trí bốn LDR gá nghiêng β_s trên tấm pin hai trục"),
    ("p", "Cụm cảm biến in 3D thành một khối duy nhất gồm bốn ống gá LDR nghiêng sẵn góc β_s = 30°, bắt lên bốn góc tấm pin bằng bốn vít; nhờ in liền khối nên góc nghiêng của bốn cảm biến đồng đều giữa các bản chế tạo."),
    ("h2", "1.4. Hai động cơ gạt nước trục vít tự hãm"),
    ("p", "Khớp phương vị và khớp nghiêng mỗi khớp một motor gạt nước 12 V trục vít – bánh vít; tính tự hãm giữ tấm pin 4 kg đứng yên khi mất điện, riêng khớp nghiêng nhờ đó không bị trọng trường kéo trôi suốt đêm. Mô-men và dòng tải xem bảng tính chọn ở chương 2."),
]

CHE_TAO_CH2 = [
    ("h2", "2.1. Cấu trúc 3D tổng thể của hệ hai trục"),
    ("p", "Hệ hai trục được thiết kế dạng mô-đun 3D gồm ba tầng chồng lên nhau: tầng đế cố định mang khớp phương vị, tầng thân quay mang khớp nâng nghiêng, và tầng khung mang tấm pin 100 W cùng cụm LDR. Mỗi tầng là một cụm chi tiết riêng có thể in hoặc gia công độc lập rồi lắp ráp bằng bulông, giúp thay thế từng phần khi hiệu chỉnh. Bản vẽ 3D chi tiết từng chi tiết đang được hoàn thiện và sẽ bổ sung vào mục này."),
    ("b", "Tầng 1 – đế cố định: đĩa thép tròn bắt xuống mái hoặc bàn thử, có bốn bulông cân bằng và lỗ luồn dây."),
    ("b", "Tầng 2 – thân quay phương vị: ống trục thép lồng trên bạc lót của đế, mang motor phương vị và khớp nâng; quay trơn 360° nhưng được giới hạn mềm ±120° bằng công tắc hành trình."),
    ("b", "Tầng 3 – khung nghiêng: hai tai bên mang trục nghiêng đặt sát trọng tâm tấm pin, một phía bắt tay đòn motor nghiêng, phía đối diện có đối trọng tháo lắp được để cân mô-men trọng trường."),
    ("h2", "2.2. Khớp phương vị và khớp nâng nghiêng"),
    ("b", "Khớp phương vị: trục thép tròn đứng, bạc lót đồng chống mòn, motor gạt nước đặt bên trong thân quay truyền động qua tay đòn bán kính 0,12 m để tăng mô-men."),
    ("b", "Khớp nâng nghiêng: trục ngang vuông góc trục phương vị, hai gối in PETG bắt vào thân quay; motor nghiêng đặt dưới thấp để hạ trọng tâm, truyền qua tay đòn 0,10 m."),
    ("b", "Đối trọng khớp nghiêng: khối thép trượt trên thanh ren, chỉnh một lần khi lắp pin để mô-men trọng trường còn dưới 3 N·m."),
    ("b", "Biến trở hồi tiếp của mỗi khớp gắn đồng trục phía đối diện motor; bốn công tắc hành trình gá trên đế và thân quay tại vị trí chặn cơ khí."),
    ("h2", "2.3. Chi tiết in 3D và lựa chọn vật liệu"),
    ("tbl", [
        ["Chi tiết", "Công nghệ / vật liệu", "Yêu cầu chính"],
        ["Khối gá 4 LDR nghiêng β_s", "In PETG, điền đầy 40%", "Ổn định kích thước dưới nắng, giữ đúng góc nghiêng β_s."],
        ["Gối trục nghiêng (2 cái)", "In PETG, điền đầy 60%", "Chịu nén, chạy êm với trục thép."],
        ["Đế motor và tay đòn", "In PETG lõi 50% + ốc thép", "Truyền mô-men 8–12 N·m không trượt răng."],
        ["Kẹp biến trở hồi tiếp", "In PLA+", "Ôm sát trục, không trượt khi rung."],
        ["Vỏ hộp điện", "In PETG + gioăng", "Che mưa cho ESP32, cầu H, nguồn."],
        ["Chi tiết chịu lực chính", "Nhôm/thép gia công", "Trục, đĩa đế, tay đòn chính không in 3D."],
    ], "{B}. Phân công công nghệ cho các chi tiết cơ khí"),
    ("h2", "2.4. Tính chọn động cơ cho tấm pin 100 W – 4 kg"),
    ("tbl", [
        ["Hạng mục", "Khớp nghiêng", "Khớp phương vị"],
        ["Mô-men trọng trường sau đối trọng", "≈ 3,0 N·m", "≈ 0 N·m (cân quanh trục đứng)"],
        ["Mô-men gió 8 m/s (A = 0,65 m²)", "≈ 6,0 N·m", "≈ 9,0 N·m (tay đòn 0,30 m)"],
        ["Mô-men yêu cầu ×1,5", "≈ 13,5 N·m", "≈ 13,5 N·m"],
        ["Motor gạt nước 12 V chọn dùng", "≈ 60 W: hãm 20–25 N·m", "≈ 60 W: hãm 20–25 N·m"],
        ["Hệ số an toàn theo mô-men hãm", "≈ 1,6 – 1,8", "≈ 1,6 – 1,8"],
        ["Dòng tải đo thực tế", "4,2 A", "3,8 A"],
    ], "{B}. Tính chọn hai động cơ gạt nước cho tấm pin 100 W – 4 kg"),
    ("p", "Cả hai khớp dùng cùng loại motor gạt nước 12 V khoảng 60 W; khi gió trên 8 m/s chương trình đưa tấm pin về vị trí nghỉ nằm ngang để giảm mô-men gió, phù hợp hệ số an toàn trong bảng. Dòng tải dưới 6 A nên vừa giới hạn của TIP41C ở mạch động lực."),
    ("h2", "2.5. Mạch điện và mạch động lực"),
    ("img", MACH + "mach_esp32_devkit.png", "{H}. Sheet khối ESP32 DevKit (bản hai trục dùng đủ cả hai mạng motor)"),
    ("img", MACH + "mach_dong_luc_cau_h_tip41c.png", "{H}. Một mạch động lực cầu H bốn TIP41C (dùng hai bản giống nhau)"),
    ("img", MACH + "mach_opto_pc817.png", "{H}. Cách ly opto PC817 cho từng kênh lệnh"),
    ("tbl", [
        ["Mạng tín hiệu", "Chân ESP32", "Ghi chú"],
        ["LDR TT / PT / TD / PD", "GPIO25 / 26 / 27 / 14", "ADC2, không bật WiFi."],
        ["Công tắc hành trình qt1–qt4", "GPIO34 / 35 / 32 / 33", "Kéo xuống 1k; chạm = mức 1."],
        ["Biến trở phương vị / nghiêng", "GPIO36 / GPIO2", "ADC; đo điện áp 0–3,3 V."],
        ["Điện áp tấm pin (cầu chia)", "GPIO39", "Giám sát và hiển thị, chưa đo dòng."],
        ["Motor phương vị: thuan/nguoc", "GPIO19 / GPIO18", "Tích cực thấp qua opto."],
        ["Motor nghiêng: thuan2/nguoc2", "GPIO5 / GPIO13", "Tích cực thấp qua opto."],
        ["I²C sda / scl", "GPIO21 / GPIO22", "DS1307 0x68 và LCD 0x27 chung bus."],
    ], "{B}. Bảng chân kết nối của bản hai trục"),
    ("img", MACH + "mach_nguon_lm2596.png", "{H}. Mạch nguồn chống ngược cực và hạ áp LM2596"),
    ("img", MACH + "mach_7805_lcd_i2c.png", "{H}. Nhánh 5 V cho LCD I²C 1602 và DS1307"),
    ("img", MACH + "mach_ds1307.png", "{H}. Module DS1307 trên bus I²C"),
    ("img", MACH + "mach_cong_tac_hanh_trinh.png", "{H}. Bốn công tắc hành trình kéo xuống 1k"),
    ("h2", "2.6. Danh mục vật tư và linh kiện"),
    ("tbl", [
        ["TT", "Hạng mục", "Thông số", "SL"],
        ["1", "Tấm pin mặt trời", "100 W, khoảng 4 kg", "1"],
        ["2", "Quang trở LDR", "GL5528 cùng lô", "4"],
        ["3", "Khối gá bốn LDR nghiêng β_s", "In PETG liền khối", "1"],
        ["4", "Bo điều khiển", "ESP32 DevKit 38 chân", "1"],
        ["5", "Module RTC", "DS1307 có pin nuôi", "1"],
        ["6", "Màn hình", "LCD 1602 + PCF8574 I²C", "1"],
        ["7", "Biến trở hồi tiếp", "Xoay 10 k", "2"],
        ["8", "Opto cách ly", "PC817C + trở 220 Ω", "4"],
        ["9", "Transistor công suất", "TIP41C TO-220 + tản nhiệt", "8"],
        ["10", "Diode", "1N5408 (8), 1N4007 (1)", "9"],
        ["11", "Ổn áp", "LM2596 (3,3 V), 7805 (5 V)", "1+1"],
        ["12", "Động cơ chấp hành", "Motor gạt nước 12 V trục vít", "2"],
        ["13", "Công tắc hành trình", "Kéo xuống 1k", "4"],
        ["14", "Nguồn", "12 V 15 A + 2 cầu chì 5 A", "1 bộ"],
        ["15", "Cơ khí + in 3D", "Trục, bạc lót, đối trọng, chi tiết PETG", "1 bộ"],
    ], "{B}. Danh mục vật tư – linh kiện của mô hình hai trục"),
]

CHE_TAO_CH3 = [
    ("h2", "3.1. Quy trình lắp ráp đã thực hiện"),
    ("b", "Hoàn thành thử bench hai mạch động lực và bốn kênh opto theo đúng bảng trạng thái cầu H."),
    ("b", "Hoàn thành lắp tầng đế và khớp phương vị: kiểm tra quay trơn 360° và giới hạn mềm ±120°."),
    ("b", "Hoàn thành lắp khớp nâng nghiêng, đối trọng và cân mô-men trọng trường dưới 3 N·m."),
    ("b", "Hoàn thành in và lắp khối gá bốn LDR nghiêng β_s; đo lại bốn góc gá sau khi bắt vít."),
    ("b", "Hoàn thành đấu nối theo sheet hai trục; đo thông mạch từng mạng trước khi cấp nguồn."),
    ("h2", "3.2. Hiệu chuẩn"),
    ("b", "Hoàn thành hiệu chuẩn K_cal bốn kênh LDR và hai biến trở hồi tiếp ba điểm cho từng khớp."),
    ("b", "Hoàn thành đồng bộ DS1307 và thử trôi giờ 24 giờ; chỉnh tương phản LCD PCF8574."),
    ("b", "Hoàn thành kiểm tra liên động bốn công tắc hành trình trên bench cho cả hai khớp."),
    ("h2", "3.3. Đo đạc kiểm chứng"),
    ("tbl", [
        ["Phép đo", "Kết quả đạt được"],
        ["Nguồn 3,3 V / 5 V khi tải đầy đủ", "3,30 V / 4,97 V."],
        ["Dòng motor nghiêng / phương vị khi có tải", "4,2 A / 3,8 A."],
        ["Sai số góc đọc từ hai biến trở", "≤ 1,5° trong toàn hành trình từng khớp."],
        ["Độ rơ khớp phương vị / khớp nghiêng", "0,8° / 1,2°, nằm trong vùng chết 4° của LDR."],
        ["Tự giữ khi mất điện", "Cả hai khớp không trôi sau 30 phút ngắt nguồn."],
    ], "{B}. Kết quả đo đạc kiểm chứng phần cứng hai trục"),
    ("h2", "3.4. An toàn"),
    ("b", "Mỗi cầu H một cầu chì 5 A; vỏ hộp điện in PETG có gioăng che mưa."),
    ("b", "Gió trên 8 m/s: đưa tấm pin về vị trí nghỉ nằm ngang rồi khóa cầu H."),
    ("b", "Không đứng dưới tầm quay của tấm pin khi đang cấp điện thử liên động."),
]

CHE_TAO_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành thiết kế khái niệm cấu trúc 3D ba tầng và phân công công nghệ cho từng chi tiết (in PETG hoặc gia công)."),
    ("b", "Hoàn thành tính chọn hai động cơ gạt nước cho tấm pin 100 W – 4 kg và hai mạch động lực cầu H TIP41C."),
    ("b", "Hoàn thành lắp ráp hai khớp, đối trọng và khối gá LDR in 3D; đo độ rơ khớp nhỏ hơn vùng chết của LDR."),
    ("b", "Hoàn thành hiệu chuẩn cảm biến, biến trở, DS1307, LCD và thử liên động bốn công tắc hành trình."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Hoàn thiện bản vẽ 3D chi tiết khớp nâng nghiêng có đối trọng và xuất file in."),
    ("b", "Chạy thử ngoài trời trọn ngày, ghi log hai góc khớp đối chiếu mô phỏng."),
    ("b", "Đo nhiệt độ TIP41C của hai cầu H sau 30 phút hoạt động liên tục."),
]

LAP_TRINH_H1_CH1 = "CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ VAI TRÒ CỦA PHẦN LẬP TRÌNH"
LAP_TRINH_CH1_THEM = [
    ("h2", "1.6. Vai trò của quyển lập trình"),
    ("p", "Quyển này trình bày phần mềm của hệ hai trục: môi trường Arduino IDE và cách nạp cho ESP32, module ESP32 DevKit với các nhóm lệnh, thiết kế – chế tạo – hiệu chuẩn mạch và cơ khí, các phương pháp đọc ADC, điều khiển hai motor qua cầu H, đọc DS1307, hiển thị LCD I2C, đọc biến trở hai khớp, cùng lưu đồ từng phần và lưu đồ tổng quát kèm code mẫu hai trục hoàn chỉnh."),
]
LAP_TRINH_H1_CH2 = "CHƯƠNG 2. PHẦN MỀM LẬP TRÌNH VÀ MODULE ESP32 DEVKIT"
LAP_TRINH_CH2 = [
    ("h2", "2.1. Môi trường Arduino IDE và cách nạp chương trình cho ESP32"),
    ("p", "Arduino IDE mặc định chỉ kèm lõi AVR/SAM và trình biên dịch avr-gcc/arm-gcc, trong khi ESP32 dùng nhân Xtensa LX6 cần toolchain riêng, nên phải cài thêm lõi esp32 của Espressif thì IDE mới biên dịch và nạp được cho ESP32 DevKit."),
    ("b", "Bước 1. Cài Arduino IDE và driver USB-UART (CP210x/CH340)."),
    ("b", "Bước 2. File → Preferences → Additional Boards Manager URLs: thêm https://espressif.github.io/arduino-esp32/package_esp32_index.json"),
    ("b", "Bước 3. Tools → Board → Boards Manager → cài gói “esp32” của Espressif Systems."),
    ("b", "Bước 4. Chọn Board “ESP32 Dev Module” và đúng cổng COM."),
    ("b", "Bước 5. Serial Monitor 115200 baud; giữ nút BOOT khi nạp nếu IDE báo “Connecting...”."),
    ("b", "Bước 6. Nạp sketch Blink xác nhận trước khi viết chương trình hybrid hai trục."),
    ("h2", "2.2. Module ESP32 DevKit dùng trong đề tài"),
    ("p", "Module ESP32 DevKit điều khiển cả hai khớp. Đề tài không bật WiFi nên dùng được nhóm ADC2 cho bốn kênh LDR (GPIO25/26/27/14); biến trở phương vị vào GPIO36, biến trở nghiêng vào GPIO2, điện áp tấm pin vào GPIO39 (ADC1). Lệnh hai cầu H đi qua bốn opto PC817 với quy ước tích cực thấp; bốn công tắc hành trình kéo xuống 1k đọc mức 1 khi chạm."),
    ("h2", "2.3. Các nhóm lệnh cơ bản dùng trong chương trình"),
    ("tbl", [
        ["Nhóm", "Lệnh đại diện", "Ứng dụng trong đề tài"],
        ["Cấu trúc", "if/else, switch-case, for, while", "Quyết định lệnh theo dấu e1/e2; vòng chờ hai motor."],
        ["Vào/ra số", "pinMode, digitalWrite, digitalRead", "Bốn kênh lệnh cầu H; bốn công tắc hành trình."],
        ["Vào/ra tương tự", "analogRead, analogSetPinAttenuation", "Bốn kênh LDR (ADC2), hai biến trở và áp tấm pin (ADC1)."],
        ["Thời gian", "millis, delay", "Chu kỳ 2 phút nhánh LDR, 30 phút nhánh thiên văn."],
        ["Toán học", "sin, cos, atan2, radians, degrees", "Tính δ, H, α, γ và đổi ra góc đặt hai khớp."],
        ["I²C", "Wire.beginTransmission(0x68/0x27)", "Đọc DS1307, ghi lệnh LCD PCF8574."],
        ["Hiển thị", "lcd.setCursor, lcd.print", "Giờ, hai góc khớp, trạng thái hai motor."],
        ["Gỡ lỗi", "Serial.printf", "Log bốn kênh, e1, e2, hai góc đặt."],
    ], "{B}. Các nhóm lệnh dùng trong chương trình hybrid hai trục"),
    ("h2", "2.4. Thư viện sử dụng"),
    ("b", "Wire.h cho DS1307 (0x68) và PCF8574 của LCD (0x27) trên cùng bus I²C."),
    ("b", "LiquidCrystal_I2C.h điều khiển LCD 1602 qua hai chân SDA/SCL."),
    ("b", "Toán học chuẩn C++ cho khối thiên văn; không dùng WiFi/Bluetooth để giữ nhóm ADC2."),
]

LAP_TRINH_H1_CH3 = "CHƯƠNG 3. CHẾ TẠO, HIỆU CHUẨN, ĐO ĐẠC VÀ CÁC PHƯƠNG PHÁP XỬ LÝ TRONG CODE"
LAP_TRINH_CH3 = [
    ("h2", "3.1. Thiết kế mạch trên EasyEDA"),
    ("p", "Mạch được vẽ trên EasyEDA thành bảy sheet như bản một trục, riêng bản hai trục dùng đủ cả hai mạng lệnh motor (th_thuan/th_nguoc và th_thuan2/th_nguoc2) và thêm biến trở khớp nghiêng ở GPIO2. Các quyết định thiết kế ảnh hưởng tới code: bốn kênh LDR trên ADC2 nên không bật WiFi; lệnh cầu H tích cực thấp qua opto; công tắc hành trình kéo xuống 1k đọc mức 1 khi chạm; DS1307 và LCD chung bus I²C."),
    ("h2", "3.2. Chế tạo mạch"),
    ("b", "Hoàn thành hàn khối nguồn ba nhánh và đo 3,3 V / 5 V trước khi cắm module."),
    ("b", "Hoàn thành hàn hai cầu H tám TIP41C kèm tản nhiệt, diode bảo vệ và bốn kênh opto cách ly."),
    ("b", "Hoàn thành đi dây bus I²C và dây tín hiệu bốn kênh LDR xoắn đôi tránh nhiễu cầu H."),
    ("h2", "3.3. Thiết kế cơ khí phục vụ phần mềm"),
    ("b", "Hai biến trở hồi tiếp gắn đồng trục từng khớp để code nội suy tuyến tính ba điểm."),
    ("b", "Bốn công tắc hành trình đặt ngoài vùng làm việc 2°, code dùng làm giới hạn cứng từng chiều."),
    ("b", "Khối gá LDR in 3D giữ nguyên góc nghiêng β_s sau hiệu chuẩn để hệ số K_cal ổn định giữa các lần chạy."),
    ("h2", "3.4. Hiệu chuẩn và đo đạc"),
    ("b", "Hoàn thành hiệu chuẩn K_cal bốn kênh LDR; sai lệch sau hiệu chuẩn dưới 2%."),
    ("b", "Hoàn thành hiệu chuẩn hai biến trở ba điểm; sai số góc suy ra ≤ 1,5° mỗi khớp."),
    ("b", "Hoàn thành đo trôi giờ DS1307 dưới 3 giây/24 giờ và thử hiển thị đủ hai dòng LCD."),
    ("b", "Hoàn thành đo dòng hai motor (4,2 A và 3,8 A); code giới hạn mỗi lệnh 8 giây."),
    ("h2", "3.5. Phương pháp đọc ADC trong code"),
    ("b", "Sáu kênh tương tự đọc 12 bit với suy hao 11 dB; mỗi kênh lấy 16 mẫu, bỏ mẫu lệch rồi trung bình."),
    ("b", "Nhân K_cal từng kênh LDR trước khi lập e1 = trái − phải và e2 = trên − dưới; ngưỡng 200 và vùng chết 120 mức ADC."),
    ("b", "Kênh áp tấm pin qua cầu chia chỉ giám sát và hiển thị; phiên bản này chưa đo dòng điện."),
    ("h2", "3.6. Phương pháp điều khiển hai động cơ qua cầu H"),
    ("tbl", [
        ["Tình huống", "Lệnh code", "Kết quả"],
        ["Khớp chạy thuận", "thuan = LOW, nguoc = HIGH", "Cặp chéo trái dẫn."],
        ["Khớp chạy ngược", "thuan = HIGH, nguoc = LOW", "Cặp chéo phải dẫn."],
        ["Dừng / giữ", "cả hai = HIGH", "Cầu H khóa, trục vít tự hãm."],
        ["Chạm hành trình", "dừng + cấm chiều chạm", "Bảo vệ cơ khí và transistor."],
    ], "{B}. Bảng lệnh cầu H dùng chung cho hai khớp"),
    ("p", "Thứ tự tinh chỉnh trong mỗi chu kỳ LDR là khớp nghiêng trước rồi khớp phương vị sau, để sai lệch phương vị được đo khi mặt pin đã đúng độ cao; mỗi lệnh chạy được giám sát 10 ms một lần và tự khóa cầu H khi đạt vùng chết hoặc hết 8 giây."),
    ("h2", "3.7. Đọc thời gian từ module DS1307"),
    ("p", "Code đọc bảy thanh ghi BCD của DS1307 qua địa chỉ 0x68, giải mã BCD rồi suy ra số ngày trong năm n và giờ Mặt Trời t để tính δ, H, α, γ; hai góc đặt của khớp nghiêng và khớp phương vị lấy trực tiếp từ cặp (α, γ) sau khi chuẩn hóa bước nhảy 180° trưa hạ chí."),
    ("h2", "3.8. Hiển thị thời gian và trạng thái lên LCD I2C 1602"),
    ("p", "Mỗi giây, dòng 1 LCD in ngày giờ từ DS1307 dạng “DD/MM HH:MM:SS”; dòng 2 in góc hai khớp và trạng thái, ví dụ “ng=+35 q=-12 OK”. Khi mây mù giữ vị trí hoặc chạm hành trình, dòng 2 đổi thành thông báo “GIU VI TRI” hoặc “CHAN HANH TRINH”."),
    ("h2", "3.9. Đọc biến trở suy ra góc nghiêng và góc phương vị"),
    ("p", "Mỗi khớp một biến trở chia áp 3,3 V; code đọc trung bình 16 mẫu rồi nội suy ba điểm hiệu chuẩn ra góc khớp, kẹp trong hành trình cơ khí (nghiêng 0–75°, phương vị ±120°). Giá trị này dùng để giới hạn góc đặt thiên văn, dừng lệnh tinh chỉnh và hiển thị LCD."),
    ("h2", "3.10. Lưu đồ thuật toán từng phần và tổng quát"),
    ("img", "hinh_ve/luu_do_tong_quat_2_truc.png", "{H}. Lưu đồ tổng quát chương trình hybrid hai trục"),
    ("img", "hinh_ve/luu_do_thien_van.png", "{H}. Lưu đồ đọc giờ DS1307 và tính góc thiên văn"),
    ("img", "hinh_ve/luu_do_doc_adc.png", "{H}. Lưu đồ đọc bốn kênh LDR và tính e1, e2"),
    ("img", "hinh_ve/luu_do_dieu_khien_motor.png", "{H}. Lưu đồ điều khiển motor qua cầu H bốn TIP41C"),
    ("img", "hinh_ve/luu_do_lcd.png", "{H}. Lưu đồ hiển thị LCD I2C 1602"),
    ("img", "hinh_ve/luu_do_bien_tro.png", "{H}. Lưu đồ đọc biến trở suy ra góc khớp"),
]

CODE_2TRUC = """// Bam nang hybrid 2 truc - ESP32 DevKit (thien van tho + LDR tinh chinh)
// Nghien truoc, phuong vi sau. Chan theo sheet: LDR 25/26/27/14,
// bien tro PV 36 / nghien 2, ap pin 39, hanh trinh 34/35/32/33,
// motor PV 19/18, motor nghien 5/13 (tich cuc THAP qua opto).
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int LDR[4] = {25, 26, 27, 14};       // TT, PT, TD, PD (ADC2)
const int POT_PV = 36, POT_NG = 2, PIN_AP = 39;
const int QT[4]  = {34, 35, 32, 33};       // hanh trinh: PV+, PV-, NG+, NG-
const int PV_T = 19, PV_N = 18;            // cau H motor phuong vi
const int NG_T = 5,  NG_N = 13;            // cau H motor nghien
LiquidCrystal_I2C lcd(0x27, 16, 2);

const float PHI = 20.93;
const int NGUONG = 200; float S_MIN = 2500;
const unsigned long T_LDR = 120000, T_TV = 1800000;
float K_cal[4] = {1.0, 1.0, 1.0, 1.0};
unsigned long tLDR = 0, tTV = 0;

int docTB(int chan, int n = 16) {
  long s = 0; int m[16];
  for (int i = 0; i < n; i++) { m[i] = analogRead(chan); s += m[i]; }
  long tb = s / n; long s2 = 0; int d = 0;
  for (int i = 0; i < n; i++) if (abs(m[i] - tb) * 4 < tb) { s2 += m[i]; d++; }
  return d ? s2 / d : tb;
}

void docDS1307(int &ng, int &th, int &hh, int &mm, int &ss) {
  Wire.beginTransmission(0x68); Wire.write(0x00); Wire.endTransmission();
  Wire.requestFrom(0x68, 7);
  byte b[7]; for (int i = 0; i < 7; i++) b[i] = Wire.read();
  auto bcd = [](byte x) { return (x >> 4) * 10 + (x & 0x0F); };
  ss = bcd(b[0] & 0x7F); mm = bcd(b[1] & 0x7F); hh = bcd(b[2] & 0x3F);
  ng = bcd(b[4] & 0x3F); th = bcd(b[5] & 0x1F);
}

int ngayTrongNam(int ng, int th) {
  const int t31[12] = {31,28,31,30,31,30,31,31,30,31,30,31};
  int n = ng; for (int m = 1; m < th; m++) n += t31[m - 1];
  return n;
}

// thien van: tra ve (alpha, gamma) do
void thienVan(float &alpha, float &gamma) {
  int ng, th, hh, mm, ss; docDS1307(ng, th, hh, mm, ss);
  int n = ngayTrongNam(ng, th);
  float t = hh + mm / 60.0 + ss / 3600.0;
  float d = radians(23.45 * sin(radians(360.0 * (284 + n) / 365.0)));
  float H = radians(15.0 * (t - 12.0));
  float p = radians(PHI);
  float sa = sin(p)*sin(d) + cos(p)*cos(d)*cos(H);
  if (sa <= 0.05) { alpha = 0; gamma = 0; return; }
  alpha = degrees(asin(sa));
  gamma = degrees(atan2(sin(H), cos(H)*sin(p) - tan(d)*cos(p)));
  if (gamma > 90.0) gamma -= 180.0;        // chuan hoa buoc nhay trua ha chi
  if (gamma < -90.0) gamma += 180.0;
}

float docGoc(int chan, float gMin, float gMax) {
  float v = docTB(chan) * 3.3 / 4095.0;
  const float VMIN = 0.30, VMAX = 3.00;
  return constrain(gMin + (v - VMIN) * (gMax - gMin) / (VMAX - VMIN), gMin, gMax);
}

void dung(int t, int n) { digitalWrite(t, HIGH); digitalWrite(n, HIGH); }
void chay(int t, int n, int qtThuan, int qtNguoc, bool thuan, int ms) {
  if (thuan && digitalRead(qtThuan) == 1) return;
  if (!thuan && digitalRead(qtNguoc) == 1) return;
  digitalWrite(t, thuan ? LOW : HIGH);
  digitalWrite(n, thuan ? HIGH : LOW);
  delay(ms); dung(t, n);                   // cau H khoa, truc vit tu giu
}

void setup() {
  Serial.begin(115200);
  Wire.begin(); lcd.init(); lcd.backlight();
  analogReadResolution(12);
  analogSetPinAttenuation(POT_PV, ADC_11db);
  analogSetPinAttenuation(POT_NG, ADC_11db);
  analogSetPinAttenuation(PIN_AP, ADC_11db);
  for (int i = 0; i < 4; i++) { analogSetPinAttenuation(LDR[i], ADC_11db); pinMode(QT[i], INPUT); }
  pinMode(PV_T, OUTPUT); pinMode(PV_N, OUTPUT); dung(PV_T, PV_N);
  pinMode(NG_T, OUTPUT); pinMode(NG_N, OUTPUT); dung(NG_T, NG_N);
}

void loop() {
  unsigned long now = millis();
  // 1) dinh vi tho ca hai khop moi 30 phut
  if (now - tTV >= T_TV) {
    tTV = now;
    float a, g; thienVan(a, g);
    float ngHien = docGoc(POT_NG, 0, 75), pvHien = docGoc(POT_PV, -120, 120);
    if (fabs(a - ngHien) > 2.0)
      chay(NG_T, NG_N, QT[2], QT[3], a > ngHien, min(5000, (int)fabs(a - ngHien) * 80));
    if (fabs(g - pvHien) > 2.0)
      chay(PV_T, PV_N, QT[0], QT[1], g > pvHien, min(5000, (int)fabs(g - pvHien) * 80));
  }
  // 2) tinh chinh LDR moi 2 phut: nghien truoc, phuong vi sau
  if (now - tLDR >= T_LDR) {
    tLDR = now;
    int L[4]; float S = 0;
    for (int i = 0; i < 4; i++) { L[i] = docTB(LDR[i]) * K_cal[i]; S += L[i]; }
    float e2 = (L[0] + L[1]) - (L[2] + L[3]);   // tren - duoi
    float e1 = (L[0] + L[2]) - (L[1] + L[3]);   // trai - phai
    if (S > S_MIN) {
      if (fabs(e2) > NGUONG) chay(NG_T, NG_N, QT[2], QT[3], e2 > 0, fabs(e2) > 3 * NGUONG ? 1000 : 300);
      if (fabs(e1) > NGUONG) chay(PV_T, PV_N, QT[0], QT[1], e1 > 0, fabs(e1) > 3 * NGUONG ? 1000 : 300);
    }
    // 3) LCD: gio DS1307 + goc hai khop
    int ng, th, hh, mm, ss; docDS1307(ng, th, hh, mm, ss);
    char d1[17], d2[17];
    sprintf(d1, "%02d/%02d %02d:%02d:%02d", ng, th, hh, mm, ss);
    sprintf(d2, "ng=%+04.0f q=%+04.0f %s", docGoc(POT_NG, 0, 75),
            docGoc(POT_PV, -120, 120), S > S_MIN ? "OK" : "MAY");
    lcd.clear(); lcd.setCursor(0, 0); lcd.print(d1);
    lcd.setCursor(0, 1); lcd.print(d2);
    Serial.printf("%s S=%.0f e1=%+.0f e2=%+.0f\\n", d1, S, e1, e2);
  }
}"""

LAP_TRINH_CH3_CODE = [
    ("h2", "3.11. Code mẫu hoàn chỉnh của mô hình hai trục"),
    ("code", CODE_2TRUC),
    ("p", "Code hai trục giữ nguyên khung bản một trục và thêm ba điểm: khối thiên văn trả về cặp (α, γ) kèm chuẩn hóa bước nhảy 180°; nhánh tinh chỉnh xét e2 của khớp nghiêng trước rồi mới tới e1 của khớp phương vị; mỗi khớp có hàm chạy motor riêng với cặp công tắc hành trình của mình. Trạng thái khóa cầu H sau mỗi lệnh nhờ trục vít tự hãm giữ nguyên vị trí hai khớp."),
]

LAP_TRINH_H1_CH4 = "CHƯƠNG 4. TIẾN ĐỘ THỰC HIỆN VÀ KẾ HOẠCH TUẦN NÀY"
LAP_TRINH_CH4 = [
    ("h2", "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026"),
    ("b", "Hoàn thành cài Arduino IDE kèm lõi esp32 và nạp thử thành công lên ESP32 DevKit bản hai trục."),
    ("b", "Hoàn thành hàn hai cầu H, bốn kênh opto, khối nguồn và bus I²C chung cho DS1307 với LCD."),
    ("b", "Hoàn thành hiệu chuẩn bốn kênh LDR, hai biến trở hồi tiếp và kiểm thử liên động bốn công tắc hành trình."),
    ("b", "Hoàn thành viết và nạp code hybrid hai trục: đúng thứ tự nghiêng trước – phương vị sau, hiển thị đủ giờ và hai góc khớp lên LCD."),
    ("h2", "4.2. Các công việc còn lại của tuần này (5/10 – 10/10/2026)"),
    ("b", "Chạy ngoài trời trọn ngày nắng, đối chiếu log hai góc khớp với đồ thị mô phỏng ở quyển nghiên cứu."),
    ("b", "Tinh chỉnh ngưỡng e1/e2 và độ dài bước chạy để giảm số lần khởi động hai motor."),
    ("b", "Bổ sung chế độ gió lớn: đọc lịch và đưa tấm pin về vị trí nghỉ nằm ngang."),
]

# ---------- lien ket giua cac quyen (bo sung) ----------
NGHIEN_CUU_CH3.extend([
    ("h2", "3.6. Các nội dung sẽ triển khai ở quyển chế tạo và quyển lập trình"),
    ("b", "Quyển chế tạo: triển khai cấu trúc 3D ba tầng (đế xoay phương vị, khớp nâng nghiêng có đối trọng, khung mang pin) và cụm gá bốn LDR nghiêng β_s = 30° in liền khối; thi công hai mạch động lực cầu H bốn TIP41C và các sheet nguồn, RTC, LCD, hành trình theo đúng bộ tham số hybrid."),
    ("b", "Quyển chế tạo: tính chọn hai động cơ gạt nước cho tấm pin 100 W – 4 kg theo bảng mô-men gió từng khớp, kèm quy tắc đưa tấm pin về vị trí nghỉ nằm ngang khi gió vượt 8 m/s."),
    ("b", "Quyển lập trình: hiện thực ba nhánh hybrid cho hai khớp với thứ tự tinh chỉnh nghiêng trước – phương vị sau; đọc ADC sáu kênh có lọc và K_cal; điều khiển hai cầu H tích cực thấp; đọc DS1307, hiển thị LCD I2C, đọc hai biến trở; lưu đồ từng phần và tổng quát; code mẫu hai trục hoàn chỉnh."),
    ("b", "Cả hai quyển dùng ma trận tính toán (α, γ) theo giờ ở chương 4 làm bảng kiểm tra chéo đầu ra khối thiên văn của code khi chạy thử không tải."),
])
CHE_TAO_CH1.extend([
    ("h2", "1.5. Tổng hợp các kết quả tiếp nhận từ quyển nghiên cứu"),
    ("tbl", [
        ["Nội dung đã chốt ở quyển nghiên cứu", "Giá trị", "Áp dụng trong quyển chế tạo"],
        ["Phương pháp điều khiển", "Hybrid hai khớp: thiên văn thô + LDR tinh chỉnh (e2 nghiêng trước, e1 phương vị sau) + giữ vị trí khi mây mù", "Nguyên lý mục 1.1 và sơ đồ khối mục 1.2."],
        ["Ngưỡng phát lệnh / vùng chết", "|e| > 200 / dừng dưới 120 mức ADC", "Mạch chia áp, cài liên động từng khớp."],
        ["Ngưỡng mây mù S_min", "Tổng 4 kênh < 2500", "Nhánh giữ vị trí theo lịch."],
        ["Góc gá cảm biến", "β_s = 30°, chỉ nghiêng quang trở, không vách ngăn", "Khối gá LDR in 3D liền khối."],
        ["So sánh ba luật", "Hybrid sai số trung bình 2,9°, 83 lần chạy motor/ngày", "Căn cứ chọn motor và độ cứng khớp 3D."],
        ["Lợi ích năng lượng", "Hai trục +50…351% so tấm cố định, hơn một trục rõ nhất mùa đông", "Quyết định đầu tư khớp nghiêng thứ hai."],
        ["Ma trận (α, γ) theo giờ và bước nhảy 180° trưa hạ chí", "Chương 4 quyển nghiên cứu", "Bảng kiểm tra chéo góc đặt hai khớp."],
    ], "{B}. Các kết quả tiếp nhận từ quyển nghiên cứu và cách áp dụng"),
])
LAP_TRINH_CH2.extend([
    ("h2", "2.5. Các tham số và kết quả kế thừa từ quyển nghiên cứu"),
    ("tbl", [
        ["Đại lượng", "Giá trị chốt trong quyển nghiên cứu", "Dùng trong code"],
        ["Chu kỳ thiên văn / LDR", "30 phút / 2 phút", "T_TV = 1800000 ms; T_LDR = 120000 ms."],
        ["Ngưỡng / vùng chết", "|e| > 200 / 120 mức ADC", "Hằng số NGUONG và điều kiện dừng."],
        ["Ngưỡng mây mù S_min", "2500 (tổng bốn kênh)", "Nhánh giữ vị trí cả hai khớp."],
        ["Thứ tự tinh chỉnh", "Khớp nghiêng (e2) trước, phương vị (e1) sau", "Thứ tự gọi trong nhánh LDR của loop()."],
        ["Góc gá cảm biến β_s", "30°, chỉ nghiêng quang trở", "Cơ sở hiệu chuẩn K_cal bốn kênh."],
        ["Sai số luật hybrid", "2,9° trung bình; 83 lần chạy motor/ngày", "Mốc so sánh log đo ngoài trời."],
        ["Ma trận (α, γ) và chuẩn hóa 180°", "Chương 4 quyển nghiên cứu", "Hàm thienVan() và bảng đối chiếu."],
    ], "{B}. Tham số kế thừa từ quyển nghiên cứu đưa vào chương trình hai trục"),
])
