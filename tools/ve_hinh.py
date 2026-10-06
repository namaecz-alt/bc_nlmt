# -*- coding: utf-8 -*-
"""Ve so do / hinh minh hoa phong cach ban ve ky thuat don gian (nen trang,
net den manh, it mau) de giong ban ve EasyEDA / ban ve tay, kem bo 7 so do
mach ve lai thiet ke EasyEDA cua de tai.

Chay:  python3 tools/ve_hinh.py
"""
import math
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, Circle

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hinh_ve")
MACH = os.path.join(OUT, "mach")

INK = "#101010"
NET = "#1a56b0"
RED = "#b03030"


def _w(t, w=30):
    return "\n".join("\n".join(textwrap.wrap(ln, w)) if ln.strip() else ""
                     for ln in t.split("\n"))


def fig(w, h, xl, yl):
    f, ax = plt.subplots(figsize=(w, h), dpi=200)
    f.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(*xl)
    ax.set_ylim(*yl)
    ax.set_aspect("equal")
    ax.axis("off")
    return f, ax


def rbox(ax, cx, cy, w, h, text, fs=8.6, wrap=26, lw=1.2, fc="white"):
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, fc=fc, ec=INK, lw=lw))
    if text:
        ax.text(cx, cy, _w(text, wrap), ha="center", va="center", color=INK,
                fontsize=fs, linespacing=1.3)


def line(ax, x1, y1, x2, y2, lw=1.0, c=INK):
    ax.plot([x1, x2], [y1, y2], color=c, lw=lw, solid_capstyle="round")


def arr(ax, x1, y1, x2, y2, c=INK, lw=1.0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=lw, shrinkA=0, shrinkB=0))


def dot(ax, x, y, c=INK):
    ax.add_patch(Circle((x, y), 0.55, fc=c, ec=c))


def txt(ax, x, y, t, fs=8.4, ha="center", va="center", c=INK, bold=False):
    ax.text(x, y, t, ha=ha, va=va, color=c, fontsize=fs,
            fontweight="bold" if bold else "normal")


def netflag(ax, x, y, name, dx=0, ha="left"):
    """Nhan mang kieu EasyEDA (mui ten ngũ giac)."""
    s = 1 if ha == "left" else -1
    pts = [(x, y - 1.1), (x + s * 4.2, y - 1.1), (x + s * 5.6, y),
           (x + s * 4.2, y + 1.1), (x, y + 1.1)]
    ax.add_patch(Polygon(pts, closed=True, fc="white", ec=NET, lw=1.0))
    txt(ax, x - s * 0.8, y, name, fs=8.0, ha="right" if ha == "left" else "left", c=NET)


def gnd(ax, x, y, label="GND"):
    line(ax, x, y, x, y - 1.6)
    for i, w in enumerate((3.2, 2.2, 1.2)):
        line(ax, x - w / 2, y - 1.6 - i * 0.8, x + w / 2, y - 1.6 - i * 0.8, lw=1.0)
    txt(ax, x, y - 4.6, label, fs=8.2)


def vcc(ax, x, y, label="VCC"):
    line(ax, x, y, x, y + 1.4)
    line(ax, x - 1.8, y + 1.4, x + 1.8, y + 1.4, lw=1.2)
    txt(ax, x, y + 2.6, label, fs=8.2)


def save(f, name, sub=None):
    d = MACH if sub == "mach" else OUT
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    f.savefig(p, facecolor="white", bbox_inches="tight", pad_inches=0.18)
    plt.close(f)
    print("da ve:", os.path.relpath(p, os.path.dirname(OUT)))


# ============================================================== so do khoi
def so_do_khoi(axis=1):
    f, ax = fig(11.2, 6.4, (0, 112), (0, 66))
    txt(ax, 56, 63.5, "SƠ ĐỒ KHỐI HỆ THỐNG BÁM NẮNG %s TRỤC (ĐIỀU KHIỂN LAI)"
        % ("MỘT" if axis == 1 else "HAI"), fs=12, bold=True)
    rbox(ax, 15, 50, 24, 10, "Ma trận 4 LDR\ncó vách che giữa\n(4 góc tấm pin)")
    rbox(ax, 15, 35, 24, 8, "Biến trở hồi tiếp\ngóc tấm pin")
    rbox(ax, 15, 22, 24, 8, "Cầu chia áp đo\nđiện áp tấm pin")
    rbox(ax, 48, 55, 26, 9, "DS1307 (I²C)\ngiờ thực cho luật\nthiên văn")
    rbox(ax, 48, 40, 26, 14, "ESP32 DevKit\n– tính góc thiên văn\n– đọc ma trận LDR\n– suy lệch & tinh chỉnh")
    rbox(ax, 48, 22, 26, 8, "LCD I²C 1602\nhiển thị giờ, góc,\ntrạng thái")
    rbox(ax, 84, 50, 24, 10, "Opto PC817 →\ncầu H 4×TIP41C →\nđộng cơ trục vít")
    rbox(ax, 84, 34, 24, 8, "Công tắc hành trình\nqt1…qt4")
    rbox(ax, 84, 20, 24, 8, "Tấm pin 100 W\n(4 kg)")
    rbox(ax, 48, 8, 60, 7, "Nguồn 12 V → 1N4007 → LM2596 (3,3 V) và 7805 (5 V)")
    arr(ax, 27, 50, 35, 44); arr(ax, 27, 35, 35, 38); arr(ax, 27, 22, 35, 34)
    arr(ax, 48, 50.5, 48, 47)
    arr(ax, 61, 44, 72, 48); arr(ax, 72, 36, 61, 38)
    arr(ax, 84, 45, 84, 38); arr(ax, 84, 30, 84, 24)
    arr(ax, 61, 36, 68, 26); arr(ax, 68, 22, 61, 20)
    line(ax, 48, 8, 20, 8); line(ax, 20, 8, 20, 18); arr(ax, 20, 18, 20, 18.001)
    line(ax, 78, 8, 96, 8); line(ax, 96, 8, 96, 16); arr(ax, 96, 16, 96, 16.001)
    txt(ax, 33, 52, "ADC", fs=7.6, c=NET)
    txt(ax, 66, 46.5, "lệnh quay", fs=7.6, c=NET)
    txt(ax, 66, 34.5, "hồi tiếp", fs=7.6, c=NET)
    if axis == 2:
        txt(ax, 84, 57, "(hai kênh giống nhau:\nnghiêng + phương vị)", fs=7.6)
    save(f, "so_do_khoi_%d_truc.png" % axis)


# ============================================================== so do ket noi
def so_do_ket_noi(axis=1):
    f, ax = fig(11.6, 7.4, (0, 116), (0, 76))
    txt(ax, 58, 73.5, "SƠ ĐỒ KẾT NỐI ESP32 DEVKIT – HỆ %s TRỤC"
        % ("MỘT" if axis == 1 else "HAI"), fs=12, bold=True)
    ax.add_patch(Rectangle((44, 12), 28, 54, fc="white", ec=INK, lw=1.4))
    txt(ax, 58, 62, "ESP32 DevKit", fs=10, bold=True)
    left = [("GPIO25", "LDR trên-trái"), ("GPIO26", "LDR trên-phải"),
            ("GPIO27", "LDR dưới-trái"), ("GPIO14", "LDR dưới-phải"),
            ("GPIO36", "Biến trở hồi tiếp góc"),
            ("GPIO39", "Cầu chia áp tấm pin" if axis == 1 else "Biến trở hồi tiếp 2"),
            ("GPIO34", "qt1 hành trình"), ("GPIO35", "qt2 hành trình")]
    if axis == 2:
        left += [("GPIO32", "qt3 hành trình"), ("GPIO33", "qt4 hành trình")]
    right = [("GPIO21", "SDA (DS1307, LCD)"), ("GPIO22", "SCL (DS1307, LCD)"),
             ("GPIO19", "th_thuan (opto PH)"), ("GPIO18", "th_nguoc (opto PH)")]
    if axis == 2:
        right += [("GPIO5", "th_thuan trục 2"), ("GPIO13", "th_nguoc trục 2")]
    right += [("3V3", "Nguồn logic"), ("GND", "Mass chung")]
    y = 57
    for pin, name in left:
        txt(ax, 46.5, y, pin, fs=7.6, ha="left")
        line(ax, 44, y, 34, y)
        txt(ax, 33, y, name, fs=7.8, ha="right")
        y -= 4.6
    y = 57
    for pin, name in right:
        txt(ax, 69.5, y, pin, fs=7.6, ha="right")
        line(ax, 72, y, 82, y)
        txt(ax, 83, y, name, fs=7.8, ha="left")
        y -= 4.6
    txt(ax, 58, 15, "Không dùng WiFi khi chạy:\nbốn kênh LDR đặt trên ADC2", fs=7.8)
    txt(ax, 58, 7.5, "Opto PC817 cách ly tín hiệu 3,3 V với mạch động lực 12 V", fs=7.8)
    save(f, "so_do_ket_noi_%d_truc.png" % axis)


# ============================================================== bo tri LDR co vach che
def bo_tri_ldr():
    f, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.8), dpi=200,
                               gridspec_kw={"width_ratios": [1.1, 1]})
    f.patch.set_facecolor("white")
    for a in (a1, a2):
        a.set_facecolor("white")
        a.axis("off")
        a.set_aspect("equal")
    a1.set_xlim(-6, 106)
    a1.set_ylim(-8, 74)
    a1.add_patch(Rectangle((10, 8), 80, 54, fc="white", ec=INK, lw=1.4))
    line(a1, 50, 8, 50, 62, lw=1.2)          # vach che chu thap
    line(a1, 10, 35, 90, 35, lw=1.2)
    txt(a1, 50, 68, "Mặt trước tấm pin: 4 LDR ở 4 góc, vách che chữ thập giữa", fs=9, bold=True)
    for (x, y, name) in ((24, 48, "L_TT"), (76, 48, "L_PT"), (24, 20, "L_TD"), (76, 20, "L_PD")):
        a1.add_patch(Circle((x, y), 4.0, fc="white", ec=INK, lw=1.2))
        txt(a1, x, y - 7.5, name, fs=8.4)
    txt(a1, 50, 0, "Vách che tạo bóng chênh lệch khi lệch hướng", fs=8.4)
    a2.set_xlim(-6, 106)
    a2.set_ylim(-10, 70)
    line(a2, 10, 20, 90, 20, lw=1.4)
    txt(a2, 50, 15, "bề mặt tấm pin", fs=8.4)
    line(a2, 50, 20, 50, 58, lw=1.0)
    a2.plot([50, 76], [20, 54], color=INK, lw=1.2)
    arr(a2, 76, 54, 84, 64, lw=1.2)
    txt(a2, 86, 66, "trục cảm quang LDR", fs=8.4, ha="left")
    txt(a2, 52, 60, "pháp tuyến", fs=8.4, ha="left")
    a2.add_patch(Rectangle((48.6, 20), 2.8, 12, fc="white", ec=INK, lw=1.2))
    txt(a2, 44, 30, "vách che", fs=8.0, ha="right")
    th = [50 + 13 * math.cos(math.radians(t)) for t in range(52, 91)]
    thy = [20 + 13 * math.sin(math.radians(t)) for t in range(52, 91)]
    a2.plot(th, thy, color=INK, lw=1.0)
    txt(a2, 62, 36, "β_s = 30°", fs=9)
    txt(a2, 50, -4, "Mặt cắt: góc gá β_s và vách che giữa cụm", fs=8.4)
    f.tight_layout()
    save(f, "bo_tri_4_ldr.png")


# ============================================================== luu do
def _fdiamond(ax, cx, cy, w, h, t, fs=8.0):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(Polygon(pts, closed=True, fc="white", ec=INK, lw=1.1))
    txt(ax, cx, cy, _w(t, 26), fs=fs)


def luu_do_tong_quat():
    f, ax = fig(10.2, 12.6, (0, 102), (0, 132))
    txt(ax, 51, 129, "LƯU ĐỒ TỔNG QUÁT CHƯƠNG TRÌNH ĐIỀU KHIỂN LAI", fs=12, bold=True)
    rbox(ax, 42, 122, 30, 6, "BẮT ĐẦU: khởi tạo ADC, I²C, LCD, chân lệnh")
    rbox(ax, 42, 111, 34, 8, "Đọc giờ DS1307 → tính góc\nthiên văn (δ, H, α, γ)")
    rbox(ax, 42, 98, 34, 7, "Đọc biến trở → góc hiện tại θ")
    _fdiamond(ax, 42, 85, 34, 10, "|γ − θ| > 5° ?\n(lệch thô)")
    rbox(ax, 82, 85, 26, 8, "Chạy motor theo\nlịch thiên văn")
    rbox(ax, 42, 68, 34, 8, "Đọc 4 LDR → e1, e2;\ntổng sáng S")
    _fdiamond(ax, 42, 54, 34, 10, "S ≥ ngưỡng nắng\nvà |e| > ngưỡng ?")
    rbox(ax, 82, 54, 26, 8, "Tinh chỉnh motor\ntheo dấu e")
    rbox(ax, 12, 54, 22, 8, "Giữ vị trí\n(theo lịch)")
    rbox(ax, 42, 38, 34, 7, "Đọc công tắc hành trình,\nchặn chiều nguy hiểm")
    rbox(ax, 42, 26, 34, 7, "Hiển thị LCD: giờ, góc,\ne1, e2, trạng thái")
    rbox(ax, 42, 14, 34, 6, "Ghi log Serial, chờ chu kỳ, lặp lại")
    arr(ax, 42, 119, 42, 115); arr(ax, 42, 107, 42, 101.5); arr(ax, 42, 94.5, 42, 90)
    arr(ax, 59, 85, 69, 85); txt(ax, 64, 87, "đúng", fs=7.8)
    arr(ax, 42, 80, 42, 72); txt(ax, 45, 76, "sai", fs=7.8)
    arr(ax, 42, 64, 42, 59)
    arr(ax, 59, 54, 69, 54); txt(ax, 64, 56, "đúng", fs=7.8)
    arr(ax, 25, 54, 23, 54); arr(ax, 25, 54, 25, 54.001)
    line(ax, 25, 54, 23, 54); txt(ax, 33, 57, "sai", fs=7.8)
    arr(ax, 42, 49, 42, 41.5)
    line(ax, 82, 81, 82, 76); line(ax, 82, 76, 96, 76); line(ax, 96, 76, 96, 38)
    line(ax, 82, 50, 82, 46); line(ax, 82, 46, 96, 46)
    line(ax, 12, 50, 12, 38); line(ax, 12, 38, 25, 38)
    arr(ax, 42, 34.5, 42, 29.5); arr(ax, 42, 22.5, 42, 17)
    line(ax, 25, 38, 25, 14); line(ax, 25, 14, 25, 14.001)
    line(ax, 96, 38, 59, 38)
    line(ax, 25, 14, 25, 6); line(ax, 25, 6, 42, 6); arr(ax, 42, 6, 42, 11)
    save(f, "luu_do_tong_quat.png")


def luu_do_thien_van():
    f, ax = fig(9.4, 10.4, (0, 94), (0, 110))
    txt(ax, 47, 107, "LƯU ĐỒ NHÁNH THIÊN VĂN (VÒNG HỞ TỪ RTC)", fs=11.5, bold=True)
    rbox(ax, 44, 100, 34, 6, "Đọc DS1307: giờ, phút, giây, ngày")
    rbox(ax, 44, 89, 40, 8, "Đổi sang giờ Mặt Trời t theo kinh độ 106,06°")
    rbox(ax, 44, 76, 44, 9, "δ = 23,45°·sin[360°·(284+n)/365]\nH = 15°·(t − 12)")
    rbox(ax, 44, 62, 46, 9, "sin α = sin φ·sin δ + cos φ·cos δ·cos H\nγ = atan2(sin H, cos H·sin φ − tan δ·cos φ)")
    rbox(ax, 44, 48, 40, 8, "Quy đổi γ về góc lệnh trục quay\ncộng hệ số lắp đặt")
    _fdiamond(ax, 44, 34, 36, 10, "|góc lệnh − θ hiện tại| > 2° ?")
    rbox(ax, 44, 18, 36, 7, "Phát xung motor tới góc lệnh\n(kiểm tra hành trình)")
    rbox(ax, 44, 7, 30, 5, "Giữ vị trí, chờ chu kỳ sau")
    for y1, y2 in ((97, 93), (85, 80.5), (71.5, 66.5), (57.5, 52), (44, 39), (29, 21.5)):
        arr(ax, 44, y1, 44, y2)
    arr(ax, 62, 34, 74, 34); line(ax, 74, 34, 74, 7); line(ax, 74, 7, 59, 7)
    txt(ax, 66, 36, "sai", fs=7.8); txt(ax, 47, 25, "đúng", fs=7.8)
    save(f, "luu_do_thien_van.png")


def luu_do_ldr():
    f, ax = fig(9.4, 10.4, (0, 94), (0, 110))
    txt(ax, 47, 107, "LƯU ĐỒ NHÁNH LDR (VÒNG KÍN TINH CHỈNH)", fs=11.5, bold=True)
    rbox(ax, 44, 100, 40, 6, "Đọc 4 kênh ADC: 32 mẫu, lấy trung bình")
    rbox(ax, 44, 89, 44, 8, "S = tổng 4 kênh; e1 = (trái − phải)/S;\ne2 = (trên − dưới)/S")
    _fdiamond(ax, 44, 74, 36, 10, "S ≥ ngưỡng nắng ?")
    rbox(ax, 80, 74, 24, 7, "Chuyển chế độ\ntheo lịch thiên văn")
    _fdiamond(ax, 44, 57, 36, 10, "|e1| > ngưỡng chết ?")
    rbox(ax, 44, 41, 38, 7, "Quay trục 1 theo dấu e1\nmột bước tinh chỉnh")
    _fdiamond(ax, 44, 26, 36, 9, "|e2| > ngưỡng chết ?")
    rbox(ax, 44, 12, 38, 6, "Quay trục 2 theo dấu e2 (bản 2 trục)")
    rbox(ax, 12, 26, 20, 6, "Dừng motor")
    arr(ax, 44, 97, 44, 93); arr(ax, 44, 85, 44, 79)
    arr(ax, 62, 74, 68, 74); txt(ax, 65, 76, "sai", fs=7.8)
    arr(ax, 44, 69, 44, 62); txt(ax, 47, 65.5, "đúng", fs=7.8)
    arr(ax, 44, 52, 44, 44.5); txt(ax, 47, 48, "đúng", fs=7.8)
    arr(ax, 44, 37.5, 44, 30.5); txt(ax, 47, 34, "sai", fs=7.8)
    arr(ax, 44, 21.5, 44, 15); txt(ax, 47, 18, "đúng", fs=7.8)
    arr(ax, 26, 26, 25, 26); line(ax, 26, 26, 22, 26); txt(ax, 34, 28.5, "sai", fs=7.8)
    line(ax, 80, 70.5, 80, 66); line(ax, 80, 66, 90, 66); line(ax, 90, 66, 90, 6)
    line(ax, 44, 9, 44, 6); line(ax, 44, 6, 90, 6)
    save(f, "luu_do_ldr.png")


def luu_do_dong_co():
    f, ax = fig(9.4, 9.6, (0, 94), (0, 102))
    txt(ax, 47, 99, "LƯU ĐỒ ĐIỀU KHIỂN ĐỘNG CƠ QUA OPTO – CẦU H", fs=11.5, bold=True)
    rbox(ax, 44, 92, 40, 6, "Nhận lệnh chiều quay và số xung")
    _fdiamond(ax, 44, 79, 36, 9, "Công tắc hành trình\nchiều đó = 0 ?")
    rbox(ax, 80, 79, 24, 6, "Bỏ lệnh, báo LCD")
    rbox(ax, 44, 64, 42, 7, "Hạ mức chân th_thuan hoặc th_nguoc\n(opto dẫn, cầu H mở chiều tương ứng)")
    rbox(ax, 44, 51, 38, 6, "Đếm xung / đọc biến trở hồi tiếp")
    _fdiamond(ax, 44, 38, 36, 9, "Tới góc đích hoặc\nhết số xung ?")
    rbox(ax, 44, 24, 40, 6, "Đưa cả hai chân lệnh lên mức cao\n(cầu H khóa, trục vít tự giữ)")
    rbox(ax, 44, 12, 30, 5, "Trả trạng thái về vòng chính")
    arr(ax, 44, 89, 44, 83.5)
    arr(ax, 62, 79, 68, 79); txt(ax, 65, 81, "đúng", fs=7.8)
    arr(ax, 44, 74.5, 44, 67.5); txt(ax, 47, 71, "sai", fs=7.8)
    arr(ax, 44, 60.5, 44, 54); arr(ax, 44, 48, 44, 42.5)
    arr(ax, 44, 33.5, 44, 27); txt(ax, 47, 30, "đúng", fs=7.8)
    line(ax, 26, 38, 14, 38); line(ax, 14, 38, 14, 45); arr(ax, 14, 45, 23, 45)
    txt(ax, 20, 40, "sai: quay tiếp", fs=7.6)
    arr(ax, 44, 21, 44, 14.5)
    line(ax, 80, 76, 80, 70); line(ax, 80, 70, 88, 70); line(ax, 88, 70, 88, 12)
    line(ax, 88, 12, 59, 12)
    save(f, "luu_do_dong_co.png")


def luu_do_hien_thi():
    f, ax = fig(9.4, 8.6, (0, 94), (0, 92))
    txt(ax, 47, 89, "LƯU ĐỒ ĐỌC GIỜ DS1307 VÀ HIỂN THỊ LCD I²C", fs=11.5, bold=True)
    rbox(ax, 44, 82, 40, 6, "Mỗi 1 s: Wire.requestFrom(0x68, 7)")
    rbox(ax, 44, 71, 44, 7, "Giải mã BCD: giây, phút, giờ,\nthứ, ngày, tháng, năm")
    rbox(ax, 44, 58, 44, 7, "Tính giờ Mặt Trời và góc thiên văn\ntương ứng")
    rbox(ax, 44, 45, 44, 7, "Lấy góc thực tế từ biến trở,\ne1, e2 từ ma trận LDR")
    rbox(ax, 44, 31, 46, 8, "LCD dòng 1: gg:mm:ss  góc lệnh\nLCD dòng 2: góc thực, e1, e2, chế độ")
    rbox(ax, 44, 17, 40, 6, "Nếu mất I²C: báo lỗi “RTC/LCD” và\ngiữ chế độ lịch cuối")
    for y1, y2 in ((79, 74.5), (67.5, 61.5), (54.5, 48.5), (41.5, 35), (27, 20)):
        arr(ax, 44, y1, 44, y2)
    line(ax, 44, 14, 44, 9); line(ax, 80, 9, 80, 82); arr(ax, 80, 82, 64, 82)
    save(f, "luu_do_hien_thi.png")


# ============================================================== 7 so do mach ve lai
def mach_cau_h():
    f, ax = fig(10.8, 7.4, (0, 108), (0, 74))
    txt(ax, 54, 71, "MẠCH ĐỘNG LỰC: CẦU H 4 TIP41C + DIODE BẢO VỆ", fs=11.5, bold=True)
    line(ax, 16, 64, 92, 64, lw=1.2); vcc(ax, 54, 64, "VCC 12 V")
    line(ax, 16, 8, 92, 8, lw=1.2); gnd(ax, 54, 8)
    # hai nua cau
    for (x, top, bot, btop, bbot) in ((32, "U1", "U2", "dkxuoi", "dknguoc"),
                                      (76, "U3", "U4", "dknguoc", "dkxuoi")):
        line(ax, x, 64, x, 58)
        rbox(ax, x, 52, 11, 12, top + "\nTIP41C", fs=7.6, wrap=10)
        txt(ax, x, 56.6, "C", fs=6.6); txt(ax, x, 47.4, "E", fs=6.6)
        line(ax, x, 46, x, 38)
        dot(ax, x, 38)
        line(ax, x, 38, x, 30)
        rbox(ax, x, 24, 11, 12, bot + "\nTIP41C", fs=7.6, wrap=10)
        txt(ax, x, 28.6, "C", fs=6.6); txt(ax, x, 19.4, "E", fs=6.6)
        line(ax, x, 18, x, 8)
        # base + tro 10k + net flag
        sgn = -1 if x == 32 else 1
        for (cy, net) in ((52, btop), (24, bbot)):
            line(ax, x - sgn * 5.5, cy, x - sgn * 12, cy)
            ax.add_patch(Rectangle((min(x - sgn * 16, x - sgn * 12), cy - 1.2), 4, 2.4,
                                   fc="white", ec=INK, lw=1.0))
            txt(ax, x - sgn * 14, cy + 2.4, "10k", fs=7.0)
            if sgn < 0:
                netflag(ax, x - 18, cy, net, ha="right")
            else:
                netflag(ax, x + 18, cy, net)
        # diode bao ve doc theo nua cau
        xd = x + (8 if x == 32 else -8)
        for (y1, y2, up) in ((64, 38, True), (38, 8, False)):
            line(ax, xd, y1, xd, y1 - (3 if up else 0))
            ym = (y1 + y2) / 2 + (6 if up else -6)
            if up:
                ax.add_patch(Polygon([(xd - 1.7, ym - 3), (xd + 1.7, ym - 3), (xd, ym + 3)],
                                     closed=True, fc="white", ec=INK, lw=1.0))
                line(ax, xd - 1.7, ym + 3, xd + 1.7, ym + 3)
            else:
                ax.add_patch(Polygon([(xd - 1.7, ym + 3), (xd + 1.7, ym + 3), (xd, ym - 3)],
                                     closed=True, fc="white", ec=INK, lw=1.0))
                line(ax, xd - 1.7, ym - 3, xd + 1.7, ym - 3)
            line(ax, xd, y2 + (3 if not up else 0), xd, y2)
            line(ax, xd, y1, x, y1) if y1 == 64 else line(ax, xd, y1, x, y1)
            dot(ax, xd, 38)
        txt(ax, xd + 3, 55, "D2" if x == 32 else "D5", fs=7.2, ha="left")
        txt(ax, xd + 3, 20, "D3" if x == 32 else "D4", fs=7.2, ha="left")
    # dong co giua hai nut
    rbox(ax, 54, 38, 14, 9, "ĐỘNG CƠ", fs=8.0, wrap=12)
    line(ax, 32, 38, 47, 38); line(ax, 61, 38, 76, 38)
    txt(ax, 54, 30, "đầu A                          đầu B", fs=7.2)
    txt(ax, 54, 3, "dkxuoi = 0: U1–U4 dẫn cặp chéo trái; dknguoc = 0: cặp chéo phải; cả hai = 1: cầu H khoá", fs=8.0)
    save(f, "mach_dong_luc_cau_h_tip41c.png", sub="mach")


def mach_opto():
    f, ax = fig(10.2, 6.4, (0, 102), (0, 64))
    txt(ax, 51, 61, "MẠCH CÁCH LY OPTO PC817C ĐIỀU KHIỂN CẦU H", fs=11.5, bold=True)
    for (cy, th, dk, ph) in ((44, "th_thuan", "dkxuoi", "PH2"), (18, "th_nguoc", "dknguoc", "PH1")):
        rbox(ax, 51, cy, 14, 12, ph + "\nPC817C", fs=7.6, wrap=12)
        vcc(ax, 40, cy + 6, "3,3 V")
        line(ax, 40, cy + 6, 44, cy + 6)
        netflag(ax, 20, cy - 6, th, ha="right")
        line(ax, 26, cy - 6, 32, cy - 6)
        ax.add_patch(Rectangle((32, cy - 7.2), 6, 2.4, fc="white", ec=INK, lw=1.0))
        txt(ax, 35, cy - 4.2, "220", fs=7.2)
        line(ax, 38, cy - 6, 44, cy - 6)
        line(ax, 58, cy + 6, 66, cy + 6); vcc(ax, 66, cy + 6, "12 V")
        line(ax, 58, cy - 6, 74, cy - 6)
        netflag(ax, 74, cy - 6, dk)
    txt(ax, 51, 5, "Chân lệnh ESP32 mức thấp sẽ sáng LED opto, transistor quang dẫn xuống mass 12 V", fs=8.2)
    save(f, "mach_opto_pc817.png", sub="mach")


def mach_hanh_trinh():
    f, ax = fig(10.2, 6.8, (0, 102), (0, 68))
    txt(ax, 51, 65, "BỐN CÔNG TẮC HÀNH TRÌNH QT1…QT4 (KÉO XUỐNG 1k)", fs=11.5, bold=True)
    for i, (cx, name, net) in enumerate(((18, "QT1", "qt1"), (40, "QT2", "qt2"),
                                         (62, "QT3", "qt3"), (84, "QT4", "qt4"))):
        vcc(ax, cx, 52, "3,3 V")
        line(ax, cx, 52, cx, 46)
        rbox(ax, cx, 41, 8, 9, name, fs=7.6, wrap=8)
        line(ax, cx, 36.5, cx, 30)
        dot(ax, cx, 30)
        netflag(ax, cx + 3, 30, net)
        line(ax, cx, 30, cx, 26)
        ax.add_patch(Rectangle((cx - 1.6, 18), 3.2, 8, fc="white", ec=INK, lw=1.0))
        txt(ax, cx + 3, 22, "1k", fs=7.2, ha="left")
        gnd(ax, cx, 18)
    txt(ax, 51, 6, "Công tắc hở: qt = 0; chạm hành trình: qt = 3,3 V → mức 1", fs=8.2)
    save(f, "mach_cong_tac_hanh_trinh.png", sub="mach")


def mach_esp32():
    f, ax = fig(9.6, 7.6, (0, 96), (0, 76))
    txt(ax, 48, 73, "KHỐI ESP32 DEVKIT VÀ CÁC MẠNG TÍN HIỆU", fs=11.5, bold=True)
    ax.add_patch(Rectangle((34, 14), 28, 52, fc="white", ec=INK, lw=1.4))
    txt(ax, 48, 62, "ESP32 DevKit", fs=10, bold=True)
    pins = [("D25", "LDR TT"), ("D26", "LDR PT"), ("D27", "LDR TD"), ("D14", "LDR PD"),
            ("D36", "biến trở"), ("D39", "áp tấm pin"), ("D34", "qt1"), ("D35", "qt2"),
            ("D32", "qt3"), ("D33", "qt4")]
    y = 56
    for p, n in pins:
        txt(ax, 36, y, p, fs=7.4, ha="left")
        line(ax, 34, y, 26, y)
        txt(ax, 25, y, n, fs=7.6, ha="right")
        y -= 4.4
    rp = [("D21", "sda"), ("D22", "scl"), ("D19", "th_thuan"), ("D18", "th_nguoc"),
          ("D5", "th_thuan 2"), ("D13", "th_nguoc 2"), ("3V3", "3,3 V"), ("GND", "mass")]
    y = 56
    for p, n in rp:
        txt(ax, 60, y, p, fs=7.4, ha="right")
        line(ax, 62, y, 70, y)
        txt(ax, 71, y, n, fs=7.6, ha="left")
        y -= 4.4
    txt(ax, 48, 8, "Bản một trục bỏ hai mạng th_thuan 2 / th_nguoc 2", fs=8.2)
    save(f, "mach_esp32_devkit.png", sub="mach")


def mach_nguon():
    f, ax = fig(10.2, 5.6, (0, 102), (0, 56))
    txt(ax, 51, 53, "MẠCH NGUỒN: CHỐNG NGƯỢC CỰC + HẠ ÁP LM2596", fs=11.5, bold=True)
    rbox(ax, 12, 34, 10, 10, "X1\nnguồn\n12 V", fs=7.4, wrap=9)
    line(ax, 17, 37, 26, 37)
    ax.add_patch(Polygon([(26, 34.6), (26, 39.4), (31, 37)], closed=True, fc="white", ec=INK, lw=1.0))
    line(ax, 31, 34.6, 31, 39.4)
    txt(ax, 28, 41.5, "1N4007", fs=7.4)
    line(ax, 31, 37, 44, 37); dot(ax, 44, 37); vcc(ax, 44, 37, "VCC 12 V")
    rbox(ax, 58, 34, 22, 12, "BC\nLM2596", fs=8.0, wrap=12)
    line(ax, 44, 37, 47, 37)
    txt(ax, 48.5, 40, "IN+", fs=7.0, ha="left")
    line(ax, 47, 30, 47, 26); gnd(ax, 47, 26)
    txt(ax, 48.5, 28, "IN-", fs=7.0, ha="left")
    line(ax, 69, 37, 80, 37); vcc(ax, 80, 37, "3,3 V")
    txt(ax, 67.5, 40, "OUT+", fs=7.0, ha="right")
    line(ax, 69, 30, 76, 30); gnd(ax, 76, 30)
    txt(ax, 67.5, 28, "OUT-", fs=7.0, ha="right")
    line(ax, 12, 29, 12, 22); gnd(ax, 12, 22)
    txt(ax, 51, 6, "LM2596 cấp 3,3 V cho ESP32; nhánh 7805 riêng cấp 5 V cho LCD và DS1307", fs=8.2)
    save(f, "mach_nguon_lm2596.png", sub="mach")


def mach_7805_lcd():
    f, ax = fig(10.2, 6.2, (0, 102), (0, 62))
    txt(ax, 51, 59, "NHÁNH 5 V: ỔN ÁP 7805 VÀ MÀN HÌNH LCD I²C 1602", fs=11.5, bold=True)
    vcc(ax, 20, 46, "VCC 12 V")
    line(ax, 20, 46, 20, 40)
    rbox(ax, 34, 40, 20, 9, "U6  7805", fs=8.2, wrap=14)
    line(ax, 20, 40, 24, 40); txt(ax, 25.5, 42, "IN", fs=7.2, ha="left")
    line(ax, 44, 40, 56, 40); vcc(ax, 56, 40, "+5 V")
    txt(ax, 42.5, 42, "OUT", fs=7.2, ha="right")
    line(ax, 34, 35.5, 34, 30); gnd(ax, 34, 30)
    line(ax, 20, 40, 20, 34); line(ax, 18.4, 34, 21.6, 34); line(ax, 18.8, 32.6, 21.2, 32.6)
    txt(ax, 24, 33, "C1 220µ", fs=7.2, ha="left")
    line(ax, 56, 40, 56, 34); line(ax, 54.4, 34, 57.6, 34); line(ax, 54.8, 32.6, 57.2, 32.6)
    txt(ax, 60, 33, "C2 220µ", fs=7.2, ha="left")
    line(ax, 20, 32, 56, 32); dot(ax, 34, 32)
    rbox(ax, 62, 16, 44, 16, "U5 – LCD 1602 I²C\n(PCF8574, địa chỉ 0x27)", fs=8.2, wrap=30)
    for i, (n, nn) in enumerate((("GND", None), ("Vcc", "+5 V"), ("SDA", "sda"), ("SCL", "scl"))):
        y = 21 - i * 3
        line(ax, 40, y, 30, y)
        txt(ax, 39, y, n, fs=7.2, ha="right")
        if nn:
            txt(ax, 29, y, nn, fs=7.4, ha="right", c=NET)
    gnd(ax, 24, 21)
    txt(ax, 51, 4, "LCD và DS1307 chung bus I²C (sda/scl) với điện trở kéo lên trên module", fs=8.2)
    save(f, "mach_7805_lcd_i2c.png", sub="mach")


def mach_ds1307():
    f, ax = fig(9.6, 5.6, (0, 96), (0, 56))
    txt(ax, 48, 53, "MODULE THỜI GIAN THỰC DS1307 (I²C 0x68)", fs=11.5, bold=True)
    ax.add_patch(Rectangle((20, 14), 40, 28, fc="white", ec=INK, lw=1.3))
    txt(ax, 40, 34, "U7  DS1307", fs=9.5, bold=True)
    ax.add_patch(Circle((30, 24), 6, fc="white", ec=INK, lw=1.1))
    txt(ax, 30, 24, "pin nuôi", fs=6.8)
    pins = [("SQW", None), ("SCL", "scl"), ("SDA", "sda"), ("VCC", "+5 V"), ("GND", None)]
    y = 38
    for n, nn in pins:
        line(ax, 60, y, 70, y)
        txt(ax, 58.5, y, n, fs=7.6, ha="right")
        if nn:
            netflag(ax, 70, y, nn)
        elif n == "VCC":
            vcc(ax, 74, y, "+5 V")
        elif n == "GND":
            gnd(ax, 74, y)
        y -= 5.5
    txt(ax, 48, 6, "Pin SQW để trống; giao tiếp Wire.beginTransmission(0x68)", fs=8.2)
    save(f, "mach_ds1307.png", sub="mach")


if __name__ == "__main__":
    so_do_khoi(1)
    so_do_khoi(2)
    so_do_ket_noi(1)
    so_do_ket_noi(2)
    bo_tri_ldr()
    luu_do_tong_quat()
    luu_do_thien_van()
    luu_do_ldr()
    luu_do_dong_co()
    luu_do_hien_thi()
    mach_cau_h()
    mach_opto()
    mach_hanh_trinh()
    mach_esp32()
    mach_nguon()
    mach_7805_lcd()
    mach_ds1307()
