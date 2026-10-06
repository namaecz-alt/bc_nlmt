# Báo cáo đồ án bám nắng mặt trời – 6 quyển theo CHƯƠNG (bản kết quả)

Kho này chứa hai bản báo cáo gốc và **6 file Word** được chia ra từ đó
(mỗi bản gốc chia thành 3 quyển: **Nghiên cứu – Chế tạo – Lập trình**).

Bản sửa đổi hiện tại (tuần 5/10 – 10/10/2026) đã chuyển sang **báo cáo kết quả**:

- Cả hai mô hình dùng **ESP32** làm vi điều khiển duy nhất — không còn bo Arduino
  trong mạch (Arduino chỉ còn là môi trường lập trình IDE).
- Phương pháp điều khiển chốt: **đọc ma trận 4 LDR ở bốn góc tấm pin và suy ra
  góc cần quay** theo công thức đóng `Δ = atan(e/tan β_s)` với
  `e = (L_phải − L_trái)/(L_phải + L_trái)` — **không quay theo bước thời gian**.
  Góc đích đọc từ **biến trở hồi tiếp**; vùng chết δ = 3°; β_s = 30°.
- Cơ cấu chấp hành: **động cơ gạt nước ô tô trục vít** — trục vít tự hãm nên
  tấm pin **tự giữ vị trí khi ngắt điện**.
- Quyển nghiên cứu có **Chương 3 kết quả mô phỏng số** (tools/mo_phong.py):
  hiệu suất thu trực xạ cố định/1 trục/2 trục, sai số suy góc Monte Carlo,
  so sánh với luật bám bước theo thời gian.
- Quyển lập trình có **code mẫu ESP32 đầy đủ trong Word** (đọc 4 kênh ADC,
  lọc trung vị 64 mẫu, lập ma trận, suy góc, quay tới góc đích, liên động),
  chương Arduino IDE giải thích **vì sao ESP32 không nạp được trực tiếp**
  và hướng dẫn cài lõi board ESP32 từng bước.
- Mạch chia áp LDR/biến trở do sinh viên tự chế — báo cáo chỉ chốt phương pháp
  đọc ADC và xử lý tín hiệu phía ESP32.
- Mỗi quyển có chương tiến độ: **kết quả đạt được trong tuần 5/10 – 10/10/2026**
  và **các công việc còn lại của tuần này**.

Phần lý thuyết nền (Chương 1, 2 của bản gốc) trong quyển Nghiên cứu vẫn được
trích **nguyên văn, đầy đủ**, chỉ thay đúng các mục 2.4/2.5 (bộ điều khiển,
chấp hành) và vá các câu nhắc tới bo Arduino/servo/quay theo bước cho khớp
phương án chốt; tài liệu tham khảo [8][9][10] được cập nhật tương ứng.

## 1. Sáu file báo cáo

| File | Cấu trúc chương |
|---|---|
| `Bao_cao_1_truc_Nghien_cuu.docx` | Chương 1 Tổng quan; Chương 2 Lý thuyết & linh kiện (2.4 ESP32, 2.5 motor gạt nước); Chương 3 Kết quả mô phỏng; Chương 4 Tiến độ tuần này |
| `Bao_cao_1_truc_Che_tao.docx` | Chương 1 Phương án thiết kế đã chốt; Chương 2 Cơ khí – mạch – vật tư (tính chọn motor); Chương 3 Lắp ráp – hiệu chuẩn – an toàn; Chương 4 Tiến độ |
| `Bao_cao_1_truc_Lap_trinh.docx` | Chương 1 Arduino IDE & cách nạp ESP32; Chương 2 Các nhóm lệnh; Chương 3 Đọc ma trận LDR + suy góc + code mẫu; Chương 4 Tiến độ |
| `Bao_cao_2_truc_Nghien_cuu.docx` | Như bản 1 trục, cho mô hình hai trục (thêm e_nghiêng, kết quả +26,2% đông chí) |
| `Bao_cao_2_truc_Che_tao.docx` | Hai motor gạt nước, hai biến trở hồi tiếp, bốn công tắc hành trình |
| `Bao_cao_2_truc_Lap_trinh.docx` | Code mẫu hai trục (hàm `quayTruc()` dùng chung, nghiêng trước – phương vị sau) |

Các file giữ nguyên style (font, heading, header/footer, bảng biểu) của bản gốc;
listing code dùng style `macro`/`Code Sample` có sẵn trong khuôn.

## 2. Bản PDF (dùng khi không có MS Word)

- `Bao_cao_day_du_6_phan.pdf`: **một file PDF duy nhất** (68 trang) ghép cả 6
  quyển theo thứ tự, có trang bìa và số trang; code hiển thị font Courier.
- Sinh lại: `pip install reportlab pillow matplotlib python-docx && python3 tools/xuat_pdf.py`

## 3. Thư mục hỗ trợ

- `hinh_ve/`: sơ đồ khối ESP32, sơ đồ kết nối chân, mô hình cơ khí motor gạt
  nước, bố trí 4 LDR, lưu đồ ma trận suy góc (1 trục & 2 trục), sơ đồ khối
  chương trình, đồ thị kết quả mô phỏng + `ket_qua_mo_phong.json` (số liệu).
- `tools/mo_phong.py`: mô phỏng số (vị trí Mặt Trời, đáp ứng LDR cos(Δ∓β_s),
  Monte Carlo sai số, vòng kín cả ngày, so sánh với bám bước thời gian).
- `tools/ve_hinh.py`: sinh toàn bộ PNG trong `hinh_ve/`.
- `tools/trich_xuat.py`: trích khối nội dung từ 2 bản Word gốc, thay mục
  2.4/2.5, vá câu chữ theo phương án chốt, ghép 6 quyển, đánh số Hình/Bảng.
- `tools/noi_dung_moi_1_truc.py`, `tools/noi_dung_moi_2_truc.py`: nội dung mới
  (kết quả mô phỏng, chế tạo, lập trình, code mẫu, tiến độ tuần này).
- `tools/build_bao_cao.py`: dựng 6 file `.docx` (có khối `code`).

## 4. Dựng lại toàn bộ

```bash
pip install python-docx reportlab matplotlib pillow
python3 tools/mo_phong.py      # so lieu + do thi ket qua
python3 tools/ve_hinh.py       # ve lai cac PNG
python3 tools/build_bao_cao.py # 6 file Word
python3 tools/xuat_pdf.py      # 1 file PDF gop
```
