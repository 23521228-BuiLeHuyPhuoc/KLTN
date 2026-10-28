# Hướng dẫn tách tuyên bố bằng tay (Bước 12)

Tách **hoàn toàn bằng tay, không nhờ AI gợi ý**. Tuyên bố tách tay là đáp án chuẩn để chấm bước tách tự động ở Bước 29; nếu AI gợi ý thì đáp án chuẩn bị lẫn cách làm của AI.

## Làm gì

1. Mở `data/tuyen_bo/doc_bo_thu.md`: 24 bài quảng cáo, mỗi bài có mã bài (`ma_qc`) ở đầu.
2. Mở `data/tuyen_bo/thu_nhap.csv` bằng Excel hoặc Google Sheets. Mỗi tuyên bố là một dòng, điền 4 cột:

| Cột | Điền gì |
|---|---|
| `ma_qc` | Mã bài, chép từ đầu bài |
| `cau_goc` | Câu hoặc vế câu chứa con số, **chép nguyên văn** từ bài (copy, dán) |
| `tuyen_bo` | Viết lại thành một câu ngắn: tên sản phẩm + thuộc tính + con số + điều kiện, **đúng như bài nói** |
| `thuoc_tinh` | Một mã trong bảng dưới |
| `ghi_chu` | Không bắt buộc. Ví dụ: bài nói về sản phẩm khác, câu khó hiểu |

3. Lưu lại dạng CSV (UTF-8), rồi báo mình chạy `scripts/chuyen_tuyen_bo.py` để kiểm và ghi `data/tuyen_bo/thu.jsonl`.

## Thuộc tính được giữ

| Mã | Điện thoại (iPhone 17) | Tai nghe (Galaxy Buds3 Pro) |
|---|---|---|
| `thoi_luong_pin` | Pin dùng được bao nhiêu giờ | Nghe nhạc, đàm thoại bao nhiêu giờ (cả khi tính hộp sạc) |
| `sac_nhanh` | Sạc tới bao nhiêu % trong bao nhiêu phút | Sạc vài phút nghe được bao lâu |
| `cong_suat_sac` | Công suất sạc (W) | Không có |
| `do_sang` | Độ sáng màn hình (nit) | Không có |
| `tan_so_quet` | Tần số quét màn hình (Hz) | Không có |
| `zoom` | Thu phóng camera (2x, 10x...) | Không có |
| `khang_nuoc` | Chống nước, bụi (IP68, độ sâu, thời gian ngâm) | Chống nước (IP57...) |
| `dung_luong_pin` | Dung lượng pin (mAh) | Dung lượng pin tai nghe hoặc hộp sạc (mAh) |

**Bỏ qua:** kích thước, trọng lượng, Bluetooth, chip, số chấm camera (48MP), giá, khuyến mãi, quà tặng, số đánh giá sao, số người dùng, so sánh với máy khác, câu khen không có con số ("pin trâu", "dùng cả ngày").

## 5 quy tắc

1. **Một dòng chỉ một thuộc tính và một con số.** Câu "pin 30 giờ, sạc 50% trong 20 phút" tách thành 2 dòng.
2. **Giữ ngữ cảnh.** Thêm tên sản phẩm. Điều kiện nằm ở câu trước hoặc câu sau thì đưa vào tuyên bố. Ví dụ bài viết "Khi bật chống ồn, bạn vẫn có... lên đến 6 giờ" thì ghi "Galaxy Buds3 Pro nghe nhạc lên đến 6 giờ khi bật chống ồn".
3. **Không thêm điều kiện bài không nói, không sửa con số.** Bài ghi "pin 30 giờ" mà không nói xem video thì tuyên bố cũng không có "xem video". Giữ cả chữ "lên đến", "luôn", "ít nhất" nếu bài có.
4. **Không phán đúng sai.** Câu sai thông số vẫn tách bình thường; gán nhãn là việc của Bước 13.
5. **Gộp tuyên bố trùng trong cùng bài.** Bài nhắc hai lần cùng một ý thì chỉ ghi một dòng.

## Ví dụ (không lấy từ 24 bài)

| `cau_goc` | `tuyen_bo` | `thuoc_tinh` |
|---|---|---|
| "nghe nhạc liền 7 tiếng ngay cả khi bật chống ồn" | Galaxy Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn | `thoi_luong_pin` |
| "sạc nhanh 50% chỉ trong 20 phút" | iPhone 17 sạc 50% trong 20 phút | `sac_nhanh` |

Mục tiêu khoảng 60 tuyên bố cho 24 bài. Bài nào không có tuyên bố nào thì bỏ qua, không cần ghi dòng.
