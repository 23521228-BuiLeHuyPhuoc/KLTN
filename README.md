# KLTN - Khóa Luận Tốt Nghiệp

Repository lưu trữ tài liệu nghiên cứu, bài báo tham khảo và các công cụ dịch tự động phục vụ quá trình thực hiện Khóa luận tốt nghiệp.

## Cấu trúc thư mục

```
.
├── báo/                  # Các bài báo nghiên cứu gốc (PDF)
│   └── báo con1/         # Tài liệu bổ trợ / chuyên sâu
├── dịch/                 # Các bản dịch song ngữ & đơn ngữ (PDF, CSV glossary)
├── run_translate_batch.sh # Script tự động dịch hàng loạt sử dụng pdf2zh (Bing Translator)
└── .gitignore            # Cấu hình bỏ qua file tạm, log và scratch
```

## Hướng dẫn sử dụng công cụ dịch

Script `run_translate_batch.sh` hỗ trợ dịch batch các file PDF trong thư mục `báo/` sang tiếng Việt và lưu kết quả vào thư mục `dịch/`:

```bash
bash run_translate_batch.sh
```
