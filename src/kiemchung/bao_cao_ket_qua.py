"""Các bảng phụ của Bước 37 (T6.4, T6.7, T6.9): Recall@k, tách tự động, thời gian và chi phí, tỷ lệ Lệch và Sai theo chế độ sinh,
độ bao phủ, bảng bỏ nhóm D1b và mau_thuan_khop_ca_hai, F1 nhãn Lệch theo loại biến đổi.

Các hàm thuần, không đọc tệp, không gọi LLM; mỗi hàm trả danh sách dòng (dict) để scripts/danh_gia_he.py ghi CSV. Hàng (hang)
là dict của một tuyên bố trong mẫu tính, như scripts/danh_gia_he.py dựng: id, cum (ma_qc), nhom, hang, llm_sinh, che_do, loai_bien_doi;
sau gan_nhan thêm chuan (nhãn chuẩn) và du ({tên hệ: nhãn dự đoán}). Ô không có dữ liệu để None (ghi thành ô trống), không bịa số.

Quy ước tự chọn (xem docstring từng hàm): ô "chưa xác định phạm vi áp dụng" của bao_phu; trần mặc định gọi lại của từng hệ và cách tính
token ra tính tiền của chi_phi.
"""
from collections import Counter
import statistics

from . import danh_gia as dg, thong_ke as tk, tach_tuyen_bo as tach, truy_hoi as th

CHE_DO = ("ten", "ten_thong_so")


def _chia(tu, mau):
    return tu / mau if mau else None


def _khoang(hang, ham, n, seed):
    """(duoi, tren) bootstrap theo cụm của ham; (None, None) khi hang rỗng."""
    if not hang:
        return None, None
    r = tk.bootstrap_cum(hang, lambda h: h["cum"], ham, n=n, seed=seed)
    return r["duoi"], r["tren"]


# 1. Recall@k

def recall_k(hang, xep_hang, bang_chung, cach_tach, n=1000, seed=2026, loai=(), ks=th.KS):
    """Mỗi k một dòng: trung, mau_so, recall, KTC bootstrap theo cụm ma_qc (duoi, tren), n_cum.

    Tái dùng truy_hoi.tinh_recall: mẫu số là tuyên bố trong hang có bằng chứng chuẩn (danh sách khác rỗng) trừ loai.
    xep_hang: {mã tuyên bố: [mã đoạn xếp giảm dần]}; bang_chung: {mã tuyên bố: [mã đoạn]} (từ tệp nhãn, như scripts/do_recall.py)."""
    trong = set(th.mau_so_recall({h["id"]: bang_chung.get(h["id"]) or [] for h in hang}, loai))
    mau = [h for h in hang if h["id"] in trong]
    diem = th.tinh_recall({h["id"]: xep_hang[h["id"]] for h in mau}, {h["id"]: bang_chung[h["id"]] for h in mau}, ks=ks)
    dong = []
    for k in ks:
        def ham(ds, k=k):
            tr, ms = th.tinh_recall({i: xep_hang[h["id"]] for i, h in enumerate(ds)},
                                    {i: bang_chung[h["id"]] for i, h in enumerate(ds)}, ks=(k,))[k]
            return _chia(tr, ms)
        tr, ms = diem[k]
        duoi, tren = _khoang(mau, ham, n, seed)
        dong.append({"cach_tach": cach_tach, "k": k, "trung": tr, "mau_so": ms, "recall": _chia(tr, ms), "duoi": duoi,
                     "tren": tren, "n_cum": len({h["cum"] for h in mau}), "n_bootstrap": n, "seed": seed})
    return dong


# 2. Tách tự động

def them_nhom(ds, mau_san_pham):
    """Bản sao ds, thêm nhom theo ma_mau (mau_san_pham: {ma_mau: dòng có nhom}) cho dòng chưa có."""
    return [d if d.get("nhom") else {**d, "nhom": mau_san_pham[d["ma_mau"]]["nhom"]} for d in ds]


def tach_tu_dong(tu_dong, tach_tay):
    """Precision, Recall của tách tự động so với tách tay: dòng chung rồi theo che_do, llm_sinh, nhom (như bao_cao của
    scripts/chay_tach_tu_dong.py; che_do luôn có đủ ten và ten_thong_so). Tái dùng tach_tuyen_bo.thong_ke."""
    dong = []

    def them(chieu, gia_tri, td, tay):
        dong.append({"phan_nhom": chieu, "gia_tri": gia_tri, **tach.thong_ke(td, tay)})
    them("chung", "tat_ca", tu_dong, tach_tay)
    for khoa in ("che_do", "llm_sinh", "nhom"):
        cac = {d.get(khoa) for d in tu_dong + tach_tay}
        if khoa == "che_do":
            cac.update(CHE_DO)
        for v in sorted(cac, key=str):
            them(khoa, "" if v is None else v, [d for d in tu_dong if d.get(khoa) == v], [d for d in tach_tay if d.get(khoa) == v])
    return dong


# 3. Thời gian và chi phí

TRAN_MAC_DINH_P = 8192   # = trich_xuat.MAX_TOKEN_RA (P, P-DK, P-NN)
TRAN_MAC_DINH_KHAC = 4096   # = doi_chung.b0.MAX_TOKEN_RA (B0, B1, B2, B3)


def tran_mac_dinh(ten_he, ghi_de=None):
    """Trần token ra mặc định của hệ: ghi_de[ten_he] nếu có, không thì 8192 cho tên bắt đầu bằng "P", 4096 cho hệ khác."""
    if ghi_de and ten_he in ghi_de:
        return ghi_de[ten_he]
    return TRAN_MAC_DINH_P if ten_he.startswith("P") else TRAN_MAC_DINH_KHAC


def token_ra_tinh_tien(r):
    """Token ra tính tiền của một bản ghi. total_tokens - input_tokens khi có cả hai (gồm token suy luận mà nhà cung cấp tính như
    đầu ra: Gemini báo output_tokens không kể suy luận, Groq đã kể trong completion_tokens, hiệu này đúng cho cả hai); không có
    total thì output_tokens, cộng reasoning_tokens khi nha_cung_cap là gemini. None khi không có usage."""
    u = r.get("usage")
    if not u:
        return None
    if u.get("total_tokens") is not None and u.get("input_tokens") is not None:
        return u["total_tokens"] - u["input_tokens"]
    if u.get("output_tokens") is None:
        return None
    return u["output_tokens"] + ((u.get("reasoning_tokens") or 0) if r.get("nha_cung_cap") == "gemini" else 0)


def chi_phi_usd(r, gia_token):
    """USD của một bản ghi theo gia_token {mô hình: {"vao": USD/1M token vào, "ra": USD/1M token ra}}; None nếu thiếu giá hoặc usage.
    Chỉ tính token của lần gọi cuối (usage ghi lần cuối); lần bị cắt trước khi gọi lại với trần gấp đôi không có trong bản ghi."""
    g = (gia_token or {}).get(r.get("mo_hinh"))
    ra = token_ra_tinh_tien(r)
    vao = (r.get("usage") or {}).get("input_tokens")
    if not g or ra is None or vao is None:
        return None
    return (vao * g["vao"] + ra * g["ra"]) / 1e6


def _tb(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def _tb_bai(theo_bai):
    """Trung bình theo bài của tổng mỗi bài; theo_bai: {ma_qc: [giá trị hoặc None]}; bài không có giá trị nào bị bỏ."""
    tong = [sum(v for v in xs if v is not None) for xs in theo_bai.values() if any(v is not None for v in xs)]
    return sum(tong) / len(tong) if tong else None


def chi_phi(ban_ghi_theo_he, cum_cua, gia_token=None, tran_ghi_de=None):
    """Mỗi hệ một dòng. ban_ghi_theo_he: {tên hệ: [bản ghi đầu ra]}; cum_cua: {mã tuyên bố: ma_qc} (bản ghi nào có ma_qc thì dùng của nó,
    bản ghi không có cả hai bị bỏ). Với P dùng bản ghi trích xuất (chay_trich_xuat.py), vì bản ghi chay_p.py không giữ usage.

    Cột: so_tuyen_bo, so_bai, token trung bình mỗi tuyên bố (input, output, reasoning, total; trung bình trên bản ghi có trường đó,
    ô trống nếu không bản ghi nào có), giay_tb / giay_trung_vi mỗi tuyên bố (từ thoi_gian_sinh_ms, chỉ B0 ghi trường này; hệ khác để
    trống), giay_tb_moi_bai và token_tb_moi_bai (cộng theo ma_qc rồi lấy trung bình các bài), so_goi_lai (tran_token lớn hơn trần mặc
    định của hệ, xem tran_mac_dinh), so_loi (loi khác rỗng hoặc nhan LOI). Có gia_token thì thêm usd_moi_tuyen_bo và usd_moi_bai (xem
    chi_phi_usd), không có hoặc thiếu giá của mô hình thì trống."""
    dong = []
    for ten, ds in ban_ghi_theo_he.items():
        ds = [{**r, "_cum": r.get("ma_qc") or cum_cua.get(r.get("id"))} for r in ds]
        ds = [r for r in ds if r["_cum"] is not None]
        tran = tran_mac_dinh(ten, tran_ghi_de)
        d = {"he": ten, "mo_hinh": ",".join(sorted({r["mo_hinh"] for r in ds if r.get("mo_hinh")})), "so_tuyen_bo": len(ds),
             "so_bai": len({r["_cum"] for r in ds}), "tran_mac_dinh": tran}
        for truong in ("input", "output", "reasoning", "total"):
            d[f"{truong}_tb"] = _tb([(r.get("usage") or {}).get(f"{truong}_tokens") for r in ds])
        giay = [r["thoi_gian_sinh_ms"] / 1000 for r in ds if r.get("thoi_gian_sinh_ms") is not None]
        d["giay_tb"] = _tb(giay)
        d["giay_trung_vi"] = statistics.median(giay) if giay else None
        theo_bai_giay, theo_bai_token, theo_bai_usd = {}, {}, {}
        for r in ds:
            g = r.get("thoi_gian_sinh_ms")
            theo_bai_giay.setdefault(r["_cum"], []).append(None if g is None else g / 1000)
            theo_bai_token.setdefault(r["_cum"], []).append((r.get("usage") or {}).get("total_tokens"))
            theo_bai_usd.setdefault(r["_cum"], []).append(chi_phi_usd(r, gia_token))
        d["giay_tb_moi_bai"] = _tb_bai(theo_bai_giay)
        d["token_tb_moi_bai"] = _tb_bai(theo_bai_token)
        d["so_goi_lai"] = sum(1 for r in ds if r.get("tran_token") is not None and r["tran_token"] > tran)
        d["so_loi"] = sum(1 for r in ds if r.get("loi") or r.get("nhan") == "LOI")
        d["usd_moi_tuyen_bo"] = _tb([chi_phi_usd(r, gia_token) for r in ds]) if gia_token else None
        d["usd_moi_bai"] = _tb_bai(theo_bai_usd) if gia_token else None
        dong.append(d)
    return dong


# 4. Tỷ lệ Lệch và Sai theo chế độ sinh

def ty_le_theo_che_do(hang, n=1000, seed=2026):
    """Trên nhãn chuẩn (hang có chuan): mỗi che_do (ten, ten_thong_so và mọi giá trị khác có mặt, rồi tat_ca) một dòng với số và tỷ lệ
    tuyên bố Lệch, Sai trên mọi tuyên bố của chế độ, kèm KTC bootstrap theo cụm. Chế độ không có tuyên bố nào: n = 0, các ô khác trống."""
    cac = sorted({h["che_do"] for h in hang if h["che_do"] is not None})
    cac = [*CHE_DO, *[c for c in cac if c not in CHE_DO]]
    dong = []
    for ten, con in [(c, [h for h in hang if h["che_do"] == c]) for c in cac] + [("tat_ca", list(hang))]:
        d = {"che_do": ten, "n": len(con)}
        for nhan, khoa in (("LECH", "lech"), ("SAI", "sai")):
            tu = sum(1 for h in con if h["chuan"] == nhan)
            d[f"so_{khoa}"], d[f"ty_le_{khoa}"] = tu, _chia(tu, len(con))
            d[f"{khoa}_duoi"], d[f"{khoa}_tren"] = _khoang(
                con, lambda ds, nhan=nhan: _chia(sum(1 for h in ds if h["chuan"] == nhan), len(ds)), n, seed)
        dong.append(d)
    return dong


# 5. Độ bao phủ

def ly_do_chua_du(r):
    """Phân loại một bản ghi P ra CHUA_DU theo dòng D và vet.nguyen_nhan (quyet_dinh.py); None nếu không phải D1a, D1b.

    "dieu_kien_la": D1a có nguyen_nhan.dieu_kien_la (điều kiện lạ của tài liệu chặn, ghi chu "chua_xac_dinh=dieu_kien_la:<cụm>").
    "chua_xac_dinh_khac": D1a loại chua_xac_dinh còn lại (cụm lạ hay xung đột ở tuyên bố, chữ gọi nhiều chế độ).
    "khong_co_mac_dinh": D1a loại mac_dinh (khóa điều kiện không có mặc định). "trich_xuat_that_bai": D1a do bước trích xuất.
    "mau_thuan_tai_lieu": D1b (tài liệu ghi hai giá trị khác nhau trong cùng điều kiện)."""
    dong = r.get("dong_d")
    if dong == "D1b":
        return "mau_thuan_tai_lieu"
    if dong != "D1a":
        return None
    nn = (r.get("vet") or {}).get("nguyen_nhan") or {}
    if nn.get("dieu_kien_la"):
        return "dieu_kien_la"
    return {"mac_dinh": "khong_co_mac_dinh", "trich_xuat_that_bai": "trich_xuat_that_bai"}.get(nn.get("loai"), "chua_xac_dinh_khac")


def bao_phu(hang, ban_ghi_p, ban_ghi_trich_xuat=None):
    """Độ bao phủ theo hãng và nhóm sản phẩm (và tat_ca). Chỉ tính tuyên bố trong hang có bản ghi P (ban_ghi_p: {id} đủ khóa dong_d, vet).

    Cột: n_tuyen_bo; n_gia_tri_bang_chung, n_co_dieu_kien_khac, ty_le_co_dieu_kien_khac (giá trị bằng chứng, tức mỗi mục có gia_tri
    trong bang_chung của bản ghi trích xuất, có dieu_kien_khac khác rỗng; trống nếu không đưa ban_ghi_trich_xuat); số và tỷ lệ
    tuyên bố ra CHUA_DU theo ly_do_chua_du: dieu_kien_la, chua_xac_dinh_khac, khong_co_mac_dinh, trich_xuat_that_bai,
    mau_thuan_tai_lieu. Quy ước tự chọn: n_chua_xac_dinh_pham_vi = dieu_kien_la + chua_xac_dinh_khac + mau_thuan_tai_lieu, vì T5.7 gọi
    "chưa xác định" là thiếu căn cứ về điều kiện hoặc phạm vi áp dụng và dừng ở D1a, còn D1b là tài liệu không cho một giá trị trong phạm vi đó."""
    p = {r["id"]: r for r in ban_ghi_p}
    tx = {r["id"]: r for r in ban_ghi_trich_xuat or []}
    cac = ["dieu_kien_la", "chua_xac_dinh_khac", "khong_co_mac_dinh", "trich_xuat_that_bai", "mau_thuan_tai_lieu"]
    mau = [h for h in hang if h["id"] in p]
    dong = []
    for chieu, gia_tri_cua in (("tat_ca", lambda h: "tat_ca"), ("hang", lambda h: h["hang"]), ("nhom", lambda h: h["nhom"])):
        for gt in sorted({gia_tri_cua(h) for h in mau}):
            con = [h for h in mau if gia_tri_cua(h) == gt]
            dem = Counter(ly_do_chua_du(p[h["id"]]) for h in con)
            d = {"chieu": chieu, "gia_tri": gt, "n_tuyen_bo": len(con)}
            if tx:
                muc = [m for h in con if h["id"] in tx for m in tx[h["id"]].get("bang_chung") or [] if m.get("gia_tri")]
                d["n_gia_tri_bang_chung"] = len(muc)
                d["n_co_dieu_kien_khac"] = sum(1 for m in muc if m.get("dieu_kien_khac"))
                d["ty_le_co_dieu_kien_khac"] = _chia(d["n_co_dieu_kien_khac"], len(muc))
            for c in cac:
                d[f"n_{c}"], d[f"ty_le_{c}"] = dem[c], _chia(dem[c], len(con))
            gop = dem["dieu_kien_la"] + dem["chua_xac_dinh_khac"] + dem["mau_thuan_tai_lieu"]
            d["n_chua_xac_dinh_pham_vi"], d["ty_le_chua_xac_dinh_pham_vi"] = gop, _chia(gop, len(con))
            dong.append(d)
    return dong


# 6. Bỏ nhóm D1b và mau_thuan_khop_ca_hai

def bang_bo_nhom(hang, he, ban_ghi_p):
    """FAR và Recall nhãn Đúng của mọi hệ khi giữ và khi bỏ D1b, mau_thuan_khop_ca_hai (T3.4, mục 11.4 của hướng dẫn).

    Hai nhóm xác định từ bản ghi của P (dong_d == D1b; ghi_chu có mau_thuan_khop_ca_hai) và bỏ theo tuyên bố: mọi hệ cùng một tập
    tuyên bố. Mỗi dòng mang so_d1b, so_mau_thuan, so_giao (cả hai) trong mẫu tính. kich_ban: giu_tat_ca, bo_D1b, bo_mau_thuan, bo_ca_hai."""
    trong = {h["id"] for h in hang}
    p = [r for r in ban_ghi_p if r["id"] in trong]
    d1b, mt = tk.ma_dong(p, "D1b"), tk.ma_co_khoa(p, "mau_thuan_khop_ca_hai")
    dem = {"so_d1b": len(d1b), "so_mau_thuan": len(mt), "so_giao": len(d1b & mt)}
    dong = []
    for ten in he:
        for kb, bo in (("giu_tat_ca", set()), ("bo_D1b", d1b), ("bo_mau_thuan", mt), ("bo_ca_hai", d1b | mt)):
            cap = [(h["chuan"], h["du"][ten]) for h in hang if h["id"] not in bo]
            ft, fm = dg.dem_far(cap)
            rt, rm = dg.dem_recall_dung(cap)
            dong.append({"he": ten, "kich_ban": kb, **dem, "so_ca_bo": len(bo), "n": len(cap), "far_tu": ft, "far_mau": fm,
                         "far": _chia(ft, fm), "recall_dung_tu": rt, "recall_dung_mau": rm, "recall_dung": _chia(rt, rm)})
    return dong


# 7. F1 nhãn Lệch theo loại biến đổi

def f1_lech_theo_loai(hang, he, n=1000, seed=2026):
    """Mỗi (hệ, loại biến đổi) và mỗi hệ cả tập (loai = "(ca_tap)") một dòng: n, số Lệch chuẩn, Precision, Recall, F1 nhãn Lệch, KTC
    bootstrap theo cụm của F1. Dùng với hang của tập cặp tối thiểu (loai_bien_doi khác None); hang không có loại thì chỉ có "(ca_tap)"."""
    loai = sorted({h["loai_bien_doi"] for h in hang if h["loai_bien_doi"]})
    dong = []
    for ten in he:
        for ten_loai, con in [("(ca_tap)", list(hang))] + [(x, [h for h in hang if h["loai_bien_doi"] == x]) for x in loai]:
            def f1(ds, ten=ten):
                return dg.prf_tung_nhan([(h["chuan"], h["du"][ten]) for h in ds])["LECH"]["f1"] if ds else None
            prf = dg.prf_tung_nhan([(h["chuan"], h["du"][ten]) for h in con])["LECH"]
            duoi, tren = _khoang(con, f1, n, seed)
            dong.append({"he": ten, "loai_bien_doi": ten_loai, "n": len(con), "n_lech_chuan": prf["tp"] + prf["fn"],
                         "precision_lech": prf["precision"], "recall_lech": prf["recall"], "f1_lech": prf["f1"],
                         "f1_lech_duoi": duoi, "f1_lech_tren": tren})
    return dong
