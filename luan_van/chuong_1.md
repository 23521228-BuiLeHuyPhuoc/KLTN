# Chương 1. Mở đầu

## 1.1. Bối cảnh và lí do chọn đề tài

Mô hình ngôn ngữ lớn (large language model, LLM) ngày càng được dùng để viết quảng cáo, nhưng nội dung do LLM viết có thể không khớp với nguồn. Hiện tượng này được gọi là ảo giác (hallucination). Trên sàn thương mại điện tử, Jiang và cộng sự ghi nhận LLM thêm vào mô tả sản phẩm những giá trị không có trong dữ liệu gốc của sản phẩm [1, tr. 1–3]. Người mua dựa vào các giá trị đó để quyết định, nên quảng cáo cần được kiểm tra trước khi đăng.

Với thông số kỹ thuật, có một loại lỗi khó phát hiện hơn sai con số: con số vẫn đúng nhưng bị tách khỏi điều kiện đi kèm. Nhiều thông số chỉ đúng trong một hoàn cảnh nhất định, và khóa luận gọi đó là thông số có điều kiện ràng buộc. Ví dụ, trang thông số của iPhone 17 ghi “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng)” [23]. Câu quảng cáo “sạc 50% chỉ trong 20 phút” giữ nguyên hai con số nhưng bỏ điều kiện về bộ tiếp hợp, nên người đọc có thể nghĩ bộ sạc nào cũng đạt tốc độ này. Nếu chỉ so con số, câu quảng cáo trên vẫn khớp với tài liệu.

Cách người đọc tiếp nhận quảng cáo cho thấy phần chữ đi kèm con số có thể bị bỏ qua. Trong báo cáo gửi Ủy ban Thương mại Liên bang Hoa Kỳ (Federal Trade Commission, FTC) năm 2012, Hastak và Murphy cho người tham gia xem quảng cáo cửa sổ tiết kiệm năng lượng ghi mức tiết kiệm “up to 47%” (lên đến 47%). Có 36% người xem trả lời rằng quảng cáo nói tiết kiệm 47% mà không nhắc đến giới hạn “lên đến”, trong khi chỉ 21,9% nhắc đúng mức “lên đến 47%” [21, tr. 7]. Kết quả này thuộc một loại sản phẩm khác và một thị trường khác, nên không suy rộng trực tiếp sang người mua Việt Nam. Khóa luận đo riêng cách hiểu của người đọc tiếng Việt bằng một khảo sát nhỏ, trình bày ở Chương 4.

Ở Việt Nam, pháp luật cũng đã đặt ra yêu cầu kiểm tra tài liệu trước khi quảng cáo. Luật số 75/2025/QH15 sửa đổi, bổ sung một số điều của Luật Quảng cáo, có hiệu lực từ ngày 01/01/2026, yêu cầu người có ảnh hưởng khi chuyển tải quảng cáo phải kiểm tra tài liệu liên quan đến sản phẩm (Điều 15a, khoản 3) [22]. Quy định này không nói riêng về nội dung do LLM tạo, và khóa luận không đưa ra kết luận pháp lý. Tuy vậy, quy định cho thấy việc đối chiếu quảng cáo với tài liệu sản phẩm là một yêu cầu có thật, không chỉ là mong muốn về mặt kỹ thuật.

Đề tài xuất phát từ nhu cầu cụ thể của CopyPro, website tạo quảng cáo bằng LLM mà tác giả đã phát triển trong đồ án chuyên ngành. CopyPro gọi giao diện lập trình ứng dụng (application programming interface, API) của nhiều LLM để viết quảng cáo từ thông tin người dùng nhập. Website đã có chức năng chấm điểm chất lượng nội dung và so khớp với Common Crawl để kiểm tra đạo văn, nhưng chưa kiểm tra thông số trong bài có khớp với tài liệu chính hãng hay không.

Bước kiểm tra này cần thiết ngay cả khi người dùng đã đưa đủ thông số cho LLM. Khi viết lại cho ngắn gọn và hấp dẫn, LLM có thể giữ con số nhưng bỏ hoặc đổi điều kiện. Vì vậy, đề tài kiểm chứng quảng cáo sau khi đã tạo và xét hai chế độ nhập, ứng với hai nguồn lỗi khác nhau. Ở chế độ chỉ nhập tên sản phẩm, LLM phải tự nhớ thông số nên có thể nhớ sai hoặc tự đặt ra con số. Ở chế độ nhập thêm đoạn thông số chính hãng, LLM đã có số liệu đúng trong yêu cầu, nên lỗi nếu có sẽ phát sinh ở bước viết lại.

Các hệ thống kiểm chứng đã khảo sát chưa xử lý trực tiếp loại lỗi này. Chúng chủ yếu xét mức khớp nội dung giữa tuyên bố và bằng chứng, chưa biểu diễn tường minh các điều kiện đi kèm thông số (mục 2.9). Trong khi đó, thông số kỹ thuật có một đặc điểm thuận lợi: hãng đã ghi điều kiện trong tài liệu, nên có thể liệt kê trước các loại điều kiện rồi so từng loại giữa quảng cáo và tài liệu. Đây là lí do khóa luận chọn đề tài “Phương pháp kiểm chứng tuyên bố về thông số kỹ thuật có điều kiện ràng buộc trong quảng cáo”.

## 1.2. Vấn đề nghiên cứu

Bài toán của khóa luận là kiểm chứng từng tuyên bố về thông số có điều kiện ràng buộc trong một bài quảng cáo, dùng tài liệu chính hãng của đúng sản phẩm làm bằng chứng. Đầu vào gồm bài quảng cáo q do LLM tạo, mẫu sản phẩm s do người dùng chọn và kho tài liệu chính hãng D(s) của mẫu đó. Tuyên bố (claim) c là một phát biểu trong q nêu giá trị của một thuộc tính nằm trong danh sách thuộc tính có điều kiện ràng buộc của nhóm sản phẩm, tức các thuộc tính mà hãng thường công bố kèm điều kiện. Với mỗi tuyên bố c, hệ thống trả về nhãn y(c), đoạn nguồn e(c) trích từ D(s) và lý do r(c).

Quảng cáo thường không nêu hết điều kiện, nên bài toán cần một quy ước cho phần không được nêu. Điều kiện mà tuyên bố không nêu được hiểu theo cách hiểu thông thường (ordinary interpretation), ghi trong tệp cấu hình của nhóm sản phẩm. Ví dụ, quảng cáo tai nghe chỉ ghi thời lượng pin mà không nói của bộ phận nào thì được hiểu là pin của tai nghe, không tính thêm hộp sạc. Quảng cáo không nhắc đến phụ kiện thì được hiểu là người dùng không mua thêm phụ kiện, chẳng hạn bộ sạc rời. Các cách hiểu này được ghi sẵn trong tệp cấu hình để mọi tuyên bố đều được đối chiếu theo cùng một căn cứ.

Con số trong tuyên bố được xem là khớp trong hai trường hợp: bằng con số hãng công bố sau khi đưa về cùng cách ghi và đơn vị, hoặc kém thuận lợi hơn con số đó. Kém thuận lợi nghĩa là kém hấp dẫn hơn với người mua. Ví dụ, hãng công bố pin 6 giờ mà quảng cáo ghi 5 giờ thì vẫn khớp, vì người mua không bị hiểu nhầm theo hướng có lợi cho người bán. Tuy nhiên, khớp con số chưa đủ để kết luận tuyên bố đúng. Tuyên bố còn phải nêu đúng điều kiện và không đổi kiểu giá trị, ví dụ không biến mức “lên đến” thành mức chắc chắn đạt.

Mỗi tuyên bố nhận một trong bốn nhãn sau.

**Đúng (Supported):** tài liệu có thông số cùng sản phẩm, thuộc tính và điều kiện với tuyên bố, giá trị khớp và kiểu giá trị không bị đổi.

**Sai (Refuted):** tài liệu có thông số cùng sản phẩm và thuộc tính, nhưng giá trị của tuyên bố mâu thuẫn với giá trị công bố ở điều kiện của tuyên bố hoặc thuận lợi hơn mọi giá trị được công bố, đồng thời không trùng giá trị nào ở điều kiện khác.

**Lệch điều kiện (Misleading):** giá trị trong tuyên bố trùng giá trị được công bố ở một điều kiện khác với điều kiện mà tuyên bố nêu hoặc được hiểu thông thường, hoặc tuyên bố biến mức tối đa “lên đến” thành mức chắc chắn đạt.

**Chưa đủ thông tin (Not Enough Info, NEI):** kho tài liệu không có thông số cùng sản phẩm và thuộc tính, không công bố giá trị ở điều kiện mà tuyên bố nêu, hoặc ghi mâu thuẫn.

Bảng 1.1 minh họa bốn nhãn trên tai nghe Galaxy Buds3 Pro. Trang của hãng ghi thời gian phát nhạc lên đến 6 giờ khi bật chống ồn và lên đến 7 giờ khi tắt chống ồn [24]. Nếu chỉ so con số, tuyên bố ở hàng thứ ba của bảng sẽ được chấp nhận vì con số 7 giờ có trong tài liệu, dù mức này chỉ đạt được khi tắt chống ồn.

**Bảng 1.1.** Ví dụ bốn nhãn với tuyên bố về thời lượng pin của Galaxy Buds3 Pro

| Tuyên bố | Nhãn | Lý do |
|---|---|---|
| Nghe nhạc lên đến 6 giờ khi bật chống ồn | Đúng | Cùng điều kiện, cùng giá trị, giữ nguyên kiểu giá trị |
| Đảm bảo nghe nhạc 6 giờ khi bật chống ồn | Lệch điều kiện | Mức tối đa bị viết thành mức chắc chắn đạt |
| Nghe nhạc lên đến 7 giờ khi bật chống ồn | Lệch điều kiện | 7 giờ chỉ đạt khi tắt chống ồn |
| Nghe nhạc lên đến 8 giờ | Sai | Thuận lợi hơn mọi giá trị công bố cho tai nghe và không trùng giá trị nào |
| Nghe nhạc lên đến 6,5 giờ ở chế độ xuyên âm | Chưa đủ thông tin | Trang không công bố thời lượng ở chế độ xuyên âm |

Bài toán khó ở ba điểm. Thứ nhất, điều kiện thường nằm ở chú thích tách khỏi con số, nên đoạn bằng chứng truy hồi được có thể thiếu điều kiện. Thứ hai, cùng một con số có thể đúng ở điều kiện này nhưng gây hiểu nhầm ở điều kiện khác, nên không thể kết luận chỉ từ con số. Thứ ba, LLM có thể bỏ hoặc tự thêm điều kiện khi trích xuất thông tin từ văn bản. Ngoài ra, trong các tài liệu đã khảo sát chưa có bộ dữ liệu tiếng Việt cho loại tuyên bố này.

## 1.3. Câu hỏi nghiên cứu và giả thuyết

Khóa luận đề xuất phương pháp kiểm chứng P gồm hai thành phần chính. Thành phần thứ nhất là trích xuất có neo nguồn (source anchoring): mỗi giá trị và điều kiện do LLM trích ra đều kèm câu gốc trong bằng chứng để mã nguồn kiểm tra lại. Thành phần thứ hai là bộ quyết định (decision module): mã Python đối chiếu điều kiện của tuyên bố với điều kiện của từng thông số trong tài liệu rồi gán nhãn theo quy tắc, thay vì để LLM tự kết luận.

P được so sánh với bốn phương pháp đối chứng và hai bản bỏ thành phần. B0 để LLM đọc bằng chứng rồi gán ba nhãn Supported, Refuted và NEI. B1 cho LLM nhận cùng bộ thông số đã trích như P rồi tự gán bốn nhãn. B2 để LLM đọc bằng chứng và gán bốn nhãn theo hướng dẫn có định nghĩa và ví dụ nhãn Lệch điều kiện. B3 dùng mô hình ba nhãn tiếng Việt của SemViQA [7]. P−ĐK là P bỏ đối chiếu điều kiện, chỉ so giá trị. P−NN là P bỏ neo nguồn và các bước kiểm tra đi kèm. Mọi phương pháp dùng cùng tuyên bố và cùng k đoạn bằng chứng xếp hạng cao nhất.

Khóa luận trả lời ba câu hỏi nghiên cứu, mỗi câu có một giả thuyết đo được. Chỉ số chính là tỷ lệ chấp nhận nhầm (false acceptance rate, FAR), tức tỷ lệ tuyên bố bị gán Đúng trong số các tuyên bố có nhãn chuẩn khác Đúng. Các độ đo được định nghĩa ở mục 2.8.

**Câu hỏi 1.** Đối chiếu tường minh điều kiện ràng buộc có làm giảm tỷ lệ tuyên bố sai hoặc lệch điều kiện bị chấp nhận là Đúng so với các cách kiểm chứng hiện có, mà không bỏ sót nhiều tuyên bố đúng hay không? Giả thuyết 1: FAR của P thấp hơn B0–B3, và Recall của nhãn Đúng không thấp hơn quá 5 điểm phần trăm so với đối chứng tốt nhất.

**Câu hỏi 2.** Quyết định nhãn bằng quy tắc tường minh trên dữ liệu đã neo nguồn có phát hiện tuyên bố Lệch điều kiện tốt hơn cách để LLM tự gán nhãn hay không? Giả thuyết 2: F1 của nhãn Lệch điều kiện của P cao hơn B1 và B2.

**Câu hỏi 3.** Neo nguồn và đối chiếu điều kiện đóng góp thế nào vào kết quả? Giả thuyết 3: P tốt hơn P−NN về FAR và F1 của nhãn Lệch điều kiện. Đóng góp của đối chiếu điều kiện được đo bằng cách so P với P−ĐK.

Mô hình, câu lệnh và giá trị k được chọn trên tập phát triển (development set) rồi khóa trước khi chạy tập kiểm tra (test set). Kết quả được báo cáo cả khi không đạt giả thuyết.

## 1.4. Mục tiêu

Mục tiêu tổng quát của khóa luận là đề xuất, đánh giá phương pháp kiểm chứng thông số có điều kiện ràng buộc trong quảng cáo tiếng Việt do LLM tạo và đưa phương pháp đó vào CopyPro. Mục tiêu này được chia thành bốn mục tiêu cụ thể.

**MT1. Xây dựng dữ liệu kiểm chứng.** Thu thập quảng cáo do LLM tạo về điện thoại thông minh, tai nghe không dây, đồng hồ thông minh và tài liệu chính hãng của đúng sản phẩm được quảng cáo. Tách các tuyên bố về thông số có điều kiện ràng buộc, gán bốn nhãn kèm đoạn nguồn và lý do, rồi tạo tập cặp tối thiểu (minimal pairs) theo từng loại lệch điều kiện.

**MT2. Đề xuất và cài đặt phương pháp P.** Xây dựng bước trích xuất bộ thông số có neo nguồn và bộ quyết định bốn nhãn dựa trên đối chiếu điều kiện. Mỗi quy tắc của bộ quyết định có kiểm thử riêng.

**MT3. Đánh giá có đối chứng.** So sánh P với B0–B3 và hai bản bỏ thành phần trên cùng tuyên bố và cùng bằng chứng, nhằm xác định P có giảm chấp nhận nhầm và phát hiện tốt hơn tuyên bố Lệch điều kiện hay không.

**MT4. Tích hợp vào CopyPro.** Thêm tính năng “Kiểm chứng thông số” để người dùng xem nhãn, đoạn nguồn và lý do của từng tuyên bố ngay sau khi tạo quảng cáo, đồng thời đo thời gian kiểm chứng một bài.

## 1.5. Đối tượng nghiên cứu

Đối tượng nghiên cứu là các phương pháp kiểm chứng tuyên bố quảng cáo do LLM tạo bằng bằng chứng văn bản. Trọng tâm là phát hiện thông số không phù hợp với tài liệu của sản phẩm hoặc phiên bản được quảng cáo, và thông số được áp dụng sai điều kiện. Dữ liệu nghiên cứu là các tuyên bố về thông số có điều kiện ràng buộc trong quảng cáo tiếng Việt, cùng trang thông số chính hãng tương ứng.

## 1.6. Phạm vi nghiên cứu

Thực nghiệm giới hạn ở ba nhóm sản phẩm với 12 mẫu của bốn hãng Apple, Samsung, Xiaomi và OPPO, đang bán chính hãng tại Việt Nam. Nhóm điện thoại gồm iPhone 17, Xiaomi 15T, OPPO Find X8, Galaxy S25 Ultra và Redmi Note 14 Pro+ 5G. Nhóm tai nghe gồm Galaxy Buds3 Pro, AirPods Pro 3, AirPods 4 và Redmi Buds 6 Pro. Nhóm đồng hồ gồm Apple Watch SE 3, Galaxy Watch8 và Xiaomi Watch S4. Dữ liệu được chia theo mẫu để tránh rò rỉ thông tin: iPhone 17, Xiaomi 15T, Galaxy Buds3 Pro và Apple Watch SE 3 thuộc tập phát triển, tám mẫu còn lại thuộc tập kiểm tra.

Đề tài tập trung vào sáu nhóm thông số thường được công bố kèm điều kiện: thời lượng pin, dung lượng pin, sạc nhanh, kháng nước và bụi, màn hình (độ sáng, tần số quét) và zoom camera. Điều kiện ràng buộc được xét gồm sáu loại:

- Chế độ hoạt động, ví dụ bật hoặc tắt chống ồn, chế độ tiết kiệm pin.
- Bộ phận, ví dụ tai nghe hay hộp sạc.
- Phụ kiện, ví dụ bộ sạc có công suất nhất định.
- Điều kiện đo, ví dụ độ sâu và thời gian ngâm nước, phần diện tích màn hình được đo.
- Phiên bản sản phẩm.
- Kiểu giá trị, ví dụ “lên đến”, “tối đa”, “điển hình”, “định mức”.

Quảng cáo do CopyPro tạo ở ngành Công nghệ bằng hai LLM thuộc hai họ mô hình khác nhau là Gemini 3.6 Flash và GPT-OSS 120B qua Groq. Mỗi mẫu có ba loại bài (mô tả sản phẩm, bài đăng mạng xã hội, trang đích) ở hai chế độ nhập đã nêu ở mục 1.1. Hai mẫu làm thử có đủ 12 tổ hợp, tức 24 bài. Mười mẫu còn lại có 8 bài mỗi mẫu, chia đều theo LLM và chế độ, xoay vòng loại bài giữa các mẫu, tức 80 bài. Từ 104 bài này, đề tài dự kiến thu được khoảng 250–300 tuyên bố và tạo thêm 100–120 biến thể cặp tối thiểu.

Hai chế độ nhập là hai đầu của lượng thông tin đưa cho LLM, nên chưa phủ hết cách nhập trong thực tế. Người dùng còn có thể chỉ nhập vài từ khóa, chép thông số từ trang bán lẻ hoặc tự tóm tắt có sai sót. Đoạn thông số trong thực nghiệm được chọn sẵn từ tài liệu của hãng, nên sạch hơn dữ liệu người dùng thật nhập vào. Các kết quả theo chế độ vì vậy chỉ có giá trị trong hai thiết lập này.

Ba nhóm sản phẩm được chọn theo bốn tiêu chí. Hãng có trang thông số chính thức bằng tiếng Việt; thông số là số liệu đo được và công bố kèm điều kiện; các nhóm có chung những nhóm thông số như pin và kháng nước để so sánh được với nhau; các nhóm có sản phẩm của cùng các hãng để nguồn bằng chứng đồng nhất. Quảng cáo mỹ phẩm, ẩm thực hay du lịch chủ yếu nêu cảm nhận, giá và ưu đãi nên khó có bằng chứng văn bản chuẩn.

Hệ thống chỉ dùng tài liệu văn bản của đúng sản phẩm làm bằng chứng, và người dùng tự chọn mẫu khi kiểm chứng. Nhãn Chưa đủ thông tin nghĩa là không tìm thấy thông tin trong kho tài liệu đã thu thập, không có nghĩa tuyên bố sai.

Các nội dung sau không thuộc phạm vi: tuyên bố về thông số không kèm điều kiện (khối lượng, kích thước, phiên bản Bluetooth), tuyên bố cảm tính, so sánh với sản phẩm khác, giá và khuyến mãi; đo hiệu năng thực tế của thiết bị; kết luận pháp lý; đánh giá trên quảng cáo do người viết. Máy tính xách tay, tivi và đồ gia dụng không được đưa vào thực nghiệm vì cần định nghĩa thêm nhiều thuộc tính và điều kiện riêng, vượt quá khối lượng gán nhãn của một người. Nếu đúng tiến độ, khóa luận thử thêm khả năng mở rộng trên máy tính bảng và một đối chứng dùng LLM mạnh hơn (B4).

## 1.7. Tính mới

Tính mới của khóa luận nằm ở loại tuyên bố được xét và ở cách kết luận, không nằm ở việc kết hợp các công cụ. Truy hồi bằng BM25, trích xuất bằng LLM, kiểm chứng qua mã nguồn và cặp tương phản đều đã có tiền lệ (Chương 2). Các nhận định dưới đây giới hạn trong những tài liệu đã khảo sát đến ngày 15/10/2026.

Thứ nhất, khóa luận xét riêng tuyên bố về thông số có điều kiện ràng buộc trong quảng cáo tiếng Việt do LLM tạo, một loại tuyên bố mà các nghiên cứu đã khảo sát chưa xét riêng.

Thứ hai, nhãn Lệch điều kiện được kết luận bằng phép đối chiếu điều kiện. P so điều kiện của tuyên bố với từng điều kiện mà hãng công bố cho cùng thông số, rồi gán Lệch điều kiện khi con số của tuyên bố trùng giá trị công bố ở một điều kiện khác, hoặc khi mức “lên đến” bị viết thành mức chắc chắn đạt. Các cách hiện có để LLM tự đọc bằng chứng rồi phán đoán [3, tr. 3–4], hoặc căn chỉnh bằng chứng có sẵn với phát biểu rồi suy ra ý định và phần thông tin bị lược bỏ [4, tr. 5–6]. Bước trích xuất của P chỉ chuẩn bị đầu vào: đối chứng B1 nhận cùng bộ thông số đã trích, B2 dùng cùng bốn nhãn, nhưng cả hai đều để LLM gán nhãn.

Thứ ba, sáu loại điều kiện được dùng làm danh mục để so từng loại. Lược đồ gán nhãn MeasEval quy định một số đo cần đi kèm những thông tin nào để được hiểu đúng [14, tr. 2–3], và khóa luận tham khảo nguyên tắc này. Danh mục sáu loại điều kiện và các quy tắc quyết định là thiết kế riêng cho thông số sản phẩm.

So với các hướng hiện có, P được kỳ vọng cải thiện ở ba điểm, và cả ba đều là giả thuyết cần đo. So với kiểm chứng ba nhãn [2], [5], [7], tuyên bố đúng con số nhưng sai điều kiện có nhãn riêng thay vì phải xếp vào một trong ba nhãn, nên FAR được kỳ vọng giảm. So với cách để LLM gán bốn nhãn bằng câu lệnh, nhãn được quyết định bằng quy tắc nên giải thích và kiểm thử được. So với các cách kiểm tra quảng cáo và văn bản do LLM tạo, P tách được sai giá trị với lệch điều kiện: Nguyen và cộng sự so khớp theo độ tương đồng [12, tr. 4–5], Jiang và cộng sự lọc bằng độ tương đồng rồi để LLM xác nhận [1, tr. 3–5], còn MiniCheck phân loại từng câu theo hai nhãn [11, tr. 2].

## 1.8. Đóng góp

Khóa luận dự kiến có năm đóng góp.

- Phương pháp P gồm trích xuất có neo nguồn và bộ quyết định bốn nhãn, được cài đặt thành mã nguồn với kiểm thử cho từng quy tắc.
- Bộ dữ liệu tiếng Việt gồm các tuyên bố về thông số có điều kiện ràng buộc, gán bốn nhãn kèm đoạn nguồn và lý do, cùng tập cặp tối thiểu để đo riêng từng loại lệch điều kiện.
- Số liệu cho biết LLM bỏ hoặc đổi điều kiện thường đến mức nào khi viết quảng cáo, so giữa hai chế độ nhập.
- Kết quả đánh giá có đối chứng với bốn cách kiểm chứng hiện có và hai bản bỏ thành phần, trên cùng tuyên bố và cùng bằng chứng.
- Tính năng “Kiểm chứng thông số” trong CopyPro, giúp người viết phát hiện và sửa tuyên bố sai hoặc lệch điều kiện trước khi đăng.

## 1.9. Bố cục khóa luận

Khóa luận gồm sáu chương. Chương 1 trình bày lí do chọn đề tài, vấn đề nghiên cứu, câu hỏi, mục tiêu, đối tượng, phạm vi và đóng góp. Chương 2 tổng quan các nghiên cứu liên quan và cơ sở lý thuyết. Chương 3 trình bày phương pháp đề xuất. Chương 4 trình bày dữ liệu, thực nghiệm, kết quả và các mối đe dọa đến tính hợp lệ. Chương 5 trình bày việc tích hợp vào CopyPro. Chương 6 kết luận và nêu hướng phát triển. Phụ lục gồm hướng dẫn gán nhãn, câu lệnh, tệp cấu hình và danh sách kiểm thử.

Số trang trong trích dẫn, ví dụ [2, tr. 3], là thứ tự trang trong tệp PDF của tài liệu, tính cả trang bìa nếu có, không phải số trang in ở chân trang.

## Ghi chú cho người duyệt

Mục này không đưa lên Google Doc.

- Viết lại toàn bộ ngày 05/11/2026 (Opus), thay bản do Codex Astra viết ngày 03/11/2026.
- Đổi tên chương từ "Tổng quan" thành "Mở đầu" để khớp Phụ lục 2 của Khoa (MỞ ĐẦU rồi TỔNG QUAN). Kế hoạch T8.1 vẫn ghi tên cũ.
- Các ví dụ ở Bảng 1.1 đều giữ chữ "lên đến" trong tuyên bố, nên không phụ thuộc vào quyết định còn mở về việc bỏ chữ "lên đến". Hàng "Đảm bảo..." theo dòng D2 của hướng dẫn. Hàng 6,5 giờ theo ví dụ V44.
- [22] mới đối chiếu qua bài báo lsvn.vn trích nguyên văn, chưa đối chiếu được văn bản trên Công báo. Phải kiểm trước khi nộp.
- Số liệu trích dẫn được đối chiếu tự động với văn bản PDF ngày 05/11/2026.
