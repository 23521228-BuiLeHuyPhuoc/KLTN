# Bước 16 · Đề xuất giải quyết câu hỏi nhãn, chuẩn bị hướng dẫn bản 2

**Ngày:** 01/11/2026 · **Trạng thái:** đã duyệt ngày 01/11/2026: người thực hiện chọn phương án khuyên (A) cho cả 8 quyết định QĐ1–QĐ8. Lúc viết đề xuất chưa sửa hướng dẫn, nhãn, script, cấu hình hay kế hoạch.

**Đã đọc:** `data/huong_dan_gan_nhan.md` (bản 1, toàn bộ); `data/nhan/cau_hoi_nhan.md` (phần A, B, C); `scripts/tao_cong_cu_gan_nhan.py` (`DONG_D_HIEN_THI`, `THONG_BAO`, `NHAC`, `CA_DAC_BIET`, khung HTML, hàm `kiem`); `luan_van/nhat_ky.md` (Bước 8–15); `ket_qua/khao_sat_cach_hieu.md`; T4, T5.1–T5.7, T6.2–T6.6, T9.1, T10 và Bước 9–16 của kế hoạch; `data/tuyen_bo/thu.jsonl` (tuyên bố và câu gốc); `data/tuyen_bo/huong_dan_tach_tay.md`; các đoạn liên quan của iPhone 17, Galaxy Buds3 Pro, Xiaomi 15T; `dien_thoai.yaml`, `tai_nghe.yaml`, `chung.yaml`.

**Ranh giới:**

- Tệp không nêu nhãn hay dòng D của tuyên bố nào trong bộ thử. Mã `tb-…` chỉ dùng để trỏ về câu hỏi trong `cau_hoi_nhan.md`.
- Ví dụ trong tệp là câu tự đặt về sản phẩm giả định (Điện thoại A, Tai nghe B, Đồng hồ C), hoặc về mẫu phát triển không có trong bộ thử (Xiaomi 15T, Apple Watch SE 3).
- Khi gán lại lượt 2, người gán chỉ đọc hướng dẫn bản 2. Không mở tệp này, `cau_hoi_nhan.md` hay nhãn lượt 1.

## 1. Quyết định cần duyệt

| # | Quyết định | Phương án khuyên | Phương án khác | Hệ quả một dòng |
|---|---|---|---|---|
| QĐ1 | Tuyên bố thiếu điều kiện có trong câu gốc thì gán theo câu nào | **A.** Gán theo chữ của tuyên bố. Trước khi gán lại, rà tách theo tiêu chí gắn điều kiện, sửa tuyên bố và ghi lý do | B. Giữ tuyên bố, người gán đọc thêm câu gốc. C. Gán theo câu gốc | A giữ nhãn khớp đúng đầu vào mà P và B0–B3 nhận; tốn 30–60 phút rà, phải chạy lại B0 và Recall@k |
| QĐ2 | Cụm điều kiện hướng dẫn chưa có ("dưới nắng", "liên tục", "tổng", "qua cổng 45W") | **A.** Đọc theo nghĩa với người mua, đối chiếu điều kiện tài liệu mô tả; cụm chung chung coi như chưa nêu | B. Chỉ nhận chữ của hãng và cụm có trong cấu hình. C. Cụm lạ là D1a | B, C gán Chưa đủ cho tuyên bố đúng nghĩa, làm FAR của đối chứng cao giả tạo; A cần phán đoán, phải có phụ lục cụm |
| QĐ3 | Cụm phủ nhiều giá trị ("mọi điều kiện ánh sáng", "dù nghe nhạc hay gọi điện") | **A.** Tuyên bố phải đúng ở mọi giá trị được phủ: so với giá trị kém thuận lợi nhất, loại `doi_dieu_kien` | B. Coi là từ khẳng định (D2). C. Bỏ qua cụm. D. Tách thành nhiều tuyên bố | A cùng logic với "kém thuận lợi nhất"; C có thể biến tuyên bố gây hiểu nhầm thành Đúng |
| QĐ4 | "hơn 18 giờ", "trên 18 giờ" | **A.** Thêm nhóm từ mức sàn vào từ khẳng định, chỉ khi đứng liền con số (D2) | B. Coi là giá trị 18 giờ, so ở D3 | A nhất quán với "ít nhất"; B cho Đúng; chưa có số liệu khảo sát về cách hiểu |
| QĐ5 | Ghi `mac_dinh` khi nào | **A.** Ghi mọi khóa ở mục 5 mà tuyên bố không nêu (trừ "như hãng công bố" và khóa không áp dụng), ở mọi dòng từ D1a | B. Chỉ ghi khóa mà đổi cách hiểu thì nhãn đổi | A nhanh, nhất quán, không sót; phân tích độ nhạy Bước 37 thành cận trên |
| QĐ6 | Giá trị suy ra bằng phép tính (tổng trừ tai nghe) | **A.** Không tính, chỉ so với số hãng công bố | B. Cho phép cộng, trừ đơn giản | A tất định, P không cần số học; tuyên bố về phần riêng của hộp sạc thường ra Chưa đủ |
| QĐ7 | Cùng con số nằm ở nhiều đoạn | **A.** Ghi mọi đoạn có cùng con số ở cùng điều kiện | B. Ghi một đoạn | A cho Recall@k đúng thực tế; thêm 10–30 giây mỗi tuyên bố |
| QĐ8 | Con số trùng giá trị của một hoạt động khác ở D4 (mục 11.2) | **A.** Giữ D4 tính mọi điều kiện; đặt trước ngưỡng xét lại: quá 1/4 số Lệch D4 | B. Giới hạn ngay D4 trong cùng hoạt động. C. Giữ, không đặt ngưỡng | FAR như nhau ở cả ba; B làm V42 đổi nhãn và lệch định nghĩa của đề cương |

**Ví dụ một dòng cho từng quyết định** (chi tiết ở mục 4):

- QĐ1: câu gốc "Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin", tuyên bố tách sót thành "dùng tới 40 giờ". A sửa tuyên bố rồi mới gán.
- QĐ2: tài liệu ghi "2500 nit (ngoài trời)", tuyên bố "sáng 2500 nit khi đi dưới trời nắng". A: cùng chế độ. B, C: không nêu chế độ.
- QĐ3: tài liệu ghi nghe nhạc 9 giờ, đàm thoại 6 giờ; tuyên bố "9 giờ dù nghe nhạc hay gọi điện". A: Lệch. C: Đúng.
- QĐ4: tài liệu "lên đến 20 giờ", tuyên bố "dùng hơn 18 giờ". A: Lệch ở D2. B: Đúng.
- QĐ5: tuyên bố "Tai nghe B nghe nhạc 12 giờ" ra Sai. A ghi `che_do_chong_on,bo_phan`; B chỉ ghi `bo_phan`.
- QĐ6: tài liệu "7 / 28 giờ", tuyên bố "hộp sạc nạp thêm 21 giờ". A: Chưa đủ. B: 28 − 7 = 21, Đúng.
- QĐ7: cùng dòng "7 giờ (bật ANC)" ở `#010` và `#030`. A ghi cả hai.
- QĐ8: "nghe nhạc 6 giờ ở chế độ xuyên âm", 6 giờ là số đàm thoại. A: Lệch. B: Chưa đủ.

**Cách duyệt:** ghi chọn của từng QĐ (A, B...) vào nhật ký. Sau khi duyệt mới viết hướng dẫn bản 2 (mục 10).

## 2. Tổng quan

19 quy tắc cho hướng dẫn bản 2:

- **11 quy tắc loại (a)**: chỉ nói rõ điều hướng dẫn, đề cương hoặc kế hoạch đã ngụ ý. Sửa chữ, không cần chọn (QT1–QT11, mục 3).
- **8 quy tắc loại (b)**: phải chọn giữa các cách hợp lý. Mỗi quy tắc là một quyết định ở bảng trên (QT12–QT19 ứng với QĐ1–QĐ8, mục 4).

Một nguyên tắc dùng xuyên suốt khi chọn: **nhãn chuẩn theo tài liệu và cách người mua hiểu, không theo khả năng cài đặt của P.** Mục 6.7 của hướng dẫn đã nói "nhãn chuẩn không theo giới hạn của cấu hình". Lý do: P cài đúng hướng dẫn. Nếu hướng dẫn chọn cách dễ cho P (ví dụ cụm lạ thì Chưa đủ), P sẽ "đúng" theo nhãn, còn đối chứng đọc theo nghĩa sẽ bị tính chấp nhận nhầm. FAR của đối chứng cao giả tạo, khoảng cách giữa P và đối chứng bị thổi phồng.

**Câu hỏi nào được quy tắc nào trả lời**

Đánh số câu hỏi theo thứ tự xuất hiện trong `cau_hoi_nhan.md`.

| Câu hỏi | Trỏ tới | Quy tắc |
|---|---|---|
| A1 | tb-00001, cụm "với mọi điều kiện ánh sáng" | QT14 (QĐ3), mục 5 |
| A2 | tb-00006, tb-00025, "liên tục" | QT13 (QĐ2) ý 3 |
| A3 | tb-00006, "hơn 24 giờ" | QT15 (QĐ4) |
| A4 | tb-00006 và 5 tuyên bố khác, từ khẳng định ở vế khác | QT4 |
| A5 | tb-00009, "tối đa" cùng "ngoài trời" | QT13 (QĐ2) ý 4 |
| A6 | tb-00015 và 10 tuyên bố khác, tuyên bố so với câu gốc | QT12 (QĐ1) |
| A7 | tb-00015, tb-00021, tb-00030, "ánh nắng", "ánh sáng mạnh" | QT13 (QĐ2) ý 2 |
| A8 | tb-00017, `mac_dinh` ở D1a | QT16 (QĐ5) |
| A9 | tb-00019, con số điều kiện dùng làm giá trị | QT6 |
| A10 | tb-00024, tb-00033, `mac_dinh` khi nhãn không đổi theo cách hiểu | QT16 (QĐ5) |
| A11 | tb-00026, như A9 | QT6 |
| A12 | tb-00033, "telephoto" | QT13 (QĐ2) ý 1, 2 |
| A13 | tb-00035, "qua USB-C 40W" | QT13 (QĐ2) ý 5, QT5 |
| A14 | tb-00036 và 6 tuyên bố khác, `mac_dinh=bo_phan` ở kháng nước | QT16 (QĐ5) |
| A15 | tb-00037, tb-00048, "tổng", "khi kết hợp hộp sạc" | QT13 (QĐ2) ý 6 |
| A16 | tb-00037, tb-00039, `mac_dinh` ở D1b | QT16 (QĐ5) |
| A17 | tb-00040, "suốt cả ngày" | QT7 |
| A18 | tb-00050, tb-00055, tb-00062, `mac_dinh` ở D5 | QT16 (QĐ5) |
| A19 | tb-00051, "hộp sạc cung cấp thêm" | QT17 (QĐ6), QT13 ý 6 |
| A20 | tb-00052, mã IP khác nhánh | QT9 |
| A21 | tb-00056, D1b khi con số kém hơn cả hai số | QT8 |
| A22 | tb-00058, tb-00059, "cho cả nhạc và cuộc gọi" | QT14 (QĐ3) |
| B1 | "xem video" so với nhãn "Thời gian xem video" | QT1 ý 3 |
| B2 | sạc nhanh không nêu bộ sạc mà dừng D1a | QT2 |
| B3 | 120Hz ở D2 khi không có từ khẳng định | QT4 |
| B4 | tb-00009, tb-00010 lưu lệch | Mục 6, S15 |
| B5 | "tối đa" của độ sâu, thời gian ngâm xét ở D2 | QT4 ý 3 |
| B6 | độ sáng không nêu chế độ trong tuyên bố | QT1, QT12 (QĐ1), QT13 (QĐ2) |
| B7 | loại `doi_dieu_kien` cùng `mac_dinh` một khóa; lý do "bán riêng" | QT5 |
| B8 | D1 dùng khi tài liệu có thuộc tính | QT3 |
| B9 | không nêu bộ phận mà so với số "Tổng" | QT1, QT12 (QĐ1) |
| B10 | D1b ở điều kiện không có mâu thuẫn | QT8 |
| B11 | mẫu câu `{trích}` ghi mã đoạn | QT10 |
| C1 | mặc định chưa được nói là dùng ở mọi dòng; quy tắc `mac_dinh` | QT1, QT2, QT16 (QĐ5) |
| C2 | ranh giới các dòng D | QT3, QT4, QT8, QT9, QT15 (QĐ4) |
| C3 | tuyên bố so với câu gốc; cụm chưa có cách đọc | QT6, QT12–QT14, QT17 (QĐ1–QĐ3, QĐ6) |
| C, nhóm phụ | lưu lệch; `{trích}` | QT10; mục 6, S14, S15 |

## 3. Quy tắc loại (a): nói rõ điều đã ngụ ý

### QT1 · Xác định điều kiện trước, không dựa vào con số

**Luật.**

1. Điều kiện của tuyên bố gồm điều kiện tuyên bố nêu rõ, cộng cách hiểu mặc định (mục 5) cho điều kiện bắt buộc không nêu. Xác định xong điều kiện mới so con số.
2. Không chọn điều kiện (chế độ, bộ phận, hoạt động, phụ kiện) vì con số chỉ khớp ở điều kiện đó. Con số trùng giá trị ở điều kiện khác là việc của D4, không phải căn cứ để đổi điều kiện của tuyên bố.
3. Cụm đã có quy tắc ở mục 5 thì theo mục 5, kể cả khi chữ của tuyên bố trùng chữ trên nhãn của tài liệu. Ví dụ: "xem video" trong tuyên bố là chưa rõ loại video, dù Apple ghi "Thời gian xem video" cho số xem video tải sẵn (V03).

**Lý do.**

- Mục 1 đặt bước 3 (xác định điều kiện) trước bước 4 (dò D1–D6).
- V25, V47: "Không chọn chế độ theo con số của tuyên bố."
- Khảo sát Bước 10, mục 6, dòng Q11: "cách hiểu mặc định không được phụ thuộc vào độ lớn con số".
- Đề cương định nghĩa Lệch là con số "trùng giá trị được công bố ở một điều kiện khác với điều kiện mà tuyên bố nêu hoặc được hiểu thông thường". Nếu chọn điều kiện theo con số thì không bao giờ có Lệch loại `bo_dieu_kien`.
- Hệ quả cho FAR: chọn điều kiện theo con số biến Lệch thành Đúng, làm FAR thấp giả tạo cho mọi hệ thống.
- Hệ quả cho P: T5.5 đã đúng thứ tự (bước B trước bước C). Bước 27 nên thêm kiểm thử "điều kiện không đổi khi đổi con số của tuyên bố".

**Sửa ở.** Mục 1, bước 3: thêm ý 2. Đoạn mới ngay trên bảng mục 7. Mục 5, phần "Ba ý hay bị hiểu nhầm": thêm ý 1 và ý 3.

**Ví dụ V.** Không đổi nhãn.

### QT2 · Mặc định dùng ở mọi dòng D; D1a chỉ có ba lối vào

**Luật.** Điều kiện có cách hiểu mặc định thì coi như tuyên bố đã nêu điều kiện đó, rồi dò tiếp D1b → D6. D1a chỉ khi:

1. tuyên bố không nêu một điều kiện mà mục 5 ghi "Không có mặc định";
2. chữ của tuyên bố trỏ tới nhiều chế độ (mục 6.5);
3. cụm điều kiện không giải được theo mục 6.7 (sau QĐ2).

Điều kiện có mặc định không bao giờ là lý do dừng ở D1a. Con số không khớp ở điều kiện mặc định cũng không phải lý do D1a.

**Lý do.** Mục 5 và lưu ý D1a ở mục 7 đã nói vậy. V21, V23, V32, V33, V34 dùng mặc định rồi đi tới D4. Nhật ký 01/11 ghi tiêu đề khung trên trang "dùng ở D1a" làm người gán hiểu mặc định chỉ dùng ở D1a; đây là nhóm lệch lớn nhất (B2).

**Sửa ở.** Mục 5, câu đầu: thêm "dùng ở mọi dòng D". Mục 7, lưu ý D1a: viết thành ba lối vào đánh số. Mục 8: D1a phải ghi nguyên nhân (mục 6, S18).

**Ví dụ V.** Không đổi.

### QT3 · D1 chỉ khi tài liệu không có con số nào cho thuộc tính

**Luật.** D1 khi tài liệu của đúng sản phẩm không có con số nào cho thuộc tính của tuyên bố, ở bất kỳ điều kiện, bộ phận hay phiên bản nào. Có con số nhưng ở điều kiện hay bộ phận khác thì không dừng ở D1: dò tiếp, thường tới D4, D5 hoặc D6. "Tài liệu không có số ở điều kiện tuyên bố nêu" là D6, không phải D1.

**Lý do.** Định nghĩa Chưa đủ thông tin của đề cương tách hai vế: "không có thông số cùng sản phẩm và thuộc tính" (D1) và "không công bố giá trị ở điều kiện mà tuyên bố nêu" (D6). V45 là D1, V44 là D6. D1 dừng trước D4, nên dùng D1 sai chỗ làm mất các ca Lệch thật. FAR không đổi (D1, D6 cùng là Chưa đủ). F1 Lệch đổi. Recall@k cũng đổi: nhãn D1 không có bằng chứng nên rơi khỏi mẫu số (Bước 14: mẫu số 56 vì 8 nhãn D1).

**Sửa ở.** Mục 7, lưu ý D1. Câu hỏi D1 trên trang (S4).

**Ví dụ V.** Không đổi.

### QT4 · D2 cần từ khẳng định gắn với con số

**Luật.**

1. Bỏ "lên đến" vẫn khớp (mục 6.2). Tuyên bố không có từ khẳng định thì không bao giờ dừng ở D2.
2. Từ khẳng định chỉ tính khi gắn với con số của tuyên bố: bổ nghĩa cho con số, hoặc cho động từ có con số ("luôn đạt 120Hz", "đảm bảo 6 giờ", "ít nhất 18 giờ"). Từ ở vế khác của câu, nói về việc khác (kết nối, thông tin, sự đồng hành), không tính. Tên tính năng không tính.
3. "Tối đa" của điều kiện đo ("độ sâu tối đa 6 mét", "tối đa 30 phút") là giới hạn của bài thử. So theo mục 6.3. Đây không phải mức "lên đến" của giá trị. Tuyên bố nêu đúng giới hạn đó không phải D2.
4. Khi tách: giữ từ khẳng định trong tuyên bố chỉ khi nó gắn với con số theo ý 2.

**Lý do.**

- Mục 6.2 dòng 171–172: "chỉ xét từ nằm trong câu chứa giá trị". T10 điểm 4: "chỉ xét từ nằm trong câu trích của giá trị". Khung "Quy tắc hay dùng" trên trang: từ phải "gắn với một mức". V40 tách "Luôn Bật" khỏi giá trị. Ba chỗ cùng một ý; bản 2 chỉ viết rõ "câu" là vế chứa con số.
- Khảo sát Q07/Q15: chỉ 1/10 người hiểu con số trần chắc chắn hơn con số có "lên đến".
- Đề cương: Lệch khi tuyên bố "biến mức tối đa 'lên đến' thành mức chắc chắn đạt". Biến thành chắc chắn là thêm lời hứa, không phải bỏ chữ.
- Hệ quả: D2 dùng cho tuyên bố chỉ thiếu "lên đến" làm tuyên bố chính xác thành Lệch. Mọi hệ thống nói Đúng bị tính chấp nhận nhầm, kể cả P (P cài D2 theo từ khẳng định). Điểm dừng 1 cũng không tính ca D2, nên D2 sai chỗ còn làm sai số đếm.

**Sửa ở.** Mục 6.2: ý 2, 3 thành gạch đầu dòng riêng, mỗi ý một ví dụ tự đặt. Mục 2 dòng 25: thêm ý 4. Mục 3: thêm một câu chú thích dưới định nghĩa Lệch, không sửa nguyên văn đề cương. Mục 7, lưu ý D2. Trang: câu hỏi D2, chữ nút Lệch, bắt buộc ghi `khang_dinh=<từ>` (S3, S7, S17).

**Ví dụ V.** Không đổi.

### QT5 · Nêu rõ phụ kiện là đủ; một điều kiện không vừa nêu rõ vừa mặc định

**Luật.**

1. "Không mua thêm" chỉ dùng khi tuyên bố không nêu phụ kiện. Tuyên bố nêu bộ sạc hay công suất bộ sạc thì so theo mục 6.3. Tuyên bố không cần nói phụ kiện "được bán riêng".
2. Với mỗi điều kiện khác tài liệu: tuyên bố nêu rõ thì loại `doi_…`, không ghi khóa đó vào `mac_dinh`; tuyên bố không nêu thì loại `bo_dieu_kien`, ghi khóa đó vào `mac_dinh`.

**Lý do.** V01 nêu "bộ sạc 40W trở lên", không nói bán riêng, và là Đúng. V22 nêu củ 20W, là `doi_dieu_kien`. Mục 5 "Không mua thêm" và bảng loại ở mục 8 đã phân biệt "không nêu" với "nêu rõ" (B7).

**Sửa ở.** Mục 5, ý "Không mua thêm". Mục 8, câu dưới bảng loại.

**Ví dụ V.** Không đổi.

### QT6 · Con số của điều kiện không phải giá trị của thuộc tính

**Luật.** Con số tài liệu dùng làm điều kiện (công suất bộ tiếp hợp tối thiểu, mốc phần trăm, số phút sạc, độ sâu, thời gian ngâm, phần diện tích đo) không phải giá trị công bố của thuộc tính. Không dùng nó để khớp ở D3 hay D4. Tuyên bố lấy con số đó làm giá trị thì dò D1–D6 với các giá trị thật của thuộc tính. Ghi `nham_vai=<cụm>` vào ghi chú (mã mới), để thống kê kiểu lỗi này ở Bước 38.

**Lý do.** Định nghĩa bốn nhãn so với "giá trị được công bố" của thuộc tính. Bộ thông số bảy trường (T5.1) tách trường giá trị với trường điều kiện. Nếu khớp con số điều kiện ở D4, lý do sẽ nói "con số có thật ở điều kiện khác", điều này sai: không điều kiện nào cho ra giá trị đó. FAR không đổi (D4, D5, D6 đều khác Đúng); chỉ đổi phân bố Lệch, Sai, Chưa đủ.

**Ví dụ tự đặt.** Tài liệu Điện thoại A: "sạc 50% trong 25 phút với bộ sạc 45W trở lên", không công bố công suất sạc có dây. Tuyên bố "Điện thoại A sạc nhanh 45W" (thuộc tính công suất sạc). 45W là điều kiện, không khớp ở D3 hay D4; dò tiếp với các giá trị công suất thật của tài liệu.

**Sửa ở.** Mục con mới 6.9 "Giá trị và điều kiện" (cùng QT17). Mục 8, bảng ghi chú: thêm `nham_vai`.

**Ví dụ V.** Không đổi.

### QT7 · Cụm khen không có con số thì bỏ qua

**Luật.** Cụm khen không có con số ("cả ngày", "suốt ngày dài", "không lo hết pin", "siêu bền", "bền bỉ", "vượt trội", "tuyệt đối", "trọn vẹn", "không giới hạn") không phải điều kiện, cũng không phải từ khẳng định. Bỏ qua khi gán. Khi tách thì bỏ khỏi tuyên bố. Ngoại lệ: cụm phủ nhiều giá trị gắn với con số theo QT14, và từ khẳng định gắn với con số theo QT4.

**Lý do.** Mục 2 dòng 30 bỏ tuyên bố cảm tính. `huong_dan_tach_tay.md` bỏ "câu khen không có con số ('pin trâu', 'dùng cả ngày')". Chữ "Pin dùng cả ngày" của Apple (V14) cũng không phải giá trị.

**Sửa ở.** Mục 2, gạch "Bỏ". Mục 6.2: thêm một câu.

**Ví dụ V.** Không đổi.

### QT8 · D1b chỉ xét điều kiện của tuyên bố, áp cho mọi con số

**Luật.** D1b khi, ở đúng điều kiện của tuyên bố (nêu rõ cộng mặc định), tài liệu ghi từ hai giá trị khác nhau. Áp dụng dù con số của tuyên bố trùng một giá trị, kém thuận lợi hơn cả hai, hay khác cả hai. Mâu thuẫn ở điều kiện khác không tính.

**Lý do.**

- Lưu ý D1b ở mục 7 và V48: "cả khi con số của tuyên bố trùng một trong hai giá trị".
- T4.3 đặt D1a, D1b trước D2 "để không bao giờ dẫn tới nhãn Đúng".
- T4.4: tuyên bố có `tai_lieu_mau_thuan` được thống kê riêng, nên FAR báo được cả khi bỏ các ca này.
- Phương án khác: con số kém hơn cả hai thì dò tiếp tới D3. Cách này gần nghĩa hơn nhưng trái lý do của T4.3, và P phải cài thêm phép "khớp mọi giá trị". Muốn đổi thì là quyết định riêng ở Bước 27 (điểm 6 ở T10). Tôi không khuyên đổi.

**Sửa ở.** Mục 7, lưu ý D1b. Câu hỏi D1b trên trang (S6). Mục "Hai số cho tổng thời gian phát nhạc" trong `CA_DAC_BIET` (S12).

**Ví dụ V.** Không đổi.

### QT9 · Mã IP khác nhánh là D5

**Luật.** Kháng nước so mã IP theo mục 6.6. Điều kiện thử không nêu thì hiểu như hãng công bố, nên tuyên bố và tài liệu cùng điều kiện. Mã khác nhánh không khớp ở D3. Nếu mã đó trùng mã của bộ phận hay điều kiện khác thì D4. Không trùng thì D5 Sai, loại `doi_gia_tri`.

**Lý do.** Định nghĩa Sai: giá trị "mâu thuẫn với giá trị công bố ở điều kiện của tuyên bố ... đồng thời không trùng giá trị nào ở điều kiện khác". Trong cấu hình, mã IP là giá trị (`don_vi: ma_ip`); điều kiện là độ sâu, thời gian ngâm, loại nước, hoạt động bị cấm. Cách đọc D6 phải coi mã IP là điều kiện, trái với cấu hình. FAR không đổi (D5, D6 đều khác Đúng).

**Sửa ở.** Mục 6.6: thêm ví dụ tự đặt "máy công bố IP68, tuyên bố IPX5: khác nhánh, không trùng mã nào, D5". Mục 7, lưu ý D5.

**Ví dụ V.** Không đổi.

### QT10 · Mẫu câu lý do: chỗ trống là câu trích nguyên văn

**Luật.** Trong mẫu câu lý do, chỗ `{trích}` là câu trích nguyên văn, không phải mã đoạn. Đổi tên thành `{câu trích}`.

**Lý do.** Mục 8: "chép nguyên văn từ `noi_dung` hoặc `chu_thich`". T4.4: ghi câu trích nguyên văn. 31 lý do của lượt 1 ghi mã đoạn ở chỗ này (B11).

**Sửa ở.** Mục 8, bảng mẫu câu (trang đọc bảng này nên tự cập nhật). T5.6 của kế hoạch. Kiểm mới trên trang (S14).

**Ví dụ V.** Không đổi.

### QT11 · Gán lại lượt 2: toàn bộ, mù với lượt 1

**Luật.** Gán lại cả 66 tuyên bố theo bản 2, trên trang dùng khóa lưu mới, `luot: 2`. Khi gán, người gán không mở nhãn lượt 1, `cau_hoi_nhan.md` và tệp này. Lượt 1 giữ nguyên ở tệp riêng.

**Lý do.** Nhật ký 01/11 đã chốt: "Bước 16 gán lại cả bộ thử theo bản 2, người gán chỉ đọc hướng dẫn bản 2, không đọc phần B theo từng tuyên bố". T3.5 điểm 5: không dùng AI để gán nhãn chuẩn; nhận xét theo từng tuyên bố của Claude không được đi vào nhãn. Thời gian của lượt 2 dùng cho việc chốt quy mô.

**Sửa ở.** Trang (S20). T3.4: thêm `luot: 2` vào mẫu.

## 4. Quyết định loại (b)

### QĐ1 · QT12 · Gán theo chữ của tuyên bố; rà tách trước khi gán lại

**Trả lời:** A6; B6, B9; C3.

**Vấn đề.** Một số tuyên bố thiếu điều kiện có trong câu gốc (ánh nắng, hộp sạc, mọi hoạt động thể thao), hoặc mang theo từ ở vế khác. Hướng dẫn không nói người gán xét theo câu nào.

**Phương án.**

- **A.** Nhãn là hàm của (tuyên bố, tài liệu, hướng dẫn). Trước khi gán lại, người thực hiện rà 66 tuyên bố với câu gốc theo tiêu chí gắn điều kiện bên dưới. Tuyên bố nào trái T4.1 thì sửa, ghi `tach_sua=<sửa gì>` vào `ghi_chu` của tuyên bố. Khi gán chỉ đọc tuyên bố.
- **B.** Giữ tuyên bố; người gán được đọc câu gốc để thêm điều kiện bị bỏ sót.
- **C.** Gán theo câu gốc (vế chứa con số).

**Tiêu chí gắn điều kiện** (dùng cho A; đưa vào mục 2 của hướng dẫn và `data/tuyen_bo/huong_dan_tach_tay.md`):

1. Điều kiện bổ nghĩa trực tiếp cho con số thì thuộc con số: cùng cụm, trong ngoặc ngay sau con số, hoặc "khi / ở / với / trong / dưới / cùng / kèm …" đi liền con số.
2. Điều kiện cụ thể ở vế nói tác dụng của chính con số thì thuộc con số ("… 2500 nit giúp nhìn rõ dưới nắng"). Nếu con số đã có điều kiện trực tiếp cùng loại thì điều kiện trực tiếp thắng.
3. Điều kiện hay từ khẳng định ở vế nói về tính năng hay việc khác thì không thuộc con số.
4. Câu gốc nhắc một con số hai lần, một lần kèm điều kiện, một lần không, thì là hai tuyên bố. Người tách đã chốt cách này ngày 30/10/2026 (nhật ký Bước 12: "Người đọc lướt chỉ thấy tiêu đề"). Quy tắc 5 "gộp tuyên bố trùng" của `huong_dan_tach_tay.md` chỉ áp khi hai lần nhắc cùng điều kiện.

**Hệ quả.**

- **A.** Nhãn khớp đúng đầu vào mà P và B0–B3 nhận (T6.2: "cùng tuyên bố"; T5.8: thực nghiệm chính dùng tuyên bố tách tay). Tuyên bố tách tay thành chuẩn tốt hơn cho Bước 29. Tốn khoảng 30–60 phút. Tuyên bố đổi chữ phải chạy lại B0 (bộ nhớ đệm giữ phần không đổi) và tính lại Recall@k. Rủi ro: người rà đã biết nhãn lượt 1 và kết quả B0. Giảm bằng tiêu chí viết trước, ghi mọi chỗ sửa, Claude không gợi ý chỗ sửa (bài học ngày 30/10). Có thể dùng một script tất định liệt kê "cụm điều kiện của cấu hình có trong câu gốc mà không có trong tuyên bố" làm danh sách để xem; người thực hiện tự quyết từng chỗ.
- **B.** Nhãn dựa vào thông tin hệ thống không thấy. FAR và F1 của mọi hệ thống bị chấm theo câu khác câu chúng nhận, lệch theo hướng không kiểm soát. Muốn công bằng phải đưa câu gốc vào đầu vào của mọi hệ thống, tức đổi thiết kế ở T5 và T6.2.
- **C.** Phá quy tắc một thuộc tính một giá trị (câu gốc thường có 2–3 con số). Bước 29 mất chuẩn để chấm tách tự động.
- **Số Lệch, FAR:** không đoán được hướng; tùy chỗ nào phải sửa.
- **Độ khó cho người gán:** A dễ nhất khi gán (chỉ một câu), nhưng ý 2 của tiêu chí cần phán đoán khi rà tách.

**Khuyên: A.**

**Ví dụ trực quan.** Câu quảng cáo: "Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin." Tuyên bố tách sót: "Đồng hồ C dùng tới 40 giờ."

- A: rà tách, sửa thành "Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin", ghi `tach_sua=thêm chế độ nguồn`, rồi gán theo câu đã sửa.
- B: tuyên bố vẫn là "40 giờ". Người gán đọc câu gốc nên gán theo chế độ tiết kiệm; hệ thống chỉ thấy "40 giờ" nên bị chấm theo câu nó không nhận.

**Sửa ở.** Mục 1: thêm bước 0 "tuyên bố là đơn vị gán". Mục 2: thêm tiêu chí gắn điều kiện. `huong_dan_tach_tay.md` quy tắc 2 và 5. Trang: khung bài quảng cáo (S22).

**Ví dụ V.** Không đổi.

### QĐ2 · QT13 · Đọc cụm điều kiện chưa có trong hướng dẫn

**Trả lời:** A2, A5, A7, A12, A13, A15; một phần B6; C3.

**Vấn đề.** Mục 6.5 chỉ đọc chữ của hãng. Cấu hình đã có cụm thông dụng (`ngoai_troi.hieu_biet_chung: "dưới nắng", "ngoài nắng"`; `kem_hop_sac.tu_tai_lieu: "Tổng thời gian"`), nhưng hướng dẫn không nhắc tới. Nhiều cụm của bộ thử chưa có cách đọc.

**Phương án.**

- **A. Đọc theo nghĩa với người mua.**
  1. Cụm có trong cấu hình (in thành phụ lục của hướng dẫn) thì là điều kiện đó.
  2. Cụm chưa có: nếu cụm tả đúng một điều kiện tài liệu công bố, bằng tên hãng dùng hoặc bằng hoàn cảnh của điều kiện ấy (ánh nắng, ánh sáng mạnh cho chế độ sáng cao ngoài trời), thì là nêu điều kiện đó. Ghi `ngoai_cau_hinh=<cụm>`.
  3. Cụm chỉ sự liên tục hay mức dùng chung ("liên tục", "sử dụng liên tục", "dùng liên tục") không nêu hoạt động cụ thể. Coi như chưa nêu hoạt động, dùng mặc định.
  4. Tuyên bố có cả chữ chỉ chế độ rõ ("ngoài trời", "HDR", "dưới nắng") và chữ mức cao ("tối đa", "đỉnh", "cực đại"): chữ chỉ chế độ quyết định; chữ mức cao là kiểu giá trị tối đa.
  5. Trong tuyên bố về thời gian sạc, con số W đi cùng cách sạc hay cổng sạc ("sạc qua cổng X 45W", "với 45W") là công suất nguồn sạc, tức điều kiện bộ tiếp hợp. Trong tuyên bố về công suất sạc thì con số W là giá trị.
  6. Bộ phận của thời lượng pin tai nghe: "tổng", "tổng cộng", "kèm / cùng / kết hợp hộp sạc" là kèm hộp sạc. "Hộp sạc" đứng riêng làm chủ ngữ ("hộp sạc cho thêm …") là bộ phận hộp sạc.
  7. Vẫn không xếp được thì D1a (mục 6.7).
- **B.** Chỉ nhận chữ của hãng và cụm có trong cấu hình. Cụm khác coi như không nêu: dùng mặc định, hoặc D1a nếu không có mặc định.
- **C.** Mọi cụm không có trong hướng dẫn và cấu hình là D1a.

**Hệ quả.**

- **FAR.** B và C gán Chưa đủ cho tuyên bố đúng nghĩa (ví dụ dưới). Đối chứng LLM đọc theo nghĩa sẽ nói Đúng và bị tính chấp nhận nhầm. P cài luật B hay C thì "đúng" theo nhãn. FAR của đối chứng cao giả tạo (mục 2). A tránh được điều này.
- **Số Lệch.** A cho nhiều ca so được ở D3–D5 hơn; không đoán được hướng.
- **Người gán.** A cần phán đoán "cùng nghĩa", nên rủi ro kappa thấp. Giảm bằng phụ lục cụm và mỗi ý một ví dụ tự đặt. B, C dễ hơn.
- **P.** A cần thêm cụm vào cấu hình từ tập phát triển ở Bước 22, 27 (được phép, T3.5 điểm 4). Cụm chưa có thì P ra D1a, ghi là giới hạn bao phủ; cơ chế này đã có ở T5.3 và mục 6.7. Ý 3 cần tách cách đọc phía tuyên bố với phía tài liệu: Xiaomi 15T dùng "Sử dụng liên tục" làm tên bài đo, và cấu hình đang khai báo `su_dung_lien_tuc` là một hoạt động.
- **Phương án riêng cho ý 3** (nếu không chọn A ý 3): coi "sử dụng liên tục" là tên một hoạt động; tài liệu nào không công bố hoạt động đó thì dò D4–D6.

**Khuyên: A** (cả 7 ý).

**Ví dụ trực quan.**

- Tài liệu Điện thoại A: "độ sáng tối đa 900 nit (tiêu chuẩn); độ sáng đỉnh 2500 nit (ngoài trời)". Tuyên bố "Điện thoại A sáng 2500 nit khi đi dưới trời nắng". A: "dưới trời nắng" tả hoàn cảnh của chế độ ngoài trời, cùng điều kiện, D3 Đúng. B, C: chữ không trùng "ngoài trời", độ sáng điện thoại không có mặc định, D1a Chưa đủ.
- Tài liệu Điện thoại A: "xem video lên đến 22 giờ; xem video trực tuyến lên đến 19 giờ". Tuyên bố "pin dùng liên tục 18 giờ". A ý 3: chưa nêu hoạt động, so với 19 giờ, D3 Đúng. Phương án riêng: "sử dụng liên tục" là hoạt động tài liệu không công bố, 18 không trùng số nào, D6 Chưa đủ.

**Sửa ở.** Mục 6.5: thêm ý 4. Mục 6.7: thêm ý 2, 3, 7. Mục con mới 6.8 "Đọc cụm điều kiện trong tuyên bố". Phụ lục mới "Cụm diễn đạt trong cấu hình", sinh từ `data/cau_hinh/*.yaml` và kiểm khớp như bảng mục 5.

**Ví dụ V.** V07 giữ nhãn Đúng. Lý do đổi từ "cùng hoạt động sử dụng liên tục" thành "không nêu hoạt động cụ thể; Xiaomi 15T chỉ công bố một hoạt động (sử dụng liên tục, 13,19 giờ), nên đó cũng là hoạt động kém thuận lợi nhất". Thêm `mac_dinh=hoat_dong`. V27 đã đọc "dưới ánh sáng mạnh" theo cách A, không đổi. Các V khác không đổi.

### QĐ3 · QT14 · Cụm phủ nhiều giá trị của một điều kiện

**Trả lời:** A1, A22; phần "mọi hoạt động thể thao" của A6, nếu cụm còn trong tuyên bố sau QĐ1.

**Phương án.**

- **A.** Cụm phủ ("mọi điều kiện X", "bất kể X", "dù A hay B", "cho cả A và B", "mọi hoạt động") gắn với con số nghĩa là tuyên bố phải đúng ở từng giá trị được phủ. Điều kiện của tuyên bố là giá trị kém thuận lợi nhất trong các giá trị được phủ mà tài liệu công bố. Đây là điều kiện nêu rõ, nên Lệch thì loại `doi_dieu_kien`. Cụm phủ không phải từ khẳng định, trừ khi có từ khẳng định gắn con số. Với kháng nước, "mọi hoạt động" phủ cả hoạt động hãng khuyến cáo không dùng (mục 6.6).
- **B.** Coi như từ khẳng định, xét ở D2.
- **C.** Bỏ qua như câu khen.
- **D.** Tách "cho cả A và B" thành hai tuyên bố.

**Hệ quả.**

- **A** cùng logic với T4.5 ("tuyên bố không nêu chế độ phải đúng ở mọi chế độ") và mục 6.7 ý 3. Khảo sát Bước 10 cũng đã xóa "bất kể điều kiện ánh sáng" khỏi Q10 vì vế này "gợi ý sẵn là mọi lúc" (`khao_sat_cach_hieu.md` mục 5).
- **B** không xác định được "mức lên đến ở cùng điều kiện" khi điều kiện là "mọi chế độ". Ca vào D2 không tính cho điểm dừng 1.
- **C** có thể biến tuyên bố gây hiểu nhầm thành Đúng (ví dụ dưới). FAR thấp giả tạo cho mọi hệ thống.
- **D** đổi số tuyên bố; không dùng được cho "mọi điều kiện".
- **Số Lệch.** A đưa các ca này vào D4, có tính cho điểm dừng 1. Không được chọn A vì lý do này; lý do chọn là cách người mua hiểu.
- **P.** Cần danh sách cụm phủ trong `chung.yaml`, và điều kiện phải nhận được một tập giá trị. Phép chọn "kém thuận lợi nhất" đã có.
- **Người gán.** Dễ, vì cụm phủ dễ nhận ra.

**Khuyên: A.**

**Ví dụ trực quan.** Tài liệu Tai nghe B: "nghe nhạc lên đến 9 giờ; đàm thoại lên đến 6 giờ". Tuyên bố "Tai nghe B dùng 9 giờ dù nghe nhạc hay gọi điện".

- A: phải đúng cả khi gọi (6 giờ). 9 giờ là số của nghe nhạc, nên D4 Lệch (`doi_dieu_kien`).
- C: bỏ cụm, mặc định nghe nhạc, D3 Đúng.

**Sửa ở.** Mục 6.8 mới. Mục 6.6 (hoạt động). Mục 8, bảng loại: ghi chú cho `doi_dieu_kien`.

**Ví dụ V.** Không đổi. Có thể thêm một ví dụ thật từ Apple Watch SE 3 (không thuộc bộ thử), ví dụ "dùng 32 giờ ở mọi chế độ" so với 18 giờ ở chế độ thường; câu trích cần kiểm trên `doan.jsonl`.

### QĐ4 · QT15 · "hơn X", "trên X" gắn với con số

**Trả lời:** A3.

**Phương án.**

- **A.** Thêm nhóm "mức sàn" vào từ khẳng định: "hơn <số>", "trên <số>", "không dưới <số>", "<số> trở lên". Chỉ tính khi đứng liền con số của giá trị tuyên bố. Xét ở D2 như "ít nhất".
- **B.** Coi "hơn 18 giờ" là giá trị 18 giờ. Kém hơn số của hãng thì khớp ở D3.
- **C.** Giá trị không xác định, D1a.

**Hệ quả.**

- **A** nhất quán với "ít nhất" (đã có) và T10 điểm 5 (khẳng định một mức thấp hơn mức "lên đến" vẫn là Lệch). Các tuyên bố này thành Lệch D2, không tính cho điểm dừng 1.
- **B** cho Đúng, nên FAR thấp hơn A trên các ca này. Hai cách nói cùng nghĩa ("hơn 18", "ít nhất 18") ra hai nhãn khác nhau.
- **C** không có lý do: con số rõ ràng.
- **Căn cứ người đọc:** chưa có. Q07 chỉ cho biết 1/10 người hiểu con số trần là "ít nhất". Ghi là chỗ chưa chắc.
- **P.** Thêm `tu_muc_san` vào `chung.yaml`. Luật "liền con số" để không bắt nhầm "trên tai nghe", "trên 25% diện tích". "Tối thiểu" vẫn chưa thêm (T10 điểm 4).
- **Người gán.** Dễ.

**Khuyên: A.**

**Ví dụ trực quan.** Tài liệu Đồng hồ C: "lên đến 20 giờ khi sử dụng bình thường". Tuyên bố "Đồng hồ C dùng hơn 18 giờ".

- A: hứa mức sàn mà tài liệu không hứa, D2 Lệch.
- B: 18 < 20, D3 Đúng.

**Sửa ở.** Mục 6.2. T5.4 (chuẩn hóa kiểu giá trị) và T10 điểm 4 của kế hoạch.

**Ví dụ V.** Không đổi. Có thể thêm ví dụ thật: "Apple Watch SE 3 dùng được hơn 16 giờ khi sử dụng bình thường" so với "lên đến 18 giờ".

### QĐ5 · QT16 · Ghi `mac_dinh` khi nào

**Trả lời:** A8, A10, A14, A16, A18; C1.

**Phương án.**

- **A.** Ghi mọi khóa của mục 5 mà tuyên bố không nêu và có giá trị khác `nhu_hang_cong_bo`, ở mọi dòng từ D1a tới D6. Gồm cả khóa "không có mặc định" khi dừng ở D1a vì khóa đó. Không ghi ở D1, vì D1 dừng trước khi xét điều kiện. Không ghi khóa không áp dụng (mục 4). Không cần xét nhãn có đổi hay không.
- **B.** Chỉ ghi khóa mà đổi cách hiểu thì nhãn đổi.

**Hệ quả.**

- **A** cơ học, nhanh, hai người gán dễ giống nhau. Danh sách cho Bước 37 đầy đủ, không sót. Phép "đổi mọi nhãn phụ thuộc mặc định thành Chưa đủ" thành cận trên, vì đếm cả nhãn không thật sự phụ thuộc. Phép tính lại với hai mặc định thay thế (chế độ nguồn đồng hồ, zoom; khảo sát mục 8) chỉ cần xem lại tay các nhãn có khóa đó.
- **B** chính xác hơn cho Bước 37, nhưng người gán phải thử ngược từng cách hiểu: chậm, dễ sót, khó đồng thuận.
- **FAR, số Lệch:** không đổi, vì chỉ là ghi chú.
- **Trang:** nút `mac_dinh=` đã chỉ hiện khóa khác `nhu_hang_cong_bo`, khớp A.

**Khuyên: A.**

**Ví dụ trực quan.** Tài liệu Tai nghe B: tai nghe 9 giờ (tắt chống ồn), 7 giờ (bật); tổng kèm hộp sạc 30 giờ. Tuyên bố "Tai nghe B nghe nhạc 12 giờ", ra D5.

- A: `mac_dinh=che_do_chong_on,bo_phan`.
- B: chỉ `mac_dinh=bo_phan`. Tính cả hộp sạc thì 12 < 30 nên nhãn đổi; đổi chế độ chống ồn thì nhãn không đổi.

**Sửa ở.** Mục 8, bảng ghi chú, dòng `mac_dinh`.

**Ví dụ V.** Nhãn không đổi. Ghi chú đổi ít nhất ở: V16 (thêm `che_do_chong_on,bo_phan`), V17 (`bo_phan`), V22 (`cach_sac`), V46 (`moc_phan_tram,cach_sac`), V48 (`hoat_dong`). Có thể đổi ở V07 (nếu QĐ2 chọn A), V11 (`hoat_dong`), V12 (`che_do_hien_thi`), V40 (`kieu_tan_so`). Rà lại cả 48 ví dụ bằng script sau khi chốt.

### QĐ6 · QT17 · Giá trị suy ra bằng phép tính

**Trả lời:** A19.

**Phương án.**

- **A.** Chỉ so với con số hãng công bố. Không cộng, trừ, nhân để tạo giá trị mới (ví dụ lấy tổng trừ tai nghe ra phần của hộp sạc). Tuyên bố về một bộ phận mà tài liệu không có số riêng thì dò D4–D6 như thường. Cấu hình chưa biết bộ phận đó thì ghi `ngoai_cau_hinh=`.
- **B.** Cho phép phép tính đơn giản trên các số cùng bảng.

**Hệ quả.**

- **A** tất định, khớp định nghĩa nhãn ("giá trị được công bố"). P không cần số học. Tuyên bố về phần riêng của hộp sạc thường ra Chưa đủ (D6) nếu không trùng số nào.
- **B** có nhiều cách tính (theo chống ồn bật hay tắt; theo số nào khi tài liệu mâu thuẫn). Người gán dễ khác nhau. P phải cài thêm luật.
- **FAR.** B có thể cho Đúng ở những ca A cho Chưa đủ.

**Khuyên: A.**

**Ví dụ trực quan.** Tài liệu Tai nghe B: "7 / 28 giờ" (tai nghe / tổng kèm hộp sạc). Tuyên bố "Hộp sạc của Tai nghe B nạp thêm 21 giờ".

- A: hãng không công bố số riêng của hộp sạc; 21 không trùng số nào; D6 Chưa đủ.
- B: 28 − 7 = 21, D3 Đúng.

**Sửa ở.** Mục con mới 6.9 (cùng QT6).

**Ví dụ V.** Không đổi.

### QĐ7 · QT18 · Bằng chứng khi cùng con số nằm ở nhiều đoạn

**Trả lời:** ghi nhận cho Bước 16 trong nhật ký Bước 14 (01/11).

**Phương án.**

- **A.** Ghi mọi đoạn chứa cùng giá trị ở cùng điều kiện mà nhãn dựa vào. Lệch: mọi đoạn chứa giá trị trùng. Sai: mọi đoạn chứa giá trị ở cùng điều kiện. Câu trích lấy từ ít nhất một đoạn; nhiều phần thì nối bằng " | ".
- **B.** Ghi một đoạn.

**Hệ quả.**

- **A** làm Recall@k phản ánh đúng việc truy hồi có lấy được bằng chứng hay không. Nhật ký Bước 14: số thời lượng pin của Buds3 Pro lặp ở `#038`, `#042`, `#044`; các ca trượt ở k = 1 đều do một đoạn khác cùng số vượt lên. Tốn thêm 10–30 giây mỗi tuyên bố. Trang có thể gợi ý các đoạn có cùng chữ trích (S16).
- **B** nhanh, nhưng Recall@k bị tính thấp hơn thực tế.
- **FAR, số Lệch:** không đổi.

**Khuyên: A.**

**Ví dụ trực quan.** Tài liệu Tai nghe B ghi "Nghe nhạc (bật ANC) lên đến 7 giờ" ở đoạn giới thiệu `#010` và ở bảng thông số `#030`. A: `bang_chung = [#010, #030]`. B: chỉ `#030`; nếu BM25 xếp `#010` đầu thì Recall@1 tính là trượt.

**Sửa ở.** Mục 8, đoạn "Bằng chứng và câu trích".

**Ví dụ V.** Nhãn không đổi. Danh sách bằng chứng có thể dài thêm ở các ví dụ Buds3 Pro (V09, V16, V31, V32...).

### QĐ8 · QT19 · Con số trùng giá trị của một hoạt động khác ở D4

**Trả lời:** mục 11.2 của hướng dẫn ("Ở Bước 16, đếm số ca Lệch chỉ do trùng số giữa hai hoạt động").

**Phương án.**

- **A.** Giữ D4 tính mọi điều kiện khác của cùng thuộc tính (như V42). Sau lượt 2, đếm ca Lệch D4 mà giá trị trùng thuộc một hoạt động khác hoạt động của tuyên bố (nêu rõ hoặc mặc định). Đặt trước ngưỡng: nếu số ca này quá 1/4 số Lệch D4 thì xét lại ở Bước 27 trên toàn tập phát triển.
- **B.** Giới hạn ngay D4 trong các giá trị cùng hoạt động với tuyên bố. Trùng số khác hoạt động thì dò tiếp D5, D6.
- **C.** Giữ D4, không đặt ngưỡng.

**Hệ quả.**

- **FAR** như nhau ở cả ba, vì Lệch, Sai, Chưa đủ đều khác Đúng.
- **B** giảm số Lệch, đổi V42, và lệch định nghĩa của đề cương ("trùng giá trị được công bố ở một điều kiện khác").
- **A** giữ định nghĩa. Ngưỡng đặt trước nên không chỉnh luật theo kết quả.
- Trùng số khác hoạt động có thể do LLM lấy nhầm ô bên cạnh trong bảng thông số, tức đúng kiểu lỗi đề tài nhắm tới. Chưa có số liệu.
- **P:** A đơn giản nhất.

**Khuyên: A.** Ngưỡng 1/4 là đề xuất; người thực hiện có thể đổi, nhưng phải chốt trước khi đếm.

**Ví dụ trực quan.** Tài liệu Tai nghe B: "nghe nhạc 9 giờ; đàm thoại 6 giờ", không có số cho chế độ xuyên âm. Tuyên bố "Tai nghe B nghe nhạc 6 giờ ở chế độ xuyên âm".

- A, C: 6 trùng số đàm thoại, D4 Lệch.
- B: không tính trùng khác hoạt động; 6 không cao hơn mọi số; D6 Chưa đủ.

**Sửa ở.** Mục 11.2: ghi ngưỡng và cách đếm.

**Ví dụ V.** A, C: không đổi. B: V42 đổi thành Chưa đủ (D6).

## 5. Danh sách từ khẳng định (điểm 4 ở T10)

Hiện có (mục 6.2, `chung.yaml`): "luôn", "đảm bảo", "bảo đảm", "ít nhất", "mọi lúc"; chỉ tính khi gắn với con số (QT4).

Dò câu gốc của 66 tuyên bố. Bảng dưới chỉ dẫn câu gốc, không nêu nhãn.

| Từ, cụm | Câu gốc chứa từ (trích) | Đề xuất | Lý do |
|---|---|---|---|
| "hơn <số>" | tb-00006: "thời lượng pin kéo dài hơn 24 giờ liên tục" | **Thêm** nếu QĐ4 chọn A, cùng "trên <số>", "không dưới <số>", "<số> trở lên" (thêm theo nghĩa, chưa gặp trong bộ thử) | Hứa mức sàn như "ít nhất"; chỉ tính khi đứng liền con số |
| "đảm bảo" | tb-00006: "đảm bảo kết nối thông suốt"; tb-00016, tb-00017: "đảm bảo kết nối liền mạch suốt ngày dài" | Đã có. Không đổi danh sách | Phạm vi theo QT4: ở các câu này từ đứng ở vế khác |
| "luôn", "Luôn Bật" | tb-00020: "mọi thông tin quan trọng luôn trong tầm tay"; tb-00032: "màn hình Luôn Bật siêu mượt với ProMotion 120Hz"; tb-00005: "tính năng Luôn Bật" | Đã có. Không đổi | Phạm vi theo QT4; tên tính năng không tính (V40) |
| "mọi lúc" | tb-00027, tb-00028: "đồng hành cùng bạn mọi lúc, mọi nơi" | Đã có. Không đổi | Phạm vi theo QT4 |
| "mọi điều kiện ánh sáng" | tb-00001: "dưới mọi điều kiện ánh sáng với màn hình siêu sáng 3000 nit"; tb-00009, tb-00010: "giúp hiển thị rõ ràng dưới mọi điều kiện ánh sáng" | **Không thêm** vào từ khẳng định | Là cụm phủ nhiều giá trị, xử lý ở QĐ3 |
| "cho cả … và …" | tb-00058, tb-00059: "26 giờ (bật ANC) cho cả nhạc và cuộc gọi" | **Không thêm** | Cụm phủ, QĐ3 |
| "mọi hoạt động" | tb-00052: "phù hợp cho mọi hoạt động thể thao"; tb-00061: "phù hợp với mọi hoạt động từ công việc đến thể thao" | **Không thêm** | Cụm phủ về hoạt động, QĐ3 và mục 6.6 |
| "liên tục" | tb-00002: "xem video liên tục lên đến 30 giờ"; tb-00025: "24 giờ sử dụng liên tục"; tb-00050: "lên tới 8 giờ liên tục"; tb-00055, tb-00062: "8 giờ nghe liên tục" | **Không thêm** | Tả cách đo (dùng không ngắt), không hứa mức sàn; xử lý ở QĐ2 ý 3 |
| "cả ngày", "suốt (cả) ngày (dài)", "không lo" | tb-00002: "Giải trí trọn vẹn cả ngày dài không lo ngắt quãng"; tb-00019: "sử dụng cả ngày mà không lo hết pin"; tb-00036, tb-00040: "suốt cả ngày dài"; tb-00053: "sử dụng liên tục suốt ngày dài mà không lo hết pin" | **Không thêm** | Câu khen không có con số, QT7 |
| "chỉ", "chỉ cần", "chỉ trong" | tb-00004: "sạc nhanh 50% chỉ trong 20 phút"; tb-00057: "chỉ cần 5 phút sạc để có thêm 2 giờ sử dụng" | **Không thêm** | Nhấn độ nhanh, không hứa mức sàn; V21 có "chỉ" và lý do không dựa vào chữ này |
| "ngay cả" | tb-00014, tb-00015: "ngay cả dưới ánh nắng gay gắt"; tb-00021: "ngay cả trong ánh sáng mạnh"; tb-00029, tb-00030: "ngay cả dưới ánh nắng mạnh" | **Không thêm** | Mở đầu một điều kiện (QĐ1, QĐ2), không phải lời hứa về mức |
| "tuyệt đối", "trọn vẹn", "không giới hạn" | tb-00001: "mượt mà tuyệt đối"; tb-00031: "trải nghiệm mượt mà không giới hạn" | **Không thêm** | Câu khen, không gắn con số (QT7) |
| "tối đa" | tb-00009: "độ sáng tối đa ngoài trời lên tới 3000 nit"; tb-00040: "thời gian phát tối đa 7 giờ trên tai nghe" | **Không thêm** | Kiểu giá trị tối đa (mục 6.2), hoặc chữ chỉ chế độ với độ sáng Apple (mục 6.5, QĐ2 ý 4) |

Phía P (Bước 22, 27): `chung.yaml` tách `tu_khang_dinh.tu` và `tu_khang_dinh.tu_muc_san`. Bước trích xuất phải ghi từ khẳng định kèm câu trích của giá trị, để Python kiểm luật "gắn với con số" và luật "liền con số". T5.4 sửa theo.

## 6. Sửa trang gán nhãn

Chỉ liệt kê, không sửa code ở lượt này. Tệp: `scripts/tao_cong_cu_gan_nhan.py` (số dòng theo bản hiện tại); `scripts/kiem_nhan.py` phải sửa theo, vì hai bên dùng chung quy tắc. Mọi kiểm mới chỉ dùng các ô người gán điền, `thuoc_tinh` và `ma_mau` ghi sẵn, và nội dung hướng dẫn. Không đọc câu tuyên bố để gợi ý nhãn (ranh giới ở docstring đầu tệp).

**Chữ dễ hiểu nhầm**

- **S1.** Khung mặc định: tiêu đề "Khi tuyên bố không nói điều kiện (dùng ở D1a)" (dòng 1072) đổi thành "Bước 3 · Điều kiện của tuyên bố: nêu rõ, hoặc cách hiểu mặc định (dùng ở mọi dòng D)". Chuyển khung lên trên bảng D1–D6 (hiện khung D ở dòng 1063–1069, khung mặc định ở 1071–1077). Câu mở đầu (dòng 1074): thêm "Không chọn điều kiện theo con số của tuyên bố".
- **S2.** "Cách làm một tuyên bố" (dòng 1052–1059): chèn bước "Xác định điều kiện" trước bước dò D. Bước 1 thêm "Gán theo chữ của tuyên bố" (nếu QĐ1 chọn A).
- **S3.** Nút nhãn LECH (dòng 1106): đổi thành "Số có thật nhưng ở điều kiện khác, hoặc có từ khẳng định ('luôn', 'ít nhất'...) gắn với mức 'lên đến'. Chỉ thiếu chữ 'lên đến' thì không phải Lệch." Nút CHUA_DU (dòng 1107): ghi đủ bốn lối: không có số cho thuộc tính (D1), không xác định được điều kiện (D1a), tài liệu mâu thuẫn (D1b), không có số ở điều kiện này (D6).
- **S4.** Câu hỏi D1 (dòng 67): "Tài liệu của đúng sản phẩm có con số nào cho thuộc tính {tên thuộc tính} không, ở bất kỳ điều kiện hay bộ phận nào? Không có số nào thì dừng. Có số nhưng ở điều kiện khác thì dò tiếp." Tên thuộc tính lấy từ `thuoc_tinh` ghi sẵn.
- **S5.** Câu hỏi D1a (dòng 73): thêm "Điều kiện có cách hiểu mặc định là đã biết, không dừng ở đây. Chỉ dừng khi: khóa 'Không có mặc định'; chữ trỏ nhiều chế độ; cụm không giải được (mục 6.7)."
- **S6.** Câu hỏi D1b (dòng 81): "Ở điều kiện vừa xác định (nêu rõ và mặc định), tài liệu có ghi hai số khác nhau không? Có thì dừng, dù số của tuyên bố trùng một số, kém hơn cả hai, hay khác cả hai."
- **S7.** Câu hỏi D2 (dòng 88): "Tuyên bố có từ khẳng định gắn ngay với con số không? Từ ở vế nói việc khác và tên tính năng không tính. Chỉ thiếu chữ 'lên đến' thì không phải D2." Danh sách từ đọc từ mục 6.2 của hướng dẫn, không chép tay.
- **S8.** Câu hỏi D3 (dòng 95): "Ở đúng điều kiện đã xác định ở Bước 3 (gồm mặc định)…".
- **S9.** Câu hỏi D4 (dòng 101): thêm "Gồm cả khi tuyên bố không nêu điều kiện và cách hiểu mặc định khác điều kiện của con số (`bo_dieu_kien`)."
- **S10.** D5, `ghi_chu_nho` (dòng 111): thêm "Mã IP khác nhánh không khớp; không trùng mã nào thì Sai."
- **S11.** Câu hỏi D6 (dòng 119): "Tài liệu có số cho thuộc tính, nhưng không có số ở điều kiện này; số của tuyên bố không trùng số nào và không đẹp hơn mọi số."
- **S12.** `CA_DAC_BIET` (dòng 739–814): bỏ mục "Cụm chung chung về ánh sáng: chưa có quy tắc" (dòng 745), thay bằng tóm tắt QĐ3. Sửa mục "Hai số cho tổng thời gian phát nhạc khi bật chống ồn" (dòng 781–786): thêm "chỉ khi điều kiện của tuyên bố, nêu rõ hoặc mặc định, là kèm hộp sạc và bật chống ồn; tuyên bố không nêu bộ phận thì là tai nghe, không so với số Tổng". Thêm mục chung (theo `nhom`) cho QĐ2, QT6, QĐ6. Chỉ chép luật, không chép câu của bộ thử.
- **S13.** "Quy tắc hay dùng" (dòng 1091–1097): "gắn với một mức" đổi thành "gắn ngay với con số". Thêm hai dòng: "Cách hiểu mặc định dùng ở mọi dòng D"; "Không chọn điều kiện theo con số".

**Kiểm mới**

- **S14.** Mẫu câu: đổi `{trích}` thành `{câu trích}` ở mục 8 của hướng dẫn (trang đọc bảng này). Thêm kiểm trong `kiem()` (dòng 1870–1875) và `kiem_nhan.py`: lý do có chuỗi dạng mã đoạn `<ma_mau>#<số>` trong ngoặc kép thì báo lỗi "Lý do chép mã đoạn thay cho câu trích".
- **S15.** Kiểm bằng chứng với thuộc tính: câu trích phải chứa đơn vị của thuộc tính tuyên bố (cột Đơn vị ở mục 6.1 cộng bảng chuẩn hóa đơn vị: nit, Hz, giờ/tiếng/h, phút/min, W, mAh, mã IP hoặc m/ATM, x). Không có thì nhắc ở khung vàng. Kiểm này bắt được lỗi lưu lệch kiểu tb-00009, tb-00010 (độ sáng mà câu trích nói 120Hz; kháng nước mà câu trích nói độ sáng). Có thể nhắc thêm khi đoạn bằng chứng không nằm trong `can_cu` của thuộc tính trong cấu hình; chỉ nhắc, không chặn, vì `can_cu` chưa đủ (thời lượng pin Buds3 Pro thiếu `#042`).
- **S16.** Nhiều đoạn cùng giá trị (nếu QĐ7 chọn A): sau khi bấm "Lấy đoạn đang bôi đen", trang tìm đúng chuỗi vừa bôi trong các đoạn khác của mẫu và hiện "Đoạn … cũng có chữ này · Thêm làm bằng chứng". Trang dùng chữ người gán bôi, không đọc tuyên bố. Chữ hướng dẫn ở dòng 1141 thêm "Ghi mọi đoạn có cùng con số ở cùng điều kiện".
- **S17.** Dừng ở D2 thì bắt buộc ghi `khang_dinh=<từ>` vào ghi chú. Trang kiểm từ đó có trong danh sách mục 6.2. Thiếu hoặc lạ thì báo lỗi.
- **S18.** Dừng ở D1a thì bắt buộc ghi nguyên nhân: `mac_dinh=<khóa không có mặc định>`, hoặc `chua_xac_dinh=<cụm>` (chữ trỏ nhiều chế độ, cụm không giải được). Báo lỗi khi D1a mà ghi chú chỉ có khóa có mặc định: "<khóa> có cách hiểu mặc định '<…>': dùng mặc định rồi dò tiếp". Đây là chiều ngược của kiểm `mac_dinh_khong_co` (dòng 142). Kiểm này chặn được nhóm lệch B2.
- **S19.** Dừng ở D1 mà ghi chú có `mac_dinh=` thì nhắc "D1 dừng trước khi xét điều kiện; không cần mac_dinh" (nếu QĐ5 chọn A).

**Cho lượt 2**

- **S20.** Khóa localStorage mới (dòng 1207: `gan_nhan_thu_v1` thành `gan_nhan_thu_v2`), `luot: 2`, tiêu đề "Bước 16 · lượt 2" (dòng 1005). Tệp tải về là `thu_luot2.jsonl` và `cau_hoi_nhan_luot2.md`. Nút "Nhập lại" từ chối bản ghi `luot: 1`. Lượt 1 giữ ở `data/nhan/thu.jsonl` (hoặc đổi tên `thu_luot1.jsonl`, ghi rõ trong nhật ký). `kiem_nhan.py` nhận tham số lượt.
- **S21.** Đồng hồ: dừng đếm khi không có thao tác quá 3 phút, ghi riêng số giây bị bỏ. Lượt 1 có hai tuyên bố cùng đúng 2.118 giây (nhật ký 01/11).
- **S22.** Khung bài quảng cáo (nếu QĐ1 chọn A): thu gọn sẵn, ghi "Gán theo chữ của tuyên bố. Câu tô vàng chỉ để kiểm tách. Thấy tuyên bố thiếu điều kiện thì ghi `tach=…` vào ô Câu hỏi nhãn, vẫn gán theo tuyên bố."

**Tiện ích**

- **S23.** Khung "Cụm điều kiện đã biết": hiện phụ lục cụm diễn đạt của nhóm và thuộc tính đang gán, cạnh khung mặc định (nếu QĐ2 chọn A). Đây cũng là nội dung lọc theo nhóm và thuộc tính, như khung mặc định.
- **S24.** Chữ hướng dẫn ô ghi chú (dòng 1157): liệt kê đủ mã `mac_dinh`, `ngoai_cau_hinh`, `ngoai_sau_loai`, `khang_dinh`, `chua_xac_dinh`, `nham_vai`.
- **S25.** Sửa docstring đầu tệp theo các kiểm mới; thêm test cho S14, S15, S17, S18 ở cả trang (phần tách bảng) và `kiem_nhan.py`.

## 7. Điểm dừng nhãn Lệch (Bước 16)

Ba tiêu chí của Bước 16 và cái cần có để biết đạt hay không. Đo sau khi gán lại lượt 2. Không chỉnh quy tắc sau khi thấy số đếm: quy tắc chốt ở tệp này trước khi gán lại.

**Tiêu chí 1 · Ít nhất 10 tuyên bố Lệch không thuộc loại "lên đến".**

- Định nghĩa đếm, ghi trước: nhãn lượt 2 có `nhan = LECH` và `dong_d = D4`. D2 là loại "lên đến". `doi_kieu_gia_tri` ở D4 (ví dụ điển hình thành định mức) vẫn tính.
- Cần có: nhãn lượt 2 theo bản 2 (sau rà tách nếu QĐ1 chọn A); `kiem_nhan.py` in số đếm theo dòng D và loại.
- Báo kèm: số ca theo loại biến đổi; số ca `bo_dieu_kien` (phụ thuộc mặc định); số ca trùng số khác hoạt động (QĐ8).
- Chỉ tính tuyên bố từ quảng cáo thông thường, không tính cặp tối thiểu.
- Không đạt: tăng bài sinh theo T9.1; vẫn thiếu thì đánh giá nhãn Lệch chủ yếu trên tập cặp tối thiểu và ghi giới hạn.

**Tiêu chí 2 · Kappa của riêng nhãn Lệch ít nhất 0,6, trên ít nhất 30 tuyên bố gồm mọi tuyên bố Lệch.**

- Cần một người thứ hai. Hiện chưa có; T9.1 cho tới 16/11.
- Ghi trước: kappa của Cohen hai lớp (Lệch / không Lệch). Báo thêm kappa bốn lớp và KTC bootstrap theo cụm bài.
- Mẫu: mọi tuyên bố Lệch của lượt 2, cộng tuyên bố chọn ngẫu nhiên (script, seed ghi trước) cho đủ ít nhất 30. Người thứ hai không biết cách chọn và không thấy nhãn. Dùng hướng dẫn bản 2 và trang có khóa lưu riêng. Không thảo luận trước khi tính.
- Lượt 1 so với lượt 2 không thay được tiêu chí này: cùng người, và hướng dẫn đổi giữa hai lượt.
- Không đạt: sửa hướng dẫn rồi gán lại.

**Tiêu chí 3 · Thử độ bao phủ trên 3 sản phẩm ngoài 12 mẫu nhận ra ít nhất 80% cụm điều kiện quyết định.**

- Chưa làm. Kế hoạch ghi "làm trước Bước 9". Nhật ký 27/10 đề xuất OPPO Reno14, OPPO Enco Air5 Pro, Galaxy Watch Ultra2, đang chờ duyệt.
- Cần có: duyệt 3 sản phẩm; tải và chia đoạn trang của chúng; người thực hiện liệt kê tay cụm điều kiện quyết định theo tiêu chí ở mục 4 của hướng dẫn; dò cụm của cấu hình (sau khi đã thêm cụm từ bộ thử) bằng một script so chuỗi đơn giản; đếm tỷ lệ cụm được nhận đúng loại và giá trị.
- Không đạt: bổ sung luật từ chính 3 trang đó.

**Kết luận.** Đạt cả ba thì giữ bốn nhãn. Không đạt thì sửa hướng dẫn, bổ sung luật, đo lại. Vẫn không đạt thì dùng phương án lùi (ba nhãn cộng cờ "thiếu hoặc đổi điều kiện"). Ghi quyết định vào nhật ký, báo CBHD.

Tiêu chí 2 và 3 có thể chưa đo được trong Bước 16. Cần người thực hiện quyết (và báo CBHD ở báo cáo bộ thử) cách xử lý: ví dụ tạm giữ bốn nhãn nếu tiêu chí 1 đạt, chốt cuối khi đo xong tiêu chí 2 và 3, muộn nhất trước Bước 27.

## 8. Chỗ kế hoạch, đề cương có vấn đề

1. **Điểm dừng không đo đủ được ở Bước 16.** Tiêu chí 3 cần bước thử độ bao phủ chưa làm. Tiêu chí 2 cần người thứ hai, mà kế hoạch cho tới 16/11 mới cần có. Kế hoạch nên ghi rõ Bước 16 kết luận tạm theo tiêu chí 1, và ngày chốt cuối.
2. **Bộ thử dùng chính 2 mẫu có ví dụ trong hướng dẫn.** Một số V gần trùng chữ tuyên bố của bộ thử (V21, V25, V47; nhật ký 31/10 đã nêu V45, V48). Các V này viết trước khi có bộ thử nên không phải lộ đáp án, nhưng gán lại và kappa trên bộ thử sẽ lạc quan. Không nên dùng chúng làm bằng chứng về độ rõ của hướng dẫn trong khóa luận. Độ tin cậy nhãn nên báo trên phần còn lại của tập phát triển và tập kiểm tra (Bước 32).
3. **Lượt 2 có thể không mù.** Nếu người thực hiện đã đọc phần B của `cau_hoi_nhan.md` (theo từng tuyên bố, có cả nhãn đang ghi), lượt 2 mang theo nhận xét đó. So lượt 1 với lượt 2 khi ấy đo tác động của bản 2 cộng tác động của nhận xét, không đo độ tin cậy.
4. **Định nghĩa Lệch của đề cương để ngỏ cách đọc "bỏ chữ lên đến".** Kế hoạch chọn cách đọc hẹp (T10 điểm 2, theo FTC 2012), hợp lý. Nhưng trang chép gần nguyên định nghĩa lên nút nhãn, và phần lớn nhãn D2 của lượt 1 không có từ khẳng định (phần B). Không sửa đề cương; thêm chú thích ở mục 3 của hướng dẫn và ở Chương 3.
5. **Nguy cơ nhãn chuẩn đi theo P.** Nhiều câu hỏi có một phương án dễ cho P (cụm lạ là D1a; chỉ đọc chữ của hãng). Chọn phương án theo khả năng cài của P làm FAR của đối chứng cao giả tạo. T4 nên ghi nguyên tắc này ở đầu mục: nhãn theo tài liệu và cách người mua hiểu; giới hạn của P ghi riêng (đã có ở T5.3 và mục 6.7 của hướng dẫn, nhưng chưa thành nguyên tắc chung).
6. **T3.4, T5.4, T5.5, T5.6 phải sửa theo bản 2.** Từ khẳng định và luật "gắn với con số" (bước trích xuất phải ghi từ khẳng định kèm câu trích của giá trị); điều kiện là một tập khi có cụm phủ (QĐ3); `{câu trích}` (QT10); `luot: 2` và các mã ghi chú mới.
7. **Lịch.** Bước 16 ghi 30–31/10, Mốc 2 là 31/10; hôm nay đã là 01/11. Các bước sau cần dời ngày.
8. **T10 có hai điểm cùng số 15.**
9. **Tiêu chí 2 chưa định nghĩa "kappa của riêng nhãn Lệch"** và cách chọn 30 tuyên bố. Chọn theo nhãn của người thứ nhất làm mẫu không ngẫu nhiên. Cần ghi trước khi đo (mục 7).

## 9. Chỗ còn chưa chắc

1. **Tiêu chí gắn điều kiện, ý 2 (QĐ1).** Vế "tác dụng của con số" cần phán đoán, hai người dễ khác nhau. Ca khó nhất: câu có cả điều kiện trực tiếp lẫn cụm phủ ở vế tác dụng.
2. **QĐ4.** Chưa có số liệu người đọc hiểu "hơn X" thế nào. A có thể gán Lệch cho cách nói mà người đọc coi như con số thường.
3. **QĐ2, ý 2.** Ghép "ánh sáng mạnh" với chế độ "ngoài trời" của Apple là suy theo nghĩa; trang Apple không tả hoàn cảnh kích hoạt. Cấu hình có thể cần một chế độ chung "sáng cao dưới ánh sáng mạnh" cho cả Apple ("ngoài trời") và Xiaomi ("tự tăng sáng"). Đây là đề xuất cho Bước 27, chưa kiểm.
4. **QT8.** D1b chặt hơn nghĩa ở ca con số kém hơn cả hai số. Giảm bằng cách báo FAR có và không có các ca `tai_lieu_mau_thuan`.
5. **QT9.** Có người coi IPX4 và IP57 không mâu thuẫn, vì thiết bị chống ngâm thường chịu được nước bắn. Hướng dẫn cấm dùng hiểu biết ngoài tài liệu, nên giữ D5.
6. **Ngưỡng 1/4 ở QĐ8** không có căn cứ số; chỉ cần chốt trước khi đếm.
7. **QĐ5 chọn A** làm phân tích độ nhạy ở Bước 37 thành cận trên. Cần số chính xác thì phải xem lại tay.
8. **Thời gian lượt 2** sẽ thấp hơn lượt 1 vì đã quen tuyên bố và công cụ. Không dùng thẳng để ước thời gian gán tập mới.
9. **Rà tách có thể thêm tuyên bố** (tiêu chí ý 4), làm đổi tổng 66 và mẫu số của các chỉ số đã tính ở Bước 14, 15.

## 10. Việc làm sau khi duyệt

1. **Duyệt.** Người thực hiện ghi chọn QĐ1–QĐ8 vào `luan_van/nhat_ky.md`.
2. **Rà tách** (nếu QĐ1 chọn A). Người thực hiện tự làm, không có gợi ý của AI. Sửa qua `data/tuyen_bo/thu_nhap.csv`, chạy `scripts/chuyen_tuyen_bo.py` ghi `data/tuyen_bo/thu.jsonl`, ghi `tach_sua=…` ở `ghi_chu`. Cập nhật `data/tuyen_bo/huong_dan_tach_tay.md` (tiêu chí gắn điều kiện, quy tắc 5).
3. **Viết `data/huong_dan_gan_nhan.md` bản 2.** Sửa mục 1, 2, 3 (chú thích), 5, 6.2, 6.5, 6.6, 6.7, 7, 8, 11.2; thêm 6.8, 6.9 và phụ lục cụm diễn đạt; sửa ghi chú, lý do của các V ở QĐ2, QĐ5; thêm ví dụ mới từ Xiaomi 15T, Apple Watch SE 3 hoặc ví dụ giả định (không lấy iPhone 17, Galaxy Buds3 Pro để tránh gần trùng bộ thử); thêm mục "Thay đổi so với bản 1". Chạy script kiểm câu trích và kiểm bảng mặc định khớp YAML.
4. **Cấu hình** (`data/cau_hinh/chung.yaml`, `dien_thoai.yaml`, `tai_nghe.yaml`). Thêm `tu_khang_dinh.tu_muc_san` (QĐ4), danh sách cụm phủ (QĐ3), cụm mới của QĐ2 ("ánh nắng", "dưới ánh nắng", "tổng cộng", "kết hợp hộp sạc", "Telephoto … chất lượng quang học"; W đi cùng cách sạc); tách cách đọc "sử dụng liên tục" phía tuyên bố và phía tài liệu. Chạy `scripts/kiem_cau_hinh.py` và test. Cụm lấy từ mẫu tập phát triển, được phép theo T3.5 điểm 4.
5. **Trang và `scripts/kiem_nhan.py`.** Làm S1–S25, sinh lại `data/nhan/cong_cu_gan_nhan.html`, chạy test.
6. **Gán lại lượt 2** (QT11). Xuất `data/nhan/thu_luot2.jsonl`; giữ lượt 1.
7. **Tính lại.** Recall@k (`scripts/do_recall.py`), B0 (`scripts/chay_b0.py`, bộ nhớ đệm giữ phần không đổi), phân bố nhãn, tiêu chí 1 của điểm dừng, đếm của QĐ8.
8. **Cập nhật kế hoạch.** T3.4, T4, T5.4–T5.6, T10 điểm 4; ô của Bước 16; nhật ký; báo cáo bộ thử gửi CBHD (`ket_qua/bo_thu/bao_cao.md`), nêu rõ tiêu chí 2 và 3 đo khi nào.
