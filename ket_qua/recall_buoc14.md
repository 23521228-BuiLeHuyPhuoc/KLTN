# Recall@k của truy hồi BM25 trên bộ thử (Bước 14)

Số tạm: bằng chứng chuẩn lấy từ nhãn lượt 1 của Bước 13; tính lại sau khi gán lại ở Bước 16.

Bộ thử có 66 tuyên bố, 8 không có bằng chứng (không tính), 2 bị loại; mẫu số 56. Tuyên bố trúng ở k khi có ít nhất một đoạn bằng chứng nằm trong top-k.

## Tuyên bố loại khỏi mẫu số

| Mã | Mẫu | Tuyên bố | Lý do |
| --- | --- | --- | --- |
| tb-00009 | dt-apple-iphone17 | iPhone 17 có độ sáng màn hình tối đa ngoài trời lên đến 3000 nit | bằng chứng lưu lệch sang tuyên bố kế bên (nhãn lượt 1) |
| tb-00010 | dt-apple-iphone17 | iPhone 17 có khả năng kháng nước chuẩn IP68 | bằng chứng lưu lệch sang tuyên bố kế bên (nhãn lượt 1) |

## Recall@k

| Cách tách | k=1 | k=3 | k=5 | k=8 |
| --- | --- | --- | --- | --- |
| Âm tiết | 83,9% (47/56) | 98,2% (55/56) | 100,0% (56/56) | 100,0% (56/56) |
| Từ (pyvi) | 87,5% (49/56) | 98,2% (55/56) | 100,0% (56/56) | 100,0% (56/56) |

## Theo mẫu

| Mẫu | Cách tách | Mẫu số | k=1 | k=3 | k=5 | k=8 |
| --- | --- | --- | --- | --- | --- | --- |
| iPhone 17 (dt-apple-iphone17) | Âm tiết | 33 | 100,0% (33/33) | 100,0% (33/33) | 100,0% (33/33) | 100,0% (33/33) |
| iPhone 17 (dt-apple-iphone17) | Từ (pyvi) | 33 | 100,0% (33/33) | 100,0% (33/33) | 100,0% (33/33) | 100,0% (33/33) |
| Galaxy Buds3 Pro (tn-samsung-buds3pro) | Âm tiết | 23 | 60,9% (14/23) | 95,7% (22/23) | 100,0% (23/23) | 100,0% (23/23) |
| Galaxy Buds3 Pro (tn-samsung-buds3pro) | Từ (pyvi) | 23 | 69,6% (16/23) | 95,7% (22/23) | 100,0% (23/23) | 100,0% (23/23) |

## Bằng chứng không nằm trong top-8 ở ít nhất một cách tách

Không có.
