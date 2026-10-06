# -*- coding: utf-8 -*-
"""Mo phong so he bam nang mat troi 1 truc tai My Hao, Hung Yen.

So sanh ba phuong phap dieu khien:
  - "thien_van" : vong ho, quay tam pin theo goc thien van tinh tu RTC (DS1307);
  - "ldr"       : vong kin, ma tran 4 LDR suy ra goc lech (phuong phap cu);
  - "lai"       : HYBRID - thien van dinh vi tho, LDR tinh chinh khi nang dep,
                  troi may thi giu lich thien van (khong dao dong vo ich).
Ket qua viet ra hinh_ve/ket_qua_mo_phong_1_truc.png va ket_qua_mo_phong.json.
Chay:  python3 tools/mo_phong.py
"""
import json
import math
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hinh_ve")

PHI = math.radians(20.93)      # vi do My Hao, Hung Yen
LAM = 106.06                   # kinh do Dong
BETA_S = math.radians(30.0)    # goc ga cam bien LDR
DELTA_DEAD = math.radians(3.0) # vung chet cua nhanh LDR tinh chinh
BETA_F = math.radians(21.0)    # goc nghieng tam doi chung co dinh

DAYS = [(80, "21/3"), (172, "21/6"), (266, "23/9"), (355, "21/12")]


def decl(n):
    return math.radians(23.45 * math.sin(math.radians(360.0 * (284 + n) / 365.0)))


def sun_vec(n, t):
    """Vectơ đơn vị hướng Mặt Trời (x = Đông, y = Bắc, z = thiên đỉnh)."""
    d = decl(n)
    h = math.radians(15.0 * (t - 12.0))
    sa = math.sin(PHI) * math.sin(d) + math.cos(PHI) * math.cos(d) * math.cos(h)
    al = math.asin(max(-1.0, min(1.0, sa)))
    ca = math.cos(al)
    az = math.atan2(math.sin(h), math.cos(h) * math.sin(PHI) - math.tan(d) * math.cos(PHI))
    return (ca * math.sin(az), ca * math.cos(az), sa)


def elev_deg(s):
    return math.degrees(math.asin(max(-1.0, min(1.0, s[2]))))


def azimuth_deg(s):
    return math.degrees(math.atan2(s[0], s[1]))


# ---------------------------------------------------------------- mặt phẳng quay
def panel_axes(rho):
    """Trục quay nằm ngang hướng Bắc-Nam; rho = góc quay (0 = nằm ngang)."""
    n = (math.sin(rho), 0.0, math.cos(rho))           # pháp tuyến tấm pin
    r = (math.cos(rho), 0.0, -math.sin(rho))          # hướng "phải" (Đông khi rho=0)
    return n, r


def rho_star(s):
    """Góc quay lý tưởng: chiếu hướng Mặt Trời lên mặt phẳng quay."""
    return math.atan2(s[0], s[2])


def ldr_pair(delt, k1=1.0, k2=1.0, diff=0.0):
    """Đáp ứng cặp LDR lệch +/- BETA_S trong mặt phẳng quay."""
    l1 = k1 * math.cos(delt - BETA_S) + diff
    l2 = k2 * math.cos(delt + BETA_S) + diff
    return l1, l2


def delta_hat(l1, l2):
    e = (l1 - l2) / (l1 + l2)
    return math.atan(e / math.tan(BETA_S))


def cloud(t, seed=0):
    """Hệ số nắng 0..1 (1 = quang đãng), biến đổi chậm trong ngày."""
    v = (0.55 + 0.45 * math.sin(2 * math.pi * (t - 7.3) / 6.1 + seed)
         + 0.22 * math.sin(2 * math.pi * (t - 4.1) / 2.7 + 2.0 * seed))
    cl = 0.5 + 0.5 * v / 1.22
    if seed == 2:
        cl -= 0.55          # ngày nhiều mây: phần lớn thời gian dưới ngưỡng nắng
    elif seed == 3:
        cl -= 0.25          # ngày mây trung bình
    return max(0.05, min(1.0, cl))


# ---------------------------------------------------------------- vòng kín một ngày
OFF = math.radians(4.0)      # sai số lắp đặt/đồng hồ của vòng hở thiên văn
STEP = math.radians(2.0)     # bước quay cố định của luật LDR thuần


def ldr_read(d, cl, t, mismatch, noise):
    """Giá trị cặp LDR: nắng đẹp theo cos(Δ∓β_s); mây dày chỉ còn sáng khuếch tán."""
    if cl < 0.45:
        # mây dày: chỉ còn sáng khuếch tán gần đều, chênh lệch rất nhỏ
        l1 = 0.35 + 0.02 * math.sin(5.1 * t + 1.0) + noise * math.sin(97.0 * t)
        l2 = 0.35 + 0.02 * math.cos(4.3 * t) + noise * math.cos(89.0 * t)
        return l1, l2
    l1, l2 = ldr_pair(d, 1.0 + mismatch, 1.0 - mismatch,
                      0.10 * math.cos(d) * (1.0 - cl))
    l1 *= 1.0 + noise * math.sin(97.0 * t)
    l2 *= 1.0 + noise * math.cos(89.0 * t)
    return l1, l2


def run_day(n, method="lai", mismatch=0.03, noise=0.01, seed=1, dt_min=2.0):
    """Mô phỏng cả ngày; trả (sai số trung bình deg, số lần chạy motor, năng lượng)."""
    errs, moves, energy = [], 0, 0.0
    rho = rho_star(sun_vec(n, 6.0)) + OFF              # xuất phát theo lịch sáng sớm
    t = 5.0
    while t <= 19.0:
        s = sun_vec(n, t)
        rs = rho_star(s)
        cl = cloud(t, seed)
        nrm, rgt = panel_axes(rho)
        cos_i = max(0.0, nrm[0] * s[0] + nrm[1] * s[1] + nrm[2] * s[2])
        energy += cl * cos_i * dt_min
        if elev_deg(s) > 5.0:
            errs.append(math.degrees(rs - rho))
            target = rho
            if method == "thien_van":
                # vòng hở: lịch thiên văn từ RTC, nhảy bước 2 độ
                if abs(rs + OFF - rho) > math.radians(2.0):
                    target = rs + OFF
                    moves += 1
            elif method == "ldr":
                d = rs - rho
                l1, l2 = ldr_read(d, cl, t, mismatch, noise)
                dh = delta_hat(l1, l2)
                if abs(dh) > DELTA_DEAD:
                    target = rho + math.copysign(STEP, dh)   # dò bước cố định
                    moves += 1
            else:                                            # lai (hybrid)
                d = rs - rho
                l1, l2 = ldr_read(d, cl, t, 0.0, noise)      # kênh đã hiệu chuẩn
                dh = delta_hat(l1, l2)
                if cl >= 0.45 and abs(dh) > math.radians(1.5):
                    target = rho + dh                        # nắng: LDR tinh chỉnh
                    moves += 1
                elif abs(rs + OFF - rho) > math.radians(5.0):
                    target = rs + OFF                        # mây/lệch thô: bám lịch
                    moves += 1
            if abs(target - rho) > 1e-9:
                rho = target
        t += dt_min / 60.0
    mean_err = sum(abs(e) for e in errs) / max(1, len(errs))
    return mean_err, moves, energy


def main():
    import random
    res = {}

    # ---- 1) năng lượng cả ngày: cố định / thiên văn / LDR / lai (4 ngày, 3 kịch bản mây)
    print("=== Nang luong thu duoc ca ngay (don vi tuong doi) ===")
    res["energy"] = []
    for n, name in DAYS:
        row = {"ngay": name, "co_dinh": 0.0, "thien_van": 0.0, "ldr": 0.0, "lai": 0.0}
        for seed in (1, 2, 3):
            # tấm cố định
            e_fix = 0.0
            t = 5.0
            while t <= 19.0:
                s = sun_vec(n, t)
                nf = (0.0, -math.sin(BETA_F), math.cos(BETA_F))
                ci = max(0.0, nf[0] * s[0] + nf[1] * s[1] + nf[2] * s[2])
                e_fix += cloud(t, seed) * ci * 2.0
                t += 2.0 / 60.0
            row["co_dinh"] += e_fix / 3.0
            for m in ("thien_van", "ldr", "lai"):
                _, _, en = run_day(n, m, seed=seed)
                row[m] += en / 3.0
        res["energy"].append(row)
        print("  %-6s co dinh=%6.1f  thien van=%6.1f (+%5.1f%%)  LDR=%6.1f (+%5.1f%%)  lai=%6.1f (+%5.1f%%)"
              % (name, row["co_dinh"], row["thien_van"],
                 100 * (row["thien_van"] / row["co_dinh"] - 1),
                 row["ldr"], 100 * (row["ldr"] / row["co_dinh"] - 1),
                 row["lai"], 100 * (row["lai"] / row["co_dinh"] - 1)))

    # ---- 2) sai số bám & số lần chạy motor (ngày quang đãng, seed=1)
    print("=== Sai so bam va so lan chay motor (ngay quang) ===")
    res["track"] = []
    for n, name in DAYS:
        r = {}
        for m in ("thien_van", "ldr", "lai"):
            er, mv, _ = run_day(n, m, seed=1)
            r[m] = (round(er, 2), mv)
        res["track"].append({"ngay": name, **{k: v for k, v in r.items()}})
        print("  %-6s thien van %5.2f do/%3d lan | LDR %5.2f do/%3d lan | LAI %5.2f do/%3d lan"
              % (name, r["thien_van"][0], r["thien_van"][1],
                 r["ldr"][0], r["ldr"][1], r["lai"][0], r["lai"][1]))

    # ---- 3) ngày nhiều mây: lai giữ lịch nên không dao động
    print("=== Ngay nhieu may (seed=2): so lan chay motor ===")
    res["cloudy"] = []
    for n, name in DAYS:
        r = {}
        for m in ("ldr", "lai"):
            er, mv, _ = run_day(n, m, seed=2)
            r[m] = (round(er, 2), mv)
        res["cloudy"].append({"ngay": name, **{k: v for k, v in r.items()}})
        print("  %-6s LDR %3d lan (sai so %4.2f) | LAI %3d lan (sai so %4.2f)"
              % (name, r["ldr"][1], r["ldr"][0], r["lai"][1], r["lai"][0]))

    # ---- 4) ví dụ trực quan một lần đọc ma trận LDR (mức ADC 12 bit)
    ex = []
    for delt_deg in (0, 3, 6, 10, 15, 20, 30):
        d = math.radians(delt_deg)
        l1, l2 = ldr_pair(d)
        a1, a2 = 2000 * l1, 2000 * l2
        e = (a1 - a2) / (a1 + a2)
        ex.append({"delta": delt_deg, "L_phai": round(a1), "L_trai": round(a2),
                   "e": round(e, 3), "delta_suy_ra": round(math.degrees(delta_hat(a1, a2)), 2)})
    res["ma_tran"] = ex
    print("=== Vi du doc ma tran LDR (muc ADC) ===")
    for r in ex:
        print("  lech that %+3d do -> L_phai=%4d L_trai=%4d e=%+.3f -> suy ra %+5.2f do"
              % (r["delta"], r["L_phai"], r["L_trai"], r["e"], r["delta_suy_ra"]))

    # ---- 5) đồ thị ngày 21/6: góc lý tưởng vs góc tấm của luật lai + hệ số mây
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.5, 7.2), dpi=200,
                                       sharex=True, gridspec_kw={"height_ratios": [2, 1]})
        ts, ideal, lai, tv, cl = [], [], [], [], []
        rho_l = rho_star(sun_vec(172, 5.0))
        rho_t = rho_l
        t = 5.0
        while t <= 19.0:
            s = sun_vec(172, t)
            rs = rho_star(s)
            c = cloud(t, 1)
            ts.append(t)
            ideal.append(math.degrees(rs))
            cl.append(c)
            # luật lai
            d = rs - rho_l
            l1, l2 = ldr_pair(d, 1.03, 0.97, 0.10 * math.cos(d) * (1 - c))
            dh = delta_hat(l1, l2)
            if c >= 0.45 and abs(dh) > DELTA_DEAD:
                rho_l += dh
            elif abs(rs - rho_l) > math.radians(6.0):
                rho_l = rs
            lai.append(math.degrees(rho_l))
            tv.append(math.degrees(rs))
            t += 2.0 / 60.0
        ax1.plot(ts, ideal, color="#1f3864", lw=2.2, label="Góc Mặt Trời lý tưởng (thiên văn)")
        ax1.plot(ts, lai, color="#c0504d", lw=1.8, ls="--",
                 label="Góc tấm pin thực tế (luật lai)")
        ax1.set_ylabel("Góc quay Đông–Tây (độ)")
        ax1.legend(loc="lower center", fontsize=9)
        ax1.grid(alpha=0.3)
        ax1.set_title("Ngày 21/6 tại Mỹ Hào: luật lai bám sát góc lý tưởng",
                      fontsize=12, fontweight="bold", color="#16324f")
        ax2.fill_between(ts, 0, cl, color="#8ea9d1", alpha=0.55)
        ax2.set_ylim(0, 1.05)
        ax2.set_ylabel("Hệ số nắng")
        ax2.set_xlabel("Giờ trong ngày (giờ Mặt Trời)")
        ax2.grid(alpha=0.3)
        fig.tight_layout()
        os.makedirs(OUT, exist_ok=True)
        fig.savefig(os.path.join(OUT, "ket_qua_mo_phong_1_truc.png"),
                    facecolor="white", bbox_inches="tight", pad_inches=0.2)
        plt.close(fig)
        print("da ve: ket_qua_mo_phong_1_truc.png")

        # bieu do cot: nang luong trong ngay, tam co dinh = 100%
        names = [r["ngay"] for r in res["energy"]]
        fig2, ax = plt.subplots(figsize=(9.5, 4.6), dpi=200)
        x = range(len(names))
        w = 0.26
        tv = [100 * r["thien_van"] / r["co_dinh"] for r in res["energy"]]
        ld = [100 * r["ldr"] / r["co_dinh"] for r in res["energy"]]
        ll = [100 * r["lai"] / r["co_dinh"] for r in res["energy"]]
        ax.bar([i - w for i in x], tv, w, color="#8ea9d1", label="Thiên văn (vòng hở)")
        ax.bar(list(x), ld, w, color="#c0504d", label="LDR thuần (vòng kín)")
        ax.bar([i + w for i in x], ll, w, color="#4f8a4f", label="Lai thiên văn + LDR")
        ax.axhline(100, color="#404040", lw=1.2, ls=":")
        ax.text(0.02, 103, "tấm cố định = 100%", fontsize=9, color="#404040")
        ax.set_xticks(list(x))
        ax.set_xticklabels(names)
        ax.set_ylabel("Năng lượng thu được trong ngày (%)")
        ax.set_title("Năng lượng thu được so với tấm cố định (trung bình 3 kịch bản mây)",
                     fontsize=11.5, fontweight="bold", color="#16324f")
        ax.legend(fontsize=9)
        ax.grid(axis="y", alpha=0.3)
        for i, v in enumerate(ll):
            ax.text(i + w, v + 3, "%.0f%%" % v, ha="center", fontsize=8.5)
        fig2.tight_layout()
        fig2.savefig(os.path.join(OUT, "ket_qua_nang_luong.png"),
                     facecolor="white", bbox_inches="tight", pad_inches=0.2)
        plt.close(fig2)
        print("da ve: ket_qua_nang_luong.png")
    except Exception as exc:  # pragma: no cover
        print("khong ve duoc hinh:", exc)

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "ket_qua_mo_phong.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print("da ghi: hinh_ve/ket_qua_mo_phong.json")


if __name__ == "__main__":
    main()
