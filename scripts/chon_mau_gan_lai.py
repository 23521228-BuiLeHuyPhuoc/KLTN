"""Bước 26: chọn ngẫu nhiên phân tầng 20% số tuyên bố của tập chính để người thực hiện tự gán lại mù ở Bước 32.

Quần thể: mọi tuyên bố của data/tuyen_bo/chinh.jsonl (không gồm bộ thử, vì bộ thử đã có lượt 3 gán lại mù riêng). Tầng là
(tập, nhóm): tập (phat_trien / kiem_tra) tra từ ma_mau theo data/chia_tap.json, nhóm là tiền tố trước dấu "-" đầu tiên của
ma_mau (dt, tn, dh). Tổng số chọn n = round(ty_le * N); chia cho các tầng theo tỉ lệ bằng phương pháp phần dư lớn nhất
(hòa phần dư thì tầng có tên sắp xếp trước được ưu tiên), mỗi tầng không rỗng có ít nhất 1 (nếu tổng vượt n thì lấy bớt ở
tầng lớn nhất). Trong mỗi tầng, mã xếp tăng dần rồi rút bằng một đối tượng random.Random(seed) duy nhất, duyệt các tầng theo
thứ tự tên tầng, nên chạy lại cho đúng kết quả cũ.

Script chỉ ghi data/nhan/danh_sach_mau.json, không đọc bất kỳ tệp nào trong data/nhan/ (chọn mẫu không mở nhãn); đọc nhãn
sẽ lộ thông tin cho bước gán lại mù. Cờ --in chỉ in kết quả ra màn hình, không ghi tệp.

Chạy: .venv/Scripts/python.exe scripts/chon_mau_gan_lai.py
"""
import argparse
import json
from pathlib import Path
import random
import sys

GOC = Path(__file__).resolve().parents[1]
TEP_TUYEN_BO = GOC / "data" / "tuyen_bo" / "chinh.jsonl"
TEP_CHIA_TAP = GOC / "data" / "chia_tap.json"
TEP_RA = GOC / "data" / "nhan" / "danh_sach_mau.json"
SEED = 20261126
TY_LE = 0.2
QUAN_THE = "258 tuyên bố tập chính (tb-00067–tb-00325); không gồm bộ thử, đã có lượt 3"
GHI_CHU_NGUOI_THU_HAI = "Chưa có người gán thứ hai; chờ CBHD"
QUY_TAC = ("Chọn ngẫu nhiên phân tầng theo (tập, nhóm): tổng round(ty_le × N), chia cho các tầng theo tỉ lệ bằng phương pháp "
           "phần dư lớn nhất, mỗi tầng không rỗng có ít nhất 1. Trong mỗi tầng xếp mã tăng dần rồi random.Random(seed).sample, "
           "duyệt các tầng theo thứ tự tên tầng.")


def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(dong) for dong in f if dong.strip()]


def doc_json(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return json.load(f)


def ten_tang(ma_mau, chia_tap):
    """"<tập>/<nhóm>" của một mẫu; mẫu không thuộc tập nào thì raise ValueError."""
    tap = [t for t in ("phat_trien", "kiem_tra") if ma_mau in chia_tap.get(t, {}).get("mau", [])]
    if len(tap) != 1:
        raise ValueError(f"mẫu {ma_mau} không thuộc đúng một tập trong chia_tap.json")
    return f"{tap[0]}/{ma_mau.split('-', 1)[0]}"


def chia_tieu_chuan(so_tang, n):
    """{tầng: số chọn}: phần dư lớn nhất (hòa thì tên tầng sắp xếp trước), rồi ép mỗi tầng không rỗng có ít nhất 1."""
    tong = sum(so_tang.values())
    if not 0 <= n <= tong:
        raise ValueError(f"số chọn {n} ngoài khoảng 0..{tong}")
    chon = {t: n * s // tong for t, s in so_tang.items()}
    du = sorted(so_tang, key=lambda t: (-(n * so_tang[t] % tong), t))
    for t in du[:n - sum(chon.values())]:
        chon[t] += 1
    for t, s in so_tang.items():
        if s > 0 and chon[t] == 0:
            chon[t] = 1
    while sum(chon.values()) > n:
        t = max((t for t in chon if chon[t] > 1), key=lambda t: (chon[t], t), default=None)
        if t is None:
            break
        chon[t] -= 1
    return chon


def chon_mau(tuyen_bo, chia_tap, ty_le=TY_LE, seed=SEED):
    """(theo_tang, danh sách mã đã chọn sắp xếp tăng dần). theo_tang: {tầng: {"quan_the": s, "chon": k}}.

    Lỗi (ValueError): mã lặp, hoặc mẫu không thuộc tập nào."""
    ma = [b["id"] for b in tuyen_bo]
    if len(set(ma)) != len(ma):
        raise ValueError("mã tuyên bố lặp trong tệp tuyên bố")
    tang = {}
    for b in tuyen_bo:
        tang.setdefault(ten_tang(b["ma_mau"], chia_tap), []).append(b["id"])
    n = round(ty_le * len(ma))
    so_chon = chia_tieu_chuan({t: len(v) for t, v in tang.items()}, n)
    rng = random.Random(seed)
    chon = []
    theo_tang = {}
    for t in sorted(tang):
        chon += rng.sample(sorted(tang[t]), so_chon[t])
        theo_tang[t] = {"quan_the": len(tang[t]), "chon": so_chon[t]}
    return theo_tang, sorted(chon)


def tao_ket_qua(tuyen_bo, chia_tap, ty_le=TY_LE, seed=SEED):
    theo_tang, chon = chon_mau(tuyen_bo, chia_tap, ty_le, seed)
    return {
        "buoc": 26,
        "ngay": "26/11/2026",
        "seed": seed,
        "ty_le": ty_le,
        "quan_the": QUAN_THE,
        "so_quan_the": len(tuyen_bo),
        "theo_tang": theo_tang,
        "gan_lai_buoc32": chon,
        "nguoi_thu_hai": [],
        "ghi_chu_nguoi_thu_hai": GHI_CHU_NGUOI_THU_HAI,
        "quy_tac": QUY_TAC,
    }


def ghi_ket_qua(duong, ket_qua):
    duong = Path(duong)
    duong.parent.mkdir(parents=True, exist_ok=True)
    duong.write_text(json.dumps(ket_qua, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Chọn mẫu phân tầng để tự gán lại mù ở Bước 32.")
    ap.add_argument("--seed", type=int, default=SEED, help=f"seed (mặc định {SEED})")
    ap.add_argument("--ty-le", type=float, default=TY_LE, help=f"tỉ lệ chọn (mặc định {TY_LE})")
    ap.add_argument("--ra", type=Path, default=TEP_RA, help="tệp kết quả (mặc định data/nhan/danh_sach_mau.json)")
    ap.add_argument("--in", dest="chi_in", action="store_true", help="chỉ in ra màn hình, không ghi tệp")
    ap.add_argument("--tuyen-bo", type=Path, default=TEP_TUYEN_BO, help="tệp tuyên bố tập chính")
    ap.add_argument("--chia-tap", type=Path, default=TEP_CHIA_TAP, help="tệp chia tập")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        ket_qua = tao_ket_qua(doc_jsonl(args.tuyen_bo), doc_json(args.chia_tap), args.ty_le, args.seed)
    except ValueError as e:
        sys.exit(str(e))
    if args.chi_in:
        print(json.dumps(ket_qua, ensure_ascii=False, indent=2))
        return
    ghi_ket_qua(args.ra, ket_qua)
    print(f"đã ghi {args.ra}: {len(ket_qua['gan_lai_buoc32'])}/{ket_qua['so_quan_the']} mã, seed {args.seed}")
    for t, v in ket_qua["theo_tang"].items():
        print(f"  {t}: {v['chon']}/{v['quan_the']}")


if __name__ == "__main__":
    main()
