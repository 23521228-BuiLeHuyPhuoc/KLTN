import importlib.util
import json
from pathlib import Path

import pytest

from kiemchung import chia_doan as cd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("kiem_bo_so_chu_thich", ROOT / "scripts/kiem_bo_so_chu_thich.py")
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)


def tu_danh_dau(chu, loai=cd.KY_HIEU_SO, thieu=False):
    """(văn bản gốc, dòng nhật ký) từ chuỗi có ⟦ký hiệu⟧ đánh dấu chỗ đã bỏ, như trong báo cáo."""
    a, b = chu.index("⟦"), chu.index("⟧")
    ky = chu[a + 1:b]
    so = [int(x) for x in ky.replace(" ", "").split(",")] if loai == cd.KY_HIEU_SO else []
    x = {"vi_tri": a, "vi_tri_moi": a, "chu": ky, "loai": loai, "so": so, "thieu": so if thieu else [], "xu_ly": ""}
    return chu[:a] + ky + chu[b + 1:], x


def test_ngu_canh_danh_dau_cho_xoa_va_xuong_dong():
    goc = "Pin dùng cả ngày\nLên đến 32 giờ ở Chế Độ Nguồn Điện Thấp8\nSạc nhanh hơn trong 45 phút nữa"
    a = goc.index("8")
    ngu = kb.ngu_canh(goc, a, a + 1)
    assert ngu.startswith("…") and ngu.endswith("…") and "Điện Thấp⟦8⟧⏎Sạc nhanh hơn" in ngu and "\n" not in ngu
    assert kb.ngu_canh("Thấp8", 4, 5) == "Thấp⟦8⟧"  # đủ ngắn thì không có dấu …
    assert kb.ngu_canh("Thấp8", 5, 5) == "Thấp8⟦⟧"  # chỗ chèn rỗng (ca chèn khoảng trắng)


@pytest.mark.parametrize("chu, mong", [
    ("Mức IP6⟦8⟧ chống nước", ["truoc_hoa_hoac_so"]),
    ("Chip MIMO⟦8⟧\nLTE", ["truoc_hoa_hoac_so"]),
    ("thế hệ thứ 2⟦10⟧\nNFC", ["truoc_hoa_hoac_so"]),
    ("Sạc lên đến 50% trong 20 phút⟦6⟧ với bộ", []),
    ("Pin dùng 18 giờ khi sử dụng bình thường⟦8⟧\nMàu", []),
    ("Pin ⟦8⟧ giờ", ["sau_la_don_vi"]),
    ("Lên đến ⟦7⟧ giờ", ["sau_la_don_vi"]),
    ("tai nghe ⟦5⟧W", ["sau_la_don_vi"]),
    ("Dài ⟦6⟧ mét", []),  # 'mét' không phải đơn vị trong danh sách (m, mm... đứng riêng)
])
def test_ma_nghi_ngo_cua_ky_hieu_so(chu, mong):
    goc, x = tu_danh_dau(chu)
    assert kb.ma_nghi_ngo(goc, x) == mong


def test_ma_nghi_ngo_so_khong_co_chu_thich_va_dau_sao():
    goc, x = tu_danh_dau("ngày dài đầy năng lượng! ⟦7⟧", thieu=True)
    assert kb.ma_nghi_ngo(goc, x) == ["khong_co_chu_thich"]
    goc, x = tu_danh_dau("Đánh giá 5⟦*⟧ cho sản phẩm", cd.KY_HIEU_SAO)
    assert kb.ma_nghi_ngo(goc, x) == ["sao_sau_so_le"]
    goc, x = tu_danh_dau("Chống nước IP68⟦*⟧ hàng đầu", cd.KY_HIEU_SAO)
    assert kb.ma_nghi_ngo(goc, x) == []
    goc, x = tu_danh_dau("Trọng lượng: 194g⟦*⟧", cd.KY_HIEU_SAO_NOI_LIEN)
    assert kb.ma_nghi_ngo(goc, x) == []


def test_tim_con_sot_chu_thuong_ngoac_phan_tram_va_danh_sach():
    nd = "Sạc 50% trong 30 phút6 với bộ\nChống nước (50m)14\nđạt 98%2\nbơi14,15 lần\nGalaxy Buds3 Pro\n4x4 MIMO\nIP68 và Wi-Fi 6"
    tim = [nd[a:b] for a, b in kb.tim_con_sot(nd)]
    assert "t6" in tim and ")14" in tim and "%2" in tim and "i14,15" in tim and "s3" in tim and "x4" in tim
    assert not any("P68" in t or "i 6" in t for t in tim)  # chữ hoa và số sau khoảng trắng không thuộc regex này
    assert kb.tim_con_sot("Không có số nào ở đây, chỉ có 120Hz và 5 giờ") == []


def test_tim_ma_hoa_con_lai_chi_lay_so_da_bo_o_cho_khac():
    nd = "Nhận dạng giọng nói AI\nPhiên dịch AI10\nTìm kiếm AI10\nGalaxy S25 Ultra\nChip A19\nQi2"
    assert [nd[a:b] for a, b in kb.tim_ma_hoa_con_lai(nd, {10})] == ["AI10", "AI10"]
    assert [nd[a:b] for a, b in kb.tim_ma_hoa_con_lai(nd, {19, 2})] == ["A19"]  # Qi2 có chữ thường trước số: thuộc regex 5.1
    assert kb.tim_ma_hoa_con_lai(nd, set()) == []


def test_tim_sao_con_lai():
    nd = "Lên đến 30 giờ (*Bật AOD)\nChú thích * biểu tượng\nIP68"
    assert [nd[a:b] for a, b in kb.tim_sao_con_lai(nd)] == ["*", "*"]


def test_code_markdown_an_toan_voi_dau_huyen():
    assert kb.code("a b") == "`a b`"
    assert kb.code("co ` dau") == "`` co ` dau ``"


def test_kiem_bat_bien_dat_va_bat_duoc_noi_dung_bi_sua():
    goc, x = tu_danh_dau("Pin\nLên đến 32 giờ ở Chế Độ Nguồn Điện Thấp⟦8⟧")
    doan = [{"id": "m#001", "noi_dung": "Pin\nLên đến 32 giờ ở Chế Độ Nguồn Điện Thấp", "noi_dung_goc": goc, "muc": "Pin"}]
    nk = [[x]]
    cu = [{"id": "m#001", "muc": "Pin", "noi_dung": goc}]
    assert kb.kiem_bat_bien("m", doan, nk, cu) == ([], [])
    # noi_dung bị đổi chữ khác ngoài ký hiệu
    sai = [dict(doan[0], noi_dung="Pin\nLên đến 33 giờ ở Chế Độ Nguồn Điện Thấp")]
    assert any("không ra noi_dung" in e for e in kb.kiem_bat_bien("m", sai, nk)[1])
    # noi_dung_goc không còn bằng noi_dung cũ, và trường khác đổi
    sai = [dict(doan[0], noi_dung_goc=goc + " ", muc="Khác")]
    loi_cu, _ = kb.kiem_bat_bien("m", sai, nk, cu)
    assert any("noi_dung_goc khác noi_dung cũ" in e for e in loi_cu) and any("trường muc đổi" in e for e in loi_cu)
    # đoạn không có ký hiệu nào bị bỏ mà noi_dung vẫn khác noi_dung_goc
    assert any("không có ký hiệu bị bỏ" in e for e in kb.kiem_bat_bien("m", doan, [[]])[1])
    # số đoạn đổi
    assert any("số đoạn đổi" in e for e in kb.kiem_bat_bien("m", doan, nk, cu * 2)[0])


def test_that_bao_cao_12_mau_dat_bat_bien_va_co_du_muc():
    rows = kb.cs.doc_mau()
    if not all((kb.cs.OUT_ROOT / r["ma_mau"] / "page.txt").exists() for r in rows):
        pytest.skip("thiếu page.txt của một mẫu")
    ket_qua = kb.sinh_lai(rows)
    loi = {"khop_dia": [], "cu": [], "bo": [], "rev": ""}
    for ma, doan, nk in ket_qua:
        tren_dia = (kb.cs.OUT_ROOT / ma / "doan.jsonl").read_text(encoding="utf-8")
        assert tren_dia == "".join(json.dumps({k: d[k] for k in kb.cs.TRUONG_JSONL}, ensure_ascii=False) + "\n" for d in doan), ma
        loi_cu, loi_bo = kb.kiem_bat_bien(ma, doan, nk)
        assert loi_cu == [] and loi_bo == [], (ma, loi_bo[:3])
    bao_cao = kb.viet_bao_cao(ket_qua, loi)
    assert "| **Cộng** | **1245** | **190** | **337** | **356** | **55** | **21** | **32** |" in bao_cao
    for muc in ("## Bất biến đã kiểm bằng code", "## 1. Bảng tổng", "## 2. Chỗ chỉnh khoảng trắng khi bỏ",
                "## 3. Danh sách đầy đủ từng chỗ đã xóa (337 chỗ)", "## 4. Nghi xóa nhầm", "## 5. Có thể còn sót",
                "### 5.2 Mã chữ hoa + số", "### 5.3 Đối chiếu với thẻ `<sup>`", "## 6. Dấu `*` còn lại trong noi_dung (5 chỗ)",
                "## 7. Bảng ghi tay (21 mục bỏ thêm, 1 mục giữ lại)", "### 7.1 Ký hiệu bỏ thêm (`KY_HIEU_BO_THEM`): 21 mục, 29 chỗ",
                "### 7.2 Ngoại lệ giữ lại (`KY_HIEU_GIU_LAI`): 1 mục"):
        assert muc in bao_cao, muc
    assert "**KHÔNG đạt**" not in bao_cao and bao_cao.count("**đạt**") == 2  # khớp đĩa và bỏ đúng ký hiệu (không có --cu)
    assert "`dt-apple-iphone17#016`" in bao_cao and "20 phút⟦6⟧ với" in bao_cao and "30 phút⟦6⟧ với" in bao_cao
    sup = kb.doi_chieu_sup(ket_qua)
    assert all(v["con"] == 0 and v["ds_con"] == [] for v in sup.values())  # không còn ký hiệu <sup> nào trong noi_dung
    assert sup["dt-apple-iphone17"]["goc"] > 0 and sup["dt-samsung-galaxys25ultra"]["goc"] > 0 and sup["dt-oppo-findx8"]["goc"] == 0
    ghi_tay = [x for _, doan, _ in ket_qua for d in doan for x in d["ky_hieu_bo"] if x["loai"] == kb.cd.KY_HIEU_GHI_TAY]
    assert len(ghi_tay) == 29 and sum(len(x["so"]) for x in ghi_tay) == 32
