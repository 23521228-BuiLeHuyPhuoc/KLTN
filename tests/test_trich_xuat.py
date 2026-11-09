"""Test trích xuất có neo nguồn và kiểm tra đầy đủ (Bước 22; luan_van/buoc22_thiet_ke_trich_xuat.md mục 11). Chỉ dùng LLM giả.

Chữ thật: tuyên bố tb-00040 của data/tuyen_bo/thu.jsonl và đoạn tn-samsung-buds3pro#038, #042, #044 (tập phát triển). Ca khác tự
đặt (sản phẩm "Buds B", "Điện thoại A" như đặc tả). Không mở dữ liệu tập kiểm tra, không gọi mạng.
"""
import copy
import importlib.util
import json
from pathlib import Path
import re
import socket

import pytest

from kiemchung import trich_xuat as tx, truy_hoi as th
from kiemchung.cau_hinh import GOC
from kiemchung.llm import LLMClient, LLMError, LLMResult

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chay_trich_xuat", ROOT / "scripts/chay_trich_xuat.py")
chay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chay)

BUDS = "tn-samsung-buds3pro"
MODEL = "gemini-3.6-flash"


@pytest.fixture(autouse=True)
def moi_truong_sach(monkeypatch):
    th.xoa_dem()
    for ten in ("GEMINI_API_KEY", "GROQ_API_KEY", "GOOGLE_API_KEY"):
        monkeypatch.delenv(ten, raising=False)

    def chan(*args, **kwargs):
        raise AssertionError("Test không được dùng mạng")
    monkeypatch.setattr(socket.socket, "connect", chan)
    yield
    th.xoa_dem()


@pytest.fixture(scope="module")
def cac():
    return tx.tat_ca_cau_hinh()


@pytest.fixture(scope="module")
def tai_nghe():
    return tx.lay_cau_hinh("tai_nghe")


@pytest.fixture(scope="module")
def dien_thoai():
    return tx.lay_cau_hinh("dien_thoai")


def doan_that(*so):
    van_ban = dict(th.doc_doan(BUDS))
    return [(f"{BUDS}#{s}", van_ban[f"{BUDS}#{s}"]) for s in so]


def gt(chu, trich, don_vi=None):
    return {"chu": chu, "don_vi": don_vi, "trich": trich}


def dk(loai, cum, trich=None):
    return {"loai": loai, "cum": cum, "trich": trich or cum}


def tb_muc(thuoc_tinh="thoi_luong_pin", gia_tri=None, dieu_kien=(), san_pham=None):
    return {"san_pham": san_pham, "thuoc_tinh": thuoc_tinh, "gia_tri": gia_tri, "dieu_kien": list(dieu_kien)}


def tl_muc(ma, gia_tri, dieu_kien=(), san_pham=None):
    return {"ma_doan": ma, "san_pham": san_pham, "gia_tri": gia_tri, "dieu_kien": list(dieu_kien)}


def chay_xu_ly(du, tuyen_bo, doan, cac, ma_mau=BUDS, nhom="tai_nghe", **kw):
    cau_hinh = next(c for c in cac if c["nhom"] == nhom)
    return tx.xu_ly(du, tuyen_bo, doan, ma_mau, cau_hinh, cac, **kw)


def ly_do(ket, truong=None):
    return [(b["phia"], b["chi_so"], b["truong"], b["ly_do"]) for b in ket["bi_loai"] if truong is None or b["truong"] == truong]


# --- Câu lệnh ---

def test_cau_lenh_trong_ma_trung_khoi_cua_dac_ta():
    md = (GOC / "luan_van" / "buoc22_thiet_ke_trich_xuat.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- CAU_LENH_TRICH_XUAT: bat_dau -->\n```text\n(.*?)\n```\n<!-- CAU_LENH_TRICH_XUAT: ket_thuc -->", md, re.S)
    assert m and tx.CAU_LENH_TRICH_XUAT == m.group(1)
    for cho in ("{ten_nhom}", "{bang_thuoc_tinh}", "{tuyen_bo}", "{doan_1..k}"):
        assert tx.CAU_LENH_TRICH_XUAT.count(cho) == 1


def test_mo_ta_thuoc_tinh_trung_bang_cua_huong_dan_tach_tay():
    md = (GOC / "data" / "tuyen_bo" / "huong_dan_tach_tay.md").read_text(encoding="utf-8")
    bang = md.split("## Thuộc tính được giữ")[1].split("\n## ")[0]
    mong = {n: {} for n in tx.NHOM}
    for dong in bang.split("\n"):
        o = [x.strip() for x in dong.strip().strip("|").split("|")]
        if dong.startswith("| `") and len(o) == 4:
            for nhom, cell in zip(("dien_thoai", "tai_nghe", "dong_ho"), o[1:]):
                if cell != "Không có":
                    mong[nhom][o[0].strip("`")] = cell
    assert tx.MO_TA_THUOC_TINH == mong
    for nhom in tx.NHOM:     # đúng tập thuộc tính của YAML nhóm (thứ tự dòng trong câu lệnh theo YAML, không theo bảng)
        assert set(tx.lay_cau_hinh(nhom)["thuoc_tinh"]) == set(mong[nhom])


def test_bang_thuoc_tinh_va_ghep_cau_lenh(tai_nghe):
    bang = tx.bang_thuoc_tinh("tai_nghe", tai_nghe)
    dong = bang.split("\n")
    assert dong[0] == "- thoi_luong_pin (gio): Nghe nhạc, đàm thoại bao nhiêu giờ (cả khi tính hộp sạc)"
    assert [d.split(" ")[1] for d in dong] == ["thoi_luong_pin", "sac_nhanh", "khang_nuoc", "dung_luong_pin"]
    doan = [("a#001", "Đoạn một\ndòng hai"), ("a#002", "Đoạn hai")]
    cau = tx.ghep_cau_lenh("tai_nghe", tai_nghe, "Buds B pin 9 giờ", doan)
    assert "quảng cáo về tai nghe và từ các đoạn" in cau
    assert bang in cau
    assert cau.endswith("Tuyên bố: Buds B pin 9 giờ\nTài liệu:\n[a#001] Đoạn một\ndòng hai\n\n[a#002] Đoạn hai\nKết quả:")
    assert tx.ghep_cau_lenh("tai_nghe", tai_nghe, "gồm {doan_1..k} và {ten_nhom}", doan).count("{doan_1..k} và {ten_nhom}") == 1
    with pytest.raises(ValueError):
        tx.ghep_cau_lenh("tai_nghe", tai_nghe, "x", [])


# --- Đọc đầu ra (mục 4) ---

def test_json_hong_va_sai_khung_cho_loi(cac):
    for du in ([], "x", {"bang_chung": []}, {"tuyen_bo": {}}, {"tuyen_bo": [], "bang_chung": []},
               {"tuyen_bo": {}, "bang_chung": {}}):
        ket = chay_xu_ly(du, "x", doan_that("044"), cac)
        assert ket["loi"] and ket["tuyen_bo"] is None and ket["bang_chung"] == []
    assert chay_xu_ly({"tuyen_bo": {}, "bang_chung": {}}, "x", [], cac)["loi"].startswith("bang_chung_sai_kieu")


def test_muc_sai_kieu_bi_bo_rieng_voi_ly_do_sai_luoc_do(cac):
    tuyen_bo = "Buds B nghe nhạc lên đến 9 giờ"
    du = {"tuyen_bo": {"san_pham": "Buds B", "thuoc_tinh": "thoi_luong_pin", "gia_tri": gt("9", "lên đến 9 giờ", "giờ"),
                       "dieu_kien": [dk("che_do_hoat_dong", "nghe nhạc"), dk("loai_la", "x"), "không phải dict", {"cum": 1}]},
          "bang_chung": [tl_muc(f"{BUDS}#044", gt("6", "Lên đến 6", None)) | {"dieu_kien": "không phải danh sách"},
                         "không phải dict", {"ma_doan": 5}]}
    ket = chay_xu_ly(du, tuyen_bo, doan_that("044"), cac)
    assert ket["loi"] is None
    assert ly_do(ket) == [("tuyen_bo", None, "san_pham", "sai_luoc_do"), ("tuyen_bo", None, "dieu_kien[1]", "sai_luoc_do"),
                          ("tuyen_bo", None, "dieu_kien[2]", "sai_luoc_do"), ("tuyen_bo", None, "dieu_kien[3]", "sai_luoc_do"),
                          ("tai_lieu", 0, "dieu_kien", "sai_luoc_do"), ("tai_lieu", 1, "muc", "sai_luoc_do"),
                          ("tai_lieu", 2, "muc", "sai_luoc_do")]
    assert ket["tuyen_bo"]["gia_tri"] == 9.0 and ket["tuyen_bo"]["dieu_kien"] == {"hoat_dong": "nghe_nhac"}
    assert [m["gia_tri"] for m in ket["bang_chung"]] == [6.0]
    assert [b["chi_so"] for b in ket["bang_chung_bi_loai"]] == [1, 2]


def test_gia_tri_sai_kieu_thi_muc_tai_lieu_vao_bi_loai(cac):
    du = {"tuyen_bo": tb_muc(), "bang_chung": [tl_muc(f"{BUDS}#044", {"chu": 6, "trich": "Lên đến 6"}),
                                              tl_muc(f"{BUDS}#044", None)]}
    ket = chay_xu_ly(du, "Buds B", doan_that("044"), cac)
    assert ket["bang_chung"] == []
    assert [(b["chi_so"], b["ly_do"]) for b in ket["bang_chung_bi_loai"]] == [(0, ["sai_luoc_do"]), (1, ["thieu_gia_tri"])]


# --- Neo nguồn qua xu_ly (mục 5) ---

def test_tai_lieu_mat_gia_tri_vao_bang_chung_bi_loai_va_tuyen_bo_giu_nguyen(cac):
    tuyen_bo = "Buds B nghe nhạc lên đến 9 giờ"
    du = {"tuyen_bo": tb_muc(gia_tri=gt("9", "câu không có trong nguồn", "giờ")),
          "bang_chung": [tl_muc(f"{BUDS}#044", gt("7", "Lên đến 6", None)),                    # số sai
                         tl_muc(f"{BUDS}#044", gt("6", "Lên đến 6 phút bịa", "phút")),         # câu trích không có
                         tl_muc(f"{BUDS}#044", gt("6", "Thời gian phát nhạc (bật ANC)\nLên đến 6", "phút")),   # đơn vị sai
                         tl_muc("tn-b#099", gt("6", "Lên đến 6")),                             # ngoài top-k
                         tl_muc(f"{BUDS}#044", gt("6", "Thời gian phát nhạc (bật ANC)\nLên đến 6"))]}   # đạt
    ket = chay_xu_ly(du, tuyen_bo, doan_that("044"), cac)
    assert ket["tuyen_bo"]["gia_tri"] is None and ket["tuyen_bo"]["thuoc_tinh"] == "thoi_luong_pin"
    assert [b["ly_do"] for b in ket["bang_chung_bi_loai"]] == [["so_khong_khop"], ["trich_khong_co_trong_nguon"],
                                                              ["don_vi_khong_khop"], ["doan_ngoai_top_k"]]
    assert [m["gia_tri"] for m in ket["bang_chung"]] == [6.0]
    assert ly_do(ket, "gia_tri")[0] == ("tuyen_bo", None, "gia_tri", "trich_khong_co_trong_nguon")
    assert ("tai_lieu", 3, "muc", "doan_ngoai_top_k") in ly_do(ket)


def test_dieu_kien_bia_va_thuoc_tinh_ngoai_nhom(cac):
    du = {"tuyen_bo": tb_muc(thuoc_tinh="zoom", gia_tri=gt("9", "lên đến 9 giờ", "giờ")),
          "bang_chung": [tl_muc(f"{BUDS}#044", gt("6", "Lên đến 6"))]}
    ket = chay_xu_ly(du, "Buds B lên đến 9 giờ", doan_that("044"), cac)
    assert ket["tuyen_bo"]["thuoc_tinh"] is None
    assert ly_do(ket, "thuoc_tinh") == [("tuyen_bo", None, "thuoc_tinh", "thuoc_tinh_ngoai_nhom")]
    assert ket["bang_chung"] == [] and ket["bang_chung_bi_loai"][0]["ly_do"] == ["khong_co_thuoc_tinh"]
    du = {"tuyen_bo": tb_muc(gia_tri=gt("9", "lên đến 9 giờ", "giờ"),
                             dieu_kien=[dk("che_do_hoat_dong", "bật ANC", "lên đến 9 giờ")]), "bang_chung": []}
    ket = chay_xu_ly(du, "Buds B lên đến 9 giờ", doan_that("044"), cac)
    assert ly_do(ket, "dieu_kien[0]") == [("tuyen_bo", None, "dieu_kien[0]", "cum_khong_trong_trich")]
    assert "che_do_chong_on" not in ket["tuyen_bo"]["dieu_kien"]


# --- Hiểu điều kiện (mục 6) ---

def hieu(cac_dk, thuoc_tinh, cau_hinh, phia="tuyen_bo"):
    return tx.hieu_dieu_kien([{"i": i, **d} for i, d in enumerate(cac_dk)], thuoc_tinh, phia, cau_hinh)


def test_cum_khop_cau_hinh_thanh_dieu_kien_co_ma(tai_nghe):
    r = hieu([dk("che_do_hoat_dong", "bật chống ồn", "khi bật chống ồn"), dk("che_do_hoat_dong", "Thời gian phát nhạc")],
             "thoi_luong_pin", tai_nghe)
    assert r["dieu_kien"] == {"che_do_chong_on": "bat", "hoat_dong": "nghe_nhac"}
    assert r["nguon_dieu_kien"] == {"che_do_chong_on": "llm", "hoat_dong": "llm"}
    assert r["trich"] == {"dieu_kien.che_do_chong_on": "khi bật chống ồn", "dieu_kien.hoat_dong": "Thời gian phát nhạc"}
    assert r["dieu_kien_khac"] == [] and r["dieu_kien_phu"] == {}
    r = hieu([dk("che_do_hoat_dong", "Thời gian phát nhạc (bật ANC)")], "thoi_luong_pin", tai_nghe)    # một cụm, hai điều kiện
    assert r["dieu_kien"] == {"che_do_chong_on": "bat", "hoat_dong": "nghe_nhac"}


def test_cum_cua_thuoc_tinh_khac_vao_dieu_kien_phu(tai_nghe):
    r = hieu([dk("che_do_hoat_dong", "bật ANC")], "dung_luong_pin", tai_nghe)
    assert r["dieu_kien"] == {} and r["dieu_kien_phu"] == {"che_do_chong_on": "bat"} and r["dieu_kien_khac"] == []


def test_cum_ngu_canh_khong_la_dieu_kien(tai_nghe):
    r = hieu([dk("dieu_kien_do", "kết quả thực tế có thể khác"), dk("dieu_kien_do", "thử nghiệm trong phòng thí nghiệm")],
             "thoi_luong_pin", tai_nghe)
    assert r["ngu_canh"] == ["kết quả thực tế có thể khác", "thử nghiệm trong phòng thí nghiệm"]
    assert r["dieu_kien"] == {} and r["dieu_kien_khac"] == []


def test_cum_la_con_dieu_kien_khac(tai_nghe):
    r = hieu([dk("che_do_hoat_dong", "khi chơi game", "pin 9 giờ khi chơi game"), dk("phu_kien", "sạc ngược")], "thoi_luong_pin", tai_nghe)
    assert r["dieu_kien_khac"] == [{"loai": "che_do_hoat_dong", "cum": "khi chơi game", "trich": "pin 9 giờ khi chơi game"},
                                   {"loai": "phu_kien", "cum": "sạc ngược", "trich": "sạc ngược"}]
    assert r["dieu_kien"] == {}


def test_cum_khong_phai_dieu_kien_va_kieu_gia_tri(tai_nghe):
    r = hieu([dk("dieu_kien_do", "cả ngày"), dk("dieu_kien_do", "chỉ qua cáp"), dk("kieu_gia_tri", "lên đến"),
              dk("dieu_kien_do", "Tối đa"), dk("kieu_gia_tri", "một kiểu lạ")], "thoi_luong_pin", tai_nghe)
    assert r["bo_qua"] == ["cả ngày"]                                   # "chỉ dùng mạng di động" không trùng hẳn mục nào
    assert [c for c, _ in zip((x["cum"] for x in r["dieu_kien_khac"]), r["dieu_kien_khac"])] == ["chỉ qua cáp"]
    assert [c for _, c in r["cum_kieu"]] == ["lên đến", "Tối đa", "một kiểu lạ"]    # loai kieu_gia_tri hoặc trùng hẳn cụm kiểu
    assert r["dieu_kien"] == {}


def test_cum_sac_toi_khong_bi_nuot_nhu_kieu_ma_nhan_theo_don_vi(dien_thoai):
    # "sạc tới 50%" chứa "tới" (kiểu toi_da) nhưng không trùng hẳn; không khớp cụm cấu hình nên nhận theo đơn vị: % -> moc_phan_tram.
    r = hieu([dk("dieu_kien_do", "sạc tới 50%")], "sac_nhanh", dien_thoai)
    assert r["cum_kieu"] == [] and r["dieu_kien_khac"] == []
    assert r["dieu_kien"] == {"moc_phan_tram": {"so": 50.0, "don_vi": "phan_tram"}}
    assert r["nguon_dieu_kien"] == {"moc_phan_tram": "llm_don_vi"}


def test_phia_va_chi_thuoc_tinh(dien_thoai, tai_nghe):
    cum = dk("che_do_hoat_dong", "sử dụng liên tục")
    assert hieu([cum], "thoi_luong_pin", dien_thoai, "tuyen_bo")["dieu_kien"] == {"hoat_dong": "kem_thuan_loi_nhat".replace("kem_thuan_loi_nhat", "chua_ro_hoat_dong")}
    r = hieu([cum], "thoi_luong_pin", dien_thoai, "tai_lieu")
    assert r["dieu_kien"] == {"hoat_dong": "su_dung_lien_tuc"}          # phia tai_lieu: giá trị khác
    assert hieu([dk("che_do_hoat_dong", "dùng liên tục")], "thoi_luong_pin", dien_thoai, "tai_lieu")["dieu_kien_khac"]
    # kem_hop_sac chỉ cho thoi_luong_pin
    assert hieu([dk("bo_phan", "có kèm hộp sạc")], "thoi_luong_pin", tai_nghe)["dieu_kien"] == {"bo_phan": "kem_hop_sac"}
    assert hieu([dk("bo_phan", "có kèm hộp sạc")], "dung_luong_pin", tai_nghe)["dieu_kien"] == {"bo_phan": "hop_sac"}


def test_dieu_kien_dang_so(dien_thoai):
    r = hieu([dk("dieu_kien_do", "Sạc lên đến 50%"), dk("phu_kien", "bộ sạc 67W trở lên"),
              dk("phu_kien", "bộ sạc", "với bộ sạc 40W")], "sac_nhanh", dien_thoai)
    assert r["dieu_kien"]["moc_phan_tram"] == {"so": 50.0, "don_vi": "phan_tram"}
    assert r["xung_dot"] == {"bo_tiep_hop": [{"so": 67.0, "don_vi": "W"}, {"so": 40.0, "don_vi": "W"}]}   # hai số khác nhau
    r = hieu([dk("phu_kien", "bộ sạc", "sạc với bộ sạc 67W")], "sac_nhanh", dien_thoai)   # số ở câu trích khi cụm không có số
    assert r["dieu_kien"]["bo_tiep_hop"] == {"so": 67.0, "don_vi": "W"}


def test_dieu_kien_so_gia_tri_ngam_va_khong_doc_duoc(dien_thoai):
    r = hieu([dk("dieu_kien_do", "sạc đầy")], "sac_nhanh", dien_thoai)
    assert r["dieu_kien"] == {"moc_phan_tram": {"so": 100.0, "don_vi": "phan_tram"}}
    r = hieu([dk("dieu_kien_do", "toàn màn hình")], "do_sang", dien_thoai)
    assert r["dieu_kien"] == {"dien_tich_do": {"so": 100.0, "don_vi": "phan_tram"}}
    r = hieu([dk("phu_kien", "bộ sạc", "với bộ sạc rời")], "sac_nhanh", dien_thoai)
    assert r["dieu_kien"] == {}
    assert r["dieu_kien_khac"] == [{"loai": "phu_kien", "cum": "bộ sạc", "trich": "với bộ sạc rời", "ly_do": "khong_doc_duoc_so"}]


def test_xung_dot_hai_gia_tri_cung_dieu_kien(tai_nghe):
    r = hieu([dk("che_do_hoat_dong", "bật ANC và tắt ANC")], "thoi_luong_pin", tai_nghe)
    assert r["xung_dot"] == {"che_do_chong_on": ["bat", "tat"]} and r["dieu_kien"] == {}
    r = hieu([dk("che_do_hoat_dong", "bật ANC"), dk("che_do_hoat_dong", "tắt ANC")], "thoi_luong_pin", tai_nghe)
    assert r["xung_dot"] == {"che_do_chong_on": ["bat", "tat"]}
    r = hieu([dk("che_do_hoat_dong", "bật ANC"), dk("che_do_hoat_dong", "bật chống ồn")], "thoi_luong_pin", tai_nghe)
    assert r["dieu_kien"] == {"che_do_chong_on": "bat"} and r["xung_dot"] == {}     # cùng giá trị: không xung đột


# --- Kiểm tra đầy đủ (mục 7) ---

def test_dieu_kien_bi_bo_sot_duoc_bo_sung_o_tuyen_bo(cac):
    tuyen_bo = "Buds B nghe nhạc lên đến 9 giờ khi bật chống ồn"
    du = {"tuyen_bo": tb_muc(gia_tri=gt("9", "lên đến 9 giờ", "giờ")), "bang_chung": []}
    ket = chay_xu_ly(du, tuyen_bo, doan_that("044"), cac)
    assert ket["tuyen_bo"]["dieu_kien"] == {"che_do_chong_on": "bat", "hoat_dong": "nghe_nhac"}
    assert ket["tuyen_bo"]["nguon_dieu_kien"] == {"che_do_chong_on": "bo_sung", "hoat_dong": "bo_sung"}
    assert {(b["dieu_kien"], b["gia_tri"], b["cum"]) for b in ket["bo_sung"]} == {("che_do_chong_on", "bat", "bật chống ồn"),
                                                                                  ("hoat_dong", "nghe_nhac", "nghe nhạc")}
    assert ket["tuyen_bo"]["kieu_gia_tri"] == "toi_da"
    # Điều kiện LLM đã ghi không bị đổi.
    du["tuyen_bo"]["dieu_kien"] = [dk("che_do_hoat_dong", "tắt chống ồn", "tắt chống ồn")]
    ket = chay_xu_ly(du, "Buds B nghe nhạc lên đến 9 giờ khi tắt chống ồn, bật chống ồn", doan_that("044"), cac)
    assert ket["tuyen_bo"]["dieu_kien"]["che_do_chong_on"] == "tat" and "che_do_chong_on" not in {b["dieu_kien"] for b in ket["bo_sung"]}


NGUON_2_DONG = "Thời gian đàm thoại\nTắt ANC: Đến 9 giờ\nBật ANC: Đến 7 giờ"


def test_khong_do_ra_ngoai_dong_cua_gia_tri(cac):
    du = {"tuyen_bo": tb_muc(), "bang_chung": [tl_muc(f"{BUDS}#900", gt("7", "Bật ANC: Đến 7 giờ", "giờ"))]}
    ket = chay_xu_ly(du, "Buds B", [(f"{BUDS}#900", NGUON_2_DONG)], cac)
    m = ket["bang_chung"][0]
    assert m["dieu_kien"] == {"che_do_chong_on": "bat"}            # không thấy "Tắt ANC" và "đàm thoại" ở dòng khác
    assert ket["bo_sung_mo_ho"] == []
    assert m["trich"] == {"gia_tri": "Bật ANC: Đến 7 giờ"}


def test_hai_gia_tri_trong_dong_la_bo_sung_mo_ho(cac):
    du = {"tuyen_bo": tb_muc(), "bang_chung": [tl_muc(f"{BUDS}#900", gt("8", "Bật ANC / Tắt ANC: 8 giờ", "giờ"))]}
    ket = chay_xu_ly(du, "Buds B", [(f"{BUDS}#900", "Thời gian phát\nBật ANC / Tắt ANC: 8 giờ")], cac)
    assert "che_do_chong_on" not in ket["bang_chung"][0]["dieu_kien"]
    assert [(b["dieu_kien"], b["gia_tri"], b["chi_so"]) for b in ket["bo_sung_mo_ho"]] == [("che_do_chong_on", ["bat", "tat"], 0)]
    assert ket["bo_sung"] == []


def test_cap_so_gach_cheo_042_dieu_ra_bo_phan(cac):
    doan = doan_that("042")
    du = {"tuyen_bo": tb_muc(), "bang_chung": [tl_muc(doan[0][0], gt("7", "Đến 7,0/30 giờ", "giờ")),
                                              tl_muc(doan[0][0], gt("30", "Đến 7,0/30 giờ", "giờ")),
                                              tl_muc(doan[0][0], gt("6", "Đến 6,0/26 giờ", "giờ"))]}
    ket = chay_xu_ly(du, "Buds B", doan, cac)
    assert [m["dieu_kien"].get("bo_phan") for m in ket["bang_chung"]] == ["tai_nghe", "kem_hop_sac", "tai_nghe"]
    assert [m["gia_tri"] for m in ket["bang_chung"]] == [7.0, 30.0, 6.0]
    assert {(b["dieu_kien"], b["cum"]) for b in ket["bo_sung"]} == {("bo_phan", "Đến 7,0/30 giờ"[4:]), ("bo_phan", "6,0/26 giờ")}
    assert all(m["kieu_gia_tri"] == "toi_da" and m["cum_kieu"] == "đến" for m in ket["bang_chung"])
    assert all(m["nguon_dieu_kien"]["bo_phan"] == "bo_sung" for m in ket["bang_chung"])


def test_cap_so_khong_ghi_de_bo_phan_cua_llm_va_dung_a_nho_hon_b(cac):
    doan = doan_that("042")
    du = {"tuyen_bo": tb_muc(), "bang_chung": [tl_muc(doan[0][0], gt("30", "Đến 7,0/30 giờ", "giờ"),
                                                      [dk("bo_phan", "hộp sạc", "Đến 7,0/30 giờ hộp sạc")]) | {}]}
    ket = chay_xu_ly(du, "Buds B", [(doan[0][0], doan[0][1] + "\nĐến 7,0/30 giờ hộp sạc")], cac)
    assert ket["bang_chung"][0]["dieu_kien"]["bo_phan"] == "hop_sac" and ket["bo_sung"] == []
    ket = chay_xu_ly({"tuyen_bo": tb_muc(), "bang_chung": [tl_muc("x#1", gt("30", "Đến 30 / 7 giờ", "giờ"))]},
                     "Buds B", [("x#1", "Đến 30 / 7 giờ")], cac)
    assert "bo_phan" not in ket["bang_chung"][0]["dieu_kien"]             # a >= b: không áp luật


def test_kieu_gia_tri_chi_khi_dung_lien_con_so(cac):
    tuyen_bo = "Buds B lên đến 30 giờ nhưng chỉ nghe 8 giờ"
    du = {"tuyen_bo": tb_muc(gia_tri=gt("8", "nghe 8 giờ", "giờ"), dieu_kien=[dk("kieu_gia_tri", "lên đến", "lên đến 30 giờ")]),
          "bang_chung": []}
    ket = chay_xu_ly(du, tuyen_bo, doan_that("044"), cac)
    assert ket["tuyen_bo"]["kieu_gia_tri"] == "khong_neu" and ket["tuyen_bo"]["cum_kieu"] is None
    assert ly_do(ket, "dieu_kien[0]") == [("tuyen_bo", None, "dieu_kien[0]", "kieu_khong_gan_so")]
    du["tuyen_bo"] = tb_muc(gia_tri=gt("30", "lên đến 30 giờ", "giờ"), dieu_kien=[dk("kieu_gia_tri", "lên đến", "lên đến 30 giờ")])
    ket = chay_xu_ly(du, tuyen_bo, doan_that("044"), cac)
    assert ket["tuyen_bo"]["kieu_gia_tri"] == "toi_da" and ket["tuyen_bo"]["cum_kieu"] == "lên đến"
    assert ly_do(ket, "dieu_kien[0]") == []


def test_kieu_khang_dinh_va_ten_tinh_nang(cac):
    du = {"tuyen_bo": tb_muc(gia_tri=gt("9", "luôn đạt 9 giờ", "giờ")), "bang_chung": []}
    assert chay_xu_ly(du, "Buds B luôn đạt 9 giờ", [], cac)["tuyen_bo"]["kieu_gia_tri"] == "khang_dinh"


def test_khac_san_pham(cac):
    nguon = "So sánh\nGalaxy Buds3 | Lên đến 6 giờ\nGalaxy Buds3 Pro | Lên đến 7 giờ\nSản phẩm lạ | Lên đến 8 giờ"
    du = {"tuyen_bo": tb_muc(), "bang_chung": [
        tl_muc(f"{BUDS}#900", gt("6", "Galaxy Buds3 | Lên đến 6 giờ", "giờ"), san_pham={"chu": "Galaxy Buds3", "trich": "Galaxy Buds3"}),
        tl_muc(f"{BUDS}#900", gt("7", "Galaxy Buds3 Pro | Lên đến 7 giờ", "giờ"), san_pham={"chu": "Galaxy Buds3 Pro", "trich": "Galaxy Buds3 Pro"}),
        tl_muc(f"{BUDS}#900", gt("8", "Sản phẩm lạ | Lên đến 8 giờ", "giờ"), san_pham={"chu": "Sản phẩm lạ", "trich": "Sản phẩm lạ"}),
        tl_muc(f"{BUDS}#900", gt("6", "Galaxy Buds3 | Lên đến 6 giờ", "giờ"))]}
    ket = chay_xu_ly(du, "Galaxy Buds3 Pro có pin lên đến 7 giờ", [(f"{BUDS}#900", nguon)], cac)
    assert [(m["san_pham_ma"], m["khac_san_pham"]) for m in ket["bang_chung"]] == [(None, True), (BUDS, False), (None, True), (BUDS, False)]
    assert ket["tuyen_bo"]["san_pham_ma"] == BUDS


# --- P−NN, tất định, bay_truong ---

def test_p_tru_nn_khong_bo_khong_dien(cac):
    tuyen_bo = "Buds B nghe nhạc lên đến 9 giờ khi bật chống ồn"
    du = {"tuyen_bo": tb_muc(gia_tri=gt("9", "câu bịa", "phút"), dieu_kien=[dk("che_do_hoat_dong", "tắt ANC", "câu bịa"),
                                                                           dk("kieu_gia_tri", "tối đa", "câu bịa")],
                             san_pham={"chu": "Buds B", "trich": "câu bịa"}),
          "bang_chung": [tl_muc("tn-b#099", gt("6", "Bật ANC: Đến 6 giờ"), [dk("che_do_hoat_dong", "bật ANC")])]}
    ket = chay_xu_ly(du, tuyen_bo, doan_that("044"), cac, neo_nguon=False, kiem_day_du=False)
    tb = ket["tuyen_bo"]
    assert tb["gia_tri"] == 9.0 and tb["don_vi"] == "phut"                       # lấy thẳng doc_so(chu), không bỏ vì trích bịa
    assert tb["dieu_kien"] == {"che_do_chong_on": "tat"} and tb["nguon_dieu_kien"] == {"che_do_chong_on": "llm"}   # không điền bật/nghe nhạc
    assert (tb["kieu_gia_tri"], tb["cum_kieu"], tb["goi_muc_cao"]) == ("toi_da", "tối đa", True)   # theo cụm LLM ghi
    assert ket["bo_sung"] == [] and ket["bo_sung_mo_ho"] == [] and tb["san_pham_ma"] is None
    assert [m["ma_doan"] for m in ket["bang_chung"]] == ["tn-b#099"]             # ma_doan ngoài top-k không bị bỏ ở P−NN
    assert [b["ly_do"] for b in ket["bi_loai"]] == []
    ket_day_du = chay_xu_ly(du, tuyen_bo, doan_that("044"), cac)
    assert ket_day_du["tuyen_bo"]["gia_tri"] is None and ket_day_du["bang_chung"] == []


def test_xu_ly_tat_dinh_va_khong_sua_dau_vao(cac):
    doan = doan_that("038", "044")
    du = {"tuyen_bo": tb_muc(gia_tri=gt("7", "tối đa 7 giờ", "giờ"), dieu_kien=[dk("che_do_hoat_dong", "bật ANC")]),
          "bang_chung": [tl_muc(doan[0][0], gt("7", "Tắt Tính năng ANC Đến 7 / 30 giờ", "giờ"))]}
    goc = copy.deepcopy(du)
    a = chay_xu_ly(du, "Galaxy Buds3 Pro tối đa 7 giờ khi bật ANC", doan, cac)
    b = chay_xu_ly(du, "Galaxy Buds3 Pro tối đa 7 giờ khi bật ANC", doan, cac)
    assert du == goc and json.dumps(a, ensure_ascii=False) == json.dumps(b, ensure_ascii=False)


def test_bay_truong(cac):
    du = {"tuyen_bo": tb_muc(), "bang_chung": [tl_muc(f"{BUDS}#044", gt("6", "Thời gian phát nhạc (bật ANC)\nLên đến 6"),
                                                      [dk("che_do_hoat_dong", "bật ANC", "Thời gian phát nhạc (bật ANC)")])]}
    ket = chay_xu_ly(du, "Buds B", doan_that("044"), cac)
    muc = ket["bang_chung"][0]
    assert muc["gia_tri"] == 6.0 and muc["don_vi"] == "gio" and muc["kieu_gia_tri"] == "toi_da" and muc["cum_kieu"] == "lên đến"
    assert muc["dieu_kien"] == {"che_do_chong_on": "bat", "hoat_dong": "nghe_nhac"}
    assert muc["trich"] == {"gia_tri": "Thời gian phát nhạc (bật ANC)\nLên đến 6",
                            "dieu_kien.che_do_chong_on": "Thời gian phát nhạc (bật ANC)"}
    muc["dieu_kien"]["bo_phan"] = "tai_nghe"
    muc["dieu_kien"]["phien_ban"] = "gps"
    bay = tx.bay_truong(muc)
    assert bay == {"san_pham": BUDS, "phien_ban": "gps", "bo_phan": "tai_nghe", "thuoc_tinh": "thoi_luong_pin", "gia_tri": 6.0,
                   "don_vi": "gio", "dieu_kien": {"che_do_chong_on": "bat", "hoat_dong": "nghe_nhac"}, "kieu_gia_tri": "toi_da",
                   "trich": muc["trich"]}


def test_khang_nuoc_ip_phu_dinh_va_co(cac):
    nguon = "Chuẩn IP57\nHộp sạc không có khả năng kháng nước\nTai nghe cũng kháng nước"
    du = {"tuyen_bo": tb_muc("khang_nuoc", gt("có", "cũng kháng nước"), [dk("bo_phan", "Hộp sạc", "Hộp sạc Galaxy Buds3 Pro")]),
          "bang_chung": [tl_muc(f"{BUDS}#901", gt("IP57", "Chuẩn IP57")),
                         tl_muc(f"{BUDS}#901", gt("không", "Hộp sạc không có khả năng kháng nước"),
                                [dk("bo_phan", "Hộp sạc", "Hộp sạc không có khả năng kháng nước")]),
                         tl_muc(f"{BUDS}#901", gt("", "Tai nghe cũng kháng nước"))]}
    ket = chay_xu_ly(du, "Hộp sạc Galaxy Buds3 Pro cũng kháng nước", [(f"{BUDS}#901", nguon)], cac)
    assert ket["tuyen_bo"]["gia_tri"] == "co" and ket["tuyen_bo"]["dieu_kien"] == {"bo_phan": "hop_sac"}
    assert [m["gia_tri"] for m in ket["bang_chung"]] == [{"bui": 5, "nuoc": 7}, "khong", "co"]
    assert ket["bang_chung"][1]["dieu_kien"] == {"bo_phan": "hop_sac"}
    assert ket["bang_chung"][0]["kieu_gia_tri"] is None


# --- Gọi LLM (LLM giả) ---

def thu_tuyen_bo(ma):
    with open(GOC / "data" / "tuyen_bo" / "thu.jsonl", encoding="utf-8") as f:
        return next(json.loads(d) for d in f if json.loads(d)["id"] == ma)


def trich_tu_tb40():
    """Đầu ra 'LLM' cho tb-00040 trên đoạn thật #038 (chữ dọc), #044 (dòng không đơn vị, nhãn ở dòng trên), #042."""
    return {"tuyen_bo": {"san_pham": {"chu": "Galaxy Buds3 Pro", "trich": "Galaxy Buds3 Pro"}, "thuoc_tinh": "thoi_luong_pin",
                         "gia_tri": gt("7", "tối đa 7 giờ", "giờ"),
                         "dieu_kien": [dk("kieu_gia_tri", "tối đa", "tối đa 7 giờ"), dk("che_do_hoat_dong", "nghe nhạc", "khi nghe nhạc"),
                                       dk("dieu_kien_do", "suốt cả ngày", "suốt cả ngày"), dk("bo_phan", "tai nghe", "trên tai nghe")]},
            "bang_chung": [
                tl_muc(f"{BUDS}#038", gt("7", "Tắt Tính năng ANC\nĐến\n7\n/\n30\ngiờ", "giờ"),
                       [dk("che_do_hoat_dong", "Thời gian phát", "Thời gian phát"), dk("che_do_hoat_dong", "Tắt Tính năng ANC", "Tắt Tính năng ANC")]),
                tl_muc(f"{BUDS}#038", gt("30", "Tắt Tính năng ANC\nĐến\n7\n/\n30\ngiờ", "giờ"),
                       [dk("che_do_hoat_dong", "Thời gian phát", "Thời gian phát"), dk("che_do_hoat_dong", "Tắt Tính năng ANC", "Tắt Tính năng ANC")]),
                tl_muc(f"{BUDS}#044", gt("6", "Thời gian phát nhạc (bật ANC)\nLên đến 6", None),
                       [dk("che_do_hoat_dong", "bật ANC", "Thời gian phát nhạc (bật ANC)"),
                        dk("che_do_hoat_dong", "Thời gian phát nhạc", "Thời gian phát nhạc (bật ANC)")]),
                tl_muc(f"{BUDS}#044", gt("26", "Tổng thời gian phát nhạc (Giờ, bật ANC)\nLên đến 26", "giờ"),
                       [dk("bo_phan", "Tổng thời gian", "Tổng thời gian phát nhạc (Giờ, bật ANC)"),
                        dk("che_do_hoat_dong", "bật ANC", "Tổng thời gian phát nhạc (Giờ, bật ANC)")]),
                tl_muc(f"{BUDS}#042", gt("7,0", "Đến 7,0/30 giờ", "giờ"), [dk("che_do_hoat_dong", "Tính năng ANC Tắt", "(Tính năng ANC Tắt)")])]}


def client_gia(tmp_path, noi_dung, dem=None):
    def transport(request, timeout_s):
        if dem is not None:
            dem.append(1)
        if isinstance(noi_dung, Exception):
            raise noi_dung
        return LLMResult(noi_dung if isinstance(noi_dung, str) else json.dumps(noi_dung, ensure_ascii=False), request["provider"],
                         request["model"], "gia-lap", {"total": 1}, "stop")
    return LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=transport)


def test_dau_cuoi_tren_tuyen_bo_va_doan_that_cua_buds3_pro(tmp_path):
    tb = thu_tuyen_bo("tb-00040")
    assert tb["tuyen_bo"] == "Galaxy Buds3 Pro có thời gian phát tối đa 7 giờ khi nghe nhạc suốt cả ngày trên tai nghe"
    bg = tx.trich_xuat(tb, tb["ma_mau"], client_gia(tmp_path, trich_tu_tb40()), MODEL)
    assert bg["loi"] is None and bg["id"] == "tb-00040" and bg["neo_nguon"] and bg["kiem_day_du"]
    assert f"{BUDS}#038" in bg["doan"] and f"{BUDS}#044" in bg["doan"] and f"{BUDS}#042" in bg["doan"]
    assert len(bg["ma_bam_cau_lenh"]) == 64 and bg["bi_loai"] == [] and bg["bo_sung_mo_ho"] == []
    tuyen = bg["tuyen_bo"]
    assert tuyen["gia_tri"] == 7.0 and tuyen["don_vi"] == "gio" and tuyen["kieu_gia_tri"] == "toi_da" and tuyen["goi_muc_cao"]
    assert tuyen["dieu_kien"] == {"hoat_dong": "nghe_nhac", "bo_phan": "tai_nghe", "che_do_chong_on": "bat"} or \
        tuyen["dieu_kien"] == {"hoat_dong": "nghe_nhac", "bo_phan": "tai_nghe"}
    assert tuyen["bo_qua"] == ["suốt cả ngày"] and tuyen["san_pham_ma"] == BUDS
    m038a, m038b, m044, m044_tong, m042 = bg["bang_chung"]
    # Cặp số gạch chéo của chữ dọc #038: cả 7 và 30 đạt neo nguồn; a nhỏ là tai nghe, b lớn là tổng kèm hộp sạc.
    assert (m038a["gia_tri"], m038b["gia_tri"]) == (7.0, 30.0)
    assert (m038a["dieu_kien"]["bo_phan"], m038b["dieu_kien"]["bo_phan"]) == ("tai_nghe", "kem_hop_sac")
    assert m038a["dieu_kien"]["che_do_chong_on"] == m038b["dieu_kien"]["che_do_chong_on"] == "tat"
    assert m038a["dieu_kien"]["hoat_dong"] == "nghe_nhac" and m038a["kieu_gia_tri"] == "toi_da"
    # Dòng không đơn vị #044, điều kiện ở nhãn dòng.
    assert (m044["gia_tri"], m044["don_vi"]) == (6.0, "gio")
    assert m044["dieu_kien"] == {"che_do_chong_on": "bat", "hoat_dong": "nghe_nhac"} and m044["kieu_gia_tri"] == "toi_da"
    assert m044["cum_kieu"] == "lên đến" and m044["nguon_dieu_kien"]["hoat_dong"] == "llm"
    assert m044_tong["dieu_kien"]["bo_phan"] == "kem_hop_sac" and m044_tong["dieu_kien"]["che_do_chong_on"] == "bat"
    # Dạng "a,b/c giờ" không dấu cách của #042.
    assert m042["gia_tri"] == 7.0 and m042["dieu_kien"]["bo_phan"] == "tai_nghe" and m042["dieu_kien"]["che_do_chong_on"] == "tat"
    assert tx.bay_truong(m038b)["bo_phan"] == "kem_hop_sac" and tx.bay_truong(m038b)["san_pham"] == BUDS
    assert bg["bang_chung_bi_loai"] == []


def test_chay_lai_dung_bo_nho_dem_va_tat_dinh(tmp_path):
    tb = thu_tuyen_bo("tb-00040")
    dem = []
    client = client_gia(tmp_path, trich_tu_tb40(), dem)
    a = tx.trich_xuat(tb, tb["ma_mau"], client, MODEL)
    b = tx.trich_xuat(tb, tb["ma_mau"], client, MODEL)
    assert len(dem) == 1 and a["tu_bo_nho_dem"] is False and b["tu_bo_nho_dem"] is True
    a.pop("tu_bo_nho_dem"), b.pop("tu_bo_nho_dem")
    assert json.dumps(a, ensure_ascii=False) == json.dumps(b, ensure_ascii=False)
    # P−NN dùng cùng đầu ra LLM (cùng câu lệnh, cùng bộ nhớ đệm), khác biệt chỉ do hai khâu kiểm.
    c = tx.trich_xuat(tb, tb["ma_mau"], client, MODEL, neo_nguon=False, kiem_day_du=False)
    assert len(dem) == 1 and c["tra_ve_tho"] == a["tra_ve_tho"] and c["ma_bam_cau_lenh"] == a["ma_bam_cau_lenh"]
    assert c["neo_nguon"] is False and c["kiem_day_du"] is False and c["bo_sung"] == []
    assert "bo_phan" not in c["bang_chung"][1]["dieu_kien"]


def test_json_hong_thanh_loi_va_loi_llm(tmp_path):
    tb = thu_tuyen_bo("tb-00040")
    bg = tx.trich_xuat(tb, tb["ma_mau"], client_gia(tmp_path / "a", "không phải JSON"), MODEL)
    assert bg["loi"].startswith("json_khong_doc_duoc") and bg["tuyen_bo"] is None and bg["tra_ve_tho"] == "không phải JSON"
    bg = tx.trich_xuat(tb, tb["ma_mau"], client_gia(tmp_path / "b", "[1, 2]"), MODEL)
    assert bg["loi"].startswith("json_khong_phai_doi_tuong")
    bg = tx.trich_xuat(tb, tb["ma_mau"], client_gia(tmp_path / "c", "```json\n" + json.dumps({"tuyen_bo": {}, "bang_chung": []}) + "\n```"), MODEL)
    assert bg["loi"] is None and bg["tuyen_bo"]["gia_tri"] is None            # khối ```json đọc được
    bg = tx.trich_xuat(tb, tb["ma_mau"], client_gia(tmp_path / "d", "  "), MODEL)
    assert bg["loi"] == "llm_khong_tra_ve_dung: empty_blocked_or_incomplete_response"
    with pytest.raises(LLMError):
        tx.trich_xuat(tb, tb["ma_mau"], client_gia(tmp_path / "e", LLMError("quota", retryable=False)), MODEL)
    with pytest.raises(ValueError):
        tx.trich_xuat(tb, tb["ma_mau"], client_gia(tmp_path / "f", "{}"), "mo-hinh-la")


def test_trich_xuat_nhan_chu_tuyen_bo(tmp_path):
    bg = tx.trich_xuat("Galaxy Buds3 Pro pin 7 giờ", BUDS, client_gia(tmp_path, trich_tu_tb40()), MODEL)
    assert bg["id"] is None and bg["chu_tuyen_bo"] == "Galaxy Buds3 Pro pin 7 giờ"
    assert len(bg["doan"]) == 5


# --- LLM giả của script và script ---

def test_gia_transport_chay_het_cac_dang_phan_hoi(tmp_path):
    client = LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=tx.gia_transport)
    loi, ok = set(), 0
    with open(GOC / "data" / "tuyen_bo" / "thu.jsonl", encoding="utf-8") as f:
        for dong in f:
            tb = json.loads(dong)
            bg = tx.trich_xuat(tb, tb["ma_mau"], client, MODEL)
            loi.add((bg["loi"] or "ok").split(":")[0])
            ok += bg["loi"] is None
    assert loi == {"ok", "json_khong_doc_duoc"} and ok > 40


def test_script_chay_gia_ghi_tep_va_chay_lai_giong_tung_byte(tmp_path, capsys):
    ra = tmp_path / "trich_xuat"
    argv = ["--gia", "--thu-muc-ra", str(ra), "--ma-mau", BUDS]
    assert chay.main(argv) == 0
    thu_muc = tmp_path / "trich_xuat_gia"
    ten = "thu_gemini-3.6-flash_k5_am_tiet_gia"
    jsonl, md = thu_muc / f"{ten}.jsonl", thu_muc / f"thong_ke_{ten}.md"
    assert jsonl.exists() and md.exists() and not ra.exists()
    ban_ghi = [json.loads(d) for d in jsonl.read_text(encoding="utf-8").splitlines()]
    assert len(ban_ghi) == 31 and all(b["ma_mau"] == BUDS and "tu_bo_nho_dem" not in b for b in ban_ghi)
    thong_ke = md.read_text(encoding="utf-8")
    assert thong_ke.startswith("**CHẠY GIẢ") and "Số tuyên bố: 31" in thong_ke and "khớp thuoc_tinh tách tay" in thong_ke
    truoc = (jsonl.read_bytes(), md.read_bytes())
    assert chay.main(argv) == 0
    assert (jsonl.read_bytes(), md.read_bytes()) == truoc


def test_script_ten_tep_theo_co(tmp_path):
    assert chay.ten_ket_qua("data/tuyen_bo/thu.jsonl", "openai/gpt-oss-120b", 8, "tu", False, False, False) == \
        "thu_openai_gpt-oss-120b_k8_tu_khong_neo_nguon_khong_day_du"
    assert chay.ten_ket_qua("thu.jsonl", MODEL, 5, "am_tiet", True, False, True) == "thu_gemini-3.6-flash_k5_am_tiet_khong_day_du_gia"
    assert chay.main(["--gia", "--thu-muc-ra", str(tmp_path / "x"), "--ma-mau", "dt-apple-iphone17", "--khong-neo-nguon",
                      "--khong-kiem-day-du", "--k", "3"]) == 0
    assert (tmp_path / "x_gia" / "thu_gemini-3.6-flash_k3_am_tiet_khong_neo_nguon_khong_day_du_gia.jsonl").exists()


# --- Điều kiện dạng số nhận theo đơn vị (bổ sung 08/11 khi cài) ---

def test_dieu_kien_so_theo_don_vi_cua_cau_hinh(dien_thoai, tai_nghe):
    def tt(c, t):
        return c["thuoc_tinh"][t]

    assert tx.dieu_kien_so_theo_don_vi(tt(dien_thoai, "sac_nhanh")) == {"W": "bo_tiep_hop", "phan_tram": "moc_phan_tram"}
    assert tx.dieu_kien_so_theo_don_vi(tt(dien_thoai, "khang_nuoc")) == {"m": "do_sau", "phut": "thoi_gian_ngam", "K": "chenh_lech_nhiet_do"}
    assert tx.dieu_kien_so_theo_don_vi(tt(dien_thoai, "do_sang")) == {"phan_tram": "dien_tich_do"}
    dong_ho = tx.lay_cau_hinh("dong_ho")
    assert tx.dieu_kien_so_theo_don_vi(tt(dong_ho, "sac_nhanh")) == {"W": "bo_tiep_hop", "phan_tram": "moc_phan_tram", "phut": "so_phut_sac"}
    assert tx.dieu_kien_so_theo_don_vi(tt(dien_thoai, "thoi_luong_pin")) == {}
    assert tx.dieu_kien_so_theo_don_vi(tt(tai_nghe, "khang_nuoc")) == {"m": "do_sau", "phut": "thoi_gian_ngam"}
    # hai điều kiện cùng đơn vị thì không áp; điều kiện không thuộc phu_kien/dieu_kien_do thì không áp
    gia = {"dieu_kien_bat_buoc": {"a": "dieu_kien_do", "b": "dieu_kien_do", "c": "che_do_hoat_dong"},
           "dieu_kien_so": {"a": {"don_vi": "m"}, "b": {"don_vi": "m"}, "c": {"don_vi": "W"}}}
    assert tx.dieu_kien_so_theo_don_vi(gia) == {}


def test_hieu_dieu_kien_nhan_theo_don_vi(dien_thoai):
    r = hieu([dk("dieu_kien_do", "sạc 50% trong 25 phút với củ 45W")], "sac_nhanh", dien_thoai)
    assert r["dieu_kien"] == {"moc_phan_tram": {"so": 50.0, "don_vi": "phan_tram"}, "bo_tiep_hop": {"so": 45.0, "don_vi": "W"}}
    assert set(r["nguon_dieu_kien"].values()) == {"llm_don_vi"}      # phút không phải điều kiện của sac_nhanh điện thoại
    r = hieu([dk("dieu_kien_do", "sạc 50% hoặc 80%")], "sac_nhanh", dien_thoai)
    assert r["dieu_kien"] == {} and list(r["xung_dot"]) == ["moc_phan_tram"]
    r = hieu([dk("dieu_kien_do", "Sạc lên đến 50%")], "sac_nhanh", dien_thoai)     # khớp cụm cấu hình: nguồn "llm"
    assert r["nguon_dieu_kien"] == {"moc_phan_tram": "llm"}
    r = hieu([dk("dieu_kien_do", "ở mức 50%")], "thoi_luong_pin", dien_thoai)       # thuộc tính không có điều kiện dạng số
    assert r["dieu_kien"] == {} and [d["cum"] for d in r["dieu_kien_khac"]] == ["ở mức 50%"]
    r = tx.hieu_dieu_kien([{"i": 0, **dk("dieu_kien_do", "sạc 50% trong 45 phút")}], "sac_nhanh", "tuyen_bo",
                          tx.lay_cau_hinh("dong_ho"), (45.0, "phut"))
    assert r["dieu_kien"] == {"moc_phan_tram": {"so": 50.0, "don_vi": "phan_tram"}}   # 45 phút là giá trị của mục


def test_tuyen_bo_dien_thoai_a_llm_ghi_du(cac):
    tb = "Điện thoại A sạc 50% trong 25 phút với củ sạc 45W"
    du = {"tuyen_bo": tb_muc("sac_nhanh", gt("25", "trong 25 phút", "phút"),
                             [dk("dieu_kien_do", "sạc 50%"), dk("phu_kien", "củ sạc 45W", "với củ sạc 45W")]), "bang_chung": []}
    t = chay_xu_ly(du, tb, doan_that("044"), cac, ma_mau="dt-apple-iphone17", nhom="dien_thoai")["tuyen_bo"]
    assert t["dieu_kien"] == {"moc_phan_tram": {"so": 50.0, "don_vi": "phan_tram"}, "bo_tiep_hop": {"so": 45.0, "don_vi": "W"}}
    assert t["nguon_dieu_kien"] == {"moc_phan_tram": "llm_don_vi", "bo_tiep_hop": "llm"} and t["dieu_kien_khac"] == []
    assert (t["gia_tri"], t["don_vi"]) == (25.0, "phut")


def test_tuyen_bo_dien_thoai_a_llm_bo_sot_ca_hai(cac):
    tb = "Điện thoại A sạc 50% trong 25 phút với củ sạc 45W"
    du = {"tuyen_bo": tb_muc("sac_nhanh", gt("25", "trong 25 phút", "phút")), "bang_chung": []}
    ket = chay_xu_ly(du, tb, doan_that("044"), cac, ma_mau="dt-apple-iphone17", nhom="dien_thoai")
    t = ket["tuyen_bo"]
    assert t["dieu_kien"] == {"moc_phan_tram": {"so": 50.0, "don_vi": "phan_tram"}, "bo_tiep_hop": {"so": 45.0, "don_vi": "W"}}
    assert t["nguon_dieu_kien"] == {"moc_phan_tram": "bo_sung", "bo_tiep_hop": "bo_sung"}
    assert {(b["dieu_kien"], b["cum"]) for b in ket["bo_sung"]} == {("moc_phan_tram", "50%"), ("bo_tiep_hop", "củ sạc")}
    assert ket["bo_sung_mo_ho"] == []      # 25 phút là giá trị, phút không phải điều kiện của sac_nhanh điện thoại


IPHONE = "dt-apple-iphone17"


def test_dong_tai_lieu_iphone17_sac_nhanh(cac):
    dong = "Sạc lên đến 50% trong khoảng 20 phút với bộ tiếp hợp 40W trở lên"
    nguon = "Sạc nhanh\n" + dong + "\nSạc nhanh 100% mất 90 phút"
    du = {"tuyen_bo": tb_muc("sac_nhanh"), "bang_chung": [tl_muc(f"{IPHONE}#900", gt("20", dong, "phút"), [dk("kieu_gia_tri", "lên đến", dong)]),
                                                         tl_muc(f"{IPHONE}#900", gt("20", dong, "phút"))]}
    ket = chay_xu_ly(du, "iPhone 17 sạc 50% trong 20 phút", [(f"{IPHONE}#900", nguon)], cac, ma_mau=IPHONE, nhom="dien_thoai")
    for m in ket["bang_chung"]:
        assert m["dieu_kien"] == {"moc_phan_tram": {"so": 50.0, "don_vi": "phan_tram"}, "bo_tiep_hop": {"so": 40.0, "don_vi": "W"}}
        assert m["gia_tri"] == 20.0 and m["kieu_gia_tri"] == "khong_neu"     # "lên đến" đứng liền 50%, không liền 20
    assert ly_do(ket, "dieu_kien[0]") == [("tai_lieu", 0, "dieu_kien[0]", "kieu_khong_gan_so")]
    assert ket["bo_sung_mo_ho"] == []          # "100% / 90 phút" ở dòng khác không bị dò


def test_dong_co_hai_so_cung_don_vi_la_bo_sung_mo_ho(cac):
    dong = "Sạc tới 50% hoặc 80% trong 30 phút"
    du = {"tuyen_bo": tb_muc("sac_nhanh"), "bang_chung": [tl_muc(f"{IPHONE}#900", gt("30", dong, "phút"))]}
    ket = chay_xu_ly(du, "iPhone 17 sạc", [(f"{IPHONE}#900", dong)], cac, ma_mau=IPHONE, nhom="dien_thoai")
    assert "moc_phan_tram" not in ket["bang_chung"][0]["dieu_kien"]
    assert [(b["dieu_kien"], b["gia_tri"]) for b in ket["bo_sung_mo_ho"]] == [
        ("moc_phan_tram", [{"so": 50.0, "don_vi": "phan_tram"}, {"so": 80.0, "don_vi": "phan_tram"}])]


def test_khang_nuoc_ip68_do_sau_va_thoi_gian(cac):
    tb = "iPhone 17 IP68 ở độ sâu 6 mét trong 30 phút"
    du = {"tuyen_bo": tb_muc("khang_nuoc", gt("IP68", "IP68")), "bang_chung": []}
    t = chay_xu_ly(du, tb, [], cac, ma_mau=IPHONE, nhom="dien_thoai")["tuyen_bo"]
    assert t["gia_tri"] == {"bui": 6, "nuoc": 8} and t["kieu_gia_tri"] is None
    assert t["dieu_kien"] == {"do_sau": {"so": 6.0, "don_vi": "m"}, "thoi_gian_ngam": {"so": 30.0, "don_vi": "phut"}}
    assert t["nguon_dieu_kien"] == {"do_sau": "bo_sung", "thoi_gian_ngam": "bo_sung"}
    du = {"tuyen_bo": tb_muc("khang_nuoc", gt("IP68", "IP68"), [dk("dieu_kien_do", "độ sâu 6 mét"), dk("dieu_kien_do", "30 phút")]),
          "bang_chung": []}
    t = chay_xu_ly(du, tb, [], cac, ma_mau=IPHONE, nhom="dien_thoai")["tuyen_bo"]
    assert t["dieu_kien"] == {"do_sau": {"so": 6.0, "don_vi": "m"}, "thoi_gian_ngam": {"so": 30.0, "don_vi": "phut"}}
    assert t["nguon_dieu_kien"] == {"do_sau": "llm_don_vi", "thoi_gian_ngam": "llm_don_vi"} and t["dieu_kien_khac"] == []


def test_dong_ho_sac_nhanh_dang_1_45_phut_la_gia_tri_khong_thanh_so_phut_sac(cac):
    tb = "Watch A sạc 80% trong 45 phút"
    du = {"tuyen_bo": tb_muc("sac_nhanh", gt("45", "trong 45 phút", "phút")), "bang_chung": []}
    t = chay_xu_ly(du, tb, [], cac, ma_mau="dh-apple-watchse3", nhom="dong_ho")["tuyen_bo"]
    assert t["dieu_kien"] == {"moc_phan_tram": {"so": 80.0, "don_vi": "phan_tram"}}
    du = {"tuyen_bo": tb_muc("sac_nhanh", gt("45", "trong 45 phút", "phút"), [dk("dieu_kien_do", "sạc 80% trong 45 phút")]),
          "bang_chung": []}
    t = chay_xu_ly(du, tb, [], cac, ma_mau="dh-apple-watchse3", nhom="dong_ho")["tuyen_bo"]
    assert t["dieu_kien"] == {"moc_phan_tram": {"so": 80.0, "don_vi": "phan_tram"}}     # 45 phút là giá trị của mục


def test_dong_ho_sac_nhanh_dang_2_sac_8_phut_dung_8_gio(cac):
    tb = "Watch A sạc 8 phút dùng 8 giờ"
    du = {"tuyen_bo": tb_muc("sac_nhanh", gt("8", "dùng 8 giờ", "giờ")), "bang_chung": []}
    t = chay_xu_ly(du, tb, [], cac, ma_mau="dh-apple-watchse3", nhom="dong_ho")["tuyen_bo"]
    assert (t["gia_tri"], t["don_vi"]) == (8.0, "gio")
    assert t["dieu_kien"]["so_phut_sac"] == {"so": 8.0, "don_vi": "phut"}     # "dùng" còn cho hoat_dong chưa rõ (cụm cấu hình)
    du = {"tuyen_bo": tb_muc("sac_nhanh", gt("8", "dùng 8 giờ", "giờ"), [dk("dieu_kien_do", "nạp 8 phút")]), "bang_chung": []}
    t = chay_xu_ly(du, "Watch A nạp 8 phút dùng 8 giờ", [], cac, ma_mau="dh-apple-watchse3", nhom="dong_ho")["tuyen_bo"]
    assert t["dieu_kien"]["so_phut_sac"] == {"so": 8.0, "don_vi": "phut"} and t["nguon_dieu_kien"]["so_phut_sac"] == "llm_don_vi"


def test_luat_don_vi_sau_mot_dieu_kien_so_khop_cum_cau_hinh():
    # Lỗi chạy thật 08/11: biến trong vòng lặp che tham số gia_tri, nên cụm thứ hai (không khớp cụm cấu hình) làm KeyError.
    cfg = tx.lay_cau_hinh("dien_thoai")
    cac_dk = [{"i": 0, "loai": "phu_kien", "cum": "bộ tiếp hợp 40W trở lên", "trich": "với bộ tiếp hợp 40W trở lên"},
              {"i": 1, "loai": "dieu_kien_do", "cum": "sạc tới 50%", "trich": "sạc tới 50%"}]
    kq = tx.hieu_dieu_kien(cac_dk, "sac_nhanh", "tai_lieu", cfg, (20.0, "phut"))
    assert kq["dieu_kien"]["bo_tiep_hop"] == {"so": 40.0, "don_vi": "W"}
    assert kq["dieu_kien"]["moc_phan_tram"] == {"so": 50.0, "don_vi": "phan_tram"}


def test_tran_token_ghi_vao_ban_ghi(tmp_path):
    tb = thu_tuyen_bo("tb-00040")
    gia = trich_tu_tb40()
    def transport(request, timeout_s):
        if request["parameters"]["max_output_tokens"] < 2000:
            return LLMResult('{"tuyen_bo', request["provider"], request["model"], "m", {}, "length")
        return LLMResult(json.dumps(gia, ensure_ascii=False), request["provider"], request["model"], "m", {}, "stop")
    client = LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=transport)
    bg = tx.trich_xuat(tb, tb["ma_mau"], client, MODEL, max_token_ra=1000)
    assert bg["tran_token"] == 2000 and bg["loi"] is None
    assert tx.trich_xuat(tb, tb["ma_mau"], client_gia(tmp_path / "k", gia, []), MODEL)["tran_token"] == tx.MAX_TOKEN_RA
