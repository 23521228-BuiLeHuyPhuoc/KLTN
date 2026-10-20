"""Nhập trang nguồn đã lưu thủ công từ Chrome thật (Bước 6), dùng khi chup_nguon.py bị chặn (HTTP 403).

Với mỗi trang trong tệp thông tin: chép nguyên byte <ma_mau>__url__page.html / .txt (hoặc __bo_sung__)
từ thư mục --tu vào data/nguon/<ma_mau>/ (trang url_bo_sung vào bo_sung/) thành page.html, page.txt;
dựng full.png từ page.html đã chép bằng Chromium headless tắt JavaScript; ghi meta.json.
full.png KHÔNG phải ảnh chụp trực tiếp trang trên Chrome: meta.json ghi rõ cách tạo.
Không đổi User-Agent, không lách chặn: tài nguyên nào bị từ chối thì chấp nhận thiếu và chỉ đếm lại.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from importlib import metadata
import json
from pathlib import Path
import shutil
import sys
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chup_nguon as chup  # noqa: E402

ROOT = chup.ROOT
SCRIPT = "scripts/nhap_nguon_thu_cong.py"
OUT_ROOT = chup.OUT_ROOT

PHUONG_PHAP = "thu_cong_chrome"
CACH_TAO_PNG = ("Dựng lại từ page.html đã lưu bằng Chromium headless, tắt JavaScript; "
                "không phải ảnh chụp trực tiếp trang trên Chrome")
HTML_CONTENT_TYPE = "text/html; charset=utf-8"
# Tên tệp nguồn trong thư mục tải về: <ma_mau>__<nhãn>__<tên tệp đích>.
SOURCE_TAG = {"url": "url", "url_bo_sung": "bo_sung"}
SOURCE_FILES = ("page.html", "page.txt")
STALE_FILES = ("full.png", "meta.json")  # của lần chụp trước (403), xóa trước khi nhập

GOTO_TIMEOUT_MS = 45000
NETWORKIDLE_TIMEOUT_MS = 15000


# --- Hàm thuần (không cần mạng) ---

def source_names(ma_mau, vai_tro):
    """{tên tệp đích: tên tệp nguồn} cho một trang."""
    if vai_tro not in SOURCE_TAG:
        raise ValueError(f"vai_tro không hợp lệ: {vai_tro!r}")
    return {name: f"{ma_mau}__{SOURCE_TAG[vai_tro]}__{name}" for name in SOURCE_FILES}


def resolve_target(page, rows, out_root=OUT_ROOT):
    """Thư mục đích của trang; ném ValueError nếu url trong tệp thông tin khác cột url/url_bo_sung của CSV."""
    ma_mau, vai_tro = page["ma_mau"], page["vai_tro"]
    row = next((r for r in rows if r["ma_mau"] == ma_mau), None)
    if row is None:
        raise ValueError(f"ma_mau không có trong CSV: {ma_mau}")
    for csv_role, csv_url, out_dir in chup.targets_for(row, out_root):
        if csv_role == vai_tro:
            if page["url"] != csv_url:
                raise ValueError(f"url trong tệp thông tin khác CSV ({vai_tro}): {page['url']} != {csv_url}")
            return out_dir
    raise ValueError(f"{ma_mau} không có {vai_tro} trong CSV")


def copy_page_files(src_dir, out_dir, ma_mau, vai_tro):
    """Chép nguyên byte page.html, page.txt vào out_dir; xóa full.png, meta.json cũ.

    Thiếu tệp nguồn thì ném FileNotFoundError trước khi động vào out_dir (bằng chứng cũ còn nguyên).
    """
    names = source_names(ma_mau, vai_tro)
    missing = [src for src in names.values() if not (Path(src_dir) / src).is_file()]
    if missing:
        raise FileNotFoundError("Thiếu tệp nguồn: " + ", ".join(missing))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in STALE_FILES:
        (out_dir / name).unlink(missing_ok=True)
    for dest, src in names.items():
        shutil.copyfile(Path(src_dir) / src, out_dir / dest)


def resource_host(url):
    return urlparse(url).hostname or "(không rõ)"


def host_counts(urls):
    """{host: số request lỗi}, host nhiều lỗi nhất trước."""
    return dict(Counter(resource_host(u) for u in urls).most_common())


def base_meta(page, thong_tin):
    """Phần meta lấy từ tệp thông tin (lúc lưu trên Chrome thật)."""
    captured = datetime.fromisoformat(page["captured_at_utc"])
    if captured.tzinfo is None:
        raise ValueError(f"captured_at_utc thiếu múi giờ: {page['captured_at_utc']}")
    utc, local = chup.timestamps(captured.astimezone(timezone.utc))
    browser = thong_tin["trinh_duyet"]
    return {"ma_mau": page["ma_mau"], "vai_tro": page["vai_tro"], "requested_url": page["url"],
            "final_url": page["url"], "http_status": page["http_status"], "title": page["title"],
            "captured_at_utc": utc, "captured_at": local, "phuong_phap": PHUONG_PHAP,
            "ghi_chu_phuong_phap": thong_tin["ghi_chu"], "user_agent": browser["user_agent"],
            "viewport": browser["viewport"], "page_scroll_height": page["page_scroll_height"]}


def full_png_meta(png, dung_luc_utc, resource_errors, networkidle, note=None):
    width, height = chup.png_size(png)
    meta = {"width": width, "height": height, "cach_tao": CACH_TAO_PNG, "dung_luc_utc": dung_luc_utc,
            "networkidle": networkidle, "tai_nguyen_loi": resource_errors}
    if note:
        meta["ghi_chu"] = note
    return meta


def write_meta(out_dir, meta):
    (Path(out_dir) / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8", newline="\n")


# --- Phần dùng trình duyệt ---

def render_full_png(browser, url, html, viewport, scroll_height):
    """Dựng ảnh toàn trang từ html (bytes); trả về (png, ghi_chu, tai_nguyen_loi, networkidle).

    page.route chỉ trả html cho đúng `url` để đường dẫn tương đối của CSS/ảnh phân giải theo trang gốc;
    mọi request khác đi mạng bình thường, bị từ chối thì chấp nhận thiếu và đếm theo host.
    """
    failed = []
    context = browser.new_context(viewport=viewport, locale=chup.LOCALE, java_script_enabled=False,
                                  device_scale_factor=1)
    try:
        page = context.new_page()
        page.on("requestfailed", lambda request: failed.append(request.url))
        page.on("response", lambda response: failed.append(response.url) if response.status >= 400 else None)
        page.route(lambda u: u == url,
                   lambda route: route.fulfill(status=200, body=html, content_type=HTML_CONTENT_TYPE))
        page.goto(url, wait_until="domcontentloaded", timeout=GOTO_TIMEOUT_MS)
        networkidle = True
        try:
            page.wait_for_load_state("networkidle", timeout=NETWORKIDLE_TIMEOUT_MS)
        except chup.PlaywrightTimeout:
            networkidle = False  # trang còn gọi mạng liên tục; vẫn chụp tiếp
        png, note = chup.full_page_png(page, scroll_height)
    finally:
        context.close()
    return png, note, host_counts(failed), networkidle


def nhap_trang(browser, page, rows, thong_tin, src_dir, out_root=OUT_ROOT):
    """Nhập một trang; trả về meta (có "error" nếu dựng ảnh lỗi).

    Ném lỗi khi chưa động tới thư mục đích được (url khác CSV, thiếu tệp nguồn).
    """
    out_dir = resolve_target(page, rows, out_root)
    copy_page_files(src_dir, out_dir, page["ma_mau"], page["vai_tro"])
    meta = base_meta(page, thong_tin)
    try:
        png, note, errors, networkidle = render_full_png(
            browser, page["url"], (out_dir / "page.html").read_bytes(),
            thong_tin["trinh_duyet"]["viewport"], page["page_scroll_height"])
        (out_dir / "full.png").write_bytes(png)
        meta["full_png"] = full_png_meta(png, chup.timestamps()[0], errors, networkidle, note)
    except Exception as exc:
        meta["error"] = f"{type(exc).__name__}: {str(exc).splitlines()[0] if str(exc) else ''}"
    meta.update({"script": SCRIPT, "script_sha256": chup.sha256_file(ROOT / SCRIPT),
                 "playwright_version": metadata.version("playwright"), "chromium_version": browser.version,
                 "git_head": chup.git_head()})
    meta = chup.build_meta(meta, out_dir)
    write_meta(out_dir, meta)
    return meta, out_dir


def print_report(meta, out_dir):
    label = f"{meta['ma_mau']} [{meta['vai_tro']}]"
    if meta.get("error"):
        print(f"LỖI {label}: {meta['error']}")
        return
    where = out_dir.relative_to(ROOT) if out_dir.is_relative_to(ROOT) else out_dir
    png = meta["full_png"]
    errors = png["tai_nguyen_loi"]
    detail = ", ".join(f"{host}: {n}" for host, n in errors.items())
    print(f"OK {label}: full.png {png['width']}x{png['height']}, tài nguyên lỗi {sum(errors.values())}"
          + (f" ({detail})" if detail else "") + f", ghi vào {where}")
    if not png["networkidle"]:
        print("    networkidle hết giờ: số tài nguyên lỗi có thể chưa đủ")
    if png.get("ghi_chu"):
        print("    ghi chú: " + png["ghi_chu"])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Nhập trang nguồn đã lưu thủ công từ Chrome thật.")
    parser.add_argument("--tu", required=True, type=Path, help="thư mục chứa <ma_mau>__url__page.html...")
    parser.add_argument("--thong-tin", required=True, type=Path, help="tệp JSON thông tin lúc lưu")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    thong_tin = json.loads(args.thong_tin.read_text(encoding="utf-8"))
    rows = chup.read_samples()

    from playwright.sync_api import sync_playwright
    failed = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for page in thong_tin["trang"]:
                try:
                    meta, out_dir = nhap_trang(browser, page, rows, thong_tin, args.tu)
                except Exception as exc:
                    print(f"LỖI {page.get('ma_mau')} [{page.get('vai_tro')}]: "
                          f"{type(exc).__name__}: {str(exc).splitlines()[0] if str(exc) else ''}")
                    failed += 1
                    continue
                print_report(meta, out_dir)
                failed += bool(meta.get("error"))
        finally:
            browser.close()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
