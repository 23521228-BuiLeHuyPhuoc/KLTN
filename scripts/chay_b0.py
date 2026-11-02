"""Bước 15: chạy đối chứng B0 (T12.1) trên bộ thử, tính FAR và Recall nhãn Đúng (T6.4).

Với mỗi mô hình và mỗi tuyên bố trong data/tuyen_bo/thu.jsonl: truy hồi top-k đoạn của đúng mẫu, ghép câu lệnh
T12.1, gọi LLM (nhiệt độ 0, qua bộ nhớ đệm của llm.py), ánh xạ Supported/Refuted/NEI -> DUNG/SAI/CHUA_DU. Nhãn chuẩn
là nhãn trong tệp --nhan (mặc định data/nhan/thu.jsonl, lượt 1). Ghi:
    ket_qua/b0_thu/<tên mô hình>.jsonl   mỗi tuyên bố một dòng, đủ cả tuyên bố bị loại khỏi chỉ số
    ket_qua/b0_buoc15.md                 báo cáo số liệu, không nhận xét
Chạy với --gia thì dùng LLM giả (không gọi mạng, không cần khóa) và ghi vào b0_thu_gia/ và b0_buoc15_gia.md, báo cáo
ghi rõ là chạy giả, để không lẫn với kết quả thật.

Chạy lại được: lời gọi trùng đi qua bộ nhớ đệm, không tốn thêm. Lỗi mạng, quota, khóa hoặc mô hình thì dừng và báo,
tệp kết quả của mô hình đang chạy dở và báo cáo không được ghi (mô hình đã chạy xong trước đó thì giữ); chạy lại
cùng lệnh để tiếp tục. Khóa API đọc từ biến môi trường GEMINI_API_KEY, GROQ_API_KEY (nạp thêm từ .env khi chạy thật).

Chạy:
    .venv/Scripts/python.exe -X utf8 scripts/chay_b0.py [--mo-hinh MA ...] [--k 5] [--cach-tach am_tiet]
        [--nhan data/nhan/thu.jsonl] [--bo tb-00009,tb-00010] [--gia]
Lần chạy Bước 15 dùng nhãn lượt 1 và --bo tb-00009,tb-00010; --bo mặc định rỗng (rà soát 02/11).
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kiemchung import danh_gia as dg, truy_hoi as th  # noqa: E402
from kiemchung.doi_chung import b0  # noqa: E402
from kiemchung.llm import LLMClient, LLMError  # noqa: E402

try:
    from dotenv import load_dotenv
except ImportError:  # chưa cài python-dotenv: --gia và test vẫn chạy; chạy thật dùng biến môi trường có sẵn
    load_dotenv = None

TEP_TUYEN_BO = ROOT / "data/tuyen_bo/thu.jsonl"
TEP_NHAN = ROOT / "data/nhan/thu.jsonl"
THU_MUC_RA = ROOT / "ket_qua"
BO_LUOT_1 = "tb-00009,tb-00010"  # danh sách loại của lần chạy Bước 15 (nhãn lượt 1); không còn là mặc định
LY_DO_MAC_DINH = "nhãn lượt 1 lưu lệch sang tuyên bố kế bên"
NGHI_MAC_DINH = 20  # giây giữa hai lần gọi thật, như interval_s của data/thu_llm/models.json (hạn mức tầng miễn phí)
TIMEOUT_MAC_DINH = 90  # giây; mô hình suy luận trả chậm hơn 30 giây của thu_llm (CopyPro cũng chờ 90 giây)
SO_LAN_THU_LAI = 2
GHI_CHU = "Số sơ bộ: nhãn chuẩn là nhãn lượt 1 của Bước 13; mô hình, k và cách tách là lựa chọn tạm, chốt ở Bước 33."


def ghi_chu_theo_nhan(dong_nhan, tep):
    """Dòng chú thích đầu báo cáo theo tệp nhãn thật: lượt 1 giữ đúng chữ của lần chạy Bước 15 (GHI_CHU)."""
    luot = sorted({str(nh.get("luot")) for nh in dong_nhan})
    if luot == ["1"]:
        return GHI_CHU
    nguoi = ", ".join(sorted({str(nh.get("nguoi_gan")) for nh in dong_nhan}))
    return (f"Số sơ bộ: nhãn chuẩn lấy từ {tep} (lượt {', '.join(luot)}, người gán {nguoi}); mô hình, k và cách tách là "
            "lựa chọn tạm, chốt ở Bước 33.")
CANH_BAO_GIA = ("**CHẠY GIẢ (--gia): LLM giả, không gọi mô hình thật. Số liệu dưới đây chỉ để thử script, không phải "
                "kết quả của B0.**")


def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(dong) for dong in f if dong.strip()]


def ten_tep(mo_hinh):
    """Tên mô hình dùng làm tên tệp: ký tự ngoài chữ, số, '.', '_', '-' (như '/') đổi thành '_'."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", mo_hinh)


def ghi_tep(duong, noi_dung):
    """Ghi qua tệp tạm rồi đổi tên, để lần chạy hỏng giữa chừng không để lại tệp nửa vời."""
    duong.parent.mkdir(parents=True, exist_ok=True)
    tam = duong.with_name(duong.name + ".tmp")
    tam.write_text(noi_dung, encoding="utf-8", newline="\n")
    os.replace(tam, duong)


def o_ty_le(trung, mau_so):
    """'58,9% (33/56)'; mẫu số 0 thì chỉ ghi '0/0'."""
    if not mau_so:
        return f"{trung}/{mau_so}"
    return f"{100 * trung / mau_so:.1f}%".replace(".", ",") + f" ({trung}/{mau_so})"


def o_van_ban(chu):
    """Chữ đặt trong ô bảng markdown: dấu | và xuống dòng không được làm vỡ bảng."""
    return " ".join(str(chu).split()).replace("|", "\\|")


def dong_bang(*o):
    return "| " + " | ".join(o) + " |"


def dem_nhan(nhan):
    """'DUNG 24, SAI 4, LECH 15, CHUA_DU 23' theo thứ tự NHAN_CHUAN."""
    nhan = list(nhan)
    return ", ".join(f"{n} {sum(1 for x in nhan if x == n)}" for n in dg.NHAN_CHUAN)


def tao_bao_cao(tuyen_bo, chuan, ban_ghi, thiet_lap, bo, ly_do, gia, ghi_chu=GHI_CHU):
    """Danh sách dòng markdown của báo cáo (chỉ số liệu, không nhận xét).

    ban_ghi: {mã mô hình: [bản ghi của b0.kiem_chung_b0, mỗi tuyên bố một bản]}; thiet_lap: {"k", "cach_tach",
    "max_token_ra"}; bo: mã tuyên bố loại khỏi chỉ số, ly_do: lý do loại; gia: chạy bằng LLM giả."""
    theo_id = {tb["id"]: tb for tb in tuyen_bo}
    da_loai = set(bo)
    trong_mau = [ma for ma in chuan if ma not in da_loai]
    ma_trong_mau = set(trong_mau)
    dong = [CANH_BAO_GIA, ""] if gia else []
    dong += [ghi_chu, "", "# Đối chứng B0 trên bộ thử (Bước 15)", "", "## Thiết lập", ""]
    dong += [
        f"- Bộ thử: {len(chuan)} tuyên bố ({dem_nhan(chuan.values())}); mẫu tính chỉ số: {len(trong_mau)} tuyên bố "
        f"({dem_nhan(chuan[ma] for ma in trong_mau)}).",
        f"- Truy hồi: BM25, top-{thiet_lap['k']}, cách tách {thiet_lap['cach_tach']}; chỉ đoạn của đúng mẫu.",
        f"- Câu lệnh: khung T12.1, SHA-256 của khung {hashlib.sha256(b0.CAU_LENH_B0.encode('utf-8')).hexdigest()}.",
        f"- Gọi LLM: nhiệt độ {b0.NHIET_DO}, max_output_tokens {thiet_lap['max_token_ra']}, JSON mode, qua bộ nhớ đệm.",
        "- Ánh xạ nhãn: Supported -> DUNG, Refuted -> SAI, NEI -> CHUA_DU; không đọc được nhãn -> LOI.",
        "- FAR = (nhãn chuẩn khác DUNG mà bị gán DUNG) / (nhãn chuẩn khác DUNG). Recall nhãn Đúng = (DUNG được gán "
        "DUNG) / (DUNG). LOI tính vào mẫu số, không là DUNG.",
    ]

    dong += ["", "## Tuyên bố loại khỏi chỉ số (vẫn chạy B0, có trong tệp kết quả)", "",
             dong_bang("Mã", "Mẫu", "Tuyên bố", "Nhãn chuẩn", "Lý do"), dong_bang(*["---"] * 5)]
    dong += [dong_bang(ma, theo_id[ma]["ma_mau"], o_van_ban(theo_id[ma]["tuyen_bo"]), chuan[ma], o_van_ban(ly_do))
             for ma in bo]
    if not bo:
        dong.append(dong_bang("(không có)", "", "", "", ""))

    du_doan = {mh: {r["id"]: r["nhan"] for r in rows} for mh, rows in ban_ghi.items()}
    dong += ["", "## Tóm tắt", "", dong_bang("Mô hình", "Mô hình thực", "FAR", "Recall nhãn Đúng",
                                              "Số LOI (mẫu tính / cả bộ)", "Mẫu số FAR", "Mẫu số Recall"),
             dong_bang(*["---"] * 7)]
    for mh, rows in ban_ghi.items():
        thuc = ", ".join(sorted({r["mo_hinh_thuc"] for r in rows if r["mo_hinh_thuc"]})) or "(chưa có)"
        far, recall = dg.tinh_far(chuan, du_doan[mh], bo), dg.tinh_recall_dung(chuan, du_doan[mh], bo)
        so_loi, loi_ca_bo = dg.dem_loi(chuan, du_doan[mh], bo), dg.dem_loi(chuan, du_doan[mh])
        dong.append(dong_bang(mh, thuc, o_ty_le(*far), o_ty_le(*recall), f"{so_loi} / {loi_ca_bo}",
                              str(far[1]), str(recall[1])))

    for mh, rows in ban_ghi.items():
        bang = dg.bang_nham_lan(chuan, du_doan[mh], bo)
        dong += ["", f"## {mh}", "", "Bảng nhầm lẫn (hàng: nhãn chuẩn; cột: nhãn dự đoán):", "",
                 dong_bang("Nhãn chuẩn", *dg.NHAN_DU_DOAN, "Tổng"), dong_bang(*["---"] * (2 + len(dg.NHAN_DU_DOAN)))]
        dong += [dong_bang(h, *(str(bang[h][c]) for c in dg.NHAN_DU_DOAN), str(sum(bang[h].values())))
                 for h in dg.NHAN_CHUAN]
        loi = {}
        for r in rows:
            if r["nhan"] == "LOI" and r["id"] in ma_trong_mau:
                ma_loi = (r["loi"] or "").split(":")[0]
                loi[ma_loi] = loi.get(ma_loi, 0) + 1
        if loi:
            dong += ["", "LOI theo nguyên nhân (mẫu tính chỉ số):", "", dong_bang("Nguyên nhân", "Số tuyên bố"),
                     dong_bang("---", "---")]
            dong += [dong_bang(ma_loi, str(n)) for ma_loi, n in sorted(loi.items())]
    return dong


def main(argv=None):
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Chạy đối chứng B0 trên bộ thử (Bước 15).")
    ap.add_argument("--mo-hinh", nargs="+", default=list(b0.MO_HINH_MAC_DINH), metavar="MA",
                    help=f"mã mô hình (mặc định {' '.join(b0.MO_HINH_MAC_DINH)}; có {', '.join(b0.NHA_CUNG_CAP)})")
    ap.add_argument("--k", type=int, default=5, help="số đoạn đưa vào câu lệnh (mặc định 5)")
    ap.add_argument("--cach-tach", choices=th.CACH_TACH, default="am_tiet", help="cách tách của BM25 (mặc định am_tiet)")
    ap.add_argument("--nhan", type=Path, default=TEP_NHAN, help=f"tệp nhãn chuẩn (mặc định {TEP_NHAN.relative_to(ROOT)}, lượt 1)")
    ap.add_argument("--bo", default="", help=f"mã tuyên bố loại khỏi chỉ số, cách nhau dấu phẩy (mặc định không loại; lần "
                                             f"chạy Bước 15 dùng {BO_LUOT_1})")
    ap.add_argument("--ly-do", default=LY_DO_MAC_DINH, help="lý do loại, in vào báo cáo")
    ap.add_argument("--gia", action="store_true", help="dùng LLM giả để chạy thử, ghi vào b0_thu_gia/, b0_buoc15_gia.md")
    ap.add_argument("--thu-muc-ra", type=Path, default=THU_MUC_RA,
                    help=f"thư mục gốc của kết quả (mặc định {THU_MUC_RA.relative_to(ROOT)})")
    ap.add_argument("--max-token-ra", type=int, default=b0.MAX_TOKEN_RA,
                    help=f"max_output_tokens mỗi lần gọi (mặc định {b0.MAX_TOKEN_RA})")
    ap.add_argument("--nghi-giay", type=float, default=NGHI_MAC_DINH,
                    help=f"giây nghỉ sau mỗi lần gọi thật (mặc định {NGHI_MAC_DINH}; không áp dụng khi lấy từ bộ nhớ đệm "
                         "hoặc --gia)")
    ap.add_argument("--timeout", type=float, default=TIMEOUT_MAC_DINH, help=f"giây chờ mỗi lần gọi (mặc định {TIMEOUT_MAC_DINH})")
    args = ap.parse_args(argv)

    mo_hinh = list(dict.fromkeys(args.mo_hinh))
    la = [m for m in mo_hinh if m not in b0.NHA_CUNG_CAP]
    if la:
        ap.error(f"mô hình chưa có nhà cung cấp trong b0.NHA_CUNG_CAP: {', '.join(la)}")
    if len({ten_tep(m) for m in mo_hinh}) != len(mo_hinh):
        ap.error("hai mô hình trùng tên tệp kết quả")
    if args.k < 1:
        ap.error("--k phải từ 1 trở lên")

    tuyen_bo = doc_jsonl(TEP_TUYEN_BO)
    dong_nhan = doc_jsonl(args.nhan)
    chuan = {nh["id"]: nh["nhan"] for nh in dong_nhan}
    try:
        ten_tep_nhan = args.nhan.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        ten_tep_nhan = str(args.nhan)
    if set(chuan) != {tb["id"] for tb in tuyen_bo}:
        sys.exit("tệp nhãn và tệp tuyên bố không cùng tập mã tuyên bố")
    bo = [ma.strip() for ma in args.bo.split(",") if ma.strip()]
    la = [ma for ma in bo if ma not in chuan]
    if la:
        sys.exit(f"--bo có mã không thuộc bộ thử: {', '.join(la)}")

    hau_to = "_gia" if args.gia else ""
    thu_muc_kq = args.thu_muc_ra / f"b0_thu{hau_to}"
    tep_bao_cao = args.thu_muc_ra / f"b0_buoc15{hau_to}.md"
    if args.gia:
        # Bộ nhớ đệm và nhật ký riêng của LLM giả, không đụng ket_qua/llm_cache của các lần gọi thật.
        client = LLMClient(thu_muc_kq / "llm_cache", thu_muc_kq / "llm_calls.jsonl", max_retries=SO_LAN_THU_LAI,
                           transport=b0.gia_transport)
    else:
        if load_dotenv is None:
            print("Cảnh báo: chưa cài python-dotenv, không nạp .env; chỉ dùng biến môi trường có sẵn.", file=sys.stderr)
        else:
            load_dotenv(ROOT / ".env", override=False, interpolate=False)
        client = LLMClient(args.thu_muc_ra / "llm_cache", args.thu_muc_ra / "llm_calls.jsonl",
                           timeout_s=args.timeout, max_retries=SO_LAN_THU_LAI)

    ket_qua, da_ghi, vua_goi_that = {}, [], False
    for mh in mo_hinh:
        ban_ghi = []
        for i, tb in enumerate(tuyen_bo, start=1):
            if vua_goi_that and args.nghi_giay > 0:
                time.sleep(args.nghi_giay)
            try:
                bg = b0.kiem_chung_b0(tb, client, mh, args.k, args.cach_tach, max_token_ra=args.max_token_ra)
            except LLMError as e:
                print(f"\nDỪNG ở {mh}, tuyên bố {tb['id']} ({i}/{len(tuyen_bo)}): {e.code}.\n"
                      f"Không ghi kết quả của {mh} và không ghi báo cáo. "
                      f"Đã ghi đủ: {', '.join(map(str, da_ghi)) or '(chưa có)'}.\n"
                      "Các tuyên bố đã gọi xong nằm trong bộ nhớ đệm; chạy lại cùng lệnh để làm tiếp.", file=sys.stderr)
                return 1
            vua_goi_that = not args.gia and not bg["tu_bo_nho_dem"]
            ban_ghi.append(bg)
            print(f"{mh} {i}/{len(tuyen_bo)} {tb['id']}: {bg['nhan']}"
                  f"{'' if bg['tu_bo_nho_dem'] else ' (gọi mới)'}{' LOI: ' + bg['loi'] if bg['loi'] else ''}",
                  file=sys.stderr, flush=True)
        duong = thu_muc_kq / f"{ten_tep(mh)}.jsonl"
        ghi_tep(duong, "".join(json.dumps(bg, ensure_ascii=False) + "\n" for bg in ban_ghi))
        da_ghi.append(duong)
        ket_qua[mh] = ban_ghi

    thiet_lap = {"k": args.k, "cach_tach": args.cach_tach, "max_token_ra": args.max_token_ra}
    dong = tao_bao_cao(tuyen_bo, chuan, ket_qua, thiet_lap, bo, args.ly_do, args.gia,
                       ghi_chu_theo_nhan(dong_nhan, ten_tep_nhan))
    ghi_tep(tep_bao_cao, "\n".join(dong) + "\n")
    print("\n".join(dong))
    print(f"\nĐã ghi {tep_bao_cao} và {len(da_ghi)} tệp trong {thu_muc_kq}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
