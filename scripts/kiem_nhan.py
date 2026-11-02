"""Bước 13, 16: kiểm tệp nhãn chuẩn do người gán xuất từ công cụ (data/nhan/thu_luot2.jsonl, thu_luot1.jsonl) và in tóm tắt.

Kiểm: mỗi tuyên bố có đúng một nhãn, không có mã lạ; dong_d (dòng D đã dừng ở, hướng dẫn mục 7) thuộc D1..D6 và nhãn
khớp dòng (D1, D1a, D1b, D6: CHUA_DU; D2, D4: LECH; D3: DUNG; D5: SAI); nhãn và loại biến đổi hợp lệ theo hướng dẫn (mục 8:
LECH luôn có loại; SAI chỉ doi_gia_tri, doi_bo_phan hoặc doi_phien_ban; DUNG và CHUA_DU để trống; D2 thì loại là
doi_kieu_gia_tri); tai_lieu_mau_thuan là true khi và chỉ khi dòng D1b (mục 4); D1 thì bằng chứng và câu trích để trống;
ghi chú: mỗi khóa của mac_dinh= phải là khóa ghi được của thuộc tính ở bảng mục 5 (trừ khóa "như hãng công bố") hoặc
ngoai_bang (mục 6.7 ý 4, QĐ10); mac_dinh=<khóa> của một điều kiện "không có mặc định" (mục 5) thì phải dừng ở D1a, D1a phải ghi nguyên nhân
(mac_dinh=<khóa không có mặc định> hoặc chua_xac_dinh=<cụm>; chỉ ghi khóa có mặc định là sai), D2 phải ghi khang_dinh=<từ>
với từ có trong mục 6.2; lý do không còn chỗ {…} của mẫu câu và không chép mã đoạn <ma_mau>#<số> vào ngoặc kép của câu trích;
mã bằng chứng có trong data/nguon/<ma_mau>/doan.jsonl của đúng mẫu; mỗi phần của câu trích (tách bằng " | ") là
chuỗi con của noi_dung, của noi_dung_goc hoặc của một chu_thich của các đoạn bằng chứng (sau khi chuẩn hóa NFC và gộp
khoảng trắng); lý do, người gán, số giây; luot (mặc định: mọi dòng cùng một lượt; --luot N thì mọi dòng phải là lượt N);
giay_nghi (tùy chọn, số giây đồng hồ đứng vì không thao tác) là số nguyên không âm. Có lỗi thì liệt kê từng lỗi và thoát mã 1.

Ngoài lỗi còn in mục "Nhắc" (không tính là lỗi, không đổi mã thoát): loại bo_dieu_kien mà ghi chú không có mac_dinh=; dòng D1
mà ghi chú có mac_dinh=; câu trích không có đơn vị của thuộc tính (cột Đơn vị mục 6.1).

Các kiểm này chỉ bắt chỗ các ô người gán điền mâu thuẫn nhau hoặc trái quy tắc, dựa vào nhóm (tiền tố ma_mau) và thuộc tính
ghi sẵn trên tuyên bố; không đọc nội dung tuyên bố để đoán nhãn hay dòng D. Bảng dòng D, thông báo lỗi, lời nhắc và các bảng
đọc từ hướng dẫn (khóa "không có mặc định", cách hiểu mặc định, từ khẳng định, đơn vị) lấy từ scripts/tao_cong_cu_gan_nhan.py
(cùng nguồn với công cụ HTML). Luật ở đây và khối LUAT_KIEM của công cụ HTML là một; sửa một bên thì sửa bên kia
(tests/test_tao_cong_cu_gan_nhan.py chạy khối đó trong node và so với script này).

noi_dung đã bỏ số chú thích của trang hãng ("20 phút6" -> "20 phút"), noi_dung_goc là bản trước khi bỏ. Câu trích chép
theo noi_dung (chữ hiển thị trên trang gán nhãn) là cách đúng, nhưng nhãn đã lưu trước đó có thể chép kèm số chú thích nên
noi_dung_goc cũng được chấp nhận.

Chạy:
    .venv/Scripts/python.exe scripts/kiem_nhan.py data/nhan/thu_luot2.jsonl [data/tuyen_bo/thu.jsonl] [--luot 2]
Lượt 1 (nhãn theo hướng dẫn bản 1) kiểm bằng luật bản 2 sẽ báo nhiều lỗi mới; đó là để biết luật mới bắt gì, không phải
lý do sửa nhãn lượt 1.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import statistics
import sys
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tao_cong_cu_gan_nhan as tc  # noqa: E402

GOC = Path(__file__).resolve().parents[1]
THU_MUC_NGUON = GOC / "data" / "nguon"
TEP_TUYEN_BO = GOC / "data" / "tuyen_bo" / "thu.jsonl"

NHAN = ("DUNG", "SAI", "LECH", "CHUA_DU")
LOAI_LECH = ("bo_dieu_kien", "doi_dieu_kien", "doi_bo_phan", "doi_phien_ban", "doi_kieu_gia_tri")
# Nhãn SAI chỉ ghi doi_gia_tri, hoặc doi_bo_phan / doi_phien_ban khi gán nhầm bộ phận, phiên bản mà không trùng số nào.
LOAI_SAI = ("doi_gia_tri", "doi_bo_phan", "doi_phien_ban")
LOAI_TAT_CA = LOAI_LECH + ("doi_gia_tri",)
# Dòng D và bảng suy nhãn, thông báo: một nguồn với công cụ HTML (scripts/tao_cong_cu_gan_nhan.py).
MA_DONG_D = tc.MA_DONG_D
NHAN_THEO_DONG = tc.NHAN_THEO_DONG
LOAI_THEO_DONG = tc.LOAI_THEO_DONG
DONG_TICK_MAU_THUAN = tc.DONG_TICK_MAU_THUAN
THONG_BAO = tc.THONG_BAO
NHAC = tc.NHAC
# Chỗ giữ chỗ của mẫu câu lý do (hướng dẫn mục 8) mà người gán quên thay.
GIU_CHO = re.compile(r"\{[^{}]*\}")
# Thứ tự trường của một dòng nhãn (hướng dẫn mục 8); công cụ HTML xuất đúng thứ tự này.
TRUONG = ("id", "nhan", "dong_d", "loai", "bang_chung", "trich", "ly_do", "nguoi_gan", "luot", "giay",
          "tai_lieu_mau_thuan", "ghi_chu")
# Trường tùy chọn (công cụ HTML xuất sau ghi_chu): giay_nghi = số giây đồng hồ đứng vì không thao tác quá 3 phút, ghi riêng
# với giay. Bản ghi không có trường này vẫn hợp lệ.
TRUONG_TUY_CHON = ("giay_nghi",)
TACH_TRICH = " | "
# Mục "ten=giá trị" của ghi chú, các mục cách nhau "; " (cùng biểu thức với công cụ HTML): mac_dinh=<khóa>,<khóa>;
# khang_dinh=<từ>; chua_xac_dinh=<cụm>.
MAC_DINH = re.compile(r"(?:^|;\s*)" + tc.MUC_MAC_DINH + r"=([^;]*)")
KHANG_DINH = re.compile(r"(?:^|;\s*)" + tc.MUC_KHANG_DINH + r"=([^;]*)")
CHUA_XAC_DINH = re.compile(r"(?:^|;\s*)" + tc.MUC_CHUA_XAC_DINH + r"=([^;]*)")
# Mã đoạn nằm trong ngoặc kép của lý do (biểu thức lấy từ công cụ HTML, cùng chuỗi với trang).
NGOAC_KEP = re.compile(tc.RE_NGOAC_KEP)
MA_DOAN = re.compile(tc.RE_MA_DOAN)
_QUY_TAC = None
# Cùng tập ký tự khoảng trắng với regex \s của JavaScript, để công cụ HTML và script này chuẩn hóa như nhau.
KHOANG_TRANG = re.compile("[\\t\\n\\v\\f\\r    -     　﻿]+")


def chuan_hoa(chuoi):
    """NFC, gộp mọi dãy khoảng trắng thành một dấu cách, bỏ khoảng trắng hai đầu."""
    return KHOANG_TRANG.sub(" ", unicodedata.normalize("NFC", chuoi)).strip()


def lay_mac_dinh(ghi_chu):
    """Các khóa sau mac_dinh= trong ghi chú (cách nhau bằng dấu phẩy); [] nếu không có mục mac_dinh."""
    m = MAC_DINH.search(ghi_chu)
    return [x.strip() for x in m.group(1).split(",") if x.strip()] if m else []


def lay_chua_xac_dinh(ghi_chu):
    """Cụm sau chua_xac_dinh= trong ghi chú (chuỗi đã bỏ khoảng trắng hai đầu); "" nếu không có mục này."""
    m = CHUA_XAC_DINH.search(ghi_chu)
    return m.group(1).strip() if m else ""


def lay_khang_dinh(ghi_chu):
    """Các từ sau khang_dinh= trong ghi chú (cách nhau bằng dấu phẩy); [] nếu không có mục khang_dinh."""
    m = KHANG_DINH.search(ghi_chu)
    return [x.strip() for x in m.group(1).split(",") if x.strip()] if m else []


def ma_doan_trong_ngoac(ly_do):
    """Mã đoạn <ma_mau>#<số> đầu tiên nằm trong ngoặc kép của lý do; "" nếu không có."""
    for m in NGOAC_KEP.finditer(ly_do):
        x = MA_DOAN.search(m.group(1))
        if x:
            return x.group(0)
    return ""


def quy_tac_huong_dan():
    """Các bảng đọc từ hướng dẫn mà luật kiểm cần (đọc một lần, cùng nguồn với công cụ HTML):
    khong_co {(nhóm, thuộc tính): {khóa: tên điều kiện}}, co_mac_dinh {(nhóm, thuộc tính): {khóa: {dieu_kien, hieu}}},
    khoa_ghi_duoc {(nhóm, thuộc tính): [khóa được ghi vào mac_dinh=]},
    tu_hop_le [từ khẳng định được ghi vào khang_dinh=, chữ thường], ds_tu (chuỗi hiện trong thông báo),
    don_vi {(nhóm, thuộc tính): {don_vi, re}} (re áp lên câu trích đã hạ chữ thường)."""
    global _QUY_TAC
    if _QUY_TAC is None:
        md = tc.doc_huong_dan()
        hang = tc.bang_mac_dinh(md)
        tu = tc.tu_khang_dinh(md)
        _QUY_TAC = {
            "khong_co": tc.khoa_khong_co_mac_dinh(hang), "co_mac_dinh": tc.khoa_co_mac_dinh(hang),
            "khoa_ghi_duoc": tc.khoa_ghi_duoc(hang),
            "tu_hop_le": [chuan_hoa(t).lower() for t in tu["tu_hop_le"]], "ds_tu": ", ".join(tu["tu_hop_le"]),
            "don_vi": {(h["nhom"], h["thuoc_tinh"]): {"don_vi": h["don_vi"], "re": re.compile(h["don_vi_mau"])}
                       for h in tc.bang_huong_loi(md)},
        }
    return _QUY_TAC


def _qt(quy_tac, ten):
    """Bảng `ten` của quy_tac nếu bên gọi truyền (thử nghiệm dùng bản rút gọn), không thì đọc từ hướng dẫn thật."""
    if quy_tac is not None and ten in quy_tac:
        return quy_tac[ten]
    return quy_tac_huong_dan()[ten]


def khong_co_mac_dinh():
    """{(tiền tố nhóm, thuộc tính): {khóa: tên điều kiện}} của các khóa "không có mặc định", đọc từ bảng mục 5 của hướng
    dẫn (cùng nguồn với công cụ HTML). Đọc một lần."""
    return quy_tac_huong_dan()["khong_co"]


def doc_jsonl(duong):
    """[(số dòng, dữ liệu hoặc None nếu hỏng, thông báo lỗi)] của các dòng không trống."""
    ket_qua = []
    with open(duong, encoding="utf-8-sig") as f:
        for so, dong in enumerate(f, 1):
            if not dong.strip():
                continue
            try:
                ket_qua.append((so, json.loads(dong), None))
            except json.JSONDecodeError as e:
                ket_qua.append((so, None, f"không phải JSON hợp lệ ({e.msg})"))
    return ket_qua


def doc_doan(ma_mau, thu_muc_nguon):
    """{mã đoạn: (noi_dung, noi_dung_goc, [chu_thich]) đã chuẩn hóa} của một mẫu; None nếu chưa có tệp.

    Tệp doan.jsonl cũ chưa có noi_dung_goc thì coi noi_dung_goc là noi_dung."""
    duong = Path(thu_muc_nguon) / ma_mau / "doan.jsonl"
    if not duong.exists():
        return None
    doan = {}
    for _, d, _ in doc_jsonl(duong):
        if d:
            doan[d["id"]] = (chuan_hoa(d["noi_dung"]), chuan_hoa(d.get("noi_dung_goc", d["noi_dung"])),
                             [chuan_hoa(c) for c in d.get("chu_thich") or []])
    return doan


def la_so_nguyen(x):
    return isinstance(x, int) and not isinstance(x, bool)


def kiem_mot_dong(nh, tb, doan, khong_co=None, quy_tac=None, luot=None):
    """Danh sách lỗi (chuỗi) của một dòng nhãn nh với tuyên bố tb; doan là {mã đoạn: ...} của mẫu hoặc None.

    khong_co: {(tiền tố nhóm, thuộc tính): {khóa: điều kiện}} các khóa "không có mặc định"; None thì đọc từ hướng dẫn
    (chỉ khi cần: dòng D1a, hoặc ghi chú có mac_dinh= và tuyên bố có thuoc_tinh). quy_tac: bản rút gọn của
    quy_tac_huong_dan() (các khóa co_mac_dinh, tu_hop_le, ds_tu); khóa nào thiếu thì đọc từ hướng dẫn thật, chỉ khi cần.
    luot: nếu có, mọi dòng nhãn phải có luot bằng số này."""
    loi = []
    thieu = [t for t in TRUONG if t not in nh]
    la = [t for t in nh if t not in TRUONG and t not in TRUONG_TUY_CHON]
    if thieu:
        loi.append(f"thiếu trường: {', '.join(thieu)}")
    if la:
        loi.append(f"trường lạ: {', '.join(la)}")
    nhan, loai = nh.get("nhan"), nh.get("loai")
    if "nhan" in nh and nhan not in NHAN:
        loi.append(f"nhan {nhan!r} không thuộc {', '.join(NHAN)}")
        nhan = None
    if "loai" in nh and nhan is not None:
        if nhan in ("DUNG", "CHUA_DU"):
            if loai is not None:
                loi.append(f"loai phải là null khi nhan là {nhan} (đang là {loai!r})")
        elif nhan == "LECH":
            if loai not in LOAI_LECH:
                goi_y = " (doi_gia_tri chỉ dùng cho SAI)" if loai == "doi_gia_tri" else ""
                loi.append(f"nhan LECH cần loai thuộc {', '.join(LOAI_LECH)}; đang là {loai!r}{goi_y}")
        elif loai not in LOAI_SAI:
            goi_y = " (loại của nhãn LECH, không dùng cho SAI)" if loai in LOAI_LECH else ""
            loi.append(f"nhan SAI cần loai thuộc {', '.join(LOAI_SAI)}; đang là {loai!r}{goi_y}")

    # Dòng D người gán dừng ở (mục 7) và các ô phải khớp dòng đó.
    dong_d = nh.get("dong_d")
    if "dong_d" in nh:
        if dong_d is None or (isinstance(dong_d, str) and not dong_d.strip()):
            loi.append(THONG_BAO["chua_chon_dong"])
            dong_d = None
        elif dong_d not in MA_DONG_D:
            loi.append(THONG_BAO["dong_la"].format(dong_d=repr(dong_d)))
            dong_d = None
    else:
        dong_d = None
    if dong_d is not None:
        if nhan is not None and nhan != NHAN_THEO_DONG[dong_d]:
            loi.append(THONG_BAO["nhan_khong_khop"].format(nhan=nhan, dong_d=dong_d, nhan_mong=NHAN_THEO_DONG[dong_d]))
        loai_d = LOAI_THEO_DONG.get(dong_d)
        # Loại ngoài LOAI_LECH (hoặc trống) đã bị báo ở trên, không báo lần hai.
        if loai_d and "loai" in nh and loai != loai_d and (nhan != "LECH" or loai in LOAI_LECH):
            loi.append(THONG_BAO["d2_sai_loai"].format(loai=repr(loai)))
        tick = nh.get("tai_lieu_mau_thuan")
        if isinstance(tick, bool):
            if dong_d == DONG_TICK_MAU_THUAN and not tick:
                loi.append(THONG_BAO["d1b_thieu_tick"])
            elif dong_d != DONG_TICK_MAU_THUAN and tick:
                loi.append(THONG_BAO["tick_khong_phai_d1b"].format(dong_d=dong_d))
        ghi_chu = nh.get("ghi_chu")
        if isinstance(ghi_chu, str):
            khoa_ghi = list(dict.fromkeys(lay_mac_dinh(ghi_chu)))
            nhom_tt = (tb["ma_mau"].split("-")[0], tb["thuoc_tinh"]) if tb.get("thuoc_tinh") else None
            cua_tb = {}  # khóa "không có mặc định" của thuộc tính; chỉ đọc hướng dẫn khi cần (D1a, hoặc ghi chú có mac_dinh=)
            if nhom_tt is not None and (dong_d == "D1a" or (khoa_ghi and dong_d != "D1")):
                if khong_co is None:
                    khong_co = khong_co_mac_dinh()
                cua_tb = khong_co.get(nhom_tt, {})
            if nhom_tt is not None and dong_d != "D1" and khoa_ghi:
                # Khóa của mac_dinh= phải là khóa ghi được của thuộc tính ở bảng mục 5 (trừ "như hãng công bố"), hoặc ngoai_bang
                # (nhãn dựa vào mục 6.7 ý 4; QĐ10). D1 không ghi mac_dinh, chỉ nhắc.
                ghi_duoc = _qt(quy_tac, "khoa_ghi_duoc").get(nhom_tt, [])
                for khoa in khoa_ghi:
                    if khoa != tc.KHOA_NGOAI_BANG and khoa not in ghi_duoc:
                        loi.append(THONG_BAO["mac_dinh_khoa_la"].format(khoa=khoa, ds=", ".join(ghi_duoc) or "(không có)"))
            if nhom_tt is not None and dong_d not in ("D1", "D1a"):
                # D1 không ghi mac_dinh (chỉ nhắc); mac_dinh của điều kiện "không có mặc định" thì phải dừng ở D1a.
                for khoa in khoa_ghi:
                    if khoa in cua_tb:
                        loi.append(THONG_BAO["mac_dinh_khong_co"].format(khoa=khoa, dieu_kien=cua_tb[khoa]))
            if nhom_tt is not None and dong_d == "D1a" and not any(k in cua_tb for k in khoa_ghi) \
                    and not lay_chua_xac_dinh(ghi_chu):
                # D1a phải ghi nguyên nhân; chỉ ghi khóa có cách hiểu mặc định là sai (dùng mặc định rồi dò tiếp).
                loi.append(THONG_BAO["d1a_thieu_nguyen_nhan"].format(ds=", ".join(cua_tb) or "(thuộc tính này không có khóa nào)"))
                co_mac_dinh = _qt(quy_tac, "co_mac_dinh").get(nhom_tt, {}) if khoa_ghi else {}
                for khoa in khoa_ghi:
                    if khoa in co_mac_dinh:
                        loi.append(THONG_BAO["d1a_mac_dinh_co_mac_dinh"].format(khoa=khoa, **co_mac_dinh[khoa]))
            if dong_d == "D2":
                # D2 phải ghi từ khẳng định, và từ đó phải có trong danh sách ở mục 6.2.
                tu_ghi = list(dict.fromkeys(lay_khang_dinh(ghi_chu)))
                hop_le = _qt(quy_tac, "tu_hop_le")
                ds_tu = _qt(quy_tac, "ds_tu")
                if not tu_ghi:
                    loi.append(THONG_BAO["d2_thieu_khang_dinh"].format(ds=ds_tu))
                for tu in tu_ghi:
                    if chuan_hoa(tu).lower() not in hop_le:
                        loi.append(THONG_BAO["d2_khang_dinh_la"].format(tu=tu, ds=ds_tu))

    bang_chung = nh.get("bang_chung")
    doan_dung = []  # (mã, noi_dung, noi_dung_goc, [chu_thich]) của các đoạn bằng chứng hợp lệ
    if "bang_chung" in nh:
        if not isinstance(bang_chung, list) or not all(isinstance(m, str) for m in bang_chung):
            loi.append("bang_chung phải là danh sách mã đoạn (chuỗi)")
            bang_chung = None
        else:
            if not bang_chung and nhan is not None and nhan != "CHUA_DU":
                loi.append(f"bang_chung rỗng (chỉ được rỗng khi nhan là CHUA_DU; đang là {nhan})")
            for ma, so_lan in Counter(bang_chung).items():
                if so_lan > 1:
                    loi.append(f"mã bằng chứng {ma} lặp {so_lan} lần")
            for ma in dict.fromkeys(bang_chung):
                if doan is None:
                    break
                if ma not in doan:
                    loi.append(f"mã bằng chứng {ma} không có trong data/nguon/{tb['ma_mau']}/doan.jsonl")
                else:
                    doan_dung.append((ma, *doan[ma]))

    trich = nh.get("trich")
    # D1: tài liệu không có thông số, nên không có bằng chứng và câu trích; khi đó bỏ các kiểm bằng chứng - câu trích.
    d1_co = dong_d == "D1" and bool((isinstance(nh.get("bang_chung"), list) and nh["bang_chung"])
                                    or (isinstance(trich, str) and trich.strip()))
    if d1_co:
        loi.append(THONG_BAO["d1_co_bang_chung"])
    if "trich" in nh:
        if not isinstance(trich, str):
            loi.append("trich phải là chuỗi")
        elif bang_chung is not None and not d1_co:
            if bang_chung and not trich.strip():
                loi.append("có bang_chung nhưng trich rỗng")
            elif trich.strip() and not bang_chung:
                loi.append("trich có nội dung nhưng bang_chung rỗng")
            elif trich.strip() and doan_dung:
                co_phan_rong = False
                for phan in trich.split(TACH_TRICH):
                    p = chuan_hoa(phan)
                    if not p:
                        if not co_phan_rong:
                            loi.append("trich có phần rỗng (hai dấu ' | ' liền nhau hoặc ở đầu/cuối)")
                        co_phan_rong = True
                    elif not any(p in nd or p in goc or any(p in ct for ct in cts) for _, nd, goc, cts in doan_dung):
                        loi.append(f"trich không là chuỗi con của noi_dung, noi_dung_goc hay chu_thich của đoạn bằng chứng: {p[:80]!r}")

    for ten in ("ly_do", "nguoi_gan"):
        if ten in nh and (not isinstance(nh[ten], str) or not nh[ten].strip()):
            loi.append(f"{ten} phải là chuỗi không rỗng")
    if isinstance(nh.get("ly_do"), str) and nh["ly_do"].strip():
        giu_cho = list(dict.fromkeys(GIU_CHO.findall(nh["ly_do"])))
        if giu_cho:
            loi.append("Lý do còn chỗ {…} chưa thay: " + ", ".join(giu_cho))
    if isinstance(nh.get("ly_do"), str) and ma_doan_trong_ngoac(nh["ly_do"]):
        loi.append(THONG_BAO["ly_do_ma_doan"].format(ma=ma_doan_trong_ngoac(nh["ly_do"])))
    if "ghi_chu" in nh and not isinstance(nh["ghi_chu"], str):
        loi.append("ghi_chu phải là chuỗi")
    if "giay" in nh and not (la_so_nguyen(nh["giay"]) and nh["giay"] > 0):
        loi.append(f"giay phải là số nguyên dương (đang là {nh['giay']!r})")
    if "luot" in nh and not (la_so_nguyen(nh["luot"]) and nh["luot"] > 0):
        loi.append(f"luot phải là số nguyên dương (đang là {nh['luot']!r})")
    elif luot is not None and "luot" in nh and nh["luot"] != luot:
        loi.append(f"luot là {nh['luot']}, khác lượt {luot} đang kiểm")
    if "giay_nghi" in nh and not (la_so_nguyen(nh["giay_nghi"]) and nh["giay_nghi"] >= 0):
        loi.append(f"giay_nghi phải là số nguyên không âm (đang là {nh['giay_nghi']!r})")
    if "tai_lieu_mau_thuan" in nh and not isinstance(nh["tai_lieu_mau_thuan"], bool):
        loi.append(f"tai_lieu_mau_thuan phải là true/false (đang là {nh['tai_lieu_mau_thuan']!r})")
    return loi


def nhac_mot_dong(nh, tb=None, quy_tac=None):
    """Lời nhắc (không phải lỗi) của một dòng nhãn: loại bo_dieu_kien mà ghi chú không có mac_dinh=; dòng D1 mà ghi chú có
    mac_dinh=; câu trích không có đơn vị của thuộc tính (cần tb có ma_mau và thuoc_tinh, không thì bỏ qua lời nhắc này)."""
    nhac = []
    ghi_chu = nh.get("ghi_chu")
    if nh.get("loai") == "bo_dieu_kien" and isinstance(ghi_chu, str) and not lay_mac_dinh(ghi_chu):
        nhac.append(NHAC["bo_dieu_kien_thieu_mac_dinh"])
    if nh.get("dong_d") == "D1" and isinstance(ghi_chu, str) and lay_mac_dinh(ghi_chu):
        nhac.append(NHAC["d1_co_mac_dinh"])
    trich = nh.get("trich")
    if tb and tb.get("ma_mau") and tb.get("thuoc_tinh") and isinstance(trich, str) and trich.strip():
        dv = _qt(quy_tac, "don_vi").get((tb["ma_mau"].split("-")[0], tb["thuoc_tinh"]))
        if dv and not dv["re"].search(chuan_hoa(trich).lower()):
            nhac.append(NHAC["trich_thieu_don_vi"].format(thuoc_tinh=tb["thuoc_tinh"], don_vi=dv["don_vi"]))
    return nhac


def nhac_tep(dong_nhan, tuyen_bo=None, quy_tac=None):
    """Các dòng nhắc "id: lời nhắc" của các dòng nhãn đã đọc được. tuyen_bo: {id: tuyên bố} (doc_tuyen_bo); không có thì
    bỏ qua lời nhắc cần nhóm và thuộc tính."""
    tuyen_bo = tuyen_bo or {}
    return [f"{nh.get('id')}: {n}" for nh in dong_nhan for n in nhac_mot_dong(nh, tuyen_bo.get(nh.get("id")), quy_tac)]


def doc_tuyen_bo(duong=TEP_TUYEN_BO):
    """{id: tuyên bố} của tệp tuyên bố."""
    return {d["id"]: d for _, d, _ in doc_jsonl(duong) if d}


def kiem_tep(duong_nhan, duong_tuyen_bo=TEP_TUYEN_BO, thu_muc_nguon=THU_MUC_NGUON, khong_co=None, quy_tac=None, luot=None):
    """(danh sách lỗi, các dòng nhãn đọc được, số tuyên bố) của tệp nhãn so với tệp tuyên bố. khong_co, quy_tac, luot: xem
    kiem_mot_dong. luot=None thì mọi dòng nhãn phải cùng một lượt (tệp xuất từ công cụ chỉ có một lượt)."""
    tuyen_bo = doc_tuyen_bo(duong_tuyen_bo)
    loi, dong_nhan, da_co = [], [], {}
    doan_theo_mau = {}
    for so, nh, loi_doc in doc_jsonl(duong_nhan):
        if loi_doc:
            loi.append(f"dòng {so}: {loi_doc}")
            continue
        if not isinstance(nh, dict):
            loi.append(f"dòng {so}: mỗi dòng phải là một đối tượng JSON")
            continue
        ma = nh.get("id")
        if not isinstance(ma, str) or ma not in tuyen_bo:
            loi.append(f"dòng {so}: id {ma!r} không có trong tệp tuyên bố")
            continue
        if ma in da_co:
            loi.append(f"dòng {so}: id {ma} lặp (đã có ở dòng {da_co[ma]})")
            continue
        da_co[ma] = so
        dong_nhan.append(nh)
        tb = tuyen_bo[ma]
        if tb["ma_mau"] not in doan_theo_mau:
            doan_theo_mau[tb["ma_mau"]] = doc_doan(tb["ma_mau"], thu_muc_nguon)
            if doan_theo_mau[tb["ma_mau"]] is None:
                loi.append(f"không có data/nguon/{tb['ma_mau']}/doan.jsonl, không kiểm được bằng chứng của mẫu này")
        for e in kiem_mot_dong(nh, tb, doan_theo_mau[tb["ma_mau"]], khong_co, quy_tac, luot):
            loi.append(f"dòng {so} ({ma}): {e}")
    for ma in tuyen_bo:
        if ma not in da_co:
            loi.append(f"thiếu nhãn cho {ma}")
    if luot is None:
        cac_luot = sorted({nh["luot"] for nh in dong_nhan if la_so_nguyen(nh.get("luot")) and nh["luot"] > 0})
        if len(cac_luot) > 1:
            loi.append("các dòng nhãn thuộc nhiều lượt khác nhau (luot: " + ", ".join(map(str, cac_luot))
                       + "); một tệp chỉ chứa một lượt, hoặc truyền --luot")
    return loi, dong_nhan, len(tuyen_bo)


def dinh_dang_giay(giay):
    giay = round(giay)
    gio, du = divmod(giay, 3600)
    phut, s = divmod(du, 60)
    return f"{gio} giờ {phut} phút {s} giây" if gio else f"{phut} phút {s} giây"


def tom_tat(dong_nhan, so_tuyen_bo):
    """Các dòng chữ tóm tắt số nhãn, số loại biến đổi và thời gian gán."""
    dem_nhan = Counter(nh.get("nhan") for nh in dong_nhan)
    dem_dong = Counter(nh.get("dong_d") for nh in dong_nhan)
    dem_loai = Counter(nh.get("loai") for nh in dong_nhan if nh.get("nhan") in ("LECH", "SAI"))
    giay = [nh["giay"] for nh in dong_nhan if la_so_nguyen(nh.get("giay")) and nh["giay"] > 0]
    cac_luot = sorted({nh["luot"] for nh in dong_nhan if la_so_nguyen(nh.get("luot"))})
    dong = [f"Đọc được {len(dong_nhan)} nhãn cho {so_tuyen_bo} tuyên bố.",
            "Lượt gán (luot): " + (", ".join(map(str, cac_luot)) or "không có"), "", "Số nhãn:"]
    dong += [f"  {n:<8} {dem_nhan.get(n, 0):>3}" for n in NHAN]
    dong += ["", "Dòng D đã dừng ở (dong_d):"]
    dong += [f"  {n:<8} {dem_dong.get(n, 0):>3}" for n in MA_DONG_D]
    dong += ["", "Loại biến đổi (nhãn LECH và SAI):"]
    dong += [f"  {n:<16} {dem_loai.get(n, 0):>3}" for n in LOAI_TAT_CA]
    dong += ["", f"Tài liệu mâu thuẫn: {sum(1 for nh in dong_nhan if nh.get('tai_lieu_mau_thuan') is True)} tuyên bố"]
    if giay:
        dong += [f"Thời gian gán ({len(giay)} tuyên bố): tổng {sum(giay)} giây ({dinh_dang_giay(sum(giay))}), "
                 f"trung bình {sum(giay) / len(giay):.1f} giây, trung vị {statistics.median(giay):g} giây mỗi tuyên bố"]
    else:
        dong += ["Thời gian gán: chưa có số giây hợp lệ"]
    nghi = [nh["giay_nghi"] for nh in dong_nhan if la_so_nguyen(nh.get("giay_nghi")) and nh["giay_nghi"] >= 0]
    if nghi:
        dong += [f"Đồng hồ đứng vì không thao tác (giay_nghi, không nằm trong giay): tổng {sum(nghi)} giây "
                 f"({dinh_dang_giay(sum(nghi))}) ở {sum(1 for x in nghi if x > 0)} tuyên bố"]
    return dong


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Kiểm tệp nhãn chuẩn của bộ thử (Bước 13, 16).")
    ap.add_argument("tep_nhan", type=Path, help="data/nhan/thu_luot2.jsonl")
    ap.add_argument("tep_tuyen_bo", type=Path, nargs="?", default=TEP_TUYEN_BO,
                    help="mặc định data/tuyen_bo/thu.jsonl")
    ap.add_argument("--luot", type=int, default=None,
                    help="lượt gán mong đợi; bỏ trống thì đọc từ các bản ghi (mọi dòng phải cùng một lượt)")
    args = ap.parse_args()
    for duong in (args.tep_nhan, args.tep_tuyen_bo):
        if not duong.exists():
            sys.exit(f"không thấy tệp {duong}")
    loi, dong_nhan, so_tuyen_bo = kiem_tep(args.tep_nhan, args.tep_tuyen_bo, luot=args.luot)
    print("\n".join(tom_tat(dong_nhan, so_tuyen_bo)))
    nhac = nhac_tep(dong_nhan, doc_tuyen_bo(args.tep_tuyen_bo))
    if nhac:
        print(f"\nNhắc ({len(nhac)}, không tính là lỗi):")
        print("\n".join(f"  - {n}" for n in nhac))
    if loi:
        print(f"\nCó {len(loi)} lỗi:")
        print("\n".join(f"  - {e}" for e in loi))
        sys.exit(1)
    print("\nKhông có lỗi.")


if __name__ == "__main__":
    main()
