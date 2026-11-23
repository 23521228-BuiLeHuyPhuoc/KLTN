"""Bước 28: chạy lại offline phần hậu xử lý của P (neo nguồn, hiểu điều kiện, kiểm tra đầy đủ) từ tra_ve_tho đã lưu.

Không gọi LLM, không đọc nhãn chuẩn. Đọc tệp kết quả của scripts/chay_trich_xuat.py, chạy lại từng bản ghi bằng
trich_xuat.xu_ly_lai (đoạn đọc lại từ data/nguon theo mã đoạn của bản ghi), điền thoi_gian_sinh_ms từ tệp JSON trong llm_cache
nếu có, rồi ghi tệp mới (cùng định dạng, mỗi tuyên bố một dòng). Chạy:
    .venv/Scripts/python.exe -X utf8 scripts/xu_ly_lai.py --trich-xuat ket_qua/trich_xuat/thu_<...>.jsonl --ra ket_qua/trich_xuat_lai/thu.jsonl
    thêm --khong-neo-nguon để ra bản P-NN (neo_nguon, kiem_day_du cùng False).
"""
import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kiemchung import tap, trich_xuat as tx  # noqa: E402

THU_MUC_CACHE = ROOT / "ket_qua/trich_xuat/llm_cache"


def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(dong) for dong in f if dong.strip()]


def xu_ly_lai_tep(duong_vao, khong_neo_nguon=False, thu_muc_cache=THU_MUC_CACHE, cho_phep_tap_kiem_tra=False):
    """Danh sách bản ghi đã chạy lại của một tệp trích xuất; mặc định bỏ bản ghi của tập kiểm tra (T3.5 quy tắc 4)."""
    co = None if not khong_neo_nguon else False
    ban_ghi = tap.loc_va_bao(doc_jsonl(duong_vao), cho_phep_tap_kiem_tra)
    return [tx.xu_ly_lai(b, neo_nguon=co, kiem_day_du=co, thu_muc_cache=thu_muc_cache) for b in ban_ghi]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Chạy lại hậu xử lý của P từ tra_ve_tho (offline).")
    ap.add_argument("--trich-xuat", type=Path, required=True)
    ap.add_argument("--ra", type=Path, required=True)
    ap.add_argument("--khong-neo-nguon", action="store_true", help="P-NN: tắt neo nguồn và kiểm tra đầy đủ")
    ap.add_argument("--thu-muc-cache", type=Path, default=THU_MUC_CACHE, help="llm_cache để lấy generation_ms")
    tap.them_co_cho_phep(ap)
    args = ap.parse_args(argv)
    ban_ghi = xu_ly_lai_tep(args.trich_xuat, args.khong_neo_nguon, args.thu_muc_cache, args.cho_phep_tap_kiem_tra)
    args.ra.parent.mkdir(parents=True, exist_ok=True)
    tam = args.ra.with_name(args.ra.name + ".tmp")
    tam.write_text("".join(json.dumps(b, ensure_ascii=False, sort_keys=True) + "\n" for b in ban_ghi), encoding="utf-8", newline="\n")
    os.replace(tam, args.ra)
    co_giay = sum(1 for b in ban_ghi if b.get("thoi_gian_sinh_ms") is not None)
    print(f"Đã ghi {len(ban_ghi)} bản ghi vào {args.ra} (có thoi_gian_sinh_ms: {co_giay}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
