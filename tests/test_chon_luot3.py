import importlib.util
import json
from pathlib import Path
import random

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chon_luot3", ROOT / "scripts/chon_luot3.py")
cl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cl)


def bo_nhan(so=66, lech_moi=4):
    """so dòng nhãn tb-00001..: dòng thứ lech_moi, 2*lech_moi... là LECH, còn lại xoay vòng DUNG, SAI, CHUA_DU."""
    khac = ("DUNG", "SAI", "CHUA_DU")
    return [{"id": f"tb-{i:05d}", "nhan": "LECH" if i % lech_moi == 0 else khac[i % 3]} for i in range(1, so + 1)]


def ma_lech(dong):
    return sorted(nh["id"] for nh in dong if nh.get("nhan") == "LECH")


def test_hang_so_theo_yeu_cau():
    assert cl.SEED == 20261102 and cl.SO_CHON == 30 and cl.NHAN_LECH == "LECH"


def test_chon_du_so_luong_gom_moi_lech_va_xep_theo_ma():
    dong = bo_nhan()  # 16 LECH
    chon = cl.chon_luot3(dong)
    assert len(chon) == 30 and chon == sorted(chon) and len(set(chon)) == 30
    assert set(ma_lech(dong)) <= set(chon)
    khac = [m for m in chon if m not in set(ma_lech(dong))]
    assert len(khac) == 30 - 16
    assert {nh["id"] for nh in dong if nh["id"] in khac}.isdisjoint(ma_lech(dong))


def test_chon_dung_cong_thuc_random_sample_cua_seed():
    dong = bo_nhan()
    lech = ma_lech(dong)
    khac = sorted(nh["id"] for nh in dong if nh["nhan"] != "LECH")
    mong = sorted(lech + random.Random(20261102).sample(khac, 30 - len(lech)))
    assert cl.chon_luot3(dong) == mong


def test_chon_tat_dinh_va_khong_phu_thuoc_thu_tu_dong():
    dong = bo_nhan()
    mot = cl.chon_luot3(dong)
    assert cl.chon_luot3(dong) == mot
    dao = list(reversed(dong))
    random.Random(1).shuffle(dao)
    assert cl.chon_luot3(dao) == mot  # thứ tự dòng trong tệp nhãn không đổi kết quả


def test_seed_khac_chi_doi_phan_khong_phai_lech():
    dong = bo_nhan()
    a, b = cl.chon_luot3(dong, seed=1), cl.chon_luot3(dong, seed=2)
    assert a != b
    assert set(ma_lech(dong)) <= set(a) and set(ma_lech(dong)) <= set(b)


def test_nhan_khac_va_dong_thieu_nhan_deu_tinh_la_khong_lech():
    dong = bo_nhan(so=40, lech_moi=5)  # 8 LECH
    dong[0] = {"id": dong[0]["id"], "nhan": "CHUA_DU"}
    dong.append({"id": "tb-99999"})  # thiếu trường nhan: không phải LECH
    chon = cl.chon_luot3(dong, so_chon=12)
    assert len(chon) == 12 and set(ma_lech(dong)) <= set(chon)


def test_so_luong_bang_dung_so_lech_thi_khong_rut_them():
    dong = bo_nhan(so=20, lech_moi=4)  # 5 LECH
    assert cl.chon_luot3(dong, so_chon=5) == ma_lech(dong)


@pytest.mark.parametrize("dong, so_chon, mong", [
    (bo_nhan(so=20, lech_moi=2), 5, "nhiều hơn số cần chọn"),  # 10 LECH
    (bo_nhan(so=10, lech_moi=4), 30, "chỉ có"),               # không đủ mã để bù
    (bo_nhan(so=6) + [{"id": "tb-00001", "nhan": "DUNG"}], 4, "mã lặp"),
])
def test_loi_dau_vao(dong, so_chon, mong):
    with pytest.raises(ValueError, match=mong):
        cl.chon_luot3(dong, so_chon=so_chon)


def test_ghi_chon_co_dong_chu_thich_va_ma_theo_thu_tu(tmp_path):
    ra = tmp_path / "con" / "chon.txt"
    cl.ghi_chon(ra, ["tb-00002", "tb-00005", "tb-00009"])
    dong = ra.read_text(encoding="utf-8").splitlines()
    assert dong[0].startswith("#") and "20261102" in dong[0] and "LECH" in dong[0] and "30" in dong[0]
    assert dong[1:] == ["tb-00002", "tb-00005", "tb-00009"]
    assert "\r" not in ra.read_text(encoding="utf-8")


def test_lenh_ghi_tep_va_khong_in_ma(tmp_path, capsys):
    nhan = tmp_path / "thu_luot2.jsonl"
    nhan.write_text("".join(json.dumps(nh) + "\n" for nh in bo_nhan()), encoding="utf-8")
    ra = tmp_path / "chon.txt"
    cl.main(["--nhan", str(nhan), "--ra", str(ra)])
    kq = capsys.readouterr().out
    ma = [d for d in ra.read_text(encoding="utf-8").splitlines() if d and not d.startswith("#")]
    assert ma == cl.chon_luot3(bo_nhan()) and len(ma) == 30
    assert "30 mã" in kq and "16 LECH" in kq
    assert "tb-" not in kq  # lượt 3 gán mù: không in danh sách mã


def test_lenh_thieu_tep_nhan_thoat(tmp_path):
    with pytest.raises(SystemExit) as e:
        cl.main(["--nhan", str(tmp_path / "khong_co.jsonl"), "--ra", str(tmp_path / "chon.txt")])
    assert "không thấy tệp" in str(e.value)


def test_tep_chon_luot3_that_dung_dinh_dang():
    tep = ROOT / "data/nhan/chon_luot3.txt"
    tuyen_bo = ROOT / "data/tuyen_bo/thu.jsonl"
    if not tep.exists() or not tuyen_bo.exists():
        pytest.skip("chưa có data/nhan/chon_luot3.txt hoặc data/tuyen_bo/thu.jsonl")
    dong = tep.read_text(encoding="utf-8").splitlines()
    assert dong[0].startswith("#") and "20261102" in dong[0]
    ma = dong[1:]
    co = {json.loads(d)["id"] for d in tuyen_bo.read_text(encoding="utf-8-sig").splitlines() if d.strip()}
    assert len(ma) == 30 and ma == sorted(ma) and len(set(ma)) == 30 and set(ma) <= co
