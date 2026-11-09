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


def test_dieu_kien_dang_so_da_khai_bao():
    dt = ch.doc_cau_hinh("dien_thoai")["thuoc_tinh"]
    assert dt["sac_nhanh"]["dieu_kien_so"]["bo_tiep_hop"] == {"don_vi": "W", "thoa_khi": "tuyen_bo_lon_hon_hoac_bang"}
    assert dt["sac_nhanh"]["dieu_kien_so"]["moc_phan_tram"]["thoa_khi"] == "tuyen_bo_nho_hon_hoac_bang"
    # chenh_lech_nhiet_do: Bước 22, hướng dẫn mục 11.3 (V08), "từ 5K trở xuống" của Xiaomi 15T.
    assert set(dt["khang_nuoc"]["dieu_kien_so"]) == {"do_sau", "thoi_gian_ngam", "chenh_lech_nhiet_do"}
    assert dt["khang_nuoc"]["dieu_kien_so"]["chenh_lech_nhiet_do"] == {"don_vi": "K", "thoa_khi": "tuyen_bo_nho_hon_hoac_bang"}
    dh = ch.doc_cau_hinh("dong_ho")["thuoc_tinh"]
    assert set(dh["sac_nhanh"]["dieu_kien_so"]) == {"bo_tiep_hop", "moc_phan_tram", "so_phut_sac"}
    tn = ch.doc_cau_hinh("tai_nghe")["thuoc_tinh"]
    assert set(tn["khang_nuoc"]["dieu_kien_so"]) == {"do_sau", "thoi_gian_ngam"}


def test_thoa_dieu_kien_so():
    assert not ch.thoa_dieu_kien_so("tuyen_bo_lon_hon_hoac_bang", 20, 40)   # củ 20W, tài liệu 40W trở lên
    assert ch.thoa_dieu_kien_so("tuyen_bo_lon_hon_hoac_bang", 65, 40)
    assert ch.thoa_dieu_kien_so("tuyen_bo_nho_hon_hoac_bang", 3, 6)         # ngâm 3 m, tài liệu tối đa 6 m
    assert not ch.thoa_dieu_kien_so("tuyen_bo_nho_hon_hoac_bang", 10, 6)
    assert not ch.thoa_dieu_kien_so("tuyen_bo_nho_hon_hoac_bang", 80, 50)   # mốc 80%, tài liệu mốc 50%
    assert ch.thoa_dieu_kien_so("bang", 30.2, 30)                           # trong ngưỡng 1%
    with pytest.raises(ValueError):
        ch.thoa_dieu_kien_so("khoang", 1, 1)


def test_dieu_kien_so_sai_khai_bao_bi_bao(tai_lieu, mau):
    dt = copy.deepcopy(ch.doc_cau_hinh("dien_thoai"))
    so = dt["thuoc_tinh"]["sac_nhanh"]["dieu_kien_so"]
    so["bo_tiep_hop"]["thoa_khi"] = "lon_hon"
    so["moc_phan_tram"]["don_vi"] = "phan_nghin"
    del dt["thuoc_tinh"]["khang_nuoc"]["dieu_kien_so"]["do_sau"]
    loi = ch.kiem_nhom(dt, *tai_lieu, mau)
    assert any("quan hệ 'lon_hon' không hợp lệ" in d for d in loi)
    assert any("đơn vị 'phan_nghin'" in d for d in loi)
    assert "dien_thoai.khang_nuoc.do_sau: điều kiện dạng số chưa khai báo trong dieu_kien_so" in loi


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


def test_thieu_nhom_muc_san_hoac_cum_phu_bi_bao(tai_lieu):
    chung = copy.deepcopy(ch.doc_yaml(ch.THU_MUC / "chung.yaml"))
    assert chung["tu_khang_dinh"]["tu_muc_san"] and chung["cum_phu"]["mau"]
    del chung["tu_khang_dinh"]["tu_muc_san"]
    del chung["cum_phu"]
    loi = ch.kiem_chung(chung, tai_lieu[0])
    assert any("thiếu tu_muc_san" in d for d in loi)
    assert any("thiếu cum_phu.mau" in d for d in loi)


def test_phia_cua_gia_tri_chi_nhan_tai_lieu_hoac_tuyen_bo(tai_lieu, mau):
    dt = copy.deepcopy(ch.doc_cau_hinh("dien_thoai"))
    hoat_dong = dt["cach_dien_dat"]["hoat_dong"]
    # "Sử dụng liên tục": tên bài đo ở phía tài liệu; "liên tục" ở phía tuyên bố là chưa nêu hoạt động (hướng dẫn mục 6.8, ý 3).
    assert hoat_dong["su_dung_lien_tuc"]["phia"] == "tai_lieu" and hoat_dong["chua_ro_hoat_dong"]["phia"] == "tuyen_bo"
    assert "liên tục" in hoat_dong["chua_ro_hoat_dong"]["hieu_biet_chung"]
    assert ch.kiem_nhom(dt, *tai_lieu, mau) == []
    hoat_dong["su_dung_lien_tuc"]["phia"] = "ca_hai"
    loi = ch.kiem_nhom(dt, *tai_lieu, mau)
    assert any("hoat_dong.su_dung_lien_tuc: phia 'ca_hai' phải là tai_lieu hoặc tuyen_bo" in d for d in loi)


def test_chi_thuoc_tinh_gioi_han_cum_kem_hop_sac(tai_lieu, mau):
    tn = copy.deepcopy(ch.doc_cau_hinh("tai_nghe"))
    bo_phan = tn["cach_dien_dat"]["bo_phan"]
    # Mục 6.8 ý 6: "kèm hộp sạc", "tổng cộng"... là bộ phận kèm hộp sạc chỉ với thời lượng pin (rà soát 02/11).
    assert bo_phan["kem_hop_sac"]["chi_thuoc_tinh"] == ["thoi_luong_pin"]
    assert ch.kiem_nhom(tn, *tai_lieu, mau) == []
    bo_phan["kem_hop_sac"]["chi_thuoc_tinh"] = ["khong_co"]
    assert any("chi_thuoc_tinh 'khong_co'" in d for d in ch.kiem_nhom(tn, *tai_lieu, mau))
    bo_phan["kem_hop_sac"]["chi_thuoc_tinh"] = []
    assert any("chi_thuoc_tinh phải là danh sách" in d for d in ch.kiem_nhom(tn, *tai_lieu, mau))


def test_su_dung_dung_dung_rieng_la_chua_ro_hoat_dong_moi_nhom():
    # QĐ12 (02/11): "sử dụng", "dùng" đứng riêng và "liên tục" là chưa nêu hoạt động, ở mọi nhóm có điều kiện hoạt động.
    for nhom in ch.NHOM:
        hd = ch.doc_cau_hinh(nhom)["cach_dien_dat"]["hoat_dong"]["chua_ro_hoat_dong"]
        assert hd["phia"] == "tuyen_bo"
        assert {"liên tục", "sử dụng", "dùng"} <= set(hd["hieu_biet_chung"]), nhom


def test_anh_sang_manh_khong_con_o_che_do_ngoai_troi():
    # QĐ14 (02/11): "ánh sáng mạnh" chưa được duyệt và trùng "Dưới ánh sáng mạnh" của Xiaomi (tu_tang_sang).
    ngoai_troi = ch.doc_cau_hinh("dien_thoai")["cach_dien_dat"]["che_do_hien_thi"]["ngoai_troi"]
    assert "ánh sáng mạnh" not in ngoai_troi["hieu_biet_chung"]


# --- Bước 22: gia_tri_ngam, cap_so_gach_cheo, cum_khong_phai_dieu_kien, ten_tinh_nang ---

def test_khoa_moi_cua_cau_hinh_that():
    dt = ch.doc_cau_hinh("dien_thoai")["cach_dien_dat"]
    assert dt["moc_phan_tram"]["gia_tri_so"]["gia_tri_ngam"] == {"sạc đầy": 100}
    assert dt["dien_tich_do"]["gia_tri_so"]["gia_tri_ngam"] == {"toàn màn hình": 100}
    assert ch.doc_cau_hinh("tai_nghe")["thuoc_tinh"]["thoi_luong_pin"]["cap_so_gach_cheo"] == ["tai_nghe", "kem_hop_sac"]
    chung = ch.doc_yaml(ch.THU_MUC / "chung.yaml")
    assert "cả ngày" in chung["cum_khong_phai_dieu_kien"]
    assert "Luôn Bật" in chung["tu_khang_dinh"]["ten_tinh_nang"]


def test_gia_tri_ngam_hong_bi_bao(tai_lieu, mau):
    dt = copy.deepcopy(ch.doc_cau_hinh("dien_thoai"))
    kb = dt["cach_dien_dat"]["moc_phan_tram"]["gia_tri_so"]
    kb["gia_tri_ngam"] = {"sạc đầy": "một trăm", "sạc nửa": 50}
    loi = ch.kiem_nhom(dt, *tai_lieu, mau)
    assert any("gia_tri_ngam 'sạc đầy' phải là số" in d for d in loi)
    assert any("gia_tri_ngam 'sạc nửa' không phải cụm của giá trị này" in d for d in loi)
    kb["gia_tri_ngam"] = {"sạc đầy": True}
    assert any("phải là số" in d for d in ch.kiem_nhom(dt, *tai_lieu, mau))
    kb["gia_tri_ngam"] = ["sạc đầy"]
    assert any("gia_tri_ngam phải là bảng" in d for d in ch.kiem_nhom(dt, *tai_lieu, mau))


def test_cap_so_gach_cheo_hong_bi_bao(tai_nghe, tai_lieu, mau):
    tt = tai_nghe["thuoc_tinh"]["thoi_luong_pin"]
    tt["cap_so_gach_cheo"] = ["tai_nghe", "hop_bi_mat"]
    assert any("cap_so_gach_cheo 'hop_bi_mat' chưa khai báo" in d for d in ch.kiem_nhom(tai_nghe, *tai_lieu, mau))
    tt["cap_so_gach_cheo"] = ["tai_nghe"]
    assert any("phải là danh sách hai giá trị khác nhau" in d for d in ch.kiem_nhom(tai_nghe, *tai_lieu, mau))
    tt["cap_so_gach_cheo"] = ["tai_nghe", "tai_nghe"]
    assert any("phải là danh sách hai giá trị khác nhau" in d for d in ch.kiem_nhom(tai_nghe, *tai_lieu, mau))
    tt["cap_so_gach_cheo"] = ["tai_nghe", "kem_hop_sac"]
    del tt["dieu_kien_bat_buoc"]["bo_phan"]
    assert any("cần điều kiện bo_phan" in d for d in ch.kiem_nhom(tai_nghe, *tai_lieu, mau))


def test_cum_khong_phai_dieu_kien_va_ten_tinh_nang_phai_la_danh_sach_chuoi(tai_lieu):
    chung = copy.deepcopy(ch.doc_yaml(ch.THU_MUC / "chung.yaml"))
    assert ch.kiem_chung(chung, tai_lieu[0]) == []
    chung["cum_khong_phai_dieu_kien"] = "cả ngày"
    chung["tu_khang_dinh"]["ten_tinh_nang"] = ["Luôn Bật", 5]
    loi = ch.kiem_chung(chung, tai_lieu[0])
    assert "chung.cum_khong_phai_dieu_kien: phải là danh sách chuỗi" in loi
    assert "chung.tu_khang_dinh.ten_tinh_nang: phải là danh sách chuỗi" in loi
    del chung["cum_khong_phai_dieu_kien"]
    assert "chung.cum_khong_phai_dieu_kien: phải là danh sách chuỗi" in ch.kiem_chung(chung, tai_lieu[0])
