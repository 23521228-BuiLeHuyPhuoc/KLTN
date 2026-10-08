# Đối chiếu thay đổi kế hoạch (nhánh `plan/opus-2026-10-08`, gốc `ca2c849`)

Công cụ AI (Claude) soạn ngày 08/10/2026. Mọi điểm mới đều là **DỰ THẢO — cần GVHD xác nhận**. Trong docx, các phần mới hoặc đã sửa được tô chữ đỏ (C00000); xem `scripts/redesign_plan_2026_10_08.py`.

| # | Cũ | Mới | Lý do | Ảnh hưởng điểm / tính mới / khả thi |
|---|---|---|---|---|
| a | Gate 1 kết thúc 15/10, phải có đúng 6 họ | Gate 1 08–31/10 (khóa, provider, lô 0); 6 Gate kết thúc 31/12 (D5, D9) | Ngày 08/10 chưa có dữ liệu thu theo quy trình | Khả thi ↑; không ảnh hưởng tính mới |
| b | Luật B đọc nghĩa đen: 11/23 câu gốc thành NEI | Luật inherit_headline (D1, QUY_TAC §3b) có kiểm thử; giữ original và reviewed tách nhau | Recall Supported bị méo | Phương pháp ↑; là một phần của C2 |
| c | Mức 7/4/7 hoặc 8/4/8 và mức 300 | MVP 120/12 (6/2/4), mục tiêu 180/18 (7/4/7); bỏ 300 (D12); RQ3 là thăm dò; báo mẫu số | simulate_power: CI rộng 0,24–0,34 với 4 họ | Trung thực ↑; khả thi ↑ |
| d | Nguy cơ vòng lặp giữa nhãn và P | Cùng hướng dẫn và hash cho B0/B1/P; người gán thứ hai trên 30 phát biểu; check_input_leak | Phản biện sẽ hỏi | Độ tin cậy ↑ (C1) |
| e | Biến thể có kiểm soát trộn với quảng cáo thường | Tách nhóm controlled_variant, ordinary_llm ≥ 50%, báo kết quả riêng | Tránh thổi phồng | Phương pháp ↑ |
| f | NEI hiểu như "hãng không công bố" | NEI là kết luận theo corpus, có search_log | Không thể chứng minh điều không tồn tại | Tránh bị bắt lỗi |
| g | Câu chữ gợi ý hệ thống end-to-end | Ghi rõ không phải end-to-end; hồ sơ bằng chứng cố định | Phạm vi thật | Không phóng đại |
| h | recall@k có thể cao một cách hiển nhiên | Báo N và k_eff = min(k, N) | Truy hồi đã lọc theo sản phẩm | Minh bạch |
| i | EX-13–15 dùng trang Apple Moldova mà không ghi chú | Ghi chú đỏ trong HuP_3; quyết định D2 | Thị trường khác | Trung thực |
| j | Chỉ dùng Apple | Thêm ít nhất 1 hãng ngoài Apple (D11) | Tổng quát yếu | Phạm vi ↑, chi phí ↑ |
| k | HuP_3 viết "Đã đối chiếu" bằng giọng sinh viên; có ghi chú nội bộ | "Theo báo/…" kèm ghi chú cần tự kiểm; mục KHAI BÁO SỬ DỤNG CÔNG CỤ AI; bỏ phụ lục nội bộ | Trung thực về phần AI hỗ trợ | Tránh rủi ro liêm chính |
| l | Không có danh sách đóng góp | C1–C3 kèm danh sách không được tuyên bố (DINH_VI_VA_TIEU_CHI) | Tính mới cần rõ mà không phóng đại | Tính mới rõ |
| m | `--check` FAIL ('độc lập 30') | validate_content viết lại theo thiết kế mới (**đổi phía kiểm tra**, không chỉ sửa docx); thêm tests/test_docs.py | Thiết kế cũ đã được thay | Tái lập |
| n | KE_HOACH_THUC_TE_2026-10-08 | Được thay bằng KE_HOACH_CHI_TIET_SINH_VIEN (2 kịch bản giờ) | Cần lịch theo ngày | Khả thi ↑ |

Không đổi: hàng "Xác nhận của CBHD / 15/09/2026"; các file evidence; examples.json; PDF và bản dịch (chỉ báo vấn đề bản quyền).
