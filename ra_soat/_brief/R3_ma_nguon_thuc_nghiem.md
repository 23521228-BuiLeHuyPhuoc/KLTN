# R3 · Mã nguồn, kiểm thử và kết quả thực nghiệm

Báo cáo ghi vào: `ra_soat/carbon/R3_ma_nguon_thuc_nghiem.md` (mã phát hiện R3-01, R3-02...).

Phạm vi: Bước 2, 11, 14, 15, 21, 22, 27 và phần đã bắt đầu của Bước 28–30, đối chiếu với đặc tả T5 (T5.1–T5.9), T6.1–T6.3, T12 trong `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md`.

## Đọc

- Toàn bộ `src/kiemchung/` (đọc kỹ `quyet_dinh*`, `trich_xuat*`, `chuan_hoa*`, `truy_hoi*`, `neo_nguon*`, `llm.py`, `doi_chung/`), các tệp trong `scripts/`, `tests/`.
- `luan_van/buoc22_thiet_ke_trich_xuat.md`, `luan_van/buoc27_thiet_ke_quyet_dinh.md`, `luan_van/buoc29_30_thiet_ke_cau_lenh.md`.
- `ket_qua/*.md`, `ket_qua/trich_xuat/thong_ke_*.md`, `ket_qua/trich_xuat/thu_*.jsonl` (kết quả thử trích xuất mới nhất, chưa commit), `ket_qua/b0_*.md`, `ket_qua/recall_*.md`.
- Các mục của `luan_van/nhat_ky.md` về những bước trên.

## Được chạy

- `.venv/Scripts/python.exe -m pytest -q` (ghi số test đạt/hỏng; test hỏng thì ghi tên và lỗi chính).
- Đoạn Python chỉ đọc để tính lại số liệu (in ra màn hình). **Không** chạy script có gọi LLM, không ghi vào `data/`, `ket_qua/` hay cache.

## Việc phải kiểm

1. **Mã khớp đặc tả không.** Bộ 7 trường (T5.1), BM25 và k (T5.2), neo nguồn và kiểm tra đầy đủ (T5.3), chuẩn hóa (T5.4), bộ quyết định A–D đúng thứ tự cố định và đúng các luật QĐ (T5.5, hướng dẫn gán nhãn, nhật ký), sinh lý do không để LLM viết tự do (T5.6), cấu hình (T5.7). Ghi mọi chỗ mã làm khác đặc tả hoặc khác hướng dẫn gán nhãn.
2. **Lỗi logic.** Tìm lỗi thật trong bộ quyết định và chuẩn hóa: xử lý "lên đến", so sánh "thuận lợi hơn/kém thuận lợi hơn" theo chiều của từng thuộc tính (thời lượng pin càng lớn càng tốt, thời gian sạc càng nhỏ càng tốt...), đổi đơn vị, khoảng giá trị, nhiều giá trị công bố, điều kiện thiếu một phần, tài liệu mâu thuẫn, so sánh số thực. Với mỗi lỗi, nêu một đầu vào cụ thể cho ra nhãn sai và nhãn đúng phải là gì (theo hướng dẫn).
3. **Rò rỉ nhãn.** Mã của P hoặc đối chứng có đọc nhãn chuẩn, đọc dữ liệu tập kiểm tra, hay có luật/từ khóa được chỉnh riêng theo từng tuyên bố của tập phát triển (overfit kiểu "if mã == ...")?
4. **Công bằng đối chứng.** B0 (và B1–B3 nếu đã có): cùng truy hồi, cùng k, cùng LLM, cùng đầu vào như P không? Prompt có thiên lệch không?
5. **Kiểm thử.** Chạy pytest. Test có thực sự kiểm luật hay chỉ kiểm cho có (ví dụ test so với chính đầu ra của hàm)? Luật nào của bộ quyết định chưa có test?
6. **Số liệu báo cáo có đúng không.** Tính lại từ tệp thô ít nhất: Recall@k trong `ket_qua/recall_*.md`, kết quả B0 trong `ket_qua/b0_*.md`, thống kê thử trích xuất trong `ket_qua/trich_xuat/thong_ke_*.md`. Ghi chỗ lệch.
7. **Tái lập.** Có ghi model, phiên bản, nhiệt độ, seed, k, thời điểm chạy, cache không? Chạy lại có ra cùng kết quả không (xét theo mã, không chạy LLM)?
8. **Bước 22 đang làm** (thử trích xuất với `gpt-oss-120b`, k=5): kết quả thử có vấn đề gì (tỷ lệ trường bị bỏ do neo nguồn, lỗi JSON, điều kiện bị sót)? Lựa chọn model có hợp với kế hoạch và quy tắc công bằng T6.2 không?
9. **Mã còn thiếu so với kế hoạch** cho Mốc 3 (27/11): khối nào chưa có, ước lượng khối lượng còn lại.
