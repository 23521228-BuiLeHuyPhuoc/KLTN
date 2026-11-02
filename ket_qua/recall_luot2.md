# Recall@k của truy hồi BM25 trên bộ thử (Bước 14)

Số tạm: bằng chứng chuẩn lấy từ data/nhan/thu_luot2.jsonl (lượt 2, người gán claude, phuoc).

Bộ thử có 66 tuyên bố, 2 không có bằng chứng (không tính), 0 bị loại; mẫu số 64. Tuyên bố trúng ở k khi có ít nhất một đoạn bằng chứng nằm trong top-k.

## Tuyên bố loại khỏi mẫu số

| Mã | Mẫu | Tuyên bố | Lý do |
| --- | --- | --- | --- |
| (không có) |  |  |  |

## Recall@k

| Cách tách | k=1 | k=3 | k=5 | k=8 |
| --- | --- | --- | --- | --- |
| Âm tiết | 96,9% (62/64) | 98,4% (63/64) | 100,0% (64/64) | 100,0% (64/64) |
| Từ (pyvi) | 100,0% (64/64) | 100,0% (64/64) | 100,0% (64/64) | 100,0% (64/64) |

## Theo mẫu

| Mẫu | Cách tách | Mẫu số | k=1 | k=3 | k=5 | k=8 |
| --- | --- | --- | --- | --- | --- | --- |
| iPhone 17 (dt-apple-iphone17) | Âm tiết | 35 | 100,0% (35/35) | 100,0% (35/35) | 100,0% (35/35) | 100,0% (35/35) |
| iPhone 17 (dt-apple-iphone17) | Từ (pyvi) | 35 | 100,0% (35/35) | 100,0% (35/35) | 100,0% (35/35) | 100,0% (35/35) |
| Galaxy Buds3 Pro (tn-samsung-buds3pro) | Âm tiết | 29 | 93,1% (27/29) | 96,6% (28/29) | 100,0% (29/29) | 100,0% (29/29) |
| Galaxy Buds3 Pro (tn-samsung-buds3pro) | Từ (pyvi) | 29 | 100,0% (29/29) | 100,0% (29/29) | 100,0% (29/29) | 100,0% (29/29) |

## Bằng chứng không nằm trong top-8 ở ít nhất một cách tách

Không có.
