# Đối chiếu tài liệu tham khảo và hướng triển khai KLTN

Ngày rà soát: 08/10/2026. Phân tích dựa trên sáu PDF gốc trong `báo/` và bài PhoBERT trong thư mục con; ưu tiên bảng số liệu và thiết lập thí nghiệm của bài gốc. Các số dưới đây là kết quả do tác giả công bố, không phải kết quả chạy lại của khóa luận. Năm tài liệu bổ sung được kiểm tra qua trang xuất bản/arXiv; chưa tái lập mô hình của các bài.

Đã rà soát lần hai theo phản biện: [bảng đối chiếu số liệu/trang gốc và kết luận từng nhận xét](KIEM_TRA_PHAN_BIEN_2026-10-08.md). Hồ sơ có ảnh các trang PDF chứa số bị nghi ngờ, snapshot năm tài liệu mới và năm trang Apple.

## 1. Fact-checking for online advertisement posts

Nguồn: [PDF [1]](../báo/[1].pdf), mục 3–5, đặc biệt mục 3.3 và Bảng 2; [PACLIC 2024](https://aclanthology.org/2024.paclic-1.40/).

- Bài toán/dữ liệu: phát hiện vi phạm trong 1.175 bài quảng cáo Facebook của 283 cơ sở thẩm mỹ, đối chiếu giấy phép, địa chỉ và kỹ thuật được cấp phép từ nguồn y tế chính thức. Đơn vị kết luận cuối là bài quảng cáo, với hai nhãn.
- Phương pháp: GPT-3.5 Turbo trích thông tin; quy tắc kiểm tra giấy phép/địa chỉ; mô hình embedding so khớp kỹ thuật quảng cáo với danh mục. Với mỗi kỹ thuật lấy độ tương đồng cao nhất với danh mục rồi lấy giá trị nhỏ nhất trên toàn bài để so với ngưỡng.
- Kết quả: BGE-M3 ở ngưỡng 0,4 đạt Accuracy 0,783, Precision 0,686, F1 0,703. Đây là F1 được báo trong bảng, không tự đổi tên thành Macro-F1. Một số cấu hình đạt Accuracy khoảng 0,791 nhưng bài lưu ý hiện tượng dự đoán thiên về lớp phổ biến; không chọn Accuracy làm bằng chứng duy nhất.
- Hạn chế: độ tương đồng ngữ nghĩa không trực tiếp xác nhận giá trị, đơn vị và điều kiện; nhãn toàn bài không chỉ rõ mức độ hỗ trợ của từng claim. Bài không cung cấp bằng chứng rằng cùng cách đánh giá áp dụng được cho thông số tai nghe.
- Kế thừa: nguồn chính thức, trích xuất có cấu trúc và kiểm tra bằng quy tắc. Đây là căn cứ phải tránh tuyên bố “LLM kết hợp Python” là đóng góp mới. Phần cần kiểm nghiệm thêm của KLTN là đối chiếu từng claim theo phạm vi sản phẩm/điều kiện và giữ riêng nhãn thiếu bằng chứng.

## 2. FactLens: Benchmarking Fine-Grained Fact Verification

Nguồn: [PDF [2]](../báo/[2].pdf), mục 2–3, Bảng 1–2, Phụ lục B.4/C/D; [ACL Findings 2025](https://aclanthology.org/2025.findings-acl.929/).

- Bài toán/dữ liệu: tách claim phức tạp thành sub-claim và đánh giá chất lượng phép tách. Có 733 claim gốc lấy từ CoverBench, không phải 733 sub-claim; người gán nhãn rà soát và sửa các phép tách do LLM tạo.
- Phương pháp: sáu tiêu chí gồm tính nguyên tử, đủ ngữ cảnh, thông tin tự thêm, bao phủ, trùng lặp và khả năng đọc. Kết hợp bộ chấm LLM với chỉ số thống kê; GPT-4o-mini kiểm chứng trên bằng chứng được cấp sẵn. Phép gộp nhãn nhị phân của bài không cần sao chép vào KLTN vốn báo từng claim.
- Kết quả: Bảng 1 ghi tương quan Pearson/Spearman của bộ chấm LLM với người ở tiêu chí đủ ngữ cảnh chỉ 0,14/0,09. Phụ lục B.4 ghi Krippendorff’s alpha tương ứng 0,0486, trong khi atomicity/coverage/redundancy đạt 0,4421/0,5300/0,4240. Đây là mức khớp của bộ chấm với người, không phải Accuracy/F1 của bộ kiểm chứng. Kết quả theo nhóm cho thấy chất lượng phép tách liên hệ với chất lượng kiểm chứng, không chứng minh mọi phép tách đều cải thiện.
- Hạn chế: không đánh giá truy hồi; mô hình kiểm chứng cố định; bộ chấm đủ ngữ cảnh còn yếu. Điểm đánh giá LLM không thay thế việc rà soát thủ công sản phẩm và điều kiện.
- Kế thừa: giữ chủ thể, phiên bản, bộ phận và điều kiện ngay trong mỗi claim; lưu liên kết về quảng cáo gốc. MVP dùng cùng tập claim đã rà soát để tránh trộn lỗi tách với lỗi quyết định; chức năng tách tự động được đánh giá riêng nếu triển khai.

## 3. Think Right, Not More: Test-Time Scaling for Numerical Claim Verification

Nguồn: [PDF [3]](../báo/[3].pdf), mục 3–5, Bảng 1–2 và mục 7; [EMNLP Findings 2025](https://aclanthology.org/2025.findings-emnlp.1322/).

- Bài toán/dữ liệu: hạn chế suy luận lệch hướng khi kiểm chứng claim số liệu; QuanTemp có 9.935/3.084/2.495 claim train/validation/test. Kiểm tra chuyển miền trên 200 claim thuộc tập đánh giá ClaimDecomp.
- Phương pháp: BM25 lấy 100 ứng viên rồi xếp hạng lại còn ba đoạn; LLM sinh các đường suy luận. Verifier dùng Llama-3.2-3B fine-tune với LoRA để chọn đường phù hợp; Adaptive BoN sử dụng biểu diễn ẩn và độ phức tạp để quyết định khi nào cần thêm lượt suy luận.
- Kết quả: Bảng 1, Llama-3.1-8B trên QuanTemp: Top-1 Macro-F1 44,80, Best-of-N 53,20, Adaptive BoN 53,91. Hiệu số Adaptive−Top-1 là 9,11 điểm phần trăm, tương đương khoảng 20,33% tương đối theo chính các số bảng. Diễn giải “18,8%” trong bài không khớp phép chia này; khi trích nên ghi trực tiếp hai điểm số và thiết lập. Trên ClaimDecomp, tương ứng Top-1 36,07 và Adaptive 42,44.
- Hạn chế: phải huấn luyện verifier, lưu nhiều đường suy luận và truy cập biểu diễn mô hình để áp dụng cơ chế thích ứng như bài. Bằng chứng nhiễu vẫn ảnh hưởng; kết quả không phải chứng minh bộ quy tắc A–B–C đã có hiệu quả.
- Kế thừa: xây ca lỗi về đơn vị, chủ thể, thời điểm/điều kiện và cách diễn đạt giới hạn số. Bảng 2 cho thấy BoN có tách đạt 51,77 so với 53,23 khi không tách; đây là lý do cần kiểm tra phép tách, không mặc định tách càng nhỏ càng tốt. Không đưa huấn luyện verifier hoặc test-time scaling vào MVP của một sinh viên.

## 4. Explaining Sources of Uncertainty in Automated Fact-Checking

Nguồn: [PDF [4]](../báo/[4].pdf), mục 2–5, Bảng 1, Limitations và Phụ lục I.

- Bài toán/dữ liệu: giải thích vì sao mô hình không chắc chắn khi đọc nhiều bằng chứng; chọn 600 mẫu HealthVer và 600 mẫu DRUID. Thiết lập chính dùng một claim với hai bằng chứng; các thiết lập bổ sung nằm ở phụ lục.
- Phương pháp: CLUE đo entropy của phân bố nhãn, xác định tương tác giữa các đoạn qua attention, gán quan hệ đồng thuận/mâu thuẫn/không liên quan và dùng chúng để hướng dẫn lời giải thích. CLUE-Span+Steering còn điều chỉnh attention. Cần phân biệt logits/attention của mô hình với độ tin cậy khách quan của tài liệu.
- Kết quả: Qwen2.5-14B trên DRUID đạt Entropy-CCT 0,102 với CLUE-Span+Steering, so với −0,080 của PromptBaseline. Đây là hệ số tương quan, chênh 0,182, không phải mức tăng Accuracy 18,2 điểm phần trăm. Đánh giá người đọc sử dụng 12 người, 40 claim và 120 lời giải thích; ưu thích của người đọc và độ trung thành với mô hình là hai góc đánh giá khác nhau.
- Hạn chế: cần khả năng truy cập nội tại mô hình và tài nguyên đáng kể; lỗi trích span/gán quan hệ có thể truyền xuống lời giải thích. Điểm giải thích tốt không đồng nghĩa nhãn kiểm chứng đúng, và bất định của mô hình không đồng nghĩa nhãn NEI.
- Kế thừa: lưu đoạn nguồn và trường nào dẫn tới kết luận, kiểm tra lý do bám nguồn/dấu vết A–B–C. KLTN có thể dùng mẫu lý do từ dấu vết quy tắc, không cần tái tạo CLUE hoặc đánh giá người đọc quy mô tương tự.

## 5. CoVer: Conflict-Aware Claim Verification

Nguồn: [PDF [5]](../báo/[5].pdf), mục 4–6, Bảng 1–3; bản PDF ghi arXiv:2609.00508v1.

- Bài toán/dữ liệu: xử lý bằng chứng bất đồng và chọn bằng chứng cần ưu tiên từ Community Notes. ContraNote Conflict có 33.686 bài đăng, gồm 6.241 Supported và 27.445 Refuted; Prioritization có 54.474 mẫu trên 27.237 bài đăng, không phải 54.474 bài độc lập.
- Phương pháp: chuẩn hóa bằng chứng và metadata; LLM dự đoán lập trường cùng chất lượng; tổng hợp điểm theo quy tắc; LLM kiểm chứng tập đồng thuận và kiểm tra lại kết quả Supported. Điểm chất lượng là đầu ra ước lượng của LLM, không phải nhãn chuẩn khách quan về nguồn.
- Kết quả: trên Conflict, CoVer có Accuracy 86,0%, Macro-F1 68,0%, Balanced Accuracy 64,5%; Confact có 82,8%, 73,4%, 76,1%. Vì vậy không thể nói CoVer tốt nhất theo mọi chỉ số. Trên Prioritization, CoVer đạt 88,5%/88,5%/89,2%. Bài nêu so sánh trên Conflict với Confact và ConflictRes chưa có ý nghĩa thống kê theo McNemar.
- Hạn chế: thiết lập chính nhị phân ánh xạ cả `insufficient` sang Refuted, không tương thích trực tiếp với NEI trong KLTN. Metadata Community Notes có thể mang tín hiệu xây nhãn; bài có kiểm tra loại metadata, cần đọc cùng kết quả chính. Không sử dụng nhãn hoặc tín hiệu tạo nhãn làm đầu vào cho hệ thống của KLTN.
- Kế thừa: chuẩn hóa schema, kiểm tra phạm vi, lưu hai phía của xung đột và rà soát hỗ trợ trước khi chấp nhận. KLTN phải đặc tả riêng: hai nguồn khác chế độ không phải xung đột; cùng phạm vi nhưng chưa giải quyết được thì NEI, không mặc định Refuted hoặc chọn nguồn thuận claim.

## 6. Fathom: A Fast and Modular RAG Pipeline for Fact-Checking

Nguồn: [PDF [6]](../báo/[6].pdf), mục 3–5, Bảng 1–4; [FEVER Workshop 2025](https://aclanthology.org/2025.fever-1.20/).

- Bài toán/dữ liệu: kiểm chứng dựa trên tài liệu web của AVeriTeC, 4.568 claim với bốn nhãn. Bài sử dụng knowledge store đã thu trước; không phải truy hồi trực tiếp toàn bộ web cho mỗi lần đánh giá. Các nhãn xung đột/cherry-picking và thiếu bằng chứng được tách riêng.
- Phương pháp: Qwen2.5-7B sinh QA giả định để mở rộng truy vấn; BM25 lấy 250 đoạn cho mỗi QA; embedding Snowflake xếp hạng lại còn 10, tối đa tám đoạn/QA đưa vào Phi-4 lượng tử hóa để quyết định. QA giả định dùng cho truy vấn, không phải bằng chứng thực tế.
- Kết quả: Bảng 4 trên test ghi AVeriTeC 0,2043 so với baseline 0,2023; chênh 0,0020 điểm, tức 0,20 điểm phần trăm hoặc khoảng 0,99% tương đối. Abstract gọi 0,99% là tuyệt đối, không khớp bảng. Thời gian là 22,73 so với 33,88 giây/claim, giảm khoảng 32,91%. Trên dev, F1 thiếu bằng chứng 0,1455 và nhãn xung đột 0; kết quả tổng thể không phản ánh tốt hai lớp ít mẫu.
- Hạn chế: kết quả dev và test khác nhau đáng kể; chia đoạn cố định có thể mất ngữ cảnh; phần lớn chất lượng nằm ở lớp phổ biến. Điểm AVeriTeC có điều kiện về bằng chứng nên không so trực tiếp với Macro-F1 ba nhãn của KLTN.
- Kế thừa: BM25 làm truy hồi nền gọn, đo thời gian toàn pipeline và lưu nguồn của từng đoạn. KLTN giữ thông số cùng tiêu đề/chú thích, chọn k trên dev/pilot và đo evidence-set recall@k; val chỉ kiểm tra cấu hình đã khóa. Không gọi chỉ số này là Ev2R, vốn đánh giá các sự kiện trong QA theo giao thức khác.

## 7. PhoBERT: Pre-trained language models for Vietnamese

Nguồn: [PDF PhoBERT v3](../báo/báo%20con1/2003.00744v3.pdf), mục 2–4, Bảng 2–3.

- Bài toán/dữ liệu: mô hình biểu diễn tiếng Việt, pretrain trên khoảng 20 GB văn bản gồm Wikipedia và tin tức đã khử trùng. Đây không phải bộ dữ liệu kiểm chứng quảng cáo.
- Phương pháp: hai cỡ base/large theo cách pretrain RoBERTa; tách từ tiếng Việt trước BPE rồi fine-tune cho POS, parsing, NER và NLI.
- Kết quả: Bảng 3 ghi PhoBERT-large đạt NER F1 94,7 và NLI Accuracy 80,0; PhoBERT-base lần lượt 93,6 và 78,5. Cấu hình NLI dùng dữ liệu huấn luyện tiếng Việt, không so trực tiếp với XLM-R huấn luyện ghép tất cả ngôn ngữ.
- Hạn chế/kế thừa: encoder cần thích nghi tác vụ; checkpoint PhoBERT cơ bản không tự là mô hình sentence embedding, retriever hay bộ quyết định Supported/Refuted/NEI. Có thể làm đối chứng mở rộng khi có dữ liệu/nguồn lực, nhưng không bắt buộc cho MVP BM25 + LLM extraction + A–B–C. Cần ghi rõ tokenizer; không viện dẫn PhoBERT để khẳng định tách theo khoảng trắng đã tương đương tách từ.

## Tài liệu bổ sung đã kiểm tra nguồn

| Tài liệu | Vai trò trong đề tài | Giới hạn áp dụng |
|---|---|---|
| [FEVER — NAACL 2018](https://aclanthology.org/N18-1074/) | Căn cứ cho ba nhãn và việc lưu bộ bằng chứng | Dữ liệu Wikipedia, không cung cấp kết quả cho miền tai nghe |
| [AVeriTeC — NeurIPS 2023](https://arxiv.org/abs/2305.13117) | Dữ liệu thực, nguồn web, chú ý rò rỉ thời gian | Khác miền và giao thức đánh giá; không cần tái tạo pipeline web |
| [ViFactCheck — arXiv 2024, accepted AAAI 2025](https://arxiv.org/abs/2412.15308) | Bối cảnh kiểm chứng tin tiếng Việt và gán nhãn claim–evidence | Không dùng kết quả của bộ tin tức làm mục tiêu bắt buộc cho quảng cáo |
| [ViWikiFC — arXiv, v2 năm 2026](https://arxiv.org/abs/2405.07615v2) | Phân biệt chất lượng truy hồi, quyết định và pipeline tiếng Việt | Nguồn Wikipedia khác tài liệu kỹ thuật chính hãng |
| [ViNumFCR — INLG 2025](https://aclanthology.org/2025.inlg-main.9/) | Bối cảnh kiểm chứng số liệu tiếng Việt | Không chứng minh đã giải quyết lỗi bộ phận, phiên bản và điều kiện của tai nghe |

Danh mục trong hai DOCX đánh số các tài liệu bổ sung là [7]–[11]: năm tài liệu, không phải sáu như một dòng trong nhật ký cũ. Chúng được bổ sung trong bản rà soát tháng 10, không ghi thành tiến độ đọc bài đã hoàn thành tháng 9.

## Khoảng trống và thiết kế nghiên cứu khả thi

Trong phạm vi tài liệu đã khảo sát, phần đáng kiểm nghiệm là: bộ claim quảng cáo tai nghe tiếng Việt có provenance và hướng dẫn ba nhãn, kết hợp đối chiếu rõ sản phẩm, phiên bản, bộ phận, loại giá trị và điều kiện. Đây là nhận định từ khảo sát hiện có, không phải khẳng định chưa từng có công trình tương tự trên toàn bộ lĩnh vực. Tính mới cần được đánh giá qua dữ liệu, đặc tả và thực nghiệm, không chỉ qua lựa chọn Python.

Ba câu hỏi giữ phạm vi vừa sức:

1. RQ1: BM25 tìm đủ một bộ bằng chứng đến đâu? Dùng evidence-set recall@k, mẫu số chỉ gồm claim có bộ bằng chứng chuẩn đủ kết luận; NEI do thiếu nguồn không được tự coi là truy hồi thành công.
2. RQ2: lỗi đến từ truy hồi, trích xuất hay quyết định? Rà mẫu được chọn trước và kiểm tra theo chuỗi nguồn → đoạn → hồ sơ → quyết định. Một mẫu có thể có nhiều lỗi. E1/E2 chỉ bổ sung khi có thời gian; nếu không chạy, kết quả kiểm tra thủ công không phải ước lượng nhân quả riêng từng thành phần.
3. RQ3 (thăm dò ở mức tối thiểu): P thay đổi FAR và Recall Supported so với B1 thế nào? B1/P dùng cùng hồ sơ đã trích/chuẩn hóa. Báo chênh lệch, mẫu số, kết quả từng họ và độ nhạy bỏ từng họ. ΔFAR<0 cùng ΔRecall≥−5 điểm phần trăm chỉ là xu hướng thuận lợi trên mẫu. Không dùng “toàn bộ CI dưới 0” làm cửa đạt/rớt hoặc suy ra ưu thế tổng quát từ bốn họ test; không sửa luật theo test.

MVP gồm dữ liệu có nhãn/provenance, BM25, JSON extraction, B0/B1/P và đánh giá E3. Chốt 120 claim/12 họ tối thiểu hoặc 180/18–20 họ mục tiêu; 300/30, P−A/P−B, E1/E2, tách tự động và website là mở rộng. Pilot cố định sáu họ nằm trong dev: 12 họ chia 6/2/4, 18 chia 7/4/7, 20 chia 8/4/8. Không chuyển pilot sang test. Chọn mô hình/prompt/k trên dev; dung sai có căn cứ nguồn; val chỉ audit một lượt sau khóa, không tối ưu nhiều cấu hình trên hai họ.

Một người gán nhãn chỉ có thể báo tự đồng thuận khi gán lại có khoảng cách thời gian; không gọi đó là độ đồng thuận giữa hai người. Chia tập theo họ, lưu cả claim sinh thông thường và biến thể có kiểm soát, báo riêng phân bố nhãn và nhóm lỗi. Bootstrap theo họ trên chỉ bốn họ test còn rất hạn chế, nên kết quả ở quy mô tối thiểu mang tính thăm dò.

A giữ lọc phạm vi/bộ phận/thuộc tính/đơn vị; C có nhánh so sánh loại giá trị rõ ràng trước tổng hợp nhãn. P−A chỉ tắt kiểm tra bộ phận, không tắt luật số của C. Xem [đặc tả A–B–C](QUY_TAC_ABC.md).

## Việc tiếp theo cần dữ liệu thực

- Hoàn thiện schema nguồn/claim/evidence/nhãn và quy ước họ sản phẩm; lưu snapshot, hash, thời điểm, ngôn ngữ và phạm vi.
- EX-01–20 đã đối chiếu trang Apple và có snapshot/ảnh 08/10; nguồn gốc câu cũ vẫn chưa xác định, không được suy ra tự viết hoặc LLM sinh. Ba ca EX-21–23 là giả lập xung đột do Codex soạn, chỉ dùng kiểm thử. Cần log sinh thật trước khi tính vào dữ liệu LLM; ngày 07/10 kế thừa không chứng minh hoàn thành tháng 9.
- Ghi cấu hình máy/API, ngân sách, tối đa hai mô hình ứng viên và log extraction; chưa có căn cứ để chọn tên mô hình thay người dùng từ hồ sơ hiện tại.
- Thu pilot và đo năng suất/chi phí trước khi chốt quy mô ở Gate 2. Các ngưỡng quản lý trong đề cương là quy ước đề xuất, chưa phải kết quả thực nghiệm hoặc tiêu chuẩn khoa học chung.
