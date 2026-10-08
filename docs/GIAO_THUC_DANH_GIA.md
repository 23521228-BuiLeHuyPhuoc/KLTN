# Giao thức dữ liệu và đánh giá — bản 10/2026 (dự thảo, khóa trước test)

Giao thức này ghi **cái gì được cố định trước khi chạy test và cái gì phải báo**. Cách làm từng bước nằm trong [sổ tay](KE_HOACH_CHI_TIET_SINH_VIEN.md) (mã công việc W…, thí nghiệm TN…). Khi khóa (sổ tay W7.3), SHA-256 của file này được ghi vào `data/locks/protocol_lock.json`; sau đó mọi thay đổi phải tăng phiên bản và ghi lý do. Bản 08/10/2026 đã được thay thế; thay đổi chính xem [bảng đối chiếu](DOI_CHIEU_THAY_DOI_KE_HOACH.md).

Trạng thái: chưa có dữ liệu thí nghiệm, chưa có người gán thứ hai, chưa có lượt chạy B0/B1/P nào.

## 1. Phạm vi kết luận

1. Đơn vị đánh giá là **phát biểu đã tách thủ công** kèm **mã sản phẩm đã biết**. Không đánh giá tách claim tự động hay tự nhận diện sản phẩm; kết luận không phải “end-to-end”.
2. Nhãn nói về **mức được tài liệu chính thức trong corpus đã khóa hỗ trợ**, không về hiệu năng thực tế. NEI là tương đối với corpus.
3. Thiết lập truy hồi chính lọc theo sản phẩm; kết quả không chứng minh khả năng chọn đúng sản phẩm trong kho mở (chỉ TN5, nếu chạy, mới đo phần này trong kho cùng hãng).

## 2. Dữ liệu

- **Corpus:** tài liệu chính thức (trang thông số, hướng dẫn sử dụng, trang hỗ trợ/PDF) của từng họ, lưu snapshot và SHA-256, ghi URL, thị trường, ngôn ngữ, thời điểm chụp. Thị trường thay thế chỉ dùng khi đúng mẫu sản phẩm và được ghi `market_substitute`. Corpus được khóa phiên bản trước test.
- **`ordinary_llm`:** quảng cáo sinh bằng mô hình G theo [mẫu prompt](../templates/ad_prompts.json) với hai điều kiện `g1_name_only`, `g2_with_spec`, không có yêu cầu tạo lỗi; giữ nguyên văn, prompt đã render, mã mô hình, tham số, thời điểm. Quy tắc dừng dựa trên **số claim hợp lệ**, số lô và ngân sách, không dựa trên nhãn hay dự đoán. Mọi output được giữ; lỗi kỹ thuật ghi `exclusion`.
- **`controlled_variant`:** cặp tối thiểu sửa đúng một yếu tố của câu cha Supported (COND, PART, ROLE, VAL, PROD, BOUND); lưu câu cha, loại thao tác, người sửa, thời điểm. Nhãn do người gán đọc nguồn, không suy từ thao tác.
- **`seed_manual`:** câu cha viết từ dòng thông số khi một thuộc tính không có câu cha Supported tự nhiên; chỉ dùng làm cha của biến thể, báo riêng.
- **Loại khỏi dữ liệu chính:** EX-01–23 (`unknown_legacy` và ca giả lập `SIM-*`), câu tự viết không có log, mọi fixture kiểm thử.
- Claim ngoài phạm vi (cảm tính, so sánh, thuộc tính khác) được gắn cờ với lý do cố định, không xóa, không thành nhãn thứ tư.

## 3. Nhãn

1. [HUONG_DAN_GAN_NHAN.md](HUONG_DAN_GAN_NHAN.md) v2 là tiêu chí ngữ nghĩa duy nhất cho người gán, B0, B1 và P (chính sách điều kiện `inherit_headline` v3, đọc vai trò con số, phạm vi xung đột theo thuộc tính, tổng hợp phép hội).
2. Người gán đọc toàn bộ corpus đã khóa; không đọc dự đoán của bất kỳ hệ thống nào; thứ tự gán xáo trộn, ẩn nhóm/thao tác khi có thể.
3. NEI-missing chỉ `final` khi có nhật ký tìm nguồn đủ ba loại nguồn (thông số, hướng dẫn, hỗ trợ/PDF) theo [mẫu](../templates/nei_search_log.json); thiếu bước → `pending_review`. Test không được còn `pending_review` khi khóa; ca loại bỏ phải báo số và lý do.
4. Kiểm độ tin cậy: phương án A — một người thứ hai gán độc lập 40 claim chọn bằng seed trước khi chạy hệ thống (phân tầng nhãn sơ bộ, nhóm, ≥ 4 họ, ≥ 15 claim test); báo đồng thuận và Cohen’s κ **trước hòa giải**, hòa giải bằng nguồn. Phương án B (không có người thứ hai) — tự gán lại 20% sau ≥ 7 ngày, báo là **tự nhất quán**. Không dùng AI thay người thứ hai.
5. Phát hiện thiếu quy định khi gán test: sửa hướng dẫn dựa trên lập luận ngữ nghĩa, tăng phiên bản, gán lại mọi tập bị ảnh hưởng, ghi trong luận văn rằng test đã ảnh hưởng tiêu chí. Không sửa luật P để khớp một ca test.

## 4. Chia tập và khóa

- Chia theo **họ**: cha, biến thể, câu gần trùng và họ dùng chung tài liệu nằm cùng tập. Họ pilot luôn ở dev. Chọn họ bằng seed và tiêu chí ghi trước (hãng, số thuộc tính có nguồn), không theo nhãn.
- **dev:** phát triển mọi thứ (chunker, k, prompt trích xuất, few-shot, từ điển mở rộng, chọn mô hình). **val:** chạy **một lần** với cấu hình đã khóa để phát hiện lỗi phần mềm/pipeline; không chỉnh theo điểm. **test:** chỉ chạy sau khóa.
- Khóa gồm: hướng dẫn, prompt (B0/B1, trích xuất, sinh), cấu hình mô hình/giải mã/k/chunker/query, splits, nhãn test, chunks, commit code, danh sách claim lặp (seed), danh sách mẫu phân tích lỗi (seed), bảng mã lỗi, chính sách lỗi/retry, ngân sách.

## 5. Phương pháp và công bằng

| Bản | Đầu vào dữ kiện | Ai quyết định |
|---|---|---|
| B0 | claim, product_context, top-k đoạn (văn bản, tiêu đề, chú thích, metadata nguồn) | LLM D + nguyên văn hướng dẫn chung |
| B1 | claim, product_context, **hồ sơ trích xuất của lượt đó** (`normalized_records_sha256`) | LLM D + cùng nguyên văn hướng dẫn |
| P | **cùng hồ sơ và hash với B1** | code A–B–C ([QUY_TAC_ABC.md](QUY_TAC_ABC.md)) |

- B0/B1 dùng cùng mô hình D, tham số giải mã, system prompt và SHA-256 hướng dẫn ([mẫu](../templates/eval_prompts.json), kiểm bằng `build_eval_prompts.py --check`). Prompt được lưu đủ; không cắt hướng dẫn khi quá ngữ cảnh (mô hình thiếu ngữ cảnh là cấu hình không hợp lệ). Few-shot nếu dùng lấy từ dev, giống nhau cho B0/B1.
- Payload chỉ chứa dữ kiện; trước mỗi lần gọi chạy `check_input_leak.py --kind <b0|b1|p|extract>` (danh sách cho phép, khóa cấm, chuỗi/mã lộ nhãn). PASS không chứng minh hết đường rò; vẫn đọc tay 10 payload mỗi lượt. Mã claim/đoạn là mã mờ; thứ tự claim xáo bằng seed.
- P–B1 là so sánh chính (cô lập cách quyết định). P–B0 khác cả biểu diễn nên chỉ tham khảo.

## 6. Truy hồi

Đoạn = dòng thông số + tiêu đề + chú thích. BM25 (k1 = 1,5, b = 0,75) trên đoạn của đúng họ; query là claim (giữ tên sản phẩm); token hóa giữ số thập phân, phiên bản, ký hiệu; từ điển Việt–Anh chỉ khi dev cho thấy giúp. k chọn trên dev (k nhỏ nhất có recall@k ≥ 0,9 trong {3, 5, 8}). Báo N, k_eff = min(k, N), recall@k tổng và riêng N ≤ k / N > k; NEI-missing không vào mẫu số; lỗi chia đoạn/thu nguồn được báo riêng với lỗi xếp hạng.

## 7. Thí nghiệm và lượt chạy

| TN | Nội dung | Lượt |
|---|---|---|
| TN1 | BM25 lọc sản phẩm trên test | 1 |
| TN2 | B0, B1, P trên toàn test; báo riêng `ordinary_llm` và tập chẩn đoán | lượt 1 toàn test; lượt 2, 3 trên m = min(30, n_test) claim chọn bằng seed khi khóa |
| TN3 | P−part, P−B, P−role, P−inherit trên hồ sơ lượt 1 | 1 (không gọi LLM) |
| TN4 | P và B1 trên hồ sơ chuẩn viết tay cho tập chẩn đoán test + câu cha | 1 |
| TN5 (nên có) | BM25 không lọc trên kho cùng hãng | 1 |
| TN6 (mở rộng) | B1, P với mô hình D thứ hai | 1 |

- Mỗi lượt TN2 có **trích xuất mới** (`extraction_run_id` mới, không dùng cache lượt trước); trong một lượt B1 và P dùng cùng hồ sơ. P tất định: không chạy lại P trên cùng hồ sơ để đo dao động.
- Lượt 1 là kết quả chính đã định trước. Báo từng lượt trên cùng m claim, min–max, tỷ lệ đổi nhãn; không chọn lượt tốt nhất, không coi 3 × m là mẫu độc lập.
- Manifest theo [templates/run_manifest.json](../templates/run_manifest.json): mô hình yêu cầu/trả về, nhà cung cấp, endpoint không chứa khóa, thời gian, giải mã, seed và trạng thái hỗ trợ, hash prompt/hướng dẫn/corpus/split/records, cache/retry, token, chi phí, độ trễ. Trường không biết ghi `unavailable` + lý do. Nhà cung cấp đổi mô hình giữa chừng → ghi và chạy lại đồng bộ.

## 8. Chỉ số, bất định và báo cáo

Định nghĩa và ví dụ tính: sổ tay mục 6.3. Bắt buộc báo: FAR (cùng FAR_R, FAR_NEI), Recall Supported, P/R/F1 từng nhãn, Macro-F1, ma trận nhầm lẫn (thêm cột ERROR), tỷ lệ dự đoán NEI, tỷ lệ chấp nhận nhầm theo loại thao tác, tỷ lệ lỗi kỹ thuật; luôn có tử/mẫu nguyên; mẫu số 0 → NA; mẫu số < 8 → “ít mẫu”.

Quy ước dấu: **ΔFAR = FAR_P − FAR_B1**, **ΔRecall_S = Recall_P − Recall_B1**; ΔFAR âm nghĩa là P chấp nhận nhầm ít hơn. Bất định: khoảng bootstrap theo họ (B = 10 000, seed khóa), bảng từng họ, bỏ từng họ, số cặp bất đồng và McNemar chính xác như mô tả; ít họ → mô tả là thăm dò, không dùng “95%” làm cửa đạt/rớt. Kết luận được phép cho từng bảng: sổ tay mục 6.5.

Điều kiện kết luận “P có tác dụng trên mẫu” (định trước): trên tập chẩn đoán test ΔFAR < 0 ở lượt 1 và cùng dấu ở lượt 2–3; số cặp bất đồng nghiêng về P; ΔRecall_S ≥ −10 điểm phần trăm; ablation tương ứng làm tăng FAR của P ở đúng loại thao tác. Không đạt → “chưa kết luận” và phân tích bằng TN4 + mã lỗi. Không tuyên bố cải thiện chỉ nhờ tăng NEI.

## 9. Lỗi kỹ thuật

ERROR/NO_OUTPUT (JSON hỏng sau 2 lần thử lại, hồ sơ không hợp lệ, timeout) là một lớp dự đoán riêng: không tính là Supported, nhưng sai với mọi nhãn vàng; không loại khỏi mẫu số. Báo tỷ lệ theo phương pháp và một dòng độ nhạy coi ERROR là Supported. Không đổi ERROR thành NEI.

## 10. Thay đổi sau khóa

Sửa lỗi phần mềm: ghi phiên bản khóa mới, lý do, chạy lại **mọi** phương pháp bị ảnh hưởng, giữ kết quả cũ. Phân tích chưa định trước được phép nhưng gắn nhãn “bổ sung sau khi xem kết quả” và tách khỏi bảng chính.

## 11. AI hỗ trợ và xác nhận của sinh viên

Các bản rà soát 08/10 và 10/2026 có công cụ AI hỗ trợ đọc nguồn, đối chiếu số, soạn tài liệu, mã tham chiếu, test và các ca giả lập EX-21–23. Tên mô hình backend của các phiên trợ lý không được tự phục dựng. Hoạt động này tách khỏi các LLM là đối tượng thí nghiệm (G, D). Sinh viên tự kiểm nguồn và chịu trách nhiệm nội dung; trạng thái xác nhận ghi trong `notes/ai_usage.md`.

Danh sách tối thiểu sinh viên tự kiểm trong bản gốc (đều **chưa xác nhận**):

| Bài/bảng | Trang PDF | Trường cần kiểm | Ảnh hỗ trợ |
|---|---:|---|---|
| [2], Bảng 1 | 3 | Cột Pearson/Spearman, hàng LLM sufficiency 0,14/0,09 | [Ảnh](../evidence/2026-10-08/papers/ref02-page03.png) |
| [3], Bảng 1 | 7 | Llama-3.1-8B/QuanTemp, Macro-F1 44,80 và 53,91; phân biệt verifier Llama-3.2-3B | [Ảnh](../evidence/2026-10-08/papers/ref03-page07.png) |
| [5], Bảng 2 | 9 | Cột Conflict, Accuracy/Macro-F1/Balanced Accuracy và CoVer/Confact | [Ảnh](../evidence/2026-10-08/papers/ref05-page09.png) |

Quy định AI của Khoa cho kỳ này chưa xác minh được từ các trang công khai đã mở ([đăng ký KLTN HK1 2026–2027](https://nc.uit.edu.vn/giao-vu/thong-bao-v-v-dang-ky-kltn-hk1-nam-hoc-2026-2027.html), [kế hoạch bảo vệ HK2 2025–2026](https://nc.uit.edu.vn/giao-vu/ke-hoach-to-chuc-bao-ve-khoa-luan-tot-nghiep-hk2-nam-hoc-2025-2026.html)); không suy ra Khoa không có quy định.
