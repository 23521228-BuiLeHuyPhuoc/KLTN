# -*- coding: utf-8 -*-
"""Dựng đề cương (.docx) từ khung đề cương cũ.

Chạy:  python3 dung_docx.py          -> bản chữ đỏ (phần thêm mới hoặc sửa tô đỏ, có dòng ghi chú)
       python3 dung_docx.py --sach  -> bản sạch để nộp (toàn bộ chữ đen, bỏ dòng ghi chú)
"""
import copy
import re
import sys
from pathlib import Path

import docx
from docx.oxml import OxmlElement
from docx.shared import Cm
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from lxml import etree

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
SACH = "--sach" in sys.argv
from noi_dung import (GHI_CHU, OLD_NUM, REFS, SEC_KE_HOACH, SEC_NOI_DUNG,  # noqa: E402
                      TITLE_EN, TITLE_VI, K, N)

BASE = str(HERE / "khung_de_cuong.docx")
OUT = str(HERE.parent / ("23521228_BuiLeHuyPhuoc_DeCuongKLTN.docx" if SACH else "23521228_BuiLeHuyPhuoc_DeCuongKLTN_chu_do.docx"))
RED = "FF0000"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
REF_RE = re.compile(r"\{ref:(\w+)\}")


def q(tag):
    return "{%s}%s" % (W, tag)


doc = docx.Document(BASE)
tbl = doc.tables[1]
trs = [r._tr for r in tbl.rows]
assert len(trs) == 98, len(trs)


def ppr_of(i, j):
    p = trs[i].findall(".//" + q("p"))[j]
    return copy.deepcopy(p.find(q("pPr")))


PPR = {
    "text": ppr_of(4, 0),
    "label": ppr_of(5, 0),
    "dash": ppr_of(5, 1),
    "plus": ppr_of(57, 2),
    "month": ppr_of(57, 1),
    "label_keep": ppr_of(57, 0),
    "ref_label": ppr_of(91, 0),
    "ref": ppr_of(91, 1),
}
PPR["sub"] = copy.deepcopy(PPR["label"])
lt = copy.deepcopy(PPR["label"])
lt.remove(lt.find(q("keepNext")))
PPR["label_text"] = lt
cap = copy.deepcopy(PPR["text"])
cap.find(q("jc")).set(q("val"), "center")
ind = cap.find(q("ind"))
if ind is not None:
    cap.remove(ind)
PPR["caption"] = cap
img = copy.deepcopy(cap)
kn = etree.Element(q("keepNext"))
img.insert(0, kn)
PPR["image"] = img
# Tên bảng đặt phía trên bảng, cùng hàng (không ngắt) với bảng.
PPR["table_caption"] = copy.deepcopy(cap)
# Mọi gạch đầu dòng "-" dùng chung numId 7, mọi dấu "+" dùng chung numId 8 (như khung cũ).
PPR["dash"].find(q("numPr")).find(q("numId")).set(q("val"), "7")
PPR["plus"].find(q("numPr")).find(q("numId")).set(q("val"), "8")

def table_cells(spec):
    """Các ô của bảng (dòng tiêu đề trước), mỗi ô là danh sách run."""
    yield from spec["header"]
    for r in spec["rows"]:
        yield from r


def runs_of(kind, payload):
    """Mọi run của một phần tử theo đúng thứ tự xuất hiện trong văn bản."""
    if kind == "image":
        return []
    if kind == "table":
        return [run for cell in table_cells(payload) for run in cell]
    return payload


# ---------------- Đánh số trích dẫn theo thứ tự xuất hiện ----------------
order = []
for section in (SEC_NOI_DUNG, SEC_KE_HOACH):
    for row in section:
        for kind, payload in row:
            for run in runs_of(kind, payload):
                for m in REF_RE.finditer(run[1]):
                    if m.group(1) not in order:
                        order.append(m.group(1))
NUM = {k: i + 1 for i, k in enumerate(order)}
missing = [k for k in order if k not in REFS]
unused = [k for k in REFS if k not in NUM]
assert not missing, missing
assert not unused, unused


def expand(run):
    flag, text, b, i = run
    red = flag == "N"
    out, pos = [], 0
    for m in REF_RE.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], b, i, red))
        key = m.group(1)
        n = NUM[key]
        out.append((f"[{n}]", b, i, red or OLD_NUM.get(key) != n))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], b, i, red))
    return out


def make_run(text, bold=False, italic=False, red=False, size=26):
    r = etree.Element(q("r"))
    rpr = etree.SubElement(r, q("rPr"))
    f = etree.SubElement(rpr, q("rFonts"))
    for a in ("ascii", "cs", "eastAsia", "hAnsi"):
        f.set(q(a), "Times New Roman")
    if bold:
        etree.SubElement(rpr, q("b"))
        etree.SubElement(rpr, q("bCs"))
    if italic:
        etree.SubElement(rpr, q("i"))
        etree.SubElement(rpr, q("iCs"))
    if red and not SACH:
        etree.SubElement(rpr, q("color")).set(q("val"), RED)
    etree.SubElement(rpr, q("sz")).set(q("val"), str(size))
    etree.SubElement(rpr, q("szCs")).set(q("val"), str(size))
    t = etree.SubElement(r, q("t"))
    t.text = text
    t.set(XML_SPACE, "preserve")
    return r


def make_par(kind, runs):
    p = etree.Element(q("p"))
    p.append(copy.deepcopy(PPR[kind]))
    for run in runs:
        for t, b, i, red in expand(run):
            p.append(make_run(t, b, i, red))
    return p


TABLE_SIZE = 22  # cỡ chữ trong bảng: 11 pt


def _sub(parent, tag, **attrs):
    e = etree.SubElement(parent, q(tag))
    for k, v in attrs.items():
        e.set(q(k), str(v))
    return e


def cell_par(runs, header=False):
    p = etree.Element(q("p"))
    ppr = _sub(p, "pPr")
    _sub(ppr, "spacing", before=20, after=20, line=252, lineRule="auto")
    _sub(ppr, "jc", val="center" if header else "left")
    for run in runs:
        for t, b, i, red in expand(run):
            p.append(make_run(t, b or header, i, red, size=TABLE_SIZE))
    return p


def make_table(spec):
    """Bảng lồng trong một hàng của khung đề cương: viền đơn, cột cố định, lặp dòng tiêu đề khi sang trang."""
    widths = spec["widths"]
    tbl = etree.Element(q("tbl"))
    pr = _sub(tbl, "tblPr")
    _sub(pr, "tblW", w=sum(widths), type="dxa")
    _sub(pr, "jc", val="center")
    borders = _sub(pr, "tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        _sub(borders, side, val="single", sz=4, space=0, color="000000")
    _sub(pr, "tblLayout", type="fixed")
    mar = _sub(pr, "tblCellMar")
    for side, w in (("top", 20), ("left", 80), ("bottom", 20), ("right", 80)):
        _sub(mar, side, w=w, type="dxa")
    grid = _sub(tbl, "tblGrid")
    for w in widths:
        _sub(grid, "gridCol", w=w)

    def add_row(cells, header=False):
        assert len(cells) == len(widths), cells
        tr = _sub(tbl, "tr")
        trpr = _sub(tr, "trPr")
        _sub(trpr, "cantSplit")
        if header:
            _sub(trpr, "tblHeader")
        for w, runs in zip(widths, cells):
            tc = _sub(tr, "tc")
            tcpr = _sub(tc, "tcPr")
            _sub(tcpr, "tcW", w=w, type="dxa")
            if header:
                _sub(tcpr, "vAlign", val="center")
            tc.append(cell_par(runs, header))

    add_row(spec["header"], header=True)
    for r in spec["rows"]:
        add_row(r)
    return tbl


def spacer():
    """Đoạn trống nhỏ sau bảng (ô của Word phải kết thúc bằng một đoạn)."""
    p = etree.Element(q("p"))
    ppr = _sub(p, "pPr")
    _sub(ppr, "spacing", before=0, after=40, line=240, lineRule="auto")
    rpr = _sub(ppr, "rPr")
    _sub(rpr, "sz", val=12)
    _sub(rpr, "szCs", val=12)
    return p


def set_runs(p, runs):
    """Thay toàn bộ run của một đoạn có sẵn, giữ nguyên pPr."""
    for r in p.findall(q("r")):
        p.remove(r)
    for run in runs:
        for t, b, i, red in expand(run):
            p.append(make_run(t, b, i, red))


ROW_TEMPLATE = copy.deepcopy(trs[5])


def make_row(top, bottom, can_split):
    tr = copy.deepcopy(ROW_TEMPLATE)
    tc = tr.find(q("tc"))
    for p in tc.findall(q("p")):
        tc.remove(p)
    tr.find(q("trPr")).find(q("cantSplit")).set(q("val"), "0" if can_split else "1")
    tcpr = tc.find(q("tcPr"))
    borders = tcpr.find(q("tcBorders"))
    for side, on in (("top", top), ("bottom", bottom)):
        e = borders.find(q(side))
        e.set(q("val"), "single" if on else "nil")
        e.set(q("sz"), "4" if on else "0")
    mar = tcpr.find(q("tcMar"))
    mar.find(q("top")).set(q("w"), "55.0" if top else "0.0")
    mar.find(q("bottom")).set(q("w"), "55.0" if bottom else "0.0")
    return tr


sig_tr = trs[97]
pending_images = []
# Quy tắc ngắt trang của các hàng trong khung đề cương:
# - Không dùng "giữ với đoạn sau" (keepNext) trong ô: thuộc tính này xích các hàng vào nhau và để lại
#   khoảng trắng lớn cuối trang. Vì vậy tiêu đề luôn nằm cùng hàng với đoạn đầu tiên của mục.
# - Hàng dài được phép ngắt trang; hàng mở đầu bằng tiêu đề có ngưỡng cao hơn để tiêu đề không nằm trơ
#   ở cuối trang.
# - Hàng chứa hình hoặc bảng không bao giờ ngắt, để tên bảng, bảng, hình và tên hình đi cùng nhau
#   (LibreOffice cũng không ngắt bảng lồng trong ô qua hai trang).
HEADINGS = {"sub", "label", "label_keep", "month", "ref_label"}
SPLIT_AT = 700          # hàng dài hơn mức này được phép ngắt trang
SPLIT_AT_HEADING = 1100  # mức tương ứng cho hàng mở đầu bằng tiêu đề


def add_section(rows):
    n = len(rows)
    for idx, row in enumerate(rows):
        size = sum(len(r[1]) for kind, payload in row for r in runs_of(kind, payload))
        limit = SPLIT_AT_HEADING if row[0][0] in HEADINGS else SPLIT_AT
        has_float = any(kind in ("image", "table") for kind, _ in row)
        can_split = size > limit and not has_float
        tr = make_row(top=(idx == 0), bottom=(idx == n - 1), can_split=can_split)
        tc = tr.find(q("tc"))
        for kind, payload in row:
            if kind == "image":
                p = OxmlElement("w:p")
                p.append(copy.deepcopy(PPR["image"]))
                tc.append(p)
                pending_images.append((p, tc, payload))
            elif kind == "table":
                tc.append(make_table(payload))
                tc.append(spacer())
            else:
                tc.append(make_par(kind, payload))
        # Hàng được phép ngắt trang thì bỏ cả "giữ các dòng cùng nhau".
        tags = ("keepNext", "keepLines") if can_split else ("keepNext",)
        for ppr in tc.iter(q("pPr")):
            for tag in tags:
                e = ppr.find(q(tag))
                if e is not None:
                    ppr.remove(e)
        sig_tr.addprevious(tr)


# ---------------- Ghi chú đầu trang ----------------
note = [p for p in doc.paragraphs if p.text.startswith("Bản rà soát")]
assert len(note) == 1
if SACH:
    note[0]._p.getparent().remove(note[0]._p)
else:
    set_runs(note[0]._p, [N(GHI_CHU, i=True)])

# ---------------- Tên đề tài ----------------
title_ps = trs[0].findall(q("tc") + "/" + q("p"))
set_runs(title_ps[1], [K("Tiếng Việt: ", b=True), N(TITLE_VI, b=True)])
set_runs(title_ps[2], [K("Tiếng Anh: ", b=True), N(TITLE_EN, b=True)])

# ---------------- Xóa nội dung cũ (hàng 4..96), dựng nội dung mới ----------------
for tr in trs[4:97]:
    tbl._tbl.remove(tr)

add_section(SEC_NOI_DUNG)

ref_rows = []
for idx, key in enumerate(order):
    n = NUM[key]
    old = key in OLD_NUM
    runs = [N(f"[{n}] ") if (not old or OLD_NUM[key] != n) else K(f"[{n}] ")]
    for text, italic in REFS[key]:
        runs.append(K(text, i=italic) if old else N(text, i=italic))
    par = ("ref", runs)
    if idx == 0:
        ref_rows.append([("ref_label", [K("Tài liệu tham khảo", b=True)]), par])
    else:
        ref_rows.append([par])
add_section(SEC_KE_HOACH + ref_rows)

# ---------------- Hình ----------------
for p, tc, path in pending_images:
    para = Paragraph(p, _Cell(tc, tbl))
    para.add_run().add_picture(path, width=Cm(15.0))

# ---------------- Ngày ký ----------------
sig_ps = sig_tr.findall(q("tc"))[1].findall(q("p"))
set_runs(sig_ps[0], [K("TP. HCM, ngày ", b=True), N("…..", b=True), K(" tháng ", b=True),
                     N("10", b=True), K(" năm 2026", b=True)])

# ---------------- Làm sạch thuộc tính số thực do khung cũ xuất từ Google Docs ----------------
FLOAT_RE = re.compile(r"^-?\d+\.\d+$")
for el in doc.element.iter():
    if not isinstance(el.tag, str):
        continue
    for name, val in list(el.attrib.items()):
        if name.startswith("{%s}" % W) and FLOAT_RE.match(val):
            el.set(name, str(int(round(float(val)))))
for pgmar in doc.element.iter(q("pgMar")):
    if pgmar.get(q("gutter")) is None:
        pgmar.set(q("gutter"), "0")

doc.save(OUT)
print("Đã lưu", OUT)
print("Số tài liệu tham khảo:", len(order))
for k in order:
    print(f"  [{NUM[k]}] {k}" + (f" (cũ [{OLD_NUM[k]}])" if k in OLD_NUM else ""))
