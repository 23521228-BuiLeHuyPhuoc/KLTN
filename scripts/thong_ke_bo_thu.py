"""Bước 16: thống kê bộ thử và tính phương án quy mô dữ liệu.

Đọc bài quảng cáo (data/quang_cao/*.json, chỉ các mẫu có mau_thu = co trong data/mau_san_pham.csv), tuyên bố
(data/tuyen_bo/thu.jsonl), nhãn lượt 2 (data/nhan/thu_luot2.jsonl, nhãn chuẩn hiện hành), nhãn lượt 1
(data/nhan/thu_luot1.jsonl, có số giây gán thật) và cấu hình data/cau_hinh/*.yaml. Ghi ket_qua/bo_thu/thong_ke.md:
phân bố nhãn, số tuyên bố mỗi bài (cả số tuyên bố có điều kiện), thời gian gán lượt 1 và phương án quy mô.
Chỉ có số liệu và phương án, không có kết luận. Không gọi LLM.

Tuyên bố có điều kiện: tuyên bố có thuộc tính mà cấu hình của nhóm mẫu ghi dieu_kien_bat_buoc không rỗng.
Phương án quy mô: mục tiêu MUC_TIEU tuyên bố tính cả bộ thử, cho mọi mẫu của mau_san_pham.csv; các mẫu chưa có trong
bộ thử là mẫu cần sinh thêm. Ước tính dùng trung bình và độ lệch chuẩn số tuyên bố mỗi bài đo trên bộ thử.

Chạy:
    .venv/Scripts/python.exe -X utf8 scripts/thong_ke_bo_thu.py [--ra <tệp>]
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kiemchung import cau_hinh  # noqa: E402

THU_MUC_QC = ROOT / "data/quang_cao"
TEP_TUYEN_BO = ROOT / "data/tuyen_bo/thu.jsonl"
TEP_NHAN_2 = ROOT / "data/nhan/thu_luot2.jsonl"
TEP_NHAN_1 = ROOT / "data/nhan/thu_luot1.jsonl"
TEP_RA = ROOT / "ket_qua/bo_thu/thong_ke.md"

MUC_TIEU = (250, 300)  # tuyên bố, tính cả bộ thử (Bước 16)
NGUONG_DIEU_KIEN = 2  # T9.1: dưới ngưỡng này thì áp phương án tăng số bài
SO_BAI_MOT_LAN = 12  # 2 LLM x 3 loại bài x 2 chế độ cho một mẫu (Bước 12, Bước 18)
CHE_DO = ("ten", "ten_thong_so")
NHAN = (("DUNG", "Đúng"), ("LECH", "Lệch"), ("SAI", "Sai"), ("CHUA_DU", "Chưa đủ thông tin"))
TEN_NHAN = dict(NHAN)
# Tên ngắn của dòng quyết định D1–D6 (data/huong_dan_gan_nhan.md mục 7); nhãn đi kèm lấy từ dữ liệu.
TEN_DONG_D = {
    "D1": "Tài liệu không có con số nào cho thuộc tính",
    "D1a": "Không xác định được điều kiện của tuyên bố",
    "D1b": "Tài liệu mâu thuẫn ở điều kiện của tuyên bố",
    "D2": "Từ khẳng định cho mức không cao hơn mức \"lên đến\"",
    "D3": "Khớp ở đúng điều kiện",
    "D4": "Giá trị công bố ở điều kiện khác",
    "D5": "Mâu thuẫn hoặc thuận lợi hơn mọi giá trị công bố",
    "D6": "Có số nhưng không công bố ở điều kiện của tuyên bố",
}
TEN_NHOM = {"dien_thoai": "Điện thoại", "tai_nghe": "Tai nghe", "dong_ho": "Đồng hồ"}


# ---------- đọc dữ liệu ----------

def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(dong) for dong in f if dong.strip()]


def doc_bai(thu_muc, ma_mau_thu):
    """Các bài của mẫu bộ thử, xếp theo mã bài: {ma_qc, ma_mau, llm, loai_bai, che_do}."""
    bai = []
    for duong in sorted(Path(thu_muc).glob("*.json")):
        with open(duong, encoding="utf-8") as f:
            qc = json.load(f)
        if qc["ma_mau"] in ma_mau_thu:
            bai.append({"ma_qc": qc["ma_qc"], "ma_mau": qc["ma_mau"], "llm": qc["mo_hinh_nha_cung_cap"],
                        "loai_bai": qc["loai_bai"], "che_do": qc["che_do"]})
    return bai


# ---------- hàm tính ----------

def thong_ke(gia_tri):
    """Mô tả một dãy số. Dãy rỗng thì các số đều None; một phần tử thì độ lệch chuẩn None."""
    n = len(gia_tri)
    if not n:
        return {"n": 0, "tong": 0, "tb": None, "trung_vi": None, "do_lech": None, "nho_nhat": None,
                "lon_nhat": None, "so_khong": 0}
    return {"n": n, "tong": sum(gia_tri), "tb": statistics.fmean(gia_tri), "trung_vi": statistics.median(gia_tri),
            "do_lech": statistics.stdev(gia_tri) if n >= 2 else None, "nho_nhat": min(gia_tri),
            "lon_nhat": max(gia_tri), "so_khong": sum(1 for g in gia_tri if g == 0)}


def thuoc_tinh_co_dieu_kien(cau_hinh_nhom):
    """Tên các thuộc tính của một nhóm mà dieu_kien_bat_buoc không rỗng."""
    return [ten for ten, tt in (cau_hinh_nhom.get("thuoc_tinh") or {}).items() if (tt or {}).get("dieu_kien_bat_buoc")]


def la_co_dieu_kien(tuyen_bo, nhom_cua_mau, co_dieu_kien):
    """Tuyên bố có điều kiện: thuộc tính nằm trong co_dieu_kien[nhóm của mẫu]. Thuộc tính ngoài cấu hình thì không."""
    return tuyen_bo["thuoc_tinh"] in co_dieu_kien.get(nhom_cua_mau[tuyen_bo["ma_mau"]], ())


def tinh_bai(bai, tuyen_bo, nhom_cua_mau, co_dieu_kien):
    """Thêm tb (số tuyên bố) và co_dk (số tuyên bố có điều kiện) vào từng bài; bài không có tuyên bố thì 0.
    Tuyên bố trỏ tới bài không có trong danh sách thì báo lỗi."""
    tb, co_dk = Counter(), Counter()
    ma_bai = {b["ma_qc"] for b in bai}
    for t in tuyen_bo:
        if t["ma_qc"] not in ma_bai:
            raise ValueError(f"{t['id']}: bài {t['ma_qc']} không có trong danh sách bài")
        tb[t["ma_qc"]] += 1
        co_dk[t["ma_qc"]] += la_co_dieu_kien(t, nhom_cua_mau, co_dieu_kien)
    return [{**b, "tb": tb[b["ma_qc"]], "co_dk": co_dk[b["ma_qc"]]} for b in bai]


def gom(ban_ghi, khoa):
    """{giá trị của khoa(bản ghi): [bản ghi]}, xếp theo giá trị."""
    nhom = {}
    for b in ban_ghi:
        nhom.setdefault(khoa(b), []).append(b)
    return dict(sorted(nhom.items(), key=lambda kv: str(kv[0])))


def uoc_tinh(ti_le_che_do, tb_che_do, do_lech_che_do, so_bai):
    """Tuyên bố từ so_bai bài mới: (trung bình, độ lệch chuẩn của tổng).

    ti_le_che_do: {chế độ: phần bài}, cộng bằng 1. Coi các bài độc lập; bài chế độ m có trung bình tb_che_do[m] và
    độ lệch chuẩn do_lech_che_do[m], nên phương sai của tổng là so_bai * tổng(phần * độ lệch chuẩn bình phương)."""
    tb = so_bai * sum(f * tb_che_do[m] for m, f in ti_le_che_do.items())
    phuong_sai = so_bai * sum(f * do_lech_che_do[m] ** 2 for m, f in ti_le_che_do.items())
    return tb, math.sqrt(phuong_sai)


def so_bai_moi_mau(muc_tieu, san_co, so_mau, tb_bai):
    """Số bài mới mỗi mẫu (số thực) để tổng đạt muc_tieu khi mỗi bài cho tb_bai tuyên bố."""
    return (muc_tieu - san_co) / so_mau / tb_bai


def ung_vien_so_bai(thap, cao, them=()):
    """Số bài nguyên mỗi mẫu cần xem: từ ceil(thap) - 1 đến floor(cao) + 1 (tối thiểu 1), cộng các số trong them."""
    tu, den = math.ceil(thap), math.floor(cao)
    return sorted({n for n in range(max(1, tu - 1), max(den, tu - 1) + 2)} | set(them))


def gio_phut(giay):
    """'4 giờ 47 phút' (làm tròn đến phút); dưới một giờ chỉ ghi phút."""
    phut = round(giay / 60)
    gio, phut = divmod(phut, 60)
    return f"{gio} giờ {phut} phút" if gio else f"{phut} phút"


def bo_lon_nhat(gia_tri, k):
    """Dãy sau khi bỏ k giá trị lớn nhất."""
    return sorted(gia_tri)[:max(0, len(gia_tri) - k)]


# ---------- định dạng ----------

def so(x, chu_so=2):
    """Số thập phân dùng dấu phẩy: 2,75."""
    return f"{x:.{chu_so}f}".replace(".", ",")


def o_so(x, chu_so=2):
    return "—" if x is None else so(x, chu_so)


def so_gon(x):
    """Số nguyên thì không thêm phần thập phân; ngược lại một chữ số."""
    if x is None:
        return "—"
    return str(int(x)) if x == int(x) else so(x, 1)


def nguyen(n):
    """Số nguyên có dấu chấm ngăn hàng nghìn: 17.238."""
    return f"{round(n):,}".replace(",", ".")


def phan_tram(tu, mau_so):
    return "—" if not mau_so else so(100 * tu / mau_so, 1) + "%"


def o_ty_le(tu, mau_so):
    """'34 (51,5%)'."""
    return f"{tu} ({phan_tram(tu, mau_so)})"


def o_van_ban(chu):
    """Chữ đặt trong ô bảng markdown: dấu | và xuống dòng không được làm vỡ bảng."""
    return " ".join(str(chu).split()).replace("|", "\\|")


def dong_bang(*o):
    return "| " + " | ".join(o) + " |"


def bang(dau, hang):
    return [dong_bang(*dau), dong_bang(*["---"] * len(dau))] + [dong_bang(*h) for h in hang]


# ---------- các mục của báo cáo ----------

def cach_tach(ten_mau):
    """[(tên cách tách, hàm khóa)] dùng chung cho bài và tuyên bố (cả hai có ma_mau, llm, loai_bai, che_do)."""
    return [("Chế độ", lambda b: b["che_do"]),
            ("LLM", lambda b: b["llm"]),
            ("Loại bài", lambda b: b["loai_bai"]),
            ("Mẫu", lambda b: ten_mau[b["ma_mau"]]),
            ("Mẫu và chế độ", lambda b: f"{ten_mau[b['ma_mau']]} / {b['che_do']}")]


def muc_phan_bo_nhan(cac_nhan, ten_mau):
    """Phân bố nhãn lượt 2: tổng, theo cách tách, và theo dòng D. cac_nhan: bản ghi có nhan, dong_d và khóa tách."""
    n = len(cac_nhan)
    dem = Counter(x["nhan"] for x in cac_nhan)
    ten_cot = [ten for _, ten in NHAN]
    dong = ["## Phân bố nhãn lượt 2", "",
            f"Nguồn: `data/nhan/thu_luot2.jsonl`, {n} tuyên bố. Trường `nguoi_gan`: "
            + ", ".join(f"{k} {v}" for k, v in sorted(Counter(x["nguoi_gan"] for x in cac_nhan).items(),
                                                       key=lambda kv: -kv[1])) + ".", "",
            "### Tổng", ""]
    dong += bang(["Nhãn", "Số tuyên bố", "Tỷ lệ"],
                 [[ten, str(dem[ma]), phan_tram(dem[ma], n)] for ma, ten in NHAN] + [["Tổng", str(n), phan_tram(n, n)]])
    dong += ["", "### Theo mẫu, LLM, chế độ và loại bài", "",
             "Mỗi ô là số tuyên bố, kèm tỷ lệ trên tổng của hàng.", ""]
    hang = []
    for ten_cach, khoa in cach_tach(ten_mau):
        if ten_cach == "Mẫu và chế độ":
            continue
        for gt, nhom in gom(cac_nhan, khoa).items():
            d = Counter(x["nhan"] for x in nhom)
            hang.append([ten_cach, o_van_ban(gt), *(o_ty_le(d[ma], len(nhom)) for ma, _ in NHAN), str(len(nhom))])
    dong += bang(["Cách tách", "Giá trị", *ten_cot, "Tổng"], hang)

    dong += ["", "### Dòng D", "", "Nhãn đi kèm lấy từ dữ liệu.", ""]
    theo_d = gom(cac_nhan, lambda x: x["dong_d"] or "(trống)")
    hang = []
    for d, nhom in sorted(theo_d.items(), key=lambda kv: (kv[0] not in TEN_DONG_D, kv[0])):
        nhan_di_kem = ", ".join(f"{TEN_NHAN.get(k, k)} {v}" for k, v in Counter(x["nhan"] for x in nhom).most_common())
        hang.append([d, TEN_DONG_D.get(d, ""), nhan_di_kem, o_ty_le(len(nhom), n)])
    dong += bang(["Dòng", "Nội dung", "Nhãn", "Số tuyên bố"], hang)
    return dong


def bang_so_tuyen_bo(bai, truong, ten_mau, kem_nguong=False):
    """Bảng thống kê số tuyên bố mỗi bài (truong = 'tb' hoặc 'co_dk'), tách theo các cách tách."""
    dau = ["Nhóm", "Số bài", "Tuyên bố", "Trung bình", "Trung vị", "Độ lệch chuẩn", "Nhỏ nhất", "Lớn nhất",
           "Bài 0 tuyên bố"]
    if kem_nguong:
        dau.append(f"Trung bình dưới {NGUONG_DIEU_KIEN}")

    def hang(ten, nhom):
        tk = thong_ke([b[truong] for b in nhom])
        h = [ten, str(tk["n"]), str(tk["tong"]), o_so(tk["tb"]), so_gon(tk["trung_vi"]), o_so(tk["do_lech"]),
             so_gon(tk["nho_nhat"]), so_gon(tk["lon_nhat"]), f"{tk['so_khong']}/{tk['n']}"]
        if kem_nguong:
            h.append("có" if tk["tb"] is not None and tk["tb"] < NGUONG_DIEU_KIEN else "không")
        return h

    ket = [hang("Tất cả", bai)]
    for ten_cach, khoa in cach_tach(ten_mau):
        for gt, nhom in gom(bai, khoa).items():
            ket.append(hang(f"{ten_cach}: {o_van_ban(gt)}", nhom))
    return bang(dau, ket)


def muc_so_tuyen_bo(bai, tuyen_bo, nhom_cua_mau, co_dieu_kien, cau_hinh_nhom, ten_mau):
    n_tb = len(tuyen_bo)
    n_dk = sum(b["co_dk"] for b in bai)
    dem_tt = Counter((nhom_cua_mau[t["ma_mau"]], t["thuoc_tinh"]) for t in tuyen_bo)
    dong = ["## Số tuyên bố mỗi bài", "",
            f"{len(bai)} bài của bộ thử, {n_tb} tuyên bố. Bài không có tuyên bố nào vẫn được tính (số 0).", "",
            "### Thuộc tính được tính là có điều kiện", "",
            "Một tuyên bố là tuyên bố có điều kiện khi thuộc tính của nó có `dieu_kien_bat_buoc` không rỗng trong cấu hình "
            "của nhóm mẫu (`data/cau_hinh/<nhóm>.yaml`).", ""]
    hang = []
    for nhom, ch in cau_hinh_nhom.items():
        for ten, tt in (ch.get("thuoc_tinh") or {}).items():
            dk = list((tt or {}).get("dieu_kien_bat_buoc") or {})
            hang.append([TEN_NHOM.get(nhom, nhom), ten, ", ".join(dk) if dk else "(rỗng)",
                         "có" if dk else "không", str(dem_tt[(nhom, ten)])])
    dong += bang(["Nhóm", "Thuộc tính", "Điều kiện bắt buộc", "Có điều kiện", "Tuyên bố của bộ thử"], hang)
    ngoai = sorted((n, t) for (n, t) in dem_tt if t not in (co_dieu_kien.get(n) or ()))
    dong += ["", f"Tuyên bố có điều kiện: {n_dk}/{n_tb}. "
             + ("Mọi thuộc tính có tuyên bố trong bộ thử đều có điều kiện bắt buộc, nên số tuyên bố có điều kiện mỗi bài "
                "bằng số tuyên bố mỗi bài." if n_dk == n_tb else
                "Thuộc tính không có điều kiện bắt buộc (không tính): "
                + ", ".join(f"{TEN_NHOM.get(n, n)}/{t} ({dem_tt[(n, t)]})" for n, t in ngoai) + ".")]
    dong += ["", "### Số tuyên bố mỗi bài", "", "Độ lệch chuẩn là độ lệch chuẩn mẫu (chia n − 1).", ""]
    dong += bang_so_tuyen_bo(bai, "tb", ten_mau)
    dong += ["", "### Số tuyên bố có điều kiện mỗi bài", "",
             f"Cột cuối so trung bình với ngưỡng {NGUONG_DIEU_KIEN} ở rủi ro \"quá ít tuyên bố có điều kiện\" (T9.1).", ""]
    dong += bang_so_tuyen_bo(bai, "co_dk", ten_mau, kem_nguong=True)
    dong += ["", "### Từng bài", ""]
    dong += bang(["Mã bài", "Mẫu", "LLM", "Loại bài", "Chế độ", "Tuyên bố", "Có điều kiện"],
                 [[b["ma_qc"], o_van_ban(ten_mau[b["ma_mau"]]), b["llm"], b["loai_bai"], b["che_do"], str(b["tb"]),
                   str(b["co_dk"])] for b in bai])
    return dong


def muc_thoi_gian(nhan1, nhan2, ten_mau):
    """Thời gian gán lượt 1 (thật). nhan1: bản ghi có id, ma_mau, giay."""
    giay = [x["giay"] for x in nhan1]
    gia_tri_luot_2 = sorted({x["giay"] for x in nhan2})
    dong = ["## Thời gian gán lượt 1", "",
            f"Nguồn: trường `giay` của `data/nhan/thu_luot1.jsonl`, {len(nhan1)} tuyên bố. Đây là thời gian gán thật.", "",
            "Lượt 2 không có thời gian thật: " + (
                f"trường `giay` của `data/nhan/thu_luot2.jsonl` chỉ có giá trị {gia_tri_luot_2[0]} ở cả {len(nhan2)} "
                "tuyên bố, là giá trị giữ chỗ, không dùng." if gia_tri_luot_2 == [1] else
                f"trường `giay` của `data/nhan/thu_luot2.jsonl` có các giá trị {gia_tri_luot_2}; chưa kiểm là thật hay giữ chỗ, "
                "không dùng."), ""]

    def hang(ten, g):
        tk = thong_ke(g)
        return [ten, str(tk["n"]), gio_phut(tk["tong"]), nguyen(tk["tb"]), so(tk["tb"] / 60, 1),
                nguyen(tk["trung_vi"]), so(tk["trung_vi"] / 60, 1), nguyen(tk["nho_nhat"]), nguyen(tk["lon_nhat"])]

    ket = [hang("Tất cả", giay)]
    for gt, nhom in gom(nhan1, lambda x: x["ma_mau"]).items():
        ket.append(hang(o_van_ban(ten_mau[gt]), [x["giay"] for x in nhom]))
    dong += bang(["Phạm vi", "Số tuyên bố", "Tổng", "Trung bình (giây)", "Trung bình (phút)", "Trung vị (giây)",
                  "Trung vị (phút)", "Nhỏ nhất (giây)", "Lớn nhất (giây)"], ket)
    lon = sorted(nhan1, key=lambda x: -x["giay"])[:5]
    dong += ["", "Năm giá trị lớn nhất: " + ", ".join(f"{x['id']} ({nguyen(x['giay'])} giây)" for x in lon) + "."]
    con_lai = bo_lon_nhat(giay, 2)
    if con_lai:
        dong.append(f"Trung bình khi bỏ hai giá trị lớn nhất: {nguyen(statistics.fmean(con_lai))} giây "
                    f"({so(statistics.fmean(con_lai) / 60, 1)} phút), trên {len(con_lai)} tuyên bố.")
    return dong


def tinh_dau_vao(bai, cac_nhan, mau, ma_mau_thu):
    """Số đo dùng cho phương án quy mô.

    bai: bài của bộ thử đã có tb; cac_nhan: nhãn lượt 2 gắn khóa tách; mau: dòng mau_san_pham.csv."""
    theo_che_do = {m: [b["tb"] for b in bai if b["che_do"] == m] for m in CHE_DO}
    tk = {m: thong_ke(g) for m, g in theo_che_do.items()}
    lech = {m: (sum(1 for x in cac_nhan if x["che_do"] == m and x["nhan"] == "LECH"),
                sum(1 for x in cac_nhan if x["che_do"] == m)) for m in CHE_DO}
    tb_mau_che_do = {}
    for ma in sorted(ma_mau_thu):
        for m in CHE_DO:
            g = [b["tb"] for b in bai if b["ma_mau"] == ma and b["che_do"] == m]
            tb_mau_che_do[(ma, m)] = statistics.fmean(g) if g else None
    moi = [r for r in mau if r["ma_mau"] not in ma_mau_thu]
    return {
        "san_co": len(cac_nhan),
        "san_co_lech": sum(1 for x in cac_nhan if x["nhan"] == "LECH"),
        "san_co_pt": sum(1 for x in cac_nhan if x["tap"] == "phattrien"),
        "san_co_kt": sum(1 for x in cac_nhan if x["tap"] == "kiemtra"),
        "so_bai_thu": len(bai),
        "tb_bai": statistics.fmean([b["tb"] for b in bai]),
        "tb_che_do": {m: tk[m]["tb"] for m in CHE_DO},
        "do_lech_che_do": {m: tk[m]["do_lech"] for m in CHE_DO},
        "so_bai_che_do": {m: tk[m]["n"] for m in CHE_DO},
        "lech_che_do": lech,
        "ty_le_lech_che_do": {m: (l / t if t else 0.0) for m, (l, t) in lech.items()},
        "tb_mau_che_do": tb_mau_che_do,
        "mau_thu": sorted(ma_mau_thu),
        "mau_moi": moi,
        "moi_pt": sum(1 for r in moi if r["tap"] == "phattrien"),
        "moi_kt": sum(1 for r in moi if r["tap"] == "kiemtra"),
    }


def hang_phuong_an(ti_le, n, dv):
    """Số đo của một phương án: mỗi mẫu mới sinh n bài với tỷ lệ chế độ ti_le."""
    so_bai = n * len(dv["mau_moi"])
    tb_moi, sd = uoc_tinh(ti_le, dv["tb_che_do"], dv["do_lech_che_do"], so_bai)
    tong = dv["san_co"] + tb_moi
    mot_mau = tb_moi / so_bai * n  # tuyên bố mới của một mẫu
    ty_le_chung = dv["san_co_lech"] / dv["san_co"]
    lech_chung = dv["san_co_lech"] + tb_moi * ty_le_chung
    lech_che_do = dv["san_co_lech"] + so_bai * sum(
        f * dv["tb_che_do"][m] * dv["ty_le_lech_che_do"][m] for m, f in ti_le.items())
    theo_mau = [dv["san_co"] + so_bai * sum(f * dv["tb_mau_che_do"][(ma, m)] for m, f in ti_le.items())
                for ma in dv["mau_thu"]]
    ty_le_khoang = ty_le_chung * sd
    return {"n": n, "so_bai": so_bai, "tb_moi": tb_moi, "tong": tong, "thap": tong - sd, "cao": tong + sd,
            "mau_thap": min(theo_mau), "mau_cao": max(theo_mau), "lech_chung": lech_chung,
            "lech_chung_thap": lech_chung - ty_le_khoang, "lech_chung_cao": lech_chung + ty_le_khoang,
            "lech_che_do": lech_che_do, "pt": dv["san_co_pt"] + dv["moi_pt"] * mot_mau,
            "kt": dv["san_co_kt"] + dv["moi_kt"] * mot_mau,
            "trong_muc_tieu": ("có" if MUC_TIEU[0] <= tong <= MUC_TIEU[1] else "dưới" if tong < MUC_TIEU[0] else "trên")}


def bang_phuong_an(ti_le, ung_vien, dv):
    """Bảng các phương án theo số bài mỗi mẫu; trả về (dòng markdown, các hàng số đo)."""
    cac_hang = [hang_phuong_an(ti_le, n, dv) for n in ung_vien]
    dau = ["Bài mỗi mẫu", "Tổng bài mới", "Tuyên bố mới", "Tổng tuyên bố", "Khoảng ±1 độ lệch chuẩn",
           "Khoảng theo mẫu", "Trung bình trong mục tiêu", "Lệch (tỷ lệ chung)", "Lệch (tỷ lệ theo chế độ)",
           "Phát triển / kiểm tra"]
    hang = [[str(h["n"]), str(h["so_bai"]), so(h["tb_moi"], 0), so(h["tong"], 0),
             f"{so(h['thap'], 0)}–{so(h['cao'], 0)}", f"{so(h['mau_thap'], 0)}–{so(h['mau_cao'], 0)}",
             h["trong_muc_tieu"], f"{so(h['lech_chung'], 0)} ({so(h['lech_chung_thap'], 0)}–{so(h['lech_chung_cao'], 0)})",
             so(h["lech_che_do"], 0), f"{so(h['pt'], 0)} / {so(h['kt'], 0)}"] for h in cac_hang]
    return bang(dau, hang), cac_hang


def muc_phuong_an(bai, cac_nhan, mau, ma_mau_thu, ten_mau, tb_giay):
    dv = tinh_dau_vao(bai, cac_nhan, mau, ma_mau_thu)
    thap, cao = MUC_TIEU
    so_moi = len(dv["mau_moi"])
    can_tong = (thap - dv["san_co"], cao - dv["san_co"])
    dong = ["## Phương án quy mô", "",
            "Chỉ có số đo và phép tính. Chưa chốt phương án nào.", "", "### Đầu vào", "",
            f"- Mục tiêu: {MUC_TIEU[0]}–{MUC_TIEU[1]} tuyên bố, tính cả {dv['san_co']} tuyên bố của bộ thử.",
            f"- Cần thêm {can_tong[0]}–{can_tong[1]} tuyên bố từ {so_moi} mẫu còn lại, tức "
            f"{so(can_tong[0] / so_moi, 1)}–{so(can_tong[1] / so_moi, 1)} tuyên bố mỗi mẫu.",
            f"- Một lần sinh đủ thiết kế của bộ thử cho một mẫu là {SO_BAI_MOT_LAN} bài (2 LLM × 3 loại bài × 2 chế độ); "
            f"{so_moi} mẫu × {SO_BAI_MOT_LAN} = {so_moi * SO_BAI_MOT_LAN} bài.",
            f"- Tỷ lệ Lệch của bộ thử (nhãn lượt 2): "
            f"{dv['san_co_lech']}/{dv['san_co']} = {phan_tram(dv['san_co_lech'], dv['san_co'])}.",
            "", "Số đo trên bộ thử:", ""]
    hang = []
    for m in CHE_DO:
        lech, tong = dv["lech_che_do"][m]
        hang.append([f"`{m}`", str(dv["so_bai_che_do"][m]), o_so(dv["tb_che_do"][m]), o_so(dv["do_lech_che_do"][m]),
                     o_ty_le(lech, tong)])
    hang.append(["Cả hai", str(dv["so_bai_thu"]), o_so(dv["tb_bai"]),
                 o_so(statistics.stdev([b["tb"] for b in bai])), o_ty_le(dv["san_co_lech"], dv["san_co"])])
    dong += bang(["Chế độ", "Số bài", "Tuyên bố mỗi bài (trung bình)", "Độ lệch chuẩn", "Lệch/tuyên bố"], hang)
    dong += ["", "Trung bình tuyên bố mỗi bài theo mẫu và chế độ (dùng cho cột \"Khoảng theo mẫu\"):", ""]
    dong += bang(["Mẫu", *(f"`{m}`" for m in CHE_DO)],
                 [[o_van_ban(ten_mau[ma]), *(o_so(dv["tb_mau_che_do"][(ma, m)]) for m in CHE_DO)] for ma in dv["mau_thu"]])
    dong += ["", f"Mẫu cần sinh thêm ({so_moi}):", ""]
    dong += bang(["Mã mẫu", "Tên", "Nhóm", "Tập"],
                 [[r["ma_mau"], o_van_ban(r["ten"]), TEN_NHOM.get(r["nhom"], r["nhom"]), r["tap"]] for r in dv["mau_moi"]])

    # ---- cách đọc các bảng ----
    dong += ["", "### Cách tính", "",
             "- Tuyên bố mới = số bài mới × trung bình tuyên bố mỗi bài của các chế độ trong phương án (theo tỷ lệ chế độ).",
             "- Khoảng ±1 độ lệch chuẩn: độ lệch chuẩn của tổng = căn của (số bài × tổng các phần chế độ × độ lệch chuẩn² của "
             "chế độ), coi các bài độc lập. Đây là dao động ngẫu nhiên giữa các bài, không gồm sai số do ước lượng trung bình "
             "từ 12 bài mỗi chế độ.",
             "- Khoảng theo mẫu: tổng khi cả " + f"{so_moi} mẫu mới cho số tuyên bố mỗi bài bằng đúng mẫu bộ thử thấp hơn, "
             "hoặc cao hơn, trong hai mẫu (iPhone 17 hoặc Galaxy Buds3 Pro).",
             f"- Trung bình trong mục tiêu: so tổng tuyên bố trung bình với {MUC_TIEU[0]}–{MUC_TIEU[1]} (có, dưới, trên).",
             f"- Lệch (tỷ lệ chung): {dv['san_co_lech']} Lệch đã có + tuyên bố mới × {phan_tram(dv['san_co_lech'], dv['san_co'])}; "
             "trong ngoặc là khoảng ứng với khoảng ±1 độ lệch chuẩn của tuyên bố. Lệch (tỷ lệ theo chế độ): dùng tỷ lệ Lệch riêng của "
             "từng chế độ trong bộ thử.",
             f"- Phát triển / kiểm tra: tuyên bố của tập phát triển ({dv['san_co_pt']} đã có + {dv['moi_pt']} mẫu mới) và của tập "
             f"kiểm tra ({dv['moi_kt']} mẫu mới), theo cột `tap` của `mau_san_pham.csv`, mỗi mẫu mới sinh cùng số bài.",
             "- Các hàng là số bài nguyên mỗi mẫu quanh khoảng cần; số bài lẻ chỉ cân bằng chế độ khi luân phiên giữa các mẫu.", ""]

    # ---- phương án (a) ----
    ti_a = {"ten": 0.5, "ten_thong_so": 0.5}
    tb_a = sum(f * dv["tb_che_do"][m] for m, f in ti_a.items())
    dong += ["### Phương án (a): giữ đủ hai chế độ như bộ thử", "",
             f"Tỷ lệ chế độ 1:1. Trung bình {so(tb_a)} tuyên bố mỗi bài. Số bài mới cần mỗi mẫu: "
             f"{so(so_bai_moi_mau(MUC_TIEU[0], dv['san_co'], so_moi, tb_a), 1)}–"
             f"{so(so_bai_moi_mau(MUC_TIEU[1], dv['san_co'], so_moi, tb_a), 1)}.", ""]
    ung = ung_vien_so_bai(so_bai_moi_mau(MUC_TIEU[0], dv["san_co"], so_moi, tb_a),
                          so_bai_moi_mau(MUC_TIEU[1], dv["san_co"], so_moi, tb_a), them=(SO_BAI_MOT_LAN,))
    b_a, h_a = bang_phuong_an(ti_a, ung, dv)
    dong += b_a + ["", f"Hàng {SO_BAI_MOT_LAN} bài mỗi mẫu là thiết kế đầy đủ như bộ thử (Bước 18 gốc).", ""]

    # ---- phương án (b) ----
    ti_b = {"ten_thong_so": 1.0}
    tb_b = dv["tb_che_do"]["ten_thong_so"]
    dong += ["### Phương án (b): chỉ chế độ `ten_thong_so`", "",
             f"Trung bình {so(tb_b)} tuyên bố mỗi bài. Số bài mới cần mỗi mẫu: "
             f"{so(so_bai_moi_mau(MUC_TIEU[0], dv['san_co'], so_moi, tb_b), 1)}–"
             f"{so(so_bai_moi_mau(MUC_TIEU[1], dv['san_co'], so_moi, tb_b), 1)}. "
             "Sáu bài (2 LLM × 3 loại bài) là một lần sinh đủ của chế độ này cho một mẫu.", ""]
    ung = ung_vien_so_bai(so_bai_moi_mau(MUC_TIEU[0], dv["san_co"], so_moi, tb_b),
                          so_bai_moi_mau(MUC_TIEU[1], dv["san_co"], so_moi, tb_b), them=(6,))
    b_b, h_b = bang_phuong_an(ti_b, ung, dv)
    dong += b_b + [""]

    # ---- phương án (c) ----
    tb_ten = dv["tb_che_do"]["ten"]
    dong += ["### Phương án (c): theo T9.1", "",
             f"T9.1: nếu trung bình dưới {NGUONG_DIEU_KIEN} tuyên bố có điều kiện mỗi bài thì tăng số bài sinh cho mỗi mẫu; "
             "nếu vẫn thiếu thì điền tên các nhóm thông số (không kèm con số) vào ô từ khóa cho mọi bài và sinh lại các bài của "
             "bộ thử (Bước 16).", "", "Trung bình tuyên bố có điều kiện mỗi bài đo được:", ""]
    tb_dk = statistics.fmean([b["co_dk"] for b in bai])
    hang = [[f"Cả {len(bai)} bài", so(tb_dk), "có" if tb_dk < NGUONG_DIEU_KIEN else "không"]]
    for m in CHE_DO:
        tb_m = statistics.fmean([b["co_dk"] for b in bai if b["che_do"] == m])
        hang.append([f"Chế độ `{m}`", so(tb_m), "có" if tb_m < NGUONG_DIEU_KIEN else "không"])
    dong += bang(["Phạm vi", "Trung bình", f"Dưới {NGUONG_DIEU_KIEN}"], hang)
    dong += ["", f"**(c1) Tăng số bài, chỉ chế độ `ten`** (chế độ có trung bình {so(tb_ten)}; không điền từ khóa). "
             f"Số bài mới cần mỗi mẫu: {so(so_bai_moi_mau(MUC_TIEU[0], dv['san_co'], so_moi, tb_ten), 1)}–"
             f"{so(so_bai_moi_mau(MUC_TIEU[1], dv['san_co'], so_moi, tb_ten), 1)}.", ""]
    ung = ung_vien_so_bai(so_bai_moi_mau(MUC_TIEU[0], dv["san_co"], so_moi, tb_ten),
                          so_bai_moi_mau(MUC_TIEU[1], dv["san_co"], so_moi, tb_ten))
    b_c1, h_c1 = bang_phuong_an({"ten": 1.0}, ung, dv)
    dong += b_c1 + ["",
                    f"**(c2) Điền tên nhóm thông số vào ô từ khóa cho mọi bài, sinh lại {len(bai)} bài của bộ thử.** "
                    "Chưa có số đo cho thiết lập này. Bảng dưới thử ba giá trị giả định của số tuyên bố mỗi bài (đều lấy từ số đo "
                    f"trên bộ thử). Mọi bài đều là bài sinh mới, gồm {len(bai)} bài sinh lại của bộ thử; "
                    f"{dv['san_co']} tuyên bố hiện có không còn tính vào tổng. Tính trên {len(dv['mau_thu']) + so_moi} mẫu.", ""]
    so_mau_tong = len(dv["mau_thu"]) + so_moi
    hang = []
    for ten, gt in (("bằng chế độ `ten`", tb_ten), ("bằng trung bình cả hai chế độ", dv["tb_bai"]),
                    ("bằng chế độ `ten_thong_so`", tb_b)):
        b_thap, b_cao = math.ceil(MUC_TIEU[0] / gt), math.floor(MUC_TIEU[1] / gt)
        hang.append([f"{so(gt)} ({ten})", f"{b_thap}–{b_cao}", f"{so(b_thap / so_mau_tong, 1)}–{so(b_cao / so_mau_tong, 1)}"])
    dong += bang(["Tuyên bố mỗi bài (giả định)", f"Tổng bài cho {MUC_TIEU[0]}–{MUC_TIEU[1]} tuyên bố",
                  f"Bài mỗi mẫu ({so_mau_tong} mẫu)"], hang)

    # ---- thời gian gán ----
    dong += ["", "### Thời gian gán ước tính cho tuyên bố mới", "",
             f"Nhân số tuyên bố mới trung bình với thời gian gán lượt 1 (trung bình {nguyen(tb_giay[0])} giây, trung vị "
             f"{nguyen(tb_giay[1])} giây mỗi tuyên bố). Lượt 1 gồm giai đoạn làm quen hướng dẫn nên chỉ là cận tham khảo; "
             "lượt 2 không có thời gian thật.", ""]
    hang = []
    for ten, hs in (("(a)", h_a), ("(b)", h_b), ("(c1)", h_c1)):
        for h in hs:
            hang.append([ten, str(h["n"]), so(h["tb_moi"], 0), so(h["tb_moi"] * tb_giay[0] / 3600, 1),
                         so(h["tb_moi"] * tb_giay[1] / 3600, 1)])
    dong += bang(["Phương án", "Bài mỗi mẫu", "Tuyên bố mới", "Giờ gán (theo trung bình)", "Giờ gán (theo trung vị)"], hang)
    return dong, dv


def muc_gia_dinh(dv, bai, ten_mau, cau_hinh_nhom):
    so_thuoc_tinh = ", ".join(f"{TEN_NHOM.get(n, n).lower()} {len(thuoc_tinh_co_dieu_kien(ch))}"
                              for n, ch in cau_hinh_nhom.items())
    bai_ten_khong = [b for b in bai if b["che_do"] == "ten" and b["tb"] == 0]
    n_ten = dv["so_bai_che_do"]["ten"]
    theo_mau = []
    for ma in dv["mau_thu"]:
        bai_mau = [b for b in bai if b["ma_mau"] == ma]
        theo_mau.append(f"{ten_mau[ma]}: {sum(b['tb'] for b in bai_mau)} tuyên bố trên {len(bai_mau)} bài "
                        f"({so(statistics.fmean([b['tb'] for b in bai_mau]))} mỗi bài)")
    return ["", "### Giả định và giới hạn", "",
            f"- Số đo chỉ từ {len(dv['mau_thu'])} mẫu ({'; '.join(theo_mau)}). "
            f"Mỗi ô mẫu × chế độ có {dv['so_bai_che_do']['ten'] // len(dv['mau_thu'])} bài.",
            "- Trung bình và độ lệch chuẩn của mỗi chế độ ước lượng từ " + " và ".join(
                f"{dv['so_bai_che_do'][m]} bài (`{m}`)" for m in CHE_DO) + ".",
            "- Giả định bài mới cùng thiết lập với bộ thử (câu lệnh, LLM, loại bài, đoạn thông số chọn theo cùng quy tắc) và tuyên bố "
            "được tách tay theo cùng quy tắc (lọc theo cấu hình, gộp trùng trong bài). Không tính hao hụt (bài lỗi, bài bị cắt).",
            f"- Số thuộc tính có điều kiện khác nhau giữa các nhóm ({so_thuoc_tinh}). Bộ thử chỉ có điện thoại và tai nghe; "
            "nhóm đồng hồ không có số đo.",
            "- Tỷ lệ điện thoại và tai nghe khác nhau: xem hàng \"Mẫu\" trong bảng số tuyên bố mỗi bài và cột \"Khoảng theo mẫu\". "
            "Khoảng theo mẫu chỉ có hai đầu mút (hai mẫu), không phải khoảng tin cậy.",
            f"- {len(bai_ten_khong)}/{n_ten} bài chế độ `ten` không có tuyên bố nào; phân bố số tuyên bố mỗi bài của chế độ này lệch, "
            "nên trung bình và độ lệch chuẩn chỉ mô tả gần đúng.",
            "- Tỷ lệ Lệch lấy từ nhãn lượt 2 của bộ thử (Claude gán, người thực hiện duyệt); mẫu nhỏ, chưa tách theo loại biến đổi "
            "và có thể đổi nếu thiết lập sinh đổi (nhất là phương án c2).",
            "- Số tuyên bố có điều kiện bằng số tuyên bố vì mọi thuộc tính đều có điều kiện bắt buộc; nếu cấu hình có thuộc tính "
            "không điều kiện thì hai số tách ra."
            if all(b["tb"] == b["co_dk"] for b in bai) else
            "- Số tuyên bố có điều kiện nhỏ hơn số tuyên bố; các phương án trên tính theo số tuyên bố (đủ mọi loại), không theo "
            "số tuyên bố có điều kiện.",
            ]


def tao_bao_cao(bai, tuyen_bo, nhan2, nhan1, mau, cau_hinh_nhom):
    """Danh sách dòng markdown. bai: bài bộ thử (doc_bai); nhan2/nhan1: nhãn lượt 2/1; mau: mau_san_pham.csv;
    cau_hinh_nhom: {nhóm: cấu hình}."""
    ten_mau = {r["ma_mau"]: r["ten"] for r in mau}
    nhom_cua_mau = {r["ma_mau"]: r["nhom"] for r in mau}
    tap_cua_mau = {r["ma_mau"]: r["tap"] for r in mau}
    co_dieu_kien = {n: set(thuoc_tinh_co_dieu_kien(ch)) for n, ch in cau_hinh_nhom.items()}
    ma_mau_thu = {b["ma_mau"] for b in bai}
    bai = tinh_bai(bai, tuyen_bo, nhom_cua_mau, co_dieu_kien)
    theo_id = {t["id"]: t for t in tuyen_bo}
    cac_nhan = [{**theo_id[x["id"]], "llm": theo_id[x["id"]]["llm_sinh"], "nhan": x["nhan"], "dong_d": x["dong_d"],
                 "nguoi_gan": x["nguoi_gan"], "tap": tap_cua_mau[theo_id[x["id"]]["ma_mau"]]} for x in nhan2]
    giay_1 = [{"id": x["id"], "ma_mau": theo_id[x["id"]]["ma_mau"], "giay": x["giay"]} for x in nhan1]
    tb_giay = (statistics.fmean([x["giay"] for x in giay_1]), statistics.median([x["giay"] for x in giay_1]))

    dong = ["# Thống kê bộ thử và phương án quy mô (Bước 16)", "",
            "Sinh bằng `scripts/thong_ke_bo_thu.py`. Chỉ có số liệu và phương án, không có kết luận. Số thập phân dùng dấu phẩy.", "",
            f"Bộ thử: {len(bai)} bài, {len(tuyen_bo)} tuyên bố, {len(ma_mau_thu)} mẫu "
            f"({', '.join(o_van_ban(ten_mau[m]) for m in sorted(ma_mau_thu))}).", ""]
    dong += muc_phan_bo_nhan(cac_nhan, ten_mau) + [""]
    dong += muc_so_tuyen_bo(bai, tuyen_bo, nhom_cua_mau, co_dieu_kien, cau_hinh_nhom, ten_mau) + [""]
    dong += muc_thoi_gian(giay_1, nhan2, ten_mau) + [""]
    d, dv = muc_phuong_an(bai, cac_nhan, mau, ma_mau_thu, ten_mau, tb_giay)
    dong += d + muc_gia_dinh(dv, bai, ten_mau, cau_hinh_nhom)
    return dong


# ---------- kiểm nhất quán dữ liệu vào ----------

def kiem_dau_vao(bai, tuyen_bo, nhan2, nhan1):
    """Danh sách lỗi (chuỗi); rỗng là đạt."""
    loi = []
    ma_bai = {b["ma_qc"]: b for b in bai}
    ids = {t["id"] for t in tuyen_bo}
    for ten, nhan in (("lượt 2", nhan2), ("lượt 1", nhan1)):
        if {x["id"] for x in nhan} != ids or len(nhan) != len(ids):
            loi.append(f"nhãn {ten} và tệp tuyên bố không cùng tập mã tuyên bố")
    for t in tuyen_bo:
        b = ma_bai.get(t["ma_qc"])
        if b is None:
            loi.append(f"{t['id']}: bài {t['ma_qc']} không có trong data/quang_cao hoặc không thuộc mẫu bộ thử")
            continue
        for khoa_t, khoa_b in (("llm_sinh", "llm"), ("che_do", "che_do"), ("loai_bai", "loai_bai"), ("ma_mau", "ma_mau")):
            if t[khoa_t] != b[khoa_b]:
                loi.append(f"{t['id']}: {khoa_t} = {t[khoa_t]} khác bài {b['ma_qc']} ({b[khoa_b]})")
    loi += [f"{x['id']}: giay lượt 1 = {x['giay']} không hợp lệ" for x in nhan1
            if not isinstance(x["giay"], (int, float)) or x["giay"] <= 0]
    return loi


def tai_du_lieu():
    """(bai, tuyen_bo, nhan2, nhan1, mau, cau_hinh_nhom) từ các tệp của repo."""
    mau = cau_hinh.doc_mau()
    ma_mau_thu = {r["ma_mau"] for r in mau if r["mau_thu"] == "co"}
    cau_hinh_nhom = {n: cau_hinh.doc_cau_hinh(n) for n in cau_hinh.NHOM}
    return (doc_bai(THU_MUC_QC, ma_mau_thu), doc_jsonl(TEP_TUYEN_BO), doc_jsonl(TEP_NHAN_2), doc_jsonl(TEP_NHAN_1),
            mau, cau_hinh_nhom)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Thống kê bộ thử và phương án quy mô (Bước 16).")
    ap.add_argument("--ra", type=Path, default=TEP_RA, help=f"tệp báo cáo (mặc định {TEP_RA.relative_to(ROOT)})")
    args = ap.parse_args()

    bai, tuyen_bo, nhan2, nhan1, mau, cau_hinh_nhom = tai_du_lieu()
    loi = kiem_dau_vao(bai, tuyen_bo, nhan2, nhan1)
    if loi:
        sys.exit("Dữ liệu vào không nhất quán:\n" + "\n".join(loi))
    dong = tao_bao_cao(bai, tuyen_bo, nhan2, nhan1, mau, cau_hinh_nhom)
    args.ra.parent.mkdir(parents=True, exist_ok=True)
    args.ra.write_text("\n".join(dong) + "\n", encoding="utf-8")
    print("\n".join(dong))
    print(f"\nĐã ghi {args.ra}")


if __name__ == "__main__":
    main()
