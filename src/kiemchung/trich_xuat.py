"""Trích xuất có neo nguồn và kiểm tra đầy đủ của P (Bước 22, T5.1, T5.3, T12.4). Đặc tả: luan_van/buoc22_thiet_ke_trich_xuat.md.

Một tuyên bố đi qua: BM25 top-k đoạn của đúng mẫu (truy_hoi.lay_doan, cùng hàm với B0) -> (a) LLM trích bộ thông số của tuyên bố và
của mọi giá trị cùng thuộc tính trong top-k đoạn, mỗi trường kèm câu trích -> (b) neo nguồn (neo_nguon.py) -> hiểu điều kiện kiểu
đóng (mục 6: cụm của cấu hình thành điều kiện có mã, cụm lạ vào dieu_kien_khac) -> (c) kiểm tra đầy đủ (mục 7: Python dò cụm của
cấu hình trong tuyên bố và trong dòng chứa giá trị, điền điều kiện LLM bỏ sót) -> bộ thông số (mục 8; bay_truong cho dạng T5.1).

Tách hai phần để test dễ: xu_ly nhận đầu ra JSON đã đọc, đoạn và cấu hình, hoàn toàn tất định, không gọi LLM; trich_xuat ghép câu
lệnh, gọi llm.LLMClient (nhiệt độ 0, JSON mode, qua bộ nhớ đệm) rồi giao cho xu_ly. Chỉ nhận JSON trần hoặc JSON trong một khối
json có rào ba dấu huyền (dùng chung b0._doc_json). Phản hồi bị chặn, rỗng, cắt cụt thành "loi"; mọi LLMError khác ném lên.

Quy ước: cụm cấu hình so bằng cau_hinh.chuan_hoa_chu có ranh giới chữ, cụm dài khớp trước (chỉ nhường nhau trong cùng một điều
kiện, vì "Tổng thời gian" của bo_phan và "Thời gian phát" của hoat_dong cùng dùng chữ "thời gian"). Vùng dò của mục tài liệu là các
dòng của văn bản đoạn có chứa câu trích của giá trị; khoảng trắng gộp một dấu cách trước khi đọc số (chữ dọc của #038).
"""
import hashlib
import json
from pathlib import Path
import re
import unicodedata

from . import neo_nguon as nn
from . import truy_hoi as th
from .cau_hinh import NHOM, THU_MUC, chuan_hoa_chu, doc_cau_hinh, doc_mau, doc_yaml
from .chuan_hoa import (GiaTri, KieuGiaTri, _cum_cua_muc, _mau_cum, bang_nhau, don_vi_tuong_thich, quy_doi, tim_gia_tri,
                        tim_kieu_gia_tri, tim_san_pham, tim_so)
from .doi_chung.b0 import LOI_NOI_DUNG, NHA_CUNG_CAP, NHIET_DO, _doc_json, goi_json
from .llm import LLMError, LLMResult

# Chép nguyên văn khối giữa hai dấu <!-- CAU_LENH_TRICH_XUAT: ... --> của luan_van/buoc22_thiet_ke_trich_xuat.md; test so lại.
# Bản cuối chốt ở Bước 33. Sinh từ tệp đặc tả, không gõ tay. MO_TA_THUOC_TINH chép chữ bảng "Thuộc tính được giữ" của
# data/tuyen_bo/huong_dan_tach_tay.md (cột của nhóm); test so lại.
CAU_LENH_TRICH_XUAT = """Bạn trích thông số kỹ thuật từ một tuyên bố quảng cáo về {ten_nhom} và từ các đoạn tài liệu chính hãng của đúng sản phẩm đó. Chỉ chép những gì có trong văn bản. Không suy đoán, không tính toán, không dùng hiểu biết bên ngoài.

VIỆC CẦN LÀM
1. Tuyên bố: ghi sản phẩm, thuộc tính, giá trị (con số và đơn vị) và mọi cụm điều kiện gắn với con số.
2. Tài liệu: tìm MỌI giá trị của cùng thuộc tính với tuyên bố trong các đoạn, ở mọi điều kiện, kể cả giá trị ở điều kiện khác với tuyên bố và giá trị không bằng con số của tuyên bố. Mỗi giá trị là một mục. Cùng một giá trị lặp ở nhiều đoạn thì mỗi đoạn một mục. Không lấy giá trị của thuộc tính khác.
3. Mỗi trường kèm "trich": đoạn chép NGUYÊN VĂN, từng chữ, từ văn bản tương ứng (chữ của tuyên bố, hoặc đoạn tài liệu có mã ghi ở "ma_doan"). Trích của một giá trị trong tài liệu chép cả dòng chứa con số, gồm nhãn của dòng, ví dụ "Thời gian xem video: Lên đến 30 giờ". Trường không có trong văn bản thì ghi null; không có điều kiện thì ghi danh sách rỗng.

THUỘC TÍNH (chọn đúng một mã cho tuyên bố; mọi mục của tài liệu dùng cùng mã đó)
{bang_thuoc_tinh}
Tuyên bố không thuộc thuộc tính nào ở trên thì ghi "thuoc_tinh": null và "bang_chung": [].

GIÁ TRỊ
- "chu": con số chép như trong văn bản ("3.000", "4,5", "18"), hoặc mã ("IP68", "WR50"). Giá trị phủ định như "không có khả năng kháng nước" thì "chu" là "không".
- "don_vi": đơn vị chép như trong văn bản ("giờ", "tiếng", "phút", "nit", "W", "mAh", "Hz", "x", "m", "%"); dòng không ghi đơn vị thì null. Không đổi đơn vị.
- Con số chỉ là điều kiện (công suất bộ sạc, mốc phần trăm khi sạc, số phút sạc, độ sâu, thời gian ngâm, phần diện tích đo) không phải giá trị; ghi nó trong điều kiện của giá trị.
- Một dòng có hai con số chung một đơn vị, cách nhau bằng "/" (ví dụ "Đến 9 / 30 giờ"), thì ghi hai mục, mỗi mục một con số, cùng "trich" là cả dòng.
- Không cộng, trừ hay nhân để ra con số mới.

ĐIỀU KIỆN
Điều kiện là mọi cụm cho biết con số đạt được trong hoàn cảnh nào. Mỗi cụm xếp vào một trong sáu loại:
- che_do_hoat_dong: chế độ hay hoạt động (bật chống ồn, nghe nhạc, xem video trực tuyến, chế độ nguồn điện thấp, HDR, quay video)
- bo_phan: bộ phận (tai nghe, hộp sạc, tổng thời gian kèm hộp sạc)
- phu_kien: phụ kiện hay cách sạc (bộ sạc 40W trở lên, sạc không dây, cáp đi kèm)
- dieu_kien_do: điều kiện đo hay thử (sạc tới 50%, sạc 15 phút, độ sâu 6 mét, tối đa 30 phút, 25% diện tích, nước ngọt)
- phien_ban: phiên bản (GPS + Cellular, bản 256 GB)
- kieu_gia_tri: chữ chỉ kiểu của con số ("lên đến", "đến", "tối đa", "đỉnh", "điển hình", "định mức", "thích ứng", "luôn", "đảm bảo", "ít nhất", "hơn")
"cum": cụm chép nguyên văn, ngắn nhất mà vẫn đủ nghĩa ("bật chống ồn", "bộ sạc 67W trở lên"). "trich": câu hoặc dòng chứa cụm đó.
Ở tài liệu, ghi MỌI cụm điều kiện gắn với giá trị, kể cả cụm nằm trong chú thích và cụm lạ không giống ví dụ nào ở trên; không bỏ cụm nào. Cụm ở nhãn của dòng hay ở tiêu đề nhóm ngay trên dòng cũng là điều kiện của dòng đó.
Không ghi làm điều kiện: cụm khen không có nội dung đo ("cả ngày", "siêu bền", "vượt trội", "không lo hết pin"), câu rào chung của tài liệu ("kết quả thực tế có thể khác", "thử nghiệm trong phòng thí nghiệm"), chữ chỉ là tên sản phẩm.

SẢN PHẨM
- Tuyên bố có tên sản phẩm thì chép tên đó.
- Ở tài liệu, "san_pham" ghi null khi giá trị là của chính sản phẩm của trang. Chỉ ghi tên khi đoạn cho thấy giá trị thuộc một sản phẩm khác (ví dụ cột khác của bảng so sánh). Không biết chắc giá trị thuộc sản phẩm nào thì không lấy giá trị đó.

ĐẦU RA
Trả về đúng một đối tượng JSON, không thêm chữ nào khác:
{"tuyen_bo": {"san_pham": {"chu": ..., "trich": ...} hoặc null, "thuoc_tinh": ... hoặc null, "gia_tri": {"chu": ..., "don_vi": ..., "trich": ...} hoặc null, "dieu_kien": [{"loai": ..., "cum": ..., "trich": ...}]}, "bang_chung": [{"ma_doan": ..., "san_pham": {"chu": ..., "trich": ...} hoặc null, "gia_tri": {"chu": ..., "don_vi": ..., "trich": ...}, "dieu_kien": [{"loai": ..., "cum": ..., "trich": ...}]}]}

VÍ DỤ 1 (sản phẩm tự đặt)
Tuyên bố: Tai nghe B nghe nhạc lên đến 9 giờ khi tắt chống ồn
Tài liệu:
[tn-b#003] Thời gian phát nhạc
Tắt ANC: Đến 9 / 30 giờ
Bật ANC: Đến 7 / 24 giờ

[tn-b#010] Thời gian đàm thoại (tắt ANC): lên đến 6 giờ
Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ
Kết quả:
{"tuyen_bo": {"san_pham": {"chu": "Tai nghe B", "trich": "Tai nghe B"}, "thuoc_tinh": "thoi_luong_pin", "gia_tri": {"chu": "9", "don_vi": "giờ", "trich": "lên đến 9 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "nghe nhạc", "trich": "nghe nhạc"}, {"loai": "kieu_gia_tri", "cum": "lên đến", "trich": "lên đến 9 giờ"}, {"loai": "che_do_hoat_dong", "cum": "tắt chống ồn", "trich": "khi tắt chống ồn"}]}, "bang_chung": [{"ma_doan": "tn-b#003", "san_pham": null, "gia_tri": {"chu": "9", "don_vi": "giờ", "trich": "Tắt ANC: Đến 9 / 30 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "Thời gian phát nhạc", "trich": "Thời gian phát nhạc"}, {"loai": "che_do_hoat_dong", "cum": "Tắt ANC", "trich": "Tắt ANC: Đến 9 / 30 giờ"}, {"loai": "kieu_gia_tri", "cum": "Đến", "trich": "Tắt ANC: Đến 9 / 30 giờ"}]}, {"ma_doan": "tn-b#003", "san_pham": null, "gia_tri": {"chu": "30", "don_vi": "giờ", "trich": "Tắt ANC: Đến 9 / 30 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "Thời gian phát nhạc", "trich": "Thời gian phát nhạc"}, {"loai": "che_do_hoat_dong", "cum": "Tắt ANC", "trich": "Tắt ANC: Đến 9 / 30 giờ"}, {"loai": "kieu_gia_tri", "cum": "Đến", "trich": "Tắt ANC: Đến 9 / 30 giờ"}]}, {"ma_doan": "tn-b#003", "san_pham": null, "gia_tri": {"chu": "7", "don_vi": "giờ", "trich": "Bật ANC: Đến 7 / 24 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "Thời gian phát nhạc", "trich": "Thời gian phát nhạc"}, {"loai": "che_do_hoat_dong", "cum": "Bật ANC", "trich": "Bật ANC: Đến 7 / 24 giờ"}, {"loai": "kieu_gia_tri", "cum": "Đến", "trich": "Bật ANC: Đến 7 / 24 giờ"}]}, {"ma_doan": "tn-b#003", "san_pham": null, "gia_tri": {"chu": "24", "don_vi": "giờ", "trich": "Bật ANC: Đến 7 / 24 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "Thời gian phát nhạc", "trich": "Thời gian phát nhạc"}, {"loai": "che_do_hoat_dong", "cum": "Bật ANC", "trich": "Bật ANC: Đến 7 / 24 giờ"}, {"loai": "kieu_gia_tri", "cum": "Đến", "trich": "Bật ANC: Đến 7 / 24 giờ"}]}, {"ma_doan": "tn-b#010", "san_pham": null, "gia_tri": {"chu": "6", "don_vi": "giờ", "trich": "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "đàm thoại", "trich": "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ"}, {"loai": "che_do_hoat_dong", "cum": "tắt ANC", "trich": "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ"}, {"loai": "kieu_gia_tri", "cum": "lên đến", "trich": "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ"}]}, {"ma_doan": "tn-b#010", "san_pham": null, "gia_tri": {"chu": "20", "don_vi": "giờ", "trich": "Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ"}, "dieu_kien": [{"loai": "bo_phan", "cum": "Tổng thời gian đàm thoại kèm hộp sạc", "trich": "Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ"}, {"loai": "che_do_hoat_dong", "cum": "đàm thoại", "trich": "Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ"}, {"loai": "che_do_hoat_dong", "cum": "tắt ANC", "trich": "Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ"}, {"loai": "kieu_gia_tri", "cum": "lên đến", "trich": "Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ"}]}]}

VÍ DỤ 2 (sản phẩm tự đặt)
Tuyên bố: Điện thoại A sạc 50% chỉ trong 25 phút với củ sạc 45W
Tài liệu:
[dt-a#007] Sạc nhanh có dây: sạc tới 50% trong khoảng 25 phút với bộ sạc 67W trở lên
Sạc không dây: sạc tới 50% trong 60 phút
Thử nghiệm trong phòng thí nghiệm, kết quả thực tế có thể khác.
Kết quả:
{"tuyen_bo": {"san_pham": {"chu": "Điện thoại A", "trich": "Điện thoại A"}, "thuoc_tinh": "sac_nhanh", "gia_tri": {"chu": "25", "don_vi": "phút", "trich": "trong 25 phút"}, "dieu_kien": [{"loai": "dieu_kien_do", "cum": "sạc 50%", "trich": "sạc 50%"}, {"loai": "phu_kien", "cum": "củ sạc 45W", "trich": "với củ sạc 45W"}]}, "bang_chung": [{"ma_doan": "dt-a#007", "san_pham": null, "gia_tri": {"chu": "25", "don_vi": "phút", "trich": "Sạc nhanh có dây: sạc tới 50% trong khoảng 25 phút với bộ sạc 67W trở lên"}, "dieu_kien": [{"loai": "phu_kien", "cum": "Sạc nhanh có dây", "trich": "Sạc nhanh có dây: sạc tới 50% trong khoảng 25 phút với bộ sạc 67W trở lên"}, {"loai": "dieu_kien_do", "cum": "sạc tới 50%", "trich": "Sạc nhanh có dây: sạc tới 50% trong khoảng 25 phút với bộ sạc 67W trở lên"}, {"loai": "phu_kien", "cum": "bộ sạc 67W trở lên", "trich": "Sạc nhanh có dây: sạc tới 50% trong khoảng 25 phút với bộ sạc 67W trở lên"}]}, {"ma_doan": "dt-a#007", "san_pham": null, "gia_tri": {"chu": "60", "don_vi": "phút", "trich": "Sạc không dây: sạc tới 50% trong 60 phút"}, "dieu_kien": [{"loai": "phu_kien", "cum": "Sạc không dây", "trich": "Sạc không dây: sạc tới 50% trong 60 phút"}, {"loai": "dieu_kien_do", "cum": "sạc tới 50%", "trich": "Sạc không dây: sạc tới 50% trong 60 phút"}]}]}

BÂY GIỜ LÀM VỚI
Tuyên bố: {tuyen_bo}
Tài liệu:
{doan_1..k}
Kết quả:"""

MO_TA_THUOC_TINH = {
    "dien_thoai": {
        "thoi_luong_pin": "Pin dùng được bao nhiêu giờ",
        "sac_nhanh": "Sạc tới bao nhiêu % trong bao nhiêu phút",
        "cong_suat_sac": "Công suất sạc (W)",
        "do_sang": "Độ sáng màn hình (nit)",
        "tan_so_quet": "Tần số quét màn hình (Hz)",
        "zoom": "Thu phóng camera (2x, 10x...)",
        "khang_nuoc": "Chống nước, bụi (IP68, độ sâu, thời gian ngâm)",
        "dung_luong_pin": "Dung lượng pin (mAh)",
    },
    "tai_nghe": {
        "thoi_luong_pin": "Nghe nhạc, đàm thoại bao nhiêu giờ (cả khi tính hộp sạc)",
        "sac_nhanh": "Sạc vài phút nghe được bao lâu",
        "khang_nuoc": "Chống nước (IP57...)",
        "dung_luong_pin": "Dung lượng pin tai nghe hoặc hộp sạc (mAh)",
    },
    "dong_ho": {
        "thoi_luong_pin": "Pin dùng được bao nhiêu giờ",
        "sac_nhanh": "Sạc tới bao nhiêu % trong bao nhiêu phút, hoặc sạc vài phút dùng được bao lâu",
        "do_sang": "Độ sáng màn hình (nit)",
        "khang_nuoc": "Chống nước, bụi (độ sâu tính bằng mét, chuẩn ISO, mã IP)",
    },
}

TEN_NHOM = {"dien_thoai": "điện thoại", "tai_nghe": "tai nghe", "dong_ho": "đồng hồ"}
MAX_TOKEN_RA = 8192   # đầu ra dài hơn B0 (mục 3, ghi chú)
_CHO_TRONG = re.compile(r"\{ten_nhom\}|\{bang_thuoc_tinh\}|\{tuyen_bo\}|\{doan_1\.\.k\}")
KY_HIEU_SO = "<số>"

_CAU_HINH = {}


# --- Cấu hình và câu lệnh ---

def lay_cau_hinh(nhom):
    """Cấu hình của nhóm (doc_cau_hinh), đọc một lần. Không sửa dict trả về."""
    if nhom not in _CAU_HINH:
        _CAU_HINH[nhom] = doc_cau_hinh(nhom)
    return _CAU_HINH[nhom]


def tat_ca_cau_hinh():
    return [lay_cau_hinh(n) for n in NHOM]


def nhom_cua_mau(ma_mau):
    for dong in doc_mau():
        if dong["ma_mau"] == ma_mau:
            return dong["nhom"]
    raise ValueError(f"mẫu không có trong mau_san_pham.csv: {ma_mau!r}")


def bang_thuoc_tinh(nhom, cau_hinh):
    """{bang_thuoc_tinh} của câu lệnh: mỗi thuộc tính của nhóm một dòng "- <mã> (<đơn vị>): <mô tả>", theo thứ tự YAML."""
    dong = []
    for ma, tt in cau_hinh["thuoc_tinh"].items():
        if ma not in MO_TA_THUOC_TINH[nhom]:
            raise ValueError(f"thuộc tính {nhom}.{ma} chưa có mô tả trong MO_TA_THUOC_TINH")
        dong.append(f"- {ma} ({tt['don_vi']}): {MO_TA_THUOC_TINH[nhom][ma]}")
    return "\n".join(dong)


def ghep_cau_lenh(nhom, cau_hinh, tuyen_bo, doan):
    """Câu lệnh đã điền. doan: [(mã đoạn, văn bản)] theo hạng BM25; mỗi đoạn "[<mã>] <văn bản>", cách nhau một dòng trống.
    Thay một lượt: chữ trong tuyên bố hay đoạn trông giống chỗ trống không bị thay lần nữa."""
    if not doan:
        raise ValueError("không có đoạn nào để đưa vào câu lệnh")
    gia_tri = {"{ten_nhom}": TEN_NHOM[nhom], "{bang_thuoc_tinh}": bang_thuoc_tinh(nhom, cau_hinh), "{tuyen_bo}": tuyen_bo,
               "{doan_1..k}": "\n\n".join(f"[{ma}] {van_ban}" for ma, van_ban in doan)}
    return _CHO_TRONG.sub(lambda m: gia_tri[m.group(0)], CAU_LENH_TRICH_XUAT)


# --- Đọc đầu ra (mục 4) ---

def _loai(bi_loai, phia, chi_so, truong, ly_do="sai_luoc_do"):
    bi_loai.append({"phia": phia, "chi_so": chi_so, "truong": truong, "ly_do": ly_do})


def _doc_muc(muc, phia, chi_so, loai_hop_le, bi_loai):
    """Mục đã đọc lược đồ: {"san_pham", "thuoc_tinh", "gia_tri", "dieu_kien"}; trường sai kiểu bị bỏ riêng, ghi sai_luoc_do."""
    sp = muc.get("san_pham")
    if sp is not None:
        if isinstance(sp, dict) and isinstance(sp.get("chu"), str) and isinstance(sp.get("trich"), str):
            sp = {"chu": sp["chu"], "trich": sp["trich"]}
        else:
            _loai(bi_loai, phia, chi_so, "san_pham")
            sp = None
    gt = muc.get("gia_tri")
    if gt is not None:
        if (isinstance(gt, dict) and isinstance(gt.get("chu"), str) and isinstance(gt.get("trich"), str)
                and (gt.get("don_vi") is None or isinstance(gt.get("don_vi"), str))):
            gt = {"chu": gt["chu"], "don_vi": gt.get("don_vi"), "trich": gt["trich"]}
        else:
            _loai(bi_loai, phia, chi_so, "gia_tri")
            gt = None
    tt = muc.get("thuoc_tinh")
    if tt is not None and not isinstance(tt, str):
        _loai(bi_loai, phia, chi_so, "thuoc_tinh")
        tt = None
    dks = muc.get("dieu_kien", [])
    if dks is None:
        dks = []
    if not isinstance(dks, list):
        _loai(bi_loai, phia, chi_so, "dieu_kien")
        dks = []
    dieu_kien = []
    for i, dk in enumerate(dks):
        if (isinstance(dk, dict) and dk.get("loai") in loai_hop_le and isinstance(dk.get("cum"), str)
                and isinstance(dk.get("trich"), str)):
            dieu_kien.append({"i": i, "loai": dk["loai"], "cum": dk["cum"], "trich": dk["trich"]})
        else:
            _loai(bi_loai, phia, chi_so, f"dieu_kien[{i}]")
    return {"san_pham": sp, "thuoc_tinh": tt, "gia_tri": gt, "dieu_kien": dieu_kien}


def doc_luoc_do(du_lieu, loai_hop_le):
    """(mục tuyên bố, [mục tài liệu], bi_loai, lỗi). Mục tài liệu là {"chi_so", "ma_doan", "muc", "ly_do"}: muc None khi bỏ cả mục
    (không phải đối tượng, ma_doan không phải chuỗi), ly_do liệt kê lý do. Lỗi (chuỗi) khi gốc không phải đối tượng, thiếu
    "tuyen_bo" hay "bang_chung", hoặc sai kiểu; khi đó các giá trị còn lại là None/[]."""
    if not isinstance(du_lieu, dict):
        return None, [], [], f"json_khong_phai_doi_tuong: {type(du_lieu).__name__}"
    if "tuyen_bo" not in du_lieu:
        return None, [], [], "thieu_tuyen_bo"
    if "bang_chung" not in du_lieu:
        return None, [], [], "thieu_bang_chung"
    if not isinstance(du_lieu["tuyen_bo"], dict):
        return None, [], [], f"tuyen_bo_sai_kieu: {type(du_lieu['tuyen_bo']).__name__}"
    if not isinstance(du_lieu["bang_chung"], list):
        return None, [], [], f"bang_chung_sai_kieu: {type(du_lieu['bang_chung']).__name__}"
    bi_loai = []
    tuyen_bo = _doc_muc(du_lieu["tuyen_bo"], "tuyen_bo", None, loai_hop_le, bi_loai)
    muc_tl = []
    for i, m in enumerate(du_lieu["bang_chung"]):
        if not isinstance(m, dict) or not isinstance(m.get("ma_doan"), str):
            _loai(bi_loai, "tai_lieu", i, "muc")
            muc_tl.append({"chi_so": i, "ma_doan": None, "muc": None, "ly_do": ["sai_luoc_do"]})
            continue
        muc_tl.append({"chi_so": i, "ma_doan": m["ma_doan"], "muc": _doc_muc(m, "tai_lieu", i, loai_hop_le, bi_loai),
                       "ly_do": []})
    return tuyen_bo, muc_tl, bi_loai, None


# --- Dò cụm cấu hình ---

def _bo_ngoac(chu):
    """Thay ngoặc đơn bằng dấu cách (giữ nguyên độ dài chuỗi, nên chỉ số vẫn là của chuỗi gốc). Cụm cấu hình và chữ cần dò đều qua hàm này
    nên "(ngoài trời)" của YAML khớp "ngoài trời" của LLM và ngược lại (T-01 a)."""
    return re.sub(r"[()]", " ", chu)


def _chuan_cum_cau_hinh(chu):
    """Cụm cấu hình hay cụm LLM ghi, đã chuẩn hóa chữ, bỏ ngoặc, gộp khoảng trắng."""
    return chuan_hoa_chu(_bo_ngoac(chu))


def _ung_vien(cau_hinh, phia, thuoc_tinh, giu_ngoac=False):
    """[(cụm đã chuẩn hóa, tên điều kiện, khóa giá trị)] của cach_dien_dat, đã bỏ giá trị có phia khác hay chi_thuoc_tinh không
    gồm thuộc tính đang xét. Cụm bỏ ngoặc (so cụm LLM ghi, _chuan_cum_cau_hinh); giu_ngoac=True giữ ngoặc như YAML ("(HDR)"): dùng
    khi dò thẳng trong văn bản nguồn (kiểm tra đầy đủ), nơi "HDR" trơ trọi ở chỗ khác của một dòng dài không phải chế độ HDR."""
    ds = []
    for ten_dk, muc in (cau_hinh.get("cach_dien_dat") or {}).items():
        for gt, kb in (muc or {}).items():
            if not isinstance(kb, dict) or ("phia" in kb and kb["phia"] != phia):
                continue
            if "chi_thuoc_tinh" in kb and thuoc_tinh not in kb["chi_thuoc_tinh"]:
                continue
            ds += [(c, ten_dk, gt) for c in ((chuan_hoa_chu(x) if giu_ngoac else _chuan_cum_cau_hinh(x)) for x in _cum_cua_muc(kb)) if c]
    return ds


def _tim_khop(chu, ung_vien):
    """Khớp cụm cấu hình trong chu (đã chuan_hoa_chu): [(đầu, cuối, tên điều kiện, khóa giá trị, cụm)] theo vị trí. Cụm dài khớp
    trước; hai khớp chồng nhau của cùng một điều kiện thì chỉ giữ khớp dài ("xem video" trong "xem video trực tuyến")."""
    cho = [(m.start(), m.end(), ten, gt, c) for c, ten, gt in ung_vien for m in re.finditer(_mau_cum(c), chu)]
    cho.sort(key=lambda x: (x[0] - x[1], x[0]))
    chon = []
    for x in cho:
        if all(x[2] != y[2] or x[1] <= y[0] or y[1] <= x[0] for y in chon):
            chon.append(x)
    return sorted(chon)


def _khop_trong_trich(c, trich, ung_vien):
    """T-01 b: LLM hay rút gọn cụm ("phát" cho "Thời gian phát", "ANC Tắt" cho "(Tính năng ANC Tắt)"). Cụm c (đã chuẩn hóa) không khớp
    cụm cấu hình nào thì thử trong câu trích: nếu c nằm trọn trong chỗ một cụm cấu hình khớp ở câu trích thì đó là cụm cấu hình ấy.
    Trả như _tim_khop (tối đa một khớp) hoặc []."""
    t = _bo_ngoac(chuan_hoa_chu(trich))
    cho_c = [m.span() for m in re.finditer(_mau_cum(c), t)]
    if not cho_c:
        return []
    for dau, cuoi, ten, gt, cum_cfg in _tim_khop(t, ung_vien):
        if any(dau <= a and b <= cuoi for a, b in cho_c):
            return [(dau, cuoi, ten, gt, cum_cfg)]
    return []


def _la_tieu_de(cum, trich, chung):
    """T-01 d: cụm LLM ghi làm điều kiện nhưng là tiêu đề mục, tên thuộc tính hay tên bộ phận, tên tính năng ("Màn hình", "Kháng Bụi & Nước",
    "Nguồn Điện Và Thời Lượng Pin", "Sạc nhanh HyperCharge", "Gold Collection"): không đổi con số khi đổi điều kiện (HD mục 4, 6.7 ý 3) nên không
    phải điều kiện lạ. Cụm không có con số mà mọi từ hoặc thuộc dieu_kien_la.tieu_de.tu_ten_chung (tên gọi chung, chữ khen), tên tính năng
    của tu_khang_dinh.ten_tinh_nang, từ nối; hoặc là tên riêng (từ viết hoa giữa chữ hay viết liền kiểu HyperCharge) đi cùng ít nhất
    một từ tên gọi chung, hoặc viết liền kiểu HyperCharge, hoặc đứng một mình thành cả dòng (cụm trùng câu trích). Cụm có chữ báo điều kiện ("chế độ chơi game", "khi
    bơi") không thuộc loại này vì có từ không phải tên gọi hay tên riêng."""
    cau_hinh_tieu_de = (chung.get("dieu_kien_la") or {}).get("tieu_de") or {}
    cum_ten = [chuan_hoa_chu(x).split() for x in [*(cau_hinh_tieu_de.get("tu_ten_chung") or []), *(cau_hinh_tieu_de.get("tu_noi") or []),
                                                    *((chung.get("tu_khang_dinh") or {}).get("ten_tinh_nang") or [])]]
    goc = [t.strip(",.;:!?\"'()[]") for t in cum.split()]
    goc = [t for t in goc if t]
    if not goc or any(ch.isdigit() for t in goc for ch in t):
        return False
    thap = [chuan_hoa_chu(t) for t in goc]
    phu = [False] * len(thap)
    for ten in sorted(cum_ten, key=len, reverse=True):
        for i in range(len(thap) - len(ten) + 1):
            if thap[i:i + len(ten)] == ten:
                for j in range(i, i + len(ten)):
                    phu[j] = True
    tat_ca_hoa = all(t[0].isupper() or not t[0].isalpha() for t in goc)

    def ten_rieng(t, i):
        return (len(t) > 1 and (t.isupper() or any(ch.isupper() for ch in t[1:]))) or (t[0].isupper() and (i > 0 or tat_ca_hoa))

    chua = [i for i, p in enumerate(phu) if not p]
    if any(not ten_rieng(goc[i], i) for i in chua):
        return False
    viet_lien = all(re.search(r"[a-zà-ỹ][A-Z]", goc[i]) for i in chua)   # tên riêng viết liền kiểu HyperCharge, ProMotion đứng một mình
    return not chua or any(phu) or viet_lien or chuan_hoa_chu(_bo_ngoac(cum)).split() == chuan_hoa_chu(_bo_ngoac(trich)).split()


def _gop(chu):
    return " ".join(chu.split())


def _gop_ban_do(chu):
    """(chuỗi gộp khoảng trắng, bản đồ về chỉ số của chu)."""
    ra, bd = [], []
    for i, c in enumerate(chu):
        if c.isspace():
            if ra and ra[-1] != " ":
                ra.append(" ")
                bd.append(i)
        else:
            ra.append(c)
            bd.append(i)
    if ra and ra[-1] == " ":
        ra.pop()
        bd.pop()
    return "".join(ra), bd


def _doi_gio_phut(so, tu, den):
    """Số `so` đơn vị tu theo đơn vị den: cùng đơn vị giữ nguyên, giờ và phút đổi được cho nhau (HD mục 6.3: "trong 1 giờ" so với
    "tối đa 30 phút"); đơn vị khác thì None (T-20)."""
    try:
        return quy_doi(so, tu, den)
    except ValueError:
        return None


def _so_dieu_kien(don_vi, cac_chu, cum_cfg, ngam, chung):
    """Con số của điều kiện dạng số (mục 6): GiaTri có đơn vị đúng (giờ và phút đổi cho nhau, kết quả theo don_vi) trong từng chữ của
    cac_chu theo thứ tự (cụm rồi câu trích), lấy con số gần cụm nhất; không có thì tra gia_tri_ngam theo cụm cấu hình. None nếu
    không đọc được."""
    for chu in cac_chu:
        gop = _gop(chu)
        ung = [(g, so) for g in tim_gia_tri(gop, chung) for so in [_doi_gio_phut(g.so, g.don_vi, don_vi)] if so is not None]
        if ung:
            vi_tri = max(gop.lower().find(cum_cfg), 0)
            return min(ung, key=lambda x: (abs(x[0].dau - vi_tri), x[0].dau))[1]
    bang = {chuan_hoa_chu(k): v for k, v in (ngam or {}).items()}
    return bang.get(cum_cfg)


def _khoa_so(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=False)


def _gon(c):
    return chuan_hoa_chu(re.sub(r"[()]", " ", c))


def _cum_kieu(cau_hinh):
    """Tập cụm (đã bỏ ngoặc, chuẩn hóa chữ) mà cụm điều kiện LLM ghi trùng hẳn thì là kiểu giá trị, không phải điều kiện (mục 6.3):
    kieu_gia_tri, tu_khang_dinh (tu, tu_muc_san bỏ "<số>"), tu_goi_muc_cao của chung.yaml, kieu_dung_luong của nhóm."""
    chung = cau_hinh["chung"]
    nguon = [*(_cum_cua_muc(m) for m in chung["kieu_gia_tri"].values()), _cum_cua_muc(chung["tu_khang_dinh"].get("tu")),
             _cum_cua_muc(chung.get("tu_goi_muc_cao")),
             *(_cum_cua_muc(m) for m in ((cau_hinh.get("cach_dien_dat") or {}).get("kieu_dung_luong") or {}).values())]
    tu_so = [m.replace(KY_HIEU_SO, " ") for m in chung["tu_khang_dinh"].get("tu_muc_san") or []]
    return {_gon(c) for ds in [*nguon, tu_so] for c in ds if _gon(c)}


LOAI_NHAN_THEO_DON_VI = ("phu_kien", "dieu_kien_do")   # loại điều kiện được nhận theo đơn vị (bổ sung 08/11 khi cài)


def dieu_kien_so_theo_don_vi(tt_yaml):
    """{khóa đơn vị: tên điều kiện} của các điều kiện dạng số (dieu_kien_so) loại phu_kien hoặc dieu_kien_do mà đơn vị của nó không
    trùng đơn vị của điều kiện dạng số nào khác trong cùng thuộc tính (hai điều kiện cùng đơn vị thì không nhận theo đơn vị).
    Giờ và phút đổi được cho nhau (T-20): điều kiện dạng phút còn được nhận khi con số ghi bằng giờ (khóa "gio") và ngược lại, trừ
    khi thuộc tính đã có điều kiện riêng cho đơn vị kia hoặc chính giá trị của thuộc tính tính bằng giờ/phút (khi đó một con số giờ
    trong cụm điều kiện nhiều khả năng là giá trị đặt nhầm chỗ, như "lên đến 8 giờ"); hieu_dieu_kien đổi số về đơn vị của điều kiện."""
    bb = tt_yaml.get("dieu_kien_bat_buoc") or {}
    theo = {}
    for ten, kb in (tt_yaml.get("dieu_kien_so") or {}).items():
        theo.setdefault(kb["don_vi"], []).append(ten)
    ra = {dv: ds[0] for dv, ds in theo.items() if len(ds) == 1 and bb.get(ds[0]) in LOAI_NHAN_THEO_DON_VI}
    if tt_yaml.get("don_vi") not in ("gio", "phut", "phut_hoac_gio"):
        for dv, kia in (("phut", "gio"), ("gio", "phut")):
            if dv in ra and kia not in theo:
                ra[kia] = ra[dv]
    return ra


def _bo_gia_tri_cua_muc(gts, gia_tri):
    """Bỏ khỏi danh sách GiaTri con số chính là giá trị của mục (cùng số và cùng khóa đơn vị). gia_tri: (số, khóa đơn vị) hoặc None."""
    if gia_tri is None or not isinstance(gia_tri[0], float):
        return gts
    return [g for g in gts if not (g.so == gia_tri[0] and g.don_vi == gia_tri[1])]


# --- Hiểu điều kiện (mục 6) ---

def hieu_dieu_kien(cac_dk, thuoc_tinh, phia, cau_hinh, gia_tri=None):
    """Hiểu điều kiện kiểu đóng cho các điều kiện còn sau neo nguồn. cac_dk: [{"i", "loai", "cum", "trich"}].

    Trả {"dieu_kien", "dieu_kien_phu", "dieu_kien_khac", "ngu_canh", "bo_qua", "xung_dot", "trich", "nguon_dieu_kien",
    "cum_kieu"}; cum_kieu là [(chỉ số, cụm)] của cụm kiểu giá trị LLM ghi (không ghi vào dieu_kien, dành cho mục 7 và P−NN).
    Thứ tự theo mục 6: ngữ cảnh, cach_dien_dat, điều kiện dạng số nhận theo đơn vị, kiểu giá trị (loai là kieu_gia_tri hoặc cụm
    trùng hẳn một cụm kiểu), cum_khong_phai_dieu_kien, rồi dieu_kien_khac. Tìm cụm cấu hình trong "cum", không trong "trich".

    Điều kiện dạng số nhận theo đơn vị (bổ sung 08/11 khi cài): cụm không khớp cụm cấu hình nào mà có con số (tim_gia_tri trên cụm
    đã gộp khoảng trắng) có đơn vị trùng đơn vị của đúng một điều kiện dạng số loại phu_kien hay dieu_kien_do của thuộc tính
    (dieu_kien_so_theo_don_vi) thì ghi điều kiện đó {"so", "don_vi"}, nguon_dieu_kien là "llm_don_vi" ("sạc tới 50%" là
    moc_phan_tram). Con số chính là gia_tri (số, khóa đơn vị) của mục không tính. gia_tri: (số, khóa đơn vị) hoặc None."""
    chung = cau_hinh["chung"]
    tt_yaml = (cau_hinh["thuoc_tinh"].get(thuoc_tinh) if thuoc_tinh else None) or {}
    dk_bb = tt_yaml.get("dieu_kien_bat_buoc") or {}
    dieu_kien_so = tt_yaml.get("dieu_kien_so") or {}
    cach = cau_hinh.get("cach_dien_dat") or {}
    ung_vien = _ung_vien(cau_hinh, phia, thuoc_tinh)
    ngu_canh_cfg = [chuan_hoa_chu(c) for c in _cum_cua_muc(chung["ngu_canh_khong_quyet_dinh"])]
    cum_kieu_cfg = _cum_kieu(cau_hinh)
    khong_phai = {chuan_hoa_chu(c) for c in chung.get("cum_khong_phai_dieu_kien") or []}
    ra = {"dieu_kien": {}, "dieu_kien_phu": {}, "dieu_kien_khac": [], "ngu_canh": [], "bo_qua": [], "xung_dot": {},
          "trich": {}, "nguon_dieu_kien": {}, "cum_kieu": []}
    theo_don_vi = dieu_kien_so_theo_don_vi(tt_yaml)
    nguon_ten = {}           # tên điều kiện -> "llm" (cụm cấu hình) hoặc "llm_don_vi"
    gia, trich_dk = {}, {}   # tên điều kiện -> {khóa so sánh: giá trị} theo thứ tự gặp; tên -> câu trích đầu tiên
    for dk in cac_dk:
        c = _chuan_cum_cau_hinh(dk["cum"])
        if any(re.search(_mau_cum(p), c) for p in ngu_canh_cfg):
            ra["ngu_canh"].append(dk["cum"])
            continue
        khop = _tim_khop(c, ung_vien)
        if not khop and dk["loai"] != "kieu_gia_tri" and _gon(dk["cum"]) not in cum_kieu_cfg:   # cụm kiểu giá trị ("lên đến") không phải cụm rút gọn
            khop = _khop_trong_trich(c, dk["trich"], ung_vien)
        if khop:
            for _, _, ten, gt, cum_cfg in khop:
                if ten not in dk_bb:
                    ra["dieu_kien_phu"].setdefault(ten, gt)
                    continue
                gia_tri_dk = gt   # không dùng tên gia_tri: tham số gia_tri là giá trị của mục (dùng ở luật đơn vị bên dưới)
                if ten in dieu_kien_so and gt == "gia_tri_so":
                    so = _so_dieu_kien(dieu_kien_so[ten]["don_vi"], [dk["cum"], dk["trich"]], cum_cfg,
                                       (cach[ten][gt] or {}).get("gia_tri_ngam"), chung)
                    if so is None:
                        ra["dieu_kien_khac"].append({"loai": dk["loai"], "cum": dk["cum"], "trich": dk["trich"],
                                                     "ly_do": "khong_doc_duoc_so"})
                        continue
                    gia_tri_dk = {"so": so, "don_vi": dieu_kien_so[ten]["don_vi"]}
                gia.setdefault(ten, {}).setdefault(_khoa_so(gia_tri_dk), gia_tri_dk)
                trich_dk.setdefault(ten, dk["trich"])
                nguon_ten[ten] = "llm"
            continue
        so_theo_don_vi = [g for g in _bo_gia_tri_cua_muc(tim_gia_tri(_gop(dk["cum"]), chung), gia_tri) if g.don_vi in theo_don_vi]
        if so_theo_don_vi:
            for g in so_theo_don_vi:
                ten = theo_don_vi[g.don_vi]
                dv_dk = dieu_kien_so[ten]["don_vi"]
                so_dk = {"so": _doi_gio_phut(g.so, g.don_vi, dv_dk), "don_vi": dv_dk}
                gia.setdefault(ten, {}).setdefault(_khoa_so(so_dk), so_dk)
                trich_dk.setdefault(ten, dk["trich"])
                nguon_ten[ten] = "llm" if nguon_ten.get(ten, "llm_don_vi") == "llm" else "llm_don_vi"
            continue
        if dk["loai"] == "kieu_gia_tri" or _gon(dk["cum"]) in cum_kieu_cfg:
            ra["cum_kieu"].append((dk["i"], dk["cum"]))
        elif c in khong_phai or _la_tieu_de(dk["cum"], dk["trich"], chung):
            ra["bo_qua"].append(dk["cum"])
        else:
            ra["dieu_kien_khac"].append({"loai": dk["loai"], "cum": dk["cum"], "trich": dk["trich"]})
    for ten, cac_gia_tri in gia.items():
        if len(cac_gia_tri) == 1:
            ra["dieu_kien"][ten] = next(iter(cac_gia_tri.values()))
            ra["trich"][f"dieu_kien.{ten}"] = trich_dk[ten]
            ra["nguon_dieu_kien"][ten] = nguon_ten[ten]
        elif dk_bb.get(ten) != "kieu_gia_tri":
            ra["xung_dot"][ten] = list(cac_gia_tri.values())
        # Điều kiện loại kieu_gia_tri có hai giá trị trong một mục ("tốc độ làm mới thích ứng lên đến 120Hz": thích ứng và tối đa) không phải
        # xung đột điều kiện: kiểu giá trị không đổi điều kiện đo (HD mục 6.1: "màn hình 120Hz" khớp "thích ứng lên đến 120Hz"), nên bỏ.
    return ra


# --- Kiểm tra đầy đủ (mục 7) ---

NUM_DONG_TIEU_DE = 2   # vung_do: số dòng tiêu đề nhóm tối đa lấy kèm


class _Vung:
    """Vùng dò đã gộp khoảng trắng; [lo, hi) là chỗ câu trích của giá trị trong text."""

    def __init__(self, text, lo, hi):
        self.text, self.lo, self.hi = text, lo, hi
        self.nhan = text   # chữ nhãn dòng (vung_do gán lại: dòng giá trị kèm tiêu đề nhóm gần nhất)

    def khoang_cach(self, dau):
        return 0 if self.lo <= dau < self.hi else min(abs(dau - self.lo), abs(dau - self.hi))


def vung_do(nguon, trich, so=None, can_tieu_de=None):
    """Vùng dò của một câu trích trong văn bản nguồn: các dòng chứa câu trích (mở rộng tới đầu và cuối dòng), khoảng trắng gộp.
    Câu trích có ở nhiều chỗ thì lấy chỗ đầu tiên có dòng chứa con số bằng so (nếu có so), không thì chỗ đầu. None nếu câu
    trích không có trong nguồn.

    Dòng chứa ";" và có so: vùng dò chỉ là vế chứa con số (HD mục 6.8: "độ sáng tối đa 1000 nit (tiêu chuẩn); độ sáng đỉnh 1600 nit (HDR); ..."
    của Apple, mỗi chế độ một vế).

    can_tieu_de (T-01 c): hàm nhận chữ của các dòng đã chọn (gộp khoảng trắng), trả True khi dòng không tự nêu thuộc tính hay điều kiện
    nào (không có cụm cấu hình). Khi đó vùng dò lấy kèm tối đa NUM_DONG_TIEU_DE dòng liền phía trên không rỗng và không có chữ số
    (tiêu đề nhóm: "Thời gian phát nhạc (bật ANC)" trên dòng "Lên đến 6"), vì chữ ở tiêu đề nhóm cũng là điều kiện của dòng. Dòng bắt đầu
    bằng "(" và không có chữ số liền sau dòng đã chọn là chú thích của dòng đó ("Đến 6,0/26 giờ" rồi "(Tính năng ANC Bật)" của #042)
    nên luôn được lấy kèm; dòng như vậy ở phía trên là chú thích của giá trị trước, không lấy làm tiêu đề."""
    cho = nn.tim_trich(nguon, trich)
    if not cho:
        return None

    def dong(d, c):
        a = nguon.rfind("\n", 0, d) + 1
        b = nguon.find("\n", c)
        return a, (len(nguon) if b < 0 else b)

    chon = cho[0]
    if so is not None:
        for d, c in cho:
            a, b = dong(d, c)
            if any(bang_nhau(so, s.so) for s in tim_so(_gop(nguon[a:b]))):
                chon = (d, c)
                break
    d, c = chon
    a, b = dong(d, c)
    if so is not None and ";" in nguon[a:b]:   # dòng liệt kê nhiều giá trị cách nhau ";": chỉ dò trong vế chứa con số (không lẫn chế độ của vế khác)
        dau_ve = a
        for ve in nguon[a:b].split(";"):
            if any(bang_nhau(so, x.so) for x in tim_so(_gop(ve))):
                a, b = dau_ve, dau_ve + len(ve)
                break
            dau_ve += len(ve) + 1
    a_gan = a   # đầu của dòng tiêu đề gần nhất (hoặc của dòng giá trị nếu không lấy tiêu đề): chữ nhãn dòng của luật chép đúng nhãn
    if can_tieu_de is not None and can_tieu_de(_gop(nguon[a:b])):
        for lan in range(NUM_DONG_TIEU_DE):
            if a == 0:
                break
            truoc = nguon[nguon.rfind("\n", 0, a - 1) + 1:a - 1]
            # dòng "(...)" là chú thích đứng sau giá trị của dòng trước nó ("Đến 7,0/30 giờ" rồi "(Tính năng ANC Tắt)"), không phải tiêu đề nhóm
            if not truoc.strip() or truoc.lstrip().startswith("(") or any(ch.isdigit() for ch in truoc):
                break
            a -= len(truoc) + 1
            if lan == 0:
                a_gan = a
    if b < len(nguon):   # dòng "(...)" không có chữ số liền sau là chú thích của dòng này
        fin = nguon.find("\n", b + 1)
        sau = nguon[b + 1:(fin if fin >= 0 else len(nguon))]
        if sau.lstrip().startswith("(") and not any(ch.isdigit() for ch in sau):
            b += 1 + len(sau)
    text, bd = _gop_ban_do(nguon[a:b])
    lo = next((i for i, x in enumerate(bd) if x >= d - a), len(bd))
    hi = max((i + 1 for i, x in enumerate(bd) if x < c - a), default=lo)
    vung = _Vung(text, lo, hi)
    vung.nhan = _gop(nguon[a_gan:b])
    return vung


def vung_tuyen_bo(chu, trich=None):
    """Vùng dò của tuyên bố: toàn bộ chữ tuyên bố (gộp khoảng trắng)."""
    text, _ = _gop_ban_do(chu)
    cho = text.lower().find(_gop(trich).lower()) if trich else -1
    return _Vung(text, 0, len(text)) if cho < 0 else _Vung(text, cho, cho + len(_gop(trich)))


def _chon_gia_tri(vung, gt, chung):
    """GiaTri của con số bằng giá trị trong vùng dò, gần câu trích nhất. Dòng không ghi đơn vị: lập GiaTri từ tim_so."""
    so, khoa = gt["gia_tri"], gt["khoa_don_vi"]
    ung = [g for g in tim_gia_tri(vung.text, chung) if bang_nhau(so, g.so) and (khoa is None or g.don_vi == khoa)]
    if not ung:
        ung = [GiaTri(so, khoa or "", s.chu, s.dau, s.cuoi) for s in tim_so(vung.text) if bang_nhau(so, s.so)]
    return min(ung, key=lambda g: (vung.khoang_cach(g.dau), g.dau)) if ung else None


def _kieu_tu_cum_llm(cac_cum, chung, cum_them):
    """P−NN (mục 9): kiểu giá trị theo cụm kiểu LLM ghi, map qua cấu hình bằng chính tim_kieu_gia_tri (đặt cụm liền trước số 0)."""
    tot = None
    for cum in cac_cum:
        c = chuan_hoa_chu(cum)
        k = tim_kieu_gia_tri(f"{c} 0", GiaTri(0.0, "", "0", len(c) + 1, len(c) + 2), chung, cum_them)
        if k.kieu == "khang_dinh":
            return k
        if k.kieu != "khong_neu" and tot is None:
            tot = k
    return tot or KieuGiaTri("khong_neu", None, False)


def _bo_sung_dieu_kien(muc, vung, phia, chi_so, cau_hinh, thuoc_tinh, bo_sung, mo_ho, gia_tri_muc=None, van_ban_doan=None):
    """Mục 7.1: điều kiện bắt buộc mà mục chưa có (cả xung_dot) thì dò cụm của điều kiện đó trong vùng dò. Thấy đúng một giá trị
    thì điền và ghi bo_sung; hai giá trị khác nhau (hay con số điều kiện không rõ là số nào) thì không điền, ghi bo_sung_mo_ho.

    Điều kiện dạng số nhận theo đơn vị (bổ sung 08/11 khi cài): điều kiện dạng số loại phu_kien hay dieu_kien_do mà đơn vị là của
    riêng nó trong thuộc tính (dieu_kien_so_theo_don_vi) và vẫn chưa có thì dò mọi con số có đơn vị đó trong vùng dò, bỏ con số
    chính là giá trị của mục (gia_tri_muc: (số, khóa đơn vị)). Thấy đúng một số thì điền (cụm là chữ khớp, vd "50%"), nhiều số
    khác nhau thì bo_sung_mo_ho.

    Phụ kiện dạng số ghi ở chú thích (Bước 28; HD mục 4: chú thích có giá trị như nội dung chính, bộ tiếp hợp 20W của Apple Watch SE 3 chỉ
    nằm trong chú thích; V34): điều kiện loại phu_kien dạng số mà vẫn chưa có sau khi dò vùng dò, ở mục tài liệu, thì dò cụm của nó (cụm
    cấu hình kèm con số, như "Bộ Tiếp Hợp Nguồn USB-C 20W") trong cả văn bản đoạn (van_ban_doan), vì chú thích của đoạn áp cho mọi dòng
    của đoạn. Thấy đúng một số thì điền, nhiều số khác nhau thì bo_sung_mo_ho (không đoán dòng nào dùng bộ nào)."""
    chung = cau_hinh["chung"]
    tt_yaml = cau_hinh["thuoc_tinh"][thuoc_tinh]
    dieu_kien_so = tt_yaml.get("dieu_kien_so") or {}
    cach = cau_hinh.get("cach_dien_dat") or {}
    khop = _tim_khop(chuan_hoa_chu(vung.text), _ung_vien(cau_hinh, phia, thuoc_tinh, giu_ngoac=True))
    don_vi_rieng = set(dieu_kien_so_theo_don_vi(tt_yaml).values())
    for ten in tt_yaml.get("dieu_kien_bat_buoc") or {}:
        if ten in muc["dieu_kien"] or ten in muc["xung_dot"]:
            continue
        gia, cum_thay, mo_ho_so = {}, [], False
        for dau, cuoi, _, gt, cum_cfg in (x for x in khop if x[2] == ten):
            chu_cum = vung.text[dau:cuoi]
            if ten in dieu_kien_so and gt == "gia_tri_so":
                don_vi = dieu_kien_so[ten]["don_vi"]
                so = _so_dieu_kien(don_vi, [chu_cum], cum_cfg, (cach[ten][gt] or {}).get("gia_tri_ngam"), chung)
                if so is None:
                    trong_vung = sorted({g.so for g in _bo_gia_tri_cua_muc(tim_gia_tri(vung.text, chung), gia_tri_muc)
                                         if g.don_vi == don_vi})
                    if len(trong_vung) > 1:
                        mo_ho_so = True
                        cum_thay.append(chu_cum)
                        continue
                    so = trong_vung[0] if trong_vung else None
                if so is None:
                    continue
                gt = {"so": so, "don_vi": don_vi}
            gia.setdefault(_khoa_so(gt), gt)
            cum_thay.append(chu_cum)
        if not gia and not mo_ho_so and ten in don_vi_rieng:
            don_vi = dieu_kien_so[ten]["don_vi"]
            for g in _bo_gia_tri_cua_muc(tim_gia_tri(vung.text, chung), gia_tri_muc):
                if g.don_vi == don_vi:
                    so_dk = {"so": g.so, "don_vi": don_vi}
                    gia.setdefault(_khoa_so(so_dk), so_dk)
                    cum_thay.append(g.chu)
        if (not gia and not mo_ho_so and van_ban_doan and phia == "tai_lieu" and ten in dieu_kien_so
                and (tt_yaml.get("dieu_kien_bat_buoc") or {}).get(ten) == "phu_kien"):
            text = _gop(van_ban_doan)
            ung_vien = [x for x in _ung_vien(cau_hinh, phia, thuoc_tinh, giu_ngoac=True)]
            for dau, cuoi, _, gt, cum_cfg in (x for x in _tim_khop(chuan_hoa_chu(text), ung_vien) if x[2] == ten):
                so = _so_dieu_kien(dieu_kien_so[ten]["don_vi"], [text[dau:cuoi]], cum_cfg, (cach[ten][gt] or {}).get("gia_tri_ngam"), chung)                     if gt == "gia_tri_so" else None
                if so is not None:
                    so_dk = {"so": so, "don_vi": dieu_kien_so[ten]["don_vi"]}
                    gia.setdefault(_khoa_so(so_dk), so_dk)
                    cum_thay.append(text[dau:cuoi])
        if mo_ho_so or len(gia) > 1:
            mo_ho.append({"phia": phia, "chi_so": chi_so, "dieu_kien": ten, "gia_tri": list(gia.values()), "cum": cum_thay})
        elif gia:
            gt = next(iter(gia.values()))
            muc["dieu_kien"][ten] = gt
            muc["nguon_dieu_kien"][ten] = "bo_sung"
            bo_sung.append({"phia": phia, "chi_so": chi_so, "dieu_kien": ten, "gia_tri": gt, "cum": cum_thay[0]})


def _cap_gach_cheo(muc, vung, gt, phia, chi_so, cau_hinh, thuoc_tinh, bo_sung):
    """Mục 7.3: vùng dò có "a / b <đơn vị>" với a < b và mục chưa có bo_phan thì số a là cap[0] (tai_nghe), số b là cap[1]
    (kem_hop_sac); ghi bo_sung với cụm là chính "a / b <đơn vị>" trong vùng dò."""
    cap = cau_hinh["thuoc_tinh"][thuoc_tinh].get("cap_so_gach_cheo")
    if not cap or "bo_phan" in muc["dieu_kien"] or "bo_phan" in muc["xung_dot"]:
        return
    gts = tim_gia_tri(vung.text, cau_hinh["chung"])
    cac_cap = [(a, b) for a, b in zip(gts, gts[1:]) if a.dau_nhom == a.dau and b.dau_nhom == a.dau and a.so < b.so]
    ung = [(g, cap[k], a, b) for a, b in cac_cap for k, g in enumerate((a, b)) if bang_nhau(gt["gia_tri"], g.so)]
    if not ung:
        return
    g, bo_phan, a, b = min(ung, key=lambda x: (vung.khoang_cach(x[0].dau), x[0].dau))
    muc["dieu_kien"]["bo_phan"] = bo_phan
    muc["nguon_dieu_kien"]["bo_phan"] = "bo_sung"
    bo_sung.append({"phia": phia, "chi_so": chi_so, "dieu_kien": "bo_phan", "gia_tri": bo_phan,
                    "cum": vung.text[a.dau:b.cuoi]})


# --- Một mục và cả bản ghi ---

LY_DO_DAI_LUONG_KHAC = "dai_luong_khac"


def _la_dai_luong_khac(gia_tri, cac_cum, chung):
    """Giá trị của mục tài liệu là con số của một đại lượng khác mà hướng dẫn xếp ngoài phạm vi (dai_luong_khac của thuộc tính trong
    YAML, ví dụ "độ sáng tối thiểu" của do_sang, HD mục 2, 6.5): cụm đứng liền trước con số trong câu trích, ở mọi chỗ con số xuất hiện."""
    if not cac_cum or not isinstance(gia_tri["gia_tri"], float):
        return False
    trich = _gop(unicodedata.normalize("NFC", gia_tri["trich"]))
    cho = [(g.dau, g.cuoi) for g in tim_gia_tri(trich, chung) if bang_nhau(gia_tri["gia_tri"], g.so)] or           [(x.dau, x.cuoi) for x in tim_so(trich) if bang_nhau(gia_tri["gia_tri"], x.so)]
    cum = [chuan_hoa_chu(c) for c in cac_cum]
    return bool(cho) and all(any(chuan_hoa_chu(trich[:dau]).rstrip(" :-–").endswith(c) for c in cum) for dau, _ in cho)


def _neo_lai_gia_tri_tuyen_bo(gia_tri, chu_tuyen_bo, chung, thuoc_tinh, don_vi_yaml, huong=None):
    """T-10, phía tuyên bố: gia_tri bị loại vì câu trích LLM lược chữ (trich_khong_co_trong_nguon, ví dụ "tần số quét 120Hz" cho câu
    "tần số quét màn hình 120Hz"). Tuyên bố là câu đơn có đúng một thuộc tính và một giá trị (HD mục 2), nên nếu chữ tuyên bố có đúng
    một giá trị số có đơn vị dùng được cho thuộc tính (don_vi_tuong_thich), và nó bằng con số LLM đã trích, thì neo lại vào chuỗi thật
    đó. Trả chuỗi thật trong chữ tuyên bố, hoặc None (không đọc được số, mã IP/không, không có hay có nhiều hơn một giá trị khớp)."""
    try:
        loai, so, _ = nn.doc_gia_tri(gia_tri["chu"], gia_tri["don_vi"], chung, thuoc_tinh, huong)
    except ValueError:
        return None
    if loai != "so" or don_vi_yaml == "ma_ip":
        return None
    chu = unicodedata.normalize("NFC", chu_tuyen_bo)
    khop = [g for g in tim_gia_tri(chu, chung) if don_vi_tuong_thich(g.don_vi, don_vi_yaml)]
    if len(khop) != 1 or not bang_nhau(so, khop[0].so):   # đúng một giá trị cùng đơn vị với thuộc tính, và bằng con số LLM đã trích
        return None
    trich = chu[khop[0].dau:khop[0].cuoi]
    return trich if nn.co_trong_nguon(chu_tuyen_bo, trich) else None


def _xay_muc(muc_tho, nguon, phia, chi_so, ma_doan, thuoc_tinh, ma_mau, cau_hinh, cac_cau_hinh, chu_tuyen_bo, neo, day_du,
             bi_loai, bo_sung, mo_ho):
    """Mục bộ thông số (mục 8) sau neo nguồn, hiểu điều kiện và (nếu day_du) kiểm tra đầy đủ."""
    chung = cau_hinh["chung"]
    tt_yaml = cau_hinh["thuoc_tinh"].get(thuoc_tinh) if thuoc_tinh else None
    khoa_tt, don_vi_yaml = nn.don_vi_cua_thuoc_tinh(tt_yaml, chung), (tt_yaml or {}).get("don_vi")
    huong = (tt_yaml or {}).get("huong_thuan_loi")
    moi, loai = nn.neo_nguon_muc(muc_tho, nguon, chung, khoa_tt, neo, thuoc_tinh, don_vi_yaml, huong)
    if (day_du and phia == "tuyen_bo" and thuoc_tinh and moi["gia_tri"] is None and muc_tho["gia_tri"] is not None
            and (("gia_tri", nn.LY_DO_TRICH) in loai)):
        trich_moi = _neo_lai_gia_tri_tuyen_bo(muc_tho["gia_tri"], nguon, chung, thuoc_tinh, don_vi_yaml, huong)
        if trich_moi:
            moi2, loai2 = nn.neo_nguon_muc({**muc_tho, "gia_tri": {**muc_tho["gia_tri"], "trich": trich_moi}}, nguon, chung, khoa_tt,
                                           neo, thuoc_tinh, don_vi_yaml, huong)
            if moi2["gia_tri"] is not None:
                moi, loai = moi2, loai2
                bo_sung.append({"phia": phia, "chi_so": chi_so, "dieu_kien": "gia_tri", "gia_tri": moi["gia_tri"]["gia_tri"],
                                "cum": trich_moi})
    if phia == "tai_lieu" and moi["gia_tri"] and _la_dai_luong_khac(moi["gia_tri"], (tt_yaml or {}).get("dai_luong_khac"), chung):
        moi["gia_tri"] = None
        loai = [*loai, ("gia_tri", LY_DO_DAI_LUONG_KHAC)]
    for truong, ly_do in loai:
        _loai(bi_loai, phia, chi_so, truong, ly_do)
    gt, sp = moi["gia_tri"], moi["san_pham"]
    hieu = hieu_dieu_kien(moi["dieu_kien"], thuoc_tinh, phia, cau_hinh, (gt["gia_tri"], gt["khoa_don_vi"]) if gt else None)
    trich = dict(hieu["trich"])
    if gt:
        trich = {"gia_tri": gt["trich"], **trich}
    if sp:
        trich = {"san_pham": sp["trich"], **trich}
    muc = {"ma_doan": ma_doan, "san_pham_ma": ma_mau if (ma_doan is not None and sp is None) else None,
           "khac_san_pham": False, "thuoc_tinh": thuoc_tinh, "gia_tri": gt["gia_tri"] if gt else None,
           "don_vi": gt["khoa_don_vi"] if gt else None, "dieu_kien": hieu["dieu_kien"], "kieu_gia_tri": None,
           "cum_kieu": None, "goi_muc_cao": False, "dieu_kien_khac": hieu["dieu_kien_khac"],
           "dieu_kien_phu": hieu["dieu_kien_phu"], "ngu_canh": hieu["ngu_canh"], "bo_qua": hieu["bo_qua"],
           "xung_dot": hieu["xung_dot"], "trich": trich, "nguon_dieu_kien": hieu["nguon_dieu_kien"], "nhan_dong": None}
    la_so = bool(gt) and nn.doc_gia_tri(gt["chu"], gt["don_vi"], chung, thuoc_tinh, huong)[0] == "so"
    cum_them = (cau_hinh.get("cach_dien_dat") or {}).get("kieu_dung_luong")
    ket_qua_kieu = None
    if day_du and thuoc_tinh:
        if ma_doan is None:
            vung = vung_tuyen_bo(chu_tuyen_bo, gt["trich"] if gt else None)
        else:
            ung_cum = _ung_vien(cau_hinh, phia, thuoc_tinh, giu_ngoac=True)
            vung = (vung_do(nguon, gt["trich"], gt["gia_tri"] if la_so else None, lambda t: not _tim_khop(chuan_hoa_chu(t), ung_cum))
                    if gt and nguon is not None else None)
        if vung is not None:
            if ma_doan is not None:
                muc["nhan_dong"] = vung.nhan   # chữ thật của dòng (kèm tiêu đề nhóm gần nhất phía trên): nhãn dòng cho luật chép đúng nhãn khi câu trích của LLM lược chữ
            _bo_sung_dieu_kien(muc, vung, phia, chi_so, cau_hinh, thuoc_tinh, bo_sung, mo_ho,
                               (gt["gia_tri"], gt["khoa_don_vi"]) if gt else None, nguon if ma_doan is not None else None)
            if la_so:
                _cap_gach_cheo(muc, vung, gt, phia, chi_so, cau_hinh, thuoc_tinh, bo_sung)
                g = _chon_gia_tri(vung, gt, chung)
                ket_qua_kieu = tim_kieu_gia_tri(vung.text, g, chung, cum_them) if g else KieuGiaTri("khong_neu", None, False)
                if ket_qua_kieu.kieu == "khong_neu":
                    for i, _ in hieu["cum_kieu"]:
                        _loai(bi_loai, phia, chi_so, f"dieu_kien[{i}]", "kieu_khong_gan_so")
        if ma_doan is None:
            muc["san_pham_ma"] = tim_san_pham(chu_tuyen_bo, cac_cau_hinh)
        elif sp is not None:
            muc["san_pham_ma"] = tim_san_pham(sp["chu"], cac_cau_hinh)
            muc["khac_san_pham"] = muc["san_pham_ma"] != ma_mau
    elif la_so:
        ket_qua_kieu = _kieu_tu_cum_llm([c for _, c in hieu["cum_kieu"]], chung, cum_them)
    if la_so and ket_qua_kieu is None:   # day_du nhưng không dò được vùng (câu trích không có trong nguồn)
        ket_qua_kieu = KieuGiaTri("khong_neu", None, False)
    if ket_qua_kieu is not None:
        muc["kieu_gia_tri"], muc["cum_kieu"], muc["goi_muc_cao"] = ket_qua_kieu.kieu, ket_qua_kieu.cum, ket_qua_kieu.goi_muc_cao
    return muc


def xu_ly(du_lieu, chu_tuyen_bo, doan, ma_mau, cau_hinh, cac_cau_hinh, neo_nguon=True, kiem_day_du=True):
    """Phần thuần của P: từ đầu ra JSON đã đọc của LLM đến bộ thông số (mục 4–9), không gọi LLM.

    doan: [(mã đoạn, văn bản)] top-k đã đưa vào câu lệnh; cau_hinh: cấu hình nhóm của ma_mau (doc_cau_hinh); cac_cau_hinh: cấu
    hình các nhóm (cho tim_san_pham). Trả {"tuyen_bo", "bang_chung", "bang_chung_bi_loai", "bi_loai", "bo_sung",
    "bo_sung_mo_ho", "loi"}; loi khác None thì mọi thứ còn lại rỗng và tuyen_bo là None."""
    chung = cau_hinh["chung"]
    tb_tho, ds_tl, bi_loai, loi = doc_luoc_do(du_lieu, set(chung["loai_dieu_kien"]))
    ket = {"tuyen_bo": None, "bang_chung": [], "bang_chung_bi_loai": [], "bi_loai": bi_loai, "bo_sung": [],
           "bo_sung_mo_ho": [], "loi": loi}
    if loi:
        return ket
    thuoc_tinh = tb_tho["thuoc_tinh"]
    if thuoc_tinh is not None and thuoc_tinh not in cau_hinh["thuoc_tinh"]:
        _loai(bi_loai, "tuyen_bo", None, "thuoc_tinh", "thuoc_tinh_ngoai_nhom")
        thuoc_tinh = None
    van_ban = dict(doan)
    chung_tham_so = (ma_mau, cau_hinh, cac_cau_hinh, chu_tuyen_bo, neo_nguon, kiem_day_du)
    ket["tuyen_bo"] = _xay_muc(tb_tho, chu_tuyen_bo, "tuyen_bo", None, None, thuoc_tinh, *chung_tham_so, bi_loai,
                               ket["bo_sung"], ket["bo_sung_mo_ho"])
    for m in ds_tl:
        if m["muc"] is None:
            ket["bang_chung_bi_loai"].append({"chi_so": m["chi_so"], "ma_doan": m["ma_doan"], "ly_do": m["ly_do"],
                                              "gia_tri": None})
            continue
        i, ma = m["chi_so"], m["ma_doan"]
        gia_tri_tho = m["muc"]["gia_tri"]
        if thuoc_tinh is None:
            _loai(bi_loai, "tai_lieu", i, "muc", "khong_co_thuoc_tinh")
            ket["bang_chung_bi_loai"].append({"chi_so": i, "ma_doan": ma, "ly_do": ["khong_co_thuoc_tinh"], "gia_tri": gia_tri_tho})
            continue
        if neo_nguon and ma not in van_ban:
            _loai(bi_loai, "tai_lieu", i, "muc", nn.LY_DO_DOAN_NGOAI_TOP_K)
            ket["bang_chung_bi_loai"].append({"chi_so": i, "ma_doan": ma, "ly_do": [nn.LY_DO_DOAN_NGOAI_TOP_K],
                                              "gia_tri": gia_tri_tho})
            continue
        muc = _xay_muc({**m["muc"], "thuoc_tinh": thuoc_tinh}, van_ban.get(ma), "tai_lieu", i, ma, thuoc_tinh, *chung_tham_so,
                       bi_loai, ket["bo_sung"], ket["bo_sung_mo_ho"])
        if muc["gia_tri"] is None:
            ly_do = [b["ly_do"] for b in bi_loai if b["phia"] == "tai_lieu" and b["chi_so"] == i and b["truong"] == "gia_tri"]
            ket["bang_chung_bi_loai"].append({"chi_so": i, "ma_doan": ma, "ly_do": ly_do or ["thieu_gia_tri"],
                                              "gia_tri": gia_tri_tho})
        else:
            ket["bang_chung"].append(muc)
    return ket


def bay_truong(muc):
    """Bộ bảy trường của T5.1 cho một mục: san_pham (mã mẫu), phien_ban, bo_phan, thuoc_tinh, gia_tri, don_vi, dieu_kien (phần còn
    lại của điều kiện, không gồm phien_ban và bo_phan) cùng kieu_gia_tri, và trich. Không có mac_dinh (việc của Bước 27)."""
    dk = muc["dieu_kien"]
    return {"san_pham": muc["san_pham_ma"], "phien_ban": dk.get("phien_ban"), "bo_phan": dk.get("bo_phan"),
            "thuoc_tinh": muc["thuoc_tinh"], "gia_tri": muc["gia_tri"], "don_vi": muc["don_vi"],
            "dieu_kien": {k: v for k, v in dk.items() if k not in ("phien_ban", "bo_phan")},
            "kieu_gia_tri": muc["kieu_gia_tri"], "trich": muc["trich"]}


def trich_xuat(tuyen_bo, ma_mau, client, mo_hinh, k=5, cach_tach="am_tiet", neo_nguon=True, kiem_day_du=True,
               thu_muc_nguon=th.THU_MUC_NGUON, max_token_ra=MAX_TOKEN_RA, nhom=None):
    """Chạy P cho một tuyên bố và trả bản ghi (mục 8).

    tuyen_bo: chữ tuyên bố (str) hoặc dict một dòng của data/tuyen_bo/thu.jsonl (lấy "id" và "tuyen_bo"); P không đọc cau_goc,
    thuoc_tinh tách tay hay nhãn. client: llm.LLMClient. neo_nguon=False, kiem_day_du=False là P−NN (mục 9). nhom mặc định theo
    mau_san_pham.csv. Bản ghi: id, ma_mau, chu_tuyen_bo, mo_hinh, nha_cung_cap, mo_hinh_thuc, k, cach_tach, doan (mã, theo
    hạng), ma_bam_cau_lenh (SHA-256), tuyen_bo, bang_chung, bang_chung_bi_loai, bi_loai, bo_sung, bo_sung_mo_ho, loi,
    neo_nguon, kiem_day_du, tra_ve_tho, finish_reason, usage, ma_yeu_cau, thoi_gian_sinh_ms (generation_ms của lần gọi LLM), tran_token (trần token ra đã dùng; gấp đôi max_token_ra nếu lần đầu bị cắt), tu_bo_nho_dem (khác nhau giữa lần chạy đầu và chạy lại;
    nơi ghi tệp nên bỏ trường này để kết quả giống từng byte)."""
    ma_id, chu = (tuyen_bo.get("id"), tuyen_bo["tuyen_bo"]) if isinstance(tuyen_bo, dict) else (None, tuyen_bo)
    nha_cung_cap = NHA_CUNG_CAP.get(mo_hinh)
    if nha_cung_cap is None:
        raise ValueError(f"mô hình chưa có nhà cung cấp: {mo_hinh!r} (có {', '.join(NHA_CUNG_CAP)})")
    nhom = nhom or nhom_cua_mau(ma_mau)
    cau_hinh = lay_cau_hinh(nhom)
    doan = th.lay_doan(ma_mau, chu, k, cach_tach, thu_muc_nguon)
    cau_lenh = ghep_cau_lenh(nhom, cau_hinh, chu, doan)
    ban_ghi = {
        "id": ma_id, "ma_mau": ma_mau, "chu_tuyen_bo": chu, "mo_hinh": mo_hinh, "nha_cung_cap": nha_cung_cap,
        "mo_hinh_thuc": None, "k": k, "cach_tach": cach_tach, "doan": [ma for ma, _ in doan],
        "ma_bam_cau_lenh": hashlib.sha256(cau_lenh.encode("utf-8")).hexdigest(), "tuyen_bo": None, "bang_chung": [],
        "bang_chung_bi_loai": [], "bi_loai": [], "bo_sung": [], "bo_sung_mo_ho": [], "loi": None, "neo_nguon": neo_nguon,
        "kiem_day_du": kiem_day_du, "tra_ve_tho": None, "finish_reason": None, "usage": None, "ma_yeu_cau": None,
        "tu_bo_nho_dem": False, "tran_token": None, "thoi_gian_sinh_ms": None,
    }
    try:
        tra_ve, tran = goi_json(client, nha_cung_cap, mo_hinh, [{"role": "user", "content": cau_lenh}],
                                NHIET_DO, max_token_ra)
    except LLMError as e:
        if e.code not in LOI_NOI_DUNG:
            raise
        ban_ghi["loi"] = f"llm_khong_tra_ve_dung: {e.code}"
        return ban_ghi
    ban_ghi.update(mo_hinh_thuc=tra_ve.actual_model, tra_ve_tho=tra_ve.text, finish_reason=tra_ve.finish_reason,
                   usage=tra_ve.usage, ma_yeu_cau=tra_ve.request_hash, tu_bo_nho_dem=tra_ve.cache_hit,
                   tran_token=tran, thoi_gian_sinh_ms=tra_ve.generation_ms)
    return _hau_xu_ly(ban_ghi, doan, cau_hinh)


def _hau_xu_ly(ban_ghi, doan, cau_hinh):
    """Đọc ban_ghi["tra_ve_tho"] rồi xu_ly (theo cờ neo_nguon, kiem_day_du của bản ghi); ghi đè các trường kết quả của bản ghi.
    JSON không đọc được thì loi khác None và các trường kết quả giữ rỗng."""
    du_lieu, loi = _doc_json(ban_ghi["tra_ve_tho"])
    if loi:
        ban_ghi["loi"] = loi
        return ban_ghi
    ban_ghi.update(xu_ly(du_lieu, ban_ghi["chu_tuyen_bo"], doan, ban_ghi["ma_mau"], cau_hinh, tat_ca_cau_hinh(),
                         ban_ghi["neo_nguon"], ban_ghi["kiem_day_du"]))
    return ban_ghi


def xu_ly_lai(ban_ghi, neo_nguon=None, kiem_day_du=None, thu_muc_nguon=th.THU_MUC_NGUON, thu_muc_cache=None):
    """Chạy lại phần hậu xử lý (neo nguồn, hiểu điều kiện, kiểm tra đầy đủ) của một bản ghi trích xuất đã lưu, không gọi LLM.

    Đọc lại từ tra_ve_tho và các đoạn theo ban_ghi["doan"] (văn bản đoạn đọc từ thu_muc_nguon). neo_nguon, kiem_day_du khác None thì
    đổi cờ của bản ghi (P-NN: cả hai False). Bản ghi chưa có tra_ve_tho (lỗi gọi LLM) giữ nguyên. thu_muc_cache khác None và bản ghi
    chưa có thoi_gian_sinh_ms thì lấy generation_ms từ <thu_muc_cache>/<ma_yeu_cau>.json nếu tệp có. Trả bản ghi mới, không sửa đầu vào."""
    moi = json.loads(json.dumps(ban_ghi))
    if thu_muc_cache and moi.get("thoi_gian_sinh_ms") is None and moi.get("ma_yeu_cau"):
        tep = Path(thu_muc_cache) / f"{moi['ma_yeu_cau']}.json"
        if tep.is_file():
            with open(tep, encoding="utf-8") as f:
                moi["thoi_gian_sinh_ms"] = (json.load(f).get("result") or {}).get("generation_ms")
    if moi.get("tra_ve_tho") is None:
        return moi
    if neo_nguon is not None:
        moi["neo_nguon"] = neo_nguon
    if kiem_day_du is not None:
        moi["kiem_day_du"] = kiem_day_du
    van_ban = dict(th.doc_doan(moi["ma_mau"], thu_muc_nguon))
    moi["loi"] = None
    return _hau_xu_ly(moi, [(ma, van_ban[ma]) for ma in moi["doan"]], lay_cau_hinh(nhom_cua_mau(moi["ma_mau"])))


# --- LLM giả ---

def _so_chu(g):
    """(chữ con số, chữ đơn vị) của một GiaTri."""
    so = re.search(r"[0-9]+(?:[.,][0-9]+)*", g.chu).group(0)
    don_vi = re.search(r"[^\d\s./,]+$", g.chu)
    return so, (don_vi.group(0) if don_vi else None)


def gia_transport(request, timeout_s):
    """LLM GIẢ cho chạy thử (--gia) và test: KHÔNG phải LLM, không gọi mạng, không là bằng chứng thực nghiệm.

    Đọc tuyên bố và đoạn từ chính câu lệnh; thuộc tính và biến thể phản hồi lấy từ mã băm câu lệnh nên cùng câu lệnh luôn ra cùng
    kết quả. Chép con số có đơn vị đầu tiên của tuyên bố và của hai đoạn đầu (câu trích là cả dòng), có đủ các dạng phản hồi để
    chạy qua đường neo nguồn: khối ```json, câu trích bịa, mã đoạn ngoài top-k, không phải JSON."""
    cau_lenh = request["messages"][-1]["content"]
    h = int(hashlib.sha256(cau_lenh.encode("utf-8")).hexdigest(), 16) % 8
    chung = doc_yaml(THU_MUC / "chung.yaml")
    cuoi = cau_lenh[cau_lenh.rfind("BÂY GIỜ LÀM VỚI"):]
    tb = re.search(r"Tuyên bố: (.*)\nTài liệu:\n", cuoi).group(1)
    ma_thuoc_tinh = re.findall(r"^- ([a-z_]+) \(", cau_lenh, re.M)
    cac_cho = list(re.finditer(r"^\[([^\]\s]+#\d+)\] ", cuoi, re.M))
    doan = []
    for j, m in enumerate(cac_cho):
        het = cac_cho[j + 1].start() if j + 1 < len(cac_cho) else cuoi.rfind("\nKết quả:")
        doan.append((m.group(1), cuoi[m.end():het].strip("\n")))

    def muc_gia_tri(g, trich):
        so, don_vi = _so_chu(g)
        return {"chu": so, "don_vi": don_vi, "trich": trich}

    gts = tim_gia_tri(tb, chung)
    tuyen_bo = {"san_pham": None, "thuoc_tinh": ma_thuoc_tinh[h % len(ma_thuoc_tinh)] if ma_thuoc_tinh else None,
                "gia_tri": muc_gia_tri(gts[0], tb[gts[0].dau:gts[0].cuoi]) if gts else None, "dieu_kien": []}
    bang_chung = []
    for ma, van_ban in doan[:2]:
        for dong in van_ban.split("\n"):
            for g in tim_gia_tri(dong, chung):
                dk = [{"loai": "kieu_gia_tri", "cum": c, "trich": dong} for c in ("lên đến", "tối đa") if c in dong.lower()]
                bang_chung.append({"ma_doan": ma, "san_pham": None, "gia_tri": muc_gia_tri(g, dong), "dieu_kien": dk[:1]})
    if h == 5 and bang_chung:
        bang_chung.append({"ma_doan": bang_chung[0]["ma_doan"], "san_pham": None, "dieu_kien": [],
                           "gia_tri": {"chu": "99", "don_vi": "giờ", "trich": "nội dung bịa không có trong nguồn"}})
    if h == 6 and bang_chung:
        bang_chung.append({**bang_chung[0], "ma_doan": "ngoai-top-k#999"})
    noi_dung = json.dumps({"tuyen_bo": tuyen_bo, "bang_chung": bang_chung[:12]}, ensure_ascii=False)
    if h == 3:
        noi_dung = f"```json\n{noi_dung}\n```"
    if h == 7:
        noi_dung = "Đây là LLM giả, không trả JSON."
    return LLMResult(noi_dung, request["provider"], request["model"], "gia-lap-trich-xuat-v1", {}, "stop")
