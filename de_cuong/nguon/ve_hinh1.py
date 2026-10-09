"""Vẽ Hình 1: quy trình kiểm chứng đề xuất (hai hàng, mũi tên thẳng)."""
import matplotlib
from pathlib import Path
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "Liberation Serif"

W_CM, H_CM = 16.0, 6.1
fig = plt.figure(figsize=(W_CM / 2.54, H_CM / 2.54), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W_CM)
ax.set_ylim(0, H_CM)
ax.axis("off")

BOX_W, BOX_H = 4.6, 2.0
GAP = (W_CM - 3 * BOX_W) / 4          # khoảng cách đều giữa các khối
XS = [GAP + i * (BOX_W + GAP) for i in range(3)]
Y_TOP, Y_BOT = 3.8, 0.3             # góc dưới của hàng trên / hàng dưới

NEW = "#d9d9d9"                        # nền xám = thành phần mới

boxes = [
    (XS[0], Y_TOP, "Quảng cáo do CopyPro\ntạo bằng LLM", None),
    (XS[1], Y_TOP, "Tách tuyên bố thông số\ncó điều kiện ràng buộc", None),
    (XS[2], Y_TOP, "Truy hồi BM25 trong tài liệu\nchính hãng của mẫu sản phẩm\nngười dùng đã chọn", None),
    (XS[0], Y_BOT, "Trích xuất bộ thông số\ncó neo nguồn\n(kiểm tra câu trích)", NEW),
    (XS[1], Y_BOT, "Bộ quyết định:\nA khớp sản phẩm, thuộc tính\nB đối chiếu điều kiện\nC so giá trị, D tổng hợp nhãn", NEW),
    (XS[2], Y_BOT, "Đúng / Sai / Lệch điều kiện /\nChưa đủ thông tin, kèm đoạn\nnguồn và lý do trên CopyPro", None),
]

for x, y, text, fill in boxes:
    ax.add_patch(FancyBboxPatch(
        (x, y), BOX_W, BOX_H,
        boxstyle="round,pad=0,rounding_size=0.18",
        linewidth=1.0, edgecolor="black",
        facecolor=fill if fill else "white",
    ))
    ax.text(x + BOX_W / 2, y + BOX_H / 2, text, ha="center", va="center",
            fontsize=9.2, linespacing=1.25)

arrow = dict(arrowstyle="-|>", color="black", lw=1.0, mutation_scale=10,
             shrinkA=0, shrinkB=0)

def h_arrow(x0, x1, y):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=arrow)

# Hàng trên: 1 -> 2 -> 3
yt = Y_TOP + BOX_H / 2
h_arrow(XS[0] + BOX_W, XS[1], yt)
h_arrow(XS[1] + BOX_W, XS[2], yt)

# Nối 3 -> 4 bằng các đoạn thẳng gấp khúc vuông góc
x3 = XS[2] + BOX_W / 2
x4 = XS[0] + BOX_W / 2
y_mid = (Y_TOP + Y_BOT + BOX_H) / 2
ax.plot([x3, x3], [Y_TOP, y_mid], color="black", lw=1.0)
ax.plot([x3, x4], [y_mid, y_mid], color="black", lw=1.0)
ax.annotate("", xy=(x4, Y_BOT + BOX_H), xytext=(x4, y_mid), arrowprops=arrow)

# Hàng dưới: 4 -> 5 -> 6
yb = Y_BOT + BOX_H / 2
h_arrow(XS[0] + BOX_W, XS[1], yb)
h_arrow(XS[1] + BOX_W, XS[2], yb)

fig.savefig(Path(__file__).with_name("hinh1_quy_trinh.png"), dpi=300)
print("ok")
