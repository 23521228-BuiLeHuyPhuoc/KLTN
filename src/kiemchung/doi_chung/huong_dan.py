"""Cắt hướng dẫn và ví dụ từ bản hướng dẫn gán nhãn, không đọc nhãn chuẩn."""
import csv
import json
from pathlib import Path
import re

GOC = Path(__file__).resolve().parents[3]
TEP = GOC / "data/huong_dan_gan_nhan.md"


def kiem_khong_lo_kiemtra(chu, tep_mau=GOC / "data/mau_san_pham.csv"):
    """Báo lỗi nếu chữ dùng trong câu lệnh chứa mã mẫu tập kiểm tra."""
    with open(tep_mau, encoding="utf-8-sig", newline="") as f:
        ma = [d["ma_mau"] for d in csv.DictReader(f) if d["tap"] == "kiemtra"]
    lo = [m for m in ma if m in chu]
    if lo:
        raise ValueError(f"hướng dẫn chứa mã tập kiểm tra: {lo}")


def _muc(chu, so):
    m = re.search(rf"^## {so}\. .*?(?=^## |\Z)", chu, re.M | re.S)
    if m is None:
        raise ValueError(f"thiếu mục {so}")
    return m.group(0)


def huong_dan_cho_cau_lenh(tep=TEP):
    """Giữ nguyên chữ mục 3–7, bỏ phần từ tiểu mục 5.1 đến mục 6."""
    chu = Path(tep).read_text(encoding="utf-8-sig")
    cac_muc = [_muc(chu, so) for so in range(3, 8)]
    cac_muc[2] = re.split(r"^### 5\.1\b", cac_muc[2], maxsplit=1, flags=re.M)[0]
    ket_qua = "".join(cac_muc)
    kiem_khong_lo_kiemtra(ket_qua)
    return ket_qua


def vi_du_b2(tep=TEP):
    """Đọc bốn ví dụ đã chỉ định, gồm chữ tuyên bố, bằng chứng, nhãn và lý do."""
    chu = _muc(Path(tep).read_text(encoding="utf-8-sig"), 9)
    ket_qua = []
    for ma in ("V09", "V16", "V24", "V46"):
        m = re.search(rf"^\*\*{ma} · (.*?) · .*?\*\* ([^\n]+)\n(.*?)(?=^\*\*V\d|\Z)", chu, re.M | re.S)
        if m is None:
            raise ValueError(f"thiếu ví dụ {ma}")
        nhan = m[1].split(" (")[0].strip()
        nhan = "Lệch điều kiện" if nhan == "Lệch" else nhan
        dong = {}
        for khoa, ten in (("bang_chung", "Bằng chứng"), ("ly_do", "Lý do")):
            d = re.search(rf"^- {ten}: (.+)$", m[3], re.M)
            if d is None:
                raise ValueError(f"{ma} thiếu {ten}")
            dong[khoa] = d[1]
        ket_qua.append({"id": ma, "tuyen_bo": m[2], "nhan": nhan, **dong,
                        "doan": re.findall(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+#\d+", dong["bang_chung"])})
    kiem_khong_lo_kiemtra(dinh_dang_vi_du(ket_qua))
    return ket_qua


def dinh_dang_vi_du(vi_du):
    """In các ví dụ cách nhau một dòng trống, kết quả là JSON tiếng Việt."""
    return "\n\n".join(
        f"Tuyên bố: {v['tuyen_bo']}\nBằng chứng: {v['bang_chung']}\nKết quả: "
        + json.dumps({k: v[k] for k in ("nhan", "doan", "ly_do")}, ensure_ascii=False) for v in vi_du)
