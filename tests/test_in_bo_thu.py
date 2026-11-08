import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("in_bo_thu", ROOT / "scripts/in_bo_thu.py")
ibt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ibt)

MAU_PHAT_TRIEN = ["dh-apple-watchse3", "dt-xiaomi-15t"]


def muc(tep):
    return re.findall(r"^## `(qc-[^`]+)`$", Path(tep).read_text(encoding="utf-8"), flags=re.M)


def test_mac_dinh_ra_dung_byte_doc_bo_thu(tmp_path):
    ra = tmp_path / "doc.md"
    assert ibt.main(["--ra", str(ra), "--csv", str(tmp_path / "nhap.csv")]) == 0
    assert ra.read_bytes() == (ROOT / "data/tuyen_bo/doc_bo_thu.md").read_bytes()
    assert ra.read_text(encoding="utf-8").startswith("# 24 bài của bộ thử (Bước 12)\n")


def test_loc_hai_mau_phat_trien(tmp_path):
    ra = tmp_path / "doc.md"
    assert ibt.main(["--mau", *MAU_PHAT_TRIEN, "--ra", str(ra), "--csv", str(tmp_path / "nhap.csv"),
                     "--tieu-de", "# {so} bài của tập phát triển (Bước 19)"]) == 0
    ma = muc(ra)
    assert len(ma) == 16
    assert sum(m.startswith("qc-dh-apple-watchse3-") for m in ma) == 8
    assert sum(m.startswith("qc-dt-xiaomi-15t-") for m in ma) == 8
    assert ra.read_text(encoding="utf-8").startswith("# 16 bài của tập phát triển (Bước 19)\n")


def test_csv_moi_co_dung_tieu_de(tmp_path):
    csv_ = tmp_path / "nhap.csv"
    ibt.main(["--ra", str(tmp_path / "doc.md"), "--csv", str(csv_)])
    dong_dau = (ROOT / "data/tuyen_bo/thu_nhap.csv").read_bytes().splitlines()[0]
    assert csv_.read_bytes() == dong_dau + b"\n"  # BOM UTF-8 + tiêu đề + LF (tệp thật có thể đã lưu CRLF bằng Excel)
    assert csv_.read_bytes().startswith(b"\xef\xbb\xbfma_qc,cau_goc,tuyen_bo,thuoc_tinh,ghi_chu,can_xem")


def test_ma_mau_khong_co_bai_thoat_khac_0(tmp_path, capsys):
    ra, csv_ = tmp_path / "doc.md", tmp_path / "nhap.csv"
    assert ibt.main(["--mau", "dt-khong-co", "--ra", str(ra), "--csv", str(csv_)]) != 0
    assert not ra.exists() and not csv_.exists()
    assert "dt-khong-co" in capsys.readouterr().err


def test_csv_da_co_khong_bi_ghi_de(tmp_path):
    csv_ = tmp_path / "nhap.csv"
    csv_.write_text("đã có dữ liệu\n", encoding="utf-8")
    assert ibt.main(["--ra", str(tmp_path / "doc.md"), "--csv", str(csv_)]) == 0
    assert csv_.read_text(encoding="utf-8") == "đã có dữ liệu\n"
