"""Bước 16: sinh phụ lục "Cụm diễn đạt trong cấu hình" (mục 13 của data/huong_dan_gan_nhan.md) từ data/cau_hinh/*.yaml.

Mục 13 là phần sinh tự động của hướng dẫn, từ tiêu đề "## 13. ..." tới hết tệp (hoặc tới tiêu đề "## " kế tiếp). Không gõ tay:
sửa YAML rồi chạy lại. Các mục khác của hướng dẫn giữ nguyên từng byte.

Nội dung sinh ra:
- lời dẫn đầu mục (cách dùng phụ lục, hằng LOI_DAN_DAU; ngày lấy từ khóa "ngay" của chung.yaml);
- 13.1 Dùng chung: bảng các nhóm cụm của chung.yaml (kieu_gia_tri, tu_goi_muc_cao, cum_quan_he, ngu_canh_khong_quyet_dinh), rồi
  từ khẳng định (tu_khang_dinh: tu, tu_muc_san, bo_qua_khi_co) và cụm phủ nhiều giá trị (cum_phu.mau);
- 13.2, 13.3, 13.4: bảng cach_dien_dat của dien_thoai.yaml, tai_nghe.yaml, dong_ho.yaml (điều kiện, giá trị, tu_tai_lieu,
  hieu_biet_chung); giá trị có khóa phia ghi thêm "(chỉ phía tài liệu)" hoặc "(chỉ phía tuyên bố)"; bảng cách gọi độ sáng theo
  hãng của điện thoại.

scripts/tao_cong_cu_gan_nhan.py (bang_cum) đọc lại các bảng này cho khung "Cụm điều kiện đã biết" của trang gán nhãn, nên tiêu đề
cột và mã trong dấu backtick giữ nguyên dạng; tests/test_sinh_phu_luc_cum.py kiểm mục 13 của hướng dẫn khớp đầu ra của script.

Chạy:
    .venv/Scripts/python.exe scripts/sinh_phu_luc_cum.py          # kiểm: mục 13 của hướng dẫn khớp YAML (mã thoát 1 nếu lệch)
    .venv/Scripts/python.exe scripts/sinh_phu_luc_cum.py --ghi    # ghi lại mục 13 vào data/huong_dan_gan_nhan.md
    .venv/Scripts/python.exe scripts/sinh_phu_luc_cum.py --in     # in mục 13 ra màn hình, không ghi
"""
import argparse
from pathlib import Path
import re
import sys

import yaml

GOC = Path(__file__).resolve().parents[1]
THU_MUC_CAU_HINH = GOC / "data" / "cau_hinh"
TEP_HUONG_DAN = GOC / "data" / "huong_dan_gan_nhan.md"

TIEU_DE_MUC_13 = "## 13. Phụ lục: cụm diễn đạt trong cấu hình"
COT_CUM = ("Chữ trong tài liệu (`tu_tai_lieu`)", "Cách nói thường gặp (`hieu_biet_chung`)")
GHI_CHU_PHIA = {"tai_lieu": " (chỉ phía tài liệu)", "tuyen_bo": " (chỉ phía tuyên bố)"}

# Lời dẫn đầu mục 13. {ngay} là ngày của chung.yaml. Viết tay một lần ở đây; tests/test_sinh_phu_luc_cum.py kiểm các mã nhắc tới có
# thật trong YAML, nên đổi YAML làm lời dẫn sai thì test báo.
LOI_DAN_DAU = """Phụ lục chép đúng các cụm trong `data/cau_hinh/chung.yaml`, `dien_thoai.yaml`, `tai_nghe.yaml`, `dong_ho.yaml` (bản ngày {ngay}), sinh bằng script từ YAML, không gõ tay (`scripts/sinh_phu_luc_cum.py`). Cấu hình đổi thì sinh lại phụ lục và kiểm khớp, như bảng mục 5.

Cách dùng (mục 6.8):

- Cụm có ở đây thì là điều kiện đó (ý 1). So cụm dài nhất trước: "xem video trực tuyến" là `xem_video_truc_tuyen`, không phải `chua_ro_loai_video`.
- `tu_tai_lieu` là chữ có trong tài liệu tập phát triển; `hieu_biet_chung` là cách nói thường gặp, chưa có trong tài liệu.
- Cụm chưa có ở đây thì đọc theo nghĩa (ý 2), ghi `ngoai_cau_hinh=<cụm>`. Thiếu cụm trong phụ lục không phải lý do D1a cho nhãn chuẩn.
- Giá trị ghi "(chỉ phía tài liệu)" hay "(chỉ phía tuyên bố)" (khóa `phia`) chỉ đọc ở một phía. "Sử dụng liên tục" (`su_dung_lien_tuc`) là tên bài đo ở phía tài liệu Xiaomi 15T. Ở phía tuyên bố, "sử dụng liên tục", "dùng liên tục", "liên tục" (`chua_ro_hoat_dong`) không nêu hoạt động cụ thể: coi như chưa nêu, dùng cách hiểu mặc định (ý 3, V07).
- Giá trị ghi "(chỉ `<thuộc tính>`)" (khóa `chi_thuoc_tinh`) chỉ là điều kiện của các thuộc tính đó. "kèm hộp sạc", "tổng cộng"... (`kem_hop_sac`) chỉ là bộ phận kèm hộp sạc với thời lượng pin (ý 6); "có kèm hộp sạc 515 mAh" không phải bộ phận này.
- "sử dụng", "dùng" đứng riêng, như "liên tục", không nêu hoạt động cụ thể (`chua_ro_hoat_dong`, mọi nhóm; ý 3).
- "dưới nắng", "ngoài nắng", "ánh nắng", "dưới ánh nắng" nằm ở chế độ `ngoai_troi` (cách gọi kiểu Apple). Cụm phụ lục ứng với cách gọi chế độ trong cấu hình: tài liệu gọi chế độ sáng cao bằng tên khác (Xiaomi: `tu_tang_sang`, "Dưới ánh sáng mạnh") thì đọc theo ý 2 (V51). "ánh sáng mạnh" không có trong phụ lục; đọc theo ý 2, ghi `ngoai_cau_hinh`.
"""


def doc_yaml(ten, thu_muc=THU_MUC_CAU_HINH):
    return yaml.safe_load((Path(thu_muc) / ten).read_text(encoding="utf-8"))


def cum(ds):
    """Các cụm trong dấu nháy kép cách nhau bằng dấu phẩy; "–" nếu không có cụm nào."""
    return ", ".join(f'"{c}"' for c in ds) if ds else "–"


def ngay_dd_mm_yyyy(ngay):
    """Ngày của chung.yaml (YAML đọc thành date, hoặc chuỗi yyyy-mm-dd) thành dd/mm/yyyy."""
    s = str(ngay)
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if not m:
        raise SystemExit(f"chung.yaml: khóa ngay '{s}' phải có dạng yyyy-mm-dd")
    return f"{m.group(3)}/{m.group(2)}/{m.group(1)}"


def bang_cach_dien_dat(cach_dien_dat):
    """Bảng "Điều kiện | Giá trị | tu_tai_lieu | hieu_biet_chung" của một tệp nhóm."""
    ra = [f"| Điều kiện | Giá trị | {COT_CUM[0]} | {COT_CUM[1]} |", "|---|---|---|---|"]
    for dieu_kien, gia_tri in cach_dien_dat.items():
        dau = True
        for ten, c in gia_tri.items():
            ghi_chu = GHI_CHU_PHIA.get(c.get("phia"), "")
            if c.get("chi_thuoc_tinh"):  # cụm chỉ là điều kiện của các thuộc tính này (trang và ra_tach.py đọc lại ghi chú)
                ghi_chu += " (chỉ " + ", ".join(f"`{t}`" for t in c["chi_thuoc_tinh"]) + ")"
            ra.append(f"| {'`' + dieu_kien + '`' if dau else ''} | `{ten}`{ghi_chu} | {cum(c.get('tu_tai_lieu'))} | "
                      f"{cum(c.get('hieu_biet_chung'))} |")
            dau = False
    return ra


def bang_dung_chung(chung):
    """13.1: bảng các nhóm cụm, rồi từ khẳng định và cụm phủ nhiều giá trị."""
    ra = [f"| Nhóm cụm | Mục con | {COT_CUM[0]} | {COT_CUM[1]} |", "|---|---|---|---|"]
    dau = True
    for ten, c in chung["kieu_gia_tri"].items():
        ra.append(f"| {'Kiểu giá trị (`kieu_gia_tri`)' if dau else ''} | `{ten}` | {cum(c.get('tu_tai_lieu'))} | "
                  f"{cum(c.get('hieu_biet_chung'))} |")
        dau = False
    t = chung["tu_goi_muc_cao"]
    ra.append(f"| Chữ gọi mức cao (`tu_goi_muc_cao`) | một giá trị: `{t['mot_gia_tri']}`; nhiều giá trị: "
              f"`{t['nhieu_gia_tri']}` | {cum(t.get('tu_tai_lieu'))} | {cum(t.get('hieu_biet_chung'))} |")
    dau = True
    for ten, c in chung["dieu_kien_so"]["cum_quan_he"].items():
        ra.append(f"| {'Quan hệ của điều kiện dạng số (`cum_quan_he`)' if dau else ''} | `{ten}` | "
                  f"{cum(c.get('tu_tai_lieu'))} | {cum(c.get('hieu_biet_chung'))} |")
        dau = False
    n = chung["ngu_canh_khong_quyet_dinh"]
    ra.append(f"| Chỉ là ngữ cảnh (`ngu_canh_khong_quyet_dinh`) | | {cum(n.get('tu_tai_lieu'))} | "
              f"{cum(n.get('hieu_biet_chung'))} |")
    tu_kd, cum_phu = chung["tu_khang_dinh"], chung["cum_phu"]
    ra += ["",
           "Từ khẳng định (`tu_khang_dinh`), chỉ tính khi gắn với con số của giá trị (mục 6.2):",
           "",
           f"- Nhóm chắc chắn (`tu`): {cum(tu_kd['tu'])}.",
           f"- Nhóm mức sàn (`tu_muc_san`), chỉ khi đứng liền con số của giá trị: {cum(tu_kd['tu_muc_san'])} "
           "(cách nói thường gặp, `hieu_biet_chung`).",
           f"- Bỏ qua khi có (`bo_qua_khi_co`): {cum(tu_kd['bo_qua_khi_co'])}.",
           "",
           f"Cụm phủ nhiều giá trị (`cum_phu.mau`, mục 6.8): {cum(cum_phu['mau'])}. Cách nói thường gặp (`hieu_biet_chung`); X là chữ "
           "chỉ điều kiện đi sau, A và B là hai giá trị được phủ. Không phải từ khẳng định. Điều kiện của tuyên bố là giá trị kém thuận "
           f"lợi nhất trong các giá trị được phủ mà tài liệu công bố (`{cum_phu['dieu_kien_cua_tuyen_bo']}`); Lệch thì loại "
           f"`{cum_phu['loai_khi_lech']}`."]
    return ra


def bang_cach_goi_do_sang(dien_thoai):
    """Bảng cách gọi độ sáng theo hãng của điện thoại (thuoc_tinh.do_sang.cach_goi_theo_hang)."""
    ra = ["Cách gọi độ sáng theo hãng (`thuoc_tinh.do_sang.cach_goi_theo_hang`), chỉ áp khi chữ phân biệt từ hai giá trị trở lên "
          "(mục 6.5):", "", "| Hãng | Chữ | Chế độ |", "|---|---|---|"]
    for hang, bang in dien_thoai["thuoc_tinh"]["do_sang"]["cach_goi_theo_hang"].items():
        for chu, che_do in bang.items():
            ra.append(f"| {hang} | \"{chu}\" | {', '.join('`' + x + '`' for x in che_do)} |")
    return ra


def dung_phu_luc(chung, dien_thoai, tai_nghe, dong_ho):
    """Toàn văn mục 13 (từ tiêu đề tới hết, kết thúc bằng một dấu xuống dòng)."""
    ra = [TIEU_DE_MUC_13, "", LOI_DAN_DAU.format(ngay=ngay_dd_mm_yyyy(chung["ngay"])).rstrip("\n"), ""]
    ra += ["### 13.1 Dùng chung (`chung.yaml`)", ""] + bang_dung_chung(chung) + [""]
    ra += ["### 13.2 Điện thoại (`dien_thoai.yaml`)", ""] + bang_cach_dien_dat(dien_thoai["cach_dien_dat"]) + [""]
    ra += bang_cach_goi_do_sang(dien_thoai) + [""]
    ra += ["### 13.3 Tai nghe (`tai_nghe.yaml`)", ""] + bang_cach_dien_dat(tai_nghe["cach_dien_dat"]) + [""]
    ra += ["### 13.4 Đồng hồ (`dong_ho.yaml`)", ""] + bang_cach_dien_dat(dong_ho["cach_dien_dat"])
    return "\n".join(ra) + "\n"


def phu_luc_tu_yaml(thu_muc=THU_MUC_CAU_HINH):
    return dung_phu_luc(doc_yaml("chung.yaml", thu_muc), doc_yaml("dien_thoai.yaml", thu_muc),
                        doc_yaml("tai_nghe.yaml", thu_muc), doc_yaml("dong_ho.yaml", thu_muc))


def vi_tri_muc_13(van_ban):
    """(vị trí đầu, vị trí cuối) của mục 13 trong hướng dẫn: từ dòng tiêu đề "## 13. " tới dòng "## " kế tiếp hoặc hết tệp.
    Thoát nếu không có đúng một tiêu đề mục 13."""
    dau = [m.start() for m in re.finditer(r"^## 13\. ", van_ban, re.M)]
    if len(dau) != 1:
        raise SystemExit(f"hướng dẫn cần đúng một tiêu đề '## 13. ...', thấy {len(dau)}")
    tiep = re.compile(r"^## ", re.M).search(van_ban, dau[0] + 1)
    return dau[0], tiep.start() if tiep else len(van_ban)


def doc_van_ban(duong):
    """Nội dung hướng dẫn, đọc theo byte để ghi lại không đổi dòng cuối hay kiểu xuống dòng."""
    b = Path(duong).read_bytes()
    if b"\r\n" in b:
        raise SystemExit(f"{duong} dùng CRLF; script chỉ xử lý LF")
    return b.decode("utf-8")


def thay_muc_13(van_ban, phu_luc):
    """Hướng dẫn với mục 13 thay bằng phu_luc (kết thúc bằng một dấu xuống dòng); phần khác giữ nguyên."""
    dau, cuoi = vi_tri_muc_13(van_ban)
    return van_ban[:dau] + phu_luc + ("\n" if cuoi < len(van_ban) else "") + van_ban[cuoi:]


def kiem(duong=TEP_HUONG_DAN, thu_muc=THU_MUC_CAU_HINH):
    """True nếu mục 13 của hướng dẫn đúng bằng phụ lục sinh từ YAML."""
    return thay_muc_13(doc_van_ban(duong), phu_luc_tu_yaml(thu_muc)) == doc_van_ban(duong)


def ghi(duong=TEP_HUONG_DAN, thu_muc=THU_MUC_CAU_HINH):
    """Ghi lại mục 13. Trả về True nếu tệp đổi."""
    cu = doc_van_ban(duong)
    moi = thay_muc_13(cu, phu_luc_tu_yaml(thu_muc))
    if moi != cu:
        Path(duong).write_bytes(moi.encode("utf-8"))
    return moi != cu


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Sinh phụ lục mục 13 của hướng dẫn gán nhãn từ data/cau_hinh/*.yaml (Bước 16).")
    ap.add_argument("--ghi", action="store_true", help="ghi lại mục 13 vào data/huong_dan_gan_nhan.md")
    ap.add_argument("--in", dest="in_ra", action="store_true", help="in mục 13 ra màn hình, không ghi")
    ap.add_argument("--huong-dan", type=Path, default=TEP_HUONG_DAN, help="mặc định data/huong_dan_gan_nhan.md")
    args = ap.parse_args(argv)
    if args.in_ra:
        sys.stdout.buffer.write(phu_luc_tu_yaml().encode("utf-8"))  # theo byte: Windows không đổi LF thành CRLF
        return 0
    if args.ghi:
        print(f"{args.huong_dan}: " + ("đã ghi lại mục 13" if ghi(args.huong_dan) else "mục 13 đã khớp YAML, không đổi"))
        return 0
    if kiem(args.huong_dan):
        print(f"{args.huong_dan}: mục 13 khớp YAML")
        return 0
    print(f"{args.huong_dan}: mục 13 không khớp YAML; chạy lại với --ghi")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
