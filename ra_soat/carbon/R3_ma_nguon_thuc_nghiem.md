# R3 · Rà soát mã nguồn, kiểm thử và kết quả thực nghiệm
Ngày: 18/11/2026 · Người rà soát: Gemini 4 Carbon · Phạm vi: Bước 2, 11, 14, 15, 21, 22, 27 và phần đã bắt đầu của Bước 28–30 (kèm mã làm sớm liên quan ở Bước 31, 34, 37), đối chiếu T5.1–T5.9, T6.1–T6.3, T12, hướng dẫn gán nhãn bản 2 và nhật ký.

## Tóm tắt
Đáng lo ngại nhất là phương pháp P khi chạy thực tế từ đầu ra trích xuất Bước 22 (`openai/gpt-oss-120b`, `k=5`) sang bộ quyết định Bước 27 trên 66 tuyên bố bộ thử đang gán `CHUA_DU` cho `34/66` tuyên bố (`51,5%`), kéo Recall nhãn Đúng của P tụt xuống `41,2%` (`14/34`, thấp hơn B0 tới `55,9` điểm phần trăm, vỡ giả thuyết H1) và `Macro-F1 = 35,8%` (thấp hơn cả bản cắt bỏ `P−ĐK` = `37,5%`) do hàng loạt lỗi khớp nối giữa tệp cấu hình YAML, `trich_xuat.py`, `chia_doan.py` và `quyet_dinh.py` mà bộ test dựng tay không phát hiện được. Về hạ tầng thực nghiệm, câu lệnh của B1 và B2 nhúng nguyên văn `35.915` ký tự hướng dẫn khiến `100%` tuyên bố vượt gấp `1,8–2,3` lần trần `8.000` TPM của Groq Free Tier (sẽ lỗi HTTP 413 toàn bộ), trong khi Gemini Free Tier bị khóa ở `~20` lượt/ngày và đối chứng B3 (SemViQA) chưa có một dòng mã nào. Ngoài ra, cơ chế chấm lỗi LLM hiện đang thiên vị P một cách bất hợp lệ (B0–B2 lỗi bị phạt nhãn `LOI`, còn P lỗi lại đổi thành `CHUA_DU` và được tính điểm đúng khi nhãn chuẩn là `CHUA_DU`), còn tiến độ tới Mốc 3 (`27/11`, còn 9 ngày) đã bất khả thi toán học ở yêu cầu gán lại mù cách tối thiểu 10 ngày của Bước 32.

## Bảng phát hiện
| Mã | Mức độ | Loại | Tiêu đề | Chỗ |
|---|---|---|---|---|
| R3-01 | NGHIÊM TRỌNG | khong_kha_thi | Câu lệnh B1 và B2 vượt gấp ~2 lần trần 8.000 TPM của Groq Free Tier ở 100% tuyên bố, còn Gemini chạm trần ~20 lượt/ngày | `src/kiemchung/doi_chung/huong_dan.py:27-34`, `src/kiemchung/llm.py:150-151` |
| R3-02 | NGHIÊM TRỌNG | sai_buoc_da_lam | Bất đối xứng khi xử lý lỗi LLM: B0–B2 bị phạt nhãn `LOI`, còn P biến lỗi LLM thành `CHUA_DU` và hưởng điểm khống | `src/kiemchung/quyet_dinh.py:716-718`, `src/kiemchung/danh_gia.py:21,85-92` |
| R3-03 | NGHIÊM TRỌNG | sai_buoc_da_lam | Lỗi khớp cụm có ngoặc trong YAML, cắt mất tiêu đề cột bảng so sánh và `vung_do` một dòng làm Recall Đúng của P tụt còn 41,2% | `data/cau_hinh/dien_thoai.yaml:209-220`, `src/kiemchung/trich_xuat.py:369-453` |
| R3-04 | NGHIÊM TRỌNG | khong_kha_thi | Khối lượng còn thiếu trước Mốc 3 (27/11) không khả thi; Bước 32 bất khả thi toán học về khoảng cách gán lại mù ≥ 10 ngày | `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:806,848,884`, `data/chia_tap.json:57` |
| R3-05 | NGHIÊM TRỌNG | sai_buoc_da_lam | Đổi đơn vị giờ ↔ phút làm đảo chiều thuận lợi ở `dong_ho.sac_nhanh` và hỏng điều kiện số khác đơn vị trái Hướng dẫn 6.2–6.3 | `src/kiemchung/quyet_dinh.py:81-84,189-190`, `src/kiemchung/trich_xuat.py:293,329,392` |
| R3-06 | CAO | sai_buoc_da_lam | Luật tự cài `lan_dieu_kien` ghi đè sai điều kiện khi hai chế độ trùng con số và phát tán `dieu_kien_khac` sang đoạn sạch | `src/kiemchung/quyet_dinh.py:276-317` |
| R3-07 | CAO | sai_buoc_da_lam | `b1.py` cắt bỏ trường sản phẩm và hãng khỏi đầu vào của B1 và cấp trần token đầu ra thấp bằng một nửa P | `src/kiemchung/doi_chung/b1.py:27-44`, `src/kiemchung/doi_chung/b0.py:38` |
| R3-08 | CAO | sai_buoc_da_lam | Lỗi biên ở `_khang_dinh`, `doc_so` với khoảng giá trị và phép so sánh số thực bất đối xứng gây FAR và phụ thuộc thứ tự đoạn | `src/kiemchung/chuan_hoa.py:64-66,222,287-297`, `src/kiemchung/cau_hinh.py:173` |
| R3-09 | CAO | sai_buoc_da_lam | Pytest hiện hỏng 2 test, bỏ qua 1 test do `.venv` thiếu gói so với `requirements.txt`, và có 0 test tích hợp `xu_ly` + `quyet_dinh` | `tests/test_llm.py:57-72`, `tests/test_thu_llm.py:45-52`, `requirements.txt:1,12-14` |
| R3-10 | CAO | sai_buoc_da_lam | Dữ liệu phát triển và bộ nhớ đệm LLM bị phân mảnh; `data/nhan/thu.jsonl` vẫn giữ nguyên bản nhãn Lượt 1 lỗi thời | `data/nhan/thu.jsonl`, `scripts/chay_trich_xuat.py:201`, `scripts/danh_gia_he.py:448-450` |
| R3-11 | CAO | rui_ro_hoi_dong | Bước 2 chưa có lượt gọi LLM thật nào; mô hình duy nhất chạy xong Bước 15 và 22 trùng với LLM sinh quảng cáo | `ket_qua/thu_llm.md:4-6,169-172`, `scripts/sinh_bo_thu.py:31` |
| R3-12 | CAO | sai_buoc_da_lam | `src/kiemchung/chia_doan.py` ghi cứng 14 ngoại lệ theo mã đoạn và văn bản của 2 mẫu thuộc tập kiểm tra | `src/kiemchung/chia_doan.py:768-798` |
| R3-13 | TRUNG BÌNH | thieu_can_bo_sung | `danh_gia_he.py` gộp nhầm hệ tham chiếu B4 vào họ hiệu chỉnh Holm, thiếu 2 phép độ nhạy và thiếu thời gian của P/B1/B2 | `scripts/danh_gia_he.py:213,327-338`, `src/kiemchung/bao_cao_ket_qua.py:86-105` |
| R3-14 | TRUNG BÌNH | sai_buoc_da_lam | Luật chép đúng nhãn (QĐ15) khớp nhầm nhãn con thiếu điều kiện nhóm và ghi thừa `mac_dinh` cho ca so thẳng (kiểu V12) | `src/kiemchung/quyet_dinh.py:322-375,526-554` |
| R3-15 | TRUNG BÌNH | sai_buoc_da_lam | `tach_tuyen_bo.py` lấy nhầm số phút điều kiện làm giá trị ở sạc nhanh đồng hồ dạng 2 và bỏ rơi ca kháng nước có/không | `src/kiemchung/tach_tuyen_bo.py:51-73,119-124` |
| R3-16 | TRUNG BÌNH | so_lieu_lech | `ket_qua/bo_thu/thong_ke.md` lệch với cấu hình `dien_thoai.yaml` hiện hành; tệp kết quả B0 lưu trường phụ không tất định | `ket_qua/bo_thu/thong_ke.md:67`, `ket_qua/b0_thu/openai_gpt-oss-120b_luot2.jsonl` |
| R3-17 | THẤP | sai_buoc_da_lam | Bốn script CLI thiếu thiết lập `sys.path` tới `src/` nên chạy trực tiếp bị lỗi `ModuleNotFoundError` | `scripts/thu_llm.py:17`, `scripts/kiem_tra_moi_truong.py:29`, `scripts/sinh_bo_thu.py:26` |
| R3-18 | THẤP | mau_thuan_noi_bo | Đánh dấu tiến độ đầu tệp kế hoạch và trường bước/tuyên bố trong `data/chia_tap.json` mâu thuẫn với trạng thái thực tế | `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:19-36`, `data/chia_tap.json:2,57` |

## Chi tiết

### [R3-01] Câu lệnh B1 và B2 vượt gấp ~2 lần trần 8.000 TPM của Groq Free Tier ở 100% tuyên bố, còn Gemini chạm trần ~20 lượt/ngày
- **Mức độ:** NGHIÊM TRỌNG
- **Loại:** khong_kha_thi
- **Chỗ:** `src/kiemchung/doi_chung/huong_dan.py:27-34`, `src/kiemchung/doi_chung/b1.py:40-44`, `src/kiemchung/doi_chung/b2.py:21-27`, `src/kiemchung/llm.py:150-151`, `ket_qua/thu_llm.md:129-130`, `ket_qua/trich_xuat/llm_calls.jsonl`
- **Bằng chứng:**
  - `src/kiemchung/doi_chung/huong_dan.py:28-31`:
    ```python
    """Giữ nguyên chữ mục 3–7, bỏ phần từ tiểu mục 5.1 đến mục 6."""
    chu = Path(tep).read_text(encoding="utf-8-sig")
    ```
  - `src/kiemchung/llm.py:150-151`:
    ```python
    if status in (413, 429):
        return LLMError("temporary_api_error", retryable=True, status_code=status, retry_after=_retry_after(exc))
    ```
  - Tự đo bằng Python trong bộ nhớ trên dữ liệu thật: `huong_dan_cho_cau_lenh()` dài `35.915` ký tự (`vi_du_b2` thêm `2.251` ký tự), trái với T12.2 (`CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:2411`: `"T4.2–T4.5 và tóm tắt tệp cấu hình"`). Khi ghép câu lệnh thật cho `thu.jsonl` (66 câu) và `chinh.jsonl` (42 câu): câu lệnh B1 dài `37.526–49.906` ký tự; B2 dài `40.552–46.351` ký tự trên `thu` và `40.771–48.720` ký tự trên `chinh`. Nhân hệ số quy đổi thực nghiệm `0,3751` token/ký tự (tính từ trung bình `usage.input_tokens / len(cau_lenh)` của 66 lượt Groq thật trong `thu_openai_gpt-oss-120b_k5_am_tiet.jsonl`), riêng đầu vào của một yêu cầu B1 chiếm khoảng `14.077–18.721` token (`66/66 > 8.000`) và B2 chiếm khoảng `15.211–18.276` token (`66/66` ở `thu`, `42/42` ở `chinh` đều `> 8.000`). Trong khi đó, hạn mức gói Free của Groq cho `openai/gpt-oss-120b` là `8.000` TPM (`ket_qua/thu_llm.md:130`). Ngay với câu lệnh P ngắn hơn gần 3 lần (`11.333–19.378` ký tự), `ket_qua/trich_xuat/llm_calls.jsonl` ngày `17/11/2026` đã ghi `10` lần lỗi HTTP `413` (`request_too_large_for_tier`) trên 12 tuyên bố của `chinh.jsonl` (`tb-00073`..`tb-00107`).
- **Vì sao là vấn đề:** Vừa là lỗi cài đặt lệch đặc tả T12.2 (chèn nguyên văn 35.915 ký tự hướng dẫn thay vì bản tóm tắt), vừa là bất khả thi về tài nguyên kế hoạch nếu giữ tầng miễn phí: với P (`~4.250–6.400` token vào), lỗi 413 xảy ra khi hai lượt gọi rơi vào cùng một phút nên chờ 20–40 giây có thể qua; nhưng với B1 và B2 (`~14.000–18.700` token vào), **một yêu cầu đơn lẻ đã vượt gấp 1,8–2,3 lần tổng ngân sách 8.000 TPM của cả phút**, nên dù `llm.py` chờ bao lâu Groq Free Tier vẫn trả HTTP 413 và làm dừng toàn bộ script ngay ở tuyên bố đầu tiên. Phía `gemini-3.6-flash` miễn phí chỉ đạt `~20` lượt/ngày (`luan_van/nhat_ky.md:155-156`, khoảng 40–50 ngày mới chạy hết thực nghiệm).
- **Đề xuất sửa:** Rút gọn phần hướng dẫn đưa vào câu lệnh B1/B2 đúng tinh thần T12.2–T12.3 (chỉ giữ T4.2–T4.5 và bảng điều kiện của đúng nhóm sản phẩm đang xét như cách P làm ở `bang_thuoc_tinh`), đồng thời bắt buộc nâng cấp lên gói trả phí theo token (Pay-as-you-go) trước Bước 28–30.
- **Độ chắc:** cao

### [R3-02] Bất đối xứng khi xử lý lỗi LLM: B0–B2 bị phạt nhãn `LOI`, còn P biến lỗi LLM thành `CHUA_DU` và hưởng điểm khống
- **Mức độ:** NGHIÊM TRỌNG
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `src/kiemchung/quyet_dinh.py:716-718`, `src/kiemchung/trich_xuat.py:697-707`, `src/kiemchung/doi_chung/b0.py:82,169-173`, `src/kiemchung/doi_chung/chung.py:18,58-62`, `src/kiemchung/doi_chung/b1.py:47-54`, `src/kiemchung/danh_gia.py:21,85-92`
- **Bằng chứng:**
  - `src/kiemchung/quyet_dinh.py:716-718`:
    ```python
    if (ban_ghi.get("loi") or not tb or tb.get("thuoc_tinh") is None or tb.get("gia_tri") is None
            or tb["thuoc_tinh"] not in cau_hinh["thuoc_tinh"]):
        return _ket_qua(cau_hinh, CHUA_DU, "D1a", None, (), ["chua_xac_dinh=trich_xuat_that_bai"],
    ```
  - `src/kiemchung/doi_chung/chung.py:60-61` và `src/kiemchung/danh_gia.py:88`:
    ```python
    else:
        kq.update(nhan="LOI", nhan_goc=None, doan=[], ly_do=None)
    ```
    ```python
    fn = sum(1 for h, c in cap if h == x and c != x)
    ```
  - Kiểm tra chuỗi xử lý: khi LLM trả về rỗng, bị chặn hoặc bị cắt cụt ở cả trần gấp đôi (`empty_blocked_or_incomplete_response`, `json_validate_failed`) hoặc JSON sai cú pháp, B0/B1/B2 xuất `nhan = "LOI"`. Trong `danh_gia.py`, `"LOI"` là nhãn dự đoán thứ 5 luôn khác cả 4 nhãn chuẩn, nên làm tăng `fn` ở mọi lớp và tăng cột `so_loi`. Ngược lại, khi LLM của P gặp đúng lỗi đó (`ban_ghi["loi"] != None`), `quyet_dinh.py` biến thành `nhan = "CHUA_DU"` (`so_loi` của P luôn bằng `0`). Ngoài ra, `b1.py:48-53` vẫn ép chạy B1 khi bản ghi trích xuất của P bị lỗi (`tuyen_bo=None, bang_chung=[]`), khiến B1 chỉ nhận hai chữ `null` và `[]` mà không có văn bản tuyên bố.
- **Vì sao là vấn đề:** Vi phạm nghiêm trọng quy tắc công bằng đối chứng T6.2: mọi lần LLM bị cắt token suy luận (rất phổ biến ở `gemini-3.6-flash`, ghi nhận 19 lần ở `luan_van/nhat_ky.md:150`) đều giúp P được tính là dự đoán đúng (`tp`) nếu nhãn chuẩn là `CHUA_DU`, làm tăng giả tạo F1 lớp `CHUA_DU` và `Macro-F1` của P trong khi dìm điểm B0–B2. Hội đồng phản biện sẽ bác tính hợp lệ của bảng so sánh nếu phát hiện P không bao giờ có `LOI` nhờ gán mặc định thành một trong bốn nhãn chuẩn.
- **Đề xuất sửa:** Tách bạch hai trường hợp ở A1 của `quyet_dinh.py`: nếu `ban_ghi.get("loi")` khác `None` (lỗi kỹ thuật của LLM/JSON) thì `p.py` phải trả `nhan = "LOI"` giống hệt B0–B2 (và B1 cũng ghi `LOI` thay vì gọi LLM trên đầu vào `null`); chỉ khi LLM trả JSON hợp lệ nhưng tuyên bố không trích được giá trị/thuộc tính mới xử lý theo luật nghiệp vụ.
- **Độ chắc:** cao

### [R3-03] Lỗi khớp cụm có ngoặc trong YAML, cắt mất tiêu đề cột bảng so sánh và `vung_do` một dòng làm Recall Đúng của P tụt còn 41,2%
- **Mức độ:** NGHIÊM TRỌNG
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `data/cau_hinh/dien_thoai.yaml:209,212,219,284`, `data/cau_hinh/dong_ho.yaml:110,113`, `data/cau_hinh/tai_nghe.yaml:83,86`, `src/kiemchung/trich_xuat.py:369-406,428-453`, `src/kiemchung/quyet_dinh.py:755-768`, `data/nguon/tn-samsung-buds3pro/doan.jsonl` (`#039`–`#042`)
- **Bằng chứng:**
  - `data/cau_hinh/dien_thoai.yaml:218-220`:
    ```yaml
    ngoai_troi:
      tu_tai_lieu: ["(ngoài trời)"]
      hieu_biet_chung: ["dưới nắng", "ngoài nắng", "ánh nắng", "dưới ánh nắng"]
    ```
  - `src/kiemchung/trich_xuat.py:436-439`:
    ```python
    def dong(d, c):
        a = nguon.rfind("\n", 0, d) + 1
        b = nguon.find("\n", c)
    ```
  - Chạy `p.kiem_chung_ban_ghi` trong bộ nhớ trên toàn bộ 66 bản ghi trích xuất thật của Bước 22 (`ket_qua/trich_xuat/thu_openai_gpt-oss-120b_k5_am_tiet.jsonl`) và đối chiếu tổng hợp với `data/nhan/thu_luot2.jsonl` (34 Đúng, 18 Lệch, 6 Sai, 8 Chưa đủ): P dự đoán `34 CHUA_DU` (`19 D1a`, `12 D1b`, `2 D1`, `1 D6`), `18 LECH`, `14 DUNG`, `0 SAI`. Tuy `FAR = 0/32 (0,0%)`, **Recall nhãn Đúng chỉ đạt `14/34 (41,2%)`** (`18/34` tuyên bố chuẩn `DUNG` bị đẩy nhầm sang `CHUA_DU`), `F1_SAI = 0,0%` (`0/6`), `F1_CHUA_DU = 23,8%`, `Macro-F1 = 35,8%` (thấp hơn cả bản bỏ đối chiếu `P−ĐK` đạt `37,5%`). Bốn lỗi cài đặt trực tiếp gây ra hiện tượng này:
    1. **Cụm cấu hình bọc dấu ngoặc đơn hoặc quá dài:** `dien_thoai.yaml:209,212,219,284` khai báo `"(tiêu chuẩn)"`, `"(HDR)"`, `"(ngoài trời)"`, `"(thông thường)"`, `"(typ)"`; `dong_ho.yaml:110,113` khai báo `"(GPS)"`, `"(GPS + Cellular)"`; `tai_nghe.yaml:83,86` chỉ có `"Tính năng ANC Bật/Tắt"` mà thiếu `"ANC Bật"`, `"ANC Tắt"`. Do câu lệnh `trich_xuat.py:57` yêu cầu chép cụm `"ngắn nhất mà vẫn đủ nghĩa"`, LLM trích `"ngoài trời"`, `"HDR"`, `"tiêu chuẩn"`, `"ANC Bật"` (24 lần), `"ANC Tắt"` (24 lần) không kèm ngoặc; `_mau_cum` đòi ký tự ngoặc nên không khớp, đẩy `93/507` (`18,3%`) mục tài liệu và `12/66` tuyên bố vào `dieu_kien_khac`. Kiểm chứng trên đầu vào tự dựng `"Màn hình iPhone 17 đạt độ sáng 3000 nit khi ở dưới nắng."` với đoạn `dt-apple-iphone17#005`: cả `hieu_dieu_kien` lẫn `_bo_sung_dieu_kien` (bị `bo_sung_mo_ho` vì 3 chế độ nằm chung một dòng) đều thất bại, `quyet_dinh` trả **`CHUA_DU` (`D1a`)** thay vì **`DUNG` (`D3`)**.
    2. **Chia đoạn làm đứt tiêu đề cột của bảng so sánh 3 sản phẩm:** ở `tn-samsung-buds3pro#039`, cuối đoạn có tiêu đề 3 cột `Buds3 Pro / Buds3 / Buds FE`, nhưng các dòng thông số bị cắt sang `#041` (`IP57`, `IPX2`) và `#042` (`7,0/30`, `6,0/26`, `6,0/30`, `5/24`, `8,5/30`, `6,0/21 giờ`) không còn tên sản phẩm. LLM trích cả thông số của Buds3 (`5/24 giờ`) và Buds FE (`8,5/30`, `6,0/21 giờ`, `IPX2`) với `san_pham: null`, cộng thêm `"ANC Tắt"` không khớp bị gán mặc định `bat`, tạo ra `10/12` ca **`D1b` (tài liệu mâu thuẫn giả)**.
    3. **`vung_do` chỉ dò đúng 1 dòng đơn** chứa câu trích: làm `148` trường điều kiện bị loại vì `cum_khong_trong_trich` (tiêu đề nhóm `"Thời Gian Phát"` nằm ở dòng trên còn `trich` chỉ chép dòng số `"Đến 7,0/30 giờ"`, hoặc LLM rút `"Sạc lên đến 50%"` thành `"sạc 50%"`) và `28` trường bị `bo_sung_mo_ho`.
    4. **Từ chỉ bộ phận hiển nhiên/tiêu đề mục lọt vào `dieu_kien_khac`:** `"màn hình"` (3 lần ở tuyên bố `do_sang`/`tan_so_quet`), `"Kháng Bụi & Nước"`, `"Kháng nước"` (9 lần ở tài liệu) chưa có trong `cum_khong_phai_dieu_kien`, bị chặn ở `D1a`.
- **Vì sao là vấn đề:** Giả thuyết chính H1 (`CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:2156`, `scripts/danh_gia_he.py:40,254`) đòi hỏi Recall nhãn Đúng của P không thấp hơn đối chứng cao nhất quá `5` điểm phần trăm (`>= 92,1%` trên bộ thử khi B0 đạt `97,1%`). Mức `41,2%` hiện tại làm H1 thất bại hoàn toàn ngay trên dữ liệu phát triển và khiến tính năng trên CopyPro báo "Chưa đủ thông tin" cho hơn một nửa số câu quảng cáo hợp lệ.
- **Đề xuất sửa:** (1) Bỏ dấu ngoặc khỏi các cụm trong YAML (hoặc thêm dạng không ngoặc `"tiêu chuẩn"`, `"HDR"`, `"ngoài trời"`, `"GPS"`, `"ANC Bật"`, `"ANC Tắt"`) và bổ sung từ hiển nhiên (`"màn hình"`, `"Kháng nước"`, `"Kháng Bụi & Nước"`) vào `cum_khong_phai_dieu_kien`; (2) khi `_bo_sung_dieu_kien` hoặc `hieu_dieu_kien` đã nhận diện được điều kiện từ một dòng, loại cụm con tương ứng khỏi `dieu_kien_khac`; (3) gắn lại ngữ cảnh tiêu đề bảng so sánh khi chia đoạn (hoặc đánh dấu bảng so sánh nhiều cột trong `chia_doan.py`).
- **Độ chắc:** cao

### [R3-04] Khối lượng còn thiếu trước Mốc 3 (27/11) không khả thi; Bước 32 bất khả thi toán học về khoảng cách gán lại mù ≥ 10 ngày
- **Mức độ:** NGHIÊM TRỌNG
- **Loại:** khong_kha_thi
- **Chỗ:** `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:45-57,765-767,804-889,2146`, `data/chia_tap.json:57`
- **Bằng chứng:**
  - `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:848` và `2146`:
    ```markdown
    - [ ] **Gán lại mù** 20% số tuyên bố đã chọn ở Bước 26, ẩn nhãn cũ. Lần gán đầu xong muộn nhất ngày 13/11 (tập kiểm tra), nên từ 24/11 mọi tuyên bố đã cách lần gán đầu ít nhất 10 ngày.
    ```
  - `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:806`:
    ```markdown
    - [ ] **B3:** cài gói `semviqa`; chạy các mô hình ba nhãn đã huấn luyện của SemViQA [7] trên cặp tuyên bố và bằng chứng.
    ```
  - Kiểm kê toàn bộ kho mã và thư mục `data/`, `ket_qua/` tại ngày `18/11/2026` (còn `9` ngày tới Mốc 3 ngày `27/11/2026`):
    1. **Dữ liệu & độ tin cậy nhãn chưa làm:** `64` bài quảng cáo tập kiểm tra trong `data/quang_cao/` chưa tách tuyên bố tay (`0` tuyên bố kiểm tra, ước tính ~`176` câu theo trung bình bộ thử), chưa gán nhãn lần đầu (Bước 23–24, ước tính `~15–20` giờ gán tay theo trung vị/trung bình Lượt 1 ở `thong_ke.md`), chưa tạo và gán nhãn `100–120` biến thể cặp tối thiểu (Bước 25, `0` dòng `ct-`), chưa gán mù Lượt 3 cho 30 câu bộ thử và chưa kiểm bao phủ trên 3 sản phẩm ngoài mẫu (Bước 16). Vì hôm nay đã là `18/11`, dù hoàn tất Bước 24 ngay trong ngày `18/11` thì `18/11 + 10 ngày = 28/11 > 27/11`, **không thể thỏa điều kiện cách tối thiểu 10 ngày trước Mốc 3**.
    2. **Mã nguồn & thực nghiệm phát triển còn thiếu:** chưa có tệp `src/kiemchung/doi_chung/b3.py` cho SemViQA (thuộc phần lõi bắt buộc không được bỏ theo T9.2 dòng `2346`, ước tính cần 1–2 ngày cài đặt, kiểm nhãn và chạy trên Colab vì máy không có GPU rời); chưa có mã và dữ liệu gán tay 7 trường cho 50 tuyên bố phát triển (Bước 28 dòng `766`); chưa chạy trích xuất Bước 22 cho 42 câu `chinh.jsonl`; chưa chạy thật Bước 29 (tách tự động), Bước 30 (B0–B3 trên toàn tập phát triển) và Bước 31 (`P−ĐK`, `P−NN` trên toàn tập phát triển).
- **Vì sao là vấn đề:** Tổng khối lượng công việc thủ công và thực nghiệm còn lại trước `27/11` ước tính tối thiểu `45–60` giờ làm việc ròng (chưa tính thời gian chờ API và sửa lỗi R3-01..R3-08), cộng thêm rào cản cứng 10 ngày chờ gán lại mù. Giữ nguyên lịch Mốc 3 ngày `27/11` chắc chắn dẫn tới vỡ mốc hoặc làm ẩu nhãn chuẩn tập kiểm tra.
- **Đề xuất sửa:** Áp dụng ngay quy tắc T9.2 và xin CBHD dời Mốc 3 khoảng 5–7 ngày (sang `02–04/12`, nén phần mở rộng Bước 43 đã gắn cờ ⭐): ưu tiên hoàn thành tách & gán nhãn tập kiểm tra (Bước 23–24) ngay lập tức để bắt đầu đếm mốc chờ gán lại mù, sau đó trong thời gian chờ mới sửa lỗi P, cài `b3.py` trên Colab và tạo tập cặp tối thiểu.
- **Độ chắc:** cao

### [R3-05] Đổi đơn vị giờ ↔ phút làm đảo chiều thuận lợi ở `dong_ho.sac_nhanh` và hỏng điều kiện số khác đơn vị trái Hướng dẫn 6.2–6.3
- **Mức độ:** NGHIÊM TRỌNG
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `src/kiemchung/quyet_dinh.py:81-84,189-190`, `src/kiemchung/trich_xuat.py:293,329,381,392`, đối chiếu `data/huong_dan_gan_nhan.md:255-262` (mục 6.2, 6.3)
- **Bằng chứng:**
  - `src/kiemchung/quyet_dinh.py:81-84` và `189-190`:
    ```python
    if self.tt["don_vi"] == "phut_hoac_gio":   # đặc tả mục 2.4
        self.dang = {"phut": 1, "gio": 2}.get(self.tb.get("don_vi"))
        if self.huong == "theo_dang":
            self.huong = "thap_hon_tot_hon" if self.dang == 1 else "cao_hon_tot_hon"
    ```
    ```python
    if bc.dang is not None:
        ds = [u for u in ds if u.get("don_vi") == bc.tb.get("don_vi")]
    ```
  - `src/kiemchung/trich_xuat.py:293`:
    ```python
    ung = [g for g in tim_gia_tri(gop, chung) if g.don_vi == don_vi]
    ```
  - Kiểm chứng thực thi 3 đầu vào cụ thể (chạy qua `trich_xuat.xu_ly` + `quyet_dinh.quyet_dinh`):
    1. Tài liệu `dh-apple-watchse3#019` ghi `"Sạc lên đến 80% trong khoảng 45 phút"` và `"Sạc 15 phút cho thời gian sử dụng lên đến 8 giờ"`. Đầu vào `"Apple Watch SE 3 sạc 15 phút dùng được 90 phút."` (`90 phút = 1,5 giờ <= 8 giờ`, nhãn đúng theo HD 6.2 là **`DUNG` (`D3`)**): do `don_vi == "phut"`, mã xếp nhầm vào `dang = 1` (`thap_hon_tot_hon`), lọc bỏ mục bằng chứng `8 giờ`, đòi `moc_phan_tram` và trả sai thành **`CHUA_DU` (`D1a`)**.
    2. Cùng tài liệu trên, đầu vào `"Apple Watch SE 3 sạc lên đến 80% trong 0,75 giờ."` (`0,75 giờ = 45 phút`, nhãn đúng: **`DUNG` (`D3`)**): do `don_vi == "gio"`, mã xếp nhầm vào `dang = 2` (**đảo chiều thuận lợi thành `cao_hon_tot_hon`**), lọc bỏ mục bằng chứng `45 phút`, đòi `so_phut_sac` và trả sai thành **`CHUA_DU` (`D1a`)** (kể cả khi tuyên bố phóng đại `"sạc 80% trong 0,5 giờ"` lẽ ra phải là **`SAI` (`D5`)** cũng trả `CHUA_DU`).
    3. Tài liệu `dt-apple-iphone17#007` ghi `"chống nước ở độ sâu tối đa 6 mét trong vòng tối đa 30 phút"`. Đầu vào đúng nguyên văn ví dụ mục 6.3 của Hướng dẫn (`data/huong_dan_gan_nhan.md:261`): `"iPhone 17 đạt chuẩn IP68, chống nước ở độ sâu 6 mét trong 1 giờ."` (nhãn đúng theo HD 6.3: **`LECH` (`D4`)**): vì `thoi_gian_ngam` khai báo `don_vi: phut`, cả `_so_dieu_kien` lẫn `dieu_kien_so_theo_don_vi` không quy đổi `"1 giờ"` sang `60 phút`, đẩy `"1 giờ"` vào `dieu_kien_khac` và trả sai thành **`CHUA_DU` (`D1a`)**.
- **Vì sao là vấn đề:** Vi phạm trực tiếp quy tắc đổi đơn vị giờ ↔ phút ở mục 6.2 và ví dụ chuẩn mục 6.3 của hướng dẫn gán nhãn; đặc biệt nguy hiểm ở nhóm đồng hồ vì làm đảo ngược hoàn toàn chiều so sánh thuận lợi (`thap_hon_tot_hon` ↔ `cao_hon_tot_hon`).
- **Đề xuất sửa:** Xác định `dang` của `dong_ho.sac_nhanh` dựa trên điều kiện đi kèm (`moc_phan_tram` -> dạng 1; `so_phut_sac` -> dạng 2) thay vì đơn vị của giá trị, cho phép quy đổi `gio` ↔ `phut` trong `cung_thuoc_tinh`, và gọi `quy_doi` trong `_so_dieu_kien` / `dieu_kien_so_theo_don_vi` khi gặp đơn vị tương thích.
- **Độ chắc:** cao

### [R3-06] Luật tự cài `lan_dieu_kien` ghi đè sai điều kiện khi hai chế độ trùng con số và phát tán `dieu_kien_khac` sang đoạn sạch
- **Mức độ:** CAO
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `src/kiemchung/quyet_dinh.py:276-317`
- **Bằng chứng:**
  - `src/kiemchung/quyet_dinh.py:284-288` và `310-315`:
    ```python
    for u in ds:
        for g in nhom:
            if bang(u, g[0], bc):
                g.append(u)
    ```
    ```python
    if cum:
        for u in g:
            ...
            u.setdefault("dieu_kien_khac", []).append(dict(m))
    ```
  - Luật này không có trong mã giả T5.5 hay hướng dẫn gán nhãn (được thêm lúc cài để cứu V23, V27), nhưng gom nhóm chỉ bằng `bang(u, g[0], bc)` mà bỏ qua sự xung đột ở các điều kiện khác của `u`. Kiểm chứng thực thi 2 đầu vào cho nhãn sai:
    1. Đoạn 1 có `6,0 giờ` với `che_do_chong_on="bat", bo_phan="tai_nghe"` (không nêu `hoat_dong`, tức mặc định `nghe_nhac`); Đoạn 2 có `6,0 giờ` với `che_do_chong_on="tat", bo_phan="tai_nghe", hoat_dong="dam_thoai"`. Vì cùng giá trị `6,0`, `lan_dieu_kien` chép `hoat_dong="dam_thoai"` đè vào Đoạn 1, khiến tuyên bố `"Galaxy Buds3 Pro nghe nhạc 6 giờ khi bật chống ồn."` (nhãn đúng: **`DUNG` (`D3`)**) bị phán sai thành **`LECH` (`D4`, `doi_dieu_kien`)**.
    2. Đoạn `#038` có `IP57` sạch đủ điều kiện; Đoạn `#039` có `IP57` kèm tiêu đề `"Kháng nước"` trong `dieu_kien_khac`. `lan_dieu_kien` chép `"Kháng nước"` sang `#038`, làm tuyên bố `"Galaxy Buds3 Pro đạt chuẩn kháng nước IP57."` (nhãn đúng: **`DUNG` (`D3`)**) bị phán sai thành **`CHUA_DU` (`D1a`)** (đã xảy ra thật 3 lần trên bộ thử Bước 22).
- **Vì sao là vấn đề:** Hai chế độ khác nhau vô tình có cùng con số (ví dụ nghe nhạc bật ANC = 6 giờ, đàm thoại tắt ANC = 6 giờ) hoặc một đoạn giới thiệu tóm tắt có cụm lạ sẽ làm hỏng các đoạn bảng thông số đầy đủ, gây lỗi hệ thống cho cả nhãn `DUNG` và `LECH`.
- **Đề xuất sửa:** Chỉ cho phép `lan_dieu_kien` giữa hai mục khi không có bất kỳ điều kiện đã biết nào khác nhau giữa chúng, và không phát tán `dieu_kien_khac` sang một mục khác vốn đã trích được tập điều kiện bắt buộc đầy đủ từ đoạn riêng của nó.
- **Độ chắc:** cao

### [R3-07] `b1.py` cắt bỏ trường sản phẩm và hãng khỏi đầu vào của B1 và cấp trần token đầu ra thấp bằng một nửa P
- **Mức độ:** CAO
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `src/kiemchung/doi_chung/b1.py:27-44`, `src/kiemchung/doi_chung/b0.py:38`, `src/kiemchung/doi_chung/chung.py:7`, `src/kiemchung/trich_xuat.py:122`, đối chiếu `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:1870-1873,2094,2109` (T5.1, T6.1, T6.2)
- **Bằng chứng:**
  - `src/kiemchung/doi_chung/b1.py:29-30`:
    ```python
    giu = {"ma_doan", "thuoc_tinh", "gia_tri", "don_vi", "dieu_kien", "kieu_gia_tri",
           "cum_kieu", "dieu_kien_khac", "ngu_canh", "trich"}
    ```
  - `src/kiemchung/doi_chung/b0.py:38` so với `src/kiemchung/trich_xuat.py:122`:
    ```python
    MAX_TOKEN_RA = 4096
    ```
    ```python
    MAX_TOKEN_RA = 8192   # đầu ra dài hơn B0 (mục 3, ghi chú)
    ```
  - Đối chiếu T5.1 và Bước 30 (`line 804`: `"B1: LLM nhận đúng bộ thông số đã trích của P"`): `bo_thong_so_cho_b1` bỏ mất `san_pham_ma`, `khac_san_pham`, `goi_muc_cao`, `xung_dot`, đồng thời `CAU_LENH_B1` không cho B1 biết `ma_mau`, tên sản phẩm cần kiểm chứng hay tên hãng. Ngoài ra, B0/B1/B2 dùng `MAX_TOKEN_RA = 4096` (nâng trần `8192`), chỉ bằng một nửa của P (`8192`, nâng trần `16384`).
- **Vì sao là vấn đề:** Làm lệch phép so sánh CH2/H2 (`P` so với `B1`, vốn là thí nghiệm then chốt để chứng minh tính mới của bộ quyết định theo T1.5 và T11 câu 2–3): (1) khi tuyên bố nói về sản phẩm khác cùng dòng (như V16 `"iPhone 17 Pro"` trên trang `iPhone 17`), P bắt được nhờ `san_pham_ma`/`chu_tuyen_bo`, còn B1 bị tước hoàn toàn thông tin sản phẩm nên không thể phát hiện; (2) khi tuyên bố dùng chữ gọi mức cao theo hãng (như `"đỉnh"` của Apple so với Xiaomi ở HD 6.5) và `bang_chung` rỗng hoặc không lộ hãng, B1 không biết sản phẩm thuộc hãng nào; (3) với mô hình suy luận tính cả `reasoning_tokens` vào `max_output_tokens`, câu lệnh B1/B2 phức tạp hơn nhưng chỉ có nửa ngân sách token ra của P nên dễ bị cắt cụt thành `LOI` hơn.
- **Đề xuất sửa:** Dùng chung hàm `bay_truong` (`trich_xuat.py:657`) kèm tên mẫu/hãng sản phẩm đang kiểm chứng và `dieu_kien_khac`/`goi_muc_cao` cho B1; đặt cùng `MAX_TOKEN_RA = 8192` cho cả P và B0–B2 theo đúng T6.2 quy tắc 2 (`"cùng cấu hình"`).
- **Độ chắc:** cao

### [R3-08] Lỗi biên ở `_khang_dinh`, `doc_so` với khoảng giá trị và phép so sánh số thực bất đối xứng gây FAR và phụ thuộc thứ tự đoạn
- **Mức độ:** CAO
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `src/kiemchung/chuan_hoa.py:64-66,220-222,274-302`, `src/kiemchung/cau_hinh.py:170-180`, `src/kiemchung/quyet_dinh.py:143-149`
- **Bằng chứng:**
  - `src/kiemchung/cau_hinh.py:173` so với `src/kiemchung/chuan_hoa.py:222`:
    ```python
    bang = abs(gia_tri_tuyen_bo - gia_tri_tai_lieu) <= nguong_bang * abs(gia_tri_tai_lieu)
    ```
    ```python
    return abs(a - b) <= nguong * abs(b) + 1e-12
    ```
  - `src/kiemchung/chuan_hoa.py:287-296`:
    ```python
    tu_gia = rf"(?:\s+[^\W\d_]+){{0,{SO_TOI_DA_TU_GIUA}}}"
    ...
    m = re.search(_mau_cum(cum) + r"[\s:]*\Z", truoc)
    ```
  - Kiểm chứng thực thi 3 nhóm đầu vào cụ thể:
    1. **Từ khẳng định bị bỏ sót -> `DUNG` nhầm (tăng FAR):** với tài liệu `"Thời gian xem video: Lên đến 30 giờ"`, tuyên bố `"iPhone 17 đảm bảo thời lượng xem video 30 giờ."` (`4` từ giữa `"đảm bảo"` và `"30"`, vượt `SO_TOI_DA_TU_GIUA = 2`) và `"iPhone 17 xem video kéo dài hơn khoảng 25 giờ."` (`1` từ `"khoảng"` xen sau `"hơn"`, `tu_muc_san` cho phép `0` từ) đều trả `KieuGiaTri(kieu='khong_neu')`, nên `quyet_dinh` bỏ qua `D2` và gán sai thành **`DUNG` (`D3`)** thay vì **`LECH` (`D2`, `doi_kieu_gia_tri`)** theo Hướng dẫn mục 6.2.
    2. **Khoảng giá trị bị xóa thành lỗi trích xuất:** `doc_so` không xử lý khoảng số gạch nối; với tuyên bố `"Màn hình iPhone 17 có tần số quét 1-120Hz."` khi LLM trích `chu="1-120"`, `neo_nguon` loại `gia_tri` (`so_khong_khop`), làm `quyet_dinh` trả **`CHUA_DU` (`D1a`)** thay vì **`DUNG` (`D3`)** (hoặc với `"1-144Hz"` trả `CHUA_DU` thay vì **`SAI` (`D5`)**).
    3. **Sai số dấu phẩy động và bất đối xứng `bang_nhau`:** `thoa_dieu_kien_so("tuyen_bo_nho_hon_hoac_bang", 30.3, 30.0, 0.01)` trả **`False`** (trong khi `bang_nhau(30.3, 30.0, 0.01)` trả **`True`**) vì `30.3 - 30.0 = 0.3000000000000007 > 0.3`. Ngoài ra `bang_nhau(99.0, 100.0, 0.01)` là `True` nhưng `bang_nhau(100.0, 99.0, 0.01)` là `False`; do đó cùng tuyên bố `"Sạc có dây 100W"`, nếu `bang_chung = [100W, 99W]` thì `gia_tri_khac_nhau` có 1 phần tử và trả **`DUNG` (`D3`)**, nhưng chỉ đảo thứ tự đoạn thành `[99W, 100W]` thì `gia_tri_khac_nhau` thành 2 phần tử và trả **`CHUA_DU` (`D1b`)**.
- **Vì sao là vấn đề:** Gây lỗi chấp nhận nhầm (tăng trực tiếp FAR — chỉ số chính của khóa luận) với các câu quảng cáo có cụm danh từ dài sau `"đảm bảo"`/`"cam kết"`/`"luôn"`, và làm kết quả kiểm chứng phụ thuộc thứ tự xếp hạng đoạn của BM25.
- **Đề xuất sửa:** Thống nhất một hàm `bang_nhau` đối xứng (dùng `max(abs(a), abs(b))` kèm `+ 1e-12`) khi gom nhóm giữa hai mục tài liệu; dùng lại `bang_nhau` trong `thoa_dieu_kien_so`; nới cửa sổ từ giữa từ khẳng định và con số trong cùng một mệnh đề không có dấu câu/con số khác; tách đầu mút cực trị cho khoảng giá trị dạng `a-b`.
- **Độ chắc:** cao

### [R3-09] Pytest hiện hỏng 2 test, bỏ qua 1 test do `.venv` thiếu gói so với `requirements.txt`, và có 0 test tích hợp `xu_ly` + `quyet_dinh`
- **Mức độ:** CAO
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `tests/test_llm.py:57-72`, `tests/test_thu_llm.py:45-52`, `tests/test_bao_cao_ket_qua.py:330-332`, `requirements.txt:1,12-14`, `tests/du_lieu/vi_du_huong_dan.json:484-555`
- **Bằng chứng:**
  - Chạy `.venv\Scripts\python.exe -m pytest -q` (và chạy lại `tests/test_llm.py` sau thay đổi cây làm việc): có **`2` test hỏng (`FAILED`), `1` test bị bỏ qua (`SKIPPED`), `1.364` test đạt**:
    1. `FAILED tests/test_llm.py::test_cache_survives_new_process` (dòng 71): `ModuleNotFoundError: No module named 'kiemchung'`.
    2. `FAILED tests/test_thu_llm.py::test_cli_offline_and_live_preflight` (dòng 51): `ModuleNotFoundError: No module named 'kiemchung'`.
    3. `SKIPPED tests/test_bao_cao_ket_qua.py:331`: `could not import 'matplotlib': No module named 'matplotlib'`.
  - Kiểm tra `importlib.metadata` trong `.venv` đối chiếu `requirements.txt:1` (`# Versions verified in .venv on Python 3.14.4 (2026-10-13)` — ghi từ máy Ubuntu cũ theo `ket_qua/thu_llm/environment.json:4-22`): ba gói `statsmodels==0.15.0`, `pandas==3.0.6`, `matplotlib==3.11.2` và chính gói nội bộ `kltn-kiemchung` **chưa được cài trong `.venv` hiện tại**.
  - Quét toàn bộ `37` tệp `tests/test_*.py`: `test_trich_xuat.py` chỉ kiểm `xu_ly`, còn `test_quyet_dinh.py` chỉ kiểm `quyet_dinh` trên các bản ghi điền tay sẵn mã điều kiện trong `tests/du_lieu/vi_du_huong_dan.json` (ví dụ `V05` dòng `485, 511, 537` gán cứng `"che_do_hien_thi": "tieu_chuan"`, `"hdr"`, `"ngoai_troi"` và `"dieu_kien_khac": []`); **`0` tệp test nào kiểm tra đầu–cuối từ `trich_xuat.xu_ly` sang `quyet_dinh.quyet_dinh` trên 51 ví dụ V01–V51**.
- **Vì sao là vấn đề:** Việc tách rời hoàn toàn dữ liệu giả của `test_quyet_dinh.py` khỏi đầu ra thật của `trich_xuat.xu_ly` tạo cảm giác an toàn giả (`51/51` ví dụ hướng dẫn đều xanh trong pytest), nhưng khi ghép hai khối lại trên dữ liệu thật (phát hiện `R3-03`) thì hàng loạt ca tương đương `V05`, `V06`, `V31` đều gãy. Đồng thời môi trường `.venv` không khớp `requirements.txt` làm hỏng khả năng tái lập và vẽ hình Bước 37.
- **Đề xuất sửa:** Cài đủ các gói trong `requirements.txt` và `pip install -e .` vào `.venv`; truyền `PYTHONPATH=src` trong subprocess của test; bổ sung bộ kiểm thử tích hợp cho V01–V51 đi từ đầu ra JSON thô qua `trich_xuat.xu_ly` rồi mới vào `quyet_dinh.quyet_dinh`.
- **Độ chắc:** cao

### [R3-10] Dữ liệu phát triển và bộ nhớ đệm LLM bị phân mảnh; `data/nhan/thu.jsonl` vẫn giữ nguyên bản nhãn Lượt 1 lỗi thời
- **Mức độ:** CAO
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `data/nhan/thu.jsonl`, `data/nhan/thu_luot2.jsonl`, `scripts/do_recall.py:67`, `scripts/chay_b0.py:218-221`, `scripts/chay_trich_xuat.py:201`, `scripts/gop_thong_ke_trich_xuat.py:7`, `scripts/danh_gia_he.py:66-67,448-450`
- **Bằng chứng:**
  - `scripts/chay_trich_xuat.py:201` so với `scripts/chay_b0.py:220`:
    ```python
    ap.add_argument("--bo-nho-dem", type=Path, default=THU_MUC_RA / "llm_cache")
    ```
    ```python
    ap.add_argument("--bo-nho-dem", type=Path, default=GOC / "ket_qua" / "llm_cache",
    ```
  - Kiểm tra mã băm SHA-256 bằng Python: `data/nhan/thu.jsonl` có mã băm `6a746332af1e...` (24 Đúng, 15 Lệch, 23 Chưa đủ, 4 Sai), **trùng từng byte với `data/nhan/thu_luot1.jsonl`** (nhãn Lượt 1 cũ trước Bước 16), khác hoàn toàn nhãn chuẩn hiện hành `data/nhan/thu_luot2.jsonl` (`7414b17f23d3...`, 34 Đúng, 18 Lệch, 8 Chưa đủ, 6 Sai); thế nhưng mặc định `--nhan` của `scripts/do_recall.py:67` và `scripts/chay_b0.py:218` vẫn trỏ vào `data/nhan/thu.jsonl`.
  - Tập phát triển 108 tuyên bố hiện nằm rời ở hai cặp tệp (`thu.jsonl` 66 câu + `chinh.jsonl` 42 câu), `scripts/gop_thong_ke_trich_xuat.py:7` ghi rõ `"Không ghi tệp jsonl gộp"`, còn `scripts/danh_gia_he.py:66-67,448-450` chỉ nhận 1 tệp `--nhan`, 1 tệp `--tuyen-bo` và báo lỗi `ValueError` nếu khai báo cùng một hệ hai lần.
- **Vì sao là vấn đề:** (1) Chạy `do_recall.py` hoặc `chay_b0.py` không truyền cờ `--nhan` sẽ âm thầm đo trên nhãn Lượt 1 đã bỏ; (2) không thể chạy `danh_gia_he.py` cho toàn bộ tập phát triển 108 tuyên bố (nếu chạy trên `chinh.jsonl` sẽ mất hết 66 câu bộ thử, trong đó mất 100% mẫu tai nghe phát triển `tn-samsung-buds3pro`); (3) tách riêng `ket_qua/trich_xuat/llm_cache` và `ket_qua/llm_cache` trái quy tắc T6.2 dòng `2109` (`"chung bộ nhớ đệm"`) và làm vỡ thiết kế đọc một tệp `llm_calls.jsonl` ở Bước 37.
- **Đề xuất sửa:** Cập nhật hoặc thay thế `data/nhan/thu.jsonl` bằng bản nhãn chuẩn đã chốt sau Lượt 3, tạo tệp/tham số đọc nhiều tệp JSONL trong `danh_gia_he.py` (hoặc xuất tệp gộp phát triển 108 câu), và trỏ mọi script về chung một thư mục `ket_qua/llm_cache` + `ket_qua/llm_calls.jsonl`.
- **Độ chắc:** cao

### [R3-11] Bước 2 chưa có lượt gọi LLM thật nào; mô hình duy nhất chạy xong Bước 15 và 22 trùng với LLM sinh quảng cáo
- **Mức độ:** CAO
- **Loại:** rui_ro_hoi_dong
- **Chỗ:** `ket_qua/thu_llm.md:4-6,168-172`, `scripts/sinh_bo_thu.py:31`, `src/kiemchung/doi_chung/b0.py:33`, `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:2112,2366`
- **Bằng chứng:**
  - `ket_qua/thu_llm.md:169-170`:
    ```markdown
    Cả 3 model bị chặn bởi `missing_api_key` và `free_tier_not_confirmed`; **0
    yêu cầu API thật**, không phát sinh chi phí từ việc gọi LLM.
    ```
  - Đối chiếu T10 điểm 9 (`line 2366`: chọn LLM cho P và B0–B2 `"trong số các LLM đã thử ở Bước 2"`): thực tế Bước 2 chưa từng chạy live (`metrics=null` cho cả 3 ứng viên), và ứng viên `openai/gpt-oss-20b` đã bị bỏ khỏi `NHA_CUNG_CAP` (`b0.py:33`) không qua đối chiếu số liệu. Hiện tại do `gemini-3.6-flash` kẹt hạn mức ngày (`45` lượt thành công trong `ket_qua/trich_xuat/llm_calls.jsonl`), chỉ có `openai/gpt-oss-120b` hoàn tất B0 và trích xuất bộ thử — trùng khít với một trong hai mô hình sinh quảng cáo (`groq-gpt-oss-120b` ở `sinh_bo_thu.py:31`, `sinh_chinh.py:19`).
- **Vì sao là vấn đề:** Hội đồng rất dễ chất vấn hai điểm: (1) vì sao chọn mô hình mà Bước 2 không có số đo thật và loại bỏ `gpt-oss-20b` (vốn nhẹ hơn, đỡ kẹt quota hơn) không có căn cứ; (2) thiên lệch tự đánh giá khi mô hình kiểm chứng trùng với mô hình sinh nửa bộ quảng cáo.
- **Đề xuất sửa:** Chạy bổ sung `scripts/thu_llm.py --mode live` trên 10 câu T4.6 (hoặc đối chiếu trực tiếp hai mô hình trên tập phát triển ở Bước 33 khi có gói trả phí) để có bảng số liệu chọn mô hình minh bạch; đảm bảo báo cáo Bước 33/37 luôn tách kết quả theo `llm_sinh` đúng quy tắc T6.2 dòng `2112`.
- **Độ chắc:** cao

### [R3-12] `src/kiemchung/chia_doan.py` ghi cứng 14 ngoại lệ theo mã đoạn và văn bản của 2 mẫu thuộc tập kiểm tra
- **Mức độ:** CAO
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `src/kiemchung/chia_doan.py:768-798`, đối chiếu `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:1636` (T3.5 quy tắc 4) và `data/chia_tap.json:37,43`
- **Bằng chứng:**
  - `src/kiemchung/chia_doan.py:790-798`:
    ```python
    ("dt-samsung-galaxys25ultra#128", "31 giờ 4,35", "4,35"),  # <sup>4</sup>,<sup>35</sup>, không phải số thập phân
    ("dt-samsung-galaxys25ultra#129", "22 giờ 4,35", "4,35"),
    ```
  - Quét toàn bộ `src/`, `scripts/`, `data/cau_hinh/` theo danh sách 8 mã mẫu của `kiem_tra` trong `data/chia_tap.json` phát hiện `src/kiemchung/chia_doan.py:777-798` ghi cứng `13` mục trong `KY_HIEU_BO_THEM` và `1` mục trong `KY_HIEU_GIU_LAI` cho hai mẫu kiểm tra `dh-samsung-galaxywatch8` và `dt-samsung-galaxys25ultra`.
- **Vì sao là vấn đề:** Dù mục đích chỉ là làm sạch chỉ số chú thích `<sup>` trên tài liệu gốc (không đọc quảng cáo hay nhãn tập kiểm tra), việc có tên mã đoạn tập kiểm tra nằm trong danh sách ngoại lệ viết tay của mã nguồn `src/` vi phạm ranh giới T3.5 quy tắc 4 và tạo điểm yếu để hội đồng nghi ngờ tác giả đã nhìn dữ liệu tập kiểm tra khi tinh chỉnh hệ thống.
- **Đề xuất sửa:** Thay bảng ngoại lệ theo mã đoạn bằng quy tắc tổng quát dựa trên thẻ `<sup>` trong `page.html` của bước chia đoạn (vốn tệp chú thích dòng `765` xác nhận mọi mục này đều có thẻ `<sup>` thật trong `page.html`), để mã không cần nêu tên bất kỳ đoạn nào của tập kiểm tra; đồng thời công khai rõ việc làm sạch chú thích Bước 7 trong mục mối đe dọa tính hợp lệ.
- **Độ chắc:** cao

### [R3-13] `danh_gia_he.py` gộp nhầm hệ tham chiếu B4 vào họ hiệu chỉnh Holm, thiếu 2 phép độ nhạy và thiếu thời gian của P/B1/B2
- **Mức độ:** TRUNG BÌNH
- **Loại:** thieu_can_bo_sung
- **Chỗ:** `scripts/danh_gia_he.py:42,213,327-338`, `src/kiemchung/bao_cao_ket_qua.py:86-105`, `src/kiemchung/trich_xuat.py:701`, `src/kiemchung/doi_chung/chung.py:50-51`, đối chiếu `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:960,970,973,2099`
- **Bằng chứng:**
  - `scripts/danh_gia_he.py:213` và `337-338`:
    ```python
    ho = {t: r["p"] for t, r in ket.items() if t.startswith("B")}
    ```
    ```python
    dong.append({"he": "(toan_bo)", "kich_ban": "chep_nhan", "n": len(tk.ma_co_khoa(nhan_tinh, "chep_nhan")),
                 "ghi_chu": GHI_CHU_CHEP_NHAN})
    ```
  - Kiểm tra mã nguồn đánh giá Bước 37: (1) điều kiện `t.startswith("B")` sẽ gộp cả `B4` vào họ kiểm định Holm nếu truyền `--he B4=...`, trái với T6.1 dòng `2099` (`"B4: Mốc tham chiếu, không kiểm định giả thuyết"`); (2) `do_nhay` chưa cài phép tính lại theo hai mặc định thay thế từ khảo sát Bước 10 (`che_do_nguon = nguon_thap` cho đồng hồ và `loai_zoom = ky_thuat_so`, kế hoạch dòng `973`) cũng như phép tính lại nhãn cho nhóm `chep_nhan` theo mặc định người đọc (dòng `960`); (3) chỉ `b0.py:176` ghi `thoi_gian_sinh_ms`, còn `trich_xuat.py:701` và `chung.py:50-51` bỏ qua `generation_ms`, nên `chi_phi.csv` luôn trả `giay_tb = None` cho P, B1, B2.
- **Vì sao là vấn đề:** Làm sai lệch `p_holm` của H1 khi chạy kèm B4 và làm thiếu các bảng số liệu về thời gian xử lý cũng như độ nhạy đã cam kết trong kế hoạch Bước 37.
- **Đề xuất sửa:** Đổi điều kiện họ Holm thành `t in {"B0", "B1", "B2", "B3"}`; ghi thêm `thoi_gian_sinh_ms=tra_ve.generation_ms` trong `trich_xuat.py` và `chung.py` (kèm tra cứu fallback từ `llm_calls.jsonl` khi đọc cache); bổ sung hàm tính lại cho hai mặc định khảo sát Bước 10.
- **Độ chắc:** cao

### [R3-14] Luật chép đúng nhãn (QĐ15) khớp nhầm nhãn con thiếu điều kiện nhóm và ghi thừa `mac_dinh` cho ca so thẳng (kiểu V12)
- **Mức độ:** TRUNG BÌNH
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `src/kiemchung/quyet_dinh.py:322-375,526-554`, đối chiếu `data/huong_dan_gan_nhan.md:313-321` và `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:1891`
- **Bằng chứng:**
  - `src/kiemchung/quyet_dinh.py:358-360` và `551-553`:
    ```python
    n = nhan_muc(u, bc)
    if n and chua_cum(chu, n):
        ung.append((len(n.split()), len(n), n, u))
    ```
    ```python
    else:
        dk.dat(c, h, "mac_dinh")
        mac_dinh.append(c)
    ```
  - Hai sai lệch so với đặc tả: (1) `nhan_muc` chỉ cắt nhãn từ chuỗi `u["trich"]["gia_tri"]`, trong khi `u["dieu_kien"]` có thể chứa thêm điều kiện lấy từ tiêu đề nhóm hoặc chú thích (ví dụ mục có `trich.gia_tri = "Thời gian phát nhạc: Lên đến 7"` nằm dưới tiêu đề nhóm `"tắt ANC"`, nên `n = "phát nhạc"`). Nếu tuyên bố viết `"Tai nghe phát nhạc 7 giờ"` (thiếu `"tắt ANC"`), `chua_cum` vẫn khớp `"phát nhạc"` và dòng `372` chép luôn `che_do_chong_on = "tat"` cho tuyên bố, biến câu `LECH` (`bo_dieu_kien`) thành `DUNG` trái điều kiện 2 của QĐ15; (2) khi `so_thang(cung_tt, bc) == True` (ví dụ `V12` trong `tests/du_lieu/vi_du_huong_dan.json`: đồng hồ chỉ có một giá trị độ sáng `1000 nit` không kèm điều kiện), dòng `553` vẫn ghi `"mac_dinh=che_do_hien_thi"` vào `ghi_chu`, khiến kịch bản độ nhạy `doi_mac_dinh` đổi nhầm cả ca so thẳng thành `CHUA_DU`.
- **Vì sao là vấn đề:** Có thể làm tăng FAR ở các bảng thông số chia dòng tiêu đề nhóm tách khỏi dòng con số, và làm phóng đại sai số trong phân tích độ nhạy `doi_mac_dinh`.
- **Đề xuất sửa:** Trong `chep_nhan`, chỉ cho phép áp dụng khi mọi điều kiện trong `u["dieu_kien"]` đều thực sự xuất hiện bằng chữ trong `u["trich"]["gia_tri"]` (tức đã nằm trong nhãn được đối chiếu với tuyên bố); khi `thang == True`, bỏ qua việc ghi `mac_dinh` cho các điều kiện không xuất hiện ở tài liệu.
- **Độ chắc:** cao

### [R3-15] `tach_tuyen_bo.py` lấy nhầm số phút điều kiện làm giá trị ở sạc nhanh đồng hồ dạng 2 và bỏ rơi ca kháng nước có/không
- **Mức độ:** TRUNG BÌNH
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `src/kiemchung/tach_tuyen_bo.py:51-73,119-124`, đối chiếu `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:786,1663` (Bước 29, T4.1)
- **Bằng chứng:**
  - `src/kiemchung/tach_tuyen_bo.py:69-72`:
    ```python
    dv = "phut" if dv == "phut_hoac_gio" else dv
    for gt in tim_gia_tri(chu, chung):
        if gt.don_vi == dv or {gt.don_vi, dv} == {"gio", "phut"}:
            return {"gia_tri": quy_doi(gt.so, gt.don_vi, dv), "don_vi": dv}
    ```
  - Kiểm tra logic ghép cặp chấm điểm tách tự động (`ghep`): (1) với tuyên bố sạc nhanh đồng hồ dạng 2 như `"Apple Watch SE 3 sạc 15 phút dùng được 8 giờ"`, `tim_gia_tri` trả `15 phút` trước `8 giờ`, nên hàm lấy nhầm điều kiện `15 phút` làm giá trị của tuyên bố (thay vì `8 giờ = 480 phút`); (2) với tuyên bố kháng nước khẳng định/phủ định không kèm mã số như `"Hộp sạc Galaxy Buds3 Pro không có khả năng kháng nước"` (thuộc phạm vi giữ lại theo T4.1 dòng `1663`), `doc_gia_tri_tuyen_bo` trả `None`, và `_bang(None, None)` ở dòng `120` trả `False`, khiến tách tự động dù tách đúng nguyên văn câu đó vẫn luôn bị chấm là cả False Positive lẫn False Negative.
- **Vì sao là vấn đề:** Làm sai lệch chỉ số Precision và Recall của khối tách tuyên bố tự động ở Bước 29 và Bước 37.
- **Đề xuất sửa:** Với tuyên bố `khang_nuoc` không có mã IP/ISO/số mét, nhận diện giá trị `"co"`/`"khong"` giống `neo_nguon.doc_gia_tri`; với câu có nhiều cụm thời gian ở `sac_nhanh`, loại cụm đi liền từ khóa điều kiện (`"sạc N phút"`) trước khi chọn giá trị chính (hoặc lấy cụm thời gian ứng với kết quả sử dụng).
- **Độ chắc:** cao

### [R3-16] `ket_qua/bo_thu/thong_ke.md` lệch với cấu hình `dien_thoai.yaml` hiện hành; tệp kết quả B0 lưu trường phụ không tất định
- **Mức độ:** TRUNG BÌNH
- **Loại:** so_lieu_lech
- **Chỗ:** `ket_qua/bo_thu/thong_ke.md:67`, `data/cau_hinh/dien_thoai.yaml:131`, `ket_qua/b0_thu/openai_gpt-oss-120b.jsonl`, `ket_qua/b0_thu/openai_gpt-oss-120b_luot2.jsonl`, `scripts/chay_b0.py:181-189`
- **Bằng chứng:**
  - Chạy lại hàm `tao_bao_cao(*tai_du_lieu())` của `scripts/thong_ke_bo_thu.py` trong bộ nhớ và so từng dòng với `ket_qua/bo_thu/thong_ke.md`: lệch ở dòng `67` — tệp đã lưu ghi `| Điện thoại | khang_nuoc | do_sau, thoi_gian_ngam, loai_nuoc, hoat_dong_bi_cam | có | 4 |`, còn cấu hình hiện hành có thêm điều kiện thứ 5 là `chenh_lech_nhiet_do` (thêm ở Bước 22, `dien_thoai.yaml:131`).
  - So hai tệp `ket_qua/b0_thu/openai_gpt-oss-120b.jsonl` và `openai_gpt-oss-120b_luot2.jsonl`: có `61/66` dòng khác nhau ở trường `tu_bo_nho_dem` (`false` đổi thành `true` khi chạy lại qua cache) vì `scripts/chay_b0.py` không loại bỏ cờ `tu_bo_nho_dem` khi ghi tệp như `scripts/chay_trich_xuat.py` đã làm.
- **Vì sao là vấn đề:** Chạy lại script thống kê không khớp từng dòng với báo cáo đã lưu trong `ket_qua/`, và chạy lại `chay_b0.py` tạo diff không cần thiết trên Git dù nhãn không đổi.
- **Đề xuất sửa:** Chạy lại `thong_ke_bo_thu.py` sau khi chốt cấu hình ở Bước 33, và bỏ trường động `tu_bo_nho_dem` khỏi bản ghi JSONL của `chay_b0.py` (giống `chay_trich_xuat.py` và `chay_doi_chung.py`) để đầu ra tái lập giống từng byte.
- **Độ chắc:** cao

### [R3-17] Bốn script CLI thiếu thiết lập `sys.path` tới `src/` nên chạy trực tiếp bị lỗi `ModuleNotFoundError`
- **Mức độ:** THẤP
- **Loại:** sai_buoc_da_lam
- **Chỗ:** `scripts/thu_llm.py:17`, `scripts/kiem_tra_moi_truong.py:29`, `scripts/sinh_bo_thu.py:26`, `scripts/sinh_chinh.py:15`
- **Bằng chứng:**
  - `scripts/thu_llm.py:17`:
    ```python
    from kiemchung.llm import KEY_ENV, LLMClient, LLMError, canonical_json, redact, utc_now
    ```
  - Quét toàn bộ `29` tệp trong `scripts/`: trong `13` script có `import kiemchung`, `9` script có `sys.path.insert(0, str(ROOT / "src"))`, còn `4` script trên không có, nên gọi trực tiếp `.venv\Scripts\python.exe scripts/<tên>.py` trên môi trường chưa cài editable sẽ hỏng ngay với `ModuleNotFoundError` (đây cũng là nguyên nhân trực tiếp làm hỏng `tests/test_thu_llm.py:51`).
- **Vì sao là vấn đề:** Gây lỗi khi chạy lại từ dòng lệnh và làm gãy gói tái lập Bước 45 nếu người kiểm tra chỉ tạo `.venv` và cài `requirements.txt`.
- **Đề xuất sửa:** Thêm `sys.path.insert(0, str(ROOT / "src"))` đồng nhất ở đầu cả 4 script và ghi rõ `pip install -e .` trong hướng dẫn cài đặt.
- **Độ chắc:** cao

### [R3-18] Đánh dấu tiến độ đầu tệp kế hoạch và trường bước/tuyên bố trong `data/chia_tap.json` mâu thuẫn với trạng thái thực tế
- **Mức độ:** THẤP
- **Loại:** mau_thuan_noi_bo
- **Chỗ:** `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:19-36`, `data/chia_tap.json:2,57`
- **Bằng chứng:**
  - `data/chia_tap.json:2,57`:
    ```json
    "buoc": 26,
    "tuyen_bo": "Danh sách mã tuyên bố theo tập ghi sau khi tách tay xong cả hai tập (Bước 19, 23)."
    ```
  - Đầu tệp `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md:19-36` vẫn để `[ ]` cho Bước 1, 5, 6, 7, 8, 9, 10, 11, 12 dù toàn bộ tệp đầu ra của các bước này đã có trong repo và các bước phụ thuộc sau đó (13–15, 17–21, 27) đã đánh dấu `[x]` (trái hướng dẫn dùng file ở dòng `10` và T3.5 quy tắc 8). Ngược lại, `data/chia_tap.json` ghi `"buoc": 26` từ ngày `08/11` khi Bước 23 chưa làm và trường `"tuyen_bo"` vẫn chỉ là câu giữ chỗ.
- **Vì sao là vấn đề:** Gây nhầm lẫn khi tự kiểm tiến độ trước các mốc CBHD (T15) và dễ dẫn tới việc quên điền danh sách mã tuyên bố chính thức vào `data/chia_tap.json` trước khi khóa cấu hình ở Bước 33.
- **Đề xuất sửa:** Đồng bộ lại các ô `[x]` đầu tệp kế hoạch đúng theo tiêu chí "Xong khi" của từng bước và cập nhật danh sách mã tuyên bố thật vào `data/chia_tap.json` ngay khi hoàn tất Bước 23.
- **Độ chắc:** cao

## Nghi vấn chưa kiểm chứng
1. **Khả năng chạy SemViQA (B3) trên phần cứng hiện tại và độ dài đoạn:** Tệp `ket_qua/thu_llm.md:38-42` ghi nhận máy chạy thử trước đây chỉ có CPU i7-4770, RAM khả dụng ~3,95 GiB và không có GPU NVIDIA, trong khi 4 mô hình SemViQA (`tc-xlmr-*`, `tc-infoxlm-*`) dựa trên XLM-RoBERTa / InfoXLM có giới hạn 512 subword tokens. Với top-5 đoạn tài liệu dài (có câu lệnh B0 lên tới `10.331` ký tự trên `chinh.jsonl`), nếu nối cả 5 đoạn vào một cặp `(claim, evidence)` sẽ bị cắt mất phần lớn bằng chứng sau 512 token; nếu tách từng đoạn rồi tổng hợp nhãn thì kế hoạch Bước 30 chưa đặc tả quy tắc gộp nhãn 3 lớp (`Supported` / `Refuted` / `NEI`) từ 5 đoạn rời.
2. **Sự tương thích giữa repo chính và nhánh `kiem-chung-thong-so` bên repo CopyPro:** Nhật ký `08/11/2026` (`luan_van/nhat_ky.md:172`) ghi Bước 40 đã làm sớm ở repo CopyPro bên ngoài, nhưng phạm vi chỉ đọc trong workspace này không có mã nguồn CopyPro nên chưa kiểm chứng được liệu hợp đồng JSON thực tế của `specVerificationService.js` có khớp hoàn toàn với `POST /kiem-chung` trong `src/kiemchung/api.py` hay không.
3. **Tỷ lệ lỗi cắt cụt của `gemini-3.6-flash` ở B1 và B2:** Trên trích xuất P (`max_output_tokens = 8192` nâng trần `16384`), `ket_qua/trich_xuat/llm_calls.jsonl` đã ghi `22` lần `empty_blocked_or_incomplete_response` trên chỉ `45` lần thành công của Gemini. Với B1/B2 chỉ có trần `4096` (nâng trần `8192`) và câu lệnh dài hơn gấp 3 lần, tỷ lệ cắt cụt rất có thể còn cao hơn nhiều nhưng chưa kiểm được vì cấm gọi API.

## Đã kiểm, không thấy vấn đề
- **Số liệu báo cáo đã công bố khớp 100% với dữ liệu thô:** Tự viết mã tính lại độc lập từ tệp thô cho thấy toàn bộ con số trong `ket_qua/recall_buoc14.md` (Recall@1/3/5/8 âm tiết & từ trên mẫu số 56 của Lượt 1), `ket_qua/recall_luot2.md` (trên mẫu số 64 của Lượt 2: âm tiết `96,9% / 98,4% / 100,0% / 100,0%`; từ `100,0%` mọi k), `ket_qua/b0_buoc15.md` (`FAR = 33/41 = 80,5%`, `Recall Đúng = 22/23 = 95,7%`), `ket_qua/b0_luot2.md` (`FAR = 24/32 = 75,0%`, `Recall Đúng = 33/34 = 97,1%`, cùng bảng nhầm lẫn 4×4) và `ket_qua/trich_xuat/thong_ke_thu_openai_gpt-oss-120b_k5_am_tiet.md` (`509` mục tài liệu, giữ `507`, loại `2`; `148` `cum_khong_trong_trich`, `14` `kieu_khong_gan_so`, `13` `trich_khong_co_trong_nguon`; `66/66` khớp thuộc tính tách tay) đều trùng khít từng ô.
- **Tính toàn vẹn cache của các kết quả đã chạy:** `66/66` mã băm `ma_yeu_cau` của `ket_qua/b0_thu/openai_gpt-oss-120b_luot2.jsonl` đều có tệp tương ứng trong `ket_qua/llm_cache/`; `66/66` mã băm của `thu_openai_gpt-oss-120b_k5_am_tiet.jsonl` đều có tệp tương ứng trong `ket_qua/trich_xuat/llm_cache/`.
- **Không rò rỉ nhãn chuẩn vào mã nguồn phương pháp và đối chứng:** Đã quét toàn bộ `src/kiemchung/` (`p.py`, `trich_xuat.py`, `quyet_dinh.py`, `chuan_hoa.py`, `neo_nguon.py`, `truy_hoi.py`, `ly_do.py`, `api.py`, `doi_chung/*`): không mô-đun nào đọc `data/nhan/`, không có nhánh `if id == ...` ăn gian theo từng tuyên bố phát triển, và phần quy tắc của `data/cau_hinh/*.yaml` không chứa mã mẫu tập kiểm tra (`kiem_cau_hinh` đạt 0 lỗi).
- **Truy hồi BM25 (`truy_hoi.py`) và sinh lý do (`ly_do.py`) bám sát đặc tả T5.2, T5.6:** BM25 cô lập chặt theo đúng `ma_mau` (kiểm cả trường `ma_mau` lẫn tiền tố `<ma_mau>#`), gộp cả `noi_dung` và `chu_thich`, dùng chung hàm `lay_doan` cho P, B0 và B2; `ly_do.py` sinh lý do hoàn toàn tất định theo 8 mẫu câu T5.6 từ dấu vết `vet`, không để LLM viết tự do.
- **Kiểm định thống kê (`thong_ke.py`) cài đúng T6.5:** Bootstrap rút mẫu lặp có hoàn lại đúng theo cụm bài quảng cáo `ma_qc` (biến thể `ct-` quy về cụm của tuyên bố gốc `tb-`), `bootstrap_hieu` dùng chung mẫu cụm trong từng vòng giữa hai hệ, McNemar nhị thức chính xác hai phía và hiệu chỉnh Holm giữ tính đơn điệu đúng công thức.
- **Định dạng và phân chia bài quảng cáo (`data/quang_cao/`, `data/chia_tap.json`):** Đủ `104` tệp JSON bài quảng cáo (`40` bài thuộc 4 mẫu tập phát triển, `64` bài thuộc 8 mẫu tập kiểm tra), tập mẫu phát triển và kiểm tra rời nhau hoàn toàn, mã băm SHA-256 của `data/mau_san_pham.csv` trong `data/chia_tap.json` khớp chính xác.

## Không kiểm được
- **Chất lượng thực tế của B1, B2, B3, tách tự động (Bước 29) và P trên `gemini-3.6-flash` cũng như trên `chinh.jsonl`:** Theo luật cứng không gọi bất kỳ API LLM nào và không cài thêm gói, không thể chạy thử live các hệ chưa có đầu ra trong cache.
- **Trạng thái khóa API và hạn mức thực tế của tài khoản sinh viên:** Theo luật cứng không đọc tệp `.env` và không truy cập mạng ra nhà cung cấp, không xác minh được tài khoản đã thu hồi khóa cũ hay đã bật gói trả phí hay chưa.
- **Độ hợp lý của nhãn chuẩn trên từng tuyên bố cụ thể của bộ thử và nội dung tập kiểm tra:** Tuân thủ tuyệt đối luật giữ tính mù của Lượt 3 (`data/nhan/chon_luot3.txt`) và luật niêm phong tập kiểm tra, báo cáo này không đối chiếu hay bình luận đáp án nhãn chuẩn của bất kỳ tuyên bố bộ thử cá lẻ nào và không mở nội dung bài quảng cáo tập kiểm tra để phân tích quy tắc.
- **Tích hợp thực tế bên phía repo CopyPro và ảnh Docker chạy thật:** Không có repo CopyPro và Docker daemon trong phạm vi rà soát chỉ đọc hiện tại.
