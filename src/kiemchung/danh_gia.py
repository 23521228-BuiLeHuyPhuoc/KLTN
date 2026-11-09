"""Chỉ số đánh giá theo T6.4: FAR, Recall nhãn Đúng, bảng nhầm lẫn (làm ở Bước 15 cho B0).

Các hàm thuần, nhận nhãn đã có sẵn: chuan = {mã tuyên bố: nhãn chuẩn} và du_doan = {mã tuyên bố: nhãn dự đoán}.
Nhãn chuẩn thuộc NHAN_CHUAN; nhãn dự đoán thuộc NHAN_DU_DOAN, trong đó LOI là "không có nhãn hợp lệ" (hệ thống
không trả được nhãn đọc được). LOI không phải DUNG: tuyên bố LOI vẫn nằm trong mẫu số, không bao giờ là một lần
chấp nhận nhầm, và là một lần bỏ sót nếu nhãn chuẩn là DUNG. Số LOI được đếm riêng ở dem_loi.

loai là danh sách mã tuyên bố bị loại khỏi mọi phép tính (mẫu số, bảng nhầm lẫn, số LOI). Kiểm chặt: tập mã của
chuan và du_doan phải trùng nhau, nhãn phải hợp lệ, mã trong loai phải thuộc chuan; sai thì raise ValueError.

Các chỉ số tỷ lệ trả (số đếm tử, mẫu số) như truy_hoi.tinh_recall; nơi gọi tự chia và tự xử lý mẫu số 0. Thêm hàm
ty_le_* trả thẳng số thực (None khi mẫu số 0).

Lõi tính nhận danh sách cặp (nhãn chuẩn, nhãn dự đoán), một tuyên bố có thể xuất hiện nhiều lần (bootstrap rút có
hoàn lại); cap_nhan đổi từ hai dict (có kiểm chặt) sang danh sách cặp. Các hàm dict tinh_far, tinh_recall_dung,
bang_nham_lan, dem_loi là vỏ bọc của lõi. Nhãn LECH có thể là nhãn dự đoán (P, B1, B2); B0 chỉ ra DUNG, SAI, CHUA_DU
nên cột LECH của B0 luôn bằng 0.
"""

NHAN_CHUAN = ("DUNG", "SAI", "LECH", "CHUA_DU")
NHAN_DU_DOAN = ("DUNG", "SAI", "LECH", "CHUA_DU", "LOI")


def mau_danh_gia(chuan, du_doan, loai=()):
    """Mã các tuyên bố vào phép tính: mọi mã của chuan trừ loai, theo thứ tự của chuan."""
    if set(chuan) != set(du_doan):
        thieu = sorted(set(chuan) - set(du_doan))
        thua = sorted(set(du_doan) - set(chuan))
        raise ValueError(f"nhãn chuẩn và nhãn dự đoán không cùng tập mã (thiếu dự đoán: {thieu}; thừa dự đoán: {thua})")
    la = sorted({n for n in chuan.values() if n not in NHAN_CHUAN})
    if la:
        raise ValueError(f"nhãn chuẩn không hợp lệ: {la} (chọn {', '.join(NHAN_CHUAN)})")
    la = sorted({n for n in du_doan.values() if n not in NHAN_DU_DOAN})
    if la:
        raise ValueError(f"nhãn dự đoán không hợp lệ: {la} (chọn {', '.join(NHAN_DU_DOAN)})")
    bo = set(loai)
    la = sorted(bo - set(chuan))
    if la:
        raise ValueError(f"danh sách loại có mã không thuộc bộ thử: {la}")
    return [ma for ma in chuan if ma not in bo]


def cap_nhan(chuan, du_doan, loai=()):
    """Danh sách cặp (nhãn chuẩn, nhãn dự đoán) của mẫu tính, theo thứ tự của chuan; kiểm chặt như mau_danh_gia."""
    return [(chuan[ma], du_doan[ma]) for ma in mau_danh_gia(chuan, du_doan, loai)]


# Lõi tính trên danh sách cặp

def dem_far(cap):
    """(số chấp nhận nhầm, mẫu số) của FAR theo T6.4.

    Mẫu số là số cặp nhãn chuẩn khác DUNG; tử số là số cặp trong đó bị gán DUNG."""
    khac_dung = [(h, c) for h, c in cap if h != "DUNG"]
    return sum(1 for _, c in khac_dung if c == "DUNG"), len(khac_dung)


def dem_recall_dung(cap):
    """(số DUNG được gán DUNG, số DUNG): Recall nhãn Đúng theo T6.4."""
    dung = [(h, c) for h, c in cap if h == "DUNG"]
    return sum(1 for _, c in dung if c == "DUNG"), len(dung)


def _chia(tu, mau):
    return tu / mau if mau else None


def ty_le_far(cap):
    """FAR là số thực; None khi mẫu số 0."""
    return _chia(*dem_far(cap))


def ty_le_recall_dung(cap):
    """Recall nhãn Đúng là số thực; None khi mẫu số 0."""
    return _chia(*dem_recall_dung(cap))


def prf_tung_nhan(cap):
    """{nhãn chuẩn: {tp, fp, fn, precision, recall, f1}} cho từng nhãn của NHAN_CHUAN.

    tp: chuẩn X, đoán X. fp: chuẩn khác X, đoán X. fn: chuẩn X, đoán khác X (kể cả LOI: LOI không là nhãn nào nên
    là một fn của nhãn chuẩn). Chia cho 0 như zero_division=0 của sklearn: precision = 0 khi tp + fp = 0, recall = 0
    khi tp + fn = 0, f1 = 0 khi precision + recall = 0."""
    ket = {}
    for x in NHAN_CHUAN:
        tp = sum(1 for h, c in cap if h == x and c == x)
        fp = sum(1 for h, c in cap if h != x and c == x)
        fn = sum(1 for h, c in cap if h == x and c != x)
        pr = tp / (tp + fp) if tp + fp else 0.0
        rc = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * pr * rc / (pr + rc) if pr + rc else 0.0
        ket[x] = {"tp": tp, "fp": fp, "fn": fn, "precision": pr, "recall": rc, "f1": f1}
    return ket


def macro_f1(cap):
    """Trung bình F1 của bốn nhãn chuẩn (T6.4); nhãn không có mặt trong cap vẫn tính, F1 = 0."""
    prf = prf_tung_nhan(cap)
    return sum(prf[x]["f1"] for x in NHAN_CHUAN) / len(NHAN_CHUAN)


def bang_nham_lan_cap(cap):
    """{nhãn chuẩn: {nhãn dự đoán: số cặp}}: hàng theo NHAN_CHUAN, cột theo NHAN_DU_DOAN, ô trống ghi 0."""
    bang = {h: {c: 0 for c in NHAN_DU_DOAN} for h in NHAN_CHUAN}
    for h, c in cap:
        bang[h][c] += 1
    return bang


def dem_loi_cap(cap):
    """Số cặp có nhãn dự đoán LOI."""
    return sum(1 for _, c in cap if c == "LOI")


# Vỏ bọc theo dict {mã: nhãn}

def tinh_far(chuan, du_doan, loai=()):
    """(số chấp nhận nhầm, mẫu số) của FAR theo T6.4; xem dem_far."""
    return dem_far(cap_nhan(chuan, du_doan, loai))


def tinh_recall_dung(chuan, du_doan, loai=()):
    """(số DUNG được gán DUNG, số DUNG): Recall nhãn Đúng theo T6.4."""
    return dem_recall_dung(cap_nhan(chuan, du_doan, loai))


def bang_nham_lan(chuan, du_doan, loai=()):
    """{nhãn chuẩn: {nhãn dự đoán: số tuyên bố}}: hàng theo NHAN_CHUAN, cột theo NHAN_DU_DOAN, ô trống ghi 0."""
    return bang_nham_lan_cap(cap_nhan(chuan, du_doan, loai))


def dem_loi(chuan, du_doan, loai=()):
    """Số tuyên bố LOI trong mẫu tính (đã trừ loai)."""
    return dem_loi_cap(cap_nhan(chuan, du_doan, loai))
