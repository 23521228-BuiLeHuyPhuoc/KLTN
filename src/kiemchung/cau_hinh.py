"""Đọc và kiểm tệp cấu hình điều kiện bắt buộc (Bước 8, T5.7).

Mỗi nhóm sản phẩm có data/cau_hinh/<nhom>.yaml, kế thừa phần dùng chung ở chung.yaml. Căn cứ của
cấu hình là data/cau_hinh/bao_phu_dieu_kien.md. kiem_* trả danh sách lỗi (chuỗi); rỗng là đạt.

Các điều kiểm:
- mỗi thuộc tính có đủ khóa theo T5.7, loại điều kiện thuộc sáu loại, mỗi điều kiện có cách hiểu
  thông thường và có mục cách diễn đạt; cách hiểu là một giá trị đã khai báo hoặc giá trị đặc biệt;
- căn cứ (mã đoạn) chỉ lấy từ tập phát triển (T3.5 quy tắc 4);
- mỗi cụm "tu_tai_lieu" có thật trong doan.jsonl của tập phát triển;
- phần luật không nhắc mã mẫu tập kiểm tra; bảng bí danh có đủ mẫu của nhóm;
- chung.yaml có luật chặn điều kiện lạ (dieu_kien_la dẫn tới D1a) và quy tắc chữ gọi mức cao;
- mỗi điều kiện dạng số (cach_dien_dat có gia_tri_so) khai báo đơn vị và quan hệ so sánh ở dieu_kien_so.
"""
import csv
import json
from pathlib import Path
import re
import unicodedata

import yaml

GOC = Path(__file__).resolve().parents[2]
THU_MUC = GOC / "data" / "cau_hinh"
NHOM = ("dien_thoai", "tai_nghe", "dong_ho")
KHOA_BAT_BUOC = ("don_vi", "huong_thuan_loi", "kieu_gia_tri_mac_dinh", "dieu_kien_bat_buoc",
                 "hieu_thong_thuong", "can_cu")
CAN_CU_KHONG_BANG_CHUNG = "hieu_biet_chung"


def doc_yaml(duong_dan):
    with open(duong_dan, encoding="utf-8") as f:
        return yaml.safe_load(f)


def doc_cau_hinh(nhom, thu_muc=THU_MUC):
    """Cấu hình của một nhóm; phần dùng chung gắn ở khóa 'chung'."""
    rieng = doc_yaml(Path(thu_muc) / f"{nhom}.yaml")
    chung = doc_yaml(Path(thu_muc) / rieng.get("ke_thua", "chung.yaml"))
    return {**rieng, "chung": chung}


def chuan_hoa_chu(s):
    """So khớp cụm diễn đạt: NFC, chữ thường, gạch không ngắt thành '-', gộp khoảng trắng."""
    s = unicodedata.normalize("NFC", s).lower()
    s = re.sub(r"[‐‑]", "-", s)
    return re.sub(r"\s+", " ", s).strip()


def doc_mau(goc=GOC):
    with open(Path(goc) / "data" / "mau_san_pham.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def tai_lieu_phat_trien(goc=GOC):
    """(chữ đã chuẩn hóa của mọi đoạn tập phát triển, tập mã đoạn tập phát triển)."""
    chu, ma = [], set()
    for row in doc_mau(goc):
        if row["tap"] != "phattrien":
            continue
        with open(Path(goc) / "data" / "nguon" / row["ma_mau"] / "doan.jsonl", encoding="utf-8") as f:
            for dong in f:
                d = json.loads(dong)
                ma.add(d["id"])
                chu.append(chuan_hoa_chu(" ".join([d["noi_dung"], *d["chu_thich"]])))
    return "\n".join(chu), ma


def _cum_tu_tai_lieu(muc):
    """Các cụm tu_tai_lieu trong một mục {gia_tri: {tu_tai_lieu: [...], hieu_biet_chung: [...]}}."""
    for ten, nguon in (muc or {}).items():
        for cum in (nguon or {}).get("tu_tai_lieu", []):
            yield ten, cum


def kiem_cum(noi, muc, van_ban):
    return [f"{noi}.{ten}: cụm '{cum}' không có trong tài liệu tập phát triển"
            for ten, cum in _cum_tu_tai_lieu(muc) if chuan_hoa_chu(cum) not in van_ban]


def kiem_chung(chung, van_ban):
    loi = kiem_cum("chung.kieu_gia_tri", {k: v for k, v in chung["kieu_gia_tri"].items()}, van_ban)
    loi += kiem_cum("chung.ngu_canh", {"ngu_canh": chung["ngu_canh_khong_quyet_dinh"]}, van_ban)
    loi += kiem_cum("chung.tu_goi_muc_cao", {"tu_goi_muc_cao": chung.get("tu_goi_muc_cao")}, van_ban)
    loi += kiem_cum("chung.dieu_kien_so", (chung.get("dieu_kien_so") or {}).get("cum_quan_he"), van_ban)
    for khoa in ("loai_dieu_kien", "hieu_thong_thuong_dac_biet", "tu_khang_dinh", "chuan_hoa",
                 "dieu_kien_la", "tu_goi_muc_cao", "dieu_kien_so"):
        if khoa not in chung:
            loi.append(f"chung: thiếu khóa {khoa}")
    if len(chung.get("loai_dieu_kien", [])) != 6:
        loi.append("chung: loai_dieu_kien phải có đúng sáu loại")
    if (chung.get("dieu_kien_la") or {}).get("nguyen_nhan_D1a") != "dieu_kien_la":
        loi.append("chung: dieu_kien_la phải dẫn tới D1a (điều kiện lạ không bao giờ ra Đúng)")
    return loi


def kiem_dieu_kien_so(noi, tt, cach, chung):
    """Điều kiện dạng số: mỗi điều kiện có cach_dien_dat chứa gia_tri_so phải khai báo trong dieu_kien_so
    (đơn vị đã chuẩn hóa, quan hệ hợp lệ), và ngược lại."""
    loi = []
    quan_he = set((chung.get("dieu_kien_so") or {}).get("quan_he_hop_le") or {})
    don_vi = set(chung["chuan_hoa"]["don_vi"])
    so = tt.get("dieu_kien_so") or {}
    dk = tt.get("dieu_kien_bat_buoc") or {}
    for ten_dk in dk:
        if "gia_tri_so" in (cach.get(ten_dk) or {}) and ten_dk not in so:
            loi.append(f"{noi}.{ten_dk}: điều kiện dạng số chưa khai báo trong dieu_kien_so")
    for ten_dk, kb in so.items():
        if ten_dk not in dk:
            loi.append(f"{noi}.{ten_dk}: dieu_kien_so khai báo điều kiện không bắt buộc")
        if (kb or {}).get("don_vi") not in don_vi:
            loi.append(f"{noi}.{ten_dk}: đơn vị '{(kb or {}).get('don_vi')}' chưa có trong chuan_hoa.don_vi")
        if (kb or {}).get("thoa_khi") not in quan_he:
            loi.append(f"{noi}.{ten_dk}: quan hệ '{(kb or {}).get('thoa_khi')}' không hợp lệ")
        if "gia_tri_so" not in (cach.get(ten_dk) or {}):
            loi.append(f"{noi}.{ten_dk}: cach_dien_dat thiếu gia_tri_so")
    return loi


def thoa_dieu_kien_so(thoa_khi, gia_tri_tuyen_bo, gia_tri_tai_lieu, nguong_bang=0.01):
    """Giá trị điều kiện của tuyên bố có thỏa điều kiện trong tài liệu không (cùng đơn vị).
    Ví dụ bộ tiếp hợp: tài liệu 40W trở lên, tuyên bố 20W thì không thỏa (khác điều kiện)."""
    bang = abs(gia_tri_tuyen_bo - gia_tri_tai_lieu) <= nguong_bang * abs(gia_tri_tai_lieu)
    if thoa_khi == "bang":
        return bang
    if thoa_khi == "tuyen_bo_lon_hon_hoac_bang":
        return bang or gia_tri_tuyen_bo > gia_tri_tai_lieu
    if thoa_khi == "tuyen_bo_nho_hon_hoac_bang":
        return bang or gia_tri_tuyen_bo < gia_tri_tai_lieu
    raise ValueError(f"quan hệ không hợp lệ: {thoa_khi}")


def kiem_nhom(cau_hinh, van_ban, ma_phat_trien, mau):
    """Lỗi của một nhóm. mau: các dòng mau_san_pham.csv."""
    loi = []
    chung = cau_hinh["chung"]
    nhom = cau_hinh.get("nhom", "?")
    loai_hop_le = set(chung["loai_dieu_kien"])
    dac_biet = set(chung["hieu_thong_thuong_dac_biet"])
    cach = cau_hinh.get("cach_dien_dat") or {}

    for ten, tt in (cau_hinh.get("thuoc_tinh") or {}).items():
        noi = f"{nhom}.{ten}"
        loi += [f"{noi}: thiếu khóa {k}" for k in KHOA_BAT_BUOC if k not in tt]
        if tt.get("kieu_gia_tri_mac_dinh") not in set(chung["kieu_gia_tri"]) | dac_biet:
            loi.append(f"{noi}: kieu_gia_tri_mac_dinh '{tt.get('kieu_gia_tri_mac_dinh')}' không hợp lệ")
        dk = tt.get("dieu_kien_bat_buoc") or {}
        htt = tt.get("hieu_thong_thuong") or {}
        for ten_dk, loai in dk.items():
            if loai not in loai_hop_le:
                loi.append(f"{noi}.{ten_dk}: loại '{loai}' không thuộc sáu loại")
            if ten_dk not in cach:
                loi.append(f"{noi}.{ten_dk}: thiếu cach_dien_dat")
            if ten_dk not in htt:
                loi.append(f"{noi}.{ten_dk}: thiếu hieu_thong_thuong")
            elif htt[ten_dk] not in dac_biet and htt[ten_dk] not in (cach.get(ten_dk) or {}):
                loi.append(f"{noi}.{ten_dk}: cách hiểu '{htt[ten_dk]}' chưa khai báo trong cach_dien_dat")
        loi += [f"{noi}.{k}: có cách hiểu nhưng không phải điều kiện bắt buộc" for k in htt if k not in dk]
        can_cu = tt.get("can_cu")
        if can_cu != CAN_CU_KHONG_BANG_CHUNG:
            loi += [f"{noi}: căn cứ '{ma}' không thuộc tập phát triển" for ma in (can_cu or [])
                    if ma not in ma_phat_trien]
        loi += kiem_dieu_kien_so(noi, tt, cach, chung)
        for hang, tu in (tt.get("cach_goi_theo_hang") or {}).items():
            for chu, che_do in tu.items():
                loi += [f"{noi}: cách gọi '{chu}' của {hang} trỏ tới chế độ chưa khai báo '{c}'"
                        for c in che_do if c not in (cach.get("che_do_hien_thi") or {})]

    for ten_dk, muc in cach.items():
        loi += kiem_cum(f"{nhom}.cach_dien_dat.{ten_dk}", muc, van_ban)

    kiem_tra = {r["ma_mau"] for r in mau if r["tap"] == "kiemtra"}
    phan_luat = yaml.safe_dump({"thuoc_tinh": cau_hinh.get("thuoc_tinh"), "cach_dien_dat": cach},
                               allow_unicode=True)
    loi += [f"{nhom}: phần luật nhắc mẫu tập kiểm tra {m}" for m in sorted(kiem_tra) if m in phan_luat]

    san_pham = cau_hinh.get("san_pham") or {}
    for r in mau:
        if r["nhom"] != nhom:
            continue
        sp = san_pham.get(r["ma_mau"])
        if not sp:
            loi.append(f"{nhom}: bảng bí danh thiếu {r['ma_mau']}")
        elif sp.get("ten") != r["ten"] or not sp.get("bi_danh"):
            loi.append(f"{nhom}: bí danh của {r['ma_mau']} sai tên hoặc trống")
    return loi


def kiem_tat_ca(thu_muc=THU_MUC, goc=GOC):
    """{tên phần: danh sách lỗi} cho chung.yaml và từng nhóm."""
    van_ban, ma = tai_lieu_phat_trien(goc)
    mau = doc_mau(goc)
    ket_qua = {"chung": kiem_chung(doc_yaml(Path(thu_muc) / "chung.yaml"), van_ban)}
    for nhom in NHOM:
        ket_qua[nhom] = kiem_nhom(doc_cau_hinh(nhom, thu_muc), van_ban, ma, mau)
    return ket_qua
