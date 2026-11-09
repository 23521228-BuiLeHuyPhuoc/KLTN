"""Bước 28 việc 1, Bước 31: chạy P (bộ quyết định A-D) trên tệp kết quả trích xuất của scripts/chay_trich_xuat.py.

Không gọi LLM, không đọc nhãn chuẩn. Bản của P theo tệp trích xuất và cờ: tệp chạy với --khong-neo-nguon --khong-kiem-day-du là P-NN
(đọc cờ neo_nguon, kiem_day_du trong từng bản ghi); --bo-doi-chieu là P-DK (cùng tệp P-NN thì báo lỗi, T5.9). Ghi, trong --thu-muc-ra:
    <he>_<tên tệp trích xuất>.jsonl        mỗi tuyên bố một kết quả (src/kiemchung/p.py, khóa sắp xếp, giống từng byte khi chạy lại)
    thong_ke_<he>_<tên tệp trích xuất>.md  tóm tắt, chỉ số liệu
Chạy:
    .venv/Scripts/python.exe -X utf8 scripts/chay_p.py --trich-xuat ket_qua/trich_xuat/<tệp>.jsonl [--bo-doi-chieu] [--thu-muc-ra ket_qua/p]
"""
import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kiemchung import p as pp  # noqa: E402

THU_MUC_RA = ROOT / "ket_qua/p"


def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(dong) for dong in f if dong.strip()]


def ghi_tep(duong, noi_dung):
    """Ghi qua tệp tạm rồi đổi tên, để lần chạy hỏng giữa chừng không để lại tệp nửa vời."""
    duong.parent.mkdir(parents=True, exist_ok=True)
    tam = duong.with_name(duong.name + ".tmp")
    tam.write_text(noi_dung, encoding="utf-8", newline="\n")
    os.replace(tam, duong)


def dem(chuoi):
    """{giá trị: số lần}, sắp theo giá trị."""
    ket = {}
    for x in chuoi:
        ket[x] = ket.get(x, 0) + 1
    return dict(sorted(ket.items(), key=lambda kv: str(kv[0])))


def nguyen_nhan_d1a(kq):
    """Nguyên nhân của một ca D1a theo ghi_chu: chua_xac_dinh=<cụm>, hoặc mac_dinh=<...>, không thì 'khac'."""
    for tien_to in ("chua_xac_dinh=", "mac_dinh="):
        for g in kq["ghi_chu"]:
            if g.startswith(tien_to):
                return g
    return "khac"


def tao_thong_ke(ket_qua, he, tep_trich_xuat):
    """Danh sách dòng markdown tóm tắt kết quả P; chỉ số liệu, không so với nhãn chuẩn."""
    def bang(tieu_de, d):
        return ["", f"## {tieu_de}", ""] + ([f"- {k}: {n}" for k, n in d.items()] or ["- (không có)"])

    d1a = [k for k in ket_qua if k["dong_d"] == "D1a"]
    lan = sum(1 for k in ket_qua if k["vet"].get("lan"))
    that_bai = sum(1 for k in ket_qua if "chua_xac_dinh=trich_xuat_that_bai" in k["ghi_chu"])
    dong = [f"# Kết quả {he} (Bước 28, 31)", "", f"- Tệp trích xuất: {tep_trich_xuat}.", f"- Số tuyên bố: {len(ket_qua)}."]
    dong += bang("Phân bố nhãn", dem(k["nhan"] for k in ket_qua))
    dong += bang("Phân bố dòng D", dem(k["dong_d"] for k in ket_qua))
    dong += bang("Phân bố loại", dem(k["loai"] or "(không)" for k in ket_qua))
    dong += bang(f"D1a theo nguyên nhân (tổng {len(d1a)})", dem(nguyen_nhan_d1a(k) for k in d1a))
    dong += ["", "## Khác", "", f"- Số ca dùng luật lan (vet.lan khác rỗng): {lan}.",
             f"- Số ca trích xuất thất bại: {that_bai}."]
    return dong


def main(argv=None):
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Chạy P (bộ quyết định A-D) trên tệp trích xuất.")
    ap.add_argument("--trich-xuat", type=Path, required=True, help="tệp jsonl kết quả của scripts/chay_trich_xuat.py")
    ap.add_argument("--bo-doi-chieu", action="store_true", help="P-DK: bỏ đối chiếu điều kiện (không dùng với tệp P-NN)")
    ap.add_argument("--thu-muc-ra", type=Path, default=THU_MUC_RA, help=f"thư mục kết quả (mặc định {THU_MUC_RA.relative_to(ROOT)})")
    args = ap.parse_args(argv)

    ban_ghi = doc_jsonl(args.trich_xuat)
    if not ban_ghi:
        ap.error("tệp trích xuất rỗng")
    thiet_lap = {(b["neo_nguon"], b["kiem_day_du"]) for b in ban_ghi}
    if len(thiet_lap) != 1:
        ap.error("tệp trích xuất lẫn bản ghi có cờ neo_nguon, kiem_day_du khác nhau")
    neo_nguon, kiem_day_du = next(iter(thiet_lap))
    try:
        he = pp.ten_he(neo_nguon, kiem_day_du, args.bo_doi_chieu)
    except ValueError as e:
        ap.error(str(e))

    ket_qua = [pp.kiem_chung_ban_ghi(b, args.bo_doi_chieu) for b in ban_ghi]
    ten = f"{he}_{args.trich_xuat.stem}"
    ghi_tep(args.thu_muc_ra / f"{ten}.jsonl",
            "".join(json.dumps(kq, ensure_ascii=False, sort_keys=True) + "\n" for kq in ket_qua))
    try:
        tep_ten = args.trich_xuat.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        tep_ten = str(args.trich_xuat)
    dong = tao_thong_ke(ket_qua, he, tep_ten)
    ghi_tep(args.thu_muc_ra / f"thong_ke_{ten}.md", "\n".join(dong) + "\n")
    print("\n".join(dong))
    print(f"\nĐã ghi {args.thu_muc_ra / (ten + '.jsonl')} và {args.thu_muc_ra / ('thong_ke_' + ten + '.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
