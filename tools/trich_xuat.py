# -*- coding: utf-8 -*-
"""Trich nguyen van noi dung tu 2 ban Word goc va ghep thanh 6 quyen theo CHUONG.

Moi quyen giu nguyen van cac doan/bang/hinh cua ban goc (khong viet tom luoc),
chen them noi dung moi (thiet ke chi tiet, lap trinh, tien do) va danh so chuong
lien tuc trong tung quyen.
"""
import os
import re
from collections import OrderedDict

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import noi_dung_moi_1_truc as M1
import noi_dung_moi_2_truc as M2

SRC = {1: "Bao_cao_do_an_mau_bam_nang_1_truc.docx",
       2: "bao_cao_mau_do_an_dieu_khien_bam_mat_troi.docx"}

# chu thich cho cac bang trich tu ban goc (theo thu tu xuat hien)
TABLE_CAPS = {
    1: ["{B}. Biến thiên xích vĩ và quỹ đạo biểu kiến theo mùa ở Bắc bán cầu",
        "{B}. So sánh các phương pháp bám nắng",
        "{B}. Cấu hình và nhiệm vụ các khối hệ thống một trục",
        "{B}. Ký hiệu và hướng gá của bốn cảm biến"],
    2: ["{B}. Biến thiên xích vĩ và quỹ đạo biểu kiến theo mùa ở Bắc bán cầu",
        "{B}. So sánh các phương pháp bám nắng",
        "{B}. Cấu hình và vai trò các khối hệ thống hai trục",
        "{B}. Ký hiệu và hướng gá của bốn cảm biến"],
}

# sua tham chieu gioa cac quyen
PATCHES = {
    2: [("phương án được chọn trình bày tại Chương 3 là so sánh trực tiếp điện trở của bốn LDR",
         "phương án được chọn trình bày tại chương thuật toán của quyển lập trình là so sánh trực tiếp điện trở của bốn LDR")],
    1: [],
}


def load_blocks(report):
    doc = Document(os.path.join(ROOT, SRC[report]))
    body = doc.element.body
    blocks = []
    tcap = 0
    pending_cap = None
    children = list(body.iterchildren())
    for i, child in enumerate(children):
        if child.tag == qn("w:p"):
            p = Paragraph(child, doc)
            txt = p.text.strip()
            has_img = bool(p._p.findall(".//" + qn("w:drawing")))
            if has_img:
                blocks.append(["img", "Luu_do_thuat_toan_bam_nang_4_LDR.png", None])
                continue
            if not txt:
                continue
            st = p.style.name
            if st == "Caption":
                # chu thich cua hinh vua chen
                for b in reversed(blocks):
                    if b[0] == "img" and b[2] is None:
                        b[2] = "{H}. " + re.sub(r"^Hình\s*[\d.]+\.?\s*", "", txt)
                        break
                continue
            if st == "Heading 1":
                blocks.append(["h1", txt])
            elif st == "Heading 2":
                blocks.append(["h2", txt])
            elif st == "Heading 3":
                blocks.append(["h3", txt])
            elif st == "List Bullet":
                blocks.append(["b", txt])
            else:
                blocks.append(["p", txt])
        elif child.tag == qn("w:tbl"):
            tb = Table(child, doc)
            rows = [[c.text.strip() for c in r.cells] for r in tb.rows]
            cap = TABLE_CAPS[report][tcap] if tcap < len(TABLE_CAPS[report]) else None
            tcap += 1
            blocks.append(["tbl", rows, cap])
    for old, new in PATCHES[report]:
        for b in blocks:
            if b[0] in ("p", "b") and old in b[1]:
                b[1] = b[1].replace(old, new)
    return blocks


def cut(blocks, start, stop=None):
    out, on = [], False
    for b in blocks:
        if b[0] == "h1":
            if b[1].startswith(start):
                on = True
            elif stop and b[1].startswith(stop):
                on = False
        if on:
            out.append(b)
    return out


def sect(blocks, num):
    """Cac khoi thuoc muc h2 co so 'num.' (kem h2 dau)."""
    out, on = [], False
    for b in blocks:
        if b[0] == "h2":
            on = b[1].startswith(num + ".")
        elif b[0] == "h1":
            on = False
        if on:
            out.append(b)
    return out


def renum(blocks, mapping):
    out = []
    for b in blocks:
        b = list(b)
        if b[0] in ("h2", "h3"):
            for old, new in mapping.items():
                if b[1].startswith(old + "."):
                    b[1] = new + "." + b[1][len(old) + 1:]
                    break
        out.append(b)
    return out


def inject(blocks, inject_map):
    out = []
    for b in blocks:
        out.append(b)
        if b[0] == "h2":
            key = b[1].split(".")[0] + "." + b[1].split(".")[1] if "." in b[1] else None
            for k, extra in inject_map.items():
                if b[1].startswith(k + "."):
                    # chen cuoi muc: tam danh dau, se chen truoc h2/h1 ke tiep
                    out.append(["__MARK__", k])
    # dien extra vao cuoi muc danh dau (truoc h2/h1 ke tiep)
    res, i = [], 0
    while i < len(out):
        b = out[i]
        if b[0] == "__MARK__":
            k = b[1]
            j = i + 1
            while j < len(out) and out[j][0] not in ("h1", "h2"):
                j += 1
            res.extend(out[i + 1:j])
            res.extend(inject_map[k])
            i = j
            continue
        res.append(b)
        i += 1
    return res


class Numberer:
    def __init__(self):
        self.h = 0
        self.b = 0

    def fix(self, cap):
        if cap is None:
            return None
        if "{H}" in cap:
            self.h += 1
            cap = cap.replace("{H}", "Hình %d" % self.h)
        if "{B}" in cap:
            self.b += 1
            cap = cap.replace("{B}", "Bảng %d" % self.b)
        return cap


def compose(report):
    M = M1 if report == 1 else M2
    blocks = load_blocks(report)
    ch1 = cut(blocks, "CHƯƠNG 1", "CHƯƠNG 2")
    ch2 = cut(blocks, "CHƯƠNG 2", "CHƯƠNG 3")
    ch3 = cut(blocks, "CHƯƠNG 3", "CHƯƠNG 4")
    refs = cut(blocks, "TÀI LIỆU THAM KHẢO")

    specs = OrderedDict()

    # ---------- quyen nghien cuu ----------
    n = Numberer()
    spec = [list(b) for b in ch1 + ch2]
    spec.append(["h1", M.NGHIEN_CUU_H1_CH3])
    spec += [list(b) for b in M.NGHIEN_CUU_CH3]
    spec += [list(b) for b in refs]
    specs["Nghien_cuu"] = (spec, n)

    # ---------- quyen che tao ----------
    n = Numberer()
    if report == 1:
        subA = sect(ch3, "3.1") + sect(ch3, "3.2") + sect(ch3, "3.3")
        mapA = {"3.1": "1.1", "3.2": "1.2", "3.3": "1.3"}
        subB = sect(ch3, "3.6")
        mapB = {"3.6": "3.4"}
    else:
        subA = (sect(ch3, "3.1") + sect(ch3, "3.2") + sect(ch3, "3.3")
                + sect(ch3, "3.4") + sect(ch3, "3.6"))
        mapA = {"3.1": "1.1", "3.2": "1.2", "3.3": "1.3", "3.4": "1.4", "3.6": "1.5"}
        subB = sect(ch3, "3.7")
        mapB = {"3.7": "3.4"}
    spec = [["h1", M.CHE_TAO_H1_CH1]]
    spec += renum(inject(subA, M.INJECT), mapA)
    spec.append(["h1", M.CHE_TAO_H1_CH2])
    spec += [list(b) for b in M.CHE_TAO_CH2]
    spec.append(["h1", M.CHE_TAO_H1_CH3])
    spec += [list(b) for b in M.CHE_TAO_CH3_NEW]
    spec += renum(subB, mapB)
    spec.append(["h1", M.CHE_TAO_H1_CH4])
    spec += [list(b) for b in M.CHE_TAO_CH4]
    spec += [list(b) for b in refs]
    specs["Che_tao"] = (spec, n)

    # ---------- quyen lap trinh ----------
    n = Numberer()
    spec = [["h1", M.LAP_TRINH_H1_CH1]] + [list(b) for b in M.LAP_TRINH_CH1]
    spec += [["h1", M.LAP_TRINH_H1_CH2]] + [list(b) for b in M.LAP_TRINH_CH2]
    spec += [["h1", M.LAP_TRINH_H1_CH3]]
    if report == 1:
        s35 = renum(sect(ch3, "3.5"), {"3.5": "3.1"})
        s35 = inject(s35, {"3.1": [list(b) for b in M.LAP_TRINH_CH3_PRE]})
        s34 = renum(sect(ch3, "3.4"), {"3.4": "3.2"})
        spec += s35 + s34
    else:
        spec += [list(b) for b in M.LAP_TRINH_CH3_PRE]
        spec += renum(sect(ch3, "3.5"), {"3.5": "3.2"})
    spec += [list(b) for b in M.LAP_TRINH_CH3_POST]
    spec.append(["h1", M.LAP_TRINH_H1_CH4])
    spec += [list(b) for b in M.LAP_TRINH_CH4]
    spec += [list(b) for b in refs]
    specs["Lap_trinh"] = (spec, n)

    # danh so hinh / bang
    for key, (sp, num) in specs.items():
        for b in sp:
            if b[0] in ("img", "tbl"):
                b[2] = num.fix(b[2])
    return specs


def all_specs():
    out = OrderedDict()
    for r in (1, 2):
        for key, (sp, _n) in compose(r).items():
            out["Bao_cao_%d_truc_%s.docx" % (r, key)] = (sp, r)
    return out


if __name__ == "__main__":
    for name, (sp, r) in all_specs().items():
        h1 = [b[1] for b in sp if b[0] == "h1"]
        h2 = [b[1] for b in sp if b[0] == "h2"]
        print("==", name, "| khoi:", len(sp), "| h1:", len(h1), "| h2:", len(h2))
        for t in h1:
            print("   ", t)
