import pytest

from kiemchung import danh_gia as dg, thong_ke as tk

# Ba tuyên bố chuẩn DUNG (một đoán LOI), hai SAI, hai LECH, một CHUA_DU
CAP = [("DUNG", "DUNG"), ("DUNG", "SAI"), ("DUNG", "LOI"), ("SAI", "DUNG"), ("SAI", "SAI"),
       ("LECH", "LECH"), ("LECH", "SAI"), ("CHUA_DU", "CHUA_DU")]


def test_nhan_du_doan_co_lech_va_b0_van_cot_lech_bang_0():
    assert dg.NHAN_DU_DOAN == ("DUNG", "SAI", "LECH", "CHUA_DU", "LOI")
    chuan = {"a": "LECH", "b": "DUNG"}
    bang = dg.bang_nham_lan(chuan, {"a": "SAI", "b": "DUNG"})
    assert all(hang["LECH"] == 0 for hang in bang.values())
    assert dg.bang_nham_lan(chuan, {"a": "LECH", "b": "DUNG"})["LECH"]["LECH"] == 1


def test_prf_tung_nhan_tinh_tay_loi_la_fn_cua_nhan_chuan():
    prf = dg.prf_tung_nhan(CAP)
    assert list(prf) == list(dg.NHAN_CHUAN)
    # DUNG: tp 1, fp 1 (SAI->DUNG), fn 2 (SAI, LOI)
    assert (prf["DUNG"]["tp"], prf["DUNG"]["fp"], prf["DUNG"]["fn"]) == (1, 1, 2)
    assert prf["DUNG"]["precision"] == 0.5 and prf["DUNG"]["recall"] == pytest.approx(1 / 3)
    assert prf["DUNG"]["f1"] == pytest.approx(0.4)
    # SAI: tp 1, fp 2 (DUNG->SAI, LECH->SAI), fn 1
    assert (prf["SAI"]["tp"], prf["SAI"]["fp"], prf["SAI"]["fn"]) == (1, 2, 1)
    assert prf["SAI"]["f1"] == pytest.approx(0.4)
    assert prf["LECH"]["f1"] == pytest.approx(2 / 3)
    assert prf["CHUA_DU"]["f1"] == 1.0
    assert dg.macro_f1(CAP) == pytest.approx((0.4 + 0.4 + 2 / 3 + 1) / 4)


def test_prf_chia_cho_0_nhu_zero_division_0():
    prf = dg.prf_tung_nhan([("DUNG", "DUNG")])
    assert prf["SAI"] == {"tp": 0, "fp": 0, "fn": 0, "precision": 0.0, "recall": 0.0, "f1": 0.0}
    assert prf["DUNG"]["f1"] == 1.0
    assert dg.macro_f1([("DUNG", "DUNG")]) == pytest.approx(0.25)
    # đoán LECH mà chuẩn không có LECH: precision 0 (tp 0, fp 1), recall 0 (mẫu số 0)
    prf = dg.prf_tung_nhan([("DUNG", "LECH")])
    assert prf["LECH"]["precision"] == 0.0 and prf["LECH"]["recall"] == 0.0 and prf["LECH"]["f1"] == 0.0
    assert dg.macro_f1([]) == 0.0


def test_far_recall_voi_loi_va_ty_le():
    # khác DUNG: SAI, SAI, LECH, LECH, CHUA_DU (5), chấp nhận nhầm 1; DUNG 3, trúng 1; LOI không là chấp nhận
    assert dg.dem_far(CAP) == (1, 5) and dg.dem_recall_dung(CAP) == (1, 3)
    assert dg.ty_le_far(CAP) == pytest.approx(0.2) and dg.ty_le_recall_dung(CAP) == pytest.approx(1 / 3)
    assert dg.dem_loi_cap(CAP) == 1
    assert dg.ty_le_far([("DUNG", "DUNG")]) is None
    assert dg.ty_le_recall_dung([("SAI", "SAI")]) is None
    # cặp lặp (bootstrap): mỗi lần xuất hiện tính một lần
    assert dg.dem_far(CAP + CAP) == (2, 10)
    # vỏ bọc dict cho cùng kết quả
    chuan = {f"t{i}": h for i, (h, _) in enumerate(CAP)}
    du = {f"t{i}": c for i, (_, c) in enumerate(CAP)}
    assert dg.tinh_far(chuan, du) == (1, 5) and dg.tinh_recall_dung(chuan, du) == (1, 3)


# Bootstrap

HANG = [{"id": f"t{i}", "cum": f"c{i // 2}", "x": i} for i in range(10)]


def trung_binh(ds):
    return sum(r["x"] for r in ds) / len(ds) if ds else None


def test_bootstrap_tat_dinh_cung_seed_va_khac_seed():
    a = tk.bootstrap_cum(HANG, lambda r: r["cum"], trung_binh, n=200, seed=7)
    b = tk.bootstrap_cum(HANG, lambda r: r["cum"], trung_binh, n=200, seed=7)
    c = tk.bootstrap_cum(HANG, lambda r: r["cum"], trung_binh, n=200, seed=8)
    assert a == b and a != c
    assert a["diem"] == 4.5 and a["n"] == 200 and a["seed"] == 7 and a["so_vong_bo"] == 0
    assert a["duoi"] < a["tren"]


def test_bootstrap_rut_theo_cum_va_cum_lap_thi_ban_ghi_lap():
    vong = []

    def ham(ds):
        vong.append(ds)
        return 0.0

    tk.bootstrap_cum(HANG, {r["id"]: r["cum"] for r in HANG}, ham, n=50, seed=1)  # cum là dict theo id
    assert vong[-1] == HANG  # lần gọi cuối là dữ liệu gốc
    for ds in vong[:-1]:
        assert len(ds) == 10  # 5 cụm, mỗi cụm 2 bản ghi
        dem = {}
        for r in ds:
            dem[r["id"]] = dem.get(r["id"], 0) + 1
        for k in range(5):  # hai bản ghi cùng cụm luôn xuất hiện số lần bằng nhau
            assert dem.get(f"t{2 * k}", 0) == dem.get(f"t{2 * k + 1}", 0)
    assert any(len(ds) != len({r["id"] for r in ds}) for ds in vong[:-1])  # có vòng rút cụm hai lần


def test_bootstrap_so_vong_bo_khong_tinh_vao_phan_vi():
    hang = [{"id": "a", "cum": "c0", "v": 1.0}, {"id": "b", "cum": "c1", "v": None}, {"id": "c", "cum": "c2", "v": None}]

    def ham(ds):
        v = [r["v"] for r in ds if r["v"] is not None]
        return sum(v) / len(v) if v else None

    r = tk.bootstrap_cum(hang, lambda r: r["cum"], ham, n=300, seed=3)
    assert 0 < r["so_vong_bo"] < 300  # vòng không rút trúng c0 (xác suất (2/3)^3) thì ham trả None
    assert r["duoi"] == 1.0 and r["tren"] == 1.0 and r["diem"] == 1.0
    tat_ca_bo = tk.bootstrap_cum(hang, lambda r: r["cum"], lambda ds: None, n=10)
    assert tat_ca_bo["so_vong_bo"] == 10 and tat_ca_bo["duoi"] is None and tat_ca_bo["diem"] is None


def test_bootstrap_hieu_hai_he_giong_het_ci_bang_0_va_dung_chung_mau_cum():
    r = tk.bootstrap_hieu(HANG, lambda r: r["cum"], trung_binh, trung_binh, n=100, seed=5)
    assert (r["diem"], r["duoi"], r["tren"]) == (0, 0, 0)
    # cùng mẫu cụm trong mỗi vòng nên hiệu với (trung bình + 1) luôn là -1
    r = tk.bootstrap_hieu(HANG, lambda r: r["cum"], trung_binh, lambda ds: trung_binh(ds) + 1, n=100, seed=5)
    assert r["duoi"] == pytest.approx(-1) and r["tren"] == pytest.approx(-1)


def test_phan_vi_noi_suy():
    assert tk.phan_vi([1, 2, 3, 4, 5], 0.5) == 3
    assert tk.phan_vi([0, 10], 0.25) == 2.5
    assert tk.phan_vi([], 0.5) is None


# McNemar, Holm

def dat_nhan(*ds):
    return {f"t{i}": n for i, n in enumerate(ds)}


def test_mcnemar_tinh_tay():
    chuan = dat_nhan("DUNG", "SAI", "SAI", "LECH", "LECH", "CHUA_DU", "SAI", "SAI")
    # t0 chuẩn DUNG nên bỏ. A chấp nhận ở t1, t2; B chấp nhận ở t3, t4, t5, t6 (t7 cả hai không chấp nhận)
    a = dat_nhan("DUNG", "DUNG", "DUNG", "SAI", "SAI", "SAI", "SAI", "SAI")
    b = dat_nhan("SAI", "SAI", "SAI", "DUNG", "DUNG", "DUNG", "DUNG", "SAI")
    r = tk.mcnemar(chuan, a, b)
    assert (r["b"], r["c"], r["n"]) == (2, 4, 6)
    # p = 2 * P(X <= 2), X ~ Bin(6, .5): 2 * (1 + 6 + 15) / 64
    assert r["p"] == pytest.approx(2 * 22 / 64)
    # b = 0, c = 5: p = 2 * 1 / 32
    a2 = dat_nhan("DUNG", "SAI", "SAI", "SAI", "SAI", "SAI", "SAI", "SAI")
    b2 = dat_nhan("DUNG", "SAI", "SAI", "DUNG", "DUNG", "DUNG", "DUNG", "DUNG")
    r = tk.mcnemar(chuan, a2, b2)
    assert (r["b"], r["c"], r["n"]) == (0, 5, 5) and r["p"] == pytest.approx(2 / 32)


def test_mcnemar_n_bang_0_p_bang_1_va_chan_o_1():
    chuan = dat_nhan("SAI", "LECH", "DUNG")
    giong = dat_nhan("SAI", "DUNG", "DUNG")
    assert tk.mcnemar(chuan, giong, giong) == {"b": 0, "c": 0, "n": 0, "p": 1.0}
    # b = 3, c = 3: 2 * P(X <= 3) = 2 * 42 / 64 > 1, chặn ở 1
    chuan = {f"t{i}": "SAI" for i in range(6)}
    a = {f"t{i}": "DUNG" if i < 3 else "SAI" for i in range(6)}
    b = {f"t{i}": "SAI" if i < 3 else "DUNG" for i in range(6)}
    assert tk.mcnemar(chuan, a, b)["p"] == 1.0


def test_mcnemar_thieu_du_doan_bao_loi():
    with pytest.raises(ValueError, match="t1"):
        tk.mcnemar({"t0": "SAI", "t1": "SAI"}, {"t0": "DUNG"}, {"t0": "SAI", "t1": "SAI"})


def test_holm_tinh_tay_giu_don_dieu_va_chan_o_1():
    r = tk.holm({"B0": 0.01, "B1": 0.04, "B2": 0.03, "B3": 0.5})
    # sắp 0.01, 0.03, 0.04, 0.5: 4*0.01 = 0.04, 3*0.03 = 0.09, 2*0.04 = 0.08 (nâng lên 0.09), 1*0.5
    assert r == {"B0": pytest.approx(0.04), "B1": pytest.approx(0.09), "B2": pytest.approx(0.09), "B3": pytest.approx(0.5)}
    assert list(r) == ["B0", "B1", "B2", "B3"]
    assert tk.holm({"a": 0.6, "b": 0.7})["a"] == 1.0
    assert tk.holm({}) == {}
    assert tk.holm({"a": 0.2}) == {"a": 0.2}


# ghi_chu và phép đổi độ nhạy

def test_doc_ghi_chu_va_khoa_mac_dinh():
    gc = "mac_dinh=che_do_nguon,zoom; khang_dinh=lên đến; chep_nhan=x; ngoai_cau_hinh=a; b"
    d = tk.doc_ghi_chu(gc)
    assert d == {"mac_dinh": "che_do_nguon,zoom", "khang_dinh": "lên đến", "chep_nhan": "x", "ngoai_cau_hinh": "a", "b": ""}
    assert tk.khoa_mac_dinh(gc) == ["che_do_nguon", "zoom"]
    assert tk.khoa_mac_dinh("") == [] and tk.khoa_mac_dinh("mac_dinh=") == [] and tk.khoa_mac_dinh(None) == []
    assert tk.doc_ghi_chu(["mac_dinh=a", "x=y"]) == {"mac_dinh": "a", "x": "y"}


NHAN = [
    {"id": "t1", "nhan": "DUNG", "dong_d": "D3", "ghi_chu": "mac_dinh=che_do_nguon"},
    {"id": "t2", "nhan": "LECH", "dong_d": "D4", "ghi_chu": "mac_dinh=ngoai_bang,zoom; ngoai_cau_hinh=x"},
    {"id": "t3", "nhan": "CHUA_DU", "dong_d": "D1b", "ghi_chu": "mac_dinh=zoom"},
    {"id": "t4", "nhan": "SAI", "dong_d": "D5", "ghi_chu": "chep_nhan=a; nham_vai=b"},
    {"id": "t5", "nhan": "DUNG", "dong_d": "D3", "ghi_chu": "mau_thuan_khop_ca_hai=1/2; mac_dinh="},
    {"id": "t6", "nhan": "SAI", "dong_d": "D1b", "ghi_chu": ""},
]


def test_doi_mac_dinh_la_can_tren_va_khong_doi_chua_du():
    moi, so = tk.doi_mac_dinh(NHAN)
    assert moi == {"t1": "CHUA_DU", "t2": "CHUA_DU", "t3": "CHUA_DU", "t4": "SAI", "t5": "DUNG", "t6": "SAI"}
    assert so == 2  # t3 vốn đã CHUA_DU nên không tính; t5 có mac_dinh rỗng
    assert NHAN[0]["nhan"] == "DUNG"  # không sửa đầu vào


def test_doi_ngoai_bang_chi_nhom_co_khoa_ngoai_bang():
    moi, so = tk.doi_ngoai_bang(NHAN)
    assert so == 1 and moi["t2"] == "CHUA_DU" and moi["t1"] == "DUNG"


def test_ma_co_khoa_va_ma_dong():
    assert tk.ma_co_khoa(NHAN, "chep_nhan") == {"t4"}
    assert tk.ma_co_khoa(NHAN, "nham_vai") == {"t4"}
    assert tk.ma_co_khoa(NHAN, "mau_thuan_khop_ca_hai") == {"t5"}
    assert tk.ma_co_khoa(NHAN, "khong_co") == set()
    assert tk.ma_dong(NHAN, "D1b") == {"t3", "t6"}
