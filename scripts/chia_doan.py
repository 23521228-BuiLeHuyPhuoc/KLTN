"""Chia page.txt của 12 mẫu thành đoạn cho BM25 (Bước 7).

Mỗi mẫu ghi data/nguon/<ma_mau>/doan.jsonl (trang chính trước, bo_sung sau, mã <ma_mau>#001...), in
bảng tóm tắt, và lấy 20 đoạn ngẫu nhiên (seed cố định) ghi vào data/kiem_doan_buoc7_lan2.md để kiểm bằng mắt
(data/kiem_doan_buoc7.md là kết quả lần 1, giữ nguyên, script không ghi vào đó).
Chỉ đọc page.txt/page.html (không sửa tệp bằng chứng), chỉ thêm doan.jsonl.

Mỗi đoạn có hai trường văn bản: noi_dung đã bỏ ký hiệu chú thích của trang hãng (số dính chữ 'Thấp8', nhóm số cuối
dòng, dấu * làm ký hiệu; ký hiệu bị bỏ sót thì bỏ thêm bằng bảng ghi tay KY_HIEU_BO_THEM) và noi_dung_goc là văn bản trước
khi bỏ. Báo cáo các chỗ đã bỏ: scripts/kiem_bo_so_chu_thich.py.
"""
import argparse
import csv
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kiemchung import chia_doan as cd  # noqa: E402

CSV_PATH = ROOT / "data/mau_san_pham.csv"
OUT_ROOT = ROOT / "data/nguon"
KIEM_PATH = ROOT / "data/kiem_doan_buoc7_lan2.md"
TRUONG_JSONL = ("id", "ma_mau", "trang", "muc", "noi_dung", "noi_dung_goc", "chu_thich", "dong")
TEP_PDF = "page_pdftotext.txt"  # PDF: dùng bản pdftotext nếu có (pypdf tách âm tiết và số), xem trich_pdf_pdftotext.py
SEED_KIEM = 20261025
SO_DOAN_KIEM = 20
TRAN_3_CHU_SO = 999  # quá mức này thì mã đoạn dùng 4 chữ số cho cả 12 mẫu


def doc_mau(path=CSV_PATH):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def chon_mau(rows, ma_mau):
    if not ma_mau:
        return list(rows)
    theo_ma = {row["ma_mau"]: row for row in rows}
    thieu = [m for m in ma_mau if m not in theo_ma]
    if thieu:
        raise ValueError("ma_mau không có trong CSV: " + ", ".join(thieu))
    return [theo_ma[m] for m in dict.fromkeys(ma_mau)]


def trang_cua_mau(row, out_root=OUT_ROOT):
    """[(vai trò, thư mục)] của trang chính (url) rồi trang bổ sung (bo_sung) nếu có."""
    goc = Path(out_root) / row["ma_mau"]
    ket_qua = [("url", goc)]
    if row.get("url_bo_sung", "").strip():
        ket_qua.append(("bo_sung", goc / "bo_sung"))
    return ket_qua


def chia_mot_mau(row, out_root=OUT_ROOT):
    """Trả (list (trang, list đoạn), thống kê) của một mẫu.

    thống kê: khong_tim_duoc (ký hiệu không có nội dung chú thích), khong_duoc_dan ('trang:số' của chú thích không
    đoạn nào dẫn tới), gan_theo_vi_tri (chú thích đứng lẻ giữa trang, gắn vào đoạn phía trên), khong_co_trong_txt
    ('trang:số' của chú thích có trong HTML mà không có trong page.txt).
    """
    theo_trang = []
    tong = {"khong_tim_duoc": [], "khong_duoc_dan": [], "gan_theo_vi_tri": [], "khong_co_trong_txt": []}
    for trang, thu_muc in trang_cua_mau(row, out_root):
        tep = TEP_PDF if (thu_muc / TEP_PDF).exists() else "page.txt"
        van_ban = (thu_muc / tep).read_text(encoding="utf-8")
        ma_html = (thu_muc / "page.html").read_text(encoding="utf-8") if (thu_muc / "page.html").exists() else ""
        doan, thong_ke = cd.chia_doan_day_du(van_ban, cd.doc_chu_thich_html(ma_html))
        theo_trang.append((trang, doan))
        tong["khong_tim_duoc"] += thong_ke["khong_tim_duoc"]
        for khoa in ("khong_duoc_dan", "gan_theo_vi_tri", "khong_co_trong_txt"):
            tong[khoa] += [f"{trang}:{so}" for so in thong_ke.get(khoa, [])]
    return theo_trang, tong


def so_chu_so_ma(so_doan_lon_nhat):
    return 4 if so_doan_lon_nhat > TRAN_3_CHU_SO else 3


def ghi_jsonl(path, dong):
    """Ghi các trường của TRUONG_JSONL (danh_ma_doan còn trả ky_hieu_bo, chỉ là nhật ký để báo cáo)."""
    noi_dung = "".join(json.dumps({k: d[k] for k in TRUONG_JSONL}, ensure_ascii=False) + "\n" for d in dong)
    Path(path).write_text(noi_dung, encoding="utf-8", newline="\n")


def co_chu_so(d):
    return any(c.isdigit() for c in d["noi_dung"])


def lay_mau_kiem(doan, so_luong=SO_DOAN_KIEM, seed=SEED_KIEM):
    """Ngẫu nhiên `so_luong` đoạn, ưu tiên đoạn có chữ số: trước hết mỗi mẫu một đoạn (để phủ đủ các
    mẫu, vì PDF Galaxy Watch8 chiếm hơn một nửa số đoạn), phần còn lại rút từ toàn bộ. Thứ tự theo mã."""
    rng = random.Random(seed)
    doan = sorted(doan, key=lambda d: d["id"])
    chon = []
    for ma_mau in sorted({d["ma_mau"] for d in doan}):
        cua_mau = [d for d in doan if d["ma_mau"] == ma_mau]
        chon.append(rng.choice([d for d in cua_mau if co_chu_so(d)] or cua_mau))
    chon = chon[:so_luong]
    con_lai = [d for d in doan if d not in chon]
    uu_tien = [d for d in con_lai if co_chu_so(d)]
    thieu = so_luong - len(chon)
    chon += rng.sample(uu_tien, min(thieu, len(uu_tien)))
    if len(chon) < so_luong:
        khac = [d for d in con_lai if d not in chon]
        chon += rng.sample(khac, min(so_luong - len(chon), len(khac)))
    return sorted(chon, key=lambda d: d["id"]), sum(1 for d in doan if co_chu_so(d))


def viet_kiem_md(mau, so_co_so, tong, seed=SEED_KIEM):
    dong = [
        "# Kiểm bằng mắt 20 đoạn ngẫu nhiên (Bước 7, lần 2)",
        "",
        f"- Seed: {seed} (`random.Random({seed})`). Chọn 12 đoạn (mỗi mẫu một) rồi 8 đoạn từ toàn bộ, ưu tiên đoạn có "
        f"chữ số ({so_co_so} trong tổng {tong} đoạn của 12 mẫu); sinh bằng `scripts/chia_doan.py`.",
        "- Cách kiểm: mở `page.txt` ở dòng ghi trong `dong`, đối chiếu từng con số trong `noi_dung` với điều kiện "
        "đi kèm; điều kiện nằm trong `noi_dung` hoặc `chu_thich` là đạt.",
        "",
    ]
    for d in mau:
        dong += [f"## {d['id']}", "", f"- Mục: {d['muc'] or '(chưa có)'}; trang: {d['trang']}; dòng: "
                 f"{d['dong'][0]}-{d['dong'][1]}", "- Nội dung:", "", "```text", d["noi_dung"], "```", ""]
        if d["chu_thich"]:
            dong += ["- Chú thích:", ""]
            for i, ct in enumerate(d["chu_thich"], start=1):
                dong += [f"  {i}. {ct}"]
            dong += [""]
        else:
            dong += ["- Chú thích: (không có)", ""]
        dong += ["- Kết quả kiểm: [ ] không mất điều kiện   [ ] mất điều kiện: ...", ""]
    return "\n".join(dong)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Chia page.txt thành đoạn cho BM25.")
    parser.add_argument("ma_mau", nargs="*", help="ma_mau trong data/mau_san_pham.csv; bỏ trống = cả 12 mẫu")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    rows = chon_mau(doc_mau(), args.ma_mau)

    ket_qua = {row["ma_mau"]: chia_mot_mau(row) for row in rows}
    lon_nhat = max(sum(len(d) for _, d in theo_trang) for theo_trang, _ in ket_qua.values())
    rong = so_chu_so_ma(lon_nhat)

    print(f"{'ma_mau':34}{'đoạn':>6}{'có chú thích':>14}{'ký hiệu không tìm được':>24}{'chú thích không được dẫn':>26}")
    tat_ca = []
    for row in rows:
        theo_trang, tk = ket_qua[row["ma_mau"]]
        doan = cd.danh_ma_doan(row["ma_mau"], theo_trang, rong)
        ghi_jsonl(OUT_ROOT / row["ma_mau"] / "doan.jsonl", doan)
        tat_ca += doan
        co_ct = sum(1 for d in doan if d["chu_thich"])
        print(f"{row['ma_mau']:34}{len(doan):>6}{co_ct:>14}{len(tk['khong_tim_duoc']):>24}{len(tk['khong_duoc_dan']):>26}")
        for khoa, nhan in (("khong_tim_duoc", "ký hiệu không có nội dung"), ("khong_duoc_dan", "chú thích không được dẫn"),
                           ("gan_theo_vi_tri", "chú thích gắn theo vị trí (đứng lẻ, không ký hiệu)"),
                           ("khong_co_trong_txt", "chú thích chỉ có trong HTML")):
            if tk[khoa]:
                print(f"    {nhan}: {', '.join(tk[khoa])}")
    print(f"Mã đoạn dùng {rong} chữ số (đoạn nhiều nhất của một mẫu: {lon_nhat}).")
    if KIEM_PATH.exists():  # tệp kiểm đã có kết quả kiểm bằng mắt, không ghi đè
        print(f"Giữ nguyên {KIEM_PATH.relative_to(ROOT)} (đã có).")
        return 0
    mau, so_co_so = lay_mau_kiem(tat_ca)
    KIEM_PATH.write_text(viet_kiem_md(mau, so_co_so, len(tat_ca)), encoding="utf-8", newline="\n")
    print(f"Ghi {len(mau)} đoạn kiểm (seed {SEED_KIEM}) vào {KIEM_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
