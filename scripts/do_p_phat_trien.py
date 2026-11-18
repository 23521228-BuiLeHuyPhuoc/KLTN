"""Bước 28: đo P, P-DK, P-NN trên tập phát triển (bộ thử thu_luot2 + chính), offline từ tra_ve_tho đã lưu.

Không gọi LLM. Chạy lại hậu xử lý (trich_xuat.xu_ly_lai) rồi bộ quyết định, so với nhãn chuẩn. Chỉ in số đếm gộp (không in nhãn theo
mã tuyên bố bộ thử, để giữ tính mù); --chi-tiet-chinh in nhãn dự đoán và nhãn chuẩn theo mã của tập chính. Chạy:
    .venv/Scripts/python.exe -X utf8 scripts/do_p_phat_trien.py [--chi-tiet-chinh]
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kiemchung import danh_gia as dg, p as pp  # noqa: E402
from kiemchung import trich_xuat as tx  # noqa: E402

TX = ROOT / "ket_qua/trich_xuat"
TAP = {"thu": (TX / "thu_openai_gpt-oss-120b_k5_am_tiet.jsonl", ROOT / "data/nhan/thu_luot2.jsonl"),
       "chinh": (TX / "chinh_openai_gpt-oss-120b_k5_am_tiet.jsonl", ROOT / "data/nhan/chinh.jsonl")}
HE = (("P", {}), ("P-DK", {"bo_doi_chieu": True}), ("P-NN", {"khong_neo": True}))


def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(d) for d in f if d.strip()]


def chay(ten_tap):
    """{tên hệ: {id: kết quả P}} và {id: nhãn chuẩn} của một tập."""
    duong, duong_nhan = TAP[ten_tap]
    goc = doc_jsonl(duong)
    chuan = {r["id"]: r["nhan"] for r in doc_jsonl(duong_nhan)}
    ket = {}
    for he, tuy in HE:
        khong_neo = tuy.get("khong_neo", False)
        ds = [tx.xu_ly_lai(b, neo_nguon=False if khong_neo else None, kiem_day_du=False if khong_neo else None) for b in goc]
        ket[he] = {b["id"]: pp.kiem_chung_ban_ghi(b, bo_doi_chieu=tuy.get("bo_doi_chieu", False)) for b in ds}
    return ket, chuan


def chi_so(kq, chuan):
    du_doan = {i: k["nhan"] for i, k in kq.items()}
    cap = dg.cap_nhan(chuan, du_doan)
    rc = dg.dem_recall_dung(cap)
    far = dg.dem_far(cap)
    prf = dg.prf_tung_nhan(cap)
    dem = {}
    for k in kq.values():
        dem[k["nhan"]] = dem.get(k["nhan"], 0) + 1
    dong = {}
    for k in kq.values():
        dong[k["dong_d"]] = dong.get(k["dong_d"], 0) + 1
    return {"dem": dem, "recall_dung": rc, "far": far, "f1_lech": prf["LECH"]["f1"], "recall_lech": (prf["LECH"]["tp"], prf["LECH"]["tp"] + prf["LECH"]["fn"]),
            "macro_f1": dg.macro_f1(cap), "d1a": dong.get("D1a", 0), "d1b": dong.get("D1b", 0), "dong": dong, "n": len(cap)}


def gop(ds):
    return {i: v for d in ds for i, v in d.items()}


def in_bang(ten, ket, chuan):
    r = chi_so(ket, chuan)
    d = r["dem"]
    print(f"{ten:<10}{r['n']:>4} | DUNG {d.get('DUNG', 0):>3} SAI {d.get('SAI', 0):>3} LECH {d.get('LECH', 0):>3} "
          f"CHUA_DU {d.get('CHUA_DU', 0):>3} LOI {d.get('LOI', 0):>2} | RecallDung {r['recall_dung'][0]}/{r['recall_dung'][1]} "
          f"FAR {r['far'][0]}/{r['far'][1]} | RecallLech {r['recall_lech'][0]}/{r['recall_lech'][1]} F1Lech {r['f1_lech']:.3f} "
          f"MacroF1 {r['macro_f1']:.4f} | D1a {r['d1a']} D1b {r['d1b']}")
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(description="Đo P, P-DK, P-NN trên tập phát triển (offline).")
    ap.add_argument("--chi-tiet-chinh", action="store_true", help="in nhãn dự đoán và chuẩn theo mã của tập chính")
    args = ap.parse_args(argv)
    kq = {t: chay(t) for t in TAP}
    for he, _ in HE:
        print(f"== {he}")
        for t in TAP:
            in_bang(t, kq[t][0][he], kq[t][1])
        in_bang("gop 108", gop(kq[t][0][he] for t in TAP), gop(kq[t][1] for t in TAP))
    if args.chi_tiet_chinh:
        ket, chuan = kq["chinh"]
        for i, k in ket["P"].items():
            print(i, chuan[i], "->", k["nhan"], k["dong_d"], k["loai"] or "", "|", "; ".join(k["ghi_chu"])[:100])
    return 0


if __name__ == "__main__":
    sys.exit(main())
