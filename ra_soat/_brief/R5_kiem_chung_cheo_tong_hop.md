# R5 · Kiểm chứng chéo và tổng hợp bốn báo cáo rà soát

Báo cáo ghi vào: `ra_soat/carbon/R5_tong_hop_kiem_chung.md`.

Bốn lượt rà soát trước (do các phiên khác viết) nằm ở:
`ra_soat/carbon/R1_thiet_ke_tinh_moi_kha_thi.md`, `ra_soat/carbon/R2_du_lieu_nhan.md`, `ra_soat/carbon/R3_ma_nguon_thuc_nghiem.md`, `ra_soat/carbon/R4_nhat_quan_ke_hoach.md`.

Vai trò của bạn: **người kiểm chứng hoài nghi**. Người rà soát trước có thể đọc nhầm dòng, trích sai, đếm sai, hiểu sai hướng dẫn, hoặc coi một lựa chọn có chủ đích (đã ghi lý do trong nhật ký) là lỗi. Đừng tin báo cáo; tin tệp nguồn.

## Việc phải làm

1. Đọc cả bốn báo cáo.
2. **Gộp trùng:** cùng một vấn đề nêu ở nhiều báo cáo thì gộp thành một mục, giữ mọi mã gốc (ví dụ "R2-04, R4-07").
3. **Kiểm chứng từng phát hiện** (kể cả mục "Nghi vấn chưa kiểm chứng"):
   - Mở đúng `đường_dẫn:dòng` được dẫn, xác nhận câu trích có thật và đúng ngữ cảnh.
   - Con số: tự đếm/tính lại bằng Python chỉ đọc.
   - Tìm trong `luan_van/nhat_ky.md` và kế hoạch xem vấn đề đã được biết, đã có quyết định hay ghi chú "Sửa ngày…" chưa. Nếu đã được xử lý có chủ đích và hợp lý thì không phải lỗi.
   - Kết luận một trong ba: **XÁC NHẬN** (đúng là vấn đề, có bằng chứng), **BÁC BỎ** (sai sự thật, đã xử lý, hoặc là lựa chọn có lý do), **CHƯA CHẮC** (cần người thực hiện quyết định hoặc cần dữ liệu không có).
   - Được chỉnh lại mức độ nếu người rà soát trước đánh giá quá cao hay quá thấp; ghi lý do.
4. Nếu trong lúc kiểm chứng bạn thấy vấn đề **NGHIÊM TRỌNG hoặc CAO** mà bốn báo cáo bỏ sót, thêm vào với mã R5-01, R5-02... (theo đúng chuẩn bằng chứng).

## Định dạng báo cáo

```
# Tổng hợp và kiểm chứng rà soát (R5)
Ngày: 18/11/2026 · Người kiểm chứng: Gemini 4 Carbon

## Tóm tắt
<5–8 câu: các vấn đề XÁC NHẬN đáng lo nhất, theo thứ tự ưu tiên>

## Thống kê
<số phát hiện gốc mỗi báo cáo; sau gộp; số XÁC NHẬN / BÁC BỎ / CHƯA CHẮC theo mức độ>

## A. Đã xác nhận (xếp theo mức độ giảm dần)
### [T-01] <Tiêu đề> · <MỨC ĐỘ> · mã gốc: R?-??
- **Loại:** ...
- **Chỗ:** `đường_dẫn:dòng`
- **Bằng chứng đã tự kiểm lại:** ...
- **Vì sao là vấn đề:** ...
- **Đề xuất sửa (chưa thực hiện):** ...
- **Ảnh hưởng tới kế hoạch:** bước nào, mốc nào phải đổi

## B. Chưa chắc, cần người thực hiện quyết định
<cùng cấu trúc, thêm dòng "Câu hỏi cho người thực hiện:">

## C. Đã bác bỏ
| Mã gốc | Tiêu đề | Lý do bác bỏ (kèm `đường_dẫn:dòng`) |

## D. Gợi ý thứ tự xử lý
<danh sách ngắn: sửa gì trước, vì liên quan mốc 27/11 và hạn 31/12>
```

Luật cứng ở `ra_soat/_brief/00_boi_canh_chung.md` vẫn áp dụng đầy đủ: chỉ ghi đúng tệp báo cáo này, không sửa tệp nào khác, không gọi LLM API, giữ tính mù lượt 3 (nếu báo cáo gốc lỡ ghi nhãn của tuyên bố bộ thử theo mã, **không chép lại**, và ghi một dòng cảnh báo "báo cáo Rx có thể đã lộ nhãn bộ thử ở mục ...").
