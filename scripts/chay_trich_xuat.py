"""Bước 22: chạy trích xuất có neo nguồn và kiểm tra đầy đủ (P, T5.1, T5.3, T12.4) trên một tệp tuyên bố.

Mỗi tuyên bố một lần gọi LLM (nhiệt độ 0, JSON mode, qua bộ nhớ đệm của llm.py), rồi neo nguồn, hiểu điều kiện và kiểm tra đầy
đủ bằng Python (src/kiemchung/trich_xuat.py, đặc tả luan_van/buoc22_thiet_ke_trich_xuat.md). Ghi, trong --thu-muc-ra:
    <tên>.jsonl           mỗi tuyên bố một bản ghi (mục 8 của đặc tả)
    thong_ke_<tên>.md     thống kê mục 10, chỉ số liệu
Tên tự sinh từ tệp tuyên bố, mô hình, k, cách tách và cờ (P−NN: --khong-neo-nguon --khong-kiem-day-du). Chạy với --gia thì dùng
LLM giả (không gọi mạng, không cần khóa) và ghi sang thư mục có hậu tố _gia, tên tệp có hậu tố _gia, báo cáo ghi rõ chạy giả.

Chạy lại được: lời gọi trùng đi qua bộ nhớ đệm, kết quả giống từng byte (tệp không có thời gian hay cờ bộ nhớ đệm). Lỗi mạng, quota,
khóa hoặc mô hình thì dừng và báo, không ghi tệp của lần chạy dở; chạy lại cùng lệnh để tiếp tục. Khóa API đọc từ biến môi trường
GEMINI_API_KEY, GROQ_API_KEY (nạp thêm từ .env khi chạy thật).

Chạy:
    .venv/Scripts/python.exe -X utf8 scripts/chay_trich_xuat.py [--tuyen-bo data/tuyen_bo/thu.jsonl] [--ma-mau MA ...]
        [--mo-hinh gemini-3.6-flash] [--k 5] [--cach-tach am_tiet] [--khong-neo-nguon --khong-kiem-day-du] [--gia]
"""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kiemchung import truy_hoi as th, trich_xuat as tx  # noqa: E402
from kiemchung.doi_chung.b0 import NHA_CUNG_CAP, NHIET_DO  # noqa: E402
from kiemchung.llm import LLMClient, LLMError  # noqa: E402

try:
    from dotenv import load_dotenv
except ImportError:  # chưa cài python-dotenv: --gia và test vẫn chạy; chạy thật dùng biến môi trường có sẵn
    load_dotenv = None

TEP_TUYEN_BO = ROOT / "data/tuyen_bo/thu.jsonl"
THU_MUC_RA = ROOT / "ket_qua/trich_xuat"
MO_HINH_MAC_DINH = "gemini-3.6-flash"
NGHI_MAC_DINH = 20      # giây giữa hai lần gọi thật (hạn mức tầng miễn phí), như chay_b0.py
TIMEOUT_MAC_DINH = 90
SO_LAN_THU_LAI = 2
CANH_BAO_GIA = ("**CHẠY GIẢ (--gia): LLM giả, không gọi mô hình thật. Số liệu dưới đây chỉ để thử script, không phải kết quả "
                "của P.**")


def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(dong) for dong in f if dong.strip()]


def ten_tep(mo_hinh):
    """Ký tự ngoài chữ, số, '.', '_', '-' (như '/') đổi thành '_'."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", mo_hinh)


def ten_ket_qua(tep_tuyen_bo, mo_hinh, k, cach_tach, neo_nguon, kiem_day_du, gia):
    """Tên (không đuôi) của tệp kết quả: <tệp tuyên bố>_<mô hình>_k<k>_<cách tách>[_khong_neo_nguon][_khong_day_du][_gia]."""
    ten = f"{Path(tep_tuyen_bo).stem}_{ten_tep(mo_hinh)}_k{k}_{cach_tach}"
    if not neo_nguon:
        ten += "_khong_neo_nguon"
    if not kiem_day_du:
        ten += "_khong_day_du"
    return ten + ("_gia" if gia else "")


def ghi_tep(duong, noi_dung):
    """Ghi qua tệp tạm rồi đổi tên, để lần chạy hỏng giữa chừng không để lại tệp nửa vời."""
    duong.parent.mkdir(parents=True, exist_ok=True)
    tam = duong.with_name(duong.name + ".tmp")
    tam.write_text(noi_dung, encoding="utf-8", newline="\n")
    os.replace(tam, duong)


def o_ty_le(trung, mau_so):
    if not mau_so:
        return f"{trung}/{mau_so}"
    return f"{100 * trung / mau_so:.1f}%".replace(".", ",") + f" ({trung}/{mau_so})"


def o_van_ban(chu):
    """Chữ đặt trong ô bảng markdown: dấu | và xuống dòng không được làm vỡ bảng."""
    return " ".join(str(chu).split()).replace("|", "\\|")


def dong_bang(*o):
    return "| " + " | ".join(o) + " |"


def dem(chuoi):
    """{giá trị: số lần}, sắp theo giá trị."""
    ket = {}
    for x in chuoi:
        ket[x] = ket.get(x, 0) + 1
    return dict(sorted(ket.items(), key=lambda kv: str(kv[0])))


def tao_thong_ke(ban_ghi, thiet_lap, tuyen_bo_goc, gia):
    """Danh sách dòng markdown của thống kê (mục 10), chỉ số liệu.

    ban_ghi: các bản ghi của trich_xuat.trich_xuat; thiet_lap: {"tep", "mo_hinh", "k", "cach_tach", "neo_nguon", "kiem_day_du",
    "max_token_ra"}; tuyen_bo_goc: {id: dòng của tệp tuyên bố}, chỉ để đếm tỉ lệ thuộc tính khớp tách tay (tham khảo)."""
    dong = [CANH_BAO_GIA, ""] if gia else []
    dong += ["# Thống kê trích xuất có neo nguồn (Bước 22)", "", "## Thiết lập", "",
             f"- Tệp tuyên bố: {thiet_lap['tep']}; mô hình {thiet_lap['mo_hinh']}; top-{thiet_lap['k']}, cách tách "
             f"{thiet_lap['cach_tach']}; max_output_tokens {thiet_lap['max_token_ra']}, nhiệt độ {NHIET_DO}, JSON mode, qua bộ nhớ đệm.",
             f"- neo_nguon = {thiet_lap['neo_nguon']}, kiem_day_du = {thiet_lap['kiem_day_du']}"
             f"{' (P−NN)' if not thiet_lap['neo_nguon'] and not thiet_lap['kiem_day_du'] else ''}.", "",
             "## Số lượng", ""]
    co_loi = [b for b in ban_ghi if b["loi"]]
    giu = sum(len(b["bang_chung"]) for b in ban_ghi)
    loai = sum(len(b["bang_chung_bi_loai"]) for b in ban_ghi)
    dong += [f"- Số tuyên bố: {len(ban_ghi)}; số lỗi LLM hay lỗi đọc đầu ra: {len(co_loi)}"
             f"{' (' + ', '.join(f'{b['id']}: {o_van_ban(b['loi'])}' for b in co_loi) + ')' if co_loi else ''}.",
             f"- Số mục tài liệu: {giu + loai} (giữ {giu}, bị loại {loai}).", ""]

    bi_loai = [(b["phia"], b["ly_do"]) for r in ban_ghi for b in r["bi_loai"]]
    dong += ["## Trường bị loại (theo lý do và theo phía)", "", dong_bang("Lý do", "Tuyên bố", "Tài liệu", "Tổng"),
             dong_bang("---", "---", "---", "---")]
    ly_do = dem(ld for _, ld in bi_loai)
    dong += [dong_bang(ld, str(bi_loai.count(("tuyen_bo", ld))), str(bi_loai.count(("tai_lieu", ld))), str(n))
             for ld, n in ly_do.items()] or [dong_bang("(không có)", "0", "0", "0")]

    bo_sung = [b for r in ban_ghi for b in r["bo_sung"]]
    mo_ho = [b for r in ban_ghi for b in r["bo_sung_mo_ho"]]
    dong += ["", "## Điều kiện bổ sung (kiểm tra đầy đủ)", "", dong_bang("Điều kiện", "Tuyên bố", "Tài liệu", "Tổng"),
             dong_bang("---", "---", "---", "---")]
    ten_dk = dem(b["dieu_kien"] for b in bo_sung)
    dong += [dong_bang(ten, str(sum(1 for b in bo_sung if b["dieu_kien"] == ten and b["phia"] == "tuyen_bo")),
                       str(sum(1 for b in bo_sung if b["dieu_kien"] == ten and b["phia"] == "tai_lieu")), str(n))
             for ten, n in ten_dk.items()] or [dong_bang("(không có)", "0", "0", "0")]
    dong += ["", f"- Điều kiện thấy hai giá trị khác nhau, không điền (bo_sung_mo_ho): {len(mo_ho)}."]

    dong += ["", "## Điều kiện lạ (dieu_kien_khac)", ""]
    tb_khac = [(b["id"], b["tuyen_bo"]["dieu_kien_khac"]) for b in ban_ghi if b["tuyen_bo"] and b["tuyen_bo"]["dieu_kien_khac"]]
    tl_khac = [(b["id"], m["ma_doan"], m["dieu_kien_khac"]) for b in ban_ghi for m in b["bang_chung"] if m["dieu_kien_khac"]]
    tong_tl = sum(len(b["bang_chung"]) for b in ban_ghi)
    dong += [f"- Số tuyên bố có dieu_kien_khac: {len(tb_khac)}/{len(ban_ghi)}.",
             f"- Số mục tài liệu giữ có dieu_kien_khac: {len(tl_khac)}/{tong_tl}.", ""]
    cum = dem(f"{dk['loai']}: {o_van_ban(dk['cum'])}" for _, ds in tb_khac for dk in ds)
    dong += ["Cụm ở phía tuyên bố:", ""] + [f"- {c} (x{n})" for c, n in cum.items()] if cum else ["Cụm ở phía tuyên bố: (không có)"]
    cum = dem(f"{dk['loai']}: {o_van_ban(dk['cum'])}" for _, _, ds in tl_khac for dk in ds)
    dong += ["", "Cụm ở phía tài liệu:", ""] + [f"- {c} (x{n})" for c, n in cum.items()] if cum else ["", "Cụm ở phía tài liệu: (không có)"]

    khac_sp = sum(1 for b in ban_ghi for m in b["bang_chung"] if m["khac_san_pham"])
    dong += ["", "## Sản phẩm", "", f"- Số mục tài liệu khac_san_pham: {khac_sp}."]

    co_so = [b for b in ban_ghi if b["id"] in tuyen_bo_goc]
    khop = sum(1 for b in co_so if b["tuyen_bo"] and b["tuyen_bo"]["thuoc_tinh"] == tuyen_bo_goc[b["id"]].get("thuoc_tinh"))
    dong += ["", "## Thuộc tính so với tách tay (tham khảo, đo chính thức ở Bước 28)", "",
             f"- Tỉ lệ thuoc_tinh trích khớp thuoc_tinh tách tay: {o_ty_le(khop, len(co_so))}."]
    return dong


def main(argv=None):
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Chạy trích xuất có neo nguồn (Bước 22).")
    ap.add_argument("--tuyen-bo", type=Path, default=TEP_TUYEN_BO, help=f"tệp tuyên bố (mặc định {TEP_TUYEN_BO.relative_to(ROOT)})")
    ap.add_argument("--ma-mau", nargs="+", default=None, metavar="MA", help="chỉ chạy tuyên bố của các mẫu này (mặc định tất cả)")
    ap.add_argument("--mo-hinh", default=MO_HINH_MAC_DINH, help=f"mã mô hình (mặc định {MO_HINH_MAC_DINH}; có {', '.join(NHA_CUNG_CAP)})")
    ap.add_argument("--k", type=int, default=5, help="số đoạn đưa vào câu lệnh (mặc định 5)")
    ap.add_argument("--cach-tach", choices=th.CACH_TACH, default="am_tiet", help="cách tách của BM25 (mặc định am_tiet)")
    ap.add_argument("--max-token-ra", type=int, default=tx.MAX_TOKEN_RA, help=f"max_output_tokens mỗi lần gọi (mặc định {tx.MAX_TOKEN_RA})")
    ap.add_argument("--nghi-giay", type=float, default=NGHI_MAC_DINH,
                    help=f"giây nghỉ sau mỗi lần gọi thật (mặc định {NGHI_MAC_DINH}; không áp dụng khi lấy từ bộ nhớ đệm hoặc --gia)")
    ap.add_argument("--timeout", type=float, default=TIMEOUT_MAC_DINH, help=f"giây chờ mỗi lần gọi (mặc định {TIMEOUT_MAC_DINH})")
    ap.add_argument("--gia", action="store_true", help="dùng LLM giả để chạy thử, ghi sang thư mục và tệp có hậu tố _gia")
    ap.add_argument("--khong-neo-nguon", action="store_true", help="tắt neo nguồn (P−NN, dùng cùng --khong-kiem-day-du)")
    ap.add_argument("--khong-kiem-day-du", action="store_true", help="tắt kiểm tra đầy đủ (P−NN, dùng cùng --khong-neo-nguon)")
    ap.add_argument("--thu-muc-ra", type=Path, default=THU_MUC_RA, help=f"thư mục kết quả (mặc định {THU_MUC_RA.relative_to(ROOT)})")
    args = ap.parse_args(argv)

    if args.mo_hinh not in NHA_CUNG_CAP:
        ap.error(f"mô hình chưa có nhà cung cấp trong b0.NHA_CUNG_CAP: {args.mo_hinh}")
    if args.k < 1:
        ap.error("--k phải từ 1 trở lên")
    neo_nguon, kiem_day_du = not args.khong_neo_nguon, not args.khong_kiem_day_du

    tuyen_bo = doc_jsonl(args.tuyen_bo)
    if args.ma_mau:
        tuyen_bo = [tb for tb in tuyen_bo if tb["ma_mau"] in set(args.ma_mau)]
    if not tuyen_bo:
        sys.exit("không có tuyên bố nào để chạy")
    try:
        tep_ten = args.tuyen_bo.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        tep_ten = str(args.tuyen_bo)

    thu_muc = args.thu_muc_ra.with_name(args.thu_muc_ra.name + "_gia") if args.gia else args.thu_muc_ra
    ten = ten_ket_qua(args.tuyen_bo, args.mo_hinh, args.k, args.cach_tach, neo_nguon, kiem_day_du, args.gia)
    if args.gia:
        client = LLMClient(thu_muc / "llm_cache", thu_muc / "llm_calls.jsonl", max_retries=SO_LAN_THU_LAI,
                           transport=tx.gia_transport)
    else:
        if load_dotenv is None:
            print("Cảnh báo: chưa cài python-dotenv, không nạp .env; chỉ dùng biến môi trường có sẵn.", file=sys.stderr)
        else:
            load_dotenv(ROOT / ".env", override=False, interpolate=False)
        client = LLMClient(thu_muc / "llm_cache", thu_muc / "llm_calls.jsonl", timeout_s=args.timeout,
                           max_retries=SO_LAN_THU_LAI)

    ban_ghi, vua_goi_that = [], False
    for i, tb in enumerate(tuyen_bo, start=1):
        if vua_goi_that and args.nghi_giay > 0:
            time.sleep(args.nghi_giay)
        try:
            bg = tx.trich_xuat(tb, tb["ma_mau"], client, args.mo_hinh, args.k, args.cach_tach, neo_nguon, kiem_day_du,
                               max_token_ra=args.max_token_ra)
        except LLMError as e:
            print(f"\nDỪNG ở tuyên bố {tb['id']} ({i}/{len(tuyen_bo)}): {e.code}.\nKhông ghi kết quả. Các tuyên bố đã gọi xong nằm "
                  "trong bộ nhớ đệm; chạy lại cùng lệnh để làm tiếp.", file=sys.stderr)
            return 1
        vua_goi_that = not args.gia and not bg["tu_bo_nho_dem"]
        print(f"{i}/{len(tuyen_bo)} {tb['id']}: {'LOI ' + bg['loi'] if bg['loi'] else 'ok'}"
              f"{'' if bg['tu_bo_nho_dem'] else ' (gọi mới)'}", file=sys.stderr, flush=True)
        ban_ghi.append(bg)

    # tu_bo_nho_dem khác nhau giữa lần chạy đầu và chạy lại; bỏ để tệp giống từng byte.
    ghi_tep(thu_muc / f"{ten}.jsonl",
            "".join(json.dumps({k: v for k, v in bg.items() if k != "tu_bo_nho_dem"}, ensure_ascii=False) + "\n" for bg in ban_ghi))
    thiet_lap = {"tep": tep_ten, "mo_hinh": args.mo_hinh, "k": args.k, "cach_tach": args.cach_tach, "neo_nguon": neo_nguon,
                 "kiem_day_du": kiem_day_du, "max_token_ra": args.max_token_ra}
    dong = tao_thong_ke(ban_ghi, thiet_lap, {tb["id"]: tb for tb in tuyen_bo}, args.gia)
    ghi_tep(thu_muc / f"thong_ke_{ten}.md", "\n".join(dong) + "\n")
    print("\n".join(dong))
    print(f"\nĐã ghi {thu_muc / (ten + '.jsonl')} và {thu_muc / ('thong_ke_' + ten + '.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
