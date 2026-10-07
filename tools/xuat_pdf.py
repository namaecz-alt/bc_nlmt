# -*- coding: utf-8 -*-
"""Xuất sáu PDF có mục lục liên kết và PDF gộp bắt đầu bằng bảng thông số chung."""
from __future__ import annotations

import os
import sys
import shutil
from xml.sax.saxutils import escape

import matplotlib
from pypdf import PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate,Frame,Image,PageBreak,PageTemplate,
                                Paragraph,Preformatted,Spacer,Table,TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents
from PIL import Image as PILImage

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import trich_xuat
import export_common_spec

FONT_DIR=os.path.join(matplotlib.get_data_path(),"fonts","ttf")
OUT_GOP=os.path.join(ROOT,"Bao_cao_day_du_6_phan.pdf")
WIDTH_CM={
    "so_do_khoi_1_truc.png":15.5,"so_do_khoi_2_truc.png":15.5,
    "so_do_ket_noi_1_truc.png":16.0,"so_do_ket_noi_2_truc.png":16.0,
    "bo_tri_4_ldr.png":15.8,"so_do_3_phuong_phap.png":15.5,
    "duong_di_mat_troi_1_truc.png":15.0,"hoat_dong_hybrid_1_truc.png":15.5,
    "hoat_dong_hybrid_2_truc.png":15.5,"so_sanh_nang_luong_1_truc.png":15.5,
    "so_sanh_nang_luong_2_truc.png":15.5,
    "luu_do_tong_quat_1_truc.png":11.5,"luu_do_tong_quat_2_truc.png":11.5,
    "luu_do_thien_van.png":11.3,"luu_do_doc_adc.png":11.3,
    "luu_do_dieu_khien_motor.png":11.3,"luu_do_lcd.png":11.3,
}
S={}


def register_fonts():
    pdfmetrics.registerFont(TTFont("Ser",os.path.join(FONT_DIR,"DejaVuSerif.ttf")))
    pdfmetrics.registerFont(TTFont("Ser-B",os.path.join(FONT_DIR,"DejaVuSerif-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Ser-I",os.path.join(FONT_DIR,"DejaVuSerif-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Mono",os.path.join(FONT_DIR,"DejaVuSans.ttf")))  # đủ dấu tiếng Việt trong comment code
    pdfmetrics.registerFontFamily("Ser",normal="Ser",bold="Ser-B",italic="Ser-I",boldItalic="Ser-B")


def make_styles():
    S["body"]=ParagraphStyle("Body",fontName="Ser",fontSize=11.5,leading=15.1,
                             alignment=TA_JUSTIFY,firstLineIndent=0.85*cm,spaceAfter=5)
    S["Heading1"]=ParagraphStyle("Heading1",fontName="Ser-B",fontSize=14.5,leading=18,
                                 alignment=TA_CENTER,spaceBefore=5,spaceAfter=9,keepWithNext=True,
                                 textColor=colors.HexColor("#1f3864"))
    S["Heading2"]=ParagraphStyle("Heading2",fontName="Ser-B",fontSize=12.5,leading=16,
                                 spaceBefore=8,spaceAfter=4,keepWithNext=True,
                                 textColor=colors.HexColor("#1f3864"))
    S["Heading3"]=ParagraphStyle("Heading3",fontName="Ser-B",fontSize=11.5,leading=14,spaceBefore=6,spaceAfter=3,keepWithNext=True)
    S["FrontHeading"]=ParagraphStyle("FrontHeading",fontName="Ser-B",fontSize=15,leading=19,
                                     alignment=TA_CENTER,spaceAfter=12,textColor=colors.HexColor("#1f3864"))
    S["bullet"]=ParagraphStyle("Bullet",parent=S["body"],firstLineIndent=0,leftIndent=0.8*cm,spaceAfter=4)
    S["eq"]=ParagraphStyle("Eq",parent=S["body"],fontName="Ser-I",alignment=TA_CENTER,firstLineIndent=0,spaceBefore=3,spaceAfter=6)
    S["cap"]=ParagraphStyle("Caption",fontName="Ser-I",fontSize=9.5,leading=12,alignment=TA_CENTER,spaceBefore=3,spaceAfter=8)
    S["tcap"]=ParagraphStyle("TableCaption",fontName="Ser-B",fontSize=9.5,leading=12,alignment=TA_CENTER,spaceBefore=4,spaceAfter=3)
    S["cell"]=ParagraphStyle("Cell",fontName="Ser",fontSize=8.4,leading=10.3)
    S["cellb"]=ParagraphStyle("CellB",parent=S["cell"],fontName="Ser-B")
    S["cover"]=ParagraphStyle("Cover",fontName="Ser-B",fontSize=16,leading=22,alignment=TA_CENTER,spaceAfter=12,textColor=colors.HexColor("#1f3864"))
    S["cover2"]=ParagraphStyle("Cover2",fontName="Ser",fontSize=11,leading=16,alignment=TA_CENTER,spaceAfter=7)
    S["cover3"]=ParagraphStyle("Cover3",fontName="Ser-B",fontSize=13,leading=18,alignment=TA_CENTER,spaceAfter=9)
    S["code"]=ParagraphStyle("Code",fontName="Mono",fontSize=6.7,leading=8.0,leftIndent=0.18*cm,rightIndent=0.1*cm,spaceAfter=0)
    S["TOC1"]=ParagraphStyle("TOC1",fontName="Ser-B",fontSize=10,leading=14,leftIndent=0,firstLineIndent=0,spaceBefore=3)
    S["TOC2"]=ParagraphStyle("TOC2",fontName="Ser",fontSize=9,leading=12,leftIndent=0.55*cm,firstLineIndent=0)


def style_text(text):
    return escape(str(text)).replace("\n","<br/>")


def cover_story(item):
    st=[Spacer(1,2.5*cm),
        Paragraph("BÁO CÁO ĐỒ ÁN – HỆ THỐNG BÁM NẮNG",S["cover"]),
        Spacer(1,0.5*cm),Paragraph(style_text(item["de_tai"]),S["cover"]),
        Spacer(1,0.6*cm),Paragraph(style_text(item["quyen"]),S["cover3"]),
        Paragraph(style_text(item["title"])+" – "+style_text(item["subtitle"]),S["cover2"]),
        Spacer(1,1.0*cm),
        Paragraph("Cấu hình và phần việc được phân công theo Bảng thông số chung. "
                  "Thiên văn định vị thô, LDR hiệu chỉnh khi đủ sáng; ban đêm/thiếu sáng giữ vị trí.",S["cover2"]),
        Spacer(1,0.6*cm),Paragraph("Biên soạn: 07/10/2026",S["cover2"]),PageBreak()]
    return st


def frontmatter(item):
    st=[]
    st += [Paragraph("LỜI MỞ ĐẦU",S["FrontHeading"]),
           Paragraph("Báo cáo trình bày phần việc được phân công trong đồ án hệ thống bám nắng mặt trời. Sáu quyển chia theo cấu hình một trục/hai trục và theo nhóm Nghiên cứu, Chế tạo, Lập trình để tách rõ tính toán, giao diện phần cứng và mã điều khiển.",S["body"]),
           Paragraph("Thông số thống nhất được quản lý trong Bảng thông số chung đặt trước bộ báo cáo. Kết quả tính toán/mô phỏng được phân biệt với phép đo; việc chưa thực hiện được ghi kèm kế hoạch dự kiến.",S["body"]),PageBreak(),
           Paragraph("LỜI CẢM ƠN",S["FrontHeading"]),
           Paragraph("Nhóm thực hiện trân trọng cảm ơn giảng viên hướng dẫn, thầy cô và các bạn đã hỗ trợ định hướng, góp ý và tạo điều kiện trong quá trình xây dựng đề tài. Các nhận xét chuyên môn giúp nhóm thống nhất quy ước góc, giới hạn hành trình, phân công nội dung và cách trình bày bằng chứng.",S["body"]),
           Paragraph("Nhóm xin tiếp thu các góp ý còn lại để hoàn thiện bản vẽ, kiểm thử phần cứng và hiệu chuẩn trước khi nghiệm thu.",S["body"]),PageBreak(),
           Paragraph("LỜI CAM ĐOAN",S["FrontHeading"]),
           Paragraph("Nhóm cam đoan nội dung được trình bày theo đúng phạm vi quyển báo cáo và nguồn đã dẫn. Kết quả tính toán/mô phỏng được phân biệt với kết quả đo. Báo cáo không khẳng định đã lắp ráp, hiệu chuẩn, đo dòng/mô-men hoặc thử phần cứng khi chưa có biên bản xác nhận; các việc đó được ghi là chưa thực hiện và có thời hạn dự kiến.",S["body"]),
           Paragraph("Thông số cơ khí, tải gió, công suất nhãn motor và giới hạn góc chưa được xác nhận được đánh dấu là giả thiết thiết kế, không phải kết quả thực nghiệm.",S["body"]),PageBreak(),
           Paragraph("MỤC LỤC",S["FrontHeading"])]
    toc=TableOfContents();toc.levelStyles=[S["TOC1"],S["TOC2"]];toc.dotsMinLevel=0
    st.extend([toc,PageBreak()])
    return st


def column_widths(n,avail):
    if n==2:frac=[0.30,0.70]
    elif n==3:frac=[0.30,0.35,0.35]
    elif n==4:frac=[0.11,0.25,0.43,0.21]
    elif n==5:frac=[0.19,0.2025,0.2025,0.2025,0.2025]
    else:frac=[1/n]*n
    return [avail*v for v in frac]


def blocks_story(blocks,avail):
    story=[];first_heading=True
    for block in blocks:
        kind=block[0]
        if kind in ("h1","h2","h3"):
            if kind=="h1" and not first_heading:story.append(PageBreak())
            if kind=="h1":first_heading=False
            name={"h1":"Heading1","h2":"Heading2","h3":"Heading3"}[kind]
            story.append(Paragraph(style_text(block[1]),S[name]))
        elif kind=="p":story.append(Paragraph(style_text(block[1]),S["body"]))
        elif kind=="b":story.append(Paragraph(style_text(block[1]),S["bullet"],bulletText="–"))
        elif kind=="eq":story.append(Paragraph(style_text(block[1]),S["eq"]))
        elif kind=="code":
            for line in block[1].splitlines():story.append(Preformatted(line if line else " ",S["code"]))
        elif kind=="img":
            full=os.path.join(ROOT,block[1])
            if not os.path.exists(full):raise FileNotFoundError(full)
            width=min(WIDTH_CM.get(os.path.basename(full),15.0)*cm,avail)
            with PILImage.open(full) as im:ratio=im.height/im.width
            story.append(Spacer(1,2));story.append(Image(full,width=width,height=width*ratio))
            if block[2]:story.append(Paragraph(style_text(block[2]),S["cap"]))
        elif kind=="tbl":
            rows,caption=block[1],block[2]
            if caption:story.append(Paragraph(style_text(caption),S["tcap"]))
            data=[]
            for i,row in enumerate(rows):
                sty=S["cellb"] if i==0 else S["cell"]
                data.append([Paragraph(style_text(cell),sty) for cell in row])
            table=Table(data,colWidths=column_widths(len(rows[0]),avail),repeatRows=1,hAlign="CENTER")
            table.setStyle(TableStyle([
                ("GRID",(0,0),(-1,-1),0.45,colors.HexColor("#536477")),
                ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#d9e5f3")),
                ("VALIGN",(0,0),(-1,-1),"TOP"),
                ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
                ("TOPPADDING",(0,0),(-1,-1),2.2),("BOTTOMPADDING",(0,0),(-1,-1),2.2),
            ]))
            story.extend([table,Spacer(1,5)])
    return story


class ReportDocTemplate(BaseDocTemplate):
    def __init__(self,*args,report_key="report",report_name="",**kwargs):
        super().__init__(*args,**kwargs);self.report_key=report_key;self.report_name=report_name;self._heading_count=0
    def beforeDocument(self):
        super().beforeDocument()
        self._heading_count=0
    def afterFlowable(self,flowable):
        if not isinstance(flowable,Paragraph):return
        name=flowable.style.name
        level={"Heading1":0,"Heading2":1}.get(name)
        if level is None:return
        text=flowable.getPlainText();key=f"{self.report_key}_{self._heading_count}"
        self._heading_count+=1
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text,key,level=level,closed=False)
        self.notify("TOCEntry",(level,text,self.page,key))


def on_page(canvas,doc):
    canvas.saveState();canvas.setFillColor(colors.HexColor("#626b75"));canvas.setFont("Ser",8.5)
    canvas.drawCentredString(A4[0]/2,1.0*cm,f"{doc.report_name}  ·  Trang {doc.page}")
    if doc.page>1:
        canvas.setStrokeColor(colors.HexColor("#d0d5dc"));canvas.setLineWidth(.45)
        canvas.line(2.3*cm,A4[1]-1.35*cm,A4[0]-2.3*cm,A4[1]-1.35*cm)
    canvas.restoreState()


def build_pdf(item):
    avail=A4[0]-4.6*cm
    story=cover_story(item)+frontmatter(item)+blocks_story(item["blocks"],avail)
    doc=ReportDocTemplate(item["pdf"],pagesize=A4,leftMargin=2.3*cm,rightMargin=2.3*cm,
                          topMargin=1.9*cm,bottomMargin=1.7*cm,title=item["quyen"],
                          author="Nhóm thực hiện đồ án",report_key=item["base"],report_name=item["quyen"])
    frame=Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id="main")
    doc.addPageTemplates([PageTemplate(id="report",frames=[frame],onPage=on_page)])
    doc.multiBuild(story)
    print("đã xuất",os.path.basename(item["pdf"]))


def merge_pdf(items):
    writer=PdfWriter()
    common=os.path.join(ROOT,"Bang_thong_so_chung.pdf")
    writer.append(common)
    for item in items:writer.append(item["pdf"])
    writer.add_metadata({"/Title":"Báo cáo đồ án bám nắng – Bảng thông số chung và sáu quyển",
                         "/Author":"Nhóm thực hiện đồ án"})
    with open(OUT_GOP,"wb") as f:writer.write(f)
    print("đã gộp",os.path.basename(OUT_GOP),"(Bảng thông số chung + 6 quyển)")


def main():
    register_fonts();make_styles()
    export_common_spec.main()
    items=trich_xuat.danh_sach_bao_cao()
    for item in items:
        build_pdf(item)
        # Giữ tên PDF lịch sử đồng bộ để không còn bản cũ gây nhầm lẫn.
        legacy=os.path.join(ROOT,item["base"].replace("Bao_cao_","Bao_cao_pdf_",1)+".pdf")
        shutil.copyfile(item["pdf"],legacy)
    merge_pdf(items)


if __name__=="__main__":main()
