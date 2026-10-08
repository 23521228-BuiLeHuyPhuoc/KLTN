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

## Kế hoạch 08/10/2026 (nhánh `plan/opus-2026-10-08`, chưa merge, chờ GVHD xác nhận)

- Bắt đầu từ [kế hoạch chi tiết cho sinh viên](docs/KE_HOACH_CHI_TIET_SINH_VIEN.md), [định vị và tiêu chí](docs/DINH_VI_VA_TIEU_CHI.md), [câu hỏi phản biện](docs/CAU_HOI_PHAN_BIEN_DU_KIEN.md), [đối chiếu thay đổi](docs/DOI_CHIEU_THAY_DOI_KE_HOACH.md), [quyết định cần chốt](docs/QUYET_DINH_CAN_CHOT.md), [nhật ký](docs/NHAT_KY_SUA_2026-10-08.md).
- Docx được sửa bằng `scripts/redesign_plan_2026_10_08.py` (đã áp dụng, script từ chối chạy lần hai). `review_patch_2026_10_08.py` đã bị thay thế.
- Kiểm tra:
  `python3 scripts/update_thesis_docs.py --check`; `python3 scripts/audit_examples.py --check`; `python3 scripts/check_paper_facts.py`; `python3 -m unittest discover -s tests`.
- Mô phỏng cỡ test: `python3 scripts/simulate_power.py`. Chặn rò nhãn: `python3 scripts/check_input_leak.py <input.json>`.
- Khóa API cũ nằm trong lịch sử công khai, **phải thu hồi**.

## Cấu trúc thư mục

```
.
├── báo/                  # Bài báo gốc (PDF) — bản quyền thuộc tác giả/nhà xuất bản
├── dịch/                 # Bản dịch máy (PDF, glossary) — xem lưu ý bản quyền
├── docs/                 # Hướng dẫn nhãn, đặc tả A–B–C, giao thức, kế hoạch, nhật ký
├── evidence/2026-10-08/  # Snapshot nguồn Apple, examples.json, mã băm
├── scripts/              # Kiểm tra docx/ví dụ/số liệu, hàm tham chiếu A–B–C, mô phỏng
├── templates/            # Mẫu manifest, search_log, gán nhãn độc lập, mẫu quảng cáo LLM
├── tests/                # unittest cho luật A–B–C
├── run_translate_batch.sh # Dịch hàng loạt bằng pdf2zh (Bing Translator)
└── .gitignore
```

## Hướng dẫn sử dụng công cụ dịch

Script `run_translate_batch.sh` hỗ trợ dịch batch các file PDF trong thư mục `báo/` sang tiếng Việt và lưu kết quả vào thư mục `dịch/`:

```bash
bash run_translate_batch.sh
```
