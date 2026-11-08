"""Bước 12: chuyển bảng tuyên bố tách tay (CSV) thành data/tuyen_bo/thu.jsonl theo T3.4, có kiểm lỗi.

Người tách điền 4 cột: ma_qc, cau_goc, tuyen_bo, thuoc_tinh (thêm ghi_chu nếu cần). Script tự điền
id (tb-00001...), ma_mau, llm_sinh, che_do, loai_bai từ data/quang_cao/<ma_qc>.json và url_nguon từ
data/mau_san_pham.csv. Kiểm: ma_qc có bài; cau_goc có nguyên văn trong bài (bỏ qua khác biệt khoảng trắng);
thuoc_tinh có trong tệp cấu hình của nhóm; tuyên bố trùng trong cùng bài thì báo.

Chạy:
    Bộ thử (tb-00001...):
    .venv/Scripts/python.exe scripts/chuyen_tuyen_bo.py data/tuyen_bo/thu_nhap.csv data/tuyen_bo/thu.jsonl
    Tập chính (Bước 19, đánh số tiếp sau bộ thử, bắt đầu từ tb-00067):
    .venv/Scripts/python.exe scripts/chuyen_tuyen_bo.py data/tuyen_bo/chinh_nhap.csv data/tuyen_bo/chinh.jsonl --tiep-sau data/tuyen_bo/thu.jsonl

--tiep-sau TEP_JSONL: đánh số từ mã lớn nhất trong tệp đó + 1; ma_qc đã có trong tệp đó là lỗi (bài thuộc bộ khác, không tách lại).
Quy ước của tập chính: dòng n của chinh_nhap.csv (dòng 1 là tiêu đề, dòng trống bỏ qua) ứng với tb-{n-1+66:05d}. Chỉ thêm dòng ở
CUỐI CSV, không chèn giữa, để mã không dịch (Bước 23 sẽ nối tiếp tập kiểm tra vào cùng tệp).
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

GOC = Path(__file__).resolve().parents[1]
NHOM = {"dt": "dien_thoai", "tn": "tai_nghe", "dh": "dong_ho"}
COT_NHAP = ("ma_qc", "cau_goc", "tuyen_bo", "thuoc_tinh")


def gon(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip()


def doc_ma_tiep_sau(tep):
    """Đọc mọi id (dạng tb-NNNNN), ma_qc và ma_mau trong tệp JSONL; trả về (số lớn nhất, tập ma_qc, tập ma_mau). Tệp thiếu hay id
    sai dạng thì thoát lỗi."""
    if not Path(tep).exists():
        sys.exit(f"không thấy tệp --tiep-sau {tep}")
    so_lon, ma_qc, ma_mau = 0, set(), set()
    for n, d in enumerate(Path(tep).read_text(encoding="utf-8-sig").splitlines(), start=1):
        if not d.strip():
            continue
        r = json.loads(d)
        khop = re.fullmatch(r"tb-(\d{5})", str(r.get("id")))
        if not khop:
            sys.exit(f"{tep} dòng {n}: id '{r.get('id')}' không đúng dạng tb-NNNNN")
        so_lon = max(so_lon, int(khop.group(1)))
        ma_qc.add(r.get("ma_qc"))
        ma_mau.add(r.get("ma_mau"))
    return so_lon, ma_qc, ma_mau


def chuyen(vao, ra, tiep_sau=None):
    """Chuyển CSV `vao` thành JSONL `ra` (xem docstring đầu tệp); trả về 0 nếu ghi được, 1 nếu có lỗi (không ghi gì)."""
    sys.stdout.reconfigure(encoding="utf-8")
    so_dau, ma_da_co, mau_da_co = (doc_ma_tiep_sau(tiep_sau) if tiep_sau else (0, set(), set()))
    url = {r["ma_mau"]: r["url"] for r in csv.DictReader(open(GOC / "data" / "mau_san_pham.csv", encoding="utf-8"))}
    thuoc_tinh = {n: set(yaml.safe_load((GOC / "data" / "cau_hinh" / f"{n}.yaml").read_text(encoding="utf-8"))
                         ["thuoc_tinh"]) for n in NHOM.values()}
    bai = {}
    loi, ket_qua, da_thay = [], [], set()
    with open(vao, encoding="utf-8-sig", newline="") as f:  # utf-8-sig: Excel lưu CSV kèm BOM
        dong = list(csv.DictReader(f))
    for so, d in enumerate(dong, start=2):  # dòng 1 là tiêu đề
        if not any((d.get(c) or "").strip() for c in COT_NHAP):
            continue
        thieu = [c for c in COT_NHAP if not (d.get(c) or "").strip()]
        if thieu:
            loi.append(f"dòng {so}: thiếu {', '.join(thieu)}")
            continue
        ma_qc = d["ma_qc"].strip()
        if ma_qc not in bai:
            tep = GOC / "data" / "quang_cao" / f"{ma_qc}.json"
            bai[ma_qc] = json.loads(tep.read_text(encoding="utf-8")) if tep.exists() else None
        b = bai[ma_qc]
        if ma_qc in ma_da_co:
            loi.append(f"dòng {so}: {ma_qc} đã có trong {tiep_sau} (bài thuộc bộ khác, không tách lại)")
            continue
        if b is None:
            loi.append(f"dòng {so}: không có bài {ma_qc}")
            continue
        if b["ma_mau"] in mau_da_co:  # cả bài của bộ kia không có tuyên bố nào (không nằm trong tệp --tiep-sau)
            loi.append(f"dòng {so}: mẫu {b['ma_mau']} thuộc bộ trong {tiep_sau}, không tách vào tệp này")
            continue
        nhom = NHOM[b["ma_mau"][:2]]
        if gon(d["cau_goc"]) not in gon(b["noi_dung"]):
            loi.append(f"dòng {so}: câu gốc không có nguyên văn trong {ma_qc}: {d['cau_goc'][:80]}")
        if d["thuoc_tinh"].strip() not in thuoc_tinh[nhom]:
            loi.append(f"dòng {so}: thuộc tính '{d['thuoc_tinh']}' không có trong {nhom}.yaml "
                       f"({', '.join(sorted(thuoc_tinh[nhom]))})")
        khoa = (ma_qc, gon(d["tuyen_bo"]).lower())
        if khoa in da_thay:
            loi.append(f"dòng {so}: tuyên bố trùng trong cùng bài, cần gộp: {d['tuyen_bo'][:80]}")
        da_thay.add(khoa)
        ket_qua.append({
            "id": f"tb-{so_dau + len(ket_qua) + 1:05d}", "ma_qc": ma_qc, "ma_mau": b["ma_mau"],
            "cau_goc": d["cau_goc"].strip(), "tuyen_bo": d["tuyen_bo"].strip(), "thuoc_tinh": d["thuoc_tinh"].strip(),
            "llm_sinh": b.get("mo_hinh_nha_cung_cap") or b["mo_hinh"], "che_do": b["che_do"], "loai_bai": b["loai_bai"],
            "url_nguon": url[b["ma_mau"]], "ghi_chu": (d.get("ghi_chu") or "").strip(),
        })
    if loi:
        print(f"{len(loi)} lỗi, chưa ghi {ra}:")
        print("\n".join("  " + x for x in loi))
        return 1
    Path(ra).parent.mkdir(parents=True, exist_ok=True)
    with open(ra, "w", encoding="utf-8", newline="\n") as f:
        for r in ket_qua:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    theo_bai = {}
    for r in ket_qua:
        theo_bai[r["ma_qc"]] = theo_bai.get(r["ma_qc"], 0) + 1
    print(f"đã ghi {len(ket_qua)} tuyên bố từ {len(theo_bai)} bài vào {ra}")
    if ket_qua:
        print(f"mã đã ghi: {ket_qua[0]['id']} … {ket_qua[-1]['id']}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Chuyển bảng tuyên bố tách tay (CSV) thành JSONL theo T3.4, có kiểm lỗi.")
    ap.add_argument("vao", help="CSV người tách điền")
    ap.add_argument("ra", help="tệp JSONL ghi ra")
    ap.add_argument("--tiep-sau", metavar="TEP_JSONL", help="đánh số tiếp sau mã lớn nhất của tệp này")
    args = ap.parse_args(argv)
    return chuyen(args.vao, args.ra, args.tiep_sau)


if __name__ == "__main__":
    sys.exit(main())
