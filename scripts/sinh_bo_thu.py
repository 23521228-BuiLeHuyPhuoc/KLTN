"""Bước 12: sinh 24 bài của bộ thử (2 mẫu thử × 2 LLM × 3 loại bài × 2 chế độ) qua CopyPro.

Đoạn thông số cho chế độ ten_thong_so: các đoạn trong doan.jsonl chứa giá trị của 16 thuộc tính, chép nguyên văn
noi_dung (như người dùng sao chép bảng thông số), nối bằng xuống dòng, không gồm chú thích. Với 2 mẫu thử (tập phát
triển), các đoạn này là các đoạn tệp cấu hình dẫn làm căn cứ (can_cu). Văn bản và danh sách mã đoạn ghi ở
data/quang_cao/thong_so/<ma_mau>.txt và .json.

"noi_dung" ở đây là noi_dung_goc của doan.jsonl: văn bản trước khi bỏ số chú thích của trang hãng (31/10/2026), tức đúng
chữ người dùng sao chép được ('20 phút6'). 24 bài đã sinh dùng văn bản này; đọc noi_dung đã bỏ số chú thích thì chạy lại
sẽ ghi đè thong_so/*.txt bằng văn bản khác với văn bản đã đưa cho LLM.

Bài đã có thì bỏ qua. Lỗi tạm thời của CopyPro (mất kết nối CSDL, HTTP 5xx) thì thử lại tối đa 3 lần.

Chạy (CopyPro đang chạy ở máy):
    PYTHONPATH=src .venv/Scripts/python.exe scripts/sinh_bo_thu.py --phien-ban-copypro a338a65
"""
import argparse
import csv
import json
import sys
import time
from pathlib import Path

import yaml

from kiemchung import sinh_quang_cao as sqc

GOC = Path(__file__).resolve().parents[1]
MAU_THU = ("dt-apple-iphone17", "tn-samsung-buds3pro")
NHOM = {"dt": "dien_thoai", "tn": "tai_nghe", "dh": "dong_ho"}
MO_HINH = ("gemini-3-6-flash", "groq-gpt-oss-120b")
SO_LAN_THU = 3
CHO_GIUA_LAN = 20


def doan_thong_so(ma_mau):
    """Mã đoạn và văn bản thông số của một mẫu tập phát triển, theo can_cu của tệp cấu hình nhóm."""
    cau_hinh = yaml.safe_load((GOC / "data" / "cau_hinh" / f"{NHOM[ma_mau[:2]]}.yaml").read_text(encoding="utf-8"))
    ma_doan = {c for tt in cau_hinh["thuoc_tinh"].values() for c in (tt.get("can_cu") or [])
               if isinstance(c, str) and c.startswith(ma_mau + "#")}
    ma_doan = sorted(ma_doan, key=lambda c: int(c.split("#")[1]))
    doan = {}
    with open(GOC / "data" / "nguon" / ma_mau / "doan.jsonl", encoding="utf-8") as f:
        for dong in f:
            d = json.loads(dong)
            doan[d["id"]] = d.get("noi_dung_goc", d["noi_dung"])  # văn bản chưa bỏ số chú thích, xem docstring đầu tệp
    return ma_doan, "\n".join(doan[c] for c in ma_doan)


def ghi_thong_so(ma_mau):
    ma_doan, van_ban = doan_thong_so(ma_mau)
    thu_muc = GOC / "data" / "quang_cao" / "thong_so"
    thu_muc.mkdir(parents=True, exist_ok=True)
    (thu_muc / f"{ma_mau}.txt").write_text(van_ban, encoding="utf-8", newline="\n")
    (thu_muc / f"{ma_mau}.json").write_text(
        json.dumps({"ma_mau": ma_mau, "ma_doan": ma_doan, "so_ky_tu": len(van_ban),
                    "quy_tac": "đoạn chứa giá trị của 16 thuộc tính (can_cu của tệp cấu hình), nguyên văn noi_dung"},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return van_ban


def la_loi_tam_thoi(loi):
    chu = str(loi)
    return any(x in chu for x in ("ETIMEDOUT", "27017", "mã HTTP 5", "không kết nối được", "timed out"))


def mo_phien_thu_lai():
    for lan_thu in range(1, SO_LAN_THU + 1):
        try:
            return sqc.mo_phien()
        except sqc.LoiCopyPro as e:
            if lan_thu == SO_LAN_THU or not la_loi_tam_thoi(e):
                raise
            print(f"mở phiên: lỗi tạm thời, thử lại sau {CHO_GIUA_LAN} giây: {e}", flush=True)
            time.sleep(CHO_GIUA_LAN)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--phien-ban-copypro", required=True)
    p.add_argument("--thu-muc-ra", default=str(GOC / "data" / "quang_cao"))
    tham_so = p.parse_args(argv)

    ten = {r["ma_mau"]: r["ten"] for r in csv.DictReader(open(GOC / "data" / "mau_san_pham.csv", encoding="utf-8"))}
    thong_so = {m: ghi_thong_so(m) for m in MAU_THU}
    phien = mo_phien_thu_lai()
    da_co = loi = 0
    for ma_mau in MAU_THU:
        for mo_hinh in MO_HINH:
            for loai in sqc.LOAI_BAI:
                for che_do in sqc.CHE_DO:
                    ma_qc = sqc.ma_quang_cao(ma_mau, mo_hinh, loai, che_do, 1)
                    if (Path(tham_so.thu_muc_ra) / f"{ma_qc}.json").exists():
                        da_co += 1
                        continue
                    for lan_thu in range(1, SO_LAN_THU + 1):
                        try:
                            bg = sqc.sinh_mot_bai(phien, ma_mau, ten[ma_mau], loai, che_do, mo_hinh, 1,
                                                  thong_so=thong_so[ma_mau] if che_do == "ten_thong_so" else "",
                                                  phien_ban_copypro=tham_so.phien_ban_copypro,
                                                  thu_muc_ra=tham_so.thu_muc_ra)
                            u = bg["usage"] or {}
                            print(f"{ma_qc} | {len(bg['noi_dung'])} ký tự | prompt trùng {bg['prompt_trung']} | "
                                  f"token {u.get('totalTokens')}", flush=True)
                            break
                        except sqc.LoiCopyPro as e:
                            if lan_thu < SO_LAN_THU and la_loi_tam_thoi(e):
                                print(f"{ma_qc} | lỗi tạm thời, thử lại sau {CHO_GIUA_LAN} giây: {e}", flush=True)
                                time.sleep(CHO_GIUA_LAN)
                                if "đăng nhập" in str(e) or "generate-options" in str(e):
                                    phien = mo_phien_thu_lai()
                                continue
                            print(f"{ma_qc} | LỖI: {e}", flush=True)
                            loi += 1
                            break
    print(f"xong: {da_co} bài đã có từ trước, {loi} bài lỗi", flush=True)
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
