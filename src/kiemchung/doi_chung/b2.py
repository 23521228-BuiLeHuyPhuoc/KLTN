"""Câu lệnh chép nguyên văn đặc tả Bước 29–30."""
from .. import truy_hoi as th
from .chung import MAX_TOKEN_RA, ket_qua_nhan, thay_mot_luot, doc_tra_ve
from .huong_dan import huong_dan_cho_cau_lenh, vi_du_b2, dinh_dang_vi_du

CAU_LENH_B2 = """Bạn là người kiểm chứng tuyên bố về thông số kỹ thuật trong quảng cáo. Chỉ dựa vào các đoạn tài liệu chính hãng dưới đây và hướng dẫn gán nhãn, gán cho tuyên bố đúng một trong bốn nhãn: "Đúng", "Sai", "Lệch điều kiện", "Chưa đủ thông tin".

HƯỚNG DẪN GÁN NHÃN
{huong_dan}

VÍ DỤ
{vi_du}

Trả về đúng một đối tượng JSON, không thêm chữ nào khác: {"nhan": "<một trong bốn nhãn>", "doan": ["<mã đoạn làm bằng chứng>"], "ly_do": "<lý do ngắn, có câu trích nguyên văn của tài liệu>"}

Tuyên bố: {tuyen_bo}
Tài liệu:
{doan_1..k}"""


def ghep_cau_lenh(tuyen_bo, doan, huong_dan, vi_du):
    """Ghép một lượt, đoạn được giữ nguyên thứ tự truy hồi."""
    if not doan:
        raise ValueError("không có đoạn nào để đưa vào câu lệnh")
    return thay_mot_luot(CAU_LENH_B2, {"{huong_dan}": huong_dan, "{vi_du}": vi_du,
                         "{tuyen_bo}": tuyen_bo,
                         "{doan_1..k}": "\n\n".join(f"[{ma}] {chu}" for ma, chu in doan)})


def chay_mot(client, mo_hinh, tuyen_bo, ma_mau, k=5, cach_tach="am_tiet",
             huong_dan=None, vi_du=None, thu_muc_nguon=th.THU_MUC_NGUON, max_token_ra=MAX_TOKEN_RA):
    """Chạy B2 trên chữ tuyên bố và top-k đoạn của đúng mẫu."""
    if huong_dan is None:
        huong_dan = huong_dan_cho_cau_lenh()
    if vi_du is None:
        vi_du = dinh_dang_vi_du(vi_du_b2())
    doan = th.lay_doan(ma_mau, tuyen_bo, k, cach_tach, thu_muc_nguon)
    kq = ket_qua_nhan(client, mo_hinh, ghep_cau_lenh(tuyen_bo, doan, huong_dan, vi_du), max_token_ra)
    kq.update(ma_mau=ma_mau, tuyen_bo=tuyen_bo, k=k, cach_tach=cach_tach, ma_doan=[ma for ma, _ in doan])
    return kq
