"""Vẽ hình kết quả cho Chương 4 (T6.9) từ các CSV của scripts/danh_gia_he.py; mỗi hình chỉ vẽ khi có CSV tương ứng.

    far_theo_he.png         bang_chinh.csv: FAR từng hệ, thanh KTC 95%
    macro_f1_theo_he.png    bang_chinh.csv: Macro-F1 từng hệ, thanh KTC 95%
    nham_lan_P.png, nham_lan_B2.png   nham_lan_<hệ>.csv: bảng nhầm lẫn dạng heatmap (số tuyên bố; màu theo tỷ lệ trong hàng)
    recall_k.png            recall_k.csv: đường Recall@k theo cách tách, dải KTC
    ty_le_che_do.png        ty_le_theo_che_do.csv: cột nhóm tỷ lệ Lệch và Sai theo chế độ sinh, thanh KTC

Chạy:
    .venv/Scripts/python.exe -X utf8 scripts/ve_hinh_ket_qua.py --vao ket_qua/kiem_tra/bang --ra ket_qua/kiem_tra/hinh
"""
import argparse
import csv
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

matplotlib.rcParams["font.family"] = ["DejaVu Sans"]
DPI = 200
XANH, CAM, XAM = "#1f4e8c", "#d9822b", "#6b6b6b"
NHAN_CHUAN = ("DUNG", "SAI", "LECH", "CHUA_DU")
NHAN_DU_DOAN = (*NHAN_CHUAN, "LOI")
TEN_NHAN = {"DUNG": "Đúng", "SAI": "Sai", "LECH": "Lệch điều kiện", "CHUA_DU": "Chưa đủ thông tin", "LOI": "Lỗi"}
HE_NHAM_LAN = ("P", "B2")


def doc_csv(duong):
    with open(duong, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def so(x):
    """Số thực của ô CSV; None nếu ô trống."""
    return None if x is None or x == "" else float(x)


def luu(fig, ra, ten):
    ra.mkdir(parents=True, exist_ok=True)
    duong = ra / ten
    fig.savefig(duong, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    return duong


def ve_cot_he(dong, khoa, nhan_y, ten_tep, ra, co_ktc=True):
    """Cột của một chỉ số theo hệ (dong: hàng của bang_chinh.csv); thanh KTC khi đủ cận."""
    ten = [d["he"] for d in dong]
    gia_tri = [so(d[f"{khoa}_diem"]) or 0.0 for d in dong]
    fig, ax = plt.subplots(figsize=(max(4.5, 0.9 * len(ten) + 1.5), 3.8))
    sai_so = None
    if co_ktc and all(so(d[f"{khoa}_duoi"]) is not None and so(d[f"{khoa}_tren"]) is not None for d in dong):
        sai_so = [[g - so(d[f"{khoa}_duoi"]) for g, d in zip(gia_tri, dong)],
                  [so(d[f"{khoa}_tren"]) - g for g, d in zip(gia_tri, dong)]]
    ax.bar(ten, gia_tri, color=XANH, width=0.6, yerr=sai_so, capsize=4, ecolor="#333333")
    for i, g in enumerate(gia_tri):
        ax.text(i, g + (sai_so[1][i] if sai_so else 0) + 0.015, f"{g:.2f}".replace(".", ","), ha="center", va="bottom", fontsize=8)
    ax.set_ylabel(nhan_y)
    ax.set_ylim(0, 1.1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color="#e0e0e0")
    ax.set_axisbelow(True)
    return luu(fig, ra, ten_tep)


def ve_nham_lan(dong, he, ra):
    """Heatmap bảng nhầm lẫn: ô ghi số tuyên bố, màu theo tỷ lệ trong hàng (nhãn chuẩn)."""
    hang = [d["nhan_chuan"] for d in dong]
    cot = [c for c in NHAN_DU_DOAN if c in dong[0]]
    so_dem = [[int(float(d[c])) for c in cot] for d in dong]
    ty_le = [[v / sum(h) if sum(h) else 0.0 for v in h] for h in so_dem]
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    anh = ax.imshow(ty_le, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(cot)), [TEN_NHAN.get(c, c) for c in cot], rotation=30, ha="right")
    ax.set_yticks(range(len(hang)), [TEN_NHAN.get(h, h) for h in hang])
    ax.set_xlabel("Nhãn dự đoán")
    ax.set_ylabel("Nhãn chuẩn")
    for i, h in enumerate(so_dem):
        for j, v in enumerate(h):
            ax.text(j, i, str(v), ha="center", va="center", fontsize=9, color="white" if ty_le[i][j] > 0.5 else "black")
    fig.colorbar(anh, ax=ax, label="Tỷ lệ trong hàng", shrink=0.8)
    ax.set_title(f"Bảng nhầm lẫn của {he}", fontsize=10)
    return luu(fig, ra, f"nham_lan_{he}.png")


def ve_recall_k(dong, ra):
    """Đường Recall@k, mỗi cách tách một đường, dải KTC khi có."""
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    cach = list(dict.fromkeys(d["cach_tach"] for d in dong))
    for c, mau in zip(cach, (XANH, CAM, XAM)):
        con = sorted((d for d in dong if d["cach_tach"] == c), key=lambda d: int(d["k"]))
        k = [int(d["k"]) for d in con]
        y = [so(d["recall"]) for d in con]
        if any(v is None for v in y):
            continue
        ax.plot(k, y, marker="o", color=mau, label={"am_tiet": "Âm tiết", "tu": "Từ (pyvi)"}.get(c, c))
        if all(so(d["duoi"]) is not None and so(d["tren"]) is not None for d in con):
            ax.fill_between(k, [so(d["duoi"]) for d in con], [so(d["tren"]) for d in con], color=mau, alpha=0.15, linewidth=0)
    ax.set_xticks(sorted({int(d["k"]) for d in dong}))
    ax.set_xlabel("k")
    ax.set_ylabel("Recall@k")
    ax.set_ylim(0, 1.05)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color="#e0e0e0")
    ax.legend(frameon=False)
    return luu(fig, ra, "recall_k.png")


def ve_ty_le_che_do(dong, ra):
    """Cột nhóm tỷ lệ Lệch và Sai theo chế độ sinh (bỏ dòng tat_ca và chế độ không có tuyên bố)."""
    con = [d for d in dong if d["che_do"] != "tat_ca" and int(float(d["n"])) > 0]
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    rong = 0.36
    for j, (khoa, ten, mau) in enumerate((("lech", "Lệch điều kiện", XANH), ("sai", "Sai", CAM))):
        y = [so(d[f"ty_le_{khoa}"]) or 0.0 for d in con]
        sai_so = None
        if all(so(d[f"{khoa}_duoi"]) is not None for d in con):
            sai_so = [[g - so(d[f"{khoa}_duoi"]) for g, d in zip(y, con)], [so(d[f"{khoa}_tren"]) - g for g, d in zip(y, con)]]
        ax.bar([i + (j - 0.5) * rong for i in range(len(con))], y, rong, color=mau, label=ten, yerr=sai_so, capsize=3, ecolor="#333333")
    ax.set_xticks(range(len(con)), [f"{d['che_do']}\n(n = {int(float(d['n']))})" for d in con])
    ax.set_xlabel("Chế độ sinh quảng cáo")
    ax.set_ylabel("Tỷ lệ tuyên bố")
    ax.set_ylim(0, 1.0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color="#e0e0e0")
    ax.set_axisbelow(True)
    ax.legend(frameon=False)
    return luu(fig, ra, "ty_le_che_do.png")


def ve_tat_ca(vao, ra):
    """Vẽ mọi hình có CSV trong vao; trả danh sách đường dẫn PNG đã ghi."""
    vao, ra = Path(vao), Path(ra)
    da_ve = []
    chinh = vao / "bang_chinh.csv"
    if chinh.exists():
        dong = doc_csv(chinh)
        if dong:
            da_ve.append(ve_cot_he(dong, "far", "FAR (tỷ lệ chấp nhận nhầm)", "far_theo_he.png", ra))
            da_ve.append(ve_cot_he(dong, "macro_f1", "Macro-F1", "macro_f1_theo_he.png", ra))
    for he in HE_NHAM_LAN:
        tep = vao / f"nham_lan_{he}.csv"
        if tep.exists() and (dong := doc_csv(tep)):
            da_ve.append(ve_nham_lan(dong, he, ra))
    tep = vao / "recall_k.csv"
    if tep.exists() and (dong := doc_csv(tep)):
        da_ve.append(ve_recall_k(dong, ra))
    tep = vao / "ty_le_theo_che_do.csv"
    if tep.exists() and (dong := doc_csv(tep)):
        da_ve.append(ve_ty_le_che_do(dong, ra))
    return da_ve


def main(argv=None):
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Vẽ hình kết quả (T6.9) từ CSV của scripts/danh_gia_he.py.")
    ap.add_argument("--vao", type=Path, required=True, help="thư mục chứa các CSV")
    ap.add_argument("--ra", type=Path, required=True, help="thư mục ghi PNG")
    args = ap.parse_args(argv)
    if not args.vao.is_dir():
        ap.error(f"không có thư mục {args.vao}")
    da_ve = ve_tat_ca(args.vao, args.ra)
    for d in da_ve:
        print("Đã ghi", d)
    if not da_ve:
        print("Không có CSV nào để vẽ.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
