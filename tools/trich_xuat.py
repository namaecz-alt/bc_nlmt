# -*- coding: utf-8 -*-
"""Trich xuat va ghep noi dung 6 quyen bao cao.

Cau truc moi (tuan 5/10 - 10/10/2026):
- Quyen Nghien cuu  = Chuong 1 + Chuong 2 cua bao cao goc (giu NGUYEN VAN,
  nhung muc 2.4/2.5 duoc THAY bang ESP32 + dong co gat mua; cac cau noi ve
  bo dem buoc theo thoi gian duoc va lai theo phuong phap ma tran suy goc)
  + Chuong 3 ket qua mo phong + Chuong 4 tien do + Tai lieu tham khao.
- Quyen Che tao  = 4 chuong moi hoan toan (phuong an chot, co khi - mach -
  vat tư, lap rap - hieu chuan - an toan, tien do) + Tai lieu tham khao.
- Quyen Lap trinh = 4 chuong moi hoan toan (Arduino IDE va cach nap ESP32,
  nhom lenh, phuong phap ma tran + code mau, tien do) + Tai lieu tham khao.
Khong con noi dung quay theo buoc thoi gian; mach khong con bo Arduino.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import noi_dung_moi_1_truc as moi1
import noi_dung_moi_2_truc as moi2

try:
    from docx import Document
except ImportError:
    Document = None

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_1 = os.path.join(BASE, "Bao_cao_do_an_mau_bam_nang_1_truc.docx")
FILE_2 = os.path.join(BASE, "bao_cao_mau_do_an_dieu_khien_bam_mat_troi.docx")


def _clean(s):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s.replace("\u2013", "-").replace("\u2014", "-")


def load_blocks(path):
    """Doc docx -> danh sach khoi (loai, noi dung) theo thu tu ban goc."""
    doc = Document(path)
    styles, blocks = {}, []
    for p in doc.paragraphs:
        t = _clean(p.text)
        if not t:
            continue
        style = (p.style.name or "").lower()
        if style.startswith("heading 1"):
            blocks.append(("h1", t))
        elif style.startswith("heading 2"):
            blocks.append(("h2", t))
        elif style.startswith("heading 3"):
            blocks.append(("h3", t))
        elif "list" in style:
            blocks.append(("b", t))
        elif t.startswith("S =") or t.startswith("e_") or t.startswith("R_") or \
                t.startswith("f(") or (len(t) < 60 and "=" in t and t[0].isupper()):
            blocks.append(("eq", t))
        else:
            blocks.append(("p", t))
    for tbl in doc.tables:
        rows = [[_clean(c.text) for c in r.cells] for r in tbl.rows]
        blocks.append(("tbl", rows, None))
    return blocks


def cut(blocks, start, end=None):
    """Lay doan tu heading bat dau bang `start` den truoc `end`."""
    i = next(k for k, b in enumerate(blocks) if b[0] in ("h1", "h2", "h3") and b[1].startswith(start))
    if end is None:
        return blocks[i:]
    j = next(k for k, b in enumerate(blocks) if k > i and b[0] in ("h1", "h2", "h3") and b[1].startswith(end))
    return blocks[i:j]


def replace_section(blocks, start_h2, end_h2, new_blocks):
    """Thay toan bo muc h2 `start_h2` (den truoc `end_h2`) bang new_blocks."""
    i = next(k for k, b in enumerate(blocks) if b[0] == "h2" and b[1].startswith(start_h2))
    j = next(k for k, b in enumerate(blocks) if b[0] == "h2" and b[1].startswith(end_h2))
    return blocks[:i] + list(new_blocks) + blocks[j:]


def patch(blocks, pairs):
    """Thay the chuoi trong doan van, gach dau dong va o bang (van dung nguyen van)."""
    out = []
    for b in blocks:
        if b[0] in ("p", "b", "eq"):
            t = b[1]
            for old, new in pairs:
                t = t.replace(old, new)
            out.append((b[0], t))
        elif b[0] == "tbl":
            rows = [[next((n for o, n in pairs if o == c), c) for c in r] for r in b[1]]
            out.append(("tbl", rows, b[2]))
        else:
            out.append(b)
    return out


PATCHES_1 = [
    # Chuong 1: cau hinh chot theo phan cung moi
    ("cấu hình tham khảo gồm ESP32, BH1750 làm kênh tham chiếu, đồng hồ thời gian thực và một cơ cấu chấp hành có giới hạn hành trình",
     "cấu hình tham khảo gồm ESP32, mạch chia áp đo điện áp tấm pin, module thời gian thực DS1307 và một động cơ gạt nước trục vít có giới hạn hành trình"),
    ("Thiết kế cụm bốn LDR, ESP32, cơ cấu chấp hành một trục, bảo vệ hành trình, đo công suất tấm pin, RTC và lưu dữ liệu.",
     "Thiết kế cụm bốn LDR, ESP32, động cơ gạt nước trục vít một trục, biến trở hồi tiếp góc, bảo vệ hành trình, đo công suất tấm pin, RTC và lưu dữ liệu."),
    # Chuong 2: bo dem buoc theo thoi gian -> ma tran suy goc; RTC chi de ghi nhan
    ("Đặt lịch thiên văn làm gốc, LDR xác nhận điều kiện nắng và hiệu chỉnh lệch còn lại.",
     "Ma trận LDR suy ra góc lệch làm gốc; RTC dùng ghi nhãn thời gian và log dữ liệu."),
    ("Phương án đề xuất cho một trục là thuật toán bám LDR có vùng chết, giới hạn hành trình và chế độ giữ vị trí khi tín hiệu kém.",
     "Phương án chốt cho một trục là đọc ma trận 4 LDR, suy ra góc cần quay, có vùng chết 3° và chế độ giữ vị trí khi tín hiệu kém."),
    ("với mô hình một trục, phương án lai thiên văn-LDR có vùng chết và chế độ giữ vị trí khi tín hiệu kém là lựa chọn đề xuất",
     "với mô hình một trục, phương pháp ma trận 4 LDR suy ra góc cần quay, có vùng chết 3° và chế độ giữ vị trí khi tín hiệu kém, là lựa chọn chốt"),
    ("ESP32 + RTC DS3231.", "ESP32 + RTC DS1307."),
    ("https://www.analog.com/media/en/technical-documentation/data-sheets/DS3231.pdf",
     "https://www.analog.com/media/en/technical-documentation/data-sheets/DS1307.pdf"),
    ("Analog Devices, DS3231 Extremely Accurate I²C-Integrated RTC/TCXO/Crystal, Datasheet.",
     "Maxim Integrated, DS1307 64 x 8, Serial I2C Real-Time Clock, Datasheet."),
    # Bang khoi chuong 1 va tai lieu tham khao: bo BH1750/Mega khoi cau hinh
    ("4 LDR tại 4 góc, gá nghiêng hướng ra ngoài; BH1750 tham chiếu.",
     "4 LDR tại 4 góc, gá nghiêng β_s = 30° hướng ra ngoài; vách che chữ thập giữa cụm."),
    ("Cơ cấu chấp hành phù hợp tải + công tắc hành trình.",
     "Động cơ gạt nước trục vít phù hợp tải + công tắc hành trình."),
    ("Đo U, I pin và điện năng actuator.",
     "Đo điện áp tấm pin và trạng thái động cơ gạt nước."),
    ("[9] Arduino, Arduino Mega 2560 Rev3 - Technical Specifications. https://docs.arduino.cc/hardware/mega-2560/",
     "[9] Espressif Systems, ESP32-DevKitC General Purpose Development Board User Guide. https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/index.html"),
    ("[10] ROHM Semiconductor, BH1750FVI Digital 16-bit Serial Output Type Ambient Light Sensor IC, Datasheet.",
     "[10] NXP Semiconductors, PCF8574 Remote 8-bit I/O Expander for I2C-bus (mạch kèm LCD 1602), Datasheet."),
]

PATCHES_2 = [
    ("Arduino Mega tính sai lệch quang, đặt góc cho servo phương vị và điều khiển động cơ giảm tốc có encoder để chỉnh độ nghiêng; công tắc hành trình giới hạn chuyển động.",
     "ESP32 tính sai lệch quang theo ma trận bốn LDR, suy ra góc đích cho hai động cơ gạt nước trục vít ở cả phương vị và độ nghiêng, hồi tiếp góc bằng biến trở xoay; công tắc hành trình giới hạn chuyển động."),
    ("Thuật toán đề xuất không cần tính góc đặt thiên văn trong vòng điều khiển chính: bộ điều khiển so sánh các cặp LDR, dịch chuyển từng bước về phía có điện trở nhỏ hơn, dừng khi sai lệch nằm trong ngưỡng và định kỳ đọc lại để hiệu chỉnh.",
     "Thuật toán của đề tài không cần tính góc đặt thiên văn trong vòng điều khiển chính: bộ điều khiển đọc ma trận bốn LDR, suy ra góc cần quay bằng quan hệ lượng giác, quay trực tiếp tới góc đích theo hồi tiếp biến trở và định kỳ đọc lại để hiệu chỉnh."),
    ("Đề xuất cụm bốn LDR, Arduino Mega, servo vị trí cho phương vị, động cơ DC giảm tốc có encoder cho độ nghiêng, RTC và công tắc hành trình.",
     "Đề xuất cụm bốn LDR, ESP32, hai động cơ gạt nước trục vít cho phương vị và độ nghiêng, hai biến trở hồi tiếp góc, RTC và công tắc hành trình."),
    ("Xây dựng quy tắc so sánh hai cặp LDR chéo, xác định phía có điện trở nhỏ hơn, điều khiển cơ cấu theo bước và đọc lại sau thời gian đặt trước.",
     "Xây dựng quy tắc ma trận bốn LDR, xác định phía nhận sáng mạnh hơn, suy ra góc cần quay cho từng trục và đọc lại sau mỗi chu kỳ."),
    ("Cấu hình đề xuất dùng Arduino Mega, bốn LDR, một servo vị trí cho phương vị, một động cơ DC giảm tốc có encoder cho độ nghiêng, driver cầu H, RTC và công tắc hành trình cho hai trục; photodiode được xem xét ở mức so sánh.",
     "Cấu hình đề xuất dùng ESP32, bốn LDR, hai động cơ gạt nước trục vít (phương vị và độ nghiêng) đóng cắt qua relay/cầu H, hai biến trở hồi tiếp góc, RTC và công tắc hành trình cho hai trục; photodiode được xem xét ở mức so sánh."),
    ("Phạm vi tập trung vào đo điện trở LDR, so sánh hai hướng nghiêng/quay, điều khiển hai cơ cấu chấp hành theo bước, đặt thời gian đọc lại và bảo vệ hành trình.",
     "Phạm vi tập trung vào đọc ma trận điện trở LDR, suy ra góc lệch hai hướng nghiêng/quay, điều khiển hai cơ cấu chấp hành quay tới góc đích và bảo vệ hành trình."),
    ("Thuật toán so sánh điện trở 4 LDR, điều khiển servo phương vị và động cơ nghiêng từng bước, dừng khi gần cân bằng và tự đọc lại theo chu kỳ.",
     "Thuật toán ma trận điện trở 4 LDR suy ra góc đích, điều khiển motor phương vị và motor nghiêng quay tới góc đích, dừng khi vào vùng chết và tự đọc lại theo chu kỳ."),
    ("Chương trình điều khiển Arduino cùng quy trình kiểm thử từng cảm biến, servo và công tắc hành trình.",
     "Chương trình điều khiển ESP32 cùng quy trình kiểm thử từng cảm biến, hai động cơ gạt nước và công tắc hành trình."),
    ("Đặt lịch thiên văn làm góc cơ sở, dùng LDR để hiệu chỉnh phần sai lệch còn lại.",
     "Ma trận LDR suy ra góc lệch làm gốc; RTC dùng ghi nhãn thời gian và log dữ liệu."),
    ("Với mô hình hai trục này, đề xuất so sánh điện trở tổng hợp của hai phía đối diện; trục nào chênh lệch vượt ngưỡng thì dịch chuyển từng bước về phía có điện trở nhỏ hơn. Khi cả hai trục gần cân bằng, dừng cơ cấu, chờ T_đọc rồi lấy mẫu mới.",
     "Với mô hình hai trục này, chốt phương pháp đọc ma trận điện trở bốn kênh; mỗi trục suy ra góc lệch từ chênh lệch chuẩn hóa hai phía đối diện theo công thức Δ = atan(e/tan β_s) và quay trực tiếp tới góc đích theo hồi tiếp biến trở. Khi cả hai trục vào vùng chết 3°, dừng cơ cấu, chờ hết chu kỳ đọc rồi lấy mẫu mới."),
    ("Với servo vị trí, tín hiệu đặt được giới hạn theo hành trình; bộ điều khiển không nên gửi lệnh liên tục gây rung khi sai số nhỏ.",
     "Với motor trục vít, lệnh quay được giới hạn theo hành trình và chỉ phát khi góc lệch vượt vùng chết; nhờ trục vít tự hãm nên không cần nuôi điện để giữ vị trí."),
    ("Đề tài được lựa chọn nhằm xây dựng thuật toán bám nắng hai trục dùng bốn LDR, servo phương vị và động cơ điều chỉnh độ nghiêng; tập trung vào cách so sánh điện trở, xác định chiều chuyển động, giới hạn hành trình và chu kỳ đọc lại cảm biến.",
     "Đề tài được lựa chọn nhằm xây dựng thuật toán bám nắng hai trục dùng bốn LDR và hai động cơ gạt nước trục vít cho phương vị, độ nghiêng; tập trung vào cách lập ma trận điện trở, suy ra góc cần quay, giới hạn hành trình và chu kỳ đọc lại cảm biến."),
    ("Điều khiển từng bước và đọc lại sau một khoảng thời gian giúp cơ cấu căn chỉnh mà không phải quay liên tục.",
     "Điều khiển suy ra góc cần quay rồi đọc lại sau mỗi chu kỳ giúp cơ cấu căn chỉnh mà không phải quay liên tục."),
    ("Tín hiệu đưa về Arduino để dừng PWM/servo theo hướng nguy hiểm, có chống dội; nơi cần bảo vệ cao hơn có thể đưa tiếp điểm vào đường liên động driver.",
     "Tín hiệu đưa về ESP32 để dừng lệnh quay motor theo hướng nguy hiểm, có chống dội; nơi cần bảo vệ cao hơn có thể đưa tiếp điểm vào đường liên động của relay/cầu H."),
    ("Góc servo thực tế bằng góc tính toán cộng offset lắp đặt, sau đó được giới hạn theo hành trình.",
     "Góc đặt thực tế bằng góc tính toán cộng offset lắp đặt, sau đó được giới hạn theo hành trình."),
    ("còn giới hạn cơ khí, vị trí home, sai số gá lắp và hành trình servo quyết định góc lệnh thực tế.",
     "còn giới hạn cơ khí, vị trí home, sai số gá lắp và hành trình motor quyết định góc lệnh thực tế."),
    ("năng lượng tiêu thụ của servo, động cơ nghiêng, Arduino và mạch phụ trợ phải được ghi riêng rồi trừ khi tính năng lượng thuần.",
     "năng lượng tiêu thụ của hai động cơ gạt nước, ESP32 và mạch phụ trợ phải được ghi riêng rồi trừ khi tính năng lượng thuần."),
    ("Năng lượng PV và năng lượng servo/bộ điều khiển cần đo trên cùng khoảng thời gian",
     "Năng lượng PV và năng lượng động cơ/bộ điều khiển cần đo trên cùng khoảng thời gian"),
    ("Việc lựa chọn ngưỡng cân bằng và bước dịch chuyển cần cân bằng giữa độ nhạy, rung cơ cấu, thời gian đáp ứng và độ bền.",
     "Việc lựa chọn vùng chết và ngưỡng phát lệnh cần cân bằng giữa độ nhạy, rung cơ cấu, thời gian đáp ứng và độ bền."),
    # Bang khoi chuong 1
    ("Arduino Mega + RTC DS3231.", "ESP32 + RTC DS1307."),
    ("Servo vị trí + nguồn riêng.", "Motor gạt nước trục vít + nguồn 12 V riêng."),
    ("Quay tấm pin trái/phải theo góc đặt.", "Quay tấm pin trái/phải tới góc đích theo hồi tiếp biến trở."),
    ("Motor DC giảm tốc + encoder + cầu H.", "Motor gạt nước trục vít + relay/cầu H."),
    ("Đo U/I PV và điện năng hai cơ cấu.", "Đo điện áp tấm pin và trạng thái hai động cơ gạt nước."),
    # Tai lieu tham khao: DS3231 -> DS1307 dung theo mach thuc te
    ("https://www.analog.com/media/en/technical-documentation/data-sheets/DS3231.pdf",
     "https://www.analog.com/media/en/technical-documentation/data-sheets/DS1307.pdf"),
    ("Analog Devices, DS3231 Extremely Accurate I²C-Integrated RTC/TCXO/Crystal, Datasheet.",
     "Maxim Integrated, DS1307 64 x 8, Serial I2C Real-Time Clock, Datasheet."),
    # Tai lieu tham khao: [8] tro thanh datasheet ESP32 (duoc trich dan trong muc 2.4 moi)
    ("[8] Arduino, Arduino Mega 2560 Rev3 - Technical Specifications. https://docs.arduino.cc/hardware/mega-2560/",
     "[8] Espressif Systems, ESP32 Series Datasheet. https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf"),
]


class Numberer(object):
    """Danh so Hinh/Bang rieng cho tung quyen bao cao."""

    def __init__(self):
        self.h = 0
        self.b = 0

    def cap(self, text):
        if "{H}" in text:
            self.h += 1
            return text.replace("{H}", "Hình %d" % self.h)
        if "{B}" in text:
            self.b += 1
            return text.replace("{B}", "Bảng %d" % self.b)
        return text

    def run(self, blocks):
        out = []
        for blk in blocks:
            if blk[0] == "img":
                out.append(("img", blk[1], self.cap(blk[2]) if blk[2] else None))
            elif blk[0] == "tbl":
                out.append(("tbl", blk[1], self.cap(blk[2]) if blk[2] else None))
            else:
                out.append(blk)
        return out


def compose(report):
    """Tra ve (nghien_cuu, che_tao, lap_trinh) - moi phan la danh sach khoi."""
    moi = moi1 if report == 1 else moi2
    fname = FILE_1 if report == 1 else FILE_2
    base = load_blocks(fname)
    ch1 = cut(base, "CHƯƠNG 1", "CHƯƠNG 2")
    ch2 = cut(base, "CHƯƠNG 2", "CHƯƠNG 3")
    refs = cut(base, "TÀI LIỆU THAM KHẢO")
    ch2 = replace_section(ch2, "2.4.", "2.6.", moi.NEW_24_25)
    ch2 = replace_section(ch2, "2.9.", "2.10.", moi.NEW_29)
    pairs = PATCHES_1 if report == 1 else PATCHES_2
    ch2 = patch(ch2, pairs)
    ch1 = patch(ch1, pairs)
    refs = patch(refs, pairs)

    nc = ch1 + ch2 + [("h1", moi.NGHIEN_CUU_H1_CH3)] + moi.NGHIEN_CUU_CH3 \
        + [("h1", moi.NGHIEN_CUU_H1_CH4)] + moi.NGHIEN_CUU_CH4 + refs

    ct = [("h1", moi.CHE_TAO_H1_CH1)] + moi.CHE_TAO_CH1 \
        + [("h1", moi.CHE_TAO_H1_CH2)] + moi.CHE_TAO_CH2 \
        + [("h1", moi.CHE_TAO_H1_CH3)] + moi.CHE_TAO_CH3 \
        + [("h1", moi.CHE_TAO_H1_CH4)] + moi.CHE_TAO_CH4 + refs

    lt = ch1 + moi.LAP_TRINH_CH1_THEM \
        + [("h1", moi.LAP_TRINH_H1_CH2)] + moi.LAP_TRINH_CH2 \
        + [("h1", moi.LAP_TRINH_H1_CH3)] + moi.LAP_TRINH_CH3 + moi.LAP_TRINH_CH3_CODE \
        + [("h1", moi.LAP_TRINH_H1_CH4)] + moi.LAP_TRINH_CH4 + refs

    num = Numberer
    return num().run(nc), num().run(ct), num().run(lt)


DE_TAI = {
    1: "NGHIÊN CỨU THUẬT TOÁN ĐO CƯỜNG ĐỘ ÁNH SÁNG ĐỂ XÁC ĐỊNH HƯỚNG "
       "ĐIỀU KHIỂN TẤM PIN ỨNG DỤNG TRONG HỆ THỐNG PIN NĂNG LƯỢNG MẶT TRỜI",
    2: "NGHIÊN CỨU THUẬT TOÁN ĐIỀU KHIỂN ĐIỀU HƯỚNG TẤM PIN ỨNG DỤNG "
       "TRONG HỆ THỐNG PIN NĂNG LƯỢNG MẶT TRỜI",
}
TEN_QUYEN = {"Nghien_cuu": "QUYỂN 1 – NGHIÊN CỨU PHƯƠNG PHÁP",
             "Che_tao": "QUYỂN 2 – CHẾ TẠO MẠCH VÀ CƠ KHÍ",
             "Lap_trinh": "QUYỂN 3 – LẬP TRÌNH VÀ HIỆU CHUẨN"}


def all_specs():
    """(spec, report) x 6, dung chung cho build_bao_cao.py va xuat_pdf.py."""
    out = []
    for r in (1, 2):
        for idx, (name, blocks) in enumerate(
                zip(("Nghien_cuu", "Che_tao", "Lap_trinh"), compose(r))):
            out.append((
                {"out": os.path.join(BASE, "Bao_cao_%d_truc_%s.docx" % (r, name)),
                 "pdf": os.path.join(BASE, "Bao_cao_pdf_%d_truc_%s.pdf" % (r, name)),
                 "title": "ĐỒ ÁN %d (mô hình %s trục)" % (r, r),
                 "de_tai": DE_TAI[r],
                 "quyen": TEN_QUYEN[name],
                 "subtitle": "Quyển %d/3 – tuần báo cáo 5/10 – 10/10/2026" % (idx + 1),
                 "blocks": blocks}, r))
    return out


if __name__ == "__main__":
    for spec, rep in all_specs():
        h1 = [b[1] for b in spec["blocks"] if b[0] == "h1"]
        ncode = sum(1 for b in spec["blocks"] if b[0] == "code")
        print("[%s] %s" % (os.path.basename(spec["out"]), spec["subtitle"]))
        for h in h1:
            print("   ", h[:100])
        print("    khoi:", len(spec["blocks"]), "| code:", ncode)
