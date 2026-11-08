"""Kiểm công cụ tập chính bằng tuyên bố tự đặt; không đọc nhãn hay dữ liệu tập kiểm tra."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cong_cu_chinh", ROOT / "scripts/tao_cong_cu_gan_nhan.py")
tc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tc)
MA_PHAT_TRIEN = ["dh-apple-watchse3", "dt-xiaomi-15t"]
# Dấu vân tay mẫu HTML trước khi thêm tập chính, chuẩn hóa xuống dòng như Python đọc mã nguồn.
SHA_MAU_CU = "bd0c3e2618e6fb4e75e7e6af8895d98d22c30b6fb304708cac13204cfa6a3405"


def du_lieu_nhung(html):
    """Đọc khối JSON của trang sinh trong thư mục tạm."""
    return json.loads(re.search(r'<script id="du-lieu" type="application/json">(.*?)</script>', html, re.S).group(1))


def ma_kiem_tra():
    """Chỉ đọc danh mục CSV, không mở quảng cáo hoặc tài liệu của tập kiểm tra."""
    with tc.TEP_MAU.open(encoding="utf-8-sig", newline="") as f:
        return sorted(m["ma_mau"] for m in csv.DictReader(f) if m["tap"] == "kiemtra")


@pytest.fixture
def tep_chinh(tmp_path):
    ds = []
    for ma in MA_PHAT_TRIEN:
        bai = sorted(tc.THU_MUC_QC.glob(f"qc-{ma}-*.json"))[:2]
        assert len(bai) == 2, f"cần hai bài thật của {ma}"
        for tep in bai:
            b = json.loads(tep.read_text(encoding="utf-8"))
            assert b["ma_mau"] == ma
            ds.append({"id": f"tb-{67 + len(ds):05d}", "ma_qc": b["ma_qc"], "ma_mau": ma,
                       "cau_goc": "Pin dùng được 10 giờ.", "tuyen_bo": "Pin dùng được 10 giờ.",
                       "thuoc_tinh": "thoi_luong_pin", "nhan": "KHONG_NHUNG_NHAN",
                       "nguoi_gan": "KHONG_NHUNG_NGUOI_GAN"})
    # Mã ngoài tập chỉ là dữ liệu giả trong tmp_path; không cần mở quảng cáo hay nguồn của mã này.
    ngoai = {"id": "tb-99999", "ma_qc": "khong_duoc_doc", "ma_mau": ma_kiem_tra()[0],
             "tuyen_bo": "KHONG_NHUNG_TUYEN_BO_NGOAI_TAP"}
    tep = tmp_path / "chinh.jsonl"
    tep.write_text("".join(json.dumps(t, ensure_ascii=False) + "\n" for t in [ngoai, *reversed(ds)]), encoding="utf-8")
    return tep, ds


def lenh_chinh(tep, ra):
    """Tham số sinh trang phát triển vào thư mục tạm."""
    return ["--bo", "chinh", "--tuyen-bo", str(tep), "--ma-mau", *MA_PHAT_TRIEN, "--ra", str(ra)]


@pytest.fixture
def trang_chinh(tep_chinh, tmp_path):
    tep, ds = tep_chinh
    ra = tmp_path / "con" / "phat_trien.html"
    tc.main(lenh_chinh(tep, ra))
    html = ra.read_text(encoding="utf-8")
    return html, du_lieu_nhung(html), ds


def test_trang_chinh_chi_nhung_du_lieu_da_loc(trang_chinh):
    html, du_lieu, ds = trang_chinh
    assert len(du_lieu["tuyen_bo"]) == 4
    assert [t["id"] for t in du_lieu["tuyen_bo"]] == [t["id"] for t in ds]
    assert set(du_lieu["bai"]) == {t["ma_qc"] for t in ds}
    assert set(du_lieu["doan"]) == set(MA_PHAT_TRIEN)
    for ma in MA_PHAT_TRIEN:
        assert du_lieu["doan"][ma] == [tc.doan_nhung(d) for d in tc.doc_jsonl(tc.THU_MUC_NGUON / ma / "doan.jsonl")]
    assert not set(ma_kiem_tra()) & {t["ma_mau"] for t in du_lieu["tuyen_bo"]}
    assert not set(ma_kiem_tra()) & set(du_lieu["doan"])
    assert all(set(t) == set(tc.TRUONG_TUYEN_BO) for t in du_lieu["tuyen_bo"])
    for chu in ("KHONG_NHUNG_NHAN", "KHONG_NHUNG_NGUOI_GAN", "KHONG_NHUNG_TUYEN_BO_NGOAI_TAP", "khong_duoc_doc"):
        assert chu not in html
    assert du_lieu["huong_dan"] == tc.dung_huong_dan(tc.doc_huong_dan())


def test_cau_hinh_tieu_de_va_tep_tai_ve(trang_chinh):
    html, du_lieu, _ = trang_chinh
    t = du_lieu["trang"]
    assert t == {"luot": 1, "bo": "chinh", "nhan_bo": "phat_trien", "nghi_ms": 180000,
                 "khoa_nhan": "gan_nhan_chinh_v2_dh-apple-watchse3_dt-xiaomi-15t",
                 "khoa_giao_dien": "gan_nhan_giao_dien_chinh_v2_dh-apple-watchse3_dt-xiaomi-15t",
                 "tep_nhan": "chinh_phat_trien.jsonl", "tep_hoi": "cau_hoi_nhan_chinh_phat_trien.md"}
    assert "gan_nhan_thu_v2" not in html
    assert "<title>Công cụ gán nhãn chuẩn - bộ chính - tập phát triển, 4 tuyên bố, lượt 1</title>" in html
    assert "Bước 20 · lượt 1" in html
    assert "Tải nhãn (chinh_phat_trien.jsonl)" in html
    assert "Tải câu hỏi nhãn (cau_hoi_nhan_chinh_phat_trien.md)" in html
    assert "Nhập lại chinh_phat_trien.jsonl đã xuất" in html
    assert "Lượt 1 gán mù với các lượt trước" not in html
    assert "luot: LUOT," in html and "nguoi_gan: (r.nguoi_gan || state.nguoi_gan).trim()" in html


def test_cau_hinh_kiem_tra_chi_can_danh_muc():
    pt = tc.cau_hinh_chinh(MA_PHAT_TRIEN)
    kt = tc.cau_hinh_chinh(ma_kiem_tra())
    assert tc.cau_hinh_chinh(list(reversed(MA_PHAT_TRIEN))) == pt
    assert kt["nhan_bo"] == "kiem_tra"
    assert kt["tep_nhan"] == "chinh_kiem_tra.jsonl"
    assert kt["tep_hoi"] == "cau_hoi_nhan_chinh_kiem_tra.md"
    assert kt["khoa_nhan"] != pt["khoa_nhan"] and kt["khoa_giao_dien"] != pt["khoa_giao_dien"]
    assert all(ma in kt["khoa_nhan"] for ma in ma_kiem_tra())


@pytest.mark.parametrize("ma", [[], ["dh-apple-watchse3"], ["sai"], ["dt-apple-iphone17", "tn-samsung-buds3pro"],
                                MA_PHAT_TRIEN + ["dt-oppo-findx8"], MA_PHAT_TRIEN + ["dh-apple-watchse3"]])
def test_danh_sach_mau_sai_khong_ghi(tmp_path, ma):
    ra = tmp_path / "sai.html"
    args = ["--bo", "chinh", "--ra", str(ra)] + (["--ma-mau", *ma] if ma else [])
    with pytest.raises(SystemExit, match="--ma-mau"):
        tc.main(args)
    assert not ra.exists()


@pytest.mark.parametrize("co_tep", [False, True])
def test_thieu_tep_hoac_loc_rong_khong_ghi(tmp_path, co_tep):
    tep, ra = tmp_path / "chinh.jsonl", tmp_path / "chua_tao" / "trang.html"
    if co_tep:
        tep.write_text(json.dumps({"id": "tb-99999", "ma_mau": "ngoai-tap"}) + "\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="không có tuyên bố nào" if co_tep else "thiếu tệp tuyên bố tập chính"):
        tc.main(lenh_chinh(tep, ra))
    assert not ra.parent.exists()


def test_mac_dinh_tap_chinh_va_khong_ghi_de(tep_chinh, tmp_path, monkeypatch):
    tep, _ = tep_chinh
    monkeypatch.setattr(tc, "TEP_TUYEN_BO_CHINH", tep)
    monkeypatch.setattr(tc, "TEP_RA", tmp_path / "cong_cu_gan_nhan.html")
    args = ["--bo", "chinh", "--ma-mau", *MA_PHAT_TRIEN]
    tc.main(args)
    ra = tmp_path / "cong_cu_gan_nhan_chinh_phat_trien.html"
    cu = ra.read_bytes()
    assert du_lieu_nhung(cu.decode("utf-8"))["trang"]["luot"] == 1
    with pytest.raises(SystemExit, match="không ghi đè"):
        tc.main(args)
    assert ra.read_bytes() == cu


@pytest.mark.parametrize("them", [["--luot", "2"], ["--luot", "3"], ["--chon", "khong_duoc_doc.txt"]])
def test_chinh_tu_choi_tham_so_luot_thu(tep_chinh, tmp_path, them):
    ra = tmp_path / "sai.html"
    with pytest.raises(SystemExit):
        tc.main(lenh_chinh(tep_chinh[0], ra) + them)
    assert not ra.exists()


def html_theo_ma_cu(du_lieu):
    """Giữ phép dựng trang trước thay đổi, kết hợp dấu vân tay mẫu HTML cố định."""
    assert hashlib.sha256(tc.MAU_HTML.encode("utf-8")).hexdigest() == SHA_MAU_CU
    t = du_lieu["trang"]
    if t["luot"] == 2:
        gan_mu = "Lượt __LUOT__ gán mù với lượt trước: không mở nhãn lượt 1 và các ghi chép về nhãn lượt 1."
    else:
        gan_mu = ("Lượt __LUOT__ gán mù với các lượt trước: không mở nhãn lượt 1, nhãn lượt 2 (kể cả nhãn do Claude gán) và "
                  "các ghi chép về những nhãn đó.")
    mau = tc.MAU_HTML.replace("__GAN_MU__", gan_mu)
    mau = mau.replace("__LUOT__", str(t["luot"])).replace("__TEP_NHAN__", t["tep_nhan"]).replace("__TEP_HOI__", t["tep_hoi"])
    return mau.replace("__DU_LIEU__", tc.json_nhung(du_lieu)).encode("utf-8")


def test_mac_dinh_giong_tung_byte_khong_doc_nhan(tmp_path, monkeypatch):
    du_lieu = tc.nap_du_lieu()
    assert len(du_lieu["tuyen_bo"]) == 66
    assert du_lieu["trang"] == {"luot": 2, "khoa_nhan": tc.KHOA_NHAN, "khoa_giao_dien": tc.KHOA_GIAO_DIEN,
                                "tep_nhan": tc.TEN_TEP_NHAN, "tep_hoi": tc.TEN_TEP_HOI, "nghi_ms": 180000}
    assert tc.KHOA_NHAN == "gan_nhan_thu_v2" and tc.TEN_TEP_NHAN == "thu_luot2.jsonl"
    assert tc.KHOA_GIAO_DIEN == "gan_nhan_giao_dien_v2" and tc.TEN_TEP_HOI == "cau_hoi_nhan_luot2.md"
    ra = tmp_path / "thu.html"
    monkeypatch.setattr(tc, "TEP_RA", ra)
    tc.main([])
    mot = ra.read_bytes()
    tc.main([])
    assert ra.read_bytes() == mot == html_theo_ma_cu(du_lieu)


def test_luot3_giong_tung_byte_voi_ma_chon_tu_dat(tmp_path):
    ma = [t["id"] for t in tc.doc_jsonl(tc.TEP_TUYEN_BO)][:4]
    chon, ra = tmp_path / "chon.txt", tmp_path / "luot3.html"
    chon.write_text("\n".join(ma), encoding="utf-8")
    tc.main(["--luot", "3", "--chon", str(chon), "--ra", str(ra)])
    assert ra.read_bytes() == html_theo_ma_cu(tc.nap_du_lieu(3, ma))


def test_javascript_xuat_va_nhap_dung_bo_luot(trang_chinh, tmp_path):
    node = shutil.which("node")
    if not node:
        pytest.skip("không có node")
    html, du_lieu, _ = trang_chinh
    js = re.search(r"<script>\n(.*?)</script>", html, re.S).group(1)
    tep = tmp_path / "trang.js"
    tep.write_text(js, encoding="utf-8")
    kq = subprocess.run([node, "--check", str(tep)], capture_output=True, text=True, encoding="utf-8")
    assert kq.returncode == 0, kq.stderr
    ham = "\n".join(re.search(r"(?:async )?function " + ten + r"\([^\n]*\) \{.*?\n\}", js, re.S).group(0)
                    for ten in ("tachTheoLuot", "banGhiXuat", "nhapTep"))
    khoi = "const TB = " + json.dumps(du_lieu["tuyen_bo"], ensure_ascii=False) + ";\n"
    khoi += "const LUOT = " + str(du_lieu["trang"]["luot"]) + ";\n" + ham + r'''
const assert = require('node:assert/strict');
const state = {nguoi_gan: 'Người gán'};
const r = {nhan: 'DUNG', dong_d: 'D3', bang_chung: [], trich: '', ly_do: '', ghi_chu: '', ms: 1000, ms_nghi: 0};
const bg = () => r, coLoai = () => false;
const alerts = [], confirms = [];
const alert = (s) => alerts.push(s), confirm = (s) => { confirms.push(s); return false; };
async function nhap(o) {
  alerts.length = 0; confirms.length = 0;
  await nhapTep([{name: 'thu.jsonl', text: async () => JSON.stringify(o)}]);
}
(async () => {
  const xuat = banGhiXuat(0);
  assert.equal(xuat.luot, 1);
  assert.equal(xuat.nguoi_gan, 'Người gán');
  await nhap(xuat);
  assert.equal(confirms.length, 1);
  assert.equal(alerts.length, 0);
  for (const luot of [2, 3, undefined]) {
    await nhap({...xuat, luot});
    assert.equal(confirms.length, 0);
    assert.ok(alerts[0].includes('không phải lượt 1'));
  }
  await nhap({...xuat, id: 'tb-99999'});
  assert.equal(confirms.length, 0);
  assert.ok(alerts[0].includes('không thuộc bộ'));
})().catch((e) => { console.error(e); process.exitCode = 1; });
'''
    tep.write_text(khoi, encoding="utf-8")
    kq = subprocess.run([node, str(tep)], capture_output=True, text=True, encoding="utf-8")
    assert kq.returncode == 0, kq.stderr
