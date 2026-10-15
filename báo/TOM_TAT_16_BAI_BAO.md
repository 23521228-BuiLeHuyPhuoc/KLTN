# Tóm tắt 16 bài báo trong đề cương khóa luận

- Số thứ tự khớp danh mục tài liệu tham khảo của đề cương bản cuối ngày 11/10/2026. Bấm vào tên bài để mở PDF.
- Nội dung tóm tắt dựa trên các PDF trong thư mục này. Riêng [5] là bản tác giả trên arXiv, tương ứng bài công bố tại AAAI 2025; [9] là bản tiền công bố arXiv.
- Các số liệu dưới đây là kết quả trong thí nghiệm của từng bài, không dùng để xếp hạng trực tiếp giữa các bài vì dữ liệu và cách đánh giá khác nhau.
- Mục **Liên hệ khóa luận** là nhận xét vận dụng vào đề tài kiểm chứng thông số kỹ thuật có điều kiện ràng buộc trong quảng cáo, không phải kết luận nguyên văn của tác giả.

## [1] [Hallucination Detection in LLM-enriched Product Listings](%5B1%5D.pdf) — 2024

- **Vấn đề:** Khi LLM bổ sung hoặc viết lại thông tin sản phẩm, mô hình có thể tự thêm thuộc tính không được dữ liệu gốc hỗ trợ. Bài xem đây là “ảo giác”, kể cả khi thông tin đó tình cờ đúng ngoài thực tế.
- **Cách làm:** Kiểm tra hai bước: dùng các phép so khớp từ ngữ và ngữ nghĩa ít tốn chi phí để tìm nhiều trường hợp đáng nghi; sau đó dùng LLM xác nhận lại để giảm báo động nhầm.
- **Kết quả chính:** Thử nghiệm trên hai bộ dữ liệu thương mại điện tử cho thấy cách làm hiệu quả hơn với thuộc tính có cấu trúc, giá trị ngắn và rõ ràng so với mô tả tự do dài.
- **Điểm cần nhớ:** “Không có trong nguồn” và “sai sự thật” là hai khái niệm khác nhau. Kiến thức thông thường cũng khiến người gán nhãn và hệ thống không thống nhất về thông tin nào được phép suy ra.
- **Liên hệ khóa luận:** Củng cố việc kiểm tra quảng cáo dựa trên tài liệu của đúng sản phẩm; cần quy định rõ trường hợp thiếu bằng chứng và trường hợp thông số bị nguồn bác bỏ.

## [2] [FEVER: A Large-scale Dataset for Fact Extraction and VERification](%5B2%5D.pdf) — 2018

- **Vấn đề:** Xác định một tuyên bố có đúng với nguồn văn bản hay không, đồng thời tìm những câu làm bằng chứng cho kết luận.
- **Dữ liệu:** Gồm **185.445 tuyên bố** được xây dựng từ Wikipedia, với ba nhãn: được hỗ trợ, bị bác bỏ và chưa đủ thông tin. Một số trường hợp cần kết hợp bằng chứng từ nhiều câu hoặc nhiều trang.
- **Cách làm:** Hệ thống cơ sở gồm ba bước: tìm tài liệu liên quan → chọn câu bằng chứng → phân loại tuyên bố dựa trên bằng chứng.
- **Kết quả chính:** Hệ thống trong bài đạt **50,91%** khi chỉ chấm nhãn, nhưng còn **31,87%** khi yêu cầu cả nhãn đúng lẫn bằng chứng đúng. Việc tìm đúng bằng chứng là một khó khăn lớn.
- **Liên hệ khóa luận:** Có thể học cách tổ chức dữ liệu gồm tuyên bố, nhãn và bằng chứng; nên đánh giá truy hồi riêng với quyết định nhãn. Ba nhãn của FEVER chưa có lớp riêng cho lỗi lệch điều kiện.

## [3] [AVeriTeC: A Dataset for Real-world Claim Verification with Evidence from the Web](%5B3%5D.pdf) — 2023

- **Vấn đề:** Nhiều bộ dữ liệu cũ dùng câu được tạo nhân tạo hoặc có bằng chứng thiếu ngữ cảnh, chưa đủ để kết luận, hay xuất hiện sau thời điểm tuyên bố.
- **Dữ liệu:** Gồm **4.568 tuyên bố thực tế** từ **50 tổ chức kiểm chứng**. Mỗi mẫu có các cặp câu hỏi–trả lời, nguồn bằng chứng trên web và phần giải thích kết luận.
- **Cách làm:** Chia việc kiểm chứng thành các câu hỏi nhỏ để tìm bằng chứng; gán nhãn và kiểm tra chất lượng qua nhiều vòng. Có bốn nhãn: được hỗ trợ, bị bác bỏ, chưa đủ bằng chứng, và bằng chứng mâu thuẫn/chọn lọc bằng chứng.
- **Đóng góp chính:** Chú trọng tính đầy đủ của bằng chứng và tránh dùng thông tin từ tương lai. Độ đồng thuận nhãn được báo cáo là **κ = 0,619**; cách đánh giá xem xét cả kết luận lẫn bằng chứng.
- **Liên hệ khóa luận:** Nên lưu URL, thời điểm và đoạn nguồn cùng lý do gán nhãn. Nhãn chọn lọc bằng chứng có liên quan tới việc bỏ bối cảnh, nhưng không đồng nhất với nhãn “Lệch điều kiện” của khóa luận.

## [4] [The Missing Parts: Augmenting Fact Verification with Half Truth Detection](%5B4%5D.pdf) — 2025

- **Vấn đề:** Một câu có thể đúng về thông tin được nói ra nhưng vẫn gây hiểu lầm vì bỏ mất bối cảnh quan trọng; bài gọi đây là “nửa sự thật”.
- **Dữ liệu:** Xây dựng **PolitiFact-Hidden**, khoảng **15 nghìn tuyên bố chính trị**, có chú thích bằng chứng được thể hiện, bằng chứng bị bỏ sót và thông điệp hàm ý của tuyên bố.
- **Cách làm:** Khung **TRACER** xác định phần bằng chứng bị bỏ sót, suy ra thông điệp hàm ý, rồi đánh giá phần bị bỏ sót có làm thay đổi cách hiểu thông điệp đó hay không. Kết quả được dùng để xét lại nhãn ban đầu.
- **Kết quả chính:** Khi ghép với HiSS, F1 của lớp Half-True trên tập kiểm tra tăng từ **44,4 lên 60,5**, tức **16,1 điểm**. Tuy nhiên, thí nghiệm chủ yếu thuộc lĩnh vực chính trị và phụ thuộc khả năng suy ra hàm ý.
- **Liên hệ khóa luận:** Đây là cơ sở gần với quảng cáo nêu đúng con số nhưng bỏ điều kiện áp dụng. Khóa luận có thể giới hạn vào điều kiện ghi rõ trong tài liệu hãng, thay vì phải suy đoán ý định của người viết.

## [5] [ViFactCheck: A New Benchmark Dataset and Methods for Multi-domain News Fact-Checking in Vietnamese](%5B5%5D.pdf) — AAAI 2025

- **Vấn đề:** Thiếu dữ liệu kiểm chứng tiếng Việt có cặp tuyên bố–bằng chứng được con người gán nhãn.
- **Dữ liệu:** Gồm **7.232 cặp tuyên bố–bằng chứng**, thuộc **12 chủ đề** tin tức; có ba nhãn được hỗ trợ, bị bác bỏ và chưa đủ thông tin. Độ đồng thuận Fleiss’ kappa đạt **0,83**.
- **Cách làm:** So sánh mô hình ngôn ngữ được tinh chỉnh với LLM dùng lời nhắc; đồng thời khảo sát truy hồi bằng BM25, SBERT và cách kết hợp hai phương pháp.
- **Kết quả chính:** Gemma được tinh chỉnh đạt **Macro-F1 89,90%** ở thiết lập sử dụng bằng chứng chuẩn của dữ liệu. Suy luận với nhiều bằng chứng, câu mơ hồ và thông tin mâu thuẫn vẫn gây khó khăn; kết quả này không đồng nghĩa hệ thống tự tìm bằng chứng đạt cùng mức điểm.
- **Liên hệ khóa luận:** Tham khảo cách viết hướng dẫn gán nhãn tiếng Việt, đo đồng thuận và xây dựng đối chứng. Cần đánh giá lại trên quảng cáo thông số kỹ thuật vì dữ liệu của bài là tin tức đa lĩnh vực.

## [6] [ViNumFCR: A Novel Vietnamese Benchmark for Numerical Reasoning Fact Checking on Social Media News](%5B6%5D.pdf) — 2025

- **Vấn đề:** Kiểm chứng câu tiếng Việt có số liệu đòi hỏi hiểu quan hệ giữa các con số và ngữ cảnh, không chỉ so khớp từ ngữ.
- **Dữ liệu:** Gồm **10.008 mẫu** trên **12 chủ đề**, với nhãn được hỗ trợ, bị bác bỏ hoặc chưa đủ thông tin, kèm bằng chứng liên quan.
- **Cách làm:** Đánh giá mô hình được tinh chỉnh và LLM dùng lời nhắc; khảo sát truy hồi bằng TF-IDF, BM25, SBERT và kết hợp SBERT với BM25.
- **Kết quả chính:** XLM-RLarge được tinh chỉnh đạt **Accuracy 90,05%** trên tập kiểm tra. Các LLM thử theo cách không có hoặc có ít ví dụ trong lời nhắc đạt thấp hơn đáng kể; không nên diễn giải thành mọi LLM đều kém, vì Gemma-2 được tinh chỉnh đạt **88,96%**.
- **Liên hệ khóa luận:** Là nguồn tham khảo cho kiểm chứng số liệu tiếng Việt và thiết kế đối chứng. Tuy nhiên, dữ liệu tin tức chưa trực tiếp kiểm tra điều kiện vận hành của sản phẩm, chẳng hạn thời lượng pin khi bật/tắt một tính năng.

## [7] [SemViQA: A Semantic Question Answering System for Vietnamese Information Fact-Checking](%5B7%5D.pdf) — 2026

- **Vấn đề:** Hệ thống kiểm chứng tiếng Việt dễ chọn sai bằng chứng khi gặp câu mơ hồ, cấu trúc phức tạp hoặc văn bản dài.
- **Cách tìm bằng chứng:** Kết hợp TF-IDF để xử lý nhanh trường hợp đơn giản với mô hình hỏi–đáp để chọn đoạn bằng chứng cho trường hợp khó; chia văn bản thành các phần phù hợp giới hạn đầu vào.
- **Cách quyết định nhãn:** Kết hợp bộ phân loại ba nhãn với bộ phân loại chuyên phân biệt “được hỗ trợ” và “bị bác bỏ”; dùng điểm tin cậy để chọn kết quả cuối.
- **Kết quả chính:** Đạt **strict accuracy 78,97% trên ISE-DSC01** và **80,82% trên ViWikiFC**. Chỉ số này yêu cầu nhãn đúng và bằng chứng đúng đối với các trường hợp cần bằng chứng. Phiên bản Faster được báo cáo tăng tốc khoảng **7 lần** trong thiết lập thử nghiệm.
- **Liên hệ khóa luận:** Gợi ý tách rõ lỗi chọn bằng chứng và lỗi gán nhãn, đồng thời cân nhắc tốc độ khi tích hợp vào CopyPro. Bài chưa xây dựng cơ chế riêng để so sánh điều kiện thông số sản phẩm.

## [8] [NumPert: Numerical Perturbations to Probe Language Models for Veracity Prediction](%5B8%5D.pdf) — 2025

- **Vấn đề:** Mô hình có thể trả lời đúng câu ban đầu nhưng vẫn giữ nguyên đáp án khi một con số quan trọng đã bị sửa.
- **Cách làm:** Tạo sáu nhóm biến đổi có kiểm soát: cách biểu diễn số, xấp xỉ, khoảng giá trị, che số, thay số ngẫu nhiên và số âm. Có phép biến đổi giữ nguyên nhãn và có phép biến đổi buộc nhãn phải đổi.
- **Kết quả chính:** Không mô hình được thử nào ổn định trong mọi tình huống. Thay đổi số có thể làm chất lượng dự đoán giảm mạnh; ngữ cảnh dài hơn cũng thường làm giảm độ chính xác.
- **Hướng cải thiện:** Đưa ví dụ về các biến đổi số vào lời nhắc giúp nhiều mô hình phục hồi một phần hiệu năng, nhưng chưa giải quyết hoàn toàn vấn đề.
- **Liên hệ khóa luận:** Dùng ý tưởng này để tạo cặp kiểm thử chỉ khác một chi tiết: giá trị, đơn vị, khoảng số hoặc điều kiện. Cần xác định trước khi nào nhãn phải giữ nguyên và khi nào phải đổi.

## [9] [VeriFin: A Neurosymbolic Framework for Verifying LLM-Generated Financial Claims](%5B9%5D.pdf) — arXiv 2026

- **Vấn đề:** Một kết quả tài chính có thể tính toán đúng nhưng vẫn sai vì lấy nhầm kỳ báo cáo, đơn vị, chỉ tiêu hoặc công thức.
- **Cách làm:** Tách câu trả lời do LLM sinh khỏi bước xác minh. Hệ thống lấy dữ kiện từ báo cáo XBRL, xác lập công thức từ nguồn độc lập với đáp án ứng viên, rồi dùng bộ giải ràng buộc **Z3** để kiểm tra.
- **Đầu ra:** Trả về được xác minh, vi phạm ràng buộc hoặc chưa thể kết luận. Khi có mâu thuẫn, hệ thống chỉ ra nhóm dữ kiện/công thức gây xung đột để hỗ trợ sửa câu trả lời.
- **Kết quả chính:** Không ghi nhận trường hợp chấp nhận nhầm câu sai trong các thử nghiệm trên **600 câu XBRLFiling** và **67 câu thuộc tập con FinanceBench**. Đây là kết quả thực nghiệm, không phải bảo đảm không bao giờ sai; hệ thống vẫn có trường hợp từ chối câu đúng hoặc chưa thể kết luận.
- **Liên hệ khóa luận:** Gần với hướng dùng LLM để trích xuất, còn Python/quy tắc quyết định nhãn. Việc dùng Z3 không bắt buộc; điểm đáng học là neo dữ kiện vào nguồn và không để câu quảng cáo tự quyết định tiêu chuẩn xác minh nó.

## [10] [FactLens: Benchmarking Fine-Grained Fact Verification](%5B10%5D.pdf) — 2025

- **Vấn đề:** Gán một nhãn cho cả câu dài có nhiều ý có thể che mất chi tiết sai. Tách thành tuyên bố nhỏ giúp kiểm tra và giải thích chính xác hơn, nhưng thao tác tách cũng có thể làm mất nghĩa.
- **Đóng góp:** Đề xuất bộ đánh giá chất lượng tách tuyên bố: mỗi ý có đủ nhỏ không, đủ ngữ cảnh không, có tự thêm thông tin không, có bao phủ hết câu gốc không, có trùng lặp không và có dễ đọc không.
- **Điểm đáng chú ý:** Khi tách câu phải giữ nguyên điều kiện. Biến mệnh đề “nếu X” thành khẳng định “X đúng” là làm sai nghĩa, dù câu mới trông rõ ràng hơn.
- **Kết quả chính:** Chất lượng tách tuyên bố liên quan đến hiệu quả kiểm chứng phía sau. Tuy nhiên, điểm đánh giá tự động chưa hoàn toàn thống nhất với con người; thí nghiệm kiểm chứng dùng bằng chứng chuẩn để tập trung đo ảnh hưởng của bước tách.
- **Liên hệ khóa luận:** Dùng để kiểm tra mô-đun tách quảng cáo thành từng thông số; mỗi ý nhỏ cần giữ đúng sản phẩm, phiên bản, giá trị và điều kiện của câu gốc.

## [11] [MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents](%5B11%5D.pdf) — 2024

- **Vấn đề:** Dùng LLM lớn để kiểm tra từng câu trong một câu trả lời có thể tốn nhiều thời gian và chi phí.
- **Cách làm:** Dùng GPT-4 tạo dữ liệu huấn luyện tổng hợp có lỗi khó và tình huống phải kết hợp nhiều câu bằng chứng; từ đó huấn luyện mô hình nhỏ chuyên kiểm tra một câu có được tài liệu hỗ trợ hay không.
- **Dữ liệu đánh giá:** Tổng hợp **10 bộ dữ liệu** thành **LLM-AggreFact**, bao gồm các tình huống như tóm tắt, hỏi–đáp và kiểm tra nội dung được LLM sinh ra.
- **Kết quả chính:** MiniCheck-FT5, khoảng **770 triệu tham số**, đạt chất lượng tổng thể tương đương GPT-4 với chi phí thấp hơn khoảng **400 lần** theo ước tính và thiết lập trong bài. Bài cũng cho thấy không phải lúc nào tách câu thành từng ý nhỏ cũng cần thiết để đạt kết quả tốt.
- **Liên hệ khóa luận:** Có thể tham khảo làm bộ kiểm tra dựa trên văn bản hoặc đối chứng gọn nhẹ. Kết quả trên bộ dữ liệu của bài chưa bảo đảm khả năng xử lý tiếng Việt hay phân biệt riêng lỗi lệch điều kiện.

## [12] [Fact-checking for Online Advertisement Posts](%5B12%5D.pdf) — 2024

- **Vấn đề:** Phát hiện quảng cáo làm đẹp/thẩm mỹ có thông tin không phù hợp với giấy phép, địa chỉ hoặc danh mục kỹ thuật đã đăng ký.
- **Dữ liệu:** Gồm **1.175 bài quảng cáo Facebook**, đối chiếu với thông tin đăng ký và được phê duyệt từ nguồn công khai của cơ quan quản lý tại TP.HCM.
- **Cách làm:** Dùng GPT-3.5 Turbo trích xuất thông tin cơ sở và kỹ thuật quảng cáo; kiểm tra giấy phép, địa chỉ bằng quy tắc; dùng biểu diễn ngữ nghĩa để so khớp từng kỹ thuật với danh mục được phép. Một nội dung không phù hợp có thể khiến cả quảng cáo bị đánh dấu.
- **Kết quả chính:** Cấu hình dùng BGE-M3 đạt **Accuracy 0,783**, **Precision 0,686** và **F1 0,703** trên dữ liệu thử nghiệm của bài.
- **Liên hệ khóa luận:** Gần về bối cảnh quảng cáo tiếng Việt và cách đối chiếu nguồn chính thức. Khóa luận chuyển sang thông số sản phẩm; độ giống ngữ nghĩa cần được bổ sung bằng so sánh giá trị, đơn vị và điều kiện áp dụng.

## [13] [Fathom: A Fast and Modular RAG Pipeline for Fact-Checking](%5B13%5D.pdf) — 2025

- **Vấn đề:** Xây dựng hệ thống kiểm chứng có bằng chứng với mô hình mở, tương đối nhỏ và thời gian xử lý phù hợp.
- **Cách làm:** Sinh câu hỏi–trả lời giả định để mở rộng truy vấn → tìm tài liệu bằng BM25 → xếp hạng lại theo độ gần ngữ nghĩa → dùng LLM dự đoán nhãn và giải thích. Các câu trả lời giả định phục vụ tìm kiếm, không tự trở thành bằng chứng thật.
- **Thử nghiệm:** Dùng AVeriTeC và kho tài liệu được cung cấp cho bài toán. Hệ thống trả bốn nhãn tương ứng AVeriTeC, gồm cả chưa đủ bằng chứng và bằng chứng mâu thuẫn/chọn lọc.
- **Kết quả chính:** Bảng 4 báo cáo điểm **New AVeriTeC (Ev2R) 0,2043**, so với **0,2023** của hệ thống cơ sở; thời gian **22,73 giây/tuyên bố**, so với **33,88 giây**. Hai lớp ít mẫu là chưa đủ bằng chứng và bằng chứng mâu thuẫn vẫn khó xử lý.
- **Lưu ý số liệu:** Phần tóm tắt mô tả mức tăng “0,99% absolute”, không khớp cách tính chênh lệch tuyệt đối từ Bảng 4. Bản tóm tắt này dùng trực tiếp các điểm trong bảng, không lặp lại cách diễn đạt đó.
- **Liên hệ khóa luận:** Tham khảo cách chia hệ thống thành mô-đun và dùng BM25 làm bước truy hồi ban đầu. Khóa luận vẫn cần kiểm tra riêng điều kiện sau khi tìm được đoạn nguồn liên quan.

## [14] [SemEval-2021 Task 8: MeasEval – Extracting Counts and Measurements and Their Related Contexts](%5B14%5D.pdf) — 2021

- **Vấn đề:** Chỉ trích được “17 mg” là chưa đủ; còn cần biết đó là lượng của cái gì, thuộc tính nào và trong hoàn cảnh nào.
- **Nhiệm vụ:** Trích xuất số lượng, đơn vị, dấu hiệu như xấp xỉ/khoảng giá trị, thực thể được đo, thuộc tính được đo và điều kiện bổ nghĩa; đồng thời nối đúng quan hệ giữa các thành phần.
- **Dữ liệu và đánh giá:** Bài mô tả dữ liệu văn bản khoa học tiếng Anh và một cuộc thi chung; đánh giá cả vị trí đoạn văn bản được trích lẫn quan hệ giữa các đoạn đó.
- **Kết quả chính:** Nhận diện con số và đơn vị tương đối dễ hơn nhận diện thực thể, thuộc tính, điều kiện và các quan hệ. Điều kiện bổ nghĩa là một trong những phần khó nhất.
- **Liên hệ khóa luận:** Là cơ sở cho cấu trúc trích xuất “sản phẩm/bộ phận – thông số – giá trị – đơn vị – điều kiện”. Đây là bài về trích xuất thông tin, chưa tự giải quyết việc gán nhãn đúng/sai cho quảng cáo.

## [15] [Get Your Vitamin C! Robust Fact Verification with Contrastive Evidence](%5B15%5D.pdf) — 2021

- **Vấn đề:** Mô hình kiểm chứng có thể dựa vào kiến thức nhớ sẵn hoặc kiểu câu, nên không đổi đáp án khi bằng chứng đã thay đổi một chi tiết quyết định.
- **Dữ liệu:** Xây dựng **VitaminC** từ hơn **100 nghìn lần sửa thông tin thực tế trên Wikipedia**, kết hợp dữ liệu tổng hợp để tạo hơn **400 nghìn cặp tuyên bố–bằng chứng**.
- **Cách làm:** Ghép cùng một tuyên bố với hai đoạn bằng chứng gần giống nhau về từ ngữ nhưng dẫn đến kết luận khác nhau. Mô hình phải nhận ra thay đổi nhỏ trong nội dung để đổi nhãn đúng.
- **Kết quả chính:** Trong phép thử được nêu ở phần mở đầu, mô hình huấn luyện bằng FEVER đổi dự đoán trên khoảng **56%** trường hợp đối lập; bổ sung VitaminC giúp tỷ lệ này lên **86%**. Huấn luyện với dữ liệu đối lập cũng cải thiện độ bền trước các ví dụ gây nhiễu.
- **Liên hệ khóa luận:** Là cơ sở xây dựng cặp tối thiểu, chẳng hạn chỉ thay “bật ANC” thành “tắt ANC” trong bằng chứng để xem hệ thống có đổi quyết định phù hợp không. Cần kiểm tra cả độ nhạy với thay đổi thật và sự ổn định khi chỉ đổi cách diễn đạt.

## [16] [The Probabilistic Relevance Framework: BM25 and Beyond](%5B16%5D.pdf) — 2009

- **Nội dung:** Bài tổng quan lý thuyết về xếp hạng tài liệu theo mức độ liên quan đến truy vấn, giải thích cơ sở của BM25 và các mô hình liên quan.
- **Ý chính của BM25:** Chấm điểm dựa trên từ trùng giữa truy vấn và tài liệu; cân nhắc độ hiếm của từ, số lần xuất hiện và độ dài tài liệu. Một từ lặp thêm nhiều lần chỉ tăng điểm tới mức bão hòa, không tăng mãi theo tỷ lệ thẳng.
- **Mở rộng:** Trình bày BM25F để xử lý tài liệu có nhiều trường như tiêu đề và nội dung; thảo luận phản hồi liên quan, đặc trưng ngoài văn bản và cách tối ưu tham số.
- **Điểm cần nhớ:** BM25 là công cụ tìm/xếp hạng tài liệu liên quan, không phải bộ quyết định đúng–sai. Đoạn có điểm cao vẫn có thể mô tả sai phiên bản sản phẩm hoặc một điều kiện khác.
- **Liên hệ khóa luận:** Dùng làm nền tảng chọn top-k đoạn nguồn. Việc giữ thông số cùng điều kiện khi chia đoạn và đo Recall@k cần được đánh giá trên dữ liệu khóa luận; đó là bước vận dụng, không phải kết quả thực nghiệm sẵn có của bài này.
