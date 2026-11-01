# Hướng dẫn gán nhãn bốn lớp

**Bản:** 1 · **Ngày:** 27/10/2026 · **Bước:** 9 · **Chốt bản 2:** Bước 16, sau bộ thử.

**Căn cứ:** đề cương bản cuối (11/10/2026); T4 trong `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md`; bộ luật Bước 8 ở `data/cau_hinh/` (commit `ab6146c`) và bảng bao phủ `data/cau_hinh/bao_phu_dieu_kien.md`.

**Dùng cho:** người gán nhãn chuẩn (Bước 13, 20, 24, 32); đặc tả của bộ quyết định trong P (Bước 27), nên mọi ví dụ ở mục 9 là kiểm thử hồi quy; phần hướng dẫn trong câu lệnh của đối chứng B2.

**Phạm vi ví dụ:** chỉ 4 mẫu tập phát triển: `dt-apple-iphone17`, `dt-xiaomi-15t`, `tn-samsung-buds3pro`, `dh-apple-watchse3`. Tệp này không chứa trang, con số hay tên mẫu của tập kiểm tra, vì tệp đi vào câu lệnh của B2.

**Phần chưa chắc:** cách hiểu mặc định ở mục 5 đã đối chiếu với khảo sát Bước 10 (10 người, 28/10/2026; mục 5.1). Mẫu nhỏ và lệch về người học công nghệ thông tin, nên các ví dụ có ghi chú `mac_dinh` được tính lại ở phân tích độ nhạy Bước 37.

## 1. Quy trình ngắn

1. Tách bài quảng cáo thành tuyên bố (mục 2).
2. Tìm trong tài liệu của mẫu các thông số cùng sản phẩm và thuộc tính với tuyên bố (mục 4).
3. Xác định điều kiện của tuyên bố: điều kiện nêu rõ giữ nguyên, điều kiện không nêu lấy cách hiểu mặc định (mục 5, 6).
4. Đi lần lượt D1 → D6, dừng ở dòng đầu tiên thỏa (mục 7).
5. Ghi nhãn, loại biến đổi, bằng chứng, lý do, ghi chú và số giây đã gán (mục 8).

## 2. Tách tuyên bố

- Mỗi tuyên bố chỉ có **một thuộc tính và một giá trị**. "Pin 6 giờ, sạc đầy trong 1 giờ" tách thành hai tuyên bố.
- **Giữ ngữ cảnh:** tên sản phẩm, phiên bản, bộ phận và điều kiện nằm ở câu trước hoặc câu sau phải đưa vào tuyên bố. Thay "tai nghe này", "máy" bằng tên sản phẩm.
- **Giữ nguyên chữ của quảng cáo** cho điều kiện và kiểu giá trị: không thêm điều kiện quảng cáo không nói, không bỏ "luôn", "lên đến", "định mức".
- **Chỉ giữ tuyên bố có thuộc tính trong cấu hình** (16 thuộc tính):
  - Điện thoại: thời lượng pin, sạc nhanh, công suất sạc, độ sáng, tần số quét, zoom, kháng nước, dung lượng pin.
  - Tai nghe: thời lượng pin, sạc nhanh, kháng nước, dung lượng pin.
  - Đồng hồ: thời lượng pin, sạc nhanh, kháng nước, độ sáng.
- **Bỏ:** khối lượng, kích thước, phiên bản Bluetooth, độ sáng tối thiểu, độ bền pin theo chu kỳ sạc; tuyên bố cảm tính ("pin trâu", "sáng rực"); so sánh với sản phẩm khác hoặc đời trước; giá và khuyến mãi; tuyên bố không có con số hay mã kiểm được, trừ khẳng định có/không ("hộp sạc cũng kháng nước").

| Câu trong quảng cáo | Tuyên bố sau khi tách | Ghi chú |
|---|---|---|
| "Galaxy Buds3 Pro cho bạn 6 giờ nghe nhạc khi bật chống ồn, tổng cộng 26 giờ cùng hộp sạc." | (1) Galaxy Buds3 Pro nghe nhạc 6 giờ khi bật chống ồn. (2) Galaxy Buds3 Pro nghe nhạc tổng 26 giờ kèm hộp sạc khi bật chống ồn. | Vế 2 mượn "nghe nhạc", "bật chống ồn" từ vế 1 |
| "Chỉ cần củ sạc 40W. iPhone 17 lấy lại 50% pin sau 20 phút." | iPhone 17 sạc 50% trong 20 phút với củ sạc 40W. | Điều kiện ở câu trước được đưa vào |
| "Apple Watch SE 3 có màn hình Luôn Bật sáng 1000 nit, kháng nước 50 m." | (1) Apple Watch SE 3 có độ sáng 1000 nit. (2) Apple Watch SE 3 chống nước 50 m. | "Luôn Bật" là tên tính năng, không phải tuyên bố |
| "Xiaomi 15T mỏng chỉ 7,5mm, pin 5500mAh trâu hơn đời trước." | Xiaomi 15T có pin 5500mAh. | Bỏ độ dày (ngoài phạm vi) và phần so với đời trước |

## 3. Bốn nhãn

Định nghĩa chép nguyên văn đề cương:

| Nhãn | Mã | Định nghĩa |
|---|---|---|
| **Đúng** | `DUNG` | Tài liệu có thông số cùng sản phẩm, thuộc tính và điều kiện với tuyên bố, giá trị khớp và kiểu giá trị không bị đổi. |
| **Sai** | `SAI` | Tài liệu có thông số cùng sản phẩm và thuộc tính, nhưng giá trị của tuyên bố mâu thuẫn với giá trị công bố ở điều kiện của tuyên bố hoặc thuận lợi hơn mọi giá trị được công bố, đồng thời không trùng giá trị nào ở điều kiện khác. |
| **Lệch điều kiện** | `LECH` | Giá trị trong tuyên bố trùng giá trị được công bố ở một điều kiện khác với điều kiện mà tuyên bố nêu hoặc được hiểu thông thường (bỏ hoặc đổi chế độ, bộ phận, phụ kiện, phiên bản, điều kiện đo), hoặc tuyên bố biến mức tối đa "lên đến" thành mức chắc chắn đạt. |
| **Chưa đủ thông tin** | `CHUA_DU` | Kho tài liệu không có thông số cùng sản phẩm và thuộc tính, không công bố giá trị ở điều kiện mà tuyên bố nêu, hoặc ghi mâu thuẫn. |

Hai khái niệm dùng chung:

- **Khớp giá trị:** bằng giá trị công bố sau chuẩn hóa, hoặc **kém thuận lợi hơn** giá trị đó (nêu thời lượng pin thấp hơn, thời gian sạc lâu hơn), vì không gây hiểu nhầm có lợi cho người bán. Hướng thuận lợi của từng thuộc tính ở mục 6.1; mã IP so theo mục 6.6.
- **Điều kiện của tuyên bố:** điều kiện nêu rõ; điều kiện bắt buộc nào không nêu thì lấy cách hiểu mặc định ở mục 5.

## 4. Tài liệu nào là bằng chứng

**Được dùng:** `noi_dung` và `chu_thich` của các đoạn trong `data/nguon/<ma_mau>/doan.jsonl`, gồm cả trang chính (`url`) và trang bổ sung (`bo_sung`). Chú thích có giá trị như nội dung chính: bộ tiếp hợp 20W của Apple Watch SE 3 và "ANC được bật theo mặc định" của Galaxy Buds3 Pro chỉ nằm trong chú thích.

**Không dùng:**

- Menu, đường dẫn, đánh giá của người dùng.
- Cột của sản phẩm khác trong bảng so sánh. Đoạn `tn-samsung-buds3pro#042` có ba cột Buds3 Pro, Buds3, Buds FE; chỉ cột Buds3 Pro là bằng chứng.
- Hiểu biết riêng của người gán về sản phẩm, kết quả đo bên ngoài, trang của mẫu khác.

**Chú thích chỉ là ngữ cảnh**, không làm đổi nhãn: "phòng thí nghiệm", "thử nghiệm nội bộ", "thiết bị tiền sản xuất", "phần mềm tiền phát hành", "kết quả thực tế có thể khác", "phụ thuộc cấu hình mạng, cài đặt", "khả năng chống nước không phải vĩnh viễn", quy trình đo chuẩn ("thử với thiết bị cạn pin", "tính giờ từ khi logo Apple xuất hiện"), và kịch bản định nghĩa một hoạt động (300 lần xem giờ, 90 thông báo... của "sử dụng bình thường" trên Watch). Tiêu chí: điều kiện chỉ tham gia quyết định khi đổi điều kiện thì con số đổi và người mua không tự suy ra được.

**Ba trạng thái của một điều kiện:**

| Trạng thái | Khi nào | Xử lý |
|---|---|---|
| Không áp dụng | Có bằng chứng điều kiện không áp dụng cho trường hợp đang xét. Ví dụ trang Watch SE 3 có hai phiên bản và hai cỡ vỏ nhưng ghi chung một thời lượng pin | Không đòi điều kiện đó khớp. Không suy "không áp dụng" từ việc tài liệu im lặng |
| Không nêu | Quảng cáo không nói điều kiện | Dùng cách hiểu mặc định ở mục 5, ghi `mac_dinh` vào ghi chú. Không nêu không có nghĩa tự động Lệch |
| Chưa xác định | Không đủ căn cứ xác định điều kiện | Chưa đủ thông tin (D1a), ghi nguyên nhân |

**Tài liệu mâu thuẫn hoặc ghi nhầm:** gán Chưa đủ thông tin ở D1b, đặt `tai_lieu_mau_thuan = true`. Người gán không tự sửa chỗ ghi nhầm của hãng, kể cả khi đoán được hãng định ghi gì (ví dụ V48).

## 5. Cách hiểu mặc định khi tuyên bố không nêu điều kiện

Nguyên tắc của đề cương: hiểu như người mua thông thường, **bộ phận chính, không mua thêm phụ kiện**. Bảng dưới chép đúng `hieu_thong_thuong` trong 3 tệp cấu hình; cột cuối là khóa trong YAML để đối chiếu. Dòng có dấu * đã đối chiếu với khảo sát Bước 10 (mục 5.1).

| Nhóm | Thuộc tính | Điều kiện | Không nêu thì hiểu là | Khóa cấu hình |
|---|---|---|---|---|
| Điện thoại | Thời lượng pin (`thoi_luong_pin`) | Hoạt động* | Hoạt động kém thuận lợi nhất trong các hoạt động hãng công bố (iPhone 17: xem video trực tuyến, 27 giờ). "Xem video" không kèm "tải sẵn" hay "trực tuyến" cũng tính là chưa nêu hoạt động | `hoat_dong: kem_thuan_loi_nhat` |
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

Ba ý của bảng hay bị hiểu nhầm:

- **"Kém thuận lợi nhất"** chỉ dùng cho hoạt động của điện thoại: tuyên bố không nêu hoạt động phải đúng ở hoạt động kém nhất hãng công bố. Tai nghe và đồng hồ có mặc định riêng (nghe nhạc, chống ồn bật; sử dụng bình thường, chế độ thường).
- **"Không mua thêm"** nghĩa là chỉ có đồ trong hộp. Con số cần bộ sạc bán riêng mà tuyên bố không nêu bộ sạc thì Lệch, dù tuyên bố chép đúng con số (V21, V23, V34).
- **"Không có mặc định"** nghĩa là tuyên bố phải tự nêu điều kiện đó. Không nêu thì người gán cũng không đoán, gán Chưa đủ thông tin ở D1a (V46; độ sáng điện thoại: V25).

### 5.1 Đối chiếu với khảo sát Bước 10

Khảo sát 10 người ngày 27–28/10/2026 (`ket_qua/khao_sat_cach_hieu.md`; 8 người học hoặc làm công nghệ thông tin). Quy tắc đặt trước: quá nửa người đọc hiểu khác cấu hình thì sửa.

| Cách hiểu trong bảng trên | Hiểu khác | Quyết định |
|---|---|---|
| Điện thoại, hoạt động: kém thuận lợi nhất | 1/10 | Giữ |
| "Xem video" là xem video tải sẵn (cách diễn đạt) | 9/10 | **Sửa**: coi như chưa nêu hoạt động (V03) |
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
- **Bỏ "lên đến" vẫn khớp.** "Nghe nhạc 6 giờ" khớp "lên đến 6 giờ". Lý do ghi thêm `(quảng cáo bỏ "lên đến")` nhưng không đổi nhãn. Căn cứ: báo cáo gốc FTC 2012 cho thấy quảng cáo "up to 47%" và "47%" không khác nhau có ý nghĩa thống kê về cách người đọc hiểu; đề tài so quảng cáo với tài liệu, không đo hiệu năng thực tế.
- **Từ khẳng định** ("luôn", "đảm bảo", "bảo đảm", "ít nhất", "mọi lúc") cho một mức không cao hơn mức "lên đến" ở cùng điều kiện thì Lệch ở D2. Các từ này hứa một mức sàn mà tài liệu không hứa. Mức khẳng định cao hơn mức "lên đến" thì bỏ qua D2, xét tiếp D3–D6.
  - Chỉ xét từ nằm trong câu chứa giá trị. "Màn hình Luôn Bật", "Luôn kết nối" là tên tính năng.
  - Bỏ qua dạng phủ định: "không đảm bảo", "không được đảm bảo", "không bảo đảm", "không phải lúc nào", "không luôn".
  - "Tối thiểu" chưa tính là từ khẳng định, vì trùng "độ sáng tối thiểu".
- **Tuyên bố ghi rõ một kiểu khác tài liệu** (ví dụ "định mức" cho con số điển hình) thì kiểu giá trị bị đổi: không thể Đúng ở D3, và được xét như khác điều kiện ở D4 (V37).

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

"Sạc đầy" hiểu là mốc 100%.

### 6.4 Chọn con số để so khi tuyên bố không nêu điều kiện

| Tài liệu của mẫu | Cách so | Ví dụ |
|---|---|---|
| Chỉ một con số cho thuộc tính (cùng bộ phận), không kèm cụm điều kiện nào trong toàn bộ tài liệu | So thẳng; lý do ghi "tài liệu không nêu điều kiện" | V12, Watch SE 3 "Độ sáng đỉnh 1000 nit" |
| Nhiều con số, mỗi số ghi rõ điều kiện; hoặc một con số kèm điều kiện | So với con số ứng với cách hiểu mặc định | V32, V24 |
| Không xác định được con số nào ứng với tuyên bố, kể cả khi điều kiện không có cách hiểu mặc định | Chưa đủ thông tin (D1a) | V47, V25, V26 |
| Con số kèm điều kiện mà cấu hình chưa biết | Người gán xử lý theo mục 6.7; hệ thống ra D1a | V08 |

### 6.5 Độ sáng: chữ "tối đa", "đỉnh", "cực đại"

- Chữ dùng để **phân biệt từ hai giá trị trở lên** là chế độ hiển thị, đọc theo cách gọi của hãng:
  - Apple (iPhone 17): "tối đa" là chế độ tiêu chuẩn; "đỉnh" là HDR hoặc ngoài trời. Tuyên bố iPhone chỉ ghi "đỉnh" mà không nói chế độ thì D1a (V47).
  - Xiaomi: "cực đại" là chế độ tự tăng sáng dưới ánh sáng mạnh, đo trên 25% diện tích. Trang Xiaomi 15T chỉ có một con số độ sáng, nên "cực đại" ở đây là kiểu giá trị tối đa; tuyên bố "độ sáng cực đại 3200 nit" vì vậy không nêu chế độ (V43, mục 11.1).
- **Tuyên bố không nêu chế độ** (không có chữ nào ở trên, hoặc chữ chỉ là kiểu giá trị): độ sáng điện thoại không có cách hiểu mặc định (khảo sát Bước 10), nên D1a (V25, V26, V43). Riêng tài liệu chỉ có một con số không kèm điều kiện thì vẫn so thẳng (mục 6.4, V12).
- Chữ **gắn với một giá trị duy nhất** là kiểu giá trị tối đa, không phải chế độ, áp cho mọi hãng (Watch SE 3 "Độ sáng đỉnh 1000 nit", V12).
- "Độ sáng tối thiểu" là đại lượng khác, ngoài phạm vi.

### 6.6 Kháng nước: mã IP và ISO 22810

- **Mã IP** so theo nhánh của IEC 60529: chữ số bụi 0–6 xếp thành thang, cao hơn tốt hơn; chữ số nước tách hai nhánh 0–6 (tia nước) và 7–8 (ngâm), 8 khắc nghiệt hơn 7, chỉ so trong cùng nhánh; khác nhánh thì không khớp. Chữ "X" (IPX7) nghĩa là không công bố chữ số bụi, không xét. Ví dụ với máy IP68: tuyên bố IP67 khớp (cùng nhánh ngâm, kém thuận lợi hơn); với máy IP57: tuyên bố IP58 thuận lợi hơn nên Sai.
- **Đồng hồ theo ISO 22810:** quy về mét (5ATM = WR50 = 50 m; 10ATM = 100 m), cao hơn tốt hơn.
- **Điều kiện thử** (độ sâu, thời gian, loại nước) không nêu thì hiểu như hãng công bố. Quảng cáo nêu nước biển, nước clo, hồ bơi khi hãng chỉ thử nước ngọt, hoặc gợi ý hoạt động hãng khuyến cáo không dùng (lặn với bình dưỡng khí, tắm biển), là đổi điều kiện.
- **Bộ phận:** hộp sạc Galaxy Buds3 Pro không kháng nước. Tuyên bố gán mã IP57 cho hộp sạc trùng giá trị của tai nghe nên Lệch ở D4 (V35); tuyên bố chỉ nói "hộp sạc kháng nước" không trùng mã nào nên Sai ở D5 (V18).

### 6.7 Điều kiện ngoài cấu hình

Nhãn chuẩn **không** theo giới hạn của cấu hình. Gặp cụm điều kiện mà mục 5 và cấu hình không có, ở tuyên bố hay ở tài liệu, người gán làm như sau:

1. Đọc tài liệu, kể cả chú thích, để biết điều kiện đó nghĩa là gì; xếp vào một trong sáu loại (chế độ hoạt động, bộ phận, phụ kiện, điều kiện đo, phiên bản, kiểu giá trị). Không xếp được thì ghi `ngoai_sau_loai=<cụm>`.
2. Quyết định điều kiện đó tham gia quyết định nhãn hay chỉ là ngữ cảnh, theo tiêu chí ở mục 4. Chỉ là ngữ cảnh thì bỏ qua.
3. Điều kiện quyết định mà tuyên bố không nêu: dùng nguyên tắc chung. Bộ phận chính; không mua thêm phụ kiện; điều kiện đo, điều kiện thử như hãng công bố; chế độ mặc định của máy nếu hãng ghi; chế độ người dùng tự chọn mà hãng không ghi mặc định thì lấy chế độ kém thuận lợi nhất. Nguyên tắc vẫn không chỉ ra được cách hiểu thì D1a, ghi rõ vì sao.
4. Gán nhãn theo D1–D6 như bình thường, ghi `ngoai_cau_hinh=<cụm>` vào ghi chú. Các ca này được thống kê riêng ở Bước 37–38: hệ thống thường ra D1a ở đây, và chỗ lệch giữa đầu ra với nhãn chuẩn là giới hạn bao phủ của cấu hình, không phải lý do sửa nhãn chuẩn.

Quy tắc 3 cho chế độ người dùng tự chọn là tạm chốt cho người gán, xem lại ở Bước 16. Hệ thống có luật tương ứng (`luat_chung_cho_nhieu_gia_tri` trong `chung.yaml`) nhưng đang tắt, chọn bật hay tắt ở Bước 33.

## 7. Thứ tự quyết định D1–D6

Đi từ trên xuống, **dừng ở dòng đầu tiên thỏa**.

| Dòng | Kiểm tra | Nhãn | Lưu ý cho người gán |
|---|---|---|---|
| D1 | Tài liệu không có thông số cùng sản phẩm và thuộc tính | Chưa đủ thông tin | Con số của sản phẩm khác trong cùng trang không tính (V17) |
| D1a | Không xác định được điều kiện của tuyên bố; hoặc giá trị khớp trong tài liệu kèm điều kiện lạ | Chưa đủ thông tin | Người gán chỉ dùng khi chính hướng dẫn không cho xác định điều kiện: thuộc tính không có mặc định (mốc phần trăm, số phút sạc), chữ trỏ nhiều chế độ (iPhone "đỉnh"), hoặc mục 6.7 vẫn không giải được. Cấu hình chưa biết một cụm không phải lý do D1a cho nhãn chuẩn |
| D1b | Tài liệu ghi hai giá trị khác nhau cho cùng sản phẩm, thuộc tính và điều kiện của tuyên bố | Chưa đủ thông tin, `tai_lieu_mau_thuan = true` | Áp dụng cả khi con số của tuyên bố trùng một trong hai giá trị |
| D2 | Từ khẳng định cho một mức không cao hơn mức "lên đến" ở cùng điều kiện | Lệch (`doi_kieu_gia_tri`) | Mục 6.2 |
| D3 | Có thông số cùng điều kiện và giá trị khớp | Đúng | Khớp là bằng (trong 1%) hoặc kém thuận lợi hơn |
| D4 | Giá trị của tuyên bố bằng giá trị công bố ở một điều kiện khác | Lệch | Tính mọi điều kiện khác của cùng sản phẩm và thuộc tính, kể cả hoạt động khác (V42) |
| D5 | Giá trị mâu thuẫn với giá trị ở cùng điều kiện, hoặc thuận lợi hơn mọi giá trị công bố cho cùng bộ phận và phiên bản | Sai | "Mọi giá trị" tính theo bộ phận: "nghe nhạc 8 giờ" là Sai vì thuận lợi hơn mọi giá trị của tai nghe, dù tổng kèm hộp sạc lớn hơn 8 giờ |
| D6 | Còn lại: tài liệu không công bố giá trị ở điều kiện tuyên bố nêu | Chưa đủ thông tin | |

D1a và D1b không có trong chuỗi D của đề cương nhưng lấy từ chỗ khác của đề cương (câu "nếu vẫn không xác định được điều kiện thì kết luận Chưa đủ thông tin" ở Nội dung 2; vế "hoặc ghi mâu thuẫn" trong định nghĩa nhãn). Hai dòng đặt trước D2 để không bao giờ dẫn tới Đúng.

## 8. Ghi nhãn

Mỗi tuyên bố một dòng trong `data/nhan/*.jsonl`:

```json
{"id": "tb-00042", "nhan": "LECH", "dong_d": "D4", "loai": "doi_dieu_kien",
 "bang_chung": ["tn-samsung-buds3pro#044"], "trich": "Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7",
 "ly_do": "7 giờ chỉ đạt khi tắt chống ồn; tuyên bố ghi bật chống ồn.",
 "nguoi_gan": "phuoc", "luot": 1, "giay": 95, "tai_lieu_mau_thuan": false, "ghi_chu": ""}
```

`dong_d`: dòng D đã dừng ở mục 7; nhãn phải khớp với dòng (D1, D1a, D1b, D6: Chưa đủ thông tin; D2, D4: Lệch; D3: Đúng; D5: Sai).

**Bằng chứng và câu trích.** Ghi mã đoạn `<ma_mau>#<số>` và chép **nguyên văn** từ `noi_dung` hoặc `chu_thich` của đoạn. Số chú thích của trang hãng đã được bỏ khỏi `noi_dung` (bản gốc ở `noi_dung_goc`), nên câu trích chép theo chữ hiển thị. Hệ thống chỉ chuẩn hóa khoảng trắng và dấu câu khi kiểm câu trích. Nhãn Lệch ghi đoạn chứa giá trị trùng; nhãn Sai ghi đoạn chứa giá trị ở cùng điều kiện; D1 để trống.

**Loại biến đổi** (`loai`):

| Mã | Khi nào |
|---|---|
| `bo_dieu_kien` | Tuyên bố không nêu điều kiện; cách hiểu mặc định khác điều kiện của con số |
| `doi_dieu_kien` | Tuyên bố nêu rõ chế độ, phụ kiện hoặc điều kiện đo khác điều kiện của con số, kể cả điều kiện dạng số không thỏa |
| `doi_bo_phan` | Tuyên bố nêu rõ bộ phận khác |
| `doi_phien_ban` | Tuyên bố nêu rõ phiên bản khác |
| `doi_kieu_gia_tri` | Dòng D2, hoặc tuyên bố ghi rõ kiểu giá trị khác tài liệu |
| `doi_gia_tri` | Nhãn Sai vì con số sai |

- Nhãn Lệch luôn có loại. Nhãn Sai ghi `doi_gia_tri`; riêng tuyên bố Sai vì gán cho bộ phận hoặc phiên bản khác mà không trùng giá trị nào thì ghi `doi_bo_phan` hoặc `doi_phien_ban` (V18). Nhãn Đúng và Chưa đủ thông tin để trống.
- Con số trùng nhiều giá trị ở điều kiện khác: so với giá trị khác tuyên bố ở ít điều kiện nhất. Khác ở từ hai điều kiện: ưu tiên điều kiện tuyên bố nêu rõ (mã `doi_...`) hơn điều kiện lấy mặc định (`bo_dieu_kien`); nêu rõ nhiều điều kiện thì ưu tiên bộ phận, rồi phiên bản, rồi kiểu giá trị, rồi các điều kiện còn lại. Lý do ghi đủ các điều kiện khác nhau. Quy tắc này tạm chốt, chốt cùng hàm `loai_bien_doi` ở Bước 27.

**Lý do** viết một câu, nêu rõ điều kiện nào bị bỏ hoặc bị đổi. Dùng mẫu câu của hệ thống (T5.6) khi được:

| Dòng | Mẫu câu |
|---|---|
| D1 | "Tài liệu của {sản phẩm} không có thông số {thuộc tính}." |
| D1a | "Chưa xác định được điều kiện của tuyên bố: “{cụm điều kiện}”." |
| D1b | "Tài liệu ghi hai giá trị khác nhau cho {thuộc tính} ở {điều kiện}: “{trích 1}” và “{trích 2}”." |
| D2 | "Tài liệu ghi mức tối đa: “{trích}”; tuyên bố viết thành mức chắc chắn đạt." |
| D3 | "Khớp với tài liệu: “{trích}”." |
| D4 | "Giá trị {giá trị} {đơn vị} chỉ đạt khi {điều kiện trong tài liệu}; tuyên bố {nêu hoặc được hiểu là} {điều kiện của tuyên bố}. Nguồn: “{trích}”." |
| D5 | "Tài liệu ghi {giá trị trong tài liệu} {đơn vị} ở {điều kiện}; tuyên bố ghi {giá trị}." |
| D6 | "Tài liệu không công bố {thuộc tính} ở {điều kiện của tuyên bố}." |

**Ghi chú** (`ghi_chu`), nhiều mục cách nhau bằng "; ":

| Mã | Khi nào ghi | Dùng ở |
|---|---|---|
| `mac_dinh=<điều kiện>` | Nhãn dựa vào cách hiểu mặc định chọn giữa nhiều giá trị (kém thuận lợi nhất, chống ồn bật, tai nghe, nghe nhạc, chế độ thường, tiêu chuẩn, quang học, không mua thêm, sạc bằng cáp...); liệt kê các điều kiện, cách nhau bằng dấu phẩy. Không ghi cho mặc định "như hãng công bố", và không ghi cho điều kiện không áp dụng (ví dụ cách sạc khi máy không có sạc không dây) | Phân tích độ nhạy ở Bước 37: tính lại khi mọi nhãn phụ thuộc mặc định đổi thành Chưa đủ thông tin |
| `ngoai_cau_hinh=<cụm>` | Điều kiện cấu hình chưa biết, người gán tự xác định theo mục 6.7 | Thống kê độ bao phủ ở Bước 37–38 |
| `ngoai_sau_loai=<cụm>` | Điều kiện không xếp được vào sáu loại | Phần giới hạn của khóa luận (T10 điểm 10) |

**Thời gian:** `giay` là số giây từ lúc đọc tuyên bố đến lúc ghi xong. Chỗ hướng dẫn chưa rõ thì ghi vào danh sách "câu hỏi nhãn" để giải quyết ở Bước 16, không tự đặt quy tắc mới.

## 9. Ví dụ

48 ví dụ, chỉ từ 4 mẫu tập phát triển. Mọi câu trích đã kiểm là chuỗi con của `noi_dung` hoặc `chu_thich` trong `doan.jsonl` đã bỏ số chú thích (sau khi gộp khoảng trắng; kiểm ngày 31/10/2026). "P:" ghi đầu ra dự kiến của hệ thống khi khác nhãn chuẩn. Mục 9.5 gom 4 ví dụ đổi nhãn sau khảo sát Bước 10; số hiệu giữ nguyên để các tệp khác nhắc tới vẫn đúng.

### 9.1 Đúng

**V01 · Đúng · D3.** iPhone 17 sạc nhanh lên đến 50% trong 20 phút với bộ sạc 40W trở lên.
- Bằng chứng: `dt-apple-iphone17#016` “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C”
- Lý do: Khớp với tài liệu: mốc 50%, 20 phút, bộ sạc 40W đạt đúng mức tối thiểu; không nêu cách sạc nên hiểu là sạc bằng cáp, như tài liệu.
- Ghi chú: `mac_dinh=cach_sac`.

**V02 · Đúng · D3 · điều kiện dạng số.** iPhone 17 sạc 50% trong 20 phút với củ sạc 60W.
- Bằng chứng: `dt-apple-iphone17#016` “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C”
- Lý do: Củ 60W thỏa "40W trở lên" (60 ≥ 40) nên cùng điều kiện; 20 phút khớp (quảng cáo bỏ "lên đến").
- Ghi chú: `mac_dinh=cach_sac`.

*V03 đổi nhãn sau khảo sát Bước 10, xem mục 9.5.*

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
- Lý do: Cùng hoạt động sử dụng liên tục; 13 giờ thấp hơn 13,19 giờ, tức kém thuận lợi hơn, vẫn khớp.

**V08 · Đúng · D3 · điều kiện lạ trong tài liệu.** Xiaomi 15T đạt chuẩn chống nước IP68.
- Bằng chứng: `dt-xiaomi-15t#012` “IP68” và chú thích “ngâm trong nước ngọt tĩnh lặng ở độ sâu 3 mét; tối đa 30 phút; với mức chênh lệch nhiệt độ giữa nước và sản phẩm là từ 5K trở xuống”
- Lý do: Không nêu điều kiện thử nên hiểu như hãng công bố; mã IP68 bằng nhau.
- Ghi chú: `ngoai_cau_hinh=chênh lệch nhiệt độ ≤5K`. Người gán xếp cụm này vào điều kiện đo của bài thử, hiểu như hãng công bố. Bảng bao phủ có ghi điều kiện nhiệt độ (mục 2.7) nhưng `dien_thoai.yaml` chưa có cụm này.
- P: D1a (`dieu_kien_la`) nếu bước trích xuất ghi cụm nhiệt độ vào `dieu_kien_khac`.

**V09 · Đúng · D3.** Galaxy Buds3 Pro nghe nhạc 6 giờ khi bật chống ồn.
- Bằng chứng: `tn-samsung-buds3pro#038` “BẬT Tính năng ANC Đến 6 / 26 giờ”; `tn-samsung-buds3pro#044` “Thời gian phát nhạc (bật ANC) Lên đến 6”
- Lý do: Cùng chế độ bật chống ồn; không nêu bộ phận nên hiểu là tai nghe (số 6 trong "6 / 26"); 6 giờ khớp (quảng cáo bỏ "lên đến"). Ví dụ của đề cương.
- Ghi chú: `mac_dinh=bo_phan`.

**V10 · Đúng · D3.** Galaxy Buds3 Pro nghe nhạc đến 6 giờ.
- Bằng chứng: `tn-samsung-buds3pro#038` “BẬT Tính năng ANC Đến 6 / 26 giờ”; `tn-samsung-buds3pro#020` chú thích “ANC (Active Noise Canceling) được bật theo mặc định.”
- Lý do: Không nêu chế độ nên hiểu là chống ồn bật, vì hãng ghi ANC bật theo mặc định; ở chế độ này tài liệu ghi đến 6 giờ, khớp.
- Ghi chú: `mac_dinh=che_do_chong_on,bo_phan`.

**V11 · Đúng · D3.** Apple Watch SE 3 dùng đến 32 giờ ở chế độ nguồn điện thấp.
- Bằng chứng: `dh-apple-watchse3#008` “Lên đến 32 giờ ở Chế Độ Nguồn Điện Thấp”
- Lý do: Cùng chế độ nguồn điện thấp; 32 giờ khớp. Ví dụ của đề cương.

**V12 · Đúng · D3 · so thẳng.** Apple Watch SE 3 có độ sáng 1000 nit.
- Bằng chứng: `dh-apple-watchse3#007` “Độ sáng đỉnh 1000 nit”
- Lý do: Tài liệu chỉ có một con số độ sáng và không kèm điều kiện nào; "đỉnh" gắn với một giá trị duy nhất nên là kiểu giá trị tối đa. So thẳng: khớp; tài liệu không nêu điều kiện.

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
- Bằng chứng: `tn-samsung-buds3pro#038` “Tắt Tính năng ANC Đến 7 / 30 giờ”, “BẬT Tính năng ANC Đến 6 / 26 giờ”
- Lý do: Tài liệu ghi 6 giờ ở điều kiện hiểu mặc định (chống ồn bật, tai nghe); 8 giờ còn thuận lợi hơn mọi giá trị công bố cho tai nghe (cao nhất 7 giờ) và không trùng giá trị nào. Ví dụ của đề cương.

**V17 · Sai (`doi_gia_tri`) · D5 · sai đối tượng (sản phẩm).** Galaxy Buds3 Pro nghe nhạc 8,5 giờ khi tắt chống ồn.
- Bằng chứng: `tn-samsung-buds3pro#042` “Đến 7,0/30 giờ (Tính năng ANC Tắt)”
- Lý do: Tài liệu ghi 7 giờ khi tắt chống ồn; tuyên bố ghi 8,5 giờ. Số 8,5 giờ trong cùng đoạn thuộc cột Galaxy Buds FE của bảng so sánh, không phải của Buds3 Pro, nên không tính là giá trị ở điều kiện khác.

**V18 · Sai (`doi_bo_phan`) · D5 · sai đối tượng (bộ phận).** Hộp sạc Galaxy Buds3 Pro cũng kháng nước.
- Bằng chứng: `tn-samsung-buds3pro#038` chú thích “Hộp sạc không có khả năng kháng nước.”
- Lý do: Tài liệu ghi hộp sạc không kháng nước; tuyên bố nói có. Tuyên bố không nêu mã nên không trùng mã IP57 của tai nghe; so với V35.

**V19 · Sai (`doi_gia_tri`) · D5.** Màn hình iPhone 17 đạt 4000 nit ngoài trời.
- Bằng chứng: `dt-apple-iphone17#005` “độ sáng đỉnh 3000 nit (ngoài trời)”
- Lý do: Tài liệu ghi 3000 nit ở chế độ ngoài trời; tuyên bố ghi 4000 nit, thuận lợi hơn và không trùng giá trị nào.

**V20 · Sai (`doi_gia_tri`) · D5 · thấp hơn tốt hơn.** Xiaomi 15T sạc đầy 100% chỉ trong 40 phút với củ sạc 67W.
- Bằng chứng: `dt-xiaomi-15t#047` “50 phút sạc đầy 100%” và chú thích “Máy được khuyến cáo sử dụng củ sạc Xiaomi 67W hoặc cao hơn.”
- Lý do: Cùng điều kiện (củ 67W thỏa "67W hoặc cao hơn", mốc 100%); tài liệu ghi 50 phút, tuyên bố ghi 40 phút. Với thời gian sạc, thấp hơn là thuận lợi hơn, nên 40 phút mâu thuẫn với tài liệu.

### 9.3 Lệch điều kiện

**V21 · Lệch (`bo_dieu_kien`) · D4.** iPhone 17 sạc 50% chỉ trong 20 phút.
- Bằng chứng: `dt-apple-iphone17#016` “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C”; `dt-apple-iphone17#040` “Trong Hộp Sản Phẩm iPhone với iOS 27 Cáp Sạc USB-C (1m)”
- Lý do: 20 phút chỉ đạt với bộ tiếp hợp 40W trở lên, được bán riêng; tuyên bố không nêu bộ sạc nên hiểu là chỉ có đồ trong hộp (cáp, không có củ sạc). Thiếu chữ "lên đến" không phải lý do của nhãn. Ví dụ của đề cương.
- Ghi chú: `mac_dinh=bo_tiep_hop`.

**V22 · Lệch (`doi_dieu_kien`) · D4 · điều kiện dạng số.** iPhone 17 sạc 50% trong 20 phút với củ sạc 20W.
- Bằng chứng: `dt-apple-iphone17#016` “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C”
- Lý do: 20 phút chỉ đạt với bộ tiếp hợp 40W trở lên; tuyên bố nêu củ 20W, thấp hơn mức tối thiểu (20 < 40), là điều kiện khác.

**V23 · Lệch (`bo_dieu_kien`) · D4.** Xiaomi 15T hỗ trợ sạc nhanh HyperCharge 67W.
- Bằng chứng: `dt-xiaomi-15t#005` “Sạc nhanh HyperCharge 67W” và chú thích “Bộ sạc không bao gồm trong hộp. Máy được khuyến cáo sử dụng củ sạc Xiaomi 67W hoặc cao hơn.”; `dt-xiaomi-15t#014` “Điện thoại di động / Cáp USB Type-C”
- Lý do: Công suất 67W cần củ sạc 67W trở lên, không có trong hộp; tuyên bố không nêu củ sạc nên hiểu là không mua thêm.
- Ghi chú: `mac_dinh=bo_tiep_hop`.

**V24 · Lệch (`bo_dieu_kien`) · D4.** iPhone 17 dùng pin được 30 giờ.
- Bằng chứng: `dt-apple-iphone17#016` “Thời gian xem video Lên đến 30 giờ”, “Thời gian xem video (trực tuyến) Lên đến 27 giờ”
- Lý do: Không nêu hoạt động nên phải đúng ở hoạt động kém thuận lợi nhất là xem video trực tuyến (27 giờ); 30 giờ là số của hoạt động xem video không trực tuyến.
- Ghi chú: `mac_dinh=hoat_dong`.

*V25, V26 đổi nhãn sau khảo sát Bước 10, xem mục 9.5.*

**V27 · Lệch (`doi_dieu_kien`) · D4 · điều kiện dạng số.** Dưới ánh sáng mạnh, Xiaomi 15T sáng 3200 nit trên toàn màn hình.
- Bằng chứng: `dt-xiaomi-15t#004` “Độ sáng cực đại: 3200 nit trên 25% diện tích màn hình”; `dt-xiaomi-15t#038` “Dưới ánh sáng mạnh, màn hình sẽ tự động kích hoạt chế độ tăng mức sáng APL 25%”
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
- Bằng chứng: `tn-samsung-buds3pro#044` “Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7”
- Lý do: 7 giờ chỉ đạt khi tắt chống ồn; tuyên bố ghi bật chống ồn (bật thì 6 giờ). Ví dụ của đề cương.
- Ghi chú: `mac_dinh=bo_phan`.

**V32 · Lệch (`bo_dieu_kien`) · D4.** Galaxy Buds3 Pro pin 7 giờ.
- Bằng chứng: `tn-samsung-buds3pro#044` “Thời gian phát nhạc (Giờ, tắt ANC) Lên đến 7”, “Thời gian phát nhạc (bật ANC) Lên đến 6”; `tn-samsung-buds3pro#020` chú thích “ANC (Active Noise Canceling) được bật theo mặc định.”
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
- Bằng chứng: `tn-samsung-buds3pro#044` “Chuẩn IP57”; `tn-samsung-buds3pro#038` chú thích “Hộp sạc không có khả năng kháng nước.”
- Lý do: IP57 chỉ áp dụng cho tai nghe; tuyên bố gán cho hộp sạc, vốn không kháng nước. IP57 trùng giá trị của tai nghe nên dừng ở D4 trước D5; so với V18.

**V36 · Lệch (`doi_bo_phan`) · D4.** Tai nghe Galaxy Buds3 Pro có pin 515 mAh.
- Bằng chứng: `tn-samsung-buds3pro#044` “Dung lượng pin tai nghe (mAh, Typical) 50”, “Dung lượng pin hộp sạc (mAh, Typical) 515”
- Lý do: 515 mAh là dung lượng hộp sạc; tuyên bố gán cho tai nghe, vốn có 50 mAh.

**V37 · Lệch (`doi_kieu_gia_tri`) · D4.** Pin Xiaomi 15T có dung lượng định mức 5500mAh.
- Bằng chứng: `dt-xiaomi-15t#005` “Pin Xiaomi Surge 5500mAh (thông thường)”; `dt-xiaomi-15t#022` “Pin bền bỉ 5500mAh (typ)”
- Lý do: 5500mAh là dung lượng điển hình; tuyên bố ghi rõ "định mức", một kiểu giá trị khác. Tuyên bố không ghi kiểu ("pin 5500mAh") thì hiểu là điển hình và Đúng.

**V38 · Lệch (`doi_kieu_gia_tri`) · D2.** Galaxy Buds3 Pro luôn nghe đủ 6 giờ.
- Bằng chứng: `tn-samsung-buds3pro#044` “Thời gian phát nhạc (bật ANC) Lên đến 6”
- Lý do: Tài liệu ghi mức tối đa "lên đến 6"; tuyên bố dùng "luôn" để biến thành mức chắc chắn đạt.
- Ghi chú: `mac_dinh=che_do_chong_on,hoat_dong,bo_phan`.

**V39 · Lệch (`doi_kieu_gia_tri`) · D2.** Apple Watch SE 3 luôn dùng đủ 18 giờ mỗi ngày.
- Bằng chứng: `dh-apple-watchse3#008` “Pin dùng cả ngày, lên đến 18 giờ khi sử dụng bình thường”
- Lý do: Tài liệu ghi mức tối đa "lên đến 18 giờ"; tuyên bố viết thành mức chắc chắn đạt.
- Ghi chú: `mac_dinh=che_do_nguon,hoat_dong`.

**V40 · Lệch (`doi_kieu_gia_tri`) · D2.** Màn hình iPhone 17 luôn chạy ở 120Hz.
- Bằng chứng: `dt-apple-iphone17#004` “Công nghệ ProMotion với tốc độ làm mới thích ứng lên đến 120Hz”
- Lý do: Tài liệu ghi tần số quét thích ứng, tối đa 120Hz; tuyên bố viết thành luôn đạt 120Hz. Khác "Màn hình Luôn Bật" cùng đoạn: chữ "Luôn" ở đó là tên tính năng, không nằm trong câu của giá trị.

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
- Bằng chứng: `tn-samsung-buds3pro#038` “Tắt Tính năng ANC Đến 7 / 30 giờ”, “BẬT Tính năng ANC Đến 6 / 26 giờ”
- Lý do: Tài liệu chỉ công bố thời lượng khi bật và tắt chống ồn, không công bố ở chế độ xuyên âm; 6,5 giờ không trùng giá trị nào và không cao hơn mọi giá trị của tai nghe (cao nhất 7 giờ). Cấu hình đã biết cụm "xuyên âm", "Ambient", nên P cũng dừng ở D6.
- Ghi chú: `mac_dinh=bo_phan`.

**V45 · Chưa đủ thông tin · D1 · thiếu bằng chứng.** Galaxy Buds3 Pro sạc nhanh 5 phút nghe được 1 giờ.
- Bằng chứng: không có.
- Lý do: Tài liệu của Galaxy Buds3 Pro không có thông số sạc nhanh.

**V46 · Chưa đủ thông tin · D1a.** iPhone 17 sạc nhanh chỉ trong 20 phút với bộ sạc 40W.
- Bằng chứng: `dt-apple-iphone17#016` “Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB-C”
- Lý do: Chưa xác định được điều kiện của tuyên bố: tuyên bố không nói sạc tới bao nhiêu phần trăm, và mốc phần trăm không có cách hiểu mặc định. Người gán không đoán mốc từ con số 20 phút.

**V47 · Chưa đủ thông tin · D1a.** iPhone 17 có độ sáng đỉnh 3000 nit.
- Bằng chứng: `dt-apple-iphone17#005` “độ sáng đỉnh 1600 nit (HDR); độ sáng đỉnh 3000 nit (ngoài trời)”
- Lý do: Trên trang Apple, "đỉnh" dùng cho hai chế độ (HDR 1600 nit, ngoài trời 3000 nit); tuyên bố không nói chế độ nào nên chưa xác định được điều kiện. Không chọn chế độ theo con số của tuyên bố.

**V48 · Chưa đủ thông tin · D1b · xung đột bằng chứng.** Galaxy Buds3 Pro dùng tổng cộng 30 giờ kèm hộp sạc khi bật chống ồn.
- Bằng chứng: `tn-samsung-buds3pro#044` “Tổng thời gian phát nhạc (Giờ, bật ANC) Lên đến 26”, “Tổng thời gian phát nhạc (Giờ, bật ANC) Lên đến 30”; `tn-samsung-buds3pro#038` “BẬT Tính năng ANC Đến 6 / 26 giờ” và chú thích “Với tính năng bật/tắt ANC, tai nghe và hộp tai nghe cung cấp tối đa 30 giờ phát khi sạc đầy.”
- Lý do: Tài liệu ghi hai giá trị cho tổng thời gian phát nhạc khi bật chống ồn: 26 giờ (khối "Thời gian phát", bảng thông số) và 30 giờ (dòng thứ hai trong bảng thông số, nằm dưới nhóm tắt ANC nhưng ghi "bật ANC"; chú thích cũng ghi tối đa 30 giờ cho cả bật và tắt). Đặt `tai_lieu_mau_thuan = true`. Tuyên bố ghi 26 giờ kèm hộp sạc khi bật chống ồn cũng ra D1b.

### 9.5 Đổi nhãn sau khảo sát Bước 10 (28/10/2026)

Khảo sát 10 người đọc (`ket_qua/khao_sat_cach_hieu.md`) sửa hai chỗ của cấu hình điện thoại: "xem video" không kèm "tải sẵn" hay "trực tuyến" coi như chưa nêu hoạt động (Q09, 9/10 người); độ sáng không còn cách hiểu mặc định khi tuyên bố không nêu chế độ (Q10, 7/10 người). Bốn ví dụ dưới đổi nhãn, giữ nguyên số hiệu.

**V03 · Lệch (`bo_dieu_kien`) · D4 · bỏ "lên đến".** iPhone 17 xem video được 30 giờ.
- Bằng chứng: `dt-apple-iphone17#016` “Thời gian xem video Lên đến 30 giờ”, “Thời gian xem video (trực tuyến) Lên đến 27 giờ”
- Lý do: "Xem video" không nói tải sẵn hay trực tuyến, nên coi như chưa nêu loại hoạt động và lấy hoạt động kém thuận lợi nhất là xem video trực tuyến (27 giờ). 30 giờ là số của xem video tải sẵn. Thiếu "lên đến" không phải lý do của nhãn.
- Ghi chú: `mac_dinh=hoat_dong`.
- Trước khảo sát: Đúng (D3), vì cấu hình hiểu "xem video" là xem video tải sẵn, khớp nhãn "Thời gian xem video" của Apple.

**V25 · Chưa đủ thông tin · D1a.** Màn hình iPhone 17 sáng 3000 nit.
- Bằng chứng: `dt-apple-iphone17#005` “Độ sáng tối đa 1000 nit (tiêu chuẩn); độ sáng đỉnh 1600 nit (HDR); độ sáng đỉnh 3000 nit (ngoài trời)”
- Lý do: Tuyên bố không nêu chế độ hiển thị, và độ sáng điện thoại không có cách hiểu mặc định, nên chưa xác định được điều kiện. Không chọn chế độ theo con số của tuyên bố.
- Ghi chú: `mac_dinh=che_do_hien_thi` (nhãn dựa vào việc không có mặc định).
- Trước khảo sát: Lệch (`bo_dieu_kien`, D4), hiểu là chế độ tiêu chuẩn (1000 nit).

**V26 · Chưa đủ thông tin · D1a.** Màn hình Xiaomi 15T sáng 3200 nit.
- Bằng chứng: `dt-xiaomi-15t#004` “Độ sáng cực đại: 3200 nit trên 25% diện tích màn hình”; `dt-xiaomi-15t#038` “Dưới ánh sáng mạnh, màn hình sẽ tự động kích hoạt chế độ tăng mức sáng APL 25%”
- Lý do: Tài liệu chỉ công bố 3200 nit khi màn hình tự tăng sáng dưới ánh sáng mạnh, đo trên 25% diện tích. Tuyên bố không nêu chế độ, độ sáng điện thoại không có cách hiểu mặc định, nên chưa xác định được điều kiện.
- Ghi chú: `mac_dinh=che_do_hien_thi`.
- Trước khảo sát: Lệch (`bo_dieu_kien`, D4), hiểu là chế độ thông thường.

**V43 · Chưa đủ thông tin · D1a · trường hợp biên.** Xiaomi 15T có độ sáng cực đại 3200 nit.
- Bằng chứng: `dt-xiaomi-15t#004` “Độ sáng cực đại: 3200 nit trên 25% diện tích màn hình”; `dt-xiaomi-15t#038` “Dưới ánh sáng mạnh, màn hình sẽ tự động kích hoạt chế độ tăng mức sáng APL 25%”
- Lý do: Trang Xiaomi 15T chỉ có một con số độ sáng, nên chữ "cực đại" là kiểu giá trị tối đa, không phải tên chế độ (mục 6.5). Tuyên bố vì vậy không nêu chế độ, và độ sáng điện thoại không có cách hiểu mặc định, nên chưa xác định được điều kiện. Chép đúng chữ của hãng không bù được điều kiện bị bỏ.
- Ghi chú: `mac_dinh=che_do_hien_thi`.
- Trước khảo sát: Lệch (`bo_dieu_kien`, D4), chốt ngày 27/10 (mục 11.1).

## 10. Bảng phủ ví dụ

**Theo nhãn và dòng quyết định:**

| Nhãn | Số ví dụ | Dòng |
|---|---|---|
| Đúng | 14 (V01, V02, V04–V15) | D3 |
| Sai | 5 (V16–V20) | D5 |
| Lệch điều kiện | 21 (V03, V21–V24, V27–V42) | D4: 18; D2: 3 (V38–V40) |
| Chưa đủ thông tin | 8 (V25, V26, V43–V48) | D1 (V45), D1a (V25, V26, V43, V46, V47), D1b (V48), D6 (V44) |

Số trên là sau khảo sát Bước 10. Trước khảo sát: Đúng 15, Sai 5, Lệch 23, Chưa đủ thông tin 5 (mục 9.5).

**Theo loại biến đổi** (mỗi loại ít nhất 2):

| Loại | Ví dụ |
|---|---|
| `bo_dieu_kien` | V03, V21, V23, V24, V28, V32, V33, V34 |
| `doi_dieu_kien` | V22, V27, V29, V30, V31, V41, V42 |
| `doi_bo_phan` | V18 (Sai), V35, V36 |
| `doi_phien_ban` | V14, V15 (cả hai Đúng: tập phát triển không có trang tách giá trị theo phiên bản, nên chưa có ví dụ Lệch đổi phiên bản) |
| `doi_kieu_gia_tri` | V37, V38, V39, V40 |
| `doi_gia_tri` | V16, V17, V19, V20 |

**Các trường hợp đề cương và kế hoạch yêu cầu:**

| Trường hợp | Ví dụ |
|---|---|
| Đúng | V01, V02, V04–V15 |
| Sai đối tượng | V17 (số của sản phẩm khác), V18 và V35, V36 (bộ phận khác) |
| Sai điều kiện | V03, V21–V24, V27–V34, V41, V42 |
| Thiếu bằng chứng | V45 (không có thuộc tính), V44 (không có giá trị ở điều kiện) |
| Điều kiện không có cách hiểu mặc định | V46 (mốc phần trăm), V25, V26, V43 (độ sáng điện thoại) |
| Xung đột bằng chứng | V48 |
| Điều kiện dạng số (≥ và ≤) | V02, V22 (bộ tiếp hợp); V06, V29 (độ sâu); V27 (phần diện tích); V20 (mốc 100%) |
| Điều kiện cấu hình chưa biết | V08 (ở tài liệu), V41 (ở tuyên bố), V27 |
| Bỏ "lên đến" | V02, V04, V09 (vẫn Đúng); V03 (Lệch vì lý do khác) |
| Watch SE 3 "đỉnh 1000 nit" so thẳng | V12 |
| Mặc định tai nghe: nghe nhạc, chống ồn bật | V10, V32, V38 |
| Mặc định đồng hồ: sử dụng bình thường, chế độ thường | V33, V39 |

**Theo nhóm:** điện thoại 24 (iPhone 17: 16; Xiaomi 15T: 8), tai nghe 14, đồng hồ 10 (cộng 48). Mỗi thuộc tính trong 16 thuộc tính có ít nhất một ví dụ, trừ sạc nhanh của tai nghe chỉ có ví dụ D1 (V45) vì Galaxy Buds3 Pro không công bố.

## 11. Ca đã chốt và rủi ro đã biết

### 11.1 Xiaomi 15T "độ sáng cực đại 3200 nit" (ví dụ 16 cũ ở T4.6)

Tuyên bố chép gần nguyên văn dòng "Độ sáng cực đại: 3200 nit trên 25% diện tích màn hình" (`dt-xiaomi-15t#004`). Bộ luật Bước 8 cho hai cách đọc:

- **Đọc theo chữ của cấu hình:** `cach_goi_theo_hang` của Xiaomi chỉ áp khi tài liệu dùng chữ đó để phân biệt từ hai giá trị trở lên. Trang Xiaomi 15T chỉ có một con số độ sáng (3200 nit ở cả `#004` và `#037`), nên "cực đại" là kiểu giá trị tối đa. Tuyên bố khi đó không nêu chế độ, hiểu là chế độ thông thường, và ra **Lệch** (`bo_dieu_kien`) như V26.
- **Đọc theo cách gọi của hãng:** "cực đại" là tên Xiaomi dùng cho mức sáng của chế độ tự tăng sáng (`#004` cùng `#038`). Tuyên bố dùng đúng chữ đó nên nêu cùng chế độ; phần 25% diện tích không nêu thì hiểu như hãng công bố. Kết quả **Đúng**, như ví dụ 16 cũ.

**Đã chốt ngày 27/10/2026: Lệch**, theo chữ của cấu hình (V43). Lý do: tuyên bố bỏ điều kiện mà con số cần, cụ thể là chế độ tự tăng sáng dưới ánh sáng mạnh. Dùng đúng chữ "cực đại" của hãng không bù được phần điều kiện bị bỏ, vì trên trang này chữ đó không gọi tên chế độ nào. Cấu hình giữ nguyên, nên V43 là kiểm thử hồi quy cho P như mọi ví dụ khác.

**Cập nhật 28/10/2026 sau khảo sát Bước 10:** độ sáng điện thoại không còn cách hiểu mặc định, nên tuyên bố không nêu chế độ chưa xác định được điều kiện. V43 đổi từ Lệch thành **Chưa đủ thông tin** (D1a, mục 9.5). Lý do của quyết định ngày 27/10 vẫn đúng: tuyên bố thiếu điều kiện mà con số cần, và chữ "cực đại" không bù được. Chỉ khác là thiếu điều kiện giờ dẫn tới "chưa xác định được" thay vì "hiểu là chế độ thông thường". Cả hai nhãn đều không phải Đúng, nên FAR không đổi.

### 11.2 Trùng số ngẫu nhiên ở D4

D4 tính mọi điều kiện khác của cùng thuộc tính, nên con số trùng giá trị của một hoạt động khác cũng ra Lệch (V42: 5 giờ trùng thời gian đàm thoại khi tắt chống ồn). Cách làm này đúng định nghĩa của đề cương và không ảnh hưởng FAR, vì Lệch cũng không phải Đúng. Rủi ro là hạ độ chính xác của nhãn Lệch. Ở Bước 16, đếm số ca Lệch chỉ do trùng số giữa hai hoạt động; nếu nhiều thì cân nhắc giới hạn D4 trong các giá trị cùng hoạt động.

### 11.3 Cụm cấu hình chưa có, gặp ngay trong tập phát triển

| Cụm | Ở đâu | Hệ quả dự kiến với P | Ví dụ |
|---|---|---|---|
| "chênh lệch nhiệt độ ... 5K" | Chú thích kháng nước Xiaomi 15T (`#012`, `#035`) | D1a cho mọi tuyên bố kháng nước của Xiaomi 15T | V08 |
| "toàn màn hình" | Tuyên bố về phần diện tích đo | D1a thay vì Lệch | V27 |
| "chỉ dùng mạng di động" | Tuyên bố về đồng hồ bản di động | D1a thay vì Lệch | V41 |
| "ghép nối ... với điện thoại thông minh Galaxy ... với các cài đặt mặc định" | Chú thích thời lượng pin Buds3 Pro (`#038`) | Người gán coi là quy trình thử (ngữ cảnh). P có thể ra D1a cho mọi tuyên bố pin Buds3 Pro nếu bước trích xuất ghi cụm này vào `dieu_kien_khac` | Không có ví dụ riêng |
| "không ghép đôi với iPhone và có bật cảm biến nhịp tim" | Chú thích 7 giờ tập luyện ngoài trời của Watch SE 3 (`#008`) | Như trên | Không có ví dụ riêng |

Các cụm này lấy từ tập phát triển nên được phép bổ sung vào cấu hình. Hai cụm cuối nên vào `ngu_canh_khong_quyet_dinh` của `chung.yaml`. Phiên thử độ bao phủ trên 3 sản phẩm ngoài 12 mẫu có thể thêm luật; khi đó đối chiếu lại mục 5, 6 và các ví dụ có ghi chú `ngoai_cau_hinh`.

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
