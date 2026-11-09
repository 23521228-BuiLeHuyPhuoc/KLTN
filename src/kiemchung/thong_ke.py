"""Thống kê của Bước 37 (T6.5, T6.6): bootstrap theo cụm, McNemar chính xác, hiệu chỉnh Holm, và các phép đổi nhãn
cho phân tích độ nhạy (đọc ghi_chu của nhãn theo T3.4).

Các hàm thuần, không đọc tệp. Bản ghi (hang) là một tuyên bố mỗi bản ghi; mọi số ngẫu nhiên đi qua random.Random(seed)
nên chạy lại cùng seed cho đúng kết quả cũ.
"""
import math
import random

CHUA_DU = "CHUA_DU"


# Bootstrap theo cụm

def _ham_cum(cum):
    """cum là hàm bản ghi -> mã cụm, hoặc dict: khóa là bản ghi["id"] nếu bản ghi là dict, không thì chính bản ghi."""
    if callable(cum):
        return cum
    return lambda r: cum[r["id"] if isinstance(r, dict) else r]


def phan_vi(da_sap, q):
    """Phân vị q (0..1) của dãy đã sắp tăng, nội suy tuyến tính (như numpy.percentile mặc định)."""
    if not da_sap:
        return None
    vi_tri = q * (len(da_sap) - 1)
    duoi = math.floor(vi_tri)
    tren = min(duoi + 1, len(da_sap) - 1)
    return da_sap[duoi] + (da_sap[tren] - da_sap[duoi]) * (vi_tri - duoi)


def bootstrap_cum(hang, cum, ham, n=1000, seed=2026, alpha=0.05):
    """KTC bootstrap phân vị, rút có hoàn lại theo cụm.

    hang: danh sách bản ghi (mỗi bản ghi một tuyên bố); cum: hàm hoặc dict cho mã cụm của bản ghi; ham(ds_hang) trả
    một số hoặc None. Mỗi vòng rút có hoàn lại đúng số cụm gốc, gom mọi bản ghi của các cụm được rút (cụm rút hai lần
    thì bản ghi lặp hai lần) rồi gọi ham. Trả dict: diem (ham trên dữ liệu gốc), duoi và tren (phân vị alpha/2 và
    1 - alpha/2 của các vòng), n, seed, so_vong_bo (số vòng ham trả None, không tính vào phân vị). Không vòng nào có
    giá trị thì duoi và tren là None."""
    lay_cum = _ham_cum(cum)
    theo_cum = {}
    for r in hang:
        theo_cum.setdefault(lay_cum(r), []).append(r)
    cac_cum = list(theo_cum.values())  # thứ tự xuất hiện đầu tiên: tất định
    rng = random.Random(seed)
    gia_tri, bo = [], 0
    for _ in range(n):
        mau = [r for i in rng.choices(range(len(cac_cum)), k=len(cac_cum)) for r in cac_cum[i]]
        v = ham(mau)
        if v is None:
            bo += 1
        else:
            gia_tri.append(v)
    gia_tri.sort()
    return {"diem": ham(list(hang)), "duoi": phan_vi(gia_tri, alpha / 2), "tren": phan_vi(gia_tri, 1 - alpha / 2),
            "n": n, "seed": seed, "so_vong_bo": bo}


def bootstrap_hieu(hang, cum, ham_a, ham_b, n=1000, seed=2026, alpha=0.05):
    """KTC bootstrap của ham_a - ham_b, cùng một mẫu cụm cho hai hệ trong mỗi vòng (cùng seed, cùng cách rút).

    Vòng nào ham_a hoặc ham_b trả None thì bỏ. Dùng cho hiệu Recall Đúng (H1: đạt khi duoi > -0.05) và hiệu F1 Lệch
    (H2, H3: đạt khi duoi > 0). Trả dict như bootstrap_cum."""
    def hieu(ds):
        a, b = ham_a(ds), ham_b(ds)
        return None if a is None or b is None else a - b
    return bootstrap_cum(hang, cum, hieu, n=n, seed=seed, alpha=alpha)


# McNemar, Holm

def mcnemar(chuan, du_a, du_b):
    """McNemar chính xác hai phía trên các tuyên bố có nhãn chuẩn khác DUNG (T6.5).

    chuan, du_a, du_b là dict {mã: nhãn}; "chấp nhận" là dự đoán DUNG. b = A chấp nhận mà B không; c = ngược lại.
    n = b + c; p = min(1, 2 * P(X <= min(b, c))) với X ~ Nhị thức(n, 1/2); n = 0 thì p = 1. Trả dict b, c, n, p."""
    thieu = sorted(ma for ma in chuan if ma not in du_a or ma not in du_b)
    if thieu:
        raise ValueError(f"thiếu dự đoán cho các mã: {thieu}")
    b = c = 0
    for ma, nhan in chuan.items():
        if nhan == "DUNG":
            continue
        a_nhan, b_nhan = du_a[ma] == "DUNG", du_b[ma] == "DUNG"
        b += a_nhan and not b_nhan
        c += b_nhan and not a_nhan
    n = b + c
    if n == 0:
        return {"b": 0, "c": 0, "n": 0, "p": 1.0}
    duoi = sum(math.comb(n, i) for i in range(min(b, c) + 1))
    return {"b": b, "c": c, "n": n, "p": min(1.0, 2 * duoi / 2 ** n)}


def holm(p_theo_ten):
    """p đã hiệu chỉnh Holm (step-down): {tên: p} -> {tên: p_holm}, giữ đơn điệu, chặn ở 1."""
    thu_tu = sorted(p_theo_ten, key=lambda ten: p_theo_ten[ten])
    m = len(thu_tu)
    ket, truoc = {}, 0.0
    for i, ten in enumerate(thu_tu):
        truoc = max(truoc, min(1.0, (m - i) * p_theo_ten[ten]))
        ket[ten] = truoc
    return {ten: ket[ten] for ten in p_theo_ten}


# Đọc ghi_chu của nhãn (T3.4) và các phép đổi độ nhạy

def doc_ghi_chu(ghi_chu):
    """{khóa: giá trị} từ ghi_chu: các mục cách nhau bằng "; ", mỗi mục khoa=gia_tri (mục không có "=" có giá trị rỗng).

    Nhận cả danh sách chuỗi mục (như p.py). Khóa lặp thì lấy mục sau cùng."""
    if isinstance(ghi_chu, str):
        muc = ghi_chu.split("; ")
    else:
        muc = list(ghi_chu or [])
    ket = {}
    for m in muc:
        m = m.strip()
        if not m:
            continue
        khoa, _, gia_tri = m.partition("=")
        ket[khoa.strip()] = gia_tri.strip()
    return ket


def khoa_mac_dinh(ghi_chu):
    """Danh sách khóa trong mac_dinh=<k1,k2,...> (rỗng nếu không có hoặc rỗng)."""
    gia_tri = doc_ghi_chu(ghi_chu).get("mac_dinh", "")
    return [k.strip() for k in gia_tri.split(",") if k.strip()]


def _doi(ban_ghi_nhan, co_doi):
    moi, so_doi = {}, 0
    for r in ban_ghi_nhan:
        nhan = r["nhan"]
        if co_doi(r) and nhan != CHUA_DU:
            nhan = CHUA_DU
            so_doi += 1
        moi[r["id"]] = nhan
    return moi, so_doi


def doi_mac_dinh(ban_ghi_nhan):
    """(nhãn mới {mã: nhãn}, số nhãn đổi): mọi nhãn có mac_dinh= khác rỗng mà khác CHUA_DU thành CHUA_DU.

    Đây là cận trên của tác động: QĐ5 ghi cả khóa không làm đổi nhãn, nên không phải mọi nhãn bị đổi đều thật sự
    phụ thuộc cách hiểu mặc định."""
    return _doi(ban_ghi_nhan, lambda r: bool(khoa_mac_dinh(r.get("ghi_chu"))))


def doi_ngoai_bang(ban_ghi_nhan):
    """Như doi_mac_dinh nhưng chỉ nhãn có khóa ngoai_bang trong mac_dinh (QĐ10)."""
    return _doi(ban_ghi_nhan, lambda r: "ngoai_bang" in khoa_mac_dinh(r.get("ghi_chu")))


def ma_co_khoa(ban_ghi_nhan, khoa):
    """Tập mã của các bản ghi có khóa này trong ghi_chu (giá trị gì cũng được), ví dụ chep_nhan, nham_vai."""
    return {r["id"] for r in ban_ghi_nhan if khoa in doc_ghi_chu(r.get("ghi_chu"))}


def ma_dong(ban_ghi_nhan, dong):
    """Tập mã của các bản ghi dừng ở dòng D này (trường dong_d), ví dụ "D1b"."""
    return {r["id"] for r in ban_ghi_nhan if r.get("dong_d") == dong}
