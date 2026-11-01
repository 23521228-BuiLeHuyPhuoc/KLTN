Số sơ bộ: nhãn chuẩn là nhãn lượt 1 của Bước 13; mô hình, k và cách tách là lựa chọn tạm, chốt ở Bước 33.

# Đối chứng B0 trên bộ thử (Bước 15)

## Thiết lập

- Bộ thử: 66 tuyên bố (DUNG 24, SAI 4, LECH 15, CHUA_DU 23); mẫu tính chỉ số: 64 tuyên bố (DUNG 23, SAI 4, LECH 14, CHUA_DU 23).
- Truy hồi: BM25, top-5, cách tách am_tiet; chỉ đoạn của đúng mẫu.
- Câu lệnh: khung T12.1, SHA-256 của khung f9bf05cd29a1a791049c300140eb260957cb1cdf0b222dbebe8f9bdb442994b7.
- Gọi LLM: nhiệt độ 0, max_output_tokens 4096, JSON mode, qua bộ nhớ đệm.
- Ánh xạ nhãn: Supported -> DUNG, Refuted -> SAI, NEI -> CHUA_DU; không đọc được nhãn -> LOI.
- FAR = (nhãn chuẩn khác DUNG mà bị gán DUNG) / (nhãn chuẩn khác DUNG). Recall nhãn Đúng = (DUNG được gán DUNG) / (DUNG). LOI tính vào mẫu số, không là DUNG.

## Tuyên bố loại khỏi chỉ số (vẫn chạy B0, có trong tệp kết quả)

| Mã | Mẫu | Tuyên bố | Nhãn chuẩn | Lý do |
| --- | --- | --- | --- | --- |
| tb-00009 | dt-apple-iphone17 | iPhone 17 có độ sáng màn hình tối đa ngoài trời lên đến 3000 nit | LECH | nhãn lượt 1 lưu lệch sang tuyên bố kế bên |
| tb-00010 | dt-apple-iphone17 | iPhone 17 có khả năng kháng nước chuẩn IP68 | DUNG | nhãn lượt 1 lưu lệch sang tuyên bố kế bên |

## Tóm tắt

| Mô hình | Mô hình thực | FAR | Recall nhãn Đúng | Số LOI (mẫu tính / cả bộ) | Mẫu số FAR | Mẫu số Recall |
| --- | --- | --- | --- | --- | --- | --- |
| openai/gpt-oss-120b | openai/gpt-oss-120b | 80,5% (33/41) | 95,7% (22/23) | 0 / 0 | 41 | 23 |

## openai/gpt-oss-120b

Bảng nhầm lẫn (hàng: nhãn chuẩn; cột: nhãn dự đoán):

| Nhãn chuẩn | DUNG | SAI | CHUA_DU | LOI | Tổng |
| --- | --- | --- | --- | --- | --- |
| DUNG | 22 | 0 | 1 | 0 | 23 |
| SAI | 2 | 1 | 1 | 0 | 4 |
| LECH | 13 | 1 | 0 | 0 | 14 |
| CHUA_DU | 18 | 2 | 3 | 0 | 23 |
