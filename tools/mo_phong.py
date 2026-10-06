# -*- coding: utf-8 -*-
"""Mo phong so phuong phap doc ma tran 4 LDR suy ra goc quay (khong quay theo thoi gian).

Ket qua dung cho ca 6 quyen bao cao: hieu suat thu nang, sai so phuong phap,
so sanh voi phuong phap bam theo buoc/thoi gian.
Chay: python3 tools/mo_phong.py
"""
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hinh_ve")

PHI = math.radians(20.93)     # vi do My Hao, Hung Yen
LAM = 106.06                  # kinh do
BETA_S = math.radians(30.0)   # goc ga cam bien
BETA_F = math.radians(21.0)   # goc nghieng tam pin co dinh
DAYS = [("21/3", 80), ("21/6", 172), ("23/9", 266), ("21/12", 355)]


def sun_vec(n_day, t_hour):
    d = math.radians(23.45) * math.sin(math.radians(360.0 * (284 + n_day) / 365.0))
    w = math.radians(15.0 * (t_hour - 12.0))
    sa = math.sin(PHI) * math.sin(d) + math.cos(PHI) * math.cos(d) * math.cos(w)
    sa = max(-1.0, min(1.0, sa))
    al = math.asin(sa)
    ca = math.cos(al)
    if ca < 1e-9:
        return None
    sg = math.cos(d) * math.sin(w) / ca
    cg = (sa * math.sin(PHI) - math.sin(d)) / (ca * math.cos(PHI))
    g = math.atan2(sg, cg)
    E = ca * math.sin(g)
    N = ca * math.cos(g)
    U = sa
    return E, N, U, al, g


def cos_fix(s):
    E, N, U, al, g = s
    n = (0.0, -math.sin(BETA_F), math.cos(BETA_F))
    return max(0.0, E * n[0] + N * n[1] + U * n[2])


def cos_1truc(s):
    E, N, U, al, g = s
    return math.hypot(E, U)


def rho_star(s):
    E, N, U, al, g = s
    return math.atan2(E, U)


def ldr_pair(delta, K1, K2, diff):
    """Hai cam bien nghenh +- beta_s trong mat phang quay."""
    L1 = K1 * max(0.0, math.cos(delta - BETA_S)) + diff
    L2 = K2 * max(0.0, math.cos(delta + BETA_S)) + diff
    return L1, L2


def delta_hat(L1, L2):
    s = L1 + L2
    if s <= 1e-9:
        return 0.0
    e = (L1 - L2) / s
    v = e / math.tan(BETA_S)
    v = max(-3.0, min(3.0, v))
    return math.atan(v)


def run_day(n_day, mismatch=0.0, noise=0.0, diff=0.0, method="matrix",
            step_deg=2.0, dead=0.03, dt_min=1.0, mat_dead=1.0):
    """Mong phng vong kin trong ngay; tra ve sai so trung binh va so lan chay."""
    import random
    random.seed(7)
    rho = 0.0                      # goc tam pin hien tai
    tilt_err_sum = 0.0
    err_sum = 0.0
    cnt = 0
    moves = 0
    t = 5.5
    while t <= 18.5:
        s = sun_vec(n_day, t)
        if s is None or s[3] < math.radians(8):
            t += dt_min / 60.0
            continue
        rs = rho_star(s)
        delta = rs - rho
        if method == "matrix":
            L1, L2 = ldr_pair(delta, 1.0 + mismatch, 1.0, diff)
            if noise:
                L1 *= 1 + random.gauss(0, noise)
                L2 *= 1 + random.gauss(0, noise)
            dh = delta_hat(L1, L2)
            if abs(dh) > math.radians(mat_dead):
                rho = rho + dh
                moves += 1
        else:  # phuong phap cu: buoc co dinh theo thoi gian
            L1, L2 = ldr_pair(delta, 1.0 + mismatch, 1.0, diff)
            if noise:
                L1 *= 1 + random.gauss(0, noise)
                L2 *= 1 + random.gauss(0, noise)
            ss = L1 + L2
            e = (L1 - L2) / ss if ss > 0 else 0.0
            if abs(e) > dead:
                rho += math.copysign(math.radians(step_deg), e)
                moves += 1
        err = rs - rho
        err_sum += abs(err)
        cnt += 1
        t += dt_min / 60.0
    return (err_sum / cnt if cnt else 0.0), moves, cnt


def yield_table():
    rows = []
    for name, n in DAYS:
        yf = y1 = y2 = 0.0
        t = 5.0
        while t <= 19.0:
            s = sun_vec(n, t)
            if s and s[3] > 0:
                yf += cos_fix(s)
                y1 += cos_1truc(s)
                y2 += 1.0
            t += 5.0 / 60.0
        rows.append((name, yf, y1, y2))
    return rows


def main():
    res = {}
    yt = yield_table()
    res["yield"] = yt
    print("=== Bang hieu suat thu truc xa (don vi tuong doi cos.dt) ===")
    for name, yf, y1, y2 in yt:
        print("%6s  co dinh=%6.2f  1 truc=%6.2f (+%4.1f%%)  2 truc=%6.2f (+%4.1f%% so 1 truc)"
              % (name, yf, y1, 100 * (y1 / yf - 1), y2, 100 * (y2 / y1 - 1)))

    print("=== Sai so phuong phap ma tran (Monte Carlo 400 lan, lech ban dau 7.5 do) ===")
    import random
    cases = [("ly tuong", 0.0, 0.0, 0.0, False),
             ("lech do loi +/-5%", 0.05, 0.0, 0.0, False),
             ("lech do loi, da hieu chuan", 0.05, 0.0, 0.0, True),
             ("nhieu 2%", 0.0, 0.02, 0.0, False),
             ("khuech tan 15%", 0.0, 0.0, 0.15, False),
             ("ton hop, da hieu chuan", 0.05, 0.02, 0.15, True)]
    res["acc"] = []
    for name, mm, nz, df, cal in cases:
        errs = []
        random.seed(11)
        for _ in range(400):
            k1 = 1.0 + random.uniform(-mm, mm)
            k2 = 1.0 + random.uniform(-mm, mm)
            if cal:
                c1, c2 = k1, k2          # hieu chuan bu do loi duoi nen khuech tan
            else:
                c1 = c2 = 1.0
            d = math.radians(random.uniform(2, 12))
            L1, L2 = ldr_pair(d, k1, k2, df * math.cos(d))
            L1 /= c1
            L2 /= c2
            if nz:
                L1 *= 1 + random.gauss(0, nz)
                L2 *= 1 + random.gauss(0, nz)
            errs.append(math.degrees(d - delta_hat(L1, L2)))
        rmse = math.sqrt(sum(e * e for e in errs) / len(errs))
        res["acc"].append((name, rmse))
        print("%-26s RMSE = %5.2f do" % (name, rmse))

    print("=== So sanh ma tran vs bam buoc co dinh (quay theo thoi gian) ===")
    res["cmp"] = []
    for _n, nd in DAYS:
        e_m, m_m, c = run_day(nd, 0.03, 0.01, 0.10, "matrix", mat_dead=1.0)
        e_d, m_d, c = run_day(nd, 0.03, 0.01, 0.10, "matrix", mat_dead=3.0)
        e_s, m_s, c = run_day(nd, 0.03, 0.01, 0.10, "step")
        res["cmp"].append((nd, math.degrees(e_m), m_m, math.degrees(e_d), m_d,
                           math.degrees(e_s), m_s))
        print("ngay %3d: ma tran(1o) %4.2f do/%3d lan | ma tran(3o) %4.2f do/%3d lan | buoc-thoi gian %4.2f do/%3d lan"
              % (nd, math.degrees(e_m), m_m, math.degrees(e_d), m_d,
                 math.degrees(e_s), m_s))

    # ---- hinh: goc mat troi vs goc bam ngay 21/6 ----
    ts, ideal, tracked = [], [], []
    rho = 0.0
    t = 5.5
    while t <= 18.5:
        s = sun_vec(172, t)
        if s and s[3] > math.radians(8):
            rs = rho_star(s)
            L1, L2 = ldr_pair(rs - rho, 1.03, 1.0, 0.10 * math.cos(rs - rho))
            dh = delta_hat(L1, L2)
            if abs(dh) > math.radians(1.0):
                rho += dh
            ts.append(t)
            ideal.append(math.degrees(rs))
            tracked.append(math.degrees(rho))
        t += 5.0 / 60.0
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 7), dpi=200, sharex=True)
    fig.patch.set_facecolor("#eef2f9")
    for a in (a1, a2):
        a.set_facecolor("#eef2f9")
    a1.plot(ts, ideal, color="#1f3864", lw=2, label="Góc Mặt Trời lý tưởng ρ*")
    a1.plot(ts, tracked, color="#2e7d32", lw=1.6, ls="--",
            label="Góc tấm pin (phương pháp ma trận LDR)")
    a1.set_ylabel("Góc quay (độ)")
    a1.legend(fontsize=8.5, loc="lower center")
    a1.grid(alpha=.3)
    a1.set_title("Ngày 21/6 tại Mỹ Hào, Hưng Yên: bám sát góc lý tưởng không cần quay theo thời gian")
    err = [abs(i - k) for i, k in zip(ideal, tracked)]
    a2.fill_between(ts, err, color="#c62828", alpha=.35)
    a2.plot(ts, err, color="#c62828", lw=1.2)
    a2.set_ylabel("Sai số |ρ* − ρ| (độ)")
    a2.set_xlabel("Giờ mặt trời")
    a2.grid(alpha=.3)
    a2.set_ylim(0, max(3, max(err) * 1.2))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "ket_qua_mo_phong_1_truc.png"),
                facecolor="#eef2f9", bbox_inches="tight")
    plt.close(fig)
    print("da ve: ket_qua_mo_phong_1_truc.png")

    with open(os.path.join(ROOT, "hinh_ve", "ket_qua_mo_phong.json"), "w") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print("da ghi: hinh_ve/ket_qua_mo_phong.json")


if __name__ == "__main__":
    main()
