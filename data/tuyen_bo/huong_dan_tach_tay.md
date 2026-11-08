# Hướng dẫn tách tuyên bố bằng tay (Bước 12, 19, 23)

**Cập nhật 01/11/2026 (Bước 16):** thêm tiêu chí gắn điều kiện và bước rà tách trước khi gán nhãn; quy tắc 5 chỉ gộp khi cùng điều kiện; từ khẳng định chỉ giữ khi gắn với con số; bỏ cụm khen đứng cạnh con số.

**Cập nhật 08/11/2026 (Bước 19):** thêm cột đồng hồ vào bảng thuộc tính; thêm cặp tệp của tập phát triển (`doc_phat_trien.md`, `chinh_nhap.csv`). Năm quy tắc và bốn tiêu chí không đổi.

Tách **hoàn toàn bằng tay, không nhờ AI gợi ý**. Tuyên bố tách tay là đáp án chuẩn để chấm bước tách tự động ở Bước 29; nếu AI gợi ý thì đáp án chuẩn bị lẫn cách làm của AI.

## Tệp của từng bộ

| Bộ | Bài để đọc | Bảng điền | Script ghi ra |
|---|---|---|---|
| Bộ thử (Bước 12), 24 bài iPhone 17 và Galaxy Buds3 Pro | `data/tuyen_bo/doc_bo_thu.md` | `data/tuyen_bo/thu_nhap.csv` | `data/tuyen_bo/thu.jsonl` (`tb-00001` … `tb-00066`) |
| Tập phát triển (Bước 19), 16 bài Apple Watch SE 3 và Xiaomi 15T | `data/tuyen_bo/doc_phat_trien.md` | `data/tuyen_bo/chinh_nhap.csv` | `data/tuyen_bo/chinh.jsonl` (từ `tb-00067`) |
| Tập kiểm tra (Bước 23), 64 bài của 8 mẫu | tệp đọc riêng, in ở Bước 23 | nối tiếp vào cuối `data/tuyen_bo/chinh_nhap.csv` | `data/tuyen_bo/chinh.jsonl` |

## Làm gì

1. Mở tệp bài để đọc của bộ đang tách (bảng trên). Mỗi bài có mã bài (`ma_qc`) ở dòng tiêu đề.
2. Mở bảng điền bằng Excel hoặc Google Sheets. Mỗi tuyên bố là một dòng, điền 4 cột:

| Cột | Điền gì |
|---|---|
| `ma_qc` | Mã bài, chép từ đầu bài |
| `cau_goc` | Câu hoặc vế câu chứa con số, **chép nguyên văn** từ bài (copy, dán) |
| `tuyen_bo` | Viết lại thành một câu ngắn: tên sản phẩm + thuộc tính + con số + điều kiện, **đúng như bài nói** |
| `thuoc_tinh` | Một mã trong bảng dưới, đúng cột nhóm sản phẩm của bài |
| `ghi_chu` | Không bắt buộc. Ví dụ: bài nói về sản phẩm khác, câu khó hiểu |

Cột `can_xem` để trống.

3. Lưu lại dạng CSV (UTF-8), rồi báo mình chạy script để kiểm và ghi tệp JSONL:
   - Bộ thử: `scripts/chuyen_tuyen_bo.py data/tuyen_bo/thu_nhap.csv data/tuyen_bo/thu.jsonl`
   - Tập phát triển và tập kiểm tra: `scripts/chuyen_tuyen_bo.py data/tuyen_bo/chinh_nhap.csv data/tuyen_bo/chinh.jsonl --tiep-sau data/tuyen_bo/thu.jsonl`

Script đánh mã `tb-…` theo thứ tự dòng của CSV. Muốn thêm dòng sau khi đã chạy script thì **chỉ thêm ở cuối CSV**, không chèn giữa, để mã của các dòng sau không bị dịch.

## Thuộc tính được giữ

| Mã | Điện thoại (iPhone 17, Xiaomi 15T) | Tai nghe (Galaxy Buds3 Pro) | Đồng hồ (Apple Watch SE 3) |
|---|---|---|---|
| `thoi_luong_pin` | Pin dùng được bao nhiêu giờ | Nghe nhạc, đàm thoại bao nhiêu giờ (cả khi tính hộp sạc) | Pin dùng được bao nhiêu giờ |
| `sac_nhanh` | Sạc tới bao nhiêu % trong bao nhiêu phút | Sạc vài phút nghe được bao lâu | Sạc tới bao nhiêu % trong bao nhiêu phút, hoặc sạc vài phút dùng được bao lâu |
| `cong_suat_sac` | Công suất sạc (W) | Không có | Không có |
| `do_sang` | Độ sáng màn hình (nit) | Không có | Độ sáng màn hình (nit) |
| `tan_so_quet` | Tần số quét màn hình (Hz) | Không có | Không có |
| `zoom` | Thu phóng camera (2x, 10x...) | Không có | Không có |
| `khang_nuoc` | Chống nước, bụi (IP68, độ sâu, thời gian ngâm) | Chống nước (IP57...) | Chống nước, bụi (độ sâu tính bằng mét, chuẩn ISO, mã IP) |
| `dung_luong_pin` | Dung lượng pin (mAh) | Dung lượng pin tai nghe hoặc hộp sạc (mAh) | Không có |

Ô "Không có" nghĩa là nhóm đó không giữ thuộc tính này: câu nói về thuộc tính ấy thì bỏ qua, không ghi dòng. Script báo lỗi nếu `thuoc_tinh` không có trong cột của nhóm.

**Bỏ qua:** kích thước, trọng lượng, Bluetooth, chip, số chấm camera (48MP), giá, khuyến mãi, quà tặng, số đánh giá sao, số người dùng, so sánh với máy khác, câu khen không có con số ("pin trâu", "dùng cả ngày"). Cụm khen đứng cạnh một con số ("cả ngày", "suốt ngày dài", "không lo hết pin", "siêu bền", "bền bỉ", "vượt trội", "tuyệt đối", "trọn vẹn", "không giới hạn") cũng bỏ khỏi tuyên bố.

## 5 quy tắc

1. **Một dòng chỉ một thuộc tính và một con số.** Câu "pin 30 giờ, sạc 50% trong 20 phút" tách thành 2 dòng.
2. **Giữ ngữ cảnh.** Thêm tên sản phẩm. Điều kiện thuộc con số thì đưa vào tuyên bố, kể cả khi nằm ở câu trước hoặc câu sau. Điều kiện nào thuộc con số thì xem **tiêu chí gắn điều kiện** bên dưới. Ví dụ bài viết "Khi bật chống ồn, bạn vẫn có... lên đến 6 giờ" thì ghi "Galaxy Buds3 Pro nghe nhạc lên đến 6 giờ khi bật chống ồn".
3. **Không thêm điều kiện bài không nói, không sửa con số.** Bài ghi "pin 30 giờ" mà không nói xem video thì tuyên bố cũng không có "xem video". Giữ chữ "lên đến" nếu bài có. Từ khẳng định ("luôn", "đảm bảo", "ít nhất", "mọi lúc", "hơn", "trên", "không dưới", "trở lên") chỉ giữ khi nó gắn với con số (tiêu chí 3 bên dưới).
4. **Không phán đúng sai.** Câu sai thông số vẫn tách bình thường; gán nhãn là việc của bước gán nhãn (Bước 13, 20, 24).
5. **Gộp tuyên bố trùng trong cùng bài** chỉ khi hai lần nhắc cùng con số và cùng điều kiện; khi đó ghi một dòng. Bài nhắc một con số hai lần, một lần kèm điều kiện, một lần không (ví dụ ở tiêu đề và ở cuối câu), thì ghi hai dòng: người đọc lướt có thể chỉ thấy lần không kèm điều kiện.

## Tiêu chí gắn điều kiện

Dùng khi tách (quy tắc 2, 3, 5) và khi rà lại tuyên bố trước lúc gán nhãn. Nguồn: hướng dẫn gán nhãn bản 2, mục 2.

1. **Điều kiện bổ nghĩa trực tiếp cho con số thì thuộc con số:** cùng cụm, trong ngoặc ngay sau con số, hoặc "khi / ở / với / trong / dưới / cùng / kèm …" đi liền con số.
2. **Điều kiện cụ thể ở vế nói tác dụng của chính con số thì thuộc con số** ("… 2500 nit giúp nhìn rõ dưới nắng"). Nếu con số đã có điều kiện trực tiếp cùng loại thì điều kiện trực tiếp thắng.
3. **Điều kiện hay từ khẳng định ở vế nói về tính năng hay việc khác thì không thuộc con số.** Ví dụ "luôn giữ kết nối ổn định, pin 8 giờ": "luôn" thuộc vế kết nối, không đưa vào tuyên bố về pin.
4. **Một con số nhắc hai lần, một lần kèm điều kiện, một lần không, thì là hai tuyên bố** (quy tắc 5).

## Rà tách trước khi gán nhãn

Trước khi gán một bộ tuyên bố, người thực hiện rà từng tuyên bố với `cau_goc` theo bốn tiêu chí trên. Rà bằng tay, không nhờ AI gợi ý chỗ sửa.

- Có thể dùng danh sách của `scripts/ra_tach.py` làm chỗ để xem: script chỉ so chuỗi, liệt kê cụm điều kiện, từ khẳng định có trong câu gốc mà không có trong tuyên bố; không gọi AI, không đề xuất cách sửa. Bộ thử: `data/tuyen_bo/ra_tach_thu.md`. Tập phát triển: chạy `scripts/ra_tach.py data/tuyen_bo/chinh.jsonl --ma-mau dh-apple-watchse3 dt-xiaomi-15t`, ra `data/tuyen_bo/ra_tach_chinh.md`.
- Tuyên bố trái tiêu chí thì sửa trong bảng điền của bộ đó (`thu_nhap.csv` hoặc `chinh_nhap.csv`), ghi `tach_sua=<sửa gì>` vào cột `ghi_chu` (ví dụ `tach_sua=thêm chế độ nguồn`). Tách thêm tuyên bố theo tiêu chí 4 cũng ghi `tach_sua=`, và thêm dòng ở cuối CSV.
- Chạy lại `scripts/chuyen_tuyen_bo.py` (lệnh ở mục "Làm gì") để kiểm và ghi lại tệp JSONL.
- Khi gán nhãn chỉ đọc tuyên bố, không đọc câu gốc để thêm điều kiện.

## Ví dụ (không lấy từ bài nào của bộ thử hay tập phát triển)

| `cau_goc` | `tuyen_bo` | `thuoc_tinh` |
|---|---|---|
| "nghe nhạc liền 7 tiếng ngay cả khi bật chống ồn" | Galaxy Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn | `thoi_luong_pin` |
| "sạc nhanh 60% chỉ trong 25 phút" | Điện thoại A sạc 60% trong 25 phút | `sac_nhanh` |
| "Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin" | Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin | `thoi_luong_pin` |
| "Màn hình Điện thoại A sáng 2500 nit, giúp bạn nhìn rõ dưới nắng" | Điện thoại A sáng 2500 nit dưới nắng | `do_sang` |

Bộ thử có khoảng 60 tuyên bố cho 24 bài. Tập phát triển và tập kiểm tra không đặt chỉ tiêu: tách đủ những gì bài nói, không cố thêm hay bớt. Bài nào không có tuyên bố nào thì bỏ qua, không cần ghi dòng.
