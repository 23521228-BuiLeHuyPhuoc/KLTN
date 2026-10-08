# Kế hoạch chi tiết cho sinh viên (08/10 → 31/12/2026)

Tài liệu do công cụ AI (Claude) soạn ngày 08/10/2026. Đây là **đề xuất, chưa được GVHD xác nhận**. Mọi số giờ đều là **GIẢ ĐỊNH**; sau lô 0, bạn đo thời gian thật rồi sửa lại.

Các chỗ ghi **[SINH VIÊN ĐIỀN: …]** là thông tin chỉ bạn biết. AI không được đoán những thông tin này.

## 0. Giải thích thuật ngữ (đọc một lần)

- **FAR (False Acceptance Rate)**: tỉ lệ phát biểu thực ra Refuted hoặc NEI mà hệ thống lại cho là Supported. Đây là lỗi nguy hiểm nhất, vì quảng cáo sai bị "duyệt".
- **Recall Supported**: trong các phát biểu thực sự đúng, hệ thống nhận ra được bao nhiêu phần.
- **recall@k**: tỉ lệ phát biểu mà đoạn bằng chứng đúng nằm trong k đoạn đầu tiên được truy xuất. Nếu hồ sơ chỉ có N đoạn thì dùng k_eff = min(k, N).
- **BM25**: cách xếp hạng văn bản cổ điển theo từ khóa trùng khớp. Không cần GPU.
- **cluster bootstrap**: lấy mẫu lại theo **họ sản phẩm** (không lấy theo từng câu) để tính khoảng tin cậy. Cách này cần thiết vì các câu cùng một họ thường giống nhau.
- **ablation**: bỏ hoặc thay một thành phần (ví dụ bỏ bước so sánh kiểu giá trị) để xem thành phần đó đóng góp bao nhiêu.
- **kappa (Cohen's κ)**: mức đồng ý giữa hai người gán nhãn sau khi trừ phần trùng do may rủi. Khoảng 0,6–0,8 là khá; giá trị này là quy ước thông dụng, không phải quy định của Khoa.
- **provenance**: nguồn gốc dữ liệu, tức ai hoặc mô hình nào sinh ra, lúc nào, dùng prompt nào, lấy từ trang nào, có mã băm nào.

## 1. Tổng quan: 5 mốc (theo Gate trong HuP_4 đề xuất)

| Mốc | Thời gian | Kết quả phải có | MVP / tùy chọn |
|---|---|---|---|
| M1 = Gate 1 | 08–31/10 | Đã thu hồi khóa; chọn được nhà cung cấp; Llama chạy thử 5 ví dụ; lô 0 (20 phát biểu); bản hướng dẫn gán nhãn v1 | MVP |
| M2 = Gate 2 | 01–14/11 | Pilot 40 phát biểu; tính kappa trên 30 phát biểu với người gán thứ hai; khóa luật D1–D4 | MVP |
| M3 = Gate 3 | 15/11–04/12 | Đủ 120 phát biểu / 12 họ (6/2/4); có ≥1 hãng ngoài Apple; khóa tập test | MVP. Mức 180/18 là tùy chọn |
| M4 = Gate 4–5 | 05–21/12 | Chạy B0/B1/P × 3 lượt; bảng E1–E3 kèm cluster bootstrap; phân tích lỗi | MVP. Ablation và RQ3 là tùy chọn |
| M5 = Gate 6 | 22–31/12 | Bản thảo khóa luận đầy đủ; gói tái lập; slide nháp | MVP |

Hạn 31/12 là **chưa xác minh**. Tuần này hãy hỏi GVHD hoặc Văn phòng Khoa ngày nộp và ngày bảo vệ thật.

## 2. Kế hoạch theo tuần (A = 12 giờ/tuần, B = 20 giờ/tuần)

Ở kịch bản A, bạn làm đủ phần MVP và bỏ toàn bộ phần tùy chọn. Ở kịch bản B, bạn có thể thêm mức 180/18, ablation và RQ3.

| Tuần | Mục tiêu | Việc chính | Giờ A / B | Đầu ra | Xong khi | Phụ thuộc |
|---|---|---|---|---|---|---|
| T1 (08–14/10) | An toàn + công cụ | Thu hồi khóa; chọn nhà cung cấp; chạy thử Llama trên 5 ví dụ; hỏi GVHD | 12 / 16 | `run_manifest` thử; email GVHD | 5 lượt chạy có log và hash prompt | Tài khoản API |
| T2 (15–21/10) | Lô 0 | Sinh 20 phát biểu ordinary_llm; gán nhãn và bấm giờ; ghi search_log | 12 / 18 | lô 0 + bảng thời gian | Có t_claim thật | T1 |
| T3 (22–31/10) | Chốt Gate 1 | Sửa hướng dẫn v1; tìm người gán thứ hai; viết Chương 1 nháp | 12 / 20 | HUONG_DAN v1; Chương 1 | GVHD đồng ý Gate 1 | Phản hồi GVHD |
| T4 (01–07/11) | Pilot | Thêm 20 phát biểu (tổng 40); người thứ hai gán 30 phát biểu | 12 / 20 | pilot 40 | Có 2 bộ nhãn độc lập | Người thứ hai |
| T5 (08–14/11) | Chốt Gate 2 | Tính kappa; xử lý bất đồng; khóa D1–D4; viết Chương 2 | 12 / 20 | báo cáo kappa; luật khóa | Luật có hash, không sửa nữa | T4 |
| T6–T8 (15/11–04/12) | Thu đủ dữ liệu | Mỗi tuần khoảng 30–40 phát biểu; thêm họ ngoài Apple; chụp bằng chứng | 36 / 60 | 120/12 (B: 180/18) | audit PASS; test khóa | Nguồn chính thức |
| T9 (05–11/12) | Chạy thí nghiệm | B0, B1, P × 3 lượt trên tập test; lưu toàn bộ output | 12 / 20 | output + manifest | Không còn lượt lỗi | T8 |
| T10 (12–21/12) | Phân tích | E1–E3, cluster bootstrap, phân tích lỗi; viết Chương 3–4 | 15 / 25 | bảng, hình | Mọi số có tử và mẫu số | T9 |
| T11–T12 (22–31/12) | Hoàn thiện | Chương 5, tóm tắt, khai báo AI, gói tái lập, slide | 20 / 30 | bản thảo PDF | GVHD nhận bản thảo | T10 |

## 3. 14 ngày đầu (theo ngày)

- [ ] **08/10** — Vào trang nhà cung cấp API cũ, **thu hồi (revoke) khóa đã lộ** và tạo khóa mới. Chỉ lưu khóa mới trong `.env` cục bộ, không commit. Khóa cũ vẫn còn trong lịch sử Git công khai, vì vậy thu hồi là bắt buộc.
- [ ] **09/10** — Chọn nhà cung cấp Llama: [SINH VIÊN ĐIỀN: tên nhà cung cấp, tên model chính xác, giá/1M token vào và ra]. Ghi vào `run_manifest`.
- [ ] **10/10** — Chạy thử Llama trên 5 ví dụ (EX-01…EX-05) bằng `build_eval_prompts.py`. Lưu prompt, sha256 của prompt, nhiệt độ, seed nếu có, và thời gian.
- [ ] **11/10** — Chạy `check_input_leak.py` trên input. Ghi lại 5 output vào log; không sửa tay.
- [ ] **12/10** — Gửi GVHD email ở mục 7 (câu hỏi Gate, mốc, phiếu chấm).
- [ ] **13/10** — Viết prompt sinh quảng cáo ordinary_llm, có lưu log và hash. Sinh thử 5 quảng cáo.
- [ ] **14/10** — Tách các phát biểu từ 5 quảng cáo đó. Ghi provenance (model, ngày, prompt hash).
- [ ] **15–17/10** — Lô 0: đủ 20 phát biểu. Gán nhãn **có bấm giờ** từng phát biểu, ghi `t_claim`, và ghi search_log cho mọi câu NEI.
- [ ] **18/10** — Tính t_claim trung bình. Ước lượng lại tổng giờ bằng công thức ở mục 4.
- [ ] **19/10** — Tìm người gán thứ hai: [SINH VIÊN ĐIỀN: tên, vai trò]. Gửi họ HUONG_DAN_GAN_NHAN.md.
- [ ] **20/10** — Chạy `audit_examples.py --check` và unittest. Ghi lô 0 vào nhật ký.
- [ ] **21/10** — Tổng kết lô 0 gửi GVHD: số lượng, t_claim, các ca khó, đề xuất sửa hướng dẫn.

## 4. Quy trình và công thức

**Gán nhãn một phát biểu:** đọc phát biểu → tìm trong hồ sơ bằng chứng của họ sản phẩm đó → áp luật A–B–C (QUY_TAC_ABC) → ghi nhãn, đoạn bằng chứng và search_log nếu là NEI → bấm giờ dừng.

**Công thức (thay số đo thật vào):**
- Giờ gán nhãn = N × t_claim / 60. Ví dụ giả định với t_claim = 6 phút: 120 phát biểu ≈ 12 giờ, 180 phát biểu ≈ 18 giờ. Cộng thêm khoảng 50% cho việc tìm bằng chứng và sửa lỗi.
- Số lượt gọi API = số phát biểu test × số hệ thống (B0, B1, P = 3) × số lượt (3).
- Chi phí ≈ số lượt × (token_vào × giá_vào + token_ra × giá_ra) / 1.000.000. Giá chưa xác minh: [SINH VIÊN ĐIỀN].
- Thời gian chạy ≈ số lượt × độ trễ trung bình / số luồng song song. Hãy đo độ trễ ở ngày 10/10.

**Cỡ mẫu:** kết quả `simulate_power.py` (giả định FAR 0,30 → 0,15) cho thấy với 4 họ test và 40 phát biểu R+NEI, khoảng tin cậy rộng khoảng 0,24 và chỉ khoảng 58% số lần mô phỏng loại được 0. Vì thế kết quả C3 phải được báo là **thăm dò**.

## 5. Viết song song và tái lập

| Thời điểm | Viết gì |
|---|---|
| Cuối 10 | Chương 1 (bài toán, câu hỏi nghiên cứu), nháp |
| Giữa 11 | Chương 2 (tổng quan 11 tài liệu, định vị) |
| Đầu 12 | Chương 3 (dữ liệu, luật, giao thức) |
| Giữa 12 | Chương 4 (kết quả, lỗi) |
| Cuối 12 | Chương 5, tóm tắt, khai báo AI |

**Checklist tái lập:**
- [ ] Mọi lượt chạy có `run_manifest` (model, ngày, nhiệt độ, sha256 prompt).
- [ ] Bằng chứng có ảnh chụp và hash; không sửa file evidence.
- [ ] Tập test được khóa bằng hash trước khi chạy.
- [ ] README ghi đủ lệnh để chạy lại.
- [ ] Tất cả các kiểm tra đều PASS.

## 6. Mốc gặp GVHD

31/10 (Gate 1), 14/11 (Gate 2), 04/12 (Gate 3), 11/12 (Gate 4), 21/12 (Gate 5), trước 31/12 (bản thảo).

## 7. Mẫu email GVHD

> Kính gửi Thầy/Cô [SINH VIÊN ĐIỀN],
> Em là [SINH VIÊN ĐIỀN], đang làm KLTN "[SINH VIÊN ĐIỀN: tên đề tài]". Em gửi Thầy/Cô bản đề xuất điều chỉnh đề cương (chữ đỏ, chờ Thầy/Cô xác nhận); trong đó có phần do công cụ AI hỗ trợ soạn và đã ghi rõ trong mục khai báo AI. Em xin ý kiến của Thầy/Cô về:
> 1. Lịch Gate mới (Gate 1 kéo dài đến 31/10) và mức MVP 120 phát biểu / 12 họ.
> 2. Luật inherit_headline (D1) và việc thêm ít nhất 1 hãng ngoài Apple.
> 3. Việc dùng Llama qua API [nhà cung cấp].
> 4. Hạn nộp và ngày bảo vệ chính thức, cùng phiếu chấm của Khoa (nếu có).
> Em cảm ơn Thầy/Cô.

## 8. Đường cắt và kế hoạch B

- Đến 31/10 chưa có lô 0 → bỏ mức 180, chỉ làm MVP.
- Đến 14/11 chưa có người gán thứ hai → báo cáo tự nhất quán (gán lại sau 7 ngày) và ghi rõ là hạn chế.
- Đến 04/12 chưa đủ 120 phát biểu → dùng kế hoạch B trong DINH_VI_VA_TIEU_CHI.md §2 (dùng N thực có).
- API hỏng hoặc quá đắt → giảm số lượt chạy từ 3 xuống 1 cho B0 và ghi rõ trong báo cáo.

## 9. Rủi ro và tín hiệu sớm

| Rủi ro | Tín hiệu sớm | Xử lý |
|---|---|---|
| Gán nhãn chậm | t_claim > 10 phút ở lô 0 | Giảm về MVP |
| Thiếu NEI hoặc Refuted tự nhiên | < 20% câu R+NEI trong ordinary_llm | Bổ sung controlled_variant, nhưng giữ ordinary_llm ≥ 50% |
| Không có nguồn chính thức ngoài Apple | Không tìm được trang spec trước 15/11 | Báo GVHD và thu hẹp phạm vi |
| API thay đổi model | Tên hoặc phiên bản model đổi | Ghi ngày; chạy lại cả 3 hệ thống cùng một ngày |
| Trễ viết | Đến cuối 11 chưa có Chương 2 | Mỗi tuần dành 3 giờ cố định để viết |

## 10. Việc CHỈ sinh viên làm được (AI không làm thay)

- [ ] Thu hồi và tạo khóa API mới.
- [ ] Gán nhãn và ký xác nhận vào dữ liệu của mình.
- [ ] Liên hệ GVHD và người gán thứ hai.
- [ ] Xác nhận các đối chiếu bài báo do AI hỗ trợ.
- [ ] Điền các ô [SINH VIÊN ĐIỀN].
- [ ] Mở hai file docx bằng Word để xem lại bố cục (AI chưa xem được vì máy không có LibreOffice).
- [ ] Quyết định có dọn lịch sử Git hay không. Các lệnh dưới đây AI **không chạy**:

```bash
git clone --mirror https://github.com/23521228-BuiLeHuyPhuoc/KLTN KLTN-mirror && cd KLTN-mirror
git filter-repo --path .env --invert-paths
git filter-repo --path CLAUDE_WORK_LOG.md --invert-paths   # tùy chọn: xóa log khỏi mọi commit (kể cả bản đã che) — sao lưu bản đã che trước, thêm lại sau
git push --force --mirror   # viết lại lịch sử công khai; mọi bản clone khác phải clone lại
```
