# Câu hỏi phản biện dự kiến và hướng trả lời

Danh sách do công cụ AI soạn ngày 08/10/2026. Đây chỉ là **hướng** trả lời. Sinh viên phải tự trả lời bằng số liệu thật của mình.

1. **Tính mới của đề tài là gì?** Có ba đóng góp có giới hạn, gồm C1 (dữ liệu có provenance), C2 (đặc tả so sánh kiểu giá trị cùng kiểm thử) và C3 (so sánh có kiểm soát P với B1). Không nói "đầu tiên"; chỉ nói "trong các tài liệu đã đọc chưa thấy".
2. **120 phát biểu có quá ít không?** Có, nên kết quả được báo là thăm dò, có khoảng tin cậy theo họ và kết quả `simulate_power`. Trọng tâm là quy trình, không phải benchmark.
3. **Tại sao không làm hệ thống end-to-end?** Truy xuất web mở thì khó kiểm soát và khó tái lập. Đề tài dùng hồ sơ bằng chứng cố định để tách riêng tác động của bước quyết định.
4. **NEI có nghĩa là hãng không công bố không?** Không. NEI chỉ nghĩa là không tìm thấy trong corpus đã chụp, có search_log làm chứng.
5. **Luật A–B–C có phải chỉ là luật thủ công?** Đúng, và đó là chủ ý: luật là đặc tả có thể kiểm thử. Phân tích lỗi chỉ ra ca nào luật giúp và ca nào luật hại.
6. **Vì sao cần inherit_headline?** Nếu đọc nghĩa đen thì 11/23 câu gốc chuyển thành NEI. Luật này mô tả cách người đọc hiểu điều kiện ở tiêu đề. Đây là quyết định D1 đã được GVHD chốt hoặc chưa chốt (ghi đúng trạng thái).
7. **Nhãn có đáng tin không?** Có người gán thứ hai trên 30 phát biểu, báo kappa và cách xử lý bất đồng. Nếu không có người thứ hai thì phải nói rõ.
8. **Có rò nhãn vào prompt không?** Có `check_input_leak.py`, tập test được khóa bằng hash trước khi chạy, và mọi hệ thống dùng cùng một hướng dẫn.
9. **Dùng LLM sinh dữ liệu rồi lại dùng LLM kiểm thì có vòng lặp không?** Có nhóm ordinary_llm (≥50%) tách khỏi controlled_variant, và có báo kết quả theo từng nhóm.
10. **Sao chủ yếu là Apple?** Vì Apple có trang thông số rõ ràng. Có ít nhất 1 hãng khác; không tổng quát hóa sang các hãng còn lại.
11. **Llama qua API có tái lập được không?** Có ghi tên và phiên bản model, ngày, nhiệt độ, hash prompt, và chạy 3 lượt để báo độ dao động.
12. **Vì sao dùng FAR làm chỉ số chính?** Duyệt nhầm quảng cáo sai gây hại nhiều nhất. Recall Supported được báo kèm để không thưởng cho hệ thống "từ chối tất cả".
13. **Vì sao dùng cluster bootstrap?** Các câu trong cùng một họ phụ thuộc nhau; bootstrap theo câu sẽ cho khoảng tin cậy hẹp giả tạo.
14. **Nếu P không tốt hơn B1 thì sao?** Kết quả âm vẫn được báo. Ablation và phân tích lỗi chỉ ra nguyên nhân là do trích xuất hay do luật.
15. **recall@k tính thế nào khi hồ sơ ít đoạn?** Dùng k_eff = min(k, N) và báo N.
16. **Bạn đã dùng AI vào việc gì?** Trả lời theo mục khai báo AI: soạn thảo, rà soát, mã. Mọi nhãn và mọi xác nhận do sinh viên làm.
17. **Bản quyền của PDF bài báo và bản dịch trong repo?** Đã ghi nhận vấn đề và đề xuất chuyển sang lưu riêng tư hoặc chỉ giữ liên kết; quyết định do sinh viên và GVHD đưa ra.
18. **Ứng dụng thực tế là gì?** Một bước kiểm tra trước khi đăng quảng cáo do LLM sinh: gắn cờ phát biểu Refuted hoặc NEI để người duyệt xem lại. Đây không phải duyệt tự động.
19. **Khóa API bị lộ đã xử lý thế nào?** Đã gỡ khỏi phần theo dõi, đã thu hồi khóa ([SINH VIÊN ĐIỀN: ngày]); lịch sử Git vẫn còn khóa cũ, nên cần thu hồi là bắt buộc.
20. **Nếu làm tiếp thì làm gì?** Mở rộng số hãng, thêm truy xuất mở, tăng cỡ test để đạt độ mạnh thống kê.
