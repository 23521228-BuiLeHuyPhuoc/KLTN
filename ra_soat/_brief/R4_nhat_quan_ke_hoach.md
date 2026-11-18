# R4 · Tính nhất quán nội bộ của kế hoạch và sổ sách

Báo cáo ghi vào: `ra_soat/carbon/R4_nhat_quan_ke_hoach.md` (mã phát hiện R4-01, R4-02...).

## Đọc

- **Toàn bộ** `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md` (đọc hết, theo từng khúc nếu cần).
- **Toàn bộ** `luan_van/nhat_ky.md`.
- `git log --date=short --pretty=format:"%h %ad %s" -200` và khi cần `git show --stat <mã>` (chỉ đọc).
- `README.md`, `data/THE_DU_LIEU.md`, `data/huong_dan_gan_nhan.md` (để đối chiếu T4).

## Việc phải kiểm

1. **Ô đánh dấu so với thực tế.** So ba nguồn: danh sách bước ở đầu tệp (dòng 15–86), ô `- [ ]`/`- [x]` trong từng bước, và thực tế (nhật ký, git log, tệp có trong repo). Lập bảng: bước nào đã làm mà chưa tick, bước nào tick mà chưa đạt "Xong khi", bước nào đầu tệp và thân bài lệch nhau.
2. **Con số và quyết định cũ còn sót.** Nhật ký ghi nhiều quyết định đổi quy mô hay cách làm (ví dụ 12 → 8 bài mỗi mẫu, 120 → 80 bài, khảo sát 20–30 hay 5–10 người, người gán thứ hai → lượt 3 tự gán lại, mốc điểm dừng, ngưỡng, LLM dùng cho trích xuất). Với mỗi quyết định, grep mọi chỗ trong kế hoạch còn ghi con số hay cách làm cũ mà không có ghi chú "Sửa ngày…". Liệt kê đủ từng dòng.
3. **Mâu thuẫn giữa các phần.** Cùng một thông tin (ngày, cỡ mẫu, định nghĩa nhãn, ngưỡng, k của BM25, số trường, tên tệp, tên đối chứng, chỉ số) ghi khác nhau ở các bước, ở T1–T16, ở `huong_dan_gan_nhan.md`, ở `THE_DU_LIEU.md`.
4. **Ngày và thứ tự phụ thuộc.** Ngày trong danh sách đầu tệp, trong tiêu đề từng bước, trong T2 (lịch, biểu đồ thời gian) có khớp không? Có bước dùng kết quả của một bước làm sau nó không? Thứ ghi kèm ngày (ví dụ "Thứ Sáu 27/11") có đúng lịch năm 2026 không?
5. **Đường dẫn và liên kết hỏng.** Mọi đường dẫn tệp được nhắc trong kế hoạch: tệp có tồn tại trong repo không (trừ tệp dự kiến làm sau, ghi rõ là dự kiến)? Neo `#b01`, `#t4-2`... có đích không?
6. **Quyết định trong nhật ký chưa vào kế hoạch.** Các QĐ (QĐ1, QĐ2...) và quyết định khác trong nhật ký: đã phản ánh vào phần chính của kế hoạch và hướng dẫn chưa?
7. **Thông tin lỗi thời ở đầu tệp và T1** (ví dụ "Cập nhật lần cuối", "Tình trạng", "Hôm nay bắt đầu ở Bước 1").
8. **Các câu hỏi còn treo** ghi trong nhật ký hay T10 (ví dụ "có cho chọn lại ngưỡng 1% ở Bước 33 không") đã được chốt chưa, chốt ở đâu.
