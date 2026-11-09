"""Test mô-đun chuẩn hóa (Bước 21, T5.4, T5.5).

Chuỗi "thật" lấy từ tập phát triển (dt-apple-iphone17, dt-xiaomi-15t, tn-samsung-buds3pro, dh-apple-watchse3):
quảng cáo data/quang_cao/qc-*.json (ma_qc) và đoạn data/nguon/<mẫu>/doan.jsonl (mã đoạn như dh-apple-watchse3#007).
Mọi chuỗi thật nằm trong bảng THAT, kèm nguồn; test_chuoi_that_la_chuoi_con_cua_nguon kiểm từng dòng.
Ca "tự đặt" (tập phát triển không có cách viết đó) ghi rõ trong chú thích, không có trong THAT.
Không mở dữ liệu của tập kiểm tra.
"""
import copy
import json

import pytest

from kiemchung import chuan_hoa as h
from kiemchung.cau_hinh import GOC, NHOM, doc_cau_hinh

MAU_PHAT_TRIEN = ("dt-apple-iphone17", "dt-xiaomi-15t", "tn-samsung-buds3pro", "dh-apple-watchse3")

# tên -> (nguồn, chuỗi thật). Một số quảng cáo của gpt-oss dùng khoảng trắng hẹp U+202F giữa số và đơn vị ( ).
THAT = {
    "xiaomi_3200_nit": ("dt-xiaomi-15t#037", "Màn hình siêu sáng 3.200 nit"),
    "xiaomi_phay": ("dt-xiaomi-15t#047", "Tối đa 13,19 giờ"),
    "xiaomi_6_83": ("dt-xiaomi-15t#022", "Màn hình 6.83\" bảo vệ mắt"),
    "apple_3000_met": ("dt-apple-iphone17#037", "được thử nghiệm ở độ cao lên đến 3.000 mét"),
    "apple_ip68": ("dt-apple-iphone17#007",
                   "Đạt mức IP68 (chống nước ở độ sâu tối đa 6 mét trong vòng tối đa 30 phút) theo tiêu chuẩn IEC 60529"),
    "buds_ip57": ("qc-tn-samsung-buds3pro-gptoss-description-ten_thong_so-1",
                  "Chuẩn chống nước IP57, bảo vệ tai nghe khỏi mồ hôi và mưa."),
    "buds_ipx4": ("qc-tn-samsung-buds3pro-gptoss-description-ten-1",
                  "Thiết kế ôm sát tai, vật liệu siêu nhẹ, chống nước IPX4, phù hợp cho mọi hoạt động thể thao."),
    "buds_ip57_tl": ("tn-samsung-buds3pro#044", "Chuẩn IP57"),
    "watch_50m_qc": ("qc-dh-apple-watchse3-gemini-social-ten_thong_so-1",
                     "Khả năng chống nước ở độ sâu 50m, sẵn sàng đồng hành trong mọi buổi tập bơi lội."),
    "watch_50m_tl": ("dh-apple-watchse3#016", "Chống nước ở độ sâu 50m (chống nước khi bơi)"),
    "xiaomi_3m": ("dt-xiaomi-15t#035", "Tăng cường khả năng chống nước đến độ sâu 3m."),
    "watch_kich_thuoc": ("qc-dh-apple-watchse3-gemini-description-ten_thong_so-1",
                         "Vỏ nhôm cao cấp với hai tùy chọn kích thước 40mm và 44mm"),
    "watch_dai_44": ("dh-apple-watchse3#002", "Dài: 44mm"),
    "apple_pin_30": ("dt-apple-iphone17#016", "Lên đến 30 giờ"),
    "apple_sac_40w": ("dt-apple-iphone17#016",
                      "Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C"),
    "apple_magsafe": ("dt-apple-iphone17#021", "Sạc không dây MagSafe lên đến 25W"),
    "apple_zoom_10x": ("dt-apple-iphone17#009", "Độ thu phóng kỹ thuật số lên đến 10x"),
    "apple_thich_ung": ("dt-apple-iphone17#004", "Công nghệ ProMotion với tốc độ làm mới thích ứng lên đến 120Hz"),
    "apple_do_sang": ("dt-apple-iphone17#005",
                      "Độ sáng tối đa 1000 nit (tiêu chuẩn); độ sáng đỉnh 1600 nit (HDR); "
                      "độ sáng đỉnh 3000 nit (ngoài trời); độ sáng tối thiểu 1 nit"),
    "apple_hon_24": ("qc-dt-apple-iphone17-gemini-landing-ten-1",
                     "Màn hình Super Retina XDR thế hệ mới cho màu sắc chân thực cùng thời lượng pin kéo dài hơn 24 giờ liên tục"),
    "apple_dam_bao_sau": ("qc-dt-apple-iphone17-gemini-social-ten_thong_so-1",
                          "Thời lượng pin lên đến 30 giờ cùng công nghệ sạc nhanh 50% trong 20 phút đảm bảo kết nối liền mạch suốt ngày dài."),
    "apple_luon_bat": ("qc-dt-apple-iphone17-gemini-description-ten_thong_so-1",
                       "Màn hình tích hợp Dynamic Island, công nghệ ProMotion 120Hz và tính năng Luôn Bật."),
    "xiaomi_luon_sau": ("qc-dt-xiaomi-15t-gptoss-social-ten-1",
                        "Công nghệ sạc nhanh 120 W chỉ trong 15 phút, bạn luôn luôn sẵn sàng."),
    "xiaomi_3200_nits_qc": ("qc-dt-xiaomi-15t-gemini-description-ten_thong_so-1",
                            "tần số quét 120Hz cùng độ sáng tối đa 3200 nits"),
    "xiaomi_typ": ("dt-xiaomi-15t#022", "Pin bền bỉ 5500mAh (typ)"),
    "xiaomi_67w_dinh": ("dt-xiaomi-15t#005", "Sạc nhanh HyperCharge 67WHỗ trợ PD3.0 / PD2.0"),
    "xiaomi_thong_thuong": ("dt-xiaomi-15t#005", "Pin Xiaomi Surge 5500mAh (thông thường)"),
    "watch_dinh_1000": ("dh-apple-watchse3#007", "Độ sáng đỉnh 1000 nit"),
    "watch_sac_15": ("dh-apple-watchse3#009", "Sạc 15 phút cho thời gian sử dụng bình thường lên đến 8 giờ"),
    "watch_80_45": ("qc-dh-apple-watchse3-gemini-description-ten_thong_so-1",
                    "thời lượng pin lên đến 18 giờ và khả năng sạc nhanh vượt trội, hỗ trợ sạc 80% chỉ trong 45 phút."),
    "buds_30_26": ("qc-tn-samsung-buds3pro-gptoss-social-ten_thong_so-1",
                   "thời lượng pin lên tới 30 giờ (tắt ANC) và 26 giờ (bật ANC)."),
    "watch_se3_qc": ("qc-dh-apple-watchse3-gemini-description-ten-1", "Apple Watch SE 3 là giải pháp công nghệ đeo tay"),
    "watch_se_qc": ("qc-dh-apple-watchse3-gemini-landing-ten-1", "Dòng thiết bị đeo Apple Watch SE đã đồng hành"),
    "xiaomi_15t_qc": ("qc-dt-xiaomi-15t-gemini-description-ten_thong_so-1", "Xiaomi 15T là dòng điện thoại thông minh cao cấp"),
    "xiaomi_14t": ("dt-xiaomi-15t#052", "Dữ liệu liên quan đến hệ thống Xiaomi 3D IceLoop được so sánh với Xiaomi 14T."),
    "iphone_16": ("dt-apple-iphone17#043",
                  "Bao bì của iPhone 17 được thiết kế hiệu quả hơn so với hộp đựng iPhone 16"),
    "iphone_air": ("dt-apple-iphone17#001", "iPhone Air"),
    "buds_ten_dai": ("tn-samsung-buds3pro#062", "Cách thay đổi đệm tai nghe Samsung Galaxy Buds3 Pro và Buds4 Pro"),
    "buds_ten_cach": ("tn-samsung-buds3pro#053", "Man, these Galaxy Buds 3 Pro are absolute beasts!"),
    "buds_hai_ten": ("tn-samsung-buds3pro#062", "Tại sao Galaxy Buds3/Buds3 Pro của bạn lại phát ra tiếng rít"),
    "watch_gps": ("dh-apple-watchse3#002", "Trọng Lượng (GPS): 32,9 gram"),
    "watch_gps_cellular": ("dh-apple-watchse3#002", "Trọng Lượng (GPS + Cellular): 33 gram"),
    "apple_zoom_2x": ("dt-apple-iphone17#009", "Đồng thời hỗ trợ Telephoto 2x chất lượng quang học 12MP"),
}


def that(ten):
    return THAT[ten][1]


@pytest.fixture(scope="module")
def cac_cau_hinh():
    return [doc_cau_hinh(n) for n in NHOM]


@pytest.fixture(scope="module")
def chung(cac_cau_hinh):
    return cac_cau_hinh[0]["chung"]


@pytest.fixture(scope="module")
def dien_thoai(cac_cau_hinh):
    return cac_cau_hinh[0]


@pytest.fixture()
def kieu(chung):
    """kieu(cau, chi_so_gia_tri, cum_them=None) -> (chuỗi giá trị, KieuGiaTri)."""
    def tim(cau, i=0, cum_them=None):
        g = h.tim_gia_tri(cau, chung)[i]
        return g.chu, h.tim_kieu_gia_tri(cau, g, chung, cum_them)
    return tim


# --- Truy lại nguồn ---

def _noi_dung_nguon(nguon):
    """Chỉ mở nguồn của tập phát triển."""
    if nguon.startswith("qc-"):
        assert any(nguon.startswith(f"qc-{m}-") for m in MAU_PHAT_TRIEN), nguon
        with open(GOC / "data" / "quang_cao" / f"{nguon}.json", encoding="utf-8") as f:
            return json.load(f)["noi_dung"]
    ma_mau = nguon.split("#")[0]
    assert ma_mau in MAU_PHAT_TRIEN, nguon
    with open(GOC / "data" / "nguon" / ma_mau / "doan.jsonl", encoding="utf-8") as f:
        for dong in f:
            d = json.loads(dong)
            if d["id"] == nguon:
                return d["noi_dung"]
    raise AssertionError(f"không có đoạn {nguon}")


@pytest.mark.parametrize("ten", sorted(THAT))
def test_chuoi_that_la_chuoi_con_cua_nguon(ten):
    nguon, chuoi = THAT[ten]
    assert chuoi in _noi_dung_nguon(nguon), f"{ten}: '{chuoi}' không có trong {nguon}"


# --- Số và đơn vị ---

@pytest.mark.parametrize("chu,mong_doi", [
    ("3.200", 3200),        # Xiaomi 15T, dt-xiaomi-15t#037: chấm ngăn hàng nghìn
    ("3.000", 3000),        # Apple, dt-apple-iphone17#037
    ("1.234.567", 1234567),  # tự đặt: hai dấu chấm
    ("4.5", 4.5),           # tự đặt: kiểu Samsung (tập phát triển không có "4.5 giờ"); chung.yaml cham_thap_phan
    ("6.83", 6.83),         # dt-xiaomi-15t#022: chấm theo sau 2 chữ số
    ("13,19", 13.19),       # dt-xiaomi-15t#047: phẩy thập phân
    ("7,0", 7.0),           # tn-samsung-buds3pro#042 ("Đến 7,0/30 giờ")
    ("1.234,5", 1234.5),    # tự đặt: chấm nghìn phối với phẩy thập phân
    ("0.500", 0.5),         # tự đặt: phần nguyên 0 luôn là thập phân
    ("30", 30),
])
def test_doc_so(chu, mong_doi):
    assert h.doc_so(chu) == pytest.approx(mong_doi)


@pytest.mark.parametrize("chu", ["", "abc", "1,2,3", "1.2.3", "3.2k"])   # tự đặt
def test_doc_so_khong_phai_so(chu):
    with pytest.raises(ValueError):
        h.doc_so(chu)


def test_doc_so_khop_chuoi_that():
    # 3.200 và 3.000 lấy ra từ chuỗi thật, không gõ lại tay
    assert h.doc_so(that("xiaomi_3200_nit").split()[-2]) == 3200
    assert h.doc_so(that("apple_3000_met").split()[-2]) == 3000


@pytest.mark.parametrize("chu,mong_doi", [
    ("giờ", "gio"), ("tiếng", "gio"), ("h", "gio"), ("Giờ", "gio"),   # tự đặt, theo T5.4
    ("phút", "phut"), ("min", "phut"),
    ("nit", "nit"), ("nits", "nit"), ("cd/m²", "nit"),
    ("mét", "m"), ("m", "m"), ("%", "phan_tram"), ("mAh", "mAh"), ("HZ", "Hz"), ("W", "W"), ("x", "x"),
    ("kg", None), ("", None),
])
def test_chuan_don_vi(chung, chu, mong_doi):
    assert h.chuan_don_vi(chu, chung) == mong_doi


def test_chuan_don_vi_phu_het_yaml(chung):
    for khoa, ds in chung["chuan_hoa"]["don_vi"].items():
        assert all(h.chuan_don_vi(a, chung) == khoa for a in ds)


def test_quy_doi_gio_phut():
    assert h.quy_doi(2, "gio", "phut") == 120
    assert h.quy_doi(90, "phut", "gio") == 1.5
    assert h.quy_doi(5, "nit", "nit") == 5
    with pytest.raises(ValueError):
        h.quy_doi(5, "gio", "nit")


# --- tim_gia_tri ---

def test_tim_gia_tri_ngan_hang_nghin_va_don_vi_nits(chung):
    gt = h.tim_gia_tri(that("xiaomi_3200_nits_qc"), chung)
    assert [(g.so, g.don_vi, g.chu) for g in gt] == [(120, "Hz", "120Hz"), (3200, "nit", "3200 nits")]
    gt = h.tim_gia_tri(that("xiaomi_3200_nit"), chung)
    assert [(g.so, g.don_vi) for g in gt] == [(3200, "nit")]


def test_tim_gia_tri_phay_thap_phan_va_met(chung):
    assert [(g.so, g.don_vi) for g in h.tim_gia_tri(that("xiaomi_phay"), chung)] == [(13.19, "gio")]
    assert [(g.so, g.don_vi) for g in h.tim_gia_tri(that("apple_3000_met"), chung)] == [(3000, "m")]


def test_tim_gia_tri_vi_tri_la_chi_so_trong_cau(chung):
    cau = that("watch_sac_15")
    for g in h.tim_gia_tri(cau, chung):
        assert cau[g.dau:g.cuoi] == g.chu


def test_tim_gia_tri_co_va_khong_khoang_trang(chung):
    # tự đặt, ghép từ các cách viết đã gặp: "50m" (Watch), "3000nits", "45W", "2x"; thêm "5 h", "30h", "50 m", "95 %"
    cau = "30h, 5 h, 45W, 3000nits, 2x, 50 m, 95 %, 80%, 120hz"
    gt = [(g.so, g.don_vi) for g in h.tim_gia_tri(cau, chung)]
    assert gt == [(30, "gio"), (5, "gio"), (45, "W"), (3000, "nit"), (2, "x"), (50, "m"), (95, "phan_tram"),
                  (80, "phan_tram"), (120, "Hz")]


def test_tim_gia_tri_ranh_gioi_chu(chung):
    # 44mm và 40mm (dh-apple-watchse3#002 và quảng cáo Watch): "m" không thành mét
    assert h.tim_gia_tri(that("watch_dai_44"), chung) == []
    assert h.tim_gia_tri(that("watch_kich_thuoc"), chung) == []
    # tự đặt: 5G không là gì, "5500mAh" là mAh chứ không phải m, "5 hơn" không là giờ
    gt = h.tim_gia_tri("Hỗ trợ 5G, pin 5500mAh, hơn 5 hơn", chung)
    assert [(g.so, g.don_vi) for g in gt] == [(5500, "mAh")]


def test_tim_gia_tri_bo_ma_ip_va_iso(chung):
    # IP68/IP57 (Apple, Samsung) và WR50, 5ATM, 10ATM (tự đặt) không là giá trị
    assert [(g.so, g.don_vi) for g in h.tim_gia_tri(that("apple_ip68"), chung)] == [(6, "m"), (30, "phut")]
    assert h.tim_gia_tri(that("buds_ip57"), chung) == []
    assert h.tim_gia_tri("Đồng hồ WR50, 5ATM, 10 ATM, IPX7", chung) == []


def test_tim_gia_tri_zoom(chung):
    assert [(g.so, g.don_vi) for g in h.tim_gia_tri(that("apple_zoom_2x"), chung)] == [(2, "x")]


# --- Mã IP ---

@pytest.mark.parametrize("ten,mong_doi", [
    ("apple_ip68", (6, 8)),      # tìm được trong câu dài
    ("buds_ip57", (5, 7)),
    ("buds_ip57_tl", (5, 7)),
    ("buds_ipx4", (None, 4)),    # chữ X ở chữ số bụi
])
def test_tach_ip_chuoi_that(ten, mong_doi):
    ip = h.tach_ip(that(ten))
    assert (ip.bui, ip.nuoc) == mong_doi


@pytest.mark.parametrize("chu,mong_doi", [   # tự đặt
    ("IPX7", (None, 7)), ("IP6X", (6, None)), ("ip68", (6, 8)), ("IP 67", (6, 7)), ("IPXX", (None, None)),
])
def test_tach_ip_tu_dat(chu, mong_doi):
    ip = h.tach_ip(chu)
    assert (ip.bui, ip.nuoc) == mong_doi


@pytest.mark.parametrize("chu", ["không có mã", "IP", "IP685", "SKIP68", "IP69K", that("watch_50m_tl")])
def test_tach_ip_khong_co(chu):
    assert h.tach_ip(chu) is None


@pytest.mark.parametrize("tb,tl,mong_doi", [
    ("IP67", "IP68", "kem_hon"),      # tự đặt tuyên bố, tài liệu IP68 là thật (dt-apple-iphone17#007): cùng nhánh ngâm
    ("IP68", "IP68", "bang"),
    ("IP58", "IP57", "tot_hon"),      # tự đặt: ví dụ mục 6.6, tài liệu IP57 là thật (tn-samsung-buds3pro#044)
    ("IP57", "IP57", "bang"),
    ("IP56", "IP57", "khac_nhanh"),   # tự đặt: 6 (tia nước) so 7 (ngâm)
    ("IPX4", "IP57", "khac_nhanh"),   # tuyên bố IPX4 thật (quảng cáo Buds3 Pro), tài liệu IP57 thật
    ("IPX5", "IP68", "khac_nhanh"),   # tự đặt: ví dụ mục 6.6
    ("IPX7", "IP68", "kem_hon"),      # tự đặt: bỏ qua bụi, 7 < 8
    ("IP68", "IPX7", "tot_hon"),
    ("IP5X", "IP57", "bang"),         # tự đặt: bỏ qua nước
    ("IP6X", "IP57", "tot_hon"),
    ("IP57", "IP68", "kem_hon"),      # bụi 5 < 6, nước 7 < 8
    ("IP58", "IP67", "tot_hon"),      # bụi kém hơn nhưng nước tốt hơn: thuận lợi hơn ở một thành phần
    ("IPX7", "IP6X", "khac_nhanh"),   # không còn thành phần để so
    ("IPX2", "IPX4", "kem_hon"),      # tự đặt (IPX2: tn-samsung-buds3pro#041 là mã của hộp sạc)
])
def test_so_ip(chung, tb, tl, mong_doi):
    assert h.so_ip(tb, tl, chung) == mong_doi


def test_so_ip_nhan_chuoi_that(chung):
    assert h.so_ip(that("buds_ipx4"), that("buds_ip57_tl"), chung) == "khac_nhanh"
    assert h.so_ip(h.tach_ip("IP68"), that("apple_ip68"), chung) == "bang"


def test_so_ip_khong_co_ma(chung):
    with pytest.raises(ValueError):
        h.so_ip("khong co ma", "IP68", chung)


# --- ISO 22810 ---

@pytest.mark.parametrize("chu,mong_doi", [   # tự đặt: tập phát triển chỉ viết "50m", không có WR/ATM
    ("WR50", 50), ("5ATM", 50), ("5 ATM", 50), ("wr 50", 50), ("10ATM", 100), ("10 ATM", 100),
    ("Đồng hồ chống nước 5ATM (WR50)", 50),
    ("3ATM", None),          # không có trong bảng quy_doi
    ("WR100", None), ("5ATMS", None), ("không có", None),
    ("chống nước 50m", None),   # "50m" là giá trị mét, do tim_gia_tri đọc (dh-apple-watchse3#016)
])
def test_doc_iso_22810(chung, chu, mong_doi):
    assert h.doc_iso_22810(chu, chung) == mong_doi


def test_doc_iso_22810_khop_dung_bang_yaml(chung):
    bang = chung["chuan_hoa"]["iso_22810"]["quy_doi"]
    for khoa, met in bang.items():
        assert h.doc_iso_22810(khoa, chung) == met
        assert h.doc_iso_22810(khoa.lower(), chung) == met
    # ATM/WR không có trong bảng thì None, kể cả khi quy tắc n ATM = 10n m suy ra được
    assert "3ATM" not in bang
    assert h.doc_iso_22810("3ATM", chung) is None


def test_met_chuoi_that_so_voi_iso(chung):
    # Watch SE 3: quảng cáo "50m" khớp tài liệu "50m" (cùng đơn vị mét)
    qc = h.tim_gia_tri(that("watch_50m_qc"), chung)[0]
    tl = h.tim_gia_tri(that("watch_50m_tl"), chung)[0]
    assert (qc.so, qc.don_vi) == (tl.so, tl.don_vi) == (50, "m")
    assert h.doc_iso_22810("5ATM", chung) == qc.so


# --- So sánh số ---

def test_nguong_bang_doc_tu_yaml(chung):
    assert h.nguong_bang(chung) == 0.01


@pytest.mark.parametrize("a,b,mong_doi", [
    (1000, 1010, True),       # đúng 1% so với b: vẫn bằng
    (1000, 1011, False),      # vượt 1%
    (1010, 1000, True),
    (3200, 3000, False),      # 3.200 (Xiaomi 15T) và 3.000 (iPhone 17) khác xa
    (50, 50, True),
    (0, 0, True),
    (1, 0, False),
])
def test_bang_nhau(a, b, mong_doi):
    assert h.bang_nhau(a, b, 0.01) is mong_doi


def test_bang_nhau_nguong_mac_dinh_va_tuy_chinh():
    assert h.bang_nhau(100, 101)
    assert not h.bang_nhau(100, 102)
    assert h.bang_nhau(100, 105, 0.05)


@pytest.mark.parametrize("tb,tl,huong,mong_doi", [
    (3000, 3200, "cao_hon_tot_hon", "kem_hon"),    # tự đặt: tuyên bố 3000 nit, tài liệu Xiaomi 3.200 nit
    (3200, 3000, "cao_hon_tot_hon", "tot_hon"),
    (3200, 3200, "cao_hon_tot_hon", "bang"),
    (3205, 3200, "cao_hon_tot_hon", "bang"),       # trong 1%
    (30, 20, "thap_hon_tot_hon", "kem_hon"),       # tự đặt: sạc 30 phút chậm hơn 20 phút
    (15, 20, "thap_hon_tot_hon", "tot_hon"),
    (20, 20, "thap_hon_tot_hon", "bang"),
    (45, 45, "thap_hon_tot_hon", "bang"),
])
def test_so_huong(tb, tl, huong, mong_doi):
    assert h.so_huong(tb, tl, huong) == mong_doi


def test_so_huong_huong_la():
    with pytest.raises(ValueError):
        h.so_huong(1, 2, "tuy_y")


# --- Kiểu giá trị ---

@pytest.mark.parametrize("ten,i,chu_gt,kieu_mong,cum,goi", [
    ("apple_pin_30", 0, "30 giờ", "toi_da", "lên đến", False),                       # dt-apple-iphone17#016
    ("apple_magsafe", 0, "25W", "toi_da", "lên đến", False),
    ("apple_zoom_10x", 0, "10x", "toi_da", "lên đến", False),
    ("xiaomi_phay", 0, "13,19 giờ", "toi_da", "tối đa", True),                       # "tối đa" là chữ gọi mức cao
    ("watch_dinh_1000", 0, "1000 nit", "toi_da", "đỉnh", True),                      # hướng dẫn mục 6.5
    ("xiaomi_3200_nits_qc", 1, "3200 nits", "toi_da", "tối đa", True),
    ("buds_30_26", 0, "30 giờ", "toi_da", "tới", False),                             # "lên tới": cụm "tới"
])
def test_kieu_toi_da(kieu, ten, i, chu_gt, kieu_mong, cum, goi):
    gt, k = kieu(that(ten), i)
    assert (gt.replace(" ", " "), k.kieu, k.cum, k.goi_muc_cao) == (chu_gt, kieu_mong, cum, goi)


def test_kieu_gia_tri_apple_do_sang_ba_muc(kieu):
    # dt-apple-iphone17#005: ba mức đều có chữ gọi mức cao; "tối thiểu" không phải cụm nào
    cau = that("apple_do_sang")
    ket_qua = [kieu(cau, i) for i in range(4)]
    assert [(g, k.kieu, k.cum, k.goi_muc_cao) for g, k in ket_qua[:3]] == [
        ("1000 nit", "toi_da", "tối đa", True),
        ("1600 nit", "toi_da", "đỉnh", True),
        ("3000 nit", "toi_da", "đỉnh", True),
    ]
    assert ket_qua[3][0] == "1 nit" and ket_qua[3][1].kieu == "khong_neu"


def test_kieu_dien_hinh_typ(kieu):
    gt, k = kieu(that("xiaomi_typ"))
    assert (gt, k.kieu, k.cum, k.goi_muc_cao) == ("5500mAh", "dien_hinh", "typ", False)


def test_kieu_thong_thuong_chi_la_dien_hinh_voi_cum_them(kieu, dien_thoai):
    cau = that("xiaomi_thong_thuong")
    assert kieu(cau)[1].kieu == "khong_neu"      # chung.yaml chưa có "(thông thường)"
    cum_them = dien_thoai["cach_dien_dat"]["kieu_dung_luong"]
    gt, k = kieu(cau, 0, cum_them)
    assert (gt, k.kieu, k.cum) == ("5500mAh", "dien_hinh", "(thông thường)")
    # cum_them cũng nhận dạng {kiểu: [cụm]}
    assert kieu(cau, 0, {"dien_hinh": ["(thông thường)"]})[1].kieu == "dien_hinh"


@pytest.mark.parametrize("cau,i,kieu_mong,cum", [   # tự đặt: tập phát triển không có cách viết này liền số
    ("Dung lượng pin điển hình 5000 mAh", 0, "dien_hinh", "điển hình"),
    ("Dung lượng pin 5000 mAh (typical)", 0, "dien_hinh", "typical"),
    ("Dung lượng pin định mức 5000 mAh", 0, "dinh_muc", "định mức"),
    ("Dung lượng pin 5000 mAh rated", 0, "dinh_muc", "rated"),
    ("Tần số quét thích ứng 120Hz", 0, "thich_ung", "thích ứng"),
    ("Pin up to 30 giờ", 0, "toi_da", "up to"),
    ("Độ sáng cực đại 3200 nit", 0, "toi_da", "cực đại"),
    ("Độ sáng peak 1000 nit", 0, "toi_da", "peak"),
    ("Độ sáng tối đa: 1000 nit", 0, "toi_da", "tối đa"),   # ':' giữa cụm và số
])
def test_kieu_tu_dat(kieu, cau, i, kieu_mong, cum):
    k = kieu(cau, i)[1]
    assert (k.kieu, k.cum) == (kieu_mong, cum)


def test_thich_ung_khong_lien_so_thi_theo_cum_lien_so(kieu):
    # dt-apple-iphone17#004: "thích ứng" cách số bởi "lên đến" nên kiểu là toi_da
    assert kieu(that("apple_thich_ung"))[1].kieu == "toi_da"


def test_khong_neu(kieu):
    assert kieu(that("xiaomi_3200_nit"))[1] == h.KieuGiaTri("khong_neu", None, False)
    assert kieu(that("watch_sac_15"), 0)[1].kieu == "khong_neu"     # 15 phút: "Sạc 15 phút ..."


def test_cum_gan_voi_con_so_khac_khong_tinh(kieu):
    # dt-apple-iphone17#016: "đến" thuộc 50%, không thuộc 20 phút
    cau = that("apple_sac_40w")
    g50, k50 = kieu(cau, 0)
    g20, k20 = kieu(cau, 1)
    assert (g50, k50.kieu) == ("50%", "toi_da")
    assert (g20, k20.kieu) == ("20 phút", "khong_neu")
    # Watch SE 3: "lên đến 8 giờ" thuộc 8 giờ, không thuộc 15 phút
    assert kieu(that("watch_sac_15"), 0) [1].kieu == "khong_neu"
    assert kieu(that("watch_sac_15"), 1) [1].kieu == "toi_da"
    # Apple: "lên đến 30 giờ" không lan sang 50% và 20 phút
    cau = that("apple_dam_bao_sau")
    assert [kieu(cau, i)[1].kieu for i in range(3)] == ["toi_da", "khong_neu", "khong_neu"]
    # Buds3 Pro: "lên tới" thuộc 30 giờ, 26 giờ không có cụm
    assert [kieu(that("buds_30_26"), i)[1].kieu for i in range(2)] == ["toi_da", "khong_neu"]
    # Watch: "lên đến 18 giờ" thuộc 18 giờ, 80% và 45 phút không có cụm
    assert [kieu(that("watch_80_45"), i)[1].kieu for i in range(3)] == ["toi_da", "khong_neu", "khong_neu"]


def test_cum_khong_lien_so_khong_tinh(kieu):
    # dt-xiaomi-15t#035: "đến độ sâu 3m", cụm "độ sâu" nằm giữa nên không liền
    gt, k = kieu(that("xiaomi_3m"))
    assert (gt, k.kieu) == ("3m", "khong_neu")
    # tự đặt: "đến" đứng sau số thuộc số kế tiếp
    assert kieu("Sạc 50% đến 80% trong 30 phút", 0)[1].kieu == "khong_neu"
    assert kieu("Sạc 50% đến 80% trong 30 phút", 1)[1].kieu == "toi_da"


@pytest.mark.parametrize("cau,cum", [   # tự đặt: tập phát triển không có từ khẳng định liền số
    ("Màn hình luôn đạt 120Hz", "luôn"),          # cách số một động từ
    ("Pin đảm bảo 6 giờ", "đảm bảo"),
    ("Pin bảo đảm 6 giờ", "bảo đảm"),
    ("Pin ít nhất 18 giờ", "ít nhất"),
    ("Màn hình mọi lúc 120Hz", "mọi lúc"),
    ("Pin đảm bảo kéo dài 6 giờ", "đảm bảo"),     # hai từ ở giữa
])
def test_tu_khang_dinh_nhom_chac_chan(kieu, cau, cum):
    k = kieu(cau)[1]
    assert (k.kieu, k.cum) == ("khang_dinh", cum)


@pytest.mark.parametrize("cau", [   # tự đặt
    "Pin đảm bảo luôn hoạt động bền bỉ suốt 6 giờ",         # ba từ ở giữa
    "Tai nghe B đảm bảo kết nối ổn định, nghe nhạc 8 giờ",   # hướng dẫn mục 6.2: từ ở vế khác của câu
    "Đảm bảo 6 giờ pin, thêm 8 giờ",                         # với 8 giờ: con số 6 giờ cắt ngang
])
def test_tu_khang_dinh_khong_gan_voi_con_so(kieu, cau):
    assert kieu(cau, -1)[1].kieu == "khong_neu"


def test_tu_khang_dinh_dung_sau_con_so_khong_tinh(kieu):
    # qc-dt-xiaomi-15t-gptoss-social-ten-1: "luôn luôn" đứng sau 15 phút
    cau = that("xiaomi_luon_sau")
    assert [kieu(cau, i)[1].kieu for i in range(2)] == ["khong_neu", "khong_neu"]
    # qc-dt-apple-iphone17-gemini-social-ten_thong_so-1: "đảm bảo" đứng sau 20 phút
    assert kieu(that("apple_dam_bao_sau"), 2)[1].kieu == "khong_neu"
    # tên tính năng "Luôn Bật" đứng sau 120Hz (V40)
    assert kieu(that("apple_luon_bat"))[1].kieu == "khong_neu"


@pytest.mark.parametrize("cau", [   # tự đặt, theo bo_qua_khi_co
    "Pin không đảm bảo 6 giờ", "Pin không được đảm bảo 6 giờ", "Pin không bảo đảm 6 giờ",
    "Màn hình không luôn 120Hz",
])
def test_tu_khang_dinh_dang_phu_dinh_bi_bo_qua(kieu, cau):
    assert kieu(cau)[1].kieu == "khong_neu"


def test_phu_dinh_roi_xuong_kieu_khac(kieu):
    # từ khẳng định bị bỏ qua thì vẫn xét tiếp kiểu: tự đặt
    assert kieu("Pin không đảm bảo, lên đến 6 giờ")[1].kieu == "toi_da"


def test_muc_san(kieu):
    gt, k = kieu(that("apple_hon_24"))
    assert (gt, k.kieu, k.cum) == ("24 giờ", "khang_dinh", "hơn")     # qc-dt-apple-iphone17-gemini-landing-ten-1
    # tự đặt: các dạng còn lại của tu_muc_san
    assert kieu("Pin trên 16 giờ")[1].cum == "trên"
    assert kieu("Pin không dưới 16 giờ")[1].cum == "không dưới"
    assert kieu("Pin 18 giờ trở lên")[1].cum == "trở lên"
    assert kieu("Pin 18 giờ trở lên")[1].kieu == "khang_dinh"
    assert kieu("Pin hơn 16 giờ")[1].goi_muc_cao is False


def test_muc_san_bo_tiep_hop_ra_khang_dinh_o_day(kieu):
    # dt-apple-iphone17#016: "40W trở lên" là điều kiện dạng số; hàm này chỉ báo cụm liền số, bộ quyết định
    # không hỏi kiểu của con số điều kiện (mục 6.2, V01). Ghi lại để thấy rõ trách nhiệm.
    gt, k = kieu(that("apple_sac_40w"), 2)
    assert (gt, k.kieu, k.cum) == ("40W", "khang_dinh", "trở lên")


def test_muc_san_khong_liền_khong_tinh(kieu):
    # tự đặt: "trên tai nghe", "hơn" cách số bởi chữ
    assert kieu("Hơn nữa pin 18 giờ")[1].kieu == "khong_neu"
    assert kieu("Hỗ trợ trên tai nghe 18 giờ")[1].kieu == "khong_neu"


def test_khang_dinh_thang_toi_da(kieu):
    # từ khẳng định xét trước kiểu: tự đặt
    assert kieu("Pin đảm bảo lên đến 6 giờ")[1].kieu == "khang_dinh"


# --- Danh sách cụm đọc từ YAML, không chép cứng ---

def _cum_yaml(muc):
    return [*(muc.get("tu_tai_lieu") or []), *(muc.get("hieu_biet_chung") or [])]


def test_moi_cum_trong_yaml_duoc_nhan(chung, kieu):
    """Mỗi cụm trong chung.yaml ra đúng kiểu khi đứng liền số (đối chiếu từng cụm, không có danh sách trong test)."""
    for ten_kieu, muc in chung["kieu_gia_tri"].items():
        for cum in _cum_yaml(muc):
            assert kieu(f"{cum} 100 nit")[1].kieu == ten_kieu, cum
    for cum in _cum_yaml(chung["tu_goi_muc_cao"]):
        k = kieu(f"{cum} 100 nit")[1]
        assert (k.kieu, k.goi_muc_cao) == (chung["tu_goi_muc_cao"]["mot_gia_tri"], True), cum
    for cum in chung["tu_khang_dinh"]["tu"]:
        assert kieu(f"{cum} 100 nit")[1].kieu == "khang_dinh", cum
    for mau in chung["tu_khang_dinh"]["tu_muc_san"]:
        assert kieu(mau.replace("<số>", "100 nit"))[1].kieu == "khang_dinh", mau
    for cum in chung["tu_khang_dinh"]["bo_qua_khi_co"]:
        assert kieu(f"{cum} 100 nit")[1].kieu != "khang_dinh", cum


def test_khong_co_cum_chep_cung_trong_ma(chung, kieu):
    """Thêm cụm vào bản sao cấu hình thì hàm nhận ngay; bớt đi thì không còn nhận."""
    moi = copy.deepcopy(chung)
    moi["tu_khang_dinh"]["tu"].append("cam kết")
    moi["kieu_gia_tri"]["dien_hinh"]["hieu_biet_chung"].append("trung bình")
    moi["tu_khang_dinh"]["tu_muc_san"].append("<số> đổ lên")
    cau = "Pin cam kết 6 giờ"
    g = h.tim_gia_tri(cau, moi)[0]
    assert h.tim_kieu_gia_tri(cau, g, moi).kieu == "khang_dinh"
    cau = "Pin trung bình 6 giờ"
    g = h.tim_gia_tri(cau, moi)[0]
    assert h.tim_kieu_gia_tri(cau, g, moi).kieu == "dien_hinh"
    cau = "Pin 6 giờ đổ lên"
    g = h.tim_gia_tri(cau, moi)[0]
    assert h.tim_kieu_gia_tri(cau, g, moi).kieu == "khang_dinh"
    # bản gốc không bị đổi và không nhận cụm mới
    assert kieu("Pin cam kết 6 giờ")[1].kieu == "khong_neu"
    # bớt hết cụm khẳng định: "luôn" không còn là từ khẳng định
    rong = copy.deepcopy(chung)
    rong["tu_khang_dinh"]["tu"] = []
    g = h.tim_gia_tri("Màn hình luôn đạt 120Hz", rong)[0]
    assert h.tim_kieu_gia_tri("Màn hình luôn đạt 120Hz", g, rong).kieu == "khong_neu"


def test_don_vi_doc_tu_yaml(chung):
    moi = copy.deepcopy(chung)
    moi["chuan_hoa"]["don_vi"]["phut"].append("phút đồng hồ")
    assert h.chuan_don_vi("phút đồng hồ", moi) == "phut"
    assert h.chuan_don_vi("phút đồng hồ", chung) is None
    assert [g.don_vi for g in h.tim_gia_tri("sạc 5 phút đồng hồ", moi)] == ["phut"]


# --- Sản phẩm và phiên bản ---

@pytest.mark.parametrize("ten,ma_mau", [
    ("watch_se3_qc", "dh-apple-watchse3"),
    ("xiaomi_15t_qc", "dt-xiaomi-15t"),
    ("buds_ten_dai", "tn-samsung-buds3pro"),      # "Samsung Galaxy Buds3 Pro" dài hơn "Galaxy Buds4 Pro"
    ("buds_ten_cach", "tn-samsung-buds3pro"),     # "Galaxy Buds 3 Pro" (có khoảng trắng)
    ("iphone_16", "dt-apple-iphone17"),           # bằng độ dài "iPhone 16": bi_danh thắng
    ("watch_se_qc", None),                        # "Apple Watch SE" nằm trong khong_nham_voi
    ("xiaomi_14t", None),                         # chỉ nhắc Xiaomi 14T
    ("iphone_air", None),
    ("buds_hai_ten", None),                       # ghi nhận: "Galaxy Buds3" (12) dài hơn "Buds3 Pro" (9)
])
def test_tim_san_pham_chuoi_that(cac_cau_hinh, ten, ma_mau):
    assert h.tim_san_pham(that(ten), cac_cau_hinh) == ma_mau


@pytest.mark.parametrize("chu,ma_mau", [   # tự đặt
    ("iPhone 17", "dt-apple-iphone17"),
    ("IPHONE 17 mới", "dt-apple-iphone17"),
    ("Apple iPhone 17 256GB", "dt-apple-iphone17"),
    ("iPhone 17 Pro", None),
    ("iPhone 17 Pro Max", None),
    ("iPhone 17e", None),
    ("iPhone 175", None),                  # ranh giới chữ
    ("Xiaomi 15T Pro", None),
    ("xiaomi 15t", "dt-xiaomi-15t"),
    ("Apple Watch SE 3", "dh-apple-watchse3"),   # dài hơn "Apple Watch SE" trong khong_nham_voi
    ("Watch SE 3", "dh-apple-watchse3"),
    ("Apple Watch SE 2", None),
    ("Galaxy Buds3 Pro", "tn-samsung-buds3pro"),
    ("Galaxy Buds3", None),
    ("Bán điện thoại cũ", None),
    ("", None),
])
def test_tim_san_pham_tu_dat(cac_cau_hinh, chu, ma_mau):
    assert h.tim_san_pham(chu, cac_cau_hinh) == ma_mau


def test_tim_san_pham_moi_bi_danh_dan_den_ma_mau(cac_cau_hinh):
    for cau_hinh in cac_cau_hinh:
        for ma, sp in cau_hinh["san_pham"].items():
            for bi_danh in sp["bi_danh"]:
                # bí danh nằm trong khong_nham_voi của mẫu khác dài hơn (Watch SE 3 ⊃ Watch SE) cũng phải ra đúng mẫu
                assert h.tim_san_pham(bi_danh, cac_cau_hinh) == ma, bi_danh
            for ten in sp["khong_nham_voi"]:
                assert h.tim_san_pham(ten, cac_cau_hinh) is None, ten


@pytest.mark.parametrize("ten,mong_doi", [
    ("watch_kich_thuoc", ["co_vo"]),              # "40mm và 44mm": một khóa, không lặp
    ("watch_dai_44", ["co_vo"]),
    ("watch_gps", ["gps"]),
    ("watch_gps_cellular", ["gps_cellular"]),     # không kèm "gps"
])
def test_tim_phien_ban_chuoi_that(cac_cau_hinh, ten, mong_doi):
    assert h.tim_phien_ban(that(ten), "dh-apple-watchse3", cac_cau_hinh) == mong_doi


def test_tim_phien_ban_tu_dat(cac_cau_hinh):
    ma = "dh-apple-watchse3"
    assert h.tim_phien_ban("GPS 44mm", ma, cac_cau_hinh) == ["gps", "co_vo"]
    assert h.tim_phien_ban("44mm GPS + Cellular", ma, cac_cau_hinh) == ["co_vo", "gps_cellular"]
    assert h.tim_phien_ban("Bản 41mm", ma, cac_cau_hinh) == []
    assert h.tim_phien_ban("GPS 44mm", "dt-apple-iphone17", cac_cau_hinh) == []   # mẫu không có bi_danh_phien_ban
    assert h.tim_phien_ban("GPS", "khong-co-mau", cac_cau_hinh) == []


# --- Bước 22: dạng "a / b <đơn vị>", tim_so, tên tính năng ---
# "Đến 7,0/30 giờ" là chuỗi thật của tn-samsung-buds3pro#042; "Đến 7 / 30 giờ" của #038 là chữ dọc (mỗi mảnh một dòng).

def _doan(ma):
    with open(GOC / "data" / "nguon" / ma.split("#")[0] / "doan.jsonl", encoding="utf-8") as f:
        return next(json.loads(d) for d in f if json.loads(d)["id"] == ma)["noi_dung"]


def test_cap_so_gach_cheo_chuoi_that_042(chung):
    van_ban = _doan("tn-samsung-buds3pro#042")
    assert "Đến 7,0/30 giờ" in van_ban
    gts = h.tim_gia_tri("Đến 7,0/30 giờ", chung)
    assert [(g.so, g.don_vi) for g in gts] == [(7.0, "gio"), (30.0, "gio")]
    assert gts[0].dau_nhom == gts[1].dau_nhom == gts[0].dau == 4
    assert gts[1].chu == "30 giờ"
    assert [g.so for g in h.tim_gia_tri(van_ban.replace("\n", " "), chung) if g.don_vi == "gio"][:4] == [7.0, 30.0, 6.0, 26.0]


@pytest.mark.parametrize("chu,mong_doi", [
    ("Đến 7 / 30 giờ", [(7.0, "gio"), (30.0, "gio")]),
    ("lên tới 6/26 giờ", [(6.0, "gio"), (26.0, "gio")]),
    ("sạc 50 / 80%", [(50.0, "phan_tram"), (80.0, "phan_tram")]),
    ("5/ 24 tiếng", [(5.0, "gio"), (24.0, "gio")]),
])
def test_cap_so_gach_cheo_tu_dat(chung, chu, mong_doi):
    assert [(g.so, g.don_vi) for g in h.tim_gia_tri(chu, chung)] == mong_doi


def test_chu_doc_phai_gop_khoang_trang_truoc(chung):
    doc = _doan("tn-samsung-buds3pro#038")
    assert "Đến\n7\n/\n30\ngiờ" in doc
    assert [g.so for g in h.tim_gia_tri(doc, chung)] == []     # mỗi mảnh một dòng: không khớp
    gop = " ".join(doc.split())
    assert [(g.so, g.don_vi) for g in h.tim_gia_tri(gop, chung)] == [(7.0, "gio"), (30.0, "gio"), (6.0, "gio"), (26.0, "gio")]


def test_gach_cheo_khong_pha_cac_dang_cu(chung):
    assert [g.don_vi for g in h.tim_gia_tri("độ sáng 3000 cd/m²", chung)] == ["nit"]
    ket = h.tim_gia_tri("Pin 30 giờ / 45 phút sạc", chung)   # "/" đứng sau đơn vị: hai giá trị riêng, không phải cặp
    assert [(g.so, g.dau_nhom) for g in ket] == [(30.0, None), (45.0, None)]
    assert h.tim_gia_tri("IP68/WR50", chung) == []


def test_kieu_gia_tri_cap_so_ap_cho_ca_b(chung):
    cau = "Thời gian phát Đến 7,0/30 giờ"
    a, b = h.tim_gia_tri(cau, chung)
    ka, kb = h.tim_kieu_gia_tri(cau, a, chung), h.tim_kieu_gia_tri(cau, b, chung)
    assert (ka.kieu, ka.cum) == (kb.kieu, kb.cum) == ("toi_da", "đến")
    # Số b đứng đơn lẻ (không thuộc cặp) thì cụm đứng xa không áp.
    lon = h.tim_gia_tri("Đến 7 giờ, còn 30 giờ", chung)[1]
    assert h.tim_kieu_gia_tri("Đến 7 giờ, còn 30 giờ", lon, chung).kieu == "khong_neu"
    ka, kb = (h.tim_kieu_gia_tri("luôn 7/30 giờ", g, chung) for g in h.tim_gia_tri("luôn 7/30 giờ", chung))
    assert ka.kieu == kb.kieu == "khang_dinh"


def test_tim_so_co_va_khong_don_vi():
    ket = h.tim_so("Thời gian phát nhạc (bật ANC) Lên đến 6, IP57, 3.000 mét, 4,5 giờ, WR50, G720")
    assert [s.so for s in ket] == [6.0, 3000.0, 4.5]
    assert [s.chu for s in ket] == ["6", "3.000", "4,5"]
    assert ket[0].dau == 38 and ket[0].cuoi == 39
    assert [s.so for s in h.tim_so("Đến 7,0/30 giờ")] == [7.0, 30.0]
    assert h.tim_so("không có số") == []


def test_ten_tinh_nang_chua_tu_khang_dinh_khong_tinh(chung, kieu):
    cau = "Màn hình Luôn Bật 120Hz"
    assert kieu(cau)[1].kieu != "khang_dinh"
    assert kieu("Công nghệ ProMotion 120Hz và tính năng Luôn Bật 120Hz")[1].kieu != "khang_dinh"
    assert kieu("Luôn kết nối 5G và luôn đạt 120Hz")[1].kieu == "khang_dinh"    # "luôn đạt" nằm ngoài tên tính năng
    assert kieu("Màn hình luôn đạt 120Hz")[1].kieu == "khang_dinh"
    assert kieu("Màn hình Luôn Bật, luôn đạt 120Hz")[1].kieu == "khang_dinh"


def test_don_vi_dinh_tu_viet_hoa_67w_ho_tro(chung):
    gts = h.tim_gia_tri(that("xiaomi_67w_dinh"), chung)
    assert [(g.so, g.don_vi) for g in gts] == [(67.0, "W")]
    assert gts[0].chu == "67W" and that("xiaomi_67w_dinh")[gts[0].dau:gts[0].cuoi] == "67W"
    assert [(g.so, g.don_vi) for g in h.tim_gia_tri("Pin 5000mAhDung lượng", chung)] == [(5000.0, "mAh")]   # đơn vị dài vẫn khớp trước
    assert [(g.so, g.don_vi) for g in h.tim_gia_tri("2xZoom quang học", chung)] == [(2.0, "x")]   # chấp nhận


def test_don_vi_dinh_chu_thuong_hoac_chu_hoa_don_van_khong_doc(chung):
    for chu in ("màn hình 5G", "chuẩn IP68", "tần số 120Hz", "44mm", "67Wh", "67Wi-Fi", "30 giờx", "50mAhx", "7WHO", "5xyz"):
        da_co = [(g.so, g.don_vi) for g in h.tim_gia_tri(chu, chung)]
        assert da_co == {"tần số 120Hz": [(120.0, "Hz")]}.get(chu, []), chu
    assert h.tim_gia_tri("67W Hỗ trợ", chung)[0].don_vi == "W"
