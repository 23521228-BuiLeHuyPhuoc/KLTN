# -*- coding: utf-8 -*-
"""Đưa nội dung đề cương vào đúng file mẫu "mau_DeCuongChiTiet_Khoa-MMT_2025.docx".

Khung (đầu trang, tiêu đề, học kỳ, nhãn từng mục, bảng, khổ giấy, chữ ký) lấy nguyên từ mẫu;
nội dung (đoạn văn, bảng lồng, hình, tài liệu tham khảo) chép nguyên từ bản đề cương nguồn,
giữ định dạng và màu chữ của nguồn. Chạy hai lần: nguồn là bản sạch -> bản sạch; nguồn là
bản chữ đỏ -> bản chữ đỏ (thêm --do để tô đỏ phần điền vào dòng học kỳ).

Chạy: python3 dung_theo_mau.py <mẫu đã giải nén> <nguồn đã giải nén> <hình 1> <thư mục ra> [--do]
"""
import copy
import re
import shutil
import sys
from pathlib import Path

from lxml import etree

MAU, SRC, HINH, OUT = (Path(a) for a in sys.argv[1:5])
DO = "--do" in sys.argv[5:]

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
RED = "FF0000"
HOC_KY = ("HỌC KỲ ", "I", " NĂM HỌC ", "2026-2027")   # đoạn chữ của mẫu xen với phần điền


def q(tag, ns=W):
    return "{%s}%s" % (ns, tag)


def ptext(el):
    return "".join(t.text or "" for t in el.iter(q("t")))


def parse(path):
    return etree.parse(str(path), etree.XMLParser(remove_blank_text=False, huge_tree=True))


if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(MAU, OUT)

# ------------------------------------------------------------------ mở hai tài liệu
tdoc = parse(OUT / "word" / "document.xml")
old_root = tdoc.getroot()
nsmap = dict(old_root.nsmap)
nsmap.setdefault("a", A)
nsmap.setdefault("pic", PIC)
root = etree.Element(old_root.tag, nsmap=nsmap)       # thêm khai báo a:, pic: ở gốc cho hình
for k, v in old_root.attrib.items():
    root.set(k, v)
for ch in list(old_root):
    root.append(ch)
tdoc._setroot(root)
tbody = root.find(q("body"))

sdoc = parse(SRC / "word" / "document.xml")
sbody = sdoc.getroot().find(q("body"))

# ------------------------------------------------------------------ đọc nguồn theo mục
s_tables = [t for t in sbody.findall(q("tbl"))]
s_main = s_tables[1]                                   # bảng 0 là đầu trang
s_rows = s_main.findall(q("tr"))


def row_children(tr):
    out = []
    for tc in tr.findall(q("tc")):
        out += [c for c in tc if c.tag in (q("p"), q("tbl"))]
    return out


def first_text(tr):
    ps = [p for p in tr.iter(q("p")) if ptext(p).strip()]
    return ptext(ps[0]) if ps else ""


def find_row(prefix, start=0):
    for i in range(start, len(s_rows)):
        if first_text(s_rows[i]).startswith(prefix):
            return i
    raise SystemExit(f"Không thấy hàng bắt đầu bằng: {prefix}")


i_ten = find_row("TÊN ĐỀ TÀI")
i_cb = find_row("Cán bộ hướng dẫn")
i_tg = find_row("Thời gian thực hiện")
i_sv = find_row("Sinh viên thực hiện")
i_nd = find_row("Nội dung đề tài")
i_kh = find_row("Kế hoạch thực hiện")
i_tl = find_row("Tài liệu tham khảo")
i_ky = find_row("Xác nhận của CBHD")
assert i_ten < i_cb < i_tg < i_sv < i_nd < i_kh < i_tl < i_ky == len(s_rows) - 1


def runs_after_prefix(p, prefix):
    """Bản sao các run chữ của đoạn p, đã cắt bỏ tiền tố (và khoảng trắng đầu) khỏi chữ."""
    runs = [copy.deepcopy(r) for r in p.findall(q("r")) if r.find(q("t")) is not None]
    full = "".join(r.find(q("t")).text or "" for r in runs)
    assert full.startswith(prefix), (full[:60], prefix)
    cut = len(prefix)
    while cut < len(full) and full[cut] == " ":
        cut += 1
    out, pos = [], 0
    for r in runs:
        t = r.find(q("t"))
        s = t.text or ""
        a, b = pos, pos + len(s)
        pos = b
        if b <= cut:
            continue
        if a < cut:
            t.text = s[cut - a:]
        t.set(XML_SPACE, "preserve")
        out.append(r)
    return out


def no_bold(runs):
    for r in runs:
        rpr = r.find(q("rPr"))
        if rpr is None:
            continue
        for tag in ("b", "bCs"):
            e = rpr.find(q(tag))
            if e is not None:
                rpr.remove(e)
    return runs


def para_with(prefix, rows):
    for tr in rows:
        for p in tr.iter(q("p")):
            if ptext(p).startswith(prefix):
                return p
    raise SystemExit(f"Không thấy đoạn: {prefix}")


ten_vi = runs_after_prefix(para_with("Tiếng Việt:", [s_rows[i_ten]]), "Tiếng Việt:")
ten_en = runs_after_prefix(para_with("Tiếng Anh:", [s_rows[i_ten]]), "Tiếng Anh:")
cbhd = no_bold(runs_after_prefix(para_with("Cán bộ hướng dẫn:", [s_rows[i_cb]]), "Cán bộ hướng dẫn:"))
tg = runs_after_prefix(para_with("Thời gian thực hiện:", [s_rows[i_tg]]), "Thời gian thực hiện:")
sv_p = [p for p in s_rows[i_sv].iter(q("p")) if ptext(p).strip() and not ptext(p).startswith("Sinh viên thực hiện")]
assert len(sv_p) == 1
sv = no_bold(runs_after_prefix(sv_p[0], ""))


def section(i0, i1, label, skip_first=False):
    """Các phần tử của mục (từ hàng i0 đến trước i1); bỏ nhãn ở đoạn đầu, bỏ hàng chỉ có đoạn rỗng."""
    goc = []
    for tr in s_rows[i0:i1]:
        kids = row_children(tr)
        if all(k.tag == q("p") and not ptext(k).strip() and k.find(".//" + q("drawing")) is None for k in kids):
            continue
        goc += kids
    assert ptext(goc[0]).startswith(label), ptext(goc[0])[:60]
    out = [copy.deepcopy(e) for e in goc]
    if skip_first:
        return out[1:]
    p = out[0]
    rest = runs_after_prefix(p, label)
    for r in p.findall(q("r")):
        p.remove(r)
    for r in rest:
        p.append(r)
    return out


noi_dung = section(i_nd, i_kh, "Nội dung đề tài:")
ke_hoach = section(i_kh, i_tl, "Kế hoạch thực hiện:")
tai_lieu = section(i_tl, i_ky, "Tài liệu tham khảo", skip_first=True)
assert all(re.match(r"^\[\d+\] ", ptext(p)) for p in tai_lieu), "TLTK lẫn đoạn khác"

ky_cells = s_rows[i_ky].findall(q("tc"))
ky_right = [p for p in ky_cells[1].iter(q("p")) if ptext(p).strip()]
ky_ngay, ky_sv, ky_chu_ky, ky_ten = (copy.deepcopy(p) for p in ky_right)
assert ptext(ky_ngay).startswith("TP. HCM") and ptext(ky_sv) == "Sinh viên"

# ------------------------------------------------------------------ đánh số: gộp định nghĩa nguồn vào mẫu
OFF = 100
tnum = parse(OUT / "word" / "numbering.xml")
snum = parse(SRC / "word" / "numbering.xml")
troot = tnum.getroot()
t_abs = troot.findall(q("abstractNum"))
t_nums = troot.findall(q("num"))
anchor_abs = t_abs[-1]
for a in snum.getroot().findall(q("abstractNum")):
    a = copy.deepcopy(a)
    a.set(q("abstractNumId"), str(int(a.get(q("abstractNumId"))) + OFF))
    anchor_abs.addnext(a)
    anchor_abs = a
anchor_num = t_nums[-1]
for n in snum.getroot().findall(q("num")):
    n = copy.deepcopy(n)
    n.set(q("numId"), str(int(n.get(q("numId"))) + OFF))
    n.find(q("abstractNumId")).set(q("val"), str(int(n.find(q("abstractNumId")).get(q("val"))) + OFF))
    anchor_num.addnext(n)
    anchor_num = n
tnum.write(str(OUT / "word" / "numbering.xml"), xml_declaration=True, encoding="UTF-8", standalone=True)

# ------------------------------------------------------------------ hình 1
rels = parse(OUT / "word" / "_rels" / "document.xml.rels")
RID = "rIdHinh1"
rel = etree.SubElement(rels.getroot(), "{%s}Relationship" % PR)
rel.set("Id", RID)
rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image")
rel.set("Target", "media/image1.png")
rels.write(str(OUT / "word" / "_rels" / "document.xml.rels"), xml_declaration=True, encoding="UTF-8", standalone=True)
(OUT / "word" / "media").mkdir(exist_ok=True)
shutil.copyfile(HINH, OUT / "word" / "media" / "image1.png")
ctp = parse(OUT / "[Content_Types].xml")
if not any(d.get("Extension") == "png" for d in ctp.getroot().findall("{%s}Default" % CT)):
    d = etree.Element("{%s}Default" % CT)
    d.set("Extension", "png")
    d.set("ContentType", "image/png")
    ctp.getroot().insert(0, d)
ctp.write(str(OUT / "[Content_Types].xml"), xml_declaration=True, encoding="UTF-8", standalone=True)


# ------------------------------------------------------------------ làm sạch phần chép sang
def prepare(el):
    for e in el.iter():
        for a in list(e.attrib):
            if a in (q("paraId", W14), q("textId", W14)) or a.startswith("{%s}rsid" % W):
                del e.attrib[a]
            elif a.startswith("{%s}" % W) and re.fullmatch(r"-?\d+\.\d+", e.get(a)):
                # Google Docs ghi số đo dạng 278.00000000000006; lược đồ OOXML chỉ nhận số nguyên.
                e.set(a, str(int(round(float(e.get(a))))))
    for n in el.iter(q("numId")):
        n.set(q("val"), str(int(n.get(q("val"))) + OFF))
    for ts in el.iter(q("tblStyle")):
        ts.getparent().remove(ts)
    for ps in el.iter(q("pStyle")):
        raise SystemExit("Nội dung có pStyle chưa xử lý: " + ps.get(q("val")))
    for b in el.iter(q("blip", A)):
        b.set(q("embed", R), RID)
    # Kiểu Normal của nguồn canh trái, của mẫu canh đều: đoạn không ghi canh lề thì ghi rõ canh trái
    # để giữ đúng cách trình bày của nguồn (ví dụ tài liệu tham khảo có đường dẫn dài).
    for p in ([el] if el.tag == q("p") else []) + list(el.iter(q("p")))[(1 if el.tag == q("p") else 0):]:
        ppr = p.find(q("pPr"))
        if ppr is None:
            ppr = etree.Element(q("pPr"))
            p.insert(0, ppr)
        if ppr.find(q("jc")) is None:
            jc = etree.Element(q("jc"))
            jc.set(q("val"), "left")
            pos = len(ppr)
            for i, ch in enumerate(ppr):
                if etree.QName(ch).localname in ("textDirection", "textAlignment", "textboxTightWrap",
                                                 "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr",
                                                 "pPrChange"):
                    pos = i
                    break
            ppr.insert(pos, jc)
    return el


# ------------------------------------------------------------------ điền vào khung mẫu
t_tables = tbody.findall(q("tbl"))
t_main = t_tables[1]
t_rows = t_main.findall(q("tr"))
assert len(t_rows) == 8


def label_para(tr):
    return tr.find(q("tc")).find(q("p"))


def append_runs(p, runs, space=True):
    if space:
        sp = etree.SubElement(p, q("r"))
        rpr = copy.deepcopy(runs[0].find(q("rPr"))) if runs[0].find(q("rPr")) is not None else None
        if rpr is not None:
            sp.append(rpr)
        t = etree.SubElement(sp, q("t"))
        t.text = " "
        t.set(XML_SPACE, "preserve")
    for r in runs:
        p.append(prepare(r))


def make_run(text, red=False, bold=True, sz="30"):
    r = etree.Element(q("r"))
    rpr = etree.SubElement(r, q("rPr"))
    if bold:
        etree.SubElement(rpr, q("b"))
        etree.SubElement(rpr, q("bCs"))
    if red:
        c = etree.SubElement(rpr, q("color"))
        c.set(q("val"), RED)
    s = etree.SubElement(rpr, q("sz"))
    s.set(q("val"), sz)
    s2 = etree.SubElement(rpr, q("szCs"))
    s2.set(q("val"), sz)
    t = etree.SubElement(r, q("t"))
    t.text = text
    t.set(XML_SPACE, "preserve")
    return r


# Dòng học kỳ
p_hk = [p for p in tbody.findall(q("p")) if ptext(p).startswith("HỌC KỲ")]
assert len(p_hk) == 1
for r in p_hk[0].findall(q("r")):
    p_hk[0].remove(r)
for k, s in enumerate(HOC_KY):
    p_hk[0].append(make_run(s, red=DO and k % 2 == 1))

# Hàng 0: tên đề tài
ps0 = t_rows[0].find(q("tc")).findall(q("p"))
assert ptext(ps0[1]).startswith("Tên tiếng Việt") and ptext(ps0[2]).startswith("Tên tiếng Anh")
append_runs(ps0[1], ten_vi)
append_runs(ps0[2], ten_en)

# Hàng 1: cán bộ hướng dẫn
append_runs(label_para(t_rows[1]), cbhd)

# Hàng 2: thời gian
p_tg = label_para(t_rows[2])
for r in p_tg.findall(q("r")):
    if (ptext(r) or "").startswith("Từ ngày"):
        p_tg.remove(r)
for r in tg:
    p_tg.append(prepare(r))

# Hàng 3: sinh viên (một sinh viên)
ps3 = t_rows[3].find(q("tc")).findall(q("p"))
assert ptext(ps3[1]).startswith("<Họ tên sinh viên 1") and ptext(ps3[2]).startswith("<Họ tên sinh viên 2")
for r in ps3[1].findall(q("r")):
    ps3[1].remove(r)
for r in sv:
    ps3[1].append(prepare(r))
ps3[2].getparent().remove(ps3[2])

# Hàng 4, 5, 6: nội dung, kế hoạch, tài liệu tham khảo.
# Mỗi mục là một ô như trong mẫu, nhưng chia thành nhiều hàng liền nhau (ẩn đường kẻ giữa chúng)
# để tiêu đề nhỏ luôn đi cùng đoạn ngay sau nó khi sang trang (LibreOffice bỏ qua "keep with
# next" trong ô bảng, còn "không ngắt hàng" thì cả Word lẫn LibreOffice đều theo).
GIOI_HAN = 1600          # khúc có tiêu đề dài hơn thế thì cho phép ngắt để không để trống nửa trang


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
    runs = [r for r in e.findall(q("r")) if (r.find(q("t")) is not None and (r.find(q("t")).text or "").strip())]
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


def new_row_like(tr0):
    tr = etree.Element(q("tr"))
    tr.append(copy.deepcopy(tr0.find(q("trPr"))))
    tc = etree.SubElement(tr, q("tc"))
    tc.append(copy.deepcopy(tr0.find(q("tc")).find(q("tcPr"))))
    return tr


for tr0, items in ((t_rows[4], noi_dung), (t_rows[5], ke_hoach), (t_rows[6], tai_lieu)):
    chunks = chunks_of(items)
    rows = [tr0]
    for e in chunks[0]:
        tr0.find(q("tc")).append(prepare(e))
    set_cant_split(tr0, size(chunks[0]) <= GIOI_HAN)
    for ch in chunks[1:]:
        tr = new_row_like(tr0)
        for e in ch:
            tr.find(q("tc")).append(prepare(e))
        set_cant_split(tr, (len(ch) > 1 or is_head(ch[0])) and size(ch) <= GIOI_HAN)
        rows[-1].addnext(tr)
        rows.append(tr)
    for k, tr in enumerate(rows):
        if k > 0:
            hide_border(tr, "top")
        if k < len(rows) - 1:
            hide_border(tr, "bottom")

# Nhãn "Kế hoạch thực hiện(Mô tả ..." của mẫu thiếu khoảng trắng trước ngoặc.
for t in label_para(t_rows[5]).iter(q("t")):
    if t.text and t.text.startswith("(Mô tả"):
        t.text = " " + t.text
        t.set(XML_SPACE, "preserve")
        break

# Hàng 7: chữ ký (ô trái giữ nguyên mẫu)
right = t_rows[7].findall(q("tc"))[1]
rps = right.findall(q("p"))
assert ptext(rps[0]).startswith("TP. HCM") and ptext(rps[1]) == "Sinh viên" and ptext(rps[2]) == "(ghi rõ họ tên)"
empties = [p for p in rps[3:] if not ptext(p).strip()]
assert len(empties) == 6


def fill(p_dst, p_src):
    for r in p_dst.findall(q("r")):
        p_dst.remove(r)
    for r in p_src.findall(q("r")):
        if r.find(q("t")) is not None:
            p_dst.append(prepare(copy.deepcopy(r)))


fill(rps[0], ky_ngay)
fill(empties[2], ky_chu_ky)
fill(empties[5], ky_ten)

tdoc.write(str(OUT / "word" / "document.xml"), xml_declaration=True, encoding="UTF-8", standalone=True)
print("Đã dựng:", OUT, "| đoạn nội dung:", len(noi_dung), "| kế hoạch:", len(ke_hoach), "| TLTK:", len(tai_lieu))
