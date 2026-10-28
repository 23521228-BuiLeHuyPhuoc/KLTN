"""Tổng hợp khảo sát cách hiểu (Bước 10) theo tiêu chí đặt trước ở mục 6 của ket_qua/khao_sat_cach_hieu.md.

Đọc ket_qua/khao_sat_cach_hieu.csv (tải từ Google Forms), xếp từng câu trả lời vào
"khớp cấu hình", "hiểu khác" hoặc "không biết", rồi in bảng Markdown kèm khoảng tin cậy Wilson 95%.

Chạy: .venv/Scripts/python.exe scripts/tong_hop_khao_sat.py
"""
import csv
import math
import sys
from collections import Counter
from pathlib import Path

CSV = Path(__file__).resolve().parents[1] / "ket_qua" / "khao_sat_cach_hieu.csv"

# Phương án được nhận theo phần đầu câu chữ, vì form thực tế có vài chỗ người thực hiện sửa chữ.
KHOP, KHAC, KB = "khớp", "hiểu khác", "không biết"
QUY_TAC = {
    1: [("Xem video đã tải sẵn", KHAC), ("Xem video trực tuyến", KHOP), ("Chơi game", KHOP), ("Dùng hằng ngày", KHOP)],
    2: [("Nghe nhạc", KHOP), ("Gọi điện", KHAC), ("Dùng lẫn lộn", KHAC)],
    3: [("Bật suốt", KHOP), ("Lúc bật lúc tắt", KHOP), ("Tắt suốt", KHAC)],
    4: [("Chỉ tính tai nghe", KHOP), ("Tính cả hộp sạc", KHAC)],
    5: [("Dùng bình thường", KHOP), ("Tập thể thao liên tục", KHAC)],
    6: [("Chế độ bình thường", KHOP), ("Lúc bình thường, lúc tiết kiệm", KHOP), ("Chế độ tiết kiệm pin", KHAC)],
    8: [("Chỉ cần", KHOP), ("Dùng đồ đi kèm", KHOP), ("Củ sạc thông thường", KHOP), ("Dùng củ sạc nào", KHOP),
        ("Phải dùng", KHAC), ("Phải có", KHAC)],
    9: [("Xem video đã tải sẵn", KHOP), ("Xem video trực tuyến", KHAC), ("Cả hai", KHAC)],
    10: [("Khi dùng bình thường", KHOP), ("Khi ra ngoài trời", KHAC), ("Khi xem phim", KHAC), ("Đây là mức sáng nhất", KHAC)],
    11: [("Chế độ bình thường", KHOP), ("Lúc bình thường, lúc tiết kiệm", KHOP), ("Chế độ tiết kiệm pin", KHAC)],
    12: [("Phóng to 10 lần bằng ống kính", KHOP), ("Phóng to 10 lần bằng phần mềm", KHAC), ("Kết hợp", KHAC)],
    13: [("Bật suốt", KHOP), ("Lúc bật lúc tắt", KHOP), ("Tắt suốt", KHAC)],
}
QUY_TAC[14] = QUY_TAC[8]
# Câu tự ghi ở ô "Khác", xếp tay vào phương án gần nhất (ghi ở mục 7 của tệp kết quả).
TU_GHI = {
    (8, "Dùng cục sạc đúng với công suất cao nhất"): KHAC,  # nói rõ Apple không tặng sạc, phải dùng sạc công suất cao
    (8, "nếu là iphone thì t nghĩ nó mua riêng"): KHAC,
}
# Q07 và Q15: mức "chắc chắn" của cách hiểu, để so từng người.
MUC_CHAC = [("18 giờ là mức tốt nhất", 0), ("Dùng thường xuyên", 1), ("Chắc chắn dùng được ít nhất", 2)]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    tam = (p + z * z / (2 * n)) / (1 + z * z / n)
    nua = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (tam - nua, tam + nua)


def xep(cau, tra_loi):
    if tra_loi.startswith("Không biết"):
        return KB
    for (c, dau), loai in TU_GHI.items():
        if c == cau and tra_loi.startswith(dau):
            return loai
    for dau, loai in QUY_TAC[cau]:
        if tra_loi.startswith(dau):
            return loai
    raise ValueError(f"Câu {cau}: chưa xếp được câu trả lời {tra_loi!r}")


def muc_chac(tra_loi):
    for dau, muc in MUC_CHAC:
        if tra_loi.startswith(dau):
            return muc
    return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    dong = list(csv.reader(CSV.open(encoding="utf-8")))
    tieu_de, phieu = dong[0], dong[1:]
    cot = {int(t.split(".")[0].split()[1]): i for i, t in enumerate(tieu_de) if t.startswith("Câu ")}
    n = len(phieu)
    khong_cntt = [p for p in phieu if p[cot[17]] == "Không"]
    print(f"Số phiếu: {n}; không học, không làm CNTT: {len(khong_cntt)}")
    print("Tuổi:", dict(Counter(p[cot[16]] for p in phieu)), "| Đã mua thiết bị:", dict(Counter(p[cot[18]] for p in phieu)))
    print()
    print("| Câu | Khớp cấu hình | Hiểu khác | Không biết | Tỷ lệ hiểu khác (KTC 95%) | Nhóm không CNTT: hiểu khác | Quá nửa hiểu khác? |")
    print("|---|---|---|---|---|---|---|")
    for cau in sorted(QUY_TAC):
        dem = Counter(xep(cau, p[cot[cau]]) for p in phieu)
        k = dem[KHAC]
        tu, toi = wilson(k, n)
        k2 = sum(xep(cau, p[cot[cau]]) == KHAC for p in khong_cntt)
        print(f"| Q{cau:02d} | {dem[KHOP]} | {k} | {dem[KB]} | {k / n:.0%} ({tu:.0%}–{toi:.0%}) | {k2}/{len(khong_cntt)} | "
              f"{'Có' if k > n / 2 else 'Không'} |")
    print()
    print("Chi tiết từng phương án:")
    for cau in sorted(set(cot) - {16, 17, 18}):
        print(f"  Q{cau:02d}:", dict(Counter(p[cot[cau]] for p in phieu).most_common()))
    print()
    doi = [(muc_chac(p[cot[7]]), muc_chac(p[cot[15]])) for p in phieu]
    chac_hon = sum(a is not None and b is not None and a > b for a, b in doi)
    print(f"Q07 so với Q15: {chac_hon}/{n} người hiểu Q07 (không có 'lên đến') chắc chắn hơn Q15; "
          f"{'quá nửa' if chac_hon > n / 2 else 'không quá nửa'}")


if __name__ == "__main__":
    main()
