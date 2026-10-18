# Thẻ dữ liệu Bước 4

| Thông tin | Giá trị |
|---|---|
| Ngày chọn mẫu và chia tập | **15/10/2026** |
| Phiên bản | **2**. Phiên bản này kiểm lại nguồn, không thay đổi 12 mẫu hoặc cách chia tập. |
| Danh sách chính | [mau_san_pham.csv](mau_san_pham.csv) |
| Quy mô | 12 mẫu: 4 mẫu phát triển và 8 mẫu kiểm tra |

## 1. Cách chia tập

### Mục đích của từng tập

- Tập phát triển gồm 4 mẫu, dùng để thử và sửa phương pháp, câu lệnh gửi LLM, quy tắc và tham số.
- Tập kiểm tra gồm 8 mẫu, chỉ dùng để đánh giá sau khi đã chốt phương pháp. Không dùng kết quả của tập này để sửa phương pháp rồi báo lại như một lần kiểm tra mới.

Việc chia tập được thực hiện có chủ đích theo kế hoạch T6.3, không chia ngẫu nhiên. Bốn mẫu phát triển được giữ theo đề xuất ban đầu. Tám mẫu còn lại được chọn sao cho tập kiểm tra có đủ nhóm sản phẩm và hãng. Tỷ lệ 4/8 phù hợp với quy mô khóa luận, không phải tỷ lệ bắt buộc cho các nghiên cứu khác.

### Thành phần hai tập

| Nhóm | Tập phát triển | Tập kiểm tra |
|---|---|---|
| Điện thoại | iPhone 17; Xiaomi 15T | OPPO Find X8; Galaxy S25 Ultra; Redmi Note 14 Pro+ 5G |
| Tai nghe | Galaxy Buds3 Pro | AirPods Pro 3; AirPods 4 bản thường; Redmi Buds 6 Pro |
| Đồng hồ | Apple Watch SE 3 GPS 44 mm | Galaxy Watch8 Bluetooth 44 mm; Xiaomi Watch S4 |
| **Tổng** | **4** | **8** |

Toàn bộ dữ liệu gồm 5 điện thoại, 4 tai nghe và 3 đồng hồ của bốn hãng: Apple, Samsung, Xiaomi và OPPO. Redmi được tính vào hãng Xiaomi. Cả hai tập đều có đủ ba nhóm sản phẩm; tập kiểm tra có đủ cả bốn hãng.

Hai mẫu dùng để thu thập thử ở Bước 5 là iPhone 17 và Galaxy Buds3 Pro.

## 2. Tiêu chí chọn nguồn

### Nguồn được chấp nhận

Mỗi mẫu phải đáp ứng đủ các điều kiện sau:

1. Nguồn là trang tiếng Việt do chính hãng công bố.
2. Nguồn có ít nhất ba thông số bằng số gắn với điều kiện sử dụng, cách đo hoặc cách thử.
3. Có thể ghi lại URL và ngày truy cập.

Trang hỗ trợ chính hãng có thông số tiếng Việt cũng được chấp nhận. Không dùng bài của cửa hàng, đánh giá của khách hàng hoặc bài tổng hợp để thay cho nguồn hãng.

### Cách dùng hai cột URL

- Cột `url` trỏ tới trang thông số hoặc trang sản phẩm có mục thông số.
- Cột `url_bo_sung` trỏ tới trang giới thiệu hoặc hướng dẫn sử dụng tiếng Việt của đúng mẫu do hãng phát hành, nếu điều kiện thử nằm ở đó.

Khi một mẫu có cả hai URL, phải đọc và lưu cả nguồn chính lẫn nguồn bổ sung. Ví dụ, trang sản phẩm Galaxy Watch8 ghi chuẩn 5ATM, còn hướng dẫn của đúng mã SM-L330 giải thích điều kiện thử ở trang 149.

### Phạm vi thông số

Chỉ tính các thuộc tính thuộc phạm vi T4.1/T4.5 của kế hoạch. Không tính:

- kích thước hoặc khối lượng;
- phiên bản Bluetooth;
- điều kiện chỉ dùng để bật một tính năng sức khỏe;
- câu chung như “kết quả thực tế có thể khác” nếu không có điều kiện cụ thể.

Nhiều mức của cùng một thuộc tính vẫn được tính riêng nếu mỗi mức có điều kiện khác nhau, chẳng hạn thời lượng pin khi bật và tắt chống ồn. Một thông số lặp lại ở nhiều vị trí chỉ được tính một lần.

Không tạo hoặc mở rộng cấu hình phương pháp dựa trên tập kiểm tra. Các thông số trong tài liệu này chỉ là dấu vết kiểm tra nguồn, chưa phải bộ tuyên bố hoặc nhãn chuẩn.

### Lưu ý khi đọc trang hãng

- AirPods 4 dùng trang hỗ trợ có mã cố định `121203`, đúng bản thường. Đường dẫn giới thiệu `/airpods-4/specs/` chuyển sang mẫu khác tại thời điểm kiểm tra nên không được dùng.
- Trang Samsung có thể chứa bảng so sánh nhiều mẫu và đánh giá của khách hàng. Khi thu thập, chỉ giữ đúng cột hoặc mục của mẫu đã chọn và bỏ phần đánh giá khách hàng.
- Một số trang Samsung vượt giới hạn dung lượng của công cụ duyệt. Các trang này đã được kiểm tra bằng cách đọc trực tiếp HTML.

## 3. Kết quả kiểm tra nguồn

Tất cả nguồn trong phần này được truy cập ngày **15/10/2026**. Các mô tả dưới đây được rút gọn để giúp tìm lại đúng mục. Khi thu thập bằng chứng, phải giữ đầy đủ chú thích và giới hạn do hãng công bố; không dùng phần rút gọn này thay cho bằng chứng gốc.

### Điện thoại

#### iPhone 17

Nguồn: [iPhone 17](https://www.apple.com/vn/iphone-17/specs/)

1. Độ sáng đỉnh 3.000 nit trong chế độ ngoài trời.
2. Kháng nước IP68 theo bài thử trong phòng thí nghiệm: độ sâu tối đa 6 m trong tối đa 30 phút. Mức này không được bảo đảm trong mọi tình huống sử dụng.
3. Sạc đến 50% trong 20 phút bằng cáp USB-C và bộ tiếp hợp từ 40 W, thử từ trạng thái pin cạn.

Vị trí đối chiếu: mục màn hình; mục chống nước và chú thích 3; mục pin/sạc và chú thích 6.

#### Xiaomi 15T

Nguồn: [Xiaomi 15T](https://www.mi.com/vn/product/xiaomi-15t/specs/) · [bổ sung](https://www.mi.com/vn/product/xiaomi-15t/)

1. Độ sáng cực đại 3.200 nit, đo trên 25% diện tích màn hình.
2. Tần số quét tối đa 120 Hz. Tần số thay đổi theo giao diện ứng dụng và chất lượng hình ảnh của trò chơi.
3. Kháng nước IP68 theo bài thử ngâm trong nước ngọt tĩnh ở độ sâu 3 m, tối đa 30 phút, chênh lệch nhiệt độ không quá 5 K.

Vị trí đối chiếu: mục màn hình; chú thích 6; mục chống bụi và nước.

#### OPPO Find X8

Nguồn: [OPPO Find X8](https://www.oppo.com/vn/smartphones/series-find-x/find-x8/specs/) · [bổ sung](https://www.oppo.com/vn/smartphones/series-find-x/find-x8/)

1. Độ sáng 800 nit ở chế độ thông thường mặc định.
2. Độ sáng 4.500 nit ở mức cực đại cục bộ, không phải mức sáng duy trì trên toàn màn hình.
3. Kháng nước IP68 theo bài thử trong nước tĩnh ở độ sâu 1,5 m trong 30 phút, chênh lệch nhiệt độ không quá 5 °C.

Vị trí đối chiếu: chú thích 13; chú thích 11.

#### Galaxy S25 Ultra

Nguồn: [Galaxy S25 Ultra](https://www.samsung.com/vn/smartphones/galaxy-s25-ultra/specs/) · [bổ sung](https://www.samsung.com/vn/smartphones/galaxy-s25-ultra/)

1. Xem video tối đa 31 giờ. Bài thử dùng video 720p lưu trên máy, tai nghe Bluetooth, thiết lập mặc định và mạng LTE.
2. Thu phóng tối đa 100x bằng kỹ thuật số, không phải zoom quang học 100x.
3. Kháng nước IP68 theo bài thử ngâm trong nước ngọt ở độ sâu tối đa 1,5 m trong tối đa 30 phút.

Vị trí đối chiếu: mục pin và chú thích thử phát lại video; câu hỏi về zoom 100x; chú thích thử kháng nước.

#### Redmi Note 14 Pro+ 5G

Nguồn: [Redmi Note 14 Pro+ 5G](https://www.mi.com/vn/product/redmi-note-14-pro-plus-5g/specs/) · [bổ sung](https://www.mi.com/vn/product/redmi-note-14-pro-plus-5g/)

1. Pin 19,5 giờ khi dùng mạng xã hội, theo thử nghiệm nội bộ của hãng. Hãng không công bố đầy đủ thiết lập của bài thử.
2. Pin 9 giờ khi xem video trực tuyến, theo thử nghiệm nội bộ của hãng. Hãng không công bố đầy đủ thiết lập của bài thử.
3. Kháng nước IP68 theo bài thử trong nước ngọt tĩnh ở độ sâu 1,5 m, tối đa 30 phút, chênh lệch nhiệt độ không quá 5 K.

Vị trí đối chiếu: khối pin có số 19,5 giờ và hoạt động tương ứng; khối pin có số 9 giờ và hoạt động tương ứng; mục chống bụi và nước.

### Tai nghe

#### Galaxy Buds3 Pro

Nguồn: [Galaxy Buds3 Pro](https://www.samsung.com/vn/audio-sound/galaxy-buds/galaxy-buds3-pro-silver-sm-r630nzaaxxv/)

1. Nghe nhạc tối đa 7 giờ bằng riêng tai nghe khi tắt chống ồn chủ động.
2. Nghe nhạc tối đa 6 giờ bằng riêng tai nghe khi bật chống ồn chủ động.
3. Tai nghe đạt IP57 theo bài thử với nước ngọt ở độ sâu 1 m trong tối đa 30 phút. Hộp sạc không kháng nước.

Vị trí đối chiếu: mục thời lượng sử dụng khi tắt ANC; mục thời lượng sử dụng khi bật ANC; chú thích IP57.

#### AirPods Pro 3

Nguồn: [AirPods Pro 3](https://www.apple.com/vn/airpods-pro/specs/)

1. Nghe tối đa 8 giờ sau một lần sạc khi bật chống ồn, đặt âm lượng ở 50% và dùng nội dung AAC 256 Kbps.
2. Nghe tối đa 7,5 giờ khi bật thêm âm thanh không gian và theo dõi chuyển động đầu trong bài thử của chú thích 13.
3. Nghe tối đa 6,5 giờ khi bật cảm biến nhịp tim và Xuyên Âm, đặt âm lượng ở 50%, đi bộ ngoài trời và nghe nhạc từ iPhone.

Vị trí đối chiếu: mục pin và chú thích 13; mục pin và chú thích 14.

#### AirPods 4

Nguồn: [AirPods 4](https://support.apple.com/vi-vn/121203)

1. Nghe tối đa 5 giờ sau một lần sạc. Bài thử dùng tai nghe bản thường, âm lượng 50%, tắt âm thanh không gian và nội dung AAC 256 Kbps.
2. Nghe tổng cộng tối đa 30 giờ khi tính cả các lần sạc lại bằng hộp. Bài thử dùng cùng thiết lập âm thanh và kéo dài đến khi cả tai nghe lẫn hộp cạn pin.
3. Sạc tai nghe đang cạn pin trong hộp 5 phút để nghe thêm khoảng 1 giờ, với âm lượng 50% và âm thanh không gian đã tắt.

Vị trí đối chiếu: mục pin và chú thích 9; mục pin và chú thích 10; mục pin và chú thích 11.

#### Redmi Buds 6 Pro

Nguồn: [Redmi Buds 6 Pro](https://www.mi.com/vn/product/redmi-buds-6-pro/specs/) · [bổ sung](https://www.mi.com/vn/product/redmi-buds-6-pro/)

1. Nghe 9,5 giờ sau một lần sạc đầy, dùng codec AAC, âm lượng 50%, tắt chống ồn và giữ các thiết lập khác ở mặc định.
2. Nghe tổng cộng 36 giờ khi tính cả hộp sạc, dùng codec AAC, âm lượng 50% và tắt chống ồn.
3. Sạc 5 phút để nghe thêm 2 giờ khi hộp còn ít nhất 20%, dùng AAC, âm lượng 50% và tắt chống ồn.

Vị trí đối chiếu: khối pin và chú thích thử thời lượng; chú thích sạc nhanh.

### Đồng hồ

#### Apple Watch SE 3

Nguồn: [Apple Watch SE 3](https://www.apple.com/vn/apple-watch-se-3/specs/)

1. Pin tối đa 18 giờ khi dùng bình thường theo bài thử của Apple. Bản GPS kết nối với iPhone qua Bluetooth trong suốt 18 giờ.
2. Pin tối đa 32 giờ khi bật chế độ nguồn điện thấp. Bài thử có 6 giờ theo dõi giấc ngủ; bản GPS kết nối với iPhone qua Bluetooth.
3. Pin tối đa 7 giờ khi chạy bộ ngoài trời, không ghép đôi với iPhone và bật cảm biến nhịp tim.

Vị trí đối chiếu: mục pin và chú thích 8; mục pin và chú thích 9.

#### Galaxy Watch8

Nguồn: [Galaxy Watch8](https://www.samsung.com/vn/watches/galaxy-watch/galaxy-watch8-44mm-silver-bluetooth-sm-l330nzsaxxv/) · [bổ sung](https://downloadcenter.samsung.com/content/UM/202507/20250730155623720/SM-L32X_L33X_L50X_UG_SEA_Android_Vie_Rev.1.1_250728.pdf)

1. Pin tối đa 40 giờ khi tắt màn hình luôn hiển thị (AOD).
2. Pin tối đa 30 giờ khi bật AOD. Phần câu hỏi về pin xác nhận số liệu này cho cả bản 40 mm và 44 mm.
3. Kháng nước 5ATM theo bài thử để yên trong nước thường ở độ sâu 50 m trong 10 phút, theo ISO 22810:2010. Điều này không có nghĩa là đồng hồ dùng được để lặn ở độ sâu 50 m.

Vị trí đối chiếu: thông số pin, AOD Off; câu hỏi về dung lượng pin; trang 149 của PDF; bìa trang 1 có mã SM-L330.

#### Xiaomi Watch S4

Nguồn: [Xiaomi Watch S4](https://www.mi.com/vn/product/xiaomi-watch-s4/specs/) · [bổ sung](https://www.mi.com/vn/product/xiaomi-watch-s4/)

1. Độ sáng HBM 1.500 nit khi toàn bộ màn hình sáng.
2. Độ sáng cực đại 2.200 nit khi chỉ một vùng màn hình sáng.
3. Pin tối đa 15 ngày theo bài thử sử dụng thông thường: dùng mặt Rainbow; tắt theo dõi giấc ngủ chính xác cao, nhịp thở khi ngủ, căng thẳng và SpO2 cả ngày; đo nhịp tim mỗi 10 phút. Chú thích còn nêu định mức thông báo, số lần bật màn hình, cuộc gọi và thời gian tập luyện.

Vị trí đối chiếu: mục màn hình và chú thích HBM; khối màn hình và chú thích cách đo; chú thích cuối trang về bài thử pin 15 ngày.

### Dấu vết kiểm tra đầy đủ

Chi tiết của từng giá trị, điều kiện, URL, thời điểm kiểm tra và SHA-256 của nguồn được lưu tại [kiem_tra_nguon_buoc4.json](kiem_tra_nguon_buoc4.json).

Quá trình kiểm tra đã đọc lại 18 trang HTML và một hướng dẫn PDF. Mỗi mẫu có ba mục đạt tiêu chí chọn nguồn. Kết quả này chỉ xác nhận nguồn phù hợp, chưa phải kết quả kiểm chứng quảng cáo.

## 4. Các thay đổi sau khi kiểm lại nguồn

- **Galaxy S25 Ultra:** bỏ kích thước màn hình 6,9 inch vì T4.1 loại kích thước. Thay bằng zoom kỹ thuật số 100x, thuộc phạm vi zoom trong T4.5.
- **Galaxy Watch8:** bỏ yêu cầu chạy để kích hoạt vùng nhịp tim. Dùng chuẩn 5ATM trên trang sản phẩm và điều kiện thử tại trang 149 của hướng dẫn tiếng Việt. Bìa PDF có mã SM-L330, đúng bản Bluetooth 44 mm đã chọn.
- **Xiaomi 15T:** thay tần số lấy mẫu cảm ứng 2.560 Hz bằng tần số quét màn hình 120 Hz theo T4.5. Đây là hai khái niệm khác nhau. Trang giới thiệu và chú thích 6 được thêm vì tần số quét còn phụ thuộc giao diện và thiết lập hình ảnh của trò chơi.
- **OPPO Find X8:** điện áp 200–240 V có trong chú thích sạc. Để bám theo bảng thuộc tính hiện có, thẻ dữ liệu dùng độ sáng và kháng nước thay cho hai mức công suất sạc; không mở rộng cấu hình sạc từ mẫu kiểm tra.
- **AirPods Pro 3:** bổ sung Xuyên Âm, âm lượng 50% và hoạt động đi bộ cho mức 6,5 giờ.
- **Apple Watch SE 3:** bổ sung bối cảnh chạy bộ và không ghép đôi iPhone cho mức 7 giờ. Hai mức 18 và 32 giờ cùng dùng chú thích 8, không có chú thích riêng cho từng mức.

## 5. Những điểm nguồn còn mơ hồ hoặc không thống nhất

### Galaxy Buds3 Pro

Bảng so sánh ghi tổng thời lượng 26 giờ khi bật ANC và 30 giờ khi tắt ANC. Trong phần thông số, dòng 30 giờ nằm dưới nhóm tắt ANC nhưng nhãn dòng lại ghi bật ANC; chú thích tổng 30 giờ cũng không rõ. Vì vậy, tổng thời lượng 26/30 giờ không được dùng làm căn cứ chọn mẫu.

Ba căn cứ đang dùng là thời lượng riêng của tai nghe ở mức 6 và 7 giờ, cùng chuẩn IP57. Khi lưu nguồn, phải giữ dấu vết của chỗ mâu thuẫn này.

### Galaxy S25 Ultra

Phần camera phân biệt zoom quang học 3x/5x với chất lượng quang học 2x/10x, nhưng một chú thích Space Zoom lại gọi 10x là quang học. Mức 10x không được dùng làm căn cứ. Các vị trí đã đọc đều xác nhận 100x là kỹ thuật số.

### Redmi Note 14 Pro+ 5G

Hãng nêu rõ hai hoạt động là dùng mạng xã hội và xem video trực tuyến, nhưng không công bố đầy đủ âm lượng, độ sáng hoặc điều kiện mạng cho hai mức pin. Thông tin hiện có đủ để chọn nguồn theo điều kiện hoạt động. Không tự bổ sung các thiết lập mà hãng chưa nêu.

## 6. Quy ước trong CSV

| Cột | Ý nghĩa |
|---|---|
| `ma_mau` | Mã theo T3.2. Các tiền tố `dt`, `tn`, `dh` lần lượt chỉ điện thoại, tai nghe và đồng hồ. |
| `nhom` | Nhận một trong ba giá trị: `dien_thoai`, `tai_nghe` hoặc `dong_ho`. |
| `tap` | Nhận giá trị `phattrien` hoặc `kiemtra`. |
| `mau_thu` | Giá trị `co` chỉ hai mẫu thu thập thử đầu tiên. Cả hai đều thuộc tập phát triển. |
| `phien_ban` | Dùng để tránh trộn thông số giữa bản thường/Pro, có/không chống ồn, GPS/di động, kích thước đồng hồ hoặc thị trường. Điện thoại chưa cố định màu và dung lượng. Nếu thông số phụ thuộc vào hai yếu tố này, bằng chứng phải ghi rõ và không được trộn giá trị. |
| `dong_san_pham` | Nhóm các biến thể gần nhau của cùng một thế hệ. Ví dụ, Xiaomi 15T và 15T Pro cùng dòng; Redmi Note 14 thuộc dòng khác. Nếu bổ sung biến thể, phải dùng cùng mã dòng và cùng tập. Các sản phẩm khác nhóm không được coi là cùng dòng chỉ vì cùng hãng. |
| `ngay_truy_cap` | Ngày kiểm tra nguồn theo định dạng `YYYY-MM-DD`, không phải ngày lưu bản chụp trang. |

## 7. Quy tắc giữ riêng tập kiểm tra

Từ ngày chia tập, mọi lựa chọn thiết kế chỉ được dựa trên bốn mẫu phát triển. Quy tắc này áp dụng cho tệp cấu hình, ví dụ hướng dẫn, câu lệnh gửi LLM, quy tắc, ngưỡng và tham số. Không đưa nội dung của tám mẫu kiểm tra vào ví dụ hướng dẫn hoặc dùng kết quả của chúng để chọn cách làm.

Ở Bước 4, nguồn của tập kiểm tra đã được đọc để xác nhận các mẫu đủ điều kiện. Vì vậy, tập này không hoàn toàn chưa từng được xem. Việc đọc nguồn chỉ phục vụ chọn mẫu; chưa sinh quảng cáo, tạo nhãn hoặc đánh giá phương pháp trên tám mẫu kiểm tra.

Ở các bước tiếp theo, việc thu thập và gán nhãn phải tuân theo quy trình đã chốt. Không sửa quy trình theo lỗi quan sát được trên tập kiểm tra.

Nếu nguồn mất hoặc cần thay mẫu, phải ghi lý do và ngày vào nhật ký trước khi đánh giá, tăng phiên bản thẻ dữ liệu, rồi kiểm lại số nhóm và hãng. Không thay mẫu vì phương pháp cho kết quả thấp. Mọi thay đổi phương pháp sau khi xem kết quả kiểm tra phải được báo cáo là sửa sau đánh giá.

## 8. Trạng thái và giới hạn

Đã hoàn thành việc chọn mẫu, chia tập và kiểm tra nguồn. Chưa lưu bộ bằng chứng HTML/PDF/ảnh theo quy trình Bước 5–6; chưa có quảng cáo hoặc nhãn chuẩn nghiên cứu. Thẻ dữ liệu sẽ được bổ sung trong các bước sau và hoàn thiện ở Bước 45.

Tập dữ liệu chỉ có 12 mẫu và được chọn có chủ đích. Kết quả trên tập này không đủ để kết luận cho mọi sản phẩm, hãng hoặc loại quảng cáo.

## 9. Phiên bản và mã kiểm tra

SHA-256 của CSV phiên bản 2, sau khi thêm hai nguồn bổ sung nhưng không đổi sản phẩm hoặc cách chia tập:

```text
9f44937436f149d33ece3061a26061c916c94c731c48b448e3a302ac56ec278e
```

CSV phiên bản 1, trước khi thêm nguồn, có SHA-256 `009bbb1d05784defd4581968fcc109738310d56484eb11740ea8c3e28bcc60cc`.

Phiên bản 2 giữ nguyên toàn bộ mã mẫu, phiên bản sản phẩm và cách chia 4/8.
