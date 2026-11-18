# R2 · Dữ liệu và nhãn của các bước đã làm

Báo cáo ghi vào: `ra_soat/carbon/R2_du_lieu_nhan.md` (mã phát hiện R2-01, R2-02...).

Phạm vi: các bước tạo dữ liệu đã làm hoặc đang làm: Bước 4–13, 16, 18–21, 26 (xem chi tiết từng bước và dòng "Xong khi" trong `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md`), cùng T3.2 (mã định danh), T3.3 (thiết lập sinh quảng cáo), T3.4 (định dạng dữ liệu), T4 (hướng dẫn gán nhãn), T4.7 (cặp tối thiểu), T6.3 (chia tập).

## Đọc

- `data/mau_san_pham.csv`, `data/chia_tap.json`, `data/kiem_tra_nguon_buoc4.json`, `data/THE_DU_LIEU.md`.
- `data/nguon/` (liệt kê, mở vài tệp), `data/kiem_doan_buoc7.md`, `data/kiem_doan_buoc7_lan2.md`, `data/kiem_bo_so_chu_thich.md`.
- `data/cau_hinh/*` (tệp YAML và `bao_phu_dieu_kien.md`).
- `data/quang_cao/` (liệt kê, đếm, mở mẫu), `data/tuyen_bo/*.jsonl` và các tệp `.md` trong đó.
- `data/nhan/*.jsonl`, `data/nhan/*.md`, `data/huong_dan_gan_nhan.md`.
- `luan_van/nhat_ky.md` (các mục về Bước 4–26), `luan_van/buoc16_de_xuat_huong_dan_ban2.md`.

## Việc phải kiểm (tự đếm, tự tính bằng Python chỉ đọc)

1. **Con số khớp nhau không.** Số mẫu, số mẫu mỗi tập, số bài quảng cáo (theo mẫu, theo LLM, theo loại bài `ten`/`ten_thong_so`), số tuyên bố, phân bố nhãn theo tập: so số đếm thật với số ghi trong kế hoạch, `THE_DU_LIEU.md`, nhật ký, chương 3. Ghi mọi chỗ lệch.
2. **Chia tập.** Tính sha256 của `data/mau_san_pham.csv` và so với `chia_tap.json`. Kiểm không có tuyên bố hay quảng cáo nào của mẫu tập kiểm tra nằm trong tệp/nhãn của tập phát triển và ngược lại. Kiểm bộ thử thuộc tập phát triển như quy tắc ghi.
3. **Định dạng và toàn vẹn tham chiếu.** Bản ghi thật có đúng các trường ở T3.4 không? Mã có trùng không, có đúng mẫu T3.2 không? Mỗi tuyên bố trỏ tới quảng cáo có thật? Mỗi bằng chứng hay đoạn nguồn trong nhãn trỏ tới đoạn có thật trong `data/nguon/`, và câu trích có nằm nguyên văn trong đoạn đó không? Nhãn có giá trị ngoài 4 lớp không?
4. **Nhãn có theo đúng hướng dẫn không** (chỉ dùng tuyên bố của **tập phát triển chính**, không dùng bộ thử để trích dẫn theo mã, xem luật mù). Lấy mẫu khoảng 15–20 tuyên bố của tập phát triển, tự áp hướng dẫn `data/huong_dan_gan_nhan.md` và T4.3 (thứ tự quyết định), đối chiếu với nhãn đã chốt. Ghi những ca bạn cho là gán sai hoặc hướng dẫn mơ hồ khiến hai người có thể gán khác nhau, kèm lý do theo đúng mục của hướng dẫn.
5. **Hướng dẫn gán nhãn tự nó có chỗ mâu thuẫn, chồng lấn hay lỗ hổng không** (hai luật cùng áp được nhưng ra nhãn khác nhau; trường hợp không luật nào phủ). Các quyết định QĐ trong nhật ký đã đưa vào hướng dẫn chưa?
6. **Phân bố nhãn có đủ để đánh giá không.** Số Lệch điều kiện, Sai, Chưa đủ thông tin ở mỗi tập có đủ để tính F1 Lệch và FAR có ý nghĩa không? Có nhóm sản phẩm hay loại điều kiện nào gần như không có mẫu?
7. **Tệp cấu hình điều kiện** có phủ các thuộc tính thực sự xuất hiện trong tuyên bố không? Có thuộc tính trong tuyên bố mà cấu hình không có (bị lọc mất), hoặc cấu hình ghi loại điều kiện không khớp tài liệu nguồn?
8. **Sinh quảng cáo** (T3.3, Bước 11, 12, 18): thiết lập thật (LLM, nhiệt độ, prompt, số bài mỗi mẫu, xoay vòng loại bài) có đúng như kế hoạch và nhật ký ghi không? Có ghi lại đủ để tái lập không?
9. **Dòng "Xong khi"** của các bước dữ liệu đã đánh dấu xong: điều kiện có thật sự đạt không?
10. **Khai báo ảnh hưởng của AI** lên nhãn (tuyên bố nào có gợi ý của Claude) đã được ghi lại ở đâu, có đủ để khóa luận khai báo không?
