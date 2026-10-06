# -*- coding: utf-8 -*-
"""Chen 7 anh ve 3D sinh vien gui vao quyen Che tao do an 2, kem caption + mo ta.

Chay: python3 tools/chen_anh_3d.py   (can co du 7 png trong hinh_ve/ve_3d/)
"""
import os
import sys

from docx import Document
from docx.shared import Inches, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "Bao_cao_2_truc_Che_tao.docx")

FIGS = [
    ("3.1. Cấu trúc 3D", [
        ("toan_canh_truoc.png", 5.6,
         "Hình toàn cảnh mô hình nhìn từ phía trước: tấm pin 100 W bắt trên khung "
         "đà ngang được nâng bởi trụ đứng giữa ba chân đế; động cơ gạt nước phương "
         "vị đặt sát hub chân đế, quay toàn bộ trụ và tấm pin quanh trục thẳng đứng."),
        ("toan_canh_sau.png", 5.6,
         "Nhìn từ phía sau: giá khớp nâng nghiêng kèm động cơ gạt nước thứ hai bắt "
         "ngay lưng tấm pin để chỉnh góc ngẩng; động cơ phương vị ở gốc trụ nối vào "
         "hub chân đế, dây động cơ chạy dọc thân trụ lên hộp điều khiển."),
        ("nhin_ben.png", 4.6,
         "Hình chiếu bên cho thấy tầm nghiêng của tấm pin: càng cua trên đỉnh trụ giữ "
         "trục nâng, tấm pin quay quanh trục ngang gắn vào càng cua; ba chân đế xòe "
         "rộng tạo đế đứng vững và chịu mô-men gió khi tấm pin nghiêng."),
    ]),
    ("3.2. Khớp phương vị", [
        ("chan_ba_va_khop_phuong_vi.png", 4.4,
         "Chân đế ba chân và ổ khớp phương vị: ba chân thép liên kết bằng đai giằng "
         "dưới, hub trên khoan lỗ tròn lồng ổ trục cho trụ quay; các mặt phẳng chuẩn "
         "trong bản vẽ dùng để ràng buộc vị trí khi lắp cụm chân."),
    ]),
    ("3.4. Tính chọn động cơ", [
        ("dong_co_gat_nuoc.png", 5.2,
         "Chi tiết động cơ gạt nước 12 V: thân hộp bánh đúc có ba tai bắt bulông, trục "
         "ra then hoa tự hãm giữ tấm pin không trôi khi ngắt điện; hai cực nguồn dạng "
         "cắm nhanh nối sang mạch cầu H bốn TIP41C."),
    ]),
    ("3.5. Các kết cấu cơ khí", [
        ("cot_va_go_khap_nghieng.png", 3.6,
         "Thân trụ và giá càng cua khớp nâng: đầu trên cột thép có hai tai má kẹp khoan "
         "lỗ đồng tâm cho trục nâng và một tấm ngang bắt thân động cơ; cụm này quyết "
         "định trục quay nâng hạ của tấm pin."),
        ("thanh_da_mang_pin.png", 5.0,
         "Thanh đà mang pin: mác thép gấp mép có lỗ bắt vít vào khung tấm pin ở hai đầu, "
         "chốt xoay giữa đà lồng vào giá càng cua để tấm pin quay đúng tâm khớp nâng "
         "và cân mô-men trọng trường."),
    ]),
]


def main():
    thieu = [t for _, items in FIGS for t, _w, _c in items
             if not os.path.exists(os.path.join(ROOT, "hinh_ve", "ve_3d", t))]
    if thieu:
        print("THIEU ANH:", ", ".join(thieu))
        sys.exit(1)
    d = Document(F)
    if any("toan_canh_truoc" in (p._p.xml or "") for p in []):
        pass
    # tranh chen trung: kiem tra caption dac trung
    for p in d.paragraphs:
        if (p.style.name or "") == "Caption" and "Toàn cảnh mô hình hai trục" in p.text:
            print("DA CHEN TU TRUOC, bo qua.")
            sys.exit(0)

    def find_head(t):
        for p in d.paragraphs:
            if (p.style.name or "").startswith("Heading 2") and p.text.strip().startswith(t):
                return p
        return None

    def next_head_from(p):
        got = False
        for q in d.paragraphs:
            if q is p:
                got = True
                continue
            if got and (q.style.name or "").startswith(("Heading 1", "Heading 2")):
                return q
        return None

    total = 0
    for head_t, items in FIGS:
        h = find_head(head_t)
        if h is None:
            print("! khong thay muc", head_t)
            continue
        nh = next_head_from(h)
        for ten, w, mo_ta in items:
            pi = d.add_paragraph()
            pi.add_run().add_picture(os.path.join("hinh_ve", "ve_3d", ten),
                                     width=Inches(w))
            cp = d.add_paragraph(style="Caption")
            dp = d.add_paragraph(mo_ta)
            nh._p.addprevious(pi._p)
            nh._p.addprevious(cp._p)
            nh._p.addprevious(dp._p)
            total += 1
    n = 0
    for p in d.paragraphs:
        if (p.style.name or "") == "Caption" and p.text.strip().startswith("Hình"):
            n += 1
            rest = p.text.split(". ", 1)[1] if ". " in p.text else p.text
            p.runs[0].text = "Hình %d. %s" % (n, rest)
            for r in p.runs[1:]:
                r._r.getparent().remove(r._r)
            p.runs[0].font.size = Pt(12)
    d.save(F)
    print("da chen %d anh 3D | tong caption Hinh: %d" % (total, n))


if __name__ == "__main__":
    main()
