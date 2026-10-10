# -*- coding: utf-8 -*-
"""Kiểm tra bản đề cương chữ đỏ.

1. Mọi đoạn chữ đen phải là chữ còn nguyên văn từ đề cương đã nộp (de_cuong_da_nop.txt)
   hoặc chữ có sẵn trong mẫu đề cương của Khoa (mau_DeCuongChiTiet_Khoa-MMT_2025.docx).
   Một đoạn đen ghép từ nhãn của mẫu và phần điền còn nguyên văn (ví dụ "Thời gian thực
   hiện: Từ ngày ...") được chấp nhận nếu tách được thành các khúc, mỗi khúc có trong một
   trong hai nguồn.
2. Trích dẫn [n] trong bài liên tục từ 1 đến số tài liệu tham khảo, không thiếu số nào,
   và được đánh số theo thứ tự xuất hiện.

Chạy: python3 kiem_tra.py [đường dẫn bản chữ đỏ]
"""
import re
import sys
from pathlib import Path

import docx

HERE = Path(__file__).resolve().parent
DOCX = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "23521228_BuiLeHuyPhuoc_DeCuongKLTN_chu_do.docx"
MAU = HERE / "mau_DeCuongChiTiet_Khoa-MMT_2025.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
MIN_KHUC = 4          # khúc ngắn hơn thế (sau khi bỏ khoảng trắng) không được tính là có trong nguồn


def q(tag):
    return "{%s}%s" % (W, tag)


def norm(s):
    # Bỏ khoảng trắng và gạch nối vì bản PDF đã nộp bị ngắt dòng, ngắt từ.
    return re.sub(r"\s+", "", s.replace(" ", " ")).replace("-", "")


def docx_text(path):
    d = docx.Document(str(path))
    return "\n".join("".join(t.text or "" for t in p.iter(q("t"))) for p in d.element.body.iter(q("p")))


nguon = [norm((HERE / "de_cuong_da_nop.txt").read_text(encoding="utf-8")), norm(docx_text(MAU))]


def co_trong_nguon(s):
    s = norm(s)
    if not s or any(s in n for n in nguon):
        return True
    i = 0
    while i < len(s):
        dai = 0
        for n in nguon:
            lo, hi = 0, len(s) - i          # tìm khúc dài nhất bắt đầu tại i có trong nguồn n
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if s[i:i + mid] in n:
                    lo = mid
                else:
                    hi = mid - 1
            dai = max(dai, lo)
        if dai < MIN_KHUC:
            return False
        i += dai
    return True


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
        if not co_trong_nguon(s):
            loi += 1
            print("Chữ đen không có trong bản đã nộp hay mẫu của Khoa:", s[:120])
print(f"Đoạn chữ đen: {so_doan}, sai khác: {loi}")

# Lấy chữ của mọi đoạn, kể cả đoạn trong bảng lồng, theo đúng thứ tự trong văn bản.
lines = ["".join(t.text or "" for t in p.iter(q("t"))) for p in doc.element.body.iter(q("p"))]
cut = [i for i, s in enumerate(lines) if s.startswith("Tài liệu tham khảo")]
assert len(cut) == 1, "Không thấy đúng một tiêu đề Tài liệu tham khảo"
body, ref_part = "\n".join(lines[:cut[0]]), "\n".join(lines[cut[0] + 1:])
refs = [int(n) for n in re.findall(r"^\[(\d+)\] ", ref_part, flags=re.M)]
n_refs = len(refs)
assert refs == list(range(1, n_refs + 1)), refs
cited = {int(n) for n in re.findall(r"\[(\d+)\]", body)}
thieu = [i for i in range(1, n_refs + 1) if i not in cited]
thua = sorted(n for n in cited if n > n_refs)
# Trích dẫn theo thứ tự xuất hiện: lần đầu nhắc tới tài liệu n phải sau lần đầu nhắc tới n-1.
first = []
for m in re.finditer(r"\[(\d+)\]", body):
    if int(m.group(1)) not in first:
        first.append(int(m.group(1)))
sai_thu_tu = first != sorted(first)
print(f"Tài liệu tham khảo: {n_refs}, số chưa được trích: {thieu or 'không có'}, "
      f"số trích không có trong danh mục: {thua or 'không có'}, "
      f"thứ tự trích dẫn: {'sai' if sai_thu_tu else 'đúng'}")
sys.exit(1 if loi or thieu or thua or sai_thu_tu else 0)
