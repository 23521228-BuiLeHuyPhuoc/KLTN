"""Chuẩn hóa số, đơn vị, mã IP, kiểu giá trị và tên sản phẩm (Bước 21, T5.4, T5.5).

Hàm thuần (nhận chuỗi và cấu hình, trả giá trị) để bộ quyết định A–D (T5.5) dùng sau này. Mọi danh sách cụm
đọc từ data/cau_hinh/*.yaml; trong mã chỉ có biểu thức chính quy khung số và khung mã IP/ISO 22810.

Quy ước vị trí: GiaTri.dau và GiaTri.cuoi là chỉ số trong chuỗi sau NFC (chuỗi tiếng Việt thường đã là NFC nên
trùng chuỗi gốc); tim_kieu_gia_tri nhận lại đúng chuỗi đó và cặp chỉ số đó.
"""
from dataclasses import dataclass
import re
import unicodedata

from .cau_hinh import chuan_hoa_chu

NGUONG_BANG_MAC_DINH = 0.01
HUONG_HOP_LE = ("cao_hon_tot_hon", "thap_hon_tot_hon")
SO_TOI_DA_TU_GIUA = 2   # tim_kieu_gia_tri: số từ tối đa giữa từ khẳng định và con số
_SO = re.compile(r"[0-9]+(?:[.,][0-9]+)*")
_MA_IP = re.compile(r"(?<![A-Za-z0-9])IP\s?([0-6X])([0-8X])(?![A-Za-z0-9])", re.IGNORECASE)
_MA_ISO = re.compile(r"(?<![A-Za-z0-9])(?:([0-9]+)\s*ATM|WR\s*([0-9]+))(?![A-Za-z0-9])", re.IGNORECASE)


@dataclass(frozen=True)
class GiaTri:
    so: float
    don_vi: str      # khóa trong chuan_hoa.don_vi: gio, phut, nit, W, mAh, Hz, x, m, phan_tram
    chu: str         # chuỗi khớp, vd. "30 giờ"
    dau: int         # chỉ số bắt đầu con số
    cuoi: int        # chỉ số sau chữ đơn vị
    dau_nhom: int | None = None   # dạng "a / b <đơn vị>": chỉ số bắt đầu của a, chung cho cả a và b; thường là None


@dataclass(frozen=True)
class So:
    so: float
    chu: str         # chuỗi con số như viết ("7,0", "3.000")
    dau: int
    cuoi: int


@dataclass(frozen=True)
class MaIP:
    bui: int | None   # None khi viết "X"
    nuoc: int | None


@dataclass(frozen=True)
class KieuGiaTri:
    kieu: str                 # khang_dinh, một khóa của kieu_gia_tri (toi_da, dien_hinh, ...) hoặc khong_neu
    cum: str | None           # cụm làm nên kết luận (đã chuẩn hóa chữ thường), None với khong_neu
    goi_muc_cao: bool = False  # cụm thuộc tu_goi_muc_cao ("tối đa", "đỉnh", "cực đại", "peak")


def _nfc(chu):
    return unicodedata.normalize("NFC", chu)


# --- Số và đơn vị ---

def doc_so(chu):
    """Đọc số theo chuan_hoa.so. Dấu phẩy luôn là thập phân; dấu chấm theo sau đúng 3 chữ số là ngăn
    hàng nghìn ("3.000" = 3000, "1.234.567" = 1234567), theo sau số chữ số khác là thập phân ("4.5").
    Ngoại lệ ngoài YAML: phần nguyên 0 ("0.500") luôn là thập phân. Không phải số thì ValueError."""
    s = chu.strip()
    if not _SO.fullmatch(s):
        raise ValueError(f"không phải số: {chu!r}")
    if "," in s:
        nguyen, _, thap = s.rpartition(",")
        nhom = nguyen.split(".")
        if "," in nguyen or any(len(g) != 3 for g in nhom[1:]):
            raise ValueError(f"không phải số: {chu!r}")
        return float("".join(nhom) + "." + thap)
    nhom = s.split(".")
    if len(nhom) == 1:
        return float(s)
    if len(nhom) == 2:
        if len(nhom[1]) == 3 and nhom[0] != "0":
            return float(nhom[0] + nhom[1])
        return float(s)
    if all(len(g) == 3 for g in nhom[1:]):
        return float("".join(nhom))
    raise ValueError(f"không phải số: {chu!r}")


def _bang_don_vi(chung):
    """{cách viết đã chuẩn hóa chữ: khóa đơn vị} từ chuan_hoa.don_vi."""
    return {chuan_hoa_chu(a): khoa for khoa, ds in chung["chuan_hoa"]["don_vi"].items() for a in ds}


def chuan_don_vi(chu, chung):
    """Khóa đơn vị của một cách viết ("tiếng" -> gio, "nits" -> nit, "mét" -> m), không phân biệt hoa
    thường; None nếu không biết. Trong YAML chưa có cặp nào chỉ khác nhau ở hoa thường nên không có chỗ mơ hồ."""
    return _bang_don_vi(chung).get(chuan_hoa_chu(chu))


def quy_doi(gia_tri, tu, den):
    """Đổi giữa gio và phut (cùng đơn vị thì giữ nguyên); đơn vị khác thì ValueError."""
    if tu == den:
        return gia_tri
    if (tu, den) == ("gio", "phut"):
        return gia_tri * 60
    if (tu, den) == ("phut", "gio"):
        return gia_tri / 60
    raise ValueError(f"không đổi được {tu} sang {den}")


def tim_gia_tri(chu, chung):
    """Mọi cặp số + đơn vị trong chuỗi, có hoặc không có khoảng trắng ("30 giờ", "45W", "3000nits", "2x").
    Đơn vị dài khớp trước ("mAh" trước "m", "Hz" trước "h") và phải kết thúc ở ranh giới chữ nên "44mm" không
    thành "m"; con số không được dính chữ phía trước nên "IP68", "WR50", "G720" không ra giá trị. Mã IP và mã
    ISO 22810 do tach_ip, doc_iso_22810 đọc. "1x Arm" hay "2 x 3" cũng ra đơn vị x (zoom); việc loại do thuộc tính.
    Dạng "a / b <đơn vị>" và "a/b <đơn vị>" ("Đến 7,0/30 giờ") ra hai GiaTri cùng đơn vị, a rồi b; cả hai có
    dau_nhom là chỉ số đầu của a (a có dau, cuoi là của cả cụm, b có dau, cuoi riêng của b). Chữ dọc, mỗi mảnh một dòng
    (mỗi chữ "7", "/", "30", "giờ" một dòng), không khớp vì khoảng trắng giữa các mảnh không được là xuống dòng: nơi gọi gộp khoảng trắng trước.
    Ranh giới sau đơn vị: không còn ký tự chữ hay số, hoặc một chữ HOA theo sau bởi một chữ thường ("67WHỗ trợ" của dt-xiaomi-15t#005,
    lỗi chia đoạn làm dính từ viết hoa vào đơn vị; "2xZoom" cũng ra 2x). "44mm", "5G", "5000mAh" (mAh khớp trước m) không đổi."""
    chu = _nfc(chu)
    bang = _bang_don_vi(chung)
    don_vi = "|".join(re.escape(a) for a in sorted(bang, key=len, reverse=True))
    so_chu = r"[0-9]+(?:[.,][0-9]+)*"
    mau = re.compile(rf"(?<![\w.,])(?P<so>{so_chu})(?:[^\S\n]*/[^\S\n]*(?P<so2>{so_chu}))?[^\S\n]*(?P<dv>{don_vi})(?=(?P<sau>\w{{0,2}}))",
                     re.IGNORECASE)
    ket_qua = []
    for m in mau.finditer(chu):
        sau = m.group("sau")   # sau đơn vị: không còn chữ, hoặc chữ HOA rồi chữ thường ("67WHỗ trợ": từ viết hoa bị dính)
        if sau and not (len(sau) == 2 and sau[0].isupper() and sau[1].islower()):
            continue
        khoa = bang[chuan_hoa_chu(m.group("dv"))]
        try:
            so = doc_so(m.group("so"))
            so2 = doc_so(m.group("so2")) if m.group("so2") else None
        except ValueError:
            continue
        if so2 is None:
            ket_qua.append(GiaTri(so, khoa, m.group(0), m.start("so"), m.end("dv")))
        else:
            ket_qua.append(GiaTri(so, khoa, m.group(0), m.start("so"), m.end("dv"), m.start("so")))
            ket_qua.append(GiaTri(so2, khoa, chu[m.start("so2"):m.end("dv")], m.start("so2"), m.end("dv"), m.start("so")))
    return ket_qua


def tim_so(chu):
    """Mọi con số trong chuỗi (có hay không đơn vị), theo thứ tự xuất hiện, kèm vị trí. Con số không được dính chữ
    hay dấu ngăn phía trước nên "IP68", "WR50" không ra số; "3.000" và "4,5" là một số. Chuỗi số doc_so không đọc
    được ("1,234,567") bị bỏ."""
    chu = _nfc(chu)
    ket_qua = []
    for m in re.finditer(r"(?<![\w.,])[0-9]+(?:[.,][0-9]+)*", chu):
        try:
            ket_qua.append(So(doc_so(m.group(0)), m.group(0), m.start(), m.end()))
        except ValueError:
            continue
    return ket_qua


# --- Mã IP và ISO 22810 ---

def tach_ip(chu):
    """MaIP của mã IP đầu tiên trong chuỗi ("IP68" -> (6, 8), "IPX7" -> (None, 7), "IP6X" -> (6, None));
    None nếu không có. Chữ số nước chỉ nhận 0–8 (IP69K không thuộc cấu hình nên ra None)."""
    m = _MA_IP.search(_nfc(chu))
    if not m:
        return None
    return MaIP(*(None if c.upper() == "X" else int(c) for c in m.groups()))


def _thanh_phan(thu_tu, huong):
    """So hai chữ số cùng thang theo hướng thuận lợi: bang, kem_hon hoặc tot_hon (của tuyên bố)."""
    if thu_tu[0] == thu_tu[1]:
        return "bang"
    hon = thu_tu[0] > thu_tu[1]
    if huong == "thap_hon_tot_hon":
        hon = not hon
    return "tot_hon" if hon else "kem_hon"


def so_ip(tuyen_bo, tai_lieu, chung):
    """So mã IP theo chuan_hoa.ma_ip (hướng dẫn mục 6.6): bang, kem_hon, tot_hon hoặc khac_nhanh.
    Bụi là thang, cao hơn tốt hơn; nước chỉ so trong cùng nhánh (0–6 tia nước, 7–8 ngâm), khác nhánh là
    khac_nhanh (thắng mọi kết quả khác). Chữ số "X" ở bên nào thì bỏ thành phần đó. Thuận lợi hơn ở bất kỳ
    thành phần nào thì tot_hon (IP58 so IP67 là tot_hon). Không còn thành phần nào để so (IPX7 so IP6X) thì
    khac_nhanh. Nhận MaIP hoặc chuỗi chứa mã IP."""
    cau_hinh_ip = chung["chuan_hoa"]["ma_ip"]
    tb, tl = (m if isinstance(m, MaIP) else tach_ip(m) for m in (tuyen_bo, tai_lieu))
    if tb is None or tl is None:
        raise ValueError("không có mã IP để so")
    nhanh = {n: ten for ten, ds in cau_hinh_ip["chu_so_nuoc"].items() if ten.startswith("nhanh_") for n in ds}
    ket_qua = []
    if tb.bui is not None and tl.bui is not None:
        huong = cau_hinh_ip["chu_so_bui"]["huong"]
        ket_qua.append(_thanh_phan((tb.bui, tl.bui), huong))
    if tb.nuoc is not None and tl.nuoc is not None:
        if nhanh.get(tb.nuoc) != nhanh.get(tl.nuoc):
            return "khac_nhanh"
        ket_qua.append(_thanh_phan((tb.nuoc, tl.nuoc), "cao_hon_tot_hon"))
    if not ket_qua:
        return "khac_nhanh"
    if "tot_hon" in ket_qua:
        return "tot_hon"
    return "kem_hon" if "kem_hon" in ket_qua else "bang"


def doc_iso_22810(chu, chung):
    """Độ sâu (mét) của mã ISO 22810 đầu tiên có trong bảng chuan_hoa.iso_22810.quy_doi ("5ATM", "5 ATM",
    "WR50", "10ATM"); không tổng quát hóa ngoài bảng ("3ATM" ra None khi bảng không có)."""
    bang = {k.lower().replace(" ", ""): float(v) for k, v in chung["chuan_hoa"]["iso_22810"]["quy_doi"].items()}
    for m in _MA_ISO.finditer(_nfc(chu)):
        khoa = f"{m.group(1)}atm" if m.group(1) else f"wr{m.group(2)}"
        if khoa in bang:
            return bang[khoa]
    return None


# --- So sánh số ---

def nguong_bang(chung):
    return chung["dieu_kien_so"]["nguong_bang"]


def bang_nhau(a, b, nguong=NGUONG_BANG_MAC_DINH):
    """Bằng nhau trong sai số tương đối so với b (giá trị của tài liệu), như thoa_dieu_kien_so."""
    return abs(a - b) <= nguong * abs(b) + 1e-12


def so_huong(tuyen_bo, tai_lieu, huong, nguong=NGUONG_BANG_MAC_DINH):
    """bang (trong ngưỡng), kem_hon hoặc tot_hon của tuyên bố so với tài liệu theo hướng thuận lợi."""
    if huong not in HUONG_HOP_LE:
        raise ValueError(f"hướng không hợp lệ: {huong}")
    if bang_nhau(tuyen_bo, tai_lieu, nguong):
        return "bang"
    return _thanh_phan((tuyen_bo, tai_lieu), huong)


# --- Kiểu giá trị ---

def _cum_cua_muc(muc):
    """Danh sách cụm của một mục YAML {tu_tai_lieu: [...], hieu_biet_chung: [...]} hoặc của một danh sách."""
    if not muc:
        return []
    if isinstance(muc, dict):
        return [*(muc.get("tu_tai_lieu") or []), *(muc.get("hieu_biet_chung") or [])]
    return list(muc)


def _mau_cum(cum):
    """Biểu thức chính quy của một cụm đã chuẩn hóa: khoảng trắng bất kỳ giữa các từ, ranh giới chữ ở hai đầu
    (bỏ ranh giới ở đầu nào không phải chữ, vd. '(typ)' mở bằng ngoặc)."""
    than = r"\s+".join(re.escape(w) for w in cum.split(" "))
    dau = r"(?<!\w)" if re.match(r"\w", cum) else ""
    cuoi = r"(?!\w)" if re.search(r"\w$", cum) else ""
    return dau + than + cuoi


def _cum_muc_san(chung):
    """(cụm đứng trước số, cụm đứng sau số) từ tu_khang_dinh.tu_muc_san, tách mẫu '<số>'."""
    truoc, sau = [], []
    for mau in chung["tu_khang_dinh"].get("tu_muc_san") or []:
        mau = chuan_hoa_chu(mau)
        if mau.endswith("<số>"):
            truoc.append(mau[:-4].strip())
        elif mau.startswith("<số>"):
            sau.append(mau[4:].strip())
    return truoc, sau


def _khoang_bo_qua(c, chung):
    """Khoảng chữ mà từ khẳng định nằm trong đó thì không tính: bo_qua_khi_co ("không đảm bảo") và tên tính năng
    chứa từ khẳng định (ten_tinh_nang: "Màn hình Luôn Bật")."""
    tu_kd = chung["tu_khang_dinh"]
    return [m.span() for cum in [*(tu_kd.get("bo_qua_khi_co") or []), *(tu_kd.get("ten_tinh_nang") or [])]
            for m in re.finditer(_mau_cum(chuan_hoa_chu(cum)), c)]


def _khang_dinh(c, dau, cuoi, chung):
    """Cụm khẳng định gắn với con số ở [dau, cuoi), hoặc None.
    Quy ước: nhóm chắc chắn (tu_khang_dinh.tu) chỉ cần đứng trước số, cho phép tối đa SO_TOI_DA_TU_GIUA từ
    chỉ gồm chữ giữa từ và số ("luôn đạt 120Hz"); giữa chúng không được có chữ số hay dấu câu nên con số khác
    cắt đứt sự gắn kết. Nhóm mức sàn đứng liền số (khoảng trắng hoặc ':'): "hơn 16 giờ" ở trước,
    "18 giờ trở lên" ở sau. Cụm nằm trong bo_qua_khi_co ("không đảm bảo") hay trong tên tính năng ten_tinh_nang ("Màn hình Luôn Bật") bị bỏ qua. Lưu ý: "40W trở lên" của
    bộ tiếp hợp cũng ra khang_dinh ở đây; bộ quyết định chỉ hỏi con số của giá trị, không hỏi con số điều kiện."""
    truoc, sau = c[:dau], c[cuoi:]
    bo_qua = _khoang_bo_qua(c, chung)

    def hop_le(dau_cum, cuoi_cum):
        return not any(a <= dau_cum and cuoi_cum <= b for a, b in bo_qua)

    tu_gia = rf"(?:\s+[^\W\d_]+){{0,{SO_TOI_DA_TU_GIUA}}}"
    for cum in chung["tu_khang_dinh"].get("tu") or []:
        cum = chuan_hoa_chu(cum)
        m = re.search(_mau_cum(cum) + tu_gia + r"[\s:]*\Z", truoc)
        if m and hop_le(m.start(), m.start() + len(cum)):
            return cum
    cum_truoc, cum_sau = _cum_muc_san(chung)
    for cum in cum_truoc:
        m = re.search(_mau_cum(cum) + r"[\s:]*\Z", truoc)
        if m and hop_le(m.start(), m.end()):
            return cum
    for cum in cum_sau:
        m = re.match(r"\s*" + _mau_cum(cum), sau)
        if m and hop_le(cuoi + m.end() - len(cum), cuoi + m.end()):
            return cum
    return None


def tim_kieu_gia_tri(cau, gia_tri, chung, cum_them=None):
    """Kiểu giá trị của một giá trị trong câu theo T5.4: khang_dinh, toi_da, dien_hinh, dinh_muc, thich_ung
    hoặc khong_neu. Chỉ xét cụm đứng liền con số của chính giá trị (không xét cụm gắn với con số khác).
    Cụm phía trước: khoảng trắng hoặc ':' giữa cụm và số. Cụm phía sau (ngay sau số + đơn vị): trong ngoặc
    ("5500mAh (typ)"), hoặc không ngoặc nhưng chỉ với cụm không phải toi_da và không phải chữ gọi mức cao
    ("đến", "tối đa", "đỉnh" đứng sau số là của số kế tiếp: "50% đến 80%"). Thứ tự: khẳng định (xem _khang_dinh),
    cụm của kieu_gia_tri và cum_them, chữ gọi mức cao, rồi khong_neu. goi_muc_cao=True khi cụm thuộc
    tu_goi_muc_cao; chữ chỉ thuộc tu_goi_muc_cao ("đỉnh") cho kiểu tu_goi_muc_cao.mot_gia_tri (toi_da).
    cum_them: cụm riêng của nhóm, nhận mục YAML {kieu: {tu_tai_lieu, hieu_biet_chung}} như
    cach_dien_dat.kieu_dung_luong hoặc {kieu: [cụm]}."""
    c = _nfc(cau).lower()
    # "a / b <đơn vị>": cụm đứng liền trước a áp cho cả b ("Đến 7 / 30 giờ"), nên b lấy vị trí đầu của a.
    dau = gia_tri.dau if gia_tri.dau_nhom is None else gia_tri.dau_nhom
    cuoi = gia_tri.cuoi
    cum = _khang_dinh(c, dau, cuoi, chung)
    if cum:
        return KieuGiaTri("khang_dinh", cum, False)

    goi = {chuan_hoa_chu(t) for t in _cum_cua_muc(chung.get("tu_goi_muc_cao"))}
    ung_vien = {}   # cụm đã chuẩn hóa -> kiểu
    for nguon in (chung["kieu_gia_tri"], cum_them or {}):
        for kieu, muc in nguon.items():
            for t in _cum_cua_muc(muc):
                ung_vien[chuan_hoa_chu(t)] = kieu
    kieu_mot_gia_tri = (chung.get("tu_goi_muc_cao") or {}).get("mot_gia_tri", "toi_da")
    for t in goi:
        ung_vien.setdefault(t, kieu_mot_gia_tri)

    truoc, sau = c[:dau], c[cuoi:]
    tot = None   # (cụm, kiểu); cụm dài nhất thắng
    for t, kieu in ung_vien.items():
        mau = _mau_cum(t)
        co = bool(re.search(mau + r"[\s:]*\Z", truoc))
        if not co:
            sau_cum = re.match(r"\s*" + mau, sau)
            co = bool(sau_cum and (t.startswith("(") or kieu != kieu_mot_gia_tri and t not in goi)
                      or re.match(r"\s*\(\s*" + mau, sau))
        if co and (tot is None or len(t) > len(tot[0])):
            tot = (t, kieu)
    if tot:
        return KieuGiaTri(tot[1], tot[0], tot[0] in goi)
    return KieuGiaTri("khong_neu", None, False)


# --- Tên sản phẩm và phiên bản ---

def _tim_cum_trong(chu, cum):
    return [m.span() for m in re.finditer(_mau_cum(cum), chu)]


def tim_san_pham(chu, cac_cau_hinh):
    """ma_mau của sản phẩm được nhắc tới trong chuỗi, hoặc None. cac_cau_hinh: các cấu hình nhóm
    (doc_cau_hinh). Khớp bí danh trong khóa san_pham, không phân biệt hoa thường, có ranh giới chữ; khớp
    dài nhất trong hợp của bi_danh và khong_nham_voi thắng (bằng độ dài thì bi_danh thắng, rồi vị trí đầu).
    Khớp dài nhất là một khong_nham_voi thì None ("iPhone 17 Pro"); "Apple Watch SE 3" dài hơn "Apple Watch SE".
    Chuỗi nhắc cả hai ("Galaxy Buds3/Buds3 Pro") theo khớp dài nhất, không tách theo từng vị trí."""
    c = chuan_hoa_chu(chu)
    tot = None   # (độ dài, là bí danh, -vị trí, ma_mau)
    for cau_hinh in cac_cau_hinh:
        for ma, sp in (cau_hinh.get("san_pham") or {}).items():
            for ten, la_bi_danh in ((sp.get("bi_danh") or [], True), (sp.get("khong_nham_voi") or [], False)):
                for t in ten:
                    t = chuan_hoa_chu(t)
                    for dau, _ in _tim_cum_trong(c, t):
                        khoa = (len(t), la_bi_danh, -dau, ma)
                        if tot is None or khoa[:3] > tot[:3]:
                            tot = khoa
    return tot[3] if tot and tot[1] else None


def tim_phien_ban(chu, ma_mau, cac_cau_hinh):
    """Khóa phiên bản (bi_danh_phien_ban của mẫu) có trong chuỗi, theo thứ tự xuất hiện, không trùng. Cách viết
    dài khớp trước nên "GPS + Cellular" chỉ ra gps_cellular, không kèm gps. Mẫu không có bảng thì list rỗng."""
    c = chuan_hoa_chu(chu)
    bang = {}
    for cau_hinh in cac_cau_hinh:
        sp = (cau_hinh.get("san_pham") or {}).get(ma_mau)
        if sp:
            bang = sp.get("bi_danh_phien_ban") or {}
    cac_cum = sorted(((chuan_hoa_chu(t), khoa) for khoa, ds in bang.items() for t in ds), key=lambda x: -len(x[0]))
    da_chiem, tim_thay = [], []
    for t, khoa in cac_cum:
        for dau, cuoi in _tim_cum_trong(c, t):
            if any(dau < b and a < cuoi for a, b in da_chiem):
                continue
            da_chiem.append((dau, cuoi))
            tim_thay.append((dau, khoa))
    ket_qua = []
    for _, khoa in sorted(tim_thay):
        if khoa not in ket_qua:
            ket_qua.append(khoa)
    return ket_qua
