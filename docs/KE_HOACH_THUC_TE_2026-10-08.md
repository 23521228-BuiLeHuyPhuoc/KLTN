# Kế hoạch thực tế 08/10–31/12/2026 (DỰ THẢO — cần sinh viên/GVHD xác nhận)

Trạng thái xuất phát (ĐÃ KIỂM trong repo ngày 08/10): chưa có quảng cáo LLM nào có log; chưa có cấu hình máy/API; chưa có code BM25/B0/B1/P; đã có hướng dẫn nhãn, đặc tả A–B–C, 23 ví dụ minh họa, hàm tham chiếu A–B–C và 27 test. Số giờ dưới đây là **ước lượng của người rà soát (SUY LUẬN)**; sinh viên điền quỹ giờ thực: [SINH VIÊN ĐIỀN: giờ/tuần].

## MVP (bắt buộc) và tùy chọn

- **MVP:** dữ liệu 120 claim / 12 họ có provenance; hướng dẫn nhãn khóa; BM25 + k_eff; trích xuất JSON; B0, B1, P chạy E3 trên test, 3 lượt; FAR, Recall Supported, Macro-F1, recall@k; người thứ hai 30 claim (hoặc ghi rõ thiếu).
- **Tùy chọn (chỉ khi Gate 4 đúng hạn):** 180 claim; P−A(bộ phận), P−B (ablation: tắt một thành phần để đo đóng góp); E1/E2; website; tách claim tự động.

## Lịch

| Tuần | Việc | Giờ ước lượng | Phụ thuộc | Đầu ra kiểm được |
|---|---|---:|---|---|
| 08–15/10 | Chốt D1–D5, D7; chọn 1–2 mô hình + nhà cung cấp; viết prompt sinh quảng cáo; **lô 0**: 2 họ × 5 quảng cáo; tách claim; gán nhãn 5 mẫu đầu có bấm giờ | 14 | Khóa API mới (sau khi thu hồi khóa lộ) | 10 file `llm_ad_sample.json`, bảng phút/claim, D1–D7 có chữ ký GVHD |
| 16–22/10 | Thu nguồn + snapshot 6 họ dev; gán nhãn pilot; mời người thứ hai | 14 | Lô 0, hướng dẫn khóa | ≥ 30 claim có nhãn + search_log cho NEI |
| 23–31/10 | Pilot 45–60 claim / 6 họ; BM25 + k_eff; B0 và P tối thiểu chạy trên pilot | 16 | Pilot, `abc_reference.py` làm chuẩn so | Log chạy, recall@k k=3/5/8, quyết định quy mô |
| 01–20/11 | Thu/gán đủ 120 claim (val 2 họ, test 4 họ); trích xuất JSON; B1; P đầy đủ qua test luật | 36 | Quy mô Gate 2 | Dữ liệu khóa hash, P qua `tests/test_abc.py` |
| 21–30/11 | Người thứ hai gán 30 claim; khóa prompt/k/mô hình; smoke test val | 14 | Dữ liệu khóa | Kappa trước hòa giải, manifest Gate 4 |
| 01–15/12 | Chạy E3 × 3 lượt; tính chỉ số + cluster bootstrap; phân tích lỗi | 18 | Gate 4 | Bảng B0/B1/P, log, khoảng tin cậy |
| 16–31/12 | Viết luận văn, bàn giao | 30 | Gate 5 | Bản nộp |

## Mốc kiểm tra

- **15/10 (pilot nhỏ):** đạt nếu có 10 quảng cáo LLM có log đầy đủ và số đo phút/claim trên 5 mẫu đầu. Từ số đo: số claim gán được trước 20/11 ≈ (giờ gán nhãn còn lại × 60) / (phút/claim). Nếu < 120 → giữ 120/12 và bỏ toàn bộ tùy chọn.
- **31/10 (pilot đủ):** đạt nếu có ≥ 45 claim / 6 họ có nhãn và B0, P chạy hết pilot không lỗi cản trở. Nếu không: báo GVHD, giảm test xuống mức tối thiểu và ghi hạn chế.

## Rủi ro chính

| Rủi ro | Dấu hiệu | Hành động |
|---|---|---|
| Khóa API lộ bị lạm dụng / bị khóa | Hóa đơn lạ, lỗi 401 | Thu hồi ngay, tạo khóa mới, không commit `.env` |
| Năng suất gán nhãn thấp | > 6 phút/claim ở lô 0 | Giữ 120/12, bỏ tùy chọn |
| LLM ít tạo claim sai tự nhiên | Lô 0 gần như toàn Supported | Bổ sung `controlled_variant`, giữ ≥ 50% thông thường |
| Không có người thứ hai | Chưa nhận lời đến 31/10 | Ghi hạn chế, không thay bằng AI |
| Test 4 họ quá ít | CI ΔFAR chứa 0 | Báo thăm dò (D6) |
