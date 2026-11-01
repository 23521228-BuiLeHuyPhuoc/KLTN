"""Chỉ số đánh giá theo T6.4: FAR, Recall nhãn Đúng, bảng nhầm lẫn (làm ở Bước 15 cho B0).

Các hàm thuần, nhận nhãn đã có sẵn: chuan = {mã tuyên bố: nhãn chuẩn} và du_doan = {mã tuyên bố: nhãn dự đoán}.
Nhãn chuẩn thuộc NHAN_CHUAN; nhãn dự đoán thuộc NHAN_DU_DOAN, trong đó LOI là "không có nhãn hợp lệ" (hệ thống
không trả được nhãn đọc được). LOI không phải DUNG: tuyên bố LOI vẫn nằm trong mẫu số, không bao giờ là một lần
chấp nhận nhầm, và là một lần bỏ sót nếu nhãn chuẩn là DUNG. Số LOI được đếm riêng ở dem_loi.

loai là danh sách mã tuyên bố bị loại khỏi mọi phép tính (mẫu số, bảng nhầm lẫn, số LOI). Kiểm chặt: tập mã của
chuan và du_doan phải trùng nhau, nhãn phải hợp lệ, mã trong loai phải thuộc chuan; sai thì raise ValueError.

Các chỉ số tỷ lệ trả (số đếm tử, mẫu số) như truy_hoi.tinh_recall; nơi gọi tự chia và tự xử lý mẫu số 0.
"""

NHAN_CHUAN = ("DUNG", "SAI", "LECH", "CHUA_DU")
NHAN_DU_DOAN = ("DUNG", "SAI", "CHUA_DU", "LOI")


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


def tinh_far(chuan, du_doan, loai=()):
    """(số chấp nhận nhầm, mẫu số) của FAR theo T6.4.

    Mẫu số là số tuyên bố nhãn chuẩn khác DUNG; tử số là số tuyên bố trong đó bị gán DUNG."""
    khac_dung = [ma for ma in mau_danh_gia(chuan, du_doan, loai) if chuan[ma] != "DUNG"]
    return sum(1 for ma in khac_dung if du_doan[ma] == "DUNG"), len(khac_dung)


def tinh_recall_dung(chuan, du_doan, loai=()):
    """(số DUNG được gán DUNG, số DUNG): Recall nhãn Đúng theo T6.4."""
    dung = [ma for ma in mau_danh_gia(chuan, du_doan, loai) if chuan[ma] == "DUNG"]
    return sum(1 for ma in dung if du_doan[ma] == "DUNG"), len(dung)


def bang_nham_lan(chuan, du_doan, loai=()):
    """{nhãn chuẩn: {nhãn dự đoán: số tuyên bố}}: hàng theo NHAN_CHUAN, cột theo NHAN_DU_DOAN, ô trống ghi 0."""
    bang = {h: {c: 0 for c in NHAN_DU_DOAN} for h in NHAN_CHUAN}
    for ma in mau_danh_gia(chuan, du_doan, loai):
        bang[chuan[ma]][du_doan[ma]] += 1
    return bang


def dem_loi(chuan, du_doan, loai=()):
    """Số tuyên bố LOI trong mẫu tính (đã trừ loai)."""
    return sum(1 for ma in mau_danh_gia(chuan, du_doan, loai) if du_doan[ma] == "LOI")
