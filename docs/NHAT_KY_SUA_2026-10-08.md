# Nhật ký sửa — rà soát 08/10/2026 (nhánh `review/opus-2026-10-08`)

Người sửa: công cụ AI (Claude Opus) theo yêu cầu sinh viên. Không push, không merge, không viết lại lịch sử. Gốc so sánh: commit `dec67a9`. Bản sao docx trước sửa: SHA-256 HuP_3 `cd252865…9949`, HuP_4 `465bead3…765e` (lấy lại: `git show dec67a9:<tên file>`).

| # | File | Trước → Sau | Lý do | Mã phát hiện | Kiểm lại |
|---|---|---|---|---|---|
| 1 | `.env`, `.gitignore` | `.env` được Git theo dõi (chứa khóa API) → `git rm --cached`, thêm `.env`, `.env.*` vào .gitignore. **Không đọc/in nội dung.** | Lộ khóa trong repo công khai | S1 | `git ls-files .env` rỗng |
| 2 | `scripts/abc_reference.py`, `tests/test_abc.py`, `tests/fixtures/examples_structured.json` | (không có) → hàm tham chiếu A–B–C1–C3, 27 test | Đặc tả chưa có kiểm thử chạy được | T2 | `python3 -m unittest discover -s tests` |
| 3 | `docs/QUY_TAC_ABC.md` | thêm §3b luật kế thừa điều kiện (DỰ THẢO) | 11/23 câu gốc đổi nhãn khi đọc B nghĩa đen | T3 | `test_original_claims_*` |
| 4 | `docs/GIAO_THUC_DANH_GIA.md` | thêm §10 thu theo lô + tiêu chí dừng, §11 độ chính xác ước lượng | Thiếu quy trình thu và tiêu chí dừng; cỡ test nhỏ | T4a, T5 | đọc §10–11; `scripts/simulate_power.py` |
| 5 | `templates/llm_ad_sample.json`, `scripts/check_input_leak.py`, `scripts/simulate_power.py` | (không có) → mẫu hồ sơ quảng cáo LLM, guard rò nhãn, mô phỏng | T4b, T5 | | `check_input_leak.py templates/llm_ad_sample.json` → PASS |
| 6 | `Đọc_báo_cùng_HuP_4_.docx` | thêm đoạn đỏ trong hàng 20, 24, 29, 32, 38, 45, 47, 64, 67; dòng đầu → "Bản đề xuất điều chỉnh … chờ GVHD xác nhận" | --check FAIL (thiếu độc lập 30, search_log, k_eff, 3 lượt, nhà cung cấp, quảng cáo thô); mốc 15/10 không thực tế | T1, T10 | `update_thesis_docs.py --check`; bảng [1, 98] và hàng chữ ký không đổi |
| 7 | `Đọc_báo_cùng_HuP_3_.docx` | "Đã đối chiếu báo/…" (4 ô) → "Đối chiếu có hỗ trợ AI; chờ sinh viên xác nhận: …" (đỏ); thêm ghi nhận AI trước 3.1; đoạn giao thức đỏ trước 3.3; "do Codex soạn" → "do công cụ AI (Codex) soạn"; 3.4 và khó khăn "[chưa có]" → "[SINH VIÊN ĐIỀN]"; 3 ô bảng mục 4 thêm dòng đỏ; đoạn Gate đề xuất đỏ ở mục 5; phụ lục nội bộ gắn "[GHI CHÚ NỘI BỘ — SINH VIÊN XÓA TRƯỚC KHI NỘP]" | Giọng sinh viên cho việc AI làm; --check FAIL; placeholder không rõ ai điền | T1, T7, T8 | `--check`; 32 bảng, số hàng không đổi |
| 8 | `scripts/review_patch_2026_10_08.py` | (không có) → script vá có kiểm CRC, XML, cấu trúc bảng, sectPr/hình, hàng chữ ký, chống vá hai lần | `update_thesis_docs.py --apply` không tái lập được (bản gốc trong scratch_test/ không có trong repo) | T1, T9 | chạy lại → "đã vá trước đó, dừng" |
| 9 | `.gitignore` | bỏ theo dõi `tests/__pycache__` (do tôi lỡ commit ở 35da2d6) và gitlink `.claude/worktrees/agent-…` không có .gitmodules | Vệ sinh repo | T9 | `git ls-files | grep -c pycache` = 0 |
| 10 | `README.md`, `docs/BAN_GIAO_2026-10-08.md` | README mô tả cấu trúc cũ → cấu trúc hiện tại + mục rà soát; ghi chú liên kết scratch_test hỏng | T1, T9 | | đọc file |
| 11 | `docs/QUYET_DINH_CAN_CHOT.md`, `docs/KE_HOACH_THUC_TE_2026-10-08.md`, file này | mới | T10 | | |

Không sửa: page.txt, metadata.json, ảnh, hash, PDF, bản dịch, `examples.json` (luật D1/D4 chưa chốt nên không đổi nhãn), hàng "Xác nhận của CBHD / 15/09/2026".

## Hướng dẫn xóa khóa khỏi lịch sử (KHÔNG chạy trong lần rà soát này)

Việc đầu tiên là **thu hồi khóa trên trang nhà cung cấp và tạo khóa mới**; xóa lịch sử không thu hồi được bản đã bị sao chép. Sau đó, nếu muốn:

```bash
pip install git-filter-repo
git clone --mirror https://github.com/23521228-BuiLeHuyPhuoc/KLTN KLTN-mirror && cd KLTN-mirror
git filter-repo --path .env --invert-paths
git push --force --mirror   # viết lại lịch sử công khai: mọi bản clone khác phải clone lại
```
