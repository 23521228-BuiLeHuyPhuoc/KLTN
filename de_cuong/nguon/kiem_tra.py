# -*- coding: utf-8 -*-
"""Kiểm tra bản đề cương chữ đỏ sau khi dựng.

1. Mọi đoạn chữ đen phải có nguyên văn trong đề cương đã nộp (de_cuong_da_nop.txt).
2. Trích dẫn [n] trong bài liên tục từ 1 đến số tài liệu tham khảo, không thiếu số nào.

Chạy: python3 kiem_tra.py  (sau khi chạy python3 dung_docx.py)
"""
import re
import sys
from pathlib import Path

import docx

HERE = Path(__file__).resolve().parent
DOCX = HERE.parent / "23521228_BuiLeHuyPhuoc_DeCuongKLTN_chu_do.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def q(tag):
    return "{%s}%s" % (W, tag)


def norm(s):
    # Bỏ khoảng trắng và gạch nối vì bản PDF đã nộp bị ngắt dòng, ngắt từ.
    return re.sub(r"\s+", "", s.replace(" ", " ")).replace("-", "")


raw = norm((HERE / "de_cuong_da_nop.txt").read_text(encoding="utf-8"))
doc = docx.Document(str(DOCX))

loi = 0
so_doan = 0
for p in doc.element.body.iter(q("p")):
    seg, segs = "", []
    for r in p.iter(q("r")):
        t = "".join(x.text or "" for x in r.iter(q("t")))
        if not t:
            continue
        rpr = r.find(q("rPr"))
        col = rpr.find(q("color")) if rpr is not None else None
        if col is not None and col.get(q("val")) == "FF0000":
            if seg.strip():
                segs.append(seg)
            seg = ""
        else:
            seg += t
    if seg.strip():
        segs.append(seg)
    for s in segs:
        so_doan += 1
        if norm(s) not in raw:
            loi += 1
            print("Chữ đen không có trong bản đã nộp:", s[:120])
print(f"Đoạn chữ đen: {so_doan}, sai khác: {loi}")

text = "\n".join(p.text for p in doc.paragraphs)
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            text += "\n" + cell.text
refs = re.findall(r"^\[(\d+)\] ", text, flags=re.M)
cited = {int(n) for n in re.findall(r"\[(\d+)\]", text)}
n_refs = len(set(refs))
thieu = [i for i in range(1, n_refs + 1) if i not in cited]
print(f"Tài liệu tham khảo: {n_refs}, số chưa được trích: {thieu or 'không có'}")
sys.exit(1 if loi or thieu else 0)
