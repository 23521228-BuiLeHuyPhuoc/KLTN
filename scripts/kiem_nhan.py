"""Bước 13: kiểm tệp nhãn chuẩn do người gán xuất từ công cụ (data/nhan/thu.jsonl) và in tóm tắt.

Kiểm: mỗi tuyên bố có đúng một nhãn, không có mã lạ; dong_d (dòng D đã dừng ở, hướng dẫn mục 7) thuộc D1..D6 và nhãn
khớp dòng (D1, D1a, D1b, D6: CHUA_DU; D2, D4: LECH; D3: DUNG; D5: SAI); nhãn và loại biến đổi hợp lệ theo hướng dẫn (mục 8:
LECH luôn có loại; SAI chỉ doi_gia_tri, doi_bo_phan hoặc doi_phien_ban; DUNG và CHUA_DU để trống; D2 thì loại là
doi_kieu_gia_tri); tai_lieu_mau_thuan là true khi và chỉ khi dòng D1b (mục 4); D1 thì bằng chứng và câu trích để trống;
ghi chú mac_dinh=<khóa> của một điều kiện "không có mặc định" (mục 5) thì phải dừng ở D1a; lý do không còn chỗ {…} của
mẫu câu; mã bằng chứng có trong data/nguon/<ma_mau>/doan.jsonl của đúng mẫu; mỗi phần của câu trích (tách bằng " | ") là
chuỗi con của noi_dung, của noi_dung_goc hoặc của một chu_thich của các đoạn bằng chứng (sau khi chuẩn hóa NFC và gộp
khoảng trắng); lý do, người gán, số giây. Có lỗi thì liệt kê từng lỗi và thoát mã 1.

Ngoài lỗi còn in mục "Nhắc" (không tính là lỗi, không đổi mã thoát): loại bo_dieu_kien mà ghi chú không có mac_dinh=.

Các kiểm này chỉ bắt chỗ các ô người gán điền mâu thuẫn nhau hoặc trái quy tắc, dựa vào nhóm (tiền tố ma_mau) và thuộc tính
ghi sẵn trên tuyên bố; không đọc nội dung tuyên bố để đoán nhãn hay dòng D. Bảng dòng D, thông báo lỗi và khóa "không có
mặc định" lấy từ scripts/tao_cong_cu_gan_nhan.py (cùng nguồn với công cụ HTML, đọc hướng dẫn mục 5).

noi_dung đã bỏ số chú thích của trang hãng ("20 phút6" -> "20 phút"), noi_dung_goc là bản trước khi bỏ. Câu trích chép
theo noi_dung (chữ hiển thị trên trang gán nhãn) là cách đúng, nhưng nhãn đã lưu trước đó có thể chép kèm số chú thích nên
noi_dung_goc cũng được chấp nhận.

Chạy:
    .venv/Scripts/python.exe scripts/kiem_nhan.py data/nhan/thu.jsonl [data/tuyen_bo/thu.jsonl]
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
TACH_TRICH = " | "
# Mục mac_dinh=<khóa>,<khóa> của ghi chú (cùng biểu thức với công cụ HTML).
MAC_DINH = re.compile(r"(?:^|;\s*)mac_dinh=([^;]*)")
_KHONG_CO_MAC_DINH = None
# Cùng tập ký tự khoảng trắng với regex \s của JavaScript, để công cụ HTML và script này chuẩn hóa như nhau.
KHOANG_TRANG = re.compile("[\\t\\n\\v\\f\\r    -     　﻿]+")


def chuan_hoa(chuoi):
    """NFC, gộp mọi dãy khoảng trắng thành một dấu cách, bỏ khoảng trắng hai đầu."""
    return KHOANG_TRANG.sub(" ", unicodedata.normalize("NFC", chuoi)).strip()


def lay_mac_dinh(ghi_chu):
    """Các khóa sau mac_dinh= trong ghi chú (cách nhau bằng dấu phẩy); [] nếu không có mục mac_dinh."""
    m = MAC_DINH.search(ghi_chu)
    return [x.strip() for x in m.group(1).split(",") if x.strip()] if m else []


def khong_co_mac_dinh():
    """{(tiền tố nhóm, thuộc tính): {khóa: tên điều kiện}} của các khóa "không có mặc định", đọc từ bảng mục 5 của hướng
    dẫn (cùng nguồn với công cụ HTML). Đọc một lần."""
    global _KHONG_CO_MAC_DINH
    if _KHONG_CO_MAC_DINH is None:
        _KHONG_CO_MAC_DINH = tc.khoa_khong_co_mac_dinh(tc.bang_mac_dinh(tc.doc_huong_dan()))
    return _KHONG_CO_MAC_DINH


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


def kiem_mot_dong(nh, tb, doan, khong_co=None):
    """Danh sách lỗi (chuỗi) của một dòng nhãn nh với tuyên bố tb; doan là {mã đoạn: ...} của mẫu hoặc None.

    khong_co: {(tiền tố nhóm, thuộc tính): {khóa: điều kiện}} các khóa "không có mặc định"; None thì đọc từ hướng dẫn
    (chỉ khi cần: ghi chú có mac_dinh= và tuyên bố có thuoc_tinh)."""
    loi = []
    thieu = [t for t in TRUONG if t not in nh]
    la = [t for t in nh if t not in TRUONG]
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
        if dong_d != "D1a" and isinstance(ghi_chu, str) and tb.get("thuoc_tinh"):
            khoa_ghi = lay_mac_dinh(ghi_chu)
            if khoa_ghi and khong_co is None:
                khong_co = khong_co_mac_dinh()
            cua_tb = (khong_co or {}).get((tb["ma_mau"].split("-")[0], tb["thuoc_tinh"]), {})
            for khoa in dict.fromkeys(khoa_ghi):
                if khoa in cua_tb:
                    loi.append(THONG_BAO["mac_dinh_khong_co"].format(khoa=khoa, dieu_kien=cua_tb[khoa]))

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
    if "ghi_chu" in nh and not isinstance(nh["ghi_chu"], str):
        loi.append("ghi_chu phải là chuỗi")
    if "giay" in nh and not (la_so_nguyen(nh["giay"]) and nh["giay"] > 0):
        loi.append(f"giay phải là số nguyên dương (đang là {nh['giay']!r})")
    if "luot" in nh and not (la_so_nguyen(nh["luot"]) and nh["luot"] > 0):
        loi.append(f"luot phải là số nguyên dương (đang là {nh['luot']!r})")
    if "tai_lieu_mau_thuan" in nh and not isinstance(nh["tai_lieu_mau_thuan"], bool):
        loi.append(f"tai_lieu_mau_thuan phải là true/false (đang là {nh['tai_lieu_mau_thuan']!r})")
    return loi


def nhac_mot_dong(nh):
    """Lời nhắc (không phải lỗi) của một dòng nhãn: loại bo_dieu_kien mà ghi chú không có mac_dinh=."""
    nhac = []
    if nh.get("loai") == "bo_dieu_kien" and isinstance(nh.get("ghi_chu"), str) and not lay_mac_dinh(nh["ghi_chu"]):
        nhac.append(NHAC["bo_dieu_kien_thieu_mac_dinh"])
    return nhac


def nhac_tep(dong_nhan):
    """Các dòng nhắc "id: lời nhắc" của các dòng nhãn đã đọc được."""
    return [f"{nh.get('id')}: {n}" for nh in dong_nhan for n in nhac_mot_dong(nh)]


def kiem_tep(duong_nhan, duong_tuyen_bo=TEP_TUYEN_BO, thu_muc_nguon=THU_MUC_NGUON, khong_co=None):
    """(danh sách lỗi, các dòng nhãn đọc được, số tuyên bố) của tệp nhãn so với tệp tuyên bố. khong_co: xem kiem_mot_dong."""
    tuyen_bo = {}
    for _, d, _ in doc_jsonl(duong_tuyen_bo):
        if d:
            tuyen_bo[d["id"]] = d
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
        for e in kiem_mot_dong(nh, tb, doan_theo_mau[tb["ma_mau"]], khong_co):
            loi.append(f"dòng {so} ({ma}): {e}")
    for ma in tuyen_bo:
        if ma not in da_co:
            loi.append(f"thiếu nhãn cho {ma}")
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
    dong = [f"Đọc được {len(dong_nhan)} nhãn cho {so_tuyen_bo} tuyên bố.", "", "Số nhãn:"]
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
    return dong


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Kiểm tệp nhãn chuẩn của bộ thử (Bước 13).")
    ap.add_argument("tep_nhan", type=Path, help="data/nhan/thu.jsonl")
    ap.add_argument("tep_tuyen_bo", type=Path, nargs="?", default=TEP_TUYEN_BO,
                    help="mặc định data/tuyen_bo/thu.jsonl")
    args = ap.parse_args()
    for duong in (args.tep_nhan, args.tep_tuyen_bo):
        if not duong.exists():
            sys.exit(f"không thấy tệp {duong}")
    loi, dong_nhan, so_tuyen_bo = kiem_tep(args.tep_nhan, args.tep_tuyen_bo)
    print("\n".join(tom_tat(dong_nhan, so_tuyen_bo)))
    nhac = nhac_tep(dong_nhan)
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
