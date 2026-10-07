# -*- coding: utf-8 -*-
"""Mô phỏng góc, luật điều khiển và proxy hình học cho một/hai trục.

Không phải phép đo, kWh hay mô hình động lực học motor. Đầu ra được lưu ở
hinh_ve/ket_qua_mo_phong.json và các đồ thị PNG.
"""
from __future__ import annotations

import json
import math
import os
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import thong_so_chung as spec

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hinh_ve")
PHI = spec.LATITUDE_DEG
DAYS = spec.DAYS
COLORS = {"21/3": "#2364aa", "21/6": "#ca3c25", "23/9": "#2a9d67", "21/12": "#7451a6"}


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def clamp(value, low, high):
    return min(high, max(low, value))


def sun_vec(day, hour):
    return spec.sun_vector(day, hour)


def panel_normal_1axis(theta_deg):
    theta = math.radians(theta_deg)
    return math.sin(theta), 0.0, math.cos(theta)


def panel_normal_2axis(beta_deg, gamma_deg):
    beta, gamma = math.radians(beta_deg), math.radians(gamma_deg)
    return math.cos(beta) * math.sin(gamma), -math.cos(beta) * math.cos(gamma), math.sin(beta)


def angular_error_deg(day, hour, normal):
    return math.degrees(math.acos(clamp(dot(sun_vec(day, hour), normal), -1.0, 1.0)))


def theta_sun_1axis(day, hour):
    x, _y, z = sun_vec(day, hour)
    return math.degrees(math.atan2(x, z))


def azimuth_limit_target(gamma_raw, current, latched=False):
    return spec.azimuth_limit_target(gamma_raw, current, latched)


def ldr_pair_error(delta_deg, direct_scale=1.0):
    """Tín hiệu tổng hợp East/West; không phải hiệu chuẩn cảm biến."""
    d = math.radians(delta_deg)
    beta_s = math.radians(30.0)
    east = direct_scale * max(0.0, math.cos(d + beta_s))
    west = direct_scale * max(0.0, math.cos(d - beta_s))
    return 3000.0 * (east - west)


def ldr_vertical_error(delta_deg, direct_scale=1.0):
    d = math.radians(delta_deg)
    beta_s = math.radians(30.0)
    top = direct_scale * max(0.0, math.cos(d - beta_s))
    bottom = direct_scale * max(0.0, math.cos(d + beta_s))
    return 3000.0 * (top - bottom)


def solar_matrix(hours=range(6, 19)):
    return {
        name: {str(hour): {"alpha_deg": round(spec.solar_angles(day, float(hour))[0], 2),
                           "gamma_deg": round(spec.solar_angles(day, float(hour))[1], 2)}
               for hour in hours}
        for name, day in DAYS
    }


def two_axis_command_matrix(hours=(7, 9, 11, 12, 13, 15, 17)):
    result = {}
    for name, day in DAYS:
        current, latched = 0.0, False
        result[name] = {}
        for hour in hours:
            alpha, gamma_raw = spec.solar_angles(day, float(hour))
            gamma_cmd, latched, state = spec.azimuth_limit_target(gamma_raw, current, latched)
            if state in ("track", "approach-boundary"):
                current = gamma_cmd
            result[name][str(hour)] = {
                "alpha_deg": round(alpha, 2),
                "beta_cmd_deg": round(spec.beta_command(alpha), 2),
                "gamma_raw_deg": round(gamma_raw, 2),
                "gamma_cmd_deg": round(gamma_cmd, 2),
                "az_state": state,
            }
    return result


def _ldr_sum(daylight, hour):
    # Mô hình tổng sáng có mây tổng hợp, không có dữ liệu ADC thực.
    cloud = 0.08 if 10.0 <= hour < 11.0 else 1.0
    alpha, _ = spec.solar_angles(daylight, hour)
    return max(0.0, math.sin(math.radians(max(alpha, 0.0)))) * 3000.0 * 4 * cloud


def simulate_day(day, mode="hybrid", axes=1, cloudy=(10.0, 11.0), seed=7):
    """Mô phỏng mỗi phút, động cơ tức thời; chỉ dùng để so luật bằng phần mềm."""
    if mode not in ("openloop", "closedloop", "hybrid") or axes not in (1, 2):
        raise ValueError("mode must be openloop/closedloop/hybrid; axes must be 1 or 2")
    rng = random.Random(seed + day + axes)
    track, errors = [], []
    motor_commands = 0
    q1, beta, gamma = 0.0, 0.0, 0.0
    gamma_latched = False
    one_active=az_active=tilt_active=False
    last_astro, last_ldr = -999.0, -999.0
    for minute in range(5 * 60, 19 * 60 + 1):
        hour = minute / 60.0
        alpha, gamma_raw = spec.solar_angles(day, hour)
        lit = alpha > 0.0
        sum_ldr = _ldr_sum(day, hour)
        if cloudy and cloudy[0] <= hour < cloudy[1]:
            sum_ldr *= 0.08
        solar_due = hour - last_astro >= 0.5
        ldr_due = hour - last_ldr >= 2.0 / 60.0

        if not lit or sum_ldr < spec.S_MIN:
            # Ban đêm/thiếu sáng: cầu H khóa, góc hiện tại không đổi.
            pass
        else:
            if mode in ("openloop", "hybrid") and solar_due:
                last_astro = hour
                if axes == 1:
                    target = clamp(theta_sun_1axis(day, hour), *spec.ONE_AXIS_LIMIT_DEG)
                    if abs(target - q1) > 2.0:
                        q1, motor_commands = target, motor_commands + 1
                else:
                    beta_target = spec.beta_command(alpha)
                    gamma_target, gamma_latched, _state = spec.azimuth_limit_target(
                        gamma_raw, gamma, gamma_latched)
                    if abs(beta_target - beta) > 1.0:
                        beta, motor_commands = beta_target, motor_commands + 1
                    if abs(gamma_target - gamma) > 1.0:
                        gamma, motor_commands = gamma_target, motor_commands + 1
            if mode in ("closedloop", "hybrid") and ldr_due:
                last_ldr = hour
                if axes == 1:
                    error_adc = ldr_pair_error(theta_sun_1axis(day, hour) - q1, 1.0)
                    error_adc += rng.gauss(0, 18.0)
                    one_active=spec.hysteresis_track(error_adc,one_active)
                    if one_active:
                        step = clamp(abs(error_adc) / 100.0, 0.5, 4.0)
                        q1 += math.copysign(step, -error_adc)
                        q1 = clamp(q1, *spec.ONE_AXIS_LIMIT_DEG)
                        motor_commands += 1
                else:
                    e_az = ldr_pair_error(gamma_raw - gamma, 1.0) + rng.gauss(0, 18.0)
                    e_tilt = ldr_vertical_error(alpha - beta, 1.0) + rng.gauss(0, 18.0)
                    tilt_active=spec.hysteresis_track(e_tilt,tilt_active)
                    az_active=spec.hysteresis_track(e_az,az_active)
                    if tilt_active:
                        beta += math.copysign(clamp(abs(e_tilt) / 120.0, 0.4, 3.0), e_tilt)
                        beta = clamp(beta, *spec.TILT_LIMIT_DEG)
                        motor_commands += 1
                    if az_active and not gamma_latched:
                        gamma += math.copysign(clamp(abs(e_az) / 120.0, 0.4, 3.0), -e_az)
                        gamma = clamp(gamma, *spec.AZIMUTH_LIMIT_DEG)
                        motor_commands += 1

        active_sun = alpha >= 5.0 and sum_ldr >= spec.S_MIN
        if axes == 1:
            ideal = theta_sun_1axis(day, hour)
            err = abs(ideal - q1)
            track.append((hour, q1, ideal))
        else:
            ideal_normal = sun_vec(day, hour)
            normal = panel_normal_2axis(beta, gamma)
            err = math.degrees(math.acos(clamp(dot(ideal_normal, normal), -1, 1)))
            track.append((hour, beta, gamma, alpha, gamma_raw))
        # Chỉ báo sai số khi mô hình đã ở trên ngưỡng chiếu sáng có thể điều khiển;
        # loại thời điểm rạng/hoàng hôn nằm dưới S_min khỏi metric.
        if active_sun:
            errors.append(err)

    return {
        "day_of_year": day, "mode": mode, "axes": axes,
        "evaluated_steps": len(errors),
        "mean_error_deg": sum(errors) / max(1, len(errors)),
        "max_error_deg": max(errors, default=0.0),
        "motor_commands": motor_commands, "track": track,
        "assumptions": "1-minute time step; synthetic cloud/light/noise; instantaneous actuator; not a hardware test",
    }


def _panel_proxy(day, hour, mode):
    alpha, gamma_raw = spec.solar_angles(day, hour)
    if alpha <= 0:
        return 0.0
    sun = sun_vec(day, hour)
    if mode == "fixed":
        normal = panel_normal_2axis(69.0, 0.0)  # mặt pin nghiêng 21° so với ngang
    elif mode == "1axis":
        theta = clamp(theta_sun_1axis(day, hour), *spec.ONE_AXIS_LIMIT_DEG)
        normal = panel_normal_1axis(theta)
    else:
        beta = spec.beta_command(alpha)
        gamma = clamp(gamma_raw, *spec.AZIMUTH_LIMIT_DEG)
        normal = panel_normal_2axis(beta, gamma)
    return max(0.0, dot(sun, normal))


def day_energy(day, mode, dt_hours=1.0 / 60.0):
    total = 0.0
    steps = round(24.0 / dt_hours)
    for i in range(steps):
        hour = i * dt_hours
        total += _panel_proxy(day, hour, mode) * dt_hours
    return total


def energy_gains():
    result = {}
    for name, day in DAYS:
        fixed = day_energy(day, "fixed")
        one = day_energy(day, "1axis")
        two = day_energy(day, "2axis")
        result[name] = {
            "fixed_proxy_index": fixed, "one_axis_proxy_index": one,
            "two_axis_limited_proxy_index": two,
            "gain_one_axis_percent": (one / fixed - 1) * 100,
            "gain_two_axis_percent": (two / fixed - 1) * 100,
        }
    return result


def calculate_summary():
    controls = {}
    for axes in (1, 2):
        controls[str(axes)] = {}
        for mode in ("openloop", "closedloop", "hybrid"):
            row = simulate_day(80, mode, axes=axes)
            controls[str(axes)][mode] = {k: row[k] for k in
                                          ("mean_error_deg", "max_error_deg", "motor_commands", "assumptions")}
    return {
        "latitude_deg": PHI,
        "longitude_reference_deg": spec.LONGITUDE_DEG,
        "azimuth_convention": "South=0, West positive; atan2 branch preserved",
        "daylight_proxy": energy_gains(),
        "solar_matrix": solar_matrix(),
        "two_axis_commands": two_axis_command_matrix(),
        "controller_model": controls,
    }


def _style_ax(ax):
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_color("#444444")
        spine.set_linewidth(0.8)
    ax.grid(color="#cccccc", lw=0.5, alpha=0.7)
    ax.tick_params(labelsize=8, colors="#222222")


def _save(fig, filename):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, filename)
    fig.savefig(path, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    return path


def plot_solar_path():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.6, 6.2), dpi=190, sharex=True)
    for name, day in DAYS:
        xs, alphas, gammas = [], [], []
        for minute in range(24 * 60):
            hour = minute / 60
            alpha, gamma = spec.solar_angles(day, hour)
            if alpha >= 0:
                xs.append(hour); alphas.append(alpha); gammas.append(gamma)
        a1.plot(xs, alphas, color=COLORS[name], lw=1.3, label=name)
        a2.plot(xs, gammas, color=COLORS[name], lw=1.3, label=name)
    a1.set_ylabel("Cao độ alpha (độ)")
    a2.set_ylabel("gamma (độ; Nam=0, Tây dương)")
    a2.set_xlabel("Giờ Mặt Trời")
    a2.set_ylim(-190, 190)
    a2.axhline(0, color="#777", lw=0.6)
    a1.legend(fontsize=8, frameon=False, ncol=4)
    a1.set_title("Quỹ đạo thiên văn chung tại Mỹ Hào – mô hình hình học, không phải đo")
    for ax in (a1, a2): _style_ax(ax)
    fig.tight_layout()
    _save(fig, "duong_di_mat_troi_1_truc.png")


def plot_energy(gains, axes):
    fig, ax = plt.subplots(figsize=(7.4, 3.8), dpi=190)
    names = [d[0] for d in DAYS]
    key = "gain_one_axis_percent" if axes == 1 else "gain_two_axis_percent"
    vals = [gains[name][key] for name in names]
    color = "#3b78a1" if axes == 1 else "#d8912b"
    bars = ax.bar(names, vals, color=color, edgecolor="#333", lw=0.6)
    for bar, value in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+1,
                f"{value:+.1f}%", ha="center", fontsize=8)
    ax.axhline(0, color="#555", lw=0.7)
    ax.set_ylabel("Proxy trực xạ so với pin cố định (%)")
    ax.set_title(("Một trục" if axes == 1 else "Hai trục, giới hạn beta/gamma") +
                 " – mô phỏng hình học, không phải kWh/đo")
    ax.set_ylim(0, max(vals)*1.25)
    _style_ax(ax); fig.tight_layout()
    _save(fig, f"so_sanh_nang_luong_{axes}_truc.png")


def plot_hybrid(day=80, axes=1):
    result = simulate_day(day, "hybrid", axes=axes)
    fig, ax = plt.subplots(figsize=(7.8, 4.0), dpi=190)
    track = result["track"]
    hours = [row[0] for row in track]
    if axes == 1:
        ax.plot(hours, [r[2] for r in track], label="Góc lý tưởng theta", color="#c3423f", lw=1.2)
        ax.plot(hours, [r[1] for r in track], label="Trục mô phỏng", color="#2364aa", lw=1.35)
        ax.set_ylabel("Góc (độ, Tây dương)")
        ax.set_ylim(-100, 100)
    else:
        ax.plot(hours, [r[3] for r in track], label="alpha thiên văn", color="#c3423f", lw=1.0)
        ax.plot(hours, [r[1] for r in track], label="beta pháp tuyến/khớp nâng (0–75)", color="#2364aa", lw=1.25)
        ax.plot(hours, [r[4] for r in track], label="gamma thô", color="#7a5195", lw=0.9, alpha=0.7)
        ax.plot(hours, [r[2] for r in track], label="gamma khớp cơ khí", color="#d8912b", lw=1.2)
        ax.set_ylabel("Góc (độ)"); ax.set_ylim(-190, 190)
    ax.axvspan(10, 11, color="#bbb", alpha=0.25, lw=0)
    ax.set_xlabel("Giờ Mặt Trời")
    ax.set_title(f"Mô hình hybrid {axes} trục, ngày {day}; mây tổng hợp 10–11h, không phải đo")
    ax.legend(fontsize=7.6, frameon=False, ncol=2)
    _style_ax(ax); fig.tight_layout()
    _save(fig, f"hoat_dong_hybrid_{axes}_truc.png")


def main():
    summary = calculate_summary()
    gains = summary["daylight_proxy"]
    print("=== Proxy hình học trực xạ; không phải kWh hoặc số đo ===")
    for name, row in gains.items():
        print(f"{name}: fixed={row['fixed_proxy_index']:.2f}, 1-axis={row['one_axis_proxy_index']:.2f} "
              f"(+{row['gain_one_axis_percent']:.1f}%), 2-axis={row['two_axis_limited_proxy_index']:.2f} "
              f"(+{row['gain_two_axis_percent']:.1f}%)")
    print("=== Mô phỏng điều khiển ngày 21/3; cloud 10–11h tổng hợp ===")
    for axes in (1, 2):
        for mode in ("openloop", "closedloop", "hybrid"):
            row = summary["controller_model"][str(axes)][mode]
            print(f"{axes}-axis {mode}: mean={row['mean_error_deg']:.3f}, max={row['max_error_deg']:.3f}, "
                  f"commands={row['motor_commands']}")
    plot_solar_path()
    for axes in (1, 2):
        plot_energy(gains, axes)
        plot_hybrid(day=80 if axes == 1 else 172, axes=axes)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "ket_qua_mo_phong.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print("Đã ghi hinh_ve/ket_qua_mo_phong.json")


if __name__ == "__main__":
    main()
