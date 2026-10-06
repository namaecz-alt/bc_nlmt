# Báo cáo đồ án bám nắng mặt trời – 6 quyển, phương pháp LAI thiên văn + LDR

Kho chứa hai bản báo cáo gốc và **6 file Word + 6 file PDF riêng** (mỗi báo cáo
một PDF) cùng một PDF gộp. Phương pháp điều khiển của bản này là
**phương pháp lai**:

- **Vòng hở thiên văn**: đọc giờ thực từ module **DS1307**, tính xích vĩ δ,
  góc giờ H, góc cao α và phương vị γ từ vĩ độ/kinh độ Mỹ Hào → góc lệnh thô.
- **Vòng kín LDR**: ma trận 4 quang trở có **vách che chữ thập** giữa cụm,
  `e1 = ADC(trái) − ADC(phải)`, `e2 = ADC(trên) − ADC(dưới)`; lệch vượt ngưỡng
  chết 3° thì tinh chỉnh motor một bước.
- **Trời nhiều mây** (tổng sáng dưới ngưỡng): bỏ LDR, giữ vị trí theo lịch
  thiên văn để tránh dao động vô ích.

Phần cứng mô tả đúng theo mạch đã thiết kế trên **EasyEDA**: ESP32 DevKit,
cầu H 4×TIP41C cách ly bằng opto PC817, nguồn LM2596 (3,3 V) và 7805 (5 V),
chống ngược cực 1N4007, công tắc hành trình qt1…qt4 kéo xuống 1k, màn hình
**LCD I²C 1602**, động cơ gạt nước ô tô trục vít tự giữ vị trí. ADC chỉ đo
điện áp, chưa đo dòng điện.

## 1. Sáu báo cáo (mỗi báo cáo 1 file Word + 1 file PDF)

| Báo cáo | File | Nội dung chính |
|---|---|---|
| 1 | `Bao_cao_1_truc_Nghien_cuu` | Chương 2 chỉ còn 3 phương pháp (quang trở / thời gian / lai); Chương 3 kết quả mô phỏng trực quan: ma trận tính toán LDR, sai số ngày nắng/ngày mây, năng lượng so tấm cố định; Chương 4 tiến độ |
| 2 | `Bao_cao_1_truc_Che_tao` | Phương án thiết kế; tính chọn động cơ cho tấm pin 4 kg – 100 W; Chương 3 chế tạo mạch theo EasyEDA (7 sơ đồ), hiệu chuẩn và đo đạc |
| 3 | `Bao_cao_1_truc_Lap_trinh` | Chương 1 tổng quan hệ + Arduino IDE + ESP32 DevKit; Chương 2 nhóm lệnh; Chương 3 đọc ADC, điều khiển động cơ, DS1307, LCD I²C, biến trở góc nghiêng, 5 lưu đồ, code mẫu |
| 4 | `Bao_cao_2_truc_Nghien_cuu` | Như báo cáo 1 cho hệ hai trục (thêm e2, trục nghiêng) |
| 5 | `Bao_cao_2_truc_Che_tao` | Như báo cáo 2 với hai cầu H, bốn opto, bốn hành trình |
| 6 | `Bao_cao_2_truc_Lap_trinh` | Như báo cáo 3 với code hai trục, nghiêng trước – phương vị sau |

Kèm theo: `Bao_cao_day_du_6_phan.pdf` – PDF gộp cả 6 quyển có trang bìa.

## 2. Số liệu mô phỏng (tools/mo_phong.py)

- Ngày nắng: sai số bám thiên văn ≈ 2,6° (lệch lắp đặt), LDR thuần ≈ 0,8°,
  lai ≈ 1,1–1,3°; số lần chạy motor 75 / 86 / 142.
- Ngày nhiều mây: LDR thuần lạc hướng 70–90°, lai giữ 1,6–1,7° theo lịch.
- Năng lượng so tấm cố định nghiêng 21°: lai đạt 157% (21/6) đến 478% (21/12).
- Ma trận tính toán LDR: góc suy ra trùng góc đặt 0–30°, ngưỡng chết e = 0,030.

## 3. Thư mục hỗ trợ

- `hinh_ve/`: sơ đồ khối, sơ đồ kết nối, bố trí LDR có vách che, 5 lưu đồ
  (tổng quát + 4 lưu đồ từng phần), 2 đồ thị kết quả mô phỏng.
- `hinh_ve/mach/`: bản vẽ lại 7 khối mạch EasyEDA (cầu H TIP41C, opto PC817,
  hành trình, ESP32, nguồn LM2596, 7805 + LCD, DS1307). Nếu có bản xuất PNG
  gốc từ EasyEDA, đặt trùng tên vào thư mục này rồi dựng lại để thay tự động.
- `tools/mo_phong.py`: mô phỏng ba phương pháp (thiên văn / LDR / lai).
- `tools/ve_hinh.py`: sinh toàn bộ PNG phong cách bản vẽ kỹ thuật.
- `tools/trich_xuat.py`: trích Chương 1–2 bản gốc (nguyên văn), thay mục
  2.4/2.5 và 2.9 theo phương án mới, vá câu chữ, ghép 6 quyển.
- `tools/noi_dung_moi_1_truc.py`, `tools/noi_dung_moi_2_truc.py`: nội dung mới.
- `tools/build_bao_cao.py`: dựng 6 file `.docx` (có khối code).
- `tools/xuat_pdf.py`: dựng 6 PDF riêng + 1 PDF gộp.

## 4. Dựng lại toàn bộ

```bash
pip install python-docx reportlab matplotlib pillow
python3 tools/mo_phong.py
python3 tools/ve_hinh.py
python3 tools/build_bao_cao.py
python3 tools/xuat_pdf.py
```
