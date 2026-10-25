"""Trích lại văn bản PDF bằng pdftotext (Xpdf) để chia đoạn, thay cho bản trích pypdf.

pypdf đọc sai khoảng cách với font của hướng dẫn Galaxy Watch8: tách âm tiết ('v ào', khoảng 4.528 chỗ)
và tách cả con số ('1 00–150 BPM' ở trang 95). pdftotext giữ đúng khoảng cách; bỏ khoảng trắng thì tập
ký tự từng trang trùng bản pypdf. page.txt (bản pypdf) giữ nguyên vì mã băm đã ghi; bản mới ghi vào
page_pdftotext.txt cùng định dạng '=== Trang N ===', meta.json thêm mã băm và phiên bản công cụ.
Cần chương trình pdftotext trong PATH (đi kèm Git for Windows, hoặc cài Xpdf/Poppler).
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chup_nguon as chup  # noqa: E402

SCRIPT = "scripts/trich_pdf_pdftotext.py"
TEN_TEP = "page_pdftotext.txt"
LENH = ["pdftotext", "-enc", "UTF-8"]
LY_DO = ("pypdf tách âm tiết và tách số (ví dụ '1 00–150 BPM'); bản này dùng để chia đoạn, "
         "page.txt (pypdf) giữ nguyên")


# --- Hàm thuần ---

def tach_trang(van_ban):
    """pdftotext ngắt trang bằng ký tự \\f; sau trang cuối cũng có một \\f."""
    trang = van_ban.replace("\r\n", "\n").split("\f")
    if trang and not trang[-1].strip():
        trang = trang[:-1]
    return trang


def dinh_dang(trang):
    """Cùng định dạng page.txt của nhánh PDF trong chup_nguon.py."""
    return "\n".join(f"=== Trang {n} ===\n{t.strip()}\n" for n, t in enumerate(trang, start=1))


def phien_ban(dau_ra_v):
    m = re.search(r"pdftotext version (\S+)", dau_ra_v)
    return m.group(1) if m else None


# --- Chạy ---

def thu_muc_pdf(out_root=chup.OUT_ROOT):
    """Các thư mục nguồn có meta.json loai 'pdf'."""
    for meta_path in sorted([*out_root.glob("*/meta.json"), *out_root.glob("*/bo_sung/meta.json")]):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("loai") == "pdf":
            yield meta_path.parent, meta


def trich_mot(thu_muc, meta):
    pdf = thu_muc / "tai_lieu.pdf"
    assert chup.sha256_file(pdf) == meta["files"]["tai_lieu.pdf"]["sha256"], f"{pdf}: mã băm lệch meta.json"
    p = subprocess.run([*LENH, str(pdf), "-"], capture_output=True, timeout=300, check=True)
    trang = tach_trang(p.stdout.decode("utf-8"))
    assert len(trang) == meta["pdf"]["pages"], f"{pdf}: {len(trang)} trang, meta.json ghi {meta['pdf']['pages']}"
    ra = thu_muc / TEN_TEP
    chup.write_text(ra, dinh_dang(trang))

    v = subprocess.run(["pdftotext", "-v"], capture_output=True, text=True, timeout=15)
    utc, vn = chup.timestamps()
    meta["files"][TEN_TEP] = {"sha256": chup.sha256_file(ra), "bytes": ra.stat().st_size}
    meta["trich_lai_pdf"] = {
        "tep": TEN_TEP,
        "cong_cu": "pdftotext",
        "phien_ban": phien_ban(v.stdout + v.stderr),
        "lenh": " ".join([*LENH, "tai_lieu.pdf", "-"]),
        "captured_at_utc": utc,
        "captured_at": vn,
        "script": SCRIPT,
        "script_sha256": chup.sha256_file(chup.ROOT / SCRIPT),
        "git_head": chup.git_head(),
        "ly_do": LY_DO,
    }
    (thu_muc / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                       encoding="utf-8", newline="\n")
    return ra, len(trang)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Trích lại PDF nguồn bằng pdftotext.")
    parser.add_argument("ma_mau", nargs="*", help="bỏ trống = mọi PDF trong data/nguon/")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    for thu_muc, meta in thu_muc_pdf():
        if args.ma_mau and meta["ma_mau"] not in args.ma_mau:
            continue
        ra, so_trang = trich_mot(thu_muc, meta)
        print(f"{ra.relative_to(chup.ROOT).as_posix()}: {so_trang} trang")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
