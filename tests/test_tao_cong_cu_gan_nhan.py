import importlib.util
import itertools
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("tao_cong_cu_gan_nhan", ROOT / "scripts/tao_cong_cu_gan_nhan.py")
tc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tc)
spec_kn = importlib.util.spec_from_file_location("kiem_nhan_cho_so_sanh", ROOT / "scripts/kiem_nhan.py")
kn = importlib.util.module_from_spec(spec_kn)
spec_kn.loader.exec_module(kn)

MA_D = ["D1", "D1a", "D1b", "D2", "D3", "D4", "D5", "D6"]


@pytest.fixture(scope="module")
def md():
    if not tc.TEP_HUONG_DAN.exists():
        pytest.skip("không có data/huong_dan_gan_nhan.md")
    return tc.doc_huong_dan()


def thoat(ham, *args):
    """Thông báo của SystemExit khi gọi ham(*args); fail nếu không thoát."""
    with pytest.raises(SystemExit) as e:
        ham(*args)
    return str(e.value)


# ---------- Bảng trên hướng dẫn thật ----------

def test_bang_quyet_dinh_va_mau_cau(md):
    dong_d = tc.bang_dong_d(md)
    assert [d["ma"] for d in dong_d] == MA_D
    mau = tc.bang_mau_cau(md)
    assert list(mau) == MA_D  # đủ 8 mẫu, khớp mã với bảng D
    d1, d1a, d4 = (next(d for d in dong_d if d["ma"] == m) for m in ("D1", "D1a", "D4"))
    assert d1["mau_cau"] == "Tài liệu của {sản phẩm} không có thông số {thuộc tính}."  # đã bỏ cặp nháy kép ngoài
    assert d1a["mau_cau"].startswith("Chưa xác định được điều kiện của tuyên bố: “{cụm điều kiện}”")
    assert "{giá trị}" in d4["mau_cau"] and '<span class="gc">{giá trị}</span>' in d4["mau_cau_html"]
    assert d1["nhan_html"] == "Chưa đủ thông tin"
    assert all(d["kiem_tra_html"] and d["nhan_html"] and d["mau_cau"] for d in dong_d)
    assert next(d for d in dong_d if d["ma"] == "D6")["luu_y_html"] == ""


def test_bang_loai_du_6_ma(md):
    loai = tc.bang_loai(md)
    assert sorted(x["ma"] for x in loai) == sorted(tc.MA_LOAI) and len(loai) == 6
    assert all(x["giai_thich"] for x in loai)
    assert "`" not in "".join(x["giai_thich"] for x in loai)


def test_bang_nhan(md):
    nhan = tc.bang_nhan(md)
    assert sorted(nhan) == sorted(tc.MA_NHAN)
    assert nhan["LECH"]["ten"] == "Lệch điều kiện" and "lên đến" in nhan["LECH"]["dinh_nghia"]


def test_bang_muc_5_ke_thua_nhom_va_thuoc_tinh(md):
    hang = tc.bang_mac_dinh(md)
    khoa = {}
    for h in hang:
        khoa.setdefault((h["nhom"], h["thuoc_tinh"]), set()).update(k["khoa"] for k in h["khoa"])
    assert "che_do_hien_thi" in khoa[("dt", "do_sang")]
    assert "che_do_chong_on" in khoa[("tn", "thoi_luong_pin")]
    # Hàng thứ hai của thời lượng pin điện thoại có ô Nhóm, Thuộc tính trống nên kế thừa hàng trên.
    assert "phien_ban" in khoa[("dt", "thoi_luong_pin")] and "hoat_dong" in khoa[("dt", "thoi_luong_pin")]
    do_sang = [k for h in hang if (h["nhom"], h["thuoc_tinh"]) == ("dt", "do_sang") for k in h["khoa"]]
    assert {"khoa": "che_do_hien_thi", "gia_tri": "khong_co_mac_dinh"} in do_sang
    # Khóa kháng nước có nhiều cụm trong một ô.
    khang_nuoc = [h for h in hang if (h["nhom"], h["thuoc_tinh"]) == ("dt", "khang_nuoc")]
    assert len(khang_nuoc) == 1 and len(khang_nuoc[0]["khoa"]) == 4


def cap_cua_66_tuyen_bo():
    duong = ROOT / "data/tuyen_bo/thu.jsonl"
    if not duong.exists():
        pytest.skip("không có data/tuyen_bo/thu.jsonl")
    dong = [json.loads(d) for d in duong.read_text(encoding="utf-8-sig").splitlines() if d.strip()]
    return {(t["ma_mau"].split("-")[0], t["thuoc_tinh"]) for t in dong}


def test_huong_dan_co_du_cap_nhom_thuoc_tinh_cua_tuyen_bo(md):
    cap = cap_cua_66_tuyen_bo()
    assert len(cap) >= 10
    huong_loi = {(h["nhom"], h["thuoc_tinh"]) for h in tc.bang_huong_loi(md)}
    mac_dinh = {(h["nhom"], h["thuoc_tinh"]) for h in tc.bang_mac_dinh(md)}
    assert cap <= huong_loi, sorted(cap - huong_loi)
    assert cap <= mac_dinh, sorted(cap - mac_dinh)


def test_dung_huong_dan_nhung_duoc_vao_json(md):
    hd = tc.dung_huong_dan(md)
    assert set(hd) == {"html", "muc_luc_html", "nhom", "nhan", "loai", "dong_d", "mac_dinh", "huong_loi", "tu_khang_dinh",
                       "ten_thuoc_tinh", "cum"}
    json.dumps(hd, ensure_ascii=False)
    assert 'id="hd-muc-8"' in hd["html"] and 'href="#hd-muc-8"' in hd["muc_luc_html"]
    assert 'id="hd-muc-6-1"' in hd["html"]


# ---------- Bảng D1-D6: suy nhãn, câu hỏi, ví dụ ----------

# Câu hỏi do bang_dong_d trả về: D1 còn chỗ {thuoc_tinh} (trang điền tên thuộc tính của tuyên bố), D2 còn chỗ {tu_khang_dinh}
# (dung_huong_dan điền danh sách từ đọc từ mục 6.2).
CAU_HOI = {
    "D1": "Tài liệu của đúng sản phẩm có con số nào cho thuộc tính {thuoc_tinh} không, ở bất kỳ điều kiện hay bộ phận nào? "
          "Không có số nào thì dừng. Có số nhưng ở điều kiện khác thì dò tiếp.",
    "D1a": "Có biết tuyên bố đang nói ở điều kiện nào không? Điều kiện nêu rõ, hoặc có cách hiểu mặc định ở khung Bước 3 phía "
           "trên, là đã biết, không dừng ở đây. Chỉ dừng khi: (1) điều kiện ghi “Không có mặc định” mà tuyên bố không nêu; "
           "(2) chữ của tuyên bố trỏ tới nhiều chế độ; (3) cụm điều kiện không giải được (mục 6.7, 6.8). Ghi nguyên nhân vào "
           "ghi chú.",
    "D1b": "Ở điều kiện vừa xác định (nêu rõ và mặc định), tài liệu có ghi hai số khác nhau không? Có thì dừng, dù số của "
           "tuyên bố trùng một số hay khác cả hai. Ngoại lệ: số của tuyên bố khớp cả hai (bằng hoặc kém hơn cả hai) thì dò "
           "tiếp, ghi mau_thuan_khop_ca_hai=<số 1>/<số 2>.",
    "D2": "Tuyên bố có từ khẳng định gắn ngay với con số không ({tu_khang_dinh})? Từ ở vế nói việc khác và tên tính năng không "
          "tính. Chỉ thiếu chữ “lên đến” thì không phải D2. Có thì dừng.",
    "D3": "Ở đúng điều kiện đã xác định ở Bước 3 (gồm mặc định), số của tuyên bố bằng hoặc kém hơn số của hãng không? Có thì dừng.",
    "D4": "Số của tuyên bố có trùng số hãng ghi cho một điều kiện khác không? Có thì dừng. Gồm cả khi tuyên bố không nêu điều "
          "kiện và cách hiểu mặc định khác điều kiện của con số (loại bo_dieu_kien).",
    "D5": "Số của tuyên bố có đẹp hơn số hãng ghi ở cùng điều kiện, hoặc đẹp hơn mọi số hãng ghi không? Có thì dừng.",
    "D6": "Tài liệu có số cho thuộc tính, nhưng không có số ở điều kiện này; số của tuyên bố không trùng số nào và không đẹp "
          "hơn mọi số.",
}
NHAN_HIEN_THI = {"D1": "Chưa đủ thông tin (bằng chứng để trống)", "D1a": "Chưa đủ thông tin",
                 "D1b": "Chưa đủ thông tin, tick “Tài liệu mâu thuẫn”", "D2": "Lệch, loại doi_kieu_gia_tri", "D3": "Đúng",
                 "D4": "Lệch", "D5": "Sai", "D6": "Chưa đủ thông tin"}
MA_VI_DU = {"D1": "", "D1a": "V26", "D1b": "", "D2": "V39", "D3": "V11", "D4": "V33", "D5": "V20", "D6": "V44"}


def test_bang_suy_nhan_tu_dong_d(md):
    assert tc.MA_DONG_D == tuple(MA_D)
    assert tc.NHAN_THEO_DONG == {"D1": "CHUA_DU", "D1a": "CHUA_DU", "D1b": "CHUA_DU", "D2": "LECH", "D3": "DUNG",
                                 "D4": "LECH", "D5": "SAI", "D6": "CHUA_DU"}
    assert tc.LOAI_THEO_DONG == {"D2": "doi_kieu_gia_tri"} and tc.DONG_TICK_MAU_THUAN == "D1b"
    dong_d = {d["ma"]: d for d in tc.bang_dong_d(md)}
    for ma, d in dong_d.items():
        assert d["nhan_ma"] == tc.NHAN_THEO_DONG[ma] and d["nhan_ma"] in tc.MA_NHAN
        assert d["loai_tu_dong"] == ("doi_kieu_gia_tri" if ma == "D2" else "")
        assert d["tu_tick"] is (ma == "D1b")
        assert d["cau_hoi"] == CAU_HOI[ma] and d["nhan_hien_thi"] == NHAN_HIEN_THI[ma]
        assert d["vi_du_ma"] == MA_VI_DU[ma] and d["vi_du"].endswith((".", "”."))
        if d["vi_du_ma"]:  # ví dụ thật: mã V có thật trong hướng dẫn
            assert f"**{d['vi_du_ma']} ·" in md, ma
    assert dong_d["D5"]["ghi_chu_nho"].startswith("Đẹp hơn: pin, độ sáng, tần số quét, zoom, công suất sạc, dung lượng pin, ")
    assert dong_d["D5"]["ghi_chu_nho"].endswith("kháng nước so theo mục 6.6. Mã IP khác nhánh không khớp; không trùng mã nào thì Sai.")
    assert all(d["ghi_chu_nho"] == "" for ma, d in dong_d.items() if ma != "D5")
    assert "Loại bo_dieu_kien, ghi chú mac_dinh=che_do_nguon,hoat_dong." in dong_d["D4"]["vi_du"]
    assert dong_d["D1"]["vi_du"].startswith("Tai nghe B nghe nhạc 8 giờ.")


MD_D = """## 7. Thứ tự

| Dòng | Kiểm tra | Nhãn | Lưu ý cho người gán |
|---|---|---|---|
| D1 | a | Chưa đủ thông tin | |
| D1a | a | Chưa đủ thông tin | |
| D1b | a | Chưa đủ thông tin, `tai_lieu_mau_thuan = true` | |
| D2 | a | Lệch (`doi_kieu_gia_tri`) | |
| D3 | a | Đúng | |
| D4 | a | Lệch | |
| D5 | a | Sai | |
| D6 | a | Chưa đủ thông tin | |

## 8. Ghi nhãn

| Dòng | Mẫu câu |
|---|---|
| D1 | "m1" |
| D1a | "m2" |
| D1b | "m3" |
| D2 | "m4" |
| D3 | "m5" |
| D4 | "m6" |
| D5 | "m7" |
| D6 | "m8" |
"""


def sua(van_ban, cu, moi):
    assert van_ban.count(cu) == 1, cu
    return van_ban.replace(cu, moi)


def test_bang_d_gia_lap_hop_le_va_khop_bang_suy_nhan():
    assert [d["ma"] for d in tc.bang_dong_d(MD_D)] == MA_D


@pytest.mark.parametrize("cu, moi, mong", [
    ("| D3 | a | Đúng |", "| D3 | a | Sai |", "dòng D3"),  # nhãn của hướng dẫn khác bảng suy nhãn
    ("| D4 | a | Lệch |", "| D4 | a | Chưa đủ thông tin |", "không bắt đầu bằng 'Lệch'"),
    ("Lệch (`doi_kieu_gia_tri`)", "Lệch", "thiếu loại doi_kieu_gia_tri"),
    ("Chưa đủ thông tin, `tai_lieu_mau_thuan = true`", "Chưa đủ thông tin", "tai_lieu_mau_thuan = true chỉ được ghi ở dòng D1b"),
    ("| D5 | a | Sai |", "| D5 | a | Sai, `tai_lieu_mau_thuan = true` |", "tai_lieu_mau_thuan = true chỉ được ghi ở dòng D1b"),
])
def test_nhan_trong_huong_dan_khong_khop_bang_suy_nhan_thoat(cu, moi, mong):
    tb = thoat(tc.bang_dong_d, sua(MD_D, cu, moi))
    assert mong in tb and "NHAN_THEO_DONG" in tb, tb


def test_bang_d_thieu_dong_hoac_dong_la_thoat():
    md = sua(sua(MD_D, "| D6 | a | Chưa đủ thông tin | |\n", ""), '| D6 | "m8" |\n', "")
    assert "bảng thiếu dòng D6" in thoat(tc.bang_dong_d, md)
    md = sua(sua(MD_D, "| D6 | a |", "| D7 | a |"), '| D6 | "m8" |', '| D7 | "m8" |')
    tb = thoat(tc.bang_dong_d, md)
    assert "D7" in tb and "không khai báo dòng này" in tb


def test_thong_bao_va_nhac_cho_trang_va_kiem_nhan():
    assert tc.THONG_BAO["chua_chon_dong"] == "Chưa bấm “Dừng ở đây” ở bảng D1–D6."
    assert tc.THONG_BAO["d1_co_bang_chung"] == "D1 nghĩa là tài liệu không có thông số này, nên bằng chứng và câu trích để trống."
    assert tc.THONG_BAO["mac_dinh_khong_co"].format(khoa="k", dieu_kien="Chế độ hiển thị") == (
        "Ghi chú có mac_dinh=k, mà “Chế độ hiển thị” không có mặc định: tuyên bố không nói điều kiện này thì dừng ở D1a, "
        "nhãn Chưa đủ thông tin.")
    assert tc.NHAC["bo_dieu_kien_thieu_mac_dinh"] == (
        "Loại bo_dieu_kien nghĩa là tuyên bố bỏ điều kiện và bạn đã dùng cách hiểu mặc định; thường cần ghi mac_dinh=… (mục 8).")
    # Luật mới của bản 2 (S14, S15, S17, S18, S19).
    assert tc.THONG_BAO["d1a_thieu_nguyen_nhan"].format(ds="che_do_hien_thi") == (
        "Dòng D1a phải ghi nguyên nhân vào ghi chú: mac_dinh=<khóa “Không có mặc định” của thuộc tính này: che_do_hien_thi> "
        "hoặc chua_xac_dinh=<cụm>.")
    assert tc.THONG_BAO["d1a_mac_dinh_co_mac_dinh"].format(khoa="cach_sac", dieu_kien="Cách sạc", hieu="Sạc bằng cáp") == (
        "Ghi chú có mac_dinh=cach_sac, mà “Cách sạc” có cách hiểu mặc định “Sạc bằng cáp”: dùng mặc định rồi dò tiếp, "
        "không dừng ở D1a vì khóa này.")
    assert tc.THONG_BAO["d2_thieu_khang_dinh"].format(ds="luôn, hơn") == (
        "Dòng D2 phải ghi từ khẳng định vào ghi chú: khang_dinh=<từ>, với <từ> là một trong: luôn, hơn.")
    assert tc.THONG_BAO["d2_khang_dinh_la"].format(tu="rất", ds="luôn, hơn") == (
        "Ghi chú có khang_dinh=rất, mà “rất” không có trong danh sách từ khẳng định ở mục 6.2: luôn, hơn.")
    assert tc.THONG_BAO["ly_do_ma_doan"].format(ma="dt-x#001") == (
        "Lý do chép mã đoạn thay cho câu trích: “dt-x#001”. Chỗ câu trích là câu nguyên văn từ tài liệu; mã đoạn đã nằm ở "
        "bằng chứng.")
    assert tc.NHAC["d1_co_mac_dinh"] == "Dòng D1 dừng trước khi xét điều kiện, nên không cần ghi mac_dinh=… (mục 8)."
    assert tc.NHAC["trich_thieu_don_vi"].format(thuoc_tinh="do_sang", don_vi="nit") == (
        "Câu trích không có đơn vị của thuộc tính do_sang (nit): kiểm lại xem bằng chứng có đúng thuộc tính của tuyên bố không.")
    # kiem_nhan.py dùng đúng các bảng này (import lại), nên hai bên cùng chữ.
    assert kn.THONG_BAO == tc.THONG_BAO and kn.NHAC == tc.NHAC and kn.NHAN_THEO_DONG == tc.NHAN_THEO_DONG


# ---------- Mục 5 ghép với mục 5.1; khóa "không có mặc định"; hướng thuận lợi ----------

def hang_muc_5(hang, nhom, thuoc_tinh, dieu_kien):
    tim = [h for h in hang if (h["nhom"], h["thuoc_tinh"], h["dieu_kien"]) == (nhom, thuoc_tinh, dieu_kien)]
    assert len(tim) == 1, (nhom, thuoc_tinh, dieu_kien)
    return tim[0]


def test_ghep_muc_5_voi_muc_5_1_tren_huong_dan_that(md):
    hang = tc.bang_mac_dinh(md)
    do_sang = hang_muc_5(hang, "dt", "do_sang", "Chế độ hiển thị")  # tên điều kiện đã bỏ dấu *
    assert do_sang["co_sao"] and len(do_sang["khao_sat"]) == 1
    assert "7/10" in do_sang["khao_sat"][0]["hieu_khac"] and "<strong>Sửa</strong>" in do_sang["khao_sat"][0]["quyet_dinh_html"]
    chong_on = hang_muc_5(hang, "tn", "thoi_luong_pin", "Chống ồn")
    assert len(chong_on["khao_sat"]) == 1 and "4/10" in chong_on["khao_sat"][0]["hieu_khac"]
    assert "Giữ" in chong_on["khao_sat"][0]["quyet_dinh_html"]
    # Hoạt động của điện thoại ghép với cả hai hàng 5.1: "kém thuận lợi nhất" (1/10) và "Xem video" (9/10).
    hoat_dong = hang_muc_5(hang, "dt", "thoi_luong_pin", "Hoạt động")
    assert [k["hieu_khac"] for k in hoat_dong["khao_sat"]] == ["1/10", "9/10"]
    assert hang_muc_5(hang, "dh", "thoi_luong_pin", "Chế độ nguồn")["khao_sat"][0]["hieu_khac"].startswith("6/10")
    assert hang_muc_5(hang, "dh", "thoi_luong_pin", "Hoạt động")["khao_sat"][0]["hieu_khac"] == "1/10"
    # Chỉ hàng có dấu * mới có khảo sát; mỗi mục khai báo tay đều đã ghép.
    co_sao = [h for h in hang if h["co_sao"]]
    assert len(co_sao) == len(tc.GHEP_KHAO_SAT) == 6 and all(h["khao_sat"] for h in co_sao)
    assert all(h["khao_sat"] == [] for h in hang if not h["co_sao"])
    assert not any(h["dieu_kien"].endswith("*") for h in hang)


@pytest.mark.parametrize("cu, moi, mong", [
    ("| Chế độ hiển thị* |", "| Chế độ hiển thị |", "không còn dấu *"),  # khai báo tay thừa
    ("| Cách sạc | Sạc bằng cáp |", "| Cách sạc* | Sạc bằng cáp |", "chưa có trong bảng ghép với mục 5.1"),  # hàng * mới
    ("| Điện thoại, chế độ hiển thị: tiêu chuẩn |", "| Điện thoại, màn hình: tiêu chuẩn |", "trúng 0 hàng"),
    ("| Điện thoại, zoom: quang học |", "| Tai nghe: nghe nhạc, zoom |", "trúng 2 hàng"),
])
def test_ghep_5_voi_5_1_khong_duoc_thi_thoat(md, cu, moi, mong):
    tb = thoat(tc.bang_mac_dinh, sua(md, cu, moi))
    assert mong in tb, tb


def test_mac_dinh_ca_khong_co_va_co_khoa_khac_thoat(md):
    # Một hàng của bảng vừa có khóa "không có mặc định" vừa có khóa khác: trang không biết nên hiện câu nào, nên thoát.
    md2 = sua(md, "| Số phút sạc | Không có mặc định | `so_phut_sac: khong_co_mac_dinh` |",
              "| Số phút sạc | Không có mặc định | `so_phut_sac: khong_co_mac_dinh, bo_phan: tai_nghe` |")
    assert "vừa có khóa khong_co_mac_dinh vừa có khóa khác" in thoat(tc.bang_mac_dinh, md2)


def test_khoa_khong_co_mac_dinh_nhan_dung_ba_ca(md):
    khoa = tc.khoa_khong_co_mac_dinh(tc.bang_mac_dinh(md))
    assert khoa[("dt", "do_sang")] == {"che_do_hien_thi": "Chế độ hiển thị"}
    assert khoa[("dt", "sac_nhanh")] == {"moc_phan_tram": "Mốc phần trăm"}
    assert khoa[("tn", "sac_nhanh")] == {"so_phut_sac": "Số phút sạc"}
    assert set(khoa[("dh", "sac_nhanh")]) == {"moc_phan_tram", "so_phut_sac"}
    # Khóa có cách hiểu (kể cả "như hãng công bố") không có trong danh sách.
    assert ("dt", "thoi_luong_pin") not in khoa and ("tn", "thoi_luong_pin") not in khoa and ("dt", "khang_nuoc") not in khoa
    assert len(khoa) == 4


def test_huong_loi_dich_sang_loi(md):
    hl = {(h["nhom"], h["thuoc_tinh"]): h for h in tc.bang_huong_loi(md)}
    assert (hl[("dt", "thoi_luong_pin")]["huong_loi"], hl[("dt", "thoi_luong_pin")]["huong_ma"]) == ("số lớn hơn là đẹp hơn", "cao_hon_tot_hon")
    assert hl[("dt", "sac_nhanh")]["huong_loi"] == "số nhỏ hơn là đẹp hơn" and hl[("dt", "sac_nhanh")]["huong_ma"] == "thap_hon_tot_hon"
    assert hl[("dt", "khang_nuoc")]["huong_loi"] == "so mã IP theo mục 6.6" and hl[("dt", "khang_nuoc")]["huong_ma"] == "theo_nhanh_ip"
    assert hl[("dh", "sac_nhanh")]["huong_loi"] == "tùy dạng, xem mục 6.1"
    assert hl[("dt", "thoi_luong_pin")]["kieu_loi"] == "mức tối đa hãng công bố" and hl[("dt", "thoi_luong_pin")]["kieu_ma"] == "toi_da"
    assert hl[("dt", "dung_luong_pin")]["kieu_loi"] == "mức điển hình" and hl[("dt", "dung_luong_pin")]["kieu_ma"] == "dien_hinh"
    assert hl[("dt", "khang_nuoc")]["kieu_loi"] == "như hãng công bố" and hl[("dh", "khang_nuoc")]["kieu_ma"] == "nhu_hang_cong_bo"
    assert all(h["huong_loi"] and h["kieu_loi"] for h in hl.values())  # mọi hàng của bảng 6.1 đều dịch được
    tb = thoat(tc.bang_huong_loi, sua(md, "| `zoom` | x | `cao_hon_tot_hon` |", "| `zoom` | x | `cao_la_tot` |"))
    assert "cao_la_tot" in tb and "chưa có cách dịch sang lời" in tb


# ---------- Lỗi rõ khi hướng dẫn sai cấu trúc ----------

MD_NHO = """# Tiêu đề

## 7. Thứ tự

| Dòng | Kiểm tra |
|---|---|
| D1 | Không có thông số |
| D2 | Từ khẳng định |

## 8. Ghi nhãn

Không có bảng ở đây.
"""


def test_tim_bang_doc_duoc_bang_trong_muc():
    hang = tc.tim_bang(MD_NHO, "7", ("Dòng", "Kiểm tra"))
    assert hang == [{"Dòng": "D1", "Kiểm tra": "Không có thông số"}, {"Dòng": "D2", "Kiểm tra": "Từ khẳng định"}]


def test_thieu_bang_thoat_voi_thong_bao_ro():
    tb = thoat(tc.tim_bang, MD_NHO, "8", ("Dòng", "Mẫu câu"))
    assert "không thấy bảng" in tb and "(Dòng, Mẫu câu)" in tb and "mục 8" in tb and "không có bảng nào" in tb
    tb = thoat(tc.tim_bang, MD_NHO, "7", ("Dòng", "Mẫu câu"))  # mục có bảng nhưng khác cột: nêu bảng đang có
    assert "mục 7" in tb and "(Dòng, Kiểm tra)" in tb


def test_thieu_muc_thoat_voi_thong_bao_ro():
    assert "không thấy mục 9" in thoat(tc.tim_bang, MD_NHO, "9", ("Dòng",))


def test_sai_so_cot_thoat():
    md = "## 3. Mục\n\n| Mã | Khi nào | Thừa |\n|---|---|---|\n| a | b | c |\n"
    tb = thoat(tc.tim_bang, md, "3", ("Mã", "Khi nào"))
    assert "có 3 cột" in tb and "cần đúng 2 cột" in tb


def test_dong_sai_so_o_thoat():
    md = "## 3. Mục\n\n| Mã | Khi nào |\n|---|---|\n| a | b | c |\n"
    tb = thoat(tc.tim_bang, md, "3", ("Mã", "Khi nào"))
    assert "dòng bảng có 3 ô" in tb and "2 cột" in tb


def test_bang_khong_co_dong_du_lieu_thoat():
    md = "## 3. Mục\n\n| Mã | Khi nào |\n|---|---|\n\nHết.\n"
    assert "không có dòng dữ liệu" in thoat(tc.tim_bang, md, "3", ("Mã", "Khi nào"))


def test_bang_trong_khoi_code_khong_tinh():
    md = "## 3. Mục\n\n```\n| Mã | Khi nào |\n|---|---|\n| a | b |\n```\n"
    assert "không thấy bảng" in thoat(tc.tim_bang, md, "3", ("Mã", "Khi nào"))


def test_dong_d_thieu_mau_cau_thoat():
    md = """## 7. Thứ tự

| Dòng | Kiểm tra | Nhãn | Lưu ý cho người gán |
|---|---|---|---|
| D1 | a | Chưa đủ thông tin | b |
| D9 | c | Sai | d |

## 8. Ghi nhãn

| Dòng | Mẫu câu |
|---|---|
| D1 | "Mẫu {x}." |
"""
    tb = thoat(tc.bang_dong_d, md)
    assert "D9" in tb and "không có mẫu" in tb


def test_loai_thieu_ma_thoat():
    md = "## 8. Ghi nhãn\n\n| Mã | Khi nào |\n|---|---|\n| `bo_dieu_kien` | a |\n"
    tb = thoat(tc.bang_loai, md)
    assert "thiếu mã" in tb and "doi_gia_tri" in tb


def test_nhom_la_trong_bang_muc_5_thoat():
    md = ("## 5. Mặc định\n\n| Nhóm | Thuộc tính | Điều kiện | Không nêu thì hiểu là | Khóa cấu hình |\n|---|---|---|---|---|\n"
          "| Máy giặt | Pin (`thoi_luong_pin`) | a | b | `x: y` |\n")
    assert "Máy giặt" in thoat(tc.bang_mac_dinh, md)


def test_thieu_tep_huong_dan_thoat(tmp_path):
    assert "thiếu tệp hướng dẫn" in thoat(tc.doc_huong_dan, tmp_path / "khong_co.md")


# ---------- Bộ chuyển markdown ----------

def test_tieu_de_co_id_va_cap():
    h = tc.chuyen_markdown("# Hướng dẫn\n\n## 5. Cách hiểu\n\n### 6.1 Hướng\n\n#### Mục nhỏ\n\n## Đường dẫn Đặc biệt\n")
    assert '<h1 id="hd-huong-dan">Hướng dẫn</h1>' in h
    assert '<h2 id="hd-muc-5">5. Cách hiểu</h2>' in h
    assert '<h3 id="hd-muc-6-1">6.1 Hướng</h3>' in h
    assert '<h4 id="hd-muc-nho">Mục nhỏ</h4>' in h
    assert 'id="hd-duong-dan-dac-biet"' in h
    ids = re.findall(r'id="([^"]+)"', tc.chuyen_markdown("## A\n\n## A\n"))
    assert len(set(ids)) == 2  # tiêu đề trùng chữ vẫn có id khác nhau


def test_dam_nghieng_code_va_dau_sao_le():
    h = tc.chuyen_markdown("**Bản:** 1 và *nghiêng* với `code` cùng `**không đậm**`.\n\nChế độ hiển thị* chỉ một dấu sao.")
    assert "<strong>Bản:</strong>" in h and "<em>nghiêng</em>" in h
    assert "<code>code</code>" in h and "<code>**không đậm**</code>" in h
    assert "hiển thị* chỉ" in h and h.count("<em>") == 1


def test_escape_truoc_khi_thay_the():
    h = tc.chuyen_markdown("Chữ <script>alert(1)</script> & **<b>đậm</b>** `<i>`\n\n| <img src=x> | b |\n|---|---|\n| <u> | `<v>` |\n")
    assert "<script>" not in h and "<img" not in h and "<b>" not in h and "<i>" not in h and "<u>" not in h
    assert "&lt;script&gt;alert(1)&lt;/script&gt; &amp; <strong>&lt;b&gt;đậm&lt;/b&gt;</strong>" in h
    assert "<code>&lt;i&gt;</code>" in h and "<th>&lt;img src=x&gt;</th>" in h and "<td><code>&lt;v&gt;</code></td>" in h


def test_bang_markdown_thanh_html():
    h = tc.chuyen_markdown("Trước bảng.\n\n| Nhóm | Mã |\n|---|:---:|\n| **Đúng** | `DUNG` |\n| Sai | `SAI` |\n\nSau bảng.")
    assert '<table><thead><tr><th>Nhóm</th><th>Mã</th></tr></thead><tbody>' in h
    assert "<tr><td><strong>Đúng</strong></td><td><code>DUNG</code></td></tr>" in h
    assert h.count("<tr>") == 3 and "<p>Trước bảng.</p>" in h and "<p>Sau bảng.</p>" in h


def test_danh_sach_gach_dau_dong_long_mot_cap():
    h = tc.chuyen_markdown("- Cha một\n  - Con a\n  - Con b\n- Cha hai\n")
    assert h == "<ul><li>Cha một<ul><li>Con a</li><li>Con b</li></ul></li><li>Cha hai</li></ul>"


def test_danh_sach_danh_so_va_hon_hop():
    h = tc.chuyen_markdown("1. Một\n2. Hai\n   - con\n3. Ba\n\nĐoạn giữa.\n\n5. Năm\n- gạch\n")
    assert h.startswith("<ol><li>Một</li><li>Hai<ul><li>con</li></ul></li><li>Ba</li></ol>")
    assert '<ol start="5"><li>Năm</li></ol><ul><li>gạch</li></ul>' in h  # đổi kiểu danh sách thì mở danh sách mới


def test_danh_sach_bat_dau_ngay_sau_doan_van():
    h = tc.chuyen_markdown("**V01 · Đúng.** Câu mở đầu.\n- Bằng chứng: a\n- Lý do: b\n\n**V02** tiếp.")
    assert h.startswith("<p><strong>V01 · Đúng.</strong> Câu mở đầu.</p>\n<ul><li>Bằng chứng: a</li>")
    assert h.count("<li>") == 2 and "<p><strong>V02</strong> tiếp.</p>" in h


def test_dong_thut_vao_noi_tiep_muc_danh_sach():
    h = tc.chuyen_markdown("- Mục dài\n  tiếp tục ở dòng sau\n- Mục hai\n")
    assert h == "<ul><li>Mục dài tiếp tục ở dòng sau</li><li>Mục hai</li></ul>"


def test_khoi_code_giu_nguyen_va_escape():
    h = tc.chuyen_markdown("```json\n{\"a\": \"<b>\"}\n# không phải tiêu đề\n| không | phải | bảng |\n```\n\nSau.")
    assert h.startswith('<pre><code>{"a": "&lt;b&gt;"}\n# không phải tiêu đề\n| không | phải | bảng |</code></pre>')
    assert "<h1" not in h and "<table" not in h and "<p>Sau.</p>" in h


def test_khoi_code_khong_dong_het_tep():
    assert tc.chuyen_markdown("```\nmở mà không đóng") == "<pre><code>mở mà không đóng</code></pre>"


def test_doan_van_gop_dong_va_ke_ngang():
    h = tc.chuyen_markdown("Dòng một\nDòng hai\n\n---\n\nDòng ba")
    assert h == "<p>Dòng một Dòng hai</p>\n<hr>\n<p>Dòng ba</p>"


def test_chuyen_toan_bo_huong_dan_that(md):
    h = tc.chuyen_markdown(md)
    assert "<script" not in h and "<ma_mau>" not in h and "&lt;ma_mau&gt;" in h
    assert h.count("<table>") == len(re.findall(r"^\|[- :|]+\|\s*$", md, flags=re.M))  # mỗi dòng |---| một bảng
    assert h.count("<pre>") == 1 and '<h2 id="hd-muc-12">' in h
    # Dấu sao lẻ (Hoạt động*) trong hướng dẫn giữ nguyên, không bị biến thành nghiêng hay đậm.
    assert "Hoạt động*" in h
    dong_nghieng = re.findall(r"^\*[^*\s].*[^*\s]\*$", md, flags=re.M)
    assert h.count("<em>") == len(dong_nghieng) >= 1


# ---------- Trang HTML sinh ra ----------

@pytest.fixture(scope="module")
def trang():
    try:
        du_lieu = tc.nap_du_lieu()
    except SystemExit as e:
        pytest.skip(f"thiếu dữ liệu để dựng trang: {e}")
    return tc.dung_html(du_lieu), du_lieu


def test_trang_co_du_noi_dung_huong_dan(trang):
    html, du_lieu = trang
    for chuoi in ("Cách làm một tuyên bố",
                  "Bước 4 · Dò từ trên xuống, bấm “Dừng ở đây” ở dòng đầu tiên đúng với tuyên bố",
                  "Bước 3 · Điều kiện của tuyên bố: nêu rõ, hoặc cách hiểu mặc định (dùng ở mọi dòng D)",
                  "Cụm điều kiện đã biết của sản phẩm và thuộc tính này (phụ lục mục 13)", "Quy tắc hay dùng",
                  "Mở hướng dẫn đầy đủ", "Dùng Ctrl+F để tìm", "Chèn mẫu câu",
                  "Hướng dẫn chưa có cách hiểu mặc định cho thuộc tính này.",
                  "Các tuyên bố sau đã lưu nhưng không qua quy tắc mới, mở lại để sửa: ",
                  "Lý do còn chỗ {…} chưa thay", "gan_nhan_giao_dien_v2", "gan_nhan_thu_v2",
                  "Số có thật nhưng ở điều kiện khác, hoặc có từ khẳng định (\"luôn\", \"ít nhất\"...) gắn với mức \"lên đến\". "
                  "Chỉ thiếu chữ \"lên đến\" thì không phải Lệch",
                  "không có số nào cho thuộc tính (D1), không xác định được điều kiện (D1a), tài liệu mâu thuẫn (D1b), hoặc "
                  "không có số ở điều kiện này (D6)",
                  "Chọn loại bằng 2 câu hỏi.", 'id="goi-y-lech"', 'id="goi-y-sai"', "'Hướng dẫn mục 8: '"):
        assert chuoi in html, chuoi
    # Mỗi loại hợp lệ của LECH và SAI có chữ ngắn trong ô chọn.
    chu_loai = re.search(r"const CHU_LOAI = \{(.*?)\n\};", html, flags=re.S).group(1)
    lech, sai = chu_loai.split("SAI:")
    for ma in ("bo_dieu_kien", "doi_dieu_kien", "doi_bo_phan", "doi_phien_ban", "doi_kieu_gia_tri"):
        assert ma + ":" in lech, ma
    for ma in ("doi_gia_tri", "doi_bo_phan", "doi_phien_ban"):
        assert ma + ":" in sai, ma
    assert html.count('<details class="hd"') == 7
    for ma in ("kh-hay-dung", "kh-bai", "kh-cum"):  # các khung đóng sẵn (không có thuộc tính open)
        assert f'<details class="hd" id="{ma}">' in html, ma
    for ma in ("kh-cach-lam", "kh-mac-dinh", "kh-quyet-dinh", "kh-ca-dac-biet"):
        assert f'<details class="hd" id="{ma}" open>' in html, ma
    # Ngoài khối dữ liệu JSON, trang không tham chiếu gì từ mạng.
    khung = re.sub(r'<script id="du-lieu".*?</script>', "", html, flags=re.S)
    assert not re.search(r'(src|href)="https?:', khung) and "<link" not in khung and "@import" not in khung
    assert "fetch(" not in khung and "XMLHttpRequest" not in khung


def test_trang_khong_de_lot_the_script_trong_du_lieu(trang):
    html, du_lieu = trang
    assert html.count("</script>") == 2
    m = re.search(r'<script id="du-lieu" type="application/json">(.*?)</script>', html, flags=re.S)
    doc_lai = json.loads(m.group(1))
    assert doc_lai == json.loads(json.dumps(du_lieu))
    assert len(doc_lai["tuyen_bo"]) == 66 and doc_lai["huong_dan"]["html"].startswith("<h1")


def test_trang_chon_dong_d_nhan_tu_suy_ra_va_khung_dieu_kien(trang):
    html, du_lieu = trang
    js = re.search(r"<script>\n(.*?)</script>", html, flags=re.S).group(1)
    # Bước 4: dòng D có nút "Dừng ở đây", "Ví dụ" (đóng sẵn), "Chèn mẫu câu"; nhãn chỉ hiển thị, không bấm đổi.
    for chuoi in ("'Dừng ở đây'", "'Đang dừng ở đây'", "'Ví dụ'", "'Ẩn ví dụ'", "Ví dụ giả định: ", "'Chèn mẫu câu'",
                  "vi.hidden = true;", "Đang dừng ở ", "Chưa chọn dòng nào.", "dong_d: r.dong_d, loai:",
                  "Tuyên bố không nói ", " → dừng ở D1a, nhãn Chưa đủ thông tin.", " → coi như tuyên bố nói: ", ". Rồi dò tiếp.",
                  "Nhãn dựa vào dòng này thì ghi mac_dinh=", "vào ghi chú.", "Khảo sát Bước 10: ", " người hiểu khác → ",
                  "Không có mặc định", "Trang mới cần bạn chọn dòng D cho các tuyên bố đã gán trước đây.",
                  "Nhắc (vẫn lưu được): "):
        assert chuoi in js, chuoi
    assert 'role="radio"' not in html and "#nut-nhan button" not in html  # nhãn không còn là nút bấm
    assert 'data-nhan="DUNG"' in html and 'id="nhac"' in html and 'id="loai-d2"' in html
    khung = re.sub(r'<script id="du-lieu".*?</script>', "", html, flags=re.S)  # bỏ toàn văn hướng dẫn (có mục 5 cũ)
    assert "Cách hiểu mặc định khi tuyên bố không nêu điều kiện" not in khung
    assert "Quảng cáo hay bỏ bớt điều kiện. Bảng dưới cho biết làm gì với từng điều kiện bị bỏ." in html
    assert "rồi kiểm lại bằng khảo sát 10 người ở Bước 10." in html
    assert "Dò bảng D1–D6 từ trên xuống, bấm “Dừng ở đây” ở dòng đầu tiên đúng với tuyên bố. Nhãn tự điền theo dòng; " \
           "Lệch hoặc Sai thì chọn thêm loại." in html
    # Dữ liệu nhúng: bảng D kèm nhãn suy ra, thông báo và lời nhắc lấy từ Python, nên trang và kiem_nhan.py cùng chữ.
    assert du_lieu["quy_tac"] == {"thong_bao": tc.THONG_BAO, "nhac": tc.NHAC, "re_ngoac_kep": tc.RE_NGOAC_KEP,
                                  "re_ma_doan": tc.RE_MA_DOAN}
    assert du_lieu["trang"] == {"luot": 2, "khoa_nhan": "gan_nhan_thu_v2", "khoa_giao_dien": "gan_nhan_giao_dien_v2",
                                "tep_nhan": "thu_luot2.jsonl", "tep_hoi": "cau_hoi_nhan_luot2.md", "nghi_ms": 180000}
    assert [d["nhan_ma"] for d in du_lieu["huong_dan"]["dong_d"]] == [tc.NHAN_THEO_DONG[m] for m in MA_D]
    assert any(h["khao_sat"] for h in du_lieu["huong_dan"]["mac_dinh"])
    # Mọi thông báo có chỗ {tên} thì trang truyền đủ các tên đó cho dien(TBAO.<khóa>, {...}); dong_la chỉ dùng ở kiem_nhan.
    for khoa, mau in tc.THONG_BAO.items():
        ten = re.findall(r"\{(\w+)\}", mau)
        if khoa == "dong_la":
            continue
        assert f"TBAO.{khoa}" in js, khoa
        if ten:
            m = re.search(r"dien\(TBAO\." + khoa + r", \{(.*?)\}\)", js, flags=re.S)
            assert m and all(t in m.group(1) for t in ten), (khoa, ten)
    # Mọi thông báo của kiem_nhan.py còn lại đều là chữ thuần của trang: không có chỗ {…} lạ.
    assert "{…}" not in "".join(tc.THONG_BAO.values()) + "".join(tc.NHAC.values())


def test_trang_khong_doc_noi_dung_tuyen_bo_de_goi_y(trang):
    # Ranh giới phương pháp: phần kiểm chỉ dùng nhóm (tiền tố ma_mau), thuoc_tinh và các ô người gán điền;
    # không đụng vào tuyen_bo, cau_goc, ghi_chu của tuyên bố trong hàm kiem, nhacCuaTuyenBo và chonDong.
    html, _ = trang
    js = re.search(r"<script>\n(.*?)</script>", html, flags=re.S).group(1)
    for ten in ("function kiem(", "function nhacCuaTuyenBo(", "function chonDong(", "function luatKiem(", "function doanCoChu(",
                "function hienGoiYDoan(", "function layBoiDen(", "function dungCumDieuKien(", "function tenThuocTinh("):
        dau = js.index(ten)
        than = js[dau:js.index("\nfunction ", dau + 10)]
        assert not re.search(r"\b(tb|TB\[[^\]]*\])\.(tuyen_bo|cau_goc|ghi_chu|llm_sinh|che_do|loai_bai|url_nguon)\b", than), ten
    # Khối luật kiểm không đụng DOM và không nhắc tới câu tuyên bố hay câu gốc; S16 chỉ dùng chuỗi người gán đã bôi đen.
    khoi = khoi_luat_kiem(html)
    assert "tuyen_bo" not in khoi and "cau_goc" not in khoi and "document" not in khoi and "$(" not in khoi


def test_trang_khong_hien_ghi_chu_cua_tuyen_bo(trang):
    # Hướng dẫn bản 2 (mục 1, bước 0): khi gán chỉ đọc chữ của tuyên bố. Ghi chú của tuyên bố (tach_sua=…, ghi chú bỏ phần, gộp)
    # không hiện trên thẻ; dữ liệu của tuyên bố vẫn nhúng nguyên.
    html, du_lieu = trang
    khung = re.sub(r'<script id="du-lieu".*?</script>', "", html, flags=re.S)
    for chuoi in ("the-ghi-chu", "ghi-chu-tb", "Ghi chú của tuyên bố"):
        assert chuoi not in khung, chuoi
    assert not re.search(r"\b(tb|TB\[[^\]]*\])\.ghi_chu\b", khung)   # ghi_chu của bản ghi người gán (r.ghi_chu) vẫn có, của tuyên bố thì không
    # Thẻ chỉ còn mã, tuyên bố, thuộc tính, mã bài, LLM, chế độ, loại bài.
    the = re.search(r"function dungThe\(\) \{.*?\n\}\n", khung, flags=re.S).group(0)
    assert "ghi_chu" not in the and "'Thuộc tính', tb.thuoc_tinh" in the
    # Trường ghi_chu vẫn nằm trong dữ liệu nhúng và không bị xóa khỏi tuyên bố.
    m = re.search(r'<script id="du-lieu" type="application/json">(.*?)</script>', html, flags=re.S)
    nhung = json.loads(m.group(1))["tuyen_bo"]
    assert "ghi_chu" in tc.TRUONG_TUYEN_BO and all("ghi_chu" in t for t in nhung)
    assert any(t["ghi_chu"] for t in nhung) and [t["ghi_chu"] for t in nhung] == [t["ghi_chu"] for t in du_lieu["tuyen_bo"]]


def khoi_luat_kiem(html):
    """Khối LUAT_KIEM (luật kiểm không đụng DOM) của trang: test chạy riêng trong node."""
    m = re.search(r"/\* >>> LUAT_KIEM.*?/\* <<< LUAT_KIEM \*/", html, flags=re.S)
    assert m, "không thấy khối LUAT_KIEM"
    return m.group(0)


def test_doan_nhung_chi_them_noi_dung_goc_khi_khac():
    d = {"id": "m#001", "ma_mau": "m", "noi_dung": "Pin\n20 phút", "noi_dung_goc": "Pin\n20 phút6", "chu_thich": ["a"], "dong": [1, 2]}
    assert tc.doan_nhung(d) == {"id": "m#001", "noi_dung": "Pin\n20 phút", "noi_dung_goc": "Pin\n20 phút6", "chu_thich": ["a"]}
    giong = dict(d, noi_dung_goc="Pin\n20 phút")
    assert tc.doan_nhung(giong) == {"id": "m#001", "noi_dung": "Pin\n20 phút", "chu_thich": ["a"]}  # không nhúng hai lần
    cu = {"id": "m#002", "noi_dung": "Pin", "chu_thich": None}  # doan.jsonl cũ chưa có noi_dung_goc
    assert tc.doan_nhung(cu) == {"id": "m#002", "noi_dung": "Pin", "chu_thich": []}


def test_trang_hien_noi_dung_da_bo_so_chu_thich_va_nhac_dung_quy_tac(trang):
    html, du_lieu = trang
    iphone = du_lieu["doan"]["dt-apple-iphone17"]
    sac = next(d for d in iphone if "Sạc lên đến 50% trong 20 phút" in d["noi_dung"])
    assert "20 phút với bộ tiếp hợp 40W" in sac["noi_dung"] and "20 phút6 với" in sac["noi_dung_goc"]
    assert all("noi_dung_goc" not in d for d in iphone if d["noi_dung"] == d.get("noi_dung_goc", d["noi_dung"]))
    assert "số chú thích của trang hãng đã được bỏ khỏi nội dung" in html
    assert "giữ cả số chú thích dính vào chữ" not in html and '"20 phút6"' not in html.replace(json.dumps(du_lieu, ensure_ascii=False), "")
    # Bản JavaScript của scripts/kiem_nhan.py: câu trích cũng được chấp nhận nếu nằm trong noi_dung_goc.
    assert "k.goc.includes(p)" in html and "chuanHoa(d.noi_dung_goc || d.noi_dung)" in html
    assert "gan_nhan_thu_v2" in html and "gan_nhan_thu_v1" not in html  # lượt 2: khóa lưu nhãn mới, không dùng lại khóa lượt 1


def test_json_nhung_chan_dong_the_script():
    s = tc.json_nhung({"a": "</script><b>"})
    assert "<" not in s and json.loads(s) == {"a": "</script><b>"}


def test_cu_phap_javascript_hop_le(trang, tmp_path):
    node = shutil.which("node")
    if not node:
        pytest.skip("không có node")
    html, _ = trang
    js = re.search(r"<script>\n(.*?)</script>", html, flags=re.S).group(1)
    tep = tmp_path / "cong_cu.js"
    tep.write_text(js, encoding="utf-8")
    kq = subprocess.run([node, "--check", str(tep)], capture_output=True, text=True, encoding="utf-8")
    assert kq.returncode == 0, kq.stderr


def test_ca_dac_biet_hop_le():
    thuoc_tinh = {"thoi_luong_pin", "sac_nhanh", "cong_suat_sac", "do_sang", "tan_so_quet", "zoom", "khang_nuoc",
                  "dung_luong_pin"}
    for c in tc.CA_DAC_BIET:
        assert {"tieu_de", "noi_dung", "nguon"} <= c.keys()
        assert ("ma_mau" in c) != ("nhom" in c)
        assert c.get("nhom", c.get("ma_mau", "").split("-")[0]) in {"dt", "tn", "dh"}
        assert "thuoc_tinh" not in c or c["thuoc_tinh"] in thuoc_tinh  # bỏ trống thì áp cho mọi thuộc tính của nhóm
        assert "{" not in c["noi_dung"]


def chuan_van(chu):
    return " ".join(unicodedata.normalize("NFC", chu).casefold().split())


def test_ca_dac_biet_chi_chep_luat_cua_ban_2():
    # S12: bỏ mục "chưa có quy tắc" (cụm chung chung về ánh sáng), thay bằng cụm phủ nhiều giá trị (QĐ3) cho cả ba nhóm.
    tieu_de = [c["tieu_de"] for c in tc.CA_DAC_BIET]
    assert not any("chưa có quy tắc" in t for t in tieu_de)
    assert not any("chưa có trong hướng dẫn" in c["nguon"] for c in tc.CA_DAC_BIET)
    for ten in ("Cụm phủ nhiều giá trị", "Cụm điều kiện chưa có trong phụ lục", "Con số của điều kiện không phải giá trị"):
        nhom = sorted(c["nhom"] for c in tc.CA_DAC_BIET if c["tieu_de"].startswith(ten))
        assert nhom == ["dh", "dt", "tn"], ten
    cum_phu = next(c for c in tc.CA_DAC_BIET if c["tieu_de"].startswith("Cụm phủ nhiều giá trị"))
    assert "kém thuận lợi nhất" in cum_phu["noi_dung"] and "doi_dieu_kien" in cum_phu["noi_dung"]
    # S12: mục D1b chỉ khi điều kiện của tuyên bố là kèm hộp sạc và bật chống ồn.
    d1b = next(c for c in tc.CA_DAC_BIET if c["tieu_de"].startswith("Hai số cho tổng"))
    assert "Chỉ khi điều kiện của tuyên bố (nêu rõ hoặc mặc định) là kèm hộp sạc và bật chống ồn" in d1b["noi_dung"]
    assert "không so với số Tổng" in d1b["noi_dung"]
    # QĐ6 (không tạo giá trị bằng phép tính) và QT6 (con số điều kiện) có mục riêng.
    assert any(c["tieu_de"] == "Không tạo giá trị mới bằng phép tính" for c in tc.CA_DAC_BIET)
    assert any("nham_vai" in c["noi_dung"] for c in tc.CA_DAC_BIET)


def test_ca_dac_biet_khong_chep_cau_cua_bo_thu():
    duong = ROOT / "data/tuyen_bo/thu.jsonl"
    if not duong.exists():
        pytest.skip("không có data/tuyen_bo/thu.jsonl")
    tuyen_bo = [json.loads(d) for d in duong.read_text(encoding="utf-8-sig").splitlines() if d.strip()]
    kho = chuan_van(" ".join(c["tieu_de"] + " " + c["noi_dung"] for c in tc.CA_DAC_BIET))
    for t in tuyen_bo:
        assert chuan_van(t["tuyen_bo"]).rstrip(".") not in kho, t["id"]
        assert chuan_van(t["cau_goc"]).lstrip("- ").rstrip(".") not in kho, t["id"]


# ---------- Bước 16: hướng dẫn bản 2 (S1-S25) ----------

def test_tu_khang_dinh_doc_tu_muc_6_2(md):
    # S7, S17: danh sách từ khẳng định đọc từ hướng dẫn, không chép tay.
    tu = tc.tu_khang_dinh(md)
    assert tu["chac_chan"] == ["luôn", "đảm bảo", "bảo đảm", "ít nhất", "mọi lúc"]
    assert tu["muc_san"] == ["hơn <số>", "trên <số>", "không dưới <số>", "<số> trở lên"]
    assert tu["tu_hop_le"] == ["luôn", "đảm bảo", "bảo đảm", "ít nhất", "mọi lúc", "hơn", "trên", "không dưới", "trở lên"]
    md2 = sua(sua(md, 'Nhóm chắc chắn: "luôn", "đảm bảo"', 'Nhóm chắc chắn: "luôn", "chắc chắn", "đảm bảo"'),
              '"<số> trở lên".', '"<số> trở lên", "vượt <số>".')
    tu2 = tc.tu_khang_dinh(md2)
    assert "chắc chắn" in tu2["chac_chan"] and "vượt" in tu2["tu_hop_le"] and "vượt <số>" in tu2["muc_san"]
    hd2 = tc.dung_huong_dan(md2)
    d2 = next(d for d in hd2["dong_d"] if d["ma"] == "D2")
    assert "“chắc chắn”" in d2["cau_hoi"] and "“vượt <số>”" in d2["cau_hoi"]
    assert "chắc chắn" in hd2["tu_khang_dinh"]["tu_hop_le"]
    assert "không thấy dòng 'Nhóm mức sàn:'" in thoat(tc.tu_khang_dinh, sua(md, "Nhóm mức sàn:", "Nhóm khác:"))


def test_cau_hoi_d1_d2_trong_huong_dan_nhung(md):
    hd = tc.dung_huong_dan(md)
    dong = {d["ma"]: d for d in hd["dong_d"]}
    # D2 (S7): danh sách từ đã điền, không còn chỗ giữ chỗ; D1 (S4) còn {thuoc_tinh} để trang điền tên thuộc tính.
    assert "{tu_khang_dinh}" not in dong["D2"]["cau_hoi"]
    assert dong["D2"]["cau_hoi"].startswith("Tuyên bố có từ khẳng định gắn ngay với con số không (“luôn”, “đảm bảo”, “bảo đảm”, "
                                           "“ít nhất”, “mọi lúc”, “hơn <số>”, “trên <số>”, “không dưới <số>”, “<số> trở lên”)?")
    assert "{thuoc_tinh}" in dong["D1"]["cau_hoi"] and "{thuoc_tinh}" not in "".join(d["cau_hoi"] for m, d in dong.items() if m != "D1")


def test_ten_thuoc_tinh_tu_bang_muc_5(md):
    ten = tc.ten_thuoc_tinh(md)
    assert ten["dt|thoi_luong_pin"] == "Thời lượng pin" and ten["tn|thoi_luong_pin"] == "Thời lượng pin"
    assert ten["dh|sac_nhanh"] == "Sạc nhanh" and ten["dt|cong_suat_sac"] == "Công suất sạc" and ten["dt|khang_nuoc"] == "Kháng nước"
    assert len(ten) == 16
    cap = {f"{n}|{t}" for n, t in cap_cua_66_tuyen_bo()}
    assert cap <= set(ten), sorted(cap - set(ten))
    assert "phải có dạng 'Tên (`ma_thuoc_tinh`)'" in thoat(tc.ten_thuoc_tinh, sua(md, "Thời lượng pin (`thoi_luong_pin`) | Hoạt động*", "(`thoi_luong_pin`) | Hoạt động*"))
    assert "phải có mã trong dấu backtick" in thoat(tc.ten_thuoc_tinh, sua(md, "Thời lượng pin (`thoi_luong_pin`) | Hoạt động*", "Thời lượng pin | Hoạt động*"))


def test_khoa_co_mac_dinh_bo_sung_cho_khoa_khong_co(md):
    hang = tc.bang_mac_dinh(md)
    co = tc.khoa_co_mac_dinh(hang)
    khong_co = tc.khoa_khong_co_mac_dinh(hang)
    assert co[("dt", "sac_nhanh")]["cach_sac"] == {"dieu_kien": "Cách sạc", "hieu": "Sạc bằng cáp"}
    assert "moc_phan_tram" not in co[("dt", "sac_nhanh")] and "moc_phan_tram" in khong_co[("dt", "sac_nhanh")]
    assert co[("dt", "thoi_luong_pin")]["hoat_dong"]["hieu"].startswith("Hoạt động kém thuận lợi nhất")
    for kn_ in khong_co:  # hai bảng không giao nhau theo khóa
        assert not set(khong_co[kn_]) & set(co.get(kn_, {}))


DON_VI_MAU = [
    ("dt", "do_sang", "Độ sáng đỉnh 1000 nit", True), ("dt", "do_sang", "Độ sáng 3.000 cd/m²", True),
    ("dt", "do_sang", "Công nghệ ProMotion thích ứng lên đến 120Hz", False),
    ("dt", "tan_so_quet", "Công nghệ ProMotion thích ứng lên đến 120Hz", True),
    ("dt", "khang_nuoc", "Đạt mức IP68 (chống nước ở độ sâu tối đa 6 mét)", True), ("dt", "khang_nuoc", "chuẩn IPX7", True),
    ("dt", "khang_nuoc", "Độ sáng đỉnh 3000 nit", False), ("dt", "khang_nuoc", "chống nước ở độ sâu 6 mét", False),
    ("dt", "thoi_luong_pin", "Thời gian xem video Lên đến 30 giờ", True), ("dt", "thoi_luong_pin", "Pin 30h", True),
    ("dt", "thoi_luong_pin", "Sạc lên đến 50% trong 20 phút", False),
    ("tn", "thoi_luong_pin", "Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7", True),
    ("tn", "thoi_luong_pin", "Dung lượng pin tai nghe (mAh, Typical) 50", False),
    ("tn", "dung_luong_pin", "Dung lượng pin tai nghe (mAh, Typical) 50", True), ("dt", "dung_luong_pin", "pin 5500mAh", True),
    ("dt", "sac_nhanh", "Sạc lên đến 50% trong 20 phút", True), ("dt", "sac_nhanh", "Sạc 20 phút", True),
    ("dt", "cong_suat_sac", "Sạc nhanh HyperCharge 67W", True), ("dt", "cong_suat_sac", "Sạc 20 phút", False),
    ("dt", "zoom", "Độ phóng đại quang học 2x", True), ("dt", "zoom", "Độ phóng đại quang học", False),
    ("dh", "khang_nuoc", "Chống nước ở độ sâu 50m (chống nước khi bơi)", True), ("dh", "khang_nuoc", "tiêu chuẩn ISO 22810, 5ATM", True),
    ("dh", "khang_nuoc", "WR50", True), ("dh", "khang_nuoc", "Độ sáng đỉnh 1000 nit", False),
    ("dh", "sac_nhanh", "Sạc lên đến 80% trong khoảng 45 phút", True), ("dh", "sac_nhanh", "Sạc 8 phút dùng 8 giờ", True),
    ("dh", "do_sang", "Độ sáng đỉnh 1000 nit", True), ("dh", "thoi_luong_pin", "Chế Độ Nguồn Điện Thấp", False),
]


@pytest.mark.parametrize("nhom, thuoc_tinh, trich, mong", DON_VI_MAU)
def test_mau_don_vi_nhan_don_vi_cua_thuoc_tinh(md, nhom, thuoc_tinh, trich, mong):
    hang = {(h["nhom"], h["thuoc_tinh"]): h for h in tc.bang_huong_loi(md)}
    mau = re.compile(hang[(nhom, thuoc_tinh)]["don_vi_mau"])
    assert bool(mau.search(unicodedata.normalize("NFC", trich).lower())) is mong


def test_don_vi_khop_bang_chuan_hoa_cua_chung_yaml(md):
    chung = yaml.safe_load((ROOT / "data/cau_hinh/chung.yaml").read_text(encoding="utf-8"))
    don_vi = chung["chuan_hoa"]["don_vi"]
    dang = {k: {x.lower() for x in v} for k, v in tc.DON_VI_BIEU_DIEN.items()}
    assert {x.lower() for x in don_vi["gio"]} <= dang["giờ"] and {x.lower() for x in don_vi["phut"]} <= dang["phút"]
    assert {x.lower() for x in don_vi["nit"]} <= dang["nit"] and {x.lower() for x in don_vi["W"]} <= dang["W"]
    assert {x.lower() for x in don_vi["mAh"]} <= dang["mAh"] and {x.lower() for x in don_vi["Hz"]} <= dang["Hz"]
    assert {x.lower() for x in don_vi["x"]} <= dang["x"] and {x.lower() for x in don_vi["m"]} <= dang["m (ISO 22810)"]
    for ma in chung["chuan_hoa"]["iso_22810"]["quy_doi"]:  # 5ATM, WR50, 10ATM: nhận qua "atm" hoặc "wr"
        assert re.sub(r"\d+", "", ma.lower()) in dang["m (ISO 22810)"], ma
    # Mọi ô "Đơn vị" của bảng 6.1 đều có cách nhận; ô lạ thì thoát.
    assert {h["don_vi"] for h in tc.bang_huong_loi(md)} <= set(tc.DON_VI_BIEU_DIEN)
    tb = thoat(tc.bang_huong_loi, sua(md, "| `zoom` | x |", "| `zoom` | lần |"))
    assert "đơn vị 'lần' chưa có cách nhận" in tb and "DON_VI_BIEU_DIEN" in tb


def cum_tu_yaml(nhom):
    """Các cụm cấu hình của một nhóm theo YAML: {điều kiện: {giá trị: (tu_tai_lieu, hieu_biet_chung)}}."""
    ten = {"dt": "dien_thoai", "tn": "tai_nghe", "dh": "dong_ho"}[nhom]
    y = yaml.safe_load((ROOT / f"data/cau_hinh/{ten}.yaml").read_text(encoding="utf-8"))
    return {dk: {gt: (c.get("tu_tai_lieu") or [], c.get("hieu_biet_chung") or []) for gt, c in gts.items()}
            for dk, gts in y["cach_dien_dat"].items()}


def test_phu_luc_muc_13_khop_cau_hinh_yaml(md):
    # Phụ lục sinh từ YAML (hướng dẫn mục 13): đọc lại bảng phải ra đúng các cụm của cấu hình.
    cum = tc.bang_cum(md)
    for nhom in ("dt", "tn", "dh"):
        tu_bang = {dk["khoa"]: {g["gia_tri"]: (g["tu_tai_lieu"], g["hieu_biet_chung"]) for g in dk["gia_tri"]}
                   for dk in cum["nhom"][nhom]}
        assert tu_bang == cum_tu_yaml(nhom), nhom
    chung = yaml.safe_load((ROOT / "data/cau_hinh/chung.yaml").read_text(encoding="utf-8"))
    bang = {c["khoa"]: c["dong"] for c in cum["chung"]}
    assert [c["khoa"] for c in cum["chung"]] == list(tc.KHOA_CUM_CHUNG)
    kieu = {d["muc_con"].strip("`"): (d["tu_tai_lieu"], d["hieu_biet_chung"]) for d in bang["kieu_gia_tri"]}
    assert kieu == {k: (v["tu_tai_lieu"], v["hieu_biet_chung"]) for k, v in chung["kieu_gia_tri"].items()}
    quan_he = {d["muc_con"].strip("`"): (d["tu_tai_lieu"], d["hieu_biet_chung"]) for d in bang["cum_quan_he"]}
    assert quan_he == {k: (v["tu_tai_lieu"], v["hieu_biet_chung"]) for k, v in chung["dieu_kien_so"]["cum_quan_he"].items()}
    assert bang["tu_goi_muc_cao"][0]["tu_tai_lieu"] == chung["tu_goi_muc_cao"]["tu_tai_lieu"]
    assert bang["tu_goi_muc_cao"][0]["hieu_biet_chung"] == chung["tu_goi_muc_cao"]["hieu_biet_chung"]
    assert bang["ngu_canh_khong_quyet_dinh"][0]["tu_tai_lieu"] == chung["ngu_canh_khong_quyet_dinh"]["tu_tai_lieu"]


def test_khung_cum_dieu_kien_co_cum_cho_moi_khoa_cua_muc_5(md):
    # S23: mỗi khóa của bảng mục 5 (theo nhóm, thuộc tính) có mặt trong phụ lục của nhóm, nên khung không bao giờ trống.
    cum = tc.bang_cum(md)
    co = {n: {dk["khoa"] for dk in cum["nhom"][n]} for n in cum["nhom"]}
    for h in tc.bang_mac_dinh(md):
        for k in h["khoa"]:
            assert k["khoa"] in co[h["nhom"]], (h["nhom"], h["thuoc_tinh"], k["khoa"])
    assert "không thấy mục 13.4" in thoat(tc.bang_cum, md.replace("### 13.4 ", "### mười ba.4 "))


def test_trang_s1_s2_thu_tu_khung_va_cach_lam(trang):
    html, _ = trang
    thu_tu = [html.index(f'id="{ma}"') for ma in ("kh-cach-lam", "kh-mac-dinh", "kh-cum", "kh-quyet-dinh", "kh-ca-dac-biet", "kh-hay-dung")]
    assert thu_tu == sorted(thu_tu)  # S1: khung điều kiện (Bước 3) nằm trên bảng D1-D6 (Bước 4)
    assert "Khi tuyên bố không nói điều kiện" not in re.sub(r'<script id="du-lieu".*?</script>', "", html, flags=re.S)
    assert "Không chọn điều kiện theo con số của tuyên bố" in html
    cach_lam = re.search(r'id="kh-cach-lam" open>(.*?)</details>', html, flags=re.S).group(1)
    buoc = re.findall(r"<li>(.*?)</li>", cach_lam, flags=re.S)
    assert len(buoc) == 7  # S2: thêm bước "Xác định điều kiện"
    assert buoc[0].startswith("Đọc tuyên bố ở thẻ trên. Gán theo chữ của tuyên bố")
    chi_so = {k: next(i for i, b in enumerate(buoc) if b.startswith(k)) for k in ("Xác định điều kiện", "Dò bảng D1–D6")}
    assert chi_so["Xác định điều kiện"] < chi_so["Dò bảng D1–D6"]


def test_trang_s13_quy_tac_hay_dung(trang):
    html, _ = trang
    quy_tac = re.search(r'id="kh-hay-dung">(.*?)</details>', html, flags=re.S).group(1)
    assert "gắn ngay với con số" in quy_tac and "gắn với một mức" not in quy_tac
    assert "Cách hiểu mặc định dùng ở mọi dòng D" in quy_tac and "Không chọn điều kiện theo con số của tuyên bố" in quy_tac
    # Danh sách từ khẳng định không chép tay ở đây: nằm ở câu hỏi D2, đọc từ mục 6.2.
    assert "“ít nhất”" not in quy_tac and '"ít nhất"' not in quy_tac


def test_trang_s16_s20_s21_s22_s24(trang):
    html, du_lieu = trang
    js = re.search(r"<script>\n(.*?)</script>", html, flags=re.S).group(1)
    # S16: gợi ý đoạn khác cùng chữ vừa bôi đen.
    for chuoi in ("hienGoiYDoan(doanCoChu(chuanHoa(t)))", "' cũng có chữ này · '", "id=\"goi-y-doan\"", "button[data-them]"):
        assert chuoi in js or chuoi in html, chuoi
    assert "Ghi mọi đoạn có cùng con số ở cùng điều kiện" in html
    # S20: lượt 2.
    assert "Bước 16 · lượt 2" in html and "<title>Công cụ gán nhãn chuẩn - bộ thử, lượt 2</title>" in html
    assert "Tải nhãn (thu_luot2.jsonl)" in html and "Tải câu hỏi nhãn (cau_hoi_nhan_luot2.md)" in html
    assert "Nhập lại thu_luot2.jsonl đã xuất" in html and "luot: LUOT," in js and "luot: 1," not in js
    assert "tachTheoLuot(moi, LUOT)" in js and "taiXuong(TRANG.tep_nhan" in js and "taiXuong(TRANG.tep_hoi" in js
    assert "__LUOT__" not in html and "__TEP_NHAN__" not in html and "__TEP_HOI__" not in html
    assert "thu.jsonl" not in re.sub(r'<script id="du-lieu".*?</script>', "", html, flags=re.S)
    # S21: đồng hồ dừng khi không thao tác quá 3 phút; số giây bỏ ghi riêng.
    for chuoi in ("hoatDongCuoi", "dangNghi()", "congGio(bg(state.idx), dt, dangNghi())", "giay_nghi: Math.round(r.ms_nghi / 1000)",
                  "Không thao tác quá ", "lúc không thao tác"):
        assert chuoi in js, chuoi
    # S22: bài quảng cáo thu gọn sẵn, nói rõ gán theo chữ của tuyên bố.
    bai = re.search(r'<details class="hd" id="kh-bai">(.*?)</details>', html, flags=re.S).group(1)
    assert "Gán theo chữ của tuyên bố. Câu tô vàng chỉ để kiểm tách." in bai and "<code>tach=…</code>" in bai and 'id="bai"' in bai
    assert "$('kh-bai').addEventListener('toggle', cuonBai)" in js
    # S24: chữ hướng dẫn ô ghi chú liệt kê đủ mã.
    ghi_chu = re.search(r'<label for="ghi-chu">.*?<textarea id="ghi-chu"', html, flags=re.S).group(0)
    for ma in ("mac_dinh", "ngoai_cau_hinh", "ngoai_sau_loai", "khang_dinh", "chua_xac_dinh", "nham_vai"):
        assert ma + "=" in ghi_chu, ma
    assert du_lieu["trang"]["nghi_ms"] == tc.NGHI_GIAY * 1000 == 180000


# ---------- Chạy khối LUAT_KIEM của trang trong node, so với kiem_nhan.py ----------

DRIVER_JS = """
const kq = ca.map((c) => {
  if (c.ham === 'luat') return luatKiem(c.r, c.nhomTt);
  if (c.ham === 'doan') return doanCungChu(c.ds, c.daCo, c.t);
  if (c.ham === 'luot') return tachTheoLuot(c.moi, c.luot);
  if (c.ham === 'qua_nghi') return quaNghi(c.bayGio, c.cuoi, c.nghi);
  if (c.ham === 'cong_gio') { congGio(c.r, c.dt, c.nghi); return c.r; }
  if (c.ham === 'muc') return layMuc(c.v, c.ten);
  throw new Error('ham la ' + c.ham);
});
process.stdout.write(JSON.stringify(kq));
"""


def chay_khoi_node(trang, cases, tmp_path):
    """Chạy khối LUAT_KIEM của trang với danh sách ca; trả về danh sách kết quả (cùng thứ tự)."""
    node = shutil.which("node")
    if not node:
        pytest.skip("không có node")
    html, du_lieu = trang
    (tmp_path / "dl.json").write_text(json.dumps(du_lieu, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "ca.json").write_text(json.dumps(cases, ensure_ascii=False), encoding="utf-8")
    ma = ("const fs = require('fs');\nconst DL = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));\nconst HD = DL.huong_dan;\n"
          + khoi_luat_kiem(html) + "\nconst ca = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));\n" + DRIVER_JS)
    (tmp_path / "chay.js").write_text(ma, encoding="utf-8")
    kq = subprocess.run([node, str(tmp_path / "chay.js"), str(tmp_path / "dl.json"), str(tmp_path / "ca.json")],
                        capture_output=True, text=True, encoding="utf-8")
    assert kq.returncode == 0, kq.stderr
    return json.loads(kq.stdout)


def ban_ghi_ca(dong_d, ghi_chu, ly_do, trich, loai=None):
    """Dòng nhãn hợp lệ cho dòng D (mọi ô khớp nhau), chỉ ghi chú, lý do và câu trích là thứ cần thử."""
    nhan = tc.NHAN_THEO_DONG[dong_d]
    if loai is None:
        loai = tc.LOAI_THEO_DONG.get(dong_d) or {"LECH": "doi_dieu_kien", "SAI": "doi_gia_tri"}.get(nhan)
    d1 = dong_d == "D1"
    return {"id": "tb-00001", "nhan": nhan, "dong_d": dong_d, "loai": loai, "bang_chung": [] if d1 else ["m#001"],
            "trich": "" if d1 else trich, "ly_do": ly_do, "nguoi_gan": "x", "luot": 2, "giay": 5,
            "tai_lieu_mau_thuan": dong_d == "D1b", "ghi_chu": ghi_chu}


GHI_CHU_CA = ["", "mac_dinh=che_do_hien_thi", "mac_dinh=moc_phan_tram,cach_sac", "mac_dinh=hoat_dong; khang_dinh=luôn",
              "khang_dinh=hơn", "khang_dinh=Luôn, xyz", "chua_xac_dinh=đỉnh", "ngoai_cau_hinh=x; mac_dinh=bo_phan,che_do_chong_on",
              "mac_dinh=; chua_xac_dinh=", "mac_dinh=so_phut_sac", "khang_dinh=trở lên", "khang_dinh=hơn 16",
              "mac_dinh=bo_tiep_hop,moc_phan_tram; chua_xac_dinh=toàn màn hình", "mac_dinh=cap_sac", "mac_dinh=hoat_dong,hoat_dong",
              "chua_xac_dinh=a, b", "nham_vai=45W; mac_dinh=che_do_hien_thi,dien_tich_do"]
NHOM_TT_CA = [("dt", "do_sang"), ("dt", "sac_nhanh"), ("dt", "thoi_luong_pin"), ("dt", "khang_nuoc"), ("tn", "thoi_luong_pin"),
              ("tn", "sac_nhanh"), ("dh", "sac_nhanh"), ("dh", "thoi_luong_pin"), ("dh", "do_sang")]
TRICH_CA = ["Lên đến 6 giờ", "Độ sáng đỉnh 1000 nit", "Đạt mức IP68", "Sạc 50% trong 20 phút", "120Hz", "Độ phóng đại 2x", "Chống nước 50m",
            "Pin 5500 mAh"]
LY_DO_CA = ["Khớp với tài liệu: “Lên đến 6 giờ”.", "Khớp với tài liệu: “dt-apple-iphone17#016”.",
            "Nguồn: \"tn-samsung-buds3pro#038\" và “Lên đến 6 giờ”.", "Nguồn: dt-apple-iphone17#016 (không ngoặc kép).",
            "Khớp “Độ sáng #1” và “dh-apple-watchse3#008”", "Lý do không có ngoặc kép."]


def test_luat_kiem_trang_giong_kiem_nhan_py(trang, tmp_path):
    ca, mong = [], []
    for (nhom, tt), dong_d, ghi_chu in itertools.product(NHOM_TT_CA, tc.MA_DONG_D, GHI_CHU_CA):
        loai = "bo_dieu_kien" if dong_d == "D4" else None
        for loai_ in ([loai, "doi_dieu_kien"] if loai else [None]):
            ca.append((nhom, tt, ban_ghi_ca(dong_d, ghi_chu, LY_DO_CA[0], TRICH_CA[0], loai_)))
    for (nhom, tt), dong_d, ly_do, trich in itertools.product([NHOM_TT_CA[0], NHOM_TT_CA[4], NHOM_TT_CA[7]], ["D1", "D1a", "D2", "D4", "D6"],
                                                              LY_DO_CA, TRICH_CA):
        ca.append((nhom, tt, ban_ghi_ca(dong_d, "mac_dinh=hoat_dong; khang_dinh=luôn; chua_xac_dinh=x", ly_do, trich)))
    assert len(ca) > 2000
    kq_js = chay_khoi_node(trang, [{"ham": "luat", "r": nh, "nhomTt": f"{n}|{t}"} for n, t, nh in ca], tmp_path)
    so_loi = so_nhac = 0
    for (nhom, tt, nh), js in zip(ca, kq_js):
        tb = {"ma_mau": f"{nhom}-test", "thuoc_tinh": tt}
        py_loi, py_nhac = kn.kiem_mot_dong(nh, tb, None), kn.nhac_mot_dong(nh, tb)
        ctx = (nhom, tt, nh["dong_d"], nh["ghi_chu"], nh["ly_do"], nh["trich"], nh["loai"])
        assert sorted(set(js["loi"])) == sorted(set(py_loi)), ctx
        assert sorted(set(js["nhac"])) == sorted(set(py_nhac)), ctx
        so_loi += bool(py_loi)
        so_nhac += bool(py_nhac)
    assert so_loi > 500 and so_nhac > 200  # bộ ca đủ đa dạng: có ca lỗi, có ca nhắc, có ca sạch


def test_luat_kiem_trang_cac_luat_moi_theo_tung_ca(trang, tmp_path):
    def luat(dong_d, ghi_chu, nhom_tt="dt|do_sang", ly_do="Khớp với tài liệu: “Lên đến 6 giờ”.", trich="Độ sáng đỉnh 1000 nit", loai=None):
        return {"ham": "luat", "r": ban_ghi_ca(dong_d, ghi_chu, ly_do, trich, loai), "nhomTt": nhom_tt}
    ca = [luat("D2", ""), luat("D2", "khang_dinh=luôn"), luat("D2", "khang_dinh=rất"), luat("D2", "khang_dinh=hơn"),   # 0-3 (S17)
          luat("D1a", ""), luat("D1a", "mac_dinh=che_do_hien_thi"), luat("D1a", "chua_xac_dinh=đỉnh"),               # 4-6 (S18)
          luat("D1a", "mac_dinh=dien_tich_do", "dt|do_sang"), luat("D1a", "mac_dinh=cach_sac", "dt|sac_nhanh"),    # 7-8
          luat("D1", "mac_dinh=hoat_dong", "dt|thoi_luong_pin"), luat("D1", ""),                                    # 9-10 (S19)
          luat("D3", "", ly_do="Khớp với tài liệu: “dt-apple-iphone17#005”."),                                      # 11 (S14)
          luat("D3", "", trich="Độ sáng đỉnh 120Hz"), luat("D3", "", trich="Độ sáng đỉnh 1000 nit"),                # 12-13 (S15)
          luat("D4", "", loai="bo_dieu_kien")]                                                                      # 14
    kq = chay_khoi_node(trang, ca, tmp_path)
    ds_tu = "luôn, đảm bảo, bảo đảm, ít nhất, mọi lúc, hơn, trên, không dưới, trở lên"
    assert kq[0]["loi"] == [tc.THONG_BAO["d2_thieu_khang_dinh"].format(ds=ds_tu)] and kq[1]["loi"] == [] and kq[3]["loi"] == []
    assert kq[2]["loi"] == [tc.THONG_BAO["d2_khang_dinh_la"].format(tu="rất", ds=ds_tu)]
    assert kq[4]["loi"][0].startswith("Dòng D1a phải ghi nguyên nhân") and "che_do_hien_thi" in kq[4]["loi"][0]
    assert kq[5]["loi"] == [] and kq[6]["loi"] == []
    # dien_tich_do là khóa "như hãng công bố": không ghi được (rà soát 02/11), cộng hai lỗi D1a.
    assert len(kq[7]["loi"]) == 3 and "không phải khóa ghi được" in kq[7]["loi"][0]
    assert "mac_dinh=dien_tich_do" in kq[7]["loi"][2] and "Như hãng công bố" in kq[7]["loi"][2]
    assert len(kq[8]["loi"]) == 2 and "Sạc bằng cáp" in kq[8]["loi"][1]
    assert kq[9]["loi"] == [] and kq[9]["nhac"][0] == tc.NHAC["d1_co_mac_dinh"] and kq[10]["nhac"] == []
    assert kq[11]["loi"] == [tc.THONG_BAO["ly_do_ma_doan"].format(ma="dt-apple-iphone17#005")]
    assert kq[12]["nhac"] == [tc.NHAC["trich_thieu_don_vi"].format(thuoc_tinh="do_sang", don_vi="nit")] and kq[13]["nhac"] == []
    assert kq[14]["nhac"] == [tc.NHAC["bo_dieu_kien_thieu_mac_dinh"]] and kq[12]["loi"] == [] and kq[13]["loi"] == []


def test_ham_thuan_s16_s20_s21_trong_node(trang, tmp_path):
    ds = [{"id": "m#001", "noi_dung": "Pin\nLên đến 6 giờ", "chu_thich": []},
          {"id": "m#002", "noi_dung": "Tổng 26 giờ", "chu_thich": ["Đến  6 giờ khi bật ANC"]},
          {"id": "m#003", "noi_dung": "Đến 6 giờ (bật ANC)", "chu_thich": None},
          {"id": "m#004", "noi_dung": "6 giờ", "chu_thich": []}]
    ca = [{"ham": "doan", "ds": ds, "daCo": ["m#001"], "t": "6 giờ"}, {"ham": "doan", "ds": ds, "daCo": [], "t": "Đến 6 giờ"},
          {"ham": "doan", "ds": ds, "daCo": [], "t": ""}, {"ham": "doan", "ds": ds, "daCo": [], "t": "đến 6 giờ"},
          {"ham": "luot", "moi": [{"id": "a", "luot": 2}, {"id": "b", "luot": 1}, {"id": "c"}, None, {"id": "d", "luot": 2}], "luot": 2},
          {"ham": "luot", "moi": [{"id": "b", "luot": 1}], "luot": 2},
          {"ham": "qua_nghi", "bayGio": 1000000, "cuoi": 820000, "nghi": 180000},
          {"ham": "qua_nghi", "bayGio": 1000001, "cuoi": 820000, "nghi": 180000},
          {"ham": "cong_gio", "r": {"ms": 10, "ms_nghi": 0}, "dt": 250, "nghi": False},
          {"ham": "cong_gio", "r": {"ms": 10, "ms_nghi": 0}, "dt": 250, "nghi": True},
          {"ham": "muc", "v": "ngoai_cau_hinh=x; khang_dinh=luôn, ít nhất ;mac_dinh=a", "ten": "khang_dinh"}]
    kq = chay_khoi_node(trang, ca, tmp_path)
    assert kq[0] == ["m#002", "m#003", "m#004"]  # S16: đoạn chưa là bằng chứng mà có chuỗi (kể cả trong chú thích, sau gộp khoảng trắng)
    assert kq[1] == ["m#002", "m#003"] and kq[2] == [] and kq[3] == ["m#001"]  # phân biệt hoa thường; chuỗi trống thì không gợi ý
    assert kq[4] == {"dung": [{"id": "a", "luot": 2}, {"id": "d", "luot": 2}], "khac": 3, "luot_khac": [1, "không có"]}  # S20
    assert kq[5]["dung"] == [] and kq[5]["khac"] == 1 and kq[5]["luot_khac"] == [1]
    assert kq[6] is False and kq[7] is True  # S21: quá 3 phút (180000 ms) mới nghỉ
    assert kq[8] == {"ms": 260, "ms_nghi": 0} and kq[9] == {"ms": 10, "ms_nghi": 250}
    assert kq[10] == ["luôn", "ít nhất"]


def test_luu_va_sang_khong_ghi_de_nguoi_gan_khi_khong_sua():
    # Rà soát 02/11 (lỗi 2): bản ghi nhập từ tệp mà người duyệt không sửa nội dung thì giữ người gán của tệp.
    src = tc.SCRIPT_JS if hasattr(tc, "SCRIPT_JS") else Path(tc.__file__).read_text(encoding="utf-8")
    assert "function noiDungNhan(r)" in src and "r.nd_goc = noiDungNhan(r); // nội dung lúc nhập" in src
    assert "if (!(r.nguoi_gan && r.nd_goc && r.nd_goc === noiDungNhan(r))) r.nguoi_gan = state.nguoi_gan.trim();" in src


def test_khung_cum_loc_theo_chi_thuoc_tinh():
    # Rà soát 02/11 (lỗi 1): "kèm hộp sạc" (kem_hop_sac) chỉ hiện cho thời lượng pin.
    md = tc.doc_huong_dan()
    tn = {dk["khoa"]: dk for dk in tc.bang_cum(md)["nhom"]["tn"]}
    kem = next(g for g in tn["bo_phan"]["gia_tri"] if g["gia_tri"] == "kem_hop_sac")
    assert kem["chi_thuoc_tinh"] == ["thoi_luong_pin"]
    assert all(g["chi_thuoc_tinh"] == [] for g in tn["bo_phan"]["gia_tri"] if g["gia_tri"] != "kem_hop_sac")
    src = Path(tc.__file__).read_text(encoding="utf-8")
    assert "!gt.chi_thuoc_tinh.includes(tb.thuoc_tinh)) continue;" in src
