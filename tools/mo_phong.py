# -*- coding: utf-8 -*-
"""Mo phong phuong phap HYBRID (thien van dinh vi tho + LDR tinh chinh).

- Tinh vi tri Mat Troi theo dung cong thuc:
    delta = 23.45*sin(360*(284+n)/365);  H = 15*(t-12)
    sin(alpha) = sin(phi)sin(delta) + cos(phi)cos(delta)cos(H)
- Ma tran tinh toan goc: alpha, gamma theo gio cho 4 ngay dai dien.
- Mo phong 1 ngay lam viec cua 3 luat: vong ho thien van, vong kin LDR, hybrid.
- Bang ADC minh hoa: e1 = ADC(trai) - ADC(phai) theo vi tri Mat Troi.
- So sanh nang luong thu duoc: co dinh / 1 truc / 2 truc (ve bieu do cot).

Chay: python3 tools/mo_phong.py  -> hinh_ve/*.png + hinh_ve/ket_qua_mo_phong.json
"""
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PHI = 20.93          # vi do My Hao, Hung Yen
DAYS = [("21/3", 80), ("21/6", 172), ("23/9", 266), ("21/12", 355)]
BETA_S = math.radians(30.0)     # goc ga cam bien (vach cheo)
ADC_MAX = 3000.0                # muc ADC khi chieu thang goc (0..4095)
ADC_DIFF = 150.0                # san ADC do anh sang khuech tan
NGUONG_E1 = 200                 # nguong |e1| phat lenh (muc ADC, ~4 do lech)
DEADBAND = 35                   # vung chet dung motor (muc ADC)
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "hinh_ve")


def rad(x):
    return math.radians(x)


def declination(n):
    return 23.45 * math.sin(rad(360.0 * (284 + n) / 365.0))


def sun_angles(n, t):
    """Tra ve (alpha, gamma) do: goc cao va goc phuong vi (tinh tu Nam, tay duong)."""
    d = rad(declination(n))
    H = rad(15.0 * (t - 12.0))
    p = rad(PHI)
    sin_a = math.sin(p) * math.sin(d) + math.cos(p) * math.cos(d) * math.cos(H)
    sin_a = max(-1.0, min(1.0, sin_a))
    a = math.asin(sin_a)
    g = math.atan2(math.sin(H), math.cos(H) * math.sin(p) - math.tan(d) * math.cos(p))
    return math.degrees(a), math.degrees(g)


def sun_vec(n, t):
    a, g = sun_angles(n, t)
    a, g = rad(a), rad(g)
    x = math.cos(a) * math.sin(g)     # huong Tay (+)
    y = math.cos(a) * math.cos(g)     # huong Bac (+)
    z = math.sin(a)                   # cao (+)
    return x, y, z


def cos_incidence_fixed(n, t, tilt=21.0):
    """cos goc toi tren tam co dinh, nghiang `tilt` do ve phia Nam."""
    x, y, z = sun_vec(n, t)
    tl = rad(tilt)
    nx, ny, nz = 0.0, -math.sin(tl), math.cos(tl)   # phap tuyen nghieng ve Nam
    return max(0.0, x * nx + y * ny + z * nz)


def cos_incidence_1axis(n, t, theta):
    """1 truc quay quanh truc Bac-Nam; theta = goc quay ve phia Tay (+)."""
    x, y, z = sun_vec(n, t)
    th = rad(theta)
    nx, nz = math.sin(th), math.cos(th)
    return max(0.0, x * nx + z * nz)


def theta_sun_1axis(n, t):
    """Goc quay ly tuong cua tam 1 truc (khop hinh chieu Dong-Tay cua vec to MT)."""
    x, y, z = sun_vec(n, t)
    return math.degrees(math.atan2(x, z))


def day_energy(n, mode, dt=1.0):
    t0, t1 = 4.0, 20.0
    e = 0.0
    t = t0
    while t <= t1:
        a, _g = sun_angles(n, t)
        if a > 0.0:                      # chi tinh khi Mat Troi tren chan troi
            if mode == "fixed":
                e += cos_incidence_fixed(n, t) * dt
            elif mode == "1axis":
                e += cos_incidence_1axis(n, t, theta_sun_1axis(n, t)) * dt
            else:                        # 2 truc: phap tuyen luon trung tia nang
                e += 1.0 * dt
        t += dt
    return e


# ---------------------------------------------------------------- LDR / ADC
def ldr_adc(delta_deg, side):
    """ADC cua cam bien ben 'trai'/'phai' khi huong MT lech delta (do, + = ve phai)."""
    d = rad(delta_deg)
    b = BETA_S
    ang = (d - b) if side == "phai" else (d + b)
    direct = max(0.0, math.cos(ang))
    diffuse = 0.12
    return ADC_MAX * direct + ADC_DIFF * (0.55 + 0.45 * max(0.0, math.cos(d))) + diffuse * 0


def bang_adc_minh_hoa():
    rows = []
    for delta in (-20, -10, -5, 0, 5, 10, 20):
        l = round(ldr_adc(delta, "trai"))
        r = round(ldr_adc(delta, "phai"))
        e1 = l - r
        if abs(e1) <= NGUONG_E1:
            act = "Dừng (trong vùng chết)"
        elif e1 > 0:
            act = "Quay sang TRÁI (về phía Đông)"
        else:
            act = "Quay sang PHẢI (về phía Tây)"
        rows.append([delta, l, r, e1, act])
    return rows


# ---------------------------------------------------------------- mo phong ngay
def simulate_day(n, mode, cloudy=(10.0, 11.0), seed=7):
    """mode: 'openloop' | 'closedloop' | 'hybrid'. Tra ve (sai so TB, max, so lan motor, day goc)."""
    import random
    random.seed(seed)
    t0 = 5.5
    t1 = 18.5
    # gio mat moc: alpha > 0
    t = 5.0
    while sun_angles(n, t)[0] <= 2.0 and t < 12:
        t += 0.1
    t0 = t
    t = 19.0
    while sun_angles(n, t)[0] <= 2.0 and t > 12:
        t -= 0.1
    t1 = t

    p = 0.0                 # goc tam pin hien tai (do)
    runs = 0
    errs = []
    track = []
    t = t0
    dt = 1.0 / 60.0         # 1 phut
    last_sched = -99.0
    last_ldr = -99.0
    while t <= t1 + 1e-9:
        ts = theta_sun_1axis(n, t)
        in_cloud = cloudy[0] <= t <= cloudy[1] if cloudy else False
        direct = 0.12 if in_cloud else 1.0

        if mode in ("openloop", "hybrid"):
            if t - last_sched >= 0.5 and not in_cloud:
                last_sched = t
                if abs(ts - p) > 2.0:
                    p = ts
                    runs += 1
        if mode in ("closedloop", "hybrid"):
            if t - last_ldr >= (2.0 / 60.0):
                last_ldr = t
                delta = (ts - p) if not in_cloud else 0.0
                # cam bien nhan direct*DNI; khi may thi tin hieu rat yeu
                d_eff = rad(delta)
                lp = ADC_MAX * direct * max(0.0, math.cos(d_eff + BETA_S)) + ADC_DIFF
                rp = ADC_MAX * direct * max(0.0, math.cos(d_eff - BETA_S)) + ADC_DIFF
                lp *= 1 + random.gauss(0, 0.02)
                rp *= 1 + random.gauss(0, 0.02)
                e1 = lp - rp
                if not in_cloud and abs(e1) > NGUONG_E1:
                    step = 5.0 if abs(e1) > 3 * NGUONG_E1 else 1.5
                    p += step if e1 < 0 else -step   # e1<0: ben phai (Tay) sang hon -> quay ve Tay
                    runs += 1
        errs.append(abs(ts - p))
        track.append((t, p, ts))
        t += dt
    mean_e = sum(errs) / len(errs)
    max_e = max(errs)
    return mean_e, max_e, runs, track


# ---------------------------------------------------------------- ve
def style_ax(ax):
    ax.set_facecolor("white")
    for s in ax.spines.values():
        s.set_color("#444444")
        s.set_linewidth(0.8)
    ax.grid(color="#cccccc", lw=0.5, alpha=0.7)
    ax.tick_params(colors="#222222", labelsize=8.5)


def ve_duong_di_mat_troi():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.6, 6.4), dpi=200, sharex=True)
    fig.patch.set_facecolor("white")
    hours = [5 + i * 0.1 for i in range(141)]
    colors = {"21/3": "#1f77b4", "21/6": "#d62728", "23/9": "#2ca02c", "21/12": "#7f7f7f"}
    for name, n in DAYS:
        xs, al, ga = [], [], []
        for t in hours:
            a, g = sun_angles(n, t)
            if a > -2:
                xs.append(t)
                al.append(max(a, 0))
                ga.append(g)
        a1.plot(xs, al, color=colors[name], lw=1.4, label=name)
        a2.plot(xs, ga, color=colors[name], lw=1.4, label=name)
    a1.set_ylabel("Góc cao α (độ)")
    a2.set_ylabel("Góc phương vị γ (độ, từ Nam)")
    a2.set_xlabel("Giờ Mặt Trời")
    a2.axhline(0, color="#999999", lw=0.7)
    a2.set_xticks(range(5, 20))
    for a in (a1, a2):
        style_ax(a)
    a1.legend(fontsize=8.5, frameon=False, ncol=4)
    a1.set_title("Đường đi của Mặt Trời tại Mỹ Hào (φ = 20,93°) – 4 ngày đại diện",
                 fontsize=10, color="#111111")
    fig.tight_layout()
    p = os.path.join(OUT, "duong_di_mat_troi.png")
    fig.savefig(p, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("da ve:", p)


def ve_so_sanh_nang_luong(res):
    fig, ax = plt.subplots(figsize=(7.6, 4.0), dpi=200)
    fig.patch.set_facecolor("white")
    labels = [d[0] for d in DAYS]
    g1 = [res["gain1"][d[0]] for d in DAYS]
    g2 = [res["gain2"][d[0]] for d in DAYS]
    x = range(len(labels))
    w = 0.36
    b1 = ax.bar([i - w / 2 for i in x], g1, w, color="#4a7ebb", edgecolor="#2c4d75", lw=0.6)
    b2 = ax.bar([i + w / 2 for i in x], g2, w, color="#e8a13c", edgecolor="#8a5d16", lw=0.6)
    for bars in (b1, b2):
        for r in bars:
            ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 3,
                    "+%.0f%%" % r.get_height(), ha="center", fontsize=8.5, color="#111111")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Điện thu được tăng thêm so với tấm cố định (%)")
    ax.set_ylim(0, max(max(g1), max(g2)) * 1.25)
    ax.legend([b1, b2], ["Bám 1 trục", "Bám 2 trục"], fontsize=9, frameon=False)
    ax.set_title("So sánh trực quan: bám nắng thu thêm bao nhiêu điện trong ngày",
                 fontsize=10, color="#111111")
    style_ax(ax)
    fig.tight_layout()
    p = os.path.join(OUT, "so_sanh_nang_luong.png")
    fig.savefig(p, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("da ve:", p)


def ve_hoat_dong_hybrid(track):
    fig, ax = plt.subplots(figsize=(8.2, 4.4), dpi=200)
    fig.patch.set_facecolor("white")
    ts = [r[0] for r in track]
    pp = [r[1] for r in track]
    ss = [r[2] for r in track]
    ax.plot(ts, ss, color="#d62728", lw=1.3, label="Góc Mặt Trời (lý tưởng)")
    ax.plot(ts, pp, color="#1f77b4", lw=1.5, label="Góc tấm pin (hybrid)")
    ax.axvspan(10, 11, color="#bbbbbb", alpha=0.45, lw=0)
    ax.text(10.5, -72, "Nhiều mây:\ngiữ vị trí theo lịch", ha="center",
            fontsize=8.5, color="#333333")
    ax.annotate("Sáng sớm: di chuyển\ntheo lịch thiên văn", xy=(6.4, -35), xytext=(6.2, -62),
                fontsize=8.5, color="#333333",
                arrowprops=dict(arrowstyle="->", color="#333333", lw=0.8))
    ax.annotate("Giữa trưa: LDR tinh chỉnh\nquanh vị trí cân bằng", xy=(12.6, 8), xytext=(13.2, -48),
                fontsize=8.5, color="#333333",
                arrowprops=dict(arrowstyle="->", color="#333333", lw=0.8))
    ax.set_xlabel("Giờ Mặt Trời")
    ax.set_ylabel("Góc tấm pin (độ)")
    ax.set_title("Một ngày làm việc của phương pháp hybrid (21/3, có đám mây 10h–11h)",
                 fontsize=10, color="#111111")
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    style_ax(ax)
    fig.tight_layout()
    p = os.path.join(OUT, "hoat_dong_hybrid.png")
    fig.savefig(p, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("da ve:", p)


def main():
    os.makedirs(OUT, exist_ok=True)
    res = {"phi": PHI, "beta_s": 30.0, "gain1": {}, "gain2": {}, "matrix": {},
           "adc_table": [], "modes": {}, "delta_days": {}}

    print("=== Nang luong thu duoc (don vi tuong doi) ===")
    for name, n in DAYS:
        f = day_energy(n, "fixed")
        a1 = day_energy(n, "1axis")
        a2 = day_energy(n, "2axis")
        res["gain1"][name] = (a1 / f - 1) * 100
        res["gain2"][name] = (a2 / f - 1) * 100
        res["delta_days"][name] = declination(n)
        print("  %6s co dinh=%6.1f  1 truc=%6.1f (+%4.1f%%)  2 truc=%6.1f (+%4.1f%%)"
              % (name, f, a1, res["gain1"][name], a2, res["gain2"][name]))

    print("=== Ma tran tinh toan goc (alpha / gamma theo gio) ===")
    gio = list(range(6, 19))
    res["hours"] = gio
    for name, n in DAYS:
        m = {}
        for h in gio:
            a, g = sun_angles(n, h)
            m[str(h)] = [round(a, 1), round(g, 1)]
        res["matrix"][name] = m
        line = " ".join("%dh:%.0f/%.0f" % (h, m[str(h)][0], m[str(h)][1]) for h in (7, 10, 12, 14, 17))
        print("  %6s delta=%+5.1f  %s" % (name, declination(n), line))

    print("=== Bang ADC minh hoa (e1 = ADC trai - ADC phai) ===")
    res["adc_table"] = bang_adc_minh_hoa()
    for r in res["adc_table"]:
        print("  lech %+3d do: trai=%4d phai=%4d e1=%+5d -> %s" % tuple(r))

    print("=== Mo phong 1 ngay 21/3 (co dam may 10h-11h) ===")
    for mode, label in (("openloop", "Vong ho thien van (30 phut/lan)"),
                        ("closedloop", "Vong kin LDR (2 phut/lan)"),
                        ("hybrid", "HYBRID (ho + kin)")):
        me, mx, runs, track = simulate_day(80, mode)
        res["modes"][mode] = {"mean": round(me, 2), "max": round(mx, 2), "runs": runs}
        print("  %-36s sai so TB=%4.1f do  max=%4.1f do  %3d lan chay motor"
              % (label, me, mx, runs))
        if mode == "hybrid":
            ve_hoat_dong_hybrid(track)

    ve_duong_di_mat_troi()
    ve_so_sanh_nang_luong(res)
    with open(os.path.join(OUT, "ket_qua_mo_phong.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print("da ghi:", os.path.join(OUT, "ket_qua_mo_phong.json"))


if __name__ == "__main__":
    main()
