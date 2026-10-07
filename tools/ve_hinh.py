# -*- coding: utf-8 -*-
"""Sơ đồ kỹ thuật đề xuất cho sáu quyển; không biểu thị phần cứng đã chế tạo."""
from __future__ import annotations

import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, Ellipse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hinh_ve")
EDGE, TXT = "#20252b", "#111820"
BLUE, PALE, GREEN, RED = "#dceaf7", "#f2f4f6", "#e4f2e9", "#f8e4e4"


def canvas(width, height, xlim=(0, 100), ylim=(0, 100)):
    fig, ax = plt.subplots(figsize=(width, height), dpi=190)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    ax.set_aspect("equal")
    return fig, ax


def textwrap_lines(text, width=28):
    return "\n".join("\n".join(textwrap.wrap(line, width)) if line else "" for line in text.split("\n"))


def box(ax, x, y, w, h, text, fc="white", fs=8, rounded=False, wrap=28, lw=0.9):
    shape = (FancyBboxPatch((x-w/2, y-h/2), w, h,
                            boxstyle="round,pad=0.02,rounding_size=1.2" if rounded else "square,pad=0",
                            facecolor=fc, edgecolor=EDGE, linewidth=lw)
             if rounded else Rectangle((x-w/2, y-h/2), w, h, facecolor=fc, edgecolor=EDGE, linewidth=lw))
    ax.add_patch(shape)
    ax.text(x, y, textwrap_lines(text, wrap), ha="center", va="center", color=TXT,
            fontsize=fs, linespacing=1.25)


def decision(ax, x, y, w, h, text, fs=7.5, wrap=22):
    ax.add_patch(Polygon([(x,y+h/2),(x+w/2,y),(x,y-h/2),(x-w/2,y)],
                         closed=True, facecolor="white", edgecolor=EDGE, linewidth=0.9))
    ax.text(x, y, textwrap_lines(text,wrap), ha="center", va="center", fontsize=fs, color=TXT,
            linespacing=1.2)


def arrow(ax, x1,y1,x2,y2,label=None,lx=None,ly=None,fs=7.2):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),
                arrowprops=dict(arrowstyle="-|>",color=EDGE,lw=0.9,shrinkA=0,shrinkB=0))
    if label:
        ax.text(lx if lx is not None else (x1+x2)/2,
                ly if ly is not None else (y1+y2)/2,
                label,ha="center",va="center",fontsize=fs,color=TXT,
                bbox=dict(fc="white",ec="none",pad=0.2))


def line(ax,x1,y1,x2,y2,lw=0.9):
    ax.plot([x1,x2],[y1,y2],color=EDGE,lw=lw)


def title(ax, text, y=97, fs=10):
    ax.text(50,y,text,ha="center",va="center",fontsize=fs,fontweight="bold",color=TXT)


def save(fig, filename):
    os.makedirs(OUT,exist_ok=True)
    fig.savefig(os.path.join(OUT,filename),facecolor="white",bbox_inches="tight",pad_inches=0.16)
    plt.close(fig)
    print("da ve:",filename)


def so_do_khoi(truc=1):
    two=truc==2
    fig,ax=canvas(10.2,6.2,(0,110),(0,68)); title(ax,f"SƠ ĐỒ KHỐI CHỨC NĂNG – HỆ {'HAI' if two else 'MỘT'} TRỤC",66,9.8)
    box(ax,15,52,26,10,"Cụm LDR + chia áp\n4 kênh ADC",BLUE,7.6,wrap=25)
    box(ax,15,38,26,9,"RTC DS1307\n(giờ dân dụng)",PALE,7.6,wrap=25)
    box(ax,15,24,26,9,"POT hồi tiếp +\ncông tắc giới hạn",PALE,7.6,wrap=25)
    box(ax,51,42,28,22,"ESP32 DevKit\nđọc cảm biến, tính góc,\nđiều khiển có giới hạn,\nhiển thị trạng thái",BLUE,8.0,wrap=26)
    box(ax,51,18,28,10,"LCD1602 / PCF8574\nI²C",PALE,7.6,wrap=25)
    arrow(ax,28,52,37,48); arrow(ax,28,38,37,42); arrow(ax,28,24,37,37)
    arrow(ax,51,31,51,23)
    count=2 if two else 1
    for i in range(count):
        y=50-i*24
        label="AZIMUTH" if i==0 else "TILT"
        box(ax,86,y,24,10,f"Cầu H {label}\n(4 TIP41C + opto)",PALE,7.3,wrap=23)
        box(ax,86,y-13,24,8,f"Motor 12 V\n{'phương vị' if i==0 else 'nâng'}",GREEN,7.3,wrap=23)
        arrow(ax,65,42,74,y); arrow(ax,86,y-5,86,y-9)
    box(ax,51,4,78,7,"Nguồn 12 V → cầu H; nguồn DC–DC phù hợp → ESP32/LCD. Cần liên động E-stop phần cứng.",PALE,7.2,wrap=75)
    ax.text(98,62,"Motor trục vít: tính tự hãm\nchưa xác minh bằng thử tải",ha="center",va="center",fontsize=7.1,color=TXT)
    save(fig,f"so_do_khoi_{truc}_truc.png")


def so_do_ket_noi(truc=1):
    two=truc==2
    fig,ax=canvas(11.2,6.4,(0,116),(0,68))
    title(ax,f"PINOUT ĐỀ XUẤT – ESP32 HỆ {'HAI' if two else 'MỘT'} TRỤC",65,9.8)
    box(ax,57,33,28,48,"ESP32 DEVKIT\n\nADC1 / ADC2\n\nI²C GPIO21 / GPIO22",BLUE,7.8,wrap=26,lw=1.1)
    left=[("LDR ET / WT / EB / WB\nGPIO25 / 26 / 27 / 14 (ADC2)",49),
          ("POT azimuth\nGPIO36 (ADC1)",37),
          (("POT beta\nGPIO4 (ADC2)" if two else "Đo áp pin\nGPIO39 (ADC1)"),25),
          ("DS1307 + LCD\nI²C GPIO21 / 22",13)]
    right=[("Cầu H AZ thuận/ngược\nGPIO19 / 18",50),
           ("Limit AZ+ / AZ−\nGPIO34 / 35",37),
           ("E-stop NC-to-GND\nGPIO23; HIGH=dừng",24)]
    if two:
        right=[("Cầu H AZ thuận/ngược\nGPIO19 / 18",51),
               ("Cầu H beta lên/xuống\nGPIO16 / 13",42),
               ("Limit AZ+ / AZ−\nGPIO34 / 35",33),
               ("Limit beta+ / beta−\nGPIO32 / 33",24),
               ("E-stop NC-to-GND\nGPIO23; HIGH=dừng",15)]
    for label,y in left:
        box(ax,15,y,30,8,label,PALE,7.0,wrap=29)
        line(ax,30,y,43,y)
    for label,y in right:
        box(ax,101,y,30,8,label,PALE,7.0,wrap=29)
        line(ax,71,y,86,y)
    note=("LDR trên ADC2: Wi-Fi tắt. GPIO34–39 chỉ input, không pull nội; limit 34/35 cần bias ngoài. "
          "GPIO2/5 tránh do strap/khởi động. Pinout đề xuất; đối chiếu biến thể bo, chưa phải schematic/as-built.")
    ax.text(58,3,note,ha="center",va="center",fontsize=6.7,color=TXT,wrap=True)
    save(fig,f"so_do_ket_noi_{truc}_truc.png")


def so_do_3_phuong_phap():
    fig,ax=canvas(10.5,7.0,(0,106),(0,72)); title(ax,"BA PHƯƠNG PHÁP BÁM NẮNG ĐƯỢC SO SÁNH",69,9.7)
    rows=[("A. Thiên văn / vòng hở",55,["RTC ngày/giờ","Tính α, γ","Đặt góc motor"]),
          ("B. LDR / vòng kín",36,["Bốn LDR","Tính e1, e2","Bù sai lệch"]),
          ("C. Hybrid / phương án chọn",17,["Thiên văn: định vị thô","LDR: hiệu chỉnh khi đủ sáng","Mây/đêm: giữ vị trí"])]
    for label,y,cells in rows:
        ax.text(2,y+6,label,fontsize=8.1,fontweight="bold",color=TXT)
        xs=[19,53,87] if len(cells)==3 else []
        ws=[23,27,25]
        for i,(txt,x) in enumerate(zip(cells,xs)):
            box(ax,x,y,ws[i],8,txt,BLUE if i==0 else PALE,7.1,wrap=25)
            if i: arrow(ax,xs[i-1]+ws[i-1]/2,y,x-ws[i]/2,y)
    ax.text(53,3,"e1/e2 và xử lý ADC được triển khai riêng trong Lập trình đồ án 1; không lặp code ở quyển khác.",
            ha="center",fontsize=7.2,color=TXT)
    save(fig,"so_do_3_phuong_phap.png")


def bo_tri_ldr():
    fig,axs=plt.subplots(1,2,figsize=(10.5,4.6),dpi=190); fig.patch.set_facecolor("white")
    for a in axs: a.set_facecolor("white");a.axis("off");a.set_aspect("equal")
    a=axs[0];a.set_xlim(0,100);a.set_ylim(0,76)
    a.add_patch(Rectangle((12,9),76,55,fc="white",ec=EDGE,lw=1.1));a.text(50,35,"tấm pin\n(nhìn thẳng)",ha="center",va="center",fontsize=8)
    pts=[(24,51,"ET"),(76,51,"WT"),(24,21,"EB"),(76,21,"WB")]
    for x,y,label in pts:
        a.add_patch(Ellipse((x,y),9,7,fc=BLUE,ec=EDGE,lw=0.9));a.text(x,y,label,ha="center",va="center",fontsize=7)
    a.text(50,70,"Vị trí cảm biến nhìn từ trước",ha="center",fontsize=8,fontweight="bold")
    a=axs[1];a.set_xlim(0,100);a.set_ylim(0,76)
    line(a,12,16,88,16,1.4);line(a,50,16,50,62,1.1)
    a.text(50,11,"mặt tấm pin",ha="center",fontsize=7.8);a.text(53,61,"pháp tuyến",fontsize=7.4)
    for x,label,sign in ((26,"ET / EB",-1),(74,"WT / WB",1)):
        a.add_patch(Ellipse((x,20),8,6,fc=BLUE,ec=EDGE,lw=0.9))
        arrow(a,x,22,x+sign*18,50)
        a.text(x+sign*18,54,label,ha="center",fontsize=7.2)
    a.text(50,69,"Mặt cắt; β_s=30° là giả thiết thiết kế",ha="center",fontsize=8,fontweight="bold")
    a.text(50,3,"Chưa chế tạo/hiệu chuẩn; xác nhận cách gá và hướng ET/WT/EB/WB trước thử nghiệm.",ha="center",fontsize=7)
    fig.tight_layout();save(fig,"bo_tri_4_ldr.png")


def luu_do_tong_quat(truc=1):
    two=truc==2
    fig,ax=canvas(8.2,14.3,(0,100),(0,142));title(ax,f"VÒNG LẶP HYBRID AN TOÀN – {'HAI' if two else 'MỘT'} TRỤC",139,9.4)
    box(ax,50,132,24,5,"Khởi động / khôi phục",BLUE,7.4,True)
    box(ax,50,122,48,7,"Khởi tạo GPIO, I²C, RTC, LCD, trạng thái motor",PALE,7.4)
    box(ax,50,111,48,7,"Đọc DS1307 và kiểm tra dữ liệu/ACK",PALE,7.4)
    decision(ax,50,100,34,9,"RTC hợp lệ?",7.5)
    box(ax,82,100,28,8,"Dừng cầu H; giữ góc;\nbáo lỗi",RED,7.1)
    box(ax,50,88,48,8,"LCD cập nhật theo bộ định thời 1 giây",BLUE,7.4)
    box(ax,50,77,50,8,"Tính giờ Mặt Trời và (α, γ) theo lịch 30 phút",PALE,7.2)
    decision(ax,50,65,38,10,"Mặt Trời trên ngưỡng cao độ?",7.2)
    box(ax,82,65,28,8,"Dừng và giữ góc hiện tại;\nreset latch ban đêm",RED,7.0)
    box(ax,50,51,50,8,"Kiểm tra S mỗi 1 s; chỉ hiệu chỉnh LDR mỗi 2 phút",PALE,7.0)
    decision(ax,50,39,38,10,"S ≥ S_min?",7.4)
    box(ax,82,39,28,8,"Mây / thiếu sáng:\ndừng, giữ vị trí",RED,7.0)
    box(ax,50,26,50,8,"Thiên văn 30 phút; LDR hiệu chỉnh 2 phút\n(beta/gamma có giới hạn)" if two else "Thiên văn 30 phút; LDR hiệu chỉnh 2 phút\n(góc azimuth có giới hạn)",GREEN,7.1)
    box(ax,50,14,50,8,"Trong khi chạy: poll E-stop, limit, hồi tiếp 10 ms;\ntối đa 8 s/lệnh; đảo chiều nghỉ 25 ms",BLUE,7.0)
    box(ax,50,4,25,5,"Lặp vòng",BLUE,7.3,True)
    arrow(ax,50,129.5,50,125.5);arrow(ax,50,118.5,50,114.5);arrow(ax,50,107.5,50,104.5)
    arrow(ax,67,100,68,100,"không",67,102);arrow(ax,50,95.5,50,92)
    arrow(ax,50,84,50,81);arrow(ax,50,73,50,70)
    arrow(ax,69,65,68,65,"không",68,67);arrow(ax,50,60,50,55)
    arrow(ax,69,39,68,39,"không",68,41);arrow(ax,50,34,50,30)
    arrow(ax,50,22,50,18);arrow(ax,50,10,50,6.5)
    line(ax,96,100,96,14);line(ax,96,14,75,14);arrow(ax,75,14,75,14)
    line(ax,96,65,96,14);line(ax,96,39,96,14)
    line(ax,38,4,9,4);line(ax,9,4,9,111);arrow(ax,9,111,26,111)
    save(fig,f"luu_do_tong_quat_{truc}_truc.png")


def luu_do_doc_adc():
    fig,ax=canvas(7.8,10.2,(0,90),(0,110));title(ax,"LỌC 4 KÊNH LDR – LẬP TRÌNH ĐỒ ÁN 1",107,9.1)
    ys=[98,87,76,64,50,36,23,10]
    texts=["Bắt đầu", "Mỗi kênh lấy 16 mẫu ADC", "Sắp xếp; bỏ 2 thấp + 2 cao;\nlấy trung bình 12 mẫu", "Nhân K_cal (placeholder 1,0;\nchưa hiệu chuẩn)", "Tính S, e1=(ET+EB)−(WT+WB),\ne2=(ET+WT)−(EB+WB)", "Nếu S < S_min: giữ vị trí,\nkhông phát lệnh LDR", "Áp hysteresis: bắt đầu |e|≥200;\ndừng |e|≤120 count", "Trả LdrResult cho module tích hợp"]
    for i,(y,t) in enumerate(zip(ys,texts)):
        box(ax,45,y,58 if i not in (0,7) else 37,7 if i not in (4,5,6) else 9,t,
            GREEN if i in (5,6) else (BLUE if i in (0,7) else PALE),7.3,i in (0,7),wrap=54)
        if i<len(ys)-1:arrow(ax,45,y-(3.5 if i not in (4,5,6) else 4.5),45,ys[i+1]+(3.5 if i+1 not in (4,5,6) else 4.5))
    ax.text(45,2,"Logic ADC chưa chạy trên bo; dải điện áp chân tối đa 3,3 V; ADC2 cần tắt Wi-Fi.",ha="center",fontsize=6.9)
    save(fig,"luu_do_doc_adc.png")


def luu_do_thien_van():
    fig,ax=canvas(7.8,11.5,(0,90),(0,120));title(ax,"RTC DÂN DỤNG → GIỜ MẶT TRỜI → GÓC ĐẶT",117,9.2)
    steps=[("Đọc 7 thanh ghi DS1307; kiểm tra ACK,\nCH, BCD, 24-hour và miền ngày/giờ",102),
           ("Lỗi RTC? dừng/giữ góc; không tạo lệnh",88),
           ("Đổi UTC+7 sang giờ Mặt Trời:\nkinh độ tham chiếu + Equation of Time",73),
           ("Tính alpha, gamma bằng cùng quy ước\nphi, delta, H; giữ nhánh atan2",58),
           ("alpha ≤ ngưỡng? dừng/giữ; không\nphát góc đích (0,0)",43),
           ("beta là cao độ pháp tuyến; beta_cmd=clamp(alpha,0°,75°);\ngamma giới hạn ±120°/latch",28),
           ("Trả target hợp lệ; không điều khiển motor\nnếu dữ liệu/thời sáng không hợp lệ",13)]
    for i,(t,y) in enumerate(steps):
        box(ax,45,y,58,9,t,RED if i in (1,4,6) else PALE,7.2,wrap=57)
        if i<len(steps)-1:arrow(ax,45,y-4.5,45,steps[i+1][1]+4.5)
    save(fig,"luu_do_thien_van.png")


def luu_do_dieu_khien_motor():
    fig,ax=canvas(8.1,10.7,(0,96),(0,112));title(ax,"GIÁM SÁT MOTOR / LIMIT / DỪNG KHẨN",109,9.2)
    entries=[("Trước lệnh: xác nhận RTC, ánh sáng,\nfeedback và interlock hợp lệ",97),
             ("GPIO23: NC kéo GND; LOW=bình thường;\nHIGH khi nhấn/đứt dây → dừng cả hai trục",83),
             ("Chọn một chiều cầu H; HIGH/HIGH=khóa;\nkhông bao giờ LOW/LOW",68),
             ("Break-before-make 25 ms; bắt đầu lệnh",53),
             ("Mỗi 10 ms kiểm tra E-stop, limit,\nfeedback và timeout tối đa 8 s",38),
             ("Có lỗi / chạm limit / hết thời gian?\ndừng motor, giữ feedback, báo lỗi",23),
             ("Hardware NC phải cắt enable/nguồn độc lập;\nGPIO23 phần mềm không thay thế mạch an toàn",8)]
    for i,(t,y) in enumerate(entries):
        box(ax,48,y,67,8,t,RED if i in (1,5,6) else PALE,7.1,wrap=65)
        if i<len(entries)-1:arrow(ax,48,y-4,48,entries[i+1][1]+4)
    save(fig,"luu_do_dieu_khien_motor.png")


def luu_do_lcd():
    fig,ax=canvas(7.5,9.0,(0,86),(0,94));title(ax,"LCD1602 – CHU KỲ RIÊNG 1 GIÂY",91,9.2)
    rows=[("Đọc giờ DS1307 và trạng thái an toàn",79),
          ("Đọc feedback/góc; lấy cờ: TRACK / HOLD / FAULT",65),
          ("Ghi LCD 1602: giờ, góc, trạng thái;\nkhông in giá trị giả khi RTC lỗi",50),
          ("Hẹn lần cập nhật kế tiếp sau 1 giây",35),
          ("Vòng LCD độc lập chu kỳ LDR 2 phút",20)]
    for i,(t,y) in enumerate(rows):
        box(ax,43,y,58,8,t,BLUE if i in (2,4) else PALE,7.2,wrap=56)
        if i<len(rows)-1:arrow(ax,43,y-4,43,rows[i+1][1]+4)
    line(ax,14,20,8,20);line(ax,8,20,8,79);arrow(ax,8,79,14,79)
    save(fig,"luu_do_lcd.png")


def main():
    so_do_khoi(1);so_do_khoi(2);so_do_ket_noi(1);so_do_ket_noi(2)
    so_do_3_phuong_phap();bo_tri_ldr()
    luu_do_tong_quat(1);luu_do_tong_quat(2)
    luu_do_doc_adc();luu_do_thien_van();luu_do_dieu_khien_motor();luu_do_lcd()


if __name__=="__main__":
    main()
