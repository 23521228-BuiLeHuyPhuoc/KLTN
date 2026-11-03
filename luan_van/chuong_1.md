# Chương 1. Tổng quan

## 1.1. Bối cảnh

Kiểm chứng thông số kỹ thuật là yêu cầu đặt ra khi sử dụng mô hình ngôn ngữ lớn (large language model, LLM) để viết quảng cáo sản phẩm. Nghiên cứu của Jiang và cộng sự cho thấy nội dung mô tả sản phẩm được LLM bổ sung có thể chứa thông tin không được dữ liệu đầu vào hỗ trợ, thuộc vấn đề ảo giác (hallucination) xét theo mức trung thành với nguồn [1, tr. 1–3]. Trong khóa luận này, căn cứ kiểm chứng là tài liệu chính hãng của sản phẩm được quảng cáo.

Thông số kỹ thuật có điều kiện ràng buộc đòi hỏi xem xét đồng thời giá trị và hoàn cảnh áp dụng. Một tuyên bố (claim) có thể giữ nguyên con số nhưng bỏ điều kiện ràng buộc (constraint), khiến ý nghĩa khác với công bố ban đầu. Ví dụ trong đề cương, iPhone 17 được mô tả là “sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên”. Câu quảng cáo “sạc 50% chỉ trong 20 phút” giữ đúng con số nhưng bỏ điều kiện về bộ tiếp hợp, khiến người mua có thể hiểu rằng bộ sạc thông thường cũng đạt tốc độ này. Đây là tình huống minh họa cho nhu cầu kiểm tra điều kiện đi kèm con số, không chỉ bản thân con số.

Các hướng kiểm chứng tự động cung cấp cơ sở để tổ chức bài toán này. FEVER sử dụng tuyên bố được xây dựng từ Wikipedia cùng ba nhãn được hỗ trợ, bị bác bỏ và chưa đủ thông tin [2, tr. 1, 3–4]. AVeriTeC sử dụng tuyên bố thực tế và bổ sung nhãn Conflicting Evidence/Cherry-picking, bao gồm cả xung đột bằng chứng lẫn lược bỏ ngữ cảnh gây hiểu nhầm [3, tr. 1, 3–4]. Sự phân biệt giữa giá trị và điều kiện trong khóa luận được đặt trong hướng nghiên cứu kiểm chứng có xét đến ngữ cảnh này.

Các nghiên cứu tiếng Việt đã tạo cơ sở về dữ liệu và hệ thống kiểm chứng. ViFactCheck xây dựng dữ liệu từ tin tức thuộc nhiều chủ đề, còn ViNumFCR tập trung vào tuyên bố chứa số liệu và suy luận liên quan [5, tr. 3–5], [6, tr. 3–5]. SemViQA kết hợp truy hồi và phân loại theo ba nhãn trên dữ liệu tiếng Việt [7, tr. 4–7]. Đối với khóa luận, vấn đề cần khảo sát riêng là khả năng phân biệt sai giá trị với việc sử dụng giá trị ở điều kiện không phù hợp trong quảng cáo.

## 1.2. CopyPro và nhu cầu kiểm chứng

CopyPro là môi trường ứng dụng của đề tài, được phát triển từ đồ án chuyên ngành trước đó. Website sử dụng giao diện lập trình ứng dụng (application programming interface, API) của nhiều LLM để tạo quảng cáo từ thông tin người dùng nhập. Theo mô tả trong đề cương, CopyPro đã có chức năng chấm điểm chất lượng nội dung và so khớp với Common Crawl để kiểm tra đạo văn, nhưng chưa kiểm tra thông số trong quảng cáo với tài liệu chính hãng.

Bước kiểm chứng sau khi sinh nội dung nhằm phát hiện sai lệch phát sinh trong quá trình diễn đạt lại. Ngay cả khi người dùng cung cấp thông số, yêu cầu viết ngắn gọn hoặc hấp dẫn vẫn đặt ra khả năng điều kiện bị bỏ hoặc đổi. Vì vậy, đề tài xét hai chế độ tạo quảng cáo: chỉ nhập tên sản phẩm và nhập thêm đoạn thông số chính hãng. Việc so sánh hai chế độ giúp khảo sát nhu cầu kiểm chứng khi lượng thông tin đầu vào khác nhau.

Kết quả kiểm chứng cần gắn với từng tuyên bố để người dùng có căn cứ chỉnh sửa. Tính năng dự kiến cho phép chọn mẫu sản phẩm, xem nhãn, đoạn nguồn và lý do ngay tại trang kết quả tạo quảng cáo. Thông tin này được đặt cạnh điểm chất lượng và kết quả kiểm tra đạo văn, đồng thời lưu cùng nội dung đã tạo. Vai trò của tính năng là hỗ trợ phát hiện thông số sai hoặc lệch điều kiện trước khi đăng.

## 1.3. Vấn đề nghiên cứu

Bài toán nghiên cứu là kiểm chứng tuyên bố thông số có điều kiện ràng buộc bằng tài liệu văn bản của đúng sản phẩm. Đầu vào gồm bài quảng cáo q do LLM tạo, mẫu sản phẩm s do người dùng chọn và kho tài liệu chính hãng D(s). Với mỗi tuyên bố c thuộc danh sách thuộc tính có điều kiện của nhóm sản phẩm, hệ thống trả về nhãn y(c), đoạn nguồn e(c) trích từ D(s) và lý do r(c). Các ký hiệu này được sử dụng nhất quán khi trình bày phương pháp.

Điều kiện không xuất hiện trong tuyên bố được xử lý theo cách hiểu thông thường (ordinary interpretation) ghi trong tệp cấu hình của nhóm sản phẩm. Ví dụ về quy ước trong đề cương là xét bộ phận chính hoặc không giả định người dùng mua thêm phụ kiện. Quy ước cần được khai báo để việc đối chiếu có căn cứ thống nhất. Giá trị được xem là khớp khi bằng giá trị công bố sau chuẩn hóa hoặc kém thuận lợi hơn, chẳng hạn thời lượng pin thấp hơn; điều kiện và kiểu giá trị vẫn phải được kiểm tra.

Hệ nhãn của đề tài phân biệt bốn kết quả kiểm chứng. Nhãn Đúng (Supported) áp dụng khi tài liệu có thông số cùng sản phẩm, thuộc tính và điều kiện, giá trị khớp, kiểu giá trị không bị đổi. Nhãn Sai (Refuted) áp dụng khi giá trị mâu thuẫn ở điều kiện của tuyên bố hoặc thuận lợi hơn mọi giá trị công bố, đồng thời không trùng giá trị nào ở điều kiện khác. Nhãn Lệch điều kiện (Misleading) áp dụng khi giá trị trùng công bố ở điều kiện khác, hoặc mức “lên đến” bị biến thành mức chắc chắn đạt. Nhãn Chưa đủ thông tin (Not Enough Info, NEI) áp dụng khi kho tài liệu thiếu thông số tương ứng, thiếu giá trị ở điều kiện cần xét hoặc ghi mâu thuẫn.

Ví dụ Galaxy Buds3 Pro trong đề cương thể hiện vai trò của điều kiện hoạt động. Tài liệu được đề cương dẫn lại công bố thời lượng phát nhạc lên đến 6 giờ khi bật chống ồn và 7 giờ khi tắt chống ồn. Theo cách gán nhãn minh họa của đề cương, “nghe nhạc 6 giờ khi bật chống ồn” là Đúng; “nghe nhạc 7 giờ khi bật chống ồn” là Lệch điều kiện; “nghe nhạc 8 giờ” là Sai. Tuyên bố về chế độ không có giá trị công bố thuộc Chưa đủ thông tin.

Khó khăn chính nằm ở việc giữ đủ quan hệ giữa con số và điều kiện. Điều kiện có thể nằm trong chú thích cách xa thông số, khiến bằng chứng truy hồi thiếu thành phần cần thiết. Một con số cũng có thể phù hợp với chế độ này nhưng không phù hợp với chế độ khác. Ngoài ra, bước trích xuất bằng LLM có thể bỏ hoặc thêm điều kiện. Những khó khăn này đòi hỏi kiểm tra căn cứ của thông tin trích xuất trước khi kết luận.

Khoảng trống được xác định trong phạm vi các tài liệu đã khảo sát đến ngày 15/10/2026. FEVER, AVeriTeC và hướng phát hiện nửa sự thật của Tang và cộng sự chưa cung cấp đúng tổ hợp quảng cáo tiếng Việt, thông số có điều kiện và quy tắc đối chiếu bốn nhãn mà đề tài đặt ra [2, tr. 3–4], [3, tr. 3–4, 7–8], [4, tr. 5–6]. TRACER sử dụng bằng chứng có sẵn để phân tích phần bị lược và tác động lên ý định hàm ẩn [4, tr. 5–6]. Khóa luận khảo sát trường hợp có thể khai báo trước các loại điều kiện từ tài liệu sản phẩm để đối chiếu tường minh.

## 1.4. Câu hỏi nghiên cứu

Câu hỏi nghiên cứu thứ nhất, ký hiệu CH1, xét khả năng giảm chấp nhận nhầm: đối chiếu tường minh điều kiện ràng buộc có làm giảm tỷ lệ tuyên bố sai hoặc lệch điều kiện bị chấp nhận là Đúng so với các cách kiểm chứng hiện có, mà không bỏ sót nhiều tuyên bố đúng hay không? Chỉ số chính là tỷ lệ chấp nhận nhầm (false acceptance rate, FAR), được tính bằng tỷ lệ dự đoán Đúng trong các tuyên bố có nhãn chuẩn khác Đúng, cùng độ bao phủ (recall) của nhãn Đúng.

Câu hỏi nghiên cứu thứ hai, ký hiệu CH2, xét vai trò của cách quyết định nhãn: quy tắc tường minh trên dữ liệu đã neo nguồn có phát hiện Lệch điều kiện tốt hơn cách để LLM tự gán nhãn hay không? Neo nguồn (source anchoring) yêu cầu thông tin trích xuất đi kèm đoạn gốc để kiểm tra. Bộ quyết định (decision module) là thành phần áp dụng quy tắc đối chiếu để gán nhãn. Chỉ số F1 của nhãn Lệch điều kiện được dùng để đánh giá câu hỏi này.

Câu hỏi nghiên cứu thứ ba, ký hiệu CH3, xét đóng góp của neo nguồn và đối chiếu điều kiện. Phương pháp đề xuất, ký hiệu P, được so sánh với P−NN bỏ neo nguồn và kiểm tra đầy đủ, cùng P−ĐK bỏ đối chiếu điều kiện và chỉ so giá trị. Giả thuyết trong đề cương kỳ vọng P có FAR thấp hơn và F1 của nhãn Lệch điều kiện cao hơn P−NN. Các kỳ vọng này cần được kiểm tra bằng thực nghiệm, kể cả khi kết quả không xác nhận giả thuyết.

## 1.5. Mục tiêu

Mục tiêu tổng quát là đề xuất và đánh giá phương pháp kiểm chứng thông số có điều kiện trong quảng cáo tiếng Việt do LLM tạo, đồng thời tích hợp vào CopyPro. Bốn mục tiêu cụ thể được ký hiệu MT1–MT4, tương ứng với dữ liệu, phương pháp, thực nghiệm và ứng dụng.

MT1 là xây dựng dữ liệu kiểm chứng cho ba nhóm thiết bị được chọn. Công việc gồm thu thập quảng cáo và tài liệu chính hãng tương ứng, tách tuyên bố thông số có điều kiện, gán bốn nhãn kèm đoạn nguồn và lý do. Tập cặp tối thiểu (minimal pairs) được tạo theo từng loại biến đổi để khảo sát riêng tác động của việc bỏ hoặc đổi điều kiện.

MT2 là đề xuất và cài đặt phương pháp P. Phương pháp gồm trích xuất bộ thông số có neo nguồn và bộ quyết định bốn nhãn dựa trên đối chiếu điều kiện. Các bước chuẩn hóa và kiểm tra câu trích chuẩn bị dữ liệu cho bộ quyết định; mỗi quy tắc cần có kiểm thử riêng. Nội dung chi tiết của các quy tắc được trình bày ở Chương 3.

MT3 là đánh giá P với các phương pháp đối chứng B0–B3 và hai bản bỏ thành phần. B0 để LLM gán ba nhãn; B1 để LLM gán bốn nhãn trên cùng bộ thông số đã trích; B2 để LLM đọc bằng chứng và gán bốn nhãn theo hướng dẫn. B3 dự kiến sử dụng mô hình ba nhãn của SemViQA, có đặc tả trong nghiên cứu gốc [7, tr. 4–5]. Việc so sánh nhằm xác định mức giảm chấp nhận nhầm và khả năng phát hiện Lệch điều kiện.

MT4 là tích hợp tính năng “Kiểm chứng thông số” vào CopyPro. Người dùng cần xem được nhãn, đoạn nguồn và lý do của từng tuyên bố sau khi tạo quảng cáo. Mục tiêu ứng dụng gắn kết quả nghiên cứu với quy trình sử dụng website và bao gồm kiểm tra chức năng, thời gian kiểm chứng một bài quảng cáo.

## 1.6. Đối tượng và phạm vi

Đối tượng nghiên cứu là các phương pháp kiểm chứng tuyên bố quảng cáo do LLM tạo bằng bằng chứng văn bản. Trọng tâm là phát hiện thông số không phù hợp với tài liệu của sản phẩm hoặc phiên bản được quảng cáo và thông số được áp dụng sai điều kiện. Dữ liệu nghiên cứu gồm tuyên bố tiếng Việt cùng trang thông số chính hãng tương ứng.

Phạm vi thực nghiệm chính gồm điện thoại thông minh, tai nghe không dây và đồng hồ thông minh. Khóa luận sử dụng 12 mẫu sản phẩm của bốn hãng (Apple, Samsung, Xiaomi, OPPO), gồm 5 điện thoại, 4 tai nghe và 3 đồng hồ, đang bán chính hãng tại Việt Nam. Sáu nhóm thông số được xét là thời lượng pin, dung lượng pin, sạc nhanh, kháng nước và bụi, màn hình gồm độ sáng và tần số quét, cùng zoom camera.

Danh mục điều kiện gồm sáu loại được khai báo theo nhóm sản phẩm. Các loại này là chế độ hoạt động, bộ phận, phụ kiện, điều kiện đo, phiên bản sản phẩm và kiểu giá trị. Việc phân loại giúp xác định phần cần đối chiếu giữa tuyên bố và công bố của hãng. Danh mục thuộc tính và điều kiện bắt buộc được đặt trong tệp cấu hình, tách khỏi quy tắc quyết định.

Tiêu chí chọn nhóm sản phẩm gắn với khả năng thu thập bằng chứng và so sánh thực nghiệm. Nhóm phù hợp phải có trang thông số chính thức bằng tiếng Việt và số liệu đo được công bố kèm điều kiện. Các nhóm đưa vào thực nghiệm còn cần có những nhóm thông số chung và sản phẩm của cùng các hãng để nguồn bằng chứng đồng nhất. Tài liệu được sử dụng giới hạn ở văn bản chính hãng của đúng mẫu đã chọn; Chưa đủ thông tin chỉ phản ánh giới hạn của kho tài liệu đã thu thập.

Quảng cáo được tạo bằng CopyPro trong ngành Công nghệ theo thiết kế của đề cương. Dữ liệu dự kiến sử dụng hai LLM thuộc hai họ mô hình và ba loại nội dung: mô tả sản phẩm, bài đăng mạng xã hội, trang đích (landing page). Mỗi loại được xét ở hai chế độ đầu vào đã nêu tại mục 1.2. Quy mô dự kiến là khoảng 250–300 tuyên bố và 100–120 biến thể cặp tối thiểu; các con số này biểu thị kế hoạch nghiên cứu.

Việc phân chia dữ liệu nhằm tách quá trình lựa chọn cấu hình khỏi đánh giá cuối. Tập phát triển (development set) được dùng để chọn mô hình, câu lệnh và cấu hình; tập kiểm tra (test set) được sử dụng sau khi các lựa chọn đã khóa. Dữ liệu được chia theo mẫu sản phẩm để hạn chế rò rỉ giữa hai tập. Chương này chưa sử dụng số liệu kết quả để khẳng định hiệu quả của phương pháp.

Phần không thuộc phạm vi gồm thông số không kèm điều kiện, tuyên bố cảm tính, so sánh với sản phẩm khác, giá và khuyến mãi. Đề tài không đo hiệu năng thực tế, không đưa kết luận pháp lý, không đánh giá quảng cáo do người viết và không tự nhận diện sản phẩm; người dùng chọn mẫu khi kiểm chứng. Máy tính xách tay, tivi và đồ gia dụng không thuộc thực nghiệm chính vì cần thêm thuộc tính và điều kiện riêng. Thử trên máy tính bảng cùng đối chứng LLM mạnh hơn B4 chỉ là phần mở rộng khi tiến độ cho phép.

## 1.7. Tính mới

Tính mới được đặt ở bài toán và phép kết luận có đối chiếu điều kiện. Trong phạm vi khảo sát, các hướng kiểm chứng quảng cáo, mô tả sản phẩm và câu do LLM sinh chưa tách riêng sai giá trị với lệch điều kiện theo thiết kế của đề tài [12, tr. 3–6], [1, tr. 3–5], [11, tr. 1–2]. Khóa luận tập trung vào tuyên bố thông số trong quảng cáo tiếng Việt và đánh giá riêng nhãn Lệch điều kiện, thay vì khẳng định tính mới cho toàn bộ hoạt động kiểm chứng bằng LLM.

Phép kết luận của P so điều kiện trong tuyên bố với từng điều kiện hãng công bố cho cùng thông số. Giá trị trùng ở điều kiện khác hoặc mức tối đa bị chuyển thành mức chắc chắn đạt là căn cứ gán Lệch điều kiện. B1 nhận cùng thông số có cấu trúc và B2 nhận cùng hệ bốn nhãn, nhưng đều để LLM kết luận. Các đối chứng này phục vụ kiểm tra đóng góp của bộ quyết định; bước trích xuất chỉ chuẩn bị đầu vào.

Sáu loại điều kiện là thiết kế áp dụng cho miền thông số sản phẩm. MeasEval cung cấp cơ sở tham khảo về biểu diễn số đo cùng đơn vị, đối tượng, thuộc tính và ngữ cảnh bổ nghĩa [14, tr. 2–3]. Khóa luận cụ thể hóa cơ sở đó thành danh mục điều kiện và quy tắc đối chiếu của mình. Hiệu quả của thiết kế cần được chứng minh qua thực nghiệm và phân tích thành phần.

## 1.8. Đóng góp

Đóng góp phương pháp dự kiến là P với trích xuất có neo nguồn và bộ quyết định bốn nhãn. Mã nguồn và kiểm thử từng quy tắc tạo căn cứ xem xét cách đi từ bằng chứng đến kết luận. Lý do được tạo từ dấu vết quyết định, giúp xác định điều kiện bị thiếu hoặc bị đổi trong từng trường hợp.

Đóng góp dữ liệu dự kiến là bộ tuyên bố tiếng Việt có nhãn, đoạn nguồn, lý do và tập cặp tối thiểu. Ý tưởng kiểm tra tương phản được tham khảo từ VitaminC, nghiên cứu sử dụng các phiên bản bằng chứng để khảo sát thay đổi nhãn [15, tr. 3–4]. Đề tài giữ nguồn chính hãng cố định và biến đổi tuyên bố; nhãn của biến thể phải được kiểm tra lại. Dữ liệu cũng phục vụ thống kê lỗi bỏ hoặc đổi điều kiện theo hai chế độ sinh quảng cáo.

Đóng góp đánh giá và ứng dụng gồm kết quả so sánh có đối chứng và tính năng trên CopyPro. Các phương pháp được đánh giá trên cùng tuyên bố và bằng chứng để xem xét lợi ích của P cùng giới hạn của từng thành phần. Kết quả cần báo cáo cả trường hợp không cải thiện. Tính năng tích hợp cung cấp nhãn, nguồn và lý do cho người viết quảng cáo, nối kết phần thực nghiệm với nhu cầu sử dụng.

## 1.9. Bố cục khóa luận

Khóa luận gồm sáu chương theo đề cương triển khai. Chương 1 trình bày bối cảnh, vấn đề, câu hỏi, mục tiêu, phạm vi và đóng góp dự kiến. Chương 2 trình bày cơ sở lý thuyết và nghiên cứu liên quan về kiểm chứng tự động, truy hồi BM25, tuyên bố số liệu, ảo giác, kiểm chứng tiếng Việt và quảng cáo.

Các chương tiếp theo trình bày phương pháp và đánh giá. Chương 3 mô tả bài toán, hệ nhãn, biểu diễn thông số, trích xuất, chuẩn hóa, quy tắc quyết định và sinh lý do. Chương 4 trình bày xây dựng dữ liệu, độ tin cậy nhãn, thiết lập, đối chứng, kết quả, phân tích lỗi và mối đe dọa đến tính hợp lệ. Chương 5 trình bày tích hợp CopyPro, kiến trúc, API, giao diện, thời gian và kết quả đầu–cuối. Chương 6 tổng kết theo MT1–MT4, nêu giới hạn và hướng phát triển. Phụ lục cung cấp hướng dẫn gán nhãn, câu lệnh, tệp cấu hình và danh sách kiểm thử.

## Ghi chú cho người duyệt

- Vị trí cần số trang: không có chỗ thiếu số trang trong các nhận định nghiên cứu được sử dụng. Số trang trong trích dẫn là thứ tự trang PDF theo `luan_van/ghi_chu_tai_lieu.md`, không phải trang in của kỷ yếu. Giữ nguyên định danh tài liệu theo danh mục [1]–[16]; chương này chỉ dẫn những tài liệu thực sự sử dụng.
- Mục 1.1 và 1.3: hai ví dụ sản phẩm đã đối chiếu với tài liệu hãng đã lưu: iPhone 17 ở đoạn `dt-apple-iphone17#016` (“Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng)”), Galaxy Buds3 Pro ở đoạn `#038` và `#044` (6 giờ khi bật chống ồn, 7 giờ khi tắt). Khi viết bản nộp có thể dẫn mã đoạn hoặc đường dẫn trang hãng.
- Mục 1.3: giữ nguyên nhãn Đúng cho câu “nghe nhạc 6 giờ khi bật chống ồn” theo ví dụ đề cương (tài liệu ghi “lên đến 6 giờ”). Việc bỏ chữ “lên đến” có bị coi là Lệch điều kiện hay không đang chờ người thực hiện quyết (quy tắc hiện hành: không Lệch). Nếu đổi quy tắc thì phải sửa ví dụ này và định nghĩa nhãn ở mục 1.3 cho khớp.
- Các chỗ diễn giải lại: mục 1.1 giới hạn ảo giác theo mức hỗ trợ của nguồn; mục 1.3 giới hạn khoảng trống ở khảo sát đến 15/10/2026 và mô tả TRACER sử dụng bằng chứng có sẵn; mục 1.4, 1.7 và 1.8 trình bày lợi ích của P là giả thuyết hoặc đóng góp dự kiến; mục 1.7 xác định sáu loại điều kiện là thiết kế của đề tài tham khảo MeasEval; mục 1.8 phân biệt biến đổi tuyên bố của đề tài với biến đổi bằng chứng trong VitaminC. Các diễn giải tuân theo mục 2 của ghi chú tài liệu.
- Mục 1.5: không khẳng định đã có trọng số SemViQA công khai; ghi chú tài liệu yêu cầu kiểm tra thêm trước khi triển khai B3. Mục 1.6 giữ quy mô ở trạng thái dự kiến và không khẳng định dữ liệu đã hoàn tất.
- Bối cảnh được rút gọn, chưa đưa nghiên cứu FTC và viện dẫn Luật Quảng cáo vào nội dung chính: FTC chưa có số trong danh mục [1]–[16], còn viện dẫn luật chưa được ghi chú kiểm tra với văn bản chính thức. Cần người duyệt quyết định việc bổ sung nguồn; không tự đánh lại số tài liệu.
- Số chữ ước tính của nội dung chính: 3.333, tính bằng các đơn vị tách bởi khoảng trắng, gồm tiêu đề và trích dẫn, không gồm mục ghi chú này. Số trang A4 cần kiểm tra khi dàn trang theo mẫu của Khoa.
