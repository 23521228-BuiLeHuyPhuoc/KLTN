"""Câu lệnh chép nguyên văn đặc tả Bước 29–30."""
import json

from .chung import MAX_TOKEN_RA, ket_qua_nhan, thay_mot_luot, doc_tra_ve

CAU_LENH_B1 = """Bạn gán nhãn cho một tuyên bố quảng cáo về thông số kỹ thuật. Bạn không có văn bản gốc; bạn chỉ có bộ thông số đã trích từ tuyên bố và từ tài liệu chính hãng (JSON dưới đây, mỗi trường kèm câu trích nguyên văn ở "trich"). Theo hướng dẫn gán nhãn, gán cho tuyên bố đúng một trong bốn nhãn: "Đúng", "Sai", "Lệch điều kiện", "Chưa đủ thông tin".

HƯỚNG DẪN GÁN NHÃN
{huong_dan}

CÁCH ĐỌC BỘ THÔNG SỐ
- "dieu_kien": các điều kiện đã nhận ra, ghi bằng tên và giá trị như cột "Khóa cấu hình" ở mục 5 của hướng dẫn. Điều kiện bắt buộc không có trong "dieu_kien" là văn bản không nêu.
- Điều kiện dạng số ghi {"so": ..., "don_vi": ...}.
- "kieu_gia_tri": khong_neu (không nêu), toi_da, dien_hinh, dinh_muc, thich_ung, khang_dinh (có từ khẳng định gắn với con số); "cum_kieu" là chữ đó.
- "dieu_kien_khac": cụm điều kiện chưa có trong cấu hình, kèm loại và câu trích.
- "ngu_canh": cụm chỉ là ngữ cảnh, không làm đổi nhãn.
- "gia_tri" của kháng nước là mã IP {"bui": ..., "nuoc": ...}, số mét theo ISO 22810, "khong" (không kháng nước) hoặc "co" (có kháng nước, không nêu mã).

Trả về đúng một đối tượng JSON, không thêm chữ nào khác: {"nhan": "<một trong bốn nhãn>", "ly_do": "<lý do ngắn>"}

Bộ thông số của tuyên bố:
{bo_thong_so_tuyen_bo}
Bộ thông số trích từ tài liệu:
{bo_thong_so_tai_lieu}"""


def bo_thong_so_cho_b1(ban_ghi):
    """In hai bộ thông số, bỏ khóa nội bộ và mục tài liệu khác sản phẩm."""
    giu = {"ma_doan", "thuoc_tinh", "gia_tri", "don_vi", "dieu_kien", "kieu_gia_tri",
           "cum_kieu", "dieu_kien_khac", "ngu_canh", "trich"}

    def loc(muc):
        return {k: v for k, v in muc.items() if k in giu} if muc is not None else None

    tb = loc(ban_ghi.get("tuyen_bo"))
    tl = [loc(m) for m in ban_ghi.get("bang_chung", []) if not m.get("khac_san_pham")]
    return tuple(json.dumps(m, ensure_ascii=False, sort_keys=True, indent=1) for m in (tb, tl))


def ghep_cau_lenh(ban_ghi, huong_dan):
    """Ghép hướng dẫn và hai bộ thông số một lượt."""
    tb, tl = bo_thong_so_cho_b1(ban_ghi)
    return thay_mot_luot(CAU_LENH_B1, {"{huong_dan}": huong_dan,
                         "{bo_thong_so_tuyen_bo}": tb, "{bo_thong_so_tai_lieu}": tl})


def chay_mot(client, mo_hinh, ban_ghi, huong_dan, max_token_ra=MAX_TOKEN_RA):
    """Chạy B1 kể cả khi trích xuất thất bại; giữ lỗi đầu vào để truy lại."""
    kq = ket_qua_nhan(client, mo_hinh, ghep_cau_lenh(ban_ghi, huong_dan), max_token_ra)
    kq.update({k: ban_ghi[k] for k in ("id", "ma_mau") if k in ban_ghi})
    kq["loi_trich_xuat"] = ban_ghi.get("loi")
    tb = ban_ghi.get("tuyen_bo") or {}
    kq["trich_xuat_thieu"] = tb.get("gia_tri") is None or tb.get("thuoc_tinh") is None
    return kq
