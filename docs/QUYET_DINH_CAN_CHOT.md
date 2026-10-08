# Quyết định cần chốt (rà soát 08/10/2026)

Mọi mục dưới đây là **DỰ THẢO — cần sinh viên/GVHD xác nhận**. Cột "Đề xuất" là phương án người rà soát chọn; chưa có giá trị phê duyệt.

| # | Câu hỏi | Đề xuất | Phương án khác | Căn cứ | Hạn chốt |
|---|---|---|---|---|---|
| D1 | Claim không nêu điều kiện thử (âm lượng 50%…) xử lý thế nào ở bước B? | `inherit_headline`: kế thừa điều kiện thử của chính thông số; điều kiện nêu rõ vẫn phải khớp; "luôn/mọi chế độ" không kế thừa (QUY_TAC_ABC §3b) | Đọc nghĩa đen → 11/23 câu gốc thành NEI; viết lại claim (không áp được cho LLM thật) | `tests/test_abc.py::test_original_claims_*` | 20/10 |
| D2 | Quảng cáo tiếng Việt có dùng được nguồn Apple thị trường khác (Moldova) không? | Không mặc định; chỉ dùng khi trang VN không có và ghi `market_mismatch`; nhãn mặc định NEI-thiếu | Coi thông số toàn cầu là như nhau | EX-13–15 lệch nhãn khi bỏ tiền tố "tại Moldova" | 20/10 |
| D3 | Ca biên C2 chưa có trong bảng: "khoảng a" vs số chính xác a; Bluetooth "5.0 trở lên"; "tối đa 15" đọc là M hay cận x | Cả ba → UNKNOWN trừ khi ngữ cảnh rõ; "tối đa" trong trang thông số hãng = M | Cho dung sai/so phiên bản lớn hơn | `tests/test_abc.py::EdgeCases` | Gate 1 |
| D4 | Có tính nhãn EX theo `original_claim` hay `reviewed_claim`? | Sau D1, gán cho `original_claim`; giữ `reviewed_claim` làm lịch sử | Giữ như hiện tại (chỉ câu sửa) | GIAO_THUC §1: thêm điều kiện = biến thể | 20/10 |
| D5 | Mốc 15/10 | **(Sửa 08/10, redesign)** Gate 1 kéo đến 31/10: môi trường API + lô 0 (2 họ × 5 quảng cáo) + đo năng suất + hướng dẫn v1; pilot 45–60 claim / 6 họ thuộc Gate 2 (01–14/11) | Giữ pilot 45–60 vào 15/10 (không khả thi: 08/10 chưa có API/log) | Đến 08/10 chưa có quảng cáo LLM có log, chưa có cấu hình API | 10/10 |
| D6 | Cỡ test và cách báo RQ3 | Giữ RQ3 thăm dò; nếu năng suất cho phép, nâng R+NEI test lên ≥ 40 | Tuyên bố có ý nghĩa thống kê với 4 họ | `scripts/simulate_power.py` | Gate 2 |
| D7 | Tiêu chí dừng thu `ordinary_llm` | Đạt sàn, hoặc 3 lô liên tiếp một nhãn tăng < 2, hoặc chạm ngân sách [SINH VIÊN ĐIỀN] | Thu đến khi đủ cân bằng nhãn | GIAO_THUC §10 | 20/10 |
| D8 | Người gán thứ hai cho 30 claim | Mời một bạn cùng khóa trước 20/10, gán sau khi khóa hướng dẫn | Chỉ tự gán lại 20% (ghi hạn chế) | GIAO_THUC §3 | 20/10 |

## Quyết định bổ sung khi thiết kế lại kế hoạch (08/10/2026, DỰ THẢO)

| # | Câu hỏi | Đề xuất | Phương án khác | Căn cứ | Hạn chốt |
|---|---|---|---|---|---|
| D9 | Lịch Gate | Gate 1 08–31/10; Gate 2 01–14/11; Gate 3 15/11–04/12; Gate 4 05–11/12; Gate 5 12–21/12; Gate 6 22–31/12 | Lịch cũ (Gate 1 01–15/10) | Đến 08/10 chưa có log LLM; hạn bảo vệ HK1 chưa công bố (chưa xác minh) | 20/10 |
| D10 | Nhà cung cấp và mô hình Llama | [SINH VIÊN ĐIỀN] — một nhà cung cấp chính + một dự phòng, ghi mã mô hình trả về | Chạy local (máy chưa rõ cấu hình) | GIAO_THUC §7 | 24/10 |
| D11 | Có hãng ngoài Apple không | Ít nhất 1 hãng (2–4 họ trong 12) có trang thông số chính thức lưu được | Chỉ Apple, ghi giới hạn | Phản biện (j): kết luận chỉ đúng một kiểu trình bày | Gate 2 |
| D12 | Cam kết quy mô | MVP 120/12 (6/2/4); 180/18 (7/4/7) chỉ khi năng suất đo cho phép; bỏ 300 | Giữ 3 tầng 120/180/300 | Một sinh viên, 12–20 giờ/tuần, còn ~12 tuần | 14/11 |
