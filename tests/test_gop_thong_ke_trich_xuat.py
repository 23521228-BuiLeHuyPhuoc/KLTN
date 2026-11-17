"""Test scripts/gop_thong_ke_trich_xuat.py (Bước 22). Chỉ dùng LLM giả (--gia), ghi vào tmp_path, không mạng.

Chữ thật: vài dòng tuyên bố của mẫu tn-samsung-buds3pro trong data/tuyen_bo/thu.jsonl (tập phát triển), chia thành hai tệp.
"""
import importlib.util
import json
from pathlib import Path
import re
import socket
import sys

import pytest

from kiemchung import truy_hoi as th

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def nap(ten):
    spec = importlib.util.spec_from_file_location(ten, ROOT / f"scripts/{ten}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


chay = nap("chay_trich_xuat")
gop = nap("gop_thong_ke_trich_xuat")

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


@pytest.fixture
def hai_tep(tmp_path):
    """Hai tệp tuyên bố nhỏ (3 và 2 dòng) và kết quả --gia của từng tệp trong tmp_path/tx_gia."""
    dong = [d for d in chay.doc_jsonl(ROOT / "data/tuyen_bo/thu.jsonl") if d["ma_mau"] == BUDS][:5]
    tep = [tmp_path / "a.jsonl", tmp_path / "b.jsonl"]
    for t, phan in zip(tep, (dong[:3], dong[3:])):
        t.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in phan), encoding="utf-8")
        assert chay.main(["--gia", "--tuyen-bo", str(t), "--thu-muc-ra", str(tmp_path / "tx"), "--nghi-giay", "0"]) == 0
    return tep


def chay_gop(tmp_path, tep, *them):
    return gop.main(["--tuyen-bo", *map(str, tep), "--mo-hinh", MODEL, "--thu-muc", str(tmp_path / "tx"), "--gia", *them])


def so(md, mau):
    return [int(x) for x in re.search(mau, md).groups()]


def test_gop_ghi_thong_ke_va_cong_dung_hai_tep(hai_tep, tmp_path, capsys):
    assert chay_gop(tmp_path, hai_tep) == 0
    ra = tmp_path / "tx_gia" / f"thong_ke_phat_trien_{MODEL}_k5_am_tiet_gia.md"
    assert ra.exists()
    md = ra.read_text(encoding="utf-8")
    assert "Số tuyên bố: 5;" in md and "Gộp từ:" in md and "(3 tuyên bố)" in md and "(2 tuyên bố)" in md
    assert "Số tuyên bố: 5;" in capsys.readouterr().out
    mau = r"giữ (\d+), bị loại (\d+)"
    rieng = [so((tmp_path / "tx_gia" / f"thong_ke_{t.stem}_{MODEL}_k5_am_tiet_gia.md").read_text(encoding="utf-8"), mau)
             for t in hai_tep]
    assert so(md, mau) == [sum(r[0] for r in rieng), sum(r[1] for r in rieng)]


def test_thieu_tep_ket_qua_thoat_khac_0_va_nem_ten_tep(hai_tep, tmp_path, capsys):
    thieu = tmp_path / "tx_gia" / f"b_{MODEL}_k5_am_tiet_gia.jsonl"
    thieu.unlink()
    assert chay_gop(tmp_path, hai_tep) != 0
    assert thieu.name in capsys.readouterr().err
    assert not list((tmp_path / "tx_gia").glob("thong_ke_phat_trien*"))


def test_tep_ket_qua_thieu_id_bao_loi_liet_ke_id(hai_tep, tmp_path, capsys):
    kq = tmp_path / "tx_gia" / f"a_{MODEL}_k5_am_tiet_gia.jsonl"
    dong = kq.read_text(encoding="utf-8").splitlines(keepends=True)
    id_mat = json.loads(dong[0])["id"]
    kq.write_text("".join(dong[1:]), encoding="utf-8")
    assert chay_gop(tmp_path, hai_tep) != 0
    err = capsys.readouterr().err
    assert "thiếu id" in err and id_mat in err


def test_id_trung_giua_cac_tep_tuyen_bo_bao_loi(hai_tep, tmp_path, capsys):
    assert chay_gop(tmp_path, [hai_tep[0], hai_tep[0]]) != 0
    assert "trùng" in capsys.readouterr().err
