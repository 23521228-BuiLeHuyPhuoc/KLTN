# -*- coding: utf-8 -*-
"""Chia lại đề mục của đề cương (bản sạch, đã theo mẫu Khoa) cho đúng các mục mà mẫu yêu cầu.

Nội dung đề tài: 1. Tổng quan (bối cảnh, nghiên cứu liên quan, hạn chế, phát biểu bài toán,
tính mới, đóng góp, cải tiến), 2. Mục tiêu, 3. Phạm vi, 4. Đối tượng, 5. Phương pháp thực hiện,
6. Kết quả mong đợi.
Kế hoạch thực hiện: 1. Mô tả kế hoạch làm việc (kèm rủi ro và phương án dự phòng),
2. Thời gian biểu, 3. Phân công công việc.
Thêm mã lớp vào dòng sinh viên.

Chạy: python3 sua_de_muc.py <thư mục đã giải nén của bản sạch>   (sửa tại chỗ)
"""
import copy
import sys
from pathlib import Path

from lxml import etree

DIR = Path(sys.argv[1])
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
GIOI_HAN = 1600
MA_LOP = "MMTT2023.2"

MO_TA = (
    "Công việc chia thành bốn giai đoạn theo tháng: tháng 09/2026 khảo sát tài liệu, xây dựng hướng "
    "dẫn gán nhãn và chuẩn bị môi trường chạy; tháng 10/2026 làm thử trên 2 mẫu sản phẩm để chốt hướng "
    "dẫn nhãn, tệp cấu hình và quy mô dữ liệu; tháng 11/2026 hoàn thiện bộ dữ liệu, cài đặt P và các "
    "đối chứng, chọn cấu hình trên tập phát triển; tháng 12/2026 chạy tập kiểm tra cuối, tích hợp vào "
    "CopyPro và hoàn thiện khóa luận. Phần lõi bắt buộc được làm trước, phần mở rộng (B4, thử trên máy "
    "tính bảng) chỉ làm khi đúng tiến độ. Các mốc kiểm tra với cán bộ hướng dẫn được ghi trong thời "
    "gian biểu; rủi ro và phương án dự phòng nêu dưới đây."
)
PHAN_CONG = (
    "Sinh viên Bùi Lê Huy Phước thực hiện toàn bộ công việc trong thời gian biểu trên, gồm khảo sát tài "
    "liệu, xây dựng và gán nhãn dữ liệu, cài đặt phương pháp P và các đối chứng, chạy thực nghiệm, tích "
    "hợp vào CopyPro và viết khóa luận. Người gán nhãn thứ hai chỉ tham gia gán độc lập khoảng 60 tuyên "
    "bố để đo độ tin cậy của nhãn."
)


def q(tag):
    return "{%s}%s" % (W, tag)


def ptext(el):
    return "".join(t.text or "" for t in el.iter(q("t")))


path = DIR / "word" / "document.xml"
tree = etree.parse(str(path), etree.XMLParser(remove_blank_text=False, huge_tree=True))
body = tree.getroot().find(q("body"))
main = body.findall(q("tbl"))[1]
rows = main.findall(q("tr"))


def row_items(tr):
    return [c for c in tr.find(q("tc")) if c.tag in (q("p"), q("tbl"))]


def first_text(tr):
    for p in tr.iter(q("p")):
        if ptext(p).strip():
            return ptext(p)
    return ""


def idx_row(prefix):
    hits = [i for i, tr in enumerate(rows) if first_text(tr).startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return hits[0]


i_nd, i_kh, i_tl = idx_row("Nội dung đề tài"), idx_row("Kế hoạch thực hiện"), idx_row("Tài liệu tham khảo")
nd_rows, kh_rows = rows[i_nd:i_kh], rows[i_kh:i_tl]
nd = [e for tr in nd_rows for e in row_items(tr)]
kh = [e for tr in kh_rows for e in row_items(tr)]


def find(items, text, start=False):
    hits = [k for k, e in enumerate(items)
            if e.tag == q("p") and (ptext(e).startswith(text) if start else ptext(e) == text)]
    assert len(hits) == 1, (text, len(hits))
    return hits[0]


def text_runs(p):
    return [r for r in p.findall(q("r")) if r.find(q("t")) is not None]


def set_text(p, text):
    runs = text_runs(p)
    runs[0].find(q("t")).text = text
    runs[0].find(q("t")).set(XML_SPACE, "preserve")
    for r in runs[1:]:
        p.remove(r)
    return p


def add_italic(p):
    for r in text_runs(p):
        rpr = r.find(q("rPr"))
        if rpr.find(q("i")) is None:
            anchor = rpr.find(q("bCs"))
            for tag in ("iCs", "i"):
                e = etree.Element(q(tag))
                e.set(q("val"), "1")
                anchor.addnext(e)
    return p


def drop_before(p):
    sp = p.find(q("pPr")).find(q("spacing"))
    if sp is not None and sp.get(q("before")) is not None:
        del sp.attrib[q("before")]
    return p


def strip_label(p, label):
    """Bỏ run nhãn đứng đầu đoạn (ví dụ "Phạm vi:") và khoảng trắng đầu run kế tiếp."""
    runs = text_runs(p)
    assert runs[0].find(q("t")).text == label, ptext(p)[:40]
    p.remove(runs[0])
    t = runs[1].find(q("t"))
    t.text = t.text.lstrip()
    return drop_before(p)


# Mẫu định dạng: đề mục lớn ("1. Tổng quan"), chữ dẫn nghiêng đậm ("Bối cảnh."), đoạn thường.
H_MAU = nd[find(nd, "1. Tổng quan")]
LEAD_RUN = text_runs(nd[find(nd, "Bối cảnh.", start=True)])[0]
P_MAU = nd[find(nd, "Đề tài được xây dựng thành một tính năng", start=True)]


def heading(text):
    return set_text(copy.deepcopy(H_MAU), text)


def body_para(text):
    return set_text(copy.deepcopy(P_MAU), text)


# ------------------------------------------------------------ Nội dung đề tài
k = find(nd, "2. Phát biểu bài toán")
nd.pop(k)
lead = copy.deepcopy(LEAD_RUN)
lead.find(q("t")).text = "Phát biểu bài toán. "
nd[k].insert(list(nd[k]).index(text_runs(nd[k])[0]), lead)

k = find(nd, "3. Tính mới, đóng góp và cải tiến", start=True)
j = find(nd, "Tính mới.")
assert j > k
nhan = nd.pop(j)
nd[k] = nhan                                   # nhãn "Tính mới." thay chỗ đề mục số 3 cũ

set_text(nd[find(nd, "Mục tiêu:")], "2. Mục tiêu")
for so, nhan_cu in ((3, "Phạm vi:"), (4, "Đối tượng:")):
    k = find(nd, nhan_cu, start=True)
    strip_label(nd[k], nhan_cu)
    nd.insert(k, heading(f"{so}. {nhan_cu.rstrip(':')}"))
set_text(nd[find(nd, "Phương pháp thực hiện:")], "5. Phương pháp thực hiện")
for so in range(1, 5):
    add_italic(nd[find(nd, f"Nội dung {so}:", start=True)])
set_text(nd[find(nd, "Kết quả mong đợi:")], "6. Kết quả mong đợi")

# ------------------------------------------------------------ Kế hoạch thực hiện
k_nhom = find(kh, "Nhóm có 1 thành viên")
k_thang = find(kh, "Tháng 09/2026:")
k_rr = find(kh, "Rủi ro và phương án dự phòng:")
assert k_nhom < k_thang < k_rr
nhan_kh = kh[0]
nhom = drop_before(kh[k_nhom])
thang = kh[k_thang:k_rr]
rui_ro = [add_italic(kh[k_rr])] + kh[k_rr + 1:]
kh = ([nhan_kh, heading("1. Mô tả kế hoạch làm việc"), body_para(MO_TA)] + rui_ro
      + [heading("2. Thời gian biểu")] + thang
      + [heading("3. Phân công công việc"), nhom, body_para(PHAN_CONG)])

# ------------------------------------------------------------ dựng lại các hàng của hai mục
def is_bold(r):
    rpr = r.find(q("rPr"))
    b = rpr.find(q("b")) if rpr is not None else None
    return b is not None and b.get(q("val"), "1") not in ("0", "false")


def is_head(e):
    if e.tag != q("p"):
        return False
    if e.find(".//" + q("drawing")) is not None:
        return True
    t = ptext(e).strip()
    if not t or len(t) > 90:
        return False
    runs = [r for r in text_runs(e) if (r.find(q("t")).text or "").strip()]
    return (bool(runs) and all(is_bold(r) for r in runs)) or t.startswith("Bảng ") or t.endswith(":")


def chunks_of(items):
    out, heads = [], []
    for e in items:
        if is_head(e):
            heads.append(e)
            continue
        if heads:
            out.append(heads + [e])
            heads = []
        elif e.tag == q("p") and not ptext(e).strip() and e.find(".//" + q("drawing")) is None and out:
            out[-1].append(e)
        else:
            out.append([e])
    if heads:
        out.append(heads)
    return out


def size(chunk):
    return sum(len(ptext(e)) for e in chunk)


def set_cant_split(tr, on):
    trpr = tr.find(q("trPr"))
    cs = trpr.find(q("cantSplit"))
    if cs is None:
        cs = etree.Element(q("cantSplit"))
        trpr.insert(0, cs)
    cs.set(q("val"), "1" if on else "0")


def hide_border(tr, side):
    tcpr = tr.find(q("tc")).find(q("tcPr"))
    b = tcpr.find(q("tcBorders"))
    if b is None:
        b = etree.Element(q("tcBorders"))
        idx = 0
        for i, ch in enumerate(tcpr):
            if etree.QName(ch).localname in ("cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge"):
                idx = i + 1
        tcpr.insert(idx, b)
    order = ["top", "start", "left", "bottom", "end", "right", "insideH", "insideV", "tl2br", "tr2bl"]
    e = b.find(q(side))
    if e is None:
        e = etree.Element(q(side))
        pos = len(b)
        for i, ch in enumerate(b):
            if order.index(etree.QName(ch).localname) > order.index(side):
                pos = i
                break
        b.insert(pos, e)
    e.set(q("val"), "nil")


def rebuild(group_rows, items):
    tr0 = group_rows[0]
    for tr in group_rows[1:]:
        main.remove(tr)
    tc0 = tr0.find(q("tc"))
    for c in [c for c in tc0 if c.tag in (q("p"), q("tbl"))]:
        tc0.remove(c)
    tcpr = tc0.find(q("tcPr"))
    if tcpr.find(q("tcBorders")) is not None:
        tcpr.remove(tcpr.find(q("tcBorders")))
    sach_tcpr = copy.deepcopy(tcpr)
    chunks = chunks_of(items[1:])
    chunks[0] = [items[0]] + chunks[0]
    made = [tr0]
    for e in chunks[0]:
        tc0.append(e)
    set_cant_split(tr0, size(chunks[0]) <= GIOI_HAN)
    for ch in chunks[1:]:
        tr = etree.Element(q("tr"))
        tr.append(copy.deepcopy(tr0.find(q("trPr"))))
        tc = etree.SubElement(tr, q("tc"))
        tc.append(copy.deepcopy(sach_tcpr))
        for e in ch:
            tc.append(e)
        set_cant_split(tr, (len(ch) > 1 or is_head(ch[0])) and size(ch) <= GIOI_HAN)
        made[-1].addnext(tr)
        made.append(tr)
    for i, tr in enumerate(made):
        if i > 0:
            hide_border(tr, "top")
        if i < len(made) - 1:
            hide_border(tr, "bottom")


rebuild(nd_rows, nd)
rebuild(kh_rows, kh)

# ------------------------------------------------------------ mã lớp
sv = [p for p in rows[idx_row("Sinh viên thực hiện")].iter(q("p")) if "23521228" in ptext(p)]
assert len(sv) == 1
for t in sv[0].iter(q("t")):
    if t.text and "23521228 - 0373025859" in t.text:
        t.text = t.text.replace("23521228 - 0373025859", f"23521228 - {MA_LOP} - 0373025859")
        break
else:
    raise SystemExit("Không thấy dòng sinh viên để thêm mã lớp")

tree.write(str(path), xml_declaration=True, encoding="UTF-8", standalone=True)
print("Đã chia lại đề mục:", len(nd), "phần tử nội dung,", len(kh), "phần tử kế hoạch")
