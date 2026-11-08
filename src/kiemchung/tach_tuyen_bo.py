"""Câu lệnh chép nguyên văn đặc tả Bước 29–30."""
from collections import Counter
from dataclasses import asdict
import json
import unicodedata

from .chuan_hoa import tim_gia_tri, tach_ip, doc_iso_22810, bang_nhau, quy_doi
from .trich_xuat import TEN_NHOM, bang_thuoc_tinh, lay_cau_hinh, nhom_cua_mau
from .doi_chung.b0 import _doc_json
from .doi_chung.chung import goi, thay_mot_luot
from .llm import LLMResult

CAU_LENH_TACH = """Tách bài quảng cáo về {ten_nhom} dưới đây thành các tuyên bố về thông số kỹ thuật. Không phán đúng sai.

QUY TẮC
1. Mỗi tuyên bố chỉ có một thuộc tính và một con số (hoặc một mã như IP68). Câu "pin 30 giờ, sạc 50% trong 20 phút" tách thành 2 tuyên bố.
2. Giữ ngữ cảnh: viết thành một câu ngắn gồm tên sản phẩm, thuộc tính, con số và điều kiện, đúng như bài nói. Thay "máy", "tai nghe này" bằng tên sản phẩm. Điều kiện thuộc con số thì đưa vào tuyên bố, kể cả khi nằm ở câu trước hay câu sau.
3. Điều kiện thuộc con số khi: bổ nghĩa trực tiếp cho con số (cùng cụm, trong ngoặc ngay sau con số, hoặc "khi / ở / với / trong / dưới / cùng / kèm …" đi liền con số); hoặc là điều kiện cụ thể ở vế nói tác dụng của chính con số ("… 2500 nit giúp nhìn rõ dưới nắng"). Điều kiện hay từ khẳng định ở vế nói về tính năng hay việc khác thì không thuộc con số.
4. Không thêm điều kiện bài không nói, không sửa con số. Giữ chữ "lên đến" nếu bài có. Từ khẳng định ("luôn", "đảm bảo", "ít nhất", "mọi lúc", "hơn", "trên", "không dưới", "trở lên") chỉ giữ khi gắn với con số.
5. Hai lần nhắc trong cùng bài chỉ gộp làm một khi cùng con số và cùng điều kiện. Một con số nhắc hai lần, một lần kèm điều kiện, một lần không, thì là hai tuyên bố.

CHỈ TÁCH CÁC THUỘC TÍNH SAU
{bang_thuoc_tinh}

BỎ QUA
Kích thước, trọng lượng, Bluetooth, chip, số chấm camera (48MP), giá, khuyến mãi, quà tặng, số đánh giá sao, số người dùng, so sánh với máy khác, câu khen không có con số ("pin trâu", "dùng cả ngày"). Cụm khen đứng cạnh một con số ("cả ngày", "suốt ngày dài", "không lo hết pin", "siêu bền", "bền bỉ", "vượt trội", "tuyệt đối", "trọn vẹn", "không giới hạn") cũng bỏ khỏi tuyên bố.

ĐẦU RA
Trả về đúng một danh sách JSON, không thêm chữ nào khác. Mỗi phần tử: {"tuyen_bo": "<câu ngắn>", "cau_goc": "<câu hoặc vế câu chứa con số, chép nguyên văn từ bài>", "thuoc_tinh_du_kien": "<mã thuộc tính>"}. Bài không có tuyên bố nào thì trả [].

VÍ DỤ
- cau_goc "nghe nhạc liền 7 tiếng ngay cả khi bật chống ồn" -> {"tuyen_bo": "Galaxy Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn", "thuoc_tinh_du_kien": "thoi_luong_pin"}
- cau_goc "sạc nhanh 60% chỉ trong 25 phút" -> {"tuyen_bo": "Điện thoại A sạc 60% trong 25 phút", "thuoc_tinh_du_kien": "sac_nhanh"}
- cau_goc "Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin" -> {"tuyen_bo": "Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin", "thuoc_tinh_du_kien": "thoi_luong_pin"}
- cau_goc "Màn hình Điện thoại A sáng 2500 nit, giúp bạn nhìn rõ dưới nắng" -> {"tuyen_bo": "Điện thoại A sáng 2500 nit dưới nắng", "thuoc_tinh_du_kien": "do_sang"}

BÀI QUẢNG CÁO
{bai}"""


def _gon(chu):
    return " ".join(unicodedata.normalize("NFC", chu).split())


def ghep_cau_lenh(bai, nhom, cau_hinh):
    """Điền nhóm, bảng thuộc tính và nguyên văn bài trong một lượt."""
    return thay_mot_luot(CAU_LENH_TACH, {"{ten_nhom}": TEN_NHOM[nhom],
                         "{bang_thuoc_tinh}": bang_thuoc_tinh(nhom, cau_hinh), "{bai}": bai["noi_dung"]})


def doc_gia_tri_tuyen_bo(tuyen_bo, thuoc_tinh, cau_hinh):
    """Đọc giá trị đầu tiên đúng đơn vị; trả {gia_tri, don_vi} hoặc None.

    Đơn vị phut_hoac_gio quy về phút. Kháng nước đồng hồ vẫn nhận mã IP;
    số mét và mã IP có khóa đơn vị riêng nên không ghép nhầm với nhau.
    """
    tt = cau_hinh["thuoc_tinh"].get(thuoc_tinh)
    if tt is None:
        return None
    chu, chung = _gon(tuyen_bo), cau_hinh["chung"]
    dv = tt["don_vi"]
    if thuoc_tinh == "khang_nuoc":
        ip = tach_ip(chu)
        if ip is not None:
            return {"gia_tri": asdict(ip), "don_vi": "ma_ip"}
        iso = doc_iso_22810(chu, chung)
        if iso is not None:
            return {"gia_tri": iso, "don_vi": "m"}
    dv = "phut" if dv == "phut_hoac_gio" else dv
    for gt in tim_gia_tri(chu, chung):
        if gt.don_vi == dv or {gt.don_vi, dv} == {"gio", "phut"}:
            return {"gia_tri": quy_doi(gt.so, gt.don_vi, dv), "don_vi": dv}
    return None


def tach_bai(client, mo_hinh, bai, max_token_ra=4096):
    """Tách một bài; trả danh sách tuyên bố, số bị lọc và lỗi ở cấp bài."""
    nhom = nhom_cua_mau(bai["ma_mau"])
    cfg = lay_cau_hinh(nhom)
    kq = goi(client, mo_hinh, ghep_cau_lenh(bai, nhom, cfg), max_token_ra)
    kq.update(ma_qc=bai["ma_qc"], ma_mau=bai["ma_mau"], tuyen_bo=[], bi_loc={})
    if kq["loi"]:
        return kq
    ds, loi = _doc_json(kq["tra_ve_tho"])
    if loi or not isinstance(ds, list):
        kq["loi"] = loi or "json_khong_phai_danh_sach"
        return kq
    dem = Counter()
    for d in ds:
        if not isinstance(d, dict) or any(not isinstance(d.get(k), str) or not d[k].strip()
                                        for k in ("tuyen_bo", "cau_goc", "thuoc_tinh_du_kien")):
            dem["sai_luoc_do"] += 1
            continue
        tt = d["thuoc_tinh_du_kien"]
        if tt not in cfg["thuoc_tinh"]:
            dem["thuoc_tinh_ngoai_nhom"] += 1
            continue
        kq["tuyen_bo"].append({"ma_qc": bai["ma_qc"], "ma_mau": bai["ma_mau"],
            "tuyen_bo": d["tuyen_bo"], "cau_goc": d["cau_goc"], "thuoc_tinh_du_kien": tt,
            "cau_goc_khong_khop": _gon(d["cau_goc"]) not in _gon(bai["noi_dung"]),
            "gia_tri": doc_gia_tri_tuyen_bo(d["tuyen_bo"], tt, cfg), "nhom": nhom,
            "che_do": bai.get("che_do"),
            "llm_sinh": bai.get("llm_sinh") or bai.get("mo_hinh_nha_cung_cap") or bai.get("mo_hinh")})
    kq["bi_loc"] = dict(dem)
    return kq


def _thuoc_tinh(d):
    return d.get("thuoc_tinh_du_kien", d.get("thuoc_tinh"))


def _gia_tri(d):
    if "gia_tri" in d:
        return d["gia_tri"]
    cfg = lay_cau_hinh(nhom_cua_mau(d["ma_mau"]))
    return doc_gia_tri_tuyen_bo(d["tuyen_bo"], _thuoc_tinh(d), cfg)


def _bang(a, b):
    if a is None or b is None or a["don_vi"] != b["don_vi"]:
        return False
    x, y = a["gia_tri"], b["gia_tri"]
    return x == y if isinstance(x, dict) or isinstance(y, dict) else bang_nhau(x, y)


def ghep(tu_dong, tach_tay):
    """Trả các cặp chỉ số (tự động, tách tay), tham lam một đối một trong mỗi bài."""
    gt_td, gt_tay = [_gia_tri(d) for d in tu_dong], [_gia_tri(d) for d in tach_tay]
    da_ghep, cap = set(), []
    for i, a in enumerate(tu_dong):
        for j, b in enumerate(tach_tay):
            if (j not in da_ghep and a["ma_qc"] == b["ma_qc"] and _thuoc_tinh(a) == _thuoc_tinh(b)
                    and _bang(gt_td[i], gt_tay[j])):
                da_ghep.add(j)
                cap.append((i, j))
                break
    return cap


def thong_ke(tu_dong, tach_tay):
    """Precision/Recall của phép tách; không đọc hay đánh giá nhãn kiểm chứng."""
    cap = ghep(tu_dong, tach_tay)
    du_dk = [(a, b) for a, b in cap if "dieu_kien" in tu_dong[a] and "dieu_kien" in tach_tay[b]]
    cung = sum(tu_dong[a]["dieu_kien"] == tach_tay[b]["dieu_kien"] for a, b in du_dk)
    return {"so_tu_dong": len(tu_dong), "so_tach_tay": len(tach_tay), "so_cap": len(cap),
            "precision": len(cap) / len(tu_dong) if tu_dong else None,
            "recall": len(cap) / len(tach_tay) if tach_tay else None,
            "so_cap_co_dieu_kien": len(du_dk), "so_cap_cung_dieu_kien": cung,
            "ty_le_cung_dieu_kien": cung / len(du_dk) if du_dk else None}


def gia_transport(request, timeout_s):
    """LLM giả trả một tuyên bố tự đặt để thử toàn bộ đường xử lý."""
    ds = [{"tuyen_bo": "Máy A dùng pin 6 giờ", "cau_goc": "pin 6 giờ",
           "thuoc_tinh_du_kien": "thoi_luong_pin"}]
    return LLMResult(json.dumps(ds, ensure_ascii=False), request["provider"], request["model"], "gia-tach-v1", {}, "stop")
