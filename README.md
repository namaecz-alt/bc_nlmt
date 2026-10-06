# Báo cáo đồ án bám nắng mặt trời – bản chia 3 quyển theo CHƯƠNG

Kho này chứa hai bản báo cáo gốc và **6 file Word** được chia ra từ đó
(mỗi bản gốc chia thành 3 quyển: **Nghiên cứu – Chế tạo – Lập trình**).
Nội dung gốc (Chương 1, 2, 3 của bản Word mẫu) được **trích nguyên văn, đầy đủ**,
không viết tóm lược; phần viết thêm mới là thiết kế chi tiết, môi trường lập trình,
các nhóm lệnh và tiến độ tuần. Mỗi quyển đánh số chương riêng (CHƯƠNG 1, 2, 3…
với mục x.y và x.y.z), kèm danh mục tài liệu tham khảo ở cuối.

## 1. Sáu file báo cáo

| File | Cấu trúc chương |
|---|---|
| `Bao_cao_1_truc_Nghien_cuu.docx` | Chương 1 Tổng quan đề tài; Chương 2 Cơ sở lý thuyết & linh kiện (nguyên văn); Chương 3 Tiến độ |
| `Bao_cao_1_truc_Che_tao.docx` | Chương 1 Phương án thiết kế hệ thống (nguyên văn 3.1–3.3 + hình); Chương 2 Cơ khí, mạch điện, vật tư; Chương 3 Lắp ráp, hiệu chuẩn, an toàn (+nguyên văn 3.6); Chương 4 Tiến độ |
| `Bao_cao_1_truc_Lap_trinh.docx` | Chương 1 Môi trường lập trình Arduino/ESP32; Chương 2 Các nhóm lệnh cơ bản; Chương 3 Tổ chức chương trình + thuật toán (nguyên văn 3.4, 3.5) + lưu đồ; Chương 4 Tiến độ |
| `Bao_cao_2_truc_Nghien_cuu.docx` | Như bản 1 trục, cho mô hình hai trục (Arduino Mega) |
| `Bao_cao_2_truc_Che_tao.docx` | Chương 1 (nguyên văn 3.1–3.4, 3.6); Chương 2–4 như trên |
| `Bao_cao_2_truc_Lap_trinh.docx` | Chương 1–2 môi trường + nhóm lệnh; Chương 3 thuật toán so sánh điện trở 4 LDR (nguyên văn 3.5) + lưu đồ; Chương 4 Tiến độ |

Mỗi quyển đều có mục **“Tiến độ thực hiện và kế hoạch tuần tới
(12/10 – 18/10/2026)”** gồm *các công việc đã làm được* và *các công việc sẽ làm
trong tuần tới*. Muốn đổi mốc tuần hoặc bổ sung đầu việc, sửa trong
`tools/noi_dung_moi_1_truc.py` / `noi_dung_moi_2_truc.py` rồi dựng lại.

Các file giữ nguyên style (font, heading, header/footer, bảng biểu) của bản gốc
vì được sinh ra từ chính bản gốc làm khuôn mẫu.

## 2. Bản PDF (dùng khi không có MS Word)

- `Bao_cao_day_du_6_phan.pdf`: **một file PDF duy nhất** ghép cả 6 quyển theo thứ tự,
  có trang bìa liệt mục lục và số trang ở chân trang.
- Sinh lại bằng: `pip install reportlab pillow matplotlib && python3 tools/xuat_pdf.py`
  (script dùng chung nguồn nội dung với bản Word, font DejaVu Serif hỗ trợ tiếng Việt).

## 3. Thư mục hỗ trợ

- `hinh_ve/`: sơ đồ khối, sơ đồ kết nối chân, mô hình cơ khí, bố trí 4 LDR,
  sơ đồ khối chương trình và lưu đồ thuật toán (PNG, chữ tiếng Việt đầy đủ).
- `tools/trich_xuat.py`: trích nguyên văn khối nội dung từ 2 bản Word gốc,
  đánh số lại chương và ghép với nội dung mới thành 6 quyển.
- `tools/noi_dung_moi_1_truc.py`, `tools/noi_dung_moi_2_truc.py`: nội dung viết mới
  (thiết kế chi tiết, môi trường lập trình, nhóm lệnh, tiến độ).
- `tools/ve_hinh.py`: vẽ toàn bộ hình trong `hinh_ve/` bằng matplotlib.
- `tools/build_bao_cao.py`: dựng 6 file `.docx` từ bản gốc + nội dung + hình vẽ.
- `tools/xuat_pdf.py`: xuất 1 file PDF gộp cả 6 quyển.

## 4. Dựng lại từ đầu

```bash
pip install python-docx matplotlib reportlab pillow
python3 tools/ve_hinh.py        # vẽ lại hình trong hinh_ve/
python3 tools/build_bao_cao.py  # sinh lại 6 file Word
python3 tools/xuat_pdf.py       # sinh lại file PDF gộp
```

## 5. File gốc

- `Bao_cao_do_an_mau_bam_nang_1_truc.docx` – bản gốc mô hình một trục.
- `bao_cao_mau_do_an_dieu_khien_bam_mat_troi.docx` – bản gốc mô hình hai trục.
- `Luu_do_thuat_toan_bam_nang_4_LDR.png` – lưu đồ thuật toán hai trục (dùng lại ở quyển lập trình bản 2 trục).
