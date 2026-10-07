# -*- coding: utf-8 -*-
"""Thông số gốc dùng chung cho sáu quyển và các mô phỏng.

Quy ước được chốt trước khi sinh báo cáo; giá trị cơ khí/điện chưa được đo
được ghi rõ là giả thiết hoặc giới hạn thiết kế.
"""
from __future__ import annotations

import math
from datetime import date

SPEC_VERSION = "1.0"
SPEC_DATE = "07/10/2026"
PLAN_DATE = "10/10/2026"
LATITUDE_DEG = 20.93
LONGITUDE_DEG = 106.10       # kinh độ tham chiếu gần Mỹ Hào, cần xác nhận tại nơi lắp
TIMEZONE_HOURS = 7            # giờ dân dụng Việt Nam, UTC+7
DAYS = (("21/3", 80), ("21/6", 172), ("23/9", 266), ("21/12", 355))

ADC_BITS = 12
ADC_MAX = (1 << ADC_BITS) - 1
LDR_PINS = (25, 26, 27, 14)  # ET, WT, EB, WB; ESP32 ADC2
POT_AZ_PIN = 36
POT_TILT_PIN = 4              # thay GPIO2 là chân strapping
PANEL_VOLTAGE_PIN = 39
AZ_FORWARD_PIN, AZ_REVERSE_PIN = 19, 18
TILT_UP_PIN, TILT_DOWN_PIN = 16, 13
LIMIT_PINS = (34, 35, 32, 33) # AZ+, AZ-, beta+, beta-
ESTOP_PIN = 23                # NC-to-GND, INPUT_PULLUP; mức HIGH là dừng/lỗi dây
I2C_SDA_PIN, I2C_SCL_PIN = 21, 22

N_SAMPLE = 16
TRIM_EACH_END = 2
START_THRESHOLD = 200
STOP_DEADBAND = 120
S_MIN = 2500
LIGHT_POLL_SECONDS = 1       # ngưỡng sáng an toàn, không phát lệnh chỉnh góc
LDR_PERIOD_SECONDS = 120     # chu kỳ hiệu chỉnh theo e1/e2
ASTRO_PERIOD_SECONDS = 1800
LCD_PERIOD_SECONDS = 1
T_CMD_MAX_MS = 8000
T_POLL_MS = 10
BREAK_BEFORE_MAKE_MS = 25

AZIMUTH_LIMIT_DEG = (-120.0, 120.0)
AZIMUTH_APPROACH_DEG = 60.0
ONE_AXIS_LIMIT_DEG = (-85.0, 85.0)
TILT_LIMIT_DEG = (0.0, 75.0)   # beta = cao độ pháp tuyến đo từ ngang, không phải nghiêng mặt pin

AIR_DENSITY_KG_M3 = 1.2
DRAG_COEFFICIENT = 1.2
PANEL_AREA_M2 = 0.65
AZ_LEVER_M = 0.30
TILT_LEVER_M = 0.20
TILT_RESIDUAL_GRAVITY_NM = 3.0
WIND_SAFETY_FACTOR = 1.5
ASSUMED_STALL_TORQUE_NM = 20.0 # giả thiết, chưa xác minh; không phải mô-men liên tục
MOTOR_LABEL_W = 60.0           # chỉ dùng 60 W/12 V nếu nhãn được xác nhận
MOTOR_VOLTAGE_V = 12.0


def _rad(degrees: float) -> float:
    return math.radians(degrees)


def day_of_year(value: date | int) -> int:
    """Trả số thứ tự ngày trong năm; nhận datetime.date hoặc số ngày đã có."""
    if isinstance(value, int):
        return value
    return value.timetuple().tm_yday


def equation_of_time_minutes(n: int) -> float:
    """Xấp xỉ phương trình thời gian NOAA, phút."""
    B = _rad(360.0 * (n - 81) / 364.0)
    return 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)


def solar_time_hours(civil_hour: float, n: int,
                     longitude_deg: float = LONGITUDE_DEG,
                     timezone_hours: int = TIMEZONE_HOURS) -> float:
    """Đổi giờ dân dụng sang giờ Mặt Trời theo kinh độ và Equation of Time.

    Kết quả có thể nhỏ hơn 0 hoặc lớn hơn 24 gần nửa đêm; các phép tính góc
    dùng sin/cos nên vẫn đúng chu kỳ. Gọi với ngày địa phương của RTC.
    """
    correction_min = 4.0 * (longitude_deg - 15.0 * timezone_hours) + equation_of_time_minutes(n)
    return civil_hour + correction_min / 60.0


def wrap_azimuth_deg(value: float) -> float:
    """Chuẩn hóa về (-180, 180], tuyệt đối không gập mất nhánh 180 độ."""
    wrapped = (value + 180.0) % 360.0 - 180.0
    return 180.0 if math.isclose(wrapped, -180.0, abs_tol=1e-10) else wrapped


def solar_angles(n: int, solar_hour: float,
                 latitude_deg: float = LATITUDE_DEG) -> tuple[float, float]:
    """(alpha, gamma) theo alpha từ chân trời, gamma Nam=0 và Tây dương."""
    delta = _rad(23.45 * math.sin(_rad(360.0 * (284 + n) / 365.0)))
    hour_angle = _rad(15.0 * (solar_hour - 12.0))
    latitude = _rad(latitude_deg)
    sin_alpha = (math.sin(latitude) * math.sin(delta) +
                 math.cos(latitude) * math.cos(delta) * math.cos(hour_angle))
    sin_alpha = max(-1.0, min(1.0, sin_alpha))
    alpha = math.degrees(math.asin(sin_alpha))
    gamma = math.degrees(math.atan2(
        math.sin(hour_angle),
        math.cos(hour_angle) * math.sin(latitude) - math.tan(delta) * math.cos(latitude),
    ))
    return alpha, wrap_azimuth_deg(gamma)


def sun_vector(n: int, solar_hour: float,
               latitude_deg: float = LATITUDE_DEG) -> tuple[float, float, float]:
    """Đơn vị véc-tơ Mặt Trời: x Tây, y Bắc, z lên."""
    alpha, gamma = map(_rad, solar_angles(n, solar_hour, latitude_deg))
    return (math.cos(alpha) * math.sin(gamma),
            -math.cos(alpha) * math.cos(gamma),
            math.sin(alpha))


def beta_command(alpha_deg: float) -> float:
    """Khớp nghiêng lấy beta từ ngang; không dùng 90°-alpha."""
    lo, hi = TILT_LIMIT_DEG
    return min(hi, max(lo, alpha_deg))


def azimuth_limit_target(gamma_raw: float, current: float,
                         latched: bool = False) -> tuple[float, bool, str]:
    """Giới hạn gamma cơ khí: một lần tiếp cận biên gần, rồi latch tới đêm."""
    low, high = AZIMUTH_LIMIT_DEG
    if latched:
        return float(current), True, "latched"
    if low <= gamma_raw <= high:
        return float(gamma_raw), False, "track"
    boundary = low if gamma_raw < low else high
    if abs(boundary - current) <= AZIMUTH_APPROACH_DEG:
        return float(boundary), True, "approach-boundary"
    return float(current), True, "hold-before-boundary"


def hysteresis_track(error: float, active: bool = False) -> bool:
    """Hysteresis: enter tracking at START, remain active until STOP deadband."""
    magnitude = abs(error)
    if not active and magnitude >= START_THRESHOLD:
        return True
    if active and magnitude <= STOP_DEADBAND:
        return False
    return active


def wind_torque(speed_m_s: float, two_axis: bool = False) -> dict[str, float]:
    """Mô-men thiết kế tham khảo từ tải gió; mọi hình học đều là giả thiết."""
    q = 0.5 * AIR_DENSITY_KG_M3 * speed_m_s ** 2
    force = q * DRAG_COEFFICIENT * PANEL_AREA_M2
    az = WIND_SAFETY_FACTOR * force * AZ_LEVER_M
    result = {
        "speed_m_s": float(speed_m_s),
        "dynamic_pressure_pa": q,
        "force_n": force,
        "azimuth_design_nm": az,
        "azimuth_ratio_assumed": ASSUMED_STALL_TORQUE_NM / az,
    }
    if two_axis:
        tilt = WIND_SAFETY_FACTOR * (force * TILT_LEVER_M + TILT_RESIDUAL_GRAVITY_NM)
        result["tilt_design_nm"] = tilt
        result["tilt_ratio_assumed"] = ASSUMED_STALL_TORQUE_NM / tilt
    return result


def wind_table(two_axis: bool = False) -> list[dict[str, float]]:
    return [wind_torque(v, two_axis) for v in (6.0, 8.0, 10.0)]


def common_spec_rows() -> list[tuple[str, str]]:
    return [
        ("Quy ước dấu", "x dương về Tây; H dương sau giờ Mặt Trời 12h. beta là cao độ của pháp tuyến tấm pin đo từ mặt phẳng ngang (không phải độ nghiêng của mặt phẳng pin); mặt pin nghiêng 90°−beta so với ngang."),
        ("Phương vị", "gamma=0° hướng Nam; gamma>0 về Tây, gamma<0 về Đông; giữ atan2 trong (-180°,180°]. Khớp azimuth giới hạn ±120° (giả thiết)."),
        ("Hai trục", "alpha là cao độ Mặt Trời; beta là cao độ pháp tuyến tấm pin đo từ mặt phẳng ngang (mặt phẳng pin nghiêng 90°−beta), nên beta lý tưởng=alpha và beta_cmd=clamp(alpha,0°…75°). Gamma thô không gập qua ±90°; vượt ±120° thì chỉ tiếp cận biên nếu cách <=60° ở lần đầu, sau đó latch đến đêm."),
        ("Bốn LDR / sai lệch", "ET, WT, EB, WB: e1=(ET+EB)-(WT+WB) (Đông-Tây); e2=(ET+WT)-(EB+WB) (trên-dưới). e1<0 yêu cầu quay Tây; e2>0 yêu cầu nâng."),
        ("Lấy mẫu/lọc", "Mỗi kênh lấy 16 mẫu ADC 12-bit; bỏ 2 mẫu thấp nhất và 2 cao nhất, trung bình 12 mẫu còn lại. K_cal chưa hiệu chuẩn: tạm dùng 1,0."),
        ("Dải ADC / pin", "Mã 0…4095, điện áp chân <=3,3 V. LDR ET/WT/EB/WB: GPIO25/26/27/14 (ADC2, tắt Wi-Fi); biến trở azimuth GPIO36; biến trở nghiêng GPIO4 (không dùng GPIO2 vì strap lúc khởi động); đo áp pin GPIO39. GPIO34–39 chỉ input và không có pull-up/down nội; limit GPIO34/35 cần điện trở bias ngoài."),
        ("Ngưỡng / vùng chết", "Bắt đầu lệnh khi |e|>=200 count; dừng khi |e|<=120 count (hysteresis); S_min=2500 count tổng bốn kênh là ngưỡng sơ bộ, cần hiệu chuẩn."),
        ("Động cơ", "Một trục: 1 motor gạt mưa 12 V trục vít cho phương vị. Hai trục: thêm 1 motor cùng loại cho nâng. Nhãn 60 W chưa xác minh; chưa có mô-men/dòng đo."),
        ("Tải gió / tay đòn", "Giả thiết: A=0,65 m²; rho=1,2 kg/m³; Cd=1,2; r_az=0,30 m; r_tilt=0,20 m; mô-men trọng lực dư nghiêng 3 N·m; hệ số thiết kế 1,5. Chưa kiểm chứng CAD/đo lực."),
        ("Chu kỳ / giới hạn lệnh", "Kiểm tra tổng sáng 1 giây để khóa khi thiếu sáng; hiệu chỉnh góc theo LDR 2 phút; cập nhật thiên văn 30 phút; LCD 1 giây (timer độc lập). Motor kiểm tra hồi tiếp/limit mỗi 10 ms, lệnh tối đa 8 s; break-before-make 25 ms khi đảo chiều. Chưa thử phần cứng."),
        ("Cầu H / E-stop", "AZ_THUAN/AZ_NGUOC (GPIO19/18), thêm TILT_LEN/TILT_XUONG (16/13); opto active-low: LOW/HIGH chạy, HIGH/HIGH khóa, LOW/LOW cấm. GPIO5 tránh. E-stop GPIO23: NC kéo GND, bình thường LOW; nhấn/đứt dây HIGH; cần liên động cắt nguồn/enable phần cứng, chưa xác minh."),
        ("Dòng motor", "Nếu nhãn 60 W/12 V là công suất điện vào: khoảng 5 A/motor; một trục 1 motor, hai trục 2 motor (ước lượng 10 A tổng). Chưa đo dòng khởi động/kẹt. TIP41C 6 A max không chứng minh mạch đủ tải."),
        ("RTC/LCD", "DS1307 0x68: đọc 7 thanh ghi BCD 0x00…0x06; kiểm tra ACK, đủ byte, CH, 24-hour và miền ngày/giờ. RTC lưu giờ dân dụng Việt Nam; dùng UTC+7, lambda tham chiếu ≈106,10°E và EoT để đổi giờ Mặt Trời. LCD1602/PCF8574 địa chỉ tham khảo 0x27 trên I²C GPIO21/22, cập nhật mỗi 1 giây."),
        ("Trạng thái bằng chứng", "Chỉ tính/mô phỏng phần mềm đã chạy. Chưa xác nhận lắp ráp, hiệu chuẩn, đo dòng/mô-men, thử ngoài trời hoặc kiểm tra trên ESP32/RTC/motor thật; dự kiến hoàn tất trước 10/10/2026."),
    ]


def shared_spec_markdown() -> str:
    lines = [
        "# BẢNG THÔNG SỐ CHUNG – HỆ THỐNG BÁM NẮNG",
        f"Phiên bản {SPEC_VERSION} · lập trước khi hiệu chỉnh sáu quyển · {SPEC_DATE}",
        "",
        "| Hạng mục | Quy ước / giá trị thống nhất |",
        "|---|---|",
    ]
    lines.extend(f"| {key} | {value.replace('|', '/') } |" for key, value in common_spec_rows())
    lines.extend([
        "",
        "**Tải gió tham khảo:** q=0,5 rho V²; F=q·Cd·A; M_az=1,5·F·0,30; M_tilt=1,5·(F·0,20+3). 20 N·m chỉ là mô-men kẹt giả định, không phải kết quả đo hay mô-men liên tục.",
        "",
        "**Mức xác minh:** chưa có phép đo, hiệu chuẩn hoặc thử nghiệm phần cứng được xác nhận. Các giới hạn/giá trị thiết kế phải được xác minh trước khi vận hành.",
        "",
    ])
    return "\n".join(lines)
