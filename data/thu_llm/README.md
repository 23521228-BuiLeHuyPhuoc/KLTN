# Bộ câu thử trích xuất cho Bước 2

10 câu nguyên văn từ T4.6: ví dụ 1, 2, 6, 8, 9, 11, 12, 13, 16, 18.
Chỉ có iPhone 17, Galaxy Buds3 Pro, Apple Watch SE 3 và Xiaomi 15T thuộc tập
phát triển dự kiến. Không thu thập quảng cáo, không dùng mẫu tập kiểm tra.

`cases.json` chứa câu và giá trị kỳ vọng được điền từ chính câu trong tài liệu,
trước khi chạy model. Đây là fixture kỹ thuật cho thử trích xuất, **không phải
nhãn chuẩn bốn lớp của bộ dữ liệu nghiên cứu**. Không lấy đầu ra LLM làm đáp án.
Người nghiên cứu nên duyệt các quy ước này trước khi dùng số đo sơ bộ.
Các con số là nội dung ví dụ trong kế hoạch; chưa xác minh lại trang hãng
(việc đó thuộc Bước 5–6).

Bộ thông số theo T5.1: sản phẩm, phiên bản, bộ phận, thuộc tính, giá trị, đơn vị,
điều kiện cùng kiểu giá trị. JSON tách riêng `dieu_kien` và `kieu_gia_tri` theo
ví dụ T5.1; thêm `trich` và `mac_dinh`. Bước thử này chỉ trích thông tin hiện rõ
theo T5.3(a), chưa áp dụng cách hiểu thông thường, kiểm tra/bổ sung điều kiện
hay bộ quyết định A–D. Trường thiếu là null, điều kiện thiếu không xuất hiện,
`mac_dinh=[]`. Không suy ra rằng tên Galaxy Buds3 Pro đã nêu rõ bộ phận tai nghe.

Quy ước cần chú ý:

- Ví dụ 1: giá trị chính là **20 phút**; “lên đến 50%” là mốc sạc trong
  `dieu_kien.moc_sac`, không phải kiểu của thời gian 20 phút. Bộ sạc 40W trở lên
  được ghi riêng. Ví dụ 2 không có bộ sạc: không tự điền 40W.
- Ví dụ 8 không nêu chế độ: không tự điền bật/tắt chống ồn.
- Ví dụ 11 giữ IP57 của **hộp sạc** đúng theo câu đang trích, dù nhãn kiểm chứng
  trong tài liệu là Lệch; đây chưa phải bài toán sửa hay phán xét câu.
- Ví dụ 16 có “cực đại” nhưng không có “25% diện tích”: không tự thêm diện tích.
- Ví dụ 18 trích được “xuyên âm” dù không có số liệu chính hãng cho chế độ này.

Cùng một system prompt, JSON schema trong prompt, JSON mode, temperature=0,
top_p=1 và trần đầu ra 2048 token cho tất cả model. Các API có cơ chế reasoning
và cách tính token khác nhau; đây là thiết lập tương đương, không cam kết lượng
suy luận bằng nhau. Model/revision thực trả về được lưu. Không gọi công cụ tìm
kiếm của model. Model ứng viên trong `models.json` chưa được chốt cho nghiên cứu.

`src/kiemchung/thu_llm.py` kiểm cấu trúc bằng Pydantic, so chính xác 8 trường
chính (điều kiện tính thành một trường), đếm điều kiện thiếu/thừa/sai và trích
dẫn thiếu/không nằm trong câu. Sai schema tính 0 trường đúng. Đây là phép đo
kỹ thuật sơ bộ, nhạy với cách viết đồng nghĩa; cần đọc lỗi từng câu. Trường null
cũng được tính, nên xem kết quả từng trường thay vì chỉ tỷ lệ chung. Kiểm tra
chuỗi trích chỉ là chẩn đoán, không chứng minh câu trích hỗ trợ đúng ý nghĩa.

Chế độ offline trả JSON rỗng cố định, không nhìn đáp án kỳ vọng, để thử đường
đi và cache. `metrics=null`, `mode=offline/mock`: không được dùng làm kết quả
chất lượng, độ trễ hoặc token của LLM thật.
