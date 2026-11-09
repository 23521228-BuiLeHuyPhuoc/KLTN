"""Ghép câu lệnh và đọc phản hồi dùng chung cho B1, B2 và tách tự động."""
import hashlib
import json
import re
import unicodedata

from .b0 import MAX_TOKEN_RA, NHA_CUNG_CAP, LOI_NOI_DUNG, _doc_json, goi_json
from ..llm import LLMError, LLMResult


def thay_mot_luot(khung, gia_tri):
    """Chỉ thay các chỗ trống của khung, không thay lại chữ vừa chèn."""
    return re.sub("|".join(re.escape(k) for k in gia_tri), lambda m: gia_tri[m[0]], khung)


def doc_tra_ve(chu):
    """Đọc bốn nhãn; JSON hỏng hoặc nhãn ngoài danh sách thành LOI."""
    kq = dict(nhan="LOI", nhan_goc=None, doan=[], ly_do=None, loi=None)
    d, loi = _doc_json(chu)
    if loi or not isinstance(d, dict):
        kq["loi"] = loi or "json_khong_phai_doi_tuong"
        return kq
    nhan = d.get("nhan")
    kq.update(nhan_goc=nhan, ly_do=d.get("ly_do"), doan=d.get("doan", []))
    bang = dict(zip(("đúng", "sai", "lệch điều kiện", "chưa đủ thông tin", "dung", "lech", "chua_du"),
                    ("DUNG", "SAI", "LECH", "CHUA_DU", "DUNG", "LECH", "CHUA_DU")))
    ma = bang.get(" ".join(unicodedata.normalize("NFC", nhan).lower().split())) if isinstance(nhan, str) else None
    if ma is None:
        kq["loi"] = f"nhan_la: {nhan!r}"
    else:
        kq["nhan"] = ma
    return kq


def goi(client, mo_hinh, cau_lenh, max_token_ra=MAX_TOKEN_RA):
    """Gọi qua bộ nhớ đệm; chỉ chuyển lỗi nội dung thành bản ghi lỗi."""
    if mo_hinh not in NHA_CUNG_CAP:
        raise ValueError(f"mô hình chưa có nhà cung cấp: {mo_hinh}")
    kq = dict(mo_hinh=mo_hinh, nha_cung_cap=NHA_CUNG_CAP[mo_hinh], cau_lenh=cau_lenh,
              ma_bam_cau_lenh=hashlib.sha256(cau_lenh.encode("utf-8")).hexdigest(),
              tra_ve_tho=None, loi=None, tu_bo_nho_dem=False, tran_token=None)
    try:
        r, tran = goi_json(client, NHA_CUNG_CAP[mo_hinh], mo_hinh, [{"role": "user", "content": cau_lenh}],
                           0, max_token_ra)
    except LLMError as e:
        if e.code not in LOI_NOI_DUNG:
            raise
        kq["loi"] = f"llm_khong_tra_ve_dung: {e.code}"
        return kq
    kq.update(tra_ve_tho=r.text, mo_hinh_thuc=r.actual_model, finish_reason=r.finish_reason,
              usage=r.usage, ma_yeu_cau=r.request_hash, tu_bo_nho_dem=r.cache_hit, tran_token=tran)
    return kq


def ket_qua_nhan(client, mo_hinh, cau_lenh, max_token_ra=MAX_TOKEN_RA):
    """Bản ghi gọi LLM và nhãn đã chuẩn hóa."""
    kq = goi(client, mo_hinh, cau_lenh, max_token_ra)
    if kq["loi"] is None:
        kq.update(doc_tra_ve(kq["tra_ve_tho"]))
    else:
        kq.update(nhan="LOI", nhan_goc=None, doan=[], ly_do=None)
    return kq


def gia_transport(request, timeout_s):
    """Transport giả tất định, không gọi mạng, không dùng làm kết quả thực nghiệm."""
    chu = request["messages"][-1]["content"]
    n = int(hashlib.sha256(chu.encode("utf-8")).hexdigest(), 16) % 4
    d = {"nhan": ("Đúng", "Sai", "Lệch điều kiện", "Chưa đủ thông tin")[n],
         "doan": [], "ly_do": "LLM giả"}
    return LLMResult(json.dumps(d, ensure_ascii=False), request["provider"], request["model"], "gia-b1-b2-v1", {}, "stop")
