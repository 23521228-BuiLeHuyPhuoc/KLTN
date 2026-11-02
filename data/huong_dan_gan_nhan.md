# Hướng dẫn gán nhãn bốn lớp

**Bản:** 2 · **Ngày:** 01/11/2026, cập nhật 02/11/2026 · **Bước:** 16 · **Bản 1:** 27/10/2026 (Bước 9), giữ trong lịch sử git.

**Căn cứ:** đề cương bản cuối (11/10/2026); T4 trong `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md`; bộ luật Bước 8 ở `data/cau_hinh/` (commit `ab6146c`) và bảng bao phủ `data/cau_hinh/bao_phu_dieu_kien.md`; 8 quyết định của Bước 16, duyệt ngày 01/11/2026, và 6 quyết định sau rà soát, duyệt ngày 02/11/2026 (nhật ký Bước 16).

**Dùng cho:** người gán nhãn chuẩn (Bước 13, 16, 20, 24, 32); đặc tả của bộ quyết định trong P (Bước 27), nên mọi ví dụ ở mục 9 là kiểm thử hồi quy; phần hướng dẫn trong câu lệnh của đối chứng B2.

**Phạm vi ví dụ:** chỉ 4 mẫu tập phát triển: `dt-apple-iphone17`, `dt-xiaomi-15t`, `tn-samsung-buds3pro`, `dh-apple-watchse3`. Ví dụ về Điện thoại A, Tai nghe B, Đồng hồ C là câu tự đặt về sản phẩm giả định. Tệp này không chứa trang, con số hay tên mẫu của tập kiểm tra, vì tệp đi vào câu lệnh của B2.

**Phần chưa chắc:** cách hiểu mặc định ở mục 5 đã đối chiếu với khảo sát Bước 10 (10 người, 28/10/2026; mục 5.1). Mẫu nhỏ và lệch về người học công nghệ thông tin, nên các ví dụ có ghi chú `mac_dinh` được tính lại ở phân tích độ nhạy Bước 37. Ba quy tắc chưa có số liệu người đọc: "hơn X" là từ khẳng định (mục 6.2), đọc cụm theo hoàn cảnh của điều kiện (mục 6.8, ý 2), và chế độ người dùng tự chọn lấy chế độ kém thuận lợi nhất khi điều kiện không có trong bảng mục 5 (mục 6.7, ý 4; nhãn dựa vào ý này ghi `mac_dinh=ngoai_bang`).

**Thay đổi so với bản 1.** Bước 16 có 19 quy tắc (QT). QT1–QT11 chỉ nói rõ điều bản 1 đã ngụ ý. QT12–QT19 là 8 quyết định, đều chọn phương án A. Nhãn của 48 ví dụ cũ không đổi.

- QT1. Xác định điều kiện trước rồi mới so con số; không chọn điều kiện theo con số (mục 1, 5, 7).
- QT2. Cách hiểu mặc định dùng ở mọi dòng D; D1a chỉ có ba lối vào (mục 5, 7).
- QT3. D1 chỉ khi tài liệu không có con số nào cho thuộc tính; có số nhưng không có ở điều kiện của tuyên bố là D6 (mục 7).
- QT4. D2 cần từ khẳng định gắn với con số; chỉ thiếu "lên đến" thì không phải Lệch; "tối đa" của điều kiện đo không phải D2 (mục 2, 3, 6.2, 6.3, 7).
- QT5. Tuyên bố nêu rõ phụ kiện là đủ; một điều kiện không vừa nêu rõ vừa ghi mặc định (mục 5, 8).
- QT6. Con số của điều kiện không phải giá trị của thuộc tính; mã ghi chú mới `nham_vai` (mục 6.9, 8).
- QT7. Cụm khen không có con số thì bỏ qua (mục 2, 6.2, 6.8).
- QT8. D1b chỉ xét điều kiện của tuyên bố, áp cho mọi con số (mục 7); ngoại lệ khi con số khớp cả hai giá trị thêm ngày 02/11 (QĐ13).
- QT9. Mã IP khác nhánh: trùng mã ở điều kiện khác thì D4, không trùng thì D5 (mục 6.6, 7).
- QT10. Chỗ trống của mẫu câu lý do là câu trích nguyên văn, đổi tên thành `{câu trích}` (mục 8).
- QT11. Gán lại theo bản 2 là một lượt mới, không xem nhãn lượt trước (mục 8).
- QT12 (QĐ1). Gán theo chữ của tuyên bố; tiêu chí gắn điều kiện khi tách; rà tách trước khi gán (mục 1, 2).
- QT13 (QĐ2). Đọc cụm điều kiện theo nghĩa với người mua; phụ lục cụm của cấu hình (mục 6.5, 6.7, 6.8, 13; lý do của V07).
- QT14 (QĐ3). Cụm phủ nhiều giá trị: tuyên bố phải đúng ở giá trị kém thuận lợi nhất, loại `doi_dieu_kien` (mục 6.6, 6.8, 8).
- QT15 (QĐ4). "hơn", "trên", "không dưới", "trở lên" đứng liền con số là từ khẳng định (mục 6.2).
- QT16 (QĐ5). Ghi `mac_dinh` mọi khóa tuyên bố không nêu, ở mọi dòng từ D1a tới D6 (mục 8; ghi chú của nhiều ví dụ ở mục 9).
- QT17 (QĐ6). Không tạo giá trị mới bằng phép tính (mục 6.9).
- QT18 (QĐ7). Ghi mọi đoạn có cùng con số ở cùng điều kiện (mục 8; bằng chứng của một số ví dụ).
- QT19 (QĐ8). D4 vẫn tính mọi điều kiện khác; đặt trước ngưỡng xét lại (mục 11.2).
- Thêm mã ghi chú `khang_dinh`, `chua_xac_dinh`, `nham_vai`; thêm ba ví dụ V49–V51.

**Cập nhật 02/11/2026** (sau rà soát hướng dẫn, công cụ và bản gán lượt 2; người thực hiện duyệt QĐ9–QĐ15). Nhãn của 50 ví dụ không đổi; V03 đổi theo QĐ15.

- QĐ9. Ngưỡng xét lại ở mục 11.2 chỉ đếm ca tuyên bố nêu rõ một hoạt động mà giá trị trùng thuộc hoạt động khác (kiểu V42); không đếm ca tuyên bố không nêu hoạt động (kiểu V24).
- QĐ10. Mục 6.7 ý 4 (chế độ kém thuận lợi nhất cho điều kiện ngoài bảng mục 5) giữ, ghi rõ chưa khảo sát; nhãn dựa vào ý này ghi `mac_dinh=ngoai_bang` (mục 8).
- QĐ11. Ở bước gán, điều kiện trực tiếp cùng loại gắn với con số thắng cụm phủ nằm ở vế nói tác dụng (mục 6.8, như tiêu chí tách 2 ở mục 2).
- QĐ12. "sử dụng", "dùng" đứng riêng là mức dùng chung, coi như chưa nêu hoạt động, ở mọi nhóm (mục 6.8 ý 3, phụ lục 13).
- QĐ13. D1b có ngoại lệ: con số khớp cả hai giá trị mâu thuẫn thì dò tiếp D2–D3; báo riêng các ca tài liệu mâu thuẫn (mục 7, 8, 11.4; lý do của V48).
- QĐ14. "ánh sáng mạnh" bỏ khỏi phụ lục cụm của chế độ ngoài trời; cụm phụ lục ứng với cách gọi chế độ trong cấu hình (mục 6.8 ý 1, 2).
- QĐ15. Luật chép đúng nhãn của tài liệu: tuyên bố gọi điều kiện bằng đúng nhãn mà tài liệu gắn cho một dòng thông số, không thiếu chữ điều kiện nào của nhãn, thì cùng điều kiện với dòng đó; xét trước cách hiểu mặc định (mục 6.8, V03; mã ghi chú `chep_nhan`).
- Sửa chữ: mục 4 (bảng so sánh `#041`, `#042`), mục 6.4 (dòng D1a), mục 6.8 ý 6 (`kem_hop_sac` chỉ với thời lượng pin), mục 6.9 (tài liệu có số ở cách sạc khác), mục 8 (`giay_nghi`, mã `ngoai_bang`, `mau_thuan_khop_ca_hai`).

## 1. Quy trình ngắn

0. **Tuyên bố là đơn vị gán.** Gán theo chữ của tuyên bố, không theo câu gốc hay bài quảng cáo. Tuyên bố đã được rà theo tiêu chí gắn điều kiện ở mục 2 trước khi gán. Thấy tuyên bố vẫn thiếu điều kiện so với câu gốc thì ghi vào câu hỏi nhãn, vẫn gán theo tuyên bố.
1. Tách bài quảng cáo thành tuyên bố (mục 2).
2. Tìm trong tài liệu của mẫu các thông số cùng sản phẩm và thuộc tính với tuyên bố (mục 4).
3. Xác định điều kiện của tuyên bố: điều kiện nêu rõ giữ nguyên (mục 6.8), điều kiện không nêu lấy cách hiểu mặc định (mục 5, 6). Không chọn chế độ, bộ phận, hoạt động hay phụ kiện vì con số của tuyên bố chỉ khớp ở đó. Con số trùng giá trị ở điều kiện khác là việc của D4, không phải căn cứ để đổi điều kiện.
4. Đi lần lượt D1 → D6, dừng ở dòng đầu tiên thỏa (mục 7).
5. Ghi nhãn, loại biến đổi, bằng chứng, lý do, ghi chú và số giây đã gán (mục 8).

## 2. Tách tuyên bố

- Mỗi tuyên bố chỉ có **một thuộc tính và một giá trị**. "Pin 6 giờ, sạc đầy trong 1 giờ" tách thành hai tuyên bố.
- **Giữ ngữ cảnh:** tên sản phẩm, phiên bản, bộ phận và điều kiện nằm ở câu trước hoặc câu sau phải đưa vào tuyên bố. Thay "tai nghe này", "máy" bằng tên sản phẩm.
- **Giữ nguyên chữ của quảng cáo** cho điều kiện và kiểu giá trị: không thêm điều kiện quảng cáo không nói, không bỏ "lên đến", "định mức". Từ khẳng định ("luôn", "đảm bảo", "ít nhất", "hơn"...) chỉ giữ khi nó gắn với con số của tuyên bố (mục 6.2); từ ở vế nói việc khác thì không đưa vào tuyên bố.
- **Chỉ giữ tuyên bố có thuộc tính trong cấu hình** (16 thuộc tính):
  - Điện thoại: thời lượng pin, sạc nhanh, công suất sạc, độ sáng, tần số quét, zoom, kháng nước, dung lượng pin.
  - Tai nghe: thời lượng pin, sạc nhanh, kháng nước, dung lượng pin.
  - Đồng hồ: thời lượng pin, sạc nhanh, kháng nước, độ sáng.
- **Bỏ:** khối lượng, kích thước, phiên bản Bluetooth, độ sáng tối thiểu, độ bền pin theo chu kỳ sạc; tuyên bố cảm tính ("pin trâu", "sáng rực"); cụm khen không có con số ("cả ngày", "suốt ngày dài", "không lo hết pin", "siêu bền", "bền bỉ", "vượt trội", "tuyệt đối", "trọn vẹn", "không giới hạn"), kể cả khi cụm đứng cạnh một con số; so sánh với sản phẩm khác hoặc đời trước; giá và khuyến mãi; tuyên bố không có con số hay mã kiểm được, trừ khẳng định có/không ("hộp sạc cũng kháng nước").
- **Gộp tuyên bố trùng** chỉ khi hai lần nhắc cùng con số và cùng điều kiện. Câu nhắc một con số hai lần, một lần kèm điều kiện, một lần không, thì là hai tuyên bố: người đọc lướt có thể chỉ thấy lần không kèm điều kiện.

**Tiêu chí gắn điều kiện.** Điều kiện nào thuộc con số thì đưa vào tuyên bố của con số đó:

1. Điều kiện bổ nghĩa trực tiếp cho con số thì thuộc con số: cùng cụm, trong ngoặc ngay sau con số, hoặc "khi / ở / với / trong / dưới / cùng / kèm …" đi liền con số.
2. Điều kiện cụ thể ở vế nói tác dụng của chính con số thì thuộc con số ("… 2500 nit giúp nhìn rõ dưới nắng"). Nếu con số đã có điều kiện trực tiếp cùng loại thì điều kiện trực tiếp thắng.
3. Điều kiện hay từ khẳng định ở vế nói về tính năng hay việc khác thì không thuộc con số.
4. Câu nhắc một con số hai lần, một lần kèm điều kiện, một lần không, thì tách thành hai tuyên bố (gạch "Gộp tuyên bố trùng" ở trên).

**Rà tách trước khi gán.** Trước khi gán một bộ tuyên bố, người thực hiện rà từng tuyên bố với câu gốc theo bốn tiêu chí trên. Tuyên bố trái tiêu chí thì sửa, ghi `tach_sua=<sửa gì>` vào `ghi_chu` của tuyên bố. Người rà tự quyết từng chỗ, không nhờ AI gợi ý. Khi gán chỉ đọc tuyên bố (mục 1, bước 0).

| Câu trong quảng cáo | Tuyên bố sau khi tách | Ghi chú |
|---|---|---|
| "Galaxy Buds3 Pro cho bạn 6 giờ nghe nhạc khi bật chống ồn, tổng cộng 26 giờ cùng hộp sạc." | (1) Galaxy Buds3 Pro nghe nhạc 6 giờ khi bật chống ồn. (2) Galaxy Buds3 Pro nghe nhạc tổng 26 giờ kèm hộp sạc khi bật chống ồn. | Vế 2 mượn "nghe nhạc", "bật chống ồn" từ vế 1 |
| "Chỉ cần củ sạc 40W. iPhone 17 lấy lại 50% pin sau 20 phút." | iPhone 17 sạc 50% trong 20 phút với củ sạc 40W. | Điều kiện ở câu trước được đưa vào |
| "Apple Watch SE 3 có màn hình Luôn Bật sáng 1000 nit, kháng nước 50 m." | (1) Apple Watch SE 3 có độ sáng 1000 nit. (2) Apple Watch SE 3 chống nước 50 m. | "Luôn Bật" là tên tính năng, không phải tuyên bố |
| "Xiaomi 15T mỏng chỉ 7,5mm, pin 5500mAh trâu hơn đời trước." | Xiaomi 15T có pin 5500mAh. | Bỏ độ dày (ngoài phạm vi) và phần so với đời trước |
| "Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin." | Đồng hồ C dùng tới 40 giờ khi bật chế độ tiết kiệm pin. | Tiêu chí 1: "khi bật chế độ tiết kiệm pin" đi liền con số. Tách thành "Đồng hồ C dùng tới 40 giờ" là sót điều kiện |
| "Màn hình Điện thoại A sáng 2500 nit, giúp bạn nhìn rõ dưới nắng." | Điện thoại A sáng 2500 nit dưới nắng. | Tiêu chí 2: vế sau nói tác dụng của chính con số |
| "Tai nghe B luôn giữ kết nối ổn định, pin dùng 8 giờ suốt ngày dài." | Tai nghe B dùng 8 giờ. | Tiêu chí 3: "luôn" thuộc vế kết nối; "suốt ngày dài" là cụm khen |
| "Đồng hồ C: pin lên đến 30 giờ. Chỉ cần bật chế độ tiết kiệm pin là đạt 30 giờ." | (1) Đồng hồ C dùng lên đến 30 giờ. (2) Đồng hồ C dùng 30 giờ khi bật chế độ tiết kiệm pin. | Tiêu chí 4: một lần kèm điều kiện, một lần không |

## 3. Bốn nhãn

Định nghĩa chép nguyên văn đề cương:

| Nhãn | Mã | Định nghĩa |
|---|---|---|
| **Đúng** | `DUNG` | Tài liệu có thông số cùng sản phẩm, thuộc tính và điều kiện với tuyên bố, giá trị khớp và kiểu giá trị không bị đổi. |
| **Sai** | `SAI` | Tài liệu có thông số cùng sản phẩm và thuộc tính, nhưng giá trị của tuyên bố mâu thuẫn với giá trị công bố ở điều kiện của tuyên bố hoặc thuận lợi hơn mọi giá trị được công bố, đồng thời không trùng giá trị nào ở điều kiện khác. |
| **Lệch điều kiện** | `LECH` | Giá trị trong tuyên bố trùng giá trị được công bố ở một điều kiện khác với điều kiện mà tuyên bố nêu hoặc được hiểu thông thường (bỏ hoặc đổi chế độ, bộ phận, phụ kiện, phiên bản, điều kiện đo), hoặc tuyên bố biến mức tối đa "lên đến" thành mức chắc chắn đạt. |
| **Chưa đủ thông tin** | `CHUA_DU` | Kho tài liệu không có thông số cùng sản phẩm và thuộc tính, không công bố giá trị ở điều kiện mà tuyên bố nêu, hoặc ghi mâu thuẫn. |

**Chú thích cho vế cuối của định nghĩa Lệch** (không sửa nguyên văn đề cương): "biến mức tối đa 'lên đến' thành mức chắc chắn đạt" nghĩa là tuyên bố thêm một lời hứa mà tài liệu không có, bằng từ khẳng định gắn với con số (mục 6.2, dòng D2). Tuyên bố chỉ thiếu chữ "lên đến" thì không phải Lệch: "nghe nhạc 6 giờ" vẫn khớp "lên đến 6 giờ".

Hai khái niệm dùng chung:

- **Khớp giá trị:** bằng giá trị công bố sau chuẩn hóa, hoặc **kém thuận lợi hơn** giá trị đó (nêu thời lượng pin thấp hơn, thời gian sạc lâu hơn), vì không gây hiểu nhầm có lợi cho người bán. Hướng thuận lợi của từng thuộc tính ở mục 6.1; mã IP so theo mục 6.6. Chỉ so với con số hãng công bố, không so với số tự tính ra (mục 6.9).
- **Điều kiện của tuyên bố:** điều kiện nêu rõ (đọc theo mục 6.8); điều kiện bắt buộc nào không nêu thì lấy cách hiểu mặc định ở mục 5. Điều kiện xác định xong mới so con số, và giữ nguyên ở mọi dòng D.

## 4. Tài liệu nào là bằng chứng

**Được dùng:** `noi_dung` và `chu_thich` của các đoạn trong `data/nguon/<ma_mau>/doan.jsonl`, gồm cả trang chính (`url`) và trang bổ sung (`bo_sung`). Chú thích có giá trị như nội dung chính: bộ tiếp hợp 20W của Apple Watch SE 3 và "ANC được bật theo mặc định" của Galaxy Buds3 Pro chỉ nằm trong chú thích.

**Không dùng:**

- Menu, đường dẫn, đánh giá của người dùng.
- Cột của sản phẩm khác trong bảng so sánh. Đoạn `tn-samsung-buds3pro#041` và `#042` là bảng so sánh ba cột Buds3 Pro, Buds3, Buds FE; thứ tự cột ghi ở cuối đoạn `#039` ("Spec · Buds3 Pro · Buds3 · Buds FE"), trong `#041`, `#042` không có tên mẫu. Chỉ cột Buds3 Pro là bằng chứng.
- Hiểu biết riêng của người gán về sản phẩm, kết quả đo bên ngoài, trang của mẫu khác.

**Chú thích chỉ là ngữ cảnh**, không làm đổi nhãn: "phòng thí nghiệm", "thử nghiệm nội bộ", "thiết bị tiền sản xuất", "phần mềm tiền phát hành", "kết quả thực tế có thể khác", "phụ thuộc cấu hình mạng, cài đặt", "khả năng chống nước không phải vĩnh viễn", quy trình đo chuẩn ("thử với thiết bị cạn pin", "tính giờ từ khi logo Apple xuất hiện"), và kịch bản định nghĩa một hoạt động (300 lần xem giờ, 90 thông báo... của "sử dụng bình thường" trên Watch). Tiêu chí: điều kiện chỉ tham gia quyết định khi đổi điều kiện thì con số đổi và người mua không tự suy ra được.

**Ba trạng thái của một điều kiện:**

| Trạng thái | Khi nào | Xử lý |
|---|---|---|
| Không áp dụng | Có bằng chứng điều kiện không áp dụng cho trường hợp đang xét. Ví dụ trang Watch SE 3 có hai phiên bản và hai cỡ vỏ nhưng ghi chung một thời lượng pin | Không đòi điều kiện đó khớp. Không suy "không áp dụng" từ việc tài liệu im lặng |
| Không nêu | Quảng cáo không nói điều kiện | Dùng cách hiểu mặc định ở mục 5, ghi `mac_dinh` vào ghi chú (mục 8). Không nêu không có nghĩa tự động Lệch |
| Chưa xác định | Không đủ căn cứ xác định điều kiện | Chưa đủ thông tin (D1a), ghi nguyên nhân: `mac_dinh=<khóa không có mặc định>` hoặc `chua_xac_dinh=<cụm>` (mục 8) |

**Tài liệu mâu thuẫn hoặc ghi nhầm:** gán Chưa đủ thông tin ở D1b, đặt `tai_lieu_mau_thuan = true`. Người gán không tự sửa chỗ ghi nhầm của hãng, kể cả khi đoán được hãng định ghi gì (ví dụ V48).

## 5. Cách hiểu mặc định khi tuyên bố không nêu điều kiện

Nguyên tắc của đề cương: hiểu như người mua thông thường, **bộ phận chính, không mua thêm phụ kiện**. Cách hiểu mặc định **dùng ở mọi dòng D**, không chỉ ở D1a: điều kiện có cách hiểu mặc định thì coi như tuyên bố đã nêu điều kiện đó, rồi dò tiếp D1b → D6. Bảng dưới chép đúng `hieu_thong_thuong` trong 3 tệp cấu hình; cột cuối là khóa trong YAML để đối chiếu. Dòng có dấu * đã đối chiếu với khảo sát Bước 10 (mục 5.1).

| Nhóm | Thuộc tính | Điều kiện | Không nêu thì hiểu là | Khóa cấu hình |
|---|---|---|---|---|
| Điện thoại | Thời lượng pin (`thoi_luong_pin`) | Hoạt động* | Hoạt động kém thuận lợi nhất trong các hoạt động hãng công bố (iPhone 17: xem video trực tuyến, 27 giờ). "Xem video" không kèm "tải sẵn" hay "trực tuyến" cũng tính là chưa nêu hoạt động, trừ khi tuyên bố chép đúng nhãn của tài liệu (mục 6.8, luật chép đúng nhãn) | `hoat_dong: kem_thuan_loi_nhat` |
| | | Phiên bản | Phiên bản nêu trong tên sản phẩm | `phien_ban: nhu_hang_cong_bo` |
| Điện thoại | Sạc nhanh (`sac_nhanh`): thời gian sạc tới một mốc phần trăm | Bộ tiếp hợp | Không mua thêm: chỉ có đồ trong hộp. iPhone 17 và Xiaomi 15T chỉ kèm cáp, nên con số cần bộ sạc bán riêng không đạt | `bo_tiep_hop: khong_mua_them` |
| | | Cách sạc | Sạc bằng cáp | `cach_sac: cap` |
| | | Mốc phần trăm | Không có mặc định: không nêu thì D1a | `moc_phan_tram: khong_co_mac_dinh` |
| Điện thoại | Công suất sạc (`cong_suat_sac`) | Bộ tiếp hợp | Không mua thêm | `bo_tiep_hop: khong_mua_them` |
| | | Có dây hay không dây | Có dây | `cach_sac: cap` |
| Điện thoại | Độ sáng (`do_sang`) | Chế độ hiển thị* | Không có mặc định: không nêu chế độ thì D1a | `che_do_hien_thi: khong_co_mac_dinh` |
| | | Phần diện tích đo | Như hãng công bố cho chế độ đó | `dien_tich_do: nhu_hang_cong_bo` |
| Điện thoại | Tần số quét (`tan_so_quet`) | Tối đa hay thích ứng | Mức tối đa: "màn hình 120Hz" khớp "thích ứng lên đến 120Hz" | `kieu_tan_so: toi_da` |
| Điện thoại | Zoom (`zoom`) | Quang học hay kỹ thuật số | Quang học | `loai_zoom: quang_hoc` |
| | | Độ phóng đại hay phạm vi thu phóng | Độ phóng đại | `dai_luong: do_phong_dai` |
| | | Chụp ảnh hay quay video | Chụp ảnh | `che_do_camera: chup_anh` |
| Điện thoại | Kháng nước (`khang_nuoc`) | Độ sâu, thời gian ngâm, loại nước, hoạt động bị cấm | Như hãng công bố | `do_sau: nhu_hang_cong_bo`, `thoi_gian_ngam: nhu_hang_cong_bo`, `loai_nuoc: nhu_hang_cong_bo`, `hoat_dong_bi_cam: nhu_hang_cong_bo` |
| Điện thoại | Dung lượng pin (`dung_luong_pin`) | Điển hình hay định mức | Điển hình | `kieu_dung_luong: dien_hinh` |
| | | Phiên bản | Phiên bản nêu trong tên sản phẩm | `phien_ban: nhu_hang_cong_bo` |
| Tai nghe | Thời lượng pin (`thoi_luong_pin`) | Chống ồn* | Bật. Samsung ghi "ANC được bật theo mặc định" (`tn-samsung-buds3pro#020`) | `che_do_chong_on: bat` |
| | | Bộ phận | Chỉ tai nghe, không tính hộp sạc | `bo_phan: tai_nghe` |
| | | Hoạt động* | Nghe nhạc | `hoat_dong: nghe_nhac` |
| Tai nghe | Sạc nhanh (`sac_nhanh`): số giờ nghe sau một số phút sạc | Số phút sạc | Không có mặc định | `so_phut_sac: khong_co_mac_dinh` |
| | | Bộ phận | Tai nghe | `bo_phan: tai_nghe` |
| Tai nghe | Kháng nước (`khang_nuoc`) | Bộ phận | Tai nghe | `bo_phan: tai_nghe` |
| | | Độ sâu, thời gian ngâm, loại nước, hoạt động bị cấm | Như hãng công bố | `do_sau: nhu_hang_cong_bo`, `thoi_gian_ngam: nhu_hang_cong_bo`, `loai_nuoc: nhu_hang_cong_bo`, `hoat_dong_bi_cam: nhu_hang_cong_bo` |
| Tai nghe | Dung lượng pin (`dung_luong_pin`) | Bộ phận | Tai nghe | `bo_phan: tai_nghe` |
| Đồng hồ | Thời lượng pin (`thoi_luong_pin`) | Chế độ nguồn* | Chế độ thường | `che_do_nguon: thuong` |
| | | Hoạt động* | Sử dụng bình thường | `hoat_dong: su_dung_binh_thuong` |
| | | Phiên bản | Phiên bản nêu trong tên; trang không tách giá trị theo phiên bản thì không áp dụng | `phien_ban: nhu_hang_cong_bo` |
| Đồng hồ | Sạc nhanh (`sac_nhanh`): dạng 1 là thời gian tới mốc phần trăm, dạng 2 là số giờ dùng sau một số phút sạc | Bộ tiếp hợp | Không mua thêm. Bộ 20W của Watch SE 3 chỉ ghi trong chú thích và không có trong hộp | `bo_tiep_hop: khong_mua_them` |
| | | Cáp sạc | Cáp đi kèm | `cap_sac: cap_di_kem` |
| | | Mốc phần trăm (dạng 1) | Không có mặc định | `moc_phan_tram: khong_co_mac_dinh` |
| | | Số phút sạc (dạng 2) | Không có mặc định | `so_phut_sac: khong_co_mac_dinh` |
| | | Hoạt động sau khi sạc (dạng 2) | Sử dụng bình thường | `hoat_dong: su_dung_binh_thuong` |
| Đồng hồ | Kháng nước (`khang_nuoc`) | Chuẩn và độ sâu | Như hãng công bố | `chuan_do_sau: nhu_hang_cong_bo` |
| | | Hoạt động được phép | Như hãng công bố; quảng cáo gợi ý hoạt động bị cấm là đổi điều kiện | `hoat_dong_cho_phep: nhu_hang_cong_bo` |
| Đồng hồ | Độ sáng (`do_sang`) | Chế độ hiển thị | Chế độ thông thường; tài liệu chỉ có một con số không kèm điều kiện thì so thẳng (mục 6.4) | `che_do_hien_thi: thong_thuong` |

Các ý của bảng hay bị hiểu nhầm:

- **Không chọn điều kiện theo con số.** Cách hiểu mặc định không phụ thuộc vào độ lớn con số của tuyên bố. Con số không khớp ở điều kiện mặc định thì dò tiếp D4–D6, không đổi sang điều kiện mà con số khớp (V24, V32).
- **Mặc định không bao giờ là lý do dừng ở D1a.** Điều kiện có cách hiểu mặc định là đã biết; chỉ điều kiện ghi "Không có mặc định" mới dẫn tới D1a khi tuyên bố không nêu (mục 7).
- **Tuyên bố chép đúng nhãn của tài liệu thì xét luật chép đúng nhãn trước bảng này** (mục 6.8). Ví dụ: Apple ghi "Thời gian xem video: Lên đến 30 giờ"; tuyên bố "xem video 30 giờ" chép đúng nhãn đó, nên cùng điều kiện (V03). Chép thiếu chữ điều kiện của nhãn, hoặc không trùng chữ nhãn nào, thì vẫn theo bảng: "pin dùng 30 giờ" là chưa nêu hoạt động (V24).
- **"Kém thuận lợi nhất"** chỉ dùng cho hoạt động của điện thoại: tuyên bố không nêu hoạt động phải đúng ở hoạt động kém nhất hãng công bố. Tai nghe và đồng hồ có mặc định riêng (nghe nhạc, chống ồn bật; sử dụng bình thường, chế độ thường).
- **"Không mua thêm"** nghĩa là chỉ có đồ trong hộp, và chỉ dùng khi tuyên bố không nêu phụ kiện. Con số cần bộ sạc bán riêng mà tuyên bố không nêu bộ sạc thì Lệch, dù tuyên bố chép đúng con số (V21, V23, V34). Tuyên bố nêu bộ sạc hay công suất bộ sạc thì so theo mục 6.3 (V01, V22); tuyên bố không cần nói phụ kiện "được bán riêng".
- **"Không có mặc định"** nghĩa là tuyên bố phải tự nêu điều kiện đó. Không nêu thì người gán cũng không đoán, gán Chưa đủ thông tin ở D1a (V46; độ sáng điện thoại: V25).

### 5.1 Đối chiếu với khảo sát Bước 10

Khảo sát 10 người ngày 27–28/10/2026 (`ket_qua/khao_sat_cach_hieu.md`; 8 người học hoặc làm công nghệ thông tin). Quy tắc đặt trước: quá nửa người đọc hiểu khác cấu hình thì sửa.

| Cách hiểu trong bảng trên | Hiểu khác | Quyết định |
|---|---|---|
| Điện thoại, hoạt động: kém thuận lợi nhất | 1/10 | Giữ |
| "Xem video" là xem video tải sẵn (cách diễn đạt) | 9/10 | **Sửa**: coi như chưa nêu hoạt động. Từ 02/11 (QĐ15), tuyên bố chép đúng nhãn "Thời gian xem video" của tài liệu thì theo luật chép đúng nhãn (V03); cách hiểu của người đọc ghi là giới hạn, tính lại ở Bước 37 |
| Điện thoại, chế độ hiển thị: tiêu chuẩn | 7/10, không cách hiểu nào quá nửa | **Sửa**: không có mặc định (V25, V26, V43) |
| Điện thoại, zoom: quang học | 6/10 | Giữ, lệch khỏi quy tắc đặt trước (lý do ở `khao_sat_cach_hieu.md` mục 8); tính lại ở Bước 37 |
| Điện thoại và đồng hồ, bộ sạc: không mua thêm | 5/10 và 4/10 | Giữ |
| Tai nghe: nghe nhạc; chống ồn bật; chỉ tai nghe | 4/10; 4/10 (cả khi đàm thoại); 4/10 | Giữ. 4/10 người tính cả hộp sạc: ghi vào giới hạn |
| Đồng hồ: sử dụng bình thường | 1/10 | Giữ |
| Đồng hồ, chế độ nguồn: thường | 6/10 với "18 giờ", 4/10 với "32 giờ" | Giữ, lệch khỏi quy tắc đặt trước; tính lại ở Bước 37 |
| Bỏ "lên đến" vẫn khớp (mục 6.2) | 1/10 hiểu câu không có "lên đến" chắc chắn hơn | Giữ |

## 6. Các quy tắc so sánh

### 6.1 Hướng thuận lợi và kiểu giá trị mặc định

| Nhóm | Thuộc tính | Đơn vị | Hướng thuận lợi | Kiểu giá trị mặc định |
|---|---|---|---|---|
| Điện thoại | `thoi_luong_pin` | giờ | Cao hơn tốt hơn (`cao_hon_tot_hon`) | Tối đa như hãng công bố (`toi_da`) |
| Điện thoại | `sac_nhanh` | phút | Thấp hơn tốt hơn (`thap_hon_tot_hon`) | `toi_da` |
| Điện thoại | `cong_suat_sac` | W | `cao_hon_tot_hon` | `toi_da` |
| Điện thoại | `do_sang` | nit | `cao_hon_tot_hon` | `toi_da` |
| Điện thoại | `tan_so_quet` | Hz | `cao_hon_tot_hon` | `toi_da` |
| Điện thoại | `zoom` | x | `cao_hon_tot_hon` | `toi_da` |
| Điện thoại | `khang_nuoc` | mã IP | Theo nhánh IP, mục 6.6 (`theo_nhanh_ip`) | Như hãng công bố (`nhu_hang_cong_bo`) |
| Điện thoại | `dung_luong_pin` | mAh | `cao_hon_tot_hon` | Điển hình (`dien_hinh`) |
| Tai nghe | `thoi_luong_pin` | giờ | `cao_hon_tot_hon` | `toi_da` |
| Tai nghe | `sac_nhanh` | giờ nghe được | `cao_hon_tot_hon` | `toi_da` |
| Tai nghe | `khang_nuoc` | mã IP | `theo_nhanh_ip` | `nhu_hang_cong_bo` |
| Tai nghe | `dung_luong_pin` | mAh | `cao_hon_tot_hon` | `dien_hinh` |
| Đồng hồ | `thoi_luong_pin` | giờ | `cao_hon_tot_hon` | `toi_da` |
| Đồng hồ | `sac_nhanh` | phút (dạng 1), giờ (dạng 2) | Dạng 1 thấp hơn tốt hơn, dạng 2 cao hơn tốt hơn (`theo_dang`) | `toi_da` |
| Đồng hồ | `khang_nuoc` | m (ISO 22810) | `cao_hon_tot_hon` | `nhu_hang_cong_bo` |
| Đồng hồ | `do_sang` | nit | `cao_hon_tot_hon` | `toi_da` |

**Bằng nhau** sau chuẩn hóa, trong ngưỡng làm tròn 1% (chọn lại ở Bước 33). Chuẩn hóa: giờ = tiếng = h; phút = min; nit = nits = cd/m²; "3.000", "3.200" là 3000, 3200 (chấm ngăn hàng nghìn khi theo sau đúng 3 chữ số); "4.5" của Samsung là 4,5 (chấm thập phân khi theo sau 1–2 chữ số); dấu phẩy luôn là thập phân ("13,19 giờ").

### 6.2 Kiểu giá trị và chữ "lên đến"

- **Cụm chỉ kiểu giá trị:** tối đa ("lên đến", "tối đa", "đến", "up to", "tới"); điển hình ("typ", "typical", "điển hình"; riêng dung lượng pin, "thông thường" cũng là điển hình); định mức ("định mức", "rated"); thích ứng ("thích ứng").
- **Tuyên bố không ghi kiểu** thì lấy kiểu mặc định ở mục 6.1, tức kiểu hãng công bố.
- **Bỏ "lên đến" vẫn khớp.** "Nghe nhạc 6 giờ" khớp "lên đến 6 giờ". Lý do ghi thêm `(quảng cáo bỏ "lên đến")` nhưng không đổi nhãn. Căn cứ: báo cáo gốc FTC 2012 cho thấy quảng cáo "up to 47%" và "47%" không khác nhau có ý nghĩa thống kê về cách người đọc hiểu; đề tài so quảng cáo với tài liệu, không đo hiệu năng thực tế. Tuyên bố không có từ khẳng định thì không bao giờ dừng ở D2.
- **Từ khẳng định** cho một mức không cao hơn mức "lên đến" ở cùng điều kiện thì Lệch ở D2. Các từ này hứa một mức sàn mà tài liệu không hứa. Mức khẳng định cao hơn mức "lên đến" thì bỏ qua D2, xét tiếp D3–D6. Có hai nhóm:
  - Nhóm chắc chắn: "luôn", "đảm bảo", "bảo đảm", "ít nhất", "mọi lúc".
  - Nhóm mức sàn: "hơn <số>", "trên <số>", "không dưới <số>", "<số> trở lên". Chỉ tính khi cụm đứng liền con số của giá trị tuyên bố. "Hơn 16 giờ" hứa như "ít nhất 16 giờ" (V50). Cụm đi với con số của điều kiện ("với bộ sạc 40W trở lên") là điều kiện dạng số (mục 6.3), không phải từ khẳng định (V01). "Trên tai nghe", "trên 25% diện tích" không đứng liền con số của giá trị nên không tính.
- **Từ khẳng định phải gắn với con số của tuyên bố**: bổ nghĩa cho con số, hoặc cho động từ có con số ("luôn đạt 120Hz", "đảm bảo 6 giờ", "ít nhất 18 giờ"). Từ ở vế khác của câu, nói về việc khác (kết nối, thông tin, sự đồng hành), không tính. Ví dụ tự đặt: "Tai nghe B đảm bảo kết nối ổn định, nghe nhạc 8 giờ" không có từ khẳng định gắn với 8 giờ.
  - Tên tính năng không tính: "Màn hình Luôn Bật", "Luôn kết nối" (V40).
  - Bỏ qua dạng phủ định: "không đảm bảo", "không được đảm bảo", "không bảo đảm", "không phải lúc nào", "không luôn".
  - "Tối thiểu" chưa tính là từ khẳng định, vì trùng "độ sáng tối thiểu".
  - Dừng ở D2 thì ghi từ đó vào ghi chú: `khang_dinh=<từ>` (mục 8).
- **"Tối đa" của điều kiện đo** ("độ sâu tối đa 6 mét", "tối đa 30 phút") là giới hạn của bài thử, so theo mục 6.3. Đây không phải mức "lên đến" của giá trị. Tuyên bố nêu đúng giới hạn đó không phải D2. Ví dụ tự đặt: tài liệu Điện thoại A ghi "IP68, độ sâu tối đa 4 mét trong tối đa 30 phút"; tuyên bố "chống nước IP68 ở độ sâu 4 mét trong 30 phút" là cùng điều kiện, xét ở D3.
- **Cụm khen không có con số** ("cả ngày", "suốt ngày dài", "không lo hết pin", "siêu bền", "bền bỉ", "vượt trội", "tuyệt đối", "trọn vẹn", "không giới hạn") không phải từ khẳng định, cũng không phải điều kiện. Bỏ qua khi gán.
- **Cụm phủ nhiều giá trị** ("mọi điều kiện ánh sáng", "dù A hay B", "cho cả A và B") không phải từ khẳng định; đọc theo mục 6.8.
- **Tuyên bố ghi rõ một kiểu khác tài liệu** (ví dụ "định mức" cho con số điển hình) thì kiểu giá trị bị đổi: không thể Đúng ở D3, và được xét như khác điều kiện ở D4 (V37).

**Từ hay gặp mà không phải từ khẳng định** (bổ sung ở Bước 16):

| Từ, cụm | Xử lý | Ở đâu |
|---|---|---|
| "mọi điều kiện ánh sáng", "mọi chế độ", "mọi hoạt động", "dù A hay B", "cho cả A và B" | Cụm phủ nhiều giá trị | Mục 6.8 |
| "liên tục", "sử dụng liên tục", "dùng liên tục" | Tả cách đo, không hứa mức sàn; coi như chưa nêu hoạt động | Mục 6.8, ý 3 |
| "cả ngày", "suốt (cả) ngày (dài)", "không lo hết pin", "không lo ngắt quãng" | Cụm khen, bỏ qua | Mục 2, mục 6.2 |
| "tuyệt đối", "trọn vẹn", "không giới hạn", "siêu bền", "bền bỉ", "vượt trội" | Cụm khen, bỏ qua | Mục 2, mục 6.2 |
| "chỉ", "chỉ cần", "chỉ trong" | Nhấn độ nhanh, không hứa mức sàn; bỏ qua (V21, V46) | Mục 6.2 |
| "ngay cả" | Mở đầu một điều kiện, không phải lời hứa về mức; đọc điều kiện theo mục 6.8 | Mục 6.8 |
| "tối đa" | Kiểu giá trị tối đa, hoặc chữ chỉ chế độ độ sáng của Apple | Mục 6.2, 6.5 |
| "đảm bảo", "luôn", "mọi lúc" ở vế nói việc khác | Không gắn với con số, không tính | Mục 6.2 |

### 6.3 Điều kiện dạng số

Điều kiện là một con số kèm quan hệ thì so bằng số sau khi chuẩn hóa đơn vị. Thỏa quan hệ là cùng điều kiện; không thỏa là khác điều kiện, xét tiếp D4–D6.

| Điều kiện | Đơn vị | Tài liệu ghi | Cùng điều kiện khi | Ví dụ |
|---|---|---|---|---|
| Công suất bộ tiếp hợp (`bo_tiep_hop`) | W | Mức tối thiểu ("40W trở lên", "67W hoặc cao hơn", bộ 20W của Watch) | Tuyên bố ≥ tài liệu | V02 (60W), V22 (20W) |
| Mốc phần trăm (`moc_phan_tram`) | % | Mốc đo ("50%", "100%", "80%") | Tuyên bố ≤ tài liệu | "sạc 30% trong 20 phút" vẫn khớp mốc 50% |
| Số phút sạc (`so_phut_sac`) | phút | Thời gian sạc trước khi dùng ("sạc 15 phút") | Tuyên bố ≥ tài liệu | Watch SE 3 "sạc 10 phút dùng 8 giờ": 10 < 15, khác điều kiện |
| Độ sâu ngâm (`do_sau`) | m | Mức tối đa ("độ sâu tối đa 6 mét", "1 mét") | Tuyên bố ≤ tài liệu | V06 (4 m), V29 (10 m) |
| Thời gian ngâm (`thoi_gian_ngam`) | phút | Mức tối đa ("tối đa 30 phút") | Tuyên bố ≤ tài liệu | "ngâm 1 giờ" là khác điều kiện |
| Phần diện tích đo (`dien_tich_do`) | % | Phần màn hình được đo ("25% diện tích") | Tuyên bố ≤ tài liệu | V27 (toàn màn hình) |

"Sạc đầy" hiểu là mốc 100%. Chữ "tối đa" của độ sâu, thời gian ngâm là giới hạn bài thử, không phải kiểu giá trị (mục 6.2). Trong tuyên bố về thời gian sạc, con số W đi cùng cách sạc hay cổng sạc là công suất bộ tiếp hợp, so theo bảng trên (mục 6.8, ý 5). Con số của các điều kiện này không phải giá trị của thuộc tính (mục 6.9).

### 6.4 Chọn con số để so khi tuyên bố không nêu điều kiện

| Tài liệu của mẫu | Cách so | Ví dụ |
|---|---|---|
| Chỉ một con số cho thuộc tính (cùng bộ phận), không kèm cụm điều kiện nào trong toàn bộ tài liệu | So thẳng; lý do ghi "tài liệu không nêu điều kiện" | V12, Watch SE 3 "Độ sáng đỉnh 1000 nit" |
| Nhiều con số, mỗi số ghi rõ điều kiện; hoặc một con số kèm điều kiện | So với con số ứng với cách hiểu mặc định | V32, V24 |
| Không xác định được điều kiện của tuyên bố: khóa "Không có mặc định", chữ trỏ nhiều chế độ, hoặc cụm không giải được (ba lối vào D1a, mục 7). Con số không khớp ở điều kiện đã xác định không phải lý do D1a | Chưa đủ thông tin (D1a) | V47, V25, V26 |
| Con số kèm điều kiện mà cấu hình chưa biết | Người gán xử lý theo mục 6.7; hệ thống ra D1a | V08 |

### 6.5 Độ sáng: chữ "tối đa", "đỉnh", "cực đại"

- Chữ dùng để **phân biệt từ hai giá trị trở lên** là chế độ hiển thị, đọc theo cách gọi của hãng:
  - Apple (iPhone 17): "tối đa" là chế độ tiêu chuẩn; "đỉnh" là HDR hoặc ngoài trời. Tuyên bố iPhone chỉ ghi "đỉnh" mà không nói chế độ thì D1a (V47).
  - Xiaomi: "cực đại" là chế độ tự tăng sáng dưới ánh sáng mạnh, đo trên 25% diện tích. Trang Xiaomi 15T chỉ có một con số độ sáng, nên "cực đại" ở đây là kiểu giá trị tối đa; tuyên bố "độ sáng cực đại 3200 nit" vì vậy không nêu chế độ (V43, mục 11.1).
- **Tuyên bố không nêu chế độ** (không có chữ nào ở trên, hoặc chữ chỉ là kiểu giá trị): độ sáng điện thoại không có cách hiểu mặc định (khảo sát Bước 10), nên D1a (V25, V26, V43). Riêng tài liệu chỉ có một con số không kèm điều kiện thì vẫn so thẳng (mục 6.4, V12).
- Chữ **gắn với một giá trị duy nhất** là kiểu giá trị tối đa, không phải chế độ, áp cho mọi hãng (Watch SE 3 "Độ sáng đỉnh 1000 nit", V12).
- **Tuyên bố có cả chữ chỉ chế độ rõ** ("ngoài trời", "HDR", "dưới nắng") **và chữ mức cao** ("tối đa", "đỉnh", "cực đại"): chữ chỉ chế độ quyết định; chữ mức cao là kiểu giá trị tối đa. Ví dụ tự đặt: hãng của Điện thoại A gọi "tối đa" là chế độ tiêu chuẩn; tuyên bố "Điện thoại A có độ sáng tối đa 1800 nit khi xem HDR" nêu chế độ HDR, chữ "tối đa" ở đây không trỏ về chế độ tiêu chuẩn.
- "Độ sáng tối thiểu" là đại lượng khác, ngoài phạm vi.

### 6.6 Kháng nước: mã IP và ISO 22810

- **Mã IP** so theo nhánh của IEC 60529: chữ số bụi 0–6 xếp thành thang, cao hơn tốt hơn; chữ số nước tách hai nhánh 0–6 (tia nước) và 7–8 (ngâm), 8 khắc nghiệt hơn 7, chỉ so trong cùng nhánh; khác nhánh thì không khớp. Chữ "X" (IPX7) nghĩa là không công bố chữ số bụi, không xét. Ví dụ với máy IP68: tuyên bố IP67 khớp (cùng nhánh ngâm, kém thuận lợi hơn); với máy IP57: tuyên bố IP58 thuận lợi hơn nên Sai.
- **Mã khác nhánh** không khớp ở D3. Mã IP là giá trị, không phải điều kiện; điều kiện thử không nêu thì hiểu như hãng công bố, nên tuyên bố và tài liệu cùng điều kiện. Mã đó trùng mã của bộ phận hay điều kiện khác thì D4. Không trùng mã nào thì D5 Sai, loại `doi_gia_tri`. Ví dụ tự đặt: máy công bố IP68, tuyên bố IPX5: khác nhánh, không trùng mã nào, D5. Không dùng hiểu biết ngoài tài liệu kiểu "máy chống ngâm thì cũng chịu được tia nước".
- **Đồng hồ theo ISO 22810:** quy về mét (5ATM = WR50 = 50 m; 10ATM = 100 m), cao hơn tốt hơn.
- **Điều kiện thử** (độ sâu, thời gian, loại nước) không nêu thì hiểu như hãng công bố. Quảng cáo nêu nước biển, nước clo, hồ bơi khi hãng chỉ thử nước ngọt, hoặc gợi ý hoạt động hãng khuyến cáo không dùng (lặn với bình dưỡng khí, tắm biển), là đổi điều kiện.
- **"Mọi hoạt động"** gắn với mã kháng nước là cụm phủ (mục 6.8): phủ cả hoạt động hãng khuyến cáo không dùng. Tài liệu chỉ công bố mức kháng nước cho các hoạt động được phép, nên mã đó trùng giá trị ở điều kiện khác: Lệch ở D4, loại `doi_dieu_kien`. Ví dụ tự đặt: Đồng hồ C chống nước 50 m, hãng khuyến cáo không lặn với bình dưỡng khí; tuyên bố "Đồng hồ C chống nước 50 m cho mọi hoạt động dưới nước" ra Lệch, như V30.
- **Bộ phận:** hộp sạc Galaxy Buds3 Pro không kháng nước. Tuyên bố gán mã IP57 cho hộp sạc trùng giá trị của tai nghe nên Lệch ở D4 (V35); tuyên bố chỉ nói "hộp sạc kháng nước" không trùng mã nào nên Sai ở D5 (V18).

### 6.7 Điều kiện ngoài cấu hình

Nhãn chuẩn **không** theo giới hạn của cấu hình. Nhãn chuẩn theo tài liệu và cách người mua hiểu; giới hạn của hệ thống P ghi riêng. Gặp cụm điều kiện mà mục 5 và phụ lục cụm (mục 13) không có, ở tuyên bố hay ở tài liệu, người gán làm như sau:

1. Cụm ở tuyên bố: đọc theo mục 6.8 trước. Cụm tả đúng một điều kiện tài liệu công bố, bằng tên hãng dùng hoặc bằng hoàn cảnh của điều kiện ấy, thì là nêu điều kiện đó (mục 6.8, ý 2). Cụm chỉ sự liên tục hay mức dùng chung thì coi như chưa nêu (mục 6.8, ý 3).
2. Cụm ở tài liệu, hoặc cụm ở tuyên bố mà mục 6.8 chưa xếp được: đọc tài liệu, kể cả chú thích, để biết điều kiện đó nghĩa là gì; xếp vào một trong sáu loại (chế độ hoạt động, bộ phận, phụ kiện, điều kiện đo, phiên bản, kiểu giá trị). Không xếp được thì ghi `ngoai_sau_loai=<cụm>`.
3. Quyết định điều kiện đó tham gia quyết định nhãn hay chỉ là ngữ cảnh, theo tiêu chí ở mục 4. Chỉ là ngữ cảnh thì bỏ qua.
4. Điều kiện quyết định mà tuyên bố không nêu: dùng nguyên tắc chung. Bộ phận chính; không mua thêm phụ kiện; điều kiện đo, điều kiện thử như hãng công bố; chế độ mặc định của máy nếu hãng ghi; chế độ người dùng tự chọn mà hãng không ghi mặc định thì lấy chế độ kém thuận lợi nhất (chưa khảo sát người đọc; nhãn dựa vào ý này ghi `mac_dinh=ngoai_bang`, mục 8). Nguyên tắc vẫn không chỉ ra được cách hiểu thì D1a, ghi rõ vì sao.
5. Gán nhãn theo D1–D6 như bình thường, ghi `ngoai_cau_hinh=<cụm>` vào ghi chú. Các ca này được thống kê riêng ở Bước 37–38: hệ thống thường ra D1a ở đây, và chỗ lệch giữa đầu ra với nhãn chuẩn là giới hạn bao phủ của cấu hình, không phải lý do sửa nhãn chuẩn.
6. Vẫn không xếp được điều kiện của tuyên bố thì D1a, ghi `chua_xac_dinh=<cụm>`.

Quy tắc 4 cho chế độ người dùng tự chọn chưa qua khảo sát người đọc (khảo sát Bước 10 chỉ xác nhận "kém thuận lợi nhất" cho hoạt động của điện thoại, mục 5.1). Người thực hiện duyệt giữ quy tắc này ngày 02/11/2026 (QĐ10), với điều kiện nhãn dựa vào quy tắc ghi `mac_dinh=ngoai_bang`, để phân tích độ nhạy ở Bước 37 tính lại các nhãn đó như Chưa đủ thông tin. Hệ thống có luật tương ứng (`luat_chung_cho_nhieu_gia_tri` trong `chung.yaml`) nhưng đang tắt, chọn bật hay tắt ở Bước 33.

### 6.8 Đọc cụm điều kiện trong tuyên bố

Đọc theo nghĩa với người mua, rồi đối chiếu với điều kiện tài liệu mô tả. Không đòi tuyên bố dùng đúng chữ của hãng.

**Luật chép đúng nhãn của tài liệu** (QĐ15, 02/11/2026). Xét **trước** cách hiểu mặc định (mục 5) và trước các ý 1–7 dưới đây. Áp khi đủ cả ba điều kiện:

- Tuyên bố gọi điều kiện **bằng đúng cụm chữ** mà tài liệu dùng làm nhãn cho một dòng thông số của cùng sản phẩm và thuộc tính. Nhãn gồm chữ của dòng, chữ trong ngoặc và chú thích gắn với dòng đó.
- Tuyên bố **không thiếu chữ điều kiện nào** của nhãn. Chữ điều kiện là chữ chỉ chế độ, bộ phận, phụ kiện, cách đo, phiên bản ("tổng", "trực tuyến", "tắt ANC", "kèm hộp sạc"…). Động từ chung ("xem", "dùng") và chữ thừa không phải điều kiện ("liên tục") không tính.
- **Khớp bằng chữ, không bằng con số:** tìm dòng có nhãn trùng chữ trước rồi mới so số. Không chọn một dòng vì số của dòng đó trùng số của tuyên bố (mục 5, "Không chọn điều kiện theo con số").

Đủ ba điều kiện thì điều kiện của tuyên bố là điều kiện của dòng đó; dò D3–D5 như thường (bằng hoặc kém thuận lợi hơn: Đúng; thuận lợi hơn: Sai). Ghi `chep_nhan=<cụm>` vào ghi chú; không ghi `mac_dinh` cho điều kiện đã khớp theo nhãn. Thiếu một điều kiện thì không áp, dùng cách hiểu mặc định như cũ.

Lý do: đề tài so quảng cáo với tài liệu; dòng tài liệu không kèm điều kiện nào thì quảng cáo chép đúng dòng đó không thiếu điều kiện so với tài liệu. Hướng dẫn không tự gán thêm nghĩa cho nhãn của hãng (ví dụ không coi "Thời gian xem video" là "xem video ngoại tuyến" khi tài liệu không ghi chữ đó). Giới hạn: khảo sát Bước 10 (Q09) có 9/10 người hiểu "xem video" là xem cả trực tuyến; các nhãn có `chep_nhan` được tính lại theo cách hiểu của người đọc ở Bước 37.

Ví dụ tự đặt: tài liệu Điện thoại A ghi "Thời gian xem video: lên đến 22 giờ" và "Thời gian xem video (trực tuyến): lên đến 19 giờ". "Điện thoại A xem video 22 giờ": trùng nhãn, D3 Đúng. "… xem video 20 giờ": D3 Đúng (kém thuận lợi hơn). "… xem video 25 giờ": D5 Sai. "Pin Điện thoại A dùng 22 giờ": không trùng chữ nhãn nào, dùng mặc định (hoạt động kém thuận lợi nhất, 19 giờ), 22 là số của dòng khác, D4 Lệch. Tài liệu Tai nghe B ghi "Tổng thời gian phát nhạc (tắt ANC): 30 giờ"; tuyên bố "Tai nghe B nghe nhạc 30 giờ" thiếu "tổng" và "tắt ANC", nên không áp luật này.

1. **Cụm có trong phụ lục** (mục 13, chép từ cấu hình) thì là điều kiện đó. Cụm phụ lục ứng với cách gọi chế độ trong cấu hình; tài liệu gọi điều kiện bằng tên khác (Xiaomi gọi chế độ sáng cao là tự tăng sáng "Dưới ánh sáng mạnh", không phải "ngoài trời") thì đọc theo ý 2 với chính chữ của tài liệu đó (V51). Giá trị phụ lục ghi "(chỉ `<thuộc tính>`)" chỉ dùng cho thuộc tính đó.
2. **Cụm chưa có trong phụ lục:** nếu cụm tả đúng một điều kiện tài liệu công bố, bằng tên hãng dùng hoặc bằng hoàn cảnh của điều kiện ấy, thì là nêu điều kiện đó. Ví dụ: "dưới trời nắng", "trong ánh sáng mạnh" tả hoàn cảnh của chế độ sáng cao ngoài trời ("ánh nắng", "dưới ánh nắng" đã có trong phụ lục). Ghi `ngoai_cau_hinh=<cụm>`. Cụm chung chung, không trỏ được tới một điều kiện tài liệu công bố, thì coi như chưa nêu. Ví dụ tự đặt: tài liệu Điện thoại A ghi "độ sáng tối đa 900 nit (tiêu chuẩn); độ sáng đỉnh 2500 nit (ngoài trời)"; tuyên bố "Điện thoại A sáng 2500 nit khi đi dưới trời nắng" nêu chế độ ngoài trời, nên D3 Đúng. Ví dụ thật: V51.
3. **Cụm chỉ sự liên tục hay mức dùng chung** ("liên tục", "sử dụng liên tục", "dùng liên tục"; "sử dụng", "dùng" đứng riêng như "tổng thời lượng sử dụng", "dùng được 20 giờ") không nêu hoạt động cụ thể, ở mọi nhóm. Coi như chưa nêu hoạt động, dùng cách hiểu mặc định ở mục 5. Ở phía tài liệu, "Sử dụng liên tục" của Xiaomi 15T là tên bài đo (V07). Ví dụ tự đặt: tài liệu Điện thoại A ghi "xem video lên đến 22 giờ; xem video trực tuyến lên đến 19 giờ"; tuyên bố "pin dùng liên tục 18 giờ" chưa nêu hoạt động, so với 19 giờ, D3 Đúng.
4. **Chữ chỉ chế độ rõ cùng chữ mức cao:** chữ chỉ chế độ quyết định; chữ mức cao là kiểu giá trị tối đa (mục 6.5).
5. **Con số W trong tuyên bố về thời gian sạc:** W đi cùng cách sạc hay cổng sạc ("sạc qua cổng X 45W", "với 45W") là công suất nguồn sạc, tức điều kiện bộ tiếp hợp, so theo mục 6.3. Trong tuyên bố về công suất sạc thì con số W là giá trị. Ví dụ tự đặt: tài liệu Điện thoại A ghi "sạc 50% trong 25 phút với bộ sạc 67W trở lên"; tuyên bố "sạc 50% trong 25 phút khi cắm sạc 65W" nêu bộ tiếp hợp 65W, thấp hơn 67W, nên khác điều kiện: D4 Lệch, `doi_dieu_kien`, như V22.
6. **Bộ phận của thời lượng pin tai nghe:** "tổng", "tổng cộng", "kèm / cùng / kết hợp hộp sạc" là kèm hộp sạc. "Hộp sạc" đứng riêng làm chủ ngữ ("hộp sạc cho thêm …") là bộ phận hộp sạc (mục 6.9). Ý này chỉ cho thời lượng pin: với dung lượng pin hay kháng nước, "kèm hộp sạc" chỉ nói sản phẩm có hộp sạc, không phải bộ phận "tổng kèm hộp sạc" (phụ lục ghi `kem_hop_sac` "(chỉ `thoi_luong_pin`)").
7. **Vẫn không xếp được** thì D1a, ghi `chua_xac_dinh=<cụm>` (mục 6.7).

**Cụm phủ nhiều giá trị.** Cụm "mọi điều kiện X", "mọi chế độ", "bất kể X", "dù A hay B", "cho cả A và B", "mọi hoạt động" gắn với con số nghĩa là tuyên bố phải đúng ở từng giá trị được phủ.

- Điều kiện của tuyên bố là giá trị kém thuận lợi nhất trong các giá trị được phủ mà tài liệu công bố. Đây là điều kiện nêu rõ, nên Lệch thì loại `doi_dieu_kien`.
- Cụm phủ không phải từ khẳng định, trừ khi tuyên bố có thêm từ khẳng định gắn với con số (mục 6.2).
- Kháng nước: "mọi hoạt động" phủ cả hoạt động hãng khuyến cáo không dùng (mục 6.6).
- Điều kiện trực tiếp thắng (QĐ11): tuyên bố đã có điều kiện cùng loại gắn trực tiếp với con số (cùng cụm, trong ngoặc ngay sau con số, hoặc "khi / ở / với / trong / dưới …" đi liền con số), còn cụm phủ nằm ở vế nói tác dụng của con số ("… giúp nhìn rõ dưới mọi điều kiện ánh sáng"), thì điều kiện của tuyên bố là điều kiện trực tiếp; cụm phủ không đổi điều kiện. Như tiêu chí tách 2 ở mục 2. Cụm phủ gắn trực tiếp với con số và tuyên bố không có điều kiện trực tiếp cùng loại thì áp các ý trên.
- Ví dụ tự đặt: tài liệu Tai nghe B ghi "nghe nhạc lên đến 9 giờ; đàm thoại lên đến 6 giờ"; tuyên bố "Tai nghe B dùng 9 giờ dù nghe nhạc hay gọi điện" phải đúng cả khi gọi (6 giờ). 9 giờ là số của nghe nhạc, nên D4 Lệch, `doi_dieu_kien`. Ví dụ thật: V49.

**Cụm khen không có con số** ("cả ngày", "suốt ngày dài", "không lo hết pin", "siêu bền", "bền bỉ", "vượt trội", "tuyệt đối", "trọn vẹn", "không giới hạn") không phải điều kiện, cũng không phải từ khẳng định. Bỏ qua khi gán. Ngoại lệ là cụm phủ ở trên và từ khẳng định gắn với con số (mục 6.2).

### 6.9 Giá trị và điều kiện

- **Con số của điều kiện không phải giá trị của thuộc tính.** Con số tài liệu dùng làm điều kiện (công suất bộ tiếp hợp tối thiểu, mốc phần trăm, số phút sạc, độ sâu, thời gian ngâm, phần diện tích đo) không phải giá trị công bố. Không dùng nó để khớp ở D3 hay D4. Tuyên bố lấy con số đó làm giá trị thì dò D1–D6 với các giá trị thật của thuộc tính. Ghi `nham_vai=<cụm>` vào ghi chú, để thống kê kiểu lỗi này ở Bước 38. Ví dụ tự đặt: tài liệu Điện thoại A chỉ ghi "sạc 50% trong 25 phút với bộ sạc 45W trở lên", không có con số công suất sạc nào. Tuyên bố "Điện thoại A sạc nhanh 45W" (thuộc tính công suất sạc): 45W là điều kiện của bài đo sạc nhanh, không phải công suất sạc; tài liệu không có số nào cho công suất sạc, nên D1. Ghi chú `nham_vai=45W`. Tài liệu có số công suất sạc ở cách sạc khác (ví dụ chỉ có số sạc không dây) thì không phải D1: dò tiếp D4–D6 với các số đó; con số của tuyên bố cao hơn mọi số công bố cho cùng bộ phận thì D5 (mục 7).
- **Không tạo giá trị mới bằng phép tính.** Chỉ so với con số hãng công bố. Không cộng, trừ, nhân các số để ra giá trị mới (ví dụ lấy tổng trừ phần tai nghe ra phần của hộp sạc). Tuyên bố về một bộ phận mà tài liệu không có số riêng thì dò D4–D6 như thường. Cấu hình chưa biết bộ phận đó thì ghi `ngoai_cau_hinh=<cụm>`. Ví dụ tự đặt: tài liệu Tai nghe B ghi "7 / 28 giờ" (tai nghe / tổng kèm hộp sạc); tuyên bố "Hộp sạc của Tai nghe B nạp thêm 21 giờ": hãng không công bố số riêng của hộp sạc, 21 không trùng số nào, nên D6 Chưa đủ thông tin.

## 7. Thứ tự quyết định D1–D6

Đi từ trên xuống, **dừng ở dòng đầu tiên thỏa**.

Trước khi dò, điều kiện của tuyên bố đã xác định xong ở bước 3 của mục 1: điều kiện nêu rõ cộng cách hiểu mặc định. Giữ nguyên điều kiện đó từ D1b tới D6. Không đổi điều kiện để con số khớp; con số trùng giá trị ở điều kiện khác là D4.

| Dòng | Kiểm tra | Nhãn | Lưu ý cho người gán |
|---|---|---|---|
| D1 | Tài liệu của đúng sản phẩm không có con số nào cho thuộc tính, ở bất kỳ điều kiện, bộ phận hay phiên bản nào | Chưa đủ thông tin | Con số của sản phẩm khác trong cùng trang không tính (V17). Có số nhưng ở điều kiện hay bộ phận khác thì không dừng ở đây: dò tiếp, thường tới D4, D5 hoặc D6. Có số cho thuộc tính nhưng không có ở điều kiện tuyên bố nêu là D6, không phải D1. Con số chỉ dùng làm điều kiện không tính là số của thuộc tính (mục 6.9). Không ghi `mac_dinh` |
| D1a | Không xác định được điều kiện của tuyên bố; hoặc giá trị khớp trong tài liệu kèm điều kiện lạ mà mục 6.7 không giải được | Chưa đủ thông tin | Chỉ có ba lối vào: (1) tuyên bố không nêu một điều kiện mà mục 5 ghi "Không có mặc định" (mốc phần trăm, số phút sạc, chế độ hiển thị của điện thoại); (2) chữ của tuyên bố trỏ tới nhiều chế độ (iPhone "đỉnh", mục 6.5); (3) cụm điều kiện không giải được theo mục 6.7, 6.8. Điều kiện có cách hiểu mặc định không bao giờ là lý do dừng ở đây; con số không khớp ở điều kiện mặc định cũng không. Cấu hình chưa biết một cụm không phải lý do D1a cho nhãn chuẩn. Ghi nguyên nhân: `mac_dinh=<khóa>` cho lối (1), `chua_xac_dinh=<cụm>` cho lối (2) và (3) |
| D1b | Ở điều kiện của tuyên bố (nêu rõ cộng mặc định), tài liệu ghi hai giá trị khác nhau cho cùng sản phẩm và thuộc tính | Chưa đủ thông tin, `tai_lieu_mau_thuan = true` | Áp dụng dù con số của tuyên bố trùng một trong hai giá trị hay khác cả hai. Ngoại lệ (QĐ13): con số khớp cả hai giá trị (bằng hoặc kém thuận lợi hơn cả hai, mục 6.1) thì không dừng ở đây, dò tiếp D2–D3; ghi `mau_thuan_khop_ca_hai=<giá trị 1>/<giá trị 2>`. Mâu thuẫn ở điều kiện khác điều kiện của tuyên bố không tính |
| D2 | Từ khẳng định gắn với con số cho một mức không cao hơn mức "lên đến" ở cùng điều kiện | Lệch (`doi_kieu_gia_tri`) | Mục 6.2. Tuyên bố không có từ khẳng định thì không bao giờ dừng ở đây; chỉ thiếu chữ "lên đến" vẫn khớp ở D3. Từ ở vế nói việc khác và tên tính năng không tính. "hơn", "trên", "không dưới", "trở lên" đứng liền con số của giá trị là từ khẳng định. Ghi `khang_dinh=<từ>` |
| D3 | Ở đúng điều kiện đã xác định (nêu rõ cộng mặc định), có thông số và giá trị khớp | Đúng | Khớp là bằng (trong 1%) hoặc kém thuận lợi hơn. Chỉ so với con số hãng công bố, không với số tự tính ra (mục 6.9) |
| D4 | Giá trị của tuyên bố bằng giá trị công bố ở một điều kiện khác | Lệch | Tính mọi điều kiện khác của cùng sản phẩm và thuộc tính, kể cả hoạt động khác (V42, mục 11.2). Gồm cả khi tuyên bố không nêu điều kiện và cách hiểu mặc định khác điều kiện của con số (`bo_dieu_kien`). Con số của điều kiện (bộ sạc, mốc phần trăm, độ sâu...) không tính là giá trị (mục 6.9) |
| D5 | Giá trị mâu thuẫn với giá trị ở cùng điều kiện, hoặc thuận lợi hơn mọi giá trị công bố cho cùng bộ phận và phiên bản | Sai | "Mọi giá trị" tính theo bộ phận: "nghe nhạc 8 giờ" là Sai vì thuận lợi hơn mọi giá trị của tai nghe, dù tổng kèm hộp sạc lớn hơn 8 giờ. Mã IP khác nhánh không khớp; không trùng mã nào ở điều kiện hay bộ phận khác thì Sai (mục 6.6) |
| D6 | Còn lại: tài liệu có số cho thuộc tính nhưng không công bố giá trị ở điều kiện của tuyên bố; số của tuyên bố không trùng số nào và không thuận lợi hơn mọi số | Chưa đủ thông tin | |

D1a và D1b không có trong chuỗi D của đề cương nhưng lấy từ chỗ khác của đề cương (câu "nếu vẫn không xác định được điều kiện thì kết luận Chưa đủ thông tin" ở Nội dung 2; vế "hoặc ghi mâu thuẫn" trong định nghĩa nhãn). Hai dòng đặt trước D2 để không bao giờ dẫn tới Đúng.

## 8. Ghi nhãn

Mỗi tuyên bố một dòng trong `data/nhan/*.jsonl`:

```json
{"id": "vd-V31", "nhan": "LECH", "dong_d": "D4", "loai": "doi_dieu_kien",
 "bang_chung": ["tn-samsung-buds3pro#038", "tn-samsung-buds3pro#042", "tn-samsung-buds3pro#044"],
 "trich": "Tắt Tính năng ANC Đến 7 / 30 giờ | Đến 7,0/30 giờ (Tính năng ANC Tắt) | Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7",
 "ly_do": "Giá trị 7 giờ chỉ đạt khi tắt chống ồn; tuyên bố nêu bật chống ồn. Nguồn: “Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7”.",
 "nguoi_gan": "phuoc", "luot": 2, "giay": 95, "tai_lieu_mau_thuan": false, "ghi_chu": "mac_dinh=bo_phan"}
```

Dòng trên là ví dụ V31 viết thành bản ghi. `id` thật là mã tuyên bố trong `data/tuyen_bo/`; ở đây dùng mã giả.

`dong_d`: dòng D đã dừng ở mục 7; nhãn phải khớp với dòng (D1, D1a, D1b, D6: Chưa đủ thông tin; D2, D4: Lệch; D3: Đúng; D5: Sai).

`luot`: lượt gán của cùng một bộ tuyên bố. Gán lại theo một bản hướng dẫn mới là một lượt mới (bộ thử: lượt 1 theo bản 1, lượt 2 theo bản 2). Lượt mới gán lại toàn bộ, lưu riêng, giữ nguyên lượt cũ. Khi gán, người gán không mở nhãn của lượt trước và các ghi chép về nhãn lượt trước.

**Bằng chứng và câu trích.** Ghi mã đoạn `<ma_mau>#<số>` và chép **nguyên văn** từ `noi_dung` hoặc `chu_thich` của đoạn. Số chú thích của trang hãng đã được bỏ khỏi `noi_dung` (bản gốc ở `noi_dung_goc`), nên câu trích chép theo chữ hiển thị. Hệ thống chỉ chuẩn hóa khoảng trắng và dấu câu khi kiểm câu trích.

- **Ghi mọi đoạn có cùng con số ở cùng điều kiện mà nhãn dựa vào**, không chỉ một đoạn. Cùng một dòng thông số thường lặp ở đoạn giới thiệu, khối nổi bật và bảng thông số (V09, V31). Nhãn Lệch: mọi đoạn chứa giá trị trùng. Nhãn Sai: mọi đoạn chứa giá trị ở cùng điều kiện. Nhãn Đúng: mọi đoạn chứa giá trị khớp. Chưa đủ thông tin ở D1a, D1b, D6: các đoạn chứa những con số mà lý do dựa vào. D1 để trống.
- Đoạn của bảng so sánh nhiều sản phẩm chỉ tính khi cột của đúng sản phẩm có con số đó (mục 4).
- Câu trích lấy từ ít nhất một đoạn bằng chứng. Nhiều phần thì nối bằng " | "; mỗi phần phải là chuỗi con nguyên văn của một đoạn bằng chứng.

**Loại biến đổi** (`loai`):

| Mã | Khi nào |
|---|---|
| `bo_dieu_kien` | Tuyên bố không nêu điều kiện; cách hiểu mặc định khác điều kiện của con số |
| `doi_dieu_kien` | Tuyên bố nêu rõ chế độ, phụ kiện hoặc điều kiện đo khác điều kiện của con số, kể cả điều kiện dạng số không thỏa và cụm phủ nhiều giá trị (mục 6.8) |
| `doi_bo_phan` | Tuyên bố nêu rõ bộ phận khác |
| `doi_phien_ban` | Tuyên bố nêu rõ phiên bản khác |
| `doi_kieu_gia_tri` | Dòng D2, hoặc tuyên bố ghi rõ kiểu giá trị khác tài liệu |
| `doi_gia_tri` | Nhãn Sai vì con số sai |

- Nhãn Lệch luôn có loại. Nhãn Sai ghi `doi_gia_tri`; riêng tuyên bố Sai vì gán cho bộ phận hoặc phiên bản khác mà không trùng giá trị nào thì ghi `doi_bo_phan` hoặc `doi_phien_ban` (V18). Nhãn Đúng và Chưa đủ thông tin để trống.
- Với mỗi điều kiện khác tài liệu: tuyên bố nêu rõ thì loại `doi_…`, và khóa đó không có trong `mac_dinh`; tuyên bố không nêu thì loại `bo_dieu_kien`, và khóa đó có trong `mac_dinh`. Một điều kiện không vừa nêu rõ vừa lấy mặc định.
- Con số trùng nhiều giá trị ở điều kiện khác: so với giá trị khác tuyên bố ở ít điều kiện nhất. Khác ở từ hai điều kiện: ưu tiên điều kiện tuyên bố nêu rõ (mã `doi_...`) hơn điều kiện lấy mặc định (`bo_dieu_kien`); nêu rõ nhiều điều kiện thì ưu tiên bộ phận, rồi phiên bản, rồi kiểu giá trị, rồi các điều kiện còn lại. Lý do ghi đủ các điều kiện khác nhau. Quy tắc này tạm chốt, chốt cùng hàm `loai_bien_doi` ở Bước 27.

**Lý do** viết một câu, nêu rõ điều kiện nào bị bỏ hoặc bị đổi. Dùng mẫu câu của hệ thống (T5.6) khi được. Chỗ `{câu trích}` là câu trích nguyên văn từ tài liệu, đặt trong ngoặc kép; không ghi mã đoạn vào chỗ này (mã đoạn đã nằm ở `bang_chung`).

| Dòng | Mẫu câu |
|---|---|
| D1 | "Tài liệu của {sản phẩm} không có thông số {thuộc tính}." |
| D1a | "Chưa xác định được điều kiện của tuyên bố: “{cụm điều kiện}”." |
| D1b | "Tài liệu ghi hai giá trị khác nhau cho {thuộc tính} ở {điều kiện}: “{câu trích 1}” và “{câu trích 2}”." |
| D2 | "Tài liệu ghi mức tối đa: “{câu trích}”; tuyên bố viết thành mức chắc chắn đạt." |
| D3 | "Khớp với tài liệu: “{câu trích}”." |
| D4 | "Giá trị {giá trị} {đơn vị} chỉ đạt khi {điều kiện trong tài liệu}; tuyên bố {nêu hoặc được hiểu là} {điều kiện của tuyên bố}. Nguồn: “{câu trích}”." |
| D5 | "Tài liệu ghi {giá trị trong tài liệu} {đơn vị} ở {điều kiện}; tuyên bố ghi {giá trị}." |
| D6 | "Tài liệu không công bố {thuộc tính} ở {điều kiện của tuyên bố}." |

**Ghi chú** (`ghi_chu`), nhiều mục cách nhau bằng "; ":

| Mã | Khi nào ghi | Dùng ở |
|---|---|---|
| `mac_dinh=<điều kiện>` | Ghi mọi khóa ở bảng mục 5 của nhóm và thuộc tính mà tuyên bố không nêu, ở mọi dòng từ D1a tới D6; các khóa cách nhau bằng dấu phẩy. Gồm cả khóa "Không có mặc định" khi dừng ở D1a vì khóa đó. Không cần xét nhãn có đổi theo cách hiểu hay không. Không ghi: khóa có giá trị `nhu_hang_cong_bo`; khóa không áp dụng (mục 4, ví dụ cách sạc khi máy không có sạc không dây); khóa tuyên bố đã nêu rõ (mục 8, loại biến đổi); mọi khóa khi dừng ở D1, vì D1 dừng trước khi xét điều kiện. Khóa đặc biệt `ngoai_bang`: nhãn dựa vào nguyên tắc chung của mục 6.7 ý 4 cho điều kiện không có trong bảng mục 5 (chưa khảo sát; QĐ10); ghi kèm `ngoai_cau_hinh=<cụm>` | Phân tích độ nhạy ở Bước 37: tính lại khi mọi nhãn phụ thuộc mặc định đổi thành Chưa đủ thông tin. Vì ghi cả khóa không làm đổi nhãn, phép tính này là cận trên |
| `khang_dinh=<từ>` | Dừng ở D2: từ khẳng định gắn với con số (mục 6.2), chép đúng chữ của tuyên bố | Kiểm D2 trên trang gán nhãn; thống kê từ khẳng định |
| `chua_xac_dinh=<cụm>` | Dừng ở D1a vì chữ của tuyên bố trỏ tới nhiều chế độ, hoặc cụm điều kiện không giải được (mục 6.7, 6.8) | Nguyên nhân của D1a; thống kê ở Bước 37–38 |
| `chep_nhan=<cụm>` | Điều kiện của tuyên bố xác định theo luật chép đúng nhãn của tài liệu (mục 6.8, QĐ15) | Phân tích độ nhạy ở Bước 37: tính lại các nhãn này theo cách hiểu mặc định của người đọc (mục 5) |
| `nham_vai=<cụm>` | Tuyên bố lấy con số tài liệu chỉ dùng làm điều kiện để làm giá trị (mục 6.9) | Thống kê kiểu lỗi ở Bước 38 |
| `mau_thuan_khop_ca_hai=<giá trị 1>/<giá trị 2>` | Tài liệu ghi hai giá trị mâu thuẫn ở điều kiện của tuyên bố, nhưng con số của tuyên bố khớp cả hai nên không dừng ở D1b (mục 7, QĐ13) | Báo riêng các ca tài liệu mâu thuẫn; tính FAR khi có và khi bỏ các ca này (mục 11.4) |
| `ngoai_cau_hinh=<cụm>` | Điều kiện cấu hình chưa biết, người gán tự xác định theo mục 6.7, 6.8 | Thống kê độ bao phủ ở Bước 37–38 |
| `ngoai_sau_loai=<cụm>` | Điều kiện không xếp được vào sáu loại | Phần giới hạn của khóa luận (T10 điểm 10) |

Dừng ở D1a thì ghi chú phải nêu nguyên nhân: `mac_dinh=<khóa không có mặc định>` hoặc `chua_xac_dinh=<cụm>`. Chỉ ghi khóa có cách hiểu mặc định mà dừng ở D1a là sai (mục 7, lưu ý D1a).

**Thời gian:** `giay` là số giây từ lúc đọc tuyên bố đến lúc ghi xong. Trang gán nhãn dừng đếm khi không có thao tác quá 3 phút và ghi số giây bị bỏ vào trường `giay_nghi` (không tính vào `giay`). Chỗ hướng dẫn chưa rõ thì ghi vào danh sách "câu hỏi nhãn" để giải quyết ở lần sửa hướng dẫn sau, không tự đặt quy tắc mới. Tuyên bố còn thiếu điều kiện so với câu gốc thì ghi `tach=<thiếu gì>` vào câu hỏi nhãn, vẫn gán theo tuyên bố (mục 1, bước 0).

## 9. Ví dụ

51 ví dụ, chỉ từ 4 mẫu tập phát triển. Mọi câu trích đã kiểm là chuỗi con của `noi_dung` hoặc `chu_thich` trong `doan.jsonl` đã bỏ số chú thích (sau khi gộp khoảng trắng; kiểm ngày 01/11/2026). "P:" ghi đầu ra dự kiến của hệ thống khi khác nhãn chuẩn. Mục 9.5 gom 4 ví dụ đổi nhãn sau khảo sát Bước 10; mục 9.6 gom 3 ví dụ thêm ở Bước 16. Số hiệu giữ nguyên để các tệp khác nhắc tới vẫn đúng.

Bản 2 không đổi nhãn ví dụ nào. Ghi chú `mac_dinh` viết lại theo mục 8 (ghi mọi khóa không nêu); bằng chứng ghi đủ các đoạn có cùng con số; D2 ghi `khang_dinh`, D1a ghi nguyên nhân.

### 9.1 Đúng

**V01 · Đúng · D3.** iPhone 17 sạc nhanh lên đến 50% trong 20 phút với bộ sạc 40W trở lên.
- Bằng chứng: `dt-apple-iphone17#016` “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C”
- Lý do: Khớp với tài liệu: mốc 50%, 20 phút, bộ sạc 40W đạt đúng mức tối thiểu; không nêu cách sạc nên hiểu là sạc bằng cáp, như tài liệu.
- Ghi chú: `mac_dinh=cach_sac`.

**V02 · Đúng · D3 · điều kiện dạng số.** iPhone 17 sạc 50% trong 20 phút với củ sạc 60W.
- Bằng chứng: `dt-apple-iphone17#016` “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C”
- Lý do: Củ 60W thỏa "40W trở lên" (60 ≥ 40) nên cùng điều kiện; 20 phút khớp (quảng cáo bỏ "lên đến").
- Ghi chú: `mac_dinh=cach_sac`.

*V03 đổi nhãn sau khảo sát Bước 10 rồi đổi lại theo QĐ15 ngày 02/11, xem mục 9.5.*

**V04 · Đúng · D3.** iPhone 17 dùng pin được 27 giờ.
- Bằng chứng: `dt-apple-iphone17#016` “Thời gian xem video (trực tuyến) Lên đến 27 giờ”
- Lý do: Không nêu hoạt động nên lấy hoạt động kém thuận lợi nhất hãng công bố là xem video trực tuyến, 27 giờ; khớp (quảng cáo bỏ "lên đến").
- Ghi chú: `mac_dinh=hoat_dong`.

**V05 · Đúng · D3.** Màn hình iPhone 17 sáng tối đa 1000 nit.
- Bằng chứng: `dt-apple-iphone17#005` “Độ sáng tối đa 1000 nit (tiêu chuẩn)”
- Lý do: Với Apple, "tối đa" là chế độ tiêu chuẩn (mục 6.5); cùng chế độ, 1000 nit khớp.

**V06 · Đúng · D3 · điều kiện dạng số.** iPhone 17 đạt IP68, chống nước ở độ sâu 4 mét trong 30 phút.
- Bằng chứng: `dt-apple-iphone17#007` “Đạt mức IP68 (chống nước ở độ sâu tối đa 6 mét trong vòng tối đa 30 phút) theo tiêu chuẩn IEC 60529”
- Lý do: 4 mét không quá 6 mét, 30 phút không quá 30 phút, nên cùng điều kiện thử; mã IP68 bằng nhau.

**V07 · Đúng · D3 · kém thuận lợi hơn.** Xiaomi 15T dùng liên tục được 13 giờ.
- Bằng chứng: `dt-xiaomi-15t#047` “Tối đa 13,19 giờ Sử dụng liên tục”
- Lý do: "Dùng liên tục" không nêu hoạt động cụ thể (mục 6.8, ý 3), nên lấy hoạt động kém thuận lợi nhất. Xiaomi 15T chỉ công bố một hoạt động (sử dụng liên tục, 13,19 giờ), nên đó cũng là hoạt động kém thuận lợi nhất. 13 giờ thấp hơn 13,19 giờ, tức kém thuận lợi hơn, vẫn khớp.
- Ghi chú: `mac_dinh=hoat_dong`.

**V08 · Đúng · D3 · điều kiện lạ trong tài liệu.** Xiaomi 15T đạt chuẩn chống nước IP68.
- Bằng chứng: `dt-xiaomi-15t#012` “IP68” và chú thích “ngâm trong nước ngọt tĩnh lặng ở độ sâu 3 mét; tối đa 30 phút; với mức chênh lệch nhiệt độ giữa nước và sản phẩm là từ 5K trở xuống”; `dt-xiaomi-15t#035` “IP68 Khả năng chống nước và bụi”
- Lý do: Không nêu điều kiện thử nên hiểu như hãng công bố; mã IP68 bằng nhau.
- Ghi chú: `ngoai_cau_hinh=chênh lệch nhiệt độ ≤5K`. Người gán xếp cụm này vào điều kiện đo của bài thử, hiểu như hãng công bố. Bảng bao phủ có ghi điều kiện nhiệt độ (mục 2.7) nhưng `dien_thoai.yaml` chưa có cụm này.
- P: D1a (`dieu_kien_la`) nếu bước trích xuất ghi cụm nhiệt độ vào `dieu_kien_khac`.

**V09 · Đúng · D3.** Galaxy Buds3 Pro nghe nhạc 6 giờ khi bật chống ồn.
- Bằng chứng: `tn-samsung-buds3pro#038` “BẬT Tính năng ANC Đến 6 / 26 giờ”; `tn-samsung-buds3pro#042` “Đến 6,0/26 giờ (Tính năng ANC Bật)”; `tn-samsung-buds3pro#044` “Thời gian phát nhạc (bật ANC) Lên đến 6”
- Lý do: Cùng chế độ bật chống ồn; không nêu bộ phận nên hiểu là tai nghe (số 6 trong "6 / 26"); 6 giờ khớp (quảng cáo bỏ "lên đến"). Con số này lặp ở khối "Thời gian phát", cột Buds3 Pro của bảng so sánh và bảng thông số, nên ghi cả ba đoạn. Ví dụ của đề cương.
- Ghi chú: `mac_dinh=bo_phan`.

**V10 · Đúng · D3.** Galaxy Buds3 Pro nghe nhạc đến 6 giờ.
- Bằng chứng: `tn-samsung-buds3pro#038` “BẬT Tính năng ANC Đến 6 / 26 giờ”; `tn-samsung-buds3pro#042` “Đến 6,0/26 giờ (Tính năng ANC Bật)”; `tn-samsung-buds3pro#044` “Thời gian phát nhạc (bật ANC) Lên đến 6”; `tn-samsung-buds3pro#020` chú thích “ANC (Active Noise Canceling) được bật theo mặc định.”
- Lý do: Không nêu chế độ nên hiểu là chống ồn bật, vì hãng ghi ANC bật theo mặc định; ở chế độ này tài liệu ghi đến 6 giờ, khớp.
- Ghi chú: `mac_dinh=che_do_chong_on,bo_phan`.

**V11 · Đúng · D3.** Apple Watch SE 3 dùng đến 32 giờ ở chế độ nguồn điện thấp.
- Bằng chứng: `dh-apple-watchse3#008` “Lên đến 32 giờ ở Chế Độ Nguồn Điện Thấp”
- Lý do: Cùng chế độ nguồn điện thấp; 32 giờ khớp. Ví dụ của đề cương.
- Ghi chú: `mac_dinh=hoat_dong`.

**V12 · Đúng · D3 · so thẳng.** Apple Watch SE 3 có độ sáng 1000 nit.
- Bằng chứng: `dh-apple-watchse3#007` “Độ sáng đỉnh 1000 nit”
- Lý do: Tài liệu chỉ có một con số độ sáng và không kèm điều kiện nào; "đỉnh" gắn với một giá trị duy nhất nên là kiểu giá trị tối đa. So thẳng: khớp; tài liệu không nêu điều kiện.
- Ghi chú: `mac_dinh=che_do_hien_thi`. Tài liệu im lặng về chế độ hiển thị không đủ để coi điều kiện này là không áp dụng (mục 4).

**V13 · Đúng · D3.** Apple Watch SE 3 chống nước 5ATM, đeo được khi bơi lội trong bể bơi.
- Bằng chứng: `dh-apple-watchse3#016` “Chống nước ở độ sâu 50m (chống nước khi bơi)” và chú thích “có khả năng chống nước ở độ sâu 50 mét theo tiêu chuẩn ISO 22810:2010”, “bơi lội trong bể bơi hoặc dưới biển”
- Lý do: Theo ISO 22810, 5ATM quy về 50 m, bằng mức hãng công bố; bơi trong bể bơi là hoạt động hãng cho phép.

**V14 · Đúng · D3 · biến thể `doi_phien_ban`.** Apple Watch SE 3 bản GPS + Cellular dùng được 18 giờ.
- Bằng chứng: `dh-apple-watchse3#008` “Pin dùng cả ngày, lên đến 18 giờ khi sử dụng bình thường” và chú thích “mức sử dụng Apple Watch SE 3 (GPS + Cellular) bao gồm tổng cộng 4 giờ kết nối mạng di động và 14 giờ kết nối với iPhone qua Bluetooth trong chu kỳ 18 giờ”
- Lý do: Tài liệu không tách thời lượng pin theo phiên bản, và chú thích cho thấy bản GPS + Cellular cũng đạt 18 giờ khi sử dụng bình thường. Đổi phiên bản ở đây không đổi giá trị, nên vẫn Đúng.
- Ghi chú: `mac_dinh=che_do_nguon,hoat_dong`.

**V15 · Đúng · D3 · biến thể `doi_phien_ban`.** Apple Watch SE 3 bản 40mm dùng được 18 giờ khi sử dụng bình thường.
- Bằng chứng: `dh-apple-watchse3#008` “Pin dùng cả ngày, lên đến 18 giờ khi sử dụng bình thường”; `dh-apple-watchse3#002` “Dài: 40mm”
- Lý do: Trang có cỡ vỏ 40mm và 44mm nhưng chỉ tách khối lượng và màn hình, không tách thời lượng pin; điều kiện cỡ vỏ không áp dụng cho thuộc tính này, nên 18 giờ khớp.
- Ghi chú: `mac_dinh=che_do_nguon`.

### 9.2 Sai

**V16 · Sai (`doi_gia_tri`) · D5.** Galaxy Buds3 Pro nghe nhạc 8 giờ.
- Bằng chứng: `tn-samsung-buds3pro#038` “Tắt Tính năng ANC Đến 7 / 30 giờ”, “BẬT Tính năng ANC Đến 6 / 26 giờ”; `tn-samsung-buds3pro#042` “Đến 6,0/26 giờ (Tính năng ANC Bật)”; `tn-samsung-buds3pro#044` “Thời gian phát nhạc (bật ANC) Lên đến 6”
- Lý do: Tài liệu ghi 6 giờ ở điều kiện hiểu mặc định (chống ồn bật, tai nghe); 8 giờ còn thuận lợi hơn mọi giá trị công bố cho tai nghe (cao nhất 7 giờ) và không trùng giá trị nào. Ví dụ của đề cương.
- Ghi chú: `mac_dinh=che_do_chong_on,bo_phan`.

**V17 · Sai (`doi_gia_tri`) · D5 · sai đối tượng (sản phẩm).** Galaxy Buds3 Pro nghe nhạc 8,5 giờ khi tắt chống ồn.
- Bằng chứng: `tn-samsung-buds3pro#042` “Đến 7,0/30 giờ (Tính năng ANC Tắt)”; `tn-samsung-buds3pro#038` “Tắt Tính năng ANC Đến 7 / 30 giờ”; `tn-samsung-buds3pro#044` “Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7”
- Lý do: Tài liệu ghi 7 giờ khi tắt chống ồn; tuyên bố ghi 8,5 giờ. Số 8,5 giờ trong đoạn `#042` thuộc cột Galaxy Buds FE của bảng so sánh, không phải của Buds3 Pro, nên không tính là giá trị ở điều kiện khác.
- Ghi chú: `mac_dinh=bo_phan`.

**V18 · Sai (`doi_bo_phan`) · D5 · sai đối tượng (bộ phận).** Hộp sạc Galaxy Buds3 Pro cũng kháng nước.
- Bằng chứng: `tn-samsung-buds3pro#038` chú thích “Hộp sạc không có khả năng kháng nước.”
- Lý do: Tài liệu ghi hộp sạc không kháng nước; tuyên bố nói có. Tuyên bố không nêu mã nên không trùng mã IP57 của tai nghe; so với V35.

**V19 · Sai (`doi_gia_tri`) · D5.** Màn hình iPhone 17 đạt 4000 nit ngoài trời.
- Bằng chứng: `dt-apple-iphone17#005` “độ sáng đỉnh 3000 nit (ngoài trời)”
- Lý do: Tài liệu ghi 3000 nit ở chế độ ngoài trời; tuyên bố ghi 4000 nit, thuận lợi hơn và không trùng giá trị nào.

**V20 · Sai (`doi_gia_tri`) · D5 · thấp hơn tốt hơn.** Xiaomi 15T sạc đầy 100% chỉ trong 40 phút với củ sạc 67W.
- Bằng chứng: `dt-xiaomi-15t#047` “50 phút sạc đầy 100%” và chú thích “Máy được khuyến cáo sử dụng củ sạc Xiaomi 67W hoặc cao hơn.”
- Lý do: Cùng điều kiện (củ 67W thỏa "67W hoặc cao hơn", mốc 100%); tài liệu ghi 50 phút, tuyên bố ghi 40 phút. Với thời gian sạc, thấp hơn là thuận lợi hơn, nên 40 phút mâu thuẫn với tài liệu.
- Ghi chú: không có `mac_dinh`. Bộ tiếp hợp và mốc phần trăm đã nêu rõ; cách sạc không áp dụng vì Xiaomi 15T không công bố sạc không dây (V23).

### 9.3 Lệch điều kiện

**V21 · Lệch (`bo_dieu_kien`) · D4.** iPhone 17 sạc 50% chỉ trong 20 phút.
- Bằng chứng: `dt-apple-iphone17#016` “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C”; `dt-apple-iphone17#040` “Trong Hộp Sản Phẩm iPhone với iOS 27 Cáp Sạc USB-C (1m)”
- Lý do: 20 phút chỉ đạt với bộ tiếp hợp 40W trở lên, được bán riêng; tuyên bố không nêu bộ sạc nên hiểu là chỉ có đồ trong hộp (cáp, không có củ sạc). Thiếu chữ "lên đến" không phải lý do của nhãn; chữ "chỉ" không phải từ khẳng định. Ví dụ của đề cương.
- Ghi chú: `mac_dinh=bo_tiep_hop,cach_sac`.

**V22 · Lệch (`doi_dieu_kien`) · D4 · điều kiện dạng số.** iPhone 17 sạc 50% trong 20 phút với củ sạc 20W.
- Bằng chứng: `dt-apple-iphone17#016` “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C”
- Lý do: 20 phút chỉ đạt với bộ tiếp hợp 40W trở lên; tuyên bố nêu củ 20W, thấp hơn mức tối thiểu (20 < 40), là điều kiện khác.
- Ghi chú: `mac_dinh=cach_sac`. Bộ tiếp hợp đã nêu rõ nên không có trong `mac_dinh`.

**V23 · Lệch (`bo_dieu_kien`) · D4.** Xiaomi 15T hỗ trợ sạc nhanh HyperCharge 67W.
- Bằng chứng: `dt-xiaomi-15t#005` “Sạc nhanh HyperCharge 67W” và chú thích “Bộ sạc không bao gồm trong hộp. Máy được khuyến cáo sử dụng củ sạc Xiaomi 67W hoặc cao hơn.”; `dt-xiaomi-15t#022` “Sạc nhanh HyperCharge 67W”; `dt-xiaomi-15t#046` “Sạc nhanh HyperCharge 67W”; `dt-xiaomi-15t#047` “Sạc nhanh HyperCharge 67W”; `dt-xiaomi-15t#014` “Điện thoại di động / Cáp USB Type-C”
- Lý do: Công suất 67W cần củ sạc 67W trở lên, không có trong hộp; tuyên bố không nêu củ sạc nên hiểu là không mua thêm.
- Ghi chú: `mac_dinh=bo_tiep_hop`. Không ghi `cach_sac`: trang Xiaomi 15T không công bố sạc không dây, nên điều kiện có dây hay không dây không áp dụng.

**V24 · Lệch (`bo_dieu_kien`) · D4.** iPhone 17 dùng pin được 30 giờ.
- Bằng chứng: `dt-apple-iphone17#016` “Thời gian xem video Lên đến 30 giờ”, “Thời gian xem video (trực tuyến) Lên đến 27 giờ”
- Lý do: Không nêu hoạt động và không trùng chữ nhãn nào của tài liệu, nên phải đúng ở hoạt động kém thuận lợi nhất là xem video trực tuyến (27 giờ); 30 giờ là số của dòng "Thời gian xem video". Không chọn dòng đó chỉ vì số 30 trùng (mục 6.8, luật chép đúng nhãn, điều kiện 3).
- Ghi chú: `mac_dinh=hoat_dong`.

*V25, V26 đổi nhãn sau khảo sát Bước 10, xem mục 9.5.*

**V27 · Lệch (`doi_dieu_kien`) · D4 · điều kiện dạng số.** Dưới ánh sáng mạnh, Xiaomi 15T sáng 3200 nit trên toàn màn hình.
- Bằng chứng: `dt-xiaomi-15t#004` “Độ sáng cực đại: 3200 nit trên 25% diện tích màn hình”; `dt-xiaomi-15t#037` “Màn hình siêu sáng 3.200 nit”; `dt-xiaomi-15t#038` “Dưới ánh sáng mạnh, màn hình sẽ tự động kích hoạt chế độ tăng mức sáng APL 25%”
- Lý do: Tuyên bố nêu đúng chế độ tự tăng sáng dưới ánh sáng mạnh. 3200 nit đo trên 25% diện tích; tuyên bố nói toàn màn hình (100%), vượt phần hãng đo (100 > 25), là điều kiện khác.
- Ghi chú: `ngoai_cau_hinh=toàn màn hình`. Cấu hình chưa có cụm "toàn màn hình" cho phần diện tích đo. Câu tuyên bố sửa ngày 28/10 (trước là "Xiaomi 15T có độ sáng cực đại 3200 nit trên toàn màn hình"): độ sáng điện thoại không còn cách hiểu mặc định, nên tuyên bố phải tự nêu chế độ thì mới còn là ví dụ về điều kiện dạng số.

**V28 · Lệch (`bo_dieu_kien`) · D4.** iPhone 17 zoom 10x.
- Bằng chứng: `dt-apple-iphone17#009` “Độ phóng đại quang học 2x”, “Độ thu phóng kỹ thuật số lên đến 10x”
- Lý do: Không nêu loại zoom nên hiểu là quang học (2x); 10x là thu phóng kỹ thuật số.
- Ghi chú: `mac_dinh=loai_zoom,dai_luong,che_do_camera`.

**V29 · Lệch (`doi_dieu_kien`) · D4 · điều kiện dạng số.** iPhone 17 đạt IP68, ngâm được ở độ sâu 10 mét.
- Bằng chứng: `dt-apple-iphone17#007` “Đạt mức IP68 (chống nước ở độ sâu tối đa 6 mét trong vòng tối đa 30 phút)”
- Lý do: IP68 của iPhone 17 chỉ thử đến độ sâu tối đa 6 mét; tuyên bố nêu 10 mét, vượt điều kiện thử (10 > 6).

**V30 · Lệch (`doi_dieu_kien`) · D4.** Apple Watch SE 3 chống nước 50 m, đeo được khi lặn với bình dưỡng khí.
- Bằng chứng: `dh-apple-watchse3#016` “Chống nước ở độ sâu 50m (chống nước khi bơi)” và chú thích “Khuyến nghị không sử dụng Apple Watch SE 3 cho hoạt động lặn với bình dưỡng khí”
- Lý do: Mức 50 m áp dụng cho hoạt động dưới nước nông như bơi; hãng khuyến nghị không dùng khi lặn với bình dưỡng khí, nhưng tuyên bố gán mức này cho đúng hoạt động đó.

**V31 · Lệch (`doi_dieu_kien`) · D4.** Galaxy Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn.
- Bằng chứng: `tn-samsung-buds3pro#038` “Tắt Tính năng ANC Đến 7 / 30 giờ”; `tn-samsung-buds3pro#042` “Đến 7,0/30 giờ (Tính năng ANC Tắt)”; `tn-samsung-buds3pro#044` “Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7”
- Lý do: 7 giờ chỉ đạt khi tắt chống ồn; tuyên bố ghi bật chống ồn (bật thì 6 giờ). Ba đoạn cùng chứa giá trị trùng. Ví dụ của đề cương.
- Ghi chú: `mac_dinh=bo_phan`.

**V32 · Lệch (`bo_dieu_kien`) · D4.** Galaxy Buds3 Pro pin 7 giờ.
- Bằng chứng: `tn-samsung-buds3pro#044` “Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7”, “Thời gian phát nhạc (bật ANC) Lên đến 6”; `tn-samsung-buds3pro#038` “Tắt Tính năng ANC Đến 7 / 30 giờ”; `tn-samsung-buds3pro#042` “Đến 7,0/30 giờ (Tính năng ANC Tắt)”; `tn-samsung-buds3pro#020` chú thích “ANC (Active Noise Canceling) được bật theo mặc định.”
- Lý do: Không nêu chế độ nên hiểu là nghe nhạc, chống ồn bật (6 giờ); 7 giờ chỉ đạt khi tắt chống ồn.
- Ghi chú: `mac_dinh=che_do_chong_on,hoat_dong,bo_phan`.

**V33 · Lệch (`bo_dieu_kien`) · D4.** Apple Watch SE 3 pin 32 giờ.
- Bằng chứng: `dh-apple-watchse3#008` “Pin dùng cả ngày, lên đến 18 giờ khi sử dụng bình thường”, “Lên đến 32 giờ ở Chế Độ Nguồn Điện Thấp”
- Lý do: Không nêu chế độ nên hiểu là chế độ thường, sử dụng bình thường (18 giờ); 32 giờ chỉ đạt ở chế độ nguồn điện thấp.
- Ghi chú: `mac_dinh=che_do_nguon,hoat_dong`.

**V34 · Lệch (`bo_dieu_kien`) · D4 · phụ kiện chỉ ghi trong chú thích.** Apple Watch SE 3 sạc 80% trong khoảng 45 phút.
- Bằng chứng: `dh-apple-watchse3#009` “Sạc lên đến 80% trong khoảng 45 phút” và chú thích “Bộ Tiếp Hợp Nguồn USB-C 20W của Apple (Phiên bản A2305)”; `dh-apple-watchse3#023` “Trong Hộp Sản Phẩm Apple Watch SE 3 Dây đeo Cáp Sạc Nhanh Từ Tính Có Đầu Nối USB-C (1m) Của Apple Watch”
- Lý do: Hãng đo 45 phút với bộ tiếp hợp 20W, không có trong hộp (hộp chỉ có cáp); tuyên bố không nêu bộ sạc nên hiểu là không mua thêm. Bộ tiếp hợp chỉ nằm trong chú thích nhưng vẫn là điều kiện bắt buộc.
- Ghi chú: `mac_dinh=bo_tiep_hop,cap_sac`.

**V35 · Lệch (`doi_bo_phan`) · D4.** Hộp sạc Galaxy Buds3 Pro cũng đạt chuẩn IP57.
- Bằng chứng: `tn-samsung-buds3pro#044` “Chuẩn IP57”; `tn-samsung-buds3pro#039` “Kháng nước IP57”; `tn-samsung-buds3pro#041` “Kháng Bụi & Nước IP57”; `tn-samsung-buds3pro#038` chú thích “IP57 dựa trên các điều kiện thử nghiệm ngâm ở độ sâu 1 mét nước ngọt trong tối đa 30 phút.”, “Hộp sạc không có khả năng kháng nước.”
- Lý do: IP57 chỉ áp dụng cho tai nghe; tuyên bố gán cho hộp sạc, vốn không kháng nước. IP57 trùng giá trị của tai nghe nên dừng ở D4 trước D5; so với V18. Đoạn `#041` là bảng so sánh có cột Buds3 Pro ghi IP57 (thứ tự cột ghi ở cuối đoạn `#039`), nên tính là bằng chứng.

**V36 · Lệch (`doi_bo_phan`) · D4.** Tai nghe Galaxy Buds3 Pro có pin 515 mAh.
- Bằng chứng: `tn-samsung-buds3pro#044` “Dung lượng pin tai nghe (mAh, Typical) 50”, “Dung lượng pin hộp sạc (mAh, Typical) 515”
- Lý do: 515 mAh là dung lượng hộp sạc; tuyên bố gán cho tai nghe, vốn có 50 mAh.

**V37 · Lệch (`doi_kieu_gia_tri`) · D4.** Pin Xiaomi 15T có dung lượng định mức 5500mAh.
- Bằng chứng: `dt-xiaomi-15t#005` “Pin Xiaomi Surge 5500mAh (thông thường)”; `dt-xiaomi-15t#022` “Pin bền bỉ 5500mAh (typ)”; `dt-xiaomi-15t#046` “5500mAh (thông thường)”
- Lý do: 5500mAh là dung lượng điển hình; tuyên bố ghi rõ "định mức", một kiểu giá trị khác. Tuyên bố không ghi kiểu ("pin 5500mAh") thì hiểu là điển hình và Đúng.

**V38 · Lệch (`doi_kieu_gia_tri`) · D2.** Galaxy Buds3 Pro luôn nghe đủ 6 giờ.
- Bằng chứng: `tn-samsung-buds3pro#044` “Thời gian phát nhạc (bật ANC) Lên đến 6”; `tn-samsung-buds3pro#038` “BẬT Tính năng ANC Đến 6 / 26 giờ”; `tn-samsung-buds3pro#042` “Đến 6,0/26 giờ (Tính năng ANC Bật)”
- Lý do: Tài liệu ghi mức tối đa "lên đến 6"; tuyên bố dùng "luôn" gắn với 6 giờ để biến thành mức chắc chắn đạt.
- Ghi chú: `khang_dinh=luôn`; `mac_dinh=che_do_chong_on,hoat_dong,bo_phan`.

**V39 · Lệch (`doi_kieu_gia_tri`) · D2.** Apple Watch SE 3 luôn dùng đủ 18 giờ mỗi ngày.
- Bằng chứng: `dh-apple-watchse3#008` “Pin dùng cả ngày, lên đến 18 giờ khi sử dụng bình thường”
- Lý do: Tài liệu ghi mức tối đa "lên đến 18 giờ"; tuyên bố viết thành mức chắc chắn đạt.
- Ghi chú: `khang_dinh=luôn`; `mac_dinh=che_do_nguon,hoat_dong`.

**V40 · Lệch (`doi_kieu_gia_tri`) · D2.** Màn hình iPhone 17 luôn chạy ở 120Hz.
- Bằng chứng: `dt-apple-iphone17#004` “Công nghệ ProMotion với tốc độ làm mới thích ứng lên đến 120Hz”
- Lý do: Tài liệu ghi tần số quét thích ứng, tối đa 120Hz; tuyên bố viết thành luôn đạt 120Hz. Khác "Màn hình Luôn Bật" cùng đoạn: chữ "Luôn" ở đó là tên tính năng, không gắn với con số.
- Ghi chú: `khang_dinh=luôn`; `mac_dinh=kieu_tan_so`.

**V41 · Lệch (`doi_dieu_kien`) · D4 · điều kiện cấu hình chưa biết.** Apple Watch SE 3 bản GPS + Cellular dùng 18 giờ khi chỉ dùng mạng di động, không cần iPhone.
- Bằng chứng: `dh-apple-watchse3#008` chú thích “mức sử dụng Apple Watch SE 3 (GPS + Cellular) bao gồm tổng cộng 4 giờ kết nối mạng di động và 14 giờ kết nối với iPhone qua Bluetooth trong chu kỳ 18 giờ”
- Lý do: 18 giờ của bản GPS + Cellular đo với 4 giờ mạng di động và 14 giờ kết nối iPhone; tuyên bố nói cả 18 giờ chỉ dùng mạng di động, là điều kiện khác. Tài liệu không công bố thời lượng khi chỉ dùng mạng di động.
- Ghi chú: `ngoai_cau_hinh=chỉ dùng mạng di động`; `mac_dinh=che_do_nguon`.
- P: D1a, vì cấu hình chưa biết cụm này. Nhãn chuẩn vẫn theo tài liệu.

**V42 · Lệch (`doi_dieu_kien`) · D4 · trường hợp biên.** Galaxy Buds3 Pro nghe nhạc 5 giờ ở chế độ xuyên âm.
- Bằng chứng: `tn-samsung-buds3pro#044` “Thời gian đàm thoại (Giờ, tắt ANC) Lên đến 5”
- Lý do: Tài liệu không công bố thời lượng ở chế độ xuyên âm (Ambient), nhưng 5 giờ trùng thời gian đàm thoại khi tắt chống ồn. Theo định nghĩa, con số trùng giá trị ở một điều kiện khác là Lệch, kể cả khi điều kiện đó là hoạt động khác.
- Ghi chú: `mac_dinh=bo_phan`; rủi ro trùng số ngẫu nhiên, xem mục 11.2.

*V43 đổi nhãn sau khảo sát Bước 10, xem mục 9.5.*

### 9.4 Chưa đủ thông tin

**V44 · Chưa đủ thông tin · D6.** Galaxy Buds3 Pro nghe nhạc 6,5 giờ ở chế độ xuyên âm.
- Bằng chứng: `tn-samsung-buds3pro#038` “Tắt Tính năng ANC Đến 7 / 30 giờ”, “BẬT Tính năng ANC Đến 6 / 26 giờ”; `tn-samsung-buds3pro#042` “Đến 7,0/30 giờ (Tính năng ANC Tắt)”, “Đến 6,0/26 giờ (Tính năng ANC Bật)”; `tn-samsung-buds3pro#044` “Thời gian phát nhạc (bật ANC) Lên đến 6”, “Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7”
- Lý do: Tài liệu chỉ công bố thời lượng khi bật và tắt chống ồn, không công bố ở chế độ xuyên âm; 6,5 giờ không trùng giá trị nào và không cao hơn mọi giá trị của tai nghe (cao nhất 7 giờ). Cấu hình đã biết cụm "xuyên âm", "Ambient", nên P cũng dừng ở D6.
- Ghi chú: `mac_dinh=bo_phan`.

**V45 · Chưa đủ thông tin · D1 · thiếu bằng chứng.** Galaxy Buds3 Pro sạc nhanh 5 phút nghe được 1 giờ.
- Bằng chứng: không có.
- Lý do: Tài liệu của Galaxy Buds3 Pro không có thông số sạc nhanh.

**V46 · Chưa đủ thông tin · D1a.** iPhone 17 sạc nhanh chỉ trong 20 phút với bộ sạc 40W.
- Bằng chứng: `dt-apple-iphone17#016` “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C”
- Lý do: Chưa xác định được điều kiện của tuyên bố: tuyên bố không nói sạc tới bao nhiêu phần trăm, và mốc phần trăm không có cách hiểu mặc định. Người gán không đoán mốc từ con số 20 phút.
- Ghi chú: `mac_dinh=moc_phan_tram,cach_sac`. Bộ tiếp hợp đã nêu rõ (40W) nên không có trong `mac_dinh`.

**V47 · Chưa đủ thông tin · D1a.** iPhone 17 có độ sáng đỉnh 3000 nit.
- Bằng chứng: `dt-apple-iphone17#005` “độ sáng đỉnh 1600 nit (HDR); độ sáng đỉnh 3000 nit (ngoài trời)”
- Lý do: Trên trang Apple, "đỉnh" dùng cho hai chế độ (HDR 1600 nit, ngoài trời 3000 nit); tuyên bố không nói chế độ nào nên chưa xác định được điều kiện. Không chọn chế độ theo con số của tuyên bố.
- Ghi chú: `chua_xac_dinh=đỉnh` (chữ trỏ tới nhiều chế độ, lối vào 2 của D1a).

**V48 · Chưa đủ thông tin · D1b · xung đột bằng chứng.** Galaxy Buds3 Pro dùng tổng cộng 30 giờ kèm hộp sạc khi bật chống ồn.
- Bằng chứng: `tn-samsung-buds3pro#044` “Tổng thời gian phát nhạc (Giờ, bật ANC) Lên đến 26”, “Tổng thời gian phát nhạc (Giờ, bật ANC) Lên đến 30”; `tn-samsung-buds3pro#038` “BẬT Tính năng ANC Đến 6 / 26 giờ” và chú thích “Với tính năng bật/tắt ANC, tai nghe và hộp tai nghe cung cấp tối đa 30 giờ phát khi sạc đầy.”; `tn-samsung-buds3pro#042` “Đến 6,0/26 giờ (Tính năng ANC Bật)”
- Lý do: Tài liệu ghi hai giá trị cho tổng thời gian phát nhạc khi bật chống ồn: 26 giờ (khối "Thời gian phát", cột Buds3 Pro của bảng so sánh, bảng thông số) và 30 giờ (dòng thứ hai trong bảng thông số, nằm dưới nhóm tắt ANC nhưng ghi "bật ANC"; chú thích cũng ghi tối đa 30 giờ cho cả bật và tắt). Đặt `tai_lieu_mau_thuan = true`. Tuyên bố ghi 26 giờ kèm hộp sạc khi bật chống ồn thì khớp cả hai giá trị (bằng 26, thấp hơn 30), nên không dừng ở D1b mà dò tiếp tới D3 (QĐ13, 02/11/2026; trước đó bản 2 cho ra D1b).
- Ghi chú: `mac_dinh=hoat_dong`.

### 9.5 Đổi nhãn sau khảo sát Bước 10 (28/10/2026)

Khảo sát 10 người đọc (`ket_qua/khao_sat_cach_hieu.md`) sửa hai chỗ của cấu hình điện thoại: "xem video" không kèm "tải sẵn" hay "trực tuyến" coi như chưa nêu hoạt động (Q09, 9/10 người); độ sáng không còn cách hiểu mặc định khi tuyên bố không nêu chế độ (Q10, 7/10 người). Bốn ví dụ dưới đổi nhãn, giữ nguyên số hiệu.

**V03 · Đúng · D3 · chép đúng nhãn của tài liệu.** iPhone 17 xem video được 30 giờ.
- Bằng chứng: `dt-apple-iphone17#016` “Thời gian xem video Lên đến 30 giờ”
- Lý do: Khớp với tài liệu: “Thời gian xem video Lên đến 30 giờ”. Tuyên bố gọi hoạt động bằng đúng nhãn "Thời gian xem video" mà Apple gắn cho 30 giờ và không thiếu chữ điều kiện nào của nhãn, nên cùng điều kiện (mục 6.8, luật chép đúng nhãn); quảng cáo bỏ "lên đến".
- Ghi chú: `chep_nhan=xem video`.
- Trước khảo sát: Đúng (D3), vì cấu hình hiểu "xem video" là xem video tải sẵn. Sau khảo sát (28/10): Lệch (`bo_dieu_kien`, D4), vì "xem video" coi như chưa nêu hoạt động, so với xem video trực tuyến 27 giờ. Từ 02/11 (QĐ15): Đúng theo luật chép đúng nhãn; hướng dẫn không coi nhãn "Thời gian xem video" là "ngoại tuyến" vì tài liệu không ghi chữ đó. Cách hiểu của người đọc (Q09) tính lại ở Bước 37.

**V25 · Chưa đủ thông tin · D1a.** Màn hình iPhone 17 sáng 3000 nit.
- Bằng chứng: `dt-apple-iphone17#005` “Độ sáng tối đa 1000 nit (tiêu chuẩn); độ sáng đỉnh 1600 nit (HDR); độ sáng đỉnh 3000 nit (ngoài trời)”
- Lý do: Tuyên bố không nêu chế độ hiển thị, và độ sáng điện thoại không có cách hiểu mặc định, nên chưa xác định được điều kiện. Không chọn chế độ theo con số của tuyên bố.
- Ghi chú: `mac_dinh=che_do_hien_thi` (nhãn dựa vào việc không có mặc định).
- Trước khảo sát: Lệch (`bo_dieu_kien`, D4), hiểu là chế độ tiêu chuẩn (1000 nit).

**V26 · Chưa đủ thông tin · D1a.** Màn hình Xiaomi 15T sáng 3200 nit.
- Bằng chứng: `dt-xiaomi-15t#004` “Độ sáng cực đại: 3200 nit trên 25% diện tích màn hình”; `dt-xiaomi-15t#037` “Màn hình siêu sáng 3.200 nit”; `dt-xiaomi-15t#038` “Dưới ánh sáng mạnh, màn hình sẽ tự động kích hoạt chế độ tăng mức sáng APL 25%”
- Lý do: Tài liệu chỉ công bố 3200 nit khi màn hình tự tăng sáng dưới ánh sáng mạnh, đo trên 25% diện tích. Tuyên bố không nêu chế độ, độ sáng điện thoại không có cách hiểu mặc định, nên chưa xác định được điều kiện.
- Ghi chú: `mac_dinh=che_do_hien_thi`.
- Trước khảo sát: Lệch (`bo_dieu_kien`, D4), hiểu là chế độ thông thường.

**V43 · Chưa đủ thông tin · D1a · trường hợp biên.** Xiaomi 15T có độ sáng cực đại 3200 nit.
- Bằng chứng: `dt-xiaomi-15t#004` “Độ sáng cực đại: 3200 nit trên 25% diện tích màn hình”; `dt-xiaomi-15t#037` “Màn hình siêu sáng 3.200 nit”; `dt-xiaomi-15t#038` “Dưới ánh sáng mạnh, màn hình sẽ tự động kích hoạt chế độ tăng mức sáng APL 25%”
- Lý do: Trang Xiaomi 15T chỉ có một con số độ sáng, nên chữ "cực đại" là kiểu giá trị tối đa, không phải tên chế độ (mục 6.5). Tuyên bố vì vậy không nêu chế độ, và độ sáng điện thoại không có cách hiểu mặc định, nên chưa xác định được điều kiện. Chép đúng chữ của hãng không bù được điều kiện bị bỏ.
- Ghi chú: `mac_dinh=che_do_hien_thi`.
- Trước khảo sát: Lệch (`bo_dieu_kien`, D4), chốt ngày 27/10 (mục 11.1).

### 9.6 Thêm ở Bước 16 (01/11/2026)

Ba ví dụ cho quy tắc mới của bản 2, lấy từ mẫu tập phát triển ngoài bộ thử.

**V49 · Lệch (`doi_dieu_kien`) · D4 · cụm phủ nhiều giá trị.** Apple Watch SE 3 dùng 32 giờ ở mọi chế độ.
- Bằng chứng: `dh-apple-watchse3#008` “Pin dùng cả ngày, lên đến 18 giờ khi sử dụng bình thường”, “Lên đến 32 giờ ở Chế Độ Nguồn Điện Thấp”
- Lý do: "Ở mọi chế độ" phủ cả chế độ thường và chế độ nguồn điện thấp, nên tuyên bố phải đúng ở chế độ kém thuận lợi nhất là chế độ thường (18 giờ). 32 giờ chỉ đạt ở chế độ nguồn điện thấp. Chế độ nguồn là điều kiện tuyên bố nêu rõ qua cụm phủ, nên loại là `doi_dieu_kien`, không phải `bo_dieu_kien` (mục 6.8).
- Ghi chú: `mac_dinh=hoat_dong`.

**V50 · Lệch (`doi_kieu_gia_tri`) · D2 · mức sàn.** Apple Watch SE 3 dùng được hơn 16 giờ khi sử dụng bình thường.
- Bằng chứng: `dh-apple-watchse3#008` “Pin dùng cả ngày, lên đến 18 giờ khi sử dụng bình thường”
- Lý do: "Hơn 16 giờ" đứng liền con số nên hứa một mức sàn, như "ít nhất 16 giờ"; tài liệu chỉ ghi mức tối đa "lên đến 18 giờ". 16 không cao hơn 18 nên dừng ở D2. Bỏ chữ "hơn" ("dùng được 16 giờ khi sử dụng bình thường") thì Đúng ở D3, vì 16 kém thuận lợi hơn 18.
- Ghi chú: `khang_dinh=hơn`; `mac_dinh=che_do_nguon`.

**V51 · Đúng · D3 · cụm tả hoàn cảnh của chế độ.** Xiaomi 15T sáng 3200 nit khi dùng dưới nắng.
- Bằng chứng: `dt-xiaomi-15t#004` “Độ sáng cực đại: 3200 nit trên 25% diện tích màn hình”; `dt-xiaomi-15t#037` “Màn hình siêu sáng 3.200 nit”; `dt-xiaomi-15t#038` “Dưới ánh sáng mạnh, màn hình sẽ tự động kích hoạt chế độ tăng mức sáng APL 25%”
- Lý do: "Dưới nắng" tả hoàn cảnh ánh sáng mạnh, đúng hoàn cảnh hãng ghi cho chế độ tự tăng sáng (mục 6.8, ý 2), nên tuyên bố nêu cùng chế độ với 3200 nit. Không nêu phần diện tích đo nên hiểu như hãng công bố (25%). 3200 nit khớp. So với V26: tuyên bố không nêu chế độ thì D1a.
- Ghi chú: `ngoai_cau_hinh=dưới nắng`. Cấu hình xếp "dưới nắng" vào chế độ ngoài trời (cách gọi kiểu Apple), chưa nối với chế độ tự tăng sáng của Xiaomi (mục 13).
- P: có thể ra D6 nếu đọc "dưới nắng" thành chế độ ngoài trời mà Xiaomi 15T không công bố.

## 10. Bảng phủ ví dụ

**Theo nhãn và dòng quyết định:**

| Nhãn | Số ví dụ | Dòng |
|---|---|---|
| Đúng | 16 (V01–V15, V51) | D3 |
| Sai | 5 (V16–V20) | D5 |
| Lệch điều kiện | 22 (V21–V24, V27–V42, V49, V50) | D4: 18; D2: 4 (V38–V40, V50) |
| Chưa đủ thông tin | 8 (V25, V26, V43–V48) | D1 (V45), D1a (V25, V26, V43, V46, V47), D1b (V48), D6 (V44) |

Số trên là sau Bước 16 (thêm V49–V51; V03 thành Đúng theo QĐ15 ngày 02/11). Sau khảo sát Bước 10, trước Bước 16: Đúng 14, Sai 5, Lệch 21, Chưa đủ thông tin 8. Trước khảo sát: Đúng 15, Sai 5, Lệch 23, Chưa đủ thông tin 5 (mục 9.5).

**Theo loại biến đổi** (mỗi loại ít nhất 2):

| Loại | Ví dụ |
|---|---|
| `bo_dieu_kien` | V21, V23, V24, V28, V32, V33, V34 |
| `doi_dieu_kien` | V22, V27, V29, V30, V31, V41, V42, V49 |
| `doi_bo_phan` | V18 (Sai), V35, V36 |
| `doi_phien_ban` | V14, V15 (cả hai Đúng: tập phát triển không có trang tách giá trị theo phiên bản, nên chưa có ví dụ Lệch đổi phiên bản) |
| `doi_kieu_gia_tri` | V37, V38, V39, V40, V50 |
| `doi_gia_tri` | V16, V17, V19, V20 |

**Các trường hợp đề cương và kế hoạch yêu cầu:**

| Trường hợp | Ví dụ |
|---|---|
| Đúng | V01–V15, V51 |
| Sai đối tượng | V17 (số của sản phẩm khác), V18 và V35, V36 (bộ phận khác) |
| Sai điều kiện | V21–V24, V27–V34, V41, V42, V49 |
| Thiếu bằng chứng | V45 (không có thuộc tính), V44 (không có giá trị ở điều kiện) |
| Điều kiện không có cách hiểu mặc định | V46 (mốc phần trăm), V25, V26, V43 (độ sáng điện thoại) |
| Xung đột bằng chứng | V48 |
| Điều kiện dạng số (≥ và ≤) | V02, V22 (bộ tiếp hợp); V06, V29 (độ sâu); V27 (phần diện tích); V20 (mốc 100%) |
| Điều kiện cấu hình chưa biết | V08 (ở tài liệu), V41, V51 (ở tuyên bố), V27 |
| Bỏ "lên đến" | V02, V03, V04, V09 (vẫn Đúng) |
| Chép đúng nhãn của tài liệu | V03 (Đúng); V24 (không trùng chữ nhãn, Lệch) |
| Từ khẳng định gắn với con số | V38, V39, V40 ("luôn"), V50 ("hơn") |
| Cụm phủ nhiều giá trị | V49 |
| Cụm chỉ sự liên tục, cụm tả hoàn cảnh (mục 6.8) | V07, V51 |
| Cùng con số ở nhiều đoạn | V08, V09, V10, V16, V17, V23, V26, V27, V31, V32, V35, V37, V38, V43, V44, V48, V51 |
| Watch SE 3 "đỉnh 1000 nit" so thẳng | V12 |
| Mặc định tai nghe: nghe nhạc, chống ồn bật | V10, V32, V38 |
| Mặc định đồng hồ: sử dụng bình thường, chế độ thường | V33, V39 |

**Theo nhóm:** điện thoại 25 (iPhone 17: 16; Xiaomi 15T: 9), tai nghe 14, đồng hồ 12 (cộng 51). Mỗi thuộc tính trong 16 thuộc tính có ít nhất một ví dụ, trừ sạc nhanh của tai nghe chỉ có ví dụ D1 (V45) vì Galaxy Buds3 Pro không công bố.

## 11. Ca đã chốt và rủi ro đã biết

### 11.1 Xiaomi 15T "độ sáng cực đại 3200 nit" (ví dụ 16 cũ ở T4.6)

Tuyên bố chép gần nguyên văn dòng "Độ sáng cực đại: 3200 nit trên 25% diện tích màn hình" (`dt-xiaomi-15t#004`). Bộ luật Bước 8 cho hai cách đọc:

- **Đọc theo chữ của cấu hình:** `cach_goi_theo_hang` của Xiaomi chỉ áp khi tài liệu dùng chữ đó để phân biệt từ hai giá trị trở lên. Trang Xiaomi 15T chỉ có một con số độ sáng (3200 nit ở cả `#004` và `#037`), nên "cực đại" là kiểu giá trị tối đa. Tuyên bố khi đó không nêu chế độ, hiểu là chế độ thông thường, và ra **Lệch** (`bo_dieu_kien`) như V26.
- **Đọc theo cách gọi của hãng:** "cực đại" là tên Xiaomi dùng cho mức sáng của chế độ tự tăng sáng (`#004` cùng `#038`). Tuyên bố dùng đúng chữ đó nên nêu cùng chế độ; phần 25% diện tích không nêu thì hiểu như hãng công bố. Kết quả **Đúng**, như ví dụ 16 cũ.

**Đã chốt ngày 27/10/2026: Lệch**, theo chữ của cấu hình (V43). Lý do: tuyên bố bỏ điều kiện mà con số cần, cụ thể là chế độ tự tăng sáng dưới ánh sáng mạnh. Dùng đúng chữ "cực đại" của hãng không bù được phần điều kiện bị bỏ, vì trên trang này chữ đó không gọi tên chế độ nào. Cấu hình giữ nguyên, nên V43 là kiểm thử hồi quy cho P như mọi ví dụ khác.

**Cập nhật 28/10/2026 sau khảo sát Bước 10:** độ sáng điện thoại không còn cách hiểu mặc định, nên tuyên bố không nêu chế độ chưa xác định được điều kiện. V43 đổi từ Lệch thành **Chưa đủ thông tin** (D1a, mục 9.5). Lý do của quyết định ngày 27/10 vẫn đúng: tuyên bố thiếu điều kiện mà con số cần, và chữ "cực đại" không bù được. Chỉ khác là thiếu điều kiện giờ dẫn tới "chưa xác định được" thay vì "hiểu là chế độ thông thường". Cả hai nhãn đều không phải Đúng, nên FAR không đổi.

### 11.2 Trùng số ngẫu nhiên ở D4

D4 tính mọi điều kiện khác của cùng thuộc tính, nên con số trùng giá trị của một hoạt động khác cũng ra Lệch (V42: 5 giờ trùng thời gian đàm thoại khi tắt chống ồn). Cách làm này đúng định nghĩa của đề cương và không ảnh hưởng FAR, vì Lệch cũng không phải Đúng. Rủi ro là hạ độ chính xác của nhãn Lệch. Con số trùng khác hoạt động cũng có thể do LLM lấy nhầm ô bên cạnh trong bảng thông số, tức đúng kiểu lỗi đề tài nhắm tới; chưa có số liệu.

**Đã chốt ở Bước 16 (01/11/2026):** giữ D4 tính mọi điều kiện khác. Ngưỡng xét lại đặt trước khi đếm:

- Sau khi gán lại lượt 2 của bộ thử, đếm các ca Lệch ở D4 mà tuyên bố **nêu rõ** một hoạt động và giá trị trùng thuộc một hoạt động khác (kiểu V42). Không đếm ca tuyên bố không nêu hoạt động (`bo_dieu_kien` theo hoạt động, kiểu V24): đó là ca bỏ điều kiện cốt lõi của đề tài, không phải trùng số tình cờ. Phạm vi này được làm rõ ngày 02/11/2026 (QĐ9), **sau khi** đã thấy số đếm theo chữ cũ trên phần iPhone 17 của bản Claude gán trước (7/13 ca D4, phần lớn là ca kiểu V03); ghi trong nhật ký Bước 16.
- Số ca này quá 1/4 số ca Lệch ở D4 thì xét lại ở Bước 27, trên toàn tập phát triển. Phương án khi xét lại: chỉ tính ở D4 các giá trị cùng hoạt động với tuyên bố, trùng số khác hoạt động thì dò tiếp D5, D6.
- Không đổi ngưỡng (1/4) sau khi đã thấy số đếm.

### 11.3 Cụm cấu hình chưa có, gặp ngay trong tập phát triển

| Cụm | Ở đâu | Hệ quả dự kiến với P | Ví dụ |
|---|---|---|---|
| "chênh lệch nhiệt độ ... 5K" | Chú thích kháng nước Xiaomi 15T (`#012`, `#035`) | D1a cho mọi tuyên bố kháng nước của Xiaomi 15T | V08 |
| "toàn màn hình" | Tuyên bố về phần diện tích đo | D1a thay vì Lệch | V27 |
| "chỉ dùng mạng di động" | Tuyên bố về đồng hồ bản di động | D1a thay vì Lệch | V41 |
| "ghép nối ... với điện thoại thông minh Galaxy ... với các cài đặt mặc định" | Chú thích thời lượng pin Buds3 Pro (`#038`) | Người gán coi là quy trình thử (ngữ cảnh). P có thể ra D1a cho mọi tuyên bố pin Buds3 Pro nếu bước trích xuất ghi cụm này vào `dieu_kien_khac` | Không có ví dụ riêng |
| "không ghép đôi với iPhone và có bật cảm biến nhịp tim" | Chú thích 7 giờ tập luyện ngoài trời của Watch SE 3 (`#008`) | Như trên | Không có ví dụ riêng |
| "dưới nắng" cho chế độ tự tăng sáng của Xiaomi | Tuyên bố về độ sáng Xiaomi 15T; cấu hình chỉ xếp cụm này vào chế độ ngoài trời | D6 hoặc D1a thay vì Đúng | V51 |

Các cụm này lấy từ tập phát triển nên được phép bổ sung vào cấu hình. Hai cụm "ghép nối …" và "không ghép đôi …" nên vào `ngu_canh_khong_quyet_dinh` của `chung.yaml`. Phiên thử độ bao phủ trên 3 sản phẩm ngoài 12 mẫu có thể thêm luật; khi đó đối chiếu lại mục 5, 6, phụ lục mục 13 và các ví dụ có ghi chú `ngoai_cau_hinh`.

### 11.4 Báo riêng các ca tài liệu mâu thuẫn (QĐ13, 02/11/2026)

Ở bộ thử, một dòng ghi nhầm trong bảng thông số của Galaxy Buds3 Pro ("bật ANC … 30" nằm dưới nhóm tắt ANC) quyết định nhãn của nhiều tuyên bố về tổng thời lượng pin. Khóa luận báo riêng: số tuyên bố dừng ở D1b, số tuyên bố có ghi chú `mau_thuan_khop_ca_hai`, và FAR, Recall nhãn Đúng của mọi hệ thống tính cả khi có và khi bỏ hai nhóm này (phân tích độ nhạy ở Bước 37).

## 12. Thay đổi so với 18 ví dụ ở T4.6

| T4.6 | Ở đây | Thay đổi |
|---|---|---|
| 1 | V01 | Giữ |
| 2 | V21 | Giữ nhãn; lý do nói rõ thiếu "lên đến" không phải lý do của nhãn |
| 3 | V25 | Đổi sau khảo sát Bước 10 (28/10): Lệch thành Chưa đủ thông tin (D1a), vì độ sáng điện thoại không còn cách hiểu mặc định |
| 4 | V05 | Giữ |
| 5 | V19 | Giữ |
| 6 | V09 | Giữ |
| 7 | V31 | Giữ |
| 8 | V32 | Giữ nhãn; lý do đổi từ "chế độ kém thuận lợi nhất" sang "chống ồn bật theo mặc định của hãng" (điểm 1 T10, tạm chốt 26/10) |
| 9 | V10 | Như ví dụ 8 |
| 10 | V16 | Giữ |
| 11 | V35 | Giữ nhãn; thêm V18 để phân biệt với tuyên bố "hộp sạc kháng nước" không nêu mã (Sai) |
| 12 | V38 | Giữ |
| 13 | V11 | Giữ |
| 14 | V33 | Giữ nhãn; lý do nêu cả hoạt động mặc định "sử dụng bình thường" |
| 15 | V39 | Giữ |
| 16 | V43 | Đổi nhãn: Đúng thành Lệch, chốt 27/10. Sau khi làm rõ điểm 12, "cực đại" gắn một giá trị duy nhất là kiểu giá trị, không mang theo chế độ (mục 11.1). Sau khảo sát Bước 10 (28/10): Chưa đủ thông tin (D1a) |
| 17 | V26 | Lý do nêu chế độ tự tăng sáng dưới ánh sáng mạnh (`#038`). Sau khảo sát Bước 10 (28/10): Lệch thành Chưa đủ thông tin (D1a) |
| 18 | V44, V42 | Đổi: 5 giờ trùng thời gian đàm thoại khi tắt chống ồn nên theo D4 ra Lệch (V42). Ví dụ D6 dùng 6,5 giờ (V44). Cấu hình đã biết "xuyên âm", nên P không còn dừng ở D1a |

## 13. Phụ lục: cụm diễn đạt trong cấu hình

Phụ lục chép đúng các cụm trong `data/cau_hinh/chung.yaml`, `dien_thoai.yaml`, `tai_nghe.yaml`, `dong_ho.yaml` (bản ngày 02/11/2026), sinh bằng script từ YAML, không gõ tay (`scripts/sinh_phu_luc_cum.py`). Cấu hình đổi thì sinh lại phụ lục và kiểm khớp, như bảng mục 5.

Cách dùng (mục 6.8):

- Cụm có ở đây thì là điều kiện đó (ý 1). So cụm dài nhất trước: "xem video trực tuyến" là `xem_video_truc_tuyen`, không phải `chua_ro_loai_video`.
- `tu_tai_lieu` là chữ có trong tài liệu tập phát triển; `hieu_biet_chung` là cách nói thường gặp, chưa có trong tài liệu.
- Cụm chưa có ở đây thì đọc theo nghĩa (ý 2), ghi `ngoai_cau_hinh=<cụm>`. Thiếu cụm trong phụ lục không phải lý do D1a cho nhãn chuẩn.
- Giá trị ghi "(chỉ phía tài liệu)" hay "(chỉ phía tuyên bố)" (khóa `phia`) chỉ đọc ở một phía. "Sử dụng liên tục" (`su_dung_lien_tuc`) là tên bài đo ở phía tài liệu Xiaomi 15T. Ở phía tuyên bố, "sử dụng liên tục", "dùng liên tục", "liên tục" (`chua_ro_hoat_dong`) không nêu hoạt động cụ thể: coi như chưa nêu, dùng cách hiểu mặc định (ý 3, V07).
- Giá trị ghi "(chỉ `<thuộc tính>`)" (khóa `chi_thuoc_tinh`) chỉ là điều kiện của các thuộc tính đó. "kèm hộp sạc", "tổng cộng"... (`kem_hop_sac`) chỉ là bộ phận kèm hộp sạc với thời lượng pin (ý 6); "có kèm hộp sạc 515 mAh" không phải bộ phận này.
- "sử dụng", "dùng" đứng riêng, như "liên tục", không nêu hoạt động cụ thể (`chua_ro_hoat_dong`, mọi nhóm; ý 3).
- "dưới nắng", "ngoài nắng", "ánh nắng", "dưới ánh nắng" nằm ở chế độ `ngoai_troi` (cách gọi kiểu Apple). Cụm phụ lục ứng với cách gọi chế độ trong cấu hình: tài liệu gọi chế độ sáng cao bằng tên khác (Xiaomi: `tu_tang_sang`, "Dưới ánh sáng mạnh") thì đọc theo ý 2 (V51). "ánh sáng mạnh" không có trong phụ lục; đọc theo ý 2, ghi `ngoai_cau_hinh`.

### 13.1 Dùng chung (`chung.yaml`)

| Nhóm cụm | Mục con | Chữ trong tài liệu (`tu_tai_lieu`) | Cách nói thường gặp (`hieu_biet_chung`) |
|---|---|---|---|
| Kiểu giá trị (`kieu_gia_tri`) | `toi_da` | "lên đến", "tối đa", "đến" | "up to", "tới" |
|  | `dien_hinh` | "typ", "typical" | "điển hình" |
|  | `dinh_muc` | – | "định mức", "rated" |
|  | `thich_ung` | "thích ứng" | – |
| Chữ gọi mức cao (`tu_goi_muc_cao`) | một giá trị: `toi_da`; nhiều giá trị: `che_do_theo_hang` | "tối đa", "đỉnh", "cực đại" | "peak" |
| Quan hệ của điều kiện dạng số (`cum_quan_he`) | `toi_thieu` | "trở lên", "hoặc cao hơn" | "tối thiểu", "ít nhất" |
|  | `toi_da` | "độ sâu tối đa", "tối đa 30 phút", "sâu tới" | "không quá" |
| Chỉ là ngữ cảnh (`ngu_canh_khong_quyet_dinh`) | | "phòng thí nghiệm", "tiền sản xuất", "phần mềm tiền phát hành", "kết quả thực tế", "không phải là các điều kiện vĩnh viễn", "không phải là điều kiện cố định", "cạn pin", "logo Apple xuất hiện" | "thử nghiệm nội bộ" |

Từ khẳng định (`tu_khang_dinh`), chỉ tính khi gắn với con số của giá trị (mục 6.2):

- Nhóm chắc chắn (`tu`): "luôn", "đảm bảo", "bảo đảm", "ít nhất", "mọi lúc".
- Nhóm mức sàn (`tu_muc_san`), chỉ khi đứng liền con số của giá trị: "hơn <số>", "trên <số>", "không dưới <số>", "<số> trở lên" (cách nói thường gặp, `hieu_biet_chung`).
- Bỏ qua khi có (`bo_qua_khi_co`): "không đảm bảo", "không được đảm bảo", "không bảo đảm", "không phải lúc nào", "không luôn".

Cụm phủ nhiều giá trị (`cum_phu.mau`, mục 6.8): "mọi điều kiện X", "mọi chế độ", "mọi hoạt động", "bất kể X", "dù A hay B", "cho cả A và B". Cách nói thường gặp (`hieu_biet_chung`); X là chữ chỉ điều kiện đi sau, A và B là hai giá trị được phủ. Không phải từ khẳng định. Điều kiện của tuyên bố là giá trị kém thuận lợi nhất trong các giá trị được phủ mà tài liệu công bố (`kem_thuan_loi_nhat`); Lệch thì loại `doi_dieu_kien`.

### 13.2 Điện thoại (`dien_thoai.yaml`)

| Điều kiện | Giá trị | Chữ trong tài liệu (`tu_tai_lieu`) | Cách nói thường gặp (`hieu_biet_chung`) |
|---|---|---|---|
| `hoat_dong` | `xem_video` | "Thời gian xem video" | "xem video tải sẵn", "xem video đã tải về", "xem video ngoại tuyến", "xem video offline" |
|  | `xem_video_truc_tuyen` | "xem video (trực tuyến)" | "xem video trực tuyến", "xem phim online", "streaming" |
|  | `chua_ro_loai_video` | – | "xem video", "xem phim" |
|  | `su_dung_lien_tuc` (chỉ phía tài liệu) | "Sử dụng liên tục" | – |
|  | `chua_ro_hoat_dong` (chỉ phía tuyên bố) | – | "sử dụng liên tục", "dùng liên tục", "liên tục", "sử dụng", "dùng" |
|  | `nghe_nhac` | – | "nghe nhạc" |
| `phien_ban` | `ten_san_pham` | – | – |
| `bo_tiep_hop` | `gia_tri_so` | "bộ tiếp hợp", "củ sạc", "Bộ sạc" | "cục sạc", "adapter" |
| `cach_sac` | `cap` | "cáp sạc USB-C" | "sạc có dây", "sạc dây" |
|  | `magsafe` | "MagSafe" | – |
|  | `khong_day` | "Sạc không dây", "Qi2" | – |
| `moc_phan_tram` | `gia_tri_so` | "Sạc lên đến 50%", "sạc đầy 100%" | "sạc đầy" |
| `che_do_hien_thi` | `tieu_chuan` | "(tiêu chuẩn)" | "bình thường" |
|  | `hdr` | "(HDR)" | "nội dung HDR" |
|  | `ngoai_troi` | "(ngoài trời)" | "dưới nắng", "ngoài nắng", "ánh nắng", "dưới ánh nắng" |
|  | `tu_tang_sang` | "Dưới ánh sáng mạnh", "tự động kích hoạt chế độ tăng mức sáng" | – |
| `dien_tich_do` | `gia_tri_so` | "25% diện tích", "APL 25%" | – |
| `kieu_tan_so` | `toi_da` | "Lên đến 120Hz", "tối đa 120Hz" | – |
|  | `thich_ung` | "tốc độ làm mới thích ứng" | "tần số quét thích ứng" |
| `loai_zoom` | `quang_hoc` | "quang học", "Telephoto 2x chất lượng quang học" | "optical", "telephoto" |
|  | `ky_thuat_so` | "kỹ thuật số" | "digital", "zoom số" |
| `dai_luong` | `do_phong_dai` | "Độ phóng đại" | – |
|  | `pham_vi` | "phạm vi thu phóng" | "dải zoom" |
| `che_do_camera` | `chup_anh` | – | "chụp ảnh", "khi chụp" |
|  | `quay_video` | "Quay Video" | "khi quay" |
| `do_sau` | `gia_tri_so` | "độ sâu tối đa 6 mét", "độ sâu 3 mét", "sâu tới 3 mét" | "ngâm", "dưới nước" |
| `thoi_gian_ngam` | `gia_tri_so` | "tối đa 30 phút" | – |
| `loai_nuoc` | `nuoc_ngot` | "nước ngọt tĩnh lặng" | – |
|  | `nuoc_khac` | "nước muối", "nước clo", "nước áp suất cao" | "nước biển", "hồ bơi" |
| `hoat_dong_bi_cam` | `di_bien_di_boi` | "đi biển", "đi bơi" | "bơi lội", "lặn" |
| `kieu_dung_luong` | `dien_hinh` | "(thông thường)", "(typ)" | "điển hình" |
|  | `dinh_muc` | – | "định mức" |

Cách gọi độ sáng theo hãng (`thuoc_tinh.do_sang.cach_goi_theo_hang`), chỉ áp khi chữ phân biệt từ hai giá trị trở lên (mục 6.5):

| Hãng | Chữ | Chế độ |
|---|---|---|
| Apple | "tối đa" | `tieu_chuan` |
| Apple | "đỉnh" | `hdr`, `ngoai_troi` |
| Xiaomi | "cực đại" | `tu_tang_sang` |

### 13.3 Tai nghe (`tai_nghe.yaml`)

| Điều kiện | Giá trị | Chữ trong tài liệu (`tu_tai_lieu`) | Cách nói thường gặp (`hieu_biet_chung`) |
|---|---|---|---|
| `che_do_chong_on` | `bat` | "bật ANC", "Tính năng ANC Bật", "BẬT Tính năng ANC" | "bật chống ồn", "bật khử ồn", "khử tiếng ồn chủ động", "chống ồn chủ động" |
|  | `tat` | "tắt ANC", "Tính năng ANC Tắt", "Tắt Tính năng ANC" | "tắt chống ồn", "tắt khử ồn" |
|  | `xuyen_am` | "Ambient", "Môi trường xung quanh" | "xuyên âm", "âm thanh xung quanh" |
| `bo_phan` | `tai_nghe` | "tai nghe" | "riêng tai nghe", "mỗi lần sạc" |
|  | `hop_sac` | "hộp sạc" | "case" |
|  | `kem_hop_sac` (chỉ `thoi_luong_pin`) | "Tổng thời gian", "tai nghe và hộp tai nghe" | "kèm hộp sạc", "tính cả hộp sạc", "cùng hộp sạc", "tổng cộng", "kết hợp hộp sạc" |
| `hoat_dong` | `nghe_nhac` | "phát nhạc", "Thời gian phát" | "nghe nhạc" |
|  | `dam_thoai` | "đàm thoại" | "gọi điện", "nghe gọi", "thời gian thoại" |
|  | `chua_ro_hoat_dong` (chỉ phía tuyên bố) | – | "sử dụng liên tục", "dùng liên tục", "liên tục", "sử dụng", "dùng" |
| `so_phut_sac` | `gia_tri_so` | – | "sạc nhanh", "phút sạc" |
| `do_sau` | `gia_tri_so` | "1 mét" | "ngâm", "dưới nước" |
| `thoi_gian_ngam` | `gia_tri_so` | "tối đa 30 phút" | – |
| `loai_nuoc` | `nuoc_ngot` | "nước ngọt" | – |
|  | `nuoc_khac` | – | "nước biển", "nước clo", "hồ bơi" |
| `hoat_dong_bi_cam` | `tam_bien_be_boi` | "tắm biển", "bể bơi" | "đi bơi", "bơi lội" |

### 13.4 Đồng hồ (`dong_ho.yaml`)

| Điều kiện | Giá trị | Chữ trong tài liệu (`tu_tai_lieu`) | Cách nói thường gặp (`hieu_biet_chung`) |
|---|---|---|---|
| `che_do_nguon` | `thuong` | – | "chế độ thường" |
|  | `nguon_thap` | "Chế Độ Nguồn Điện Thấp" | "tiết kiệm pin", "nguồn điện thấp" |
| `hoat_dong` | `su_dung_binh_thuong` | "sử dụng bình thường" | "dùng bình thường", "dùng hằng ngày" |
|  | `tap_luyen` | "tập luyện ngoài trời" | "tập luyện", "tập thể thao" |
|  | `theo_doi_giac_ngu` | "theo dõi giấc ngủ" | – |
|  | `chua_ro_hoat_dong` (chỉ phía tuyên bố) | – | "sử dụng liên tục", "dùng liên tục", "liên tục", "sử dụng", "dùng" |
| `phien_ban` | `gps` | "(GPS)" | – |
|  | `gps_cellular` | "(GPS + Cellular)" | "bản di động", "eSIM" |
| `bo_tiep_hop` | `gia_tri_so` | "Bộ Tiếp Hợp Nguồn USB-C 20W" | "cục sạc", "củ sạc" |
| `cap_sac` | `cap_di_kem` | "Cáp Sạc Nhanh Từ Tính" | "cáp đi kèm" |
| `moc_phan_tram` | `gia_tri_so` | "Sạc lên đến 80%" | "sạc đầy" |
| `so_phut_sac` | `gia_tri_so` | "Sạc 15 phút", "Sạc 8 phút" | – |
| `chuan_do_sau` | `iso_22810` | "ISO 22810", "độ sâu 50m" | "5ATM", "WR50" |
| `hoat_dong_cho_phep` | `duoc_phep` | "bơi lội trong bể bơi", "dưới biển" | – |
|  | `bi_cam` | "lặn với bình dưỡng khí", "lướt ván" | "lặn sâu" |
| `che_do_hien_thi` | `thong_thuong` | – | "bình thường" |
