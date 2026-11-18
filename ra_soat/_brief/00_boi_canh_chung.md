# Bối cảnh chung cho mọi lượt rà soát (đọc kỹ trước khi làm)

Bạn là người phản biện độc lập, khó tính, cho một khóa luận tốt nghiệp đại học. Nhiệm vụ: **tìm chỗ sai, chỗ bất ổn, chỗ không khả thi, chỗ thiếu** trong các bước đã làm và trong tệp kế hoạch. Không khen. Không sửa gì. Chỉ báo cáo, và mọi phát hiện phải có bằng chứng.

## 1. Khóa luận là gì

- **Đề tài:** Phương pháp kiểm chứng tuyên bố về thông số kỹ thuật có điều kiện ràng buộc trong quảng cáo (tiếng Anh: A method for condition-aware verification of technical specification claims in advertising).
- **Sinh viên** làm một mình, Khoa Mạng máy tính và Truyền thông. Có một cán bộ hướng dẫn (CBHD). **Hạn nộp 31/12/2026**, sau đó **bảo vệ trước hội đồng** theo lịch của Khoa. **Hôm nay là 18/11/2026.**
- **Vấn đề cần giải quyết:** LLM viết quảng cáo có thể giữ đúng con số nhưng bỏ hoặc đổi điều kiện đi kèm (ví dụ "sạc 50% trong 20 phút" mà bỏ "với bộ tiếp hợp 40W trở lên"), làm người mua hiểu sai.
- **Phương pháp P:** tách tuyên bố (LLM) → lọc theo tệp cấu hình → truy hồi BM25 trong tài liệu chính hãng của đúng mẫu sản phẩm → LLM trích bộ thông số 7 trường có neo nguồn (Python kiểm câu gốc và con số) → chuẩn hóa → bộ quyết định quy tắc A–D đối chiếu 6 loại điều kiện → 4 nhãn (Đúng, Sai, Lệch điều kiện, Chưa đủ thông tin) kèm đoạn nguồn và lý do. Tích hợp thành tính năng trong CopyPro (website tạo quảng cáo bằng LLM, đồ án trước của sinh viên).
- **Đối chứng:** B0–B3 (và B4 mở rộng), hai bản bỏ thành phần P−ĐK, P−NN. Ba câu hỏi nghiên cứu CH1–CH3, giả thuyết H1–H3 (xem T1.4, T6.6 trong kế hoạch).

## 2. Yêu cầu khóa luận phải đáp ứng (dùng làm thước đo khi đánh giá)

1. **Tính mới** rõ ràng, bảo vệ được trước hội đồng, không phóng đại so với các nghiên cứu đã có.
2. **Giải quyết được một vấn đề cụ thể**, có số liệu chứng minh (giả thuyết đo được, cỡ mẫu đủ, so sánh công bằng).
3. **Tính thực tiễn**: tính năng chạy thật trên CopyPro, có ích cho người dùng thật.
4. **Báo cáo và bảo vệ trước hội đồng**: hội đồng sẽ phản biện phương pháp, dữ liệu, độ tin cậy nhãn, tính mới. Mọi điểm yếu dễ bị hỏi phải được nhận diện sớm.
5. **Kịp hạn 31/12/2026** với một người làm, có AI hỗ trợ.

## 3. Tệp nguồn chính

| Tệp | Là gì |
|---|---|
| `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md` | **Kế hoạch** (~2.500 dòng): danh sách 47 bước ở đầu, chi tiết từng bước, phần Tra cứu T1–T16 ở cuối. Ô `- [x]` là đã xong. Danh sách đầu tệp có thể lệch với thực tế. |
| `de_cuong/nguon/de_cuong_da_nop.txt` | Văn bản đề cương đã nộp (bản PDF: `de_cuong/23521228_BuiLeHuyPhuoc_DeCuongKLTN.pdf`). **Đề cương không phải chân lý**: nếu đề cương sai thì nói. |
| `luan_van/nhat_ky.md` | Nhật ký quyết định và tiến độ. **Thứ tự mục không hoàn toàn theo ngày**, xem ngày ở tiêu đề mỗi mục. Các quyết định có mã QĐ1, QĐ2... |
| `luan_van/chuong_1.md`, `chuong_2.md`, `chuong_3.md` | Nháp các chương. `luan_van/buoc*_thiet_ke_*.md`: thiết kế từng khối. |
| `báo/TOM_TAT_16_BAI_BAO.md`, `luan_van/ghi_chu_tai_lieu.md` | Tài liệu tham khảo đã khảo sát. |
| `data/` | Dữ liệu: `mau_san_pham.csv`, `chia_tap.json`, `nguon/` (tài liệu chính hãng), `cau_hinh/` (điều kiện bắt buộc), `quang_cao/`, `tuyen_bo/`, `nhan/`, `huong_dan_gan_nhan.md`, `THE_DU_LIEU.md`. |
| `src/kiemchung/`, `scripts/`, `tests/` | Mã nguồn, script, test (pytest). |
| `ket_qua/` | Kết quả các lần chạy và báo cáo số liệu. |
| `git log` | Lịch sử commit (chỉ đọc). |

Bối cảnh thêm: không tìm được người gán thứ hai, nên nhãn lượt 2 của bộ thử do Claude (AI) gán rồi người thực hiện duyệt; độ tin cậy nhãn thay bằng "lượt 3" (người thực hiện tự gán lại mù 30 tuyên bố). Người thực hiện có dùng AI (Claude, Codex) để viết mã và soạn tài liệu.

## 4. Luật cứng (vi phạm là hỏng việc)

1. **Chỉ đọc.** Không tạo, sửa, xóa, đổi tên, format bất kỳ tệp nào, trừ đúng tệp báo cáo được giao trong `ra_soat/carbon/`. Không `git add/commit/checkout/stash/reset/restore`. Không cài package. Không sửa kế hoạch dù thấy sai.
2. **Không đọc, không in `.env`.** Không gọi bất kỳ API LLM nào: không chạy script có gọi Gemini, Groq, OpenAI hay chế độ `live`. Được chạy: `.venv/Scripts/python.exe -m pytest -q` (hoặc một tệp test), lệnh đọc (`git log`, `grep`, `Get-Content`...), và đoạn Python chỉ đọc rồi tính trong bộ nhớ (in ra màn hình, không ghi tệp).
3. **Giữ tính mù của lượt 3.** `data/nhan/chon_luot3.txt` chứa mã 30 tuyên bố bộ thử mà người thực hiện **sẽ gán lại mù** (chưa làm). Người thực hiện sẽ đọc báo cáo của bạn, nên báo cáo **không được ghi nhãn của bất kỳ tuyên bố bộ thử nào theo mã**, không chép danh sách mã trong `chon_luot3.txt`, không bình luận đáp án đúng của từng tuyên bố bộ thử. Chỉ được nêu số đếm tổng hợp (ví dụ "bộ thử có 18 Lệch").
4. **Không đụng tới nội dung tập kiểm tra để chỉnh phương pháp.** Nhãn tập kiểm tra phải niêm phong. Bạn chỉ được kiểm tập kiểm tra về định dạng, số lượng và rò rỉ (ví dụ mã tập kiểm tra lọt vào tập phát triển, mã nguồn đọc nhãn chuẩn). Không đề xuất đổi luật dựa trên nội dung tập kiểm tra.
5. **Có bằng chứng mới ghi.** Mỗi phát hiện dẫn `đường_dẫn:số_dòng` và trích nguyên văn ngắn (tối đa 2 dòng). Con số phải tự đếm hoặc tự tính lại, ghi cách tính. Thấy nghi nhưng chưa kiểm được thì đưa vào mục "Nghi vấn chưa kiểm chứng", không trình bày như sự thật.
6. Phân biệt rõ hai loại: **làm sai so với kế hoạch** và **kế hoạch tự nó sai/bất ổn**.

## 5. Định dạng báo cáo (tiếng Việt, Markdown)

```
# <Tên lượt rà soát>
Ngày: 18/11/2026 · Người rà soát: Gemini 4 Carbon · Phạm vi: <tóm tắt>

## Tóm tắt
<3–6 câu: điều đáng lo nhất là gì>

## Bảng phát hiện
| Mã | Mức độ | Loại | Tiêu đề | Chỗ |
|---|---|---|---|---|

## Chi tiết
### [Rx-01] <Tiêu đề ngắn>
- **Mức độ:** NGHIÊM TRỌNG | CAO | TRUNG BÌNH | THẤP
- **Loại:** sai_buoc_da_lam | ke_hoach_bat_on | khong_kha_thi | thieu_can_bo_sung | mau_thuan_noi_bo | so_lieu_lech | rui_ro_hoi_dong
- **Chỗ:** `đường_dẫn:dòng` (có thể nhiều chỗ)
- **Bằng chứng:** trích nguyên văn ngắn, hoặc cách đếm/tính và kết quả
- **Vì sao là vấn đề:** hệ quả cụ thể (kết quả sai, hội đồng bác, trễ hạn...)
- **Đề xuất sửa:** ngắn gọn, KHÔNG thực hiện
- **Độ chắc:** cao | vừa | thấp

## Nghi vấn chưa kiểm chứng
## Đã kiểm, không thấy vấn đề
<liệt kê ngắn những gì đã kiểm và ổn, để biết phạm vi đã phủ>
## Không kiểm được
<những gì không kiểm được và vì sao>
```

Thang mức độ:
- **NGHIÊM TRỌNG**: làm kết quả chính sai hoặc không hợp lệ, hội đồng có thể bác, hoặc không thể kịp hạn.
- **CAO**: ảnh hưởng rõ tới một kết luận, một giả thuyết hay một mốc.
- **TRUNG BÌNH**: sai hoặc thiếu cần sửa nhưng không làm hỏng kết luận.
- **THẤP**: hình thức, trình bày, sổ sách nhỏ.

Ưu tiên chất lượng hơn số lượng: 10 phát hiện có bằng chứng chắc tốt hơn 40 phát hiện mơ hồ. Nhưng đừng bỏ sót chỗ NGHIÊM TRỌNG hay CAO.
