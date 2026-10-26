# Phân tích: điều kiện nằm ngoài bộ luật và tính khả thi của nhãn Lệch điều kiện

**Ngày:** 26/10/2026 · **Người hỏi:** người thực hiện · **Phân tích:** Claude · **Trạng thái:** người thực hiện đã duyệt; đề xuất 1–4 ở mục 9 đã áp dụng chiều 26/10, đề xuất 5 (thử độ bao phủ) làm ở phiên sau.

## 1. Câu hỏi

Bộ luật (tệp cấu hình Bước 8) chỉ học điều kiện từ 4 mẫu tập phát triển. Nếu 4 mẫu cho pin có điều kiện A, B nhưng 12 mẫu có A, B, C, D, E, F, thì bộ luật có còn đúng đắn không, hay C–F bị coi là "không có điều kiện"? Kèm theo: nhãn Lệch điều kiện vốn chỉ là đề xuất, có thật sự khả thi không.

## 2. Kết luận ngắn

1. **Có lỗi thật, và lỗi nằm ở thiết kế xử lý điều kiện của P, không nằm ở bài toán.** Nếu bước trích xuất chỉ ghi các điều kiện có tên trong tệp cấu hình, điều kiện lạ trong tài liệu sẽ bị bỏ im lặng. Giá trị kèm điều kiện lạ khi đó bị coi như không có điều kiện, và quảng cáo khớp con số đó được chấm **Đúng nhầm**. Lỗi này đánh thẳng vào FAR, chỉ số chính của giả thuyết 1.
2. **Gốc của lỗi** là tiền đề trong đề cương: "có thể liệt kê trước các loại điều kiện". Tiền đề này đúng với **6 loại** điều kiện, nhưng tệp cấu hình lại liệt kê **từng điều kiện cụ thể** (chống ồn, MagSafe...). Loại thì ít và ổn định; điều kiện cụ thể thì mở, không liệt kê hết được. MeasEval, lược đồ mà đề cương nói là đang áp dụng, cũng ghi điều kiện (Qualifier) dưới dạng đoạn chữ mở, không theo danh sách đóng.
3. **Sửa được mà không đổi bài toán:** tách việc *phát hiện* điều kiện (mở: ghi mọi điều kiện gắn với con số, kể cả điều kiện lạ) khỏi việc *hiểu* điều kiện (đóng: cách hiểu mặc định và cách diễn đạt chỉ có cho điều kiện đã biết). Điều kiện lạ không bao giờ được coi là "không điều kiện"; quảng cáo khớp giá trị kèm điều kiện lạ thì ra Chưa đủ thông tin, không ra Đúng.
4. **Nhãn Lệch khả thi một phần.** Phần chắc nhất là D4 khi tài liệu công bố nhiều giá trị ở các điều kiện khác nhau và con số của quảng cáo trùng giá trị ở điều kiện không phải mặc định. Phần mong manh là cách hiểu mặc định (do người làm đặt) và độ đồng thuận khi gán nhãn. Giả thuyết 1 (giảm FAR) không phụ thuộc nhãn Lệch, vì Lệch hay Chưa đủ thông tin đều không phải Đúng; giả thuyết 2 (F1 nhãn Lệch) mới là phần rủi ro.
5. **Phát hiện phụ:** số liệu gốc của nghiên cứu FTC 2012 cho thấy bỏ chữ "lên đến" **không** làm người đọc hiểu khác đi có ý nghĩa thống kê. Quyết định sáng 26/10 ("bỏ lên đến là Lệch") nên đảo lại; đề cương đúng ở ví dụ đoạn 73.

## 3. Điều kiện được dùng ở đâu trong P

| Vai trò | Cần biết trước tên điều kiện? | Điều kiện lạ thì hiện tại ra sao |
|---|---|---|
| (1) Lọc tuyên bố thuộc phạm vi | Không; chỉ cần danh sách thuộc tính (sáu nhóm thông số của đề cương) | Không ảnh hưởng |
| (2) Đọc điều kiện của giá trị trong tài liệu | Không nhất thiết; tài liệu tự ghi điều kiện | **Bị bỏ im lặng** nếu chỉ ghi điều kiện có trong cấu hình. Đây là lỗi |
| (3) Đọc điều kiện của tuyên bố | Không nhất thiết | Đã có luật: tuyên bố nêu điều kiện lạ thì D1a |
| (4) So điều kiện của tuyên bố với tài liệu | Cần biết các cách diễn đạt tương đương | Không so được |
| (5) Hiểu điều kiện khi tuyên bố không nêu | Cần (đây là giả định về người đọc) | Không có cách hiểu |

Chỉ vai trò (2) gây kết luận sai; vai trò (3), (4), (5) chỉ làm giảm độ bao phủ.

## 4. Ba tình huống khi tài liệu có điều kiện lạ

Ví dụ giả định: bộ luật biết chống ồn (A) và hộp sạc (B); một tai nghe khác có thêm "chế độ chơi game" (C).

| Tài liệu ghi | Hiện tại | Đúng ra |
|---|---|---|
| "10 giờ khi tắt chế độ chơi game, 8 giờ khi bật" | C bị bỏ; hai giá trị trông như cùng điều kiện nên ra D1b "tài liệu mâu thuẫn" | Quảng cáo "pin 10 giờ" là Lệch (10 giờ chỉ khi tắt chơi game); "pin 8 giờ" là Đúng |
| Chỉ "10 giờ khi tắt chế độ chơi game" | C bị bỏ; thành một con số không điều kiện; so thẳng nên ra **Đúng** | Không biết "tắt chơi game" có phải trạng thái bình thường không, nên ít nhất phải là Chưa đủ thông tin |
| Quảng cáo tự ghi "10 giờ khi tắt chế độ chơi game" | D1a | D1a là chấp nhận được |

Không phải điều kiện lạ nào cũng quan trọng: "đo trong phòng thí nghiệm" cũng là một điều kiện gắn với con số nhưng chỉ là ngữ cảnh. Phân biệt hai loại này vốn khó, kể cả với người: trong MeasEval, độ đồng thuận giữa người gán nhãn cho Qualifier chỉ là Krippendorff's alpha 0,334, thấp nhất trong các loại nhãn (Quantity 0,943).

## 5. Vì sao lỗi này nghiêm trọng

- FAR là tỷ lệ tuyên bố không đúng bị chấp nhận là Đúng. Tình huống thứ hai ở mục 4 tạo đúng loại lỗi này, nên lỗi làm hỏng chính chỉ số mà đề tài muốn giảm.
- Lỗi xảy ra im lặng: không có cờ, không có thống kê. Trên tập kiểm tra, các hãng không có trong tập phát triển (OPPO; điện thoại, đồng hồ Samsung) là nơi dễ gặp điều kiện lạ nhất.
- Quy tắc "tài liệu chỉ có một con số không kèm điều kiện thì so thẳng" thêm sáng 26/10 làm lỗi dễ xảy ra hơn, vì nó dựa vào việc "không thấy điều kiện" mà chưa phân biệt "không có" với "có nhưng bộ luật không biết".

## 6. Các phương án sửa

| Phương án | Cách làm | Ưu | Nhược |
|---|---|---|---|
| **1. Chặn bảo thủ** | Bước trích xuất ghi **mọi** cụm điều kiện gắn với con số, kèm loại (một trong sáu) và câu trích; cụm không khớp cấu hình ghi vào `dieu_kien_khac`. Giá trị có `dieu_kien_khac` thì điều kiện đó là chưa xác định: quảng cáo khớp giá trị này ra Chưa đủ thông tin, không ra Đúng. "So thẳng" chỉ khi giá trị không kèm cụm điều kiện nào | Giữ FAR an toàn; tất định; ít sửa | Thêm Chưa đủ thông tin; mất các ca Lệch do điều kiện lạ |
| **2. Luật chung cho điều kiện lạ** | Như phương án 1, cộng: nếu tài liệu công bố từ hai giá trị trở lên chỉ khác nhau ở điều kiện lạ, coi đó là các lựa chọn của người dùng và áp "kém thuận lợi nhất": quảng cáo trùng giá trị tốt hơn là Lệch, không cao hơn giá trị kém nhất là Đúng | Lấy lại một phần ca Lệch; vẫn tất định | Có thể chấm Lệch nhầm khi điều kiện lạ là một đại lượng khác (như đàm thoại so với nghe nhạc) chứ không phải lựa chọn |
| **3. Để LLM ghép điều kiện** | LLM quyết định điều kiện lạ có tương đương hay có phải mặc định không | Độ bao phủ cao | Không tất định; khó giữ FAR thấp; lẫn với đối chứng B1, B2 nên làm mờ đóng góp. Kế hoạch đã xếp vào hướng phát triển (T10, câu hỏi 5) |

**Đề xuất:** làm phương án 1 ngay vì là điều kiện cần cho giả thuyết 1. Cài phương án 2 thành tùy chọn, bật hay tắt chọn trên tập phát triển ở Bước 33 như mọi tham số khác. Giữ phương án 3 cho Chương 6.

Đo thêm: tỷ lệ giá trị có `dieu_kien_khac` và tỷ lệ tuyên bố ra Chưa đủ thông tin vì điều kiện lạ, trên tập phát triển, trên bước thử ngoài 12 mẫu, và trên tập kiểm tra. Nhãn chuẩn không phụ thuộc cấu hình (T4.3), nên mọi ca Chưa đủ thông tin do điều kiện lạ đều bị tính là sai trong chỉ số chính; khóa luận vẫn báo trung thực mức thiếu.

## 7. Nhãn Lệch điều kiện có khả thi không

**Bằng chứng từ nghiên cứu liên quan:**

- Nhãn Conflicting Evidence/Cherry-picking của AVeriTeC hiếm (khoảng 4–8% số tuyên bố trong các tập của shared task) và khó: Fathom đạt F1 bằng 0 (đề cương dẫn); một nghiên cứu so sánh nhiều bộ dữ liệu (bản preprint, chưa kiểm bản bình duyệt) báo F1 dưới 0,18 cho mọi mô hình, lỗi tập trung ở ranh giới với Refuted.
- TRACER [4] tăng F1 nửa sự thật tối đa 16 điểm nhờ đoán ý định và phần bị bỏ, tức bài toán "bỏ ngữ cảnh" vẫn khó ngay cả khi có mô-đun riêng.
- MeasEval: điều kiện (Qualifier) là đoạn chữ mở và có độ đồng thuận thấp nhất (alpha 0,334).

**Phần chắc:** khi tài liệu công bố nhiều giá trị ở các điều kiện ghi rõ (Buds3 Pro: 6/7 giờ theo chống ồn; Watch SE 3: 18/32 giờ theo chế độ nguồn), việc con số quảng cáo trùng một giá trị ở điều kiện khác là kiểm được bằng máy, không cần đoán ý định. Đây là điểm khác biệt thật so với AVeriTeC và TRACER, nơi phần bị bỏ không có sẵn trong bằng chứng.

**Phần mong manh:**

- Cách hiểu mặc định là giả định của người làm; khảo sát 20–30 người ở Bước 10 và phân tích độ nhạy ở Bước 37 chỉ giảm, không xóa, rủi ro này.
- Độ đồng thuận của riêng nhãn Lệch chưa biết. Kappa chung cao vẫn có thể che một lớp hiếm có đồng thuận thấp (điều preprint trên chỉ ra với AVeriTeC).
- Số tuyên bố Lệch thật trong quảng cáo do LLM viết chưa biết. Tập cặp tối thiểu tạo từ chính các loại biến đổi trong cấu hình nên luôn nằm trong vùng bộ luật biết; kết quả trên tập này sẽ cao hơn thực tế và phải báo riêng.

**Hệ quả với ba câu hỏi nghiên cứu:** câu 1 (FAR) đứng được kể cả khi nhãn Lệch yếu, miễn là lỗi ở mục 5 được sửa. Câu 2 (F1 nhãn Lệch) là phần rủi ro. Câu 3 (đóng góp của neo nguồn và đối chiếu điều kiện) đo bằng P−ĐK, P−NN, không đổi.

**Đề xuất điểm dừng ở Bước 16** (sau bộ thử), ghi trước vào kế hoạch:

| Tiêu chí | Ngưỡng đề xuất | Nếu không đạt |
|---|---|---|
| Số tuyên bố Lệch không thuộc loại "lên đến" trong bộ thử | ít nhất 10 | Tăng bài sinh theo T9.1; vẫn thiếu thì nhãn Lệch chủ yếu đánh giá trên tập cặp tối thiểu, ghi rõ giới hạn |
| Kappa riêng cho nhãn Lệch giữa người thực hiện và một người thứ hai trên bộ thử | ít nhất 0,6 | Sửa hướng dẫn; vẫn thấp thì chuyển phương án lùi |
| Độ bao phủ cấu hình trên 3 sản phẩm ngoài 12 mẫu | ít nhất 80% cụm điều kiện quyết định được nhận ra | Bổ sung luật từ chính 3 trang đó |

**Phương án lùi** nếu nhãn Lệch không đạt: giữ ba nhãn Đúng, Sai, Chưa đủ thông tin cộng một cờ "thiếu hoặc đổi điều kiện" kèm loại điều kiện. Đóng góp chính (đối chiếu điều kiện làm giảm FAR, lý do chỉ ra điều kiện bị bỏ) vẫn giữ nguyên.

## 8. Phát hiện phụ

**8.1 Điểm 2 (bỏ "lên đến") nên đảo lại.** Báo cáo gốc của FTC (Hastak và Murphy, 2012) chia ngẫu nhiên khoảng 115 người cho mỗi bản quảng cáo cửa sổ: "up to 47%", "47%" không có "up to", và "up to 47%" kèm chú thích mức tiết kiệm trung bình 25%. Kết quả:

| Câu hỏi | "Up to 47%" | "47%" | Khác biệt |
|---|---|---|---|
| Quảng cáo nói tiết kiệm 47% (không nhắc "up to"), câu Q4a | 45,6% | 58,3% | Không có ý nghĩa thống kê (p < 0,05, hai phía) |
| Từ một nửa người dùng trở lên tiết kiệm được khoảng 47%, theo quảng cáo, câu Q4b | 48,2% | 40,9% | Không có ý nghĩa thống kê |
| Như trên, theo ý kiến riêng, câu Q5 | 43,0% | 45,2% | Không có ý nghĩa thống kê |

Nghĩa là chữ "up to" gần như không làm người đọc hiểu khác đi: có hay không có, nhiều người vẫn tin mình đạt mức tối đa. Đề tài so quảng cáo với tài liệu hãng, không đo hiệu năng thực tế (đề cương, Không thuộc phạm vi). Quảng cáo chép "6 giờ" từ "lên đến 6 giờ" vì vậy không gây hiểu sai hơn chính tài liệu, và nên là Đúng, đúng như ví dụ ở đoạn 73 của đề cương. Lý do sáng 26/10 dùng để đổi điểm 2 đã đọc sai hàm ý của nghiên cứu FTC. Đề xuất: đảo lại quyết định; D2 chỉ áp dụng cho từ khẳng định rõ ("luôn", "ít nhất"...), vì các từ này nói một mức sàn bảo đảm, khác hẳn nghĩa với tài liệu. Có thể ghi thêm ghi chú "quảng cáo bỏ 'lên đến'" trong lý do mà không đổi nhãn. Mẫu khoảng 115 người mỗi nhóm nên không loại trừ một khác biệt nhỏ.

**8.2 Chữ "đỉnh", "cực đại" khi chỉ có một con số.** Quy tắc hiện tại coi các chữ này là chế độ hiển thị (điểm 12). Đề xuất làm rõ: nếu tài liệu dùng chữ đó để phân biệt từ hai giá trị trở lên (iPhone 17: "đỉnh" 1600 và 3000 nit) thì là chế độ; nếu chỉ gắn với một giá trị duy nhất (Watch SE 3: "đỉnh 1000 nit") thì hiểu là mức tối đa, tức kiểu giá trị. Cách này áp được cho cả hãng chưa có trong tập phát triển mà không cần khai báo riêng.

## 9. Việc đề xuất (chờ người thực hiện quyết)

1. Thêm luật chặn điều kiện lạ (phương án 1) vào `chung.yaml`, bảng bao phủ mục 1, T10 (điểm mới), Bước 22 (trường `dieu_kien_khac` trong kết quả trích xuất) và Bước 27 (quy tắc và kiểm thử). Phương án 2 thành tùy chọn chọn ở Bước 33.
2. Đảo lại điểm 2 theo mục 8.1; sửa bảng bao phủ, 3 tệp nhóm (kiểu giá trị mặc định của thời lượng pin, thời gian sạc), T10, nhật ký.
3. Làm rõ điểm 12 theo mục 8.2.
4. Ghi điểm dừng Bước 16 và phương án lùi (mục 7) vào kế hoạch.
5. Chạy bước thử độ bao phủ trên 3 sản phẩm ngoài 12 mẫu trước khi sang Bước 9.

## Nguồn

- M. Hastak, D. Murphy, *Effects of a Bristol Windows Advertisement with an "Up To" Savings Claim on Consumer Take-Away and Beliefs*, FTC, 06/2012: https://www.ftc.gov/sites/default/files/documents/reports/effects-bristol-windows-advertisement-savings-claim-consumer-take-away-beliefs/120629bristolwindowsreport.pdf
- C. Harper và cộng sự, *SemEval-2021 Task 8: MeasEval*, 2021 (định nghĩa Qualifier, bảng 1 độ đồng thuận): https://aclanthology.org/2021.semeval-1.38.pdf
- M. Schlichtkrull và cộng sự, *The Automated Verification of Textual Claims (AVeriTeC) Shared Task* (tỷ lệ nhãn): https://arxiv.org/abs/2410.23850
- *How Robust Are Automated Fact-Checking Systems? A Cross-Benchmark Evaluation* (preprint, chưa kiểm bản bình duyệt): https://arxiv.org/abs/2608.25934
- Y. Tang, J. Wang, A. K. H. Tung, *The Missing Parts: Augmenting Fact Verification with Half Truth Detection*, EMNLP 2025: https://arxiv.org/abs/2508.00489
