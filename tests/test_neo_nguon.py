"""Test neo nguồn (Bước 22, mục 5 của luan_van/buoc22_thiet_ke_trich_xuat.md).

Chữ thật lấy từ tập phát triển (tn-samsung-buds3pro#038, #042, #044); ca khác tự đặt. Không mở dữ liệu tập kiểm tra.
"""
import json

import pytest

from kiemchung import neo_nguon as nn
from kiemchung.cau_hinh import GOC, THU_MUC, doc_yaml


@pytest.fixture(scope="module")
def chung():
    return doc_yaml(THU_MUC / "chung.yaml")


def doan(ma):
    with open(GOC / "data" / "nguon" / ma.split("#")[0] / "doan.jsonl", encoding="utf-8") as f:
        d = next(json.loads(x) for x in f if json.loads(x)["id"] == ma)
    return "\n".join([d["noi_dung"], *d["chu_thich"]])


def gt(chu, trich, don_vi=None):
    return {"chu": chu, "don_vi": don_vi, "trich": trich}


# --- chuan_so_khop ---

def test_chuan_so_khop_quy_tac():
    assert nn.chuan_so_khop("  Tắt ANC:\n  Đến 9 / 30 giờ. ")[0] == "tắt anc đến 9 30 giờ"
    assert nn.chuan_so_khop("(Giờ, bật ANC)")[0] == "giờ bật anc"
    assert nn.chuan_so_khop("Lên đến 3.000 mét; 4,5 giờ.")[0] == "lên đến 3.000 mét 4,5 giờ"
    assert nn.chuan_so_khop("USB‑C – “nháy”")[0] == "usb c nháy"
    assert nn.chuan_so_khop("50 mAh")[0] == "50 mah"
    assert nn.chuan_so_khop("...")[0] == ""
    assert nn.chuan_so_khop("")[0] == ""


def test_chuan_so_khop_khoang_trang_hep_va_nbsp():
    assert nn.chuan_so_khop("7 giờ nữa")[0] == "7 giờ nữa"
    assert nn.chuan_so_khop("7 giờ")[0] == nn.chuan_so_khop("7 giờ")[0]


def test_chuan_so_khop_nfc_va_ban_do():
    goc = "Chó Đến 7 / 30"      # "ó" viết rời (o + dấu sắc)
    chuoi, ban_do = nn.chuan_so_khop(goc)
    assert chuoi == "chó đến 7 30" and len(ban_do) == len(chuoi)
    assert goc[ban_do[chuoi.index("đến")]] == "Đ"
    assert goc[ban_do[chuoi.index("30")]] == "3"
    assert ban_do == sorted(ban_do)


def test_tim_trich_ve_vi_tri_goc():
    nguon = "Thời gian phát\nTắt Tính năng ANC\nĐến\n7\n/\n30\ngiờ"
    cho = nn.tim_trich(nguon, "tắt tính năng anc: Đến 7 / 30 giờ")
    assert cho == [(15, len(nguon))]
    assert nguon[cho[0][0]:cho[0][1]].startswith("Tắt Tính năng ANC")
    assert nn.tim_trich(nguon, "...") == []
    assert nn.tim_trich(nguon, "Tắt ANC") == []
    assert len(nn.tim_trich("a 6 b 6", "6")) == 2


# --- gia_tri: số ---

def test_so_dung_va_sai(chung):
    ok = nn.kiem_gia_tri(gt("6", "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ", "giờ"), chung, "gio")
    assert ok == {"gia_tri": 6.0, "khoa_don_vi": "gio"}
    assert nn.kiem_gia_tri(gt("7", "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ", "giờ"), chung, "gio") == nn.LY_DO_SO
    assert nn.kiem_gia_tri(gt("sáu", "lên đến 6 giờ", "giờ"), chung, "gio") == nn.LY_DO_SO


def test_don_vi_sai(chung):
    assert nn.kiem_gia_tri(gt("6", "lên đến 6 giờ", "phút"), chung, "gio") == nn.LY_DO_DON_VI
    assert nn.kiem_gia_tri(gt("6", "lên đến 6 giờ", "bí ẩn"), chung, "gio") == nn.LY_DO_DON_VI
    # tiếng = giờ: cùng khóa
    assert nn.kiem_gia_tri(gt("6", "lên đến 6 tiếng", "giờ"), chung, "gio")["khoa_don_vi"] == "gio"


def test_cap_so_gach_cheo_ca_hai_so_dat(chung):
    for chu, mong in (("9", 9.0), ("30", 30.0)):
        assert nn.kiem_gia_tri(gt(chu, "Tắt ANC: Đến 9 / 30 giờ", "giờ"), chung, "gio") == {"gia_tri": mong, "khoa_don_vi": "gio"}
    assert nn.kiem_gia_tri(gt("7", "Đến 7,0/30 giờ", "giờ"), chung, "gio")["gia_tri"] == 7.0
    assert nn.kiem_gia_tri(gt("30", "Đến 9 / 30 giờ", "phút"), chung, "gio") == nn.LY_DO_DON_VI
    assert nn.kiem_gia_tri(gt("24", "Đến 9 / 30 giờ", "giờ"), chung, "gio") == nn.LY_DO_SO


def test_chu_doc_cua_038_duoc_gop_khoang_trang(chung):
    van_ban = doan("tn-samsung-buds3pro#038")
    trich = "Tắt Tính năng ANC\nĐến\n7\n/\n30\ngiờ"
    assert nn.co_trong_nguon(van_ban, trich)
    assert nn.co_trong_nguon(van_ban, "Tắt Tính năng ANC Đến 7 / 30 giờ")
    for chu in ("7", "30"):
        assert isinstance(nn.kiem_gia_tri(gt(chu, trich, "giờ"), chung, "gio"), dict)


def test_dong_khong_don_vi_044(chung):
    van_ban = doan("tn-samsung-buds3pro#044")
    trich = "Thời gian phát nhạc (bật ANC)\nLên đến 6"
    assert nn.co_trong_nguon(van_ban, "Thời gian phát nhạc (bật ANC) Lên đến 6")
    for don_vi in (None, "giờ"):
        assert nn.kiem_gia_tri(gt("6", trich, don_vi), chung, "gio") == {"gia_tri": 6.0, "khoa_don_vi": "gio"}
    # đơn vị khác đơn vị của thuộc tính, trong khi dòng không có đơn vị: không đạt
    assert nn.kiem_gia_tri(gt("6", trich, "phút"), chung, "gio") == nn.LY_DO_DON_VI
    assert nn.kiem_gia_tri(gt("5", trich, None), chung, "gio") == nn.LY_DO_SO


def test_khoang_trang_hep_giua_so_va_don_vi(chung):
    trich = "lên đến 6 giờ"
    assert nn.kiem_gia_tri(gt("6", trich, "giờ"), chung, "gio")["khoa_don_vi"] == "gio"
    assert nn.co_trong_nguon("Pin lên đến 6 giờ liên tục", trich)
    assert nn.co_trong_nguon("Pin lên đến 6 giờ liên tục", "lên đến 6 giờ")


def test_so_co_dau_ngan_hang_nghin(chung):
    assert nn.kiem_gia_tri(gt("3.000", "độ sáng 3.000 nit", "nit"), chung, "nit")["gia_tri"] == 3000.0
    assert nn.kiem_gia_tri(gt("3000", "độ sáng 3.000 nit", "nit"), chung, "nit")["gia_tri"] == 3000.0
    assert nn.kiem_gia_tri(gt("4,5", "Lên đến 4.5", "giờ"), chung, "gio") == {"gia_tri": 4.5, "khoa_don_vi": "gio"}


# --- gia_tri: mã ---

def test_ma_ip(chung):
    assert nn.kiem_gia_tri(gt("IP68", "Chống nước IP68"), chung, None)["gia_tri"] == {"bui": 6, "nuoc": 8}
    assert nn.kiem_gia_tri(gt("IPX7", "chuẩn IPX7"), chung, None)["gia_tri"] == {"bui": None, "nuoc": 7}
    assert nn.kiem_gia_tri(gt("IP68", "Chống nước IP67"), chung, None) == nn.LY_DO_MA
    assert nn.kiem_gia_tri(gt("IP68", "Chống nước tốt"), chung, None) == nn.LY_DO_MA


def test_wr50_va_iso(chung):
    r = nn.kiem_gia_tri(gt("WR50", "Chống nước ISO 22810 WR50"), chung, "m")
    assert r == {"gia_tri": 50.0, "khoa_don_vi": "m"}
    assert nn.kiem_gia_tri(gt("5ATM", "Chịu nước 5 ATM"), chung, None)["gia_tri"] == 50.0
    assert nn.kiem_gia_tri(gt("WR50", "Chịu nước 10ATM"), chung, None) == nn.LY_DO_MA


def test_phu_dinh_khong_co_kha_nang_khang_nuoc(chung):
    trich = "Hộp sạc không có khả năng kháng nước"
    assert nn.kiem_gia_tri(gt("không", trich), chung, None) == {"gia_tri": "khong", "khoa_don_vi": None}
    assert nn.kiem_gia_tri(gt("Không", "Hộp sạc không chống nước"), chung, None)["gia_tri"] == "khong"
    assert nn.kiem_gia_tri(gt("không", "Hộp sạc kháng nước"), chung, None) == nn.LY_DO_MA
    assert nn.kiem_gia_tri(gt("không", "Không khuyến cáo khi tắm biển"), chung, None) == nn.LY_DO_MA


def test_khang_dinh_co_chi_o_khang_nuoc(chung):
    def f(chu, trich, tt="khang_nuoc"):
        return nn.kiem_gia_tri(gt(chu, trich), chung, None, tt)

    assert f("có", "Hộp sạc Galaxy Buds3 Pro cũng kháng nước") == {"gia_tri": "co", "khoa_don_vi": None}
    assert f("", "hộp sạc cũng chống nước")["gia_tri"] == "co"
    assert f("Có", "hộp sạc chống nước")["gia_tri"] == "co"
    assert f("có", "Hộp sạc không có khả năng kháng nước") == nn.LY_DO_MA          # "không" đứng trước cụm
    assert f("có", "Hộp sạc cũng hỗ trợ sạc nhanh") == nn.LY_DO_MA
    assert f("không", "Hộp sạc không có khả năng kháng nước")["gia_tri"] == "khong"
    assert f("có", "kháng nước", tt="thoi_luong_pin") == nn.LY_DO_SO              # chỉ thuộc tính khang_nuoc


# --- một mục ---

def muc(**kw):
    return {"san_pham": None, "gia_tri": None, "dieu_kien": [], **kw}


def dk(i, loai, cum, trich):
    return {"i": i, "loai": loai, "cum": cum, "trich": trich}


def test_neo_muc_bo_truong_sai_va_giu_truong_dung(chung):
    nguon = "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ"
    m = muc(san_pham={"chu": "Buds3", "trich": "bịa đặt"}, gia_tri=gt("7", "lên đến 6 giờ", "giờ"),
            dieu_kien=[dk(0, "che_do_hoat_dong", "tắt ANC", "Thời gian đàm thoại (tắt ANC)"),
                       dk(1, "che_do_hoat_dong", "bật ANC", "Thời gian đàm thoại (tắt ANC)"),    # cụm bịa
                       dk(2, "kieu_gia_tri", "lên đến", "câu không có trong nguồn")])
    moi, bi = nn.neo_nguon_muc(m, nguon, chung, "gio")
    assert moi["san_pham"] is None and moi["gia_tri"] is None
    assert [d["i"] for d in moi["dieu_kien"]] == [0]
    assert bi == [("san_pham", nn.LY_DO_TRICH), ("gia_tri", nn.LY_DO_SO), ("dieu_kien[1]", nn.LY_DO_CUM),
                  ("dieu_kien[2]", nn.LY_DO_TRICH)]
    assert m["san_pham"]["chu"] == "Buds3"      # không sửa đầu vào


def test_neo_muc_trich_khong_co_trong_nguon(chung):
    m = muc(gia_tri=gt("6", "Thời lượng pin tới 6 giờ", "giờ"))
    moi, bi = nn.neo_nguon_muc(m, "Pin lên đến 6 giờ", chung, "gio")
    assert moi["gia_tri"] is None and bi == [("gia_tri", nn.LY_DO_TRICH)]


def test_neo_muc_san_pham_ten_khong_trong_trich(chung):
    m = muc(san_pham={"chu": "Buds4", "trich": "Galaxy Buds3 Pro"})
    moi, bi = nn.neo_nguon_muc(m, "Galaxy Buds3 Pro", chung, None)
    assert moi["san_pham"] is None and bi == [("san_pham", nn.LY_DO_TEN)]
    moi, bi = nn.neo_nguon_muc(muc(san_pham={"chu": "Buds3 Pro", "trich": "Galaxy Buds3 Pro"}), "Galaxy Buds3 Pro", chung, None)
    assert moi["san_pham"]["chu"] == "Buds3 Pro" and bi == []


def test_neo_muc_tat_kiem_nguon_khong_bo_gi(chung):
    m = muc(san_pham={"chu": "Buds3", "trich": "bịa đặt"}, gia_tri=gt("7", "câu bịa", "phút"),
            dieu_kien=[dk(0, "che_do_hoat_dong", "bật ANC", "câu bịa")])
    moi, bi = nn.neo_nguon_muc(m, "Pin lên đến 6 giờ", chung, "gio", kiem_nguon=False)
    assert bi == [] and moi["san_pham"] == m["san_pham"] and moi["dieu_kien"] == m["dieu_kien"]
    assert moi["gia_tri"]["gia_tri"] == 7.0 and moi["gia_tri"]["khoa_don_vi"] == "phut"
    moi, _ = nn.neo_nguon_muc(muc(gia_tri=gt("7", "x")), None, chung, "gio", kiem_nguon=False)
    assert moi["gia_tri"]["khoa_don_vi"] == "gio"        # không ghi đơn vị: lấy theo thuộc tính
    moi, bi = nn.neo_nguon_muc(muc(gia_tri=gt("nhiều", "x")), None, chung, "gio", kiem_nguon=False)
    assert moi["gia_tri"] is None and bi == [("gia_tri", nn.LY_DO_SO)]
