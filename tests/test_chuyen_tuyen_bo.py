import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chuyen_tuyen_bo", ROOT / "scripts/chuyen_tuyen_bo.py")
ctb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctb)

THU = ROOT / "data/tuyen_bo/thu.jsonl"
BAI_PHAT_TRIEN = ROOT / "data/quang_cao/qc-dh-apple-watchse3-gemini-description-ten_thong_so-1.json"


def doan(tep, tu=0, den=4):
    """Đoạn con của noi_dung (vài từ liền nhau) làm cau_goc."""
    b = json.loads(tep.read_text(encoding="utf-8"))
    return b["ma_qc"], " ".join(b["noi_dung"].split()[tu:den])


def viet_csv(tep, dong):
    with open(tep, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ma_qc", "cau_goc", "tuyen_bo", "thuoc_tinh", "ghi_chu", "can_xem"])
        w.writerows(dong)


def doc(tep):
    return [json.loads(d) for d in Path(tep).read_text(encoding="utf-8").splitlines()]


@pytest.fixture
def csv_phat_trien(tmp_path):
    ma1, g1 = doan(BAI_PHAT_TRIEN, 0, 4)
    ma2, g2 = doan(BAI_PHAT_TRIEN, 4, 8)
    tep = tmp_path / "vao.csv"
    viet_csv(tep, [[ma1, g1, "tuyên bố một", "do_sang", "", ""], [ma2, g2, "tuyên bố hai", "khang_nuoc", "", ""]])
    return tep


def test_khong_co_tiep_sau_bat_dau_tu_00001(tmp_path, csv_phat_trien):
    ra = tmp_path / "ra.jsonl"
    assert ctb.chuyen(csv_phat_trien, ra) == 0
    kq = doc(ra)
    assert [r["id"] for r in kq] == ["tb-00001", "tb-00002"]
    assert kq[0]["thuoc_tinh"] == "do_sang" and kq[1]["thuoc_tinh"] == "khang_nuoc"  # thuộc tính đồng hồ hợp lệ
    assert kq[0]["ma_mau"] == "dh-apple-watchse3"


def test_tiep_sau_thu_bat_dau_tu_00067(tmp_path, csv_phat_trien, capsys):
    ra = tmp_path / "ra.jsonl"
    assert ctb.main([str(csv_phat_trien), str(ra), "--tiep-sau", str(THU)]) == 0
    assert [r["id"] for r in doc(ra)] == ["tb-00067", "tb-00068"]
    assert "tb-00067 … tb-00068" in capsys.readouterr().out


def test_ma_qc_da_co_trong_tep_tiep_sau_la_loi(tmp_path, capsys):
    ma_thu = json.loads(THU.read_text(encoding="utf-8-sig").splitlines()[0])["ma_qc"]
    _, g = doan(BAI_PHAT_TRIEN)
    vao, ra = tmp_path / "vao.csv", tmp_path / "ra.jsonl"
    viet_csv(vao, [[ma_thu, g, "x", "do_sang", "", ""]])
    assert ctb.chuyen(vao, ra, THU) == 1
    assert not ra.exists()
    assert "đã có trong" in capsys.readouterr().out


def test_thuoc_tinh_sai_bao_loi_khong_ghi(tmp_path, capsys):
    ma, g = doan(BAI_PHAT_TRIEN)
    vao, ra = tmp_path / "vao.csv", tmp_path / "ra.jsonl"
    viet_csv(vao, [[ma, g, "x", "thuoc_tinh_khong_co", "", ""]])
    assert ctb.chuyen(vao, ra) == 1
    assert not ra.exists()
    assert "không có trong dong_ho.yaml" in capsys.readouterr().out


def test_tep_tiep_sau_id_sai_dang_la_loi(tmp_path, csv_phat_trien):
    xau = tmp_path / "xau.jsonl"
    xau.write_text(json.dumps({"id": "tb-66", "ma_qc": "qc-khac"}) + "\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        ctb.chuyen(csv_phat_trien, tmp_path / "ra.jsonl", xau)
    with pytest.raises(SystemExit):  # tệp không có
        ctb.chuyen(csv_phat_trien, tmp_path / "ra.jsonl", tmp_path / "khong_co.jsonl")
    assert not (tmp_path / "ra.jsonl").exists()


def test_doc_ma_tiep_sau_lay_so_lon_nhat():
    so_lon, ma_qc, ma_mau = ctb.doc_ma_tiep_sau(THU)
    assert so_lon == 66 and len(ma_qc) == 20
    assert ma_mau == {"dt-apple-iphone17", "tn-samsung-buds3pro"}


def test_bai_bo_thu_khong_co_tuyen_bo_van_bi_chan(tmp_path, capsys):
    # 4/24 bài của bộ thử không có tuyên bố nên không nằm trong thu.jsonl; vẫn không được tách vào tập chính.
    _, ma_qc, _ = ctb.doc_ma_tiep_sau(THU)
    bai_trong = sorted(p for p in (ROOT / "data/quang_cao").glob("qc-*.json")
                       if p.stem not in ma_qc and ("-apple-iphone17-" in p.stem or "-samsung-buds3pro-" in p.stem))
    assert len(bai_trong) == 4
    ma, g = doan(bai_trong[0])
    vao, ra = tmp_path / "vao.csv", tmp_path / "ra.jsonl"
    viet_csv(vao, [[ma, g, "x", "thoi_luong_pin", "", ""]])
    assert ctb.chuyen(vao, ra, THU) == 1
    assert not ra.exists()
    assert "thuộc bộ trong" in capsys.readouterr().out


def test_sinh_lai_thu_jsonl_dung_tung_byte(tmp_path):
    csv_ = ROOT / "data/tuyen_bo/thu_nhap.csv"
    if not (csv_.exists() and THU.exists()):
        pytest.skip("không có thu_nhap.csv hoặc thu.jsonl")
    ra = tmp_path / "thu.jsonl"
    assert ctb.chuyen(csv_, ra) == 0
    assert ra.read_bytes() == THU.read_bytes()
