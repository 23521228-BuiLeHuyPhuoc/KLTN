import builtins
import importlib.util
import io
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chon_mau_gan_lai", ROOT / "scripts/chon_mau_gan_lai.py")
cm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cm)

# Kích thước tầng giả: tổng 100, chọn 20 -> mỗi tầng đúng tỉ lệ có phần dư khác nhau.
CAU_TRUC = {"dt-a": 31, "dt-b": 17, "tn-a": 23, "tn-b": 9, "dh-a": 20}
TAP_GIA = {"phat_trien": ["dt-a", "tn-a", "dh-a"], "kiem_tra": ["dt-b", "tn-b"]}


def bo_gia(cau_truc=CAU_TRUC):
    ban_ghi, i = [], 1
    for ma_mau, so in cau_truc.items():
        for _ in range(so):
            ban_ghi.append({"id": f"tb-{i:05d}", "ma_mau": ma_mau})
            i += 1
    return ban_ghi


def chia_tap_gia(tap=TAP_GIA):
    return {t: {"mau": m} for t, m in tap.items()}


def ghi_gia(tmp_path, ban_ghi, chia_tap):
    tb, ct = tmp_path / "chinh.jsonl", tmp_path / "chia_tap.json"
    tb.write_text("﻿" + "".join(json.dumps(b) + "\n" for b in ban_ghi), encoding="utf-8")
    ct.write_text(json.dumps(chia_tap), encoding="utf-8")
    return tb, ct


def hamilton_chuan(so_tang, n):
    """Cài đặt độc lập bằng Fraction để đối chiếu."""
    from fractions import Fraction
    tong = sum(so_tang.values())
    ly_tuong = {t: Fraction(n * s, tong) for t, s in so_tang.items()}
    chon = {t: int(x) for t, x in ly_tuong.items()}
    thu_tu = sorted(ly_tuong, key=lambda t: (-(ly_tuong[t] - chon[t]), t))
    for t in thu_tu[:n - sum(chon.values())]:
        chon[t] += 1
    return chon


def test_hang_so_theo_yeu_cau():
    assert cm.SEED == 20261126 and cm.TY_LE == 0.2
    assert cm.TEP_RA.parts[-3:] == ("data", "nhan", "danh_sach_mau.json")


def test_cung_seed_cung_ket_qua_khac_seed_khac():
    ban_ghi, chia_tap = bo_gia(), chia_tap_gia()
    a = cm.tao_ket_qua(ban_ghi, chia_tap, seed=1)
    b = cm.tao_ket_qua(ban_ghi, chia_tap, seed=1)
    c = cm.tao_ket_qua(ban_ghi, chia_tap, seed=2)
    assert a == b
    assert a["gan_lai_buoc32"] != c["gan_lai_buoc32"]
    assert a["theo_tang"] == c["theo_tang"]


def test_tong_va_so_chon_moi_tang_theo_phan_du_lon_nhat():
    ket_qua = cm.tao_ket_qua(bo_gia(), chia_tap_gia())
    assert len(ket_qua["gan_lai_buoc32"]) == round(0.2 * 100) == 20
    so_tang = {t: v["quan_the"] for t, v in ket_qua["theo_tang"].items()}
    assert so_tang == {"phat_trien/dt": 31, "kiem_tra/dt": 17, "phat_trien/tn": 23, "kiem_tra/tn": 9, "phat_trien/dh": 20}
    assert {t: v["chon"] for t, v in ket_qua["theo_tang"].items()} == hamilton_chuan(so_tang, 20)
    assert all(v["chon"] >= 1 for v in ket_qua["theo_tang"].values())
    assert sum(v["chon"] for v in ket_qua["theo_tang"].values()) == 20


def test_hoa_phan_du_uu_tien_ten_tang_truoc():
    # Hai tầng 5 và 5, chọn 5: phần dư bằng nhau (0.5), tầng tên sắp xếp trước được thêm 1.
    assert cm.chia_tieu_chuan({"b": 5, "a": 5}, 5) == {"a": 3, "b": 2}


def test_moi_tang_khong_rong_co_it_nhat_1_va_tong_khong_vuot_n():
    cau_truc = {"dt-a": 90, "tn-a": 8, "dh-a": 2}
    ban_ghi = bo_gia(cau_truc)
    ket_qua = cm.tao_ket_qua(ban_ghi, chia_tap_gia({"phat_trien": list(cau_truc), "kiem_tra": []}), ty_le=0.1)
    chon = {t: v["chon"] for t, v in ket_qua["theo_tang"].items()}
    assert chon == {"phat_trien/dt": 8, "phat_trien/tn": 1, "phat_trien/dh": 1}
    assert len(ket_qua["gan_lai_buoc32"]) == 10


def test_ep_toi_thieu_1_lay_bot_o_tang_lon_nhat():
    # 100 mã: 97 + 2 + 1, chọn 3 -> Hamilton cho 3,0,0; ép tối thiểu 1 rồi bớt ở tầng lớn nhất còn 1.
    assert cm.chia_tieu_chuan({"a": 97, "b": 2, "c": 1}, 3) == {"a": 1, "b": 1, "c": 1}


def test_ma_chon_thuoc_quan_the_khong_trung_va_dung_tang():
    ban_ghi, chia_tap = bo_gia(), chia_tap_gia()
    ket_qua = cm.tao_ket_qua(ban_ghi, chia_tap)
    chon = ket_qua["gan_lai_buoc32"]
    assert len(set(chon)) == len(chon) and chon == sorted(chon)
    ma_quan_the = {b["id"] for b in ban_ghi}
    assert set(chon) <= ma_quan_the
    mau = {b["id"]: b["ma_mau"] for b in ban_ghi}
    dem = {}
    for m in chon:
        t = cm.ten_tang(mau[m], chia_tap)
        dem[t] = dem.get(t, 0) + 1
    assert dem == {t: v["chon"] for t, v in ket_qua["theo_tang"].items()}


def test_dau_ra_co_du_khoa_theo_yeu_cau():
    ket_qua = cm.tao_ket_qua(bo_gia(), chia_tap_gia(), seed=7)
    assert ket_qua["buoc"] == 26 and ket_qua["ngay"] == "26/11/2026" and ket_qua["seed"] == 7
    assert ket_qua["ty_le"] == 0.2 and ket_qua["so_quan_the"] == 100
    assert ket_qua["nguoi_thu_hai"] == []
    assert ket_qua["ghi_chu_nguoi_thu_hai"] == "Chưa có người gán thứ hai; chờ CBHD"
    assert ket_qua["quan_the"] == cm.QUAN_THE and ket_qua["quy_tac"]


def test_mau_khong_thuoc_tap_nao_bao_loi():
    ban_ghi = bo_gia() + [{"id": "tb-99999", "ma_mau": "dt-la"}]
    with pytest.raises(ValueError, match="dt-la"):
        cm.tao_ket_qua(ban_ghi, chia_tap_gia())


def test_ma_lap_bao_loi():
    ban_ghi = bo_gia()
    ban_ghi.append(dict(ban_ghi[0]))
    with pytest.raises(ValueError, match="lặp"):
        cm.tao_ket_qua(ban_ghi, chia_tap_gia())


def test_main_ghi_tep_va_in_khong_ghi(tmp_path, capsys):
    tb, ct = ghi_gia(tmp_path, bo_gia(), chia_tap_gia())
    ra = tmp_path / "ra" / "dsm.json"
    cm.main(["--tuyen-bo", str(tb), "--chia-tap", str(ct), "--ra", str(ra), "--seed", "5"])
    du_lieu = json.loads(ra.read_text(encoding="utf-8"))
    assert du_lieu["seed"] == 5 and len(du_lieu["gan_lai_buoc32"]) == 20
    assert b"\r\n" not in ra.read_bytes() and "Chưa có người gán thứ hai" in ra.read_text(encoding="utf-8")
    ra2 = tmp_path / "khong_ghi.json"
    capsys.readouterr()
    cm.main(["--tuyen-bo", str(tb), "--chia-tap", str(ct), "--ra", str(ra2), "--in"])
    assert not ra2.exists()
    assert json.loads(capsys.readouterr().out)["buoc"] == 26


def chan_doc_data_nhan(monkeypatch):
    """Báo lỗi nếu bất kỳ lệnh mở tệp nào chạm đường dẫn chứa data/nhan (đọc hay ghi)."""
    def kiem(duong):
        s = str(duong).replace("\\", "/")
        if "data/nhan" in s:
            raise AssertionError(f"script mở tệp dưới data/nhan: {s}")

    mo_goc = builtins.open
    path_open_goc = Path.open

    def open_gia(file, *a, **k):
        kiem(file)
        return mo_goc(file, *a, **k)

    def path_open_gia(self, *a, **k):
        kiem(self)
        return path_open_goc(self, *a, **k)

    monkeypatch.setattr(builtins, "open", open_gia)
    monkeypatch.setattr(io, "open", open_gia)
    monkeypatch.setattr(Path, "open", path_open_gia)


def test_khong_mo_tep_data_nhan_khi_doc(tmp_path, monkeypatch):
    chan_doc_data_nhan(monkeypatch)
    ra = tmp_path / "dsm.json"
    cm.main(["--ra", str(ra)])  # đọc dữ liệu thật, ghi vào tmp_path
    assert ra.exists()
    cm.main(["--in"])
    with pytest.raises(AssertionError):  # xác nhận bẫy hoạt động
        open(ROOT / "data" / "nhan" / "x.json")


def test_du_lieu_that(tmp_path):
    ra = tmp_path / "dsm.json"
    cm.main(["--ra", str(ra)])
    kq = json.loads(ra.read_text(encoding="utf-8"))
    assert kq["so_quan_the"] == 258 and len(kq["gan_lai_buoc32"]) == 52
    so_tang = {t: v["quan_the"] for t, v in kq["theo_tang"].items()}
    assert sum(so_tang.values()) == 258
    assert {t: v["chon"] for t, v in kq["theo_tang"].items()} == hamilton_chuan(so_tang, 52)
    assert all(v["chon"] >= 1 for v in kq["theo_tang"].values())
    thu = {json.loads(d)["id"] for d in (ROOT / "data/tuyen_bo/thu.jsonl").read_text(encoding="utf-8-sig").splitlines() if d.strip()}
    assert not thu & set(kq["gan_lai_buoc32"])
    chinh = {json.loads(d)["id"] for d in (ROOT / "data/tuyen_bo/chinh.jsonl").read_text(encoding="utf-8-sig").splitlines() if d.strip()}
    assert set(kq["gan_lai_buoc32"]) <= chinh and len(chinh) == 258
