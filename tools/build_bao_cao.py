# -*- coding: utf-8 -*-
"""Dung 6 file Word (3 quyen x 2 ban bao cao) theo cau truc CHUONG.

Noi dung goc duoc trich boi trich_xuat.py; noi dung moi nam trong
noi_dung_moi_1_truc.py / noi_dung_moi_2_truc.py; so lieu trong hinh_ve/.
Chay:  python3 tools/build_bao_cao.py
"""
import os
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trich_xuat

WIDTHS = {
    "so_do_khoi_1_truc.png": 15.5, "so_do_khoi_2_truc.png": 15.5,
    "so_do_ket_noi_1_truc.png": 16.0, "so_do_ket_noi_2_truc.png": 16.0,
    "mo_hinh_co_khi_1_truc.png": 15.0, "mo_hinh_co_khi_2_truc.png": 15.0,
    "bo_tri_4_ldr.png": 15.5, "so_do_khoi_chuong_trinh.png": 16.0,
    "luu_do_ma_tran_1_truc.png": 11.5, "luu_do_ma_tran_2_truc.png": 11.5,
    "ket_qua_mo_phong_1_truc.png": 16.0,
}


def new_doc(report):
    doc = Document(trich_xuat.FILE_1 if report == 1 else trich_xuat.FILE_2)
    body = doc.element.body
    for child in list(body):
        if child.tag.endswith("}sectPr"):
            continue
        body.remove(child)
    return doc


def _code_style_name(doc):
    names = {s.name for s in doc.styles}
    for cand in ("Code Sample", "macro", "HTML Preformatted"):
        if cand in names:
            return cand
    return None


def add_block(doc, block, code_style):
    kind = block[0]
    if kind in ("h1", "h2", "h3"):
        doc.add_paragraph(block[1], style={"h1": "Heading 1", "h2": "Heading 2",
                                           "h3": "Heading 3"}[kind])
    elif kind == "p":
        doc.add_paragraph(block[1], style="Normal")
    elif kind == "b":
        doc.add_paragraph(block[1], style="List Bullet")
    elif kind == "eq":
        p = doc.add_paragraph(style="Normal")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.add_run(block[1]).italic = True
    elif kind == "code":
        for i, ln in enumerate(block[1].splitlines()):
            p = doc.add_paragraph(style=code_style) if code_style \
                else doc.add_paragraph(style="Normal")
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.space_before = Pt(6 if i == 0 else 0)
            p.paragraph_format.left_indent = Cm(0.6)
            run = p.add_run(ln if ln else " ")
            run.font.name = "Consolas"
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(0x1F, 0x33, 0x50)
    elif kind == "img":
        fname = os.path.basename(block[1])
        w = WIDTHS.get(fname, 15.0)
        full = os.path.join(ROOT, block[1])
        p = doc.add_paragraph(style="Normal")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.add_run().add_picture(full, width=Cm(w))
        if block[2]:
            doc.add_paragraph(block[2], style="Caption")
    elif kind == "tbl":
        rows, caption = block[1], block[2]
        if caption:
            cp = doc.add_paragraph(caption, style="Caption")
            cp.paragraph_format.space_after = Pt(4)
        t = doc.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = doc.styles["Table Grid"]
        t.alignment = 1
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                para = t.cell(i, j).paragraphs[0]
                para.paragraph_format.first_line_indent = Cm(0)
                para.paragraph_format.space_after = Pt(2)
                run = para.add_run(val)
                run.font.size = Pt(11)
                if i == 0:
                    run.bold = True
        doc.add_paragraph("", style="Normal")


def main():
    for spec, report in trich_xuat.all_specs():
        doc = new_doc(report)
        code_style = _code_style_name(doc)
        for block in spec["blocks"]:
            add_block(doc, block, code_style)
        doc.core_properties.title = os.path.basename(spec["out"]).replace(".docx", "").replace("_", " ")
        doc.save(spec["out"])
        print("đã tạo:", os.path.basename(spec["out"]),
              "| %d khối" % len(spec["blocks"]))


if __name__ == "__main__":
    main()
