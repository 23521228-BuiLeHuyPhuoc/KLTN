# Rà tách chinh.jsonl: cụm có trong câu gốc mà không có trong tuyên bố

Sinh bằng `scripts/ra_tach.py` từ `data/tuyen_bo/chinh.jsonl` và `data/cau_hinh/*.yaml` (cụm của phụ lục mục 13), từ khẳng định (mục 6.2) và cụm phủ nhiều giá trị (mục 6.8) của `data/huong_dan_gan_nhan.md`. Chỉ so chuỗi: không đề xuất cách sửa, không nêu nhãn. Người thực hiện tự quyết từng chỗ theo bốn tiêu chí gắn điều kiện (mục 2 của hướng dẫn).

- Cụm thấy ở đây có thể thuộc con số khác của cùng câu gốc hoặc là tên tính năng (tiêu chí 3); không thấy cụm nào không có nghĩa tuyên bố đủ điều kiện, vì cụm ngoài cấu hình không được dò.
- Chỉ xét các điều kiện của thuộc tính ghi trên tuyên bố.
- Đã lọc theo mẫu: dt-oppo-findx8, dt-samsung-galaxys25ultra, dt-xiaomi-redminote14proplus5g, tn-apple-airpodspro3, tn-apple-airpods4, tn-xiaomi-redmibuds6pro, dh-samsung-galaxywatch8, dh-xiaomi-watchs4.
- 8 / 216 tuyên bố có cụm được liệt kê.

| Mã | Tuyên bố | Câu gốc | Cụm có trong câu gốc, không có trong tuyên bố |
|---|---|---|---|
| tb-00110 | Galaxy Watch8 có màn hình cực sáng 3.000 nits hiển thị sắc nét mọi lúc | Màn hình cực sáng 3.000 nits hiển thị sắc nét mọi lúc | – |
| tb-00111 | Galaxy Watch8 có thời gian sử dụng lên tới 30 giờ ngay cả khi bật chế độ Màn hình luôn bật (Always On Display) | thời gian sử dụng bền bỉ lên tới 30 giờ ngay cả khi bật chế độ Màn hình luôn bật (Always On Display). | – |
| tb-00112 | Galaxy Watch8 kháng nước 5ATM đạt chuẩn ISO 22810:2010 ở độ sâu tới 50 m | chứng nhận kháng nước 5ATM đạt chuẩn ISO 22810:2010 ở độ sâu tới 50 m | – |
| tb-00113 | Galaxy Watch8 có chuẩn kháng nước IPX8 | chuẩn kháng nước IPX8 | – |
| tb-00114 | Galaxy Watch8 có chuẩn kháng bụi IP6X theo tiêu chuẩn IEC 60529 | chuẩn kháng bụi IP6X cao cấp theo tiêu chuẩn IEC 60529 | – |
| tb-00115 | Galaxy Watch8 có độ sáng lên tới 3.000 nits | Được trang bị màn hình vượt trội với độ sáng lên tới 3.000 nits | – |
| tb-00116 | Galaxy Watch8 có thời lượng pin lên đến 30 giờ ở chế độ Always On Display | Thời lượng pin lên đến 30 giờ ở chế độ Always On Display | – |
| tb-00117 | Galaxy Watch8 có khả năng kháng nước 5ATM | Khả năng kháng nước 5ATM, IPX8 | – |
| tb-00118 | Galaxy Watch8 có khả năng kháng nước IPX8 | Khả năng kháng nước 5ATM, IPX8 | chuan_do_sau=iso_22810: “5ATM” |
| tb-00119 | Galaxy Watch8 có màn hình 3.000 nits | Màn hình 3.000 nits | – |
| tb-00120 | Galaxy Watch8 có chuẩn kháng bụi IP6X | chuẩn kháng bụi IP6X | – |
| tb-00121 | Galaxy Watch8 có kháng nước 5ATM | kháng nước 5ATM | – |
| tb-00122 | Galaxy Watch8 có màn hình siêu sáng 3.000 nits | màn hình siêu sáng 3.000 nits | – |
| tb-00123 | Galaxy Watch8 có thời lượng pin lên tới 30 giờ ở chế độ Always On Display | Thời lượng pin lên tới 30 giờ ở chế độ Always On Display | – |
| tb-00124 | Galaxy Watch8 có khả năng kháng nước 5ATM | Khả năng kháng nước 5ATM, IPX8 | – |
| tb-00125 | Galaxy Watch8 có khả năng kháng nước IPX8 | Khả năng kháng nước 5ATM, IPX8 | chuan_do_sau=iso_22810: “5ATM” |
| tb-00126 | Galaxy Watch8 có màn hình sáng tới 3.000 nits | Màn hình sáng tới 3.000 nits | – |
| tb-00127 | Galaxy Watch8 kháng bụi IP6X | kháng bụi IP6X | – |
| tb-00128 | Galaxy Watch8 có độ sáng lên tới 3.000 nits | độ sáng lên tới 3.000 nits | – |
| tb-00129 | Galaxy Watch8 cho tới 30 giờ sử dụng liên tục ở chế độ Always On Display | cho tới 30 giờ sử dụng liên tục ở chế độ Always On Display | – |
| tb-00130 | Galaxy Watch8 kháng nước 5ATM | kháng nước 5ATM, IPX8 | – |
| tb-00131 | Galaxy Watch8 kháng nước IPX8 | kháng nước 5ATM, IPX8 | chuan_do_sau=iso_22810: “5ATM” |
| tb-00132 | Galaxy Watch8 kháng bụi IP6X | kháng bụi IP6X | – |
| tb-00133 | Xiaomi Watch S4 có thời lượng hoạt động lên đến 15 ngày | thời lượng hoạt động lên đến 15 ngày | – |
| tb-00134 | Xiaomi Watch S4 có tính năng sạc nhanh 5 phút dùng đủ 2 ngày | tính năng sạc nhanh 5 phút dùng đủ 2 ngày. | – |
| tb-00135 | Xiaomi Watch S4 có độ sáng cực đại 2.200 nit | độ sáng cực đại 2.200 nit | – |
| tb-00136 | Xiaomi Watch S4 có khả năng chống nước 5ATM | khả năng chống nước 5ATM vượt trội. | – |
| tb-00137 | Xiaomi Watch S4 có thời lượng pin ấn tượng lên đến 15 ngày sử dụng liên tục chỉ với một lần sạc đầy | thời lượng pin ấn tượng lên đến 15 ngày sử dụng liên tục chỉ với một lần sạc đầy. | – |
| tb-00138 | Xiaomi Watch S4 có thời lượng pin ấn tượng lên đến 15 ngày | thời lượng pin ấn tượng lên đến 15 ngày. | – |
| tb-00139 | Xiaomi Watch S4 có độ sáng HBM 1.500 nit | độ sáng HBM 1.500 nit | – |
| tb-00140 | Xiaomi Watch S4 có độ sáng cực đại 2.200 nit | độ sáng cực đại 2.200 nit | – |
| tb-00141 | Xiaomi Watch S4 có thời lượng pin 15 ngày | Thời lượng pin 15 ngày vượt trội | – |
| tb-00142 | Xiaomi Watch S4 sạc nhanh chỉ 5 phút sạc cho 2 ngày sử dụng | sạc nhanh vượt trội chỉ 5 phút sạc cho 2 ngày sử dụng. | – |
| tb-00143 | Xiaomi Watch S4 đạt chuẩn chống nước 5ATM | đạt chuẩn chống nước 5ATM | – |
| tb-00144 | Xiaomi Watch S4 có thời lượng sử dụng lên tới 14 ngày chỉ với một lần sạc | thời lượng sử dụng lên tới 14 ngày chỉ với một lần sạc | – |
| tb-00145 | Xiaomi Watch S4 có pin kéo dài 15 ngày | pin kéo dài 15 ngày | – |
| tb-00146 | Xiaomi Watch S4 có độ sáng lên tới 1.500 nit | độ sáng lên tới 1.500 nit | – |
| tb-00147 | Xiaomi Watch S4 có thời lượng pin lên đến 15 ngày | Thời lượng pin lên đến 15 ngày | – |
| tb-00148 | Xiaomi Watch S4 chỉ cần sạc 5 phút là có thể sử dụng liên tục 2 ngày | chỉ cần sạc 5 phút là có thể sử dụng liên tục 2 ngày | – |
| tb-00149 | Xiaomi Watch S4 có thời lượng pin thực tế đạt trên 14 ngày | thời lượng pin thực tế đạt trên 14 ngày | – |
| tb-00150 | Xiaomi Watch S4 có pin kéo dài tới 14 ngày | Pin kéo dài tới 14 ngày | – |
| tb-00151 | Xiaomi Watch S4 có độ sáng lên tới 1.500 nit (HBM) | độ sáng lên tới 1.500 nit (HBM) | – |
| tb-00152 | Xiaomi Watch S4 có thời lượng sử dụng lên tới 15 ngày | thời lượng sử dụng lên tới 15 ngày | – |
| tb-00153 | Xiaomi Watch S4 chỉ cần sạc 5 phút là đủ dùng 2 ngày | chỉ cần sạc 5 phút là đủ dùng 2 ngày | – |
| tb-00154 | Xiaomi Watch S4 có khả năng chống nước 5ATM | Khả năng chống nước 5ATM | – |
| tb-00155 | OPPO Find X8 có màn hình AMOLED 120Hz | Màn hình AMOLED 120Hz | – |
| tb-00156 | OPPO Find X8 có màn hình ProXDR 120Hz | màn hình ProXDR 120Hz | – |
| tb-00157 | OPPO Find X8 có độ sáng tối đa 4500nits | độ sáng tối đa 4500nits | – |
| tb-00158 | OPPO Find X8 có dung lượng pin 5630mAh | Dung lượng pin 5630mAh | – |
| tb-00159 | OPPO Find X8 hỗ trợ phát trực tuyến liên tục 21 giờ | hỗ trợ phát trực tuyến liên tục 21 giờ | – |
| tb-00160 | OPPO Find X8 sạc nhanh SuperVOOC 80W | sạc nhanh SuperVOOC 80W | – |
| tb-00161 | OPPO Find X8 sạc không dây 50W | sạc không dây 50W | – |
| tb-00162 | OPPO Find X8 có chuẩn kháng nước IP68 | chuẩn kháng nước IP68 và IP69 | – |
| tb-00163 | OPPO Find X8 có chuẩn kháng nước IP69 | chuẩn kháng nước IP68 và IP69 | – |
| tb-00164 | OPPO Find X8 chụp ảnh ở mọi khoảng cách đến 120x | Chụp ảnh sắc nét và chân thực ở mọi khoảng cách từ 0.6x đến 120x | – |
| tb-00165 | OPPO Find X8 quay phim Dolby Vision liên tục tới 5.1 giờ ngay cả trong môi trường âm 20 độ C | quay phim Dolby Vision liên tục tới 5.1 giờ ngay cả trong môi trường khắc nghiệt âm 20 độ C | – |
| tb-00166 | OPPO Find X8 có màn hình ProXDR 120Hz | Màn hình ProXDR 120Hz | – |
| tb-00167 | OPPO Find X8 có độ sáng tối đa 4500 nits | độ sáng tối đa 4500 nits | – |
| tb-00168 | OPPO Find X8 có viên pin Silicon-carbon 5630mAh dung lượng lớn | Viên pin Silicon-carbon 5630mAh dung lượng lớn | – |
| tb-00169 | OPPO Find X8 sạc nhanh SuperVOOC 80W | sạc nhanh SuperVOOC 80W | – |
| tb-00170 | OPPO Find X8 sạc không dây 50W tiện lợi | sạc không dây 50W tiện lợi. | – |
| tb-00171 | OPPO Find X8 có độ bền chuẩn IP68 | độ bền chuẩn IP68 và IP69 | – |
| tb-00172 | OPPO Find X8 có độ bền chuẩn IP69 | độ bền chuẩn IP68 và IP69 | – |
| tb-00173 | OPPO Find X8 có pin 5000mAh | Pin 5000mAh | – |
| tb-00174 | OPPO Find X8 hỗ trợ sạc nhanh 80W | hỗ trợ sạc nhanh 80W | – |
| tb-00175 | OPPO Find X8 có màn hình LTPO 120Hz | Màn hình LTPO 120Hz | – |
| tb-00176 | OPPO Find X8 có màn hình 120 Hz | 120 Hz | – |
| tb-00177 | OPPO Find X8 có độ sáng lên tới 4500 nits | độ sáng lên tới 4500 nits | – |
| tb-00178 | OPPO Find X8 có pin silicon‑carbon 5630 mAh | Pin silicon‑carbon 5630 mAh | – |
| tb-00179 | OPPO Find X8 cho tới 21 giờ phát trực tuyến liên tục | cho tới 21 giờ phát trực tuyến liên tục | – |
| tb-00180 | OPPO Find X8 sạc nhanh 80 W có dây | sạc nhanh 80 W có dây | – |
| tb-00181 | OPPO Find X8 có 50 W không dây | 50 W không dây | – |
| tb-00182 | OPPO Find X8 có zoom quang học 3× | zoom quang học 3× | – |
| tb-00183 | OPPO Find X8 có chuẩn IP68 | chuẩn IP68/IP69 | – |
| tb-00184 | OPPO Find X8 có chuẩn IP69 | chuẩn IP68/IP69 | – |
| tb-00185 | OPPO Find X8 có pin 5000mAh | Pin 5000mAh | – |
| tb-00186 | OPPO Find X8 hỗ trợ sạc nhanh 80W | hỗ trợ sạc nhanh 80W | – |
| tb-00187 | OPPO Find X8 sạc đầy trong vòng 30 phút | sạc đầy trong vòng 30 phút | – |
| tb-00188 | OPPO Find X8 có màn hình 6.59” ProXDR 120Hz | Màn hình 6.59” ProXDR 120Hz | – |
| tb-00189 | OPPO Find X8 có độ sáng lên tới 4500 nits | độ sáng lên tới 4500 nits | – |
| tb-00190 | OPPO Find X8 có zoom lên tới 120x | zoom lên tới 120x | – |
| tb-00191 | OPPO Find X8 có pin silicon‑carbon 5630 mAh | Pin silicon‑carbon 5630 mAh | – |
| tb-00192 | OPPO Find X8 cho tới 21 giờ phát trực tuyến liên tục | cho tới 21 giờ phát trực tuyến liên tục | – |
| tb-00193 | OPPO Find X8 sạc nhanh 80W SuperVOOC | sạc nhanh 80W SuperVOOC | – |
| tb-00194 | OPPO Find X8 sạc không dây 50W AirVOOC | sạc không dây 50W AirVOOC | – |
| tb-00195 | OPPO Find X8 có khả năng chịu nước, bụi IP68 | khả năng chịu nước, bụi IP68/IP69 | – |
| tb-00196 | OPPO Find X8 có khả năng chịu nước, bụi IP69 | khả năng chịu nước, bụi IP68/IP69 | – |
| tb-00197 | Galaxy S25 Ultra có dung lượng pin 5000 mAh | dung lượng pin 5000 mAh | – |
| tb-00198 | Galaxy S25 Ultra có thời gian phát video lên đến 31 giờ | thời gian phát video lên đến 31 giờ | – |
| tb-00199 | Galaxy S25 Ultra có khả năng kháng nước IP68 | khả năng kháng nước IP68 bền bỉ. | – |
| tb-00200 | Galaxy S25 Ultra có tần số quét 120 Hz | tần số quét 120 Hz | – |
| tb-00201 | Galaxy S25 Ultra có zoom kỹ thuật số lên đến 100x | zoom kỹ thuật số lên đến 100x | – |
| tb-00202 | Galaxy S25 Ultra có tần số quét 120Hz | tần số quét 120Hz | – |
| tb-00203 | Galaxy S25 Ultra có zoom 100x | Zoom 100x | – |
| tb-00204 | Galaxy S25 Ultra có zoom quang học 3x | Zoom quang học 3x, 5x | – |
| tb-00205 | Galaxy S25 Ultra có zoom quang học 5x | Zoom quang học 3x, 5x | – |
| tb-00206 | Galaxy S25 Ultra có zoom kỹ thuật số lên đến 100x | Zoom kỹ thuật số lên đến 100x | – |
| tb-00207 | Galaxy S25 Ultra có pin dung lượng 5000mAh | pin dung lượng 5000mAh | – |
| tb-00208 | Galaxy S25 Ultra có thời gian phát video liên tục lên tới 31 giờ | thời gian phát video liên tục lên tới 31 giờ | – |
| tb-00209 | Galaxy S25 Ultra có độ bền chuẩn IP68 | độ bền chuẩn IP68 | – |
| tb-00210 | Galaxy S25 Ultra kháng nước ở độ sâu 1.5m trong 30 phút đạt chuẩn IP68 | kháng nước ở độ sâu 1.5m trong 30 phút đạt chuẩn IP68 | – |
| tb-00211 | Galaxy S25 Ultra có pin 6000mAh | Pin 6000mAh | – |
| tb-00212 | Galaxy S25 Ultra sạc nhanh 65W | sạc nhanh 65W | – |
| tb-00213 | Galaxy S25 Ultra có siêu màn hình Dynamic AMOLED 2X 120 Hz | Siêu màn hình Dynamic AMOLED 2X 120 Hz | – |
| tb-00214 | Galaxy S25 Ultra có camera Zoom 100x | camera Zoom 100x | – |
| tb-00215 | Galaxy S25 Ultra có màn hình 6.9” Quad HD+ 3120 × 1440, 120 Hz mượt mà | Màn hình 6.9” Quad HD+ 3120 × 1440, 120 Hz mượt mà | – |
| tb-00216 | Galaxy S25 Ultra có zoom quang học 3x | Zoom quang học 3x & 5x | – |
| tb-00217 | Galaxy S25 Ultra có zoom quang học 5x | Zoom quang học 3x & 5x | – |
| tb-00218 | Galaxy S25 Ultra có zoom kỹ thuật số lên tới 100x | Zoom kỹ thuật số lên tới 100x | – |
| tb-00219 | Galaxy S25 Ultra có pin 5000 mAh | Pin 5000 mAh | – |
| tb-00220 | Galaxy S25 Ultra có thời gian phát video lên tới 31 giờ | thời gian phát video lên tới 31 giờ | – |
| tb-00221 | Galaxy S25 Ultra có chuẩn IP68 chống nước/độ 1.5 m trong 30 phút | chuẩn IP68 chống nước/độ 1.5 m trong 30 phút | – |
| tb-00222 | Galaxy S25 Ultra có pin 6000 mAh | Pin 6000 mAh | – |
| tb-00223 | Galaxy S25 Ultra sạc nhanh 80W | sạc nhanh 80W | – |
| tb-00224 | Galaxy S25 Ultra có tần số 120 Hz | tần số 120 Hz | – |
| tb-00225 | Galaxy S25 Ultra có zoom quang học 3x | zoom quang học 3x/5x | – |
| tb-00226 | Galaxy S25 Ultra có zoom quang học 5x | zoom quang học 3x/5x | – |
| tb-00227 | Galaxy S25 Ultra có 100x kỹ thuật số | 100x kỹ thuật số | – |
| tb-00228 | Galaxy S25 Ultra có pin 5000 mAh | Pin 5000 mAh | – |
| tb-00229 | Galaxy S25 Ultra cho tới 31 giờ phát video | cho tới 31 giờ phát video | – |
| tb-00230 | Galaxy S25 Ultra có chuẩn IP68 kháng nước, bão | chuẩn IP68 kháng nước, bão | – |
| tb-00231 | Redmi Note 14 Pro+ 5G có chuẩn kháng nước, kháng bụi IP68 | chuẩn kháng nước, kháng bụi IP68 | – |
| tb-00232 | Redmi Note 14 Pro+ 5G có màn hình AMOLED 1.5K 120Hz | Màn hình AMOLED 1.5K 120Hz | – |
| tb-00233 | Redmi Note 14 Pro+ 5G có độ sáng cực đại 3000 nit | độ sáng cực đại 3000 nit | – |
| tb-00234 | Redmi Note 14 Pro+ 5G có pin 5110mAh | Pin 5110mAh | – |
| tb-00235 | Redmi Note 14 Pro+ 5G sạc nhanh HyperCharge 120W | sạc nhanh HyperCharge 120W | – |
| tb-00236 | Redmi Note 14 Pro+ 5G có camera thu phóng quang học 4X | camera thu phóng quang học 4X | – |
| tb-00237 | Redmi Note 14 Pro+ 5G có chuẩn kháng nước và bụi IP68 | chuẩn kháng nước và bụi IP68 | – |
| tb-00238 | Redmi Note 14 Pro+ 5G sạc siêu nhanh công suất 120W | Sạc siêu nhanh công suất 120W | – |
| tb-00239 | Redmi Note 14 Pro+ 5G có màn hình AMOLED 1.5K 120Hz | Màn hình AMOLED 1.5K 120Hz | – |
| tb-00240 | Redmi Note 14 Pro+ 5G có chuẩn chống nước và bụi IP68 | Chuẩn chống nước và bụi IP68 | – |
| tb-00241 | Redmi Note 14 Pro+ 5G có viên pin 5110mAh | Viên pin 5110mAh | – |
| tb-00242 | Redmi Note 14 Pro+ 5G sạc nhanh 120W HyperCharge | sạc nhanh 120W HyperCharge | – |
| tb-00243 | Redmi Note 14 Pro+ 5G có camera thu phóng quang học 4X | Camera thu phóng quang học 4X | – |
| tb-00244 | Redmi Note 14 Pro+ 5G có pin 5110mAh | pin 5110mAh | – |
| tb-00245 | Redmi Note 14 Pro+ 5G có tần số làm mới 120Hz | tần số làm mới 120Hz | – |
| tb-00246 | Redmi Note 14 Pro+ 5G có công nghệ HyperCharge 120W | công nghệ HyperCharge 120W | – |
| tb-00247 | Redmi Note 14 Pro+ 5G có độ sáng cực đại 3000 nit | độ sáng cực đại 3000 nit | – |
| tb-00248 | Redmi Note 14 Pro+ 5G có khả năng chống bụi và nước chuẩn IP68 | Khả năng chống bụi và nước chuẩn IP68 | – |
| tb-00249 | Redmi Note 14 Pro+ 5G có ống kính thu phóng quang học 2X | ống kính thu phóng quang học 2X/4X | – |
| tb-00250 | Redmi Note 14 Pro+ 5G có ống kính thu phóng quang học 4X | ống kính thu phóng quang học 2X/4X | – |
| tb-00251 | Redmi Note 14 Pro+ 5G có pin 5000mAh | Pin 5000mAh | – |
| tb-00252 | Redmi Note 14 Pro+ 5G sạc nhanh 67W | sạc nhanh 67W | – |
| tb-00253 | Redmi Note 14 Pro+ 5G có pin 5110 mAh | pin 5110 mAh | – |
| tb-00254 | Redmi Note 14 Pro+ 5G sạc 120W | sạc 120W | – |
| tb-00255 | Redmi Note 14 Pro+ 5G có màn hình AMOLED Crystal Res 6,67” 120 Hz | Màn hình AMOLED Crystal Res 6,67” 120 Hz | – |
| tb-00256 | Redmi Note 14 Pro+ 5G có độ sáng cực đại 3000 nit | độ sáng cực đại 3000 nit | – |
| tb-00257 | Redmi Note 14 Pro+ 5G chỉ 15 phút đầy 100 % | chỉ 15 phút đầy 100 % | – |
| tb-00258 | Redmi Note 14 Pro+ 5G dùng liên tục tới 19,5 giờ xem video | dùng liên tục tới 19,5 giờ xem video | – |
| tb-00259 | Redmi Note 14 Pro+ 5G dùng liên tục tới 9 giờ lướt mạng xã hội | 9 giờ lướt mạng xã hội | – |
| tb-00260 | Redmi Note 14 Pro+ 5G dùng liên tục tới 15 giờ chơi game | 15 giờ chơi game | – |
| tb-00261 | Redmi Note 14 Pro+ 5G có bảo vệ IP68 | bảo vệ IP68 | – |
| tb-00262 | Redmi Note 14 Pro+ 5G có độ sáng 3000 nit rõ ràng dưới ánh nắng mạnh | độ sáng 3000 nit thực sự rõ ràng dưới ánh nắng mạnh | – |
| tb-00263 | Redmi Note 14 Pro+ 5G có pin 5000mAh | Pin 5000mAh | – |
| tb-00264 | Redmi Note 14 Pro+ 5G sạc nhanh 67W | sạc nhanh 67W | – |
| tb-00265 | AirPods 4 có tổng thời gian nghe lên đến 30 giờ cùng hộp sạc USB-C tiện lợi | tổng thời gian nghe lên đến 30 giờ cùng hộp sạc USB-C tiện lợi | – |
| tb-00266 | AirPods 4 chống nước đạt chuẩn IP54 | chống nước đạt chuẩn IP54 | – |
| tb-00267 | AirPods 4 sạc nhanh chỉ với 5 phút trong hộp sạc giúp kéo dài thời gian nghe thêm khoảng 1 giờ | Sạc nhanh thông minh chỉ với 5 phút trong hộp sạc giúp kéo dài thời gian nghe thêm khoảng 1 giờ | – |
| tb-00268 | AirPods 4 có thời lượng pin ấn tượng lên đến 30 giờ | thời lượng pin ấn tượng lên đến 30 giờ | – |
| tb-00269 | AirPods 4 có chuẩn kháng nước IP54 | chuẩn kháng nước IP54 | – |
| tb-00270 | AirPods 4 có thể tận hưởng âm nhạc liên tục lên đến 5 giờ chỉ với một lần sạc đầy | Tận hưởng âm nhạc liên tục lên đến 5 giờ chỉ với một lần sạc đầy | – |
| tb-00271 | AirPods 4 có tổng thời gian nghe được mở rộng lên tới 30 giờ khi kết hợp cùng hộp sạc USB-C | tổng thời gian nghe được mở rộng lên tới 30 giờ | – |
| tb-00272 | AirPods 4 có 1 giờ sử dụng chỉ sau 5 phút đặt trong hộp sạc | 1 giờ sử dụng chỉ sau 5 phút đặt trong hộp sạc | – |
| tb-00273 | AirPods 4 có khả năng chống nước đạt chuẩn IP54 | nước đạt chuẩn IP54 | – |
| tb-00274 | AirPods 4 có thời lượng pin lên đến 30 giờ (kèm hộp sạc) | Thời lượng pin lên đến 30 giờ (kèm hộp sạc) | – |
| tb-00275 | AirPods 4 có thời lượng pin lên tới 30 giờ | thời lượng pin lên tới 30 giờ | – |
| tb-00276 | AirPods 4 có chống nước chuẩn IP54 | nước chuẩn IP54 | – |
| tb-00277 | AirPods 4 có thời lượng pin 5 giờ nghe nhạc liên tục mỗi lần sạc | 5 giờ nghe nhạc liên tục mỗi lần sạc | – |
| tb-00278 | AirPods 4 có thời lượng pin tổng cộng 30 giờ với hộp sạc USB‑C | tổng cộng 30 giờ với hộp sạc USB‑C | – |
| tb-00279 | AirPods 4 chỉ 5 phút sạc trong hộp đã tăng thêm 1 giờ thời gian sử dụng | chỉ 5 phút sạc trong hộp đã tăng thêm 1 giờ thời gian sử dụng | – |
| tb-00280 | AirPods 4 có pin kéo dài tới 30 giờ | Pin kéo dài tới 30 giờ | – |
| tb-00281 | AirPods 4 với chuẩn IP54 (chúng chống bụi, chống mồ hôi và chống nước) | Với chuẩn IP54, chúng chống bụi, chống mồ hôi và chống nước | – |
| tb-00282 | AirPods 4 cung cấp tới 30 giờ nghe nhạc liên tục với hộp sạc USB-C siêu gọn | cung cấp tới 30 giờ nghe nhạc liên tục | – |
| tb-00283 | AirPods 4 chỉ cần 5 phút sạc, bạn sẽ có thêm 1 giờ âm nhạc với hộp sạc USB-C siêu gọn | chỉ cần 5 phút sạc, bạn sẽ có thêm 1 giờ âm nhạc | – |
| tb-00284 | AirPods 4 có thời gian nghe lên đến 5 giờ cho mỗi lần sạc | Thời gian nghe lên đến 5 giờ cho mỗi lần sạc | – |
| tb-00285 | AirPods Pro 3 có khả năng chống nước IP57 | khả năng chống nước IP57 | – |
| tb-00286 | AirPods Pro 3 có thời lượng pin lên đến 8 giờ nghe liên tục khi bật Chủ Động Khử Tiếng Ồn | Lên đến 8 giờ nghe liên tục khi bật Chủ Động Khử Tiếng Ồn | – |
| tb-00287 | AirPods Pro 3 có thời lượng pin tổng cộng 24 giờ cùng hộp sạc MagSafe USB-C | tổng cộng 24 giờ cùng hộp sạc MagSafe USB-C | – |
| tb-00288 | AirPods Pro 3 có tính năng sạc nhanh 5 phút mang lại ngay 1 giờ sử dụng | tính năng sạc nhanh 5 phút mang lại ngay 1 giờ sử dụng | – |
| tb-00289 | AirPods Pro 3 có tính năng Thiết Bị Trợ Thính lên đến 10 giờ | tính năng Thiết Bị Trợ Thính lên đến 10 giờ | – |
| tb-00290 | AirPods Pro 3 chống nước IP57 cho cả tai nghe và hộp sạc | chống nước IP57 cho cả tai nghe và hộp sạc | – |
| tb-00291 | AirPods Pro 3 có chống nước IP57 | chống nước IP57 | – |
| tb-00292 | AirPods Pro 3 có thời lượng pin lên đến 8 giờ nghe liên tục khi bật Chủ Động Khử Tiếng Ồn | Thời lượng pin lên đến 8 giờ nghe liên tục khi bật Chủ Động Khử Tiếng Ồn | – |
| tb-00293 | AirPods Pro 3 có thời lượng pin tổng cộng 24 giờ cùng hộp sạc MagSafe USB-C | tổng cộng 24 giờ cùng hộp sạc MagSafe USB-C. | – |
| tb-00294 | AirPods Pro 3 sạc nhanh thông minh chỉ 5 phút trong hộp sạc mang lại 1 giờ nghe nhạc không gián đoạn | Sạc nhanh thông minh chỉ 5 phút trong hộp sạc mang lại 1 giờ nghe nhạc không gián đoạn | – |
| tb-00295 | AirPods Pro 3 có thời lượng pin lên tới 6 giờ liên tục | thời lượng pin lên tới 6 giờ liên tục | – |
| tb-00296 | AirPods Pro 3 chống nước IPX4 | chống nước IPX4 | – |
| tb-00297 | AirPods Pro 3 có chống nước chuẩn IP57 | nước chuẩn IP57 | – |
| tb-00298 | AirPods Pro 3 chỉ 5 phút trong hộp tăng thời gian nghe thêm 1 giờ với hộp sạc MagSafe (USB‑C) | chỉ 5 phút trong hộp tăng thời gian nghe thêm 1 giờ | – |
| tb-00299 | AirPods Pro 3 có tổng thời gian nghe lên tới 24 giờ với MagSafe (USB‑C) | tổng thời gian nghe lên tới 24 giờ | – |
| tb-00300 | AirPods Pro 3 có thời lượng pin lên tới 6 giờ sử dụng liên tục | Thời lượng pin lên tới 6 giờ sử dụng liên tục | – |
| tb-00301 | AirPods Pro 3 có thời lượng pin 30 giờ với hộp sạc không dây | 30 giờ với hộp sạc không dây | – |
| tb-00302 | AirPods Pro 3 cho tới 8 giờ nghe liên tục | cho tới 8 giờ nghe liên tục | – |
| tb-00303 | AirPods Pro 3 có chống nước chuẩn IP57 | nước chuẩn IP57 | – |
| tb-00304 | AirPods Pro 3 có hộp sạc MagSafe hỗ trợ Qi, USB‑C, cho 24 giờ năng lượng chỉ với một lần sạc | Hộp sạc MagSafe hỗ trợ Qi, USB‑C, cho 24 giờ năng lượng chỉ với một lần sạc | – |
| tb-00305 | AirPods Pro 3 chỉ 5 phút sạc, bạn có thêm 1 giờ nghe nhạc | Chỉ 5 phút sạc, bạn có thêm 1 giờ nghe nhạc | – |
| tb-00306 | Redmi Buds 6 Pro có thời gian phát nhạc liên tục lên đến 36 giờ khi dùng kèm hộp sạc | Thời gian phát nhạc liên tục lên đến 36 giờ khi dùng kèm hộp sạc | – |
| tb-00307 | Redmi Buds 6 Pro có chuẩn kháng nước IP54 | chuẩn kháng nước IP54 | – |
| tb-00308 | Redmi Buds 6 Pro có thời lượng sử dụng lên tới 36 giờ | thời lượng sử dụng vượt trội lên tới 36 giờ | – |
| tb-00309 | Redmi Buds 6 Pro có tính năng sạc nhanh 5 phút cho 2 giờ phát nhạc | tính năng sạc nhanh 5 phút cho 2 giờ phát nhạc. | – |
| tb-00310 | Redmi Buds 6 Pro có tổng thời gian sử dụng lên tới 36 giờ cùng hộp sạc | Tổng thời gian sử dụng lên tới 36 giờ cùng hộp sạc | – |
| tb-00311 | Redmi Buds 6 Pro có thời lượng pin lên tới 36 giờ khi kết hợp cùng hộp sạc | Thời lượng pin bền bỉ lên tới 36 giờ khi kết hợp cùng hộp sạc | – |
| tb-00312 | Redmi Buds 6 Pro sạc nhanh chỉ 5 phút sạc cho 2 giờ nghe nhạc liên tục | chỉ 5 phút sạc cho 2 giờ nghe nhạc liên tục | – |
| tb-00313 | Redmi Buds 6 Pro có thời lượng pin lên tới 36 giờ gồm tai nghe và hộp sạc | Thời lượng pin lên tới 36 giờ (2 giờ tai nghe + 34 giờ hộp sạc) | – |
| tb-00314 | Redmi Buds 6 Pro có thời lượng pin 2 giờ ở tai nghe | Thời lượng pin lên tới 36 giờ (2 giờ tai nghe + 34 giờ hộp sạc) | bo_phan=hop_sac: “hộp sạc”; kieu_gia_tri=toi_da: “tới” |
| tb-00315 | Redmi Buds 6 Pro có thêm 34 giờ thời lượng pin từ hộp sạc | Thời lượng pin lên tới 36 giờ (2 giờ tai nghe + 34 giờ hộp sạc) | bo_phan=tai_nghe: “tai nghe”; kieu_gia_tri=toi_da: “tới” |
| tb-00316 | Redmi Buds 6 Pro sạc nhanh 5 phút chỉ đủ phát nhạc 2 giờ | Sạc nhanh 5 phút chỉ đủ phát nhạc 2 giờ | – |
| tb-00317 | Redmi Buds 6 Pro có pin tích hợp 54 mAh (tai nghe) | Pin tích hợp 54 mAh (tai nghe) | – |
| tb-00318 | Redmi Buds 6 Pro có pin 480 mAh (hộp sạc) | 480 mAh (hộp sạc) | – |
| tb-00319 | Redmi Buds 6 Pro có thời lượng pin lên tới 30 giờ gồm tai nghe và hộp sạc | Thời lượng pin lên tới 30 giờ: 5 giờ nghe liên tục sau mỗi lần sạc, kèm 25 giờ dự phòng trong hộp sạc | hoat_dong=chua_ro_hoat_dong: “liên tục” |
| tb-00320 | Redmi Buds 6 Pro có 5 giờ nghe liên tục sau mỗi lần sạc | Thời lượng pin lên tới 30 giờ: 5 giờ nghe liên tục sau mỗi lần sạc, kèm 25 giờ dự phòng trong hộp sạc | bo_phan=hop_sac: “hộp sạc”; kieu_gia_tri=toi_da: “tới” |
| tb-00321 | Redmi Buds 6 Pro có 25 giờ dự phòng trong hộp sạc | Thời lượng pin lên tới 30 giờ: 5 giờ nghe liên tục sau mỗi lần sạc, kèm 25 giờ dự phòng trong hộp sạc | bo_phan=tai_nghe: “mỗi lần sạc”; hoat_dong=chua_ro_hoat_dong: “liên tục”; kieu_gia_tri=toi_da: “tới” |
| tb-00322 | Redmi Buds 6 Pro có thời lượng pin 36 giờ cùng hộp sạc | Thời lượng pin 36 giờ cùng hộp sạc | – |
| tb-00323 | Redmi Buds 6 Pro chỉ 5 phút sạc nhanh cho 2 giờ phát nhạc | chỉ 5 phút sạc nhanh cho 2 giờ phát nhạc | – |
| tb-00324 | Redmi Buds 6 Pro có pin lên tới 8 giờ liên tục | Pin siêu bền lên tới 8 giờ liên tục | – |
| tb-00325 | Redmi Buds 6 Pro có kèm hộp sạc nhanh cho 24 giờ sử dụng không gián đoạn | kèm hộp sạc nhanh cho 24 giờ sử dụng không gián đoạn | – |
