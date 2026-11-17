# Thống kê trích xuất có neo nguồn (Bước 22)

## Thiết lập

- Tệp tuyên bố: data/tuyen_bo/thu.jsonl; mô hình openai/gpt-oss-120b; top-5, cách tách am_tiet; max_output_tokens 8192, nhiệt độ 0, JSON mode, qua bộ nhớ đệm.
- neo_nguon = True, kiem_day_du = True.

## Số lượng

- Số tuyên bố: 66; số lỗi LLM hay lỗi đọc đầu ra: 0.
- Số mục tài liệu: 509 (giữ 507, bị loại 2).

## Trường bị loại (theo lý do và theo phía)

| Lý do | Tuyên bố | Tài liệu | Tổng |
| --- | --- | --- | --- |
| cum_khong_trong_trich | 3 | 145 | 148 |
| kieu_khong_gan_so | 1 | 13 | 14 |
| trich_khong_co_trong_nguon | 3 | 10 | 13 |

## Điều kiện bổ sung (kiểm tra đầy đủ)

| Điều kiện | Tuyên bố | Tài liệu | Tổng |
| --- | --- | --- | --- |
| bo_phan | 2 | 257 | 259 |
| cach_sac | 0 | 4 | 4 |
| che_do_chong_on | 0 | 36 | 36 |
| hoat_dong | 1 | 4 | 5 |
| hoat_dong_bi_cam | 0 | 8 | 8 |
| loai_nuoc | 0 | 1 | 1 |
| loai_zoom | 1 | 1 | 2 |
| moc_phan_tram | 4 | 6 | 10 |

- Điều kiện thấy hai giá trị khác nhau, không điền (bo_sung_mo_ho): 28.

## Điều kiện lạ (dieu_kien_khac)

- Số tuyên bố có dieu_kien_khac: 12/66.
- Số mục tài liệu giữ có dieu_kien_khac: 93/507.

Cụm ở phía tuyên bố:

- bo_phan: màn hình (x3)
- che_do_hoat_dong: cho cả nhạc và cuộc gọi (x1)
- che_do_hoat_dong: kết nối âm nhạc (x1)
- che_do_hoat_dong: luôn bật (x1)
- che_do_hoat_dong: ngoài trời (x1)
- che_do_hoat_dong: nhạc và cuộc gọi (x1)
- che_do_hoat_dong: video (x1)
- dieu_kien_do: mọi điều kiện ánh sáng (x1)
- dieu_kien_do: trong ánh sáng mạnh (x1)
- phu_kien: hộp sạc nhanh (x1)

Cụm ở phía tài liệu:

- bo_phan: Công nghệ ProMotion (x3)
- bo_phan: Kháng Bụi & Nước (x6)
- bo_phan: Kháng nước (x3)
- bo_phan: phát (x1)
- che_do_hoat_dong: ANC Bật (x24)
- che_do_hoat_dong: ANC Tắt (x24)
- che_do_hoat_dong: Dynamic Island (x1)
- che_do_hoat_dong: HDR (x4)
- che_do_hoat_dong: Màn hình Luôn Bật (x1)
- che_do_hoat_dong: ngoài trời (x3)
- che_do_hoat_dong: phát (x16)
- dieu_kien_do: ngoài trời (x2)
- dieu_kien_do: tiêu chuẩn (x3)
- phu_kien: Công Suất Tối Đa 60W (x1)
- phu_kien: HDR (x1)
- phu_kien: tiêu chuẩn (x1)

## Sản phẩm

- Số mục tài liệu khac_san_pham: 0.

## Thuộc tính so với tách tay (tham khảo, đo chính thức ở Bước 28)

- Tỉ lệ thuoc_tinh trích khớp thuoc_tinh tách tay: 100,0% (66/66).
