# T-18 · Danh sách chỗ cần bạn rà lại tách tuyên bố (tập phát triển)

Mục 2 của `data/huong_dan_gan_nhan.md` (đoạn "Rà tách trước khi gán") ghi: người rà tự quyết từng chỗ, không nhờ AI gợi ý. Vì vậy Claude **không sửa** `data/tuyen_bo/*.jsonl` và `data/nhan/*.jsonl` cho mục này. Tệp này chỉ liệt kê chỗ rà soát đã phát hiện, kèm câu gốc, để bạn tự quyết có tách, sửa hay giữ, và tự viết chữ tuyên bố.

Khi sửa, ghi `tach_sua=<sửa gì>` vào `ghi_chu` của tuyên bố như hướng dẫn yêu cầu. Tuyên bố mới cần mã mới (mã lớn nhất hiện là `tb-00109`), cần gán nhãn, và cần chạy trích xuất cho riêng các tuyên bố mới hoặc đổi chữ (khoảng 10–13 lượt gọi LLM).

## A. Câu có thông số trong phạm vi nhưng chưa có tuyên bố nào

| # | Bài quảng cáo (`data/quang_cao/<mã>.json`) | Tập | Câu trong bài | Thuộc tính liên quan |
|---|---|---|---|---|
| 1 | `qc-dh-apple-watchse3-gemini-landing-ten-1` (bài đang có 0 tuyên bố) | chính | "… và khả năng chống nước ở độ sâu 50m đáp ứng tốt mọi hoạt động thể thao." | kháng nước |
| 2 | `qc-dh-apple-watchse3-gptoss-landing-ten_thong_so-1` | chính | "Pin bền cả ngày, lên tới 18 giờ sử dụng bình thường và sạc nhanh 80 % chỉ trong 45 phút, …" (phần 18 giờ đã là `tb-00078`) | sạc nhanh |
| 3 | `qc-dt-xiaomi-15t-gemini-description-ten_thong_so-1` | chính | "Bền bỉ vượt trội trước mọi tác động từ môi trường nhờ chuẩn chống nước và chống bụi IP68 cao cấp." | kháng nước |
| 4 | `qc-dt-xiaomi-15t-gemini-landing-ten_thong_so-1` | chính | "Xiaomi 15T khẳng định độ bền bỉ cao cấp với chuẩn chống nước và bụi IP68 cùng mặt kính cường lực …" | kháng nước |
| 5 | `qc-dt-xiaomi-15t-gptoss-description-ten-1` | chính | "Pin 5000mAh hỗ trợ sạc nhanh 120W, chỉ trong 20 phút bạn đã có đầy năng lượng cho cả ngày." (5000mAh là `tb-00093`, 20 phút là `tb-00094`) | công suất sạc |
| 6 | `qc-dt-apple-iphone17-gptoss-description-ten_thong_so-1` | bộ thử | "Độ bền IP68, lớp phủ kháng dầu, chống vân tay, cùng cổng USB‑C …" | kháng nước |
| 7 | `qc-dt-apple-iphone17-gptoss-social-ten_thong_so-1` | bộ thử | "Độ bền IP68, lớp phủ kháng dầu, chống vân tay – sẵn sàng đối mặt …" | kháng nước |
| 8 | `qc-dt-apple-iphone17-gptoss-landing-ten_thong_so-1` | bộ thử | "Hệ thống camera 48MP Dual Fusion kết hợp Telephoto 2x và Ultra Wide 120°, …" (bài `social` cùng mẫu đã tách "telephoto 2x" thành `tb-00033`) | zoom |

Ba câu số 6–8 thuộc bộ thử. Thêm tuyên bố vào bộ thử không chạm 20 tuyên bố của lượt 3 (`data/nhan/chon_luot3.txt`), nhưng làm đổi con số 66 ở các báo cáo Bước 13–16.

## B. Tuyên bố đã tách nhưng lệch câu gốc

| Mã | Câu gốc trong bài | Chữ tuyên bố hiện tại | Chỗ lệch |
|---|---|---|---|
| `tb-00071` | "Thời lượng pin ấn tượng lên đến 18 giờ sử dụng thông thường và 32 giờ ở Chế Độ Nguồn Điện Thấp." | "Apple Watch SE 3 có thời lượng pin lên đến 18 giờ (khi sử dụng thông thường) và 32 giờ (ở Chế Độ Nguồn Điện Thấp)" | Hai giá trị trong một tuyên bố, trái quy tắc "mỗi tuyên bố một thuộc tính và một giá trị". Bạn đã chủ ý giữ ngày 15/11 (nhật ký dòng 138, 155). Chạy P trên bản ghi này: bộ trích xuất gán điều kiện "nguồn điện thấp" của vế 32 giờ cho giá trị 18 giờ, và Bước 29 sẽ chấm oan bộ tách tự động ở vế 32 giờ |
| `tb-00073` | "Khả năng chống nước ở độ sâu 50m, sẵn sàng đồng hành trong **mọi** buổi tập bơi lội." | "… chống nước ở độ sâu 50m (trong buổi tập bơi lội)" | Rơi chữ "mọi" |
| `tb-00080` | "Thiết kế nhẹ nhàng, thời lượng pin lên tới 18 giờ, phù hợp cho mọi công việc và hoạt động ngoài trời." | "Apple Watch SE 3 có thời lượng pin lên tới 18 giờ" | Bỏ vế "phù hợp cho mọi công việc và hoạt động ngoài trời". Vế này có thuộc con số không là chỗ bạn xét theo tiêu chí gắn điều kiện 2 và 3 ở mục 2 |
| `tb-00079` | "Màn hình Retina Luôn Bật sáng tới 1000 nit, kính cường lực Ion‑X chịu nứt gấp 4 lần, …" | (chữ tuyên bố ổn) | `cau_goc` chép cụt ở dấu phẩy |

## C. Sau khi bạn sửa

Báo Claude để: chạy trích xuất cho các tuyên bố mới hoặc đổi chữ, chạy lại P, cập nhật số đếm 108 ở kế hoạch và `data/THE_DU_LIEU.md`, đánh dấu T-18 xong trong `ra_soat/TONG_HOP_BAT_THUONG.md`.
