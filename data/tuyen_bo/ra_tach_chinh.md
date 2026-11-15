# Rà tách chinh.jsonl: cụm có trong câu gốc mà không có trong tuyên bố

Sinh bằng `scripts/ra_tach.py` từ `data/tuyen_bo/chinh.jsonl` và `data/cau_hinh/*.yaml` (cụm của phụ lục mục 13), từ khẳng định (mục 6.2) và cụm phủ nhiều giá trị (mục 6.8) của `data/huong_dan_gan_nhan.md`. Chỉ so chuỗi: không đề xuất cách sửa, không nêu nhãn. Người thực hiện tự quyết từng chỗ theo bốn tiêu chí gắn điều kiện (mục 2 của hướng dẫn).

- Cụm thấy ở đây có thể thuộc con số khác của cùng câu gốc hoặc là tên tính năng (tiêu chí 3); không thấy cụm nào không có nghĩa tuyên bố đủ điều kiện, vì cụm ngoài cấu hình không được dò.
- Chỉ xét các điều kiện của thuộc tính ghi trên tuyên bố.
- Đã lọc theo mẫu: dh-apple-watchse3, dt-xiaomi-15t.
- 12 / 41 tuyên bố có cụm được liệt kê.

| Mã | Tuyên bố | Câu gốc | Cụm có trong câu gốc, không có trong tuyên bố |
|---|---|---|---|
| tb-00067 | Apple Watch SE 3 có thời lượng pin lên đến 18 giờ | Duy trì kết nối liên tục suốt ngày dài với thời lượng pin lên đến 18 giờ và khả năng sạc nhanh vượt trội, hỗ trợ sạc 80% chỉ trong 45 phút. | hoat_dong=chua_ro_hoat_dong: “liên tục” |
| tb-00068 | Apple Watch SE 3 hỗ trợ sạc nhanh 80% chỉ trong 45 phút | Duy trì kết nối liên tục suốt ngày dài với thời lượng pin lên đến 18 giờ và khả năng sạc nhanh vượt trội, hỗ trợ sạc 80% chỉ trong 45 phút. | hoat_dong=chua_ro_hoat_dong: “liên tục”; kieu_gia_tri=toi_da: “lên đến” |
| tb-00069 | Apple Watch SE 3 có độ sáng màn hình tối đa 1000 nit (hiển thị rõ nét dưới ánh nắng) | Màn hình Retina OLED luôn bật với kính cường lực Ion-X chống nứt gấp 4 lần và độ sáng tối đa 1000 nit hiển thị rõ nét dưới ánh nắng. | từ khẳng định: “luôn” |
| tb-00070 | Apple Watch SE 3 có khả năng chống nước ở độ sâu 50m (khi bơi lội) | Vỏ nhôm cao cấp với hai tùy chọn kích thước 40mm và 44mm, khả năng chống nước ở độ sâu 50m sẵn sàng đồng hành khi bơi lội. | – |
| tb-00071 | Apple Watch SE 3 có thời lượng pin lên đến 18 giờ (khi sử dụng thông thường) và 32 giờ (ở Chế Độ Nguồn Điện Thấp) | Thời lượng pin ấn tượng lên đến 18 giờ sử dụng thông thường và 32 giờ ở Chế Độ Nguồn Điện Thấp. | – |
| tb-00072 | Apple Watch SE 3 hỗ trợ sạc nhanh đạt 80% pin chỉ trong khoảng 45 phút | Hỗ trợ sạc nhanh vượt trội, đạt 80% pin chỉ trong khoảng 45 phút. | – |
| tb-00073 | Apple Watch SE 3 có khả năng chống nước ở độ sâu 50m (trong buổi tập bơi lội) | Khả năng chống nước ở độ sâu 50m, sẵn sàng đồng hành trong mọi buổi tập bơi lội. | – |
| tb-00074 | Apple Watch SE 3 có thời lượng pin bền cả ngày | Pin bền cả ngày, sạc nhanh 45 phút lên 80% giúp bạn luôn sẵn sàng. | từ khẳng định: “luôn” |
| tb-00075 | Apple Watch SE 3 sạc nhanh 45 phút lên 80% pin | Pin bền cả ngày, sạc nhanh 45 phút lên 80% giúp bạn luôn sẵn sàng. | từ khẳng định: “luôn” |
| tb-00076 | Apple Watch SE 3 có độ sáng màn hình 1000 nit | Màn hình 44 mm, độ sáng 1000 nit, kính Ion‑X chịu va đập gấp 4 lần. | – |
| tb-00077 | Apple Watch SE 3 có khả năng chống nước 50 m | Khả năng chống nước 50 m, loa và micrô tích hợp cho gọi và phát nhạc | – |
| tb-00078 | Apple Watch SE 3 có thời lượng pin lên tới 18 giờ (khi sử dụng bình thường) | Pin bền cả ngày, lên tới 18 giờ sử dụng bình thường và sạc nhanh 80 % chỉ trong 45 phút, giúp bạn luôn sẵn sàng cho mọi hoạt động. | từ khẳng định: “luôn”; cụm phủ: “mọi hoạt động” |
| tb-00079 | Apple Watch SE 3 có màn hình Retina Luôn Bật sáng tới 1000 nit | Màn hình Retina Luôn Bật sáng tới 1000 nit, | – |
| tb-00080 | Apple Watch SE 3 có thời lượng pin lên tới 18 giờ | Thiết kế nhẹ nhàng, thời lượng pin lên tới 18 giờ, phù hợp cho mọi công việc và hoạt động ngoài trời. | – |
| tb-00081 | Xiaomi 15T có tần số quét màn hình 120Hz | Màn hình AMOLED 6.83 inch độ phân giải 1.5K, tần số quét 120Hz cùng độ sáng tối đa 3200 nits. | kieu_gia_tri=toi_da: “tối đa” |
| tb-00082 | Xiaomi 15T có độ sáng màn hình tối đa 3200 nits | Màn hình AMOLED 6.83 inch độ phân giải 1.5K, tần số quét 120Hz cùng độ sáng tối đa 3200 nits. | – |
| tb-00083 | Xiaomi 15T có dung lượng pin 5500mAh | Vi xử lý MediaTek Dimensity 8400-Ultra kết hợp pin 5500mAh và công nghệ sạc nhanh HyperCharge 67W. | – |
| tb-00084 | Xiaomi 15T có công nghệ sạc nhanh HyperCharge công suất 67W | Vi xử lý MediaTek Dimensity 8400-Ultra kết hợp pin 5500mAh và công nghệ sạc nhanh HyperCharge 67W. | – |
| tb-00085 | Xiaomi 15T có màn hình tần số quét 120Hz | Subheadline: Trải nghiệm kiệt tác công nghệ di động thế hệ mới với hệ thống ống kính Leica chuyên nghiệp, màn hình bảo vệ mắt 120Hz và viên pin 5500mAh bền bỉ trong một thiết kế mỏng nhẹ tinh tế. | – |
| tb-00086 | Xiaomi 15T có viên pin dung lượng 5500mAh | Subheadline: Trải nghiệm kiệt tác công nghệ di động thế hệ mới với hệ thống ống kính Leica chuyên nghiệp, màn hình bảo vệ mắt 120Hz và viên pin 5500mAh bền bỉ trong một thiết kế mỏng nhẹ tinh tế. | – |
| tb-00087 | Xiaomi 15T có màn hình độ sáng 3200 nit (hiển thị rõ nét dưới ánh nắng gắt) | Màn hình AMOLED 6.83 inch siêu sáng 3200 nit kết hợp tần số quét 120Hz: Tận hưởng không gian giải trí sống động với độ phân giải 1.5K hiển thị rõ nét ngay dưới ánh nắng gắt, đồng thời bảo vệ thị lực tối đa nhờ đạt 3 chứng nhận uy tín từ TÜV Rheinland. | kieu_gia_tri=toi_da: “tối đa”; tu_goi_muc_cao: “tối đa” |
| tb-00088 | Xiaomi 15T có tần số quét màn hình 120Hz | Màn hình AMOLED 6.83 inch siêu sáng 3200 nit kết hợp tần số quét 120Hz: Tận hưởng không gian giải trí sống động với độ phân giải 1.5K hiển thị rõ nét ngay dưới ánh nắng gắt, đồng thời bảo vệ thị lực tối đa nhờ đạt 3 chứng nhận uy tín từ TÜV Rheinland. | kieu_gia_tri=toi_da: “tối đa” |
| tb-00089 | Xiaomi 15T có dung lượng pin 5500mAh | Hiệu năng Dimensity 8400-Ultra mạnh mẽ cùng thời lượng pin 5500mAh: Xử lý mượt mà mọi tác vụ nhờ chip tiến trình 4nm hiện đại, hệ thống tản nhiệt 3D IceLoop vượt trội và công nghệ sạc nhanh HyperCharge 67W giúp nạp đầy 100% pin chỉ trong 50 phút. | – |
| tb-00090 | Xiaomi 15T có công nghệ sạc nhanh HyperCharge công suất 67W | Hiệu năng Dimensity 8400-Ultra mạnh mẽ cùng thời lượng pin 5500mAh: Xử lý mượt mà mọi tác vụ nhờ chip tiến trình 4nm hiện đại, hệ thống tản nhiệt 3D IceLoop vượt trội và công nghệ sạc nhanh HyperCharge 67W giúp nạp đầy 100% pin chỉ trong 50 phút. | – |
| tb-00091 | Xiaomi 15T nạp đầy 100% pin chỉ trong 50 phút (với công nghệ sạc nhanh HyperCharge 67W) | Hiệu năng Dimensity 8400-Ultra mạnh mẽ cùng thời lượng pin 5500mAh: Xử lý mượt mà mọi tác vụ nhờ chip tiến trình 4nm hiện đại, hệ thống tản nhiệt 3D IceLoop vượt trội và công nghệ sạc nhanh HyperCharge 67W giúp nạp đầy 100% pin chỉ trong 50 phút. | – |
| tb-00092 | Xiaomi 15T có tần số làm mới màn hình 120Hz | Với màn hình 6.7 inch AMOLED, độ phân giải 2K và tần số làm mới 120Hz, mọi hình ảnh đều sống động, sắc nét và phản hồi nhanh chóng. | – |
| tb-00093 | Xiaomi 15T có dung lượng pin 5000mAh | Pin 5000mAh hỗ trợ sạc nhanh 120W, chỉ trong 20 phút bạn đã có đầy năng lượng cho cả ngày. | – |
| tb-00094 | Xiaomi 15T sạc đầy năng lượng trong 20 phút (với sạc nhanh 120W) | Pin 5000mAh hỗ trợ sạc nhanh 120W, chỉ trong 20 phút bạn đã có đầy năng lượng cho cả ngày. | – |
| tb-00095 | Xiaomi 15T có độ sáng màn hình 3200 nit | Màn hình AMOLED 6.83” với độ sáng 3200 nit, tần số quét 120Hz và công nghệ bảo vệ mắt TÜV Rheinland, cho hình ảnh rực rỡ và an toàn cho mắt. | – |
| tb-00096 | Xiaomi 15T có tần số quét màn hình 120Hz | Màn hình AMOLED 6.83” với độ sáng 3200 nit, tần số quét 120Hz và công nghệ bảo vệ mắt TÜV Rheinland, cho hình ảnh rực rỡ và an toàn cho mắt. | – |
| tb-00097 | Xiaomi 15T có dung lượng pin 5500mAh (cho tới 13 giờ sử dụng liên tục) | Pin 5500mAh cùng sạc nhanh HyperCharge 67W, cho tới 13 giờ sử dụng liên tục và chỉ 50 phút sạc đầy 100 %. | – |
| tb-00098 | Xiaomi 15T hỗ trợ sạc nhanh HyperCharge công suất 67W | Pin 5500mAh cùng sạc nhanh HyperCharge 67W, cho tới 13 giờ sử dụng liên tục và chỉ 50 phút sạc đầy 100 %. | kieu_gia_tri=toi_da: “tới” |
| tb-00099 | Xiaomi 15T sạc đầy 100% pin chỉ trong 50 phút (với sạc nhanh HyperCharge 67W) | Pin 5500mAh cùng sạc nhanh HyperCharge 67W, cho tới 13 giờ sử dụng liên tục và chỉ 50 phút sạc đầy 100 %. | kieu_gia_tri=toi_da: “tới” |
| tb-00100 | Xiaomi 15T có tần số làm mới màn hình 120 Hz | Màn hình AMOLED 6.7 inch với tần số làm mới 120 Hz hiển thị sắc nét, màu sắc sống động | – |
| tb-00101 | Xiaomi 15T có công nghệ sạc nhanh công suất 120 W (sạc chỉ trong 15 phút) | Công nghệ sạc nhanh 120 W chỉ trong 15 phút, bạn luôn luôn sẵn sàng. | từ khẳng định: “luôn” |
| tb-00102 | Xiaomi 15T có độ sáng màn hình 3200 nits (ngay cả dưới ánh sáng mạnh) | Caption: Xiaomi 15T mang màn hình 6.83” AMOLED 3200 nits, 120Hz, bảo vệ mắt TÜV Rheinland, cho hình ảnh sáng rõ ngay cả dưới ánh sáng mạnh | – |
| tb-00103 | Xiaomi 15T có tần số quét màn hình 120Hz | Caption: Xiaomi 15T mang màn hình 6.83” AMOLED 3200 nits, 120Hz, bảo vệ mắt TÜV Rheinland, cho hình ảnh sáng rõ ngay cả dưới ánh sáng mạnh | – |
| tb-00104 | Xiaomi 15T có dung lượng pin 5500 mAh | Pin 5500 mAh kèm sạc HyperCharge 67W, đầy 100% trong 50 phút | – |
| tb-00105 | Xiaomi 15T có sạc HyperCharge công suất 67W | Pin 5500 mAh kèm sạc HyperCharge 67W, đầy 100% trong 50 phút | – |
| tb-00106 | Xiaomi 15T sạc đầy 100% pin trong 50 phút (với sạc HyperCharge 67W) | Pin 5500 mAh kèm sạc HyperCharge 67W, đầy 100% trong 50 phút | – |
| tb-00107 | Xiaomi 15T đạt chuẩn IP68 chống nước, bụi | chuẩn IP68 chống nước, bụi | – |
