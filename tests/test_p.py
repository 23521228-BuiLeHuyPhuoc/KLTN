"""Test P đầu-cuối (Bước 28 việc 1, Bước 31; T5.5, T5.9): src/kiemchung/p.py và scripts/chay_p.py.

Đầu vào là bản ghi trích xuất tự dựng (tests/du_lieu/vi_du_huong_dan.json, như test_quyet_dinh.py) hoặc kết quả của LLM giả
(trich_xuat.gia_transport, không phải bằng chứng thực nghiệm). Không gọi LLM thật, không đọc nhãn chuẩn.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

from kiemchung import p as pp
from kiemchung import trich_xuat as tx
from kiemchung.llm import LLMClient
from kiemchung.quyet_dinh import quyet_dinh

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chay_p", ROOT / "scripts/chay_p.py")
chay_p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chay_p)
spec = importlib.util.spec_from_file_location("chay_trich_xuat", ROOT / "scripts/chay_trich_xuat.py")
chay_tx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chay_tx)

VI_DU = json.loads((ROOT / "tests" / "du_lieu" / "vi_du_huong_dan.json").read_text(encoding="utf-8"))
BUDS = "tn-samsung-buds3pro"
MODEL = "gemini-3.6-flash"


def ban_ghi_vi_du(ma, neo_nguon=True, kiem_day_du=True):
    """Bản ghi của ví dụ hướng dẫn, thêm các trường mà trich_xuat ghi (mo_hinh, k, cach_tach, cờ)."""
    r = next(v for v in VI_DU if v["id"] == ma)
    return {**copy.deepcopy(r["ban_ghi"]), "mo_hinh": MODEL, "k": 5, "cach_tach": "am_tiet", "neo_nguon": neo_nguon,
            "kiem_day_du": kiem_day_du}


def cau_hinh_cua(bg):
    return tx.lay_cau_hinh(tx.nhom_cua_mau(bg["ma_mau"]))


def test_kiem_chung_ban_ghi_cung_nhan_voi_quyet_dinh():
    for r in VI_DU:
        bg = ban_ghi_vi_du(r["id"])
        kq = pp.kiem_chung_ban_ghi(copy.deepcopy(bg))
        goc = quyet_dinh(copy.deepcopy(bg), cau_hinh_cua(bg))
        assert (kq["nhan"], kq["dong_d"], kq["loai"], kq["ly_do"]) == (goc["nhan"], goc["dong_d"], goc["loai"], goc["ly_do"]), r["id"]
        assert kq["vet"] == goc["vet"] and kq["ghi_chu"] == goc["ghi_chu"] and kq["he"] == "P"


def test_kiem_chung_ban_ghi_cac_truong():
    bg = ban_ghi_vi_du("V31")
    kq = pp.kiem_chung_ban_ghi(bg)
    assert set(kq) == {"id", "ma_mau", "nhan", "dong_d", "loai", "bang_chung", "trich", "ly_do", "ghi_chu", "tai_lieu_mau_thuan",
                       "vet", "he", "mo_hinh", "k", "cach_tach", "neo_nguon", "kiem_day_du"}
    assert (kq["id"], kq["ma_mau"], kq["mo_hinh"], kq["k"], kq["cach_tach"]) == ("vd-V31", BUDS, MODEL, 5, "am_tiet")
    assert (kq["neo_nguon"], kq["kiem_day_du"]) == (True, True)
    json.dumps(kq, ensure_ascii=False, sort_keys=True)


def test_p_tru_dk_buds3_pro_7_gio_khi_bat_chong_on_ra_dung():
    bg = ban_ghi_vi_du("V31")
    p = pp.kiem_chung_ban_ghi(copy.deepcopy(bg))
    assert (p["nhan"], p["dong_d"], p["he"]) == ("LECH", "D4", "P")
    dk = pp.kiem_chung_ban_ghi(copy.deepcopy(bg), bo_doi_chieu=True)
    assert (dk["nhan"], dk["dong_d"], dk["he"]) == ("DUNG", "D3", "P-DK")


def test_truong_he_cho_ba_ban():
    assert pp.kiem_chung_ban_ghi(ban_ghi_vi_du("V31"))["he"] == "P"
    assert pp.kiem_chung_ban_ghi(ban_ghi_vi_du("V31"), bo_doi_chieu=True)["he"] == "P-DK"
    nn = pp.kiem_chung_ban_ghi(ban_ghi_vi_du("V31", neo_nguon=False, kiem_day_du=False))
    assert nn["he"] == "P-NN" and (nn["neo_nguon"], nn["kiem_day_du"]) == (False, False)


def test_to_hop_co_khong_hop_le():
    with pytest.raises(ValueError):
        pp.kiem_chung_ban_ghi(ban_ghi_vi_du("V31", neo_nguon=False, kiem_day_du=False), bo_doi_chieu=True)
    with pytest.raises(ValueError):
        pp.kiem_chung_ban_ghi(ban_ghi_vi_du("V31", neo_nguon=False, kiem_day_du=True))


def test_kiem_chung_bo_neo_nguon_va_bo_doi_chieu_cung_luc(tmp_path):
    client = LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=tx.gia_transport)
    with pytest.raises(ValueError):
        pp.kiem_chung("Galaxy Buds3 Pro nghe nhạc 7 giờ", BUDS, client, MODEL, bo_doi_chieu=True, bo_neo_nguon=True)
    assert not (tmp_path / "calls.jsonl").exists() or (tmp_path / "calls.jsonl").read_text(encoding="utf-8") == ""


def test_kiem_chung_voi_gia_transport_chay_het(tmp_path):
    client = LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=tx.gia_transport)
    with open(ROOT / "data" / "tuyen_bo" / "thu.jsonl", encoding="utf-8") as f:
        dong = [json.loads(d) for d in f if d.strip()]
    tb = [d for d in dong if d["ma_mau"] == BUDS][:12]
    assert tb
    for ten, kw, he in (("P", {}, "P"), ("P-DK", {"bo_doi_chieu": True}, "P-DK"), ("P-NN", {"bo_neo_nguon": True}, "P-NN")):
        for d in tb:
            kq = pp.kiem_chung(d, BUDS, client, MODEL, **kw)
            assert kq["he"] == he and kq["id"] == d["id"], ten
            assert kq["nhan"] in ("DUNG", "SAI", "LECH", "CHUA_DU") and kq["ly_do"]
            assert (kq["neo_nguon"], kq["kiem_day_du"]) == ((False, False) if he == "P-NN" else (True, True))
            json.dumps(kq, ensure_ascii=False, sort_keys=True)


# --- scripts/chay_p.py ---

def tao_tep_trich_xuat(thu_muc, khong_neo=False):
    """Chạy chay_trich_xuat.py --gia (LLM giả) vào thư mục tạm, trả đường dẫn tệp jsonl."""
    argv = ["--gia", "--thu-muc-ra", str(thu_muc / "tx"), "--ma-mau", BUDS, "--nghi-giay", "0"]
    if khong_neo:
        argv += ["--khong-neo-nguon", "--khong-kiem-day-du"]
    assert chay_tx.main(argv) == 0
    tep = [t for t in (thu_muc / "tx_gia").glob("*.jsonl") if t.name != "llm_calls.jsonl"]
    assert len(tep) == 1
    return tep[0]


def test_script_chay_p_ghi_tep_va_chay_lai_giong_tung_byte(tmp_path, capsys):
    tep = tao_tep_trich_xuat(tmp_path)
    ra = tmp_path / "p"
    argv = ["--trich-xuat", str(tep), "--thu-muc-ra", str(ra)]
    assert chay_p.main(argv) == 0
    jsonl, md = ra / f"P_{tep.stem}.jsonl", ra / f"thong_ke_P_{tep.stem}.md"
    assert jsonl.exists() and md.exists()
    kq = [json.loads(d) for d in jsonl.read_text(encoding="utf-8").splitlines()]
    assert len(kq) == 31 and all(k["he"] == "P" and k["ma_mau"] == BUDS for k in kq)
    tom_tat = md.read_text(encoding="utf-8")
    for muc in ("Số tuyên bố: 31", "Phân bố nhãn", "Phân bố dòng D", "Phân bố loại", "D1a theo nguyên nhân", "luật lan",
                "trích xuất thất bại"):
        assert muc in tom_tat
    truoc = (jsonl.read_bytes(), md.read_bytes())
    assert chay_p.main(argv) == 0
    assert (jsonl.read_bytes(), md.read_bytes()) == truoc


def test_script_chay_p_bo_doi_chieu_ghi_p_dk(tmp_path):
    tep = tao_tep_trich_xuat(tmp_path)
    ra = tmp_path / "p"
    assert chay_p.main(["--trich-xuat", str(tep), "--thu-muc-ra", str(ra), "--bo-doi-chieu"]) == 0
    kq = [json.loads(d) for d in (ra / f"P-DK_{tep.stem}.jsonl").read_text(encoding="utf-8").splitlines()]
    assert kq and all(k["he"] == "P-DK" for k in kq)
    assert (ra / f"thong_ke_P-DK_{tep.stem}.md").exists()


def test_script_chay_p_tep_p_nn_la_p_nn_va_khong_dung_voi_bo_doi_chieu(tmp_path):
    tep = tao_tep_trich_xuat(tmp_path, khong_neo=True)
    ra = tmp_path / "p"
    assert chay_p.main(["--trich-xuat", str(tep), "--thu-muc-ra", str(ra)]) == 0
    kq = [json.loads(d) for d in (ra / f"P-NN_{tep.stem}.jsonl").read_text(encoding="utf-8").splitlines()]
    assert kq and all(k["he"] == "P-NN" for k in kq)
    ra2 = tmp_path / "p2"
    with pytest.raises(SystemExit) as e:
        chay_p.main(["--trich-xuat", str(tep), "--thu-muc-ra", str(ra2), "--bo-doi-chieu"])
    assert e.value.code != 0
    assert not ra2.exists()
