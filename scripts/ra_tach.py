"""Bước 16, QĐ1: hỗ trợ rà tách. Với mỗi tuyên bố trong data/tuyen_bo/thu.jsonl, liệt kê các cụm điều kiện, từ khẳng định
và cụm phủ nhiều giá trị CÓ trong câu gốc (cau_goc) mà KHÔNG có trong tuyên bố (tuyen_bo). Ghi data/tuyen_bo/ra_tach_thu.md.

Người thực hiện dùng danh sách này làm chỗ để xem, rồi tự quyết từng chỗ theo bốn tiêu chí gắn điều kiện (hướng dẫn gán nhãn
mục 2, data/tuyen_bo/huong_dan_tach_tay.md). Script chỉ so chuỗi một cách tất định: không đề xuất cách sửa, không nêu nhãn,
không gọi LLM. Không thấy cụm nào ở một tuyên bố không có nghĩa tuyên bố đủ điều kiện (cụm ngoài cấu hình không được dò), và
thấy cụm không có nghĩa tuyên bố sai tiêu chí (cụm có thể thuộc con số khác của cùng câu gốc, tiêu chí 3).

Dò cái gì (cùng nguồn với phụ lục mục 13 và mục 6.2, 6.8 của data/huong_dan_gan_nhan.md):
- Cụm điều kiện: mọi cụm (tu_tai_lieu và hieu_biet_chung) trong data/cau_hinh/chung.yaml (kieu_gia_tri, tu_goi_muc_cao,
  dieu_kien_so.cum_quan_he) và cach_dien_dat của yaml nhóm ứng với tiền tố ma_mau (dt: dien_thoai.yaml, tn: tai_nghe.yaml,
  dh: dong_ho.yaml). Mặc định chỉ xét các điều kiện của thuộc tính ghi trên tuyên bố (dieu_kien_bat_buoc của thuộc tính trong yaml
  nhóm; kieu_gia_tri luôn xét; tu_goi_muc_cao khi thuộc tính có che_do_hien_thi; cum_quan_he khi thuộc tính có điều kiện dạng
  số); --khong-loc-thuoc-tinh thì xét mọi điều kiện của nhóm. Cụm "ngu_canh_khong_quyet_dinh" là ngữ cảnh, không dò. Câu gốc và
  tuyên bố đều là chữ của quảng cáo, nên giá trị có khóa phia: tai_lieu (chỉ đọc ở phía tài liệu, ví dụ "Sử dụng liên tục" của
  Xiaomi 15T) bị bỏ; giá trị phia: tuyen_bo (ví dụ chua_ro_hoat_dong: "liên tục") được dò.
- Từ khẳng định: các từ ở mục 6.2 (nhóm chắc chắn và nhóm mức sàn "hơn / trên / không dưới <số>", "<số> trở lên", chỉ khi đứng
  liền con số), đọc từ hướng dẫn bằng tao_cong_cu_gan_nhan.tu_khang_dinh; dạng phủ định trong tu_khang_dinh.bo_qua_khi_co của
  chung.yaml ("không đảm bảo"...) bị bỏ qua. Tên tính năng như "Luôn Bật" vẫn được liệt kê: tiêu chí 3 do người rà quyết.
- Cụm phủ nhiều giá trị (mục 6.8, chung.yaml cum_phu.mau): "mọi điều kiện X", "mọi chế độ", "mọi hoạt động", "bất kể X",
  "dù A hay B", "cho cả A và B".

Cách so: cả hai chuỗi chuẩn hóa NFC, bỏ dấu ngoặc đơn, gộp khoảng trắng, không phân biệt hoa thường; cụm khớp khi hai đầu không
dính chữ hay số khác. Chỉ giữ cụm dài nhất ở mỗi chỗ (cụm nằm gọn trong cụm dài hơn thì bỏ). Một giá trị điều kiện (ví dụ
che_do_chong_on=bat) coi là có trong tuyên bố nếu bất kỳ cụm nào của giá trị đó có trong tuyên bố, nên "bật ANC" ở câu gốc không
bị liệt kê khi tuyên bố ghi "bật chống ồn". Từ khẳng định so theo chữ khớp; cụm phủ coi là có nếu tuyên bố có cụm cùng kiểu.

Chạy: .venv/Scripts/python.exe scripts/ra_tach.py [--ra data/tuyen_bo/ra_tach_thu.md] [--khong-loc-thuoc-tinh]

Cách sửa một tuyên bố (script này không sửa gì; data/tuyen_bo/thu.jsonl do scripts/chuyen_tuyen_bo.py ghi từ
data/tuyen_bo/thu_nhap.csv, chạy lại trên CSV hiện tại cho ra đúng từng byte của thu.jsonl):
1. Mở data/tuyen_bo/thu_nhap.csv bằng Excel hoặc Google Sheets (UTF-8). Dòng n của CSV (dòng 1 là tiêu đề, dòng trống bỏ qua)
   ứng với tb-{n-1:05d}, vì chuyen_tuyen_bo.py đánh mã theo thứ tự dòng. Tìm dòng bằng ma_qc và cau_goc.
2. Sửa cột tuyen_bo. Giữ nguyên cột cau_goc (chuyen_tuyen_bo.py kiểm câu gốc có nguyên văn trong bài). Ghi vào cột ghi_chu:
   tach_sua=<sửa gì>, ví dụ tach_sua=thêm chế độ nguồn; đã có ghi chú thì nối thêm bằng "; ".
3. Tách thêm một tuyên bố (tiêu chí 4): thêm dòng ở CUỐI CSV (chép ma_qc và cau_goc, điền tuyen_bo và thuoc_tinh, ghi_chu bắt đầu
   bằng tach_sua=). Đừng chèn giữa CSV: mã tb-… của các dòng sau sẽ dịch, lệch với nhãn lượt 1 (data/nhan/thu.jsonl,
   thu_luot1.jsonl) và với kết quả B0, Recall@k đã ghi theo mã.
4. Lưu CSV (UTF-8) rồi chạy
       .venv/Scripts/python.exe scripts/chuyen_tuyen_bo.py data/tuyen_bo/thu_nhap.csv data/tuyen_bo/thu.jsonl
   Script kiểm lỗi (câu gốc có trong bài, thuộc tính có trong cấu hình, tuyên bố không trùng trong cùng bài) rồi mới ghi; có lỗi
   thì không ghi gì.
5. Tuyên bố được nhúng vào trang gán nhãn và đi vào B0: chạy lại scripts/tao_cong_cu_gan_nhan.py để sinh lại trang, scripts/chay_b0.py
   (bộ nhớ đệm giữ phần không đổi) và scripts/do_recall.py; chạy lại scripts/ra_tach.py để cập nhật danh sách này.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import unicodedata

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tao_cong_cu_gan_nhan as tc  # noqa: E402

GOC = Path(__file__).resolve().parents[1]
TEP_TUYEN_BO = GOC / "data" / "tuyen_bo" / "thu.jsonl"
THU_MUC_CAU_HINH = GOC / "data" / "cau_hinh"
TEP_RA = GOC / "data" / "tuyen_bo" / "ra_tach_thu.md"
YAML_NHOM = {"dt": "dien_thoai", "tn": "tai_nghe", "dh": "dong_ho"}

NHAN_TU_KHANG_DINH = "từ khẳng định"
NHAN_CUM_PHU = "cụm phủ"
# Cụm phủ nhiều giá trị (mục 6.8): mẫu như chung.yaml cum_phu.mau (tests/test_ra_tach.py kiểm hai bên cùng danh sách) -> biểu thức
# (áp lên chuỗi đã chuẩn hóa). Cụm chỉ lấy vài chữ quanh từ khóa để người rà thấy ngữ cảnh; "có trong tuyên bố" tính theo kiểu
# (mẫu), không theo đúng chữ.
CUM_PHU = {
    "mọi điều kiện X": r"mọi điều kiện(?:\s+[^\s,.;:!?]+){0,2}",
    "mọi chế độ": r"mọi chế độ",
    "mọi hoạt động": r"mọi hoạt động(?:\s+[^\s,.;:!?]+){0,3}",
    "bất kể X": r"bất kể(?:\s+[^\s,.;:!?]+){1,3}",
    "dù A hay B": r"dù\s+(?:[^\s,.;:!?]+\s+){1,4}?hay(?:\s+[^\s,.;:!?]+){1,3}",
    "cho cả A và B": r"cho cả\s+(?:[^\s,.;:!?]+\s+){1,4}?và(?:\s+[^\s,.;:!?]+){1,3}",
}
# Nhóm mức sàn của mục 6.2: cụm đứng liền con số. Khóa là cụm như hướng dẫn viết ("hơn <số>"), giá trị là biểu thức.
BIEU_THUC_MUC_SAN = {
    "hơn <số>": r"hơn\s+\d[\d.,]*",
    "trên <số>": r"trên\s+\d[\d.,]*",
    "không dưới <số>": r"không dưới\s+\d[\d.,]*",
    "<số> trở lên": r"\d[\d.,]*\s*[^\W\d_]{0,6}\s+trở lên",
}


def chuan(chu):
    """NFC, bỏ dấu ngoặc đơn, gộp khoảng trắng (giữ hoa thường để hiện lại đúng chữ; so bằng IGNORECASE)."""
    chu = unicodedata.normalize("NFC", chu or "")
    return " ".join(re.sub(r"[()]", " ", chu).split())


def doc_yaml(ten):
    return yaml.safe_load((THU_MUC_CAU_HINH / f"{ten}.yaml").read_text(encoding="utf-8"))


def _cum_cua(muc):
    """Mọi cụm (tu_tai_lieu rồi hieu_biet_chung) của một mục {tu_tai_lieu: [...], hieu_biet_chung: [...]}."""
    return list((muc or {}).get("tu_tai_lieu") or []) + list((muc or {}).get("hieu_biet_chung") or [])


def nhom_cum(nhom, thuoc_tinh=None, loc_thuoc_tinh=True):
    """[(mã giá trị, [cụm])] của các cụm điều kiện áp cho nhóm (tiền tố ma_mau) và thuộc tính.

    Mã giá trị: "<điều kiện>=<giá trị>" cho cach_dien_dat của yaml nhóm, "kieu_gia_tri=<giá trị>", "tu_goi_muc_cao",
    "cum_quan_he=<giá trị>" cho phần dùng chung. loc_thuoc_tinh: chỉ các điều kiện của thuộc tính (xem docstring đầu tệp).
    Giá trị phia: tai_lieu của cach_dien_dat không có trong kết quả (chỉ đọc ở phía tài liệu). Giá trị có chi_thuoc_tinh chỉ có
    khi thuoc_tinh nằm trong danh sách đó (khi lọc theo thuộc tính)."""
    chung, yaml_nhom = doc_yaml("chung"), doc_yaml(YAML_NHOM[nhom])
    cach = yaml_nhom["cach_dien_dat"]
    khoa = set(cach)
    if loc_thuoc_tinh and thuoc_tinh:
        khoa = set(yaml_nhom["thuoc_tinh"][thuoc_tinh].get("dieu_kien_bat_buoc") or {}) & set(cach)
    dang_so = any("gia_tri_so" in cach[k] for k in khoa)
    ra = [(f"kieu_gia_tri={gt}", _cum_cua(m)) for gt, m in chung["kieu_gia_tri"].items()]
    if not loc_thuoc_tinh or "che_do_hien_thi" in khoa:
        ra.append(("tu_goi_muc_cao", _cum_cua(chung["tu_goi_muc_cao"])))
    if not loc_thuoc_tinh or dang_so:
        ra += [(f"cum_quan_he={gt}", _cum_cua(m)) for gt, m in chung["dieu_kien_so"]["cum_quan_he"].items()]
    for dk, gts in cach.items():
        if dk in khoa:
            ra += [(f"{dk}={gt}", _cum_cua(m)) for gt, m in gts.items() if m.get("phia") != "tai_lieu"
                   and not (loc_thuoc_tinh and thuoc_tinh and m.get("chi_thuoc_tinh")
                            and thuoc_tinh not in m["chi_thuoc_tinh"])]
    return [(ma, cum) for ma, cum in ra if cum]


def _bieu_thuc_cum(cum):
    return re.compile(r"(?<!\w)" + re.escape(chuan(cum)) + r"(?!\w)", re.IGNORECASE)


def tim_cum_dieu_kien(van_ban, cac_nhom_cum):
    """[(vị trí đầu, vị trí cuối, chữ khớp, {mã giá trị})] các cụm điều kiện trong van_ban (đã chuẩn hóa), chỉ giữ cụm dài nhất."""
    theo_cum = {}
    for ma, ds in cac_nhom_cum:
        for cum in ds:
            theo_cum.setdefault(chuan(cum).casefold(), (cum, set()))[1].add(ma)
    khop = []
    for _, (cum, ma) in theo_cum.items():
        for m in _bieu_thuc_cum(cum).finditer(van_ban):
            khop.append((m.start(), m.end(), m.group(0), ma))
    return _giu_cum_dai_nhat(khop)


def _giu_cum_dai_nhat(khop):
    """Bỏ khớp nằm gọn trong một khớp dài hơn (khớp bằng nhau về vị trí thì gộp mã giá trị)."""
    gop = {}
    for dau, cuoi, chu, ma in khop:
        gop.setdefault((dau, cuoi), [chu, set()])[1] |= ma
    ra = []
    for (dau, cuoi), (chu, ma) in gop.items():
        if any(d <= dau and cuoi <= c and (d, c) != (dau, cuoi) for d, c in gop):
            continue
        ra.append((dau, cuoi, chu, ma))
    return sorted(ra)


def tim_tu_khang_dinh(van_ban, tu_khang_dinh, bo_qua):
    """[(vị trí, chữ khớp)] từ khẳng định trong van_ban: nhóm chắc chắn theo chữ, nhóm mức sàn khi đứng liền con số; bỏ qua
    chỗ nằm trong một cụm phủ định (bo_qua_khi_co)."""
    cam = [(m.start(), m.end()) for cum in bo_qua for m in _bieu_thuc_cum(cum).finditer(van_ban)]
    ra = []
    for tu in tu_khang_dinh["chac_chan"]:
        for m in _bieu_thuc_cum(tu).finditer(van_ban):
            if not any(d <= m.start() and m.end() <= c for d, c in cam):
                ra.append((m.start(), m.group(0)))
    for cum in tu_khang_dinh["muc_san"]:
        bt = BIEU_THUC_MUC_SAN.get(cum)
        if bt is None:
            raise SystemExit(f"mục 6.2 có cụm mức sàn '{cum}' mà {Path(__file__).name} chưa có biểu thức (BIEU_THUC_MUC_SAN)")
        ra += [(m.start(), m.group(0)) for m in re.finditer(r"(?<!\w)" + bt, van_ban, re.IGNORECASE)]
    return sorted(ra)


def tim_cum_phu(van_ban):
    """[(vị trí, kiểu, chữ khớp)] cụm phủ nhiều giá trị trong van_ban."""
    ra = []
    for kieu, bt in CUM_PHU.items():
        ra += [(m.start(), kieu, m.group(0)) for m in re.finditer(r"(?<!\w)" + bt, van_ban, re.IGNORECASE)]
    return sorted(ra)


def ra_tach_mot(tb, tu_khang_dinh, bo_qua, loc_thuoc_tinh=True):
    """{nhãn nhóm: [chữ khớp]} các cụm có trong cau_goc của tuyên bố tb mà không có trong tuyen_bo (xem docstring đầu tệp).
    Nhãn nhóm: "<điều kiện>=<giá trị>", "tu_goi_muc_cao", "kieu_gia_tri=…", "cum_quan_he=…", "từ khẳng định", "cụm phủ"."""
    goc, tuyen_bo = chuan(tb["cau_goc"]), chuan(tb["tuyen_bo"])
    cac = nhom_cum(tb["ma_mau"].split("-")[0], tb.get("thuoc_tinh"), loc_thuoc_tinh)
    ket_qua = {}

    def them(nhan, chu):
        ds = ket_qua.setdefault(nhan, [])
        if chu.casefold() not in {x.casefold() for x in ds}:
            ds.append(chu)

    co_trong_tuyen_bo = set()  # mã giá trị có ít nhất một cụm trong tuyên bố
    for _, _, _, ma in tim_cum_dieu_kien(tuyen_bo, cac):
        co_trong_tuyen_bo |= ma
    for _, _, chu, ma in tim_cum_dieu_kien(goc, cac):
        for m in sorted(ma - co_trong_tuyen_bo):
            them(m, chu)
    chu_tuyen_bo = {chu.casefold() for _, chu in tim_tu_khang_dinh(tuyen_bo, tu_khang_dinh, bo_qua)}
    for _, chu in tim_tu_khang_dinh(goc, tu_khang_dinh, bo_qua):
        if chu.casefold() not in chu_tuyen_bo:
            them(NHAN_TU_KHANG_DINH, chu)
    kieu_tuyen_bo = {kieu for _, kieu, _ in tim_cum_phu(tuyen_bo)}
    for _, kieu, chu in tim_cum_phu(goc):
        if kieu not in kieu_tuyen_bo:
            them(NHAN_CUM_PHU, chu)
    return ket_qua


def _thu_tu_nhan(nhan):
    """Điều kiện (theo tên) trước, rồi từ khẳng định, rồi cụm phủ."""
    return (2 if nhan == NHAN_CUM_PHU else 1 if nhan == NHAN_TU_KHANG_DINH else 0, nhan)


def mo_ta_cum(ket_qua):
    """Chuỗi một ô của bảng: "nhóm: “cụm”, “cụm”; nhóm: …"; "–" nếu không có gì."""
    if not ket_qua:
        return "–"
    return "; ".join(f"{nhan}: " + ", ".join(f"“{c}”" for c in ket_qua[nhan]) for nhan in sorted(ket_qua, key=_thu_tu_nhan))


def _o(chu):
    """Ô bảng markdown: thoát dấu | và gộp xuống dòng."""
    return " ".join(str(chu).split()).replace("|", "\\|")


def dung_bao_cao(tuyen_bo, ket_qua, loc_thuoc_tinh=True):
    """Nội dung data/tuyen_bo/ra_tach_thu.md: tiêu đề, giải thích ngắn, bảng một dòng mỗi tuyên bố, tóm tắt."""
    co = [t for t in tuyen_bo if ket_qua[t["id"]]]
    dong = [
        "# Rà tách bộ thử: cụm có trong câu gốc mà không có trong tuyên bố",
        "",
        "Sinh bằng `scripts/ra_tach.py` từ `data/tuyen_bo/thu.jsonl` và `data/cau_hinh/*.yaml` (cụm của phụ lục mục 13), từ khẳng "
        "định (mục 6.2) và cụm phủ nhiều giá trị (mục 6.8) của `data/huong_dan_gan_nhan.md`. Chỉ so chuỗi: không đề xuất cách sửa, "
        "không nêu nhãn. Người thực hiện tự quyết từng chỗ theo bốn tiêu chí gắn điều kiện (mục 2 của hướng dẫn).",
        "",
        "- Cụm thấy ở đây có thể thuộc con số khác của cùng câu gốc hoặc là tên tính năng (tiêu chí 3); không thấy cụm nào không "
        "có nghĩa tuyên bố đủ điều kiện, vì cụm ngoài cấu hình không được dò.",
        "- " + ("Chỉ xét các điều kiện của thuộc tính ghi trên tuyên bố." if loc_thuoc_tinh else "Xét mọi điều kiện của nhóm sản phẩm."),
        f"- {len(co)} / {len(tuyen_bo)} tuyên bố có cụm được liệt kê.",
        "",
        "| Mã | Tuyên bố | Câu gốc | Cụm có trong câu gốc, không có trong tuyên bố |",
        "|---|---|---|---|",
    ]
    for t in tuyen_bo:
        dong.append(f"| {t['id']} | {_o(t['tuyen_bo'])} | {_o(t['cau_goc'])} | {_o(mo_ta_cum(ket_qua[t['id']]))} |")
    return "\n".join(dong) + "\n"


def chay(tep_tuyen_bo=TEP_TUYEN_BO, tep_ra=TEP_RA, loc_thuoc_tinh=True):
    """Đọc tuyên bố và hướng dẫn, ghi tep_ra; trả về (danh sách tuyên bố, {id: kết quả}, số tuyên bố có cụm)."""
    tuyen_bo = [json.loads(d) for d in Path(tep_tuyen_bo).read_text(encoding="utf-8-sig").splitlines() if d.strip()]
    tu_khang_dinh = tc.tu_khang_dinh(tc.doc_huong_dan())
    bo_qua = doc_yaml("chung")["tu_khang_dinh"].get("bo_qua_khi_co") or []
    ket_qua = {t["id"]: ra_tach_mot(t, tu_khang_dinh, bo_qua, loc_thuoc_tinh) for t in tuyen_bo}
    Path(tep_ra).write_text(dung_bao_cao(tuyen_bo, ket_qua, loc_thuoc_tinh), encoding="utf-8", newline="\n")
    return tuyen_bo, ket_qua, sum(1 for v in ket_qua.values() if v)


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Rà tách: cụm có trong câu gốc mà không có trong tuyên bố (Bước 16, QĐ1).")
    ap.add_argument("--tuyen-bo", type=Path, default=TEP_TUYEN_BO, help="mặc định data/tuyen_bo/thu.jsonl")
    ap.add_argument("--ra", type=Path, default=TEP_RA, help="mặc định data/tuyen_bo/ra_tach_thu.md")
    ap.add_argument("--khong-loc-thuoc-tinh", action="store_true", help="xét mọi điều kiện của nhóm, không chỉ của thuộc tính")
    args = ap.parse_args(argv)
    if not args.tuyen_bo.exists():
        sys.exit(f"không thấy tệp {args.tuyen_bo}")
    tuyen_bo, _, so_co = chay(args.tuyen_bo, args.ra, not args.khong_loc_thuoc_tinh)
    print(f"đã ghi {args.ra}: {so_co} / {len(tuyen_bo)} tuyên bố có cụm được liệt kê")


if __name__ == "__main__":
    main()
