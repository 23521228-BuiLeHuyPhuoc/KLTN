"""Kiểm tra thiết kế bộ chính và thông số bằng dữ liệu giả, không gọi mạng."""
from collections import Counter
import importlib.util
import json
from pathlib import Path

import pytest

TEP = Path(__file__).resolve().parents[1] / "scripts/sinh_chinh.py"
spec = importlib.util.spec_from_file_location("sinh_chinh", TEP)
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)


def test_thiet_ke():
    mau = [r["ma_mau"] for r in sc.doc_mau()]
    to_hop = sc.thiet_ke(mau)
    assert len(to_hop) == 80
    ma_qc = {sc.sqc.ma_quang_cao(*t, 1) for t in to_hop}
    assert len(ma_qc) == 80
    bo_thu = {sc.sqc.ma_quang_cao(ma, mh, loai, cd, 1)
              for ma in sc.MAU_THU for mh in sc.MO_HINH
              for loai in sc.sqc.LOAI_BAI for cd in sc.sqc.CHE_DO}
    assert len(bo_thu) == 24
    assert ma_qc.isdisjoint(bo_thu)
    assert set(Counter(t[0] for t in to_hop).values()) == {8}
    assert set(Counter((t[0], t[3]) for t in to_hop).values()) == {4}
    assert set(Counter((t[0], t[1], t[3]) for t in to_hop).values()) == {2}
    assert sorted(Counter(t[2] for t in to_hop).values()) == [26, 27, 27]
    for i, ma in enumerate(mau):
        for d, cd in enumerate(sc.sqc.CHE_DO):
            assert {t[2] for t in to_hop if t[0] == ma and t[3] == cd} == set(sc.sqc.LOAI_BAI)
            for m, mh in enumerate(sc.MO_HINH):
                assert {t[2] for t in to_hop if t[0] == ma and t[1] == mh and t[3] == cd} == (
                    set(sc.sqc.LOAI_BAI) - {sc.sqc.LOAI_BAI[(i + 2*m + d) % 3]})
    for mh in sc.MO_HINH:
        for cd in sc.sqc.CHE_DO:
            dem = Counter(t[2] for t in to_hop if t[1] == mh and t[3] == cd)
            assert sorted(dem.values()) == [6, 7, 7]
    assert list(dict.fromkeys(t[0] for t in to_hop)) == mau


def tao_doan(tmp_path, noi_dung):
    tep = tmp_path / "doan.jsonl"
    tep.write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in noi_dung), encoding="utf-8")
    return tep


def test_thu_tu_va_noi_dung_goc(tmp_path):
    tep = tao_doan(tmp_path, [
        {"id": "m#001", "noi_dung": "20 phút", "noi_dung_goc": "20 phút6"},
        {"id": "m#002", "noi_dung": "Đã sửa", "noi_dung_goc": " Nguyên văn7 "},
    ])
    assert sc.dung_van_ban(tep, ["m#002", "m#001"]) == " Nguyên văn7 \n20 phút6"


@pytest.mark.parametrize("do_dai", [5000, 5001])
def test_gioi_han_ky_tu(tmp_path, do_dai):
    tep = tao_doan(tmp_path, [{"id": "m#001", "noi_dung_goc": "á" * do_dai}])
    if do_dai == 5000:
        assert len(sc.dung_van_ban(tep, ["m#001"])) == 5000
    else:
        with pytest.raises(ValueError, match="5.000"):
            sc.dung_van_ban(tep, ["m#001"])


@pytest.mark.parametrize("ma_doan", [[], ["m#999"], ["m#001"]])
def test_thieu_du_lieu(tmp_path, ma_doan):
    tep = tao_doan(tmp_path, [{"id": "m#001", "noi_dung": "không dùng thay bản gốc"}])
    with pytest.raises(ValueError):
        sc.dung_van_ban(tep, ma_doan)


def test_chon_doan_kiemtra(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "GOC", tmp_path)
    thu_muc = tmp_path / "data/quang_cao/thong_so"
    thu_muc.mkdir(parents=True)
    nguon = tmp_path / "data/nguon/dt-gia"
    nguon.mkdir(parents=True)
    tao_doan(nguon, [{"id": "dt-gia#001", "noi_dung_goc": "Một1"},
                    {"id": "dt-gia#002", "noi_dung_goc": "Hai2"}])
    tep = thu_muc / "chon_doan_kiemtra.json"
    for du_lieu in (None, {}):
        if du_lieu is not None:
            tep.write_text(json.dumps(du_lieu), encoding="utf-8")
        with pytest.raises(ValueError, match="chưa có đoạn thông số"):
            sc.doan_thong_so("dt-gia", "kiemtra")
    tep.write_text(json.dumps({"dt-gia": [{"id": "dt-gia#002"}, {"id": "dt-gia#001"}]}),
                   encoding="utf-8")
    ma, vb, quy_tac = sc.doan_thong_so("dt-gia", "kiemtra")
    assert ma == ["dt-gia#002", "dt-gia#001"]
    assert vb == "Hai2\nMột1"
    assert "chon_doan_kiemtra.json" in quy_tac


@pytest.mark.parametrize("chu", ["429", "RESOURCE_EXHAUSTED", "High demand", "overloaded", "503",
                                 "ETIMEDOUT", "mã HTTP 500"])
def test_loi_tam_thoi(chu):
    assert sc.la_loi_tam_thoi(sc.sqc.LoiCopyPro(chu))
    assert not sc.la_loi_tam_thoi(sc.sqc.LoiCopyPro("fallback"))


def test_khong_ghi_mau_thu(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "GOC", tmp_path)
    for ma in sc.MAU_THU:
        with pytest.raises(ValueError, match="mẫu thử"):
            sc.ghi_thong_so(ma, (["gia"], "văn bản", "quy tắc"))
    assert not list(tmp_path.iterdir())


def test_liet_ke_khong_goi_mang(tmp_path, monkeypatch, capsys):
    mau = sc.doc_mau()
    monkeypatch.setattr(sc, "GOC", tmp_path)
    monkeypatch.setattr(sc, "doc_mau", lambda: mau)
    def cam_goi(*args, **kwargs):
        pytest.fail("--liet-ke không được gọi mạng hoặc ghi thông số")
    monkeypatch.setattr(sc.sqc, "mo_phien", cam_goi)
    monkeypatch.setattr(sc.sqc, "goi_api", cam_goi)
    monkeypatch.setattr(sc, "ghi_thong_so", cam_goi)
    monkeypatch.setattr(sc, "doan_thong_so", lambda *args: (_ for _ in ()).throw(
        ValueError("chưa có đoạn thông số")))
    assert sc.main(["--liet-ke"]) == 0
    out = capsys.readouterr().out
    assert sum(d.startswith("qc-") for d in out.splitlines()) == 80
    assert "chưa có đoạn thông số" in out


def test_thoi_gian_cho_theo_loai_loi():
    assert sc.thoi_gian_cho("mã HTTP 500: connect ETIMEDOUT 1.2.3.4:27017", 2) == sc.CHO_MAT_KET_NOI
    assert sc.thoi_gian_cho("mã HTTP 429: RESOURCE_EXHAUSTED", 0) == 60
    assert sc.thoi_gian_cho("model is experiencing high demand", 2) == 240
