import hashlib
import importlib.util
import io
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chup_nguon", ROOT / "scripts/chup_nguon.py")
chup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chup)

ROWS = [
    {"ma_mau": "a", "url": "https://www.apple.com/vn/x/", "url_bo_sung": ""},
    {"ma_mau": "b", "url": "https://www.mi.com/vn/b/specs/", "url_bo_sung": "https://www.mi.com/vn/b/"},
    {"ma_mau": "c", "url": "https://example.com/c", "url_bo_sung": "  "},
]


def info(**kw):
    base = {"tag": "button", "role": None, "ariaExpanded": None, "type": None, "href": None,
            "disabled": False, "inForm": False, "inArea": False, "inConsent": False,
            "inNav": False, "inExclude": False, "visible": True, "text": "", "key": "k"}
    return base | kw


def test_select_rows_keeps_argument_order_and_dedupes():
    assert [r["ma_mau"] for r in chup.select_rows(ROWS, ["c", "a", "c"])] == ["c", "a"]
    assert chup.select_rows(ROWS, [], tat_ca=True) == ROWS


def test_select_rows_rejects_unknown_or_empty():
    with pytest.raises(ValueError, match="khong-co"):
        chup.select_rows(ROWS, ["a", "khong-co"])
    with pytest.raises(ValueError):
        chup.select_rows(ROWS, [])


def test_targets_put_supplement_in_bo_sung_folder(tmp_path):
    assert chup.targets_for(ROWS[0], tmp_path) == [("url", ROWS[0]["url"], tmp_path / "a")]
    assert chup.targets_for(ROWS[1], tmp_path) == [
        ("url", ROWS[1]["url"], tmp_path / "b"),
        ("url_bo_sung", ROWS[1]["url_bo_sung"], tmp_path / "b" / "bo_sung")]
    assert len(chup.targets_for(ROWS[2], tmp_path)) == 1  # url_bo_sung chỉ có khoảng trắng


def test_real_csv_has_the_two_pilot_samples():
    ids = {r["ma_mau"] for r in chup.read_samples()}
    assert {"dt-apple-iphone17", "tn-samsung-buds3pro"} <= ids


@pytest.mark.parametrize("text", ["Xem thêm", "XEM THÊM thông tin", "Mở rộng", "Chi tiết", "Thông số kỹ thuật",
                                  "Xem tất cả", "Lưu ý", "Chú thích"])
def test_expand_text_matches(text):
    assert chup.EXPAND_TEXT.search(text)


@pytest.mark.parametrize("text", ["Mua ngay", "Đồng ý", "Chấp nhận tất cả", "So sánh", ""])
def test_expand_text_ignores_other_buttons(text):
    assert not chup.EXPAND_TEXT.search(text)


def test_expand_candidate_rules():
    assert chup.is_expand_candidate(info(text="Xem thêm"))
    assert chup.is_expand_candidate(info(tag="div", role="button", text="Chi tiết"))
    # aria-expanded=false chỉ bấm khi nằm trong vùng thông số/chú thích
    assert not chup.is_expand_candidate(info(tag="div", ariaExpanded="false", text="Màn hình"))
    assert chup.is_expand_candidate(info(tag="div", ariaExpanded="false", text="Màn hình", inArea=True))
    assert not chup.is_expand_candidate(info(text="Xem thêm", ariaExpanded="true"))
    assert not chup.is_expand_candidate(info(text="Xem thêm", visible=False))
    assert not chup.is_expand_candidate(info(text="Xem thêm", disabled=True))
    assert not chup.is_expand_candidate(info(text="Xem thêm", inConsent=True))
    assert not chup.is_expand_candidate(info(text="Xem thêm", inNav=True))
    assert chup.is_expand_candidate(info(text="Xem thêm", inNav=True, inArea=True))
    assert not chup.is_expand_candidate(info(text="Chi tiết", inForm=True, type="submit"))
    # đánh giá của người dùng không phải thông số nhà sản xuất
    assert not chup.is_expand_candidate(info(text="Xem thêm", inExclude=True))


def test_never_click_links_that_navigate():
    assert not chup.is_expand_candidate(info(tag="a", role="button", href="/vn/iphone/", text="Xem thêm"))
    assert not chup.is_expand_candidate(info(tag="a", ariaExpanded="false", href="https://x.vn/", text="Chi tiết"))
    assert chup.is_expand_candidate(info(tag="a", role="button", href="#", text="Xem thêm"))
    assert chup.is_expand_candidate(info(tag="a", role="button", href=None, text="Xem thêm"))


def test_only_reject_buttons_in_consent_banner_are_clicked():
    assert chup.is_reject_button(info(text="Từ chối tất cả", inConsent=True))
    assert chup.is_reject_button(info(text="Reject all", inConsent=True))
    assert not chup.is_reject_button(info(text="Đồng ý", inConsent=True))
    assert not chup.is_reject_button(info(text="Chấp nhận tất cả", inConsent=True))
    assert not chup.is_reject_button(info(text="Từ chối", inConsent=False))
    assert not chup.is_reject_button(info(text="Từ chối", inConsent=True, visible=False))


def test_footnote_like_lines():
    for line in ["* Pin có thể thay đổi", "1. Thử nghiệm sạc nhanh", "Kết quả thực tế có thể khác",
                 "Tùy điều kiện sử dụng"]:
        assert chup.is_footnote_like(line)
    for line in ["Màn hình 6,3 inch", "", "   ", "2 camera", "4.7", "7.1.2ch sound", "18.1 x 19.8 x 33.2"]:
        assert not chup.is_footnote_like(line)


def test_hidden_footnotes_reports_only_missing_footnote_lines():
    inner = "Màn hình 6,3 inch\n* Pin dùng thử nghiệm ở 25 độ"
    nodes = ["Màn hình 6,3 inch", "*  Pin dùng thử nghiệm\nở 25 độ",   # có trong innerText (khác khoảng trắng)
             "* Chống nước IP57 theo điều kiện thử nghiệm", "* Chống nước IP57 theo điều kiện thử nghiệm",
             "Ẩn: không phải chú thích", "THỬ NGHIỆM SẠC NHANH"]
    assert chup.hidden_footnotes(nodes, inner) == ["* Chống nước IP57 theo điều kiện thử nghiệm",
                                                   "THỬ NGHIỆM SẠC NHANH"]
    # innerText áp dụng text-transform nên so sánh không phân biệt hoa thường
    assert chup.hidden_footnotes(["THỬ NGHIỆM SẠC NHANH"], "Thử nghiệm sạc nhanh") == []


def test_host_ignores_www_prefix():
    assert chup.host_of("https://www.apple.com/vn/a") == chup.host_of("https://apple.com/vn/b")
    assert chup.host_of("https://support.apple.com/x") != chup.host_of("https://www.apple.com/x")


def test_build_meta_hashes_the_three_data_files(tmp_path):
    (tmp_path / "page.html").write_bytes("<p>é</p>\n".encode())
    (tmp_path / "page.txt").write_bytes(b"abc\n")
    (tmp_path / "meta.json").write_bytes(b"{}")  # không được tính vào files
    meta = chup.build_meta({"ma_mau": "a"}, tmp_path)
    assert meta["ma_mau"] == "a"
    assert list(meta["files"]) == ["page.html", "page.txt"]  # full.png chưa có thì bỏ qua
    assert meta["files"]["page.txt"] == {"sha256": hashlib.sha256(b"abc\n").hexdigest(), "bytes": 4}
    assert meta["files"]["page.html"]["bytes"] == len("<p>é</p>\n".encode())


def test_write_text_uses_lf_and_utf8(tmp_path):
    chup.write_text(tmp_path / "t.txt", "a\r\nb\nđ")
    assert (tmp_path / "t.txt").read_bytes() == "a\nb\nđ".encode()


def test_timestamps_use_vietnam_offset():
    from datetime import datetime, timezone
    utc, local = chup.timestamps(datetime(2026, 10, 15, 17, 30, 0, tzinfo=timezone.utc))
    assert utc == "2026-10-15T17:30:00+00:00"
    assert local == "2026-10-16T00:30:00+07:00"


def test_png_size_reads_ihdr():
    import struct
    ihdr = struct.pack(">IIBBBBB", 1440, 7321, 8, 6, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + ihdr + b"\0\0\0\0"
    assert chup.png_size(data) == (1440, 7321)


def fake_png(height):
    import struct
    ihdr = struct.pack(">IIBBBBB", 1440, height, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + ihdr + b"\0\0\0\0"


class FakePage:
    def __init__(self, *results):
        self.results, self.timeouts = list(results), []

    def screenshot(self, **kwargs):
        self.timeouts.append(kwargs["timeout"])
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


def test_full_page_png_single_attempt_has_no_note():
    page = FakePage(fake_png(5000))
    data, note = chup.full_page_png(page, 5000)
    assert chup.png_size(data) == (1440, 5000) and note is None
    assert page.timeouts == [chup.SHOT_TIMEOUTS_MS[0]]


def test_full_page_png_retries_after_timeout_and_notes_it():
    page = FakePage(chup.PlaywrightTimeout("hết giờ"), fake_png(5000))
    data, note = chup.full_page_png(page, 5000)
    assert chup.png_size(data) == (1440, 5000)
    assert page.timeouts == list(chup.SHOT_TIMEOUTS_MS)
    assert "chụp lại" in note


def test_full_page_png_raises_when_every_attempt_times_out():
    page = FakePage(*[chup.PlaywrightTimeout("hết giờ")] * len(chup.SHOT_TIMEOUTS_MS))
    with pytest.raises(chup.PlaywrightTimeout):
        chup.full_page_png(page, 5000)


def test_full_page_png_notes_height_mismatch():
    _, note = chup.full_page_png(FakePage(fake_png(3000)), 5000)
    assert "3000" in note and "5000" in note


def make_pdf(pages):
    """PDF tối giản (font Helvetica, chữ ASCII), mỗi phần tử của pages là chữ của một trang."""
    n = len(pages)
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [" + b" ".join(b"%d 0 R" % (4 + 2 * i) for i in range(n)) +
            b"] /Count %d >>" % n,
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    for i, text in enumerate(pages):
        stream = b"BT /F1 12 Tf 72 720 Td (" + text.encode("ascii") + b") Tj ET"
        objs.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                    b"/Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R >>" % (5 + 2 * i))
        objs.append(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream")
    out, offsets = bytearray(b"%PDF-1.4\n"), []
    for num, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % num + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    return bytes(out)


@pytest.mark.parametrize("url", [
    "https://downloadcenter.samsung.com/content/UM/202507/x/SM-L32X_UG.pdf",
    "https://example.com/a/B.PDF",
    "https://example.com/a.Pdf?download=1#page=2"])
def test_is_pdf_url_true(url):
    assert chup.is_pdf_url(url)


@pytest.mark.parametrize("url", [
    "https://www.samsung.com/vn/watches/galaxy-watch/galaxy-watch8-40mm-black-bluetooth-sm-l500nzkaxxv/",
    "https://example.com/pdf/",
    "https://example.com/doc?file=a.pdf",
    "https://example.com/a.pdf/view",
    "https://example.com/a.pdfx"])
def test_is_pdf_url_false(url):
    assert not chup.is_pdf_url(url)


def test_extract_pdf_text_marks_each_page():
    text, pages = chup.extract_pdf_text(make_pdf(["Hello alpha", "Second page beta"]))
    assert pages == 2
    assert text.startswith("=== Trang 1 ===\n")
    assert "Hello alpha" in text and "Second page beta" in text
    assert text.index("=== Trang 2 ===") < text.index("Second page beta")
    assert text.index("Hello alpha") < text.index("=== Trang 2 ===")


def test_extract_pdf_text_blank_page_has_header_only():
    from pypdf import PdfWriter
    buf = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.write(buf)
    text, pages = chup.extract_pdf_text(buf.getvalue())
    assert pages == 1
    assert text.strip() == "=== Trang 1 ==="
    assert chup.pdf_text_chars(text) == 0


def test_pdf_text_chars_ignores_page_headers():
    assert chup.pdf_text_chars("=== Trang 1 ===\nabc\n\n=== Trang 2 ===\n\n") == 3


def test_pdf_text_warning_thresholds():
    assert "rỗng" in chup.pdf_text_warning(0)
    assert "199" in chup.pdf_text_warning(199)
    assert chup.pdf_text_warning(200) is None


def test_check_pdf_response():
    chup.check_pdf_response(200, b"%PDF-1.7 ...")
    with pytest.raises(RuntimeError, match="HTTP 404"):
        chup.check_pdf_response(404, b"%PDF-1.7")
    with pytest.raises(RuntimeError, match="%PDF"):
        chup.check_pdf_response(200, b"<html>Access denied</html>")


def test_pdf_meta_fields_and_build_meta_hash_the_pdf(tmp_path):
    data = make_pdf(["Hello"])
    text, pages = chup.extract_pdf_text(data)
    (tmp_path / "tai_lieu.pdf").write_bytes(data)
    chup.write_text(tmp_path / "page.txt", text)
    base = {"ma_mau": "a"} | chup.pdf_meta_fields(pages, "application/pdf", len(data))
    meta = chup.build_meta(base, tmp_path)
    assert meta["loai"] == "pdf"
    assert meta["pdf"] == {"pages": 1, "content_type": "application/pdf", "bytes": len(data)}
    assert list(meta["files"]) == ["tai_lieu.pdf", "page.txt"]  # không có page.html, full.png
    assert meta["files"]["tai_lieu.pdf"] == {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    assert meta["files"]["page.txt"]["sha256"] == chup.sha256_file(tmp_path / "page.txt")


def test_html_meta_keeps_old_format(tmp_path):
    (tmp_path / "page.html").write_bytes(b"<p>x</p>")
    meta = chup.build_meta({"ma_mau": "a"}, tmp_path)
    assert "loai" not in meta and "pdf" not in meta
    assert list(meta["files"]) == ["page.html"]


def test_pdf_file_is_cleaned_before_each_capture():
    assert "tai_lieu.pdf" in chup.PAGE_FILES
    assert "tai_lieu.pdf" in chup.HASHED_FILES


class FakeResponse:
    def __init__(self, body, status=200, url="https://example.com/a.pdf"):
        self._body, self.status, self.url = body, status, url
        self.headers = {"content-type": "application/pdf"}

    def body(self):
        return self._body


class FakeContext:
    def __init__(self, response):
        self.request, self._response, self.calls = self, response, []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self._response


def pdf_base():
    return {"ma_mau": "a", "vai_tro": "url_bo_sung", "requested_url": "https://example.com/a.pdf",
            "final_url": None, "http_status": None, "title": None, "viewport": {}, "user_agent": None,
            "expansion_clicks": []}


def test_capture_pdf_writes_exact_bytes_and_text(tmp_path):
    data = make_pdf(["Hello alpha"])
    ctx, base, report = FakeContext(FakeResponse(data)), pdf_base(), {"hidden": []}
    chup.capture_pdf(ctx, base, report, tmp_path, "https://example.com/a.pdf")
    assert ctx.calls[0][1]["headers"] == {"Accept-Language": "vi-VN"}
    assert (tmp_path / "tai_lieu.pdf").read_bytes() == data
    assert "Hello alpha" in (tmp_path / "page.txt").read_text(encoding="utf-8")
    assert not (tmp_path / "page.html").exists() and not (tmp_path / "full.png").exists()
    assert base["loai"] == "pdf" and base["pdf"]["pages"] == 1 and base["http_status"] == 200
    assert not {"title", "viewport", "user_agent", "expansion_clicks"} & set(base)
    assert report["pdf_chars"] == len("Hello alpha")


@pytest.mark.parametrize("response", [FakeResponse(b"%PDF-1.4", status=403),
                                      FakeResponse(b"<html>blocked</html>")])
def test_capture_pdf_rejects_bad_response(tmp_path, response):
    with pytest.raises(RuntimeError):
        chup.capture_pdf(FakeContext(response), pdf_base(), {"hidden": []}, tmp_path, "https://example.com/a.pdf")
    assert not (tmp_path / "tai_lieu.pdf").exists()
