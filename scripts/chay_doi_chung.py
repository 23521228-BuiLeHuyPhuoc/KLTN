"""Chạy B1/B2, chỉ ghi đầu ra hệ thống; không đọc nhãn chuẩn."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kiemchung.doi_chung import b1, b2
from kiemchung.doi_chung.chung import NHA_CUNG_CAP, gia_transport
from kiemchung.doi_chung.huong_dan import huong_dan_cho_cau_lenh, vi_du_b2, dinh_dang_vi_du
from kiemchung.llm import LLMClient, LLMError


def doc_jsonl(tep):
    """Đọc tệp JSONL UTF-8, bỏ dòng trắng."""
    return [json.loads(d) for d in Path(tep).read_text(encoding="utf-8-sig").splitlines() if d.strip()]


def ghi_tep(tep, chu):
    """Ghi nguyên tử với xuống dòng LF."""
    tep.parent.mkdir(parents=True, exist_ok=True)
    tam = tep.with_name(tep.name + ".tmp")
    tam.write_text(chu, encoding="utf-8", newline="\n")
    tam.replace(tep)


def ten_tep(chu):
    """Đổi ký tự không hợp lệ trong tên mô hình thành gạch dưới."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", chu)


def tham_so_chung(ap, thu_muc_ra):
    """Các tham số chung cho hai script Bước 29–30."""
    ap.add_argument("--tuyen-bo", type=Path, default=ROOT / "data/tuyen_bo/thu.jsonl")
    ap.add_argument("--ma-mau", help="mã mẫu, có thể cách nhau bằng dấu phẩy")
    ap.add_argument("--mo-hinh", default="gemini-3.6-flash", choices=tuple(NHA_CUNG_CAP))
    ap.add_argument("--max-token-ra", type=int, default=4096)
    ap.add_argument("--nghi-giay", type=float, default=20)
    ap.add_argument("--timeout", type=float, default=90)
    ap.add_argument("--gia", action="store_true")
    ap.add_argument("--thu-muc-ra", type=Path, default=thu_muc_ra)


def kiem_tham_so(ap, args):
    """Chặn tham số thời gian và giới hạn đầu ra không hợp lệ."""
    if not math.isfinite(args.nghi_giay) or args.nghi_giay < 0:
        ap.error("--nghi-giay phải hữu hạn và không âm")
    if not math.isfinite(args.timeout) or args.timeout <= 0 or args.max_token_ra < 1:
        ap.error("--timeout và --max-token-ra phải dương")


def tao_client(args, transport):
    """Chạy thật dùng bộ nhớ đệm chung của P/B0; chạy giả ghi riêng dưới thư mục đầu ra."""
    if args.gia:
        goc = args.thu_muc_ra / "gia"
        return LLMClient(goc / "llm_cache", goc / "llm_calls.jsonl", timeout_s=args.timeout, transport=transport)
    try:
        from dotenv import load_dotenv
    except ImportError:
        pass
    else:
        load_dotenv(ROOT / ".env", override=False, interpolate=False)
    return LLMClient(ROOT / "ket_qua/llm_cache", ROOT / "ket_qua/llm_calls.jsonl", timeout_s=args.timeout)


def loc_mau(ds, ma_mau):
    """Lọc danh sách theo các mã mẫu yêu cầu."""
    ma = {m.strip() for m in ma_mau.split(",")} if ma_mau else None
    return [d for d in ds if ma is None or d["ma_mau"] in ma]


def jsonl_on_dinh(ds):
    """Không ghi cờ bộ nhớ đệm hoặc thời gian vào JSONL kết quả."""
    return "".join(json.dumps({k: v for k, v in d.items() if k not in {"tu_bo_nho_dem", "thoi_gian_sinh_ms"}},
                              ensure_ascii=False, sort_keys=True) + "\n" for d in ds)


def main(argv=None):
    """Chạy một đối chứng, trả mã thoát; lỗi hạ tầng không ghi kết quả dở."""
    ap = argparse.ArgumentParser(description=__doc__)
    tham_so_chung(ap, ROOT / "ket_qua/doi_chung")
    ap.add_argument("--he", choices=("b1", "b2"), required=True)
    ap.add_argument("--trich-xuat", type=Path)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--cach-tach", default="am_tiet", choices=b2.th.CACH_TACH)
    args = ap.parse_args(argv)
    kiem_tham_so(ap, args)
    if args.he == "b1" and args.trich_xuat is None:
        ap.error("--he b1 bắt buộc có --trich-xuat")
    if args.k < 1:
        ap.error("--k phải dương")
    tep = args.trich_xuat if args.he == "b1" else args.tuyen_bo
    ds = loc_mau(doc_jsonl(tep), args.ma_mau)
    hd = huong_dan_cho_cau_lenh()
    vd = dinh_dang_vi_du(vi_du_b2()) if args.he == "b2" else None
    client = tao_client(args, gia_transport)
    kq, vua_goi = [], False
    for d in ds:
        if vua_goi and args.nghi_giay:
            time.sleep(args.nghi_giay)
        try:
            if args.he == "b1":
                r = b1.chay_mot(client, args.mo_hinh, d, hd, args.max_token_ra)
            else:
                r = b2.chay_mot(client, args.mo_hinh, d["tuyen_bo"], d["ma_mau"], args.k, args.cach_tach,
                                hd, vd, max_token_ra=args.max_token_ra)
                r["id"] = d["id"]
        except LLMError as e:
            print(f"Dừng: {e.code}; chưa ghi kết quả, có thể chạy lại từ bộ nhớ đệm.", file=sys.stderr)
            return 1
        kq.append(r)
        vua_goi = not args.gia and not r["tu_bo_nho_dem"]
    ten = f"{args.he}_{tep.stem}_{ten_tep(args.mo_hinh)}" + ("_gia" if args.gia else "")
    dem = Counter(r["nhan"] for r in kq)
    bo_dem = sum(r["tu_bo_nho_dem"] for r in kq)
    dong = [f"# {args.he.upper()}" + (" (LLM giả)" if args.gia else ""), "",
            f"Số bản ghi: {len(kq)}", "Phân bố nhãn hệ thống: " + ", ".join(f"{n}: {dem[n]}" for n in ("DUNG", "SAI", "LECH", "CHUA_DU", "LOI")),
            f"Số LOI: {dem['LOI']}", f"Số lần gọi thật: {0 if args.gia else len(kq) - bo_dem}",
            f"Số lần từ bộ nhớ đệm: {bo_dem}"]
    ghi_tep(args.thu_muc_ra / f"{ten}.jsonl", jsonl_on_dinh(kq))
    ghi_tep(args.thu_muc_ra / f"{ten}.md", "\n".join(dong) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
