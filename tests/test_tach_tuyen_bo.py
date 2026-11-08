"""Kiểm tách tự động trên bài và tuyên bố tự đặt."""
import importlib.util
import json
from pathlib import Path
import re
import socket

import pytest

from kiemchung import tach_tuyen_bo as tach
from kiemchung.llm import LLMClient, LLMResult

ROOT = Path(__file__).resolve().parents[1]
BAI = {"ma_qc": "qc-dt-a-gia-ten-1", "ma_mau": "dt-a", "noi_dung": "pin 6 giờ",
       "che_do": "ten", "mo_hinh": "gia"}


@pytest.fixture(autouse=True)
def moi_truong(monkeypatch):
    def chan(*args, **kwargs):
        raise AssertionError("không được gọi mạng")
    monkeypatch.setattr(socket.socket, "connect", chan)
    monkeypatch.setattr(tach, "nhom_cua_mau", lambda ma: "dien_thoai")


def test_cau_lenh():
    chu = (ROOT / "luan_van/buoc29_30_thiet_ke_cau_lenh.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- CAU_LENH_TACH: bat_dau -->\s*```text\n(.*?)\n```\s*<!-- CAU_LENH_TACH: ket_thuc -->", chu, re.S)
    assert m[1] == tach.CAU_LENH_TACH
    cau = tach.ghep_cau_lenh({**BAI, "noi_dung": "{bai} {ten_nhom}"}, "dien_thoai", tach.lay_cau_hinh("dien_thoai"))
    assert cau.endswith("{bai} {ten_nhom}")


@pytest.mark.parametrize("nhom,chu,tt,gt,dv", [
    ("dien_thoai", "Máy A pin 90 phút", "thoi_luong_pin", 1.5, "gio"),
    ("dien_thoai", "Máy A pin 6 giờ", "thoi_luong_pin", 6, "gio"),
    ("dien_thoai", "sạc 50% trong 0,5 giờ với 40W", "sac_nhanh", 30, "phut"),
    ("dien_thoai", "Máy A 40W, màn hình 2000 nit và 3000 nit", "do_sang", 2000, "nit"),
    ("dien_thoai", "Máy A IP68", "khang_nuoc", {"bui": 6, "nuoc": 8}, "ma_ip"),
    ("dong_ho", "Đồng hồ A WR50", "khang_nuoc", 50, "m"),
    ("dong_ho", "sạc trong 1 giờ", "sac_nhanh", 60, "phut"),
])
def test_doc_gia_tri(nhom, chu, tt, gt, dv):
    assert tach.doc_gia_tri_tuyen_bo(chu, tt, tach.lay_cau_hinh(nhom)) == {"gia_tri": gt, "don_vi": dv}


def test_khong_doc_duoc():
    assert tach.doc_gia_tri_tuyen_bo("pin trâu", "thoi_luong_pin", tach.lay_cau_hinh("dien_thoai")) is None


def chay(tmp_path, chu):
    def transport(request, timeout_s):
        return LLMResult(chu, request["provider"], request["model"], "gia", {}, "stop")
    client = LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=transport)
    return tach.tach_bai(client, "gemini-3.6-flash", BAI)


def test_loc_va_cau_goc(tmp_path):
    ds = [{"tuyen_bo": "Máy A pin 6 giờ", "cau_goc": "pin  6\n giờ", "thuoc_tinh_du_kien": "thoi_luong_pin"},
          {"tuyen_bo": "Máy A pin 7 giờ", "cau_goc": "không có", "thuoc_tinh_du_kien": "thoi_luong_pin"},
          {"tuyen_bo": "Máy A 48 MP", "cau_goc": "48 MP", "thuoc_tinh_du_kien": "camera"}, {}]
    r = chay(tmp_path, "```json\n" + json.dumps(ds, ensure_ascii=False) + "\n```")
    assert r["loi"] is None
    assert [d["cau_goc_khong_khop"] for d in r["tuyen_bo"]] == [False, True]
    assert r["bi_loc"] == {"thuoc_tinh_ngoai_nhom": 1, "sai_luoc_do": 1}


@pytest.mark.parametrize("chu", ["hỏng", "{}", "null"])
def test_bai_loi(tmp_path, chu):
    assert chay(tmp_path, chu)["loi"]
    assert chay(tmp_path, chu)["tuyen_bo"] == []


def test_danh_sach_rong(tmp_path):
    r = chay(tmp_path, "[]")
    assert r["loi"] is None and r["tuyen_bo"] == []


def test_ghep_va_chi_so():
    def d(so, bai="qc-a", tt="thoi_luong_pin"):
        return {"ma_qc": bai, "thuoc_tinh": tt, "gia_tri": {"gia_tri": so, "don_vi": "gio"}}
    td = [d(6), d(6), d(7), d(6, "qc-b"), d(6, tt="sac_nhanh")]
    tay = [d(6), d(8)]
    assert tach.ghep(td, tay) == [(0, 0)]
    s = tach.thong_ke(td, tay)
    assert s["precision"] == 1 / 5 and s["recall"] == 1 / 2
    assert tach.thong_ke([], [d(6)])["recall"] == 0
    assert tach.thong_ke([], [])["precision"] is None
    assert tach.ghep([dict(d(6), gia_tri=None)], [dict(d(6), gia_tri=None)]) == []


def test_script_gia(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("chay_tach_tu_dong", ROOT / "scripts/chay_tach_tu_dong.py")
    script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(script)
    thu_muc = tmp_path / "quang_cao"
    thu_muc.mkdir()
    for i in (1, 2):
        b = {**BAI, "ma_qc": f"qc-dt-a-gia-ten-{i}"}
        (thu_muc / f"{b['ma_qc']}.json").write_text(json.dumps(b), encoding="utf-8")
    # Tệp không thuộc mẫu được chọn không được mở, dù không phải JSON hợp lệ.
    (thu_muc / "qc-dt-khac-gia-ten-1.json").write_text("không được đọc", encoding="utf-8")
    monkeypatch.setattr(script, "THU_MUC_QUANG_CAO", thu_muc)
    tep = tmp_path / "thu.jsonl"
    tep.write_text(json.dumps({"id": "tb-1", "ma_qc": BAI["ma_qc"], "ma_mau": "dt-a",
                               "tuyen_bo": "Máy A pin 6 giờ", "thuoc_tinh": "thoi_luong_pin"}) + "\n", encoding="utf-8")
    ra = tmp_path / "ra"
    args = ["--tuyen-bo", str(tep), "--gia", "--thu-muc-ra", str(ra)]
    assert script.main(args) == 0
    ket_qua = ra / "tach_thu_gemini-3.6-flash_gia.jsonl"
    truoc = ket_qua.read_bytes()
    assert len(truoc.splitlines()) == 2
    assert script.main(args) == 0
    assert ket_qua.read_bytes() == truoc
    md = (ra / "tach_thu_gemini-3.6-flash_gia.md").read_text(encoding="utf-8")
    assert "0.500000" in md and "1.000000" in md
    assert "ten_thong_so" in md and "llm_sinh" in md and "dien_thoai" in md
