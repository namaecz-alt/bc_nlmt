# -*- coding: utf-8 -*-
"""Khai báo sáu báo cáo, thứ tự đầu ra và đánh số hình/bảng tự động."""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_reports import compose

VOLUMES = (("Nghien_cuu", "Nghiên cứu"),
           ("Che_tao", "Chế tạo"),
           ("Lap_trinh", "Lập trình"))
DE_TAI = "Đồ án điện năng lượng mặt trời – phương pháp hybrid thiên văn và LDR"


def _numbered_blocks(blocks):
    result=[]; nfig=ntbl=0
    for block in blocks:
        item=list(block)
        if item[0]=="img" and len(item)>2 and item[2]:
            nfig+=1; item[2]=item[2].replace("{H}",f"Hình {nfig}")
        elif item[0]=="tbl" and len(item)>2 and item[2]:
            ntbl+=1; item[2]=item[2].replace("{B}",f"Bảng {ntbl}")
        result.append(tuple(item))
    return result


def danh_sach_bao_cao():
    reports=[]
    for report_no in (1,2):
        axis_label="một trục" if report_no==1 else "hai trục"
        for key,label in VOLUMES:
            base=f"Bao_cao_{report_no}_truc_{key}"
            reports.append({
                "report": report_no,
                "volume": key,
                "volume_label": label,
                "axis_label": axis_label,
                "base": base,
                "docx": os.path.join(ROOT,base+".docx"),
                "pdf": os.path.join(ROOT,base+".pdf"),
                "title": f"BÁO CÁO {label.upper()}",
                "subtitle": f"Cấu hình {axis_label}",
                "de_tai": DE_TAI,
                "quyen": f"QUYỂN {label.upper()} – ĐỒ ÁN {report_no}",
                "blocks": _numbered_blocks(compose(report_no,key)),
            })
    return reports


def all_specs():
    """API tương thích cho các công cụ build/export."""
    reports=danh_sach_bao_cao()
    return [(item,item["report"]) for item in reports]


if __name__=="__main__":
    for item in danh_sach_bao_cao():
        print(f"{item['base']}: {len(item['blocks'])} khối nội dung")
