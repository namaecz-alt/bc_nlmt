# -*- coding: utf-8 -*-
"""Ve so do / hinh minh hoa cho bao cao (ban dung ESP32 + dong co gat mua).

Chay:  python3 tools/ve_hinh.py
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
    return "\n".join("\n".join(textwrap.wrap(ln, w)) if ln.strip() else ""
                     for ln in t.split("\n"))


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
    ax.text(x, y, text, ha="center", va="center", color=TXT, fontsize=fs, fontweight="bold")


def note(ax, x, y, text, fs=8.5, ha="center"):
    ax.text(x, y, text, ha=ha, va="center", color=ACC, fontsize=fs, fontweight="bold")


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    fig.savefig(p, facecolor=BG, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("đã vẽ:", p)


# ------------------------------------------------------------------ bo tri 4 LDR
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
    a2.text(63, 38, "β_s", ha="center", va="center", color=TXT, fontsize=10, fontweight="bold")
    a2.text(50, -4, "Mặt cắt: góc gá β_s giữa pháp tuyến và trục cảm quang",
            ha="center", va="center", color=TXT, fontsize=9)
    fig.tight_layout()
    save(fig, "bo_tri_4_ldr.png")


# ------------------------------------------------------------------ so do khoi
def ve_so_do_khoi(axis="mot"):
    fig, ax = new_fig(11, 6.6, (0, 110), (0, 72))
    if axis == "mot":
        act = "Motor gạt nước trục vít\n(tự giữ khi mất điện)\n+ hồi tiếp biến trở"
        mid = "Ma trận 4 LDR:\ntính S, e_quay →\nΔ_quay = atan(e/tan β_s)"
        fb = "Biến trở xoay hồi tiếp\ngóc trục"
    else:
        act = "2 motor gạt nước trục vít\n(phương vị + nghiêng)\n+ 2 biến trở hồi tiếp"
        mid = "Ma trận 4 LDR:\ne_quay, e_nghiêng →\nΔ_quay, Δ_nghiêng"
        fb = "2 biến trở hồi tiếp\ngóc hai trục"
    box(ax, 14, 60, 22, 10, "Cụm 4 LDR\n(4 góc tấm pin)", "io")
    box(ax, 14, 46, 22, 9, "Mạch chia áp\n(sinh viên tự chế)", "proc", fs=8.4, wrap=22)
    box(ax, 14, 32, 22, 9, "ADS1115 đo U, I\n(I²C, 16 bit)", "io", fs=8.6)
    box(ax, 14, 18, 22, 9, "RTC DS3231\n(I²C, ghi nhãn log)", "io", fs=8.4, wrap=22)
    box(ax, 50, 52, 27, 12, mid, "proc", fs=8.6)
    box(ax, 50, 32, 27, 12, "ESP32\nADC 12 bit, lọc trung vị,\ntính góc đích, liên động", "proc", fs=9.0, wrap=26)
    box(ax, 50, 13, 27, 9, "Ghi log Serial:\n4 kênh, e, Δ, góc đích, U–I", "io", fs=8.4, wrap=26)
    box(ax, 88, 46, 18, 14, act, "proc", fs=8.2, wrap=20)
    box(ax, 88, 22, 18, 10, "Tấm pin\nmặt trời", "term", fs=9.5, wrap=16)
    box(ax, 88, 64, 18, 8, fb, "io", fs=8.0, wrap=20)
    arrow(ax, 14, 55, 14, 50.5)
    arrow(ax, 25, 46, 36.5, 50, rad=-0.2)
    arrow(ax, 25, 32, 36.5, 33, rad=0.1)
    arrow(ax, 25, 18, 36.5, 29, rad=0.2)
    arrow(ax, 50, 46, 50, 38)
    arrow(ax, 63.5, 32, 79, 42, rad=-0.2)
    arrow(ax, 88, 39, 88, 27)
    arrow(ax, 88, 60, 88, 53)
    arrow(ax, 79, 64, 63.5, 56, rad=-0.2)
    arrow(ax, 79, 20, 63.5, 15, rad=-0.2)
    note(ax, 71, 68, "Hồi tiếp góc thực tế")
    note(ax, 71, 24, "Trục vít tự hãm: giữ nguyên vị trí khi dừng/mất điện")
    title(ax, 55, 70.5, "SƠ ĐỒ KHỐI HỆ THỐNG BÁM NẮNG %s TRỤC (ESP32)" % ("MỘT" if axis == "mot" else "HAI"))
    save(fig, "so_do_khoi_%s_truc.png" % ("1" if axis == "mot" else "2"))


# ------------------------------------------------------------------ so do ket noi ESP32
def ve_ket_noi(axis="mot"):
    fig, ax = new_fig(11.5, 6.8, (0, 115), (0, 74))
    if axis == "mot":
        left = [("Cụm 4 LDR (ma trận 4 góc)", "GPIO36/39/34/35 (ADC1)"),
                ("Biến trở hồi tiếp góc trục", "GPIO32 (ADC1_CH4)"),
                ("ADS1115 đo U, I pin", "GPIO21 (SDA) – GPIO22 (SCL)"),
                ("RTC DS3231", "GPIO21 (SDA) – GPIO22 (SCL)"),
                ("Công tắc hành trình Đ/T", "GPIO4 – GPIO5 (pull-up)")]
        right = [("Relay/cầu H motor gạt nước", "GPIO26 (chiều A) – GPIO27 (B)"),
                 ("Nút dừng khẩn cấp", "GPIO18 (INPUT_PULLUP)"),
                 ("Đèn báo trạng thái", "GPIO2 (OUTPUT)"),
                 ("Serial Monitor / ghi log", "USB-UART (GPIO1/3)"),
                 ("Nguồn logic 5 V / tải 12 V", "Tách khối, chung mass")]
    else:
        left = [("Cụm 4 LDR (ma trận 4 góc)", "GPIO36/39/34/35 (ADC1)"),
                ("Biến trở hồi tiếp phương vị", "GPIO32 (ADC1_CH4)"),
                ("Biến trở hồi tiếp nghiêng", "GPIO33 (ADC1_CH5)"),
                ("ADS1115 đo U, I pin", "GPIO21 (SDA) – GPIO22 (SCL)"),
                ("RTC DS3231", "GPIO21 (SDA) – GPIO22 (SCL)")]
        right = [("Relay/cầu H motor phương vị", "GPIO26 – GPIO27"),
                 ("Relay/cầu H motor nghiêng", "GPIO14 – GPIO13"),
                 ("Công tắc hành trình 4 đầu", "GPIO4 – 5 – 18 – 19"),
                 ("Nút dừng khẩn cấp", "GPIO25 (INPUT_PULLUP)"),
                 ("Serial Monitor / ghi log", "USB-UART (GPIO1/3)")]
    box(ax, 57, 37, 34, 46, "", "proc")
    ax.text(57, 57, "ESP32 DEV KIT", ha="center", va="center", color=TXT,
            fontsize=11.5, fontweight="bold")
    ax.text(57, 52.8, "Vi điều khiển duy nhất của mạch", ha="center", va="center",
            color=ACC, fontsize=8.5)
    y0 = 46.5
    for i, (name, pin) in enumerate(left):
        y = y0 - i * 7.6
        box(ax, 15, y, 26, 6, name, "io", fs=8.2, wrap=28)
        line(ax, 28, y, 40, y)
        ax.add_patch(Circle((40, y), 0.7, fc=EDGE, ec=EDGE))
        ax.text(56.4, y, pin, ha="right", va="center", color=TXT, fontsize=7.2)
    for i, (name, pin) in enumerate(right):
        y = y0 - i * 7.6
        box(ax, 98, y, 28, 6, name, "io", fs=8.2, wrap=28)
        line(ax, 74, y, 84, y)
        ax.add_patch(Circle((74, y), 0.7, fc=EDGE, ec=EDGE))
        ax.text(57.6, y, pin, ha="left", va="center", color=TXT, fontsize=7.2)
    title(ax, 57, 68, "SƠ ĐỒ KẾT NỐI ESP32 – HỆ %s TRỤC" % ("MỘT" if axis == "mot" else "HAI"))
    note(ax, 57, 3, "Không dùng bo Arduino trong mạch; mạch chia áp LDR do sinh viên tự chế và hiệu chuẩn.")
    save(fig, "so_do_ket_noi_%s_truc.png" % ("1" if axis == "mot" else "2"))


# ------------------------------------------------------------------ mo hinh co khi
def ve_co_khi(axis="mot"):
    fig, ax = new_fig(11, 6.4, (0, 110), (0, 68))
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
        ax.add_patch(Rectangle((58, 10), 14, 6, fc=BLUE, ec=EDGE, lw=1.8))
        ax.text(65, 3.6, "Motor gạt nước ô tô (trục vít tự hãm)", ha="center",
                va="center", color=TXT, fontsize=8.3)
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
        ax.text(55, 60, "Quay Đông – Tây theo góc suy ra từ ma trận LDR",
                ha="center", va="center", color=ACC, fontsize=9.5, fontweight="bold")
        ax.text(33, 22, "Gối đỡ", ha="center", va="center", color=TXT, fontsize=8)
        ax.text(88, 16, "Biến trở hồi tiếp", ha="center", va="center", color=TXT, fontsize=8)
        ax.add_patch(Rectangle((84, 10), 8, 4, fc=WHITE, ec=EDGE, lw=1.4))
    else:
        line(ax, 6, 6, 104, 6, 2.6)
        for x in range(8, 104, 6):
            line(ax, x, 6, x - 2.4, 3, 1.0)
        ax.add_patch(Rectangle((44, 6), 22, 8, fc=BLUE, ec=EDGE, lw=1.8))
        ax.text(55, 10, "Đế + motor gạt nước phương vị", ha="center", va="center",
                color=TXT, fontsize=8.3)
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
        ax.add_patch(Rectangle((74, 22.5), 14, 7, fc=BLUE, ec=EDGE, lw=1.8))
        line(ax, 80, 29.5, 70, 46, 2.0)
        ax.text(79, 18.5, "Motor gạt nước nghiêng", ha="center", va="center", color=TXT, fontsize=8)
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
        ax.text(30, 12, "2 biến trở hồi tiếp góc", ha="center", va="center", color=TXT, fontsize=8)
    title(ax, 55, 65, "MÔ HÌNH CƠ KHÍ HỆ %s TRỤC – ĐỘNG CƠ GẠT NƯỚC TRỤC VÍT" % ("MỘT" if axis == "mot" else "HAI"))
    save(fig, "mo_hinh_co_khi_%s_truc.png" % ("1" if axis == "mot" else "2"))


# ------------------------------------------------------------------ khoi chuong trinh
def ve_khoi_chuong_trinh():
    fig, ax = new_fig(11.5, 5.0, (0, 115), (0, 48))
    steps = [("Đọc 4 kênh ADC\n(64 mẫu, trung vị)", 12),
             ("Ma trận LDR:\nS, e_quay, e_nghiêng", 30),
             ("Δ = atan(e/tan β_s)\nsuy ra góc cần quay", 49),
             ("|Δ| > ngưỡng δ?\nso sánh giá trị", 68),
             ("Đọc biến trở →\nθ đích = θ + Δ", 87),
             ("Chạy motor tới\nθ đích, liên động", 104)]
    for t, x in steps:
        box(ax, x, 31, 15.5, 14, t, "proc", fs=8.2, wrap=17)
    for i in range(len(steps) - 1):
        arrow(ax, steps[i][1] + 7.8, 31, steps[i + 1][1] - 7.8, 31)
    box(ax, 62, 12, 30, 8, "Ghi log Serial: 4 kênh, e, Δ, θ đích, U–I", "io", fs=8.4, wrap=40)
    arrow(ax, 104, 24, 104, 12)
    line(ax, 104, 12, 77, 12)
    arrow(ax, 87, 24, 87, 16)
    line(ax, 12, 12, 12, 24)
    line(ax, 12, 12, 47, 12)
    note(ax, 26, 6, "Vòng lặp chu kỳ T_mẫu; motor trục vít tự giữ khi dừng")
    note(ax, 68, 41, "KHÔNG: chờ chu kỳ sau, không quay theo thời gian")
    title(ax, 57, 45, "SƠ ĐỒ KHỐI CHƯƠNG TRÌNH ĐỌC MA TRẬN LDR VÀ SUY RA GÓC QUAY")
    save(fig, "so_do_khoi_chuong_trinh.png")


# ------------------------------------------------------------------ luu do ma tran
def ve_luu_do_ma_tran(axis="mot"):
    fig, ax = new_fig(10.5, 12.8, (0, 104), (0, 146))
    ten = "MỘT TRỤC" if axis == "mot" else "HAI TRỤC"
    title(ax, 50, 142, "LƯU ĐỒ PHƯƠNG PHÁP MA TRẬN 4 LDR SUY RA GÓC QUAY (%s)" % ten, 12.5)
    box(ax, 40, 134, 26, 7, "BẮT ĐẦU", "start", 10, bold=True)
    box(ax, 40, 122, 46, 10,
        "Khởi tạo ESP32: ADC 12 bit + attenuation, chân relay, I²C; nạp β_s, ngưỡng δ, giới hạn góc, hệ số hiệu chuẩn 4 kênh.",
        "proc", 8.5)
    box(ax, 40, 107, 46, 10,
        "Đọc 4 kênh LDR: 64 mẫu/kênh, lấy trung vị rồi trung bình; đọc ADS1115 (U, I) và RTC.",
        "io", 8.6)
    box(ax, 40, 92, 46, 11,
        "Lập ma trận: S = tổng 4 kênh; e_quay = (phải − trái)/S; e_nghiêng = (trên − dưới)/S.",
        "proc", 8.6)
    box(ax, 40, 74, 46, 12,
        "TÍN HIỆU DÙNG ĐƯỢC?\nS trong dải, không bão hòa,\nbiến động thấp", "dec", 8.4, wrap=34)
    box(ax, 82, 92, 28, 10,
        "Giữ nguyên góc hiện tại (motor trục vít tự giữ); ghi log cảnh báo.", "proc", 8.4, wrap=24)
    box(ax, 40, 56, 46, 11,
        "Suy ra góc cần quay:\nΔ_quay = atan(e_quay / tan β_s);\nΔ_nghiêng = atan(e_nghiêng / tan β_s).",
        "proc", 8.4, wrap=40)
    box(ax, 40, 39, 40, 9,
        "|Δ| > NGƯỠNG δ?\n(so sánh với vùng chết)", "dec", 8.4, wrap=30)
    box(ax, 82, 56, 28, 9,
        "Chờ hết chu kỳ T_mẫu rồi đọc lại ma trận.", "io", 8.5, wrap=24)
    box(ax, 40, 24, 40, 9,
        "Đọc biến trở hồi tiếp: θ_hiện tại;\nθ_đích = sat(θ + Δ, θ_min, θ_max).", "proc", 8.4, wrap=36)
    box(ax, 40, 10, 40, 9,
        "KIỂM TRA CÔNG TẮC HÀNH TRÌNH;\nchạy motor đúng chiều đến khi θ = θ_đích thì dừng.",
        "proc", 8.3, wrap=36)
    box(ax, 40, -2, 40, 6, "Ghi log; chờ T_mẫu; lặp lại.", "io", 8.5)
    arrow(ax, 40, 130.5, 40, 127)
    arrow(ax, 40, 117, 40, 112)
    arrow(ax, 40, 102, 40, 97.5)
    arrow(ax, 40, 86.5, 40, 80)
    arrow(ax, 63, 74, 69, 87, label="KHÔNG", lx=70, ly=82)
    arrow(ax, 40, 68, 40, 61.5, label="CÓ", lx=45, ly=65)
    arrow(ax, 40, 50.5, 40, 43.5)
    arrow(ax, 60, 39, 69, 52, label="KHÔNG", lx=68, ly=47)
    arrow(ax, 40, 34.5, 40, 28.5, label="CÓ", lx=45, ly=31.5)
    arrow(ax, 40, 19.5, 40, 14.5)
    arrow(ax, 40, 5.5, 40, 1)
    line(ax, 82, 87, 82, 83)
    line(ax, 82, 83, 99, 83)
    line(ax, 82, 51.5, 82, 47)
    line(ax, 82, 47, 99, 47)
    line(ax, 99, 83, 99, -2)
    line(ax, 99, -2, 60, -2)
    line(ax, 20, -2, 6, -2)
    line(ax, 6, -2, 6, 107)
    arrow(ax, 6, 107, 17, 107)
    note(ax, 9, 2, "Lặp lại mỗi chu kỳ", ha="left")
    if axis == "hai":
        note(ax, 50, -8, "Trục nghiêng chỉnh trước, đến phiên xoay: lặp lại cùng quy tắc với e_quay.")
    save(fig, "luu_do_ma_tran_%s_truc.png" % ("1" if axis == "mot" else "2"))


if __name__ == "__main__":
    ve_bo_tri_ldr()
    ve_so_do_khoi("mot")
    ve_so_do_khoi("hai")
    ve_ket_noi("mot")
    ve_ket_noi("hai")
    ve_co_khi("mot")
    ve_co_khi("hai")
    ve_khoi_chuong_trinh()
    ve_luu_do_ma_tran("mot")
    ve_luu_do_ma_tran("hai")
