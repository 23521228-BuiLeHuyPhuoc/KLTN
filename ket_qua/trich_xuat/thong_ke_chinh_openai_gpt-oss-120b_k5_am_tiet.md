# Thống kê trích xuất có neo nguồn (Bước 22)

## Thiết lập

- Tệp tuyên bố: data/tuyen_bo/chinh.jsonl; mô hình openai/gpt-oss-120b; top-5, cách tách am_tiet; max_output_tokens 8192, nhiệt độ 0, JSON mode, qua bộ nhớ đệm.
- neo_nguon = True, kiem_day_du = True.

## Số lượng

- Số tuyên bố: 42; số lỗi LLM hay lỗi đọc đầu ra: 0.
- Số mục tài liệu: 123 (giữ 123, bị loại 0).

## Trường bị loại (theo lý do và theo phía)

| Lý do | Tuyên bố | Tài liệu | Tổng |
| --- | --- | --- | --- |
| cum_khong_trong_trich | 0 | 4 | 4 |
| kieu_khong_gan_so | 2 | 15 | 17 |
| trich_khong_co_trong_nguon | 7 | 0 | 7 |

## Điều kiện bổ sung (kiểm tra đầy đủ)

| Điều kiện | Tuyên bố | Tài liệu | Tổng |
| --- | --- | --- | --- |
| che_do_nguon | 1 | 0 | 1 |
| chenh_lech_nhiet_do | 0 | 2 | 2 |
| chuan_do_sau | 2 | 4 | 6 |
| do_sau | 0 | 1 | 1 |
| hoat_dong | 1 | 2 | 3 |
| kieu_dung_luong | 0 | 11 | 11 |
| kieu_tan_so | 0 | 21 | 21 |
| so_phut_sac | 0 | 6 | 6 |
| thoi_gian_ngam | 0 | 1 | 1 |

- Điều kiện thấy hai giá trị khác nhau, không điền (bo_sung_mo_ho): 5.

## Điều kiện lạ (dieu_kien_khac)

- Số tuyên bố có dieu_kien_khac: 6/42.
- Số mục tài liệu giữ có dieu_kien_khac: 75/123.

Cụm ở phía tuyên bố:

- che_do_hoat_dong: Luôn Bật (x1)
- che_do_hoat_dong: bơi lội (x2)
- phu_kien: HyperCharge (x1)
- phu_kien: công nghệ sạc nhanh HyperCharge (x2)

Cụm ở phía tài liệu:

- bo_phan: Bộ sạc không bao gồm trong hộp (x1)
- bo_phan: Màn hình (x10)
- bo_phan: Màn hình Retina (x2)
- bo_phan: Pin (x6)
- bo_phan: Tần số quét (x1)
- bo_phan: tần số quét (x1)
- che_do_hoat_dong: Gold Collection (x6)
- che_do_hoat_dong: Màn hình (x3)
- che_do_hoat_dong: Màn hình 6.83" bảo vệ mắt (x1)
- che_do_hoat_dong: Màn hình Retina Luôn Bật với OLED và LTPO (x2)
- che_do_hoat_dong: Nguồn Điện Và Thời Lượng Pin (x3)
- che_do_hoat_dong: Nâng tầm khả năng hiển thị (x10)
- che_do_hoat_dong: Sạc (x4)
- che_do_hoat_dong: Thời lượng pin hàng đầu (x3)
- che_do_hoat_dong: Tần số quét (x5)
- che_do_hoat_dong: bơi (x2)
- che_do_hoat_dong: khi bơi (x1)
- dieu_kien_do: 30 phút (x1)
- dieu_kien_do: 8 giờ (x4)
- dieu_kien_do: lên đến 8 giờ (x2)
- dieu_kien_do: độ sâu (x2)
- dieu_kien_do: độ sâu 3m (x1)
- phien_ban: Gold Collection (x3)
- phu_kien: Cổng sạc USB-C (x1)
- phu_kien: HyperCharge (x3)
- phu_kien: Sạc nhanh (x3)
- phu_kien: Sạc nhanh HyperCharge (x13)
- phu_kien: hỗ trợ PD3.0 / PD2.0 (x1)

## Sản phẩm

- Số mục tài liệu khac_san_pham: 0.

## Thuộc tính so với tách tay (tham khảo, đo chính thức ở Bước 28)

- Tỉ lệ thuoc_tinh trích khớp thuoc_tinh tách tay: 100,0% (42/42).
