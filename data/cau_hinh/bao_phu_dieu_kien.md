# Bảng bao phủ điều kiện (Bước 8)

**Ngày:** 26/10/2026 · **Trạng thái:** bản 2, đã chốt cùng người thực hiện; YAML viết từ bảng này.

**Nguồn:** chỉ 4 mẫu tập phát triển (T3.5 quy tắc 4): `dt-apple-iphone17`, `dt-xiaomi-15t`, `tn-samsung-buds3pro`, `dh-apple-watchse3`. Đã đọc trọn `page.txt` trang chính của 4 mẫu và `bo_sung/page.txt` của Xiaomi 15T; phần đánh giá của người dùng trên trang Samsung (dòng 688–1199) chỉ dò bằng tìm kiếm. Mã đoạn lấy từ `doan.jsonl` ở commit `f09e66a`; `(u)` là trang `url`, `(b)` là trang `bo_sung`; `ct` nghĩa là nằm trong `chu_thich` của đoạn đó.

## 1. Quy ước

**Loại điều kiện** (sáu loại của đề cương): CĐ = chế độ hoạt động, BP = bộ phận, PK = phụ kiện, ĐĐ = điều kiện đo, PB = phiên bản, KGT = kiểu giá trị.

**Vai trò:**

- **QĐ** (tham gia quyết định nhãn): đổi điều kiện thì con số đổi, và người mua không tự suy ra được điều kiện đó.
- **NC** (chỉ lưu làm ngữ cảnh): quy trình đo chuẩn, định nghĩa thuật ngữ hoặc câu rào chung. Không làm thay đổi con số ứng với lựa chọn của người dùng. Danh sách ở mục 5.

**Căn cứ:** BC = bằng chứng trong tập phát triển; CH = chuẩn quốc tế; HB = hiểu biết chung về nhóm sản phẩm (T5.7 cho phép).

**Trạng thái:** Chốt (đã có quyết định, ghi ở mục 9). "Xác nhận ở Bước 10" nghĩa là cách hiểu mặc định sẽ được khảo sát người đọc kiểm lại; sai thì sửa cấu hình.

**Ba trạng thái của một điều kiện** (T5.7), áp dụng cho mọi dòng:

| Trạng thái | Khi nào | Xử lý |
|---|---|---|
| Không áp dụng | Có bằng chứng điều kiện không áp dụng cho trường hợp đang xét (ví dụ máy không có chống ồn) | Không đòi trích giá trị. Không suy từ việc tài liệu im lặng |
| Không nêu | Quảng cáo không nói điều kiện | Dùng cột "Không nêu thì hiểu là", ghi vào `mac_dinh` |
| Chưa xác định | Không đủ căn cứ xác định điều kiện hoặc phạm vi | Chưa đủ thông tin (D1a), ghi nguyên nhân |

**Kiểu giá trị mặc định của tuyên bố** (điểm 2, T10): con số trống trong quảng cáo được hiểu như cách hãng công bố.

- **Thời lượng pin, thời gian sạc, độ sáng, tần số quét, zoom, công suất sạc:** mức tối đa như hãng công bố. Quảng cáo bỏ "lên đến" vẫn khớp; lý do ghi thêm ghi chú "quảng cáo bỏ 'lên đến'" nhưng không đổi nhãn. Chỉ từ khẳng định rõ ("luôn", "ít nhất"...) mới là Lệch (D2), vì các từ này hứa một mức sàn mà tài liệu không hứa.
- **Dung lượng pin:** điển hình.
- Căn cứ (đảo lại chiều 26/10, xem `luan_van/phan_tich_dieu_kien_ngoai_cau_hinh.md` mục 8.1): báo cáo gốc của FTC 2012 cho thấy quảng cáo "up to 47%" và "47%" không khác nhau có ý nghĩa thống kê về cách người đọc hiểu, nên quảng cáo chép con số mà bỏ "lên đến" không gây hiểu sai hơn chính tài liệu. Đề tài so quảng cáo với tài liệu, không đo hiệu năng thực tế. Khớp với ví dụ ở đoạn 73 của đề cương.

**Điều kiện lạ trong tài liệu** (chốt 26/10, T10 điểm 15). Phát hiện điều kiện làm theo kiểu mở, hiểu điều kiện làm theo kiểu đóng:

- Bước trích xuất ghi **mọi** cụm điều kiện gắn với một giá trị trong tài liệu, kèm loại (một trong sáu) và câu trích; cụm không khớp cách diễn đạt nào trong cấu hình ghi vào `dieu_kien_khac`. Không bỏ cụm nào vì cấu hình không biết.
- Giá trị có `dieu_kien_khac` thì điều kiện đó là **chưa xác định**: quảng cáo khớp giá trị này ra Chưa đủ thông tin (D1a, nguyên nhân `dieu_kien_la`), **không bao giờ ra Đúng**. Ghi vào thống kê "chưa hỗ trợ".
- Cụm chỉ là câu rào chung (mục 5) không tính là điều kiện lạ.
- Tùy chọn, chọn ở Bước 33 trên tập phát triển: nếu tài liệu có từ hai giá trị chỉ khác nhau ở cùng một điều kiện lạ, coi đó là lựa chọn của người dùng và áp "kém thuận lợi nhất" (quảng cáo trùng giá trị tốt hơn là Lệch; không cao hơn giá trị kém nhất là Đúng). Mặc định tắt.

**Chọn con số để so khi quảng cáo không nêu điều kiện** (chốt 26/10). Dữ liệu ghi điều kiện của tuyên bố là "không nêu", không tự viết thêm. Con số để so được chọn theo tài liệu của mẫu:

| Tài liệu của mẫu | Cách so | Ví dụ |
|---|---|---|
| Chỉ một con số cho thuộc tính (cùng bộ phận), không kèm cụm điều kiện nào trong toàn bộ tài liệu, kể cả cụm cấu hình chưa biết | So thẳng; ghi "tài liệu không nêu điều kiện" | Watch SE 3 "độ sáng đỉnh 1000 nit" ("đỉnh" gắn với một giá trị duy nhất nên là kiểu giá trị, xem mục 2.4): quảng cáo 1000 nit là Đúng, 1500 nit là Sai |
| Có con số kèm điều kiện lạ | Chưa đủ thông tin (D1a, `dieu_kien_la`) | Giả định: "10 giờ khi tắt chế độ chơi game" mà cấu hình không biết "chế độ chơi game" |
| Nhiều con số, mỗi số ghi rõ điều kiện | So với con số ứng với cách hiểu mặc định (cột "Không nêu thì hiểu là"); ghi các trường lấy mặc định vào `mac_dinh` | Buds3 Pro "pin 7 giờ": mặc định nghe nhạc, chống ồn bật là 6 giờ; 7 giờ chỉ đạt khi tắt chống ồn nên Lệch |
| Nhiều con số mà không xác định được số nào ứng với quảng cáo | Chưa đủ thông tin (D1a) | iPhone "độ sáng đỉnh 3000 nit" ("đỉnh" là HDR hoặc ngoài trời); zoom 2x, 4x của Xiaomi |

Lý do giữ cách hiểu mặc định thay vì trả Chưa đủ thông tin cho mọi quảng cáo không nêu điều kiện: quảng cáo gây hiểu sai hay không phụ thuộc người mua hiểu câu đó thế nào. Không có giả định thì không phân biệt được "pin 6 giờ" (đúng với cách dùng thông thường) với "pin 7 giờ" (chỉ đạt khi tắt chống ồn). Hai chốt chặn cho điểm yếu của cách này: khảo sát 20–30 người ở Bước 10, và phân tích độ nhạy ở Bước 37 (tính lại khi mọi nhãn phụ thuộc mặc định đổi thành Chưa đủ thông tin).

## 2. Điện thoại

### 2.1 Thời lượng pin (`thoi_luong_pin`)

Đơn vị: giờ · Cao hơn tốt hơn · Kiểu mặc định: tối đa như hãng công bố · Nguồn: `dt-apple-iphone17#016(u)`, `dt-xiaomi-15t#047(b)`.

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Hoạt động sử dụng | CĐ | iPhone: xem video 30 giờ, xem video trực tuyến 27 giờ. Xiaomi: sử dụng liên tục 13,19 giờ | Khi hãng công bố theo hoạt động | Hoạt động kém thuận lợi nhất trong các hoạt động hãng công bố (iPhone: 27 giờ) | QĐ | BC, T4.5 | Chốt, xác nhận ở Bước 10 |
| "Lên đến", "Tối đa" | KGT | "Lên đến 30 giờ", "Tối đa 13,19 giờ" | Mọi số liệu | Như hãng công bố (tối đa); bỏ "lên đến" vẫn khớp, ghi chú trong lý do; từ khẳng định là Lệch (D2) | QĐ | BC, FTC 2012 | Chốt |
| Phiên bản | PB | Tập phát triển không tách thời lượng pin theo phiên bản | Khi tài liệu tách theo phiên bản | Phiên bản nêu trong tên | QĐ | HB, T4.5 | Chốt |

### 2.2 Sạc nhanh, thời gian sạc tới mốc phần trăm (`sac_nhanh`)

Đơn vị: phút · Thấp hơn tốt hơn · Kiểu mặc định: tối đa như hãng công bố · Nguồn: `dt-apple-iphone17#016(u)` (kèm `ct`), `#040(u)` (trong hộp chỉ có cáp); `dt-xiaomi-15t#047(b)`, `#005(u)` `ct`, `#014(u)` (bộ sản phẩm chỉ có cáp).

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Công suất bộ tiếp hợp | PK | iPhone: ≥40W qua cáp USB-C, 50% trong 20 phút; ≥30W qua MagSafe, 50% trong 30 phút; cả hai bán riêng. Xiaomi: củ ≥67W, không có trong hộp, đầy 100% trong 50 phút | Khi hãng nêu bộ sạc | Không mua thêm phụ kiện: chỉ có đồ trong hộp, nên con số không đạt được; quảng cáo không nêu bộ sạc thì Lệch | QĐ | BC, ví dụ trong đề cương | Chốt |
| Cách sạc: cáp hay MagSafe | PK | 20 phút qua cáp; 30 phút qua MagSafe | Máy hỗ trợ sạc không dây | Sạc bằng cáp | QĐ | BC | Chốt |
| Mốc phần trăm | ĐĐ | 50% (iPhone), 100% (Xiaomi) | Mọi số liệu | Không có mặc định; quảng cáo không nêu mốc thì chưa xác định (D1a) | QĐ | BC | Chốt |
| "Lên đến" | KGT | "Sạc lên đến 50% trong 20 phút" | Mọi số liệu | Như hãng công bố (tối đa); bỏ "lên đến" vẫn khớp, ghi chú trong lý do; từ khẳng định là Lệch (D2) | QĐ | BC, FTC 2012 | Chốt |
| Bắt đầu từ cạn pin; tính giờ từ khi hiện logo | ĐĐ | `ct` của iPhone `#016` | | | NC | BC | Chốt |

### 2.3 Công suất sạc (`cong_suat_sac`, mới)

Đơn vị: W · Cao hơn tốt hơn · Kiểu mặc định: tối đa · Nguồn: `dt-apple-iphone17#021(u)` (kèm `ct`), `dt-xiaomi-15t#005(u)` (kèm `ct`).

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Bộ sạc | PK | iPhone: MagSafe hoặc Qi2 lên đến 25W, cần bộ tiếp hợp ≥30W. Xiaomi: HyperCharge 67W, khuyến cáo củ ≥67W, không có trong hộp | Khi hãng nêu bộ sạc | Không mua thêm; quảng cáo không nêu bộ sạc thì Lệch | QĐ | BC | Chốt |
| Có dây hay không dây | CĐ | 25W là không dây (iPhone); 67W là có dây (Xiaomi) | Máy công bố cả hai cách | Có dây | QĐ | BC | Chốt |
| "Lên đến" | KGT | "lên đến 25W" | Mọi số liệu | Mức tối đa; bỏ "lên đến" không tính là Lệch | QĐ | Năng lực tối đa | Chốt |

### 2.4 Độ sáng (`do_sang`)

Đơn vị: nit · Cao hơn tốt hơn · Kiểu mặc định: tối đa · Nguồn: `dt-apple-iphone17#005(u)`; `dt-xiaomi-15t#004(u)`, `#037(b)`, `#038(b)`.

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Chế độ hiển thị | CĐ | iPhone: tiêu chuẩn 1000, HDR 1600, ngoài trời 3000. Xiaomi: 3200 khi tự tăng sáng dưới ánh sáng mạnh | Mọi số liệu | Chế độ thông thường (tiêu chuẩn) | QĐ | BC, T4.5 | Chốt, xác nhận ở Bước 10 |
| Phần diện tích đo | ĐĐ | Xiaomi: "trên 25% diện tích màn hình", "APL 25%" | Khi hãng nêu | Như hãng công bố cho chế độ đó | QĐ | BC, T4.5 | Chốt |
| Cách gọi theo hãng (điểm 12) | CĐ | Apple: "tối đa" là tiêu chuẩn; "đỉnh" là HDR hoặc ngoài trời. Xiaomi: "cực đại" là chế độ tự tăng sáng, đo trên 25% diện tích | Chỉ khi tài liệu dùng chữ đó để phân biệt từ hai giá trị trở lên; chữ gắn với một giá trị duy nhất là kiểu giá trị tối đa (áp cho mọi hãng) | Quảng cáo iPhone chỉ ghi "đỉnh" thì chưa xác định (D1a) | QĐ | BC | Chốt |

"Độ sáng tối thiểu 1 nit" là đại lượng khác, không so với độ sáng tối đa; xếp ngoài phạm vi.

### 2.5 Tần số quét (`tan_so_quet`)

Đơn vị: Hz · Cao hơn tốt hơn · Kiểu mặc định: tối đa · Nguồn: `dt-apple-iphone17#004(u)`; `dt-xiaomi-15t#004(u)`, `#037(b)` `ct`.

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Thích ứng hay cố định ở mức tối đa | KGT | iPhone: "thích ứng lên đến 120Hz". Xiaomi: "tối đa 120Hz", thay đổi theo ứng dụng | Mọi số liệu | Mức tối đa: "màn hình 120Hz" khớp; "luôn 120Hz" là D2 Lệch | QĐ | BC, T4.5 | Chốt |

### 2.6 Zoom (`zoom`)

Đơn vị: x · Cao hơn tốt hơn · Kiểu mặc định: tối đa · Nguồn: `dt-apple-iphone17#009(u)`, `#012(u)`; `dt-xiaomi-15t#007(u)`, `#006(u)`, `#027(b)`.

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Quang học hay kỹ thuật số (điểm 3) | CĐ | iPhone: quang học 2x, kỹ thuật số lên đến 10x. Xiaomi: kỹ thuật số lên đến 60x | Mọi số liệu | Quang học | QĐ | BC, T4.5 | Chốt |
| Độ phóng đại hay phạm vi thu phóng | ĐĐ | iPhone: phóng đại quang học 2x, phạm vi quang học 4x | Khi hãng nêu cả hai | Độ phóng đại | QĐ | BC | Chốt (mới) |
| Chụp ảnh hay quay video | CĐ | iPhone: kỹ thuật số 10x khi chụp, 6x khi quay | Khi hãng tách | Chụp ảnh | QĐ | BC | Chốt (mới) |

"Telephoto 2x chất lượng quang học" của iPhone tính là quang học, vì chính Apple ghi "Độ phóng đại quang học 2x". Xiaomi ghi các mức 0,6x, 1x, 2x, 4x (`#027(b)`) mà không nói loại: chưa xác định (mục 7).

### 2.7 Kháng nước (`khang_nuoc`)

So khớp: mã IP theo nhánh của IEC 60529 (điểm 11) · Nguồn: `dt-apple-iphone17#007(u)` (kèm `ct`); `dt-xiaomi-15t#012(u)` `ct`, `#035(b)`.

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Mã IP | ĐĐ | IP68 (cả hai) | Mọi số liệu | Chữ số bụi 0–6 xếp thành thang; chữ số nước tách hai nhánh 0–6 (tia nước) và 7–8 (ngâm), 8 khắc nghiệt hơn 7; chỉ so trong cùng nhánh | QĐ | CH (IEC 60529) | Chốt |
| Độ sâu, thời gian | ĐĐ | iPhone: 6 m, 30 phút. Xiaomi: 3 m, 30 phút | Mọi số liệu | Điều kiện thử hãng công bố | QĐ | BC, T4.5 | Chốt |
| Loại nước, nhiệt độ | ĐĐ | Xiaomi: nước ngọt tĩnh lặng, chênh nhiệt ≤5K; không chịu nước muối, nước clo, nước áp suất cao | Khi hãng nêu | Điều kiện thử hãng công bố; quảng cáo nêu nước biển hay hồ bơi là đổi điều kiện | QĐ | BC | Chốt (mới) |
| Hoạt động bị cấm | ĐĐ | Xiaomi: không dùng khi đi biển, đi bơi | Khi hãng nêu | Quảng cáo gợi ý hoạt động bị cấm là Lệch, loại đổi điều kiện | QĐ | BC | Chốt (mới) |

### 2.8 Dung lượng pin (`dung_luong_pin`)

Đơn vị: mAh · Cao hơn tốt hơn · Kiểu mặc định: điển hình · Nguồn: `dt-xiaomi-15t#005(u)`, `#022(b)`, `#046(b)`. iPhone 17 không công bố mAh.

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Điển hình hay định mức | KGT | "5500mAh (thông thường)", "(typ)" | Mọi số liệu | Điển hình; "thông thường" là cách gọi của điển hình, chỉ dùng trong thuộc tính này | QĐ | BC, HB (cần trích chuẩn khi viết) | Chốt |
| Phiên bản | PB | Không tách theo phiên bản | Khi tài liệu tách | Phiên bản nêu trong tên | QĐ | HB | Chốt |

## 3. Tai nghe

### 3.1 Thời lượng pin (`thoi_luong_pin`)

Đơn vị: giờ · Cao hơn tốt hơn · Kiểu mặc định: tối đa như hãng công bố · Nguồn: `tn-samsung-buds3pro#038(u)` (khối "Thời gian phát", kèm `ct`), `#044(u)` (bảng thông số), `#042(u)` (bảng so sánh, có máy khác), `#020(u)` `ct` (ANC bật mặc định).

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Chống ồn bật hay tắt | CĐ | Phát nhạc 6 giờ (bật) / 7 giờ (tắt); đàm thoại 4,5 / 5 giờ | Tai nghe có chống ồn | Bật. Có bằng chứng từ hãng: "ANC được bật theo mặc định" | QĐ | BC, T4.5 | Chốt |
| Chỉ tai nghe hay kèm hộp sạc | BP | Phát nhạc kèm hộp 26 / 30 giờ; đàm thoại kèm hộp 20 / 22 giờ; cách ghi "7/30" là tai nghe/tổng | Tai nghe có hộp sạc | Chỉ tai nghe | QĐ | BC, T4.5 | Chốt |
| Phát nhạc hay đàm thoại | CĐ | Phát nhạc 6–7 giờ; đàm thoại 4,5–5 giờ | Khi hãng tách | **Phát nhạc**: công dụng chính; Samsung định nghĩa "thời gian phát" là phát nhạc trực tuyến | QĐ | BC | Chốt, xác nhận ở Bước 10 |
| "Đến", "Lên đến" | KGT | "Đến 7/30 giờ", "Lên đến 6" | Mọi số liệu | Như hãng công bố (tối đa); bỏ "lên đến" vẫn khớp, ghi chú trong lý do; từ khẳng định là Lệch (D2) | QĐ | BC, FTC 2012 | Chốt |

### 3.2 Sạc nhanh (`sac_nhanh`, số giờ dùng sau X phút sạc)

Galaxy Buds3 Pro **không công bố** sạc nhanh. Luật lấy từ T4.5: số phút sạc (ĐĐ); bộ phận (BP), không nêu thì hiểu là tai nghe; "lên đến" theo nguyên tắc điểm 2. Căn cứ: HB. Trạng thái: Chốt; chưa có bằng chứng trong tập phát triển (mục 7).

### 3.3 Kháng nước (`khang_nuoc`)

Nguồn: `tn-samsung-buds3pro#044(u)` ("Chuẩn IP57"), `#038(u)` `ct`.

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Bộ phận | BP | IP57 cho tai nghe; "hộp sạc không có khả năng kháng nước" | Tai nghe có hộp sạc | Tai nghe | QĐ | BC, T4.5 | Chốt |
| Mã IP | ĐĐ | IP57 | Mọi số liệu | So theo nhánh như mục 2.7 | QĐ | CH | Chốt |
| Độ sâu, thời gian, loại nước | ĐĐ | Ngâm 1 m nước ngọt, tối đa 30 phút | Mọi số liệu | Điều kiện thử hãng công bố | QĐ | BC | Chốt |
| Hoạt động bị cấm | ĐĐ | Không khuyến cáo dùng khi tắm biển hoặc ở bể bơi | Khi hãng nêu | Quảng cáo gợi ý bơi là Lệch | QĐ | BC | Chốt (mới) |

### 3.4 Dung lượng pin (`dung_luong_pin`)

Nguồn: `tn-samsung-buds3pro#044(u)`.

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Bộ phận | BP | Tai nghe 50 mAh; hộp sạc 515 mAh | Tai nghe có hộp sạc | Tai nghe | QĐ | BC, T4.5 | Chốt |
| Điển hình | KGT | "(mAh, Typical)" | Mọi số liệu | Điển hình | QĐ | BC | Chốt |

## 4. Đồng hồ

### 4.1 Thời lượng pin (`thoi_luong_pin`)

Đơn vị: giờ · Cao hơn tốt hơn · Kiểu mặc định: tối đa như hãng công bố · Nguồn: `dh-apple-watchse3#008(u)` (kèm `ct` kịch bản), `#002(u)` (cỡ vỏ, phiên bản).

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Chế độ nguồn | CĐ | Thường 18 giờ; nguồn điện thấp 32 giờ | Máy có chế độ nguồn thấp | Chế độ thường | QĐ | BC, T4.5 | Chốt |
| Hoạt động | CĐ | Sử dụng bình thường 18 giờ; tập luyện ngoài trời 7 giờ | Khi hãng tách | **Sử dụng bình thường**: hãng công bố đúng hoạt động này. Khác điện thoại, nơi hãng không công bố "sử dụng bình thường" | QĐ | BC | Chốt, xác nhận ở Bước 10 |
| Phiên bản GPS hay GPS + Cellular | PB | Cùng 18 giờ; kịch bản đo khác nhau (bản Cellular có 4 giờ dùng mạng di động) | Khi tài liệu tách giá trị | Phiên bản nêu trong tên; trang không tách giá trị thì không áp dụng | QĐ | BC | Chốt |
| "Lên đến" | KGT | "lên đến 18 giờ" | Mọi số liệu | Như hãng công bố (tối đa); bỏ "lên đến" vẫn khớp, ghi chú trong lý do; từ khẳng định là Lệch (D2) | QĐ | BC, FTC 2012 | Chốt |

Cỡ vỏ 40mm và 44mm khác trọng lượng và diện tích màn hình, nhưng trang không tách thời lượng pin theo cỡ vỏ.

### 4.2 Sạc nhanh (`sac_nhanh`)

Hai dạng: thời gian tới mốc phần trăm, và số giờ dùng sau X phút sạc · Kiểu mặc định: tối đa như hãng công bố · Nguồn: `dh-apple-watchse3#009(u)` (kèm `ct`), `#023(u)` (trong hộp chỉ có cáp).

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Bộ tiếp hợp 20W | PK | Chỉ ghi trong chú thích, là thiết bị dùng khi đo; không có trong hộp | Khi hãng nêu | Không mua thêm; quảng cáo không nêu thì Lệch | QĐ | BC | Chốt |
| Cáp sạc nhanh | PK | Có trong hộp | Mọi số liệu | Cáp đi kèm | QĐ | BC, T4.5 | Chốt |
| Mốc phần trăm | ĐĐ | 0–80% trong khoảng 45 phút | Dạng 1 | Không có mặc định; không nêu mốc thì D1a | QĐ | BC | Chốt |
| Số phút sạc | ĐĐ | Sạc 15 phút dùng 8 giờ; sạc 8 phút dùng 8 giờ | Dạng 2 | Không có mặc định | QĐ | BC | Chốt (mới) |
| Hoạt động sau khi sạc | CĐ | Sử dụng bình thường (15 phút); theo dõi giấc ngủ (8 phút) | Dạng 2 | Sử dụng bình thường | QĐ | BC | Chốt (mới) |
| "Lên đến" | KGT | "lên đến 80%", "lên đến 8 giờ" | Mọi số liệu | Như hãng công bố (tối đa); bỏ "lên đến" vẫn khớp, ghi chú trong lý do; từ khẳng định là Lệch (D2) | QĐ | BC, FTC 2012 | Chốt |

### 4.3 Kháng nước (`khang_nuoc`)

Nguồn: `dh-apple-watchse3#016(u)` (kèm `ct`).

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Chuẩn và độ sâu | ĐĐ | 50 m theo ISO 22810:2010 | Mọi số liệu | Như hãng công bố; chuẩn hóa 5ATM = 50 m; mức cao hơn là tốt hơn | QĐ | CH (ISO 22810) | Chốt |
| Hoạt động được phép hay bị cấm | ĐĐ | Được: bơi trong bể, dưới biển ở vùng nước nông. Cấm: lặn bình dưỡng khí, lướt ván, thể thao dưới nước tốc độ cao | Khi hãng nêu | Quảng cáo gợi ý hoạt động bị cấm là Lệch | QĐ | BC | Chốt |

### 4.4 Độ sáng (`do_sang`)

Nguồn: `dh-apple-watchse3#007(u)`.

| Điều kiện | Loại | Giá trị gặp | Phạm vi áp dụng | Không nêu thì hiểu là | Vai trò | Căn cứ | Trạng thái |
|---|---|---|---|---|---|---|---|
| Chế độ hiển thị | CĐ | "Độ sáng đỉnh 1000 nit", không nêu chế độ; chỉ có một con số độ sáng tối đa | Mọi số liệu | "Đỉnh" gắn với một giá trị duy nhất nên là kiểu giá trị tối đa, không phải chế độ; tài liệu không kèm cụm điều kiện nào khác nên so thẳng: quảng cáo 1000 nit là Đúng | QĐ | BC | Chốt |

## 5. Chú thích chỉ lưu làm ngữ cảnh (NC)

Các câu sau xuất hiện ở cả 4 mẫu. Chúng không làm đổi con số ứng với lựa chọn của người dùng, nên không tham gia quyết định nhãn:

- "Phòng thí nghiệm (nội bộ)", "điều kiện phòng thí nghiệm có kiểm soát".
- "Thiết bị tiền sản xuất", "phần mềm tiền phát hành".
- "Kết quả thực tế có thể khác", "phụ thuộc cấu hình mạng, cài đặt, cường độ tín hiệu".
- "Khả năng chống nước không phải vĩnh viễn, giảm theo thời gian"; "không bảo hành hư hỏng do chất lỏng".
- Quy trình đo chuẩn: "thử với thiết bị cạn pin", "tính giờ từ khi hiện logo".
- Kịch bản định nghĩa "sử dụng bình thường" của Watch (300 lần xem giờ, 90 thông báo...): lưu làm định nghĩa của điều kiện, không phải điều kiện riêng.

## 6. Mâu thuẫn và chỗ dễ nhầm trong tài liệu

1. **Buds3 Pro `#044`:** dòng "Tổng thời gian phát nhạc (Giờ, bật ANC) Lên đến 30" gắn nhãn "bật ANC", nhưng chỗ khác ghi bật ANC thì tổng là 26 giờ. Chú thích ở `#038` ghi "với tính năng bật/tắt ANC... tối đa 30 giờ". Quảng cáo nêu tổng 30 giờ kèm bật ANC thì D1b. Giữ quyết định ở Bước 5: không dùng tổng 26/30 giờ làm căn cứ.
2. **Buds3 Pro `#042`:** bảng so sánh có cả Buds3 và Buds FE trong cùng đoạn. Chỉ dùng giá trị của cột Buds3 Pro.
3. **Buds3 Pro:** chú thích "ANC được bật theo mặc định" nằm ở `#020`, không cùng đoạn với số liệu pin `#038`. Cấu hình ghi chú thích này làm căn cứ cho cách hiểu; không trông vào việc truy hồi kéo được đoạn `#020`.
4. **Apple:** trên trang iPhone 17, "tối đa" chỉ chế độ tiêu chuẩn, "đỉnh" chỉ chế độ khác, vì các chữ này phân biệt nhiều giá trị. Trên trang Watch SE 3, "đỉnh" gắn với giá trị duy nhất nên là kiểu giá trị tối đa (điểm 12 làm rõ 26/10).

## 7. Chưa hỗ trợ và dự đoán độ bao phủ

Ghi trước khi có kết quả, để đối chiếu ở Bước 37–38:

- **Hãng không có trong tập phát triển:** OPPO (điện thoại), Samsung (điện thoại, đồng hồ). Cách gọi riêng của các hãng này chưa có trong cấu hình; dự kiến độ bao phủ thấp hơn các hãng còn lại.
- **Tai nghe sạc nhanh:** không có bằng chứng; luật chỉ dựa vào T4.5.
- **Zoom của Xiaomi:** các mức 2x, 4x không ghi là quang học hay kỹ thuật số, nên chưa xác định.
- **Phiên bản điện thoại:** chưa có ví dụ tài liệu tách số liệu theo phiên bản.
- **Tài liệu dạng PDF:** tập phát triển không có hướng dẫn sử dụng dạng PDF.

## 8. Ngoài phạm vi

Có điều kiện nhưng không thuộc danh sách thuộc tính: dung lượng lưu trữ khả dụng; kích thước màn hình theo đường chéo; độ sáng tối thiểu; độ bền pin (≥80% sau 1600 chu kỳ); tần số lấy mẫu cảm ứng (bật Game Turbo); điều chỉnh độ sáng PWM; độ phân giải và tốc độ quay video; tỷ lệ vật liệu tái chế; các con số so với đời trước (anten, tản nhiệt, viền).

## 9. Quyết định

| Mục | Nội dung | Trạng thái |
|---|---|---|
| Điểm 2 (T10) | Thời lượng pin, thời gian sạc, độ sáng, tần số quét, zoom, công suất sạc: tối đa như hãng công bố; bỏ "lên đến" vẫn khớp, ghi chú trong lý do; chỉ từ khẳng định là Lệch (D2). Dung lượng pin: điển hình. Đảo lại chiều 26/10 theo số liệu gốc FTC 2012 (sáng 26/10 từng chốt "bỏ lên đến là Lệch") | Chốt 26/10 |
| Điểm 3 (T10) | Zoom: quang học hay kỹ thuật số là chế độ hoạt động; thêm độ phóng đại hay phạm vi (điều kiện đo), chụp ảnh hay quay video (chế độ hoạt động) | Chốt |
| Điểm 4 (T10) | Từ khẳng định: luôn, đảm bảo, bảo đảm, ít nhất, mọi lúc; chỉ xét trong câu trích của giá trị; bỏ dạng phủ định; chưa thêm "tối thiểu" | Chốt |
| Điểm 11 (T10) | Mã IP so theo nhánh của IEC 60529; ISO 22810 so theo độ sâu, cao hơn là tốt hơn | Chốt |
| Điểm 12 (T10) | Cách gọi độ sáng khai báo theo hãng, chỉ từ tập phát triển; "đỉnh" của iPhone thì D1a. Làm rõ: chữ phân biệt từ hai giá trị trở lên là chế độ; gắn với một giá trị duy nhất là kiểu giá trị tối đa | Chốt |
| Điểm 15 (T10, mới) | Điều kiện lạ trong tài liệu: ghi mọi cụm điều kiện, cụm cấu hình không biết vào `dieu_kien_khac`; giá trị kèm điều kiện lạ thì quảng cáo khớp nó ra D1a, không bao giờ ra Đúng; luật chung cho điều kiện lạ là tùy chọn chọn ở Bước 33 | Chốt 26/10 |
| Mới | Thêm thuộc tính công suất sạc cho điện thoại | Chốt 26/10 |
| Mới | Bộ tiếp hợp 20W của Watch là điều kiện bắt buộc | Chốt 26/10 |
| Mới | Chọn con số để so khi quảng cáo không nêu điều kiện: một con số thì so thẳng; nhiều con số thì theo cách hiểu mặc định; không xác định được thì D1a (mục 1) | Chốt 26/10 |
| Mới | Tai nghe: hoạt động mặc định là phát nhạc | Chốt 26/10, xác nhận ở Bước 10 |
| Mới | Đồng hồ: hoạt động mặc định là sử dụng bình thường | Chốt 26/10, xác nhận ở Bước 10 |
| Mới | Watch "độ sáng đỉnh 1000 nit": một con số nên so thẳng ("đỉnh" là kiểu giá trị tối đa theo điểm 12) | Chốt 26/10 |
| Mới | Điểm dừng ở Bước 16 cho nhãn Lệch và phương án lùi (3 nhãn cộng cờ thiếu điều kiện) | Chốt 26/10, đã ghi vào kế hoạch |
| Mới | Hai chốt chặn cho cách hiểu mặc định: khảo sát 20–30 người (Bước 10), phân tích độ nhạy (Bước 37) | Chốt 26/10, đã ghi vào kế hoạch |
| Mới | Cấu trúc tệp: `chung.yaml` cộng 3 tệp nhóm | Chốt 26/10 |
| Mới | Thử độ bao phủ trên 3 trang sản phẩm ngoài 12 mẫu, là một tiêu chí của điểm dừng Bước 16 | Chốt 26/10; làm ở phiên sau, trước Bước 9 |
