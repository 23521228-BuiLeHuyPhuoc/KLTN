# -*- coding: utf-8 -*-
"""Tạo bản chữ đỏ: chữ đen = còn nguyên văn từ đề cương đã nộp, chữ đỏ = mới hoặc đã sửa.

Màu được kế thừa từ bản chữ đỏ cũ (trên GitHub) ở những chỗ chữ không đổi; chỗ thêm hoặc sửa
thành đỏ. Cuối cùng, mọi đoạn chữ đen phải có nguyên văn trong de_cuong_da_nop.txt, nếu không
thì cũng tô đỏ.

Chạy: python3 to_mau_do.py <bản đỏ cũ.docx> <thư mục đã giải nén của bản sạch mới> <de_cuong_da_nop.txt>
(thư mục được sửa tại chỗ)
"""
import copy
import difflib
import re
import sys
from pathlib import Path

import docx
from lxml import etree

OLD, NEWDIR, GOC = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
RED = "FF0000"
MIN_BLOCK = 6          # khối trùng ngắn hơn thế không được giữ màu đen (tránh vụn)


def q(tag):
    return "{%s}%s" % (W, tag)


def norm(s):
    return re.sub(r"\s+", "", s.replace(" ", " ")).replace("-", "")


# ------------------------------------------------ màu từng ký tự của bản đỏ cũ
def old_paras(path):
    d = docx.Document(str(path))
    out = []
    for p in d.element.body.iter(q("p")):
        text, cols = "", []
        for r in p.iter(q("r")):
            t = "".join(x.text or "" for x in r.iter(q("t")))
            if not t:
                continue
            rpr = r.find(q("rPr"))
            c = rpr.find(q("color")) if rpr is not None else None
            red = c is not None and c.get(q("val")) == RED
            text += t
            cols += [red] * len(t)
        out.append((text, cols))
    return out


old = old_paras(OLD)

doc_path = NEWDIR / "word" / "document.xml"
tree = etree.parse(str(doc_path), etree.XMLParser(remove_blank_text=False, huge_tree=True))
body = tree.getroot().find(q("body"))
new_ps = list(body.iter(q("p")))


def ptext(p):
    return "".join(t.text or "" for t in p.iter(q("t")))


new_txt = [ptext(p) for p in new_ps]

# ------------------------------------------------ ghép đoạn mới với đoạn cũ
pair = {}
sm = difflib.SequenceMatcher(None, [t for t, _ in old], new_txt, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            pair[j1 + k] = i1 + k
    elif tag == "replace":
        for j in range(j1, j2):
            if not new_txt[j].strip():
                continue
            best, score = None, 0.0
            for i in range(i1, i2):
                r = difflib.SequenceMatcher(None, old[i][0], new_txt[j], autojunk=False).ratio()
                if r > score:
                    best, score = i, r
            if best is not None and score >= 0.7:
                pair[j] = best

# ------------------------------------------------ màu từng ký tự của bản mới
colors = []
for j, t in enumerate(new_txt):
    red = [True] * len(t)
    if j in pair:
        ot, oc = old[pair[j]]
        for a, b, size in difflib.SequenceMatcher(None, ot, t, autojunk=False).get_matching_blocks():
            if size >= MIN_BLOCK or (size == len(t) and size > 0):
                for k in range(size):
                    red[b + k] = oc[a + k]
    colors.append(red)

# Kiểm tra an toàn: đoạn chữ đen phải có nguyên văn trong đề cương đã nộp.
raw = norm(GOC.read_text(encoding="utf-8"))
sua = 0
for j, t in enumerate(new_txt):
    red = colors[j]
    k = 0
    while k < len(t):
        if red[k]:
            k += 1
            continue
        e = k
        while e < len(t) and not red[e]:
            e += 1
        seg = t[k:e]
        if seg.strip() and norm(seg) not in raw:
            for x in range(k, e):
                red[x] = True
            sua += 1
        k = e
print("Đoạn chữ đen không có trong bản đã nộp, đã chuyển sang đỏ:", sua)

# ------------------------------------------------ tách run và tô màu
ORDER_AFTER = ["spacing", "w", "kern", "position", "sz", "szCs", "highlight", "u", "effect", "bdr",
               "shd", "fitText", "vertAlign", "rtl", "cs", "em", "lang", "eastAsianLayout",
               "specVanish", "oMath"]


def set_red(r):
    rpr = r.find(q("rPr"))
    if rpr is None:
        rpr = etree.Element(q("rPr"))
        r.insert(0, rpr)
    c = rpr.find(q("color"))
    if c is None:
        c = etree.Element(q("color"))
        pos = None
        for i, ch in enumerate(rpr):
            if etree.QName(ch).localname in ORDER_AFTER:
                pos = i
                break
        if pos is None:
            rpr.append(c)
        else:
            rpr.insert(pos, c)
    c.set(q("val"), RED)


n_do = 0
for j, p in enumerate(new_ps):
    t_all = new_txt[j]
    if not t_all:
        continue
    red = colors[j]
    off = 0
    for r in list(p.iter(q("r"))):
        ts = r.findall(q("t"))
        if not ts:
            continue
        assert len(ts) == 1 and len([k for k in r if k.tag not in (q("rPr"), q("t"))]) == 0, "run lạ"
        t = ts[0].text or ""
        seg_cols = red[off: off + len(t)]
        off += len(t)
        if not t:
            continue
        # gom các khúc cùng màu
        parts, s = [], 0
        for k in range(1, len(t) + 1):
            if k == len(t) or seg_cols[k] != seg_cols[s]:
                parts.append((t[s:k], seg_cols[s]))
                s = k
        if len(parts) == 1:
            if parts[0][1]:
                set_red(r)
                n_do += len(t)
            continue
        anchor = r
        for txt, is_red in parts:
            nr = copy.deepcopy(r)
            nt = nr.find(q("t"))
            nt.text = txt
            nt.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            if is_red:
                set_red(nr)
                n_do += len(txt)
            anchor.addnext(nr)
            anchor = nr
        r.getparent().remove(r)
    assert off == len(t_all), (j, off, len(t_all))

tree.write(str(doc_path), xml_declaration=True, encoding="UTF-8", standalone=True)
tong = sum(len(t) for t in new_txt)
print(f"Ký tự đỏ: {n_do}/{tong}")
