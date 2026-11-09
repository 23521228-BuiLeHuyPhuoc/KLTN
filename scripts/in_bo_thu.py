"""Bước 12, 19: in các bài quảng cáo của một nhóm mẫu ra tệp markdown để đọc khi tách tay, và tạo bảng nhập CSV
(chỉ dòng tiêu đề) nếu chưa có. Bài in nguyên văn, không đánh dấu câu nào, không gọi LLM.

Chạy:
    Bộ thử (Bước 12, mặc định): .venv/Scripts/python.exe scripts/in_bo_thu.py
        -> data/tuyen_bo/doc_bo_thu.md và data/tuyen_bo/thu_nhap.csv
    Tập phát triển (Bước 19): .venv/Scripts/python.exe scripts/in_bo_thu.py --mau dh-apple-watchse3 dt-xiaomi-15t
        --ra data/tuyen_bo/doc_phat_trien.md --csv data/tuyen_bo/chinh_nhap.csv
        --tieu-de "# {so} bài của tập phát triển (Bước 19)"
        -> data/tuyen_bo/doc_phat_trien.md và data/tuyen_bo/chinh_nhap.csv
Tệp CSV chỉ được tạo khi chưa có, không ghi đè.
"""
import argparse
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
THU_MUC_QC = GOC / "data" / "quang_cao"
THU_MUC_TB = GOC / "data" / "tuyen_bo"
TEN_LOAI = {"description": "Mô tả sản phẩm", "social": "Bài mạng xã hội", "landing": "Landing page"}
TEN_CHE_DO = {"ten": "chỉ nhập tên", "ten_thong_so": "nhập tên và thông số"}
MAU_BO_THU = ["dt-apple-iphone17", "tn-samsung-buds3pro"]
TIEU_DE_BO_THU = "# 24 bài của bộ thử (Bước 12)"
TIEU_DE_CSV = "ma_qc,cau_goc,tuyen_bo,thuoc_tinh,ghi_chu,can_xem\n"


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="In bài quảng cáo của các mẫu ra markdown để tách tay.")
    ap.add_argument("--mau", nargs="+", default=MAU_BO_THU, metavar="MA_MAU", help="mặc định: mẫu của bộ thử")
    ap.add_argument("--ra", type=Path, default=THU_MUC_TB / "doc_bo_thu.md", help="mặc định data/tuyen_bo/doc_bo_thu.md")
    ap.add_argument("--csv", type=Path, default=THU_MUC_TB / "thu_nhap.csv", help="mặc định data/tuyen_bo/thu_nhap.csv")
    ap.add_argument("--tieu-de", default=TIEU_DE_BO_THU, help="dòng tiêu đề; {so} được điền số bài")
    args = ap.parse_args(argv)
    bai = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(THU_MUC_QC.glob("qc-*.json"))]
    bai = [b for b in bai if b["ma_mau"] in args.mau]
    thieu = [m for m in args.mau if not any(b["ma_mau"] == m for b in bai)]
    if thieu:
        print(f"không có bài nào của mẫu: {', '.join(thieu)}", file=sys.stderr)
        return 1
    dong = [args.tieu_de.format(so=len(bai)), "",
            "Đọc theo hướng dẫn `data/tuyen_bo/huong_dan_tach_tay.md`. Mã bài ở dòng tiêu đề, chép vào cột `ma_qc`.", ""]
    for b in bai:
        dong += [f"## `{b['ma_qc']}`", "",
                 f"{b['ten_nhap']} · {b['mo_hinh_nha_cung_cap'] or b['mo_hinh']} · {TEN_LOAI[b['loai_bai']]} · "
                 f"{TEN_CHE_DO[b['che_do']]}", "", "```text", b["noi_dung"].rstrip(), "```", ""]
    args.ra.parent.mkdir(parents=True, exist_ok=True)
    args.ra.write_text("\n".join(dong), encoding="utf-8", newline="\n")
    if not args.csv.exists():
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        args.csv.write_text(TIEU_DE_CSV, encoding="utf-8-sig", newline="\n")
    print(f"đã in {len(bai)} bài vào {args.ra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
