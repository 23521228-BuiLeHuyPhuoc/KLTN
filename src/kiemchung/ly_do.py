"""Sinh lý do từ dấu vết của bộ quyết định (Bước 27, T5.6, đặc tả mục 9).

Tám mẫu câu cố định của T5.6 (bảng ở HD mục 8); lý do luôn khớp nhãn vì sinh từ cùng dấu vết `vet` mà quyet_dinh trả. Tên điều kiện và
giá trị in bằng chữ tiếng Việt: giá trị lấy cụm đầu (tu_tai_lieu, rồi hieu_biet_chung) của cach_dien_dat; tên thuộc tính và tên điều
kiện dạng số là bảng ngắn bên dưới (mô tả của Bước 22 là câu hỏi dài, không chèn được vào câu lý do).
"""
import re

TRONG_HOP = "chi_do_trong_hop"
TEN_THUOC_TINH = {
    "thoi_luong_pin": "thời lượng pin", "sac_nhanh": "sạc nhanh", "cong_suat_sac": "công suất sạc", "do_sang": "độ sáng",
    "tan_so_quet": "tần số quét", "zoom": "zoom", "khang_nuoc": "kháng nước", "dung_luong_pin": "dung lượng pin",
}
TEN_DIEU_KIEN = {
    "bo_tiep_hop": "bộ tiếp hợp", "moc_phan_tram": "mốc phần trăm", "so_phut_sac": "số phút sạc", "do_sau": "độ sâu",
    "thoi_gian_ngam": "thời gian ngâm", "dien_tich_do": "diện tích đo", "chenh_lech_nhiet_do": "chênh lệch nhiệt độ",
    "che_do_hien_thi": "chế độ hiển thị", "kieu_gia_tri": "kiểu giá trị",
}
DON_VI = {"phan_tram": "%", "W": "W", "m": " m", "phut": " phút", "gio": " giờ", "K": "K", "nit": " nit", "mAh": "mAh", "Hz": "Hz", "x": "x"}
TEN_KIEU = {"toi_da": "tối đa (lên đến)", "dien_hinh": "điển hình", "dinh_muc": "định mức", "thich_ung": "thích ứng",
            "khang_dinh": "mức chắc chắn đạt"}
HAU_TO_QUAN_HE = {"tuyen_bo_lon_hon_hoac_bang": " trở lên", "tuyen_bo_nho_hon_hoac_bang": " trở xuống"}
MAU_CAU = {
    "D1": "Tài liệu của ", "D1a": "Chưa xác định được điều kiện của tuyên bố: ", "D1b": "Tài liệu ghi hai giá trị khác nhau cho ",
    "D2": "Tài liệu ghi mức tối đa: ", "D3": "Khớp với tài liệu: ", "D4": "Giá trị ", "D5": "Tài liệu ghi ",
    "D6": "Tài liệu không công bố ",
}


def dinh_dang_so(g):
    """Số hoặc mã ở dạng in được: 26, 4.5, IP57, "không", "có"."""
    if isinstance(g, dict):
        return "IP" + "".join("X" if g.get(k) is None else str(g[k]) for k in ("bui", "nuoc"))
    if isinstance(g, str):
        return g
    return f"{g:g}"


def _gia_tri(g, don_vi):
    if g == "khong":
        return "không kháng nước"
    if g == "co":
        return "có kháng nước"
    return dinh_dang_so(g) + (DON_VI.get(don_vi, f" {don_vi}") if don_vi and not isinstance(g, (dict, str)) else "")


def ten_hien_thi(cau_hinh, c, v):
    """Chữ in của (điều kiện c, giá trị chuỗi v): cụm đầu của giá trị trong cach_dien_dat, bỏ ngoặc."""
    if v == TRONG_HOP:
        return "chỉ có đồ trong hộp"
    kb = ((cau_hinh.get("cach_dien_dat") or {}).get(c) or {}).get(v) or {}
    for khoa in ("tu_tai_lieu", "hieu_biet_chung"):
        for cum in kb.get(khoa) or []:
            cum = " ".join(re.sub(r"[()]", " ", cum).split())
            if cum:
                return cum if any(sum(ch.isupper() for ch in w) >= 2 for w in cum.split()) else cum.lower()
    return str(v).replace("_", " ")


def mo_ta_dieu_kien(cau_hinh, c, v, phia="tuyen_bo"):
    """Mô tả một điều kiện; phia = tai_lieu thì điều kiện dạng số thêm "trở lên"/"trở xuống" theo quan hệ."""
    if c == "dieu_kien_khac":
        return f"“{v}”" if v else "không nêu"
    if c == "kieu_gia_tri":
        return "kiểu " + TEN_KIEU.get(v, str(v))
    ten = TEN_DIEU_KIEN.get(c, c.replace("_", " "))
    if v is None:
        return f"không nêu {ten}"
    if isinstance(v, dict):
        thoa = None
        for tt in (cau_hinh.get("thuoc_tinh") or {}).values():
            if c in (tt.get("dieu_kien_so") or {}):
                thoa = tt["dieu_kien_so"][c]["thoa_khi"]
        hau = HAU_TO_QUAN_HE.get(thoa, "") if phia == "tai_lieu" else ""
        return f"{ten} {v['so']:g}{DON_VI.get(v.get('don_vi'), ' ' + str(v.get('don_vi')))}{hau}"
    return ten_hien_thi(cau_hinh, c, v)


def _dieu_kien_tb(kq, cau_hinh):
    vet = kq["vet"]
    thu_tu = list((cau_hinh["thuoc_tinh"].get(vet.get("thuoc_tinh")) or {}).get("dieu_kien_bat_buoc") or {})
    dk = vet.get("dieu_kien_tuyen_bo") or {}
    ds = [mo_ta_dieu_kien(cau_hinh, c, dk[c]) for c in sorted(dk, key=lambda x: thu_tu.index(x) if x in thu_tu else 99)]
    return ", ".join(ds) if ds else "điều kiện của tuyên bố"


def sinh_ly_do(kq, cau_hinh):
    """Lý do một câu theo dòng D của kq["dong_d"], từ kq["vet"]. Cấu trúc câu giữ đúng mẫu T5.6; phần thêm (bỏ "lên đến", so thẳng)
    nằm cuối câu."""
    vet, dong = kq["vet"], kq["dong_d"]
    tt = TEN_THUOC_TINH.get(vet.get("thuoc_tinh"), str(vet.get("thuoc_tinh")))
    if dong == "D1":
        return f"Tài liệu của {vet.get('san_pham')} không có thông số {tt}."
    if dong == "D1a":
        nn = vet.get("nguyen_nhan") or {}
        if nn.get("loai") == "mac_dinh":
            cum = ", ".join(TEN_DIEU_KIEN.get(c, c.replace("_", " ")) for c in nn["khoa"])
        elif nn.get("loai") == "trich_xuat_that_bai":
            cum = "chưa trích được thông số của tuyên bố"
        else:
            cum = nn.get("cum")
        return f"Chưa xác định được điều kiện của tuyên bố: “{cum}”."
    gt_tb = vet["tuyen_bo"]
    if dong == "D1b":
        t = [m["trich"] for m in vet["mau_thuan"][:2]]
        return f"Tài liệu ghi hai giá trị khác nhau cho {tt} ở {_dieu_kien_tb(kq, cau_hinh)}: “{t[0]}” và “{t[1]}”."
    if dong == "D2":
        return f"Tài liệu ghi mức tối đa: “{vet['trich_chinh']}”; tuyên bố viết thành mức chắc chắn đạt."
    if dong == "D3":
        them = ""
        if vet.get("bo_len_den"):
            them += f" ({cau_hinh['chung'].get('ghi_chu_bo_len_den', 'quảng cáo bỏ "lên đến"')})"
        s = f"Khớp với tài liệu: “{vet['trich_chinh']}”.{them}"
        return s + (" Tài liệu không nêu điều kiện." if vet.get("so_thang") else "")
    if dong == "D4":
        kb = vet["khac_biet"]
        u = vet["u"]
        tl = " và ".join(mo_ta_dieu_kien(cau_hinh, d["dk"], d["tai_lieu"], "tai_lieu") if d["tai_lieu"] is not None
                         else f"{TEN_DIEU_KIEN.get(d['dk'], d['dk'])} như hãng công bố" for d in kb)
        ro = [mo_ta_dieu_kien(cau_hinh, d["dk"], d["tuyen_bo"]) for d in kb if d["nguon"] != "mac_dinh"]
        md = [mo_ta_dieu_kien(cau_hinh, d["dk"], d["tuyen_bo"]) if d["tuyen_bo"] is not None else "không nêu điều kiện lạ"
              for d in kb if d["nguon"] == "mac_dinh"]
        phan = []
        if ro:
            phan.append("nêu " + ", ".join(ro))
        if md:
            phan.append("được hiểu là " + ", ".join(md))
        return (f"Giá trị {_gia_tri(u['gia_tri'], u.get('don_vi'))} chỉ đạt khi {tl}; tuyên bố {' và '.join(phan)}. "
                f"Nguồn: “{vet['trich_chinh']}”.")
    if dong == "D5":
        u = vet["u"]
        return (f"Tài liệu ghi {_gia_tri(u['gia_tri'], u.get('don_vi'))} ở {_dieu_kien_tb(kq, cau_hinh)}; "
                f"tuyên bố ghi {_gia_tri(gt_tb['gia_tri'], gt_tb.get('don_vi'))}.")
    return f"Tài liệu không công bố {tt} ở {_dieu_kien_tb(kq, cau_hinh)}."
