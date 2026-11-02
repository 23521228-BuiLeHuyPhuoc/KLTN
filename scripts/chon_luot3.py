"""Chọn 30 tuyên bố của bộ thử cho lượt 3 (người thực hiện tự gán lại mù, rồi đo độ nhất quán bằng scripts/do_nhat_quan.py).

Cách chọn: mọi tuyên bố có nhan == "LECH" trong data/nhan/thu_luot2.jsonl, cộng thêm các tuyên bố không phải LECH rút ngẫu
nhiên cho đủ 30 bằng random.Random(20261102).sample trên danh sách mã không phải LECH đã xếp theo thứ tự mã. Kết quả xếp
theo thứ tự mã, ghi vào data/nhan/chon_luot3.txt (một dòng chú thích bắt đầu bằng #, rồi mỗi dòng một mã). Hàm chon_luot3
tất định: cùng nhãn lượt 2, cùng seed và cùng số lượng thì cùng danh sách.

Script cố ý chỉ in số lượng, không in mã hay nhãn của các tuyên bố đã chọn, vì lượt 3 gán mù. Mẫu chọn theo nhãn lượt 2 nên
không phải mẫu ngẫu nhiên của bộ thử (tỷ lệ Lệch trong mẫu cao hơn trong bộ thử), xem ghi chú ở báo cáo của do_nhat_quan.py.

Chạy: .venv/Scripts/python.exe scripts/chon_luot3.py
Rồi sinh trang gán nhãn lượt 3:
    .venv/Scripts/python.exe scripts/tao_cong_cu_gan_nhan.py --luot 3 --chon data/nhan/chon_luot3.txt --ra data/nhan/cong_cu_gan_nhan_luot3.html
"""
import argparse
import json
from pathlib import Path
import random
import sys

GOC = Path(__file__).resolve().parents[1]
TEP_NHAN_LUOT2 = GOC / "data" / "nhan" / "thu_luot2.jsonl"
TEP_RA = GOC / "data" / "nhan" / "chon_luot3.txt"
SEED = 20261102
SO_CHON = 30
NHAN_LECH = "LECH"


def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(dong) for dong in f if dong.strip()]


def chon_luot3(dong_nhan, so_chon=SO_CHON, seed=SEED):
    """Danh sách mã (xếp theo thứ tự mã) của lượt 3: mọi mã có nhan == "LECH" trong dong_nhan, cộng so_chon - (số LECH) mã
    không phải LECH rút bằng random.Random(seed).sample trên các mã không phải LECH đã xếp theo thứ tự mã.

    Lỗi (ValueError): mã lặp, số LECH quá so_chon, hoặc không đủ mã không phải LECH để bù."""
    ma = [nh["id"] for nh in dong_nhan]
    lap = sorted({m for m in ma if ma.count(m) > 1})
    if lap:
        raise ValueError("mã lặp trong tệp nhãn: " + ", ".join(lap))
    lech = sorted(nh["id"] for nh in dong_nhan if nh.get("nhan") == NHAN_LECH)
    khac = sorted(nh["id"] for nh in dong_nhan if nh.get("nhan") != NHAN_LECH)
    them = so_chon - len(lech)
    if them < 0:
        raise ValueError(f"có {len(lech)} tuyên bố {NHAN_LECH}, nhiều hơn số cần chọn {so_chon}")
    if them > len(khac):
        raise ValueError(f"cần thêm {them} tuyên bố không phải {NHAN_LECH}, chỉ có {len(khac)}")
    return sorted(lech + random.Random(seed).sample(khac, them))


def dong_chu_thich(so_chon=SO_CHON, seed=SEED):
    return (f"# Lượt 3: mọi tuyên bố có nhan == \"{NHAN_LECH}\" trong data/nhan/thu_luot2.jsonl, cộng tuyên bố không phải "
            f"{NHAN_LECH} rút bằng random.Random({seed}).sample trên các mã đã xếp theo thứ tự mã cho đủ {so_chon}; "
            f"xếp theo thứ tự mã. Sinh bằng scripts/chon_luot3.py.")


def ghi_chon(duong, ma, so_chon=SO_CHON, seed=SEED):
    duong = Path(duong)
    duong.parent.mkdir(parents=True, exist_ok=True)
    duong.write_text(dong_chu_thich(so_chon, seed) + "\n" + "".join(m + "\n" for m in ma), encoding="utf-8", newline="\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Chọn tuyên bố cho lượt 3 (gán lại mù một phần bộ thử).")
    ap.add_argument("--nhan", type=Path, default=TEP_NHAN_LUOT2, help="tệp nhãn lượt 2 (mặc định data/nhan/thu_luot2.jsonl)")
    ap.add_argument("--ra", type=Path, default=TEP_RA, help="tệp mã sinh ra (mặc định data/nhan/chon_luot3.txt)")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    if not args.nhan.exists():
        sys.exit(f"không thấy tệp {args.nhan}")
    dong_nhan = doc_jsonl(args.nhan)
    try:
        ma = chon_luot3(dong_nhan)
    except ValueError as e:
        sys.exit(f"{args.nhan.name}: {e}")
    ghi_chon(args.ra, ma)
    so_lech = sum(1 for nh in dong_nhan if nh.get("nhan") == NHAN_LECH)
    print(f"đã ghi {args.ra}: {len(ma)} mã ({so_lech} {NHAN_LECH} của lượt 2 + {len(ma) - so_lech} mã khác, seed {SEED}); "
          f"không in danh sách vì lượt 3 gán mù")


if __name__ == "__main__":
    main()
