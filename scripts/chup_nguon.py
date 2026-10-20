"""Capture official manufacturer spec pages as traceable evidence (Bước 5).

Mỗi trang lưu đúng 4 tệp vào data/nguon/<ma_mau>/ (trang url_bo_sung vào bo_sung/):
page.html (sau khi mở rộng), page.txt (văn bản nhìn thấy), full.png, meta.json.
Không sửa nội dung trang: chỉ cuộn, bấm nút mở rộng, và (nếu có) bấm "từ chối" cookie.

URL có đường dẫn kết thúc .pdf đi nhánh riêng (Chromium headless không hiển thị PDF): tải thẳng
bằng context.request rồi lưu tai_lieu.pdf (nguyên byte), page.txt (văn bản trích bằng pypdf), meta.json.
"""
import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
from importlib import metadata
import io
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
from urllib.parse import urlparse

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "scripts/chup_nguon.py"
CSV_PATH = ROOT / "data/mau_san_pham.csv"
OUT_ROOT = ROOT / "data/nguon"

VIEWPORT = {"width": 1440, "height": 1000}
LOCALE = "vi-VN"
TIMEZONE = "Asia/Ho_Chi_Minh"
# Việt Nam không có giờ mùa hè nên UTC+7 cố định đúng; tránh phụ thuộc tzdata trên Windows.
VN_TZ = timezone(timedelta(hours=7))

PAGE_FILES = ("page.html", "page.txt", "full.png", "tai_lieu.pdf", "meta.json")
HASHED_FILES = ("tai_lieu.pdf", "page.html", "page.txt", "full.png")

PDF_MAGIC = b"%PDF"
PDF_TIMEOUT_MS = 60000
PDF_MIN_CHARS = 200  # page.txt ngắn hơn mức này thì nhiều khả năng PDF là ảnh quét, không có lớp chữ
# Trường của nhánh trang thường không có nghĩa với PDF.
HTML_ONLY_META = ("title", "viewport", "user_agent", "expansion_clicks")

EXPAND_TEXT = re.compile(r"xem thêm|mở rộng|chi tiết|thông số|xem tất cả|lưu ý|chú thích", re.I)
REJECT_TEXT = re.compile(r"từ chối|reject|decline|refuse|deny", re.I)
FOOTNOTE_KEYWORDS = re.compile(r"thử nghiệm|kết quả thực tế|có thể thay đổi|điều kiện", re.I)
FOOTNOTE_START = re.compile(r"^(\*|\d+\.\s)")

EXPAND_SELECTOR = 'button, [role="button"], [aria-expanded="false"]'
CONSENT_SELECTOR = ('[id*="cookie" i], [class*="cookie" i], [id*="consent" i], [class*="consent" i], '
                    '[id*="onetrust" i], [class*="onetrust" i], [id*="gdpr" i], [class*="gdpr" i], '
                    '[aria-label*="cookie" i]')
AREA_SELECTOR = ('[id*="spec" i], [class*="spec" i], [id*="disclaimer" i], [class*="disclaimer" i], '
                 '[id*="footnote" i], [class*="footnote" i], [class*="legal" i], [class*="sosumi" i], '
                 '[class*="technical" i]')
NAV_SELECTOR = ('nav, header, [role="navigation"], [role="banner"], '
                '[id*="globalnav" i], [class*="globalnav" i]')
# Đánh giá/bình luận của người dùng: không phải thông số nhà sản xuất và đổi giữa các lần chụp.
EXCLUDE_SELECTOR = '[id*="review" i], [class*="review" i], [id*="comment" i], [class*="comment" i]'

SCROLL_STEP = 800
SCROLL_PAUSE_MS = 150
MAX_PASSES = 3
MAX_CLICKS = 40
MAX_RESTARTS = 2
CLICK_TIMEOUT_MS = 2000
MAX_SHOT_HEIGHT = 16000  # Chromium cắt ảnh toàn trang cao hơn khoảng 16384 px
# Thời hạn (ms) từng lần chụp ảnh toàn trang. Có trang (vd. OPPO Find X8) kẹt vô hạn ở lần chụp
# toàn trang đầu tiên dù timeout dài bao nhiêu, nhưng sau khi lần đó bị hủy thì lần kế chụp xong
# trong vài giây; nên lần đầu để ngắn rồi chụp lại thay vì chờ 60 s.
SHOT_TIMEOUTS_MS = (15000, 60000)

# Chạy trong trang, chỉ đọc DOM. `els` là danh sách ElementHandle.
INFO_JS = """([els, area, consent, nav, exclude]) => els.map(el => {
  // Bỏ qua body/html: <body class="page-specs"> không phải vùng thông số.
  const within = sel => { const n = el.closest(sel); return !!n && n !== document.body && n !== document.documentElement; };
  const norm = s => (s || '').replace(/\\s+/g, ' ').trim();
  const cs = getComputedStyle(el);
  const r = el.getBoundingClientRect();
  const text = norm(el.innerText || el.textContent) || norm(el.getAttribute('aria-label')) || norm(el.getAttribute('title'));
  const path = [];
  for (let n = el; n && n.nodeType === 1 && n !== document.body; n = n.parentElement) {
    const same = n.parentElement ? [...n.parentElement.children].filter(c => c.tagName === n.tagName) : [n];
    path.push(n.tagName.toLowerCase() + ':' + same.indexOf(n));
  }
  return {
    tag: el.tagName.toLowerCase(),
    role: el.getAttribute('role'),
    ariaExpanded: el.getAttribute('aria-expanded'),
    type: el.getAttribute('type'),
    href: el.tagName === 'A' ? el.getAttribute('href') : null,
    disabled: el.disabled === true || el.getAttribute('aria-disabled') === 'true',
    inForm: !!el.closest('form'),
    inArea: within(area),
    inConsent: within(consent),
    inNav: within(nav),
    inExclude: within(exclude),
    visible: r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none',
    text: text.slice(0, 120),
    key: path.join('>'),
  };
})"""

SCROLL_JS = """async ([step, pause]) => {
  for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
    window.scrollTo(0, y);
    await new Promise(resolve => setTimeout(resolve, pause));
  }
  window.scrollTo(0, 0);
  await document.fonts.ready;
  const pending = [...document.images].filter(img => !img.complete);
  await Promise.race([
    Promise.all(pending.map(img => new Promise(resolve => { img.onload = img.onerror = resolve; }))),
    new Promise(resolve => setTimeout(resolve, 8000)),
  ]);
  return document.documentElement.scrollHeight;
}"""

# Độ dài văn bản nhìn thấy và số hộp thoại đang hiện: dùng để đánh giá một cú bấm mở hay đóng nội dung.
STATE_JS = """() => ({
  chars: document.body.innerText.length,
  dialogs: [...document.querySelectorAll('[role="dialog"], [role="alertdialog"], [aria-modal="true"], dialog[open]')]
    .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden'; }).length,
})"""

# Mọi nút văn bản trong body, bỏ script/style; dùng để so với innerText.
TEXT_NODES_JS = """() => {
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode: n => n.parentElement && !n.parentElement.closest('script, style, noscript, template')
      ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT,
  });
  while (walker.nextNode()) out.push(walker.currentNode.nodeValue);
  return out;
}"""


# --- Hàm thuần (không cần mạng) ---

def read_samples(path=CSV_PATH):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def select_rows(rows, ma_mau, tat_ca=False):
    if tat_ca:
        return list(rows)
    by_id = {row["ma_mau"]: row for row in rows}
    unknown = [m for m in ma_mau if m not in by_id]
    if unknown:
        raise ValueError("ma_mau không có trong CSV: " + ", ".join(unknown))
    if not ma_mau:
        raise ValueError("Cần ít nhất một ma_mau hoặc --tat-ca")
    return [by_id[m] for m in dict.fromkeys(ma_mau)]


def targets_for(row, out_root=OUT_ROOT):
    """(vai_tro, url, thư mục) cho url chính và url_bo_sung nếu có."""
    base = Path(out_root) / row["ma_mau"]
    targets = [("url", row["url"].strip(), base)]
    if row.get("url_bo_sung", "").strip():
        targets.append(("url_bo_sung", row["url_bo_sung"].strip(), base / "bo_sung"))
    return targets


def host_of(url):
    host = (urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def is_pdf_url(url):
    """Đường dẫn (bỏ query/fragment) kết thúc .pdf, không phân biệt hoa thường."""
    return urlparse(url).path.lower().endswith(".pdf")


def check_pdf_response(status, body):
    """Ném RuntimeError nếu phản hồi không phải PDF hợp lệ (HTTP khác 200 hoặc thiếu %PDF)."""
    if status != 200:
        raise RuntimeError(f"HTTP {status}")
    if not body.startswith(PDF_MAGIC):
        raise RuntimeError("Nội dung tải về không bắt đầu bằng %PDF")


def extract_pdf_text(data):
    """(văn bản, số trang). Mỗi trang mở đầu bằng dòng '=== Trang N ==='."""
    reader = PdfReader(io.BytesIO(data))
    parts = [f"=== Trang {n} ===\n{(page.extract_text() or '').strip()}\n"
             for n, page in enumerate(reader.pages, start=1)]
    return "\n".join(parts), len(reader.pages)


def pdf_text_chars(text):
    """Số ký tự văn bản trích, không tính các dòng '=== Trang N ===' và khoảng trắng đầu/cuối."""
    return len(re.sub(r"^=== Trang \d+ ===$", "", text, flags=re.M).strip())


def pdf_meta_fields(pages, content_type, size):
    """Trường meta riêng của nhánh PDF."""
    return {"loai": "pdf", "pdf": {"pages": pages, "content_type": content_type, "bytes": size}}


def pdf_text_warning(chars):
    """Cảnh báo nếu văn bản trích quá ngắn; None nếu ổn."""
    if chars == 0:
        return "page.txt rỗng: PDF có thể là ảnh, cần OCR hoặc kiểm tay"
    if chars < PDF_MIN_CHARS:
        return f"page.txt chỉ có {chars} ký tự (< {PDF_MIN_CHARS}): PDF có thể là ảnh, cần kiểm tay"
    return None


def is_expand_candidate(info):
    """Chỉ nút (button / role=button / aria-expanded=false), không phải liên kết điều hướng."""
    if not info["visible"] or info["disabled"] or info["inConsent"]:
        return False
    if info["ariaExpanded"] == "true":
        return False
    if info["tag"] == "a" and (info["href"] or "").strip() not in ("", "#"):
        return False
    if info["inForm"] and info["type"] == "submit":
        return False
    if info["inNav"] and not info["inArea"]:
        return False
    if info["inExclude"]:
        return False
    is_button = info["tag"] == "button" or info["role"] == "button" or info["ariaExpanded"] == "false"
    if not is_button:
        return False
    if EXPAND_TEXT.search(info["text"]):
        return True
    return info["ariaExpanded"] == "false" and info["inArea"]


def is_reject_button(info):
    """Chỉ nút 'từ chối' nằm trong banner cookie; không bao giờ là nút chấp nhận."""
    is_button = info["tag"] == "button" or info["role"] == "button"
    return bool(info["visible"] and info["inConsent"] and is_button and REJECT_TEXT.search(info["text"]))


def is_footnote_like(line):
    line = line.strip()
    return bool(line and (FOOTNOTE_START.match(line) or FOOTNOTE_KEYWORDS.search(line)))


def _norm(text):
    return re.sub(r"\s+", " ", text).strip().casefold()


def hidden_footnotes(text_nodes, inner_text):
    """Dòng giống chú thích có trong DOM nhưng không có trong văn bản nhìn thấy."""
    visible = _norm(inner_text)
    seen, hidden = set(), []
    for node in text_nodes:
        line = re.sub(r"\s+", " ", node).strip()
        if not is_footnote_like(line) or line in seen:
            continue
        seen.add(line)
        if _norm(line) not in visible:
            hidden.append(line)
    return hidden


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_meta(base, out_dir):
    """Gắn files {tên: {sha256, bytes}} cho 3 tệp dữ liệu đã ghi (tệp thiếu thì bỏ qua)."""
    files = {}
    for name in HASHED_FILES:
        p = Path(out_dir) / name
        if p.exists():
            files[name] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    return {**base, "files": files}


def timestamps(now=None):
    now = now or datetime.now(timezone.utc)
    return now.isoformat(timespec="seconds"), now.astimezone(VN_TZ).isoformat(timespec="seconds")


def png_size(data):
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "không phải PNG"
    return struct.unpack(">II", data[16:24])  # (rộng, cao)


def write_text(path, text):
    Path(path).write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def git_head():
    try:
        p = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                           timeout=15, cwd=ROOT)
        return p.stdout.strip() if p.returncode == 0 else None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


# --- Phần dùng trình duyệt ---

def describe(page, selector):
    """(handles, infos) của các phần tử khớp selector; infos cùng thứ tự với handles."""
    handles = page.query_selector_all(selector)
    infos = page.evaluate(INFO_JS, [handles, AREA_SELECTOR, CONSENT_SELECTOR, NAV_SELECTOR,
                                    EXCLUDE_SELECTOR])
    return handles, infos


def button_infos(page):
    return describe(page, "button, [role='button']")


def banner_visible(page):
    """Còn banner cookie hiện trên trang không."""
    return any(i["inConsent"] and i["visible"] for i in button_infos(page)[1])


def reject_consent(page):
    """Bấm 'từ chối' nếu có banner cookie; không bấm chấp nhận. Trả về mô tả cho meta."""
    handles, infos = button_infos(page)
    banner = any(i["inConsent"] and i["visible"] for i in infos)
    rejected = None
    for handle, info in zip(handles, infos):
        if is_reject_button(info):
            try:
                handle.click(timeout=3000)
                page.wait_for_timeout(500)
                rejected = info["text"]
            except Exception:
                pass
            break
    return {"banner_detected": banner, "rejected": rejected}


def go_back_to(page, url):
    """Quay lại url sau khi một cú bấm làm đổi URL."""
    try:
        page.go_back(wait_until="domcontentloaded", timeout=15000)
    except Exception:
        pass
    if page.url != url:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)


def page_state(page):
    """STATE_JS sau khi hoạt ảnh mở/đóng đã lắng xuống."""
    state = page.evaluate(STATE_JS)
    for _ in range(6):
        page.wait_for_timeout(250)
        newer = page.evaluate(STATE_JS)
        if newer == state:
            break
        state = newer
    return state


def expand_collapsed(page, loads):
    """Bấm các nút mở rộng. Trả về (clicks, skipped, restarts).

    clicks chỉ gồm cú bấm làm tăng văn bản nhìn thấy. Aria-expanded có thể lỗi thời (vd. Samsung:
    "Xem thêm" mở tất cả nhưng các accordion vẫn ghi false), nên cú bấm làm văn bản giảm sẽ bị
    bấm lại để khôi phục, và cú bấm mở hộp thoại sẽ bị đóng bằng Escape.
    """
    clicks, skipped, nav_keys = [], [], set()
    done, restarts = set(), 0
    state = page_state(page)
    for _ in range(MAX_PASSES + MAX_RESTARTS):
        handles, infos = describe(page, EXPAND_SELECTOR)
        todo = [(h, i) for h, i in zip(handles, infos)
                if is_expand_candidate(i) and i["key"] not in done]
        # Nút có chữ "xem thêm/mở rộng..." thường là nút điều khiển chung: bấm trước.
        todo.sort(key=lambda hi: not EXPAND_TEXT.search(hi[1]["text"]))
        if not todo or len(clicks) >= MAX_CLICKS:
            break
        reloaded = False
        for handle, info in todo:
            if len(clicks) >= MAX_CLICKS:
                break
            done.add(info["key"])
            label = info["text"] or info["tag"]
            before, loads_before = page.url, len(loads)
            try:
                handle.click(timeout=CLICK_TIMEOUT_MS)
            except Exception as exc:
                skipped.append({"text": label, "ly_do": "click lỗi: " + str(exc).splitlines()[0]})
                continue
            after = page_state(page)
            if page.url != before:
                skipped.append({"text": label, "ly_do": "URL đổi sang " + page.url})
                nav_keys.add(info["key"])
                go_back_to(page, before)
                state = page_state(page)
                if len(loads) > loads_before:
                    reloaded = True  # trang tải lại: các cú bấm trước đó đã mất
                break
            if after["dialogs"] > state["dialogs"]:
                page.keyboard.press("Escape")
                skipped.append({"text": label, "ly_do": "mở hộp thoại; đã đóng bằng Escape"})
                state = page_state(page)
                continue
            delta = after["chars"] - state["chars"]
            if delta < 0:
                reason = f"làm thu gọn {-delta} ký tự; đã bấm lại để khôi phục"
                try:
                    handle.click(timeout=CLICK_TIMEOUT_MS)
                except Exception as exc:
                    reason += "; bấm lại lỗi: " + str(exc).splitlines()[0]
                after = page_state(page)
                if after["chars"] < state["chars"]:
                    reason += f"; còn thiếu {state['chars'] - after['chars']} ký tự so với trước khi bấm"
                skipped.append({"text": label, "ly_do": reason})
            elif delta == 0:
                skipped.append({"text": label, "ly_do": "không đổi văn bản nhìn thấy"})
            else:
                clicks.append(label)
            state = after
        if reloaded:
            if restarts >= MAX_RESTARTS:
                break
            restarts += 1
            clicks.clear()
            done = set(nav_keys)
            page.evaluate(SCROLL_JS, [SCROLL_STEP, SCROLL_PAUSE_MS])
            state = page_state(page)
    return clicks, skipped, restarts


def full_page_png(page, scroll_height):
    """Ảnh toàn trang; trả về (bytes, ghi_chu). Ghi chú nếu phải chụp lại hoặc ảnh không phủ hết chiều cao trang."""
    notes = []
    for attempt, timeout in enumerate(SHOT_TIMEOUTS_MS, start=1):
        try:
            data = page.screenshot(full_page=True, animations="disabled", timeout=timeout)
            break
        except PlaywrightTimeout:
            if attempt == len(SHOT_TIMEOUTS_MS):
                raise
            notes.append(f"Lần chụp {attempt} quá {timeout} ms, đã chụp lại")
    width, height = png_size(data)
    if abs(height - scroll_height) > 50:  # lệch vài px do trang tự co giãn là bình thường
        notes.append(f"Ảnh cao {height} px khác chiều cao trang {scroll_height} px")
    return data, "; ".join(notes) or None


def capture_html(context, base, report, out_dir, url):
    """Nhánh trang thường: mở bằng trình duyệt, mở rộng nội dung, lưu html/txt/png."""
    page = context.new_page()
    context.on("page", lambda p: p.close() if p is not page else None)
    loads = []
    page.on("load", lambda _: loads.append(1))
    response = page.goto(url, wait_until="domcontentloaded", timeout=45000)
    base["networkidle"] = True
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        base["networkidle"] = False  # trang còn gọi mạng liên tục; vẫn chụp tiếp
    base["final_url"] = page.url
    base["http_status"] = response.status if response else None
    base["title"] = page.title()
    base["user_agent"] = page.evaluate("navigator.userAgent")
    if base["http_status"] != 200:
        raise RuntimeError(f"HTTP {base['http_status']}")
    if host_of(page.url) != host_of(url):
        raise RuntimeError(f"URL cuối khác host: {page.url}")

    base["consent"] = reject_consent(page)
    page.evaluate(SCROLL_JS, [SCROLL_STEP, SCROLL_PAUSE_MS])
    clicks, skipped, restarts = expand_collapsed(page, loads)
    scroll_height = page.evaluate(SCROLL_JS, [SCROLL_STEP, SCROLL_PAUSE_MS])
    base["expansion_clicks"] = clicks
    base["expansion_skipped"] = skipped
    if restarts:
        base["expansion_restarts"] = restarts
    base["consent"]["banner_visible_at_capture"] = banner_visible(page)

    inner_text = page.locator("body").inner_text()
    report["hidden"] = hidden_footnotes(page.evaluate(TEXT_NODES_JS), inner_text)
    write_text(out_dir / "page.html", page.content())
    write_text(out_dir / "page.txt", inner_text)
    png, note = full_page_png(page, scroll_height)
    (out_dir / "full.png").write_bytes(png)
    width, height = png_size(png)
    base["page_scroll_height"] = scroll_height
    base["full_png"] = {"width": width, "height": height}
    if note:
        base["full_png"]["ghi_chu"] = note


def capture_pdf(context, base, report, out_dir, url):
    """Nhánh PDF: tải bằng APIRequestContext (giữ Accept-Language), lưu nguyên byte + văn bản trích."""
    for key in HTML_ONLY_META:
        base.pop(key, None)
    base["loai"] = "pdf"
    response = context.request.get(url, headers={"Accept-Language": "vi-VN"}, timeout=PDF_TIMEOUT_MS)
    body = response.body()
    base["final_url"] = response.url
    base["http_status"] = response.status
    check_pdf_response(response.status, body)
    (out_dir / "tai_lieu.pdf").write_bytes(body)  # lưu trước khi trích: lỗi trích vẫn còn bản gốc
    text, pages = extract_pdf_text(body)
    write_text(out_dir / "page.txt", text)
    base.update(pdf_meta_fields(pages, response.headers.get("content-type"), len(body)))
    report["pdf_chars"] = pdf_text_chars(text)


def capture_target(browser, ma_mau, vai_tro, url, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in PAGE_FILES:  # tránh lẫn tệp cũ của lần chụp trước
        (out_dir / name).unlink(missing_ok=True)
    utc, local = timestamps()
    base = {"ma_mau": ma_mau, "vai_tro": vai_tro, "requested_url": url, "final_url": None,
            "http_status": None, "title": None, "captured_at_utc": utc, "captured_at": local,
            "playwright_version": metadata.version("playwright"), "chromium_version": browser.version,
            "viewport": VIEWPORT, "user_agent": None, "expansion_clicks": [],
            "script": SCRIPT, "script_sha256": sha256_file(ROOT / SCRIPT), "git_head": git_head()}
    report = {"hidden": []}
    context = browser.new_context(viewport=VIEWPORT, locale=LOCALE, timezone_id=TIMEZONE,
                                  device_scale_factor=1, extra_http_headers={"Accept-Language": "vi-VN"})
    try:
        if is_pdf_url(url):
            capture_pdf(context, base, report, out_dir, url)
        else:
            capture_html(context, base, report, out_dir, url)
    except Exception as exc:
        base["error"] = f"{type(exc).__name__}: {str(exc).splitlines()[0] if str(exc) else ''}"
    finally:
        context.close()
    meta = build_meta(base, out_dir)
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                       encoding="utf-8", newline="\n")
    return meta, report


def print_report(meta, report, out_dir):
    label = f"{meta['ma_mau']} [{meta['vai_tro']}]"
    if meta.get("error"):
        print(f"LỖI {label}: {meta['error']}")
        return
    where = out_dir.relative_to(ROOT) if out_dir.is_relative_to(ROOT) else out_dir
    if meta.get("loai") == "pdf":
        chars = report.get("pdf_chars", 0)
        print(f"OK {label}: HTTP {meta['http_status']}, PDF {meta['pdf']['pages']} trang, "
              f"{chars} ký tự trích, tai_lieu.pdf {meta['pdf']['bytes']} byte, ghi vào {where}")
        warning = pdf_text_warning(chars)
        if warning:
            print(f"    CẢNH BÁO: {warning}")
        return
    size = meta.get("full_png", {})
    print(f"OK {label}: HTTP {meta['http_status']}, {len(meta['expansion_clicks'])} cú bấm mở rộng, "
          f"full.png {size.get('width')}x{size.get('height')}, ghi vào {where}")
    for text in meta["expansion_clicks"]:
        print(f"    bấm: {text}")
    for item in meta.get("expansion_skipped", []):
        print(f"    bỏ qua: {item['text']} ({item['ly_do']})")
    consent = meta.get("consent", {})
    if consent.get("banner_detected"):
        print(f"    cookie: đã từ chối = {consent['rejected']!r}, "
              f"banner còn hiện = {consent['banner_visible_at_capture']}")
    hidden = report["hidden"]
    print(f"    chú thích ẩn (có trong DOM, không có trong innerText): {len(hidden)}")
    for line in hidden[:5]:
        print("      - " + (line if len(line) <= 160 else line[:157] + "..."))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Chụp trang nguồn chính thức làm bằng chứng.")
    parser.add_argument("ma_mau", nargs="*", help="ma_mau trong data/mau_san_pham.csv")
    parser.add_argument("--tat-ca", action="store_true", help="chụp toàn bộ mẫu trong CSV")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    rows = select_rows(read_samples(), args.ma_mau, args.tat_ca)

    from playwright.sync_api import sync_playwright
    failed = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for row in rows:
                for vai_tro, url, out_dir in targets_for(row):
                    meta, report = capture_target(browser, row["ma_mau"], vai_tro, url, out_dir)
                    print_report(meta, report, out_dir)
                    failed += bool(meta.get("error"))
        finally:
            browser.close()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
