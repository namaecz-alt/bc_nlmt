# -*- coding: utf-8 -*-
"""Xuat 1 file PDF gop ca 6 phan bao cao (dung khi khong co MS Word).

Nguon noi dung giong het ban Word: tools/trich_xuat.py + noi_dung_moi_*.py.
Font DejaVu Serif (di kem matplotlib) ho tro day du tieng Viet.
Chay:  python3 tools/xuat_pdf.py
"""
import os

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image, PageBreak,
                                PageTemplate, Paragraph, Preformatted, Spacer,
                                Table, TableStyle)

import matplotlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trich_xuat

FONT_DIR = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
OUT_PDF = os.path.join(ROOT, "Bao_cao_day_du_6_phan.pdf")

WIDTH_CM = {
    "so_do_khoi_1_truc.png": 15.5, "so_do_khoi_2_truc.png": 15.5,
    "so_do_ket_noi_1_truc.png": 16.0, "so_do_ket_noi_2_truc.png": 16.0,
    "mo_hinh_co_khi_1_truc.png": 15.0, "mo_hinh_co_khi_2_truc.png": 15.0,
    "bo_tri_4_ldr.png": 15.5, "so_do_khoi_chuong_trinh.png": 16.0,
    "ket_qua_mo_phong_1_truc.png": 15.5, "ket_qua_nang_luong.png": 15.5,
    "luu_do_tong_quat.png": 11.0, "luu_do_thien_van.png": 10.0,
    "luu_do_ldr.png": 10.0, "luu_do_dong_co.png": 10.0, "luu_do_hien_thi.png": 10.0,
    "mach_dong_luc_cau_h_tip41c.png": 14.5, "mach_opto_pc817.png": 14.0,
    "mach_cong_tac_hanh_trinh.png": 14.5, "mach_esp32_devkit.png": 13.0,
    "mach_nguon_lm2596.png": 14.5, "mach_7805_lcd_i2c.png": 14.5,
    "mach_ds1307.png": 13.0,
}


def register_fonts():
    pdfmetrics.registerFont(TTFont("Ser", os.path.join(FONT_DIR, "DejaVuSerif.ttf")))
    pdfmetrics.registerFont(TTFont("Ser-B", os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Ser-I", os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf")))
    pdfmetrics.registerFontFamily("Ser", normal="Ser", bold="Ser-B",
                                  italic="Ser-I", boldItalic="Ser-B")


S = {}


def make_styles():
    S["body"] = ParagraphStyle("body", fontName="Ser", fontSize=12, leading=15.5,
                               alignment=TA_JUSTIFY, firstLineIndent=1.0 * cm,
                               spaceAfter=6)
    S["h1"] = ParagraphStyle("h1", fontName="Ser-B", fontSize=14, leading=18,
                             alignment=TA_CENTER, spaceBefore=6, spaceAfter=12)
    S["h2"] = ParagraphStyle("h2", fontName="Ser-B", fontSize=13, leading=16.5,
                             spaceBefore=10, spaceAfter=6)
    S["h3"] = ParagraphStyle("h3", fontName="Ser-B", fontSize=12, leading=15,
                             spaceBefore=8, spaceAfter=4)
    S["bullet"] = ParagraphStyle("bullet", parent=S["body"], firstLineIndent=0,
                                 leftIndent=0.9 * cm, bulletIndent=0.25 * cm,
                                 spaceAfter=4)
    S["eq"] = ParagraphStyle("eq", parent=S["body"], alignment=TA_CENTER,
                             firstLineIndent=0, fontName="Ser-I", spaceBefore=2,
                             spaceAfter=6)
    S["cap"] = ParagraphStyle("cap", fontName="Ser-I", fontSize=10.5, leading=13,
                              alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
    S["tcap"] = ParagraphStyle("tcap", fontName="Ser-B", fontSize=10.5, leading=13,
                               alignment=TA_CENTER, spaceBefore=6, spaceAfter=4)
    S["cell"] = ParagraphStyle("cell", fontName="Ser", fontSize=9.5, leading=12)
    S["cellb"] = ParagraphStyle("cellb", parent=S["cell"], fontName="Ser-B")
    S["cover"] = ParagraphStyle("cover", fontName="Ser-B", fontSize=16, leading=22,
                                alignment=TA_CENTER, spaceAfter=10)
    S["cover2"] = ParagraphStyle("cover2", fontName="Ser", fontSize=12, leading=17,
                                alignment=TA_CENTER, spaceAfter=6)
    S["code"] = ParagraphStyle("code", fontName="Courier", fontSize=7.2, leading=9.0,
                               leftIndent=0.4 * cm, spaceBefore=0, spaceAfter=0)


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def col_widths(n, avail):
    if n == 2:
        fr = [0.30, 0.70]
    elif n == 3:
        fr = [0.30, 0.35, 0.35]
    elif n == 4:
        fr = [0.07, 0.28, 0.52, 0.13]
    else:
        fr = [1.0 / n] * n
    return [avail * f for f in fr[:n]]


def story_of_spec(spec):
    story = [Paragraph(esc(spec["title"]), S["h1"]),
             Paragraph(esc(spec["subtitle"]), S["cap"])]
    for block in spec["blocks"]:
        story += flow_of(block)
    return story


def flow_of(block):
    out = []
    kind = block[0]
    if kind == "h1":
        out.append(Paragraph(esc(block[1]), S["h1"]))
    elif kind == "h2":
        out.append(Paragraph(esc(block[1]), S["h2"]))
    elif kind == "h3":
        out.append(Paragraph(esc(block[1]), S["h3"]))
    elif kind == "p":
        out.append(Paragraph(esc(block[1]), S["body"]))
    elif kind == "b":
        out.append(Paragraph(esc(block[1]), S["bullet"], bulletText="-"))
    elif kind == "eq":
        out.append(Paragraph(esc(block[1]), S["eq"]))
    elif kind == "code":
        for ln in block[1].splitlines():
            out.append(Preformatted(ln if ln else " ", S["code"]))
    elif kind == "img":
        path = block[1]
        full = path if os.path.isabs(path) else os.path.join(ROOT, path)
        w = WIDTH_CM.get(os.path.basename(path), 15.0) * cm
        with PILImage.open(full) as im:
            iw, ih = im.size
        h = w * ih / iw
        out.append(Spacer(1, 4))
        out.append(Image(full, width=w, height=h))
        if block[2]:
            out.append(Paragraph(esc(block[2]), S["cap"]))
    elif kind == "tbl":
        rows, caption = block[1], block[2]
        if caption:
            out.append(Paragraph(esc(caption), S["tcap"]))
        avail = A4[0] - 5.0 * cm
        data = []
        for i, row in enumerate(rows):
            st = S["cellb"] if i == 0 else S["cell"]
            data.append([Paragraph(esc(c), st) for c in row])
        t = Table(data, colWidths=col_widths(len(rows[0]), avail), repeatRows=1)
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#1f3864")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d7e4f6")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        out.append(t)
        out.append(Spacer(1, 8))
    return out


def build_doc(story, out_path, title):
    doc = BaseDocTemplate(out_path, pagesize=A4,
                          leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                          topMargin=2.2 * cm, bottomMargin=2.0 * cm, title=title)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])
    doc.build(story)
    print("da xuat:", os.path.basename(out_path))


def build_story():
    story = []
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph("BÁO CÁO ĐỒ ÁN – HỆ THỐNG BÁM NẮNG MẶT TRỜI", S["cover"]))
    story.append(Paragraph("Bản tổng hợp 6 quyển (mỗi báo cáo chia 3 quyển: "
                           "Nghiên cứu – Chế tạo – Lập trình), đánh số theo CHƯƠNG. "
                           "Cả hai mô hình dùng ESP32, ma trận 4 LDR suy ra góc quay "
                           "và động cơ gạt nước trục vít.", S["cover2"]))
    story.append(Spacer(1, 1.2 * cm))
    for t in ["Quyển 1. Nghiên cứu – mô hình một trục (ESP32): Chương 1–4",
              "Quyển 2. Chế tạo mô hình một trục: Chương 1–4",
              "Quyển 3. Lập trình mô hình một trục: Chương 1–4",
              "Quyển 4. Nghiên cứu – mô hình hai trục (ESP32): Chương 1–4",
              "Quyển 5. Chế tạo mô hình hai trục: Chương 1–4",
              "Quyển 6. Lập trình mô hình hai trục: Chương 1–4"]:
        story.append(Paragraph("•  " + t, ParagraphStyle("li", parent=S["cover2"],
                                                         alignment=0,
                                                         leftIndent=3 * cm)))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("Mỗi quyển có mục tiến độ: kết quả đạt được trong tuần "
                           "5/10 – 10/10/2026 và các công việc còn lại của tuần này.", S["cover2"]))

    avail = A4[0] - 5.0 * cm
    for spec, _r in trich_xuat.all_specs():
        story.append(PageBreak())
        for block in spec["blocks"]:
            kind = block[0]
            if kind == "h1":
                story.append(Paragraph(esc(block[1]), S["h1"]))
            elif kind == "h2":
                story.append(Paragraph(esc(block[1]), S["h2"]))
            elif kind == "h3":
                story.append(Paragraph(esc(block[1]), S["h3"]))
            elif kind == "p":
                story.append(Paragraph(esc(block[1]), S["body"]))
            elif kind == "b":
                story.append(Paragraph(esc(block[1]), S["bullet"], bulletText="–"))
            elif kind == "eq":
                story.append(Paragraph(esc(block[1]), S["eq"]))
            elif kind == "code":
                for ln in block[1].splitlines():
                    story.append(Preformatted(ln if ln else " ", S["code"]))
            elif kind == "img":
                path = block[1]
                full = path if os.path.isabs(path) else os.path.join(ROOT, path)
                w = WIDTH_CM.get(os.path.basename(path), 15.0) * cm
                with PILImage.open(full) as im:
                    iw, ih = im.size
                h = w * ih / iw
                story.append(Spacer(1, 4))
                story.append(Image(full, width=w, height=h))
                if block[2]:
                    story.append(Paragraph(esc(block[2]), S["cap"]))
            elif kind == "tbl":
                rows, caption = block[1], block[2]
                if caption:
                    story.append(Paragraph(esc(caption), S["tcap"]))
                data = []
                for i, row in enumerate(rows):
                    st = S["cellb"] if i == 0 else S["cell"]
                    data.append([Paragraph(esc(c), st) for c in row])
                t = Table(data, colWidths=col_widths(len(rows[0]), avail),
                          repeatRows=1)
                t.setStyle(TableStyle([
                    ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#1f3864")),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d7e4f6")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ]))
                story.append(t)
                story.append(Spacer(1, 8))
    return story


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Ser", 10)
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm, "Trang %d" % doc.page)
    canvas.setStrokeColor(colors.HexColor("#1f3864"))
    canvas.setLineWidth(0.6)
    canvas.line(2.5 * cm, A4[1] - 1.6 * cm, A4[0] - 2.5 * cm, A4[1] - 1.6 * cm)
    canvas.restoreState()


def main():
    register_fonts()
    make_styles()
    # 6 PDF rieng, moi bao cao mot file
    for spec, _r in trich_xuat.all_specs():
        out = spec["out"].replace(".docx", ".pdf")
        build_doc(story_of_spec(spec), out, spec["title"])
    # PDF gop ca 6 quyen
    build_doc(build_story(), OUT_PDF,
              "Bao cao do an - he thong bam nang mat troi (6 phan)")


if __name__ == "__main__":
    main()
