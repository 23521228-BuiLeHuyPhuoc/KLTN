# Ghi chú tài liệu — Bước 3

Ngày đối chiếu: **15/10/2026**. Dùng để viết Chương 2 và kiểm tra trích dẫn của [đề cương bản cuối](../de_cuong/23521228_BuiLeHuyPhuoc_DeCuongKLTN.pdf). Đây là ghi chú khảo sát có kiểm nguồn, chưa phải chương luận văn hoàn chỉnh.

## 1. Cách đọc và phạm vi

- **“PDF tr. n” là trang thứ n tính từ đầu tệp**, kể cả bìa, bắt đầu từ 1. Liên kết có `#page=n` mở trang tương ứng nếu trình đọc hỗ trợ. Không nhầm số này với số trang kỷ yếu ở chân trang.
- [1]–[16] theo danh mục đề cương hiện tại, không theo bộ sáu bài cũ. Xem [danh mục gốc](../báo/README.md) và [mã băm PDF](../báo/danh_muc.json). Cả 16 tệp đã được đối chiếu SHA-256 với danh mục, không có thay đổi.
- [5] là bản tác giả arXiv:2412.15308v1, không phải PDF phân trang AAAI 308–316; [3] là arXiv v3; [9] là arXiv v1. Khi chuyển sang bản công bố khác phải kiểm lại trang và số liệu.
- Mỗi mục tách **nội dung bài gốc** và **nhận xét vận dụng**. Hạn chế “so với đề tài” là đánh giá của người khảo sát về phạm vi bài, không mặc nhiên là tuyên bố của tác giả.
- Số liệu chỉ có ý nghĩa trong dữ liệu, mô hình, cách chia tập và chỉ số của từng bài. Không xếp hạng các phương pháp bằng cách so trực tiếp các con số ở đây.
- Đã rà phần tổng quan, Bảng 1, tính mới, đóng góp và những đoạn viện dẫn nghiên cứu trong phương pháp của đề cương. Ví dụ thông số sản phẩm và câu viện dẫn luật nằm ngoài kiểm toán bài báo này; phải kiểm riêng bằng nguồn hãng/văn bản chính thức trước khi viết bản luận văn.
- Hồ sơ kiểm trang và phiên bản: [kiem_tra_tai_lieu.json](kiem_tra_tai_lieu.json). Bốn bài khảo sát bổ sung lưu ở [báo/bo_sung](../báo/bo_sung/README.md), không tự đổi số tài liệu của đề cương.

## 2. Đối chiếu các nhận định trong đề cương

Các hàng dưới đây gom những câu diễn đạt cùng một ý; vị trí đều là trang PDF của đề cương. “Cần diễn đạt lại” nghĩa là đã tìm được nguồn để đối chiếu nhưng câu hiện tại thiếu điều kiện hoặc vượt quá kết quả nguồn. Chưa sửa PDF/DOCX đã nộp.

| Vị trí đề cương | Nhận định cần kiểm | Trang nguồn và kết luận đối chiếu |
|---|---|---|
| Tr. 2, bối cảnh; tr. 4, Jiang | LLM bổ sung mô tả sản phẩm có thể sinh thông tin không khớp nguồn | **Có căn cứ.** [1], [PDF tr. 1–3](../báo/%5B1%5D.pdf#page=1): tác giả xét sự trung thành với đầu vào; thông tin không được nguồn hỗ trợ không nhất thiết sai ngoài thực tế. |
| Tr. 2, nghiên cứu FTC 2012 | Người đọc có thể hiểu “up to” thành mức sẽ đạt | **Có căn cứ trong miền khảo sát cụ thể.** Báo cáo Hastak–Murphy, [PDF tr. 3–7](https://search.ftc.gov/sites/default/files/documents/reports/effects-bristol-windows-advertisement-savings-claim-consumer-take-away-beliefs/120629bristolwindowsreport.pdf#page=3), khảo sát quảng cáo cửa sổ tiết kiệm năng lượng tại Mỹ. Xem mục 4.5; không suy rộng trực tiếp sang mọi người mua Việt Nam. |
| Tr. 2, FEVER; Bảng 1 tr. 4 | Khoảng 185 nghìn tuyên bố sửa từ Wikipedia; ba nhãn và bằng chứng | **Đúng:** 185.445 tuyên bố; [2], [PDF tr. 1](../báo/%5B2%5D.pdf#page=1), quy trình tạo/gán nhãn ở tr. 3–4. |
| Tr. 2, FEVER | Cách chia ba nhãn được “phần lớn” nghiên cứu sau dùng lại | **Cần thu hẹp.** [5] tr. 3–4, [6] tr. 3, [7] tr. 4–5 cho thấy các ví dụ kế thừa; không có thống kê toàn bộ lĩnh vực để chứng minh “phần lớn”. Nên viết “được nhiều bộ dữ liệu tiếp nối, như …”. |
| Tr. 2, AVeriTeC; Bảng 1 tr. 4 | Gần 4.600 tuyên bố thật; nhãn Conflicting Evidence/Cherry-picking | **Đúng:** 4.568 tuyên bố từ 50 tổ chức; [3], [PDF tr. 1, 3–4](../báo/%5B3%5D.pdf#page=3). Nhãn gộp cả xung đột bằng chứng và bỏ ngữ cảnh gây hiểu nhầm. |
| Tr. 2, Tang | Khoảng 15 nghìn phát biểu; TRACER suy ý định và đánh giá thông tin bị bỏ | **Đúng có điều kiện:** 14.994 mẫu, quy trình bán tự động có kiểm tra người; [4], [PDF tr. 4–6](../báo/%5B4%5D.pdf#page=4). Không gọi đây là bộ được gán toàn bộ thủ công. |
| Tr. 2, Tang | F1 Half-True tăng đến 16 điểm | **Đúng:** HiSS trên test tăng 44,4 → 60,5, tức **16,1 điểm F1** trên thang 100; [4], [PDF tr. 7–8, Bảng 8](../báo/%5B4%5D.pdf#page=8). Không phải mức tăng của mọi backbone. |
| Tr. 3, ViFactCheck | 7.232 cặp, 12 chủ đề, Gemma macro-F1 89,9% | **Bổ sung thiết lập:** [5], [PDF tr. 3–5](../báo/%5B5%5D.pdf#page=3), Bảng 3 tr. 5. **Gemma tinh chỉnh + Evidence: 89,90%; Context: 85,94%.** Không phải kết quả gọi API zero-shot hoặc toàn quy trình truy hồi. |
| Tr. 3, ViNumFCR | Hơn 10 nghìn mẫu tin tức chứa số liệu | **Đúng:** 10.008 cặp; [6], [PDF tr. 3–5](../báo/%5B6%5D.pdf#page=3), Bảng 4 tr. 5. Có thao tác số và suy luận ngôn ngữ; không phải mẫu nào cũng là bài toán tính số học nhiều bước. |
| Tr. 3, SemViQA | Truy hồi ngữ nghĩa, phân loại hai bước, hạng nhất UIT | **Có căn cứ:** [7], [PDF tr. 4–7](../báo/%5B7%5D.pdf#page=4), Bảng 2–3. Nên viết “kết hợp TF-IDF với QATC” vì hệ thống vẫn dùng khớp từ, không loại bỏ nó hoàn toàn. |
| Tr. 3, NumPert | Sửa con số có kiểm soát, độ chính xác giảm đến 62% | **Cần diễn đạt lại:** abstract [8], tr. 1 có con số 62%, nhưng [Bảng 2, PDF tr. 5](../báo/%5B8%5D.pdf#page=5) báo chênh lệch accuracy theo **điểm phần trăm**, và có mức giảm lớn hơn 62. Không dùng 62% như mức giảm tối đa chung. Xem mục 3.8. |
| Tr. 3, VeriFin | XBRL, công thức, Z3; 600 câu/28 công ty; 0 so với 6–92 chấp nhận sai | **Đúng trong thí nghiệm:** [9], [PDF tr. 1, 3–7](../báo/%5B9%5D.pdf#page=6), Hình 4. Trong nhóm so sánh, 92 là **Direct LLM nhận tất cả, không có bước kiểm chứng**; các bộ kiểm chứng còn lại: 26, 75, 6. Không biến 0 quan sát thành bảo đảm tuyệt đối. |
| Tr. 3, FactLens; tr. 10, tách tuyên bố | Tách nhỏ nhưng giữ nghĩa/ngữ cảnh, có người kiểm và thước đo chất lượng | **Đúng:** [10], [PDF tr. 2–4](../báo/%5B10%5D.pdf#page=2), gán nhãn tr. 10. Ví dụ biến một điều kiện thành khẳng định độc lập được chỉ ra ở tr. 3. |
| Tr. 3, MiniCheck | Mô hình nhỏ huấn luyện tổng hợp, ngang GPT-4, rẻ khoảng 400 lần | **Cần ghi rõ phạm vi:** [11], [PDF tr. 7–8, Bảng 2–4](../báo/%5B11%5D.pdf#page=7): MiniCheck-FT5 BAcc 74,7, GPT-4 75,3; chi phí suy luận 0,24 USD so với 107 USD trên khoảng 13K mẫu. Đây là BAcc và giá theo thiết lập bài, không phải giá API hiện tại. |
| Tr. 3, Nguyen | Facebook tiếng Việt; GPT-3.5 trích thông tin, so cổng y tế TP.HCM | **Đúng về quy trình:** [12], [PDF tr. 3–6](../báo/%5B12%5D.pdf#page=3). Nhãn là vi phạm/không vi phạm theo tiêu chí giấy phép và dịch vụ của nghiên cứu, không phải bốn nhãn thông số của đề tài. |
| Tr. 3, Nguyen | F1 0,703 trên 1.175 bài | **Đúng:** dữ liệu [12] tr. 6; [Bảng 2, PDF tr. 8](../báo/%5B12%5D.pdf#page=8), BGE-M3, ngưỡng 0,4: accuracy 0,783, precision 0,686, F1 0,703. Không tự gọi chỉ số này là macro-F1 hoặc hiệu năng một tập test độc lập nếu chưa có mô tả tương ứng. |
| Tr. 4, Jiang | Lọc rẻ rồi LLM xác nhận; khó với thuộc tính tự do | **Đúng:** [1], [PDF tr. 3–8](../báo/%5B1%5D.pdf#page=6). Bảng kết quả chuẩn hóa theo mục tiêu nội bộ p/r/f1, không phải các tỷ lệ tuyệt đối. |
| Tr. 4, Fathom; Bảng 1; tr. 7 | F1 bằng 0 ở Conflicting/Cherry-picking trên dev AVeriTeC | **Đúng:** [13], [PDF tr. 5, Bảng 3](../báo/%5B13%5D.pdf#page=5), F1 = 0,0000. Không suy ra toàn bộ hệ thống hoặc mọi hệ thống bốn nhãn đều thất bại. |
| Tr. 4–5, Bảng 1 | Các bài chưa biểu diễn sáu loại điều kiện như P | **Nhận xét phạm vi, cần giới hạn.** Đối chiếu đặc tả: [2] tr. 3–4; [3] tr. 3–4, 7–8; [4] tr. 5–6; [5] tr. 3–5; [6] tr. 3–7; [7] tr. 4–5; [8] tr. 3; [9] tr. 3–4; [11] tr. 2; [12] tr. 3–6; [13] tr. 3–5. Chỉ kết luận về các hệ thống đã khảo sát, không khẳng định cả lĩnh vực không xét điều kiện. |
| Tr. 4, Tang | Phải đoán thông tin bị bỏ | **Cần chính xác hơn:** [4], [PDF tr. 5–6](../báo/%5B4%5D.pdf#page=5). TRACER nhận **bằng chứng có sẵn**, căn chỉnh phần không được trình bày, suy ý định/giả định rồi tìm bằng chứng ẩn quan trọng; không phải tự bịa toàn bộ ngữ cảnh không có nguồn. |
| Tr. 4, VeriFin | “Chỉ làm được” khi dữ liệu đã là bảng | **Quá tuyệt đối:** [9], [PDF tr. 3–5, 7](../báo/%5B9%5D.pdf#page=3) dùng dữ kiện XBRL nhưng cũng cho phép công thức được xác lập từ câu hỏi, registry hoặc disclosure text và thử FinanceBench. Nên viết “được thiết kế cho miền tài chính với dữ kiện và phép tính được neo vào nguồn có cấu trúc”. |
| Tr. 4, 6, tính mới | Chưa có nghiên cứu/bộ dữ liệu cho bài toán này | **Kết luận khảo sát có phạm vi.** Các bài dưới đây chưa cung cấp đúng tổ hợp quảng cáo tiếng Việt + thông số có điều kiện + quy tắc bốn nhãn của đề tài. Không có một trang nguồn đơn lẻ chứng minh “chưa có trên toàn thế giới”; nên giữ “trong các tài liệu đã khảo sát đến 15/10/2026”. |
| Tr. 6–7, MeasEval | Sáu loại điều kiện là phần áp dụng lược đồ MeasEval | **Có cơ sở tham khảo, không phải kế thừa nguyên xi:** [14], [PDF tr. 2–3](../báo/%5B14%5D.pdf#page=2) có Quantity, Unit, Modifier, MeasuredEntity, MeasuredProperty, Qualifier. **Sáu loại điều kiện và quy tắc A–D là thiết kế của đề tài.** |
| Tr. 7, VitaminC | Tập cặp tối thiểu dựa trên ý tưởng cặp tương phản | **Đúng ở mức ý tưởng:** [15], [PDF tr. 3–4](../báo/%5B15%5D.pdf#page=3). VitaminC chủ yếu đổi **bằng chứng** và theo dõi nhãn; đề tài đổi **tuyên bố** với nguồn cố định, cần nói rõ khác biệt này. |
| Tr. 7, cải tiến | Ba nhãn dễ chấp nhận đúng số/sai điều kiện; P giảm FAR/tăng F1 | **Giả thuyết của đề tài, chưa là kết quả.** [2], [5], [7] xác nhận hệ nhãn, không chứng minh chúng tất yếu nhận sai. Bộ ba nhãn vẫn có thể bác bỏ hoặc trả NEI khi điều kiện không khớp; lợi ích tách LECH phải được đo bằng đối chứng. |
| Tr. 7, cải tiến | So với [12], [1], [11]: P kiểm từng tuyên bố, so khớp theo điều kiện thay vì theo độ tương đồng, nên phân biệt được sai giá trị với lệch điều kiện | **Đúng một phần, cần nói riêng từng bài.** [12], [PDF tr. 4–5](../báo/%5B12%5D.pdf#page=5): so danh mục kỹ thuật bằng cosine trên embedding BGE-M3 với ngưỡng, nhãn ở cấp bài; “theo độ tương đồng” đúng với bài này. [1], [PDF tr. 3–5](../báo/%5B1%5D.pdf#page=3): tầng LSS lọc bằng ROUGE/BLEU/METEOR và embedding, sau đó LLM xác nhận; đơn vị kiểm là thuộc tính. [11], [PDF tr. 1–2](../báo/%5B11%5D.pdf#page=2): MiniCheck là bộ phân loại cấp câu, đã kiểm từng câu và không so theo độ tương đồng; điểm khác thật là hai nhãn Supported/Unsupported không tách SAI/LECH/CHUA_DU. Nên viết: “[12] so khớp theo độ tương đồng, [1] lọc bằng độ tương đồng rồi để LLM xác nhận, [11] phân loại từng câu theo hai nhãn; cả ba chưa tách sai giá trị với lệch điều kiện.” Việc P tách được hai loại lỗi này vẫn là giả thuyết, phải đo. |
| Tr. 10, BM25/Fathom | BM25 truy hồi nền, tham khảo tầng đầu Fathom | **Đúng:** [16], [PDF tr. 28–31](../báo/%5B16%5D.pdf#page=30), đặc biệt công thức (3.15); [13], [PDF tr. 3–4, mục 4.2](../báo/%5B13%5D.pdf#page=3). Fathom còn có HyDE-QA và dense reranking; P không phải bản tái lập toàn hệ thống này. |
| Tr. 12, Bảng 2 | B0 “đại diện kiểm chứng ba nhãn phổ biến [2]”; B2 “theo cách đặt nhãn của AVeriTeC [3]”; B3 “mô hình ba nhãn tiếng Việt đã huấn luyện sẵn của SemViQA [7]” | **B0 đúng, giữ cách nói hẹp:** [2], [PDF tr. 1, 3](../báo/%5B2%5D.pdf#page=1) định nghĩa Supported/Refuted/NotEnoughInfo; chữ “phổ biến” dùng cùng căn cứ và cùng giới hạn với hàng FEVER tr. 2 ở trên. **B2 đúng ở mức cảm hứng:** [3], [PDF tr. 3–4](../báo/%5B3%5D.pdf#page=3) có nhãn thứ tư Conflicting Evidence/Cherry-picking; LECH của đề tài hẹp hơn, nguồn mâu thuẫn có thể thuộc CHUA_DU (mục 3.3). B2 không tái lập baseline AVeriTeC; tr. 7 cũng gắn AVeriTeC với B2, hai chỗ khớp nhau. **B3 cần kiểm thêm ngoài PDF:** [7], [PDF tr. 1](../báo/%5B7%5D.pdf#page=1) chỉ nói mã nguồn có trên GitHub; [PDF tr. 4–5](../báo/%5B7%5D.pdf#page=4) mô tả mô hình ba nhãn huấn luyện trên ISE-DSC01 (tin tức) và ViWikiFC (Wikipedia). Bài không nói có phát hành trọng số, nên trước Bước 30 phải kiểm repo; nếu không có trọng số thì phải tự huấn luyện lại và ghi rõ. B3 chạy ngoài miền huấn luyện khi áp vào quảng cáo thông số. |

## 3. Ghi chú 16 tài liệu chính

### 3.1. [1] Jiang và cộng sự — Hallucination Detection in LLM-enriched Product Listings (2024)

Nguồn: [PDF gốc](../báo/%5B1%5D.pdf), [ACL Anthology](https://aclanthology.org/2024.ecnlp-1.4/).

- **Bài toán:** phát hiện giá trị LLM thêm vào mô tả sản phẩm nhưng không trung thành với dữ liệu đầu vào; phân biệt vấn đề này với sự đúng/sai ngoài thực tế. PDF tr. 1–3, mục 1–2.1.
- **Dữ liệu và nhãn:** DS có 200 listings/2.765 entries thuộc tính có cấu trúc; DU có 4.042 listings/12.126 entries thuộc tính tự do. Chuyên gia miền kiểm và gán nhãn ảo giác ở cấp thuộc tính. PDF tr. 6, mục 4.1, Bảng 1–2.
- **Phương pháp:** Lexical and Semantic Screening lọc ứng viên bằng các phép so khớp rẻ; LLM xác nhận ứng viên. PDF tr. 3–5, mục 3.
- **Kết quả:** thuộc tính ngắn, xác định rõ dễ xử lý hơn mô tả dài; precision trên DU thấp và phụ thuộc cách hiểu suy luận thường thức. PDF tr. 6–8, Bảng 3–6, mục 4.3. Kết quả dùng P/p, R/r, F1/f1 theo mục tiêu nội bộ; không diễn giải 1,09 thành F1 109%.
- **Vận dụng/hạn chế so với đề tài:** học cách đối chiếu với nguồn riêng của sản phẩm; chưa có bộ quy tắc tách sai giá trị và lệch điều kiện của thông số. Không coi mọi thông tin không có trong nguồn là SAI.

### 3.2. [2] Thorne và cộng sự — FEVER (2018)

Nguồn: [PDF gốc](../báo/%5B2%5D.pdf), [ACL Anthology](https://aclanthology.org/N18-1074/).

- **Bài toán/dữ liệu:** 185.445 tuyên bố tạo và biến đổi từ Wikipedia; tìm bằng chứng rồi gán Supported, Refuted hoặc Not Enough Info. PDF tr. 1, 3.
- **Gán nhãn:** tách công đoạn tạo câu và xác minh; người xác minh đánh dấu câu bằng chứng cho Supported/Refuted. Có kiểm tra nhiều người, Fleiss κ = 0,6841. PDF tr. 3–4, mục 3.1–3.4.
- **Phương pháp:** truy hồi tài liệu, chọn câu, mô hình nhận diện quan hệ suy diễn. PDF tr. 6–7, mục 5.
- **Kết quả:** baseline báo 31,87% khi cần nhãn và bằng chứng đúng, 50,91% nếu bỏ yêu cầu bằng chứng; PDF tr. 1–2, kết quả test chi tiết tr. 8. Bảng dev tr. 7 là thiết lập khác, không tráo với số test.
- **Vận dụng/hạn chế:** học cách lưu bằng chứng và đánh giá truy hồi riêng. Ba nhãn không phân biệt nguyên nhân “sai số” với “lệch điều kiện”, nhưng không có nghĩa mô hình ba nhãn không thể phát hiện điều kiện sai. Dữ liệu Wikipedia nhân tạo khác quảng cáo sản phẩm.

### 3.3. [3] Schlichtkrull và cộng sự — AVeriTeC (2023, arXiv v3)

Nguồn: [PDF gốc](../báo/%5B3%5D.pdf), [arXiv](https://arxiv.org/abs/2305.13117).

- **Bài toán/dữ liệu:** 4.568 tuyên bố thật từ 50 tổ chức kiểm chứng; bằng chứng web biểu diễn bằng cặp hỏi–đáp, có URL, lý do và thông tin thời điểm. PDF tr. 1, 3–4.
- **Nhãn:** Supported, Refuted, Not Enough Evidence, Conflicting Evidence/Cherry-picking. Nhãn cuối gồm cả nguồn xung đột và tuyên bố đúng kỹ thuật nhưng bỏ ngữ cảnh quan trọng. PDF tr. 3–4, mục 3.
- **Gán nhãn:** người khác nhau trích câu, tìm/viết hỏi–đáp và kiểm tra tính đủ của bằng chứng; bất đồng phải làm lại hoặc loại mẫu. PDF tr. 4–5, mục 4.
- **Phương pháp/kết quả:** baseline tìm kiếm, tạo hỏi–đáp, xếp hạng và phân loại; AVeriTeC-BLOOM-7b đạt AVeriTeC score 0,15 tại ngưỡng bằng chứng λ = 0,25. PDF tr. 7–8, Bảng 3. Đây không phải accuracy chỉ xét nhãn.
- **Vận dụng/hạn chế:** tham khảo lớp gây hiểu nhầm và sự đầy đủ bằng chứng. Không đồng nhất nhãn cuối với LECH: trong đề tài, nguồn mâu thuẫn có thể thuộc CHUA_DU. B2 là đối chứng lấy cảm hứng về nhãn, không tái lập baseline AVeriTeC nguyên bản.

### 3.4. [4] Tang và cộng sự — The Missing Parts / TRACER (2025)

Nguồn: [PDF gốc](../báo/%5B4%5D.pdf), [ACL Anthology](https://aclanthology.org/2025.emnlp-main.1724/).

- **Bài toán:** phát hiện nửa sự thật: nội dung được nói có thể đúng nhưng thông tin bị bỏ làm thay đổi cách hiểu. PDF tr. 1–3.
- **Dữ liệu/nhãn:** PolitiFact-Hidden có 14.994 mẫu; gộp True → True, Mostly True/Half-True → Half-True, các mức còn lại → False. PDF tr. 4, Bảng 2–3.
- **Gán nhãn:** GPT-4o-mini hỗ trợ đánh dấu bằng chứng được trình bày/ẩn và suy ý định, kết hợp kiểm chất lượng bởi người; không phải 14.994 ý định đều do người viết. PDF tr. 4–5.
- **Phương pháp:** căn chỉnh bằng chứng, suy ý định, đánh giá giả định phản thực để tìm Critical Hidden Evidence, rồi xét lại nhãn. PDF tr. 5–6, mục 5.
- **Kết quả:** HiSS + TRACER tăng F1 Half-True test từ 44,4 lên 60,5; macro-F1 từ 59,4 lên 65,7. PDF tr. 7–8, Bảng 7–8.
- **Vận dụng/hạn chế:** củng cố nhu cầu kiểm phần bị bỏ. Đề tài thử thay suy ý định mở bằng danh mục điều kiện thông số và quy tắc xác định trước; hiệu quả tốt hơn vẫn phải thực nghiệm.

### 3.5. [5] Hoa và cộng sự — ViFactCheck (bản tác giả 2024, bài AAAI 2025)

Nguồn: [PDF arXiv đã lưu](../báo/%5B5%5D.pdf), [arXiv v1](https://arxiv.org/abs/2412.15308v1).

- **Bài toán/dữ liệu:** 7.232 mẫu kiểm chứng tiếng Việt, 12 chủ đề từ báo điện tử. PDF tr. 1, 3 và 12. **Nguồn là tin tức, không phải Wikipedia**; Bảng 1 của bài phân biệt rõ với ViWikiFC.
- **Gán nhãn:** người tạo tuyên bố và chọn bằng chứng, ba nhãn Support/Refute/NEI; kiểm tra chéo chất lượng. PDF tr. 3–4, phụ lục tr. 10–12.
- **Phương pháp:** so mô hình tiền huấn luyện, prompting và tinh chỉnh LLM; thử với toàn ngữ cảnh và với bằng chứng. PDF tr. 4–5.
- **Kết quả:** Gemma đã tinh chỉnh đạt macro-F1 **89,90% với Evidence**, **85,94% với Context**, Bảng 3, PDF tr. 5; giải thích macro-F1 và kết quả tổng kết ở tr. 7. Không gán số này cho Gemini hay một cuộc gọi Gemma chưa tinh chỉnh.
- **Vận dụng/hạn chế:** tham khảo nhãn, hướng dẫn và thiết kế kiểm tra bằng chứng tiếng Việt. Không trực tiếp đo tính đúng của điều kiện vận hành sản phẩm; cần dữ liệu miền quảng cáo riêng.

### 3.6. [6] Luong và cộng sự — ViNumFCR (2025)

Nguồn: [PDF gốc](../báo/%5B6%5D.pdf), [ACL Anthology](https://aclanthology.org/2025.inlg-main.9/).

- **Bài toán/dữ liệu:** 10.008 cặp chứa số liệu thuộc 12 chủ đề tin tức; nguồn VnExpress. PDF tr. 3–5, Bảng 4.
- **Gán nhãn:** người tạo Supported/Refuted/NEI và bằng chứng; năm người kiểm chéo các cặp không do mình viết, loại mẫu không đạt ít nhất ba phiếu giống nhau. PDF tr. 3–4.
- **Phương pháp:** mô hình ngôn ngữ cho phân loại, BM25/SBERT/TF-IDF cho truy hồi. PDF tr. 6–7.
- **Kết quả:** XLM-RLarge tinh chỉnh đạt accuracy test 90,05%, F1 90,06; Gemma-2 tinh chỉnh đạt accuracy 88,96%. PDF tr. 7, Bảng 6. Không kết luận mọi LLM đều kém từ riêng zero/few-shot.
- **Điểm cần kiểm:** Bảng 7 cùng trang ghi BM25 P = 97,40, R = 90,47 nhưng F1 = 99,80; nếu cùng cách gộp thông thường thì không nhất quán. Không dùng 99,80 làm số liệu trích chắc chắn. Đã kiểm trực tiếp ảnh trang, không phải lỗi trích text.
- **Vận dụng/hạn chế:** học cách tạo biến thể số và kiểm nhãn chéo; nhãn thông thường chưa tách riêng nguyên nhân lệch điều kiện sản phẩm.

### 3.7. [7] Tran và cộng sự — SemViQA (2026)

Nguồn: [PDF gốc](../báo/%5B7%5D.pdf), [ACL Anthology](https://aclanthology.org/2026.acl-industry.94/).

- **Bài toán/dữ liệu/nhãn:** kiểm chứng tiếng Việt trên ISE-DSC01 và ViWikiFC, ba nhãn Supported/Refuted/NEI; dùng dữ liệu đã có, không phải bài giới thiệu bộ nhãn thông số mới. PDF tr. 4–5, Bảng 1.
- **Phương pháp:** chia ngữ cảnh dài thành đoạn khoảng 400 token; TF-IDF xử lý trường hợp dễ, QATC chọn bằng chứng cho trường hợp khó. Phân loại ba lớp rồi phân biệt Supported/Refuted, kết hợp điểm tin cậy. PDF tr. 4–5, mục 3.
- **Kết quả:** strict accuracy 78,97% trên ISE-DSC01 và 80,82% trên ViWikiFC; cấu hình backbone đạt đỉnh có thể khác nhau giữa hai tập. PDF tr. 6, Bảng 2. Kết quả đứng đầu leaderboard UIT nằm ở tr. 7, Bảng 3.
- **Vận dụng/hạn chế:** tách đo lỗi truy hồi và gán nhãn, giữ ngữ cảnh khi chia đoạn. Đây là hệ thống kết hợp khớp từ và ngữ nghĩa; không thể mô tả là chỉ dùng ngữ nghĩa. Chưa đánh giá riêng điều kiện thông số.

### 3.8. [8] Aarnes và Setty — NumPert (2025)

Nguồn: [PDF gốc](../báo/%5B8%5D.pdf), [ACL Anthology](https://aclanthology.org/2025.ijcnlp-srw.8/).

- **Bài toán/dữ liệu:** kiểm độ vững trước thay đổi số trên QuanTemp; dùng 260 câu True và 604 câu False ban đầu, bỏ lớp Conflicting. PDF tr. 3, Bảng 1.
- **Tạo nhãn/biến thể:** sáu nhóm Num, Approx, Range, Mask, Rand-Repl, Neg-Num; phân biệt phép giữ nhãn và đổi True → False, có kiểm thủ công tính hợp lệ. PDF tr. 3–4. Đây không phải biến đổi số tùy ý rồi mặc định mọi câu đều sai.
- **Kết quả:** Bảng 2, PDF tr. 5 cho thấy ảnh hưởng rất khác nhau theo phép sửa, model và prompt. Ví dụ GPT-4o-Mini ở two-shot, Neg-num: accuracy **89,62% → 27,45%**; bảng ghi −62,16 (chênh khoảng 62,17 nếu tính từ hai số đã làm tròn). GPT-4o zero-shot, Mask: **80,00% → 19,25%**, giảm 60,75 điểm phần trăm.
- **Sửa cách trích:** abstract tr. 1 viết mức giảm tới 62%, nhưng Bảng 2 có mức lớn hơn, như 74,12 điểm ở GPT-4o-Mini zero-shot/Mask. Nên trích một dòng cụ thể kèm thiết lập hoặc nói “giảm mạnh”, không lấy 62 làm trần chung.
- **Vận dụng/hạn chế:** tạo cặp kiểm thử số/đơn vị/điều kiện, kiểm lại nhãn từng biến thể. Kết quả không chứng minh mọi so sánh số đều cần bộ giải ký hiệu.

### 3.9. [9] Hall và cộng sự — VeriFin (2026, tiền công bố arXiv v1)

Nguồn: [PDF gốc](../báo/%5B9%5D.pdf), [arXiv](https://arxiv.org/abs/2608.10213).

- **Bài toán:** kiểm câu trả lời tài chính bằng dữ kiện, kỳ, đơn vị và phép tính có nguồn; Z3 kiểm ràng buộc. PDF tr. 1, 3–4.
- **Dữ liệu/đáp án:** XBRLFiling gồm 600 câu, 28 công ty; tạo từ quan hệ tính toán trong báo cáo XBRL, đáp án truy ngược được tới giá trị công bố. Có thêm 67 câu số liệu FinanceBench. PDF tr. 4–5. Đây không phải gán nhãn quảng cáo bằng người.
- **Phương pháp:** tách câu trả lời ứng viên khỏi nguồn xác định dữ kiện/công thức; trả Verified/Violated/Abstain và dấu vết ràng buộc. PDF tr. 3–4.
- **Kết quả:** trên nhóm câu ứng viên Claude Haiku 4.5, XBRLFiling có FA = 0, nhưng từ chối 46 câu đúng và abstain 7/600, coverage 98,8%; FinanceBench coverage 80,6%. PDF tr. 6–7, Hình 4. Mức 6–92 FA của đối chứng gồm cả Direct LLM không xác minh.
- **Vận dụng/hạn chế:** neo nguồn trước quyết định và báo cả FA lẫn giữ được câu đúng. Không mô tả Z3 tự hiểu văn bản hay bảo đảm toàn hệ thống không sai; tính tất định phụ thuộc dữ kiện/công thức đã được xác lập đúng. P dùng quy tắc điều kiện, không nhất thiết phải dùng Z3.

### 3.10. [10] Mitra và cộng sự — FactLens (2025)

Nguồn: [PDF gốc](../báo/%5B10%5D.pdf), [ACL Anthology](https://aclanthology.org/2025.findings-acl.929/).

- **Bài toán:** kiểm chất lượng tách câu phức tạp thành đơn vị có thể xác minh độc lập. PDF tr. 2–3.
- **Dữ liệu/gán nhãn:** 733 mẫu CoverBench, LLM tạo ứng viên, người rà và sửa sub-claims; dùng bằng chứng có sẵn để giảm nhiễu do truy hồi. PDF tr. 4; hai chuyên gia và hướng dẫn chấm ở tr. 10.
- **Phương pháp:** chấm atomicity, sufficiency, fabrication, coverage, redundancy, readability; điểm low/medium/high, ở cấp câu con hoặc toàn bộ phép tách. PDF tr. 2–3.
- **Kết quả:** tương quan bộ chấm với người không đồng đều; sufficiency thấp (Pearson 0,14, Spearman 0,09 cho LLM evaluator), Bảng 1, PDF tr. 3. Quan hệ chất lượng tách–kiểm chứng được phân tích ở tr. 4–5 và 10–12.
- **Vận dụng/hạn chế:** giữ sản phẩm, phiên bản và điều kiện; không sửa một phát biểu sai thành đúng trong bước tách. Ví dụ biến mệnh đề điều kiện thành sự kiện là fabrication, tr. 3. Không dùng bộ chấm LLM làm nhãn chuẩn của khóa luận, cũng không mặc định tách càng nhỏ càng tốt.

### 3.11. [11] Tang, Laban và Durrett — MiniCheck (2024)

Nguồn: [PDF gốc](../báo/%5B11%5D.pdf), [ACL Anthology](https://aclanthology.org/2024.emnlp-main.499/).

- **Bài toán/nhãn:** cho tài liệu và câu, phân loại Supported/Unsupported; Unsupported gộp không được hỗ trợ và mâu thuẫn. PDF tr. 2, mục 2; cách chuyển nhãn ANLI ở tr. 5.
- **Dữ liệu/gán nhãn:** sinh dữ liệu huấn luyện có kiểm soát bằng GPT-4, kết hợp dữ liệu entailment. Đánh giá LLM-AGGREFACT tổng hợp 10 bộ có nhãn người, khoảng 13K mẫu test. PDF tr. 3–7.
- **Kết quả:** MiniCheck-FT5 770M đạt BAcc trung bình 74,7 so với GPT-4 75,3, không tinh chỉnh ngưỡng từng tập; Bảng 2–3, PDF tr. 7. Chi phí 0,24 USD so với 107 USD, tỷ lệ khoảng 446 lần, theo quy đổi GPU/API của bài; Bảng 3–4, tr. 7–8.
- **Kết quả cần nhớ thêm:** tách câu không cải thiện nhất quán trong thiết lập này; MiniCheck-FT5 giảm 1,4 điểm BAcc khi tách, Bảng 5, tr. 8.
- **Vận dụng/hạn chế:** tham khảo bộ phân loại dựa nguồn và đối chứng chi phí; hai nhãn không phân biệt LECH/SAI/CHUA_DU. Không lấy kết quả chi phí năm 2024 làm dự toán hiện tại, không dùng bài để khẳng định tách câu luôn có lợi.

### 3.12. [12] Nguyen và cộng sự — Fact-checking for Online Advertisement Posts (2024)

Nguồn: [PDF gốc](../báo/%5B12%5D.pdf), [ACL Anthology](https://aclanthology.org/2024.paclic-1.40/).

- **Bài toán/dữ liệu:** 1.175 bài quảng cáo Facebook của 283 cơ sở làm đẹp/thẩm mỹ; dữ liệu tham chiếu từ cổng hoạt động y tế TP.HCM. PDF tr. 3, 6.
- **Nhãn:** 929 không vi phạm, 246 vi phạm; nhãn xây bằng đối chiếu dịch vụ quảng cáo với danh mục được phép theo quy trình bài. PDF tr. 6, mục 4.2–4.3. Đây là nhãn cấp bài, không phải đánh giá từng thông số có điều kiện.
- **Phương pháp:** GPT-3.5 Turbo trích thông tin; kiểm giấy phép/địa chỉ và so độ tương đồng danh mục kỹ thuật. PDF tr. 3–6.
- **Kết quả:** BGE-M3 ngưỡng 0,4: accuracy 0,783, precision 0,686, F1 0,703; Bảng 2, PDF tr. 8. Không tự gắn thêm kiểu macro/micro/weighted khi nguồn chưa làm rõ.
- **Vận dụng/hạn chế:** tiền lệ gần về quảng cáo tiếng Việt, LLM trích và đối chiếu nguồn chính thức. P đổi đơn vị kiểm chứng sang tuyên bố và kiểm điều kiện thông số; không dùng nghiên cứu này làm căn cứ tự động kết luận pháp lý cho quảng cáo điện tử.

### 3.13. [13] Rashid và Hakak — Fathom (2025)

Nguồn: [PDF gốc](../báo/%5B13%5D.pdf), [ACL Anthology](https://aclanthology.org/2025.fever-1.20/).

- **Bài toán/dữ liệu/nhãn:** hệ thống cho AVeriTeC, dùng bốn nhãn đã có; không giới thiệu nhãn người mới. Phân bố dev có 38 câu Conflicting Evidence/Cherry-picking, PDF tr. 2, Bảng 1.
- **Phương pháp:** sinh HyDE-QA, BM25 lấy ứng viên, xếp hạng lại bằng embedding, LLM dự đoán nhãn. Chia đoạn và giữ tham chiếu đoạn lân cận. PDF tr. 3–4, mục 4.
- **Kết quả:** dev: F1 Supported 0,6877, Refuted 0,8436, NEI 0,1455, CP/CE **0,0000**, macro-F1 0,4192, accuracy 0,7200. PDF tr. 5, Bảng 3. Không nhầm macro-F1 với AVeriTeC score ở Bảng 2.
- **Vận dụng/hạn chế:** tham khảo tầng truy hồi và báo riêng lớp khó. P chỉ mượn BM25 nền, không có nghĩa đã tái lập Fathom. Kết quả một lớp của một hệ thống là động lực khảo sát, không phải bằng chứng rằng bốn nhãn hoặc RAG nói chung không hiệu quả.

### 3.14. [14] Harper và cộng sự — MeasEval (2021)

Nguồn: [PDF gốc](../báo/%5B14%5D.pdf), [ACL Anthology](https://aclanthology.org/2021.semeval-1.38/).

- **Bài toán:** trích số đo cùng đơn vị, loại giá trị, đối tượng, thuộc tính, thông tin bổ nghĩa và quan hệ; có quan hệ xuyên câu. PDF tr. 2–3, mục 3–4.1.
- **Dữ liệu/gán nhãn:** từ 110 bài khoa học; ít nhất hai người gán, họp phân xử, có thể thêm người thứ ba. PDF tr. 3, mục 4.2. Đây là nhãn span/quan hệ, không phải nhãn đúng/sai tuyên bố.
- **Kết quả:** đội LIORI đạt overall F1 0,519; riêng Qualifier 0,163, Bảng 2, PDF tr. 5. Krippendorff α của Qualifier là 0,334 trong tập đo đồng thuận, Bảng 1, tr. 3: ngữ cảnh số đo không dễ gán nhất quán.
- **Vận dụng/hạn chế:** cơ sở để giữ giá trị đi cùng điều kiện/đối tượng và câu nguồn. MeasEval không định nghĩa sẵn sáu loại điều kiện sản phẩm, không chuẩn hóa mọi số đo và không đưa quy tắc A–D. Danh mục điều kiện bắt buộc của đề tài cần viết, dẫn nguồn hãng và kiểm riêng.

### 3.15. [15] Schuster, Fisch và Barzilay — VitaminC (2021)

Nguồn: [PDF gốc](../báo/%5B15%5D.pdf), [ACL Anthology](https://aclanthology.org/2021.naacl-main.52/).

- **Bài toán:** mô hình phải nhạy với thay đổi bằng chứng làm đổi sự thật, thay vì dựa vào nhớ sẵn hoặc trùng từ. PDF tr. 1–3.
- **Dữ liệu/gán nhãn:** người xét sửa đổi Wikipedia, viết các tuyên bố được hỗ trợ/bác bỏ bởi hai phiên bản; bổ sung sửa đổi tổng hợp từ FEVER. Có Supported/Refuted/NEI. PDF tr. 3–4. Tổng 325.724 cặp từ sửa đổi thực + 163.180 cặp tổng hợp = 488.904 cặp, mục 3.4/Bảng 2.
- **Kết quả:** ALBERT-xlarge huấn luyện VitC+FEVER có tỷ lệ đổi dự đoán theo ngữ cảnh tương phản 90,94%, so với 64,59% khi chỉ huấn luyện FEVER; Bảng 4, PDF tr. 8. Đây là cột Contrast, không phải accuracy chung.
- **Vận dụng/hạn chế:** thiết kế cặp chỉ đổi chi tiết cần kiểm, chia theo nguồn để hạn chế rò rỉ. Đề tài giữ tài liệu hãng cố định và sửa tuyên bố; đó là vận dụng ý tưởng, không tái tạo nguyên cách sinh cặp của VitaminC. Mỗi biến thể vẫn cần nhãn thủ công.

### 3.16. [16] Robertson và Zaragoza — BM25 and Beyond (2009)

Nguồn: [PDF tác giả](../báo/%5B16%5D.pdf), [DOI](https://doi.org/10.1561/1500000019).

- **Bài toán:** xếp hạng tài liệu theo mức liên quan với truy vấn trong khung truy hồi xác suất; không phải phân loại tính đúng của tuyên bố. PDF tr. 3–5, 30.
- **Dữ liệu/gán nhãn:** đây là bài tổng quan lý thuyết và thực nghiệm truy hồi, không công bố một bộ nhãn kiểm chứng mới. Khi tối ưu tham số cần truy vấn và nhãn liên quan của tập đánh giá, mục 3.5, PDF tr. 30–31.
- **Phương pháp:** kết hợp trọng số RSJ/IDF, bão hòa tần suất từ và chuẩn hóa độ dài; công thức (3.10)–(3.15), PDF tr. 27–30. Tr. 30 PDF tương ứng trang in 360.
- **Kết quả/giới hạn:** tổng hợp khuyến nghị tham số và biến thể; chính tác giả nêu giá trị tốt phụ thuộc tài liệu/truy vấn, PDF tr. 30–31. Không có một F1 kiểm chứng để mang sang so với LLM.
- **Vận dụng:** dùng làm tầng chọn top-k đoạn trong tài liệu đúng mẫu sản phẩm; chọn cách tách từ/k trên tập phát triển. Điểm BM25 cao không chứng minh đủ điều kiện hoặc tuyên bố đúng; phải giữ chú thích và đo Recall@k.

## 4. Khảo sát bổ sung tháng 10

Tra cứu ngày 15/10/2026 trên ACL Anthology, arXiv và trang FTC. Các cụm tìm: `FActScore Fine-grained Atomic Evaluation`, `ProgramFC fact checking complex claims`, `ViWikiFC Vietnamese fact checking`, `half truth detection missing parts`, `Beyond Binary Nuance-Controlled`, `FTC 2012 up to claims consumers`. Chọn nguồn gốc phục vụ bốn hướng của Bước 3; đây là khảo sát có mục tiêu, không phải tổng quan hệ thống toàn bộ công bố. Thông tin tải và SHA-256: [danh mục bổ sung](../báo/bo_sung/danh_muc.json).

### 4.1. BS1 — FActScore: ảo giác và độ đúng từng sự kiện

Min và cộng sự, EMNLP 2023. [Nguồn](https://aclanthology.org/2023.emnlp-main.741/), [PDF](../báo/bo_sung/FActScore.pdf#page=4).

**Bài toán/cách làm:** tách văn bản LLM thành sự kiện nhỏ, đo tỷ lệ được nguồn hỗ trợ; định nghĩa ở PDF tr. 3. **Dữ liệu/nhãn:** tiểu sử sinh bởi mô hình, người kiểm Supported/Not-supported đối với Wikipedia, tr. 4. **Kết quả:** FActScore ChatGPT 58,3 trong thiết lập bài, Bảng 1 tr. 4. **Vận dụng:** báo lỗi theo tuyên bố thay vì gán cả quảng cáo một nhãn. **Giới hạn:** tỷ lệ hỗ trợ không phân biệt riêng lệch điều kiện; không dùng điểm năm 2023 để đánh giá model hiện tại.

### 4.2. BS2 — ProgramFC: kiểm chứng qua chương trình

Pan và cộng sự, ACL 2023. [Nguồn](https://aclanthology.org/2023.acl-long.386/), [PDF](../báo/bo_sung/ProgramFC.pdf#page=6).

**Bài toán/cách làm:** LLM sinh chương trình chia kiểm chứng thành tác vụ gọi hàm, trả True/False; PDF tr. 3–4. **Dữ liệu/nhãn:** dùng nhãn có sẵn từ HOVER và FEVEROUS-S, mục 4 tr. 5. **Kết quả:** ProgramFC N=5 đạt macro-F1 68,06 ở FEVEROUS-S/open-book, Bảng 1 tr. 6. **Vận dụng:** dấu vết thực thi giúp phân tích lỗi. **Giới hạn:** hàm con vẫn có mô hình ngôn ngữ; chương trình được sinh khác với quy tắc A–D cố định. Vì đã có ProgramFC, không tuyên bố “kết hợp LLM và mã quyết định” tự nó là điểm mới.

### 4.3. BS3 — ViWikiFC: phân biệt lỗi truy hồi và lỗi quyết định

Le và cộng sự, arXiv:2405.07615v2, 16/03/2026. [Nguồn](https://arxiv.org/abs/2405.07615v2), [PDF](../báo/bo_sung/ViWikiFC.pdf#page=8).

**Bài toán/dữ liệu:** kiểm chứng Wikipedia tiếng Việt, khoảng 20,9 nghìn mẫu. **Nhãn:** người viết Supported/Refuted/NEI và kiểm chéo, PDF tr. 4–5. **Kết quả:** InfoXLMLarge đạt F1 test 86,51; BM25 + InfoXLMLarge chỉ đạt strict accuracy 67,00 khi tính cả truy hồi, Bảng 4 và 6 tr. 8. **Vận dụng:** cần báo cả truy hồi và kết quả đầu–cuối. **Giới hạn:** không thuộc miền quảng cáo thông số; số lượng trong các bản/các bài dẫn lại có chênh lệch, không ghép số giữa phiên bản. Các chỉ số trên cũng không đo cùng một đại lượng.

### 4.4. BS4 — Beyond Binary: ngữ cảnh và tuyên bố nửa sự thật

Albertson và cộng sự, ROCLING 2025. [Nguồn](https://aclanthology.org/2025.rocling-main.5/), [PDF](../báo/bo_sung/Beyond_Binary.pdf#page=5).

**Bài toán/cách làm:** MEGA biểu diễn bằng chứng và ngữ cảnh bằng đồ thị, thử thêm/bỏ sắc thái ở đoạn bằng chứng, giữ nguyên tuyên bố; PDF tr. 3. **Dữ liệu/nhãn:** lấy 6.000 câu cân bằng từ PolitiFact; gộp True/Somewhat True/Completely False, bỏ Mostly False, tr. 4–5. **Kết quả:** accuracy claims-only 60%, nuance-injected 75%; F1 Somewhat True 63 → 74, Bảng 2 tr. 5. **Vận dụng:** thử có kiểm soát ảnh hưởng của cách diễn đạt. **Giới hạn:** không phải thí nghiệm bỏ điều kiện thông số; nhãn chính trị này không tương đương LECH.

### 4.5. BS5 — Báo cáo FTC về cách hiểu “up to” (2012)

Hastak và Murphy, báo cáo tháng 5/2012, FTC công bố tháng 6/2012. [Bản PDF đã lưu](../báo/bo_sung/FTC_Up_To_2012.pdf#page=7), [báo cáo gốc](https://search.ftc.gov/sites/default/files/documents/reports/effects-bristol-windows-advertisement-savings-claim-consumer-take-away-beliefs/120629bristolwindowsreport.pdf#page=7), [trang công bố](https://www.ftc.gov/news-events/news/press-releases/2012/06/ftc-report-many-consumers-believe-claims-promise-maximum-results).

Khảo sát 360 người ở Mỹ về quảng cáo cửa sổ; PDF tr. 3–5. Trong nhóm “up to”, 36% trả lời mở nhắc mức tiết kiệm 47% mà bỏ giới hạn; Bảng 1 tr. 7. Kết quả về **tiếp nhận thông điệp**, không đo hiệu quả cửa sổ. Vận dụng: làm động lực cho khảo sát tiếng Việt ở Bước 10; không thay thế khảo sát đó.

## 5. Tổng hợp phục vụ Chương 2

| Nhóm | Nguồn nên dùng | Điều rút ra cho đề tài |
|---|---|---|
| Kiểm chứng và bằng chứng | [2], [3], [13], [16] | Phải tách lỗi tìm nguồn khỏi lỗi kết luận; lưu nguồn và kiểm tính đủ. |
| Nửa sự thật, thiếu ngữ cảnh | [3], [4], BS4, BS5 | Phần bị bỏ có thể thay đổi cách hiểu; nhãn của từng bộ không đồng nhất. |
| Tiếng Việt | [5], [6], [7], BS3 | Có cơ sở về dữ liệu/đối chứng; vẫn phải đánh giá trên miền thông số sản phẩm. |
| Số liệu, biểu diễn và quyết định | [8], [9], [14], BS2 | Giữ đối tượng, đơn vị, điều kiện, kiểu giá trị; quyết định phải có dấu vết và kiểm thử. |
| Quảng cáo và văn bản LLM | [1], [10], [11], [12], BS1 | Kiểm theo nguồn chính thức; tách câu phải giữ nghĩa, lợi ích và chi phí cần được đo. |
| Kiểm thử tương phản | [8], [15], BS4 | Phân biệt phép giữ nhãn/đổi nhãn; chỉ đổi yếu tố cần khảo sát, không tự suy nhãn chuẩn. |

**Cách trình bày tính mới phù hợp với bằng chứng hiện có:** Trong các tài liệu đã khảo sát, đề tài tập trung vào quảng cáo thông số sản phẩm bằng tiếng Việt, biểu diễn điều kiện tường minh và quyết định bốn nhãn bằng quy tắc. LLM, BM25, neo nguồn, kiểm chứng qua mã và cặp tương phản đều có tiền lệ. Phần cần chứng minh là lợi ích của **đối chiếu điều kiện trong bộ quyết định**, trên dữ liệu và đối chứng của đề tài, chứ không phải chỉ ghép các công cụ này.

**Các câu có thể dùng khi viết lại tổng quan:**

1. “ViFactCheck báo cáo macro-F1 89,90% cho Gemma đã tinh chỉnh trong thiết lập nhận bằng chứng; con số này không bao gồm chất lượng truy hồi.” — [5], PDF tr. 5, Bảng 3.
2. “NumPert cho thấy một số biến đổi số gây suy giảm accuracy lớn; chẳng hạn GPT-4o ở zero-shot giảm từ 80,00% xuống 19,25% trong phép Mask của Bảng 2.” — [8], PDF tr. 5. Không gọi đây là mức giảm của mọi mô hình.
3. “MiniCheck-FT5 đạt BAcc gần GPT-4 trên LLM-AGGREFACT với chi phí suy luận quy đổi thấp hơn hơn 400 lần trong thiết lập của nghiên cứu.” — [11], PDF tr. 7–8.
4. “MeasEval là cơ sở tham khảo cho việc biểu diễn số đo cùng ngữ cảnh; đề tài tự xây danh mục điều kiện cho sản phẩm và quy tắc quyết định.” — [14], PDF tr. 2–3.
5. “TRACER phân tích bằng chứng bị lược khỏi phát biểu và suy ra tác động lên ý định hàm ẩn; đề tài khảo sát trường hợp có thể khai báo trước loại điều kiện cần đối chiếu.” — [4], PDF tr. 5–6.

## 6. Trạng thái và việc tiếp theo

- Đã có ghi chú bài toán, dữ liệu/nhãn, phương pháp, kết quả và giới hạn cho 16 bài; mỗi nhận định nghiên cứu trong đề cương đã có điểm đối chiếu hoặc được đánh dấu là suy luận/khẳng định cần thu hẹp.
- Đã bổ sung bốn bài cho bốn hướng khảo sát tháng 10 và đối chiếu nghiên cứu FTC được nhắc trong bối cảnh. Tài liệu bổ sung dùng mã BS để không tự thay danh mục đã nộp.
- **Đạt phần khảo sát và kiểm nguồn của Bước 3.** Các chỗ sai hoặc thiếu điều kiện không được coi là đã đúng chỉ vì tìm được trang; cần dùng cách diễn đạt đã hiệu chỉnh khi viết Chương 2/Bước 17 và trao đổi với CBHD nếu sửa bản đề cương chính thức.
- Việc tiếp theo theo kế hoạch là **Bước 4: chọn 12 mẫu sản phẩm và chia tập trước**. Không phải cài thêm LLM hay chuyển thẳng sang gán nhãn dữ liệu chính.
