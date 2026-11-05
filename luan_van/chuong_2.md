# Chương 2. Tổng quan và cơ sở lý thuyết

Chương này khảo sát các hướng nghiên cứu liên quan đến bài toán đã nêu ở mục 1.2, đồng thời trình bày những cơ sở lý thuyết mà các chương sau sử dụng. Các mục 2.1 đến 2.7 đi lần lượt từ kiểm chứng thông tin nói chung đến kiểm chứng quảng cáo. Mục 2.8 định nghĩa các độ đo đánh giá. Mục 2.9 tổng hợp hạn chế của các nghiên cứu và cách đề tài xử lý. Mỗi số liệu dưới đây chỉ có ý nghĩa trong dữ liệu, mô hình và độ đo của nghiên cứu đó, nên không dùng để xếp hạng các phương pháp với nhau.

## 2.1. Kiểm chứng thông tin tự động

Kiểm chứng thông tin tự động (automated fact-checking) là bài toán xác định một tuyên bố có được bằng chứng (evidence) ủng hộ hay không. Hệ thống thường làm hai việc nối tiếp: truy hồi bằng chứng từ một kho văn bản, rồi gán nhãn cho tuyên bố dựa trên bằng chứng đó. Hai việc này có thể sai độc lập với nhau, nên các nghiên cứu thường đo riêng từng việc.

FEVER là bộ dữ liệu đặt nền cho bài toán này. Thorne và cộng sự lấy câu từ Wikipedia rồi viết lại hoặc biến đổi thành 185.445 tuyên bố [2, tr. 1]. Hệ thống phải tìm câu bằng chứng trong Wikipedia, rồi gán một trong ba nhãn: được ủng hộ (Supported), bị bác bỏ (Refuted) hoặc không đủ thông tin (Not Enough Info, NEI) [2, tr. 3]. Hệ thống cơ sở (baseline) của bài đạt 31,87% khi phải đúng cả nhãn lẫn bằng chứng, và 50,91% khi chỉ cần đúng nhãn [2, tr. 1]. Khoảng cách giữa hai con số cho thấy đoán đúng nhãn là chưa đủ; hệ thống còn phải chỉ ra đúng bằng chứng. Đề tài kế thừa yêu cầu này: mỗi kết luận phải kèm đoạn nguồn.

Hệ ba nhãn của FEVER được nhiều nghiên cứu sau dùng lại, trong đó có các bộ dữ liệu tiếng Việt ở mục 2.6. Hệ nhãn này không có lớp riêng cho tuyên bố đúng con số nhưng sai điều kiện. Điều đó không có nghĩa mô hình ba nhãn chắc chắn sẽ chấp nhận nhầm các tuyên bố ấy, vì mô hình vẫn có thể trả Refuted hoặc NEI khi điều kiện không khớp. Mức chấp nhận nhầm thực tế là điều đề tài đo bằng đối chứng B0.

AVeriTeC chuyển từ tuyên bố nhân tạo sang tuyên bố thật. Schlichtkrull và cộng sự thu thập 4.568 tuyên bố do 50 tổ chức kiểm chứng đã xử lý, với bằng chứng tìm trên web và biểu diễn bằng các cặp hỏi–đáp [3, tr. 1, 3]. Bộ dữ liệu thêm nhãn thứ tư là Conflicting Evidence/Cherry-picking, gộp hai trường hợp: bằng chứng vừa ủng hộ vừa bác bỏ tuyên bố, hoặc tuyên bố đúng về mặt kỹ thuật nhưng gây hiểu nhầm vì bỏ qua ngữ cảnh quan trọng [3, tr. 3–4]. Trường hợp sau rất gần với lỗi mà đề tài quan tâm. Tuy nhiên, nhãn này không đồng nhất với Lệch điều kiện: trong đề tài, tài liệu ghi mâu thuẫn thuộc nhãn Chưa đủ thông tin, còn Lệch điều kiện chỉ dành cho tuyên bố bỏ hoặc đổi điều kiện.

Lớp gây hiểu nhầm là lớp khó ngay với các hệ thống gần đây. Fathom của Rashid và Hakak là một quy trình kết hợp truy hồi với mô hình sinh (retrieval-augmented generation, RAG) cho AVeriTeC. Hệ thống sinh các cặp hỏi–đáp giả định để mở rộng ngữ cảnh của tuyên bố (HyDE-QA), lấy ứng viên bằng BM25, xếp hạng lại bằng biểu diễn vectơ (embedding), rồi để LLM dự đoán nhãn [13, tr. 2–4]. Trên tập phát triển của AVeriTeC, Fathom đạt F1 0,8436 ở nhãn Refuted và 0,6877 ở nhãn Supported, nhưng F1 bằng 0 ở nhãn Conflicting Evidence/Cherry-picking [13, tr. 5]. Tập này chỉ có 38 tuyên bố thuộc nhãn đó [13, tr. 2], và đây là kết quả của một hệ thống. Kết quả là động lực để khảo sát lớp gây hiểu nhầm, không chứng minh rằng mọi hệ thống bốn nhãn đều thất bại.

Một hướng khác giảm phần việc giao cho LLM bằng cách đưa suy luận vào chương trình. ProgramFC của Pan và cộng sự cho LLM sinh một chương trình chia việc kiểm chứng thành các tác vụ con, mỗi tác vụ gọi một hàm, rồi thực thi để lấy kết luận [18, tr. 3–4]. Trên FEVEROUS-S ở thiết lập phải tự tìm bằng chứng, cấu hình N = 5 đạt macro-F1 68,06 [18, tr. 6]. Dấu vết thực thi giúp phân tích lỗi. Khác với đề tài, chương trình của ProgramFC do mô hình sinh ra cho từng tuyên bố, còn quy tắc của bộ quyết định được viết sẵn và cố định. Vì ProgramFC và VeriFin (mục 2.3) đã tồn tại, đề tài không coi việc kết hợp LLM với mã nguồn tự nó là điểm mới.

## 2.2. Truy hồi bằng chứng và BM25

Truy hồi bằng chứng (evidence retrieval) chọn từ kho tài liệu những đoạn liên quan đến tuyên bố để đưa cho bước gán nhãn. Chất lượng của bước này ảnh hưởng trực tiếp đến kết quả cuối. Với ViWikiFC, mô hình InfoXLMLarge đạt F1 86,51% ở bước gán nhãn, còn toàn bộ quy trình dùng BM25 và InfoXLMLarge chỉ đạt strict accuracy 67,00% [19, tr. 1]. Hai chỉ số này đo hai đại lượng khác nhau nên không thể lấy hiệu của chúng làm mức lỗi do truy hồi. Điều rút ra là cần báo cáo cả kết quả của từng bước lẫn kết quả đầu–cuối.

BM25 là hàm xếp hạng cổ điển trong khung truy hồi xác suất (probabilistic relevance framework) của Robertson và Zaragoza. Điểm của một tài liệu d với truy vấn Q là tổng trọng số của các từ t trong Q [16, tr. 29–30]:

Điểm(d, Q) = Σ [ tf / (k1 · ((1 − b) + b · dl / avdl) + tf) ] · w(t)     (2.1)

Trong công thức (2.1), tf là số lần từ t xuất hiện trong d, dl là độ dài của d, avdl là độ dài trung bình của các tài liệu trong kho, còn w(t) là trọng số Robertson–Spärck Jones của từ t. Khi không có thông tin về mức liên quan, w(t) rút về một dạng của nghịch đảo tần suất tài liệu (inverse document frequency, idf) [16, tr. 30]. Công thức thể hiện ba ý. Từ càng hiếm trong kho thì càng đóng góp nhiều điểm. Số lần xuất hiện của một từ tăng thì điểm tăng nhưng chậm dần và có giới hạn, gọi là bão hòa. Tài liệu dài bị điều chỉnh để không được lợi chỉ vì dài.

Hai tham số k1 và b điều chỉnh mức bão hòa và mức chuẩn hóa độ dài. Mô hình không chỉ ra cách đặt hai tham số này; các tác giả cho biết thực nghiệm thường thấy giá trị 0,5 < b < 0,8 và 1,2 < k1 < 2 cho kết quả khá tốt [16, tr. 30]. Khi có truy vấn và nhãn liên quan, có thể tối ưu tham số trên chính dữ liệu đó.

Đề tài dùng BM25 làm phương pháp truy hồi nền, theo cách dùng ở giai đoạn đầu của Fathom [13, tr. 3–4] nhưng không tái lập các bước còn lại của hệ thống này. Hệ thống chỉ tìm trong tài liệu của mẫu sản phẩm người dùng đã chọn và lấy k đoạn có điểm cao nhất. Kho tìm kiếm vì vậy nhỏ, và tên thuộc tính, đơn vị đo là những từ khóa rõ. Giá trị k và cách tách từ được chọn trên tập phát triển.

BM25 có một giới hạn quan trọng với bài toán này: hàm chỉ xếp hạng theo mức liên quan về từ vựng, không cho biết tuyên bố đúng hay sai, cũng không bảo đảm đoạn được chọn có chứa điều kiện đi kèm giá trị. Trên trang thông số, điều kiện thường nằm ở chú thích cách xa con số. Vì vậy, khi chia tài liệu thành đoạn, đề tài nối chú thích vào đoạn mang ký hiệu chú thích tương ứng, để con số và điều kiện nằm cùng một đoạn. Chất lượng truy hồi được đo riêng bằng Recall@k (mục 2.8).

## 2.3. Tuyên bố số liệu và biểu diễn số đo

Một con số trong tuyên bố chỉ kiểm chứng được khi xét cùng đơn vị, đối tượng được đo và điều kiện đi kèm. Bốn nghiên cứu dưới đây làm rõ các khía cạnh khác nhau của yêu cầu này.

NumPert của Aarnes và Setty kiểm tra độ vững của mô hình ngôn ngữ khi con số trong tuyên bố bị thay đổi có kiểm soát. Từ bộ dữ liệu QuanTemp, các tác giả áp dụng sáu nhóm biến đổi, phân biệt phép giữ nguyên nhãn với phép đổi nhãn từ True sang False, và kiểm tra thủ công tính hợp lệ của biến thể [8, tr. 3–4]. Ảnh hưởng khác nhau rõ rệt theo phép biến đổi, mô hình và câu lệnh. Chẳng hạn, trên phần tuyên bố có nhãn True, ở thiết lập zero-shot với phép Mask, độ chính xác (accuracy) của GPT-4o giảm từ 80,00% xuống 19,25%, còn của GPT-4o-Mini giảm 74,12 điểm phần trăm [8, tr. 5]. Kết quả này không chứng minh mọi phép so sánh số đều cần công cụ riêng, nhưng cho thấy để LLM tự so con số là thiếu ổn định. Vì vậy, đề tài chuẩn hóa giá trị, đơn vị và so sánh chúng bằng mã Python.

VeriFin của Hall và cộng sự thay việc để LLM tự kết luận bằng phép kiểm tra có nguồn. Với câu trả lời số liệu tài chính, hệ thống lấy dữ kiện từ báo cáo dạng XBRL, một định dạng mà mỗi chỉ tiêu được gắn thẻ riêng, xác lập phép tính cần dùng, rồi dùng bộ giải ràng buộc Z3 để trả về một trong ba kết quả: Verified, Violated hoặc Abstain [9, tr. 1, 3–4]. Trên bộ XBRLFiling gồm 600 câu hỏi về 28 công ty, với câu trả lời ứng viên do Claude Haiku 4.5 sinh, VeriFin không chấp nhận nhầm câu nào trong 92 câu sai, nhưng từ chối 46 câu đúng [9, tr. 1, 7]. Các phương pháp đối chứng chấp nhận nhầm từ 6 đến 92 câu, trong đó 92 là trường hợp nhận mọi câu trả lời mà không kiểm chứng [9, tr. 2, 7]. Số 0 ở đây là quan sát trong thí nghiệm, không phải bảo đảm tuyệt đối, và đây là bản tiền công bố (preprint). Đề tài học từ VeriFin hai điều: neo nguồn trước khi quyết định, và báo cáo đồng thời số câu sai bị chấp nhận lẫn số câu đúng bị từ chối. Điểm khác là VeriFin dựa trên dữ kiện đã có cấu trúc, còn trang thông số và quảng cáo là văn bản tự do.

MeasEval của Harper và cộng sự là cơ sở tham khảo về việc biểu diễn số đo cùng ngữ cảnh. Lược đồ gán nhãn gồm giá trị (Quantity), đơn vị (Unit), từ bổ nghĩa (Modifier), đối tượng (MeasuredEntity), thuộc tính (MeasuredProperty) và thông tin ngữ cảnh (Qualifier) [14, tr. 2–5]. Trong dữ liệu từ 110 bài báo khoa học, độ đồng thuận Krippendorff's alpha của Qualifier chỉ đạt 0,334, thấp xa so với 0,866 của Unit [14, tr. 3]. Đội dẫn đầu đạt F1 tổng thể 0,519, riêng Qualifier chỉ đạt 0,163 [14, tr. 5]. Các con số này cho thấy ngữ cảnh đi kèm số đo khó gán nhất quán và khó trích xuất, đúng với khó khăn mà đề tài gặp. MeasEval chỉ gán nhãn đoạn văn và quan hệ, không kết luận tuyên bố đúng hay sai, và không định nghĩa sáu loại điều kiện của thông số sản phẩm. Đề tài tự xây danh mục điều kiện và quy tắc quyết định.

VitaminC của Schuster và cộng sự cung cấp ý tưởng về cặp ví dụ tương phản. Bài toán đặt ra là mô hình phải nhạy với những thay đổi của bằng chứng làm đổi sự thật, thay vì dựa vào kiến thức đã nhớ hoặc sự trùng từ [15, tr. 1–3]. Khi huấn luyện thêm trên VitaminC, tỷ lệ tuyên bố mà mô hình ALBERT-xlarge đổi dự đoán khi gặp bằng chứng tương phản tăng từ 64,59% lên 90,94% [15, tr. 8]. Đề tài dùng ý tưởng này cho tập cặp tối thiểu, với một khác biệt: VitaminC chủ yếu đổi bằng chứng, còn đề tài giữ tài liệu của hãng cố định và đổi tuyên bố (bỏ hoặc đổi điều kiện, đổi bộ phận, đổi kiểu giá trị, đổi giá trị, đổi phiên bản). Nhãn của mỗi biến thể được kiểm tra thủ công.

## 2.4. Ảo giác của LLM và kiểm tra văn bản do LLM tạo

Trong khóa luận, ảo giác được hiểu theo nghĩa thiếu trung thành với nguồn: văn bản sinh ra chứa thông tin không được nguồn đầu vào hỗ trợ. Thông tin như vậy không nhất thiết sai ngoài thực tế [1, tr. 1–3]. Vì thế, đề tài không coi mọi thông tin vắng trong tài liệu là Sai, mà tách riêng nhãn Chưa đủ thông tin.

Một cách đo phổ biến là chia văn bản thành các đơn vị nhỏ rồi kiểm từng đơn vị. FActScore của Min và cộng sự tách văn bản do mô hình sinh thành các sự kiện nguyên tử, rồi tính tỷ lệ sự kiện được nguồn hỗ trợ [17, tr. 3]. Trên tiểu sử do mô hình viết, ChatGPT đạt 58,3% so với Wikipedia [17, tr. 4]. Cách đo này cho biết lỗi nằm ở đâu thay vì gán một nhãn cho cả văn bản, và đề tài áp dụng tinh thần đó khi gán nhãn cho từng tuyên bố. Tuy nhiên, tỷ lệ được hỗ trợ không tách riêng trường hợp lệch điều kiện.

MiniCheck của Tang và cộng sự kiểm tra từng câu do LLM viết có được tài liệu nền (grounding document) hỗ trợ hay không. Mô hình gán hai nhãn Supported và Unsupported, trong đó Unsupported gộp cả không được hỗ trợ lẫn mâu thuẫn [11, tr. 2]. Mô hình MiniCheck-FT5 có 770 triệu tham số, huấn luyện trên dữ liệu tổng hợp, đạt độ chính xác cân bằng (balanced accuracy, BAcc) 74,7 so với 75,3 của GPT-4 [11, tr. 7]. Chi phí suy luận theo cách quy đổi của bài là 0,24 USD so với 107 USD trên khoảng 13 nghìn mẫu [11, tr. 7–8]. Hai nhãn này không đủ để phân biệt sai giá trị với lệch điều kiện.

Việc tách tuyên bố cần được đo riêng vì có thể làm hỏng ý nghĩa ban đầu. FactLens của Mitra và cộng sự chấm phép tách theo sáu tiêu chí, gồm tính nguyên tử (atomicity), tính đủ (sufficiency), không thêm thắt (fabrication), độ bao phủ (coverage), không thừa (redundancy) và tính dễ đọc (readability) [10, tr. 2–3]. Bài nêu ví dụ biến một mệnh đề điều kiện thành sự kiện độc lập là lỗi fabrication [10, tr. 3]. Đây chính là rủi ro của đề tài, vì tách tuyên bố mà bỏ điều kiện sẽ làm đổi nhãn. Vì vậy, đề tài giữ sản phẩm, phiên bản, bộ phận và điều kiện trong từng tuyên bố, và đo bước tách tự động bằng Precision, Recall so với tuyên bố tách thủ công. Tách nhỏ hơn cũng không mặc nhiên tốt hơn: trong thiết lập của MiniCheck, tách câu làm BAcc của MiniCheck-FT5 giảm 1,4 điểm [11, tr. 8].

## 2.5. Tuyên bố nửa sự thật và cách người đọc hiểu

Tuyên bố nửa sự thật (half-truth) là tuyên bố có phần được nói ra có thể đúng, nhưng phần bị bỏ làm thay đổi cách người đọc hiểu [4, tr. 1–3]. Đây là hướng nghiên cứu gần nhất với nhãn Lệch điều kiện về mặt khái niệm.

Tang và cộng sự xây dựng bộ PolitiFact-Hidden gồm 14.994 phát biểu chính trị với ba nhãn True, Half-True và False; việc gán nhãn có GPT-4o-mini hỗ trợ và người kiểm tra chất lượng [4, tr. 4–5]. Hệ thống TRACER của nhóm là một mô-đun gắn thêm vào hệ thống kiểm chứng có sẵn. TRACER căn chỉnh bằng chứng có sẵn với phát biểu, suy ra ý định của phát biểu, rồi đánh giá bằng chứng bị ẩn có làm đổi ý định đó hay không [4, tr. 5–6]. Khi gắn vào HiSS, một phương pháp kiểm chứng dựa trên câu lệnh, TRACER nâng F1 của nhãn Half-True trên tập kiểm tra từ 44,4 lên 60,5, tức tăng 16,1 điểm [4, tr. 7–8]. Bài toán của đề tài có một đặc điểm khác: hãng đã ghi điều kiện trong tài liệu, nên có thể khai báo trước các loại điều kiện cần đối chiếu thay vì phải suy ra ý định. Hướng này có hiệu quả hơn hay không phải được xác nhận bằng thực nghiệm.

Beyond Binary của Albertson và cộng sự cho thấy sắc thái của ngữ cảnh ảnh hưởng đến kết quả kiểm chứng. Trên 6.000 phát biểu cân bằng từ PolitiFact, mô hình chỉ dùng tuyên bố đạt độ chính xác 60%, còn phương pháp MEGA khi thêm sắc thái vào đoạn bằng chứng đạt 75% [20, tr. 4–6]. Thí nghiệm không xét điều kiện của thông số, nhưng kiểu thiết kế thay đổi một yếu tố rồi quan sát ảnh hưởng là điều đề tài áp dụng cho tập cặp tối thiểu.

Với quảng cáo, câu hỏi đặt ra là người đọc thực sự hiểu cụm “lên đến” như thế nào. Báo cáo của Hastak và Murphy gửi FTC năm 2012 phỏng vấn 360 người tại các trung tâm thương mại ở Hoa Kỳ về ba phiên bản quảng cáo cửa sổ tiết kiệm năng lượng [21, tr. 3–4]. Trong nhóm xem quảng cáo “up to 47%”, 36,0% trả lời rằng quảng cáo nói tiết kiệm 47% mà không nhắc giới hạn. Trong nhóm xem quảng cáo ghi thẳng “47%”, tỷ lệ này là 47,8%, và chênh lệch giữa hai nhóm không có ý nghĩa thống kê ở mức p < 0,05 [21, tr. 7]. Nói cách khác, cụm “up to” không làm giảm rõ rệt số người ghi nhận con số 47% như một mức không kèm giới hạn. Kết quả nói về cách tiếp nhận thông điệp, thuộc một loại sản phẩm và một thị trường khác, nên đề tài chỉ dùng làm động lực để khảo sát cách hiểu của người đọc tiếng Việt, không dùng để suy ra cách hiểu của người mua Việt Nam.

## 2.6. Kiểm chứng tiếng Việt

Kiểm chứng tiếng Việt đã có một số bộ dữ liệu và hệ thống, đều dùng ba nhãn tương tự FEVER và thuộc miền tin tức hoặc Wikipedia. Các nghiên cứu này cung cấp cơ sở về dữ liệu và đối chứng, nhưng chưa đánh giá riêng điều kiện của thông số kỹ thuật.

ViFactCheck của Hoa và cộng sự gồm 7.232 cặp tuyên bố và bằng chứng do người gán nhãn, lấy từ báo điện tử thuộc 12 chủ đề [5, tr. 1, 3]. Mô hình Gemma đã tinh chỉnh đạt macro-F1 89,90% khi được đưa sẵn bằng chứng và 85,94% khi nhận toàn bộ ngữ cảnh [5, tr. 5]. Các con số này chưa tính chất lượng truy hồi.

ViNumFCR của Luong và cộng sự tập trung vào tuyên bố có số liệu, gồm 10.008 cặp thuộc 12 chủ đề tin tức từ VnExpress [6, tr. 3–5]. Mô hình XLM-R Large đã tinh chỉnh đạt độ chính xác 90,05%, còn Gemma-2 đã tinh chỉnh đạt 88,96% [6, tr. 7]. Bộ dữ liệu xét thao tác số và suy luận ngôn ngữ trên con số, nhưng nhãn của bài không tách riêng nguyên nhân lệch điều kiện.

SemViQA của Tran và cộng sự là hệ thống kiểm chứng tiếng Việt trên hai bộ ISE-DSC01 và ViWikiFC. Hệ thống chia ngữ cảnh dài thành các đoạn khoảng 400 token, dùng TF-IDF cho trường hợp dễ và mô hình hỏi–đáp phân loại token (Question Answering Token Classification, QATC) để chọn bằng chứng cho trường hợp khó, rồi gán nhãn qua hai bước nối tiếp [7, tr. 4–5]. Hệ thống đạt strict accuracy 78,97% trên ISE-DSC01, 80,82% trên ViWikiFC và đứng đầu cuộc thi UIT Data Science Challenge [7, tr. 1, 6–7]. Đề tài dùng mô hình ba nhãn của SemViQA làm đối chứng B3, đại diện cho hệ thống tiếng Việt sẵn có. Mô hình này được huấn luyện trên tin tức và Wikipedia nên sẽ chạy ngoài miền huấn luyện khi áp vào quảng cáo.

ViWikiFC của Le và cộng sự gồm 20.916 tuyên bố do người viết dựa trên Wikipedia tiếng Việt [19, tr. 1]. Như đã nêu ở mục 2.2, bài báo cáo cả kết quả từng bước lẫn kết quả khi tính cả truy hồi.

## 2.7. Kiểm chứng quảng cáo và mô tả sản phẩm

Hai nghiên cứu gần nhất với miền ứng dụng của đề tài là nghiên cứu về mô tả sản phẩm của Jiang và cộng sự, và nghiên cứu về quảng cáo tiếng Việt của Nguyen và cộng sự.

Jiang và cộng sự phát hiện giá trị mà LLM thêm vào mô tả sản phẩm nhưng không trung thành với dữ liệu đầu vào. Bộ DS có 200 mô tả với thuộc tính có cấu trúc, bộ DU có 4.042 mô tả với thuộc tính viết tự do, và chuyên gia gán nhãn ảo giác ở cấp thuộc tính [1, tr. 6]. Quy trình dùng các phép so khớp rẻ để lọc những chỗ nghi ngờ, rồi để LLM xác nhận [1, tr. 3–5]. Cách làm cho kết quả tốt với thuộc tính ngắn và rõ, còn với thuộc tính viết tự do thì Precision thấp vì khó phân biệt suy luận hợp lý với ảo giác [1, tr. 6–8]. Đề tài học từ bài này cách đối chiếu với nguồn riêng của từng sản phẩm, nhưng cần thêm quy tắc để tách sai giá trị với lệch điều kiện.

Nguyen và cộng sự kiểm chứng bài quảng cáo dịch vụ làm đẹp trên Facebook tiếng Việt. Dữ liệu gồm 1.175 bài của 283 cơ sở, trong đó 246 bài bị gán nhãn vi phạm [12, tr. 6]. GPT-3.5 Turbo trích số giấy phép, địa chỉ và danh sách dịch vụ, rồi hệ thống so với dữ liệu trên cổng thông tin hoạt động y tế của Thành phố Hồ Chí Minh; danh sách dịch vụ được so bằng độ tương đồng cosine trên biểu diễn vectơ với một ngưỡng [12, tr. 3–6]. Với mô hình BGE-M3 ở ngưỡng 0,4, hệ thống đạt độ chính xác 0,783, Precision 0,686 và F1 0,703 [12, tr. 8]. Đây là tiền lệ gần về dùng LLM trích thông tin từ quảng cáo tiếng Việt và đối chiếu với nguồn chính thức. Đề tài khác ở hai điểm: gán nhãn cho từng tuyên bố thay vì cả bài, và so theo điều kiện cùng giá trị đã chuẩn hóa thay vì theo độ tương đồng.

## 2.8. Các độ đo đánh giá

Các độ đo dưới đây được dùng ở Chương 4. Với một nhãn L, gọi TP là số tuyên bố có nhãn chuẩn L và được dự đoán là L, FP là số tuyên bố có nhãn chuẩn khác L nhưng được dự đoán là L, FN là số tuyên bố có nhãn chuẩn L nhưng được dự đoán là nhãn khác.

Precision = TP / (TP + FP)     (2.2)

Recall = TP / (TP + FN)     (2.3)

F1 = 2 · Precision · Recall / (Precision + Recall)     (2.4)

Precision cho biết trong các dự đoán L có bao nhiêu dự đoán đúng. Recall cho biết hệ thống tìm được bao nhiêu trong số các tuyên bố thực sự mang nhãn L. F1 là trung bình điều hòa của hai chỉ số, và Macro-F1 là trung bình cộng F1 của các nhãn, nên mỗi nhãn có trọng số như nhau dù ít hay nhiều mẫu. Độ chính xác (accuracy) là tỷ lệ dự đoán đúng trên tổng số mẫu; độ đo này dễ bị các nhãn đông mẫu chi phối.

Tỷ lệ chấp nhận nhầm là độ đo chính của đề tài, vì sai lầm tốn kém nhất là để một tuyên bố không đúng lọt qua với nhãn Đúng:

FAR = (số tuyên bố có nhãn chuẩn khác Đúng nhưng bị gán Đúng) / (số tuyên bố có nhãn chuẩn khác Đúng)     (2.5)

FAR thấp một mình chưa đủ, vì một hệ thống không bao giờ gán Đúng sẽ có FAR bằng 0. Do đó FAR luôn được báo cùng Recall của nhãn Đúng. VeriFin cũng báo cáo đồng thời hai mặt này ở mục 2.3.

Recall@k đo chất lượng truy hồi: tỷ lệ tuyên bố có đoạn bằng chứng cần thiết nằm trong k đoạn được xếp hạng cao nhất.

Độ tin cậy của nhãn chuẩn được đo bằng hệ số kappa của Cohen [25], dùng để so hai lượt gán trên cùng một tập tuyên bố:

κ = (po − pe) / (1 − pe)     (2.6)

Trong công thức (2.6), po là tỷ lệ tuyên bố mà hai lượt gán giống nhau, còn pe là tỷ lệ giống nhau mong đợi do ngẫu nhiên. Các phép ước lượng khoảng tin cậy và kiểm định được trình bày ở Chương 4.

## 2.9. Hạn chế của các nghiên cứu và hướng của đề tài

Các nghiên cứu đã khảo sát cung cấp nền tảng về hệ nhãn, truy hồi, biểu diễn số liệu và kiểm tra văn bản do LLM tạo, nhưng chưa nghiên cứu nào trong số đó biểu diễn riêng các loại điều kiện của thông số như chế độ hoạt động, bộ phận, phụ kiện, điều kiện đo, phiên bản và kiểu giá trị. MeasEval có thành phần Qualifier cho ngữ cảnh của số đo nhưng không có quy tắc kết luận nhãn. Nhận định này chỉ áp dụng cho các tài liệu đã khảo sát đến ngày 15/10/2026, không phải kết luận về toàn bộ lĩnh vực.

Từ các hạn chế đó, đề tài chọn ba hướng xử lý. Thứ nhất, liệt kê trước các loại điều kiện trong tệp cấu hình của từng nhóm sản phẩm, thay vì suy đoán phần thông tin bị bỏ, vì hãng đã ghi điều kiện trong tài liệu. Thứ hai, trích xuất có neo nguồn, để mọi giá trị và điều kiện do LLM trích ra đều được mã nguồn kiểm tra với câu gốc. Thứ ba, quyết định nhãn bằng quy tắc xác định trước thay vì để LLM tự gán. Bảng 2.1 đối chiếu từng hạn chế với cách xử lý và nơi đo kết quả. Cột “Cách đề tài xử lý” là lựa chọn thiết kế; lợi ích của các lựa chọn này là giả thuyết, được kiểm tra ở Chương 4.

**Bảng 2.1.** Hạn chế của các nghiên cứu liên quan và cách đề tài xử lý

| Nghiên cứu | Hạn chế với bài toán của đề tài | Cách đề tài xử lý | Nơi đo |
|---|---|---|---|
| FEVER [2] | Ba nhãn, không có lớp riêng cho tuyên bố đúng con số nhưng sai điều kiện | Thêm nhãn Lệch điều kiện; dùng hệ ba nhãn làm đối chứng B0 | FAR của P so với B0 |
| AVeriTeC [3], Fathom [13] | Nhãn gây hiểu nhầm gộp cả xung đột bằng chứng và bỏ ngữ cảnh, không gắn với điều kiện cụ thể; Fathom đạt F1 bằng 0 ở nhãn này [13, tr. 5] | Tách hai hiện tượng: tài liệu ghi mâu thuẫn là Chưa đủ thông tin; tuyên bố bỏ hoặc đổi điều kiện là Lệch điều kiện | Đối chứng B2; F1 nhãn Lệch điều kiện |
| Tang và cộng sự [4] | Suy ra ý định và phần bị lược bỏ; không có danh mục khai báo trước những gì có thể bị bỏ | Khai báo sáu loại điều kiện trong tệp cấu hình; gặp cụm điều kiện ngoài cấu hình thì không kết luận Đúng | Độ bao phủ của cấu hình |
| ViFactCheck [5], SemViQA [7], ViWikiFC [19] | Tin tức và Wikipedia, ba nhãn, không thuộc miền thông số sản phẩm | Xây bộ dữ liệu quảng cáo tiếng Việt cho ba nhóm thiết bị; đo riêng truy hồi và quyết định, rồi đo đầu–cuối | Recall@k; đối chứng B3 |
| ViNumFCR [6], NumPert [8] | Xét con số, không xét điều kiện đi kèm; so con số bằng mô hình ngôn ngữ thiếu ổn định | So giá trị, đơn vị và hướng thuận lợi bằng quy tắc tất định, không giao cho LLM | Kiểm thử bộ quyết định; biến thể đổi giá trị |
| MiniCheck [11], Jiang và cộng sự [1] | Hai nhãn, hoặc lọc bằng độ tương đồng rồi để LLM xác nhận; chưa tách sai giá trị với lệch điều kiện | Bốn nhãn; mỗi tuyên bố có đoạn nguồn và lý do chỉ ra điều kiện bị bỏ hoặc đổi | F1 nhãn Lệch điều kiện |
| VeriFin [9] | Kiểm tra tất định nhưng dựa trên dữ kiện có cấu trúc của miền tài chính | Nối chú thích vào đoạn khi chia tài liệu; LLM trích bộ thông số có neo nguồn từ văn bản tự do, rồi bộ quyết định kết luận | Bản bỏ neo nguồn P−NN |
| Nguyen và cộng sự [12] | Nhãn cấp bài; so danh mục theo độ tương đồng với ngưỡng | Nhãn cho từng tuyên bố; so theo điều kiện và giá trị đã chuẩn hóa | Bản bỏ đối chiếu điều kiện P−ĐK |
| MeasEval [14] | Lược đồ biểu diễn số đo, không có quy tắc kết luận nhãn | Tự xây danh mục sáu loại điều kiện và quy tắc quyết định | Kiểm thử tệp cấu hình |
| VitaminC [15] | Cặp tương phản chủ yếu đổi bằng chứng | Tập cặp tối thiểu đổi tuyên bố, giữ nguyên tài liệu của hãng; kiểm tra nhãn thủ công | Kết quả trên tập cặp tối thiểu |
| Báo cáo FTC [21] | Khảo sát quảng cáo cửa sổ tại Hoa Kỳ, không suy rộng sang người mua Việt Nam | Khảo sát cách hiểu của người đọc tiếng Việt; tính lại kết quả khi đổi cách hiểu thông thường | Phân tích độ nhạy |

## 2.10. Kết chương

Chương này cho thấy ba điều làm nền cho phần phương pháp. Thứ nhất, lớp gây hiểu nhầm là lớp khó, và các hệ nhãn hiện có chưa gắn lớp này với điều kiện cụ thể của thông số. Thứ hai, truy hồi, trích xuất và quyết định có thể sai độc lập, nên phải đo riêng từng bước và báo cáo cả kết quả đầu–cuối. Thứ ba, các công cụ như BM25, trích xuất bằng LLM, kiểm chứng qua mã nguồn và cặp tương phản đều đã có tiền lệ, nên điều cần chứng minh là lợi ích của việc đối chiếu điều kiện trong bộ quyết định. Chương 3 trình bày phương pháp P dựa trên các nhận định này.

## Ghi chú cho người duyệt

Mục này không đưa lên Google Doc.

- Viết lại toàn bộ ngày 05/11/2026 (Opus), thay bản do Sonnet viết ngày 03/11/2026. Đổi tên chương cho khớp Phụ lục 2 của Khoa (TỔNG QUAN). Danh mục tài liệu đầy đủ ở `luan_van/tai_lieu_tham_khao.md`; mã BS1–BS5 cũ thành [17]–[21].
- Mục 2.8 và công thức BM25 là phần mới so với bản cũ. Công thức (2.1) viết gộp từ (3.12)–(3.15) của [16].
- Số liệu trích dẫn được đối chiếu tự động với văn bản PDF ngày 05/11/2026.
- Khi hoàn thiện danh mục tài liệu theo quy định của Khoa (tách tiếng Việt, tiếng Anh, xếp theo alphabet), phải đánh lại toàn bộ số trích dẫn bằng script.
