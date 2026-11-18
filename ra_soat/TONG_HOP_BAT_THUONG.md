# Tổng hợp bất thường sau rà soát ngày 18/11/2026

Tệp này gom các điểm bất thường sau khi Gemini 4 Carbon rà soát và mình (Claude Opus) **tự kiểm lại từng mục**. **Kế hoạch chưa được sửa gì.** Bạn đọc, chốt từng điểm, rồi mới sửa kế hoạch.

## Kết luận nhanh

Trong 35 mục Carbon xác nhận, mình tự kiểm lại cả 35. Mình chạy lại mã trên dữ liệu đã có trong cache (không gọi API), đếm lại số liệu, chạy pytest, và đọc văn bản gốc.

| Kết luận | Số mục | Mã |
|---|---|---|
| Lỗi thật, **sửa ngay** (trước Bước 28–30 và Mốc 3) | 17 | T-01, T-03, T-06, T-09, T-10, T-11, T-12, T-18, T-20, T-21, T-22, T-23, T-24 (một phần), T-26, T-29, T-30, T-34 |
| Có thật, nhưng **bạn phải chốt hướng** trước khi sửa | 9 | T-02, T-04, T-05, T-07, T-08, T-15, T-16, T-19, T-31 |
| Lỗi thật, **sửa sau** (trước khi viết bản cuối, demo, nộp) | 6 | T-14, T-17, T-25, T-28, T-32, T-35 |
| Có thật nhưng **không bắt buộc sửa**, chỉ cần khai báo hoặc cân nhắc | 2 | T-13, T-27 |
| Mình **bác** phần chính | 1 | T-33 (phần `b < c`) |

Có 4 chỗ mình kết luận khác Carbon:
- **T-04:** mình bác ý "tiến trình thử lại nền đang làm phình log". Không có tiến trình nào chạy. `llm_calls.jsonl` nặng 273 MB vì mỗi dòng chép nguyên câu lệnh.
- **T-08:** mình hạ từ NGHIÊM TRỌNG xuống CAO. Việc dữ liệu tự nhiên thiếu loại `doi_bo_phan`, `doi_phien_ban` là chuyện bình thường. Kế hoạch đã có Bước 25 (cặp tối thiểu) để bù đúng chỗ này.
- **T-15:** mình nâng tầm quan trọng. Chạy lại cho thấy FAR của P và P−NN đều bằng 0, nên vế FAR của H3 không thể đạt.
- **T-33:** mình bác phần "thiếu điều kiện `b < c`". Cột "Đạt" của H1 đã đòi FAR(P) thấp hơn từng đối chứng.

## Tình trạng sau đợt sửa ngày 18/11 (Nhóm 1)

| Mã | Tình trạng | Ghi chú |
|---|---|---|
| T-01, T-09, T-10, T-20, T-21, T-22 | ✅ Đã sửa | P trên 108 tuyên bố: Recall Đúng 23/64 → 59/64, FAR 0/44, Macro-F1 0,42 → 0,80 (đo offline, `scripts/do_p_phat_trien.py`) |
| T-06 | ✅ Đã sửa | P và B1 trả `LOI` khi lỗi kỹ thuật LLM |
| T-03 | ✅ Đã sửa | Script và kế hoạch trỏ `thu_luot2.jsonl`; `data/nhan/thu.jsonl` vẫn giữ (trùng `thu_luot1.jsonl`), chờ bạn quyết có xóa không |
| T-12 | ✅ Đã sửa | B1 nhận đủ đầu vào như bộ quyết định của P; trần token 8192. Kết quả B0 cũ phải chạy lại vì đổi khóa bộ nhớ đệm |
| T-23 | ✅ Đã sửa | 1446 test đạt, cả khi không đặt `PYTHONUTF8`; 70 test đầu–cuối mới |
| T-24 | ✅ Đã sửa | Ngưỡng 1% cố định; "Xong khi" Bước 37 |
| T-26 | ✅ Đã sửa | 19 nhãn Xiaomi 15T đủ đoạn lặp, không đổi nhãn |
| T-29 | ✅ Đã sửa | `cach_sac` cùng loại phụ kiện; dòng độ sáng ở `bao_phu_dieu_kien.md`. Thiếu `dung_luong_pin` cho đồng hồ: ghi giới hạn (trang Galaxy Watch Ultra2 có công bố mAh) |
| T-30 | ✅ Đã sửa | Họ Holm B0–B3; lưu `thoi_gian_sinh_ms` |
| T-34 | ✅ Đã sửa | Đồng bộ theo Google Sheet. Còn 2 chỗ lệch cho bạn quyết: Bước 17, việc 35.1 |
| T-11 | ⚠️ Đã thử, không đạt | 78/168 cụm (46,4%) < 80%. Chờ bạn duyệt bổ sung luật từ 3 trang (`ket_qua/bao_phu/bao_cao_carbon.md` mục 3) |
| T-18 | ⏸ Để bạn làm | Hướng dẫn mục 2 cấm AI gợi ý khi rà tách. Danh sách: `T18_danh_sach_can_ra_tach.md` |

## ⚠️ Việc bảo mật cần làm ngay (ngoài kế hoạch)

Repo `23521228-BuiLeHuyPhuoc/KLTN` **đang công khai**. Commit `8946bb0` (08/10/2026) trong lịch sử `main` có tệp `.env` chứa một `ANTHROPIC_AUTH_TOKEN`. Mình chỉ đếm, không đọc giá trị. `ket_qua/thu_llm.md:203-216` ghi "cần thu hồi" nhưng chưa có xác nhận đã thu hồi. Nếu chưa làm, bạn vào trang quản lý khóa của nhà cung cấp, thu hồi khóa đó rồi tạo khóa mới. Xóa tệp khỏi Git không làm khóa hết hiệu lực.

## Cách làm

| Lượt | Phạm vi | Báo cáo |
|---|---|---|
| R1 | Thiết kế nghiên cứu, tính mới, thực tiễn, kịp hạn | [R1](carbon/R1_thiet_ke_tinh_moi_kha_thi.md) |
| R2 | Dữ liệu và nhãn | [R2](carbon/R2_du_lieu_nhan.md) |
| R3 | Mã nguồn, kiểm thử, kết quả | [R3](carbon/R3_ma_nguon_thuc_nghiem.md) |
| R4 | Nhất quán nội bộ của kế hoạch | [R4](carbon/R4_nhat_quan_ke_hoach.md) |
| R5 | Carbon kiểm chứng chéo, gộp trùng | [R5](carbon/R5_tong_hop_kiem_chung.md) (chi tiết đầy đủ từng mục T-xx, B-xx) |

Brief giao cho Carbon nằm ở [`_brief/`](_brief/). Carbon chỉ ghi đúng 5 tệp báo cáo, không sửa tệp nào khác. Không báo cáo nào ghi nhãn của tuyên bố bộ thử theo mã, nên bạn đọc được mà vẫn giữ tính mù của lượt 3. Trong lúc Carbon chạy có một phiên khác làm Bước 22 (PR #30), nên vài số dòng Carbon dẫn có thể lệch vài dòng.

## Bảng kết luận từng mục

Cột "Mình kiểm bằng gì": **chạy** là chạy lại mã trên cache hoặc dữ liệu thật; **đếm** là tự đếm hay tính lại; **đọc** là đọc mã hay văn bản gốc.

### Nhóm 1: lỗi thật, sửa ngay

| Mã | Vấn đề | Mình kiểm bằng gì, thấy gì | Cách sửa gợi ý |
|---|---|---|---|
| T-01 | P đạt Recall Đúng **23/64 (35,9%)** trên 108 tuyên bố tập phát triển, trả Chưa đủ cho 64/108 | **Chạy:** bộ thử 14/34, tập chính 9/30. Đồng thời FAR của P là 0/32 và 0/12, tức P quá thận trọng | Sửa cụm YAML bọc ngoặc, `vung_do` một dòng, tiêu đề bảng bị cắt, tên mục lọt vào `dieu_kien_khac`. Đây đúng là việc của Bước 28, làm trên tập phát triển là hợp lệ |
| T-03 | `data/nhan/thu.jsonl` trùng từng byte `thu_luot1.jsonl` (nhãn đã hủy) | **Đếm:** mã băm trùng; `do_recall.py:22`, `chay_b0.py:41` mặc định đọc tệp này; `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:590` ghi nhầm | Đổi mặc định và dòng 590 sang `thu_luot2.jsonl`, khoảng 10 phút |
| T-06 | Lỗi kỹ thuật LLM: P ra `CHUA_DU`, B0–B2 ra `LOI` | **Đọc:** `quyet_dinh.py:716-718` và `doi_chung/chung.py:18,61` | Cho P trả `LOI` khi `ban_ghi["loi"]` khác rỗng, giống đối chứng |
| T-09 | Đơn vị không khớp thuộc tính vẫn qua neo nguồn, sinh "tài liệu mâu thuẫn" giả | **Chạy:** `tb-00107` (IP68) ra `CHUA_DU D1b` vì `3 m` và `30 phút` lọt vào bằng chứng | Lọc đơn vị theo thuộc tính ở `neo_nguon.kiem_gia_tri` hoặc `cung_thuoc_tinh` |
| T-10 | Câu trích của LLM lược chữ, neo nguồn xóa mất giá trị tuyên bố | **Chạy:** 4 tuyên bố "120Hz" (`tb-00081`, `088`, `096`, `103`) mất giá trị, ra `D1a` | Phía tuyên bố: nếu chữ tuyên bố có đúng một giá trị khớp đơn vị thì neo lại |
| T-11 | Bỏ qua cổng "điểm dừng nhãn Lệch" ở Bước 16 | **Đọc:** `ket_qua/bo_thu/bao_cao.md` tự ghi "chưa đủ căn cứ"; chưa thử bao phủ trên 3 sản phẩm ngoài mẫu | Làm bài thử bao phủ trên 3 trang ngoài 12 mẫu trước Mốc 3; ghi rõ tiêu chí kappa không đo được như thiết kế |
| T-12 | B1 không nhận chữ tuyên bố, mã mẫu, hãng (P có dùng); trần token ra 4096 so với 8192 của P | **Đọc:** `b1.py:27-36`, `b0.py:38`, `trich_xuat.py:122` | Cho B1 cùng đầu vào mà luật của P dùng; cùng trần token |
| T-18 | Tách tay tập phát triển sót tuyên bố; `tb-00071` gộp hai giá trị | **Chạy/đọc:** bài `qc-dh-apple-watchse3-gemini-landing-ten-1` có "chống nước ở độ sâu 50m" mà 0 tuyên bố; `tb-00071` bị gán `che_do_nguon=nguon_thap` cho giá trị 18 giờ (sai, 18 giờ là chế độ thường) | Bổ sung tuyên bố sót, tách `tb-00071`, gán nhãn phần thêm. Cần trước Bước 29 vì tách tay là đáp án chấm tách tự động |
| T-20 | `dong_ho.sac_nhanh` đoán "dạng" theo đơn vị; điều kiện số khác đơn vị (giờ, phút) không quy đổi | **Đọc:** `quyet_dinh.py:81-84`, `trich_xuat.py:293`. Ví dụ ở mục 6.3 của chính hướng dẫn ("trong 1 giờ" so với "30 phút") sẽ ra `D1a` thay vì `D4` | Quy đổi giờ, phút khi đọc điều kiện; xác định dạng theo điều kiện đi kèm |
| T-21 | `lan_dieu_kien` lan điều kiện giữa hai mục cùng số mà không kiểm xung đột; lan cả cụm lạ sang đoạn sạch | **Đọc:** `quyet_dinh.py:276-317` | Chỉ lan khi không xung đột; không lan `dieu_kien_khac` từ đoạn giới thiệu. Góp phần vào T-01 |
| T-22 | `doc_so("1-120")` báo lỗi; "đảm bảo thời lượng xem video 30 giờ" không nhận là khẳng định | **Chạy:** đúng cả hai. Phần biên số thực (30,3 so với 30; 99 so với 100) có thật nhưng hầu như không gặp | Đọc khoảng `a-b`; nới cửa sổ chữ giữa từ khẳng định và con số. Phần biên số thực: không cần gấp |
| T-23 | pytest hỏng 2 test; chưa có test tích hợp trích xuất → quyết định | **Chạy:** `2 failed, 1362 passed, 1 skipped`. Không đặt `PYTHONUTF8=1` thì pytest dừng ngay lúc nạp test | `pip install -e .`; thêm `sys.path` cho 3 script; viết vài test tích hợp từ ví dụ V01–V51 |
| T-24 | Ngưỡng 1% "chọn lại trên tập phát triển" (T10 điểm 8) trái luật nhãn D3 "trong 1%" | **Đọc:** `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:1708` và `:2365`. Ý "Bước 24 trước Bước 27" nay không còn ý nghĩa vì Bước 27 đã làm trước | Cố định 1%; sửa "Xong khi" của Bước 37 (Bảng 8 thuộc Bước 38) |
| T-26 | 19/42 nhãn `chinh.jsonl` chỉ ghi một đoạn bằng chứng dù con số lặp ở nhiều đoạn (QĐ7) | **Đếm:** "120Hz" có ở `#004`, `#022`, `#037`, các nhãn chỉ ghi một đoạn | Bổ sung đoạn lặp. Chỉ ảnh hưởng Recall@k, không đổi nhãn |
| T-29 | `cach_sac` là `phu_kien` ở `sac_nhanh` nhưng là `che_do_hoat_dong` ở `cong_suat_sac`; `dong_ho.yaml` không có `dung_luong_pin` | **Đọc:** `dien_thoai.yaml:28,48`; `dong_ho.yaml` không có dòng nào | Thống nhất loại của `cach_sac` (ảnh hưởng thống kê theo 6 loại điều kiện, tức Tính mới 3). Thiếu `dung_luong_pin` thì ghi giới hạn, không đọc trang tập kiểm tra để thêm |
| T-30 | `danh_gia_he.py:213` đưa cả B4 vào họ Holm; P, B1, B2 không lưu thời gian sinh | **Đọc:** đúng như mô tả | Lọc họ Holm còn B0–B3; lưu `thoi_gian_sinh_ms` |
| T-34 | Ô đánh dấu lệch: đầu tệp 11/47 bước, thân bài 106/206 việc | **Đọc:** danh sách đầu tệp để trống Bước 1, 2, 5–12, 16 dù đã làm | Đồng bộ một lượt theo "Xong khi" |

### Nhóm 2: có thật, bạn phải chốt hướng

| Mã | Vấn đề | Mình kiểm | Câu hỏi cho bạn |
|---|---|---|---|
| T-02 | T3.5 cấm AI gán nhãn chuẩn; thực tế 59/66 nhãn lượt 2 do Claude gán, `chinh.jsonl` ghi `phuoc` cả 42 dòng dù nhật ký ghi Claude sửa 28 dòng | **Đếm** | Bạn chủ động chọn cách này nên đây không phải làm sai lén. Cần chốt: tập kiểm tra có tự làm 100% không AI không? Ghi phần AI tham gia vào nhãn bằng trường nào? |
| T-04 | `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:848` giả định tập kiểm tra gán xong 13/11 nên từ 24/11 đủ 10 ngày; thực tế Bước 23–24 chưa làm | **Đọc** | Lùi Mốc 3 đến ngày nào? Kích hoạt T9.2 để cắt Bước 43 không? |
| T-05 | Hướng dẫn nhúng vào câu lệnh B1/B2 dài 35.915 ký tự (khoảng 14–19k token), vượt trần 8.000 token/phút của Groq miễn phí | **Đếm** | Chạy B1/B2 bằng LLM nào? Trả phí Groq, hay rút gọn hướng dẫn theo nhóm như T12.2? (Gemini có trần lớn hơn) |
| T-07 | Lượt 3 gán lại trên bộ thử mà bạn đã thảo luận từng nhóm nhãn với Claude, và bạn biết tập chọn chứa mọi Lệch; kế hoạch còn 14 dòng ghi "người gán thứ hai" | **Đếm** | Giữ lượt 3 trên bộ thử, hay gán lại mù trên tập chính và tập kiểm tra theo tỷ lệ tự nhiên? Có nhờ CBHD tìm một người gán độc lập 40–50 câu không? |
| T-08 | Ước tính 286 tuyên bố nhân thẳng trung bình bộ thử; tập kiểm tra có 16 bài đồng hồ (ít tuyên bố) nên thực tế có thể chỉ khoảng 165; lực thống kê cho H1 (biên −5 điểm) yếu | **Đếm** phân bố 108 nhãn (Đúng 64, Lệch 25, Chưa đủ 11, Sai 8). Phần mô phỏng lực kiểm định mình chưa chạy lại | Giữ mốc "Recall Đúng tốt nhất của đối chứng" (hiện B0 đoán tràn với FAR 75% đang là mốc) hay đổi? Có báo cáo cỡ hiệu ứng nhỏ nhất phát hiện được (MDE) không? |
| T-15 | P−NN tắt cùng lúc neo nguồn và kiểm tra đầy đủ; chưa có cách chấm bằng chứng, lý do và cách ghép cho đánh giá đầu-cuối | **Chạy:** FAR của P và P−NN đều 0 (bộ thử 0/32, tập chính 0/12); trên tập chính P−NN cho kết quả giống hệt P. P−ĐK có FAR 28/32, nên đối chiếu điều kiện mới là phần tạo khác biệt | Đổi định nghĩa P−NN (chỉ bỏ neo nguồn), hay đổi chỉ số của H3? Phải chốt trước khi khóa T6.6 |
| T-16 | QĐ15 chấm Đúng cho câu mà 9/10 người khảo sát hiểu khác; Q06, Q12 giữ nguyên dù 6/10 hiểu khác (quá ngưỡng một nửa đã đặt) | **Đọc:** có kịch bản cận trên `doi_mac_dinh`, nhưng chưa có kịch bản đổi đúng mặc định Q06, Q12, và `chep_nhan` chỉ ghi "tính lại tay" | Đây không phải lỗi mà là lựa chọn bạn đã duyệt, nhưng hội đồng sẽ hỏi. Giữ QĐ15 và cài đủ kịch bản độ nhạy như Bước 37 đã hứa? |
| T-19 | "HyperCharge 67W": 3 tuyên bố `cong_suat_sac` là Lệch (theo V23), 3 tuyên bố `sac_nhanh` "(với sạc HyperCharge 67W)" là Đúng; hướng dẫn chưa ghi ngoại lệ `khong_mua_them` mà mã đã cài | **Đọc** | Hai kiểu nhãn này có thể biện được (67W là giá trị ở `cong_suat_sac` nhưng là điều kiện ở `sac_nhanh`), nhưng hướng dẫn chưa có câu nào nói rõ. Chốt luật rồi ghi vào mục 6.8 trước Bước 24 |
| T-31 | `mau_san_pham.csv` có hai mã băm (CRLF và LF); repo công khai đang chứa 85 tệp nguyên văn trang của hãng, trái lời đáp T11#16 "chỉ chia sẻ trích đoạn" | **Đếm:** đúng cả hai | Để repo riêng tư, hay sửa lời đáp T11#16? Ghi mã băm theo LF trong `.gitattributes`? |

### Nhóm 3: lỗi thật, sửa sau

| Mã | Vấn đề | Mình kiểm | Khi nào sửa |
|---|---|---|---|
| T-14 | Chương 1 và T1.3 nói 1 khối mới (bộ quyết định A–D); `chuong_3.md:9` và Hình 3.1 tô 3 khối; câu trả lời mẫu về tính mới viết "các cách hiện có để LLM tự phán đoán", trái với Chương 2 (VeriFin dùng Z3, ProgramFC chạy chương trình) | **Đọc** | Trước bản Chương 3 gửi CBHD và trước bảo vệ |
| T-17 | `api.py` khóa tuần tự toàn cục; một bài 5–9 lời gọi LLM dễ vượt 60 giây phía CopyPro | **Đọc:** `api.py:108,127` | Trước Bước 41 (quay video, demo) |
| T-25 | Dàn ý T8.1 và T13 chưa có mục khai báo dùng AI; T11 thiếu các câu hỏi phản biện về AI làm nhãn, QĐ15, VeriFin | **Đọc:** T8.1 không có chữ nào về AI | Trước Bước 42 |
| T-28 | `chep_nhan` lấy cả điều kiện từ tiêu đề nhóm dù nhãn dòng không chứa chữ đó | **Đọc:** `quyet_dinh.py:322-375`; mình chưa chạy ví dụ cụ thể | Cùng đợt sửa P, mức thấp |
| T-32 | `dt-xiaomi-15t#004` dính chữ "120HzMàn"; thiếu 5 ảnh `full.png` ở trang quá cao | **Đọc:** đúng | Tùy chọn: tách chữ dính khi tạo chỉ mục BM25, ghi ngoại lệ vào "Xong khi" |
| T-35 | Sổ sách nhỏ: 3 chỗ còn "5–10 người đọc", ngày cập nhật tháng 10 ở đầu kế hoạch, README, thẻ dữ liệu | **Đọc** | Lúc đồng bộ kế hoạch |

### Nhóm 4: không bắt buộc sửa

| Mã | Vấn đề | Kết luận của mình |
|---|---|---|
| T-13 | Thiếu đối chứng "LLM đọc trọn trang"; LLM sinh trùng LLM kiểm chứng; Bước 2 chưa có số đo API thật | Phần LLM trùng đã có quy tắc T6.2 mục 5 (báo kết quả chia theo LLM sinh). Bước 2 chỉ là sổ sách vì các bước sau đã gọi API thật. Đối chứng đọc trọn trang là gợi ý hay, có thể thay B4 nếu cắt Bước 43, nhưng không bắt buộc |
| T-27 | `chia_doan.py` ghi cứng 14 ngoại lệ theo mã đoạn của 2 mẫu tập kiểm tra | Chỉ là làm sạch ký hiệu chú thích ở Bước 7, đã ghi trong nhật ký. Sửa mã có thể làm đổi `doan.jsonl`. Chỉ cần khai báo trong phần mối đe dọa tính hợp lệ |

### Phần mình bác

| Mã | Ý bị bác | Lý do |
|---|---|---|
| T-33 | "T6.6 thiếu điều kiện một phía `b < c`, là lỗ hổng kiểm định hai phía" | Cột "Đạt" của H1 đã đòi FAR(P) thấp hơn từng đối chứng, nên chiều so sánh đã có. Phần còn lại của T-33 (Chương 1 thiếu "công suất sạc", lược đồ ở T3–T5 lỗi thời) là sổ sách thật, gộp vào lúc đồng bộ kế hoạch |
| T-04 | "Tiến trình thử lại nền đang làm phình log" | Không có tiến trình nào chạy lúc mình kiểm. Rủi ro thật là tệp 273 MB chưa nằm trong `.gitignore`, lỡ commit thì GitHub chặn vì quá 100 MB |

## Mục Carbon để lại cho bạn (R5 phần B)

| Mã | Câu hỏi |
|---|---|
| B-01 | CBHD đã xác nhận chính thức Mốc 1, Mốc 2, tiêu chí T6.6 chưa? Tên đề tài mới đã cập nhật trên hệ thống của Khoa chưa? |
| B-02 | B3 (`semviqa`) có chạy được trên Python 3.14, máy không GPU không? |
| B-03 | 6 chú thích thiếu trong `page.txt` của Galaxy Watch8 và 1 ký hiệu của S25 Ultra có chứa điều kiện thông số không? |
| B-04 | Đã đối chiếu nguyên văn Luật 75/2025/QH15, Điều 15a, khoản 3 trên Công báo chưa? |
| B-05 | Hợp đồng JSON phía nhánh `kiem-chung-thong-so` của CopyPro có khớp không? Bản sao lưu `data/nguon/` còn không? |
| B-06 | Khóa API cũ trong commit `8946bb0` đã thu hồi chưa (xem mục bảo mật)? |

## Thứ tự mình đề xuất

1. **Hôm nay:** thu hồi khóa cũ (bảo mật). Chốt các câu hỏi ở Nhóm 2, nhất là lịch (T-04), LLM cho đối chứng (T-05), chính sách AI cho tập kiểm tra (T-02).
2. **Trước khi gán tập kiểm tra (Bước 23–24):** chốt luật HyperCharge và đồng bộ hướng dẫn (T-19), sửa `thu.jsonl` (T-03).
3. **Trong thời gian chờ 10 ngày của Bước 32:** sửa cụm lỗi của P trên tập phát triển (T-01, T-09, T-10, T-20, T-21, T-22), sửa đối chứng (T-06, T-12), sửa dữ liệu phát triển (T-18, T-26), pytest (T-23), thử bao phủ (T-11).
4. **Trước khi khóa cấu hình:** chốt lại H1, H3 và P−NN (T-08, T-15), sửa T6.6, đồng bộ kế hoạch (T-24, T-29, T-34, T-35).
5. **Trước khi viết và demo:** T-14, T-17, T-25.
