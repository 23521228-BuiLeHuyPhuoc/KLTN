# Bước 22: thiết kế trích xuất có neo nguồn và kiểm tra đầy đủ

Opus viết ngày 08/11/2026, trước khi cài. Tệp này là đặc tả cho `src/kiemchung/trich_xuat.py`, `src/kiemchung/neo_nguon.py` và là nguồn cho mục trích xuất của Chương 3. Căn cứ: T5.1, T5.3, T5.4, T12.4 của kế hoạch; mục 6.2–6.9 của hướng dẫn gán nhãn bản 2; `chung.yaml` mục `dieu_kien_la`.

## 1. Vị trí trong P

```
tuyên bố (chữ) + mã mẫu
  -> BM25 top-k đoạn của đúng mẫu (cùng hàm với B0)
  -> (a) LLM trích bộ thông số của tuyên bố và của mọi giá trị cùng thuộc tính trong top-k đoạn, mỗi trường kèm câu trích
  -> (b) Python kiểm neo nguồn: câu trích có thật, con số khớp, cụm điều kiện có trong câu trích; trường sai bị bỏ
  -> hiểu điều kiện: cụm điều kiện -> (tên điều kiện, giá trị) theo cach_dien_dat; cụm không khớp -> dieu_kien_khac
  -> (c) Python kiểm tra đầy đủ: dò cụm của cấu hình trong tuyên bố và trong dòng chứa giá trị, điền điều kiện LLM bỏ sót
  -> chuẩn hóa (chuan_hoa.py) -> bộ thông số -> bộ quyết định A–D (Bước 27)
```

Hai nguyên tắc của `chung.yaml dieu_kien_la`: **phát hiện điều kiện theo kiểu mở** (LLM ghi mọi cụm điều kiện, kể cả cụm cấu hình không biết), **hiểu điều kiện theo kiểu đóng** (chỉ cụm có trong cấu hình mới thành điều kiện có mã; cụm còn lại vào `dieu_kien_khac` và dẫn tới D1a, không bao giờ ra Đúng).

## 2. Đầu vào

- P chỉ nhận **chữ tuyên bố** (`tuyen_bo`) và **mã mẫu** (`ma_mau`), như B0. P không đọc `cau_goc`, `thuoc_tinh` tách tay hay nhãn. `thuoc_tinh` tách tay chỉ dùng để đo độ đúng trích xuất ở Bước 28.
- Top-k đoạn lấy bằng đúng hàm của B0 (`lay_doan`, chuyển sang `truy_hoi.py` để dùng chung), nên mọi hệ thống có cùng top-k (T5.2). Mặc định k = 5, tách âm tiết; chọn lại ở Bước 33.
- Văn bản một đoạn là văn bản đánh chỉ mục của `truy_hoi.doc_doan`: `noi_dung` rồi các `chu_thich`, nối bằng dấu xuống dòng. Câu trích của tài liệu so với đúng văn bản này.

## 3. Câu lệnh (bản T12.4 đầu tiên, chốt ở Bước 33)

Mỗi tuyên bố một lần gọi. Câu lệnh là một chuỗi cố định, chỉ thay bốn chỗ trống: `{ten_nhom}`, `{bang_thuoc_tinh}`, `{tuyen_bo}`, `{doan_1..k}`. Thay một lượt như B0 (chữ trong tuyên bố hay đoạn trông giống chỗ trống không bị thay lần nữa). Đoạn ghi dạng `[<mã đoạn>] <văn bản>`, cách nhau một dòng trống, theo hạng BM25 giảm dần. Mã có hằng `CAU_LENH_TRICH_XUAT` chép đúng khối dưới; test so hai bên.

`{bang_thuoc_tinh}`: mỗi thuộc tính của nhóm một dòng `- <mã> (<đơn vị>): <mô tả>`, theo thứ tự trong YAML nhóm. Mô tả lấy đúng chữ của bảng thuộc tính trong `data/tuyen_bo/huong_dan_tach_tay.md` (cột của nhóm), để người tách tay và LLM hiểu thuộc tính như nhau. `{ten_nhom}`: "điện thoại", "tai nghe", "đồng hồ".

<!-- CAU_LENH_TRICH_XUAT: bat_dau -->
```text
Bạn trích thông số kỹ thuật từ một tuyên bố quảng cáo về {ten_nhom} và từ các đoạn tài liệu chính hãng của đúng sản phẩm đó. Chỉ chép những gì có trong văn bản. Không suy đoán, không tính toán, không dùng hiểu biết bên ngoài.

VIỆC CẦN LÀM
1. Tuyên bố: ghi sản phẩm, thuộc tính, giá trị (con số và đơn vị) và mọi cụm điều kiện gắn với con số.
2. Tài liệu: tìm MỌI giá trị của cùng thuộc tính với tuyên bố trong các đoạn, ở mọi điều kiện, kể cả giá trị ở điều kiện khác với tuyên bố và giá trị không bằng con số của tuyên bố. Mỗi giá trị là một mục. Cùng một giá trị lặp ở nhiều đoạn thì mỗi đoạn một mục. Không lấy giá trị của thuộc tính khác.
3. Mỗi trường kèm "trich": đoạn chép NGUYÊN VĂN, từng chữ, từ văn bản tương ứng (chữ của tuyên bố, hoặc đoạn tài liệu có mã ghi ở "ma_doan"). Trích của một giá trị trong tài liệu chép cả dòng chứa con số, gồm nhãn của dòng, ví dụ "Thời gian xem video: Lên đến 30 giờ". Trường không có trong văn bản thì ghi null; không có điều kiện thì ghi danh sách rỗng.

THUỘC TÍNH (chọn đúng một mã cho tuyên bố; mọi mục của tài liệu dùng cùng mã đó)
{bang_thuoc_tinh}
Tuyên bố không thuộc thuộc tính nào ở trên thì ghi "thuoc_tinh": null và "bang_chung": [].

GIÁ TRỊ
- "chu": con số chép như trong văn bản ("3.000", "4,5", "18"), hoặc mã ("IP68", "WR50"). Giá trị phủ định như "không có khả năng kháng nước" thì "chu" là "không".
- "don_vi": đơn vị chép như trong văn bản ("giờ", "tiếng", "phút", "nit", "W", "mAh", "Hz", "x", "m", "%"); dòng không ghi đơn vị thì null. Không đổi đơn vị.
- Con số chỉ là điều kiện (công suất bộ sạc, mốc phần trăm khi sạc, số phút sạc, độ sâu, thời gian ngâm, phần diện tích đo) không phải giá trị; ghi nó trong điều kiện của giá trị.
- Một dòng có hai con số chung một đơn vị, cách nhau bằng "/" (ví dụ "Đến 9 / 30 giờ"), thì ghi hai mục, mỗi mục một con số, cùng "trich" là cả dòng.
- Không cộng, trừ hay nhân để ra con số mới.

ĐIỀU KIỆN
Điều kiện là mọi cụm cho biết con số đạt được trong hoàn cảnh nào. Mỗi cụm xếp vào một trong sáu loại:
- che_do_hoat_dong: chế độ hay hoạt động (bật chống ồn, nghe nhạc, xem video trực tuyến, chế độ nguồn điện thấp, HDR, quay video)
- bo_phan: bộ phận (tai nghe, hộp sạc, tổng thời gian kèm hộp sạc)
- phu_kien: phụ kiện hay cách sạc (bộ sạc 40W trở lên, sạc không dây, cáp đi kèm)
- dieu_kien_do: điều kiện đo hay thử (sạc tới 50%, sạc 15 phút, độ sâu 6 mét, tối đa 30 phút, 25% diện tích, nước ngọt)
- phien_ban: phiên bản (GPS + Cellular, bản 256 GB)
- kieu_gia_tri: chữ chỉ kiểu của con số ("lên đến", "đến", "tối đa", "đỉnh", "điển hình", "định mức", "thích ứng", "luôn", "đảm bảo", "ít nhất", "hơn")
"cum": cụm chép nguyên văn, ngắn nhất mà vẫn đủ nghĩa ("bật chống ồn", "bộ sạc 67W trở lên"). "trich": câu hoặc dòng chứa cụm đó.
Ở tài liệu, ghi MỌI cụm điều kiện gắn với giá trị, kể cả cụm nằm trong chú thích và cụm lạ không giống ví dụ nào ở trên; không bỏ cụm nào. Cụm ở nhãn của dòng hay ở tiêu đề nhóm ngay trên dòng cũng là điều kiện của dòng đó.
Không ghi làm điều kiện: cụm khen không có nội dung đo ("cả ngày", "siêu bền", "vượt trội", "không lo hết pin"), câu rào chung của tài liệu ("kết quả thực tế có thể khác", "thử nghiệm trong phòng thí nghiệm"), chữ chỉ là tên sản phẩm.

SẢN PHẨM
- Tuyên bố có tên sản phẩm thì chép tên đó.
- Ở tài liệu, "san_pham" ghi null khi giá trị là của chính sản phẩm của trang. Chỉ ghi tên khi đoạn cho thấy giá trị thuộc một sản phẩm khác (ví dụ cột khác của bảng so sánh). Không biết chắc giá trị thuộc sản phẩm nào thì không lấy giá trị đó.

ĐẦU RA
Trả về đúng một đối tượng JSON, không thêm chữ nào khác:
{"tuyen_bo": {"san_pham": {"chu": ..., "trich": ...} hoặc null, "thuoc_tinh": ... hoặc null, "gia_tri": {"chu": ..., "don_vi": ..., "trich": ...} hoặc null, "dieu_kien": [{"loai": ..., "cum": ..., "trich": ...}]}, "bang_chung": [{"ma_doan": ..., "san_pham": {"chu": ..., "trich": ...} hoặc null, "gia_tri": {"chu": ..., "don_vi": ..., "trich": ...}, "dieu_kien": [{"loai": ..., "cum": ..., "trich": ...}]}]}

VÍ DỤ 1 (sản phẩm tự đặt)
Tuyên bố: Tai nghe B nghe nhạc lên đến 9 giờ khi tắt chống ồn
Tài liệu:
[tn-b#003] Thời gian phát nhạc
Tắt ANC: Đến 9 / 30 giờ
Bật ANC: Đến 7 / 24 giờ

[tn-b#010] Thời gian đàm thoại (tắt ANC): lên đến 6 giờ
Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ
Kết quả:
{"tuyen_bo": {"san_pham": {"chu": "Tai nghe B", "trich": "Tai nghe B"}, "thuoc_tinh": "thoi_luong_pin", "gia_tri": {"chu": "9", "don_vi": "giờ", "trich": "lên đến 9 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "nghe nhạc", "trich": "nghe nhạc"}, {"loai": "kieu_gia_tri", "cum": "lên đến", "trich": "lên đến 9 giờ"}, {"loai": "che_do_hoat_dong", "cum": "tắt chống ồn", "trich": "khi tắt chống ồn"}]}, "bang_chung": [{"ma_doan": "tn-b#003", "san_pham": null, "gia_tri": {"chu": "9", "don_vi": "giờ", "trich": "Tắt ANC: Đến 9 / 30 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "Thời gian phát nhạc", "trich": "Thời gian phát nhạc"}, {"loai": "che_do_hoat_dong", "cum": "Tắt ANC", "trich": "Tắt ANC: Đến 9 / 30 giờ"}, {"loai": "kieu_gia_tri", "cum": "Đến", "trich": "Tắt ANC: Đến 9 / 30 giờ"}]}, {"ma_doan": "tn-b#003", "san_pham": null, "gia_tri": {"chu": "30", "don_vi": "giờ", "trich": "Tắt ANC: Đến 9 / 30 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "Thời gian phát nhạc", "trich": "Thời gian phát nhạc"}, {"loai": "che_do_hoat_dong", "cum": "Tắt ANC", "trich": "Tắt ANC: Đến 9 / 30 giờ"}, {"loai": "kieu_gia_tri", "cum": "Đến", "trich": "Tắt ANC: Đến 9 / 30 giờ"}]}, {"ma_doan": "tn-b#003", "san_pham": null, "gia_tri": {"chu": "7", "don_vi": "giờ", "trich": "Bật ANC: Đến 7 / 24 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "Thời gian phát nhạc", "trich": "Thời gian phát nhạc"}, {"loai": "che_do_hoat_dong", "cum": "Bật ANC", "trich": "Bật ANC: Đến 7 / 24 giờ"}, {"loai": "kieu_gia_tri", "cum": "Đến", "trich": "Bật ANC: Đến 7 / 24 giờ"}]}, {"ma_doan": "tn-b#003", "san_pham": null, "gia_tri": {"chu": "24", "don_vi": "giờ", "trich": "Bật ANC: Đến 7 / 24 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "Thời gian phát nhạc", "trich": "Thời gian phát nhạc"}, {"loai": "che_do_hoat_dong", "cum": "Bật ANC", "trich": "Bật ANC: Đến 7 / 24 giờ"}, {"loai": "kieu_gia_tri", "cum": "Đến", "trich": "Bật ANC: Đến 7 / 24 giờ"}]}, {"ma_doan": "tn-b#010", "san_pham": null, "gia_tri": {"chu": "6", "don_vi": "giờ", "trich": "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ"}, "dieu_kien": [{"loai": "che_do_hoat_dong", "cum": "đàm thoại", "trich": "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ"}, {"loai": "che_do_hoat_dong", "cum": "tắt ANC", "trich": "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ"}, {"loai": "kieu_gia_tri", "cum": "lên đến", "trich": "Thời gian đàm thoại (tắt ANC): lên đến 6 giờ"}]}, {"ma_doan": "tn-b#010", "san_pham": null, "gia_tri": {"chu": "20", "don_vi": "giờ", "trich": "Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ"}, "dieu_kien": [{"loai": "bo_phan", "cum": "Tổng thời gian đàm thoại kèm hộp sạc", "trich": "Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ"}, {"loai": "che_do_hoat_dong", "cum": "đàm thoại", "trich": "Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ"}, {"loai": "che_do_hoat_dong", "cum": "tắt ANC", "trich": "Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ"}, {"loai": "kieu_gia_tri", "cum": "lên đến", "trich": "Tổng thời gian đàm thoại kèm hộp sạc (tắt ANC): lên đến 20 giờ"}]}]}

VÍ DỤ 2 (sản phẩm tự đặt)
Tuyên bố: Điện thoại A sạc 50% chỉ trong 25 phút với củ sạc 45W
Tài liệu:
[dt-a#007] Sạc nhanh có dây: sạc tới 50% trong khoảng 25 phút với bộ sạc 67W trở lên
Sạc không dây: sạc tới 50% trong 60 phút
Thử nghiệm trong phòng thí nghiệm, kết quả thực tế có thể khác.
Kết quả:
{"tuyen_bo": {"san_pham": {"chu": "Điện thoại A", "trich": "Điện thoại A"}, "thuoc_tinh": "sac_nhanh", "gia_tri": {"chu": "25", "don_vi": "phút", "trich": "trong 25 phút"}, "dieu_kien": [{"loai": "dieu_kien_do", "cum": "sạc 50%", "trich": "sạc 50%"}, {"loai": "phu_kien", "cum": "củ sạc 45W", "trich": "với củ sạc 45W"}]}, "bang_chung": [{"ma_doan": "dt-a#007", "san_pham": null, "gia_tri": {"chu": "25", "don_vi": "phút", "trich": "Sạc nhanh có dây: sạc tới 50% trong khoảng 25 phút với bộ sạc 67W trở lên"}, "dieu_kien": [{"loai": "phu_kien", "cum": "Sạc nhanh có dây", "trich": "Sạc nhanh có dây: sạc tới 50% trong khoảng 25 phút với bộ sạc 67W trở lên"}, {"loai": "dieu_kien_do", "cum": "sạc tới 50%", "trich": "Sạc nhanh có dây: sạc tới 50% trong khoảng 25 phút với bộ sạc 67W trở lên"}, {"loai": "phu_kien", "cum": "bộ sạc 67W trở lên", "trich": "Sạc nhanh có dây: sạc tới 50% trong khoảng 25 phút với bộ sạc 67W trở lên"}]}, {"ma_doan": "dt-a#007", "san_pham": null, "gia_tri": {"chu": "60", "don_vi": "phút", "trich": "Sạc không dây: sạc tới 50% trong 60 phút"}, "dieu_kien": [{"loai": "phu_kien", "cum": "Sạc không dây", "trich": "Sạc không dây: sạc tới 50% trong 60 phút"}, {"loai": "dieu_kien_do", "cum": "sạc tới 50%", "trich": "Sạc không dây: sạc tới 50% trong 60 phút"}]}]}

BÂY GIỜ LÀM VỚI
Tuyên bố: {tuyen_bo}
Tài liệu:
{doan_1..k}
Kết quả:
```
<!-- CAU_LENH_TRICH_XUAT: ket_thuc -->

Ghi chú về câu lệnh:

- Hai ví dụ dùng sản phẩm tự đặt (Tai nghe B, Điện thoại A) như các ví dụ tự đặt của hướng dẫn, để câu lệnh không chứa đáp án của tuyên bố nào trong dữ liệu. Ví dụ 1 có hai dạng khó của tài liệu thật (dòng "a / b giờ" không ghi bộ phận, nhãn dòng chứa điều kiện); ví dụ 2 có con số điều kiện (50%, 67W, 45W), từ nhấn mạnh "chỉ" không phải điều kiện, và câu rào chung không được ghi.
- Ví dụ 1 không ghi bộ phận cho 9 và 30 vì đoạn không có chữ nào nói bộ phận; Python điền theo luật ở mục 6 (cặp số gạch chéo). LLM không được tự suy bộ phận.
- "khoảng" ở ví dụ 2 không được ghi làm điều kiện: chữ chỉ độ gần đúng, không phải hoàn cảnh đo. Chưa có quy tắc nhãn cho "khoảng"; nếu gặp ở tuyên bố thật thì báo ở nhật ký.
- Tham số gọi giống B0 (T6.2): nhiệt độ 0, chế độ JSON, đi qua bộ nhớ đệm của `llm.py`; giới hạn token đầu ra 8.192 vì đầu ra dài hơn B0.

## 4. Đọc đầu ra của LLM

- Chỉ nhận JSON trần hoặc JSON trong một khối ```json (như B0). Không đọc được, không phải đối tượng, thiếu khóa `tuyen_bo` hay `bang_chung` sai kiểu: bản ghi có `loi` nói rõ lý do, không đoán. Phản hồi bị chặn, rỗng, cắt cụt cũng thành `loi`; lỗi mạng, quota, khóa thì ném lên để dừng chạy.
- Mục có kiểu sai (ví dụ `dieu_kien` không phải danh sách, `loai` không thuộc sáu loại) bị bỏ riêng mục đó và ghi vào `bi_loai` với lý do `sai_luoc_do`.

## 5. (b) Neo nguồn

Chuẩn hóa để so chuỗi con (hàm `chuan_so_khop`): NFC, chữ thường, mọi dấu câu và ký hiệu (gồm `/`, `:`, ngoặc, gạch nối các kiểu, dấu nháy) thành khoảng trắng, mọi khoảng trắng (gồm U+202F, U+00A0, xuống dòng) gộp thành một dấu cách, bỏ khoảng trắng đầu cuối. Dấu chấm và phẩy nằm giữa hai chữ số giữ nguyên ("3.000", "4,5"). Nguồn: chữ tuyên bố cho phía tuyên bố; văn bản của đoạn `ma_doan` cho phía tài liệu.

| Trường | Đạt khi | Không đạt |
|---|---|---|
| `ma_doan` | thuộc top-k đã đưa vào câu lệnh | bỏ cả mục, lý do `doan_ngoai_top_k` |
| mọi `trich` | là chuỗi con của nguồn sau chuẩn hóa | bỏ trường đó, lý do `trich_khong_co_trong_nguon` |
| `gia_tri` (số) | `doc_so(chu)` đọc được; trong `trich` có con số bằng nó (`bang_nhau`); nếu `don_vi` khác null thì `chuan_don_vi(don_vi)` đọc được và trong `trich` con số đó đi với đơn vị cùng khóa, hoặc đứng trong dạng "a / b <đơn vị>" | bỏ `gia_tri`, lý do `so_khong_khop` hoặc `don_vi_khong_khop` |
| `gia_tri` (mã) | IP: `tach_ip(chu)` bằng `tach_ip(trich)`; ISO 22810: `doc_iso_22810` hai bên bằng nhau; phủ định: `chu` là "không" và `trich` có "không" cùng "kháng nước" hoặc "chống nước"; khẳng định không kèm mã (V18 "hộp sạc cũng kháng nước"): `chu` là "có" hoặc rỗng, `trich` có "kháng nước" hoặc "chống nước" mà không có "không" đứng trước | bỏ `gia_tri`, lý do `ma_khong_khop` |
| `dieu_kien[i]` | `loai` thuộc sáu loại; `trich` có trong nguồn; `cum` là chuỗi con của `trich` | bỏ điều kiện đó, lý do tương ứng |
| `san_pham` | `trich` có trong nguồn; `chu` là chuỗi con của `trich` | bỏ `san_pham` |
| `thuoc_tinh` (tuyên bố) | thuộc danh sách thuộc tính của nhóm | `null`, lý do `thuoc_tinh_ngoai_nhom` |

Mục tài liệu mất `gia_tri` thì chuyển sang `bang_chung_bi_loai` (vẫn lưu để thống kê), không đưa sang bộ quyết định. Tuyên bố mất `gia_tri` hay `thuoc_tinh` thì bộ quyết định không có gì để so; bản ghi giữ nguyên để Bước 27 xử lý (dự kiến D1a, nguyên nhân `trich_xuat_that_bai`).

Con số của dòng không ghi đơn vị (Buds3 Pro `#044` "Thời gian phát nhạc (bật ANC) Lên đến 6"): đạt khi con số có trong `trich` và `don_vi` là null hoặc là đơn vị của thuộc tính; đơn vị của giá trị lấy theo thuộc tính.

## 6. Hiểu điều kiện (kiểu đóng)

Với mỗi điều kiện còn lại sau neo nguồn, tìm cụm của cấu hình **trong `cum`** (không tìm trong `trich`, vì câu trích của cả dòng có thể chứa điều kiện của con số khác). So bằng `chuan_hoa_chu`, có ranh giới chữ, cụm dài khớp trước. Nơi tìm, theo thứ tự:

1. `ngu_canh_khong_quyet_dinh` của `chung.yaml`: khớp thì ghi vào `ngu_canh`, không là điều kiện.
2. `cach_dien_dat` của nhóm: bỏ giá trị có `phia` không đúng phía đang xét; bỏ giá trị có `chi_thuoc_tinh` không gồm thuộc tính của tuyên bố. Khớp điều kiện thuộc `dieu_kien_bat_buoc` của thuộc tính thì ghi `dieu_kien[<tên>] = <giá trị>`; khớp điều kiện của thuộc tính khác thì ghi vào `dieu_kien_phu` (lưu, không dùng).
   - Điều kiện dạng số (`gia_tri_so`): đọc con số bằng `tim_gia_tri` trong `cum` (rồi trong `trich` nếu `cum` không có số), lấy con số có đơn vị đúng `dieu_kien_so.<tên>.don_vi`; cụm không có số thì tra `gia_tri_ngam` ("sạc đầy" = 100, "toàn màn hình" = 100). Ghi `{"so": …, "don_vi": …}`. Không đọc được số thì điều kiện đó vào `dieu_kien_khac` với lý do `khong_doc_duoc_so`.
3. Kiểu giá trị (`loai` là `kieu_gia_tri`, hoặc cụm khớp `kieu_gia_tri`, `tu_khang_dinh`, `tu_goi_muc_cao` của `chung.yaml`, `kieu_dung_luong` của nhóm): không ghi ở đây; kiểu giá trị do `tim_kieu_gia_tri` quyết ở mục 7 trên chữ của nguồn, để cụm phải đứng liền con số của chính giá trị.
4. `cum_khong_phai_dieu_kien` của `chung.yaml`: `cum` trùng hẳn một mục (sau chuẩn hóa) thì bỏ, ghi vào `bo_qua`.
5. Không khớp gì: ghi vào `dieu_kien_khac` `{loai, cum, trich}`. Đây là điều kiện lạ: ở tài liệu thì giá trị đó dẫn tới D1a khi được khớp (luật chặn của Bước 27); ở tuyên bố thì tuyên bố có điều kiện chưa xác định, dẫn tới D1a.

Một `cum` khớp hai giá trị khác nhau của cùng một điều kiện (ví dụ cả "bật ANC" và "tắt ANC") thì điều kiện đó ghi `xung_dot` với cả hai giá trị; bộ quyết định coi là chưa xác định.

## 7. (c) Kiểm tra đầy đủ

Vùng dò:

- Tuyên bố: toàn bộ chữ tuyên bố.
- Mục tài liệu: các dòng của văn bản đoạn có chứa `trich` của giá trị (mở rộng `trich` tới đầu và cuối dòng; dòng tính theo dấu xuống dòng của văn bản đoạn). Không dò cả đoạn, vì một đoạn có nhiều giá trị ở nhiều điều kiện.

Việc dò:

1. Với mỗi điều kiện bắt buộc của thuộc tính mà mục chưa có: dò cụm của điều kiện đó (đúng phía, đúng `chi_thuoc_tinh`) trong vùng dò. Thấy đúng một giá trị thì điền và ghi `bo_sung` `{phia, dieu_kien, gia_tri, cum}`; thấy hai giá trị khác nhau thì không điền, ghi `bo_sung_mo_ho`. Điều kiện dạng số đọc con số như mục 6.
2. Kiểu giá trị: `tim_gia_tri` và `tim_kieu_gia_tri` của `chuan_hoa.py` được mở rộng cho dạng "a / b <đơn vị>": cả a và b đều là `GiaTri` cùng đơn vị, và cụm kiểu đứng liền trước a ("Đến 7 / 30 giờ") áp cho cả a và b. Tìm `GiaTri` của con số trong vùng dò (con số bằng `gia_tri`, gần vị trí `trich` nhất), gọi `tim_kieu_gia_tri` với `cum_them` là `kieu_dung_luong` của nhóm nếu có. Kết quả ghi `kieu_gia_tri`, `cum_kieu`, `goi_muc_cao`. Kiểu do LLM ghi mà Python không thấy đứng liền con số thì không dùng, ghi vào `bi_loai` lý do `kieu_khong_gan_so`.
3. Cặp số gạch chéo (khóa mới `cap_so_gach_cheo` của thuộc tính trong YAML nhóm, hiện chỉ có `tai_nghe.thoi_luong_pin: [tai_nghe, kem_hop_sac]`): vùng dò có dạng "a / b <đơn vị>" với a < b và mục chưa có `bo_phan` thì số a là `tai_nghe`, số b là `kem_hop_sac`, ghi `bo_sung` với `cum` là chuỗi "a / b <đơn vị>". Căn cứ: Buds3 Pro `#038` ("Đến 7 / 30 giờ", chú thích "tai nghe và hộp tai nghe cung cấp tối đa 30 giờ"), `#042`, cách đọc của hướng dẫn ở các ví dụ V-pin Buds3 Pro ("số 6 trong '6 / 26'" là tai nghe).
4. Sản phẩm của mục tài liệu: `san_pham` null thì là mẫu của trang; có thì `tim_san_pham(chu)`. Ra mẫu khác hoặc `None` thì ghi `khac_san_pham: true` (bộ quyết định bỏ ở bước A). Sản phẩm của tuyên bố: `tim_san_pham` trên chữ tuyên bố, ghi `san_pham_ma`.

Kiểm tra đầy đủ không đổi điều kiện đã có từ LLM sau neo nguồn; chỉ điền chỗ trống. Không dò `dieu_kien_khac` (cụm lạ không có trong cấu hình nên không dò được); chỗ hở này là giới hạn bao phủ, báo ở Bước 37–38.

## 8. Bộ thông số sau cùng

Mỗi mục (tuyên bố hoặc tài liệu) sau ba khâu:

```json
{"ma_doan": "tn-samsung-buds3pro#044", "san_pham_ma": "tn-samsung-buds3pro", "khac_san_pham": false,
 "thuoc_tinh": "thoi_luong_pin", "gia_tri": 6.0, "don_vi": "gio",
 "dieu_kien": {"che_do_chong_on": "bat", "hoat_dong": "nghe_nhac", "bo_phan": "tai_nghe"},
 "kieu_gia_tri": "toi_da", "cum_kieu": "lên đến", "goi_muc_cao": false,
 "dieu_kien_khac": [], "dieu_kien_phu": {}, "ngu_canh": [], "bo_qua": [], "xung_dot": {},
 "trich": {"gia_tri": "Thời gian phát nhạc (bật ANC) Lên đến 6", "dieu_kien.che_do_chong_on": "Thời gian phát nhạc (bật ANC) Lên đến 6"},
 "nguon_dieu_kien": {"che_do_chong_on": "llm", "hoat_dong": "llm", "bo_phan": "bo_sung"}}
```

- `gia_tri`: số thực sau `doc_so`; mã IP là `{"bui": …, "nuoc": …}`; ISO 22810 là số mét với `don_vi` `m`; phủ định là chuỗi `"khong"`, khẳng định không kèm mã là `"co"` (bổ sung 08/11 trong lúc cài). `don_vi` là khóa của `chuan_hoa.don_vi`.
- Bảy trường của T5.1: sản phẩm (`san_pham_ma`), phiên bản (`dieu_kien.phien_ban`), bộ phận (`dieu_kien.bo_phan`), thuộc tính, giá trị, đơn vị, điều kiện cùng kiểu giá trị (phần còn lại của `dieu_kien` và `kieu_gia_tri`). Hàm `bay_truong(muc)` trả đúng dạng T5.1 để in và để đo độ đúng ở Bước 28.
- `mac_dinh` không ghi ở bước này: cách hiểu mặc định là việc của bước B trong bộ quyết định (Bước 27), vì cần biết tài liệu có những điều kiện nào.

Bản ghi của một tuyên bố: `{"id", "ma_mau", "mo_hinh", "k", "cach_tach", "doan": [mã], "tuyen_bo": <mục>, "bang_chung": [<mục>], "bang_chung_bi_loai": [...], "bi_loai": [{"phia", "chi_so", "truong", "ly_do"}], "bo_sung": [...], "loi": null, "neo_nguon": true, "kiem_day_du": true}`.

## 9. Cờ cho bản bỏ thành phần

`trich_xuat(..., neo_nguon=True, kiem_day_du=True)`. P−NN (Bước 31) gọi với cả hai bằng False: không bỏ trường nào ở khâu (b), không điền gì ở khâu (c). Khâu hiểu điều kiện (mục 6) vẫn chạy, vì bộ quyết định cần mã điều kiện; giá trị lấy thẳng `doc_so(chu)`, kiểu giá trị lấy theo cụm `kieu_gia_tri` LLM ghi (map qua cấu hình) thay cho `tim_kieu_gia_tri`. Cùng một đầu ra LLM (cùng bộ nhớ đệm) cho P và P−NN, nên khác biệt chỉ do hai khâu kiểm.

## 10. (d) Thống kê

`scripts/chay_trich_xuat.py` ghi `ket_qua/trich_xuat/<tên>.jsonl` và `ket_qua/trich_xuat/thong_ke_<tên>.md`: số tuyên bố, số lỗi LLM, số mục tài liệu (giữ, bị loại), số trường bị loại theo lý do và theo phía, số điều kiện bổ sung theo tên điều kiện, số tuyên bố và số mục tài liệu có `dieu_kien_khac` (kèm danh sách cụm), số mục `khac_san_pham`, tỉ lệ `thuoc_tinh` trích khớp `thuoc_tinh` tách tay (chỉ để tham khảo, đo chính thức ở Bước 28).

## 11. Kiểm thử (LLM giả)

Neo nguồn: câu trích không có trong nguồn; con số sai (LLM ghi 7, câu trích "6 giờ"); đơn vị sai (LLM ghi phút, câu trích "giờ"); điều kiện bịa (cụm không có trong câu trích); `ma_doan` ngoài top-k; dạng "a / b giờ" cả hai số đều đạt; dòng không có đơn vị; mã IP, WR50, "không có khả năng kháng nước"; khoảng trắng hẹp U+202F.
Hiểu điều kiện: cụm khớp cấu hình; cụm của thuộc tính khác vào `dieu_kien_phu`; cụm ngữ cảnh; cụm lạ còn `dieu_kien_khac` sau neo nguồn (yêu cầu của kế hoạch); `cum_khong_phai_dieu_kien`; `phia`, `chi_thuoc_tinh`; điều kiện dạng số có số, có `gia_tri_ngam`, không đọc được số; xung đột hai giá trị.
Kiểm tra đầy đủ: điều kiện bị bỏ sót được bổ sung (tuyên bố "bật chống ồn" mà LLM không ghi); không dò ra ngoài dòng của giá trị; cặp số gạch chéo; kiểu giá trị chỉ khi đứng liền con số; `khac_san_pham`.
Khác: JSON hỏng; tất định (gọi hai lần cùng kết quả); P−NN không bỏ, không điền; câu lệnh trong mã trùng khối của tệp này.

## 12. Giới hạn đã biết

- Cụm tả hoàn cảnh mà cấu hình chưa có (V51 "dưới nắng" cho chế độ tự tăng sáng của Xiaomi) vẫn thành điều kiện đã biết nhưng sai chế độ (`ngoai_troi`); việc ghép hai chế độ để ở Bước 27 như ghi trong `dien_thoai.yaml`.
- `dt-xiaomi-15t#005` dính chữ "67WHỗ trợ": `tim_gia_tri` không đọc ra 67W, nên giá trị công suất sạc ở đoạn này bị loại ở neo nguồn. Lỗi của chia đoạn, ghi lại, không sửa nguồn.
- Luật chép đúng nhãn (QĐ15) và cách hiểu mặc định thuộc Bước 27, không thuộc bước này.
