# -*- coding: utf-8 -*-
"""Chen cac anh ve 3D (commit 86b2aa2, thu muc pin_nlmt/) vao Chuong 3 quyen
Che tao do an 2, kem doan mo ta nguyen ly va caption danh so lai.

Chay: python3 tools/chen_anh_3d.py
"""
import os
import shutil
import sys

from docx import Document
from docx.shared import Inches, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "Bao_cao_2_truc_Che_tao.docx")
SRC = os.path.join(ROOT, "pin_nlmt")
DST = os.path.join(ROOT, "hinh_ve", "ve_3d")

# ten file goc (pin_nlmt/) -> ten chuan (hinh_ve/ve_3d/)
CANON = [
    ("toàn bộ cơ cấu.jpg", "toan_canh_truoc.jpg"),
    ("toàn bộ cơ cấu mặt sau.jpg", "toan_canh_sau.jpg"),
    ("giá đỡ động cơ và trục.jpg", "chan_ba_va_khop_phuong_vi.jpg"),
    ("động cơ trục vít.jpg", "dong_co_gat_nuoc.jpg"),
    ("jgb37.jpg", "dong_co_jgb37.jpg"),
    ("kẹp pin năng lượng mặt trời.jpg", "thanh_da_mang_pin.jpg"),
]

MO_TA_MO_DAU = (
    "Cơ cấu bám hai trục được lắp từ ba cụm chính: chân đế ba chân kèm khớp phương "
    "vị ở gốc, thân trụ đứng mang càng cua khớp nâng trên đỉnh, và khung tấm pin bắt "
    "trên thanh đà. Động cơ gạt nước đặt tại gốc trụ quay toàn bộ trụ và tấm pin quanh "
    "trục thẳng đứng để dõi theo hướng nắng trong ngày; động cơ giảm tốc JGB37 gắn "
    "trên càng cua đỉnh trụ chỉnh góc nghiêng tấm pin qua trục nâng theo mùa. Cả hai "
    "động cơ đều có hộp giảm tốc tự hãm nên tấm pin giữ nguyên vị trí khi ngắt điện "
    "hoặc khi gió thổi mạnh."
)

FIGS = [
    ("3.1. Cấu trúc 3D", [
        ("__MO_TA_MO_DAU__", None, None, MO_TA_MO_DAU),
        ("toan_canh_truoc.jpg", 5.6, "Toàn cảnh cơ cấu bám hai trục nhìn từ phía trước",
         "Hình toàn cảnh mô hình nhìn từ phía trước: tấm pin 100 W bắt trên khung đà "
         "ngang được nâng bởi trụ đứng giữa ba chân đế; động cơ gạt nước phương vị "
         "đặt sát hub chân đế, quay toàn bộ trụ và tấm pin quanh trục thẳng đứng."),
        ("toan_canh_sau.jpg", 5.6, "Toàn cảnh cơ cấu bám hai trục nhìn từ phía sau",
         "Nhìn từ phía sau: giá khớp nâng kèm động cơ giảm tốc bắt ngay lưng tấm pin "
         "để chỉnh góc ngẩng; động cơ phương vị ở gốc trụ nối vào hub chân đế, dây "
         "động cơ chạy dọc thân trụ lên hộp điều khiển."),
    ]),
    ("3.2. Khớp phương vị", [
        ("chan_ba_va_khop_phuong_vi.jpg", 4.4, "Chân đế ba chân và ổ khớp phương vị",
         "Chân đế ba chân và ổ khớp phương vị: ba chân thép liên kết bằng đai giằng "
         "dưới, hub trên khoan lỗ tròn lồng ổ trục và bắt giá động cơ phương vị; các "
         "mặt phẳng chuẩn trong bản vẽ dùng để ràng buộc vị trí khi lắp cụm chân."),
    ]),
    ("3.4. Tính chọn động cơ", [
        ("dong_co_gat_nuoc.jpg", 5.2, "Động cơ gạt nước 12 V cho trục phương vị",
         "Động cơ gạt nước 12 V cho trục phương vị: thân hộp bánh đúc có ba tai bắt "
         "bulông, trục ra then hoa tự hãm giữ tấm pin không trôi khi ngắt điện; hai "
         "cực nguồn dạng cắm nhanh nối sang mạch cầu H bốn TIP41C."),
        ("dong_co_jgb37.jpg", 4.6, "Động cơ giảm tốc JGB37 cho trục nâng nghiêng",
         "Động cơ giảm tốc JGB37 cho trục nâng nghiêng: hộp giảm tốc mặt bích tròn có "
         "vòng vít bắt vào giá càng cua, trục ra trơn nối chốt quay của thanh đà; tốc "
         "độ quay thấp, mô-men lớn phù hợp nâng hạ chậm tấm pin nặng khoảng 4 kg."),
    ]),
    ("3.5. Các kết cấu cơ khí", [
        ("thanh_da_mang_pin.jpg", 5.0, "Thanh đà mang tấm pin",
         "Thanh đà mang pin: mác thép gấp mép có lỗ bắt vít vào khung tấm pin ở hai "
         "đầu, chốt xoay giữa đà lồng vào giá càng cua để tấm pin quay đúng tâm khớp "
         "nâng và cân mô-men trọng trường."),
    ]),
]


def main():
    os.makedirs(DST, exist_ok=True)
    for goc, chuan in CANON:
        p_goc = os.path.join(SRC, goc)
        if not os.path.exists(p_goc):
            print("THIEU ANH NGUON:", goc)
            sys.exit(1)
        shutil.copyfile(p_goc, os.path.join(DST, chuan))

    d = Document(F)
    for p in d.paragraphs:
        if (p.style.name or "") == "Caption" and "toàn cảnh mô hình nhìn từ phía trước" in p.text:
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
            if q._p is p._p:
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
        for ten, w, mo_ta_cap, mo_ta in items:
            if ten == "__MO_TA_MO_DAU__":
                dp = d.add_paragraph(mo_ta)
                nh._p.addprevious(dp._p)
                continue
            pi = d.add_paragraph()
            pi.add_run().add_picture(os.path.join(DST, ten), width=Inches(w))
            cp = d.add_paragraph(style="Caption")
            cp.add_run("Hình 0. %s" % mo_ta_cap)
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
    print("da chen %d anh 3D + 1 doan mo dau | tong caption Hinh: %d" % (total, n))


if __name__ == "__main__":
    main()
