"""Bước 37: tính chỉ số, khoảng tin cậy, kiểm định cho các hệ (T6.4, T6.5, T6.6, T6.7), ghi CSV.

Đọc nhãn chuẩn (--nhan), tuyên bố (--tuyen-bo) và dự đoán của từng hệ (--he TEN=duong_dan.jsonl, mỗi dòng có id và nhan;
nhãn không đọc được thành LOI). Không gọi LLM. Mặc định chỉ lấy tuyên bố thường (bỏ mã ct-...); --cap-toi-thieu chỉ lấy
biến thể cặp tối thiểu. Cụm bootstrap là ma_qc của tuyên bố; biến thể ct-<số>-<loại> lấy cụm của tuyên bố gốc tb-<số>.
Mọi hệ phải có dự đoán cho mọi tuyên bố trong mẫu, thiếu thì báo lỗi. Tên hệ chuẩn hóa: dấu gạch nối kiểu "−" hay "–"
thành "-", "ĐK" thành "DK" (P−ĐK -> P-DK, P−NN -> P-NN). Ghi trong --ra:
    bang_chinh.csv   mỗi hệ một dòng: FAR, Recall Đúng, P/R/F1 từng nhãn, Macro-F1 (kèm KTC bootstrap), số LOI
    mcnemar.csv      hệ chính so với từng hệ còn lại; Holm tính trên họ đối chứng B* (cột trong_ho_holm)
    gia_thuyet.csv   H1, H2, H3 theo T6.6, hai mức: theo phát biểu và có ý nghĩa thống kê
    nham_lan_<he>.csv   bảng nhầm lẫn từng hệ
    theo_nhom.csv    mô tả theo nhóm sản phẩm, hãng, llm_sinh, che_do (và loại biến đổi với cặp tối thiểu), không CI
    do_nhay.csv      phân tích độ nhạy: đổi nhãn mặc định, ngoai_bang, bỏ D1b, bỏ mau_thuan_khop_ca_hai
Chạy:
    .venv/Scripts/python.exe -X utf8 scripts/danh_gia_he.py --nhan data/nhan/<tệp>.jsonl --tuyen-bo data/tuyen_bo/<tệp>.jsonl
        --he B0=... --he P=... --tap kiem_tra --ra ket_qua/kiem_tra/bang
"""
import argparse
import csv
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kiemchung import danh_gia as dg, thong_ke as tk  # noqa: E402

TEP_CHIA_TAP = ROOT / "data/chia_tap.json"
TEP_MAU_SAN_PHAM = ROOT / "data/mau_san_pham.csv"
MA_CT = re.compile(r"^ct-(\d+)-(.+)$")
NGUONG_KEM_HON = -0.05  # H1: cận dưới KTC của hiệu Recall Đúng phải lớn hơn mức này
MUC_Y_NGHIA = 0.05
GHI_CHU_CHEP_NHAN = "số tuyên bố có chep_nhan; cần tính lại tay theo QĐ15, không tự đổi nhãn"


def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(dong) for dong in f if dong.strip()]


def chuan_hoa_ten(ten):
    """Tên hệ chuẩn: các dấu gạch nối Unicode thành "-", Đ thành D, bỏ khoảng trắng."""
    ten = ten.strip()
    for gach in "−–—‐‑":
        ten = ten.replace(gach, "-")
    return ten.replace("Đ", "D").replace("đ", "d")


def doc_he(cac_he):
    """['TEN=duong_dan', ...] -> {tên chuẩn: {mã: nhãn dự đoán}}; thiếu nhãn hoặc nhãn lỗi thành LOI."""
    ket = {}
    for muc in cac_he:
        ten, dau, duong = muc.partition("=")
        if not dau or not ten.strip() or not duong.strip():
            raise ValueError(f"--he phải có dạng TEN=duong_dan.jsonl, nhận được: {muc!r}")
        ten = chuan_hoa_ten(ten)
        if ten in ket:
            raise ValueError(f"hệ {ten} khai báo hai lần")
        du_doan = {}
        for r in doc_jsonl(duong.strip()):
            if r["id"] in du_doan:
                raise ValueError(f"hệ {ten}: mã {r['id']} xuất hiện hai lần")
            nhan = r.get("nhan")
            if nhan is None or nhan == "":
                nhan = "LOI"
            if nhan not in dg.NHAN_DU_DOAN:
                raise ValueError(f"hệ {ten}: nhãn không hợp lệ {nhan!r} ở {r['id']} (chọn {', '.join(dg.NHAN_DU_DOAN)})")
            du_doan[r["id"]] = nhan
        ket[ten] = du_doan
    return ket


def doc_mau_san_pham(duong):
    with open(duong, encoding="utf-8-sig", newline="") as f:
        return {r["ma_mau"]: r for r in csv.DictReader(f)}


def chon_mau(tuyen_bo, tap, cap_toi_thieu, mau_san_pham, chia_tap):
    """Danh sách hàng {id, cum, ma_mau, nhom, hang, llm_sinh, che_do, loai_bien_doi} của mẫu tính, theo thứ tự tệp tuyên bố."""
    theo_id = {}
    for tb in tuyen_bo:
        if tb["id"] in theo_id:
            raise ValueError(f"tuyên bố {tb['id']} xuất hiện hai lần")
        theo_id[tb["id"]] = tb
    ma_tap = None
    if tap:
        if tap not in chia_tap or "mau" not in chia_tap[tap]:
            raise ValueError(f"data/chia_tap.json không có danh sách mẫu của tập {tap!r}")
        ma_tap = set(chia_tap[tap]["mau"])
    hang = []
    for tb in tuyen_bo:
        khop = MA_CT.match(tb["id"])
        if bool(khop) != bool(cap_toi_thieu):
            continue
        goc = tb
        if khop:
            goc = theo_id.get(f"tb-{khop.group(1)}")
            if goc is None:
                raise ValueError(f"biến thể {tb['id']}: không có tuyên bố gốc tb-{khop.group(1)} trong tệp tuyên bố")
        ma_mau = tb.get("ma_mau") or goc["ma_mau"]
        if ma_tap is not None and ma_mau not in ma_tap:
            continue
        if ma_mau not in mau_san_pham:
            raise ValueError(f"mã mẫu {ma_mau} (tuyên bố {tb['id']}) không có trong data/mau_san_pham.csv")
        sp = mau_san_pham[ma_mau]
        hang.append({"id": tb["id"], "cum": goc["ma_qc"], "ma_mau": ma_mau, "nhom": sp["nhom"], "hang": sp["hang"],
                     "llm_sinh": tb.get("llm_sinh") or goc.get("llm_sinh"),
                     "che_do": tb.get("che_do") or goc.get("che_do"),
                     "loai_bien_doi": khop.group(2) if khop else None})
    if not hang:
        raise ValueError("mẫu tính rỗng (kiểm --tap, --cap-toi-thieu và tệp tuyên bố)")
    return hang


def kiem_day_du(hang, chuan, he):
    """Kiểm chặt: nhãn chuẩn cho mọi tuyên bố trong mẫu, và mọi hệ có dự đoán cho mọi tuyên bố."""
    ma = [h["id"] for h in hang]
    thieu = [m for m in ma if m not in chuan]
    if thieu:
        raise ValueError(f"thiếu nhãn chuẩn cho {len(thieu)} tuyên bố: {thieu}")
    for ten, du_doan in he.items():
        thieu = [m for m in ma if m not in du_doan]
        if thieu:
            raise ValueError(f"hệ {ten} thiếu dự đoán cho {len(thieu)} tuyên bố: {thieu}")


# Chỉ số

def lam_ham(chi_so, ten_he):
    """Hàm ds_hang -> số (hoặc None) cho bootstrap. Mỗi hàng mang chuan và du_doan: {tên hệ: nhãn}."""
    def cap(ds):
        return [(r["chuan"], r["du"][ten_he]) for r in ds]
    if chi_so == "far":
        return lambda ds: dg.ty_le_far(cap(ds))
    if chi_so == "recall_dung":
        return lambda ds: dg.ty_le_recall_dung(cap(ds))
    if chi_so == "macro_f1":
        return lambda ds: dg.macro_f1(cap(ds))
    if chi_so.startswith("f1_"):
        nhan = chi_so[3:]
        return lambda ds: dg.prf_tung_nhan(cap(ds))[nhan]["f1"]
    raise ValueError(chi_so)


def gan_nhan(hang, chuan, he):
    """Hàng mở rộng với chuan (một nhãn) và du ({tên hệ: nhãn}) để các hàm chỉ số nhận bản ghi."""
    return [{**h, "chuan": chuan[h["id"]], "du": {t: d[h["id"]] for t, d in he.items()}} for h in hang]


def lam_tron(x):
    return "" if x is None else round(x, 6)


def ghi_csv(duong, cot, dong):
    duong.parent.mkdir(parents=True, exist_ok=True)
    with open(duong, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cot)
        for d in dong:
            w.writerow([lam_tron(d.get(c)) if isinstance(d.get(c), float) or d.get(c) is None else d[c] for c in cot])


def ten_tep(ten):
    return re.sub(r"[^\w-]", "_", ten)


def bang_chinh(hang, he, n, seed):
    ket = {}
    for ten in he:
        cap = [(h["chuan"], h["du"][ten]) for h in hang]
        prf = dg.prf_tung_nhan(cap)
        d = {"he": ten, "n": len(hang), "so_loi": dg.dem_loi_cap(cap)}
        tu, mau = dg.dem_far(cap)
        d.update(far_tu=tu, far_mau=mau)
        tu, mau = dg.dem_recall_dung(cap)
        d.update(recall_dung_tu=tu, recall_dung_mau=mau)
        chi_so = [("far", "far"), ("recall_dung", "recall_dung"), ("macro_f1", "macro_f1")] + \
                 [(f"f1_{x}", f"f1_{x}") for x in dg.NHAN_CHUAN]
        for khoa, chi in chi_so:
            r = tk.bootstrap_cum(hang, lambda h: h["cum"], lam_ham(chi, ten), n=n, seed=seed)
            d[f"{khoa}_diem"], d[f"{khoa}_duoi"], d[f"{khoa}_tren"] = r["diem"], r["duoi"], r["tren"]
            d[f"{khoa}_so_vong_bo"] = r["so_vong_bo"]
        for x in dg.NHAN_CHUAN:
            d[f"p_{x}"], d[f"r_{x}"], d[f"f1_{x}"] = prf[x]["precision"], prf[x]["recall"], prf[x]["f1"]
        d["n_bootstrap"], d["seed"] = n, seed
        ket[ten] = d
    return ket


COT_CHINH = (["he", "n", "far_tu", "far_mau", "far_diem", "far_duoi", "far_tren",
              "recall_dung_tu", "recall_dung_mau", "recall_dung_diem", "recall_dung_duoi", "recall_dung_tren"]
             + [f"{m}_{x}" for x in dg.NHAN_CHUAN for m in ("p", "r", "f1")]
             + [f"f1_{x}_{m}" for x in dg.NHAN_CHUAN for m in ("duoi", "tren")]
             + ["macro_f1_diem", "macro_f1_duoi", "macro_f1_tren", "so_loi", "n_bootstrap", "seed"])


def tinh_mcnemar(hang, he, he_chinh):
    chuan = {h["id"]: h["chuan"] for h in hang}
    du = {t: {h["id"]: h["du"][t] for h in hang} for t in he}
    ket = {}
    for ten in he:
        if ten != he_chinh:
            ket[ten] = tk.mcnemar(chuan, du[he_chinh], du[ten])
    ho = {t: r["p"] for t, r in ket.items() if t.startswith("B")}
    p_holm = tk.holm(ho)
    for t, r in ket.items():
        r["trong_ho_holm"] = t in ho
        r["p_holm"] = p_holm.get(t)
    return ket


def tinh_gia_thuyet(hang, he, he_chinh, mc, bang, n, seed):
    """Các dòng H1, H2, H3 (hai mức mỗi giả thuyết). dat: dat, khong_dat hoặc 'thiếu hệ'."""
    def far(t):
        return bang[t]["far_diem"]

    def rec(t):
        return bang[t]["recall_dung_diem"]

    def f1l(t):
        return bang[t]["f1_LECH_diem"]

    def thap_hon(a, b):
        return a is not None and b is not None and a < b

    def hieu(chi, a, b):
        return tk.bootstrap_hieu(hang, lambda h: h["cum"], lam_ham(chi, a), lam_ham(chi, b), n=n, seed=seed)

    dong = []

    def them(gt, muc, dat, chi_tiet, thieu=()):
        dong.append({"gia_thuyet": gt, "muc": muc, "dat": dat, "chi_tiet": chi_tiet, "he_thieu": ",".join(thieu)})

    thieu_he = "thiếu hệ"
    # H1
    can = [f"B{i}" for i in range(4)]
    co = [t for t in can if t in he and t != he_chinh]
    vang = [t for t in can if t not in co]
    if he_chinh not in he or not co:
        them("H1", "theo_phat_bieu", thieu_he, f"cần {he_chinh} và ít nhất một hệ B0-B3", vang)
        them("H1", "y_nghia_thong_ke", thieu_he, f"cần {he_chinh} và ít nhất một hệ B0-B3", vang)
    else:
        tot = max(co, key=lambda t: (rec(t) if rec(t) is not None else -1.0, t))
        far_thap = all(thap_hon(far(he_chinh), far(t)) for t in co)
        recall_ok = rec(he_chinh) is not None and rec(tot) is not None and rec(he_chinh) - rec(tot) >= NGUONG_KEM_HON
        ct = "; ".join(f"FAR {t}={lam_tron(far(t))}" for t in co) + \
             f"; FAR {he_chinh}={lam_tron(far(he_chinh))}; đối chứng Recall Đúng cao nhất {tot}: " \
             f"{lam_tron(rec(tot))}, {he_chinh}: {lam_tron(rec(he_chinh))}"
        them("H1", "theo_phat_bieu", "dat" if far_thap and recall_ok else "khong_dat", ct, vang)
        h = hieu("recall_dung", he_chinh, tot)
        p_ok = all(mc[t]["p_holm"] < MUC_Y_NGHIA and mc[t]["b"] < mc[t]["c"] for t in co)
        ci_ok = h["duoi"] is not None and h["duoi"] > NGUONG_KEM_HON
        ct = "; ".join(f"p_holm {t}={lam_tron(mc[t]['p_holm'])} (b={mc[t]['b']}, c={mc[t]['c']})" for t in co) + \
             f"; hiệu Recall Đúng {he_chinh}-{tot}: {lam_tron(h['diem'])} [{lam_tron(h['duoi'])}, {lam_tron(h['tren'])}]"
        them("H1", "y_nghia_thong_ke", "dat" if p_ok and ci_ok else "khong_dat", ct, vang)
    # H2
    can = ["B1", "B2"]
    vang = [t for t in can if t not in he]
    if he_chinh not in he or vang:
        them("H2", "theo_phat_bieu", thieu_he, f"cần {he_chinh}, B1, B2", vang)
        them("H2", "y_nghia_thong_ke", thieu_he, f"cần {he_chinh}, B1, B2", vang)
    else:
        ok = all(thap_hon(f1l(t), f1l(he_chinh)) for t in can)
        them("H2", "theo_phat_bieu", "dat" if ok else "khong_dat",
             f"F1 Lệch {he_chinh}={lam_tron(f1l(he_chinh))}; " + "; ".join(f"{t}={lam_tron(f1l(t))}" for t in can))
        hs = {t: hieu("f1_LECH", he_chinh, t) for t in can}
        ok = all(h["duoi"] is not None and h["duoi"] > 0 for h in hs.values())
        them("H2", "y_nghia_thong_ke", "dat" if ok else "khong_dat",
             "; ".join(f"hiệu F1 Lệch {he_chinh}-{t}: {lam_tron(h['diem'])} [{lam_tron(h['duoi'])}, {lam_tron(h['tren'])}]"
                       for t, h in hs.items()))
    # H3
    t = "P-NN"
    if he_chinh not in he or t not in he:
        them("H3", "theo_phat_bieu", thieu_he, f"cần {he_chinh} và {t}", [x for x in (he_chinh, t) if x not in he])
        them("H3", "y_nghia_thong_ke", thieu_he, f"cần {he_chinh} và {t}", [x for x in (he_chinh, t) if x not in he])
    else:
        ok = thap_hon(far(he_chinh), far(t)) and thap_hon(f1l(t), f1l(he_chinh))
        them("H3", "theo_phat_bieu", "dat" if ok else "khong_dat",
             f"FAR {he_chinh}={lam_tron(far(he_chinh))}, {t}={lam_tron(far(t))}; "
             f"F1 Lệch {he_chinh}={lam_tron(f1l(he_chinh))}, {t}={lam_tron(f1l(t))}")
        h = hieu("f1_LECH", he_chinh, t)
        p_ok = mc[t]["p"] < MUC_Y_NGHIA and mc[t]["b"] < mc[t]["c"]
        ci_ok = h["duoi"] is not None and h["duoi"] > 0
        them("H3", "y_nghia_thong_ke", "dat" if p_ok and ci_ok else "khong_dat",
             f"McNemar p={lam_tron(mc[t]['p'])} (b={mc[t]['b']}, c={mc[t]['c']}); hiệu F1 Lệch {he_chinh}-{t}: "
             f"{lam_tron(h['diem'])} [{lam_tron(h['duoi'])}, {lam_tron(h['tren'])}]")
    return dong


def chi_so_diem(cap):
    prf = dg.prf_tung_nhan(cap)
    return {"n": len(cap), "far": dg.ty_le_far(cap), "far_mau": dg.dem_far(cap)[1], "recall_dung": dg.ty_le_recall_dung(cap),
            "recall_dung_mau": dg.dem_recall_dung(cap)[1], "macro_f1": dg.macro_f1(cap), "f1_lech": prf["LECH"]["f1"]}


def theo_nhom(hang, he):
    chieu = ["nhom", "hang", "llm_sinh", "che_do"]
    if any(h["loai_bien_doi"] for h in hang):
        chieu.append("loai_bien_doi")
    dong = []
    for ten in he:
        for c in chieu:
            for gt in sorted({str(h[c]) for h in hang}):
                con = [h for h in hang if str(h[c]) == gt]
                dong.append({"he": ten, "chieu": c, "gia_tri": gt,
                             **chi_so_diem([(h["chuan"], h["du"][ten]) for h in con])})
    return dong


def do_nhay(hang, he, ban_ghi_nhan):
    ma_mau = {h["id"] for h in hang}
    nhan_tinh = [r for r in ban_ghi_nhan if r["id"] in ma_mau]
    chuan_goc = {h["id"]: h["chuan"] for h in hang}
    moi_md, so_md = tk.doi_mac_dinh(nhan_tinh)
    moi_nb, so_nb = tk.doi_ngoai_bang(nhan_tinh)
    d1b = tk.ma_dong(nhan_tinh, "D1b")
    mt = tk.ma_co_khoa(nhan_tinh, "mau_thuan_khop_ca_hai")
    kich_ban = [("goc", chuan_goc, set(), 0, 0), ("doi_mac_dinh", moi_md, set(), so_md, 0),
                ("doi_ngoai_bang", moi_nb, set(), so_nb, 0), ("bo_D1b", chuan_goc, d1b, 0, len(d1b)),
                ("bo_mau_thuan_khop_ca_hai", chuan_goc, mt, 0, len(mt)),
                ("bo_ca_hai", chuan_goc, d1b | mt, 0, len(d1b | mt))]
    dong = []
    for ten in he:
        for ten_kb, chuan, bo, so_doi, so_bo in kich_ban:
            cap = [(chuan[h["id"]], h["du"][ten]) for h in hang if h["id"] not in bo]
            dong.append({"he": ten, "kich_ban": ten_kb, **chi_so_diem(cap), "so_nhan_doi": so_doi, "so_ca_bo": so_bo,
                         "ghi_chu": ""})
    dong.append({"he": "(toan_bo)", "kich_ban": "chep_nhan", "n": len(tk.ma_co_khoa(nhan_tinh, "chep_nhan")),
                 "ghi_chu": GHI_CHU_CHEP_NHAN})
    return dong


COT_NHOM = ["he", "chieu", "gia_tri", "n", "far_mau", "far", "recall_dung_mau", "recall_dung", "macro_f1", "f1_lech"]
COT_NHAY = ["he", "kich_ban", "n", "far_mau", "far", "recall_dung_mau", "recall_dung", "macro_f1", "f1_lech", "so_nhan_doi",
            "so_ca_bo", "ghi_chu"]


def main(argv=None):
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Tính chỉ số, KTC bootstrap, McNemar, Holm cho các hệ (Bước 37).")
    ap.add_argument("--nhan", type=Path, required=True, help="tệp jsonl nhãn chuẩn (id, nhan, ghi_chu, dong_d)")
    ap.add_argument("--tuyen-bo", type=Path, required=True, help="tệp jsonl tuyên bố (id, ma_qc, ma_mau, llm_sinh, che_do)")
    ap.add_argument("--he", action="append", required=True, metavar="TEN=DUONG_DAN", help="một hệ; lặp lại để thêm hệ")
    ap.add_argument("--tap", choices=("phat_trien", "kiem_tra"), help="lọc theo data/chia_tap.json (mặc định: không lọc)")
    ap.add_argument("--he-chinh", default="P", help="hệ so với các hệ còn lại (mặc định P)")
    ap.add_argument("--cap-toi-thieu", action="store_true", help="chỉ lấy biến thể ct-...; mặc định chỉ lấy tuyên bố thường")
    ap.add_argument("--ra", type=Path, required=True, help="thư mục ghi CSV")
    ap.add_argument("--n-bootstrap", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--chia-tap", type=Path, default=TEP_CHIA_TAP)
    ap.add_argument("--mau-san-pham", type=Path, default=TEP_MAU_SAN_PHAM)
    args = ap.parse_args(argv)
    if args.n_bootstrap < 1:
        ap.error("--n-bootstrap phải dương")
    try:
        he_chinh = chuan_hoa_ten(args.he_chinh)
        he = doc_he(args.he)
        if he_chinh not in he:
            raise ValueError(f"--he-chinh {he_chinh} không có trong các hệ đã khai báo: {sorted(he)}")
        ban_ghi_nhan = doc_jsonl(args.nhan)
        chuan = {}
        for r in ban_ghi_nhan:
            if r["id"] in chuan:
                raise ValueError(f"nhãn chuẩn: mã {r['id']} xuất hiện hai lần")
            chuan[r["id"]] = r["nhan"]
        with open(args.chia_tap, encoding="utf-8-sig") as f:
            chia_tap = json.load(f)
        hang = chon_mau(doc_jsonl(args.tuyen_bo), args.tap, args.cap_toi_thieu, doc_mau_san_pham(args.mau_san_pham), chia_tap)
        kiem_day_du(hang, chuan, he)
        sai = sorted({chuan[h["id"]] for h in hang} - set(dg.NHAN_CHUAN))
        if sai:
            raise ValueError(f"nhãn chuẩn không hợp lệ: {sai}")
    except ValueError as e:
        ap.error(str(e))

    hang = gan_nhan(hang, chuan, he)
    bang = bang_chinh(hang, he, args.n_bootstrap, args.seed)
    mc = tinh_mcnemar(hang, he, he_chinh)
    gt = tinh_gia_thuyet(hang, he, he_chinh, mc, bang, args.n_bootstrap, args.seed)

    ra = args.ra
    ghi_csv(ra / "bang_chinh.csv", COT_CHINH, [bang[t] for t in he])
    ghi_csv(ra / "mcnemar.csv", ["he_chinh", "he_doi_chung", "b", "c", "n", "p", "p_holm", "trong_ho_holm"],
            [{"he_chinh": he_chinh, "he_doi_chung": t, **r} for t, r in mc.items()])
    ghi_csv(ra / "gia_thuyet.csv", ["gia_thuyet", "muc", "dat", "chi_tiet", "he_thieu"], gt)
    for t in he:
        b = dg.bang_nham_lan_cap([(h["chuan"], h["du"][t]) for h in hang])
        ghi_csv(ra / f"nham_lan_{ten_tep(t)}.csv", ["nhan_chuan", *dg.NHAN_DU_DOAN, "tong"],
                [{"nhan_chuan": x, **b[x], "tong": sum(b[x].values())} for x in dg.NHAN_CHUAN])
    ghi_csv(ra / "theo_nhom.csv", COT_NHOM, theo_nhom(hang, he))
    ghi_csv(ra / "do_nhay.csv", COT_NHAY, do_nhay(hang, he, ban_ghi_nhan))

    print(f"Mẫu tính: {len(hang)} tuyên bố, {len({h['cum'] for h in hang})} cụm "
          f"({'cặp tối thiểu' if args.cap_toi_thieu else 'tuyên bố thường'}{', tập ' + args.tap if args.tap else ''}); "
          f"bootstrap {args.n_bootstrap} vòng, seed {args.seed}.")
    for t in he:
        d = bang[t]
        print(f"{t}: FAR {lam_tron(d['far_diem'])} [{lam_tron(d['far_duoi'])}, {lam_tron(d['far_tren'])}]; "
              f"Recall Đúng {lam_tron(d['recall_dung_diem'])}; Macro-F1 {lam_tron(d['macro_f1_diem'])}; LOI {d['so_loi']}")
    for d in gt:
        print(f"{d['gia_thuyet']} / {d['muc']}: {d['dat']}")
    print(f"Đã ghi CSV vào {ra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
