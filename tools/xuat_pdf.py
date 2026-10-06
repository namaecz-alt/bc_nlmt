# -*- coding: utf-8 -*-
"""Xuat 1 file PDF gop ca 6 phan bao cao (dung khi khong co MS Word).

Nguon noi dung giong het ban Word: tools/noi_dung_1_truc.py va noi_dung_2_truc.py.
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
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

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
    "luu_do_thuat_toan_1_truc.png": 11.5, "Luu_do_thuat_toan_bam_nang_4_LDR.png": 12.0,
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


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def col_widths(n, avail):
    if n == 2:
        fr = [0.30, 0.70]
    elif n == 3:
        fr = [0.30, 0.35, 0.35]
    else:
        fr = [0.07, 0.30, 0.50, 0.13]
    return [avail * f for f in fr[:n]]


def build_story():
    story = []
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph("BÁO CÁO ĐỒ ÁN – HỆ THỐNG BÁM NẮNG MẶT TRỜI", S["cover"]))
    story.append(Paragraph("Bản tổng hợp 6 quyển (mỗi báo cáo chia 3 quyển: "
                           "Nghiên cứu – Chế tạo – Lập trình), đánh số theo CHƯƠNG", S["cover2"]))
    story.append(Spacer(1, 1.2 * cm))
    for t in ["Quyển 1. Nghiên cứu – mô hình một trục (ESP32): Chương 1–3",
              "Quyển 2. Chế tạo mô hình một trục: Chương 1–4",
              "Quyển 3. Lập trình mô hình một trục: Chương 1–4",
              "Quyển 4. Nghiên cứu – mô hình hai trục (Arduino Mega): Chương 1–3",
              "Quyển 5. Chế tạo mô hình hai trục: Chương 1–4",
              "Quyển 6. Lập trình mô hình hai trục: Chương 1–4"]:
        story.append(Paragraph("•  " + t, ParagraphStyle("li", parent=S["cover2"],
                                                         alignment=0,
                                                         leftIndent=3 * cm)))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("Mỗi phần có mục “Tiến độ thực hiện và kế hoạch tuần tới” "
                           "(12/10 – 18/10/2026).", S["cover2"]))

    avail = A4[0] - 5.0 * cm
    for spec, _r in trich_xuat.all_specs().values():
        story.append(PageBreak())
        for block in spec:
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
    doc = BaseDocTemplate(OUT_PDF, pagesize=A4,
                          leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                          topMargin=2.2 * cm, bottomMargin=2.0 * cm,
                          title="Bao cao do an - he thong bam nang mat troi (6 phan)")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])
    doc.build(build_story())
    print("da xuat:", OUT_PDF)


if __name__ == "__main__":
    main()
