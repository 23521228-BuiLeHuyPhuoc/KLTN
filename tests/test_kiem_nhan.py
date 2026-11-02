import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("kiem_nhan", ROOT / "scripts/kiem_nhan.py")
kn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kn)

DOAN = [
    {"id": "dt-test#001", "ma_mau": "dt-test", "noi_dung": "Pin\nXem video liên tục\nLên đến 30 giờ", "chu_thich": []},
    {"id": "dt-test#002", "ma_mau": "dt-test", "noi_dung": "Màn hình 1000 nit",
     "chu_thich": ["Độ sáng đo   trong phòng thí nghiệm", "Kết quả thực tế có thể khác"]},
    {"id": "dt-test#003", "ma_mau": "dt-test", "noi_dung": "Chống nước IP68", "chu_thich": []},
    # Đoạn đã bỏ số chú thích của trang hãng: noi_dung là chữ hiển thị, noi_dung_goc là bản trước khi bỏ.
    {"id": "dt-test#004", "ma_mau": "dt-test", "noi_dung": "Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W\nBền bỉ",
     "noi_dung_goc": "Sạc lên đến 50% trong 20 phút6 với bộ tiếp hợp 40W\nBền bỉ", "chu_thich": ["Đo với bộ tiếp hợp 40W"]},
]
TUYEN_BO = [{"id": f"tb-{i:05d}", "ma_mau": "dt-test", "thuoc_tinh": "do_sang"} for i in range(1, 5)]
# Bản rút gọn của khóa "không có mặc định" ở mục 5 (khong_co_mac_dinh() đọc bản thật từ hướng dẫn).
KHONG_CO = {("dt", "do_sang"): {"che_do_hien_thi": "Chế độ hiển thị"}}
# Dòng D thường đi với từng nhãn (D6 cho phép có hoặc không có bằng chứng).
DONG_THEO_NHAN = {"DUNG": "D3", "SAI": "D5", "LECH": "D4", "CHUA_DU": "D6"}


def ghi_jsonl(duong, dong):
    duong.parent.mkdir(parents=True, exist_ok=True)
    duong.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in dong), encoding="utf-8")
    return duong


def nhan(ma, **kw):
    """Một dòng nhãn hợp lệ (SAI/doi_gia_tri, D5) với các trường ghi đè bởi kw. Không truyền dong_d thì lấy dòng D
    thường đi với nhãn (D1b nếu tai_lieu_mau_thuan là true)."""
    dong = {"id": ma, "nhan": "SAI", "dong_d": "D5", "loai": "doi_gia_tri", "bang_chung": ["dt-test#002"],
            "trich": "Màn hình 1000 nit", "ly_do": "Tài liệu ghi 1000 nit; tuyên bố ghi 3000.",
            "nguoi_gan": "phuoc", "luot": 1, "giay": 40, "tai_lieu_mau_thuan": False, "ghi_chu": ""}
    dong.update(kw)
    if "dong_d" not in kw:
        dong["dong_d"] = "D1b" if dong["tai_lieu_mau_thuan"] is True else DONG_THEO_NHAN.get(dong["nhan"], "D5")
    return dong


@pytest.fixture
def mt(tmp_path):
    """Thư mục tạm có nguon/dt-test/doan.jsonl và tệp tuyên bố 4 dòng."""
    nguon = tmp_path / "nguon"
    ghi_jsonl(nguon / "dt-test" / "doan.jsonl", DOAN)
    return {"nguon": nguon, "tb": ghi_jsonl(tmp_path / "thu.jsonl", TUYEN_BO), "nhan": tmp_path / "nhan.jsonl"}


def chay(mt, dong):
    ghi_jsonl(mt["nhan"], dong)
    return kn.kiem_tep(mt["nhan"], mt["tb"], mt["nguon"])


def bo_dung():
    """Bốn nhãn hợp lệ, mỗi loại nhãn một dòng."""
    return [
        nhan("tb-00001", nhan="DUNG", loai=None, bang_chung=["dt-test#001"], trich="Lên đến 30 giờ", giay=30),
        nhan("tb-00002"),
        nhan("tb-00003", nhan="LECH", loai="doi_dieu_kien", bang_chung=["dt-test#002"],
             trich="Độ sáng đo trong phòng thí nghiệm", giay=51),
        nhan("tb-00004", nhan="CHUA_DU", loai=None, bang_chung=[], trich="", giay=19, tai_lieu_mau_thuan=True),
    ]


def test_tep_hop_le_khong_loi_va_tom_tat(mt):
    loi, dong_nhan, so_tb = chay(mt, bo_dung())
    assert loi == []
    assert so_tb == 4 and len(dong_nhan) == 4
    chu = "\n".join(kn.tom_tat(dong_nhan, so_tb))
    assert "DUNG       1" in chu and "CHUA_DU    1" in chu
    assert "doi_gia_tri        1" in chu and "doi_dieu_kien      1" in chu
    assert "tổng 140 giây" in chu  # 30 + 40 + 51 + 19
    assert "trung bình 35.0 giây" in chu and "trung vị 35 giây" in chu  # trung vị của 19, 30, 40, 51
    assert "Tài liệu mâu thuẫn: 1" in chu


def test_thieu_nhan_id_la_va_id_lap(mt):
    dong = bo_dung()[:3] + [nhan("tb-00001"), nhan("tb-99999")]
    loi, _, _ = chay(mt, dong)
    chu = "\n".join(loi)
    assert "thiếu nhãn cho tb-00004" in chu
    assert "tb-99999" in chu and "không có trong tệp tuyên bố" in chu
    assert "id tb-00001 lặp" in chu


@pytest.mark.parametrize("sua, mong", [
    ({"nhan": "TOT", "loai": None}, "không thuộc"),
    ({"nhan": "LECH", "loai": None}, "nhan LECH cần loai"),
    ({"nhan": "LECH", "loai": "doi_gia_tri"}, "doi_gia_tri chỉ dùng cho SAI"),
    ({"nhan": "SAI", "loai": None}, "nhan SAI cần loai"),
    ({"nhan": "SAI", "loai": "khac"}, "nhan SAI cần loai"),
    # SAI không đi với các loại của LECH, thông báo nói rõ đó là loại của nhãn LECH.
    ({"nhan": "SAI", "loai": "doi_dieu_kien"}, "loại của nhãn LECH, không dùng cho SAI"),
    ({"nhan": "SAI", "loai": "bo_dieu_kien"}, "loại của nhãn LECH, không dùng cho SAI"),
    ({"nhan": "SAI", "loai": "doi_kieu_gia_tri"}, "loại của nhãn LECH, không dùng cho SAI"),
    ({"nhan": "DUNG", "loai": "doi_gia_tri"}, "loai phải là null"),
    ({"nhan": "CHUA_DU", "loai": "bo_dieu_kien", "bang_chung": [], "trich": ""}, "loai phải là null"),
])
def test_loai_theo_nhan(mt, sua, mong):
    loi, _, _ = chay(mt, [nhan("tb-00001", **sua)] + bo_dung()[1:])
    assert any(mong in e for e in loi), loi


@pytest.mark.parametrize("ma_nhan, loai", [("SAI", "doi_gia_tri"), ("SAI", "doi_bo_phan"), ("SAI", "doi_phien_ban"),
                                           ("LECH", "bo_dieu_kien"), ("LECH", "doi_dieu_kien"), ("LECH", "doi_bo_phan"),
                                           ("LECH", "doi_phien_ban"), ("LECH", "doi_kieu_gia_tri")])
def test_loai_hop_le(mt, ma_nhan, loai):
    loi, _, _ = chay(mt, [nhan("tb-00001", nhan=ma_nhan, loai=loai)] + bo_dung()[1:])
    assert loi == []


def test_hang_loai_theo_nhan():
    # LOAI_TAT_CA đủ 6 loại cho phần thống kê; LECH 5 loại; SAI 3 loại; giao của hai là bộ phận và phiên bản.
    assert len(kn.LOAI_TAT_CA) == 6 and set(kn.LOAI_TAT_CA) == set(kn.LOAI_LECH) | set(kn.LOAI_SAI)
    assert kn.LOAI_SAI == ("doi_gia_tri", "doi_bo_phan", "doi_phien_ban")
    assert set(kn.LOAI_LECH) & set(kn.LOAI_SAI) == {"doi_bo_phan", "doi_phien_ban"}


def test_tom_tat_liet_ke_du_6_loai(mt):
    _, dong_nhan, so_tb = chay(mt, bo_dung())
    chu = "\n".join(kn.tom_tat(dong_nhan, so_tb))
    for loai in kn.LOAI_TAT_CA:
        assert f"  {loai:<16}" in chu, loai


# ---------- Dòng D (dong_d): bảng suy nhãn và các lỗi mâu thuẫn giữa các ô ----------

def test_bang_suy_nhan_tu_dong_d():
    assert kn.MA_DONG_D == ("D1", "D1a", "D1b", "D2", "D3", "D4", "D5", "D6")
    assert kn.NHAN_THEO_DONG == {"D1": "CHUA_DU", "D1a": "CHUA_DU", "D1b": "CHUA_DU", "D2": "LECH", "D3": "DUNG",
                                 "D4": "LECH", "D5": "SAI", "D6": "CHUA_DU"}
    assert kn.LOAI_THEO_DONG == {"D2": "doi_kieu_gia_tri"} and kn.DONG_TICK_MAU_THUAN == "D1b"
    assert kn.TRUONG[:3] == ("id", "nhan", "dong_d")  # dong_d ngay sau nhan, như công cụ HTML xuất
    assert all(n in kn.NHAN for n in kn.NHAN_THEO_DONG.values())


def bo_theo_dong(dong_d):
    """Một dòng nhãn hợp lệ cho dòng D đã cho (D1 không bằng chứng, D1b có tick, D2 loại doi_kieu_gia_tri)."""
    nhan_d = kn.NHAN_THEO_DONG[dong_d]
    kw = {"nhan": nhan_d, "dong_d": dong_d, "loai": None}
    if nhan_d == "LECH":
        kw["loai"] = kn.LOAI_THEO_DONG.get(dong_d, "doi_dieu_kien")
    if nhan_d == "SAI":
        kw["loai"] = "doi_gia_tri"
    if dong_d == "D1":
        kw.update(bang_chung=[], trich="")
    if dong_d == "D1b":
        kw["tai_lieu_mau_thuan"] = True
    if dong_d == "D1a":
        kw["ghi_chu"] = "chua_xac_dinh=đỉnh"  # D1a phải ghi nguyên nhân (hướng dẫn mục 8)
    if dong_d == "D2":
        kw["ghi_chu"] = "khang_dinh=luôn"  # D2 phải ghi từ khẳng định
    return nhan("tb-00001", **kw)


@pytest.mark.parametrize("dong_d", kn.MA_DONG_D)
def test_moi_dong_d_hop_le_voi_nhan_tuong_ung(mt, dong_d):
    loi, dong_nhan, _ = chay(mt, [bo_theo_dong(dong_d)] + bo_dung()[1:])
    assert loi == [], loi
    assert dong_nhan[0]["dong_d"] == dong_d


@pytest.mark.parametrize("dong_d", kn.MA_DONG_D)
def test_nhan_khong_khop_dong_d(mt, dong_d):
    mong = kn.NHAN_THEO_DONG[dong_d]
    for sai in kn.NHAN:
        if sai == mong:
            continue
        dong = bo_theo_dong(dong_d)
        # Chỉ đổi nhãn (và loại cho hợp nhãn mới); các lỗi khác nếu có không làm mất lỗi nhãn không khớp dòng D.
        dong.update(nhan=sai, loai={"LECH": "doi_dieu_kien", "SAI": "doi_gia_tri"}.get(sai))
        loi = chay(mt, [dong] + bo_dung()[1:])[0]
        chuoi = kn.THONG_BAO["nhan_khong_khop"].format(nhan=sai, dong_d=dong_d, nhan_mong=mong)
        assert chuoi in "\n".join(loi), (dong_d, sai, loi)


def test_loi_1_chua_chon_dong_d(mt):
    chua = "Chưa bấm “Dừng ở đây” ở bảng D1–D6."
    assert kn.THONG_BAO["chua_chon_dong"] == chua
    for gia_tri in (None, "", "  "):
        loi = chay(mt, [nhan("tb-00001", dong_d=gia_tri)] + bo_dung()[1:])[0]
        assert loi == [f"dòng 1 (tb-00001): {chua}"], loi
    bo = nhan("tb-00001")
    del bo["dong_d"]
    loi = chay(mt, [bo] + bo_dung()[1:])[0]
    assert loi == ["dòng 1 (tb-00001): thiếu trường: dong_d"], loi  # trường bắt buộc
    loi = chay(mt, [nhan("tb-00001", dong_d="D7")] + bo_dung()[1:])[0]
    assert len(loi) == 1 and "dong_d 'D7' không thuộc D1, D1a, D1b, D2, D3, D4, D5, D6" in loi[0]


def test_loi_2_nhan_khong_khop_dong_d_thong_bao(mt):
    loi = chay(mt, [nhan("tb-00001", nhan="DUNG", loai=None, dong_d="D4")] + bo_dung()[1:])[0]
    assert len(loi) == 1 and "Nhãn DUNG không khớp dòng D4: dòng D4 phải ra nhãn LECH" in loi[0], loi
    assert "D1, D1a, D1b, D6: CHUA_DU; D2, D4: LECH; D3: DUNG; D5: SAI" in loi[0]
    # Nhãn không thuộc bốn nhãn thì chỉ báo lỗi nhãn, không báo thêm không khớp.
    loi = chay(mt, [nhan("tb-00001", nhan="TOT", loai=None, dong_d="D3")] + bo_dung()[1:])[0]
    assert len(loi) == 1 and "không thuộc" in loi[0], loi


@pytest.mark.parametrize("sua", [{"bang_chung": ["dt-test#001"]}, {"trich": "Màn hình 1000 nit"},
                                 {"bang_chung": ["dt-test#001"], "trich": "Lên đến 30 giờ"},
                                 {"bang_chung": ["dt-test#099"], "trich": ""}])
def test_loi_3_d1_khong_co_bang_chung_hay_trich(mt, sua):
    dong = bo_theo_dong("D1")
    dong.update(sua)
    loi = chay(mt, [dong] + bo_dung()[1:])[0]
    mau = "D1 nghĩa là tài liệu không có thông số này, nên bằng chứng và câu trích để trống."
    assert sum(mau in e for e in loi) == 1 and all(e.startswith("dòng 1 (tb-00001): ") for e in loi), loi
    # Không kèm lời khuyên ngược ("hãy thêm đoạn chứa câu trích làm bằng chứng") cho cùng một chỗ sai.
    assert not any("hãy thêm" in e or "trich rỗng" in e or "bang_chung rỗng" in e for e in loi), loi
    if sua.get("bang_chung") == ["dt-test#099"]:  # mã bằng chứng không có thật vẫn bị báo riêng
        assert len(loi) == 2 and any("mã bằng chứng dt-test#099 không có trong" in e for e in loi)
    else:
        assert len(loi) == 1, loi


def test_d1_de_trong_hop_le_va_cac_dong_chua_du_khac_duoc_co_bang_chung(mt):
    assert chay(mt, [bo_theo_dong("D1")] + bo_dung()[1:])[0] == []
    for d in ("D1a", "D1b", "D6"):
        dong = bo_theo_dong(d)  # có bang_chung và trich mặc định của nhan()
        assert dong["bang_chung"] and chay(mt, [dong] + bo_dung()[1:])[0] == [], d


def test_loi_4_d1b_khi_va_chi_khi_tai_lieu_mau_thuan(mt):
    loi = chay(mt, [nhan("tb-00001", nhan="CHUA_DU", loai=None, dong_d="D1b", tai_lieu_mau_thuan=False)] + bo_dung()[1:])[0]
    assert len(loi) == 1 and "Dòng D1b là tài liệu ghi hai số khác nhau" in loi[0] and "tai_lieu_mau_thuan" in loi[0], loi
    for d, kw in (("D3", {"nhan": "DUNG", "loai": None}), ("D4", {"nhan": "LECH", "loai": "doi_dieu_kien"}),
                  ("D5", {}), ("D1a", {"nhan": "CHUA_DU", "loai": None, "ghi_chu": "chua_xac_dinh=x"}),
                  ("D1", {"nhan": "CHUA_DU", "loai": None, "bang_chung": [], "trich": ""})):
        loi = chay(mt, [nhan("tb-00001", dong_d=d, tai_lieu_mau_thuan=True, **kw)] + bo_dung()[1:])[0]
        assert len(loi) == 1 and f"mà dòng là {d}: chỉ dòng D1b mới có" in loi[0], (d, loi)
    assert chay(mt, [bo_theo_dong("D1b")] + bo_dung()[1:])[0] == []


def test_tai_lieu_mau_thuan_khong_con_bao_hai_lan_va_nhan_sai_chi_bao_loi_nhan(mt):
    # Tick mà nhãn không phải CHUA_DU: một lỗi theo dòng D, không thêm lỗi "phải là CHUA_DU" riêng.
    loi = chay(mt, [nhan("tb-00001", nhan="DUNG", loai=None, dong_d="D1b", tai_lieu_mau_thuan=True)] + bo_dung()[1:])[0]
    assert len(loi) == 1 and "Nhãn DUNG không khớp dòng D1b" in loi[0], loi
    loi = chay(mt, [nhan("tb-00001", nhan="TOT", loai=None, dong_d="D1b", tai_lieu_mau_thuan=True)] + bo_dung()[1:])[0]
    assert len(loi) == 1 and "không thuộc" in loi[0], loi


def test_loi_5_d2_thi_loai_la_doi_kieu_gia_tri(mt):
    mau = "Dòng D2 là lệch kiểu giá trị, nên loại phải là doi_kieu_gia_tri (đang là 'doi_dieu_kien')."
    kd = {"ghi_chu": "khang_dinh=luôn"}  # D2 phải ghi từ khẳng định; ở đây chỉ thử loại
    loi = chay(mt, [nhan("tb-00001", nhan="LECH", dong_d="D2", loai="doi_dieu_kien", **kd)] + bo_dung()[1:])[0]
    assert loi == [f"dòng 1 (tb-00001): {mau}"], loi
    assert chay(mt, [nhan("tb-00001", nhan="LECH", dong_d="D2", loai="doi_kieu_gia_tri", **kd)] + bo_dung()[1:])[0] == []
    # Loại trống: đã có lỗi "nhan LECH cần loai", không báo thêm lần hai.
    loi = chay(mt, [nhan("tb-00001", nhan="LECH", dong_d="D2", loai=None, **kd)] + bo_dung()[1:])[0]
    assert len(loi) == 1 and "nhan LECH cần loai" in loi[0], loi
    # D4 cũng cho doi_kieu_gia_tri (tuyên bố ghi rõ kiểu giá trị khác, hướng dẫn V37), không bị ép loại.
    assert chay(mt, [nhan("tb-00001", nhan="LECH", dong_d="D4", loai="doi_kieu_gia_tri")] + bo_dung()[1:])[0] == []


def mac_dinh(khoa, **kw):
    """Dòng nhãn DUNG (D3) có ghi chú mac_dinh=<khoa>; kw ghi đè các trường khác."""
    return nhan("tb-00001", **{"nhan": "DUNG", "loai": None, "ghi_chu": f"mac_dinh={khoa}", **kw})


def chay_voi(mt, dong):
    """Lỗi khi kiểm với KHONG_CO (bản rút gọn) thay vì đọc hướng dẫn thật."""
    ghi_jsonl(mt["nhan"], dong)
    return kn.kiem_tep(mt["nhan"], mt["tb"], mt["nguon"], KHONG_CO)[0]


def test_loi_6_mac_dinh_cua_dieu_kien_khong_co_mac_dinh(mt):
    chu = ("Ghi chú có mac_dinh=che_do_hien_thi, mà “Chế độ hiển thị” không có mặc định: tuyên bố không nói điều kiện "
           "này thì dừng ở D1a, nhãn Chưa đủ thông tin.")
    for d, kw in (("D3", {}), ("D4", {"nhan": "LECH", "loai": "doi_dieu_kien"}), ("D6", {"nhan": "CHUA_DU", "loai": None})):
        loi = chay_voi(mt, [mac_dinh("che_do_hien_thi", dong_d=d, **kw)] + bo_dung()[1:])
        assert loi == [f"dòng 1 (tb-00001): {chu}"], (d, loi)
    # D1 dừng trước khi xét điều kiện nên không ghi mac_dinh: không phải lỗi "phải dừng ở D1a", chỉ nhắc (S19).
    d1 = mac_dinh("che_do_hien_thi", dong_d="D1", nhan="CHUA_DU", loai=None, bang_chung=[], trich="")
    assert chay_voi(mt, [d1] + bo_dung()[1:]) == [] and kn.nhac_mot_dong(d1) == [kn.NHAC["d1_co_mac_dinh"]]
    # Đúng dòng D1a thì cho phép (hướng dẫn V25); khóa khác thì không bị; nhiều khóa thì chỉ khóa không có mặc định bị báo.
    dung = nhan("tb-00001", nhan="CHUA_DU", dong_d="D1a", loai=None, ghi_chu="mac_dinh=che_do_hien_thi")
    assert chay_voi(mt, [dung] + bo_dung()[1:]) == []
    assert chay_voi(mt, [mac_dinh("ngoai_bang", dong_d="D3")] + bo_dung()[1:]) == []
    loi = chay_voi(mt, [mac_dinh("ngoai_bang, che_do_hien_thi", dong_d="D3")] + bo_dung()[1:])
    assert len(loi) == 1 and "mac_dinh=che_do_hien_thi" in loi[0]
    # mac_dinh nằm giữa các mục ghi chú khác.
    loi = chay_voi(mt, [nhan("tb-00001", nhan="DUNG", loai=None, ghi_chu="ngoai_cau_hinh=x; mac_dinh=ngoai_bang,che_do_hien_thi")]
                   + bo_dung()[1:])
    assert len(loi) == 1 and "mac_dinh=che_do_hien_thi" in loi[0]


def test_loi_6_chi_xet_dung_nhom_va_thuoc_tinh_cua_tuyen_bo():
    # Cùng khóa nhưng tuyên bố thuộc nhóm khác, hoặc thuộc tính khác: không phải điều kiện "không có mặc định" ở đó.
    # (Bảng khóa ghi được rút gọn cho phép che_do_hien_thi ở cả ba, để chỉ xét luật "không có mặc định".)
    qt = {"khoa_ghi_duoc": {k: ["che_do_hien_thi"] for k in (("tn", "do_sang"), ("dt", "thoi_luong_pin"), ("dt", "do_sang"))}}
    for ma_mau, thuoc_tinh in (("tn-test", "do_sang"), ("dt-test", "thoi_luong_pin")):
        tb = {"ma_mau": ma_mau, "thuoc_tinh": thuoc_tinh}
        assert kn.kiem_mot_dong(mac_dinh("che_do_hien_thi", dong_d="D3"), tb, None, KHONG_CO, qt) == []
    tb = {"ma_mau": "dt-test", "thuoc_tinh": "do_sang"}
    assert len(kn.kiem_mot_dong(mac_dinh("che_do_hien_thi", dong_d="D3"), tb, None, KHONG_CO, qt)) == 1
    # Tuyên bố không có thuoc_tinh (tệp tuyên bố rút gọn): bỏ qua, không đọc hướng dẫn.
    assert kn.kiem_mot_dong(mac_dinh("che_do_hien_thi", dong_d="D3"), {"ma_mau": "dt-test"}, None) == []


def test_khong_co_mac_dinh_doc_tu_huong_dan_that():
    if not kn.tc.TEP_HUONG_DAN.exists():
        pytest.skip("không có data/huong_dan_gan_nhan.md")
    khoa = kn.khong_co_mac_dinh()
    assert khoa[("dt", "do_sang")] == {"che_do_hien_thi": "Chế độ hiển thị"}
    assert khoa[("dt", "sac_nhanh")] == {"moc_phan_tram": "Mốc phần trăm"}
    assert khoa[("tn", "sac_nhanh")] == {"so_phut_sac": "Số phút sạc"}
    assert ("dt", "thoi_luong_pin") not in khoa and ("tn", "thoi_luong_pin") not in khoa
    # Qua đường mặc định (khong_co=None): độ sáng điện thoại, D3, mac_dinh=che_do_hien_thi -> lỗi.
    tb = {"ma_mau": "dt-apple-iphone17", "thuoc_tinh": "do_sang"}
    loi = kn.kiem_mot_dong(mac_dinh("che_do_hien_thi", dong_d="D3"), tb, None)
    assert len(loi) == 1 and "“Chế độ hiển thị” không có mặc định" in loi[0]
    tb = {"ma_mau": "tn-samsung-buds3pro", "thuoc_tinh": "sac_nhanh"}
    loi = kn.kiem_mot_dong(mac_dinh("so_phut_sac", dong_d="D4", nhan="LECH", loai="bo_dieu_kien"), tb, None)
    assert len(loi) == 1 and "“Số phút sạc” không có mặc định" in loi[0]


def test_nhac_7_bo_dieu_kien_thieu_mac_dinh(mt):
    mau = ("Loại bo_dieu_kien nghĩa là tuyên bố bỏ điều kiện và bạn đã dùng cách hiểu mặc định; "
           "thường cần ghi mac_dinh=… (mục 8).")
    thieu = nhan("tb-00001", nhan="LECH", loai="bo_dieu_kien", ghi_chu="")
    assert kn.nhac_mot_dong(thieu) == [mau]
    assert kn.nhac_mot_dong(dict(thieu, ghi_chu="ngoai_cau_hinh=x")) == [mau]
    assert kn.nhac_mot_dong(dict(thieu, ghi_chu="mac_dinh=")) == [mau]  # mac_dinh trống coi như chưa ghi
    assert kn.nhac_mot_dong(dict(thieu, ghi_chu="mac_dinh=hoat_dong")) == []
    assert kn.nhac_mot_dong(dict(thieu, ghi_chu="ngoai_cau_hinh=x; mac_dinh=che_do_nguon,hoat_dong")) == []
    assert kn.nhac_mot_dong(dict(thieu, loai="doi_dieu_kien")) == []
    # Chỉ nhắc, không phải lỗi: kiem_tep không báo gì.
    loi, dong_nhan, _ = chay(mt, [thieu] + bo_dung()[1:])
    assert loi == [] and kn.nhac_tep(dong_nhan) == [f"tb-00001: {mau}"]


def test_tom_tat_thong_ke_theo_dong_d(mt):
    _, dong_nhan, so_tb = chay(mt, bo_dung())  # D3, D5, D4 và D1b
    chu = "\n".join(kn.tom_tat(dong_nhan, so_tb))
    assert "Dòng D đã dừng ở (dong_d):" in chu
    for d in kn.MA_DONG_D:
        dem = {"D3": 1, "D4": 1, "D5": 1, "D1b": 1}.get(d, 0)
        assert f"  {d:<8} {dem:>3}" in chu, d


def test_lenh_in_muc_nhac_va_van_thoat_ma_0(tmp_path):
    doan_that = ROOT / "data/nguon/dt-apple-iphone17/doan.jsonl"
    if not doan_that.exists():
        pytest.skip("không có data/nguon/dt-apple-iphone17/doan.jsonl")
    d = json.loads(doan_that.read_text(encoding="utf-8").splitlines()[1])
    tb = ghi_jsonl(tmp_path / "thu.jsonl", [{"id": "tb-00001", "ma_mau": "dt-apple-iphone17"}])
    n = ghi_jsonl(tmp_path / "nhan.jsonl", [nhan("tb-00001", nhan="LECH", loai="bo_dieu_kien", bang_chung=[d["id"]],
                                                 trich=d["noi_dung"][:20])])
    kq = chay_lenh({"nhan": n, "tb": tb})
    assert kq.returncode == 0, kq.stdout
    assert "Nhắc (1, không tính là lỗi):" in kq.stdout and "tb-00001: Loại bo_dieu_kien" in kq.stdout
    assert "Không có lỗi." in kq.stdout and "Dòng D đã dừng ở (dong_d):" in kq.stdout


@pytest.mark.parametrize("ly_do, mong", [
    ("Tài liệu của {sản phẩm} không có thông số {thuộc tính}.", ["{sản phẩm}", "{thuộc tính}"]),
    ("Khớp với tài liệu: {trích}.", ["{trích}"]),
    ("Giá trị {} chỉ đạt khi ghi rõ.", ["{}"]),
])
def test_ly_do_con_cho_giu_cho(mt, ly_do, mong):
    loi, _, _ = chay(mt, [nhan("tb-00001", ly_do=ly_do)] + bo_dung()[1:])
    assert len(loi) == 1 and "(tb-00001): Lý do còn chỗ {…} chưa thay" in loi[0], loi
    assert all(m in loi[0] for m in mong)


@pytest.mark.parametrize("ly_do", [
    "Khớp với tài liệu: “Màn hình 1000 nit”.",
    "Tài liệu ghi {1000 nit",  # ngoặc lẻ không phải chỗ giữ chỗ hoàn chỉnh
    "Tài liệu ghi 1000 nit}",
])
def test_ly_do_khong_con_cho_giu_cho(mt, ly_do):
    assert chay(mt, [nhan("tb-00001", ly_do=ly_do)] + bo_dung()[1:])[0] == []


def test_bang_chung(mt):
    dong = bo_dung()
    dong[0] = nhan("tb-00001", nhan="DUNG", loai=None, bang_chung=[], trich="")  # DUNG phải có bằng chứng
    dong[1] = nhan("tb-00002", bang_chung=["dt-test#002", "dt-test#099"])  # mã không có trong doan.jsonl
    dong[2] = nhan("tb-00003", nhan="LECH", loai="bo_dieu_kien", bang_chung=["dt-khac#002"])  # mã của mẫu khác
    chu = "\n".join(chay(mt, dong)[0])
    assert "(tb-00001): bang_chung rỗng" in chu
    assert "mã bằng chứng dt-test#099 không có trong data/nguon/dt-test/doan.jsonl" in chu
    assert "mã bằng chứng dt-khac#002 không có trong" in chu
    assert not any("(tb-00004)" in e for e in chay(mt, dong)[0])  # CHUA_DU không bằng chứng thì được


def test_bang_chung_lap_va_sai_kieu(mt):
    dong = bo_dung()
    dong[1] = nhan("tb-00002", bang_chung=["dt-test#002", "dt-test#002"])
    dong[2] = nhan("tb-00003", nhan="LECH", loai="bo_dieu_kien", bang_chung="dt-test#002")
    chu = "\n".join(chay(mt, dong)[0])
    assert "dt-test#002 lặp 2 lần" in chu
    assert "bang_chung phải là danh sách" in chu


def test_trich_chuan_hoa_nfc_va_khoang_trang(mt):
    dong = bo_dung()
    # NBSP và xuống dòng trong tài liệu khớp dấu cách trong câu trích; câu trích ở dạng NFD vẫn khớp.
    dong[0] = nhan("tb-00001", nhan="DUNG", loai=None, bang_chung=["dt-test#001"],
                   trich=unicodedata.normalize("NFD", "Xem video liên tục Lên đến 30 giờ"))
    # Hai phần tách bằng " | ", phần thứ hai nằm trong một chu_thich (không cần khớp với chú thích kia).
    dong[2] = nhan("tb-00003", nhan="LECH", loai="bo_dieu_kien", bang_chung=["dt-test#002"],
                   trich="Màn hình 1000 nit | Độ sáng đo trong phòng thí nghiệm")
    assert chay(mt, dong)[0] == []


def test_trich_chap_nhan_noi_dung_hien_thi_va_noi_dung_goc(mt):
    def loi_cua(trich, ma="dt-test#004"):
        return chay(mt, [nhan("tb-00001", bang_chung=[ma], trich=trich)] + bo_dung()[1:])[0]
    assert loi_cua("Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W") == []  # chữ hiển thị (noi_dung)
    assert loi_cua("Sạc lên đến 50% trong 20 phút6 với bộ tiếp hợp 40W") == []  # nhãn cũ chép kèm số chú thích (noi_dung_goc)
    assert loi_cua("trong 20 phút với bộ tiếp hợp 40W Bền bỉ | Đo với bộ tiếp hợp 40W") == []  # xuống dòng thành dấu cách
    assert loi_cua("phút6 với bộ tiếp hợp | Đo với bộ tiếp hợp 40W") == []
    # Không phải chuỗi con của noi_dung, noi_dung_goc hay chu_thich nào: vẫn lỗi (kể cả khi chỉ khác ở chỗ ghép hai bản).
    for sai in ["Sạc lên đến 50% trong 20 phút 6 với bộ tiếp hợp", "Sạc lên đến 50% trong 20 phút7 với", "phút6 với bộ tiếp hợp 40W Bền bỉ 7"]:
        assert any("trich không là chuỗi con" in e for e in loi_cua(sai)), sai
    # Đoạn của tệp doan.jsonl cũ (chưa có noi_dung_goc) vẫn kiểm được theo noi_dung.
    assert loi_cua("Màn hình 1000 nit", "dt-test#002") == []
    assert kn.doc_doan("dt-test", mt["nguon"])["dt-test#002"][1] == "Màn hình 1000 nit"
    assert kn.doc_doan("dt-test", mt["nguon"])["dt-test#004"][1].startswith("Sạc lên đến 50% trong 20 phút6 với")


def test_trich_sai(mt):
    dong = bo_dung()
    dong[0] = nhan("tb-00001", nhan="DUNG", loai=None, bang_chung=["dt-test#001"], trich="Lên đến 3000 giờ")
    dong[1] = nhan("tb-00002", trich="Màn hình 1000 nit | Chống nước IP68")  # phần 2 thuộc đoạn không được chọn
    dong[2] = nhan("tb-00003", nhan="LECH", loai="bo_dieu_kien", trich="Màn hình 1000 nit |  | ")  # phần rỗng
    dong[3] = nhan("tb-00004", nhan="CHUA_DU", loai=None, bang_chung=[], trich="có chữ nhưng không bằng chứng")
    loi = chay(mt, dong)[0]
    chu = "\n".join(loi)
    assert "(tb-00001): trich không là chuỗi con" in chu and "3000 giờ" in chu
    assert "(tb-00002): trich không là chuỗi con" in chu and "Chống nước IP68" in chu
    assert "(tb-00003): trich có phần rỗng" in chu
    assert "(tb-00004): trich có nội dung nhưng bang_chung rỗng" in chu
    assert len(loi) == 4
    # Có bằng chứng mà trích rỗng.
    loi = chay(mt, [nhan("tb-00001", trich="  ")] + bo_dung()[1:])[0]
    assert any("có bang_chung nhưng trich rỗng" in e for e in loi)


@pytest.mark.parametrize("sua, mong", [
    ({"giay": 0}, "giay phải là số nguyên dương"),
    ({"giay": -5}, "giay phải là số nguyên dương"),
    ({"giay": 12.5}, "giay phải là số nguyên dương"),
    ({"giay": "40"}, "giay phải là số nguyên dương"),
    ({"giay": True}, "giay phải là số nguyên dương"),
    ({"ly_do": "  "}, "ly_do phải là chuỗi không rỗng"),
    ({"nguoi_gan": ""}, "nguoi_gan phải là chuỗi không rỗng"),
    ({"tai_lieu_mau_thuan": "false"}, "tai_lieu_mau_thuan phải là true/false"),
    ({"tai_lieu_mau_thuan": 0}, "tai_lieu_mau_thuan phải là true/false"),
    ({"luot": 0}, "luot phải là số nguyên dương"),
])
def test_kieu_va_gia_tri_truong(mt, sua, mong):
    loi, _, _ = chay(mt, [nhan("tb-00001", **sua)] + bo_dung()[1:])
    assert len(loi) == 1 and mong in loi[0], loi


def test_thieu_truong_va_truong_la(mt):
    sai = nhan("tb-00001")
    del sai["ly_do"]
    sai["gia_dinh"] = 1
    loi = chay(mt, [sai] + bo_dung()[1:])[0]
    assert any("thiếu trường: ly_do" in e for e in loi) and any("trường lạ: gia_dinh" in e for e in loi)


def test_dong_hong_va_dong_trong(mt):
    mt["nhan"].write_text("{không phải json\n\n[1, 2]\n" + json.dumps(nhan("tb-00001")) + "\n", encoding="utf-8")
    loi, dong_nhan, _ = kn.kiem_tep(mt["nhan"], mt["tb"], mt["nguon"])
    assert len(dong_nhan) == 1
    assert any(e.startswith("dòng 1: không phải JSON") for e in loi)
    assert any(e.startswith("dòng 3: mỗi dòng phải là một đối tượng") for e in loi)


def test_mau_chua_co_doan_jsonl(tmp_path):
    tb = ghi_jsonl(tmp_path / "thu.jsonl", [{"id": "tb-00001", "ma_mau": "khong-co"}])
    n = ghi_jsonl(tmp_path / "nhan.jsonl", [nhan("tb-00001")])
    loi, _, _ = kn.kiem_tep(n, tb, tmp_path / "nguon")
    assert len(loi) == 1 and "không có data/nguon/khong-co/doan.jsonl" in loi[0]


def test_chuan_hoa():
    assert kn.chuan_hoa("  a  b\n\tc　d  ") == "a b c d"
    assert kn.chuan_hoa(unicodedata.normalize("NFD", "Điện thoại")) == "Điện thoại"


def test_dung_doan_that_cua_iphone17(tmp_path):
    doan_that = ROOT / "data/nguon/dt-apple-iphone17/doan.jsonl"
    if not doan_that.exists():
        pytest.skip("không có data/nguon/dt-apple-iphone17/doan.jsonl")
    d = json.loads(doan_that.read_text(encoding="utf-8").splitlines()[1])
    trich = " ".join(d["noi_dung"].split("\n")[:3])  # dòng bị gộp thành dấu cách, vẫn khớp sau chuẩn hóa
    tb = ghi_jsonl(tmp_path / "thu.jsonl", [{"id": "tb-00001", "ma_mau": "dt-apple-iphone17"}])
    n = ghi_jsonl(tmp_path / "nhan.jsonl", [nhan("tb-00001", bang_chung=[d["id"]], trich=trich)])
    assert kn.kiem_tep(n, tb)[0] == []
    n = ghi_jsonl(tmp_path / "nhan.jsonl", [nhan("tb-00001", bang_chung=[d["id"]], trich=trich + " không có thật")])
    assert any("trich không là chuỗi con" in e for e in kn.kiem_tep(n, tb)[0])


def chay_lenh(mt):
    return subprocess.run([sys.executable, str(ROOT / "scripts/kiem_nhan.py"), str(mt["nhan"]), str(mt["tb"])],
                          capture_output=True, text=True, encoding="utf-8", cwd=mt["nhan"].parent,
                          env={**os.environ, "PYTHONIOENCODING": "utf-8"})


def test_lenh_thoat_ma_1_khi_co_loi(mt):
    # Dòng lệnh dùng data/nguon thật nên không thấy mẫu dt-test; không ảnh hưởng điều cần kiểm ở đây.
    ghi_jsonl(mt["nhan"], bo_dung()[:3])
    kq = chay_lenh(mt)
    assert kq.returncode == 1
    assert "thiếu nhãn cho tb-00004" in kq.stdout and "Có " in kq.stdout


def test_lenh_thoat_ma_0_khi_hop_le(tmp_path):
    doan_that = ROOT / "data/nguon/dt-apple-iphone17/doan.jsonl"
    if not doan_that.exists():
        pytest.skip("không có data/nguon/dt-apple-iphone17/doan.jsonl")
    d = json.loads(doan_that.read_text(encoding="utf-8").splitlines()[1])
    tb = ghi_jsonl(tmp_path / "thu.jsonl", [{"id": "tb-00001", "ma_mau": "dt-apple-iphone17"}])
    n = ghi_jsonl(tmp_path / "nhan.jsonl", [nhan("tb-00001", bang_chung=[d["id"]], trich=d["noi_dung"][:20])])
    kq = chay_lenh({"nhan": n, "tb": tb})
    assert kq.returncode == 0, kq.stdout
    assert "Không có lỗi." in kq.stdout


# ---------- Bước 16: luật của hướng dẫn bản 2 (S14, S15, S17-S21) ----------

# Bản rút gọn của các bảng đọc từ hướng dẫn (quy_tac_huong_dan() đọc bản thật), cho tuyên bố dt-test / do_sang.
QUY_TAC = {
    "co_mac_dinh": {("dt", "do_sang"): {"dien_tich_do": {"dieu_kien": "Phần diện tích đo", "hieu": "Như hãng công bố cho chế độ đó"}}},
    # Bản rút gọn: các test dùng bảng này nhắm luật khác, nên mọi khóa xuất hiện trong ghi chú của chúng đều ghi được.
    "khoa_ghi_duoc": {("dt", "do_sang"): ["che_do_hien_thi", "dien_tich_do", "che_do_nguon", "a"], ("dt", "thoi_luong_pin"): ["hoat_dong"]},
    "tu_hop_le": ["luôn", "đảm bảo", "bảo đảm", "ít nhất", "mọi lúc", "hơn", "trên", "không dưới", "trở lên"],
    "ds_tu": "luôn, đảm bảo, bảo đảm, ít nhất, mọi lúc, hơn, trên, không dưới, trở lên",
    "don_vi": {("dt", "do_sang"): {"don_vi": "nit", "re": re.compile(kn.tc.mau_don_vi("nit", "thử"))}},
}


def chay_qt(mt, dong, luot=None):
    """Lỗi khi kiểm với bản rút gọn của KHONG_CO và QUY_TAC."""
    ghi_jsonl(mt["nhan"], dong)
    return kn.kiem_tep(mt["nhan"], mt["tb"], mt["nguon"], KHONG_CO, QUY_TAC, luot)[0]


def d2(ghi_chu, **kw):
    return nhan("tb-00001", nhan="LECH", dong_d="D2", loai="doi_kieu_gia_tri", ghi_chu=ghi_chu, **kw)


def d1a(ghi_chu, **kw):
    return nhan("tb-00001", nhan="CHUA_DU", dong_d="D1a", loai=None, ghi_chu=ghi_chu, **kw)


@pytest.mark.parametrize("ly_do, ma", [
    ("Khớp với tài liệu: “dt-apple-iphone17#016”.", "dt-apple-iphone17#016"),
    ('Khớp với tài liệu: "tn-samsung-buds3pro#038".', "tn-samsung-buds3pro#038"),
    ("Tài liệu ghi “Lên đến 30 giờ” và “dh-apple-watchse3#008”; 7 giờ chỉ đạt khi tắt chống ồn. Nguồn: “dt-x-y#1”.", "dh-apple-watchse3#008"),
    ("Nguồn: “Thời gian xem video lên đến 30 giờ (dt-apple-iphone17#016)”.", "dt-apple-iphone17#016"),
])
def test_s14_ly_do_chep_ma_doan_vao_cho_cau_trich(mt, ly_do, ma):
    loi = chay_qt(mt, [nhan("tb-00001", ly_do=ly_do)] + bo_dung()[1:])
    assert loi == ["dòng 1 (tb-00001): " + kn.THONG_BAO["ly_do_ma_doan"].format(ma=ma)], loi
    assert "Lý do chép mã đoạn thay cho câu trích" in loi[0]


@pytest.mark.parametrize("ly_do", [
    "Khớp với tài liệu: “Màn hình 1000 nit”.",
    "Mã đoạn dt-apple-iphone17#016 nằm ngoài ngoặc kép.",   # chỉ bắt mã đoạn trong ngoặc kép (S14)
    "Khớp “giá trị #1” và “tập dev-1”.",                     # có dấu # nhưng không phải <ma_mau>#<số>
    "Không có ngoặc kép nào.",
])
def test_s14_ly_do_khong_chep_ma_doan(mt, ly_do):
    assert chay_qt(mt, [nhan("tb-00001", ly_do=ly_do)] + bo_dung()[1:]) == []


def test_s14_tren_nhan_luot_1_that():
    nhan_1, tb = ROOT / "data/nhan/thu_luot1.jsonl", ROOT / "data/tuyen_bo/thu.jsonl"
    if not (nhan_1.exists() and tb.exists() and kn.tc.TEP_HUONG_DAN.exists()):
        pytest.skip("không có nhãn lượt 1")
    loi, dong_nhan, so_tb = kn.kiem_tep(nhan_1, tb)
    assert so_tb == len(dong_nhan) == 66
    # Lượt 1 viết theo hướng dẫn bản 1: 31 lý do chép mã đoạn vào chỗ câu trích (B11 trong cau_hoi_nhan_luot1.md).
    assert sum("Lý do chép mã đoạn thay cho câu trích" in e for e in loi) == 31


def test_s15_nhac_cau_trich_khong_co_don_vi(mt):
    tb = {"id": "tb-00001", "ma_mau": "dt-test", "thuoc_tinh": "do_sang"}
    mau = ("Câu trích không có đơn vị của thuộc tính do_sang (nit): kiểm lại xem bằng chứng có đúng thuộc tính của tuyên bố không.")
    assert kn.NHAC["trich_thieu_don_vi"].format(thuoc_tinh="do_sang", don_vi="nit") == mau
    ok = nhan("tb-00001", trich="Màn hình 1000 nit")
    assert kn.nhac_mot_dong(ok, tb, QUY_TAC) == []
    assert kn.nhac_mot_dong(dict(ok, trich="Màn hình 1000 NITS"), tb, QUY_TAC) == []     # hoa thường, nits
    assert kn.nhac_mot_dong(dict(ok, trich="độ sáng 3.000 cd/m²"), tb, QUY_TAC) == []
    lech = dict(ok, trich="Công nghệ ProMotion thích ứng lên đến 120Hz")                    # lưu lệch sang tuyên bố kế bên
    assert kn.nhac_mot_dong(lech, tb, QUY_TAC) == [mau]
    assert kn.nhac_mot_dong(dict(ok, trich="Màn hình 1000 | Lên đến 120Hz"), tb, QUY_TAC) == [mau]
    assert kn.nhac_mot_dong(dict(ok, trich="Luminit 5"), tb, QUY_TAC) == [mau]         # "nit" nằm giữa chữ thì không tính
    assert kn.nhac_mot_dong(dict(ok, trich="   "), tb, QUY_TAC) == []                      # trống: D1, không có gì để kiểm
    assert kn.nhac_mot_dong(lech, None, QUY_TAC) == [] and kn.nhac_mot_dong(lech) == []   # không biết thuộc tính thì thôi
    assert kn.nhac_mot_dong(lech, {"ma_mau": "dt-test", "thuoc_tinh": "zoom"}, QUY_TAC) == []   # thuộc tính chưa có đơn vị
    # Chỉ nhắc, không phải lỗi, và kiem_tep không đổi; nhac_tep gắn mã tuyên bố.
    ghi_jsonl(mt["nhan"], [nhan("tb-00001", bang_chung=["dt-test#001"], trich="Lên đến 30 giờ")] + bo_dung()[1:])
    loi, dong_nhan, _ = kn.kiem_tep(mt["nhan"], mt["tb"], mt["nguon"], KHONG_CO, QUY_TAC)
    assert loi == []
    tuyen_bo = kn.doc_tuyen_bo(mt["tb"])
    nhac = kn.nhac_tep(dong_nhan, tuyen_bo, QUY_TAC)
    assert nhac[0] == f"tb-00001: {mau}"


def test_s15_don_vi_doc_tu_huong_dan_that():
    if not kn.tc.TEP_HUONG_DAN.exists():
        pytest.skip("không có data/huong_dan_gan_nhan.md")
    tb = {"id": "tb-00001", "ma_mau": "dt-apple-iphone17", "thuoc_tinh": "do_sang"}
    assert kn.nhac_mot_dong(nhan("tb-00001", trich="Độ sáng tối đa 1000 nit (tiêu chuẩn)"), tb) == []
    nhac = kn.nhac_mot_dong(nhan("tb-00001", trich="Công nghệ ProMotion thích ứng lên đến 120Hz"), tb)
    assert nhac == [kn.NHAC["trich_thieu_don_vi"].format(thuoc_tinh="do_sang", don_vi="nit")]
    tb = {"id": "tb-00002", "ma_mau": "dt-apple-iphone17", "thuoc_tinh": "khang_nuoc"}
    assert kn.nhac_mot_dong(nhan("tb-00002", trich="Đạt mức IP68 (chống nước ở độ sâu tối đa 6 mét)"), tb) == []
    assert len(kn.nhac_mot_dong(nhan("tb-00002", trich="Độ sáng đỉnh 3000 nit"), tb)) == 1


def test_s17_d2_phai_ghi_khang_dinh_co_trong_muc_6_2(mt):
    thieu = kn.THONG_BAO["d2_thieu_khang_dinh"].format(ds=QUY_TAC["ds_tu"])
    assert thieu == ("Dòng D2 phải ghi từ khẳng định vào ghi chú: khang_dinh=<từ>, với <từ> là một trong: "
                     "luôn, đảm bảo, bảo đảm, ít nhất, mọi lúc, hơn, trên, không dưới, trở lên.")
    for ghi_chu in ("", "mac_dinh=dien_tich_do", "khang_dinh=", "ngoai_cau_hinh=x; khang_dinh="):
        assert chay_qt(mt, [d2(ghi_chu)] + bo_dung()[1:]) == [f"dòng 1 (tb-00001): {thieu}"], ghi_chu
    la = chay_qt(mt, [d2("khang_dinh=rất")] + bo_dung()[1:])
    assert la == ["dòng 1 (tb-00001): " + kn.THONG_BAO["d2_khang_dinh_la"].format(tu="rất", ds=QUY_TAC["ds_tu"])]
    assert "“rất” không có trong danh sách từ khẳng định ở mục 6.2" in la[0]
    # Từ hợp lệ: đúng chữ ở mục 6.2 (hoa thường, khoảng trắng không quan trọng); mức sàn ghi từ, không ghi cả "hơn 16 giờ".
    for ghi_chu in ("khang_dinh=luôn", "khang_dinh=Luôn", "khang_dinh=hơn; mac_dinh=che_do_nguon", "khang_dinh=ít  nhất",
                    "mac_dinh=a; khang_dinh=trở lên", "khang_dinh=luôn, đảm bảo"):
        assert chay_qt(mt, [d2(ghi_chu)] + bo_dung()[1:]) == [], ghi_chu
    loi = chay_qt(mt, [d2("khang_dinh=hơn 16 giờ")] + bo_dung()[1:])
    assert len(loi) == 1 and "khang_dinh=hơn 16 giờ" in loi[0]
    loi = chay_qt(mt, [d2("khang_dinh=luôn, rất, rất")] + bo_dung()[1:])  # từ lạ lặp lại chỉ báo một lần
    assert len(loi) == 1 and "khang_dinh=rất" in loi[0]
    # Chỉ D2 bị buộc; dòng khác không cần khang_dinh.
    assert chay_qt(mt, [nhan("tb-00001", nhan="LECH", dong_d="D4", loai="doi_dieu_kien")] + bo_dung()[1:]) == []


def test_s17_d2_doc_tu_huong_dan_that():
    if not kn.tc.TEP_HUONG_DAN.exists():
        pytest.skip("không có data/huong_dan_gan_nhan.md")
    tb = {"ma_mau": "dt-apple-iphone17", "thuoc_tinh": "tan_so_quet"}
    d = d2("khang_dinh=luôn")
    assert kn.kiem_mot_dong(d, tb, None) == []
    assert kn.kiem_mot_dong(d2("khang_dinh=hơn"), tb, None) == []    # V50: khang_dinh=hơn
    assert len(kn.kiem_mot_dong(d2(""), tb, None)) == 1 and len(kn.kiem_mot_dong(d2("khang_dinh=tối thiểu"), tb, None)) == 1


def test_s18_d1a_phai_ghi_nguyen_nhan(mt):
    thieu = kn.THONG_BAO["d1a_thieu_nguyen_nhan"].format(ds="che_do_hien_thi")
    assert thieu == ("Dòng D1a phải ghi nguyên nhân vào ghi chú: mac_dinh=<khóa “Không có mặc định” của thuộc tính này: "
                     "che_do_hien_thi> hoặc chua_xac_dinh=<cụm>.")
    assert chay_qt(mt, [d1a("")] + bo_dung()[1:]) == [f"dòng 1 (tb-00001): {thieu}"]
    # Đủ nguyên nhân: khóa "không có mặc định" (kể cả kèm khóa có mặc định, V46), hoặc chua_xac_dinh (V47).
    for ghi_chu in ("mac_dinh=che_do_hien_thi", "mac_dinh=dien_tich_do,che_do_hien_thi", "chua_xac_dinh=đỉnh",
                    "mac_dinh=dien_tich_do; chua_xac_dinh=toàn màn hình", "mac_dinh=che_do_hien_thi; chua_xac_dinh=đỉnh"):
        assert chay_qt(mt, [d1a(ghi_chu)] + bo_dung()[1:]) == [], ghi_chu
    # Chỉ ghi khóa có cách hiểu mặc định thì sai: dùng mặc định rồi dò tiếp (chiều ngược của mac_dinh_khong_co).
    loi = chay_qt(mt, [d1a("mac_dinh=dien_tich_do")] + bo_dung()[1:])
    assert loi == [f"dòng 1 (tb-00001): {thieu}",
                   "dòng 1 (tb-00001): Ghi chú có mac_dinh=dien_tich_do, mà “Phần diện tích đo” có cách hiểu mặc định “Như hãng công bố "
                   "cho chế độ đó”: dùng mặc định rồi dò tiếp, không dừng ở D1a vì khóa này."]
    # chua_xac_dinh trống hoặc mac_dinh trống không tính là nguyên nhân; khóa lạ cũng không.
    for ghi_chu in ("chua_xac_dinh=", "chua_xac_dinh=  ; mac_dinh=", "mac_dinh=khoa_la", "ngoai_cau_hinh=x"):
        loi = chay_qt(mt, [d1a(ghi_chu)] + bo_dung()[1:])
        # khoa_la còn bị báo riêng là khóa không ghi được (rà soát 02/11).
        assert len(loi) == (2 if "khoa_la" in ghi_chu else 1) and "phải ghi nguyên nhân" in loi[-1], (ghi_chu, loi)


def test_s18_d1a_thuoc_tinh_khong_co_khoa_khong_co_mac_dinh(mt):
    # Thuộc tính không có khóa "Không có mặc định": chỉ chua_xac_dinh mới là nguyên nhân.
    tb = {"ma_mau": "dt-test", "thuoc_tinh": "thoi_luong_pin"}
    loi = kn.kiem_mot_dong(d1a("mac_dinh=hoat_dong"), tb, None, KHONG_CO, QUY_TAC)
    assert len(loi) == 1 and "(thuộc tính này không có khóa nào)" in loi[0], loi
    assert kn.kiem_mot_dong(d1a("chua_xac_dinh=liên tục"), tb, None, KHONG_CO, QUY_TAC) == []
    # Tuyên bố không có thuoc_tinh (tệp tuyên bố rút gọn): không biết khóa nào, bỏ qua, không đọc hướng dẫn.
    assert kn.kiem_mot_dong(d1a(""), {"ma_mau": "dt-test"}, None) == []


def test_s18_d1a_doc_tu_huong_dan_that():
    if not kn.tc.TEP_HUONG_DAN.exists():
        pytest.skip("không có data/huong_dan_gan_nhan.md")
    tb = {"ma_mau": "dt-apple-iphone17", "thuoc_tinh": "sac_nhanh"}
    assert len(kn.kiem_mot_dong(d1a(""), tb, None)) == 1
    assert kn.kiem_mot_dong(d1a("mac_dinh=moc_phan_tram,cach_sac"), tb, None) == []         # V46
    loi = kn.kiem_mot_dong(d1a("mac_dinh=cach_sac"), tb, None)
    assert len(loi) == 2 and "mac_dinh=cach_sac" in loi[1] and "Sạc bằng cáp" in loi[1]


def test_s19_d1_co_mac_dinh_chi_nhac(mt):
    d1 = nhan("tb-00001", nhan="CHUA_DU", dong_d="D1", loai=None, bang_chung=[], trich="", ghi_chu="mac_dinh=hoat_dong")
    assert kn.NHAC["d1_co_mac_dinh"] == "Dòng D1 dừng trước khi xét điều kiện, nên không cần ghi mac_dinh=… (mục 8)."
    assert kn.nhac_mot_dong(d1) == [kn.NHAC["d1_co_mac_dinh"]]
    assert kn.nhac_mot_dong(dict(d1, ghi_chu="")) == [] and kn.nhac_mot_dong(dict(d1, ghi_chu="mac_dinh=")) == []
    assert kn.nhac_mot_dong(dict(d1, dong_d="D6", bang_chung=["dt-test#001"], trich="Màn hình 1000 nit")) == []
    assert chay_qt(mt, [d1] + bo_dung()[1:]) == []     # chỉ nhắc, không phải lỗi
    # kể cả khóa "không có mặc định": ở D1 không báo lỗi "phải dừng ở D1a".
    assert chay_qt(mt, [dict(d1, ghi_chu="mac_dinh=che_do_hien_thi")] + bo_dung()[1:]) == []


def test_s20_luot_mac_dinh_doc_tu_ban_ghi_va_tham_so_luot(mt):
    dong = [dict(nh, luot=2) for nh in bo_dung()]
    ghi_jsonl(mt["nhan"], dong)
    loi, dong_nhan, _ = kn.kiem_tep(mt["nhan"], mt["tb"], mt["nguon"], KHONG_CO, QUY_TAC)
    assert loi == [] and "Lượt gán (luot): 2" in "\n".join(kn.tom_tat(dong_nhan, 4))
    assert kn.kiem_tep(mt["nhan"], mt["tb"], mt["nguon"], KHONG_CO, QUY_TAC, 2)[0] == []
    loi = kn.kiem_tep(mt["nhan"], mt["tb"], mt["nguon"], KHONG_CO, QUY_TAC, 1)[0]
    assert len(loi) == 4 and all("luot là 2, khác lượt 1 đang kiểm" in e for e in loi), loi
    # Không truyền lượt mà tệp trộn hai lượt: một lỗi nêu các lượt.
    ghi_jsonl(mt["nhan"], [dict(dong[0], luot=1)] + dong[1:])
    loi = kn.kiem_tep(mt["nhan"], mt["tb"], mt["nguon"], KHONG_CO, QUY_TAC)[0]
    assert loi == ["các dòng nhãn thuộc nhiều lượt khác nhau (luot: 1, 2); một tệp chỉ chứa một lượt, hoặc truyền --luot"], loi
    assert "Lượt gán (luot): 1, 2" in "\n".join(kn.tom_tat([dict(dong[0], luot=1), dong[1]], 4))


def test_s20_lenh_luot(tmp_path):
    doan_that = ROOT / "data/nguon/dt-apple-iphone17/doan.jsonl"
    if not doan_that.exists():
        pytest.skip("không có data/nguon/dt-apple-iphone17/doan.jsonl")
    d = json.loads(doan_that.read_text(encoding="utf-8").splitlines()[1])
    tb = ghi_jsonl(tmp_path / "thu.jsonl", [{"id": "tb-00001", "ma_mau": "dt-apple-iphone17"}])
    n = ghi_jsonl(tmp_path / "nhan.jsonl", [nhan("tb-00001", bang_chung=[d["id"]], trich=d["noi_dung"][:20], luot=2)])

    def lenh(*them):
        return subprocess.run([sys.executable, str(ROOT / "scripts/kiem_nhan.py"), str(n), str(tb), *them], capture_output=True,
                              text=True, encoding="utf-8", cwd=tmp_path, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    kq = lenh()
    assert kq.returncode == 0 and "Lượt gán (luot): 2" in kq.stdout, kq.stdout
    assert lenh("--luot", "2").returncode == 0
    kq = lenh("--luot", "1")
    assert kq.returncode == 1 and "luot là 2, khác lượt 1 đang kiểm" in kq.stdout


def test_s21_giay_nghi_tuy_chon(mt):
    dong = bo_dung()
    assert "giay_nghi" in kn.TRUONG_TUY_CHON and "giay_nghi" not in kn.TRUONG   # không bắt buộc: lượt 1 không có trường này
    assert chay(mt, dong)[0] == []
    for gia_tri in (0, 7, 420):
        assert chay(mt, [dict(dong[0], giay_nghi=gia_tri)] + dong[1:])[0] == [], gia_tri
    for gia_tri in (-1, 2.5, "7", True, None):
        loi = chay(mt, [dict(dong[0], giay_nghi=gia_tri)] + dong[1:])[0]
        assert len(loi) == 1 and "giay_nghi phải là số nguyên không âm" in loi[0], (gia_tri, loi)
    loi = chay(mt, [dict(dong[0], giay_la=3)] + dong[1:])[0]
    assert len(loi) == 1 and "trường lạ: giay_la" in loi[0]
    _, dong_nhan, so_tb = chay(mt, [dict(dong[0], giay_nghi=300), dict(dong[1], giay_nghi=0)] + dong[2:])
    chu = "\n".join(kn.tom_tat(dong_nhan, so_tb))
    assert "Đồng hồ đứng vì không thao tác (giay_nghi, không nằm trong giay): tổng 300 giây (5 phút 0 giây) ở 1 tuyên bố" in chu
    assert "giay_nghi" not in "\n".join(kn.tom_tat(bo_dung(), 4))   # không có trường thì không in dòng này


def test_mac_dinh_chi_nhan_khoa_ghi_duoc_cua_thuoc_tinh():
    # Rà soát 02/11 (lỗi 3): khóa của mac_dinh= phải là khóa bảng mục 5 của nhóm và thuộc tính, trừ "như hãng công bố";
    # ngoai_bang (mục 6.7 ý 4, QĐ10) ghi được ở mọi thuộc tính; D1 không bị báo (chỉ nhắc S19).
    if not kn.tc.TEP_HUONG_DAN.exists():
        pytest.skip("không có data/huong_dan_gan_nhan.md")
    tb = {"ma_mau": "dt-apple-iphone17", "thuoc_tinh": "sac_nhanh"}
    ok = nhan("tb-00001", nhan="LECH", dong_d="D4", loai="bo_dieu_kien", ghi_chu="mac_dinh=bo_tiep_hop,cach_sac")
    assert kn.kiem_mot_dong(ok, tb, None) == []
    for khoa in ("bo_tiep_hop, ngoai_bang", "ngoai_bang"):
        assert kn.kiem_mot_dong(nhan("tb-00001", nhan="DUNG", loai=None, ghi_chu=f"mac_dinh={khoa}"), tb, None) == [], khoa
    for khoa in ("bo_tiep_hp", "che_do_hien_thi", "hoat_dong"):  # gõ sai; khóa của thuộc tính khác
        loi = kn.kiem_mot_dong(nhan("tb-00001", nhan="DUNG", loai=None, ghi_chu=f"mac_dinh={khoa}"), tb, None)
        assert len(loi) == 1 and f"mac_dinh={khoa}" in loi[0] and "không phải khóa ghi được" in loi[0], khoa
    tb = {"ma_mau": "dt-apple-iphone17", "thuoc_tinh": "do_sang"}  # dien_tich_do: "như hãng công bố", không ghi
    loi = kn.kiem_mot_dong(nhan("tb-00001", nhan="DUNG", loai=None, ghi_chu="mac_dinh=dien_tich_do"), tb, None)
    assert len(loi) == 1 and "như hãng công bố" in loi[0]
    d1 = nhan("tb-00001", nhan="CHUA_DU", dong_d="D1", loai=None, bang_chung=[], trich="", ghi_chu="mac_dinh=xyz")
    assert kn.kiem_mot_dong(d1, tb, None) == []
