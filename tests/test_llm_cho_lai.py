"""Thời gian chờ trước lần thử lại của llm.py (rà soát Bước 16, 02/11/2026): lỗi 429 chờ lâu, lỗi khác giữ như cũ."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kiemchung import llm  # noqa: E402


class _Loi(Exception):
    def __init__(self, status, headers=None):
        self.status_code = status
        self.response = type("R", (), {"headers": headers or {}})()


def test_429_khong_retry_after_cho_20_roi_40_giay():
    loi = llm._safe_error(_Loi(429))
    assert loi.retryable and loi.status_code == 429 and loi.retry_after is None
    assert [llm.retry_delay(loi, a) for a in (1, 2, 3, 4)] == [20, 40, 80, 120]


def test_429_ton_trong_retry_after_co_tran():
    assert llm.retry_delay(llm._safe_error(_Loi(429, {"retry-after": "7"})), 1) == 7.0
    assert llm.retry_delay(llm._safe_error(_Loi(429, {"retry-after": "999"})), 1) == llm.RETRY_WAIT_CAP_S
    assert llm._safe_error(_Loi(429, {"retry-after": "Wed, 21 Oct 2026"})).retry_after is None  # dạng ngày: bỏ qua


def test_loi_tam_thoi_khac_giu_cach_cho_ngan():
    loi = llm._safe_error(_Loi(503))
    assert loi.retryable and [llm.retry_delay(loi, a) for a in (1, 2, 3, 4)] == [1, 2, 4, 4]


def test_vong_thu_lai_dung_thoi_gian_cho_moi(tmp_path, monkeypatch):
    cho = []
    monkeypatch.setattr(llm.time, "sleep", lambda s: cho.append(s))

    def transport(request, timeout_s):
        raise _Loi(429)

    client = llm.LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", max_retries=2, transport=transport)
    try:
        client.call("groq", "openai/gpt-oss-120b", [{"role": "user", "content": "x"}], {"temperature": 0})
    except llm.LLMError as e:
        assert e.code == "temporary_api_error" and e.status_code == 429
    assert cho == [20, 40]
