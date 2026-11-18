"""Kiểm B1/B2 bằng transport giả, không đọc nhãn hay tài liệu thật."""
import importlib.util
import json
from pathlib import Path
import re
import socket
import unicodedata

import pytest

from kiemchung.doi_chung import b1, b2
from kiemchung.doi_chung.chung import doc_tra_ve
from kiemchung.doi_chung.huong_dan import (huong_dan_cho_cau_lenh, vi_du_b2, dinh_dang_vi_du,
                                         kiem_khong_lo_kiemtra)
from kiemchung.llm import LLMClient, LLMResult

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def chan_mang(monkeypatch):
    """Không cho test gọi mạng dù cấu hình môi trường có khóa."""
    def chan(*args, **kwargs):
        raise AssertionError("không được gọi mạng")
    monkeypatch.setattr(socket.socket, "connect", chan)


def nap_script(ten):
    spec = importlib.util.spec_from_file_location(ten, ROOT / "scripts" / f"{ten}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("ten,khung", [("B1", b1.CAU_LENH_B1), ("B2", b2.CAU_LENH_B2)])
def test_cau_lenh_nguyen_van(ten, khung):
    chu = (ROOT / "luan_van/buoc29_30_thiet_ke_cau_lenh.md").read_text(encoding="utf-8")
    m = re.search(rf"<!-- CAU_LENH_{ten}: bat_dau -->\s*```text\n(.*?)\n```\s*<!-- CAU_LENH_{ten}: ket_thuc -->", chu, re.S)
    assert m is not None and m[1] == khung


def test_huong_dan_va_vi_du():
    hd = huong_dan_cho_cau_lenh()
    assert re.findall(r"^## (\d+)\.", hd, re.M) == ["3", "4", "5", "6", "7"]
    assert "### 5.1" not in hd
    vd = vi_du_b2()
    assert [d["id"] for d in vd] == ["V09", "V16", "V24", "V46"]
    assert [d["nhan"] for d in vd] == ["Đúng", "Sai", "Lệch điều kiện", "Chưa đủ thông tin"]
    assert all(d["doan"] and d["ly_do"] and d["tuyen_bo"] for d in vd)
    kiem_khong_lo_kiemtra(hd + dinh_dang_vi_du(vd))


def test_huong_dan_giu_nguyen_chu():
    chu = (ROOT / "data/huong_dan_gan_nhan.md").read_text(encoding="utf-8")
    dau = chu.index("## 3.")
    truoc = chu.index("### 5.1")
    sau = chu.index("## 6.")
    cuoi = chu.index("## 8.")
    assert huong_dan_cho_cau_lenh() == chu[dau:truoc] + chu[sau:cuoi]


def test_thay_mot_luot():
    chu = b2.ghep_cau_lenh("câu {tuyen_bo} {vi_du}", [("dt-a#001", "{huong_dan}")], "HD", "VD")
    assert "Tuyên bố: câu {tuyen_bo} {vi_du}" in chu
    assert "[dt-a#001] {huong_dan}" in chu
    chu = b1.ghep_cau_lenh({"tuyen_bo": {"trich": "{huong_dan}"}, "bang_chung": []}, "HD")
    assert '"trich": "{huong_dan}"' in chu


@pytest.mark.parametrize("chu,ma", [("Đúng", "DUNG"), ("Sai", "SAI"), ("Lệch điều kiện", "LECH"),
                                      ("Chưa đủ thông tin", "CHUA_DU"), ("DUNG", "DUNG"), ("SAI", "SAI"),
                                      ("LECH", "LECH"), ("CHUA_DU", "CHUA_DU")])
def test_nhan(chu, ma):
    for n in (chu, chu.lower(), chu.upper(), " \n" + chu.replace(" ", "   ") + "\t", unicodedata.normalize("NFD", chu)):
        d = json.dumps({"nhan": n}, ensure_ascii=False)
        assert doc_tra_ve(d)["nhan"] == ma
        assert doc_tra_ve(f"```json\n{d}\n```")["nhan"] == ma


@pytest.mark.parametrize("chu", ['{"nhan":"Lệch"}', '{"nhan":"abc"}', "{", "[]", "{}", '{"nhan":5}'])
def test_nhan_loi(chu):
    assert doc_tra_ve(chu)["nhan"] == "LOI"
    assert doc_tra_ve(chu)["loi"]


def test_bo_thong_so():
    muc = {"thuoc_tinh": "pin", "gia_tri": 6, "trich": {"gia_tri": "6 giờ"}, "nguon_dieu_kien": {},
           "bo_qua": [], "dieu_kien_phu": [], "dieu_kien": {}, "khac_san_pham": False}
    bg = {"tuyen_bo": muc, "bang_chung": [muc, {**muc, "khac_san_pham": True}]}
    tb, tl = b1.bo_thong_so_cho_b1(bg)
    khoa = ("thuoc_tinh", "gia_tri", "trich", "dieu_kien")
    assert json.loads(tl) == [{k: muc[k] for k in khoa}]
    assert {k: v for k, v in json.loads(tb).items() if k in khoa} == {k: muc[k] for k in khoa}
    assert set(json.loads(tb)) == set(khoa) | {"ma_mau", "ten_san_pham", "hang", "chu_tuyen_bo"}
    assert tb == json.dumps(json.loads(tb), ensure_ascii=False, sort_keys=True, indent=1)
    assert "nguon_dieu_kien" in muc
    assert b1.bo_thong_so_cho_b1({"tuyen_bo": None, "bang_chung": [], "loi": "hỏng"}) == ("null", "[]")


def test_chay_b1_loi_trich_xuat_tra_loi_khong_goi_llm(tmp_path):
    def transport(request, timeout_s):
        raise AssertionError("không được gọi LLM khi bản ghi trích xuất có loi")
    client = LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=transport)
    bg = {"id": "tb-1", "ma_mau": "dt-a", "tuyen_bo": None, "bang_chung": [], "loi": "hỏng"}
    r = b1.chay_mot(client, "gemini-3.6-flash", bg, "HD")
    assert r["nhan"] == "LOI" and r["loi_trich_xuat"] == "hỏng" and r["id"] == "tb-1"
    assert r["trich_xuat_thieu"] and not r["tu_bo_nho_dem"]


def test_chay_b1_thieu_trich_xuat_van_goi_llm_va_dem(tmp_path):
    def transport(request, timeout_s):
        return LLMResult('{"nhan":"Đúng"}', request["provider"], request["model"], "gia", {}, "stop")
    client = LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=transport)
    bg = {"id": "tb-1", "ma_mau": "dt-a", "tuyen_bo": None, "bang_chung": []}
    r = b1.chay_mot(client, "gemini-3.6-flash", bg, "HD")
    assert r["nhan"] == "DUNG" and r["loi_trich_xuat"] is None and r["trich_xuat_thieu"]
    assert isinstance(r["thoi_gian_sinh_ms"], float)
    assert b1.chay_mot(client, "gemini-3.6-flash", bg, "HD")["tu_bo_nho_dem"]


def test_b1_nhan_cung_thong_tin_nhu_p_khong_nhan_luat_cua_p():
    bg = {"id": "tb-1", "ma_mau": "dt-xiaomi-15t", "chu_tuyen_bo": "Xiaomi 15T sạc 90W",
          "tuyen_bo": {"thuoc_tinh": "sac_nhanh", "gia_tri": 90, "don_vi": "w", "san_pham_ma": "dt-xiaomi-15t",
                       "goi_muc_cao": True, "xung_dot": {"che_do": ["a", "b"]}, "kieu_gia_tri": "toi_da",
                       "cum_kieu": "tối đa", "dieu_kien": {}, "trich": {"gia_tri": "90W"}, "bo_qua": ["x"]},
          "bang_chung": [{"ma_doan": "d#1", "thuoc_tinh": "sac_nhanh", "gia_tri": 90, "san_pham_ma": "dt-xiaomi-15t",
                          "xung_dot": {"c": [1, 2]}, "goi_muc_cao": False, "khac_san_pham": False,
                          "nguon_dieu_kien": {"c": "lan"}},
                         {"ma_doan": "d#2", "khac_san_pham": True, "gia_tri": 1}]}
    tb, tl = (json.loads(x) for x in b1.bo_thong_so_cho_b1(bg))
    for k in ("chu_tuyen_bo", "ma_mau", "ten_san_pham", "hang", "san_pham_ma", "goi_muc_cao", "xung_dot"):
        assert tb[k] is not None, k
    assert tb["hang"] == "Xiaomi" and tb["chu_tuyen_bo"] == "Xiaomi 15T sạc 90W"
    assert "bo_qua" not in tb
    assert [m["ma_doan"] for m in tl] == ["d#1"]          # khac_san_pham đã bị P lọc ở khâu trích xuất
    assert tl[0]["san_pham_ma"] == "dt-xiaomi-15t" and tl[0]["xung_dot"] == {"c": [1, 2]}
    assert "nguon_dieu_kien" not in tl[0]                  # dấu vết luật lan của P không đưa cho B1


def test_tran_token_b0_b2_bang_p():
    from kiemchung import trich_xuat as tx
    from kiemchung.doi_chung import b0, chung
    assert b0.MAX_TOKEN_RA == chung.MAX_TOKEN_RA == tx.MAX_TOKEN_RA == 8192


@pytest.mark.parametrize("he", ["b1", "b2"])
def test_script_gia(tmp_path, monkeypatch, he):
    script = nap_script("chay_doi_chung")
    monkeypatch.setattr(script.b2.th, "lay_doan", lambda *a: [("dt-a#001", "pin 6 giờ")])
    tep = tmp_path / "thu.jsonl"
    d = {"id": "tb-1", "ma_mau": "dt-a", "tuyen_bo": None if he == "b1" else "pin 6 giờ", "bang_chung": []}
    tep.write_text(json.dumps(d) + "\n", encoding="utf-8")
    ra = tmp_path / "ra"
    args = ["--he", he, "--trich-xuat" if he == "b1" else "--tuyen-bo", str(tep), "--gia", "--thu-muc-ra", str(ra)]
    assert script.main(args) == 0
    tep_ra = ra / f"{he}_thu_gemini-3.6-flash_gia.jsonl"
    truoc = tep_ra.read_bytes()
    assert script.main(args) == 0
    assert tep_ra.read_bytes() == truoc
    assert "tu_bo_nho_dem" not in truoc.decode("utf-8")
    assert json.loads(truoc)["nhan"] in {"DUNG", "SAI", "LECH", "CHUA_DU"}
