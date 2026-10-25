/*
 * =====================================================================================
 * ĐỒ ÁN CƠ ĐIỆN TỬ - HỆ THỐNG PIN NĂNG LƯỢNG MẶT TRỜI BÁM NẮNG 2 TRỤC (DUAL-AXIS TRACKER)
 * CHƯƠNG TRÌNH 1: ĐIỀU KHIỂN 2 ĐỘNG CƠ SERVO SG90
 * Màn hình: LCD 1602 I2C (16 cột x 2 dòng) - Chỉ hiển thị điện áp 4 quang trở (1 số lẻ)
 * Vi điều khiển: ESP32 DevKit (38 chân)
 * 
 * PHÂN BỔ CHÂN (PINOUT):
 * 1. Cụm 4 cảm biến quang trở (LDR) - Cầu phân áp với trở 10k:
 *    - GPIO 32: LDR 1 - Trên - Trái  (Top-Left  - TL)
 *    - GPIO 33: LDR 2 - Trên - Phải  (Top-Right - TR)
 *    - GPIO 34: LDR 3 - Dưới - Trái  (Bottom-Left  - BL) [Input-only ADC1]
 *    - GPIO 35: LDR 4 - Dưới - Phải  (Bottom-Right - BR) [Input-only ADC1]
 * 
 * 2. Động cơ Servo SG90 (Điều khiển góc 0 - 180 độ):
 *    - GPIO 19: Servo 1 (sv1) - Điều khiển trục ngang (Horizontal / Azimuth / Trái - Phải)
 *    - GPIO 18: Servo 2 (sv2) - Điều khiển trục đứng (Vertical / Elevation / Lên - Xuống)
 * 
 * 3. Màn hình LCD 1602 qua giao tiếp I2C:
 *    - GPIO 21: SDA | GPIO 22: SCL (Tự động nhận diện 0x27 / 0x3F + I2C Timeout chống treo)
 * =====================================================================================
 */

#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ESP32Servo.h>

// ===================== CẤU HÌNH CHÂN =====================
const int PIN_LDR_TL = 33;  // LDR 1: Trên - Trái
const int PIN_LDR_TR = 32;  // LDR 2: Trên - Phải
const int PIN_LDR_BL = 34;  // LDR 3: Dưới - Trái
const int PIN_LDR_BR = 35;  // LDR 4: Dưới - Phải

const int PIN_SERVO_H = 19; // sv1: Trục ngang (Horizontal - Azimuth)
const int PIN_SERVO_V = 18; // sv2: Trục đứng  (Vertical - Elevation)

const int PIN_LED_ONBOARD = 2; // LED báo trạng thái ESP32 (GPIO 2)

// ===================== CẤU HÌNH ĐẢO CHIỀU SERVO =====================
const bool INVERT_SERVO_H = true; // true: Đảo chiều quay trục ngang
const bool INVERT_SERVO_V = false; // true: Đảo chiều quay trục đứng

// ===================== KHỞI TẠO ĐỐI TƯỢNG LCD 1602 (16x2) & SERVO =====================
LiquidCrystal_I2C lcd27(0x27, 16, 2);
LiquidCrystal_I2C lcd3F(0x3F, 16, 2);
LiquidCrystal_I2C* lcd = &lcd27;
bool lcdFound = false;

Servo servoH; // sv1 - Trục ngang
Servo servoV; // sv2 - Trục đứng

// ===================== THAM SỐ THUẬT TOÁN =====================
const float TOLERANCE_H = 0.08;     // Vùng chết trục ngang: 80 mV (0.08V)
const float TOLERANCE_V = 0.08;     // Vùng chết trục đứng:  80 mV (0.08V)
const float DARK_THRESHOLD = 0.25;  // Ngưỡng phát hiện trời tối (Volt)

// Giới hạn góc an toàn (độ)
const int LIMIT_H_MIN = 10;
const int LIMIT_H_MAX = 170;
const int LIMIT_V_MIN = 15;
const int LIMIT_V_MAX = 165;

int angleH = 90;
int angleV = 90;
const int STEP_SIZE = 1;

// Chu kỳ thời gian (ms)
unsigned long lastControlTime = 0;
const unsigned long CONTROL_INTERVAL = 40;  // 40ms cập nhật servo 1 lần

unsigned long lastLcdTime = 0;
const unsigned long LCD_INTERVAL = 400;     // 400ms cập nhật LCD 1602 1 lần

unsigned long lastSerialTime = 0;
const unsigned long SERIAL_INTERVAL = 2500; // 2.5s in Serial 1 lần

float K_cal[4] = {1.00, 1.00, 1.00, 1.00}; // Cân chỉnh [TL, TR, BL, BR]

// ===================== HÀM KHỞI TẠO I2C LCD 1602 CÓ TIMEOUT =====================
void initI2CSafe() {
    Serial.println("\n[1/3] Kiem tra ket noi I2C LCD 1602 (SDA=21, SCL=22)...");
    pinMode(21, INPUT_PULLUP);
    pinMode(22, INPUT_PULLUP);
    
    Wire.begin(21, 22);
    Wire.setClock(100000);
    Wire.setTimeOut(25); // Timeout 25ms chống treo vi điều khiển
    delay(50);

    Wire.beginTransmission(0x27);
    byte err27 = Wire.endTransmission();

    Wire.beginTransmission(0x3F);
    byte err3F = Wire.endTransmission();

    if (err27 == 0) {
        lcd = &lcd27;
        lcdFound = true;
        Serial.println("  -> TIM THAY LCD 1602 TAI DIA CHI: 0x27 (PCF8574T)");
    } else if (err3F == 0) {
        lcd = &lcd3F;
        lcdFound = true;
        Serial.println("  -> TIM THAY LCD 1602 TAI DIA CHI: 0x3F (PCF8574AT)");
    } else {
        lcdFound = false;
        Serial.println("  -> [CANH BAO]: CHUA TIM THAY LCD 1602 TREN BUS I2C!");
        Serial.println("     Kiem tra 4 day LCD (VCC 5V, GND, SDA 21, SCL 22) va bien tro xanh duong.");
    }

    if (lcdFound) {
        lcd->init();
        lcd->backlight();
        lcd->clear();
        lcd->setCursor(0, 0);
        lcd->print("SOLAR TRACKER 2X");
        lcd->setCursor(0, 1);
        lcd->print("ESP32 SAN SANG..");
        delay(800);
        lcd->clear();
    }
}

// ===================== HÀM ĐỌC ADC VÀ TÍNH ĐIỆN ÁP =====================
float readVoltageOnly(int pin, int samples = 16) {
    long sum = 0;
    int rawArray[16];
    
    for (int i = 0; i < samples; i++) {
        rawArray[i] = analogRead(pin);
        sum += rawArray[i];
        delayMicroseconds(60);
    }
    
    int avgRaw = sum / samples;
    long refinedSum = 0;
    int validCount = 0;
    
    for (int i = 0; i < samples; i++) {
        if (abs(rawArray[i] - avgRaw) * 4 < avgRaw) { // Lọc bỏ mẫu lệch > 25%
            refinedSum += rawArray[i];
            validCount++;
        }
    }
    
    int finalRaw = (validCount > 0) ? (refinedSum / validCount) : avgRaw;
    float volt = ((float)finalRaw * 3.3f) / 4095.0f;
    return volt;
}

// ===================== THIẾT LẬP BAN ĐẦU (SETUP) =====================
void setup() {
    Serial.begin(115200);
    
    pinMode(PIN_LED_ONBOARD, OUTPUT);
    digitalWrite(PIN_LED_ONBOARD, HIGH);

    delay(1000);

    Serial.println("\n");
    Serial.println("*******************************************************************************");
    Serial.println("   DO AN CO DIEN TU - BAN NANG MAT TROI 2 TRUC SERVO SG90 (LCD 1602 I2C)       ");
    Serial.println("   ESP32 DevKit | 4 Quang tro (32-35) | 2 Servo SG90 (sv1: 19, sv2: 18)        ");
    Serial.println("   [LCD 1602: Chi hien thi dien ap 4 quang tro - Lay 1 chu so sau dau phay]    ");
    Serial.println("*******************************************************************************");

    // 1. Cấu hình ADC ESP32
    Serial.println("[1/3] Cau hinh bo doc ADC 12-bit (GPIO 32, 33, 34, 35)...");
    analogReadResolution(12);
    analogSetPinAttenuation(PIN_LDR_TL, ADC_11db);
    analogSetPinAttenuation(PIN_LDR_TR, ADC_11db);
    analogSetPinAttenuation(PIN_LDR_BL, ADC_11db);
    analogSetPinAttenuation(PIN_LDR_BR, ADC_11db);

    // 2. Khởi tạo I2C LCD 1602 có bảo vệ chống treo
    initI2CSafe();

    // 3. Khởi tạo 2 Servo SG90
    Serial.println("[2/3] Khoi tao 2 dong co Servo SG90 (sv1: chan 19, sv2: chan 18)...");
    servoH.setPeriodHertz(50);
    servoH.attach(PIN_SERVO_H, 500, 2400); // sv1 - chân 19

    servoV.setPeriodHertz(50);
    servoV.attach(PIN_SERVO_V, 500, 2400); // sv2 - chân 18

    servoH.write(angleH);
    servoV.write(angleV);
    
    Serial.println("===> KHOI DONG HOAN TAT! BAT DAU VONG LAP DIEU KHIEN...");
    Serial.println("*******************************************************************************\n");
    digitalWrite(PIN_LED_ONBOARD, LOW);
}

// ===================== VÒNG LẶP CHÍNH (LOOP) =====================
void loop() {
    unsigned long currentMillis = millis();

    digitalWrite(PIN_LED_ONBOARD, (currentMillis / 500) % 2 == 0);

    // 1. ĐỌC ĐIỆN ÁP (V) TẠI 4 VỊ TRÍ CẢM BIẾN
    float vTL = readVoltageOnly(PIN_LDR_TL) * K_cal[0]; // Trên - Trái
    float vTR = readVoltageOnly(PIN_LDR_TR) * K_cal[1]; // Trên - Phải
    float vBL = readVoltageOnly(PIN_LDR_BL) * K_cal[2]; // Dưới - Trái
    float vBR = readVoltageOnly(PIN_LDR_BR) * K_cal[3]; // Dưới - Phải

    // 2. TÍNH CÁC THÀNH PHẦN THEO TRỤC ĐỨNG VÀ TRỤC NGANG
    float vTop    = (vTL + vTR) / 2.0f; // Nửa trên
    float vBottom = (vBL + vBR) / 2.0f; // Nửa dưới
    float vLeft   = (vTL + vBL) / 2.0f; // Nửa trái
    float vRight  = (vTR + vBR) / 2.0f; // Nửa phải
    float vAvgAll = (vTop + vBottom) / 2.0f;

    // Sai lệch điện áp
    float diffV = vTop - vBottom; // Trục đứng: Trên - Dưới
    float diffH = vLeft - vRight; // Trục ngang: Trái - Phải

    String statusStr = "CAN BANG [OK]";

    // ================= 3. THUẬT TOÁN ĐIỀU KHIỂN HƯỚNG NẮNG 2 TRỤC =================
    if (currentMillis - lastControlTime >= CONTROL_INTERVAL) {
        lastControlTime = currentMillis;

        if (vAvgAll < DARK_THRESHOLD) {
            statusStr = "TROI TOI (NGHI)";
        } else {
            bool movingV = false;
            bool movingH = false;

            // A. ĐIỀU KHIỂN TRỤC ĐỨNG (sv2 - GPIO 18)
            if (abs(diffV) > TOLERANCE_V) {
                movingV = true;
                if (diffV > 0) {
                    angleV += (INVERT_SERVO_V ? -STEP_SIZE : STEP_SIZE); // Nâng lên
                } else {
                    angleV += (INVERT_SERVO_V ? STEP_SIZE : -STEP_SIZE); // Hạ xuống
                }
                angleV = constrain(angleV, LIMIT_V_MIN, LIMIT_V_MAX);
                servoV.write(angleV);
            }

            // B. ĐIỀU KHIỂN TRỤC NGANG (sv1 - GPIO 19)
            if (abs(diffH) > TOLERANCE_H) {
                movingH = true;
                if (diffH > 0) {
                    angleH += (INVERT_SERVO_H ? -STEP_SIZE : STEP_SIZE); // Quay trái
                } else {
                    angleH += (INVERT_SERVO_H ? STEP_SIZE : -STEP_SIZE); // Quay phải
                }
                angleH = constrain(angleH, LIMIT_H_MIN, LIMIT_H_MAX);
                servoH.write(angleH);
            }

            if (!movingV && !movingH) {
                statusStr = "CAN BANG [OK]";
            } else {
                if (movingV && movingH) statusStr = "CHINH CA 2 TRUC";
                else if (movingV) statusStr = (diffV > 0 ? "NANG TRUC DUNG" : "HA TRUC DUNG");
                else statusStr = (diffH > 0 ? "QUAY SANG TRAI" : "QUAY SANG PHAI");
            }
        }
    }

    // ================= 4. HIỂN THỊ CHỈ ĐIỆN ÁP 4 QUANG TRỞ LÊN LCD 1602 (1 SỐ SAU DẤU PHẨY) =================
    if (lcdFound && (currentMillis - lastLcdTime >= LCD_INTERVAL)) {
        lastLcdTime = currentMillis;

        char line0[17]; // Dòng 1: TL và TR
        char line1[17]; // Dòng 2: BL và BR

        // Định dạng đúng 16 ký tự, lấy 1 chữ số thập phân (ví dụ: "TL:2.4V  TR:2.1V ")
        snprintf(line0, sizeof(line0), "TL:%.1fV  TR:%.1fV ", vTL, vTR);
        snprintf(line1, sizeof(line1), "BL:%.1fV  BR:%.1fV ", vBL, vBR);

        lcd->setCursor(0, 0); lcd->print(line0);
        lcd->setCursor(0, 1); lcd->print(line1);
    }

    // ================= 5. HIỂN THỊ LÊN SERIAL MONITOR (MỖI 2.5 GIÂY) =================
    if (currentMillis - lastSerialTime >= SERIAL_INTERVAL) {
        lastSerialTime = currentMillis;

        Serial.println("-------------------------------------------------------------------------------");
        Serial.printf("[DIEN AP LDR] TL(32): %.1fV  |  TR(33): %.1fV  |  BL(34): %.1fV  |  BR(35): %.1fV\n",
                      vTL, vTR, vBL, vBR);
        Serial.printf("[SAI LECH   ] Truc Dung (dV): %+.2fV  |  Truc Ngang (dH): %+.2fV\n",
                      diffV, diffH);
        Serial.printf("[SERVO SG90 ] sv1-Ngang (GPIO 19): %3d°  |  sv2-Dung (GPIO 18): %3d°\n",
                      angleH, angleV);
        Serial.printf("[TRANG THAI ] LCD 1602: %s  |  Van hanh: %s\n",
                      lcdFound ? "Hoat dong tot" : "CHUA KET NOI (kiem tra day/bien tro)",
                      statusStr.c_str());
        Serial.println("-------------------------------------------------------------------------------");
    }
}
