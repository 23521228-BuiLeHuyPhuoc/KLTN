# KLTN – Khóa luận tốt nghiệp

**Đề tài:** Phương pháp kiểm chứng tuyên bố về thông số kỹ thuật có điều kiện ràng buộc trong quảng cáo
(*A method for condition-aware verification of technical specification claims in advertising*)

**Sinh viên:** Bùi Lê Huy Phước (23521228, MMTT2023.2) · **CBHD:** ThS Trần Hồng Nghi · **Thời gian:** 15/09/2026 – 31/12/2026

## Hai tài liệu chính

| Tài liệu | Nội dung |
|---|---|
| [Đề cương bản cuối](de_cuong/23521228_DECUONGKHOALUAN_UIT.pdf) | `de_cuong/23521228_DECUONGKHOALUAN_UIT.pdf`, bản cuối ngày 10/10/2026, xuất từ Google Docs. Mọi kế hoạch bám theo bản này. |
| [Bản làm việc của đề cương](de_cuong/) | `23521228_BuiLeHuyPhuoc_DeCuongKLTN.docx` và `..._chu_do.docx` (tô đỏ phần sửa so với đề cương đã nộp) là các bản trước bản cuối, có vài chỗ khác bản cuối (ví dụ tên tiếng Anh). |
| [Chi tiết tuyến tính của khóa luận](CHI_TIET_TUYEN_TINH_KHOA_LUAN.md) | Kế hoạch từ đầu đến cuối: 45 bước theo ngày (09/10–31/12/2026 và bảo vệ), mốc kiểm tra, hướng dẫn gán nhãn, đặc tả phương pháp, giao thức thực nghiệm, tích hợp CopyPro, câu hỏi phản biện, tự chấm theo thang 10. |

Đề cương đã sửa theo nhận xét của Khoa; bản cuối ngày 10/10/2026 chờ CBHD xác nhận ở mốc 12/10. Repo chưa có dữ liệu thực nghiệm. Thư mục `data/`, `src/`, `tests/`, `ket_qua/`, `luan_van/` được tạo ở bước 03 của kế hoạch.

## Cấu trúc thư mục

```
.
├── CHI_TIET_TUYEN_TINH_KHOA_LUAN.md   # kế hoạch tuyến tính
├── de_cuong/                          # đề cương: bản cuối (PDF), bản làm việc (.docx, bản chữ đỏ)
│   └── nguon/                         # mã dựng đề cương từ khung của Khoa và nội dung
├── báo/                               # bài báo gốc (PDF), bản quyền thuộc tác giả và nhà xuất bản
├── dịch/                              # bản dịch máy để đọc
└── run_translate_batch.sh             # dịch hàng loạt PDF bằng pdf2zh
```

## Dựng lại đề cương sau khi sửa nội dung

Sửa chữ trong `de_cuong/nguon/noi_dung.py`. Hàm `K(...)` giữ nguyên chữ của bản đã nộp (chữ đen), hàm `N(...)` đánh dấu phần mới hoặc sửa (chữ đỏ). Sau đó chạy:

```bash
cd de_cuong/nguon
pip install python-docx lxml matplotlib
python3 ve_hinh1.py            # vẽ Hình 1
python3 dung_docx.py           # bản chữ đỏ
python3 dung_docx.py --sach    # bản sạch để nộp
python3 kiem_tra.py            # chữ đen khớp bản đã nộp, mọi tài liệu đều được trích, đúng thứ tự
```

Trích dẫn được đánh số tự động theo thứ tự xuất hiện (chuẩn IEEE). Bảng khai báo trong `noi_dung.py` (`BANG_1`, `BANG_2`), mỗi ô là danh sách `K(...)`/`N(...)` như đoạn văn. Xuất PDF bằng LibreOffice: `soffice --headless --convert-to pdf ../*.docx`.

## Tài liệu cũ

Phiên bản trước của đề tài ("kiểm chứng thông tin quảng cáo dựa trên bằng chứng văn bản cho tai nghe không dây") đã được gỡ khỏi thư mục làm việc. Phiên bản đó gồm sổ tay B01–B52, `docs/`, `evidence/`, `scripts/`, `templates/`, `tests/`, `Đọc_báo_cùng_HuP_3_.docx` và `Đọc_báo_cùng_HuP_4_.docx`, và vẫn còn trong lịch sử Git ở commit `ba88a48`. Ví dụ, để lấy lại một tệp:

```bash
git checkout ba88a48 -- scripts/capture_evidence.mjs
```

**Bảo mật:** lịch sử Git từng chứa tệp `.env`. Nếu khóa API trong đó chưa được thu hồi, hãy thu hồi ở trang của nhà cung cấp và tạo khóa mới. Khóa chỉ để trong `.env` cục bộ; tệp này đã được đưa vào `.gitignore`.

## Công cụ dịch bài báo

Script `run_translate_batch.sh` dịch các PDF trong `báo/` sang tiếng Việt và lưu vào `dịch/`. Trước khi chạy, sửa các đường dẫn `VENV`, `INPUT_DIR`, `OUTPUT_DIR` trong script cho đúng máy.

```bash
bash run_translate_batch.sh
```
