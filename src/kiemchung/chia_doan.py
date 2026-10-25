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

Ba phần: (1) đọc chú thích (số, dấu *, chú thích nối liền trong dòng), (2) tách đoạn theo mục,
(3) gắn tên mục và chú thích vào từng đoạn.
"""
from dataclasses import dataclass, replace
import html
import re

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


# --- Đọc dòng ---

def lam_sach(dong):
    dong = dong.replace("\u200b", "").replace("\ufeff", "")
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


def ung_vien_so_dinh_chu(chu):
    """[(số, ở cuối dòng, vị trí)] của các số đứng cuối từ và dính liền chữ cái ('Điện5', 'MIMO8')."""
    ket_qua = []
    for m in SO_DINH_CHU.finditer(chu):
        s = m.start(1)
        if chu[s - 1].isalpha() and (s < 2 or not chu[s - 2].isalpha()):
            if not (chu[s - 1].isupper() and s >= 2 and chu[s - 2].isdigit()):
                continue
        o_cuoi_dong = not chu[m.end(1):].strip(" .,;:)")
        ket_qua.append((int(m.group(1)), o_cuoi_dong, s))
    return ket_qua


def so_chu_thich_dinh_chu(chu):
    """[(số, ở cuối dòng)] của các số đứng cuối từ và dính liền chữ cái ('Điện5', 'MIMO8', 'Va Chạm7').

    Không lấy số liệu: '120Hz', '48MP', 'iPhone 17', 'v5.4' không là chữ số cuối từ dính chữ (hoặc là số
    thập phân/4 chữ số). Loại mã kiểu 'A19', 'N1', 'n8' (một chữ cái rồi số) trừ khi chữ hoa đứng ngay
    sau số ('25W6', đơn vị rồi ký hiệu). Mã như 'IP68' hay 'Qi2' còn lọt qua hàm này; chuan_bi_manh() loại
    chúng bằng thứ tự xuất hiện của số chú thích.
    """
    return [(k, o_cuoi) for k, o_cuoi, _ in ung_vien_so_dinh_chu(chu)]


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


def so_ke_tiep_cuoi_dong(chu, ky_vong, bang):
    """[(số, vị trí)] của ký hiệu dính vào một chữ số khác ở cuối dòng và chính là số chú thích kế tiếp.

    'thế hệ thứ 210' (số 2 rồi ký hiệu 10), 'Wi-Fi 617, 18' (số 6 rồi ký hiệu 17, 18). Chỉ nhận số có 3
    chữ số mà hai chữ số cuối đúng bằng số chú thích kế tiếp (từ 10) có trong bang, nên số liệu
    thường hiếm khi bị nhận nhầm.
    """
    m = re.search(r"(?<=\s)(\d{3})((?:,\s*\d{1,2})*)$", chu)
    if m and ky_vong >= 10 and int(m.group(1)[-2:]) == ky_vong and ky_vong in bang:
        dem = [ky_vong] + [int(x) for x in re.findall(r"\d+", m.group(2))]
        if dem == list(range(ky_vong, ky_vong + len(dem))) and all(k in bang for k in dem):
            return [(k, m.end(1)) for k in dem]
    return []


def so_chu_thich_don_cach_chu(chu):
    """Một số cách chữ ở cuối dòng: 'Sẵn sàng cho mọi cuộc chơi 1' (Samsung).

    Chỉ nhận khi phần chữ trước đủ dài (>= 20 ký tự) và từ ngay trước số viết thường hoặc kết thúc
    bằng dấu câu; nhờ vậy giá trị ('Lên đến 20'), tên máy ('Samsung 68', 'Watch8 Classic 44') không bị nhận.
    """
    m = re.search(r"(?<=\s)(\d{1,2})\s*$", chu)
    if not m:
        return []
    truoc = chu[:m.start()].rstrip()
    tu_truoc = truoc.split()[-1] if truoc.split() else ""
    if len(truoc) < 20 or not tu_truoc or not (tu_truoc[0].islower() or tu_truoc[-1] in ".!?)”"):
        return []
    return [int(m.group(1))]


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
    kieu_cach = co_so and sum(
        1 for _, _, chu, _, _ in thong_tin
        if len(so_chu_thich_cach_chu(chu)) >= 2 and any(k in bang for k in so_chu_thich_cach_chu(chu))
    ) >= MIN_KIEU_CACH
    manh, cao_nhat, da_thay = [], 0, set()
    for i, so, chu, ky_sao, noi_lien in thong_tin:
        so_ky_hieu = []  # [(số, vị trí trong dòng)]
        nhom = nhom_so_cuoi(chu) if co_so else None
        if nhom:  # nhóm số ở cuối dòng: nhận mọi số có trong danh sách, không xét thứ tự
            so_ky_hieu += [(k, len(chu)) for k in nhom[1] if k <= so_lon_nhat]
            for k, _ in so_ky_hieu:
                da_thay.add(k)
                if 0 < k - cao_nhat <= KHOANG_NHAY_SO:
                    cao_nhat = k
        elif kieu_cach:
            so_ky_hieu += [(k, len(chu)) for k in so_chu_thich_don_cach_chu(chu) if k in bang]
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
            for k, o_cuoi, vi_tri in ung_vien_so_dinh_chu(chu):
                if k > so_lon_nhat or (nhom and vi_tri >= nhom[0]):
                    continue  # lớn hơn mọi số chú thích đang có ('Reno16'), hoặc đã nằm trong nhóm số cuối dòng
                moi = 0 < k - cao_nhat <= KHOANG_NHAY_SO
                # Không đúng thứ tự vẫn nhận nếu số đứng cuối dòng và có chú thích (số của trang không
                # theo thứ tự xuất hiện), trừ khi cả dòng chỉ là tên máy ('Galaxy Watch7').
                cuoi_dong_hop_le = (o_cuoi and k in bang and not la_ten_ma_ngan(chu)
                                    and not la_ma_tieu_chuan(chu, vi_tri))
                if moi or cuoi_dong_hop_le:
                    so_ky_hieu.append((k, vi_tri))
                    da_thay.add(k)
                    if moi:
                        cao_nhat = max(cao_nhat, k)
            if not so_ky_hieu and cao_nhat >= 1:
                for k, vi_tri in so_ke_tiep_cuoi_dong(chu, cao_nhat + 1, bang):
                    so_ky_hieu.append((k, vi_tri))
                    da_thay.add(k)
                    cao_nhat = max(cao_nhat, k)
        thong_ke["ky_hieu"] += len(so_ky_hieu) + len(ky_sao)
        thong_ke["khong_tim_duoc"] += [str(k) for k, _ in so_ky_hieu if k not in bang]
        khoang = chia_dong(chu) or [(0, len(chu))]
        dac = len(khoang) > 1 or bool(noi_lien)
        for p, (a, b) in enumerate(khoang):
            # ký hiệu thuộc mảnh nào: mảnh đầu nhận cả chỗ trước nó, mảnh cuối nhận cả chỗ sau nó
            dau = a if p else -1
            cuoi = khoang[p + 1][0] if p + 1 < len(khoang) else len(chu) + 1
            manh.append(Manh(i, so, chu[a:b], p > 0, dac,
                             tuple(k for k, v in so_ky_hieu if dau <= v < cuoi),
                             tuple(r for r, v in ky_sao if dau <= v < cuoi),
                             tuple(t for _, t, v in noi_lien if dau <= v < cuoi)))
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

def noi_dung_doan(muc, manh):
    """Các dòng nối bằng xuống dòng (mảnh cùng dòng nối bằng khoảng trắng); mở đầu bằng tên mục."""
    phan = []
    for m in manh:
        if phan and m.noi_truoc:
            phan[-1] += " " + m.chu
        else:
            phan.append(m.chu)
    chu = "\n".join(phan)
    return muc + "\n" + chu if muc and not chu.startswith(muc) else chu


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
        ket_qua.append({"muc": d["muc"], "noi_dung": noi_dung_doan(d["muc"], manh),
                        "chu_thich": list(dict.fromkeys(chu_thich)),
                        "dong": [min(m.so for m in manh), max(m.so for m in manh)],
                        "_dau": manh[0].chi_so})
    # Chú thích cả dòng bắt đầu bằng *: gắn vào đoạn đứng ngay trước nếu không dẫn theo ký hiệu.
    for chi_so, khoa, noi in dung_rieng:
        if khoa in sao_da_dung:
            continue
        truoc = [d for d in ket_qua if d["_dau"] < chi_so]
        if truoc:
            truoc[-1]["chu_thich"].append(noi)
        else:
            ket_qua.append({"muc": "Chú thích", "noi_dung": "Chú thích\n" + noi, "chu_thich": [],
                            "dong": [dong[chi_so].so] * 2, "_dau": chi_so})
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
            ket_qua.append({"muc": "Chú thích", "noi_dung": f"Chú thích {so}\n{thong_tin['chu']}", "chu_thich": [],
                            "dong": [dong[chi_so[0]].so, dong[chi_so[-1]].so], "_dau": chi_so[0]})
    ket_qua.sort(key=lambda d: d["_dau"])
    for d in ket_qua:
        del d["_dau"]
    return ket_qua


def chia_doan_day_du(van_ban, bang_chu_thich=None):
    """Trả (list đoạn, thống kê). Đoạn: {muc, noi_dung, chu_thich, dong}.

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


def danh_ma_doan(ma_mau, doan_theo_trang, so_chu_so=3):
    """Gán id '<ma_mau>#<số>' liên tục qua các trang của một mẫu (url trước, bo_sung sau).

    doan_theo_trang: [(trang, list đoạn)]. Trả list dict đủ trường theo thứ tự id.
    """
    ket_qua, so = [], 0
    for trang, doan in doan_theo_trang:
        for d in doan:
            so += 1
            ket_qua.append({"id": f"{ma_mau}#{so:0{so_chu_so}d}", "ma_mau": ma_mau, "trang": trang,
                            "muc": d["muc"], "noi_dung": d["noi_dung"], "chu_thich": d["chu_thich"],
                            "dong": d["dong"]})
    return ket_qua
