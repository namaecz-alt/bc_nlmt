# -*- coding: utf-8 -*-
"""Xuat PDF TRUC TIEP tu 6 file Word hien hanh (ban sinh vien da hieu dinh).

Moi doan van, bang, anh, code trong Word di thang vao PDF theo thu tu,
nhan chuoi Hinh/Bang lam caption. Chay: python3 tools/xuat_pdf_tu_docx.py
"""
import hashlib
import os
import sys

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph as DParagraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, Spacer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xuat_pdf as XP
import trich_xuat

MEDIA = os.path.join(ROOT, "tmp_media")
os.makedirs(MEDIA, exist_ok=True)

HASH2NAME = {}
for dirpath, _dn, fn in os.walk(os.path.join(ROOT, "hinh_ve")):
    for f in fn:
        if f.lower().endswith(".png"):
            p = os.path.join(dirpath, f)
            HASH2NAME[hashlib.md5(open(p, "rb").read()).hexdigest()] = f
for f in os.listdir(ROOT):
    if f.lower().endswith(".png"):
        p = os.path.join(ROOT, f)
        HASH2NAME.setdefault(hashlib.md5(open(p, "rb").read()).hexdigest(), f)

FILES = [
    ("Bao_cao_1_truc_Nghien_cuu.docx", 1, "Nghien_cuu", 1),
    ("Bao_cao_1_truc_Che_tao.docx", 1, "Che_tao", 2),
    ("Bao_cao_1_truc_Lap_trinh.docx", 1, "Lap_trinh", 3),
    ("Bao_cao_2_truc_Nghien_cuu.docx", 2, "Nghien_cuu", 1),
    ("Bao_cao_2_truc_Che_tao.docx", 2, "Che_tao", 2),
    ("Bao_cao_2_truc_Lap_trinh.docx", 2, "Lap_trinh", 3),
]


def is_code_para(p):
    if (p.style.name or "") == "macro":
        return True
    runs = [r for r in p.runs if r.text.strip()]
    return bool(runs) and all((r.font.name or "").startswith(("Consolas", "Courier"))
                              for r in runs)


def docx_blocks(path):
    doc = Document(path)
    blocks = []
    code_buf = []

    def flush_code():
        if code_buf:
            blocks.append(("code", "\n".join(code_buf)))
            del code_buf[:]

    for child in doc.element.body:
        tag = child.tag.split("}")[-1]
        if tag == "p":
            p = DParagraph(child, doc)
            if is_code_para(p):
                code_buf.append(p.text)
                continue
            flush_code()
            t = " ".join(p.text.split())
            has_blip = "blip" in child.xml
            st = p.style.name or ""
            if has_blip:
                ns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
                blip = next(child.iter(
                    "{http://schemas.openxmlformats.org/drawingml/2006/main}blip"))
                part = doc.part.related_parts[blip.get(ns + "embed")]
                md5 = hashlib.md5(part.blob).hexdigest()
                name = HASH2NAME.get(md5, md5 + ".png")
                full = os.path.join(MEDIA, name)
                if not os.path.exists(full):
                    open(full, "wb").write(part.blob)
                blocks.append(("img", os.path.relpath(full, ROOT), None))
            elif st.startswith("Heading 1"):
                if t:
                    blocks.append(("h1", t))
            elif st.startswith("Heading 2"):
                if t:
                    blocks.append(("h2", t))
            elif st.startswith("Heading 3"):
                if t:
                    blocks.append(("h3", t))
            elif st == "Caption":
                if blocks and blocks[-1][0] in ("img", "tbl") and blocks[-1][2] is None:
                    blocks[-1] = (blocks[-1][0], blocks[-1][1], t)
                elif t:
                    blocks.append(("p", t))
            elif st.startswith("List"):
                if t:
                    blocks.append(("b", t))
            else:
                if t:
                    blocks.append(("p", t))
        elif tag == "tbl":
            flush_code()
            tbl = Table(child, doc)
            rows = [[" ".join(c.text.split()) for c in r.cells] for r in tbl.rows]
            blocks.append(("tbl", rows, None))
    flush_code()
    return blocks


def main():
    XP.register_fonts()
    XP.make_styles()
    avail = A4[0] - 5.0 * cm
    specs = []
    for fname, rep, quyen, idx in FILES:
        specs.append(({
            "out": os.path.join(ROOT, fname),
            "pdf": os.path.join(ROOT, "Bao_cao_pdf_%d_truc_%s.pdf" % (rep, quyen)),
            "title": "ĐỒ ÁN %d (mô hình %d trục)" % (rep, rep),
            "de_tai": trich_xuat.DE_TAI[rep],
            "quyen": trich_xuat.TEN_QUYEN[quyen],
            "subtitle": "Quyển %d/3 – tuần báo cáo 5/10 – 10/10/2026" % idx,
            "blocks": docx_blocks(os.path.join(ROOT, fname))}, rep))
    for spec, _r in specs:
        story = XP.cover_story(spec) + [PageBreak()] + XP.blocks_story(spec["blocks"], avail)
        XP.build(spec["pdf"], story)
    story = [Spacer(1, 4 * cm),
             Paragraph("BÁO CÁO ĐỒ ÁN – HỆ THỐNG BÁM NẮNG MẶT TRỜI", XP.S["cover"]),
             Paragraph("Bản tổng hợp 6 quyển dựng trực tiếp từ bản Word đã hiệu đính "
                       "tuần 5/10 – 10/10/2026", XP.S["cover2"]),
             Spacer(1, 1.0 * cm)]
    for i, (spec, r) in enumerate(specs, 1):
        story.append(Paragraph("•  %d. Đồ án %d – %s" % (i, r, spec["quyen"]),
                               ParagraphStyle("li", parent=XP.S["cover2"], alignment=0)))
        story.append(Spacer(1, 0.2 * cm))
    story.append(PageBreak())
    for spec, _r in specs:
        story += XP.cover_story(spec) + [PageBreak()] + XP.blocks_story(spec["blocks"], avail)
        story.append(PageBreak())
    XP.build(XP.OUT_GOP, story)


if __name__ == "__main__":
    main()
