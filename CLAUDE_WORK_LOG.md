# 📋 NHẬT KÝ CÔNG VIỆC CLAUDE CLI ĐÃ LÀM

> **Dự án:** Khóa Luận Tốt Nghiệp (KLTN) - Kiểm chứng claim quảng cáo tai nghe không dây
> **Sinh viên:** Bùi Lê Huy Phước (MSSV: 23521228)
> **Tổng hợp từ:** 7 sessions Claude CLI (`E--baitap-KLTN-KLTN`)
> **Cập nhật:** 2026-10-08

> **Trạng thái mới nhất — rà soát phản biện 08/10/2026:** Hai DOCX đã được sửa tiếp: RQ3 tối thiểu là thăm dò; pilot cố định 6 họ; chọn cấu hình trên dev, val audit sau khóa; bổ sung C2 so loại giá trị và sửa P−A. Đã đối chiếu số liệu PDF và đủ [7]–[11], chụp năm trang Apple, rà 20 ví dụ cũ, thêm 3 ca xung đột giả lập. Nguồn gốc 20 câu cũ vẫn chưa xác định; chưa tính 23 ca là dữ liệu quảng cáo LLM. Xem [kết luận từng nhận xét](docs/KIEM_TRA_PHAN_BIEN_2026-10-08.md), [bàn giao](docs/BAN_GIAO_2026-10-08.md), [hồ sơ ảnh/nguồn](evidence/2026-10-08/README.md). Phần nhật ký bên dưới là lịch sử: kế hoạch pilot 6–8 họ, chọn k trên val hoặc giữ nguyên mọi trích dẫn trong lần sửa đầu **đã được thay thế**, không phải đặc tả hiện hành.

---

## 📊 Tổng quan các Sessions

| # | Session ID | Thời gian | Kích thước | Trạng thái |
|---|-----------|-----------|------------|------------|
| 1 | `7b8ca511` | 07/10 ~20:56 | 10 KB | Test thử |
| 2 | `f7446f79` | 07/10 ~20:58 | 2 KB | Trống/lỗi |
| 3 | `78dcdd6e` | 07/10 ~21:37 | **1 MB** | **Session chính - nhiều công việc nhất** |
| 4 | `f4fd21f5` | 07/10 ~22:17 | 94 KB | Tiếp tục từ session 3 |
| 5 | `286747df` | 08/10 ~06:33 | 422 KB | Tiếp tục (nhiều lỗi 524 timeout) |
| 6 | `a045b7b9` | 08/10 ~06:46 | 717 KB | Tiếp tục (lỗi 524) |
| 7 | `74321358` | 08/10 ~06:49 | 544 KB | Session cuối (lỗi 524 + cross-session) |

---

## ✅ CÔNG VIỆC ĐÃ HOÀN THÀNH

### 1. Đọc & Phân tích toàn bộ tài liệu KLTN

Claude đã đọc và phân tích kỹ:
- **`Đọc_báo_cùng_HuP_3_.docx`** — Xác định đây là **báo cáo tiến độ tháng 09/2026**
- **`Đọc_báo_cùng_HuP_4_.docx`** — Xác định đây là **đề cương chi tiết** (bảng 98 hàng, hai cột lặp nội dung)
- **6 bài báo PDF** trong thư mục `báo/` — Các tài liệu tham khảo
- **Bản dịch** trong thư mục `dịch/` — Các bản dịch song ngữ/đơn ngữ đã có

### 2. Nhận xét & Đề xuất cải thiện kế hoạch KLTN

Claude đã phân tích sâu và đưa ra nhận xét:

#### Về Đề cương (`Đọc_báo_cùng_HuP_4_.docx`):
- **Đóng góp nghiên cứu cần làm rõ**: Bộ dữ liệu/khung gán nhãn claim quảng cáo tiếng Việt có provenance và đối chiếu nhận thức về sản phẩm-phiên bản-bộ phận-điều kiện-loại giá trị → không coi việc "Python quyết định nhãn" tự thân là tính mới
- **Thêm câu hỏi nghiên cứu RQ1-RQ3** và tiêu chí thành công:
  - RQ1: BM25 tìm đủ bộ bằng chứng đến đâu
  - RQ2: Lỗi nào đến từ truy hồi, trích xuất hay quyết định
  - RQ3: P có giảm FAR so với B1 mà vẫn giữ Recall Supported không
- **Chuyển quy mô dữ liệu thành mục tiêu theo tầng**:
  - Tối thiểu: 120 claim / 12 hệ sản phẩm
  - Mục tiêu: 180 claim / 18-20 hệ
  - Mở rộng: 300 claim / 30 hệ (chỉ khi pilot đủ năng suất)
- **Xác định MVP bắt buộc**: provenance, dữ liệu có nhãn, BM25, JSON extraction, B0/B1/P và đánh giá chính. Đưa P-A/P-B, E1/E2, website xuống phần tùy chọn
- **Thêm bảng rủi ro** với ngưỡng hành động cụ thể

#### Về Báo cáo tháng 9 (`Đọc_báo_cùng_HuP_3_.docx`):
- **Mốc chốt minh chứng: 30/09/2026** — phân biệt 3 trạng thái: đã có minh chứng trong kỳ / có trong bản thảo nhưng chưa xác nhận / chuyển sang tháng 10
- **Sửa mâu thuẫn**: có 20 ví dụ EX-01→EX-20 nhưng bảng lại nói chưa có đủ ví dụ
- **Các URL ngày 07/10** — chú thích là dữ liệu cập nhật sau kỳ báo cáo, không dùng làm minh chứng tháng 9
- **Thay `[Cần bổ sung]`** bằng bảng/ô thông tin thực tế phải xác nhận (cấu hình máy/API, mô hình, mã thể, log, thời gian chạy, lỗi)

### 3. Đề xuất bổ sung tài liệu tham khảo

Claude đã nghiên cứu và đề xuất thêm 5 tài liệu nền tảng:
- **FEVER** (Thorne et al., 2018) — Benchmark fact verification
- **AVeriTeC** (Schlichtkrull et al., 2023) — Evidence retrieval
- **ViFactCheck** (arXiv:2412.15308) — Fact-check tiếng Việt
- **ViWikiFC** (arXiv:2405.07615) — Wiki fact-check tiếng Việt
- **ViNumFCR** (INLG 2025, `2025.inlg-main.9`) — Numerical fact-check tiếng Việt

→ Dùng để đặt bối cảnh benchmark/evidence retrieval, không bắt buộc tái tạo toàn bộ hệ thống.

### 4. Lập kế hoạch timeline mới (Gates)

Claude đã thiết kế lại timeline thành các cổng nghiệm thu:

| Giai đoạn | Thời gian | Công việc |
|-----------|-----------|-----------|
| **Gate 1** | 01-15/10 | Khóa schema, hướng dẫn nhãn, provenance, pilot 45-60 claim/6-8 hệ |
| **Gate 2** | 16-31/10 | Hoàn tất BM25, B0/P tối thiểu; chốt môi trường, k và quyết định quy mô |
| **Gate 3** | 01-20/11 | Thu thập/gán nhãn dữ liệu chính, kiểm tra lỗi 20%, chia tập theo hệ; B1 |
| **Gate 4** | 21-30/11 | Khóa dữ liệu, prompt, mô hình, k, dung sai, giao thức; smoke test |
| **Gate 5** | 01-15/12 | Chạy B0/B1/P trên test; E1/E2, P-A/P-B tùy thời gian; tính chỉ số |
| **Gate 6** | 16-31/12 | Phân tích lỗi, viết luận văn, đóng gói mã-dữ liệu-README, chuẩn bị bảo vệ |

### 5. Tạo Plan chi tiết để sửa 2 file DOCX

Claude đã tạo 2 kế hoạch chi tiết (plans):
- **`cuddly-juggling-peach.md`** — Plan cập nhật đề cương và báo cáo KLTN
- **`indexed-scribbling-willow.md`** — Plan chi tiết hơn với hướng dẫn triển khai

Nội dung plan bao gồm:
- Context phân tích
- Phạm vi cập nhật cho từng file
- Cách triển khai bằng `python-docx` (giữ formatting, style, font)
- Verification steps

### 6. Chuẩn bị script Python sửa DOCX

Claude đã chuẩn bị script `update_docs.py` tại:
```
C:\Users\HP\.claude\jobs\74321358\tmp\update_docs.py
```
Nhưng **chưa được chạy** do môi trường chặn thao tác thực thi.

### 7. Điều phối cross-session (nhiều Claude chạy song song)

Claude CLI đã sử dụng cross-session messaging:
- Session `kltn-fd` gửi tin nhắn hỏi tiến độ
- Session `kltn-22` hỏi đã sửa DOCX chưa
- Session `cap-nhat-de-cuong-bao-cao` thông báo đang sửa trực tiếp 2 DOCX
- Session `Đoạn chat trước` xác nhận đã nhận tóm tắt và tiếp tục

### 8. Spawn 7 subagents để xử lý song song

Trong session chính (`78dcdd6e`), Claude đã tạo 7 subagents:
- `agent-a0b36389` — Phân tích tài liệu
- `agent-a341b6df` — Phân tích bài báo
- `agent-a3d0dfc3` — **"Thiết kế kế hoạch chỉnh sửa"** (failed: timeout 524)
- `agent-a59c986a` — Xử lý dữ liệu
- `agent-a775efa0` — **"Phân tích các bài báo tham khảo"** (failed: auth 401)
- `agent-abef3f06` — Xử lý bổ sung
- `agent-ac4d7881` — Kiểm tra
- `agent-afce8996` — Tổng hợp

---

## ❌ CÔNG VIỆC CHƯA HOÀN THÀNH (do lỗi)

### Lỗi chính gặp phải:
1. **Error 524 (Cloudflare Timeout)** — Xuất hiện rất nhiều lần, API không phản hồi trong 120s
2. **Error 401 (Invalid Token)** — Token hết hạn/không hợp lệ
3. **Script chưa chạy** — `update_docs.py` chưa được thực thi do môi trường chặn

### Công việc còn dở:
- [ ] **Sửa trực tiếp `Đọc_báo_cùng_HuP_4_.docx`** (đề cương) — Đã có plan nhưng chưa thực hiện
- [ ] **Sửa trực tiếp `Đọc_báo_cùng_HuP_3_.docx`** (báo cáo tháng 9) — Đã có plan nhưng chưa thực hiện
- [ ] **Kiểm tra & verify** sau khi sửa DOCX
- [ ] **Hoàn tất phân tích các bài báo tham khảo** (subagent bị fail)

---

## 📨 PROMPT GỐC CỦA CÁC SUBAGENT

Claude CLI đã spawn 4 subagent chính với các prompt sau:

### Subagent 1: "Phân tích tài liệu khóa luận" (model: sonnet)

```
Trong repo E:\baitap\KLTN\KLTN, hay đọc và phân tích hai file DOCX
Đọc_báo_cùng_HuP_3_.docx và Đọc_báo_cùng_HuP_4_.docx (dùng python/docx nếu cần),
xác định file nào là kế hoạch, file nào là báo cáo tháng 9, tóm tắt nội dung,
điểm mạnh/yếu, các khoảng trống và đề xuất điều chỉnh. Không sửa file.
Trả lời bằng tiếng Việt, nêu rõ cấu trúc và nội dung quan trọng.
```

### Subagent 2: "Phân tích các bài báo tham khảo" (model: sonnet)

```
Đọc các PDF trong thư mục E:\baitap\KLTN\KLTN\báo (bao gồm báo[1]-[6] và
báo\báo con1\2003.00744v3.pdf) và các bản dịch tương ứng nếu cần.
Tổng hợp cho từng bài: đề tài, dữ liệu, phương pháp/mô hình, kết quả,
hạn chế, điểm có thể kế thừa và khoảng trống nghiên cứu.
Đề xuất hướng đề tài khóa luận có tính mới nhưng khả thi cho sinh viên,
cùng các bài báo bổ sung nên tìm. Không sửa file. Trả lời tiếng Việt.
```

### Subagent 3: "Kiểm tra điểm cần sửa" (model: haiku)

```
Chỉ đọc và khảo sát cấu trúc hai file DOCX trong E:\baitap\KLTN\KLTN:
Đọc_báo_cùng_HuP_3_.docx và Đọc_báo_cùng_HuP_4_.docx. Xác định các vị trí/nội dung
mà khi chỉnh sửa cần bảo toàn định dạng, các cảnh báo thực tế như URL/ngày/sản phẩm
giả lập, và đề xuất phạm vi chỉnh sửa tối thiểu để nâng tính khả thi kế hoạch
15/9-31/12. Không sửa gì. Trả lời tiếng Việt thật cô đọng.
```

### Subagent 4: "Thiết kế kế hoạch chỉnh sửa" (model: opus) ⭐ QUAN TRỌNG NHẤT

```
Bối cảnh đã khảo sát: Người dùng muốn sửa hai DOCX trong repo E:\baitap\KLTN\KLTN:
file 4 là đề cương chi tiết, file 3 là báo cáo tiến độ tháng 09/2026.
Đề tài: kiểm chứng phát biểu quảng cáo tiếng Việt do LLM tạo về tai nghe không dây
dựa trên tài liệu chính thức, nhãn Supported/Refuted/NEI.
Phương án có BM25, LLM trích xuất, quy tắc A-B-C; baseline B0 (LLM đọc trực tiếp),
B1 (LLM quyết định trên hồ sơ chuẩn hóa); E1/E2/E3, P-A/P-B,
mục tiêu 300 claims/30 families; timeline 15/9-31/12. Đánh giá FAR,
supported recall, macro F1, evidence-set recall@k.
Tài liệu tham khảo hiện có 6 bài. Các vấn đề: báo cáo tháng 9 ghi [Cần bổ sung]
và 20 ví dụ có URL/ngày 07/10 nên không thuộc kỳ 9; kế hoạch quá tham vọng
cho một sinh viên/3.5 tháng; cần tránh tuyên bố novelty chỉ vì dùng Python rules.

Hay đề xuất một kế hoạch CHỈNH SỬA CỤ THỂ hai file sao cho đề tài mới vừa đủ,
khả thi, chặt chẽ, và lịch tháng 10-12 hợp lý. Phân biệt: cần chỉnh câu chữ/
thiết kế nghiên cứu (có thể thực hiện ngay) và không được bịa kết quả đã làm.
Đưa đề xuất về scope tối giản/MVP vs hạng mục tùy chọn, quy mô dữ liệu và
lịch có deliverables/gates. Cân nhắc đề xuất 2-3 tài liệu liên quan đáng tin cậy
(ViFactCheck, ViWikiFC, ViNumFCR/FEVER/AVeriTeC) và cách trích dẫn.
Không sửa file. Trả lời tiếng Việt, dạng plan rõ ràng để main agent viết vào plan file.
```

### Subagent 5: "Inspect DOCX work status" (model: haiku, session 6)

```
Read-only inspect the repository DOCX files Đọc_báo_cùng_HuP_3_.docx and _4_.docx
plus git status. Determine whether any prior edits exist, summarize exact structure/
content relevant to planned updates, and report any scripts or artifacts.
Do not modify files or run destructive commands.
```

### Subagent 6: "Plan DOCX update" (model: opus, session 6)

```
We need plan implementation for directly updating two DOCX thesis docs.
Background: _4_ is 98-row 2-column detailed thesis plan and _3_ is Sep 2026 progress
report. Existing plan at C:\Users\HP\.claude\plans\indexed-scribbling-willow.md
specifies required content updates. Constraints: preserve tables/styles, update both
repeated columns consistently, don't fabricate results. Need explain practical
python-docx implementation + robust verification. Do not modify any files;
return detailed execution plan.
```

---

## 🐍 SCRIPT PYTHON ĐÃ CHUẨN BỊ (chưa chạy)

File: `C:\Users\HP\.claude\jobs\74321358\tmp\update_docs.py`

Script này sử dụng `python-docx` để sửa trực tiếp 2 file DOCX. Nội dung chính:

### Phần 1 — Sửa Đề cương (`Đọc_báo_cùng_HuP_4_.docx`):

Cập nhật ~25 hàng trong bảng chính (bảng 98 hàng, 2 cột lặp), bao gồm:
- **Hàng 13**: Thêm khung gán nhãn claim quảng cáo tiếng Việt
- **Hàng 16**: Đóng góp = bộ dữ liệu có provenance + quy trình kiểm chứng nhận thức
- **Hàng 19**: Thêm RQ1-RQ3 và tiêu chí thành công (FAR, Recall Supported, evidence-set recall@k)
- **Hàng 49-51**: Quy mô dữ liệu theo tầng 120/180/300
- **Hàng 53-54**: Phân chia dev/val/test theo hệ sản phẩm 40%/20%/40%
- **Hàng 61-62**: BM25 + evidence retrieval recall@k
- **Hàng 67-68**: MVP bắt buộc vs hạng mục tùy chọn
- **Hàng 72-90**: Timeline mới theo 6 Gates (10/2026 → 12/2026)
- **Hàng 96**: Thêm 6 tài liệu tham khảo mới [7]-[11]

### Phần 2 — Sửa Báo cáo tháng 9 (`Đọc_báo_cùng_HuP_3_.docx`):

- Sửa mô tả đề tài → làm rõ đóng góp thực sự
- Thêm "mốc chốt minh chứng: 30/09/2026"
- Phân biệt 3 trạng thái: đã có minh chứng / có bản thảo chưa xác nhận / chuyển tháng 10
- Thay `[Cần bổ sung] Cấu hình thực tế` → yêu cầu điền CPU/RAM/GPU, model, mã thể, log
- Thay `[Cần bổ sung] Khó khăn thực tế` → yêu cầu ghi đầu việc bị vướng, nguyên nhân
- Sửa kế hoạch tháng 10 → tổ chức theo cổng nghiệm thu
- Sửa bảng trạng thái (table 28) → 4 hàng với trạng thái minh chứng trung thực
- Thêm "Đề xuất đọc thêm" (FEVER, AVeriTeC, ViFactCheck, ViWikiFC, ViNumFCR)
- Thêm 6 tài liệu tham khảo [7]-[11] vào danh mục

### Các helper functions:
- `set_cell_text()` — Thay text cell giữ style, font Times New Roman 12pt
- `set_row_both()` — Cập nhật cả 2 cột cùng lúc
- `replace_paragraph_text()` — Replace text trong paragraph giữ style
- `walk_paragraphs()` — Duyệt mọi paragraph (cả trong table)
- `set_matching_paragraph()` — Tìm paragraph chứa marker rồi thay toàn bộ text
- `insert_after()` — Chèn paragraph mới sau paragraph đã có

### Cách chạy (nếu muốn thực hiện):
```bash
pip install python-docx
python "C:\Users\HP\.claude\jobs\74321358\tmp\update_docs.py"
```

⚠️ Script tự backup trước khi sửa vào `C:\Users\HP\.claude\jobs\74321358\tmp\*.before-update.docx`

---

## 📋 CÔNG VIỆC CLAUDE CLI TÍNH LÀM TIẾP

Dựa trên plans và cross-session messages, đây là các công việc Claude CLI dự định nhưng chưa hoàn thành:

### Ưu tiên 1 — Sửa trực tiếp 2 file DOCX:
1. Chạy `update_docs.py` để cập nhật đề cương và báo cáo
2. Kiểm tra kết quả bằng python-docx (số bảng, heading, keyword verification)
3. Convert DOCX → kiểm tra file không lỗi Open XML
4. Báo rõ phần nào đã chỉnh vs phần nào cần người dùng/giảng viên điền

### Ưu tiên 2 — Phân tích sâu bài báo tham khảo:
1. Đọc kỹ 6 bài báo PDF + bài bổ trợ
2. Tổng hợp: đề tài, dữ liệu, phương pháp, kết quả, hạn chế
3. Xác định khoảng trống nghiên cứu
4. Đề xuất hướng đề tài có tính mới nhưng khả thi

### Ưu tiên 3 — Verification sau sửa:
1. Mở lại 2 DOCX → xác minh số bảng, kích thước, heading không hỏng
2. Trích xuất text → kiểm tra keywords: `120`, `180`, `300`, `B0`, `B1`, `P`, `FAR`, `Recall Supported`, `30/09/2026`, gates tháng 10-12
3. Xác minh đề cương giữ nội dung nhất quán giữa 2 cột
4. Xác minh báo cáo không còn `[Cần bổ sung]` trần trụi, không có ngày 07/10 được mô tả là minh chứng tháng 9
5. Nếu có LibreOffice → convert để phát hiện lỗi Open XML

---

## 🔧 Thông tin kỹ thuật

- **Claude CLI sessions**: Lưu tại `C:\Users\HP\.claude\projects\E--baitap-KLTN-KLTN\`
- **Plans**: Lưu tại `C:\Users\HP\.claude\plans\`
  - `cuddly-juggling-peach.md` — Plan cập nhật đề cương và báo cáo
  - `indexed-scribbling-willow.md` — Plan chi tiết hơn với hướng dẫn triển khai
- **Script chưa chạy**: `C:\Users\HP\.claude\jobs\74321358\tmp\update_docs.py`
- **Backup DOCX**: `C:\Users\HP\.claude\jobs\74321358\tmp\*.before-update.docx`
- **API Endpoint**: `https://gpt.teamsoclo.site` (TeamSocLo gateway)
- **Model**: `claude-opus-5-5` (default)
- **Worktree**: `.claude\worktrees\agent-a775efa0b4ad438bb`

---

*File này được tổng hợp từ dữ liệu thực tế của 7 sessions Claude CLI (JSONL logs), 2 plan files, và script update_docs.py.*

---

## Cập nhật tiếp nối lần 1 — Codex, 08/10/2026 (lịch sử)

- [x] Sửa trực tiếp `Đọc_báo_cùng_HuP_4_.docx`: RQ1–RQ3, đóng góp, quy mô theo tầng, chia theo họ không rò pilot, MVP/tùy chọn, Gate 1–6, rủi ro và tài liệu [7]–[11].
- [x] Sửa trực tiếp `Đọc_báo_cùng_HuP_3_.docx`: chốt minh chứng 30/09; sửa mâu thuẫn 20 ví dụ; phân biệt cập nhật 07/10; ghi nhãn minh họa dự kiến; các thông tin chưa có được ghi rõ, không bịa kết quả.
- [x] Đối chiếu sáu bài chính và PhoBERT; ghi kết quả, hạn chế, phần kế thừa và các chỗ dễ trích số liệu sai tại `docs/PHAN_TICH_TAI_LIEU.md`.
- [x] Kiểm tra cấu trúc: giữ 2/29 bảng, 98 hàng bảng đề cương, ô gộp, styles, hình, liên kết và chữ ký; kiểm tra toàn bộ XML; xuất PDF thành công (đề cương 12 trang, báo cáo 28 trang).
- [x] Lưu script tái lập ở `scripts/update_thesis_docs.py`; sao lưu bản gốc và manifest tại `scratch_test/docx-review-2026-10-08/` (được Git bỏ qua).
- [ ] Sinh viên xác nhận minh chứng đúng kỳ tháng 9, snapshot và nhãn ví dụ, cấu hình/API/ngân sách/mô hình/log và khó khăn thực tế.
- [ ] Triển khai nghiên cứu Gate 1 trở đi: schema, dữ liệu pilot, BM25, extraction và B0/B1/P. Chưa có thực nghiệm mới trong lần cập nhật tài liệu này.

Chi tiết thay đổi, kiểm tra, đường dẫn bản sao lưu và lệnh chạy lại: [docs/BAN_GIAO_2026-10-08.md](docs/BAN_GIAO_2026-10-08.md).

## Rà soát phản biện lần 2 — Codex, 08/10/2026

- [x] Đồng bộ quy mô với kết luận: RQ3 tối thiểu thăm dò, pilot đúng 6 họ, dev/val/test 6/2/4 hoặc 7/4/7 hoặc 8/4/8; val không dùng tìm kiếm cấu hình.
- [x] Thêm C2 so kiểu giá trị và phân biệt mức tối đa công bố; P−A chỉ bỏ kiểm tra bộ phận. Đặc tả chi tiết ở `docs/QUY_TAC_ABC.md`; chưa triển khai pipeline nghiên cứu.
- [x] Kiểm từng số bị nghi ngờ trong PDF gốc, lưu ảnh trang và hash; mở đủ [7]–[11]. Giữ các số được xác nhận, tách bất nhất “18,8%” khỏi chênh lệch Bảng 1.
- [x] Mở năm trang Apple, lưu HTML/text/ảnh/hash; sửa nguồn trích, ngữ cảnh và điều kiện của 20 ví dụ. Giữ câu gốc riêng; nguồn gốc sinh của chúng vẫn chưa xác định.
- [x] Thêm EX-21–23 giả lập xung đột, sản phẩm SIM-*, do Codex soạn; không gán cho Apple, không tính vào dữ liệu quảng cáo LLM. Hồ sơ đủ 23 mẫu: `evidence/2026-10-08/examples.json`.
- [x] Kiểm tra DOCX/XML và đối chiếu mẫu/nguồn; báo cáo hiện 32 bảng, đề cương vẫn 2 bảng/98 hàng. Xuất PDF 37/12 trang và kiểm bố cục; lưu bản trước sửa trong `scratch_test/docx-review-2026-10-08/before-audit/`.
- [ ] Vẫn cần log sinh quảng cáo thực để xác nhận phạm vi dữ liệu LLM, minh chứng tháng 9 và tài nguyên thí nghiệm; không thể điền bằng suy đoán.

Xem [kết luận kiểm tra phản biện](docs/KIEM_TRA_PHAN_BIEN_2026-10-08.md) và [hồ sơ nguồn/ảnh](evidence/2026-10-08/README.md). Các mục pilot/chọn k/giữ nguyên trích dẫn ở phần lịch sử không còn là đặc tả hiện hành.
