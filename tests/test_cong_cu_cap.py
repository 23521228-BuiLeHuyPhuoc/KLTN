"""Kiểm trang gán nhãn tập cặp tối thiểu (--bo cap, Bước 25) bằng biến thể giả tự đặt; không đọc nhãn hay data/cap_toi_thieu.jsonl."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cong_cu_cap", ROOT / "scripts/tao_cong_cu_gan_nhan.py")
tc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tc)
spec_kn = importlib.util.spec_from_file_location("kiem_nhan_cap", ROOT / "scripts/kiem_nhan.py")
kn = importlib.util.module_from_spec(spec_kn)
spec_kn.loader.exec_module(kn)

MA_MAU = ["dh-apple-watchse3", "dt-xiaomi-15t"]
SO_GOC, SO_LOAI, SO_MOI_GOC_LOAI = 4, 6, 1
# Mã băm của trang cũ sinh bằng tham số cố định, đo trước khi thêm --bo cap, với hướng dẫn thay bằng bản giả (để không phụ
# thuộc nội dung data/huong_dan_gan_nhan.md, vốn đang được sửa). Đổi mẫu HTML hay dữ liệu bộ thử thì phải đo lại có chủ ý.
# Đã đo lại một lần vì thêm hiện số chú thích của trang hãng: so với trang cũ, dữ liệu nhúng chỉ thêm trường dau và dau_ct
# của các đoạn có số chú thích, mẫu chỉ thêm CSS, JS hiện số và sửa hàm lấy phần bôi đen (đã đối chiếu bằng diff bỏ phần dữ liệu).
SHA_THU_LUOT2 = "a56696105df8f7ebe04730efa517696e0c5ccaf210d445d85a1d4ba5b7eb6f08"
SHA_THU_LUOT3 = "2120104dce764a9d1289e72f052650c64b356bf520919c5acb1f31a3e0c35ca3"
SHA_CHINH = "fbd5cf3f8d72f1370e7c5daf5b1067482a9be209ba155ceaa100da36f6e532ae"


def du_lieu_nhung(html):
    return json.loads(re.search(r'<script id="du-lieu" type="application/json">(.*?)</script>', html, re.S).group(1))


def bien_the_gia():
    """24 biến thể giả: 4 gốc x 6 loại, id kiểu ct-<số>-<đuôi> với đuôi đặc trưng; goc, loai, cau_goc... đều là chuỗi đặc trưng
    không trùng id, để dò chúng trong trang."""
    ds = []
    for g in range(SO_GOC):
        for l in range(SO_LOAI):
            n = len(ds) + 1
            ds.append({"id": f"ct-{n:05d}-DAC_TRUNG_ID_{n}", "goc": f"KHONG_NHUNG_GOC_{g}", "loai": f"KHONG_NHUNG_LOAI_{l}",
                       "tap": "phat_trien" if g % 2 else "kiem_tra", "ma_mau": MA_MAU[g % 2], "thuoc_tinh": "thoi_luong_pin",
                       "tuyen_bo": f"Pin dùng được {10 + n} giờ.", "ma_qc": f"KHONG_NHUNG_MA_QC_{g}",
                       "cau_goc": f"KHONG_NHUNG_CAU_GOC_{g}", "llm_sinh": "KHONG_NHUNG_LLM", "che_do": "KHONG_NHUNG_CHE_DO",
                       "loai_bai": "KHONG_NHUNG_LOAI_BAI", "url_nguon": "https://khong-nhung.example/x",
                       "ghi_chu": "KHONG_NHUNG_GHI_CHU"})
    return ds


def ghi_cap(tmp_path, ds, ten="cap.jsonl"):
    tep = tmp_path / ten
    tep.write_text("".join(json.dumps(t, ensure_ascii=False) + "\n" for t in ds), encoding="utf-8")
    return tep


@pytest.fixture
def tep_cap(tmp_path):
    ds = bien_the_gia()
    # Tệp đảo ngược thứ tự: thứ tự hiển thị không được phụ thuộc thứ tự trong tệp.
    return ghi_cap(tmp_path, list(reversed(ds))), ds


@pytest.fixture
def trang_cap(tep_cap, tmp_path):
    tep, ds = tep_cap
    ra = tmp_path / "con" / "cap.html"
    tc.main(["--bo", "cap", "--tuyen-bo", str(tep), "--ra", str(ra)])
    html = ra.read_text(encoding="utf-8")
    return html, du_lieu_nhung(html), ds


def html_tinh(html):
    """Trang bỏ khối dữ liệu JSON nhúng: chỉ còn chữ và mã JavaScript tĩnh của giao diện."""
    return re.sub(r'<script id="du-lieu" type="application/json">.*?</script>', "", html, flags=re.S)


def test_du_lieu_nhung_khong_lo_goi_y_nhan(trang_cap):
    html, du_lieu, ds = trang_cap
    assert len(du_lieu["tuyen_bo"]) == len(ds)
    # Mọi chuỗi gợi ý (giá trị goc, loai, cau_goc, ma_qc, ... đặc trưng) không có trong cả trang, kể cả khối dữ liệu.
    for chu in ("KHONG_NHUNG_GOC_", "KHONG_NHUNG_LOAI_", "KHONG_NHUNG_CAU_GOC_", "KHONG_NHUNG_MA_QC_", "KHONG_NHUNG_LLM",
                "KHONG_NHUNG_CHE_DO", "KHONG_NHUNG_LOAI_BAI", "khong-nhung.example", "KHONG_NHUNG_GHI_CHU"):
        assert chu not in html, chu
    for t in du_lieu["tuyen_bo"]:
        assert set(t) == set(tc.TRUONG_TUYEN_BO)
        for k in ("ma_qc", "cau_goc", "llm_sinh", "che_do", "loai_bai", "url_nguon", "ghi_chu"):
            assert t[k] == "", k
        assert "goc" not in t and "loai" not in t and "tap" not in t
    # Chỉ id (để xuất tệp), ma_mau, tuyen_bo, thuoc_tinh còn nội dung.
    goc = {t["id"]: t for t in ds}
    for t in du_lieu["tuyen_bo"]:
        assert t["ma_mau"] == goc[t["id"]]["ma_mau"] and t["tuyen_bo"] == goc[t["id"]]["tuyen_bo"]
        assert t["thuoc_tinh"] == "thoi_luong_pin"
    assert sorted(t["id"] for t in du_lieu["tuyen_bo"]) == sorted(goc)
    # Không nạp bài quảng cáo; đoạn tài liệu của mọi mẫu có biến thể.
    assert du_lieu["bai"] == {}
    assert set(du_lieu["doan"]) == set(MA_MAU)
    for ma in MA_MAU:
        assert du_lieu["doan"][ma] == [tc.doan_nhung(d) for d in tc.doc_jsonl(tc.THU_MUC_NGUON / ma / "doan.jsonl")]


def test_giao_dien_khong_hien_id(trang_cap):
    """Hai lớp kiểm. (1) Chữ tĩnh của trang (HTML và JavaScript, đã bỏ khối dữ liệu JSON): không có chuỗi đuôi id đặc trưng,
    nên id chỉ xuất hiện trong dữ liệu dùng để xuất tệp. (2) Mã JavaScript: mọi chỗ dựng chữ hiển thị từ id của mẫu dùng chung
    (danh sách trái, tiêu đề thẻ, nút cảnh báo, tệp câu hỏi, thông báo nhập) đã được thay bằng 'Biến thể N' (TENHT); không
    còn dòng gốc nào hiện tb.id, ma_qc, llm_sinh... ra giao diện."""
    html, du_lieu, ds = trang_cap
    tinh = html_tinh(html)
    assert "DAC_TRUNG_ID" not in tinh
    assert any("DAC_TRUNG_ID" in t["id"] for t in du_lieu["tuyen_bo"])
    assert "TENHT" in tinh
    for cu in ("el('span', 'ma-muc', tb.id)", "$('the-ma').textContent = tb.id", "'Mã bài', tb.ma_qc", "tb.llm_sinh",
               "tb.che_do", "tb.loai_bai", "el('button', 'lien-ket', id)", "'- ' + tb.id", "tb.ma_qc + ')'",
               "'id ' + o.id", "o.id + ' không qua kiểm", "thieuDong.join", "(tb-\\d+)", "không có bài ' + tb.ma_qc"):
        assert cu not in tinh, cu
    # Danh sách trái và thẻ ghi số thứ tự, khung chi tiết chỉ Thuộc tính và Mẫu.
    assert "el('span', 'ma-muc', TENHT.get(tb.id))" in tinh
    assert "'Biến thể ' + (state.idx + 1) + '/' + TB.length" in tinh
    assert "[['Thuộc tính', tb.thuoc_tinh], ['Mẫu', tb.ma_mau]]" in tinh
    assert "Biến thể (\\d+)" in tinh
    # Khung bài quảng cáo ẩn, không nói tới bài.
    assert '<div class="khung" hidden>\n      <details class="hd" id="kh-bai">' in tinh
    assert "(biến thể không có bài gốc)" in tinh


def test_khoa_luu_ten_tep_va_tieu_de(trang_cap):
    html, du_lieu, _ = trang_cap
    assert du_lieu["trang"] == {"luot": 1, "khoa_nhan": "gan_nhan_cap_v1", "khoa_giao_dien": "gan_nhan_giao_dien_cap_v1",
                                "tep_nhan": "cap_toi_thieu_nhan.jsonl", "tep_hoi": "cau_hoi_nhan_cap.md",
                                "nghi_ms": tc.NGHI_GIAY * 1000, "bo": "cap"}
    # Không trùng khóa của trang bộ thử, tập chính.
    cac_khac = {tc.KHOA_NHAN, tc.KHOA_GIAO_DIEN, tc.cau_hinh_luot(3)["khoa_nhan"], tc.cau_hinh_chinh(MA_MAU)["khoa_nhan"],
                tc.cau_hinh_chinh(MA_MAU)["khoa_giao_dien"]}
    assert not cac_khac & {"gan_nhan_cap_v1", "gan_nhan_giao_dien_cap_v1"}
    assert "<title>Công cụ gán nhãn chuẩn - Tập cặp tối thiểu (Bước 25)</title>" in html
    assert "<h1>Công cụ gán nhãn chuẩn - Tập cặp tối thiểu (Bước 25)</h1>" in html
    assert "Tập cặp tối thiểu (Bước 25), lượt 1: gán mù từng biến thể" in html
    assert "Tải nhãn (cap_toi_thieu_nhan.jsonl)" in html and "Tải câu hỏi nhãn (cau_hoi_nhan_cap.md)" in html


def test_thu_tu_xao_on_dinh_theo_seed(tep_cap, tmp_path):
    tep, ds = tep_cap
    def thu_tu(**kw):
        return [t["id"] for t in tc.nap_du_lieu(bo="cap", tuyen_bo_tep=tep, **kw)["tuyen_bo"]]
    mac_dinh = thu_tu()
    assert mac_dinh == thu_tu()
    assert sorted(mac_dinh) == sorted(t["id"] for t in ds)
    assert mac_dinh != sorted(mac_dinh)
    assert mac_dinh != [t["id"] for t in ds] and mac_dinh != [t["id"] for t in reversed(ds)]
    # Không phụ thuộc thứ tự dòng trong tệp.
    tep2 = ghi_cap(tmp_path, ds, "cap2.jsonl")
    assert [t["id"] for t in tc.nap_du_lieu(bo="cap", tuyen_bo_tep=tep2)["tuyen_bo"]] == mac_dinh
    # Seed khác thì thứ tự khác; mặc định là 20261127.
    assert tc.SEED_XAO_CAP == 20261127
    assert thu_tu(seed_cap=20261127) == mac_dinh
    assert thu_tu(seed_cap=1) != mac_dinh
    # Cùng gốc hoặc cùng loại không liền nhau (dữ liệu giả có đủ gốc và loại để tránh được).
    theo_id = {t["id"]: t for t in ds}
    for a, b in zip(mac_dinh, mac_dinh[1:]):
        assert theo_id[a]["goc"] != theo_id[b]["goc"]
        assert theo_id[a]["loai"] != theo_id[b]["loai"]


def test_seed_xao_qua_dong_lenh(tep_cap, tmp_path):
    tep, _ = tep_cap
    ra1, ra2 = tmp_path / "a.html", tmp_path / "b.html"
    tc.main(["--bo", "cap", "--tuyen-bo", str(tep), "--ra", str(ra1), "--seed-xao", "7"])
    tc.main(["--bo", "cap", "--tuyen-bo", str(tep), "--ra", str(ra2)])
    a, b = (du_lieu_nhung(r.read_text(encoding="utf-8"))["tuyen_bo"] for r in (ra1, ra2))
    assert [t["id"] for t in a] != [t["id"] for t in b]
    with pytest.raises(SystemExit) as e:
        tc.main(["--seed-xao", "7", "--ra", str(tmp_path / "c.html")])
    assert e.value.code == 2


def test_ma_mau_voi_bo_cap_bao_loi(tep_cap, tmp_path):
    tep, _ = tep_cap
    ra = tmp_path / "x.html"
    with pytest.raises(SystemExit) as e:
        tc.main(["--bo", "cap", "--tuyen-bo", str(tep), "--ma-mau", *MA_MAU, "--ra", str(ra)])
    assert e.value.code == 2
    assert not ra.exists()


def test_thieu_tep_cap_bao_loi_khong_tao_tep(tmp_path):
    ra = tmp_path / "x.html"
    with pytest.raises(SystemExit) as e:
        tc.main(["--bo", "cap", "--tuyen-bo", str(tmp_path / "khong_co.jsonl"), "--ra", str(ra)])
    assert "thiếu tệp cặp tối thiểu" in str(e.value)
    assert not ra.exists()


def test_khong_ghi_de_trang_da_co(tep_cap, tmp_path):
    tep, _ = tep_cap
    ra = tmp_path / "x.html"
    ra.write_text("cu", encoding="utf-8")
    with pytest.raises(SystemExit):
        tc.main(["--bo", "cap", "--tuyen-bo", str(tep), "--ra", str(ra)])
    assert ra.read_text(encoding="utf-8") == "cu"


def test_id_lap_hoac_thieu_truong_bao_loi(tmp_path):
    ds = bien_the_gia()[:3]
    ds[1]["id"] = ds[0]["id"]
    with pytest.raises(SystemExit) as e:
        tc.nap_du_lieu(bo="cap", tuyen_bo_tep=ghi_cap(tmp_path, ds))
    assert "id lặp" in str(e.value)
    ds = bien_the_gia()[:3]
    ds[2]["ma_mau"] = ""
    with pytest.raises(SystemExit) as e:
        tc.nap_du_lieu(bo="cap", tuyen_bo_tep=ghi_cap(tmp_path, ds, "b.jsonl"))
    assert "thiếu trường ma_mau" in str(e.value)


def test_trang_thu_va_chinh_khong_doi(monkeypatch, tmp_path):
    """Sinh lại trang bộ thử (lượt 2, lượt 3) và tập chính bằng tham số cố định: mã băm phải bằng mã đo trước khi thêm --bo cap."""
    monkeypatch.setattr(tc, "doc_huong_dan", lambda *a, **k: "")
    monkeypatch.setattr(tc, "dung_huong_dan", lambda md: {"dong_d": [], "loai": [], "mac_dinh": [], "huong_loi": []})
    def bam(tep):
        return hashlib.sha256(tep.read_bytes()).hexdigest()
    tc.main(["--ra", str(tmp_path / "thu.html")])
    assert bam(tmp_path / "thu.html") == SHA_THU_LUOT2
    tc.main(["--luot", "3", "--ra", str(tmp_path / "thu3.html")])
    assert bam(tmp_path / "thu3.html") == SHA_THU_LUOT3
    ds = []
    for ma in MA_MAU:
        for tep in sorted(tc.THU_MUC_QC.glob(f"qc-{ma}-*.json"))[:2]:
            b = json.loads(tep.read_text(encoding="utf-8"))
            ds.append({"id": f"tb-{67 + len(ds):05d}", "ma_qc": b["ma_qc"], "ma_mau": ma, "cau_goc": "Pin dùng được 10 giờ.",
                       "tuyen_bo": "Pin dùng được 10 giờ.", "thuoc_tinh": "thoi_luong_pin"})
    tep = ghi_cap(tmp_path, ds, "chinh.jsonl")
    tc.main(["--bo", "chinh", "--tuyen-bo", str(tep), "--ma-mau", *MA_MAU, "--ra", str(tmp_path / "chinh.html")])
    assert bam(tmp_path / "chinh.html") == SHA_CHINH


def test_kiem_nhan_chay_tren_nhan_cua_bien_the(tep_cap, tmp_path):
    tep, ds = tep_cap
    hai = ghi_cap(tmp_path, ds[:2], "hai.jsonl")
    nhan = [{"id": t["id"], "nhan": "CHUA_DU", "dong_d": "D1", "loai": None, "bang_chung": [], "trich": "",
             "ly_do": "Tài liệu không nói tới thông số này.", "nguoi_gan": "A", "luot": 1, "giay": 30,
             "tai_lieu_mau_thuan": False, "ghi_chu": "", "giay_nghi": 0} for t in ds[:2]]
    tep_nhan = ghi_cap(tmp_path, nhan, "cap_toi_thieu_nhan.jsonl")
    loi, dong_nhan, so = kn.kiem_tep(tep_nhan, hai, luot=1)
    assert loi == [] and so == 2 and len(dong_nhan) == 2
    # Thiếu nhãn của một biến thể và id lạ đều bị báo.
    loi, _, _ = kn.kiem_tep(ghi_cap(tmp_path, nhan[:1], "mot.jsonl"), hai, luot=1)
    assert any("thiếu nhãn cho" in e for e in loi)
    la = dict(nhan[0], id="ct-99999-la")
    loi, _, _ = kn.kiem_tep(ghi_cap(tmp_path, [la, nhan[1]], "la.jsonl"), hai, luot=1)
    assert any("không có trong tệp tuyên bố" in e for e in loi)
