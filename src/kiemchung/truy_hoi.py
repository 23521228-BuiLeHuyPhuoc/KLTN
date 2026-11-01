"""Truy hồi BM25 trong tài liệu của một mẫu sản phẩm (Bước 14, T5.2).

Chỉ tìm trong data/nguon/<ma_mau>/doan.jsonl của đúng mẫu được chọn; truy vấn là văn bản tuyên bố. Văn bản
của mỗi đoạn là noi_dung cộng các chu_thich (hướng dẫn gán nhãn mục 8 cho phép chép bằng chứng từ chú thích).
Chỉ mục là BM25Okapi của rank-bm25 với tham số mặc định.

Hai cách tách (chọn ở Bước 33): "am_tiet" (mỗi âm tiết một mảnh) và "tu" (pyvi ghép từ, giữ từ ghép dạng
'thời_lượng'). Cả hai đều NFC, chữ thường, bỏ dấu câu, giữ số có dấu ngăn bên trong thành một mảnh ('5,4',
'28.999.000') và tách chỗ chữ số dính chữ cái ('515mAh' -> '515', 'mah'; 'IP68' -> 'ip', '68'). Lý do tách chữ
số khỏi chữ cái: quảng cáo viết liền '515mAh', còn tài liệu Samsung viết '515' và 'mAh' ở hai dòng; không tách
thì hai bên không có mảnh chung nào để khớp.

Kiểm chặt: mọi đoạn đọc vào phải thuộc đúng ma_mau (trường ma_mau và tiền tố mã đoạn), và mọi kết quả trả ra
phải là đoạn của chỉ mục; sai thì raise ValueError, không trả im lặng đoạn của mẫu khác.

Phần cuối là các hàm thuần tính Recall@k theo T6.4 (nhận danh sách đã xếp hạng và bằng chứng chuẩn); script đo
nằm ở scripts/do_recall.py.
"""
import json
from pathlib import Path
import re
import unicodedata

from pyvi import ViTokenizer
from rank_bm25 import BM25Okapi

from .cau_hinh import GOC

THU_MUC_NGUON = GOC / "data" / "nguon"
CACH_TACH = ("am_tiet", "tu")
KS = (1, 3, 5, 8)

# Mảnh chữ là dãy chữ cái liền nhau (dấu rời của chữ NFC không ghép được cũng tính là chữ);
# mảnh số là dãy chữ số, bên trong có thể có dấu ngăn ('5,4', '28.999.000').
CHU = r"(?:[^\W\d_]|[̀-ͯ])+"
SO = r"\d+(?:[.,]\d+)*"
MANH_AM_TIET = re.compile(rf"{SO}|{CHU}")
MANH_TU = re.compile(rf"{SO}|{CHU}(?:_{CHU})*")  # '_' nối các âm tiết của từ ghép do pyvi sinh ra

_DEM = {}  # (thư mục nguồn, ma_mau, cách tách) -> ChiMuc


def tach_tu(van_ban, cach="am_tiet"):
    """Danh sách mảnh của một văn bản theo cách tách "am_tiet" hoặc "tu" (xem đầu tệp).

    Cách "tu" chạy pyvi từng dòng một để từ ghép không vắt qua hai dòng của trang."""
    if cach not in CACH_TACH:
        raise ValueError(f"cách tách không hợp lệ: {cach!r} (chọn {', '.join(CACH_TACH)})")
    van_ban = unicodedata.normalize("NFC", van_ban)
    if cach == "tu":
        van_ban = "\n".join(ViTokenizer.tokenize(dong) for dong in van_ban.split("\n"))
    manh = MANH_TU if cach == "tu" else MANH_AM_TIET
    return manh.findall(van_ban.lower())


def doc_doan(ma_mau, thu_muc_nguon=THU_MUC_NGUON):
    """[(mã đoạn, văn bản đánh chỉ mục)] theo thứ tự trong doan.jsonl của đúng mẫu ma_mau.

    Văn bản đánh chỉ mục là noi_dung và các chu_thich nối bằng dấu xuống dòng."""
    if not ma_mau or Path(ma_mau).name != ma_mau or ma_mau == "..":
        raise ValueError(f"mã mẫu không hợp lệ: {ma_mau!r}")
    duong = Path(thu_muc_nguon) / ma_mau / "doan.jsonl"
    doan, da_co = [], set()
    with open(duong, encoding="utf-8") as f:
        for dong in f:
            if not dong.strip():
                continue
            d = json.loads(dong)
            if d["ma_mau"] != ma_mau or not d["id"].startswith(f"{ma_mau}#"):
                raise ValueError(f"{duong}: đoạn {d['id']!r} (ma_mau {d['ma_mau']!r}) không thuộc mẫu {ma_mau}")
            if d["id"] in da_co:
                raise ValueError(f"{duong}: mã đoạn {d['id']} lặp")
            da_co.add(d["id"])
            doan.append((d["id"], "\n".join([d["noi_dung"], *(d.get("chu_thich") or [])])))
    if not doan:
        raise ValueError(f"{duong}: không có đoạn nào")
    return doan


class ChiMuc:
    """Chỉ mục BM25 của một mẫu với một cách tách."""

    def __init__(self, ma_mau, cach_tach="am_tiet", thu_muc_nguon=THU_MUC_NGUON):
        doan = doc_doan(ma_mau, thu_muc_nguon)
        corpus = [tach_tu(van_ban, cach_tach) for _, van_ban in doan]
        if not any(corpus):
            raise ValueError(f"mẫu {ma_mau}: không đoạn nào có chữ để đánh chỉ mục")
        self.ma_mau = ma_mau
        self.cach_tach = cach_tach
        self.ma_doan = [ma for ma, _ in doan]
        self._tap_ma = set(self.ma_doan)
        self.bm25 = BM25Okapi(corpus)

    def xep_hang(self, tuyen_bo, k=None):
        """Top-k [(mã đoạn, điểm)] cho văn bản tuyên bố, điểm giảm dần, hòa điểm thì theo thứ tự đoạn trong tệp.

        k=None hoặc lớn hơn số đoạn thì trả hết các đoạn của mẫu."""
        if k is not None and k < 1:
            raise ValueError(f"k phải từ 1 trở lên (đang là {k})")
        diem = self.bm25.get_scores(tach_tu(tuyen_bo, self.cach_tach))
        thu_tu = sorted(range(len(self.ma_doan)), key=lambda i: -diem[i])  # sort ổn định giữ thứ tự tệp khi hòa
        ket_qua = [(self.ma_doan[i], float(diem[i])) for i in thu_tu[:k]]
        tien_to = f"{self.ma_mau}#"
        lac = [ma for ma, _ in ket_qua if not ma.startswith(tien_to) or ma not in self._tap_ma]
        if lac:
            raise ValueError(f"truy hồi mẫu {self.ma_mau} trả về đoạn của mẫu khác: {lac}")
        return ket_qua


def lay_chi_muc(ma_mau, cach_tach="am_tiet", thu_muc_nguon=THU_MUC_NGUON):
    """ChiMuc của (thư mục nguồn, ma_mau, cách tách); dựng một lần rồi nhớ đệm."""
    khoa = (str(Path(thu_muc_nguon).resolve()), ma_mau, cach_tach)
    if khoa not in _DEM:
        _DEM[khoa] = ChiMuc(ma_mau, cach_tach, thu_muc_nguon)
    return _DEM[khoa]


def xoa_dem():
    """Bỏ mọi chỉ mục đã nhớ (khi doan.jsonl đổi giữa chừng, hoặc trong test)."""
    _DEM.clear()


def truy_hoi(ma_mau, tuyen_bo, k, cach_tach="am_tiet", thu_muc_nguon=THU_MUC_NGUON):
    """Top-k [(mã đoạn, điểm)] của văn bản tuyên bố trong tài liệu của đúng mẫu ma_mau."""
    return lay_chi_muc(ma_mau, cach_tach, thu_muc_nguon).xep_hang(tuyen_bo, k)


# --- Recall@k (T6.4) ---

def hang_bang_chung(ma_xep, bang_chung):
    """Hạng (từ 1) của đoạn bằng chứng đứng cao nhất trong danh sách mã đã xếp; None nếu không đoạn nào có mặt."""
    chuan = set(bang_chung)
    for hang, ma in enumerate(ma_xep, start=1):
        if ma in chuan:
            return hang
    return None


def mau_so_recall(bang_chung, loai=()):
    """Mã các tuyên bố tính vào mẫu số của Recall@k: có bằng chứng (danh sách khác rỗng), trừ các mã trong loai.

    bang_chung: {mã tuyên bố: [mã đoạn]}."""
    bo = set(loai)
    return [ma for ma, bc in bang_chung.items() if bc and ma not in bo]


def tinh_recall(xep_hang, bang_chung, loai=(), ks=KS):
    """{k: (số trúng, mẫu số)} theo T6.4: tuyên bố trúng ở k nếu có ít nhất một đoạn bằng chứng nằm trong top-k.

    xep_hang: {mã tuyên bố: [mã đoạn đã xếp điểm giảm dần]}; bang_chung: {mã tuyên bố: [mã đoạn]}. Tuyên bố không
    có bằng chứng và các mã trong loai không vào mẫu số."""
    hang = [hang_bang_chung(xep_hang[ma], bang_chung[ma]) for ma in mau_so_recall(bang_chung, loai)]
    return {k: (sum(1 for h in hang if h is not None and h <= k), len(hang)) for k in ks}
