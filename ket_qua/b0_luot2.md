Số sơ bộ: nhãn chuẩn lấy từ data/nhan/thu_luot2.jsonl (lượt 2, người gán claude, phuoc); mô hình, k và cách tách là lựa chọn tạm, chốt ở Bước 33.

# Đối chứng B0 trên bộ thử (Bước 15)

## Thiết lập

- Bộ thử: 66 tuyên bố (DUNG 34, SAI 6, LECH 18, CHUA_DU 8); mẫu tính chỉ số: 66 tuyên bố (DUNG 34, SAI 6, LECH 18, CHUA_DU 8).
- Truy hồi: BM25, top-5, cách tách am_tiet; chỉ đoạn của đúng mẫu.
- Câu lệnh: khung T12.1, SHA-256 của khung f9bf05cd29a1a791049c300140eb260957cb1cdf0b222dbebe8f9bdb442994b7.
- Gọi LLM: nhiệt độ 0, max_output_tokens 4096, JSON mode, qua bộ nhớ đệm.
- Ánh xạ nhãn: Supported -> DUNG, Refuted -> SAI, NEI -> CHUA_DU; không đọc được nhãn -> LOI.
- FAR = (nhãn chuẩn khác DUNG mà bị gán DUNG) / (nhãn chuẩn khác DUNG). Recall nhãn Đúng = (DUNG được gán DUNG) / (DUNG). LOI tính vào mẫu số, không là DUNG.

## Tuyên bố loại khỏi chỉ số (vẫn chạy B0, có trong tệp kết quả)

| Mã | Mẫu | Tuyên bố | Nhãn chuẩn | Lý do |
| --- | --- | --- | --- | --- |
| (không có) |  |  |  |  |

## Tóm tắt

| Mô hình | Mô hình thực | FAR | Recall nhãn Đúng | Số LOI (mẫu tính / cả bộ) | Mẫu số FAR | Mẫu số Recall |
| --- | --- | --- | --- | --- | --- | --- |
| openai/gpt-oss-120b | openai/gpt-oss-120b | 75,0% (24/32) | 97,1% (33/34) | 0 / 0 | 32 | 34 |

## openai/gpt-oss-120b

Bảng nhầm lẫn (hàng: nhãn chuẩn; cột: nhãn dự đoán):

| Nhãn chuẩn | DUNG | SAI | CHUA_DU | LOI | Tổng |
| --- | --- | --- | --- | --- | --- |
| DUNG | 33 | 0 | 1 | 0 | 34 |
| SAI | 4 | 1 | 1 | 0 | 6 |
| LECH | 15 | 3 | 0 | 0 | 18 |
| CHUA_DU | 5 | 0 | 3 | 0 | 8 |
