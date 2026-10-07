# -*- coding: utf-8 -*-
"""Nguồn nội dung biên tập cho sáu quyển.

Nội dung chuyên môn được phân công theo đúng chủ đề; các kết quả đo phần cứng
chưa có bằng chứng được ghi là chưa thực hiện.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mo_phong as sim
import thong_so_chung as spec

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _fmt(value, digits=1):
    return f"{value:.{digits}f}".replace(".", ",")


def _common_ch1(report, volume):
    config = "một trục" if report == 1 else "hai trục"
    role = {"Nghien_cuu": "mô hình và kết quả tính toán/mô phỏng",
            "Che_tao": "giao diện thiết kế cơ khí–điện và kế hoạch xác minh",
            "Lap_trinh": "phần mềm thuộc phạm vi quyển lập trình"}[volume]
    return [
        ("h1", "CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI"),
        ("h2", "1.1. Bối cảnh"),
        ("p", "Góc chiếu Mặt Trời thay đổi theo ngày và giờ; hệ bám nắng cần thống nhất dấu góc, cảm biến, hành trình và trạng thái an toàn trước khi tích hợp. Bộ đồ án có hai cấu hình riêng: một trục và hai trục."),
        ("h2", "1.2. Mục tiêu và cấu hình"),
        ("p", f"Quyển này thuộc cấu hình {config}, đảm nhiệm {role}. Bảng thông số chung một trang được đặt trước sáu báo cáo và là nguồn chuẩn cho các hằng số, chân, chu kỳ và giới hạn [1]."),
        ("h2", "1.3. Ranh giới nội dung và bằng chứng"),
        ("p", "Nghiên cứu giữ công thức/mô phỏng; Chế tạo giữ kết cấu, giao diện, tải và kế hoạch đo; Lập trình giữ thuật toán/code theo phần được giao. Quyển không sở hữu nội dung chuyên môn sẽ dẫn chiếu thay vì chép lại. Chưa có biên bản xác nhận lắp ráp, hiệu chuẩn hoặc thử nghiệm phần cứng; mọi số liệu tính toán/mô phỏng được ghi nhãn riêng."),
    ]


def _refs(kind):
    refs = ["[1] Nhóm thực hiện, Bảng thông số chung hệ thống bám nắng, phiên bản 1.0, cập nhật 07/10/2026."]
    if kind == "solar":
        refs += ["[2] NOAA Global Monitoring Laboratory, Solar Calculation Details, phương trình thời gian và góc Mặt Trời, https://gml.noaa.gov/grad/solcalc/solareqns.PDF."]
    elif kind == "hardware":
        refs += ["[2] Espressif Systems, ESP32 Series Datasheet, https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf.",
                 "[3] onsemi, TIP41C NPN Silicon Power Transistor Datasheet, https://www.onsemi.com/pdf/datasheet/tip41c-d.pdf."]
    elif kind == "program":
        refs += ["[2] Espressif Systems, ESP32 Series Datasheet, https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf."]
    elif kind == "solar_code":
        refs += ["[2] NOAA Global Monitoring Laboratory, Solar Calculation Details, phương trình thời gian và góc Mặt Trời, https://gml.noaa.gov/grad/solcalc/solareqns.PDF.",
                 "[3] Espressif Systems, ESP32 Series Datasheet, https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf.",
                 "[4] Maxim Integrated/Analog Devices, DS1307 64 x 8 Serial I2C Real-Time Clock Datasheet, https://www.analog.com/media/en/technical-documentation/data-sheets/ds1307.pdf."]
    return [("h1", "TÀI LIỆU THAM KHẢO")] + [("b", r) for r in refs]


def _matrix_rows(field):
    rows = [["Giờ Mặt Trời", "21/3", "21/6", "23/9", "21/12"]]
    for hour in range(6, 19):
        row = [f"{hour:02d}:00"]
        for _name, day in spec.DAYS:
            alpha, gamma = spec.solar_angles(day, float(hour))
            value = alpha if field == "alpha" else gamma
            row.append(_fmt(value, 1) + "°")
        rows.append(row)
    return rows


def _wind_rows(two_axis=False):
    if two_axis:
        rows = [["V (m/s)", "M_az (N·m)", "M_beta (N·m)", "20/M_az", "20/M_beta"]]
        for r in spec.wind_table(True):
            rows.append([_fmt(r["speed_m_s"], 0), _fmt(r["azimuth_design_nm"], 2),
                         _fmt(r["tilt_design_nm"], 2), _fmt(r["azimuth_ratio_assumed"], 2),
                         _fmt(r["tilt_ratio_assumed"], 2)])
        return rows
    rows = [["V (m/s)", "M_az thiết kế (N·m)", "20/M_az giả định"]]
    for r in spec.wind_table(False):
        rows.append([_fmt(r["speed_m_s"], 0), _fmt(r["azimuth_design_nm"], 2),
                     _fmt(r["azimuth_ratio_assumed"], 2)])
    return rows


def _control_rows(axes):
    rows = [["Luật (mô hình %s trục)" % axes, "Sai số TB (°)", "Sai số max (°)", "Lệnh motor mô phỏng"]]
    for mode, label in (("openloop", "Thiên văn 30 phút"), ("closedloop", "LDR 2 phút"), ("hybrid", "Hybrid")):
        result = sim.simulate_day(80, mode, axes=axes)
        rows.append([label, _fmt(result["mean_error_deg"], 2),
                     _fmt(result["max_error_deg"], 2), str(result["motor_commands"])])
    return rows


def _research1():
    gains = sim.energy_gains()
    gain_rows = [["Ngày", "Một trục so với pin cố định (proxy trực xạ)"]]
    for name, _day in spec.DAYS:
        gain_rows.append([name, "+" + _fmt(gains[name]["gain_one_axis_percent"], 1) + "%"])
    return _common_ch1(1, "Nghien_cuu") + [
        ("h1", "CHƯƠNG 2. CƠ SỞ TÍNH TOÁN VÀ MÔ HÌNH MỘT TRỤC"),
        ("h2", "2.1. Quy ước tọa độ và công thức thiên văn"),
        ("p", "Dùng alpha là góc cao từ chân trời; gamma=0° hướng Nam, gamma dương về Tây. Giờ RTC là giờ dân dụng Việt Nam, phải đổi sang giờ Mặt Trời theo UTC+7, kinh độ tham chiếu và phương trình thời gian. Công thức số và quy ước dấu xem Bảng thông số chung [1] và tài liệu [2]."),
        ("eq", "delta=23,45°·sin[360°(284+n)/365]; H=15°(t_solar−12)"),
        ("eq", "sin(alpha)=sin(phi)sin(delta)+cos(phi)cos(delta)cos(H)"),
        ("eq", "gamma=atan2(sin(H), sin(phi)cos(H)−tan(delta)cos(phi))"),
        ("p", "gamma được giữ trong nhánh atan2 (−180°,180°]; không ép về ±90°. Tại trưa hạ chí ở vĩ độ tham chiếu, gamma xấp xỉ 180° là hướng Bắc, không phải 0°."),
        ("h2", "2.2. Hình học khớp một trục"),
        ("p", "Véc-tơ Mặt Trời dùng x hướng Tây, y hướng Bắc, z hướng lên. Với trục cơ khí Bắc–Nam, pháp tuyến quay trong mặt phẳng Đông–Tây; góc pháp tuyến lý tưởng theta=atan2(cos(alpha)sin(gamma),sin(alpha)), dương về Tây; góc actuator được kẹp trong ±85° theo giả thiết hành trình. Không bao gồm backlash, quán tính hoặc tốc độ motor."),
        ("eq", "theta_cmd=clamp(atan2(cos(alpha)sin(gamma),sin(alpha)), −85°, +85°)"),
        ("h2", "2.3. Ranh giới với cảm biến"),
        ("p", "Quyển Nghiên cứu sở hữu công thức thiên văn và mô hình một trục. Cách đọc bốn LDR, lọc mẫu và tính e1/e2 thuộc duy nhất quyển Lập trình đồ án 1; không chép code ADC ở đây."),
        ("img", "hinh_ve/so_do_3_phuong_phap.png", "{H}. Ba nhóm phương pháp; phần lọc ADC/e1/e2 giao cho Lập trình đồ án 1"),
        ("h1", "CHƯƠNG 3. KẾT QUẢ TÍNH VÀ MÔ PHỎNG MỘT TRỤC"),
        ("h2", "3.1. Quỹ đạo thiên văn tại Mỹ Hào"),
        ("p", "Tính với vĩ độ tham chiếu 20,93°B, các ngày đại diện 21/3, 21/6, 23/9, 21/12 và giờ Mặt Trời. Đây là kết quả công thức, không phải phép đo ngoài trời."),
        ("img", "hinh_ve/duong_di_mat_troi_1_truc.png", "{H}. Quỹ đạo alpha/gamma dùng chung; gamma giữ nguyên nhánh ±180°"),
        ("h2", "3.2. So sánh ba luật trên mô hình một trục"),
        ("p", "Mô phỏng một ngày 21/3, bước 1 phút, mây 10–11h và nhiễu LDR tổng hợp; motor được giả định tức thời. Sai số trục chỉ tính khi alpha≥5° và tổng sáng mô hình S≥S_min, loại thời điểm rạng/hoàng hôn dưới ngưỡng. Sai số là góc giữa target một trục và trục mô phỏng; số lệnh là số lần cập nhật, không phải số liệu đo."),
        ("tbl", _control_rows(1), "{B}. Sai số góc và số lệnh – dữ liệu mô phỏng một trục"),
        ("img", "hinh_ve/hoat_dong_hybrid_1_truc.png", "{H}. Góc trục trong mô phỏng hybrid một trục, mây tổng hợp 10–11h"),
        ("h2", "3.3. Proxy trực xạ so với pin cố định"),
        ("p", "Tích phân max(0,n_sun·n_panel) theo ngày cho tấm cố định có mặt phẳng nghiêng 21° so với ngang (pháp tuyến cao 69°), hướng Nam, và trục đơn lý tưởng giới hạn ±85°. Proxy hình học này không phải kWh, điện năng hoặc hiệu suất điện thực."),
        ("img", "hinh_ve/so_sanh_nang_luong_1_truc.png", "{H}. Mức thay đổi proxy trực xạ một trục so với tấm cố định"),
        ("tbl", gain_rows, "{B}. Proxy hình học một trục; không phải số đo điện"),
        ("h2", "3.4. Hạn chế"),
        ("b", "Mô hình chưa xét mây biến thiên theo không gian, bức xạ khuếch tán, bóng che, tốc độ motor, backlash, tải gió hoặc công suất tiêu thụ."),
        ("b", "Chưa thực hiện, dự kiến trước %s: đối chiếu giờ Mặt Trời/tọa độ tại nơi lắp và đo góc trục bằng dụng cụ tham chiếu." % spec.PLAN_DATE),
        ("h1", "CHƯƠNG 4. MA TRẬN GÓC VÀ TRẠNG THÁI CÔNG VIỆC"),
        ("h2", "4.1. Ma trận góc cao alpha"),
        ("p", "Bảng được xuất tự động từ cùng hàm solar_angles, giờ Mặt Trời 06:00–18:00. Các ngày và giờ dùng chung với ma trận gamma."),
        ("tbl", _matrix_rows("alpha"), "{B}. Ma trận alpha (độ), một công thức thống nhất [1,2]"),
        ("h2", "4.2. Ma trận phương vị gamma"),
        ("p", "Gamma=0° hướng Nam, Tây dương. Giá trị 180° được giữ nguyên; giới hạn cơ khí không làm đổi bảng góc thiên văn."),
        ("tbl", _matrix_rows("gamma"), "{B}. Ma trận gamma (độ), cùng hàm atan2; không gập mất 180°"),
        ("h2", "4.3. Công việc đã làm/chưa làm"),
        ("b", "Đã chạy lại công thức, mô phỏng một trục và xuất bảng/đồ thị từ mã nguồn trong repository."),
        ("b", "Chưa có phép đo góc, điện năng, dòng motor hoặc thử ngoài trời; dự kiến hoàn thành trước %s." % spec.PLAN_DATE),
    ] + _refs("solar")


def _fabrication(report):
    two = report == 2
    if not two:
        motor_table = [["Khối", "Cấu hình đề xuất", "Tình trạng xác minh"],
                       ["Bộ điều khiển", "ESP32 DevKit", "Chưa xác nhận bo/as-built."],
                       ["Cảm biến", "Bốn LDR; gá nghiêng beta_s=30°", "Chưa hiệu chuẩn thực."],
                       ["Chấp hành", "1 motor gạt mưa 12 V trục vít, phương vị", "Nhãn 60 W/mô-men cần xác minh."],
                       ["Cầu H", "Một mạch 4 TIP41C + opto", "Chưa thử tải/nhiệt; xem datasheet [3]."],
                       ["Hồi tiếp/limit", "1 biến trở; 2 công tắc AZ", "Chưa kiểm tra trên mạch thực."],
                       ["RTC/LCD", "DS1307 + LCD1602/PCF8574", "Địa chỉ 0x68/0x27 tham khảo."]]
        blocks = _common_ch1(1, "Che_tao") + [
            ("h1", "CHƯƠNG 2. GIAO DIỆN CHẾ TẠO VÀ TẢI MỘT TRỤC"),
            ("h2", "2.1. Sơ đồ khối và chân giao tiếp"),
            ("p", "Các hình là sơ đồ chức năng/pinout đề xuất, không phải sơ đồ mạch as-built hoặc bằng chứng đã lắp. Thuật toán ADC/code thuộc quyển Lập trình đồ án 1."),
            ("img", "hinh_ve/so_do_khoi_1_truc.png", "{H}. Sơ đồ khối một trục; phương án chức năng"),
            ("img", "hinh_ve/so_do_ket_noi_1_truc.png", "{H}. Pinout một trục đề xuất; cần đối chiếu bo và dây thật"),
            ("img", "hinh_ve/bo_tri_4_ldr.png", "{H}. Bố trí bốn LDR; beta_s=30° là giả thiết, chưa hiệu chuẩn"),
            ("tbl", motor_table, "{B}. Giao diện phần cứng một trục; chưa xác nhận lắp ráp"),
            ("h2", "2.2. Motor, cầu H và dòng tham khảo"),
            ("p", "Chỉ có một motor phương vị trong cấu hình này. Nếu nhãn 60 W/12 V là công suất điện vào thì P/V xấp xỉ 5 A cho motor; đây là phép tính tham khảo chưa đo, chưa gồm dòng khởi động/kẹt. TIP41C có giới hạn cực đại theo datasheet nhưng không chứng minh mạch chịu 5 A liên tục."),
            ("p", "Tự hãm của trục vít phải xác minh bằng thử tải; không coi là phanh an toàn. Cách điều khiển active-low và liên động được trình bày ở quyển Lập trình đồ án 2 để không lặp lý thuyết cầu H."),
            ("h2", "2.3. Mô-men tải gió – chỉ khớp phương vị"),
            ("p", "Giả thiết tính sơ bộ: A=0,65 m², rho=1,2 kg/m³, Cd=1,2, tay đòn azimuth 0,30 m, hệ số thiết kế 1,5. M=1,5·(0,5·rho·V²·Cd·A)·r. Không cộng mô-men nghiêng hoặc dòng của motor thứ hai vào quyển một trục."),
            ("tbl", _wind_rows(False), "{B}. Mô-men phương vị một trục; tỷ số dùng 20 N·m giả định"),
            ("p", "20 N·m là giả thiết mô-men kẹt, chưa xác minh và không phải mô-men liên tục. Ở 10 m/s mô-men thiết kế vượt giả thiết này; chưa chứng minh cơ cấu đạt tải."),
            ("h1", "CHƯƠNG 3. BẰNG CHỨNG CHẾ TẠO VÀ KẾ HOẠCH XÁC MINH"),
            ("h2", "3.1. Ranh giới hồ sơ"),
            ("p", "Chưa có hồ sơ as-built hoặc biên bản xác nhận cơ cấu một trục được lắp đúng cấu hình trên. Không dùng phối cảnh/render làm ảnh sản phẩm thật."),
            ("h2", "3.2. Bảng kiểm thử/đo đạc"),
            ("tbl", [["Hạng mục", "Tình trạng", "Kế hoạch"],
                     ["Lắp cơ khí/hành trình", "Chưa xác nhận.", "Chưa thực hiện, dự kiến trước %s: kiểm tra hành trình và lập biên bản." % spec.PLAN_DATE],
                     ["Hiệu chuẩn LDR/POT", "Chưa có dữ liệu gốc.", "Chưa thực hiện, dự kiến trước %s: lưu 16 mẫu/kênh tại góc chuẩn." % spec.PLAN_DATE],
                     ["Dòng/mô-men motor", "Chưa đo.", "Chưa thực hiện, dự kiến trước %s: đo tải và dòng khởi động bằng thiết bị phù hợp." % spec.PLAN_DATE],
                     ["Cầu H/nhiệt", "Chưa thử bench.", "Chưa thực hiện, dự kiến trước %s: thử bảo vệ, đảo chiều, sụt áp và nhiệt." % spec.PLAN_DATE],
                     ["Ngoài trời", "Chưa thử.", "Chưa thực hiện, dự kiến trước %s: ghi dữ liệu hệ thống và tham chiếu đồng thời." % spec.PLAN_DATE]],
                    "{B}. Kế hoạch xác minh; không phải kết quả đo"),
            ("h2", "3.3. Hạn chế"),
            ("b", "Diện tích/tâm áp lực/tay đòn và tải liên kết chưa được xác nhận từ CAD hoặc phép đo lực."),
            ("b", "Chưa có bằng chứng phanh gió, tự hãm, hiệu chuẩn hoặc đo dòng; mọi giá trị tải là tham khảo."),
            ("h1", "CHƯƠNG 4. TIẾN ĐỘ"),
            ("b", "Đã tính mô-men phương vị trên máy tính bằng bộ giả thiết công bố; chưa phải nghiệm thu kết cấu."),
            ("b", "Chưa thực hiện, dự kiến trước %s: chốt bản vẽ as-built, xác nhận tay đòn/diện tích/khối lượng, đo tải và kiểm thử an toàn." % spec.PLAN_DATE),
        ]
    else:
        motor_table = [["Khớp/tín hiệu", "Cấu hình và GPIO đề xuất", "Trạng thái"],
                       ["Phương vị", "Motor 12 V; AZ_THUAN 19, AZ_NGUOC 18; POT 36", "Chưa xác nhận đấu nối."],
                       ["Nâng", "Motor 12 V; TILT_LEN 16, TILT_XUONG 13; POT 4", "GPIO2 loại do strap; GPIO5 tránh."],
                       ["LDR/limit", "LDR 25/26/27/14; limit 34/35/32/33", "ADC2 cần tắt Wi-Fi; GPIO34–39 chỉ input."],
                       ["RTC/LCD/E-stop", "I²C 21/22; DS1307 0x68; LCD 0x27; ESTOP 23", "NC-to-GND; HIGH khi nhấn/đứt dây; chưa xác minh."]]
        blocks = _common_ch1(2, "Che_tao") + [
            ("h1", "CHƯƠNG 2. GIAO DIỆN CƠ KHÍ–ĐIỆN HỆ HAI TRỤC"),
            ("h2", "2.1. Sơ đồ và chân đề xuất"),
            ("p", "Sơ đồ khối/pinout dưới đây không phải schematic EasyEDA hoàn chỉnh hoặc hồ sơ as-built. Phương án tránh GPIO2 do chân strapping khi reset/khởi động; mức tải trên chân này có thể làm boot sai. POT nghiêng chuyển sang GPIO4 (ADC2, tắt Wi-Fi). GPIO5 cũng tránh cho tín hiệu mới. GPIO34–39 chỉ input và không có pull-up/down nội; hai limit trên GPIO34/35 cần điện trở bias ngoài."),
            ("img", "hinh_ve/so_do_khoi_2_truc.png", "{H}. Sơ đồ khối hai trục; chưa phải sơ đồ nguyên lý"),
            ("img", "hinh_ve/so_do_ket_noi_2_truc.png", "{H}. Pinout hai trục đề xuất; xác nhận chân theo biến thể bo"),
            ("tbl", motor_table, "{B}. Bảng giao diện hai khớp và GPIO; chưa xác nhận lắp"),
            ("h2", "2.2. Giả thiết kết cấu và hành trình"),
            ("p", "Beta là cao độ pháp tuyến tấm pin từ mặt phẳng ngang (mặt pin nghiêng 90°−beta) và beta_cmd=clamp(alpha,0°…75°); không nhầm beta pháp tuyến với độ nghiêng mặt phẳng pin. Tại điểm tham chiếu, trưa 21/6 alpha≈87,5°, nên lệnh bão hòa ở 75° (chênh ≈12,5°); đây là giới hạn thiết kế, không phải nhầm quy ước góc. Chưa xác nhận bằng CAD hoặc công tắc thật rằng khớp đạt 75°. Gamma actuator giới hạn ±120°. Kích thước, khối lượng 4 kg và tay đòn chưa xác nhận bằng CAD."),
            ("h2", "2.3. Mô-men theo từng khớp"),
            ("p", "Dùng q=0,5·rho·V²; F=q·Cd·A. Phương vị M_az=1,5·F·0,30. Khớp nâng M_beta=1,5·(F·0,20+3 N·m) với 3 N·m là mô-men trọng lực dư giả định."),
            ("tbl", _wind_rows(True), "{B}. Mô-men thiết kế tham khảo riêng từng khớp; 20 N·m chưa xác minh"),
            ("p", "Ở 8 m/s, M_az≈13,48 N·m và M_beta≈13,49 N·m; ở 10 m/s lần lượt khoảng 21,06 và 18,54 N·m. So sánh với 20 N·m giả định không chứng minh motor đạt vì đó là mô-men kẹt giả định, không phải mô-men liên tục."),
            ("h2", "2.4. Dòng và mạch công suất"),
            ("p", "Nếu nhãn 60 W/12 V là công suất điện vào thì khoảng 5 A/motor; hai motor khoảng 10 A tổng trước dòng khởi động/kẹt và tổn hao. Chưa đo dòng. TIP41C 6 A max không chứng minh mạch chịu được tải; cần xác minh datasheet/SOA/nhiệt hoặc chọn driver phù hợp [2,3]."),
            ("h1", "CHƯƠNG 3. HỒ SƠ VÀ KẾ HOẠCH XÁC MINH"),
            ("h2", "3.1. Trạng thái thiết kế"),
            ("p", "Chưa có sơ đồ mạch hai trục as-built, bản vẽ kích thước/collision-check hoặc ảnh xác nhận hệ hai trục đã chế tạo. Không dùng ảnh một trục làm bằng chứng cho cấu hình này."),
            ("h2", "3.2. Bảng kiểm thử/đo đạc"),
            ("tbl", [["Hạng mục", "Bằng chứng hiện có", "Kế hoạch"],
                     ["CAD/hành trình", "Chưa có bản vẽ as-built.", "Chưa thực hiện, dự kiến trước %s: dựng CAD và kiểm tra va chạm." % spec.PLAN_DATE],
                     ["Mạch 2 cầu H", "Chưa có schematic/biên bản.", "Chưa thực hiện, dự kiến trước %s: hoàn thiện schematic, rà strap/driver." % spec.PLAN_DATE],
                     ["Dòng/mô-men", "Chưa đo; 20 N·m là giả thiết.", "Chưa thực hiện, dự kiến trước %s: đo độc lập từng khớp và dòng khởi động/kẹt." % spec.PLAN_DATE],
                     ["Hiệu chuẩn", "Chưa có dữ liệu gốc.", "Chưa thực hiện, dự kiến trước %s: hiệu chuẩn hai POT, LDR và limit." % spec.PLAN_DATE],
                     ["Ngoài trời", "Chưa thử.", "Chưa thực hiện, dự kiến trước %s: ghi góc/lệnh/dòng/thời tiết." % spec.PLAN_DATE]],
                    "{B}. Kế hoạch xác minh; không phải kết quả thử"),
            ("h2", "3.3. Hạn chế và an toàn"),
            ("b", "Cần xác minh tay đòn, trọng tâm, đối trọng, liên kết, phanh và driver từ CAD/đo lực trước vận hành."),
            ("b", "E-stop GPIO23 chỉ là đầu vào phần mềm dự kiến; cần tiếp điểm phần cứng NC cắt enable/nguồn độc lập."),
            ("h1", "CHƯƠNG 4. TIẾN ĐỘ"),
            ("b", "Đã tính lại tải từng khớp trên máy tính theo giả thiết công bố; không phải nghiệm thu kết cấu."),
            ("b", "Chưa thực hiện, dự kiến trước %s: hoàn thiện CAD/schematic, chế tạo, đo dòng/mô-men và kiểm tra an toàn." % spec.PLAN_DATE),
        ]
    return blocks + _refs("hardware")


def _programming1():
    code = r'''// Module LDR – nội dung chi tiết duy nhất của Lập trình đồ án 1
#include <Arduino.h>
#include <algorithm>
#include "ldr_module.h" // giao diện dùng chung ở firmware/ldr_module.h

const uint8_t LDR_PIN[4] = {25, 26, 27, 14}; // ET, WT, EB, WB (ADC2)
const uint8_t N_SAMPLE = 16;
const int32_t ADC_MAX = 4095, START_THRESHOLD = 200, STOP_DEADBAND = 120;
const int32_t S_MIN = 2500;
float K_cal[4] = {1.0f, 1.0f, 1.0f, 1.0f}; // chưa hiệu chuẩn
void initLdrAdc() {
  analogReadResolution(12);
  for (uint8_t i=0; i<4; ++i) pinMode(LDR_PIN[i], INPUT);
  // Cấu hình attenuation phù hợp board/Arduino-ESP32; không vượt 3,3 V ở chân.
}

uint16_t readTrimmed(uint8_t pin) {
  uint16_t samples[N_SAMPLE];
  for (uint8_t i=0; i<N_SAMPLE; ++i) {
    samples[i] = analogRead(pin);
    delayMicroseconds(250);
  }
  std::sort(samples, samples + N_SAMPLE);
  uint32_t total = 0;
  for (uint8_t i=2; i<N_SAMPLE-2; ++i) total += samples[i];
  return total / 12; // bỏ 2 thấp + 2 cao, trung bình 12
}

LdrResult readLdrMatrix() {
  int32_t v[4];
  for (uint8_t i=0; i<4; ++i) {
    const int32_t scaled=(int32_t)roundf(readTrimmed(LDR_PIN[i])*K_cal[i]);
    v[i]=constrain(scaled,0,ADC_MAX);
  }
  // e1 dương: phía Đông sáng hơn; e1 âm: phía Tây sáng hơn.
  const int32_t e1 = (v[0]+v[2]) - (v[1]+v[3]);
  // e2 dương: phía trên sáng hơn; e2 âm: phía dưới sáng hơn.
  const int32_t e2 = (v[0]+v[1]) - (v[2]+v[3]);
  return {e1, e2, v[0]+v[1]+v[2]+v[3]};
}

bool hysteresisTrack(int32_t error, bool &active) {
  if (!active && abs(error) >= START_THRESHOLD) active = true;
  if (active && abs(error) <= STOP_DEADBAND) active = false;
  return active;
}

bool ldrHasEnoughLight(const LdrResult &r) {
  return r.sum >= S_MIN; // nếu thiếu sáng: caller dừng và giữ góc hiện tại
}
'''
    blocks = _common_ch1(1, "Lap_trinh") + [
        ("h1", "CHƯƠNG 2. ĐỌC ADC VÀ XỬ LÝ MA TRẬN LDR"),
        ("h2", "2.1. Phạm vi module cảm biến"),
        ("p", "Quyển này sở hữu đọc bốn kênh LDR, lọc mẫu, K_cal và e1/e2. Header giao diện dùng chung duy nhất là firmware/ldr_module.h; thuật toán ADC chỉ đặt tại quyển này. Công thức thiên văn ở Nghiên cứu đồ án 1; chân, nguồn, phần cứng ở Chế tạo đồ án 1/2. Không lặp code motor, RTC hay LCD."),
        ("h2", "2.2. Sơ đồ cảm biến và ADC"),
        ("p", "ET/WT/EB/WB lần lượt là Đông-trên, Tây-trên, Đông-dưới, Tây-dưới. GPIO25/26/27/14 là ADC2; phải tắt Wi-Fi, không đưa điện áp chân vượt 3,3 V. Mã ADC 12-bit 0…4095; dải hữu ích còn tùy suy hao và từng chip."),
        ("h2", "2.3. Lọc mẫu và chuẩn hóa"),
        ("p", "Mỗi kênh đọc 16 mẫu; bỏ 2 cực tiểu và 2 cực đại, lấy trung bình 12 mẫu. K_cal từng kênh khởi tạo 1,0 chỉ là placeholder. Hiệu chuẩn thực phải lưu số liệu gốc ở nhiều mức sáng/góc, chưa thực hiện."),
        ("h2", "2.4. Sai lệch và vùng chết"),
        ("eq", "e1=(ET+EB)−(WT+WB);    e2=(ET+WT)−(EB+WB)"),
        ("p", "e1 dương nghĩa phía Đông sáng hơn; e1 âm yêu cầu quay Tây. e2 dương yêu cầu nâng; e2 âm yêu cầu hạ. Bắt đầu tinh chỉnh khi |e|≥200 count; dừng khi |e|≤120 count. Chỉ khớp nghiêng của hệ hai trục dùng e2; điều khiển nghiêng thuộc quyển Lập trình đồ án 2."),
        ("h1", "CHƯƠNG 3. CODE MẪU VÀ KIỂM THỬ"),
        ("h2", "3.1. Trích đoạn đọc ma trận LDR"),
        ("p", "Đây là module tham khảo để trả LdrResult cho quyển Lập trình đồ án 2; chưa nạp lên ESP32, chưa thay thế hiệu chuẩn hoặc kiểm thử mạch."),
        ("img", "hinh_ve/luu_do_doc_adc.png", "{H}. Lọc ADC, K_cal, e1/e2 thuộc Lập trình đồ án 1"),
        ("code", code),
        ("h2", "3.2. Bảng kiểm thử"),
        ("tbl", [["Hạng mục", "Đã kiểm tra", "Bằng chứng/trạng thái"],
                 ["Dấu e1/e2", "Unit test dữ liệu tổng hợp.", "Đã kiểm tra số học phần mềm; chưa thử cảm biến."],
                 ["Bộ lọc 16 mẫu", "Kiểm tra bỏ 2 thấp/2 cao.", "Đã kiểm tra logic; chưa có dữ liệu ADC thực."],
                 ["K_cal/độ lặp", "Chưa đo.", "Chưa thực hiện, dự kiến trước %s." % spec.PLAN_DATE],
                 ["S_min/ngưỡng góc", "Chưa hiệu chuẩn.", "Chưa thực hiện, dự kiến trước %s." % spec.PLAN_DATE],
                 ["ESP32 ADC2/Wi-Fi", "Chưa nạp/chạy bo thật.", "Chưa thực hiện, dự kiến trước %s." % spec.PLAN_DATE]],
                "{B}. Kiểm tra phần mềm và việc phần cứng còn thiếu"),
        ("h2", "3.3. Hạn chế"),
        ("b", "Mô hình LDR tổng hợp không thay thế sai số cảm biến, điện trở chia áp, hướng đặt, bóng che hoặc đặc tính phổ."),
        ("b", "Chưa thực hiện, dự kiến trước %s: hiệu chuẩn bốn kênh, kiểm tra bão hòa ADC và chốt S_min bằng dữ liệu đã lưu." % spec.PLAN_DATE),
        ("h1", "CHƯƠNG 4. TIẾN ĐỘ"),
        ("b", "Đã viết module đọc/lọc và chạy unit test dữ liệu số tổng hợp; chưa đo cảm biến thật."),
        ("b", "Chưa thực hiện, dự kiến trước %s: ghi ADC thô từng kênh, sai số góc và điều kiện chiếu sáng." % spec.PLAN_DATE),
    ]
    return blocks + _refs("program")


def _programming2():
    code = r'''// Mẫu tích hợp thời gian/điều khiển hai trục – không phải firmware đã nạp
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "ldr_module.h"                   // giao diện LdrResult/readLdrMatrix từ quyển 3

const uint8_t AZ_THUAN=19, AZ_NGUOC=18;
const uint8_t TILT_LEN=16, TILT_XUONG=13;
const uint8_t POT_AZ=36, POT_TILT=4;        // GPIO2 bị loại vì strap khi boot
const uint8_t LIM[4]={34,35,32,33};
const uint8_t ESTOP=23;                     // tiếp điểm NC kéo GND
const uint32_t T_ASTRO=1800000UL;           // target thiên văn: 30 phút
const uint32_t T_LIGHT=1000UL;              // kiểm tra thiếu sáng: 1 giây
const uint32_t T_LDR=120000UL;              // hiệu chỉnh e1/e2: 2 phút
const uint32_t T_LCD=1000UL;                // LCD: 1 giây, timer độc lập
const uint32_t T_CMD_MAX_MS=8000UL, T_POLL_MS=10UL;
const int32_t S_MIN=2500, START_THRESHOLD=200, STOP_DEADBAND=120;
const float PHI=20.93f, LON=106.10f, AZ_MIN=-120, AZ_MAX=120;
const float BETA_MIN=0, BETA_MAX=75;
bool azLatchedToNight=false;
LiquidCrystal_I2C lcd(0x27,16,2);

struct CivilTime { int day, month, year, hour, minute, second; };
struct SunPosition { float alphaDeg, gammaDeg; };
uint32_t lastLightPoll=0,lastLdrAdjust=0,lastAstro=0,lastLCD=0,lastMotorPoll=0;
bool astroInitialized=false;
LdrResult latestLdr={0,0,0};
void updateLCD(const CivilTime &, const char *status); // giao diện hiển thị
void updateAstronomyTarget(const SunPosition &);      // beta clamp, gamma limit/latch
void updateLdrCorrection(const LdrResult &);          // giao diện e1/e2 từ quyển 3
void pollFeedbackLimitsAndMotor();                   // state machine không blocking

void stopPair(uint8_t a,uint8_t b) { digitalWrite(a,HIGH); digitalWrite(b,HIGH); }
void stopAllMotors() {
  stopPair(AZ_THUAN,AZ_NGUOC); stopPair(TILT_LEN,TILT_XUONG);
}
void configureSafetyInput() { pinMode(ESTOP,INPUT_PULLUP); } // NC-GND: LOW bình thường
bool motorRunGuard(uint32_t startMs, bool targetLimitHit) {
  // targetLimitHit đã debounce; NC mở/nhấn/đứt dây => HIGH; timeout tối đa 8 s.
  if (digitalRead(ESTOP)==HIGH || targetLimitHit || uint32_t(millis()-startMs)>=T_CMD_MAX_MS) {
    stopAllMotors(); return false;
  }
  return true;
}
void setPair(uint8_t a,uint8_t b,bool positive) {
  stopPair(a,b); delay(25);                    // break-before-make
  digitalWrite(a,positive?LOW:HIGH);
  digitalWrite(b,positive?HIGH:LOW);           // không bao giờ LOW/LOW
}

bool readDs1307(CivilTime &t) {
  Wire.beginTransmission(0x68); Wire.write(0x00);
  if (Wire.endTransmission(false)!=0) return false;
  if (Wire.requestFrom((uint8_t)0x68,(uint8_t)7)!=7) return false;
  uint8_t b[7]; for (uint8_t i=0;i<7;i++) b[i]=Wire.read();
  if (b[0]&0x80) return false;                 // CH: oscillator stopped
  auto validBcd=[](uint8_t x){ return ((x>>4)&15)<=9 && (x&15)<=9; };
  if (!validBcd(b[0]&0x7f)||!validBcd(b[1]&0x7f)||!validBcd(b[2]&0x3f)||
      !validBcd(b[4]&0x3f)||!validBcd(b[5]&0x1f)||!validBcd(b[6])) return false;
  auto bcd=[](uint8_t x){ return (x>>4)*10+(x&15); };
  t.second=bcd(b[0]&0x7f); t.minute=bcd(b[1]&0x7f);
  if (b[2]&0x40) return false;                 // mẫu này chỉ nhận 24-hour
  t.hour=bcd(b[2]&0x3f); t.day=bcd(b[4]&0x3f);
  t.month=bcd(b[5]&0x1f); t.year=2000+bcd(b[6]);
  const bool leap=(t.year%4==0 && (t.year%100!=0 || t.year%400==0));
  const uint8_t mdays[12]={31,(uint8_t)(leap?29:28),31,30,31,30,31,31,30,31,30,31};
  return t.second<60 && t.minute<60 && t.hour<24 && t.month>=1 && t.month<=12 &&
         t.day>=1 && t.day<=mdays[t.month-1];
}

int dayOfYear(const CivilTime &t) {
  const uint8_t days[12]={31,28,31,30,31,30,31,31,30,31,30,31};
  const bool leap=(t.year%4==0 && (t.year%100!=0 || t.year%400==0));
  int n=t.day;
  for(int m=1;m<t.month;m++) n+=days[m-1]+((m==2 && leap)?1:0);
  return n;
}
float equationOfTimeMinutes(int n) {
  const float B=radians(360.0f*(n-81)/364.0f);
  return 9.87f*sinf(2*B)-7.53f*cosf(B)-1.5f*sinf(B);
}
float civilToSolarHour(const CivilTime &t) {
  const int n=dayOfYear(t);
  const float civil=t.hour+t.minute/60.0f+t.second/3600.0f;
  const float corr=4.0f*(LON-15.0f*7.0f)+equationOfTimeMinutes(n);
  return civil+corr/60.0f;                   // giờ DS1307 UTC+7 -> giờ Mặt Trời
}
bool solarTarget(float solarHour,int n,SunPosition &out) {
  const float d=radians(23.45f*sinf(radians(360.0f*(284+n)/365.0f)));
  const float H=radians(15.0f*(solarHour-12.0f)), p=radians(PHI);
  const float s=sinf(p)*sinf(d)+cosf(p)*cosf(d)*cosf(H);
  if (s<=0.05f) return false;                 // đêm/thấp: không sinh (0,0)
  out.alphaDeg=degrees(asinf(constrain(s,-1.0f,1.0f)));
  float g=degrees(atan2f(sinf(H),cosf(H)*sinf(p)-tanf(d)*cosf(p)));
  if (g<=-180.0f+0.0001f) g=180.0f;          // không gập mất nhánh 180°
  out.gammaDeg=g;
  return true;                                // giữ cả nhánh gamma=180°
}

// Scheduler minh họa: LCD 1 s độc lập; kiểm tra sáng 1 s; hiệu chỉnh LDR 2 phút.
// Target thiên văn 30 phút. readLdrMatrix() là module thuộc quyển Lập trình 1.
void serviceOnce() {
  const uint32_t now=millis();
  CivilTime t;
  if (!readDs1307(t)) {
    stopAllMotors();
    if (uint32_t(now-lastLCD)>=T_LCD) {
      lastLCD=now; lcd.clear(); lcd.setCursor(0,0); lcd.print("RTC ERROR - HOLD");
    }
    return;                                  // RTC lỗi: không sinh target
  }
  SunPosition sun{};
  const bool sunUp=solarTarget(civilToSolarHour(t),dayOfYear(t),sun);
  const bool estop=(digitalRead(ESTOP)==HIGH);
  if (uint32_t(now-lastLCD)>=T_LCD) {        // độc lập nhánh hiệu chỉnh 2 phút
    lastLCD=now;
    updateLCD(t,estop?"ESTOP":(sunUp?"TRACK":"HOLD"));
  }
  if (uint32_t(now-lastLightPoll)>=T_LIGHT) {
    latestLdr=readLdrMatrix(); lastLightPoll=now; // kiểm tra S mỗi giây
  }
  if (estop || !sunUp || latestLdr.sum<S_MIN) {
    stopAllMotors();                         // dừng/giữ feedback; không target (0,0)
    if (!sunUp) azLatchedToNight=false;      // cho phép xét biên lại ngày kế tiếp
    return;
  }
  if (!astroInitialized || uint32_t(now-lastAstro)>=T_ASTRO) {
    updateAstronomyTarget(sun); lastAstro=now; astroInitialized=true;
  }
  if (uint32_t(now-lastLdrAdjust)>=T_LDR) {
    updateLdrCorrection(latestLdr); lastLdrAdjust=now;
  }
  if (uint32_t(now-lastMotorPoll)>=T_POLL_MS) {
    pollFeedbackLimitsAndMotor(); lastMotorPoll=now;
  }
}
// Mỗi state motor cũng phải gọi motorRunGuard(startMs); GPIO23 NC phần mềm
// không thay cho tiếp điểm phần cứng độc lập cắt enable/nguồn motor.
void setup() {
  pinMode(AZ_THUAN,OUTPUT); pinMode(AZ_NGUOC,OUTPUT);
  pinMode(TILT_LEN,OUTPUT); pinMode(TILT_XUONG,OUTPUT);
  for(uint8_t i=0;i<4;i++) pinMode(LIM[i],INPUT); // GPIO34/35 cần điện trở bias ngoài
  configureSafetyInput(); Wire.begin(21,22);
  lcd.init(); lcd.backlight(); stopAllMotors();
}
void loop() { serviceOnce(); }                // không dùng delay trong vòng giám sát
'''
    blocks = _common_ch1(2, "Lap_trinh") + [
        ("h1", "CHƯƠNG 2. ĐIỀU KHIỂN HAI TRỤC VÀ GIAO DIỆN LDR"),
        ("h2", "2.1. Phân công module"),
        ("p", "Quyển này sở hữu điều khiển motor hai trục, đọc DS1307, LCD, biến trở hồi tiếp, limit và dừng khẩn. Lấy mẫu ADC/hiệu chuẩn LDR/e1/e2 thuộc quyển Lập trình đồ án 1; tại đây chỉ gọi giao diện LdrResult, không lặp code đo sáng."),
        ("h2", "2.2. Thời gian DS1307 và giờ Mặt Trời"),
        ("p", "DS1307 tại 0x68 chứa bảy thanh ghi BCD; kiểm tra ACK, đủ byte, CH, chế độ 24 giờ và miền ngày/giờ trước khi tính. RTC lưu giờ dân dụng Việt Nam. Đổi sang giờ Mặt Trời theo UTC+7, kinh độ tham chiếu lambda≈106,10°E và Equation of Time rồi mới tính H. Kinh độ cần thay bằng tọa độ chính xác khi lắp."),
        ("h2", "2.3. beta, gamma và trạng thái an toàn"),
            ("p", "beta là cao độ pháp tuyến đo từ phương ngang (mặt phẳng pin nghiêng 90°−beta); beta_cmd=clamp(alpha,0°…75°), không dùng 90°−alpha. Tại điểm tham chiếu, trưa 21/6 alpha≈87,5°, lớn hơn hành trình 75° khoảng 12,5°; lệnh bị kẹp ở 75° nên còn sai lệch hình học, chưa chứng minh khớp thật đạt hết hành trình. gamma giữ góc atan2, kể cả ±180°; gamma actuator giới hạn ±120° theo latch. Ban đêm, RTC lỗi hoặc S<S_min: khóa cầu H và giữ góc hồi tiếp, không ra lệnh 0°; khả năng tự giữ cơ khí cần thử riêng."),
        ("h2", "2.4. Chu kỳ, LCD, limit và E-stop"),
        ("p", "Chu kỳ thống nhất: cập nhật target thiên văn 30 phút; kiểm tra tổng sáng 1 giây; hiệu chỉnh e1/e2 theo LDR 2 phút; LCD 1 giây bằng timer độc lập (không đặt trong nhánh LDR). Trong khi motor chạy, kiểm tra hồi tiếp/limit/E-stop mỗi 10 ms; lệnh tối đa 8 giây, nghỉ 25 ms trước đảo chiều. E-stop GPIO23 dùng NC kéo GND: LOW bình thường, HIGH khi nhấn hoặc đứt dây; firmware dừng cả hai cặp, nhưng phải có mạch NC phần cứng cắt enable/nguồn độc lập."),
        ("h1", "CHƯƠNG 3. MÃ THAM KHẢO VÀ KIỂM THỬ"),
        ("h2", "3.1. Trích đoạn tích hợp thời gian và an toàn"),
        ("p", "Đoạn dưới là giao diện tham khảo, chưa nạp lên bo. Hàm đọc LDR không lặp lại; phần đo nằm ở Lập trình đồ án 1. Bộ định thời LCD 1 giây và kiểm tra sáng 1 giây được tách riêng; chỉ nhánh hiệu chỉnh e1/e2 chạy mỗi 2 phút."),
        ("img", "hinh_ve/luu_do_tong_quat_2_truc.png", "{H}. Vòng tích hợp hai trục: target 30 phút, kiểm tra sáng/LCD 1 giây, hiệu chỉnh LDR 2 phút"),
        ("img", "hinh_ve/luu_do_thien_van.png", "{H}. RTC và góc thiên văn; lỗi/đêm không tạo lệnh (0,0)"),
        ("img", "hinh_ve/luu_do_dieu_khien_motor.png", "{H}. Giám sát motor, GPIO23 NC, limit và timeout"),
        ("img", "hinh_ve/luu_do_lcd.png", "{H}. Chu kỳ LCD 1 giây độc lập chu kỳ LDR"),
        ("code", code),
        ("h2", "3.2. Bảng kiểm thử"),
        ("tbl", [["Ca kiểm tra", "Logic phần mềm", "Bằng chứng/trạng thái"],
                 ["Gamma=180°", "Giữ nhánh atan2; không quét vòng.", "Unit test số học qua; chưa thử motor."],
                 ["Đêm/RTC lỗi", "Stop/hold feedback; không zero-target.", "Rà logic; chưa thử bench/hardware."],
                 ["Thiếu sáng S<S_min", "Dừng và giữ vị trí.", "Chưa có dữ liệu LDR thật."],
                 ["E-stop/đứt dây", "NC bình thường LOW; HIGH dừng.", "Chân/sơ đồ đề xuất; chưa xác minh."],
                 ["LCD / light poll / LDR adjust", "1 s / 1 s / 2 phút; timer riêng.", "Rà logic; chưa nạp chạy trên phần cứng."],
                 ["Motor timeout/limit", "8 s, poll 10 ms.", "Chưa thử cơ cấu thật."]],
                "{B}. Ca kiểm tra logic; không đồng nghĩa kiểm thử phần cứng"),
        ("h2", "3.3. Hạn chế"),
        ("b", "Code mẫu chưa là firmware production: cần xử lý debounce limit, lỗi I²C khi chạy, watchdog, kiểm tra ADC và điều khiển công suất."),
        ("b", "GPIO23 chỉ tạo tín hiệu dừng phần mềm; không bảo đảm cắt dòng motor nếu cầu H lỗi. Cần kiểm tra sơ đồ thật và liên động cắt nguồn."),
        ("b", "Chưa thực hiện, dự kiến trước %s: nạp thử, xác nhận RTC/LCD, kiểm tra E-stop, limit, thời gian lệnh và giữ vị trí." % spec.PLAN_DATE),
        ("h1", "CHƯƠNG 4. TIẾN ĐỘ"),
        ("b", "Đã rà logic thời gian và chạy unit test phần mềm; không có xác nhận firmware đã nạp."),
        ("b", "Chưa thực hiện, dự kiến trước %s: hoàn thiện tích hợp, đo trôi RTC, xác minh LCD/light-poll 1 giây và nhánh hiệu chỉnh LDR 2 phút trên bo." % spec.PLAN_DATE),
    ]
    return blocks + _refs("solar_code")


def compose(report: int, volume: str):
    if volume == "Nghien_cuu":
        return _research1() if report == 1 else _research2()
    if volume == "Che_tao":
        return _fabrication(report)
    if volume == "Lap_trinh":
        return _programming1() if report == 1 else _programming2()
    raise ValueError((report, volume))


def _research2():
    controls = _control_rows(2)
    commands = [["Ngày/giờ", "alpha (°)", "beta lệnh (°)", "gamma thô (°)", "gamma lệnh (°)", "Trạng thái"]]
    model = sim.two_axis_command_matrix()
    for day_name in ("21/6", "21/12"):
        for hour in (7, 9, 11, 12, 13, 15, 17):
            r = model[day_name][str(hour)]
            commands.append([f"{day_name} {hour:02d}h", _fmt(r["alpha_deg"], 1),
                             _fmt(r["beta_cmd_deg"], 1), _fmt(r["gamma_raw_deg"], 1),
                             _fmt(r["gamma_cmd_deg"], 1), r["az_state"]])
    gains = sim.energy_gains()
    gain_rows = [["Ngày", "Proxy hai trục giới hạn so với tấm cố định"]]
    for name, _day in spec.DAYS:
        gain_rows.append([name, "+" + _fmt(gains[name]["gain_two_axis_percent"], 1) + "%"])
    return _common_ch1(2, "Nghien_cuu") + [
        ("h1", "CHƯƠNG 2. MÔ HÌNH ĐIỀU HƯỚNG HAI TRỤC"),
        ("h2", "2.1. Góc cơ khí và góc thiên văn"),
        ("p", "Quỹ đạo alpha/gamma và công thức thiên văn dùng chung đã trình bày ở Hình 2 và Chương 2 của quyển Nghiên cứu đồ án 1; không chép lại bảng mùa. Quyển này chỉ tập trung biến đổi sang hai khớp và giới hạn cơ khí [1,2]. beta là cao độ của pháp tuyến tấm pin đo từ phương ngang (mặt phẳng pin nghiêng 90°−beta); góc đặt lý tưởng beta=alpha."),
        ("eq", "beta_cmd=clamp(alpha,0°,75°); gamma_raw giữ nguyên trong (−180°,180°]"),
        ("h2", "2.2. Giới hạn azimuth và giữ vị trí"),
        ("p", "Hành trình azimuth giả thiết ±120°. Không gập gamma qua ±90° và không cho motor quét vòng qua nhánh 180°. Khi target lần đầu ra ngoài dải, chỉ tiếp cận biên gần nếu cách không quá 60°; nếu xa hơn thì giữ vị trí hiện tại, sau đó latch tới đêm. Khi alpha<=0 hoặc thiếu sáng/RTC lỗi, dừng và giữ góc hồi tiếp."),
        ("h2", "2.3. Phạm vi"),
        ("p", "Các kết quả dưới đây là mô phỏng riêng hai trục. Lý thuyết LDR/ADC giữ ở Lập trình đồ án 1; tải/kết cấu ở Chế tạo đồ án 2; code tích hợp ở Lập trình đồ án 2."),
        ("h1", "CHƯƠNG 3. KẾT QUẢ MÔ PHỎNG RIÊNG HAI TRỤC"),
        ("h2", "3.1. Đồ thị thiên văn chung không lặp lại"),
        ("p", "Quỹ đạo alpha/gamma thuần túy giống nhau ở cả hai cấu hình nên chỉ minh họa tại Hình 2 quyển Nghiên cứu đồ án 1. Khác biệt hai trục là beta/gamma actuator sau giới hạn/latch; đầu ra riêng hai trục được minh họa ở Hình 1 ngay dưới đây."),
        ("h2", "3.2. Sai số mô hình hai trục"),
        ("p", "Mô phỏng ngày 21/3, bước 1 phút, mây tổng hợp 10–11h; actuator tức thời, không có mô hình tải. Sai số vector chỉ tính khi alpha≥5° và S≥S_min; số lệnh là số cập nhật trong mô hình. Đây là số liệu mô phỏng riêng hai trục, không phải số liệu một trục hoặc phép đo."),
        ("tbl", controls, "{B}. Sai số/lệnh của ba luật trong mô phỏng hai trục"),
        ("img", "hinh_ve/hoat_dong_hybrid_2_truc.png", "{H}. alpha, beta và gamma thô/lệnh trong mô phỏng hybrid hai trục 21/6"),
        ("h2", "3.3. Proxy trực xạ có giới hạn"),
        ("p", "Tích phân max(0,n_sun·n_panel) với beta là cao độ pháp tuyến, beta<=75° và gamma trong ±120°; so sánh tấm cố định có mặt phẳng nghiêng 21° so với ngang (pháp tuyến cao 69°), hướng Nam. Proxy dùng giới hạn hình học, chưa mô phỏng đầy đủ latch, tốc độ/backlash, mây/khuếch tán/nhiệt/điện motor; không phải kWh hoặc sản lượng điện."),
        ("img", "hinh_ve/so_sanh_nang_luong_2_truc.png", "{H}. Proxy hình học hai trục giới hạn so với pin cố định"),
        ("tbl", gain_rows, "{B}. Proxy hai trục; không phải phép đo điện"),
        ("h2", "3.4. Hạn chế"),
        ("b", "Chưa xét động lực học, độ rơ, tốc độ, dòng motor, gió, che bóng hoặc điều khiển biến trở. LDR/noise/cloud trong mô phỏng là dữ liệu tổng hợp."),
        ("h1", "CHƯƠNG 4. BẢNG LỆNH VÀ KIỂM TRA TÍNH TOÁN"),
        ("h2", "4.1. Bảng lệnh beta/gamma"),
        ("p", "Bảng xuất tự động từ cùng một hàm góc, quét theo phút rồi lấy giờ đại diện; góc thiên văn và góc actuator được tách riêng."),
        ("tbl", commands, "{B}. Góc đặt hai trục và trạng thái latch; dữ liệu mô phỏng"),
        ("h2", "4.2. Nhánh 180°"),
        ("p", "Ngày 21/6 gần trưa gamma thô xấp xỉ 180°. Bảng giữ nguyên gamma thô; actuator không chạy vòng qua 180° mà chỉ giữ/tiếp cận biên theo quy tắc. beta là cao độ pháp tuyến từ phương ngang, beta_cmd kẹp 0–75°; mặt phẳng pin nghiêng 90°−beta, không dùng beta=90°−alpha."),
        ("h2", "4.3. Trạng thái công việc"),
        ("b", "Đã chạy mô phỏng hai trục và tái xuất đồ thị/bảng từ cùng hàm tính; chưa đo trên cơ cấu."),
        ("b", "Chưa thực hiện, dự kiến trước %s: xác minh góc bằng encoder/thước, đo dòng và kiểm thử hai trục ngoài trời." % spec.PLAN_DATE),
    ] + _refs("solar")
