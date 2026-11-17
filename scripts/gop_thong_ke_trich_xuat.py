"""Bước 22: gộp thống kê trích xuất của nhiều tệp tuyên bố thành một bảng cho cả tập phát triển (thu + chinh = 108 tuyên bố).

scripts/chay_trich_xuat.py chạy từng tệp tuyên bố và ghi <thư mục>/<stem>_<mô hình>_k<k>_<cách tách>.jsonl. Script này không gọi
LLM: đọc các tệp kết quả đó, kiểm tập id khớp từng tệp tuyên bố (thiếu, thừa hay trùng id giữa các tệp đều báo lỗi), gộp bản ghi
theo thứ tự tệp rồi sinh thống kê bằng đúng hàm tao_thong_ke của chay_trich_xuat.py. Ghi
    <thư mục>/thong_ke_<tên>_<mô hình>_k<k>_<cách tách>[_khong_neo_nguon][_khong_day_du][_gia].md
và in nội dung ra stdout. Không ghi tệp jsonl gộp.

Chạy (sau khi đã chạy chay_trich_xuat.py cho từng tệp với cùng mô hình, k, cách tách, cờ):
    .venv/Scripts/python.exe -X utf8 scripts/gop_thong_ke_trich_xuat.py --mo-hinh gemini-3.6-flash
        [--tuyen-bo data/tuyen_bo/thu.jsonl data/tuyen_bo/chinh.jsonl] [--k 5] [--cach-tach am_tiet]
        [--khong-neo-nguon --khong-kiem-day-du] [--thu-muc ket_qua/trich_xuat] [--ten phat_trien] [--gia]
"""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import chay_trich_xuat as cx  # noqa: E402  (nạp luôn đường dẫn src cho kiemchung)
from kiemchung import trich_xuat as tx, truy_hoi as th  # noqa: E402

TUYEN_BO_MAC_DINH = [ROOT / "data/tuyen_bo/thu.jsonl", ROOT / "data/tuyen_bo/chinh.jsonl"]


def ten_tuong_doi(duong):
    try:
        return Path(duong).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(duong)


def main(argv=None):
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Gộp thống kê trích xuất của nhiều tệp tuyên bố (Bước 22).")
    ap.add_argument("--tuyen-bo", type=Path, nargs="+", default=TUYEN_BO_MAC_DINH,
                    help="các tệp tuyên bố (mặc định thu.jsonl và chinh.jsonl của data/tuyen_bo)")
    ap.add_argument("--mo-hinh", required=True, help="mã mô hình đã dùng khi chạy chay_trich_xuat.py")
    ap.add_argument("--k", type=int, default=5, help="số đoạn đưa vào câu lệnh (mặc định 5)")
    ap.add_argument("--cach-tach", choices=th.CACH_TACH, default="am_tiet", help="cách tách của BM25 (mặc định am_tiet)")
    ap.add_argument("--khong-neo-nguon", action="store_true", help="kết quả chạy với --khong-neo-nguon (P−NN)")
    ap.add_argument("--khong-kiem-day-du", action="store_true", help="kết quả chạy với --khong-kiem-day-du (P−NN)")
    ap.add_argument("--thu-muc", type=Path, default=cx.THU_MUC_RA, help="thư mục kết quả (mặc định ket_qua/trich_xuat)")
    ap.add_argument("--ten", default="phat_trien", help="tên tập gộp, dùng đặt tên tệp thống kê (mặc định phat_trien)")
    ap.add_argument("--gia", action="store_true", help="gộp kết quả chạy --gia (thư mục và tệp có hậu tố _gia)")
    args = ap.parse_args(argv)

    neo_nguon, kiem_day_du = not args.khong_neo_nguon, not args.khong_kiem_day_du
    thu_muc = args.thu_muc.with_name(args.thu_muc.name + "_gia") if args.gia else args.thu_muc

    # tìm tệp kết quả trước, báo hết tệp thiếu một lượt
    tep_kq = [thu_muc / (cx.ten_ket_qua(t, args.mo_hinh, args.k, args.cach_tach, neo_nguon, kiem_day_du, args.gia) + ".jsonl")
              for t in args.tuyen_bo]
    thieu = [t for t in tep_kq if not t.exists()]
    if thieu:
        print("Thiếu tệp kết quả (chạy chay_trich_xuat.py trước):\n" + "\n".join(f"  {t}" for t in thieu), file=sys.stderr)
        return 1

    ban_ghi, tuyen_bo_goc, tom_tat, loi = [], {}, [], []
    for tep_tb, tep in zip(args.tuyen_bo, tep_kq):
        tb = cx.doc_jsonl(tep_tb)
        kq = cx.doc_jsonl(tep)
        id_tb, id_kq = {d["id"] for d in tb}, {d["id"] for d in kq}
        trung = sorted(tuyen_bo_goc.keys() & id_tb)
        if trung:
            loi.append(f"{tep_tb}: id trùng với tệp tuyên bố trước: {', '.join(trung)}")
        if id_tb - id_kq:
            loi.append(f"{tep.name}: thiếu id so với {tep_tb}: {', '.join(sorted(id_tb - id_kq))}")
        if id_kq - id_tb:
            loi.append(f"{tep.name}: thừa id so với {tep_tb}: {', '.join(sorted(id_kq - id_tb))}")
        if len(kq) != len(id_kq):
            loi.append(f"{tep.name}: có id lặp lại trong tệp kết quả")
        tuyen_bo_goc.update({d["id"]: d for d in tb})
        ban_ghi += kq
        tom_tat.append(f"{ten_tuong_doi(tep)} ({len(kq)} tuyên bố)")
    if loi:
        print("Lỗi:\n" + "\n".join(f"  {m}" for m in loi), file=sys.stderr)
        return 1

    thiet_lap = {"tep": " + ".join(ten_tuong_doi(t) for t in args.tuyen_bo), "mo_hinh": args.mo_hinh, "k": args.k,
                 "cach_tach": args.cach_tach, "neo_nguon": neo_nguon, "kiem_day_du": kiem_day_du,
                 "max_token_ra": tx.MAX_TOKEN_RA}
    dong = cx.tao_thong_ke(ban_ghi, thiet_lap, tuyen_bo_goc, args.gia)
    vi_tri = next(i for i, d in enumerate(dong) if d.startswith("# Thống kê")) + 1
    dong.insert(vi_tri, f"- Gộp từ: {', '.join(tom_tat)}.")
    ten = cx.ten_ket_qua(Path(args.ten + ".jsonl"), args.mo_hinh, args.k, args.cach_tach, neo_nguon, kiem_day_du, args.gia)
    tep_ra = thu_muc / f"thong_ke_{ten}.md"
    cx.ghi_tep(tep_ra, "\n".join(dong) + "\n")
    print("\n".join(dong))
    print(f"\nĐã ghi {tep_ra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
