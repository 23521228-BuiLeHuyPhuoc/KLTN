"""Kiểm tệp cấu hình điều kiện ở data/cau_hinh/ (Bước 8). In lỗi theo từng tệp; có lỗi thì mã thoát 1."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kiemchung import cau_hinh as ch  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ket_qua = ch.kiem_tat_ca()
    for phan, loi in ket_qua.items():
        if phan != "chung":
            so_tt = len(ch.doc_cau_hinh(phan)["thuoc_tinh"])
            print(f"{phan}: {so_tt} thuộc tính, {len(loi)} lỗi")
        else:
            print(f"chung: {len(loi)} lỗi")
        for dong in loi:
            print(f"    {dong}")
    return 1 if any(ket_qua.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
