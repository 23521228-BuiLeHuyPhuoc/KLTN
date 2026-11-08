# Bước 29, 30: câu lệnh tách tự động, B1, B2

Opus viết ngày 08/11/2026, trước khi cài. Đây là bản đầu (lần thử 1) của ba câu lệnh; bản cuối chốt ở Bước 33 và lưu kèm mã băm. Theo T6.2 quy tắc 3, số lần thử câu lệnh của B0–B2 bằng số lần thử dành cho câu lệnh trích xuất của P; mỗi lần sửa câu lệnh ghi một dòng vào nhật ký.

Căn cứ: T5.8, T6.1, T6.2, T12.2, T12.3, T12.5 của kế hoạch; `data/huong_dan_gan_nhan.md` (bản 2, tiêu đề tệp ghi rõ tệp đi vào câu lệnh của B2); `data/tuyen_bo/huong_dan_tach_tay.md`; `luan_van/buoc22_thiet_ke_trich_xuat.md` (định dạng bộ thông số mà B1 nhận).

## 1. Phần dùng chung cho B1 và B2: hướng dẫn trong câu lệnh

`{huong_dan}` là chữ của `data/huong_dan_gan_nhan.md`, cắt bằng script theo tiêu đề, không gõ tay:

- mục "## 3. Bốn nhãn", "## 4. Tài liệu nào là bằng chứng", "## 5. Cách hiểu mặc định ..." (bỏ tiểu mục "### 5.1"), "## 6. Các quy tắc so sánh", "## 7. Thứ tự quyết định D1–D6";
- không đưa mục 1–2 (quy trình, tách tuyên bố), 8 (ghi nhãn), 9–12 (ví dụ, bảng phủ, ca đã chốt, thay đổi), 13 (phụ lục cụm).

Lý do chọn: đây là phần định nghĩa nhãn, bằng chứng, cách hiểu mặc định, quy tắc so và thứ tự quyết định, tương ứng T4.2–T4.5 mà T12.2, T12.3 ghi; P cũng cài đúng các mục này. Hướng dẫn chỉ có chữ của tập phát triển và ví dụ tự đặt, nên đưa vào câu lệnh không lộ tập kiểm tra (T6.2 quy tắc 4). Test kiểm `{huong_dan}` không chứa mã mẫu tập kiểm tra.

B1 và B2 dùng cùng mô hình, cùng tham số với P và B0 (nhiệt độ 0, chế độ JSON, chung bộ nhớ đệm), cùng top-k đoạn (B2) hoặc cùng bộ thông số của P (B1).

Đầu ra của cả hai: JSON `{"nhan": …, "ly_do": …}` (B2 thêm `"doan": [...]`). Ánh xạ nhãn: "Đúng" → `DUNG`, "Sai" → `SAI`, "Lệch điều kiện" → `LECH`, "Chưa đủ thông tin" → `CHUA_DU` (so sau khi chuẩn hóa chữ: NFC, chữ thường, gộp khoảng trắng; chấp nhận thêm mã `DUNG`, `SAI`, `LECH`, `CHUA_DU`). Nhãn khác hay JSON hỏng thì `LOI`, như B0; không đoán.

## 2. B2 (T12.3): hướng dẫn, bốn ví dụ, tuyên bố, top-k đoạn

`{vi_du}`: bốn ví dụ của hướng dẫn mục 9, mỗi nhãn một ví dụ, có ví dụ Lệch điều kiện (T6.1):

| Nhãn | Ví dụ | Vì sao chọn |
|---|---|---|
| Đúng | V09 (Galaxy Buds3 Pro nghe nhạc 6 giờ khi bật chống ồn) | Ví dụ của đề cương, điều kiện nêu rõ, bỏ "lên đến" vẫn khớp |
| Sai | V16 (Galaxy Buds3 Pro nghe nhạc 8 giờ) | Thuận lợi hơn mọi giá trị của tai nghe dù tổng kèm hộp sạc lớn hơn |
| Lệch điều kiện | V24 (iPhone 17 dùng pin được 30 giờ) | Kiểu lỗi chính của đề tài: không nêu hoạt động, con số của hoạt động thuận lợi hơn |
| Chưa đủ thông tin | V46 (iPhone 17 sạc nhanh chỉ trong 20 phút với bộ sạc 40W) | D1a: thiếu điều kiện không có mặc định (mốc phần trăm) |

Mỗi ví dụ in dạng: `Tuyên bố: …` / `Bằng chứng: …` (dòng "Bằng chứng" của ví dụ trong hướng dẫn) / `Kết quả: {"nhan": "…", "doan": [...], "ly_do": "…"}` (lý do là dòng "Lý do" của ví dụ). Script đọc bốn ví dụ từ mục 9, không gõ tay. Bốn tuyên bố này là câu của hướng dẫn, không phải tuyên bố tách từ quảng cáo; nếu trùng chữ một tuyên bố của tập phát triển thì vẫn chỉ ảnh hưởng tập phát triển.

<!-- CAU_LENH_B2: bat_dau -->
```text
Bạn là người kiểm chứng tuyên bố về thông số kỹ thuật trong quảng cáo. Chỉ dựa vào các đoạn tài liệu chính hãng dưới đây và hướng dẫn gán nhãn, gán cho tuyên bố đúng một trong bốn nhãn: "Đúng", "Sai", "Lệch điều kiện", "Chưa đủ thông tin".

HƯỚNG DẪN GÁN NHÃN
{huong_dan}

VÍ DỤ
{vi_du}

Trả về đúng một đối tượng JSON, không thêm chữ nào khác: {"nhan": "<một trong bốn nhãn>", "doan": ["<mã đoạn làm bằng chứng>"], "ly_do": "<lý do ngắn, có câu trích nguyên văn của tài liệu>"}

Tuyên bố: {tuyen_bo}
Tài liệu:
{doan_1..k}
```
<!-- CAU_LENH_B2: ket_thuc -->

`{doan_1..k}` định dạng như B0 và P: `[<mã đoạn>] <văn bản>`, cách nhau một dòng trống, hạng BM25 giảm dần.

## 3. B1 (T12.2): hướng dẫn và bộ thông số của P

B1 nhận đúng đầu vào của bộ quyết định trong P: bộ thông số của tuyên bố và các bộ thông số trích từ tài liệu, sau neo nguồn và kiểm tra đầy đủ (bản ghi Bước 22, mục 8 của thiết kế trích xuất). B1 không nhận chữ tuyên bố gốc hay đoạn tài liệu, để khác biệt giữa B1 và P chỉ nằm ở người ra quyết định (LLM hay luật A–D). Không có ví dụ (T12.2 không ghi ví dụ; ví dụ là phần của B2).

`{bo_thong_so_tuyen_bo}`, `{bo_thong_so_tai_lieu}`: JSON của mục tuyên bố và danh sách mục tài liệu, bỏ các khóa nội bộ (`nguon_dieu_kien`, `bo_qua`, `dieu_kien_phu`) và mục `khac_san_pham`; giữ `ma_doan`, `thuoc_tinh`, `gia_tri`, `don_vi`, `dieu_kien`, `kieu_gia_tri`, `cum_kieu`, `dieu_kien_khac`, `ngu_canh`, `trich`. In với `ensure_ascii=False`, khóa sắp xếp, thụt lề 1.

<!-- CAU_LENH_B1: bat_dau -->
```text
Bạn gán nhãn cho một tuyên bố quảng cáo về thông số kỹ thuật. Bạn không có văn bản gốc; bạn chỉ có bộ thông số đã trích từ tuyên bố và từ tài liệu chính hãng (JSON dưới đây, mỗi trường kèm câu trích nguyên văn ở "trich"). Theo hướng dẫn gán nhãn, gán cho tuyên bố đúng một trong bốn nhãn: "Đúng", "Sai", "Lệch điều kiện", "Chưa đủ thông tin".

HƯỚNG DẪN GÁN NHÃN
{huong_dan}

CÁCH ĐỌC BỘ THÔNG SỐ
- "dieu_kien": các điều kiện đã nhận ra, ghi bằng tên và giá trị như cột "Khóa cấu hình" ở mục 5 của hướng dẫn. Điều kiện bắt buộc không có trong "dieu_kien" là văn bản không nêu.
- Điều kiện dạng số ghi {"so": ..., "don_vi": ...}.
- "kieu_gia_tri": khong_neu (không nêu), toi_da, dien_hinh, dinh_muc, thich_ung, khang_dinh (có từ khẳng định gắn với con số); "cum_kieu" là chữ đó.
- "dieu_kien_khac": cụm điều kiện chưa có trong cấu hình, kèm loại và câu trích.
- "ngu_canh": cụm chỉ là ngữ cảnh, không làm đổi nhãn.
- "gia_tri" của kháng nước là mã IP {"bui": ..., "nuoc": ...}, số mét theo ISO 22810, "khong" (không kháng nước) hoặc "co" (có kháng nước, không nêu mã).

Trả về đúng một đối tượng JSON, không thêm chữ nào khác: {"nhan": "<một trong bốn nhãn>", "ly_do": "<lý do ngắn>"}

Bộ thông số của tuyên bố:
{bo_thong_so_tuyen_bo}
Bộ thông số trích từ tài liệu:
{bo_thong_so_tai_lieu}
```
<!-- CAU_LENH_B1: ket_thuc -->

Tuyên bố mà P trích thất bại (không có `gia_tri` hay `thuoc_tinh`) vẫn đưa vào B1 như thường: B1 thấy bộ thông số thiếu và tự quyết; ghi số ca này trong bảng kết quả.

## 4. B3: SemViQA

Không có câu lệnh. Đầu vào là cặp (chữ tuyên bố, văn bản ghép của top-k đoạn) hoặc từng cặp (tuyên bố, đoạn) rồi gộp; cách gộp chọn ở Bước 33 trên tập phát triển. Cần cài gói `semviqa` và tải bốn mô hình từ Hugging Face (`SemViQA/tc-xlmr-viwikifc`, `tc-xlmr-isedsc01`, `tc-infoxlm-viwikifc`, `tc-infoxlm-isedsc01`): **chờ người thực hiện đồng ý tải** trước khi cài.

## 5. Bước 29: tách tuyên bố tự động (T12.5)

Quy tắc trong câu lệnh chép ý của `data/tuyen_bo/huong_dan_tach_tay.md` (năm quy tắc, bốn tiêu chí gắn điều kiện, danh sách bỏ qua), để tách tự động và tách tay theo cùng quy tắc. Ví dụ là bốn dòng ví dụ của hướng dẫn tách tay (sản phẩm tự đặt hoặc câu không lấy từ bài nào). `{bang_thuoc_tinh}` như câu lệnh trích xuất của P.

<!-- CAU_LENH_TACH: bat_dau -->
```text
Tách bài quảng cáo về {ten_nhom} dưới đây thành các tuyên bố về thông số kỹ thuật. Không phán đúng sai.

QUY TẮC
1. Mỗi tuyên bố chỉ có một thuộc tính và một con số (hoặc một mã như IP68). Câu "pin 30 giờ, sạc 50% trong 20 phút" tách thành 2 tuyên bố.
2. Giữ ngữ cảnh: viết thành một câu ngắn gồm tên sản phẩm, thuộc tính, con số và điều kiện, đúng như bài nói. Thay "máy", "tai nghe này" bằng tên sản phẩm. Điều kiện thuộc con số thì đưa vào tuyên bố, kể cả khi nằm ở câu trước hay câu sau.
3. Điều kiện thuộc con số khi: bổ nghĩa trực tiếp cho con số (cùng cụm, trong ngoặc ngay sau con số, hoặc "khi / ở / với / trong / dưới / cùng / kèm …" đi liền con số); hoặc là điều kiện cụ thể ở vế nói tác dụng của chính con số ("… 2500 nit giúp nhìn rõ dưới nắng"). Điều kiện hay từ khẳng định ở vế nói về tính năng hay việc khác thì không thuộc con số.
4. Không thêm điều kiện bài không nói, không sửa con số. Giữ chữ "lên đến" nếu bài có. Từ khẳng định ("luôn", "đảm bảo", "ít nhất", "mọi lúc", "hơn", "trên", "không dưới", "trở lên") chỉ giữ khi gắn với con số.
5. Hai lần nhắc trong cùng bài chỉ gộp làm một khi cùng con số và cùng điều kiện. Một con số nhắc hai lần, một lần kèm điều kiện, một lần không, thì là hai tuyên bố.

CHỈ TÁCH CÁC THUỘC TÍNH SAU
{bang_thuoc_tinh}

BỎ QUA
Kích thước, trọng lượng, Bluetooth, chip, số chấm camera (48MP), giá, khuyến mãi, quà tặng, số đánh giá sao, số người dùng, so sánh với máy khác, câu khen không có con số ("pin trâu", "dùng cả ngày"). Cụm khen đứng cạnh một con số ("cả ngày", "suốt ngày dài", "không lo hết pin", "siêu bền", "bền bỉ", "vượt trội", "tuyệt đối", "trọn vẹn", "không giới hạn") cũng bỏ khỏi tuyên bố.

ĐẦU RA
Trả về đúng một danh sách JSON, không thêm chữ nào khác. Mỗi phần tử: {"tuyen_bo": "<câu ngắn>", "cau_goc": "<câu hoặc vế câu chứa con số, chép nguyên văn từ bài>", "thuoc_tinh_du_kien": "<mã thuộc tính>"}. Bài không có tuyên bố nào thì trả [].

VÍ DỤ
- cau_goc "nghe nhạc liền 7 tiếng ngay cả khi bật chống ồn" -> {"tuyen_bo": "Galaxy Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn", "thuoc_tinh_du_kien": "thoi_luong_pin"}
- cau_goc "sạc nhanh 60% chỉ trong 25 phút" -> {"tuyen_bo": "Điện thoại A sạc 60% trong 25 phút", "thuoc_tinh_du_kien": "sac_nhanh"}
- cau_goc "Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin" -> {"tuyen_bo": "Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin", "thuoc_tinh_du_kien": "thoi_luong_pin"}
- cau_goc "Màn hình Điện thoại A sáng 2500 nit, giúp bạn nhìn rõ dưới nắng" -> {"tuyen_bo": "Điện thoại A sáng 2500 nit dưới nắng", "thuoc_tinh_du_kien": "do_sang"}

BÀI QUẢNG CÁO
{bai}
```
<!-- CAU_LENH_TACH: ket_thuc -->

Python sau LLM:

1. Đọc danh sách JSON (trần hoặc trong khối ```json); hỏng thì bài đó `LOI`, không đoán.
2. Giữ phần tử có `thuoc_tinh_du_kien` thuộc thuộc tính của nhóm (T5.8). Đếm số bị bỏ theo lý do.
3. `cau_goc` không có nguyên văn trong bài (so sau khi gộp khoảng trắng, NFC) thì vẫn giữ tuyên bố nhưng đánh dấu `cau_goc_khong_khop`; không dùng làm lý do bỏ, vì tách tay cũng chỉ đòi câu gốc để truy lại.

So với tách tay (Precision, Recall trên tập phát triển):

- Hai tuyên bố trùng khi cùng bài, cùng thuộc tính và cùng giá trị sau chuẩn hóa (T5.8): con số và đơn vị đọc bằng `chuan_hoa.tim_gia_tri` (cùng khóa đơn vị, `bang_nhau`; giờ và phút quy đổi), mã IP bằng `tach_ip`, ISO 22810 bằng `doc_iso_22810`. Tuyên bố có nhiều con số thì lấy con số đầu tiên có đơn vị đúng của thuộc tính.
- Ghép một đối một trong từng bài, tham lam theo thứ tự xuất hiện. Precision = số cặp ghép / số tuyên bố tự động; Recall = số cặp ghép / số tuyên bố tách tay. Báo chung và chia theo chế độ sinh (`ten`, `ten_thong_so`), theo LLM sinh, theo nhóm sản phẩm.
- Không xét điều kiện khi ghép (T5.8 chỉ đòi thuộc tính và giá trị). Ghi thêm, để tham khảo, tỉ lệ cặp ghép có cùng tập điều kiện sau khâu hiểu điều kiện của Bước 22 (tức tách tự động có giữ điều kiện như người tách không).

Tập phát triển gồm 24 bài bộ thử (đã có tách tay `thu.jsonl`) và 16 bài của hai mẫu mới (chờ người thực hiện tách ở Bước 19). Chạy được ngay trên bộ thử; báo lại khi có phần tách tay của 16 bài.
