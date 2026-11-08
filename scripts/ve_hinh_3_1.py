"""Vẽ Hình 3.1 (sơ đồ phương pháp P) cho Chương 3: luan_van/hinh/hinh_3_1.{png,svg}."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

matplotlib.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
matplotlib.rcParams["svg.fonttype"] = "none"

RA = Path(__file__).resolve().parent.parent / "luan_van" / "hinh"
RA.mkdir(parents=True, exist_ok=True)

W, H = 6.3, 8.0            # inch, rộng ~16 cm
XC, BW, BH = 2.35, 3.5, 0.62   # tâm cột chính, rộng, cao khối
GAP = 0.34
VIEN, NEN_MOI, VIEN_MOI = "#6b6b6b", "#dbe8f7", "#1f4e8c"

fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")


def khoi(xc, yc, w, h, chu, moi=False, co=9):
    ax.add_patch(FancyBboxPatch((xc - w / 2, yc - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                fc=NEN_MOI if moi else "white",
                                ec=VIEN_MOI if moi else VIEN,
                                lw=1.8 if moi else 1.1))
    ax.text(xc, yc, chu, ha="center", va="center", fontsize=co, linespacing=1.3)


def mui_ten(x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=11))


nhan = [
    ("Tuyên bố c, mẫu sản phẩm s", False),
    ("Truy hồi BM25 trên D(s): k đoạn", False),
    ("LLM trích bộ thông số\nkèm câu gốc", False),
    ("Neo nguồn", True),
    ("Kiểm tra đầy đủ và chuẩn hóa", True),
    ("Bộ quyết định A–D", True),
    ("Sinh lý do từ dấu vết\ncủa bộ quyết định", False),
    ("Nhãn y(c), đoạn nguồn e(c), lý do r(c)", False),
]
ytop = H - 0.45 - BH / 2
ys = [ytop - i * (BH + GAP) for i in range(len(nhan))]
for (chu, moi), y in zip(nhan, ys):
    khoi(XC, y, BW, BH, chu, moi)
for y_tren, y_duoi in zip(ys[:-1], ys[1:]):
    mui_ten(XC, y_tren - BH / 2, XC, y_duoi + BH / 2)

# Khối cấu hình: cao phủ ba khối mới, mũi tên ngang vào từng khối
cx, cw = 5.3, 1.7
ytr, yd = ys[3] + BH / 2 + 0.12, ys[5] - BH / 2 - 0.12
khoi(cx, (ytr + yd) / 2, cw, ytr - yd,
     "Tệp cấu hình\ncủa nhóm\nsản phẩm", co=9)
for i in (3, 4, 5):
    mui_ten(cx - cw / 2, ys[i], XC + BW / 2, ys[i])

# Chú thích
ax.add_patch(FancyBboxPatch((4.45, H - 0.9), 0.28, 0.18, boxstyle="round,pad=0,rounding_size=0.03",
                            fc=NEN_MOI, ec=VIEN_MOI, lw=1.5))
ax.text(4.8, H - 0.81, "Khối tô màu:\nphần đề tài đề xuất", fontsize=8, va="center", linespacing=1.3)

for dinh_dang in ("png", "svg"):
    fig.savefig(RA / f"hinh_3_1.{dinh_dang}", dpi=300, facecolor="white",
                bbox_inches="tight", pad_inches=0.1)
print("Đã xuất", RA / "hinh_3_1.png")
