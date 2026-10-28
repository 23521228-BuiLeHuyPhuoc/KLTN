# Khảo sát cách hiểu của người đọc (Bước 10)

**Trạng thái:** phiếu bản 2 ngày 27/10/2026 (sửa cho người không rành công nghệ, thêm phương án), câu quảng cáo lấy từ bài do CopyPro tạo. Đã thu 10 phiếu (mục 7) và chốt cách xử lý ngày 28/10 (mục 8).

## 1. Để làm gì

Tệp cấu hình ghi cách hiểu khi quảng cáo không nêu điều kiện, ví dụ "tai nghe pin 6 giờ" thì hiểu là nghe nhạc, chống ồn bật, chỉ tính tai nghe. Các cách hiểu này do người làm đề tài đặt ra ở Bước 8. Khảo sát hỏi người đọc thật để xác nhận hoặc sửa, theo [T4.5](../CHI_TIET_TUYEN_TINH_KHOA_LUAN.md#t4-5) và điểm 1 của [T10](../CHI_TIET_TUYEN_TINH_KHOA_LUAN.md#t10). Đề cương (cả bản đã nộp và bản cuối) ghi việc này là "khảo sát nhanh cách hiểu của 5–10 người đọc"; kế hoạch nâng lên 20–30 người ngày 26/10.

## 2. Câu quảng cáo lấy từ đâu

- **Nguồn:** 18 bài do CopyPro tạo ngày 27/10/2026, lưu ở `ket_qua/khao_sat_quang_cao_goc.jsonl` (câu lệnh, tham số, mã bài trên CopyPro, nội dung, số token). Gọi API `POST /api/contents/generate` của backend CopyPro chạy ở máy, tài khoản demo gói Pro. Câu lệnh ghép y như `buildPrompt()` của giao diện; với cả 18 bài, trường `prompt` CopyPro lưu trùng từng ký tự với câu lệnh đã gửi.
- **Thiết lập:** theo [T3.3](../CHI_TIET_TUYEN_TINH_KHOA_LUAN.md#t3-3): ngành Công nghệ, giọng Chuyên nghiệp, độ dài vừa (1.800 token), 1 phiên bản; từ khóa và đối tượng để trống. 3 mẫu tập phát triển (iPhone 17, Galaxy Buds3 Pro, Apple Watch SE 3) × 3 loại bài (mô tả sản phẩm, bài mạng xã hội, landing page) × 2 chế độ (`ten`: chỉ nhập tên; `ten_thong_so`: nhập thêm đoạn thông số chính hãng vào ô "Thông tin bổ sung").
- **Mô hình:** Gemini 2.5 Flash (`gemini-flash`), mô hình duy nhất trong danh sách của CopyPro còn chạy được. Hai mô hình của đề tài (Gemini 3.6 Flash, GPT-OSS 120B) chưa được thêm vào CopyPro (việc của Bước 11). Phiếu chỉ cần câu quảng cáo như LLM viết, nên khác mô hình không ảnh hưởng mục đích khảo sát.
- **Câu dùng được:** 9 bài chế độ `ten` gần như không có con số. Các bài chế độ `ten_thong_so` có con số nhưng thường chép luôn điều kiện ("3000 nit khi ở ngoài trời", "6 giờ (bật ANC)"). Chỉ 3 câu nêu con số mà thiếu điều kiện cần hỏi; 3 câu này dùng nguyên văn cho Q08, Q09, Q13, Q14. Các câu còn lại lấy câu thật rồi **chỉ xóa chữ**: xóa phần điều kiện cần hỏi và các vế nói về thông số khác, không thêm hay đổi chữ nào. Bảng ở mục 5 ghi câu gốc và phần đã bỏ.
- **Dòng "Thông tin thêm":** 5 đoạn có thêm một dòng do người làm đề tài viết, giải thích từ khó (chống ồn, chế độ tiết kiệm pin, nit, thu phóng) và cho biết tai nghe có hộp sạc. Dòng này chỉ nói tính năng có tồn tại và người dùng tự bật tắt được, không nói con số đo ở điều kiện nào, cũng không nói hãng để mặc định thế nào. Việc nhắc tới hộp sạc có thể làm nhiều người nghĩ tới hộp sạc hơn ở Q04; ghi vào giới hạn khi viết khóa luận.

## 3. Cách gửi phiếu

- **Công cụ:** Google Forms, tạo bằng `ket_qua/tao_google_form.gs` (Google Apps Script sinh từ mục 4, nên form khớp từng chữ với phiếu). Hàm `taoPhieu` tạo form mới; hàm `capNhatPhieu` ghi đè form đã tạo, giữ nguyên đường dẫn, và dừng nếu form đã có câu trả lời. Không thu email, không xáo trộn câu. Mọi câu đều bắt buộc. Câu trắc nghiệm có thêm ô "Khác" để người đọc tự ghi.
- **Form:** đường dẫn `https://docs.google.com/forms/d/e/1FAIpQLSfJ_oUJVXZLy0blgcaaJyaLvqR3FI_dXa5ZCuQHiRLs7mYCiQ/viewform` là form bản 1, không dùng. Phiếu được thu bằng một form khác tạo từ bản 2; bảng câu trả lời ở Google Sheets `1a8M03Vuq1UEfLhUUHu0KIXIZCKdgkG5IvloVvyUW4lk`.
- **Người trả lời:** 20–30 người từ 18 tuổi, ưu tiên người không học hay làm công nghệ thông tin. Gửi qua Zalo hoặc Facebook cho người quen và nhờ chuyển tiếp. Ghi lại đã gửi qua kênh nào. Đề cương chỉ yêu cầu 5–10 người; dưới 20 người thì vẫn dùng được nhưng phải ghi rõ khoảng tin cậy rộng.
- **Không gợi ý:** chỉ gửi đường dẫn kèm lời mở đầu của phiếu. Không giải thích thêm, không nói "đáp án" trước khi người đó nộp.
- **Thứ tự câu cố định** như mục 4. Câu Q15 nằm ở trang riêng sau Q01–Q14, để người đọc trả lời Q07 ("18 giờ") trước khi thấy câu có chữ "lên đến".
- **Trên form, câu đánh số "Câu 1" đến "Câu 18":** Câu 1–15 là Q01–Q15, Câu 16–18 là D1–D3.
- **Khi đủ phiếu:** trong Google Forms chọn Câu trả lời, tải tệp CSV, lưu vào `ket_qua/khao_sat_cach_hieu.csv`. Tệp không có thông tin cá nhân nên được đưa vào repo.

## 4. Phiếu (sinh form từ mục này)

Mỗi đoạn trích là một khung tiêu đề trên form (`####`), dòng `>` là phần mô tả của khung. Câu hỏi bên dưới chỉ hỏi một ý. Phương án "Khác: ..." là ô tự ghi của Google Forms.

**Tiêu đề:** Bạn hiểu quảng cáo điện thoại, tai nghe, đồng hồ như thế nào?

**Mô tả:** Phiếu này phục vụ khóa luận tốt nghiệp về quảng cáo thiết bị điện tử. Bạn sẽ đọc 10 đoạn trích ngắn từ quảng cáo, mỗi đoạn có 1 đến 3 câu hỏi. Hãy chọn theo cảm nhận đầu tiên khi đọc, không cần tra cứu. Không có đáp án đúng hay sai. Nếu không phương án nào giống ý bạn, hãy ghi vào ô "Khác". Phiếu ẩn danh, không thu tên hay email, mất khoảng 6 phút. Phiếu dành cho người từ 18 tuổi.

### Trang 1

#### Đoạn 1: điện thoại iPhone 17
> "Luôn sẵn sàng cho mọi hành trình với thời lượng pin ấn tượng, lên đến 30 giờ."

**Q01.** Theo bạn, 30 giờ pin này là khi dùng điện thoại vào việc gì?
- Xem video đã tải sẵn trong máy
- Xem video trực tuyến (YouTube, Netflix...)
- Chơi game, dùng nặng
- Dùng hằng ngày, nhiều việc lẫn lộn (nhắn tin, lướt web, gọi điện...)
- Không biết / không chắc
- Khác: ...

#### Đoạn 2: tai nghe Galaxy Buds3 Pro
> "Tận hưởng thời gian sử dụng vượt trội: lên đến 6 giờ."
> Thông tin thêm: tai nghe này có tính năng chống ồn (tự lọc bớt tiếng ồn xung quanh, gọi tắt là ANC), người dùng tự bật hoặc tắt. Tai nghe đi kèm một hộp sạc: cất tai nghe vào hộp thì tai nghe được sạc lại.

**Q02.** Theo bạn, 6 giờ này là khi dùng tai nghe vào việc gì?
- Nghe nhạc, xem phim
- Gọi điện
- Dùng lẫn lộn, lúc nghe nhạc lúc gọi điện
- Không biết / không chắc
- Khác: ...

**Q03.** Theo bạn, trong 6 giờ đó tính năng chống ồn đang bật hay tắt?
- Bật suốt
- Tắt suốt
- Lúc bật lúc tắt
- Không biết / không chắc
- Khác: ...

**Q04.** Theo bạn, 6 giờ này được tính thế nào?
- Chỉ tính tai nghe: sạc đầy tai nghe một lần, nghe liên tục được 6 giờ
- Tính cả hộp sạc: hết pin thì cất tai nghe vào hộp sạc lại rồi nghe tiếp, cộng lại được 6 giờ
- Không biết / không chắc
- Khác: ...

#### Đoạn 3: đồng hồ Apple Watch SE 3
> "Tận hưởng trải nghiệm liền mạch với thời lượng pin ấn tượng: 18 giờ."
> Thông tin thêm: đồng hồ này có chế độ tiết kiệm pin (tắt bớt một số tính năng để pin dùng lâu hơn), người dùng tự bật hoặc tắt.

**Q05.** Theo bạn, 18 giờ này là khi dùng đồng hồ thế nào?
- Dùng bình thường hằng ngày: xem giờ, nhận thông báo, đo nhịp tim
- Dùng bình thường, có lúc tập thể dục một chút
- Tập thể thao liên tục suốt 18 giờ (ví dụ chạy bộ có bật định vị GPS)
- Không biết / không chắc
- Khác: ...

**Q06.** Theo bạn, trong 18 giờ đó đồng hồ đang ở chế độ nào?
- Chế độ bình thường, đủ tính năng
- Chế độ tiết kiệm pin
- Lúc bình thường, lúc tiết kiệm pin
- Không biết / không chắc
- Khác: ...

**Q07.** Theo bạn, con số 18 giờ nghĩa là gì?
- Dùng thường xuyên sẽ được khoảng 18 giờ
- 18 giờ là mức tốt nhất, dùng thực tế thường ít hơn
- Chắc chắn dùng được ít nhất 18 giờ, có khi còn hơn
- Không biết / không chắc
- Khác: ...

#### Đoạn 4: điện thoại iPhone 17
> "Luôn sẵn sàng cho mọi hành trình với thời lượng pin ấn tượng, xem video lên đến 30 giờ và khả năng sạc nhanh 50% chỉ trong 20 phút."

**Q08.** Theo bạn, cần gì để sạc được 50% pin trong 20 phút?
- Dùng đồ đi kèm khi mua máy là đủ, không phải mua thêm gì
- Dùng củ sạc nào cũng được, kể cả củ sạc cũ ở nhà
- Phải có củ sạc loại mạnh (công suất cao), thường phải mua riêng
- Không biết / không chắc
- Khác: ...

**Q09.** Theo bạn, "xem video" ở đây là xem thế nào?
- Xem video đã tải sẵn trong máy
- Xem video trực tuyến (YouTube, Netflix...)
- Cả hai, không phân biệt
- Không biết / không chắc
- Khác: ...

#### Đoạn 5: điện thoại iPhone 17
> "Với độ sáng 3000 nit, mọi nội dung từ phim ảnh đến ảnh chụp đều rực rỡ và sắc nét."
> Thông tin thêm: nit là đơn vị đo độ sáng màn hình, số càng lớn màn hình càng sáng.

**Q10.** Theo bạn, màn hình sáng được 3000 nit khi nào?
- Khi dùng bình thường, lúc nào cũng sáng được như vậy
- Khi ra ngoài trời nắng (máy tự tăng độ sáng)
- Khi xem phim hoặc ảnh loại HDR (loại hình ảnh có vùng sáng rất sáng)
- Đây là mức sáng nhất máy có thể đạt, không rõ lúc nào
- Không biết / không chắc
- Khác: ...

#### Đoạn 6: đồng hồ Apple Watch SE 3
> "Tận hưởng trải nghiệm liền mạch với thời lượng pin ấn tượng: kéo dài tới 32 giờ."
> Thông tin thêm: đồng hồ này có chế độ tiết kiệm pin (tắt bớt một số tính năng để pin dùng lâu hơn), người dùng tự bật hoặc tắt.

**Q11.** Theo bạn, trong 32 giờ đó đồng hồ đang ở chế độ nào?
- Chế độ bình thường, đủ tính năng
- Chế độ tiết kiệm pin
- Lúc bình thường, lúc tiết kiệm pin
- Không biết / không chắc
- Khác: ...

#### Đoạn 7: điện thoại iPhone 17
> "Ghi lại mọi khoảnh khắc đáng giá với hệ thống camera đa năng, cho phép bạn thu phóng lên đến 10x, đảm bảo mọi chi tiết đều được nắm bắt hoàn hảo."
> Thông tin thêm: thu phóng (zoom) là phóng to cảnh ở xa khi chụp ảnh.

**Q12.** Theo bạn, thu phóng 10x ở đây là gì?
- Phóng to 10 lần bằng ống kính, ảnh vẫn nét như chụp thường
- Phóng to 10 lần bằng phần mềm, ảnh có thể mờ hoặc vỡ hạt
- Kết hợp: một phần bằng ống kính, phần còn lại bằng phần mềm
- Không biết / không chắc
- Khác: ...

#### Đoạn 8: tai nghe Galaxy Buds3 Pro
> "Các cuộc trò chuyện cũng trở nên rõ ràng hơn bao giờ hết với thời lượng đàm thoại lên đến 5 giờ."
> Thông tin thêm: tai nghe này có tính năng chống ồn (tự lọc bớt tiếng ồn xung quanh, gọi tắt là ANC), người dùng tự bật hoặc tắt.

**Q13.** Theo bạn, trong 5 giờ gọi điện đó tính năng chống ồn đang bật hay tắt?
- Bật suốt
- Tắt suốt
- Lúc bật lúc tắt
- Không biết / không chắc
- Khác: ...

#### Đoạn 9: đồng hồ Apple Watch SE 3
> "Khả năng sạc nhanh vượt trội giúp bạn quay lại hoạt động chỉ trong tích tắc, với 80% pin chỉ trong khoảng 45 phút, hoặc 15 phút sạc cho 8 giờ sử dụng."

**Q14.** Theo bạn, cần gì để sạc được 80% pin trong khoảng 45 phút?
- Dùng đồ đi kèm khi mua đồng hồ là đủ, không phải mua thêm gì
- Dùng củ sạc nào cũng được, kể cả củ sạc cũ ở nhà
- Phải có củ sạc loại mạnh (công suất cao), thường phải mua riêng
- Không biết / không chắc
- Khác: ...

### Trang 2

#### Đoạn 10: đồng hồ Apple Watch SE 3
> "Tận hưởng trải nghiệm liền mạch với thời lượng pin ấn tượng: lên đến 18 giờ."

**Q15.** Theo bạn, con số 18 giờ nghĩa là gì?
- Dùng thường xuyên sẽ được khoảng 18 giờ
- 18 giờ là mức tốt nhất, dùng thực tế thường ít hơn
- Chắc chắn dùng được ít nhất 18 giờ, có khi còn hơn
- Không biết / không chắc
- Khác: ...

### Trang 3: về bạn

**D1.** Bạn bao nhiêu tuổi? 18–24 · 25–34 · 35–49 · Từ 50 trở lên

**D2.** Bạn có học hoặc làm trong ngành công nghệ thông tin không? Có · Không

**D3.** Trong 2 năm qua, bạn có mua điện thoại, tai nghe không dây hoặc đồng hồ thông minh không? Có · Không

## 5. Câu gốc và phần đã bỏ

Ba bài nguồn, đều là bài mạng xã hội ở chế độ `ten_thong_so`: iPhone 17 (dòng 11 của tệp JSONL, mã bài `6ae06c1f54393a9c38fa7ecd`), Galaxy Buds3 Pro (dòng 14, `6ae06c6654393a9c38fa7f69`), Apple Watch SE 3 (dòng 17, `6ae06ca154393a9c38fa8005`).

| Đoạn | Câu gốc trong bài | Phần đã bỏ | Lý do bỏ |
|---|---|---|---|
| 1 (Q01) | "Luôn sẵn sàng cho mọi hành trình với thời lượng pin ấn tượng, xem video lên đến 30 giờ và khả năng sạc nhanh 50% chỉ trong 20 phút." | "xem video"; vế "và khả năng sạc nhanh..." | Câu hỏi về hoạt động; vế sạc hỏi riêng ở Q08 |
| 2 (Q02–Q04) | "Tận hưởng thời gian sử dụng vượt trội: lên đến 7 giờ (tắt ANC) hoặc 6 giờ (bật ANC) chỉ với một lần sạc tai nghe, và tổng cộng đến 30 giờ cùng hộp sạc (khi tắt ANC)." | "7 giờ (tắt ANC) hoặc"; "(bật ANC)"; "chỉ với một lần sạc tai nghe"; vế hộp sạc | Ba câu hỏi về hoạt động, chống ồn, bộ phận |
| 3 (Q05–Q07) | "Tận hưởng trải nghiệm liền mạch với thời lượng pin ấn tượng: lên đến 18 giờ sử dụng bình thường và kéo dài tới 32 giờ ở Chế Độ Nguồn Điện Thấp." | "lên đến"; "sử dụng bình thường"; vế 32 giờ | Hỏi hoạt động, chế độ nguồn; bỏ "lên đến" để so với Q15 |
| 4 (Q08, Q09) | Như đoạn 1 | Không bỏ gì | |
| 5 (Q10) | "Với độ sáng đỉnh 3000 nit khi ở ngoài trời, mọi nội dung từ phim ảnh đến ảnh chụp đều rực rỡ và sắc nét, bất kể điều kiện ánh sáng." | "đỉnh"; "khi ở ngoài trời"; "bất kể điều kiện ánh sáng" | Hỏi chế độ hiển thị. "Đỉnh" trên trang Apple trỏ hai chế độ (V47). Vế "bất kể điều kiện ánh sáng" gợi ý sẵn là mọi lúc |
| 6 (Q11) | Như đoạn 3 | Vế 18 giờ; "ở Chế Độ Nguồn Điện Thấp" | Hỏi chế độ nguồn |
| 7 (Q12) | "Ghi lại mọi khoảnh khắc đáng giá với hệ thống camera đa năng, cho phép bạn thu phóng quang học 4x và kỹ thuật số lên đến 10x, đảm bảo mọi chi tiết đều được nắm bắt hoàn hảo." | "quang học 4x và kỹ thuật số" | Hỏi loại zoom |
| 8 (Q13) | "Các cuộc trò chuyện cũng trở nên rõ ràng hơn bao giờ hết với thời lượng đàm thoại lên đến 5 giờ." | Không bỏ gì | |
| 9 (Q14) | "Khả năng sạc nhanh vượt trội giúp bạn quay lại hoạt động chỉ trong tích tắc, với 80% pin chỉ trong khoảng 45 phút, hoặc 15 phút sạc cho 8 giờ sử dụng." | Không bỏ gì | |
| 10 (Q15) | Như đoạn 3 | "sử dụng bình thường"; vế 32 giờ | Giữ "lên đến" như câu gốc |

## 6. Tiêu chí chấm, đặt trước khi có kết quả

Mục này viết trước khi gửi phiếu, để kết quả không làm đổi cách chấm. Mỗi phương án của mỗi câu được xếp sẵn vào "khớp cấu hình" hoặc "hiểu khác".

**Quy tắc chung (theo Bước 10):** khi số người chọn phương án "hiểu khác" vượt quá một nửa tổng số phiếu thì sửa cấu hình, hướng dẫn gán nhãn và các ví dụ liên quan.

- "Không biết / không chắc" không tính là hiểu khác.
- Câu tự ghi ở ô "Khác" được xếp vào phương án gần nhất; câu không xếp được thì tính như "Không biết". Cách xếp từng câu ghi ở mục 7.
- Báo tỷ lệ kèm khoảng tin cậy 95% (cách tính Wilson). Với 20 người, khoảng này rộng khoảng ±20 điểm phần trăm, nên tỷ lệ gần 50% chỉ là tín hiệu yếu và cần ghi rõ như vậy.
- Báo riêng nhóm không học, không làm công nghệ thông tin (D2 = Không). Quyết định vẫn dựa trên toàn bộ phiếu.
- **Phương án "lẫn lộn"** ("lúc bật lúc tắt", "lúc bình thường lúc tiết kiệm pin") khớp cấu hình. Lý do: người chọn phương án này chờ con số đúng cả ở chế độ tốn pin hơn. Chế độ tốn pin hơn cũng là chế độ cấu hình đang chọn (chống ồn bật, chế độ nguồn thường), nên kết luận giống hệt.

| Câu | Kiểm điều kiện nào | Cấu hình hiện tại | Khớp cấu hình | Hiểu khác | Nếu quá nửa hiểu khác | Ví dụ trong hướng dẫn cần xem lại |
|---|---|---|---|---|---|---|
| Q01 | Hoạt động, pin điện thoại (`hoat_dong`) | Hoạt động kém thuận lợi nhất hãng công bố (iPhone 17: xem video trực tuyến, 27 giờ) | Trực tuyến; Chơi game; Dùng lẫn lộn | Xem video đã tải sẵn | Đổi mặc định thành xem video tải sẵn | V04, V24 |
| Q02 | Hoạt động, pin tai nghe (`hoat_dong`) | Nghe nhạc | Nghe nhạc, xem phim | Gọi điện; Dùng lẫn lộn | "Gọi điện" quá nửa: đổi mặc định thành đàm thoại. Hai phương án cộng lại quá nửa: đổi thành hoạt động kém thuận lợi nhất hãng công bố, như điện thoại | V32, V38 |
| Q03 | Chống ồn khi nghe nhạc (`che_do_chong_on`) | Bật | Bật suốt; Lúc bật lúc tắt | Tắt suốt | Đổi mặc định thành tắt | V10, V32, V38 |
| Q04 | Bộ phận, pin tai nghe (`bo_phan`) | Chỉ tai nghe | Chỉ tính tai nghe | Tính cả hộp sạc | "Bộ phận chính" là nguyên tắc của đề cương: không tự đổi, ghi vào giới hạn và hỏi CBHD | V09, V10, V31, V32, V38, V42, V44 |
| Q05 | Hoạt động, pin đồng hồ (`hoat_dong`) | Sử dụng bình thường. Apple tính cả một buổi tập 60 phút trong 18 giờ (`dh-apple-watchse3#008`) | Dùng bình thường; Dùng bình thường, có lúc tập | Tập thể thao liên tục | Đổi mặc định thành tập luyện | V14, V33, V39 |
| Q06 | Chế độ nguồn (`che_do_nguon`) | Chế độ thường | Bình thường; Lúc bình thường lúc tiết kiệm | Tiết kiệm pin | Đổi mặc định thành nguồn điện thấp | V14, V15, V33, V39, V41 |
| Q07 và Q15 | Quy tắc "bỏ lên đến vẫn khớp" (mục 6.2 của hướng dẫn) | Bỏ "lên đến" không đổi nhãn | (so từng người) | Người hiểu Q07 chắc chắn hơn Q15. Thứ tự từ yếu tới chắc: "mức tốt nhất, thực tế thường ít hơn"; "khoảng 18 giờ"; "ít nhất 18 giờ" | Đổi quy tắc: bỏ "lên đến" là Lệch (`doi_kieu_gia_tri`), tức đảo lại quyết định chiều 26/10 ở điểm 2 của T10 | V02, V03, V04, V09 |
| Q08 | Bộ sạc điện thoại (`bo_tiep_hop`) | Không mua thêm (hộp iPhone 17 chỉ có cáp, `dt-apple-iphone17#040`) | Đồ đi kèm khi mua là đủ; Củ sạc nào cũng được | Phải có củ sạc loại mạnh, mua riêng | "Không mua thêm phụ kiện" là nguyên tắc của đề cương: không tự đổi, ghi vào giới hạn và hỏi CBHD | V21, V23 |
| Q09 | Từ "xem video" (`xem_video` trong `cach_dien_dat` của `dien_thoai.yaml`) | "Xem video" không kèm chữ nào khác hiểu là xem video tải sẵn (30 giờ) | Tải sẵn | Trực tuyến; Cả hai, không phân biệt (khi đó con số phải đúng cả lúc xem trực tuyến, 27 giờ) | Bỏ "xem video", "xem phim" khỏi cách diễn đạt của `xem_video`. Khi đó "xem video" coi như không nêu rõ loại, lấy hoạt động kém thuận lợi nhất (trực tuyến, 27 giờ) | V03 (thành Lệch) |
| Q10 | Chế độ hiển thị (`che_do_hien_thi`) | Tiêu chuẩn | Dùng bình thường | Ngoài trời nắng; HDR; Mức sáng nhất, không rõ lúc nào | Một phương án quá nửa: "ngoài trời" hoặc "HDR" thì đổi mặc định thành chế độ đó; "mức sáng nhất" thì so với giá trị cao nhất của mọi chế độ (V25, V26, V43 thành Đúng). Ba phương án cộng lại quá nửa nhưng không cái nào quá nửa: đổi thành "không có mặc định" (D1a) | V25, V26, V43 |
| Q11 | Chế độ nguồn, kiểm chéo với Q06 | Chế độ thường | Bình thường; Lúc bình thường lúc tiết kiệm | Tiết kiệm pin | Không đổi cấu hình theo riêng câu này, vì cách hiểu mặc định không được phụ thuộc vào độ lớn con số. Nếu Q06 ra "khớp" mà Q11 ra "hiểu khác", ghi là phát hiện: người đọc đoán chế độ từ con số. Khi đó đưa V33 vào phân tích độ nhạy ở Bước 37 | V33 |
| Q12 | Loại zoom (`loai_zoom`) | Quang học | Bằng ống kính | Bằng phần mềm; Kết hợp | Đổi mặc định thành kỹ thuật số | V28 |
| Q13 | Chống ồn khi đàm thoại (`che_do_chong_on`) | Bật: 5 giờ là số khi tắt chống ồn (bật là 4,5 giờ), nên câu này ra Lệch | Bật suốt; Lúc bật lúc tắt | Tắt suốt | Như Q03. Nếu Q03 và Q13 cho kết quả trái nhau thì tách mặc định chống ồn theo hoạt động | Chưa có ví dụ; xét khi gán nhãn |
| Q14 | Bộ sạc đồng hồ (`bo_tiep_hop`) | Không mua thêm: bộ 20W chỉ ghi ở chú thích và không có trong hộp | Đồ đi kèm khi mua là đủ; Củ sạc nào cũng được | Phải có củ sạc loại mạnh, mua riêng | Như Q08 | V34 |

**Về cặp Q07 và Q15:** mỗi người trả lời cả hai câu, nên so được từng người. Cách này có thể làm người đọc đoán ra ý đồ của câu hỏi và cố trả lời khác đi. Nếu vậy thì số người đổi cách hiểu tăng lên, tức là lệch về phía bác bỏ quy tắc "bỏ lên đến vẫn khớp". Vì vậy nếu kết quả vẫn ủng hộ quy tắc thì kết luận càng chắc. Báo thêm tỷ lệ chọn từng phương án ở mỗi câu, để so với báo cáo FTC 2012 (`luan_van/phan_tich_dieu_kien_ngoai_cau_hinh.md` mục 8.1).

## 7. Kết quả

**Thu về ngày 27–28/10/2026:** 10 phiếu, lưu ở `ket_qua/khao_sat_cach_hieu.csv`. Bảng dưới do `scripts/tong_hop_khao_sat.py` tính, xếp phương án đúng như mục 6.

**Người trả lời:** 9 người 18–24 tuổi, 1 người 35–49 tuổi; 8 người học hoặc làm công nghệ thông tin, chỉ 2 người không; 9 người đã mua thiết bị loại này trong 2 năm qua. Mẫu này đạt mức 5–10 người của đề cương nhưng chưa đạt 20–30 người của kế hoạch, và lệch hẳn về người trẻ học công nghệ thông tin, không giống "người mua thông thường".

**Form thực tế khác mục 4 ở 3 chỗ:**
- Người thực hiện tạo một form mới (không phải form ở đường dẫn trong mục 3) và đổi cách xưng hô thành "mày".
- Q08: phương án đầu là "Chỉ cần dùng cái cục sạc có sẵn trong hộp máy lúc mua". Câu này ngầm nói trong hộp có củ sạc, trong khi hộp iPhone 17 chỉ có cáp, nên có thể kéo người đọc về phương án này. Phương án ba ghi "cục sạc" thay cho "củ sạc".
- Q14 dùng chữ của bản 2 trước khi sửa ("Chỉ cần đồ có sẵn trong hộp đồng hồ", "Củ sạc thông thường nào cũng được", "Phải dùng củ sạc công suất cao, thường phải mua riêng"). Nghĩa không đổi.

| Câu | Khớp cấu hình | Hiểu khác | Không biết | Tỷ lệ hiểu khác (KTC 95%) | Nhóm không CNTT: hiểu khác | Quá nửa hiểu khác? |
|---|---|---|---|---|---|---|
| Q01 | 9 | 1 | 0 | 10% (2%–40%) | 0/2 | Không |
| Q02 | 5 | 4 | 1 | 40% (17%–69%) | 1/2 | Không |
| Q03 | 6 | 4 | 0 | 40% (17%–69%) | 0/2 | Không |
| Q04 | 5 | 4 | 1 | 40% (17%–69%) | 0/2 | Không |
| Q05 | 9 | 1 | 0 | 10% (2%–40%) | 0/2 | Không |
| Q06 | 4 | 6 | 0 | 60% (31%–83%) | 0/2 | **Có** |
| Q08 | 5 | 5 | 0 | 50% (24%–76%) | 1/2 | Không (đúng một nửa) |
| Q09 | 1 | 9 | 0 | 90% (60%–98%) | 2/2 | **Có** |
| Q10 | 3 | 7 | 0 | 70% (40%–89%) | 1/2 | **Có** |
| Q11 | 6 | 4 | 0 | 40% (17%–69%) | 0/2 | Không |
| Q12 | 4 | 6 | 0 | 60% (31%–83%) | 1/2 | **Có** |
| Q13 | 6 | 4 | 0 | 40% (17%–69%) | 0/2 | Không |
| Q14 | 5 | 4 | 1 | 40% (17%–69%) | 1/2 | Không |

**Chi tiết các câu vượt ngưỡng:**
- Q06 (Watch "18 giờ", chế độ nào): tiết kiệm pin 6, bình thường 3, lúc bình thường lúc tiết kiệm 1. Cùng 10 người đó, ở Q11 ("32 giờ") lại có 6 người chọn chế độ bình thường và 4 người chọn tiết kiệm pin. 2 người chọn "tiết kiệm pin" cho 18 giờ nhưng "bình thường" cho 32 giờ.
- Q09 ("xem video"): cả hai, không phân biệt 5; trực tuyến 4; tải sẵn 1.
- Q10 (3000 nit): mức sáng nhất, không rõ lúc nào 5; dùng bình thường 3; HDR 2; ngoài trời 0. Không phương án "hiểu khác" nào vượt quá nửa.
- Q12 (zoom 10x): phần mềm 5, ống kính 4, kết hợp 1.

**Cặp Q07 và Q15 ("lên đến"):** Q07 có 9 người chọn "18 giờ là mức tốt nhất, dùng thực tế thường ít hơn" và 1 người chọn "ít nhất 18 giờ". Q15 có cả 10 người chọn "mức tốt nhất". Chỉ 1/10 người hiểu câu không có "lên đến" chắc chắn hơn câu có "lên đến", nên quy tắc "bỏ lên đến vẫn khớp" được giữ. Người đọc hiểu con số trần là mức tối đa ngay cả khi không có chữ "lên đến", khớp với báo cáo FTC 2012.

**Câu tự ghi (2 câu, đều ở Q08), xếp vào "phải dùng củ sạc công suất cao, mua riêng":**
- Một người ghi phải dùng sạc công suất cao và lưu ý Apple không tặng củ sạc. Người này cũng nhận xét quảng cáo "50% trong 20 phút" giấu thời gian sạc đầy.
- Một người ghi "nếu là iphone thì t nghĩ nó mua riêng".

**Ghi nhận khác:** 4/10 người hiểu "pin 6 giờ" của tai nghe là tính cả hộp sạc (Q04). Nguyên tắc "bộ phận chính" của đề cương vì vậy không phải ai cũng hiểu giống nhau; ghi vào phần giới hạn.

## 8. Các chỗ đã sửa theo khảo sát (chốt 28/10/2026)

Người thực hiện quyết định chốt với 10 phiếu, không khảo sát thêm.

**Sửa theo đúng tiêu chí đặt trước:**
- **Q09, "xem video" (9/10 hiểu khác):** trong `dien_thoai.yaml`, bỏ "xem video", "xem phim" khỏi cách diễn đạt của `xem_video`, thêm `chua_ro_loai_video`: cụm này coi như chưa nêu hoạt động, áp hoạt động kém thuận lợi nhất. Trong hướng dẫn, V03 đổi từ Đúng thành Lệch.
- **Q10, độ sáng (7/10 hiểu khác, không cách hiểu nào quá nửa):** `do_sang.hieu_thong_thuong.che_do_hien_thi` đổi từ `tieu_chuan` thành `khong_co_mac_dinh`. V25, V26, V43 đổi từ Lệch thành Chưa đủ thông tin (D1a). V27 sửa câu tuyên bố để tự nêu chế độ, giữ vai trò ví dụ điều kiện dạng số.

**Giữ cấu hình, lệch khỏi tiêu chí đặt trước:** Q06 (chế độ nguồn của đồng hồ, 6/10) và Q12 (zoom, 6/10). Theo tiêu chí, hai câu này phải đổi mặc định thành chế độ nguồn điện thấp và zoom kỹ thuật số. Không đổi vì 4 lý do:
1. Q06 trái với Q11 trên cùng 10 người: 6/10 người chọn "tiết kiệm pin" cho "18 giờ", nhưng 6/10 người chọn "bình thường" cho "32 giờ". Người đọc không có một cách hiểu ổn định. Khi người đọc chia hai, chỉ cách hiểu kém thuận lợi (chế độ thường, zoom quang học) bảo đảm tuyên bố được chấm Đúng là đúng với cả hai nhóm.
2. Cả hai câu chỉ vượt ngưỡng đúng 1 người, khoảng tin cậy 31%–83%.
3. 8/10 người học hoặc làm công nghệ thông tin. Với zoom, người trong ngành biết điện thoại thường phóng bằng phần mềm; 2 người ngoài ngành chia 1–1.
4. Đổi theo tiêu chí thì V33 ("pin 32 giờ") và V28 ("zoom 10x") thành Đúng, tức là hệ thống chấp nhận cả tuyên bố mà 4/10 người đọc hiểu theo cách bị lừa. Việc này làm tăng trực tiếp FAR, chỉ số chính của đề tài.

Cách bù: ở Bước 37, tính lại kết quả với hai mặc định thay thế (chế độ nguồn điện thấp; zoom kỹ thuật số) và báo cả hai. Khi viết khóa luận, nêu rõ đây là chỗ lệch khỏi tiêu chí đặt trước và lý do.

**Giữ, không vượt ngưỡng:** các câu còn lại. Q08 đúng một nửa (5/10); phương án đầu của form ngầm nói hộp có củ sạc, nên con số này có thể cao hơn thực tế. Quy tắc "bỏ lên đến vẫn khớp" được ủng hộ rõ (1/10).

**Giới hạn cần nêu khi viết:** 10 phiếu (đạt mức 5–10 của đề cương, chưa đạt 20–30 của kế hoạch); 8/10 người học công nghệ thông tin, 9/10 người 18–24 tuổi; dòng "Thông tin thêm" có thể gợi ý (Q06 nhắc chế độ tiết kiệm pin ngay trước câu hỏi; Q04 nhắc hộp sạc); 4/10 người hiểu pin tai nghe là tính cả hộp sạc, trái với nguyên tắc "bộ phận chính" của đề cương.

**Điểm 1 ở T10:** chốt giữ tạm chốt ngày 26/10 (điện thoại: hoạt động kém thuận lợi nhất; tai nghe: nghe nhạc, chống ồn bật; đồng hồ: sử dụng bình thường, chế độ thường), cộng hai sửa đổi trên.

## 9. Ghi nhận khi tạo bài (cho Bước 11, 12, 16)

- **13/18 bài bị cắt giữa chừng.** Gemini 2.5 Flash suy luận trước khi viết, và số token suy luận tính vào giới hạn 1.800 token của độ dài vừa. Ví dụ bài mô tả iPhone 17: 1.724 token suy luận, chỉ còn 72 token để viết. Chế độ `ten_thong_so` bị nặng hơn (8/9 bài so với 5/9 ở chế độ `ten`). Gemini 3.6 Flash và GPT-OSS 120B cũng suy luận trước khi viết, nên Bước 11 phải xử lý chỗ này trước khi sinh bộ thử, nếu không nhiều tuyên bố sẽ mất.
- **Chế độ `ten` gần như không có con số:** trong 9 bài, chỉ có một con số thuộc 16 thuộc tính của đề tài là "kháng nước và bụi chuẩn IPX7" cho Buds3 Pro (trang hãng ghi IP57). Đây là tín hiệu sớm cho rủi ro "quá ít tuyên bố" ở điểm 13 của T10, dù mô hình khác mô hình của đề tài và nhiều bài bị cắt.
- **Hai mô hình trong danh sách của CopyPro đã ngừng chạy:** `gemini-flash-lite` (Google báo không còn cho người dùng mới) và `groq-llama-3-3-70b` (Groq báo không có mô hình). Gói Free của CopyPro chỉ dùng `gemini-flash-lite`, nên người dùng gói Free hiện không tạo được bài.
- Lần chạy đầu bị lỗi đọc kết quả sau khi CopyPro đã tạo 1 bài (bài mô tả iPhone 17). Bài đó nằm trong thư viện của tài khoản demo nhưng không có trong tệp JSONL. Hai lần thử mô hình đã ngừng bị từ chối ngay, không tạo bài nào.
