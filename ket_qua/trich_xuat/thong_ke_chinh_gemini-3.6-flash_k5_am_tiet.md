# Thống kê trích xuất có neo nguồn (Bước 22)

## Thiết lập

- Tệp tuyên bố: data/tuyen_bo/chinh.jsonl; mô hình gemini-3.6-flash; top-5, cách tách am_tiet; max_output_tokens 8192, nhiệt độ 0, JSON mode, qua bộ nhớ đệm.
- neo_nguon = True, kiem_day_du = True.

## Số lượng

- Số tuyên bố: 42; số lỗi LLM hay lỗi đọc đầu ra: 0.
- Số mục tài liệu: 109 (giữ 106, bị loại 3).

## Trường bị loại (theo lý do và theo phía)

| Lý do | Tuyên bố | Tài liệu | Tổng |
| --- | --- | --- | --- |
| dai_luong_khac | 0 | 3 | 3 |
| kieu_khong_gan_so | 1 | 5 | 6 |

## Điều kiện bổ sung (kiểm tra đầy đủ)

| Điều kiện | Tuyên bố | Tài liệu | Tổng |
| --- | --- | --- | --- |
| bo_tiep_hop | 0 | 9 | 9 |
| che_do_nguon | 1 | 0 | 1 |
| chuan_do_sau | 2 | 3 | 5 |
| kieu_tan_so | 0 | 21 | 21 |

- Điều kiện thấy hai giá trị khác nhau, không điền (bo_sung_mo_ho): 2.

## Điều kiện lạ (dieu_kien_khac)

- Số tuyên bố có dieu_kien_khac: 0/42.
- Số mục tài liệu giữ có dieu_kien_khac: 11/106.

Cụm ở phía tuyên bố: (không có)

Cụm ở phía tài liệu:

- bo_phan: Màn hình 6.83" bảo vệ mắt (x10)
- che_do_hoat_dong: các hoạt động dưới nước nông (x1)

## Sản phẩm

- Số mục tài liệu khac_san_pham: 0.

## Thuộc tính so với tách tay (tham khảo, đo chính thức ở Bước 28)

- Tỉ lệ thuoc_tinh trích khớp thuoc_tinh tách tay: 100,0% (42/42).
