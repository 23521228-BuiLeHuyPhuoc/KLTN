"""Phương pháp P đầu-cuối (Bước 28 việc 1, Bước 31; T5.5, T5.9): trích xuất (trich_xuat.py) rồi bộ quyết định A-D (quyet_dinh.py).

Ba bản, mỗi bản bỏ đúng một thành phần: P đủ cả ba; P-DK bỏ đối chiếu điều kiện (quyet_dinh doi_chieu=False); P-NN bỏ neo nguồn và
kiểm tra đầy đủ của bước trích xuất (neo_nguon=False, kiem_day_du=False, cùng tắt). Tên bản (trường "he") đọc từ cờ ghi trong bản ghi
trích xuất và từ bo_doi_chieu; P-NN cùng P-DK là bản bỏ hai thành phần, ngoài thiết kế T5.9, nên báo lỗi.
Không đọc nhãn chuẩn, không gọi LLM ở kiem_chung_ban_ghi.
"""
from . import trich_xuat as tx
from .quyet_dinh import quyet_dinh

HE_P, HE_P_DK, HE_P_NN = "P", "P-DK", "P-NN"
TRUONG_CHEP = ("mo_hinh", "k", "cach_tach", "neo_nguon", "kiem_day_du")


def ten_he(neo_nguon, kiem_day_du, bo_doi_chieu):
    """Tên bản của P theo cờ. Chỉ nhận ba tổ hợp của T5.9: không bỏ gì, bỏ đối chiếu, hoặc bỏ cả neo nguồn lẫn kiểm tra đầy đủ."""
    if neo_nguon != kiem_day_du:
        raise ValueError("neo_nguon và kiem_day_du phải cùng bật hoặc cùng tắt (P-NN tắt cả hai)")
    if not neo_nguon and bo_doi_chieu:
        raise ValueError("P-NN và P-DK không dùng cùng lúc: mỗi bản chỉ bỏ một thành phần (T5.9)")
    return HE_P_NN if not neo_nguon else HE_P_DK if bo_doi_chieu else HE_P


def kiem_chung_ban_ghi(ban_ghi, bo_doi_chieu=False, luat_chung=None):
    """Kết quả P cho một bản ghi trích xuất (trich_xuat.trich_xuat hoặc một dòng của tệp jsonl của chay_trich_xuat.py).

    Lấy cấu hình nhóm theo ma_mau, gọi quyet_dinh(doi_chieu=not bo_doi_chieu, luat_chung_cho_nhieu_gia_tri=luat_chung). Trả: id, ma_mau,
    nhan, dong_d, loai, bang_chung, trich, ly_do, ghi_chu, tai_lieu_mau_thuan, vet, he, rồi mo_hinh, k, cach_tach, neo_nguon,
    kiem_day_du chép từ bản ghi trích xuất."""
    he = ten_he(ban_ghi["neo_nguon"], ban_ghi["kiem_day_du"], bo_doi_chieu)
    cau_hinh = tx.lay_cau_hinh(tx.nhom_cua_mau(ban_ghi["ma_mau"]))
    kq = quyet_dinh(ban_ghi, cau_hinh, doi_chieu=not bo_doi_chieu, luat_chung_cho_nhieu_gia_tri=luat_chung)
    ra = {"id": ban_ghi.get("id"), "ma_mau": ban_ghi["ma_mau"]}
    for khoa in ("nhan", "dong_d", "loai", "bang_chung", "trich", "ly_do", "ghi_chu", "tai_lieu_mau_thuan", "vet"):
        ra[khoa] = kq[khoa]
    ra["he"] = he
    ra.update({khoa: ban_ghi[khoa] for khoa in TRUONG_CHEP})
    return ra


def kiem_chung(tuyen_bo, ma_mau, client, mo_hinh, k=5, cach_tach="am_tiet", bo_doi_chieu=False, bo_neo_nguon=False, **kw):
    """P đầu-cuối cho một tuyên bố: trich_xuat (neo_nguon và kiem_day_du bật trừ khi bo_neo_nguon) rồi kiem_chung_ban_ghi.

    bo_neo_nguon (P-NN) và bo_doi_chieu (P-DK) không dùng cùng lúc: ValueError. **kw chuyển cho trich_xuat (thu_muc_nguon,
    max_token_ra, nhom) trừ luat_chung, chuyển cho quyet_dinh. Trả như kiem_chung_ban_ghi."""
    if bo_neo_nguon and bo_doi_chieu:
        raise ValueError("bo_neo_nguon và bo_doi_chieu không dùng cùng lúc: mỗi bản chỉ bỏ một thành phần (T5.9)")
    luat_chung = kw.pop("luat_chung", None)
    ban_ghi = tx.trich_xuat(tuyen_bo, ma_mau, client, mo_hinh, k, cach_tach, neo_nguon=not bo_neo_nguon,
                            kiem_day_du=not bo_neo_nguon, **kw)
    return kiem_chung_ban_ghi(ban_ghi, bo_doi_chieu, luat_chung)
