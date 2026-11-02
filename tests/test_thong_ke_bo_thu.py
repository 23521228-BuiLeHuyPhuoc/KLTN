import importlib.util
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("thong_ke_bo_thu", ROOT / "scripts/thong_ke_bo_thu.py")
tk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tk)

MAU = [
    {"ma_mau": "m1", "nhom": "dien_thoai", "ten": "Máy 1", "tap": "phattrien", "mau_thu": "co"},
    {"ma_mau": "m2", "nhom": "tai_nghe", "ten": "Tai 2", "tap": "phattrien", "mau_thu": "co"},
    {"ma_mau": "m3", "nhom": "dien_thoai", "ten": "Máy 3", "tap": "kiemtra", "mau_thu": "khong"},
    {"ma_mau": "m4", "nhom": "tai_nghe", "ten": "Tai 4", "tap": "kiemtra", "mau_thu": "khong"},
]
# 'a' có điều kiện bắt buộc; 'b' có khóa nhưng rỗng; 'ngoai' không có trong cấu hình.
CAU_HINH = {
    "dien_thoai": {"thuoc_tinh": {"a": {"dieu_kien_bat_buoc": {"x": "y"}}, "b": {"dieu_kien_bat_buoc": {}}}},
    "tai_nghe": {"thuoc_tinh": {"a": {"dieu_kien_bat_buoc": {"x": "y"}}, "c": {}}},
}
# Số tuyên bố mỗi bài: ten [0, 1, 2, 0] (trung bình 0,75), ten_thong_so [3, 4, 5, 3] (trung bình 3,75).
SO_TB = {("m1", "gA", "ten"): 0, ("m1", "gA", "ten_thong_so"): 3, ("m1", "gB", "ten"): 1, ("m1", "gB", "ten_thong_so"): 4,
         ("m2", "gA", "ten"): 2, ("m2", "gA", "ten_thong_so"): 5, ("m2", "gB", "ten"): 0, ("m2", "gB", "ten_thong_so"): 3}


def bo_du_lieu():
    """(bai, tuyen_bo, nhan2, nhan1) nhỏ, tự nhất quán. Thuộc tính tuyên bố xoay vòng a, b, ngoai (m1) / a, c (m2)."""
    bai, tuyen_bo = [], []
    for (ma_mau, llm, che_do), n in SO_TB.items():
        ma_qc = f"qc-{ma_mau}-{llm}-{che_do}"
        bai.append({"ma_qc": ma_qc, "ma_mau": ma_mau, "llm": llm, "loai_bai": "description", "che_do": che_do})
        ds = ("a", "b", "ngoai") if ma_mau == "m1" else ("a", "c")
        for i in range(n):
            tuyen_bo.append({"id": f"tb-{len(tuyen_bo) + 1:05d}", "ma_qc": ma_qc, "ma_mau": ma_mau,
                             "thuoc_tinh": ds[i % len(ds)], "llm_sinh": llm, "che_do": che_do, "loai_bai": "description"})
    nhan = ("DUNG", "LECH", "SAI", "CHUA_DU")
    nhan2 = [{"id": t["id"], "nhan": nhan[i % 4], "dong_d": ("D3", "D4", "D5", "D6")[i % 4], "nguoi_gan": "claude", "giay": 1}
             for i, t in enumerate(tuyen_bo)]
    nhan1 = [{"id": t["id"], "giay": 60 * (i + 1)} for i, t in enumerate(tuyen_bo)]
    return bai, tuyen_bo, nhan2, nhan1


def dem_dieu_kien():
    return {n: set(tk.thuoc_tinh_co_dieu_kien(ch)) for n, ch in CAU_HINH.items()}


# ---------- hàm tính ----------

def test_thong_ke_day_so():
    r = tk.thong_ke([0, 1, 2, 0])
    assert (r["n"], r["tong"], r["tb"], r["trung_vi"], r["nho_nhat"], r["lon_nhat"], r["so_khong"]) == (4, 3, 0.75, 0.5, 0, 2, 2)
    assert r["do_lech"] == pytest.approx(math.sqrt(2.75 / 3))  # độ lệch chuẩn mẫu, chia n - 1


def test_thong_ke_day_rong_va_mot_phan_tu():
    rong = tk.thong_ke([])
    assert rong["n"] == 0 and rong["tb"] is None and rong["do_lech"] is None and rong["so_khong"] == 0
    mot = tk.thong_ke([5])
    assert mot["tb"] == 5 and mot["do_lech"] is None


def test_thuoc_tinh_co_dieu_kien_bo_qua_rong_va_thieu():
    assert tk.thuoc_tinh_co_dieu_kien(CAU_HINH["dien_thoai"]) == ["a"]
    assert tk.thuoc_tinh_co_dieu_kien(CAU_HINH["tai_nghe"]) == ["a"]  # 'c' không có khóa dieu_kien_bat_buoc
    assert tk.thuoc_tinh_co_dieu_kien({}) == []


def test_tinh_bai_dem_ca_bai_khong_tuyen_bo_va_tuyen_bo_co_dieu_kien():
    bai, tuyen_bo, _, _ = bo_du_lieu()
    nhom = {r["ma_mau"]: r["nhom"] for r in MAU}
    r = {b["ma_qc"]: b for b in tk.tinh_bai(bai, tuyen_bo, nhom, dem_dieu_kien())}
    assert r["qc-m1-gA-ten"]["tb"] == 0 and r["qc-m1-gA-ten"]["co_dk"] == 0  # bài không có tuyên bố vẫn có mặt
    # m1/gB/ten_thong_so có 4 tuyên bố với thuộc tính a, b, ngoai, a: chỉ 'a' có điều kiện
    assert r["qc-m1-gB-ten_thong_so"]["tb"] == 4 and r["qc-m1-gB-ten_thong_so"]["co_dk"] == 2
    # m2: thuộc tính c không có điều kiện bắt buộc; m2/gA/ten_thong_so có 5 tuyên bố a, c, a, c, a
    assert r["qc-m2-gA-ten_thong_so"]["tb"] == 5 and r["qc-m2-gA-ten_thong_so"]["co_dk"] == 3
    assert sum(b["tb"] for b in r.values()) == len(tuyen_bo)


def test_tinh_bai_tuyen_bo_tro_toi_bai_la_thi_bao_loi():
    bai, tuyen_bo, _, _ = bo_du_lieu()
    tuyen_bo[0]["ma_qc"] = "qc-khong-co"
    with pytest.raises(ValueError, match="qc-khong-co"):
        tk.tinh_bai(bai, tuyen_bo, {r["ma_mau"]: r["nhom"] for r in MAU}, dem_dieu_kien())


def test_la_co_dieu_kien_thuoc_tinh_ngoai_cau_hinh_khong_tinh():
    nhom = {"m1": "dien_thoai"}
    co_dk = {"dien_thoai": {"a"}}
    assert tk.la_co_dieu_kien({"ma_mau": "m1", "thuoc_tinh": "a"}, nhom, co_dk)
    assert not tk.la_co_dieu_kien({"ma_mau": "m1", "thuoc_tinh": "zzz"}, nhom, co_dk)
    assert not tk.la_co_dieu_kien({"ma_mau": "m1", "thuoc_tinh": "a"}, nhom, {})


def test_gom_xep_theo_gia_tri():
    ban_ghi = [{"k": "b", "v": 1}, {"k": "a", "v": 2}, {"k": "b", "v": 3}]
    r = tk.gom(ban_ghi, lambda x: x["k"])
    assert list(r) == ["a", "b"] and [x["v"] for x in r["b"]] == [1, 3]


def test_uoc_tinh_mot_che_do_va_hai_che_do():
    tb, sd = tk.uoc_tinh({"ten_thong_so": 1.0}, {"ten": 1.0, "ten_thong_so": 4.0}, {"ten": 1.0, "ten_thong_so": 2.0}, 25)
    assert tb == pytest.approx(100) and sd == pytest.approx(10)  # 2 * căn 25
    tb, sd = tk.uoc_tinh({"ten": 0.5, "ten_thong_so": 0.5}, {"ten": 1.0, "ten_thong_so": 4.0},
                         {"ten": 1.0, "ten_thong_so": 2.0}, 10)
    assert tb == pytest.approx(25)  # 10 * (0,5 * 1 + 0,5 * 4)
    assert sd == pytest.approx(math.sqrt(10 * (0.5 * 1 + 0.5 * 4)))  # phương sai cộng theo phần chế độ


def test_so_bai_moi_mau():
    assert tk.so_bai_moi_mau(250, 66, 10, 2.75) == pytest.approx(184 / 10 / 2.75)
    assert tk.so_bai_moi_mau(300, 66, 10, 2.75) == pytest.approx(234 / 10 / 2.75)


@pytest.mark.parametrize("thap, cao, them, mong_doi", [
    (6.69, 8.51, (), [6, 7, 8, 9]),
    (4.33, 5.5, (), [4, 5, 6]),
    (5.2, 5.8, (), [5, 6]),  # khoảng không chứa số nguyên nào: lấy hai số nguyên kề
    (6.69, 8.51, (12,), [6, 7, 8, 9, 12]),
    (0.5, 0.9, (), [1]),  # không bao giờ dưới 1
])
def test_ung_vien_so_bai(thap, cao, them, mong_doi):
    assert tk.ung_vien_so_bai(thap, cao, them) == mong_doi


def test_gio_phut_va_bo_lon_nhat():
    assert tk.gio_phut(17238) == "4 giờ 47 phút"
    assert tk.gio_phut(3000) == "50 phút"
    assert tk.gio_phut(3599) == "1 giờ 0 phút"  # làm tròn đến phút rồi mới tách giờ
    assert tk.bo_lon_nhat([5, 1, 9, 3], 2) == [1, 3]
    assert tk.bo_lon_nhat([5, 1], 5) == []


def test_dinh_dang_so_dung_dau_phay():
    assert tk.so(2.75) == "2,75" and tk.so(2.75, 0) == "3" and tk.so(1234.5, 1) == "1234,5"
    assert tk.nguyen(17238) == "17.238" and tk.nguyen(2118.4) == "2.118" and tk.nguyen(110) == "110"
    assert tk.phan_tram(18, 66) == "27,3%" and tk.phan_tram(0, 0) == "—"
    assert tk.o_ty_le(34, 66) == "34 (51,5%)"
    assert tk.so_gon(2.0) == "2" and tk.so_gon(2.5) == "2,5" and tk.so_gon(None) == "—"
    assert tk.o_so(None) == "—" and tk.o_so(0.5) == "0,50"
    assert tk.o_van_ban("a | b\nc") == "a \\| b c"


# ---------- đọc dữ liệu và kiểm đầu vào ----------

def test_doc_bai_chi_lay_mau_bo_thu(tmp_path):
    for ma_qc, ma_mau in (("qc-1", "m1"), ("qc-2", "m3")):
        (tmp_path / f"{ma_qc}.json").write_text(json.dumps(
            {"ma_qc": ma_qc, "ma_mau": ma_mau, "mo_hinh_nha_cung_cap": "gA", "loai_bai": "social", "che_do": "ten", "noi_dung": "x"}),
            encoding="utf-8")
    (tmp_path / "thong_so").mkdir()
    (tmp_path / "thong_so" / "m1.json").write_text("{}", encoding="utf-8")  # thư mục con không phải bài
    r = tk.doc_bai(tmp_path, {"m1"})
    assert r == [{"ma_qc": "qc-1", "ma_mau": "m1", "llm": "gA", "loai_bai": "social", "che_do": "ten"}]


def test_kiem_dau_vao_du_lieu_dung_va_cac_loi():
    bai, tuyen_bo, nhan2, nhan1 = bo_du_lieu()
    assert tk.kiem_dau_vao(bai, tuyen_bo, nhan2, nhan1) == []
    sai_llm = [{**t} for t in tuyen_bo]
    sai_llm[0]["llm_sinh"] = "khac"
    assert any("llm_sinh" in e for e in tk.kiem_dau_vao(bai, sai_llm, nhan2, nhan1))
    assert any("không cùng tập" in e for e in tk.kiem_dau_vao(bai, tuyen_bo, nhan2[:-1], nhan1))
    assert any("giay" in e for e in tk.kiem_dau_vao(bai, tuyen_bo, nhan2, [{**nhan1[0], "giay": 0}, *nhan1[1:]]))
    assert any("không có trong data/quang_cao" in e for e in tk.kiem_dau_vao(bai[:1] + bai[2:], tuyen_bo, nhan2, nhan1))  # bỏ bài thứ hai (có 3 tuyên bố)


# ---------- phương án quy mô ----------

def dau_vao():
    bai, tuyen_bo, nhan2, _ = bo_du_lieu()
    nhom = {r["ma_mau"]: r["nhom"] for r in MAU}
    bai = tk.tinh_bai(bai, tuyen_bo, nhom, dem_dieu_kien())
    theo_id = {t["id"]: t for t in tuyen_bo}
    tap = {r["ma_mau"]: r["tap"] for r in MAU}
    cac_nhan = [{**theo_id[x["id"]], "llm": theo_id[x["id"]]["llm_sinh"], "nhan": x["nhan"], "dong_d": x["dong_d"],
                 "nguoi_gan": x["nguoi_gan"], "tap": tap[theo_id[x["id"]]["ma_mau"]]} for x in nhan2]
    return bai, cac_nhan, tk.tinh_dau_vao(bai, cac_nhan, MAU, {"m1", "m2"})


def test_tinh_dau_vao():
    bai, cac_nhan, dv = dau_vao()
    assert dv["san_co"] == 18 and dv["san_co_lech"] == sum(1 for x in cac_nhan if x["nhan"] == "LECH")
    assert dv["tb_che_do"] == {"ten": 0.75, "ten_thong_so": 3.75}
    assert dv["so_bai_che_do"] == {"ten": 4, "ten_thong_so": 4} and dv["so_bai_thu"] == 8
    assert dv["tb_mau_che_do"][("m1", "ten")] == 0.5 and dv["tb_mau_che_do"][("m2", "ten_thong_so")] == 4.0
    assert [r["ma_mau"] for r in dv["mau_moi"]] == ["m3", "m4"] and dv["moi_pt"] == 0 and dv["moi_kt"] == 2
    assert dv["san_co_pt"] == 18 and dv["san_co_kt"] == 0
    lech_ten, tong_ten = dv["lech_che_do"]["ten"]
    assert tong_ten == 3 and dv["ty_le_lech_che_do"]["ten"] == pytest.approx(lech_ten / 3)


def test_hang_phuong_an_tinh_tay():
    _, _, dv = dau_vao()
    h = tk.hang_phuong_an({"ten": 0.5, "ten_thong_so": 0.5}, 2, dv)  # 2 mẫu mới x 2 bài = 4 bài mới
    assert h["so_bai"] == 4 and h["tb_moi"] == pytest.approx(9) and h["tong"] == pytest.approx(27)
    sd = math.sqrt(4 * (0.5 * (2.75 / 3) + 0.5 * (2.75 / 3)))
    assert h["thap"] == pytest.approx(27 - sd) and h["cao"] == pytest.approx(27 + sd)
    # Cả 2 mẫu mới giống m1 / giống m2: trung bình mỗi bài m1 = 0,5 / 3,5, m2 = 1,0 / 4,0
    assert h["mau_thap"] == pytest.approx(18 + 4 * (0.5 * 0.5 + 0.5 * 3.5))
    assert h["mau_cao"] == pytest.approx(18 + 4 * (0.5 * 1.0 + 0.5 * 4.0))
    assert h["lech_chung"] == pytest.approx(dv["san_co_lech"] + 9 * dv["san_co_lech"] / 18)
    assert h["pt"] == pytest.approx(18) and h["kt"] == pytest.approx(9)  # hai mẫu mới đều thuộc tập kiểm tra
    assert h["trong_muc_tieu"] == "dưới"


def test_hang_phuong_an_so_sanh_voi_muc_tieu():
    _, _, dv = dau_vao()
    trong = {n: tk.hang_phuong_an({"ten_thong_so": 1.0}, n, dv)["trong_muc_tieu"] for n in (1, 30, 31, 37, 38)}
    # tổng = 18 + 2 mẫu * n * 3,75 = 18 + 7,5 n; mục tiêu 250–300
    assert trong == {1: "dưới", 30: "dưới", 31: "có", 37: "có", 38: "trên"}


# ---------- báo cáo ----------

def test_tao_bao_cao_tren_du_lieu_nho():
    bai, tuyen_bo, nhan2, nhan1 = bo_du_lieu()
    dong = tk.tao_bao_cao(bai, tuyen_bo, nhan2, nhan1, MAU, CAU_HINH)
    van_ban = "\n".join(dong)
    for muc in ("## Phân bố nhãn lượt 2", "## Số tuyên bố mỗi bài", "## Thời gian gán lượt 1", "## Phương án quy mô",
                "### Phương án (a)", "### Phương án (b)", "### Phương án (c)"):
        assert muc in van_ban
    assert "Bộ thử: 8 bài, 18 tuyên bố, 2 mẫu (Máy 1, Tai 2)." in van_ban
    assert "| Tất cả | 8 | 18 | 2,25 | 2,5 |" in van_ban  # số tuyên bố mỗi bài [0, 3, 1, 4, 2, 5, 0, 3]
    assert "| Chế độ: ten_thong_so | 4 | 15 | 3,75 |" in van_ban
    assert "| Lệch | 5 | 27,8% |" in van_ban  # nhãn xoay vòng Đúng, Lệch, Sai, Chưa đủ trên 18 tuyên bố
    assert "giữ chỗ" in van_ban  # lượt 2 có giay = 1 ở mọi dòng


def test_tao_bao_cao_dem_bai_khong_tuyen_bo_va_tuyen_bo_co_dieu_kien():
    bai, tuyen_bo, nhan2, nhan1 = bo_du_lieu()
    van_ban = "\n".join(tk.tao_bao_cao(bai, tuyen_bo, nhan2, nhan1, MAU, CAU_HINH))
    # hai bài không có tuyên bố (m1/gA/ten và m2/gB/ten) đều thuộc chế độ ten
    assert "| Chế độ: ten | 4 | 3 | 0,75 | 0,5 | 0,96 | 0 | 2 | 2/4 |" in van_ban
    # thuộc tính b (điều kiện rỗng), c (không khai báo điều kiện) và ngoai (ngoài cấu hình) không tính
    assert "Tuyên bố có điều kiện: 10/18." in van_ban
    assert "Thuộc tính không có điều kiện bắt buộc (không tính)" in van_ban


def test_muc_thoi_gian_luot_2_co_giay_khac_1_thi_khong_noi_la_giu_cho():
    nhan1 = [{"id": "tb-1", "ma_mau": "m1", "giay": 100}, {"id": "tb-2", "ma_mau": "m1", "giay": 300},
             {"id": "tb-3", "ma_mau": "m2", "giay": 200}]
    ten_mau = {"m1": "Máy 1", "m2": "Tai 2"}
    giu_cho = "\n".join(tk.muc_thoi_gian(nhan1, [{"giay": 1}] * 3, ten_mau))
    khac = "\n".join(tk.muc_thoi_gian(nhan1, [{"giay": 1}, {"giay": 50}, {"giay": 1}], ten_mau))
    assert "giá trị giữ chỗ" in giu_cho and "giá trị giữ chỗ" not in khac
    assert "| Tất cả | 3 | 10 phút | 200 | 3,3 | 200 | 3,3 | 100 | 300 |" in giu_cho
    assert "| Máy 1 | 2 | 7 phút | 200 | 3,3 | 200 | 3,3 | 100 | 300 |" in giu_cho


# ---------- dữ liệu thật của repo ----------

def test_du_lieu_that_nhat_quan_va_bao_cao_chay_duoc():
    bai, tuyen_bo, nhan2, nhan1, mau, cau_hinh_nhom = tk.tai_du_lieu()
    assert tk.kiem_dau_vao(bai, tuyen_bo, nhan2, nhan1) == []
    tinh = tk.tinh_bai(bai, tuyen_bo, {r["ma_mau"]: r["nhom"] for r in mau},
                       {n: set(tk.thuoc_tinh_co_dieu_kien(ch)) for n, ch in cau_hinh_nhom.items()})
    assert sum(b["tb"] for b in tinh) == len(tuyen_bo)  # mọi tuyên bố rơi vào đúng một bài
    assert all(0 <= b["co_dk"] <= b["tb"] for b in tinh)
    van_ban = "\n".join(tk.tao_bao_cao(bai, tuyen_bo, nhan2, nhan1, mau, cau_hinh_nhom))
    assert "## Phương án quy mô" in van_ban and f"{len(tuyen_bo)} tuyên bố" in van_ban
