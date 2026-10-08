# Kết quả kiểm tra các nhận xét — 08/10/2026

Phạm vi: [đề cương](../Đọc_báo_cùng_HuP_4_.docx), [báo cáo](../Đọc_báo_cùng_HuP_3_.docx), PDF gốc trong `báo/`, năm trang Apple và năm trang tài liệu [7]–[11]. Các nguồn web được mở trực tiếp và lưu HTML/văn bản/metadata; Apple có ảnh chụp. Không có thí nghiệm B0/B1/P mới hoặc dữ liệu quảng cáo LLM mới được chứng nhận trong lần sửa này.

## 1. Quy mô và tiêu chí kết luận: cần sửa, nhưng không thể đoán trước CI

Nhận xét về độ yếu của bốn họ test và nguy cơ chọn quá nhiều cấu hình trên hai họ validation là có cơ sở. Tuy nhiên, chưa có dữ liệu/hiệu ứng thì không thể khẳng định CI “gần như chắc chắn” chứa 0; bốn họ vẫn có thể cho khoảng nằm dưới 0, nhưng điều đó không tự bảo đảm suy rộng đáng tin cậy. Vấn đề là thiết kế, công suất và độ ổn định, không chỉ dấu của khoảng.

Đã chọn phương án giữ mức khả thi 120 claim/12 họ, **RQ3 thăm dò**:

| Tổng họ | Dev / val / test | Pilot |
|---|---|---|
| 12 | 6 / 2 / 4 | Đúng 6 họ, toàn bộ ở dev |
| 18 | 7 / 4 / 7 | Đúng 6 họ, toàn bộ ở dev |
| 20 | 8 / 4 / 8 | Đúng 6 họ, toàn bộ ở dev |
| 30, mở rộng | 12 / 6 / 12 | Đúng 6 họ, toàn bộ ở dev |

Như vậy nhận xét “18–20 họ chỉ có tối đa 7 họ pilot” đúng với 18, nhưng không đúng với 20 (dev có 8). Dù vậy, Gate 1 cho phép 8 mà chưa biết tầng cuối tạo rủi ro thật; đã bỏ lựa chọn 8 ở Gate 1 và bỏ nhánh tối thiểu 14 họ.

- Mô hình (tối đa hai ứng viên), prompt, k chọn trên dev theo tiêu chí ghi trước; k xét recall theo họ và chi phí. Dung sai có căn cứ nguồn, không tìm kiếm theo nhãn.
- Khóa trước khi mở val. Val chỉ audit/smoke test một lượt; nếu phải sửa vì lỗi thì công khai val đã bị dùng cho phát triển, không coi là kiểm định độc lập nữa.
- RQ3 báo ΔFAR, ΔRecall, mẫu số, kết quả từng họ và phân tích bỏ lần lượt một họ. ΔFAR<0, ΔRecall≥−5 điểm phần trăm chỉ mô tả xu hướng thuận lợi trên mẫu, không phải chứng minh ưu thế hoặc không-thua-kém.
- Bỏ cửa đạt/rớt “toàn bộ CI FAR dưới 0”. Nếu báo bootstrap theo họ 95%, ghi rõ với bốn họ không bảo đảm độ bao phủ danh nghĩa; không thay bootstrap claim độc lập để làm khoảng hẹp giả tạo. Mẫu số bằng 0 phải ghi không xác định.
- Không tự coi 16, 18–20 hoặc 30 họ là đủ cho suy luận khẳng định; muốn làm vậy cần thiết kế/công suất chốt trước test. Kết quả âm/không xác định vẫn là kết quả hợp lệ của khóa luận.

Cảnh báo suy luận khi ít cụm phù hợp với thảo luận phương pháp của [Cameron và Miller, 2015](https://doi.org/10.3368/jhr.50.2.317). Tài liệu đó bàn suy luận theo cụm trong hồi quy, không phải công thức công suất riêng cho FAR của đề tài; ở đây chỉ dùng làm bối cảnh thận trọng, không suy ra ngưỡng họ tối thiểu từ bài.

## 2. A–B–C: lỗi đặc tả thật, đã đồng bộ cả ablation

Bản trước giao loại giá trị từ A sang C nhưng C chỉ có luật tổng hợp, chưa có quan hệ so sánh. P−A lại ghi bỏ kiểm tra loại giá trị. Đã sửa:

- A lọc phạm vi/thuộc tính/đơn vị; B đối chiếu điều kiện; C1 kiểm xung đột, **C2 so kiểu giá trị**, C3 tổng hợp nhãn.
- `>24` so `=24` → bác bỏ; `≤3` so `=3` → chưa đủ; `≤3` so `=4` → bác bỏ nếu cùng phạm vi.
- Phân biệt thời lượng quan sát với **mức tối đa công bố**: 20 và 25 là hai mức khác nhau, không được hỗ trợ bằng bao hàm khoảng.
- `P−A(bộ phận)` chỉ tắt kiểm tra bộ phận, giữ luật loại giá trị của C. Không tuyên bố ablation này đo tác động bỏ toàn bộ A.

Xem [đặc tả và ca biên](QUY_TAC_ABC.md). Đây là sửa thiết kế nghiên cứu; chưa có mã pipeline C thực nghiệm để tuyên bố đã chạy các test đó.

## 3. Số liệu bài báo: đã đọc lại bảng/mục gốc

Số trang PDF dưới đây đếm từ 1. [Manifest](../evidence/2026-10-08/papers/manifest.json) ghi SHA-256 từng PDF gốc, trang và ảnh trang đã dùng. Kiểm tra chuỗi tự động chỉ chống hồi quy; cách đọc hàng/cột được rà riêng.

| Chi tiết bị nghi ngờ | Vị trí bài gốc | Kết luận và cách ghi sau sửa |
|---|---|---|
| FactLens 0,14 / 0,09 | [PDF [2]](../báo/[2].pdf), Bảng 1, PDF 3, trang in 18087; [ảnh](../evidence/2026-10-08/papers/ref02-page03.png) | Đúng: Pearson/Spearman ở **sufficiency**, cột LLM evaluator so người; không phải Accuracy |
| Alpha 0,0486 | [2], Bảng 6, PDF 10, trang in 18094; [ảnh](../evidence/2026-10-08/papers/ref02-page10.png) | Đúng: độ khớp evaluator với người; không phải đồng thuận giữa hai người của Bảng 7 |
| 733 claim | [2], mục 3.1, PDF 4; [ảnh](../evidence/2026-10-08/papers/ref02-page04.png) | Đúng: claim gốc lấy từ CoverBench, không phải 733 sub-claim |
| VerifierFC 53,91 / 44,80 | [PDF [3]](../báo/[3].pdf), Bảng 1, PDF 7, trang in 24351; [ảnh](../evidence/2026-10-08/papers/ref03-page07.png) | Đúng: Macro-F1 Llama-3.1-8B / QuanTemp, Adaptive BoN so Top-1; chênh 9,11 điểm phần trăm, khoảng 20,33% tương đối |
| “18,8%” | [3], abstract PDF 1 và mục 5.2 PDF 6; [ảnh](../evidence/2026-10-08/papers/ref03-page06.png) | Có thật trong diễn giải của bài nhưng không khớp phép tính từ cặp điểm trên. Không dùng làm mức tăng của cặp số đó; chỉ giữ như ghi chú bất nhất |
| Llama-3.2-3B | [3], mục 4, PDF 6; chú thích Bảng 1 PDF 7 | Đúng: **verifier/reward model** fine-tune LoRA, không phải nhầm tên Llama-3.1-8B là mô hình sinh |
| CLUE 12 người / 40 claim / 120 giải thích | [PDF [4]](../báo/[4].pdf), mục 5.1 PDF 6 và Phụ lục I.1 PDF 21; [ảnh](../evidence/2026-10-08/papers/ref04-page06.png) | Đúng: 40 claim duy nhất, 20 từ mỗi bộ DRUID/HealthVer; ba phương pháp tạo 120 giải thích |
| CLUE 0,102 / −0,080 | [4], Bảng 1, PDF 7; [ảnh](../evidence/2026-10-08/papers/ref04-page07.png) | Đúng: Qwen2.5-14B / DRUID; hệ số Entropy-CCT, không phải độ chính xác |
| CoVer “chưa có ý nghĩa thống kê” | [PDF [5]](../báo/[5].pdf), mục 6.4 / Statistical testing, PDF 8; [ảnh](../evidence/2026-10-08/papers/ref05-page08.png) | Tác giả có báo McNemar α=0,05, riêng so sánh trên ContraNote Conflict với CONFACT/ConflictRes. Không mở rộng thành mọi tập/chỉ số đều không có ý nghĩa; không phải kiểm định do KLTN chạy lại |
| CoVer Accuracy 86,0 / Macro-F1 68,0; Confact Macro-F1 73,4 | [5], Bảng 2, PDF 9; [ảnh](../evidence/2026-10-08/papers/ref05-page09.png) | Đúng hàng/cột Conflict; Accuracy cao không đồng nghĩa tốt hơn mọi chỉ số |

### Danh mục [7]–[11]

Đã mở đủ từng link và lưu trang nguồn trong `evidence/2026-10-08/ref*/`. Không thay năm/số trang chỉ vì nhận xét nghi ngờ; giữ những phần trang xuất bản xác nhận.

| Số | Nguồn chính | Xác nhận |
|---|---|---|
| [7] | [FEVER](https://aclanthology.org/N18-1074/) | Thorne và cộng sự, NAACL-HLT 2018, **809–819** |
| [8] | [AVeriTeC](https://arxiv.org/abs/2305.13117) | Schlichtkrull, Guo, Vlachos; NeurIPS 2023 Datasets & Benchmarks |
| [9] | [ViFactCheck](https://arxiv.org/abs/2412.15308) | Preprint 2024, trang arXiv ghi accepted AAAI 2025; tiếp tục dẫn dạng preprint, không tự thêm số trang proceedings |
| [10] | [ViWikiFC v2](https://arxiv.org/abs/2405.07615v2) | v1 **13/05/2024**, v2 **16/03/2026**; “v2, 2026” không sai, đã ghi ngày cụ thể |
| [11] | [ViNumFCR](https://aclanthology.org/2025.inlg-main.9/) | INLG 2025, **134–147** đúng metadata ACL Anthology |

## 4. Ví dụ Apple: lỗi trích/ngữ cảnh có thật, nghi ngờ AirPods 5 không được nguồn hiện tại ủng hộ

Tại lần kiểm ngày 08/10/2026, [trang AirPods 5 Việt Nam](https://www.apple.com/vn/airpods-5/specs/) trả HTTP 200, có tên AirPods 5. Chưa có căn cứ đổi EX-01–04 thành AirPods 4.

Trong cùng mục có tiêu đề “Mỗi Bên”, DOM tách khối tai nghe và khối hộp:

- Tai nghe: 4,3 g; dưới hình tai nghe, danh sách không có class `case`.
- Hộp: 32,3 g bản USB-C; dưới hình hộp, danh sách `ul.data-containers.case`.
- [Ảnh toàn mục](../evidence/2026-10-08/apple-airpods5-vn/dimensions-section.png) hiển thị cả hai hình và hai thông số. Vì vậy **không đảo nhãn EX-01/02/03 chỉ vì tiêu đề chung**; sửa bộ định vị để không gán nhầm bộ phận.
- [Trang AirPods 4 Moldova](https://www.apple.com/md/airpods-4/specs/) cũng có hộp tiêu chuẩn 32,3 g và bản ANC 34,7 g. Trùng khối lượng không chứng minh hai trang cùng thế hệ. Giữ thị trường/ngôn ngữ riêng, không gộp làm xung đột.

Các lỗi/thiếu sót đã sửa cụ thể:

1. Trích trực tiếp từ snapshot, giữ nguyên chữ/khoảng trắng; không tự thêm dấu chấm vào trong ngoặc trích. Mỗi đoạn có offset/dòng trong `page.txt`.
2. EX-01/02 xác định khối hộp trong DOM/ảnh; EX-04 nêu rõ bản đi kèm Hộp Sạc USB-C.
3. EX-06 giữ cả ngoặc nguồn về 7,5 giờ khi bật Âm Thanh Không Gian và Theo Dõi Chuyển Động Đầu. Câu rà soát giới hạn phạm vi công bố/phép thử, không tuyên bố mọi chế độ đều 8 giờ. Xem [nguồn Pro 3](https://www.apple.com/vn/airpods-pro/specs/) và [ảnh](../evidence/2026-10-08/apple-pro3-vn/battery-section.png).
4. Các câu pin/sạc nay nói rõ phạm vi thông số hãng, có `condition_ref` đến chú thích. Điều kiện claim nêu riêng (ANC tắt ở EX-10, âm lượng 100% ở EX-16) không được thay bằng điều kiện của nguồn để ép Supported.
5. EX-17/18 bỏ đoạn ghép “tiêu đề — câu thông số” giả dạng nguyên văn; tiêu đề tai nghe+hộp được ghi riêng. Giữ đoạn `>24` đúng [nguồn AirPods 2](https://support.apple.com/vi-vn/111856); C2 cho EX-18 Refuted, EX-20 NEI-thiếu.
6. NEI-thiếu chỉ nói thiếu trong **bộ nguồn đã lưu**, không khẳng định toàn bộ internet không có thông tin.
7. Bổ sung EX-21–23: xung đột pin, khối lượng, Bluetooth trên sản phẩm giả định `SIM-*`. Hai nguồn từng ca cùng phạm vi/điều kiện/hiệu lực/mức ưu tiên. Đây là **ca kiểm thử giả lập**, chưa tìm thấy xung đột thật trong năm trang đã kiểm. Không tính ba ca này vào pilot/test hoặc suy ra hiệu quả thực tế.

### Nguồn gốc mẫu: giữ điều chưa biết, không bịa lịch sử

- **EX-01–20:** `unknown_legacy`, model/prompt/run/time gốc đều chưa có. Không kết luận tự viết; cũng chưa xác nhận LLM sinh. Giữ nguyên câu trong bản thảo riêng với câu biên tập ngày 08/10.
- Câu biên tập được ghi `assistant_documentation_edit`, người biên tập Codex; không biến thành log thực nghiệm sinh quảng cáo của sinh viên.
- **EX-21–23:** `synthetic_test_fixture`, do Codex soạn theo yêu cầu thêm ca xung đột; không phải sản phẩm thật hay dữ liệu sinh LLM theo giao thức thí nghiệm.
- Tất cả 23 ca hiện có `dataset_eligible=false`. Để đủ phạm vi đề tài, bước thu dữ liệu vẫn cần mẫu LLM có model/phiên bản, prompt, cấu hình, thời điểm và output gốc; biến thể cần liên kết mẫu cha và thao tác sửa. Không thể phục dựng những trường này bằng suy đoán.

Hồ sơ từng mẫu: [examples.json](../evidence/2026-10-08/examples.json). Danh sách ảnh, nguồn và cách kiểm tra: [evidence README](../evidence/2026-10-08/README.md).
