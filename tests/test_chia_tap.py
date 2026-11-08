"""Bước 26: data/chia_tap.json khớp cách chia theo mẫu ở data/mau_san_pham.csv (Bước 4)."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_chia_tap_khop_mau_san_pham():
    chia = json.loads((ROOT / "data/chia_tap.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader(open(ROOT / "data/mau_san_pham.csv", encoding="utf-8")))
    assert chia["phat_trien"]["mau"] == [r["ma_mau"] for r in rows if r["tap"] == "phattrien"]
    assert chia["kiem_tra"]["mau"] == [r["ma_mau"] for r in rows if r["tap"] == "kiemtra"]
    assert not set(chia["phat_trien"]["mau"]) & set(chia["kiem_tra"]["mau"])
    assert set(chia["phat_trien"]["mau_thu"]) <= set(chia["phat_trien"]["mau"])
    # Tập kiểm tra có đủ ba nhóm và bốn hãng (T6.3).
    assert chia["kiem_tra"]["nhom"] == ["dien_thoai", "dong_ho", "tai_nghe"]
    assert len(chia["kiem_tra"]["hang"]) == 4
    assert chia["sha256_mau_san_pham_csv"] == hashlib.sha256((ROOT / "data/mau_san_pham.csv").read_bytes()).hexdigest()
