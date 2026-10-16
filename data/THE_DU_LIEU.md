# Thẻ dữ liệu — bản đầu, Bước 4

Ngày chọn mẫu và chia tập: **15/10/2026**. Phiên bản: **2** (kiểm lại nguồn; giữ nguyên 12 mẫu và cách chia tập).
Danh sách chính: [mau_san_pham.csv](mau_san_pham.csv).

## Hai tập dùng để làm gì?

- **Tập phát triển (4 mẫu):** dùng để thử và sửa phương pháp, câu lệnh gửi LLM, quy tắc và tham số.
- **Tập kiểm tra (8 mẫu):** dành cho lần đánh giá sau khi đã chốt phương pháp. Không dùng kết quả của tập này để sửa phương pháp rồi báo lại như một lần kiểm tra mới.

Đây là cách chia có chủ đích theo kế hoạch T6.3, không phải chia ngẫu nhiên. Giữ bốn mẫu phát triển đã đề xuất. Chọn tám mẫu còn lại để tập kiểm tra có đủ nhóm và hãng. Tỷ lệ 4/8 phục vụ quy mô khóa luận; không phải tỷ lệ bắt buộc cho mọi nghiên cứu.

| Nhóm | Tập phát triển | Tập kiểm tra |
|---|---|---|
| Điện thoại | iPhone 17; Xiaomi 15T | OPPO Find X8; Galaxy S25 Ultra; Redmi Note 14 Pro+ 5G |
| Tai nghe | Galaxy Buds3 Pro | AirPods Pro 3; AirPods 4 bản thường; Redmi Buds 6 Pro |
| Đồng hồ | Apple Watch SE 3 GPS 44 mm | Galaxy Watch8 Bluetooth 44 mm; Xiaomi Watch S4 |
| **Tổng** | **4** | **8** |

Có 5 điện thoại, 4 tai nghe và 3 đồng hồ. Bốn hãng là Apple, Samsung, Xiaomi và OPPO. Redmi được tính vào hãng Xiaomi. Cả hai tập có đủ ba nhóm; riêng tập kiểm tra có đủ cả bốn hãng. Hai mẫu làm thử ở Bước 5 là iPhone 17 và Galaxy Buds3 Pro.

## Nguồn

Chỉ chọn trang tiếng Việt do chính hãng công bố. Mỗi mẫu phải có ít nhất ba thông số bằng số gắn với điều kiện sử dụng, cách đo hoặc cách thử. Phải ghi được URL và ngày truy cập. Không dùng bài của cửa hàng, đánh giá của khách hàng hay bài tổng hợp để thay nguồn hãng.

Cột `url` trỏ tới trang thông số hoặc trang sản phẩm có mục thông số. Cột `url_bo_sung` chứa trang giới thiệu hoặc hướng dẫn sử dụng tiếng Việt của đúng mẫu do hãng phát hành, khi điều kiện thử nằm ở đó. Cần đọc và lưu cả nguồn chính lẫn nguồn bổ sung. Với Watch8, trang sản phẩm ghi 5ATM; hướng dẫn đúng mã SM-L330 giải thích điều kiện thử ở trang 149. Trang hỗ trợ chính hãng có thông số tiếng Việt cũng được chấp nhận.

Chỉ đếm thuộc tính thuộc phạm vi T4.1/T4.5 của kế hoạch. Loại kích thước, khối lượng, phiên bản Bluetooth và điều kiện để bật một tính năng sức khỏe. Không coi câu chung “kết quả thực tế có thể khác” là điều kiện đủ. Chưa tạo hoặc mở rộng cấu hình phương pháp dựa trên tập kiểm tra.

Ba mức của cùng một thuộc tính vẫn được tính nếu chúng có điều kiện khác nhau, chẳng hạn pin khi bật hoặc tắt chống ồn. Không đếm ba lần một thông số lặp lại ở nhiều vị trí. Bảng dưới chỉ ghi dấu vết kiểm tra nguồn, chưa phải bộ tuyên bố hay nhãn chuẩn.

AirPods 4 dùng trang hỗ trợ có mã cố định `121203`, đúng bản thường. Đường dẫn giới thiệu `/airpods-4/specs/` chuyển sang mẫu khác lúc kiểm tra nên không dùng. Trang Samsung có bảng so sánh nhiều mẫu và đánh giá của khách hàng; khi thu thập phải giữ đúng cột/mục của mẫu đã chọn, bỏ đánh giá khách hàng. Một số trang Samsung vượt giới hạn dung lượng của công cụ duyệt; đã đọc HTML trực tiếp để kiểm tra.

## Kiểm tra điều kiện chọn mẫu

Tất cả nguồn dưới đây được truy cập ngày **15/10/2026**. Số liệu được diễn giải ngắn để tìm lại đúng mục. Khi thu thập phải giữ toàn bộ chú thích và giới hạn của hãng, không dùng các câu rút gọn này thay cho bằng chứng gốc.

| Mẫu và nguồn | Ba thông số đã kiểm lại | Vị trí đối chiếu |
|---|---|---|
| [iPhone 17](https://www.apple.com/vn/iphone-17/specs/) | 1. Độ sáng đỉnh 3.000 nit — Chế độ ngoài trời. 2. Kháng nước IP68 — Bài thử phòng thí nghiệm: tối đa 6 m trong tối đa 30 phút; không phải mức được bảo đảm ở mọi tình huống sử dụng. 3. Sạc đến 50% trong 20 phút — Cáp USB-C, bộ tiếp hợp từ 40 W; thử từ pin cạn. | Mục màn hình; Mục chống nước và chú thích 3; Mục pin/sạc và chú thích 6 |
| [Xiaomi 15T](https://www.mi.com/vn/product/xiaomi-15t/specs/) · [bổ sung](https://www.mi.com/vn/product/xiaomi-15t/) | 1. Độ sáng cực đại 3.200 nit — Đo trên 25% diện tích màn hình. 2. Tần số quét tối đa 120 Hz — Tần số thay đổi theo giao diện ứng dụng và chất lượng hình ảnh của trò chơi. 3. Kháng nước IP68 — Ngâm nước ngọt tĩnh 3 m, tối đa 30 phút, chênh nhiệt không quá 5 K. | Mục màn hình; Chú thích 6; Mục chống bụi và nước |
| [Galaxy Buds3 Pro](https://www.samsung.com/vn/audio-sound/galaxy-buds/galaxy-buds3-pro-silver-sm-r630nzaaxxv/) | 1. Nghe nhạc tối đa 7 giờ — Chỉ tai nghe; tắt chống ồn chủ động. 2. Nghe nhạc tối đa 6 giờ — Chỉ tai nghe; bật chống ồn chủ động. 3. Kháng nước IP57 — Tai nghe được thử với nước ngọt ở 1 m trong tối đa 30 phút; hộp sạc không kháng nước. | Mục thời lượng sử dụng khi tắt ANC; Mục thời lượng sử dụng khi bật ANC; Chú thích IP57 |
| [Apple Watch SE 3](https://www.apple.com/vn/apple-watch-se-3/specs/) | 1. Pin tối đa 18 giờ — Dùng bình thường theo bài thử của Apple; bản GPS kết nối iPhone qua Bluetooth suốt 18 giờ. 2. Pin tối đa 32 giờ — Bật chế độ nguồn điện thấp; bài thử có 6 giờ theo dõi giấc ngủ; bản GPS kết nối iPhone qua Bluetooth. 3. Pin tối đa 7 giờ — Chạy bộ ngoài trời, không ghép đôi iPhone, bật cảm biến nhịp tim. | Mục pin và chú thích 8; Mục pin và chú thích 9 |
| [OPPO Find X8](https://www.oppo.com/vn/smartphones/series-find-x/find-x8/specs/) · [bổ sung](https://www.oppo.com/vn/smartphones/series-find-x/find-x8/) | 1. Độ sáng 800 nit — Chế độ thông thường mặc định. 2. Độ sáng 4.500 nit — Mức cực đại cục bộ, không phải toàn màn hình luôn sáng ở mức đó. 3. Kháng nước IP68 — Nước tĩnh ở 1,5 m trong 30 phút, chênh nhiệt không quá 5 °C. | Chú thích 13; Chú thích 11 |
| [Galaxy S25 Ultra](https://www.samsung.com/vn/smartphones/galaxy-s25-ultra/specs/) · [bổ sung](https://www.samsung.com/vn/smartphones/galaxy-s25-ultra/) | 1. Xem video tối đa 31 giờ — Bài thử video 720p lưu trên máy, tai nghe Bluetooth, thiết lập mặc định trên LTE. 2. Thu phóng tối đa 100x — Thu phóng kỹ thuật số, không phải zoom quang học 100x. 3. Kháng nước IP68 — Bài thử ngâm nước ngọt ở độ sâu tối đa 1,5 m trong tối đa 30 phút. | Mục pin và chú thích thử phát lại video; Câu hỏi về zoom 100x; Chú thích thử kháng nước |
| [Redmi Note 14 Pro+ 5G](https://www.mi.com/vn/product/redmi-note-14-pro-plus-5g/specs/) · [bổ sung](https://www.mi.com/vn/product/redmi-note-14-pro-plus-5g/) | 1. Pin 19,5 giờ — Hoạt động mạng xã hội; kết quả thử nghiệm nội bộ của hãng. Hãng không nêu đầy đủ thiết lập của bài thử này. 2. Pin 9 giờ — Xem video trực tuyến; kết quả thử nghiệm nội bộ của hãng. Hãng không nêu đầy đủ thiết lập của bài thử này. 3. Kháng nước IP68 — Nước ngọt tĩnh 1,5 m, tối đa 30 phút, chênh nhiệt không quá 5 K. | Khối pin: số 19,5 giờ và hoạt động bên dưới; Khối pin: số 9 giờ và hoạt động bên dưới; Mục chống bụi và nước |
| [AirPods Pro 3](https://www.apple.com/vn/airpods-pro/specs/) | 1. Nghe tối đa 8 giờ — Một lần sạc; bật chống ồn, âm lượng 50%, bài thử AAC 256 Kbps. 2. Nghe tối đa 7,5 giờ — Bật thêm âm thanh không gian và theo dõi chuyển động đầu trong bài thử của chú thích 13. 3. Nghe tối đa 6,5 giờ — Bật cảm biến nhịp tim và Xuyên Âm, âm lượng 50%; đi bộ ngoài trời và nghe nhạc từ iPhone. | Mục pin và chú thích 13; Mục pin và chú thích 14 |
| [AirPods 4](https://support.apple.com/vi-vn/121203) | 1. Nghe tối đa 5 giờ — Tai nghe bản thường, một lần sạc; âm lượng 50%, tắt âm thanh không gian, bài thử AAC 256 Kbps. 2. Nghe tổng cộng tối đa 30 giờ — Tính cả các lần sạc lại bằng hộp; cùng thiết lập âm thanh, thử đến khi cả tai nghe và hộp cạn pin. 3. Thêm khoảng 1 giờ nghe — Tai nghe ban đầu cạn pin được sạc 5 phút trong hộp; âm lượng 50%, tắt âm thanh không gian. | Mục pin và chú thích 9; Mục pin và chú thích 10; Mục pin và chú thích 11 |
| [Redmi Buds 6 Pro](https://www.mi.com/vn/product/redmi-buds-6-pro/specs/) · [bổ sung](https://www.mi.com/vn/product/redmi-buds-6-pro/) | 1. Nghe 9,5 giờ — Một lần sạc đầy; codec AAC, âm lượng 50%, tắt chống ồn, thiết lập còn lại mặc định. 2. Nghe tổng cộng 36 giờ — Tính cả hộp sạc; codec AAC, âm lượng 50%, tắt chống ồn. 3. Nghe thêm 2 giờ — Sạc 5 phút; hộp còn ít nhất 20%; AAC, âm lượng 50%, tắt chống ồn. | Khối pin và chú thích thử thời lượng; Chú thích sạc nhanh |
| [Galaxy Watch8](https://www.samsung.com/vn/watches/galaxy-watch/galaxy-watch8-44mm-silver-bluetooth-sm-l330nzsaxxv/) · [bổ sung](https://downloadcenter.samsung.com/content/UM/202507/20250730155623720/SM-L32X_L33X_L50X_UG_SEA_Android_Vie_Rev.1.1_250728.pdf) | 1. Pin tối đa 40 giờ — Tắt màn hình luôn hiển thị (AOD). 2. Pin tối đa 30 giờ — Bật AOD; câu hỏi về pin xác nhận cho cả bản 40 mm và 44 mm. 3. Kháng nước 5ATM — Bài thử để yên trong nước thường ở 50 m trong 10 phút theo ISO 22810:2010; không hiểu là cho phép lặn ở 50 m. | Thông số pin, AOD Off; Câu hỏi về dung lượng pin; PDF trang 149; bìa trang 1 có SM-L330 |
| [Xiaomi Watch S4](https://www.mi.com/vn/product/xiaomi-watch-s4/specs/) · [bổ sung](https://www.mi.com/vn/product/xiaomi-watch-s4/) | 1. Độ sáng HBM 1.500 nit — Toàn bộ màn hình sáng. 2. Độ sáng cực đại 2.200 nit — Chỉ một vùng màn hình sáng. 3. Pin tối đa 15 ngày — Bài thử dùng thông thường: mặt Rainbow; tắt theo dõi giấc ngủ chính xác cao, nhịp thở khi ngủ, căng thẳng và SpO2 cả ngày; đo nhịp tim mỗi 10 phút. Còn định mức thông báo, bật màn hình, gọi và tập luyện trong chú thích. | Mục màn hình và chú thích HBM; Khối màn hình và chú thích cách đo; Chú thích cuối trang về bài thử pin 15 ngày |

Chi tiết từng giá trị, điều kiện, URL, thời điểm kiểm và SHA-256 của nguồn: [kiem_tra_nguon_buoc4.json](kiem_tra_nguon_buoc4.json). Đã đọc lại 18 trang HTML và một hướng dẫn PDF. Mỗi mẫu có ba mục đạt tiêu chí chọn nguồn; đây không phải kết quả kiểm chứng quảng cáo.

### Những chỗ đã sửa sau khi kiểm lại

- **Galaxy S25 Ultra:** bỏ kích thước màn hình 6,9 inch vì T4.1 loại kích thước; dùng zoom kỹ thuật số 100x, đúng phạm vi zoom trong T4.5.
- **Galaxy Watch8:** bỏ yêu cầu chạy để kích hoạt vùng nhịp tim. Dùng chuẩn 5ATM trên trang sản phẩm, ghép với điều kiện thử ở hướng dẫn tiếng Việt trang 149. Bìa PDF có mã SM-L330, đúng bản Bluetooth 44 mm đã chọn.
- **Xiaomi 15T:** thay tần số lấy mẫu cảm ứng 2.560 Hz bằng tần số quét màn hình 120 Hz theo T4.5. Hai khái niệm này khác nhau. Bổ sung trang giới thiệu, chú thích 6, vì tần số quét còn phụ thuộc giao diện và thiết lập hình ảnh trò chơi.
- **OPPO Find X8:** điện áp 200–240 V thật sự có trong chú thích sạc. Tuy nhiên, để bám bảng thuộc tính hiện có, dùng độ sáng và kháng nước thay hai mức công suất sạc; không tự mở rộng cấu hình sạc từ mẫu kiểm tra.
- **AirPods Pro 3:** thêm Xuyên Âm, âm lượng 50% và hoạt động đi bộ cho mức 6,5 giờ. **Apple Watch SE 3:** thêm bối cảnh chạy bộ/không ghép đôi iPhone cho mức 7 giờ; hai mức 18/32 giờ dùng chung chú thích 8, không phải mỗi mức có một chú thích riêng.

### Chỗ nguồn còn mơ hồ hoặc không thống nhất

- **Galaxy Buds3 Pro:** bảng so sánh ghi tổng thời lượng 26 giờ khi bật ANC và 30 giờ khi tắt ANC. Trong phần thông số, dòng 30 giờ nằm dưới nhóm tắt ANC nhưng nhãn dòng lại ghi bật ANC; chú thích tổng 30 giờ cũng viết không rõ. Không dùng tổng 26/30 giờ làm một trong ba căn cứ chọn mẫu. Ba căn cứ đang dùng là thời lượng riêng tai nghe 6/7 giờ và IP57. Khi lưu nguồn phải giữ dấu vết chỗ mâu thuẫn này.
- **Galaxy S25 Ultra:** phần camera phân biệt zoom quang học 3x/5x với chất lượng quang học 2x/10x, nhưng một chú thích Space Zoom lại gọi 10x là quang học. Không lấy 10x làm căn cứ. Các chỗ đã đọc đều xác nhận 100x là kỹ thuật số.
- **Redmi Note 14 Pro+ 5G:** hãng nêu rõ hoạt động mạng xã hội và video trực tuyến, nhưng không công bố đủ âm lượng, độ sáng hay điều kiện mạng cho hai mức pin. Đủ để chọn nguồn theo điều kiện hoạt động; không được tự bổ sung các thiết lập hãng chưa nêu.


## Quy ước trong CSV

- `ma_mau`: mã theo T3.2. Tiền tố `dt`, `tn`, `dh` lần lượt chỉ điện thoại, tai nghe, đồng hồ.
- `nhom`: `dien_thoai`, `tai_nghe` hoặc `dong_ho`.
- `tap`: `phattrien` hoặc `kiemtra`.
- `mau_thu`: `co` chỉ hai mẫu thu thập thử đầu tiên; cả hai thuộc tập phát triển.
- `phien_ban`: giúp tránh trộn thông số giữa bản thường/Pro, có/không chống ồn, GPS/di động, kích thước đồng hồ hoặc thị trường. Điện thoại chưa cố định màu và dung lượng; nếu thông số phụ thuộc vào hai yếu tố này thì phải ghi rõ trong bằng chứng, không trộn giá trị.
- `dong_san_pham`: nhóm các biến thể gần nhau của cùng thế hệ. Ví dụ Xiaomi 15T và 15T Pro cùng dòng; Redmi Note 14 thuộc dòng khác. Nếu bổ sung biến thể về sau, phải dùng cùng mã dòng và cùng tập. Khác nhóm sản phẩm không được coi là cùng dòng chỉ vì cùng hãng.
- `ngay_truy_cap`: ngày kiểm tra nguồn, định dạng `YYYY-MM-DD`; không phải ngày lưu bản chụp trang.

## Giữ riêng tập kiểm tra

Từ ngày chia tập, mọi lựa chọn thiết kế chỉ dựa trên bốn mẫu phát triển: tệp cấu hình, ví dụ hướng dẫn, câu lệnh gửi LLM, quy tắc, ngưỡng và tham số. Không đưa nội dung tám mẫu kiểm tra vào ví dụ hướng dẫn hoặc dùng kết quả của chúng để chọn cách làm.

Ở Bước 4 đã đọc nguồn của tập kiểm tra để xác nhận đủ điều kiện chọn mẫu. Vì vậy không gọi tập này là hoàn toàn chưa từng được xem. Việc đọc chỉ phục vụ chọn nguồn; chưa sinh quảng cáo, tạo nhãn hay đánh giá phương pháp trên tám mẫu đó. Ở các bước tiếp theo, thu thập và gán nhãn theo quy trình đã chốt; không sửa quy trình theo lỗi của tập kiểm tra.

Nếu nguồn mất hoặc cần thay mẫu, ghi lý do và ngày vào nhật ký trước khi đánh giá, tăng phiên bản thẻ dữ liệu và kiểm lại số nhóm/hãng. Không thay mẫu vì phương pháp cho kết quả thấp. Sau khi xem kết quả kiểm tra, mọi sửa đổi phương pháp phải được báo cáo là sửa sau đánh giá.

## Trạng thái và giới hạn

Đã chọn mẫu, chia tập và kiểm tra nguồn. Chưa lưu bộ bằng chứng HTML/PDF/ảnh theo quy trình Bước 5–6; chưa có quảng cáo hoặc nhãn chuẩn nghiên cứu. Thẻ dữ liệu sẽ được bổ sung ở các bước sau và hoàn thiện ở Bước 45.

Mười hai mẫu là tập nhỏ được chọn có chủ đích. Kết quả trên tập này không đủ để kết luận cho mọi sản phẩm, mọi hãng hay mọi loại quảng cáo.

SHA-256 của CSV phiên bản 2 (chỉ thêm hai nguồn bổ sung, không đổi sản phẩm/tập):

```text
9f44937436f149d33ece3061a26061c916c94c731c48b448e3a302ac56ec278e
```

CSV phiên bản 1 trước khi thêm nguồn có SHA-256 `009bbb1d05784defd4581968fcc109738310d56484eb11740ea8c3e28bcc60cc`. Phiên bản 2 giữ nguyên toàn bộ mã mẫu, phiên bản sản phẩm và phân chia 4/8.
