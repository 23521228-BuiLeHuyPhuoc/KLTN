# KLTN - Khóa Luận Tốt Nghiệp

Repository lưu trữ tài liệu nghiên cứu, bài báo tham khảo và các công cụ dịch tự động phục vụ quá trình thực hiện Khóa luận tốt nghiệp.

## Tài liệu KLTN đang làm việc

- [Đề cương chi tiết](Đọc_báo_cùng_HuP_4_.docx) và [báo cáo tháng 09/2026](Đọc_báo_cùng_HuP_3_.docx), cập nhật ngày 08/10/2026.
- [Phân tích bảy bài tham khảo](docs/PHAN_TICH_TAI_LIEU.md).
- [Bàn giao sau khi tiếp nối Claude](docs/BAN_GIAO_2026-10-08.md): thay đổi, kiểm tra, bản sao lưu và thông tin còn cần xác nhận.
- [Kiểm tra phản biện và các sửa đổi lần hai](docs/KIEM_TRA_PHAN_BIEN_2026-10-08.md): tiêu chí RQ3, A–B–C, số liệu gốc và 23 ví dụ.
- [Đặc tả A–B–C](docs/QUY_TAC_ABC.md), [ảnh chụp và hồ sơ nguồn](evidence/2026-10-08/README.md).
- [Nhật ký công việc](CLAUDE_WORK_LOG.md).

Kiểm tra nội dung và cấu trúc hai DOCX: `python3 scripts/update_thesis_docs.py --check`. Script chỉ dùng thư viện chuẩn Python; mặc định chạy xem trước, chỉ sửa file khi có `--apply`.

Kiểm hồ sơ ví dụ/hash nguồn: `python3 scripts/audit_examples.py --check`. Đối chiếu vị trí số liệu bài gốc: `python3 scripts/check_paper_facts.py` (cần Poppler). Đây là kiểm tra tài liệu, chưa phải chạy pipeline/thí nghiệm B0/B1/P.

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
