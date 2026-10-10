# -*- coding: utf-8 -*-
"""Viết lại phần "Tính mới." thành danh sách các điểm mới, đưa định nghĩa bộ bảy trường vào
bước Trích xuất có neo nguồn (thay tham chiếu "nêu ở mục 3" đã sai sau khi chia lại đề mục),
rồi đánh số lại trích dẫn theo thứ tự xuất hiện.

Chạy: python3 sua_tinh_moi.py <thư mục đã giải nén của bản sạch>   (sửa tại chỗ)
"""
import copy
import re
import sys
from pathlib import Path

from lxml import etree

DIR = Path(sys.argv[1])
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
GIOI_HAN = 1600

DIEM_MOI = [
    "Xét riêng loại tuyên bố thông số có điều kiện ràng buộc trong quảng cáo tiếng Việt do LLM tạo, loại "
    "tuyên bố mà các nghiên cứu đã khảo sát chưa xét riêng. Nhãn Lệch điều kiện được định nghĩa bằng quy "
    "tắc cụ thể (phần Phát biểu bài toán), để người gán nhãn và hệ thống dùng cùng một tiêu chí.",

    "Kết luận bằng phép đối chiếu điều kiện: P so điều kiện của tuyên bố (nêu rõ, hoặc theo cách hiểu "
    "thông thường) với từng điều kiện mà hãng công bố cho cùng thông số, rồi kết luận Lệch điều kiện khi "
    "con số của tuyên bố trùng với giá trị được công bố ở một điều kiện khác, hoặc khi mức “lên đến” bị "
    "viết thành mức chắc chắn đạt. Các cách hiện có để LLM tự đọc bằng chứng rồi phán đoán [3], hoặc phải "
    "tự đoán phần ngữ cảnh bị bỏ [4]. Điểm mới nằm ở bước kết luận này, không ở bước tách điều kiện (LLM "
    "trích, Python kiểm tra câu trích) vốn chỉ chuẩn bị đầu vào; đối chứng B1 nhận cùng bộ thông số đã "
    "trích, B2 dùng cùng bốn nhãn, nhưng cả hai đều để LLM gán nhãn (Bảng 2).",

    "Dùng sáu loại điều kiện của thông số (chế độ hoạt động, bộ phận, phụ kiện, điều kiện đo, phiên bản, "
    "kiểu giá trị) làm danh mục để so từng loại. Đây là cách cụ thể hóa cho thông số sản phẩm phần thông "
    "tin cần có để hiểu đúng một số đo trong lược đồ gán nhãn MeasEval [15].",
]
TRICH_CU = "điền bảy trường thông số nêu ở mục 3, mỗi trường kèm câu gốc làm căn cứ."
TRICH_MOI = ("điền bộ bảy trường thông số (sản phẩm và phiên bản, bộ phận, thuộc tính, giá trị, đơn vị, "
             "điều kiện ràng buộc, kiểu giá trị), mỗi trường kèm câu gốc làm căn cứ.")


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


def text_runs(p):
    return [r for r in p.findall(q("r")) if r.find(q("t")) is not None]


def set_text(p, text):
    runs = text_runs(p)
    runs[0].find(q("t")).text = text
    runs[0].find(q("t")).set(XML_SPACE, "preserve")
    for r in runs[1:]:
        p.remove(r)
    return p


i_nd, i_kh, i_tl = idx_row("Nội dung đề tài"), idx_row("Kế hoạch thực hiện"), idx_row("Tài liệu tham khảo")
nd_rows = rows[i_nd:i_kh]
nd = [e for tr in nd_rows for e in row_items(tr)]

# ------------------------------------------------------------ phần Tính mới
L = [k for k, e in enumerate(nd) if e.tag == q("p") and ptext(e) == "Tính mới."]
assert len(L) == 1
L = L[0]
assert ptext(nd[L + 1]).startswith("Đề tài không xây dựng lại một hệ thống kiểm chứng tổng quát.")
assert ptext(nd[L + 2]).startswith("Bước kết luận dựa trên đối chiếu điều kiện")
assert ptext(nd[L + 3]).startswith("Điểm mới này khác với hai phần dễ bị nhầm")
bullet = nd[L + 2]
moi = []
for k, text in enumerate(DIEM_MOI):
    b = bullet if k == 1 else copy.deepcopy(bullet)
    moi.append(set_text(b, text))
nd[L + 1:L + 4] = moi

# ------------------------------------------------------------ bước Trích xuất có neo nguồn
hits = [e for e in nd if e.tag == q("p") and ptext(e).startswith("Trích xuất có neo nguồn:")]
assert len(hits) == 1
for t in hits[0].iter(q("t")):
    if t.text and TRICH_CU in t.text:
        t.text = t.text.replace(TRICH_CU, TRICH_MOI)
        break
else:
    raise SystemExit("Không thấy câu cần sửa trong bước Trích xuất có neo nguồn")


# ------------------------------------------------------------ dựng lại các hàng của mục Nội dung
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


def set_border(tr, side, hidden):
    tcpr = tr.find(q("tc")).find(q("tcPr"))
    b = tcpr.find(q("tcBorders"))
    if b is None:
        if not hidden:
            return
        b = etree.Element(q("tcBorders"))
        idx = 0
        for i, ch in enumerate(tcpr):
            if etree.QName(ch).localname in ("cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge"):
                idx = i + 1
        tcpr.insert(idx, b)
    e = b.find(q(side))
    if not hidden:
        if e is not None:
            b.remove(e)
        if len(b) == 0:
            tcpr.remove(b)
        return
    order = ["top", "start", "left", "bottom", "end", "right", "insideH", "insideV", "tl2br", "tr2bl"]
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
        set_border(tr, "top", i > 0)
        set_border(tr, "bottom", i < len(made) - 1)


rebuild(nd_rows, nd)

# ------------------------------------------------------------ đánh số lại trích dẫn
rows = main.findall(q("tr"))
i_tl = idx_row("Tài liệu tham khảo")
tl_row = rows[i_tl]
all_p = list(body.iter(q("p")))
nhan_tl = [p for p in tl_row.iter(q("p")) if ptext(p).startswith("Tài liệu tham khảo")][0]
cut = all_p.index(nhan_tl)
body_p = all_p[:cut]
CIT = re.compile(r"\[(\d+)\]")
order = []
for p in body_p:
    for m in CIT.finditer(ptext(p)):
        n = int(m.group(1))
        if n not in order:
            order.append(n)
ref_rows = rows[i_tl + 1:-1]                 # các hàng tài liệu [2]..; hàng cuối là chữ ký
ref_p = {}
for tr in [tl_row] + ref_rows:
    for p in tr.iter(q("p")):
        m = re.match(r"^\[(\d+)\] ", ptext(p))
        if m:
            ref_p[int(m.group(1))] = (p, tr)
assert sorted(order) == sorted(ref_p) == list(range(1, len(ref_p) + 1)), (order, sorted(ref_p))
moi_so = {old: k + 1 for k, old in enumerate(order)}
print("Ánh xạ số cũ -> mới:", {k: v for k, v in moi_so.items() if k != v} or "không đổi")

if any(k != v for k, v in moi_so.items()):
    for p in body_p:
        for t in p.iter(q("t")):
            if t.text and CIT.search(t.text):
                t.text = CIT.sub(lambda m: "[%d]" % moi_so[int(m.group(1))], t.text)
    assert moi_so[1] == 1, "Tài liệu [1] phải nằm cùng hàng với nhãn"
    for old, (p, tr) in ref_p.items():
        t0 = text_runs(p)[0].find(q("t"))
        t0.text = re.sub(r"^\[\d+\] ", "[%d] " % moi_so[old], t0.text)
    for tr in ref_rows:
        main.remove(tr)
    anchor = tl_row
    for old in sorted((o for o in ref_p if o != 1), key=lambda o: moi_so[o]):
        tr = ref_p[old][1]
        anchor.addnext(tr)
        anchor = tr
    ref_rows = sorted(ref_rows, key=lambda tr: moi_so[[o for o, (p, r) in ref_p.items() if r is tr][0]])
    # Đường kẻ ẩn giữa các tài liệu, hiện ở cuối mục; tài liệu cuối đi cùng trang với khung chữ ký.
    for k, tr in enumerate(ref_rows):
        set_border(tr, "top", True)
        set_border(tr, "bottom", k < len(ref_rows) - 1)
        for p in tr.iter(q("p")):
            ppr = p.find(q("pPr"))
            kn = ppr.find(q("keepNext"))
            if k == len(ref_rows) - 1 and kn is None:
                kn = etree.Element(q("keepNext"))
                kn.set(q("val"), "1")
                ppr.insert(0, kn)
            elif k < len(ref_rows) - 1 and kn is not None:
                ppr.remove(kn)

tree.write(str(path), xml_declaration=True, encoding="UTF-8", standalone=True)
print("Đã viết lại phần Tính mới:", len(DIEM_MOI), "điểm mới")
