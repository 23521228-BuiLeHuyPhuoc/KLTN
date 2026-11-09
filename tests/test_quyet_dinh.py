"""Test bộ quyết định A–D và sinh lý do (Bước 27, T5.5, T5.6, T5.8, T5.9).

Ca "dựng tay": tests/du_lieu/vi_du_huong_dan.json, 51 ví dụ V01–V51 của hướng dẫn mục 9, mỗi ví dụ một bản ghi trích xuất theo
định dạng Bước 22 (mục 8) với câu trích chép từ doan.jsonl của 4 mẫu tập phát triển. Ca "tự đặt" dùng sản phẩm giả (Tai nghe B, Điện
thoại A) hoặc 4 mẫu phát triển. Không mở dữ liệu của tập kiểm tra, không gọi LLM.
"""
import copy
import importlib.util
import json
from pathlib import Path
import re
import unicodedata

import pytest

from kiemchung import ly_do as ld
from kiemchung import quyet_dinh as qd
from kiemchung.cau_hinh import doc_cau_hinh
from kiemchung.chuan_hoa import tim_gia_tri, tim_kieu_gia_tri

GOC = Path(__file__).resolve().parents[1]
CF = {n: doc_cau_hinh(n) for n in ("dien_thoai", "tai_nghe", "dong_ho")}
NHOM = {"dt": "dien_thoai", "tn": "tai_nghe", "dh": "dong_ho"}
VI_DU = json.loads((GOC / "tests" / "du_lieu" / "vi_du_huong_dan.json").read_text(encoding="utf-8"))
NHAN = {"Đúng": "DUNG", "Sai": "SAI", "Lệch": "LECH", "Chưa đủ thông tin": "CHUA_DU"}
MAU_CAU = {"D1": "Tài liệu của ", "D1a": "Chưa xác định được điều kiện của tuyên bố: “", "D1b": "Tài liệu ghi hai giá trị khác nhau cho ",
           "D2": "Tài liệu ghi mức tối đa: “", "D3": "Khớp với tài liệu: “", "D4": "Giá trị ", "D5": "Tài liệu ghi ", "D6": "Tài liệu không công bố "}
NHAN_CUA_DONG = {"D1": "CHUA_DU", "D1a": "CHUA_DU", "D1b": "CHUA_DU", "D6": "CHUA_DU", "D2": "LECH", "D4": "LECH", "D3": "DUNG", "D5": "SAI"}


def chay_vi_du(r, **kw):
    return qd.quyet_dinh(copy.deepcopy(r["ban_ghi"]), CF[NHOM[r["ma_mau"][:2]]], **kw)


# --- Dựng ca tự đặt ---

def muc(tt, gt, dv=None, dk=None, kieu="khong_neu", ck=None, ma="tn-b#001", trich=None, khac=None, goi=False, khac_sp=False, xd=None,
        mau="tn-b"):
    return {"ma_doan": ma, "san_pham_ma": None if khac_sp else mau, "khac_san_pham": khac_sp, "thuoc_tinh": tt, "gia_tri": gt, "don_vi": dv,
            "dieu_kien": dk or {}, "kieu_gia_tri": kieu, "cum_kieu": ck, "goi_muc_cao": goi, "dieu_kien_khac": khac or [],
            "dieu_kien_phu": {}, "ngu_canh": [], "bo_qua": [], "xung_dot": xd or {}, "trich": {"gia_tri": trich or f"trích {ma} {gt}"},
            "nguon_dieu_kien": {}}


def chay(nhom, chu, tb, bang_chung, mau="tn-b", **kw):
    ban_ghi = {"ma_mau": mau, "chu_tuyen_bo": chu, "tuyen_bo": tb, "bang_chung": bang_chung, "loi": None}
    return qd.quyet_dinh(ban_ghi, CF[nhom], **kw)


def pin(gt, dk=None, **kw):
    """Mục thời lượng pin của Tai nghe B (giờ)."""
    return muc("thoi_luong_pin", gt, "gio", dk, **kw)


def tn_dk(cd="bat", bp="tai_nghe", hd="nghe_nhac"):
    return {"che_do_chong_on": cd, "bo_phan": bp, "hoat_dong": hd}


def pin_tb(gt, dk=None, **kw):
    return pin(gt, dk, ma=None, **kw)


def hai_gia_tri():
    """Tai nghe B nghe nhạc bật chống ồn: 9 giờ ở tai nghe (tắt ANC), 7 giờ (bật ANC), cùng chống ồn để thử D1b: xem từng ca."""
    return [pin(9.0, tn_dk(), ma="tn-b#001", ck="lên đến", kieu="toi_da"), pin(7.0, tn_dk(), ma="tn-b#002", ck="lên đến", kieu="toi_da")]


def kho_tai_nghe_b():
    return [pin(9.0, tn_dk("tat"), ma="tn-b#003", ck="đến", kieu="toi_da"), pin(7.0, tn_dk("bat"), ma="tn-b#003", ck="đến", kieu="toi_da"),
            pin(30.0, tn_dk("tat", "kem_hop_sac"), ma="tn-b#003", ck="đến", kieu="toi_da"),
            pin(24.0, tn_dk("bat", "kem_hop_sac"), ma="tn-b#003", ck="đến", kieu="toi_da"),
            pin(6.0, tn_dk("tat", "tai_nghe", "dam_thoai"), ma="tn-b#010", ck="lên đến", kieu="toi_da")]


def tb_nghe_nhac(gt, **kw):
    dk = {"hoat_dong": "nghe_nhac"}
    dk.update(kw.pop("dk", {}))
    return pin_tb(gt, dk, **kw)


def ket(k):
    return (k["nhan"], k["dong_d"], k["loai"])


# --- Cấu trúc và cấu hình ---

def test_khoa_chep_nhan_trong_chung_yaml():
    assert CF["tai_nghe"]["chung"]["chep_nhan"]["bo_chu_dau"] == ["thời gian", "thời lượng"]


def test_cum_phu_giong_ra_tach():
    spec = importlib.util.spec_from_file_location("ra_tach", GOC / "scripts/ra_tach.py")
    rt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rt)
    assert qd.CUM_PHU == rt.CUM_PHU
    assert list(qd.CUM_PHU) == CF["tai_nghe"]["chung"]["cum_phu"]["mau"]


def test_dau_ra_du_truong():
    k = chay("tai_nghe", "Tai nghe B nghe nhạc 6 giờ", tb_nghe_nhac(6.0), kho_tai_nghe_b())
    assert set(k) == {"nhan", "dong_d", "loai", "bang_chung", "trich", "ly_do", "ghi_chu", "tai_lieu_mau_thuan", "vet"}
    assert isinstance(k["ghi_chu"], list) and k["tai_lieu_mau_thuan"] is False
    json.dumps(k, ensure_ascii=False)   # vết phải ghi ra JSON được


# --- Hồi quy 51 ví dụ ---

def test_du_51_vi_du():
    assert [r["id"] for r in VI_DU] == [f"V{i:02d}" for i in range(1, 52)]


@pytest.mark.parametrize("r", VI_DU, ids=lambda r: r["id"])
def test_hoi_quy_vi_du(r):
    k = chay_vi_du(r)
    mong = r.get("p_du_kien") or {"nhan": r["nhan"], "dong_d": r["dong_d"], "loai": r["loai"]}
    assert ket(k) == (mong["nhan"], mong["dong_d"], mong["loai"]), k["ly_do"]
    assert k["tai_lieu_mau_thuan"] == (k["dong_d"] == "D1b")


def test_vi_du_p_khac_nhan_chuan_co_ly_do():
    khac = [r for r in VI_DU if "p_du_kien" in r]
    for r in khac:   # ví dụ mà P ra khác nhãn chuẩn phải ghi lý do (giới hạn bao phủ)
        assert r["ly_do_khac"] and (r["p_du_kien"]["nhan"], r["p_du_kien"]["dong_d"]) != (r["nhan"], r["dong_d"])
    assert khac == []   # sau luật lan điều kiện, cả 51 ví dụ ra đúng nhãn chuẩn (V23, V27 trước đó ra Đúng)
    assert sum((r["nhan"], r["dong_d"], r["loai"]) == ket(chay_vi_du(r)) for r in VI_DU) == 51


def test_v23_v27_ra_dung_nho_luat_lan():
    for i in ("V23", "V27"):
        r = next(v for v in VI_DU if v["id"] == i)
        k = chay_vi_du(r)
        assert ket(k) == ("LECH", "D4", r["loai"]) and k["vet"]["lan"], i
    r = next(v for v in VI_DU if v["id"] == "V23")
    assert any(u["ma_doan"] == "dt-xiaomi-15t#005" for u in r["ban_ghi"]["bang_chung"])


def _gop(chu):
    return unicodedata.normalize("NFC", " ".join(chu.split()))


def _tieu_de_huong_dan():
    huong = (GOC / "data" / "huong_dan_gan_nhan.md").read_text(encoding="utf-8")
    tieu = {}
    for m in re.finditer(r"^\*\*(V\d+) · ([^·(]+?)(?: \(`(\w+)`\))? · (D\w+)[^*]*\*\*\s*(.*)$", huong, re.M):
        tieu[m.group(1)] = (NHAN[m.group(2).strip()], m.group(4), m.group(3), m.group(5).strip())
    return tieu


def test_nhan_dong_loai_trung_tieu_de_huong_dan():
    tieu = _tieu_de_huong_dan()
    assert len(tieu) == 51
    for r in VI_DU:
        nhan, dong, loai, chu = tieu[r["id"]]
        assert (r["nhan"], r["dong_d"], r["loai"]) == (nhan, dong, loai), r["id"]
        assert r["chu_tuyen_bo"] == chu == r["ban_ghi"]["chu_tuyen_bo"], r["id"]


def _doan(ma_mau):
    van = {}
    with open(GOC / "data" / "nguon" / ma_mau / "doan.jsonl", encoding="utf-8") as f:
        for dong in f:
            d = json.loads(dong)
            van[d["id"]] = _gop(" ".join([d["noi_dung"], *d["chu_thich"]]))
    return van


def test_cau_trich_la_chuoi_con_cua_nguon():
    mau_phat_trien = {"dt-apple-iphone17", "dt-xiaomi-15t", "tn-samsung-buds3pro", "dh-apple-watchse3"}
    kho = {m: _doan(m) for m in mau_phat_trien}
    for r in VI_DU:
        assert r["ma_mau"] in mau_phat_trien
        bg = r["ban_ghi"]
        for t in bg["tuyen_bo"]["trich"].values():
            assert _gop(t) in _gop(bg["chu_tuyen_bo"]), (r["id"], t)
        for u in bg["bang_chung"]:
            van = kho[r["ma_mau"]][u["ma_doan"]]
            for khoa, t in u["trich"].items():
                assert _gop(t) in van, (r["id"], u["ma_doan"], khoa, t)


# --- D1 ---

def test_d1_khong_co_muc_nao():
    k = chay("tai_nghe", "Tai nghe B sạc nhanh 5 phút nghe 1 giờ", muc("sac_nhanh", 1.0, "gio", {"so_phut_sac": {"so": 5, "don_vi": "phut"}}, ma=None), [])
    assert ket(k) == ("CHUA_DU", "D1", None) and k["bang_chung"] == [] and k["ghi_chu"] == []


def test_d1_chi_co_thuoc_tinh_khac_hoac_san_pham_khac():
    tb = tb_nghe_nhac(6.0)
    assert chay("tai_nghe", "x", tb, [muc("dung_luong_pin", 515.0, "mAh")])["dong_d"] == "D1"
    k = chay("tai_nghe", "x", tb, [pin(6.0, tn_dk(), khac_sp=True)])   # giá trị của cột sản phẩm khác
    assert k["dong_d"] == "D1"


def test_d1_tuyen_bo_goi_san_pham_khac_mau():
    buds = "tn-samsung-buds3pro"
    kho = [{**u, "san_pham_ma": buds} for u in kho_tai_nghe_b()]
    tb = tb_nghe_nhac(6.0)
    tb["san_pham_ma"] = "tn-apple-airpodspro3"
    k = chay("tai_nghe", "AirPods Pro 3 nghe nhạc 6 giờ", tb, kho, mau=buds)
    assert k["dong_d"] == "D1"
    tb2 = tb_nghe_nhac(6.0)   # tên khớp khong_nham_voi (san_pham_ma None của Bước 22)
    k2 = chay("tai_nghe", "Galaxy Buds FE nghe nhạc 6 giờ", tb2, kho, mau=buds)
    assert k2["dong_d"] == "D1"
    assert chay("tai_nghe", "Galaxy Buds3 Pro nghe nhạc 6 giờ", {**tb2, "san_pham_ma": buds}, kho, mau=buds)["dong_d"] != "D1"


def test_d1_sac_nhanh_dong_ho_chi_so_trong_cung_dang():
    cap = {"so_phut_sac": {"so": 15, "don_vi": "phut"}, "hoat_dong": "su_dung_binh_thuong"}
    dang2 = muc("sac_nhanh", 8.0, "gio", cap, mau="dh-a", ma="dh-a#009", kieu="toi_da", ck="lên đến")
    tb1 = muc("sac_nhanh", 45.0, "phut", {"moc_phan_tram": {"so": 80, "don_vi": "phan_tram"}}, ma=None, mau="dh-a")
    assert chay("dong_ho", "x", tb1, [dang2], mau="dh-a")["dong_d"] == "D1"   # dạng 1 mà chỉ có mục dạng 2
    tb2 = muc("sac_nhanh", 8.0, "gio", {"so_phut_sac": {"so": 15, "don_vi": "phut"}}, ma=None, mau="dh-a")
    assert ket(chay("dong_ho", "Đồng hồ A sạc 15 phút dùng 8 giờ", tb2, [dang2], mau="dh-a")) == ("DUNG", "D3", None)
    tb3 = muc("sac_nhanh", 8.0, "gio", {"so_phut_sac": {"so": 10, "don_vi": "phut"}}, ma=None, mau="dh-a")   # 10 < 15: khác điều kiện
    assert chay("dong_ho", "x", tb3, [dang2], mau="dh-a")["dong_d"] in ("D4", "D5", "D6")


# --- D1a ---

def test_d1a_trich_xuat_that_bai():
    cf = CF["tai_nghe"]
    for ban_ghi in ({"ma_mau": "tn-b", "loi": "json_hong", "tuyen_bo": None, "bang_chung": []},
                    {"ma_mau": "tn-b", "loi": None, "tuyen_bo": muc("thoi_luong_pin", None, "gio", ma=None), "bang_chung": []},
                    {"ma_mau": "tn-b", "loi": None, "tuyen_bo": {**muc("thoi_luong_pin", 6.0, "gio", ma=None), "thuoc_tinh": None}, "bang_chung": []}):
        k = qd.quyet_dinh(ban_ghi, cf)
        assert ket(k) == ("CHUA_DU", "D1a", None) and k["ghi_chu"] == ["chua_xac_dinh=trich_xuat_that_bai"]
        assert k["ly_do"].startswith(MAU_CAU["D1a"])
    k = qd.quyet_dinh({"ma_mau": "tn-b", "loi": "x", "tuyen_bo": None, "bang_chung": []}, cf, doi_chieu=False)
    assert k["dong_d"] == "D1a"   # P−ĐK vẫn D1a khi trích xuất thất bại


def test_d1a_ba_loi_vao():
    # (1) khóa không có mặc định: mốc phần trăm của sạc nhanh điện thoại
    sac = muc("sac_nhanh", 20.0, "phut", {"moc_phan_tram": {"so": 50, "don_vi": "phan_tram"}, "bo_tiep_hop": {"so": 40, "don_vi": "W"}}, mau="dt-a", ma="dt-a#1")
    tb = muc("sac_nhanh", 20.0, "phut", {"bo_tiep_hop": {"so": 40, "don_vi": "W"}}, ma=None, mau="dt-a")
    k = chay("dien_thoai", "Điện thoại A sạc 20 phút với bộ sạc 40W", tb, [sac], mau="dt-a")
    assert ket(k) == ("CHUA_DU", "D1a", None) and "mac_dinh=moc_phan_tram" in k["ghi_chu"]
    # (2) chữ gọi mức cao trỏ nhiều chế độ: "đỉnh" của Apple
    ds = [muc("do_sang", 1000.0, "nit", {"che_do_hien_thi": "tieu_chuan"}, mau="dt-apple-iphone17", ma="dt-apple-iphone17#5"),
          muc("do_sang", 1600.0, "nit", {"che_do_hien_thi": "hdr"}, mau="dt-apple-iphone17", ma="dt-apple-iphone17#5"),
          muc("do_sang", 3000.0, "nit", {"che_do_hien_thi": "ngoai_troi"}, mau="dt-apple-iphone17", ma="dt-apple-iphone17#5")]
    tb = muc("do_sang", 3000.0, "nit", ma=None, mau="dt-apple-iphone17", kieu="toi_da", ck="đỉnh", goi=True)
    k = chay("dien_thoai", "iPhone 17 có độ sáng đỉnh 3000 nit", tb, ds, mau="dt-apple-iphone17")
    assert ket(k) == ("CHUA_DU", "D1a", None) and k["ghi_chu"][0] == "chua_xac_dinh=đỉnh"
    # (3) cụm điều kiện không giải được ở tuyên bố
    tb = tb_nghe_nhac(6.0)
    tb["dieu_kien_khac"] = [{"loai": "che_do_hoat_dong", "cum": "chế độ chơi game", "trich": "chế độ chơi game"}]
    k = chay("tai_nghe", "Tai nghe B nghe nhạc 6 giờ ở chế độ chơi game", tb, kho_tai_nghe_b())
    assert ket(k) == ("CHUA_DU", "D1a", None) and k["ghi_chu"][0] == "chua_xac_dinh=chế độ chơi game"
    assert k["ly_do"] == "Chưa xác định được điều kiện của tuyên bố: “chế độ chơi game”."


def test_d1a_xung_dot_va_khong_dao_chieu_voi_so_thang():
    tb = tb_nghe_nhac(6.0)
    tb["xung_dot"] = {"che_do_chong_on": ["bat", "tat"]}
    assert chay("tai_nghe", "x", tb, kho_tai_nghe_b())["dong_d"] == "D1a"
    # một con số không điều kiện: so thẳng, không dừng ở D1a vì độ sáng không có mặc định
    tl = muc("do_sang", 1000.0, "nit", mau="dh-a", ma="dh-a#7", kieu="toi_da", ck="đỉnh", goi=True)
    tb = muc("do_sang", 1000.0, "nit", ma=None, mau="dh-a")
    k = chay("dong_ho", "Đồng hồ A sáng 1000 nit", tb, [tl], mau="dh-a")
    assert ket(k) == ("DUNG", "D3", None) and k["vet"]["so_thang"] and k["ly_do"].endswith("Tài liệu không nêu điều kiện.")
    tl2 = muc("do_sang", 1000.0, "nit", {"dien_tich_do": {"so": 25, "don_vi": "phan_tram"}}, mau="dt-a", ma="dt-a#7")
    tb = muc("do_sang", 1000.0, "nit", ma=None, mau="dt-a")
    assert chay("dien_thoai", "x", tb, [tl2], mau="dt-a")["dong_d"] == "D1a"   # có điều kiện: không so thẳng


# --- Luật chặn điều kiện lạ ---

LA = [{"loai": "che_do_hoat_dong", "cum": "chế độ chơi game", "trich": "x"}]


def tl_game(gt, cum, ma):
    return pin(gt, tn_dk(), ma=ma, ck="đến", kieu="toi_da", khac=[{"loai": "che_do_hoat_dong", "cum": cum, "trich": "x"}])


def test_luat_chan_tinh_huong_1_hai_gia_tri_khac_nhau_o_dieu_kien_la():
    kho = [tl_game(10.0, "tắt chế độ chơi game", "tn-b#1"), tl_game(8.0, "bật chế độ chơi game", "tn-b#2")]
    for gt in (10.0, 8.0):   # luật chung tắt: D1a, không D1b và không Đúng
        k = chay("tai_nghe", "x", tb_nghe_nhac(gt), kho, luat_chung_cho_nhieu_gia_tri=False)
        assert ket(k) == ("CHUA_DU", "D1a", None)
        assert k["ghi_chu"][-1].startswith("chua_xac_dinh=dieu_kien_la:")
    # luật chung bật: lấy giá trị kém thuận lợi nhất (8): 10 giờ Lệch, 8 giờ Đúng
    assert ket(chay("tai_nghe", "x", tb_nghe_nhac(10.0), kho, luat_chung_cho_nhieu_gia_tri=True))[:2] == ("LECH", "D4")
    assert ket(chay("tai_nghe", "x", tb_nghe_nhac(8.0), kho, luat_chung_cho_nhieu_gia_tri=True)) == ("DUNG", "D3", None)
    assert ket(chay("tai_nghe", "x", tb_nghe_nhac(7.0), kho, luat_chung_cho_nhieu_gia_tri=True)) == ("DUNG", "D3", None)


def test_luat_chan_tinh_huong_2_mot_gia_tri_kem_dieu_kien_la():
    kho = [tl_game(10.0, "tắt chế độ chơi game", "tn-b#1")]
    for bat in (False, True):   # công tắc không cứu được: chỉ một giá trị, không phải lựa chọn
        assert ket(chay("tai_nghe", "x", tb_nghe_nhac(10.0), kho, luat_chung_cho_nhieu_gia_tri=bat)) == ("CHUA_DU", "D1a", None)
    # con số không khớp giá trị có điều kiện lạ thì không bị chặn
    assert chay("tai_nghe", "x", tb_nghe_nhac(12.0), kho)["dong_d"] == "D5"


def test_luat_chan_tinh_huong_3_tuyen_bo_tu_ghi_dieu_kien_la():
    tb = tb_nghe_nhac(10.0)
    tb["dieu_kien_khac"] = LA
    kho = [pin(10.0, tn_dk(), ma="tn-b#1", ck="đến", kieu="toi_da")]
    assert ket(chay("tai_nghe", "x", tb, kho)) == ("CHUA_DU", "D1a", None)


def test_cong_tac_luat_chung_doc_tu_yaml():
    cf = copy.deepcopy(CF["tai_nghe"])
    assert cf["chung"]["dieu_kien_la"]["luat_chung_cho_nhieu_gia_tri"] == "tat"
    kho = [tl_game(10.0, "tắt chế độ chơi game", "tn-b#1"), tl_game(8.0, "bật chế độ chơi game", "tn-b#2")]
    ban_ghi = {"ma_mau": "tn-b", "chu_tuyen_bo": "x", "tuyen_bo": tb_nghe_nhac(8.0), "bang_chung": kho}
    assert qd.quyet_dinh(ban_ghi, cf)["dong_d"] == "D1a"
    cf["chung"]["dieu_kien_la"]["luat_chung_cho_nhieu_gia_tri"] = "bat"
    assert qd.quyet_dinh(ban_ghi, cf)["dong_d"] == "D3"


# --- D1b ---

def test_d1b_hai_gia_tri_khac_nhau_o_cung_dieu_kien():
    kho = hai_gia_tri()   # 9 và 7 giờ cùng bật chống ồn, tai nghe, nghe nhạc
    for gt in (9.0, 8.0, 12.0):   # trùng một giá trị, giữa hai giá trị, cao hơn cả hai: đều D1b
        k = chay("tai_nghe", "x", tb_nghe_nhac(gt), kho)
        assert ket(k) == ("CHUA_DU", "D1b", None) and k["tai_lieu_mau_thuan"] is True
    assert set(chay("tai_nghe", "x", tb_nghe_nhac(9.0), kho)["bang_chung"]) == {"tn-b#001", "tn-b#002"}


def test_d1b_ngoai_le_khop_ca_hai_qd13():
    kho = hai_gia_tri()
    k = chay("tai_nghe", "x", tb_nghe_nhac(7.0), kho)   # 7 bằng 7 và kém hơn 9
    assert ket(k) == ("DUNG", "D3", None) and "mau_thuan_khop_ca_hai=9/7" in k["ghi_chu"] and k["tai_lieu_mau_thuan"] is False
    k = chay("tai_nghe", "x", tb_nghe_nhac(5.0), kho)
    assert ket(k) == ("DUNG", "D3", None) and "mau_thuan_khop_ca_hai=9/7" in k["ghi_chu"]


def test_d1b_khong_tinh_khi_trong_nguong_bang_hoac_khac_dieu_kien():
    kho = [pin(9.0, tn_dk(), ma="tn-b#1"), pin(9.05, tn_dk(), ma="tn-b#2")]   # 0,55% < 1%
    assert chay("tai_nghe", "x", tb_nghe_nhac(9.0), kho)["dong_d"] == "D3"
    kho = [pin(9.0, tn_dk("bat"), ma="tn-b#1"), pin(7.0, tn_dk("tat"), ma="tn-b#2")]   # mâu thuẫn ở điều kiện khác thì không tính
    assert chay("tai_nghe", "x", tb_nghe_nhac(9.0), kho)["dong_d"] == "D3"


# --- D2 ---

def test_d2_tu_khang_dinh_khong_cao_hon_muc_len_den():
    kho = kho_tai_nghe_b()
    k = chay("tai_nghe", "x", {**tb_nghe_nhac(7.0), "kieu_gia_tri": "khang_dinh", "cum_kieu": "luôn"}, kho)
    assert ket(k) == ("LECH", "D2", "doi_kieu_gia_tri") and "khang_dinh=luôn" in k["ghi_chu"]
    k = chay("tai_nghe", "x", {**tb_nghe_nhac(5.0), "kieu_gia_tri": "khang_dinh", "cum_kieu": "đảm bảo"}, kho)
    assert k["dong_d"] == "D2"


def test_d2_muc_san_hon():
    kho = kho_tai_nghe_b()
    k = chay("tai_nghe", "x", {**tb_nghe_nhac(6.0), "kieu_gia_tri": "khang_dinh", "cum_kieu": "hơn"}, kho)
    assert k["dong_d"] == "D2" and "khang_dinh=hơn" in k["ghi_chu"]
    # bỏ chữ "hơn" thì Đúng ở D3
    assert ket(chay("tai_nghe", "x", tb_nghe_nhac(6.0), kho))[:2] == ("DUNG", "D3")


def test_d2_khong_ap_khi_khong_chac_chan_hoac_cao_hon_muc_toi_da():
    kho = kho_tai_nghe_b()
    # cao hơn mức "lên đến" thì bỏ qua D2, xét tiếp: 8 giờ thuận lợi hơn mọi giá trị ở cùng điều kiện (tai nghe, bật: 7)
    k = chay("tai_nghe", "x", {**tb_nghe_nhac(8.0), "kieu_gia_tri": "khang_dinh", "cum_kieu": "luôn"}, kho)
    assert k["dong_d"] == "D5"
    # tên tính năng không phải từ khẳng định: kiểu giá trị do tim_kieu_gia_tri của chuan_hoa quyết, ra khong_neu thì Đúng
    cau = "Màn hình Luôn Bật hiển thị 120Hz"
    kieu = tim_kieu_gia_tri(cau, tim_gia_tri(cau, CF["dien_thoai"]["chung"])[0], CF["dien_thoai"]["chung"])
    assert kieu.kieu == "khong_neu"
    tl = muc("tan_so_quet", 120.0, "Hz", mau="dt-a", ma="dt-a#4", kieu="toi_da", ck="lên đến")
    tb = {**muc("tan_so_quet", 120.0, "Hz", ma=None, mau="dt-a"), "kieu_gia_tri": kieu.kieu}
    assert ket(chay("dien_thoai", cau, tb, [tl], mau="dt-a")) == ("DUNG", "D3", None)
    assert chay("dien_thoai", cau, {**tb, "kieu_gia_tri": "khang_dinh", "cum_kieu": "luôn"}, [tl], mau="dt-a")["dong_d"] == "D2"


# --- D3 ---

def test_d3_bang_kem_hon_va_ma_ip():
    kho = kho_tai_nghe_b()
    assert ket(chay("tai_nghe", "x", tb_nghe_nhac(7.0), kho)) == ("DUNG", "D3", None)    # bằng giá trị bật chống ồn
    k = chay("tai_nghe", "x", tb_nghe_nhac(5.0), kho)                                       # kém thuận lợi hơn
    assert ket(k) == ("DUNG", "D3", None) and k["bang_chung"] == ["tn-b#003"]
    ip68 = {"bui": 6, "nuoc": 8}
    tl = muc("khang_nuoc", ip68, None, mau="dt-a", ma="dt-a#7")
    for ip in ({"bui": 6, "nuoc": 8}, {"bui": 6, "nuoc": 7}, {"bui": None, "nuoc": 7}):   # IP68, IP67 (kém hơn), IPX7
        assert chay("dien_thoai", "x", muc("khang_nuoc", ip, None, ma=None, mau="dt-a"), [tl], mau="dt-a")["dong_d"] == "D3"


def test_d3_ghi_chu_bo_len_den_va_dieu_kien_so():
    kho = [pin(9.0, tn_dk(), ck="lên đến", kieu="toi_da", trich="Thời gian phát nhạc: lên đến 9 giờ")]
    k = chay("tai_nghe", "x", tb_nghe_nhac(9.0), kho)
    assert k["ly_do"] == 'Khớp với tài liệu: “Thời gian phát nhạc: lên đến 9 giờ”. (quảng cáo bỏ "lên đến")'
    tb_kieu = {**tb_nghe_nhac(9.0), "kieu_gia_tri": "toi_da", "cum_kieu": "lên đến"}
    assert chay("tai_nghe", "x", tb_kieu, kho)["ly_do"] == "Khớp với tài liệu: “Thời gian phát nhạc: lên đến 9 giờ”."
    # điều kiện dạng số: độ sâu 4 m không quá 6 m
    tl = muc("khang_nuoc", {"bui": 6, "nuoc": 8}, None, {"do_sau": {"so": 6, "don_vi": "m"}}, mau="dt-a", ma="dt-a#7")
    tb = muc("khang_nuoc", {"bui": 6, "nuoc": 8}, None, {"do_sau": {"so": 4, "don_vi": "m"}}, ma=None, mau="dt-a")
    assert chay("dien_thoai", "x", tb, [tl], mau="dt-a")["dong_d"] == "D3"


# --- D4 ---

def test_d4_doi_dieu_kien_va_bo_dieu_kien():
    kho = kho_tai_nghe_b()
    k = chay("tai_nghe", "x", tb_nghe_nhac(9.0, dk={"che_do_chong_on": "bat"}), kho)   # 9 giờ chỉ đạt khi tắt chống ồn
    assert ket(k) == ("LECH", "D4", "doi_dieu_kien") and "mac_dinh=bo_phan" in k["ghi_chu"]
    k = chay("tai_nghe", "x", pin_tb(9.0), kho)   # không nêu gì: mặc định bật chống ồn, nghe nhạc, tai nghe
    assert ket(k) == ("LECH", "D4", "bo_dieu_kien") and k["ghi_chu"] == ["mac_dinh=che_do_chong_on,bo_phan,hoat_dong"]


def test_d4_doi_bo_phan_va_gia_tri_trung_hoat_dong_khac():
    kho = kho_tai_nghe_b()
    k = chay("tai_nghe", "x", tb_nghe_nhac(24.0, dk={"bo_phan": "tai_nghe", "che_do_chong_on": "bat"}), kho)   # 24 là của tổng kèm hộp
    assert ket(k) == ("LECH", "D4", "doi_bo_phan")
    k = chay("tai_nghe", "x", tb_nghe_nhac(6.0, dk={"che_do_chong_on": "xuyen_am"}), kho)   # 6 giờ trùng đàm thoại tắt ANC (kiểu V42)
    assert ket(k) == ("LECH", "D4", "doi_dieu_kien") and k["vet"]["u"]["ma_doan"] == "tn-b#010"


def test_d4_chon_muc_khac_it_dieu_kien_nhat_va_uu_tien_bo_phan():
    kho = [pin(10.0, tn_dk("tat", "kem_hop_sac", "dam_thoai"), ma="tn-b#1"), pin(10.0, tn_dk("tat", "tai_nghe", "nghe_nhac"), ma="tn-b#2"),
           pin(6.0, tn_dk(), ma="tn-b#3")]
    k = chay("tai_nghe", "x", tb_nghe_nhac(10.0, dk={"che_do_chong_on": "bat"}), kho)
    assert k["vet"]["u"]["ma_doan"] == "tn-b#2" and k["loai"] == "doi_dieu_kien" and len(k["vet"]["khac_biet"]) == 1
    # hai điều kiện nêu rõ khác cùng lúc: ưu tiên bộ phận
    kho = [pin(10.0, tn_dk("tat", "kem_hop_sac"), ma="tn-b#1"), pin(6.0, tn_dk(), ma="tn-b#3")]
    k = chay("tai_nghe", "x", tb_nghe_nhac(10.0, dk={"che_do_chong_on": "bat", "bo_phan": "tai_nghe"}), kho)
    assert k["loai"] == "doi_bo_phan" and len(k["vet"]["khac_biet"]) == 2
    # ghi đủ các điều kiện khác trong lý do
    assert "tắt" in k["ly_do"] and "hộp" in k["ly_do"] or "tổng" in k["ly_do"]


def test_d4_dieu_kien_so_va_loai_kieu_gia_tri():
    sac = muc("sac_nhanh", 20.0, "phut", {"moc_phan_tram": {"so": 50, "don_vi": "phan_tram"}, "bo_tiep_hop": {"so": 40, "don_vi": "W"}}, mau="dt-a", ma="dt-a#1")
    for w, mong in ((20, "doi_dieu_kien"), (60, None)):
        tb = muc("sac_nhanh", 20.0, "phut", {"moc_phan_tram": {"so": 50, "don_vi": "phan_tram"}, "bo_tiep_hop": {"so": w, "don_vi": "W"}}, ma=None, mau="dt-a")
        k = chay("dien_thoai", "x", tb, [sac], mau="dt-a")
        assert (k["loai"] == mong) and (k["dong_d"] == ("D4" if mong else "D3"))
    tl = muc("dung_luong_pin", 5500.0, "mAh", mau="dt-a", ma="dt-a#5", kieu="dien_hinh", ck="(thông thường)")
    tb = {**muc("dung_luong_pin", 5500.0, "mAh", ma=None, mau="dt-a"), "kieu_gia_tri": "dinh_muc", "cum_kieu": "định mức"}
    assert ket(chay("dien_thoai", "x", tb, [tl], mau="dt-a")) == ("LECH", "D4", "doi_kieu_gia_tri")
    assert ket(chay("dien_thoai", "x", muc("dung_luong_pin", 5500.0, "mAh", ma=None, mau="dt-a"), [tl], mau="dt-a"))[:2] == ("DUNG", "D3")


# --- D5 ---

def test_d5_thuan_loi_hon_hoac_mau_thuan_o_cung_dieu_kien():
    kho = kho_tai_nghe_b()
    assert ket(chay("tai_nghe", "x", tb_nghe_nhac(8.0), kho)) == ("SAI", "D5", "doi_gia_tri")
    # thời gian sạc: thấp hơn là thuận lợi hơn
    sac = muc("sac_nhanh", 50.0, "phut", {"moc_phan_tram": {"so": 100, "don_vi": "phan_tram"}, "bo_tiep_hop": {"so": 67, "don_vi": "W"}}, mau="dt-a", ma="dt-a#1")
    tb = muc("sac_nhanh", 40.0, "phut", {"moc_phan_tram": {"so": 100, "don_vi": "phan_tram"}, "bo_tiep_hop": {"so": 67, "don_vi": "W"}}, ma=None, mau="dt-a")
    assert ket(chay("dien_thoai", "x", tb, [sac], mau="dt-a")) == ("SAI", "D5", "doi_gia_tri")


def test_d5_ma_ip_khac_nhanh_va_khong_khang_dinh():
    tl = muc("khang_nuoc", {"bui": 6, "nuoc": 8}, None, mau="dt-a", ma="dt-a#7")
    k = chay("dien_thoai", "x", muc("khang_nuoc", {"bui": None, "nuoc": 5}, None, ma=None, mau="dt-a"), [tl], mau="dt-a")   # IPX5: khác nhánh
    assert ket(k) == ("SAI", "D5", "doi_gia_tri")
    # IP58 so với máy IP57: thuận lợi hơn nên Sai
    tl57 = muc("khang_nuoc", {"bui": 5, "nuoc": 7}, None, mau="dt-a", ma="dt-a#7")
    assert chay("dien_thoai", "x", muc("khang_nuoc", {"bui": 5, "nuoc": 8}, None, ma=None, mau="dt-a"), [tl57], mau="dt-a")["dong_d"] == "D5"
    # hộp sạc "cũng kháng nước" mà tài liệu ghi không: Sai, doi_bo_phan
    kho = [muc("khang_nuoc", "khong", None, {"bo_phan": "hop_sac"}, ma="tn-b#1"), muc("khang_nuoc", {"bui": 5, "nuoc": 7}, None, ma="tn-b#2")]
    tb = muc("khang_nuoc", "co", None, {"bo_phan": "hop_sac"}, ma=None)
    assert ket(chay("tai_nghe", "x", tb, kho)) == ("SAI", "D5", "doi_bo_phan")


def test_d5_thuan_loi_hon_moi_gia_tri_khi_khong_co_gia_tri_o_dieu_kien():
    kho = [pin(7.0, tn_dk(), ma="tn-b#1"), pin(30.0, tn_dk("bat", "kem_hop_sac"), ma="tn-b#1")]
    k = chay("tai_nghe", "x", tb_nghe_nhac(8.0, dk={"che_do_chong_on": "xuyen_am"}), kho)
    assert ket(k) == ("SAI", "D5", "doi_gia_tri")   # 8 > 7, cao nhất của tai nghe; 30 là của tổng kèm hộp không tính


# --- D6 ---

def test_d6_khong_cong_bo_o_dieu_kien_cua_tuyen_bo():
    kho = kho_tai_nghe_b()
    k = chay("tai_nghe", "x", tb_nghe_nhac(6.5, dk={"che_do_chong_on": "xuyen_am"}), kho)
    assert ket(k) == ("CHUA_DU", "D6", None) and k["ly_do"].startswith("Tài liệu không công bố thời lượng pin ở")
    assert chay("tai_nghe", "x", tb_nghe_nhac(3.0, dk={"che_do_chong_on": "xuyen_am"}), kho)["dong_d"] == "D6"
    assert chay("tai_nghe", "x", tb_nghe_nhac(8.0, dk={"hoat_dong": "dam_thoai"}), [pin(9.0, tn_dk("bat", hd="nghe_nhac"), ma="tn-b#1")])["dong_d"] in ("D5", "D6")


# --- Ba trạng thái điều kiện, luật cụm phủ, chép nhãn ---

def test_ba_trang_thai_dieu_kien():
    # không áp dụng: trang đồng hồ ghi chung 18 giờ, không tách theo phiên bản (V14, V15)
    r = next(v for v in VI_DU if v["id"] == "V15")
    ban_ghi = copy.deepcopy(r["ban_ghi"])
    ban_ghi["bang_chung"] = [u for u in ban_ghi["bang_chung"] if "phien_ban" not in u["dieu_kien"]]
    k = qd.quyet_dinh(ban_ghi, CF["dong_ho"])
    assert k["dong_d"] == "D3" and "phien_ban" in k["vet"]["khong_ap_dung"] and "phien_ban" not in k["vet"]["dieu_kien_tuyen_bo"]
    # không nêu: dùng cách hiểu mặc định và ghi mac_dinh
    k = chay("tai_nghe", "x", pin_tb(9.0), kho_tai_nghe_b())
    assert set(k["vet"]["dieu_kien_tuyen_bo"]) == {"che_do_chong_on", "bo_phan", "hoat_dong"} and set(k["vet"]["nguon_dieu_kien"].values()) == {"mac_dinh"}
    # chưa xác định (D1a) và điều kiện chưa hỗ trợ (dieu_kien_khac) tách riêng: nguyên nhân khác nhau
    sac = muc("sac_nhanh", 20.0, "phut", {"moc_phan_tram": {"so": 50, "don_vi": "phan_tram"}}, mau="dt-a", ma="dt-a#1")
    k1 = chay("dien_thoai", "x", muc("sac_nhanh", 20.0, "phut", ma=None, mau="dt-a"), [sac], mau="dt-a")
    tb = tb_nghe_nhac(6.0)
    tb["dieu_kien_khac"] = LA
    k2 = chay("tai_nghe", "x", tb, kho_tai_nghe_b())
    assert k1["vet"]["nguyen_nhan"]["loai"] == "mac_dinh" and k2["vet"]["nguyen_nhan"]["loai"] == "chua_xac_dinh"


def test_cum_phu_nhieu_gia_tri():
    wa = "dh-apple-watchse3"
    r = next(v for v in VI_DU if v["id"] == "V49")
    k = chay_vi_du(r)
    assert ket(k) == ("LECH", "D4", "doi_dieu_kien") and k["vet"]["dieu_kien_tuyen_bo"]["che_do_nguon"] == "thuong"
    assert k["vet"]["nguon_dieu_kien"]["che_do_nguon"] == "cum_phu" and "chua_xac_dinh" not in " ".join(k["ghi_chu"])
    # kháng nước "mọi hoạt động" phủ cả hoạt động bị cấm (đồng hồ)
    tl = muc("khang_nuoc", 50.0, "m", {"chuan_do_sau": "iso_22810", "hoat_dong_cho_phep": "duoc_phep"}, mau=wa, ma=wa + "#16")
    tb = {**muc("khang_nuoc", 50.0, "m", ma=None, mau=wa), "dieu_kien_khac": [{"loai": "che_do_hoat_dong", "cum": "mọi hoạt động dưới nước", "trich": "x"}]}
    k = chay("dong_ho", "Đồng hồ C chống nước 50 m cho mọi hoạt động dưới nước", tb, [tl], mau=wa)
    assert ket(k) == ("LECH", "D4", "doi_dieu_kien") and k["vet"]["dieu_kien_tuyen_bo"]["hoat_dong_cho_phep"] == "bi_cam"
    # "mọi điều kiện ánh sáng" -> chế độ hiển thị, kém thuận lợi nhất là tiêu chuẩn (1000 nit)
    ds = [muc("do_sang", 1000.0, "nit", {"che_do_hien_thi": "tieu_chuan"}, mau="dt-a", ma="dt-a#5"),
          muc("do_sang", 3000.0, "nit", {"che_do_hien_thi": "ngoai_troi"}, mau="dt-a", ma="dt-a#5")]
    tb = {**muc("do_sang", 3000.0, "nit", ma=None, mau="dt-a"), "dieu_kien_khac": [{"loai": "che_do_hoat_dong", "cum": "mọi điều kiện ánh sáng", "trich": "x"}]}
    k = chay("dien_thoai", "x", tb, ds, mau="dt-a")
    assert ket(k) == ("LECH", "D4", "doi_dieu_kien") and k["vet"]["dieu_kien_tuyen_bo"]["che_do_hien_thi"] == "tieu_chuan"
    # "dù nghe nhạc hay gọi điện" -> hoạt động, kém thuận lợi nhất là đàm thoại
    kho = [pin(9.0, tn_dk(hd="nghe_nhac"), ma="tn-b#1"), pin(6.0, tn_dk(hd="dam_thoai"), ma="tn-b#1")]
    tb = {**pin_tb(9.0), "dieu_kien_khac": [{"loai": "che_do_hoat_dong", "cum": "dù nghe nhạc hay gọi điện", "trich": "x"}]}
    k = chay("tai_nghe", "x", tb, kho)
    assert ket(k) == ("LECH", "D4", "doi_dieu_kien") and k["vet"]["dieu_kien_tuyen_bo"]["hoat_dong"] == "dam_thoai"
    # điều kiện trực tiếp thắng cụm phủ (QĐ11)
    tb = {**pin_tb(9.0, {"hoat_dong": "nghe_nhac"}), "dieu_kien_khac": tb["dieu_kien_khac"]}
    k = chay("tai_nghe", "x", tb, kho)
    assert k["dong_d"] == "D3" and k["vet"]["nguon_dieu_kien"]["hoat_dong"] == "neu_ro"
    # cụm phủ không xác định được điều kiện vẫn là điều kiện lạ
    tb = {**pin_tb(9.0), "dieu_kien_khac": [{"loai": "che_do_hoat_dong", "cum": "mọi điều kiện thời tiết", "trich": "x"}]}
    assert chay("tai_nghe", "x", tb, kho)["dong_d"] == "D1a"


DT_A = [muc("thoi_luong_pin", 22.0, "gio", {"hoat_dong": "xem_video"}, mau="dt-a", ma="dt-a#1", kieu="toi_da", ck="lên đến",
            trich="Thời gian xem video: lên đến 22 giờ"),
        muc("thoi_luong_pin", 19.0, "gio", {"hoat_dong": "xem_video_truc_tuyen"}, mau="dt-a", ma="dt-a#1", kieu="toi_da", ck="lên đến",
            trich="Thời gian xem video (trực tuyến): lên đến 19 giờ")]


def qd15(chu, gt, dk):
    return chay("dien_thoai", chu, muc("thoi_luong_pin", gt, "gio", dk, ma=None, mau="dt-a"), copy.deepcopy(DT_A), mau="dt-a")


def test_qd15_chep_dung_nhan():
    xem = {"hoat_dong": "chua_ro_loai_video"}
    k = qd15("Điện thoại A xem video 22 giờ", 22.0, xem)
    assert ket(k) == ("DUNG", "D3", None) and "chep_nhan=xem video" in k["ghi_chu"] and not any(g.startswith("mac_dinh") for g in k["ghi_chu"])
    assert ket(qd15("Điện thoại A xem video 20 giờ", 20.0, xem)) == ("DUNG", "D3", None)    # thấp hơn
    assert ket(qd15("Điện thoại A xem video 22 giờ", 22.0, xem))[0] == "DUNG"             # số bằng
    assert ket(qd15("Điện thoại A xem video 25 giờ", 25.0, xem)) == ("SAI", "D5", "doi_gia_tri")   # cao hơn
    k = qd15("Pin Điện thoại A dùng 22 giờ", 22.0, {"hoat_dong": "chua_ro_hoat_dong"})   # không trùng chữ nhãn nào: mặc định
    assert ket(k) == ("LECH", "D4", "bo_dieu_kien") and not any(g.startswith("chep_nhan") for g in k["ghi_chu"])


def test_qd15_thieu_chu_dieu_kien_thi_khong_ap():
    kho = [pin(30.0, tn_dk("tat", "kem_hop_sac"), ma="tn-b#1", trich="Tổng thời gian phát nhạc (tắt ANC): 30 giờ", ck=None)]
    k = chay("tai_nghe", "Tai nghe B nghe nhạc 30 giờ", tb_nghe_nhac(30.0), kho)   # thiếu "tổng" và "tắt ANC"
    assert not any(g.startswith("chep_nhan") for g in k["ghi_chu"]) and k["dong_d"] == "D4"
    chu = "Tai nghe B tổng thời gian phát nhạc tắt ANC 30 giờ"
    k = chay("tai_nghe", chu, pin_tb(30.0), kho)
    assert ket(k) == ("DUNG", "D3", None) and "chep_nhan=tổng thời gian phát nhạc tắt anc" in k["ghi_chu"]


def test_qd15_hai_nhan_dai_bang_nhau_dieu_kien_khac_nhau_khong_ap():
    kho = [pin(10.0, tn_dk("bat"), ma="tn-b#1", trich="Phát nhạc: 10 giờ"), pin(8.0, tn_dk("tat"), ma="tn-b#2", trich="Phát nhạc: 8 giờ")]
    k = chay("tai_nghe", "Tai nghe B phát nhạc 10 giờ", pin_tb(10.0), kho)
    assert not any(g.startswith("chep_nhan") for g in k["ghi_chu"])


def test_doi_con_so_khong_doi_dieu_kien_tuyen_bo():
    """T5.5: không dùng con số của tuyên bố để chọn điều kiện; đổi con số thì dieu_kien_tuyen_bo trong vết không đổi."""
    for r in VI_DU:
        g = r["ban_ghi"]["tuyen_bo"]["gia_tri"]
        if not isinstance(g, float):
            continue
        goc = chay_vi_du(r)["vet"].get("dieu_kien_tuyen_bo")
        khac = [g * 0.5, g * 1.5, g + 7, g * 3]
        khac += [u["gia_tri"] for u in r["ban_ghi"]["bang_chung"] if isinstance(u["gia_tri"], float)]
        for v in khac:
            ban_ghi = copy.deepcopy(r["ban_ghi"])
            ban_ghi["tuyen_bo"]["gia_tri"] = v
            k = qd.quyet_dinh(ban_ghi, CF[NHOM[r["ma_mau"][:2]]])
            assert k["vet"].get("dieu_kien_tuyen_bo") == goc, (r["id"], v)


# --- P−ĐK ---

def test_p_tru_dk_buds3_pro_7_gio_khi_bat_chong_on_ra_dung():
    r = next(v for v in VI_DU if v["id"] == "V31")
    assert ket(chay_vi_du(r)) == ("LECH", "D4", "doi_dieu_kien")
    k = chay_vi_du(r, doi_chieu=False)
    assert ket(k) == ("DUNG", "D3", None) and k["ghi_chu"] == []


def test_p_tru_dk_khong_bao_gio_ra_d1a_d1b_d4():
    for r in VI_DU:
        k = chay_vi_du(r, doi_chieu=False)
        assert k["dong_d"] not in ("D1a", "D1b", "D4", "D6") or (k["dong_d"] == "D1" and r["id"] == "V45"), (r["id"], k["dong_d"])
        assert k["tai_lieu_mau_thuan"] is False
    k = chay("tai_nghe", "x", tb_nghe_nhac(12.0), hai_gia_tri(), doi_chieu=False)   # P có D1b ở đây, P−ĐK thì không
    assert k["dong_d"] == "D5"
    k = chay("tai_nghe", "x", tb_nghe_nhac(5.0), hai_gia_tri(), doi_chieu=False)
    assert k["dong_d"] == "D3"


# --- Ngưỡng QĐ8 ---

def test_dem_nguong_qd8():
    def d4(dk, nguon):
        return {"dong_d": "D4", "vet": {"khac_biet": [{"dk": dk, "nguon": nguon}]}}
    ds = [d4("hoat_dong", "neu_ro"), d4("hoat_dong", "mac_dinh"), d4("che_do_chong_on", "neu_ro"), d4("hoat_dong", "chep_nhan"), {"dong_d": "D3", "vet": {}}]
    r = qd.dem_nguong_qd8(ds)
    assert r == {"d4": 4, "nhieu_hoat_dong": 1, "ti_le": 0.25, "vuot_nguong": False}
    assert qd.dem_nguong_qd8(ds[:1])["vuot_nguong"] is True and qd.NGUONG_QD8 == 0.25
    assert qd.dem_nguong_qd8([]) == {"d4": 0, "nhieu_hoat_dong": 0, "ti_le": 0.0, "vuot_nguong": False}


def test_dem_nguong_qd8_tren_51_vi_du():
    r = qd.dem_nguong_qd8([chay_vi_du(v) for v in VI_DU])
    assert r["d4"] >= 15 and r["nhieu_hoat_dong"] >= 1   # V42 nêu rõ nghe nhạc mà 5 giờ trùng đàm thoại tắt ANC


# --- Lý do ---

@pytest.mark.parametrize("r", VI_DU, ids=lambda r: r["id"])
def test_ly_do_khop_nhan(r):
    k = chay_vi_du(r)
    assert NHAN_CUA_DONG[k["dong_d"]] == k["nhan"]
    assert k["ly_do"].startswith(MAU_CAU[k["dong_d"]]) and k["ly_do"].endswith(("." , '”.', "”", ")"))
    assert "\n" not in k["ly_do"]
    if k["dong_d"] in ("D2", "D3", "D4"):
        assert k["vet"]["trich_chinh"] in k["ly_do"]
    if k["dong_d"] == "D4":
        assert "chỉ đạt khi" in k["ly_do"] and "tuyên bố " in k["ly_do"] and "Nguồn: “" in k["ly_do"]


def test_ly_do_tam_mau_cau_dung_dong():
    mau = {}
    for r in VI_DU:
        k = chay_vi_du(r)
        mau.setdefault(k["dong_d"], k["ly_do"])
    assert set(mau) == {"D1", "D1a", "D1b", "D2", "D3", "D4", "D5", "D6"}
    assert mau["D1"] == "Tài liệu của Galaxy Buds3 Pro không có thông số sạc nhanh."
    assert re.fullmatch(r"Tài liệu ghi hai giá trị khác nhau cho thời lượng pin ở .+: “.+” và “.+”\.", mau["D1b"])
    assert re.fullmatch(r"Tài liệu ghi .+ ở .+; tuyên bố ghi .+\.", mau["D5"])
    assert re.fullmatch(r"Tài liệu không công bố thời lượng pin ở .+\.", mau["D6"])


def test_ly_do_d3_so_thang_va_so_trong_ly_do_d4():
    k = chay_vi_du(next(v for v in VI_DU if v["id"] == "V12"))
    assert k["ly_do"].endswith("Tài liệu không nêu điều kiện.")
    k = chay_vi_du(next(v for v in VI_DU if v["id"] == "V21"))
    assert k["ly_do"].startswith("Giá trị 20 phút chỉ đạt khi bộ tiếp hợp 40W trở lên; tuyên bố được hiểu là chỉ có đồ trong hộp.")
    k = chay_vi_du(next(v for v in VI_DU if v["id"] == "V31"))
    assert k["ly_do"].startswith("Giá trị 7 giờ chỉ đạt khi tắt ANC; tuyên bố nêu bật ANC.")


def test_ten_hien_thi_va_dinh_dang():
    cf = CF["tai_nghe"]
    assert ld.ten_hien_thi(cf, "che_do_chong_on", "bat") == "bật ANC"
    assert ld.ten_hien_thi(CF["dien_thoai"], "hoat_dong", "xem_video_truc_tuyen") == "xem video trực tuyến"
    assert ld.dinh_dang_so({"bui": 5, "nuoc": 7}) == "IP57" and ld.dinh_dang_so({"bui": None, "nuoc": 7}) == "IPX7"
    assert ld.dinh_dang_so(26.0) == "26" and ld.dinh_dang_so(4.5) == "4.5"


# --- Luật lan điều kiện giữa các mục cùng giá trị ---

def _lan(tls, tb, chu="x", nhom="tai_nghe", mau="tn-b"):
    return chay(nhom, chu, tb, tls, mau=mau)


def test_lan_dieu_kien_dung():
    a = pin(7.0, tn_dk("tat", "tai_nghe"), ma="tn-b#1")
    b = pin(7.0, {"che_do_chong_on": "tat", "hoat_dong": "nghe_nhac"}, ma="tn-b#2")   # không ghi bộ phận
    goc = copy.deepcopy([a, b])
    ds, vet = qd.lan_dieu_kien([a, b], qd.BoiCanh({"ma_mau": "tn-b", "tuyen_bo": pin_tb(7.0) | {"thuoc_tinh": "thoi_luong_pin"}}, CF["tai_nghe"]))
    assert ds[1]["dieu_kien"]["bo_phan"] == "tai_nghe" and ds[1]["nguon_dieu_kien"]["bo_phan"] == "lan"
    assert vet == [{"ma_doan": "tn-b#2", "dk": "bo_phan", "gia_tri": "tai_nghe"}]
    assert [a, b] == goc   # không sửa đầu vào
    # tuyên bố hộp sạc: mục #2 nhờ lan là của tai nghe nên không khớp; nếu không lan thì mặc định cũng là tai nghe: cùng kết quả D4
    k = _lan([a, b], tb_nghe_nhac(7.0, dk={"che_do_chong_on": "tat", "bo_phan": "kem_hop_sac"}))
    assert ket(k) == ("LECH", "D4", "doi_bo_phan") and k["vet"]["lan"][0]["dk"] == "bo_phan"
    # điều kiện số lan: Xiaomi 67W (V23 cũ) — mục không ghi bộ sạc nhận 67W của mục cùng giá trị
    sac = [muc("cong_suat_sac", 67.0, "W", {"bo_tiep_hop": {"so": 67, "don_vi": "W"}}, mau="dt-a", ma="dt-a#1"),
           muc("cong_suat_sac", 67.0, "W", {}, mau="dt-a", ma="dt-a#2")]
    k = chay("dien_thoai", "x", muc("cong_suat_sac", 67.0, "W", ma=None, mau="dt-a"), sac, mau="dt-a")
    assert ket(k) == ("LECH", "D4", "bo_dieu_kien")
    k = chay("dien_thoai", "x", muc("cong_suat_sac", 67.0, "W", {"bo_tiep_hop": {"so": 67, "don_vi": "W"}}, ma=None, mau="dt-a"), sac, mau="dt-a")
    assert ket(k)[:2] == ("DUNG", "D3")


def test_lan_khong_khi_hai_gia_tri_dieu_kien_khac_nhau_hoac_khac_gia_tri():
    sac = [muc("cong_suat_sac", 67.0, "W", {"bo_tiep_hop": {"so": 67, "don_vi": "W"}}, mau="dt-a", ma="dt-a#1"),
           muc("cong_suat_sac", 67.0, "W", {"bo_tiep_hop": {"so": 30, "don_vi": "W"}}, mau="dt-a", ma="dt-a#2"),
           muc("cong_suat_sac", 67.0, "W", {}, mau="dt-a", ma="dt-a#3")]
    k = chay("dien_thoai", "x", muc("cong_suat_sac", 67.0, "W", ma=None, mau="dt-a"), sac, mau="dt-a")
    assert k["vet"]["lan"] == []
    # con số khác nhau thì không cùng nhóm
    sac = [muc("cong_suat_sac", 67.0, "W", {"bo_tiep_hop": {"so": 67, "don_vi": "W"}}, mau="dt-a", ma="dt-a#1"),
           muc("cong_suat_sac", 25.0, "W", {}, mau="dt-a", ma="dt-a#3")]
    k = chay("dien_thoai", "x", muc("cong_suat_sac", 25.0, "W", ma=None, mau="dt-a"), sac, mau="dt-a")
    assert k["vet"]["lan"] == [] and k["dong_d"] == "D3"


def test_lan_khong_qua_muc_khac_san_pham():
    a = pin(7.0, tn_dk("tat", "tai_nghe"), ma="tn-b#1", khac_sp=True)   # cột sản phẩm khác
    b = pin(7.0, {"che_do_chong_on": "tat", "hoat_dong": "nghe_nhac"}, ma="tn-b#2")
    k = _lan([a, b], tb_nghe_nhac(7.0, dk={"che_do_chong_on": "tat"}))
    assert k["vet"]["lan"] == [] and k["dong_d"] == "D3"


def test_lan_dieu_kien_khac():
    la = [{"loai": "che_do_hoat_dong", "cum": "chế độ chơi game", "trich": "x"}]
    a = pin(10.0, tn_dk(), ma="tn-b#1", khac=la)
    b = pin(10.0, tn_dk(), ma="tn-b#2")   # cùng con số ở đoạn khác, không ghi cụm lạ
    ds, vet = qd.lan_dieu_kien([a, b], qd.BoiCanh({"ma_mau": "tn-b", "tuyen_bo": pin_tb(10.0) | {"thuoc_tinh": "thoi_luong_pin"}}, CF["tai_nghe"]))
    assert ds[1]["dieu_kien_khac"] == la and vet == [{"ma_doan": "tn-b#2", "dk": "dieu_kien_khac", "gia_tri": "chế độ chơi game"}]
    assert b["dieu_kien_khac"] == []
    k = _lan([a, b], tb_nghe_nhac(10.0))   # luật chặn vẫn đúng: D1a, không ra Đúng
    assert ket(k) == ("CHUA_DU", "D1a", None) and set(k["bang_chung"]) == {"tn-b#1", "tn-b#2"}
    c = pin(8.0, tn_dk(), ma="tn-b#3")   # con số khác: không lan
    bc = qd.BoiCanh({"ma_mau": "tn-b", "tuyen_bo": pin_tb(8.0) | {"thuoc_tinh": "thoi_luong_pin"}}, CF["tai_nghe"])
    assert qd.lan_dieu_kien([a, b, c], bc)[0][2]["dieu_kien_khac"] == []


def test_p_tru_dk_khong_lan():
    r = next(v for v in VI_DU if v["id"] == "V27")
    assert "lan" not in chay_vi_du(r, doi_chieu=False)["vet"]
