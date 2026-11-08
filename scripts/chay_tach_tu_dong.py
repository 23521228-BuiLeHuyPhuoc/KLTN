"""Tách các bài của mẫu được chọn và so với tách tay; không đọc nhãn kiểm chứng."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chay_doi_chung import (doc_jsonl, ghi_tep, ten_tep, tham_so_chung, kiem_tham_so,
                           tao_client, loc_mau, jsonl_on_dinh)
from kiemchung import tach_tuyen_bo as tach
from kiemchung.llm import LLMError

THU_MUC_QUANG_CAO = ROOT / "data/quang_cao"


def doc_bai(thu_muc, cac_mau):
    """Chọn tên tệp theo mã mẫu trước khi mở, gồm cả bài không có tuyên bố tách tay."""
    ket_qua = []
    for tep in sorted(Path(thu_muc).glob("*.json")):
        if not any(tep.stem.startswith(f"qc-{ma}-") for ma in cac_mau):
            continue
        bai = json.loads(tep.read_text(encoding="utf-8-sig"))
        if bai["ma_mau"] in cac_mau:
            bai.setdefault("ma_qc", tep.stem)
            ket_qua.append(bai)
    return ket_qua


def bao_cao(tu_dong, tach_tay, cac_bai, gia):
    """Báo phép tách theo bài sinh, không dùng nhãn đúng/sai."""
    dong = ["# Tách tự động" + (" (LLM giả, không là kết quả thực nghiệm)" if gia else ""), "",
            "| Phân nhóm | Giá trị | Tự động | Tách tay | Ghép | Precision | Recall |",
            "| --- | --- | --- | --- | --- | --- | --- |"]

    def them(ten, gia_tri, td, tay):
        s = tach.thong_ke(td, tay)
        p = "không xác định" if s["precision"] is None else f"{s['precision']:.6f}"
        r = "không xác định" if s["recall"] is None else f"{s['recall']:.6f}"
        chu = str(gia_tri).replace("|", "\\|").replace("\n", " ")
        dong.append(f"| {ten} | {chu} | {s['so_tu_dong']} | {s['so_tach_tay']} | {s['so_cap']} | {p} | {r} |")
    them("chung", "tất cả", tu_dong, tach_tay)
    for khoa in ("che_do", "llm_sinh", "nhom"):
        cac_gia_tri = {d.get(khoa) for d in tu_dong + tach_tay}
        if khoa == "che_do":
            cac_gia_tri.update(("ten", "ten_thong_so"))
        for v in sorted(cac_gia_tri, key=str):
            them(khoa, v, [d for d in tu_dong if d.get(khoa) == v], [d for d in tach_tay if d.get(khoa) == v])
    dem = Counter()
    for b in cac_bai:
        dem.update(b["bi_loc"])
    dong += ["", f"Số bài LOI: {sum(b['loi'] is not None for b in cac_bai)}", "", "Số bị lọc theo lý do:"]
    dong += [f"- {ly_do}: {n}" for ly_do, n in sorted(dem.items())] or ["- Không có: 0"]
    s = tach.thong_ke(tu_dong, tach_tay)
    dong += ["", f"Cặp có kết quả hiểu điều kiện Bước 22 ở cả hai phía: {s['so_cap_co_dieu_kien']}",
             f"Cặp cùng điều kiện: {s['so_cap_cung_dieu_kien']}",
             "Tỉ lệ cùng điều kiện: " + (str(s["ty_le_cung_dieu_kien"]) if s["ty_le_cung_dieu_kien"] is not None
                                        else "chưa tính được; cần kết quả Bước 22 cho cả hai phía.")]
    return "\n".join(dong) + "\n"


def main(argv=None):
    """Tách mọi bài của các mẫu trong tệp tách tay và ghi kết quả tất định."""
    ap = argparse.ArgumentParser(description=__doc__)
    tham_so_chung(ap, ROOT / "ket_qua/tach_tu_dong")
    args = ap.parse_args(argv)
    kiem_tham_so(ap, args)
    tay = loc_mau(doc_jsonl(args.tuyen_bo), args.ma_mau)
    bai = doc_bai(THU_MUC_QUANG_CAO, {d["ma_mau"] for d in tay})
    theo_ma = {b["ma_qc"]: b for b in bai}
    thieu = {d["ma_qc"] for d in tay} - theo_ma.keys()
    if thieu:
        ap.error(f"thiếu bài quảng cáo: {sorted(thieu)}")
    for d in tay:
        b = theo_ma[d["ma_qc"]]
        d["nhom"] = tach.nhom_cua_mau(d["ma_mau"])
        d["che_do"] = b.get("che_do")
        d["llm_sinh"] = b.get("llm_sinh") or b.get("mo_hinh_nha_cung_cap") or b.get("mo_hinh")
    client = tao_client(args, tach.gia_transport)
    ket_qua, tu_dong, vua_goi = [], [], False
    for b in bai:
        if vua_goi and args.nghi_giay:
            time.sleep(args.nghi_giay)
        try:
            r = tach.tach_bai(client, args.mo_hinh, b, args.max_token_ra)
        except LLMError as e:
            print(f"Dừng: {e.code}; chưa ghi kết quả, có thể chạy lại từ bộ nhớ đệm.", file=sys.stderr)
            return 1
        ket_qua.append(r)
        tu_dong.extend(r["tuyen_bo"])
        vua_goi = not args.gia and not r["tu_bo_nho_dem"]
    ten = f"tach_{args.tuyen_bo.stem}_{ten_tep(args.mo_hinh)}" + ("_gia" if args.gia else "")
    ghi_tep(args.thu_muc_ra / f"{ten}.jsonl", jsonl_on_dinh(tu_dong))
    ghi_tep(args.thu_muc_ra / f"{ten}_bai.jsonl", jsonl_on_dinh(ket_qua))
    ghi_tep(args.thu_muc_ra / f"{ten}.md", bao_cao(tu_dong, tay, ket_qua, args.gia))
    return 0


if __name__ == "__main__":
    sys.exit(main())
