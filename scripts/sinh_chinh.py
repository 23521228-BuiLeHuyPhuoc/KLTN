"""Bước 18: sinh 80 bài của 10 mẫu còn lại; --liet-ke không gọi CopyPro.

Thông số dùng noi_dung_goc, giữ cả số chú thích như văn bản sao chép từ
trang hãng (xem sinh_bo_thu.py), nối các đoạn bằng xuống dòng.
"""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys
import time

import yaml
from kiemchung import sinh_quang_cao as sqc

GOC = Path(__file__).resolve().parents[1]
MAU_THU = ("dt-apple-iphone17", "tn-samsung-buds3pro")
MO_HINH = ("gemini-3-6-flash", "groq-gpt-oss-120b")
NHOM = {"dt": "dien_thoai", "tn": "tai_nghe", "dh": "dong_ho"}
CHO_THU_LAI = (60, 120, 240)
GIOI_HAN_THONG_SO = 5000


def doc_mau():
    with open(GOC / "data/mau_san_pham.csv", encoding="utf-8-sig", newline="") as f:
        mau = [r for r in csv.DictReader(f) if r["ma_mau"] not in MAU_THU]
    if len(mau) != 10 or len({r["ma_mau"] for r in mau}) != 10:
        raise ValueError("cần đúng 10 mẫu khác nhau sau khi bỏ hai mẫu thử")
    return mau


def thiet_ke(mau_moi):
    """Nhận các mã mẫu theo thứ tự CSV, trả (mã mẫu, mô hình, loại, chế độ)."""
    return [(ma, mh, loai, cd)
            for i, ma in enumerate(mau_moi)
            for m, mh in enumerate(MO_HINH)
            for d, cd in enumerate(sqc.CHE_DO)
            for loai in sqc.LOAI_BAI if loai != sqc.LOAI_BAI[(i + 2*m + d) % 3]]


def dung_van_ban(tep_doan, ma_doan):
    """Giữ thứ tự mã đoạn và nguyên văn, kể cả số chú thích của trang hãng."""
    with open(tep_doan, encoding="utf-8") as f:
        doan = {d["id"]: d for d in (json.loads(dong) for dong in f)}
    try:
        van_ban = "\n".join(doan[c]["noi_dung_goc"] for c in ma_doan)
    except KeyError as e:
        raise ValueError(f"{tep_doan}: thiếu đoạn hoặc noi_dung_goc: {e}") from e
    if not van_ban.strip():
        raise ValueError(f"{tep_doan}: chưa có đoạn thông số")
    # Backend CopyPro chặn câu lệnh quá 6.000 ký tự (contentValidation.js); khung câu lệnh của bộ thử
    # dài nhất 976 ký tự (landing), tên sản phẩm dài hơn cộng thêm khoảng 10, nên chừa 1.000.
    if len(van_ban) > GIOI_HAN_THONG_SO:
        raise ValueError(f"{tep_doan}: thông số {len(van_ban)} ký tự, vượt 5.000 ký tự")
    return van_ban


def doan_thong_so(ma_mau, tap):
    if ma_mau in MAU_THU:
        raise ValueError(f"không dùng mẫu thử: {ma_mau}")
    if tap == "phattrien":
        tep = GOC / "data/cau_hinh" / f"{NHOM[ma_mau[:2]]}.yaml"
        cau_hinh = yaml.safe_load(tep.read_text(encoding="utf-8"))
        ma_doan = {c for tt in cau_hinh["thuoc_tinh"].values() for c in (tt.get("can_cu") or [])
                   if isinstance(c, str) and c.startswith(ma_mau + "#")}
        ma_doan = sorted(ma_doan, key=lambda c: int(c.split("#")[1]))
        quy_tac = "can_cu của cấu hình nhóm, nguyên văn noi_dung_goc"
    elif tap == "kiemtra":
        tep = GOC / "data/quang_cao/thong_so/chon_doan_kiemtra.json"
        if not tep.exists():
            raise ValueError(f"{ma_mau}: chưa có đoạn thông số; thiếu {tep}")
        chon = json.loads(tep.read_text(encoding="utf-8"))
        if not chon.get(ma_mau):
            raise ValueError(f"{ma_mau}: chưa có đoạn thông số trong {tep}")
        ma_doan = [d["id"] for d in chon[ma_mau]]
        quy_tac = "chon_doan_kiemtra.json, giữ thứ tự mã đoạn, nguyên văn noi_dung_goc"
    else:
        raise ValueError(f"{ma_mau}: tập không hợp lệ: {tap}")
    if any(not c.startswith(ma_mau + "#") for c in ma_doan):
        raise ValueError(f"{ma_mau}: mã đoạn thuộc mẫu khác")
    van_ban = dung_van_ban(GOC / "data/nguon" / ma_mau / "doan.jsonl", ma_doan)
    return ma_doan, van_ban, quy_tac


def ghi_thong_so(ma_mau, thong_so):
    if ma_mau in MAU_THU:
        raise ValueError(f"không ghi đè thông số mẫu thử: {ma_mau}")
    ma_doan, van_ban, quy_tac = thong_so
    thu_muc = GOC / "data/quang_cao/thong_so"
    thu_muc.mkdir(parents=True, exist_ok=True)
    (thu_muc / f"{ma_mau}.txt").write_text(van_ban, encoding="utf-8", newline="\n")
    (thu_muc / f"{ma_mau}.json").write_text(
        json.dumps({"ma_mau": ma_mau, "ma_doan": ma_doan, "so_ky_tu": len(van_ban),
                    "quy_tac": quy_tac}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n")


LOI_HAN_MUC = ("429", "resource_exhausted", "high demand", "overloaded", "503")
CHO_MAT_KET_NOI = 20  # MongoDB của CopyPro chập chờn: chờ ngắn như sinh_bo_thu


def la_loi_tam_thoi(loi):
    chu = str(loi).lower()
    return any(x in chu for x in ("etimedout", "27017", "mã http 5", "không kết nối được",
                                  "timed out") + LOI_HAN_MUC)


def thoi_gian_cho(loi, lan_thu):
    """Hết hạn mức hoặc quá tải của nhà cung cấp thì chờ tăng dần; mất kết nối CSDL thì chờ ngắn."""
    if any(x in str(loi).lower() for x in LOI_HAN_MUC):
        return CHO_THU_LAI[lan_thu]
    return CHO_MAT_KET_NOI


def liet_ke(mau, to_hop):
    tap = {r["ma_mau"]: r["tap"] for r in mau}
    print("ma_qc | tap")
    for t in to_hop:
        print(f"{sqc.ma_quang_cao(*t, 1)} | {tap[t[0]]}")
    dem = Counter((loai, cd, mh) for _, mh, loai, cd in to_hop)
    print("\nloai | che_do | mo_hinh | so_bai")
    for mh in MO_HINH:
        for cd in sqc.CHE_DO:
            for loai in sqc.LOAI_BAI:
                print(f"{loai} | {cd} | {mh} | {dem[loai, cd, mh]}")
    dem_mau = Counter((ma, cd) for ma, _, _, cd in to_hop)
    print("\nma_mau | ten | ten_thong_so | so_ky_tu_thong_so")
    loi = False
    for r in mau:
        ma = r["ma_mau"]
        try:
            so_ky_tu = len(doan_thong_so(ma, r["tap"])[1])
        except (OSError, ValueError, KeyError, yaml.YAMLError) as e:
            so_ky_tu = str(e)
            if "chưa có đoạn thông số" not in str(e):
                loi = True
        print(f"{ma} | {dem_mau[ma, 'ten']} | {dem_mau[ma, 'ten_thong_so']} | {so_ky_tu}")
    return int(loi)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--liet-ke", action="store_true")
    p.add_argument("--phien-ban-copypro")
    p.add_argument("--thu-muc-ra", default=str(GOC / "data/quang_cao"))
    args = p.parse_args(argv)
    if not args.liet_ke and not args.phien_ban_copypro:
        p.error("chạy thật cần --phien-ban-copypro")
    try:
        mau = doc_mau()
        to_hop = thiet_ke([r["ma_mau"] for r in mau])
        if args.liet_ke:
            return liet_ke(mau, to_hop)
        # Kiểm tra toàn bộ trước khi ghi thông số hay mở phiên CopyPro.
        thong_so = {r["ma_mau"]: doan_thong_so(r["ma_mau"], r["tap"]) for r in mau}
    except (OSError, ValueError, KeyError, yaml.YAMLError) as e:
        print(f"LỖI: {e}", file=sys.stderr)
        return 1
    for ma, ts in thong_so.items():
        ghi_thong_so(ma, ts)
    ten = {r["ma_mau"]: r["ten"] for r in mau}
    phien = None
    da_co = moi = loi = 0
    for ma, mh, loai, cd in to_hop:
        ma_qc = sqc.ma_quang_cao(ma, mh, loai, cd, 1)
        if (Path(args.thu_muc_ra) / f"{ma_qc}.json").exists():
            da_co += 1
            continue
        for lan_thu in range(4):
            try:
                if phien is None:
                    phien = sqc.mo_phien()
                bg = sqc.sinh_mot_bai(phien, ma, ten[ma], loai, cd, mh, 1,
                                      thong_so=thong_so[ma][1] if cd == "ten_thong_so" else "",
                                      phien_ban_copypro=args.phien_ban_copypro,
                                      thu_muc_ra=args.thu_muc_ra)
                moi += 1
                print(f"{ma_qc} | {len(bg['noi_dung'])} ký tự | prompt trùng {bg['prompt_trung']} | "
                      f"token {(bg['usage'] or {}).get('totalTokens')}", flush=True)
                break
            except sqc.LoiCopyPro as e:
                if lan_thu < 3 and la_loi_tam_thoi(e):
                    cho = thoi_gian_cho(e, lan_thu)
                    print(f"{ma_qc} | lỗi tạm thời, thử lại sau {cho} giây: {e}", flush=True)
                    time.sleep(cho)
                    if "đăng nhập" in str(e) or "generate-options" in str(e):
                        phien = None
                    continue
                print(f"{ma_qc} | LỖI: {e}", flush=True)
                loi += 1
                break
    print(f"xong: {da_co} bài đã có từ trước, {moi} bài mới, {loi} bài lỗi", flush=True)
    return 1 if loi else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
