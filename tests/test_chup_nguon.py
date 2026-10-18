import hashlib
import importlib.util
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
