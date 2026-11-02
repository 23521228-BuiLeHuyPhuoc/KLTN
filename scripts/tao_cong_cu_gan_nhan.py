"""Bước 13, 16: sinh công cụ gán nhãn chuẩn data/nhan/cong_cu_gan_nhan.html cho 66 tuyên bố của bộ thử.

Một tệp HTML tự chứa (CSS, JavaScript viết thẳng, không tải gì từ mạng), mở trực tiếp bằng trình duyệt
(file://). Dữ liệu nhúng vào tệp dưới dạng JSON: tuyên bố (data/tuyen_bo/thu.jsonl), bài quảng cáo của các
tuyên bố đó (data/quang_cao/<ma_qc>.json), toàn bộ đoạn tài liệu của các mẫu có tuyên bố
(data/nguon/<ma_mau>/doan.jsonl, giữ nguyên thứ tự trong tệp; cột phải hiện noi_dung đã bỏ số chú thích của trang hãng, bản
trước khi bỏ ở noi_dung_goc chỉ dùng để kiểm câu trích) và nội dung hướng dẫn gán nhãn
(data/huong_dan_gan_nhan.md, đọc lúc sinh trang: sửa hướng dẫn rồi chạy lại script là trang cập nhật).

Bản này là trang của lượt 2 (Bước 16, hướng dẫn bản 2, luan_van/buoc16_de_xuat_huong_dan_ban2.md mục 6, S1-S25):
khóa lưu gan_nhan_thu_v2, bản ghi xuất ra có luot = 2, tệp tải về thu_luot2.jsonl và cau_hoi_nhan_luot2.md. Lượt 1 giữ
nguyên ở data/nhan/thu.jsonl và thu_luot1.jsonl; nút "Nhập lại" từ chối bản ghi luot khác 2.

Lượt 3 (người thực hiện tự gán lại mù một phần bộ thử để đo độ nhất quán, scripts/do_nhat_quan.py): cùng trang, tham số
--luot 3 --chon <tệp mã> --ra <HTML>. Khóa lưu thêm hậu tố _luot3 (gan_nhan_thu_v2_luot3, gan_nhan_giao_dien_v2_luot3) để không
đè dữ liệu lượt 2 trong trình duyệt, bản ghi xuất ra có luot = 3, tệp tải về thu_luot3.jsonl và cau_hoi_nhan_luot3.md, nút
"Nhập lại" chỉ nhận bản ghi luot = 3. --chon chỉ đưa các tuyên bố có mã trong tệp vào trang, xáo trộn thứ tự theo seed cố định
(SEED_XAO) để thứ tự không lộ nhóm. Trang không nhúng nhãn nào (lượt 1, lượt 2, của Claude). Không có --luot thì sinh trang
lượt 2 như cũ (--luot 2 không kèm --chon là trang đầy đủ 66 tuyên bố).

Ranh giới của công cụ (giữ khi sửa):
- Được hiện: nội dung hướng dẫn giống nhau cho mọi tuyên bố (cách làm, bảng D1-D6 kèm câu hỏi, ví dụ và mẫu câu, quy
  tắc hay dùng, toàn văn hướng dẫn), hoặc nội dung lọc theo nhóm sản phẩm (tiền tố ma_mau) và thuộc tính đã ghi sẵn
  trên tuyên bố (khung "Bước 3" từ mục 5 và 5.1, khung "Cụm điều kiện đã biết" từ phụ lục mục 13, hướng thuận lợi ở
  mục 6.1, tên thuộc tính ở câu hỏi D1).
- Không được: gợi ý nhãn, tự đánh giá D1-D6 cho một tuyên bố, đoán loại biến đổi, chọn bằng chứng, lọc hay sắp xếp
  đoạn tài liệu theo tuyên bố (cột phải hiện mọi đoạn của mẫu). Người gán tự đọc, tự chọn dòng D ("Dừng ở đây").
- Không hiện ghi_chu của tuyên bố (ghi chú tách như tach_sua=…, ghi chú bỏ phần, gộp): khi gán chỉ đọc chữ của tuyên bố (hướng
  dẫn mục 1, bước 0). Trường ghi_chu vẫn nằm trong dữ liệu nhúng (TRUONG_TUYEN_BO), chỉ không hiện ra.
- Nhãn và loại chỉ được suy ra từ dòng D người gán đã chọn (NHAN_THEO_DONG, LOAI_THEO_DONG), không từ nội dung tuyên bố.
- Bắt lỗi chỉ theo kiểu "các ô người gán điền mâu thuẫn nhau hoặc trái quy tắc", dựa vào thông tin đã có sẵn trên
  tuyên bố (nhóm từ tiền tố ma_mau, thuộc tính) và các ô người gán điền (dòng D, nhãn, loại, bằng chứng, câu trích,
  lý do, ghi chú, tick tài liệu mâu thuẫn). Không đọc nội dung tuyên bố (tuyen_bo, cau_goc) để suy ra nhãn: không dò cụm
  điều kiện trong câu tuyên bố, không đoán dòng D. Gợi ý "đoạn khác cũng có chữ này" (S16) chỉ dùng chuỗi người gán
  đã bôi đen.
Các quy tắc kiểm trên trang là bản JavaScript của scripts/kiem_nhan.py; sửa một bên thì sửa bên kia (tests/test_tao_cong_cu_gan_nhan.py
chạy khối LUAT_KIEM của trang trong node và so với kiem_nhan.py). Quy tắc: dòng D, loại biến đổi theo nhãn, tài liệu mâu thuẫn,
chỗ {…} chưa thay, bằng chứng, câu trích, mac_dinh trong ghi chú (mac_dinh của điều kiện "không có mặc định" chỉ ở D1a; D1a phải
ghi nguyên nhân: mac_dinh=<khóa không có mặc định> hoặc chua_xac_dinh=<cụm>; D2 phải ghi khang_dinh=<từ ở mục 6.2>), lý do không
chép mã đoạn vào chỗ câu trích. Lời nhắc (không chặn lưu): bo_dieu_kien thiếu mac_dinh, D1 mà ghi mac_dinh, câu trích không có đơn vị
của thuộc tính (mục 6.1). Bảng dòng D, thông báo lỗi và lời nhắc nằm ở đây (THONG_BAO, NHAC) và được nhúng vào trang, còn
kiem_nhan.py import lại, nên hai bên cùng chữ.

Nhãn đã gán nằm trong localStorage của trình duyệt (khóa gan_nhan_thu_v2), không nằm trong tệp HTML, nên sinh lại
trang không mất nhãn. Trạng thái mở/đóng các khung hướng dẫn và danh sách tuyên bố đang bị cảnh báo "không qua quy
tắc mới" nằm ở khóa riêng gan_nhan_giao_dien_v2. Đồng hồ dừng đếm khi không có thao tác quá 3 phút; số giây bị bỏ ghi riêng
(trường giay_nghi của bản ghi xuất ra, tùy chọn).

Chạy: .venv/Scripts/python.exe scripts/tao_cong_cu_gan_nhan.py
Kết quả: nút "Tải nhãn (thu_luot2.jsonl)" trong công cụ tải tệp để chép vào data/nhan/thu_luot2.jsonl, rồi kiểm bằng
    .venv/Scripts/python.exe scripts/kiem_nhan.py data/nhan/thu_luot2.jsonl
Lượt 3: .venv/Scripts/python.exe scripts/tao_cong_cu_gan_nhan.py --luot 3 --chon data/nhan/chon_luot3.txt --ra data/nhan/cong_cu_gan_nhan_luot3.html
    (không có --ra thì ghi data/nhan/cong_cu_gan_nhan_luot3.html; tệp tải về thu_luot3.jsonl kiểm bằng
    kiem_nhan.py data/nhan/thu_luot3.jsonl --chon data/nhan/chon_luot3.txt --luot 3)
"""
import argparse
import html
import json
from pathlib import Path
import random
import re
import sys
import unicodedata

GOC = Path(__file__).resolve().parents[1]
TEP_TUYEN_BO = GOC / "data" / "tuyen_bo" / "thu.jsonl"
TEP_HUONG_DAN = GOC / "data" / "huong_dan_gan_nhan.md"
THU_MUC_QC = GOC / "data" / "quang_cao"
THU_MUC_NGUON = GOC / "data" / "nguon"
TEP_RA = GOC / "data" / "nhan" / "cong_cu_gan_nhan.html"

TRUONG_TUYEN_BO = ("id", "ma_qc", "ma_mau", "cau_goc", "tuyen_bo", "thuoc_tinh", "llm_sinh", "che_do",
                   "loai_bai", "url_nguon", "ghi_chu")
# Nhóm sản phẩm suy từ tiền tố của ma_mau (dt-apple-iphone17 -> dt); tên nhóm như cột "Nhóm" trong hướng dẫn.
NHOM_THEO_TIEN_TO = {"dt": "Điện thoại", "tn": "Tai nghe", "dh": "Đồng hồ"}
MA_NHAN = ("DUNG", "SAI", "LECH", "CHUA_DU")
# Lượt gán của trang này (hướng dẫn mục 8, QT11): lượt 2 theo hướng dẫn bản 2. Khóa lưu riêng với lượt 1 (gan_nhan_thu_v1).
LUOT = 2
KHOA_NHAN = "gan_nhan_thu_v2"
KHOA_GIAO_DIEN = "gan_nhan_giao_dien_v2"
TEN_TEP_NHAN = f"thu_luot{LUOT}.jsonl"
TEN_TEP_HOI = f"cau_hoi_nhan_luot{LUOT}.md"
# Trang chọn một phần bộ thử (--chon): thứ tự hiển thị xáo trộn theo seed này, phụ thuộc tập mã chứ không phụ thuộc thứ tự
# trong tệp chọn, nên sinh lại trang vẫn ra đúng thứ tự cũ (chỉ số tuyên bố đang mở lưu trong trình duyệt vẫn đúng).
SEED_XAO = 20261102
NGHI_GIAY = 180  # S21: không thao tác quá chừng này giây thì đồng hồ dừng đếm
MA_LOAI = ("bo_dieu_kien", "doi_dieu_kien", "doi_bo_phan", "doi_phien_ban", "doi_kieu_gia_tri", "doi_gia_tri")

# Dòng D (hướng dẫn mục 7) và nhãn suy ra từ dòng người gán dừng ở. Bấm "Dừng ở đây" thì nhãn tự đặt theo bảng này;
# D2 còn tự đặt loại, D1b còn tự tick tai_lieu_mau_thuan. Tên nhãn trong bảng mục 7 của hướng dẫn phải khớp (bang_dong_d kiểm).
MA_DONG_D = ("D1", "D1a", "D1b", "D2", "D3", "D4", "D5", "D6")
NHAN_THEO_DONG = {"D1": "CHUA_DU", "D1a": "CHUA_DU", "D1b": "CHUA_DU", "D2": "LECH", "D3": "DUNG", "D4": "LECH",
                  "D5": "SAI", "D6": "CHUA_DU"}
LOAI_THEO_DONG = {"D2": "doi_kieu_gia_tri"}
DONG_TICK_MAU_THUAN = "D1b"
TEN_NHAN_TRONG_HUONG_DAN = {"CHUA_DU": "Chưa đủ thông tin", "LECH": "Lệch", "DUNG": "Đúng", "SAI": "Sai"}

# Chữ hiện trên trang cho từng dòng D (giống nhau cho mọi tuyên bố). vi_du: (mã ví dụ trong hướng dẫn, "" nếu giả định; chữ).
DONG_D_HIEN_THI = {
    "D1": {
        # {thuoc_tinh} do trang thay bằng tên thuộc tính ghi sẵn trên tuyên bố (tên lấy từ bảng mục 5 của hướng dẫn).
        "cau_hoi": "Tài liệu của đúng sản phẩm có con số nào cho thuộc tính {thuoc_tinh} không, ở bất kỳ điều kiện hay bộ "
                   "phận nào? Không có số nào thì dừng. Có số nhưng ở điều kiện khác thì dò tiếp.",
        "nhan": "Chưa đủ thông tin (bằng chứng để trống)",
        "vi_du": ("", "Tai nghe B nghe nhạc 8 giờ. Hãng chỉ ghi Bluetooth, trọng lượng, chống nước; không có con số giờ "
                      "pin nào, kể cả trong chú thích. Không có gì để so nên dừng ở D1, bằng chứng để trống."),
    },
    "D1a": {
        "cau_hoi": "Có biết tuyên bố đang nói ở điều kiện nào không? Điều kiện nêu rõ, hoặc có cách hiểu mặc định ở khung "
                   "Bước 3 phía trên, là đã biết, không dừng ở đây. Chỉ dừng khi: (1) điều kiện ghi “Không có mặc "
                   "định” mà tuyên bố không nêu; (2) chữ của tuyên bố trỏ tới nhiều chế độ; (3) cụm điều kiện không "
                   "giải được (mục 6.7, 6.8). Ghi nguyên nhân vào ghi chú.",
        "nhan": "Chưa đủ thông tin",
        "vi_du": ("V26", "Màn hình Xiaomi 15T sáng 3200 nit. Hãng ghi 3200 nit khi màn hình tự tăng sáng dưới ánh sáng "
                         "mạnh. Tuyên bố không nói chế độ nào, và độ sáng điện thoại “Không có mặc định”, nên không biết "
                         "so với số nào. Dừng ở D1a dù con số khớp. Ghi chú mac_dinh=che_do_hien_thi."),
    },
    "D1b": {
        "cau_hoi": "Ở điều kiện vừa xác định (nêu rõ và mặc định), tài liệu có ghi hai số khác nhau không? Có thì dừng, "
                   "dù số của tuyên bố trùng một số hay khác cả hai. Ngoại lệ: số của tuyên bố khớp cả hai (bằng hoặc kém "
                   "hơn cả hai) thì dò tiếp, ghi mau_thuan_khop_ca_hai=<số 1>/<số 2>.",
        "nhan": "Chưa đủ thông tin, tick “Tài liệu mâu thuẫn”",
        "vi_du": ("", "Đồng hồ C dùng 20 giờ khi sử dụng bình thường. Mục Pin ghi “lên đến 20 giờ khi sử dụng bình "
                      "thường”, bảng thông số ghi “lên đến 24 giờ khi sử dụng bình thường”. Cùng điều kiện mà hai chỗ "
                      "ghi hai số, dừng ở D1b kể cả khi số của tuyên bố trùng một trong hai."),
    },
    "D2": {
        # {tu_khang_dinh} do bang_dong_d thay bằng danh sách đọc từ mục 6.2 của hướng dẫn, không chép tay.
        "cau_hoi": "Tuyên bố có từ khẳng định gắn ngay với con số không ({tu_khang_dinh})? Từ ở vế nói việc khác và tên "
                   "tính năng không tính. Chỉ thiếu chữ “lên đến” thì không phải D2. Có thì dừng.",
        "nhan": "Lệch, loại doi_kieu_gia_tri",
        "vi_du": ("V39", "Apple Watch SE 3 luôn dùng đủ 18 giờ mỗi ngày. Hãng ghi “lên đến 18 giờ khi sử dụng bình "
                         "thường”. Hãng hứa tối đa, tuyên bố hứa lúc nào cũng đủ. Bỏ chữ “luôn” thì câu này Đúng ở D3. Ghi chú khang_dinh=luôn."),
    },
    "D3": {
        "cau_hoi": "Ở đúng điều kiện đã xác định ở Bước 3 (gồm mặc định), số của tuyên bố bằng hoặc kém hơn số của hãng "
                   "không? Có thì dừng.",
        "nhan": "Đúng",
        "vi_du": ("V11", "Apple Watch SE 3 dùng đến 32 giờ ở chế độ nguồn điện thấp. Hãng ghi “lên đến 32 giờ ở Chế Độ "
                         "Nguồn Điện Thấp”. Cùng chế độ, 32 bằng 32. Nói 30 giờ cũng Đúng, vì kém hơn số của hãng."),
    },
    "D4": {
        "cau_hoi": "Số của tuyên bố có trùng số hãng ghi cho một điều kiện khác không? Có thì dừng. Gồm cả khi tuyên bố "
                   "không nêu điều kiện và cách hiểu mặc định khác điều kiện của con số (loại bo_dieu_kien).",
        "nhan": "Lệch",
        "vi_du": ("V33", "Apple Watch SE 3 pin 32 giờ. Hãng ghi 18 giờ khi sử dụng bình thường, 32 giờ ở chế độ nguồn "
                         "điện thấp. Tuyên bố không nêu chế độ, đồng hồ có cách hiểu mặc định là chế độ thường (18 giờ), "
                         "nên D3 không khớp; 32 giờ là số có thật của chế độ khác. Loại bo_dieu_kien, ghi chú "
                         "mac_dinh=che_do_nguon,hoat_dong."),
    },
    "D5": {
        "cau_hoi": "Số của tuyên bố có đẹp hơn số hãng ghi ở cùng điều kiện, hoặc đẹp hơn mọi số hãng ghi không? Có thì dừng.",
        "nhan": "Sai",
        "ghi_chu_nho": "Đẹp hơn: pin, độ sáng, tần số quét, zoom, công suất sạc, dung lượng pin, số giờ nghe sau khi sạc "
                       "thì số lớn hơn là đẹp hơn; thời gian sạc (phút) thì số nhỏ hơn là đẹp hơn; kháng nước so theo "
                       "mục 6.6. Mã IP khác nhánh không khớp; không trùng mã nào thì Sai.",
        "vi_du": ("V20", "Xiaomi 15T sạc đầy 100% chỉ trong 40 phút với củ sạc 67W. Hãng ghi 50 phút sạc đầy 100%, cần "
                         "củ 67W trở lên. Cùng điều kiện mà tuyên bố nói nhanh hơn, và 40 phút không có ở đâu trong tài "
                         "liệu. Loại doi_gia_tri."),
    },
    "D6": {
        "cau_hoi": "Tài liệu có số cho thuộc tính, nhưng không có số ở điều kiện này; số của tuyên bố không trùng số nào "
                   "và không đẹp hơn mọi số.",
        "nhan": "Chưa đủ thông tin",
        "vi_du": ("V44", "Galaxy Buds3 Pro nghe nhạc 6,5 giờ ở chế độ xuyên âm. Hãng ghi 7 giờ khi tắt chống ồn, 6 giờ "
                         "khi bật, không có số cho chế độ xuyên âm. 6,5 không trùng số nào (không phải D4) và không cao "
                         "hơn mọi số (cao nhất 7, không phải D5)."),
    },
}

# Thông báo lỗi chung của trang và scripts/kiem_nhan.py ({tên} do bên gọi điền). Lỗi chặn lưu; NHAC chỉ nhắc.
THONG_BAO = {
    "chua_chon_dong": "Chưa bấm “Dừng ở đây” ở bảng D1–D6.",
    "dong_la": "dong_d {dong_d} không thuộc " + ", ".join(MA_DONG_D) + ".",
    "nhan_khong_khop": "Nhãn {nhan} không khớp dòng {dong_d}: dòng {dong_d} phải ra nhãn {nhan_mong} "
                       "(D1, D1a, D1b, D6: CHUA_DU; D2, D4: LECH; D3: DUNG; D5: SAI). Bấm “Dừng ở đây” ở dòng đúng "
                       "để nhãn tự điền lại.",
    "d1_co_bang_chung": "D1 nghĩa là tài liệu không có thông số này, nên bằng chứng và câu trích để trống.",
    "d1b_thieu_tick": "Dòng D1b là tài liệu ghi hai số khác nhau cho cùng điều kiện, nên phải đặt "
                      "tai_lieu_mau_thuan là true (trên trang: tick “Tài liệu mâu thuẫn”). Nếu không phải ca này thì "
                      "bấm “Dừng ở đây” ở dòng khác.",
    "tick_khong_phai_d1b": "Đang đặt tai_lieu_mau_thuan là true (tick “Tài liệu mâu thuẫn”) mà dòng là {dong_d}: chỉ "
                           "dòng D1b mới có. Bỏ tick, hoặc bấm “Dừng ở đây” ở D1b nếu tài liệu thật sự ghi hai số khác "
                           "nhau cho cùng điều kiện.",
    "d2_sai_loai": "Dòng D2 là lệch kiểu giá trị, nên loại phải là doi_kieu_gia_tri (đang là {loai}).",
    "mac_dinh_khong_co": "Ghi chú có mac_dinh={khoa}, mà “{dieu_kien}” không có mặc định: tuyên bố không nói điều kiện "
                         "này thì dừng ở D1a, nhãn Chưa đủ thông tin.",
    "d1a_thieu_nguyen_nhan": "Dòng D1a phải ghi nguyên nhân vào ghi chú: mac_dinh=<khóa “Không có mặc định” của thuộc tính "
                             "này: {ds}> hoặc chua_xac_dinh=<cụm>.",
    "d1a_mac_dinh_co_mac_dinh": "Ghi chú có mac_dinh={khoa}, mà “{dieu_kien}” có cách hiểu mặc định “{hieu}”: dùng mặc "
                                "định rồi dò tiếp, không dừng ở D1a vì khóa này.",
    "d2_thieu_khang_dinh": "Dòng D2 phải ghi từ khẳng định vào ghi chú: khang_dinh=<từ>, với <từ> là một trong: {ds}.",
    "mac_dinh_khoa_la": "Ghi chú có mac_dinh={khoa}, mà “{khoa}” không phải khóa ghi được của thuộc tính này ở bảng mục 5 "
                        "(ghi được: {ds}; hoặc ngoai_bang khi nhãn dựa vào mục 6.7 ý 4). Khóa “như hãng công bố” không ghi.",
    "d2_khang_dinh_la": "Ghi chú có khang_dinh={tu}, mà “{tu}” không có trong danh sách từ khẳng định ở mục 6.2: {ds}.",
    "ly_do_ma_doan": "Lý do chép mã đoạn thay cho câu trích: “{ma}”. Chỗ câu trích là câu nguyên văn từ tài liệu; mã đoạn "
                     "đã nằm ở bằng chứng.",
}
NHAC = {
    "bo_dieu_kien_thieu_mac_dinh": "Loại bo_dieu_kien nghĩa là tuyên bố bỏ điều kiện và bạn đã dùng cách hiểu mặc định; "
                                   "thường cần ghi mac_dinh=… (mục 8).",
    "d1_co_mac_dinh": "Dòng D1 dừng trước khi xét điều kiện, nên không cần ghi mac_dinh=… (mục 8).",
    "trich_thieu_don_vi": "Câu trích không có đơn vị của thuộc tính {thuoc_tinh} ({don_vi}): kiểm lại xem bằng chứng có "
                          "đúng thuộc tính của tuyên bố không.",
}

# Mã ghi chú (hướng dẫn mục 8) mà luật kiểm đọc: mục "ten=a,b" (mac_dinh, khang_dinh) hoặc "ten=cụm" (chua_xac_dinh).
# Cùng biểu thức với JavaScript của trang (RE_MUC) và scripts/kiem_nhan.py.
MUC_MAC_DINH = "mac_dinh"
MUC_KHANG_DINH = "khang_dinh"
MUC_CHUA_XAC_DINH = "chua_xac_dinh"
# Mã đoạn <ma_mau>#<số> nằm trong ngoặc kép của lý do (S14): chỗ ngoặc kép phải là câu trích nguyên văn (mục 8, QT10).
RE_NGOAC_KEP = r'[“"]([^“”"]*)[”"]'
RE_MA_DOAN = r"[a-z]{2}-[a-z0-9-]+#\d+"
# Biểu thức nhận một đơn vị trong câu trích (đã NFC, gộp khoảng trắng, hạ chữ thường): đơn vị đứng độc lập, tức trước
# nó không phải chữ cái và sau nó không phải chữ cái (số thì được, "50m", "20 phút"). Dùng chung cho trang (RegExp) và Python.
CHU_CAI = "A-Za-zÀ-ỹ"

# Cột "Đơn vị" của bảng mục 6.1 -> các dạng viết trong tài liệu (S15). Dạng viết là mảnh biểu thức chính quy, đã hạ chữ thường.
# Giờ, phút, nit, W, mAh, Hz, x, m theo bảng chuẩn hóa đơn vị trong chung.yaml (chuan_hoa.don_vi) và mục 6.1; mã IP,
# ISO 22810 (m, ATM, WR) theo mục 6.6. Ô "Đơn vị" lạ thì thoát (bang_huong_loi), để người sửa hướng dẫn thêm vào đây.
_GIO = ("giờ", "tiếng", "h")
_PHUT = ("phút", "min")
DON_VI_BIEU_DIEN = {
    "giờ": _GIO,
    "phút": _PHUT,
    "W": ("w",),
    "nit": ("nit", "nits", "cd/m²"),
    "Hz": ("hz",),
    "x": ("x",),
    "mã IP": ("ip[x0-9]",),
    "mAh": ("mah",),
    "giờ nghe được": _GIO,
    "phút (dạng 1), giờ (dạng 2)": _PHUT + _GIO,
    "m (ISO 22810)": ("m", "mét", "atm", "wr"),
}

# Cách dịch mã hướng thuận lợi và kiểu giá trị (mục 6.1) sang lời; mã gốc giữ trong ngoặc nhỏ.
LOI_HUONG_THUAN_LOI = {
    "cao_hon_tot_hon": "số lớn hơn là đẹp hơn",
    "thap_hon_tot_hon": "số nhỏ hơn là đẹp hơn",
    "theo_nhanh_ip": "so mã IP theo mục 6.6",
    "theo_dang": "tùy dạng, xem mục 6.1",
}
LOI_KIEU_GIA_TRI = {
    "toi_da": "mức tối đa hãng công bố",
    "dien_hinh": "mức điển hình",
    "nhu_hang_cong_bo": "như hãng công bố",
}

# Ghép hàng có dấu * của bảng mục 5 với hàng bảng mục 5.1 (khảo sát Bước 10). Khóa: (tiền tố nhóm, thuộc tính, tên điều
# kiện bỏ dấu *). Giá trị: các chuỗi (không phân biệt hoa thường) mỗi chuỗi nhận ra đúng một hàng 5.1 qua cột
# "Cách hiểu trong bảng trên". Hàng có dấu * mà thiếu ở đây, hoặc chuỗi không nhận ra đúng một hàng, thì thoát.
GHEP_KHAO_SAT = {
    ("dt", "thoi_luong_pin", "Hoạt động"): ("Điện thoại, hoạt động", "Xem video"),
    ("dt", "do_sang", "Chế độ hiển thị"): ("Điện thoại, chế độ hiển thị",),
    ("tn", "thoi_luong_pin", "Chống ồn"): ("Tai nghe: nghe nhạc",),
    ("tn", "thoi_luong_pin", "Hoạt động"): ("Tai nghe: nghe nhạc",),
    ("dh", "thoi_luong_pin", "Chế độ nguồn"): ("Đồng hồ, chế độ nguồn",),
    ("dh", "thoi_luong_pin", "Hoạt động"): ("Đồng hồ: sử dụng bình thường",),
}
KHONG_CO_MAC_DINH = "khong_co_mac_dinh"


def doc_jsonl(duong):
    with open(duong, encoding="utf-8-sig") as f:
        return [json.loads(dong) for dong in f if dong.strip()]


def cau_hinh_luot(luot=LUOT):
    """Khóa localStorage và tên tệp tải về của trang lượt `luot`. Lượt 2 giữ nguyên tên gốc; lượt khác thêm hậu tố
    _luot<N> vào khóa để không đè dữ liệu lượt 2 trong trình duyệt (tên tệp đã có số lượt)."""
    if not isinstance(luot, int) or isinstance(luot, bool) or luot < 2:
        sys.exit(f"--luot phải là số nguyên từ 2 (lượt 1 theo hướng dẫn bản 1, không sinh bằng script này): {luot!r}")
    hau_to = "" if luot == LUOT else f"_luot{luot}"
    return {"khoa_nhan": KHOA_NHAN + hau_to, "khoa_giao_dien": KHOA_GIAO_DIEN + hau_to,
            "tep_nhan": f"thu_luot{luot}.jsonl", "tep_hoi": f"cau_hoi_nhan_luot{luot}.md"}


def doc_tep_ma(duong):
    """Mã tuyên bố trong tệp chọn (--chon), theo thứ tự trong tệp: mỗi dòng một mã; dòng trống và dòng bắt đầu bằng # bỏ
    qua. Tệp không có mã nào hoặc có mã lặp thì thoát."""
    duong = Path(duong)
    if not duong.exists():
        sys.exit(f"thiếu tệp chọn: {duong}")
    ma = []
    for dong in duong.read_text(encoding="utf-8-sig").splitlines():
        dong = dong.strip()
        if dong and not dong.startswith("#"):
            ma.append(dong)
    lap = sorted({m for m in ma if ma.count(m) > 1})
    if lap:
        sys.exit(f"{duong.name}: mã lặp: {', '.join(lap)}")
    if not ma:
        sys.exit(f"{duong.name}: không có mã tuyên bố nào")
    return ma


def chon_va_xao(tuyen_bo, ma_chon, seed=SEED_XAO):
    """Các tuyên bố có mã trong ma_chon, thứ tự xáo trộn bằng random.Random(seed) trên danh sách đã xếp theo mã (nên chỉ phụ
    thuộc tập mã và seed). Mã không có trong tuyên bố thì thoát."""
    theo_ma = {t["id"]: t for t in tuyen_bo}
    la = sorted(set(ma_chon) - set(theo_ma))
    if la:
        sys.exit(f"mã không có trong {TEP_TUYEN_BO.name}: {', '.join(la)}")
    ds = [theo_ma[m] for m in sorted(set(ma_chon))]
    random.Random(seed).shuffle(ds)
    return ds


# ---------- Đọc hướng dẫn: markdown sang HTML và tách bảng theo mục ----------

_RE_RAO = re.compile(r"^\s*```")
_RE_TIEU_DE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_RE_MUC_SO = re.compile(r"^(\d+(?:\.\d+)*)\.?(?:\s|$)")
_RE_DANH_SACH = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
_RE_KE_NGANG = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
_RE_PHAN_CACH = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
_RE_CODE = re.compile(r"`([^`\n]+)`")
_RE_DAM = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*")
_RE_NGHIENG = re.compile(r"(?<![*\w])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![*\w])")
_RE_GIU_CHO = re.compile(r"\{[^{}]*\}")


def esc(chu):
    """Escape cho nội dung thẻ (không phải giá trị thuộc tính): & < >."""
    return html.escape(chu, quote=False)


def loi_huong_dan(thong_bao):
    sys.exit(f"{TEP_HUONG_DAN.name}: {thong_bao}")


def doc_huong_dan(duong=TEP_HUONG_DAN):
    duong = Path(duong)
    if not duong.exists():
        sys.exit(f"thiếu tệp hướng dẫn: {duong}")
    van_ban = duong.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return unicodedata.normalize("NFC", van_ban)


def _inline(text, ra_html):
    """Inline: `code`, **đậm**, *nghiêng*. ra_html=True: HTML đã escape (escape trước, thay thẻ sau); False: chữ thuần."""
    code = []

    def giu(m):
        code.append(m.group(1))
        return f"\x00{len(code) - 1}\x00"

    t = _RE_CODE.sub(giu, text)
    if ra_html:
        t = esc(t)
        t = _RE_DAM.sub(r"<strong>\1</strong>", t)
        t = _RE_NGHIENG.sub(r"<em>\1</em>", t)
        return re.sub("\x00(\\d+)\x00", lambda m: "<code>" + esc(code[int(m.group(1))]) + "</code>", t)
    t = _RE_DAM.sub(r"\1", t)
    t = _RE_NGHIENG.sub(r"\1", t)
    return re.sub("\x00(\\d+)\x00", lambda m: code[int(m.group(1))], t)


def chuyen_inline(text):
    return _inline(text, True)


def van_ban_thuan(text):
    """Bỏ định dạng inline, giữ chữ."""
    return _inline(text, False)


def html_mau_cau(mau):
    """HTML của mẫu câu, chỗ {…} được tô để dễ thấy."""
    return _RE_GIU_CHO.sub(lambda m: f'<span class="gc">{m.group(0)}</span>', esc(mau))


def tach_o_bang(dong):
    """Các ô của một dòng bảng markdown; `|` trong cặp backtick hoặc viết \\| không tách ô."""
    s = dong.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    o, hien, trong_code, i = [], [], False, 0
    while i < len(s):
        c = s[i]
        if c == "\\" and s[i + 1:i + 2] == "|":
            hien.append("|")
            i += 2
            continue
        if c == "`":
            trong_code = not trong_code
        if c == "|" and not trong_code:
            o.append("".join(hien).strip())
            hien = []
        else:
            hien.append(c)
        i += 1
    if trong_code:  # backtick lẻ: tách thô theo dấu |
        return [x.strip() for x in s.split("|")]
    o.append("".join(hien).strip())
    return o


def la_dong_phan_cach(dong):
    return "|" in dong and bool(_RE_PHAN_CACH.match(dong))


def doc_bang(dong, i):
    """Bảng bắt đầu ở dòng i: (tiêu đề, [(các ô, dòng gốc)], chỉ số dòng sau bảng); None nếu dòng i không mở bảng."""
    if not (dong[i].lstrip().startswith("|") and i + 1 < len(dong) and la_dong_phan_cach(dong[i + 1])):
        return None
    tieu_de, hang, i = tach_o_bang(dong[i]), [], i + 2
    while i < len(dong) and dong[i].lstrip().startswith("|"):
        hang.append((tach_o_bang(dong[i]), dong[i]))
        i += 1
    return tieu_de, hang, i


def cac_bang(dong):
    """Mọi bảng trong danh sách dòng (bỏ qua khối code)."""
    ket_qua, i, trong_rao = [], 0, False
    while i < len(dong):
        if _RE_RAO.match(dong[i]):
            trong_rao = not trong_rao
        elif not trong_rao:
            b = doc_bang(dong, i)
            if b:
                ket_qua.append({"tieu_de": b[0], "dong": b[1]})
                i = b[2]
                continue
        i += 1
    return ket_qua


def noi_dung_muc(md, so_muc):
    """Các dòng của mục có số `so_muc` (ví dụ "5", "6.1"), tính cả mục con, tới tiêu đề cùng cấp hoặc cao hơn."""
    ra, trong_muc, cap, trong_rao = [], False, 0, False
    for d in md.split("\n"):
        la_rao = bool(_RE_RAO.match(d))
        if la_rao:
            trong_rao = not trong_rao
        m = None if (la_rao or trong_rao) else _RE_TIEU_DE.match(d)
        if m and trong_muc and len(m.group(1)) <= cap:
            break
        if m and not trong_muc:
            s = _RE_MUC_SO.match(m.group(2))
            if s and s.group(1) == so_muc:
                trong_muc, cap = True, len(m.group(1))
            continue
        if trong_muc:
            ra.append(d)
    if not trong_muc:
        loi_huong_dan(f"không thấy mục {so_muc} (tiêu đề dạng '## {so_muc}. ...')")
    return ra


def _ten_cot(c):
    return unicodedata.normalize("NFC", van_ban_thuan(c)).strip().casefold()


def tim_bang(md, so_muc, cot):
    """Bảng trong mục `so_muc` có đúng các cột `cot`; trả về [{tên cột: ô (markdown)}].

    Không thấy bảng, số cột khác, hoặc có dòng sai số ô thì thoát với thông báo nói rõ mục và bảng nào.
    """
    bang = cac_bang(noi_dung_muc(md, so_muc))
    can = [_ten_cot(c) for c in cot]
    for b in bang:
        ten = [_ten_cot(c) for c in b["tieu_de"]]
        if not all(c in ten for c in can):
            continue
        if len(ten) != len(can):
            loi_huong_dan(f"mục {so_muc}: bảng ({', '.join(cot)}) có {len(ten)} cột "
                          f"({', '.join(b['tieu_de'])}), cần đúng {len(can)} cột")
        if not b["dong"]:
            loi_huong_dan(f"mục {so_muc}: bảng ({', '.join(cot)}) không có dòng dữ liệu nào")
        vi_tri = [ten.index(c) for c in can]
        ket_qua = []
        for o, goc in b["dong"]:
            if len(o) != len(ten):
                loi_huong_dan(f"mục {so_muc}: dòng bảng có {len(o)} ô, bảng có {len(ten)} cột: {goc.strip()[:90]}")
            ket_qua.append({c: o[v] for c, v in zip(cot, vi_tri)})
        return ket_qua
    co = "; ".join("(" + ", ".join(b["tieu_de"]) + ")" for b in bang) or "không có bảng nào"
    loi_huong_dan(f"không thấy bảng có các cột ({', '.join(cot)}) trong mục {so_muc}; bảng có trong mục: {co}")


def _tao_id(chu, da_dung):
    m = _RE_MUC_SO.match(chu)
    if m:
        goc = "hd-muc-" + m.group(1).replace(".", "-")
    else:
        t = unicodedata.normalize("NFD", chu.lower().replace("đ", "d"))
        t = "".join(c for c in t if not unicodedata.combining(c))
        goc = "hd-" + (re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "muc")
    ten, k = goc, 2
    while ten in da_dung:
        ten, k = f"{goc}-{k}", k + 1
    da_dung.add(ten)
    return ten


def _bat_dau_khoi(dong, i):
    """Dòng i mở một khối khác đoạn văn (khối code, tiêu đề, bảng, dòng kẻ, mục danh sách)."""
    d = dong[i]
    return bool(_RE_RAO.match(d) or _RE_TIEU_DE.match(d) or _RE_KE_NGANG.match(d) or _RE_DANH_SACH.match(d)
                or doc_bang(dong, i))


def _html_nhom_danh_sach(nut):
    ra, k = [], 0
    while k < len(nut):
        j = k
        while j < len(nut) and nut[j]["co_so"] == nut[k]["co_so"]:
            j += 1
        nhom = nut[k:j]
        tag = "ol" if nhom[0]["co_so"] else "ul"
        bat_dau = f' start="{nhom[0]["so"]}"' if tag == "ol" and nhom[0]["so"] not in (None, 1) else ""
        li = "".join(f"<li>{chuyen_inline(x['text'])}{_html_nhom_danh_sach(x['con']) if x['con'] else ''}</li>"
                     for x in nhom)
        ra.append(f"<{tag}{bat_dau}>{li}</{tag}>")
        k = j
    return "".join(ra)


def _html_danh_sach(muc):
    cay = []
    for m in muc:
        nut = dict(m, con=[])
        if m["cap"] == 0 or not cay:
            cay.append(nut)
        else:
            cay[-1]["con"].append(nut)
    return _html_nhom_danh_sach(cay)


def _chuyen(md):
    """(HTML, [(cấp, id, chữ tiêu đề)]) của một văn bản markdown tối giản."""
    dong = md.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ra, tieu_de, da_dung, i, n = [], [], set(), 0, len(dong)
    while i < n:
        d = dong[i]
        if not d.strip():
            i += 1
            continue
        if _RE_RAO.match(d):
            code, i = [], i + 1
            while i < n and not _RE_RAO.match(dong[i]):
                code.append(dong[i])
                i += 1
            i += 1  # dòng đóng khối (hoặc hết tệp)
            ra.append("<pre><code>" + esc("\n".join(code)) + "</code></pre>")
            continue
        m = _RE_TIEU_DE.match(d)
        if m:
            cap, chu = len(m.group(1)), van_ban_thuan(m.group(2))
            ma = _tao_id(chu, da_dung)
            tieu_de.append((cap, ma, chu))
            ra.append(f'<h{cap} id="{ma}">{chuyen_inline(m.group(2))}</h{cap}>')
            i += 1
            continue
        if _RE_KE_NGANG.match(d):
            ra.append("<hr>")
            i += 1
            continue
        b = doc_bang(dong, i)
        if b:
            tieu, hang, i = b
            ra.append('<div class="cuon-ngang"><table><thead><tr>'
                      + "".join(f"<th>{chuyen_inline(c)}</th>" for c in tieu) + "</tr></thead><tbody>"
                      + "".join("<tr>" + "".join(f"<td>{chuyen_inline(c)}</td>" for c in o) + "</tr>" for o, _ in hang)
                      + "</tbody></table></div>")
            continue
        if _RE_DANH_SACH.match(d):
            muc = []
            while i < n:
                m = _RE_DANH_SACH.match(dong[i])
                if m:
                    dau = m.group(2)
                    muc.append({"cap": 0 if len(m.group(1).expandtabs(4)) < 2 else 1, "co_so": dau[0].isdigit(),
                                "so": int(dau[:-1]) if dau[0].isdigit() else None, "text": m.group(3).strip()})
                elif muc and dong[i].strip() and dong[i][:1] in " \t" and not _bat_dau_khoi(dong, i):
                    muc[-1]["text"] += " " + dong[i].strip()  # dòng thụt vào tiếp nối mục trước
                else:
                    break
                i += 1
            ra.append(_html_danh_sach(muc))
            continue
        doan = [d.strip()]
        i += 1
        while i < n and dong[i].strip() and not _bat_dau_khoi(dong, i):
            doan.append(dong[i].strip())
            i += 1
        ra.append("<p>" + chuyen_inline(" ".join(doan)) + "</p>")
    return "\n".join(ra), tieu_de


def chuyen_markdown(md):
    """HTML (đã escape) của markdown tối giản: tiêu đề #..######, đoạn văn, danh sách (lồng một cấp), bảng, ```code```,
    `code`, **đậm**, *nghiêng*. Tiêu đề có id: mục đánh số "5." -> hd-muc-5, "6.1" -> hd-muc-6-1."""
    return _chuyen(md)[0]


# ---------- Các bảng của hướng dẫn mà trang dùng ----------

def _ma_trong_backtick(o):
    m = re.search(r"`([A-Za-z0-9_]+)`", o)
    return m.group(1) if m else ""


def _nhom_theo_ten(ten, noi):
    ten = unicodedata.normalize("NFC", van_ban_thuan(ten)).strip()
    for tien_to, t in NHOM_THEO_TIEN_TO.items():
        if t == ten:
            return tien_to
    loi_huong_dan(f"{noi}: nhóm '{ten}' không thuộc {', '.join(NHOM_THEO_TIEN_TO.values())}")


def _hang_ke_thua(hang, noi):
    """Với bảng mà ô Nhóm, Thuộc tính để trống thì kế thừa hàng trên: [(tiền tố nhóm, mã thuộc tính, hàng)]."""
    ra, nhom, thuoc_tinh = [], "", ""
    for k, h in enumerate(hang, 1):
        if h["Nhóm"].strip():
            nhom = _nhom_theo_ten(h["Nhóm"], f"{noi}, dòng {k}")
            if not h["Thuộc tính"].strip():
                loi_huong_dan(f"{noi}, dòng {k}: có ô Nhóm nhưng ô Thuộc tính trống")
        if h["Thuộc tính"].strip():
            thuoc_tinh = _ma_trong_backtick(h["Thuộc tính"])
            if not thuoc_tinh:
                loi_huong_dan(f"{noi}, dòng {k}: ô Thuộc tính phải có mã trong dấu backtick: {h['Thuộc tính'][:60]}")
        if not nhom or not thuoc_tinh:
            loi_huong_dan(f"{noi}, dòng {k}: chưa có nhóm hoặc thuộc tính để kế thừa")
        ra.append((nhom, thuoc_tinh, h))
    return ra


def bang_nhan(md):
    """{mã nhãn: {ten, dinh_nghia}} từ bảng "Nhãn | Mã | Định nghĩa" ở mục 3."""
    ra = {}
    for h in tim_bang(md, "3", ("Nhãn", "Mã", "Định nghĩa")):
        ra[_ma_trong_backtick(h["Mã"])] = {"ten": van_ban_thuan(h["Nhãn"]).strip(),
                                           "dinh_nghia": van_ban_thuan(h["Định nghĩa"]).strip()}
    thieu = [m for m in MA_NHAN if m not in ra]
    if thieu:
        loi_huong_dan(f"mục 3: bảng nhãn thiếu mã {', '.join(thieu)}")
    return ra


def bang_loai(md):
    """[{ma, giai_thich}] từ bảng "Mã | Khi nào" (loại biến đổi) ở mục 8; phải đủ 6 loại."""
    ra = [{"ma": _ma_trong_backtick(h["Mã"]), "giai_thich": van_ban_thuan(h["Khi nào"]).strip()}
          for h in tim_bang(md, "8", ("Mã", "Khi nào"))]
    thieu = [m for m in MA_LOAI if m not in {x["ma"] for x in ra}]
    if thieu:
        loi_huong_dan(f"mục 8: bảng loại biến đổi thiếu mã {', '.join(thieu)}")
    return ra


def bang_mau_cau(md):
    """{mã dòng D: mẫu câu (chữ thuần, bỏ cặp nháy kép ngoài cùng)} từ bảng "Dòng | Mẫu câu" ở mục 8."""
    ra = {}
    for h in tim_bang(md, "8", ("Dòng", "Mẫu câu")):
        mau = van_ban_thuan(h["Mẫu câu"]).strip()
        if len(mau) >= 2 and mau[0] == '"' and mau[-1] == '"':
            mau = mau[1:-1]
        ra[van_ban_thuan(h["Dòng"]).strip()] = mau
    return ra


def _kiem_nhan_dong_d(ma, nhan_md):
    """Nhãn ở bảng mục 7 của dòng `ma` phải khớp bảng suy nhãn NHAN_THEO_DONG (và loại, tick của D2, D1b)."""
    chu = van_ban_thuan(nhan_md).strip()
    ten = TEN_NHAN_TRONG_HUONG_DAN[NHAN_THEO_DONG[ma]]
    loi = []
    if not chu.startswith(ten):
        loi.append(f"nhãn '{chu}' không bắt đầu bằng '{ten}'")
    if ma in LOAI_THEO_DONG and LOAI_THEO_DONG[ma] not in chu:
        loi.append(f"thiếu loại {LOAI_THEO_DONG[ma]}")
    if (ma == DONG_TICK_MAU_THUAN) != ("tai_lieu_mau_thuan = true" in chu):
        loi.append("tai_lieu_mau_thuan = true chỉ được ghi ở dòng " + DONG_TICK_MAU_THUAN)
    if loi:
        loi_huong_dan(f"mục 7, dòng {ma}: {'; '.join(loi)}. Bảng NHAN_THEO_DONG trong scripts/{Path(__file__).name} "
                      f"(nhãn tự điền khi bấm \"Dừng ở đây\") phải khớp bảng này; sửa một bên cho khớp.")


def bang_dong_d(md):
    """[{ma, kiem_tra_html, nhan_html, luu_y_html, mau_cau, mau_cau_html, cau_hoi, nhan_hien_thi, nhan_ma, loai_tu_dong,
    tu_tick, ghi_chu_nho, vi_du_ma, vi_du}] cho từng dòng D1..D6: bảng mục 7 ghép với bảng mẫu câu mục 8 theo mã dòng và
    với chữ hiện trên trang (DONG_D_HIEN_THI). Dòng D không có mẫu câu thì thoát (nút "Chèn mẫu câu" sẽ không có gì để
    chèn); bảng mục 7 phải đủ MA_DONG_D và nhãn của từng dòng phải khớp NHAN_THEO_DONG."""
    mau = bang_mau_cau(md)
    ra = []
    for h in tim_bang(md, "7", ("Dòng", "Kiểm tra", "Nhãn", "Lưu ý cho người gán")):
        ma = van_ban_thuan(h["Dòng"]).strip()
        if ma not in mau:
            loi_huong_dan(f"mục 7 có dòng {ma} nhưng bảng mẫu câu ở mục 8 không có mẫu cho dòng này "
                          f"(các mã có mẫu: {', '.join(mau)})")
        if ma not in NHAN_THEO_DONG or ma not in DONG_D_HIEN_THI:
            loi_huong_dan(f"mục 7 có dòng {ma} nhưng scripts/{Path(__file__).name} không khai báo dòng này "
                          f"(các dòng đã khai báo: {', '.join(MA_DONG_D)})")
        _kiem_nhan_dong_d(ma, h["Nhãn"])
        hien = DONG_D_HIEN_THI[ma]
        ra.append({"ma": ma, "kiem_tra_html": chuyen_inline(h["Kiểm tra"]), "nhan_html": chuyen_inline(h["Nhãn"]),
                   "luu_y_html": chuyen_inline(h["Lưu ý cho người gán"]), "mau_cau": mau[ma],
                   "mau_cau_html": html_mau_cau(mau[ma]), "cau_hoi": hien["cau_hoi"], "nhan_hien_thi": hien["nhan"],
                   "nhan_ma": NHAN_THEO_DONG[ma], "loai_tu_dong": LOAI_THEO_DONG.get(ma, ""),
                   "tu_tick": ma == DONG_TICK_MAU_THUAN, "ghi_chu_nho": hien.get("ghi_chu_nho", ""),
                   "vi_du_ma": hien["vi_du"][0], "vi_du": hien["vi_du"][1]})
    thieu = [m for m in MA_DONG_D if m not in {d["ma"] for d in ra}]
    if thieu:
        loi_huong_dan(f"mục 7: bảng thiếu dòng {', '.join(thieu)}")
    return ra


def _khoa_cau_hinh(o, noi):
    """[{khoa, gia_tri}] từ ô Khóa cấu hình: các cụm `khoa: gia_tri` cách nhau dấu phẩy."""
    ra = []
    for phan in o.split(","):
        phan = phan.strip().strip("`").strip()
        if not phan:
            continue
        khoa, dau, gia_tri = phan.partition(":")
        if not dau or not khoa.strip() or not gia_tri.strip():
            loi_huong_dan(f"{noi}: ô Khóa cấu hình phải có dạng `khoa: gia_tri`, đang là: {o[:80]}")
        ra.append({"khoa": khoa.strip(), "gia_tri": gia_tri.strip()})
    return ra


def _chuan_so_khop(chu):
    return unicodedata.normalize("NFC", chu).casefold()


def bang_khao_sat(md):
    """Các hàng bảng mục 5.1 (đối chiếu khảo sát Bước 10): [{cach_hieu, hieu_khac, quyet_dinh_html}]."""
    return [{"cach_hieu": van_ban_thuan(h["Cách hiểu trong bảng trên"]).strip(),
             "hieu_khac": van_ban_thuan(h["Hiểu khác"]).strip(), "quyet_dinh_html": chuyen_inline(h["Quyết định"])}
            for h in tim_bang(md, "5.1", ("Cách hiểu trong bảng trên", "Hiểu khác", "Quyết định"))]


def _ghep_khao_sat(hang, khao_sat):
    """Gắn khóa "khao_sat" ([{hieu_khac, quyet_dinh_html}]) vào các hàng mục 5 có dấu *, theo GHEP_KHAO_SAT.

    Thoát nếu: hàng có dấu * mà GHEP_KHAO_SAT không có; mục của GHEP_KHAO_SAT không còn hàng mục 5 tương ứng (có dấu *);
    một chuỗi nhận ra không trúng hàng mục 5.1 nào hoặc trúng nhiều hơn một hàng."""
    co_sao = {(h["nhom"], h["thuoc_tinh"], h["dieu_kien"]) for h in hang if h["co_sao"]}
    thieu = sorted(co_sao - set(GHEP_KHAO_SAT))
    if thieu:
        loi_huong_dan("mục 5: hàng có dấu * chưa có trong bảng ghép với mục 5.1 (GHEP_KHAO_SAT trong "
                      f"scripts/{Path(__file__).name}): " + "; ".join(", ".join(k) for k in thieu))
    thua = sorted(set(GHEP_KHAO_SAT) - co_sao)
    if thua:
        loi_huong_dan("bảng ghép với mục 5.1 (GHEP_KHAO_SAT) có hàng không còn dấu * ở mục 5: "
                      + "; ".join(", ".join(k) for k in thua))
    for h in hang:
        h["khao_sat"] = []
        if not h["co_sao"]:
            continue
        khoa = (h["nhom"], h["thuoc_tinh"], h["dieu_kien"])
        da_ghep = []
        for chuoi in GHEP_KHAO_SAT[khoa]:
            trung = [k for k in khao_sat if _chuan_so_khop(chuoi) in _chuan_so_khop(k["cach_hieu"])]
            if len(trung) != 1:
                loi_huong_dan(f"mục 5.1: chuỗi '{chuoi}' (ghép cho {', '.join(khoa)}) trúng {len(trung)} hàng, cần đúng 1 "
                              f"(cột 'Cách hiểu trong bảng trên')")
            if trung[0]["cach_hieu"] not in da_ghep:
                da_ghep.append(trung[0]["cach_hieu"])
                h["khao_sat"].append({"hieu_khac": trung[0]["hieu_khac"], "quyet_dinh_html": trung[0]["quyet_dinh_html"]})


def bang_mac_dinh(md):
    """Các hàng bảng mục 5 (cách hiểu mặc định), ô Nhóm và Thuộc tính trống thì kế thừa hàng trên.

    Mỗi hàng có dieu_kien (chữ thuần, bỏ dấu *), hieu (chữ thuần của cột "Không nêu thì hiểu là"), co_sao, khoa
    [{khoa, gia_tri}] và khao_sat (hàng có dấu * ghép với bảng 5.1, xem GHEP_KHAO_SAT)."""
    hang = tim_bang(md, "5", ("Nhóm", "Thuộc tính", "Điều kiện", "Không nêu thì hiểu là", "Khóa cấu hình"))
    ra = []
    for k, (nhom, thuoc_tinh, h) in enumerate(_hang_ke_thua(hang, "mục 5"), 1):
        dieu_kien = unicodedata.normalize("NFC", van_ban_thuan(h["Điều kiện"])).strip()
        ra.append({"nhom": nhom, "thuoc_tinh": thuoc_tinh, "dieu_kien": dieu_kien.rstrip("*").strip(),
                   "co_sao": dieu_kien.endswith("*"), "dieu_kien_html": chuyen_inline(h["Điều kiện"]),
                   "hieu_html": chuyen_inline(h["Không nêu thì hiểu là"]),
                   "hieu": van_ban_thuan(h["Không nêu thì hiểu là"]).strip(),
                   "khoa": _khoa_cau_hinh(h["Khóa cấu hình"], f"mục 5, dòng {k}")})
    _ghep_khao_sat(ra, bang_khao_sat(md))
    for h in ra:
        gia_tri = {k["gia_tri"] for k in h["khoa"]}
        if KHONG_CO_MAC_DINH in gia_tri and len(gia_tri) > 1:
            loi_huong_dan(f"mục 5: hàng '{h['dieu_kien']}' ({h['nhom']}, {h['thuoc_tinh']}) vừa có khóa "
                          f"{KHONG_CO_MAC_DINH} vừa có khóa khác; tách thành hai hàng")
    return ra


def khoa_khong_co_mac_dinh(hang_mac_dinh):
    """{(tiền tố nhóm, thuộc tính): {khóa cấu hình: tên điều kiện}} của các khóa ghi khong_co_mac_dinh ở bảng mục 5.
    Dùng chung cho trang và scripts/kiem_nhan.py (quy tắc: ghi chú mac_dinh=<khóa> thì phải dừng ở D1a)."""
    ra = {}
    for h in hang_mac_dinh:
        for k in h["khoa"]:
            if k["gia_tri"] == KHONG_CO_MAC_DINH:
                ra.setdefault((h["nhom"], h["thuoc_tinh"]), {})[k["khoa"]] = h["dieu_kien"]
    return ra


def khoa_co_mac_dinh(hang_mac_dinh):
    """{(tiền tố nhóm, thuộc tính): {khóa cấu hình: {dieu_kien, hieu}}} của các khóa CÓ cách hiểu mặc định (kể cả "như hãng
    công bố") ở bảng mục 5. Dùng cho quy tắc D1a: ghi chú chỉ có khóa loại này thì không đủ nguyên nhân dừng ở D1a."""
    ra = {}
    for h in hang_mac_dinh:
        for k in h["khoa"]:
            if k["gia_tri"] != KHONG_CO_MAC_DINH:
                ra.setdefault((h["nhom"], h["thuoc_tinh"]), {})[k["khoa"]] = {"dieu_kien": h["dieu_kien"], "hieu": h["hieu"]}
    return ra


KHOA_NGOAI_BANG = "ngoai_bang"  # mac_dinh=ngoai_bang: nhãn dựa vào mục 6.7 ý 4 (QĐ10, 02/11), điều kiện ngoài bảng mục 5


def khoa_ghi_duoc(hang_mac_dinh):
    """{(tiền tố nhóm, thuộc tính): [khóa]} các khóa được ghi vào mac_dinh= theo mục 8: khóa của bảng mục 5 cho nhóm và thuộc
    tính đó, trừ khóa "như hãng công bố" (kể cả khóa "không có mặc định"). Cộng thêm KHOA_NGOAI_BANG ở mọi thuộc tính."""
    ra = {}
    for h in hang_mac_dinh:
        for k in h["khoa"]:
            if k["gia_tri"] != "nhu_hang_cong_bo":
                ds = ra.setdefault((h["nhom"], h["thuoc_tinh"]), [])
                if k["khoa"] not in ds:
                    ds.append(k["khoa"])
    return ra


def ten_thuoc_tinh(md):
    """{"<tiền tố nhóm>|<mã thuộc tính>": tên tiếng Việt} từ ô Thuộc tính của bảng mục 5 (ví dụ "Thời lượng pin
    (`thoi_luong_pin`)" -> "Thời lượng pin"). Dùng cho câu hỏi D1: tên thuộc tính ghi sẵn trên tuyên bố."""
    hang = tim_bang(md, "5", ("Nhóm", "Thuộc tính", "Điều kiện", "Không nêu thì hiểu là", "Khóa cấu hình"))
    ra = {}
    for nhom, thuoc_tinh, h in _hang_ke_thua(hang, "mục 5"):
        o = h["Thuộc tính"].strip()
        if not o:
            continue
        m = re.match(r"^(.*?)\s*\(\s*`[A-Za-z0-9_]+`\s*\)", o)
        ten = van_ban_thuan(m.group(1)).strip() if m else ""
        if not ten:
            loi_huong_dan(f"mục 5: ô Thuộc tính '{o[:60]}' phải có dạng 'Tên (`ma_thuoc_tinh`)'")
        ra[f"{nhom}|{thuoc_tinh}"] = ten
    return ra


_RE_TRONG_NGOAC = re.compile(r'["“]([^"“”]+)["”]')


def tu_khang_dinh(md):
    """Từ khẳng định đọc từ mục 6.2 của hướng dẫn (không chép tay): {"chac_chan": ["luôn", ...], "muc_san": ["hơn <số>",
    ...], "tu_hop_le": [...]}. tu_hop_le là các từ được ghi vào khang_dinh=<từ>: nhóm chắc chắn nguyên chữ, nhóm mức sàn bỏ
    chỗ <số> ("hơn <số>" -> "hơn", "<số> trở lên" -> "trở lên")."""
    dong = noi_dung_muc(md, "6.2")
    ra = {}
    for khoa, nhan in (("chac_chan", "Nhóm chắc chắn:"), ("muc_san", "Nhóm mức sàn:")):
        van = next((d.split(nhan, 1)[1] for d in dong if nhan in d), None)
        if van is None:
            loi_huong_dan(f"mục 6.2: không thấy dòng '{nhan}'")
        ra[khoa] = [unicodedata.normalize("NFC", x).strip() for x in _RE_TRONG_NGOAC.findall(van.strip().split(". ")[0])]
        if not ra[khoa]:
            loi_huong_dan(f"mục 6.2: dòng '{nhan}' không có từ nào trong dấu nháy kép")
    tu = list(ra["chac_chan"])
    for cum in ra["muc_san"]:
        tu.append(cum.replace("<số>", "").strip())
    ra["tu_hop_le"] = list(dict.fromkeys(t for t in tu if t))
    return ra


def mau_don_vi(don_vi, noi):
    """Biểu thức chính quy (chuỗi dùng chung cho Python và JavaScript, áp lên chuỗi đã hạ chữ thường) nhận đơn vị của cột
    "Đơn vị" mục 6.1 trong câu trích. Ô lạ thì thoát."""
    if don_vi not in DON_VI_BIEU_DIEN:
        loi_huong_dan(f"{noi}: đơn vị '{don_vi}' chưa có cách nhận trong câu trích (DON_VI_BIEU_DIEN trong "
                      f"scripts/{Path(__file__).name}; các đơn vị đã biết: {', '.join(DON_VI_BIEU_DIEN)})")
    return f"(?:^|[^{CHU_CAI}])(?:{'|'.join(DON_VI_BIEU_DIEN[don_vi])})(?![{CHU_CAI}])"


def _ma_huong_loi(o, bang_loi, noi):
    ma = _ma_trong_backtick(o)
    if ma not in bang_loi:
        loi_huong_dan(f"{noi}: mã '{ma}' trong ô '{o[:60]}' chưa có cách dịch sang lời (các mã đã biết: "
                      f"{', '.join(bang_loi)})")
    return ma


def bang_huong_loi(md):
    """Các hàng bảng mục 6.1 (đơn vị, hướng thuận lợi, kiểu giá trị mặc định), kèm mã và lời dịch của từng ô; don_vi_mau
    là biểu thức nhận đơn vị trong câu trích (mau_don_vi)."""
    hang = tim_bang(md, "6.1", ("Nhóm", "Thuộc tính", "Đơn vị", "Hướng thuận lợi", "Kiểu giá trị mặc định"))
    ra = []
    for k, (nhom, thuoc_tinh, h) in enumerate(_hang_ke_thua(hang, "mục 6.1"), 1):
        huong = _ma_huong_loi(h["Hướng thuận lợi"], LOI_HUONG_THUAN_LOI, f"mục 6.1, dòng {k}")
        kieu = _ma_huong_loi(h["Kiểu giá trị mặc định"], LOI_KIEU_GIA_TRI, f"mục 6.1, dòng {k}")
        don_vi = van_ban_thuan(h["Đơn vị"]).strip()
        ra.append({"nhom": nhom, "thuoc_tinh": thuoc_tinh, "don_vi": don_vi,
                   "don_vi_mau": mau_don_vi(don_vi, f"mục 6.1, dòng {k}"),
                   "huong_html": chuyen_inline(h["Hướng thuận lợi"]),
                   "kieu_html": chuyen_inline(h["Kiểu giá trị mặc định"]), "huong_ma": huong,
                   "huong_loi": LOI_HUONG_THUAN_LOI[huong], "kieu_ma": kieu, "kieu_loi": LOI_KIEU_GIA_TRI[kieu]})
    return ra


_RE_CHU_TRONG_NHAY = re.compile(r'"([^"]+)"')
# Mục "Nhóm cụm" của bảng 13.1 -> khóa trong chung.yaml. Hàng nào của 13.1 hiện ở khung "Cụm điều kiện đã biết" thì
# cum_ap_dung (JavaScript) quyết định theo thuộc tính đang gán.
KHOA_CUM_CHUNG = ("kieu_gia_tri", "tu_goi_muc_cao", "cum_quan_he", "ngu_canh_khong_quyet_dinh")
PHU_LUC_NHOM = {"13.2": "dt", "13.3": "tn", "13.4": "dh"}


def _cac_cum(o):
    """Các cụm trong dấu nháy kép của một ô phụ lục; "–" hoặc ô trống là không có cụm."""
    return [unicodedata.normalize("NFC", x).strip() for x in _RE_CHU_TRONG_NHAY.findall(o)]


def bang_cum(md):
    """Phụ lục mục 13 (cụm diễn đạt trong cấu hình, sinh từ YAML): {"chung": [...], "nhom": {"dt": [...], "tn": [...],
    "dh": [...]}}. chung: [{khoa, dong: [{muc_con, tu_tai_lieu, hieu_biet_chung}]}] từ bảng 13.1. nhom: [{khoa (mã điều
    kiện), gia_tri: [{gia_tri, tu_tai_lieu, hieu_biet_chung}]}] từ bảng 13.2 (điện thoại), 13.3 (tai nghe), 13.4 (đồng hồ);
    ô Điều kiện trống thì kế thừa hàng trên."""
    cot_cum = ("Chữ trong tài liệu (`tu_tai_lieu`)", "Cách nói thường gặp (`hieu_biet_chung`)")
    chung, thu_tu = {}, []
    for h in tim_bang(md, "13.1", ("Nhóm cụm", "Mục con") + cot_cum):
        if h["Nhóm cụm"].strip():
            khoa = _ma_trong_backtick(h["Nhóm cụm"])
            if khoa not in KHOA_CUM_CHUNG:
                loi_huong_dan(f"mục 13.1: nhóm cụm '{h['Nhóm cụm'][:60]}' có mã '{khoa}', ngoài {', '.join(KHOA_CUM_CHUNG)}")
            chung[khoa] = []
            thu_tu.append(khoa)
        if not thu_tu:
            loi_huong_dan("mục 13.1: dòng đầu của bảng chưa có ô Nhóm cụm")
        chung[thu_tu[-1]].append({"muc_con": van_ban_thuan(h["Mục con"]).strip(),
                                  "tu_tai_lieu": _cac_cum(h[cot_cum[0]]), "hieu_biet_chung": _cac_cum(h[cot_cum[1]])})
    thieu = [k for k in KHOA_CUM_CHUNG if k not in chung]
    if thieu:
        loi_huong_dan(f"mục 13.1: thiếu nhóm cụm {', '.join(thieu)}")
    nhom = {}
    for muc, tien_to in PHU_LUC_NHOM.items():
        ra, dieu_kien = [], None
        for h in tim_bang(md, muc, ("Điều kiện", "Giá trị") + cot_cum):
            if h["Điều kiện"].strip():
                ma = _ma_trong_backtick(h["Điều kiện"])
                if not ma:
                    loi_huong_dan(f"mục {muc}: ô Điều kiện phải có mã trong dấu backtick: {h['Điều kiện'][:60]}")
                dieu_kien = {"khoa": ma, "gia_tri": []}
                ra.append(dieu_kien)
            if dieu_kien is None:
                loi_huong_dan(f"mục {muc}: dòng đầu của bảng chưa có ô Điều kiện")
            gia_tri = _ma_trong_backtick(h["Giá trị"])
            if not gia_tri:
                loi_huong_dan(f"mục {muc}: ô Giá trị phải có mã trong dấu backtick: {h['Giá trị'][:60]}")
            # "(chỉ `thoi_luong_pin`)" sau mã giá trị: khóa chi_thuoc_tinh của YAML (cụm chỉ là điều kiện của các thuộc tính đó)
            chi = re.search(r"\(chỉ ((?:`[A-Za-z0-9_]+`(?:, )?)+)\)", h["Giá trị"])
            dieu_kien["gia_tri"].append({"gia_tri": gia_tri, "tu_tai_lieu": _cac_cum(h[cot_cum[0]]),
                                         "hieu_biet_chung": _cac_cum(h[cot_cum[1]]),
                                         "chi_thuoc_tinh": re.findall(r"`([A-Za-z0-9_]+)`", chi.group(1)) if chi else []})
        nhom[tien_to] = ra
    return {"chung": [{"khoa": k, "dong": chung[k]} for k in KHOA_CUM_CHUNG], "nhom": nhom}


def dung_huong_dan(md):
    """Phần hướng dẫn nhúng vào trang: toàn văn đã chuyển HTML cùng các bảng đã tách."""
    html_day_du, tieu_de = _chuyen(md)
    muc_luc = "".join(f'<a href="#{ma}">{esc(chu)}</a>' for cap, ma, chu in tieu_de if cap == 2)
    tu_kd = tu_khang_dinh(md)
    ds_tu = ", ".join(f"“{x}”" for x in tu_kd["chac_chan"] + tu_kd["muc_san"])
    dong_d = bang_dong_d(md)
    for d in dong_d:  # chỗ giữ chỗ của câu hỏi D2: danh sách từ lấy từ mục 6.2 (chỗ {thuoc_tinh} của D1 để trang thay)
        d["cau_hoi"] = d["cau_hoi"].replace("{tu_khang_dinh}", ds_tu)
    return {"html": html_day_du, "muc_luc_html": f'<nav class="muc-luc">{muc_luc}</nav>',
            "nhom": NHOM_THEO_TIEN_TO, "nhan": bang_nhan(md), "loai": bang_loai(md), "dong_d": dong_d,
            "mac_dinh": bang_mac_dinh(md), "huong_loi": bang_huong_loi(md), "tu_khang_dinh": tu_kd,
            "ten_thuoc_tinh": ten_thuoc_tinh(md), "cum": bang_cum(md)}


# ---------- Dữ liệu và HTML ----------

def doan_nhung(d):
    """Đoạn nhúng vào trang. noi_dung_goc chỉ nhúng khi khác noi_dung (đoạn đã bỏ số chú thích) để trang không phình ra."""
    x = {"id": d["id"], "noi_dung": d["noi_dung"], "chu_thich": list(d.get("chu_thich") or [])}
    if d.get("noi_dung_goc", d["noi_dung"]) != d["noi_dung"]:
        x["noi_dung_goc"] = d["noi_dung_goc"]
    return x


def nap_du_lieu(luot=LUOT, ma_chon=None, seed_xao=SEED_XAO):
    """Dữ liệu nhúng vào HTML; thoát với thông báo rõ nếu thiếu tệp hoặc hướng dẫn sai cấu trúc.

    luot: lượt gán của trang (khóa lưu, tên tệp tải về). ma_chon: nếu có, chỉ đưa các tuyên bố có mã này vào, thứ tự xáo
    trộn theo seed_xao; bài quảng cáo và đoạn tài liệu cũng chỉ của các tuyên bố đó. Không nhúng nhãn nào."""
    cau_hinh = cau_hinh_luot(luot)
    tuyen_bo = [{k: t.get(k, "") for k in TRUONG_TUYEN_BO} for t in doc_jsonl(TEP_TUYEN_BO)]
    if ma_chon is not None:
        tuyen_bo = chon_va_xao(tuyen_bo, ma_chon, seed_xao)
    bai, doan, thieu = {}, {}, []
    for ma_qc in sorted({t["ma_qc"] for t in tuyen_bo}):
        duong = THU_MUC_QC / f"{ma_qc}.json"
        if not duong.exists():
            thieu.append(str(duong))
            continue
        b = json.loads(duong.read_text(encoding="utf-8"))
        bai[ma_qc] = {"noi_dung": b["noi_dung"], "ten_nhap": b.get("ten_nhap", "")}
    for ma_mau in sorted({t["ma_mau"] for t in tuyen_bo}):
        duong = THU_MUC_NGUON / ma_mau / "doan.jsonl"
        if not duong.exists():
            thieu.append(str(duong))
            continue
        doan[ma_mau] = [doan_nhung(d) for d in doc_jsonl(duong)]
    if thieu:
        sys.exit("thiếu tệp dữ liệu:\n  " + "\n  ".join(thieu))
    return {"tuyen_bo": tuyen_bo, "bai": bai, "doan": doan, "huong_dan": dung_huong_dan(doc_huong_dan()),
            "quy_tac": {"thong_bao": THONG_BAO, "nhac": NHAC, "re_ngoac_kep": RE_NGOAC_KEP, "re_ma_doan": RE_MA_DOAN},
            "trang": {"luot": luot, "khoa_nhan": cau_hinh["khoa_nhan"], "khoa_giao_dien": cau_hinh["khoa_giao_dien"],
                      "tep_nhan": cau_hinh["tep_nhan"], "tep_hoi": cau_hinh["tep_hoi"], "nghi_ms": NGHI_GIAY * 1000},
            "ca_dac_biet": CA_DAC_BIET}


# Khung "Ca đặc biệt": quy tắc riêng và ca đã chốt của hướng dẫn bản 2, tóm lại bằng lời. Mỗi mục lọc theo ma_mau
# (hoặc nhom = tiền tố ma_mau) và thuoc_tinh (có thể bỏ trống: áp cho mọi thuộc tính của nhóm) ghi sẵn trên tuyên bố,
# không đọc câu tuyên bố. Chỉ chép luật của hướng dẫn, không chép câu của bộ thử (tests/test_tao_cong_cu_gan_nhan.py kiểm
# không câu tuyên bố nào nằm trong đây). Sửa hướng dẫn thì sửa cả bảng này; cột nguon trỏ về mục và ví dụ gốc.
def _moi_nhom(muc):
    """Một mục chung áp cho cả ba nhóm sản phẩm."""
    return [dict(muc, nhom=nhom) for nhom in NHOM_THEO_TIEN_TO]


CA_DAC_BIET = [
    {"ma_mau": "dt-apple-iphone17", "thuoc_tinh": "do_sang", "tieu_de": "Chữ “tối đa” và “đỉnh” trên trang Apple",
     "noi_dung": "Apple dùng “tối đa” cho chế độ tiêu chuẩn (1000 nit), còn “đỉnh” cho hai chế độ: HDR (1600 nit) "
                 "và ngoài trời (3000 nit). Tuyên bố chỉ ghi “đỉnh” mà không nói chế độ nào thì chưa xác định được "
                 "điều kiện: D1a, ghi chua_xac_dinh=đỉnh. Không chọn chế độ theo con số của tuyên bố. Tuyên bố có cả "
                 "chữ chỉ chế độ rõ (“ngoài trời”, “HDR”, “dưới nắng”) và chữ mức cao (“tối đa”, “đỉnh”): chữ chỉ chế "
                 "độ quyết định, chữ mức cao là kiểu giá trị tối đa.",
     "nguon": "mục 6.5, 6.8 ý 4, V05, V47"},
    {"nhom": "dt", "thuoc_tinh": "do_sang", "tieu_de": "Chế độ hiển thị: nêu bằng tên hãng hoặc bằng hoàn cảnh",
     "noi_dung": "Độ sáng điện thoại không có cách hiểu mặc định: tuyên bố không nêu chế độ thì D1a, ghi "
                 "mac_dinh=che_do_hien_thi (trừ khi tài liệu chỉ có một con số không kèm điều kiện nào: so thẳng, mục "
                 "6.4). Chế độ nêu bằng tên hãng dùng hoặc bằng hoàn cảnh của chế độ ấy: “dưới nắng”, “ánh nắng”, “ánh "
                 "sáng mạnh” tả hoàn cảnh của chế độ sáng cao ngoài trời (mục 6.8 ý 2), ghi ngoai_cau_hinh=<cụm> nếu "
                 "phụ lục chưa có cụm đó. Phần diện tích đo không nêu thì hiểu như hãng công bố.",
     "nguon": "mục 6.4, 6.5, 6.8, V25, V26, V51"},
    {"ma_mau": "dt-apple-iphone17", "thuoc_tinh": "thoi_luong_pin",
     "tieu_de": "Tuyên bố chép đúng nhãn “Thời gian xem video” của tài liệu",
     "noi_dung": "Luật chép đúng nhãn (mục 6.8, QĐ15): tuyên bố gọi hoạt động bằng đúng nhãn “Thời gian xem video” và "
                 "không thiếu chữ điều kiện nào của nhãn (như “trực tuyến”) thì cùng điều kiện với dòng đó, so số ở D3–D5, "
                 "ghi chep_nhan=…. Không trùng chữ nhãn nào (chỉ nói “pin … giờ”) thì vẫn là chưa nêu hoạt động: lấy hoạt "
                 "động kém thuận lợi nhất hãng công bố (xem video trực tuyến). Không chọn dòng vì con số trùng.",
     "nguon": "mục 5, 5.1, 6.8, V03, V24"},
    {"nhom": "dt", "thuoc_tinh": "thoi_luong_pin", "tieu_de": "“Liên tục”, “sử dụng liên tục”, “dùng liên tục”",
     "noi_dung": "Cụm chỉ sự liên tục hay mức dùng chung, không nêu hoạt động cụ thể: coi như chưa nêu hoạt động, dùng "
                 "cách hiểu mặc định (hoạt động kém thuận lợi nhất hãng công bố). Cụm này không phải từ khẳng định. "
                 "“Sử dụng liên tục” của Xiaomi 15T là tên bài đo ở phía tài liệu, không phải hoạt động mà tuyên bố nêu.",
     "nguon": "mục 6.2, 6.8 ý 3, V07"},
    {"nhom": "dt", "thuoc_tinh": "zoom", "tieu_de": "Zoom không nói quang học hay kỹ thuật số",
     "noi_dung": "Hiểu là zoom quang học, tính theo độ phóng đại, khi chụp ảnh. Ví dụ “iPhone 17 zoom 10x” so với 2x "
                 "quang học; 10x là thu phóng kỹ thuật số nên Lệch ở D4. Khảo sát có 6/10 người hiểu khác; hướng dẫn "
                 "vẫn giữ (lệch khỏi quy tắc đặt trước), Bước 37 tính lại với cách hiểu kỹ thuật số.",
     "nguon": "mục 5.1, V28"},
    {"nhom": "dt", "thuoc_tinh": "sac_nhanh", "tieu_de": "Sạc nhanh: bộ sạc và mốc phần trăm",
     "noi_dung": "Không nói bộ sạc: hiểu là chỉ dùng đồ có trong hộp, không mua thêm củ sạc (iPhone 17 chỉ kèm cáp). "
                 "Con số cần bộ sạc bán riêng mà tuyên bố không nêu bộ sạc thì Lệch (bo_dieu_kien), dù chép đúng con "
                 "số; ghi mac_dinh mọi khóa tuyên bố không nêu (bo_tiep_hop, cach_sac). Tuyên bố nêu bộ sạc hay công "
                 "suất bộ sạc thì so theo điều kiện dạng số (mục 6.3), không cần nói “bán riêng”: đủ mức tối thiểu "
                 "thì cùng điều kiện, thiếu thì Lệch (doi_dieu_kien). Con số W đi cùng cách sạc hay cổng sạc là công "
                 "suất bộ tiếp hợp (mục 6.8 ý 5). Không nói sạc tới bao nhiêu phần trăm: D1a. Khảo sát: 5/10 người "
                 "hiểu khác về bộ sạc, chưa quá nửa nên giữ.",
     "nguon": "mục 5, 5.1, 6.3, 6.8 ý 5, V01, V21, V22, V46"},
    {"nhom": "dt", "thuoc_tinh": "cong_suat_sac", "tieu_de": "Công suất sạc: bộ sạc, và con số của điều kiện",
     "noi_dung": "Như sạc nhanh: không nói bộ sạc thì hiểu là không mua thêm củ sạc, sạc có dây. Công suất chỉ đạt với "
                 "củ sạc bán riêng mà tuyên bố không nêu thì Lệch (bo_dieu_kien), ghi mac_dinh mọi khóa tuyên bố không "
                 "nêu. Con số W mà tài liệu chỉ dùng làm mức tối thiểu của bộ tiếp hợp (“… W trở lên”) không phải công "
                 "suất sạc: không khớp ở D3, D4. Tuyên bố lấy con số đó làm công suất thì dò D1–D6 với các giá trị thật "
                 "của thuộc tính, ghi nham_vai=<cụm>. Khảo sát: 5/10 người hiểu khác về bộ sạc, chưa quá nửa nên giữ.",
     "nguon": "mục 5, 5.1, 6.9, V23"},
    {"nhom": "dt", "thuoc_tinh": "tan_so_quet", "tieu_de": "Tần số quét và chữ “luôn”",
     "noi_dung": "“Màn hình 120Hz” khớp “thích ứng lên đến 120Hz”, vì không nói thì hiểu là mức tối đa. Nhưng “luôn "
                 "chạy ở 120Hz” biến mức tối đa thành chắc chắn: Lệch ở D2, ghi khang_dinh=luôn. Chữ “Luôn” trong tên "
                 "tính năng “Màn hình Luôn Bật”, và chữ “luôn” ở vế nói việc khác (kết nối, thông tin), không gắn với "
                 "con số nên không tính.",
     "nguon": "mục 5, 6.2, V40"},
    {"nhom": "dt", "thuoc_tinh": "khang_nuoc", "tieu_de": "Kháng nước: độ sâu, thời gian, mã IP",
     "noi_dung": "Không nói độ sâu, thời gian ngâm thì hiểu như hãng công bố. Có nói thì so bằng số với mức hãng thử "
                 "(mục 6.3): không vượt là cùng điều kiện; vượt là điều kiện khác. “Tối đa” của độ sâu, thời gian "
                 "ngâm là giới hạn của bài thử, không phải kiểu giá trị. Mã IP so theo nhánh (mục 6.6): khác nhánh "
                 "không khớp ở D3; trùng mã của bộ phận hay điều kiện khác thì D4; không trùng mã nào thì D5, "
                 "doi_gia_tri.",
     "nguon": "mục 6.2, 6.3, 6.6, V06, V29"},
    {"ma_mau": "tn-samsung-buds3pro", "thuoc_tinh": "thoi_luong_pin",
     "tieu_de": "Hai số cho tổng thời gian phát nhạc khi bật chống ồn",
     "noi_dung": "Bảng thông số ghi “Tổng thời gian phát nhạc (Giờ, bật ANC)” hai lần, 26 và 30 giờ; chú thích còn "
                 "ghi tối đa 30 giờ cho cả bật và tắt ANC. Chỉ khi điều kiện của tuyên bố (nêu rõ hoặc mặc định) là "
                 "kèm hộp sạc và bật chống ồn thì D1b: Chưa đủ thông tin, tick “Tài liệu mâu thuẫn”, kể cả khi số của "
                 "tuyên bố trùng một trong hai. Ngoại lệ (QĐ13): số của tuyên bố khớp cả hai (bằng hoặc thấp hơn cả "
                 "hai) thì dò tiếp D2–D3, ghi mau_thuan_khop_ca_hai. Tuyên bố không nêu bộ phận thì là tai nghe, "
                 "không so với số Tổng.",
     "nguon": "mục 4, 7 (D1b), V48"},
    {"ma_mau": "tn-samsung-buds3pro", "thuoc_tinh": "thoi_luong_pin",
     "tieu_de": "Không nói chống ồn, hoạt động, bộ phận",
     "noi_dung": "Hiểu là chống ồn bật (Samsung ghi ANC bật theo mặc định), nghe nhạc, chỉ tính tai nghe, không tính "
                 "hộp sạc; ghi mac_dinh mọi khóa tuyên bố không nêu. Khảo sát: mỗi điểm có 4/10 người hiểu khác (4/10 "
                 "người tính cả hộp sạc), chưa quá nửa nên giữ.",
     "nguon": "mục 5, 5.1, V10, V32"},
    {"ma_mau": "tn-samsung-buds3pro", "thuoc_tinh": "thoi_luong_pin",
     "tieu_de": "Chữ chỉ bộ phận: kèm hộp sạc hay hộp sạc",
     "noi_dung": "“Tổng”, “tổng cộng”, “kèm / cùng / kết hợp hộp sạc” là kèm hộp sạc. “Hộp sạc” đứng riêng làm chủ "
                 "ngữ (“hộp sạc cho thêm …”) là bộ phận hộp sạc.",
     "nguon": "mục 6.8 ý 6"},
    {"ma_mau": "tn-samsung-buds3pro", "thuoc_tinh": "thoi_luong_pin", "tieu_de": "Không tạo giá trị mới bằng phép tính",
     "noi_dung": "Chỉ so với con số hãng công bố. Không lấy tổng trừ phần tai nghe để ra phần riêng của hộp sạc, không "
                 "cộng, trừ, nhân các số. Tuyên bố về phần mà hãng không công bố số riêng thì dò D4–D6 như thường: "
                 "không trùng số nào thì D6.",
     "nguon": "mục 6.9"},
    {"ma_mau": "tn-samsung-buds3pro", "thuoc_tinh": "thoi_luong_pin",
     "tieu_de": "Con số trùng số của một hoạt động khác",
     "noi_dung": "D4 tính mọi điều kiện khác của cùng thuộc tính, kể cả hoạt động khác: con số trùng thời gian của một "
                 "hoạt động khác (đàm thoại) thì Lệch. Sau khi gán lượt 2 sẽ đếm các ca này; quá 1/4 số Lệch D4 thì "
                 "xét lại ở Bước 27.",
     "nguon": "mục 11.2, V42"},
    {"ma_mau": "tn-samsung-buds3pro", "thuoc_tinh": "thoi_luong_pin", "tieu_de": "Chú thích về cách hãng đo",
     "noi_dung": "Chú thích “ghép nối … với điện thoại thông minh Galaxy … với các cài đặt mặc định” chỉ là cách hãng "
                 "đo, không phải điều kiện: bỏ qua.",
     "nguon": "mục 4, 11.3"},
    {"ma_mau": "tn-samsung-buds3pro", "thuoc_tinh": "khang_nuoc", "tieu_de": "Hộp sạc không kháng nước",
     "noi_dung": "IP57 chỉ áp dụng cho tai nghe; Samsung ghi hộp sạc không kháng nước. Tuyên bố gán IP57 cho hộp sạc "
                 "thì Lệch (doi_bo_phan); chỉ nói hộp sạc kháng nước mà không nêu mã thì Sai (doi_bo_phan). Tuyên bố "
                 "không nói bộ phận thì hiểu là tai nghe. Mã IP khác nhánh với mã của tai nghe: không khớp; không "
                 "trùng mã nào thì Sai (mục 6.6).",
     "nguon": "mục 5, 6.6, V18, V35"},
    {"ma_mau": "tn-samsung-buds3pro", "thuoc_tinh": "dung_luong_pin", "tieu_de": "Pin tai nghe và pin hộp sạc",
     "noi_dung": "Tai nghe 50 mAh, hộp sạc 515 mAh (mức điển hình). Gán 515 mAh cho tai nghe thì Lệch (doi_bo_phan). "
                 "Tuyên bố không nói bộ phận thì hiểu là tai nghe.",
     "nguon": "mục 5, V36"},
    {"ma_mau": "tn-samsung-buds3pro", "thuoc_tinh": "sac_nhanh", "tieu_de": "Sạc nhanh của Buds3 Pro",
     "noi_dung": "Tài liệu Buds3 Pro không có thông số sạc nhanh, nên tuyên bố sạc nhanh dừng ở D1, bằng chứng để "
                 "trống, không ghi mac_dinh. Số phút sạc của tai nghe cũng không có mặc định.",
     "nguon": "mục 5, 7 (D1), V45"},
] + _moi_nhom({
    "tieu_de": "Cụm phủ nhiều giá trị: “mọi điều kiện …”, “mọi chế độ”, “mọi hoạt động”, “bất kể …”, “dù A hay B”, "
               "“cho cả A và B”",
    "noi_dung": "Cụm phủ gắn với con số nghĩa là tuyên bố phải đúng ở từng giá trị được phủ. Điều kiện của tuyên bố là "
                "giá trị kém thuận lợi nhất trong các giá trị được phủ mà tài liệu công bố; đây là điều kiện nêu rõ, "
                "nên Lệch thì loại doi_dieu_kien. Cụm phủ không phải từ khẳng định, trừ khi có thêm từ khẳng định gắn "
                "với con số. Kháng nước: “mọi hoạt động” phủ cả hoạt động hãng khuyến cáo không dùng.",
    "nguon": "mục 6.2, 6.6, 6.8, V49"}) + _moi_nhom({
    "tieu_de": "Cụm điều kiện chưa có trong phụ lục: đọc theo nghĩa với người mua",
    "noi_dung": "Cụm tả đúng một điều kiện tài liệu công bố, bằng tên hãng dùng hoặc bằng hoàn cảnh của điều kiện ấy, "
                "thì là nêu điều kiện đó; ghi ngoai_cau_hinh=<cụm>. Cụm chung chung, không trỏ được tới điều kiện nào "
                "tài liệu công bố, thì coi như chưa nêu: dùng cách hiểu mặc định. Cụm ở tài liệu mà không xếp được vào "
                "sáu loại: ngoai_sau_loai=<cụm>. Cụm ở tuyên bố vẫn không xếp được: D1a, ghi chua_xac_dinh=<cụm>. "
                "Cấu hình chưa biết cụm không phải lý do D1a cho nhãn chuẩn.",
    "nguon": "mục 6.7, 6.8, V08, V51"}) + _moi_nhom({
    "tieu_de": "Con số của điều kiện không phải giá trị của thuộc tính",
    "noi_dung": "Con số tài liệu dùng làm điều kiện (mức tối thiểu của bộ tiếp hợp, mốc phần trăm, số phút sạc, độ sâu, "
                "thời gian ngâm, phần diện tích đo) không phải giá trị công bố: không dùng để khớp ở D3 hay D4. "
                "Tuyên bố lấy con số đó làm giá trị thì dò D1–D6 với các giá trị thật của thuộc tính, và ghi "
                "nham_vai=<cụm>.",
    "nguon": "mục 6.3, 6.9"})


def json_nhung(du_lieu):
    """JSON an toàn để đặt trong thẻ <script type="application/json">: không để lọt '<' (chặn '</script>')."""
    return json.dumps(du_lieu, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def dung_html(du_lieu):
    """Điền chữ phụ thuộc lượt (tiêu đề, tên tệp tải về) trước, nhúng dữ liệu JSON sau cùng."""
    t = du_lieu["trang"]
    if t["luot"] == LUOT:
        gan_mu = "Lượt __LUOT__ gán mù với lượt trước: không mở nhãn lượt 1 và các ghi chép về nhãn lượt 1."
    else:
        gan_mu = ("Lượt __LUOT__ gán mù với các lượt trước: không mở nhãn lượt 1, nhãn lượt 2 (kể cả nhãn do Claude gán) và "
                  "các ghi chép về những nhãn đó.")
    mau = MAU_HTML.replace("__GAN_MU__", gan_mu)
    mau = mau.replace("__LUOT__", str(t["luot"])).replace("__TEP_NHAN__", t["tep_nhan"]).replace("__TEP_HOI__", t["tep_hoi"])
    return mau.replace("__DU_LIEU__", json_nhung(du_lieu))


# Mẫu HTML. Chuỗi thô (r"""), nên các \u00a0, \n... bên trong là của JavaScript. Không dùng ba dấu nháy kép trong đây.
MAU_HTML = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Công cụ gán nhãn chuẩn - bộ thử, lượt __LUOT__</title>
<style>
:root {
  --nen: #f4f5f7; --khung: #ffffff; --chu: #1c2026; --phu: #5a6370; --vien: #d3d8df;
  --nhan: #1d5fc4; --nhan-nen: #e5eefc; --mark: #ffe27a; --mark-chu: #1c2026;
  --loi: #b3261e; --loi-nen: #fdecea; --tot: #1a7f37; --tot-nen: #e6f4ea; --canh-bao-nen: #fff4d6;
}
@media (prefers-color-scheme: dark) {
  :root {
    --nen: #14171a; --khung: #1d2227; --chu: #e6e9ed; --phu: #9ba4af; --vien: #383f47;
    --nhan: #7db0ff; --nhan-nen: #1f3556; --mark: #7a6400; --mark-chu: #ffffff;
    --loi: #ff8f86; --loi-nen: #3b1f1d; --tot: #5fd37a; --tot-nen: #1b3324; --canh-bao-nen: #3d3412;
  }
}
* { box-sizing: border-box; }
[hidden] { display: none !important; }
html, body { margin: 0; }
body { font: 15px/1.5 system-ui, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: var(--nen);
       color: var(--chu); height: 100vh; display: flex; flex-direction: column; }
code { font-family: Consolas, "Courier New", monospace; font-size: 0.92em; background: var(--nhan-nen); padding: 0 4px; border-radius: 3px; }
h1 { font-size: 16px; margin: 0; }
h2 { font-size: 14px; margin: 0 0 8px; }
button { font: inherit; cursor: pointer; border: 1px solid var(--vien); background: var(--khung); color: var(--chu);
         border-radius: 6px; padding: 5px 10px; }
button:hover:not(:disabled) { border-color: var(--nhan); }
button:disabled { opacity: 0.55; cursor: default; }
button.chinh { background: var(--nhan); border-color: var(--nhan); color: #fff; font-weight: 600; }
button.nho { padding: 1px 8px; font-size: 13px; }
input[type=text], input[type=search], select, textarea { font: inherit; color: var(--chu); background: var(--khung);
  border: 1px solid var(--vien); border-radius: 6px; padding: 5px 8px; width: 100%; }
textarea { resize: vertical; }
label { display: block; font-weight: 600; font-size: 13px; margin: 10px 0 3px; }
label.kiem { display: flex; align-items: center; gap: 6px; font-weight: 600; }
label.kiem input { width: auto; }
.phu { color: var(--phu); font-size: 13px; margin: 4px 0; }

#dau { padding: 8px 14px; background: var(--khung); border-bottom: 1px solid var(--vien); }
#dau .dau-hang { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
#dau .nhac { margin: 2px 0 0; font-size: 13px; color: var(--phu); }
#canh-bao, #canh-bao-lai { margin: 6px 0 0; padding: 6px 10px; background: var(--canh-bao-nen); border: 1px solid #d9a400; border-radius: 6px; font-size: 13px; }

#luoi { flex: 1; min-height: 0; display: grid; grid-template-columns: 270px minmax(0, 1.25fr) minmax(0, 1fr);
        gap: 12px; padding: 12px; }
#luoi > * { min-height: 0; overflow: auto; }
.khung { background: var(--khung); border: 1px solid var(--vien); border-radius: 8px; padding: 10px 12px; margin-bottom: 12px; }

#cot-trai { display: flex; flex-direction: column; overflow: hidden; }
#cot-trai .khung { flex: none; }
#tien-do { font-weight: 600; margin: 8px 0 6px; }
.nut-cot { display: flex; flex-direction: column; gap: 5px; }
#ds { list-style: none; margin: 0; padding: 0; flex: 1; min-height: 0; overflow: auto; position: relative;
      background: var(--khung); border: 1px solid var(--vien); border-radius: 8px; }
#ds li { margin: 0; }
.muc { display: flex; gap: 6px; width: 100%; text-align: left; border: 0; border-bottom: 1px solid var(--vien);
       border-radius: 0; background: transparent; padding: 5px 8px; align-items: baseline; }
.muc .dau-gan { width: 1.1em; flex: none; color: var(--phu); }
.muc .ma-muc { flex: none; font-family: Consolas, monospace; font-size: 12.5px; color: var(--phu); }
.muc .tt { min-width: 0; font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.muc.xong .dau-gan { color: var(--tot); font-weight: 700; }
.muc.dang-mo { background: var(--nhan-nen); }

.the-dau { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
.the-dau .ma { font-family: Consolas, monospace; font-weight: 700; }
.dong-ho { font-family: Consolas, monospace; font-size: 20px; font-weight: 700; font-variant-numeric: tabular-nums; margin-left: auto; }
.dong-ho.dung { color: var(--phu); }
.tuyen-bo { font-size: 18px; font-weight: 700; margin: 8px 0; }
.chi-tiet { display: grid; grid-template-columns: max-content 1fr; gap: 2px 10px; margin: 0; font-size: 13px; }
.chi-tiet dt { color: var(--phu); }
.chi-tiet dd { margin: 0; overflow-wrap: anywhere; }

.bai { white-space: pre-wrap; overflow-wrap: anywhere; max-height: 42vh; overflow: auto; position: relative; padding: 6px 8px;
       border: 1px solid var(--vien); border-radius: 6px; font-size: 14px; }
.bai mark { background: var(--mark); color: var(--mark-chu); border-radius: 2px; padding: 0 1px; }

/* Các khung hướng dẫn trong biểu mẫu (cột giữa rộng khoảng 500px, chữ 13px) */
details.hd { border: 1px solid var(--vien); border-radius: 6px; margin: 0 0 8px; }
details.hd > summary { cursor: pointer; font-weight: 700; font-size: 13px; padding: 5px 10px; background: var(--nen); border-radius: 6px; }
details.hd[open] > summary { border-bottom: 1px solid var(--vien); border-radius: 6px 6px 0 0; }
.hd-nd { font-size: 13px; line-height: 1.45; padding: 6px 10px 8px; }
.hd-nd ol, .hd-nd ul { margin: 0; padding-left: 20px; }
.hd-nd li { margin: 3px 0; }
.hd-nd p { margin: 4px 0; }
.phu-nho { color: var(--phu); font-size: 12px; }
.gc { background: var(--mark); color: var(--mark-chu); border-radius: 2px; padding: 0 2px; font-style: normal; }
#d-trang-thai { margin: 0 0 6px; font-weight: 600; }
.d-hang { display: grid; grid-template-columns: 34px minmax(0, 1fr); gap: 0 6px; padding: 6px 4px; border-top: 1px solid var(--vien); border-left: 3px solid transparent; }
.d-hang:first-child { border-top: 0; }
.d-hang.chon { background: var(--nhan-nen); border-left-color: var(--nhan); }
.d-ma { font-family: Consolas, monospace; font-weight: 700; }
.d-cau-hoi { font-size: 13px; }
.d-nhan { font-weight: 600; color: var(--nhan); margin-top: 2px; }
.d-luu-y { font-size: 12px; color: var(--phu); margin-top: 1px; }
.d-mau { display: flex; gap: 8px; align-items: flex-start; margin-top: 3px; font-size: 12px; }
.d-mau .van { flex: 1; min-width: 0; font-style: italic; overflow-wrap: anywhere; }
.d-mau button { flex: none; }
.d-nut { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 5px; }
.d-nut .dung-o { margin-left: auto; font-weight: 600; }
.d-vi-du { margin-top: 5px; padding: 5px 8px; border: 1px dashed var(--vien); border-radius: 6px; font-size: 12.5px; background: var(--khung); }
.goi-y-loai { margin-top: 6px; padding: 6px 10px; border: 1px dashed var(--vien); border-radius: 6px; font-size: 12.5px; line-height: 1.45; background: var(--khung); }
.goi-y-loai ol, .goi-y-loai ul { margin: 3px 0; padding-left: 20px; }
.goi-y-loai li { margin: 2px 0; }
.goi-y-loai p { margin: 4px 0; }
.md-hang { padding: 5px 0; border-top: 1px solid var(--vien); }
.md-hang:first-of-type { border-top: 0; }
.md-hang.khong-co { background: var(--loi-nen); border-left: 3px solid var(--loi); padding: 5px 6px; border-radius: 4px; }
.md-the { display: inline-block; margin-right: 6px; padding: 0 5px; font-size: 11.5px; font-weight: 700; color: var(--loi); border: 1px solid var(--loi); border-radius: 4px; }
.md-ghi { font-size: 12px; color: var(--phu); margin-top: 3px; }
.md-nut { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 3px; }
.md-nut button.da-them { border-color: var(--tot); color: var(--tot); }
.md-huong { margin: 6px 0 0; padding-top: 5px; border-top: 1px solid var(--vien); }

#nut-nhan { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px; }
#nut-nhan .nhan-o { padding: 7px 8px; font-weight: 600; text-align: left; border: 1px solid var(--vien); border-radius: 6px; opacity: 0.6; }
#nut-nhan .nhan-o.chon { background: var(--nhan); border-color: var(--nhan); color: #fff; opacity: 1; }
#nut-nhan small { display: block; font-weight: 400; font-size: 12px; line-height: 1.3; opacity: 0.9; }
#nhac { margin-top: 10px; padding: 6px 10px; background: var(--canh-bao-nen); border: 1px solid #d9a400; border-radius: 6px; font-size: 13.5px; }
#bang-chung { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px; }
#bang-chung li.bc { display: inline-flex; align-items: center; gap: 4px; border: 1px solid var(--vien); border-radius: 6px; padding: 2px 4px 2px 8px; }
#bang-chung li.trong { color: var(--phu); font-size: 13px; }
.lien-ket { border: 0; background: none; padding: 0; color: var(--nhan); font-family: Consolas, monospace; font-size: 13px; text-decoration: underline; }
.hang-nut { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.hang-nut .chinh { margin-left: auto; }
#loi { margin-top: 10px; padding: 6px 10px; background: var(--loi-nen); color: var(--loi); border: 1px solid var(--loi); border-radius: 6px; font-size: 13.5px; }
#loi ul { margin: 0; padding-left: 18px; }
#tin { color: var(--tot); font-size: 13px; margin: 6px 0 0; }

#cot-phai { position: relative; }
#khung-tim { position: sticky; top: 0; z-index: 2; margin-bottom: 8px; }
.doan { background: var(--khung); border: 1px solid var(--vien); border-radius: 8px; padding: 8px 10px; margin-bottom: 8px; }
.doan.da-chon { border-color: var(--nhan); box-shadow: 0 0 0 1px var(--nhan); }
.doan-dau { display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 4px; }
.ma { font-family: Consolas, monospace; font-size: 12.5px; color: var(--phu); user-select: none; -webkit-user-select: none; }
.doan button { user-select: none; -webkit-user-select: none; }
.noi-dung { white-space: pre-wrap; overflow-wrap: anywhere; font-size: 14px; }
.chu-thich { white-space: pre-wrap; overflow-wrap: anywhere; font-size: 12px; color: var(--phu); margin-top: 6px; padding-top: 4px; border-top: 1px dashed var(--vien); }
.chu-thich::before { content: "Chú thích: "; font-style: italic; }

/* Khung phủ bên phải: toàn văn hướng dẫn */
#huong-dan { position: fixed; top: 0; right: 0; bottom: 0; width: min(780px, 94vw); z-index: 50; display: flex; flex-direction: column;
             background: var(--khung); border-left: 1px solid var(--vien); box-shadow: -6px 0 18px rgba(0, 0, 0, 0.25); }
.hdan-dau { display: flex; align-items: center; gap: 10px; padding: 8px 14px; border-bottom: 1px solid var(--vien); }
.hdan-dau .dong { margin-left: auto; }
#hdan-nd { flex: 1; min-height: 0; overflow: auto; padding: 4px 18px 48px; font-size: 14px; }
.md h1 { font-size: 20px; margin: 12px 0 6px; }
.md h2 { font-size: 17px; margin: 24px 0 6px; padding-top: 8px; border-top: 1px solid var(--vien); }
.md h3 { font-size: 15px; margin: 16px 0 4px; }
.md h4 { font-size: 14px; margin: 12px 0 4px; }
.md p { margin: 6px 0; }
.md ul, .md ol { margin: 4px 0 8px; padding-left: 22px; }
.md li { margin: 2px 0; }
.md pre { overflow: auto; background: var(--nhan-nen); padding: 8px 10px; border-radius: 6px; font-size: 12.5px; }
.md pre code { background: none; padding: 0; }
.md .cuon-ngang { overflow-x: auto; margin: 8px 0; }
.md table { border-collapse: collapse; font-size: 13px; }
.md th, .md td { border: 1px solid var(--vien); padding: 3px 7px; vertical-align: top; text-align: left; overflow-wrap: anywhere; }
.md th { background: var(--nen); }
.muc-luc { display: flex; flex-wrap: wrap; gap: 4px 12px; margin: 8px 0 4px; font-size: 13px; }
.muc-luc a { color: var(--nhan); }

@media (max-width: 1100px) {
  body { height: auto; display: block; }
  #luoi { display: block; padding: 8px; }
  #luoi > * { overflow: visible; }
  #cot-trai { overflow: visible; }
  #ds { max-height: 40vh; margin-bottom: 12px; }
  #cot-phai { max-height: 80vh; overflow: auto; }
}
</style>
</head>
<body>
<header id="dau">
  <div class="dau-hang">
    <h1>Công cụ gán nhãn chuẩn - bộ thử (Bước 16 · lượt __LUOT__)</h1>
    <button id="btn-hd" type="button" class="nho" aria-controls="huong-dan" aria-expanded="false">Mở hướng dẫn đầy đủ</button>
  </div>
  <p class="nhac">Các khung hướng dẫn lấy từ <code>data/huong_dan_gan_nhan.md</code> (bản 2) lúc sinh trang. Công cụ chỉ hiện tài liệu, hướng dẫn và ghi lại dòng D bạn chọn (nhãn tự điền theo dòng), không đọc tuyên bố để gợi ý nhãn; trang chỉ báo khi các ô bạn điền mâu thuẫn nhau hoặc trái quy tắc. __GAN_MU__</p>
  <p id="canh-bao" role="alert" hidden></p>
  <div id="canh-bao-lai" role="alert" hidden></div>
</header>

<main id="luoi">
  <aside id="cot-trai" aria-label="Danh sách tuyên bố">
    <div class="khung">
      <label for="nguoi-gan" style="margin-top:0">Người gán (nguoi_gan)</label>
      <input id="nguoi-gan" type="text" autocomplete="off">
      <p id="tien-do"></p>
      <div class="nut-cot">
        <button id="btn-tai-nhan" type="button">Tải nhãn (__TEP_NHAN__)</button>
        <button id="btn-tai-hoi" type="button">Tải câu hỏi nhãn (__TEP_HOI__)</button>
        <button id="btn-nhap" type="button">Nhập lại __TEP_NHAN__ đã xuất</button>
        <input id="tep-nhap" type="file" accept=".jsonl,.json,.md,.txt" multiple hidden>
      </div>
      <p class="phu">Tự lưu trong trình duyệt này; vẫn nên tải tệp nhãn thường xuyên.</p>
    </div>
    <ol id="ds"></ol>
  </aside>

  <section id="cot-giua" aria-label="Tuyên bố đang gán">
    <div class="khung" id="the">
      <div class="the-dau">
        <span class="ma" id="the-ma" style="user-select:text"></span>
        <button id="btn-tam-dung" type="button" class="nho">Tạm dừng</button>
        <span id="dong-ho" class="dong-ho" title="Thời gian cộng dồn của tuyên bố này">00:00</span>
      </div>
      <p id="trang-thai-dh" class="phu"></p>
      <p id="the-tb" class="tuyen-bo"></p>
      <dl id="the-chi-tiet" class="chi-tiet"></dl>
    </div>

    <div class="khung">
      <details class="hd" id="kh-bai">
        <summary>Bài quảng cáo (chỉ để kiểm tách, đóng sẵn) <span id="bai-ten" class="phu"></span></summary>
        <div class="hd-nd">
          <p>Gán theo chữ của tuyên bố. Câu tô vàng chỉ để kiểm tách. Thấy tuyên bố thiếu điều kiện thì ghi <code>tach=…</code> vào ô Câu hỏi nhãn, vẫn gán theo tuyên bố.</p>
          <div id="bai" class="bai"></div>
        </div>
      </details>
    </div>

    <form id="form" class="khung" autocomplete="off">
      <details class="hd" id="kh-cach-lam" open>
        <summary>Cách làm một tuyên bố</summary>
        <div class="hd-nd">
          <ol>
            <li>Đọc tuyên bố ở thẻ trên. Gán theo chữ của tuyên bố; bài quảng cáo (đóng sẵn) chỉ để kiểm tách.</li>
            <li>Ở cột phải, gõ con số hoặc từ khóa vào ô tìm. Đọc đoạn, bấm "Thêm làm bằng chứng".</li>
            <li>Bôi đen câu cần trích trong đoạn, bấm "Lấy đoạn đang bôi đen". Đoạn khác có cùng chữ thì trang hỏi có thêm không: ghi mọi đoạn có cùng con số ở cùng điều kiện.</li>
            <li>Xác định điều kiện của tuyên bố (khung “Bước 3”): điều kiện nêu rõ thì giữ nguyên, điều kiện không nêu thì lấy cách hiểu mặc định. Không chọn điều kiện theo con số của tuyên bố.</li>
            <li>Dò bảng D1–D6 từ trên xuống, bấm “Dừng ở đây” ở dòng đầu tiên đúng với tuyên bố. Nhãn tự điền theo dòng; Lệch hoặc Sai thì chọn thêm loại.</li>
            <li>Viết lý do: bấm "Chèn mẫu câu" ở dòng vừa dừng, rồi thay các chỗ {…}. Ghi chú: mac_dinh=… cho mọi khóa tuyên bố không nêu (từ D1a tới D6); D2 thì khang_dinh=…; D1a thì nguyên nhân.</li>
            <li>Bấm "Lưu và sang tuyên bố sau". Còn thiếu gì thì trang báo đỏ.</li>
          </ol>
        </div>
      </details>

      <details class="hd" id="kh-mac-dinh" open>
        <summary>Bước 3 · Điều kiện của tuyên bố: nêu rõ, hoặc cách hiểu mặc định (dùng ở mọi dòng D)</summary>
        <div class="hd-nd">
          <p>Quảng cáo hay bỏ bớt điều kiện. Bảng dưới cho biết làm gì với từng điều kiện bị bỏ. Không chọn điều kiện theo con số của tuyên bố: con số trùng giá trị ở điều kiện khác là việc của D4. Dòng có cách hiểu: coi như tuyên bố đã nói điều kiện đó, rồi dò tiếp từ D1b tới D6 (không dừng ở D1a vì điều kiện này). Dòng “Không có mặc định”: không biết tuyên bố nói điều kiện nào, dừng ở D1a, nhãn Chưa đủ thông tin. Các cách hiểu này chốt ở Bước 8 theo nguyên tắc “hiểu như người mua thông thường, bộ phận chính, không mua thêm phụ kiện”, rồi kiểm lại bằng khảo sát 10 người ở Bước 10.</p>
          <div id="md-nd"></div>
        </div>
      </details>

      <details class="hd" id="kh-cum">
        <summary>Cụm điều kiện đã biết của sản phẩm và thuộc tính này (phụ lục mục 13)</summary>
        <div class="hd-nd">
          <p class="phu-nho">Cụm có ở đây thì là điều kiện đó (mục 6.8, ý 1). Cụm chưa có thì đọc theo nghĩa với người mua và ghi ngoai_cau_hinh=…; thiếu cụm ở đây không phải lý do dừng ở D1a. Chỉ hiện các điều kiện của đúng nhóm và thuộc tính đang gán; đây không phải gợi ý nhãn.</p>
          <div id="cum-nd"></div>
        </div>
      </details>

      <details class="hd" id="kh-quyet-dinh" open>
        <summary>Bước 4 · Dò từ trên xuống, bấm “Dừng ở đây” ở dòng đầu tiên đúng với tuyên bố</summary>
        <div class="hd-nd">
          <p id="d-trang-thai"></p>
          <div id="d-ds"></div>
        </div>
      </details>

      <details class="hd" id="kh-ca-dac-biet" open>
        <summary>Ca đặc biệt của sản phẩm và thuộc tính này</summary>
        <div class="hd-nd">
          <p>Quy tắc riêng và ca đã chốt trong hướng dẫn, chỉ hiện các ca của đúng sản phẩm và thuộc tính đang gán. Đây không phải gợi ý nhãn cho tuyên bố đang mở: bạn vẫn tự dò D1–D6.</p>
          <div id="cdb-nd"></div>
        </div>
      </details>

      <details class="hd" id="kh-hay-dung">
        <summary>Quy tắc hay dùng</summary>
        <div class="hd-nd">
          <ul>
            <li>Khớp là bằng con số của hãng (lệch không quá 1%) hoặc kém thuận lợi hơn, ví dụ pin ít giờ hơn, sạc lâu hơn (mục 3, 6.1).</li>
            <li>Bỏ chữ "lên đến" vẫn khớp, không đổi nhãn (mục 6.2).</li>
            <li>Từ khẳng định (danh sách ở dòng D2, đọc từ mục 6.2) gắn ngay với con số, cho một mức không cao hơn mức "lên đến", thì Lệch ở D2 và ghi khang_dinh=… Tên tính năng như "Màn hình Luôn Bật" và từ ở vế nói việc khác không tính (mục 6.2).</li>
            <li>Cách hiểu mặc định dùng ở mọi dòng D, không chỉ ở D1a (mục 5, 7).</li>
            <li>Không chọn điều kiện theo con số của tuyên bố: xác định điều kiện trước, rồi mới so con số (mục 1, bước 3).</li>
            <li>Chú thích của đoạn cũng là bằng chứng. Trong bảng so sánh chỉ dùng cột của đúng sản phẩm (mục 4).</li>
            <li>Không dùng hiểu biết riêng hay trang ngoài kho tài liệu (mục 4).</li>
            <li>Không tự sửa chỗ hãng ghi nhầm. Tài liệu ghi hai số khác nhau cho cùng điều kiện thì Chưa đủ ở D1b và tick "Tài liệu mâu thuẫn" (mục 4).</li>
            <li>Chỗ hướng dẫn chưa rõ thì ghi vào ô Câu hỏi nhãn, đừng tự đặt quy tắc.</li>
          </ul>
        </div>
      </details>

      <h2>Nhãn <span class="phu">(tự điền theo dòng D bạn dừng ở Bước 4, không bấm đổi ở đây)</span></h2>
      <div id="nut-nhan" role="group" aria-label="Nhãn tự điền theo dòng D">
        <div class="nhan-o" data-nhan="DUNG">DUNG<small>Đúng: Cùng điều kiện, con số khớp</small></div>
        <div class="nhan-o" data-nhan="SAI">SAI<small>Sai: Số mâu thuẫn ở cùng điều kiện, hoặc đẹp hơn mọi số của hãng</small></div>
        <div class="nhan-o" data-nhan="LECH">LECH<small>Lệch điều kiện: Số có thật nhưng ở điều kiện khác, hoặc có từ khẳng định ("luôn", "ít nhất"...) gắn với mức "lên đến". Chỉ thiếu chữ "lên đến" thì không phải Lệch</small></div>
        <div class="nhan-o" data-nhan="CHUA_DU">CHUA_DU<small>Chưa đủ thông tin: không có số nào cho thuộc tính (D1), không xác định được điều kiện (D1a), tài liệu mâu thuẫn (D1b), hoặc không có số ở điều kiện này (D6)</small></div>
      </div>

      <div id="o-loai" hidden>
        <label for="loai">Loại biến đổi (loai) - bắt buộc với LECH và SAI</label>
        <p id="loai-d2" class="phu" hidden>Bạn dừng ở D2 nên loại đã khóa sẵn là doi_kieu_gia_tri, không cần chọn.</p>
        <select id="loai"></select>
        <div id="goi-y-lech" class="goi-y-loai" hidden>
          <strong>Chọn loại bằng 2 câu hỏi.</strong> Con số của quảng cáo có trong tài liệu, nhưng ở điều kiện khác. Quảng cáo làm sai điều kiện theo kiểu nào?
          <ol>
            <li>Quảng cáo có <b>nói ra</b> điều kiện không? Không nói gì → <code>bo_dieu_kien</code>. Có nói nhưng nói sai → sang câu 2.</li>
            <li>Nói sai cái gì?
              <ul>
                <li>Chế độ, phụ kiện, cách đo → <code>doi_dieu_kien</code>. Kể cả nói con số điều kiện không đủ: củ sạc 20W trong khi tài liệu cần 40W trở lên (V22); và cụm phủ nhiều giá trị ("mọi chế độ", "dù A hay B") mà số chỉ đúng ở một giá trị được phủ (V49).</li>
                <li>Bộ phận → <code>doi_bo_phan</code>. Ví dụ "Hộp sạc Buds3 Pro đạt IP57", trong khi IP57 là của tai nghe (V35).</li>
                <li>Phiên bản → <code>doi_phien_ban</code>. Con số của phiên bản này bị gắn cho phiên bản khác.</li>
                <li>Kiểu con số → <code>doi_kieu_gia_tri</code>. "Lên đến 6 giờ" thành "luôn đủ 6 giờ" (V38); dung lượng điển hình thành định mức (V37).</li>
              </ul>
            </li>
          </ol>
          <p><b>Cặp ví dụ.</b> Tài liệu Galaxy Buds3 Pro ghi 7 giờ khi <b>tắt</b> chống ồn.</p>
          <ul>
            <li>"Buds3 Pro pin 7 giờ": không nói gì về chống ồn, người mua hiểu là đang bật → <code>bo_dieu_kien</code> (V32).</li>
            <li>"Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn": có nói, nhưng nói sai → <code>doi_dieu_kien</code> (V31).</li>
          </ul>
          <p class="phu-nho">Sai nhiều chỗ cùng lúc: chỗ quảng cáo nói ra được ưu tiên hơn chỗ im lặng. Nói ra nhiều chỗ thì ưu tiên bộ phận, rồi phiên bản, rồi kiểu con số, rồi các điều kiện còn lại. Con số trùng nhiều chỗ trong tài liệu: so với chỗ khác quảng cáo ít điều kiện nhất.</p>
          <p class="phu-nho">Chọn <code>bo_dieu_kien</code> thì ô ghi chú thường cần <code>mac_dinh=...</code>: bấm nút ở khung "Bước 3".</p>
        </div>
        <div id="goi-y-sai" class="goi-y-loai" hidden>
          Gần như luôn chọn <code>doi_gia_tri</code>: con số sai. Chỉ chọn <code>doi_bo_phan</code> hoặc <code>doi_phien_ban</code> khi quảng cáo nói về bộ phận hoặc phiên bản khác, và không trùng con số nào của tài liệu. Ví dụ "Hộp sạc Buds3 Pro cũng kháng nước", trong khi hộp sạc không kháng nước (V18).
        </div>
      </div>

      <label>Bằng chứng (bang_chung) - thêm từ cột phải</label>
      <p class="phu">Ghi mọi đoạn có cùng con số ở cùng điều kiện, không chỉ một đoạn (mục 8). Lệch: mọi đoạn chứa con số trùng. Sai: mọi đoạn chứa con số ở cùng điều kiện. Đúng: mọi đoạn chứa giá trị khớp. Chưa đủ ở D1a, D1b, D6: các đoạn chứa những con số mà lý do dựa vào. D1: để trống.</p>
      <ul id="bang-chung"></ul>

      <label for="trich">Câu trích (trich)</label>
      <p class="phu">Chép nguyên văn theo chữ hiển thị ở cột phải; số chú thích của trang hãng đã được bỏ khỏi nội dung. Nhiều phần thì bấm "Lấy đoạn đang bôi đen" nhiều lần, trang tự nối bằng " | ".</p>
      <textarea id="trich" rows="3"></textarea>
      <div class="hang-nut" style="margin-top:6px">
        <button id="btn-lay" type="button">Lấy đoạn đang bôi đen</button>
      </div>
      <p id="nhac-trich" class="phu" hidden></p>
      <div id="goi-y-doan" class="goi-y-loai" hidden></div>

      <label for="ly-do">Lý do (ly_do)</label>
      <p class="phu">Một câu, nói rõ điều kiện nào bị bỏ hoặc bị đổi. Dùng nút "Chèn mẫu câu" ở bảng D1–D6. Chỗ “câu trích” là câu nguyên văn từ tài liệu, đặt trong ngoặc kép; đừng ghi mã đoạn vào đó (mã đoạn đã nằm ở bằng chứng).</p>
      <textarea id="ly-do" rows="3"></textarea>

      <label for="ghi-chu">Ghi chú (ghi_chu)</label>
      <p class="phu">Nhiều mục cách nhau "; " (mục 8). mac_dinh=… mọi khóa tuyên bố không nêu, từ D1a tới D6, không ghi ở D1 (bấm nút ở khung “Bước 3”). khang_dinh=… từ khẳng định, bắt buộc ở D2. chua_xac_dinh=… cụm làm D1a (chữ trỏ nhiều chế độ, cụm không giải được); D1a phải ghi nguyên nhân bằng chua_xac_dinh hoặc mac_dinh của khóa “Không có mặc định”. chep_nhan=… tuyên bố chép đúng nhãn của tài liệu (mục 6.8), khi đó không ghi mac_dinh cho điều kiện đó. nham_vai=… con số điều kiện bị dùng làm giá trị. ngoai_cau_hinh=… điều kiện hướng dẫn chưa có, người gán tự xác định. ngoai_sau_loai=… điều kiện không xếp được vào sáu loại.</p>
      <textarea id="ghi-chu" rows="2"></textarea>

      <label class="kiem"><input id="mau-thuan" type="checkbox"> Tài liệu mâu thuẫn (tai_lieu_mau_thuan)</label>
      <p class="phu">Tự tick khi bấm “Dừng ở đây” ở D1b (tài liệu ghi hai số khác nhau cho cùng điều kiện, nhãn Chưa đủ) và tự bỏ tick khi chuyển sang dòng khác. Chỉ dòng D1b mới được tick.</p>

      <label for="cau-hoi">Câu hỏi nhãn (tùy chọn) - chỗ hướng dẫn chưa rõ</label>
      <p class="phu">Chỗ hướng dẫn chưa rõ: ghi vào đây, đừng tự đặt quy tắc. Tuyên bố còn thiếu điều kiện so với bài quảng cáo: ghi <code>tach=…</code> (thiếu gì) và vẫn gán theo tuyên bố (mục 1, bước 0).</p>
      <textarea id="cau-hoi" rows="2"></textarea>

      <div id="loi" role="alert" hidden></div>
      <div id="nhac" hidden></div>
      <p id="tin" hidden></p>

      <div class="hang-nut">
        <button id="btn-truoc" type="button">Trước</button>
        <button id="btn-sau" type="button">Sau</button>
        <button id="btn-luu" type="button" class="chinh">Lưu và sang tuyên bố sau</button>
      </div>
    </form>
  </section>

  <aside id="cot-phai" aria-label="Tài liệu của mẫu">
    <div id="khung-tim" class="khung" style="margin-bottom:8px">
      <h2>Tài liệu của mẫu <span id="ten-mau" class="phu"></span></h2>
      <input id="tim" type="search" placeholder="Tìm trong tài liệu (không phân biệt hoa thường)" autocomplete="off">
      <p id="dem-doan" class="phu"></p>
    </div>
    <div id="doan"></div>
  </aside>
</main>

<aside id="huong-dan" role="dialog" aria-label="Hướng dẫn gán nhãn đầy đủ" hidden>
  <div class="hdan-dau">
    <strong>Hướng dẫn gán nhãn đầy đủ</strong>
    <span class="phu" style="margin:0">Dùng Ctrl+F để tìm</span>
    <button id="btn-dong-hd" type="button" class="nho dong">Đóng</button>
  </div>
  <div id="hdan-nd" class="md"></div>
</aside>

<script id="du-lieu" type="application/json">__DU_LIEU__</script>
<script>
(function () {
'use strict';

const $ = (id) => document.getElementById(id);
const DL = JSON.parse($('du-lieu').textContent);
const TB = DL.tuyen_bo;
const HD = DL.huong_dan;
const TRANG = DL.trang; // lượt, khóa lưu, tên tệp tải về: chữ lấy từ scripts/tao_cong_cu_gan_nhan.py
const LUOT = TRANG.luot;
const KHOA = TRANG.khoa_nhan;
const KHOA_GD = TRANG.khoa_giao_dien;
const NGHI_MS = TRANG.nghi_ms; // không thao tác quá chừng này thì đồng hồ dừng đếm
const MA_NHAN = ['DUNG', 'SAI', 'LECH', 'CHUA_DU'];
// Loại biến đổi theo nhãn (hướng dẫn mục 8): LECH luôn có loại; SAI chỉ ghi doi_gia_tri, hoặc doi_bo_phan / doi_phien_ban
// khi gán nhầm bộ phận, phiên bản mà không trùng số nào; DUNG và CHUA_DU để trống.
const LOAI_LECH = ['bo_dieu_kien', 'doi_dieu_kien', 'doi_bo_phan', 'doi_phien_ban', 'doi_kieu_gia_tri'];
const LOAI_SAI = ['doi_gia_tri', 'doi_bo_phan', 'doi_phien_ban'];
const LOAI_TAT_CA = LOAI_LECH.concat(['doi_gia_tri']);
const LOAI_THEO_NHAN = { LECH: LOAI_LECH, SAI: LOAI_SAI };
const GIAI_THICH_LOAI = {};
for (const l of HD.loai) GIAI_THICH_LOAI[l.ma] = l.giai_thich;
// Chữ ngắn trong ô chọn (ô chọn không xuống dòng); nguyên văn mục 8 nằm ở chú thích khi rê chuột.
const CHU_LOAI = {
  LECH: { bo_dieu_kien: 'Quảng cáo không nói gì về điều kiện', doi_dieu_kien: 'Có nói điều kiện nhưng sai (chế độ, phụ kiện, cách đo)',
    doi_bo_phan: 'Gắn số cho nhầm bộ phận', doi_phien_ban: 'Gắn số cho nhầm phiên bản',
    doi_kieu_gia_tri: 'Đổi kiểu con số ("lên đến" thành "luôn", điển hình thành định mức)' },
  SAI: { doi_gia_tri: 'Con số sai', doi_bo_phan: 'Nói về bộ phận khác, không trùng số nào',
    doi_phien_ban: 'Nói về phiên bản khác, không trùng số nào' }
};
function tieuDeLoai(m) { return GIAI_THICH_LOAI[m] ? 'Hướng dẫn mục 8: ' + GIAI_THICH_LOAI[m] : ''; }
// Dòng D (hướng dẫn mục 7): nhãn tự điền, loại và tick tự đặt theo dòng người gán dừng ở; chữ lấy từ scripts/tao_cong_cu_gan_nhan.py.
const MA_DONG = HD.dong_d.map((d) => d.ma);
const DONG_MAP = {};
for (const d of HD.dong_d) DONG_MAP[d.ma] = d;
/* >>> LUAT_KIEM: luật kiểm không đụng DOM, bản JavaScript của scripts/kiem_nhan.py (test chạy riêng khối này trong node) */
const TBAO = DL.quy_tac.thong_bao; // thông báo lỗi, cùng chữ với scripts/kiem_nhan.py
const NHAC = DL.quy_tac.nhac;
const dien = (mau, v) => mau.replace(/\{(\w+)\}/g, (m, k) => (k in v ? String(v[k]) : m));
const RE_GIU_CHO = /\{[^{}]*\}/g;
// Cùng tập khoảng trắng với scripts/kiem_nhan.py, để công cụ và script kiểm chuẩn hóa như nhau.
const KT = /[\t\n\v\f\r \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]+/g;
const KT1 = /[\t\n\v\f\r \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]/;
const chuanHoa = (s) => String(s).normalize('NFC').replace(KT, ' ').trim();
// Mã đoạn <ma_mau>#<số> trong ngoặc kép của lý do (S14): chuỗi biểu thức lấy từ Python, cùng với kiem_nhan.py.
const RE_NGOAC_KEP = new RegExp(DL.quy_tac.re_ngoac_kep, 'g');
const RE_MA_DOAN = new RegExp(DL.quy_tac.re_ma_doan);
// Điều kiện theo nhóm (tiền tố ma_mau) và thuộc tính: { 'dt|do_sang': { che_do_hien_thi: 'Chế độ hiển thị' } } cho điều kiện
// "không có mặc định"; { 'dt|sac_nhanh': { cach_sac: { dieu_kien, hieu } } } cho điều kiện có cách hiểu mặc định.
const KHONG_CO = {};
const CO_MAC_DINH = {};
const KHOA_GHI_DUOC = {}; // khóa được ghi vào mac_dinh= (mục 8): khóa bảng mục 5 trừ "như hãng công bố"; cộng ngoai_bang (QĐ10)
for (const h of HD.mac_dinh) {
  const kn = h.nhom + '|' + h.thuoc_tinh;
  for (const k of h.khoa) {
    if (k.gia_tri === 'khong_co_mac_dinh') (KHONG_CO[kn] = KHONG_CO[kn] || {})[k.khoa] = h.dieu_kien;
    else (CO_MAC_DINH[kn] = CO_MAC_DINH[kn] || {})[k.khoa] = { dieu_kien: h.dieu_kien, hieu: h.hieu };
    if (k.gia_tri !== 'nhu_hang_cong_bo') {
      const ds = (KHOA_GHI_DUOC[kn] = KHOA_GHI_DUOC[kn] || []);
      if (!ds.includes(k.khoa)) ds.push(k.khoa);
    }
  }
}
const KHOA_NGOAI_BANG = 'ngoai_bang';
// Từ khẳng định hợp lệ cho khang_dinh=<từ> (S17): đọc từ mục 6.2 của hướng dẫn lúc sinh trang.
const TU_HOP_LE = HD.tu_khang_dinh.tu_hop_le.map((t) => chuanHoa(t).toLowerCase());
const DS_TU_KHANG_DINH = HD.tu_khang_dinh.tu_hop_le.join(', ');
// Đơn vị của thuộc tính (cột Đơn vị mục 6.1) và biểu thức nhận nó trong câu trích đã hạ chữ thường (S15).
const DON_VI = {};
for (const h of HD.huong_loi) DON_VI[h.nhom + '|' + h.thuoc_tinh] = { don_vi: h.don_vi, re: new RegExp(h.don_vi_mau) };
// Mục "ten=giá trị" của ô ghi chú (các mục cách nhau "; "); cùng biểu thức với scripts/kiem_nhan.py.
function giaTriMuc(v, ten) {
  const m = new RegExp('(^|;\\s*)' + ten + '=([^;]*)').exec(v);
  return m ? m[2] : null;
}
function layMuc(v, ten) {
  const g = giaTriMuc(v, ten);
  return g === null ? [] : g.split(',').map((x) => x.trim()).filter(Boolean);
}
const layMacDinh = (v) => layMuc(v, 'mac_dinh');
function layChuaXacDinh(v) {
  const g = giaTriMuc(v, 'chua_xac_dinh');
  return g === null ? '' : g.trim();
}
function maDoanTrongNgoac(lyDo) {
  for (const m of String(lyDo).matchAll(RE_NGOAC_KEP)) {
    const x = RE_MA_DOAN.exec(m[1]);
    if (x) return x[0];
  }
  return '';
}
// Luật về ô ghi chú, lý do và câu trích của một bản ghi r (dong_d, nhan, loai, ghi_chu, ly_do, trich) với nhomTt = 'dt|do_sang'.
// Trả về { loi: [...] (chặn lưu), nhac: [...] (chỉ nhắc) }. Chỉ dùng các ô người gán điền và nhóm, thuộc tính ghi sẵn.
function luatKiem(r, nhomTt) {
  const loi = [], nhac = [];
  const d = r.dong_d, gc = r.ghi_chu || '';
  const khongCo = KHONG_CO[nhomTt] || {}, coMacDinh = CO_MAC_DINH[nhomTt] || {};
  const khoa = Array.from(new Set(layMacDinh(gc)));
  if (d !== 'D1') { // khóa của mac_dinh= phải là khóa ghi được của thuộc tính (mục 8; D1 không ghi mac_dinh, chỉ nhắc)
    const ghiDuoc = KHOA_GHI_DUOC[nhomTt] || [];
    for (const k of khoa) {
      if (k !== KHOA_NGOAI_BANG && !ghiDuoc.includes(k)) loi.push(dien(TBAO.mac_dinh_khoa_la, { khoa: k, ds: ghiDuoc.join(', ') || '(không có)' }));
    }
  }
  if (d && d !== 'D1a' && d !== 'D1') { // mac_dinh=<khóa> của điều kiện "không có mặc định" thì phải dừng ở D1a (D1 không ghi mac_dinh)
    for (const k of khoa) if (khongCo[k]) loi.push(dien(TBAO.mac_dinh_khong_co, { khoa: k, dieu_kien: khongCo[k] }));
  }
  if (d === 'D1a' && !khoa.some((k) => khongCo[k]) && !layChuaXacDinh(gc)) { // D1a phải ghi nguyên nhân (S18)
    loi.push(dien(TBAO.d1a_thieu_nguyen_nhan, { ds: Object.keys(khongCo).join(', ') || '(thuộc tính này không có khóa nào)' }));
    for (const k of khoa) {
      if (coMacDinh[k]) loi.push(dien(TBAO.d1a_mac_dinh_co_mac_dinh, { khoa: k, dieu_kien: coMacDinh[k].dieu_kien, hieu: coMacDinh[k].hieu }));
    }
  }
  if (d === 'D2') { // D2 phải ghi từ khẳng định có trong mục 6.2 (S17)
    const tu = Array.from(new Set(layMuc(gc, 'khang_dinh')));
    if (!tu.length) loi.push(dien(TBAO.d2_thieu_khang_dinh, { ds: DS_TU_KHANG_DINH }));
    for (const t of tu) if (!TU_HOP_LE.includes(chuanHoa(t).toLowerCase())) loi.push(dien(TBAO.d2_khang_dinh_la, { tu: t, ds: DS_TU_KHANG_DINH }));
  }
  const ma = maDoanTrongNgoac(r.ly_do || ''); // lý do chép mã đoạn vào chỗ câu trích (S14)
  if (ma) loi.push(dien(TBAO.ly_do_ma_doan, { ma: ma }));
  if (r.nhan === 'LECH' && r.loai === 'bo_dieu_kien' && !khoa.length) nhac.push(NHAC.bo_dieu_kien_thieu_mac_dinh);
  if (d === 'D1' && khoa.length) nhac.push(NHAC.d1_co_mac_dinh); // S19
  const dv = DON_VI[nhomTt]; // S15: câu trích phải có đơn vị của thuộc tính
  const trich = (r.trich || '').trim();
  if (dv && trich && !dv.re.test(chuanHoa(trich).toLowerCase())) {
    nhac.push(dien(NHAC.trich_thieu_don_vi, { thuoc_tinh: nhomTt.split('|')[1], don_vi: dv.don_vi }));
  }
  return { loi: loi, nhac: nhac };
}
// S16: các đoạn trong ds ({id, noi_dung, chu_thich}) chưa nằm trong daCo mà cũng chứa đúng chuỗi t (chuỗi người gán vừa bôi đen).
function doanCungChu(ds, daCo, t) {
  if (!t) return [];
  return ds.filter((d) => !daCo.includes(d.id)
    && (chuanHoa(d.noi_dung).includes(t) || (d.chu_thich || []).some((c) => chuanHoa(c).includes(t)))).map((d) => d.id);
}
// S20: "Nhập lại" chỉ nhận bản ghi đúng lượt của trang; bản ghi lượt khác (hoặc không có luot) bị từ chối.
function tachTheoLuot(moi, luot) {
  const dung = moi.filter((o) => o && o.luot === luot);
  const khac = moi.filter((o) => !(o && o.luot === luot));
  return { dung: dung, khac: khac.length, luot_khac: Array.from(new Set(khac.map((o) => (o && o.luot !== undefined ? o.luot : 'không có')))) };
}
// S21: không thao tác quá nghiMs thì thời gian trôi qua (dt) cộng vào ms_nghi thay vì ms.
const quaNghi = (bayGio, hoatDongCuoi, nghiMs) => bayGio - hoatDongCuoi > nghiMs;
function congGio(r, dt, nghi) { if (nghi) r.ms_nghi += dt; else r.ms += dt; }
/* <<< LUAT_KIEM */

const DOAN_MAP = {};
for (const m of Object.keys(DL.doan)) {
  DOAN_MAP[m] = {};
  for (const d of DL.doan[m]) DOAN_MAP[m][d.id] = d;
}

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
}
const chuoi = (x) => (typeof x === 'string' ? x : '');
const noiLoai = (ds) => (ds.length > 1 ? ds.slice(0, -1).join(', ') + ' hoặc ' + ds[ds.length - 1] : ds.join(''));

/* ---------- Trạng thái ---------- */

const state = { nguoi_gan: 'phuoc', idx: 0, tamDung: false, ban_ghi: {} };
let luuOk = true;
let lanLuu = Date.now();
let chuaLuuGio = false;
const khongQua = new Set(); // mã tuyên bố đã lưu nhưng không qua quy tắc khi nạp lại trang

function banGhiMoi() {
  // ms: thời gian đã đếm; ms_nghi: thời gian đồng hồ đứng vì không thao tác quá NGHI_MS (ghi riêng, không cộng vào ms).
  return { nhan: '', dong_d: '', loai: '', bang_chung: [], trich: '', ly_do: '', ghi_chu: '', tai_lieu_mau_thuan: false,
           cau_hoi: '', ms: 0, ms_nghi: 0, da_gan: false, dung: false, nguoi_gan: '', nd_goc: '' };
}
// Nội dung nhãn của bản ghi (không tính số giây, câu hỏi, người gán). nd_goc giữ nội dung lúc nhập tệp hay lần lưu trước:
// "Lưu và sang" chỉ đổi người gán khi nội dung khác nd_goc, để bản ghi nhập từ tệp mà người duyệt không sửa giữ người gán cũ.
function noiDungNhan(r) {
  return JSON.stringify([r.nhan, r.dong_d, r.loai, r.bang_chung, r.trich.trim(), r.ly_do.trim(), !!r.tai_lieu_mau_thuan,
                         r.ghi_chu.trim()]);
}
function lamSach(x) {
  const r = banGhiMoi();
  r.nhan = MA_NHAN.includes(x.nhan) ? x.nhan : '';
  r.dong_d = MA_DONG.includes(x.dong_d) ? x.dong_d : ''; // bản ghi lưu trước khi có dòng D: để trống, không đoán
  r.loai = chuoi(x.loai);
  r.bang_chung = Array.isArray(x.bang_chung) ? x.bang_chung.filter((m) => typeof m === 'string') : [];
  r.trich = chuoi(x.trich); r.ly_do = chuoi(x.ly_do); r.ghi_chu = chuoi(x.ghi_chu); r.cau_hoi = chuoi(x.cau_hoi);
  r.tai_lieu_mau_thuan = x.tai_lieu_mau_thuan === true;
  r.ms = Number.isFinite(x.ms) && x.ms > 0 ? x.ms : 0;
  r.ms_nghi = Number.isFinite(x.ms_nghi) && x.ms_nghi > 0 ? x.ms_nghi : 0;
  r.da_gan = x.da_gan === true; r.dung = x.dung === true; r.nguoi_gan = chuoi(x.nguoi_gan); r.nd_goc = chuoi(x.nd_goc);
  return r;
}
function bg(i) {
  const id = TB[i].id;
  if (!state.ban_ghi[id]) state.ban_ghi[id] = banGhiMoi();
  return state.ban_ghi[id];
}
const coLoai = (nhan) => nhan === 'LECH' || nhan === 'SAI';

let canhBaoNap = '';
function capNhatCanhBao() {
  const o = $('canh-bao'), t = [];
  if (!luuOk) t.push('Không lưu được vào trình duyệt (localStorage bị chặn hoặc hỏng). Công cụ vẫn chạy, nhưng nhớ xuất tệp thường xuyên (nút "Tải nhãn"); đóng trang là mất nhãn chưa xuất.');
  if (canhBaoNap) t.push(canhBaoNap);
  o.hidden = !t.length;
  o.textContent = t.join(' ');
}
function luu() {
  lanLuu = Date.now(); chuaLuuGio = false;
  try {
    localStorage.setItem(KHOA, JSON.stringify({ v: 1, nguoi_gan: state.nguoi_gan, idx: state.idx, ban_ghi: state.ban_ghi }));
    if (!luuOk) { luuOk = true; capNhatCanhBao(); }
  } catch (e) {
    if (luuOk) { luuOk = false; capNhatCanhBao(); }
  }
}
function nap() {
  try {
    const t = localStorage.getItem(KHOA);
    if (!t) return;
    let d;
    try { d = JSON.parse(t); } catch (e) {
      try { localStorage.setItem(KHOA + '_hong', t); } catch (e2) { /* bỏ qua */ }
      canhBaoNap = 'Dữ liệu cũ trong trình duyệt bị hỏng nên không đọc được (đã chép sang khóa ' + KHOA + '_hong). Bắt đầu lại từ trống; nếu có tệp ' + TRANG.tep_nhan + ' đã xuất thì bấm "Nhập lại".';
      return;
    }
    if (typeof d.nguoi_gan === 'string' && d.nguoi_gan.trim()) state.nguoi_gan = d.nguoi_gan;
    if (Number.isInteger(d.idx) && d.idx >= 0 && d.idx < TB.length) state.idx = d.idx;
    for (const tb of TB) {
      const x = d.ban_ghi && d.ban_ghi[tb.id];
      if (x && typeof x === 'object') state.ban_ghi[tb.id] = lamSach(x);
    }
  } catch (e) {
    luuOk = false; capNhatCanhBao();
  }
}
// Sau khi nạp: bản ghi đã gán mà không qua quy tắc hiện hành thì bỏ dấu "đã gán" (giữ nguyên dữ liệu và số giây).
function kiemLaiKhiNap() {
  TB.forEach((tb, i) => {
    const r = state.ban_ghi[tb.id];
    if (!r || !r.da_gan) return;
    if (kiem(i, r.nguoi_gan || state.nguoi_gan).length) { r.da_gan = false; r.dung = false; khongQua.add(tb.id); }
  });
}
let kyBanner = '';
function capNhatBannerLai() {
  const ds = TB.filter((tb) => khongQua.has(tb.id) && !(state.ban_ghi[tb.id] && state.ban_ghi[tb.id].da_gan)).map((tb) => tb.id);
  const thieuDong = ds.some((id) => !(state.ban_ghi[id] && state.ban_ghi[id].dong_d)); // có bản ghi cũ chưa chọn dòng D
  const ky = ds.join(',') + '|' + thieuDong;
  if (ky === kyBanner) return;
  kyBanner = ky;
  const o = $('canh-bao-lai');
  o.textContent = '';
  o.hidden = !ds.length;
  if (!ds.length) return;
  o.append('Các tuyên bố sau đã lưu nhưng không qua quy tắc mới, mở lại để sửa: ');
  ds.forEach((id, k) => {
    if (k) o.append(', ');
    const b = el('button', 'lien-ket', id);
    b.type = 'button'; b.dataset.mo = id;
    o.append(b);
  });
  if (thieuDong) o.append('. Trang mới cần bạn chọn dòng D cho các tuyên bố đã gán trước đây.');
}

/* ---------- Đồng hồ ---------- */

let last = Date.now();
let hoatDongCuoi = Date.now(); // lần thao tác gần nhất (phím, chuột, cuộn, chạm)
// Đồng hồ chỉ chạy khi: không tạm dừng, trang hiện và được chọn, tuyên bố chưa lưu, và có thao tác trong NGHI_MS gần đây.
// Không thao tác quá NGHI_MS thì thời gian trôi qua không cộng vào ms mà cộng vào ms_nghi (xuất ra là giay_nghi).
function canDem() {
  return !state.tamDung && document.visibilityState === 'visible' && document.hasFocus() && !bg(state.idx).dung;
}
function dangNghi() { return quaNghi(Date.now(), hoatDongCuoi, NGHI_MS); }
function dangDem() { return canDem() && !dangNghi(); }
function mmss(giay) {
  const p = Math.floor(giay / 60), s = giay % 60;
  return String(p).padStart(2, '0') + ':' + String(s).padStart(2, '0');
}
function capNhatDongHo() {
  const r = bg(state.idx);
  const dem = dangDem();
  $('dong-ho').textContent = mmss(Math.floor(r.ms / 1000));
  $('dong-ho').classList.toggle('dung', !dem);
  let tt = 'Đang đếm giờ.';
  if (!dem) {
    if (state.tamDung) tt = 'Đã tạm dừng (bấm "Tiếp tục").';
    else if (r.dung) tt = 'Đã lưu nên đồng hồ dừng; sửa lại nhãn thì đếm tiếp.';
    else if (document.visibilityState !== 'visible') tt = 'Trang đang ẩn nên đồng hồ dừng.';
    else if (!document.hasFocus()) tt = 'Cửa sổ chưa được chọn nên đồng hồ dừng (bấm vào trang để đếm tiếp).';
    else tt = 'Không thao tác quá ' + Math.round(NGHI_MS / 60000) + ' phút nên đồng hồ dừng (thao tác lại để đếm tiếp).';
  }
  if (r.ms_nghi > 0) tt += ' Đã bỏ ' + Math.round(r.ms_nghi / 1000) + ' giây lúc không thao tác.';
  $('trang-thai-dh').textContent = tt;
  $('btn-tam-dung').textContent = state.tamDung ? 'Tiếp tục' : 'Tạm dừng';
}
function tick() {
  const now = Date.now();
  const dt = Math.min(Math.max(now - last, 0), 1000); // trần 1 giây: trình duyệt hãm bộ đếm khi trang ẩn
  last = now;
  if (dt > 0 && canDem()) {
    congGio(bg(state.idx), dt, dangNghi());
    chuaLuuGio = true;
  }
  capNhatDongHo();
  if (chuaLuuGio && now - lanLuu > 5000) luu();
}

/* ---------- Danh sách tuyên bố (cột trái) ---------- */

let dsNut = [];
function ngan(s, n) {
  s = s.normalize('NFC');
  if (s.length <= n) return s;
  const c = s.slice(0, n), k = c.lastIndexOf(' ');
  return (k > n / 2 ? c.slice(0, k) : c) + '…';
}
function dungDanhSach() {
  const ol = $('ds');
  ol.textContent = '';
  dsNut = TB.map((tb, i) => {
    const li = el('li');
    const b = el('button', 'muc');
    b.type = 'button'; b.dataset.i = String(i);
    b.append(el('span', 'dau-gan', '○'), el('span', 'ma-muc', tb.id), el('span', 'tt', ngan(tb.tuyen_bo, 38)));
    b.title = tb.tuyen_bo;
    li.append(b); ol.append(li);
    return b;
  });
  capNhatDanhSach();
}
function capNhatDanhSach() {
  let xong = 0;
  dsNut.forEach((b, i) => {
    const r = state.ban_ghi[TB[i].id];
    const x = !!(r && r.da_gan);
    if (x) xong++;
    b.classList.toggle('xong', x);
    b.classList.toggle('dang-mo', i === state.idx);
    b.firstChild.textContent = x ? '✓' : '○';
  });
  $('tien-do').textContent = 'Đã gán ' + xong + ' / ' + TB.length;
  capNhatBannerLai();
  const it = dsNut[state.idx], ol = $('ds');
  if (it) {
    const top = it.parentElement.offsetTop, cao = it.offsetHeight;
    if (top < ol.scrollTop) ol.scrollTop = top;
    else if (top + cao > ol.scrollTop + ol.clientHeight) ol.scrollTop = top + cao - ol.clientHeight;
  }
}

/* ---------- Thẻ tuyên bố và bài quảng cáo (cột giữa) ---------- */

function dungThe() {
  const tb = TB[state.idx];
  $('the-ma').textContent = tb.id + '  (' + (state.idx + 1) + '/' + TB.length + ')';
  $('the-tb').textContent = tb.tuyen_bo;
  const dl = $('the-chi-tiet');
  dl.textContent = '';
  [['Thuộc tính', tb.thuoc_tinh], ['Mã bài', tb.ma_qc], ['LLM', tb.llm_sinh], ['Chế độ', tb.che_do], ['Loại bài', tb.loai_bai]]
    .forEach(([k, v]) => { dl.append(el('dt', '', k), el('dd', '', v)); });
  // Không hiện ghi chú của tuyên bố (tach_sua=…): khi gán chỉ đọc chữ của tuyên bố (hướng dẫn mục 1, bước 0). Dữ liệu vẫn nhúng.
}

// Tô sáng cau_goc trong bài. So sau khi NFC và gộp khoảng trắng; bản đồ ban[k] = vị trí trong bài gốc của ký tự thứ k.
let markDau = null; // mark đầu tiên của câu gốc trong bài đang hiện
function cuonBai() { // khung bài đóng sẵn nên chỉ cuộn được khi đã mở
  const box = $('bai');
  if ($('kh-bai').open) box.scrollTop = markDau ? Math.max(0, markDau.offsetTop - box.clientHeight / 3) : 0;
}
function dungBai() {
  const tb = TB[state.idx];
  const bai = DL.bai[tb.ma_qc];
  const box = $('bai');
  box.textContent = '';
  markDau = null;
  $('bai-ten').textContent = bai && bai.ten_nhap ? '(sản phẩm nhập: ' + bai.ten_nhap + ')' : '';
  if (!bai) { box.textContent = '(không có bài ' + tb.ma_qc + ')'; return; }
  const goc = bai.noi_dung.normalize('NFC');
  let g = '';
  const ban = [];
  for (let j = 0; j < goc.length; j++) {
    if (KT1.test(goc[j])) {
      if (g.length && g[g.length - 1] !== ' ') { g += ' '; ban.push(j); }
    } else { g += goc[j]; ban.push(j); }
  }
  const cg = chuanHoa(tb.cau_goc);
  const doan = [];
  if (cg) {
    let tu = 0, p;
    while ((p = g.indexOf(cg, tu)) !== -1) {
      doan.push([ban[p], ban[p + cg.length - 1] + 1]);
      tu = p + cg.length;
    }
  }
  let vt = 0, dau = null;
  for (const [a, b] of doan) {
    box.append(document.createTextNode(goc.slice(vt, a)));
    const m = el('mark', '', goc.slice(a, b));
    if (!dau) dau = m;
    box.append(m);
    vt = b;
  }
  box.append(document.createTextNode(goc.slice(vt)));
  markDau = dau;
  cuonBai();
}

/* ---------- Khung hướng dẫn trong biểu mẫu ---------- */

// Bảng D1-D6 (Bước 4): giống nhau cho mọi tuyên bố, dựng một lần; capNhatKhungD tô dòng đang chọn của tuyên bố đang mở.
function dungKhungD() {
  const goc = $('d-ds');
  goc.textContent = '';
  for (const d of HD.dong_d) {
    const nd = el('div', 'd-nd');
    const ch = el('div', 'd-cau-hoi', d.cau_hoi);
    ch.dataset.mau = d.cau_hoi; // D1 có chỗ {thuoc_tinh}: capNhatKhungD điền tên thuộc tính của tuyên bố đang mở
    nd.append(ch, el('div', 'd-nhan', '→ Nhãn: ' + d.nhan_hien_thi));
    if (d.ghi_chu_nho) nd.append(el('div', 'd-luu-y', d.ghi_chu_nho));
    const kt = el('div', 'd-luu-y'); kt.innerHTML = 'Kiểm tra (hướng dẫn): ' + d.kiem_tra_html;
    nd.append(kt);
    if (d.luu_y_html) {
      const ly = el('div', 'd-luu-y'); ly.innerHTML = 'Lưu ý: ' + d.luu_y_html;
      nd.append(ly);
    }
    const mau = el('div', 'd-mau');
    const van = el('span', 'van'); van.innerHTML = d.mau_cau_html;
    const nut = el('button', 'nho', 'Chèn mẫu câu');
    nut.type = 'button'; nut.dataset.chen = d.ma;
    mau.append(van, nut);
    nd.append(mau);
    const hang_nut = el('div', 'd-nut');
    const vd = el('button', 'nho', 'Ví dụ');
    vd.type = 'button'; vd.dataset.vd = d.ma; vd.setAttribute('aria-expanded', 'false');
    const dung = el('button', 'nho dung-o', 'Dừng ở đây');
    dung.type = 'button'; dung.dataset.dung = d.ma; dung.setAttribute('aria-pressed', 'false');
    hang_nut.append(vd, dung);
    const vi = el('div', 'd-vi-du');
    vi.hidden = true;
    vi.append(el('strong', '', d.vi_du_ma ? 'Ví dụ (' + d.vi_du_ma + '): ' : 'Ví dụ giả định: '), document.createTextNode(d.vi_du));
    nd.append(hang_nut, vi);
    const hang = el('div', 'd-hang');
    hang.dataset.dong = d.ma;
    hang.append(el('div', 'd-ma', d.ma), nd);
    goc.append(hang);
  }
}
// Mở/đóng ví dụ của một dòng D (đóng sẵn).
function bamViDu(ma) {
  const hang = document.querySelector('.d-hang[data-dong="' + ma + '"]');
  if (!hang) return;
  const vi = hang.querySelector('.d-vi-du'), nut = hang.querySelector('button[data-vd]');
  vi.hidden = !vi.hidden;
  nut.textContent = vi.hidden ? 'Ví dụ' : 'Ẩn ví dụ';
  nut.setAttribute('aria-expanded', vi.hidden ? 'false' : 'true');
}
// Tô dòng D người gán đã chọn cho tuyên bố đang mở và ghi trạng thái ở đầu bảng.
function tenThuocTinh(tb) { // tên thuộc tính ghi sẵn trên tuyên bố, lấy từ bảng mục 5; không có thì mã thuộc tính
  return HD.ten_thuoc_tinh[tb.ma_mau.split('-')[0] + '|' + tb.thuoc_tinh] || tb.thuoc_tinh;
}
function capNhatKhungD() {
  const r = bg(state.idx);
  const ten = tenThuocTinh(TB[state.idx]);
  document.querySelectorAll('#d-ds .d-hang').forEach((h) => {
    const ch = h.querySelector('.d-cau-hoi');
    ch.textContent = dien(ch.dataset.mau, { thuoc_tinh: '“' + ten + '”' });
    const on = h.dataset.dong === r.dong_d;
    h.classList.toggle('chon', on);
    const b = h.querySelector('button[data-dung]');
    b.classList.toggle('chinh', on);
    b.textContent = on ? 'Đang dừng ở đây' : 'Dừng ở đây';
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
  const d = DONG_MAP[r.dong_d];
  $('d-trang-thai').textContent = d ? 'Đang dừng ở ' + d.ma + ' → nhãn: ' + d.nhan_hien_thi + '.'
    : 'Chưa chọn dòng nào. Bấm “Dừng ở đây” ở dòng đầu tiên đúng với tuyên bố.';
}
// "Dừng ở đây": đặt dong_d và tự đặt nhãn, loại (D2), tick tài liệu mâu thuẫn (D1b). Các ô khác giữ nguyên; loại cũ chỉ
// giữ khi còn hợp lệ với nhãn mới và dòng cũ không phải D2 (loại D2 do trang tự đặt). Bản ghi cũ chưa có dong_d: lần chọn
// đầu giữ loại và tick như cũ (trừ D1b, D2 tự đặt), sai thì phần kiểm báo.
function chonDong(ma) {
  const d = DONG_MAP[ma], r = bg(state.idx);
  if (!d) return;
  const truoc = [r.dong_d, r.nhan, r.loai, r.tai_lieu_mau_thuan].join('|');
  const cu = r.dong_d;
  r.dong_d = ma;
  r.nhan = d.nhan_ma;
  if (d.loai_tu_dong) r.loai = d.loai_tu_dong;
  else if (cu === 'D2' || !(LOAI_THEO_NHAN[r.nhan] || []).includes(r.loai)) r.loai = '';
  if (d.tu_tick) r.tai_lieu_mau_thuan = true;
  else if (cu) r.tai_lieu_mau_thuan = false; // bấm dòng thì tick theo dòng đó; bản ghi cũ chưa có dòng giữ ô như cũ
  if ([r.dong_d, r.nhan, r.loai, r.tai_lieu_mau_thuan].join('|') === truoc) return; // bấm lại đúng dòng đang chọn: không đổi gì
  $('mau-thuan').checked = r.tai_lieu_mau_thuan;
  capNhatNut(); capNhatKhungD(); suaDoi(false);
}
// Chèn mẫu câu vào ô Lý do như người gán gõ: ô đã có chữ thì xuống dòng rồi nối; đi qua đúng sự kiện input.
function chenMau(ma) {
  const d = HD.dong_d.find((x) => x.ma === ma);
  if (!d) return;
  const o = $('ly-do');
  const cu = o.value;
  const dau = cu.trim() ? cu + (/\n$/.test(cu) ? '' : '\n') : '';
  o.value = dau + d.mau_cau;
  o.dispatchEvent(new Event('input', { bubbles: true }));
  o.focus();
  const m = /\{[^{}]*\}/.exec(d.mau_cau);
  if (m) o.setSelectionRange(dau.length + m.index, dau.length + m.index + m[0].length);
  else o.setSelectionRange(o.value.length, o.value.length);
}

const RE_MAC_DINH = /(^|;\s*)mac_dinh=([^;]*)/; // layMacDinh nằm ở khối LUAT_KIEM
// Thêm khóa vào mục mac_dinh của ô Ghi chú (chưa có mục thì thêm mục, nối bằng "; "); đi qua sự kiện input.
function themMacDinh(khoa) {
  const o = $('ghi-chu');
  const v = o.value;
  const m = RE_MAC_DINH.exec(v);
  let moi;
  if (m) {
    if (layMacDinh(v).includes(khoa)) return;
    const dauGiaTri = m.index + m[0].length - m[2].length;
    const giaTri = m[2].replace(/\s+$/, '');
    moi = v.slice(0, dauGiaTri) + giaTri + (giaTri.trim() ? ',' : '') + khoa + v.slice(dauGiaTri + giaTri.length);
  } else {
    const cu = v.replace(/[\s;]+$/, '');
    moi = cu ? cu + '; mac_dinh=' + khoa : 'mac_dinh=' + khoa;
  }
  o.value = moi;
  o.dispatchEvent(new Event('input', { bubbles: true }));
}
function capNhatNutMacDinh() {
  const co = layMacDinh($('ghi-chu').value);
  document.querySelectorAll('#md-nd button[data-khoa]').forEach((b) => {
    const da = co.includes(b.dataset.khoa);
    b.classList.toggle('da-them', da);
    b.setAttribute('aria-pressed', da ? 'true' : 'false');
  });
}
// Ca đặc biệt của hướng dẫn cho đúng mẫu (hoặc nhóm) và thuộc tính ghi sẵn trên tuyên bố; không đọc câu tuyên bố.
function dungCaDacBiet() {
  const tb = TB[state.idx];
  const nhom = tb.ma_mau.split('-')[0];
  const goc = $('cdb-nd');
  goc.textContent = '';
  const ds = DL.ca_dac_biet.filter((c) => (c.ma_mau ? c.ma_mau === tb.ma_mau : c.nhom === nhom)
    && (!c.thuoc_tinh || c.thuoc_tinh === tb.thuoc_tinh));
  if (!ds.length) { goc.append(el('p', '', 'Hướng dẫn không có ca đặc biệt cho thuộc tính này.')); return; }
  for (const c of ds) {
    const d = el('div', 'md-hang');
    d.append(el('strong', '', c.tieu_de), el('div', '', c.noi_dung), el('p', 'phu-nho', 'Nguồn: ' + c.nguon));
    goc.append(d);
  }
}
// Cách hiểu mặc định của đúng nhóm (tiền tố ma_mau) và thuộc tính ghi sẵn trên tuyên bố đang mở.
function dungMacDinh() {
  const tb = TB[state.idx];
  const nhom = tb.ma_mau.split('-')[0];
  const goc = $('md-nd');
  goc.textContent = '';
  goc.append(el('p', 'phu-nho', (HD.nhom[nhom] || nhom) + ' · ' + tb.thuoc_tinh));
  const hang = HD.mac_dinh.filter((h) => h.nhom === nhom && h.thuoc_tinh === tb.thuoc_tinh);
  if (!hang.length) goc.append(el('p', '', 'Hướng dẫn chưa có cách hiểu mặc định cho thuộc tính này.'));
  for (const h of hang) {
    // Mỗi hàng của bảng mục 5 thành một câu nếu-thì; hàng "không có mặc định" tô đỏ nhạt và dẫn tới D1a.
    const khongCo = h.khoa.some((k) => k.gia_tri === 'khong_co_mac_dinh');
    const d = el('div', 'md-hang' + (khongCo ? ' khong-co' : ''));
    const cau = el('div', 'md-cau');
    if (khongCo) cau.append(el('span', 'md-the', 'Không có mặc định'));
    cau.append('Tuyên bố không nói ', el('strong', '', h.dieu_kien));
    if (khongCo) {
      cau.append(' → dừng ở D1a, nhãn Chưa đủ thông tin.');
    } else {
      const hieu = el('span', 'md-hieu'); hieu.innerHTML = h.hieu_html.replace(/\.\s*$/, '');
      cau.append(' → coi như tuyên bố nói: ', hieu, '. Rồi dò tiếp.');
    }
    d.append(cau);
    const khoa = h.khoa.filter((k) => k.gia_tri !== 'nhu_hang_cong_bo');
    if (khoa.length) {
      const nn = el('div', 'md-nut');
      for (const k of khoa) {
        const b = el('button', 'nho', 'mac_dinh=' + k.khoa);
        b.type = 'button'; b.dataset.khoa = k.khoa; b.title = k.khoa + ': ' + k.gia_tri;
        nn.append(b);
      }
      d.append(nn, el('div', 'md-ghi', 'Nhãn dựa vào dòng này thì ghi mac_dinh=' + khoa.map((k) => k.khoa).join(',') + ' vào ghi chú.'));
    }
    for (const ks of h.khao_sat || []) {
      const l = el('div', 'md-ghi');
      const qd = el('span'); qd.innerHTML = ks.quyet_dinh_html;
      l.append('Khảo sát Bước 10: ' + ks.hieu_khac + ' người hiểu khác → ', qd);
      d.append(l);
    }
    goc.append(d);
  }
  const hl = HD.huong_loi.find((h) => h.nhom === nhom && h.thuoc_tinh === tb.thuoc_tinh);
  if (hl) {
    const p = el('p', 'md-huong');
    p.append(el('strong', '', 'Hướng thuận lợi: '), hl.huong_loi + ' ', el('span', 'phu-nho', '(' + hl.huong_ma + ')'), ' · ',
             el('strong', '', 'Kiểu giá trị mặc định: '), hl.kieu_loi + ' ', el('span', 'phu-nho', '(' + hl.kieu_ma + ')'));
    goc.append(p);
  }
  capNhatNutMacDinh();
}

// Khung "Cụm điều kiện đã biết" (S23): phụ lục mục 13 lọc theo nhóm và theo các điều kiện của bảng mục 5 cho thuộc tính ghi sẵn
// trên tuyên bố đang mở. Không đọc câu tuyên bố.
function dungCumDieuKien() {
  const tb = TB[state.idx];
  const nhom = tb.ma_mau.split('-')[0];
  const goc = $('cum-nd');
  goc.textContent = '';
  goc.append(el('p', 'phu-nho', (HD.nhom[nhom] || nhom) + ' · ' + tb.thuoc_tinh));
  const hang = HD.mac_dinh.filter((h) => h.nhom === nhom && h.thuoc_tinh === tb.thuoc_tinh);
  const tenDk = {};
  for (const h of hang) for (const k of h.khoa) if (!(k.khoa in tenDk)) tenDk[k.khoa] = h.dieu_kien;
  const phuLuc = HD.cum.nhom[nhom] || [];
  const dkSo = new Set(); // điều kiện dạng số của thuộc tính này (giá trị gia_tri_so trong phụ lục)
  for (const dk of phuLuc) {
    if (!(dk.khoa in tenDk)) continue;
    const kq = el('div', 'md-hang');
    kq.append(el('strong', '', tenDk[dk.khoa]), el('span', 'phu-nho', ' (' + dk.khoa + ')'));
    for (const gt of dk.gia_tri) {
      if (gt.chi_thuoc_tinh && gt.chi_thuoc_tinh.length && !gt.chi_thuoc_tinh.includes(tb.thuoc_tinh)) continue; // chi_thuoc_tinh
      if (gt.gia_tri === 'gia_tri_so') dkSo.add(dk.khoa);
      kq.append(dongCum(gt.gia_tri, gt.tu_tai_lieu, gt.hieu_biet_chung));
    }
    goc.append(kq);
  }
  const thieu = Object.keys(tenDk).filter((k) => !phuLuc.some((dk) => dk.khoa === k));
  if (thieu.length) goc.append(el('p', 'phu-nho', 'Phụ lục chưa có cụm cho: ' + thieu.join(', ') + '.'));
  // Phần dùng chung (bảng 13.1): kiểu giá trị luôn hiện; chữ gọi mức cao chỉ với thuộc tính có chế độ hiển thị (độ sáng);
  // quan hệ của điều kiện dạng số chỉ khi thuộc tính có điều kiện dạng số.
  const hienChung = { kieu_gia_tri: true, tu_goi_muc_cao: 'che_do_hien_thi' in tenDk, cum_quan_he: dkSo.size > 0 };
  for (const c of HD.cum.chung) {
    if (!hienChung[c.khoa]) continue;
    const kq = el('div', 'md-hang');
    kq.append(el('strong', '', TEN_CUM_CHUNG[c.khoa]), el('span', 'phu-nho', ' (dùng chung, ' + c.khoa + ')'));
    for (const d of c.dong) kq.append(dongCum(d.muc_con, d.tu_tai_lieu, d.hieu_biet_chung));
    goc.append(kq);
  }
}
const TEN_CUM_CHUNG = { kieu_gia_tri: 'Kiểu giá trị', tu_goi_muc_cao: 'Chữ gọi mức cao', cum_quan_he: 'Quan hệ của điều kiện dạng số' };
function dongCum(ten, taiLieu, thuongGap) {
  const d = el('div', 'md-ghi');
  const ds = (xs) => xs.map((x) => '“' + x + '”').join(', ');
  const phan = [];
  if (taiLieu.length) phan.push('trong tài liệu ' + ds(taiLieu));
  if (thuongGap.length) phan.push('cách nói thường gặp ' + ds(thuongGap));
  d.append(el('code', '', ten || '–'), ' ' + (phan.length ? phan.join('; ') : '(theo tên sản phẩm hoặc con số trong tài liệu)'));
  return d;
}

/* ---------- Khung phủ: toàn văn hướng dẫn ---------- */

function dungHuongDan() {
  $('hdan-nd').innerHTML = HD.muc_luc_html + HD.html;
  for (const b of document.querySelectorAll('#nut-nhan [data-nhan]')) {
    const n = HD.nhan[b.dataset.nhan];
    if (n) b.title = n.dinh_nghia;
  }
}
function moHuongDan() {
  $('huong-dan').hidden = false;
  $('btn-hd').setAttribute('aria-expanded', 'true');
  $('btn-dong-hd').focus();
}
function dongHuongDan() {
  $('huong-dan').hidden = true;
  $('btn-hd').setAttribute('aria-expanded', 'false');
  $('btn-hd').focus();
}

/* ---------- Trạng thái mở/đóng các khung (khóa riêng, không ảnh hưởng nhãn) ---------- */

// Khóa giao diện: trạng thái các khung details và danh sách mã tuyên bố đang bị cảnh báo "không qua quy tắc mới"
// (để dải vàng còn nhắc ở các lần nạp sau cho tới khi người gán lưu lại). Không đụng khóa nhãn (KHOA).
function luuGiaoDien() {
  try {
    const o = {};
    document.querySelectorAll('details.hd').forEach((d) => { o[d.id] = d.open; });
    localStorage.setItem(KHOA_GD, JSON.stringify({ v: 1, details: o, khong_qua: Array.from(khongQua) }));
  } catch (e) { /* không lưu được thì thôi */ }
}
function napGiaoDien() {
  let saved = {}, kq = [];
  try {
    const t = localStorage.getItem(KHOA_GD);
    const d = t ? JSON.parse(t) : null;
    if (d && typeof d === 'object') {
      if (d.details && typeof d.details === 'object') saved = d.details;
      if (Array.isArray(d.khong_qua)) kq = d.khong_qua;
    }
  } catch (e) { saved = {}; kq = []; }
  for (const id of kq) {
    const r = typeof id === 'string' ? state.ban_ghi[id] : null;
    if (r && !r.da_gan) khongQua.add(id); // đã cảnh báo ở lần nạp trước mà chưa lưu lại
  }
  document.querySelectorAll('details.hd').forEach((d) => {
    if (typeof saved[d.id] === 'boolean') d.open = saved[d.id];
    d.addEventListener('toggle', luuGiaoDien);
  });
  luuGiaoDien();
}

/* ---------- Biểu mẫu nhãn ---------- */

// Ô chọn loại chỉ có các loại hợp lệ với nhãn đang chọn, mỗi loại kèm chữ ngắn (CHU_LOAI); khung gợi ý theo nhãn.
function dungOLoai() {
  const r = bg(state.idx), sel = $('loai');
  const loaiD = r.dong_d && DONG_MAP[r.dong_d] ? DONG_MAP[r.dong_d].loai_tu_dong : ''; // D2: chỉ có doi_kieu_gia_tri
  const hopLe = loaiD ? [loaiD] : (LOAI_THEO_NHAN[r.nhan] || []);
  const chu = CHU_LOAI[r.nhan] || {};
  $('loai-d2').hidden = !loaiD;
  $('goi-y-lech').hidden = !(r.nhan === 'LECH' && !loaiD);
  $('goi-y-sai').hidden = r.nhan !== 'SAI';
  sel.textContent = '';
  sel.append(new Option('- chọn -', ''));
  if (r.loai && !hopLe.includes(r.loai)) {
    const o = new Option(r.loai + ' (không hợp lệ với nhãn ' + r.nhan + ')', r.loai);
    o.disabled = true;
    sel.append(o);
  }
  for (const m of hopLe) {
    const o = new Option(m + ' · ' + (chu[m] || GIAI_THICH_LOAI[m] || ''), m);
    o.title = tieuDeLoai(m);
    sel.append(o);
  }
  sel.value = r.loai;
  sel.title = tieuDeLoai(sel.value);
}
function capNhatNut() {
  const r = bg(state.idx);
  document.querySelectorAll('#nut-nhan [data-nhan]').forEach((b) => {
    const on = b.dataset.nhan === r.nhan;
    b.classList.toggle('chon', on);
    b.setAttribute('aria-current', on ? 'true' : 'false');
  });
  $('o-loai').hidden = !coLoai(r.nhan);
  dungOLoai();
}
function dungBangChung() {
  const ul = $('bang-chung');
  ul.textContent = '';
  const r = bg(state.idx);
  if (!r.bang_chung.length) { ul.append(el('li', 'trong', '(chưa chọn đoạn nào)')); return; }
  for (const ma of r.bang_chung) {
    const li = el('li', 'bc');
    const a = el('button', 'lien-ket', ma); a.type = 'button'; a.dataset.ma = ma; a.title = 'Cuộn tới đoạn này ở cột phải';
    const x = el('button', 'nho', 'Xóa'); x.type = 'button'; x.dataset.xoa = ma;
    li.append(a, x); ul.append(li);
  }
}
function hienLoi(ds) {
  const o = $('loi');
  o.textContent = '';
  o.hidden = !ds.length;
  if (!ds.length) return;
  const ul = el('ul');
  ds.forEach((e) => ul.append(el('li', '', e)));
  o.append(el('strong', '', 'Chưa lưu được, cần sửa:'), ul);
}
function hienTin(ma, noi) {
  const o = $(ma);
  o.hidden = !noi;
  o.textContent = noi || '';
}
function napForm() {
  const r = bg(state.idx);
  $('trich').value = r.trich;
  $('ly-do').value = r.ly_do;
  $('ghi-chu').value = r.ghi_chu;
  $('mau-thuan').checked = r.tai_lieu_mau_thuan;
  $('cau-hoi').value = r.cau_hoi;
  hienLoi([]); hienTin('tin', ''); hienTin('nhac-trich', '');
  capNhatNut(); capNhatKhungD(); dungBangChung(); capNhatNhac();
  // Tuyên bố đã lưu mà không qua quy tắc mới: nói ngay chỗ cần sửa.
  if (khongQua.has(TB[state.idx].id) && !r.da_gan) hienLoi(kiem(state.idx, r.nguoi_gan || state.nguoi_gan));
}

// Kiểm một tuyên bố để tính là "đã gán". nguoi: tên người gán dùng để kiểm. Chỉ bắt chỗ các ô người gán điền mâu thuẫn
// nhau hoặc trái quy tắc (bản của scripts/kiem_nhan.py): không đọc nội dung tuyên bố để đoán nhãn hay dòng D.
const nhomTt = (tb) => tb.ma_mau.split('-')[0] + '|' + tb.thuoc_tinh; // chỉ nhóm và thuộc tính ghi sẵn
function kiem(i, nguoi) {
  const tb = TB[i], r = bg(i), e = [];
  const d = r.dong_d;
  if (!nguoi.trim()) e.push('Chưa nhập tên người gán (ô ở cột trái).');
  if (!d) {
    e.push(TBAO.chua_chon_dong);
  } else if (r.nhan !== DONG_MAP[d].nhan_ma) {
    e.push(dien(TBAO.nhan_khong_khop, { nhan: r.nhan || '(trống)', dong_d: d, nhan_mong: DONG_MAP[d].nhan_ma }));
  }
  if (r.nhan) {
    if (coLoai(r.nhan)) {
      const hopLe = LOAI_THEO_NHAN[r.nhan];
      if (!r.loai) e.push('Nhãn ' + r.nhan + ' phải chọn loại biến đổi.');
      else if (!LOAI_TAT_CA.includes(r.loai)) e.push('Loại biến đổi không hợp lệ: ' + r.loai + '.');
      else if (!hopLe.includes(r.loai)) {
        e.push('Nhãn ' + r.nhan + ' chỉ đi với ' + noiLoai(hopLe) + '; ' + r.loai + ' là loại của nhãn ' + (r.nhan === 'SAI' ? 'LECH' : 'SAI') + '.');
      }
    }
    if (r.nhan !== 'CHUA_DU' && !r.bang_chung.length) e.push('Nhãn ' + r.nhan + ' cần ít nhất một bằng chứng (chỉ CHUA_DU được để trống).');
  }
  if (d) {
    const loaiD = DONG_MAP[d].loai_tu_dong; // D2: loại phải là doi_kieu_gia_tri (loại ngoài LECH hoặc trống đã báo ở trên)
    if (loaiD && r.loai !== loaiD && (r.nhan !== 'LECH' || LOAI_LECH.includes(r.loai))) {
      e.push(dien(TBAO.d2_sai_loai, { loai: r.loai ? "'" + r.loai + "'" : 'trống' }));
    }
    if (DONG_MAP[d].tu_tick && !r.tai_lieu_mau_thuan) e.push(TBAO.d1b_thieu_tick);
    else if (!DONG_MAP[d].tu_tick && r.tai_lieu_mau_thuan) e.push(dien(TBAO.tick_khong_phai_d1b, { dong_d: d }));
  }
  // Ghi chú (mac_dinh, chua_xac_dinh, khang_dinh) và lý do (mã đoạn): luật chung với scripts/kiem_nhan.py, khối LUAT_KIEM.
  luatKiem(r, nhomTt(tb)).loi.forEach((x) => e.push(x));
  const mau = DOAN_MAP[tb.ma_mau] || {};
  for (const m of r.bang_chung) if (!mau[m]) e.push('Mã bằng chứng ' + m + ' không có trong tài liệu của mẫu ' + tb.ma_mau + '.');
  const dung = r.bang_chung.filter((m) => mau[m]).map((m) => mau[m]);
  // D1: tài liệu không có thông số, nên bằng chứng và câu trích để trống; khi đó bỏ các kiểm bằng chứng - câu trích.
  const d1Co = d === 'D1' && (r.bang_chung.length > 0 || r.trich.trim() !== '');
  if (d1Co) {
    e.push(TBAO.d1_co_bang_chung);
  } else if (r.bang_chung.length) {
    if (!r.trich.trim()) e.push('Có bằng chứng thì phải có câu trích.');
  } else if (r.trich.trim()) {
    e.push('Có câu trích nhưng chưa có bằng chứng: hãy thêm đoạn chứa câu trích làm bằng chứng.');
  }
  if (!d1Co && r.trich.trim() && dung.length) {
    // Nhãn đã lưu có thể chép kèm số chú thích của trang hãng (noi_dung_goc), nên chấp nhận cả bản trước khi bỏ ký hiệu.
    const kho = dung.map((d) => ({ nd: chuanHoa(d.noi_dung), goc: chuanHoa(d.noi_dung_goc || d.noi_dung), ct: (d.chu_thich || []).map(chuanHoa) }));
    let rong = false;
    for (const phan of r.trich.split(' | ')) {
      const p = chuanHoa(phan);
      if (!p) { rong = true; continue; }
      if (!kho.some((k) => k.nd.includes(p) || k.goc.includes(p) || k.ct.some((c) => c.includes(p)))) {
        e.push('Câu trích không nằm trong nội dung hay chú thích của các đoạn bằng chứng đã chọn: "' + p.slice(0, 80) + '"');
      }
    }
    if (rong) e.push('Câu trích có phần rỗng (hai dấu " | " liền nhau, hoặc ở đầu hay cuối).');
  }
  if (!r.ly_do.trim()) {
    e.push('Chưa viết lý do.');
  } else {
    const gc = r.ly_do.match(RE_GIU_CHO);
    if (gc) e.push('Lý do còn chỗ {…} chưa thay: ' + Array.from(new Set(gc)).join(', '));
  }
  return e;
}

// Lời nhắc (khung vàng, không chặn lưu) của tuyên bố i; bản của nhac_mot_dong trong scripts/kiem_nhan.py (khối LUAT_KIEM).
function nhacCuaTuyenBo(i) {
  return luatKiem(bg(i), nhomTt(TB[i])).nhac;
}
function capNhatNhac() {
  const n = nhacCuaTuyenBo(state.idx), o = $('nhac');
  o.textContent = '';
  o.hidden = !n.length;
  if (n.length) o.append(el('strong', '', 'Nhắc (vẫn lưu được): '), n.join(' '));
}

// Mọi thay đổi nhãn đều gỡ trạng thái "đã gán" (phải bấm Lưu lại) và cho đồng hồ chạy tiếp. cauHoi=true: chỉ đổi câu hỏi.
function suaDoi(cauHoi) {
  const r = bg(state.idx);
  if (!cauHoi) {
    r.da_gan = false; r.dung = false;
    if (!$('loi').hidden) hienLoi(kiem(state.idx, state.nguoi_gan)); // đang báo lỗi thì cập nhật theo chỗ vừa sửa
    capNhatNhac();
  }
  hienTin('tin', '');
  capNhatDanhSach(); luu();
}

/* ---------- Cột phải: tài liệu của mẫu ---------- */

let mauHT = null;
let doanEls = [];
function dungDoan() {
  const tb = TB[state.idx];
  if (mauHT !== tb.ma_mau) {
    mauHT = tb.ma_mau;
    const goc = $('doan');
    goc.textContent = '';
    doanEls = [];
    $('ten-mau').textContent = '(' + tb.ma_mau + ')';
    for (const d of DL.doan[tb.ma_mau] || []) {
      const a = el('article', 'doan');
      const dau = el('div', 'doan-dau');
      const nut = el('button', 'nho', 'Thêm làm bằng chứng');
      nut.type = 'button'; nut.dataset.id = d.id;
      dau.append(el('span', 'ma', d.id), nut);
      a.append(dau, el('div', 'noi-dung', d.noi_dung));
      for (const c of d.chu_thich || []) a.append(el('div', 'chu-thich', c));
      goc.append(a);
      doanEls.push({ el: a, nut: nut, id: d.id, kho: chuanHoa(d.noi_dung + ' ' + (d.chu_thich || []).join(' ')).toLowerCase() });
    }
  }
  $('tim').value = '';
  loc(); capNhatNutDoan();
  $('cot-phai').scrollTop = 0;
}
function loc() {
  const q = chuanHoa($('tim').value).toLowerCase();
  let n = 0;
  for (const d of doanEls) {
    const ok = !q || d.kho.includes(q);
    d.el.hidden = !ok;
    if (ok) n++;
  }
  $('dem-doan').textContent = q ? 'Hiện ' + n + ' / ' + doanEls.length + ' đoạn' : doanEls.length + ' đoạn';
}
function capNhatNutDoan() {
  const r = bg(state.idx);
  for (const d of doanEls) {
    const co = r.bang_chung.includes(d.id);
    d.nut.textContent = co ? 'Đã thêm' : 'Thêm làm bằng chứng';
    d.nut.disabled = co;
    d.el.classList.toggle('da-chon', co);
  }
}
function cuonToiDoan(ma) {
  const d = doanEls.find((x) => x.id === ma);
  if (!d) return;
  if (d.el.hidden) { $('tim').value = ''; loc(); }
  const cot = $('cot-phai');
  const y = d.el.getBoundingClientRect().top - cot.getBoundingClientRect().top + cot.scrollTop - $('khung-tim').offsetHeight - 8;
  cot.scrollTop = Math.max(0, y);
}
function layBoiDen() {
  const sel = window.getSelection();
  const cot = $('cot-phai');
  if (!sel || sel.rangeCount === 0 || sel.isCollapsed || !cot.contains(sel.anchorNode) || !cot.contains(sel.focusNode)) {
    hienTin('nhac-trich', 'Chưa có đoạn nào được bôi đen trong cột phải (tài liệu).');
    return;
  }
  const t = sel.toString().replace(KT, ' ').trim();
  if (!t) { hienTin('nhac-trich', 'Phần bôi đen không có chữ.'); return; }
  const o = $('trich');
  const cu = o.value.trim();
  o.value = cu ? cu + ' | ' + t : t;
  bg(state.idx).trich = o.value;
  hienTin('nhac-trich', '');
  suaDoi(false);
  hienGoiYDoan(doanCoChu(chuanHoa(t)));
}
// S16: các đoạn khác của mẫu (chưa là bằng chứng) cũng có đúng chuỗi người gán vừa bôi đen. Chỉ dùng chuỗi bôi đen và đoạn
// của mẫu; không đọc tuyên bố.
function doanCoChu(t) {
  return doanCungChu(DL.doan[TB[state.idx].ma_mau] || [], bg(state.idx).bang_chung, t);
}
function hienGoiYDoan(ds) {
  const o = $('goi-y-doan');
  o.textContent = '';
  o.hidden = !ds.length;
  for (const id of ds) {
    const d = el('div');
    const b = el('button', 'nho', 'Thêm làm bằng chứng');
    b.type = 'button'; b.dataset.them = id;
    d.append('Đoạn ', el('code', '', id), ' cũng có chữ này · ', b);
    o.append(d);
  }
}

/* ---------- Mở, lưu, chuyển tuyên bố ---------- */

function mo(i) {
  if (i < 0 || i >= TB.length) return;
  tick();
  state.idx = i; last = Date.now();
  bg(i);
  dungThe(); dungBai(); napForm(); dungMacDinh(); dungCumDieuKien(); dungCaDacBiet(); dungDoan(); hienGoiYDoan([]);
  hoatDongCuoi = Date.now();
  capNhatDanhSach(); capNhatDongHo(); luu();
}
function luuVaSang() {
  const i = state.idx, r = bg(i);
  const loi = kiem(i, state.nguoi_gan);
  if (loi.length) { hienLoi(loi); hienTin('tin', ''); return; }
  tick();
  r.trich = r.trich.trim(); r.ly_do = r.ly_do.trim(); r.ghi_chu = r.ghi_chu.trim();
  if (!coLoai(r.nhan)) r.loai = '';
  if (!(r.nguoi_gan && r.nd_goc && r.nd_goc === noiDungNhan(r))) r.nguoi_gan = state.nguoi_gan.trim(); // có sửa thì đổi người gán
  r.nd_goc = noiDungNhan(r);
  r.da_gan = true; r.dung = true;
  if (khongQua.delete(TB[i].id)) luuGiaoDien();
  hienLoi([]);
  if (i < TB.length - 1) { mo(i + 1); return; }
  napForm(); capNhatDanhSach(); capNhatDongHo(); luu();
  hienTin('tin', 'Đã lưu tuyên bố cuối cùng.');
}

/* ---------- Xuất và nhập ---------- */

function taiXuong(ten, noiDung, mime) {
  const blob = new Blob([noiDung], { type: mime + ';charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = ten;
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}
function banGhiXuat(i) {
  const tb = TB[i], r = bg(i);
  return {
    id: tb.id, nhan: r.nhan, dong_d: r.dong_d, loai: coLoai(r.nhan) ? r.loai : null, bang_chung: r.bang_chung.slice(),
    trich: r.trich.trim(), ly_do: r.ly_do.trim(), nguoi_gan: (r.nguoi_gan || state.nguoi_gan).trim(), luot: LUOT,
    giay: Math.max(1, Math.round(r.ms / 1000)), tai_lieu_mau_thuan: !!r.tai_lieu_mau_thuan, ghi_chu: r.ghi_chu.trim(),
    giay_nghi: Math.round(r.ms_nghi / 1000) // số giây đồng hồ đứng vì không thao tác quá NGHI_MS (không nằm trong giay)
  };
}
function taiNhan() {
  tick(); luu();
  const ds = TB.map((_, i) => i).filter((i) => bg(i).da_gan);
  if (!ds.length) { alert('Chưa có tuyên bố nào được gán (bấm "Lưu và sang tuyên bố sau" ở từng tuyên bố).'); return; }
  const con = TB.length - ds.length;
  if (con > 0 && !confirm('Còn ' + con + ' tuyên bố chưa gán, sẽ không có trong tệp. Vẫn tải ' + ds.length + ' nhãn đã gán?')) return;
  taiXuong(TRANG.tep_nhan, ds.map((i) => JSON.stringify(banGhiXuat(i))).join('\n') + '\n', 'application/x-ndjson');
}
function taiCauHoi() {
  const dong = [];
  TB.forEach((tb, i) => {
    const q = bg(i).cau_hoi.replace(KT, ' ').trim();
    if (q) dong.push('- ' + tb.id + ' (' + tb.ma_qc + '): ' + q);
  });
  if (!dong.length) { alert('Chưa có câu hỏi nhãn nào.'); return; }
  taiXuong(TRANG.tep_hoi, '# Câu hỏi nhãn (bộ thử, lượt ' + LUOT + ')\n\n' + dong.join('\n') + '\n', 'text/markdown');
}
async function nhapTep(files) {
  const moi = [], hoi = [], loi = [];
  for (const f of files) {
    const t = (await f.text()).replace(/^\ufeff/, '');
    t.split(/\r?\n/).forEach((dong, k) => {
      if (!dong.trim()) return;
      const m = dong.match(/^- (tb-\d+) \([^)]*\): (.*)$/);
      if (m) { hoi.push([m[1], m[2]]); return; }
      if (dong.trim()[0] !== '{') return; // dòng tiêu đề .md và các dòng khác
      try { moi.push(JSON.parse(dong)); } catch (e) { loi.push(f.name + ' dòng ' + (k + 1) + ': không phải JSON hợp lệ'); }
    });
  }
  // Trang này chỉ nhận bản ghi của lượt hiện tại: bản ghi lượt khác (luot: 1) bị từ chối, không ghi đè nhãn đang gán.
  const { dung: nhan, khac, luot_khac: luotKhac } = tachTheoLuot(moi, LUOT);
  if (khac) {
    loi.push('Từ chối ' + khac + ' bản ghi không phải lượt ' + LUOT + ' (luot: ' + luotKhac.join(', ') + '). Trang này chỉ nhận lượt '
      + LUOT + '; nhãn lượt khác để ở tệp riêng, không nhập vào đây.');
  }
  if (!nhan.length && !hoi.length) { alert('Không đọc được nhãn hay câu hỏi nào từ tệp đã chọn.' + (loi.length ? '\n' + loi.join('\n') : '')); return; }
  if (!confirm('Nhập ' + nhan.length + ' nhãn và ' + hoi.length + ' câu hỏi từ tệp? Nhãn hiện có của các tuyên bố trùng mã sẽ bị ghi đè (cả số giây).')) return;
  let dat = 0, khongDat = 0;
  const thieuDong = []; // nhãn của tệp cũ chưa có dong_d: không đoán dòng D, người gán chọn lại
  for (const o of nhan) {
    const i = TB.findIndex((t) => t.id === o.id);
    if (i < 0) { loi.push('id ' + o.id + ' không có trong danh sách tuyên bố'); continue; }
    const r = bg(i);
    r.nhan = MA_NHAN.includes(o.nhan) ? o.nhan : '';
    r.dong_d = MA_DONG.includes(o.dong_d) ? o.dong_d : '';
    r.loai = chuoi(o.loai);
    r.bang_chung = Array.isArray(o.bang_chung) ? o.bang_chung.filter((m) => typeof m === 'string') : [];
    r.trich = chuoi(o.trich); r.ly_do = chuoi(o.ly_do); r.ghi_chu = chuoi(o.ghi_chu);
    r.tai_lieu_mau_thuan = o.tai_lieu_mau_thuan === true;
    r.nguoi_gan = chuoi(o.nguoi_gan);
    r.ms = Number.isFinite(o.giay) && o.giay > 0 ? Math.round(o.giay) * 1000 : 0;
    r.ms_nghi = Number.isFinite(o.giay_nghi) && o.giay_nghi > 0 ? Math.round(o.giay_nghi) * 1000 : 0;
    r.nd_goc = noiDungNhan(r); // nội dung lúc nhập: "Lưu và sang" không sửa gì thì giữ người gán của tệp
    khongQua.delete(o.id);
    const e = kiem(i, r.nguoi_gan);
    r.da_gan = e.length === 0; r.dung = r.da_gan;
    if (r.da_gan) dat++;
    else if (!r.dong_d) { khongDat++; khongQua.add(o.id); thieuDong.push(o.id); } // dải vàng nhắc mở lại
    else { khongDat++; loi.push(o.id + ' không qua kiểm: ' + e.join(' ')); }
  }
  if (thieuDong.length) loi.push('Trang mới cần bạn chọn dòng D cho các tuyên bố đã gán trước đây (tệp chưa có dong_d): ' + thieuDong.join(', ') + '.');
  for (const [id, q] of hoi) {
    const i = TB.findIndex((t) => t.id === id);
    if (i >= 0) bg(i).cau_hoi = q; else loi.push('câu hỏi của ' + id + ': không có trong danh sách tuyên bố');
  }
  const ten = nhan.map((o) => chuoi(o.nguoi_gan).trim()).find((x) => x);
  if (ten) { state.nguoi_gan = ten; $('nguoi-gan').value = ten; }
  luuGiaoDien();
  mo(state.idx);
  alert('Đã nhập ' + dat + ' nhãn đạt kiểm' + (khongDat ? ', ' + khongDat + ' nhãn không đạt (nhập như bản nháp, cần Lưu lại)' : '') + ', ' + hoi.length + ' câu hỏi.' + (loi.length ? '\n\nChú ý:\n' + loi.join('\n') : ''));
}

/* ---------- Gắn sự kiện ---------- */

$('ds').addEventListener('click', (e) => {
  const b = e.target.closest('button.muc');
  if (b) mo(Number(b.dataset.i));
});
$('canh-bao-lai').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-mo]');
  if (!b) return;
  const i = TB.findIndex((t) => t.id === b.dataset.mo);
  if (i >= 0) mo(i);
});
$('nguoi-gan').addEventListener('input', (e) => { state.nguoi_gan = e.target.value; luu(); });
$('btn-tam-dung').addEventListener('click', () => { tick(); state.tamDung = !state.tamDung; last = Date.now(); capNhatDongHo(); });
$('loai').addEventListener('change', (e) => {
  bg(state.idx).loai = e.target.value;
  e.target.title = tieuDeLoai(e.target.value);
  suaDoi(false);
});
$('trich').addEventListener('input', (e) => { bg(state.idx).trich = e.target.value; suaDoi(false); });
$('ly-do').addEventListener('input', (e) => { bg(state.idx).ly_do = e.target.value; suaDoi(false); });
$('ghi-chu').addEventListener('input', (e) => { bg(state.idx).ghi_chu = e.target.value; capNhatNutMacDinh(); suaDoi(false); });
$('mau-thuan').addEventListener('change', (e) => { bg(state.idx).tai_lieu_mau_thuan = e.target.checked; suaDoi(false); });
$('cau-hoi').addEventListener('input', (e) => { bg(state.idx).cau_hoi = e.target.value; suaDoi(true); });
$('d-ds').addEventListener('click', (e) => {
  const chen = e.target.closest('button[data-chen]');
  if (chen) { chenMau(chen.dataset.chen); return; }
  const vd = e.target.closest('button[data-vd]');
  if (vd) { bamViDu(vd.dataset.vd); return; }
  const dung = e.target.closest('button[data-dung]');
  if (dung) chonDong(dung.dataset.dung);
});
$('md-nd').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-khoa]');
  if (b) themMacDinh(b.dataset.khoa);
});
$('bang-chung').addEventListener('click', (e) => {
  const x = e.target.closest('button[data-xoa]');
  if (x) {
    const r = bg(state.idx);
    r.bang_chung = r.bang_chung.filter((m) => m !== x.dataset.xoa);
    dungBangChung(); capNhatNutDoan(); suaDoi(false);
    return;
  }
  const a = e.target.closest('button[data-ma]');
  if (a) cuonToiDoan(a.dataset.ma);
});
$('doan').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-id]');
  if (!b || b.disabled) return;
  const r = bg(state.idx);
  if (!r.bang_chung.includes(b.dataset.id)) r.bang_chung.push(b.dataset.id);
  dungBangChung(); capNhatNutDoan(); suaDoi(false);
});
$('goi-y-doan').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-them]');
  if (!b) return;
  const r = bg(state.idx);
  if (!r.bang_chung.includes(b.dataset.them)) r.bang_chung.push(b.dataset.them);
  b.parentElement.remove();
  if (!$('goi-y-doan').children.length) $('goi-y-doan').hidden = true;
  dungBangChung(); capNhatNutDoan(); suaDoi(false);
});
$('kh-bai').addEventListener('toggle', cuonBai);
// Mọi thao tác (phím, chuột, cuộn, chạm) làm mới mốc "có thao tác" của đồng hồ; không đọc nội dung thao tác.
for (const ten of ['keydown', 'mousedown', 'mousemove', 'wheel', 'touchstart', 'scroll']) {
  document.addEventListener(ten, () => { hoatDongCuoi = Date.now(); }, { capture: true, passive: true });
}
$('tim').addEventListener('input', loc);
$('btn-lay').addEventListener('mousedown', (e) => e.preventDefault()); // giữ vùng đang bôi đen
$('btn-lay').addEventListener('click', layBoiDen);
$('form').addEventListener('submit', (e) => e.preventDefault());
$('btn-luu').addEventListener('click', luuVaSang);
$('btn-truoc').addEventListener('click', () => mo(state.idx - 1));
$('btn-sau').addEventListener('click', () => mo(state.idx + 1));
$('btn-tai-nhan').addEventListener('click', taiNhan);
$('btn-tai-hoi').addEventListener('click', taiCauHoi);
$('btn-nhap').addEventListener('click', () => $('tep-nhap').click());
$('tep-nhap').addEventListener('change', async (e) => {
  const fs = Array.from(e.target.files);
  e.target.value = '';
  if (fs.length) await nhapTep(fs);
});
$('btn-hd').addEventListener('click', () => { if ($('huong-dan').hidden) moHuongDan(); else dongHuongDan(); });
$('btn-dong-hd').addEventListener('click', dongHuongDan);
$('hdan-nd').addEventListener('click', (e) => {
  const a = e.target.closest('a[href^="#hd-"]');
  if (!a) return;
  e.preventDefault();
  const dich = document.getElementById(a.getAttribute('href').slice(1));
  if (dich) dich.scrollIntoView();
});
document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !$('huong-dan').hidden) dongHuongDan(); });
window.addEventListener('focus', () => { last = Date.now(); capNhatDongHo(); });
window.addEventListener('blur', () => { tick(); last = Date.now(); luu(); capNhatDongHo(); });
document.addEventListener('visibilitychange', () => { tick(); last = Date.now(); if (document.visibilityState !== 'visible') luu(); capNhatDongHo(); });
window.addEventListener('pagehide', () => { tick(); luu(); });
window.addEventListener('beforeunload', (e) => { if (!luuOk) { e.preventDefault(); e.returnValue = ''; } });

/* ---------- Khởi động ---------- */

nap();
kiemLaiKhiNap();
capNhatCanhBao();
$('nguoi-gan').value = state.nguoi_gan;
dungKhungD();
dungHuongDan();
napGiaoDien();
dungDanhSach();
mo(state.idx);
setInterval(tick, 250);
})();
</script>
</body>
</html>
"""


def duong_ra_mac_dinh(luot, co_chon):
    """Đường dẫn HTML khi không có --ra. Lượt 2 đầy đủ ghi TEP_RA như cũ; lượt khác ghi cong_cu_gan_nhan_luot<N>.html;
    lượt 2 mà chỉ một phần (--chon) thì phải nói rõ --ra, để không ghi đè trang lượt 2 đầy đủ bằng trang một phần."""
    if luot != LUOT:
        return TEP_RA.with_name(f"{TEP_RA.stem}_luot{luot}{TEP_RA.suffix}")
    if co_chon:
        sys.exit(f"--luot {LUOT} kèm --chon phải có --ra (mặc định {TEP_RA.name} là trang lượt {LUOT} đầy đủ, không ghi đè)")
    return TEP_RA


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Sinh công cụ gán nhãn chuẩn HTML của bộ thử (Bước 13, 16).")
    ap.add_argument("--luot", type=int, default=LUOT, help=f"lượt gán của trang, từ 2 (mặc định {LUOT})")
    ap.add_argument("--chon", type=Path, default=None,
                    help="tệp mã tuyên bố (mỗi dòng một mã, # là chú thích): chỉ đưa các tuyên bố này vào trang, xáo trộn thứ tự")
    ap.add_argument("--ra", type=Path, default=None, help=f"đường dẫn HTML sinh ra (mặc định {TEP_RA.name} cho lượt {LUOT})")
    args = ap.parse_args(argv)
    cau_hinh_luot(args.luot)
    tep_ra = args.ra or duong_ra_mac_dinh(args.luot, args.chon is not None)
    du_lieu = nap_du_lieu(args.luot, doc_tep_ma(args.chon) if args.chon else None)
    html_ra = dung_html(du_lieu)
    tep_ra.parent.mkdir(parents=True, exist_ok=True)
    tep_ra.write_text(html_ra, encoding="utf-8", newline="\n")
    so_doan = sum(len(d) for d in du_lieu["doan"].values())
    hd = du_lieu["huong_dan"]
    print(f"đã sinh {tep_ra}: lượt {args.luot}, {len(du_lieu['tuyen_bo'])} tuyên bố, {len(du_lieu['bai'])} bài, "
          f"{so_doan} đoạn của {len(du_lieu['doan'])} mẫu, {tep_ra.stat().st_size / 1024:.0f} KB")
    print(f"hướng dẫn: {len(hd['dong_d'])} dòng D, {len(hd['loai'])} loại, {len(hd['mac_dinh'])} hàng mặc định "
          f"({sum(1 for h in hd['mac_dinh'] if h['khao_sat'])} hàng ghép khảo sát), "
          f"{len(hd['huong_loi'])} hàng hướng thuận lợi")


if __name__ == "__main__":
    main()
