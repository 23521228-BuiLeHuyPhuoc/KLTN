"""Test src/kiemchung/tap.py và việc chặn tuyên bố tập kiểm tra ở các script chạy hệ thống (T3.5 quy tắc 4).

Chỉ dùng LLM giả (--gia), tệp tạm trong tmp_path, không gọi mạng. Tuyên bố thật: vài dòng của mẫu tn-samsung-buds3pro trong
data/tuyen_bo/thu.jsonl (tập phát triển) và vài dòng của tập kiểm tra trong data/tuyen_bo/chinh.jsonl (chỉ đọc).
"""
import importlib.util
import json
from pathlib import Path
import socket
import sys

import pytest

from kiemchung import tap, truy_hoi as th

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def nap(ten):
    spec = importlib.util.spec_from_file_location(ten, ROOT / f"scripts/{ten}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


chay = nap("chay_trich_xuat")
gop = nap("gop_thong_ke_trich_xuat")
chay_b0 = nap("chay_b0")
doi_chung = nap("chay_doi_chung")
tach_tu_dong = nap("chay_tach_tu_dong")
chay_p = nap("chay_p")
xu_ly_lai = nap("xu_ly_lai")

BUDS = "tn-samsung-buds3pro"
MODEL = "gemini-3.6-flash"
MAU_KIEM_TRA = tap.doc_mau_kiem_tra()
THONG_BAO = "Bỏ 2 tuyên bố của tập kiểm tra (T3.5 quy tắc 4); thêm --cho-phep-tap-kiem-tra sau Bước 33 nếu cần."


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


def doc(duong):
    return [json.loads(d) for d in Path(duong).read_text(encoding="utf-8").splitlines() if d.strip()]


@pytest.fixture
def tuyen_bo(tmp_path):
    """(tệp, id phát triển, id kiểm tra): 2 tuyên bố phát triển rồi 2 tuyên bố kiểm tra trong một tệp tạm."""
    pt = [d for d in doc(ROOT / "data/tuyen_bo/thu.jsonl") if d["ma_mau"] == BUDS][:2]
    kt = [d for d in doc(ROOT / "data/tuyen_bo/chinh.jsonl") if d["ma_mau"] in MAU_KIEM_TRA][:2]
    assert len(pt) == 2 and len(kt) == 2
    tep = tmp_path / "hon_hop.jsonl"
    tep.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in pt + kt), encoding="utf-8")
    return tep, [d["id"] for d in pt], [d["id"] for d in kt]


# --- helper ---

def test_doc_mau_kiem_tra_khop_chia_tap_json():
    mau = json.loads((ROOT / "data/chia_tap.json").read_text(encoding="utf-8"))
    assert MAU_KIEM_TRA == set(mau["kiem_tra"]["mau"]) and len(MAU_KIEM_TRA) == 8
    assert not MAU_KIEM_TRA & set(mau["phat_trien"]["mau"])


def test_doc_mau_kiem_tra_thieu_danh_sach_bao_loi(tmp_path):
    tep = tmp_path / "chia_tap.json"
    tep.write_text(json.dumps({"kiem_tra": {}}), encoding="utf-8")
    with pytest.raises(ValueError, match="kiem_tra"):
        tap.doc_mau_kiem_tra(tep)


def test_loc_mac_dinh_bo_tap_kiem_tra_giu_thu_tu():
    ds = [{"id": "a", "ma_mau": BUDS}, {"id": "b", "ma_mau": "dt-oppo-findx8"}, {"id": "c", "ma_mau": "dt-xiaomi-15t"}]
    giu, so_bo = tap.loc_tap_kiem_tra(ds)
    assert [d["id"] for d in giu] == ["a", "c"] and so_bo == 1


def test_loc_cho_phep_giu_het_va_khong_doc_chia_tap(monkeypatch):
    monkeypatch.setattr(tap, "doc_mau_kiem_tra", lambda *a: pytest.fail("không được đọc chia_tap.json"))
    ds = [{"id": "b", "ma_mau": "dt-oppo-findx8"}, {"id": "a", "ma_mau": BUDS}]
    assert tap.loc_tap_kiem_tra(ds, cho_phep=True) == (ds, 0)


def test_loc_nhan_mau_kiem_tra_tuy_chon():
    ds = [{"id": "a", "ma_mau": "x"}, {"id": "b", "ma_mau": "y"}]
    assert tap.loc_tap_kiem_tra(ds, mau_kiem_tra={"y"}) == ([ds[0]], 1)


def test_loc_va_bao_in_dung_mot_dong_khi_co_bo_va_im_khi_khong(capsys):
    ds = [{"id": "a", "ma_mau": "dt-oppo-findx8"}, {"id": "b", "ma_mau": "dt-oppo-findx8"}, {"id": "c", "ma_mau": BUDS}]
    assert tap.loc_va_bao(ds) == [ds[2]]
    err = capsys.readouterr().err
    assert err == THONG_BAO + "\n"
    tap.loc_va_bao([ds[2]])
    tap.loc_va_bao(ds, cho_phep=True)
    assert capsys.readouterr().err == ""


# --- chay_trich_xuat.py ---

def chay_tx(tuyen_bo, tmp_path, *them):
    return chay.main(["--gia", "--tuyen-bo", str(tuyen_bo[0]), "--thu-muc-ra", str(tmp_path / "tx"), "--nghi-giay", "0", *them])


def tep_tx(tmp_path):
    return tmp_path / "tx_gia" / f"hon_hop_{MODEL}_k5_am_tiet_gia.jsonl"


def test_trich_xuat_mac_dinh_bo_tap_kiem_tra(tuyen_bo, tmp_path, capsys):
    assert chay_tx(tuyen_bo, tmp_path) == 0
    assert [b["id"] for b in doc(tep_tx(tmp_path))] == tuyen_bo[1]
    err = capsys.readouterr().err
    assert err.count("Bỏ ") == 1 and THONG_BAO in err


def test_trich_xuat_co_cho_phep_giu_tap_kiem_tra(tuyen_bo, tmp_path, capsys):
    assert chay_tx(tuyen_bo, tmp_path, "--cho-phep-tap-kiem-tra") == 0
    assert [b["id"] for b in doc(tep_tx(tmp_path))] == tuyen_bo[1] + tuyen_bo[2]
    assert "Bỏ " not in capsys.readouterr().err


def test_trich_xuat_toan_tuyen_bo_kiem_tra_thi_dung_lai(tuyen_bo, tmp_path):
    kt = tmp_path / "kt.jsonl"
    kt.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in doc(tuyen_bo[0]) if d["id"] in tuyen_bo[2]),
                  encoding="utf-8")
    with pytest.raises(SystemExit, match="không có tuyên bố nào"):
        chay.main(["--gia", "--tuyen-bo", str(kt), "--thu-muc-ra", str(tmp_path / "tx")])


# --- gop_thong_ke_trich_xuat.py ---

def chay_gop(tuyen_bo, tmp_path, *them):
    return gop.main(["--tuyen-bo", str(tuyen_bo[0]), "--mo-hinh", MODEL, "--thu-muc", str(tmp_path / "tx"), "--gia",
                     "--ten", "hon_hop", *them])


def test_gop_mac_dinh_bo_tap_kiem_tra_khop_ket_qua_phat_trien(tuyen_bo, tmp_path, capsys):
    assert chay_tx(tuyen_bo, tmp_path) == 0
    capsys.readouterr()
    assert chay_gop(tuyen_bo, tmp_path) == 0
    cap = capsys.readouterr()
    assert THONG_BAO in cap.err and "Số tuyên bố: 2;" in cap.out


def test_gop_mac_dinh_bao_loi_khi_ket_qua_co_tuyen_bo_kiem_tra(tuyen_bo, tmp_path, capsys):
    assert chay_tx(tuyen_bo, tmp_path, "--cho-phep-tap-kiem-tra") == 0
    capsys.readouterr()
    assert chay_gop(tuyen_bo, tmp_path) == 1
    err = capsys.readouterr().err
    assert "thừa id" in err and tuyen_bo[2][0] in err


def test_gop_co_cho_phep_giu_tap_kiem_tra(tuyen_bo, tmp_path, capsys):
    assert chay_tx(tuyen_bo, tmp_path, "--cho-phep-tap-kiem-tra") == 0
    capsys.readouterr()
    assert chay_gop(tuyen_bo, tmp_path, "--cho-phep-tap-kiem-tra") == 0
    cap = capsys.readouterr()
    assert "Bỏ " not in cap.err and "Số tuyên bố: 4;" in cap.out


# --- chay_b0.py ---

def chay_b0_gia(tuyen_bo, tmp_path, monkeypatch, ma_nhan, *them):
    """chay_b0 đọc tệp tuyên bố cố định (TEP_TUYEN_BO) và tệp nhãn phải cùng tập mã với phần tuyên bố được giữ."""
    monkeypatch.setattr(chay_b0, "TEP_TUYEN_BO", tuyen_bo[0])
    nhan = tmp_path / "nhan_gia.jsonl"
    nhan.write_text("".join(json.dumps({"id": ma, "nhan": "DUNG"}) + "\n" for ma in ma_nhan), encoding="utf-8")
    return chay_b0.main(["--gia", "--mo-hinh", MODEL, "--thu-muc-ra", str(tmp_path / "b0"), "--nhan", str(nhan),
                         "--nghi-giay", "0", *them])


def test_b0_mac_dinh_bo_tap_kiem_tra(tuyen_bo, tmp_path, monkeypatch, capsys):
    assert chay_b0_gia(tuyen_bo, tmp_path, monkeypatch, tuyen_bo[1]) == 0
    assert [b["id"] for b in doc(tmp_path / "b0" / "b0_thu_gia" / f"{MODEL}.jsonl")] == tuyen_bo[1]
    assert THONG_BAO in capsys.readouterr().err


def test_b0_co_cho_phep_giu_tap_kiem_tra(tuyen_bo, tmp_path, monkeypatch, capsys):
    assert chay_b0_gia(tuyen_bo, tmp_path, monkeypatch, tuyen_bo[1] + tuyen_bo[2], "--cho-phep-tap-kiem-tra") == 0
    assert [b["id"] for b in doc(tmp_path / "b0" / "b0_thu_gia" / f"{MODEL}.jsonl")] == tuyen_bo[1] + tuyen_bo[2]
    assert "Bỏ " not in capsys.readouterr().err


# --- chay_doi_chung.py (B2; B1 dùng cùng đường lọc) ---

def chay_b2(tuyen_bo, tmp_path, *them):
    return doi_chung.main(["--he", "b2", "--gia", "--tuyen-bo", str(tuyen_bo[0]), "--mo-hinh", MODEL,
                           "--thu-muc-ra", str(tmp_path / "dc"), "--nghi-giay", "0", *them])


def test_doi_chung_mac_dinh_bo_tap_kiem_tra(tuyen_bo, tmp_path, capsys):
    assert chay_b2(tuyen_bo, tmp_path) == 0
    assert [b["id"] for b in doc(tmp_path / "dc" / f"b2_hon_hop_{MODEL}_gia.jsonl")] == tuyen_bo[1]
    assert THONG_BAO in capsys.readouterr().err


def test_doi_chung_co_cho_phep_giu_tap_kiem_tra(tuyen_bo, tmp_path, capsys):
    assert chay_b2(tuyen_bo, tmp_path, "--cho-phep-tap-kiem-tra") == 0
    assert [b["id"] for b in doc(tmp_path / "dc" / f"b2_hon_hop_{MODEL}_gia.jsonl")] == tuyen_bo[1] + tuyen_bo[2]
    assert "Bỏ " not in capsys.readouterr().err


# --- chay_tach_tu_dong.py ---

def chay_tach(tuyen_bo, tmp_path, *them):
    return tach_tu_dong.main(["--gia", "--tuyen-bo", str(tuyen_bo[0]), "--mo-hinh", MODEL,
                              "--thu-muc-ra", str(tmp_path / "td"), "--nghi-giay", "0", *them])


def mau_trong_bai(tmp_path):
    return {b["ma_mau"] for b in doc(tmp_path / "td" / f"tach_hon_hop_{MODEL}_gia_bai.jsonl")}


def test_tach_tu_dong_mac_dinh_bo_tap_kiem_tra(tuyen_bo, tmp_path, capsys):
    assert chay_tach(tuyen_bo, tmp_path) == 0
    assert mau_trong_bai(tmp_path) == {BUDS}
    assert THONG_BAO in capsys.readouterr().err


def test_tach_tu_dong_co_cho_phep_giu_tap_kiem_tra(tuyen_bo, tmp_path, capsys):
    assert chay_tach(tuyen_bo, tmp_path, "--cho-phep-tap-kiem-tra") == 0
    assert mau_trong_bai(tmp_path) > {BUDS}
    assert "Bỏ " not in capsys.readouterr().err


# --- chay_p.py và xu_ly_lai.py (offline, đọc kết quả trích xuất) ---

@pytest.fixture
def trich_xuat(tuyen_bo, tmp_path):
    """Tệp trích xuất giả (--gia) của cả 4 tuyên bố, kể cả 2 tuyên bố kiểm tra (chạy có cờ để dựng dữ liệu thử)."""
    assert chay_tx(tuyen_bo, tmp_path, "--cho-phep-tap-kiem-tra") == 0
    return tep_tx(tmp_path)


def test_chay_p_mac_dinh_bo_tap_kiem_tra(trich_xuat, tuyen_bo, tmp_path, capsys):
    assert chay_p.main(["--trich-xuat", str(trich_xuat), "--thu-muc-ra", str(tmp_path / "p")]) == 0
    assert len(doc(next((tmp_path / "p").glob("P_*.jsonl")))) == 2
    assert THONG_BAO in capsys.readouterr().err


def test_chay_p_co_cho_phep_giu_tap_kiem_tra(trich_xuat, tuyen_bo, tmp_path, capsys):
    assert chay_p.main(["--trich-xuat", str(trich_xuat), "--thu-muc-ra", str(tmp_path / "p"), "--cho-phep-tap-kiem-tra"]) == 0
    assert len(doc(next((tmp_path / "p").glob("P_*.jsonl")))) == 4
    assert "Bỏ " not in capsys.readouterr().err


def test_xu_ly_lai_mac_dinh_bo_tap_kiem_tra(trich_xuat, tmp_path, capsys):
    ra = tmp_path / "lai.jsonl"
    assert xu_ly_lai.main(["--trich-xuat", str(trich_xuat), "--ra", str(ra), "--thu-muc-cache", str(tmp_path / "cache")]) == 0
    assert len(doc(ra)) == 2
    assert THONG_BAO in capsys.readouterr().err


def test_xu_ly_lai_co_cho_phep_giu_tap_kiem_tra(trich_xuat, tmp_path, capsys):
    ra = tmp_path / "lai.jsonl"
    assert xu_ly_lai.main(["--trich-xuat", str(trich_xuat), "--ra", str(ra), "--thu-muc-cache", str(tmp_path / "cache"),
                           "--cho-phep-tap-kiem-tra"]) == 0
    assert len(doc(ra)) == 4
    assert "Bỏ " not in capsys.readouterr().err
