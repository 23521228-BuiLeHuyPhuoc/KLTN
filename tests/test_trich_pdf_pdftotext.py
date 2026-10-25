import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("trich_pdf_pdftotext", ROOT / "scripts/trich_pdf_pdftotext.py")
trich = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trich)


def test_tach_trang_bo_trang_rong_sau_dau_ngat_cuoi():
    assert trich.tach_trang("Trang một\r\n\fTrang hai\n\f") == ["Trang một\n", "Trang hai\n"]
    assert trich.tach_trang("A\f\fC") == ["A", "", "C"]  # trang trắng giữa tài liệu vẫn được đếm


def test_dinh_dang_giong_nhanh_pdf_cua_chup_nguon():
    assert trich.dinh_dang(["  dây đeo \n", "100–150 BPM"]) == (
        "=== Trang 1 ===\ndây đeo\n\n=== Trang 2 ===\n100–150 BPM\n")


def test_phien_ban_doc_tu_dau_ra_v():
    assert trich.phien_ban("pdftotext version 4.00\nCopyright 1996-2017 Glyph & Cog, LLC") == "4.00"
    assert trich.phien_ban("lỗi") is None
