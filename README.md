# Báo cáo đồ án bám nắng mặt trời – 6 quyển × 2 đồ án (bản hybrid)

Hai đồ án, mỗi đồ án 3 quyển (**Nghiên cứu – Chế tạo – Lập trình**), đánh số theo
CHƯƠNG, tuần báo cáo **5/10 – 10/10/2026**:

- **Đồ án 1 (một trục)**: Nghiên cứu thuật toán đo cường độ ánh sáng để xác định
  hướng điều khiển tấm pin ứng dụng trong hệ thống pin năng lượng mặt trời.
- **Đồ án 2 (hai trục)**: Nghiên cứu thuật toán điều khiển điều hướng tấm pin
  ứng dụng trong hệ thống pin năng lượng mặt trời (quyển chế tạo nói về cấu trúc 3D).

## Phương pháp: HYBRID (thiên văn + LDR)

- **Nhóm 1 – vòng hở thiên văn**: δ = 23,45°·sin[360°·(284+n)/365]; H = 15°·(t−12);
  sin α = sin φ·sin δ + cos φ·cos δ·cos H; γ tính từ (α, δ, φ). Đọc ngày giờ từ
  **DS1307** để định vị thô mỗi 30 phút.
- **Nhóm 2 – vòng kín LDR**: 4 LDR ở 4 góc có vách che giữa;
  e1 = ADC(trái) − ADC(phải), e2 = ADC(trên) − ADC(dưới); |e| > ngưỡng thì quay
  motor theo dấu e, ngược lại dừng (vùng chết chống dao động).
- **Nhóm 3 – hybrid (lựa chọn)**: thiên văn định vị thô buổi sáng và mỗi chu kỳ,
  LDR tinh chỉnh khi gần đúng, trời nhiều mây thì giữ vị trí theo lịch.

## Phần cứng thực tế đưa vào báo cáo

ESP32 DevKit (LDR: GPIO25/26/27/14; biến trở GPIO36 (+GPIO2 bản 2 trục); áp tấm
pin GPIO39; hành trình qt1–qt4 GPIO34/35/32/33; lệnh motor GPIO19/18 (+5/13);
I²C GPIO21/22) • **mạch động lực cầu H 4 TIP41C** + diode bảo vệ, lệnh tích cực
thấp qua **opto PC817** • **motor gạt nước 12 V trục vít tự hãm** • **DS1307**
(I²C 0x68) • **LCD 1602 + PCF8574** (0x27) hiển thị giờ và góc • nguồn 12 V qua
1N4007, LM2596 3,3 V và 7805 5 V • tấm pin **100 W – 4 kg** (bảng tính chọn động
cơ đã tính lại). ADC chỉ đo điện áp, chưa đo dòng điện.

## File đầu ra

| File | Nội dung |
|---|---|
| `Bao_cao_{1,2}_truc_Nghien_cuu.docx/.pdf` | Nghiên cứu phương pháp hybrid + mô phỏng trực quan + ma trận tính toán (chương 4) |
| `Bao_cao_{1,2}_truc_Che_tao.docx/.pdf` | Chế tạo: mạch EasyEDA (7 sheet trong `hinh_ve/mach/`), mạch động lực, cơ khí / cấu trúc 3D, tính chọn motor |
| `Bao_cao_{1,2}_truc_Lap_trinh.docx/.pdf` | Lập trình: chương 1 tổng quan, chương 2 Arduino IDE + ESP32 DevKit + nhóm lệnh, chương 3 chế tạo–hiệu chuẩn–đo đạc + phương pháp đọc ADC/điều khiển motor/DS1307/LCD/biến trở + lưu đồ từng phần và tổng quát + code mẫu |
| `Bao_cao_day_du_6_phan.pdf` | Bản gộp cả 6 quyển |

Mỗi báo cáo có **1 file PDF riêng** (`Bao_cao_pdf_*.pdf`) dùng khi không có Word.

## Dựng lại toàn bộ

```bash
pip install python-docx reportlab matplotlib pillow
python3 tools/mo_phong.py      # số liệu + đồ thị trực quan + ket_qua_mo_phong.json
python3 tools/ve_hinh.py       # sơ đồ khối, kết nối, 3 phương pháp, 6 lưu đồ
python3 tools/build_bao_cao.py # 6 file Word
python3 tools/xuat_pdf.py      # 6 PDF riêng + 1 PDF gộp
```

- `tools/trich_xuat.py`: trích nguyên văn Chương 1–2 của hai bản Word gốc cho
  quyển nghiên cứu (riêng mục 2.4/2.5 và 2.9 được thay bằng nội dung hybrid),
  ghép nội dung mới từ `tools/noi_dung_moi_{1,2}_truc.py`, đánh số Hình/Bảng.
- `hinh_ve/mach/`: 7 sheet mạch nguyên lý EasyEDA do sinh viên thiết kế.
- Bản vẽ cơ khí tấm pin đang được vẽ lại, sẽ bổ sung sau.
