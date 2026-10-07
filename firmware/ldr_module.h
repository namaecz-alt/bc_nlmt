#pragma once
#include <stdint.h>

// Giao diện dữ liệu duy nhất giữa module ADC/LDR (Lập trình 1) và
// bộ điều khiển tích hợp hai trục (Lập trình 2).
struct LdrResult {
  int32_t e1;   // Đông - Tây
  int32_t e2;   // trên - dưới
  int32_t sum;  // tổng bốn kênh đã hiệu chỉnh
};

void initLdrAdc();
LdrResult readLdrMatrix();
bool ldrHasEnoughLight(const LdrResult &result);
bool hysteresisTrack(int32_t error, bool &active);
