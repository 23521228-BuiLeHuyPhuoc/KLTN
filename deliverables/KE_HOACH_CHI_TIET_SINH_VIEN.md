# Kế hoạch công việc khóa luận — làm lần lượt từ đầu đến cuối

**Đề tài:** Phương pháp kiểm chứng phát biểu quảng cáo dựa trên bằng chứng văn bản cho tai nghe không dây  
**Sinh viên:** Bùi Lê Huy Phước (23521228) · **CBHD:** ThS Trần Hồng Nghi · **Thời gian:** 09/10–31/12/2026  
**Tổng công sức ước lượng:** ≈ 208–320 giờ (≈ 17–27 giờ/tuần) · **Trạng thái:** chờ GVHD xác nhận

## Cách dùng file này

1. Làm **theo đúng thứ tự B01 → B52**. Mỗi việc ghi rõ việc nào phải xong trước; không có việc nào cần kết quả của việc phía sau.
2. Mỗi việc có bốn phần: **Mục đích → Làm (từng bước) → Nếu vướng → Checklist bàn giao**. Chỉ chuyển sang việc tiếp theo khi đã tick hết checklist.
3. Cuối mỗi giai đoạn có **checklist bàn giao giai đoạn** — đó là thứ đem đi báo cáo GVHD.
4. Khi một bước ghi “tra cứu §x”, mở `deliverables/TRA_CUU_KLTN.md` mục x (luật gán nhãn, đặc tả thuật toán, mẫu file, lý do thiết kế). Không cần đọc file tra cứu từ đầu.

## Toàn cảnh: 10 giai đoạn, 52 việc

| GĐ | Giai đoạn | Thời gian | Việc | Kết quả cuối giai đoạn |
|---|---|---|---|---|
| 1 | Khởi động và chốt tính mới | 09/10–18/10 | B01–B05 | M1 — Tính mới đã kiểm: tra cứu §2.2 có cột “Đã đọc” = toàn văn cho mọi bài; GVHD đã trả lời QĐ1 hoặc đã ghi ngày hỏi |
| 2 | Môi trường | 19/10–22/10 | B06–B07 | Smoke test 5 ví dụ chạy hết B0/B1/P có manifest |
| 3 | Nguồn cho 2 họ pilot | 23/10–01/11 | B08–B12 | D1–D4 cho 2 họ pilot, độ phủ 100% |
| 4 | Dữ liệu pilot | 02/11–09/11 | B13–B19 | Lô pilot có nhãn, ≥ 2 biến thể mỗi loại COND/PART/ROLE, có số đo phút/claim |
| 5 | Pipeline trên dev và pilot | 10/11–23/11 | B20–B30 | M2 — Pilot xong: báo cáo pilot, quy mô chốt (QĐ5), JSON hợp lệ ≥ 95% trên dev |
| 6 | Dữ liệu đủ quy mô | 24/11–07/12 | B31–B34 | M3 — Dữ liệu đủ: đạt sàn test ở tra cứu §3.4; κ đã báo |
| 7 | Chia tập và khóa | 08/12–11/12 | B35–B38 | M4 — Khóa: `protocol_lock.json` đã commit; val chạy đúng một lần |
| 8 | Thực nghiệm và phân tích | 12/12–17/12 | B39–B42 | M5 — Kết quả: bảng B3–B12 tái tạo byte-khớp từ `runs/` |
| 9 | Viết luận văn | 18/12–27/12 | B43–B49 | M6 — Bản thảo đủ 5 chương, mọi số truy về file |
| 10 | Bàn giao và bảo vệ | 28/12–31/12 | B50–B52 | M7 — Gói tái lập chạy lại trên bản sao mới; slide đã tập dượt |

## Danh sách việc (xem nhanh)

| Việc | Tên việc | Cần xong trước | Giờ |
|---|---|---|---|
| B01 | Thu hồi khóa API đã lộ, tạo `.env` | — | 0,5 |
| B02 | Đọc sổ tay, gửi câu hỏi GVHD | B01 | 2–3 |
| B03 | Đọc, ghi chép bài báo gần nhất | B02 | 8–12 |
| B04 | Lập bảng công trình gần nhất, kiểm lại tính mới | B03 | 4–6 |
| B05 | Chốt định nghĩa bài toán và QĐ | B04 | 2–3 |
| B06 | Cài môi trường và cấu trúc repo | B05 | 3–4 |
| B07 | Chọn mô hình, chạy thử một mẫu | B01, B06 | 4–6 |
| B08 | Kiểm kê họ AirPods và Beats | B05 | 2–3 |
| B09 | Thu nguồn, snapshot cho 2 họ pilot | B08 | 3–6 |
| B10 | Trích văn bản có cấu trúc (M1) | B09 | 5–7 |
| B11 | Chia đoạn, sinh mã đoạn (M2) | B10 | 4–6 |
| B12 | Kiểm độ phủ nguồn | B11 | 1–2 |
| B13 | Chốt giao thức, prompt sinh quảng cáo | B07 | 2–3 |
| B14 | Sinh quảng cáo lô pilot (M3) | B13 | 2–3 |
| B15 | Tách phát biểu lô pilot | B14 | 2–3 |
| B16 | Tạo biến thể cặp tối thiểu lô pilot | B15 | 2–3 |
| B17 | Kiểm trùng, loại ngoài phạm vi | B16 | 1 |
| B18 | Gán nhãn tham chiếu lô pilot | B12, B17 | 4–6 |
| B19 | Nhật ký tìm nguồn cho NEI lô pilot | B18 | 1–2 |
| B20 | BM25 lọc theo sản phẩm (M4) | B11 | 5–7 |
| B21 | Đo recall@k trên dev, chọn k | B18, B20 | 1–2 |
| B22 | Schema σ có trường trích dẫn, prompt trích xuất | B05 | 3–4 |
| B23 | Trích xuất, neo nguồn, chuẩn hóa (M5, M6) | B21, B22 | 9–13 |
| B24 | Đánh giá trích xuất trên dev | B18, B23 | 2–3 |
| B25 | Nối SAV (P) với hồ sơ (M7) | B23 | 3–4 |
| B26 | Cài B0, B1, B2 (M8) | B23 | 5–7 |
| B27 | Kiểm công bằng, rò nhãn (M9) | B25, B26 | 1–2 |
| B28 | Runner, manifest, cache (M10) | B27 | 5–8 |
| B29 | Chạy pilot trên dev | B28 | 3–5 |
| B30 | Chốt quy mô, cấu hình, mức kết luận | B29 | 2–3 |
| B31 | Thu nguồn, chia đoạn các họ còn lại | B30 | 8–16 |
| B32 | Sinh quảng cáo, tách claim, biến thể còn lại | B30, B31 | 4–8 |
| B33 | Gán nhãn, nhật ký NEI phần còn lại | B32 | 10–22 |
| B34 | Kiểm độ tin cậy nhãn | B33 | 3–5 |
| B35 | Chia tập theo họ | B33 | 1 |
| B36 | Hồ sơ chuẩn cho TN4 | B35 | 6–8 |
| B37 | Kiểm dữ liệu trước thực nghiệm (M13) | B36 | 2–3 |
| B38 | Khóa giao thức | B37 | 1–2 |
| B39 | Chạy TN1–TN4 | B38 | 6–10 |
| B40 | Tính chỉ số, bảng, hình (M11, M12) | B39 | 4–6 |
| B41 | Mã lỗi, gán lỗi theo chuỗi | B40 | 6–8 |
| B42 | Case study và nhận xét | B41 | 2–3 |
| B43 | Chương 1 — Mở đầu | B02 | 6–8 |
| B44 | Chương 2 — Cơ sở, công trình liên quan | B04 | 10–14 |
| B45 | Chương 3 — Dữ liệu và phương pháp SAV | B38 | 12–16 |
| B46 | Chương 4 — Kết quả và thảo luận | B42 | 12–16 |
| B47 | Chương 5 — Kết luận, giới hạn | B46 | 3–4 |
| B48 | Hình, bảng, công thức xuất bản | B47 | 4–6 |
| B49 | Tham khảo, thuật ngữ, khai báo AI, định dạng | B48 | 4–6 |
| B50 | Gói tái lập, demo dòng lệnh, README | B40 | 6–10 |
| B51 | Slide và chuẩn bị bảo vệ | B49 | 6–10 |
| B52 | Kiểm điều kiện hoàn thành | B50, B51 | 1 |

---

## Giai đoạn 1 — Khởi động và chốt tính mới (09/10–18/10)

### B01 · Thu hồi khóa API đã lộ, tạo `.env`

**Cần xong trước:** không (làm ngay) · **Thời lượng:** 0,5 giờ

**Mục đích:** an toàn tài khoản; không liên quan nội dung nghiên cứu.

**Cần có trong tay:** tài khoản nhà cung cấp cũ; `.gitignore`.

**Làm:**

1. Vào trang quản lý khóa, thu hồi khóa cũ
2. Tạo khóa mới với hạn mức chi tiêu (nếu nhà cung cấp hỗ trợ)
3. Ghi vào `.env` cục bộ
4. Kiểm `git check-ignore .env` trả về `.env`
5. Ghi ngày thu hồi vào lab notebook (không ghi khóa).
- **Mẫu:** `.env`: `PROVIDER_API_KEY=...` (không bao giờ commit).

**Nếu vướng:** không đăng nhập được tài khoản cũ → liên hệ hỗ trợ nhà cung cấp; vẫn dùng tài khoản mới cho thí nghiệm. Có muốn dọn lịch sử Git không là quyết định riêng (QĐ12, tra cứu §14.2), không chặn nghiên cứu.

**Checklist bàn giao:**

- [ ] Khóa mới cục bộ
- [ ] Dòng nhật ký
- [ ] `git status` không thấy `.env`
- [ ] `git grep -n "sk-"` không có kết quả trong cây làm việc
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B02 · Đọc sổ tay, gửi câu hỏi GVHD

**Cần xong trước:** B01 · **Thời lượng:** 2–3 giờ

**Mục đích:** hiểu thiết kế trước khi làm; lấy các thông tin chỉ GVHD/Khoa cung cấp (hạn nộp, phiếu chấm, quy định AI, đồng ý thay đổi thiết kế).

**Cần có trong tay:** file tra cứu, đề cương `Đọc_báo_cùng_HuP_4_.docx`, bảng QĐ1–QĐ12 (tra cứu §14.2), mẫu email tra cứu Phụ lục A.

**Làm:**

1. Đọc Phần I của file tra cứu (tra cứu §1–3), sau đó đọc lướt Phần II (tra cứu §5–10): đọc kỹ tra cứu §5 (hướng dẫn nhãn) và tra cứu §6.2 (thuật toán P). Ghi mọi chỗ chưa hiểu vào `notes/lab_notebook.md` mục “câu hỏi”.
2. Mở bảng QĐ1–QĐ12 (tra cứu §14.2), đánh dấu các quyết định có cột “Cần xác nhận” = GVHD.
3. Gửi email theo tra cứu Phụ lục A kèm đề cương `Đọc_báo_cùng_HuP_4_.docx`; hỏi đúng 5 việc: thay đổi thiết kế, quy mô theo pilot, hãng thứ hai, hạn nộp/bảo vệ, quy định khai báo AI/phiếu chấm.
4. Ghi ngày gửi và câu trả lời (nguyên văn hoặc tóm tắt có ngày) vào cột “Trạng thái” của bảng QĐ (chép bảng sang `notes/decisions.md` để cập nhật).
- **Mẫu:** phụ lục A.

**Nếu vướng:** GVHD chưa trả lời → không dừng; tiếp tục B03–B10 (không phụ thuộc xác nhận), nhắc lại sau một tuần. GVHD yêu cầu giữ thiết kế cũ → so sánh với bảng đối chiếu thay đổi (lịch sử Git (bản 7107507)), sửa sổ tay theo ý kiến và ghi lý do.

**Checklist bàn giao:**

- [ ] Email đã gửi
- [ ] `notes/lab_notebook.md` có mục câu hỏi
- [ ] `notes/decisions.md` có trạng thái từng QĐ
- [ ] Có bản ghi ngày gửi
- [ ] Mọi QĐ “cần GVHD” có trạng thái `đã hỏi` hoặc `đã xác nhận (ngày)`
- [ ] Đạt điều kiện xong: mọi QĐ “GVHD” có trạng thái
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B03 · Đọc, ghi chép bài báo gần nhất

**Cần xong trước:** B02 · **Thời lượng:** 8–12 giờ · **Ghi chú:** đọc theo tra cứu §2.2

**Mục đích:** có căn cứ cho Chương 2 và cho bảng đối chiếu B1; xác nhận những nhận xét AI đã soạn.

**Cần có trong tay:** `báo/[1]–[6].pdf`, `báo/báo con1/2003.00744v3.pdf` (PhoBERT), [12] VitaminC (aclanthology.org/2021.naacl-main.52), [13] arXiv 2610.00689, SynthAVE arXiv 2607.07469, ghi chép sẵn ở tra cứu Phụ lục D. Bản dịch trong `dịch/` chỉ để đọc nhanh; mọi số phải đối chiếu bản gốc.

**Làm:**

1. Với mỗi bài, trả lời 8 câu: bài toán; đơn vị đánh giá; nguồn bằng chứng; cơ chế quyết định; nhãn và cách xử lý thiếu/xung đột; chỉ số và bảng chính (ghi trang); hạn chế do tác giả nêu; điều KLTN kế thừa/khác.
2. Ghi vào `notes/reading/<mã bài>.md` theo mẫu bên dưới, mỗi số liệu kèm “tr. X, Bảng Y”.
3. Đối chiếu với tra cứu Phụ lục D: đánh dấu từng dòng `đã kiểm (ngày)` trong ghi chép của bạn hoặc sửa nếu lệch. Ba ô trong bảng tự kiểm ở cuối tra cứu Phụ lục D — [2] Bảng 1 tr. 3, [3] Bảng 1 tr. 7, [5] Bảng 2 tr. 9 — phải được tự kiểm.
4. Với [12], [13], SynthAVE: đọc toàn văn; nếu chỉ đọc được tóm tắt thì ghi rõ giới hạn.
5. Chuyển mỗi nhận xét thành yêu cầu: ví dụ “CoVer ánh xạ insufficient → Refuted” → yêu cầu “KLTN giữ NEI riêng; TN2 báo NEI→S riêng”.
- **Mẫu:**
```markdown
# [5] CoVer — đọc ngày …
- Bài toán: … (tr. 2, tra cứu §1)
- Nhãn: nhị phân; insufficient → Refuted (tr. 5, tra cứu §3.1)
- Kết quả chính: Conflict: Acc 86,0 / Macro-F1 68,0 / BalAcc 64,5 (tr. 9, Bảng 2)
- Kế thừa: lưu hai phía xung đột → tra cứu §6.2 bước C1
- Khác: không có chiều điều kiện/vai trò → TN3
```

**Nếu vướng:** số trong tóm tắt bài khác bảng (đã gặp ở [3], [6]) → ghi số trong bảng và chú thích sự khác. Bài mới đổi phiên bản arXiv → ghi số phiên bản đã đọc.

**Checklist bàn giao:**

- [ ] `notes/reading/*.md` (mới) có dấu đã kiểm so với tra cứu Phụ lục D
- [ ] Danh mục tham khảo IEEE trong `thesis/references.bib` (danh sách [1]–[13] ở tra cứu Phụ lục D)
- [ ] Mỗi bài có đủ 8 câu và số trang
- [ ] `python3 scripts/check_paper_facts.py` PASS
- [ ] Không còn dòng “chưa xác nhận” cho số dùng trong luận văn
- [ ] Đạt điều kiện xong: đủ ghi chép bài ở tra cứu §2.2
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B04 · Lập bảng công trình gần nhất, kiểm lại tính mới

**Cần xong trước:** B03 · **Thời lượng:** 4–6 giờ

**Mục đích:** chứng minh vị trí đóng góp C\* bằng nguồn, không bằng tuyên bố.

**Cần có trong tay:** ghi chép B03; bảng ở tra cứu §2.2.

**Làm:**

1. Sao bảng ở tra cứu §2.2 sang `results/tables/B1_related_work.csv` với các cột: công trình, bài toán, đầu vào, cơ chế, đánh giá, kế thừa, điểm khác, thí nghiệm kiểm, nguồn (trang/bảng)
2. Sửa từng ô theo bản gốc
3. Với mỗi “điểm khác”, ghi thí nghiệm TN nào kiểm nó; nếu không có TN nào → hoặc bỏ điểm khác đó khỏi tuyên bố, hoặc thêm thí nghiệm (phải ghi lý do).
4. Kiểm riêng từng thành phần của SAV: (1) có bài nào neo từng trường thông số vào chuỗi nguyên văn rồi kiểm tất định chưa; (2) có bài nào coi vai trò con số và điều kiện thử là chiều phạm vi chưa. Ghi kết quả vào cột “Đã đọc” và “SAV cải tiến ở đâu” của tra cứu §2.2.
- **Mẫu:** hàng mẫu ở tra cứu §2.2.

**Nếu vướng:** phát hiện công trình đã làm gần như C\* → báo GVHD, thu hẹp C\* (ví dụ chỉ còn “đánh giá trong miền tai nghe tiếng Việt”) và sửa tra cứu §2.4; đây là kết quả hợp lệ của khảo sát.

**Checklist bàn giao:**

- [ ] `results/tables/B1_related_work.csv`
- [ ] Bảng 2.x trong luận văn
- [ ] Mọi hàng có nguồn trang/bảng
- [ ] Mọi “điểm khác” trỏ tới một TN hoặc ghi “chỉ bối cảnh”
- [ ] Đạt điều kiện xong: mỗi dòng có trang/bảng gốc; tra cứu §2.2 được cập nhật
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B05 · Chốt định nghĩa bài toán và QĐ

**Cần xong trước:** B04 · **Thời lượng:** 2–3 giờ

**Mục đích:** cố định đơn vị đánh giá, họ sản phẩm, chính sách nhãn và quy mô mục tiêu trước khi thu dữ liệu.

**Cần có trong tay:** tra cứu §1 và 3; bảng QĐ (tra cứu §14.2).

**Làm:**

1. Với QĐ1–QĐ12, ghi “đề xuất giữ” hoặc “đề xuất sửa” kèm lý do
2. Chỉ những QĐ có cột “Cần xác nhận = GVHD” mới chờ; các QĐ kỹ thuật sinh viên tự chốt và ghi ngày
3. Nếu sửa chính sách nhãn → sửa tra cứu §5 của file tra cứu **và** `docs/HUONG_DAN_GAN_NHAN.md` (bản máy đọc, phải giống hệt tra cứu §5), tăng phiên bản, chạy `python3 scripts/build_eval_prompts.py --apply` rồi `--check`, chạy unittest.
- **Mẫu:** hàng QĐ: `QĐ5 | Quy mô | test ≥ 4 họ, sàn R+NEI ≥ 40 | chốt theo pilot B30 | SV | đã chốt tạm 2026-10-..`.

**Nếu vướng:** GVHD muốn đổi chính sách `inherit_headline` → chính sách mới phải áp cho cả người gán và ba hệ thống; sửa code P và test tương ứng; không chọn chính sách theo kết quả hệ thống.

**Checklist bàn giao:**

- [ ] `notes/decisions.md` cập nhật
- [ ] Nếu đổi luật thì tra cứu §5 + `docs/HUONG_DAN_GAN_NHAN.md` + eval_prompts + test cập nhật
- [ ] `python3 -m unittest discover -s tests` PASS
- [ ] `build_eval_prompts.py --check` PASS
- [ ] Không QĐ nào ở trạng thái trống
- [ ] Đạt điều kiện xong: QĐ1–QĐ5 có trạng thái
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### Checklist bàn giao giai đoạn 1

- [ ] B01 · Thu hồi khóa API đã lộ, tạo `.env` — `.env` cục bộ; dòng nhật ký
- [ ] B02 · Đọc sổ tay, gửi câu hỏi GVHD — email; `notes/decisions.md`
- [ ] B03 · Đọc, ghi chép bài báo gần nhất — `notes/reading/*.md`
- [ ] B04 · Lập bảng công trình gần nhất, kiểm lại tính mới — bảng B1 (Chương 2); kết luận tính mới
- [ ] B05 · Chốt định nghĩa bài toán và QĐ — `notes/decisions.md` cập nhật
- [ ] **Mốc:** M1 — Tính mới đã kiểm: tra cứu §2.2 có cột “Đã đọc” = toàn văn cho mọi bài; GVHD đã trả lời QĐ1 hoặc đã ghi ngày hỏi
- [ ] Gửi GVHD tóm tắt 5 dòng: đã xong gì, số liệu chính, vướng gì, việc tiếp theo

---

## Giai đoạn 2 — Môi trường (19/10–22/10)

### B06 · Cài môi trường và cấu trúc repo

**Cần xong trước:** B05 · **Thời lượng:** 3–4 giờ

**Mục đích:** môi trường tái lập được cho mọi module.

**Cần có trong tay:** máy cá nhân (Linux/macOS/Windows + WSL), Python ≥ 3.11, Git.

**Làm:**

1. `python3 -m venv .venv && . .venv/bin/activate`.
2. Tạo `requirements.txt` khóa phiên bản: `rank-bm25==0.2.2`, `beautifulsoup4`, `lxml`, `pdfplumber` (PDF), `jsonschema`, `pyyaml`, `requests`, `matplotlib`, `pandas`; ghi đúng số phiên bản sau khi cài bằng `pip freeze | grep -i -E "bm25|beautifulsoup|lxml|pdfplumber|jsonschema|yaml|requests|matplotlib|pandas" > requirements.lock`.
3. Tạo thư mục theo tra cứu §9.1 và `kltn/__init__.py`; thêm `.env`, `.venv/` vào `.gitignore`.
4. Chạy `python3 -m unittest discover -s tests` để chắc mọi test hiện có PASS trong môi trường mới.
- **Mẫu:** kiến thức cần: Python cơ bản (hàm, dict, JSON), dòng lệnh, Git commit/branch. Không cần GPU.

**Nếu vướng:** thư viện không cài được trên Windows → dùng WSL; `pdfplumber` lỗi → dùng `pdftotext` (Poppler) và ghi lựa chọn.

**Checklist bàn giao:**

- [ ] `requirements.txt`, `requirements.lock`, cây thư mục, `kltn/`
- [ ] Venv mới trên máy sạch: `pip install -r requirements.lock` + unittest PASS
- [ ] Đạt điều kiện xong: test hiện có PASS
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B07 · Chọn mô hình, chạy thử một mẫu

**Cần xong trước:** B01, B06 · **Thời lượng:** 4–6 giờ

**Mục đích:** chọn mô hình theo khả năng thật; đo độ trễ, lỗi JSON và chi phí trên 5 ví dụ, không trên test.

**Cần có trong tay:** `templates/eval_prompts.json` (nội dung ở tra cứu Phụ lục C), `evidence/2026-10-08/examples.json` (5 ca: EX-02, EX-06, EX-10, EX-11, EX-18 — chỉ là ví dụ), danh sách ứng viên dưới đây.

**Làm:**

1. **Ứng viên mô hình quyết định/trích xuất (D):** một mô hình trọng số mở có hỗ trợ tiếng Việt được tài liệu mô hình nêu rõ, cỡ 7–14B, ví dụ Qwen2.5-7B/14B-Instruct; Llama-3.1-8B-Instruct là phương án thay thế (tài liệu mô hình Llama 3.1 liệt kê 8 ngôn ngữ hỗ trợ chính thức, không có tiếng Việt — cần kiểm lại khi chọn). Lý do chọn trọng số mở: tái lập được, chạy local được nếu API đổi. Tên phiên bản, giá và khả năng truy cập **chưa xác minh**; ghi đúng tên nhà cung cấp trả về.
2. **Ứng viên mô hình sinh quảng cáo (G):** một mô hình chat thương mại phổ biến mà người làm marketing thật hay dùng (ví dụ dòng GPT-4o-mini hoặc Gemini Flash), **khác họ** với D để giảm vòng lặp “LLM tự kiểm LLM”. Chưa xác minh giá/hạn mức.
3. Với mỗi D ứng viên: gửi prompt B1 cho 5 ví dụ (dùng hồ sơ trong fixture), temperature 0, lưu thông điệp/phản hồi/token/độ trễ vào `runs/smoke-<ngày>/`, theo mẫu manifest ở tra cứu Phụ lục C (`templates/run_manifest.json`).
4. Đo: tỷ lệ JSON hợp lệ; trường `label` hợp lệ; độ trễ trung vị; token vào/ra; chi phí ước tính.
5. Chọn D chính theo thứ tự: (a) cửa sổ ngữ cảnh đủ cho hướng dẫn + k đoạn không cắt bớt; (b) JSON hợp lệ ≥ 95% sau một lần thử lại; (c) chi phí/độ trễ trong ngân sách. **Không** chọn theo việc mô hình đoán đúng nhãn 5 ví dụ (quá ít, và đó không phải tiêu chí công bằng).
- **Mẫu:** công thức chi phí CT11 (tra cứu §8.2).

**Nếu vướng:** nhà cung cấp không trả mã mô hình thực → ghi `model_returned_id: unavailable`; không có seed → ghi trạng thái; cửa sổ ngữ cảnh thiếu → loại mô hình đó, không cắt hướng dẫn.

**Checklist bàn giao:**

- [ ] `configs/models.yaml` (`decision_model`, `generator_model`, nhà cung cấp, endpoint không chứa khóa, tham số)
- [ ] `runs/smoke-*/manifest.json`
- [ ] Ghi QĐ6 (tra cứu §14.2)
- [ ] 5/5 lượt có manifest đủ trường (trường không biết ghi `unavailable` + lý do)
- [ ] `check_input_leak.py --kind b1` PASS trên payload đã gửi
- [ ] Đạt điều kiện xong: smoke test 5 ví dụ có manifest
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### Checklist bàn giao giai đoạn 2

- [ ] B06 · Cài môi trường và cấu trúc repo — venv, `requirements.txt`, thư mục tra cứu §9.1
- [ ] B07 · Chọn mô hình, chạy thử một mẫu — `configs/models.yaml`, `runs/smoke-*`
- [ ] **Mốc:** Smoke test 5 ví dụ chạy hết B0/B1/P có manifest
- [ ] Gửi GVHD tóm tắt 5 dòng: đã xong gì, số liệu chính, vướng gì, việc tiếp theo

---

## Giai đoạn 3 — Nguồn cho 2 họ pilot (23/10–01/11)

### B08 · Kiểm kê họ AirPods và Beats

**Cần xong trước:** B05 · **Thời lượng:** 2–3 giờ · **Ghi chú:** có thể làm xen kẽ với B06–B07

**Mục đích:** chọn họ có đủ nguồn chính thức cho các thuộc tính trong phạm vi; tránh chọn họ thiếu dữ liệu rồi phải bỏ.

**Cần có trong tay:** trang thông số Apple đã có (5 trang trong `evidence/2026-10-08/`); trang hãng thứ hai.

**Làm:**

1. Lập danh sách ứng viên: Apple (AirPods 2, AirPods 4 / 4 ANC, AirPods 5, AirPods Pro 2, AirPods Pro 3, AirPods Max 2 — kiểm còn trang chính thức); hãng thứ hai có trang thông số tiếng Việt hoặc tiếng Anh chính thức (ứng viên: Sony, Samsung, JBL; chọn hãng có trang thông số dạng bảng và có chú thích điều kiện pin).
2. Với mỗi ứng viên, tìm bằng Google/Bing: `site:<domain chính thức> <tên sản phẩm> thông số` và `… specifications`, `… user guide pdf`. Nguồn chính thức = tên miền của hãng hoặc trang hỗ trợ của hãng; không dùng trang bán lẻ/báo.
3. Điền D1 `data/families.csv`: có trang thông số? có hướng dẫn sử dụng/hỗ trợ? thuộc tính nào có số? có chú thích điều kiện pin? thị trường nào?
4. Quy tắc chọn: giữ họ có ≥ 3/5 thuộc tính có số liệu chính thức; ưu tiên thị trường VN, nếu không có thì trang toàn cầu/US cho đúng mẫu và ghi `market_substitute=true` (QĐ2, tra cứu §14.2). Mục tiêu 10–12 họ; tối thiểu 6.
5. Gộp các biến thể dùng chung trang/thế hệ vào một họ (ví dụ AirPods 4 và AirPods 4 ANC).
6. Thêm 4 họ Beats từ trang chính thức beatsbydre.com (ví dụ Powerbeats Pro 2, Beats Studio Pro, Beats Solo 4, Beats Fit Pro — kiểm lại danh sách đang bán ở ngày thu); ghi `brand=Beats`. Nếu thấy trang thông số văn bản của hãng độc lập, ghi vào D1 như họ tùy chọn.
- **Mẫu:** hàng D1 ở tra cứu §9.2.

**Nếu vướng:** trang hãng thứ hai chặn trình duyệt tự động → chụp thủ công (ghi `capture_method: manual browser`); trang chỉ có ảnh, không có văn bản → không dùng (phạm vi là văn bản), ghi `status=image_only`.

**Checklist bàn giao:**

- [ ] `data/families.csv` (D1)
- [ ] Mỗi họ có ≥ 1 URL chính thức truy cập được
- [ ] Cột thuộc tính không trống
- [ ] Số họ ≥ 6, có ≥ 1 hãng ngoài Apple hoặc đã ghi lý do không có
- [ ] Đạt điều kiện xong: 10 họ (≈ 6 AirPods + 4 Beats) có trạng thái nguồn
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B09 · Thu nguồn, snapshot cho 2 họ pilot

**Cần xong trước:** B08 · **Thời lượng:** 3–6 giờ

**Mục đích:** kho nguồn cố định, có hash, truy vết được tới từng đoạn.

**Cần có trong tay:** D1; `scripts/capture_evidence.mjs` (Playwright, đã dùng ngày 08/10); `evidence/2026-10-08/` để chuyển sang kho.

**Làm:**

1. Với mỗi URL: chạy `node scripts/capture_evidence.mjs` (sửa danh sách URL trong script hoặc thêm tham số) để lưu `response.html`, `page.html`, `page.txt`, ảnh toàn trang và metadata. Với PDF: tải về `raw.pdf`, ghi SHA-256.
2. Đặt vào `data/corpus/<source_id>/`; `source_id = <hãng>-<sản phẩm>-<thị trường>[-<loại>]`, ví dụ `apple-max2-vn`, `apple-max2-vn-manual`.
3. Ghi một dòng D2 `data/sources.csv`: URL yêu cầu/cuối, thị trường, ngôn ngữ, thời điểm UTC, cách chụp, hash.
4. Mở `page.txt`, đối chiếu với trang thật: các khối Pin, Kích thước và trọng lượng, Kết nối, chú thích có đủ không. Nếu thiếu chú thích (do JS) → chụp lại sau khi mở rộng phần chú thích.
5. Chuyển 5 nguồn Apple cũ: sao chép nguyên thư mục, giữ hash; ghi `supersedes` nếu chụp lại bản mới.
6. Đủ hồ sơ nguồn khi: có trang thông số + đã tìm hướng dẫn sử dụng/hỗ trợ (có hoặc ghi `not_found` kèm từ khóa đã tìm). Không ép mọi thị trường thành một bản; mỗi bản là một `source_id`.
- **Mẫu:** `evidence/2026-10-08/apple-max2-vn/metadata.json` (captured_at_utc `2026-10-08T02:34:06.198Z`, SHA-256 page.txt `2a649d31…`).

**Nếu vướng:** trang đổi nội dung giữa hai lần chụp → giữ cả hai bản, chọn bản theo ngày khóa corpus, ghi lý do; trang chuyển hướng sang thị trường khác → ghi `final_url`, đánh dấu market thực.

**Checklist bàn giao:**

- [ ] `data/corpus/*` (D3), `data/sources.csv` (D2)
- [ ] Script kiểm (M13 `validate_data.py --sources`) xác nhận mọi file có hash khớp, mọi `source_id` trong D2 có thư mục
- [ ] Đọc thủ công 1 trang/họ thấy đủ chú thích pin
- [ ] Đạt điều kiện xong: mỗi nguồn có URL, ngày, SHA-256
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B10 · Trích văn bản có cấu trúc (M1)

**Cần xong trước:** B09 · **Thời lượng:** 5–7 giờ

**Mục đích:** giữ mỗi con số cùng tiêu đề mục, ô bảng, bộ phận, chế độ và chú thích để B và A có thông tin.

**Cần có trong tay:** `page.html` / `raw.pdf`.

**Làm:**

1. HTML: dùng BeautifulSoup; duyệt cây theo thứ tự; mỗi tiêu đề `h2/h3/h4` hoặc khối có vai trò tiêu đề cập nhật `heading_path`; mỗi dòng thông số (`p`, `li`, ô bảng) thành một “đơn vị văn bản” kèm `heading_path` hiện tại.
2. Chú thích: nhận số chú thích ở cuối dòng (ví dụ “Chủ Động Khử Tiếng Ồn10” → văn bản “…Ồn” + `footnote_ids=["10"]`); tìm khối chú thích cuối trang, ánh xạ số → nội dung. Không xóa số chú thích khỏi văn bản gốc; lưu cả bản gốc `raw_text`.
3. Bảng: mỗi ô thành “<tiêu đề cột>: <tiêu đề hàng>: <giá trị>”.
4. PDF: `pdfplumber` theo trang; giữ số trang; tiêu đề nhận bằng cỡ chữ lớn hơn thân bài (ghi ngưỡng).
5. Chuẩn hóa *chỉ trình bày*: Unicode NFC, khoảng trắng; **không** đổi dấu thập phân, không bỏ ký hiệu `≥ ≤ > <`, không bỏ từ phủ định, không dịch.
- **Mẫu:** dòng `Thời gian nghe lên đến 20 giờ với một lần sạc khi bật tính năng Chủ Động Khử Tiếng Ồn10` dưới “Pin › AirPods Max 2 (sạc đầy)” → `{"heading_path": ["Pin","AirPods Max 2 (sạc đầy)"], "text": "Thời gian nghe lên đến 20 giờ … Chủ Động Khử Tiếng Ồn", "footnote_ids": ["10"], "raw_text": "…Ồn10"}`.

**Nếu vướng:** số chú thích dính vào số liệu (“20 giờ10”) → regex chỉ tách số chú thích ở cuối đơn vị khi số đó có trong danh sách chú thích; “AirPods 4” — số 4 là tên sản phẩm, không phải chú thích → chỉ tách sau chữ không phải tên sản phẩm; nghi ngờ → giữ nguyên và đánh dấu `footnote_ambiguous=true` để kiểm tay.

**Checklist bàn giao:**

- [ ] `kltn/extract_text.py` (M1)
- [ ] `data/corpus/<source_id>/units.jsonl`
- [ ] Test `tests/test_extract_text.py` trên `evidence/2026-10-08/apple-max2-vn/page.html`: tìm được dòng 20 giờ với `footnote_ids=["10"]`, chú thích 10 chứa “Âm lượng được đặt ở mức 50%”
- [ ] Số đơn vị khác rỗng
- [ ] Với mỗi nguồn, 100% dòng chứa số trong `page.txt` xuất hiện trong `units.jsonl` (kiểm độ phủ B12)
- [ ] Đạt điều kiện xong: test M1 PASS
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B11 · Chia đoạn, sinh mã đoạn (M2)

**Cần xong trước:** B10 · **Thời lượng:** 4–6 giờ

**Mục đích:** đơn vị truy hồi đủ nhỏ để BM25 phân biệt, đủ lớn để giữ điều kiện.

**Cần có trong tay:** `units.jsonl`.

**Làm:**

1. Đơn vị index mặc định = **một đơn vị văn bản + tiêu đề** (một dòng thông số). Văn bản đưa vào BM25 = `" › ".join(heading_path) + " | " + text + " | " + " ".join(footnotes)`.
2. Chú thích được gắn vào đoạn bằng `footnote_ids`, nội dung chú thích đưa vào trường `footnotes` của đoạn (để B0 đọc và trích xuất thấy điều kiện thử).
3. Khử trùng: hai đoạn cùng `source_id` và cùng `text_sha256` → giữ một, ghi `dup_of`. Không khử trùng giữa các nguồn khác nhau (cần cho phát hiện xung đột).
4. `chunk_id = opaque('k', source_id, str(char_start), text)`.
5. Ghi D4 `data/chunks.jsonl`; `chunker_version` ghi vào khóa.
- **Mẫu:** bản ghi D4 ở tra cứu §9.2.

**Nếu vướng:** một thông số trải hai dòng (số ở dòng 1, điều kiện ở dòng 2) → gộp hai đơn vị liền nhau cùng `heading_path` nếu dòng 2 không có số; ghi quy tắc vào `chunker_version`.

**Checklist bàn giao:**

- [ ] `kltn/chunk.py` (M2)
- [ ] `data/chunks.jsonl` (D4)
- [ ] Mọi `chunk_id` duy nhất
- [ ] Mọi đoạn trỏ về `source_id` có trong D2
- [ ] `char_start/char_end` cắt đúng `text` trong `page.txt` (nếu là HTML) — kiểm bằng M13
- [ ] Đạt điều kiện xong: mã đoạn ổn định, không trùng
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B12 · Kiểm độ phủ nguồn

**Cần xong trước:** B11 · **Thời lượng:** 1–2 giờ

**Mục đích:** phát hiện số liệu/điều kiện bị mất khi trích và chia đoạn — lỗi này nếu không bắt sẽ bị đếm sai thành lỗi truy hồi.

**Cần có trong tay:** `page.txt`, `chunks.jsonl`.

**Làm:**

1. Liệt kê mọi dòng trong `page.txt` có số + đơn vị (regex `\d+([.,]\d+)?\s*(giờ|phút|gram|g|mm|%)` hoặc “Bluetooth \d”)
2. Kiểm mỗi dòng có trong ít nhất một đoạn
3. Kiểm mọi số chú thích trong dòng thông số có nội dung chú thích
4. Ghi báo cáo `results/tables/coverage_<source_id>.csv`: dòng, có/không, chunk_id.
- **Mẫu:** dòng “5 phút sạc đem đến thời gian nghe khoảng 1,5 giờ11” phải nằm trong một đoạn có `footnote_ids=["11"]`.

**Nếu vướng:** dòng số là năm/mã model (“2026”, “A3184”) → danh sách loại trừ có lý do.

**Checklist bàn giao:**

- [ ] Báo cáo độ phủ
- [ ] Cột `coverage_ok` trong D2
- [ ] 100% dòng số có đoạn
- [ ] 100% chú thích được ánh xạ hoặc có ghi chú lý do
- [ ] Đạt điều kiện xong: độ phủ 100% thuộc tính đã chọn
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### Checklist bàn giao giai đoạn 3

- [ ] B08 · Kiểm kê họ AirPods và Beats — D1 `data/families.csv`
- [ ] B09 · Thu nguồn, snapshot cho 2 họ pilot — D2, D3 cho 2 họ
- [ ] B10 · Trích văn bản có cấu trúc (M1) — `units.jsonl` 2 họ
- [ ] B11 · Chia đoạn, sinh mã đoạn (M2) — D4 2 họ
- [ ] B12 · Kiểm độ phủ nguồn — báo cáo độ phủ
- [ ] **Mốc:** D1–D4 cho 2 họ pilot, độ phủ 100%
- [ ] Gửi GVHD tóm tắt 5 dòng: đã xong gì, số liệu chính, vướng gì, việc tiếp theo

---

## Giai đoạn 4 — Dữ liệu pilot (02/11–09/11)

### B13 · Chốt giao thức, prompt sinh quảng cáo

**Cần xong trước:** B07 · **Thời lượng:** 2–3 giờ

**Mục đích:** có quảng cáo LLM “thông thường” với log đầy đủ, để kết quả trên tập thông thường phản ánh cách dùng thật.

**Cần có trong tay:** `configs/models.yaml`; D1; tài liệu nguồn (cho điều kiện g2).

**Làm:**

1. Cố định **hai điều kiện sinh**, đều không yêu cầu tạo lỗi: `g1_name_only` — mô hình chỉ được biết tên sản phẩm (lỗi xuất hiện tự nhiên do mô hình nhớ sai/cũ); `g2_with_spec` — mô hình được đưa bảng thông số rút gọn chép nguyên từ `page.txt` (mô phỏng marketer dán thông số). Ghi điều kiện vào D5.
2. Prompt mẫu (lưu `templates/ad_prompts.json`, có SHA-256; bản đầy đủ ở tra cứu Phụ lục C):
   ```text
   [g1] Bạn là người viết quảng cáo cho một cửa hàng điện tử tại Việt Nam. Viết một đoạn quảng cáo
   tiếng Việt khoảng 120–180 từ cho sản phẩm "{product}". Nêu cụ thể các thông số nổi bật như thời
   lượng pin, sạc, trọng lượng, chống ồn và kết nối. Giọng văn hấp dẫn, tự nhiên.
   [g2] … như trên … Dùng thông tin sản phẩm sau:
   <SPEC>{spec_excerpt}</SPEC>
   ```
   Không thêm câu “hãy nói sai”, “phóng đại”.
3. Tham số: temperature 0,7 (đa dạng câu chữ), top_p 1, max_tokens 400; seed nếu nhà cung cấp hỗ trợ (ghi số), nếu không ghi `unsupported`.
4. Lô: mỗi lô = mỗi họ × 3 quảng cáo g1 + 3 quảng cáo g2. Lô 0 chỉ chạy trên 2 họ dev.
5. Quy tắc dừng chốt trước (chỉ dựa trên số claim hợp lệ, **không** dựa trên nhãn hay dự đoán): dừng sinh cho một họ khi đạt mục tiêu claim thông thường của họ (mục tiêu chia đều từ bảng ở tra cứu §3.4, ví dụ 12–16 claim/họ test), hoặc đã chạy 3 lô, hoặc chạm ngân sách G (QĐ7, tra cứu §14.2).
- **Mẫu:** D5 theo mẫu ở tra cứu Phụ lục C.

**Nếu vướng:** g1 cho quá ít thông số (mô hình từ chối nêu số) → vẫn giữ output; số claim/quảng cáo thấp được dùng để tính số quảng cáo cần sinh.

**Checklist bàn giao:**

- [ ] `templates/ad_prompts.json` (đã chốt, có hash)
- [ ] Quy tắc sinh khớp tra cứu §7.2
- [ ] Prompt có hash
- [ ] Không có từ yêu cầu tạo lỗi
- [ ] Đã ghi quy tắc dừng trước khi chạy lô 1
- [ ] Đạt điều kiện xong: prompt có mã băm
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B14 · Sinh quảng cáo lô pilot (M3)

**Cần xong trước:** B13 · **Thời lượng:** 2–3 giờ

**Mục đích:** tạo D5 có provenance.

**Cần có trong tay:** prompt, `configs/models.yaml`, D1.

**Làm:**

1. Chạy `python -m kltn.generate_ads --batch 0 --families <dev1>,<dev2>`
2. Script lưu mỗi quảng cáo vào `data/ads/<ad_id>.json` gồm prompt render, phản hồi thô, SHA-256, model trả về, thời điểm
3. Không chạy lại để “lấy bản đẹp hơn”; lỗi kỹ thuật (timeout, rỗng) → ghi `exclusion.excluded=true` + lý do, chạy lại một lần với `retry_of`.
- **Mẫu:** `ad_id = opaque('a', family_id, batch, str(index), condition)`.

**Nếu vướng:** nhà cung cấp đổi mô hình giữa các lô → ghi thay đổi; báo theo lô.

**Checklist bàn giao:**

- [ ] `kltn/generate_ads.py` (M3)
- [ ] `data/ads/*.json` (D5)
- [ ] Dòng nhật ký lô trong lab notebook (ngày, số quảng cáo, lỗi, chi phí)
- [ ] Số file = số yêu cầu
- [ ] Mọi file có `raw_ad_sha256` khớp `raw_ad_text`
- [ ] Không có khóa API trong file (`grep -r "Authorization" data/ads` rỗng)
- [ ] Đạt điều kiện xong: mọi quảng cáo có log đủ
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B15 · Tách phát biểu lô pilot

**Cần xong trước:** B14 · **Thời lượng:** 2–3 giờ

**Mục đích:** đơn vị đánh giá đúng nghĩa, giữ chủ thể và điều kiện.

**Cần có trong tay:** D5; tra cứu §5.1 (phạm vi thuộc tính).

**Làm:**

1. Đọc quảng cáo; đánh dấu mọi câu/mệnh đề có thông số thuộc 5 thuộc tính.
2. Một claim = một mệnh đề có chủ thể + thông số + điều kiện của nó. Câu có hai thông số độc lập (“pin 6 giờ và nặng 5,3 g”) → tách hai claim; câu có một thông số nhiều điều kiện → giữ một claim.
3. Chủ thể bị ẩn (“Tai nghe còn…”) → thay bằng chủ thể trong ngữ cảnh *chỉ khi rõ ràng*, ghi `text_edit=presentation_only` và mô tả (“thêm chủ thể ‘AirPods Max 2’ từ câu trước”). Không thêm điều kiện, không sửa số, không đổi từ định tính (“lên đến”, “chính xác”).
4. Ghi `char_start/char_end` vào quảng cáo gốc (đoạn chứa mệnh đề), `claim_text`, `group=ordinary_llm`, `ad_id`.
5. Ngoài phạm vi (cảm tính, so sánh với đối thủ, thuộc tính khác như chống nước/giá): ghi `in_scope=false` + lý do theo danh sách cố định (`subjective`, `comparative`, `other_attribute`, `no_number`), không xóa.
- **Mẫu:** quảng cáo giả định: “…AirPods Max 2 mang lại tới 20 giờ nghe nhạc liên tục kể cả khi tắt chống ồn, sạc nhanh 5 phút cho khoảng 1,5 giờ…” → claim 1 “AirPods Max 2 mang lại tới 20 giờ nghe nhạc liên tục kể cả khi tắt chống ồn” (`verbatim`); claim 2 “sạc nhanh 5 phút cho khoảng 1,5 giờ” → `presentation_only`: thêm chủ thể “AirPods Max 2”.

**Nếu vướng:** mệnh đề mơ hồ chủ thể (hộp hay tai nghe?) → giữ nguyên văn, không đoán; nhãn sẽ do nguồn quyết định (thường NEI). Một quảng cáo lặp lại cùng claim → giữ lần đầu, lần sau `dedup_of`.

**Checklist bàn giao:**

- [ ] Dòng `group=ordinary_llm` trong D6 `data/claims.jsonl`
- [ ] M13 kiểm `claim_text` (bỏ phần thêm chủ thể) là chuỗi con của quảng cáo tại vị trí ghi
- [ ] Mọi claim có `in_scope`
- [ ] Ghi `minutes` vào D12
- [ ] Đạt điều kiện xong: mỗi claim có claim_id, bấm giờ
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B16 · Tạo biến thể cặp tối thiểu lô pilot

**Cần xong trước:** B15 · **Thời lượng:** 2–3 giờ · **Ghi chú:** tạo tập chẩn đoán

**Mục đích:** đo trực tiếp lỗi lệch phạm vi theo từng loại — cốt lõi của RQ2/RQ3.

**Cần có trong tay:** D6 + D7 của câu cha; nguồn.

**Làm:**

1. Chọn câu cha: claim `ordinary_llm` có nhãn **Supported**; nếu một thuộc tính trong họ không có câu cha Supported, tạo câu cha `seed_manual` bằng cách chép một dòng thông số thành câu khẳng định (ghi rõ nhóm này, không tính vào tập thông thường).
2. Với mỗi câu cha, tạo **một biến thể cho mỗi loại áp dụng được**, sửa đúng một yếu tố:
   - `COND`: đổi/thêm điều kiện (“khi bật chống ồn” → “khi tắt chống ồn”).
   - `PART`: đổi bộ phận (“tai nghe nặng 386,2 g” → “Smart Case nặng 386,2 g”).
   - `ROLE`: đổi vai trò con số (“lên đến 20 giờ” → “luôn đạt đúng 20 giờ” / “chính xác 20 giờ”).
   - `VAL`: đổi giá trị (“20 giờ” → “25 giờ”; “Bluetooth 5.3” → “5.2”).
   - `PROD`: đổi sang sản phẩm cùng hãng, khác thế hệ, giữ nguyên số.
   - `BOUND`: đổi bất đẳng thức (“hơn 24 giờ” → “24 giờ”).
3. Ghi D6: `group=controlled_variant`, `parent_claim_id`, `mutation_type`, `mutation_note`, `editor`, `created_at`. **Không** ghi nhãn kỳ vọng ở D6.
4. Gán nhãn biến thể ở B18 bằng cách đọc nguồn như mọi claim. Thao tác không quyết định nhãn: đổi số có thể vẫn Supported nếu nguồn có số đó ở chế độ khác (ví dụ AirPods 5: 4 giờ bật chống ồn, 6 giờ tắt).
5. Câu cha và mọi biến thể luôn cùng họ → cùng tập (B35).
- **Mẫu:** xem tra cứu §11.3.

**Nếu vướng:** biến thể vô nghĩa (Bluetooth “khi tắt chống ồn”) → không tạo; ghi “không áp dụng”. Biến thể trùng một claim thông thường đã có → giữ cả hai nhưng ghi `dedup_of` để không đếm hai lần.

**Checklist bàn giao:**

- [ ] Dòng `controlled_variant` trong D6
- [ ] Mọi biến thể có `parent_claim_id` tồn tại và cùng `family_id`
- [ ] Đếm theo `mutation_type` × tập đạt mục tiêu ở tra cứu §3.4
- [ ] Câu biến thể không chứa từ lộ thao tác (“sai”, “biến thể”) — `check_input_leak` bắt khi tạo payload
- [ ] Đạt điều kiện xong: ≥ 2 biến thể mỗi loại COND/PART/ROLE
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B17 · Kiểm trùng, loại ngoài phạm vi

**Cần xong trước:** B16 · **Thời lượng:** 1 giờ

**Mục đích:** danh sách claim cố định trước khi chạy hệ thống; tránh chọn mẫu sau khi thấy kết quả.

**Cần có trong tay:** D6.

**Làm:**

1. Trùng chính xác sau chuẩn hóa khoảng trắng/chữ hoa trong cùng họ → `dedup_of`
2. Gần trùng (cùng thuộc tính, cùng số, cùng điều kiện, khác câu chữ) → giữ, gắn `near_dup_group` để khi bootstrap không coi là độc lập hoàn toàn
3. Đếm theo họ × nhóm × `in_scope`
4. Ghi bảng tổng hợp vào lab notebook.
- **Mẫu:** lệnh `python -m kltn.validate_data --claims` in bảng đếm.

**Nếu vướng:** phát hiện lỗi tách sau khi đã gán nhãn → sửa claim thành phiên bản mới (`revision_of`), gán nhãn lại; không sửa đè.

**Checklist bàn giao:**

- [ ] D6 đã gắn cờ
- [ ] Bảng đếm
- [ ] M13 PASS
- [ ] Không claim nào bị xóa khỏi file (chỉ gắn cờ)
- [ ] Đạt điều kiện xong: không còn claim trùng
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B18 · Gán nhãn tham chiếu lô pilot

**Cần xong trước:** B12, B17 · **Thời lượng:** 4–6 giờ

**Mục đích:** nhãn chuẩn độc lập với mọi hệ thống.

**Cần có trong tay:** D6 (chỉ `claim_text`, `product`, `family_id` — **ẩn** `group`, `mutation_type` khi gán biến thể nếu được: dùng file xuất ẩn trường), D3/D4, hướng dẫn nhãn v2 (tra cứu §5).

**Làm:**

1. Xuất danh sách cần gán: `python -m kltn.annotate export --family <id> --hide group,mutation_type,parent_claim_id --shuffle 42` → `data/annotation/todo_<family>.csv`. Thứ tự xáo trộn để câu cha và biến thể không đứng cạnh nhau.
2. Với mỗi claim: bấm giờ bắt đầu; xác định sản phẩm/phiên bản, bộ phận, thuộc tính, điều kiện claim nêu, cách diễn đạt con số (tra cứu §5.5).
3. Mở `data/chunks.jsonl` (lọc `family_id`) hoặc `page.txt`; tìm theo mục (Pin, Kích thước, Kết nối) **và** theo từ khóa Việt–Anh; đọc chú thích của dòng tìm được.
4. Áp tra cứu §5.3 → 6.4 → 6.6 → 6.7 → 6.8 theo thứ tự; viết lý do một câu chỉ ra điểm khớp/khác/thiếu.
5. Ghi bộ bằng chứng chuẩn: danh sách `chunk_id` tối thiểu để kết luận (thường 1 đoạn; nhiều đoạn khi số và điều kiện ở hai đoạn, hoặc khi xung đột cần cả hai phía). Có thể có nhiều bộ thay thế (hai nguồn cùng nói một điều).
6. NEI-missing → bắt buộc B19 trước khi `status=final`. Chưa chắc → `status=pending_review` + câu hỏi trong `unresolved_question`.
7. Bấm giờ dừng, ghi `minutes`.
- **Mẫu:** tra cứu §11.4 (bản ghi D7 cho claim AirPods Max 2).

**Nếu vướng:** - Khác sản phẩm (claim AirPods 4 nhưng số của AirPods 4 ANC) → không dùng số đó; thường NEI hoặc Refuted nếu đúng sản phẩm có số khác. - Khác chế độ → tra cứu §5.4 (ý 1); mức tối đa/khoảng/gần đúng → tra cứu §5.5–5.6. - Xung đột thật (hai trang chính thức cùng phạm vi khác số) → NEI-conflict, ghi cả hai phía. - Trang lỗi/không truy cập → không gán NEI; `pending_review` + ghi nguồn lỗi (lỗi kỹ thuật thu nguồn). - Thấy hướng dẫn thiếu quy định → tra cứu §10.4 bước 3.

**Checklist bàn giao:**

- [ ] D7 `data/labels.jsonl`
- [ ] D12 thời gian
- [ ] M13: mọi claim `in_scope=true` có nhãn
- [ ] Mọi `chunk_id` trong `gold_evidence_sets` tồn tại và cùng họ
- [ ] Supported/Refuted có ≥ 1 bộ bằng chứng
- [ ] NEI-missing có search log
- [ ] `guide_sha256` khớp hướng dẫn hiện hành
- [ ] Đạt điều kiện xong: mọi claim có nhãn + bộ bằng chứng
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B19 · Nhật ký tìm nguồn cho NEI lô pilot

**Cần xong trước:** B18 · **Thời lượng:** 1–2 giờ

**Mục đích:** NEI phải là “đã tìm theo quy trình mà không có trong corpus”, không phải “không thấy từ khóa”.

**Cần có trong tay:** D2/D3 của họ; mẫu nhật ký NEI ở tra cứu Phụ lục C.

**Làm:**

1. Ghi phạm vi claim (sản phẩm, phiên bản, bộ phận, thuộc tính, điều kiện) và điều còn thiếu.
2. Kiểm **ba loại nguồn** trong corpus: trang thông số, hướng dẫn sử dụng, trang hỗ trợ/PDF. Loại nào không có trong corpus → ghi `not_in_corpus` + từ khóa đã tìm ở B09.
3. Với mỗi nguồn: đọc theo mục (không chỉ Ctrl+F); thử ≥ 3 từ khóa Việt và ≥ 2 tiếng Anh (ví dụ “tắt chống ồn”, “Chủ Động Khử Tiếng Ồn”, “ANC off”, “noise cancellation off”, “Khử tiếng ồn tắt”); ghi mục/chú thích đã đọc và kết quả.
4. Lý do dừng: “đã đọc đủ ba loại nguồn trong corpus; thông số ở điều kiện X không có”.
5. Chưa hoàn thành bước nào → `status=pending_review`.
- **Mẫu:** `evidence/2026-10-08/examples.json` EX-10 có `nei_search_log` một trang (chỉ minh họa; thiếu manual/support nên `production_label_ready=false`).

**Nếu vướng:** tìm thấy thông tin ở nguồn chính thức ngoài corpus → thêm nguồn vào corpus (phiên bản mới), gán lại claim; không giữ NEI cũ.

**Checklist bàn giao:**

- [ ] `data/search_logs/<claim_id>.json` (D8)
- [ ] Ba loại nguồn có trạng thái khác `pending`
- [ ] Có ≥ 5 từ khóa
- [ ] Có lý do dừng
- [ ] Đạt điều kiện xong: mọi NEI-missing có log
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### Checklist bàn giao giai đoạn 4

- [ ] B13 · Chốt giao thức, prompt sinh quảng cáo — `templates/ad_prompts.json` v1
- [ ] B14 · Sinh quảng cáo lô pilot (M3) — D5 lô 0 (2 họ × 6)
- [ ] B15 · Tách phát biểu lô pilot — D6 lô 0; `data/timing.csv`
- [ ] B16 · Tạo biến thể cặp tối thiểu lô pilot — D6 biến thể lô 0
- [ ] B17 · Kiểm trùng, loại ngoài phạm vi — D11 danh sách loại
- [ ] B18 · Gán nhãn tham chiếu lô pilot — D7 lô 0
- [ ] B19 · Nhật ký tìm nguồn cho NEI lô pilot — D8 lô 0
- [ ] **Mốc:** Lô pilot có nhãn, ≥ 2 biến thể mỗi loại COND/PART/ROLE, có số đo phút/claim
- [ ] Gửi GVHD tóm tắt 5 dòng: đã xong gì, số liệu chính, vướng gì, việc tiếp theo

---

## Giai đoạn 5 — Pipeline trên dev và pilot (10/11–23/11)

### B20 · BM25 lọc theo sản phẩm (M4)

**Cần xong trước:** B11 · **Thời lượng:** 5–7 giờ · **Ghi chú:** dùng D4 của B11

**Mục đích:** lấy k đoạn ứng viên cho mỗi claim; cùng output dùng cho B0, trích xuất (B1/P).

**Cần có trong tay:** D4; claim (`claim_text`, `product`, `family_id`).

**Làm:**

1. **Đơn vị index:** đoạn D4 (tiêu đề + dòng + chú thích, mục B11).
2. **Token hóa:** chữ thường, Unicode NFC; tách theo khoảng trắng và dấu câu; **giữ** số thập phân (“1,5” và “1.5” → cùng token `1.5`), giữ “5.3”, giữ ký hiệu `%`; không bỏ dấu tiếng Việt (bản thử: thêm một bản không dấu nếu dev cho thấy giúp — quyết định trên dev). Không dùng stopword cho từ phủ định (“không”, “tắt”).
3. **Từ điển mở rộng Việt–Anh** (tùy chọn, chốt trên dev): `pin→battery, thời gian nghe→listening time, sạc→charge, chống ồn|khử tiếng ồn→ANC|noise cancellation, trọng lượng|nặng→weight, hộp sạc→case`. Chỉ thêm token vào query, không thay.
4. **Lọc sản phẩm:** chỉ index đoạn có `family_id` của claim (thiết lập chính `product-filtered`).
5. **Query** = `claim_text` đã token hóa (giữ tên sản phẩm).
6. `rank_bm25.BM25Okapi` với k1=1,5, b=0,75 (mặc định thư viện; không tinh chỉnh trên test).
7. Lưu `runs/<run_id>/retrieval.jsonl`: `claim_id, N, k, k_eff, ranked_chunk_ids, scores`.
- **Mẫu:** query “AirPods Max 2 mang lại tới 20 giờ nghe nhạc liên tục kể cả khi tắt chống ồn” trong họ AirPods Max 2 → mong đợi đoạn “Pin › AirPods Max 2 (sạc đầy) | Thời gian nghe lên đến 20 giờ … khi bật …” ở hạng 1–2. Danh sách thật phải lấy từ output, không viết tay vào luận văn.

**Nếu vướng:** claim chỉ nêu “tai nghe” không nêu tên → query vẫn có `product` từ ngữ cảnh (ghép tên sản phẩm vào query), ghi quy tắc.

**Checklist bàn giao:**

- [ ] `kltn/bm25.py` (M4)
- [ ] File retrieval
- [ ] `tests/test_bm25.py`: token hóa giữ “1,5”→“1.5”, “5.3”
- [ ] Lọc không trả đoạn khác họ
- [ ] Với N<k, k_eff=N và trả đủ N đoạn
- [ ] Kết quả tất định (chạy hai lần giống nhau)
- [ ] Đạt điều kiện xong: test M4 PASS
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B21 · Đo recall@k trên dev, chọn k

**Cần xong trước:** B18, B20 · **Thời lượng:** 1–2 giờ

**Mục đích:** chọn k bằng dữ liệu dev; phân biệt lỗi chia đoạn/thu nguồn với lỗi xếp hạng.

**Cần có trong tay:** retrieval dev; D7 (gold sets).

**Làm:**

1. Mẫu số: claim dev có nhãn `final` **và** có ≥ 1 bộ bằng chứng chuẩn (Supported, Refuted, NEI-conflict). NEI-missing không vào mẫu số (không có bộ chuẩn).
2. Với k ∈ {3, 5, 8}: tính recall@k (CT5), báo riêng nhóm N ≤ k và N > k.
3. Claim không đạt ở mọi k: đọc từng ca, gắn mã `L-CHUNK` (bằng chứng bị cắt/thiếu khi chia đoạn), `L-SRC` (không có trong corpus), hoặc `L-RANK` (có nhưng xếp thấp).
4. Chọn k nhỏ nhất có recall@k ≥ 0,9 trên dev **và** tổng độ dài prompt B0 không vượt cửa sổ ngữ cảnh; nếu không k nào đạt 0,9, chọn k=8 và ghi giới hạn. Ghi `configs/retrieval.yaml`.
- **Mẫu:** dev 50 claim có bộ chuẩn: recall@3 = 41/50, @5 = 46/50, @8 = 48/50; 2 ca không đạt là `L-CHUNK` → sửa chunker (B11) trước khi chọn k.

**Nếu vướng:** sửa chunker sau khi đo → đo lại toàn dev; không đo trên test.

**Checklist bàn giao:**

- [ ] `configs/retrieval.yaml`
- [ ] `results/tables/dev_recall.csv` (không đưa vào kết quả chính)
- [ ] M11 tính khớp tay trên 5 claim
- [ ] Đạt điều kiện xong: k ghi vào cấu hình
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B22 · Schema σ có trường trích dẫn, prompt trích xuất

**Cần xong trước:** B05 · **Thời lượng:** 3–4 giờ · **Ghi chú:** có thể soạn xen kẽ với B13–B19

**Mục đích:** hồ sơ chung cho B1 và P, thuần dữ kiện.

**Cần có trong tay:** JSON Schema hồ sơ ở tra cứu Phụ lục C (`templates/extraction_schema.json`); tra cứu §5.5 (bảng đọc vai trò con số).

**Làm:**

1. Schema: `claim_record` (sản phẩm, phiên bản, thị trường hoặc null, bộ phận, `universal`, `condition_ref`, danh sách thuộc tính với `attribute ∈ {battery_single, battery_total, charge_time, quick_charge, weight, anc, bluetooth}`, `part ∈ {earbud, earbuds_pair, case, headphone, headphone_with_case}`, `unit`, `value{kind, role, a, b, closed, v, op}`, `conditions{anc, volume, spatial, charge_minutes, case_type, …}`, `quote`); `evidence_records` (cùng trường + `id`, `chunk_id`, `source_id`, `quote`).
2. Prompt trích xuất **một lần gọi cho mỗi claim**, đầu vào: claim + product_context + top-k đoạn (text, heading_path, footnotes); yêu cầu trả đúng JSON schema; chưa biết → null/`unknown`; không kết luận nhãn.
   ```text
   Hệ thống: Bạn trích dữ kiện có cấu trúc. Không đánh giá đúng/sai. Chỉ ghi điều có trong văn bản.
   Với mỗi giá trị: kind theo dấu hiệu (lên đến/tối đa → exact + role declared_maximum; con số trần
   trong claim → role stated_spec; "chính xác/luôn" → exact + measurement; hơn → gt; ít nhất → ge;
   khoảng → approx). Điều kiện chỉ ghi khi văn bản hoặc chú thích của đoạn nêu. quote phải chép nguyên văn.
   Trả JSON: {"claim_record": …, "evidence_records": […]}
   ```
3. Viết 3 ví dụ few-shot **từ dev** (không từ EX, không từ test); lưu `templates/extract_prompt.json` + SHA-256.
4. Schema σ của dữ kiện nguồn có thêm `quotes` (`value` bắt buộc, `conditions.<k>`, `part`); prompt yêu cầu chép nguyên văn, không diễn giải. Thử trên 23 ví dụ sẵn có: mọi chuỗi trích phải qua `grounding_reference.ground`.
- **Mẫu:** output đúng — xem tra cứu §11.4. Output sai thường gặp: (a) gán `role=declared_maximum` cho claim “chính xác 20 giờ”; (b) thêm `conditions.anc="on"` vào claim không nêu; (c) `quote` không có trong đoạn; (d) thêm trường `label`.

**Nếu vướng:** mô hình hay bịa điều kiện → thêm luật kiểm `quote` ở B23 thay vì dặn thêm trong prompt mãi.

**Checklist bàn giao:**

- [ ] Schema + prompt có hash
- [ ] Jsonschema hợp lệ
- [ ] Prompt không chứa từ nhãn (Supported/Refuted/NEI)
- [ ] Đạt điều kiện xong: schema validate trên 23 ví dụ
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B23 · Trích xuất, neo nguồn, chuẩn hóa (M5, M6)

**Cần xong trước:** B21, B22 · **Thời lượng:** 9–13 giờ

**Mục đích:** biến phản hồi thành hồ sơ hợp lệ hoặc lỗi kỹ thuật có ghi chép.

**Cần có trong tay:** prompt; retrieval; `configs/models.yaml`.

**Làm:**

1. M6 `llm_client.call(messages, model_cfg)` → lưu request/response thô, token, độ trễ; cache theo `sha256(messages + model_cfg)` **chỉ trong cùng `extraction_run_id`**.
2. Parse: lấy khối JSON đầu tiên; lỗi → retry tối đa 2 lần với thông báo lỗi schema; vẫn lỗi → `status=ERROR`.
3. Validate (M5 `validate_records`): schema; enum; số đọc được (`Decimal`, đổi “,”→“.”); khoảng không đảo biên; mọi `evidence_record.chunk_id` thuộc top-k của claim; `quote` là chuỗi con của text hoặc footnotes của đoạn đó (so sau chuẩn hóa khoảng trắng); `conditions` của bằng chứng chỉ chứa giá trị xuất hiện trong text/footnote (kiểm từ khóa: “bật/tắt”, “50%”…). Vi phạm → bỏ bản ghi đó và ghi `dropped_records` + lý do (không bịa thay).
4. Chuẩn hóa: đơn vị (`giờ`→`h`, `phút`→`min`, `gram|g`→`g`), Bluetooth `"Bluetooth 5.3"`→`"5.3"`; `market` của claim = null nếu claim không nêu.
5. Ghi `runs/<run_id>/records/<claim_id>.json` + `normalized_records_sha256` (hash của toàn bộ thư mục records theo thứ tự claim_id).
6. Sau khi parse, gọi `grounding_reference.ground_all(records, chunks)`; lưu `kept` làm hồ sơ chung cho B1, B2, SAV và `dropped` (kèm lý do) vào `records_dropped.jsonl`. Báo tỷ lệ loại theo lý do trên dev; nếu > 20% thì sửa prompt trước khi khóa (không nới kiểm neo).
- **Mẫu:**
```python
def extract(claim, chunks, cfg, run_id):
    for attempt in range(3):
        resp = llm_client.call(render(claim, chunks), cfg)
        try:
            rec = parse_json(resp.text)
            rec, dropped = validate_records(rec, chunks)   # RecordError nếu hỏng toàn bộ
            return {'status': 'ok', 'records': normalize(rec), 'dropped': dropped}
        except (JSONError, RecordError) as e:
            last = str(e)
    return {'status': 'ERROR', 'error': last}
```

**Nếu vướng:** tỷ lệ ERROR > 5% trên dev → sửa prompt/schema trước khi đi tiếp; không hạ chuẩn validate.

**Checklist bàn giao:**

- [ ] `kltn/extract_records.py` (M5), `kltn/llm_client.py` (M6)
- [ ] Records
- [ ] Test với phản hồi giả (mock): JSON hỏng → retry rồi ERROR
- [ ] `quote` bịa → bản ghi bị bỏ
- [ ] Chunk ngoài top-k → bỏ
- [ ] Số “1,5” → `"1.5"`
- [ ] Đạt điều kiện xong: JSON hợp lệ ≥ 95%; tỷ lệ loại do neo được ghi
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B24 · Đánh giá trích xuất trên dev

**Cần xong trước:** B18, B23 · **Thời lượng:** 2–3 giờ

**Mục đích:** biết hồ sơ sai ở trường nào trước khi so B1/P (nếu hồ sơ hỏng, cả B1 và P đều hỏng).

**Cần có trong tay:** records dev; gold records dev.

**Làm:**

1. So từng trường: `part`, `attribute`, `value.kind`, `value.role`, `value.a`, `conditions`; tính độ chính xác theo trường; liệt kê 10 lỗi đại diện.
- **Mẫu:** `role` đúng 26/30, `conditions` đúng 24/30 (lỗi chủ yếu: bỏ sót “khi tắt chống ồn”).

**Nếu vướng:** một trường < 80% đúng → sửa prompt/few-shot trên dev, đo lại; ghi số vòng sửa.

**Checklist bàn giao:**

- [ ] `results/tables/dev_extraction_fields.csv` (không phải kết quả chính; dùng trong Chương 3 mục thiết kế)
- [ ] Có bảng và 10 ví dụ lỗi
- [ ] Đạt điều kiện xong: ≥ 80% trường đúng hoặc ghi lỗi
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B25 · Nối SAV (P) với hồ sơ (M7)

**Cần xong trước:** B23 · **Thời lượng:** 3–4 giờ

**Mục đích:** P chạy trên hồ sơ trích xuất thật.

**Cần có trong tay:** records; `scripts/abc_reference.py`.

**Làm:**

1. Phần kế thừa từ mã tham chiếu: toàn bộ A–B–C1–C2–C3, chính sách chung, ablation, kiểm hồ sơ → `RecordError`. Phần cần thêm: chuyển định dạng records (M5) sang hợp đồng `verdict` (đổi tên trường nếu khác), gọi `safe_verdict`, ghi `evidence_ids` = id các bản ghi đã dùng ở thuộc tính quyết định, ghi `reason` từ vết. Phần chưa có: luật xác nhận bao phủ cho claim phổ quát (giới hạn đã ghi).
2. `kltn/decide_p.py`: `decide(records, ablate=()) -> prediction`; chuyển `abc_reference.py` vào `kltn/abc.py` (giữ `scripts/abc_reference.py` làm wrapper import lại để test cũ chạy).
3. Ghi prediction theo tra cứu §9.2; `ERROR` khi hồ sơ hỏng hoặc extraction `status=ERROR`.
4. Thêm ablation **P−ground**: SAV nhận hồ sơ *trước* khi neo (cùng lượt trích xuất), để đo đóng góp của thành phần 1.
- **Mẫu:** `{"claim_id":"c_…","method":"P","label":"NEI","nei_type":"missing","evidence_ids":[],"reason":"không còn bằng chứng sau A/B (điều kiện anc=off không có)","status":"ok"}`.

**Nếu vướng:** “chưa lỗi Python” không có nghĩa phán quyết hợp lệ: mọi dự đoán `ok` phải có vết cho từng thuộc tính; thiếu vết → coi là lỗi phần mềm.

**Checklist bàn giao:**

- [ ] M7
- [ ] Test: 23 hồ sơ fixture qua `decide` cho đúng nhãn như `tests/test_abc.py`
- [ ] Hồ sơ hỏng → `ERROR` (không bao giờ là NEI)
- [ ] Ablation sinh 4 dự đoán khác method
- [ ] Đạt điều kiện xong: `tests/test_abc.py` PASS
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B26 · Cài B0, B1, B2 (M8)

**Cần xong trước:** B23 · **Thời lượng:** 5–7 giờ

**Mục đích:** đối chứng công bằng: cùng claim, cùng mô hình, cùng hướng dẫn, cùng cấu hình.

**Cần có trong tay:** `templates/eval_prompts.json` (đã chứa nguyên văn hướng dẫn v2 + SHA-256; cấu trúc ở tra cứu Phụ lục C).

**Làm:**

1. B0 payload (`--kind b0`): `claim_id, claim_text, product_context, evidence_texts` (top-k đoạn: `chunk_id, source_id, heading_path, text, footnotes, locale`).
2. B1 payload (`--kind b1`): `claim_id, claim_text, product_context, extraction_run_id, normalized_records_sha256, normalized_records` — **đúng** records mà P dùng trong cùng lượt (cùng hash).
3. Render prompt bằng thay `{{INPUT_JSON}}`; lưu thông điệp đầy đủ + SHA-256; không cắt hướng dẫn.
4. Gọi D với temperature 0, cùng `max_tokens`; parse `label, nei_type, evidence_ids, reason`; retry tối đa 2 lần nếu JSON hỏng; vẫn hỏng → `ERROR`. `evidence_ids` không có trong đầu vào → giữ nhãn, ghi `invalid_evidence_ids` (báo riêng).
5. Thêm **B2**: prompt B1 + danh sách kiểm phạm vi (sản phẩm → bộ phận → điều kiện → vai trò con số → giá trị) + 3 ví dụ lấy từ dev (không từ test). Chạy B0/B1/B2 với hai mô hình quyết định D1 (mở) và D2 (thương mại nhỏ) ghi trong `configs/models.yaml`; cùng tham số giải mã.
- **Mẫu:** payload mẫu hợp lệ trong `tests/test_leak.py` (`B0_OK`, `B1_OK`).

**Nếu vướng:** mô hình trả “Not enough info” thay “NEI” → bảng ánh xạ cố định nhỏ (ghi trong code), không đoán rộng.

**Checklist bàn giao:**

- [ ] `kltn/baselines.py` (M8)
- [ ] Test: prompt B0 và B1 có cùng system prompt (so chuỗi), cùng SHA-256 hướng dẫn
- [ ] Payload qua `check_input_leak --kind`
- [ ] Parse đúng 6 phản hồi mẫu (hợp lệ, thiếu trường, nhãn lạ, JSON trong markdown, rỗng, dài quá)
- [ ] Đạt điều kiện xong: parse 100% trên dev hoặc ERROR
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B27 · Kiểm công bằng, rò nhãn (M9)

**Cần xong trước:** B25, B26 · **Thời lượng:** 1–2 giờ

**Mục đích:** chặn đáp án và dấu vết lọt vào payload; bảo đảm B1 và P cùng hồ sơ.

**Cần có trong tay:** payload dev.

**Làm:**

1. Runner gọi `check_input_leak.problems(payload, kind)` trước **mỗi** lệnh gọi; FAIL → dừng claim đó, ghi lỗi
2. Kiểm `records_sha256` của B1 = của P trong cùng `repeat_id`
3. Kiểm mọi phương pháp nhận cùng danh sách `claim_id` theo cùng thứ tự đã xáo trộn bằng seed (không sắp theo nhóm/nhãn)
4. Đọc 10 payload ngẫu nhiên bằng mắt tìm dấu hiệu lộ (ví dụ câu biến thể có từ “sai”).
- **Mẫu:** `python3 scripts/check_input_leak.py --kind b1 runs/dev-*/payloads/b1/*.json`.

**Nếu vướng:** PASS không chứng minh hết đường rò (docstring của script) — vẫn đọc tay.

**Checklist bàn giao:**

- [ ] `kltn/payload.py` (M9)
- [ ] Log kiểm trong manifest
- [ ] 100% payload PASS
- [ ] Hash B1=P
- [ ] Đạt điều kiện xong: `check_input_leak` PASS
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B28 · Runner, manifest, cache (M10)

**Cần xong trước:** B27 · **Thời lượng:** 5–8 giờ · **Ghi chú:** chuyển lên trước pilot (bản cũ đặt sau)

**Mục đích:** chạy ma trận thí nghiệm tái lập được, không thiếu/trùng mẫu.

**Cần có trong tay:** `configs/runs/<tn>.yaml`; protocol_lock.

**Làm:**

1. Cấu hình một lượt chạy: `split, methods [B0,B1,P,P−part,P−cond,P−role,P−inherit], repeat_id, sample_list (all | repeat_subset), records_source (extracted | gold)`.
2. Kiểm trước chạy: `lock verify`; danh sách claim = danh sách đã khóa; số đoạn top-k có sẵn; ngân sách còn lại ≥ ước tính CT11.
3. Thứ tự trong một lượt: retrieval → extraction (một lần/claim, `extraction_run_id` mới cho mỗi lượt) → P và ablation (không gọi LLM) → B1 (cùng records) → B0.
4. Ghi tăng dần `predictions.jsonl`; chạy lại bỏ qua claim × method đã có `status=ok`; ERROR được retry theo chính sách (tối đa 2 lần, cách 30 giây), vẫn lỗi → giữ ERROR.
5. Cuối lượt: kiểm thiếu/trùng (mỗi claim × method đúng 1 dòng); ghi `manifest.json` theo template (token, chi phí, thời gian, lỗi).
- **Mẫu:** `python -m kltn.runner configs/runs/tn2_test_r1.yaml`.

**Nếu vướng:** nhà cung cấp đổi mô hình giữa lượt → dừng, ghi, chạy lại cả lượt cho mọi phương pháp.

**Checklist bàn giao:**

- [ ] `kltn/runner.py` (M10)
- [ ] `runs/<run_id>/` (D14)
- [ ] Test: chạy giả (mock LLM) trên 5 claim, ngắt giữa chừng, chạy lại → không trùng dòng
- [ ] Manifest đủ trường
- [ ] Đạt điều kiện xong: chạy lại được sau lỗi
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B29 · Chạy pilot trên dev

**Cần xong trước:** B28 · **Thời lượng:** 3–5 giờ

**Mục đích:** kiểm các giả định khả thi trước khi thu đủ dữ liệu: số claim/quảng cáo, công sức, lỗi JSON, recall@k, chi phí, hành vi B0/B1/B2/P.

**Cần có trong tay:** dev lô 0 + biến thể của nó (mục tiêu ≈ 40 claim thông thường + ≈ 20 biến thể); D12 thời gian.

**Làm:**

1. Đo công sức thật từ D12: t_nguồn/họ, t_tách/quảng cáo, t_claim, t_var, t_log; số claim hợp lệ/quảng cáo (c̄).
2. Chạy TN1–TN3 bản thử trên dev (chỉ dev): recall@k, B0/B1/B2/P, ablation; ghi tỷ lệ ERROR, token, độ trễ, chi phí.
3. Đọc 20 ca P và B1 bất đồng; gắn mã lỗi (B41) để biết lỗi chủ yếu ở đâu.
4. Ghi `notes/pilot_report.md`: bảng số đo, so với giả định ở tra cứu §3.3, vấn đề và sửa đổi.
- **Mẫu:** c̄ = 4,2 → muốn 70 claim thông thường test cần ⌈70 / 4,2⌉ = 17 quảng cáo test; t_claim = 8,5 phút → 150 claim thông thường ≈ 21 h.

**Nếu vướng:** ERROR > 5% → sửa B22; recall@8 < 0,8 → sửa B10/B20; một nhãn hầu như không xuất hiện ở tập thông thường → bình thường, tập chẩn đoán bù cho phép đo cơ chế; không chỉnh prompt sinh để “tạo lỗi”.

**Checklist bàn giao:**

- [ ] `notes/pilot_report.md`
- [ ] `runs/pilot-*`
- [ ] Mọi số trong báo cáo truy về file (D12, manifest)
- [ ] Đạt điều kiện xong: đủ output cho mọi claim dev
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B30 · Chốt quy mô, cấu hình, mức kết luận

**Cần xong trước:** B29 · **Thời lượng:** 2–3 giờ

**Mục đích:** biến số đo pilot thành quyết định có ghi chép.

**Cần có trong tay:** pilot report; `scripts/simulate_power.py`.

**Làm:**

1. Cập nhật bảng 5.4 bằng số đo.
2. Chạy `python3 scripts/simulate_power.py --families 4 5 6 --per-family <số R+NEI dự kiến mỗi họ test> --far-b1 <FAR_B1 pilot> --far-p <FAR_P pilot>` — chỉ để hình dung độ rộng khoảng; ghi rõ đây là mô phỏng với FAR pilot (dev), không phải kết quả.
3. Chọn quy mô trong khung ở tra cứu §3.4: nếu tổng giờ dự báo vượt ngân sách thời gian → giảm claim thông thường test (không dưới sàn), giữ tập chẩn đoán.
4. Chốt cấu hình dev: mô hình, k, prompt trích xuất, từ điển mở rộng — **không** đổi nữa sau B38.
5. Ghi QĐ5 (quy mô) và QĐ6 (mô hình) với ngày vào `notes/decisions.md`; báo GVHD.
- **Mẫu:** “Quy mô chốt: test 5 họ, 70 thông thường + 65 biến thể; dev 4 họ; val 2 họ. Lý do: t_claim 8,5 phút, ngân sách 300 h.” (minh họa)

**Nếu vướng:** dự báo không đạt sàn ngay cả khi cắt → kích hoạt dự phòng 2.6.

**Checklist bàn giao:**

- [ ] `notes/decisions.md` cập nhật QĐ5, QĐ6
- [ ] Bảng quy mô ở tra cứu §3.4 cập nhật số chốt
- [ ] Có quyết định ghi ngày và lý do số liệu
- [ ] Đạt điều kiện xong: GVHD xác nhận hoặc ghi ngày hỏi
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### Checklist bàn giao giai đoạn 5

- [ ] B20 · BM25 lọc theo sản phẩm (M4) — `kltn/bm25.py`
- [ ] B21 · Đo recall@k trên dev, chọn k — bảng recall dev; k đề xuất
- [ ] B22 · Schema σ có trường trích dẫn, prompt trích xuất — schema + prompt v1
- [ ] B23 · Trích xuất, neo nguồn, chuẩn hóa (M5, M6) — `records.jsonl` dev + danh sách loại do neo
- [ ] B24 · Đánh giá trích xuất trên dev — bảng độ đúng từng trường
- [ ] B25 · Nối SAV (P) với hồ sơ (M7) — `kltn/decide_p.py`
- [ ] B26 · Cài B0, B1, B2 (M8) — `kltn/baselines.py`
- [ ] B27 · Kiểm công bằng, rò nhãn (M9) — báo cáo kiểm rò
- [ ] B28 · Runner, manifest, cache (M10) — `kltn/runner.py`
- [ ] B29 · Chạy pilot trên dev — `runs/pilot-*`; báo cáo pilot
- [ ] B30 · Chốt quy mô, cấu hình, mức kết luận — QĐ5 chốt; tra cứu §3.4 cập nhật
- [ ] **Mốc:** M2 — Pilot xong: báo cáo pilot, quy mô chốt (QĐ5), JSON hợp lệ ≥ 95% trên dev
- [ ] Gửi GVHD tóm tắt 5 dòng: đã xong gì, số liệu chính, vướng gì, việc tiếp theo

---

## Giai đoạn 6 — Dữ liệu đủ quy mô (24/11–07/12)

### B31 · Thu nguồn, chia đoạn các họ còn lại

**Cần xong trước:** B30 · **Thời lượng:** 8–16 giờ · **Ghi chú:** lặp quy trình B09–B12

**Mục đích:** mở rộng kho nguồn từ 2 họ pilot lên đủ số họ chốt ở B30.

**Làm:**

1. Với từng họ còn lại trong D1, lặp đúng quy trình B09 (thu nguồn, snapshot), B10 (trích văn bản bằng M1), B11 (chia đoạn bằng M2), B12 (kiểm độ phủ). Không sửa M1/M2 trừ khi gặp định dạng mới; nếu sửa, chạy lại trên 2 họ pilot và so mã đoạn.

**Nếu vướng:** hãng thứ hai không có trang thông số văn bản → ghi vào D1, áp dụng tra cứu §14.4.

**Checklist bàn giao:**

- [ ] D2–D4 cho mọi họ
- [ ] Độ phủ 100% thuộc tính đã chọn cho mọi họ
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B32 · Sinh quảng cáo, tách claim, biến thể còn lại

**Cần xong trước:** B30, B31 · **Thời lượng:** 4–8 giờ · **Ghi chú:** lặp B14–B17

**Mục đích:** đủ claim thông thường và biến thể chẩn đoán theo quy mô B30.

**Làm:**

1. Lặp B14 (sinh quảng cáo bằng prompt đã khóa ở B13), B15 (tách claim, bấm giờ), B16 (biến thể cặp tối thiểu, ≥ 12 mỗi loại thao tác ở test), B17 (kiểm trùng). Không đổi prompt sinh; nếu buộc phải đổi, ghi phiên bản mới và lý do.

**Checklist bàn giao:**

- [ ] D5, D6 đủ
- [ ] Đạt sàn ở tra cứu §3.4
- [ ] Đạt điều kiện xong: đạt sàn tra cứu §3.4
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B33 · Gán nhãn, nhật ký NEI phần còn lại

**Cần xong trước:** B32 · **Thời lượng:** 10–22 giờ · **Ghi chú:** lặp B18–B19

**Mục đích:** nhãn vàng cho toàn bộ claim mới.

**Làm:**

1. Lặp B18 (gán nhãn tham chiếu và bộ bằng chứng chuẩn theo tra cứu §5) và B19 (nhật ký tìm nguồn cho mọi NEI-missing). Gán theo họ, không xem dự đoán của hệ thống.

**Checklist bàn giao:**

- [ ] D7, D8 đủ
- [ ] Tập sẽ làm test không còn `pending_review`
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B34 · Kiểm độ tin cậy nhãn

**Cần xong trước:** B33 · **Thời lượng:** 3–5 giờ

**Mục đích:** đo nhãn có lặp lại được không; báo trung thực mức kiểm.

**Cần có trong tay:** D6, D7; mẫu `templates/independent_annotation.csv` (cột ở tra cứu Phụ lục C).

**Làm:**

- **Các bước (phương án A — có người thứ hai):**
1. Người thứ hai: một bạn cùng khóa/học viên đọc được tiếng Việt và tiếng Anh kỹ thuật; sinh viên tự mời, ghi tên/vai trò sau khi họ đồng ý (không bịa).
2. Chọn 40 claim bằng seed ghi lại (`random.Random(20261115)`), phân tầng theo nhãn sơ bộ (≈ 13 mỗi nhãn), hai nhóm và ≥ 4 họ, trong đó ≥ 15 claim test. Chọn **trước** khi chạy hệ thống.
3. Gói `data/annotation2/package/`: hướng dẫn v2, corpus (chunks + page.txt của các họ liên quan), CSV chỉ có `sample_id` mờ, `claim_text`, `product`. Không có nhãn, lý do, nhóm, thao tác, dự đoán.
4. Luyện: 5 claim dev ngoài mẫu, giải thích sau khi họ gán xong.
5. Người thứ hai gán vào `data/annotation2/results.csv` theo mẫu.
6. Tính **trước hòa giải**: tỷ lệ đồng thuận, Cohen’s κ ba nhãn (CT9), bảng 3×3 (B11); NEI-missing/conflict gộp thành NEI khi tính κ, báo riêng bảng phụ.
7. Hòa giải bằng nguồn: hai người đọc lại nguồn; lưu nhãn ban đầu cả hai, lý do bất đồng, nhãn cuối; không dùng P.
- **Phương án B — chưa có người thứ hai:** tự gán lại 20% claim (seed ghi lại) sau ≥ 7 ngày, ẩn nhãn cũ; báo là **tự nhất quán**, ghi giới hạn trong luận văn. Không dùng AI thay người thứ hai.
- **Mẫu:** tính κ giả lập ở tra cứu §8.3 (CT9).

**Nếu vướng:** κ thấp (< 0,6) → xem bảng bất đồng: nếu tập trung ở một quy tắc → sửa hướng dẫn (tra cứu §10.4), gán lại toàn bộ claim bị ảnh hưởng; không chỉ sửa 40 ca mẫu.

**Checklist bàn giao:**

- [ ] `data/annotation2/` (D10)
- [ ] B11
- [ ] Bản ghi `revision_of` cho nhãn sửa sau hòa giải
- [ ] Có log người thứ hai (ngày, file) hoặc đã ghi rõ dùng phương án B
- [ ] Κ tính bằng M11 và bằng tay khớp
- [ ] Đạt điều kiện xong: κ báo trước hòa giải
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### Checklist bàn giao giai đoạn 6

- [ ] B31 · Thu nguồn, chia đoạn các họ còn lại — D1–D4 cho mọi họ
- [ ] B32 · Sinh quảng cáo, tách claim, biến thể còn lại — D5, D6 đủ quy mô B30
- [ ] B33 · Gán nhãn, nhật ký NEI phần còn lại — D7, D8 đủ
- [ ] B34 · Kiểm độ tin cậy nhãn — D10; Cohen’s κ
- [ ] **Mốc:** M3 — Dữ liệu đủ: đạt sàn test ở tra cứu §3.4; κ đã báo
- [ ] Gửi GVHD tóm tắt 5 dòng: đã xong gì, số liệu chính, vướng gì, việc tiếp theo

---

## Giai đoạn 7 — Chia tập và khóa (08/12–11/12)

### B35 · Chia tập theo họ

**Cần xong trước:** B33 · **Thời lượng:** 1 giờ

**Mục đích:** không rò giữa các tập: mọi claim của một họ (gồm cha, biến thể, gần trùng) ở cùng một tập.

**Cần có trong tay:** D1, D6 (đếm).

**Làm:**

1. Họ pilot (2 họ của lô 0) **luôn ở dev**.
2. Với các họ còn lại: xếp theo hãng; dùng seed ghi lại để chọn: test 5 họ (≥ 1 họ hãng thứ hai nếu có), val 2, dev còn lại. Không chọn họ để cân nhãn sau khi đã nhìn nhãn; chỉ được dùng tiêu chí đã ghi trước (số thuộc tính có nguồn, hãng).
3. Ghi `data/splits.json` (D11) gồm `rule` và `seed`.
- **Mẫu:** `{"dev":["apple-airpods-max-2","apple-airpods-5",…],"val":[…],"test":[…],"seed":20261101}`.

**Nếu vướng:** hai họ cùng dùng chung một tài liệu (ví dụ trang so sánh) → ghép thành một nhóm chia tập.

**Checklist bàn giao:**

- [ ] D11
- [ ] M13: mỗi họ đúng một tập
- [ ] Mọi claim có họ trong D11
- [ ] Mọi `parent_claim_id` cùng tập với con
- [ ] Đạt điều kiện xong: không họ nào ở hai tập
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B36 · Hồ sơ chuẩn cho TN4

**Cần xong trước:** B35 · **Thời lượng:** 6–8 giờ

**Mục đích:** tách lỗi trích xuất khỏi lỗi quyết định: B1 và P chạy trên hồ sơ đúng tuyệt đối.

**Cần có trong tay:** claim chẩn đoán của test + câu cha; bộ bằng chứng chuẩn; schema.

**Làm:**

1. Với mỗi claim, viết `claim_record` đúng schema theo câu chữ (vai trò con số theo tra cứu §5.5)
2. Viết `evidence_records` cho **mọi đoạn trong top-k của BM25 lượt 1** (không chỉ đoạn chuẩn) để B1/P gặp đúng nhiễu như thật — nếu chưa có output BM25 thì viết cho các đoạn của họ cùng thuộc tính
3. Kiểm `quote` là chuỗi con của đoạn
4. Lưu `data/gold_records/<claim_id>.json`.
- **Mẫu:** tra cứu §11.4 (hồ sơ claim AirPods Max 2).

**Nếu vướng:** đoạn có hai thông số → hai bản ghi bằng chứng.

**Checklist bàn giao:**

- [ ] D9
- [ ] M5 `validate_records` PASS trên 100% file
- [ ] Người làm đọc lại 10% sau 2 ngày
- [ ] Đạt điều kiện xong: đủ n_4 claim
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B37 · Kiểm dữ liệu trước thực nghiệm (M13)

**Cần xong trước:** B36 · **Thời lượng:** 2–3 giờ

**Mục đích:** bắt lỗi schema, ID, phân bố trước khi tốn lượt gọi mô hình.

**Cần có trong tay:** D1–D11.

**Làm:**

1. Chạy `python -m kltn.validate_data --all` kiểm: (1) schema từng file (jsonschema); (2) liên kết ID: claim→ad, claim→parent, label→claim, gold chunk→chunks, chunk→source, source→family; (3) trường thiếu; (4) bảng phân bố nhóm × nhãn × tập × họ; (5) số `pending_review` (test phải = 0 hoặc đã quyết định loại có ghi lý do, báo số); (6) mỗi NEI-missing có search log; (7) không file payload mẫu nào rò (gọi `check_input_leak`).
- **Mẫu:** đầu ra mong đợi: `PASS schema (7 files) | PASS links | test: S=34 R=31 NEI=36 pending=0 | variants COND=14 PART=12 ROLE=13 VAL=15 PROD=12`. (Số chỉ minh họa.)

**Nếu vướng:** test dưới sàn → quay B13 sinh thêm lô theo quy tắc dừng (không đổi họ giữa các tập); nếu đã chạm ngân sách → báo thiếu hụt, giảm mức kết luận (tra cứu §14.4).

**Checklist bàn giao:**

- [ ] `results/tables/B3_dataset_stats.csv`
- [ ] Log kiểm trong `runs/precheck-<ngày>.txt`
- [ ] Lệnh thoát mã 0
- [ ] Đạt điều kiện xong: mã thoát 0
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B38 · Khóa giao thức

**Cần xong trước:** B37 · **Thời lượng:** 1–2 giờ

**Mục đích:** cố định mọi thứ ảnh hưởng kết quả trước khi chạy test.

**Cần có trong tay:** hướng dẫn, prompt, cấu hình, splits, labels, chunks, code.

**Làm:**

1. `python -m kltn.lock create` ghi `data/locks/protocol_lock.json`: SHA-256 của `docs/HUONG_DAN_GAN_NHAN.md` (bản máy đọc của tra cứu §5), eval_prompts, prompt trích xuất, `configs/*.yaml` (mô hình, k, chunker, query), `splits.json`, `labels.jsonl` (lọc test), `chunks.jsonl`, commit hash code, danh sách 30 claim lặp (seed), danh sách mẫu phân tích lỗi (seed), quy tắc xử lý lỗi/retry, ngân sách.
2. Commit `B38: khóa giao thức v1`.
3. Chạy **val một lần** bằng cấu hình đã khóa (B39 bước 1); nếu val lộ lỗi phần mềm (không phải điểm thấp) → sửa, ghi `protocol_lock` v1.1 + lý do, không chỉnh để tăng điểm.
- **Mẫu:** `{"version":"1.0","created_at":"…","files":{"docs/HUONG_DAN_GAN_NHAN.md":"…sha…"},"repeat_subset":["c_…"],"error_policy":"…"}`.

**Nếu vướng:** cần sửa sau khóa → tra cứu §10.4 bước 4.

**Checklist bàn giao:**

- [ ] D13
- [ ] `python -m kltn.lock verify` trả PASS
- [ ] Runner từ chối chạy test nếu hash lệch
- [ ] Đạt điều kiện xong: lock đã commit
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### Checklist bàn giao giai đoạn 7

- [ ] B35 · Chia tập theo họ — D9 split
- [ ] B36 · Hồ sơ chuẩn cho TN4 — D9b hồ sơ chuẩn
- [ ] B37 · Kiểm dữ liệu trước thực nghiệm (M13) — báo cáo M13
- [ ] B38 · Khóa giao thức — `protocol_lock.json`; val chạy 1 lần
- [ ] **Mốc:** M4 — Khóa: `protocol_lock.json` đã commit; val chạy đúng một lần
- [ ] Gửi GVHD tóm tắt 5 dòng: đã xong gì, số liệu chính, vướng gì, việc tiếp theo

---

## Giai đoạn 8 — Thực nghiệm và phân tích (12/12–17/12)

### B39 · Chạy TN1–TN4

**Cần xong trước:** B38 · **Thời lượng:** 6–10 giờ

**Cần có trong tay:** ma trận ở tra cứu §8.1.

**Làm:**

1. Val một lượt (B0/B1/B2/P) bằng cấu hình khóa → chỉ kiểm lỗi phần mềm/pipeline; ghi kết quả val riêng, không chỉnh theo điểm.
2. Test lượt 1 (TN1 + TN2 + TN3) toàn bộ test.
3. TN4: P và B1 trên `records_source=gold` cho tập chẩn đoán test + câu cha.
4. Lượt 2 và 3 trên `repeat_subset` (30 claim chọn bằng seed lúc khóa, phân tầng nhãn/nhóm/họ), mỗi lượt có trích xuất mới.
6. Sau mỗi bước: kiểm thiếu/trùng; ghi lab notebook.
6. TN2 gồm B0, B1, B2, SAV × {D1, D2}; TN3 gồm thêm P−ground; so sánh chính là SAV vs B2.
- **Mẫu:** xem bảng ma trận ở tra cứu §8.1.

**Nếu vướng:** chi phí vượt dự toán → dừng sau lượt 1 (kết quả chính đã đủ), giảm lượt lặp và ghi trước khi chạy tiếp.

**Checklist bàn giao:**

- [ ] `runs/tn*/`
- [ ] Mọi ô của ma trận có output đủ số dòng
- [ ] ERROR được đếm, không xóa
- [ ] Đạt điều kiện xong: không thiếu/trùng mẫu
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B40 · Tính chỉ số, bảng, hình (M11, M12)

**Cần xong trước:** B39 · **Thời lượng:** 4–6 giờ

**Mục đích:** biến output thành bảng/hình có tử số, mẫu số và nguồn file.

**Cần có trong tay:** predictions, labels, splits, claims (nhóm, `mutation_type`).

**Làm:**

1. M11 tính CT1–CT10 theo tập con: toàn test, thông thường, chẩn đoán, từng `mutation_type`, từng họ
2. Bootstrap theo họ (CT8) với B = 10 000, seed ghi lại; leave-one-family-out
3. M12 xuất CSV vào `results/tables/B*.csv` và hình `results/figures/H*.pdf` + `.png`
4. Mỗi file kèm dòng chú thích nguồn (`run_id`, `labels_sha256`).
- **Mẫu:** tra cứu §8.3 (ví dụ tính FAR giả lập), tra cứu §13.1–13.2.

**Nếu vướng:** muốn thêm phân tích chưa định trước → được, nhưng đặt tên “phân tích bổ sung sau khi xem kết quả” và tách khỏi bảng chính.

**Checklist bàn giao:**

- [ ] `kltn/metrics.py` (M11), `kltn/report.py` (M12)
- [ ] B4–B10, H4–H7, H9
- [ ] `tests/test_metrics.py`: ví dụ giả lập tra cứu §8.3 cho đúng số
- [ ] Mẫu số 0 → `NA`
- [ ] Tính tay 1 bảng con khớp
- [ ] Đạt điều kiện xong: tái tạo byte-khớp
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B41 · Mã lỗi, gán lỗi theo chuỗi

**Cần xong trước:** B40 · **Thời lượng:** 6–8 giờ

**Mục đích:** quy mỗi dự đoán sai về bước gây ra; một mẫu có thể có nhiều mã.

**Cần có trong tay:** predictions, retrieval, records, gold records (nếu có), labels, nguồn.

**Làm:**

- **Bảng mã lỗi (chốt trước khi xem kết quả test, ghi trong protocol_lock):**   | Mã | Bước | Định nghĩa | Cách phát hiện |
|---|---|---|---|
| L-SRC | nguồn | thông tin cần có không nằm trong corpus hoặc snapshot thiếu | search log / đọc trang |
| L-CHUNK | chia đoạn | số và điều kiện bị tách/mất chú thích | đoạn chuẩn thiếu footnote |
| L-RANK | truy hồi | bộ chuẩn có trong corpus nhưng ngoài top-k | retrieval.jsonl |
| L-EX-PART / L-EX-COND / L-EX-ROLE / L-EX-VAL / L-EX-PROD | trích xuất | trường tương ứng sai so với hồ sơ chuẩn | so records với gold record/nguồn |
| L-EX-HALL | trích xuất | bản ghi bịa (quote không có) — đã bị bỏ ở validate nhưng làm thiếu thông tin | `dropped_records` |
| L-DEC-SCOPE | quyết định | hồ sơ đúng nhưng bỏ qua phạm vi (B1/B0) hoặc luật A/B sai (P) | hồ sơ đúng + nhãn sai |
| L-DEC-VALUE | quyết định | so giá trị/vai trò sai | như trên |
| L-DEC-AGG | quyết định | tổng hợp nhiều thuộc tính/xung đột sai | như trên |
| L-RULE-GAP | quyết định (P) | ca chưa có luật (ví dụ claim phổ quát cần bao phủ) | vết P |
| L-TECH | kỹ thuật | ERROR, JSON hỏng, timeout | status |
| L-GOLD? | nhãn | nghi nhãn chuẩn sai | đọc lại nguồn — **không sửa nhãn test**; ghi ca, xử lý theo 3.6 |
1. Chọn mẫu theo danh sách khóa trước (seed): mọi ca P sai + mọi ca B1 sai trên tập chẩn đoán test, và 40 ca ngẫu nhiên tập thông thường
2. Với mỗi ca mở `retrieval → records → prediction → nguồn`, gán mã vào `results/error_analysis.csv` (`claim_id, method, codes, note, evidence_file`)
3. Đếm theo mã × phương pháp × nhóm → B12.
- **Mẫu:** `c_…, B1, L-DEC-SCOPE, "hồ sơ ghi anc=off ở claim, bằng chứng anc=on; B1 vẫn Supported", runs/tn2_r1/records/c_….json`.

**Nếu vướng:** phân tích bổ sung sau khi xem kết quả → cột `post_hoc=true`.

**Checklist bàn giao:**

- [ ] `results/error_analysis.csv`
- [ ] B12
- [ ] Mọi ca trong danh sách có ≥ 1 mã
- [ ] 10% ca được gán lại sau 3 ngày khớp mã chính
- [ ] Đạt điều kiện xong: mỗi mẫu có mã lỗi
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B42 · Case study và nhận xét

**Cần xong trước:** B41 · **Thời lượng:** 2–3 giờ

**Mục đích:** minh họa có đại diện, không chỉ kể ca P thắng.

**Cần có trong tay:** error_analysis, B5–B8.

**Làm:**

1. Chọn 4 loại ca, mỗi loại 1–2: **cải thiện** (B1 sai, P đúng), **thất bại** (P sai — ưu tiên L-EX hoặc L-RULE-GAP), **đánh đổi** (P trả NEI cho claim Supported mà B1 đúng), **chưa kết luận** (cả hai đúng/sai vì lý do khác). Với mỗi ca: claim, đoạn nguồn (trích), hồ sơ, vết P, đầu ra B1, mã lỗi, ý nghĩa.
- **Mẫu:** - Giả thuyết được hỗ trợ: “Trên 14 biến thể COND của tập test, P chấp nhận nhầm 1/14, B1 4/14 (lượt 1); xu hướng giữ ở hai lượt lặp; P−cond tăng lên 5/14. Kết quả cho thấy kiểm điều kiện đóng góp vào khác biệt trên mẫu này.” (số minh họa)
- Không được hỗ trợ: “FAR của P và B1 trên tập thông thường lần lượt a/n và b/n; chênh lệch không nhất quán giữa các lượt; không đủ cơ sở cho rằng P giảm chấp nhận nhầm với quảng cáo thông thường.”
- Thiếu chứng cứ: “Chỉ 6 ca ROLE trong test; chỉ mô tả.”

**Checklist bàn giao:**

- [ ] Tra cứu §3.5.x luận văn
- [ ] `results/case_studies.md`
- [ ] Mỗi nhận xét có số (tử/mẫu) và ít nhất một `claim_id`
- [ ] Đạt điều kiện xong: mỗi case truy về file
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### Checklist bàn giao giai đoạn 8

- [ ] B39 · Chạy TN1–TN4 — `runs/test-*` đủ
- [ ] B40 · Tính chỉ số, bảng, hình (M11, M12) — B3–B11, H4–H9
- [ ] B41 · Mã lỗi, gán lỗi theo chuỗi — B12
- [ ] B42 · Case study và nhận xét — 3–5 case study
- [ ] **Mốc:** M5 — Kết quả: bảng B3–B12 tái tạo byte-khớp từ `runs/`
- [ ] Gửi GVHD tóm tắt 5 dòng: đã xong gì, số liệu chính, vướng gì, việc tiếp theo

---

## Giai đoạn 9 — Viết luận văn (18/12–27/12)

### B43 · Chương 1 — Mở đầu

**Cần xong trước:** B02 · **Thời lượng:** 6–8 giờ · **Ghi chú:** viết nháp xen kẽ từ sau B05

**Cần có trong tay:** B05. Viết nháp sớm, sửa lại sau B28.

**Làm:**

- **Trả lời:** bài toán gì, cho ai, vì sao đáng làm, phạm vi và đóng góp.
- **Ý cần viết:** người dùng và cách dùng (tra cứu §1.1); lỗi lệch phạm vi với ví dụ AirPods Max 2 (tra cứu §1.2); giới hạn “tài liệu hãng, không hiệu năng thực”; RQ1–RQ3; đóng góp C\* và hỗ trợ; cấu trúc luận văn.
- **Căn cứ:** tra cứu §1 và 3; H8 (ảnh nguồn); H1 (pipeline).

**Checklist bàn giao:**

- [ ] Mọi tuyên bố đóng góp có TN tương ứng trong bảng truy vết (tra cứu §3)
- [ ] Không dùng “đầu tiên”
- [ ] Đạt điều kiện xong: GVHD đọc
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B44 · Chương 2 — Cơ sở, công trình liên quan

**Cần xong trước:** B04 · **Thời lượng:** 10–14 giờ · **Ghi chú:** viết nháp xen kẽ từ sau B04

**Cần có trong tay:** B04.

**Làm:**

- **Trả lời:** đã có gì; còn khác gì; vì sao chọn thiết kế này.
- **Ý:** kiểm chứng sự thật và ba nhãn [7], [8]; tiếng Việt [9]–[11]; quảng cáo [1]; số liệu và độ bền [3], [12], [13]; xung đột [5]; truy hồi [6]; tách claim [2]; thuộc tính sản phẩm (SynthAVE) chỉ bối cảnh. Bảng B1.
- **Căn cứ:** B03 ghi chép có trang/bảng.

**Checklist bàn giao:**

- [ ] Mọi số có trang
- [ ] Danh mục IEEE khớp trích dẫn (script đếm `[n]`)
- [ ] Đạt điều kiện xong: bảng B1 có trích dẫn
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B45 · Chương 3 — Dữ liệu và phương pháp SAV

**Cần xong trước:** B38 · **Thời lượng:** 12–16 giờ · **Ghi chú:** nháp phần dữ liệu từ sau B30

**Cần có trong tay:** B38 (mọi cấu hình đã khóa).

**Làm:**

- **Trả lời:** dữ liệu tạo ra sao; nhãn định nghĩa ra sao; P/B0/B1 hoạt động ra sao; đánh giá thế nào.
- **Ý:** kho nguồn (B2, H2); giao thức sinh quảng cáo, tách claim, biến thể (B13); hướng dẫn nhãn và chính sách điều kiện (tra cứu §5); kiểm nhãn (B11); chia tập (B3); BM25 (B20); schema + trích xuất (B22); thuật toán P (H3, giả mã ở tra cứu §6.2); B0/B1 công bằng; ma trận TN và chỉ số (tra cứu §8).

**Checklist bàn giao:**

- [ ] Thông số trong chương khớp `protocol_lock.json`
- [ ] Prompt đầy đủ ở phụ lục
- [ ] Đạt điều kiện xong: giả mã + H1–H3
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B46 · Chương 4 — Kết quả và thảo luận

**Cần xong trước:** B42 · **Thời lượng:** 12–16 giờ

**Cần có trong tay:** B40, B41.

**Làm:**

- **Trả lời:** RQ1–RQ3 với số; kết luận nào được phép.

**Checklist bàn giao:**

- [ ] Mỗi số trong văn bản tra được trong `results/tables/*.csv`
- [ ] Mỗi bảng có chú thích mẫu số và “kết luận được phép / không được phép” (tra cứu §8.5)
- [ ] Đạt điều kiện xong: mọi số truy về file
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B47 · Chương 5 — Kết luận, giới hạn

**Cần xong trước:** B46 · **Thời lượng:** 3–4 giờ

**Cần có trong tay:** B46. **Công sức:** 4–6 h.

**Làm:**

- **Ý:** trả lời ngắn từng RQ; giới hạn (product-filtered; claim tách thủ công; một người gán chính; ít họ; tập chẩn đoán do sinh viên tạo; NEI tương đối với corpus; một mô hình quyết định); hướng tiếp (tách tự động, nhiều hãng, kiểm bao phủ claim phổ quát).

**Checklist bàn giao:**

- [ ] Đạt điều kiện xong: không có tuyên bố cấm (tra cứu §2.6)
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B48 · Hình, bảng, công thức xuất bản

**Cần xong trước:** B47 · **Thời lượng:** 4–6 giờ

**Làm:**

1. Dùng M12 cho bảng/hình số liệu (matplotlib, xuất PDF vector + PNG 300 dpi); sơ đồ H1–H3 vẽ bằng draw.io/diagrams.net, lưu file nguồn `thesis/figures/src/*.drawio` và bản xuất PDF; công thức gõ bằng trình soạn công thức của Word hoặc LaTeX, dùng đúng ký hiệu tra cứu §8.3. Bảng mẫu khi chưa có số: để ô trống “chờ đo”; dữ liệu minh họa ghi “giả lập” ở chú thích và không nằm trong `results/`.

**Checklist bàn giao:**

- [ ] Danh mục ở tra cứu §13.1–13.3: mọi B/H/CT có file nguồn, file xuất, mục sử dụng
- [ ] Đạt điều kiện xong: đánh số khớp
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B49 · Tham khảo, thuật ngữ, khai báo AI, định dạng

**Cần xong trước:** B48 · **Thời lượng:** 4–6 giờ

**Làm:**

1. Quản lý tham khảo bằng Zotero hoặc `thesis/references.bib`, kiểu IEEE
2. Bảng thuật ngữ Việt–Anh (từ tra cứu §4.1) ở đầu luận văn
3. Khai báo AI dựa trên `notes/ai_usage.md` (tra cứu §10.2) theo mẫu của Khoa nếu có; tách “AI hỗ trợ soạn thảo/lập trình” với “LLM là đối tượng thí nghiệm”
4. Kiểm định dạng theo mẫu Khoa: lề, cỡ chữ, đánh số chương/bảng/hình, mục lục tự động; xuất PDF và mở kiểm từng trang.

**Checklist bàn giao:**

- [ ] Không trích dẫn thiếu mục
- [ ] Không mục tham khảo không được trích
- [ ] PDF không có bảng tràn lề
- [ ] Đạt điều kiện xong: qua kiểm đạo văn
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### Checklist bàn giao giai đoạn 9

- [ ] B43 · Chương 1 — Mở đầu — Chương 1
- [ ] B44 · Chương 2 — Cơ sở, công trình liên quan — Chương 2
- [ ] B45 · Chương 3 — Dữ liệu và phương pháp SAV — Chương 3
- [ ] B46 · Chương 4 — Kết quả và thảo luận — Chương 4
- [ ] B47 · Chương 5 — Kết luận, giới hạn — Chương 5
- [ ] B48 · Hình, bảng, công thức xuất bản — hình/bảng cuối
- [ ] B49 · Tham khảo, thuật ngữ, khai báo AI, định dạng — bản PDF + Word
- [ ] **Mốc:** M6 — Bản thảo đủ 5 chương, mọi số truy về file
- [ ] Gửi GVHD tóm tắt 5 dòng: đã xong gì, số liệu chính, vướng gì, việc tiếp theo

---

## Giai đoạn 10 — Bàn giao và bảo vệ (28/12–31/12)

### B50 · Gói tái lập, demo dòng lệnh, README

**Cần xong trước:** B40 · **Thời lượng:** 6–10 giờ · **Ghi chú:** gồm demo dòng lệnh (bỏ demo web)

**Làm:**

- **Lựa chọn:** CLI + notebook là đủ cho đóng góp nghiên cứu; giao diện web chỉ là mở rộng. Demo phải chạy trên dữ liệu đã có, không gọi mô hình trực tiếp khi bảo vệ nếu mạng không chắc chắn (dùng output đã lưu, nói rõ).
- **Kịch bản:** (1) nhập claim “AirPods Max 2 mang lại tới 20 giờ nghe nhạc kể cả khi tắt chống ồn” + sản phẩm; (2) hiện top-k đoạn; (3) hiện hồ sơ; (4) P: NEI-missing + vết “điều kiện anc=off không có”; B1: đầu ra đã lưu; (5) ca Refuted (EX-11: 25 giờ), ca Supported (EX-09); (6) một ca P sai (từ B42) và giải thích giới hạn.
- **Lệnh:** `python -m kltn.demo --claim "..." --product "AirPods Max 2" --from-run runs/tn2_test_r1`.
- **Nội dung:** code (gắn tag Git `thesis-v1`), `requirements.lock`, `configs/`, prompt có hash, `protocol_lock.json`, `data/` (claims, labels, splits, chunks, danh mục nguồn; snapshot nếu được phép — QĐ11), `runs/` (manifest, predictions; phản hồi thô nếu không nhạy cảm), `results/`, README “chạy lại”.

**Checklist bàn giao:**

- [ ] Chạy được trên máy sạch trong < 1 phút với output đã lưu
- [ ] Clone vào thư mục mới → `pip install -r requirements.lock` → `python -m kltn.report --from-runs runs/` tái tạo B4–B10 khớp byte với `results/tables/`
- [ ] `python3 -m unittest discover -s tests` PASS. Chạy lại mô hình là tùy chọn (tốn phí, có thể khác do nhà cung cấp)
- [ ] Đạt điều kiện xong: chạy lại trên bản sao mới
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B51 · Slide và chuẩn bị bảo vệ

**Cần xong trước:** B49 · **Thời lượng:** 6–10 giờ

**Làm:**

1. 12–15 slide: vấn đề + ví dụ thật (H8), C\*, thiết kế dữ liệu, P vs B1 (H1, H3), kết quả chính (B6/H5, B7), lỗi và giới hạn, kết luận
2. Chọn kết quả chính theo bảng truy vết, không chọn bảng đẹp nhất
3. Kết quả âm: trình bày bằng TN4/B12
4. Luyện với danh sách câu hỏi ở tra cứu §15, mỗi câu trả lời trỏ tới một bảng/file.

**Checklist bàn giao:**

- [ ] Trình bày thử ≤ thời gian quy định
- [ ] Mọi số trên slide khớp `results/`
- [ ] Đạt điều kiện xong: tập dượt ≥ 2 lần
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### B52 · Kiểm điều kiện hoàn thành

**Cần xong trước:** B50, B51 · **Thời lượng:** 1 giờ

**Làm:**

1. Kiểm điều kiện hoàn thành.

**Checklist bàn giao:**

- [ ] Đạt điều kiện xong: mọi mục đạt
- [ ] Đã ghi `notes/lab_notebook.md` và commit

### Checklist bàn giao giai đoạn 10

- [ ] B50 · Gói tái lập, demo dòng lệnh, README — gói tái lập
- [ ] B51 · Slide và chuẩn bị bảo vệ — slide; câu hỏi có số liệu
- [ ] B52 · Kiểm điều kiện hoàn thành — checklist
- [ ] **Mốc:** M7 — Gói tái lập chạy lại trên bản sao mới; slide đã tập dượt
- [ ] Gửi GVHD tóm tắt 5 dòng: đã xong gì, số liệu chính, vướng gì, việc tiếp theo

---

## Khi xong B52

Toàn bộ checklist đã tick nghĩa là: luận văn, dữ liệu, mã nguồn, kết quả TN1–TN4, gói tái lập và slide đã sẵn sàng nộp và bảo vệ.
