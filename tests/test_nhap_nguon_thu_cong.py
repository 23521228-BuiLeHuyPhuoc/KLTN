import hashlib
import importlib.util
import json
import struct
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("nhap_nguon_thu_cong", ROOT / "scripts/nhap_nguon_thu_cong.py")
nhap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nhap)

INFO_PATH = ROOT / "data/nguon/thu_cong_20261020.json"

ROWS = [
    {"ma_mau": "a", "url": "https://www.mi.com/vn/a/specs/", "url_bo_sung": "https://www.mi.com/vn/a/"},
    {"ma_mau": "b", "url": "https://www.mi.com/vn/b/specs/", "url_bo_sung": " "},
]
THONG_TIN = {
    "ghi_chu": "Lưu từ Chrome thật.",
    "trinh_duyet": {"user_agent": "UA/1.0", "viewport": {"width": 1536, "height": 742}},
}
PAGE = {"ma_mau": "a", "vai_tro": "url", "url": "https://www.mi.com/vn/a/specs/", "http_status": 200,
        "title": "Xiaomi A – Trang chính thức", "captured_at_utc": "2026-10-20T08:35:07+00:00",
        "page_scroll_height": 12633}


def fake_png(width=1536, height=5000):
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + ihdr + b"\0\0\0\0"


def test_source_names_map_role_to_downloaded_file_names():
    assert nhap.source_names("dt-x", "url") == {"page.html": "dt-x__url__page.html",
                                                "page.txt": "dt-x__url__page.txt"}
    assert nhap.source_names("dt-x", "url_bo_sung") == {"page.html": "dt-x__bo_sung__page.html",
                                                        "page.txt": "dt-x__bo_sung__page.txt"}
    with pytest.raises(ValueError, match="vai_tro"):
        nhap.source_names("dt-x", "khac")


def test_resolve_target_maps_role_to_folder(tmp_path):
    assert nhap.resolve_target(PAGE, ROWS, tmp_path) == tmp_path / "a"
    sup = PAGE | {"vai_tro": "url_bo_sung", "url": "https://www.mi.com/vn/a/"}
    assert nhap.resolve_target(sup, ROWS, tmp_path) == tmp_path / "a" / "bo_sung"


def test_resolve_target_rejects_url_that_differs_from_csv(tmp_path):
    with pytest.raises(ValueError, match="khác CSV"):
        nhap.resolve_target(PAGE | {"url": "https://www.mi.com/vn/a/specs"}, ROWS, tmp_path)  # thiếu dấu /
    with pytest.raises(ValueError, match="khác CSV"):
        nhap.resolve_target(PAGE | {"vai_tro": "url_bo_sung"}, ROWS, tmp_path)  # url chính gắn nhầm vai trò


def test_resolve_target_rejects_unknown_sample_or_missing_supplement(tmp_path):
    with pytest.raises(ValueError, match="không có trong CSV"):
        nhap.resolve_target(PAGE | {"ma_mau": "z"}, ROWS, tmp_path)
    with pytest.raises(ValueError, match="không có url_bo_sung"):
        nhap.resolve_target(PAGE | {"ma_mau": "b", "vai_tro": "url_bo_sung", "url": "x"}, ROWS, tmp_path)


@pytest.mark.skipif(not INFO_PATH.exists(), reason="chưa có tệp thông tin thủ công")
def test_real_info_file_urls_match_real_csv(tmp_path):
    info = json.loads(INFO_PATH.read_text(encoding="utf-8"))
    rows = nhap.chup.read_samples()
    assert len(info["trang"]) == 8
    for page in info["trang"]:
        nhap.resolve_target(page, rows, tmp_path)  # ném lỗi nếu url khác CSV


def make_sources(src, ma_mau="a", tag="url"):
    html = b"\xef\xbb\xbf<!DOCTYPE html>\r\n<p>Th\xc3\xb4ng s\xe1\xbb\x91</p>\r\n\xff\xfe\r\n"  # BOM, CRLF, byte lỗi UTF-8
    txt = "Màn hình\r\n6,7 inch\r\n".encode()
    (src / f"{ma_mau}__{tag}__page.html").write_bytes(html)
    (src / f"{ma_mau}__{tag}__page.txt").write_bytes(txt)
    return html, txt


def test_copy_page_files_copies_exact_bytes_and_removes_stale(tmp_path):
    src, out = tmp_path / "tai_ve", tmp_path / "nguon" / "a"
    src.mkdir()
    out.mkdir(parents=True)
    html, txt = make_sources(src)
    (out / "full.png").write_bytes(b"cu")
    (out / "meta.json").write_bytes(b'{"error": "HTTP 403"}')
    (out / "page.html").write_bytes(b"cu")
    nhap.copy_page_files(src, out, "a", "url")
    assert (out / "page.html").read_bytes() == html
    assert (out / "page.txt").read_bytes() == txt
    assert not (out / "full.png").exists() and not (out / "meta.json").exists()
    assert (src / "a__url__page.html").read_bytes() == html  # tệp nguồn còn nguyên


def test_copy_page_files_supplement_leaves_main_folder_alone(tmp_path):
    src, main = tmp_path / "tai_ve", tmp_path / "a"
    src.mkdir()
    (main / "bo_sung").mkdir(parents=True)
    (main / "meta.json").write_bytes(b"chinh")
    (main / "bo_sung" / "meta.json").write_bytes(b"cu")
    html, txt = make_sources(src, tag="bo_sung")
    nhap.copy_page_files(src, main / "bo_sung", "a", "url_bo_sung")
    assert (main / "bo_sung" / "page.html").read_bytes() == html
    assert not (main / "bo_sung" / "meta.json").exists()
    assert (main / "meta.json").read_bytes() == b"chinh" and not (main / "page.html").exists()


def test_copy_page_files_missing_source_raises_and_keeps_old_files(tmp_path):
    src, out = tmp_path / "tai_ve", tmp_path / "a"
    src.mkdir()
    out.mkdir()
    (src / "a__url__page.html").write_bytes(b"<p>x</p>")  # thiếu page.txt
    (out / "meta.json").write_bytes(b'{"error": "HTTP 403"}')
    with pytest.raises(FileNotFoundError, match="a__url__page.txt"):
        nhap.copy_page_files(src, out, "a", "url")
    assert (out / "meta.json").read_bytes() == b'{"error": "HTTP 403"}'
    assert not (out / "page.html").exists()


def test_host_counts_groups_by_host_most_frequent_first():
    urls = ["https://i01.appmifile.com/a.png", "https://www.mi.com/x.css", "https://i01.appmifile.com/b.png",
            "https://i01.appmifile.com/c.png", "data:image/png;base64,AAAA"]
    counts = nhap.host_counts(urls)
    assert counts == {"i01.appmifile.com": 3, "www.mi.com": 1, "(không rõ)": 1}
    assert list(counts)[0] == "i01.appmifile.com"
    assert nhap.host_counts([]) == {}


def test_base_meta_takes_fields_from_info_and_derives_vietnam_time():
    meta = nhap.base_meta(PAGE, THONG_TIN)
    assert list(meta) == ["ma_mau", "vai_tro", "requested_url", "final_url", "http_status", "title",
                          "captured_at_utc", "captured_at", "phuong_phap", "ghi_chu_phuong_phap",
                          "user_agent", "viewport", "page_scroll_height"]
    assert meta["requested_url"] == meta["final_url"] == PAGE["url"]
    assert meta["captured_at_utc"] == "2026-10-20T08:35:07+00:00"
    assert meta["captured_at"] == "2026-10-20T15:35:07+07:00"
    assert meta["phuong_phap"] == "thu_cong_chrome"
    assert meta["ghi_chu_phuong_phap"] == "Lưu từ Chrome thật."
    assert meta["user_agent"] == "UA/1.0" and meta["viewport"] == {"width": 1536, "height": 742}
    assert meta["page_scroll_height"] == 12633 and meta["http_status"] == 200


def test_base_meta_normalises_other_offsets_to_utc_and_rejects_naive_time():
    meta = nhap.base_meta(PAGE | {"captured_at_utc": "2026-10-20T15:35:07+07:00"}, THONG_TIN)
    assert meta["captured_at_utc"] == "2026-10-20T08:35:07+00:00"
    assert meta["captured_at"] == "2026-10-20T15:35:07+07:00"
    with pytest.raises(ValueError, match="múi giờ"):
        nhap.base_meta(PAGE | {"captured_at_utc": "2026-10-20T08:35:07"}, THONG_TIN)


def test_full_png_meta_states_how_the_image_was_made():
    meta = nhap.full_png_meta(fake_png(1536, 7321), "2026-10-20T09:00:00+00:00", {"cdn.example": 2}, True)
    assert meta["width"] == 1536 and meta["height"] == 7321
    assert "Dựng lại từ page.html" in meta["cach_tao"] and "tắt JavaScript" in meta["cach_tao"]
    assert "không phải ảnh chụp trực tiếp" in meta["cach_tao"]
    assert meta["dung_luc_utc"] == "2026-10-20T09:00:00+00:00"
    assert meta["tai_nguyen_loi"] == {"cdn.example": 2} and meta["networkidle"] is True
    assert "ghi_chu" not in meta
    assert nhap.full_png_meta(fake_png(), "t", {}, False, "ghi chú")["ghi_chu"] == "ghi chú"


def test_meta_file_style_and_hashes_of_copied_files(tmp_path):
    src, out = tmp_path / "tai_ve", tmp_path / "a"
    src.mkdir()
    html, txt = make_sources(src)
    nhap.copy_page_files(src, out, "a", "url")
    png = fake_png()
    (out / "full.png").write_bytes(png)
    meta = nhap.base_meta(PAGE, THONG_TIN) | {"full_png": nhap.full_png_meta(png, "t", {}, True)}
    meta = nhap.chup.build_meta(meta, out)
    nhap.write_meta(out, meta)
    raw = (out / "meta.json").read_bytes()
    assert raw.endswith(b"\n") and b"\r" not in raw
    assert "Xiaomi A – Trang chính thức".encode() in raw  # ensure_ascii=False
    assert raw.decode().startswith('{\n  "ma_mau": "a"')  # indent=2
    loaded = json.loads(raw)
    assert list(loaded["files"]) == ["page.html", "page.txt", "full.png"]
    assert loaded["files"]["page.html"] == {"sha256": hashlib.sha256(html).hexdigest(), "bytes": len(html)}
    assert loaded["files"]["page.txt"] == {"sha256": hashlib.sha256(txt).hexdigest(), "bytes": len(txt)}
    assert loaded["files"]["full.png"]["sha256"] == hashlib.sha256(png).hexdigest()


# --- render_full_png với trình duyệt giả (không mạng) ---

URL = "https://www.mi.com/vn/a/specs/"
VIEWPORT = {"width": 1536, "height": 742}


class FakeRoute:
    def __init__(self, page):
        self.page = page

    def fulfill(self, **kwargs):
        self.page.fulfilled = kwargs


class FakeResponse:
    def __init__(self, url, status):
        self.url, self.status = url, status


class FakeRequest:
    def __init__(self, url):
        self.url = url


class FakePage:
    def __init__(self, idle_timeout=False, shot_error=None):
        self.handlers, self.matcher, self.route_handler = {}, None, None
        self.fulfilled, self.goto_args = None, None
        self.idle_timeout, self.shot_error, self.png = idle_timeout, shot_error, fake_png()

    def on(self, event, handler):
        self.handlers[event] = handler

    def route(self, matcher, handler):
        self.matcher, self.route_handler = matcher, handler

    def goto(self, url, **kwargs):
        self.goto_args = (url, kwargs)
        # trình duyệt thật gọi handler route cho đúng URL gốc, rồi sinh request phụ
        assert self.matcher(url) and not self.matcher(url + "x") and not self.matcher("https://cdn.example/a.css")
        self.route_handler(FakeRoute(self))
        self.handlers["requestfailed"](FakeRequest("https://cdn.example/a.css"))
        self.handlers["response"](FakeResponse("https://cdn.example/b.png", 404))
        self.handlers["response"](FakeResponse("https://cdn.example/ok.png", 200))
        self.handlers["response"](FakeResponse("https://img.example/c.png", 403))

    def wait_for_load_state(self, state, timeout):
        assert state == "networkidle"
        if self.idle_timeout:
            raise nhap.chup.PlaywrightTimeout("hết giờ")

    def screenshot(self, **kwargs):
        if self.shot_error:
            raise self.shot_error
        return self.png


class FakeContext:
    def __init__(self, page):
        self.page, self.closed = page, False

    def new_page(self):
        return self.page

    def close(self):
        self.closed = True


class FakeBrowser:
    def __init__(self, page):
        self.page, self.context, self.context_kwargs = page, None, None

    def new_context(self, **kwargs):
        self.context_kwargs = kwargs
        self.context = FakeContext(self.page)
        return self.context


def test_render_full_png_serves_saved_html_for_original_url_only():
    page = FakePage()
    browser = FakeBrowser(page)
    html = b"\xef\xbb\xbf<p>x</p>\r\n"
    png, note, errors, idle = nhap.render_full_png(browser, URL, html, VIEWPORT, 5000)
    assert browser.context_kwargs == {"viewport": VIEWPORT, "locale": "vi-VN", "java_script_enabled": False,
                                      "device_scale_factor": 1}  # không đặt user_agent
    assert page.fulfilled == {"status": 200, "body": html, "content_type": "text/html; charset=utf-8"}
    assert page.goto_args[0] == URL
    assert png == page.png and note is None and idle is True
    assert errors == {"cdn.example": 2, "img.example": 1}  # request lỗi + HTTP >= 400; HTTP 200 không tính
    assert browser.context.closed


def test_render_full_png_still_shoots_when_networkidle_times_out():
    _, _, errors, idle = nhap.render_full_png(FakeBrowser(FakePage(idle_timeout=True)), URL, b"<p>", VIEWPORT, 5000)
    assert idle is False and errors["cdn.example"] == 2


def test_render_full_png_closes_context_when_screenshot_fails():
    browser = FakeBrowser(FakePage(shot_error=nhap.chup.PlaywrightTimeout("hết giờ")))
    with pytest.raises(nhap.chup.PlaywrightTimeout):
        nhap.render_full_png(browser, URL, b"<p>", VIEWPORT, 5000)
    assert browser.context.closed