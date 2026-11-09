"""goi_json: gọi lại một lần với trần token gấp đôi khi đầu ra bị cắt; tran_token ghi vào bản ghi."""
import socket

import pytest

from kiemchung.doi_chung import chung
from kiemchung.doi_chung.b0 import goi_json
from kiemchung.llm import LLMClient, LLMError, LLMResult

MSG = [{"role": "user", "content": "cau lenh"}]
MODEL = "openai/gpt-oss-120b"


@pytest.fixture(autouse=True)
def chan_mang(monkeypatch):
    def chan(*args, **kwargs):
        raise AssertionError("test không được gọi mạng")
    monkeypatch.setattr(socket.socket, "connect", chan)


class Transport:
    """Trần nhỏ (<= nho) bị cắt (length hoặc 400 json_validate_failed); trần lớn trả JSON đúng."""
    def __init__(self, nho, kieu="length"):
        self.nho, self.kieu, self.tran = nho, kieu, []

    def __call__(self, request, timeout_s):
        tran = request["parameters"]["max_output_tokens"]
        self.tran.append(tran)
        if tran <= self.nho:
            if self.kieu == "400":
                e = Exception("loi")
                e.status_code, e.body = 400, {"error": {"code": "json_validate_failed"}}
                raise e
            return LLMResult('{"nhan', request["provider"], request["model"], "m", {}, "length")
        return LLMResult('{"nhan": "Đúng"}', request["provider"], request["model"], "m", {}, "stop")


def tao(tmp_path, transport):
    return LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=transport)


@pytest.mark.parametrize("kieu", ["length", "400"])
def test_goi_lai_tran_doi_va_dung_cache(tmp_path, kieu):
    t = Transport(100, kieu)
    c = tao(tmp_path, t)
    kq, tran = goi_json(c, "groq", MODEL, MSG, 0, 100)
    assert tran == 200 and kq.text == '{"nhan": "Đúng"}' and t.tran == [100, 200]
    # Chạy lại: bộ nhớ đệm đã có ở trần đôi nên không chạm trần nhỏ.
    t2 = Transport(100, kieu)
    kq2, tran2 = goi_json(tao(tmp_path, t2), "groq", MODEL, MSG, 0, 100)
    assert tran2 == 200 and kq2.cache_hit and t2.tran == []


def test_khong_bi_cat_giu_tran_goc(tmp_path):
    t = Transport(0)
    _, tran = goi_json(tao(tmp_path, t), "groq", MODEL, MSG, 0, 100)
    assert tran == 100 and t.tran == [100]


def test_loi_khac_nem_ngay(tmp_path):
    def transport(request, timeout_s):
        transport.n += 1
        e = Exception("x")
        e.status_code = 401
        raise e
    transport.n = 0
    with pytest.raises(LLMError) as ei:
        goi_json(tao(tmp_path, transport), "groq", MODEL, MSG, 0, 100)
    assert ei.value.code == "authentication_or_permission_denied" and transport.n == 1


def test_lan_hai_van_loi_thi_nem(tmp_path):
    t = Transport(10 ** 9)
    with pytest.raises(LLMError) as ei:
        goi_json(tao(tmp_path, t), "groq", MODEL, MSG, 0, 100)
    assert ei.value.code == "empty_blocked_or_incomplete_response" and t.tran == [100, 200]


def test_chung_goi_ghi_tran_token(tmp_path):
    c = tao(tmp_path, Transport(50))
    kq = chung.goi(c, MODEL, "cau lenh", max_token_ra=50)
    assert kq["tran_token"] == 100 and kq["loi"] is None
    kq = chung.goi(tao(tmp_path / "khac", Transport(10 ** 9)), MODEL, "cau lenh", max_token_ra=50)
    assert kq["tran_token"] is None and kq["loi"] == "llm_khong_tra_ve_dung: empty_blocked_or_incomplete_response"
    assert chung.goi(tao(tmp_path / "ba", Transport(0)), MODEL, "cau lenh", max_token_ra=50)["tran_token"] == 50
