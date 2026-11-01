import importlib.util
import json
from pathlib import Path
import unicodedata

import pytest

from kiemchung import truy_hoi as th

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("do_recall", ROOT / "scripts/do_recall.py")
do_recall = importlib.util.module_from_spec(spec)
spec.loader.exec_module(do_recall)

# Sáu đoạn: 'ip68' chỉ ở hai đoạn giống hệt nhau (#002, #003) nên có điểm dương, hòa điểm.
DOAN_A = [
    ("Dung lượng pin lớn", []),
    ("Chống nước IP68 ngoài trời", []),
    ("Chống nước IP68 ngoài trời", []),
    ("Kết nối bluetooth ổn định", []),
    ("Màn hình sáng rõ ban ngày", []),
    ("Camera chụp đêm tốt", []),
]


@pytest.fixture(autouse=True)
def sach_dem():
    th.xoa_dem()
    yield
    th.xoa_dem()


def ghi_doan(thu_muc_nguon, ma_mau, doan, thu_tu=None):
    """Ghi nguon/<ma_mau>/doan.jsonl từ [(noi_dung, [chu_thich])]; mã đoạn <ma_mau>#001... theo vị trí.

    thu_tu: thứ tự ghi các chỉ số (từ 0) trong tệp, mặc định giữ nguyên."""
    thu_muc = Path(thu_muc_nguon) / ma_mau
    thu_muc.mkdir(parents=True, exist_ok=True)
    dong = [{"id": f"{ma_mau}#{i:03d}", "ma_mau": ma_mau, "noi_dung": nd, "chu_thich": ct}
            for i, (nd, ct) in enumerate(doan, 1)]
    dong = [dong[i] for i in (thu_tu if thu_tu is not None else range(len(dong)))]
    (thu_muc / "doan.jsonl").write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in dong),
                                        encoding="utf-8")


@pytest.fixture
def nguon(tmp_path):
    """Hai mẫu: dt-a và dt-b; dt-b có đoạn trùng y hệt câu truy vấn 'Chống nước IP68 ngoài trời'."""
    thu_muc = tmp_path / "nguon"
    ghi_doan(thu_muc, "dt-a", DOAN_A)
    ghi_doan(thu_muc, "dt-b", [("Chống nước IP68 ngoài trời", []), ("Chống nước IP68 ngoài trời", ["IP68"]),
                               ("Pin rất lớn", []), ("Loa to", []), ("Sạc nhanh", [])])
    return thu_muc


# --- Không bao giờ trả về đoạn của mẫu khác ---

@pytest.mark.parametrize("cach", th.CACH_TACH)
@pytest.mark.parametrize("k", [1, 3, 100, None])
def test_chi_tra_ve_doan_cua_dung_mau(nguon, cach, k):
    cau = "Chống nước IP68 ngoài trời"
    kq_a = th.truy_hoi("dt-a", cau, k, cach, nguon)
    kq_b = th.truy_hoi("dt-b", cau, k, cach, nguon)
    assert kq_a and all(ma.startswith("dt-a#") for ma, _ in kq_a)
    assert kq_b and all(ma.startswith("dt-b#") for ma, _ in kq_b)
    dau = [ma for ma, _ in kq_a[:2]]
    assert dau == ["dt-a#002", "dt-a#003"][:len(dau)]


def test_chi_muc_khong_lan_mau_ke_ca_khi_tat_ca_diem_bang_khong(nguon):
    kq = th.truy_hoi("dt-a", "zzz qqq", None, "am_tiet", nguon)
    assert {ma for ma, _ in kq} == {f"dt-a#{i:03d}" for i in range(1, 7)}


def test_doan_cua_mau_khac_trong_tep_bi_tu_choi(nguon):
    # Tệp của dt-a lẫn một đoạn của dt-b.
    duong = nguon / "dt-a" / "doan.jsonl"
    dong_b = json.dumps({"id": "dt-b#001", "ma_mau": "dt-b", "noi_dung": "x", "chu_thich": []})
    duong.write_text(duong.read_text(encoding="utf-8") + dong_b + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="không thuộc mẫu dt-a"):
        th.truy_hoi("dt-a", "pin", 3, "am_tiet", nguon)


def test_ma_doan_lech_tien_to_bi_tu_choi(nguon):
    # ma_mau đúng nhưng mã đoạn mang tiền tố mẫu khác.
    duong = nguon / "dt-a" / "doan.jsonl"
    dong = json.dumps({"id": "dt-b#009", "ma_mau": "dt-a", "noi_dung": "x", "chu_thich": []})
    duong.write_text(duong.read_text(encoding="utf-8") + dong + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="không thuộc mẫu dt-a"):
        th.truy_hoi("dt-a", "pin", 3, "am_tiet", nguon)


def test_ket_qua_lac_mau_bi_chan(nguon):
    chi_muc = th.lay_chi_muc("dt-a", "am_tiet", nguon)
    chi_muc.ma_doan[0] = "dt-b#001"  # giả lập chỉ mục bị lẫn mã của mẫu khác
    with pytest.raises(ValueError, match="mẫu khác"):
        chi_muc.xep_hang("pin", None)


@pytest.mark.parametrize("ma_mau", ["../dt-b", "dt-a/..", "..", "", "dt-a/../dt-b"])
def test_ma_mau_co_duong_dan_bi_tu_choi(nguon, ma_mau):
    with pytest.raises(ValueError, match="mã mẫu không hợp lệ"):
        th.truy_hoi(ma_mau, "pin", 3, "am_tiet", nguon)


def test_mau_khong_co_tep_hoac_khong_co_doan(nguon):
    with pytest.raises(FileNotFoundError):
        th.truy_hoi("dt-khong-co", "pin", 3, "am_tiet", nguon)
    ghi_doan(nguon, "dt-rong", [])
    with pytest.raises(ValueError, match="không có đoạn nào"):
        th.truy_hoi("dt-rong", "pin", 3, "am_tiet", nguon)


# --- k, thứ tự, hòa điểm ---

def test_k_lon_hon_so_doan_tra_het(nguon):
    kq = th.truy_hoi("dt-a", "Chống nước IP68", 50, "am_tiet", nguon)
    assert len(kq) == len(DOAN_A)
    assert len({ma for ma, _ in kq}) == len(DOAN_A)
    assert th.truy_hoi("dt-a", "Chống nước IP68", None, "am_tiet", nguon) == kq


def test_k_nho_cat_dung_dau_danh_sach(nguon):
    day_du = th.truy_hoi("dt-a", "Chống nước IP68", None, "am_tiet", nguon)
    assert th.truy_hoi("dt-a", "Chống nước IP68", 2, "am_tiet", nguon) == day_du[:2]


@pytest.mark.parametrize("k", [0, -1])
def test_k_khong_hop_le(nguon, k):
    with pytest.raises(ValueError, match="k phải từ 1"):
        th.truy_hoi("dt-a", "pin", k, "am_tiet", nguon)


def test_diem_giam_dan(nguon):
    diem = [d for _, d in th.truy_hoi("dt-a", "Chống nước IP68 pin", None, "am_tiet", nguon)]
    assert diem == sorted(diem, reverse=True)
    assert diem[0] > diem[-1]


def test_hoa_diem_giu_thu_tu_trong_tep(tmp_path):
    # #002 và #003 giống hệt nhau nên hòa điểm; đổi chỗ chúng trong tệp thì thứ tự kết quả đổi theo tệp.
    ghi_doan(tmp_path, "dt-a", DOAN_A)
    kq = th.truy_hoi("dt-a", "Chống nước IP68", 2, "am_tiet", tmp_path)
    assert [ma for ma, _ in kq] == ["dt-a#002", "dt-a#003"] and kq[0][1] == kq[1][1] > 0

    th.xoa_dem()
    ghi_doan(tmp_path, "dt-a", DOAN_A, thu_tu=[0, 2, 1, 3, 4, 5])
    kq = th.truy_hoi("dt-a", "Chống nước IP68", 2, "am_tiet", tmp_path)
    assert [ma for ma, _ in kq] == ["dt-a#003", "dt-a#002"]


def test_moi_diem_bang_khong_thi_theo_thu_tu_tep(tmp_path):
    ghi_doan(tmp_path, "dt-a", DOAN_A, thu_tu=[3, 1, 5, 0, 2, 4])
    kq = th.truy_hoi("dt-a", "zzz", None, "am_tiet", tmp_path)
    assert [ma for ma, _ in kq] == ["dt-a#004", "dt-a#002", "dt-a#006", "dt-a#001", "dt-a#003", "dt-a#005"]
    assert {d for _, d in kq} == {0.0}


# --- Văn bản đánh chỉ mục, nhớ đệm ---

def test_chu_thich_duoc_danh_chi_muc(tmp_path):
    ghi_doan(tmp_path, "dt-a", [("Pin", []), ("Sạc", ["Thời gian sạc đo trong phòng thí nghiệm"]), ("Loa", []),
                                ("Camera", []), ("Màn hình", [])])
    kq = th.truy_hoi("dt-a", "phòng thí nghiệm", 1, "am_tiet", tmp_path)
    assert kq[0][0] == "dt-a#002"


@pytest.mark.parametrize("cach", th.CACH_TACH)
def test_so_dinh_don_vi_khop_tai_lieu_viet_roi(tmp_path, cach):
    # Quảng cáo viết liền '515mAh', tài liệu Samsung viết '515' và 'mAh' ở hai dòng.
    ghi_doan(tmp_path, "dt-a", [("Màn hình\n6,2 inch", []), ("Dung lượng pin\n515\nmAh", []), ("Âm thanh\nLoa kép", []),
                                ("Camera\n50 MP", []), ("Kết nối\nBluetooth 5.4", [])])
    kq = th.truy_hoi("dt-a", "pin 515mAh", 1, cach, tmp_path)
    assert kq[0][0] == "dt-a#002"


def test_nho_dem_theo_mau_va_cach_tach(nguon):
    a1 = th.lay_chi_muc("dt-a", "am_tiet", nguon)
    assert th.lay_chi_muc("dt-a", "am_tiet", nguon) is a1
    assert th.lay_chi_muc("dt-a", "tu", nguon) is not a1
    assert th.lay_chi_muc("dt-b", "am_tiet", nguon) is not a1
    th.xoa_dem()
    assert th.lay_chi_muc("dt-a", "am_tiet", nguon) is not a1


def test_dem_phan_biet_thu_muc_nguon(tmp_path):
    ghi_doan(tmp_path / "x", "dt-a", DOAN_A)
    ghi_doan(tmp_path / "y", "dt-a", [("Chỉ có đoạn này", [])] * 2 + DOAN_A[:4])
    # Cùng ma_mau và cách tách, khác thư mục nguồn thì không dùng chung chỉ mục.
    assert th.truy_hoi("dt-a", "pin", 1, "am_tiet", tmp_path / "x")[0][0] == "dt-a#001"
    assert th.truy_hoi("dt-a", "pin", 1, "am_tiet", tmp_path / "y")[0][0] == "dt-a#003"


# --- Tách chữ ---

@pytest.mark.parametrize("cach", th.CACH_TACH)
@pytest.mark.parametrize("van_ban, mong_doi", [
    ("515mAh", ["515", "mah"]),
    ("120Hz", ["120", "hz"]),
    ("IP68", ["ip", "68"]),
    ("5,4", ["5,4"]),
    ("28.999.000", ["28.999.000"]),
    ("pin 515mAh, sạc 25W.", ["pin", "515", "mah", "sạc", "25", "w"]),
    ("Giá 28.999.000đ; màn 6,3 inch (120Hz)!", ["giá", "28.999.000", "đ", "màn", "6,3", "inch", "120", "hz"]),
    ("Wi-Fi 6E", ["wi", "fi", "6", "e"]),
    ("", []),
    ("... - ,", []),
])
def test_tach_chu_hai_cach(cach, van_ban, mong_doi):
    assert th.tach_tu(van_ban, cach) == mong_doi


@pytest.mark.parametrize("cach", th.CACH_TACH)
def test_nfc_va_chu_thuong(cach):
    nfd = unicodedata.normalize("NFD", "Sạc NHANH Thời")
    assert nfd != unicodedata.normalize("NFC", nfd)
    assert th.tach_tu(nfd, cach)[0] == "sạc"
    assert th.tach_tu(nfd, cach) == th.tach_tu("sạc nhanh thời", cach)


def test_am_tiet_tach_tung_am_tiet_con_tu_giu_tu_ghep():
    van_ban = "Thời lượng pin xem video liên tục"
    assert th.tach_tu(van_ban, "am_tiet") == ["thời", "lượng", "pin", "xem", "video", "liên", "tục"]
    manh = th.tach_tu(van_ban, "tu")
    assert "thời_lượng" in manh and "liên_tục" in manh
    assert "thời" not in manh and "lượng" not in manh


def test_tu_khong_ghep_tu_qua_hai_dong():
    # 'Thời lượng' vắt qua hai dòng thì không ghép thành một từ.
    assert th.tach_tu("Thời\nlượng", "tu") == ["thời", "lượng"]


def test_cach_tach_la():
    with pytest.raises(ValueError, match="cách tách không hợp lệ"):
        th.tach_tu("pin", "ky_tu")


# --- Recall@k ---

XEP_HANG = {
    "t1": ["a#1", "a#2", "a#3", "a#4"],
    "t2": ["a#2", "a#3", "a#1", "a#4"],
    "t3": ["a#2", "a#3", "a#4", "a#1"],
    "t4": ["a#1", "a#2", "a#3", "a#4"],
    "t5": ["a#4", "a#3", "a#2", "a#1"],
}
BANG_CHUNG = {
    "t1": ["a#1"],            # hạng 1
    "t2": ["a#1", "a#3"],     # a#3 hạng 2: có ít nhất một đoạn trong top-k là trúng
    "t3": ["a#1"],            # hạng 4
    "t4": [],                 # không có bằng chứng: không vào mẫu số
    "t5": ["a#1"],            # hạng 4, nhưng bị loại
}


def test_hang_bang_chung():
    assert th.hang_bang_chung(["a#2", "a#1", "a#3"], ["a#3", "a#1"]) == 2
    assert th.hang_bang_chung(["a#2", "a#1"], ["a#9"]) is None
    assert th.hang_bang_chung([], ["a#1"]) is None
    assert th.hang_bang_chung(["a#1"], []) is None


def test_mau_so_bo_tuyen_bo_khong_bang_chung_va_danh_sach_loai():
    assert th.mau_so_recall(BANG_CHUNG) == ["t1", "t2", "t3", "t5"]
    assert th.mau_so_recall(BANG_CHUNG, loai=["t5"]) == ["t1", "t2", "t3"]
    assert th.mau_so_recall(BANG_CHUNG, loai=["t4", "t5"]) == ["t1", "t2", "t3"]  # t4 loại thêm cũng không đổi


def test_tinh_recall_du_lieu_nho():
    recall = th.tinh_recall(XEP_HANG, BANG_CHUNG, loai=["t5"])
    assert recall == {1: (1, 3), 3: (2, 3), 5: (3, 3), 8: (3, 3)}
    # Không loại t5 thì mẫu số là 4 và t5 (hạng 4) trúng từ k=5.
    assert th.tinh_recall(XEP_HANG, BANG_CHUNG) == {1: (1, 4), 3: (2, 4), 5: (4, 4), 8: (4, 4)}
    assert th.tinh_recall(XEP_HANG, BANG_CHUNG, loai=["t5"], ks=(2, 4)) == {2: (2, 3), 4: (3, 3)}


def test_tinh_recall_mau_so_bang_khong():
    assert th.tinh_recall({"t4": ["a#1"]}, {"t4": []}) == {1: (0, 0), 3: (0, 0), 5: (0, 0), 8: (0, 0)}


def test_recall_tu_truy_hoi_that(tmp_path):
    ghi_doan(tmp_path, "dt-a", DOAN_A)
    tuyen_bo = {"t1": "Chống nước IP68", "t2": "Dung lượng pin", "t3": "Camera"}
    bang_chung = {"t1": ["dt-a#003"], "t2": ["dt-a#001"], "t3": []}
    xep_hang = {ma: [m for m, _ in th.truy_hoi("dt-a", cau, None, "am_tiet", tmp_path)]
                for ma, cau in tuyen_bo.items()}
    assert th.tinh_recall(xep_hang, bang_chung) == {1: (1, 2), 3: (2, 2), 5: (2, 2), 8: (2, 2)}


# --- Script đo ---

def test_o_ty_le():
    assert do_recall.o_ty_le(47, 56) == "83,9% (47/56)"
    assert do_recall.o_ty_le(56, 56) == "100,0% (56/56)"
    assert do_recall.o_ty_le(0, 0) == "0/0"


def test_bao_cao_co_ghi_chu_ly_do_va_hang():
    tuyen_bo = [{"id": f"t{i}", "ma_mau": "dt-a", "tuyen_bo": f"Tuyên bố | số {i}"} for i in range(1, 5)]
    bang_chung = {"t1": ["a#1"], "t2": ["a#1"], "t3": ["a#1"], "t4": []}
    xep_hang = {
        "am_tiet": {"t1": ["a#1"] + [f"a#{i}" for i in range(2, 12)], "t2": ["a#2", "a#1"],
                    "t3": ["a#2", "a#3", "a#4", "a#5", "a#6", "a#7", "a#8", "a#9", "a#1"], "t4": ["a#1"]},
        "tu": {"t1": ["a#1"], "t2": ["a#2", "a#1"], "t3": ["a#1"], "t4": ["a#1"]},
    }
    dong = do_recall.tao_bao_cao(tuyen_bo, bang_chung, xep_hang, ["t2"], "lý do thử", {"dt-a": "Máy A"})
    chu = "\n".join(dong)
    assert do_recall.GHI_CHU in chu
    assert "4 tuyên bố, 1 không có bằng chứng (không tính), 1 bị loại; mẫu số 2" in chu
    assert "| t2 | dt-a | Tuyên bố \\| số 2 | lý do thử |" in chu
    assert "| Âm tiết | 50,0% (1/2) | 50,0% (1/2) | 50,0% (1/2) | 50,0% (1/2) |" in chu
    assert "| Từ (pyvi) | 100,0% (2/2) | 100,0% (2/2) | 100,0% (2/2) | 100,0% (2/2) |" in chu
    assert "| Máy A | Âm tiết | 2 |" in chu
    # Chỉ t3 có hạng 9 (> 8) ở cách âm tiết; t1 hạng 1, t2 bị loại.
    assert "| t3 | dt-a | a#1 | 9 | 1 | Tuyên bố \\| số 3 |" in chu
    assert "| t1 | dt-a | a#1 |" not in chu
