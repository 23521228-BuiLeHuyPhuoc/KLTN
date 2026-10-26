import copy

import pytest

from kiemchung import cau_hinh as ch


@pytest.fixture(scope="module")
def tai_lieu():
    return ch.tai_lieu_phat_trien()


@pytest.fixture(scope="module")
def mau():
    return ch.doc_mau()


@pytest.fixture()
def tai_nghe():
    return copy.deepcopy(ch.doc_cau_hinh("tai_nghe"))


def test_cau_hinh_that_khong_co_loi():
    assert ch.kiem_tat_ca() == {"chung": [], "dien_thoai": [], "tai_nghe": [], "dong_ho": []}


def test_du_16_thuoc_tinh_moi_thuoc_tinh_du_khoa():
    so = {n: len(ch.doc_cau_hinh(n)["thuoc_tinh"]) for n in ch.NHOM}
    assert so == {"dien_thoai": 8, "tai_nghe": 4, "dong_ho": 4}
    for n in ch.NHOM:
        for tt in ch.doc_cau_hinh(n)["thuoc_tinh"].values():
            assert set(ch.KHOA_BAT_BUOC) <= set(tt)


def test_thoi_luong_pin_va_sac_nhanh_theo_hang_cong_bo_dung_luong_dien_hinh():
    for n in ch.NHOM:
        tt = ch.doc_cau_hinh(n)["thuoc_tinh"]
        assert tt["thoi_luong_pin"]["kieu_gia_tri_mac_dinh"] == "toi_da"
        assert tt["sac_nhanh"]["kieu_gia_tri_mac_dinh"] == "toi_da"
        if "dung_luong_pin" in tt:
            assert tt["dung_luong_pin"]["kieu_gia_tri_mac_dinh"] == "dien_hinh"


def test_thieu_luat_chan_dieu_kien_la_bi_bao(tai_lieu):
    chung = copy.deepcopy(ch.doc_yaml(ch.THU_MUC / "chung.yaml"))
    chung["dieu_kien_la"]["nguyen_nhan_D1a"] = "so_thang"
    loi = ch.kiem_chung(chung, tai_lieu[0])
    assert any("điều kiện lạ không bao giờ ra Đúng" in d for d in loi)
    del chung["dieu_kien_la"]
    assert "chung: thiếu khóa dieu_kien_la" in ch.kiem_chung(chung, tai_lieu[0])


def test_chuan_hoa_chu():
    assert ch.chuan_hoa_chu("Cáp sạc USB‑C  (1m)") == "cáp sạc usb-c (1m)"


def test_thieu_khoa_bi_bao(tai_nghe, tai_lieu, mau):
    del tai_nghe["thuoc_tinh"]["dung_luong_pin"]["don_vi"]
    loi = ch.kiem_nhom(tai_nghe, *tai_lieu, mau)
    assert "tai_nghe.dung_luong_pin: thiếu khóa don_vi" in loi


def test_loai_dieu_kien_ngoai_sau_loai_bi_bao(tai_nghe, tai_lieu, mau):
    tai_nghe["thuoc_tinh"]["dung_luong_pin"]["dieu_kien_bat_buoc"]["bo_phan"] = "mau_sac"
    loi = ch.kiem_nhom(tai_nghe, *tai_lieu, mau)
    assert any("không thuộc sáu loại" in d for d in loi)


def test_cach_hieu_chua_khai_bao_bi_bao(tai_nghe, tai_lieu, mau):
    tai_nghe["thuoc_tinh"]["thoi_luong_pin"]["hieu_thong_thuong"]["hoat_dong"] = "chay_bo"
    loi = ch.kiem_nhom(tai_nghe, *tai_lieu, mau)
    assert any("'chay_bo' chưa khai báo" in d for d in loi)


def test_cum_khong_co_trong_tai_lieu_phat_trien_bi_bao(tai_nghe, tai_lieu, mau):
    tai_nghe["cach_dien_dat"]["che_do_chong_on"]["bat"]["tu_tai_lieu"].append("chế độ siêu chống ồn")
    loi = ch.kiem_nhom(tai_nghe, *tai_lieu, mau)
    assert any("'chế độ siêu chống ồn' không có" in d for d in loi)


def test_can_cu_tu_tap_kiem_tra_bi_bao(tai_nghe, tai_lieu, mau):
    tai_nghe["thuoc_tinh"]["dung_luong_pin"]["can_cu"].append("tn-apple-airpods4#002")
    loi = ch.kiem_nhom(tai_nghe, *tai_lieu, mau)
    assert any("không thuộc tập phát triển" in d for d in loi)
    assert any("nhắc mẫu tập kiểm tra tn-apple-airpods4" in d for d in loi)


def test_bang_bi_danh_thieu_mau_bi_bao(tai_nghe, tai_lieu, mau):
    del tai_nghe["san_pham"]["tn-apple-airpods4"]
    loi = ch.kiem_nhom(tai_nghe, *tai_lieu, mau)
    assert "tai_nghe: bảng bí danh thiếu tn-apple-airpods4" in loi


def test_cach_goi_theo_hang_tro_toi_che_do_chua_khai_bao_bi_bao(tai_lieu, mau):
    dt = copy.deepcopy(ch.doc_cau_hinh("dien_thoai"))
    dt["thuoc_tinh"]["do_sang"]["cach_goi_theo_hang"]["Apple"]["đỉnh"].append("sieu_sang")
    loi = ch.kiem_nhom(dt, *tai_lieu, mau)
    assert any("chế độ chưa khai báo 'sieu_sang'" in d for d in loi)
