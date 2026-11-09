"""Bộ quyết định A–D của P (Bước 27, T5.5, T5.9).

Cài đúng luan_van/buoc27_thiet_ke_quyet_dinh.md (gọi tắt "đặc tả") và hướng dẫn gán nhãn mục 5–8 (gọi tắt "HD"). Hàm thuần: nhận bản ghi
trích xuất (định dạng mục 8 của luan_van/buoc22_thiet_ke_trich_xuat.md) và cấu hình nhóm, trả dict nhãn; không gọi LLM, không đọc
nguồn. Không import module trích xuất. Điều kiện của một mục là dict {tên: giá trị}; điều kiện dạng số là {"so", "don_vi"}.

Mỗi hàm con ghi mục đặc tả và mục HD nó cài. Chỗ đặc tả để máy cần luật cụ thể đánh dấu [luật cài] ở đặc tả; chỗ đặc tả chưa đủ và
bản cài phải tự quyết thì ghi "[tự quyết]" trong docstring.
"""
import functools
import json
import re
import unicodedata

from .cau_hinh import chuan_hoa_chu, doc_mau, thoa_dieu_kien_so
from .chuan_hoa import MaIP, nguong_bang, quy_doi, so_huong, so_ip, tim_gia_tri, tim_san_pham, tim_so
from . import ly_do as _ly_do

DUNG, SAI, LECH, CHUA_DU = "DUNG", "SAI", "LECH", "CHUA_DU"
TRONG_HOP = "chi_do_trong_hop"   # điều kiện khong_mua_them: chỉ có đồ trong hộp
NGUONG_QD8 = 0.25                # HD mục 11.2: không đổi sau khi đếm
KIEU_RO = ("toi_da", "dien_hinh", "dinh_muc", "thich_ung")
# Cùng biểu thức với scripts/ra_tach.py CUM_PHU (tests/test_quyet_dinh.py kiểm hai bên giống nhau).
CUM_PHU = {
    "mọi điều kiện X": r"mọi điều kiện(?:\s+[^\s,.;:!?]+){0,2}",
    "mọi chế độ": r"mọi chế độ",
    "mọi hoạt động": r"mọi hoạt động(?:\s+[^\s,.;:!?]+){0,3}",
    "bất kể X": r"bất kể(?:\s+[^\s,.;:!?]+){1,3}",
    "dù A hay B": r"dù\s+(?:[^\s,.;:!?]+\s+){1,4}?hay(?:\s+[^\s,.;:!?]+){1,3}",
    "cho cả A và B": r"cho cả\s+(?:[^\s,.;:!?]+\s+){1,4}?và(?:\s+[^\s,.;:!?]+){1,3}",
}


# --- Tiện ích chữ ---

def chuan_cum(chu):
    """Chữ thường, NFC, dấu câu và ký hiệu thành khoảng trắng, gộp khoảng trắng (cùng tinh thần chuan_so_khop của neo nguồn)."""
    chu = unicodedata.normalize("NFC", chu or "").lower()
    chu = "".join(" " if (c.isspace() or unicodedata.category(c)[0] in "PS") else c for c in chu)
    return " ".join(chu.split())


def chua_cum(van_ban, cum):
    """van_ban (đã chuan_cum) chứa cum (đã chuan_cum) như một cụm liền, có ranh giới chữ."""
    return bool(cum) and re.search(r"(?<!\w)" + re.escape(cum) + r"(?!\w)", van_ban) is not None


def _khoa_ma(ma_doan):
    """Khóa sắp theo mã đoạn: (mẫu, số)."""
    mau, _, so = (ma_doan or "").rpartition("#")
    return (mau, int(so) if so.isdigit() else 0)


@functools.lru_cache(maxsize=1)
def _bang_hang():
    return {r["ma_mau"]: r["hang"] for r in doc_mau()}


# --- Bối cảnh ---

class BoiCanh:
    """Dữ liệu cố định của một lần quyết định: thuộc tính, bảng điều kiện, hãng, dạng sạc nhanh của đồng hồ."""

    def __init__(self, ban_ghi, cau_hinh):
        self.cau_hinh = cau_hinh
        self.chung = cau_hinh["chung"]
        self.tb = ban_ghi["tuyen_bo"]
        self.ma_mau = ban_ghi["ma_mau"]
        self.chu = ban_ghi.get("chu_tuyen_bo") or ""
        self.ten_tt = self.tb["thuoc_tinh"]
        self.tt = cau_hinh["thuoc_tinh"][self.ten_tt]
        self.dk_bb = self.tt.get("dieu_kien_bat_buoc") or {}
        self.htt = self.tt.get("hieu_thong_thuong") or {}
        self.so = self.tt.get("dieu_kien_so") or {}
        self.cach = cau_hinh.get("cach_dien_dat") or {}
        self.dac_biet = set(self.chung["hieu_thong_thuong_dac_biet"])
        self.nguong = nguong_bang(self.chung)
        self.hang = ban_ghi.get("hang") or _bang_hang().get(self.ma_mau)
        self.dang = None
        self.huong = self.tt["huong_thuan_loi"]
        if self.tt["don_vi"] == "phut_hoac_gio":   # đặc tả mục 2.4
            self.dang = {"phut": 1, "gio": 2}.get(self.tb.get("don_vi"))
            if self.huong == "theo_dang":
                self.huong = "thap_hon_tot_hon" if self.dang == 1 else "cao_hon_tot_hon"


class DieuKien:
    """Điều kiện của tuyên bố sau bước B: gia_tri {tên: giá trị}, nguon {tên: neu_ro | cum_phu | chep_nhan | mac_dinh}."""

    def __init__(self):
        self.gia_tri, self.nguon = {}, {}

    def dat(self, c, v, nguon):
        self.gia_tri[c], self.nguon[c] = v, nguon

    def bo(self, c):
        self.gia_tri.pop(c, None)
        self.nguon.pop(c, None)

    def __contains__(self, c):
        return c in self.gia_tri


# --- So giá trị ---

def so_sanh(tb, u, bc):
    """tb và u là mục có gia_tri, don_vi. Trả bang | kem_hon | tot_hon | khac (đặc tả mục 6; HD 3, 6.1, 6.6).
    "co"/"khong" chỉ bằng chính nó; mã IP theo so_ip (khác nhánh là khac); số theo hướng thuận lợi, bằng trong ngưỡng."""
    a, b = tb["gia_tri"], u["gia_tri"]
    if isinstance(a, str) or isinstance(b, str):
        return "bang" if a == b else "khac"
    if isinstance(a, dict) or isinstance(b, dict):
        if not (isinstance(a, dict) and isinstance(b, dict)):
            return "khac"
        r = so_ip(MaIP(a.get("bui"), a.get("nuoc")), MaIP(b.get("bui"), b.get("nuoc")), bc.chung)
        return "khac" if r == "khac_nhanh" else r
    dv_a, dv_b = tb.get("don_vi"), u.get("don_vi")
    if dv_a and dv_b and dv_a != dv_b:
        try:
            a = quy_doi(a, dv_a, dv_b)
        except ValueError:
            return "khac"
    huong = bc.huong if bc.huong in ("cao_hon_tot_hon", "thap_hon_tot_hon") else "cao_hon_tot_hon"
    return so_huong(a, b, huong, bc.nguong)


def khop_gia_tri(tb, u, bc):
    """Đặc tả mục 6, HD 3 "Khớp giá trị": bằng hoặc kém thuận lợi hơn."""
    return so_sanh(tb, u, bc) in ("bang", "kem_hon")


def bang(tb, u, bc):
    """Đặc tả mục 6: bằng trong ngưỡng; mã IP bằng nhau; "co"/"khong" bằng nhau."""
    return so_sanh(tb, u, bc) == "bang"


def thuan_loi_hon_moi_gia_tri(tb, cung_bp, bc):
    """Đặc tả mục 6 D5 (HD 7 D5): tuyên bố thuận lợi hơn mọi giá trị khẳng định của cùng bộ phận, phiên bản."""
    khang = [u for u in cung_bp if u["gia_tri"] != "khong"]
    return bool(khang) and all(so_sanh(tb, u, bc) == "tot_hon" for u in khang)


def gia_tri_khac_nhau(cac_muc, bc):
    """Đại diện của các giá trị khác nhau (ngoài ngưỡng bằng nhau), theo thứ tự xuất hiện (D1b)."""
    dai_dien = []
    for u in cac_muc:
        if not any(bang(u, v, bc) for v in dai_dien):
            dai_dien.append(u)
    return dai_dien


def _so_theo_don_vi(u, bc):
    """Số của mục theo đơn vị của thuộc tính, hoặc None nếu không phải số."""
    g = u.get("gia_tri")
    if isinstance(g, bool) or not isinstance(g, (int, float)):
        return None
    dv, dich = u.get("don_vi"), bc.tt["don_vi"]
    if dv in ("gio", "phut") and dich in ("gio", "phut") and dv != dich:
        return quy_doi(g, dv, dich)
    return g


# --- Bước A ---

def san_pham_khac(ban_ghi, cau_hinh):
    """Đặc tả mục 2.2: tuyên bố gọi sản phẩm khác mẫu (san_pham_ma khác ma_mau, hoặc chữ khớp khong_nham_voi).
    [tự quyết] bản ghi Bước 22 để san_pham_ma = None cả khi tuyên bố không nêu sản phẩm lẫn khi khớp khong_nham_voi, nên
    phân biệt bằng chu_tuyen_bo (nếu có): khớp dài nhất là khong_nham_voi (tim_san_pham ra None mà chữ có tên đó) thì là khác."""
    tb, ma_mau = ban_ghi["tuyen_bo"], ban_ghi["ma_mau"]
    ma = tb.get("san_pham_ma")
    if ma is not None and ma != ma_mau:
        return True
    chu = ban_ghi.get("chu_tuyen_bo") or ""
    if not chu:
        return False
    r = tim_san_pham(chu, [cau_hinh])
    if r is not None:
        return r != ma_mau
    c = chuan_hoa_chu(chu)
    return any(chua_cum(c, chuan_hoa_chu(t)) for sp in (cau_hinh.get("san_pham") or {}).values()
               for t in sp.get("khong_nham_voi") or [])


def cung_thuoc_tinh(ban_ghi, bc):
    """Đặc tả mục 2.3–2.4: mục tài liệu cùng thuộc tính, có giá trị, không khác sản phẩm; sạc nhanh đồng hồ chỉ giữ cùng dạng."""
    ds = [u for u in ban_ghi.get("bang_chung") or []
          if u.get("thuoc_tinh") == bc.ten_tt and u.get("gia_tri") is not None and not u.get("khac_san_pham")
          and u.get("san_pham_ma") in (None, bc.ma_mau)]
    if bc.dang is not None:
        ds = [u for u in ds if u.get("don_vi") == bc.tb.get("don_vi")]
    return ds


# --- Điều kiện của mục tài liệu và so điều kiện ---

def dk_tai_lieu(u, c, bc):
    """(giá trị, nguồn) của điều kiện c ở mục tài liệu u; giá trị None là không ràng buộc. Đặc tả mục 4: mục không ghi c lấy
    cách hiểu mặc định nếu là giá trị cụ thể; khong_mua_them nghĩa là "chỉ đồ trong hộp"; các giá trị đặc biệt khác không ràng buộc."""
    v = (u.get("dieu_kien") or {}).get(c)
    if v is not None:
        return v, "neu_ro"
    h = bc.htt.get(c)
    if h == "khong_mua_them":
        return TRONG_HOP, "mac_dinh"
    if h is None or h in bc.dac_biet:
        return None, "khong_rang_buoc"
    return h, "mac_dinh"


def ap_dung(c, cung_tt, bc):
    """Đặc tả mục 4 [luật cài], HD 4 "không áp dụng": c áp dụng khi pham_vi_ap_dung ghi "dạng N" khớp dạng của tuyên bố, hoặc ít nhất
    một mục của cung_tt có c, hoặc c là khong_co_mac_dinh (thuộc tính chỉ có nghĩa khi có c)."""
    pv = (bc.tt.get("pham_vi_ap_dung") or {}).get(c)
    if isinstance(pv, str) and pv.startswith("dạng"):
        return bc.dang is None or pv == f"dạng {bc.dang}"
    if any((u.get("dieu_kien") or {}).get(c) is not None for u in cung_tt):
        return True
    return bc.htt.get(c) == "khong_co_mac_dinh"


def _khop_mot(c, tv, uv, bc):
    """Một điều kiện: tv của tuyên bố, uv của tài liệu (None là không ràng buộc). Đặc tả mục 5."""
    if uv is None or tv is None:
        return True
    if tv == TRONG_HOP:
        return uv == TRONG_HOP
    if uv == TRONG_HOP:
        return False
    if isinstance(tv, dict) or isinstance(uv, dict):
        if not (isinstance(tv, dict) and isinstance(uv, dict)):
            return False
        a, b = tv["so"], uv["so"]
        if tv.get("don_vi") != uv.get("don_vi"):
            try:
                a = quy_doi(a, tv["don_vi"], uv["don_vi"])
            except (ValueError, KeyError):
                return False
        return thoa_dieu_kien_so(bc.so[c]["thoa_khi"], a, b, bc.nguong)
    return tv == uv


def khac_biet(dk, u, bc):
    """Danh sách điều kiện khác nhau giữa tuyên bố và mục u (kể cả kiểu giá trị). Đặc tả mục 5; cụm lạ của u xử lý ở luật chặn."""
    kq = []
    for c, tv in dk.gia_tri.items():
        if bc.dk_bb.get(c) == "kieu_gia_tri":
            continue
        uv, _ = dk_tai_lieu(u, c, bc)
        if not _khop_mot(c, tv, uv, bc):
            kq.append({"dk": c, "loai_dk": bc.dk_bb[c], "tuyen_bo": tv, "tai_lieu": uv, "nguon": dk.nguon[c]})
    kt = bc.tb.get("kieu_gia_tri")
    if kt not in (None, "khong_neu", "khang_dinh"):   # chỉ so khi tuyên bố ghi rõ kiểu
        ku = u.get("kieu_gia_tri")
        if ku in (None, "khong_neu"):
            ku = bc.tt.get("kieu_gia_tri_mac_dinh")
        if ku not in (None, "nhu_hang_cong_bo") and ku != kt:
            kq.append({"dk": "kieu_gia_tri", "loai_dk": "kieu_gia_tri", "tuyen_bo": kt, "tai_lieu": ku, "nguon": "neu_ro"})
    return kq


def khop_dieu_kien(dk, u, bc):
    """Đặc tả mục 5: mọi điều kiện áp dụng khớp (chữ bằng nhau, số theo thoa_khi, kiểu giá trị khi tuyên bố ghi rõ)."""
    return not khac_biet(dk, u, bc)


def _khop_bp_pb(dk, u, bc):
    """u cùng bộ phận và phiên bản với tuyên bố (điều kiện khác bỏ qua): cung_bo_phan_va_phien_ban."""
    for c, loai in bc.dk_bb.items():
        if loai in ("bo_phan", "phien_ban") and c in dk:
            uv, _ = dk_tai_lieu(u, c, bc)
            if not _khop_mot(c, dk.gia_tri[c], uv, bc):
                return False
    return True


def lan_dieu_kien(cung_tt, bc):
    """Đặc tả mục 2, ý 5 [luật cài]: lan điều kiện giữa các mục cùng giá trị. Với mỗi điều kiện bắt buộc c, nhóm các mục cung_tt có
    giá trị bằng nhau (bang, cùng đơn vị sau quy đổi); trong nhóm, nếu mọi mục có ghi c đều cùng một giá trị (điều kiện số: cùng số và
    đơn vị) thì mục không ghi c nhận giá trị đó, nguồn "lan". Từ hai giá trị khác nhau của c trong nhóm thì không lan c. Cụm lạ
    (dieu_kien_khac) lan như vậy: mọi mục trong nhóm nhận hợp các cụm lạ của nhóm. Trả (danh sách mục đã sao chép, danh sách vết);
    không sửa bản ghi đầu vào, không lan qua mục khac_san_pham (đã loại khỏi cung_tt)."""
    ds = [json.loads(json.dumps(u)) for u in cung_tt]
    nhom = []
    for u in ds:
        for g in nhom:
            if bang(u, g[0], bc):
                g.append(u)
                break
        else:
            nhom.append([u])
    vet = []
    for g in nhom:
        if len(g) < 2:
            continue
        for c, loai in bc.dk_bb.items():
            if loai == "kieu_gia_tri":
                continue
            co = {json.dumps(u["dieu_kien"][c], sort_keys=True) for u in g if (u.get("dieu_kien") or {}).get(c) is not None}
            if len(co) != 1:
                continue
            gia_tri = next(u["dieu_kien"][c] for u in g if (u.get("dieu_kien") or {}).get(c) is not None)
            for u in g:
                if (u.get("dieu_kien") or {}).get(c) is None:
                    u.setdefault("dieu_kien", {})[c] = gia_tri
                    u.setdefault("nguon_dieu_kien", {})[c] = "lan"
                    vet.append({"ma_doan": u.get("ma_doan"), "dk": c, "gia_tri": gia_tri})
        cum = []
        for u in g:
            cum += [m for m in u.get("dieu_kien_khac") or [] if m.get("cum") not in [x.get("cum") for x in cum]]
        if cum:
            for u in g:
                co = [m.get("cum") for m in u.get("dieu_kien_khac") or []]
                for m in cum:
                    if m.get("cum") not in co:
                        u.setdefault("dieu_kien_khac", []).append(dict(m))
                        vet.append({"ma_doan": u.get("ma_doan"), "dk": "dieu_kien_khac", "gia_tri": m.get("cum")})
    return ds, vet


# --- Luật chép đúng nhãn (QĐ15) ---

def nhan_muc(u, bc):
    """Đặc tả mục 3 B2: nhãn của mục tài liệu = câu trích giá trị bỏ con số, đơn vị, cụm kiểu giá trị, dấu câu và chữ chung đầu nhãn."""
    trich = (u.get("trich") or {}).get("gia_tri")
    if not trich:
        return ""
    t = unicodedata.normalize("NFC", trich)
    cat = [(g.dau_nhom if g.dau_nhom is not None else g.dau, g.cuoi) for g in tim_gia_tri(t, bc.chung)]
    cat += [(s.dau, s.cuoi) for s in tim_so(t)]
    cat += [m.span() for m in re.finditer(r"(?<![A-Za-z0-9])IP\s?[0-6X][0-8X](?![A-Za-z0-9])|(?<![A-Za-z0-9])WR\s?[0-9]+|(?<![A-Za-z0-9])[0-9]+\s?ATM", t, re.I)]
    chu = list(t)
    for a, b in cat:
        for i in range(a, b):
            chu[i] = " "
    n = chuan_cum("".join(chu))
    ck = chuan_cum(u.get("cum_kieu") or "")
    if ck:
        n = " ".join(re.sub(r"(?<!\w)" + re.escape(ck) + r"(?!\w)", " ", n).split())
    bo = [chuan_cum(x) for x in (bc.chung.get("chep_nhan") or {}).get("bo_chu_dau") or []]
    doi = True
    while doi:
        doi = False
        for w in bo:
            if n == w or n.startswith(w + " "):
                n, doi = n[len(w):].strip(), True
    return n


def chep_nhan(cung_tt, dk, bc):
    """Đặc tả mục 3 B2 [luật cài], HD 6.8 QĐ15. Trả {"nhan", "ma_doan", "dk": {điều kiện lấy từ mục}} hoặc None.
    Nhãn còn ít nhất một chữ và nằm trọn trong chữ tuyên bố; chọn nhãn dài nhất (số chữ, rồi số ký tự); hai nhãn dài bằng nhau mà
    điều kiện khác nhau thì không áp. Chỉ lấy điều kiện (không phải kiểu giá trị) mà tuyên bố chưa nêu rõ. [tự quyết] tính
    "điều kiện của mục" trên các điều kiện bắt buộc của thuộc tính; không lấy điều kiện có cách hiểu khong_mua_them (bộ sạc bán riêng),
    vì HD 5 và V21, V23, V34 cho tuyên bố không nêu bộ sạc là Lệch dù chép đúng chữ của dòng ("Sạc nhanh HyperCharge 67W")."""
    chu = chuan_cum(bc.chu)
    ung = []
    for u in cung_tt:
        n = nhan_muc(u, bc)
        if n and chua_cum(chu, n):
            ung.append((len(n.split()), len(n), n, u))
    if not ung:
        return None
    tot = max(k[:2] for k in ung)
    cac = [k for k in ung if k[:2] == tot]

    def chu_ky(u):
        return json.dumps({c: v for c, v in (u.get("dieu_kien") or {}).items() if c in bc.dk_bb}, sort_keys=True)

    if len({chu_ky(k[3]) for k in cac}) > 1:
        return None
    u = cac[0][3]
    lay = {c: v for c, v in (u.get("dieu_kien") or {}).items()
           if c in bc.dk_bb and bc.dk_bb[c] != "kieu_gia_tri" and c not in dk and bc.htt.get(c) != "khong_mua_them"}
    return {"nhan": cac[0][2], "ma_doan": u.get("ma_doan"), "dk": lay}


# --- Cụm phủ nhiều giá trị ---

def _cum_cua_gia_tri(bc, c, v):
    """Các cụm (đã chuan_cum) của giá trị v của điều kiện c ở phía tuyên bố, đúng chi_thuoc_tinh."""
    kb = (bc.cach.get(c) or {}).get(v) or {}
    if kb.get("phia") == "tai_lieu" or (kb.get("chi_thuoc_tinh") and bc.ten_tt not in kb["chi_thuoc_tinh"]):
        return []
    return [chuan_cum(x) for k in ("tu_tai_lieu", "hieu_biet_chung") for x in kb.get(k) or []]


def kem_thuan_loi_nhat(c, cung_tt, dk, bc, gioi_han=None):
    """Đặc tả mục 3 B6, B4: giá trị của điều kiện c mà con số tài liệu (cùng bộ phận, phiên bản với tuyên bố) kém thuận lợi nhất;
    gioi_han là tập giá trị được phủ (None là mọi giá trị). Mục không ghi c lấy giá trị mặc định cụ thể. None nếu không có căn cứ."""
    nhom = {}
    for u in cung_tt:
        if not _khop_bp_pb(dk, u, bc):
            continue
        v, _ = dk_tai_lieu(u, c, bc)
        if v is None or v == TRONG_HOP or isinstance(v, dict) or (gioi_han is not None and v not in gioi_han):
            continue
        so = _so_theo_don_vi(u, bc)
        if so is not None:
            nhom.setdefault(v, []).append(so)
    if not nhom:
        return None
    cao = bc.huong != "thap_hon_tot_hon"
    xau = {v: (min(s) if cao else max(s)) for v, s in nhom.items()}
    return sorted(xau, key=lambda v: (xau[v] if cao else -xau[v], v))[0]


def _dieu_kien_duoc_phu(mau, chu_khop, bc):
    """(điều kiện được phủ, tập giá trị được phủ hoặc None, giá trị cố định hoặc None) theo bảng đặc tả mục 3 B4."""
    if mau == "mọi chế độ":
        return next((c for c, l in bc.dk_bb.items() if l == "che_do_hoat_dong" and not c.startswith("hoat_dong")), None), None, None
    if mau == "mọi hoạt động":
        if "hoat_dong" in bc.dk_bb:
            return "hoat_dong", None, None
        if "hoat_dong_cho_phep" in bc.dk_bb:   # phủ cả hoạt động bị cấm
            return "hoat_dong_cho_phep", None, "bi_cam"
        if "hoat_dong_bi_cam" in bc.dk_bb:
            gt = list(bc.cach.get("hoat_dong_bi_cam") or [])
            return "hoat_dong_bi_cam", None, gt[0] if gt else None
        return None, None, None
    if mau in ("mọi điều kiện X", "bất kể X"):
        x = chuan_cum(re.sub(r"^(mọi điều kiện|bất kể)\s*", "", chu_khop))
        if "ánh sáng" in x:
            return ("che_do_hien_thi" if "che_do_hien_thi" in bc.dk_bb else None), None, None
        for c in bc.dk_bb:
            if x and any(x in chuan_cum(t) for v in bc.cach.get(c) or {} for t in _cum_cua_gia_tri(bc, c, v)):
                return c, None, None
        return None, None, None
    m = re.match(r"dù\s+(?P<a>.+?)\s+hay\s+(?P<b>.+)", chu_khop) or re.match(r"cho cả\s+(?P<a>.+?)\s+và\s+(?P<b>.+)", chu_khop)
    if m:
        a, b = chuan_cum(m.group("a")), chuan_cum(m.group("b"))
        for c, loai in bc.dk_bb.items():
            if loai == "kieu_gia_tri":
                continue
            va = {v for v in bc.cach.get(c) or {} if any(chua_cum(a, t) for t in _cum_cua_gia_tri(bc, c, v))}
            vb = {v for v in bc.cach.get(c) or {} if any(chua_cum(b, t) for t in _cum_cua_gia_tri(bc, c, v))}
            if va and vb and len(va | vb) >= 2:
                return c, va | vb, None
    return None, None, None


def cum_phu(muc_khac, cung_tt, dk, bc):
    """Đặc tả mục 3 B4, HD 6.8 "Cụm phủ nhiều giá trị". Trả None nếu không phải cụm phủ hoặc không xác định được điều kiện
    được phủ (khi đó vẫn là điều kiện lạ); ngược lại {"mau", "dieu_kien", "gia_tri", "bo_qua"}. Điều kiện trực tiếp cùng loại đã có
    ở tuyên bố thì thắng (QĐ11): bo_qua. Điều kiện của tuyên bố là giá trị kém thuận lợi nhất trong các giá trị được phủ mà tài liệu
    công bố; kháng nước "mọi hoạt động" là hoạt động bị cấm."""
    cum = chuan_hoa_chu(muc_khac.get("cum") or "")
    for mau, bt in CUM_PHU.items():
        m = re.search(r"(?<!\w)" + bt, cum, re.IGNORECASE)
        if m:
            break
    else:
        return None
    c, phu, co_dinh = _dieu_kien_duoc_phu(mau, m.group(0), bc)
    if c is None:
        return None
    if c in dk:
        return {"mau": mau, "dieu_kien": c, "gia_tri": None, "bo_qua": True}
    v = co_dinh or kem_thuan_loi_nhat(c, cung_tt, dk, bc, phu)
    if v is None:
        return None
    return {"mau": mau, "dieu_kien": c, "gia_tri": v, "bo_qua": False}


def goi_muc_cao(cung_tt, dk, bc):
    """Đặc tả mục 3 B5, HD 6.5: tuyên bố có chữ gọi mức cao, không có chữ chỉ chế độ, tài liệu có từ hai giá trị khác nhau thì tra
    cach_goi_theo_hang[hãng][chữ]. Trả (điều kiện, danh sách chế độ) hoặc None."""
    c = "che_do_hien_thi"
    cach = bc.tt.get("cach_goi_theo_hang")
    if not bc.tb.get("goi_muc_cao") or not cach or c in dk or c not in bc.dk_bb or len(gia_tri_khac_nhau(cung_tt, bc)) < 2:
        return None
    bang_hang = {chuan_hoa_chu(k): v for k, v in (cach.get(bc.hang) or {}).items()}
    modes = bang_hang.get(chuan_hoa_chu(bc.tb.get("cum_kieu") or ""))
    return (c, modes) if modes else None


def so_thang(cung_tt, bc):
    """Đặc tả mục 3 B6 "So thẳng", HD 6.4: cung_tt chỉ có một giá trị và không mục nào có điều kiện (dieu_kien, dieu_kien_khac).
    [tự quyết] chữ gọi mức cao ("đỉnh" của V12) không tính là điều kiện, vì V12 là ví dụ so thẳng; câu "kể cả kiểu giá trị do chữ
    gọi mức cao" của đặc tả mâu thuẫn với V12 nếu hiểu ngược lại."""
    if len(gia_tri_khac_nhau(cung_tt, bc)) != 1:
        return False
    return not any(u.get("dieu_kien") or u.get("dieu_kien_khac") or u.get("xung_dot") for u in cung_tt)


def dieu_kien_tuyen_bo(cung_tt, bc):
    """Đặc tả mục 3 (bước B), mục 4. Trả dict: dk (DieuKien), mac_dinh, chep_nhan, d1a (None hoặc {"loai", "cum"|"khoa"}),
    khong_ap_dung, so_thang, cum_phu. Không bao giờ dùng con số của tuyên bố. Thứ tự: nêu rõ (B3), cụm phủ (B4), chép nhãn (B2),
    chữ gọi mức cao (B5), cách hiểu mặc định (B6); điều kiện chưa xác định (B1) chọn theo thứ tự: cụm lạ, xung đột, chữ gọi mức
    cao trỏ nhiều chế độ, khóa không có mặc định."""
    tb = bc.tb
    dk = DieuKien()
    tb_dk = tb.get("dieu_kien") or {}
    for c, loai in bc.dk_bb.items():   # B3
        v = tb_dk.get(c)
        if loai != "kieu_gia_tri" and v is not None and not str(v).startswith("chua_ro"):
            dk.dat(c, v, "neu_ro")
    la, phu_ghi = [], []
    for m in tb.get("dieu_kien_khac") or []:   # B1 và B4
        p = cum_phu(m, cung_tt, dk, bc)
        if p is None:
            la.append(m.get("cum") or "")
        elif not p["bo_qua"]:
            dk.dat(p["dieu_kien"], p["gia_tri"], "cum_phu")
            phu_ghi.append(p)
    xd = [f"{c}={'/'.join(map(str, vs))}" for c, vs in (tb.get("xung_dot") or {}).items()]
    cn = chep_nhan(cung_tt, dk, bc)   # B2
    chep = None
    if cn and cn["dk"]:
        for c, v in cn["dk"].items():
            dk.dat(c, v, "chep_nhan")
        chep = cn["nhan"]
    nhieu_che_do, da_xet = None, set()
    gm = goi_muc_cao(cung_tt, dk, bc)   # B5
    if gm:
        c, modes = gm
        if len(modes) == 1:
            dk.dat(c, modes[0], "neu_ro")
        else:
            nhieu_che_do = tb.get("cum_kieu")
            da_xet.add(c)   # đã chưa xác định bằng chữ gọi mức cao, không ghi thêm mac_dinh cho khóa này
    khong_ap_dung = []
    for c in list(dk.gia_tri):   # điều kiện không áp dụng thì không ràng buộc
        if not ap_dung(c, cung_tt, bc):
            dk.bo(c)
            khong_ap_dung.append(c)
    thang = so_thang(cung_tt, bc)
    mac_dinh, thieu, cho_kem = [], [], []
    kt = tb.get("kieu_gia_tri")
    for c, loai in bc.dk_bb.items():   # B6
        if c in dk or c in khong_ap_dung or c in da_xet:
            continue
        h = bc.htt.get(c)
        if loai == "kieu_gia_tri":   # kiểu giá trị: nêu rõ nếu tuyên bố ghi kiểu; mặc định chỉ ghi chú, so ở khac_biet
            if kt in (None, "khong_neu", "khang_dinh") and h not in (None, "nhu_hang_cong_bo") and h not in bc.dac_biet:
                mac_dinh.append(c)
            continue
        if not ap_dung(c, cung_tt, bc):
            khong_ap_dung.append(c)
            continue
        if h in (None, "nhu_hang_cong_bo"):
            continue
        if h == "khong_co_mac_dinh":
            if not thang:
                mac_dinh.append(c)
                thieu.append(c)
        elif h == "khong_mua_them":
            dk.dat(c, TRONG_HOP, "mac_dinh")
            mac_dinh.append(c)
        elif h == "kem_thuan_loi_nhat":
            cho_kem.append(c)
        else:
            dk.dat(c, h, "mac_dinh")
            mac_dinh.append(c)
    for c in cho_kem:
        v = kem_thuan_loi_nhat(c, cung_tt, dk, bc)
        if v is not None:
            dk.dat(c, v, "mac_dinh")
            mac_dinh.append(c)
    thu_tu = list(bc.dk_bb)
    mac_dinh.sort(key=thu_tu.index)
    d1a = None
    if la:
        d1a = {"loai": "chua_xac_dinh", "cum": la[0]}
    elif xd:
        d1a = {"loai": "chua_xac_dinh", "cum": xd[0]}
    elif nhieu_che_do:
        d1a = {"loai": "chua_xac_dinh", "cum": nhieu_che_do}
    elif thieu:
        d1a = {"loai": "mac_dinh", "khoa": sorted(thieu, key=thu_tu.index)}
    return {"dk": dk, "mac_dinh": mac_dinh, "chep_nhan": chep, "d1a": d1a, "khong_ap_dung": khong_ap_dung,
            "so_thang": thang, "cum_phu": phu_ghi}


# --- Biến đổi, bằng chứng ---

_THU_TU_LOAI = {"bo_phan": 0, "phien_ban": 1, "kieu_gia_tri": 2}


def _khac_biet_day_du(dk, u, bc):
    """khac_biet cộng điều kiện lạ (dieu_kien_khac) của u mà tuyên bố không nêu (tính như điều kiện lấy mặc định)."""
    kb = khac_biet(dk, u, bc)
    kb += [{"dk": "dieu_kien_khac", "loai_dk": "dieu_kien_khac", "tuyen_bo": None, "tai_lieu": m.get("cum"), "nguon": "mac_dinh"}
           for m in u.get("dieu_kien_khac") or []]
    return kb


def _loai_tu_khac_biet(kb):
    ro = [d for d in kb if d["nguon"] != "mac_dinh"]
    if not ro:
        return "bo_dieu_kien"
    loai = min((d["loai_dk"] for d in ro), key=lambda x: _THU_TU_LOAI.get(x, 3))
    return {"bo_phan": "doi_bo_phan", "phien_ban": "doi_phien_ban", "kieu_gia_tri": "doi_kieu_gia_tri"}.get(loai, "doi_dieu_kien")


def loai_bien_doi(dk, u, bc):
    """Đặc tả mục 7, HD 8: loại biến đổi giữa điều kiện của tuyên bố và của u. Nêu rõ (kể cả cụm phủ, chép nhãn) thì doi_*; lấy mặc định
    thì bo_dieu_kien. Nhiều điều kiện khác thì ưu tiên điều kiện nêu rõ; trong đó bộ phận, phiên bản, kiểu giá trị, điều kiện còn lại."""
    return _loai_tu_khac_biet(_khac_biet_day_du(dk, u, bc))


def _chon_d4(ung, dk, bc):
    """Đặc tả mục 7: trong các u bằng giá trị chọn u khác ít điều kiện nhất; hòa thì ưu tiên khác ở điều kiện nêu rõ, rồi bộ phận,
    phiên bản, kiểu giá trị, điều kiện còn lại (rồi mã đoạn cho tất định). Trả (u, danh sách khác biệt, các u cùng dấu vết)."""
    def khoa(u):
        kb = _khac_biet_day_du(dk, u, bc)
        ro = [d for d in kb if d["nguon"] != "mac_dinh"]
        hang = min((_THU_TU_LOAI.get(d["loai_dk"], 3) for d in ro), default=9)
        return (len(kb), 0 if ro else 1, hang, _khoa_ma(u.get("ma_doan")))

    tot = min(ung, key=khoa)
    kb = _khac_biet_day_du(dk, tot, bc)

    def dau_vet(u):
        return {(d["dk"], json.dumps(d["tai_lieu"], sort_keys=True, default=str)) for d in _khac_biet_day_du(dk, u, bc)}

    dau = dau_vet(tot)
    return tot, kb, [u for u in ung if dau_vet(u) == dau]


def _chung_cu(cac_muc):
    """(mã đoạn sắp theo mã, các câu trích giá trị không trùng nối bằng " | ") — đặc tả mục 7, cuối."""
    ds = sorted(cac_muc, key=lambda u: _khoa_ma(u.get("ma_doan")))
    ma, trich = [], []
    for u in ds:
        if u.get("ma_doan") and u["ma_doan"] not in ma:
            ma.append(u["ma_doan"])
        t = (u.get("trich") or {}).get("gia_tri")
        if t and t not in trich:
            trich.append(t)
    return ma, " | ".join(trich)


# --- Luật chặn điều kiện lạ ---

def _la(u):
    return bool(u.get("dieu_kien_khac") or u.get("xung_dot"))


def _cum_la(u):
    cum = [m.get("cum") for m in u.get("dieu_kien_khac") or []]
    cum += [f"{c}={'/'.join(map(str, vs))}" for c, vs in (u.get("xung_dot") or {}).items()]
    return "; ".join(x for x in cum if x)


def gop_luat_chung(cung_dk, bc):
    """Đặc tả mục 6, luật chung cho nhiều giá trị (HD 6.7; phương án 2 của phan_tich_dieu_kien_ngoai_cau_hinh.md): từ hai mục chỉ khác nhau
    ở cùng một điều kiện lạ (cùng điều kiện đã biết, cùng loại cụm lạ, cụm và giá trị khác nhau) là lựa chọn của người dùng; giữ mục có
    giá trị kém thuận lợi nhất (coi như hết điều kiện lạ), các mục còn lại chuyển sang khac_dk. Trả (cung_dk mới, khac_them, nhóm đã gộp)."""
    nhom = {}
    for u in cung_dk:
        if len(u.get("dieu_kien_khac") or []) == 1 and not u.get("xung_dot"):
            khoa = (json.dumps(u.get("dieu_kien") or {}, sort_keys=True), u.get("kieu_gia_tri"), u["dieu_kien_khac"][0].get("loai"))
            nhom.setdefault(khoa, []).append(u)
    moi, khac, da_gop = list(cung_dk), [], []
    cao = bc.huong != "thap_hon_tot_hon"
    for ds in nhom.values():
        if len(ds) < 2 or len({u["dieu_kien_khac"][0].get("cum") for u in ds}) < 2 or len(gia_tri_khac_nhau(ds, bc)) < 2:
            continue
        so = [(_so_theo_don_vi(u, bc), u) for u in ds]
        if any(s is None for s, _ in so):
            continue
        kem = (min if cao else max)(so, key=lambda x: x[0])[1]
        for u in ds:
            if u is not kem:
                moi.remove(u)
                khac.append(u)
        da_gop.append({"cum": [u["dieu_kien_khac"][0].get("cum") for u in ds], "ma_doan": kem.get("ma_doan"), "gia_tri": kem["gia_tri"]})
        kem_sach = dict(kem)
        kem_sach["dieu_kien_khac"] = []
        moi[moi.index(kem)] = kem_sach
    return moi, khac, da_gop


# --- Hàm chính ---

def _vet_so_sanh(cung_tt, cung_dk, dk, tb, bc):
    kq = []
    for u in cung_tt:
        kq.append({"ma_doan": u.get("ma_doan"), "gia_tri": u["gia_tri"], "don_vi": u.get("don_vi"), "so": so_sanh(tb, u, bc),
                   "cung_dk": any(u.get("ma_doan") == v.get("ma_doan") and u["gia_tri"] == v["gia_tri"] for v in cung_dk),
                   "khac_biet": khac_biet(dk, u, bc) if dk is not None else []})
    return kq


def _ten_san_pham(ban_ghi, cau_hinh, khac):
    tb = ban_ghi["tuyen_bo"]
    if khac:
        return (tb.get("trich") or {}).get("san_pham") or tb.get("san_pham_ma") or "sản phẩm khác"
    return ((cau_hinh.get("san_pham") or {}).get(ban_ghi["ma_mau"]) or {}).get("ten") or ban_ghi["ma_mau"]


def _ket_qua(cau_hinh, nhan, dong, loai, bang_chung=(), ghi_chu=(), mau_thuan=False, vet=None):
    ma, trich = _chung_cu(bang_chung)
    kq = {"nhan": nhan, "dong_d": dong, "loai": loai, "bang_chung": ma, "trich": trich, "ly_do": "",
          "ghi_chu": list(ghi_chu), "tai_lieu_mau_thuan": mau_thuan, "vet": vet or {}}
    kq["ly_do"] = _ly_do.sinh_ly_do(kq, cau_hinh)
    return kq


def _so_tb(tb):
    return {"gia_tri": tb["gia_tri"], "don_vi": tb.get("don_vi"), "kieu_gia_tri": tb.get("kieu_gia_tri"),
            "cum_kieu": tb.get("cum_kieu"), "goi_muc_cao": tb.get("goi_muc_cao")}


def quyet_dinh(ban_ghi, cau_hinh, doi_chieu=True, luat_chung_cho_nhieu_gia_tri=None):
    """Bộ quyết định A–D (đặc tả mục 1–8; T5.5). ban_ghi: bản ghi trích xuất của một tuyên bố (Bước 22, mục 8); cau_hinh: doc_cau_hinh của nhóm.
    doi_chieu=False là P−ĐK (T5.9). luat_chung_cho_nhieu_gia_tri: True/False/"bat"/"tat", None thì đọc chung.yaml.
    Trả dict: nhan (DUNG, SAI, LECH, CHUA_DU), dong_d (D1, D1a, D1b, D2–D6), loai, bang_chung, trich, ly_do, ghi_chu (danh sách chuỗi),
    tai_lieu_mau_thuan, vet (dấu vết cho sinh lý do và phân tích lỗi)."""
    chung = cau_hinh["chung"]
    if luat_chung_cho_nhieu_gia_tri is None:
        luat_chung_cho_nhieu_gia_tri = (chung.get("dieu_kien_la") or {}).get("luat_chung_cho_nhieu_gia_tri")
    luat = luat_chung_cho_nhieu_gia_tri in (True, "bat")
    tb = ban_ghi.get("tuyen_bo")
    # A1: trích xuất thất bại
    if (ban_ghi.get("loi") or not tb or tb.get("thuoc_tinh") is None or tb.get("gia_tri") is None
            or tb["thuoc_tinh"] not in cau_hinh["thuoc_tinh"]):
        return _ket_qua(cau_hinh, CHUA_DU, "D1a", None, (), ["chua_xac_dinh=trich_xuat_that_bai"],
                        vet={"dong": "D1a", "doi_chieu": doi_chieu, "nguyen_nhan": {"loai": "trich_xuat_that_bai", "cum": "trich_xuat_that_bai"},
                             "thuoc_tinh": (tb or {}).get("thuoc_tinh"), "san_pham": _ten_san_pham({**ban_ghi, "tuyen_bo": tb or {}}, cau_hinh, False)})
    bc = BoiCanh(ban_ghi, cau_hinh)
    base = {"doi_chieu": doi_chieu, "thuoc_tinh": bc.ten_tt, "tuyen_bo": _so_tb(tb)}
    khac_sp = san_pham_khac(ban_ghi, cau_hinh)
    cung_tt = [] if khac_sp else cung_thuoc_tinh(ban_ghi, bc)
    if not cung_tt:   # A2, A3: D1
        return _ket_qua(cau_hinh, CHUA_DU, "D1", None, (), (),
                        vet={**base, "dong": "D1", "san_pham": _ten_san_pham(ban_ghi, cau_hinh, khac_sp), "san_pham_khac": khac_sp})
    base["san_pham"] = _ten_san_pham(ban_ghi, cau_hinh, False)

    ghi_chu = []
    if doi_chieu:
        cung_tt, lan = lan_dieu_kien(cung_tt, bc)
        base["lan"] = lan
        r = dieu_kien_tuyen_bo(cung_tt, bc)
        dk = r["dk"]
        base.update({"dieu_kien_tuyen_bo": dict(dk.gia_tri), "nguon_dieu_kien": dict(dk.nguon), "khong_ap_dung": r["khong_ap_dung"],
                     "so_thang": r["so_thang"], "cum_phu": r["cum_phu"], "chep_nhan": r["chep_nhan"], "mac_dinh": r["mac_dinh"]})
        if r["mac_dinh"]:
            ghi_chu.append("mac_dinh=" + ",".join(r["mac_dinh"]))
        if r["chep_nhan"]:
            ghi_chu.append(f"chep_nhan={r['chep_nhan']}")
        if r["d1a"]:   # B1
            if r["d1a"]["loai"] == "chua_xac_dinh":
                ghi_chu.insert(0, f"chua_xac_dinh={r['d1a']['cum']}")
            khop = [u for u in cung_tt if khop_gia_tri(tb, u, bc)]
            return _ket_qua(cau_hinh, CHUA_DU, "D1a", None, khop or cung_tt, ghi_chu,
                            vet={**base, "dong": "D1a", "nguyen_nhan": r["d1a"]})
        cung_dk = [u for u in cung_tt if khop_dieu_kien(dk, u, bc)]
        khac_dk = [u for u in cung_tt if u not in cung_dk]
        # Luật chặn điều kiện lạ
        gop = []
        if luat:
            cung_dk, them, gop = gop_luat_chung(cung_dk, bc)
            khac_dk += them
        chan = [u for u in cung_dk if _la(u) and khop_gia_tri(tb, u, bc)]
        if chan:
            cum = _cum_la(chan[0])
            return _ket_qua(cau_hinh, CHUA_DU, "D1a", None, chan, ghi_chu + [f"chua_xac_dinh=dieu_kien_la:{cum}"],
                            vet={**base, "dong": "D1a", "nguyen_nhan": {"loai": "chua_xac_dinh", "cum": cum, "dieu_kien_la": True},
                                 "luat_chung": gop})
        # D1b
        khac_nhau = gia_tri_khac_nhau(cung_dk, bc)
        if len(khac_nhau) >= 2:
            if not all(khop_gia_tri(tb, u, bc) for u in cung_dk):
                return _ket_qua(cau_hinh, CHUA_DU, "D1b", None, cung_dk, ghi_chu, True,
                                vet={**base, "dong": "D1b", "mau_thuan": [{"ma_doan": u.get("ma_doan"), "gia_tri": u["gia_tri"],
                                                                           "trich": (u.get("trich") or {}).get("gia_tri")} for u in khac_nhau]})
            ghi_chu.append("mau_thuan_khop_ca_hai=" + "/".join(_ly_do.dinh_dang_so(u["gia_tri"]) for u in khac_nhau[:2]))
        cung_bp = [u for u in cung_tt if _khop_bp_pb(dk, u, bc)]
    else:   # P−ĐK: bỏ bước B
        dk = DieuKien()
        cung_dk, khac_dk, cung_bp = list(cung_tt), [], list(cung_tt)
        base.update({"dieu_kien_tuyen_bo": {}, "nguon_dieu_kien": {}})
    base["cung_dk"] = [u.get("ma_doan") for u in cung_dk]
    base["khac_dk"] = [u.get("ma_doan") for u in khac_dk]
    base["so_sanh"] = _vet_so_sanh(cung_tt, cung_dk, dk if doi_chieu else None, tb, bc)

    # D2
    if tb.get("kieu_gia_tri") == "khang_dinh":
        def la_toi_da(u):
            k = u.get("kieu_gia_tri")
            return (k if k not in (None, "khong_neu") else bc.tt.get("kieu_gia_tri_mac_dinh")) == "toi_da"
        ung = [u for u in cung_dk if la_toi_da(u) and so_sanh(tb, u, bc) != "tot_hon"]
        if ung:
            tu = tb.get("cum_kieu")
            return _ket_qua(cau_hinh, LECH, "D2", "doi_kieu_gia_tri", ung, ghi_chu + [f"khang_dinh={tu}"],
                            vet={**base, "dong": "D2", "khang_dinh": tu, "trich_chinh": (ung[0].get("trich") or {}).get("gia_tri")})
    # D3
    khop = [u for u in cung_dk if khop_gia_tri(tb, u, bc)]
    if khop:
        u0 = sorted(khop, key=lambda u: _khoa_ma(u.get("ma_doan")))[0]
        k0 = u0.get("kieu_gia_tri")
        bo_len_den = (tb.get("kieu_gia_tri") in (None, "khong_neu") and
                      (k0 if k0 not in (None, "khong_neu") else bc.tt.get("kieu_gia_tri_mac_dinh")) == "toi_da")
        return _ket_qua(cau_hinh, DUNG, "D3", None, khop, ghi_chu,
                        vet={**base, "dong": "D3", "trich_chinh": (u0.get("trich") or {}).get("gia_tri"), "bo_len_den": bo_len_den})
    # D4
    ung4 = [u for u in khac_dk if bang(tb, u, bc)]
    if ung4:
        u, kb, cung_vet = _chon_d4(ung4, dk, bc)
        loai = _loai_tu_khac_biet(kb)
        return _ket_qua(cau_hinh, LECH, "D4", loai, cung_vet, ghi_chu,
                        vet={**base, "dong": "D4", "khac_biet": kb, "u": {"ma_doan": u.get("ma_doan"), "gia_tri": u["gia_tri"], "don_vi": u.get("don_vi")},
                             "trich_chinh": (u.get("trich") or {}).get("gia_tri")})
    # D5
    if cung_dk or thuan_loi_hon_moi_gia_tri(tb, cung_bp, bc):
        goc = cung_dk or cung_bp
        loai = "doi_gia_tri"
        for c, ten in (("bo_phan", "doi_bo_phan"), ("phien_ban", "doi_phien_ban")):
            ten_dk = next((k for k, l in bc.dk_bb.items() if l == c), None)
            if ten_dk and ten_dk in dk and dk.nguon[ten_dk] != "mac_dinh" and not any(u["gia_tri"] != "khong" for u in cung_bp):
                loai = ten
                break
        so_goc = [u for u in goc if not isinstance(u["gia_tri"], (str, dict))]
        cao = bc.huong != "thap_hon_tot_hon"
        u_tot = (max if cao else min)(so_goc, key=lambda u: _so_theo_don_vi(u, bc)) if so_goc else goc[0]
        cung_gt = [u for u in goc if bang(u, u_tot, bc)]
        return _ket_qua(cau_hinh, SAI, "D5", loai, cung_gt, ghi_chu,
                        vet={**base, "dong": "D5", "u": {"ma_doan": u_tot.get("ma_doan"), "gia_tri": u_tot["gia_tri"], "don_vi": u_tot.get("don_vi")}})
    # D6
    return _ket_qua(cau_hinh, CHUA_DU, "D6", None, cung_bp or cung_tt, ghi_chu, vet={**base, "dong": "D6"})


# --- Ngưỡng QĐ8 (HD 11.2) ---

def dem_nguong_qd8(ket_qua):
    """Đếm trên danh sách đầu ra quyet_dinh: số ca D4 (nhãn Lệch), số ca D4 mà tuyên bố nêu rõ một hoạt động và giá trị trùng thuộc hoạt
    động khác (kiểu V42), tỉ lệ và có vượt NGUONG_QD8 không. Không đổi ngưỡng sau khi đếm.
    [tự quyết] "nêu rõ hoạt động" là nguồn neu_ro hoặc cum_phu; chép nhãn (QĐ15) và mặc định không tính (QĐ9). "Hoạt động" là điều
    kiện có tên bắt đầu bằng hoat_dong."""
    d4 = [k for k in ket_qua if k["dong_d"] == "D4"]
    n = 0
    for k in d4:
        if any(d["dk"].startswith("hoat_dong") and d["nguon"] in ("neu_ro", "cum_phu") for d in k["vet"].get("khac_biet") or []):
            n += 1
    ti_le = n / len(d4) if d4 else 0.0
    return {"d4": len(d4), "nhieu_hoat_dong": n, "ti_le": ti_le, "vuot_nguong": ti_le > NGUONG_QD8}
