# Thống kê trích xuất có neo nguồn (Bước 22)
- Gộp từ: ket_qua/trich_xuat/thu_gemini-3.6-flash_k5_am_tiet.jsonl (66 tuyên bố), ket_qua/trich_xuat/chinh_gemini-3.6-flash_k5_am_tiet.jsonl (42 tuyên bố).

## Thiết lập

- Tệp tuyên bố: data/tuyen_bo/thu.jsonl + data/tuyen_bo/chinh.jsonl; mô hình gemini-3.6-flash; top-5, cách tách am_tiet; max_output_tokens 8192, nhiệt độ 0, JSON mode, qua bộ nhớ đệm.
- neo_nguon = True, kiem_day_du = True.

## Số lượng

- Số tuyên bố: 108; số lỗi LLM hay lỗi đọc đầu ra: 2 (tb-00050: llm_khong_tra_ve_dung: empty_blocked_or_incomplete_response, tb-00066: llm_khong_tra_ve_dung: empty_blocked_or_incomplete_response).
- Số mục tài liệu: 509 (giữ 497, bị loại 12).

## Trường bị loại (theo lý do và theo phía)

| Lý do | Tuyên bố | Tài liệu | Tổng |
| --- | --- | --- | --- |
| cum_khong_trong_trich | 2 | 0 | 2 |
| dai_luong_khac | 0 | 8 | 8 |
| kieu_khong_gan_so | 1 | 17 | 18 |
| trich_khong_co_trong_nguon | 0 | 36 | 36 |

## Điều kiện bổ sung (kiểm tra đầy đủ)

| Điều kiện | Tuyên bố | Tài liệu | Tổng |
| --- | --- | --- | --- |
| bo_phan | 0 | 132 | 132 |
| bo_tiep_hop | 0 | 9 | 9 |
| che_do_nguon | 1 | 0 | 1 |
| chuan_do_sau | 2 | 3 | 5 |
| dai_luong | 0 | 2 | 2 |
| hoat_dong | 1 | 16 | 17 |
| hoat_dong_bi_cam | 0 | 6 | 6 |
| kieu_tan_so | 0 | 21 | 21 |
| moc_phan_tram | 2 | 0 | 2 |

- Điều kiện thấy hai giá trị khác nhau, không điền (bo_sung_mo_ho): 9.

## Điều kiện lạ (dieu_kien_khac)

- Số tuyên bố có dieu_kien_khac: 7/108.
- Số mục tài liệu giữ có dieu_kien_khac: 45/497.

Cụm ở phía tuyên bố:

- che_do_hoat_dong: cuộc gọi (x2)
- che_do_hoat_dong: kết nối âm nhạc (x1)
- che_do_hoat_dong: nhạc (x2)
- che_do_hoat_dong: video (x1)
- dieu_kien_do: mọi điều kiện ánh sáng (x1)
- dieu_kien_do: trong ánh sáng mạnh (x1)
- phu_kien: hộp sạc nhanh (x1)

Cụm ở phía tài liệu:

- bo_phan: Màn hình 6.83" bảo vệ mắt (x10)
- che_do_hoat_dong: Thời gian sử dụng (x9)
- che_do_hoat_dong: Thời lượng sử dụng (x9)
- che_do_hoat_dong: các hoạt động dưới nước nông (x1)
- che_do_hoat_dong: phát (x16)
- dieu_kien_do: khi sạc đầy (x11)
- dieu_kien_do: sạc đầy (x5)

## Sản phẩm

- Số mục tài liệu khac_san_pham: 24.

## Thuộc tính so với tách tay (tham khảo, đo chính thức ở Bước 28)

- Tỉ lệ thuoc_tinh trích khớp thuoc_tinh tách tay: 98,1% (106/108).
