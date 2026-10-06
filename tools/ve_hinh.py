# -*- coding: utf-8 -*-
"""Ve so do / luu do theo phong cach ban ve ky thuat: nen trang, net manh,
chu den, it mau - dung cho 6 quyen bao cao phuong phap hybrid.

Chay:  python3 tools/ve_hinh.py
"""
import math
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hinh_ve")
EDGE = "#222222"
FILL = "#ffffff"
FILL2 = "#f2f2f2"
TXT = "#111111"


def _w(t, n=30):
    out = []
    for ln in t.split("\n"):
        out.extend(textwrap.wrap(ln, n) if ln.strip() else [""])
    return "\n".join(out)


def new_fig(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, cx, cy, w, h, text, fs=8.0, fill=FILL, wrap=28, round_=False):
    if round_:
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                    boxstyle="round,pad=0,rounding_size=1.6",
                                    fc=fill, ec=EDGE, lw=0.9))
    else:
        ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, fc=fill, ec=EDGE, lw=0.9))
    ax.text(cx, cy, _w(text, wrap), ha="center", va="center", color=TXT,
            fontsize=fs, linespacing=1.3)


def dec(ax, cx, cy, w, h, text, fs=7.6, wrap=24):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2),
                          (cx - w / 2, cy)], closed=True, fc=FILL, ec=EDGE, lw=0.9))
    ax.text(cx, cy, _w(text, wrap), ha="center", va="center", color=TXT,
            fontsize=fs, linespacing=1.25)


def arr(ax, x1, y1, x2, y2, label=None, lx=None, ly=None, fs=7.4):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=0.9, shrinkA=0, shrinkB=0))
    if label:
        ax.text(lx if lx is not None else (x1 + x2) / 2 + 1.2,
                ly if ly is not None else (y1 + y2) / 2, label,
                ha="left", va="center", color=TXT, fontsize=fs)


def line(ax, x1, y1, x2, y2, lw=0.9):
    ax.plot([x1, x2], [y1, y2], color=EDGE, lw=lw)


def title(ax, x, y, text, fs=10.5):
    ax.text(x, y, text, ha="center", va="center", color=TXT, fontsize=fs, fontweight="bold")


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    fig.savefig(p, facecolor="white", bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    print("da ve:", name)


# ------------------------------------------------------------------ so do khoi
def so_do_khoi(truc=1):
    hai = (truc == 2)
    fig, ax = new_fig(10.6, 6.6, (0, 106), (0, 66))
    box(ax, 16, 54, 26, 9, "Cụm 4 LDR + mạch chia áp\n(4 kênh 0–3,3 V)", fs=7.8, wrap=26)
    box(ax, 16, 41, 26, 8, "Biến trở chia áp\nhồi tiếp góc tấm pin" + ("" if not hai else " (2 cái)"), fs=7.8, wrap=26)
    box(ax, 16, 28, 26, 8, "Module RTC DS1307\n(bus I²C)", fs=7.8, wrap=26)
    box(ax, 16, 15, 26, 8, "Công tắc hành trình\n+ nút dừng khẩn cấp", fs=7.8, wrap=26)
    box(ax, 52, 40, 26, 16, "ESP32 DevKit\nđọc ADC, tính thiên văn,\nso sánh e1/e2, phát lệnh,\nhiển thị LCD", fs=8.2, wrap=24)
    box(ax, 52, 18, 26, 9, "LCD I2C 1602\nhiển thị giờ, góc, trạng thái", fs=7.8, wrap=26)
    nb = 2 if hai else 1
    for i in range(nb):
        y = 46 - i * 16
        box(ax, 86, y, 24, 10, "Mạch cầu H 4 TIP41C\n(mạch động lực %d)" % (i + 1), fs=7.8, wrap=24)
        box(ax, 86, y - 13, 24, 8, "Motor gạt nước 12 V\ntrục vít tự hãm", fs=7.8, wrap=24)
        arr(ax, 86, y - 5, 86, y - 9)
        arr(ax, 65, 40, 74, y)
    arr(ax, 29, 54, 39, 45)
    arr(ax, 29, 41, 39, 41)
    arr(ax, 29, 28, 39, 36)
    arr(ax, 29, 15, 39, 33)
    arr(ax, 52, 32, 52, 22.5)
    box(ax, 52, 6, 40, 6, "Nguồn 12 V (ắc quy) → mạch động lực;  mạch ổn áp 5 V/3,3 V → ESP32, LCD", fs=7.6, wrap=60)
    ax.text(97, 60, "Trục vít tự hãm:\ngiữ vị trí khi ngắt điện", fontsize=7.6, color=TXT,
            ha="left", va="center")
    title(ax, 53, 64, "SƠ ĐỒ KHỐI HỆ THỐNG BÁM NẮNG %s TRỤC – PHƯƠNG PHÁP HYBRID"
          % ("MỘT" if not hai else "HAI"))
    save(fig, "so_do_khoi_%d_truc.png" % truc)


# ------------------------------------------------------------------ so do ket noi
def so_do_ket_noi(truc=1):
    hai = (truc == 2)
    fig, ax = new_fig(11.0, 6.2, (0, 110), (0, 62))
    box(ax, 55, 31, 30, 44, "", fill=FILL2)
    ax.text(55, 50, "ESP32 DEVKIT", ha="center", va="center", fontsize=10, fontweight="bold", color=TXT)
    left = [("4 kênh LDR (chia áp)", "GPIO36 / 39 / 34 / 35"),
            ("Biến trở góc quay", "GPIO32 (ADC)")]
    if hai:
        left.append(("Biến trở góc nghiêng", "GPIO33 (ADC)"))
    left += [("RTC DS1307 (I²C)", "GPIO21 SDA / GPIO22 SCL"),
             ("LCD I2C 1602 (I²C)", "chung bus 21 / 22")]
    right = [("Cầu H 1: IN1, IN2", "GPIO26 / GPIO27")]
    if hai:
        right.append(("Cầu H 2: IN3, IN4", "GPIO14 / GPIO13"))
    right += [("CT hành trình", "GPIO4 / GPIO5" + (" / 18 / 19" if hai else "")),
              ("Nút dừng khẩn cấp", "GPIO18" if not hai else "GPIO25")]
    y = 44
    for name, pin in left:
        box(ax, 16, y, 26, 6, name, fs=7.6, wrap=26)
        line(ax, 29, y, 40, y)
        ax.text(41, y, pin, fontsize=6.9, ha="left", va="center", color=TXT)
        y -= 7.4
    y = 44
    for name, pin in right:
        box(ax, 94, y, 26, 6, name, fs=7.6, wrap=26)
        line(ax, 70, y, 81, y)
        ax.text(69, y, pin, fontsize=6.9, ha="right", va="center", color=TXT)
        y -= 7.4
    title(ax, 55, 58, "SƠ ĐỒ KẾT NỐI ESP32 DEVKIT – HỆ %s TRỤC" % ("MỘT" if not hai else "HAI"))
    ax.text(55, 2, "ADC của ESP32 chỉ đo điện áp (0–3,3 V): 4 kênh LDR và biến trở hồi tiếp; "
                   "không đo dòng điện trong thiết kế này.", fontsize=7.6, ha="center", color=TXT)
    save(fig, "so_do_ket_noi_%d_truc.png" % truc)


# ------------------------------------------------------------------ 3 phuong phap
def so_do_3_phuong_phap():
    fig, ax = new_fig(10.6, 7.4, (0, 106), (0, 74))
    rows = [("a) Nhóm 1 – Vòng hở theo thời gian (thiên văn)", 60,
             [("RTC DS1307\nđọc ngày, giờ", 14), ("Tính δ, H, α, γ\ntheo công thức", 36),
              ("Đổi ra góc đặt\ncủa tấm pin", 58), ("Cầu H chạy motor\ntới góc đặt", 80)], None),
            ("b) Nhóm 2 – Vòng kín cảm biến LDR", 38,
             [("4 LDR gá nghiêng β_s\nđọc 4 mức sáng", 14), ("e1 = trái − phải\ne2 = trên − dưới", 36),
              ("|e| > ngưỡng?\nso dấu, vùng chết", 58), ("Cầu H quay đúng chiều\nđến khi cân bằng", 80)],
             "tấm pin gắn cụm LDR"),
            ("c) Nhóm 3 – HYBRID (đề tài chọn)", 14,
             [("RTC + công thức\nthiên văn: định vị thô", 14), ("4 LDR: tinh chỉnh\nquanh vị trí cân bằng", 38),
              ("Trời mây mù?\ngiữ vị trí theo lịch", 62), ("Cầu H chạy motor\ntheo lệnh tổng hợp", 84)], None)]
    for t, y0, cells, note in rows:
        ax.text(2, y0 + 8.5, t, fontsize=8.6, fontweight="bold", color=TXT, va="center")
        xs = [c[1] for c in cells]
        for i, (txt, x) in enumerate(cells):
            box(ax, x, y0, 20, 10, txt, fs=7.4, wrap=20)
            if i:
                arr(ax, xs[i - 1] + 10, y0, x - 10, y0)
        if note:
            line(ax, 80, y0 - 5, 80, y0 - 8)
            line(ax, 80, y0 - 8, 14, y0 - 8)
            arr(ax, 14, y0 - 8, 14, y0 - 5)
            ax.text(48, y0 - 10, note + " (hồi tiếp quang)", fontsize=7.2, ha="center", color=TXT)
    title(ax, 53, 72, "BA NHÓM PHƯƠNG PHÁP BÁM NẮNG XEM XÉT TRONG ĐỀ TÀI")
    save(fig, "so_do_3_phuong_phap.png")


# ------------------------------------------------------------------ bo tri LDR + vach che
def bo_tri_ldr():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.8), dpi=200,
                                 gridspec_kw={"width_ratios": [1.1, 1]})
    fig.patch.set_facecolor("white")
    for a in (a1, a2):
        a.set_facecolor("white")
        a.axis("off")
        a.set_aspect("equal")
    a1.set_xlim(-6, 106)
    a1.set_ylim(-12, 76)
    a1.add_patch(Rectangle((10, 8), 80, 54, fc="white", ec=EDGE, lw=1.2))
    pos = {"LDR trái trên": (20, 52, -1, 1), "LDR phải trên": (80, 52, 1, 1),
           "LDR trái dưới": (20, 18, -1, -1), "LDR phải dưới": (80, 18, 1, -1)}
    for k, (x, y, dx, dy) in pos.items():
        a1.add_patch(plt.Circle((x, y), 4.0, fc="white", ec=EDGE, lw=1.1))
        a1.annotate("", xy=(x + dx * 10, y + dy * 8), xytext=(x, y),
                    arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=0.9))
        a1.text(x - dx * 1, y - dy * 9.5, k, ha="center", va="center",
                fontsize=7.4, color=TXT)
    a1.text(50, 35, "tấm pin\n(nhìn thẳng)", ha="center", va="center",
            fontsize=8, color="#555555")
    a1.text(50, 68, "mũi tên: hướng trục cảm quang nghiêng ra ngoài tâm",
            ha="center", va="center", fontsize=7.6, color=TXT)
    a1.text(50, -6, "Bốn LDR ở bốn góc, chỉ gá nghiêng quang trở, không dùng vách ngăn",
            ha="center", va="center", fontsize=8, color=TXT)
    a2.set_xlim(-6, 106)
    a2.set_ylim(-14, 72)
    line(a2, 10, 18, 90, 18, 1.4)
    a2.text(50, 13.5, "mặt tấm pin", ha="center", fontsize=8, color=TXT)
    line(a2, 50, 18, 50, 58)
    a2.text(51.5, 60, "pháp tuyến", fontsize=8, color=TXT, ha="left")
    for sx, dx, lab in ((26, -1, "LDR trái"), (74, 1, "LDR phải")):
        a2.add_patch(plt.Circle((sx, 21), 3.2, fc="white", ec=EDGE, lw=1.1))
        a2.annotate("", xy=(sx + dx * 14, 21 + 22), xytext=(sx, 21),
                    arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=1.0))
        a2.text(sx + dx * 17, 46, lab, fontsize=7.6, ha="center", color=TXT)
    th = [50 + 15 * math.cos(math.radians(t)) for t in range(62, 91)]
    thy = [18 + 15 * math.sin(math.radians(t)) for t in range(62, 91)]
    a2.plot(th, thy, color=EDGE, lw=0.9)
    a2.text(38, 35, "β_s", fontsize=9, color=TXT)
    th2 = [50 - 15 * math.cos(math.radians(t)) for t in range(62, 91)]
    a2.plot(th2, thy, color=EDGE, lw=0.9)
    a2.text(59, 35, "β_s", fontsize=9, color=TXT)
    a2.text(50, -8, "Mặt cắt: trục cảm quang mỗi LDR nghiêng góc β_s so với pháp tuyến",
            ha="center", fontsize=8, color=TXT)
    fig.tight_layout()
    p = os.path.join(OUT, "bo_tri_4_ldr.png")
    fig.savefig(p, facecolor="white", bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    print("da ve: bo_tri_4_ldr.png")


# ------------------------------------------------------------------ luu do
def luu_do_tong_quat(truc=1):
    hai = (truc == 2)
    fig, ax = new_fig(9.6, 13.6, (0, 96), (0, 136))
    title(ax, 48, 133, "LƯU ĐỒ TỔNG QUÁT CHƯƠNG TRÌNH HYBRID – HỆ %s TRỤC"
          % ("MỘT" if not hai else "HAI"), 10)
    box(ax, 40, 126, 22, 5, "BẮT ĐẦU", fs=8.4, round_=True)
    box(ax, 40, 116, 44, 8, "Khởi tạo: ADC 12 bit; I²C (DS1307, LCD); chân cầu H;\nđọc hệ số hiệu chuẩn; đọc giờ DS1307", fs=7.4, wrap=44)
    box(ax, 40, 104, 40, 7, "Đọc giờ, ngày từ DS1307 → tính δ, H, α, γ", fs=7.6, wrap=40)
    dec(ax, 40, 92, 40, 10, "Đến chu kỳ định vị thô\n(30 phút)?", fs=7.6)
    box(ax, 78, 92, 26, 8, "So góc thiên văn với góc tấm pin:\nlệch > 2° thì chạy motor tới góc đặt", fs=7.2, wrap=26)
    box(ax, 40, 78, 40, 8, "Đọc 4 kênh ADC → tính S, e1" + (", e2" if hai else ""), fs=7.6, wrap=40)
    dec(ax, 40, 66, 38, 9, "Nắng đủ mạnh?\n(S > S_min)", fs=7.6)
    box(ax, 78, 66, 26, 7, "Trời mây mù:\ngiữ nguyên vị trí theo lịch", fs=7.4, wrap=26)
    dec(ax, 40, 53, 38, 9, "|e1| > ngưỡng?", fs=7.6)
    box(ax, 78, 53, 26, 7, "Chạy motor trục quay\ntheo dấu e1 (cầu H)", fs=7.4, wrap=26)
    if hai:
        dec(ax, 40, 40, 38, 9, "|e2| > ngưỡng?", fs=7.6)
        box(ax, 78, 40, 26, 7, "Chạy motor trục nghiêng\ntheo dấu e2 (cầu H)", fs=7.4, wrap=26)
        y_lcd = 27
    else:
        y_lcd = 33
    box(ax, 40, y_lcd, 40, 7, "Đọc biến trở → góc tấm pin; hiển thị giờ,\ngóc, trạng thái lên LCD I2C 1602", fs=7.4, wrap=40)
    box(ax, 40, y_lcd - 10, 30, 6, "Chờ hết chu kỳ rồi lặp lại", fs=7.8, round_=True)
    arr(ax, 40, 123.5, 40, 120)
    arr(ax, 40, 112, 40, 107.5)
    arr(ax, 40, 100.5, 40, 97)
    arr(ax, 40, 87, 40, 82, label="không", lx=41, ly=84.5)
    arr(ax, 60, 92, 65, 92, label="có", lx=60.5, ly=93.5)
    arr(ax, 40, 74, 40, 70.5)
    arr(ax, 59, 66, 65, 66, label="không", lx=59.5, ly=67.5)
    arr(ax, 40, 61.5, 40, 57.5, label="có", lx=41, ly=59.5)
    arr(ax, 59, 53, 65, 53, label="có", lx=59.5, ly=54.5)
    arr(ax, 40, 48.5, 40, 44.5 if hai else 36.5, label="không", lx=41, ly=46.5 if hai else 40)
    if hai:
        arr(ax, 59, 40, 65, 40, label="có", lx=59.5, ly=41.5)
        arr(ax, 40, 35.5, 40, 30.5, label="không", lx=41, ly=33)
    arr(ax, 40, y_lcd - 3.5, 40, y_lcd - 7)
    line(ax, 78, 88, 78, 84);  line(ax, 78, 84, 95, 84)
    line(ax, 78, 62.5, 78, 60); line(ax, 78, 60, 95, 60)
    line(ax, 78, 49.5, 78, 47); line(ax, 78, 47, 95, 47)
    if hai:
        line(ax, 78, 36.5, 78, 34.5); line(ax, 78, 34.5, 95, 34.5)
    line(ax, 95, 84, 95, y_lcd)
    line(ax, 95, y_lcd, 60, y_lcd)
    line(ax, 25, y_lcd - 10, 8, y_lcd - 10)
    line(ax, 8, y_lcd - 10, 8, 104)
    arr(ax, 8, 104, 20, 104)
    save(fig, "luu_do_tong_quat_%d_truc.png" % truc)


def luu_do_thien_van():
    fig, ax = new_fig(8.6, 11.4, (0, 86), (0, 114))
    title(ax, 43, 111, "LƯU ĐỒ ĐỌC GIỜ DS1307 VÀ TÍNH GÓC THIÊN VĂN", 9.5)
    box(ax, 43, 104, 22, 5, "BẮT ĐẦU", fs=8.4, round_=True)
    box(ax, 43, 95, 44, 7, "Đọc DS1307 qua I²C: giây, phút, giờ, ngày, tháng, năm", fs=7.6, wrap=44)
    box(ax, 43, 84, 44, 7, "Tính n = số ngày từ 1/1;  t = giờ Mặt Trời quy đổi", fs=7.6, wrap=44)
    box(ax, 43, 73, 46, 8, "δ = 23,45° · sin[360°·(284 + n)/365]", fs=8.0, wrap=46)
    box(ax, 43, 62, 46, 8, "H = 15° · (t − 12)", fs=8.0, wrap=46)
    box(ax, 43, 50, 50, 9, "sin α = sin φ·sin δ + cos φ·cos δ·cos H\n→ góc cao α", fs=7.8, wrap=50)
    box(ax, 43, 37, 50, 9, "γ = atan2(sin H, cos H·sin φ − tan δ·cos φ)\n→ góc phương vị", fs=7.8, wrap=50)
    box(ax, 43, 24, 50, 8, "Đổi (α, γ) ra góc đặt của từng trục, giới hạn hành trình", fs=7.6, wrap=50)
    box(ax, 43, 13, 26, 5, "Trả về góc đặt", fs=8.2, round_=True)
    for y1, y2 in ((101.5, 98.5), (91.5, 87.5), (80.5, 77), (69, 66),
                   (58, 54.5), (45.5, 41.5), (32.5, 28), (20, 15.5)):
        arr(ax, 43, y1, 43, y2)
    save(fig, "luu_do_thien_van.png")


def luu_do_doc_adc():
    fig, ax = new_fig(8.6, 11.0, (0, 86), (0, 110))
    title(ax, 43, 107, "LƯU ĐỒ ĐỌC ADC BỐN KÊNH LDR", 9.5)
    box(ax, 43, 100, 22, 5, "BẮT ĐẦU", fs=8.4, round_=True)
    box(ax, 43, 91, 46, 7, "Với mỗi kênh: lấy 16 mẫu ADC, bỏ mẫu lỗi, lấy trung bình", fs=7.6, wrap=46)
    box(ax, 43, 80, 46, 7, "Nhân hệ số hiệu chuẩn K_cal của từng kênh", fs=7.6, wrap=46)
    box(ax, 43, 69, 48, 8, "S = tổng 4 kênh;  e1 = (trái) − (phải);\ne2 = (trên) − (dưới)", fs=7.8, wrap=48)
    dec(ax, 43, 56, 38, 9, "S < S_min ?\n(trời mây mù)", fs=7.6)
    box(ax, 74, 56, 22, 7, "Báo cờ mây mù:\nkhông phát lệnh LDR", fs=7.4, wrap=22)
    box(ax, 43, 43, 44, 7, "Trả về S, e1, e2 cho khối quyết định", fs=7.8, wrap=44)
    box(ax, 43, 32, 22, 5, "KẾT THÚC", fs=8.4, round_=True)
    arr(ax, 43, 97.5, 43, 94.5)
    arr(ax, 43, 87.5, 43, 83.5)
    arr(ax, 43, 76.5, 43, 73)
    arr(ax, 43, 65, 43, 60.5)
    arr(ax, 62, 56, 63, 56, label="đúng", lx=62.5, ly=57.5)
    arr(ax, 43, 51.5, 43, 46.5, label="sai", lx=44, ly=49)
    arr(ax, 43, 39.5, 43, 34.5)
    save(fig, "luu_do_doc_adc.png")


def luu_do_dieu_khien_motor():
    fig, ax = new_fig(8.8, 11.6, (0, 88), (0, 116))
    title(ax, 44, 113, "LƯU ĐỒ ĐIỀU KHIỂN MOTOR QUA CẦU H 4 TIP41C", 9.5)
    box(ax, 44, 106, 30, 6, "Nhận e của một trục và góc tấm pin", fs=7.8, wrap=30)
    dec(ax, 44, 95, 36, 9, "|e| > ngưỡng?", fs=7.8)
    box(ax, 76, 95, 22, 7, "Tắt cả hai nhánh cầu H\n(motor tự giữ)", fs=7.4, wrap=22)
    dec(ax, 44, 82, 36, 9, "e mang dấu nào?\n(xác định chiều)", fs=7.6)
    box(ax, 20, 70, 22, 7, "Chiều A:\nIN1 = 1, IN2 = 0", fs=7.6, wrap=22)
    box(ax, 68, 70, 22, 7, "Chiều B:\nIN1 = 0, IN2 = 1", fs=7.6, wrap=22)
    dec(ax, 44, 58, 38, 9, "Công tắc hành trình\nchiều đó chạm?", fs=7.6)
    box(ax, 78, 58, 20, 7, "Dừng ngay,\nbáo lỗi trên LCD", fs=7.4, wrap=20)
    box(ax, 44, 45, 40, 8, "Giữ lệnh chạy; mỗi 10 ms đọc lại e\nvà biến trở hồi tiếp", fs=7.6, wrap=40)
    dec(ax, 44, 32, 38, 9, "|e| ≤ vùng chết\nhoặc tới góc đích?", fs=7.6)
    box(ax, 44, 19, 34, 7, "Tắt cả IN1, IN2 – trục vít tự hãm giữ vị trí", fs=7.6, wrap=34)
    box(ax, 44, 9, 22, 5, "KẾT THÚC", fs=8.4, round_=True)
    arr(ax, 44, 103, 44, 99.5)
    arr(ax, 44, 90.5, 44, 86.5, label="có", lx=45, ly=88.5)
    arr(ax, 62, 95, 65, 95, label="không", lx=62.5, ly=96.5)
    arr(ax, 36, 78, 26, 73.5, label="dương", lx=26, ly=76)
    arr(ax, 52, 78, 62, 73.5, label="âm", lx=58, ly=76)
    line(ax, 20, 66.5, 20, 63)
    line(ax, 68, 66.5, 68, 63)
    line(ax, 20, 63, 68, 63)
    arr(ax, 44, 63, 44, 62.5)
    arr(ax, 44, 53.5, 44, 49)
    arr(ax, 63, 58, 68, 58, label="có", lx=63.5, ly=59.5)
    arr(ax, 44, 41, 44, 36.5, label="chưa", lx=45, ly=38.5)
    arr(ax, 44, 27.5, 44, 22.5, label="rồi", lx=45, ly=25)
    arr(ax, 44, 15.5, 44, 11.5)
    save(fig, "luu_do_dieu_khien_motor.png")


def luu_do_lcd():
    fig, ax = new_fig(8.4, 9.6, (0, 84), (0, 96))
    title(ax, 42, 93, "LƯU ĐỒ HIỂN THỊ LCD I2C 1602", 9.5)
    box(ax, 42, 86, 22, 5, "BẮT ĐẦU", fs=8.4, round_=True)
    box(ax, 42, 77, 44, 7, "Đọc giờ, ngày từ DS1307 (I²C, địa chỉ 0x68)", fs=7.6, wrap=44)
    box(ax, 42, 66, 44, 7, "Đọc góc tấm pin từ biến trở và trạng thái motor", fs=7.6, wrap=44)
    box(ax, 42, 55, 46, 8, "Dòng 1: “DD/MM  HH:MM:SS”\nDòng 2: goc=+xx,x  e1=+xxx", fs=7.6, wrap=46)
    box(ax, 42, 43, 40, 7, "lcd.setCursor + lcd.print qua thư viện LiquidCrystal_I2C", fs=7.4, wrap=40)
    box(ax, 42, 32, 30, 6, "Chờ 1 giây rồi cập nhật lại", fs=7.8, round_=True)
    arr(ax, 42, 83.5, 42, 80.5)
    arr(ax, 42, 73.5, 42, 69.5)
    arr(ax, 42, 62.5, 42, 59)
    arr(ax, 42, 51, 42, 46.5)
    arr(ax, 42, 39.5, 42, 35)
    line(ax, 42, 29, 42, 26)
    line(ax, 42, 26, 12, 26)
    line(ax, 12, 26, 12, 77)
    arr(ax, 12, 77, 20, 77)
    save(fig, "luu_do_lcd.png")


def luu_do_bien_tro():
    fig, ax = new_fig(8.4, 9.8, (0, 84), (0, 98))
    title(ax, 42, 95, "LƯU ĐỒ ĐỌC BIẾN TRỞ SUY RA GÓC TẤM PIN", 9.5)
    box(ax, 42, 88, 22, 5, "BẮT ĐẦU", fs=8.4, round_=True)
    box(ax, 42, 79, 44, 7, "Đọc 16 mẫu ADC kênh biến trở, lấy trung bình", fs=7.6, wrap=44)
    box(ax, 42, 68, 46, 8, "Đổi sang điện áp: V = ADC · 3,3 / 4095", fs=7.8, wrap=46)
    box(ax, 42, 56, 50, 9, "Nội suy 3 điểm hiệu chuẩn:\nθ = θ_min + (V − V_min)·(θ_max − θ_min)/(V_max − V_min)", fs=7.4, wrap=50)
    box(ax, 42, 43, 44, 7, "Giới hạn θ trong hành trình cơ khí", fs=7.6, wrap=44)
    box(ax, 42, 32, 40, 7, "Trả về θ cho khối điều khiển và hiển thị LCD", fs=7.6, wrap=40)
    box(ax, 42, 21, 22, 5, "KẾT THÚC", fs=8.4, round_=True)
    arr(ax, 42, 85.5, 42, 82.5)
    arr(ax, 42, 75.5, 42, 72)
    arr(ax, 42, 64, 42, 60.5)
    arr(ax, 42, 51.5, 42, 46.5)
    arr(ax, 42, 39.5, 42, 35.5)
    arr(ax, 42, 28.5, 42, 23.5)
    save(fig, "luu_do_bien_tro.png")


if __name__ == "__main__":
    so_do_khoi(1)
    so_do_khoi(2)
    so_do_ket_noi(1)
    so_do_ket_noi(2)
    so_do_3_phuong_phap()
    bo_tri_ldr()
    luu_do_tong_quat(1)
    luu_do_tong_quat(2)
    luu_do_thien_van()
    luu_do_doc_adc()
    luu_do_dieu_khien_motor()
    luu_do_lcd()
    luu_do_bien_tro()
