"""Báo cáo kiểm việc bỏ ký hiệu chú thích khỏi noi_dung của doan.jsonl -> data/kiem_bo_so_chu_thich.md.

Sinh lại 12 mẫu bằng chia_doan (cùng hàm nhận diện ký hiệu với scripts/chia_doan.py, không có bộ nhận diện riêng),
kiểm doan.jsonl trên đĩa khớp từng byte với bản sinh lại, rồi ghi báo cáo gồm: bảng tổng theo mẫu, danh sách đầy đủ từng
chỗ đã bỏ kèm ngữ cảnh, các chỗ nghi bỏ nhầm và các chỗ có thể còn sót để người kiểm xem. Không sửa doan.jsonl.

Chạy: .venv/Scripts/python.exe scripts/kiem_bo_so_chu_thich.py [--cu <git rev>]
--cu: so noi_dung_goc với noi_dung của doan.jsonl ở bản git đó (bản trước khi bỏ ký hiệu), để kiểm bản gốc không đổi byte nào.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "scripts"))
sys.path.insert(0, str(GOC / "src"))
import chia_doan as cs  # noqa: E402
from kiemchung import chia_doan as cd  # noqa: E402

TEP_BAO_CAO = GOC / "data" / "kiem_bo_so_chu_thich.md"
NGAY = "31/10/2026"
NGU_CANH = 30  # số ký tự lấy mỗi bên chỗ xóa
# Chữ đơn vị liền sau chỗ xóa (cách nhiều nhất một dấu cách): số vừa xóa có thể là số liệu ('pin 8 giờ', '5 W').
DON_VI = re.compile(r" ?(?:giờ|phút|giây|mAh|Wh|W|Hz|nits?|%|mm|cm|km|m|kg|g|x|GB|TB|MB|MP|inch|lần)(?![^\W\d_])")
SO_LE_TRUOC = re.compile(r"(?<!\S)\d{1,2}$")
# Số 1-2 chữ số dính ngay sau chữ thường, dấu đóng ngoặc hoặc dấu % rồi tới khoảng trắng/xuống dòng/hết chuỗi.
CON_SOT = re.compile(r"[a-zà-ỹđ%)](\d{1,2})(?=\s|$)")
# Mã chữ hoa + 1-2 chữ số ở cuối từ ('AI10', 'S25'); nhóm 1 là cả mã, nhóm 2 là số.
MA_HOA = re.compile(r"(?<!\S)(\S*?[A-Z](\d{1,2}))(?=\s|$)")
# Danh sách số dính chữ ('bơi14,15') không có khoảng trắng sau dấu phẩy: CON_SOT không thấy, nên tìm thêm.
CON_SOT_DANH_SACH = re.compile(r"[a-zà-ỹđ%)](\d{1,2}(?:,\d{1,2})+)(?=\s|$)")
LY_DO = {
    "truoc_hoa_hoac_so": "liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305)",
    "sau_la_don_vi": "liền sau là chữ đơn vị (giờ, phút, mAh, W, Hz, %, mm, x...)",
    "khong_co_chu_thich": "trang không có chú thích mang số này",
    "sao_sau_so_le": "dấu * ngay sau một con số đứng riêng (có thể là điểm đánh giá '5*', không phải ký hiệu)",
}


def doc_jsonl(duong):
    return [json.loads(d) for d in Path(duong).read_text(encoding="utf-8").splitlines() if d.strip()]


def sinh_lai(rows):
    """[(ma_mau, [đoạn dạng jsonl], [nhật ký bỏ ký hiệu của từng đoạn])] sinh lại từ page.txt/page.html, đã áp bảng ghi tay."""
    ket_qua = {row["ma_mau"]: cs.chia_mot_mau(row)[0] for row in rows}
    rong = cs.so_chu_so_ma(max(sum(len(d) for _, d in t) for t in ket_qua.values()))
    ra = []
    for row in rows:
        doan = cd.danh_ma_doan(row["ma_mau"], ket_qua[row["ma_mau"]], rong)
        ra.append((row["ma_mau"], doan, [d["ky_hieu_bo"] for d in doan]))
    return ra


def ngu_canh(goc, a, b, do_rong=NGU_CANH):
    """Ngữ cảnh quanh goc[a:b], đánh dấu chỗ đó bằng ⟦ ⟧; xuống dòng thành ⏎; '…' ở phía bị cắt."""
    dau, cuoi = max(0, a - do_rong), min(len(goc), b + do_rong)
    chu = ("…" if dau else "") + goc[dau:a] + "⟦" + goc[a:b] + "⟧" + goc[b:cuoi] + ("…" if cuoi < len(goc) else "")
    return chu.replace("\n", "⏎")


def ma_nghi_ngo(goc, x):
    """Mã lý do (khóa của LY_DO) vì sao chỗ xóa x (một dict của nhật ký) đáng nghi; [] nếu không."""
    a, b = x["vi_tri"], x["vi_tri"] + len(x["chu"])
    truoc, sau = goc[a - 1:a] if a else "", goc[b:b + 1]
    ma = []
    if x["loai"] == cd.KY_HIEU_SO:
        if truoc and (truoc.isupper() or truoc.isdigit()):
            ma.append("truoc_hoa_hoac_so")
        if DON_VI.match(goc, b):
            ma.append("sau_la_don_vi")
        if x["thieu"]:
            ma.append("khong_co_chu_thich")
    elif x["loai"] == cd.KY_HIEU_SAO and SO_LE_TRUOC.search(goc[:a]):
        ma.append("sao_sau_so_le")
    return ma


def tim_ma_hoa_con_lai(noi_dung, so_da_bo):
    """[(a, b)] của mã chữ hoa + số ('AI10', 'X8') còn lại trong noi_dung mà số đó cũng đã bị bỏ như ký hiệu ở chỗ khác
    của mẫu; [a, b) là cả mã. Phần lớn là tên máy ('S25', 'X8'), nhưng 'AI10' là ký hiệu chú thích 10 bị sót."""
    return [(m.start(), m.end()) for m in MA_HOA.finditer(noi_dung) if int(m.group(2)) in so_da_bo]


def tim_sao_con_lai(noi_dung):
    """[(a, b)] của dấu * còn lại trong noi_dung (không bỏ, hoặc chưa được nhận ra là ký hiệu)."""
    return [(m.start(), m.end()) for m in re.finditer(r"\*+", noi_dung)]


def tim_con_sot(noi_dung):
    """[(a, b)] của chữ + số còn lại trong noi_dung mà có thể là ký hiệu chú thích bị sót."""
    ket_qua = [(m.start(), m.end()) for m in CON_SOT.finditer(noi_dung)]
    ket_qua += [(m.start(), m.end()) for m in CON_SOT_DANH_SACH.finditer(noi_dung)]
    return sorted(ket_qua)


def kiem_bat_bien(ma_mau, doan, nhat_ky, cu=None):
    """(lỗi so với bản git cũ, lỗi việc bỏ ký hiệu) của một mẫu; rỗng là đạt.

    doan: đoạn dạng jsonl vừa sinh lại; nhat_ky: nhật ký bỏ ký hiệu của từng đoạn; cu: đoạn của bản git trước (hoặc None).
    """
    loi_cu, loi = [], []
    if cu is not None and len(cu) != len(doan):
        loi_cu.append(f"{ma_mau}: số đoạn đổi {len(cu)} -> {len(doan)}")
        cu = None
    for i, (d, nk) in enumerate(zip(doan, nhat_ky)):
        goc, nd = d["noi_dung_goc"], d["noi_dung"]
        if cu is not None:
            c = cu[i]
            if d["noi_dung_goc"] != c["noi_dung"]:
                loi_cu.append(f"{d['id']}: noi_dung_goc khác noi_dung cũ")
            for k in c:
                if k != "noi_dung" and c[k] != d.get(k):
                    loi_cu.append(f"{d['id']}: trường {k} đổi")
        con_lai, dau = [], 0
        for x in sorted(nk, key=lambda x: x["vi_tri"]):
            a = x["vi_tri"]
            if goc[a:a + len(x["chu"])] != x["chu"] or a < dau:
                loi.append(f"{d['id']}: nhật ký lệch văn bản tại {a}")
            con_lai.append(goc[dau:a])
            dau = a + len(x["chu"])
        con_lai.append(goc[dau:])
        if "".join("".join(con_lai).split()) != "".join(nd.split()):
            loi.append(f"{d['id']}: bỏ các ký hiệu đã ghi khỏi noi_dung_goc không ra noi_dung")
        if not nk and goc != nd:
            loi.append(f"{d['id']}: không có ký hiệu bị bỏ mà noi_dung khác noi_dung_goc")
    return loi_cu, loi


def doc_cu_tu_git(ma_mau, rev):
    kq = subprocess.run(["git", "show", f"{rev}:data/nguon/{ma_mau}/doan.jsonl"], capture_output=True, cwd=GOC)
    if kq.returncode:
        sys.exit(f"git show {rev} lỗi cho {ma_mau}: {kq.stderr.decode('utf-8', 'replace')}")
    return [json.loads(d) for d in kq.stdout.decode("utf-8").splitlines() if d.strip()]


def code(chu):
    """Chuỗi trong cặp dấu ` an toàn với Markdown."""
    rao = "``" if "`" in chu else "`"
    return f"{rao} {chu} {rao}" if "`" in chu else f"{rao}{chu}{rao}"


def dem_theo_mau(doan, nhat_ky):
    """(đoạn, đoạn đổi, chỗ xóa, số, sao, sao nối liền, ghi tay): số ký hiệu số tính từng số, không tính từng cụm."""
    tat_ca = [x for nk in nhat_ky for x in nk]
    return (len(doan), sum(1 for d in doan if d["noi_dung"] != d["noi_dung_goc"]), len(tat_ca),
            sum(len(x["so"]) for x in tat_ca if x["loai"] == cd.KY_HIEU_SO),
            sum(1 for x in tat_ca if x["loai"] == cd.KY_HIEU_SAO),
            sum(1 for x in tat_ca if x["loai"] == cd.KY_HIEU_SAO_NOI_LIEN),
            sum(len(x["so"]) for x in tat_ca if x["loai"] == cd.KY_HIEU_GHI_TAY))


SUP_HTML = re.compile(r"<(a|span|sup)\b[^>]*(?:data-sup|class=\"[^\"]*(?:sup|footnote)[^\"]*\")[^>]*>(.*?)</\1>", re.S)


def phang(chu):
    return re.sub(r"\s+", "", unicodedata.normalize("NFC", chu))


def doi_chieu_sup(ket_qua):
    """{ma_mau: {'goc': số cặp (đoạn, chữ + số) từ thẻ sup có trong noi_dung_goc, 'con': số cặp còn trong noi_dung, 'ds_con': [...]}}.

    Mỗi thẻ sup (hoặc liên kết ký hiệu) chứa 1-2 chữ số trong page.html được ghép với 14 ký tự chữ đứng trước; tìm chuỗi đó (bỏ khoảng
    trắng, số không được dính thêm chữ số sau) trong từng đoạn."""
    ra = {}
    for ma, doan, _ in ket_qua:
        goc, nd = {d["id"]: phang(d["noi_dung_goc"]) for d in doan}, {d["id"]: phang(d["noi_dung"]) for d in doan}
        cap_goc, cap_con = set(), set()
        for tep in (cs.OUT_ROOT / ma / "page.html", cs.OUT_ROOT / ma / "bo_sung" / "page.html"):
            if not tep.exists():
                continue
            h = tep.read_text(encoding="utf-8")
            for m in SUP_HTML.finditer(h):
                so = phang(cd.van_ban_cua_html(m.group(2)))
                if not re.fullmatch(r"\d{1,2}", so):
                    continue
                cat = re.sub(r"<(script|style)\b.*?</\1>", " ", h[max(0, m.start() - 500):m.start()], flags=re.S)
                truoc = phang(cd.van_ban_cua_html(cat))[-14:]
                if not truoc:
                    continue
                mau = re.compile(re.escape(truoc + so) + r"(?!\d)")
                for i in goc:
                    if mau.search(goc[i]):
                        cap_goc.add((i, truoc + so))
                    if mau.search(nd[i]):
                        cap_con.add((i, truoc + so))
        ra[ma] = {"goc": len(cap_goc), "con": len(cap_con), "ds_con": sorted(cap_con)}
    return ra


def phan_bang_ghi_tay(ket_qua):
    """Các dòng Markdown của mục 7: bảng bỏ thêm ghi tay (KY_HIEU_BO_THEM) và bảng giữ lại (KY_HIEU_GIU_LAI)."""
    theo_id = {d["id"]: d for _, doan, _ in ket_qua for d in doan}
    them = [(d, x) for d in theo_id.values() for x in d["ky_hieu_bo"] if x["loai"] == cd.KY_HIEU_GHI_TAY]
    dong = [f"## 7. Bảng ghi tay ({len(cd.KY_HIEU_BO_THEM)} mục bỏ thêm, {len(cd.KY_HIEU_GIU_LAI)} mục giữ lại)", "",
            "Hai hằng trong `src/kiemchung/chia_doan.py`, mỗi mục gồm mã đoạn, ngữ cảnh trong `noi_dung_goc` (chứa ký hiệu đúng một lần) và ký hiệu. "
            "Chỉ đổi `noi_dung`; `chu_thich` và cách gắn chú thích không đổi. Mục không tìm thấy ngữ cảnh, hoặc đã được bỏ rồi, là lỗi (`ValueError`) "
            "chứ không bị bỏ qua. Mỗi mục đã đối chiếu thẻ `<sup>` của `page.html`.", "",
            f"### 7.1 Ký hiệu bỏ thêm (`KY_HIEU_BO_THEM`): {len(cd.KY_HIEU_BO_THEM)} mục, {len(them)} chỗ", "",
            "| Mẫu | Số mục | Số chỗ đã bỏ |", "|---|---:|---:|"]
    for ma, _, _ in ket_qua:
        muc = sum(1 for i, _, _ in cd.KY_HIEU_BO_THEM if i.startswith(ma + "#"))
        cho = sum(1 for d, _ in them if d["ma_mau"] == ma)
        if muc or cho:
            dong.append(f"| {ma} | {muc} | {cho} |")
    dong += ["", "Từng chỗ (mã đoạn, ký hiệu, ngữ cảnh trước khi bỏ; `⟦…⟧` là chỗ bỏ):", ""]
    dong += [f"- `{d['id']}` · {code(x['chu'])} · {noi_xoa(d, x)}" for d, x in them]
    dong += ["", f"### 7.2 Ngoại lệ giữ lại (`KY_HIEU_GIU_LAI`): {len(cd.KY_HIEU_GIU_LAI)} mục", "",
             "Ký hiệu mà nhận diện đã nhận nhưng không phải ký hiệu chú thích, giữ nguyên trong `noi_dung` (ngữ cảnh lấy từ `noi_dung`):", ""]
    for ma_doan, ngu_canh_muc, ky in cd.KY_HIEU_GIU_LAI:
        d = theo_id[ma_doan]
        cho = cd.vi_tri_ky_hieu_trong_ngu_canh(ma_doan, d["noi_dung"], ngu_canh_muc, ky)
        dong += [f"- `{ma_doan}` · {code(ky)} · {code(ngu_canh(d['noi_dung'], a, b))}" for a, b in cho]
    return dong + [""]


def noi_xoa(d, x):
    """Ngữ cảnh (trong noi_dung_goc của đoạn d) của chỗ xóa x, bọc trong code Markdown."""
    return code(ngu_canh(d["noi_dung_goc"], x["vi_tri"], x["vi_tri"] + len(x["chu"])))


def phan_bat_bien(loi):
    """Các dòng Markdown nêu kết quả kiểm bất biến; loi: {'khop_dia': [...], 'cu': [...], 'bo': [...], 'rev': str}."""
    def ket_qua(ds):
        return "**đạt**" if not ds else "**KHÔNG đạt**"
    dong = ["## Bất biến đã kiểm bằng code", "",
            f"- Bản sinh lại từ `page.txt`/`page.html` giống `doan.jsonl` trên đĩa từng byte: {ket_qua(loi['khop_dia'])}."]
    dong += [f"  - {e}" for e in loi["khop_dia"]]
    if loi["rev"]:
        dong.append(f"- `noi_dung_goc` bằng `noi_dung` của bản git `{loi['rev']}` (trước khi bỏ ký hiệu) cho mọi đoạn, và `id`, `ma_mau`, "
                    f"`trang`, `muc`, `chu_thich`, `dong`, số đoạn, thứ tự không đổi: {ket_qua(loi['cu'])}.")
        dong += [f"  - {e}" for e in loi["cu"]]
    dong.append("- Với mọi đoạn, bỏ các ký hiệu đã ghi nhận khỏi `noi_dung_goc` ra đúng `noi_dung` (không kể khoảng trắng; khoảng trắng "
                f"chỉ đổi ở các chỗ ghi ở mục 2), đoạn không có ký hiệu thì `noi_dung` = `noi_dung_goc`: {ket_qua(loi['bo'])}.")
    dong += [f"  - {e}" for e in loi["bo"]]
    return dong + [""]


def viet_bao_cao(ket_qua, loi):
    """Nội dung data/kiem_bo_so_chu_thich.md."""
    dem = {ma: dem_theo_mau(doan, nk) for ma, doan, nk in ket_qua}
    tong = [sum(v[i] for v in dem.values()) for i in range(7)]
    tat_ca = [(d, x) for _, doan, nk in ket_qua for d, n in zip(doan, nk) for x in n]
    chen = [(d, x) for d, x in tat_ca if x["xu_ly"] == "chen_cach"]
    giua = [(d, x) for d, x in tat_ca if x["xu_ly"] == "bo_cach_sau"]
    cuoi_dong = sum(1 for _, x in tat_ca if x["xu_ly"] == "bo_cach_truoc")
    nghi = [(d, x, ma_nghi_ngo(d["noi_dung_goc"], x)) for d, x in tat_ca]
    nghi = [t for t in nghi if t[2]]

    dong = [f"# Kiểm việc bỏ ký hiệu chú thích khỏi noi_dung ({NGAY})", "",
            "Số chú thích của trang hãng (trên web là chữ số nhỏ in cao: `Thấp8`, `20 phút6`, ` 1, 4, 5` ở cuối dòng) và dấu `*`, `**` "
            "làm ký hiệu chú thích đã bị bỏ khỏi `noi_dung` của `data/nguon/<ma_mau>/doan.jsonl`; `noi_dung_goc` giữ văn bản trước khi bỏ, "
            "từng byte. Phần lớn là các khoảng mà `chia_doan` đã dùng để gắn chú thích vào đoạn (`chuan_bi_manh`), không có bộ nhận diện riêng; "
            "ký hiệu thật mà nhận diện đó bỏ sót thì bỏ thêm bằng bảng ghi tay `KY_HIEU_BO_THEM` (mục 7). "
            "Số trong tên mã (`IP68`, `Buds3`, `A2305`), số liệu (`5.000mAh`) và `USB-C` không phải ký hiệu nên còn nguyên. Ba ngoại lệ "
            "cho dấu `*` mà `chia_doan` vẫn nhận ra (để gắn chú thích) nhưng không bỏ: dấu `*` mà trang không có dòng chú thích nào bắt đầu bằng "
            "đúng chuỗi đó, dấu `*` đứng giữa hai khoảng trắng (nhãn đọc màn hình \"Chú thích * biểu tượng\" của Apple), và `5*` trong lời "
            "đánh giá (điểm 5 sao) giữ lại bằng bảng ghi tay `KY_HIEU_GIU_LAI`. "
            "Báo cáo này do `scripts/kiem_bo_so_chu_thich.py` sinh ra; mục 4 đến 6 là việc để người kiểm xem, mục 7 liệt kê hai bảng ghi tay.", ""]
    dong += phan_bat_bien(loi)
    dong += ["## 1. Bảng tổng", "",
             "| Mẫu | Đoạn | Đoạn đổi | Chỗ xóa | Ký hiệu số | Ký hiệu sao `*` | Sao mở chú thích nối liền | Số bỏ bằng bảng ghi tay |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    dong += [f"| {ma} | " + " | ".join(str(x) for x in v) + " |" for ma, v in dem.items()]
    dong += ["| **Cộng** | " + " | ".join(f"**{x}**" for x in tong) + " |", "",
             "- Chỗ xóa là một cụm liền nhau (`14, 15` là một chỗ, hai ký hiệu số). Ký hiệu sao là dấu `*`/`**` đứng sau chữ làm ký hiệu "
             "(`IP68**`, `24 tháng.*`); sao mở chú thích nối liền là dấu `*` dính liền chữ sau mà `chia_doan` đã bóc nội dung chú thích đó "
             "đi (`194g*`, `Hz**`), nội dung chú thích nằm ở `chu_thich`. Cột cuối là số ký hiệu số bỏ bằng bảng ghi tay (đã tính vào "
             "Chỗ xóa, không tính vào cột Ký hiệu số).",
             "- Đoạn Galaxy Watch8 phần lớn lấy từ PDF hướng dẫn sử dụng nên không có ký hiệu để bỏ; chỉ trang chính (`url`) có.", ""]

    dong += ["## 2. Chỗ chỉnh khoảng trắng khi bỏ", "",
             f"- Ký hiệu dính liền chữ sau không có khoảng trắng (`2.560Hz**Gam màu`), đã chèn một dấu cách để hai chữ không dính nhau: **{len(chen)}** chỗ."]
    dong += [f"  - `{d['id']}` {code(x['chu'])}: {noi_xoa(d, x)} -> {code(ngu_canh(d['noi_dung'], x['vi_tri_moi'], x['vi_tri_moi']))}"
             for d, x in chen]
    dong += [f"- Ký hiệu nằm giữa hai dấu cách: bỏ một dấu cách để còn đúng một, **{len(giua)}** chỗ."]
    dong += [f"  - `{d['id']}` {code(x['chu'])}: {noi_xoa(d, x)}" for d, x in giua]
    dong += [f"- Ký hiệu cuối dòng đứng sau một dấu cách (`năng lượng! 7`): bỏ luôn dấu cách đó, **{cuoi_dong}** chỗ (không liệt kê).", ""]

    dong += [f"## 3. Danh sách đầy đủ từng chỗ đã xóa ({len(tat_ca)} chỗ)", "",
             "Mỗi dòng: mã đoạn, loại, ký hiệu đã xóa, ngữ cảnh khoảng 30 ký tự mỗi bên (`⟦…⟧` là chỗ xóa, `⏎` là xuống dòng).", ""]
    ten_loai = {cd.KY_HIEU_SO: "số", cd.KY_HIEU_SAO: "sao", cd.KY_HIEU_SAO_NOI_LIEN: "sao nối liền", cd.KY_HIEU_GHI_TAY: "số (ghi tay)"}
    for ma, doan, nk in ket_qua:
        co = [(d, x) for d, n in zip(doan, nk) for x in n]
        dong += [f"### {ma} ({len(co)} chỗ)", ""]
        dong += [f"- `{d['id']}` · {ten_loai[x['loai']]} {code(x['chu'])} · {noi_xoa(d, x)}" for d, x in co]
        dong.append("")

    dong += [f"## 4. Nghi xóa nhầm ({len(nghi)} chỗ)", "",
             "Chỗ xóa có ít nhất một dấu hiệu: ký tự liền trước là chữ HOA hoặc chữ số (kiểu `IP68`, `Buds3`, `A2305`); liền sau (cách nhiều nhất một "
             "dấu cách) là chữ đơn vị (giờ, phút, mAh, W, Hz, nit, %, m, mm, x...); số đã xóa không có chú thích tương ứng trong bảng chú thích của trang; "
             "hoặc dấu `*` ngay sau một con số đứng riêng. Người kiểm xem từng chỗ có đúng là ký hiệu không (ví dụ `MIMO8`, `25W6` là ký hiệu thật).", ""]
    dong += [f"- `{d['id']}` · {code(x['chu'])} · {'; '.join(LY_DO[m] for m in ma)} · {noi_xoa(d, x)}" for d, x, ma in nghi] or ["(Không có chỗ nào.)"]
    dong.append("")

    sot = [(ma, d, a, b) for ma, doan, _ in ket_qua for d in doan for a, b in tim_con_sot(d["noi_dung"])]
    dong += [f"## 5. Có thể còn sót ({len(sot)} chỗ theo regex, thêm mã chữ hoa ở 5.2)", "",
             "### 5.1 Chữ thường, `)` hoặc `%` liền ngay sau là 1-2 chữ số", "",
             "Trong `noi_dung` mới: chữ thường, dấu đóng ngoặc hoặc dấu % liền ngay sau là 1-2 chữ số rồi tới khoảng trắng, xuống dòng hoặc hết chuỗi "
             "(regex `[a-zà-ỹđ%)]\\d{1,2}(?=\\s|$)`), thêm danh sách số dính chữ không cách (`bơi14,15`). Nhiều chỗ là tên máy hoặc số liệu "
             "(`Buds3`, `Watch8`, `4x4`) hoặc tên người dùng trong đánh giá. **Không tự xóa**: người kiểm xem có phải ký hiệu bị sót không. "
             "Các ký hiệu thật từng bị sót (`30 phút6`, `AI10`, `xong1`, `nhất2,3`, `Samsung34`...) đã bỏ bằng bảng ghi tay ở mục 7; mục 5.3 đối "
             "chiếu lại với thẻ `<sup>` của `page.html` để chắc không còn ký hiệu thật nào trong `noi_dung`.", ""]
    for ma, doan, _ in ket_qua:
        cua = [t for t in sot if t[0] == ma]
        if not cua:
            continue
        hay_gap = Counter(t[1]["noi_dung"][t[2]:t[3]] for t in cua).most_common(8)
        dong += [f"#### {ma} ({len(cua)} chỗ)", "", "Hay gặp: " + ", ".join(f"{code(k)} ×{n}" for k, n in hay_gap), ""]
        dong += [f"- `{d['id']}` · {code(d['noi_dung'][a:b])} · {code(ngu_canh(d['noi_dung'], a + 1, b))}" for _, d, a, b in cua]
        dong.append("")

    dong += ["### 5.2 Mã chữ hoa + số, số đó cũng đã bị bỏ như ký hiệu ở chỗ khác của mẫu", "",
             "Regex ở 5.1 không thấy chữ hoa. Bảng này gom mã chữ hoa + 1-2 chữ số còn trong `noi_dung` (ví dụ `AI10`, `X8`, `S25`) mà số đó "
             "cũng đã bị bỏ như ký hiệu trong cùng mẫu. Phần còn lại là tên máy "
             "hoặc tên chuẩn (`AV1`, `HDR10`). `AI10` của Xiaomi 15T trước đây nằm ở đây nay đã bỏ bằng bảng ghi tay.", "",
             "| Mẫu | Mã | Số lần | Ví dụ |", "|---|---|---:|---|"]
    co_hang = False
    for ma, doan, nk in ket_qua:
        da_bo = {k for n in nk for x in n for k in x["so"]}
        dem_ma, vi_du = Counter(), {}
        for d in doan:
            for a, b in tim_ma_hoa_con_lai(d["noi_dung"], da_bo):
                ten = d["noi_dung"][a:b]
                dem_ma[ten] += 1
                vi_du.setdefault(ten, d["id"])
        for ten, n in dem_ma.most_common():
            dong.append(f"| {ma} | {code(ten)} | {n} | `{vi_du[ten]}` |")
            co_hang = True
    if not co_hang:
        dong.append("| (không có) | | | |")
    dong.append("")

    sup = doi_chieu_sup(ket_qua)
    dong += ["### 5.3 Đối chiếu với thẻ `<sup>` của page.html", "",
             "Mỗi số trong thẻ `<sup>` hoặc liên kết ký hiệu (`data-sup`, `click_sup`) của `page.html`, ghép với 14 ký tự chữ đứng trước nó, được tìm "
             "trong `noi_dung_goc` (ký hiệu có trong văn bản) và trong `noi_dung` (ký hiệu còn sót), bỏ qua khoảng trắng. Con số là số cặp (đoạn, chữ + số) "
             "tìm được; 0 nghĩa là mục này không đối chiếu được (OPPO, AirPods 4 dùng thẻ khác; các trang Xiaomi dùng dấu `*`), "
             "các mẫu đó chỉ có 5.1 và 5.2.", "",
             "| Mẫu | Có trong noi_dung_goc | Còn trong noi_dung |", "|---|---:|---:|"]
    dong += [f"| {ma} | {v['goc']} | {v['con']} |" for ma, v in sup.items()]
    con = [(ma, i, ct) for ma, v in sup.items() for i, ct in v["ds_con"]]
    dong += ["", "Còn lại trong `noi_dung`: " + (", ".join(f"`{i}` {code(ct)}" for _, i, ct in con) if con else "không có."), ""]

    sao = [(d, a, b) for _, doan, _ in ket_qua for d in doan for a, b in tim_sao_con_lai(d["noi_dung"])]
    dong += [f"## 6. Dấu `*` còn lại trong noi_dung ({len(sao)} chỗ)", "",
             "Dấu `*` chưa bị bỏ: không được `chia_doan` nhận là ký hiệu (ví dụ `(*Bật AOD)`), hoặc được nhận nhưng thuộc ba ngoại lệ nói ở đầu báo cáo.", ""]
    dong += [f"- `{d['id']}` · {code(d['noi_dung'][a:b])} · {code(ngu_canh(d['noi_dung'], a, b))}" for d, a, b in sao] or ["(Không có chỗ nào.)"]
    dong.append("")
    dong += phan_bang_ghi_tay(ket_qua)
    return "\n".join(dong).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Báo cáo kiểm việc bỏ ký hiệu chú thích khỏi noi_dung.")
    ap.add_argument("--cu", help="bản git (vd. HEAD) có doan.jsonl trước khi bỏ ký hiệu, để kiểm noi_dung_goc")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    rows = cs.doc_mau()
    ket_qua = sinh_lai(rows)
    loi = {"khop_dia": [], "cu": [], "bo": [], "rev": ""}
    for ma, doan, nk in ket_qua:
        tren_dia = (cs.OUT_ROOT / ma / "doan.jsonl").read_text(encoding="utf-8")
        if tren_dia != "".join(json.dumps({k: d[k] for k in cs.TRUONG_JSONL}, ensure_ascii=False) + "\n" for d in doan):
            loi["khop_dia"].append(f"{ma}: doan.jsonl trên đĩa khác bản sinh lại (chạy scripts/chia_doan.py)")
        cu = doc_cu_tu_git(ma, args.cu) if args.cu else None
        loi_cu, loi_bo = kiem_bat_bien(ma, doan, nk, cu)
        loi["cu"] += loi_cu
        loi["bo"] += loi_bo
    loi["rev"] = subprocess.run(["git", "rev-parse", "--short", args.cu], capture_output=True, text=True,
                                cwd=GOC).stdout.strip() if args.cu else ""
    TEP_BAO_CAO.write_text(viet_bao_cao(ket_qua, loi), encoding="utf-8", newline="\n")
    dem = [dem_theo_mau(doan, nk) for _, doan, nk in ket_qua]
    print(f"Ghi {TEP_BAO_CAO.relative_to(GOC)}: {sum(v[1] for v in dem)}/{sum(v[0] for v in dem)} đoạn đổi, "
          f"{sum(v[3] for v in dem)} ký hiệu số, {sum(v[4] for v in dem)} dấu sao, {sum(v[5] for v in dem)} sao nối liền, "
          f"{sum(v[6] for v in dem)} số bỏ bằng bảng ghi tay.")
    tat_ca_loi = [e for k, v in loi.items() if k != "rev" for e in v]
    if tat_ca_loi:
        print(f"Có {len(tat_ca_loi)} lỗi bất biến:\n  " + "\n  ".join(tat_ca_loi[:20]))
        return 1
    print("Bất biến đạt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
