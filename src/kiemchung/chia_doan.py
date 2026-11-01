"""Chia page.txt thành đoạn cho BM25 (Bước 7).

Mỗi đoạn là một cụm dòng liền nhau của một mục thông số kèm chú thích của nó, để con số không bị
tách khỏi điều kiện. Chỉ có hàm thuần (nhận chuỗi, trả list); scripts/chia_doan.py lo đọc/ghi tệp.

Luật tách được thiết kế chỉ dựa trên 4 mẫu tập phát triển (T3.5, quy tắc 4); tập kiểm tra chỉ được
sửa phần đọc định dạng chung (vd. dòng '=== Trang N ===' của PDF). Các chỗ đã sửa sau khi chạy
thử trên tập kiểm tra, đều thuộc phần đọc định dạng: bỏ nhãn <button> khi lấy chú thích từ HTML;
nhận data-sup="N" như data-sup="sup-N"; lấy danh sách <ol> dài nhất làm chú thích khi thẻ không ghi
số; bỏ qua số lớn hơn mọi số chú thích đang có ('Reno16'); danh sách số cách chữ phải có ', ' ('4,35'
là số thập phân); dấu * đứng sau khoảng trắng hoặc '(' không mở chú thích ('(*Bật AOD)'); dòng văn
xuôi dài hơn CAP_CUNG chia theo câu.

Sửa lần 2 (theo kết quả kiểm 20 đoạn lần 1): số hiển thị của chú thích lấy từ liên kết ký hiệu trong
HTML (mã trong thẻ <li> có thể lệch số hiển thị); nhóm số cuối dòng sau dấu kết câu ('năng lượng! 7',
'hơn. 10', 'hóa. 2,5', 'đệm. 40, 41, 42 43, 44') nhận không xét thứ tự; số dính cuối chữ ở cuối dòng cũng
nhận không xét thứ tự nếu có trong danh sách chú thích, trừ tên máy ('Galaxy Watch7') và tên chuẩn
('AV1'); số dính vào chữ số khác ('thứ 210', 'Wi-Fi 617, 18') chỉ nhận khi đúng là số chú thích kế tiếp;
chú thích đứng lẻ giữa trang mà không ký hiệu nào dẫn tới thì gắn vào đoạn phía trên.

Sửa lần 3 (31/10/2026, trước khi người gán nhãn đọc tài liệu): ký hiệu chú thích đã nhận ra (số dính chữ
'Thấp8', nhóm số cuối dòng ' 1, 4, 5', dấu * và ** làm ký hiệu hoặc mở chú thích nối liền) bị bỏ khỏi
noi_dung để không bị đọc nhầm thành số liệu ('20 phút6' -> '20 phút'); noi_dung_goc giữ nguyên văn bản
trước khi bỏ. Chỉ bỏ đúng các khoảng chuan_bi_manh() đã dùng để gắn chú thích, không có bộ nhận diện
riêng: số không được nhận ra ('IP68', 'Buds3', 'A2305', '5.000mAh') vẫn ở lại. Bỏ xong, hai bên chữ vẫn
cách nhau đúng một khoảng trắng như cũ (xem bo_ky_hieu_chu_thich). Hai loại dấu * được nhận ra (để gắn chú
thích) nhưng không bỏ: dấu mà trang không có dòng chú thích nào bắt đầu bằng đúng chuỗi đó ('5* product' của một
lời đánh giá) và dấu đứng riêng giữa hai khoảng trắng ('Chú thích * biểu tượng', nhãn đọc màn hình).
Nhận diện của chuan_bi_manh vẫn bỏ sót một số ký hiệu thật ('30 phút6' nhắc lại giữa dòng, 'AI10', số dính chữ ở
trang S25 Ultra); các chỗ đó bỏ bằng bảng ghi tay KY_HIEU_BO_THEM, và dấu '5*' của một lời đánh giá giữ lại bằng
KY_HIEU_GIU_LAI (xem ap_dung_bang_ghi_tay; hai bảng chỉ đổi noi_dung, không đổi chu_thich). Luật tách đoạn không đổi: mọi trường khác của đoạn (id, muc, chu_thich, dong) giống hệt trước khi bỏ ký hiệu, nên muc của
tiêu đề có số cách chữ hoặc sau ')' ('Định nghĩa lại âm thanh nguyên bản 1') vẫn còn số như cũ.

Ba phần: (1) đọc chú thích (số, dấu *, chú thích nối liền trong dòng), (2) tách đoạn theo mục,
(3) gắn tên mục và chú thích vào từng đoạn, bỏ ký hiệu khỏi noi_dung.
"""
from dataclasses import dataclass, replace
import html
import re
import unicodedata

DONG_TRANG_PDF = re.compile(r"^=== Trang (\d+) ===$")
# Chữ giao diện không mang thông số; giữ danh sách này ngắn (thà giữ thừa còn hơn bỏ sót).
DONG_RAC = frozenset({"Skip to content", "Play", "Previous", "Next", "close", "Layer popup open",
                      "Open Tooltip Layer"})
DONG_GIU = frozenset({"/"})  # dòng không chữ không số nhưng mang nghĩa: 'Đến 7 / 30 giờ'
# Đơn vị dính sau số ('120Hz', '256GB'), không phải chỗ hai mục dính nhau.
DON_VI_SAU_SO = frozenset({"Hz", "Mbps", "Gbps", "Kbps", "Mb", "Kb", "Wh", "Ah", "GB", "MB", "KB", "TB", "MP"})
GIA_TRI_CO_CHU = frozenset({"có", "không", "support", "not support", "yes", "no"})

CAP = 600          # độ dài mục tiêu của một đoạn (ký tự)
CAP_CUNG = 1400    # quá mức này thì buộc cắt dù chỗ cắt không đẹp
TOI_THIEU = 150    # đoạn chưa dài tới mức này thì tiêu đề mới không mở đoạn mới
DAI = 100          # dòng dài từ mức này: văn xuôi hoặc dòng dồn nhiều mục
TIEU_DE_TOI_DA = 80
KHOANG_NHAY_SO = 3  # số chú thích mới xuất hiện không nhảy quá chừng này so với số cao nhất đã thấy
MIN_KIEU_CACH = 3   # số dòng 'N, N, N' cuối dòng để coi trang dùng kiểu ký hiệu cách chữ

SO_DAU_DONG = re.compile(r"^(\d{1,3})\.\s+(\S.*)$")
# Nhóm số ký hiệu ở cuối dòng (số cách chữ). '4,35' đứng sau chữ là số thập phân nên chỉ nhận danh sách
# có ', ' hoặc đứng sau dấu kết câu.
NHOM_CACH = re.compile(r"(?<=\s)(\d{1,2}(?:,\s+\d{1,2})+)\s*$")  # 'mới 1, 4, 5'
# 'năng lượng! 7', 'hóa. 2,5', 'đệm. 40, 41, 42 43, 44' (hai cụm ký hiệu liền nhau)
NHOM_SAU_CAU = re.compile(r"(?<=[.!?…”’]\s)(\d{1,2}(?:,?\s*\d{1,2})*)\s*$")
NHOM_DINH_CAU = re.compile(r"(?<=[^\W\d_][.!?…])(\d{1,2}(?:,\d{1,2})*)$")  # 'giải trí.4,32'
SO_DINH_CHU = re.compile(r"(?:(?<=[^\W\d_])|(?<=[)%])|(?<=[^\W\d_][.,;:]))(\d{1,2})(?!\w|[.,]\d)")
SO_NGUYEN = re.compile(r"\d+")
DAU_CAU_DONG = ".,;:!?)"          # dấu câu không đứng sau khoảng trắng khi bỏ ký hiệu đứng giữa
DAU_CAU_DONG_TRUOC = ".,;:!?)%”’\"]®™"  # ký tự kết thúc một cụm mà chữ sau nó phải cách ra
DAU_SAO = re.compile(r"\*+")
# Nhãn mới bắt đầu ngay sau chỗ dính: 'Gam màu:' (từ thường, tối đa 6 từ rồi dấu ':') hoặc 'GPU:', 'LTE FDD:' (chữ hoa).
CO_NHAN_THUONG = re.compile(r"[^\s:|]+(?:\s+[^\s:|]+){0,5}:")
CO_NHAN_HOA = re.compile(r"[A-Z][A-Z0-9]+(?:\s+[A-Z0-9]+)?:")
LI_CHU_THICH = re.compile(r"<li\b[^>]*?(?:\bid=\"footnote-(\d+)\"|\bdata-sup=\"(?:sup-)?(\d+)\")[^>]*>(.*?)</li>",
                          re.S)
LIEN_KET_KY_HIEU = re.compile(r"<a\b[^>]*\bdata-sup(?:-tag)?=\"(?:sup-)?(\d+)\"[^>]*>(.*?)</a>", re.S)
DANH_SACH_THU_TU = re.compile(r"<ol\b[^>]*>(.*?)</ol>", re.S)
MUC_DANH_SACH = re.compile(r"<li\b[^>]*>(.*?)</li>", re.S)
MIN_MUC_DANH_SACH = 3  # danh sách <ol> ngắn hơn không coi là khối chú thích


@dataclass(frozen=True)
class Dong:
    so: int            # số dòng (từ 1) trong tệp gốc
    chu: str | None    # None: dòng phân trang PDF


KY_HIEU_SO = "so"                      # số chú thích: 'Thấp8', ' 1, 4, 5'
KY_HIEU_SAO = "sao"                    # dấu * làm ký hiệu: 'IP68**', '24 tháng.*'
KY_HIEU_SAO_NOI_LIEN = "sao_noi_lien"  # dấu * mở chú thích nối liền: '194g*' (nội dung chú thích đã bóc đi)
KY_HIEU_GHI_TAY = "ghi_tay"            # số chú thích bỏ thêm theo bảng KY_HIEU_BO_THEM (nhận diện của chuan_bi_manh bỏ sót)


@dataclass(frozen=True)
class KhoangBo:
    """Một cụm ký hiệu chú thích nằm trong chữ, sẽ bị bỏ khỏi noi_dung (noi_dung_goc vẫn giữ)."""
    a: int             # vị trí bắt đầu: trong chu của mảnh, hoặc trong noi_dung_goc của đoạn
    b: int             # vị trí kết thúc (không gồm)
    loai: str          # KY_HIEU_SO, KY_HIEU_SAO, KY_HIEU_SAO_NOI_LIEN hoặc KY_HIEU_GHI_TAY
    so: tuple = ()     # các số chú thích trong cụm ('14, 15' là hai số)
    thieu: tuple = ()  # trong đó số mà trang không có nội dung chú thích tương ứng


@dataclass(frozen=True)
class Manh:
    """Một dòng, hoặc một mảnh của dòng dồn; đơn vị để gom thành đoạn."""
    chi_so: int        # vị trí dòng trong danh sách Dong
    so: int
    chu: str
    noi_truoc: bool = False   # mảnh tiếp liền mảnh trước của cùng một dòng
    dac: bool = False         # dòng dồn nhiều mục hoặc có chú thích nối liền: coi như dòng dài
    ky_hieu: tuple = ()       # số chú thích xuất hiện ở đây
    dau_sao: tuple = ()       # chuỗi * dùng làm ký hiệu
    chu_thich_dong: tuple = ()  # chú thích nối liền trong dòng (đã bóc ra khỏi chu)
    bo: tuple = ()            # KhoangBo (tính trong chu) của mọi ký hiệu ở đây, để bỏ khỏi noi_dung


# --- Đọc dòng ---

KY_TU_AN = re.compile(r"[\u00ad\u200b-\u200d\u2060\ufeff]")  # g\u1ea1ch m\u1ec1m, k\u00fd t\u1ef1 \u0111\u1ed9 r\u1ed9ng 0
GACH_DAC_BIET = re.compile(r"[\u2010\u2011]")  # 'sub\u20116' (g\u1ea1ch kh\u00f4ng ng\u1eaft) -> 'sub-6'


def lam_sach(dong):
    """NFC tr\u01b0\u1edbc: trang OPPO/Xiaomi c\u00f3 ch\u1eef Vi\u1ec7t d\u1ea1ng d\u1ea5u t\u00e1ch r\u1eddi (NFD), nh\u00ecn gi\u1ed1ng
    nh\u01b0ng kh\u00f4ng kh\u1edbp khi t\u00ecm ki\u1ebfm."""
    dong = unicodedata.normalize("NFC", dong)
    dong = GACH_DAC_BIET.sub("-", KY_TU_AN.sub("", dong))
    return re.sub(r"\s+", " ", dong).strip()


def doc_dong(van_ban):
    """Dòng còn lại sau khi bỏ dòng rỗng/không chữ không số, dòng giao diện, dòng lặp liền nhau.
    Dòng '=== Trang N ===' của PDF giữ lại với chu=None để làm chỗ ngắt."""
    ket_qua, truoc = [], None
    for so, goc in enumerate(van_ban.replace("\r\n", "\n").split("\n"), start=1):
        s = lam_sach(goc)
        if DONG_TRANG_PDF.match(s):
            ket_qua.append(Dong(so, None))
            truoc = None
            continue
        if not any(c.isalnum() for c in s) and s not in DONG_GIU:
            continue
        if s in DONG_RAC or s == truoc:
            continue
        ket_qua.append(Dong(so, s))
        truoc = s
    return ket_qua


# --- Phần 1: đọc chú thích ---

def van_ban_cua_html(ma_html):
    """Chữ nhìn thấy của một đoạn HTML: bỏ nhãn nút ('Quay lại Địa điểm'), thẻ, ký tự &-escape."""
    ma_html = re.sub(r"<button\b.*?</button>", " ", ma_html, flags=re.S)
    return lam_sach(html.unescape(re.sub(r"<[^>]+>", " ", ma_html)))


def nhan_hien_thi_html(ma_html):
    """{mã trong thẻ: số hiển thị} từ các liên kết ký hiệu <a data-sup-tag="sup-58">56</a>.

    Số người đọc thấy không phải lúc nào cũng bằng mã trong thẻ <li>: Samsung bỏ qua mã thiếu nên
    mã 58 hiện là 56. Nhãn không phải một số (ví dụ '8,9,10,') thì giữ mã làm số hiển thị.
    """
    nhan = {}
    for m in LIEN_KET_KY_HIEU.finditer(ma_html):
        chu = van_ban_cua_html(m.group(2))
        if re.fullmatch(r"\d{1,2}", chu):
            nhan.setdefault(int(m.group(1)), int(chu))
    return nhan


def doc_chu_thich_html(ma_html):
    """{số: nội dung} từ danh sách chú thích đánh số trong page.html.

    page.txt không mang số thứ tự chú thích (số do danh sách HTML tự sinh) và Samsung có chú thích
    bị xuống hàng, nên số phải lấy từ page.html: Apple <li id="footnote-N">, Samsung <li data-sup="N">
    hoặc "sup-N", đổi sang số hiển thị theo liên kết ký hiệu. Trang không ghi số trong thẻ thì lấy danh
    sách <ol> dài nhất, đánh số theo thứ tự.
    """
    nhan = nhan_hien_thi_html(ma_html)
    bang = {}
    for m in LI_CHU_THICH.finditer(ma_html):
        so = int(m.group(1) or m.group(2))
        noi_dung = van_ban_cua_html(m.group(3))
        so = nhan.get(so, so)
        if so > 0 and noi_dung and so not in bang:
            bang[so] = noi_dung
    if not bang:
        danh_sach = [MUC_DANH_SACH.findall(m.group(1)) for m in DANH_SACH_THU_TU.finditer(ma_html)]
        dai_nhat = max(danh_sach, key=len, default=[])
        if len(dai_nhat) >= MIN_MUC_DANH_SACH:
            bang = {so: van_ban_cua_html(x) for so, x in enumerate(dai_nhat, start=1) if van_ban_cua_html(x)}
    return bang


def khoa_so_khop(s):
    return "".join(c for c in s if c.isalnum()).casefold()


def khop_chu_thich_html(dong, bang):
    """Tìm dòng của từng chú thích trong page.txt: {số: [chỉ số dòng]}.

    Duyệt từ cuối lên vì khối chú thích nằm cuối trang và cùng thứ tự với danh sách; so khớp theo
    chữ-số (bỏ khoảng trắng, dấu) để chịu được khác biệt nhỏ giữa HTML và văn bản hiển thị.
    Chú thích bị xuống hàng thành nhiều dòng thì gom các dòng liền nhau.
    """
    vi_tri, con_tro = {}, len(dong)
    khoa_dong = [khoa_so_khop(d.chu) if d.chu else "" for d in dong]
    for so in sorted(bang, reverse=True):
        dich = khoa_so_khop(bang[so])
        for j in range(con_tro - 1, -1, -1):
            if not khoa_dong[j] or not dich.startswith(khoa_dong[j]):
                continue
            gop, k = khoa_dong[j], j
            while len(gop) < len(dich) and k + 1 < con_tro and khoa_dong[k + 1]:
                k += 1
                gop += khoa_dong[k]
            if gop == dich:
                vi_tri[so] = list(range(j, k + 1))
                con_tro = j
                break
    return vi_tri


def vi_tri_ranh_gioi(chu, tu=0):
    """Chỗ hai mục dính liền nhau không có khoảng trắng ('194g*Dữ', '30 phút.Băng', 'mmChiều').

    Trả [(chỉ số, co_nhan)]; co_nhan: ngay sau có nhãn kết thúc bằng ':' ('Gam màu:', 'GPU:'), tức chắc
    chắn là nhãn mới bắt đầu. Chữ thường ASCII dính chữ hoa không nhãn ('MediaTek', 'MoMo') không tính
    là ranh giới; chữ thường của từ có dấu tiếng Việt ('hìnhMở', 'phẳngCorning') thì tính.
    """
    ket_qua = []
    for i in range(max(tu, 1), len(chu)):
        c, truoc = chu[i], chu[i - 1]
        if not c.isupper() or truoc.isupper() or truoc.isspace():
            continue
        sau_la_thuong = i + 1 < len(chu) and chu[i + 1].islower()
        if sau_la_thuong:
            co_nhan = bool(CO_NHAN_THUONG.match(chu, i))
        else:
            co_nhan = bool(CO_NHAN_HOA.match(chu, i))
            if not co_nhan:
                continue
        if truoc.isdigit() and any(chu.startswith(u, i) and not chu[i + len(u):i + len(u) + 1].islower()
                                   for u in DON_VI_SAU_SO):
            continue  # '120Hz'
        if truoc in ".!?…":
            if i >= 2 and chu[i - 2].isupper() and (i < 3 or not chu[i - 3].isalpha()):
                continue  # viết tắt kiểu 'U.S.A'
            hop_le = True
        elif truoc.isdigit() or truoc in ")%®™\"”’]:":
            hop_le = True
        elif truoc.islower():
            k = i
            while k > 0 and chu[k - 1].isalpha():
                k -= 1
            tu_truoc = chu[k:i]
            if sau_la_thuong:
                hop_le = co_nhan or not tu_truoc.isascii()
            else:  # nhãn chữ hoa ('GPU:') dính sau số liệu có đơn vị ('2,1GHz'), không phải sau chữ ('NavIC:')
                m_so = re.search(r"[\w,.]*$", chu[:i])
                hop_le = any(ch.isdigit() for ch in m_so.group())
        else:
            hop_le = False
        if hop_le:
            ket_qua.append((i, co_nhan))
    return ket_qua


def ket_thuc_chu_thich_noi_lien(chu, bat_dau):
    """Chỉ số kết thúc chú thích nối liền sau dấu * (ví dụ '...194g*Dữ liệu do...khác.').

    Kết thúc ở dấu * kế tiếp, hoặc ở chỗ một nhãn mới bắt đầu; không có thì hết dòng. Chú thích nhiều
    đoạn ('...2013.Vui lòng lưu ý...') được giữ nguyên vì chỗ dính chữ sau dấu chấm chưa chắc là nhãn.
    """
    ket = len(chu)
    m = DAU_SAO.search(chu, bat_dau)
    if m:
        ket = m.start()
    for i, co_nhan in vi_tri_ranh_gioi(chu, bat_dau):
        if co_nhan and i < ket:
            return i
    return ket


def tach_dau_sao(dong_chu):
    """Tách dấu * khỏi một dòng.

    Trả (chu còn lại, [(chuỗi *, vị trí)] làm ký hiệu, [(chuỗi *, nội dung chú thích nối liền, vị trí)],
    chú thích cả dòng). Vị trí tính trong chu còn lại. '*' là ký hiệu khi không có chữ liền sau
    ('...24 tháng.*'); '*' dính liền chữ sau nó mở một chú thích ('194g*Dữ liệu...'). Dòng bắt đầu bằng
    '*' là chú thích cả dòng, tách riêng, không gắn vào dòng nào.
    """
    if not dong_chu or "*" not in dong_chu:
        return dong_chu, [], [], None
    dau_dong = DAU_SAO.match(dong_chu)
    if dau_dong and dong_chu[dau_dong.end():].strip():
        return "", [], [], (dau_dong.group(), dong_chu[dau_dong.end():].strip())
    con_lai, ky_hieu, noi_lien, cuoi, dai = [], [], [], 0, 0
    for m in DAU_SAO.finditer(dong_chu):
        if m.start() < cuoi:
            continue
        sau = dong_chu[m.end():m.end() + 1]
        truoc = dong_chu[m.start() - 1] if m.start() else ""
        if sau and sau.isalnum() and (not truoc or truoc in " ([{“\"'"):
            continue  # '(*Bật AOD)': dấu * mở đầu một cụm chữ trong dòng, không phải chú thích
        if sau and sau.isalnum():
            ket = ket_thuc_chu_thich_noi_lien(dong_chu, m.end())
            con_lai.append(dong_chu[cuoi:m.end()])
            dai += m.end() - cuoi
            noi_lien.append((m.group(), dong_chu[m.end():ket].strip(), dai - 1))
            cuoi = ket
        else:
            ky_hieu.append((m.group(), dai + m.start() - cuoi))
    con_lai.append(dong_chu[cuoi:])
    chu = "".join(con_lai)
    lech = len(chu) - len(chu.lstrip())
    return chu.strip(), [(r, v - lech) for r, v in ky_hieu], [(r, t, v - lech) for r, t, v in noi_lien], None


def nhom_so_cuoi(chu):
    """(vị trí, [số]) của nhóm số ký hiệu cách chữ hoặc đứng sau dấu kết câu ở cuối dòng, hoặc None.

    'mới 1, 4, 5' (Samsung), 'năng lượng! 7' và 'hơn. 10' (OPPO), 'hóa. 2,5', 'giải trí.4,32'.
    """
    for mau in (NHOM_SAU_CAU, NHOM_CACH, NHOM_DINH_CAU):
        m = mau.search(chu)
        if m:
            return m.start(1), [int(x) for x in re.findall(r"\d+", m.group(1))]
    return None


def bo_ky_hieu_cuoi(chu):
    """Bỏ ký hiệu chú thích ở cuối tên mục: dấu *, số dính chữ, nhóm số ' 1, 4, 5'."""
    t = chu.rstrip("* ")
    nhom = nhom_so_cuoi(t)
    if nhom:
        t = t[:nhom[0]].rstrip()
    return re.sub(r"(?<=[^\W\d_])\d{1,2}$", "", t)


def khoang_nhom_cuoi(chu, bat_dau, so_lon_nhat):
    """[(a, b, [số])] của nhóm số ký hiệu ở cuối dòng bắt đầu từ vị trí bat_dau (xem nhom_so_cuoi).

    Mỗi khoảng là một cụm số liền nhau ('1, 4, 5', '40, 41, 42 43, 44'). Số lớn hơn so_lon_nhat không phải
    ký hiệu (chuan_bi_manh bỏ qua chúng) nên cắt cụm ra, để không bỏ nhầm.
    """
    ket_qua = []
    cum = None
    for m in SO_NGUYEN.finditer(chu, bat_dau):
        k = int(m.group())
        if k > so_lon_nhat:
            cum = None
        elif cum is not None and not chu[cum[1]:m.start()].strip(", "):
            cum[1] = m.end()
            cum[2].append(k)
        else:
            cum = [m.start(), m.end(), [k]]
            ket_qua.append(cum)
    return [tuple(c) for c in ket_qua]


def ung_vien_so_dinh_chu(chu):
    """[(số, ở cuối dòng, vị trí, vị trí kết thúc)] của các số đứng cuối từ và dính liền chữ cái ('Điện5', 'MIMO8')."""
    ket_qua = []
    for m in SO_DINH_CHU.finditer(chu):
        s = m.start(1)
        if chu[s - 1].isalpha() and (s < 2 or not chu[s - 2].isalpha()):
            if not (chu[s - 1].isupper() and s >= 2 and chu[s - 2].isdigit()):
                continue
        o_cuoi_dong = not chu[m.end(1):].strip(" .,;:)")
        ket_qua.append((int(m.group(1)), o_cuoi_dong, s, m.end(1)))
    return ket_qua


def so_chu_thich_dinh_chu(chu):
    """[(số, ở cuối dòng)] của các số đứng cuối từ và dính liền chữ cái ('Điện5', 'MIMO8', 'Va Chạm7').

    Không lấy số liệu: '120Hz', '48MP', 'iPhone 17', 'v5.4' không là chữ số cuối từ dính chữ (hoặc là số
    thập phân/4 chữ số). Loại mã kiểu 'A19', 'N1', 'n8' (một chữ cái rồi số) trừ khi chữ hoa đứng ngay
    sau số ('25W6', đơn vị rồi ký hiệu). Mã như 'IP68' hay 'Qi2' còn lọt qua hàm này; chuan_bi_manh() loại
    chúng bằng thứ tự xuất hiện của số chú thích.
    """
    return [(k, o_cuoi) for k, o_cuoi, _, _ in ung_vien_so_dinh_chu(chu)]


def so_chu_thich_cach_chu(chu):
    """Các số của nhóm số ký hiệu ở cuối dòng (xem nhom_so_cuoi): [] nếu không có."""
    nhom = nhom_so_cuoi(chu)
    return nhom[1] if nhom else []


def la_ten_ma_ngan(chu):
    """Dòng ngắn chỉ có chữ không dấu, mỗi từ viết hoa ('Galaxy Watch7', 'OPPO Enco Buds3'): tên máy,
    số cuối dòng là số của tên chứ không phải ký hiệu chú thích."""
    tu = chu.split()
    return chu.isascii() and len(tu) <= 4 and all(w[0].isupper() or w[0].isdigit() for w in tu)


def la_ma_tieu_chuan(chu, vi_tri):
    """Số ở vi_tri dính sau 2-3 chữ hoa liền nhau ('AV1', 'USB3'): tên chuẩn/codec, không phải ký hiệu."""
    j = vi_tri
    while j > 0 and chu[j - 1].isalpha():
        j -= 1
    chu_truoc = chu[j:vi_tri]
    return chu_truoc.isupper() and 2 <= len(chu_truoc) <= 3


def khoang_ke_tiep_cuoi_dong(chu, ky_vong, bang):
    """(a, b, [số]) của ký hiệu dính vào một chữ số khác ở cuối dòng và chính là số chú thích kế tiếp, hoặc None.

    'thế hệ thứ 210' (số 2 rồi ký hiệu 10), 'Wi-Fi 617, 18' (số 6 rồi ký hiệu 17, 18). Chỉ nhận số có 3
    chữ số mà hai chữ số cuối đúng bằng số chú thích kế tiếp (từ 10) có trong bang, nên số liệu
    thường hiếm khi bị nhận nhầm. [a, b) là phần ký hiệu ('10', '17, 18'), không gồm chữ số của số liệu.
    """
    m = re.search(r"(?<=\s)(\d{3})((?:,\s*\d{1,2})*)$", chu)
    if m and ky_vong >= 10 and int(m.group(1)[-2:]) == ky_vong and ky_vong in bang:
        dem = [ky_vong] + [int(x) for x in re.findall(r"\d+", m.group(2))]
        if dem == list(range(ky_vong, ky_vong + len(dem))) and all(k in bang for k in dem):
            return m.end(1) - 2, m.end(), dem
    return None


def so_ke_tiep_cuoi_dong(chu, ky_vong, bang):
    """[(số, vị trí)] của ký hiệu dính vào một chữ số khác ở cuối dòng và là số chú thích kế tiếp
    (xem khoang_ke_tiep_cuoi_dong); vị trí là chỗ kết thúc số liệu đứng trước."""
    kq = khoang_ke_tiep_cuoi_dong(chu, ky_vong, bang)
    return [(k, kq[0] + 2) for k in kq[2]] if kq else []


def khoang_don_cach_chu(chu):
    """(a, b, số) của một số cách chữ ở cuối dòng: 'Sẵn sàng cho mọi cuộc chơi 1' (Samsung), hoặc None.

    Chỉ nhận khi phần chữ trước đủ dài (>= 20 ký tự) và từ ngay trước số viết thường hoặc kết thúc
    bằng dấu câu; nhờ vậy giá trị ('Lên đến 20'), tên máy ('Samsung 68', 'Watch8 Classic 44') không bị nhận.
    """
    m = re.search(r"(?<=\s)(\d{1,2})\s*$", chu)
    if not m:
        return None
    truoc = chu[:m.start()].rstrip()
    tu_truoc = truoc.split()[-1] if truoc.split() else ""
    if len(truoc) < 20 or not tu_truoc or not (tu_truoc[0].islower() or tu_truoc[-1] in ".!?)”"):
        return None
    return m.start(1), m.end(1), int(m.group(1))


def so_chu_thich_don_cach_chu(chu):
    """[số] của một số cách chữ ở cuối dòng (xem khoang_don_cach_chu): [] nếu không có."""
    kq = khoang_don_cach_chu(chu)
    return [kq[2]] if kq else []


# --- Phần 2: tách đoạn ---

def la_gia_tri(chu):
    return len(chu) <= 30 and (any(c.isdigit() for c in chu) or chu.casefold() in GIA_TRI_CO_CHU)


def la_tieu_de_hoa(chu):
    """Dòng viết hoa chữ đầu từng từ, không số ('Pin Và Nguồn Điện5', 'Camera Trước')."""
    t = bo_ky_hieu_cuoi(chu)
    if not 4 <= len(t) <= 60 or t[-1] in ".,;:?!)" or len(t.split()) > 10 or la_gia_tri(t):
        return False
    tu = [w for w in t.split() if any(c.isalpha() for c in w)]
    if not tu or any(c.isdigit() for c in t):
        return False
    return all(w[0].isupper() for w in tu)


def la_ung_vien_chay(chu):
    """Dòng ngắn có thể là tiêu đề của đoạn văn ngay sau nó (Xiaomi, Samsung)."""
    return (4 <= len(chu) <= TIEU_DE_TOI_DA and not la_gia_tri(chu) and not chu[0].islower()
            and chu[-1] not in ":.")


def la_dai(m):
    """Dòng dài, dòng dồn nhiều mục, hoặc câu văn tương đối dài có ký hiệu chú thích ('...dễ dàng hơn. 10')."""
    return len(m.chu) >= DAI or m.dac or (len(m.chu) >= DAI * 3 // 5 and bool(m.ky_hieu))


def tim_chay_tieu_de(manh):
    """{chỉ số mảnh đầu: chỉ số mảnh dài}: 1-2 dòng ngắn rồi một dòng dài/dồn (tiêu đề + đoạn văn).

    Dòng dài sau tiêu đề thường mang ký hiệu chú thích của cả mục (Samsung '...bạn đi. 33, 34, 35').
    """
    ket_qua, trong_chay = {}, set()
    n = len(manh)
    for i in range(n):
        if i in trong_chay or manh[i].noi_truoc or la_dai(manh[i]) or not la_ung_vien_chay(manh[i].chu):
            continue
        if i > 0 and len(manh[i - 1].chu) >= DAI and manh[i - 1].chu[-1] not in ".:!?)”":
            continue  # dòng bị PDF xuống hàng giữa câu, không phải tiêu đề
        j = i + 1
        if j < n and len(manh[i].chu) >= 15 and not la_dai(manh[j]) and not manh[j].noi_truoc:
            # dòng thứ hai của cụm: tiêu đề phụ, hoặc giá trị đi kèm tiêu đề ('Siêu Sạc Nhanh' / '80W và AirVOOC 50W')
            if (len(manh[j].chu) >= 15 and la_ung_vien_chay(manh[j].chu)) or la_gia_tri(manh[j].chu):
                j += 1
        if j < n and la_dai(manh[j]) and not manh[j].chu[0].islower():
            ket_qua[i] = j
            trong_chay.update(range(i, j))
    return ket_qua


def tim_tieu_de_hoa(manh):
    """Chỉ số các tiêu đề viết hoa chữ đầu: dòng cuối của một dãy dòng viết hoa, theo sau là nội dung."""
    n = len(manh)
    co_ban = [not m.noi_truoc and not m.dac and la_tieu_de_hoa(m.chu) for m in manh]
    chay = tim_chay_tieu_de(manh)
    return {i for i in range(n - 1)
            if co_ban[i] and not co_ban[i + 1] and i + 1 not in chay and not manh[i + 1].noi_truoc
            and not la_gia_tri(manh[i + 1].chu)}


def cat_duoc(truoc, sau):
    """Có thể cắt đoạn giữa hai dòng không: không tách nhãn khỏi giá trị, không cắt giữa câu."""
    if truoc.endswith(":") or sau[0].islower() or sau[0] in "(/),.;+-%" or la_tieu_de_hoa(truoc):
        return False
    return not (la_gia_tri(sau) and len(truoc) <= 40)


def tach_cau(chu, gioi_han=CAP):
    """Khoảng [a, b) của các cụm câu liền nhau, mỗi cụm cỡ gioi_han, trong một đoạn văn quá dài
    (mô tả video, tuyên bố miễn trừ...)."""
    cat = [i + 1 for i in range(1, len(chu) - 2)
           if chu[i - 1] in ".!?" and chu[i] == " " and chu[i + 1].isupper()]
    moc, dau = [0], 0
    for i in cat:
        if i - dau >= gioi_han:
            moc.append(i)
            dau = i
    return list(zip(moc, moc[1:] + [len(chu)]))


def chia_dong(chu):
    """Khoảng [a, b) của các mảnh trong một dòng: tách dòng dồn ('Chiều cao: 163,2mmChiều rộng: 78,0mm...')
    tại chỗ nhãn mới bắt đầu; mảnh vẫn dài hơn CAP_CUNG (văn xuôi không nhãn) thì chia tiếp theo câu."""
    cat = [i for i, _ in vi_tri_ranh_gioi(chu)]
    khoang = []
    for a, b in zip([0] + cat, cat + [len(chu)]):
        con = [(a + x, a + y) for x, y in tach_cau(chu[a:b])] if b - a > CAP_CUNG else [(a, b)]
        for x, y in con:
            while x < y and chu[x].isspace():
                x += 1
            while y > x and chu[y - 1].isspace():
                y -= 1
            if y > x:
                khoang.append((x, y))
    return khoang


def tach_nhan(chu):
    """Các mảnh của một dòng (xem chia_dong)."""
    return [chu[a:b] for a, b in chia_dong(chu)]


def sao_dung_rieng(chu, a, b):
    """Dấu * ở chu[a:b] đứng giữa hai khoảng trắng (hoặc đầu/cuối dòng): không dính vào chữ nào nên không phải ký hiệu."""
    return (a == 0 or chu[a - 1].isspace()) and (b >= len(chu) or chu[b].isspace())


def chuan_bi_manh(dong, bang, loai):
    """Biến các dòng giữ lại thành mảnh, gom ký hiệu chú thích.

    Trả (mảnh, thống kê, chú thích cả dòng bắt đầu bằng '*' [(chỉ số dòng, khóa, nội dung)]).
    Ký hiệu số dính chữ phải đứng theo thứ tự xuất hiện của danh sách chú thích (số mới chỉ nhích
    thêm vài đơn vị so với số cao nhất đã thấy; số đã thấy chỉ nhắc lại khi đứng cuối dòng); nhờ vậy
    số trong tên mã ('Qi2', 'n1', 'HDR10') không bị nhận nhầm.
    """
    thong_ke = {"ky_hieu": 0, "khong_tim_duoc": [], "khong_duoc_dan": [], "gan_theo_vi_tri": []}
    thong_tin, dung_rieng = [], []
    for i, d in enumerate(dong):
        if d.chu is None or i in loai:
            continue
        chu, ky_sao, noi_lien, ca_dong = tach_dau_sao(d.chu)
        if ca_dong:
            dung_rieng.append((i, *ca_dong))
        else:
            thong_tin.append((i, d.so, chu, ky_sao, noi_lien))

    co_so = bool(bang)
    so_lon_nhat = max(bang, default=0)
    sao_co_chu_thich = {khoa for _, khoa, _ in dung_rieng}  # '*', '**' mà trang có dòng chú thích bắt đầu bằng đúng chuỗi đó
    kieu_cach = co_so and sum(
        1 for _, _, chu, _, _ in thong_tin
        if len(so_chu_thich_cach_chu(chu)) >= 2 and any(k in bang for k in so_chu_thich_cach_chu(chu))
    ) >= MIN_KIEU_CACH
    manh, cao_nhat, da_thay = [], 0, set()
    for i, so, chu, ky_sao, noi_lien in thong_tin:
        so_ky_hieu = []  # [(số, vị trí trong dòng)]
        # Mọi ký hiệu trong dòng, để bỏ khỏi noi_dung. Dấu * mà trang không có chú thích bắt đầu bằng nó ('5* product' của
        # một lời đánh giá) hoặc đứng riêng giữa hai khoảng trắng ('Chú thích * biểu tượng', nhãn đọc màn hình) không bỏ.
        bo = [KhoangBo(v, v + len(r), KY_HIEU_SAO) for r, v in ky_sao
              if r in sao_co_chu_thich and not sao_dung_rieng(chu, v, v + len(r))]
        bo += [KhoangBo(v - len(r) + 1, v + 1, KY_HIEU_SAO_NOI_LIEN) for r, _, v in noi_lien]
        nhom = nhom_so_cuoi(chu) if co_so else None
        if nhom:  # nhóm số ở cuối dòng: nhận mọi số có trong danh sách, không xét thứ tự
            so_ky_hieu += [(k, len(chu)) for k in nhom[1] if k <= so_lon_nhat]
            bo += [KhoangBo(a, b, KY_HIEU_SO, tuple(ks), tuple(k for k in ks if k not in bang))
                   for a, b, ks in khoang_nhom_cuoi(chu, nhom[0], so_lon_nhat)]
            for k, _ in so_ky_hieu:
                da_thay.add(k)
                if 0 < k - cao_nhat <= KHOANG_NHAY_SO:
                    cao_nhat = k
        elif kieu_cach:
            don = khoang_don_cach_chu(chu)
            if don and don[2] in bang:
                so_ky_hieu.append((don[2], len(chu)))
                bo.append(KhoangBo(don[0], don[1], KY_HIEU_SO, (don[2],)))
        if co_so and not kieu_cach:
            if chu.isdigit() and len(chu) <= 2 and manh and int(chu) == cao_nhat + 1:
                # số chú thích đứng riêng một dòng sau tiêu đề ('Sử dụng hóa chất thông minh hơn' / '24')
                da_thay.add(int(chu))
                cao_nhat = int(chu)
                thong_ke["ky_hieu"] += 1
                if int(chu) not in bang:
                    thong_ke["khong_tim_duoc"].append(chu)
                manh[-1] = replace(manh[-1], ky_hieu=manh[-1].ky_hieu + (int(chu),))
                continue
            for k, o_cuoi, vi_tri, het in ung_vien_so_dinh_chu(chu):
                if k > so_lon_nhat or (nhom and vi_tri >= nhom[0]):
                    continue  # lớn hơn mọi số chú thích đang có ('Reno16'), hoặc đã nằm trong nhóm số cuối dòng
                moi = 0 < k - cao_nhat <= KHOANG_NHAY_SO
                # Không đúng thứ tự vẫn nhận nếu số đứng cuối dòng và có chú thích (số của trang không
                # theo thứ tự xuất hiện), trừ khi cả dòng chỉ là tên máy ('Galaxy Watch7').
                cuoi_dong_hop_le = (o_cuoi and k in bang and not la_ten_ma_ngan(chu)
                                    and not la_ma_tieu_chuan(chu, vi_tri))
                if moi or cuoi_dong_hop_le:
                    so_ky_hieu.append((k, vi_tri))
                    bo.append(KhoangBo(vi_tri, het, KY_HIEU_SO, (k,), () if k in bang else (k,)))
                    da_thay.add(k)
                    if moi:
                        cao_nhat = max(cao_nhat, k)
            if not so_ky_hieu and cao_nhat >= 1:
                ke_tiep = khoang_ke_tiep_cuoi_dong(chu, cao_nhat + 1, bang)
                if ke_tiep:
                    for k in ke_tiep[2]:
                        so_ky_hieu.append((k, ke_tiep[0] + 2))
                        da_thay.add(k)
                        cao_nhat = max(cao_nhat, k)
                    bo.append(KhoangBo(ke_tiep[0], ke_tiep[1], KY_HIEU_SO, tuple(ke_tiep[2])))
        thong_ke["ky_hieu"] += len(so_ky_hieu) + len(ky_sao)
        thong_ke["khong_tim_duoc"] += [str(k) for k, _ in so_ky_hieu if k not in bang]
        khoang = chia_dong(chu) or [(0, len(chu))]
        dac = len(khoang) > 1 or bool(noi_lien)
        da_chia = 0
        for p, (a, b) in enumerate(khoang):
            # ký hiệu thuộc mảnh nào: mảnh đầu nhận cả chỗ trước nó, mảnh cuối nhận cả chỗ sau nó
            dau = a if p else -1
            cuoi = khoang[p + 1][0] if p + 1 < len(khoang) else len(chu) + 1
            cua_manh = tuple(replace(x, a=x.a - a, b=x.b - a) for x in bo if a <= x.a and x.b <= b)
            da_chia += len(cua_manh)
            manh.append(Manh(i, so, chu[a:b], p > 0, dac,
                             tuple(k for k, v in so_ky_hieu if dau <= v < cuoi),
                             tuple(r for r, v in ky_sao if dau <= v < cuoi),
                             tuple(t for _, t, v in noi_lien if dau <= v < cuoi), cua_manh))
        # Mọi ký hiệu đã nhận ra phải bị bỏ khỏi đúng một mảnh; lệch ở đây là lỗi chứ không lặng lẽ bỏ sót.
        if da_chia != len(bo) or sum(len(x.so) for x in bo) != len(so_ky_hieu):
            raise ValueError(f"dòng {so}: ký hiệu chú thích không khớp với khoảng cần bỏ: {chu!r}")
    return manh, thong_ke, dung_rieng


def gom_doan(manh):
    """Gom mảnh thành đoạn thô: list {muc, manh, ke_thua}; ke_thua = ký hiệu của dòng tiêu đề mục."""
    chay, hoa = tim_chay_tieu_de(manh), tim_tieu_de_hoa(manh)
    doan, hien_tai = [], None
    muc, ke_thua = "", ((), ())
    for i, m in enumerate(manh):
        do_dai = sum(len(x.chu) + 1 for x in hien_tai["manh"]) if hien_tai else 0
        la_tieu_de = i in chay or i in hoa
        mo_moi = hien_tai is None
        if hien_tai is not None:
            if la_tieu_de and do_dai >= TOI_THIEU:
                mo_moi = True
            elif do_dai + len(m.chu) > CAP and cat_duoc(manh[i - 1].chu, m.chu):
                mo_moi, la_tieu_de = True, False
            elif do_dai + len(m.chu) > CAP_CUNG:
                mo_moi, la_tieu_de = True, False
        if mo_moi:
            if hien_tai:
                doan.append(hien_tai)
            if la_tieu_de:
                muc = bo_ky_hieu_cuoi(m.chu)
                den = manh[i:chay[i] + 1] if i in chay else [m]
                ke_thua = (tuple(k for x in den for k in x.ky_hieu), tuple(s for x in den for s in x.dau_sao))
            hien_tai = {"muc": muc, "manh": [], "ke_thua": ke_thua}
        hien_tai["manh"].append(m)
    if hien_tai:
        doan.append(hien_tai)
    return doan


def gom_theo_ngat(manh):
    """Gom đoạn, ngắt cứng ở chỗ phân trang PDF (phần tử None trong danh sách)."""
    khoi, doan = [], []
    for m in manh:
        if m is None:
            doan += gom_doan(khoi)
            khoi = []
        else:
            khoi.append(m)
    return doan + gom_doan(khoi)


# --- Phần 3: gắn tên mục và chú thích ---

def ghep_noi_dung_goc(muc, manh):
    """(noi_dung_goc, [KhoangBo]) của một đoạn: các dòng nối bằng xuống dòng (mảnh cùng dòng nối bằng
    khoảng trắng); mở đầu bằng tên mục. Khoảng bỏ tính theo vị trí trong noi_dung_goc."""
    chu, bo = "", []
    for i, m in enumerate(manh):
        chu += "" if i == 0 else " " if m.noi_truoc else "\n"
        bo += [replace(x, a=x.a + len(chu), b=x.b + len(chu)) for x in m.bo]
        chu += m.chu
    if muc and not chu.startswith(muc):
        chu = muc + "\n" + chu
        bo = [replace(x, a=x.a + len(muc) + 1, b=x.b + len(muc) + 1) for x in bo]
    return chu, bo


def bo_ky_hieu_chu_thich(chu, khoang):
    """(văn bản đã bỏ ký hiệu, [nhật ký]): bỏ các khoảng KhoangBo khỏi chu, giữ hai bên cách nhau như cũ.

    Cụm ký hiệu nằm giữa hai từ ('20 phút6 với') thì chữ hai bên giữ nguyên, vẫn một khoảng trắng ('20 phút
    với'). Cụm ở cuối dòng sau một khoảng trắng ('năng lượng! 7') thì bỏ luôn khoảng trắng đó. Chỉ khi ký hiệu dính
    giữa hai chữ không có khoảng trắng ('Thấp8Mới') mới chèn một khoảng trắng để hai từ không dính nhau, và khi ký
    hiệu kẹp giữa một khoảng trắng và dấu câu thì bỏ khoảng trắng thừa.
    Nhật ký có một dict cho mỗi khoảng: vi_tri (trong chu), vi_tri_moi (chỗ đó trong văn bản mới), chu (đoạn đã
    bỏ), loai, so, thieu, xu_ly ('' nếu không phải chỉnh khoảng trắng; 'chen_cach', 'bo_cach_truoc', 'bo_cach_sau' nếu có).
    """
    khoang = sorted(khoang, key=lambda x: (x.a, x.b))
    nhom = []  # các khoảng chạm hoặc chồng nhau là một chỗ bỏ
    for x in khoang:
        if nhom and x.a <= nhom[-1][-1].b:
            nhom[-1].append(x)
        else:
            nhom.append([x])
    ra, cuoi, nhat_ky = "", 0, []
    for cum in nhom:
        a, b = cum[0].a, max(x.b for x in cum)
        ra += chu[cuoi:a]
        truoc, sau = ra[-1:], chu[b:b + 1]
        xu_ly = ""
        if sau in ("", "\n"):
            if truoc == " ":
                ra, xu_ly = ra[:-1], "bo_cach_truoc"
        elif truoc == " " and sau == " ":
            b, xu_ly = b + 1, "bo_cach_sau"
        elif truoc == " " and sau in DAU_CAU_DONG:
            ra, xu_ly = ra[:-1], "bo_cach_truoc"
        elif sau.isalnum() and (truoc.isalnum() or truoc in DAU_CAU_DONG_TRUOC):
            ra, xu_ly = ra + " ", "chen_cach"
        cuoi = b
        for j, x in enumerate(cum):
            nhat_ky.append({"vi_tri": x.a, "vi_tri_moi": len(ra), "chu": chu[x.a:x.b], "loai": x.loai, "so": list(x.so),
                            "thieu": list(x.thieu), "xu_ly": xu_ly if j == 0 else ""})
    return ra + chu[cuoi:], nhat_ky


# --- Bảng ghi tay: ký hiệu chuan_bi_manh bỏ sót, và dấu * nhận nhầm ---

# Số chú thích thật mà nhận diện của chuan_bi_manh bỏ sót (số nhắc lại giữa dòng, 'AI10' bị coi là tên chuẩn như 'AV1',
# số dính chữ ở trang dùng kiểu số cách chữ, số cách chữ sau tiêu đề viết hoa). Mỗi mục: (mã đoạn, ngữ cảnh, ký hiệu);
# ngữ cảnh là chuỗi trong noi_dung_goc của đoạn và chứa ký hiệu đúng một lần; mọi chỗ ngữ cảnh xuất hiện trong đoạn đều
# bỏ ký hiệu (chỗ chuan_bi_manh đã bỏ rồi thì thôi). Mỗi mục đã đối chiếu với thẻ <sup> của page.html (chữ đứng trước và số
# hiển thị đều khớp). Bảng chỉ bỏ chữ khỏi noi_dung: chu_thich và cách gắn chú thích không đổi. Mục không tìm thấy ngữ
# cảnh, hoặc đã được bỏ hết, là lỗi (ValueError) để bảng không lệch khỏi văn bản mà không ai biết.
KY_HIEU_BO_THEM = (
    ("dt-apple-iphone17#016", "30 phút6", "6"),  # '20 phút6' ở dòng trên đã được nhận; số 6 nhắc lại giữa dòng thì không
    ("dt-xiaomi-15t#035", "Gold Collection 5", "5"),  # số cách chữ sau tiêu đề: 'Bộ sưu tập Gold Collection <sup>5</sup>'
    ("dt-xiaomi-15t#041", "Nhận dạng giọng nói AI10", "10"),  # 'AI' bị coi là tên chuẩn như 'AV1' nên số nhắc lại không nhận
    ("dt-xiaomi-15t#041", "Phiên dịch AI10", "10"),
    ("dt-xiaomi-15t#041", "Tìm kiếm AI10", "10"),
    ("dt-xiaomi-15t#041", "Hình nền động AI10", "10"),
    ("dt-xiaomi-15t#041", "Viết AI10", "10"),
    ("dh-apple-watchse3#004", "Siri AI1", "1"),  # như trên; 'Apple Intelligence1' ở trên đã được nhận
    ("dh-samsung-galaxywatch8#015", "ngày của bạn1", "1"),
    # S25 Ultra: trang dùng kiểu số cách chữ nên chuan_bi_manh bỏ qua số dính chữ; số 33 và 34 không có trong bảng chú thích
    # của trang (bảng dừng ở 32) nhưng <sup> có và cùng kiểu với 5, 7, 8 đã nhận cùng đoạn.
    ("dt-samsung-galaxys25ultra#034", "ra lệnh là xong1", "1"),
    ("dt-samsung-galaxys25ultra#034", "tiên tiến nhất2,3", "2,3"),
    ("dt-samsung-galaxys25ultra#035", "pin vượt trội4", "4"),
    ("dt-samsung-galaxys25ultra#036", "của chúng tôi6", "6"),
    ("dt-samsung-galaxys25ultra#037", "218 g 33", "33"),
    ("dt-samsung-galaxys25ultra#037", "227 g 33", "33"),
    ("dt-samsung-galaxys25ultra#038", "của Samsung34", "34"),
    ("dt-samsung-galaxys25ultra#039", "ra lệnh là xong1", "1"),
    ("dt-samsung-galaxys25ultra#111", "tiên tiến nhất3", "3"),
    ("dt-samsung-galaxys25ultra#114", "Ultra Wide3", "3"),
    ("dt-samsung-galaxys25ultra#128", "31 giờ 4,35", "4,35"),  # <sup>4</sup>,<sup>35</sup>, không phải số thập phân
    ("dt-samsung-galaxys25ultra#129", "22 giờ 4,35", "4,35"),
)

# Ký hiệu chuan_bi_manh đã nhận nhưng không phải ký hiệu chú thích: cùng cấu trúc với KY_HIEU_BO_THEM, giữ lại trong noi_dung.
# Mục không có ký hiệu nào đã được nhận ở đúng chỗ đó là lỗi (ValueError).
KY_HIEU_GIU_LAI = (
    ("dh-samsung-galaxywatch8#129", "5* product", "*"),  # lời đánh giá 'a 5* product': điểm 5 sao, không phải chú thích
)

KY_HIEU_BO_THEM_HOP_LE = re.compile(r"\d{1,2}(?:,\d{1,2})*")


def vi_tri_ky_hieu_trong_ngu_canh(ma_doan, goc, ngu_canh, ky_hieu):
    """[(a, b)] của ky_hieu ở mọi chỗ ngu_canh xuất hiện trong goc. ValueError nếu ngữ cảnh không chứa ký hiệu đúng một
    lần hoặc không có trong goc (mục của bảng ghi tay đã lệch khỏi văn bản)."""
    if not ky_hieu or ngu_canh.count(ky_hieu) != 1:
        raise ValueError(f"{ma_doan}: ngữ cảnh {ngu_canh!r} phải chứa ký hiệu {ky_hieu!r} đúng một lần")
    lech = ngu_canh.index(ky_hieu)
    cho = [m.start() + lech for m in re.finditer(re.escape(ngu_canh), goc)]
    if not cho:
        raise ValueError(f"{ma_doan}: không thấy ngữ cảnh {ngu_canh!r} trong noi_dung_goc")
    return [(p, p + len(ky_hieu)) for p in cho]


def ap_dung_bang_ghi_tay(ma_doan, goc, noi_dung, nhat_ky, bo_them=KY_HIEU_BO_THEM, giu_lai=KY_HIEU_GIU_LAI):
    """(noi_dung, nhật ký) của đoạn ma_doan sau khi áp hai bảng ghi tay lên kết quả của chuan_bi_manh.

    Bỏ ký hiệu của bo_them (nhật ký ghi loại KY_HIEU_GHI_TAY) và giữ lại ký hiệu của giu_lai, rồi bỏ lại từ noi_dung_goc
    để khoảng trắng hai bên vẫn đúng. Đoạn không có mục nào trong hai bảng thì trả nguyên noi_dung và nhat_ky.
    ValueError nếu một mục không khớp văn bản: không tìm thấy ngữ cảnh, ký hiệu không phải số, ký hiệu đã được bỏ rồi
    (mục thừa), hoặc mục giu_lai không có ký hiệu nào đã bị bỏ ở chỗ đó.
    """
    them = [(c, k) for m, c, k in bo_them if m == ma_doan]
    giu = [(c, k) for m, c, k in giu_lai if m == ma_doan]
    if not them and not giu:
        return noi_dung, nhat_ky
    khoang = [KhoangBo(x["vi_tri"], x["vi_tri"] + len(x["chu"]), x["loai"], tuple(x["so"]), tuple(x["thieu"]))
              for x in nhat_ky]
    for ngu_canh, ky_hieu in giu:
        cho = vi_tri_ky_hieu_trong_ngu_canh(ma_doan, goc, ngu_canh, ky_hieu)
        bo_di = [x for x in khoang if (x.a, x.b) in cho]
        if not bo_di:
            raise ValueError(f"{ma_doan}: không có ký hiệu nào đã bị bỏ tại {ngu_canh!r} để giữ lại")
        khoang = [x for x in khoang if x not in bo_di]
    for ngu_canh, ky_hieu in them:
        if not KY_HIEU_BO_THEM_HOP_LE.fullmatch(ky_hieu):
            raise ValueError(f"{ma_doan}: ký hiệu {ky_hieu!r} phải là số chú thích (số, dấu phẩy)")
        moi = [(a, b) for a, b in vi_tri_ky_hieu_trong_ngu_canh(ma_doan, goc, ngu_canh, ky_hieu)
               if not any(x.a < b and a < x.b for x in khoang)]
        if not moi:
            raise ValueError(f"{ma_doan}: ký hiệu {ky_hieu!r} ở {ngu_canh!r} đã được bỏ rồi, xóa mục này khỏi bảng")
        so = tuple(int(k) for k in SO_NGUYEN.findall(ky_hieu))
        khoang += [KhoangBo(a, b, KY_HIEU_GHI_TAY, so) for a, b in moi]
    return bo_ky_hieu_chu_thich(goc, khoang)


def dung_doan(doan_tho, chu_thich_so, dung_rieng, dong, thong_ke):
    """Đoạn thô -> đoạn hoàn chỉnh: gắn chú thích (theo số, theo dấu *, nối liền trong dòng)."""
    sao_theo_khoa = {}
    for _, khoa, noi in dung_rieng:
        sao_theo_khoa.setdefault(khoa, []).append(noi)
    ket_qua, so_da_dung, sao_da_dung = [], set(), set()
    for d in doan_tho:
        manh = d["manh"]
        chu_thich = []
        for k in dict.fromkeys([k for m in manh for k in m.ky_hieu] + list(d["ke_thua"][0])):
            if k in chu_thich_so:
                chu_thich.append(chu_thich_so[k]["chu"])
                so_da_dung.add(k)
        for m in manh:
            chu_thich += m.chu_thich_dong
        for khoa in dict.fromkeys([s for m in manh for s in m.dau_sao] + list(d["ke_thua"][1])):
            if len(sao_theo_khoa.get(khoa, [])) == 1:  # khóa trùng nhiều chú thích thì gắn theo vị trí
                chu_thich.append(sao_theo_khoa[khoa][0])
                sao_da_dung.add(khoa)
            elif khoa not in sao_theo_khoa:
                thong_ke["khong_tim_duoc"].append(khoa)
        goc, bo = ghep_noi_dung_goc(d["muc"], manh)
        noi_dung, nhat_ky = bo_ky_hieu_chu_thich(goc, bo)
        ket_qua.append({"muc": d["muc"], "noi_dung": noi_dung, "noi_dung_goc": goc,
                        "chu_thich": list(dict.fromkeys(chu_thich)),
                        "dong": [min(m.so for m in manh), max(m.so for m in manh)],
                        "ky_hieu_bo": nhat_ky, "_dau": manh[0].chi_so})
    # Chú thích cả dòng bắt đầu bằng *: gắn vào đoạn đứng ngay trước nếu không dẫn theo ký hiệu.
    for chi_so, khoa, noi in dung_rieng:
        if khoa in sao_da_dung:
            continue
        truoc = [d for d in ket_qua if d["_dau"] < chi_so]
        if truoc:
            truoc[-1]["chu_thich"].append(noi)
        else:
            ket_qua.append({"muc": "Chú thích", "noi_dung": "Chú thích\n" + noi, "noi_dung_goc": "Chú thích\n" + noi,
                            "chu_thich": [], "dong": [dong[chi_so].so] * 2, "ky_hieu_bo": [], "_dau": chi_so})
    # Chú thích có số mà chưa đoạn nào dẫn tới: đứng lẻ giữa trang (không nằm trong khối chú thích) thì chú
    # thích cho phần ngay phía trên nó; còn lại giữ thành đoạn riêng để vẫn tìm được.
    dong_chu_thich = {i for v in chu_thich_so.values() for i in v["dong"]}
    for so, thong_tin in sorted(chu_thich_so.items()):
        if so not in so_da_dung:
            chi_so = thong_tin["dong"]
            truoc = [d for d in ket_qua if d["_dau"] < chi_so[0]]
            if truoc and chi_so[0] - 1 not in dong_chu_thich and chi_so[-1] + 1 not in dong_chu_thich:
                truoc[-1]["chu_thich"].append(thong_tin["chu"])
                thong_ke["gan_theo_vi_tri"].append(so)
                continue
            thong_ke["khong_duoc_dan"].append(so)
            chu = f"Chú thích {so}\n{thong_tin['chu']}"
            ket_qua.append({"muc": "Chú thích", "noi_dung": chu, "noi_dung_goc": chu, "chu_thich": [],
                            "dong": [dong[chi_so[0]].so, dong[chi_so[-1]].so], "ky_hieu_bo": [], "_dau": chi_so[0]})
    ket_qua.sort(key=lambda d: d["_dau"])
    for d in ket_qua:
        del d["_dau"]
    return ket_qua


def chia_doan_day_du(van_ban, bang_chu_thich=None):
    """Trả (list đoạn, thống kê). Đoạn: {muc, noi_dung, noi_dung_goc, chu_thich, dong, ky_hieu_bo}.

    noi_dung_goc là văn bản trước khi bỏ ký hiệu chú thích; noi_dung đã bỏ chúng (xem bo_ky_hieu_chu_thich);
    ky_hieu_bo là nhật ký các chỗ đã bỏ (danh_ma_doan không ghi nó vào doan.jsonl).

    bang_chu_thich: {số: nội dung} lấy từ doc_chu_thich_html(); không có thì chỉ nhận chú thích có số
    ghi sẵn trong văn bản ('5. ...') và chú thích dấu *. Tài liệu PDF (có dòng '=== Trang N ===')
    chỉ được chia đoạn, không gắn chú thích.
    thống kê: {"ky_hieu": số ký hiệu nhận ra, "khong_tim_duoc": [ký hiệu không có nội dung chú thích],
    "khong_duoc_dan": [số chú thích không được đoạn nào dẫn tới, nay là đoạn "Chú thích N"],
    "khong_co_trong_txt": [số chú thích có trong page.html nhưng không có dòng nào trong page.txt]}.
    """
    dong = doc_dong(van_ban)
    if any(d.chu is None for d in dong):
        thong_ke = {"ky_hieu": 0, "khong_tim_duoc": [], "khong_duoc_dan": [], "gan_theo_vi_tri": []}
        manh = [None if d.chu is None else Manh(i, d.so, d.chu) for i, d in enumerate(dong)]
        return dung_doan(gom_theo_ngat(manh), {}, [], dong, thong_ke), thong_ke

    chu_thich_so, loai = {}, set()
    khop = khop_chu_thich_html(dong, bang_chu_thich or {})
    for so, chi_so in khop.items():
        chu_thich_so[so] = {"chu": bang_chu_thich[so], "dong": chi_so}
        loai.update(chi_so)
    for i, d in enumerate(dong):
        m = SO_DAU_DONG.match(d.chu) if i not in loai else None
        if m and int(m.group(1)) not in chu_thich_so:
            chu_thich_so[int(m.group(1))] = {"chu": m.group(2), "dong": [i]}
            loai.add(i)
    for i in sorted(loai):  # nhãn 'Lưu ý:' đứng ngay trước khối chú thích cũng bỏ
        truoc = dong[i - 1].chu if i > 0 else None
        if truoc and i - 1 not in loai and truoc.endswith(":") and len(truoc) <= 20:
            loai.add(i - 1)

    manh, thong_ke, dung_rieng = chuan_bi_manh(dong, {k: v["chu"] for k, v in chu_thich_so.items()}, loai)
    thong_ke["khong_co_trong_txt"] = sorted(set(bang_chu_thich or {}) - set(khop))
    return dung_doan(gom_doan(manh), chu_thich_so, dung_rieng, dong, thong_ke), thong_ke


def chia_doan(van_ban, bang_chu_thich=None):
    """List đoạn của một page.txt; xem chia_doan_day_du() để lấy thêm thống kê."""
    return chia_doan_day_du(van_ban, bang_chu_thich)[0]


def danh_ma_doan(ma_mau, doan_theo_trang, so_chu_so=3, bo_them=KY_HIEU_BO_THEM, giu_lai=KY_HIEU_GIU_LAI):
    """Gán id '<ma_mau>#<số>' liên tục qua các trang của một mẫu (url trước, bo_sung sau).

    doan_theo_trang: [(trang, list đoạn)]. Trả list dict đủ trường theo thứ tự id, kèm ky_hieu_bo (nhật ký bỏ ký hiệu,
    không ghi vào doan.jsonl). Áp hai bảng ghi tay bo_them và giu_lai lên noi_dung (xem ap_dung_bang_ghi_tay) vì mã đoạn
    chỉ có ở đây; mục của bảng cho một mã đoạn của mẫu này mà mẫu không có đoạn đó là lỗi (ValueError).
    """
    ket_qua, so = [], 0
    for trang, doan in doan_theo_trang:
        for d in doan:
            so += 1
            ma_doan = f"{ma_mau}#{so:0{so_chu_so}d}"
            noi_dung, nhat_ky = ap_dung_bang_ghi_tay(ma_doan, d["noi_dung_goc"], d["noi_dung"], d["ky_hieu_bo"],
                                                     bo_them, giu_lai)
            ket_qua.append({"id": ma_doan, "ma_mau": ma_mau, "trang": trang,
                            "muc": d["muc"], "noi_dung": noi_dung, "noi_dung_goc": d["noi_dung_goc"],
                            "chu_thich": d["chu_thich"], "dong": d["dong"], "ky_hieu_bo": nhat_ky})
    co_ma = {d["id"] for d in ket_qua}
    for ma_doan, ngu_canh, _ in (*bo_them, *giu_lai):
        if ma_doan.startswith(ma_mau + "#") and ma_doan not in co_ma:
            raise ValueError(f"{ma_doan}: bảng ghi tay có mục ({ngu_canh!r}) cho một mã đoạn không tồn tại")
    return ket_qua
