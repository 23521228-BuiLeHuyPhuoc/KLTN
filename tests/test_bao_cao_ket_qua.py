import csv
import importlib.util
import json
from pathlib import Path

import pytest

from kiemchung import bao_cao_ket_qua as bc, truy_hoi as th

ROOT = Path(__file__).resolve().parents[1]


def tai_script(ten):
    spec = importlib.util.spec_from_file_location(ten, ROOT / f"scripts/{ten}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


danh_gia_he = tai_script("danh_gia_he")


def h(i, cum, chuan="DUNG", du=None, che_do="ten", nhom="dien_thoai", hang="Apple", loai=None):
    return {"id": f"tb-{i}", "cum": cum, "chuan": chuan, "du": du or {}, "che_do": che_do, "nhom": nhom, "hang": hang,
            "loai_bien_doi": loai, "llm_sinh": "gemini", "ma_mau": "m1"}


# Recall@k

def test_recall_k_dem_dung_va_loai_tuyen_bo_khong_bang_chung():
    hang = [h(1, "a"), h(2, "a"), h(3, "b"), h(4, "b")]
    xep = {"tb-1": ["d1", "d2"], "tb-2": ["d2", "d3", "d1"], "tb-3": ["d9", "d8", "d7"]}
    bang_chung = {"tb-1": ["d1"], "tb-2": ["d1"], "tb-3": ["d7"], "tb-4": []}
    dong = {d["k"]: d for d in bc.recall_k(hang, xep, bang_chung, "am_tiet", n=50, seed=1, ks=(1, 3))}
    assert (dong[1]["trung"], dong[1]["mau_so"]) == (1, 3)
    assert (dong[3]["trung"], dong[3]["mau_so"]) == (3, 3)
    assert dong[3]["recall"] == 1.0 and dong[3]["duoi"] == 1.0 and dong[3]["tren"] == 1.0
    assert dong[1]["duoi"] <= dong[1]["tren"]
    assert dong[1]["n_cum"] == 2 and dong[1]["cach_tach"] == "am_tiet"
    # loai khỏi mẫu số
    d2 = bc.recall_k(hang, xep, bang_chung, "tu", n=10, loai=["tb-3"], ks=(1,))[0]
    assert d2["mau_so"] == 2


def test_recall_k_mau_so_khong():
    hang = [h(1, "a")]
    d = bc.recall_k(hang, {}, {"tb-1": []}, "tu", n=10, ks=(1,))[0]
    assert d["mau_so"] == 0 and d["recall"] is None and d["duoi"] is None


# Tách tự động

def tb_tach(ma_qc, tt, gia_tri, che_do="ten", nhom="dien_thoai", llm="gemini"):
    return {"ma_qc": ma_qc, "ma_mau": "m1", "thuoc_tinh": tt, "gia_tri": {"gia_tri": gia_tri, "don_vi": "gio"},
            "che_do": che_do, "nhom": nhom, "llm_sinh": llm}


def test_tach_tu_dong_chung_va_theo_nhom():
    tay = [tb_tach("q1", "thoi_luong_pin", 30), tb_tach("q1", "sac_nhanh", 20, che_do="ten_thong_so"), tb_tach("q2", "thoi_luong_pin", 8)]
    td = [tb_tach("q1", "thoi_luong_pin", 30), tb_tach("q2", "thoi_luong_pin", 9), tb_tach("q2", "sac_nhanh", 5)]
    dong = bc.tach_tu_dong(td, tay)
    chung = dong[0]
    assert (chung["phan_nhom"], chung["gia_tri"]) == ("chung", "tat_ca")
    assert (chung["so_tu_dong"], chung["so_tach_tay"], chung["so_cap"]) == (3, 3, 1)
    assert chung["precision"] == pytest.approx(1 / 3) and chung["recall"] == pytest.approx(1 / 3)
    che_do = {d["gia_tri"]: d for d in dong if d["phan_nhom"] == "che_do"}
    assert set(che_do) == {"ten", "ten_thong_so"}
    assert che_do["ten_thong_so"]["so_tu_dong"] == 0 and che_do["ten_thong_so"]["precision"] is None
    assert che_do["ten_thong_so"]["recall"] == 0.0
    assert {d["gia_tri"] for d in dong if d["phan_nhom"] == "nhom"} == {"dien_thoai"}


def test_them_nhom_chi_dien_cho_dong_thieu():
    ds = bc.them_nhom([{"ma_mau": "m1"}, {"ma_mau": "m1", "nhom": "x"}], {"m1": {"nhom": "tai_nghe"}})
    assert [d["nhom"] for d in ds] == ["tai_nghe", "x"]


# Chi phí

def ban_ghi(i, vao, ra, lt=None, tong=None, tran=4096, loi=None, ms=None, mo_hinh="mh", ncc="gemini"):
    usage = {"input_tokens": vao, "output_tokens": ra, "reasoning_tokens": lt, "total_tokens": tong}
    return {"id": f"tb-{i}", "usage": None if vao is None else usage, "tran_token": tran, "loi": loi, "thoi_gian_sinh_ms": ms,
            "mo_hinh": mo_hinh, "nha_cung_cap": ncc}


def test_chi_phi_token_thoi_gian_goi_lai_va_loi():
    cum = {"tb-1": "a", "tb-2": "a", "tb-3": "b", "tb-9": "z"}
    b0 = [ban_ghi(1, 100, 10, tong=110, ms=2000), ban_ghi(2, 300, 30, tong=330, ms=4000, tran=8192),
          ban_ghi(3, None, None, loi="llm_khong_tra_ve_dung: x", ms=None)]
    p = [ban_ghi(1, 1000, 100, lt=50, tong=1150, tran=8192), ban_ghi(3, 500, 50, lt=0, tong=550, tran=8192)]
    dong = {d["he"]: d for d in bc.chi_phi({"B0": b0, "P": p}, cum)}
    d = dong["B0"]
    assert (d["so_tuyen_bo"], d["so_bai"]) == (3, 2)
    assert d["input_tb"] == 200 and d["output_tb"] == 20 and d["total_tb"] == 220
    assert d["reasoning_tb"] is None
    assert d["giay_tb"] == 3 and d["giay_trung_vi"] == 3
    # bài a: 2 + 4 giây = 6, bài b không có thời gian bị bỏ; token bài a = 440
    assert d["giay_tb_moi_bai"] == 6 and d["token_tb_moi_bai"] == 440
    assert d["so_goi_lai"] == 1 and d["so_loi"] == 1 and d["tran_mac_dinh"] == 4096
    assert d["usd_moi_tuyen_bo"] is None and d["usd_moi_bai"] is None
    dp = dong["P"]
    assert dp["tran_mac_dinh"] == 8192 and dp["so_goi_lai"] == 0
    assert dp["reasoning_tb"] == 25 and dp["giay_tb"] is None and dp["token_tb_moi_bai"] == 850
    # ghi đè trần
    assert bc.chi_phi({"P": p}, cum, tran_ghi_de={"P": 4096})[0]["so_goi_lai"] == 2


def test_chi_phi_usd_tinh_ca_suy_luan_va_thieu_gia():
    gia = {"mh": {"vao": 1.0, "ra": 4.0}}
    cum = {"tb-1": "a", "tb-2": "a", "tb-3": "b"}
    ds = [ban_ghi(1, 1000, 100, lt=300, tong=1400), ban_ghi(2, 1000, 100, lt=300, tong=1400),
          ban_ghi(3, 1000, 100, lt=300, tong=1400, mo_hinh="la")]
    d = bc.chi_phi({"B2": ds}, cum, gia)[0]
    ra = (1000 * 1.0 + 400 * 4.0) / 1e6  # token ra tính cả suy luận: total - input = 400
    assert d["usd_moi_tuyen_bo"] == pytest.approx(ra)
    assert d["usd_moi_bai"] == pytest.approx(2 * ra)  # bài a: 2 bản ghi; bài b thiếu giá bị bỏ


def test_token_ra_tinh_tien_khong_tinh_hai_lan_suy_luan_cua_groq():
    # không có total: Gemini cộng suy luận, Groq (completion_tokens đã gồm suy luận) thì không
    assert bc.token_ra_tinh_tien(ban_ghi(1, 10, 5, lt=3, ncc="gemini")) == 8
    assert bc.token_ra_tinh_tien(ban_ghi(1, 10, 5, lt=3, ncc="groq")) == 5
    assert bc.token_ra_tinh_tien({"usage": None}) is None


# Tỷ lệ theo chế độ

def test_ty_le_theo_che_do_dem_lech_sai_va_dong_trong():
    hang = [h(1, "a", "LECH"), h(2, "a", "SAI"), h(3, "b", "DUNG"), h(4, "b", "LECH")]
    dong = {d["che_do"]: d for d in bc.ty_le_theo_che_do(hang, n=50)}
    d = dong["ten"]
    assert (d["n"], d["so_lech"], d["so_sai"]) == (4, 2, 1)
    assert d["ty_le_lech"] == 0.5 and d["ty_le_sai"] == 0.25
    assert d["lech_duoi"] <= d["lech_tren"]
    t = dong["ten_thong_so"]
    assert t["n"] == 0 and t["ty_le_lech"] is None and t["lech_duoi"] is None
    assert dong["tat_ca"]["n"] == 4


# Độ bao phủ

def ban_p(i, dong_d, nn=None, ghi_chu=()):
    return {"id": f"tb-{i}", "dong_d": dong_d, "ghi_chu": list(ghi_chu), "vet": {"nguyen_nhan": nn} if nn else {}}


def test_ly_do_chua_du_phan_loai():
    assert bc.ly_do_chua_du(ban_p(1, "D1a", {"loai": "chua_xac_dinh", "cum": "x", "dieu_kien_la": True})) == "dieu_kien_la"
    assert bc.ly_do_chua_du(ban_p(1, "D1a", {"loai": "chua_xac_dinh", "cum": "x"})) == "chua_xac_dinh_khac"
    assert bc.ly_do_chua_du(ban_p(1, "D1a", {"loai": "mac_dinh", "khoa": ["a"]})) == "khong_co_mac_dinh"
    assert bc.ly_do_chua_du(ban_p(1, "D1a", {"loai": "trich_xuat_that_bai"})) == "trich_xuat_that_bai"
    assert bc.ly_do_chua_du(ban_p(1, "D1b")) == "mau_thuan_tai_lieu"
    assert bc.ly_do_chua_du(ban_p(1, "D3")) is None


def test_bao_phu_theo_hang_va_nhom_va_dieu_kien_khac():
    hang = [h(1, "a", hang="Apple"), h(2, "a", hang="Apple"), h(3, "b", hang="Samsung", nhom="tai_nghe"), h(4, "b", hang="Samsung")]
    p = [ban_p(1, "D1a", {"loai": "chua_xac_dinh", "dieu_kien_la": True}), ban_p(2, "D1b"), ban_p(3, "D3"),
         ban_p(4, "D1a", {"loai": "chua_xac_dinh"})]
    tx = [{"id": "tb-1", "bang_chung": [{"gia_tri": 1, "dieu_kien_khac": [{"cum": "x"}]}, {"gia_tri": 2, "dieu_kien_khac": []},
                                          {"gia_tri": None, "dieu_kien_khac": [{"cum": "y"}]}]},
          {"id": "tb-3", "bang_chung": [{"gia_tri": 3}]}]
    dong = {(d["chieu"], d["gia_tri"]): d for d in bc.bao_phu(hang, p, tx)}
    t = dong[("tat_ca", "tat_ca")]
    assert t["n_tuyen_bo"] == 4 and t["n_gia_tri_bang_chung"] == 3 and t["n_co_dieu_kien_khac"] == 1
    assert t["ty_le_co_dieu_kien_khac"] == pytest.approx(1 / 3)
    assert (t["n_dieu_kien_la"], t["n_mau_thuan_tai_lieu"], t["n_chua_xac_dinh_khac"]) == (1, 1, 1)
    assert t["n_chua_xac_dinh_pham_vi"] == 3 and t["ty_le_chua_xac_dinh_pham_vi"] == 0.75
    assert dong[("hang", "Apple")]["n_dieu_kien_la"] == 1 and dong[("hang", "Samsung")]["n_dieu_kien_la"] == 0
    assert dong[("nhom", "tai_nghe")]["n_tuyen_bo"] == 1
    # không có bản ghi trích xuất thì các cột dieu_kien_khac để trống
    khong = bc.bao_phu(hang, p)
    assert "n_gia_tri_bang_chung" not in khong[0]


# Bỏ nhóm

def test_bang_bo_nhom_bo_theo_tuyen_bo_cho_moi_he():
    hang = [h(1, "a", "SAI", {"P": "CHUA_DU", "B0": "DUNG"}), h(2, "a", "DUNG", {"P": "DUNG", "B0": "DUNG"}),
            h(3, "b", "LECH", {"P": "LECH", "B0": "DUNG"}), h(4, "b", "DUNG", {"P": "CHUA_DU", "B0": "DUNG"})]
    p = [ban_p(1, "D1b"), ban_p(2, "D3", ghi_chu=["mau_thuan_khop_ca_hai=1/2"]), ban_p(3, "D4"), ban_p(4, "D1b"),
         ban_p(99, "D1b")]  # tb-99 ngoài mẫu không tính
    dong = {(d["he"], d["kich_ban"]): d for d in bc.bang_bo_nhom(hang, ["P", "B0"], p)}
    g = dong[("B0", "giu_tat_ca")]
    assert (g["so_d1b"], g["so_mau_thuan"], g["so_giao"], g["so_ca_bo"]) == (2, 1, 0, 0)
    assert (g["far_tu"], g["far_mau"]) == (2, 2) and (g["recall_dung_tu"], g["recall_dung_mau"]) == (2, 2)
    b = dong[("B0", "bo_D1b")]
    assert b["n"] == 2 and (b["far_tu"], b["far_mau"]) == (1, 1) and b["so_ca_bo"] == 2
    assert dong[("P", "bo_D1b")]["recall_dung"] == 1.0 and dong[("P", "giu_tat_ca")]["recall_dung"] == 0.5
    assert dong[("P", "bo_ca_hai")]["n"] == 1 and dong[("P", "bo_ca_hai")]["far_mau"] == 1
    assert dong[("P", "bo_mau_thuan")]["so_ca_bo"] == 1


# F1 Lệch theo loại

def test_f1_lech_theo_loai_va_ca_tap():
    hang = [h(1, "a", "LECH", {"P": "LECH"}, loai="bo_dieu_kien"), h(2, "a", "LECH", {"P": "DUNG"}, loai="bo_dieu_kien"),
            h(3, "b", "LECH", {"P": "LECH"}, loai="doi_bo_phan"), h(4, "b", "DUNG", {"P": "LECH"}, loai="doi_bo_phan")]
    dong = {d["loai_bien_doi"]: d for d in bc.f1_lech_theo_loai(hang, ["P"], n=30)}
    assert set(dong) == {"(ca_tap)", "bo_dieu_kien", "doi_bo_phan"}
    assert dong["bo_dieu_kien"]["n"] == 2 and dong["bo_dieu_kien"]["n_lech_chuan"] == 2
    assert dong["bo_dieu_kien"]["precision_lech"] == 1.0 and dong["bo_dieu_kien"]["recall_lech"] == 0.5
    assert dong["bo_dieu_kien"]["f1_lech"] == pytest.approx(2 / 3)
    assert dong["doi_bo_phan"]["precision_lech"] == 0.5
    assert dong["(ca_tap)"]["n"] == 4 and dong["(ca_tap)"]["f1_lech_duoi"] <= dong["(ca_tap)"]["f1_lech_tren"]


# Tích hợp với scripts/danh_gia_he.py

def ghi_jsonl(duong, ds):
    duong.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in ds), encoding="utf-8")


def doc_csv(duong):
    with open(duong, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


@pytest.fixture
def mo_hinh(tmp_path):
    """Sáu tuyên bố thường ở mẫu m1, hai hệ (P có dong_d, vet), một cặp tối thiểu, nguồn truy hồi giả."""
    nhan_chuan = ["DUNG", "SAI", "LECH", "LECH", "DUNG", "CHUA_DU"]
    tb = [{"id": f"tb-{i:05d}", "ma_qc": f"q{(i - 1) // 2}", "ma_mau": "m1", "tuyen_bo": f"pin {i} giờ", "llm_sinh": "gemini",
           "che_do": "ten" if i <= 3 else "ten_thong_so"} for i in range(1, 7)]
    tb.append({"id": "ct-00001-bo_dieu_kien", "ma_qc": "x", "ma_mau": "m1", "tuyen_bo": "pin 1 giờ", "che_do": "ten", "llm_sinh": "gemini"})
    nhan = [{"id": f"tb-{i:05d}", "nhan": n, "dong_d": "D3", "ghi_chu": "", "bang_chung": ["m1#001"] if i != 6 else []}
            for i, n in enumerate(nhan_chuan, 1)]
    nhan.append({"id": "ct-00001-bo_dieu_kien", "nhan": "LECH", "dong_d": "D4", "ghi_chu": "", "bang_chung": ["m1#001"]})
    du_p = ["DUNG", "CHUA_DU", "LECH", "LECH", "DUNG", "CHUA_DU"]
    p = [{"id": f"tb-{i:05d}", "nhan": n, "dong_d": "D1b" if i == 2 else "D3", "ghi_chu": [], "vet": {}} for i, n in enumerate(du_p, 1)]
    p.append({"id": "ct-00001-bo_dieu_kien", "nhan": "LECH", "dong_d": "D4", "ghi_chu": [], "vet": {}})
    b0 = [{"id": f"tb-{i:05d}", "nhan": "DUNG"} for i in range(1, 7)] + [{"id": "ct-00001-bo_dieu_kien", "nhan": "DUNG"}]
    for ten, ds in (("tb", tb), ("nhan", nhan), ("p", p), ("b0", b0)):
        ghi_jsonl(tmp_path / f"{ten}.jsonl", ds)
    (tmp_path / "chia_tap.json").write_text(json.dumps({"kiem_tra": {"mau": ["m1"]}, "phat_trien": {"mau": []}}), encoding="utf-8")
    (tmp_path / "mau.csv").write_text("ma_mau,nhom,hang,ten\nm1,dien_thoai,Apple,A\n", encoding="utf-8")
    nguon = tmp_path / "nguon" / "m1"
    nguon.mkdir(parents=True)
    ghi_jsonl(nguon / "doan.jsonl", [{"id": f"m1#00{i}", "ma_mau": "m1", "noi_dung": nd}
                                    for i, nd in enumerate(["pin 1 giờ liên tục", "camera 48 chấm", "màn hình sáng"], 1)])
    return tmp_path


def chay(tmp, *them, ra="ra", cap_toi_thieu=False):
    argv = ["--nhan", str(tmp / "nhan.jsonl"), "--tuyen-bo", str(tmp / "tb.jsonl"), "--chia-tap", str(tmp / "chia_tap.json"),
            "--mau-san-pham", str(tmp / "mau.csv"), "--ra", str(tmp / ra), "--n-bootstrap", "50", "--tap", "kiem_tra",
            "--he", f"P={tmp / 'p.jsonl'}", "--he", f"B0={tmp / 'b0.jsonl'}"]
    if cap_toi_thieu:
        argv.append("--cap-toi-thieu")
    return danh_gia_he.main(argv + [str(x) for x in them]), tmp / ra


def test_khong_truyen_tham_so_thi_khong_ghi_tep_phu(mo_hinh):
    ma, ra = chay(mo_hinh)
    assert ma == 0
    for ten in ("recall_k", "tach_tu_dong", "chi_phi", "ty_le_theo_che_do", "bao_phu", "bang_bo_nhom", "loai_bien_doi"):
        assert not (ra / f"{ten}.csv").exists()


def test_recall_k_csv_tu_script(mo_hinh):
    ma, ra = chay(mo_hinh, "--recall-k", "--cach-tach", "am_tiet", "--thu-muc-nguon", mo_hinh / "nguon")
    assert ma == 0
    dong = doc_csv(ra / "recall_k.csv")
    assert [d["k"] for d in dong] == [str(k) for k in th.KS]
    assert dong[0]["mau_so"] == "5"  # tb-6 không có bằng chứng
    assert float(dong[-1]["recall"]) == 1.0 and dong[0]["cach_tach"] == "am_tiet"


def test_tach_tu_dong_csv_va_thieu_mot_tep(mo_hinh, capsys):
    tay = [tb_tach("q1", "thoi_luong_pin", 30), tb_tach("q2", "thoi_luong_pin", 8)]
    td = [tb_tach("q1", "thoi_luong_pin", 30)]
    for d in tay + td:
        del d["nhom"]
    ghi_jsonl(mo_hinh / "tay.jsonl", tay)
    ghi_jsonl(mo_hinh / "td.jsonl", td)
    ma, ra = chay(mo_hinh, "--tach-tu-dong", mo_hinh / "td.jsonl", "--tach-tay", mo_hinh / "tay.jsonl")
    assert ma == 0
    dong = doc_csv(ra / "tach_tu_dong.csv")
    assert dong[0]["phan_nhom"] == "chung" and dong[0]["precision"] == "1.0" and dong[0]["recall"] == "0.5"
    assert any(d["phan_nhom"] == "nhom" and d["gia_tri"] == "dien_thoai" for d in dong)
    with pytest.raises(SystemExit):
        chay(mo_hinh, "--tach-tu-dong", mo_hinh / "td.jsonl")


def test_chi_phi_csv_va_gia_token(mo_hinh):
    b0 = [{**ban_ghi(i, 100, 10, tong=110, ms=1000), "id": f"tb-{i:05d}"} for i in range(1, 7)]
    ghi_jsonl(mo_hinh / "cp_b0.jsonl", b0)
    (mo_hinh / "gia.json").write_text(json.dumps({"mh": {"vao": 1.0, "ra": 2.0}}), encoding="utf-8")
    ma, ra = chay(mo_hinh, "--chi-phi", f"B0={mo_hinh / 'cp_b0.jsonl'}", "--gia-token", mo_hinh / "gia.json", ra="ra2")
    assert ma == 0
    d = doc_csv(mo_hinh / "ra2" / "chi_phi.csv")[0]
    assert d["he"] == "B0" and d["so_tuyen_bo"] == "6" and d["so_bai"] == "3" and d["giay_tb"] == "1.0"
    assert float(d["usd_moi_tuyen_bo"]) == pytest.approx((100 * 1 + 10 * 2) / 1e6)
    # không có --gia-token thì cột USD trống
    chay(mo_hinh, "--chi-phi", f"B0={mo_hinh / 'cp_b0.jsonl'}", ra="ra3")
    assert doc_csv(mo_hinh / "ra3" / "chi_phi.csv")[0]["usd_moi_tuyen_bo"] == ""


def test_ty_le_bao_phu_bo_nhom_tu_script(mo_hinh):
    ma, ra = chay(mo_hinh, "--ty-le-che-do", "--bao-phu", "--bang-bo-nhom")
    assert ma == 0
    che_do = {d["che_do"]: d for d in doc_csv(ra / "ty_le_theo_che_do.csv")}
    assert che_do["ten"]["n"] == "3" and che_do["ten"]["so_sai"] == "1" and che_do["ten_thong_so"]["so_lech"] == "1"
    bao_phu = {(d["chieu"], d["gia_tri"]): d for d in doc_csv(ra / "bao_phu.csv")}
    assert bao_phu[("tat_ca", "tat_ca")]["n_mau_thuan_tai_lieu"] == "1"
    assert bao_phu[("tat_ca", "tat_ca")]["n_gia_tri_bang_chung"] == ""  # không đưa --trich-xuat
    assert ("hang", "Apple") in bao_phu and ("nhom", "dien_thoai") in bao_phu
    bo = {(d["he"], d["kich_ban"]): d for d in doc_csv(ra / "bang_bo_nhom.csv")}
    assert bo[("P", "giu_tat_ca")]["so_d1b"] == "1"
    assert bo[("B0", "bo_D1b")]["n"] == "5" and bo[("B0", "bo_D1b")]["far_mau"] == "3"


def test_f1_lech_theo_loai_can_cap_toi_thieu(mo_hinh, capsys):
    with pytest.raises(SystemExit):
        chay(mo_hinh, "--f1-lech-theo-loai")
    ma, ra = chay(mo_hinh, "--f1-lech-theo-loai", cap_toi_thieu=True)
    assert ma == 0
    dong = doc_csv(ra / "loai_bien_doi.csv")
    assert {d["loai_bien_doi"] for d in dong} == {"(ca_tap)", "bo_dieu_kien"}


def test_bao_phu_thieu_dong_d_bao_loi(mo_hinh, capsys):
    ghi_jsonl(mo_hinh / "p.jsonl", [{"id": f"tb-{i:05d}", "nhan": "DUNG"} for i in range(1, 7)] + [{"id": "ct-00001-bo_dieu_kien", "nhan": "DUNG"}])
    with pytest.raises(SystemExit):
        chay(mo_hinh, "--bao-phu")
    assert "dong_d" in capsys.readouterr().err


# Hình

def test_ve_hinh_tao_png(tmp_path):
    pytest.importorskip("matplotlib")
    ve = tai_script("ve_hinh_ket_qua")
    vao, ra = tmp_path / "vao", tmp_path / "ra"
    vao.mkdir()

    def viet(ten, cot, dong):
        with open(vao / ten, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(cot)
            w.writerows(dong)
    viet("bang_chinh.csv", ["he", "far_diem", "far_duoi", "far_tren", "macro_f1_diem", "macro_f1_duoi", "macro_f1_tren"],
         [["P", 0.1, 0.05, 0.2, 0.7, 0.6, 0.8], ["B0", 0.4, 0.3, 0.5, 0.5, 0.4, 0.6]])
    for he in ("P", "B2"):
        viet(f"nham_lan_{he}.csv", ["nhan_chuan", "DUNG", "SAI", "LECH", "CHUA_DU", "LOI", "tong"],
             [[x, 3, 1, 0, 2, 0, 6] for x in ("DUNG", "SAI", "LECH", "CHUA_DU")])
    viet("recall_k.csv", ["cach_tach", "k", "recall", "duoi", "tren"],
         [[c, k, 0.5 + k / 20, 0.4, 0.9] for c in ("am_tiet", "tu") for k in (1, 3, 5, 8)])
    viet("ty_le_theo_che_do.csv", ["che_do", "n", "ty_le_lech", "lech_duoi", "lech_tren", "ty_le_sai", "sai_duoi", "sai_tren"],
         [["ten", 10, 0.3, 0.1, 0.5, 0.2, 0.1, 0.3], ["ten_thong_so", 0, "", "", "", "", "", ""], ["tat_ca", 10, 0.3, 0.1, 0.5, 0.2, 0.1, 0.3]])
    da_ve = ve.ve_tat_ca(vao, ra)
    assert {d.name for d in da_ve} == {"far_theo_he.png", "macro_f1_theo_he.png", "nham_lan_P.png", "nham_lan_B2.png", "recall_k.png",
                                       "ty_le_che_do.png"}
    assert all(d.stat().st_size > 1000 and d.read_bytes()[:4] == b"\x89PNG" for d in da_ve)
    # thư mục không có CSV thì không vẽ gì
    assert ve.ve_tat_ca(tmp_path / "ra", tmp_path / "ra2") == []
    assert ve.main(["--vao", str(vao), "--ra", str(tmp_path / "ra3")]) == 0
