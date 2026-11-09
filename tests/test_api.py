"""Kiểm dịch vụ kiểm chứng (api.py) bằng TestClient và LLM giả (không gọi mạng, chỉ dùng mẫu tập phát triển)."""
import json
from pathlib import Path
import socket

from fastapi.testclient import TestClient
import pytest

from kiemchung import api, p as pp, tach_tuyen_bo as tach, trich_xuat as tx
from kiemchung.llm import LLMClient, LLMError, LLMResult

BUDS = "tn-samsung-buds3pro"
MODEL = "gemini-3.6-flash"
VAN_BAN = ("Galaxy Buds3 Pro nghe nhạc liền 7 tiếng ngay cả khi bật chống ồn. "
           "Hộp sạc kéo dài tổng thời gian nghe lên đến 30 giờ.")
CAU_GOC = "nghe nhạc liền 7 tiếng ngay cả khi bật chống ồn"
MAU_KIEM_TRA = {"dt-oppo-findx8", "dt-samsung-galaxys25ultra", "dt-xiaomi-redminote14proplus5g", "tn-apple-airpodspro3",
                "tn-apple-airpods4", "tn-xiaomi-redmibuds6pro", "dh-samsung-galaxywatch8", "dh-xiaomi-watchs4"}


@pytest.fixture(autouse=True)
def chan_mang(monkeypatch):
    connect = socket.socket.connect

    def chan(self, dia_chi, *args, **kwargs):
        if not (isinstance(dia_chi, tuple) and dia_chi[0] in ("127.0.0.1", "::1", "localhost")):   # vòng lặp asyncio của TestClient tự nối loopback
            raise AssertionError("không được gọi mạng")
        return connect(self, dia_chi, *args, **kwargs)
    monkeypatch.setattr(socket.socket, "connect", chan)


def transport_tach_va_trich(request, timeout_s):
    """Câu lệnh tách thì trả hai tuyên bố tự đặt; còn lại là LLM giả của trích xuất."""
    if request["messages"][-1]["content"].startswith("Tách bài quảng cáo"):
        ds = [{"tuyen_bo": "Galaxy Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn", "cau_goc": CAU_GOC,
               "thuoc_tinh_du_kien": "thoi_luong_pin"},
              {"tuyen_bo": "Galaxy Buds3 Pro nghe nhạc lên đến 30 giờ cùng hộp sạc", "cau_goc": "lên đến 30 giờ",
               "thuoc_tinh_du_kien": "thoi_luong_pin"}]
        return LLMResult(json.dumps(ds, ensure_ascii=False), request["provider"], request["model"], "gia-tach-v1", {}, "stop")
    return tx.gia_transport(request, timeout_s)


def tao_client(thu_muc, transport=transport_tach_va_trich):
    return LLMClient(thu_muc / "cache", thu_muc / "calls.jsonl", transport=transport, max_retries=0)


@pytest.fixture
def may(tmp_path):
    return TestClient(api.tao_app(client=tao_client(tmp_path / "api"), mo_hinh=MODEL))


def test_danh_sach_mau(may):
    r = may.get("/mau-san-pham")
    assert r.status_code == 200
    ds = r.json()
    ma = {m["ma_mau"] for m in ds}
    assert BUDS in ma and "dt-apple-iphone17" in ma
    assert all(set(m) == {"ma_mau", "ten", "nhom", "hang"} for m in ds)
    buds = next(m for m in ds if m["ma_mau"] == BUDS)
    assert buds == {"ma_mau": BUDS, "ten": "Galaxy Buds3 Pro", "nhom": "tai_nghe", "hang": "Samsung"}
    # kho có đủ mẫu thì API liệt kê cả mẫu tập kiểm tra (chỉ liệt kê, test không chạy kiểm chứng trên chúng)
    assert ma >= MAU_KIEM_TRA or not (api.th.THU_MUC_NGUON / "dt-oppo-findx8" / "doan.jsonl").is_file()


def test_danh_sach_mau_bo_mau_khong_co_doan(tmp_path):
    kho = tmp_path / "nguon"
    (kho / BUDS).mkdir(parents=True)
    (kho / BUDS / "doan.jsonl").write_text("", encoding="utf-8")
    r = TestClient(api.tao_app(client=tao_client(tmp_path), thu_muc_nguon=kho)).get("/mau-san-pham")
    assert [m["ma_mau"] for m in r.json()] == [BUDS]


def test_kiem_chung_dung_cau_truc(may):
    r = may.post("/kiem-chung", json={"van_ban": VAN_BAN, "ma_mau": BUDS})
    assert r.status_code == 200
    d = r.json()
    assert set(d) == {"phien_ban_he_thong", "ket_qua", "thoi_gian_ms"}
    assert d["thoi_gian_ms"] >= 0
    pb = d["phien_ban_he_thong"]
    assert "commit=" in pb and f"mo_hinh={MODEL}" in pb and "cau_lenh_trich_xuat=" in pb and "cau_lenh_tach=" in pb
    assert len(d["ket_qua"]) == 2
    for kq in d["ket_qua"]:
        assert set(kq) == {"tuyen_bo", "thuoc_tinh", "nhan", "doan_nguon", "trich", "ly_do"}
        assert kq["thuoc_tinh"] == "thoi_luong_pin"
        assert kq["nhan"] in {"DUNG", "SAI", "LECH", "CHUA_DU"}
        assert all(set(o) == {"ma_doan", "noi_dung"} and o["ma_doan"].startswith(f"{BUDS}#") and o["noi_dung"]
                   for o in kq["doan_nguon"])


def test_kiem_chung_trung_voi_goi_truc_tiep(tmp_path):
    """Điều kiện xong của Bước 34: kết quả API trùng với tach_bai rồi p.kiem_chung cùng client."""
    client = tao_client(tmp_path / "chung")
    r = TestClient(api.tao_app(client=client, mo_hinh=MODEL)).post("/kiem-chung", json={"van_ban": VAN_BAN, "ma_mau": BUDS})
    assert r.status_code == 200

    bai = {"ma_qc": "x", "ma_mau": BUDS, "noi_dung": VAN_BAN}
    ds = tach.tach_bai(client, MODEL, bai)["tuyen_bo"]
    assert ds
    mong_doi = []
    for tb in ds:
        kq = pp.kiem_chung(tb["tuyen_bo"], BUDS, client, MODEL)
        mong_doi.append({"tuyen_bo": tb["tuyen_bo"], "thuoc_tinh": tb["thuoc_tinh_du_kien"], "nhan": kq["nhan"],
                         "doan_nguon": kq["bang_chung"], "trich": kq["trich"], "ly_do": kq["ly_do"]})
    thuc = [{**kq, "doan_nguon": [o["ma_doan"] for o in kq["doan_nguon"]]} for kq in r.json()["ket_qua"]]
    assert thuc == mong_doi


def test_kiem_chung_trung_khi_hai_client_rieng(tmp_path):
    """Hai client, hai bộ nhớ đệm riêng (không dùng chung kết quả đã nhớ): API vẫn trùng gọi trực tiếp."""
    r = TestClient(api.tao_app(client=tao_client(tmp_path / "a"), mo_hinh=MODEL)).post(
        "/kiem-chung", json={"van_ban": VAN_BAN, "ma_mau": BUDS})
    rieng = tao_client(tmp_path / "b")
    ds = tach.tach_bai(rieng, MODEL, {"ma_qc": "x", "ma_mau": BUDS, "noi_dung": VAN_BAN})["tuyen_bo"]
    nhan = [pp.kiem_chung(tb["tuyen_bo"], BUDS, rieng, MODEL)["nhan"] for tb in ds]
    assert [kq["nhan"] for kq in r.json()["ket_qua"]] == nhan


def test_kiem_chung_bai_khong_co_tuyen_bo(tmp_path):
    def rong(request, timeout_s):
        return LLMResult("[]", request["provider"], request["model"], "gia", {}, "stop")
    r = TestClient(api.tao_app(client=tao_client(tmp_path, rong), mo_hinh=MODEL)).post(
        "/kiem-chung", json={"van_ban": "Tai nghe đẹp.", "ma_mau": BUDS})
    assert r.status_code == 200 and r.json()["ket_qua"] == []


@pytest.mark.parametrize("body", [
    {"van_ban": VAN_BAN, "ma_mau": "khong-co-mau-nay"},
    {"van_ban": VAN_BAN, "ma_mau": "../data"},
    {"van_ban": "", "ma_mau": BUDS},
    {"van_ban": "   \n ", "ma_mau": BUDS},
    {"van_ban": "a" * (api.DO_DAI_TOI_DA + 1), "ma_mau": BUDS},
    {"ma_mau": BUDS},
    {"van_ban": VAN_BAN},
])
def test_dau_vao_sai_422(may, body):
    assert may.post("/kiem-chung", json=body).status_code == 422


def test_do_dai_toi_da_van_nhan(may):
    assert may.post("/kiem-chung", json={"van_ban": "a" * api.DO_DAI_TOI_DA, "ma_mau": BUDS}).status_code == 200


@pytest.mark.parametrize("loi", [LLMError("temporary_api_error", retryable=True, status_code=429),
                                 LLMError("missing_api_key:GEMINI_API_KEY"), ConnectionError("https://x?key=SECRET-123")])
def test_loi_llm_503_khong_lo_chi_tiet(tmp_path, loi):
    def hong(request, timeout_s):
        raise loi
    r = TestClient(api.tao_app(client=tao_client(tmp_path, hong), mo_hinh=MODEL)).post(
        "/kiem-chung", json={"van_ban": VAN_BAN, "ma_mau": BUDS})
    assert r.status_code == 503
    assert "SECRET" not in r.text and "https://" not in r.text


def test_loi_llm_o_buoc_trich_xuat_503(tmp_path):
    def hong_o_trich(request, timeout_s):
        if request["messages"][-1]["content"].startswith("Tách bài quảng cáo"):
            return transport_tach_va_trich(request, timeout_s)
        raise LLMError("temporary_api_error", retryable=True, status_code=503)
    r = TestClient(api.tao_app(client=tao_client(tmp_path, hong_o_trich), mo_hinh=MODEL)).post(
        "/kiem-chung", json={"van_ban": VAN_BAN, "ma_mau": BUDS})
    assert r.status_code == 503


def test_dau_ra_tach_khong_dung_503(tmp_path):
    def khong_phai_json(request, timeout_s):
        return LLMResult("không phải json", request["provider"], request["model"], "gia", {}, "stop")
    r = TestClient(api.tao_app(client=tao_client(tmp_path, khong_phai_json), mo_hinh=MODEL)).post(
        "/kiem-chung", json={"van_ban": VAN_BAN, "ma_mau": BUDS})
    assert r.status_code == 503


def test_cau_hinh_sai():
    with pytest.raises(ValueError):
        api.tao_app(mo_hinh="mo-hinh-la")
    with pytest.raises(ValueError):
        api.tao_app(k=0)
    with pytest.raises(ValueError):
        api.tao_app(cach_tach="la")


def test_cau_hinh_tu_bien_moi_truong(monkeypatch, tmp_path):
    monkeypatch.setenv("KIEMCHUNG_K", "3")
    monkeypatch.setenv("KIEMCHUNG_CACH_TACH", "tu")
    monkeypatch.setenv("KIEMCHUNG_CACHE_DIR", str(tmp_path / "dem"))
    monkeypatch.setenv("KIEMCHUNG_NHAT_KY", str(tmp_path / "nk.jsonl"))
    monkeypatch.setattr(api, "load_dotenv", None)
    c = api._tao_client()
    assert c.cache_dir == tmp_path / "dem" and c.log_path == tmp_path / "nk.jsonl"
    assert c.cache_dir != api.GOC / "ket_qua" / "llm_cache"
    r = TestClient(api.tao_app(client=tao_client(tmp_path), mo_hinh=MODEL)).post(
        "/kiem-chung", json={"van_ban": VAN_BAN, "ma_mau": BUDS})
    assert "k=3" in r.json()["phien_ban_he_thong"] and "cach_tach=tu" in r.json()["phien_ban_he_thong"]


def test_bo_nho_dem_mac_dinh_tach_khoi_thuc_nghiem(monkeypatch):
    for ten in ("KIEMCHUNG_CACHE_DIR", "KIEMCHUNG_NHAT_KY"):
        monkeypatch.delenv(ten, raising=False)
    monkeypatch.setattr(api, "load_dotenv", None)
    c = api._tao_client()
    assert c.cache_dir == api.GOC / "ket_qua" / "llm_cache_api"
    assert Path(c.log_path) != api.GOC / "ket_qua" / "llm_calls.jsonl"
