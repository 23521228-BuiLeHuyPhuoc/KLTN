"""Chặn tuyên bố tập kiểm tra khi chạy hệ thống (T3.5 quy tắc 4).

Không hệ thống nào (trích xuất bằng LLM, P, đối chứng B0-B3, P-ĐK, P-NN) được chạy trên tuyên bố tập kiểm tra trước khi khóa
cấu hình ở Bước 33. Danh sách mẫu của tập kiểm tra đọc từ data/chia_tap.json (["kiem_tra"]["mau"]); các script chạy hệ thống
lọc tuyên bố qua loc_va_bao, mặc định bỏ mọi tuyên bố có ma_mau thuộc tập kiểm tra và chỉ giữ lại khi có cờ
--cho-phep-tap-kiem-tra.
"""
import json
from pathlib import Path
import sys

GOC = Path(__file__).resolve().parents[2]
TEP_CHIA_TAP = GOC / "data" / "chia_tap.json"
CO_CHO_PHEP = "--cho-phep-tap-kiem-tra"
TRO_GIUP_CO = "chỉ dùng sau khi khóa cấu hình ở Bước 33 (T3.5 quy tắc 4)"


def doc_mau_kiem_tra(tep=TEP_CHIA_TAP):
    """Tập mã mẫu của tập kiểm tra trong data/chia_tap.json; thiếu danh sách thì raise ValueError."""
    with open(tep, encoding="utf-8-sig") as f:
        chia_tap = json.load(f)
    mau = chia_tap.get("kiem_tra", {}).get("mau")
    if not mau:
        raise ValueError(f"{tep} không có danh sách mẫu của tập 'kiem_tra'")
    return set(mau)


def loc_tap_kiem_tra(ban_ghi, cho_phep=False, mau_kiem_tra=None):
    """(phần giữ lại, số bản ghi bị bỏ). Bản ghi là dict có ma_mau, giữ nguyên thứ tự.

    Mặc định bỏ bản ghi có ma_mau thuộc tập kiểm tra; cho_phep=True thì giữ hết và không đọc chia_tap.json."""
    ban_ghi = list(ban_ghi)
    if cho_phep:
        return ban_ghi, 0
    if mau_kiem_tra is None:
        mau_kiem_tra = doc_mau_kiem_tra()
    giu = [b for b in ban_ghi if b["ma_mau"] not in mau_kiem_tra]
    return giu, len(ban_ghi) - len(giu)


def them_co_cho_phep(ap):
    """Thêm cờ --cho-phep-tap-kiem-tra vào argparse."""
    ap.add_argument(CO_CHO_PHEP, action="store_true", help=TRO_GIUP_CO)


def loc_va_bao(ban_ghi, cho_phep=False, mau_kiem_tra=None, file=None):
    """loc_tap_kiem_tra rồi in đúng một dòng báo (ra stderr) nếu có bản ghi bị bỏ; trả phần giữ lại."""
    giu, so_bo = loc_tap_kiem_tra(ban_ghi, cho_phep, mau_kiem_tra)
    if so_bo:
        print(f"Bỏ {so_bo} tuyên bố của tập kiểm tra (T3.5 quy tắc 4); thêm {CO_CHO_PHEP} sau Bước 33 nếu cần.",
              file=file or sys.stderr)
    return giu
