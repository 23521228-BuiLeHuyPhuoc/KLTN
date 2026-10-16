# Nhật ký khóa luận

## 15/10/2026 — Kiểm lại Bước 4 theo yêu cầu

- Đọc lại 18 trang HTML chính hãng và hướng dẫn Watch8 tiếng Việt (bìa có SM-L330; kiểm trực tiếp trang 149). Hồ sơ `data/kiem_tra_nguon_buoc4.json` ghi ba giá trị/điều kiện cho mỗi mẫu, URL, thời điểm và hash nguồn. Đây là kiểm nguồn, không phải gán nhãn chuẩn.
- Sửa cách đếm chưa đúng phạm vi: bỏ kích thước S25 Ultra, điều kiện bật vùng nhịp tim Watch8, tần số lấy mẫu cảm ứng Xiaomi 15T và hai mức công suất sạc OPPO. Thay bằng các thuộc tính đã có trong T4.5, không mở rộng cấu hình từ tập kiểm tra.
- Bổ sung điều kiện trong chú thích cho AirPods Pro 3 và Watch SE 3; đánh dấu cách ghi không thống nhất về tổng pin Buds3 Pro và zoom 10x S25 Ultra. Không tự suy ra thiết lập thử pin Redmi Note 14 Pro+ mà hãng không công bố.
- Sau sửa, cả 12 mẫu có ít nhất ba mục phù hợp tiêu chí chọn nguồn. Giữ nguyên 4 mẫu phát triển/8 mẫu kiểm tra. Thẻ dữ liệu lên phiên bản 2; CSV chỉ thêm nguồn Xiaomi 15T và hướng dẫn Watch8. Chưa thu thập bộ bằng chứng theo Bước 5–6 hoặc chạy API.

## 15/10/2026 — Bước 4

- Chọn 12 mẫu và ghi `data/mau_san_pham.csv`: 5 điện thoại, 4 tai nghe, 3 đồng hồ; 4 hãng Apple, Samsung, Xiaomi, OPPO. Tạo `data/THE_DU_LIEU.md` bản đầu với tiêu chí nguồn, phiên bản sản phẩm, đường dẫn và dấu vết kiểm tra ít nhất ba thông số kèm điều kiện cho mỗi mẫu.
- Chốt 4 mẫu phát triển theo kế hoạch: iPhone 17, Xiaomi 15T, Galaxy Buds3 Pro, Apple Watch SE 3. Tám mẫu còn lại thuộc tập kiểm tra; tập này có đủ ba nhóm và bốn hãng. Không chia các biến thể cùng dòng sang hai tập. Redmi được tính là Xiaomi.
- Từ hôm nay, mọi lựa chọn thiết kế (tệp cấu hình, ví dụ hướng dẫn, câu lệnh gửi LLM, quy tắc, ngưỡng, tham số) chỉ dựa trên tập phát triển, theo T3.5 quy tắc 4. Đã xem nguồn tập kiểm tra để chọn mẫu, chưa dùng chúng để thiết kế hoặc đánh giá phương pháp.
- Kiểm tra trực tiếp nguồn tiếng Việt của hãng. AirPods 4 dùng trang hỗ trợ mã 121203 cho bản thường vì URL giới thiệu chuyển sang mẫu khác. Galaxy Watch8 chọn Bluetooth 44 mm. Ghi nguồn bổ sung khi chú thích nằm ở trang giới thiệu. Chưa thu thập bộ bằng chứng Bước 5–6, chưa gọi thêm API hoặc tạo nhãn chuẩn.

## 15/10/2026 — Bước 3

- Đối chiếu nhận định nghiên cứu trong đề cương bản cuối với 16 PDF gốc; kiểm SHA-256 khớp danh mục. Tạo `ghi_chu_tai_lieu.md` gồm bảng kiểm trích dẫn, ghi chú từng bài và số trang PDF bắt đầu từ 1; kiểm trực tiếp ảnh các bảng NumPert, Fathom, ViNumFCR.
- Bổ sung bốn bài FActScore, ProgramFC, ViWikiFC v2, Beyond Binary và báo cáo FTC 2012; lưu PDF, nguồn tải, thời điểm và mã băm trong `báo/bo_sung/`. Khảo sát có mục tiêu, không tuyên bố đã bao quát toàn bộ lĩnh vực.
- Làm rõ thiết lập 89,90% của ViFactCheck, BAcc/chi phí MiniCheck, phạm vi FA = 0 của VeriFin; đánh dấu diễn đạt 62% của NumPert, nguồn gốc sáu loại điều kiện và những nhận định tính mới cần thu hẹp. Chưa sửa đề cương PDF/DOCX hoặc tạo nhãn chuẩn bằng AI.
- Cập nhật trạng thái Bước 3 và dòng kế hoạch cũ về sáu bài để khớp bộ 16 bài hiện tại; gắn hồ sơ kiểm trang trong `kiem_tra_tai_lieu.json`. Bước tiếp theo là chọn mẫu/chia tập ở Bước 4. Không sửa mã LLM hoặc chạy thêm API trong bước khảo sát này.

## 13/10/2026 — Bước 2

- Khảo sát đúng repo `/home/phuocblh/KLTN/KLTN` (`main`, HEAD `78c8150`, ban đầu sạch); đọc README, Bước 2/T3.1/T3.5/T4.6/T5.1/T5.3 và đối chiếu PDF đề cương bản cuối. Giữ nguyên repo CopyPro bên cạnh, đề cương và lịch kế hoạch; không commit/push theo yêu cầu.
- Tạo sáu thư mục, package editable, `.venv` Python 3.14.4, đủ thư viện cùng pin/lock; chọn Pyvi vì gọn. Bộ pin cần Python ≥ 3.12; thay wrapt prerelease bằng 2.5.0 ổn định. 16 import, tokenizer, biểu đồ không giao diện và `pip check` đạt.
- Viết giao diện Gemini/Groq chung, cache JSON theo hash đầy đủ và tách mock/live, nhật ký JSONL an toàn, timeout/retry giới hạn. 32 kiểm thử đạt (gồm cache qua tiến trình mới, SDK/HTTP giả lập); còn một cảnh báo deprecation từ SDK Google.
- Tạo 10 câu kỹ thuật nguyên văn từ T4.6 cùng kỳ vọng đọc từ câu, không phải nhãn chuẩn nghiên cứu; chạy offline ba cấu hình, 30 lượt lặp đọc cache. Ghi tài nguyên môi trường, phiên bản và nguồn quota chính thức vào `ket_qua/thu_llm.md`; chưa xây BM25/P hoặc dùng tập kiểm tra.
- Trở ngại: thiếu khóa Gemini/Groq, chưa xác minh Free tier/quota tài khoản; live tiền kiểm exit 2, không gọi API thật. Git xác nhận `.env` từng được commit rồi bỏ theo dõi nhưng chưa có căn cứ khóa đã thu hồi. Cần người dùng thu hồi/tạo mới và cấu hình `.env`, sau đó chạy thử thật; Bước 2 chưa hoàn thành đầy đủ.
