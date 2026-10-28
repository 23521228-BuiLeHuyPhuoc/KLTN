"""Bước 12: in các bài của bộ thử ra data/tuyen_bo/doc_bo_thu.md để đọc khi tách tay, và tạo
data/tuyen_bo/thu_nhap.csv (chỉ dòng tiêu đề) nếu chưa có. Bài in nguyên văn, không đánh dấu câu nào.

Chạy: .venv/Scripts/python.exe scripts/in_bo_thu.py
"""
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
THU_MUC_QC = GOC / "data" / "quang_cao"
THU_MUC_TB = GOC / "data" / "tuyen_bo"
TEN_LOAI = {"description": "Mô tả sản phẩm", "social": "Bài mạng xã hội", "landing": "Landing page"}
TEN_CHE_DO = {"ten": "chỉ nhập tên", "ten_thong_so": "nhập tên và thông số"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    bai = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(THU_MUC_QC.glob("qc-*.json"))]
    dong = ["# 24 bài của bộ thử (Bước 12)", "",
            "Đọc theo hướng dẫn `data/tuyen_bo/huong_dan_tach_tay.md`. Mã bài ở dòng tiêu đề, chép vào cột `ma_qc`.", ""]
    for b in bai:
        dong += [f"## `{b['ma_qc']}`", "",
                 f"{b['ten_nhap']} · {b['mo_hinh_nha_cung_cap'] or b['mo_hinh']} · {TEN_LOAI[b['loai_bai']]} · "
                 f"{TEN_CHE_DO[b['che_do']]}", "", "```text", b["noi_dung"].rstrip(), "```", ""]
    THU_MUC_TB.mkdir(parents=True, exist_ok=True)
    (THU_MUC_TB / "doc_bo_thu.md").write_text("\n".join(dong), encoding="utf-8", newline="\n")
    csv_mau = THU_MUC_TB / "thu_nhap.csv"
    if not csv_mau.exists():
        csv_mau.write_text("ma_qc,cau_goc,tuyen_bo,thuoc_tinh,ghi_chu\n", encoding="utf-8-sig", newline="\n")
    print(f"đã in {len(bai)} bài vào {THU_MUC_TB / 'doc_bo_thu.md'}")


if __name__ == "__main__":
    main()
