"""Câu lệnh chép nguyên văn đặc tả Bước 29–30."""
import json

from ..cau_hinh import doc_mau
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
- Bộ thông số của tuyên bố có thêm "chu_tuyen_bo" (chữ của tuyên bố), "ma_mau", "ten_san_pham", "hang" của sản phẩm được quảng cáo.
- "san_pham_ma": mã mẫu của sản phẩm mà mục gọi tên; null khi mục không gọi tên sản phẩm.
- "goi_muc_cao": true khi mục dùng chữ gọi mức cao ("tối đa", "đỉnh", "cực đại") (mục 6.5 của hướng dẫn).
- "xung_dot": điều kiện mà mục ghi từ hai giá trị trở lên, nên chưa xác định được giá trị của điều kiện đó.

Trả về đúng một đối tượng JSON, không thêm chữ nào khác: {"nhan": "<một trong bốn nhãn>", "ly_do": "<lý do ngắn>"}

Bộ thông số của tuyên bố:
{bo_thong_so_tuyen_bo}
Bộ thông số trích từ tài liệu:
{bo_thong_so_tai_lieu}"""


# B1 nhận cùng thông tin mà quyet_dinh đọc từ bản ghi trích xuất (ma_doan, thuoc_tinh, gia_tri, don_vi, dieu_kien,
# dieu_kien_khac, kieu_gia_tri, cum_kieu, goi_muc_cao, xung_dot, trich, san_pham_ma, ngu_canh), nhưng không nhận kết quả
# các luật của P (lan_dieu_kien, san_pham_khac, cung_thuoc_tinh...): B1 tự suy luận từ dữ liệu thô đó.
GIU = {"ma_doan", "thuoc_tinh", "gia_tri", "don_vi", "dieu_kien", "kieu_gia_tri", "cum_kieu", "goi_muc_cao",
       "dieu_kien_khac", "ngu_canh", "xung_dot", "san_pham_ma", "trich"}


def thong_tin_san_pham(ban_ghi):
    """Mã mẫu, tên sản phẩm, hãng (như BoiCanh: ban_ghi.hang hoặc mau_san_pham.csv) và chữ tuyên bố gốc."""
    ma_mau = ban_ghi.get("ma_mau")
    dong = next((r for r in doc_mau() if r["ma_mau"] == ma_mau), {})
    return {"ma_mau": ma_mau, "ten_san_pham": dong.get("ten"), "hang": ban_ghi.get("hang") or dong.get("hang"),
            "chu_tuyen_bo": ban_ghi.get("chu_tuyen_bo")}


def bo_thong_so_cho_b1(ban_ghi):
    """In hai bộ thông số. Mục tài liệu khac_san_pham bị bỏ vì P đã lọc ở khâu trích xuất (neo nguồn), trước quyet_dinh.
    Cờ san_pham_khac của tuyên bố do quyet_dinh tính nên không truyền; B1 nhận chu_tuyen_bo, ma_mau, ten_san_pham,
    hang và san_pham_ma của tuyên bố để tự phán đoán."""
    def loc(muc):
        return {k: v for k, v in muc.items() if k in GIU} if muc is not None else None

    tb = loc(ban_ghi.get("tuyen_bo"))
    if tb is not None:
        tb = {**thong_tin_san_pham(ban_ghi), **tb}
    tl = [loc(m) for m in ban_ghi.get("bang_chung", []) if not m.get("khac_san_pham")]
    return tuple(json.dumps(m, ensure_ascii=False, sort_keys=True, indent=1) for m in (tb, tl))


def ghep_cau_lenh(ban_ghi, huong_dan):
    """Ghép hướng dẫn và hai bộ thông số một lượt."""
    tb, tl = bo_thong_so_cho_b1(ban_ghi)
    return thay_mot_luot(CAU_LENH_B1, {"{huong_dan}": huong_dan,
                         "{bo_thong_so_tuyen_bo}": tb, "{bo_thong_so_tai_lieu}": tl})


def chay_mot(client, mo_hinh, ban_ghi, huong_dan, max_token_ra=MAX_TOKEN_RA):
    """Chạy B1 kể cả khi trích xuất thất bại; giữ lỗi đầu vào để truy lại.
    Bản ghi trích xuất có loi (lỗi kỹ thuật LLM của P) thì trả LOI ngay, không gọi LLM, giống P (T-06)."""
    if ban_ghi.get("loi"):
        kq = dict(mo_hinh=mo_hinh, nhan="LOI", nhan_goc=None, doan=[], ly_do=None,
                  loi=f"trich_xuat_loi: {ban_ghi['loi']}", tu_bo_nho_dem=False, tran_token=None)
        kq.update({k: ban_ghi[k] for k in ("id", "ma_mau") if k in ban_ghi})
        kq["loi_trich_xuat"] = ban_ghi["loi"]
        kq["trich_xuat_thieu"] = True
        return kq
    kq = ket_qua_nhan(client, mo_hinh, ghep_cau_lenh(ban_ghi, huong_dan), max_token_ra)
    kq.update({k: ban_ghi[k] for k in ("id", "ma_mau") if k in ban_ghi})
    kq["loi_trich_xuat"] = ban_ghi.get("loi")
    tb = ban_ghi.get("tuyen_bo") or {}
    kq["trich_xuat_thieu"] = tb.get("gia_tri") is None or tb.get("thuoc_tinh") is None
    return kq
