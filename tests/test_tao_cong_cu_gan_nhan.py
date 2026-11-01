import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("tao_cong_cu_gan_nhan", ROOT / "scripts/tao_cong_cu_gan_nhan.py")
tc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tc)

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
    assert set(hd) == {"html", "muc_luc_html", "nhom", "nhan", "loai", "dong_d", "mac_dinh", "huong_loi"}
    json.dumps(hd, ensure_ascii=False)
    assert 'id="hd-muc-8"' in hd["html"] and 'href="#hd-muc-8"' in hd["muc_luc_html"]
    assert 'id="hd-muc-6-1"' in hd["html"]


# ---------- Bảng D1-D6: suy nhãn, câu hỏi, ví dụ ----------

CAU_HOI = {
    "D1": "Tài liệu có nói gì về thông số này của đúng sản phẩm không? Không có thì dừng.",
    "D1a": "Có biết tuyên bố đang nói ở điều kiện nào không? Tuyên bố nêu rõ thì biết. Không nêu thì xem khung “Khi tuyên bố "
           "không nói điều kiện” bên dưới: dòng đó ghi “Không có mặc định” thì không biết, dừng.",
    "D1b": "Ở điều kiện đó, tài liệu có ghi hai số khác nhau không? Có thì dừng.",
    "D2": "Tuyên bố có chữ “luôn”, “đảm bảo”, “bảo đảm”, “ít nhất”, “mọi lúc” biến mức “lên đến” của hãng thành mức chắc "
          "chắn không? Có thì dừng.",
    "D3": "Ở đúng điều kiện đó, số của tuyên bố bằng hoặc kém hơn số của hãng không? Có thì dừng.",
    "D4": "Số của tuyên bố có trùng số hãng ghi cho một điều kiện khác không? Có thì dừng.",
    "D5": "Số của tuyên bố có đẹp hơn số hãng ghi ở cùng điều kiện, hoặc đẹp hơn mọi số hãng ghi không? Có thì dừng.",
    "D6": "Không rơi vào dòng nào ở trên.",
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
    assert dong_d["D5"]["ghi_chu_nho"].endswith("kháng nước so theo mục 6.6.")
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
    # kiem_nhan.py dùng đúng các bảng này (import lại), nên hai bên cùng chữ.
    spec_kn = importlib.util.spec_from_file_location("kiem_nhan_cho_so_sanh", ROOT / "scripts/kiem_nhan.py")
    kn = importlib.util.module_from_spec(spec_kn)
    spec_kn.loader.exec_module(kn)
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
                  "Khi tuyên bố không nói điều kiện (dùng ở D1a)", "Quy tắc hay dùng",
                  "Mở hướng dẫn đầy đủ", "Dùng Ctrl+F để tìm", "Chèn mẫu câu",
                  "Hướng dẫn chưa có cách hiểu mặc định cho thuộc tính này.",
                  "Các tuyên bố sau đã lưu nhưng không qua quy tắc mới, mở lại để sửa: ",
                  "Lý do còn chỗ {…} chưa thay", "gan_nhan_giao_dien_v1", "gan_nhan_thu_v1",
                  "Số có thật nhưng ở điều kiện khác, hoặc biến \"lên đến\" thành chắc chắn",
                  "Chọn loại bằng 2 câu hỏi.", 'id="goi-y-lech"', 'id="goi-y-sai"', "'Hướng dẫn mục 8: '"):
        assert chuoi in html, chuoi
    # Mỗi loại hợp lệ của LECH và SAI có chữ ngắn trong ô chọn.
    chu_loai = re.search(r"const CHU_LOAI = \{(.*?)\n\};", html, flags=re.S).group(1)
    lech, sai = chu_loai.split("SAI:")
    for ma in ("bo_dieu_kien", "doi_dieu_kien", "doi_bo_phan", "doi_phien_ban", "doi_kieu_gia_tri"):
        assert ma + ":" in lech, ma
    for ma in ("doi_gia_tri", "doi_bo_phan", "doi_phien_ban"):
        assert ma + ":" in sai, ma
    assert html.count('<details class="hd"') == 5
    assert '<details class="hd" id="kh-hay-dung">' in html  # khung Quy tắc hay dùng đóng sẵn
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
    assert du_lieu["quy_tac"] == {"thong_bao": tc.THONG_BAO, "nhac": tc.NHAC}
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
    for ten in ("function kiem(", "function nhacCuaTuyenBo(", "function chonDong("):
        dau = js.index(ten)
        than = js[dau:js.index("\nfunction ", dau + 10)]
        assert not re.search(r"\b(tb|TB\[[^\]]*\])\.(tuyen_bo|cau_goc|ghi_chu|llm_sinh|che_do|loai_bai|url_nguon)\b", than), ten


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
    assert "gan_nhan_thu_v1" in html  # khóa lưu nhãn không đổi


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
        assert {"tieu_de", "noi_dung", "nguon", "thuoc_tinh"} <= c.keys()
        assert ("ma_mau" in c) != ("nhom" in c)
        assert c.get("nhom", c.get("ma_mau", "").split("-")[0]) in {"dt", "tn", "dh"}
        assert c["thuoc_tinh"] in thuoc_tinh
        assert "{" not in c["noi_dung"]
