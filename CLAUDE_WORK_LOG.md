# 📋 NHẬT KÝ CÔNG VIỆC CLAUDE CLI ĐÃ LÀM

> **Dự án:** Khóa Luận Tốt Nghiệp (KLTN) - Kiểm chứng claim quảng cáo tai nghe không dây
> **Sinh viên:** Bùi Lê Huy Phước (MSSV: 23521228)
> **Tổng hợp từ:** 7 sessions Claude CLI (`E--baitap-KLTN-KLTN`)
> **Cập nhật:** 2026-10-08

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

## 🔧 Thông tin kỹ thuật

- **Claude CLI sessions**: Lưu tại `C:\Users\HP\.claude\projects\E--baitap-KLTN-KLTN\`
- **Plans**: Lưu tại `C:\Users\HP\.claude\plans\`
- **API Endpoint**: `https://gpt.teamsoclo.site` (TeamSocLo gateway)
- **Model**: `claude-opus-5-5` (default)
- **Worktree**: `.claude\worktrees\agent-a775efa0b4ad438bb`

---

*File này được tổng hợp từ dữ liệu thực tế của 7 sessions Claude CLI (JSONL logs) và 2 plan files.*
