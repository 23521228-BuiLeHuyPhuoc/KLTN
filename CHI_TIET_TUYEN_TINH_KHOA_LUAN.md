# Chi tiết tuyến tính của khóa luận

| | |
|---|---|
| **Tên đề tài (tiếng Việt)** | Phương pháp kiểm chứng tuyên bố về thông số kỹ thuật có điều kiện ràng buộc trong quảng cáo |
| **Tên đề tài (tiếng Anh)** | A method for verifying conditional technical specification claims in advertisements |
| **Sinh viên** | Bùi Lê Huy Phước – 23521228 |
| **Cán bộ hướng dẫn (CBHD)** | ThS Trần Hồng Nghi |
| **Thời gian** | 15/09/2026 – 31/12/2026; bảo vệ theo lịch Khoa (dự kiến tháng 01/2027) |
| **Cập nhật** | 10/10/2026, khớp với đề cương trong thư mục `de_cuong/` (bản đã bổ sung Bảng 1, Bảng 2 và câu hỏi nghiên cứu, xem mục 4.4) |

> **Trạng thái:** đề cương đã sửa theo nhận xét của Khoa, đang chờ CBHD xác nhận. Repo chưa có dữ liệu thực nghiệm và chưa có kết quả. Mọi số giờ, quy mô và ngày tháng dưới đây là ước lượng. Sau bộ thử ban đầu (bước 15) phải cập nhật lại bằng số đo thật.

**Quy ước tên gọi để không nhầm:**

| Ký hiệu | Nghĩa |
|---|---|
| Bước 01–45 | Các bước công việc |
| Mốc 0–8 | Các mốc |
| M1–M4 | Mục tiêu trong đề cương |
| CH1–CH3 | Câu hỏi nghiên cứu trong đề cương |
| H1–H4 | Giả thuyết (mục 8.6) |
| B0–B3 | Các phương pháp đối chứng |
| P | Phương pháp đề xuất |

---

## 0. Cách dùng tài liệu này

Repo có hai tài liệu chính:

| Tài liệu | Trả lời câu hỏi | Dùng khi |
|---|---|---|
| Đề cương (`de_cuong/23521228_BuiLeHuyPhuoc_DeCuongKLTN.docx`) | Làm gì, vì sao, tính mới là gì, đến khi nào | Nộp Khoa, gửi CBHD, viết Chương 1 |
| File này | Làm thế nào, theo thứ tự nào, khi nào xong | Hằng ngày |

**Thứ tự đọc:**

1. Mục 1: đề tài trong một trang.
2. Mục 2: tính mới và cách chứng minh.
3. Mục 3: bảng tuyến tính các bước.
4. Bắt đầu bước đang tới ở mục 10.

Mục 5–9 là quy chuẩn và đặc tả, chỉ đọc khi một bước trỏ tới.

**Quy tắc tuyến tính:**

1. Mỗi bước chỉ cần kết quả của các bước có số nhỏ hơn. Số thứ tự cũng là thứ tự bắt đầu làm.
2. Một số bước chạy xen kẽ, chủ yếu là các bước viết chương. Cột "Ngày" trong bảng ở mục 3.2 ghi rõ khoảng thời gian.
3. Mỗi bước có tiêu chí "Xong khi". Bước chỉ được đánh dấu xong khi đạt đủ tiêu chí đó.
4. Khi đề cương và file này khác nhau, sửa cho khớp rồi ghi một dòng vào nhật ký (mục 5.4).

---

## 1. Đề tài trong một trang

**Vấn đề.** CopyPro tạo quảng cáo bằng LLM nhưng không có nguồn thông số để đối chiếu. Bài viết vì vậy có thể chứa con số đúng nhưng bị tách khỏi điều kiện công bố. Ví dụ, bài ghi "sạc 50% trong 20 phút" mà bỏ "với bộ tiếp hợp 40W trở lên".

Các phương pháp kiểm chứng hiện có chủ yếu xét mức khớp nội dung, chưa biểu diễn tường minh điều kiện này:
- tập ba nhãn như FEVER không có chỗ cho loại lỗi này;
- Fathom đạt F1 bằng 0 ở lớp Cherry-picking của AVeriTeC.

**Bài toán.**

- **Đầu vào:**
  - bài quảng cáo q do LLM tạo;
  - mẫu sản phẩm s do người dùng chọn;
  - kho tài liệu chính hãng D(s) của mẫu đó.
- **Đầu ra:** với mỗi tuyên bố có điều kiện ràng buộc c trong q:
  - nhãn y(c) thuộc {Đúng, Sai, Lệch điều kiện, Chưa đủ thông tin};
  - đoạn nguồn e(c);
  - lý do r(c).

**Tuyên bố có điều kiện ràng buộc** là tuyên bố nêu giá trị của một thuộc tính nằm trong danh sách thuộc tính có điều kiện ràng buộc của nhóm sản phẩm (tệp cấu hình, bước 07). Điều kiện ràng buộc có sáu loại:

1. Chế độ hoạt động.
2. Bộ phận.
3. Phụ kiện.
4. Điều kiện đo.
5. Phiên bản.
6. Kiểu giá trị.

**Phương pháp P** có 5 khối:

1. **Tách và lọc tuyên bố tự động.** LLM tách bài thành tuyên bố. Python chỉ giữ tuyên bố có thuộc tính trong tệp cấu hình.
2. **Truy hồi BM25** trong tài liệu của đúng mẫu sản phẩm.
3. **Trích xuất có neo nguồn.**
   - LLM chuyển tuyên bố và bằng chứng thành bộ thông số: sản phẩm và phiên bản, bộ phận, thuộc tính, giá trị, đơn vị, điều kiện ràng buộc, kiểu giá trị.
   - Mỗi trường kèm câu trích nguyên văn.
   - Python loại trường không neo được vào nguồn.
   - Một bước kiểm tra đầy đủ bổ sung điều kiện bị LLM bỏ sót.
4. **Chuẩn hóa** giá trị, đơn vị và kiểu giá trị.
5. **Bộ quyết định A–D** (mục 6.2 và 7.5) đọc tệp cấu hình điều kiện theo nhóm sản phẩm, rồi sinh lý do từ dấu vết quyết định.

**Đối chứng:**

| Ký hiệu | Mô tả |
|---|---|
| B0 | LLM đọc bằng chứng, gán 3 nhãn |
| B1 | LLM nhận cùng bộ thông số và cùng hướng dẫn gán nhãn với P, gán 4 nhãn |
| B2 | LLM đọc bằng chứng, gán 4 nhãn theo hướng dẫn, kiểu AVeriTeC |
| B3 | Mô hình SemViQA-TC đã công bố, 3 nhãn |
| P−ĐK | P bỏ đối chiếu điều kiện |
| P−NN | P bỏ neo nguồn |

**Dữ liệu:**

- Khoảng 12 mẫu: 5 điện thoại, 4 tai nghe không dây, 3 đồng hồ thông minh, của ít nhất 3 hãng.
- Quảng cáo do CopyPro sinh:
  - 2 LLM: Gemini 2.5 Flash và Llama 3.3 70B;
  - 3 loại bài: mô tả sản phẩm, bài đăng mạng xã hội, trang đích;
  - 2 chế độ: chỉ tên sản phẩm, hoặc tên kèm đoạn thông số.
- Khoảng 250–300 tuyên bố có nhãn, kể cả khoảng 60 tuyên bố của bộ thử ban đầu (thuộc tập phát triển).
- 100–120 biến thể cặp tối thiểu.
- Chia tập theo mẫu sản phẩm: khoảng 4 mẫu cho tập phát triển, 8 mẫu cho tập kiểm tra.

**Chỉ số chính:**

- FAR: tỷ lệ tuyên bố bị gán Đúng trong số các tuyên bố có nhãn chuẩn khác Đúng;
- F1 của nhãn Lệch điều kiện;
- Macro-F1;
- Recall của nhãn Đúng.

**Câu hỏi nghiên cứu và giả thuyết** (đề cương mục 2 và Nội dung 3; cách kết luận ở mục 8.6):

| Câu hỏi | Giả thuyết |
|---|---|
| CH1. Đối chiếu tường minh điều kiện có giảm tỷ lệ tuyên bố sai hoặc lệch bị chấp nhận là Đúng so với các cách kiểm chứng hiện có, mà không bỏ sót nhiều tuyên bố đúng? | H1: P có FAR thấp hơn B0–B3. H4: Recall của nhãn Đúng không thấp hơn quá 5 điểm phần trăm so với đối chứng tốt nhất |
| CH2. Quy tắc tường minh trên dữ liệu đã neo nguồn có phát hiện Lệch điều kiện tốt hơn để LLM tự gán nhãn? | H2: P có F1 của nhãn Lệch điều kiện cao hơn B1 và B2 |
| CH3. Neo nguồn và đối chiếu điều kiện đóng góp thế nào? | H3: P tốt hơn P−NN về FAR và F1 Lệch; P−ĐK để kiểm tra hợp lý |

**Sản phẩm cuối:**

1. Bộ dữ liệu, hướng dẫn gán nhãn, tệp cấu hình điều kiện.
2. Mã nguồn P và các đối chứng, có kiểm thử.
3. Báo cáo thực nghiệm.
4. Tính năng "Kiểm chứng thông số" chạy trên CopyPro.
5. Khóa luận và slide bảo vệ.

### 1.1 Ví dụ xuyên suốt (dùng lại trong khóa luận và khi bảo vệ)

Trang Galaxy Buds3 Pro (Samsung Việt Nam, truy cập 09/10/2026) ghi:

- phát nhạc lên đến 6 giờ khi bật chống ồn (ANC), lên đến 7 giờ khi tắt ANC;
- tai nghe đạt chuẩn IP57;
- chú thích "Hộp sạc không có khả năng kháng nước".

Giả sử CopyPro sinh câu: *"Galaxy Buds3 Pro nghe nhạc liền 7 tiếng ngay cả khi bật chống ồn, chuẩn IP57 nên cả hộp sạc cũng không sợ nước."*

| Tuyên bố tách ra | Điều kiện của tuyên bố | Tài liệu | Nhãn | Lý do sinh tự động |
|---|---|---|---|---|
| Nghe nhạc 7 giờ khi bật chống ồn | chế độ = bật ANC | Bật ANC: 6 giờ; 7 giờ là khi tắt ANC | **Lệch điều kiện** | "Giá trị 7 giờ chỉ đúng khi tắt chống ồn (nguồn: ...); tuyên bố ghi bật chống ồn." |
| Hộp sạc chống nước chuẩn IP57 | bộ phận = hộp sạc | IP57 là của tai nghe; hộp sạc không kháng nước | **Lệch điều kiện** | "Chuẩn IP57 áp dụng cho tai nghe; tài liệu ghi hộp sạc không có khả năng kháng nước." |

Cách kiểm chứng ba nhãn thấy con số 7 giờ và chuẩn IP57 đều có trong tài liệu nên dễ trả về Supported. Đây chính là lỗi mà đề tài khắc phục.

---

## 2. Tính mới, đóng góp, cải tiến và cách chứng minh từng ý

Hội đồng sẽ hỏi: "Em làm gì mà các bài đã công bố chưa làm, và bằng chứng nào cho thấy nó tốt hơn?" Bảng dưới gắn mỗi ý với bằng chứng sẽ có.

| Ý (theo đề cương mục 3) | Chứng minh bằng | Bước | Bảng/hình trong khóa luận |
|---|---|---|---|
| **Tính mới 1:** nhãn Lệch điều kiện được quyết định bằng đối chiếu điều kiện tường minh | P so với B1 (cùng dữ liệu cấu trúc và cùng hướng dẫn, LLM tự quyết) và B2 về F1 Lệch; P so với P−ĐK | 27, 28, 33, 35 | Bảng kết quả chính, bảng phân tích thành phần |
| **Tính mới 2:** neo nguồn loại giá trị và điều kiện bịa; kiểm tra đầy đủ phát hiện điều kiện bị bỏ sót | P so với P−NN; độ đúng từng trường trích xuất; số trường bị loại, số điều kiện được bổ sung | 23, 27, 28, 36 | Bảng độ đúng trích xuất, bảng phân tích thành phần |
| **Đóng góp 1:** phương pháp P có mã nguồn và kiểm thử | ≥30 kiểm thử cho các quy tắc A–D, gồm mọi ví dụ của hướng dẫn | 26 | Phụ lục kiểm thử |
| **Đóng góp 2:** bộ dữ liệu tiếng Việt 4 nhãn và tập cặp tối thiểu | Thống kê dữ liệu; kappa giữa hai người gán; kappa khi gán lại | 19–21, 29 | Bảng thống kê dữ liệu, bảng độ tin cậy nhãn |
| **Đóng góp 3:** đánh giá có đối chứng | 7 hệ thống trên cùng tuyên bố, cùng bằng chứng, cùng LLM; khoảng tin cậy; McNemar có hiệu chỉnh Holm | 33, 35, 37 | Bảng kết quả chính, hình khoảng tin cậy |
| **Đóng góp 4:** tính năng trong CopyPro | Chạy trên quảng cáo của CopyPro; kết quả đầu–cuối; thời gian mỗi bài; video | 32, 34, 38, 39 | Hình giao diện, bảng thời gian |
| **Cải tiến so với ba nhãn (FEVER, ViFactCheck, SemViQA)** | FAR của P so với B0, B3 | 33, 35 | Bảng kết quả chính |
| **Cải tiến so với LLM gán nhãn bằng câu lệnh (kiểu AVeriTeC)** | F1 Lệch của P so với B2 | 33, 35 | Bảng kết quả chính |
| **Cải tiến so với LLM kết hợp quy tắc của [16]** | Kiểm chứng từng tuyên bố; kết quả theo loại biến đổi trên tập cặp tối thiểu | 20, 35 | Bảng theo loại biến đổi |
| **Cải tiến so với phát hiện ảo giác mức thuộc tính [17] và MiniCheck [15]** | Phân biệt Sai với Lệch: ma trận nhầm lẫn | 35 | Hình ma trận nhầm lẫn |

**Câu trả lời một câu khi bị hỏi về tính mới:** "Các phương pháp hiện có chủ yếu xét con số có khớp tài liệu hay không. Em biểu diễn thêm điều kiện ràng buộc của từng thông số, trích xuất có kiểm tra câu trích, và quyết định nhãn Lệch điều kiện bằng quy tắc tường minh. Nhờ vậy, tuyên bố đúng số nhưng sai điều kiện không còn bị chấp nhận, và hệ thống chỉ ra được điều kiện nào bị bỏ hoặc bị đổi."

---

## 3. Lộ trình tổng thể

### 3.1 Các mốc

| Mốc | Ngày | Điều kiện đạt mốc | Gửi CBHD |
|---|---|---|---|
| Mốc 0 | 30/09 ✅ | Đã làm phần tháng 9 của đề cương: khảo sát, tiêu chí nguồn, hướng dẫn nhãn ban đầu, 20 ví dụ | Báo cáo tháng 9 (đã gửi) |
| Mốc 1 | 12/10 | CBHD xác nhận đề cương và tên đề tài; nộp lại theo lịch Khoa | Đề cương sửa |
| Mốc 2 | 31/10 | Xong bộ thử: khoảng 60 tuyên bố có nhãn, BM25, B0, hướng dẫn bản 2, quy mô đã chốt | Tóm tắt 1 trang |
| Mốc 3 | 27/11 | Dữ liệu và độ tin cậy nhãn xong; P và đối chứng chạy trên tập phát triển; cấu hình đã khóa; nhãn tập kiểm tra đã niêm phong | Tệp khóa cấu hình |
| Mốc 4 | 08/12 | Có kết quả tập kiểm tra, khoảng tin cậy, kiểm định, phân tích lỗi | Bảng kết quả chính |
| Mốc 5 | 13/12 | Tính năng chạy trên CopyPro | Video minh họa |
| Mốc 6 | 18/12 | Bản thảo khóa luận đầy đủ | Toàn văn |
| Mốc 7 | 31/12 | Nộp khóa luận, mã nguồn, dữ liệu | Bản cuối |
| Mốc 8 | 01/2027 | Bảo vệ | Slide |

### 3.2 Bảng tuyến tính

Ký hiệu: ⬜ chưa làm, 🔄 đang làm, ✅ xong. Cột "Giờ" là ước lượng công sức của sinh viên.

| Bước | Việc | Ngày | Đầu ra chính | Xong khi | Giờ |
|---|---|---|---|---|---|
| **Giai đoạn 1 – Chốt đề tài** | | | | | |
| ⬜ 01 | Đối chiếu lại đề cương với bài gốc | 09–10/10 | Ghi chú trích dẫn trong `luan_van/ghi_chu_tai_lieu.md` | Mỗi câu nói về bài khác trong đề cương có số trang trong bài gốc | 3 |
| ⬜ 02 | Gửi đề cương cho CBHD, chốt tên, nộp lại | 10–12/10 | Đề cương bản chốt | CBHD đồng ý; tên trên hệ thống đăng ký trùng từng ký tự với đề cương → **Mốc 1** | 2 |
| ⬜ 03 | Dọn repo, tạo thư mục và môi trường Python | 10–12/10 | `data/ src/ tests/ ket_qua/ luan_van/`, `requirements.txt` | `pytest` chạy được; khóa API cũ đã thu hồi | 3 |
| **Giai đoạn 2 – Nguồn bằng chứng và quy chuẩn nhãn** | | | | | |
| ⬜ 04 | Chọn 12 mẫu, chia trước tập phát triển và tập kiểm tra | 13–14/10 | `data/mau_san_pham.csv` | Đủ 3 nhóm, ≥3 hãng; mỗi mẫu có trang VN chính hãng ghi điều kiện | 3 |
| ⬜ 05 | Chụp trang thông số chính hãng | 14–16/10 | `data/nguon/<ma_mau>/` (html, txt, png, meta.json) | 12/12 mẫu đủ 4 tệp, có mã băm SHA-256 và ngày truy cập | 6 |
| ⬜ 06 | Chia tài liệu thành đoạn, giữ thông số cùng điều kiện và chú thích | 16–17/10 | `doan.jsonl` mỗi mẫu | Kiểm 20 đoạn ngẫu nhiên, không đoạn nào tách con số khỏi chú thích điều kiện | 5 |
| ⬜ 07 | Tệp cấu hình thuộc tính có điều kiện, chỉ dựa trên trang của tập phát triển | 17–18/10 | `data/cau_hinh/{dien_thoai,tai_nghe,dong_ho}.yaml` | Mọi thuộc tính trong 6 nhóm thông số có điều kiện bắt buộc, cách hiểu thông thường, hướng thuận lợi, cách diễn đạt | 4 |
| ⬜ 08 | Hướng dẫn gán nhãn bản 1, khảo sát nhanh cách hiểu của người đọc | 18–21/10 | `data/huong_dan_gan_nhan.md`, `ket_qua/khao_sat_cach_hieu.md` | Có cây quyết định, quy tắc, ≥24 ví dụ chỉ từ mẫu tập phát triển; khảo sát 5–10 người | 9 |
| **Giai đoạn 3 – Bộ thử ban đầu** | | | | | |
| ⬜ 09 | Script sinh quảng cáo theo đúng câu lệnh của CopyPro | 20–22/10 | `src/kiemchung/sinh_quang_cao.py` | Kiểm thử: câu lệnh trùng từng ký tự với `buildPrompt()` của CopyPro | 6 |
| ⬜ 10 | Sinh quảng cáo cho 2 mẫu thử | 22/10 | `data/quang_cao/*.json` (24 lần gọi) | Mỗi tệp có câu lệnh, mô hình, tham số, đầu ra, thời điểm | 2 |
| ⬜ 11 | Tách và lọc tuyên bố bộ thử (thủ công, có LLM hỗ trợ) | 23/10 | `data/tuyen_bo/thu.jsonl` (khoảng 60) | Mỗi tuyên bố giữ đủ ngữ cảnh; thuộc tính nằm trong tệp cấu hình | 4 |
| ⬜ 12 | Gán nhãn bộ thử, bấm giờ | 24–25/10 | `data/nhan/thu.jsonl` | 100% có nhãn, đoạn bằng chứng, lý do, số giây | 4 |
| ⬜ 13 | Mô-đun BM25, đo Recall@k | 24–26/10 | `src/kiemchung/truy_hoi.py` | Có Recall@{1,3,5,8} trên bộ thử và kiểm thử | 6 |
| ⬜ 14 | Cài đặt B0, chạy trên bộ thử | 27–28/10 | `doi_chung/b0.py` | Chạy hết bộ thử, có bộ nhớ đệm | 5 |
| ⬜ 15 | Phân tích lỗi bộ thử, hướng dẫn bản 2, chốt quy mô | 29–31/10 | `ket_qua/bo_thu/bao_cao.md` | Có số phút mỗi tuyên bố, phân bố nhãn, số tuyên bố mỗi quảng cáo, quy mô chốt → **Mốc 2** | 4 |
| ⬜ 16 | Viết nháp Chương 1 và 2 (đọc kỹ tài liệu) | 27/10–08/11 | `luan_van/chuong1.md`, `chuong2.md` | Đủ mục theo 11.1; mọi tài liệu được trích dẫn đúng trang | 14 |
| **Giai đoạn 4 – Dữ liệu chính** | | | | | |
| ⬜ 17 | Sinh quảng cáo cho 10 mẫu còn lại | 02–03/11 | `data/quang_cao/*.json` (thêm 120 lần gọi) | Đủ tổ hợp mẫu × LLM × loại bài × chế độ | 4 |
| ⬜ 18 | Tách, lọc và lấy mẫu tuyên bố chính | 03–05/11 | `data/tuyen_bo/chinh.jsonl` | Cùng bộ thử đạt 250–300 tuyên bố, phân tầng theo nhóm, LLM, chế độ | 6 |
| ⬜ 19 | Gán nhãn chính lần 1: tập phát triển trước (xong 08/11), tập kiểm tra sau (09–13/11) | 05–13/11 | `data/nhan/chinh.jsonl` | 100% có nhãn, bằng chứng, lý do, thời gian | 15 |
| ⬜ 20 | Tạo tập cặp tối thiểu | 13–15/11 | `data/cap_toi_thieu.jsonl` | 100–120 biến thể; mỗi loại ≥15, riêng loại đổi phiên bản tùy dữ liệu | 6 |
| ⬜ 21 | Chốt chia tập (chưa niêm phong) | 15/11 | `data/chia_tap.json` | Commit; từ đây phát triển chỉ dùng tập phát triển | 1 |
| **Giai đoạn 5 – Phương pháp P và đối chứng** | | | | | |
| ⬜ 22 | Chuẩn hóa giá trị, đơn vị, kiểu giá trị | 09–10/11 | `src/kiemchung/chuan_hoa.py` | ≥20 kiểm thử đạt | 6 |
| ⬜ 23 | Trích xuất có neo nguồn, kiểm tra đầy đủ | 10–17/11 | `trich_xuat.py`, `neo_nguon.py` | Kiểm thử neo nguồn đạt; chạy hết tập phát triển; có số trường bị loại và số điều kiện được bổ sung | 14 |
| ⬜ 24 | Tách và lọc tuyên bố tự động (cho CopyPro) | 16–18/11 | `src/kiemchung/tach_tuyen_bo.py` | Có Precision và Recall so với tuyên bố tách thủ công trên tập phát triển | 6 |
| ⬜ 25 | Cài đặt B2 và B3 | 17–19/11 | `doi_chung/b2.py`, `b3.py` | Chạy hết tập phát triển; ánh xạ nhãn B3 đã kiểm | 6 |
| ⬜ 26 | Bộ quyết định A–D, sinh lý do, kiểm thử | 18–22/11 | `quyet_dinh.py`, `tests/test_quyet_dinh.py` | ≥30 kiểm thử đạt, gồm mọi ví dụ trong hướng dẫn | 14 |
| ⬜ 27 | Ghép P, cài đặt B1, đo độ đúng trích xuất trên tập phát triển | 21–24/11 | `p.py`, `doi_chung/b1.py`, bảng độ đúng trích xuất | P, B1 chạy hết tập phát triển; độ đúng từng trường đo trên 50 tuyên bố | 8 |
| ⬜ 28 | Bản bỏ thành phần P−ĐK, P−NN | 24/11 | Cờ cấu hình trong `p.py` | Hai bản chạy hết tập phát triển | 3 |
| ⬜ 29 | Gán lại mù 20% số tuyên bố, người gán thứ hai, tính kappa | 23–25/11 | `ket_qua/do_tin_cay_nhan.md` | Có kappa trong-người và giữa-hai-người (hoặc ghi rõ không có người thứ hai); mọi sửa nhãn có ghi chép | 8 |
| ⬜ 30 | Viết nháp Chương 3 (phương pháp) | 24/11–10/12 | `luan_van/chuong3.md` | Có định nghĩa, biểu diễn, thuật toán, ví dụ xuyên suốt, hình quy trình | 12 |
| ⬜ 31 | Chọn cấu hình trên tập phát triển, khóa, niêm phong nhãn tập kiểm tra | 26–27/11 | `ket_qua/khoa_cau_hinh.md`, tag `khoa-cau-hinh` | Tag và mã băm nhãn tập kiểm tra được đẩy lên trước lần chạy tập kiểm tra đầu tiên → **Mốc 3** | 6 |
| ⬜ 32 | Dịch vụ kiểm chứng FastAPI (tách tự động + P), bắt đầu tích hợp CopyPro | 28–30/11 | `src/kiemchung/api.py`, `Dockerfile` | `POST /kiem-chung` cho 3 quảng cáo mẫu trả kết quả trùng việc chạy tách tự động rồi `p.py` | 8 |
| **Giai đoạn 6 – Thực nghiệm cuối và tích hợp song song** | | | | | |
| ⬜ 33 | Chạy tập kiểm tra một lần: 7 hệ thống và chạy đầu–cuối | 01–02/12 | `ket_qua/kiem_tra/*.jsonl`, `manifest.json` | Đủ đầu ra; manifest có tag khóa và mã băm cấu hình | 5 |
| ⬜ 34 | Backend CopyPro: tuyến API, dịch vụ gọi, lưu kết quả | 02–04/12 | Nhánh `kiem-chung-thong-so` trong repo CopyPro | Gọi API trả kết quả và lưu vào `Content` | 6 |
| ⬜ 35 | Tính chỉ số, khoảng tin cậy, kiểm định | 02–05/12 | `danh_gia.py`, bảng và hình | Đủ bảng 1–11 ở mục 8.7 | 8 |
| ⬜ 36 | Phân tích lỗi; đo độ đúng trích xuất trên 30 tuyên bố tập kiểm tra | 05–08/12 | `ket_qua/phan_tich_loi.md` | Mọi lỗi của P (tối đa 60) được xếp nguồn gốc; có 3–5 trường hợp điển hình | 9 |
| ⬜ 37 | Trả lời giả thuyết, phân tích phụ | 08/12 | Mục "Thảo luận" Chương 4 | Mỗi giả thuyết có kết luận đạt hoặc không đạt kèm số liệu → **Mốc 4** | 3 |
| ⬜ 38 | Giao diện CopyPro: bảng kết quả kiểm chứng | 08–12/12 | Thành phần giao diện mới | Người dùng chọn mẫu, bấm kiểm chứng, xem nhãn, đoạn nguồn, lý do | 10 |
| ⬜ 39 | Kiểm tra tích hợp, đo thời gian, quay video | 12–13/12 | Ảnh chụp, video 2–3 phút, bảng thời gian | Chạy được trên 10 quảng cáo tập kiểm tra → **Mốc 5** | 4 |
| **Giai đoạn 7 – Viết và nộp** | | | | | |
| ⬜ 40 | Viết Chương 4 (dữ liệu và thực nghiệm) | 08–17/12 | `luan_van/chuong4.md` | Đủ bảng và hình mục 8.7; có thảo luận và mối đe dọa đến tính hợp lệ | 16 |
| ⬜ 41 | Viết Chương 5 (tích hợp) và Chương 6 (kết luận) | 13–18/12 | `chuong5.md`, `chuong6.md` | Có kiến trúc, API, giao diện, thời gian, kết luận, hướng phát triển | 10 |
| ⬜ 42 | Gửi bản thảo đầy đủ cho CBHD (18/12), sửa theo góp ý (19–26/12) | 18–26/12 | Khóa luận bản sửa | Mọi góp ý có trạng thái đã sửa hoặc lý do → **Mốc 6** | 14 |
| ⬜ 43 | Gói tái lập: README, script chạy lại, thẻ dữ liệu | 21–27/12 | `README.md`, `scripts/chay_lai.sh`, `data/THE_DU_LIEU.md` | Một máy sạch chạy lại ra đúng bảng kết quả chính | 6 |
| ⬜ 44 | Kiểm tra cuối và nộp | 27–31/12 | Khóa luận PDF, mã nguồn, dữ liệu, tag `v1.0` | Đạt danh sách Phụ lục B → **Mốc 7** | 6 |
| **Giai đoạn 8 – Bảo vệ** | | | | | |
| ⬜ 45 | Slide, video dự phòng, tập dượt, câu hỏi phản biện | Theo lịch Khoa | Slide 15–20 trang, video | Tập dượt 3 lần đúng giờ; trả lời được mục 13 → **Mốc 8** | 15 |

**Tổng:** khoảng 300 giờ cho bước 01–44, từ 09/10 đến 31/12, trung bình khoảng 25 giờ/tuần. Thêm khoảng 15 giờ chuẩn bị bảo vệ.

### 3.3 Công sức theo tuần

| Tuần | Ngày | Bước chính | Giờ |
|---|---|---|---|
| 4 | 09–12/10 | 01–03 | 8 |
| 5 | 13–19/10 | 04–08 | 23 |
| 6 | 20–26/10 | 08–13 | 26 |
| 7 | 27/10–02/11 | 14–17 | 18 |
| 8 | 03–09/11 | 16–19, 22 | 28 |
| 9 | 10–16/11 | 19–24 | 29 |
| 10 | 17–23/11 | 23–27, 29 | 32 |
| 11 | 24–30/11 | 27–32 | 31 |
| 12 | 01–07/12 | 30, 33–36 | 32 |
| 13 | 08–14/12 | 30, 36–40 | 31 |
| 14 | 15–21/12 | 40–42 | 19 |
| 15–16 | 22–31/12 | 42–44 | 23 |
| **Cộng** | | | **300** |

Tuần 10–13 là cao điểm, khoảng 31–32 giờ/tuần. Nếu chậm hơn bảng một ngày ở bất kỳ tuần nào, áp dụng ngay phương án rút gọn ở mục 12.2, không dồn việc sang tuần sau.

---

## 4. Mục tiêu 10 điểm: tiêu chí và tự chấm

### 4.1 Thang tự chấm tham khảo

Đây không phải thang chính thức của Khoa. Thang được dựng từ những gì hội đồng hay hỏi và từ nhận xét trong file xét đề cương. Dùng để tự kiểm tra trước mỗi mốc.

| # | Tiêu chí | Tối đa | Để đạt tối đa cần | Bước |
|---|---|---|---|---|
| T1 | Tính mới và đóng góp | 2,5 | Chỉ ra hạn chế cụ thể của bài đã công bố; cải tiến được kiểm chứng bằng thí nghiệm; nói được khác biệt với từng bài gần nhất | 01, 16, 26–28, 35 |
| T2 | Phương pháp đúng đắn | 2,0 | Bài toán, nhãn, biểu diễn, thuật toán định nghĩa chặt và nhất quán; có cơ chế xử lý điểm yếu (neo nguồn, kiểm tra đầy đủ) | 07, 08, 22–26 |
| T3 | Thực nghiệm đáng tin | 2,5 | Đối chứng mạnh và công bằng; phân tích thành phần; khóa trước tập kiểm tra; khoảng tin cậy; kiểm định có hiệu chỉnh; độ tin cậy nhãn; báo cả kết quả âm | 19–21, 29, 31, 33–37 |
| T4 | Sản phẩm ứng dụng | 1,0 | Tính năng chạy trên CopyPro; kết quả đầu–cuối; video; đo thời gian | 24, 32, 34, 38, 39 |
| T5 | Khóa luận | 1,0 | Đúng mẫu Khoa; mạch lạc; đủ trích dẫn; bảng và hình rõ; không lỗi chính tả | 16, 30, 40–44 |
| T6 | Bảo vệ | 1,0 | Đúng giờ; trả lời thẳng; demo chạy được | 45 |

### 4.2 Điều kiện cần để chạm mức cao nhất

1. **Dữ liệu thật và độ tin cậy nhãn.** Có kappa giữa hai người; khảo sát cách hiểu của người đọc; không chỉ một người tự gán rồi tự đánh giá.
2. **Đối chứng không phải "bù nhìn".**
   - B1 dùng đúng bộ thông số và cùng hướng dẫn gán nhãn với P.
   - B2 có đầy đủ hướng dẫn và ví dụ.
   - B3 là mô hình tiếng Việt đã công bố.
   - Tất cả dùng cùng bằng chứng, cùng LLM.
3. **Phân tích thành phần** (P−ĐK, P−NN) để chứng minh lợi ích đến từ đâu.
4. **Khóa cấu hình và niêm phong nhãn trước khi chạy tập kiểm tra**, có tag git làm bằng chứng. Tập kiểm tra chỉ chạy một lần.
5. **Thống kê đúng:**
   - bootstrap theo cụm quảng cáo;
   - McNemar có hiệu chỉnh Holm;
   - kiểm tra "không kém hơn" cho Recall Đúng;
   - bảng theo hãng và theo loại chỉ là mô tả.
6. **Trung thực:** nếu P không đạt giả thuyết vẫn báo và giải thích bằng phân tích lỗi.
7. **Demo chạy được** trên CopyPro, có video dự phòng, có kết quả đầu–cuối.
8. **Tái lập được:** một lệnh chạy lại ra bảng kết quả chính.
9. **Điểm cộng nếu CBHD đồng ý:** viết bài báo ngắn từ kết quả sau khi nộp khóa luận.

### 4.3 Lỗi làm mất điểm thường gặp (rút từ file xét đề cương của Khoa)

| Lỗi | Cách tránh |
|---|---|
| Tên tiếng Việt, tiếng Anh và tên trên hệ thống không khớp; viết hoa sai trong tên tiếng Anh | Bước 02: so từng ký tự; tên tiếng Anh viết hoa chữ đầu câu, trừ tên riêng |
| Dùng từ tiếng Anh khi có từ tiếng Việt tương đương | Dùng thuật ngữ tiếng Việt, ghi tiếng Anh trong ngoặc ở lần đầu |
| Tài liệu tham khảo không được trích dẫn, hoặc trích dẫn sai nội dung bài gốc | Bước 01 và 16 ghi số trang; Phụ lục B kiểm lại |
| Số nội dung không tương ứng số mục tiêu | Giữ M1–M4 ↔ Nội dung 1–4 ↔ Chương 3–5 |
| Thiếu dữ liệu, đối chứng, độ đo cụ thể | Mục 8 ghi rõ từng thứ |
| Hình kiến trúc do AI vẽ, mũi tên xiên | Vẽ bằng matplotlib, draw.io hoặc TikZ; mũi tên thẳng |
| Định dạng gạch đầu dòng, in đậm, in nghiêng không thống nhất | Dùng mẫu Word của Khoa; kiểm ở bước 44 |
| Đặt "..." trong văn bản khoa học | Không dùng |
| Phạm vi không khớp tên đề tài | Phạm vi trong đề cương nêu tiêu chí chọn nhóm sản phẩm; khóa luận giữ nguyên |
| Biến, tham số, công thức dùng mà chưa định nghĩa | Mọi ký hiệu (q, s, D(s), c, y(c), e(c), r(c), k, FAR) được định nghĩa ở lần xuất hiện đầu |
| Ghi sai nội dung bài được trích (Khoa có đọc bài gốc, ví dụ ghi bài báo có "research gap" trong khi bài chỉ có "research question") | Mỗi câu nói về bài khác phải khớp số trang trong bài gốc (bước 01) |
| Trích dẫn lệch: nhiều tài liệu cho phần độ đo, ít cho công trình liên quan; hoặc quá nhiều tài liệu | Phần lớn tài liệu dùng cho tổng quan và so sánh; giữ khoảng 25 tài liệu, tài liệu nào cũng có vai trò |
| Gộp nhiều kỹ thuật, nhiều thành phần cho một khóa luận | Một câu hỏi trung tâm (đối chiếu điều kiện); CopyPro là nơi triển khai, không phải bài toán thứ hai |
| Viết hoa không cần thiết trong nội dung | Chỉ viết hoa tên riêng; tên chế độ của hãng viết thường (ví dụ "chế độ nguồn điện thấp") |
| Đoạn đầu tổng quan trộn ngữ cảnh với nghiên cứu hiện có | Tách đoạn: bối cảnh, CopyPro, các nghiên cứu liên quan, hạn chế |

### 4.4 Bài học từ 38 đề cương được đánh giá Đạt (đọc ngày 10/10/2026)

**Số liệu từ file xét đề cương.** Mỗi đề cương nhóm hai người chiếm hai dòng, nên đếm theo dòng có tên đề tài:

| Danh sách | Số đề cương | Đạt | Tỷ lệ |
|---|---|---|---|
| NT505.R11 (lớp của mình) | 48 | 2 | 4% |
| NT505.R11.ANTT | 64 | 24 | 38% |
| NT505.R11.ANTN | 17 | 12 | 71% |

Hội đồng của lớp NT505.R11 yêu cầu sửa 46/48 đề cương, nên bị yêu cầu sửa là bình thường. Nhận xét cho 46 đề cương đó, đếm theo từ khóa nên chỉ là ước lượng, xoay quanh: hình thức (khoảng 20), tổng quan và trích dẫn (khoảng 16), tên đề tài (khoảng 15), thực nghiệm chưa cụ thể (khoảng 13), nội dung thực hiện chưa cụ thể hoặc chưa khớp mục tiêu (khoảng 9), định vị đóng góp so với cách sẵn có (4), phạm vi và trọng tâm (4), biến chưa định nghĩa (4). Nhận xét của đề tài này rơi vào ba nhóm nội dung nặng nhất: tổng quan, đóng góp, phạm vi.

**Điểm chung của hai đề cương Đạt ở NT505.R11 (23520008, 23520810):**

1. Tổng quan đi theo mạch: bối cảnh → từng nhóm nghiên cứu, mỗi ý có trích dẫn → hạn chế của nhóm đó → khoảng trống → hướng của đề tài. Không có câu nào nói về bài khác mà thiếu trích dẫn.
2. Có bảng so sánh các công trình liên quan, cột cuối là hạn chế so với đề tài (23520810).
3. Có câu hỏi nghiên cứu hoặc câu hỏi chính mà thực nghiệm phải trả lời (23520008).
4. Nêu rõ dữ liệu, đối chứng, độ đo, kịch bản thực nghiệm; có mục giới hạn của đề tài nói rõ phần nào không làm và vì sao.
5. Kế hoạch theo tuần, có các lần gặp cán bộ hướng dẫn.

**Điểm cộng thường gặp ở các đề cương Đạt khác (ANTT, ANTN):**

1. Mục "Tính mới và đóng góp" nói thẳng thành phần nào đã có trong nghiên cứu trước, điểm mới nằm ở đâu, và khác từng bài gần nhất thế nào (23520197).
2. Bảng các phương pháp được so sánh, ghi vai trò của từng cặp so sánh, tức cặp nào tách riêng đóng góp của thành phần nào (23520197).
3. LLM luôn đi kèm một bước kiểm chứng tất định: tên đề tài và phương pháp dùng các cụm "có kiểm chứng", "dựa trên bằng chứng", "xác minh có chọn lọc" (23520295, 23521179, 23521735, 23520315, 23521602). Hướng neo nguồn và bộ quyết định bằng quy tắc của đề tài này cùng mạch đó.
4. Tiêu chí thành công chốt trước khi chạy tập kiểm tra và cam kết báo cáo cả kết quả âm.
5. Khoảng trống nghiên cứu đánh số và mỗi khoảng trống gắn với một phần việc của đề tài (23521179, 23520295).

**Đã đưa vào đề cương (bản 10/10/2026, chữ đỏ):** Bảng 1 so sánh nghiên cứu liên quan; câu nói rõ thành phần nào đã có và điểm mới nằm ở đâu (mục 3); ví dụ bốn nhãn với Galaxy Buds3 Pro (mục 2); ba câu hỏi nghiên cứu CH1–CH3 (mục 2) và giả thuyết H1–H3 tương ứng (Nội dung 3); Bảng 2 các phương pháp được so sánh và vai trò; các mốc gặp cán bộ hướng dẫn trong kế hoạch; sửa "bộ pilot" thành "bộ dữ liệu thử ban đầu", viết thường tên chế độ của hãng.

**Không đổi:** kế hoạch vẫn theo tháng như khung đề cương đã nộp. Hội đồng không nhận xét về phần kế hoạch của đề tài này, và các mốc gặp cán bộ hướng dẫn đã được thêm vào từng tháng.

---

## 5. Quy ước dự án

### 5.1 Cấu trúc thư mục (tạo ở bước 03)

```
KLTN/
├── CHI_TIET_TUYEN_TINH_KHOA_LUAN.md       # file này
├── README.md
├── de_cuong/                              # đề cương bản sạch, bản chữ đỏ, PDF, mã dựng
├── báo/  dịch/  run_translate_batch.sh    # bài tham khảo và bản dịch để đọc
├── data/
│   ├── mau_san_pham.csv                   # 12 mẫu, nhóm, hãng, URL, tập
│   ├── nguon/<ma_mau>/                    # page.html, page.txt, full.png, meta.json, doan.jsonl
│   ├── cau_hinh/<nhom>.yaml               # thuộc tính có điều kiện, điều kiện bắt buộc
│   ├── huong_dan_gan_nhan.md
│   ├── quang_cao/<ma_qc>.json             # câu lệnh, mô hình, tham số, đầu ra
│   ├── tuyen_bo/{thu,chinh}.jsonl
│   ├── nhan/{thu,chinh,gan_lai,nguoi_2}.jsonl
│   ├── cap_toi_thieu.jsonl
│   └── chia_tap.json
├── src/kiemchung/                         # tach_tuyen_bo, truy_hoi, trich_xuat, neo_nguon, chuan_hoa, quyet_dinh, p, api, danh_gia
│   └── doi_chung/                         # b0, b1, b2, b3
├── tests/
├── ket_qua/                               # mỗi lần chạy một thư mục con + manifest.json
└── luan_van/                              # nháp chương, hình, bảng, nhật ký
```

Tên thư mục và tệp mã nguồn viết không dấu để tránh lỗi trên các hệ điều hành.

### 5.2 Mã định danh

| Đối tượng | Mẫu mã | Ví dụ |
|---|---|---|
| Mẫu sản phẩm | `<nhóm>-<hãng>-<tên>` | `tn-samsung-buds3pro`, `dt-apple-iphone17`, `dh-apple-watchse3` |
| Đoạn tài liệu | `<ma_mau>#<số>` | `tn-samsung-buds3pro#014` |
| Lần sinh quảng cáo | `qc-<ma_mau>-<llm>-<loai>-<che_do>-<lần>` | `qc-tn-samsung-buds3pro-gemini-social-ten-1` |
| Tuyên bố | `tb-<5 chữ số>` | `tb-00042` |
| Biến thể cặp tối thiểu | `ct-<số tb gốc>-<loại>` | `ct-00042-doi_bo_phan` |
| Lần chạy | `run-<ngày>-<hệ thống>-<tập>` | `run-20261201-P-test` |

### 5.3 Định dạng dữ liệu

Tuyên bố (`data/tuyen_bo/*.jsonl`):

```json
{"id": "tb-00042", "ma_qc": "qc-tn-samsung-buds3pro-gemini-social-ten-1", "ma_mau": "tn-samsung-buds3pro",
 "cau_goc": "Galaxy Buds3 Pro nghe nhạc liền 7 tiếng ngay cả khi bật chống ồn",
 "tuyen_bo": "Galaxy Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn",
 "thuoc_tinh": "thoi_luong_pin_nghe_nhac", "llm_sinh": "gemini-2.5-flash", "che_do": "ten", "loai_bai": "social"}
```

Nhãn (`data/nhan/*.jsonl`):

```json
{"id": "tb-00042", "nhan": "LECH", "loai": "doi_dieu_kien",
 "bang_chung": ["tn-samsung-buds3pro#014"], "trich": "Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7",
 "ly_do": "7 giờ chỉ đúng khi tắt ANC", "nguoi_gan": "phuoc", "luot": 1, "giay": 95, "tai_lieu_mau_thuan": false}
```

- **Mã nhãn:** `DUNG`, `SAI`, `LECH`, `CHUA_DU`.
- **Mã loại biến đổi** (dùng chung cho nhãn Lệch và cho tập cặp tối thiểu):
  - `bo_dieu_kien`
  - `doi_dieu_kien`
  - `doi_bo_phan`
  - `doi_phien_ban`
  - `doi_kieu_gia_tri`
  - `doi_gia_tri` (biến thể này cho nhãn Sai)

### 5.4 Quy tắc làm việc

1. **Nhật ký:** mỗi ngày ghi 3–5 dòng vào `luan_van/nhat_ky.md`: đã làm gì, số liệu gì, vướng gì, thay đổi gì.
2. **Commit nhỏ, thường xuyên.** Không commit khóa API; khóa nằm trong `.env`, tệp này đã có trong `.gitignore`.
3. **Bộ nhớ đệm LLM:** mọi lần gọi LLM được lưu theo mã băm của (mô hình, câu lệnh, tham số). Nhờ vậy chạy lại không tốn tiền và không đổi kết quả.
4. **Bảo vệ tập kiểm tra:**
   - Sau bước 21, mọi lựa chọn (câu lệnh, k, mô hình, ngưỡng sai số) chỉ dựa trên tập phát triển.
   - Nhãn tập kiểm tra chỉ được mở để gán lại mù ở bước 29.
   - Tệp cấu hình chỉ được sửa dựa trên tập phát triển; mỗi lần sửa ghi vào nhật ký.
5. **Dùng AI hỗ trợ:**
   - Được dùng để viết mã và sửa câu.
   - Không dùng AI để gán nhãn chuẩn, không dùng AI vẽ hình kiến trúc.
   - Luôn kiểm lại trích dẫn trên bài gốc.
6. **Sao lưu:** đẩy repo lên GitHub mỗi ngày làm việc. Ảnh chụp trang lưu thêm một bản trên Drive.

---

## 6. Hướng dẫn gán nhãn (khung cho bản 1 ở bước 08)

### 6.1 Tách tuyên bố

- Một tuyên bố chỉ chứa một thuộc tính và một giá trị. Câu "pin 6 giờ, sạc đầy trong 1 giờ" tách thành hai tuyên bố.
- Giữ ngữ cảnh: tên sản phẩm, phiên bản, bộ phận và điều kiện nằm ở câu trước hoặc câu sau phải được đưa vào tuyên bố.
- **Chỉ giữ tuyên bố có điều kiện ràng buộc,** tức tuyên bố có thuộc tính nằm trong tệp cấu hình của nhóm sản phẩm. Bỏ:
  - khối lượng, kích thước, phiên bản Bluetooth;
  - tuyên bố cảm tính;
  - giá và khuyến mãi.

### 6.2 Định nghĩa và thứ tự quyết định nhãn

**Hai khái niệm dùng chung:**

- **Khớp giá trị.** Giá trị của tuyên bố bằng giá trị công bố sau chuẩn hóa (sai số làm tròn cho phép là một ngưỡng, mặc định 1%, chọn ở bước 31). Giá trị **kém thuận lợi hơn** cũng được coi là khớp, ví dụ nêu thời lượng pin thấp hơn hay thời gian sạc lâu hơn, vì không gây hiểu nhầm có lợi cho người bán. Hướng thuận lợi của mỗi thuộc tính ghi trong tệp cấu hình. Mã phân loại như chuẩn IP phải bằng đúng.
- **Điều kiện của tuyên bố.** Gồm điều kiện được nêu rõ. Điều kiện bắt buộc nào không nêu thì dùng cách hiểu thông thường (6.3). Nếu điều kiện bắt buộc không nêu là một **chế độ người dùng tự chọn** (bật/tắt chống ồn, chế độ tiết kiệm pin, hoạt động sử dụng) thì ghi là "chế độ chưa xác định". Chế độ chưa xác định không được coi là cùng điều kiện với bất kỳ chế độ cụ thể nào; trường hợp này dùng quy tắc E1.

**Thứ tự quyết định** (dừng ở dòng đầu tiên thỏa):

| # | Điều kiện | Nhãn |
|---|---|---|
| A | Tài liệu không có thông số cùng sản phẩm và thuộc tính | Chưa đủ thông tin |
| C1 | Tuyên bố khẳng định chắc chắn ("luôn", "đảm bảo", "ít nhất", "mọi lúc") một mức mà tài liệu chỉ ghi là tối đa ("lên đến") | Lệch điều kiện (`doi_kieu_gia_tri`) |
| C2 | Có thông số cùng điều kiện và giá trị khớp. Với chế độ chưa xác định: giá trị khớp với giá trị kém thuận lợi nhất trong các chế độ được công bố (quy tắc E1) | Đúng |
| C3 | Giá trị của tuyên bố bằng giá trị được công bố ở một điều kiện khác (chế độ, bộ phận, phụ kiện, phiên bản hoặc điều kiện đo khác) | Lệch điều kiện |
| C4 | Có thông số cùng điều kiện (hoặc, với chế độ chưa xác định, ở chế độ bất kỳ) mà giá trị mâu thuẫn; hoặc giá trị thuận lợi hơn mọi giá trị được công bố | Sai |
| C5 | Còn lại: điều kiện mà tuyên bố nêu không được công bố, hoặc tài liệu mâu thuẫn | Chưa đủ thông tin |

**Quy tắc E1 (giá trị thận trọng)** chỉ áp dụng khi đủ bốn điều:

1. Tệp cấu hình bật `ngoai_le_than_trong` cho thuộc tính.
2. Điều kiện bị bỏ là chế độ người dùng tự chọn, không phải phụ kiện mua thêm hay bộ phận.
3. Tài liệu công bố ít nhất hai giá trị cho các chế độ khác nhau.
4. Kiểu giá trị của tuyên bố là "không nêu" hoặc "lên đến".

### 6.3 Cách hiểu thông thường khi tuyên bố không nêu điều kiện

Tuyên bố không nêu điều kiện được hiểu theo cách người mua thông thường hiểu: áp dụng chung, cho bộ phận chính, với phụ kiện có sẵn trong hộp và chế độ hiển thị thông thường. Cách hiểu cụ thể ghi trong tệp cấu hình (bước 07). Ở bước 08, khảo sát nhanh 5–10 người đọc với 8 tuyên bố không nêu điều kiện để kiểm tra cách hiểu này, và ghi kết quả vào khóa luận.

| Nhóm | Thuộc tính | Điều kiện bắt buộc | Cách hiểu khi không nêu | Chỉ ghi nhận (không đổi nhãn) |
|---|---|---|---|---|
| Điện thoại | Thời lượng pin | hoạt động (xem video, xem trực tuyến, nghe nhạc) | chế độ chưa xác định → E1 | kịch bản thử nghiệm của hãng |
| Điện thoại | Sạc nhanh | công suất bộ sạc; mốc % và thời gian | không mua thêm bộ sạc | loại cáp |
| Điện thoại | Độ sáng | chế độ (thông thường, HDR, ngoài trời, cực đại) | chế độ thông thường | phần diện tích đo, APL: dùng để giải thích vì sao là độ sáng đỉnh, ghi vào lý do |
| Điện thoại | Tần số quét | kiểu giá trị (tối đa, thích ứng) | mức tối đa như hãng công bố | dải tần số |
| Điện thoại | Zoom | quang học hay kỹ thuật số | quang học | ống kính |
| Điện thoại | Kháng nước | chuẩn IP, độ sâu, thời gian | chuẩn hãng công bố | loại nước |
| Điện thoại | Dung lượng pin | phiên bản | phiên bản được nêu trong tên | định mức hay điển hình |
| Tai nghe | Thời lượng pin | chế độ chống ồn; chỉ tai nghe hay kèm hộp sạc | chỉ tai nghe; chế độ chưa xác định → E1 | âm lượng, codec |
| Tai nghe | Sạc nhanh | số phút sạc, số giờ nghe | – | – |
| Tai nghe | Kháng nước | bộ phận (tai nghe hay hộp sạc), chuẩn IP | tai nghe | – |
| Tai nghe | Dung lượng pin | bộ phận | tai nghe | – |
| Đồng hồ | Thời lượng pin | chế độ (thường, tiết kiệm pin), kết nối (GPS hay di động) | chế độ chưa xác định → E1 | kịch bản thử nghiệm |
| Đồng hồ | Sạc nhanh | bộ sạc hoặc cáp, mốc % và thời gian | cáp đi kèm | – |
| Đồng hồ | Kháng nước | độ sâu hoặc chuẩn, hoạt động được phép | chuẩn hãng công bố | – |
| Đồng hồ | Độ sáng | chế độ | thông thường | – |

**Kiểu giá trị.** Không có từ chỉ kiểu giá trị thì hiểu là con số hãng công bố. Chỉ gán Lệch vì đổi kiểu giá trị theo dòng C1.

**Từ "tiêu chuẩn" hiểu theo thuộc tính.** Với độ sáng, "tiêu chuẩn" là chế độ thông thường. Với dung lượng pin, "tiêu chuẩn" là giá trị điển hình.

### 6.4 Ví dụ (chỉ lấy từ mẫu dự kiến thuộc tập phát triển)

Các con số đã đối chiếu với trang chính hãng tiếng Việt ngày 09/10/2026. Ở bước 05, kiểm lại từng con số trên bản chụp.

| # | Tuyên bố | Dòng | Nhãn | Lý do |
|---|---|---|---|---|
| 1 | iPhone 17 sạc nhanh lên đến 50% trong 20 phút với bộ sạc 40W trở lên | C2 | Đúng | Khớp cả giá trị và điều kiện bộ tiếp hợp 40W |
| 2 | iPhone 17 sạc 50% chỉ trong 20 phút | C3 | Lệch (`bo_dieu_kien`) | Hiểu là không mua thêm bộ sạc; 50%/20 phút chỉ đúng với bộ tiếp hợp 40W trở lên (bán riêng) |
| 3 | Màn hình iPhone 17 sáng 3000 nit | C3 | Lệch (`bo_dieu_kien`) | Hiểu là chế độ thông thường (1000 nit); 3000 nit là độ sáng đỉnh ngoài trời |
| 4 | Màn hình iPhone 17 sáng tối đa 1000 nit | C2 | Đúng | Khớp độ sáng tối đa ở chế độ thông thường |
| 5 | Màn hình iPhone 17 đạt 4000 nit ngoài trời | C4 | Sai | Cùng điều kiện ngoài trời, tài liệu ghi 3000 nit; 4000 thuận lợi hơn mọi giá trị |
| 6 | Galaxy Buds3 Pro nghe nhạc 6 giờ khi bật chống ồn | C2 | Đúng | Khớp |
| 7 | Galaxy Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn | C3 | Lệch (`doi_dieu_kien`) | 7 giờ là khi tắt ANC |
| 8 | Galaxy Buds3 Pro pin 7 giờ | C3 | Lệch (`bo_dieu_kien`) | Chế độ chưa xác định; E1 chỉ cho Đúng khi ≤ 6 giờ; 7 giờ là khi tắt ANC |
| 9 | Galaxy Buds3 Pro nghe nhạc đến 6 giờ | C2 (E1) | Đúng | Bằng giá trị kém thuận lợi nhất trong hai chế độ |
| 10 | Galaxy Buds3 Pro pin 8 giờ | C4 | Sai | Thuận lợi hơn mọi giá trị công bố (6 và 7 giờ) |
| 11 | Hộp sạc Galaxy Buds3 Pro cũng chống nước IP57 | C3 | Lệch (`doi_bo_phan`) | IP57 là của tai nghe; hộp sạc không kháng nước |
| 12 | Galaxy Buds3 Pro luôn nghe đủ 6 giờ | C1 | Lệch (`doi_kieu_gia_tri`) | Tài liệu ghi "lên đến 6 giờ" |
| 13 | Apple Watch SE 3 dùng đến 32 giờ ở chế độ nguồn điện thấp | C2 | Đúng | Khớp |
| 14 | Apple Watch SE 3 pin 32 giờ | C3 | Lệch (`bo_dieu_kien`) | Chế độ chưa xác định; 32 giờ chỉ ở chế độ nguồn điện thấp |
| 15 | Apple Watch SE 3 luôn dùng đủ 18 giờ mỗi ngày | C1 | Lệch (`doi_kieu_gia_tri`) | Tài liệu ghi "lên đến 18 giờ" |
| 16 | Xiaomi 15T có độ sáng cực đại 3200 nit | C2 | Đúng | Cùng chế độ cực đại; phần 25% diện tích chỉ ghi vào lý do |
| 17 | Màn hình Xiaomi 15T sáng 3200 nit | C3 | Lệch (`bo_dieu_kien`) | Không nói "cực đại" nên hiểu là chế độ thông thường; 3200 nit là độ sáng cực đại đo trên 25% diện tích |
| 18 | Galaxy Buds3 Pro nghe 5 giờ ở chế độ xuyên âm | C5 | Chưa đủ thông tin* | *Nếu trang không công bố chế độ xuyên âm |

### 6.5 Bằng chứng, lý do, tài liệu mâu thuẫn

- Ghi mã đoạn và câu trích nguyên văn. Lý do viết một câu, nêu rõ điều kiện nào bị bỏ hoặc bị đổi.
- **Tài liệu mâu thuẫn hoặc ghi nhầm** (cùng một thông số ghi khác nhau ở hai chỗ):
  - gán Chưa đủ thông tin;
  - đặt `tai_lieu_mau_thuan = true`;
  - thống kê riêng.
- Lần kiểm tra ngày 09/10/2026 phát hiện hai trang cần kiểm lại trên bản chụp ở bước 05:
  - trang Galaxy Buds3 Pro có chỗ chú thích chế độ ANC cho tổng thời gian kèm hộp sạc có vẻ không nhất quán;
  - trang OPPO Find X8 ghi giá trị "định mức" lớn hơn giá trị "tiêu chuẩn".
- Ví dụ trong hướng dẫn chỉ lấy từ mẫu tập phát triển. Ví dụ tai nghe soạn tháng 9 nào dùng mẫu thuộc tập kiểm tra thì thay bằng ví dụ mới.

---

## 7. Đặc tả phương pháp P

### 7.1 Bộ thông số

```json
{
  "san_pham": "Galaxy Buds3 Pro", "phien_ban": null,
  "thuoc_tinh": "thoi_luong_pin_nghe_nhac", "gia_tri": 7, "don_vi": "gio",
  "dieu_kien": {"che_do_chong_on": "anc_bat", "bo_phan": "tai_nghe"},
  "kieu_gia_tri": "khong_neu",
  "trich": {"gia_tri": "7 tiếng", "che_do_chong_on": "ngay cả khi bật chống ồn", "bo_phan": null}
}
```

Bộ phận và phiên bản nằm trong `dieu_kien` vì chúng được đối chiếu ở bước B của bộ quyết định, không dùng để lọc ở bước A.

### 7.2 Truy hồi BM25

- Chỉ tìm trong `doan.jsonl` của mẫu người dùng chọn.
- Thử hai cách tách từ trên tập phát triển: theo âm tiết, và theo từ bằng `pyvi` hoặc `underthesea`. Chọn cách có Recall@5 cao hơn.
- k ∈ {3, 5, 8}, chọn ở bước 31.

### 7.3 Trích xuất có neo nguồn và kiểm tra đầy đủ

1. LLM nhận tuyên bố và top-k đoạn, trả JSON theo lược đồ 7.1 cho tuyên bố và cho từng thông số ứng viên trong bằng chứng. Mỗi trường có câu trích.
2. **Kiểm tra neo nguồn** (Python, tất định):
   - (a) câu trích là chuỗi con của văn bản nguồn, sau khi chuẩn hóa khoảng trắng và dấu câu;
   - (b) giá trị nằm trong câu trích của nó:
     - giá trị số: con số xuất hiện trong câu trích;
     - mã như IP57: mã xuất hiện;
     - giá trị phủ định như "không kháng nước": cụm phủ định xuất hiện;
   - (c) cách diễn đạt của điều kiện xuất hiện trong câu trích của điều kiện.
   - Trường không đạt bị đặt `null` và ghi vào `bi_loai`.
3. **Kiểm tra đầy đủ:** với mỗi điều kiện bắt buộc của thuộc tính, tìm các cách diễn đạt trong tệp cấu hình (ví dụ "bật ANC", "bật chống ồn", "khử tiếng ồn chủ động") trong văn bản của tuyên bố hoặc của đoạn nguồn.
   - Nếu văn bản có cách diễn đạt mà trường đang `null` thì điền theo cách diễn đạt đó và ghi vào `bo_sung`.
   - Nếu tìm thấy nhiều cách diễn đạt mâu thuẫn, kết luận Chưa đủ thông tin.
4. Ghi số trường bị loại và số trường được bổ sung cho từng tuyên bố. Đây là số liệu cho Chương 4.

### 7.4 Chuẩn hóa

- **Đơn vị:**
  - giờ/tiếng/h;
  - phút/min;
  - nit/nits/cd/m²;
  - W, mAh, Hz;
  - chuẩn IP (tách bụi/nước: IP57 → bụi 5, nước 7);
  - zoom (x);
  - số có dấu chấm ngăn cách hàng nghìn ("3.000 nit" = 3000).
- **Kiểu giá trị:**
  - {lên đến, tối đa, up to} → `toi_da`;
  - {điển hình, typical} → `dien_hinh`;
  - {định mức, rated} → `dinh_muc`;
  - {luôn, đảm bảo, ít nhất, mọi lúc} → `khang_dinh`;
  - không có → `khong_neu`.
  - "Tiêu chuẩn" hiểu theo thuộc tính (6.3).
- **Tên sản phẩm và phiên bản:** dùng bảng bí danh trong tệp cấu hình.

### 7.5 Bộ quyết định (mã giả, cùng thứ tự với 6.2)

```python
def quyet_dinh(tb, ung_vien, cau_hinh):
    # A. cùng sản phẩm và thuộc tính (bộ phận, phiên bản KHÔNG lọc ở đây)
    cung_tt = [u for u in ung_vien if u.san_pham == tb.san_pham and u.thuoc_tinh == tb.thuoc_tinh]
    if not cung_tt:
        return CHUA_DU, vet("không có thông số cùng thuộc tính")

    # B. điều kiện của tuyên bố: điều kiện nêu + cách hiểu thông thường; đánh dấu chế độ chưa xác định
    dk = dieu_kien_tuyen_bo(tb, cau_hinh)
    # chỉ so điều kiện bắt buộc; "chế độ chưa xác định" không khớp chế độ cụ thể nào (xử lý bằng E1)
    cung_dk = [u for u in cung_tt if khop_dieu_kien(dk, u.dieu_kien, cau_hinh)]
    khac_dk = [u for u in cung_tt if u not in cung_dk]

    # C1. đổi kiểu giá trị
    for u in cung_tt:
        if tb.kieu_gia_tri == "khang_dinh" and u.kieu_gia_tri == "toi_da" and bang(tb, u):
            return LECH, vet("doi_kieu_gia_tri", u)

    # C2. đúng (kể cả E1)
    if dk.che_do_chua_xac_dinh and ap_dung_E1(tb, cung_tt, cau_hinh):
        u = kem_thuan_loi_nhat(cung_tt, cau_hinh)
        if khop_gia_tri(tb, u, cau_hinh):
            return DUNG, vet("E1", u)
    for u in cung_dk:
        if khop_gia_tri(tb, u, cau_hinh):          # bằng, hoặc kém thuận lợi hơn; mã phải bằng
            return DUNG, vet("khop", u)

    # C3. trùng giá trị ở điều kiện khác
    for u in khac_dk:
        if bang(tb, u):
            return LECH, vet(loai_bien_doi(dk, u.dieu_kien), u)

    # C4. sai
    so_sanh = cung_tt if dk.che_do_chua_xac_dinh else cung_dk
    if so_sanh or thuan_loi_hon_moi_gia_tri(tb, cung_tt, cau_hinh):
        return SAI, vet("mau_thuan", so_sanh[:1] or cung_tt[:1])

    # C5. còn lại
    return CHUA_DU, vet("không có thông số ở điều kiện của tuyên bố")
```

- **P−ĐK:** bỏ bước B; mọi ứng viên cùng thuộc tính được coi là cùng điều kiện, nên không bao giờ ra nhãn Lệch từ dòng C3.
- **P−NN:** bỏ bước 2 và bước 3 của mục 7.3.

### 7.6 Sinh lý do

Lý do được ghép từ `vet` theo mẫu câu cố định, ví dụ: "Giá trị {gia_tri} {don_vi} chỉ đúng khi {dieu_kien_tai_lieu}; tuyên bố ghi {dieu_kien_tb}. Nguồn: “{trich}”." Không để LLM viết lý do tự do, để lý do luôn khớp với nhãn.

### 7.7 Tệp cấu hình (ví dụ `data/cau_hinh/tai_nghe.yaml`)

```yaml
nhom: tai_nghe
thuoc_tinh:
  thoi_luong_pin_nghe_nhac:
    don_vi: gio
    huong_thuan_loi: cao_hon_tot_hon
    dieu_kien_bat_buoc: [che_do_chong_on, bo_phan]
    che_do_nguoi_dung_chon: [che_do_chong_on]   # được dùng cho E1
    hieu_thong_thuong: {bo_phan: tai_nghe}
    ngoai_le_than_trong: true
    chi_ghi_nhan: [am_luong, codec]
  khang_nuoc:
    dieu_kien_bat_buoc: [bo_phan]
    hieu_thong_thuong: {bo_phan: tai_nghe}
    so_khop: ma_bang_nhau                        # IP57 phải bằng IP57
cach_dien_dat:
  che_do_chong_on:
    anc_bat: ["bật ANC", "bật chống ồn", "khử tiếng ồn chủ động"]
    anc_tat: ["tắt ANC", "tắt chống ồn"]
  bo_phan:
    hop_sac: ["hộp sạc", "hộp sạc đi kèm"]
```

Tệp cấu hình viết từ trang của tập phát triển và hiểu biết chung về nhóm sản phẩm. Tệp đóng băng cùng lúc khóa cấu hình ở bước 31.

### 7.8 Kiểm thử (bước 26)

- Mỗi dòng A, C1–C5 và quy tắc E1 có ít nhất 3 kiểm thử: khớp, không khớp, trường hợp biên.
- Toàn bộ 18 ví dụ ở 6.4 thành kiểm thử hồi quy.
- Có kiểm thử cho neo nguồn và kiểm tra đầy đủ: câu trích không có trong nguồn, số sai, điều kiện bịa, điều kiện bị bỏ sót.

---

## 8. Đối chứng và thực nghiệm

### 8.1 Các hệ thống

| Ký hiệu | Đầu vào | Quyết định nhãn | Số nhãn | Ghi chú |
|---|---|---|---|---|
| B0 | Tuyên bố + top-k đoạn | LLM | 3 (Supported, Refuted, NEI) | Đại diện kiểm chứng ba nhãn phổ biến; định nghĩa ba nhãn theo FEVER |
| B1 | Bộ thông số đã trích của tuyên bố và bằng chứng (giống P) + hướng dẫn gán nhãn 6.2–6.3 + tóm tắt tệp cấu hình | LLM | 4 | Tách riêng tác động của bộ quyết định tường minh |
| B2 | Tuyên bố + top-k đoạn + hướng dẫn 6.2–6.3 + 4 ví dụ từ tập phát triển | LLM | 4 | Khắc phục chỉ bằng câu lệnh, kiểu AVeriTeC |
| B3 | Cặp (tuyên bố, nối top-k đoạn) | SemViQA-TC | 3 | Xem cách chạy bên dưới |
| P | Mục 7 | Quy tắc A–D | 4 | |
| P−ĐK | P bỏ đối chiếu điều kiện | Quy tắc | 4 | |
| P−NN | P bỏ neo nguồn và kiểm tra đầy đủ | Quy tắc | 4 | |

**Cách chạy B3:**

- Checkpoint `SemViQA/tc-xlmr-isedsc01` hoặc `tc-xlmr-viwikifc`: giấy phép MIT, XLM-R large, chọn trên tập phát triển.
- Gói `semviqa`. Thứ tự nhãn của mô hình là NEI, SUPPORTED, REFUTED.
- Độ dài tối đa 256 token, chỉ cắt phần bằng chứng.
- Mô hình được huấn luyện trên tin tức (ngoài miền).

**Ánh xạ nhãn của hệ thống 3 nhãn:**

- Supported → Đúng;
- Refuted → Sai;
- NEI → Chưa đủ thông tin.

B0 và B3 không bao giờ dự đoán Lệch. Vì vậy:

- so sánh chính với hai hệ thống này là FAR;
- F1 Lệch của chúng bằng 0 theo cấu trúc, ghi rõ trong bảng;
- giả thuyết về F1 Lệch chỉ so với B1 và B2.

### 8.2 Quy tắc công bằng

1. Cùng tuyên bố, cùng top-k đoạn, cùng LLM (chọn ở bước 31, mặc định Gemini 2.5 Flash, nhiệt độ 0), cùng bộ nhớ đệm.
2. Câu lệnh của B0–B2 được tinh chỉnh trên tập phát triển với số lần thử bằng số lần thử dành cho câu lệnh trích xuất của P. Ghi số lần thử vào nhật ký.
3. Không dùng ví dụ thuộc tập kiểm tra trong bất kỳ câu lệnh nào.
4. Vì Gemini vừa sinh một nửa số quảng cáo vừa kiểm chứng, mọi bảng chính đều báo thêm kết quả tách theo LLM sinh quảng cáo.

### 8.3 Chia tập, khóa và niêm phong

- **Chia theo mẫu sản phẩm:**
  - tập phát triển: 2 mẫu thử và khoảng 2 mẫu nữa, đủ 3 nhóm;
  - tập kiểm tra: 8 mẫu còn lại, nhóm nào và hãng nào cũng có mẫu;
  - không đặt hai mẫu cùng dòng (ví dụ Xiaomi 15T và 15T Pro) vào hai tập khác nhau.
- **Bước 31 làm ba việc cùng lúc:**
  1. Ghi `ket_qua/khoa_cau_hinh.md`:
     - mô hình LLM và phiên bản API;
     - mã băm từng câu lệnh;
     - k, cách tách từ, ngưỡng sai số;
     - phiên bản tệp cấu hình;
     - checkpoint B3;
     - ngày giờ.
  2. Tính mã băm tệp nhãn tập kiểm tra sau khi đã gán lại và đối chiếu người thứ hai (bước 29).
  3. Commit, gắn tag `khoa-cau-hinh` và đẩy lên **trước** lần chạy tập kiểm tra đầu tiên.
- Sau tag này không sửa nhãn tập kiểm tra. Lỗi nhãn phát hiện sau đó được ghi vào phần mối đe dọa đến tính hợp lệ, không sửa âm thầm.

### 8.4 Chỉ số

| Chỉ số | Công thức | Ý nghĩa |
|---|---|---|
| FAR | #(chuẩn ≠ Đúng ∧ đoán = Đúng) / #(chuẩn ≠ Đúng) | Tỷ lệ tuyên bố sai hoặc lệch bị chấp nhận nhầm. Chỉ số quan trọng nhất |
| Recall Đúng | #(chuẩn = Đúng ∧ đoán = Đúng) / #(chuẩn = Đúng) | Không được thấp hơn đối chứng tốt nhất quá 5 điểm |
| P, R, F1 từng nhãn | Định nghĩa thông thường | Đặc biệt F1 Lệch |
| Macro-F1 | Trung bình F1 của 4 nhãn | |
| Recall@k | #(tuyên bố có đoạn bằng chứng chuẩn trong top-k) / #(tuyên bố có bằng chứng) | Chất lượng truy hồi |
| Precision, Recall của tách tự động | So với tuyên bố tách thủ công | Chất lượng khối tách tuyên bố |
| Độ đúng trích xuất | Tỷ lệ trường đúng: 50 tuyên bố tập phát triển (bước 27) và 30 tuyên bố tập kiểm tra (bước 36), gán tay | Chất lượng khối trích xuất |
| Kết quả đầu–cuối | FAR và Macro-F1 khi tách tự động rồi kiểm chứng trên quảng cáo tập kiểm tra | Chất lượng khi dùng thật trên CopyPro |
| Thời gian, chi phí | Giây và token mỗi tuyên bố | Khả năng dùng trên CopyPro |

### 8.5 Thống kê

- **Khoảng tin cậy 95%:** bootstrap 1000 lần theo cụm quảng cáo, vì các tuyên bố cùng quảng cáo phụ thuộc nhau. Biến thể cặp tối thiểu được gom cụm theo tuyên bố gốc.
- **McNemar:** trên các tuyên bố có nhãn chuẩn khác Đúng, so quyết định chấp nhận hay không của P với từng đối chứng. Hiệu chỉnh Holm cho các phép so sánh.
- **Recall Đúng:** kiểm tra "không kém hơn". Đạt khi cận dưới khoảng tin cậy của hiệu (P trừ đối chứng tốt nhất) lớn hơn −5 điểm.
- **Bảng mô tả:** bảng theo hãng, theo nhóm sản phẩm và theo loại biến đổi chỉ là mô tả, không kiểm định (mỗi ô ít mẫu).
- **Độ tin cậy nhãn:**
  - kappa của Cohen giữa lần gán 1 và lần gán lại (20% số tuyên bố, cách ít nhất 10 ngày, ẩn nhãn cũ);
  - kappa giữa hai người trên khoảng 60 tuyên bố, tính trước khi thảo luận thống nhất.

### 8.6 Giả thuyết và cách kết luận

| Mã | Giả thuyết | Kết luận "đạt" khi |
|---|---|---|
| H1 | P có FAR thấp hơn B0–B3 | FAR(P) < FAR(Bi) với mọi i, McNemar sau hiệu chỉnh Holm có p < 0,05 với ít nhất B0 và B1 |
| H2 | P có F1 Lệch cao hơn B1 và B2 | Khoảng tin cậy của hiệu F1 Lệch (P trừ B1, P trừ B2) nằm hoàn toàn trên 0 |
| H3 | Neo nguồn có ích | P tốt hơn P−NN về FAR và F1 Lệch, khoảng tin cậy của hiệu không chứa 0. P−ĐK chỉ để kiểm tra hợp lý, kỳ vọng F1 Lệch gần 0 |
| H4 | P không làm mất tuyên bố đúng | Kiểm tra "không kém hơn" ở 8.5 đạt |

Đề cương viết gọn thành ba giả thuyết H1–H3 ứng với CH1–CH3; điều kiện của H4 nằm trong H1 của đề cương. Khi viết khóa luận, giữ bốn giả thuyết như bảng trên và ghi rõ ánh xạ: CH1 ↔ H1, H4; CH2 ↔ H2; CH3 ↔ H3.

Phân tích phụ (không phải giả thuyết; dùng làm khuyến nghị cho CopyPro):

1. Tỷ lệ tuyên bố Lệch và Sai trong quảng cáo theo LLM sinh.
2. Tỷ lệ đó theo chế độ có hoặc không kèm đoạn thông số.
3. Tỷ lệ đó theo loại bài.

### 8.7 Bảng và hình kết quả (Chương 4)

1. Thống kê dữ liệu: số mẫu, quảng cáo, tuyên bố theo nhóm, nhãn, LLM, chế độ.
2. Độ tin cậy nhãn: kappa trong-người và giữa-hai-người; kết quả khảo sát cách hiểu.
3. **Bảng kết quả chính:** 7 hệ thống × (FAR, Recall Đúng, F1 từng nhãn, Macro-F1), có khoảng tin cậy.
4. Phân tích thành phần: P, P−ĐK, P−NN.
5. Theo loại biến đổi trên tập cặp tối thiểu.
6. Theo nhóm sản phẩm, hãng, LLM sinh quảng cáo.
7. Ma trận nhầm lẫn của P và B2.
8. Recall@k, Precision và Recall của tách tự động, độ đúng trích xuất.
9. Kết quả đầu–cuối.
10. Thời gian và chi phí.
11. Phân tích phụ.
12. Phân loại lỗi kèm 3–5 trường hợp điển hình.

---

## 9. Tích hợp CopyPro

### 9.1 Kiến trúc

```
Trình duyệt (Next.js: Generator.tsx, trang chi tiết nội dung)
   │ POST /api/contents/:id/verify-specs {maMau}
   ▼
Backend CopyPro (Express, Node.js)
   │ specVerificationService.js gọi SPEC_VERIFIER_URL
   ▼
Dịch vụ kiểm chứng (FastAPI, Python, repo KLTN: src/kiemchung/api.py)
   │ tách và lọc tuyên bố → BM25 → trích xuất có neo nguồn → chuẩn hóa → A–D → lý do
   ▼
Kết quả {tuyen_bo, nhan, doan_nguon, trich, ly_do} → lưu vào Content.specVerification
```

### 9.2 API của dịch vụ kiểm chứng

- `GET /mau-san-pham` → danh sách mẫu có trong kho tài liệu.
- `POST /kiem-chung` với `{"van_ban": "...", "ma_mau": "tn-samsung-buds3pro"}` → `{"phien_ban_he_thong": "...", "ket_qua": [{"tuyen_bo", "nhan", "doan_nguon", "trich", "ly_do"}], "thoi_gian_ms": ...}`.

### 9.3 Thay đổi trong repo CopyPro (nhánh `kiem-chung-thong-so`, theo mã ở commit `09a35a5`)

| Tệp | Thay đổi |
|---|---|
| `backend/src/models/Content.js` | Thêm `specVerification`: `productId`, `results[]`, `verifiedAt`, `verifierVersion` |
| `backend/src/routes/user/contentRoutes.js` | Thêm `router.post('/:id/verify-specs', ...)` |
| `backend/src/controllers/user/contentController.js` | Thêm `verifySpecs` |
| `backend/src/services/specVerificationService.js` (mới) | Gọi dịch vụ Python; xử lý quá thời gian; lưu kết quả |
| `backend/src/validations/contentValidation.js` | Lược đồ cho `verify-specs` |
| `frontend/src/services/contentService.ts`, `frontend/src/hooks/queries/useContents.ts` | Hàm và hook gọi API mới |
| `frontend/src/app/generate/Generator.tsx` | Nút "Kiểm chứng thông số" và ô chọn mẫu sản phẩm, đặt cạnh điểm chất lượng |
| `frontend/src/app/contents/[id]/` | Hiển thị kết quả đã lưu |
| `SpecVerificationPanel.tsx` (mới) | Tô màu tuyên bố theo nhãn; xem đoạn nguồn và lý do |

### 9.4 Kiểm tra (bước 39)

- Chạy trên 10 quảng cáo tập kiểm tra. Kết quả trên giao diện phải trùng kết quả chạy dịch vụ trực tiếp.
- Đo thời gian từ lúc bấm đến lúc có kết quả, ghi trung vị và p90.
- Quay video 2–3 phút: tạo quảng cáo → kiểm chứng → sửa tuyên bố lệch → kiểm chứng lại.

---

## 10. Chi tiết từng bước

Mỗi bước có **Mục đích**, **Làm**, **Xong khi**. Bước nào trỏ tới mục 5–9 thì đọc mục đó trước.

### Giai đoạn 1 – Chốt đề tài (09–12/10)

**Bước 01. Đối chiếu lại đề cương với bài gốc.**

- *Mục đích:* mọi câu nói về bài khác trong đề cương phải đúng với bài gốc. Khoa từng nhắc lỗi này ở đề cương của bạn khác.
- *Làm:* mở bài gốc trong `báo/` hoặc trang ACL Anthology, tìm đoạn tương ứng, ghi số trang vào `ghi_chu_tai_lieu.md`. Các ý đã được đối chiếu ngày 09/10/2026:
  - Fathom F1 bằng 0 ở nhãn Conflicting/Cherry-picking trên tập phát triển (38 tuyên bố);
  - [16] chỉ gán một nhãn cho cả bài;
  - NumPert giảm đến 62%;
  - SemViQA ở ACL 2026 Industry Track;
  - Điều 15a khoản 3 Luật 75/2025/QH15.

  Sinh viên tự đọc lại để trả lời được khi bị hỏi.
- *Xong khi:* mỗi câu có số trang.

**Bước 02. Gửi đề cương cho CBHD, chốt tên đề tài.**

- *Làm:*
  1. Gửi bản `_chu_do.docx` kèm 3 dòng tóm tắt thay đổi:
     - tên mới;
     - phạm vi chỉ gồm tuyên bố có điều kiện ràng buộc;
     - tính mới, đóng góp và cải tiến.
  2. Hỏi CBHD hai câu: tên tiếng Anh đã ổn chưa; có đồng ý nhờ một bạn làm người gán thứ hai không.
  3. Khi được đồng ý, nộp bản sạch theo lịch Khoa.
  4. Cập nhật tên trên hệ thống đăng ký, so từng ký tự.
- *Xong khi:* **Mốc 1**.

**Bước 03. Dọn repo, tạo thư mục và môi trường.**

- *Làm:*
  1. Tạo thư mục theo 5.1.
  2. Tạo `requirements.txt` gồm: python ≥ 3.10, rank-bm25, pyvi, pydantic, pyyaml, google-genai, groq, fastapi, uvicorn, pytest, scikit-learn, statsmodels, pandas, matplotlib, playwright.
  3. Tạo `.env.example`.
  4. Lịch sử repo từng có tệp `.env`. Nếu khóa trong đó chưa thu hồi thì thu hồi và tạo khóa mới.
- *Xong khi:* `pytest` chạy; `git check-ignore .env` trả về `.env`.

### Giai đoạn 2 – Nguồn bằng chứng và quy chuẩn nhãn (13–21/10)

**Bước 04. Chọn 12 mẫu sản phẩm.**

- *Làm:*
  1. Mở trang thông số tiếng Việt của các ứng viên:
     - điện thoại: iPhone 17, Xiaomi 15T, OPPO Find X8, một mẫu Galaxy S và một mẫu khác dòng;
     - tai nghe: Galaxy Buds3 Pro, AirPods Pro 3, AirPods 4, một mẫu Xiaomi hoặc OPPO;
     - đồng hồ: Apple Watch SE 3, một mẫu Galaxy Watch, một mẫu Xiaomi.
  2. Giữ mẫu có ít nhất 3 thông số kèm điều kiện.
  3. Ghi `mau_san_pham.csv`.
  4. Chia trước:
     - tập phát triển: iPhone 17, Galaxy Buds3 Pro (2 mẫu thử), Apple Watch SE 3, Xiaomi 15T;
     - tập kiểm tra: 8 mẫu còn lại.
- *Xong khi:* đủ 3 nhóm, ≥3 hãng; tập kiểm tra có đủ nhóm và hãng.

**Bước 05. Chụp trang thông số.**

- *Làm:*
  1. Script Playwright mở URL, chờ tải xong, mở các mục "Xem thêm" và chú thích.
  2. Lưu `page.html`, `page.txt` (chữ hiển thị), `full.png`, `meta.json` (url, thời điểm, mã băm SHA-256).
  3. Có thể tham khảo `scripts/capture_evidence.mjs` trong lịch sử repo (commit `ba88a48`).
  4. Kiểm lại hai trang nghi vấn ở 6.5.
- *Xong khi:* đủ 12 mẫu; chú thích điều kiện có trong `page.txt`.

**Bước 06. Chia đoạn.**

- *Làm:*
  1. Mỗi dòng hoặc mục thông số là một đoạn.
  2. Chú thích (dấu *, số mũ) nối vào đoạn có ký hiệu tương ứng.
  3. Đoạn mang tiêu đề mục ("Pin", "Màn hình") ở đầu.
- *Xong khi:* kiểm 20 đoạn ngẫu nhiên, không đoạn nào mất điều kiện.

**Bước 07. Tệp cấu hình.**

- *Làm:* viết 3 tệp YAML theo 7.7 từ bảng 6.3 và **chỉ từ trang của tập phát triển**. Không mở trang của tập kiểm tra khi viết.
- *Xong khi:* mọi thuộc tính trong 6 nhóm thông số có đủ các khóa ở 7.7.

**Bước 08. Hướng dẫn gán nhãn bản 1 và khảo sát cách hiểu.**

- *Làm:*
  1. Viết `huong_dan_gan_nhan.md` theo mục 6.
  2. Chuyển 20 ví dụ tháng 9 sang 4 nhãn; thay ví dụ nào dùng mẫu tập kiểm tra.
  3. Bổ sung cho đủ ≥24 ví dụ.
  4. Khảo sát nhanh 5–10 người: đưa 8 tuyên bố không nêu điều kiện (ví dụ "Apple Watch SE 3 pin 32 giờ"), hỏi họ hiểu thế nào. Ghi tỷ lệ hiểu theo cách hiểu thông thường đã chọn.
- *Xong khi:* mỗi nhãn và mỗi loại biến đổi có ≥2 ví dụ; có kết quả khảo sát.

### Giai đoạn 3 – Bộ thử ban đầu (20/10–08/11)

**Bước 09. Script sinh quảng cáo.**

- *Làm:*
  1. Sao chép nguyên văn `buildPrompt()` và `getCopyTypeFormatPrompt()` trong `frontend/src/app/generate/Generator.tsx` của CopyPro (commit `09a35a5`) sang Python.
  2. Cố định ngành "Công nghệ", giọng điệu "Chuyên nghiệp", độ dài "medium", 3 phiên bản mỗi lần gọi (mặc định của CopyPro).
  3. Từ khóa là 3–4 thông số nổi bật của mẫu.
  4. Hai chế độ:
     - `ten`: chỉ tên sản phẩm;
     - `ten_thong_so`: dán đoạn thông số vào "Thông tin bổ sung".
  5. Gọi `gemini-2.5-flash` và `llama-3.3-70b-versatile` (Groq).
  6. Sinh 2–3 bài bằng giao diện CopyPro để đối chiếu.
- *Xong khi:* có kiểm thử so khớp câu lệnh.

**Bước 10. Sinh quảng cáo cho 2 mẫu thử.** Gồm 2 × 2 × 3 × 2 = 24 lần gọi. *Xong khi:* có 24 tệp.

**Bước 11. Tách và lọc tuyên bố bộ thử.**

- *Làm:* LLM tách theo 6.1 rồi sửa tay, lọc theo tệp cấu hình, gộp tuyên bố trùng.
- *Xong khi:* có khoảng 60 tuyên bố.

**Bước 12. Gán nhãn bộ thử.**

- *Làm:* theo 6.2. Ghi bằng chứng, lý do, số giây. Chỗ nào hướng dẫn chưa rõ thì ghi vào danh sách "câu hỏi nhãn".
- *Xong khi:* 100% có nhãn.

**Bước 13. BM25.** Cài 7.2, đo Recall@k trên bộ thử. *Xong khi:* có bảng Recall@k và kiểm thử.

**Bước 14. B0.** Câu lệnh ở Phụ lục A.1, nhiệt độ 0, bộ nhớ đệm, ánh xạ nhãn. *Xong khi:* chạy hết bộ thử.

**Bước 15. Phân tích bộ thử, chốt quy mô.**

- *Làm:*
  1. Tính phân bố nhãn, số phút mỗi tuyên bố, số tuyên bố có điều kiện mỗi quảng cáo.
  2. Xem B0 sai ở đâu.
  3. Sửa hướng dẫn thành bản 2 và gán lại bộ thử theo bản 2.
  4. Chốt số lần sinh để đạt 250–300 tuyên bố (tính cả bộ thử).
  5. Gửi CBHD tóm tắt 1 trang.
- *Xong khi:* **Mốc 2**.

**Bước 16. Nháp Chương 1 và 2.**

- *Làm:* đọc kỹ AVeriTeC [7], Fathom [20], [16], Jiang [17], MiniCheck [15], SemViQA [11], NumPert [13]. Lập bảng "hạn chế → cải tiến" và viết theo 11.1.
- *Xong khi:* mọi tài liệu được trích dẫn đúng trang.

### Giai đoạn 4 – Dữ liệu chính (02–15/11)

**Bước 17. Sinh quảng cáo cho 10 mẫu còn lại.**

- *Làm:* 10 × 2 × 3 × 2 = 120 lần gọi. Nếu bước 15 cho thấy thiếu tuyên bố thì tăng số lần sinh, không đổi brief.
- *Xong khi:* đủ tổ hợp.

**Bước 18. Tách, lọc, lấy mẫu.**

- *Làm:* như bước 11, rồi lấy mẫu phân tầng theo nhóm × LLM × chế độ.
- *Xong khi:* tính cả bộ thử, có 250–300 tuyên bố.

**Bước 19. Gán nhãn chính lần 1.**

- *Làm:*
  1. Gán tập phát triển trước (xong 08/11) để bước 22–23 có dữ liệu.
  2. Gán tập kiểm tra sau (09–13/11).
  3. Mỗi buổi tối đa 60 phút liên tục.
- *Xong khi:* 100% có nhãn.

**Bước 20. Tập cặp tối thiểu.**

- *Làm:* từ tuyên bố Đúng, tạo 6 loại biến đổi theo mã ở 5.3:
  - bỏ điều kiện;
  - đổi điều kiện (thay bằng điều kiện khác có trong tài liệu);
  - đổi bộ phận;
  - đổi kiểu giá trị;
  - đổi giá trị (giá trị không có ở điều kiện nào, cho nhãn Sai);
  - đổi phiên bản (chỉ khi trang có nhiều phiên bản).

  Gán và kiểm tay từng nhãn.
- *Xong khi:* 100–120 biến thể; mỗi loại ≥15, riêng loại đổi phiên bản tùy dữ liệu.

**Bước 21. Chốt chia tập.** Ghi `chia_tap.json` và commit. *Xong khi:* từ đây mọi phát triển chỉ dùng tập phát triển.

### Giai đoạn 5 – Phương pháp P và đối chứng (09–30/11)

**Bước 22. Chuẩn hóa.** Cài 7.4. *Xong khi:* có ≥20 kiểm thử ("6 tiếng" = 6 giờ, "IP57", "3.000 nit" = 3000, "lên đến").

**Bước 23. Trích xuất có neo nguồn và kiểm tra đầy đủ.**

- *Làm:* câu lệnh ở Phụ lục A.4, lược đồ 7.1, kiểm tra 7.3.
- *Xong khi:* kiểm thử đạt; chạy hết tập phát triển; có thống kê `bi_loai` và `bo_sung`.

**Bước 24. Tách và lọc tuyên bố tự động.**

- *Làm:* câu lệnh tách (Phụ lục A.5) và bộ lọc theo tệp cấu hình. So với tuyên bố tách thủ công của tập phát triển: tuyên bố được coi là trùng khi cùng thuộc tính và cùng giá trị.
- *Xong khi:* có Precision và Recall.

**Bước 25. B2 và B3.**

- *Làm:*
  - B2: câu lệnh Phụ lục A.3.
  - B3: cài `semviqa`, chạy hai checkpoint trên tập phát triển, chọn checkpoint tốt hơn.
- *Xong khi:* cả hai chạy hết tập phát triển.

**Bước 26. Bộ quyết định A–D.**

- *Làm:* cài 7.5–7.6; viết kiểm thử theo 7.8.
- *Xong khi:* ≥30 kiểm thử đạt, gồm 18 ví dụ ở 6.4.

**Bước 27. Ghép P, cài đặt B1, đo độ đúng trích xuất.**

- *Làm:*
  1. Ghép `p.py`.
  2. B1 nhận đúng bộ thông số của P cùng hướng dẫn 6.2–6.3 (Phụ lục A.2).
  3. Gán tay trường đúng của 50 tuyên bố tập phát triển.
- *Xong khi:* có bảng độ đúng trích xuất.

**Bước 28. P−ĐK và P−NN.** Thêm hai cờ theo 7.5. *Xong khi:* chạy hết tập phát triển.

**Bước 29. Độ tin cậy nhãn.**

- *Làm:*
  1. Gán lại mù 20% số tuyên bố (phân tầng theo nhóm và tập), cách lần đầu ít nhất 10 ngày.
  2. Người thứ hai đọc hướng dẫn, gán thử 10 ví dụ tập phát triển có phản hồi, rồi gán độc lập 60 tuyên bố phân tầng.
  3. Tính kappa trước khi thảo luận.
  4. Nhãn chuẩn sai rõ ràng thì sửa và ghi vào `ket_qua/sua_nhan.md`. Mọi sửa phải xong trong bước này, trước khi niêm phong, và không dựa trên đầu ra của hệ thống.
- *Xong khi:* có `do_tin_cay_nhan.md`.

**Bước 30. Nháp Chương 3.** Viết song song từ khi khóa cấu hình đến khi có kết quả; dùng ví dụ 1.1; vẽ lại Hình 1 của đề cương ở độ phân giải cao. *Xong khi:* đủ mục 11.1.

**Bước 31. Chọn cấu hình, khóa, niêm phong.**

- *Làm:*
  1. Chọn LLM (một LLM chung cho trích xuất và B0–B2), k, cách tách từ, ngưỡng sai số, checkpoint B3, chỉ dựa trên tập phát triển.
  2. Làm ba việc ở 8.3.
- *Xong khi:* **Mốc 3**; CBHD nhận tệp khóa.

**Bước 32. Dịch vụ FastAPI.**

- *Làm:* cài 9.2 (tách tự động rồi P), viết `Dockerfile`, chạy cục bộ, thử 3 quảng cáo.
- *Xong khi:* kết quả của API trùng việc chạy tách tự động rồi `p.py`.

### Giai đoạn 6 – Thực nghiệm cuối và tích hợp song song (01–13/12)

**Bước 33. Chạy tập kiểm tra một lần.**

- *Làm:*
  1. Chạy 7 hệ thống trên tuyên bố thường và cặp tối thiểu, cộng một lượt đầu–cuối trên quảng cáo tập kiểm tra.
  2. Ghi `manifest.json`.
  3. Nếu chương trình lỗi giữa chừng thì chạy lại phần lỗi với đúng cấu hình đã khóa và ghi vào nhật ký.
- *Xong khi:* đủ đầu ra.

**Bước 34. Backend CopyPro.**

- *Làm:* theo bảng 9.3 (phần backend), biến môi trường `SPEC_VERIFIER_URL`, giới hạn thời gian 60 giây, lưu vào `Content`.
- *Xong khi:* gọi API bằng Postman thành công và kết quả được lưu.

**Bước 35. Chỉ số, khoảng tin cậy, kiểm định.**

- *Làm:* `danh_gia.py` theo 8.4–8.5; xuất bảng ra CSV và Word; vẽ hình.
- *Xong khi:* đủ bảng 1–11 ở 8.7.

**Bước 36. Phân tích lỗi.**

- *Làm:*
  1. Với mỗi lỗi của P (tối đa 60, lấy ngẫu nhiên nếu nhiều hơn), xác định nguồn: tách tuyên bố, truy hồi, trích xuất, quyết định, hay nhãn chuẩn.
  2. Gán tay trường đúng của 30 tuyên bố tập kiểm tra để đo độ đúng trích xuất.
  3. Chọn 3–5 trường hợp điển hình.
- *Xong khi:* có bảng 12 ở 8.7.

**Bước 37. Giả thuyết và phân tích phụ.** Điền bảng 8.6, viết thảo luận trung thực. *Xong khi:* **Mốc 4**.

**Bước 38. Giao diện CopyPro.**

- *Làm:* thành phần `SpecVerificationPanel.tsx`:
  - màu theo nhãn: Đúng xanh lá, Sai đỏ, Lệch cam, Chưa đủ xám;
  - mỗi tuyên bố có nút xem đoạn nguồn và lý do;
  - ô chọn mẫu sản phẩm;
  - đặt cạnh điểm chất lượng và kết quả đạo văn.
- *Xong khi:* chạy được cục bộ và trên bản triển khai thử.

**Bước 39. Kiểm tra tích hợp và video.** Theo 9.4. *Xong khi:* **Mốc 5**.

### Giai đoạn 7 – Viết và nộp (08–31/12)

**Bước 40. Chương 4.** Viết theo 8.7 và 11.1. Mỗi bảng có một đoạn "con số này nói gì". Có mục mối đe dọa đến tính hợp lệ:

- người gán chính là tác giả;
- quảng cáo do LLM sinh;
- B3 ngoài miền;
- cùng LLM vừa sinh vừa kiểm chứng;
- số mẫu tập kiểm tra.

**Bước 41. Chương 5 và 6.**

- Chương 5: kiến trúc 9.1, API, ảnh giao diện, bảng thời gian.
- Chương 6: kết luận theo M1–M4, giới hạn, hướng phát triển (mục 14).

**Bước 42. Bản thảo đầy đủ.** Gửi CBHD ngày 18/12 kèm bảng "góp ý → cách sửa"; sửa trong 19–26/12. *Xong khi:* **Mốc 6**.

**Bước 43. Gói tái lập.**

- README hướng dẫn cài và chạy.
- `scripts/chay_lai.sh` chạy từ đầu ra đã lưu ra bảng kết quả, không gọi lại LLM nhờ bộ nhớ đệm.
- Thẻ dữ liệu: nguồn; giấy phép (trang thông số thuộc bản quyền của hãng, chỉ chia sẻ trích đoạn ngắn và đường dẫn); cách gán nhãn; giới hạn.

**Bước 44. Kiểm tra cuối và nộp.** Theo Phụ lục B; gắn tag `v1.0`. Dành 27–30/12 làm thời gian dự phòng. *Xong khi:* **Mốc 7**.

### Giai đoạn 8 – Bảo vệ

**Bước 45. Chuẩn bị bảo vệ.**

- Slide 15–20 trang cho khoảng 15 phút, theo thứ tự: vấn đề → ví dụ xuyên suốt → hạn chế các bài trước → phương pháp → dữ liệu → kết quả → demo → kết luận.
- Video demo dự phòng.
- Tập dượt 3 lần.
- Học thuộc câu trả lời ở mục 13.

---

## 11. Viết khóa luận

### 11.1 Dàn ý và số trang dự kiến (khoảng 60–80 trang, theo mẫu Khoa)

| Chương | Nội dung | Trang | Bước |
|---|---|---|---|
| 1. Tổng quan | Bối cảnh, CopyPro, vấn đề, mục tiêu M1–M4, phạm vi, đối tượng, đóng góp, bố cục | 8–10 | 16 |
| 2. Cơ sở lý thuyết và nghiên cứu liên quan | Kiểm chứng tự động (FEVER, AVeriTeC), BM25, tuyên bố số liệu, ảo giác của LLM, kiểm chứng tiếng Việt, kiểm chứng quảng cáo; bảng "hạn chế → cải tiến" | 12–15 | 16 |
| 3. Phương pháp đề xuất | Phát biểu bài toán, định nghĩa nhãn, bộ thông số, tách tuyên bố, trích xuất có neo nguồn, kiểm tra đầy đủ, chuẩn hóa, A–D, tệp cấu hình, sinh lý do, ví dụ xuyên suốt | 12–15 | 30 |
| 4. Dữ liệu và thực nghiệm | Xây dựng dữ liệu, hướng dẫn nhãn, độ tin cậy, thiết lập, đối chứng, kết quả, phân tích thành phần, phân tích lỗi, thảo luận, mối đe dọa đến tính hợp lệ | 15–20 | 40 |
| 5. Tích hợp vào CopyPro | Kiến trúc, API, giao diện, đánh giá thời gian, kết quả đầu–cuối | 6–8 | 41 |
| 6. Kết luận và hướng phát triển | Kết quả theo mục tiêu, giới hạn, hướng phát triển | 2–3 | 41 |
| Phụ lục | Hướng dẫn gán nhãn, câu lệnh, tệp cấu hình, kiểm thử | – | 43 |

### 11.2 Quy tắc viết

- Mỗi đoạn mở đầu bằng ý chính.
- Mọi con số có nguồn: bảng của mình, hoặc tài liệu kèm trang.
- Thuật ngữ thống nhất trong toàn khóa luận:
  - tuyên bố;
  - điều kiện ràng buộc;
  - cách hiểu thông thường;
  - Lệch điều kiện;
  - neo nguồn;
  - bộ quyết định.
- Hình tự vẽ, mũi tên thẳng; bảng có tiêu đề và nguồn.
- Không dùng "...", không viết hoa tùy tiện.

---

## 12. Rủi ro và phương án

### 12.1 Bảng rủi ro

| Rủi ro | Dấu hiệu sớm | Phương án |
|---|---|---|
| Quảng cáo chứa ít tuyên bố có điều kiện | Bước 15: dưới 2 tuyên bố có điều kiện mỗi quảng cáo | Tăng số lần sinh mỗi mẫu; giữ brief cố định; tập cặp tối thiểu bảo đảm đủ mẫu từng loại |
| Trang thông số dùng mã động, thiếu chú thích hoặc ghi nhầm | Bước 05: `page.txt` thiếu chú thích | Mở rộng các mục trước khi chụp; đổi mẫu cùng nhóm; gắn cờ mâu thuẫn |
| Gán nhãn chậm | Bước 12: hơn 3 phút mỗi tuyên bố | Giảm tuyên bố thường xuống khoảng 200; giữ đủ cặp tối thiểu và đủ hãng trong tập kiểm tra |
| Giới hạn API hoặc chi phí | Lỗi 429, hết hạn mức | Bộ nhớ đệm; chạy theo lô; dùng mô hình đã có trên CopyPro |
| Không có người gán thứ hai | Hết 20/11 chưa có người | Chỉ báo kappa trong-người, ghi rõ giới hạn |
| SemViQA không chạy được | Lỗi cài gói, thiếu RAM | Chạy trên Colab; nếu vẫn lỗi thì bỏ B3 và ghi rõ |
| P không đạt giả thuyết | Bước 37 | Báo trung thực; phân tích lỗi chỉ ra khối gây lỗi; đề xuất cải tiến ở Chương 6 |
| Trễ tích hợp CopyPro | Bước 34 trễ quá 2 ngày | Giao diện tối giản: một bảng danh sách, vẫn lưu vào `Content` để giữ cam kết của Nội dung 4 |

### 12.2 Phương án rút gọn khi chậm tiến độ

Bỏ dần theo thứ tự dưới đây, mục đầu tiên bỏ trước:

1. Bảng theo hãng và phân tích phụ.
2. Khảo sát cách hiểu của người đọc.
3. Video demo (thay bằng ảnh chụp).
4. B3.
5. Người gán thứ hai.

**Lõi không bao giờ bỏ:**

- P với đủ A–D, neo nguồn và kiểm tra đầy đủ;
- B0, B1, B2;
- P−ĐK và P−NN;
- tập kiểm tra được khóa và niêm phong;
- FAR và F1 Lệch có khoảng tin cậy;
- tính năng trên CopyPro có lưu kết quả.

---

## 13. Câu hỏi phản biện dự kiến

| # | Câu hỏi | Ý chính để trả lời |
|---|---|---|
| 1 | Đề tài khác gì kiểm chứng thông tin thông thường? | Các phương pháp hiện có chủ yếu xét khớp nội dung. Em biểu diễn điều kiện ràng buộc và quyết định nhãn Lệch bằng quy tắc. Bằng chứng là FAR và F1 Lệch so với B0–B3, cùng ví dụ Buds3 Pro |
| 2 | Vì sao dùng quy tắc mà không huấn luyện mô hình? | Dữ liệu nhỏ; quy tắc giải thích và kiểm thử được; lý do luôn khớp nhãn. LLM vẫn được dùng ở phần nó làm tốt là tách và trích xuất, và có neo nguồn |
| 3 | Quy tắc có cứng nhắc, khó mở rộng không? | Phần phụ thuộc nhóm sản phẩm nằm trong tệp cấu hình; thêm nhóm là thêm tệp. Khả năng mở rộng là thiết kế, chưa được thực nghiệm ngoài 3 nhóm; mục 14 nêu chi phí |
| 4 | Tự gán nhãn rồi tự đánh giá có thiên lệch không? | Hướng dẫn viết trước; B1, B2 nhận cùng hướng dẫn; khóa và niêm phong trước tập kiểm tra; kappa giữa hai người và trong-người; khảo sát cách hiểu |
| 5 | Quảng cáo do LLM sinh có đại diện cho quảng cáo thật không? | Đúng ngữ cảnh sử dụng của CopyPro; đã nêu giới hạn; hướng phát triển là quảng cáo thật trên sàn thương mại điện tử |
| 6 | Vì sao chỉ 12 mẫu và 3 nhóm? | Tiêu chí chọn ở đề cương; tập cặp tối thiểu bù cho số mẫu; mở rộng nhóm cần định nghĩa thêm điều kiện bắt buộc |
| 7 | LLM trích xuất sai thì sao? | Neo nguồn loại trường bịa; kiểm tra đầy đủ bắt điều kiện bị bỏ sót; P−NN đo tác dụng; có bảng độ đúng trích xuất trên cả hai tập |
| 8 | Gemini vừa sinh vừa kiểm chứng thì có thiên lệch không? | Kết quả được báo tách theo LLM sinh quảng cáo |
| 9 | Nếu P không tốt hơn đối chứng? | Báo trung thực; phân tích lỗi chỉ ra khối gây lỗi; vẫn có đóng góp dữ liệu và tính năng |
| 10 | Vì sao BM25 mà không dùng truy hồi dày đặc? | Kho tài liệu mỗi mẫu nhỏ; đã đo Recall@k; truy hồi không phải trọng tâm |
| 11 | B3 không có nhãn Lệch, so sánh có công bằng không? | So bằng FAR; giả thuyết về F1 Lệch chỉ so với B1, B2. B3 được dùng làm đại diện hệ thống tiếng Việt sẵn có, đã nêu là ngoài miền |
| 12 | "Cách hiểu thông thường" có chủ quan không? | Ghi trong tệp cấu hình trước khi gán nhãn; có khảo sát người đọc và kappa; quy tắc E1 tránh phạt tuyên bố thận trọng |
| 13 | Tài liệu chính hãng sai thì sao? | Gắn cờ mâu thuẫn, gán Chưa đủ thông tin, thống kê riêng; không kết luận pháp lý |
| 14 | Thời gian và chi phí khi dùng thật? | Bảng thời gian (trung vị, p90) và token mỗi tuyên bố; kết quả đầu–cuối |
| 15 | Có vi phạm bản quyền khi dùng trang thông số không? | Chỉ dùng để nghiên cứu; chia sẻ trích đoạn ngắn kèm đường dẫn |
| 16 | Vì sao tiếng Việt? | CopyPro phục vụ người Việt; tài nguyên kiểm chứng tiếng Việt còn ít; Luật Quảng cáo sửa đổi 2025 nhấn mạnh việc kiểm tra tài liệu sản phẩm |

---

## 14. Ngoài phạm vi và hướng phát triển

**Ngoài phạm vi:**

- tuyên bố không kèm điều kiện;
- tuyên bố cảm tính, so sánh, giá, khuyến mãi;
- đo hiệu năng thật;
- kết luận pháp lý;
- tự nhận diện sản phẩm.

**Hướng phát triển:**

1. Thêm nhóm sản phẩm (máy tính bảng, máy tính xách tay, tivi, đồ gia dụng) bằng tệp cấu hình mới.
2. Kiểm chứng quảng cáo thật trên sàn thương mại điện tử.
3. Truy hồi bằng chứng ngoài trang chính hãng, xử lý xung đột như CoVer [19].
4. Gợi ý sửa câu tự động: viết lại tuyên bố Lệch kèm điều kiện đúng.
5. Thêm trường "thông số sản phẩm" vào brief của CopyPro để giảm lỗi ngay từ bước sinh.

---

## Phụ lục A. Khung câu lệnh

Đây là điểm bắt đầu. Bản cuối được chốt ở bước 31 và lưu kèm mã băm.

**A.1 B0 (3 nhãn).** "Bạn là người kiểm chứng thông tin. Dựa CHỈ vào các đoạn tài liệu chính hãng dưới đây, hãy cho biết tuyên bố được tài liệu ủng hộ (Supported), bị bác bỏ (Refuted) hay chưa đủ thông tin (NEI). Trả về JSON {"nhan": ..., "doan": [...], "ly_do": ...}. Tuyên bố: {tb}. Tài liệu: {doan_1..k}."

**A.2 B1 (4 nhãn, dữ liệu cấu trúc).** "Cho bộ thông số của tuyên bố và các bộ thông số trích từ tài liệu (JSON). Gán một nhãn: Đúng, Sai, Lệch điều kiện, Chưa đủ thông tin, theo hướng dẫn sau: {mục 6.2–6.3 và tóm tắt tệp cấu hình}. Trả về JSON."

**A.3 B2 (4 nhãn, hướng dẫn và ví dụ).** Gồm hướng dẫn 6.2–6.3, 4 ví dụ từ tập phát triển (mỗi nhãn một ví dụ), tuyên bố và top-k đoạn. Trả về JSON.

**A.4 Trích xuất của P.** "Trích bộ thông số theo lược đồ JSON cho tuyên bố và cho từng thông số liên quan trong tài liệu. Với MỖI trường, ghi kèm 'trich' là đoạn chép NGUYÊN VĂN từ văn bản tương ứng. Không suy đoán; trường không có trong văn bản thì để null." Kèm lược đồ 7.1 và 2 ví dụ.

**A.5 Tách tuyên bố.** "Tách đoạn quảng cáo thành các tuyên bố, mỗi tuyên bố một thuộc tính và một giá trị; giữ tên sản phẩm, phiên bản, bộ phận và điều kiện từ câu xung quanh. Trả về danh sách JSON {"tuyen_bo", "cau_goc", "thuoc_tinh_du_kien"}." Sau đó Python chỉ giữ tuyên bố có thuộc tính trong tệp cấu hình.

## Phụ lục B. Danh sách kiểm tra trước khi nộp (bước 44)

- [ ] Tên đề tài tiếng Việt và tiếng Anh trong khóa luận, đề cương và hệ thống trùng từng ký tự.
- [ ] Mọi tài liệu trong danh mục được trích dẫn ít nhất một lần; mọi trích dẫn có trong danh mục; định dạng IEEE thống nhất.
- [ ] Mỗi câu nói về bài báo khác khớp với ghi chú có số trang.
- [ ] Mục tiêu M1–M4 tương ứng Nội dung 1–4 và các chương.
- [ ] Bảng và hình có số, có tiêu đề, được nhắc trong bài; hình tự vẽ, mũi tên thẳng.
- [ ] Không còn "...", chữ đỏ, ghi chú nháp; định dạng gạch đầu dòng thống nhất.
- [ ] Số liệu trong Chương 4 khớp tệp kết quả (chạy `scripts/chay_lai.sh` rồi so).
- [ ] Tag `khoa-cau-hinh` có ngày trước lần chạy tập kiểm tra.
- [ ] Đã kiểm tra trùng lặp văn bản theo quy định của trường.
- [ ] Repo có README, giấy phép, thẻ dữ liệu; không có khóa API.
- [ ] Video demo và bản PDF khóa luận đã lưu ở hai nơi.
