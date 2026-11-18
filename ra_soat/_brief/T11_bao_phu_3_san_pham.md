# T-11 · Thử độ bao phủ cấu hình trên 3 sản phẩm ngoài 12 mẫu

Người giao: Claude Opus, ngày 18/11/2026. Người làm: Gemini 4 Carbon.

## Bối cảnh

Khóa luận kiểm chứng tuyên bố thông số có điều kiện trong quảng cáo tiếng Việt (điện thoại, tai nghe, đồng hồ). Phương pháp dựa trên tệp cấu hình `data/cau_hinh/dien_thoai.yaml`, `tai_nghe.yaml`, `dong_ho.yaml` (và `chung.yaml`): mỗi thuộc tính khai báo các điều kiện bắt buộc, sáu loại điều kiện, và cách diễn đạt (`cach_dien_dat`: `tu_tai_lieu`, `hieu_biet_chung`) để máy nhận ra cụm điều kiện trong tài liệu của hãng. Điều kiện dạng số khai báo ở `dieu_kien_so` (đơn vị và quan hệ).

Kế hoạch (Bước 16, `CHI_TIET_TUYEN_TINH_KHOA_LUAN.md` dòng 495–504, và `luan_van/phan_tich_dieu_kien_ngoai_cau_hinh.md` mục 7) đặt một điểm dừng: **cấu hình phải nhận ra ít nhất 80% cụm điều kiện quyết định trên 3 sản phẩm ngoài 12 mẫu**; không đạt thì bổ sung luật từ chính 3 trang đó. Bài thử này chưa làm. Ba sản phẩm đã đề xuất ngày 27/10 (`luan_van/nhat_ky.md` dòng 33): **OPPO Reno14** (điện thoại), **OPPO Enco Air5 Pro** (tai nghe), **Galaxy Watch Ultra2** (đồng hồ).

## Việc phải làm

1. Tìm trang thông số **chính hãng tiếng Việt** của 3 sản phẩm (ưu tiên `oppo.com/vn`, `samsung.com/vn`; trang sản phẩm và trang thông số kỹ thuật). Nếu một sản phẩm không có hoặc không mở được trang chính hãng tiếng Việt, chọn sản phẩm thay thế **cùng nhóm, cùng hãng nếu được**, không thuộc 12 mẫu dưới đây, và ghi rõ lý do. Không dùng trang bán lẻ trừ khi không còn cách nào khác (ghi rõ).
2. Với mỗi thuộc tính có trong ba tệp YAML (khóa dưới `thuoc_tinh`), tìm **mọi giá trị** trang công bố cho thuộc tính đó và **mọi cụm điều kiện quyết định** gắn với giá trị. Cụm điều kiện quyết định là cụm làm giá trị thay đổi hoặc giới hạn phạm vi đúng của giá trị: chế độ (bật/tắt chống ồn, chế độ tiết kiệm pin), bộ phận (tai nghe hay hộp sạc), phụ kiện (công suất củ sạc, cáp), điều kiện đo (mốc phần trăm, độ sâu, thời gian ngâm, vùng đo), phiên bản/dung lượng, kiểu giá trị (tối đa, điển hình...). Không tính câu rào chung kiểu "kết quả có thể khác tùy điều kiện sử dụng" (xem `ngu_canh_khong_quyet_dinh` trong `chung.yaml`).
3. Với từng cụm, xét cấu hình có **nhận ra** không: cụm khớp (sau khi bỏ khác biệt hoa/thường, khoảng trắng, ngoặc bao quanh) một cách diễn đạt khai báo cho đúng thuộc tính đó, hoặc là điều kiện số có đơn vị và quan hệ khai báo trong `dieu_kien_so` của thuộc tính. Ghi một trong ba: `nhan_ra`, `khong_nhan_ra`, `khong_ro` (kèm lý do ngắn).
4. Ghi thêm các thuộc tính trang có công bố mà YAML của nhóm đó **chưa khai báo** (ví dụ đồng hồ có dung lượng pin mAh), nhưng không tính vào tỷ lệ.

## Kết quả phải ghi (chỉ hai tệp này, không ghi tệp nào khác)

- `ket_qua/bao_phu/cum_3_san_pham.json`: một mảng JSON, mỗi phần tử: `{"san_pham", "url", "nhom", "thuoc_tinh", "gia_tri", "don_vi", "cum_dieu_kien", "loai_du_kien", "trich", "ket_luan", "khoa_yaml_khop", "ghi_chu"}`. `trich` là câu trích ngắn nguyên văn từ trang, **tối đa 25 chữ**.
- `ket_qua/bao_phu/bao_cao_carbon.md`: tiếng Việt có dấu. Gồm: URL đã dùng và ngày truy cập; bảng số đếm theo sản phẩm và tổng (`nhan_ra / tổng cụm`, %); kết luận đạt hay không đạt ngưỡng 80%; danh sách cụm `khong_nhan_ra` kèm đề xuất thêm vào YAML (khóa điều kiện, cách diễn đạt, thuộc tính); danh sách thuộc tính chưa khai báo; những chỗ bạn không chắc.

## Luật cứng

- Không sửa bất kỳ tệp nào khác trong repo (không sửa YAML, mã, kế hoạch).
- Không đọc dữ liệu của 8 mẫu tập kiểm tra: thư mục `data/nguon/<mã>/`, `data/quang_cao/` của `dt-oppo-findx8`, `dt-samsung-galaxys25ultra`, `dt-xiaomi-redminote14proplus5g`, `tn-apple-airpodspro3`, `tn-apple-airpods4`, `tn-xiaomi-redmibuds6pro`, `dh-samsung-galaxywatch8`, `dh-xiaomi-watchs4`. Bốn mẫu tập phát triển (`dt-apple-iphone17`, `dt-xiaomi-15t`, `tn-samsung-buds3pro`, `dh-apple-watchse3`) thì được đọc nếu cần đối chiếu.
- Không lưu toàn văn trang web vào repo (bản quyền). Chỉ lưu câu trích ngắn trong JSON.
- Không gọi LLM API qua mã của dự án. Không đọc hay in `.env`.
- Không bịa: cụm nào không thấy trên trang thì không ghi. Mỗi phần tử phải có `url` và `trich` thật.

Khi xong, trả lời một dòng: `DA_XONG <số cụm> <tỷ lệ nhận ra>`.
