# -*- coding: utf-8 -*-
"""Ap dung cac ghi chu boi do cua sinh vien vao 6 file Word (ban 6316853).
Nguyen tac: khong viet lai cho sinh vien da xoa; chi lam them cho bôi đỏ."""
import re
from copy import deepcopy
from docx import Document
from docx.shared import RGBColor, Pt, Inches

RED = "FF0000"
BLACK = RGBColor(0, 0, 0)


def is_red(r):
    c = r.font.color
    return c is not None and getattr(c, "rgb", None) is not None and str(c.rgb).upper() == RED


def dered(p):
    for r in p.runs:
        if is_red(r):
            r.font.color.rgb = BLACK


def strip_red_runs(p):
    for r in list(p.runs):
        if is_red(r):
            r._r.getparent().remove(r._r)


def set_text(p, text):
    runs = p.runs
    if runs:
        runs[0].text = text
        runs[0].font.color.rgb = BLACK
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        p.add_run(text)


def para(doc, pred, start=0):
    for i, p in enumerate(doc.paragraphs):
        if i >= start and pred(p):
            return i
    return -1


def h1(t):
    return lambda p: (p.style.name or "") == "Heading 1" and p.text.strip().startswith(t)


def h2(t):
    return lambda p: (p.style.name or "").startswith("Heading 2") and p.text.strip().startswith(t)


def body_idx(doc, el):
    for i, ch in enumerate(doc.element.body):
        if ch is el:
            return i
    return -1


def section_elems(doc, head_p):
    """Cac element than bai tu heading den truoc heading cung cap/cao hon."""
    st = head_p.style.name
    stops = ("Heading 1", "Heading 2") if st.endswith("2") else ("Heading 1", "Heading 2", "Heading 3")
    els = [head_p._p]
    i = body_idx(doc, head_p._p) + 1
    body = doc.element.body
    while i < len(body):
        el = body[i]
        done = False
        if el.tag.endswith("}p"):
            from docx.text.paragraph import Paragraph
            pp = Paragraph(el, doc)
            s = pp.style.name or ""
            if any(s.startswith(x) for x in stops):
                done = True
        if done:
            break
        els.append(el)
        i += 1
    return els


def remove_elems(elems):
    for el in elems:
        el.getparent().remove(el)


def insert_after(ref_el, new_els):
    cur = ref_el
    for el in new_els:
        cur.addnext(el)
        cur = el
    return cur


def new_para(doc, text, style=None, font=None, size=None):
    p = doc.add_paragraph(text, style=style) if style else doc.add_paragraph(text)
    for r in p.runs:
        if font:
            r.font.name = font
        if size:
            r.font.size = Pt(size)
        r.font.color.rgb = BLACK
    el = p._p
    el.getparent().remove(el)
    return el


def renumber(doc, pattern, mapping):
    rx = re.compile(pattern)
    for p in doc.paragraphs:
        if any(r.font.name and r.font.name.startswith(("Consolas", "Courier")) for r in p.runs):
            continue
        t = p.text
        nt = rx.sub(lambda m: mapping.get(m.group(0), m.group(0)), t)
        if nt != t:
            set_text(p, nt)


def add_ref(doc, text):
    i = para(doc, h1("TÀI LIỆU THAM KHẢO"))
    els = section_elems(doc, doc.paragraphs[i])
    last = els[-1]
    last.addnext(new_para(doc, text))


def swap_image(doc, cap_kw, png_path, width_in):
    from PIL import Image
    ci = para(doc, lambda p: (p.style.name or "") == "Caption" and cap_kw in p.text)
    if ci < 0:
        print("   ! khong thay caption:", cap_kw)
        return False
    # tim paragraph ve ngay truoc caption
    di = ci - 1
    while di >= 0:
        if "<w:drawing" in doc.paragraphs[di]._p.xml or "blip" in doc.paragraphs[di]._p.xml:
            break
        di -= 1
    if di < 0:
        print("   ! khong thay hinh cho:", cap_kw)
        return False
    p = doc.paragraphs[di]
    ns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    blips = p._p.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
    rid = next(blips).get(ns + "embed")
    part = doc.part.related_parts[rid]
    part._blob = open(png_path, "rb").read()
    w, h = Image.open(png_path).size
    ratio = float(h) / w
    for sh in doc.inline_shapes:
        b = sh._inline.graphic.graphicData.pic.blipFill.blip
        if b.embed == rid:
            wd = width_in
            ht = wd * ratio
            if ht > 8.6:
                ht = 8.6
                wd = ht / ratio
            sh.width = Inches(wd)
            sh.height = Inches(ht)
    print("   da doi anh:", cap_kw)
    return True


# ============================ NC1 ============================
print("== NC1")
d = Document("Bao_cao_1_truc_Nghien_cuu.docx")
# p16: bo chuoi lenh do o cuoi, giu noi dung pham vi
i = para(d, lambda p: p.text.startswith("Phạm vi tập trung vào mô hình công suất nhỏ"))
strip_red_runs(d.paragraphs[i])
set_text(d.paragraphs[i], "Phạm vi tập trung vào mô hình công suất nhỏ, chuyển động trong mặt phẳng "
         "Đông-Tây và xử lý tín hiệu cảm biến. Báo cáo không thiết kế hệ thống hòa lưới, bộ nghịch lưu "
         "hoặc MPPT; không khẳng định mức tăng sản lượng trước khi đo; không mở rộng sang cơ cấu giàn quy "
         "mô nhà máy. Photodiode được trình bày để so sánh lựa chọn cảm biến, không mặc định là phần tử "
         "của mạch chính.")
# xoa muc 2.6 cong tac hanh trinh
i = para(d, h2("2.6."))
remove_elems(section_elems(d, d.paragraphs[i]))
renumber(d, r"(?<![\d.])2\.(7|8|9|10)\.", {"2.7.": "2.6.", "2.8.": "2.7.", "2.9.": "2.8.", "2.10.": "2.9."})
# doan 2.6.1-2.6.3 (cu 2.7.x): bo chu "Viet don gian thoi", giu noi dung
i = para(d, lambda p: "Viết đơn giản thôi" in p.text)
if i >= 0:
    dered(d.paragraphs[i])
    set_text(d.paragraphs[i], d.paragraphs[i].text.replace(" Viết đơn giản thôi", "").replace("Viết đơn giản thôi", "").strip())
for p in d.paragraphs:
    dered(p)
# ten 3 phuong phap: bo chu Nhom
i = para(d, h2("2.8. Ba phương pháp"))
set_text(d.paragraphs[i], "2.8. Ba phương pháp bám nắng xem xét trong đề tài")
i = para(d, lambda p: p.text.strip().startswith("2.8.1."))
set_text(d.paragraphs[i], "2.8.1. Vòng hở theo thời gian (thuật toán thiên văn)")
i = para(d, lambda p: p.text.strip().startswith("2.8.2."))
set_text(d.paragraphs[i], "2.8.2. Vòng kín dùng cảm biến quang trở (LDR)")
i = para(d, lambda p: p.text.strip().startswith("2.8.3."))
set_text(d.paragraphs[i], "2.8.3. Phương pháp hybrid (kết hợp), phương án lựa chọn")
for p in d.paragraphs:
    t = p.text
    nt = t.replace("Nhóm 1 – ", "").replace("Nhóm 2 – ", "").replace("Nhóm 3 – ", "")
    nt = nt.replace("Nhóm 1", "Vòng hở thiên văn").replace("Nhóm 2", "Vòng kín quang trở").replace("Nhóm 3", "Phương pháp hybrid")
    nt = nt.replace("ba nhóm", "ba phương pháp")
    if nt != t:
        set_text(p, nt)
# 3.4: tham khao
i = para(d, h2("3.4."))
set_text(d.paragraphs[i], "3.4. Tham khảo mức tăng sản lượng của hệ bám nắng")
els = section_elems(d, d.paragraphs[i])
note1 = new_para(d, "Chưa có số liệu đo thực tế nên mục này trình bày theo dạng tham khảo: khoảng tăng "
                    "sản lượng công bố trong tài liệu và kết quả mô phỏng của đề tài đặt cạnh nhau để đối "
                    "chiếu; toàn bộ sẽ kiểm chứng lại bằng đo đạc khi có thiết bị.")
note2 = new_para(d, "Các tổng quan về hệ bám nắng công bố mức tăng sản lượng khoảng 20–45% so với giàn cố "
                    "định tùy vĩ độ và kiểu bám, trong đó bám hai trục cao hơn một trục [11]. Kết quả mô "
                    "phỏng của đề tài ở bảng và biểu đồ dưới đây nằm trong khoảng đó và chỉ dùng làm tham "
                    "khảo định hướng thiết kế.")
insert_after(els[0], [note1, note2])
for p in d.paragraphs:
    if (p.style.name or "") == "Caption" and "thu thêm" in p.text:
        set_text(p, p.text + " (mô phỏng tham khảo, sẽ kiểm chứng)")
add_ref(d, "[11] H. Mousazadeh, A. Keyhani, A. Javadi, H. Mobli, K. Abrinia, A. Sharifi, "
           "'A review of principle and solar-tracking methods for increasing PV systems efficiency', "
           "Renewable and Sustainable Energy Reviews, 13(8), 2009.")
# 3.5: bo chu trong ngoac
i = para(d, h2("3.5."))
set_text(d.paragraphs[i], "3.5. Lưu đồ thuật toán tổng quát")
# 3.6: viet lai kieu tran thuat
i = para(d, h2("3.6."))
els = section_elems(d, d.paragraphs[i])
set_text(d.paragraphs[i], "3.6. Phân bố nội dung giữa các quyển trong đồ án")
remove_elems(els[1:])
body = [new_para(d, "Quyển chế tạo của đồ án trình bày toàn bộ phần cứng: bảy sheet mạch nguyên lý EasyEDA, "
                    "mạch động lực cầu H bốn TIP41C, khung cơ khí một trục và quy trình lắp ráp, hiệu chuẩn, "
                    "đo đạc trên bench."),
        new_para(d, "Quyển lập trình trình bày môi trường Arduino IDE, các hàm xử lý quang trở, cầu H, DS1307, "
                    "LCD và biến trở hồi tiếp, lưu đồ thuật toán từng phần cùng chương trình tham khảo ở phụ lục."),
        new_para(d, "Các tham số thống nhất giữa ba quyển (ngưỡng phát lệnh, vùng chết, chu kỳ thiên văn và "
                    "chu kỳ tinh chỉnh) được ghi ở mục 2.8 quyển chế tạo và mục 2.12 quyển lập trình để tiện "
                    "đối chiếu khi làm mạch và viết code.")]
insert_after(els[0], body)
# 4.1: xoa 2 bullet, viet lai 1 bullet
i = para(d, lambda p: p.text.startswith("Hoàn thành mô phỏng kiểm chứng"))
if i >= 0:
    remove_elems([d.paragraphs[i]._p])
i = para(d, lambda p: p.text.startswith("Hoàn thành sơ đồ khối hệ thống"))
if i >= 0:
    remove_elems([d.paragraphs[i]._p])
i = para(d, lambda p: p.text.startswith("Hoàn thành bộ công thức thiên văn cài trên ESP32"))
set_text(d.paragraphs[i], "Hoàn thành bảng tra góc đặt tấm pin theo giờ phục vụ cài đặt thiên văn trên ESP32: "
         "ví dụ ngày 21/3 tại Mỹ Hào, 8h khung quay +62° về phía Đông, 10h +32°, 12h 0°, 14h −32°, 16h −62° "
         "(quy ước dương về phía Đông; số lấy từ khối tính toán, sẽ kiểm chứng bằng đo đạc).")
# xoa 4.2 ma tran, doi 4.3 -> 4.2 va viet lai
i = para(d, h2("4.2."))
remove_elems(section_elems(d, d.paragraphs[i]))
i = para(d, h2("4.3."))
els = section_elems(d, d.paragraphs[i])
set_text(d.paragraphs[i], "4.2. Các công việc tiếp theo (tuần 5/10 – 10/10/2026 và tuần kế)")
remove_elems(els[1:])
bul = [new_para(d, t, style="List Bullet") for t in (
    "Hỗ trợ bên chế tạo: lắp mạch đọc quang trở và mạch động lực cầu H, chạy thử động cơ trục vít trên bench để có số liệu đo.",
    "Chế tạo mạch điều khiển ESP32 đọc giờ DS1307 và điện áp quang trở, phục vụ đo đạc kiểm chứng các kết quả chương 3.",
    "Đo kiểm chứng bảng tra giờ – góc đặt và các biểu đồ mô phỏng khi có thiết bị; các số liệu hiện tại giữ nguyên dạng tham khảo.",
    "Vẽ lại bản vẽ cơ khí tấm pin 100 W và bổ sung vào quyển chế tạo.")]
insert_after(els[0], bul)
for p in d.paragraphs:
    dered(p)
d.save("Bao_cao_1_truc_Nghien_cuu.docx")
print("   NC1 xong")

# ============================ NC2 ============================
print("== NC2")
src = Document("Bao_cao_1_truc_Nghien_cuu.docx")
si = para(src, h2("2.8. Ba phương pháp"))
src_els = section_elems(src, src.paragraphs[si])
copied = [deepcopy(el) for el in src_els]
for el in copied:  # danh so lai 2.8 -> 2.9
    from docx.text.paragraph import Paragraph
    pp = Paragraph(el, src)
    if (pp.style.name or "").startswith(("Heading 2", "Heading 3")) and pp.text.strip().startswith("2.8"):
        for r in pp.runs:
            r.text = re.sub(r"^2\.8", "2.9", r.text, count=1) if r.text.strip().startswith("2.8") else r.text
        if pp.runs and not pp.runs[0].text.strip().startswith("2.9"):
            pp.runs[0].text = re.sub(r"2\.8", "2.9", pp.runs[0].text, count=1)
d = Document("Bao_cao_2_truc_Nghien_cuu.docx")
i = para(d, h2("2.9. Ba phương pháp"))
els = section_elems(d, d.paragraphs[i])
ref = els[0].getprevious()
remove_elems(els)
insert_after(ref, copied)
# chuong 3 khac di
i = para(d, h1("CHƯƠNG 3"))
set_text(d.paragraphs[i], "CHƯƠNG 3. KẾT QUẢ NGHIÊN CỨU PHƯƠNG PHÁP HYBRID CHO HỆ HAI TRỤC BẰNG MÔ PHỎNG")
i = para(d, h2("3.1."))
els = section_elems(d, d.paragraphs[i])
set_text(d.paragraphs[i], "3.1. Quỹ đạo Mặt Trời và yêu cầu bám cho hai khớp (số liệu tham khảo)")
note = new_para(d, "Khác mô hình một trục chỉ quay Đông–Tây, hệ hai trục phải giữ pháp tuyến tấm pin trùng "
                   "hướng Mặt Trời ở cả hai phương: khớp nâng bám góc cao α còn khớp phương vị bám góc γ, "
                   "và hai khớp không được tranh chấp nhau khi sai lệch còn nhỏ. Các đồ thị và con số trong "
                   "mục này lấy từ công cụ tính quỹ đạo chạy trên máy tính, dùng làm tham khảo định hướng "
                   "thiết kế; chưa phải kết quả đo thực tế và sẽ kiểm chứng lại.")
insert_after(els[0], [note])
i = para(d, h2("3.4."))
set_text(d.paragraphs[i], "3.4. Lợi ích năng lượng của cấu hình hai trục (tham khảo, chờ kiểm chứng)")
els = section_elems(d, d.paragraphs[i])
note = new_para(d, "Biểu đồ dưới đây là kết quả mô phỏng tham khảo trên chuỗi ngày điển hình, chưa qua đo "
                   "đạc; mục đích là ước lượng mức đáng đầu tư của khớp thứ hai. Số liệu sẽ kiểm chứng lại "
                   "bằng thiết bị đo và được ghi vào mục việc làm tiếp theo của chương 4.")
insert_after(els[0], [note])
i = para(d, h2("3.5."))
set_text(d.paragraphs[i], "3.5. Lưu đồ thuật toán bám nắng bằng bốn LDR (bản vẽ của sinh viên)")
i = para(d, lambda p: p.text.startswith("Lưu đồ hai trục khác bản một trục"))
set_text(d.paragraphs[i], "Lưu đồ do sinh viên vẽ tập trung vào vòng tinh chỉnh quang trở của hai khớp: xét "
         "cân bằng nghiêng trước rồi mới đến phương vị, mỗi lần chỉ dịch một bước nhỏ về phía nhận sáng mạnh "
         "hơn và đọc lại sau T_đọc. Nhánh định vị thô thiên văn và nhánh giữ vị trí khi mây mù mô tả ở mục 3.3.")
for p in d.paragraphs:
    if (p.style.name or "") == "Caption" and "Lưu đồ tổng quát chương trình hybrid hai trục" in p.text:
        set_text(p, "Hình 5. Lưu đồ thuật toán bám nắng bằng bốn LDR do sinh viên vẽ")
# xoa 3.6
i = para(d, h2("3.6."))
remove_elems(section_elems(d, d.paragraphs[i]))
# 4.1: xoa 4 bullet bia, them bullet that
i = para(d, h2("4.1."))
els = section_elems(d, d.paragraphs[i])
remove_elems(els[1:])
bul = [new_para(d, t, style="List Bullet") for t in (
    "Hoàn thành công cụ tính quỹ đạo Mặt Trời và góc đặt hai khớp chạy trên máy tính; số liệu dùng làm tham khảo và sẽ kiểm chứng lại bằng đo đạc.",
    "Hoàn thành tổng quan tài liệu các phương pháp bám nắng hai trục và lựa chọn phương pháp hybrid (chương 2).",
    "Hoàn thành bản thảo chương 1 và chương 2 của ba quyển đồ án 2 theo sườn chung với đồ án 1.")]
insert_after(els[0], bul)
# 4.2: ghi chu tham khao
i = para(d, h2("4.2."))
els = section_elems(d, d.paragraphs[i])
strip_red_runs(d.paragraphs[para(d, lambda p: "hiện tại mới đang tháng 10" in p.text)])
note = new_para(d, "Bảng ma trận dưới đây là số liệu tính toán tham khảo từ công thức thiên văn chạy trên máy "
                   "tính, chưa qua đo đạc; sẽ kiểm chứng lại khi có thiết bị đo.")
insert_after(els[0], [note])
# 4.3: xoa bullet 3D
i = para(d, lambda p: p.text.startswith("Hoàn thiện bản vẽ 3D khớp nâng nghiêng"))
if i >= 0:
    remove_elems([d.paragraphs[i]._p])
for p in d.paragraphs:
    dered(p)
d.save("Bao_cao_2_truc_Nghien_cuu.docx")
print("   NC2 xong")

# ============================ CT2 ============================
print("== CT2")
copied = [deepcopy(el) for el in src_els]
from docx.text.paragraph import Paragraph as _P
for el in copied:
    pp = _P(el, src)
    if (pp.style.name or "").startswith(("Heading 2", "Heading 3")):
        for r in pp.runs:
            if r.text.strip().startswith("2.8"):
                r.text = re.sub(r"2\.8", "2.7", r.text, count=1)
d = Document("Bao_cao_2_truc_Che_tao.docx")
i = para(d, lambda p: p.text.strip().startswith("2.7. Ba phương pháp"))
j = para(d, h2("2.8."), i)
body = d.element.body
els = list(body)[body_idx(d, d.paragraphs[i]._p):body_idx(d, d.paragraphs[j]._p)]
ref = els[0].getprevious()
remove_elems(els)
insert_after(ref, copied)
# 3.5: co khi thuan
i = para(d, h2("3.5."))
els = section_elems(d, d.paragraphs[i])
set_text(d.paragraphs[i], "3.5. Các kết cấu cơ khí và gá công tắc hành trình ngắt động cơ")
remove_elems(els[1:])
body = [new_para(d, "Hệ hai trục trong tuần này chế tạo thuần cơ khí: tầng đế thép có bulông cân bằng, khớp "
                    "phương vị dùng ổ bi mặt phẳng và bạc lót, khớp nâng nghiêng có đối trọng để mô-men trọng "
                    "trường dưới 3 N·m; khung nhôm định hình bắt tấm pin 100 W – 4 kg đối xứng qua trục nâng."),
        new_para(d, "Công tắc hành trình được gá trên giá cơ khí ở hai đầu hành trình của mỗi khớp; tiếp điểm "
                    "nối vào mạch ngắt động cơ sao cho chạm hành trình chiều nào thì cắt điện chiều đó. Việc gá "
                    "công tắc thuộc phần cơ khí lắp ráp; các mạch điện còn lại (nguồn, cầu H, cảm biến) dùng "
                    "chung hồ sơ mạch của đồ án 1 và tích hợp ở tuần chế tạo mạch."),
        new_para(d, "Các chi tiết in 3D gồm khối gá bốn LDR nghiêng β_s, ốp khớp phương vị, tay đòn khớp nâng; "
                    "vật liệu PETG điền đầy 40%. Danh mục chi tiết cơ khí và bản vẽ từng part liệt kê ở mục 3.6 "
                    "và mục 4.2.")]
insert_after(els[0], body)
# 3.6: bang chi tiet co khi
i = para(d, h2("3.6."))
els = section_elems(d, d.paragraphs[i])
set_text(d.paragraphs[i], "3.6. Danh mục chi tiết cơ khí")
remove_elems(els[1:])
rows = [["Chi tiết", "Quy cách / vật liệu", "Số lượng"],
        ["Tấm pin năng lượng", "100 W, khoảng 4 kg", "1"],
        ["Khung mang pin", "Nhôm định hình 30×30", "1 bộ"],
        ["Tầng đế", "Thép hộp, bulông cân bằng", "1"],
        ["Khớp phương vị", "Ổ bi mặt phẳng + bạc lót", "1"],
        ["Trục nâng nghiêng", "Thép tròn Ø20 + gối đỡ", "2"],
        ["Đối trọng cân mô-men", "Thép 5 kg", "2"],
        ["Động cơ gạt nước", "12 V, khoảng 60 W, trục vít tự hãm", "2"],
        ["Biến trở hồi tiếp góc", "10 kΩ, gắn đồng trục", "2"],
        ["Khối gá bốn LDR", "In PETG, nghiêng β_s = 30°", "1"],
        ["Công tắc hành trình + giá gá", "Chặn hai đầu hành trình mỗi khớp", "4"],
        ["Bulông, ốc, bản lề", "Inox M5–M8", "1 bộ"]]
cap = new_para(d, "Bảng 5. Danh mục chi tiết cơ khí của mô hình hai trục", style="Caption")
tbl = d.add_table(rows=len(rows), cols=3)
tbl.style = "Table Grid"
for a, row in enumerate(rows):
    for b, val in enumerate(row):
        tbl.cell(a, b).text = val
tel = tbl._tbl
tel.getparent().remove(tel)
insert_after(els[0], [cap, tel])
# 3.7: quy trinh co khi du kien
i = para(d, h2("3.7."))
els = section_elems(d, d.paragraphs[i])
set_text(d.paragraphs[i], "3.7. Quy trình lắp ráp cơ khí dự kiến")
remove_elems(els[1:])
bul = [new_para(d, t, style="List Bullet") for t in (
    "Lắp tầng đế và khớp phương vị: kiểm tra quay trơn 360° và giới hạn mềm ±120°.",
    "Lắp khớp nâng nghiêng, đối trọng; cân mô-men trọng trường dưới 3 N·m.",
    "In và lắp khối gá bốn LDR nghiêng β_s; đo lại bốn góc gá sau khi bắt vít.",
    "Gá công tắc hành trình ở hai đầu hành trình mỗi khớp; thử chặn hành trình bằng tay trước khi lắp động cơ.")]
insert_after(els[0], bul)
# 4.1: solidworks
i = para(d, h2("4.1."))
els = section_elems(d, d.paragraphs[i])
set_text(d.paragraphs[i], "4.1. Kết quả đạt được trong tuần 5/10 – 10/10/2026")
remove_elems(els[1:])
bul = [new_para(d, t, style="List Bullet") for t in (
    "Làm quen phần mềm SolidWorks: dựng phác tầng đế, khớp phương vị và khớp nâng nghiêng của hệ hai trục.",
    "Mô phỏng kích thước sơ bộ các chi tiết theo tấm pin 100 W – 4 kg và hành trình hai khớp trước khi vẽ chính thức.")]
insert_after(els[0], bul)
# 4.2: them bullet chia part
i = para(d, lambda p: "Chi nhỏ các bản vẽ 3d" in p.text)
if i >= 0:
    remove_elems([d.paragraphs[i]._p])
i = para(d, h2("4.2."))
els = section_elems(d, d.paragraphs[i])
add = [new_para(d, "Chia nhỏ bản vẽ 3D thành nhiều part riêng (đế, khớp phương vị, khớp nâng, đối trọng, khối "
                   "gá LDR, tay đòn) và vẽ lại từng part trong SolidWorks.", style="List Bullet")]
insert_after(els[-1], add)
for p in d.paragraphs:
    dered(p)
d.save("Bao_cao_2_truc_Che_tao.docx")
print("   CT2 xong")

# ============================ LT1 ============================
print("== LT1")
d = Document("Bao_cao_1_truc_Lap_trinh.docx")
# xoa 3.1-3.4
for t in ("3.1. Thiết kế mạch", "3.2. Chế tạo mạch", "3.3. Thiết kế cơ khí", "3.4. Hiệu chuẩn và đo đạc"):
    i = para(d, h2(t))
    if i >= 0:
        remove_elems(section_elems(d, d.paragraphs[i]))
i = para(d, lambda p: (p.style.name or "") == "Heading 2" and not p.text.strip())
if i >= 0:
    remove_elems([d.paragraphs[i]._p])
renumber(d, r"(?<![\d.])3\.(5|6|7|8|9|10|11)\.",
         {"3.5.": "3.1.", "3.6.": "3.2.", "3.7.": "3.3.", "3.8.": "3.4.",
          "3.9.": "3.5.", "3.10.": "3.6.", "3.11.": "3.7."})
i = para(d, h2("3.6. Lưu đồ"))
set_text(d.paragraphs[i], "3.6. Lưu đồ thuật toán từng phần và tổng quát")
# xoa 3 ghi chu do ve luu do
for kw in ("Lưu đồ đọc adc đang bị sai", "Lưu đồ điều khiển mô tơ qua cầu h cũng đang sai",
           "Lưu đồ này gần đúng thiếu phần kết thúc", "Các chương trình cho esp nên để ở phụ lục"):
    i = para(d, lambda p, kw=kw: p.text.strip().lower().startswith(kw.lower()))
    if i >= 0:
        remove_elems([d.paragraphs[i]._p])
# chuyen luu do tong quat xuong truoc muc code
ic = para(d, lambda p: (p.style.name or "") == "Caption" and "tổng quát" in p.text)
if ic >= 0:
    di = ic - 1
    while di >= 0 and "blip" not in d.paragraphs[di]._p.xml:
        di -= 1
    cap_el = d.paragraphs[ic]._p
    img_el = d.paragraphs[di]._p
    ih = para(d, h2("3.7."), ic)
    head_el = d.paragraphs[ih]._p
    head_el.addprevious(img_el)
    head_el.addprevious(cap_el)
# 3.7: code -> phu luc + snippet
i = para(d, h2("3.7."))
set_text(d.paragraphs[i], "3.7. Yêu cầu phần mềm và các hàm thực hiện từng khối")
els = section_elems(d, d.paragraphs[i])
code_els = []
for el in els[1:]:
    if el.tag.endswith("}p"):
        pp = _P(el, d)
        if pp.runs and (pp.runs[0].font.name or "").startswith(("Consolas", "Courier")):
            code_els.append(el)
refs_i = para(d, h1("TÀI LIỆU THAM KHẢO"))
ref_el = d.paragraphs[refs_i]._p
phu_luc = new_para(d, "PHỤ LỤC A. CHƯƠNG TRÌNH THAM KHẢO CHO ESP32 MỘT TRỤC", style="Heading 1")
pl_intro = new_para(d, "Chương trình hoàn chỉnh ghép từ các khối hàm ở mục 3.7, giữ nguyên cấu trúc khi nạp "
                       "cho ESP32 DevKit.")
ref_el.addprevious(phu_luc)
ref_el.addprevious(pl_intro)
for el in code_els:
    ref_el.addprevious(el)
for el in list(section_elems(d, d.paragraphs[para(d, h2("3.7."))])):
    if el.tag.endswith("}p"):
        pp = _P(el, d)
        if pp.runs and (pp.runs[0].font.name or "").startswith(("Consolas", "Courier")):
            el.getparent().remove(el)
# snippet nho vao 3.7
snip = [
    ("3.7.1. Đọc giá trị ADC bốn kênh quang trở",
     ["int docQuangTro(int chan, float kCal) {",
      "  long s = 0;",
      "  for (int i = 0; i < 16; i++) { s += analogRead(chan); delay(2); }",
      "  return (int)((s / 16.0) * kCal);",
      "}"]),
    ("3.7.2. Điều khiển chiều quay và tốc độ động cơ qua cầu H",
     ["void quayMotor(int pinThuan, int pinNguoc, int chieu, int pwm) {",
      "  ledcWrite(KENH_PWM, pwm);            // toc do",
      "  digitalWrite(pinThuan, chieu > 0 ? LOW : HIGH);   // tich cuc thap",
      "  digitalWrite(pinNguoc, chieu < 0 ? LOW : HIGH);",
      "}",
      "void khoaMotor(int pinThuan, int pinNguoc) {",
      "  digitalWrite(pinThuan, HIGH); digitalWrite(pinNguoc, HIGH);",
      "}"]),
    ("3.7.3. Đọc thời gian từ DS1307",
     ["DateTime bayGio = RTC.now();",
      "int ngay = bayGio.day(); int thang = bayGio.month();",
      "int gio = bayGio.hour(); int phut = bayGio.minute();"]),
    ("3.7.4. Hiển thị hai dòng lên LCD I2C",
     ["lcd.clear();",
      "lcd.setCursor(0, 0); lcd.print(\"Gio: 10:35  A=47.2\");",
      "lcd.setCursor(0, 1); lcd.print(\"Goc pin: -12  e1=+85\");"]),
    ("3.7.5. Đọc biến trở hồi tiếp suy ra góc khung",
     ["float gocHoiTiep() {",
      "  int v = analogRead(PIN_BIEN_TRO);",
      "  return noiSuyBaDiem(v, V_MIN, V_MID, V_MAX);",
      "}"]),
]
cur = d.paragraphs[para(d, h2("3.7."))]._p
new_els = [new_para(d, "Mỗi khối xử lý trong chương trình được viết thành hàm riêng để dễ kiểm thử trên "
                       "bench; năm khối chính liệt kê dưới đây, chương trình ghép hoàn chỉnh đặt ở Phụ lục A.")]
for head, lines in snip:
    new_els.append(new_para(d, head, style="Heading 3"))
    for ln in lines:
        new_els.append(new_para(d, ln, font="Consolas", size=9))
new_els.append(new_para(d, "Ghép năm khối hàm trên theo lưu đồ tổng quát ở mục 3.6 được chương trình hoàn "
                           "chỉnh ở Phụ lục A; các yêu cầu phần mềm đều bám đúng lưu đồ, không thêm nhánh ngoài."))
insert_after(cur, new_els)
# 4.1 / 4.2
i = para(d, lambda p: p.text.startswith("Hoàn thành viết và nạp code hybrid một trục"))
set_text(d.paragraphs[i], "Hoàn thành viết code hybrid một trục trên Arduino IDE theo lưu đồ mới (ba nhánh "
         "thiên văn – LDR – giữ vị trí khi mây mù, hiển thị hai dòng LCD); chưa nạp chạy trên mạch thật vì "
         "tuần này mới có sơ đồ nguyên lý, chưa ra mạch in.")
i = para(d, lambda p: p.text.strip().startswith("Ghi thêm các công việc theo thực tế"))
if i >= 0:
    remove_elems([d.paragraphs[i]._p])
i = para(d, h2("4.2."))
els = section_elems(d, d.paragraphs[i])
add = [new_para(d, t, style="List Bullet") for t in (
    "Nạp và chạy thử code hybrid trên mạch in ngay khi mạch được chế tạo xong.",
    "Hỗ trợ bên chế tạo lắp mạch đọc quang trở và mạch động lực cầu H để có mạch đo thật.",
    "Hiệu chuẩn và đo đạc trên mạch: chuyển sang tuần sau, khi code chạy được trên mạch.",
    "Thiết kế cơ khí phục vụ phần mềm (gá biến trở đồng trục, giá chặn hành trình): chuyển sang quyển chế tạo khi bắt đầu làm cơ khí.")]
insert_after(els[-1], add)
for p in d.paragraphs:
    dered(p)
d.save("Bao_cao_1_truc_Lap_trinh.docx")
print("   LT1 xong")

# ============================ doi anh ============================
print("== doi anh")
V = "hinh_ve/"
swap_image(Document("Bao_cao_1_truc_Nghien_cuu.docx"), "Lưu đồ tổng quát", V + "luu_do_tong_quat_1_truc.png", 6.2) or None
d = Document("Bao_cao_1_truc_Nghien_cuu.docx")
swap_image(d, "Lưu đồ tổng quát", V + "luu_do_tong_quat_1_truc.png", 6.2)
d.save("Bao_cao_1_truc_Nghien_cuu.docx")
d = Document("Bao_cao_2_truc_Nghien_cuu.docx")
swap_image(d, "Lưu đồ thuật toán bám nắng bằng bốn LDR", "Luu_do_thuat_toan_bam_nang_4_LDR.png", 6.0)
d.save("Bao_cao_2_truc_Nghien_cuu.docx")
for f, tag in (("Bao_cao_1_truc_Lap_trinh.docx", "1_truc"), ("Bao_cao_2_truc_Lap_trinh.docx", "2_truc")):
    d = Document(f)
    swap_image(d, "thiên văn", V + "luu_do_thien_van.png", 5.6)
    swap_image(d, "đọc ADC", V + "luu_do_doc_adc.png", 5.6)
    swap_image(d, "cầu H", V + "luu_do_dieu_khien_motor.png", 5.6)
    swap_image(d, "LCD", V + "luu_do_lcd.png", 5.4)
    swap_image(d, "biến trở", V + "luu_do_bien_tro.png", 5.4)
    swap_image(d, "tổng quát", V + "luu_do_tong_quat_%s.png" % tag, 6.2)
    d.save(f)
print("HOAN TAT")
