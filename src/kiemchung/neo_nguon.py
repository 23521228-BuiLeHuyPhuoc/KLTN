"""Neo nguồn của bước trích xuất P (Bước 22, T5.3 khâu b): Python kiểm từng trường LLM trích xem có thật trong nguồn.

Nguồn là chữ tuyên bố (phía tuyên bố) hoặc văn bản đoạn có mã ma_doan (phía tài liệu). Mọi so khớp chuỗi đi qua
chuan_so_khop (mục 5 của luan_van/buoc22_thiet_ke_trich_xuat.md): NFC, chữ thường, dấu câu và ký hiệu thành khoảng trắng,
khoảng trắng gộp một dấu cách, dấu chấm và phẩy giữa hai chữ số giữ nguyên; kèm bản đồ vị trí về chuỗi gốc để đoạn khớp
tìm được dòng chứa nó (kiểm tra đầy đủ chỉ dò trong dòng của giá trị).

Hàm thuần: nhận chuỗi, dict đã đọc và cấu hình, trả kết quả; không gọi LLM, không đọc tệp.

Kiểu dữ liệu của một mục trước khi neo (do trich_xuat.doc_luoc_do dựng): dict có
    san_pham   {"chu", "trich"} hoặc None
    gia_tri    {"chu", "don_vi", "trich"} hoặc None
    dieu_kien  [{"i", "loai", "cum", "trich"}] (i là chỉ số trong danh sách LLM trả, giữ để báo lý do)
Sau neo_nguon_muc, gia_tri (nếu còn) có thêm "gia_tri" (số thực, {"bui", "nuoc"} hoặc "khong") và "khoa_don_vi".
"""
import unicodedata

from .chuan_hoa import bang_nhau, chuan_don_vi, doc_iso_22810, doc_so, tach_ip, tim_gia_tri, tim_so

LY_DO_DOAN_NGOAI_TOP_K = "doan_ngoai_top_k"
LY_DO_TRICH = "trich_khong_co_trong_nguon"
LY_DO_SO = "so_khong_khop"
LY_DO_DON_VI = "don_vi_khong_khop"
LY_DO_MA = "ma_khong_khop"
LY_DO_CUM = "cum_khong_trong_trich"
LY_DO_TEN = "ten_khong_trong_trich"
PHU_DINH = "khong"        # giá trị phủ định ghi vào bộ thông số
CHU_KHONG = "không"       # chữ trong văn bản; LLM có thể ghi "khong" không dấu
KHANG_DINH = "co"          # kháng nước khẳng định không kèm mã ("Hộp sạc cũng kháng nước"); chỉ thuộc tính khang_nuoc
TU_KHANG_DINH_CO = ("có", "co")
THUOC_TINH_CO_KHONG = "khang_nuoc"
CUM_PHU_DINH = ("kháng nước", "chống nước")   # mục 5: chữ đi cùng "không" ở câu trích của giá trị phủ định


def chuan_so_khop(chu):
    """(chuỗi chuẩn hóa, bản đồ): bản đồ[i] là chỉ số trong chuỗi gốc của ký tự (hay cụm ký tự gộp) sinh ra ký tự i.

    NFC theo từng cụm (chữ cái và dấu rời đi sau nó) để chỉ số vẫn là của chuỗi gốc; chữ thường; ký tự khoảng trắng
    (gồm U+202F, U+00A0, xuống dòng), dấu câu và ký hiệu (nhóm Unicode P và S: "/", ":", ngoặc, gạch nối các kiểu, dấu
    nháy, "%", "+") thành khoảng trắng; dãy khoảng trắng gộp một dấu cách có chỉ số của ký tự đầu dãy; bỏ khoảng trắng
    đầu và cuối. Dấu "." và "," có chữ số ngay trước và ngay sau trong chuỗi gốc ("3.000", "4,5") giữ nguyên."""
    ra, ban_do = [], []
    i, n = 0, len(chu)
    while i < n:
        j = i + 1
        while j < n and unicodedata.combining(chu[j]):
            j += 1
        cum = unicodedata.normalize("NFC", chu[i:j]).lower()
        giua_hai_so = (cum in ".,") and i > 0 and j < n and chu[i - 1].isdecimal() and chu[j].isdecimal()
        for c in cum:
            if not giua_hai_so and (c.isspace() or unicodedata.category(c)[0] in "PS"):
                if ra and ra[-1] != " ":
                    ra.append(" ")
                    ban_do.append(i)
            else:
                ra.append(c)
                ban_do.append(i)
        i = j
    if ra and ra[-1] == " ":
        ra.pop()
        ban_do.pop()
    return "".join(ra), ban_do


def _cuoi_goc(nguon, chi_so):
    """Chỉ số ngay sau ký tự gốc ở chi_so (kể cả dấu rời đi sau nó)."""
    j = chi_so + 1
    while j < len(nguon) and unicodedata.combining(nguon[j]):
        j += 1
    return j


def tim_trich(nguon, trich):
    """Mọi chỗ câu trích có trong nguồn (so sau chuan_so_khop): [(đầu, cuối)] là chỉ số trong nguồn gốc, theo thứ tự
    xuất hiện. Câu trích rỗng sau chuẩn hóa (chỉ có dấu câu) không khớp chỗ nào."""
    nt, _ = chuan_so_khop(trich)
    if not nt:
        return []
    ns, ban_do = chuan_so_khop(nguon)
    ket_qua, tu = [], 0
    while True:
        i = ns.find(nt, tu)
        if i < 0:
            return ket_qua
        j = i + len(nt)
        ket_qua.append((ban_do[i], _cuoi_goc(nguon, ban_do[j - 1])))
        tu = i + 1


def co_trong_nguon(nguon, trich):
    return bool(tim_trich(nguon, trich))


def la_chuoi_con(cum, trich):
    """cum là chuỗi con của trich sau chuan_so_khop (cum rỗng sau chuẩn hóa thì không)."""
    nc, _ = chuan_so_khop(cum)
    return bool(nc) and nc in chuan_so_khop(trich)[0]


def _gop(chu):
    """Gộp mọi khoảng trắng (kể cả xuống dòng) thành một dấu cách: chữ dọc "Đến\\n7\\n/\\n30\\ngiờ" thành một dòng."""
    return " ".join(chu.split())


# --- Giá trị ---

def don_vi_cua_thuoc_tinh(thuoc_tinh_yaml, chung):
    """Khóa chuan_hoa.don_vi của thuộc tính (don_vi trong YAML nhóm), hoặc None khi không phải một khóa đơn vị
    ("ma_ip", "phut_hoac_gio")."""
    khoa = (thuoc_tinh_yaml or {}).get("don_vi")
    return khoa if khoa in chung["chuan_hoa"]["don_vi"] else None


def doc_gia_tri(chu, don_vi, chung, thuoc_tinh=None):
    """Đọc trường giá trị LLM trả, chưa so với câu trích: (loại, giá trị, khóa đơn vị) hoặc ValueError.

    loại là "phu_dinh" ("không" -> "khong"), "co" (chỉ thuộc tính khang_nuoc: chu "có" hoặc rỗng -> "co"), "ip" ({"bui", "nuoc"}), "iso" (số mét, đơn vị m) hoặc "so" (doc_so, đơn vị là
    chuan_don_vi(don_vi) hay None khi don_vi null). Thứ tự thử: phủ định, mã IP, mã ISO 22810, số."""
    c = chu.strip()
    if c.casefold() in (CHU_KHONG, PHU_DINH):
        return "phu_dinh", PHU_DINH, None
    if thuoc_tinh == THUOC_TINH_CO_KHONG and (not c or c.casefold() in TU_KHANG_DINH_CO):
        return "co", KHANG_DINH, None
    ip = tach_ip(c)
    if ip is not None:
        return "ip", {"bui": ip.bui, "nuoc": ip.nuoc}, None
    met = doc_iso_22810(c, chung)
    if met is not None:
        return "iso", met, "m"
    so = doc_so(c)
    khoa = None
    if don_vi is not None:
        khoa = chuan_don_vi(don_vi, chung)
        if khoa is None:
            raise ValueError(f"đơn vị không biết: {don_vi!r}")
    return "so", so, khoa


def _kiem_so(so, don_vi, trich, chung, khoa_tt):
    """(khóa đơn vị, None) hoặc (None, lý do) cho giá trị số: con số có trong câu trích, đơn vị đi cùng con số đó.

    Dòng không ghi đơn vị (Buds3 Pro #044 "Lên đến 6") đạt khi don_vi là null hoặc đúng đơn vị của thuộc tính; đơn vị
    của giá trị khi đó lấy theo thuộc tính. Dạng "a / b <đơn vị>" do tim_gia_tri đọc, cả a và b đều đạt."""
    tr = _gop(trich)
    if not any(bang_nhau(so, s.so) for s in tim_so(tr)):
        return None, LY_DO_SO
    cung_so = [g for g in tim_gia_tri(tr, chung) if bang_nhau(so, g.so)]
    if don_vi is None:
        return (cung_so[0].don_vi if cung_so else khoa_tt), None
    khoa = chuan_don_vi(don_vi, chung)
    if khoa is None:
        return None, LY_DO_DON_VI
    if any(g.don_vi == khoa for g in cung_so) or (not cung_so and khoa == khoa_tt):
        return khoa, None
    return None, LY_DO_DON_VI


def _co_khang_dinh_nuoc(nt):
    """Chuỗi đã chuan_so_khop có "kháng nước" hay "chống nước" mà không có "không" đứng trước cụm đó."""
    vi_tri = [i for i in (nt.find(c) for c in CUM_PHU_DINH) if i >= 0]
    return bool(vi_tri) and f" {CHU_KHONG} " not in f" {nt[:min(vi_tri)]} "


def kiem_gia_tri(gia_tri, chung, khoa_tt, thuoc_tinh=None):
    """Kiểm một giá trị với câu trích của nó (mục 5): trả {"gia_tri", "khoa_don_vi"} hoặc lý do bị bỏ (chuỗi).

    Số: so_khong_khop, don_vi_khong_khop. Mã: IP bằng IP, ISO 22810 bằng ISO 22810, phủ định "không" cùng "kháng nước"
    hay "chống nước" trong câu trích; khang_nuoc khẳng định ("có"): câu trích có "kháng nước" hay "chống nước" và không
    có "không" đứng trước cụm đó; không khớp thì ma_khong_khop. Số không đọc được thì so_khong_khop."""
    trich = _gop(gia_tri["trich"])
    try:
        loai, gt, khoa = doc_gia_tri(gia_tri["chu"], gia_tri["don_vi"], chung, thuoc_tinh)
    except ValueError:
        return LY_DO_DON_VI if gia_tri["don_vi"] is not None and _la_so(gia_tri["chu"]) else LY_DO_SO
    if loai == "ip":
        khop = tach_ip(trich) == tach_ip(gia_tri["chu"])
    elif loai == "iso":
        khop = doc_iso_22810(trich, chung) == gt
    elif loai == "co":
        khop = _co_khang_dinh_nuoc(chuan_so_khop(trich)[0])
    elif loai == "phu_dinh":
        nt, _ = chuan_so_khop(trich)
        khop = f" {CHU_KHONG} " in f" {nt} " and any(c in nt for c in CUM_PHU_DINH)
    else:
        khoa, ly_do = _kiem_so(gt, gia_tri["don_vi"], trich, chung, khoa_tt)
        return ly_do if ly_do else {"gia_tri": gt, "khoa_don_vi": khoa}
    return {"gia_tri": gt, "khoa_don_vi": khoa} if khop else LY_DO_MA


def _la_so(chu):
    try:
        doc_so(chu)
    except ValueError:
        return False
    return True


# --- Một mục ---

def neo_nguon_muc(muc, nguon, chung, khoa_tt, kiem_nguon=True, thuoc_tinh=None):
    """Neo nguồn cho một mục (tuyên bố hoặc mục tài liệu): (mục mới, [(trường, lý do)]).

    nguon: chữ nguồn của mục (tuyên bố hoặc văn bản đoạn); None thì mọi câu trích coi như không kiểm được nguồn (dùng
    cho mục có ma_doan ngoài top-k khi kiem_nguon=False). kiem_nguon=False (P−NN, mục 9): không bỏ trường nào vì câu trích;
    gia_tri vẫn đọc thẳng bằng doc_gia_tri (số không đọc được thì vẫn bỏ, lý do so_khong_khop, vì không có số để giữ).
    Không sửa muc; trường bị bỏ là gia_tri (None), san_pham (None) hoặc một điều kiện (rút khỏi danh sách)."""
    moi = {"san_pham": muc.get("san_pham"), "gia_tri": None, "dieu_kien": []}
    bi_loai = []

    sp = muc.get("san_pham")
    if sp is not None and kiem_nguon:
        if not co_trong_nguon(nguon or "", sp["trich"]):
            moi["san_pham"] = None
            bi_loai.append(("san_pham", LY_DO_TRICH))
        elif not la_chuoi_con(sp["chu"], sp["trich"]):
            moi["san_pham"] = None
            bi_loai.append(("san_pham", LY_DO_TEN))

    gt = muc.get("gia_tri")
    if gt is not None:
        if kiem_nguon and not co_trong_nguon(nguon or "", gt["trich"]):
            bi_loai.append(("gia_tri", LY_DO_TRICH))
        elif kiem_nguon:
            kq = kiem_gia_tri(gt, chung, khoa_tt, thuoc_tinh)
            if isinstance(kq, str):
                bi_loai.append(("gia_tri", kq))
            else:
                moi["gia_tri"] = {**gt, **kq}
        else:
            try:
                loai, so, khoa = doc_gia_tri(gt["chu"], gt["don_vi"], chung, thuoc_tinh)
            except ValueError:
                bi_loai.append(("gia_tri", LY_DO_SO))
            else:
                moi["gia_tri"] = {**gt, "gia_tri": so, "khoa_don_vi": khoa if khoa or loai != "so" else khoa_tt}

    for dk in muc.get("dieu_kien") or []:
        truong = f"dieu_kien[{dk['i']}]"
        if kiem_nguon and not co_trong_nguon(nguon or "", dk["trich"]):
            bi_loai.append((truong, LY_DO_TRICH))
        elif kiem_nguon and not la_chuoi_con(dk["cum"], dk["trich"]):
            bi_loai.append((truong, LY_DO_CUM))
        else:
            moi["dieu_kien"].append(dk)
    return moi, bi_loai
