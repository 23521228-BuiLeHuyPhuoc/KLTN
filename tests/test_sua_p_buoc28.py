"""Test hồi quy các sửa của Bước 28 (T-01, T-06, T-09, T-10, T-20, T-21, T-22, T-29, T-30) và test tích hợp đầu-cuối (T-23).

Test tích hợp đi từ JSON thô LLM trả về, qua trich_xuat.xu_ly (neo nguồn, hiểu điều kiện, kiểm tra đầy đủ) rồi quyet_dinh.quyet_dinh.
Văn bản đoạn là chữ thật của tập phát triển (data/nguon của dt-apple-iphone17, dt-xiaomi-15t, dh-apple-watchse3, tn-samsung-buds3pro);
JSON LLM tự dựng cho các ví dụ của hướng dẫn (mục 6.3, V08, V23); bản ghi thật của tập chính đọc từ cache kết quả trích xuất
(ket_qua/trich_xuat/chinh_*.jsonl, tra_ve_tho). Không dùng bản ghi bộ thử, không gọi LLM, không mở dữ liệu tập kiểm tra.
"""
import copy
import json
from pathlib import Path

import pytest

from kiemchung import chuan_hoa as ch, neo_nguon as nn, p as pp, quyet_dinh as qd, trich_xuat as tx, truy_hoi as th
from kiemchung.cau_hinh import doc_cau_hinh, thoa_dieu_kien_so

ROOT = Path(__file__).resolve().parents[1]
CHINH_TRICH_XUAT = ROOT / "ket_qua/trich_xuat/chinh_openai_gpt-oss-120b_k5_am_tiet.jsonl"
CHINH_NHAN = ROOT / "data/nhan/chinh.jsonl"
CF = {n: doc_cau_hinh(n) for n in ("dien_thoai", "tai_nghe", "dong_ho")}
TAT_CA = tx.tat_ca_cau_hinh()
IPHONE, XIAOMI, WATCH, BUDS = "dt-apple-iphone17", "dt-xiaomi-15t", "dh-apple-watchse3", "tn-samsung-buds3pro"
NHOM = {IPHONE: "dien_thoai", XIAOMI: "dien_thoai", WATCH: "dong_ho", BUDS: "tai_nghe"}


# --- Dựng ca ---

def doan(ma_mau, *so):
    van_ban = dict(th.doc_doan(ma_mau))
    return [(f"{ma_mau}#{s}", van_ban[f"{ma_mau}#{s}"]) for s in so]


def gt(chu, trich, don_vi=None):
    return {"chu": chu, "don_vi": don_vi, "trich": trich}


def dk(loai, cum, trich=None):
    return {"loai": loai, "cum": cum, "trich": trich or cum}


def tb(thuoc_tinh, gia_tri, dieu_kien=(), san_pham=None):
    return {"san_pham": san_pham, "thuoc_tinh": thuoc_tinh, "gia_tri": gia_tri, "dieu_kien": list(dieu_kien)}


def tl(ma_doan, gia_tri, dieu_kien=()):
    return {"ma_doan": ma_doan, "san_pham": None, "gia_tri": gia_tri, "dieu_kien": list(dieu_kien)}


def chay(ma_mau, chu, tuyen_bo, bang_chung, ds_doan, **kw):
    """JSON thô LLM -> xu_ly -> quyet_dinh. Trả (kết quả quyết định, kết quả xu_ly)."""
    cf = CF[NHOM[ma_mau]]
    ket = tx.xu_ly({"tuyen_bo": tuyen_bo, "bang_chung": bang_chung}, chu, ds_doan, ma_mau, cf, TAT_CA)
    assert ket["loi"] is None
    ban_ghi = {"id": "t", "ma_mau": ma_mau, "chu_tuyen_bo": chu, "loi": None, "neo_nguon": True, "kiem_day_du": True, **ket}
    return qd.quyet_dinh(ban_ghi, cf, **kw), ket


def ket(k):
    return (k["nhan"], k["dong_d"], k["loai"])


# --- Ví dụ mục 6.3 của hướng dẫn (T-20, T-23) ---

TRICH_IP68_IPHONE = "Đạt mức IP68 (chống nước ở độ sâu tối đa 6 mét trong vòng tối đa 30 phút)"


def ca_muc_6_3(chu):
    return chay(IPHONE, chu, tb("khang_nuoc", gt("IP68", "IP68"), [dk("dieu_kien_do", "độ sâu 6 mét", "chống nước ở độ sâu 6 mét"),
                                                                    dk("dieu_kien_do", "trong 1 giờ", "trong 1 giờ")],
                                {"chu": "iPhone 17", "trich": "iPhone 17"}),
                [tl(f"{IPHONE}#007", gt("IP68", TRICH_IP68_IPHONE),
                    [dk("dieu_kien_do", "độ sâu tối đa 6 mét", TRICH_IP68_IPHONE), dk("dieu_kien_do", "tối đa 30 phút", TRICH_IP68_IPHONE)])],
                doan(IPHONE, "007"))


def test_muc_6_3_6_met_trong_1_gio_la_lech_d4_khong_phai_d1a():
    k, x = ca_muc_6_3("iPhone 17 đạt chuẩn IP68, chống nước ở độ sâu 6 mét trong 1 giờ")
    # "1 giờ" quy đổi thành 60 phút của điều kiện thoi_gian_ngam, không còn là cụm lạ
    assert x["tuyen_bo"]["dieu_kien"]["thoi_gian_ngam"] == {"so": 60.0, "don_vi": "phut"} and x["tuyen_bo"]["dieu_kien_khac"] == []
    assert x["bang_chung"][0]["dieu_kien"]["thoi_gian_ngam"] == {"so": 30.0, "don_vi": "phut"}
    assert ket(k) == ("LECH", "D4", "doi_dieu_kien")
    assert "thời gian ngâm 30 phút trở xuống" in k["ly_do"] and "60 phút" in k["ly_do"]


def test_muc_6_3_ngam_30_phut_van_dung():
    k, _ = ca_muc_6_3("iPhone 17 đạt chuẩn IP68, chống nước ở độ sâu 6 mét trong 1 giờ".replace("1 giờ", "30 phút"))
    assert ket(k) == ("DUNG", "D3", None)
    k, _ = ca_muc_6_3("iPhone 17 đạt chuẩn IP68, chống nước ở độ sâu 6 mét trong 0,5 giờ")   # 0,5 giờ = 30 phút
    assert ket(k) == ("DUNG", "D3", None)


# --- V08, V23 (T-23; T-09, T-01 d) ---

def test_v08_xiaomi_ip68_dung_du_co_so_dieu_kien_khac_don_vi():
    """V08 Đúng D3. Thêm hai mục tài liệu LLM liệt kê nhầm con số điều kiện (3 m, 30 phút) làm giá trị: T-09 loại chúng, không ra D1b."""
    d = doan(XIAOMI, "012", "035")
    trich_ip = "Khả năng chống bụi và nước\nIP68"
    chu = "Xiaomi 15T đạt chuẩn chống nước IP68."
    ct = "ngâm trong nước ngọt tĩnh lặng ở độ sâu 3 mét; tối đa 30 phút; với mức chênh lệch nhiệt độ giữa nước và sản phẩm là từ 5K trở xuống"
    bang_chung = [tl(f"{XIAOMI}#012", gt("IP68", trich_ip), [dk("dieu_kien_do", "ngâm trong nước ngọt tĩnh lặng", ct),
                                                          dk("dieu_kien_do", "chênh lệch nhiệt độ giữa nước và sản phẩm là từ 5K trở xuống", ct)]),
                  tl(f"{XIAOMI}#035", gt("IP68", "IP68\nKhả năng chống nước và bụi")),
                  tl(f"{XIAOMI}#035", gt("3", "chống nước đến độ sâu 3m", "m")),
                  tl(f"{XIAOMI}#035", gt("30", "trong 30 phút", "phút"))]
    k, x = chay(XIAOMI, chu, tb("khang_nuoc", gt("IP68", "IP68"), san_pham={"chu": "Xiaomi 15T", "trich": "Xiaomi 15T"}), bang_chung, d)
    ly_do = {b["chi_so"]: b["ly_do"] for b in x["bang_chung_bi_loai"]}
    assert ly_do == {2: ["don_vi_khong_khop"], 3: ["don_vi_khong_khop"]}, x["bang_chung_bi_loai"]
    assert len(x["bang_chung"]) == 2 and ket(k) == ("DUNG", "D3", None)


def test_v23_xiaomi_hypercharge_67w_lech_d4_ten_tinh_nang_khong_la_dieu_kien_la():
    """V23 Lệch D4 bo_dieu_kien: "Sạc nhanh HyperCharge" là tên dòng, không phải điều kiện lạ (T-01 d): không D1a, củ sạc 67W vẫn ra D4."""
    d = doan(XIAOMI, "005")
    chu = "Xiaomi 15T hỗ trợ sạc nhanh HyperCharge 67W."
    ten = "Sạc nhanh HyperCharge 67W"
    k, x = chay(XIAOMI, chu, tb("cong_suat_sac", gt("67", "HyperCharge 67W", "W"), [dk("phu_kien", "sạc nhanh HyperCharge", ten)],
                                {"chu": "Xiaomi 15T", "trich": "Xiaomi 15T"}),
                [tl(f"{XIAOMI}#005", gt("67", ten, "W"), [dk("phu_kien", "Sạc nhanh HyperCharge", ten),
                                                          dk("phu_kien", "củ sạc Xiaomi 67W hoặc cao hơn",
                                                             "Máy được khuyến cáo sử dụng củ sạc Xiaomi 67W hoặc cao hơn.")])], d)
    assert x["tuyen_bo"]["dieu_kien_khac"] == [] and x["bang_chung"][0]["dieu_kien_khac"] == []
    assert x["bang_chung"][0]["dieu_kien"]["bo_tiep_hop"] == {"so": 67.0, "don_vi": "W"}
    assert ket(k) == ("LECH", "D4", "bo_dieu_kien")


# --- Ví dụ khác của hướng dẫn: giờ ↔ phút ở sạc nhanh đồng hồ (T-20) ---

def sac_dong_ho(chu, gia_tri, dieu_kien_tb, bang_chung):
    return chay(WATCH, chu, tb("sac_nhanh", gia_tri, dieu_kien_tb, {"chu": "Apple Watch SE 3", "trich": "Apple Watch SE 3"}), bang_chung,
                doan(WATCH, "009"))


DONG_15P = "Sạc 15 phút cho thời gian sử dụng bình thường lên đến 8 giờ"
DONG_80 = "Sạc lên đến 80% trong khoảng 45 phút"


def test_dang_sac_nhanh_theo_dieu_kien_khong_theo_don_vi_cua_gia_tri():
    # "sạc 15 phút dùng 90 phút": giá trị tính bằng phút nhưng là dạng 2 (số phút sạc), so với "lên đến 8 giờ" = 480 phút: Đúng
    k, x = sac_dong_ho("Apple Watch SE 3 sạc 15 phút với củ sạc 20W dùng được 90 phút", gt("90", "dùng được 90 phút", "phút"),
                       [dk("dieu_kien_do", "sạc 15 phút", "sạc 15 phút"), dk("phu_kien", "củ sạc 20W", "với củ sạc 20W")],
                       [tl(f"{WATCH}#009", gt("8", DONG_15P, "giờ"), [dk("dieu_kien_do", "Sạc 15 phút", DONG_15P)]),
                        tl(f"{WATCH}#009", gt("45", DONG_80, "phút"), [dk("dieu_kien_do", "Sạc lên đến 80%", DONG_80)])])
    assert qd.dang_sac_nhanh(x["tuyen_bo"]) == 2
    assert ket(k) == ("DUNG", "D3", None) and k["bang_chung"] == [f"{WATCH}#009"]
    # "sạc 80% trong 0,5 giờ": dạng 1 bằng giờ; 30 phút nhanh hơn mọi giá trị công bố (45 phút): Sai
    k, x = sac_dong_ho("Apple Watch SE 3 sạc 80% với củ sạc 20W trong 0,5 giờ", gt("0,5", "trong 0,5 giờ", "giờ"),
                       [dk("dieu_kien_do", "sạc 80%", "sạc 80%"), dk("phu_kien", "củ sạc 20W", "với củ sạc 20W")],
                       [tl(f"{WATCH}#009", gt("45", DONG_80, "phút"), [dk("dieu_kien_do", "Sạc lên đến 80%", DONG_80)])])
    assert qd.dang_sac_nhanh(x["tuyen_bo"]) == 1
    assert ket(k) == ("SAI", "D5", "doi_gia_tri")


def test_v34_bo_tiep_hop_chi_ghi_trong_chu_thich_la_lech_d4():
    """V34 Lệch bo_dieu_kien: bộ tiếp hợp 20W của Watch SE 3 chỉ nằm trong chú thích của đoạn #009; LLM không ghi nó làm điều kiện của dòng,
    kiểm tra đầy đủ tìm trong cả đoạn (HD mục 4). Chỉ ra Đúng nếu bỏ sót chú thích."""
    k, x = sac_dong_ho("Apple Watch SE 3 sạc 80% trong khoảng 45 phút", gt("45", "trong khoảng 45 phút", "phút"),
                       [dk("dieu_kien_do", "sạc 80%", "sạc 80%")],
                       [tl(f"{WATCH}#009", gt("45", DONG_80, "phút"), [dk("dieu_kien_do", "Sạc lên đến 80%", DONG_80)])])
    assert x["bang_chung"][0]["dieu_kien"]["bo_tiep_hop"] == {"so": 20.0, "don_vi": "W"}
    assert x["bang_chung"][0]["nguon_dieu_kien"]["bo_tiep_hop"] == "bo_sung"
    assert ket(k) == ("LECH", "D4", "bo_dieu_kien")
    # tuyên bố nêu rõ củ sạc 20W thì khớp
    k, _ = sac_dong_ho("Apple Watch SE 3 sạc 80% trong khoảng 45 phút với củ sạc 20W", gt("45", "trong khoảng 45 phút", "phút"),
                       [dk("dieu_kien_do", "sạc 80%", "sạc 80%"), dk("phu_kien", "củ sạc 20W", "với củ sạc 20W")],
                       [tl(f"{WATCH}#009", gt("45", DONG_80, "phút"), [dk("dieu_kien_do", "Sạc lên đến 80%", DONG_80)])])
    assert ket(k)[:2] == ("DUNG", "D3")


def test_phu_kien_chu_thich_chi_dien_cho_muc_tai_lieu_va_khong_ghi_de():
    cf = CF["dong_ho"]
    van_ban = "Sạc lên đến 80% trong khoảng 45 phút\nThử với Bộ Tiếp Hợp Nguồn USB-C 20W của Apple"
    vung = tx.vung_do(van_ban, "Sạc lên đến 80%")
    muc = {"dieu_kien": {}, "xung_dot": {}, "nguon_dieu_kien": {}}
    tx._bo_sung_dieu_kien(muc, vung, "tai_lieu", 0, cf, "sac_nhanh", [], [], None, van_ban)
    assert muc["dieu_kien"]["bo_tiep_hop"] == {"so": 20.0, "don_vi": "W"}
    muc = {"dieu_kien": {}, "xung_dot": {}, "nguon_dieu_kien": {}}   # phía tuyên bố hoặc không có văn bản đoạn: không dò chú thích
    tx._bo_sung_dieu_kien(muc, vung, "tuyen_bo", None, cf, "sac_nhanh", [], [], None, None)
    assert "bo_tiep_hop" not in muc["dieu_kien"]
    muc = {"dieu_kien": {"bo_tiep_hop": {"so": 30.0, "don_vi": "W"}}, "xung_dot": {}, "nguon_dieu_kien": {}}   # LLM đã ghi thì giữ
    tx._bo_sung_dieu_kien(muc, vung, "tai_lieu", 0, cf, "sac_nhanh", [], [], None, van_ban)
    assert muc["dieu_kien"]["bo_tiep_hop"] == {"so": 30.0, "don_vi": "W"}


def test_dang_sac_nhanh_khong_dieu_kien_dung_don_vi():
    assert qd.dang_sac_nhanh({"dieu_kien": {}, "don_vi": "phut"}) == 1 and qd.dang_sac_nhanh({"dieu_kien": {}, "don_vi": "gio"}) == 2
    assert qd.dang_sac_nhanh({"dieu_kien": {"moc_phan_tram": {"so": 80, "don_vi": "phan_tram"}}, "don_vi": "gio"}) == 1
    assert qd.dang_sac_nhanh({"dieu_kien": {"so_phut_sac": {"so": 15, "don_vi": "phut"}}, "don_vi": "phut"}) == 2
    assert qd.dang_sac_nhanh({"dieu_kien": {"so_phut_sac": 1, "moc_phan_tram": 1}, "don_vi": "gio"}) == 2   # xung đột: theo đơn vị
    assert qd.dang_sac_nhanh({"dieu_kien": {}, "don_vi": None}) is None


def test_quy_doi_gio_phut_o_dieu_kien_so():
    tt = CF["dien_thoai"]["thuoc_tinh"]["khang_nuoc"]
    assert tx.dieu_kien_so_theo_don_vi(tt)["gio"] == "thoi_gian_ngam"
    chung = CF["dien_thoai"]["chung"]
    assert tx._so_dieu_kien("phut", ["ngâm trong 1,5 giờ"], "tối đa 30 phút", None, chung) == 90.0
    assert tx._so_dieu_kien("phut", ["ngâm tối đa 45 phút"], "tối đa 30 phút", None, chung) == 45.0
    assert tx._so_dieu_kien("phut", ["độ sâu 3 mét"], "tối đa 30 phút", None, chung) is None


# --- T-06 (phía P) ---

def test_p_loi_ky_thuat_ra_nhan_loi_json_hong_va_llm_loi():
    ban_ghi = {"id": "x", "ma_mau": BUDS, "chu_tuyen_bo": "Buds nghe nhạc 6 giờ", "loi": "llm_khong_tra_ve_dung: empty_blocked_or_incomplete_response",
               "tuyen_bo": None, "bang_chung": [], "tra_ve_tho": None, "neo_nguon": True, "kiem_day_du": True, "mo_hinh": "m", "k": 5,
               "cach_tach": "am_tiet"}
    for he in (False, True):
        kq = pp.kiem_chung_ban_ghi(ban_ghi, bo_doi_chieu=he)
        assert (kq["nhan"], kq["dong_d"]) == ("LOI", "LOI") and "Lỗi kỹ thuật" in kq["ly_do"]
    # JSON thô không đọc được: xu_ly_lai ghi loi, P ra LOI; JSON hợp lệ mà không trích được thì vẫn D1a
    hong = {**ban_ghi, "loi": None, "tra_ve_tho": "đây không phải JSON", "doan": [f"{BUDS}#044"]}
    kq = pp.kiem_chung_ban_ghi(tx.xu_ly_lai(hong))
    assert kq["nhan"] == "LOI"
    rong = {**ban_ghi, "loi": None, "tra_ve_tho": json.dumps({"tuyen_bo": {"san_pham": None, "thuoc_tinh": None, "gia_tri": None, "dieu_kien": []},
                                                              "bang_chung": []}), "doan": [f"{BUDS}#044"]}
    kq = pp.kiem_chung_ban_ghi(tx.xu_ly_lai(rong))
    assert (kq["nhan"], kq["dong_d"]) == ("CHUA_DU", "D1a") and kq["ghi_chu"] == ["chua_xac_dinh=trich_xuat_that_bai"]


def test_chay_p_thong_ke_dem_loi(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("chay_p", ROOT / "scripts/chay_p.py")
    chay_p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(chay_p)
    kq = [{"nhan": "LOI", "dong_d": "LOI", "loai": None, "ghi_chu": ["loi=x"], "vet": {}},
          {"nhan": "CHUA_DU", "dong_d": "D1a", "loai": None, "ghi_chu": ["chua_xac_dinh=trich_xuat_that_bai"], "vet": {}}]
    dong = "\n".join(chay_p.tao_thong_ke(kq, "P", "x.jsonl"))
    assert "- Số ca LOI (lỗi kỹ thuật gọi LLM hay JSON không đọc được, không phải nhãn): 1." in dong
    assert "- LOI: 1" in dong and "- CHUA_DU: 1" in dong


# --- T-09 ---

def test_don_vi_tuong_thich_voi_thuoc_tinh():
    assert not ch.don_vi_tuong_thich("m", "ma_ip") and not ch.don_vi_tuong_thich(None, "ma_ip") and not ch.don_vi_tuong_thich("phut", "ma_ip")
    assert ch.don_vi_tuong_thich("gio", "gio") and ch.don_vi_tuong_thich("phut", "gio") and ch.don_vi_tuong_thich("gio", "phut_hoac_gio")
    assert not ch.don_vi_tuong_thich("W", "gio") and not ch.don_vi_tuong_thich("phan_tram", "phut_hoac_gio")
    assert ch.don_vi_tuong_thich(None, "nit") and ch.don_vi_tuong_thich("nit", None)


def test_neo_nguon_bo_gia_tri_so_o_thuoc_tinh_ma_ip():
    chung = CF["dien_thoai"]["chung"]
    assert nn.kiem_gia_tri(gt("3", "độ sâu 3 mét", "mét"), chung, None, "khang_nuoc", "ma_ip") == nn.LY_DO_DON_VI
    assert nn.kiem_gia_tri(gt("30", "tối đa 30 phút", "phút"), chung, None, "khang_nuoc", "ma_ip") == nn.LY_DO_DON_VI
    assert isinstance(nn.kiem_gia_tri(gt("IP68", "IP68"), chung, None, "khang_nuoc", "ma_ip"), dict)
    assert isinstance(nn.kiem_gia_tri(gt("50", "sạc 50%", "%"), chung, "phan_tram", "do_sang", "nit"), str)   # % không phải nit
    assert isinstance(nn.kiem_gia_tri(gt("30", "dùng 30 giờ", "giờ"), chung, "gio", "thoi_luong_pin", "gio"), dict)


def test_cung_thuoc_tinh_loai_muc_khac_don_vi_cua_thuoc_tinh():
    bc = qd.BoiCanh({"ma_mau": XIAOMI, "tuyen_bo": {"thuoc_tinh": "khang_nuoc", "gia_tri": {"bui": 6, "nuoc": 8}}}, CF["dien_thoai"])

    def muc(g, dv):
        return {"thuoc_tinh": "khang_nuoc", "gia_tri": g, "don_vi": dv, "khac_san_pham": False, "san_pham_ma": XIAOMI}
    ban_ghi = {"bang_chung": [muc({"bui": 6, "nuoc": 8}, None), muc(3.0, "m"), muc(30.0, "phut"), muc("khong", None)]}
    assert [u["gia_tri"] for u in qd.cung_thuoc_tinh(ban_ghi, bc)] == [{"bui": 6, "nuoc": 8}, "khong"]


# --- T-10 ---

def test_neo_lai_gia_tri_tuyen_bo_khi_cau_trich_luoc_chu():
    chu = "Xiaomi 15T có tần số quét màn hình 120Hz"
    d = doan(XIAOMI, "004")
    k, x = chay(XIAOMI, chu, tb("tan_so_quet", gt("120", "tần số quét 120Hz", "Hz"), san_pham={"chu": "Xiaomi 15T", "trich": "Xiaomi 15T"}),
                [tl(f"{XIAOMI}#004", gt("120", "Tần số quét: Lên đến 120Hz"))], d)
    assert x["tuyen_bo"]["gia_tri"] == 120.0 and x["tuyen_bo"]["trich"]["gia_tri"] == "120Hz"
    neo = [b for b in x["bo_sung"] if b["phia"] == "tuyen_bo" and b["dieu_kien"] == "gia_tri"]
    assert neo == [{"phia": "tuyen_bo", "chi_so": None, "dieu_kien": "gia_tri", "gia_tri": 120.0, "cum": "120Hz"}]
    assert not [b for b in x["bi_loai"] if b["phia"] == "tuyen_bo" and b["truong"] == "gia_tri"]
    assert ket(k)[:2] == ("DUNG", "D3")


def test_khong_neo_lai_khi_so_khac_hoac_nhieu_gia_tri_hoac_ma_ip_hoac_p_nn():
    d = doan(XIAOMI, "004")
    for chu, so, ten in (("Xiaomi 15T có tần số quét màn hình 120Hz", "144", "so khác con số của tuyên bố"),
                         ("Xiaomi 15T quét 60Hz hoặc 120Hz màn hình", "120", "hai giá trị cùng đơn vị"),
                         ("Xiaomi 15T có tần số quét màn hình", "120", "không có con số trong chữ tuyên bố")):
        x = tx.xu_ly({"tuyen_bo": tb("tan_so_quet", gt(so, "tần số quét 120Hz", "Hz")), "bang_chung": []}, chu, d, XIAOMI, CF["dien_thoai"], TAT_CA)
        assert x["tuyen_bo"]["gia_tri"] is None, ten
    # mã IP không neo lại theo số
    x = tx.xu_ly({"tuyen_bo": tb("khang_nuoc", gt("IP68", "kháng IP68")), "bang_chung": []}, "Xiaomi 15T chống nước IP68", d, XIAOMI,
                 CF["dien_thoai"], TAT_CA)
    assert x["tuyen_bo"]["gia_tri"] is None
    # P−NN (kiem_day_du=False): không neo lại
    x = tx.xu_ly({"tuyen_bo": tb("tan_so_quet", gt("120", "tần số quét 120Hz", "Hz")), "bang_chung": []}, "Xiaomi 15T có tần số quét màn hình 120Hz",
                 d, XIAOMI, CF["dien_thoai"], TAT_CA, neo_nguon=False, kiem_day_du=False)
    assert x["bo_sung"] == []


# --- T-21 ---

def _bc_pin(gia_tri=6.0):
    return qd.BoiCanh({"ma_mau": "tn-b", "tuyen_bo": {"thuoc_tinh": "thoi_luong_pin", "gia_tri": gia_tri, "don_vi": "gio"}}, CF["tai_nghe"])


def _pin(gt_, dk_, ma, khac=None):
    return {"ma_doan": ma, "san_pham_ma": "tn-b", "khac_san_pham": False, "thuoc_tinh": "thoi_luong_pin", "gia_tri": gt_, "don_vi": "gio",
            "dieu_kien": dk_, "kieu_gia_tri": "khong_neu", "cum_kieu": None, "goi_muc_cao": False, "dieu_kien_khac": khac or [],
            "dieu_kien_phu": {}, "ngu_canh": [], "bo_qua": [], "xung_dot": {}, "trich": {"gia_tri": f"t {ma}"}, "nguon_dieu_kien": {}}


def test_lan_khong_khi_xung_dot_o_dieu_kien_da_biet():
    """Hai mục cùng 6 giờ: bật chống ồn (không ghi hoạt động) và tắt chống ồn + đàm thoại: hoat_dong không lan sang mục thứ nhất."""
    a = _pin(6.0, {"che_do_chong_on": "bat"}, "tn-b#1")
    b = _pin(6.0, {"che_do_chong_on": "tat", "hoat_dong": "dam_thoai"}, "tn-b#2")
    ds, vet = qd.lan_dieu_kien([a, b], _bc_pin())
    assert "hoat_dong" not in ds[0]["dieu_kien"] and vet == []
    # không xung đột (cùng chống ồn): vẫn lan như trước
    c = _pin(6.0, {"che_do_chong_on": "bat", "hoat_dong": "nghe_nhac"}, "tn-b#3")
    ds, vet = qd.lan_dieu_kien([a, c], _bc_pin())
    assert ds[0]["dieu_kien"]["hoat_dong"] == "nghe_nhac" and vet == [{"ma_doan": "tn-b#1", "dk": "hoat_dong", "gia_tri": "nghe_nhac"}]
    # câu "nghe nhạc 6 giờ khi bật chống ồn": Đúng, không bị phán Lệch vì hoat_dong dam_thoai lan sang
    tb_ = _pin(6.0, {"che_do_chong_on": "bat", "hoat_dong": "nghe_nhac"}, None)
    k = qd.quyet_dinh({"ma_mau": "tn-b", "chu_tuyen_bo": "x", "tuyen_bo": tb_, "bang_chung": [a, b], "loi": None}, CF["tai_nghe"])
    assert ket(k)[:2] == ("DUNG", "D3")


def test_khong_lan_cum_la_sang_muc_sach():
    la = [{"loai": "che_do_hoat_dong", "cum": "Gold Collection", "trich": "x"}]
    a, b = _pin(6.0, {}, "tn-b#1", khac=la), _pin(6.0, {}, "tn-b#2")
    ds, vet = qd.lan_dieu_kien([a, b], _bc_pin())
    assert ds[1]["dieu_kien_khac"] == [] and ds[0]["dieu_kien_khac"] == la and vet == []


# --- T-22 ---

def test_doc_so_khoang_va_huong():
    assert ch.doc_so("1-120") == 120.0 and ch.doc_so("1–144") == 144.0
    assert ch.doc_so("20-30", "thap_hon_tot_hon") == 20.0 and ch.doc_so("20-30", "cao_hon_tot_hon") == 30.0
    assert ch.doc_so("3.000") == 3000.0 and ch.doc_so("4,5") == 4.5
    with pytest.raises(ValueError):
        ch.doc_so("1-")


def test_gia_tri_khoang_o_tuyen_bo_khong_con_d1a_va_dung_voi_tai_lieu():
    chu = "Xiaomi 15T có tần số quét 1-120Hz"
    k, x = chay(XIAOMI, chu, tb("tan_so_quet", gt("1-120", "tần số quét 1-120Hz", "Hz"), san_pham={"chu": "Xiaomi 15T", "trich": "Xiaomi 15T"}),
                [tl(f"{XIAOMI}#004", gt("120", "Tần số quét: Lên đến 120Hz"))], doan(XIAOMI, "004"))
    assert x["tuyen_bo"]["gia_tri"] == 120.0 and ket(k)[:2] == ("DUNG", "D3")
    k, x = chay(XIAOMI, "Xiaomi 15T có tần số quét 1-144Hz", tb("tan_so_quet", gt("1-144", "tần số quét 1-144Hz", "Hz")),
                [tl(f"{XIAOMI}#004", gt("120", "Tần số quét: Lên đến 120Hz"))], doan(XIAOMI, "004"))
    assert ket(k)[:2] == ("SAI", "D5")


@pytest.mark.parametrize("cau,so,don_vi,khang_dinh", [
    ("iPhone 17 đảm bảo thời lượng xem video 30 giờ.", "30 giờ", "gio", True),
    ("Tai nghe B đảm bảo kết nối ổn định, nghe nhạc 8 giờ", "8 giờ", "gio", False),            # dấu phẩy: vế khác (HD mục 6.2)
    ("Tai nghe B đảm bảo kết nối ổn định và nghe nhạc 8 giờ", "8 giờ", "gio", False),          # từ nối mệnh đề
    ("Pin bảo đảm thời lượng xem video suốt 18 giờ", "18 giờ", "gio", True),
])
def test_tu_khang_dinh_cung_menh_de(cau, so, don_vi, khang_dinh):
    chung = CF["dien_thoai"]["chung"]
    g = next(x for x in ch.tim_gia_tri(cau, chung) if x.chu == so)
    assert (ch.tim_kieu_gia_tri(cau, g, chung).kieu == "khang_dinh") is khang_dinh


def test_d2_cho_tu_khang_dinh_xa_con_so():
    """T-22: "đảm bảo thời lượng xem video 30 giờ" so với "Lên đến 30 giờ" là D2 Lệch, không còn D3 Đúng (tăng FAR)."""
    chu = "iPhone 17 đảm bảo thời lượng xem video 30 giờ."
    k, _ = chay(IPHONE, chu, tb("thoi_luong_pin", gt("30", "xem video 30 giờ", "giờ"), [dk("che_do_hoat_dong", "xem video", "xem video 30 giờ")],
                                {"chu": "iPhone 17", "trich": "iPhone 17"}),
                [tl(f"{IPHONE}#016", gt("30", "Thời gian xem video\nLên đến 30 giờ"), [dk("che_do_hoat_dong", "Thời gian xem video")])],
                doan(IPHONE, "016"))
    assert ket(k) == ("LECH", "D2", "doi_kieu_gia_tri")


def test_thoa_dieu_kien_so_dung_sai_so_thuc():
    assert thoa_dieu_kien_so("tuyen_bo_nho_hon_hoac_bang", 30.3, 30.0, 0.01) is True
    assert thoa_dieu_kien_so("tuyen_bo_nho_hon_hoac_bang", 30.31, 30.0, 0.01) is False


def test_gia_tri_khac_nhau_khong_phu_thuoc_thu_tu():
    bc = qd.BoiCanh({"ma_mau": XIAOMI, "tuyen_bo": {"thuoc_tinh": "cong_suat_sac", "gia_tri": 100.0, "don_vi": "W"}}, CF["dien_thoai"])

    def muc(g):
        return {"thuoc_tinh": "cong_suat_sac", "gia_tri": g, "don_vi": "W", "ma_doan": f"x#{int(g)}"}
    for ds in ([100.0, 99.0], [99.0, 100.0]):
        assert len(qd.gia_tri_khac_nhau([muc(g) for g in ds], bc)) == 1
    assert qd.bang_doi_xung(muc(100.0), muc(99.0), bc) and qd.bang_doi_xung(muc(99.0), muc(100.0), bc)
    assert not qd.bang_doi_xung(muc(100.0), muc(90.0), bc)


# --- T-29 ---

def test_cach_sac_cung_loai_phu_kien_o_ca_hai_thuoc_tinh():
    tt = CF["dien_thoai"]["thuoc_tinh"]
    assert tt["sac_nhanh"]["dieu_kien_bat_buoc"]["cach_sac"] == "phu_kien" == tt["cong_suat_sac"]["dieu_kien_bat_buoc"]["cach_sac"]
    assert CF["dong_ho"]["thuoc_tinh"]["sac_nhanh"]["dieu_kien_bat_buoc"]["cap_sac"] == "phu_kien"


# --- T-30 ---

def test_xu_ly_lai_dien_thoi_gian_sinh_tu_cache(tmp_path):
    ma = "ab" * 32
    (tmp_path / f"{ma}.json").write_text(json.dumps({"status": "success", "result": {"generation_ms": 1234.5}}), encoding="utf-8")
    d = doan(BUDS, "044")
    gia_tri = {"tuyen_bo": tb("thoi_luong_pin", gt("6", "nghe nhạc 6 giờ", "giờ")), "bang_chung": []}
    ban_ghi = {"id": "x", "ma_mau": BUDS, "chu_tuyen_bo": "Galaxy Buds3 Pro nghe nhạc 6 giờ", "tra_ve_tho": json.dumps(gia_tri), "doan": [d[0][0]],
               "neo_nguon": True, "kiem_day_du": True, "loi": None, "ma_yeu_cau": ma, "thoi_gian_sinh_ms": None}
    moi = tx.xu_ly_lai(ban_ghi, thu_muc_cache=tmp_path)
    assert moi["thoi_gian_sinh_ms"] == 1234.5 and ban_ghi["thoi_gian_sinh_ms"] is None   # không sửa đầu vào
    assert tx.xu_ly_lai(ban_ghi)["thoi_gian_sinh_ms"] is None                          # không có thư mục cache thì giữ None
    assert tx.xu_ly_lai({**ban_ghi, "thoi_gian_sinh_ms": 7.0}, thu_muc_cache=tmp_path)["thoi_gian_sinh_ms"] == 7.0   # đã có thì không ghi đè


def test_trich_xuat_luu_thoi_gian_sinh_ms(tmp_path):
    from kiemchung.llm import LLMClient
    client = LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=tx.gia_transport)
    kq = tx.trich_xuat("Galaxy Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn", BUDS, client, "gemini-3.6-flash")
    assert isinstance(kq["thoi_gian_sinh_ms"], float) and kq["thoi_gian_sinh_ms"] >= 0 or kq["loi"]


# --- T-01 ---

def test_cum_cau_hinh_khop_khong_phu_thuoc_ngoac():
    # YAML ghi "(ngoài trời)", LLM trích "ngoài trời" và ngược lại "(tiêu chuẩn)"
    cf = CF["dien_thoai"]
    r = tx.hieu_dieu_kien([{"i": 0, "loai": "che_do_hoat_dong", "cum": "ngoài trời", "trich": "độ sáng đỉnh 3000 nit (ngoài trời)"},
                           {"i": 1, "loai": "che_do_hoat_dong", "cum": "(tiêu chuẩn)", "trich": "tối đa 1000 nit (tiêu chuẩn)"}], "do_sang", "tai_lieu", cf)
    assert r["dieu_kien"] == {"che_do_hien_thi": "ngoai_troi"} or r["xung_dot"] == {"che_do_hien_thi": ["ngoai_troi", "tieu_chuan"]}
    assert r["dieu_kien_khac"] == []


def test_cum_llm_rut_gon_khop_cum_cau_hinh_trong_cau_trich():
    tai_nghe = CF["tai_nghe"]
    cac = [{"i": 0, "loai": "che_do_hoat_dong", "cum": "ANC Tắt", "trich": "(Tính năng ANC Tắt)"},
           {"i": 1, "loai": "che_do_hoat_dong", "cum": "phát", "trich": "Thời gian phát"}]
    r = tx.hieu_dieu_kien(cac, "thoi_luong_pin", "tai_lieu", tai_nghe)
    assert r["dieu_kien"] == {"che_do_chong_on": "tat", "hoat_dong": "nghe_nhac"} and r["dieu_kien_khac"] == []
    # cụm rút gọn không nằm trong cụm cấu hình ở câu trích thì vẫn là cụm lạ
    r = tx.hieu_dieu_kien([{"i": 0, "loai": "che_do_hoat_dong", "cum": "chơi game", "trich": "Thời gian phát khi chơi game"}], "thoi_luong_pin", "tai_lieu", tai_nghe)
    assert [m["cum"] for m in r["dieu_kien_khac"]] == ["chơi game"]
    # cụm kiểu giá trị ("lên đến") không bị coi là cụm rút gọn của "Sạc lên đến 50%"
    dong = "Sạc lên đến 50% trong khoảng 20 phút với bộ tiếp hợp 40W trở lên"
    r = tx.hieu_dieu_kien([{"i": 0, "loai": "kieu_gia_tri", "cum": "lên đến", "trich": dong}], "sac_nhanh", "tai_lieu", CF["dien_thoai"])
    assert r["cum_kieu"] == [(0, "lên đến")] and r["dieu_kien"] == {}


@pytest.mark.parametrize("cum,trich,la_tieu_de", [
    ("Màn hình", "Màn hình", True), ("Kháng Bụi & Nước", "Kháng Bụi & Nước", True), ("Pin", "Pin Xiaomi Surge 5500mAh", True),
    ("Nguồn Điện Và Thời Lượng Pin", "Nguồn Điện Và Thời Lượng Pin", True), ("Thời lượng pin hàng đầu", "Thời lượng pin hàng đầu", True),
    ("Sạc nhanh HyperCharge", "Sạc nhanh HyperCharge 67W", True), ("Công nghệ ProMotion", "Công nghệ ProMotion với tốc độ", True),
    ("HyperCharge", "sạc HyperCharge", True), ("Gold Collection", "Gold Collection", True), ("Dynamic Island", "Dynamic Island", True), ("Màn hình Luôn Bật", "Màn hình Luôn Bật", True),
    ("Nâng tầm khả năng hiển thị", "Nâng tầm khả năng hiển thị", True),
    ("chế độ chơi game", "chế độ chơi game", False), ("khi bơi", "chống nước khi bơi", False), ("Chơi Game", "Thời gian phát khi Chơi Game", False),
    ("Màn hình 6.83\" bảo vệ mắt", "Màn hình 6.83\" bảo vệ mắt", False),   # có con số
    ("Bộ sạc không bao gồm trong hộp", "Bộ sạc không bao gồm trong hộp.", False),
])
def test_tieu_de_khong_la_dieu_kien_la(cum, trich, la_tieu_de):
    assert tx._la_tieu_de(cum, trich, CF["dien_thoai"]["chung"]) is la_tieu_de


def test_tieu_de_vao_bo_qua_khong_vao_dieu_kien_khac():
    cf = CF["dien_thoai"]
    r = tx.hieu_dieu_kien([{"i": 0, "loai": "bo_phan", "cum": "Màn hình", "trich": "Màn hình"},
                           {"i": 1, "loai": "che_do_hoat_dong", "cum": "chế độ chơi game", "trich": "chế độ chơi game"}], "tan_so_quet", "tai_lieu", cf)
    assert r["bo_qua"] == ["Màn hình"] and [m["cum"] for m in r["dieu_kien_khac"]] == ["chế độ chơi game"]


def test_vung_do_lay_tieu_de_nhom_va_chu_thich_dong_sau():
    nguon = "Pin Và Nguồn Điện\nThời gian xem video\nLên đến 30 giờ\nThời gian xem video (trực tuyến)\nLên đến 27 giờ\nTích hợp pin"
    khong_cum = lambda t: "xem video" not in t.lower()   # dòng không tự nêu điều kiện
    v = tx.vung_do(nguon, "Lên đến 27 giờ", can_tieu_de=lambda t: True)
    assert v.text == "Thời gian xem video (trực tuyến) Lên đến 27 giờ" and v.nhan == "Thời gian xem video (trực tuyến) Lên đến 27 giờ"
    assert tx.vung_do(nguon, "Lên đến 30 giờ", can_tieu_de=lambda t: True).nhan == "Thời gian xem video Lên đến 30 giờ"
    assert tx.vung_do(nguon, "Lên đến 30 giờ").text == "Lên đến 30 giờ"     # mặc định không lấy tiêu đề
    assert khong_cum("Lên đến 30 giờ") and not khong_cum("Thời gian xem video Lên đến 30 giờ")
    # dòng "(…)" phía trên là chú thích của giá trị trước, không phải tiêu đề; dòng "(…)" liền sau là của dòng này
    bang = "Thời Gian Phát\nĐến 7,0/30 giờ\n(Tính năng ANC Tắt)\nĐến 6,0/26 giờ\n(Tính năng ANC Bật)"
    v = tx.vung_do(bang, "Đến 6,0/26 giờ", can_tieu_de=lambda t: True)
    assert v.text == "Đến 6,0/26 giờ (Tính năng ANC Bật)"
    v = tx.vung_do(bang, "Đến 7,0/30 giờ", can_tieu_de=lambda t: True)
    assert v.text == "Thời Gian Phát Đến 7,0/30 giờ (Tính năng ANC Tắt)"


def test_vung_do_chi_lay_ve_chua_con_so_khi_dong_liet_ke_nhieu_gia_tri():
    nguon = "Độ sáng tối đa 1000 nit (tiêu chuẩn); độ sáng đỉnh 1600 nit (HDR); độ sáng đỉnh 3000 nit (ngoài trời)"
    v = tx.vung_do(nguon, nguon, 1600.0)
    assert v.text == "độ sáng đỉnh 1600 nit (HDR)"
    assert tx.vung_do(nguon, nguon).text == nguon      # không có so thì giữ nguyên cả dòng


def test_xung_dot_kieu_gia_tri_khong_la_xung_dot_dieu_kien():
    cf = CF["dien_thoai"]
    r = tx.hieu_dieu_kien([{"i": 0, "loai": "kieu_gia_tri", "cum": "tốc độ làm mới thích ứng", "trich": "ProMotion với tốc độ làm mới thích ứng lên đến 120Hz"},
                           {"i": 1, "loai": "kieu_gia_tri", "cum": "Lên đến 120Hz", "trich": "ProMotion với tốc độ làm mới thích ứng lên đến 120Hz"}],
                          "tan_so_quet", "tai_lieu", cf)
    assert r["xung_dot"] == {}


def _muc_bang(ma_doan, gia_tri, trich):
    return {"ma_doan": ma_doan, "san_pham_ma": "tn-b", "khac_san_pham": False, "thuoc_tinh": "khang_nuoc", "gia_tri": gia_tri, "don_vi": None,
            "dieu_kien": {}, "kieu_gia_tri": None, "cum_kieu": None, "goi_muc_cao": False, "dieu_kien_khac": [], "dieu_kien_phu": {}, "ngu_canh": [],
            "bo_qua": [], "xung_dot": {}, "trich": {"gia_tri": trich}, "nguon_dieu_kien": {}}


def test_bang_so_sanh_nhieu_mau_khong_ket_luan_mau_thuan():
    ip57, ipx2 = {"bui": 5, "nuoc": 7}, {"bui": None, "nuoc": 2}
    tb_ = _muc_bang(None, ip57, "IP57")
    ban_ghi = {"ma_mau": "tn-b", "chu_tuyen_bo": "x", "tuyen_bo": tb_, "loi": None,
               "bang_chung": [_muc_bang("tn-b#41", ip57, "IP57"), _muc_bang("tn-b#41", ipx2, "IPX2"), _muc_bang("tn-b#39", ip57, "IP57")]}
    k = qd.quyet_dinh(ban_ghi, CF["tai_nghe"])
    assert ket(k)[:2] == ("DUNG", "D3") and k["vet"]["bang_nhieu_cot"] == ["tn-b#41"] and k["bang_chung"] == ["tn-b#39"]
    # hai dòng cùng nhãn có chữ trong một bảng thông số (#044 "Tổng ... Lên đến 26" và "... Lên đến 30"): vẫn là tài liệu mâu thuẫn (V48)
    def pin(g, ma):
        return {**_muc_bang(ma, g, f"Tổng thời gian phát nhạc (Giờ, bật ANC) Lên đến {g:g}"), "thuoc_tinh": "thoi_luong_pin", "don_vi": "gio",
                "dieu_kien": {"bo_phan": "kem_hop_sac", "che_do_chong_on": "bat", "hoat_dong": "nghe_nhac"}}
    tb2 = {**pin(30.0, None), "dieu_kien": {"bo_phan": "kem_hop_sac", "che_do_chong_on": "bat", "hoat_dong": "nghe_nhac"}}
    k = qd.quyet_dinh({"ma_mau": "tn-b", "chu_tuyen_bo": "x", "tuyen_bo": tb2, "loi": None, "bang_chung": [pin(26.0, "tn-b#44"), pin(30.0, "tn-b#44")]},
                      CF["tai_nghe"])
    assert ket(k)[:2] == ("CHUA_DU", "D1b")
    # ba cột cùng nhãn, ba giá trị khác nhau trong một đoạn: không đủ căn cứ, mục bị loại khỏi bằng chứng
    k = qd.quyet_dinh({"ma_mau": "tn-b", "chu_tuyen_bo": "x", "tuyen_bo": tb2,
                       "bang_chung": [pin(26.0, "tn-b#42"), pin(24.0, "tn-b#42"), pin(21.0, "tn-b#42")], "loi": None}, CF["tai_nghe"])
    assert ket(k)[:2] == ("CHUA_DU", "D1") and k["vet"]["bang_nhieu_cot"] == ["tn-b#42"]


def test_dai_luong_khac_do_sang_toi_thieu_khong_la_bang_chung():
    d = doan(WATCH, "007")
    chu = "Apple Watch SE 3 có độ sáng màn hình 1000 nit"
    k, x = chay(WATCH, chu, tb("do_sang", gt("1000", "độ sáng 1000 nit", "nit"), san_pham={"chu": "Apple Watch SE 3", "trich": "Apple Watch SE 3"}),
                [tl(f"{WATCH}#007", gt("1000", "Độ sáng đỉnh 1000 nit")), tl(f"{WATCH}#007", gt("2", "Độ sáng tối thiểu 2 nit"))], d)
    assert [m["gia_tri"] for m in x["bang_chung"]] == [1000.0]
    assert x["bang_chung_bi_loai"][0]["ly_do"] == ["dai_luong_khac"] and ket(k)[:2] == ("DUNG", "D3")


def test_phu_dinh_khong_duoc_dam_bao_khong_phai_khong_khang_nuoc():
    chung = CF["tai_nghe"]["chung"]
    gia_tri = gt("không", "Nếu tai nghe bị hỏng, chúng không được đảm bảo khả năng kháng nước.")
    assert nn.kiem_gia_tri(gia_tri, chung, None, "khang_nuoc", "ma_ip") == nn.LY_DO_MA
    thuc = nn.kiem_gia_tri(gt("không", "Hộp sạc không có khả năng kháng nước."), chung, None, "khang_nuoc", "ma_ip")
    assert thuc == {"gia_tri": "khong", "khoa_don_vi": None}


# --- T-23: bản ghi thật của tập chính, từ tra_ve_tho qua xu_ly_lai rồi quyết định ---

@pytest.fixture(scope="module")
def chinh():
    if not (CHINH_TRICH_XUAT.exists() and CHINH_NHAN.exists()):
        pytest.skip("không có kết quả trích xuất hay nhãn của tập chính")
    ban_ghi = {r["id"]: r for r in map(json.loads, CHINH_TRICH_XUAT.read_text(encoding="utf-8").splitlines())}
    nhan = {r["id"]: r for r in map(json.loads, CHINH_NHAN.read_text(encoding="utf-8").splitlines())}
    return ban_ghi, nhan


def p_tu_ban_ghi_that(chinh, ma, **kw):
    return pp.kiem_chung_ban_ghi(tx.xu_ly_lai(chinh[0][ma], **kw))


def test_tb_00107_ip68_khong_con_d1b_vi_3m_va_30_phut(chinh):
    goc = pp.kiem_chung_ban_ghi(chinh[0]["tb-00107"])   # bản ghi lưu sẵn (trước các sửa này nếu cache cũ)
    kq = p_tu_ban_ghi_that(chinh, "tb-00107")
    assert (kq["nhan"], kq["dong_d"]) == (chinh[1]["tb-00107"]["nhan"], chinh[1]["tb-00107"]["dong_d"]) == ("DUNG", "D3")
    assert goc["he"] == "P"


@pytest.mark.parametrize("ma", ["tb-00081", "tb-00088", "tb-00096", "tb-00103"])
def test_tan_so_quet_120hz_khong_con_trich_xuat_that_bai(chinh, ma):
    x = tx.xu_ly_lai(chinh[0][ma])
    assert x["tuyen_bo"]["gia_tri"] == 120.0 and any(b["phia"] == "tuyen_bo" and b["dieu_kien"] == "gia_tri" for b in x["bo_sung"])
    kq = pp.kiem_chung_ban_ghi(x)
    assert (kq["nhan"], kq["dong_d"]) == ("DUNG", "D3") and chinh[1][ma]["nhan"] == "DUNG"


@pytest.mark.parametrize("ma", ["tb-00067", "tb-00084", "tb-00090", "tb-00094", "tb-00098", "tb-00101", "tb-00106"])
def test_ban_ghi_that_chinh_khop_nhan_chuan(chinh, ma):
    kq = p_tu_ban_ghi_that(chinh, ma)
    chuan = chinh[1][ma]
    assert (kq["nhan"], kq["dong_d"]) == (chuan["nhan"], chuan["dong_d"])


def test_xu_ly_lai_p_nn_dung_cung_tra_ve_tho(chinh):
    x = tx.xu_ly_lai(chinh[0]["tb-00081"], neo_nguon=False, kiem_day_du=False)
    assert (x["neo_nguon"], x["kiem_day_du"]) == (False, False) and pp.kiem_chung_ban_ghi(x)["he"] == "P-NN"
    assert x["tra_ve_tho"] == chinh[0]["tb-00081"]["tra_ve_tho"]


def test_xu_ly_lai_tat_dinh_va_khong_sua_dau_vao(chinh):
    goc = copy.deepcopy(chinh[0]["tb-00067"])
    a, b = tx.xu_ly_lai(chinh[0]["tb-00067"]), tx.xu_ly_lai(chinh[0]["tb-00067"])
    assert a == b and chinh[0]["tb-00067"] == goc
