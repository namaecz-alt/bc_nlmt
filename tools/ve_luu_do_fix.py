# -*- coding: utf-8 -*-
"""Ve lai 6 luu do theo ghi chu: chi noi chuc nang khoi, co nut Ket thuc,
khoi khoi tao thu vien o luu do tong quat, sua dung luu do ADC va cau H."""
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Polygon

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hinh_ve")
EDGE = "#1f3864"
TXT = "#1f3864"
FILL_PROC = "#dce6f1"
FILL_DEC = "#fff2cc"
FILL_IO = "#e2efda"
FILL_TERM = "#d9ead3"


def box(ax, x, y, w, h, text, kind="proc"):
    fc = {"proc": FILL_PROC, "dec": FILL_DEC, "io": FILL_IO, "term": FILL_TERM}[kind]
    if kind == "term":
        ax.add_patch(Ellipse((x, y), w, h, fc=fc, ec=EDGE, lw=1.2))
    elif kind == "dec":
        ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)],
                             closed=True, fc=fc, ec=EDGE, lw=1.2))
    else:
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.02,rounding_size=0.3",
                                    fc=fc, ec=EDGE, lw=1.2))
    ax.text(x, y, text, ha="center", va="center", fontsize=8.2, color=TXT)


def arrow(ax, x1, y1, x2, y2, label=None, lx=0.0, ly=0.0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=1.1))
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, fontsize=7.6, color=TXT,
                ha="center", va="center")


def canvas(w, h, n):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, n)
    ax.set_aspect("auto")
    ax.text(50, n - 1.2, "", ha="center")
    return fig, ax


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print("da ve:", name)


def luu_do_thien_van():
    fig, ax = canvas(7.2, 8.6, 100)
    ys = [95, 84, 71, 58, 45, 32, 19, 7]
    box(ax, 50, ys[0], 26, 7, "BẮT ĐẦU", "term")
    box(ax, 50, ys[1], 62, 10, "Đọc ngày và giờ thực tế từ module DS1307")
    box(ax, 50, ys[2], 62, 12, "Tính góc lệch δ, góc giờ H, góc cao α\nvà phương vị γ theo công thức thiên văn")
    box(ax, 50, ys[3], 62, 12, "Chuẩn hóa bước nhảy 180° của γ\nvào trưa ngày hạ chí")
    box(ax, 50, ys[4], 62, 10, "Đổi (α, γ) ra góc đặt thô của khung pin")
    box(ax, 50, ys[5], 62, 10, "Chuyển góc đặt thô cho khối tinh chỉnh LDR")
    box(ax, 50, ys[6], 62, 8, "Ghi nhãn thời gian cho nhật ký số liệu")
    box(ax, 50, ys[7], 26, 7, "KẾT THÚC CHU KỲ", "term")
    for a, b in zip(ys[:-1], ys[1:]):
        arrow(ax, 50, a - (3.5 if a == ys[0] else 5), 50, b + 5.5)
    ax.text(86, 52, "Chu kỳ 30 phút", fontsize=7.8, color=TXT)
    save(fig, "luu_do_thien_van.png")


def luu_do_doc_adc():
    fig, ax = canvas(7.2, 9.2, 100)
    ys = [95, 85, 73, 61, 49, 36, 23, 10]
    box(ax, 50, ys[0], 26, 6, "BẮT ĐẦU", "term")
    box(ax, 50, ys[1], 64, 9, "Đọc bốn kênh quang trở ở GPIO25, 26, 27, 14")
    box(ax, 50, ys[2], 64, 9, "Lọc trung bình 16 mẫu cho mỗi kênh")
    box(ax, 50, ys[3], 64, 9, "Nhân hệ số hiệu chuẩn K_cal để bốn kênh bằng nhau")
    box(ax, 50, ys[4], 64, 10, "Tính sai lệch e1 = trái − phải\nvà e2 = trên − dưới")
    box(ax, 50, ys[5], 64, 10, "So sánh |e| với ngưỡng phát lệnh\nvà vùng chết")
    box(ax, 50, ys[6], 64, 8, "Chuyển sai lệch và tổng sáng S cho khối điều khiển")
    box(ax, 50, ys[7], 26, 6, "KẾT THÚC LẦN ĐỌC", "term")
    steps = [3, 4.5, 4.5, 4.5, 5, 5, 4.5, 3]
    for a, b, da, db in zip(ys[:-1], ys[1:], steps[:-1], steps[1:]):
        arrow(ax, 50, a - da, 50, b + db)
    ax.text(86, 55, "Chu kỳ 2 phút", fontsize=7.8, color=TXT)
    save(fig, "luu_do_doc_adc.png")


def luu_do_dieu_khien_motor():
    fig, ax = canvas(7.6, 9.4, 100)
    box(ax, 50, 95, 26, 6, "BẮT ĐẦU", "term")
    box(ax, 50, 85, 62, 9, "Nhận chiều cần chỉnh từ khối sai lệch LDR")
    box(ax, 50, 73, 62, 9, "Đọc biến trở hồi tiếp để biết góc hiện tại")
    box(ax, 50, 60, 56, 11, "Góc đã sát giới hạn hành trình\ntheo chiều cần chạy?", "dec")
    box(ax, 85, 60, 26, 10, "Cấm chiều đó,\ngiữ nguyên vị trí", "proc")
    box(ax, 50, 45, 62, 10, "Đặt mức lệnh cầu H theo chiều quay\n(tích cực thấp, cách ly qua opto)")
    box(ax, 50, 32, 62, 10, "Chạy motor đến khi |e| vào vùng chết\nhoặc hết thời gian cho phép")
    box(ax, 50, 19, 62, 9, "Trả cả hai lệnh về mức khóa để cầu H tự giữ")
    box(ax, 50, 7, 26, 6, "KẾT THÚC LỆNH", "term")
    arrow(ax, 50, 92, 50, 89.5)
    arrow(ax, 50, 80.5, 50, 77.5)
    arrow(ax, 50, 68.5, 50, 65.5)
    arrow(ax, 78, 60, 72, 60, "có", 0, 2.2)
    arrow(ax, 50, 54.5, 50, 50, "không", 7, 0)
    arrow(ax, 50, 40, 50, 37)
    arrow(ax, 50, 27, 50, 23.5)
    arrow(ax, 50, 14.5, 50, 10)
    save(fig, "luu_do_dieu_khien_motor.png")


def luu_do_lcd():
    fig, ax = canvas(7.2, 7.6, 100)
    ys = [94, 83, 70, 57, 44, 31, 18, 7]
    box(ax, 50, ys[0], 26, 7, "BẮT ĐẦU", "term")
    box(ax, 50, ys[1], 62, 10, "Khởi tạo thư viện LCD I2C ở địa chỉ 0x27")
    box(ax, 50, ys[2], 62, 10, "Đọc giờ từ DS1307 và góc từ biến trở hồi tiếp")
    box(ax, 50, ys[3], 62, 10, "Lập chuỗi hai dòng tiếng Việt không dấu")
    box(ax, 50, ys[4], 62, 10, "Gửi chuỗi lên màn hình qua bus I2C")
    box(ax, 50, ys[5], 62, 8, "Giữ nguyên màn hình đến lần cập nhật sau")
    box(ax, 50, ys[6], 26, 7, "KẾT THÚC LẦN HIỂN THỊ", "term")
    for a, b in zip(ys[:-2], ys[1:-1]):
        arrow(ax, 50, a - 5, 50, b + 5)
    arrow(ax, 50, ys[5] - 4, 50, ys[6] + 3.5)
    ax.text(85, 62, "Mỗi 1 giây", fontsize=7.8, color=TXT)
    save(fig, "luu_do_lcd.png")


def luu_do_bien_tro():
    fig, ax = canvas(7.2, 8.4, 100)
    ys = [95, 85, 73, 61, 48, 35, 22, 9]
    box(ax, 50, ys[0], 26, 6, "BẮT ĐẦU", "term")
    box(ax, 50, ys[1], 62, 9, "Đọc điện áp wiper của biến trở hồi tiếp góc")
    box(ax, 50, ys[2], 62, 9, "Lọc trung bình 8 mẫu")
    box(ax, 50, ys[3], 62, 10, "Nội suy ba điểm hiệu chuẩn\nV_min, V_mid, V_max")
    box(ax, 50, ys[4], 62, 9, "Suy ra góc hiện tại của khung pin")
    box(ax, 50, ys[5], 62, 10, "So sánh góc với giới hạn hành trình hai đầu")
    box(ax, 50, ys[6], 62, 8, "Chuyển góc và cờ giới hạn cho khối bảo vệ")
    box(ax, 50, ys[7], 26, 6, "KẾT THÚC LẦN ĐỌC", "term")
    for a, b in zip(ys[:-1], ys[1:]):
        arrow(ax, 50, a - 4.5, 50, b + 4.5)
    save(fig, "luu_do_bien_tro.png")


def luu_do_tong_quat(mot_truc=True):
    fig, ax = canvas(8.6, 11.0, 100)
    box(ax, 46, 96, 24, 5, "BẮT ĐẦU", "term")
    box(ax, 46, 88, 58, 8, "Khởi tạo thư viện và chân: Wire, LCD I2C, DS1307,\nkênh ADC quang trở và hai lệnh cầu H")
    box(ax, 46, 78, 52, 8, "Đến chu kỳ thiên văn 30 phút?", "dec")
    box(ax, 82, 78, 26, 8, "Tính (α, γ) và đặt\ngóc thô cho khung")
    box(ax, 46, 66, 52, 8, "Đến chu kỳ tinh chỉnh LDR 2 phút?", "dec")
    box(ax, 82, 66, 26, 10, "Đọc bốn kênh, tính sai lệch;\nvượt ngưỡng thì chạy motor,\nvào vùng chết thì dừng")
    box(ax, 46, 53, 52, 8, "Tổng sáng S nhỏ hơn ngưỡng mây mù?", "dec")
    box(ax, 82, 53, 26, 8, "Giữ vị trí theo lịch\nthiên văn, không tinh chỉnh")
    if not mot_truc:
        box(ax, 46, 41, 52, 8, "Thứ tự tinh chỉnh: khớp nghiêng trước,\nkhớp phương vị sau?", "dec")
        box(ax, 82, 41, 26, 8, "Chỉnh e2 rồi mới chỉnh e1")
        y_next = 30
    else:
        y_next = 41
    box(ax, 46, y_next, 58, 8, "Đọc biến trở giám sát hành trình, cập nhật\nhai dòng LCD mỗi giây")
    box(ax, 46, y_next - 10, 58, 7, "Gió lớn hoặc tắt máy: đưa tấm pin về vị trí nghỉ")
    box(ax, 46, y_next - 19, 24, 5, "KẾT THÚC", "term")
    arrow(ax, 46, 93.5, 46, 92)
    arrow(ax, 46, 84, 46, 82)
    arrow(ax, 46, 74, 46, 70, "không", 6, 0)
    arrow(ax, 72, 78, 69, 78, "có", 0, 1.8)
    arrow(ax, 82, 74, 82, 72)
    ax.annotate("", xy=(97, 88), xytext=(97, 72), arrowprops=dict(arrowstyle="-", color=EDGE, lw=0.9))
    ax.annotate("", xy=(75, 88), xytext=(97, 88), arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=0.9))
    arrow(ax, 46, 62, 46, 57, "không", 6, 0)
    arrow(ax, 72, 66, 69, 66, "có", 0, 1.8)
    arrow(ax, 82, 61, 82, 59)
    arrow(ax, 46, 49, 46, 45 if not mot_truc else 45, "không", 6, 0)
    arrow(ax, 72, 53, 69, 53, "có", 0, 1.8)
    arrow(ax, 82, 49, 82, 47)
    if not mot_truc:
        arrow(ax, 46, 37, 46, 34, "không", 6, 0)
        arrow(ax, 72, 41, 69, 41, "có", 0, 1.8)
    arrow(ax, 46, y_next - 4, 46, y_next - 6.5)
    arrow(ax, 46, y_next - 13.5, 46, y_next - 16.5)
    ax.annotate("", xy=(3, 88), xytext=(3, y_next - 4), arrowprops=dict(arrowstyle="-", color=EDGE, lw=0.9))
    ax.annotate("", xy=(17, y_next - 4), xytext=(3, y_next - 4), arrowprops=dict(arrowstyle="-", color=EDGE, lw=0.9))
    ax.annotate("", xy=(3, 88), xytext=(17, 88), arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=0.9))
    ax.text(8, 60, "Lặp lại", fontsize=7.8, color=TXT, rotation=90)
    save(fig, "luu_do_tong_quat_%s.png" % ("1_truc" if mot_truc else "2_truc"))


if __name__ == "__main__":
    luu_do_thien_van()
    luu_do_doc_adc()
    luu_do_dieu_khien_motor()
    luu_do_lcd()
    luu_do_bien_tro()
    luu_do_tong_quat(True)
    luu_do_tong_quat(False)
