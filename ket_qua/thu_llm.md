# Bước 2 — Môi trường thực nghiệm và thử LLM ban đầu

**Ngày thực hiện/tra cứu:** 13/10/2026, múi giờ Asia/Ho_Chi_Minh.
**Kết luận:** phần môi trường và kiểm thử offline chạy được. **Bước 2 chưa
hoàn thành đầy đủ**: chưa có khóa mới để thử LLM thật, chưa xác minh quota/gói
tài khoản, và chưa xác nhận việc thu hồi khóa từng lộ trong lịch sử Git.
Không dùng kết quả mock để kết luận chất lượng hay tốc độ của LLM.

## 1. Repo và tài liệu chuẩn

- Repo làm việc: `/home/phuocblh/KLTN/KLTN`, remote
  `https://github.com/23521228-BuiLeHuyPhuoc/KLTN.git`, nhánh `main`.
- HEAD lúc bắt đầu: `78c8150`; working tree sạch. Không tìm thấy `AGENTS.md`
  áp dụng trong repo hoặc các thư mục cha đã kiểm tra. Đã đọc README và quy
  ước T3.5. Không commit/push theo yêu cầu phiên này.
- Thư mục mở ban đầu là repo CopyPro bên cạnh. Chỉ khảo sát trạng thái ở đó,
  giữ nguyên tệp kế hoạch chưa được Git theo dõi của người dùng.
- Chuẩn: `de_cuong/23521228_BuiLeHuyPhuoc_DeCuongKLTN.pdf`, xuất từ
  `_ban_cuoi.docx`, theo README. Đọc PDF bằng `pdftotext`, đối chiếu mục Nội
  dung 2 và lịch tháng 09/2026: thử LLM phù hợp tài nguyên, trích bộ thông số
  có nguồn. Không dùng bản `.docx` cũ hay bản chữ đỏ làm chuẩn.
- Đã đọc Bước 2, T3.1, T3.5, T4.6, T5.1 và T5.3 trong kế hoạch tại repo đúng.
  Không sửa đề cương, kế hoạch, lịch, nhãn dữ liệu nghiên cứu hay Google Sheets.
- SHA-256 kế hoạch: `bed0dc2251659f2ea613d9c21f4e4f571081a56a559b22ad480619f30e38e9a7`.
  SHA-256 PDF bản cuối: `e3cf1d2d09184c555525ad265d0fa63e45b51ab75d4342c96143452b037ca0c3`.

## 2. Tài nguyên môi trường thực thi

Nguồn máy đọc được: [environment.json](thu_llm/environment.json), ghi lúc
13:21:21 +07:00. Đây là **môi trường shell thực thi công việc**, chưa xác minh
đây có phải máy cá nhân của sinh viên hay không. `systemd-detect-virt` trả
`none` (exit 1): công cụ không phát hiện VM/container; không dùng kết quả này
để khẳng định quyền sở hữu hoặc vị trí máy.

| Hạng mục | Đo được |
|---|---|
| Hệ điều hành | Ubuntu 26.04.1 LTS, Linux 7.0.0-38-generic, x86_64 |
| CPU | Intel Core i7-4770 @ 3.40 GHz; 4 lõi/8 luồng; tiến trình được dùng 8 CPU logic |
| RAM | 15.02 GiB tổng; khoảng 3.95 GiB khả dụng lúc ghi |
| Swap | 4 GiB, gần hết phần trống ở thời điểm ghi |
| GPU | Intel đồ họa tích hợp, PCI 8086:0412; không có `nvidia-smi` hay thiết bị NVIDIA được phát hiện |
| VRAM | Chưa xác minh bộ nhớ GPU riêng; đồ họa tích hợp dùng bộ nhớ chia sẻ |
| Ổ đĩa tại repo | Khoảng 217.97 GiB tổng, 97.32 GiB trống |
| Python | CPython 3.14.4; `.venv/bin/python` |
| Môi trường ảo | `/home/phuocblh/KLTN/KLTN/.venv`; Python hệ thống không bị thay đổi |

Nhận định kỹ thuật: bộ thử qua API phù hợp hơn với RAM đang khả dụng và không
có GPU CUDA. Chạy model nhỏ lượng tử hóa trên CPU có thể là hướng thử sau,
nhưng chưa đo được tốc độ hay mức RAM của model nào. Không tải trọng số lớn,
không cài local LLM chỉ để đủ hình thức; GPT-OSS được đưa vào danh sách thử
qua Groq. Không thay đổi quy trình thực nghiệm chính từ nhận định này.

## 3. Thư viện và thiết lập

Đã tạo đủ `data/`, `src/kiemchung/`, `tests/`, `scripts/`, `ket_qua/`,
`luan_van/`. Package cài editable bằng `pyproject.toml`; import dùng được cả
trong script và pytest. Chỉ có giao diện LLM và bộ thử, chưa cài BM25, P hay API
kiểm chứng.

| Thư viện | Phiên bản đã chạy |
|---|---|
| rank-bm25 / pyvi | 0.2.2 / 0.1.1 |
| pydantic / pyyaml | 2.14.1 / 6.0.3 |
| google-genai / groq | 2.30.0 / 1.7.0 |
| fastapi / uvicorn | 0.143.0 / 0.54.0 |
| pytest | 9.1.1 |
| scikit-learn / statsmodels | 1.9.1 / 0.15.0 |
| pandas / matplotlib | 3.0.6 / 3.11.2 |
| playwright | 1.63.0 |
| python-dotenv | 1.2.4 |

Chọn Pyvi vì gọn, có tokenizer tiếng Việt, không kéo runtime học sâu. Đã chạy
`ViTokenizer.tokenize`: “Điện_thoại có thời_lượng pin tốt”. Chưa xây mô-đun
truy hồi. Thêm python-dotenv để nạp khóa cục bộ mà không thực thi shell.
Playwright mới kiểm import, chưa cần tải trình duyệt cho bước này.

`requirements.txt` khóa phụ thuộc trực tiếp, `requirements-lock.txt` ghi đầy
đủ phụ thuộc gián tiếp. Đã thay bản prerelease wrapt do resolver chọn bằng bản
ổn định 2.5.0 và kiểm tra lại. Bộ phiên bản có NumPy/SciPy cần Python ≥ 3.12,
nên metadata package đặt ≥ 3.12 (đáp ứng yêu cầu ≥ 3.10 của kế hoạch); môi trường
đã kiểm chứng là 3.14.4. Không tuyên bố bộ pin này chạy trên Python 3.10/3.11.

## 4. Gọi LLM, cache và nhật ký

`src/kiemchung/llm.py` cung cấp `LLMClient.call` chung cho Gemini Developer
API và Groq. Provider/model/tham số/cấu hình JSON truyền từ ngoài. Khóa API
chỉ đọc từ biến môi trường, không đưa vào request để lưu.

- SHA-256 trên JSON có sắp thứ tự khóa; giữ nguyên thứ tự messages và nội dung
  prompt. Bao gồm provider, model, messages, parameters, JSON mode, output
  schema, phiên bản adapter/cache và chế độ mock/live.
- Cache JSON bền vững, ghi qua tệp tạm rồi thay thế nguyên tử; kiểm checksum
  nội dung. Lưu request, output, model thực trả về, token usage và thời gian.
- JSONL ghi từng lần gọi thật, lỗi/retry và cache hit; có request, thời điểm,
  tham số, hash, trạng thái, thời lượng và usage khi có. Cache hit không được
  cộng thành token mới. Không lưu header, khóa hay exception thô từ SDK.
- Timeout 30 giây, tối đa 2 retry, backoff ngắn có giới hạn. Retry lỗi tạm
  thời/timeout, không retry sai khóa/quyền, model không có hay yêu cầu sai.
  Retry của SDK tắt để tránh nhân số lần gọi.
- Lỗi API, output rỗng, bị chặn hoặc chưa hoàn tất không cache thành công.
  Output JSON sai cấu trúc vẫn được giữ để đánh giá lỗi model.
- Mock dùng transport giả và cache namespace riêng. Đây là thiết kế tuần tự
  cho khóa luận một người; chưa gom các cache miss đồng thời từ nhiều tiến trình.

Tham chiếu SDK chính thức, kiểm ngày 13/10/2026:
[Google Gen AI Python](https://googleapis.github.io/python-genai/),
[Groq Python SDK](https://github.com/groq/groq-python).
Hai adapter đã được kiểm với SDK cài thực tế và HTTP giả lập, chưa qua máy chủ
thật do thiếu khóa.

## 5. Model và hạn mức công bố

Tra tài liệu chính thức ngày **13/10/2026**; không mặc định tên model cũ còn
phục vụ. Các mức dưới là thông tin công bố, **quota thực tế của tài khoản:
chưa xác minh**, gồm cả quyền truy cập model và trạng thái billing.

| Ứng viên | Thông tin công bố và lý do đưa vào thử |
|---|---|
| Google `gemini-3.6-flash` | Trang hiện hành vẫn liệt kê, có input/output miễn phí ở Free tier Standard; giữ ứng viên phù hợp tên dự kiến trong kế hoạch. Không suy ra tài khoản này được miễn phí từ thông tin đó. |
| Groq `openai/gpt-oss-20b` | Model production, open-weight; thêm ứng viên nhỏ hơn để so với 120B qua cùng provider. |
| Groq `openai/gpt-oss-120b` | Model production, open-weight; ứng viên dự kiến trong kế hoạch, không tải trọng số về máy. |

Google đo RPM, TPM và RPD theo project, không theo từng khóa. Trang công khai
hiện chỉ dẫn xem hạn mức hoạt động trong AI Studio; không ghi một con số cố
định cho project chưa truy cập được. Nguồn:
[Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits),
[Gemini pricing — 3.6 Flash](https://ai.google.dev/gemini-api/docs/pricing#gemini-3.6-flash).

Bảng Free Plan Limits của Groq tại thời điểm đọc liệt kê **cả GPT-OSS 20B và
120B**: 30 RPM, 1.000 RPD, 8.000 TPM, 200.000 TPD. Giới hạn áp dụng theo
organization, có ngoại lệ; cần xem Limits của tài khoản trước khi chạy. Nguồn:
[Groq rate limits](https://console.groq.com/docs/rate-limits),
[Groq supported models](https://console.groq.com/docs/models).
Không nhầm bảng tốc độ/giá Developer trong trang models với quota Free thực tế.

Danh sách này là **ứng viên**, chưa xếp hạng chất lượng hay chọn model cho
thực nghiệm chính. Script yêu cầu người chạy xác nhận free tier trước khi gọi
thật; không tự bật billing, nâng gói, dùng paid tier hay tải local model.

## 6. Bộ câu và kết quả thực tế

10 câu từ T4.6 số **1, 2, 6, 8, 9, 11, 12, 13, 16, 18**, chỉ thuộc tập phát
triển. Xem [cases.json](../data/thu_llm/cases.json) và
[quy ước kỳ vọng](../data/thu_llm/README.md). Kỳ vọng được điền từ câu trong
kế hoạch trước khi chạy model, không lấy đầu ra model làm đáp án và không
phải nhãn chuẩn nghiên cứu.

Bao phủ số/đơn vị, bộ sạc, mốc sạc, bộ phận hộp sạc, chống ồn/xuyên âm, nguồn
điện thấp, độ sáng cực đại, “đến”, “luôn”, cùng thông tin không được phép suy
diễn. Cùng system prompt/schema, temperature=0, top_p=1, trần output 2048;
cơ chế reasoning/token của provider có thể khác nhau.

Lượt offline cuối: [manifest](thu_llm/2026-10-13-offline-final/manifest.json),
[kết quả từng câu](thu_llm/2026-10-13-offline-final/results.jsonl),
[nhật ký](thu_llm/2026-10-13-offline-final/calls.jsonl).

| Cấu hình giả lập | Số câu | Gọi transport mock mới | Lượt lặp lấy cache | Chất lượng/token API thật |
|---|---:|---:|---:|---|
| Gemini 3.6 Flash | 10 | 10 | 10 | Chưa đo; metrics=null |
| GPT-OSS 20B | 10 | 10 | 10 | Chưa đo; metrics=null |
| GPT-OSS 120B | 10 | 10 | 10 | Chưa đo; metrics=null |

Các thời gian dưới 1 ms trong manifest là **thời gian mock/đọc cache**, không
phải tốc độ LLM. JSON rỗng của mock chỉ thử đường đi, không giả làm kết quả
trích xuất. Có lưu cả lượt chạy đầu khi đang hoàn thiện công cụ; báo cáo dùng
lượt `offline-final`, có bản chụp mã và hash nguồn.

Lượt live chỉ chạy tiền kiểm: [manifest](thu_llm/2026-10-13-live-preflight-final/manifest.json).
Cả 3 model bị chặn bởi `missing_api_key` và `free_tier_not_confirmed`; **0
yêu cầu API thật**, không phát sinh chi phí từ việc gọi LLM. Chưa có số đo
schema hợp lệ, độ đúng từng trường, lỗi thiếu/bịa điều kiện, độ trễ API hay
token usage thực tế. Công cụ đã sẵn sàng ghi các số đo đó khi có khóa và quota.

## 7. Kiểm tra đã chạy

| Lệnh/kiểm tra | Kết quả thực tế |
|---|---|
| `python3 -m venv .venv` | Tạo môi trường riêng thành công |
| `.venv/bin/python -m pip install -r requirements.txt -c requirements-lock.txt -e .` | Cài được package editable và bộ phiên bản đã khóa |
| `.venv/bin/python -m pip check` | `No broken requirements found.` |
| `.venv/bin/python scripts/kiem_tra_moi_truong.py` | 16 import đạt; Pyvi và Matplotlib Agg chạy được |
| `.venv/bin/python -m pytest -q` | **32 passed**, 1 warning từ SDK Google trên Python 3.14; xem [pytest.txt](thu_llm/pytest.txt) |
| `scripts/thu_llm.py --mode offline` (bằng Python trong .venv) | 30 câu theo cấu hình, 30 cache hit lặp; exit 0 |
| `scripts/thu_llm.py --mode live` (bằng Python trong .venv) | Tiền kiểm bị chặn đúng dự kiến, exit 2; không gọi mạng API |
| `git check-ignore .env` | In `.env` |
| `git ls-files -- .env` | Rỗng, `.env` hiện không được theo dõi |
| `git diff --check` | Đạt |

Kiểm thử tự động không dùng API thật; chặn socket trong test adapter và dùng
HTTP giả lập với SDK thật. Bao phủ gọi hai lần chỉ một lần đến provider, cache
qua client mới và **tiến trình Python mới**, thay provider/model/prompt/tham số/
schema làm đổi hash, cache mock không dùng cho live, retry có giới hạn, lỗi
không cache, cache hỏng, thiếu khóa, output bị cắt/chặn, chống lộ khóa trong
request/output/log, chuyển đổi request/usage Gemini/Groq và CLI offline/live.

Warning còn lại là `DeprecationWarning` về `_UnionGenericAlias` trong
`google/genai/types.py`, dự kiến bị bỏ ở Python 3.17; không làm hỏng bài kiểm
trên 3.14.4. Không sửa mã thư viện bên thứ ba để giấu warning.

## 8. Khóa API và việc còn cần người dùng

[security_check.json](thu_llm/security_check.json) chỉ lưu trạng thái và metadata
Git, không lưu nội dung khóa. Commit `8946bb0` ngày 08/10 chứa lịch sử `.env`;
commit `966f8ad` cùng ngày bỏ theo dõi và ghi cần thu hồi. Không đọc/in giá trị
khóa lịch sử, không dùng lại chúng, không viết lại lịch sử hoặc force-push.

Hiện không có `.env` ở repo, không có `GEMINI_API_KEY`/`GROQ_API_KEY` trong
tiến trình. `.env.example` có hai biến rỗng; `.env`, venv và bytecode bị ignore;
cache và kết quả JSON/JSONL vẫn được giữ. Kiểm tra mẫu khóa và giá trị bí mật
trong môi trường không thấy lộ trong các tệp đã quét; điều đó **không chứng
minh khóa cũ đã được thu hồi**.

Người dùng cần:

1. Thu hồi khóa từng lộ tại nhà cung cấp nếu chưa làm, tạo khóa mới; ghi nhận
   việc thu hồi bằng xác nhận không chứa khóa. Chỉ bỏ `.env` khỏi Git là chưa đủ.
2. Điền khóa mới vào `.env` cục bộ, xác minh Free tier và quota trong console.
   Không gửi khóa vào chat hoặc commit. Không tự dùng lại khóa trong lịch sử.
3. Chạy lệnh live trong [README](../README.md#thử-api-thật); có thể yêu cầu
   trợ lý chạy tiếp sau khi cấu hình. Xem lỗi từng câu và cập nhật báo cáo bằng
   kết quả thật trước khi đánh dấu Bước 2 hoàn tất.

## 9. Trạng thái từng yêu cầu

| Mục | Trạng thái | Căn cứ/phần còn thiếu |
|---|---|---|
| 2.1 Cấu trúc và nhật ký | Xong | Đủ sáu thư mục, package/import, nhật ký ngày thật |
| 2.2 Môi trường/thư viện | Xong | Venv riêng, đủ thư viện, pin/lock, smoke và pip check đạt |
| 2.3 Biến môi trường | Xong | Mẫu rỗng, ignore đúng, `.env` không tracked; khóa thật chưa được cung cấp |
| 2.4 Khóa trong lịch sử | Xong một phần | Đã xác nhận lịch sử; chưa xác minh việc thu hồi/tạo mới |
| 2.5 Hàm gọi LLM | Xong | Hai adapter, cache/log, timeout/retry, kiểm thử offline; kết nối thật chờ khóa |
| 2.6 Tài nguyên/hạn mức | Xong một phần | Tài nguyên và tài liệu công bố đã ghi; quota/billing tài khoản chưa xác minh |
| 2.7 Thử 5–10 câu | Xong một phần | 10 câu, kỳ vọng, script, offline đầy đủ; thử LLM thật bị chặn |

Chưa đánh dấu Bước 2 hoàn thành trong kế hoạch. Những việc phụ thuộc tài khoản
và khóa cần hoàn tất trước khi kết luận đã thử thành công các LLM ứng viên.
