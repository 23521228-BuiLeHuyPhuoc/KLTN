# Nhật ký khóa luận

## 13/10/2026 — Bước 2

- Khảo sát đúng repo `/home/phuocblh/KLTN/KLTN` (`main`, HEAD `78c8150`, ban đầu sạch); đọc README, Bước 2/T3.1/T3.5/T4.6/T5.1/T5.3 và đối chiếu PDF đề cương bản cuối. Giữ nguyên repo CopyPro bên cạnh, đề cương và lịch kế hoạch; không commit/push theo yêu cầu.
- Tạo sáu thư mục, package editable, `.venv` Python 3.14.4, đủ thư viện cùng pin/lock; chọn Pyvi vì gọn. Bộ pin cần Python ≥ 3.12; thay wrapt prerelease bằng 2.5.0 ổn định. 16 import, tokenizer, biểu đồ không giao diện và `pip check` đạt.
- Viết giao diện Gemini/Groq chung, cache JSON theo hash đầy đủ và tách mock/live, nhật ký JSONL an toàn, timeout/retry giới hạn. 32 kiểm thử đạt (gồm cache qua tiến trình mới, SDK/HTTP giả lập); còn một cảnh báo deprecation từ SDK Google.
- Tạo 10 câu kỹ thuật nguyên văn từ T4.6 cùng kỳ vọng đọc từ câu, không phải nhãn chuẩn nghiên cứu; chạy offline ba cấu hình, 30 lượt lặp đọc cache. Ghi tài nguyên môi trường, phiên bản và nguồn quota chính thức vào `ket_qua/thu_llm.md`; chưa xây BM25/P hoặc dùng tập kiểm tra.
- Trở ngại: thiếu khóa Gemini/Groq, chưa xác minh Free tier/quota tài khoản; live tiền kiểm exit 2, không gọi API thật. Git xác nhận `.env` từng được commit rồi bỏ theo dõi nhưng chưa có căn cứ khóa đã thu hồi. Cần người dùng thu hồi/tạo mới và cấu hình `.env`, sau đó chạy thử thật; Bước 2 chưa hoàn thành đầy đủ.
