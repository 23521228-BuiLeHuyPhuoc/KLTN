"""Bước 14: đo Recall@k (k = 1, 3, 5, 8) của truy hồi BM25 trên bộ thử, cho hai cách tách (âm tiết, từ).

Truy vấn là tuyên bố trong data/tuyen_bo/thu.jsonl, tìm trong doan.jsonl của đúng mẫu của tuyên bố; chuẩn là
bang_chung trong tệp nhãn (--nhan, mặc định data/nhan/thu.jsonl là lượt 1). Theo T6.4, tuyên bố trúng ở k nếu có ít nhất một đoạn bằng chứng nằm trong
top-k; mẫu số là các tuyên bố có bằng chứng, trừ danh sách --bo. Ghi ket_qua/recall_buoc14.md (chỉ có số liệu, không
nhận xét). Chỉ đọc dữ liệu, không gọi LLM.

Chạy (lượt 1, đúng như lần đo của Bước 14):
    .venv/Scripts/python.exe scripts/do_recall.py --nhan data/nhan/thu.jsonl --bo tb-00009,tb-00010
Lượt khác: --nhan <tệp nhãn>; --bo mặc định rỗng (rà soát 02/11: không còn đọc cứng nhãn lượt 1 và danh sách loại).
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kiemchung import cau_hinh, truy_hoi as th  # noqa: E402

TEP_TUYEN_BO = ROOT / "data/tuyen_bo/thu.jsonl"
TEP_NHAN = ROOT / "data/nhan/thu.jsonl"
TEP_RA = ROOT / "ket_qua/recall_buoc14.md"
BO_LUOT_1 = "tb-00009,tb-00010"  # danh sách loại của lần đo Bước 14 (nhãn lượt 1); không còn là mặc định
LY_DO_MAC_DINH = "bằng chứng lưu lệch sang tuyên bố kế bên (nhãn lượt 1)"
TEN_CACH = {"am_tiet": "Âm tiết", "tu": "Từ (pyvi)"}
GHI_CHU = "Số tạm: bằng chứng chuẩn lấy từ nhãn lượt 1 của Bước 13; tính lại sau khi gán lại ở Bước 16."


def ghi_chu_theo_nhan(dong_nhan, tep):
    """Dòng chú thích đầu báo cáo theo tệp nhãn thật: lượt 1 giữ đúng chữ của lần đo Bước 14 (GHI_CHU)."""
    luot = sorted({str(nh.get("luot")) for nh in dong_nhan})
    if luot == ["1"]:
        return GHI_CHU
    nguoi = ", ".join(sorted({str(nh.get("nguoi_gan")) for nh in dong_nhan}))
    return f"Số tạm: bằng chứng chuẩn lấy từ {tep} (lượt {', '.join(luot)}, người gán {nguoi})."


def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(dong) for dong in f if dong.strip()]


def o_ty_le(trung, mau_so):
    """'58,9% (33/56)'; mẫu số 0 thì chỉ ghi '0/0'."""
    if not mau_so:
        return f"{trung}/{mau_so}"
    return f"{100 * trung / mau_so:.1f}%".replace(".", ",") + f" ({trung}/{mau_so})"


def o_van_ban(chu):
    """Chữ đặt trong ô bảng markdown: dấu | và xuống dòng không được làm vỡ bảng."""
    return " ".join(chu.split()).replace("|", "\\|")


def dong_bang(*o):
    return "| " + " | ".join(o) + " |"


def xep_hang_tat_ca(tuyen_bo, cach):
    """{mã tuyên bố: [mã đoạn xếp giảm dần]} với toàn bộ đoạn của mẫu (k=None), theo một cách tách."""
    return {tb["id"]: [ma for ma, _ in th.truy_hoi(tb["ma_mau"], tb["tuyen_bo"], None, cach)] for tb in tuyen_bo}


def tao_bao_cao(tuyen_bo, bang_chung, xep_hang, bo, ly_do, ten_mau, ghi_chu=GHI_CHU):
    """Danh sách dòng markdown của báo cáo.

    xep_hang: {cách tách: {mã tuyên bố: [mã đoạn xếp giảm dần]}}; bo: các mã tuyên bố loại khỏi mẫu số;
    ten_mau: {ma_mau: tên hiển thị}."""
    cac_cach = list(xep_hang)
    mau_so = th.mau_so_recall(bang_chung, bo)
    theo_id = {tb["id"]: tb for tb in tuyen_bo}
    khong_bang_chung = [ma for ma, bc in bang_chung.items() if not bc]
    bi_loai = [ma for ma in bo if bang_chung[ma]]
    dau_k = [f"k={k}" for k in th.KS]
    dong = ["# Recall@k của truy hồi BM25 trên bộ thử (Bước 14)", "", ghi_chu, "",
            f"Bộ thử có {len(tuyen_bo)} tuyên bố, {len(khong_bang_chung)} không có bằng chứng (không tính), "
            f"{len(bi_loai)} bị loại; mẫu số {len(mau_so)}. Tuyên bố trúng ở k khi có ít nhất một đoạn bằng chứng "
            "nằm trong top-k.", ""]

    dong += ["## Tuyên bố loại khỏi mẫu số", "", dong_bang("Mã", "Mẫu", "Tuyên bố", "Lý do"), dong_bang(*["---"] * 4)]
    dong += [dong_bang(ma, theo_id[ma]["ma_mau"], o_van_ban(theo_id[ma]["tuyen_bo"]), ly_do) for ma in bo]
    if not bo:
        dong += [dong_bang("(không có)", "", "", "")]

    dong += ["", "## Recall@k", "", dong_bang("Cách tách", *dau_k), dong_bang(*["---"] * (1 + len(th.KS)))]
    for cach in cac_cach:
        recall = th.tinh_recall(xep_hang[cach], bang_chung, bo)
        dong.append(dong_bang(TEN_CACH[cach], *(o_ty_le(*recall[k]) for k in th.KS)))

    dong += ["", "## Theo mẫu", "", dong_bang("Mẫu", "Cách tách", "Mẫu số", *dau_k),
             dong_bang(*["---"] * (3 + len(th.KS)))]
    for ma_mau in dict.fromkeys(tb["ma_mau"] for tb in tuyen_bo):
        cua_mau = {ma: bc for ma, bc in bang_chung.items() if theo_id[ma]["ma_mau"] == ma_mau}
        for cach in cac_cach:
            recall = th.tinh_recall(xep_hang[cach], cua_mau, bo)
            dong.append(dong_bang(ten_mau.get(ma_mau, ma_mau), TEN_CACH[cach], str(recall[th.KS[0]][1]),
                                  *(o_ty_le(*recall[k]) for k in th.KS)))

    k_max = max(th.KS)
    hang = {ma: [th.hang_bang_chung(xep_hang[cach][ma], bang_chung[ma]) for cach in cac_cach] for ma in mau_so}
    truot = [ma for ma in mau_so if any(h > k_max for h in hang[ma])]
    dong += ["", f"## Bằng chứng không nằm trong top-{k_max} ở ít nhất một cách tách", ""]
    if truot:
        dong += [dong_bang("Mã", "Mẫu", "Bằng chứng chuẩn", *(f"Hạng ({TEN_CACH[c]})" for c in cac_cach), "Tuyên bố"),
                 dong_bang(*["---"] * (4 + len(cac_cach)))]
        dong += [dong_bang(ma, theo_id[ma]["ma_mau"], ", ".join(bang_chung[ma]), *map(str, hang[ma]),
                           o_van_ban(theo_id[ma]["tuyen_bo"])) for ma in truot]
    else:
        dong.append("Không có.")
    return dong


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Đo Recall@k của BM25 trên bộ thử (Bước 14).")
    ap.add_argument("--nhan", type=Path, default=TEP_NHAN, help=f"tệp nhãn chuẩn (mặc định {TEP_NHAN.relative_to(ROOT)}, lượt 1)")
    ap.add_argument("--bo", default="", help=f"mã tuyên bố loại khỏi mẫu số, cách nhau dấu phẩy (mặc định không loại; lần đo "
                                             f"Bước 14 dùng {BO_LUOT_1})")
    ap.add_argument("--ly-do", default=LY_DO_MAC_DINH, help="lý do loại, in vào báo cáo")
    ap.add_argument("--ra", type=Path, default=TEP_RA, help=f"tệp báo cáo (mặc định {TEP_RA.relative_to(ROOT)})")
    args = ap.parse_args()

    tuyen_bo = doc_jsonl(TEP_TUYEN_BO)
    dong_nhan = doc_jsonl(args.nhan)
    bang_chung = {nh["id"]: nh["bang_chung"] for nh in dong_nhan}
    if set(bang_chung) != {tb["id"] for tb in tuyen_bo}:
        sys.exit("tệp nhãn và tệp tuyên bố không cùng tập mã tuyên bố")
    bo = [ma.strip() for ma in args.bo.split(",") if ma.strip()]
    la = [ma for ma in bo if ma not in bang_chung]
    if la:
        sys.exit(f"--bo có mã không thuộc bộ thử: {', '.join(la)}")

    xep_hang = {cach: xep_hang_tat_ca(tuyen_bo, cach) for cach in th.CACH_TACH}
    # Bằng chứng chuẩn phải là đoạn của đúng mẫu; nếu không, hạng sẽ là None và Recall bị đo sai.
    for ma in th.mau_so_recall(bang_chung):
        for cach in th.CACH_TACH:
            if th.hang_bang_chung(xep_hang[cach][ma], bang_chung[ma]) is None:
                sys.exit(f"{ma}: bằng chứng {bang_chung[ma]} không có trong doan.jsonl của mẫu")
    ten_mau = {r["ma_mau"]: f"{r['ten']} ({r['ma_mau']})" for r in cau_hinh.doc_mau()}
    try:
        ten_tep = args.nhan.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        ten_tep = str(args.nhan)
    dong = tao_bao_cao(tuyen_bo, bang_chung, xep_hang, bo, args.ly_do, ten_mau, ghi_chu_theo_nhan(dong_nhan, ten_tep))
    args.ra.parent.mkdir(parents=True, exist_ok=True)
    args.ra.write_text("\n".join(dong) + "\n", encoding="utf-8")
    print("\n".join(dong))
    print(f"\nĐã ghi {args.ra}")


if __name__ == "__main__":
    main()
