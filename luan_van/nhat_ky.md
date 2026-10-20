# Nhật ký khóa luận

## 20/10/2026 — Bước 6

- Bổ sung 4 mẫu Xiaomi: theo đồng ý của người thực hiện, `page.html` (`<!DOCTYPE html>` + DOM sau khi cuộn hết trang) và `page.txt` (`document.body.innerText`) của 8 trang (`url` và `url_bo_sung`) được tải từ Chrome thật qua Claude in Chrome lúc 15:35–15:38 (HTTP 200, không trang nào có nút mở rộng ở phần nội dung). Không giả User-Agent hay lách chặn của Chromium headless. Thông tin lúc lưu ở `data/nguon/thu_cong_20261020.json`.
- `scripts/nhap_nguon_thu_cong.py` chép nguyên byte vào `data/nguon/`, tạo `meta.json` (`"phuong_phap": "thu_cong_chrome"`) và dựng `full.png` từ `page.html` đã lưu bằng Chromium headless, tắt JavaScript. Ảnh này không phải ảnh chụp trực tiếp: www.mi.com chặn 10 tệp CSS khi dựng, nên phần đầu/cuối trang vỡ bố cục, phần thông số vẫn đọc được. 4 trang `url` có đủ 4 tệp; 4 trang `bo_sung` thiếu `full.png` vì thiếu CSS làm trang cao 247.000–461.000 px, Chromium không chụp được. 66 test đạt; mã băm `page.html`/`page.txt` khớp giữa Downloads, thư mục đích và `meta.json`.
- Trước khi nhập, `data/nguon/dt-xiaomi-15t/` có thêm `page.html`, `page.txt`, `full.png` và `bo_sung/full.png` ghi lúc 14:13–15:18 không rõ nguồn (không do lần chạy nào được ghi ở đây); các tệp này đã bị thay bằng bản lưu từ Chrome.
- Ví dụ 16–17 khớp: trang thông số Xiaomi 15T ghi "Độ sáng cực đại: 3200 nit trên 25% diện tích màn hình". Cả 8 trang Xiaomi có chú thích dạng `*`/"thử nghiệm" trong `page.txt`; với 8 mẫu tập kiểm tra chỉ kiểm có mặt chú thích, không dùng để thiết kế.
- Kết quả: đủ 12 mẫu, trang `url` của mỗi mẫu có 4 tệp. Còn: sao lưu ảnh ra ngoài máy; 4 `bo_sung/full.png` của Xiaomi.

## 20/10/2026 — Bước 6 (lần chạy đầu: chưa chụp được 4 mẫu Xiaomi)

- Thêm nhánh PDF vào `scripts/chup_nguon.py` (tải bằng `context.request`, lưu `tai_lieu.pdf`, `page.txt` trích bằng `pypdf` có dòng `=== Trang N ===`, `meta.json`; không có `page.html`/`full.png`). Thêm `pypdf==6.21.1` vào `requirements.txt`. Sửa `full_page_png`: lần chụp đầu quá 15 giây thì chụp lại với 60 giây (trang bổ sung của OPPO Find X8 kẹt ở lần đầu, chưa rõ nguyên nhân; `meta.json` ghi chú việc chụp lại). Tất cả 50 test của `tests/test_chup_nguon.py` đạt.
- Chụp được 6/10 mẫu, mã băm khớp: Apple Watch SE 3, OPPO Find X8 (kèm `bo_sung/`), Galaxy S25 Ultra (kèm `bo_sung/`), AirPods Pro 3, AirPods 4, Galaxy Watch8 (trang + PDF hướng dẫn 158 trang, bản trích 255.281 ký tự).
- 4 mẫu Xiaomi (Xiaomi 15T, Redmi Note 14 Pro+ 5G, Redmi Buds 6 Pro, Xiaomi Watch S4) trả HTTP 403 "Access Denied" khi chụp bằng Chromium headless, cả `url` và `url_bo_sung`; `curl` thường thì nhận HTTP 200. Chưa tìm cách vượt chặn; thư mục các mẫu này mới chỉ có `meta.json` ghi lỗi. Xiaomi 15T thuộc tập phát triển nên cần giải quyết trước Bước 8.
- Chỗ nghi vấn OPPO Find X8 xác nhận: trang thông số ghi "Giá trị định mức 5630mAh, giá trị tiêu chuẩn 5490mAh", còn chú thích trên trang giới thiệu ghi ngược lại (tiêu chuẩn 5.630, định mức 5.490). Hai trang của hãng không thống nhất; xử lý như điều kiện không rõ khi dùng làm nhãn.
- Apple Watch SE 3 khớp ví dụ 13–15: "lên đến 18 giờ khi sử dụng bình thường", "lên đến 32 giờ ở Chế Độ Nguồn Điện Thấp". Ví dụ 16–17 (Xiaomi 15T) chưa kiểm được vì chưa chụp. Chưa kiểm hết chú thích điều kiện của 6 mẫu đã chụp và chưa sao lưu ảnh.
- `data/nguon/dt-apple-iphone17/page.html` bị ghi đè lúc 13:01 (không rõ nguyên nhân, mã băm lệch `meta.json`); đã khôi phục từ commit e69fe57, mã băm khớp lại.

## 20/10/2026 — Làm rõ phạm vi điều kiện trong kế hoạch

- Theo trao đổi với người thực hiện, giữ nguyên 12 mẫu và chia tập ở Bước 4; bổ sung Bước 8 bảng bao phủ từ bốn mẫu phát triển, phạm vi áp dụng và phân biệt không áp dụng/không nêu/chưa xác định. Chưa tạo cấu hình hoặc đánh dấu hoàn thành Bước 8–9.
- Làm rõ Bước 9 và T5.3/T5.7: nhãn chuẩn dựa trên bằng chứng, không theo giới hạn hỗ trợ của hệ thống; không dùng điều kiện riêng của tập kiểm tra để bổ sung quy tắc.
- Bổ sung kiểm thử ở Bước 27 và phân tích độ bao phủ ở Bước 37–38; giữ các ca chưa hỗ trợ trong chỉ số chính. Đây là điều chỉnh kế hoạch, chưa thực hiện thí nghiệm hoặc sửa dữ liệu/nhãn.

## 19/10/2026 — Bước 5

- Viết `scripts/chup_nguon.py` bằng Python Playwright 1.63.0 (Chromium 1243) thay cho script `.mjs` cũ; 27 test ở `tests/test_chup_nguon.py` đạt. Tạo `.venv` trên máy Windows, mới cài `playwright` và `pytest`; các test cần `pydantic` chưa chạy được.
- Chụp iPhone 17 và Galaxy Buds3 Pro vào `data/nguon/`: HTTP 200, đủ 4 tệp, mã băm khớp. Trang Samsung cần bấm "Xem thêm" của mục thông số; các nút con ghi sai trạng thái `aria-expanded`, nên script kiểm văn bản sau mỗi lần bấm và hoàn tác khi nội dung bị thu lại. Không bấm vùng đánh giá của người dùng; banner cookie Samsung chỉ có nút "Chấp nhận" nên để nguyên, không che thông số.
- Chỗ nghi vấn tổng pin Buds3 Pro vẫn còn: khối thông số ghi 26 giờ khi bật ANC, chú thích ghi tối đa 30 giờ cho cả bật/tắt ANC. Giữ quyết định không dùng tổng 26/30 giờ. Các con số của ví dụ 1–12, 18 ở T4.6 khớp bản chụp; trang Samsung gọi xuyên âm là "Ambient".
- Thêm `.gitattributes` để `data/nguon/` không bị đổi xuống dòng khi checkout. Chưa sao lưu ảnh chụp ra ngoài máy. Với Bước 6: `url_bo_sung` của Galaxy Watch8 là PDF, script hiện chưa tải được.

## 15/10/2026 — Kiểm lại Bước 4 theo yêu cầu

- Đọc lại 18 trang HTML chính hãng và hướng dẫn Watch8 tiếng Việt (bìa có SM-L330; kiểm trực tiếp trang 149). Hồ sơ `data/kiem_tra_nguon_buoc4.json` ghi ba giá trị/điều kiện cho mỗi mẫu, URL, thời điểm và hash nguồn. Đây là kiểm nguồn, không phải gán nhãn chuẩn.
- Sửa cách đếm chưa đúng phạm vi: bỏ kích thước S25 Ultra, điều kiện bật vùng nhịp tim Watch8, tần số lấy mẫu cảm ứng Xiaomi 15T và hai mức công suất sạc OPPO. Thay bằng các thuộc tính đã có trong T4.5, không mở rộng cấu hình từ tập kiểm tra.
- Bổ sung điều kiện trong chú thích cho AirPods Pro 3 và Watch SE 3; đánh dấu cách ghi không thống nhất về tổng pin Buds3 Pro và zoom 10x S25 Ultra. Không tự suy ra thiết lập thử pin Redmi Note 14 Pro+ mà hãng không công bố.
- Sau sửa, cả 12 mẫu có ít nhất ba mục phù hợp tiêu chí chọn nguồn. Giữ nguyên 4 mẫu phát triển/8 mẫu kiểm tra. Thẻ dữ liệu lên phiên bản 2; CSV chỉ thêm nguồn Xiaomi 15T và hướng dẫn Watch8. Chưa thu thập bộ bằng chứng theo Bước 5–6 hoặc chạy API.

## 15/10/2026 — Bước 4

- Chọn 12 mẫu và ghi `data/mau_san_pham.csv`: 5 điện thoại, 4 tai nghe, 3 đồng hồ; 4 hãng Apple, Samsung, Xiaomi, OPPO. Tạo `data/THE_DU_LIEU.md` bản đầu với tiêu chí nguồn, phiên bản sản phẩm, đường dẫn và dấu vết kiểm tra ít nhất ba thông số kèm điều kiện cho mỗi mẫu.
- Chốt 4 mẫu phát triển theo kế hoạch: iPhone 17, Xiaomi 15T, Galaxy Buds3 Pro, Apple Watch SE 3. Tám mẫu còn lại thuộc tập kiểm tra; tập này có đủ ba nhóm và bốn hãng. Không chia các biến thể cùng dòng sang hai tập. Redmi được tính là Xiaomi.
- Từ hôm nay, mọi lựa chọn thiết kế (tệp cấu hình, ví dụ hướng dẫn, câu lệnh gửi LLM, quy tắc, ngưỡng, tham số) chỉ dựa trên tập phát triển, theo T3.5 quy tắc 4. Đã xem nguồn tập kiểm tra để chọn mẫu, chưa dùng chúng để thiết kế hoặc đánh giá phương pháp.
- Kiểm tra trực tiếp nguồn tiếng Việt của hãng. AirPods 4 dùng trang hỗ trợ mã 121203 cho bản thường vì URL giới thiệu chuyển sang mẫu khác. Galaxy Watch8 chọn Bluetooth 44 mm. Ghi nguồn bổ sung khi chú thích nằm ở trang giới thiệu. Chưa thu thập bộ bằng chứng Bước 5–6, chưa gọi thêm API hoặc tạo nhãn chuẩn.

## 15/10/2026 — Bước 3

- Đối chiếu nhận định nghiên cứu trong đề cương bản cuối với 16 PDF gốc; kiểm SHA-256 khớp danh mục. Tạo `ghi_chu_tai_lieu.md` gồm bảng kiểm trích dẫn, ghi chú từng bài và số trang PDF bắt đầu từ 1; kiểm trực tiếp ảnh các bảng NumPert, Fathom, ViNumFCR.
- Bổ sung bốn bài FActScore, ProgramFC, ViWikiFC v2, Beyond Binary và báo cáo FTC 2012; lưu PDF, nguồn tải, thời điểm và mã băm trong `báo/bo_sung/`. Khảo sát có mục tiêu, không tuyên bố đã bao quát toàn bộ lĩnh vực.
- Làm rõ thiết lập 89,90% của ViFactCheck, BAcc/chi phí MiniCheck, phạm vi FA = 0 của VeriFin; đánh dấu diễn đạt 62% của NumPert, nguồn gốc sáu loại điều kiện và những nhận định tính mới cần thu hẹp. Chưa sửa đề cương PDF/DOCX hoặc tạo nhãn chuẩn bằng AI.
- Cập nhật trạng thái Bước 3 và dòng kế hoạch cũ về sáu bài để khớp bộ 16 bài hiện tại; gắn hồ sơ kiểm trang trong `kiem_tra_tai_lieu.json`. Bước tiếp theo là chọn mẫu/chia tập ở Bước 4. Không sửa mã LLM hoặc chạy thêm API trong bước khảo sát này.

## 13/10/2026 — Bước 2

- Khảo sát đúng repo `/home/phuocblh/KLTN/KLTN` (`main`, HEAD `78c8150`, ban đầu sạch); đọc README, Bước 2/T3.1/T3.5/T4.6/T5.1/T5.3 và đối chiếu PDF đề cương bản cuối. Giữ nguyên repo CopyPro bên cạnh, đề cương và lịch kế hoạch; không commit/push theo yêu cầu.
- Tạo sáu thư mục, package editable, `.venv` Python 3.14.4, đủ thư viện cùng pin/lock; chọn Pyvi vì gọn. Bộ pin cần Python ≥ 3.12; thay wrapt prerelease bằng 2.5.0 ổn định. 16 import, tokenizer, biểu đồ không giao diện và `pip check` đạt.
- Viết giao diện Gemini/Groq chung, cache JSON theo hash đầy đủ và tách mock/live, nhật ký JSONL an toàn, timeout/retry giới hạn. 32 kiểm thử đạt (gồm cache qua tiến trình mới, SDK/HTTP giả lập); còn một cảnh báo deprecation từ SDK Google.
- Tạo 10 câu kỹ thuật nguyên văn từ T4.6 cùng kỳ vọng đọc từ câu, không phải nhãn chuẩn nghiên cứu; chạy offline ba cấu hình, 30 lượt lặp đọc cache. Ghi tài nguyên môi trường, phiên bản và nguồn quota chính thức vào `ket_qua/thu_llm.md`; chưa xây BM25/P hoặc dùng tập kiểm tra.
- Trở ngại: thiếu khóa Gemini/Groq, chưa xác minh Free tier/quota tài khoản; live tiền kiểm exit 2, không gọi API thật. Git xác nhận `.env` từng được commit rồi bỏ theo dõi nhưng chưa có căn cứ khóa đã thu hồi. Cần người dùng thu hồi/tạo mới và cấu hình `.env`, sau đó chạy thử thật; Bước 2 chưa hoàn thành đầy đủ.
