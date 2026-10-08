# Quyết định cần chốt (rà soát 08/10/2026)

Mọi mục dưới đây là **DỰ THẢO — cần sinh viên/GVHD xác nhận**. Cột "Đề xuất" là phương án người rà soát chọn; chưa có giá trị phê duyệt.

| # | Câu hỏi | Đề xuất | Phương án khác | Căn cứ | Hạn chốt |
|---|---|---|---|---|---|
| D1 | Claim không nêu điều kiện thử (âm lượng 50%…) xử lý thế nào ở bước B? | `inherit_headline`: kế thừa điều kiện thử của chính thông số; điều kiện nêu rõ vẫn phải khớp; "luôn/mọi chế độ" không kế thừa (QUY_TAC_ABC §3b) | Đọc nghĩa đen → 11/23 câu gốc thành NEI; viết lại claim (không áp được cho LLM thật) | `tests/test_abc.py::test_original_claims_*` | 15/10 |
| D2 | Quảng cáo tiếng Việt có dùng được nguồn Apple thị trường khác (Moldova) không? | Không mặc định; chỉ dùng khi trang VN không có và ghi `market_mismatch`; nhãn mặc định NEI-thiếu | Coi thông số toàn cầu là như nhau | EX-13–15 lệch nhãn khi bỏ tiền tố "tại Moldova" | 15/10 |
| D3 | Ca biên C2 chưa có trong bảng: "khoảng a" vs số chính xác a; Bluetooth "5.0 trở lên"; "tối đa 15" đọc là M hay cận x | Cả ba → UNKNOWN trừ khi ngữ cảnh rõ; "tối đa" trong trang thông số hãng = M | Cho dung sai/so phiên bản lớn hơn | `tests/test_abc.py::EdgeCases` | Gate 1 |
| D4 | Có tính nhãn EX theo `original_claim` hay `reviewed_claim`? | Sau D1, gán cho `original_claim`; giữ `reviewed_claim` làm lịch sử | Giữ như hiện tại (chỉ câu sửa) | GIAO_THUC §1: thêm điều kiện = biến thể | 15/10 |
| D5 | Mốc 15/10 | Chỉ cam kết khóa schema/hướng dẫn + lô 0 (2 họ × 5 quảng cáo) + đo năng suất; pilot 45–60 claim / 6 họ dời về 31/10 | Giữ pilot 45–60 vào 15/10 | Đến 08/10 chưa có quảng cáo LLM có log, chưa có cấu hình API | 10/10 |
| D6 | Cỡ test và cách báo RQ3 | Giữ RQ3 thăm dò; nếu năng suất cho phép, nâng R+NEI test lên ≥ 40 | Tuyên bố có ý nghĩa thống kê với 4 họ | `scripts/simulate_power.py` | Gate 2 |
| D7 | Tiêu chí dừng thu `ordinary_llm` | Đạt sàn, hoặc 3 lô liên tiếp một nhãn tăng < 2, hoặc chạm ngân sách [SINH VIÊN ĐIỀN] | Thu đến khi đủ cân bằng nhãn | GIAO_THUC §10 | 15/10 |
| D8 | Người gán thứ hai cho 30 claim | Mời một bạn cùng khóa trước 20/10, gán sau khi khóa hướng dẫn | Chỉ tự gán lại 20% (ghi hạn chế) | GIAO_THUC §3 | 20/10 |
