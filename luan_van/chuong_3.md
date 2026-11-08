# Chương 3. Phương pháp đề xuất

Chương này trình bày phương pháp kiểm chứng P. Mục 3.1 nêu ý tưởng chung và sơ đồ của P. Mục 3.2 phát biểu bài toán ở dạng chặt hơn Chương 1, gồm các khái niệm điều kiện, cách hiểu thông thường và ba trạng thái của một điều kiện. Các mục 3.3 đến 3.9 lần lượt trình bày bộ thông số bảy trường, bước tách tuyên bố và truy hồi, bước trích xuất có neo nguồn, bước chuẩn hóa, tệp cấu hình, bộ quyết định A–D và cách sinh lý do. Mục 3.10 mô tả hai bản bỏ thành phần dùng để đo đóng góp của từng phần. Mục 3.11 đi qua toàn bộ phương pháp bằng một ví dụ.

## 3.1. Ý tưởng chung

P tách việc kiểm chứng thành hai phần có trách nhiệm khác nhau. LLM chỉ làm việc đọc: trích từ tuyên bố và từ đoạn tài liệu các trường của một bộ thông số, kèm câu gốc cho từng trường. Mã Python làm mọi việc cần kết luận: kiểm câu gốc có thật, đưa giá trị về cùng cách ghi, xác định điều kiện của tuyên bố và đối chiếu điều kiện đó với điều kiện của từng thông số trong tài liệu để gán nhãn theo một thứ tự quy tắc cố định. Cách chia này nhắm vào hai nguồn lỗi đã nêu ở Chương 2: LLM có thể bỏ hoặc tự thêm điều kiện khi đọc văn bản, và LLM tự gán nhãn thì khó phân biệt một con số đúng với một con số đúng ở điều kiện khác.

Hình 3.1 là sơ đồ của P. Một tuyên bố đi qua sáu bước: truy hồi k đoạn tài liệu bằng BM25; LLM trích bộ thông số của tuyên bố và của mọi giá trị cùng thuộc tính trong k đoạn; Python kiểm neo nguồn; Python kiểm tra đầy đủ và chuẩn hóa; bộ quyết định A–D gán nhãn; cuối cùng lý do được ghép từ dấu vết của bộ quyết định. Ba bước giữa (neo nguồn, kiểm tra đầy đủ, bộ quyết định) là phần đề tài đề xuất; các bước còn lại dùng kỹ thuật đã có.

**Hình 3.1.** Sơ đồ phương pháp P (tuyên bố c, mẫu s → BM25 trên D(s) → LLM trích bộ thông số kèm câu gốc → neo nguồn → kiểm tra đầy đủ, chuẩn hóa → bộ quyết định A–D → nhãn y(c), đoạn nguồn e(c), lý do r(c); tệp cấu hình của nhóm sản phẩm cấp dữ liệu cho ba bước sau cùng)

## 3.2. Phát biểu bài toán

Bài toán được nêu ở mục 1.2: với bài quảng cáo q, mẫu sản phẩm s và kho tài liệu chính hãng D(s), hệ thống trả về cho mỗi tuyên bố c trong q một nhãn y(c), đoạn nguồn e(c) và lý do r(c). Mục này nêu rõ các khái niệm mà bộ quyết định dùng.

**Thuộc tính có điều kiện ràng buộc.** Mỗi nhóm sản phẩm có một danh sách thuộc tính mà hãng thường công bố kèm điều kiện. Đề tài dùng 16 thuộc tính: điện thoại có thời lượng pin, sạc nhanh, công suất sạc, độ sáng, tần số quét, zoom, kháng nước và dung lượng pin; tai nghe có thời lượng pin, sạc nhanh, kháng nước và dung lượng pin; đồng hồ có thời lượng pin, sạc nhanh, kháng nước và độ sáng. Tuyên bố về thuộc tính ngoài danh sách không thuộc phạm vi.

**Điều kiện.** Điều kiện là hoàn cảnh mà con số đạt được. Mỗi điều kiện thuộc một trong sáu loại: chế độ hoạt động, bộ phận, phụ kiện, điều kiện đo, phiên bản và kiểu giá trị (Bảng 3.2). Một số điều kiện là con số kèm quan hệ, gọi là điều kiện dạng số, ví dụ "bộ sạc 40W trở lên" hay "độ sâu tối đa 6 mét". Với mỗi thuộc tính, tệp cấu hình liệt kê các điều kiện bắt buộc, tức các điều kiện mà khi đổi thì con số đổi và người mua không tự suy ra được.

**Bảng 3.2.** Sáu loại điều kiện

| Loại | Ví dụ trong tài liệu tập phát triển |
|---|---|
| Chế độ hoạt động | bật hay tắt chống ồn; xem video hay xem video trực tuyến; chế độ nguồn điện thấp; chế độ hiển thị HDR |
| Bộ phận | tai nghe; hộp sạc; tổng thời gian kèm hộp sạc |
| Phụ kiện | bộ tiếp hợp 20W; sạc bằng cáp hay sạc không dây |
| Điều kiện đo | sạc tới 50%; sạc 15 phút; ngâm ở độ sâu 6 mét trong tối đa 30 phút; đo trên 25% diện tích màn hình |
| Phiên bản | Apple Watch SE 3 bản GPS hay GPS + Cellular |
| Kiểu giá trị | "lên đến" (tối đa), "điển hình", "định mức", "thích ứng"; từ khẳng định như "luôn", "đảm bảo", "hơn" |

**Điều kiện của tuyên bố.** Điều kiện của tuyên bố gồm điều kiện được nêu rõ và, với điều kiện bắt buộc không được nêu, cách hiểu thông thường ghi trong tệp cấu hình (mục 1.2). Điều kiện của tuyên bố được xác định một lần, trước khi so con số, và giữ nguyên trong mọi bước so sánh sau đó. Hệ thống không bao giờ chọn điều kiện theo con số của tuyên bố: nếu con số chỉ khớp ở một điều kiện khác, đó là dấu hiệu Lệch điều kiện chứ không phải căn cứ để đổi điều kiện.

**Ba trạng thái của một điều kiện.** Một điều kiện bắt buộc có thể không áp dụng, không được nêu, hoặc chưa xác định, và ba trạng thái này được xử lý khác nhau. Không áp dụng là khi tài liệu cho thấy điều kiện không ảnh hưởng tới con số trong trường hợp đang xét; ví dụ trang Apple Watch SE 3 ghi cùng một thời lượng pin cho cả hai phiên bản, nên phiên bản không cần khớp. Không được nêu là khi quảng cáo không nói điều kiện; hệ thống dùng cách hiểu thông thường và ghi lại điều kiện đó để phân tích độ nhạy. Chưa xác định là khi không đủ căn cứ để biết điều kiện của tuyên bố, ví dụ tuyên bố về độ sáng điện thoại không nêu chế độ hiển thị (khảo sát người đọc không cho một cách hiểu chung nào), hoặc tuyên bố có cụm điều kiện mà hệ thống không giải được. Khi đó hệ thống kết luận Chưa đủ thông tin.

**Khớp giá trị.** Giá trị của tuyên bố khớp giá trị của tài liệu khi bằng nhau sau chuẩn hóa, trong ngưỡng sai số tương đối 1%, hoặc kém thuận lợi hơn theo hướng thuận lợi của thuộc tính. Mỗi thuộc tính có một hướng: thời lượng pin, độ sáng, dung lượng pin cao hơn là tốt hơn; thời gian sạc tới một mốc phần trăm thấp hơn là tốt hơn; mã IP so theo nhánh của chuẩn IEC 60529 (mục 3.6). Ngưỡng 1% được chọn lại trên tập phát triển.

## 3.3. Bộ thông số bảy trường

Mọi tuyên bố và mọi thông số trong tài liệu được biểu diễn bằng cùng một bộ bảy trường (Bảng 3.1), nên bộ quyết định chỉ cần so hai bộ thông số cùng cấu trúc. Sáu loại điều kiện nằm trong các trường phiên bản, bộ phận và trường điều kiện cùng kiểu giá trị.

**Bảng 3.1.** Bộ thông số bảy trường

| # | Trường | Ví dụ | Loại điều kiện nằm trong trường |
|---|---|---|---|
| 1 | Sản phẩm | Galaxy Buds3 Pro | – |
| 2 | Phiên bản | Apple Watch SE 3 bản GPS + Cellular | Phiên bản |
| 3 | Bộ phận | tai nghe; tổng kèm hộp sạc | Bộ phận |
| 4 | Thuộc tính | thời lượng pin | – |
| 5 | Giá trị | 7 | – |
| 6 | Đơn vị | giờ | – |
| 7 | Điều kiện cùng kiểu giá trị | bật chống ồn; nghe nhạc; bộ sạc 40W trở lên; "lên đến" | Chế độ hoạt động, phụ kiện, điều kiện đo, kiểu giá trị |

Mỗi trường kèm câu gốc (trích) mà nó được đọc ra. Ngoài bảy trường, bộ thông số của một giá trị trong tài liệu còn có ba phần phụ: mã đoạn chứa giá trị; danh sách điều kiện lạ, tức các cụm điều kiện gắn với giá trị mà tệp cấu hình chưa biết; và cờ cho biết giá trị thuộc một sản phẩm khác (ví dụ cột khác của bảng so sánh). Điều kiện được ghi bằng tên và giá trị của tệp cấu hình, chẳng hạn chế độ chống ồn bằng "bật"; điều kiện dạng số ghi con số và đơn vị.

## 3.4. Tách tuyên bố và truy hồi bằng chứng

**Tách tuyên bố.** Thực nghiệm chính dùng tuyên bố tách bằng tay theo một hướng dẫn viết trước. Mỗi tuyên bố chỉ có một thuộc tính và một con số; tên sản phẩm và các điều kiện thuộc con số được đưa vào tuyên bố, kể cả khi nằm ở câu trước hay câu sau; không thêm điều kiện mà bài không nói và không sửa con số. Một điều kiện thuộc con số khi bổ nghĩa trực tiếp cho con số (cùng cụm, trong ngoặc ngay sau con số, hoặc đi liền sau các chữ "khi", "ở", "với", "trong", "dưới", "cùng", "kèm"), hoặc khi là điều kiện cụ thể ở vế nói tác dụng của chính con số. Điều kiện hay từ khẳng định ở vế nói về việc khác thì không thuộc con số. Một con số được nhắc hai lần, một lần kèm điều kiện và một lần không, được tách thành hai tuyên bố, vì người đọc lướt có thể chỉ thấy lần không kèm điều kiện. Tách tay tránh để cách làm của LLM lẫn vào đáp án chuẩn của bước tách tự động.

Tính năng trên CopyPro cần tách tự động. P dùng một câu lệnh chép đúng các quy tắc trên, yêu cầu LLM trả danh sách tuyên bố kèm câu gốc và thuộc tính dự kiến; Python chỉ giữ tuyên bố có thuộc tính thuộc danh sách của nhóm. Bước này được đánh giá riêng bằng Precision và Recall so với tách tay, trong đó hai tuyên bố được xem là trùng khi cùng bài, cùng thuộc tính và cùng giá trị sau chuẩn hóa.

**Truy hồi.** P chỉ tìm trong D(s), tài liệu của đúng mẫu người dùng chọn. Tài liệu đã được chia thành đoạn theo cấu trúc trang, và chú thích được nối vào đoạn mang ký hiệu chú thích tương ứng (mục 2.2), nên một đoạn gồm nội dung chính và các chú thích của nó. Truy vấn là chữ của tuyên bố; BM25 xếp hạng các đoạn và P lấy k đoạn có điểm cao nhất. Giá trị k (trong 3, 5 và 8) và cách tách từ (theo âm tiết hay theo từ) được chọn trên tập phát triển. Để so sánh công bằng, mọi phương pháp trong thực nghiệm nhận cùng k đoạn cho cùng một tuyên bố.

## 3.5. Trích xuất có neo nguồn

Bước trích xuất có ba khâu: (a) LLM trích bộ thông số kèm câu gốc; (b) Python kiểm neo nguồn và bỏ trường không đạt; (c) Python kiểm tra đầy đủ để bổ sung điều kiện mà LLM bỏ sót. Giữa (b) và (c) là khâu hiểu điều kiện, đưa cụm chữ về tên và giá trị của tệp cấu hình.

### 3.5.1. LLM trích bộ thông số

Mỗi tuyên bố cần một lần gọi LLM. Câu lệnh gồm danh sách thuộc tính của nhóm, định nghĩa sáu loại điều kiện, các quy tắc trích, hai ví dụ, tuyên bố và k đoạn tài liệu (Phụ lục). LLM trả về một đối tượng JSON gồm bộ thông số của tuyên bố và bộ thông số của mọi giá trị cùng thuộc tính tìm thấy trong k đoạn. Năm quy tắc chính của câu lệnh như sau.

- Lấy mọi giá trị của thuộc tính ở mọi điều kiện, kể cả giá trị ở điều kiện khác với tuyên bố và giá trị không bằng con số của tuyên bố. Bộ quyết định cần các giá trị này để nhận ra Lệch điều kiện.
- Mỗi trường kèm câu gốc chép nguyên văn; câu gốc của một giá trị trong tài liệu chép cả dòng chứa con số, gồm nhãn của dòng.
- Ghi mọi cụm điều kiện gắn với giá trị, kể cả cụm nằm trong chú thích và cụm lạ không giống ví dụ nào; mỗi cụm kèm loại của nó.
- Con số chỉ là điều kiện (công suất bộ sạc, mốc phần trăm, độ sâu) không phải giá trị. Không cộng, trừ hay nhân để tạo con số mới.
- Không ghi làm điều kiện các cụm khen không có nội dung đo và các câu rào chung của tài liệu.

Hai ví dụ trong câu lệnh dùng sản phẩm tự đặt ("Tai nghe B", "Điện thoại A") thay vì sản phẩm thật, để câu lệnh không chứa đáp án của tuyên bố nào trong dữ liệu. Quy tắc thứ ba thể hiện nguyên tắc "phát hiện điều kiện theo kiểu mở": LLM không bị giới hạn trong danh sách điều kiện của tệp cấu hình, nên điều kiện lạ không bị bỏ im lặng.

### 3.5.2. Neo nguồn

Neo nguồn kiểm từng trường mà LLM trả về và bỏ trường không đạt, không đoán thay. Phép so chuỗi dùng một dạng chuẩn hóa chung: đưa về dạng Unicode NFC, chữ thường, đổi mọi dấu câu và ký hiệu thành khoảng trắng, gộp khoảng trắng; dấu chấm và dấu phẩy nằm giữa hai chữ số được giữ để không làm sai con số. Bảng 3.3 nêu điều kiện đạt của từng trường.

**Bảng 3.3.** Điều kiện đạt của neo nguồn

| Trường | Đạt khi | Không đạt thì |
|---|---|---|
| Mã đoạn | thuộc k đoạn đã đưa vào câu lệnh | bỏ cả giá trị |
| Câu gốc của mọi trường | là chuỗi con của nguồn (chữ tuyên bố, hoặc văn bản của đoạn) | bỏ trường đó |
| Giá trị số | trong câu gốc có con số bằng giá trị; nếu có đơn vị thì đơn vị đi cùng con số đó trùng đơn vị LLM ghi | bỏ giá trị |
| Giá trị mã | mã IP hay mã ISO 22810 trong câu gốc trùng mã LLM ghi; giá trị phủ định ("không có khả năng kháng nước") có chữ "không" cùng "kháng nước" | bỏ giá trị |
| Cụm điều kiện | loại thuộc sáu loại; cụm là chuỗi con của câu gốc của nó | bỏ điều kiện đó |
| Thuộc tính của tuyên bố | thuộc danh sách thuộc tính của nhóm | để trống |

Một giá trị trong tài liệu bị bỏ thì không được đưa sang bộ quyết định nhưng vẫn được lưu để thống kê. Số trường bị bỏ của từng tuyên bố là một số liệu của Chương 4, cho thấy LLM tự thêm hay chép sai bao nhiêu.

### 3.5.3. Hiểu điều kiện theo kiểu đóng

Mỗi cụm điều kiện còn lại sau neo nguồn được đưa về tên và giá trị của tệp cấu hình, theo nguyên tắc "hiểu điều kiện theo kiểu đóng": chỉ cụm có trong tệp cấu hình mới thành điều kiện có tên. Hệ thống tìm cụm của tệp cấu hình bên trong cụm LLM ghi (không tìm trong cả câu gốc, vì câu gốc của một dòng có thể chứa điều kiện của con số khác) và xét theo thứ tự sau.

1. Cụm chỉ là ngữ cảnh (ví dụ "phòng thí nghiệm", "thiết bị tiền sản xuất") được ghi riêng và không tham gia quyết định.
2. Cụm khớp cách diễn đạt của một điều kiện trong tệp cấu hình thì thành điều kiện đó. Hai ràng buộc được áp: một số cách diễn đạt chỉ đọc ở một phía (ví dụ "sử dụng liên tục" là tên một bài đo ở phía tài liệu của Xiaomi 15T, còn ở phía tuyên bố chỉ có nghĩa là dùng không ngắt), và một số cách diễn đạt chỉ là điều kiện của một thuộc tính (ví dụ "kèm hộp sạc" chỉ là bộ phận khi nói về thời lượng pin).
3. Cụm không khớp cách diễn đạt nào nhưng chứa con số có đơn vị trùng đơn vị của đúng một điều kiện dạng số của thuộc tính thì thành điều kiện đó. Ví dụ với sạc nhanh điện thoại, "sạc tới 50%" là mốc phần trăm vì chỉ mốc phần trăm có đơn vị phần trăm, còn "củ sạc 45W" là công suất bộ tiếp hợp.
4. Cụm chỉ kiểu giá trị được để lại cho khâu (c), vì kiểu giá trị phải gắn với chính con số.
5. Cụm khen hay nhấn mạnh ("cả ngày", "chỉ trong") bị bỏ qua.
6. Cụm còn lại là điều kiện lạ và được giữ nguyên chữ, loại và câu gốc.

Điều kiện lạ không bị bỏ đi. Ở phía tuyên bố, điều kiện lạ làm điều kiện của tuyên bố trở thành chưa xác định. Ở phía tài liệu, giá trị mang điều kiện lạ không bao giờ dẫn tới nhãn Đúng (mục 3.8). Đây là cách P xử lý giới hạn bao phủ của tệp cấu hình: thà kết luận Chưa đủ thông tin còn hơn chấp nhận nhầm.

### 3.5.4. Kiểm tra đầy đủ

Kiểm tra đầy đủ dò lại các cách diễn đạt của tệp cấu hình trong văn bản nguồn để bổ sung điều kiện bắt buộc mà LLM bỏ sót. Vùng dò của tuyên bố là toàn bộ chữ tuyên bố. Vùng dò của một giá trị trong tài liệu chỉ là các dòng chứa câu gốc của giá trị đó, không phải cả đoạn, vì một đoạn thường liệt kê nhiều giá trị ở nhiều điều kiện. Khâu này gồm bốn việc.

- Với mỗi điều kiện bắt buộc còn trống, dò cách diễn đạt của điều kiện đó trong vùng dò. Thấy đúng một giá trị thì điền vào và ghi là được bổ sung; thấy hai giá trị khác nhau thì không điền. Điều kiện dạng số được dò thêm theo đơn vị như ý 3 ở mục 3.5.3, bỏ qua chính con số của giá trị.
- Kiểu giá trị được xác định bằng hàm của bước chuẩn hóa (mục 3.6), chỉ xét cụm đứng liền con số. Kiểu do LLM ghi mà không đứng liền con số thì không được dùng.
- Dòng tài liệu dạng "a / b giờ" không ghi bộ phận được đọc theo quy ước của tệp cấu hình cho thời lượng pin tai nghe: số nhỏ là của tai nghe, số lớn là tổng kèm hộp sạc. Quy ước này có căn cứ trong chú thích của trang Galaxy Buds3 Pro ("tai nghe và hộp tai nghe cung cấp tối đa 30 giờ phát") [24].
- Tên sản phẩm của giá trị được kiểm bằng bảng bí danh; giá trị của sản phẩm khác được đánh dấu để bộ quyết định bỏ qua.

Kiểm tra đầy đủ không sửa điều kiện đã có, chỉ điền chỗ trống, và không dò được điều kiện lạ vì điều kiện lạ không có trong tệp cấu hình. Số điều kiện được bổ sung là số liệu thứ hai của Chương 4.

## 3.6. Chuẩn hóa

Bước chuẩn hóa đưa các cách ghi khác nhau về cùng một dạng để so được với nhau. Mọi danh sách cụm được đọc từ tệp cấu hình; mã nguồn chỉ chứa khung nhận dạng con số và mã. Bước này gồm năm phần.

- **Con số.** Tài liệu tập phát triển dùng hai kiểu ghi số: Apple và Xiaomi dùng dấu chấm ngăn hàng nghìn ("3.000 nit"), Samsung dùng dấu chấm thập phân ("4.5" giờ), và dấu phẩy luôn là thập phân ("13,19 giờ"). Quy tắc đọc: dấu chấm theo sau đúng ba chữ số là ngăn hàng nghìn, theo sau một hoặc hai chữ số là thập phân.
- **Đơn vị.** Giờ, tiếng và h là một đơn vị; nit, nits và cd/m² là một đơn vị; giờ và phút đổi được cho nhau. Đơn vị dài được khớp trước để "mAh" không bị đọc thành "m".
- **Mã kháng nước.** Mã IP được tách thành chữ số bụi và chữ số nước. Chữ số bụi xếp thành thang, cao hơn là tốt hơn. Chữ số nước chia hai nhánh, 0 đến 6 là chịu tia nước và 7, 8 là chịu ngâm; chỉ so trong cùng nhánh, khác nhánh thì không khớp. Đồng hồ theo chuẩn ISO 22810 được quy về mét (5ATM bằng WR50 bằng 50 m).
- **Kiểu giá trị.** Cụm "lên đến", "tối đa", "đến", "tới" cho kiểu tối đa; "điển hình", "typ" cho kiểu điển hình; "định mức" cho kiểu định mức; "thích ứng" cho kiểu thích ứng. Từ khẳng định ("luôn", "đảm bảo", "bảo đảm", "ít nhất", "mọi lúc") và nhóm mức sàn ("hơn", "trên", "không dưới" đứng trước con số, "trở lên" đứng sau) cho kiểu khẳng định. Chỉ cụm đứng liền con số của chính giá trị mới được tính; trong "sạc đến 50% trong 30 phút", chữ "đến" thuộc con số 50%, không thuộc 30 phút. Dạng phủ định ("không đảm bảo") và tên tính năng ("Màn hình Luôn Bật") không tính.
- **Tên sản phẩm và phiên bản.** Tên được khớp theo bảng bí danh của tệp cấu hình, lấy khớp dài nhất, và mỗi mẫu có danh sách tên dễ nhầm. Nhờ vậy "iPhone 17 Pro" không bị nhận là iPhone 17, trong khi "Apple Watch SE 3" vẫn là Apple Watch SE 3 dù "Apple Watch SE" nằm trong danh sách dễ nhầm.

## 3.7. Tệp cấu hình điều kiện bắt buộc

Tệp cấu hình là nơi tập trung mọi tri thức về điều kiện mà bộ quyết định cần, tách khỏi mã nguồn. Đề tài có một tệp dùng chung và ba tệp cho ba nhóm sản phẩm. Với mỗi thuộc tính, tệp nhóm ghi: đơn vị; hướng thuận lợi; kiểu giá trị mặc định; các điều kiện bắt buộc cùng loại của chúng; cách hiểu thông thường của từng điều kiện; phạm vi áp dụng; và căn cứ là mã đoạn tài liệu. Mỗi điều kiện có danh sách cách diễn đạt, chia hai nguồn: cụm có thật trong tài liệu tập phát triển, và cách nói thường gặp chưa có trong tài liệu. Tệp dùng chung ghi các quy tắc chung: cách đọc số, các cụm kiểu giá trị, từ khẳng định, cụm phủ nhiều giá trị, cụm chỉ là ngữ cảnh và luật chặn điều kiện lạ.

Cách hiểu thông thường theo nguyên tắc của đề tài: hiểu như người mua thông thường, lấy bộ phận chính và không mua thêm phụ kiện. Bảng 3.4 tóm tắt các cách hiểu chính; bảng đầy đủ nằm trong hướng dẫn gán nhãn ở Phụ lục. Các cách hiểu này đã được đối chiếu với một khảo sát nhỏ về cách người đọc hiểu quảng cáo; ở độ sáng điện thoại, không cách hiểu nào được quá nửa người đọc chọn, nên điều kiện chế độ hiển thị không có cách hiểu thông thường.

**Bảng 3.4.** Một số cách hiểu thông thường khi tuyên bố không nêu điều kiện

| Nhóm, thuộc tính | Điều kiện | Không nêu thì hiểu là |
|---|---|---|
| Điện thoại, thời lượng pin | Hoạt động | Hoạt động kém thuận lợi nhất trong các hoạt động hãng công bố |
| Điện thoại, sạc nhanh | Bộ tiếp hợp | Không mua thêm: chỉ có đồ trong hộp |
| Điện thoại, sạc nhanh | Mốc phần trăm | Không có cách hiểu chung: tuyên bố phải tự nêu |
| Điện thoại, độ sáng | Chế độ hiển thị | Không có cách hiểu chung: tuyên bố phải tự nêu |
| Điện thoại, zoom | Loại zoom | Quang học |
| Tai nghe, thời lượng pin | Chống ồn; bộ phận; hoạt động | Bật (hãng ghi chống ồn bật theo mặc định); chỉ tai nghe; nghe nhạc |
| Đồng hồ, thời lượng pin | Chế độ nguồn; hoạt động | Chế độ thường; sử dụng bình thường |
| Mọi nhóm, kháng nước | Độ sâu, thời gian ngâm, loại nước | Như hãng công bố |

Tệp cấu hình chỉ được viết từ tài liệu của tập phát triển và hiểu biết chung về nhóm sản phẩm; không có quy tắc nào viết riêng cho một mẫu của tập kiểm tra. Một chương trình kiểm tra tự động bảo đảm rằng mỗi điều kiện có đủ cách hiểu và cách diễn đạt, mọi căn cứ thuộc tập phát triển, và mọi cụm ghi là "có trong tài liệu" đúng là có trong tài liệu tập phát triển. Tệp cấu hình được khóa cùng các tham số khác trước khi chạy tập kiểm tra.

## 3.8. Bộ quyết định A–D

Bộ quyết định nhận bộ thông số của tuyên bố và bộ thông số của các giá trị trong tài liệu, rồi gán nhãn qua bốn bước: (A) tìm thông số cùng sản phẩm và thuộc tính; (B) xác định điều kiện của tuyên bố; (C) so giá trị theo đơn vị và hướng thuận lợi; (D) tổng hợp theo một thứ tự dòng cố định. Thuật toán 3.1 là mã giả của bộ quyết định; các mục con dưới đây giải thích từng bước.

**Thuật toán 3.1.** Bộ quyết định A–D (doi_chieu = sai là bản P−ĐK ở mục 3.10)

```
hàm quyết_định(tb, ứng_viên, cấu_hình, doi_chieu = đúng):
    # A. Thông số cùng sản phẩm và thuộc tính
    cùng_tt ← {u ∈ ứng_viên | cùng sản phẩm, cùng thuộc tính, có giá trị}
    nếu cùng_tt rỗng: trả Chưa đủ thông tin (D1)
    nếu doi_chieu: cùng_tt ← lan_điều_kiện(cùng_tt)

    # B. Điều kiện của tuyên bố: nêu rõ, rồi cách hiểu thông thường
    nếu doi_chieu:
        dk ← điều_kiện_tuyên_bố(tb, cùng_tt, cấu_hình)
        nếu dk chưa xác định: trả Chưa đủ thông tin (D1a)
        cùng_dk ← {u ∈ cùng_tt | khớp_điều_kiện(dk, u)}
        nếu có u ∈ cùng_dk mang điều kiện lạ và khớp_giá_trị(tb, u): trả Chưa đủ thông tin (D1a)
        nếu cùng_dk có hai giá trị khác nhau mà tb không khớp cả hai: trả Chưa đủ thông tin (D1b)
    ngược lại: cùng_dk ← cùng_tt
    khác_dk ← cùng_tt − cùng_dk

    # C, D. So giá trị và tổng hợp
    nếu tb có từ khẳng định và có u ∈ cùng_dk kiểu tối đa mà tb không thuận lợi hơn u: trả Lệch điều kiện (D2)
    nếu có u ∈ cùng_dk mà khớp_giá_trị(tb, u): trả Đúng (D3)
    nếu có u ∈ khác_dk mà bằng(tb, u): trả Lệch điều kiện (D4)
    nếu cùng_dk khác rỗng, hoặc tb thuận lợi hơn mọi giá trị cùng bộ phận và phiên bản: trả Sai (D5)
    trả Chưa đủ thông tin (D6)
```

### 3.8.1. Bước A: thông số cùng sản phẩm và thuộc tính

Bước A giữ các giá trị trong tài liệu cùng thuộc tính với tuyên bố, có giá trị đã qua neo nguồn, và không thuộc sản phẩm khác. Không còn giá trị nào thì tuyên bố dừng ở D1 (Chưa đủ thông tin). Tuyên bố mà bước trích xuất không đọc được thuộc tính hay giá trị cũng ra Chưa đủ thông tin và được ghi là lỗi trích xuất. Với sạc nhanh của đồng hồ, giá trị tính bằng phút (thời gian sạc tới một mốc) và giá trị tính bằng giờ (số giờ dùng sau vài phút sạc) là hai dạng, chỉ so trong cùng dạng.

Bước A còn áp một luật gọi là lan điều kiện. Cùng một dòng thông số thường được nhắc lại ở nhiều đoạn của trang: phần giới thiệu, khối nổi bật, bảng thông số. Có khi chỉ một đoạn ghi điều kiện, các đoạn khác chỉ ghi con số. Nếu để nguyên, đoạn không ghi điều kiện sẽ được hiểu là "như hãng công bố" và một tuyên bố bỏ điều kiện có thể được chấp nhận nhầm. Luật lan điều kiện xử lý việc này: trong nhóm các giá trị bằng nhau, nếu những giá trị có ghi một điều kiện đều ghi cùng một giá trị điều kiện, thì giá trị không ghi điều kiện đó nhận giá trị điều kiện ấy; nếu các đoạn ghi khác nhau thì không lan. Điều kiện lạ cũng được lan. Ví dụ, trang Xiaomi 15T ghi độ sáng 3200 nit "trên 25% diện tích màn hình" ở bảng thông số nhưng chỉ ghi "Màn hình siêu sáng 3.200 nit" ở phần giới thiệu; sau khi lan, cả hai đoạn đều mang điều kiện đo trên 25% diện tích, và tuyên bố "sáng 3200 nit trên toàn màn hình" không còn khớp ở đoạn giới thiệu.

### 3.8.2. Bước B: điều kiện của tuyên bố

Bước B xác định điều kiện của tuyên bố một lần, theo năm nguồn được xét lần lượt.

1. **Điều kiện nêu rõ** do bước trích xuất đọc từ tuyên bố được giữ nguyên. Riêng các cụm chỉ sự liên tục hay mức dùng chung ("dùng liên tục", "sử dụng") và cụm "xem video" không kèm loại được coi là chưa nêu hoạt động.
2. **Cụm phủ nhiều giá trị** ("ở mọi chế độ", "dù nghe nhạc hay gọi điện") nghĩa là tuyên bố phải đúng ở từng giá trị được phủ, nên điều kiện của tuyên bố là giá trị kém thuận lợi nhất trong các giá trị được phủ mà tài liệu công bố. Với kháng nước, "mọi hoạt động" phủ cả các hoạt động hãng khuyến cáo không dùng.
3. **Luật chép đúng nhãn của tài liệu.** Nhãn của một dòng thông số là chữ của dòng sau khi bỏ con số, đơn vị và cụm kiểu giá trị, ví dụ "xem video" của dòng "Thời gian xem video: Lên đến 30 giờ". Khi chữ tuyên bố chứa trọn nhãn của một dòng, và đó là nhãn dài nhất được chứa, điều kiện của tuyên bố lấy theo dòng đó. Luật này phản ánh việc đề tài so quảng cáo với tài liệu: quảng cáo chép đúng nhãn của một dòng thì không thiếu điều kiện so với dòng ấy. Luật không lấy điều kiện về phụ kiện bán riêng, vì con số cần bộ sạc mua thêm mà quảng cáo không nêu bộ sạc vẫn gây hiểu nhầm.
4. **Chữ gọi mức cao của độ sáng** ("tối đa", "đỉnh", "cực đại") được tra theo cách gọi của từng hãng, chỉ khi tài liệu dùng chữ đó để phân biệt từ hai giá trị trở lên. Ở trang iPhone 17, "tối đa" chỉ chế độ tiêu chuẩn còn "đỉnh" trỏ tới hai chế độ, nên tuyên bố chỉ ghi "đỉnh" là chưa xác định. Ở trang chỉ có một giá trị độ sáng, chữ này chỉ là kiểu tối đa.
5. **Cách hiểu thông thường** được dùng cho mỗi điều kiện bắt buộc còn trống và áp dụng được. Một điều kiện áp dụng khi có ít nhất một giá trị trong tài liệu ghi điều kiện đó, hoặc khi thuộc tính chỉ có nghĩa với điều kiện đó (mốc phần trăm của sạc nhanh, chế độ hiển thị của độ sáng điện thoại). Cách hiểu là giá trị cụ thể thì dùng ngay; "kém thuận lợi nhất" thì lấy giá trị điều kiện có con số kém nhất trong tài liệu; "không mua thêm" thì giá trị nào cần bộ tiếp hợp là khác điều kiện; "như hãng công bố" thì không ràng buộc; "không có cách hiểu chung" thì điều kiện chưa xác định.

Một ngoại lệ được gọi là so thẳng: khi tài liệu chỉ có một con số cho thuộc tính và con số đó không kèm cụm điều kiện nào, tuyên bố không nêu điều kiện được so thẳng với con số đó. Ví dụ, trang Apple Watch SE 3 chỉ ghi "Độ sáng đỉnh 1000 nit", nên tuyên bố "có độ sáng 1000 nit" được so thẳng.

Điều kiện của tuyên bố là chưa xác định, và tuyên bố dừng ngay ở D1a, trong ba trường hợp: tuyên bố có điều kiện lạ không phải cụm phủ; chữ của tuyên bố trỏ tới nhiều chế độ; hoặc một điều kiện áp dụng không có cách hiểu chung mà tuyên bố không nêu. Cách hiểu thông thường không bao giờ là lý do dừng ở D1a, và con số không khớp ở điều kiện đã xác định cũng không.

### 3.8.3. Bước C và D: so giá trị và thứ tự quyết định

Hai giá trị cùng điều kiện khi mọi điều kiện bắt buộc áp dụng đều khớp: điều kiện chữ thì bằng nhau, điều kiện dạng số thì thỏa quan hệ khai báo trong tệp cấu hình (ví dụ bộ sạc của tuyên bố phải bằng hoặc mạnh hơn mức tối thiểu hãng ghi, độ sâu của tuyên bố phải không quá độ sâu hãng thử), và kiểu giá trị được so khi tuyên bố ghi rõ. Bộ quyết định chia các giá trị cùng thuộc tính thành nhóm cùng điều kiện với tuyên bố và nhóm khác điều kiện, rồi đi lần lượt các dòng của Bảng 3.5 và dừng ở dòng đầu tiên thỏa.

**Bảng 3.5.** Thứ tự quyết định

| Dòng | Kiểm tra | Nhãn |
|---|---|---|
| D1 | Tài liệu của đúng sản phẩm không có con số nào cho thuộc tính | Chưa đủ thông tin |
| D1a | Không xác định được điều kiện của tuyên bố; hoặc giá trị khớp mang điều kiện lạ | Chưa đủ thông tin |
| D1b | Ở điều kiện của tuyên bố, tài liệu ghi hai giá trị khác nhau, trừ khi con số của tuyên bố khớp cả hai | Chưa đủ thông tin, đánh dấu tài liệu mâu thuẫn |
| D2 | Từ khẳng định gắn với con số cho một mức không cao hơn mức "lên đến" ở cùng điều kiện | Lệch điều kiện |
| D3 | Ở đúng điều kiện của tuyên bố có giá trị khớp | Đúng |
| D4 | Con số của tuyên bố bằng giá trị công bố ở một điều kiện khác | Lệch điều kiện |
| D5 | Con số mâu thuẫn với giá trị ở cùng điều kiện, hoặc thuận lợi hơn mọi giá trị cùng bộ phận và phiên bản | Sai |
| D6 | Còn lại: tài liệu không công bố giá trị ở điều kiện của tuyên bố | Chưa đủ thông tin |

Ba điểm của thứ tự này cần giải thích. Thứ nhất, D1a và D1b được thêm vào chuỗi D1–D6 ban đầu, suy ra từ định nghĩa nhãn Chưa đủ thông tin (vế "ghi mâu thuẫn") và từ nguyên tắc "không xác định được điều kiện thì kết luận Chưa đủ thông tin"; hai dòng được đặt trước D2 để không bao giờ dẫn tới Đúng. Thứ hai, D2 chỉ áp khi tuyên bố có từ khẳng định gắn với con số; tuyên bố chỉ bỏ chữ "lên đến" vẫn khớp ở D3. Thứ ba, D4 xét mọi điều kiện khác, kể cả hoạt động khác, nên một con số trùng ngẫu nhiên với giá trị của hoạt động khác cũng ra Lệch điều kiện; rủi ro này được đếm riêng trên tập phát triển.

**Luật chặn điều kiện lạ.** Giá trị trong tài liệu mang điều kiện lạ không bao giờ dẫn tới Đúng: nếu tuyên bố khớp giá trị này, kết luận là Chưa đủ thông tin ở D1a với nguyên nhân "điều kiện lạ". Luật này giữ cho FAR không tăng khi tài liệu có điều kiện mà tệp cấu hình chưa biết. Một biến thể của luật, coi các giá trị chỉ khác nhau ở cùng một điều kiện lạ là lựa chọn của người dùng và lấy giá trị kém thuận lợi nhất, được cài thành công tắc, mặc định tắt và chọn trên tập phát triển.

**Loại biến đổi.** Với nhãn Lệch điều kiện ở D4, bộ quyết định ghi loại biến đổi bằng cách so điều kiện của tuyên bố với điều kiện của giá trị trùng: điều kiện khác nhau mà tuyên bố không nêu là bỏ điều kiện; nêu rõ khác đi là đổi điều kiện, đổi bộ phận, đổi phiên bản hoặc đổi kiểu giá trị. Nhiều giá trị cùng trùng thì chọn giá trị khác ít điều kiện nhất. Nhãn Sai ghi loại đổi giá trị, trừ khi tuyên bố gán con số cho một bộ phận hay phiên bản mà tài liệu không công bố giá trị nào.

## 3.9. Sinh lý do

Lý do được ghép từ dấu vết của bộ quyết định theo một mẫu câu cố định cho mỗi dòng (Bảng 3.6), nên lý do luôn khớp với nhãn và luôn kèm câu gốc của tài liệu. Chỗ trống "câu trích" là câu gốc nguyên văn của giá trị mà nhãn dựa vào. Khi tuyên bố bỏ chữ "lên đến" mà vẫn khớp, lý do ghi thêm điều này để người đọc biết.

**Bảng 3.6.** Mẫu câu lý do

| Dòng | Mẫu câu |
|---|---|
| D1 | Tài liệu của {sản phẩm} không có thông số {thuộc tính}. |
| D1a | Chưa xác định được điều kiện của tuyên bố: “{cụm điều kiện}”. |
| D1b | Tài liệu ghi hai giá trị khác nhau cho {thuộc tính} ở {điều kiện}: “{câu trích 1}” và “{câu trích 2}”. |
| D2 | Tài liệu ghi mức tối đa: “{câu trích}”; tuyên bố viết thành mức chắc chắn đạt. |
| D3 | Khớp với tài liệu: “{câu trích}”. |
| D4 | Giá trị {giá trị} {đơn vị} chỉ đạt khi {điều kiện trong tài liệu}; tuyên bố {nêu hoặc được hiểu là} {điều kiện của tuyên bố}. Nguồn: “{câu trích}”. |
| D5 | Tài liệu ghi {giá trị trong tài liệu} {đơn vị} ở {điều kiện}; tuyên bố ghi {giá trị}. |
| D6 | Tài liệu không công bố {thuộc tính} ở {điều kiện của tuyên bố}. |

Đoạn nguồn e(c) là danh sách mã các đoạn chứa giá trị mà nhãn dựa vào: mọi đoạn có cùng con số ở cùng điều kiện với nhãn Đúng và Sai, mọi đoạn chứa giá trị trùng với nhãn Lệch điều kiện.

## 3.10. Các bản bỏ thành phần

Để đo đóng góp của từng thành phần (câu hỏi 3), P có hai cờ cấu hình tạo ra hai bản bỏ thành phần, không sao chép mã.

- **P−ĐK** bỏ bước B: mọi giá trị cùng sản phẩm và thuộc tính được coi như cùng điều kiện, nên chỉ còn so giá trị. Bản này tắt cả D1a và D1b; nếu không, các giá trị khác nhau ở những điều kiện khác nhau sẽ bị coi là tài liệu mâu thuẫn. Kết quả là P−ĐK không bao giờ ra Lệch điều kiện ở D4.
- **P−NN** bỏ neo nguồn và kiểm tra đầy đủ của bước trích xuất, dùng nguyên đầu ra của LLM. Khâu hiểu điều kiện vẫn chạy để bộ quyết định có tên điều kiện. P−NN dùng chính đầu ra LLM của P (cùng bộ nhớ đệm), nên khác biệt giữa hai bản chỉ do hai khâu kiểm.

## 3.11. Ví dụ xuyên suốt

Mục này đi qua P với tuyên bố "Galaxy Buds3 Pro nghe nhạc lên đến 7 giờ khi bật chống ồn". Trang của hãng ghi 7 giờ khi tắt chống ồn và 6 giờ khi bật chống ồn [24].

**Truy hồi.** BM25 trả về các đoạn có chữ "thời gian phát", "ANC", "giờ", trong đó có khối "Thời gian phát" và bảng thông số. Khối "Thời gian phát" ghi dọc "Tắt Tính năng ANC / Đến 7 / 30 giờ / BẬT Tính năng ANC / Đến 6 / 26 giờ"; bảng thông số ghi từng dòng như "Thời gian phát nhạc (bật ANC) Lên đến 6" và "Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7".

**Trích xuất và neo nguồn.** Ở phía tuyên bố, LLM đọc thuộc tính thời lượng pin, giá trị 7 giờ và ba cụm điều kiện "nghe nhạc", "lên đến", "bật chống ồn". Ở phía tài liệu, LLM ghi các giá trị 7, 30, 6 và 26 của khối "Thời gian phát" cùng các dòng của bảng thông số, mỗi giá trị kèm dòng gốc. Neo nguồn kiểm từng câu gốc có trong đoạn và từng con số có trong câu gốc của nó; dòng bảng không ghi đơn vị như "Lên đến 6" vẫn đạt vì con số có mặt và đơn vị lấy theo thuộc tính.

**Hiểu điều kiện và kiểm tra đầy đủ.** "Bật chống ồn" khớp cách diễn đạt của chế độ chống ồn bật, "nghe nhạc" khớp hoạt động nghe nhạc, "Tắt Tính năng ANC" khớp chế độ chống ồn tắt. Dòng "Đến 7 / 30 giờ" không ghi bộ phận, nên quy ước cặp số gán 7 giờ cho tai nghe và 30 giờ cho tổng kèm hộp sạc. Chữ "Đến" đứng liền "7 / 30" cho kiểu tối đa cho cả hai số.

**Bộ quyết định.** Bước A giữ các giá trị thời lượng pin. Con số 7 giờ xuất hiện ở cả khối "Thời gian phát" và bảng thông số; điều kiện nào một nơi ghi mà nơi kia chưa ghi (ví dụ bộ phận tai nghe suy từ cặp số) được luật lan điều kiện điền sang, vì hai nơi cùng gắn 7 giờ với chế độ tắt chống ồn và không mâu thuẫn nhau. Bước B xác định điều kiện của tuyên bố: chống ồn bật và nghe nhạc được nêu rõ; bộ phận không nêu nên hiểu là tai nghe. Nhóm cùng điều kiện chỉ có giá trị 6 giờ, nên không có mâu thuẫn ở D1b. Tuyên bố không có từ khẳng định nên bỏ qua D2. Ở D3, 7 giờ thuận lợi hơn 6 giờ nên không khớp. Ở D4, 7 giờ bằng giá trị ở điều kiện tắt chống ồn, nên nhãn là Lệch điều kiện, loại đổi điều kiện.

**Lý do.** Theo mẫu câu của D4: "Giá trị 7 giờ chỉ đạt khi tắt chống ồn; tuyên bố nêu bật chống ồn. Nguồn: “Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7”." Đoạn nguồn gồm mọi đoạn chứa giá trị 7 giờ ở điều kiện tắt chống ồn.

**So với P−ĐK.** Bản bỏ đối chiếu điều kiện chỉ so con số. Con số 7 giờ có trong tài liệu nên P−ĐK kết luận Đúng. Đây chính là lỗi chấp nhận nhầm mà P nhắm tới.

## 3.12. Kết chương

Chương này trình bày phương pháp P theo nguyên tắc để LLM đọc và để mã nguồn kết luận. LLM trích bộ thông số kèm câu gốc theo kiểu mở; neo nguồn bỏ những gì không có thật trong văn bản; khâu hiểu điều kiện và kiểm tra đầy đủ đưa điều kiện về tệp cấu hình theo kiểu đóng; bộ quyết định xác định điều kiện của tuyên bố trước rồi mới so con số, theo một thứ tự dòng cố định. Các luật cài thêm cho trường hợp thật của tài liệu (lan điều kiện giữa các đoạn, chép đúng nhãn, cặp số gạch chéo, điều kiện dạng số theo đơn vị) đều được kiểm bằng các ví dụ của hướng dẫn gán nhãn. Chương 4 trình bày dữ liệu, cách đánh giá P so với các đối chứng và kết quả.

## Ghi chú cho người duyệt

Mục này không đưa lên Google Doc.

- Nháp đầu do Opus viết ngày 08/11/2026 (Bước 35), sớm hơn lịch (30/11) để viết khi mã còn mới; mọi mô tả theo mã ở commit `688a14b` (trích xuất), `fde903c` (bộ quyết định), `1cf2e2e` (P đầu-cuối). Nếu Bước 28–33 đổi luật hay tham số thì sửa lại chương này.
- Chưa có Hình 3.1 thật: Bước 35 việc 2 yêu cầu vẽ lại Hình 1 của đề cương ở độ phân giải cao, mũi tên thẳng, chỉ tô khối chứa điểm mới (neo nguồn, kiểm tra đầy đủ, bộ quyết định). Bảng 3.1 lặp T5.1; Bảng 3.5, 3.6 lặp hướng dẫn mục 7, 8.
- Chương 3 cố ý không nêu số liệu của bài báo khác để khỏi cần số trang mới; các chỗ dẫn về cơ sở lý thuyết trỏ về Chương 2. Trích dẫn duy nhất là [24] (trang Galaxy Buds3 Pro).
- Thuật ngữ "luật cài" (luật thêm để máy chạy được hướng dẫn) không dùng trong thân chương; các luật đó được trình bày như một phần của phương pháp.
- Chưa đưa lên Google Doc. Khi đưa lên, Thuật toán 3.1 đặt trong khung chữ đều, đánh số như bảng.
