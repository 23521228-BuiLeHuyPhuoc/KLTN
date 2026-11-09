"""Đối chứng B0 (Bước 15, T6.1, T12.1): LLM đọc tuyên bố và top-k đoạn tài liệu, gán Supported, Refuted hoặc NEI.

Một tuyên bố đi qua bốn việc: truy hồi BM25 lấy top-k đoạn của đúng mẫu (truy_hoi.truy_hoi); ghép vào khung
câu lệnh T12.1 (CAU_LENH_B0, chép đúng nguyên văn kế hoạch, chỉ thay {tuyen_bo} và {doan_1..k}); gọi LLM qua
llm.LLMClient với nhiệt độ 0, JSON mode, đi qua bộ nhớ đệm; đọc JSON {"nhan", "doan", "ly_do"} và ánh xạ nhãn
theo T6.1: Supported -> DUNG, Refuted -> SAI, NEI -> CHUA_DU. B0 không bao giờ ra LECH.

Định dạng đoạn trong câu lệnh: mỗi đoạn là "[<mã đoạn>] <văn bản>", các đoạn cách nhau một dòng trống, theo hạng
BM25 giảm dần. Văn bản của đoạn là văn bản đánh chỉ mục của truy_hoi.doc_doan: noi_dung rồi các chu_thich, nối
bằng dấu xuống dòng. Mã đoạn nằm trong ngoặc vuông để LLM chép lại vào trường "doan".

Không đoán nhãn: JSON không đọc được, không phải đối tượng, thiếu "nhan" hoặc nhãn không thuộc ba nhãn trên thì
bản ghi có nhan = "LOI" và trường "loi" nói rõ lý do (nhan_goc giữ nguyên chữ LLM trả). Chỉ chấp nhận JSON trần
hoặc JSON trong một khối ```json; không đi tìm dấu ngoặc nhọn trong văn bản tự do. Phản hồi bị chặn, rỗng hoặc
cắt cụt (llm.py raise empty_blocked_or_incomplete_response) cũng thành LOI; mọi LLMError khác (mạng, quota, khóa,
mô hình không có) được ném lên cho nơi gọi dừng chạy.
"""
import hashlib
import json
import re

from .. import truy_hoi as th
from ..llm import LLMResult, LLMError

# Chép nguyên văn từ T12.1 của CHI_TIET_TUYEN_TINH_KHOA_LUAN.md (test so lại với kế hoạch). Bản cuối chốt ở Bước 33.
CAU_LENH_B0 = (
    'Bạn là người kiểm chứng thông tin. Chỉ dựa vào các đoạn tài liệu chính hãng dưới đây, cho biết tuyên bố '
    'được tài liệu ủng hộ (Supported), bị bác bỏ (Refuted) hay chưa đủ thông tin (NEI). Trả về JSON '
    '{"nhan": …, "doan": […], "ly_do": …}. Tuyên bố: {tuyen_bo}. Tài liệu: {doan_1..k}.')

# Nhà cung cấp theo mã mô hình; llm.py không tự suy ra nhà cung cấp, nơi gọi phải nêu. Hai mô hình đã dùng ở
# Bước 11–12. Mã lạ thì ValueError, không đoán nhà cung cấp.
NHA_CUNG_CAP = {"gemini-3.6-flash": "gemini", "openai/gpt-oss-120b": "groq"}
MO_HINH_MAC_DINH = tuple(NHA_CUNG_CAP)

NHIET_DO = 0  # T6.2
# Mô hình suy luận tính token suy luận vào giới hạn đầu ra (Bước 10 ghi lại 13/18 bài Gemini bị cắt ở giới hạn thấp).
MAX_TOKEN_RA = 4096

ANH_XA_NHAN = {"supported": "DUNG", "refuted": "SAI", "nei": "CHUA_DU"}  # khóa: chữ thường, đã bỏ khoảng trắng đầu cuối
LOI_NOI_DUNG = frozenset({"empty_blocked_or_incomplete_response", "json_validate_failed"})  # LLMError coi là LOI của tuyên bố, không dừng chạy
LOI_BI_CAT = frozenset({"empty_blocked_or_incomplete_response", "json_validate_failed"})  # đầu ra bị cắt: thử lại trần gấp đôi

_CHO_TRONG = re.compile(r"\{tuyen_bo\}|\{doan_1\.\.k\}")
_KHOI_MA = re.compile(r"```[ \t]*(?:json)?[ \t]*\r?\n?(.*?)```", re.S | re.I)


# Chuyển sang truy_hoi.lay_doan ở Bước 22 để P dùng chung; giữ tên cũ cho test và nơi gọi B0.
lay_doan = th.lay_doan


def ghep_cau_lenh(tuyen_bo, doan):
    """Câu lệnh T12.1 đã điền. doan: [(mã đoạn, văn bản)] theo thứ tự đưa vào (xem định dạng ở đầu tệp)."""
    if not doan:
        raise ValueError("không có đoạn nào để đưa vào câu lệnh")
    gia_tri = {"{tuyen_bo}": tuyen_bo,
               "{doan_1..k}": "\n\n".join(f"[{ma}] {van_ban}" for ma, van_ban in doan)}
    # Thay một lượt: chữ trong tuyên bố hay đoạn trông giống chỗ trống cũng không bị thay lần nữa.
    return _CHO_TRONG.sub(lambda m: gia_tri[m.group(0)], CAU_LENH_B0)


def _doc_json(van_ban):
    """(đối tượng JSON, None) hoặc (None, lý do lỗi): JSON trần hoặc nội dung khối ``` đầu tiên."""
    chu = van_ban.strip()
    ung_vien = [chu]
    khoi = _KHOI_MA.search(chu)
    if khoi:
        ung_vien.append(khoi.group(1).strip())
    loi = None
    for c in ung_vien:
        try:
            return json.loads(c), None
        except ValueError as e:
            loi = loi or str(e)
    return None, f"json_khong_doc_duoc: {loi}"


def doc_tra_ve(van_ban):
    """Đọc văn bản LLM trả về thành {nhan_goc, nhan, doan, ly_do, loi}.

    nhan là DUNG, SAI, CHUA_DU hoặc LOI (loi nêu lý do, nhan_goc là chữ LLM ghi ở "nhan" nếu có)."""
    ket_qua = {"nhan_goc": None, "nhan": "LOI", "doan": [], "ly_do": None, "loi": None}
    du_lieu, loi = _doc_json(van_ban)
    if loi:
        ket_qua["loi"] = loi
        return ket_qua
    if not isinstance(du_lieu, dict):
        ket_qua["loi"] = f"json_khong_phai_doi_tuong: {type(du_lieu).__name__}"
        return ket_qua
    doan = du_lieu.get("doan")
    ket_qua["doan"] = [str(d) for d in doan] if isinstance(doan, list) else [doan] if isinstance(doan, str) else []
    ly_do = du_lieu.get("ly_do")
    ket_qua["ly_do"] = ly_do if ly_do is None or isinstance(ly_do, str) else json.dumps(ly_do, ensure_ascii=False)
    nhan_goc = du_lieu.get("nhan")
    if not isinstance(nhan_goc, str):
        ket_qua["loi"] = "thieu_nhan" if nhan_goc is None else f"nhan_khong_phai_chuoi: {nhan_goc!r}"
        return ket_qua
    ket_qua["nhan_goc"] = nhan_goc
    nhan = ANH_XA_NHAN.get(nhan_goc.strip().casefold())
    if nhan is None:
        ket_qua["loi"] = f"nhan_la: {nhan_goc!r}"
        return ket_qua
    ket_qua["nhan"] = nhan
    return ket_qua


def goi_json(client, nha_cung_cap, mo_hinh, messages, nhiet_do, max_token_ra):
    """Gọi JSON mode, trả (kết quả, trần token đã dùng). Đầu ra bị cắt hoặc JSON hỏng thì gọi lại một lần với trần gấp đôi.

    Nếu bộ nhớ đệm đã có kết quả ở trần gấp đôi (lần chạy trước đã nâng trần) thì gọi thẳng trần đó để chạy lại tất định."""
    tran2 = 2 * max_token_ra
    co_dem = getattr(client, "has_cache", None)
    if co_dem and co_dem(nha_cung_cap, mo_hinh, messages, {"temperature": nhiet_do, "max_output_tokens": tran2},
                         json_output=True):
        return client.call(nha_cung_cap, mo_hinh, messages, {"temperature": nhiet_do, "max_output_tokens": tran2},
                           json_output=True), tran2
    try:
        return client.call(nha_cung_cap, mo_hinh, messages,
                           {"temperature": nhiet_do, "max_output_tokens": max_token_ra}, json_output=True), max_token_ra
    except LLMError as e:
        if e.code not in LOI_BI_CAT:
            raise
    return client.call(nha_cung_cap, mo_hinh, messages, {"temperature": nhiet_do, "max_output_tokens": tran2},
                       json_output=True), tran2


def kiem_chung_b0(tuyen_bo, client, mo_hinh, k=5, cach_tach="am_tiet", thu_muc_nguon=th.THU_MUC_NGUON,
                  max_token_ra=MAX_TOKEN_RA):
    """Chạy B0 cho một tuyên bố và trả bản ghi để kiểm lại.

    tuyen_bo: dict có id, ma_mau, tuyen_bo (một dòng của data/tuyen_bo/thu.jsonl); client: llm.LLMClient.
    Bản ghi: id, ma_mau, tuyen_bo; mo_hinh (đã yêu cầu), nha_cung_cap, mo_hinh_thuc (actual_model); k, cach_tach,
    ma_doan (đã đưa vào câu lệnh, theo hạng); cau_lenh và ma_bam_cau_lenh (SHA-256); tra_ve_tho (văn bản LLM trả);
    nhan_goc, nhan, doan, ly_do, loi (xem doc_tra_ve); finish_reason, usage, thoi_gian_sinh_ms; ma_yeu_cau (mã
    băm yêu cầu của llm.py, tên tệp trong bộ nhớ đệm) và tu_bo_nho_dem (lần chạy này lấy từ bộ nhớ đệm); tran_token (trần token ra đã dùng, gấp đôi
    max_token_ra nếu lần đầu bị cắt)."""
    nha_cung_cap = NHA_CUNG_CAP.get(mo_hinh)
    if nha_cung_cap is None:
        raise ValueError(f"mô hình chưa có nhà cung cấp: {mo_hinh!r} (có {', '.join(NHA_CUNG_CAP)})")
    doan = lay_doan(tuyen_bo["ma_mau"], tuyen_bo["tuyen_bo"], k, cach_tach, thu_muc_nguon)
    cau_lenh = ghep_cau_lenh(tuyen_bo["tuyen_bo"], doan)
    ban_ghi = {
        "id": tuyen_bo["id"], "ma_mau": tuyen_bo["ma_mau"], "tuyen_bo": tuyen_bo["tuyen_bo"],
        "mo_hinh": mo_hinh, "nha_cung_cap": nha_cung_cap, "mo_hinh_thuc": None,
        "k": k, "cach_tach": cach_tach, "ma_doan": [ma for ma, _ in doan],
        "ma_bam_cau_lenh": hashlib.sha256(cau_lenh.encode("utf-8")).hexdigest(), "cau_lenh": cau_lenh,
        "tra_ve_tho": None, "nhan_goc": None, "nhan": "LOI", "doan": [], "ly_do": None, "loi": None,
        "finish_reason": None, "usage": None, "thoi_gian_sinh_ms": None, "ma_yeu_cau": None, "tu_bo_nho_dem": False,
        "tran_token": None,
    }
    try:
        tra_ve, tran = goi_json(client, nha_cung_cap, mo_hinh, [{"role": "user", "content": cau_lenh}],
                                NHIET_DO, max_token_ra)
    except LLMError as e:
        if e.code not in LOI_NOI_DUNG:
            raise
        ban_ghi["loi"] = f"llm_khong_tra_ve_dung: {e.code}"
        return ban_ghi
    ban_ghi.update(
        mo_hinh_thuc=tra_ve.actual_model, tra_ve_tho=tra_ve.text, finish_reason=tra_ve.finish_reason,
        usage=tra_ve.usage, thoi_gian_sinh_ms=tra_ve.generation_ms, ma_yeu_cau=tra_ve.request_hash,
        tu_bo_nho_dem=tra_ve.cache_hit, tran_token=tran, **doc_tra_ve(tra_ve.text))
    return ban_ghi


def gia_transport(request, timeout_s):
    """LLM GIẢ cho chạy thử (--gia) và test: KHÔNG phải LLM, không gọi mạng, không là bằng chứng thực nghiệm.

    Nhãn lấy từ mã băm câu lệnh nên cùng câu lệnh luôn ra cùng kết quả; có đủ các dạng phản hồi (nhãn hoa
    thường, khối ```json, hỏng) để chạy qua đường LOI của doc_tra_ve."""
    cau_lenh = request["messages"][-1]["content"]
    h = int(hashlib.sha256(cau_lenh.encode("utf-8")).hexdigest(), 16) % 8
    ma_doan = re.findall(r"^\[([^\]\s]+#\d+)\] ", cau_lenh, re.M)[:1]
    nhan = ["Supported", "Refuted", "NEI", "nei", " SUPPORTED ", "Refuted", "NEI"][h % 7]
    noi_dung = json.dumps({"nhan": nhan, "doan": ma_doan, "ly_do": "trả lời của LLM giả"}, ensure_ascii=False)
    if h == 3:
        noi_dung = f"```json\n{noi_dung}\n```"
    if h == 7:
        noi_dung = "Đây là LLM giả, không trả JSON."
    return LLMResult(noi_dung, request["provider"], request["model"], "gia-lap-b0-v1", {}, "stop")
