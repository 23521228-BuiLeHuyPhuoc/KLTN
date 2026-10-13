# KLTN – Khóa luận tốt nghiệp

**Đề tài:** Phương pháp kiểm chứng tuyên bố về thông số kỹ thuật có điều kiện ràng buộc trong quảng cáo
(*A method for condition-aware verification of technical specification claims in advertising*)

**Sinh viên:** Bùi Lê Huy Phước (23521228, MMTT2023.2) · **CBHD:** ThS Trần Hồng Nghi · **Thời gian:** 15/09/2026 – 31/12/2026

## Hai tài liệu chính

| Tài liệu | Nội dung |
|---|---|
| [Đề cương bản cuối](de_cuong/23521228_BuiLeHuyPhuoc_DeCuongKLTN.pdf) | `de_cuong/23521228_BuiLeHuyPhuoc_DeCuongKLTN.pdf`, bản gửi CBHD ngày 11/10/2026, xuất từ `de_cuong/23521228_BuiLeHuyPhuoc_DeCuongKLTN_ban_cuoi.docx` (bản Google Docs tải về dạng .docx, đã sửa các chỗ ghi ở Bước 1 của kế hoạch và sửa định dạng: phông Times New Roman, không còn khoảng trống lớn). Mọi kế hoạch bám theo bản này. Bản ngày 10/10/2026 (`23521228_DECUONGKHOALUAN_UIT.pdf`) đã được thay, vẫn còn trong lịch sử Git ở commit `cf9dfd3`. |
| [Bản làm việc cũ của đề cương](de_cuong/) | `23521228_BuiLeHuyPhuoc_DeCuongKLTN.docx` và `..._chu_do.docx`/`.pdf` (tô đỏ phần sửa so với đề cương đã nộp) được dựng bằng script trước khi chuyển sang Google Docs. Đây không phải bản gửi CBHD và không cần sửa; nội dung có vài chỗ khác bản cuối (ví dụ tên tiếng Anh). |
| [Chi tiết tuyến tính của khóa luận](CHI_TIET_TUYEN_TINH_KHOA_LUAN.md) | Kế hoạch khớp đề cương bản cuối, đọc từ trên xuống là làm theo: đầu file là danh sách 47 bước theo đúng thứ tự làm (từ 11/10/2026 đến khi bảo vệ, bắt đầu ở Bước 1), xen 7 mốc kiểm tra với CBHD; mỗi bước có ngày, việc cần làm, tệp phải làm ra và tiêu chí xong. Phần Tra cứu cuối file gồm lịch tổng thể, quy ước dự án, hướng dẫn gán nhãn, đặc tả phương pháp P, thực nghiệm, tích hợp CopyPro, rủi ro, các điểm cần chốt khi làm thử, câu hỏi phản biện, bảng đối chiếu với đề cương. |

Đề cương đã sửa theo nhận xét của Khoa và các chỗ ghi ở Bước 1 của kế hoạch; bản cuối ngày 11/10/2026 chờ CBHD xác nhận ở mốc 12/10. Đã dựng môi trường Bước 2 và bộ câu thử kỹ thuật từ ví dụ tập phát triển; chưa có dữ liệu thực nghiệm chính. Trạng thái, giới hạn và kết quả chạy được ghi tại [báo cáo thử LLM](ket_qua/thu_llm.md).

## Cấu trúc thư mục

```
.
├── CHI_TIET_TUYEN_TINH_KHOA_LUAN.md   # kế hoạch: danh sách việc ở đầu file, tra cứu ở cuối
├── de_cuong/                          # đề cương: bản cuối (PDF, _ban_cuoi.docx), bản làm việc cũ (.docx, bản chữ đỏ)
│   └── nguon/                         # mã dựng đề cương từ khung của Khoa và nội dung
├── báo/                               # bài báo gốc (PDF), bản quyền thuộc tác giả và nhà xuất bản
├── dịch/                              # bản dịch máy để đọc
└── run_translate_batch.sh             # dịch hàng loạt PDF bằng pdf2zh
```

## Môi trường thực nghiệm Bước 2

Các thư mục mới: `data/thu_llm/` (10 câu, đáp án trích xuất và cấu hình model),
`src/kiemchung/` (giao diện gọi LLM, công cụ thử), `tests/`, `scripts/`,
`ket_qua/` (cache, nhật ký gọi và kết quả), `luan_van/nhat_ky.md`.

Đã kiểm chứng trên Ubuntu x86_64, **Python 3.14.4**, môi trường `.venv` riêng.
Kế hoạch yêu cầu Python ≥ 3.10; bộ phiên bản được chọn cần **Python ≥ 3.12**
do NumPy/SciPy hiện dùng. Chỉ Python 3.14.4 đã được chạy kiểm tra thực tế.
Không cài vào Python hệ thống.

```bash
cd /home/phuocblh/KLTN/KLTN
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -c requirements-lock.txt -e .
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
.venv/bin/python scripts/kiem_tra_moi_truong.py
.venv/bin/python scripts/thu_llm.py --mode offline
```

`requirements.txt` khóa các thư viện trực tiếp; `requirements-lock.txt` khóa
cả phụ thuộc gián tiếp của môi trường đã thử. Chọn **Pyvi** vì đủ cho thử tách
từ tiếng Việt, không cần thêm runtime học sâu. `python-dotenv` là thư viện bổ
sung duy nhất phục vụ nạp `.env` mà không thực thi nội dung như lệnh shell.
Playwright đã cài package và kiểm tra import; chưa tải trình duyệt vì chưa đến
bước thu thập trang.

### Thử API thật

Trước tiên thu hồi khóa từng lộ trong lịch sử Git, tạo khóa mới ở nhà cung cấp.
Lưu khóa mới vào `.env` cục bộ, không dán vào chat hay terminal output.
Chỉ tạo mẫu nếu chưa có tệp để tránh ghi đè khóa đang dùng:

```bash
test -e .env || cp .env.example .env
chmod 600 .env
git check-ignore .env
git ls-files -- .env
```

Lệnh đầu kiểm tra Git phải in `.env`, lệnh sau phải không có kết quả.
Sau khi điền khóa bằng trình soạn thảo, xác minh project Google và organization
Groq đang ở **Free tier** cùng quota thực tế trong console. Khi đã xác minh:

```bash
.venv/bin/python scripts/thu_llm.py --mode live --confirm-free-tier
```

Cờ trên ghi nhận xác nhận của người chạy, không tự kiểm tra hay thay đổi billing.
Không có khóa hoặc thiếu cờ thì script chỉ ghi trạng thái bị chặn, trả mã 2,
không gọi API. Có thể chỉ thử một model:

```bash
.venv/bin/python scripts/thu_llm.py --mode live --confirm-free-tier --model openai/gpt-oss-20b
```

Đổi model/tham số trong `data/thu_llm/models.json`, không cần sửa giao diện gọi.
Script dùng cùng 10 câu và cùng yêu cầu JSON cho các model; tối đa 30 yêu cầu
khác nhau khi chạy cả 3 ứng viên, tối đa 3 lần thử cho mỗi yêu cầu lỗi tạm thời.
Dừng model đang chạy khi hết retry hay lỗi xác thực/model. Mỗi câu được gọi
lại bằng client mới để xác nhận cache. Mặc định giãn 20 giây sau một kết quả
API mới; quota tài khoản có thể đòi hỏi giãn thêm. Không tự nâng cấp gói.

Mỗi lượt tạo thư mục mới có dấu thời gian trong `ket_qua/thu_llm/`, gồm đầu vào,
cấu hình, bản chụp mã thử, `manifest.json`, kết quả từng câu và nhật ký khi có
lần gọi. `--output` chỉ nhận thư mục chưa tồn tại. Cache JSON dùng chung nằm
ở `ket_qua/llm_cache/`; `--cache-dir` cho phép chọn cache riêng. **Mock và live
có khóa cache khác nhau**. Cache và các kết quả JSON/JSONL được giữ để tái lập,
không bị `.gitignore` loại trừ. Không có khóa xác thực trong các tệp này.

`LLMClient.call(provider, model, messages, parameters, json_output=True)` là
giao diện chung. `output_schema` tùy chọn cũng tham gia khóa cache. Hàm nhận
tin nhắn text (`system` đầu tiên nếu có, `user`, `assistant`); không hỗ trợ
ảnh, tool calling hay streaming trong Bước 2. Hàm đọc khóa từ biến môi trường;
script tự nạp `.env` và không ghi đè biến đã có trong tiến trình.

Timeout mặc định 30 giây cho lần gọi, retry tối đa 2 lần; SDK retry đã tắt.
Lỗi được chuyển sang mã an toàn (xác thực/quyền, model không tồn tại, yêu cầu
không hợp lệ, lỗi tạm thời, timeout). Không lưu nội dung exception gốc vì có
thể chứa khóa. Cache lỗi/hỏng bị báo rõ và không âm thầm gọi lại API; chỉ xóa
đúng cache lỗi sau khi kiểm tra nếu muốn thử lại. Cache ghi thay thế nguyên tử,
thiết kế chạy tuần tự; chưa chống hai tiến trình cùng gọi API cho một cache miss.

`usage` trong kết quả cache là token của lần sinh ban đầu. Nhật ký cache hit
có `usage=null`, `source_usage` riêng; `elapsed_ms` đo lần gọi hiện tại còn
`generation_ms` giữ thời gian sinh ban đầu (kể cả retry/backoff). Không cộng
token của cache hit thành token API mới. Output hết giới hạn, bị chặn hoặc rỗng
không được cache thành công. JSON không đúng schema vẫn được lưu là đầu ra API
để phân tích lỗi, và bị công cụ thử đánh dấu schema không hợp lệ.

Xem [bộ câu và quy ước chấm](data/thu_llm/README.md),
[báo cáo thực tế và nguồn quota](ket_qua/thu_llm.md).

## Dựng lại đề cương sau khi sửa nội dung

> Bản cuối (PDF) xuất từ `23521228_BuiLeHuyPhuoc_DeCuongKLTN_ban_cuoi.docx`, không dựng từ các script dưới đây. Các script chỉ dựng lại bản làm việc cũ: chạy `dung_docx.py` sẽ ghi đè hai tệp `.docx` làm việc (không đụng tới tệp `_ban_cuoi.docx`) bằng nội dung cũ trong `noi_dung.py`, và PDF xuất từ các tệp này không được chép đè lên `23521228_BuiLeHuyPhuoc_DeCuongKLTN.pdf` (bản cuối).

Sửa chữ trong `de_cuong/nguon/noi_dung.py`. Hàm `K(...)` giữ nguyên chữ của bản đã nộp (chữ đen), hàm `N(...)` đánh dấu phần mới hoặc sửa (chữ đỏ). Sau đó chạy:

```bash
cd de_cuong/nguon
pip install python-docx lxml matplotlib
python3 ve_hinh1.py            # vẽ Hình 1
python3 dung_docx.py           # bản chữ đỏ
python3 dung_docx.py --sach    # bản sạch (cũ)
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
