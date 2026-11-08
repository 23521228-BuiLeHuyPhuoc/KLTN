import csv
import importlib.util
import json
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ra_tach", ROOT / "scripts/ra_tach.py")
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)
tc = rt.tc

TU_KHANG_DINH = {"chac_chan": ["luôn", "đảm bảo", "bảo đảm", "ít nhất", "mọi lúc"],
                 "muc_san": ["hơn <số>", "trên <số>", "không dưới <số>", "<số> trở lên"]}
BO_QUA = ["không đảm bảo", "không được đảm bảo", "không bảo đảm", "không phải lúc nào", "không luôn"]


def tb(ma_mau, thuoc_tinh, cau_goc, tuyen_bo, ma="tb-00001"):
    return {"id": ma, "ma_mau": ma_mau, "thuoc_tinh": thuoc_tinh, "cau_goc": cau_goc, "tuyen_bo": tuyen_bo}


def tach(ma_mau, thuoc_tinh, cau_goc, tuyen_bo, loc=True):
    return rt.ra_tach_mot(tb(ma_mau, thuoc_tinh, cau_goc, tuyen_bo), TU_KHANG_DINH, BO_QUA, loc)


@pytest.fixture(scope="module")
def md():
    if not tc.TEP_HUONG_DAN.exists():
        pytest.skip("không có data/huong_dan_gan_nhan.md")
    return tc.doc_huong_dan()


# ---------- Cụm của cấu hình khớp phụ lục mục 13 ----------

def test_chuan_nfc_bo_ngoac_gop_khoang_trang():
    assert rt.chuan("  Xem  video\n(trực  tuyến) ") == "Xem video trực tuyến"
    assert rt.chuan(None) == "" and rt.chuan("Đồng hồ") == rt.chuan("Đồng hồ")  # NFD và NFC ra cùng kết quả


def gia_tri_chi_phia_tai_lieu(nhom):
    """{"<điều kiện>=<giá trị>"} của các giá trị có khóa phia: tai_lieu trong yaml nhóm (phụ lục mục 13 ghi "(chỉ phía tài liệu)")."""
    y = rt.doc_yaml(rt.YAML_NHOM[nhom])
    return {f"{dk}={gt}" for dk, gts in y["cach_dien_dat"].items() for gt, c in gts.items() if c.get("phia") == "tai_lieu"}


def test_cum_dieu_kien_khong_loc_khop_phu_luc_muc_13(md):
    # Mọi cụm script dò (không lọc theo thuộc tính) là đúng các cụm in ở phụ lục mục 13 của hướng dẫn, trừ cụm ngữ cảnh và các
    # giá trị chỉ đọc ở phía tài liệu (câu gốc và tuyên bố là chữ của quảng cáo).
    cum = tc.bang_cum(md)
    chung = {"kieu_gia_tri": {}, "cum_quan_he": {}}
    tu_goi = []
    for c in cum["chung"]:
        for d in c["dong"]:
            ds = d["tu_tai_lieu"] + d["hieu_biet_chung"]
            if c["khoa"] in chung and ds:
                chung[c["khoa"]][d["muc_con"]] = ds
            elif c["khoa"] == "tu_goi_muc_cao":
                tu_goi = ds
    for nhom in ("dt", "tn", "dh"):
        ra = dict(rt.nhom_cum(nhom, None, False))
        mong = {f"kieu_gia_tri={k}": v for k, v in chung["kieu_gia_tri"].items()}
        mong.update({f"cum_quan_he={k}": v for k, v in chung["cum_quan_he"].items()})
        mong["tu_goi_muc_cao"] = tu_goi
        for dk in cum["nhom"][nhom]:
            mong.update({f"{dk['khoa']}={g['gia_tri']}": g["tu_tai_lieu"] + g["hieu_biet_chung"] for g in dk["gia_tri"]
                         if g["tu_tai_lieu"] + g["hieu_biet_chung"]})
        for ma in gia_tri_chi_phia_tai_lieu(nhom):
            del mong[ma]
        assert ra == mong, nhom


def test_gia_tri_phia_tai_lieu_bi_bo_gia_tri_phia_tuyen_bo_duoc_do():
    # "Sử dụng liên tục" là tên bài đo của Xiaomi 15T (phía tài liệu); ở quảng cáo, "liên tục" chưa nêu hoạt động (mục 6.8, ý 3).
    assert gia_tri_chi_phia_tai_lieu("dt") == {"hoat_dong=su_dung_lien_tuc"} and not gia_tri_chi_phia_tai_lieu("tn")
    ma = dict(rt.nhom_cum("dt", "thoi_luong_pin", True))
    assert "hoat_dong=su_dung_lien_tuc" not in ma
    assert ma["hoat_dong=chua_ro_hoat_dong"] == ["sử dụng liên tục", "dùng liên tục", "liên tục", "sử dụng", "dùng"]  # QĐ12
    mau = ("dt-apple-iphone17", "thoi_luong_pin")
    # Câu gốc có "sử dụng liên tục" mà tuyên bố bỏ thì liệt kê là chưa nêu hoạt động, không phải hoạt động su_dung_lien_tuc.
    assert tach(*mau, "Pin siêu bền 24 giờ sử dụng liên tục", "Pin siêu bền 24 giờ") == {"hoat_dong=chua_ro_hoat_dong": ["sử dụng liên tục"]}
    assert tach(*mau, "Pin 24 giờ sử dụng liên tục", "Pin 24 giờ dùng liên tục") == {}   # cùng giá trị thì tuyên bố đã có


def test_cum_moi_cua_buoc_16_nam_dung_gia_tri():
    # QĐ2 (mục 6.8): ánh nắng là hoàn cảnh của chế độ sáng cao ngoài trời; tổng cộng, kết hợp hộp sạc là kèm hộp sạc;
    # telephoto là zoom quang học. "ánh sáng mạnh" đã bỏ khỏi phụ lục (QĐ14, 02/11): không còn được dò.
    assert tach("dt-apple-iphone17", "do_sang", "Sáng 3000 nit dưới ánh nắng gay gắt", "Sáng 3000 nit") == {"che_do_hien_thi=ngoai_troi": ["dưới ánh nắng"]}
    assert tach("dt-apple-iphone17", "do_sang", "Sáng 3000 nit trong ánh sáng mạnh", "Sáng 3000 nit") == {}
    assert tach("tn-samsung-buds3pro", "thoi_luong_pin", "Tổng cộng 30 giờ", "30 giờ") == {"bo_phan=kem_hop_sac": ["Tổng cộng"]}
    assert tach("tn-samsung-buds3pro", "thoi_luong_pin", "30 giờ khi kết hợp hộp sạc", "30 giờ") == {"bo_phan=kem_hop_sac": ["kết hợp hộp sạc"]}
    assert tach("dt-apple-iphone17", "zoom", "Hỗ trợ telephoto 2x", "Zoom 2x") == {"loai_zoom=quang_hoc": ["telephoto"]}


def test_loc_theo_thuoc_tinh_chi_giu_dieu_kien_cua_thuoc_tinh():
    ma_loc = {ma for ma, _ in rt.nhom_cum("tn", "thoi_luong_pin", True)}
    ma_het = {ma for ma, _ in rt.nhom_cum("tn", "thoi_luong_pin", False)}
    assert ma_loc < ma_het
    assert {"che_do_chong_on=bat", "bo_phan=kem_hop_sac", "hoat_dong=nghe_nhac", "kieu_gia_tri=toi_da"} <= ma_loc
    assert not any(m.startswith(("do_sau=", "loai_nuoc=", "so_phut_sac=", "cum_quan_he", "tu_goi_muc_cao")) for m in ma_loc)
    # Độ sáng điện thoại có chế độ hiển thị nên có chữ gọi mức cao; kháng nước có điều kiện dạng số nên có cụm quan hệ.
    assert "tu_goi_muc_cao" in {m for m, _ in rt.nhom_cum("dt", "do_sang")}
    assert "cum_quan_he=toi_thieu" in {m for m, _ in rt.nhom_cum("dt", "khang_nuoc")}
    assert "tu_goi_muc_cao" not in {m for m, _ in rt.nhom_cum("dt", "khang_nuoc")}


# ---------- So câu gốc với tuyên bố ----------

def test_cum_dieu_kien_co_trong_cau_goc_khong_co_trong_tuyen_bo():
    kq = tach("tn-samsung-buds3pro", "thoi_luong_pin", "Tai nghe B nghe nhạc 7 giờ khi bật ANC.", "Tai nghe B nghe nhạc 7 giờ")
    assert kq == {"che_do_chong_on=bat": ["bật ANC"]}
    # Tuyên bố có cụm khác của cùng giá trị ("bật chống ồn" cũng là che_do_chong_on=bat) thì điều kiện đã có.
    assert tach("tn-samsung-buds3pro", "thoi_luong_pin", "Nghe 7 giờ khi bật ANC.", "Nghe 7 giờ khi bật chống ồn") == {}
    # Giá trị khác thì vẫn thiếu.
    assert tach("tn-samsung-buds3pro", "thoi_luong_pin", "Nghe 7 giờ khi bật ANC.", "Nghe 7 giờ khi tắt chống ồn") == \
        {"che_do_chong_on=bat": ["bật ANC"]}
    # Không phân biệt hoa thường; bỏ ngoặc đơn.
    assert tach("tn-samsung-buds3pro", "thoi_luong_pin", "Nghe 7 giờ (BẬT ANC)", "Nghe 7 giờ") == {"che_do_chong_on=bat": ["BẬT ANC"]}
    # Thuộc tính khác thì điều kiện của thuộc tính này không được dò (lọc); bỏ lọc thì có.
    assert tach("tn-samsung-buds3pro", "khang_nuoc", "Chuẩn IP57, nghe 7 giờ khi bật ANC", "Chuẩn IP57") == {}
    assert tach("tn-samsung-buds3pro", "khang_nuoc", "Chuẩn IP57, nghe 7 giờ khi bật ANC", "Chuẩn IP57", loc=False) == \
        {"che_do_chong_on=bat": ["bật ANC"]}


def test_chi_giu_cum_dai_nhat():
    cau = "Xem video trực tuyến lên đến 27 giờ"
    kq = tach("dt-apple-iphone17", "thoi_luong_pin", cau, "Xem video 27 giờ")
    assert kq["hoat_dong=xem_video_truc_tuyen"] == ["Xem video trực tuyến"]
    assert "hoat_dong=chua_ro_loai_video" not in kq and kq["kieu_gia_tri=toi_da"] == ["lên đến"]
    # Cụm không dính vào chữ khác: "tai nghe" nằm giữa "ctai nghee" thì không khớp.
    assert tach("tn-samsung-buds3pro", "thoi_luong_pin", "ctai nghee 7 giờ", "7 giờ") == {}


def test_tu_khang_dinh_chac_chan_muc_san_va_phu_dinh():
    mau = ("dt-apple-iphone17", "tan_so_quet")
    assert tach(*mau, "Màn hình luôn đạt 120Hz", "Màn hình 120Hz") == {"từ khẳng định": ["luôn"]}
    assert tach(*mau, "Màn hình luôn đạt 120Hz", "Màn hình luôn đạt 120Hz") == {}
    assert tach(*mau, "Pin không đảm bảo 120Hz, mọi lúc", "120Hz") == {"từ khẳng định": ["mọi lúc"]}   # phủ định bị bỏ qua
    assert tach(*mau, "Pin kéo dài hơn 24 giờ", "Pin 24 giờ") == {"từ khẳng định": ["hơn 24"]}
    assert tach(*mau, "Pin kéo dài hơn 24 giờ", "Pin kéo dài hơn 24 giờ") == {}
    assert tach(*mau, "Nhiều hơn người dùng", "120Hz") == {}              # "hơn" không đứng liền con số
    assert tach(*mau, "Sạc 18 giờ trở lên", "Sạc 18 giờ") == {"từ khẳng định": ["18 giờ trở lên"]}
    assert tach(*mau, "Trên 25% diện tích", "120Hz") == {"từ khẳng định": ["Trên 25"]}
    # Tên tính năng vẫn được liệt kê (tiêu chí 3 do người rà quyết), tuyên bố có chữ thì thôi.
    assert tach(*mau, "Màn hình Luôn Bật 120Hz", "120Hz") == {"từ khẳng định": ["Luôn"]}
    assert tach(*mau, "Màn hình Luôn Bật 120Hz", "màn hình luôn bật 120Hz") == {}


def test_mau_cum_phu_va_muc_san_khop_chung_yaml():
    # Biểu thức của script là cách cài đặt; danh sách cụm là của chung.yaml (cum_phu.mau, tu_khang_dinh.tu_muc_san).
    chung = rt.doc_yaml("chung")
    assert set(rt.CUM_PHU) == set(chung["cum_phu"]["mau"])
    assert set(rt.BIEU_THUC_MUC_SAN) == set(chung["tu_khang_dinh"]["tu_muc_san"])


def test_cum_phu_theo_kieu():
    mau = ("dt-apple-iphone17", "do_sang")
    kq = tach(*mau, "Sáng 3000 nit dưới mọi điều kiện ánh sáng", "Sáng 3000 nit")
    assert kq == {"cụm phủ": ["mọi điều kiện ánh sáng"]}
    assert tach(*mau, "Sáng dưới mọi điều kiện ánh sáng", "Sáng với mọi điều kiện ánh sáng khác") == {}   # cùng kiểu thì coi là có
    kq = tach("tn-samsung-buds3pro", "thoi_luong_pin", "9 giờ dù nghe nhạc hay gọi điện, bất kể thời gian", "9 giờ")
    assert kq["cụm phủ"] == ["dù nghe nhạc hay gọi điện", "bất kể thời gian"]
    assert kq["hoat_dong=nghe_nhac"] == ["nghe nhạc"] and kq["hoat_dong=dam_thoai"] == ["gọi điện"]  # cụm điều kiện bên trong cụm phủ
    assert tach("tn-samsung-buds3pro", "thoi_luong_pin", "26 giờ cho cả nhạc và cuộc gọi", "26 giờ") == \
        {"cụm phủ": ["cho cả nhạc và cuộc gọi"]}
    assert tach("dh-apple-watchse3", "thoi_luong_pin", "32 giờ ở mọi chế độ", "32 giờ") == {"cụm phủ": ["mọi chế độ"]}
    assert tach("dh-apple-watchse3", "khang_nuoc", "50 m cho mọi hoạt động dưới nước", "50 m") == \
        {"cụm phủ": ["mọi hoạt động dưới nước"]}


def test_mo_ta_cum_dieu_kien_roi_tu_khang_dinh_roi_cum_phu():
    ket_qua = {"cụm phủ": ["mọi chế độ"], "từ khẳng định": ["luôn", "hơn 24"], "hoat_dong=nghe_nhac": ["nghe nhạc"],
               "bo_phan=tai_nghe": ["tai nghe", "riêng tai nghe"]}
    assert rt.mo_ta_cum(ket_qua) == ("bo_phan=tai_nghe: “tai nghe”, “riêng tai nghe”; hoat_dong=nghe_nhac: “nghe nhạc”; "
                                    "từ khẳng định: “luôn”, “hơn 24”; cụm phủ: “mọi chế độ”")
    assert rt.mo_ta_cum({}) == "–"


def test_ra_tach_tat_dinh_va_khong_nhac_toi_nhan(tmp_path, md):
    tep = tmp_path / "thu.jsonl"
    dong = [tb("tn-samsung-buds3pro", "thoi_luong_pin", "Nghe 7 giờ | khi bật ANC, luôn luôn.", "Nghe 7 giờ", "tb-00001"),
            tb("dt-apple-iphone17", "tan_so_quet", "Màn hình 120Hz", "Màn hình 120Hz", "tb-00002")]
    tep.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in dong), encoding="utf-8")
    ra1, ra2 = tmp_path / "ra1.md", tmp_path / "ra2.md"
    tuyen_bo, ket_qua, so_co = rt.chay(tep, ra1)
    rt.chay(tep, ra2)
    assert ra1.read_bytes() == ra2.read_bytes() and so_co == 1 and len(tuyen_bo) == 2
    chu = ra1.read_text(encoding="utf-8")
    assert "| tb-00001 | Nghe 7 giờ | Nghe 7 giờ \\| khi bật ANC, luôn luôn. | che_do_chong_on=bat: “bật ANC”; từ khẳng định: “luôn” |" in chu
    assert "| tb-00002 | Màn hình 120Hz | Màn hình 120Hz | – |" in chu
    assert "1 / 2 tuyên bố có cụm được liệt kê." in chu
    # Không nêu nhãn, không đề xuất cách sửa.
    assert not re.search(r"\b(DUNG|SAI|LECH|CHUA_DU|D[1-6]a?)\b", chu)
    for tu in ("nên sửa", "đề xuất sửa", "sửa thành", "thêm vào tuyên bố"):
        assert tu not in chu


def test_main_ghi_tep_va_in_tom_tat(tmp_path, capsys):
    tep = tmp_path / "thu.jsonl"
    tep.write_text(json.dumps(tb("dt-apple-iphone17", "tan_so_quet", "Luôn 120Hz", "120Hz")) + "\n", encoding="utf-8")
    ra = tmp_path / "ra.md"
    rt.main(["--tuyen-bo", str(tep), "--ra", str(ra)])
    assert "1 / 1 tuyên bố có cụm được liệt kê" in capsys.readouterr().out
    assert "Chỉ xét các điều kiện của thuộc tính ghi trên tuyên bố." in ra.read_text(encoding="utf-8")
    rt.main(["--tuyen-bo", str(tep), "--ra", str(ra), "--khong-loc-thuoc-tinh"])
    assert "Xét mọi điều kiện của nhóm sản phẩm." in ra.read_text(encoding="utf-8")


def test_tren_bo_thu_that(tmp_path, md):
    tep = ROOT / "data/tuyen_bo/thu.jsonl"
    if not tep.exists():
        pytest.skip("không có data/tuyen_bo/thu.jsonl")
    ra = tmp_path / "ra.md"
    tuyen_bo, ket_qua, so_co = rt.chay(tep, ra)
    assert len(tuyen_bo) == 66 and 0 < so_co < 66
    dong = [d for d in ra.read_text(encoding="utf-8").splitlines() if d.startswith("| tb-")]
    assert len(dong) == 66 and all(d.count(" | ") >= 3 for d in dong)
    # Lọc theo thuộc tính chỉ bớt điều kiện, không thêm. Một giá trị có thể đổi: bỏ cụm có chi_thuoc_tinh ("cùng hộp sạc" của
    # kem_hop_sac) thì cụm ngắn hơn của cùng điều kiện ("hộp sạc" của hop_sac) có thể khớp.
    _, ket_qua_het, so_co_het = rt.chay(tep, tmp_path / "ra_het.md", loc_thuoc_tinh=False)
    assert so_co <= so_co_het
    dieu_kien = lambda kq: {m.split("=")[0] for m in kq}  # noqa: E731
    for ma, kq in ket_qua.items():
        assert dieu_kien(kq) <= dieu_kien(ket_qua_het[ma])


# ---------- Lời hướng dẫn cách sửa trong docstring ----------

def test_docstring_ghi_cach_sua_voi_tach_sua():
    doc = rt.__doc__
    for chuoi in ("Cách sửa một tuyên bố", "tach_sua=<sửa gì>", "tach_sua=thêm chế độ nguồn", "data/tuyen_bo/thu_nhap.csv",
                  "scripts/chuyen_tuyen_bo.py data/tuyen_bo/thu_nhap.csv data/tuyen_bo/thu.jsonl", "ứng với tb-{n-1:05d}",
                  "thêm dòng ở CUỐI CSV", "scripts/tao_cong_cu_gan_nhan.py", "không đề xuất cách sửa"):
        assert chuoi in doc, chuoi


def test_thu_nhap_csv_dong_n_ung_voi_tb_n_tru_1():
    # Lời trong docstring: dòng n của CSV ứng với tb-{n-1:05d} (chuyen_tuyen_bo.py đánh mã theo thứ tự dòng).
    csv_ = ROOT / "data/tuyen_bo/thu_nhap.csv"
    jsonl = ROOT / "data/tuyen_bo/thu.jsonl"
    if not (csv_.exists() and jsonl.exists()):
        pytest.skip("không có thu_nhap.csv hoặc thu.jsonl")
    with open(csv_, encoding="utf-8-sig", newline="") as f:
        dong_csv = [r for r in csv.DictReader(f) if any((r.get(c) or "").strip() for c in ("ma_qc", "cau_goc", "tuyen_bo", "thuoc_tinh"))]
    thu = [json.loads(d) for d in jsonl.read_text(encoding="utf-8-sig").splitlines() if d.strip()]
    assert len(dong_csv) == len(thu)
    for n, (r, t) in enumerate(zip(dong_csv, thu), start=1):
        assert t["id"] == f"tb-{n:05d}" and t["ma_qc"] == r["ma_qc"].strip() and t["tuyen_bo"] == r["tuyen_bo"].strip(), n


def test_kem_hop_sac_chi_cho_thoi_luong_pin():
    # chi_thuoc_tinh (rà soát 02/11): "kèm hộp sạc" là bộ phận kèm hộp sạc chỉ với thời lượng pin (mục 6.8 ý 6).
    assert "bo_phan=kem_hop_sac" in dict(rt.nhom_cum("tn", "thoi_luong_pin", True))
    assert "bo_phan=kem_hop_sac" not in dict(rt.nhom_cum("tn", "dung_luong_pin", True))
    assert "bo_phan=kem_hop_sac" not in dict(rt.nhom_cum("tn", "khang_nuoc", True))
    assert "bo_phan=kem_hop_sac" in dict(rt.nhom_cum("tn", None, False))


# ---------- Tệp tuyên bố khác thu.jsonl ----------

def viet_jsonl(tep, dong):
    tep.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in dong), encoding="utf-8")


def test_ra_mac_dinh_theo_stem_tep_tuyen_bo(tmp_path):
    assert rt.tep_ra_mac_dinh(Path("data/tuyen_bo/thu.jsonl")) == Path("data/tuyen_bo/ra_tach_thu.md")
    assert rt.tep_ra_mac_dinh(tmp_path / "chinh.jsonl") == tmp_path / "ra_tach_chinh.md"
    tep = tmp_path / "chinh.jsonl"
    viet_jsonl(tep, [tb("dt-apple-iphone17", "tan_so_quet", "Luôn 120Hz", "120Hz")])
    rt.main(["--tuyen-bo", str(tep)])   # quên --ra: ghi ra_tach_chinh.md cạnh tệp, không đụng báo cáo bộ thử
    assert (tmp_path / "ra_tach_chinh.md").exists() and not (tmp_path / "ra_tach_thu.md").exists()


def test_doi_so_vi_tri_va_xung_dot_voi_tuyen_bo(tmp_path):
    tep = tmp_path / "chinh.jsonl"
    viet_jsonl(tep, [tb("dt-apple-iphone17", "tan_so_quet", "Luôn 120Hz", "120Hz")])
    rt.main([str(tep)])
    assert (tmp_path / "ra_tach_chinh.md").exists()
    rt.main([str(tep), "--tuyen-bo", str(tep), "--ra", str(tmp_path / "ra.md")])   # cùng tệp thì không sao
    assert (tmp_path / "ra.md").exists()
    khac = tmp_path / "khac.jsonl"
    viet_jsonl(khac, [tb("dt-apple-iphone17", "tan_so_quet", "Luôn 120Hz", "120Hz")])
    with pytest.raises(SystemExit) as e:
        rt.main([str(tep), "--tuyen-bo", str(khac)])
    assert e.value.code != 0


def test_loc_ma_mau(tmp_path, capsys):
    tep = tmp_path / "chinh.jsonl"
    viet_jsonl(tep, [tb("dt-apple-iphone17", "tan_so_quet", "Luôn 120Hz", "120Hz", "tb-00067"),
                     tb("dh-apple-watchse3", "thoi_luong_pin", "32 giờ ở mọi chế độ", "32 giờ", "tb-00068"),
                     tb("dh-apple-watchse3", "khang_nuoc", "50 m", "50 m", "tb-00069")])
    ra = tmp_path / "ra.md"
    rt.main([str(tep), "--ra", str(ra), "--ma-mau", "dh-apple-watchse3"])
    chu = ra.read_text(encoding="utf-8")
    assert "tb-00067" not in chu and "tb-00068" in chu and "tb-00069" in chu
    assert "Đã lọc theo mẫu: dh-apple-watchse3." in chu and "1 / 2 tuyên bố có cụm được liệt kê." in chu
    assert "1 / 2 tuyên bố" in capsys.readouterr().out
    with pytest.raises(SystemExit):   # mẫu không có tuyên bố nào
        rt.main([str(tep), "--ra", str(ra), "--ma-mau", "tn-khong-co"])


def test_tieu_de_ghi_dung_tep_dau_vao(tmp_path):
    tep = tmp_path / "chinh.jsonl"
    viet_jsonl(tep, [tb("dt-apple-iphone17", "tan_so_quet", "Luôn 120Hz", "120Hz")])
    ra = tmp_path / "ra.md"
    rt.main([str(tep), "--ra", str(ra)])
    chu = ra.read_text(encoding="utf-8")
    assert chu.startswith("# Rà tách chinh.jsonl:") and "bộ thử" not in chu.splitlines()[0]
    assert f"từ `{tep.resolve().as_posix()}`" in chu   # ngoài repo: đường dẫn đầy đủ
    # Tệp trong repo: đường dẫn tương đối, dấu /; thu.jsonl vẫn gọi là bộ thử.
    assert rt.duong_dan_hien_thi(ROOT / "data" / "tuyen_bo" / "chinh.jsonl") == "data/tuyen_bo/chinh.jsonl"
    thu = tmp_path / "thu.jsonl"
    viet_jsonl(thu, [tb("dt-apple-iphone17", "tan_so_quet", "Luôn 120Hz", "120Hz")])
    rt.main([str(thu), "--ra", str(ra)])
    assert ra.read_text(encoding="utf-8").startswith("# Rà tách bộ thử:")
    assert "từ `data/tuyen_bo/thu.jsonl`" in rt.dung_bao_cao([], {}, True, ROOT / "data/tuyen_bo/thu.jsonl")
