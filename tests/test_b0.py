import hashlib
import importlib.util
import json
from pathlib import Path
import re
import socket

import pytest

from kiemchung import danh_gia as dg, truy_hoi as th
from kiemchung.doi_chung import b0
from kiemchung.llm import LLMClient, LLMError, LLMResult

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chay_b0", ROOT / "scripts/chay_b0.py")
chay_b0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chay_b0)

# Chép riêng từ T12.1, tách ở hai chỗ trống để thử ghép; không dùng b0.CAU_LENH_B0.
T12_1_TRUOC = ('Bạn là người kiểm chứng thông tin. Chỉ dựa vào các đoạn tài liệu chính hãng dưới đây, cho biết tuyên bố '
               'được tài liệu ủng hộ (Supported), bị bác bỏ (Refuted) hay chưa đủ thông tin (NEI). Trả về JSON '
               '{"nhan": …, "doan": […], "ly_do": …}. Tuyên bố: ')
T12_1_GIUA = ". Tài liệu: "
T12_1_SAU = "."

DOAN_A = [
    ("Dung lượng pin lớn", []),
    ("Chống nước IP68 ngoài trời", ["IP68 theo IEC 60529"]),
    ("Chống nước IP68 sâu 6 mét", []),
    ("Kết nối bluetooth ổn định", []),
    ("Màn hình sáng rõ ban ngày", []),
    ("Camera chụp đêm tốt", []),
]
DOAN_B = [("Chống nước IP68 ngoài trời", []), ("Pin rất lớn", []), ("Loa to", []), ("Sạc nhanh", []),
          ("Camera kép", []), ("Màn hình cong", [])]
TUYEN_BO = {"id": "tb-1", "ma_mau": "dt-a", "tuyen_bo": "Máy A chống nước IP68"}
JSON_DUNG = '{"nhan": "Supported", "doan": ["dt-a#002"], "ly_do": "khớp"}'


@pytest.fixture(autouse=True)
def moi_truong_sach(monkeypatch):
    th.xoa_dem()
    for ten in ("GEMINI_API_KEY", "GROQ_API_KEY", "GOOGLE_API_KEY"):
        monkeypatch.delenv(ten, raising=False)

    def chan(*args, **kwargs):
        raise AssertionError("Test không được dùng mạng")
    monkeypatch.setattr(socket.socket, "connect", chan)
    yield
    th.xoa_dem()


def ghi_doan(thu_muc_nguon, ma_mau, doan):
    thu_muc = Path(thu_muc_nguon) / ma_mau
    thu_muc.mkdir(parents=True, exist_ok=True)
    dong = [{"id": f"{ma_mau}#{i:03d}", "ma_mau": ma_mau, "noi_dung": nd, "chu_thich": ct}
            for i, (nd, ct) in enumerate(doan, 1)]
    (thu_muc / "doan.jsonl").write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in dong),
                                        encoding="utf-8")


@pytest.fixture
def nguon(tmp_path):
    thu_muc = tmp_path / "nguon"
    ghi_doan(thu_muc, "dt-a", DOAN_A)
    ghi_doan(thu_muc, "dt-b", DOAN_B)
    return thu_muc


def llm_gia(noi_dung=JSON_DUNG, finish="stop"):
    """Transport giả trả cố định một văn bản; ghi lại các yêu cầu vào .cac_lan."""
    def transport(request, timeout_s):
        transport.cac_lan.append(request)
        return LLMResult(noi_dung, request["provider"], request["model"], "mo-hinh-thuc",
                         {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15}, finish)
    transport.cac_lan = []
    return transport


def client(tmp_path, transport):
    return LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=transport, max_retries=0)


def chay(tmp_path, nguon, transport, mo_hinh="gemini-3.6-flash", k=3):
    return b0.kiem_chung_b0(TUYEN_BO, client(tmp_path, transport), mo_hinh, k=k, thu_muc_nguon=nguon)


# --- Câu lệnh ---

def test_cau_lenh_dung_nguyen_van_t12_1_va_chen_dung_cho():
    doan = [("dt-a#002", "Chống nước IP68"), ("dt-a#005", "Màn hình\nsáng")]
    cau_lenh = b0.ghep_cau_lenh("Máy A chống nước IP68", doan)
    tai_lieu = "[dt-a#002] Chống nước IP68\n\n[dt-a#005] Màn hình\nsáng"
    assert cau_lenh == T12_1_TRUOC + "Máy A chống nước IP68" + T12_1_GIUA + tai_lieu + T12_1_SAU


def test_khung_cau_lenh_trung_ke_hoach():
    ke_hoach = ROOT / "CHI_TIET_TUYEN_TINH_KHOA_LUAN.md"
    if not ke_hoach.exists():
        pytest.skip("không có tệp kế hoạch")
    khop = re.search(r'^\*\*T12\.1 B0 \(ba nhãn\)\.\*\* "(.*)"$', ke_hoach.read_text(encoding="utf-8"), re.M)
    assert khop, "không tìm thấy T12.1 trong kế hoạch"
    assert b0.CAU_LENH_B0 == khop.group(1)
    assert T12_1_TRUOC + "{tuyen_bo}" + T12_1_GIUA + "{doan_1..k}" + T12_1_SAU == khop.group(1)


def test_cho_trong_chi_thay_mot_luot():
    cau_lenh = b0.ghep_cau_lenh("gõ {doan_1..k} vào", [("dt-a#001", "có {tuyen_bo} trong đoạn")])
    assert cau_lenh == (T12_1_TRUOC + "gõ {doan_1..k} vào" + T12_1_GIUA
                        + "[dt-a#001] có {tuyen_bo} trong đoạn" + T12_1_SAU)


def test_cau_lenh_can_it_nhat_mot_doan():
    with pytest.raises(ValueError, match="không có đoạn nào"):
        b0.ghep_cau_lenh("x", [])


def test_lay_doan_theo_hang_bm25_va_van_ban_nhu_van_ban_chi_muc(nguon):
    doan = b0.lay_doan("dt-a", "Chống nước IP68", 2, "am_tiet", nguon)
    assert [ma for ma, _ in doan] == [ma for ma, _ in th.truy_hoi("dt-a", "Chống nước IP68", 2, "am_tiet", nguon)]
    van_ban = dict(th.doc_doan("dt-a", nguon))
    assert all(vb == van_ban[ma] for ma, vb in doan)
    # Đoạn #002 có chú thích: văn bản là noi_dung, xuống dòng, chu_thich.
    assert dict(doan)["dt-a#002"] == "Chống nước IP68 ngoài trời\nIP68 theo IEC 60529"


def test_chi_dua_doan_cua_dung_mau_vao_cau_lenh(tmp_path, nguon):
    transport = llm_gia()
    ban_ghi = chay(tmp_path, nguon, transport, k=3)
    cau_lenh = transport.cac_lan[0]["messages"][0]["content"]
    assert len(ban_ghi["ma_doan"]) == 3 and all(ma.startswith("dt-a#") for ma in ban_ghi["ma_doan"])
    assert "dt-b#" not in cau_lenh and "Pin rất lớn" not in cau_lenh
    assert all(f"[{ma}] " in cau_lenh for ma in ban_ghi["ma_doan"])
    assert cau_lenh == b0.ghep_cau_lenh(TUYEN_BO["tuyen_bo"], b0.lay_doan("dt-a", TUYEN_BO["tuyen_bo"], 3, "am_tiet", nguon))
    # Mẫu khác cùng nguồn thì chỉ thấy đoạn của mẫu đó.
    transport_b = llm_gia()
    b0.kiem_chung_b0({"id": "tb-2", "ma_mau": "dt-b", "tuyen_bo": "Máy B chống nước IP68"},
                     client(tmp_path / "b", transport_b), "gemini-3.6-flash", k=3, thu_muc_nguon=nguon)
    cau_lenh_b = transport_b.cac_lan[0]["messages"][0]["content"]
    assert "dt-a#" not in cau_lenh_b and "[dt-b#001]" in cau_lenh_b


# --- Gọi LLM và bản ghi ---

@pytest.mark.parametrize("mo_hinh, nha_cung_cap", [("gemini-3.6-flash", "gemini"), ("openai/gpt-oss-120b", "groq")])
def test_goi_llm_nhiet_do_0_json_va_dung_nha_cung_cap(tmp_path, nguon, mo_hinh, nha_cung_cap):
    transport = llm_gia()
    ban_ghi = chay(tmp_path, nguon, transport, mo_hinh)
    yeu_cau = transport.cac_lan[0]
    assert (yeu_cau["provider"], yeu_cau["model"]) == (nha_cung_cap, mo_hinh)
    assert yeu_cau["parameters"]["temperature"] == 0
    assert yeu_cau["json_output"] is True and yeu_cau["output_schema"] is None
    assert [m["role"] for m in yeu_cau["messages"]] == ["user"]
    assert (ban_ghi["mo_hinh"], ban_ghi["nha_cung_cap"]) == (mo_hinh, nha_cung_cap)


def test_ban_ghi_du_de_kiem_lai(tmp_path, nguon):
    ban_ghi = chay(tmp_path, nguon, llm_gia(), k=4)
    assert ban_ghi["id"] == "tb-1" and ban_ghi["ma_mau"] == "dt-a" and ban_ghi["tuyen_bo"] == TUYEN_BO["tuyen_bo"]
    assert ban_ghi["mo_hinh_thuc"] == "mo-hinh-thuc"
    assert ban_ghi["k"] == 4 and ban_ghi["cach_tach"] == "am_tiet" and len(ban_ghi["ma_doan"]) == 4
    assert ban_ghi["ma_bam_cau_lenh"] == hashlib.sha256(ban_ghi["cau_lenh"].encode("utf-8")).hexdigest()
    assert ban_ghi["tra_ve_tho"] == JSON_DUNG
    assert (ban_ghi["nhan_goc"], ban_ghi["nhan"], ban_ghi["doan"], ban_ghi["ly_do"], ban_ghi["loi"]) == (
        "Supported", "DUNG", ["dt-a#002"], "khớp", None)
    assert ban_ghi["finish_reason"] == "stop" and ban_ghi["usage"]["total_tokens"] == 15
    assert len(ban_ghi["ma_yeu_cau"]) == 64
    assert (tmp_path / "cache" / f"{ban_ghi['ma_yeu_cau']}.json").exists()
    json.dumps(ban_ghi, ensure_ascii=False)  # ghi được ra JSONL


def test_lan_hai_di_qua_bo_nho_dem(tmp_path, nguon):
    transport = llm_gia()
    lan_1 = chay(tmp_path, nguon, transport)
    lan_2 = chay(tmp_path, nguon, transport)
    assert len(transport.cac_lan) == 1
    assert (lan_1["tu_bo_nho_dem"], lan_2["tu_bo_nho_dem"]) == (False, True)
    assert {**lan_1, "tu_bo_nho_dem": True} == lan_2


def test_mo_hinh_la_bi_tu_choi(tmp_path, nguon):
    transport = llm_gia()
    with pytest.raises(ValueError, match="chưa có nhà cung cấp"):
        chay(tmp_path, nguon, transport, "mo-hinh-la")
    assert transport.cac_lan == []


def test_phan_hoi_cat_cut_thanh_loi_khong_dung_lai(tmp_path, nguon):
    ban_ghi = chay(tmp_path, nguon, llm_gia(finish="length"))
    assert ban_ghi["nhan"] == "LOI" and ban_ghi["tra_ve_tho"] is None and ban_ghi["tu_bo_nho_dem"] is False
    assert ban_ghi["loi"] == "llm_khong_tra_ve_dung: empty_blocked_or_incomplete_response"
    assert ban_ghi["ma_doan"] and ban_ghi["cau_lenh"]  # vẫn đủ để kiểm lại câu lệnh đã gửi


def test_phan_hoi_rong_thanh_loi(tmp_path, nguon):
    assert chay(tmp_path, nguon, llm_gia("  "))["nhan"] == "LOI"


@pytest.mark.parametrize("loi", [LLMError("temporary_api_error", retryable=True, status_code=429),
                                 LLMError("authentication_or_permission_denied", status_code=401),
                                 RuntimeError("mất kết nối")])
def test_loi_mang_quota_khoa_duoc_nem_len(tmp_path, nguon, loi):
    def hong(request, timeout_s):
        raise loi
    with pytest.raises(LLMError):
        chay(tmp_path, nguon, hong)


# --- Đọc phản hồi và ánh xạ nhãn ---

@pytest.mark.parametrize("nhan_goc, mong_doi", [
    ("Supported", "DUNG"), ("Refuted", "SAI"), ("NEI", "CHUA_DU"),
    ("supported", "DUNG"), ("REFUTED", "SAI"), ("nei", "CHUA_DU"), ("Nei", "CHUA_DU"),
    ("  Supported \n", "DUNG"),
])
def test_anh_xa_nhan(nhan_goc, mong_doi):
    kq = b0.doc_tra_ve(json.dumps({"nhan": nhan_goc, "doan": ["a#1", "a#2"], "ly_do": "vì"}))
    assert (kq["nhan"], kq["nhan_goc"], kq["doan"], kq["ly_do"], kq["loi"]) == (mong_doi, nhan_goc, ["a#1", "a#2"], "vì", None)


@pytest.mark.parametrize("van_ban", [
    '```json\n{"nhan": "Refuted", "doan": [], "ly_do": "x"}\n```',
    '```JSON\n{"nhan": "Refuted", "doan": [], "ly_do": "x"}\n```',
    '```\n{"nhan": "Refuted", "doan": [], "ly_do": "x"}\n```',
    'Kết quả:\n```json\n{"nhan": "Refuted", "doan": [], "ly_do": "x"}\n```\nHết.',
    '```json {"nhan": "Refuted", "doan": [], "ly_do": "x"} ```',
    '\n  {"nhan": "Refuted", "doan": [], "ly_do": "x"}  \n',
])
def test_json_trong_khoi_ma_hoac_tran(van_ban):
    kq = b0.doc_tra_ve(van_ban)
    assert (kq["nhan"], kq["loi"]) == ("SAI", None)


@pytest.mark.parametrize("van_ban, ma_loi", [
    ("Tuyên bố đúng.", "json_khong_doc_duoc"),
    ('{"nhan": "Supported", "doan": [}', "json_khong_doc_duoc"),
    ('```json\n{"nhan": "Supported",\n```', "json_khong_doc_duoc"),
    ("", "json_khong_doc_duoc"),
    ('["Supported"]', "json_khong_phai_doi_tuong"),
    ('"Supported"', "json_khong_phai_doi_tuong"),
    ("null", "json_khong_phai_doi_tuong"),
    ('{"doan": [], "ly_do": "x"}', "thieu_nhan"),
    ('{"nhan": null}', "thieu_nhan"),
    ('{"nhan": 1}', "nhan_khong_phai_chuoi"),
    ('{"nhan": ["Supported"]}', "nhan_khong_phai_chuoi"),
])
def test_khong_doc_duoc_thi_loi_khong_doan_nhan(van_ban, ma_loi):
    kq = b0.doc_tra_ve(van_ban)
    assert kq["nhan"] == "LOI" and kq["loi"].split(":")[0] == ma_loi


@pytest.mark.parametrize("nhan_goc", ["Maybe", "Not Enough Info", "Đúng", "DUNG", "LECH", "Supported.", "Supp orted", "", " "])
def test_nhan_la_thi_loi_va_giu_chu_goc(nhan_goc):
    kq = b0.doc_tra_ve(json.dumps({"nhan": nhan_goc, "doan": [], "ly_do": "x"}))
    assert kq["nhan"] == "LOI" and kq["nhan_goc"] == nhan_goc and kq["loi"].startswith("nhan_la")
    assert kq["ly_do"] == "x"  # lý do LLM nêu vẫn được giữ


def test_doan_va_ly_do_khong_dung_kieu_khong_lam_hong_nhan():
    kq = b0.doc_tra_ve('{"nhan": "NEI", "doan": "a#1", "ly_do": {"x": 1}}')
    assert (kq["nhan"], kq["doan"], kq["ly_do"]) == ("CHUA_DU", ["a#1"], '{"x": 1}')
    kq = b0.doc_tra_ve('{"nhan": "NEI"}')
    assert (kq["nhan"], kq["doan"], kq["ly_do"]) == ("CHUA_DU", [], None)


# --- Chỉ số: FAR, Recall nhãn Đúng, bảng nhầm lẫn ---

CHUAN = {"t1": "DUNG", "t2": "DUNG", "t3": "SAI", "t4": "LECH", "t5": "CHUA_DU", "t6": "LECH", "t7": "DUNG"}
DU_DOAN = {"t1": "DUNG", "t2": "LOI", "t3": "DUNG", "t4": "CHUA_DU", "t5": "DUNG", "t6": "LOI", "t7": "SAI"}


def test_far_va_recall_dung_du_lieu_nho():
    # Khác DUNG: t3, t4, t5, t6 (4); bị gán DUNG: t3, t5. DUNG: t1, t2, t7 (3); được gán DUNG: t1.
    assert dg.tinh_far(CHUAN, DU_DOAN) == (2, 4)
    assert dg.tinh_recall_dung(CHUAN, DU_DOAN) == (1, 3)


def test_bang_nham_lan_du_lieu_nho():
    bang = dg.bang_nham_lan(CHUAN, DU_DOAN)
    assert list(bang) == ["DUNG", "SAI", "LECH", "CHUA_DU"]
    assert all(list(hang) == ["DUNG", "SAI", "CHUA_DU", "LOI"] for hang in bang.values())
    assert bang == {
        "DUNG": {"DUNG": 1, "SAI": 1, "CHUA_DU": 0, "LOI": 1},
        "SAI": {"DUNG": 1, "SAI": 0, "CHUA_DU": 0, "LOI": 0},
        "LECH": {"DUNG": 0, "SAI": 0, "CHUA_DU": 1, "LOI": 1},
        "CHUA_DU": {"DUNG": 1, "SAI": 0, "CHUA_DU": 0, "LOI": 0},
    }
    assert sum(sum(hang.values()) for hang in bang.values()) == len(CHUAN)


def test_loi_nam_trong_mau_so_va_duoc_dem_rieng():
    # t6 (LECH, LOI) ở mẫu số FAR nhưng không là chấp nhận nhầm; t2 (DUNG, LOI) ở mẫu số Recall nhưng không trúng.
    assert dg.dem_loi(CHUAN, DU_DOAN) == 2
    all_dung = {ma: "DUNG" for ma in CHUAN}
    assert dg.tinh_far(CHUAN, all_dung) == (4, 4)
    assert dg.tinh_far(CHUAN, {**all_dung, "t6": "LOI"}) == (3, 4)
    assert dg.tinh_recall_dung(CHUAN, {**all_dung, "t2": "LOI"}) == (2, 3)


def test_danh_sach_loai_bo_khoi_moi_phep_tinh():
    assert dg.tinh_far(CHUAN, DU_DOAN, loai=["t5"]) == (1, 3)
    assert dg.tinh_recall_dung(CHUAN, DU_DOAN, loai=["t2"]) == (1, 2)
    assert dg.dem_loi(CHUAN, DU_DOAN, loai=["t2"]) == 1
    bang = dg.bang_nham_lan(CHUAN, DU_DOAN, loai=["t2", "t5"])
    assert bang["DUNG"] == {"DUNG": 1, "SAI": 1, "CHUA_DU": 0, "LOI": 0}
    assert bang["CHUA_DU"] == {"DUNG": 0, "SAI": 0, "CHUA_DU": 0, "LOI": 0}
    assert dg.mau_danh_gia(CHUAN, DU_DOAN, loai=["t2", "t5"]) == ["t1", "t3", "t4", "t6", "t7"]


def test_mau_so_bang_khong():
    chi_dung = {"t1": "DUNG", "t2": "DUNG"}
    assert dg.tinh_far(chi_dung, {"t1": "DUNG", "t2": "SAI"}) == (0, 0)
    khong_dung = {"t1": "SAI", "t2": "LECH"}
    assert dg.tinh_recall_dung(khong_dung, {"t1": "SAI", "t2": "SAI"}) == (0, 0)
    assert dg.tinh_far(CHUAN, DU_DOAN, loai=list(CHUAN)) == (0, 0)


def test_chi_so_kiem_chat_dau_vao():
    with pytest.raises(ValueError, match="không cùng tập mã"):
        dg.tinh_far(CHUAN, {**DU_DOAN, "t8": "DUNG"})
    with pytest.raises(ValueError, match="không cùng tập mã"):
        dg.tinh_far(CHUAN, {k: v for k, v in DU_DOAN.items() if k != "t1"})
    with pytest.raises(ValueError, match="nhãn dự đoán không hợp lệ"):
        dg.tinh_far(CHUAN, {**DU_DOAN, "t1": "LECH"})  # B0 không được ra LECH
    with pytest.raises(ValueError, match="nhãn chuẩn không hợp lệ"):
        dg.tinh_far({**CHUAN, "t1": "LOI"}, DU_DOAN)
    with pytest.raises(ValueError, match="không thuộc bộ thử"):
        dg.tinh_far(CHUAN, DU_DOAN, loai=["t99"])


# --- Báo cáo ---

def bao_cao_nho(gia):
    tuyen_bo = [{"id": f"t{i}", "ma_mau": "dt-a", "tuyen_bo": f"Tuyên bố | số {i}"} for i in range(1, 8)]
    ban_ghi = {"mo-hinh-x": [{"id": ma, "nhan": DU_DOAN[ma], "mo_hinh_thuc": "x-v2",
                              "loi": "nhan_la: 'Maybe'" if DU_DOAN[ma] == "LOI" else None} for ma in CHUAN]}
    thiet_lap = {"k": 5, "cach_tach": "am_tiet", "max_token_ra": 4096}
    return chay_b0.tao_bao_cao(tuyen_bo, CHUAN, ban_ghi, thiet_lap, ["t5"], "lý do thử", gia)


def test_o_ty_le():
    assert chay_b0.o_ty_le(2, 4) == "50,0% (2/4)"
    assert chay_b0.o_ty_le(0, 0) == "0/0"


def test_bao_cao_co_so_lieu_va_khong_nhan_xet():
    dong = bao_cao_nho(gia=False)
    chu = "\n".join(dong)
    assert dong[0] == "Số sơ bộ: nhãn chuẩn là nhãn lượt 1 của Bước 13; mô hình, k và cách tách là lựa chọn tạm, chốt ở Bước 33."
    assert "CHẠY GIẢ" not in chu
    assert "- Bộ thử: 7 tuyên bố (DUNG 3, SAI 1, LECH 2, CHUA_DU 1); mẫu tính chỉ số: 6 tuyên bố (DUNG 3, SAI 1, LECH 2, CHUA_DU 0)." in chu
    assert "| t5 | dt-a | Tuyên bố \\| số 5 | CHUA_DU | lý do thử |" in chu
    # Loại t5: FAR 1/3 (t3), Recall 1/3 (t1 trong t1, t2, t7), LOI 2 trong mẫu tính và 2 cả bộ.
    assert "| mo-hinh-x | x-v2 | 33,3% (1/3) | 33,3% (1/3) | 2 / 2 | 3 | 3 |" in chu
    assert "| DUNG | 1 | 1 | 0 | 1 | 3 |" in chu
    assert "| LECH | 0 | 0 | 1 | 1 | 2 |" in chu
    assert "| CHUA_DU | 0 | 0 | 0 | 0 | 0 |" in chu  # t5 bị loại
    assert "| nhan_la | 2 |" in chu


def test_bao_cao_chay_gia_ghi_ro_la_gia():
    dong = bao_cao_nho(gia=True)
    assert dong[0].startswith("**CHẠY GIẢ (--gia)")
    assert chay_b0.GHI_CHU in dong


@pytest.mark.parametrize("mo_hinh, ten", [("gemini-3.6-flash", "gemini-3.6-flash"),
                                          ("openai/gpt-oss-120b", "openai_gpt-oss-120b")])
def test_ten_tep_an_toan(mo_hinh, ten):
    assert chay_b0.ten_tep(mo_hinh) == ten


# --- Script (chỉ chạy với LLM giả, ghi vào thư mục tạm) ---

def doc_ket_qua(tmp_path, ten):
    duong = tmp_path / "b0_thu_gia" / f"{ten}.jsonl"
    return [json.loads(dong) for dong in duong.read_text(encoding="utf-8").splitlines()]


def dem_goi_gia(monkeypatch, loi_theo_mo_hinh=None):
    """Bọc b0.gia_transport: đếm lượt gọi thật; mô hình trong loi_theo_mo_hinh thì ném LLMError."""
    dem = {"goi": 0}
    goc = b0.gia_transport

    def transport(request, timeout_s):
        dem["goi"] += 1
        if request["model"] in (loi_theo_mo_hinh or {}):
            raise loi_theo_mo_hinh[request["model"]]
        return goc(request, timeout_s)
    monkeypatch.setattr(b0, "gia_transport", transport)
    return dem


def test_script_chay_gia_het_66_tuyen_bo_ca_hai_mo_hinh(tmp_path, monkeypatch, capsys):
    dem = dem_goi_gia(monkeypatch)
    assert chay_b0.main(["--gia", "--thu-muc-ra", str(tmp_path)]) == 0
    tuyen_bo = chay_b0.doc_jsonl(chay_b0.TEP_TUYEN_BO)
    chuan = {nh["id"]: nh["nhan"] for nh in chay_b0.doc_jsonl(chay_b0.TEP_NHAN)}
    assert len(tuyen_bo) == 66
    for mo_hinh, ten in [("gemini-3.6-flash", "gemini-3.6-flash"), ("openai/gpt-oss-120b", "openai_gpt-oss-120b")]:
        ban_ghi = doc_ket_qua(tmp_path, ten)
        assert [r["id"] for r in ban_ghi] == [tb["id"] for tb in tuyen_bo]  # đủ 66, kể cả tb-00009, tb-00010
        assert all(r["mo_hinh"] == mo_hinh and r["k"] == 5 and r["cach_tach"] == "am_tiet" and len(r["ma_doan"]) == 5
                   for r in ban_ghi)
        assert all(ma.startswith(r["ma_mau"] + "#") for r in ban_ghi for ma in r["ma_doan"])
        assert {r["nhan"] for r in ban_ghi} <= set(dg.NHAN_DU_DOAN) and {"DUNG", "SAI", "CHUA_DU", "LOI"} == {r["nhan"] for r in ban_ghi}
    # Tuyên bố trùng chữ và cùng mẫu cho cùng câu lệnh nên chỉ gọi một lần, lần sau lấy từ bộ nhớ đệm.
    assert dem["goi"] == 2 * len({(tb["ma_mau"], tb["tuyen_bo"]) for tb in tuyen_bo})
    # Báo cáo khớp số tính lại từ tệp kết quả.
    bao_cao = (tmp_path / "b0_buoc15_gia.md").read_text(encoding="utf-8")
    du_doan = {r["id"]: r["nhan"] for r in doc_ket_qua(tmp_path, "gemini-3.6-flash")}
    bo = ["tb-00009", "tb-00010"]
    assert f"| gemini-3.6-flash | gia-lap-b0-v1 | {chay_b0.o_ty_le(*dg.tinh_far(chuan, du_doan, bo))} | " \
           f"{chay_b0.o_ty_le(*dg.tinh_recall_dung(chuan, du_doan, bo))} | " in bao_cao
    assert dg.tinh_far(chuan, du_doan, bo)[1] == sum(1 for ma, n in chuan.items() if n != "DUNG" and ma not in bo)
    assert bao_cao.splitlines()[0].startswith("**CHẠY GIẢ") and chay_b0.GHI_CHU in bao_cao
    assert "| tb-00009 |" in bao_cao and "nhãn lượt 1 lưu lệch sang tuyên bố kế bên" in bao_cao
    # Chạy giả không đụng tới thư mục của kết quả thật.
    assert not (tmp_path / "b0_buoc15.md").exists() and not (tmp_path / "b0_thu").exists()
    assert not (tmp_path / "llm_cache").exists()
    assert "CHẠY GIẢ" in capsys.readouterr().out


def test_script_chay_lai_di_qua_bo_nho_dem(tmp_path, monkeypatch):
    dem = dem_goi_gia(monkeypatch)
    args = ["--gia", "--thu-muc-ra", str(tmp_path), "--mo-hinh", "gemini-3.6-flash"]
    assert chay_b0.main(args) == 0
    lan_1 = doc_ket_qua(tmp_path, "gemini-3.6-flash")
    goi_lan_1 = dem["goi"]
    assert 0 < goi_lan_1 <= 66
    assert chay_b0.main(args) == 0
    assert dem["goi"] == goi_lan_1  # lần hai không gọi thêm
    lan_2 = doc_ket_qua(tmp_path, "gemini-3.6-flash")
    assert [{**r, "tu_bo_nho_dem": True} for r in lan_1] == [{**r, "tu_bo_nho_dem": True} for r in lan_2]
    assert all(r["tu_bo_nho_dem"] for r in lan_2)


def test_script_k_va_cach_tach_la_tham_so(tmp_path, monkeypatch):
    dem_goi_gia(monkeypatch)
    assert chay_b0.main(["--gia", "--thu-muc-ra", str(tmp_path), "--mo-hinh", "gemini-3.6-flash",
                         "--k", "3", "--cach-tach", "tu", "--bo", "tb-00001"]) == 0
    ban_ghi = doc_ket_qua(tmp_path, "gemini-3.6-flash")
    assert all(r["k"] == 3 and r["cach_tach"] == "tu" and len(r["ma_doan"]) == 3 for r in ban_ghi)
    bao_cao = (tmp_path / "b0_buoc15_gia.md").read_text(encoding="utf-8")
    assert "top-3, cách tách tu" in bao_cao and "| tb-00001 |" in bao_cao and "| tb-00009 |" not in bao_cao


def test_script_dung_khi_loi_quota_o_mo_hinh_dau(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("kiemchung.llm.time.sleep", lambda giay: None)
    dem_goi_gia(monkeypatch, {"gemini-3.6-flash": LLMError("temporary_api_error", retryable=True, status_code=429)})
    assert chay_b0.main(["--gia", "--thu-muc-ra", str(tmp_path)]) == 1
    loi = capsys.readouterr().err
    assert "DỪNG ở gemini-3.6-flash" in loi and "tb-00001" in loi and "temporary_api_error" in loi
    assert not (tmp_path / "b0_thu_gia" / "gemini-3.6-flash.jsonl").exists()
    assert not (tmp_path / "b0_buoc15_gia.md").exists()


def test_script_dung_khi_loi_o_mo_hinh_sau_giu_mo_hinh_da_xong(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("kiemchung.llm.time.sleep", lambda giay: None)
    dem_goi_gia(monkeypatch, {"openai/gpt-oss-120b": LLMError("authentication_or_permission_denied", status_code=401)})
    assert chay_b0.main(["--gia", "--thu-muc-ra", str(tmp_path)]) == 1
    assert "DỪNG ở openai/gpt-oss-120b" in capsys.readouterr().err
    assert len(doc_ket_qua(tmp_path, "gemini-3.6-flash")) == 66  # mô hình đã xong vẫn giữ
    assert not (tmp_path / "b0_thu_gia" / "openai_gpt-oss-120b.jsonl").exists()
    assert not list((tmp_path / "b0_thu_gia").glob("*.tmp")) and not (tmp_path / "b0_buoc15_gia.md").exists()


def test_script_chay_that_thieu_khoa_thi_dung_khong_ghi_gi(tmp_path, monkeypatch, capsys):
    # Không --gia nhưng đã xóa khóa, chặn nạp .env và chặn mạng: llm.py dừng trước khi gọi, không có lời gọi thật.
    monkeypatch.setattr(chay_b0, "load_dotenv", lambda *args, **kwargs: None)
    assert chay_b0.main(["--thu-muc-ra", str(tmp_path), "--mo-hinh", "gemini-3.6-flash"]) == 1
    assert "missing_api_key:GEMINI_API_KEY" in capsys.readouterr().err
    assert not (tmp_path / "b0_thu").exists() and not (tmp_path / "b0_buoc15.md").exists()


def test_script_tu_choi_mo_hinh_la_va_ma_bo_la(tmp_path, capsys):
    with pytest.raises(SystemExit):
        chay_b0.main(["--gia", "--thu-muc-ra", str(tmp_path), "--mo-hinh", "mo-hinh-la"])
    with pytest.raises(SystemExit):
        chay_b0.main(["--gia", "--thu-muc-ra", str(tmp_path), "--bo", "tb-99999"])
    assert not list(tmp_path.iterdir())
