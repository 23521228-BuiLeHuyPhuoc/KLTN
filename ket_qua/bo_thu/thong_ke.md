# Thống kê bộ thử và phương án quy mô (Bước 16)

Sinh bằng `scripts/thong_ke_bo_thu.py`. Chỉ có số liệu và phương án, không có kết luận. Số thập phân dùng dấu phẩy.

Bộ thử: 24 bài, 66 tuyên bố, 2 mẫu (iPhone 17, Galaxy Buds3 Pro).

## Phân bố nhãn lượt 2

Nguồn: `data/nhan/thu_luot2.jsonl`, 66 tuyên bố. Trường `nguoi_gan`: claude 59, phuoc 7.

### Tổng

| Nhãn | Số tuyên bố | Tỷ lệ |
| --- | --- | --- |
| Đúng | 34 | 51,5% |
| Lệch | 18 | 27,3% |
| Sai | 6 | 9,1% |
| Chưa đủ thông tin | 8 | 12,1% |
| Tổng | 66 | 100,0% |

### Theo mẫu, LLM, chế độ và loại bài

Mỗi ô là số tuyên bố, kèm tỷ lệ trên tổng của hàng.

| Cách tách | Giá trị | Đúng | Lệch | Sai | Chưa đủ thông tin | Tổng |
| --- | --- | --- | --- | --- | --- | --- |
| Chế độ | ten | 3 (20,0%) | 2 (13,3%) | 6 (40,0%) | 4 (26,7%) | 15 |
| Chế độ | ten_thong_so | 31 (60,8%) | 16 (31,4%) | 0 (0,0%) | 4 (7,8%) | 51 |
| LLM | gemini-3.6-flash | 16 (51,6%) | 11 (35,5%) | 0 (0,0%) | 4 (12,9%) | 31 |
| LLM | openai/gpt-oss-120b | 18 (51,4%) | 7 (20,0%) | 6 (17,1%) | 4 (11,4%) | 35 |
| Loại bài | description | 11 (55,0%) | 3 (15,0%) | 3 (15,0%) | 3 (15,0%) | 20 |
| Loại bài | landing | 15 (50,0%) | 10 (33,3%) | 2 (6,7%) | 3 (10,0%) | 30 |
| Loại bài | social | 8 (50,0%) | 5 (31,2%) | 1 (6,2%) | 2 (12,5%) | 16 |
| Mẫu | Galaxy Buds3 Pro | 11 (35,5%) | 8 (25,8%) | 4 (12,9%) | 8 (25,8%) | 31 |
| Mẫu | iPhone 17 | 23 (65,7%) | 10 (28,6%) | 2 (5,7%) | 0 (0,0%) | 35 |

### Dòng D

Nhãn đi kèm lấy từ dữ liệu.

| Dòng | Nội dung | Nhãn | Số tuyên bố |
| --- | --- | --- | --- |
| D1 | Tài liệu không có con số nào cho thuộc tính | Chưa đủ thông tin 2 | 2 (3,0%) |
| D1b | Tài liệu mâu thuẫn ở điều kiện của tuyên bố | Chưa đủ thông tin 5 | 5 (7,6%) |
| D2 | Từ khẳng định cho mức không cao hơn mức "lên đến" | Lệch 1 | 1 (1,5%) |
| D3 | Khớp ở đúng điều kiện | Đúng 34 | 34 (51,5%) |
| D4 | Giá trị công bố ở điều kiện khác | Lệch 17 | 17 (25,8%) |
| D5 | Mâu thuẫn hoặc thuận lợi hơn mọi giá trị công bố | Sai 6 | 6 (9,1%) |
| D6 | Có số nhưng không công bố ở điều kiện của tuyên bố | Chưa đủ thông tin 1 | 1 (1,5%) |

## Số tuyên bố mỗi bài

24 bài của bộ thử, 66 tuyên bố. Bài không có tuyên bố nào vẫn được tính (số 0).

### Thuộc tính được tính là có điều kiện

Một tuyên bố là tuyên bố có điều kiện khi thuộc tính của nó có `dieu_kien_bat_buoc` không rỗng trong cấu hình của nhóm mẫu (`data/cau_hinh/<nhóm>.yaml`).

| Nhóm | Thuộc tính | Điều kiện bắt buộc | Có điều kiện | Tuyên bố của bộ thử |
| --- | --- | --- | --- | --- |
| Điện thoại | thoi_luong_pin | hoat_dong, phien_ban | có | 9 |
| Điện thoại | sac_nhanh | bo_tiep_hop, cach_sac, moc_phan_tram | có | 6 |
| Điện thoại | cong_suat_sac | bo_tiep_hop, cach_sac | có | 2 |
| Điện thoại | do_sang | che_do_hien_thi, dien_tich_do | có | 5 |
| Điện thoại | tan_so_quet | kieu_tan_so | có | 7 |
| Điện thoại | zoom | loai_zoom, dai_luong, che_do_camera | có | 2 |
| Điện thoại | khang_nuoc | do_sau, thoi_gian_ngam, loai_nuoc, hoat_dong_bi_cam | có | 4 |
| Điện thoại | dung_luong_pin | kieu_dung_luong, phien_ban | có | 0 |
| Tai nghe | thoi_luong_pin | che_do_chong_on, bo_phan, hoat_dong | có | 18 |
| Tai nghe | sac_nhanh | so_phut_sac, bo_phan | có | 2 |
| Tai nghe | khang_nuoc | bo_phan, do_sau, thoi_gian_ngam, loai_nuoc, hoat_dong_bi_cam | có | 7 |
| Tai nghe | dung_luong_pin | bo_phan | có | 4 |
| Đồng hồ | thoi_luong_pin | che_do_nguon, hoat_dong, phien_ban | có | 0 |
| Đồng hồ | sac_nhanh | bo_tiep_hop, cap_sac, moc_phan_tram, so_phut_sac, hoat_dong | có | 0 |
| Đồng hồ | khang_nuoc | chuan_do_sau, hoat_dong_cho_phep | có | 0 |
| Đồng hồ | do_sang | che_do_hien_thi | có | 0 |

Tuyên bố có điều kiện: 66/66. Mọi thuộc tính có tuyên bố trong bộ thử đều có điều kiện bắt buộc, nên số tuyên bố có điều kiện mỗi bài bằng số tuyên bố mỗi bài.

### Số tuyên bố mỗi bài

Độ lệch chuẩn là độ lệch chuẩn mẫu (chia n − 1).

| Nhóm | Số bài | Tuyên bố | Trung bình | Trung vị | Độ lệch chuẩn | Nhỏ nhất | Lớn nhất | Bài 0 tuyên bố |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tất cả | 24 | 66 | 2,75 | 2,5 | 2,13 | 0 | 8 | 4/24 |
| Chế độ: ten | 12 | 15 | 1,25 | 1 | 1,14 | 0 | 3 | 4/12 |
| Chế độ: ten_thong_so | 12 | 51 | 4,25 | 4 | 1,82 | 2 | 8 | 0/12 |
| LLM: gemini-3.6-flash | 12 | 31 | 2,58 | 1,5 | 2,84 | 0 | 8 | 4/12 |
| LLM: openai/gpt-oss-120b | 12 | 35 | 2,92 | 3 | 1,16 | 1 | 5 | 0/12 |
| Loại bài: description | 8 | 20 | 2,50 | 2,5 | 1,93 | 0 | 5 | 2/8 |
| Loại bài: landing | 8 | 30 | 3,75 | 3,5 | 2,60 | 1 | 8 | 0/8 |
| Loại bài: social | 8 | 16 | 2,00 | 2 | 1,60 | 0 | 4 | 2/8 |
| Mẫu: Galaxy Buds3 Pro | 12 | 31 | 2,58 | 2,5 | 2,11 | 0 | 8 | 2/12 |
| Mẫu: iPhone 17 | 12 | 35 | 2,92 | 3 | 2,23 | 0 | 7 | 2/12 |
| Mẫu và chế độ: Galaxy Buds3 Pro / ten | 6 | 9 | 1,50 | 1,5 | 1,38 | 0 | 3 | 2/6 |
| Mẫu và chế độ: Galaxy Buds3 Pro / ten_thong_so | 6 | 22 | 3,67 | 3 | 2,25 | 2 | 8 | 0/6 |
| Mẫu và chế độ: iPhone 17 / ten | 6 | 6 | 1,00 | 1 | 0,89 | 0 | 2 | 2/6 |
| Mẫu và chế độ: iPhone 17 / ten_thong_so | 6 | 29 | 4,83 | 4,5 | 1,17 | 4 | 7 | 0/6 |

### Số tuyên bố có điều kiện mỗi bài

Cột cuối so trung bình với ngưỡng 2 ở rủi ro "quá ít tuyên bố có điều kiện" (T9.1).

| Nhóm | Số bài | Tuyên bố | Trung bình | Trung vị | Độ lệch chuẩn | Nhỏ nhất | Lớn nhất | Bài 0 tuyên bố | Trung bình dưới 2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tất cả | 24 | 66 | 2,75 | 2,5 | 2,13 | 0 | 8 | 4/24 | không |
| Chế độ: ten | 12 | 15 | 1,25 | 1 | 1,14 | 0 | 3 | 4/12 | có |
| Chế độ: ten_thong_so | 12 | 51 | 4,25 | 4 | 1,82 | 2 | 8 | 0/12 | không |
| LLM: gemini-3.6-flash | 12 | 31 | 2,58 | 1,5 | 2,84 | 0 | 8 | 4/12 | không |
| LLM: openai/gpt-oss-120b | 12 | 35 | 2,92 | 3 | 1,16 | 1 | 5 | 0/12 | không |
| Loại bài: description | 8 | 20 | 2,50 | 2,5 | 1,93 | 0 | 5 | 2/8 | không |
| Loại bài: landing | 8 | 30 | 3,75 | 3,5 | 2,60 | 1 | 8 | 0/8 | không |
| Loại bài: social | 8 | 16 | 2,00 | 2 | 1,60 | 0 | 4 | 2/8 | không |
| Mẫu: Galaxy Buds3 Pro | 12 | 31 | 2,58 | 2,5 | 2,11 | 0 | 8 | 2/12 | không |
| Mẫu: iPhone 17 | 12 | 35 | 2,92 | 3 | 2,23 | 0 | 7 | 2/12 | không |
| Mẫu và chế độ: Galaxy Buds3 Pro / ten | 6 | 9 | 1,50 | 1,5 | 1,38 | 0 | 3 | 2/6 | có |
| Mẫu và chế độ: Galaxy Buds3 Pro / ten_thong_so | 6 | 22 | 3,67 | 3 | 2,25 | 2 | 8 | 0/6 | không |
| Mẫu và chế độ: iPhone 17 / ten | 6 | 6 | 1,00 | 1 | 0,89 | 0 | 2 | 2/6 | có |
| Mẫu và chế độ: iPhone 17 / ten_thong_so | 6 | 29 | 4,83 | 4,5 | 1,17 | 4 | 7 | 0/6 | không |

### Từng bài

| Mã bài | Mẫu | LLM | Loại bài | Chế độ | Tuyên bố | Có điều kiện |
| --- | --- | --- | --- | --- | --- | --- |
| qc-dt-apple-iphone17-gemini-description-ten-1 | iPhone 17 | gemini-3.6-flash | description | ten | 0 | 0 |
| qc-dt-apple-iphone17-gemini-description-ten_thong_so-1 | iPhone 17 | gemini-3.6-flash | description | ten_thong_so | 5 | 5 |
| qc-dt-apple-iphone17-gemini-landing-ten-1 | iPhone 17 | gemini-3.6-flash | landing | ten | 1 | 1 |
| qc-dt-apple-iphone17-gemini-landing-ten_thong_so-1 | iPhone 17 | gemini-3.6-flash | landing | ten_thong_so | 7 | 7 |
| qc-dt-apple-iphone17-gemini-social-ten-1 | iPhone 17 | gemini-3.6-flash | social | ten | 0 | 0 |
| qc-dt-apple-iphone17-gemini-social-ten_thong_so-1 | iPhone 17 | gemini-3.6-flash | social | ten_thong_so | 4 | 4 |
| qc-dt-apple-iphone17-gptoss-description-ten-1 | iPhone 17 | openai/gpt-oss-120b | description | ten | 2 | 2 |
| qc-dt-apple-iphone17-gptoss-description-ten_thong_so-1 | iPhone 17 | openai/gpt-oss-120b | description | ten_thong_so | 5 | 5 |
| qc-dt-apple-iphone17-gptoss-landing-ten-1 | iPhone 17 | openai/gpt-oss-120b | landing | ten | 2 | 2 |
| qc-dt-apple-iphone17-gptoss-landing-ten_thong_so-1 | iPhone 17 | openai/gpt-oss-120b | landing | ten_thong_so | 4 | 4 |
| qc-dt-apple-iphone17-gptoss-social-ten-1 | iPhone 17 | openai/gpt-oss-120b | social | ten | 1 | 1 |
| qc-dt-apple-iphone17-gptoss-social-ten_thong_so-1 | iPhone 17 | openai/gpt-oss-120b | social | ten_thong_so | 4 | 4 |
| qc-tn-samsung-buds3pro-gemini-description-ten-1 | Galaxy Buds3 Pro | gemini-3.6-flash | description | ten | 0 | 0 |
| qc-tn-samsung-buds3pro-gemini-description-ten_thong_so-1 | Galaxy Buds3 Pro | gemini-3.6-flash | description | ten_thong_so | 3 | 3 |
| qc-tn-samsung-buds3pro-gemini-landing-ten-1 | Galaxy Buds3 Pro | gemini-3.6-flash | landing | ten | 1 | 1 |
| qc-tn-samsung-buds3pro-gemini-landing-ten_thong_so-1 | Galaxy Buds3 Pro | gemini-3.6-flash | landing | ten_thong_so | 8 | 8 |
| qc-tn-samsung-buds3pro-gemini-social-ten-1 | Galaxy Buds3 Pro | gemini-3.6-flash | social | ten | 0 | 0 |
| qc-tn-samsung-buds3pro-gemini-social-ten_thong_so-1 | Galaxy Buds3 Pro | gemini-3.6-flash | social | ten_thong_so | 2 | 2 |
| qc-tn-samsung-buds3pro-gptoss-description-ten-1 | Galaxy Buds3 Pro | openai/gpt-oss-120b | description | ten | 3 | 3 |
| qc-tn-samsung-buds3pro-gptoss-description-ten_thong_so-1 | Galaxy Buds3 Pro | openai/gpt-oss-120b | description | ten_thong_so | 2 | 2 |
| qc-tn-samsung-buds3pro-gptoss-landing-ten-1 | Galaxy Buds3 Pro | openai/gpt-oss-120b | landing | ten | 3 | 3 |
| qc-tn-samsung-buds3pro-gptoss-landing-ten_thong_so-1 | Galaxy Buds3 Pro | openai/gpt-oss-120b | landing | ten_thong_so | 4 | 4 |
| qc-tn-samsung-buds3pro-gptoss-social-ten-1 | Galaxy Buds3 Pro | openai/gpt-oss-120b | social | ten | 2 | 2 |
| qc-tn-samsung-buds3pro-gptoss-social-ten_thong_so-1 | Galaxy Buds3 Pro | openai/gpt-oss-120b | social | ten_thong_so | 3 | 3 |

## Thời gian gán lượt 1

Nguồn: trường `giay` của `data/nhan/thu_luot1.jsonl`, 66 tuyên bố. Đây là thời gian gán thật.

Lượt 2 không có thời gian thật: trường `giay` của `data/nhan/thu_luot2.jsonl` chỉ có giá trị 1 ở cả 66 tuyên bố, là giá trị giữ chỗ, không dùng.

| Phạm vi | Số tuyên bố | Tổng | Trung bình (giây) | Trung bình (phút) | Trung vị (giây) | Trung vị (phút) | Nhỏ nhất (giây) | Lớn nhất (giây) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tất cả | 66 | 4 giờ 47 phút | 261 | 4,4 | 110 | 1,8 | 28 | 2.118 |
| iPhone 17 | 35 | 3 giờ 35 phút | 369 | 6,1 | 143 | 2,4 | 28 | 2.118 |
| Galaxy Buds3 Pro | 31 | 1 giờ 12 phút | 140 | 2,3 | 72 | 1,2 | 28 | 1.108 |

Năm giá trị lớn nhất: tb-00029 (2.118 giây), tb-00035 (2.118 giây), tb-00008 (1.160 giây), tb-00056 (1.108 giây), tb-00001 (1.034 giây).
Trung bình khi bỏ hai giá trị lớn nhất: 203 giây (3,4 phút), trên 64 tuyên bố.

## Phương án quy mô

Chỉ có số đo và phép tính. Chưa chốt phương án nào.

### Đầu vào

- Mục tiêu: 250–300 tuyên bố, tính cả 66 tuyên bố của bộ thử.
- Cần thêm 184–234 tuyên bố từ 10 mẫu còn lại, tức 18,4–23,4 tuyên bố mỗi mẫu.
- Một lần sinh đủ thiết kế của bộ thử cho một mẫu là 12 bài (2 LLM × 3 loại bài × 2 chế độ); 10 mẫu × 12 = 120 bài.
- Tỷ lệ Lệch của bộ thử (nhãn lượt 2): 18/66 = 27,3%.

Số đo trên bộ thử:

| Chế độ | Số bài | Tuyên bố mỗi bài (trung bình) | Độ lệch chuẩn | Lệch/tuyên bố |
| --- | --- | --- | --- | --- |
| `ten` | 12 | 1,25 | 1,14 | 2 (13,3%) |
| `ten_thong_so` | 12 | 4,25 | 1,82 | 16 (31,4%) |
| Cả hai | 24 | 2,75 | 2,13 | 18 (27,3%) |

Trung bình tuyên bố mỗi bài theo mẫu và chế độ (dùng cho cột "Khoảng theo mẫu"):

| Mẫu | `ten` | `ten_thong_so` |
| --- | --- | --- |
| iPhone 17 | 1,00 | 4,83 |
| Galaxy Buds3 Pro | 1,50 | 3,67 |

Mẫu cần sinh thêm (10):

| Mã mẫu | Tên | Nhóm | Tập |
| --- | --- | --- | --- |
| dt-xiaomi-15t | Xiaomi 15T | Điện thoại | phattrien |
| dh-apple-watchse3 | Apple Watch SE 3 | Đồng hồ | phattrien |
| dt-oppo-findx8 | OPPO Find X8 | Điện thoại | kiemtra |
| dt-samsung-galaxys25ultra | Galaxy S25 Ultra | Điện thoại | kiemtra |
| dt-xiaomi-redminote14proplus5g | Redmi Note 14 Pro+ 5G | Điện thoại | kiemtra |
| tn-apple-airpodspro3 | AirPods Pro 3 | Tai nghe | kiemtra |
| tn-apple-airpods4 | AirPods 4 | Tai nghe | kiemtra |
| tn-xiaomi-redmibuds6pro | Redmi Buds 6 Pro | Tai nghe | kiemtra |
| dh-samsung-galaxywatch8 | Galaxy Watch8 | Đồng hồ | kiemtra |
| dh-xiaomi-watchs4 | Xiaomi Watch S4 | Đồng hồ | kiemtra |

### Cách tính

- Tuyên bố mới = số bài mới × trung bình tuyên bố mỗi bài của các chế độ trong phương án (theo tỷ lệ chế độ).
- Khoảng ±1 độ lệch chuẩn: độ lệch chuẩn của tổng = căn của (số bài × tổng các phần chế độ × độ lệch chuẩn² của chế độ), coi các bài độc lập. Đây là dao động ngẫu nhiên giữa các bài, không gồm sai số do ước lượng trung bình từ 12 bài mỗi chế độ.
- Khoảng theo mẫu: tổng khi cả 10 mẫu mới cho số tuyên bố mỗi bài bằng đúng mẫu bộ thử thấp hơn, hoặc cao hơn, trong hai mẫu (iPhone 17 hoặc Galaxy Buds3 Pro).
- Trung bình trong mục tiêu: so tổng tuyên bố trung bình với 250–300 (có, dưới, trên).
- Lệch (tỷ lệ chung): 18 Lệch đã có + tuyên bố mới × 27,3%; trong ngoặc là khoảng ứng với khoảng ±1 độ lệch chuẩn của tuyên bố. Lệch (tỷ lệ theo chế độ): dùng tỷ lệ Lệch riêng của từng chế độ trong bộ thử.
- Phát triển / kiểm tra: tuyên bố của tập phát triển (66 đã có + 2 mẫu mới) và của tập kiểm tra (8 mẫu mới), theo cột `tap` của `mau_san_pham.csv`, mỗi mẫu mới sinh cùng số bài.
- Các hàng là số bài nguyên mỗi mẫu quanh khoảng cần; số bài lẻ chỉ cân bằng chế độ khi luân phiên giữa các mẫu.

### Phương án (a): giữ đủ hai chế độ như bộ thử

Tỷ lệ chế độ 1:1. Trung bình 2,75 tuyên bố mỗi bài. Số bài mới cần mỗi mẫu: 6,7–8,5.

| Bài mỗi mẫu | Tổng bài mới | Tuyên bố mới | Tổng tuyên bố | Khoảng ±1 độ lệch chuẩn | Khoảng theo mẫu | Trung bình trong mục tiêu | Lệch (tỷ lệ chung) | Lệch (tỷ lệ theo chế độ) | Phát triển / kiểm tra |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 60 | 165 | 231 | 219–243 | 221–241 | dưới | 63 (60–66) | 63 | 99 / 132 |
| 7 | 70 | 192 | 258 | 246–271 | 247–270 | có | 70 (67–74) | 70 | 104 / 154 |
| 8 | 80 | 220 | 286 | 272–300 | 273–299 | có | 78 (74–82) | 78 | 110 / 176 |
| 9 | 90 | 248 | 314 | 299–328 | 298–328 | trên | 86 (82–89) | 86 | 116 / 198 |
| 12 | 120 | 330 | 396 | 379–413 | 376–416 | trên | 108 (103–113) | 108 | 132 / 264 |

Hàng 12 bài mỗi mẫu là thiết kế đầy đủ như bộ thử (Bước 18 gốc).

### Phương án (b): chỉ chế độ `ten_thong_so`

Trung bình 4,25 tuyên bố mỗi bài. Số bài mới cần mỗi mẫu: 4,3–5,5. Sáu bài (2 LLM × 3 loại bài) là một lần sinh đủ của chế độ này cho một mẫu.

| Bài mỗi mẫu | Tổng bài mới | Tuyên bố mới | Tổng tuyên bố | Khoảng ±1 độ lệch chuẩn | Khoảng theo mẫu | Trung bình trong mục tiêu | Lệch (tỷ lệ chung) | Lệch (tỷ lệ theo chế độ) | Phát triển / kiểm tra |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 40 | 170 | 236 | 225–247 | 213–259 | dưới | 64 (61–67) | 71 | 100 / 136 |
| 5 | 50 | 212 | 278 | 266–291 | 249–308 | có | 76 (72–79) | 85 | 108 / 170 |
| 6 | 60 | 255 | 321 | 307–335 | 286–356 | trên | 88 (84–91) | 98 | 117 / 204 |

### Phương án (c): theo T9.1

T9.1: nếu trung bình dưới 2 tuyên bố có điều kiện mỗi bài thì tăng số bài sinh cho mỗi mẫu; nếu vẫn thiếu thì điền tên các nhóm thông số (không kèm con số) vào ô từ khóa cho mọi bài và sinh lại các bài của bộ thử (Bước 16).

Trung bình tuyên bố có điều kiện mỗi bài đo được:

| Phạm vi | Trung bình | Dưới 2 |
| --- | --- | --- |
| Cả 24 bài | 2,75 | không |
| Chế độ `ten` | 1,25 | có |
| Chế độ `ten_thong_so` | 4,25 | không |

**(c1) Tăng số bài, chỉ chế độ `ten`** (chế độ có trung bình 1,25; không điền từ khóa). Số bài mới cần mỗi mẫu: 14,7–18,7.

| Bài mỗi mẫu | Tổng bài mới | Tuyên bố mới | Tổng tuyên bố | Khoảng ±1 độ lệch chuẩn | Khoảng theo mẫu | Trung bình trong mục tiêu | Lệch (tỷ lệ chung) | Lệch (tỷ lệ theo chế độ) | Phát triển / kiểm tra |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 14 | 140 | 175 | 241 | 228–254 | 206–276 | dưới | 66 (62–69) | 41 | 101 / 140 |
| 15 | 150 | 188 | 254 | 240–267 | 216–291 | có | 69 (65–73) | 43 | 104 / 150 |
| 16 | 160 | 200 | 266 | 252–280 | 226–306 | có | 73 (69–76) | 45 | 106 / 160 |
| 17 | 170 | 212 | 278 | 264–293 | 236–321 | có | 76 (72–80) | 46 | 108 / 170 |
| 18 | 180 | 225 | 291 | 276–306 | 246–336 | có | 79 (75–84) | 48 | 111 / 180 |
| 19 | 190 | 238 | 304 | 288–319 | 256–351 | trên | 83 (78–87) | 50 | 114 / 190 |

**(c2) Điền tên nhóm thông số vào ô từ khóa cho mọi bài, sinh lại 24 bài của bộ thử.** Chưa có số đo cho thiết lập này. Bảng dưới thử ba giá trị giả định của số tuyên bố mỗi bài (đều lấy từ số đo trên bộ thử). Mọi bài đều là bài sinh mới, gồm 24 bài sinh lại của bộ thử; 66 tuyên bố hiện có không còn tính vào tổng. Tính trên 12 mẫu.

| Tuyên bố mỗi bài (giả định) | Tổng bài cho 250–300 tuyên bố | Bài mỗi mẫu (12 mẫu) |
| --- | --- | --- |
| 1,25 (bằng chế độ `ten`) | 200–240 | 16,7–20,0 |
| 2,75 (bằng trung bình cả hai chế độ) | 91–109 | 7,6–9,1 |
| 4,25 (bằng chế độ `ten_thong_so`) | 59–70 | 4,9–5,8 |

### Thời gian gán ước tính cho tuyên bố mới

Nhân số tuyên bố mới trung bình với thời gian gán lượt 1 (trung bình 261 giây, trung vị 110 giây mỗi tuyên bố). Lượt 1 gồm giai đoạn làm quen hướng dẫn nên chỉ là cận tham khảo; lượt 2 không có thời gian thật.

| Phương án | Bài mỗi mẫu | Tuyên bố mới | Giờ gán (theo trung bình) | Giờ gán (theo trung vị) |
| --- | --- | --- | --- | --- |
| (a) | 6 | 165 | 12,0 | 5,0 |
| (a) | 7 | 192 | 14,0 | 5,9 |
| (a) | 8 | 220 | 16,0 | 6,7 |
| (a) | 9 | 248 | 18,0 | 7,6 |
| (a) | 12 | 330 | 23,9 | 10,1 |
| (b) | 4 | 170 | 12,3 | 5,2 |
| (b) | 5 | 212 | 15,4 | 6,5 |
| (b) | 6 | 255 | 18,5 | 7,8 |
| (c1) | 14 | 175 | 12,7 | 5,3 |
| (c1) | 15 | 188 | 13,6 | 5,7 |
| (c1) | 16 | 200 | 14,5 | 6,1 |
| (c1) | 17 | 212 | 15,4 | 6,5 |
| (c1) | 18 | 225 | 16,3 | 6,9 |
| (c1) | 19 | 238 | 17,2 | 7,3 |

### Giả định và giới hạn

- Số đo chỉ từ 2 mẫu (iPhone 17: 35 tuyên bố trên 12 bài (2,92 mỗi bài); Galaxy Buds3 Pro: 31 tuyên bố trên 12 bài (2,58 mỗi bài)). Mỗi ô mẫu × chế độ có 6 bài.
- Trung bình và độ lệch chuẩn của mỗi chế độ ước lượng từ 12 bài (`ten`) và 12 bài (`ten_thong_so`).
- Giả định bài mới cùng thiết lập với bộ thử (câu lệnh, LLM, loại bài, đoạn thông số chọn theo cùng quy tắc) và tuyên bố được tách tay theo cùng quy tắc (lọc theo cấu hình, gộp trùng trong bài). Không tính hao hụt (bài lỗi, bài bị cắt).
- Số thuộc tính có điều kiện khác nhau giữa các nhóm (điện thoại 8, tai nghe 4, đồng hồ 4). Bộ thử chỉ có điện thoại và tai nghe; nhóm đồng hồ không có số đo.
- Tỷ lệ điện thoại và tai nghe khác nhau: xem hàng "Mẫu" trong bảng số tuyên bố mỗi bài và cột "Khoảng theo mẫu". Khoảng theo mẫu chỉ có hai đầu mút (hai mẫu), không phải khoảng tin cậy.
- 4/12 bài chế độ `ten` không có tuyên bố nào; phân bố số tuyên bố mỗi bài của chế độ này lệch, nên trung bình và độ lệch chuẩn chỉ mô tả gần đúng.
- Tỷ lệ Lệch lấy từ nhãn lượt 2 của bộ thử (Claude gán, người thực hiện duyệt); mẫu nhỏ, chưa tách theo loại biến đổi và có thể đổi nếu thiết lập sinh đổi (nhất là phương án c2).
- Số tuyên bố có điều kiện bằng số tuyên bố vì mọi thuộc tính đều có điều kiện bắt buộc; nếu cấu hình có thuộc tính không điều kiện thì hai số tách ra.
