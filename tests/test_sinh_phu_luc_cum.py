import copy
import importlib.util
from pathlib import Path
import re

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sinh_phu_luc_cum", ROOT / "scripts/sinh_phu_luc_cum.py")
spl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spl)
spec_tc = importlib.util.spec_from_file_location("tao_cong_cu_gan_nhan_cho_phu_luc", ROOT / "scripts/tao_cong_cu_gan_nhan.py")
tc = importlib.util.module_from_spec(spec_tc)
spec_tc.loader.exec_module(tc)

TEN_YAML = ("chung", "dien_thoai", "tai_nghe", "dong_ho")


@pytest.fixture(scope="module")
def yaml_cau_hinh():
    return {ten: yaml.safe_load((ROOT / f"data/cau_hinh/{ten}.yaml").read_text(encoding="utf-8")) for ten in TEN_YAML}


@pytest.fixture(scope="module")
def phu_luc(yaml_cau_hinh):
    return spl.dung_phu_luc(*(yaml_cau_hinh[ten] for ten in TEN_YAML))


@pytest.fixture(scope="module")
def md():
    if not tc.TEP_HUONG_DAN.exists():
        pytest.skip("không có data/huong_dan_gan_nhan.md")
    return tc.doc_huong_dan()


def cum_tu_bang(cum_nhom):
    return {dk["khoa"]: {g["gia_tri"]: (g["tu_tai_lieu"], g["hieu_biet_chung"]) for g in dk["gia_tri"]} for dk in cum_nhom}


# ---------- Mục 13 của hướng dẫn khớp YAML ----------

def test_muc_13_cua_huong_dan_khop_dau_ra_cua_script():
    # Đây là phép kiểm "khớp YAML" từng chữ: sửa YAML mà chưa chạy scripts/sinh_phu_luc_cum.py --ghi thì test này báo.
    assert spl.kiem(), "mục 13 của data/huong_dan_gan_nhan.md không khớp data/cau_hinh/*.yaml; chạy scripts/sinh_phu_luc_cum.py --ghi"


def test_phu_luc_sinh_ra_doc_lai_dung_cum_cua_yaml(phu_luc, yaml_cau_hinh):
    cum = tc.bang_cum(phu_luc)
    for tien_to, ten in (("dt", "dien_thoai"), ("tn", "tai_nghe"), ("dh", "dong_ho")):
        mong = {dk: {gt: (c.get("tu_tai_lieu") or [], c.get("hieu_biet_chung") or []) for gt, c in gts.items()}
                for dk, gts in yaml_cau_hinh[ten]["cach_dien_dat"].items()}
        assert cum_tu_bang(cum["nhom"][tien_to]) == mong, ten
    chung = yaml_cau_hinh["chung"]
    bang = {c["khoa"]: c["dong"] for c in cum["chung"]}
    kieu = {d["muc_con"]: (d["tu_tai_lieu"], d["hieu_biet_chung"]) for d in bang["kieu_gia_tri"]}
    assert kieu == {k: (v["tu_tai_lieu"], v["hieu_biet_chung"]) for k, v in chung["kieu_gia_tri"].items()}
    assert bang["tu_goi_muc_cao"][0]["hieu_biet_chung"] == chung["tu_goi_muc_cao"]["hieu_biet_chung"]


def test_phu_luc_ghi_tu_khang_dinh_muc_san_va_cum_phu(phu_luc, yaml_cau_hinh):
    chung = yaml_cau_hinh["chung"]
    for tu in chung["tu_khang_dinh"]["tu"] + chung["tu_khang_dinh"]["tu_muc_san"] + chung["tu_khang_dinh"]["bo_qua_khi_co"] + chung["cum_phu"]["mau"]:
        assert f'"{tu}"' in phu_luc, tu
    assert "Nhóm mức sàn của mục 6.2 chưa có trong cấu hình" not in phu_luc


def test_gia_tri_co_khoa_phia_duoc_ghi_ro_phia(phu_luc, yaml_cau_hinh):
    assert "| `su_dung_lien_tuc` (chỉ phía tài liệu) |" in phu_luc and "| `chua_ro_hoat_dong` (chỉ phía tuyên bố) |" in phu_luc
    gia_tri_co_phia = [(gt, c["phia"]) for ten in ("dien_thoai", "tai_nghe", "dong_ho")
                       for gts in yaml_cau_hinh[ten]["cach_dien_dat"].values() for gt, c in gts.items() if "phia" in c]
    # chua_ro_hoat_dong có ở cả ba nhóm (QĐ12, 02/11); chi_mang_di_dong của đồng hồ thêm ở Bước 22 (hướng dẫn mục 11.3, V41).
    assert sorted(gia_tri_co_phia) == sorted([("su_dung_lien_tuc", "tai_lieu")] + [("chua_ro_hoat_dong", "tuyen_bo")] * 3
                                             + [("chi_mang_di_dong", "tuyen_bo")])
    assert "| `chi_mang_di_dong` (chỉ phía tuyên bố) (chỉ `thoi_luong_pin`) |" in phu_luc
    assert "| `kem_hop_sac` (chỉ `thoi_luong_pin`) |" in phu_luc
    # Giá trị không có khóa phia thì không bị ghi chú gì.
    assert "| `xem_video` |" in phu_luc and "| `chua_ro_loai_video` |" in phu_luc


def test_ngay_cua_phu_luc_lay_tu_chung_yaml(yaml_cau_hinh):
    chung = copy.deepcopy(yaml_cau_hinh["chung"])
    chung["ngay"] = "2027-01-09"
    pl = spl.dung_phu_luc(chung, *(yaml_cau_hinh[ten] for ten in TEN_YAML[1:]))
    assert "(bản ngày 09/01/2027)" in pl
    with pytest.raises(SystemExit):
        spl.ngay_dd_mm_yyyy("09/01/2027")


def test_loi_dan_nhac_toi_ma_co_that_trong_yaml(yaml_cau_hinh):
    # Lời dẫn đầu mục 13 viết tay một lần ở script; mã nào nó nhắc phải còn trong YAML, kẻo đổi YAML làm lời dẫn sai.
    dt = yaml_cau_hinh["dien_thoai"]["cach_dien_dat"]
    ma = set(re.findall(r"`([a-z0-9_]+)`", spl.LOI_DAN_DAU))
    tn = yaml_cau_hinh["tai_nghe"]["cach_dien_dat"]
    co = ({gt for gts in dt.values() for gt in gts} | {gt for gts in tn.values() for gt in gts}
          | {"phia", "chi_thuoc_tinh", "ngoai_cau_hinh", "tu_tai_lieu", "hieu_biet_chung"})
    assert ma <= co, ma - co
    assert tn["bo_phan"]["kem_hop_sac"]["chi_thuoc_tinh"] == ["thoi_luong_pin"]
    ngoai_troi = dt["che_do_hien_thi"]["ngoai_troi"]
    dong = next(d for d in spl.LOI_DAN_DAU.splitlines() if "nằm ở chế độ `ngoai_troi`" in d)
    for cum in re.findall(r'"([^"]+)"', dong.split("nằm ở chế độ")[0]):
        assert cum in ngoai_troi["tu_tai_lieu"] + ngoai_troi["hieu_biet_chung"], cum
    assert "ánh sáng mạnh" not in ngoai_troi["hieu_biet_chung"]  # QĐ14 (02/11)
    assert "Dưới ánh sáng mạnh" in dt["che_do_hien_thi"]["tu_tang_sang"]["tu_tai_lieu"]


# ---------- Hướng dẫn (mục 6.2, 6.8) và YAML nói cùng một danh sách ----------

def test_tu_khang_dinh_cua_muc_6_2_khop_chung_yaml(md, yaml_cau_hinh):
    tu = tc.tu_khang_dinh(md)
    kd = yaml_cau_hinh["chung"]["tu_khang_dinh"]
    assert tu["chac_chan"] == kd["tu"] and tu["muc_san"] == kd["tu_muc_san"]


def test_cum_phu_cua_muc_6_8_khop_chung_yaml(md, yaml_cau_hinh):
    dong = " ".join(tc.noi_dung_muc(md, "6.8"))
    doan = next(d for d in dong.split("**Cụm phủ nhiều giá trị.**")[1:])
    cau_dau = doan.split(" gắn với con số")[0]
    trong_huong_dan = re.findall(r'"([^"]+)"', cau_dau)
    assert trong_huong_dan and set(trong_huong_dan) == set(yaml_cau_hinh["chung"]["cum_phu"]["mau"])


def test_cum_moi_cua_buoc_16_co_trong_phu_luc_dung_gia_tri(md):
    cum = tc.bang_cum(md)
    dt = cum_tu_bang(cum["nhom"]["dt"])
    tn = cum_tu_bang(cum["nhom"]["tn"])
    gop = lambda c: c[0] + c[1]  # noqa: E731
    for chu in ("ánh nắng", "dưới ánh nắng"):
        assert chu in gop(dt["che_do_hien_thi"]["ngoai_troi"])
    assert "ánh sáng mạnh" not in gop(dt["che_do_hien_thi"]["ngoai_troi"])  # QĐ14 (02/11)
    assert "Dưới ánh sáng mạnh" in gop(dt["che_do_hien_thi"]["tu_tang_sang"])
    for chu in ("tổng cộng", "kết hợp hộp sạc"):
        assert chu in tn["bo_phan"]["kem_hop_sac"][1]
    assert "telephoto" in dt["loai_zoom"]["quang_hoc"][1] and "Telephoto 2x chất lượng quang học" in dt["loai_zoom"]["quang_hoc"][0]
    assert dt["hoat_dong"]["chua_ro_hoat_dong"] == ([], ["sử dụng liên tục", "dùng liên tục", "liên tục", "sử dụng", "dùng"])
    assert dt["hoat_dong"]["su_dung_lien_tuc"] == (["Sử dụng liên tục"], [])


# ---------- Chỉ mục 13 bị ghi, các mục khác giữ nguyên từng byte ----------

def van_ban_mau(sau=""):
    return "# Hướng dẫn\n\n## 1. Mục một\n\nChữ giữ nguyên.\n\n## 12. Mục mười hai\n\nBảng.\n\n## 13. Phụ lục cũ\n\nSai hết.\n" + sau


def test_thay_muc_13_chi_doi_muc_13():
    pl = "## 13. Phụ lục: mới\n\nĐúng.\n"
    truoc = "# Hướng dẫn\n\n## 1. Mục một\n\nChữ giữ nguyên.\n\n## 12. Mục mười hai\n\nBảng.\n\n"
    assert spl.thay_muc_13(van_ban_mau(), pl) == truoc + pl
    # Mục 13 không phải mục cuối: phần sau giữ nguyên, cách mục 13 một dòng trống.
    sau = "\n## 14. Mục sau\n\nCòn nguyên.\n"
    assert spl.thay_muc_13(van_ban_mau(sau), pl) == truoc + pl + sau
    # Ghi hai lần ra cùng kết quả.
    moi = spl.thay_muc_13(van_ban_mau(sau), pl)
    assert spl.thay_muc_13(moi, pl) == moi


def test_thieu_hoac_thua_tieu_de_muc_13_thi_thoat():
    with pytest.raises(SystemExit):
        spl.vi_tri_muc_13("# Hướng dẫn\n\n## 12. Mục mười hai\n")
    with pytest.raises(SystemExit):
        spl.vi_tri_muc_13("## 13. A\n\n## 13. B\n")


def test_ghi_va_kiem_tren_ban_sao(tmp_path):
    ban_sao = tmp_path / "huong_dan.md"
    goc = tc.TEP_HUONG_DAN.read_bytes() if tc.TEP_HUONG_DAN.exists() else van_ban_mau().encode("utf-8")
    ban_sao.write_bytes(goc)
    spl.ghi(ban_sao)
    assert spl.kiem(ban_sao) and spl.ghi(ban_sao) is False   # lần ghi thứ hai không đổi gì
    truoc_13 = goc[:goc.index("## 13. ".encode("utf-8"))]
    assert ban_sao.read_bytes().startswith(truoc_13)           # mục 1-12 giữ nguyên từng byte
    # Làm hỏng một ô của mục 13 thì kiểm báo lệch, ghi lại thì khớp.
    ban_sao.write_bytes(ban_sao.read_bytes().replace('"optical", "telephoto"'.encode("utf-8"), '"optical"'.encode("utf-8"), 1))
    assert spl.kiem(ban_sao) is False and spl.main(["--huong-dan", str(ban_sao)]) == 1
    assert spl.main(["--ghi", "--huong-dan", str(ban_sao)]) == 0 and spl.kiem(ban_sao)


def test_in_ra_man_hinh_dung_byte(capfd):
    assert spl.main(["--in"]) == 0
    ra = capfd.readouterr().out
    assert ra.startswith("## 13. Phụ lục: cụm diễn đạt trong cấu hình\n") and "\r" not in ra
