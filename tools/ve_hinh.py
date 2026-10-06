# -*- coding: utf-8 -*-
"""Vẽ các sơ đồ / hình minh họa cho báo cáo đồ án bám nắng.

Phong cách đồng bộ với lưu đồ có sẵn (Luu_do_thuat_toan_bam_nang_4_LDR.png):
nền xanh nhạt, ô chữ nhật xanh nhạt/trắng, hình thoi vàng nhạt, oval xanh lá,
đường viền và chữ màu xanh đậm.
Chạy:  python3 tools/ve_hinh.py
"""
import math
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Ellipse, Circle, Rectangle

BG = "#eef2f9"
BLUE = "#d7e4f6"
WHITE = "#fbfdff"
YELLOW = "#fbe7b6"
GREEN = "#d9ecdc"
EDGE = "#1f3864"
TXT = "#16324f"
ACC = "#2e5f9e"

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hinh_ve")


def _wrap(t, w=34):
    out = []
    for ln in t.split("\n"):
        out.append("\n".join(textwrap.wrap(ln, w)) if ln.strip() else "")
    return "\n".join(out)


def new_fig(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, cx, cy, w, h, text, kind="proc", fs=9.0, wrap=34, bold=False):
    fills = {"proc": BLUE, "io": WHITE, "dec": YELLOW, "start": GREEN, "term": GREEN}
    if kind == "dec":
        pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
        ax.add_patch(Polygon(pts, closed=True, fc=fills[kind], ec=EDGE, lw=1.6))
    elif kind in ("start", "term"):
        ax.add_patch(Ellipse((cx, cy), w, h, fc=fills[kind], ec=EDGE, lw=1.6))
    else:
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                    boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=fills[kind], ec=EDGE, lw=1.6))
    ax.text(cx, cy, _wrap(text, wrap), ha="center", va="center", color=TXT,
            fontsize=fs, fontweight="bold" if (bold or kind == "dec") else "normal",
            linespacing=1.35)


def arrow(ax, x1, y1, x2, y2, label=None, lx=None, ly=None, fs=8.5, rad=None):
    style = "arc3,rad=%s" % rad if rad is not None else "arc3,rad=0"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=1.8,
                                connectionstyle=style, shrinkA=0, shrinkB=0))
    if label:
        ax.text(lx if lx is not None else (x1 + x2) / 2,
                ly if ly is not None else (y1 + y2) / 2,
                label, ha="center", va="center", color=ACC,
                fontsize=fs, fontweight="bold")


def line(ax, x1, y1, x2, y2, lw=1.8):
    ax.plot([x1, x2], [y1, y2], color=EDGE, lw=lw, solid_capstyle="round")


def title(ax, x, y, text, fs=13):
    ax.text(x, y, text, ha="center", va="center", color=TXT,
            fontsize=fs, fontweight="bold")


def note(ax, x, y, text, fs=8.5, ha="center"):
    ax.text(x, y, text, ha=ha, va="center", color=ACC, fontsize=fs, fontweight="bold")


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    fig.savefig(p, facecolor=BG, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("đã vẽ:", p)


# ------------------------------------------------------------------ 1) bố trí 4 LDR
def ve_bo_tri_ldr():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.2), dpi=200,
                                 gridspec_kw={"width_ratios": [1.15, 1]})
    fig.patch.set_facecolor(BG)
    for a in (a1, a2):
        a.set_facecolor(BG)
        a.axis("off")
        a.set_aspect("equal")
    a1.set_xlim(-10, 110)
    a1.set_ylim(-8, 78)
    a1.add_patch(FancyBboxPatch((8, 8), 84, 56, boxstyle="round,pad=0,rounding_size=2",
                                fc=WHITE, ec=EDGE, lw=2))
    a1.text(50, 70, "Mặt trước tấm pin (nhìn thẳng góc)", ha="center", va="center",
            color=TXT, fontsize=10, fontweight="bold")
    pos = {"L_TT": (16, 56, -1, 1), "L_PT": (84, 56, 1, 1),
           "L_TD": (16, 16, -1, -1), "L_PD": (84, 16, 1, -1)}
    for k, (x, y, dx, dy) in pos.items():
        a1.add_patch(Circle((x, y), 4.2, fc=BLUE, ec=EDGE, lw=1.6))
        a1.annotate("", xy=(x + dx * 11, y + dy * 9), xytext=(x, y),
                    arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2))
        a1.text(x + dx * 3.4, y + dy * 3.4 - (2 if dy < 0 else -2), k, ha="center",
                va="center", color=TXT, fontsize=9, fontweight="bold")
    a1.text(50, 36, "Pháp tuyến\nmặt pin", ha="center", va="center", color=ACC,
            fontsize=8.5, fontweight="bold")
    a1.text(50, -3, "Mỗi cảm biến gá chếch ra ngoài tâm cụm một góc β_s bằng nhau",
            ha="center", va="center", color=TXT, fontsize=9)
    a2.set_xlim(-6, 106)
    a2.set_ylim(-10, 74)
    line(a2, 10, 20, 90, 20, 2.4)
    a2.text(50, 15, "Bề mặt tấm pin", ha="center", va="center", color=TXT, fontsize=9)
    line(a2, 50, 20, 50, 62)
    a2.plot([50, 78], [20, 56], color=ACC, lw=2)
    a2.annotate("", xy=(86, 66), xytext=(78, 56),
                arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2))
    a2.text(88, 69, "Trục cảm quang LDR", ha="left", va="center", color=ACC,
            fontsize=9, fontweight="bold")
    a2.text(52, 64, "Pháp tuyến", ha="left", va="center", color=TXT, fontsize=9)
    a2.add_patch(Ellipse((50, 20), 7, 7, fc=BLUE, ec=EDGE, lw=1.6))
    th = [50 + 14 * math.cos(math.radians(t)) for t in range(52, 91)]
    th_y = [20 + 14 * math.sin(math.radians(t)) for t in range(52, 91)]
    a2.plot(th, th_y, color=EDGE, lw=1.4)
    a2.text(63, 38, "β_s", ha="center", va="center", color=TXT, fontsize=10,
            fontweight="bold")
    a2.text(50, -4, "Mặt cắt: góc gá β_s giữa pháp tuyến và trục cảm quang",
            ha="center", va="center", color=TXT, fontsize=9)
    fig.tight_layout()
    save(fig, "bo_tri_4_ldr.png")


# ------------------------------------------------------------------ 2) sơ đồ khối hệ thống
def ve_so_do_khoi(axis="mot"):
    fig, ax = new_fig(11, 6.4, (0, 110), (0, 70))
    if axis == "mot":
        ctrl = "ESP32\nlọc – thuật toán lai – ghi dữ liệu"
        act = "Cơ cấu chấp hành 1 trục\n(servo mô-men cao / actuator)"
        mid = "Lọc, bù sai khác,\ntính S, e_quay, e_nghiêng"
        aux = "BH1750 tham chiếu\n(I²C)"
    else:
        ctrl = "Arduino Mega\nquy đổi R, so sánh 4 LDR"
        act = "Servo phương vị +\nmotor nghiêng (cầu H, encoder)"
        mid = "Lọc, quy đổi R_LDR,\ne_nghiêng, e_quay"
        aux = "Công tắc hành trình\n4 đầu (2 trục)"
    box(ax, 14, 58, 22, 10, "Cụm 4 LDR\n(4 góc tấm pin)", "io")
    box(ax, 14, 44, 22, 9, "Cầu phân áp + lọc nhiễu", "proc", fs=8.4, wrap=24)
    box(ax, 14, 30, 22, 9, aux, "io", fs=8.4, wrap=24)
    box(ax, 14, 16, 22, 9, "RTC DS3231\n(I²C)", "io", fs=8.6)
    box(ax, 50, 52, 26, 10, mid, "proc", fs=8.6)
    box(ax, 50, 32, 26, 12, ctrl, "proc", fs=9.2, wrap=26)
    box(ax, 50, 13, 26, 9, "Khối đo U, I của pin và\nđiện năng cơ cấu", "io", fs=8.4, wrap=26)
    box(ax, 88, 42, 18, 13, act, "proc", fs=8.4, wrap=20)
    box(ax, 88, 20, 18, 10, "Tấm pin\nmặt trời", "term", fs=9.5, wrap=16)
    arrow(ax, 14, 53, 14, 48.5)
    arrow(ax, 25, 44, 37, 49, rad=-0.2)
    arrow(ax, 25, 30, 37, 32, rad=0.12)
    arrow(ax, 25, 16, 37, 28, rad=0.2)
    arrow(ax, 50, 47, 50, 38)
    arrow(ax, 63, 32, 79, 39, rad=-0.2)
    arrow(ax, 88, 35.5, 88, 25)
    arrow(ax, 79, 18, 63, 14, rad=-0.2)
    line(ax, 88, 48.5, 88, 60)
    line(ax, 88, 60, 50, 60)
    arrow(ax, 50, 60, 50, 57)
    note(ax, 70, 63, "Phản hồi góc / trạng thái giới hạn")
    title(ax, 55, 67.5, "SƠ ĐỒ KHỐI HỆ THỐNG BÁM NẮNG %s TRỤC" % ("MỘT" if axis == "mot" else "HAI"))
    save(fig, "so_do_khoi_%s_truc.png" % ("1" if axis == "mot" else "2"))


# ------------------------------------------------------------------ 3) sơ đồ kết nối
def ve_ket_noi(axis="mot"):
    fig, ax = new_fig(11.5, 6.6, (0, 115), (0, 72))
    if axis == "mot":
        ten = "ESP32 DEV KIT"
        left = [("Cụm 4 LDR (cầu phân áp)", "GPIO36/39/34/35 (ADC1)"),
                ("BH1750 đo sáng tham chiếu", "GPIO21 (SDA) – GPIO22 (SCL)"),
                ("RTC DS3231", "GPIO21 (SDA) – GPIO22 (SCL)"),
                ("Cầu chia áp đo U pin", "GPIO32 (ADC1_CH4)"),
                ("Cảm biến dòng ACS712", "GPIO33 (ADC1_CH5)")]
        right = [("Driver / servo 1 trục (PWM)", "GPIO26 (LEDC_PWM)"),
                 ("Công tắc hành trình ĐÔNG", "GPIO4 (INPUT_PULLUP)"),
                 ("Công tắc hành trình TÂY", "GPIO5 (INPUT_PULLUP)"),
                 ("Nút dừng khẩn cấp", "GPIO18 (INPUT_PULLUP)"),
                 ("Serial Monitor / ghi log", "USB-UART (GPIO1/3)")]
    else:
        ten = "ARDUINO MEGA 2560"
        left = [("Cụm 4 LDR (cầu phân áp)", "A0 – A1 – A2 – A3"),
                ("RTC DS3231", "20 (SDA) – 21 (SCL)"),
                ("Encoder motor nghiêng", "2 (INT0) – 3 (INT1)"),
                ("Cầu chia áp đo U pin", "A6"),
                ("Cảm biến dòng ACS712", "A7")]
        right = [("Servo phương vị", "12 (thư viện Servo)"),
                 ("Cầu H: chân PWM", "10 (PWM)"),
                 ("Cầu H: chiều quay A/B", "22 – 23"),
                 ("Công tắc hành trình 4 đầu", "26 – 27 – 28 – 29"),
                 ("Serial Monitor / ghi log", "USB (Serial0)")]
    box(ax, 57, 36, 34, 44, "", "proc")
    ax.text(57, 55, ten, ha="center", va="center", color=TXT, fontsize=11.5, fontweight="bold")
    ax.text(57, 50.8, "Vi điều khiển trung tâm", ha="center", va="center", color=ACC, fontsize=8.5)
    y0 = 45
    for i, (name, pin) in enumerate(left):
        y = y0 - i * 7.4
        box(ax, 15, y, 26, 6, name, "io", fs=8.2, wrap=28)
        line(ax, 28, y, 40, y)
        ax.add_patch(Circle((40, y), 0.7, fc=EDGE, ec=EDGE))
        ax.text(56.4, y, pin, ha="right", va="center", color=TXT, fontsize=7.2)
    for i, (name, pin) in enumerate(right):
        y = y0 - i * 7.4
        box(ax, 98, y, 28, 6, name, "io", fs=8.2, wrap=28)
        line(ax, 74, y, 84, y)
        ax.add_patch(Circle((74, y), 0.7, fc=EDGE, ec=EDGE))
        ax.text(57.6, y, pin, ha="left", va="center", color=TXT, fontsize=7.2)
    title(ax, 57, 66, "SƠ ĐỒ KẾT NỐI CẢM BIẾN – CƠ CẤU (%s)" % ten)
    note(ax, 57, 3, "Bảng chân mang tính đề xuất; chốt lại sau khi đối chiếu sơ đồ mạch và tài liệu bo mạch.")
    save(fig, "so_do_ket_noi_%s_truc.png" % ("1" if axis == "mot" else "2"))


# ------------------------------------------------------------------ 4) mô hình cơ khí
def ve_co_khi(axis="mot"):
    fig, ax = new_fig(11, 6.2, (0, 110), (0, 66))
    if axis == "mot":
        line(ax, 6, 8, 104, 8, 2.6)
        for x in range(8, 104, 6):
            line(ax, x, 8, x - 2.4, 5, 1.0)
        ax.add_patch(Rectangle((30, 8), 6, 20, fc=BLUE, ec=EDGE, lw=1.8))
        ax.add_patch(Rectangle((74, 8), 6, 20, fc=BLUE, ec=EDGE, lw=1.8))
        ax.add_patch(Circle((33, 30), 3.2, fc=WHITE, ec=EDGE, lw=1.8))
        ax.add_patch(Circle((77, 30), 3.2, fc=WHITE, ec=EDGE, lw=1.8))
        line(ax, 33, 30, 77, 30, 2.2)
        ang = math.radians(15)
        cx, cy = 55, 35
        L, T = 30, 2.2
        dx, dy = math.cos(ang) * L, math.sin(ang) * L
        pts = [(cx - dx, cy - dy), (cx + dx, cy + dy),
               (cx + dx - math.sin(ang) * T * 2, cy + dy + math.cos(ang) * T * 2),
               (cx - dx - math.sin(ang) * T * 2, cy - dy + math.cos(ang) * T * 2)]
        ax.add_patch(Polygon(pts, closed=True, fc=YELLOW, ec=EDGE, lw=2))
        ax.text(cx, 49, "Tấm pin quay quanh trục ngang Bắc – Nam", ha="center",
                va="center", color=TXT, fontsize=9.5, fontweight="bold")
        line(ax, 58, 31, 64, 16, 2.2)
        ax.add_patch(Rectangle((58, 10), 12, 6, fc=BLUE, ec=EDGE, lw=1.8))
        ax.text(64, 3.6, "Actuator / servo", ha="center", va="center", color=TXT, fontsize=8.5)
        ax.add_patch(Rectangle((12, 12), 5, 8, fc=GREEN, ec=EDGE, lw=1.6))
        ax.add_patch(Rectangle((93, 12), 5, 8, fc=GREEN, ec=EDGE, lw=1.6))
        ax.text(14.5, 23, "CTHT ĐÔNG", ha="center", va="center", color=TXT, fontsize=8)
        ax.text(95.5, 23, "CTHT TÂY", ha="center", va="center", color=TXT, fontsize=8)
        ax.annotate("", xy=(24, 47), xytext=(40, 53),
                    arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2,
                                    connectionstyle="arc3,rad=0.35"))
        ax.annotate("", xy=(86, 47), xytext=(70, 53),
                    arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2,
                                    connectionstyle="arc3,rad=-0.35"))
        ax.text(55, 59, "Quay Đông – Tây trong mặt phẳng vuông góc trục",
                ha="center", va="center", color=ACC, fontsize=9.5, fontweight="bold")
        ax.text(33, 22, "Gối đỡ", ha="center", va="center", color=TXT, fontsize=8)
    else:
        line(ax, 6, 6, 104, 6, 2.6)
        for x in range(8, 104, 6):
            line(ax, x, 6, x - 2.4, 3, 1.0)
        ax.add_patch(Rectangle((44, 6), 22, 8, fc=BLUE, ec=EDGE, lw=1.8))
        ax.text(55, 10, "Đế + servo phương vị", ha="center", va="center", color=TXT, fontsize=8.5)
        ax.add_patch(Rectangle((52, 14), 6, 16, fc=BLUE, ec=EDGE, lw=1.8))
        ax.add_patch(Circle((55, 32), 3.4, fc=WHITE, ec=EDGE, lw=1.8))
        ang = math.radians(22)
        cx, cy = 52, 41
        L, T = 28, 2.2
        dx, dy = math.cos(ang) * L, math.sin(ang) * L
        pts = [(cx - dx, cy - dy), (cx + dx, cy + dy),
               (cx + dx - math.sin(ang) * T * 2, cy + dy + math.cos(ang) * T * 2),
               (cx - dx - math.sin(ang) * T * 2, cy - dy + math.cos(ang) * T * 2)]
        ax.add_patch(Polygon(pts, closed=True, fc=YELLOW, ec=EDGE, lw=2))
        line(ax, 55, 34, 51, 39.5, 2.0)
        ax.text(60, 58, "Tấm pin (nghiêng + xoay)", ha="center", va="center",
                color=TXT, fontsize=9.5, fontweight="bold")
        ax.add_patch(Rectangle((74, 22.5), 12, 7, fc=BLUE, ec=EDGE, lw=1.8))
        line(ax, 80, 29.5, 70, 46, 2.0)
        ax.text(78, 18.5, "Motor nghiêng + encoder", ha="center", va="center", color=TXT, fontsize=8)
        ax.annotate("", xy=(30, 52), xytext=(44, 56),
                    arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2,
                                    connectionstyle="arc3,rad=0.35"))
        ax.text(24, 58, "Xoay phương vị", ha="center", va="center", color=ACC,
                fontsize=9, fontweight="bold")
        ax.annotate("", xy=(88, 44), xytext=(78, 48),
                    arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2,
                                    connectionstyle="arc3,rad=-0.3"))
        ax.text(95, 52, "Nâng / hạ\ngóc nghiêng", ha="center", va="center", color=ACC,
                fontsize=9, fontweight="bold")
        ax.add_patch(Rectangle((16, 10), 5, 7, fc=GREEN, ec=EDGE, lw=1.6))
        ax.add_patch(Rectangle((93, 10), 5, 7, fc=GREEN, ec=EDGE, lw=1.6))
        ax.text(18.5, 20, "CTHT\nphương vị", ha="center", va="center", color=TXT, fontsize=7.6)
        ax.text(95.5, 20, "CTHT\nnghiêng", ha="center", va="center", color=TXT, fontsize=7.6)
    title(ax, 55, 63, "MÔ HÌNH CƠ KHÍ ĐỀ XUẤT – HỆ %s TRỤC" % ("MỘT" if axis == "mot" else "HAI"))
    save(fig, "mo_hinh_co_khi_%s_truc.png" % ("1" if axis == "mot" else "2"))


# ------------------------------------------------------------------ 5) sơ đồ khối chương trình
def ve_khoi_chuong_trinh():
    fig, ax = new_fig(11.5, 4.8, (0, 115), (0, 46))
    steps = [("Đọc 4 kênh ADC\n(LDR)", 12), ("Loại mẫu đột biến,\nlọc thông thấp", 30),
             ("Bù offset/độ lợi;\ntính S, e_quay,\ne_nghiêng", 49),
             ("Đánh giá chất\nlượng ánh sáng", 68), ("Chọn trục và\nluật phát lệnh", 87),
             ("Giới hạn góc,\nliên động CTHT", 104)]
    for t, x in steps:
        box(ax, x, 30, 15.5, 14, t, "proc", fs=8.2, wrap=16)
    for i in range(len(steps) - 1):
        arrow(ax, steps[i][1] + 7.8, 30, steps[i + 1][1] - 7.8, 30)
    box(ax, 62, 11, 30, 8, "Ghi log / Serial: tín hiệu, góc đặt, trạng thái, U–I", "io", fs=8.4, wrap=40)
    arrow(ax, 104, 23, 104, 11)
    line(ax, 104, 11, 77, 11)
    arrow(ax, 87, 23, 87, 15)
    line(ax, 12, 11, 12, 23)
    line(ax, 12, 11, 47, 11)
    note(ax, 26, 6, "Vòng lặp chu kỳ T_mẫu")
    title(ax, 57, 42, "SƠ ĐỒ KHỐI CHỨC NĂNG CỦA CHƯƠNG TRÌNH ĐIỀU KHIỂN")
    save(fig, "so_do_khoi_chuong_trinh.png")


# ------------------------------------------------------------------ 6) lưu đồ 1 trục (thuật toán lai)
def ve_luu_do_1_truc():
    fig, ax = new_fig(10.5, 12.5, (0, 104), (0, 142))
    title(ax, 50, 138, "LƯU ĐỒ THUẬT TOÁN LAI THIÊN VĂN – CẢM BIẾN (1 TRỤC)", 13)
    box(ax, 40, 130, 26, 7, "BẮT ĐẦU", "start", 10, bold=True)
    box(ax, 40, 118, 46, 10,
        "Khởi tạo ESP32, ADC, RTC, PWM; nạp tham số: vùng chết δ, giới hạn góc, hệ số K_a, chu kỳ.",
        "proc", 8.6)
    box(ax, 40, 103, 46, 9,
        "Đọc RTC; tính góc tham chiếu thiên văn R* theo ngày, giờ, vĩ độ – kinh độ.",
        "io", 8.6)
    box(ax, 40, 88, 46, 10,
        "Đọc 4 LDR; lọc mẫu; tính S, e_quay, e_nghiêng, e_chéo.", "io", 8.6)
    box(ax, 40, 70, 46, 13,
        "TÍN HIỆU ĐỦ TIN CẬY?\nS trong dải làm việc, biến động thấp,\nkhông bão hòa, e_chéo hợp lý",
        "dec", 8.3, wrap=40)
    box(ax, 40, 53, 46, 11,
        "e_a = e_quay (trục được lắp);\nf = sign(e_a)·(|e_a| − δ) ngoài vùng chết;\nθ* = sat(R* + K_a·f, θ_min, θ_max)",
        "proc", 8.2, wrap=40)
    box(ax, 82, 53, 28, 10,
        "Chế độ thiên văn: θ* = R* (giới hạn trong hành trình), không dùng hiệu chỉnh LDR.",
        "proc", 8.3, wrap=24)
    box(ax, 40, 34, 40, 10,
        "KIỂM TRA GIỚI HẠN?\nCông tắc hành trình không chặn\nhướng đang lệnh", "dec", 8.3, wrap=34)
    box(ax, 82, 26, 28, 10,
        "Chặn lệnh hướng đang bị chặn; chỉ cho phép quay ngược để thoát.", "proc", 8.4, wrap=24)
    box(ax, 40, 19, 40, 8,
        "Phát lệnh PWM/servo; ghi log S, e, góc đặt, trạng thái.", "proc", 8.5)
    box(ax, 40, 7, 40, 7, "Chờ hết chu kỳ T_mẫu rồi lặp lại.", "io", 8.6)
    arrow(ax, 40, 126.5, 40, 123)
    arrow(ax, 40, 113, 40, 107.5)
    arrow(ax, 40, 98.5, 40, 93)
    arrow(ax, 40, 83, 40, 76.5)
    arrow(ax, 40, 63.5, 40, 58.5, label="CÓ", lx=45, ly=61)
    arrow(ax, 63, 70, 69, 58, label="KHÔNG", lx=70, ly=66)
    # hai chế độ gộp lại trước khi kiểm tra giới hạn
    arrow(ax, 40, 47.5, 40, 44.6)
    line(ax, 82, 48, 82, 44)
    line(ax, 82, 44, 40, 44)
    arrow(ax, 40, 44, 40, 39.2)
    arrow(ax, 40, 29, 40, 23, label="CÓ", lx=45, ly=26)
    arrow(ax, 60, 34, 69, 29, label="KHÔNG", lx=68, ly=33)
    arrow(ax, 40, 15, 40, 10.5)
    # nhánh chặn lệnh gom về ô chờ cuối chu kỳ
    line(ax, 82, 21, 82, 7)
    line(ax, 82, 7, 60, 7)
    # rail trái quay về khối đọc LDR
    line(ax, 20, 7, 6, 7)
    line(ax, 6, 7, 6, 88)
    arrow(ax, 6, 88, 17, 88)
    note(ax, 9, 12, "Lặp lại mỗi chu kỳ", ha="left")
    note(ax, 96, 70, "Sau mỗi bước:\nđọc lại cảm biến", ha="right")
    save(fig, "luu_do_thuat_toan_1_truc.png")


if __name__ == "__main__":
    ve_bo_tri_ldr()
    ve_so_do_khoi("mot")
    ve_so_do_khoi("hai")
    ve_ket_noi("mot")
    ve_ket_noi("hai")
    ve_co_khi("mot")
    ve_co_khi("hai")
    ve_khoi_chuong_trinh()
    ve_luu_do_1_truc()
