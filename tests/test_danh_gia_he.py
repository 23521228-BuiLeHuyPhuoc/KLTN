import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("danh_gia_he", ROOT / "scripts/danh_gia_he.py")
danh_gia_he = importlib.util.module_from_spec(spec)
spec.loader.exec_module(danh_gia_he)

# Tám tuyên bố thường (4 cụm quảng cáo, hai mẫu thuộc tập kiểm tra), một ở mẫu m3 (tập phát triển), một biến thể ct-.
QC = {1: "qc1", 2: "qc1", 3: "qc2", 4: "qc2", 5: "qc3", 6: "qc3", 7: "qc4", 8: "qc4", 9: "qc5"}
MAU = {i: ("m1" if i <= 4 else "m2" if i <= 8 else "m3") for i in QC}
CHUAN = {1: "DUNG", 2: "SAI", 3: "LECH", 4: "LECH", 5: "DUNG", 6: "CHUA_DU", 7: "LECH", 8: "SAI", 9: "DUNG"}
GHI_CHU = {1: "mac_dinh=che_do_nguon", 2: "chep_nhan=a", 3: "mac_dinh=ngoai_bang; ngoai_cau_hinh=x", 5: "mau_thuan_khop_ca_hai=1/2"}
DONG_D = {6: "D1b"}


def ghi_jsonl(duong, ds):
    duong.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in ds), encoding="utf-8")


def ma(i):
    return f"tb-{i:05d}"


@pytest.fixture
def du_lieu(tmp_path):
    tuyen_bo = [{"id": ma(i), "ma_qc": QC[i], "ma_mau": MAU[i], "llm_sinh": "gemini" if i % 2 else "groq",
                 "che_do": "ten" if i <= 4 else "ten_thong_so"} for i in QC]
    tuyen_bo.append({"id": "ct-00001-bo_dieu_kien", "ma_qc": "qc-khac", "ma_mau": "m1", "llm_sinh": "gemini", "che_do": "ten"})
    nhan = [{"id": ma(i), "nhan": CHUAN[i], "dong_d": DONG_D.get(i, "D3"), "ghi_chu": GHI_CHU.get(i, "")} for i in QC]
    nhan.append({"id": "ct-00001-bo_dieu_kien", "nhan": "LECH", "dong_d": "D4", "ghi_chu": ""})
    p = {**CHUAN}
    b0 = {i: "DUNG" if CHUAN[i] in ("LECH", "DUNG") or i in (7, 8) else CHUAN[i] for i in QC}  # chấp nhận nhầm ở 3, 4, 7, 8
    p_nn = {**CHUAN, 3: "DUNG"}
    tep = {}
    for ten, d, ct in (("P", p, "LECH"), ("B0", b0, "DUNG"), ("P−NN", p_nn, "LECH")):
        rows = [{"id": ma(i), "nhan": d[i]} for i in QC] + [{"id": "ct-00001-bo_dieu_kien", "nhan": ct}]
        if ten == "B0":
            rows[1] = {"id": ma(2), "nhan": None}  # nhãn lỗi -> LOI
        tep[ten] = tmp_path / f"he_{len(tep)}.jsonl"
        ghi_jsonl(tep[ten], rows)
    ghi_jsonl(tmp_path / "tb.jsonl", tuyen_bo)
    ghi_jsonl(tmp_path / "nhan.jsonl", nhan)
    (tmp_path / "chia_tap.json").write_text(json.dumps({"kiem_tra": {"mau": ["m1", "m2"]}, "phat_trien": {"mau": ["m3"]}}), encoding="utf-8")
    (tmp_path / "mau.csv").write_text(
        "ma_mau,nhom,hang,ten\nm1,dien_thoai,Apple,A\nm2,tai_nghe,Samsung,B\nm3,dong_ho,Xiaomi,C\n", encoding="utf-8")
    return tmp_path, tep


def chay(du_lieu, *them, ra="ra"):
    tmp, tep = du_lieu
    argv = ["--nhan", str(tmp / "nhan.jsonl"), "--tuyen-bo", str(tmp / "tb.jsonl"), "--chia-tap", str(tmp / "chia_tap.json"),
            "--mau-san-pham", str(tmp / "mau.csv"), "--ra", str(tmp / ra), "--n-bootstrap", "100", "--tap", "kiem_tra"]
    for ten, duong in tep.items():
        argv += ["--he", f"{ten}={duong}"]
    return danh_gia_he.main(argv + list(them)), tmp / ra


def doc_csv(duong):
    with open(duong, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_dau_cuoi_du_tep_va_so_lieu(du_lieu, capsys):
    ma_thoat, ra = chay(du_lieu)
    assert ma_thoat == 0
    assert sorted(p.name for p in ra.iterdir()) == sorted(
        ["bang_chinh.csv", "mcnemar.csv", "gia_thuyet.csv", "theo_nhom.csv", "do_nhay.csv",
         "nham_lan_P.csv", "nham_lan_B0.csv", "nham_lan_P-NN.csv"])
    chinh = {r["he"]: r for r in doc_csv(ra / "bang_chinh.csv")}
    assert list(chinh) == ["P", "B0", "P-NN"]  # P−NN chuẩn hóa
    # mẫu: tb-1..8 (không lấy tb-9 ở tập phát triển, không lấy ct-)
    assert chinh["P"]["n"] == "8"
    assert (chinh["P"]["far_tu"], chinh["P"]["far_mau"]) == ("0", "6")
    assert float(chinh["P"]["far_diem"]) == 0 and float(chinh["P"]["far_duoi"]) == 0 and float(chinh["P"]["far_tren"]) == 0
    assert float(chinh["P"]["macro_f1_diem"]) == 1.0 and chinh["P"]["so_loi"] == "0"
    assert float(chinh["P"]["recall_dung_diem"]) == 1.0 and float(chinh["P"]["f1_LECH"]) == 1.0
    assert (chinh["B0"]["far_tu"], chinh["B0"]["far_mau"]) == ("4", "6")
    assert chinh["B0"]["so_loi"] == "1"  # tb-2 nhãn None
    assert float(chinh["B0"]["far_diem"]) == pytest.approx(4 / 6, abs=1e-6)
    assert (chinh["P-NN"]["far_tu"], chinh["P-NN"]["far_mau"]) == ("1", "6")
    assert float(chinh["P-NN"]["f1_LECH"]) == pytest.approx(0.8)

    mc = {r["he_doi_chung"]: r for r in doc_csv(ra / "mcnemar.csv")}
    assert list(mc) == ["B0", "P-NN"]
    # b = P chấp nhận mà B0 không = 0; c = B0 chấp nhận mà P không = 4 (tb-3, 4, 7, 8); p = 2 * 1 / 16
    assert (mc["B0"]["b"], mc["B0"]["c"], mc["B0"]["n"]) == ("0", "4", "4")
    assert float(mc["B0"]["p"]) == 0.125 and float(mc["B0"]["p_holm"]) == 0.125 and mc["B0"]["trong_ho_holm"] == "True"
    assert (mc["P-NN"]["b"], mc["P-NN"]["c"], mc["P-NN"]["n"], mc["P-NN"]["p"]) == ("0", "1", "1", "1.0")
    assert mc["P-NN"]["p_holm"] == "" and mc["P-NN"]["trong_ho_holm"] == "False"

    gt = {(r["gia_thuyet"], r["muc"]): r for r in doc_csv(ra / "gia_thuyet.csv")}
    assert len(gt) == 6
    assert gt[("H1", "theo_phat_bieu")]["dat"] == "dat"  # FAR 0 < 4/6; Recall Đúng P = B0 = 1
    assert gt[("H1", "theo_phat_bieu")]["he_thieu"] == "B1,B2,B3"
    assert gt[("H1", "y_nghia_thong_ke")]["dat"] == "khong_dat"  # p_holm = 0.125
    assert gt[("H2", "theo_phat_bieu")]["dat"] == "thiếu hệ" and gt[("H2", "y_nghia_thong_ke")]["dat"] == "thiếu hệ"
    assert gt[("H3", "theo_phat_bieu")]["dat"] == "dat"  # FAR 0 < 1/6; F1 Lệch 1 > 0,8
    assert gt[("H3", "y_nghia_thong_ke")]["dat"] == "khong_dat"  # p = 1

    nl = {r["nhan_chuan"]: r for r in doc_csv(ra / "nham_lan_B0.csv")}
    assert list(nl) == ["DUNG", "SAI", "LECH", "CHUA_DU"]
    assert nl["LECH"]["DUNG"] == "3" and nl["LECH"]["LECH"] == "0" and nl["SAI"]["LOI"] == "1" and nl["LECH"]["tong"] == "3"

    nhom = [r for r in doc_csv(ra / "theo_nhom.csv") if r["he"] == "P"]
    chieu = {(r["chieu"], r["gia_tri"]): r for r in nhom}
    assert {c for c, _ in chieu} == {"nhom", "hang", "llm_sinh", "che_do"}  # không có loai_bien_doi khi chỉ tuyên bố thường
    assert chieu[("nhom", "dien_thoai")]["n"] == "4" and chieu[("nhom", "tai_nghe")]["n"] == "4"
    assert chieu[("hang", "Apple")]["far_mau"] == "3"  # tb-2, 3, 4
    assert chieu[("che_do", "ten")]["n"] == "4"

    nhay = {(r["he"], r["kich_ban"]): r for r in doc_csv(ra / "do_nhay.csv")}
    assert nhay[("P", "goc")]["so_nhan_doi"] == "0"
    # tb-1 (DUNG) và tb-3 (LECH) có mac_dinh nên thành CHUA_DU: khác DUNG 1(CUD), 2, 3(CUD), 4, 6, 7, 8 = 7; P chấp nhận tb-1
    assert nhay[("P", "doi_mac_dinh")]["so_nhan_doi"] == "2" and nhay[("P", "doi_mac_dinh")]["far_mau"] == "7"
    assert float(nhay[("P", "doi_mac_dinh")]["far"]) == pytest.approx(1 / 7, abs=1e-6)
    assert nhay[("P", "doi_ngoai_bang")]["so_nhan_doi"] == "1"
    assert nhay[("P", "bo_D1b")]["so_ca_bo"] == "1" and nhay[("P", "bo_D1b")]["n"] == "7"
    assert nhay[("P", "bo_mau_thuan_khop_ca_hai")]["so_ca_bo"] == "1"
    assert nhay[("P", "bo_ca_hai")]["n"] == "6" and nhay[("P", "bo_ca_hai")]["so_ca_bo"] == "2"
    chep = nhay[("(toan_bo)", "chep_nhan")]
    assert chep["n"] == "1" and "QĐ15" in chep["ghi_chu"]

    ra_man_hinh = capsys.readouterr().out
    assert "P: FAR" in ra_man_hinh and "H1 / theo_phat_bieu: dat" in ra_man_hinh


def test_tat_dinh_chay_lai_cung_seed_cho_csv_giong_het(du_lieu):
    _, ra1 = chay(du_lieu, ra="ra1")
    _, ra2 = chay(du_lieu, ra="ra2")
    for ten in ("bang_chinh.csv", "mcnemar.csv", "gia_thuyet.csv"):
        assert (ra1 / ten).read_bytes() == (ra2 / ten).read_bytes()


def test_cap_toi_thieu_dung_cum_cua_tuyen_bo_goc_va_them_chieu_loai(du_lieu):
    ma_thoat, ra = chay(du_lieu, "--cap-toi-thieu")
    assert ma_thoat == 0
    chinh = {r["he"]: r for r in doc_csv(ra / "bang_chinh.csv")}
    assert chinh["P"]["n"] == "1"
    nhom = doc_csv(ra / "theo_nhom.csv")
    assert any(r["chieu"] == "loai_bien_doi" and r["gia_tri"] == "bo_dieu_kien" and r["n"] == "1" for r in nhom)
    # cụm của ct-00001-... là qc1 (cụm tb-00001), không phải qc-khac
    hang = danh_gia_he.chon_mau(
        danh_gia_he.doc_jsonl(du_lieu[0] / "tb.jsonl"), "kiem_tra", True, danh_gia_he.doc_mau_san_pham(du_lieu[0] / "mau.csv"),
        json.loads((du_lieu[0] / "chia_tap.json").read_text(encoding="utf-8")))
    assert [(h["id"], h["cum"]) for h in hang] == [("ct-00001-bo_dieu_kien", "qc1")]


def test_he_thieu_du_doan_bao_loi_kem_ma(du_lieu, capsys):
    tmp, tep = du_lieu
    rows = [r for r in danh_gia_he.doc_jsonl(tep["B0"]) if r["id"] != ma(8)]
    ghi_jsonl(tep["B0"], rows)
    with pytest.raises(SystemExit):
        chay(du_lieu)
    loi = capsys.readouterr().err
    assert "B0" in loi and "tb-00008" in loi


def test_ban_goc_cua_bien_the_khong_co_bao_loi(du_lieu, capsys):
    tmp, _ = du_lieu
    tb = danh_gia_he.doc_jsonl(tmp / "tb.jsonl") + [{"id": "ct-00099-doi_gia_tri", "ma_qc": "x", "ma_mau": "m1"}]
    ghi_jsonl(tmp / "tb.jsonl", tb)
    with pytest.raises(SystemExit):
        chay(du_lieu, "--cap-toi-thieu")
    assert "tb-00099" in capsys.readouterr().err


def test_chuan_hoa_ten_he():
    assert danh_gia_he.chuan_hoa_ten("P−ĐK") == "P-DK"
    assert danh_gia_he.chuan_hoa_ten(" P–NN ") == "P-NN"
    assert danh_gia_he.chuan_hoa_ten("P-NN") == "P-NN"
