"""Đo độ nhất quán giữa nhãn lượt 3 và nhãn lượt 2 của bộ thử, ghi ket_qua/bo_thu/nhat_quan_luot3.md.

So hai tệp nhãn (mặc định data/nhan/thu_luot3.jsonl với data/nhan/thu_luot2.jsonl) trên các mã có ở cả hai tệp: tỷ lệ đồng ý,
kappa của Cohen cho bốn nhãn (DUNG, SAI, LECH, CHUA_DU), kappa của riêng nhãn Lệch (Lệch so với không Lệch), bảng nhầm lẫn
(hàng: lượt 2, cột: lượt 3) và danh sách tuyên bố khác nhãn. Mã chỉ có ở một tệp được liệt kê và không tính vào số đo.

Ý nghĩa của số đo (ghi trong báo cáo): nhãn lượt 2 là "Claude gán, người thực hiện duyệt"; lượt 3 do chính người thực hiện
gán lại mù một phần bộ thử sau vài ngày. Vì vậy đây là độ nhất quán của một người với nhãn chuẩn, không phải độ đồng thuận
giữa hai người; nó không thay cho kappa giữa hai người của kế hoạch (Bước 32) khi có người gán thứ hai.

Chạy: .venv/Scripts/python.exe -X utf8 scripts/do_nhat_quan.py [tep_luot3 [tep_luot2]] [--ra ket_qua/bo_thu/nhat_quan_luot3.md]
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

GOC = Path(__file__).resolve().parents[1]
TEP_LUOT3 = GOC / "data" / "nhan" / "thu_luot3.jsonl"
TEP_LUOT2 = GOC / "data" / "nhan" / "thu_luot2.jsonl"
TEP_TUYEN_BO = GOC / "data" / "tuyen_bo" / "thu.jsonl"
TEP_RA = GOC / "ket_qua" / "bo_thu" / "nhat_quan_luot3.md"

NHAN = ("DUNG", "SAI", "LECH", "CHUA_DU")
NHAN_LECH = "LECH"
KHONG_LECH = "KHONG_LECH"


def doc_nhan(duong):
    """{mã: bản ghi nhãn} của một tệp nhãn. ValueError (nói rõ tệp và dòng) nếu dòng hỏng, thiếu id, nhãn lạ hoặc mã lặp."""
    ten = Path(duong).name
    ra = {}
    with open(duong, encoding="utf-8-sig") as f:
        for so, dong in enumerate(f, 1):
            if not dong.strip():
                continue
            try:
                nh = json.loads(dong)
            except json.JSONDecodeError as e:
                raise ValueError(f"{ten} dòng {so}: không phải JSON hợp lệ ({e.msg})") from None
            if not isinstance(nh, dict) or not isinstance(nh.get("id"), str):
                raise ValueError(f"{ten} dòng {so}: mỗi dòng phải là đối tượng JSON có id (chuỗi)")
            if nh.get("nhan") not in NHAN:
                raise ValueError(f"{ten} dòng {so} ({nh['id']}): nhan {nh.get('nhan')!r} không thuộc {', '.join(NHAN)}")
            if nh["id"] in ra:
                raise ValueError(f"{ten} dòng {so}: id {nh['id']} lặp")
            ra[nh["id"]] = nh
    return ra


def doc_cau(duong):
    """{mã: chữ tuyên bố} từ tệp tuyên bố; {} nếu không có tệp (báo cáo vẫn ra, thiếu cột tuyên bố)."""
    if not duong or not Path(duong).exists():
        return {}
    with open(duong, encoding="utf-8-sig") as f:
        return {d["id"]: d.get("tuyen_bo", "") for d in map(json.loads, (x for x in f if x.strip()))}


def kappa_cohen(cap):
    """Kappa của Cohen của danh sách cặp (nhãn A, nhãn B); lớp nhãn lấy từ chính các cặp. None nếu không xác định: không có
    cặp nào, hoặc mẫu số 1 - pe bằng 0 (cả hai bên chỉ dùng cùng một nhãn, nên không có gì để trừ phần trùng do ngẫu nhiên)."""
    n = len(cap)
    if n == 0:
        return None
    po = sum(1 for a, b in cap if a == b) / n
    dem_a, dem_b = Counter(a for a, _ in cap), Counter(b for _, b in cap)
    pe = sum(dem_a[k] * dem_b[k] for k in dem_a.keys() | dem_b.keys()) / (n * n)
    if pe >= 1:
        return None
    return (po - pe) / (1 - pe)


def la_lech(nhan):
    return NHAN_LECH if nhan == NHAN_LECH else KHONG_LECH


def do_nhat_quan(nhan3, nhan2):
    """Số đo của hai tệp nhãn đã đọc ({mã: bản ghi}). Cặp là (lượt 2, lượt 3) theo từng mã chung."""
    chung = sorted(set(nhan3) & set(nhan2))
    cap = [(nhan2[m]["nhan"], nhan3[m]["nhan"]) for m in chung]
    cap_lech = [(la_lech(a), la_lech(b)) for a, b in cap]
    dem = Counter(cap)
    dem_lech = Counter(cap_lech)
    return {
        "n": len(chung), "chung": chung, "chi_o_luot3": sorted(set(nhan3) - set(nhan2)),
        "chi_o_luot2": sorted(set(nhan2) - set(nhan3)),
        "khop": sum(1 for a, b in cap if a == b), "kappa_4": kappa_cohen(cap),
        "khop_lech": sum(1 for a, b in cap_lech if a == b), "kappa_lech": kappa_cohen(cap_lech),
        "bang": {(a, b): dem[(a, b)] for a in NHAN for b in NHAN},
        "bang_lech": {(a, b): dem_lech[(a, b)] for a in (NHAN_LECH, KHONG_LECH) for b in (NHAN_LECH, KHONG_LECH)},
        "khac": [{"id": m, "luot2": nhan2[m], "luot3": nhan3[m]} for m in chung if nhan2[m]["nhan"] != nhan3[m]["nhan"]],
        "lech_luot2": sum(1 for a, _ in cap if a == NHAN_LECH), "lech_luot3": sum(1 for _, b in cap if b == NHAN_LECH),
    }


def so_thap_phan(x, chu_so=3):
    """Số kiểu tiếng Việt (dấu phẩy thập phân); None thì ghi "không xác định"."""
    return "không xác định" if x is None else f"{x:.{chu_so}f}".replace(".", ",")


def phan_tram(tu, mau):
    return "không có" if mau == 0 else f"{100 * tu / mau:.1f}".replace(".", ",") + "%"


def _o(s):
    """Chữ trong ô bảng markdown: không để `|` hay xuống dòng phá bảng."""
    return " ".join(str(s).split()).replace("|", "\\|")


def _nhan_dong(nh):
    """`LECH (D4)`: nhãn kèm dòng D người gán dừng ở nếu có."""
    return f"{nh['nhan']} ({nh['dong_d']})" if nh.get("dong_d") else nh["nhan"]


def bang_nham_lan_md(bang, nhan, tieu_de_hang, tieu_de_cot):
    dong = [f"| {tieu_de_hang} \\ {tieu_de_cot} | " + " | ".join(nhan) + " | Tổng |", "|---|" + "---:|" * (len(nhan) + 1)]
    for a in nhan:
        so = [bang[(a, b)] for b in nhan]
        dong.append(f"| **{a}** | " + " | ".join(map(str, so)) + f" | {sum(so)} |")
    cot = [sum(bang[(a, b)] for a in nhan) for b in nhan]
    dong.append("| **Tổng** | " + " | ".join(map(str, cot)) + f" | {sum(cot)} |")
    return dong


def viet_bao_cao(kq, ten_luot3="thu_luot3.jsonl", ten_luot2="thu_luot2.jsonl", cau=None):
    """Báo cáo markdown của kết quả do_nhat_quan. cau: {mã: chữ tuyên bố} (tùy chọn) để hiện ở danh sách khác nhãn."""
    cau = cau or {}
    n = kq["n"]
    d = [
        "# Độ nhất quán nhãn lượt 3 với lượt 2 (bộ thử)",
        "",
        f"- Nguồn: `{ten_luot3}` (lượt 3) so với `{ten_luot2}` (lượt 2). Sinh bằng `scripts/do_nhat_quan.py`.",
        f"- Số tuyên bố chung hai lượt: {n}.",
    ]
    if kq["chi_o_luot3"]:
        d.append(f"- Chỉ có ở lượt 3, không tính: {len(kq['chi_o_luot3'])} ({', '.join(kq['chi_o_luot3'])}).")
    if kq["chi_o_luot2"]:
        d.append(f"- Chỉ có ở lượt 2, không tính: {len(kq['chi_o_luot2'])}.")
    d += [
        "",
        "## Số đo này là gì",
        "",
        "- Nhãn lượt 2 là **Claude gán, người thực hiện duyệt**. Nhãn lượt 3 do **chính người thực hiện gán lại mù** một phần "
        "bộ thử, sau vài ngày, vì không tìm được người gán thứ hai.",
        "- Vì vậy kết quả là **độ nhất quán của một người với nhãn chuẩn**, không phải độ đồng thuận giữa hai người. Nó không "
        "thay cho kappa giữa hai người gán độc lập; không dùng nó để báo là đã có kappa giữa hai người.",
        "- Người gán lượt 3 cũng là người đã duyệt nhãn lượt 2, nên độ nhất quán ở đây có thể cao hơn so với một người thứ "
        "hai chưa thấy nhãn nào.",
        f"- Mẫu chung có {n} tuyên bố, trong đó {kq['lech_luot2']} Lệch theo lượt 2. Nếu mẫu được chọn có chủ đích theo nhãn "
        "lượt 2 (mọi tuyên bố Lệch cộng một phần ngẫu nhiên của số còn lại) thì tỷ lệ Lệch trong mẫu cao hơn trong cả bộ thử, "
        "mà kappa phụ thuộc tỷ lệ này. Với cỡ mẫu nhỏ, kappa dao động mạnh; báo cáo này không tính khoảng tin cậy.",
        "",
        "## Kết quả",
        "",
        "| Số đo | Giá trị |",
        "|---|---|",
        f"| Tỷ lệ đồng ý, bốn nhãn | {kq['khop']}/{n} = {phan_tram(kq['khop'], n)} |",
        f"| Kappa của Cohen, bốn nhãn (DUNG, SAI, LECH, CHUA_DU) | {so_thap_phan(kq['kappa_4'])} |",
        f"| Tỷ lệ đồng ý, Lệch so với không Lệch | {kq['khop_lech']}/{n} = {phan_tram(kq['khop_lech'], n)} |",
        f"| Kappa của Cohen, riêng nhãn Lệch (Lệch so với không Lệch) | {so_thap_phan(kq['kappa_lech'])} |",
        f"| Số tuyên bố Lệch | lượt 2: {kq['lech_luot2']}, lượt 3: {kq['lech_luot3']} |",
        "",
        "Kappa không xác định khi cả hai lượt chỉ dùng cùng một nhãn (không có gì để trừ phần trùng do ngẫu nhiên).",
        "",
        "## Bảng nhầm lẫn bốn nhãn (hàng: lượt 2, cột: lượt 3)",
        "",
    ]
    d += bang_nham_lan_md(kq["bang"], NHAN, "Lượt 2", "Lượt 3")
    d += ["", "## Bảng nhầm lẫn Lệch so với không Lệch (hàng: lượt 2, cột: lượt 3)", ""]
    d += bang_nham_lan_md(kq["bang_lech"], (NHAN_LECH, KHONG_LECH), "Lượt 2", "Lượt 3")
    d += ["", f"## Tuyên bố khác nhãn ({len(kq['khac'])})", ""]
    if not kq["khac"]:
        d.append("Không có: mọi tuyên bố chung đều cùng nhãn ở hai lượt.")
    else:
        co_cau = any(cau.get(x["id"]) for x in kq["khac"])
        d += ["| Mã | Lượt 2 (dòng D) | Lượt 3 (dòng D) |" + (" Tuyên bố |" if co_cau else ""),
              "|---|---|---|" + ("---|" if co_cau else "")]
        for x in kq["khac"]:
            d.append(f"| {x['id']} | {_o(_nhan_dong(x['luot2']))} | {_o(_nhan_dong(x['luot3']))} |"
                     + (f" {_o(cau.get(x['id'], ''))} |" if co_cau else ""))
    return "\n".join(d) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Đo độ nhất quán nhãn lượt 3 với lượt 2 của bộ thử.")
    ap.add_argument("tep_luot3", type=Path, nargs="?", default=TEP_LUOT3, help="mặc định data/nhan/thu_luot3.jsonl")
    ap.add_argument("tep_luot2", type=Path, nargs="?", default=TEP_LUOT2, help="mặc định data/nhan/thu_luot2.jsonl")
    ap.add_argument("--tuyen-bo", type=Path, default=TEP_TUYEN_BO,
                    help="tệp tuyên bố để hiện chữ tuyên bố ở danh sách khác nhãn (mặc định data/tuyen_bo/thu.jsonl)")
    ap.add_argument("--ra", type=Path, default=TEP_RA, help="mặc định ket_qua/bo_thu/nhat_quan_luot3.md")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    for duong in (args.tep_luot3, args.tep_luot2):
        if not duong.exists():
            sys.exit(f"không thấy tệp {duong}")
    try:
        kq = do_nhat_quan(doc_nhan(args.tep_luot3), doc_nhan(args.tep_luot2))
    except ValueError as e:
        sys.exit(str(e))
    if kq["n"] == 0:
        sys.exit(f"{args.tep_luot3.name} và {args.tep_luot2.name} không có mã chung nào")
    bao_cao = viet_bao_cao(kq, args.tep_luot3.name, args.tep_luot2.name, doc_cau(args.tuyen_bo))
    args.ra.parent.mkdir(parents=True, exist_ok=True)
    args.ra.write_text(bao_cao, encoding="utf-8", newline="\n")
    print(bao_cao)
    print(f"đã ghi {args.ra}")


if __name__ == "__main__":
    main()
