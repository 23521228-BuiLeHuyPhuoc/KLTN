# Định vị đề tài, tính mới và đối chiếu tiêu chí chấm (08/10/2026, cập nhật 10/2026)

Tài liệu do AI (Claude) soạn để sinh viên và GVHD xem xét. Mọi lựa chọn đều là **DỰ THẢO — cần GVHD xác nhận**.

## 1. Tiêu chí chấm: đã tìm được gì

**ĐÃ KIỂM (mở trang ngày 08/10/2026):**
- [Thông báo đăng ký KLTN HK1 2026–2027](https://nc.uit.edu.vn/giao-vu/thong-bao-v-v-dang-ky-kltn-hk1-nam-hoc-2026-2027.html): đăng ký và nộp đề cương 10–15/09/2026. Trang **không** nêu mốc báo cáo tiến độ, nộp khóa luận hay bảo vệ, và không có tiêu chí chấm hay quy định về AI.
- [Mẫu đề cương chi tiết Khoa MMT&TT](https://nc.uit.edu.vn/wp-content/uploads/2025/09/mau_DeCuongChiTiet_Khoa-MMT_2025.docx) yêu cầu các mục: mục tiêu, phạm vi, đối tượng, phương pháp, kết quả mong đợi, kế hoạch và phân công, tài liệu tham khảo theo IEEE.
- [Kế hoạch bảo vệ HK2 2025–2026](https://nc.uit.edu.vn/giao-vu/ke-hoach-to-chuc-bao-ve-khoa-luan-tot-nghiep-hk2-nam-hoc-2025-2026.html): nộp PDF và Word để kiểm tra đạo văn, gặp GV phản biện, bảo vệ trước hội đồng, nộp bản cuối sau bảo vệ. Trang không có phiếu chấm.

**CHƯA XÁC MINH:** phiếu chấm và trọng số điểm của GVHD, phản biện và hội đồng; hạn nộp và ngày bảo vệ của HK1 2026–2027. Cần làm: hỏi GVHD hoặc Văn phòng Khoa (E8.2, info.nc@uit.edu.vn) để xin phiếu chấm và lịch đúng kỳ.

**GIẢ ĐỊNH:** các tiêu chí học thuật thông dụng dưới đây. Đây không phải rubric của Khoa.

| Tiêu chí (giả định) | Kế hoạch đáp ứng thế nào | Minh chứng sẽ có |
|---|---|---|
| Đủ các mục theo mẫu đề cương (ĐÃ KIỂM) | HuP_4 có đủ mục tiêu M1–M5, phạm vi, đối tượng, phương pháp, kết quả, kế hoạch và tham khảo IEEE | Docx; `update_thesis_docs.py --check` |
| Bài toán rõ, có ý nghĩa | Kiểm chứng phát biểu thông số có điều kiện trong quảng cáo LLM | Chương 1; ví dụ EX-10, EX-18 |
| Tổng quan tài liệu | 11 tài liệu, có số liệu đối chiếu trang PDF | Bảng HuP_3 §3.1; `check_paper_facts.py` |
| Tính mới có giới hạn | Đóng góp C1–C3 (mục 2) | Dữ liệu, đặc tả, kiểm thử, bảng E3 |
| Phương pháp đúng | Chia tập theo họ, khóa trước test, cùng hướng dẫn cho mọi bản, người gán thứ hai | GIAO_THUC; mã băm; log |
| Thực nghiệm và phân tích | FAR, Recall Supported, mẫu số, từng họ, cluster bootstrap, phân tích lỗi | Bảng Gate 5 |
| Trung thực về giới hạn | Không end-to-end, NEI theo corpus, RQ3 thăm dò, khai báo AI | Chương kết luận; phụ lục AI |
| Khả thi và đúng hạn | MVP 120/12, có đường cắt giảm | KE_HOACH_CHI_TIET_SINH_VIEN |
| Tái lập | run_manifest, prompt có hash, README | Gói bàn giao |
| Trình bày và bảo vệ | Theo Phụ lục 2 của Khoa; chuẩn bị câu hỏi | CAU_HOI_PHAN_BIEN_DU_KIEN |

## 2. Tính mới: 3 đóng góp kiểm chứng được

Khảo sát nhanh trên web ngày 08/10/2026 chỉ tìm thấy hướng dẫn thực hành và [SynthAVE](https://arxiv.org/pdf/2607.07469) (3 phán quyết cho thuộc tính sản phẩm). Tôi chưa đọc kỹ bài này. Tôi không tìm thấy công trình nào về phát biểu thông số **có điều kiện** trong quảng cáo tiếng Việt, nhưng tìm kiếm chưa hệ thống, nên đây chỉ là **CHƯA XÁC MINH**.

| Đóng góp | Bằng chứng sẽ nộp | Rủi ro bị phản biện | Nếu kết quả âm / không đạt |
|---|---|---|---|
| C1. Bộ dữ liệu nhỏ có provenance: ordinary_llm tách khỏi controlled_variant, có search_log cho NEI, có kiểm độ tin cậy nhãn | Dữ liệu và log sinh; κ trước hòa giải trên 40 claim (phương án A) hoặc tự nhất quán 20% (phương án B) — GIAO_THUC §3 | "Quá nhỏ"; "nhãn do một người làm" | Báo đúng số lượng; nếu không có người thứ hai thì chỉ nêu tự nhất quán và hạ C1 thành "bộ thử có quy trình" |
| C2. Đặc tả và cài đặt so sánh kiểu giá trị (x so với M, biên mở/đóng, gần đúng, phiên bản) cùng luật inherit_headline, có kiểm thử | QUY_TAC_ABC; `abc_reference.py`; bộ kiểm thử trong `tests/` | "Chỉ là luật thủ công"; "[1], [5] đã dùng luật" | Vẫn đứng được vì là đặc tả; kết hợp với phân tích lỗi để chỉ ra ca nào luật giúp và ca nào luật hại |
| C3. So sánh có kiểm soát P với B1 trên cùng hồ sơ, tách tác động của bước quyết định | TN2 (lượt 1 toàn test, lượt 2–3 trên m ≤ 30 claim), TN3 ablation, TN4 hồ sơ chuẩn; ΔFAR = FAR_P − FAR_B1 kèm tử số, mẫu số và cặp bất đồng (sổ tay mục 6) | "4 họ test không đủ" | Báo là thăm dò. Nếu P không tốt hơn thì phân tích nguyên nhân (trích xuất hay luật, qua TN4 và mã lỗi); kết quả âm vẫn hợp lệ |

**KHÔNG được tuyên bố:** "đầu tiên" hay "chưa ai làm"; "có ý nghĩa thống kê"; "hệ thống end-to-end"; "tổng quát cho mọi tai nghe hoặc mọi hãng"; "hãng không công bố" (chỉ có thể nói "không tìm thấy trong corpus X"); "dùng Python ra nhãn là tính mới"; "bộ benchmark"; gọi kết quả tự gán lại là đồng thuận giữa hai người.

**Kế hoạch B:** nếu đến 04/12 chưa đủ 120 phát biểu, hoặc API không ổn định, thì thu hẹp thành "đặc tả A–B–C + bộ thử + so sánh trên N phát biểu thực có". Trọng tâm chuyển sang C2 và phân tích lỗi, C3 chỉ còn mô tả. Phương án này phải báo GVHD trước Gate 4.
