# Báo cáo bộ thử — Bản nháp gửi CBHD

Ngày 02/11/2026. Kính gửi Thầy/Cô, em báo cáo kết quả bộ thử như sau.

## 1. Mục tiêu

Em dùng bộ thử để rà soát hướng dẫn kiểm chứng tuyên bố thông số kỹ thuật có điều kiện trong quảng cáo tiếng Việt do LLM tạo. Bộ thử giúp kiểm tra bốn nhãn Đúng, Sai, Lệch điều kiện, Chưa đủ thông tin và chốt quy mô dữ liệu.

## 2. Dữ liệu

Bộ thử gồm 2 mẫu (iPhone 17 và Galaxy Buds3 Pro), 24 bài và 66 tuyên bố. Các thuộc tính của cả 66 tuyên bố đều có điều kiện bắt buộc trong cấu hình.

| Chế độ đầu vào | Số bài | Tuyên bố | Trung bình/bài | Bài không có tuyên bố |
|---|---:|---:|---:|---:|
| Chỉ tên sản phẩm (ten) | 12 | 15 | 1,25 | 4/12 |
| Tên và thông số (ten_thong_so) | 12 | 51 | 4,25 | 0/12 |
| Toàn bộ | 24 | 66 | 2,75 | 4/24 |

## 3. Hướng dẫn gán nhãn

Em đã chốt hướng dẫn bản 2 và cập nhật ngày 02/11/2026. Các thay đổi chính gồm:

- Xác định điều kiện trước khi so con số; dùng cách hiểu mặc định ở mọi bước xét nhãn và ghi rõ điều kiện được hiểu mặc định.
- Làm rõ cụm chỉ nhiều điều kiện, từ khẳng định gắn với con số và trường hợp tài liệu mâu thuẫn. Việc bỏ riêng cụm “lên đến” không tự động dẫn đến nhãn Lệch.
- Phân biệt giá trị thông số với con số dùng làm điều kiện; không tạo giá trị mới bằng phép tính; ghi đủ các đoạn bằng chứng tương ứng.
- Áp dụng QĐ15: nếu tuyên bố gọi điều kiện bằng đúng nhãn của một dòng thông số trong tài liệu, không thiếu chữ điều kiện nào, thì coi là cùng điều kiện với dòng đó. Luật xét trước cách hiểu mặc định và khớp bằng chữ, không suy từ con số. Lý do là tránh tự thêm nghĩa mà nhãn của hãng không ghi; ảnh hưởng của luật cần được xét trong phân tích độ nhạy.

## 4. Gán nhãn và phân bố

Lượt 1 do em gán theo bản 1; em giữ kết quả để nhận diện chỗ chưa rõ và sửa hướng dẫn. Lượt 2 do Claude gán trước theo bản 2, sau đó em duyệt. Nhãn chuẩn của bộ thử vì vậy là **“Claude gán, người duyệt”**; em có thể bị nhãn có sẵn dẫn dắt, và đây không phải gán độc lập giữa hai người.

| Nhãn | Lượt 1 | Lượt 2 | Tỷ lệ lượt 2 |
|---|---:|---:|---:|
| Đúng | 24 | 34 | 51,5% |
| Sai | 4 | 6 | 9,1% |
| Lệch điều kiện | 15 | 18 | 27,3% |
| Chưa đủ thông tin | 23 | 8 | 12,1% |

## 5. Kết quả sơ bộ

Các số dưới đây là kết quả sơ bộ trên bộ thử 66 tuyên bố, dùng nhãn lượt 2. Recall@k chỉ tính 64 tuyên bố có bằng chứng; 2 tuyên bố không có bằng chứng không vào mẫu số. Một tuyên bố được tính là trúng khi có ít nhất một đoạn bằng chứng trong top-k.

| BM25 | k = 1 | k = 3 | k = 5 | k = 8 |
|---|---:|---:|---:|---:|
| Tách âm tiết | 96,9% (62/64) | 98,4% (63/64) | 100,0% (64/64) | 100,0% (64/64) |
| Tách từ (pyvi) | 100,0% (64/64) | 100,0% (64/64) | 100,0% (64/64) | 100,0% (64/64) |

Đối chứng B0 dùng GPT-OSS 120B, nhận top-5 đoạn BM25 tách âm tiết và không có nhãn Lệch riêng. Trên đủ 66 tuyên bố, FAR là **75,0% (24/32)**, Recall nhãn Đúng là **97,1% (33/34)**; **15/18** tuyên bố Lệch bị gán Đúng. FAR tính tỷ lệ nhãn chuẩn khác Đúng bị B0 gán Đúng.

Các báo cáo lượt 1 dùng nhãn và mẫu số khác nên không dùng để kết luận hệ thống đã cải thiện. Recall lượt 2 còn có thể lạc quan vì tập bằng chứng được mở rộng, có cả đoạn không chứa con số. Mô hình, k và cách tách hiện là lựa chọn tạm.

## 6. Điểm dừng nhãn Lệch

| Tiêu chí | Trạng thái đến 02/11/2026 |
|---|---|
| Có ít nhất 10 ca Lệch không thuộc loại “lên đến” | Đạt: 17 ca. |
| Người thứ hai gán độc lập ít nhất 30 câu; kappa nhãn Lệch ≥ 0,6 | Em chưa tìm được người thứ hai. Em dự kiến tự gán lại mù 30 câu sau vài ngày, gồm mọi ca Lệch và các câu chọn ngẫu nhiên. Chưa có kết quả; phép đo này chỉ phản ánh độ nhất quán với nhãn chuẩn, không thay thế đồng thuận giữa hai người. |
| Nhận ra ít nhất 80% cụm điều kiện quyết định trên 3 sản phẩm ngoài 12 mẫu | Chưa thực hiện. |

Em chưa đủ căn cứ xác nhận đã đạt toàn bộ điểm dừng.

## 7. Quy mô đã chốt

Em đã chọn 8 bài mỗi mẫu cho 10 mẫu còn lại: 4 bài chỉ tên và 4 bài tên kèm thông số, chia đều cho 2 LLM, xoay vòng loại bài. Phương án có 80 bài mới, dự kiến khoảng **286 tuyên bố**, tính cả bộ thử, và khoảng **78 ca Lệch**. Đây là dự kiến từ số đo bộ thử. Trung bình chung 2,75 tuyên bố/bài không dưới ngưỡng 2 của T9.1 nên em chưa áp dụng phương án thêm từ khóa.

## 8. Rủi ro và giới hạn

- Khảo sát cách hiểu chỉ có 10 người, lệch về người học công nghệ thông tin. Nhãn chuẩn do Claude gán và em duyệt còn có nguy cơ thiên lệch.
- Gemini 3.6 Flash vượt hạn mức, chưa chạy hết bộ thử; kết quả B0 hiện chỉ báo cáo GPT-OSS 120B.
- Bảng so sánh nhiều mẫu đã khiến B0 lấy nhầm số của mẫu khác. Recall cao chưa bảo đảm mô hình đọc đúng cột sản phẩm.
- Bộ thử chỉ có điện thoại và tai nghe, chưa có số đo cho đồng hồ. Tiến độ trễ so với Mốc 2 ngày 31/10/2026; đến 02/11/2026, điểm dừng nhãn Lệch vẫn chưa hoàn tất.

## 9. Xin ý kiến Thầy/Cô

- Thầy/Cô có chấp nhận phương án gán lại mù thay cho người gán thứ hai, với giới hạn nêu trên không?
- Luật chép đúng nhãn của tài liệu (QĐ15) có hợp lý không?
- Nhãn chuẩn theo cách “Claude gán, người duyệt” có được chấp nhận cho bộ thử không?
- Quy mô 8 bài mỗi mẫu cho phần còn lại có phù hợp không?
