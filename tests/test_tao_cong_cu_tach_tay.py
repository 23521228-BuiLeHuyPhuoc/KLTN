import csv as csvmod
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import subprocess

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def nap(ten, duong):
    spec = importlib.util.spec_from_file_location(ten, ROOT / duong)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


tt = nap("tao_cong_cu_tach_tay", "scripts/tao_cong_cu_tach_tay.py")
ct = nap("chuyen_tuyen_bo_cho_so_sanh", "scripts/chuyen_tuyen_bo.py")
NODE = shutil.which("node")


@pytest.fixture(scope="module")
def trang(tmp_path_factory):
    ra = tmp_path_factory.mktemp("tach_tay") / "cong_cu.html"
    tt.main(["--ra", str(ra)])
    html = ra.read_text(encoding="utf-8")
    m = re.search(r'<script id="du-lieu" type="application/json">(.*?)</script>', html, flags=re.S)
    return html, json.loads(m.group(1))


# ---------- Đọc bài ----------

def test_doc_64_bai_8_mau_moi_mau_8_bai():
    bai = tt.doc_bai(tt.TEP_DOC)
    assert len(bai) == 64 and len({b["ma"] for b in bai}) == 64
    mau = tt.doc_mau()
    dem = {}
    for b in bai:
        m = tt.ma_mau_cua_bai(b["ma"], mau)
        assert mau[m]["tap"] == "kiemtra"
        dem[m] = dem.get(m, 0) + 1
    assert len(dem) == 8 and set(dem.values()) == {8}


def test_toan_van_la_chuoi_con_cua_tep_doc():
    nguon = tt.TEP_DOC.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    for b in tt.doc_bai(tt.TEP_DOC):
        assert b["van_ban"].strip() and b["van_ban"] in nguon
        assert len(b["thong_tin"]) >= 3  # sản phẩm, LLM, loại bài (, chế độ)


def test_bai_khong_khop_mau_thi_thoat(tmp_path):
    doc = tmp_path / "doc.md"
    doc.write_text("## `qc-dt-khong-co-gemini-x-1`\n\nA · B · C · D\n\n```text\nnội dung\n```\n", encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        tt.nap_du_lieu(doc, "k")
    assert "không khớp mẫu nào" in str(e.value)


def test_mau_khong_thuoc_tap_kiem_tra_thi_thoat(tmp_path):
    doc = tmp_path / "doc.md"
    doc.write_text("## `qc-dt-apple-iphone17-gemini-x-1`\n\nA · B · C · D\n\n```text\nnội dung\n```\n", encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        tt.nap_du_lieu(doc, "k")
    assert "không phải 'kiemtra'" in str(e.value)


# ---------- Thuộc tính theo nhóm ----------

def test_thuoc_tinh_theo_nhom_trung_nguon_chuyen_tuyen_bo(trang):
    _, du = trang
    for nhom in ct.NHOM.values():
        yaml_tt = yaml.safe_load((ROOT / "data" / "cau_hinh" / f"{nhom}.yaml").read_text(encoding="utf-8"))["thuoc_tinh"]
        ds = [x["ma"] for x in du["thuoc_tinh"][nhom]]
        assert set(ds) == set(yaml_tt) and len(ds) == len(set(ds))
        assert all(x["y_nghia"] and x["dau_hieu"] for x in du["thuoc_tinh"][nhom])
    # thứ tự theo bảng hướng dẫn
    assert [x["ma"] for x in du["thuoc_tinh"]["dong_ho"]] == ["thoi_luong_pin", "sac_nhanh", "do_sang", "khang_nuoc"]
    assert len(du["thuoc_tinh"]["dien_thoai"]) == 8


def test_bai_gan_nhom_dung(trang):
    _, du = trang
    for b in du["bai"]:
        assert ct.NHOM[b["ma_mau"][:2]] == b["nhom"]


# ---------- HTML ----------

def test_json_nhung_doc_lai_duoc_va_du_bai(trang):
    _, du = trang
    assert len(du["bai"]) == 64 and du["khoa"] == "tach_tay_kiem_tra_v1" and du["cot_csv"] == list(tt.COT_CSV)
    goc = {b["ma"]: b["van_ban"] for b in tt.doc_bai(tt.TEP_DOC)}
    assert all(b["van_ban"] == goc[b["ma"]] for b in du["bai"])
    assert "Giữ ngữ cảnh" in du["huong_dan"]["quy_tac_html"]
    assert "Điều kiện bổ nghĩa trực tiếp" in du["huong_dan"]["tieu_chi_html"]


def test_json_nhung_chan_dong_the_script():
    s = tt.json_nhung({"a": "</script><b>"})
    assert "<" not in s and json.loads(s) == {"a": "</script><b>"}


def test_html_tu_chua_khong_tai_tu_mang(trang):
    html, _ = trang
    assert "data/nhan" not in html
    assert "<script src" not in html.lower() and "http" not in html.lower()
    assert not re.search(r"<link[^>]+href|@import|<img|<iframe|fetch\(|XMLHttpRequest", html)


def test_khong_ghi_de_tep_co_san(tmp_path):
    ra = tmp_path / "a.html"
    ra.write_text("cũ", encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        tt.main(["--ra", str(ra)])
    assert "không ghi đè" in str(e.value)
    assert ra.read_text(encoding="utf-8") == "cũ"


def test_khoa_tuy_chon(tmp_path):
    ra = tmp_path / "b.html"
    tt.main(["--ra", str(ra), "--khoa", "khoa_khac"])
    assert '"khoa":"khoa_khac"' in ra.read_text(encoding="utf-8")


def khoi(html, ten):
    m = re.search(rf"/\* >>> {ten}.*?/\* <<< {ten} \*/", html, flags=re.S)
    assert m, f"không thấy khối {ten}"
    return m.group(0)


def test_cu_phap_javascript_hop_le(trang, tmp_path):
    if not NODE:
        pytest.skip("không có node")
    html, _ = trang
    js = re.search(r"<script>\n(.*?)</script>", html, flags=re.S).group(1)
    js = js.replace("const DL = JSON.parse(document.getElementById('du-lieu').textContent);", "const DL = {};")
    tep = tmp_path / "cong_cu.js"
    tep.write_text(js, encoding="utf-8")
    kq = subprocess.run([NODE, "--check", str(tep)], capture_output=True, text=True, encoding="utf-8")
    assert kq.returncode == 0, kq.stderr


# ---------- Hàm thuần trong node ----------

def chay_node(trang, ma_js, tmp_path):
    """Chạy khối HAM_THUAN của trang rồi ma_js (đặt kết quả vào biến kq); trả về kq đã qua JSON."""
    if not NODE:
        pytest.skip("không có node")
    html, _ = trang
    tep = tmp_path / "chay.js"
    tep.write_text(khoi(html, "HAM_THUAN") + "\n" + ma_js + "\nprocess.stdout.write(JSON.stringify(kq));\n", encoding="utf-8")
    r = subprocess.run([NODE, str(tep)], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_csv_bom_crlf_quote_va_thu_tu(trang, tmp_path):
    ma = r"""
const ds = [{ma: 'qc-a'}, {ma: 'qc-b'}, {ma: 'qc-c'}];
const st = {bai: {
  'qc-a': {dong: [
    {id: 'x2', t: 2, bd: 50, cau_goc: 'sau', thuoc_tinh: 'sac_nhanh', tuyen_bo: ' B ', ghi_chu: ''},
    {id: 'x1', t: 1, bd: 10, cau_goc: 'câu, có "ngoặc"', thuoc_tinh: 'thoi_luong_pin', tuyen_bo: 'Dòng 1\nDòng 2', ghi_chu: 'g'},
    {id: 'x3', t: 3, bd: 10, cau_goc: 'câu, có "ngoặc"', thuoc_tinh: 'khang_nuoc', tuyen_bo: 'C', ghi_chu: ''}]},
  'qc-b': {dong: []},
  'qc-c': {dong: [{id: 'y', t: 4, bd: 0, cau_goc: 'đầu', thuoc_tinh: 'zoom', tuyen_bo: 'D', ghi_chu: 'a,b'}]}}};
const kq = taoCsv(ds, st, ['ma_qc','cau_goc','tuyen_bo','thuoc_tinh','ghi_chu','can_xem']);
"""
    csv = chay_node(trang, ma, tmp_path)
    assert csv.startswith("﻿ma_qc,cau_goc,tuyen_bo,thuoc_tinh,ghi_chu,can_xem\r\n")
    assert csv.endswith("\r\n")
    # xuống dòng thật chỉ nằm trong ô được quote; ngoài ra mọi xuống dòng là CRLF
    assert csv.count("\n") == csv.count("\r\n") + 1
    assert '"Dòng 1\nDòng 2"' in csv and '"câu, có ""ngoặc"""' in csv and '"a,b"' in csv
    hang = list(csvmod.reader(io.StringIO(csv[1:], newline="")))
    assert hang[0] == ["ma_qc", "cau_goc", "tuyen_bo", "thuoc_tinh", "ghi_chu", "can_xem"]
    assert hang[1:] == [
        ["qc-a", 'câu, có "ngoặc"', "Dòng 1\nDòng 2", "thoi_luong_pin", "g", ""],
        ["qc-a", 'câu, có "ngoặc"', "C", "khang_nuoc", "", ""],
        ["qc-a", "sau", "B", "sac_nhanh", "", ""],
        ["qc-c", "đầu", "D", "zoom", "a,b", ""],
    ]


CA_KIEM = [
    # (tên ca, cau_goc, tuyen_bo, mã cảnh báo mong đợi)
    ("hoan_hao", "Pin dùng đến 20 giờ khi xem video", "Galaxy Watch8 pin dùng đến 20 giờ khi xem video", []),
    ("trong", "Pin 20 giờ", "   ", ["a"]),
    ("so_la", "Pin 20 giờ", "Galaxy Watch8 pin 24 giờ", ["b"]),
    ("so_thap_phan_cung_nghia", "Sáng 2,5 nit", "Galaxy Watch8 sáng 2.5 nit", []),
    ("ngan_nghin", "Sáng 3.000 nit", "Galaxy Watch8 sáng 3000 nit", []),
    ("ngan_nghin_phay_va_hep", "Pin 5 000 mAh", "Galaxy Watch8 pin 5,000 mAh", []),
    ("so_cua_ten_khong_tinh", "Pin 20 giờ", "GALAXY WATCH8 pin 20 giờ", []),
    ("thieu_len_den", "Pin lên đến 20 giờ", "Galaxy Watch8 pin 20 giờ", ["c"]),
    ("thieu_toi_da", "Pin Tối Đa 20 giờ", "Galaxy Watch8 pin 20 giờ", ["c"]),
    ("co_up_to", "Battery up to 20 hours", "Galaxy Watch8 battery up to 20 hours", []),
    ("doi_len_den_sang_toi_da", "Pin lên đến 20 giờ", "Galaxy Watch8 pin tối đa 20 giờ", []),
    ("thieu_ten", "Pin 20 giờ", "Đồng hồ pin 20 giờ", ["d"]),
    ("nhieu_loi", "Pin lên đến 20 giờ", "Đồng hồ pin 30 giờ", ["b", "c", "d"]),
]


def ma_kiem(ca):
    return f"const ca = {json.dumps(ca, ensure_ascii=False)};\nconst kq = ca.map((c) => kiemDong(c.d, c.b).map((x) => x.ma));"


def test_canh_bao_a_den_d_trong_node(trang, tmp_path):
    ca = [{"d": {"bd": 0, "cau_goc": g, "tuyen_bo": b, "thuoc_tinh": "thoi_luong_pin", "ghi_chu": ""},
           "b": {"ten_mau": "Galaxy Watch8", "van_ban": "xx " + g + " yy"}} for _, g, b, _ in CA_KIEM]
    kq = chay_node(trang, ma_kiem(ca), tmp_path)
    for (ten, _, _, mong), got in zip(CA_KIEM, kq):
        assert got == mong, ten


def test_canh_bao_e_cau_goc_khong_con_trong_bai(trang, tmp_path):
    ca = [{"d": {"bd": 0, "cau_goc": "câu lạ", "tuyen_bo": "Galaxy Watch8 câu lạ", "thuoc_tinh": "zoom", "ghi_chu": ""},
           "b": {"ten_mau": "Galaxy Watch8", "van_ban": "bài khác"}}]
    assert chay_node(trang, ma_kiem(ca), tmp_path) == [["e"]]


def test_chia_doan_va_cat_khoang_trang(trang, tmp_path):
    ma = r"""
const van = 'ab 12 cd 3,5 e';
const dongs = [{id: 'p', bd: 3, cau_goc: '12 cd'}];
const kq = {
  cat: [catKhoangTrang('  xy z  ', 0, 8), catKhoangTrang('   ', 0, 3)],
  doan: chiaDoan(van, dongs, true).map((o) => [van.slice(o.s, o.e), o.so, o.ids]),
  khongSo: chiaDoan(van, dongs, false).map((o) => [van.slice(o.s, o.e), o.so, o.ids]),
};
"""
    kq = chay_node(trang, ma, tmp_path)
    assert kq["cat"] == [{"bd": 2, "kt": 6}, None]
    assert kq["doan"] == [["ab ", False, []], ["12", True, ["p"]], [" cd", False, ["p"]], [" ", False, []], ["3,5", True, []],
                          [" e", False, []]]
    assert kq["khongSo"] == [["ab ", False, []], ["12 cd", False, ["p"]], [" 3,5 e", False, []]]


def test_nhap_sao_luu_chi_nhan_ma_bai_co_trong_trang(trang, tmp_path):
    ma = r"""
const ds = [{ma: 'qc-a', van_ban: 'Pin 20 giờ nhé', ds_tt: ['thoi_luong_pin', 'zoom']}];
const du = {bai: {
  'qc-a': {xong: 'co', dong: [
    {id: 'd1', t: 5, bd: 0, cau_goc: 'Pin 20 giờ', thuoc_tinh: 'thoi_luong_pin', tuyen_bo: 'A', ghi_chu: ''},
    {id: 'd2', t: 6, bd: 99, cau_goc: 'giờ nhé', thuoc_tinh: 'zoom', tuyen_bo: '', ghi_chu: 'x'},
    {id: 'd3', t: 7, bd: 0, cau_goc: 'Pin', thuoc_tinh: 'sac_nhanh', tuyen_bo: '', ghi_chu: ''},
    {id: 'd4', t: 8, bd: 0, cau_goc: '', thuoc_tinh: 'zoom'}]},
  'qc-la': {xong: 'co', dong: [{id: 'z', cau_goc: 'a', thuoc_tinh: 'zoom'}]}}};
const r = nhapTrangThai(du, ds);
const kq = {boQua: r.boQua, baiLa: r.baiLa, ma: Object.keys(r.st.bai), tiep: r.st.tiep, xong: r.st.bai['qc-a'].xong,
  dong: r.st.bai['qc-a'].dong.map((d) => [d.id, d.bd, d.thuoc_tinh])};
"""
    kq = chay_node(trang, ma, tmp_path)
    assert kq["boQua"] == 3 and kq["baiLa"] == ["qc-la"] and kq["ma"] == ["qc-a"]
    assert kq["xong"] == "co" and kq["tiep"] == 7
    assert kq["dong"] == [["d1", 0, "thoi_luong_pin"], ["d2", 7, "zoom"]]  # d2: vị trí tính lại theo chuỗi


# ---------- Bản nháp tuyên bố ----------

CUM_KHEN_HUONG_DAN = ["cả ngày", "suốt ngày dài", "không lo hết pin", "siêu bền", "bền bỉ", "vượt trội", "tuyệt đối", "trọn vẹn",
                      "không giới hạn"]


def test_cum_khen_nhung_khop_huong_dan(trang):
    _, du = trang
    md = tt.TEP_HUONG_DAN.read_text(encoding="utf-8-sig")
    m = re.search(r"Cụm khen đứng cạnh một con số\s*\((.*?)\)", md, flags=re.S)
    assert du["cum_khen"] == re.findall(r'"([^"]+)"', m.group(1))
    assert du["cum_khen"] == CUM_KHEN_HUONG_DAN


def ma_nhap(ca, cum):
    return (f"CUM_KHEN = {json.dumps(cum, ensure_ascii=False)};\nconst ca = {json.dumps(ca, ensure_ascii=False)};\n"
            "const kq = ca.map((c) => nhapTuyenBo(c[0], c[1]));")


CA_NHAP = [
    # (câu gốc, tên mẫu, bản nháp mong đợi)
    ("- Thời lượng pin lên đến 30 giờ.", "Galaxy Watch8", "Galaxy Watch8 Thời lượng pin lên đến 30 giờ"),
    ("• Sạc nhanh 50% trong 30 phút!", "Galaxy S25", "Galaxy S25 Sạc nhanh 50% trong 30 phút"),
    ("1) Pin 5.000 mAh", "Galaxy S25", "Galaxy S25 Pin 5.000 mAh"),
    # Hành vi mong đợi: chỉ xóa cụm khen và nhãn khung bài, KHÔNG viết lại câu (còn lại "dùng" lửng là chủ ý, người dùng tự sửa).
    ("Lợi ích chính: Pin bền bỉ 30 giờ, dùng cả ngày", "Galaxy Watch8", "Galaxy Watch8 Pin 30 giờ, dùng"),
    ("Độ sáng: 3.000 nits", "Galaxy Watch8", "Galaxy Watch8 Độ sáng 3.000 nits"),
    ("Phiên bản 2: Pin 30 giờ", "Galaxy Watch8", "Galaxy Watch8 Pin 30 giờ"),
    ("Galaxy Watch8 có pin 30 giờ.", "Galaxy Watch8", "Galaxy Watch8 có pin 30 giờ"),
    ("galaxy watch8: pin\n  lên   đến 30 giờ", "Galaxy Watch8", "galaxy watch8: pin lên đến 30 giờ"),  # tiền tố có chữ số nên giữ nguyên dấu hai chấm
    ("Pin tối đa 30 giờ, luôn bền", "Galaxy Watch8", "Galaxy Watch8 Pin tối đa 30 giờ, luôn bền"),
    ("Pin SIÊU BỀN, vượt trội, 5000 mAh", "Galaxy S25", "Galaxy S25 Pin, 5000 mAh"),
    ("Pin 5000 mAh, trọn vẹn.", "Galaxy S25", "Galaxy S25 Pin 5000 mAh"),
    ("Pin cả ngày dài 20 giờ", "Galaxy S25", "Galaxy S25 Pin dài 20 giờ"),
    ("Pin tuyệt đốix 20 giờ", "Galaxy S25", "Galaxy S25 Pin tuyệt đốix 20 giờ"),  # cụm dính chữ cái thì không khớp
]


def test_nhap_tuyen_bo_trong_node(trang, tmp_path):
    kq = chay_node(trang, ma_nhap([[g, t] for g, t, _ in CA_NHAP], CUM_KHEN_HUONG_DAN), tmp_path)
    for (g, _, mong), got in zip(CA_NHAP, kq):
        assert got == mong, g


def test_nhap_tuyen_bo_khong_them_ten_lan_hai_va_giu_so(trang, tmp_path):
    cau = "Pin lên đến 30 giờ, sạc 50% trong 30 phút, luôn ổn định"
    kq = chay_node(trang, ma_nhap([[cau, "Galaxy Watch8"], ["Galaxy Watch8 " + cau, "Galaxy Watch8"], [" . ", "X"]],
                                  CUM_KHEN_HUONG_DAN), tmp_path)
    assert kq[0] == "Galaxy Watch8 " + cau
    assert kq[1] == "Galaxy Watch8 " + cau and kq[1].lower().count("galaxy watch8") == 1
    assert kq[2] == ""
    for g in ("lên đến", "30 giờ", "50%", "30 phút", "luôn"):
        assert g in kq[0]


def test_canh_bao_f_khi_con_nhap_va_chuan_dong_doc_du_lieu_cu(trang, tmp_path):
    ma = r"""
const b = {ten_mau: 'Galaxy Watch8', van_ban: 'Pin 20 giờ'};
const d = (nhap) => ({bd: 0, cau_goc: 'Pin 20 giờ', tuyen_bo: 'Galaxy Watch8 Pin 20 giờ', thuoc_tinh: 'zoom', ghi_chu: '', nhap});
const cu = {cau_goc: 'Pin 20 giờ', thuoc_tinh: 'zoom', tuyen_bo: 'x'};
const bb = {van_ban: 'Pin 20 giờ', ds_tt: ['zoom']};
const kq = {bat: kiemDong(d(true), b).map((x) => x.ma), tat: kiemDong(d(false), b).map((x) => x.ma),
  khong: kiemDong(Object.assign(d(true), {nhap: undefined}), b).map((x) => x.ma),
  cu: chuanDong(cu, bb, 'qc-a').nhap, moi: chuanDong(Object.assign({}, cu, {nhap: true}), bb, 'qc-a').nhap,
  la: chuanDong(Object.assign({}, cu, {nhap: 'true'}), bb, 'qc-a').nhap};
"""
    kq = chay_node(trang, ma, tmp_path)
    assert kq == {"bat": ["f"], "tat": [], "khong": [], "cu": False, "moi": True, "la": False}
