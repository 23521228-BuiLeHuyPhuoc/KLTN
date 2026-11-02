import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("do_nhat_quan", ROOT / "scripts/do_nhat_quan.py")
dq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dq)

# (mã, nhãn lượt 2, nhãn lượt 3, dòng D lượt 2, dòng D lượt 3). Số tính tay:
# lượt 2: LECH 4, DUNG 4, SAI 1, CHUA_DU 1; lượt 3: LECH 3, DUNG 5, SAI 2, CHUA_DU 0; đồng ý 7/10.
# Bốn nhãn: pe = (4*3 + 4*5 + 1*2 + 1*0)/100 = 0,34; kappa = (0,7 - 0,34)/(1 - 0,34) = 6/11.
# Lệch / không Lệch: đồng ý 9/10; pe = (4*3 + 6*7)/100 = 0,54; kappa = (0,9 - 0,54)/(1 - 0,54) = 18/23.
CAC_CAP = [
    ("tb-00001", "LECH", "LECH", "D4", "D4"),
    ("tb-00002", "LECH", "LECH", "D4", "D2"),
    ("tb-00003", "LECH", "LECH", "D2", "D2"),
    ("tb-00004", "LECH", "DUNG", "D4", "D3"),
    ("tb-00005", "DUNG", "DUNG", "D3", "D3"),
    ("tb-00006", "DUNG", "DUNG", "D3", "D3"),
    ("tb-00007", "DUNG", "SAI", "D3", "D5"),
    ("tb-00008", "DUNG", "DUNG", "D3", "D3"),
    ("tb-00009", "SAI", "SAI", "D5", "D5"),
    ("tb-00010", "CHUA_DU", "DUNG", "D1", "D3"),
]


def ban_ghi(ma, nhan, dong_d):
    return {"id": ma, "nhan": nhan, "dong_d": dong_d, "luot": 2}


def hai_tep(cap=CAC_CAP):
    nhan2 = {m: ban_ghi(m, a, da) for m, a, _, da, _ in cap}
    nhan3 = {m: dict(ban_ghi(m, b, db), luot=3) for m, _, b, _, db in cap}
    return nhan3, nhan2


def ghi_jsonl(duong, dong):
    duong.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in dong), encoding="utf-8")
    return duong


def test_kappa_hai_lop_tinh_tay():
    # 20 cặp cùng Lệch, 5 Lệch/không, 10 không/Lệch, 15 cùng không: đồng ý 0,7; pe = (25*30 + 25*20)/2500 = 0,5; kappa 0,4.
    cap = [("LECH", "LECH")] * 20 + [("LECH", "DUNG")] * 5 + [("DUNG", "LECH")] * 10 + [("DUNG", "DUNG")] * 15
    assert dq.kappa_cohen(cap) == pytest.approx(0.4)


def test_kappa_dong_y_hoan_toan_la_1_va_nguoc_hoan_toan_am():
    cap = [("LECH", "LECH")] * 3 + [("DUNG", "DUNG")] * 4 + [("SAI", "SAI")]
    assert dq.kappa_cohen(cap) == pytest.approx(1.0)
    nguoc = [("LECH", "DUNG")] * 5 + [("DUNG", "LECH")] * 5
    assert dq.kappa_cohen(nguoc) == pytest.approx(-1.0)


def test_kappa_khong_xac_dinh_khi_mot_nhan_duy_nhat_hoac_khong_co_cap():
    assert dq.kappa_cohen([("LECH", "LECH")] * 5) is None
    assert dq.kappa_cohen([]) is None
    assert dq.kappa_cohen([("DUNG", "SAI")] * 3) == pytest.approx(0.0)  # hai bên đều chỉ một nhãn nhưng khác nhau: pe = 0


def test_do_nhat_quan_so_do_tinh_tay():
    kq = dq.do_nhat_quan(*hai_tep())
    assert kq["n"] == 10 and kq["khop"] == 7 and kq["khop_lech"] == 9
    assert kq["kappa_4"] == pytest.approx(6 / 11)
    assert kq["kappa_lech"] == pytest.approx(18 / 23)
    assert kq["lech_luot2"] == 4 and kq["lech_luot3"] == 3
    assert kq["chi_o_luot3"] == [] and kq["chi_o_luot2"] == []
    assert [x["id"] for x in kq["khac"]] == ["tb-00004", "tb-00007", "tb-00010"]


def test_bang_nham_lan_hang_la_luot_2_cot_la_luot_3():
    kq = dq.do_nhat_quan(*hai_tep())
    b = kq["bang"]
    assert b[("LECH", "LECH")] == 3 and b[("LECH", "DUNG")] == 1 and b[("DUNG", "LECH")] == 0
    assert b[("DUNG", "SAI")] == 1 and b[("CHUA_DU", "DUNG")] == 1 and b[("DUNG", "DUNG")] == 3
    assert sum(b.values()) == 10 and sum(v for (a, _), v in b.items() if a == "LECH") == 4  # tổng hàng LECH = số Lệch của lượt 2
    assert sum(v for (_, c), v in b.items() if c == "DUNG") == 5  # tổng cột DUNG = số Đúng của lượt 3
    bl = kq["bang_lech"]
    assert bl[("LECH", "LECH")] == 3 and bl[("LECH", "KHONG_LECH")] == 1
    assert bl[("KHONG_LECH", "LECH")] == 0 and bl[("KHONG_LECH", "KHONG_LECH")] == 6


def test_chi_do_tren_ma_chung_va_liet_ke_ma_le():
    nhan3, nhan2 = hai_tep()
    nhan3["tb-00099"] = ban_ghi("tb-00099", "LECH", "D4")  # chỉ ở lượt 3
    del nhan3["tb-00001"]  # chỉ ở lượt 2
    kq = dq.do_nhat_quan(nhan3, nhan2)
    assert kq["n"] == 9 and kq["chi_o_luot3"] == ["tb-00099"] and kq["chi_o_luot2"] == ["tb-00001"]
    assert "tb-00099" not in kq["chung"] and "tb-00001" not in kq["chung"]
    assert kq["lech_luot2"] == 3  # tb-00001 (LECH) không tính


def test_doc_nhan_loi(tmp_path):
    ok = ghi_jsonl(tmp_path / "a.jsonl", [ban_ghi("tb-00001", "LECH", "D4")])
    assert dq.doc_nhan(ok)["tb-00001"]["nhan"] == "LECH"
    lap = ghi_jsonl(tmp_path / "lap.jsonl", [ban_ghi("tb-00001", "LECH", "D4"), ban_ghi("tb-00001", "DUNG", "D3")])
    with pytest.raises(ValueError, match="id tb-00001 lặp"):
        dq.doc_nhan(lap)
    la = ghi_jsonl(tmp_path / "la.jsonl", [ban_ghi("tb-00001", "TOT", "D3")])
    with pytest.raises(ValueError, match="không thuộc"):
        dq.doc_nhan(la)
    hong = tmp_path / "hong.jsonl"
    hong.write_text('{"id": "tb-00001", "nhan": \n', encoding="utf-8")
    with pytest.raises(ValueError, match="không phải JSON hợp lệ"):
        dq.doc_nhan(hong)
    thieu_id = ghi_jsonl(tmp_path / "id.jsonl", [{"nhan": "LECH"}])
    with pytest.raises(ValueError, match="có id"):
        dq.doc_nhan(thieu_id)


def test_bao_cao_ghi_ro_y_nghia_va_co_du_muc():
    kq = dq.do_nhat_quan(*hai_tep())
    bc = dq.viet_bao_cao(kq, cau={"tb-00004": "Tuyên bố có | dấu gạch\nvà xuống dòng"})
    assert "**Claude gán, người thực hiện duyệt**" in bc
    assert "**chính người thực hiện gán lại mù**" in bc
    assert "độ nhất quán của một người với nhãn chuẩn" in bc and "không phải độ đồng thuận giữa hai người" in bc
    assert "7/10 = 70,0%" in bc and "9/10 = 90,0%" in bc
    assert "| Kappa của Cohen, bốn nhãn (DUNG, SAI, LECH, CHUA_DU) | 0,545 |" in bc
    assert "| Kappa của Cohen, riêng nhãn Lệch (Lệch so với không Lệch) | 0,783 |" in bc
    assert "## Bảng nhầm lẫn bốn nhãn (hàng: lượt 2, cột: lượt 3)" in bc
    assert "| Lượt 2 \\ Lượt 3 | DUNG | SAI | LECH | CHUA_DU | Tổng |" in bc
    assert "| **LECH** | 1 | 0 | 3 | 0 | 4 |" in bc
    assert "## Tuyên bố khác nhãn (3)" in bc
    assert "| tb-00004 | LECH (D4) | DUNG (D3) | Tuyên bố có \\| dấu gạch và xuống dòng |" in bc
    assert "| tb-00007 | DUNG (D3) | SAI (D5) |  |" in bc  # không có chữ tuyên bố thì để trống
    assert bc.endswith("\n")


def test_bao_cao_khong_cot_tuyen_bo_khi_khong_co_chu_va_khong_khac_nhan():
    kq = dq.do_nhat_quan(*hai_tep())
    bc = dq.viet_bao_cao(kq)
    assert "| Mã | Lượt 2 (dòng D) | Lượt 3 (dòng D) |\n" in bc and "Tuyên bố |" not in bc
    giong = [(m, a, a, da, da) for m, a, _, da, _ in CAC_CAP]
    kq2 = dq.do_nhat_quan(*hai_tep(giong))
    assert kq2["khac"] == [] and kq2["kappa_4"] == pytest.approx(1.0)
    assert "Không có: mọi tuyên bố chung đều cùng nhãn ở hai lượt." in dq.viet_bao_cao(kq2)


def test_bao_cao_kappa_khong_xac_dinh_khi_mot_nhan():
    cap = [(f"tb-{i:05d}", "DUNG", "DUNG", "D3", "D3") for i in range(1, 6)]
    kq = dq.do_nhat_quan(*hai_tep(cap))
    assert kq["kappa_4"] is None and kq["kappa_lech"] is None
    bc = dq.viet_bao_cao(kq)
    assert "| Kappa của Cohen, bốn nhãn (DUNG, SAI, LECH, CHUA_DU) | không xác định |" in bc


def test_so_thap_phan_dau_phay():
    assert dq.so_thap_phan(0.54545) == "0,545" and dq.so_thap_phan(None) == "không xác định"
    assert dq.phan_tram(0, 0) == "không có" and dq.phan_tram(27, 30) == "90,0%"


def test_lenh_ghi_bao_cao_va_in(tmp_path, capsys):
    nhan3, nhan2 = hai_tep()
    t3 = ghi_jsonl(tmp_path / "thu_luot3.jsonl", list(nhan3.values()))
    t2 = ghi_jsonl(tmp_path / "thu_luot2.jsonl", list(nhan2.values()))
    tb = ghi_jsonl(tmp_path / "thu.jsonl", [{"id": "tb-00004", "tuyen_bo": "Câu bốn"}])
    ra = tmp_path / "ket_qua" / "bo_thu" / "nhat_quan_luot3.md"
    dq.main([str(t3), str(t2), "--tuyen-bo", str(tb), "--ra", str(ra)])
    out = capsys.readouterr().out
    bc = ra.read_text(encoding="utf-8")
    assert bc in out and "`thu_luot3.jsonl` (lượt 3) so với `thu_luot2.jsonl` (lượt 2)" in bc
    assert "| tb-00004 | LECH (D4) | DUNG (D3) | Câu bốn |" in bc and "\r" not in bc


def test_lenh_thoat_khi_thieu_tep_hoac_khong_co_ma_chung(tmp_path):
    t2 = ghi_jsonl(tmp_path / "thu_luot2.jsonl", [ban_ghi("tb-00001", "LECH", "D4")])
    with pytest.raises(SystemExit) as e:
        dq.main([str(tmp_path / "khong_co.jsonl"), str(t2), "--ra", str(tmp_path / "ra.md")])
    assert "không thấy tệp" in str(e.value)
    t3 = ghi_jsonl(tmp_path / "thu_luot3.jsonl", [ban_ghi("tb-00002", "LECH", "D4")])
    with pytest.raises(SystemExit) as e:
        dq.main([str(t3), str(t2), "--ra", str(tmp_path / "ra.md")])
    assert "không có mã chung nào" in str(e.value) and not (tmp_path / "ra.md").exists()
