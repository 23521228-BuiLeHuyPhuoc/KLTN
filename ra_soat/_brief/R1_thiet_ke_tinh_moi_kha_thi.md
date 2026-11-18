# R1 · Thiết kế nghiên cứu, tính mới, tính thực tiễn, khả năng kịp hạn

Báo cáo ghi vào: `ra_soat/carbon/R1_thiet_ke_tinh_moi_kha_thi.md` (mã phát hiện R1-01, R1-02...).

## Đọc

- `de_cuong/nguon/de_cuong_da_nop.txt` (toàn bộ).
- `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md`: đầu tệp và danh sách bước (dòng 1–86); toàn bộ phần Tra cứu từ `## Tra cứu` (khoảng dòng 1241) đến hết, đặc biệt T1, T2, T6, T9, T10, T11, T14, T15; các bước 28–47 (việc còn lại).
- `báo/TOM_TAT_16_BAI_BAO.md`, `luan_van/ghi_chu_tai_lieu.md`, `luan_van/tai_lieu_tham_khao.md`.
- `luan_van/chuong_1.md`, `luan_van/chuong_2.md`, `luan_van/chuong_3.md`.
- Số liệu thực tế: `data/THE_DU_LIEU.md`, `ket_qua/bo_thu/thong_ke.md`, `ket_qua/b0_luot2.md`, `ket_qua/recall_luot2.md`, `ket_qua/khao_sat_cach_hieu.md`, và các mục mới nhất của `luan_van/nhat_ky.md`. Tự đếm số tuyên bố và phân bố nhãn theo tập từ `data/tuyen_bo/*.jsonl`, `data/nhan/*.jsonl`, `data/chia_tap.json` (nhớ luật mù ở bối cảnh chung: chỉ nêu số tổng hợp).

## Câu hỏi phải trả lời (mỗi câu ít nhất một kết luận, có bằng chứng)

1. **Tính mới.** So với 16 bài báo đã khảo sát, ba ý "Tính mới" ở T1.5 có thật mới không? Ý nào phóng đại, ý nào dễ bị hội đồng bác ("chỉ là luật thủ công", "chỉ là pipeline RAG + rule", "MeasEval đã có")? Câu trả lời mẫu về tính mới trong T1.5 và T11 có đứng vững không?
2. **Vấn đề và giải pháp có khớp nhau không.** Bài toán ở T1.1–T1.2 có được đo đúng bằng CH1–CH3 và chỉ số ở T6.4 không? Có câu hỏi nghiên cứu nào không trả lời được bằng thiết kế hiện tại?
3. **Cỡ mẫu và thống kê.** Với số tuyên bố thực tế (tự đếm) ở tập phát triển và dự kiến ở tập kiểm tra, số tuyên bố Lệch điều kiện và Sai trong tập kiểm tra là bao nhiêu? Kiểm định và khoảng tin cậy ở T6.5–T6.6 có đủ lực (power) để kết luận H1–H3 không? Tiêu chí "Recall nhãn Đúng không thấp hơn quá 5 điểm phần trăm" có đo được với cỡ mẫu đó không? Ước lượng độ rộng KTC 95% cho FAR và F1 Lệch, ghi cách tính.
4. **Công bằng của đối chứng.** B0–B4 và P−ĐK, P−NN ở T6.1–T6.2 có so sánh công bằng không (cùng LLM, cùng truy hồi, cùng k, cùng bộ thông số)? Có đối chứng nào là "người rơm" dễ thắng? Có thiếu đối chứng hiển nhiên mà hội đồng sẽ hỏi (ví dụ LLM mạnh đọc toàn bộ tài liệu, NLI có sẵn)?
5. **Độ tin cậy nhãn.** Một người gán, nhãn lượt 2 do AI gán rồi người duyệt, lượt 3 là tự gán lại. Đây có phải điểm yếu nghiêm trọng trước hội đồng không? Kế hoạch (T6, T9, T11, Bước 32) đã xử lý đủ chưa? Đề xuất cách giảm rủi ro khả thi trong 6 tuần.
6. **Tính thực tiễn và tổng quát.** Phạm vi 3 nhóm sản phẩm, 12 mẫu, tài liệu chính hãng, tiếng Việt: kết quả có tổng quát được không, giới hạn đã ghi rõ chưa? Tích hợp CopyPro (T7, Bước 34, 40, 41) có đủ chứng minh tính thực tiễn không (ví dụ có đo thời gian chạy, chi phí, người dùng thật dùng thử)?
7. **Khả năng kịp hạn.** Hôm nay 18/11/2026. Liệt kê các bước chưa xong (tự kiểm theo nhật ký, git log và tệp thực có, không chỉ tin ô đánh dấu). So với ngày ghi trong kế hoạch, đang chậm bao nhiêu ngày? Mốc 3 (27/11) và hạn 31/12 có khả thi không? T9.2 (thứ tự rút gọn khi chậm) đã nên kích hoạt chưa? Bước nào nên cắt hay gộp?
8. **Chuẩn bị bảo vệ.** T11 có thiếu câu hỏi phản biện hiểm nào không (về nhãn, về AI hỗ trợ làm nhãn và mã, về tính mới, về cỡ mẫu, về rò rỉ dữ liệu, về việc LLM đánh giá LLM)? Khai báo việc dùng AI trong khóa luận đã có kế hoạch chưa?
9. **Thiếu cần bổ sung.** Những gì một khóa luận loại này thường phải có mà kế hoạch chưa có hoặc mờ (ví dụ phân tích lỗi định tính, chi phí, đạo đức, thẻ dữ liệu, tái lập, giới hạn).
10. **Đề cương có chỗ nào sai hoặc nay đã không còn đúng** so với cách làm thực tế (đổi quy mô, đổi người gán...), mà kế hoạch hay chương 1–3 vẫn ghi theo đề cương cũ?
