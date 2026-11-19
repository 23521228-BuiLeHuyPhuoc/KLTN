"""Bước 23: sinh công cụ tách tuyên bố bằng tay data/tuyen_bo/cong_cu_tach_kiem_tra.html cho 64 bài của tập kiểm tra.

Mục đích: người thực hiện tách TAY tuyên bố (hướng dẫn: data/tuyen_bo/huong_dan_tach_tay.md) thay vì chép vào Excel. Trang cho
bôi đen một câu trong bài, bấm thuộc tính, ra một dòng; tự gõ câu tuyên bố; xuất CSV đúng định dạng để nối vào cuối
data/tuyen_bo/chinh_nhap.csv.

Một tệp HTML tự chứa (CSS, JavaScript viết thẳng, không tải gì từ mạng), mở trực tiếp bằng trình duyệt (file://). Dữ liệu nhúng
dưới dạng JSON: toàn văn 64 bài (data/tuyen_bo/doc_kiem_tra.md, giữ nguyên từng ký tự), tên sản phẩm và nhóm theo
data/mau_san_pham.csv, danh sách thuộc tính hợp lệ của từng nhóm, nội dung hướng dẫn (đọc lúc sinh trang: sửa
huong_dan_tach_tay.md rồi chạy lại script là trang cập nhật).

RANH GIỚI (giữ khi sửa): cột cau_goc (chọn câu) và tuyen_bo (câu viết lại) là đáp án chuẩn để chấm bước tách tự động bằng LLM ở
Bước 29, nên trang KHÔNG được gợi ý câu nào nên chọn, KHÔNG đoán thuộc tính cho câu, KHÔNG viết lại câu, KHÔNG thêm hay bỏ điều kiện.
Được phép: điền sẵn bản nháp tuyên bố TẤT ĐỊNH (quy tắc chuỗi, không LLM) từ câu người dùng đã bôi đen: gộp khoảng trắng, bỏ ký hiệu
đầu dòng, bỏ nhãn khung bài ("Lợi ích chính:"...), xóa các cụm khen theo mục "Bỏ qua" của hướng dẫn (đọc lúc sinh trang), bỏ dấu câu
cuối, thêm tên sản phẩm vào đầu nếu chưa có; không đụng con số, đơn vị, "lên đến"/"tối đa", từ khẳng định hay điều kiện. Người thực
hiện tự rà và sửa; dòng còn nguyên bản nháp bị cảnh báo (f) và ô tuyên bố đổi màu. Được phép: tô nhạt MỌI chữ số trong bài như nhau (không phân biệt đơn vị, không gắn thuộc tính; có nút bật/tắt) và kiểm tra tất
định trên chính các ô người dùng điền: (a) tuyen_bo trống; (b) con số trong tuyen_bo không có trong cau_goc; (c) cau_goc có
"lên đến"/"tối đa"/"up to" mà tuyen_bo không có; (d) tuyen_bo không chứa tên sản phẩm; thêm (e) cau_goc không còn nằm trong bài
(chỉ xảy ra khi sinh lại trang từ tệp bài đã đổi); (f) tuyên bố còn là bản nháp tự động chưa sửa. Cảnh báo chỉ là gợi ý rà theo quy tắc 2, 3 của hướng dẫn, không chặn và không
kết luận đúng sai.

Danh sách thuộc tính hợp lệ của mỗi nhóm lấy từ ĐÚNG nguồn scripts/chuyen_tuyen_bo.py dùng: tên nhóm theo chuyen_tuyen_bo.NHOM,
khóa "thuoc_tinh" của data/cau_hinh/<nhóm>.yaml. Thứ tự và cột "ý nghĩa" theo bảng "Thuộc tính được giữ" của huong_dan_tach_tay.md;
script thoát nếu bảng đó và yaml không khớp nhau. Cột "dấu hiệu" là hằng DAU_HIEU trong script này.

Chạy:
    .venv/Scripts/python.exe -X utf8 scripts/tao_cong_cu_tach_tay.py [--doc TEP_MD] [--ra TEP_HTML] [--khoa KHOA_LOCALSTORAGE]
Không ghi đè tệp --ra đã có (báo lỗi, chọn --ra khác hoặc xóa tệp cũ). Trang lưu vào localStorage của trình duyệt theo --khoa,
sinh lại trang không mất dữ liệu đã tách (cùng khóa, cùng đường dẫn tệp).

Cách dùng:
1. Mở data/tuyen_bo/cong_cu_tach_kiem_tra.html bằng trình duyệt.
2. Chọn bài ở cột trái. Bôi đen câu cần tách ở giữa, bấm nút thuộc tính (hoặc phím 1, 2, ...) để thêm dòng; câu có hai con số thì bôi
   lại và bấm thuộc tính khác. Ở cột phải gõ tuyên bố, ghi chú nếu cần. Xong bài thì bấm "Xong bài" (hoặc "Bài không có câu nào").
3. Bấm "Xuất CSV" (tải tach_kiem_tra.csv). "Sao lưu JSON" để lưu dự phòng, "Nhập sao lưu" để khôi phục.
4. Gửi tach_kiem_tra.csv cho Claude: nối vào cuối data/tuyen_bo/chinh_nhap.csv rồi chạy
   scripts/chuyen_tuyen_bo.py data/tuyen_bo/chinh_nhap.csv data/tuyen_bo/chinh.jsonl --tiep-sau data/tuyen_bo/thu.jsonl
"""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
import re
import sys
import unicodedata

import yaml

GOC = Path(__file__).resolve().parents[1]
TEP_DOC = GOC / "data" / "tuyen_bo" / "doc_kiem_tra.md"
TEP_RA = GOC / "data" / "tuyen_bo" / "cong_cu_tach_kiem_tra.html"
TEP_MAU = GOC / "data" / "mau_san_pham.csv"
TEP_HUONG_DAN = GOC / "data" / "tuyen_bo" / "huong_dan_tach_tay.md"
KHOA_MAC_DINH = "tach_tay_kiem_tra_v1"
TAP_CUA_TRANG = "kiemtra"
TEN_TEP_CSV = "tach_kiem_tra.csv"
COT_CSV = ("ma_qc", "cau_goc", "tuyen_bo", "thuoc_tinh", "ghi_chu", "can_xem")
NHOM_TEN_TRONG_BANG = {"dien_thoai": "Điện thoại", "tai_nghe": "Tai nghe", "dong_ho": "Đồng hồ"}

# Dấu hiệu nhận biết từng thuộc tính (chữ gợi nhớ cố định, giống nhau cho mọi bài; không dò trong bài).
DAU_HIEU = {
    "thoi_luong_pin": "số giờ/ngày dùng pin, nghe nhạc, đàm thoại",
    "sac_nhanh": "sạc …% trong … phút, sạc đầy trong …, sạc … phút dùng … giờ",
    "cong_suat_sac": "W",
    "do_sang": "nit",
    "tan_so_quet": "Hz của màn hình",
    "zoom": "2x, 5x, zoom quang học",
    "khang_nuoc": "IP…, ATM, mét, ISO 22810, phút ngâm",
    "dung_luong_pin": "mAh",
}
# Màu từng thuộc tính (nền nhạt khi gạch chân câu đã chọn, nút bấm); cố định theo mã.
MAU_THUOC_TINH = {
    "thoi_luong_pin": "#1e88e5", "sac_nhanh": "#fb8c00", "cong_suat_sac": "#8e24aa", "do_sang": "#9e9d24",
    "tan_so_quet": "#00897b", "zoom": "#d81b60", "khang_nuoc": "#00838f", "dung_luong_pin": "#6d4c41",
}


def nap_module(ten, duong):
    spec = importlib.util.spec_from_file_location(ten, duong)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def chuyen_tuyen_bo():
    return nap_module("chuyen_tuyen_bo_cho_tach_tay", GOC / "scripts" / "chuyen_tuyen_bo.py")


def gan_nhan_md():
    """scripts/tao_cong_cu_gan_nhan.py: dùng lại bộ chuyển markdown và tách ô bảng (không đụng dữ liệu nhãn)."""
    return nap_module("tao_cong_cu_gan_nhan_cho_tach_tay", GOC / "scripts" / "tao_cong_cu_gan_nhan.py")


def thoat(thong_bao):
    sys.exit(thong_bao)


# ---------- Đọc bài ----------

_RE_TIEU_DE_BAI = re.compile(r"^## `(qc-[^`\s]+)`\s*$")


def doc_bai(tep):
    """Các bài trong tệp doc: [{ma, thong_tin (danh sách chữ cách nhau bởi " · "), van_ban}] theo thứ tự trong tệp.

    Mỗi bài: dòng `## \\`ma\\``, một dòng thông tin, khối ```text ... ```. van_ban là các dòng trong khối nối bằng \\n (giữ nguyên
    từng ký tự, kể cả dòng trống và khoảng trắng cuối dòng).
    """
    tep = Path(tep)
    if not tep.exists():
        thoat(f"không thấy tệp bài: {tep}")
    dong = tep.read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("\n")
    bai, i, n = [], 0, len(dong)
    while i < n:
        m = _RE_TIEU_DE_BAI.match(dong[i])
        if not m:
            i += 1
            continue
        ma, i = m.group(1), i + 1
        while i < n and not dong[i].strip():
            i += 1
        if i >= n or dong[i].startswith("```") or dong[i].startswith("## "):
            thoat(f"{tep.name}: bài {ma} không có dòng thông tin")
        thong_tin = [p.strip() for p in dong[i].split(" · ")]
        i += 1
        while i < n and not dong[i].strip():
            i += 1
        if i >= n or dong[i].rstrip() != "```text":
            thoat(f"{tep.name}: bài {ma} thiếu khối ```text")
        i += 1
        dau = i
        while i < n and dong[i].rstrip() != "```":
            i += 1
        if i >= n:
            thoat(f"{tep.name}: bài {ma} thiếu dòng đóng ```")
        van_ban = "\n".join(dong[dau:i])
        i += 1
        if not van_ban.strip():
            thoat(f"{tep.name}: bài {ma} không có nội dung")
        bai.append({"ma": ma, "thong_tin": thong_tin, "van_ban": van_ban})
    ma_lap = sorted({b["ma"] for b in bai if sum(1 for x in bai if x["ma"] == b["ma"]) > 1})
    if ma_lap:
        thoat(f"{tep.name}: mã bài lặp: {', '.join(ma_lap)}")
    if not bai:
        thoat(f"{tep.name}: không có bài nào")
    return bai


def doc_mau(tep=TEP_MAU):
    """{ma_mau: dòng của data/mau_san_pham.csv}."""
    with open(tep, encoding="utf-8-sig", newline="") as f:
        return {r["ma_mau"]: r for r in csv.DictReader(f)}


def ma_mau_cua_bai(ma_qc, mau):
    """ma_mau của bài theo tiền tố qc-<ma_mau>- (lấy mã dài nhất khớp); không khớp mẫu nào thì thoát."""
    khop = [m for m in mau if ma_qc.startswith(f"qc-{m}-")]
    if not khop:
        thoat(f"bài {ma_qc} không khớp mẫu nào trong {TEP_MAU.name} (tiền tố qc-<ma_mau>-)")
    return max(khop, key=len)


# ---------- Thuộc tính theo nhóm ----------

def thuoc_tinh_hop_le(ct):
    """{nhóm: tập thuộc tính hợp lệ}, đọc đúng như chuyen_tuyen_bo.chuyen: khóa thuoc_tinh của data/cau_hinh/<nhóm>.yaml."""
    return {n: set(yaml.safe_load((ct.GOC / "data" / "cau_hinh" / f"{n}.yaml").read_text(encoding="utf-8"))["thuoc_tinh"])
            for n in ct.NHOM.values()}


def bang_thuoc_tinh_md(md, gn):
    """Bảng "Thuộc tính được giữ" của hướng dẫn: [(mã, {tên nhóm trong bảng: ô})] theo thứ tự hàng."""
    dong, trong, hang, cot = md.split("\n"), False, [], None
    for d in dong:
        if d.startswith("## "):
            if trong:
                break
            trong = d[3:].strip() == "Thuộc tính được giữ"
            continue
        if trong and d.lstrip().startswith("|"):
            o = gn.tach_o_bang(d)
            if gn.la_dong_phan_cach(d):
                continue
            if cot is None:
                cot = o
                continue
            m = re.search(r"`([A-Za-z0-9_]+)`", o[0])
            if not m or len(o) != len(cot):
                thoat(f"{TEP_HUONG_DAN.name}: dòng bảng thuộc tính sai dạng: {d[:80]}")
            hang.append((m.group(1), dict(zip(cot[1:], o[1:]))))
    if not hang:
        thoat(f"{TEP_HUONG_DAN.name}: không thấy bảng ở mục '## Thuộc tính được giữ'")
    return hang, cot


def thuoc_tinh_theo_nhom(md, ct, gn):
    """{nhóm: [{ma, y_nghia, dau_hieu}]} theo thứ tự bảng hướng dẫn; ô "Không có" nghĩa là nhóm không giữ thuộc tính đó, và tập
    còn lại phải đúng bằng tập hợp lệ của yaml (cùng nguồn chuyen_tuyen_bo.py), nếu không thì thoát."""
    hang, cot = bang_thuoc_tinh_md(md, gn)
    hop_le = thuoc_tinh_hop_le(ct)
    ra = {}
    for nhom, ten in NHOM_TEN_TRONG_BANG.items():
        c = [x for x in cot[1:] if unicodedata.normalize("NFC", x).startswith(ten)]
        if len(c) != 1:
            thoat(f"{TEP_HUONG_DAN.name}: bảng thuộc tính phải có đúng một cột cho nhóm '{ten}' (có {len(c)})")
        ds = []
        for ma, o in hang:
            y = gn.van_ban_thuan(o[c[0]]).strip()
            if y and not y.startswith("Không có"):
                if ma not in DAU_HIEU:
                    thoat(f"thuộc tính {ma} chưa có trong DAU_HIEU của {Path(__file__).name}")
                ds.append({"ma": ma, "y_nghia": y, "dau_hieu": DAU_HIEU[ma]})
        if {x["ma"] for x in ds} != hop_le[nhom]:
            thoat(f"{TEP_HUONG_DAN.name} và data/cau_hinh/{nhom}.yaml không khớp thuộc tính nhóm {nhom}: "
                  f"bảng {sorted(x['ma'] for x in ds)}, yaml {sorted(hop_le[nhom])}")
        ra[nhom] = ds
    sai_mau = sorted(set(MAU_THUOC_TINH) ^ set(DAU_HIEU))
    if sai_mau:
        thoat(f"MAU_THUOC_TINH và DAU_HIEU lệch mã: {', '.join(sai_mau)}")
    return ra


def muc_hai(md, tieu_de):
    """Các dòng của mục '## <tieu_de>' (không kể dòng tiêu đề) tới mục '## ' kế tiếp."""
    ra, trong = [], False
    for d in md.split("\n"):
        if d.startswith("## "):
            if trong:
                break
            trong = d[3:].strip() == tieu_de
            continue
        if trong:
            ra.append(d)
    if not trong:
        thoat(f"{TEP_HUONG_DAN.name}: không thấy mục '## {tieu_de}'")
    return "\n".join(ra)


def cum_khen_tu_huong_dan(md):
    """Các cụm trong ngoặc kép ở câu "Cụm khen đứng cạnh một con số (...)" của hướng dẫn, theo thứ tự xuất hiện."""
    m = re.search(r"Cụm khen đứng cạnh một con số\s*\((.*?)\)", md, flags=re.S)
    cum = re.findall(r'["“]([^"”]+)["”]', m.group(1)) if m else []
    if not cum:
        thoat(f"{TEP_HUONG_DAN.name}: không thấy danh sách cụm khen ở câu 'Cụm khen đứng cạnh một con số (...)'")
    return cum


# ---------- Dữ liệu và HTML ----------

def nap_du_lieu(tep_doc, khoa):
    """Dữ liệu nhúng vào trang (xem docstring). Thoát nếu bài không khớp mẫu hoặc mẫu không thuộc tập kiểm tra."""
    ct, gn = chuyen_tuyen_bo(), gan_nhan_md()
    mau = doc_mau()
    bai = doc_bai(tep_doc)
    ra = []
    for b in bai:
        ma_mau = ma_mau_cua_bai(b["ma"], mau)
        m = mau[ma_mau]
        if m["tap"] != TAP_CUA_TRANG:
            thoat(f"bài {b['ma']}: mẫu {ma_mau} thuộc tập '{m['tap']}', không phải '{TAP_CUA_TRANG}'")
        if ct.NHOM.get(ma_mau[:2]) != m["nhom"]:
            thoat(f"mẫu {ma_mau}: nhóm '{m['nhom']}' không khớp tiền tố {ma_mau[:2]} của chuyen_tuyen_bo.NHOM")
        ra.append({"ma": b["ma"], "ma_mau": ma_mau, "ten_mau": m["ten"], "nhom": m["nhom"], "thong_tin": b["thong_tin"][1:],
                   "van_ban": b["van_ban"]})
    md = unicodedata.normalize("NFC", TEP_HUONG_DAN.read_text(encoding="utf-8-sig").replace("\r\n", "\n"))
    thuoc_tinh = thuoc_tinh_theo_nhom(md, ct, gn)
    cac_mau = list(dict.fromkeys(b["ma_mau"] for b in ra))
    return {"khoa": khoa, "tep_csv": TEN_TEP_CSV, "cot_csv": list(COT_CSV), "bai": ra,
            "mau": {m: {"ten": mau[m]["ten"], "nhom": mau[m]["nhom"]} for m in cac_mau},
            "thuoc_tinh": thuoc_tinh, "mau_thuoc_tinh": MAU_THUOC_TINH, "cum_khen": cum_khen_tu_huong_dan(md),
            "huong_dan": {"quy_tac_html": gn.chuyen_markdown(muc_hai(md, "5 quy tắc")),
                          "tieu_chi_html": gn.chuyen_markdown(muc_hai(md, "Tiêu chí gắn điều kiện"))}}


def json_nhung(du_lieu):
    """JSON an toàn để đặt trong thẻ <script type="application/json">: không để lọt '<' (chặn '</script>')."""
    return json.dumps(du_lieu, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def dung_html(du_lieu):
    return (KHUNG_HTML.replace("__DU_LIEU__", json_nhung(du_lieu))
            .replace("__HAM_THUAN__", HAM_THUAN_JS).replace("__GIAO_DIEN__", GIAO_DIEN_JS))


KHUNG_HTML = r"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>Tách tuyên bố bằng tay - tập kiểm tra</title>
<style>
* { box-sizing: border-box; }
body { margin: 0; font: 14px/1.45 system-ui, "Segoe UI", sans-serif; color: #222; background: #f4f5f7; height: 100vh;
  display: flex; flex-direction: column; overflow: hidden; }
header { background: #1f2d3d; color: #fff; padding: 6px 10px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
header h1 { font-size: 15px; margin: 0 8px 0 0; }
header button, header label { font-size: 13px; }
button { font: inherit; cursor: pointer; border: 1px solid #aab; background: #fff; border-radius: 4px; padding: 3px 8px; }
button:hover { background: #eef; }
header button { background: #34495e; color: #fff; border-color: #567; }
header button:hover { background: #46607a; }
#tien-do { display: flex; align-items: center; gap: 6px; font-size: 13px; }
#thanh { width: 140px; height: 10px; background: #567; border-radius: 5px; overflow: hidden; }
#thanh i { display: block; height: 100%; background: #4caf50; width: 0; }
header select { font-size: 13px; }
#chinh { flex: 1; display: grid; grid-template-columns: minmax(180px, 250px) minmax(320px, 1fr) minmax(300px, 430px); overflow-x: auto; gap: 6px; padding: 6px; min-height: 0; position: relative; }
.cot { background: #fff; border: 1px solid #ccd; border-radius: 4px; overflow: auto; min-height: 0; }
#trai .nhom { background: #e8ecf3; font-weight: 600; padding: 4px 8px; position: sticky; top: 0; z-index: 1; }
#trai .bai { padding: 4px 8px; border-bottom: 1px solid #eee; cursor: pointer; display: flex; gap: 6px; align-items: baseline; }
#trai .bai:hover { background: #f1f6ff; }
#trai .bai.chon { background: #dbe9ff; }
#trai .bai .ten { flex: 1; font-size: 12.5px; }
#trai .bai .tt { white-space: nowrap; font-size: 12.5px; }
#giua { display: flex; flex-direction: column; overflow: hidden; }
#giua .dau, #phai .dau { padding: 6px 10px; border-bottom: 1px solid #dde; background: #fafbfd; display: flex; flex-wrap: wrap; gap: 6px 10px; align-items: center; }
#van-bao { flex: 1; overflow: auto; padding: 10px 14px; }
#van { white-space: pre-wrap; font-size: 15px; line-height: 1.7; word-break: break-word; }
#van .so { background: #fff2b3; }
#van .ch { border-bottom: 3px solid; }
#phai { display: flex; flex-direction: column; overflow: hidden; }
#ds-dong { flex: 1; overflow: auto; padding: 6px; }
.dong { border: 1px solid #ccd; border-left-width: 6px; border-radius: 4px; padding: 6px; margin-bottom: 8px; background: #fff; }
.dong .goc { white-space: pre-wrap; background: #f5f5f5; padding: 4px 6px; border-radius: 3px; font-size: 13px; max-height: 6.5em; overflow: auto; }
.dong .hang { display: flex; gap: 6px; margin-top: 4px; align-items: center; }
.dong textarea { width: 100%; font: inherit; min-height: 54px; margin-top: 4px; resize: vertical; }
.dong input[type=text] { flex: 1; font: inherit; min-width: 0; }
.dong select { font: inherit; max-width: 200px; }
.dong textarea.nhap { background: #fff6dd; border: 2px solid #e0a020; }
.dong .canh-bao { color: #b45f00; font-size: 12.5px; margin-top: 3px; }
.dong .xoa { color: #b00020; }
.dong.thieu { background: #fffaf0; }
.nhan-nho { font-size: 12px; color: #667; }
#thanh-chon { position: fixed; display: none; z-index: 20; background: #263238; padding: 4px; border-radius: 6px; box-shadow: 0 2px 8px #0006; gap: 4px; flex-wrap: wrap; max-width: 520px; }
#thanh-chon button { color: #fff; border: 0; font-size: 12.5px; padding: 4px 8px; }
#thanh-chon button b { opacity: .8; margin-right: 3px; }
#hd { position: absolute; z-index: 15; left: 6px; right: 6px; top: 6px; max-height: calc(100% - 12px); overflow: auto; background: #fff; border: 2px solid #1f2d3d;
  border-radius: 6px; padding: 8px 14px; display: none; box-shadow: 0 4px 16px #0005; }
#hd table { border-collapse: collapse; margin: 4px 0 8px; }
#hd th, #hd td { border: 1px solid #ccd; padding: 3px 8px; text-align: left; vertical-align: top; }
#hd th { background: #eef; }
#hd h2 { font-size: 15px; margin: 8px 0 4px; }
#hd h3, #hd h4 { font-size: 14px; margin: 6px 0 2px; }
#hd summary { cursor: pointer; font-weight: 600; margin: 6px 0; }
.rong { color: #889; padding: 14px; }
</style>
</head>
<body>
<header>
  <h1>Tách tuyên bố bằng tay</h1>
  <div id="tien-do"><span id="chu-tien-do"></span><div id="thanh"><i></i></div></div>
  <select id="loc" title="Lọc danh sách bài">
    <option value="tat_ca">Tất cả bài</option><option value="chua_xong">Chưa xong</option><option value="canh_bao">Có cảnh báo</option>
  </select>
  <label><input type="checkbox" id="chk-so" checked> Tô nhạt số</label>
  <button id="nut-hd">Hướng dẫn</button>
  <button id="nut-csv">Xuất CSV</button>
  <button id="nut-sao-luu">Sao lưu JSON</button>
  <button id="nut-nhap">Nhập sao lưu</button>
  <input type="file" id="tep-nhap" accept=".json,application/json" style="display:none">
</header>
<div id="chinh">
  <div id="trai" class="cot"></div>
  <div id="giua" class="cot">
    <div class="dau"><b id="ma-bai"></b><span id="thong-tin-bai" class="nhan-nho"></span><button id="nut-tiep">Bài chưa xong kế tiếp ▶</button></div>
    <div id="van-bao"><div id="van"></div></div>
  </div>
  <div id="phai" class="cot">
    <div class="dau"><button id="nut-xong">Xong bài</button><button id="nut-khong">Bài không có câu nào</button><span id="tt-bai" class="nhan-nho"></span></div>
    <div id="ds-dong"></div>
  </div>
  <div id="hd"></div>
</div>
<div id="thanh-chon"></div>
<script id="du-lieu" type="application/json">__DU_LIEU__</script>
<script>
const DL = JSON.parse(document.getElementById('du-lieu').textContent);
__HAM_THUAN__
__GIAO_DIEN__
</script>
</body>
</html>
"""

HAM_THUAN_JS = r"""/* >>> HAM_THUAN: hàm không đụng DOM (test chạy riêng khối này trong node) */
const CUM_TOI_DA = ['lên đến', 'tối đa', 'up to'];
const KHONG_GIAN = /\s+/g;
/* Cụm khen cần bỏ khỏi bản nháp: giao diện gán từ DL.cum_khen (lấy từ huong_dan_tach_tay.md lúc sinh trang). */
let CUM_KHEN = [];
const NHAN_KHUNG = ['lợi ích chính', 'đặc điểm nổi bật', 'mô tả ngắn', 'hero headline', 'subheadline', 'tiêu đề', 'lời kêu gọi hành động',
  'bằng chứng', 'offer', 'cta', 'phiên bản 1', 'phiên bản 2'];

function nfc(s) { return String(s == null ? '' : s).normalize('NFC'); }
function bo(s) { return nfc(s).replace(KHONG_GIAN, ' ').trim().toLowerCase(); }
function thoatRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

/* Chuẩn hóa một cụm chữ số (đã bỏ khoảng trắng hẹp): dấu "." và "," thập phân như nhau; nhóm đúng 3 chữ số sau dấu là ngăn nghìn. */
function chuanSo(tok) {
  const bo0 = (x) => x.replace(/^0+(?=\d)/, '');
  const phan = tok.split(/[.,]/);
  if (phan.length === 1) return bo0(phan[0]);
  const nghin = phan.slice(1).every((p) => p.length === 3) && phan[0].length <= 3 && phan[0] !== '0';
  if (nghin) return bo0(phan.join(''));
  const le = phan[phan.length - 1].replace(/0+$/, '');
  return bo0(phan.slice(0, -1).join('')) + (le ? '.' + le : '');
}
function cacSo(s) {
  const t = nfc(s).replace(/(\d)[   ](?=\d{3}(?!\d))/g, '$1');
  return (t.match(/\d+(?:[.,]\d+)*/g) || []).map(chuanSo);
}

/* Bản nháp tuyên bố, tất định, chỉ xóa và ghép chuỗi (không viết lại câu, không thêm/bỏ con số, "lên đến", điều kiện):
   gộp khoảng trắng; bỏ ký hiệu đầu dòng; bỏ nhãn khung bài (nhãn khác thì chỉ đổi ":" thành dấu cách); xóa cụm khen nguyên cụm
   (không phân biệt hoa thường); bỏ dấu câu cuối; thêm tên sản phẩm vào đầu nếu chưa có. */
function nhapTuyenBo(cauGoc, tenMau) {
  let s = nfc(cauGoc).replace(KHONG_GIAN, ' ').trim();
  s = s.replace(/^(?:[•*>]\s*|(?:[-–]|\d+[.)])\s+)/, '');
  const hai = s.indexOf(':');
  if (hai > 0) {
    const truoc = s.slice(0, hai).trim(), sau = s.slice(hai + 1).trim();
    if (NHAN_KHUNG.includes(bo(truoc))) s = sau;
    else if (truoc.split(' ').length <= 4 && !/\d/.test(truoc)) s = truoc + ' ' + sau;
  }
  CUM_KHEN.slice().sort((x, y) => y.length - x.length).forEach((c) => {
    s = s.replace(new RegExp('(?<![\\p{L}\\p{N}])' + thoatRe(nfc(c)) + '(?![\\p{L}\\p{N}])', 'giu'), ' ');
  });
  s = s.replace(KHONG_GIAN, ' ').replace(/\s+([,;.!?])/g, '$1').replace(/,(?:\s*,)+/g, ',').replace(/^[\s,;]+/, '');
  s = s.replace(/[\s.!?…;:,]+$/, '').trim();
  const ten = nfc(tenMau).trim();
  if (!s) return '';
  return ten && !bo(s).includes(bo(ten)) ? ten + ' ' + s : s;
}

/* Kiểm tất định trên các ô người dùng điền. d = dòng, b = {ten_mau, van_ban}. Trả về [{ma, msg}] (không chặn). */
function kiemDong(d, b) {
  const kq = [];
  if (d.bd < 0 || !nfc(b.van_ban).includes(nfc(d.cau_goc))) {
    kq.push({ma: 'e', msg: 'Câu gốc không còn nằm trong bài (bài đã đổi?). Xóa dòng hoặc chọn lại.'});
  }
  const tb = nfc(d.tuyen_bo).trim();
  if (!tb) { kq.push({ma: 'a', msg: 'Chưa có tuyên bố.'}); return kq; }
  const ten = nfc(b.ten_mau).trim();
  const khongTen = ten ? tb.replace(new RegExp(thoatRe(ten), 'gi'), ' ') : tb;
  const soGoc = new Set(cacSo(d.cau_goc));
  const la = [...new Set(cacSo(khongTen))].filter((x) => !soGoc.has(x));
  if (la.length) kq.push({ma: 'b', msg: 'Con số ' + la.join(', ') + ' trong tuyên bố không có trong câu gốc (rà quy tắc 3).'});
  const goc = bo(d.cau_goc), tbl = bo(tb);
  if (CUM_TOI_DA.some((c) => goc.includes(c)) && !CUM_TOI_DA.some((c) => tbl.includes(c))) {
    kq.push({ma: 'c', msg: 'Câu gốc có "lên đến"/"tối đa"/"up to" mà tuyên bố không có (rà quy tắc 3).'});
  }
  if (ten && !tbl.includes(bo(ten))) kq.push({ma: 'd', msg: 'Tuyên bố không chứa tên sản phẩm "' + ten + '" (rà quy tắc 2).'});
  if (d.nhap === true) {
    kq.push({ma: 'f', msg: 'Tuyên bố còn là bản nháp tự động, chưa sửa: rà điều kiện theo quy tắc 2, 3 và tiêu chí gắn điều kiện ' +
      '(điều kiện ở câu trước/sau, cụm thuộc vế khác).'});
  }
  return kq;
}

function sapDong(ds) { return ds.slice().sort((x, y) => (x.bd - y.bd) || (x.t - y.t)); }

/* Cắt khoảng trắng hai đầu của đoạn [bd, kt) trong văn bản; trả null nếu rỗng. */
function catKhoangTrang(van, bd, kt) {
  while (bd < kt && /\s/.test(van[bd])) bd++;
  while (kt > bd && /\s/.test(van[kt - 1])) kt--;
  return kt > bd ? {bd, kt} : null;
}

/* Chia văn bản thành đoạn theo ranh giới: các dòng đã chọn (bd, cau_goc) và mọi cụm chữ số (khi tomSo). */
function chiaDoan(van, dongs, tomSo) {
  const n = van.length, so = new Uint8Array(n + 1), cat = new Set([0, n]);
  if (tomSo) {
    const re = /\d+(?:[.,]\d+)*/g; let m;
    while ((m = re.exec(van))) { for (let i = m.index; i < m.index + m[0].length; i++) so[i] = 1; cat.add(m.index); cat.add(m.index + m[0].length); }
  }
  const co = dongs.filter((d) => d.bd >= 0 && d.bd + d.cau_goc.length <= n);
  co.forEach((d) => { cat.add(d.bd); cat.add(d.bd + d.cau_goc.length); });
  const moc = [...cat].sort((x, y) => x - y), ra = [];
  for (let k = 0; k + 1 < moc.length; k++) {
    const a = moc[k], b = moc[k + 1];
    if (b <= a) continue;
    ra.push({s: a, e: b, so: !!so[a], ids: co.filter((d) => d.bd <= a && d.bd + d.cau_goc.length >= b).map((d) => d.id)});
  }
  return ra;
}

function trongCsv(v) {
  const s = String(v == null ? '' : v);
  return /[",\r\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}
/* CSV tuyên bố: BOM, CRLF, tiêu đề cot, bài theo thứ tự trong trang, dòng theo vị trí trong bài, can_xem trống. */
function taoCsv(dsBai, st, cot) {
  const dong = [cot.map(trongCsv).join(',')];
  dsBai.forEach((b) => {
    const t = st.bai[b.ma];
    if (!t) return;
    sapDong(t.dong).forEach((d) => {
      dong.push([b.ma, d.cau_goc, nfc(d.tuyen_bo).trim(), d.thuoc_tinh, nfc(d.ghi_chu).trim(), ''].map(trongCsv).join(','));
    });
  });
  return '﻿' + dong.join('\r\n') + '\r\n';
}

/* Chuẩn hóa một dòng đọc từ localStorage hay bản sao lưu: null nếu hỏng; vị trí bd tính lại khi lệch. */
function chuanDong(d, b, ma) {
  if (!d || typeof d !== 'object' || typeof d.cau_goc !== 'string' || !d.cau_goc.trim()) return null;
  if (!b.ds_tt.includes(d.thuoc_tinh)) return null;
  let bd = Number.isInteger(d.bd) ? d.bd : -1;
  if (bd < 0 || b.van_ban.substr(bd, d.cau_goc.length) !== d.cau_goc) bd = b.van_ban.indexOf(d.cau_goc);
  return {id: typeof d.id === 'string' && d.id ? d.id : ma + ':' + Math.random().toString(36).slice(2), t: Number.isFinite(d.t) ? d.t : 0, bd,
          cau_goc: d.cau_goc, thuoc_tinh: d.thuoc_tinh, tuyen_bo: typeof d.tuyen_bo === 'string' ? d.tuyen_bo : '',
          ghi_chu: typeof d.ghi_chu === 'string' ? d.ghi_chu : '', nhap: d.nhap === true};
}

/* Dựng trạng thái từ dữ liệu lưu/sao lưu; chỉ nhận mã bài có trong trang (dsBai: [{ma, van_ban, ds_tt}]). boQua = số dòng bỏ. */
function nhapTrangThai(du, dsBai) {
  const theoMa = {}; dsBai.forEach((b) => { theoMa[b.ma] = b; });
  const st = {tiep: 1, bai: {}}; let boQua = 0; const baiLa = [];
  const goc = du && typeof du === 'object' && du.bai && typeof du.bai === 'object' ? du.bai : {};
  Object.keys(goc).forEach((ma) => {
    const t = goc[ma], ds = t && Array.isArray(t.dong) ? t.dong : [];
    if (!theoMa[ma]) { boQua += ds.length; baiLa.push(ma); return; }
    const dong = [];
    ds.forEach((d) => { const c = chuanDong(d, theoMa[ma], ma); if (c) dong.push(c); else boQua++; });
    st.bai[ma] = {xong: t.xong === 'co' || t.xong === 'khong' ? t.xong : '', dong};
  });
  let max = 0;
  Object.keys(st.bai).forEach((ma) => st.bai[ma].dong.forEach((d) => { max = Math.max(max, d.t); }));
  Object.keys(st.bai).forEach((ma) => st.bai[ma].dong.forEach((d) => { if (!d.t) d.t = ++max; }));
  st.tiep = max + 1;
  dsBai.forEach((b) => { if (!st.bai[b.ma]) st.bai[b.ma] = {xong: '', dong: []}; });
  return {st, boQua, baiLa};
}
/* <<< HAM_THUAN */"""

GIAO_DIEN_JS = r"""
const KHOA = DL.khoa, KHOA_GD = DL.khoa + '_gd';
const BAI = DL.bai.map((b) => Object.assign({}, b, {ds_tt: DL.thuoc_tinh[b.nhom].map((x) => x.ma)}));
const THEO_MA = {}; BAI.forEach((b) => { THEO_MA[b.ma] = b; });
const $ = (id) => document.getElementById(id);
const MAU = DL.mau_thuoc_tinh;
CUM_KHEN = DL.cum_khen || [];
/* localStorage có thể bị chặn (trình duyệt tắt lưu trữ): khi đó trang vẫn chạy, chỉ không nhớ lại, nên nhắc dùng Sao lưu JSON. */
let luuDuoc = true;
function doc(khoa) { try { return JSON.parse(localStorage.getItem(khoa) || 'null'); } catch (x) { luuDuoc = false; return null; } }
function ghi(khoa, v) { try { localStorage.setItem(khoa, JSON.stringify(v)); } catch (x) { luuDuoc = false; } }
let st = nhapTrangThai(doc(KHOA), BAI).st;
let gd = Object.assign({chon: BAI[0].ma, so: true}, doc(KHOA_GD) || {});
if (!THEO_MA[gd.chon]) gd.chon = BAI[0].ma;
let hienTuyenBo = null;

function luu() { ghi(KHOA, st); }
function luuGd() { ghi(KHOA_GD, gd); }
function e(ten, thuoc, ...con) {
  const x = document.createElement(ten);
  Object.keys(thuoc || {}).forEach((k) => { if (k === 'cls') x.className = thuoc[k]; else if (k === 'txt') x.textContent = thuoc[k]; else x[k] = thuoc[k]; });
  con.forEach((c) => x.append(c));
  return x;
}
function bai() { return THEO_MA[gd.chon]; }
function tBai(ma) { return st.bai[ma]; }
function canhBaoBai(b) { return tBai(b.ma).dong.some((d) => kiemDong(d, b).length); }
function thieuBai(b) { return tBai(b.ma).dong.filter((d) => !d.tuyen_bo.trim()).length; }

function veTienDo() {
  const xong = BAI.filter((b) => tBai(b.ma).xong).length;
  const dong = BAI.reduce((s, b) => s + tBai(b.ma).dong.length, 0);
  $('chu-tien-do').textContent = 'Xong ' + xong + '/' + BAI.length + ' bài, ' + dong + ' dòng';
  $('thanh').firstElementChild.style.width = (100 * xong / BAI.length) + '%';
}

function veTrai() {
  const loc = $('loc').value, tr = $('trai'), cuon = tr.scrollTop;
  tr.textContent = '';
  let mauHt = '', k = 0, chen = 0;
  BAI.forEach((b) => {
    if (b.ma_mau !== mauHt) { mauHt = b.ma_mau; k = 0; }
    k++;
    const t = tBai(b.ma), cb = canhBaoBai(b);
    if (loc === 'chua_xong' && t.xong) return;
    if (loc === 'canh_bao' && !cb) return;
    if (b.ma_mau !== tr.lastGroup) { tr.append(e('div', {cls: 'nhom', txt: b.ten_mau})); tr.lastGroup = b.ma_mau; }
    const tt = (t.dong.length ? t.dong.length + ' dòng ' : '') + (t.xong ? '✅' : '') + (cb ? '⚠️' : '');
    const it = e('div', {cls: 'bai' + (b.ma === gd.chon ? ' chon' : ''), title: b.ma}, e('span', {cls: 'ten', txt: k + '. ' + b.thong_tin.join(' · ')}),
                 e('span', {cls: 'tt', txt: tt}));
    it.onclick = () => chonBai(b.ma);
    tr.append(it); chen++;
  });
  tr.lastGroup = null;
  if (!chen) tr.append(e('div', {cls: 'rong', txt: 'Không có bài nào theo bộ lọc.'}));
  tr.scrollTop = cuon;
}

function veGiua() {
  const b = bai(), v = $('van');
  $('ma-bai').textContent = b.ma;
  $('thong-tin-bai').textContent = b.ten_mau + ' · ' + b.thong_tin.join(' · ');
  v.textContent = '';
  const dongs = tBai(b.ma).dong, theoId = {}; dongs.forEach((d) => { theoId[d.id] = d; });
  chiaDoan(b.van_ban, dongs, gd.so).forEach((o) => {
    const chu = b.van_ban.slice(o.s, o.e);
    if (!o.ids.length && !o.so) { v.append(document.createTextNode(chu)); return; }
    const sp = e('span', {});
    sp.textContent = chu;
    if (o.so) sp.className = 'so';
    if (o.ids.length) {
      const d = theoId[o.ids[0]], mau = MAU[d.thuoc_tinh] || '#888';
      sp.className += ' ch'; sp.style.borderBottomColor = mau;
      if (!o.so) sp.style.background = mau + '2e';
      sp.title = o.ids.map((i) => theoId[i].thuoc_tinh).join(', ');
    }
    v.append(sp);
  });
}

function veHuongDan() {
  const b = bai(), p = $('hd'), ds = DL.thuoc_tinh[b.nhom];
  p.textContent = '';
  p.append(e('button', {txt: 'Đóng', onclick: () => { p.style.display = 'none'; }}));
  p.append(e('h2', {txt: 'Thuộc tính của nhóm bài đang mở (' + b.ten_mau + ')'}));
  const bang = e('table', {}, e('tr', {}, e('th', {txt: 'Phím'}), e('th', {txt: 'Mã'}), e('th', {txt: 'Ý nghĩa'}), e('th', {txt: 'Dấu hiệu'})));
  ds.forEach((x, i) => bang.append(e('tr', {}, e('td', {txt: String(i + 1)}), e('td', {txt: x.ma}), e('td', {txt: x.y_nghia}), e('td', {txt: x.dau_hieu}))));
  p.append(bang);
  [['5 quy tắc', DL.huong_dan.quy_tac_html], ['Tiêu chí gắn điều kiện', DL.huong_dan.tieu_chi_html]].forEach(([ten, h]) => {
    const dt = e('details', {open: true}, e('summary', {txt: ten}));
    const kh = e('div', {}); kh.innerHTML = h; dt.append(kh); p.append(dt);
  });
}

function veCanhBao(d, khung) {
  khung.textContent = '';
  kiemDong(d, bai()).forEach((c) => khung.append(e('div', {txt: '⚠️ ' + c.msg})));
}

function veDong(d) {
  const b = bai(), mau = MAU[d.thuoc_tinh] || '#888';
  const sel = e('select', {}), ta = e('textarea', {placeholder: 'Tên sản phẩm + thuộc tính + con số + điều kiện, đúng như bài nói', value: d.tuyen_bo});
  b.ds_tt.forEach((m) => sel.append(e('option', {value: m, txt: m, selected: m === d.thuoc_tinh})));
  const ghi = e('input', {type: 'text', placeholder: 'ghi_chu (không bắt buộc)', value: d.ghi_chu});
  const cb = e('div', {cls: 'canh-bao'});
  const kung = e('div', {cls: 'dong', id: 'dong-' + d.id}, e('div', {cls: 'goc', txt: d.cau_goc}),
    e('div', {cls: 'hang'}, sel, e('button', {txt: 'Chèn tên sản phẩm', title: 'Chèn "' + b.ten_mau + '" vào đầu ô tuyên bố', onclick: () => {
      if (bo(ta.value).startsWith(bo(b.ten_mau))) return;
      ta.value = b.ten_mau + (ta.value ? ' ' + ta.value : ''); ta.dispatchEvent(new Event('input')); ta.focus();
    }}), e('button', {txt: 'Đặt lại nháp', title: 'Điền lại bản nháp tự động từ câu gốc', onclick: () => {
      const bn = nhapTuyenBo(d.cau_goc, b.ten_mau);
      if (ta.value !== bn && !confirm('Ô tuyên bố đang khác bản nháp. Thay bằng bản nháp tự động?')) return;
      ta.value = bn; d.tuyen_bo = bn; d.nhap = true; luu(); lam();
    }}), e('button', {txt: 'Đã rà, giữ nguyên', title: 'Bản nháp đã đúng quy tắc 2, 3: bỏ đánh dấu nháp mà không sửa chữ', onclick: () => {
      if (!d.tuyen_bo.trim()) return;
      d.nhap = false; luu(); lam();
    }}), e('button', {cls: 'xoa', txt: 'Xóa', onclick: () => {
      if (!confirm('Xóa dòng này?\n' + d.cau_goc.slice(0, 120))) return;
      tBai(b.ma).dong = tBai(b.ma).dong.filter((x) => x.id !== d.id); luu(); veBai(); }})),
    ta, e('div', {cls: 'hang'}, ghi), cb);
  kung.style.borderLeftColor = mau;
  const lam = () => { kung.classList.toggle('thieu', !d.tuyen_bo.trim()); ta.classList.toggle('nhap', d.nhap === true); veCanhBao(d, cb); veTrai(); veTienDo(); veTrangThaiBai(); };
  sel.onchange = () => { d.thuoc_tinh = sel.value; kung.style.borderLeftColor = MAU[d.thuoc_tinh] || '#888'; luu(); veGiua(); lam(); };
  ta.oninput = () => {
    d.tuyen_bo = ta.value;
    if (d.nhap && ta.value !== nhapTuyenBo(d.cau_goc, b.ten_mau)) d.nhap = false;
    luu(); lam();
  };
  ghi.oninput = () => { d.ghi_chu = ghi.value; luu(); };
  kung.classList.toggle('thieu', !d.tuyen_bo.trim()); ta.classList.toggle('nhap', d.nhap === true); veCanhBao(d, cb);
  return kung;
}

function veTrangThaiBai() {
  const b = bai(), t = tBai(b.ma);
  $('tt-bai').textContent = t.dong.length + ' dòng' + (thieuBai(b) ? ', ' + thieuBai(b) + ' thiếu tuyên bố' : '');
  $('nut-xong').textContent = t.xong === 'co' ? 'Mở lại bài (đã xong)' : 'Xong bài';
  $('nut-khong').textContent = t.xong === 'khong' ? 'Mở lại bài (không có câu)' : 'Bài không có câu nào';
}

function veDongBai() {
  const ds = $('ds-dong'), b = bai(), dongs = sapDong(tBai(b.ma).dong);
  ds.textContent = '';
  if (!dongs.length) ds.append(e('div', {cls: 'rong', txt: 'Chưa có dòng nào. Bôi đen một câu trong bài rồi bấm thuộc tính.'}));
  dongs.forEach((d) => ds.append(veDong(d)));
}

function veBai() { veGiua(); veDongBai(); veTrangThaiBai(); veTrai(); veTienDo(); }

function chonBai(ma) {
  gd.chon = ma; luuGd(); an(); veHuongDan(); veBai();
  $('van-bao').scrollTop = 0; $('ds-dong').scrollTop = 0;
}

/* ---- Thanh nổi chọn thuộc tính ---- */
let dangChon = null;
function an() { $('thanh-chon').style.display = 'none'; dangChon = null; }
function viTriChon() {
  const sel = window.getSelection();
  if (!sel || !sel.rangeCount || sel.isCollapsed) return null;
  const r = sel.getRangeAt(0).cloneRange(), v = $('van'), vr = document.createRange();
  vr.selectNodeContents(v);  // kéo quá ra ngoài khung bài thì cắt vùng chọn về trong bài
  if (r.compareBoundaryPoints(Range.START_TO_START, vr) < 0) r.setStart(vr.startContainer, vr.startOffset);
  if (r.compareBoundaryPoints(Range.END_TO_END, vr) > 0) r.setEnd(vr.endContainer, vr.endOffset);
  if (r.collapsed || !v.contains(r.startContainer) || !v.contains(r.endContainer)) return null;
  const a = document.createRange(); a.selectNodeContents(v); a.setEnd(r.startContainer, r.startOffset);
  const bd = a.toString().length, kt = bd + r.toString().length, van = bai().van_ban;
  if (van.slice(bd, kt) !== r.toString()) return null;
  const c = catKhoangTrang(van, bd, kt);
  return c ? {bd: c.bd, kt: c.kt, rect: r.getBoundingClientRect()} : null;
}
function hienThanh() {
  const c = viTriChon();
  if (!c) { an(); return; }
  dangChon = c;
  const tc = $('thanh-chon'); tc.textContent = '';
  bai().ds_tt.forEach((m, i) => {
    const nut = e('button', {}, e('b', {txt: String(i + 1)}), m);
    nut.style.background = MAU[m] || '#555';
    nut.onmousedown = (ev) => ev.preventDefault();
    nut.onclick = () => themDong(m);
    tc.append(nut);
  });
  tc.style.display = 'flex';
  const h = tc.offsetHeight;
  tc.style.left = Math.max(4, Math.min(window.innerWidth - 530, c.rect.left)) + 'px';
  tc.style.top = (c.rect.top - h - 6 > 4 ? c.rect.top - h - 6 : c.rect.bottom + 6) + 'px';
}
function themDong(m) {
  if (!dangChon) return;
  const b = bai(), d = {id: 'd' + st.tiep, t: st.tiep, bd: dangChon.bd, cau_goc: b.van_ban.slice(dangChon.bd, dangChon.kt), thuoc_tinh: m, tuyen_bo: '', ghi_chu: '', nhap: true};
  d.tuyen_bo = nhapTuyenBo(d.cau_goc, b.ten_mau);
  st.tiep++;
  tBai(b.ma).dong.push(d);
  if (tBai(b.ma).xong === 'khong') tBai(b.ma).xong = '';
  luu(); window.getSelection().removeAllRanges(); an(); veBai();
  const kt = document.querySelector('#dong-' + d.id);
  if (kt) { kt.scrollIntoView({block: 'nearest'}); kt.querySelector('textarea').focus(); }
}
document.addEventListener('mouseup', (ev) => { if (!$('thanh-chon').contains(ev.target)) setTimeout(hienThanh, 0); });  // thả chuột ngoài khung bài vẫn hiện thanh
$('van').addEventListener('keyup', (ev) => { if (ev.shiftKey) hienThanh(); });
document.addEventListener('mousedown', (ev) => { if (!$('thanh-chon').contains(ev.target)) an(); });
document.addEventListener('keydown', (ev) => {
  if (ev.key === 'Escape') { an(); $('hd').style.display = 'none'; return; }
  if (!dangChon || ev.ctrlKey || ev.metaKey || ev.altKey || /^(INPUT|TEXTAREA|SELECT)$/.test((ev.target.tagName || ''))) return;
  const i = parseInt(ev.key, 10);
  if (i >= 1 && i <= bai().ds_tt.length) { ev.preventDefault(); themDong(bai().ds_tt[i - 1]); }
});

/* ---- Nút trên đầu trang ---- */
$('loc').onchange = veTrai;
$('chk-so').checked = !!gd.so;
$('chk-so').onchange = () => { gd.so = $('chk-so').checked; luuGd(); veGiua(); };
$('nut-hd').onclick = () => { const p = $('hd'); p.style.display = p.style.display === 'block' ? 'none' : 'block'; };
$('nut-tiep').onclick = () => {
  const k = BAI.findIndex((b) => b.ma === gd.chon);
  for (let i = 1; i <= BAI.length; i++) { const b = BAI[(k + i) % BAI.length]; if (!tBai(b.ma).xong) { chonBai(b.ma); return; } }
  alert('Mọi bài đã xong.');
};
$('nut-xong').onclick = () => {
  const t = tBai(gd.chon);
  if (t.xong === 'co') t.xong = '';
  else if (!t.dong.length) { alert('Bài chưa có dòng nào. Nếu bài không có câu nào cần tách, bấm "Bài không có câu nào".'); return; }
  else t.xong = 'co';
  luu(); veBai();
};
$('nut-khong').onclick = () => {
  const t = tBai(gd.chon);
  if (t.xong === 'khong') t.xong = '';
  else if (t.dong.length) { alert('Bài đang có ' + t.dong.length + ' dòng. Xóa hết dòng trước, hoặc bấm "Xong bài".'); return; }
  else t.xong = 'khong';
  luu(); veBai();
};
function taiXuong(ten, noi, kieu) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([noi], {type: kieu})); a.download = ten;
  document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
}
$('nut-csv').onclick = () => {
  const thieu = BAI.reduce((s, b) => s + thieuBai(b), 0), chua = BAI.filter((b) => !tBai(b.ma).xong).length;
  const nhap = BAI.reduce((s, b) => s + tBai(b.ma).dong.filter((d) => d.nhap === true).length, 0);
  if ((thieu || chua || nhap) && !confirm('Còn ' + thieu + ' dòng thiếu tuyên bố, ' + nhap + ' dòng còn là bản nháp chưa sửa và ' + chua +
      ' bài chưa xong. Vẫn xuất CSV?')) return;
  taiXuong(DL.tep_csv, taoCsv(BAI, st, DL.cot_csv), 'text/csv;charset=utf-8');
};
$('nut-sao-luu').onclick = () => taiXuong('sao_luu_' + KHOA + '.json', JSON.stringify({phien_ban: 1, khoa: KHOA, bai: st.bai}, null, 1), 'application/json');
$('nut-nhap').onclick = () => $('tep-nhap').click();
$('tep-nhap').onchange = () => {
  const f = $('tep-nhap').files[0]; $('tep-nhap').value = '';
  if (!f) return;
  f.text().then((chu) => {
    let du; try { du = JSON.parse(chu); } catch (x) { alert('Tệp không phải JSON.'); return; }
    const kq = nhapTrangThai(du, BAI), so = BAI.reduce((s, b) => s + kq.st.bai[b.ma].dong.length, 0);
    if (!confirm('Khôi phục ' + so + ' dòng, thay toàn bộ dữ liệu hiện có. Bỏ qua ' + kq.boQua + ' dòng' +
        (kq.baiLa.length ? ' (mã bài không có trong trang: ' + kq.baiLa.join(', ') + ')' : '') + '. Tiếp tục?')) return;
    st = kq.st; luu(); veBai(); veHuongDan();
  });
};

$('chk-so').checked = !!gd.so;
veHuongDan(); veBai();
if (!luuDuoc) $('chu-tien-do').title = 'Trình duyệt đang chặn localStorage: dữ liệu không được nhớ, hãy dùng Sao lưu JSON.';
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sinh công cụ tách tuyên bố bằng tay (HTML tự chứa) cho tập kiểm tra.")
    ap.add_argument("--doc", type=Path, default=TEP_DOC, help="tệp bài để đọc (mặc định data/tuyen_bo/doc_kiem_tra.md)")
    ap.add_argument("--ra", type=Path, default=TEP_RA, help="HTML ghi ra (không ghi đè tệp đã có)")
    ap.add_argument("--khoa", default=KHOA_MAC_DINH, help="khóa localStorage")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if args.ra.exists():
        thoat(f"tệp đã tồn tại, không ghi đè: {args.ra}; hãy chọn --ra khác hoặc xóa tệp cũ")
    du_lieu = nap_du_lieu(args.doc, args.khoa)
    html_ra = dung_html(du_lieu)
    args.ra.parent.mkdir(parents=True, exist_ok=True)
    try:
        with args.ra.open("x", encoding="utf-8", newline="\n") as f:
            f.write(html_ra)
    except FileExistsError:
        thoat(f"tệp đã tồn tại, không ghi đè: {args.ra}; hãy chọn --ra khác hoặc xóa tệp cũ")
    theo_mau = {}
    for b in du_lieu["bai"]:
        theo_mau[b["ma_mau"]] = theo_mau.get(b["ma_mau"], 0) + 1
    print(f"đã sinh {args.ra}: {len(du_lieu['bai'])} bài, {len(theo_mau)} mẫu ({', '.join(f'{m} {n}' for m, n in theo_mau.items())}), "
          f"{args.ra.stat().st_size / 1024:.0f} KB, khóa {args.khoa}")


if __name__ == "__main__":
    main()
