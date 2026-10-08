# Đặc tả A–B–C sau rà soát 08/10/2026

Đây là **đặc tả để triển khai**, không phải báo cáo đã chạy pipeline B0/B1/P. Các ví dụ và nhãn trong hồ sơ là ca minh họa; chưa phải kết quả dự đoán của chương trình.

## 1. Phạm vi và thứ tự

1. A đối chiếu sản phẩm, phiên bản, thị trường/hiệu lực nguồn, bộ phận, thuộc tính và đơn vị. Đổi đơn vị khi cùng đại lượng. Trích `value_kind`, nhưng **không loại nguồn chỉ vì khác loại giá trị**.
2. B đối chiếu điều kiện thiết yếu và phạm vi claim. Thiếu điều kiện cần thiết → `UNKNOWN`; không liên quan → `NOT_APPLICABLE`. Không dùng nguồn ANC bật để kết luận số giờ ANC tắt. Nếu claim nói rõ theo thông số/phép thử hãng, giữ `condition_ref` tới đúng chú thích; không tự thêm điều kiện vào claim không có tham chiếu đó.
3. C1 tìm xung đột giữa những nguồn cùng phạm vi còn áp dụng. Hai số khác nhau vì khác phiên bản/chế độ/thời điểm hiệu lực không tự tạo xung đột. Chỉ ưu tiên nguồn thay thế khi có căn cứ và quy tắc chốt trước, không chọn nguồn vì thuận claim. Xung đột chưa giải quyết → `NEI/conflict`.
4. C2, nếu không có xung đột đó, đối chiếu kiểu giá trị theo bảng dưới, tạo quan hệ `SUPPORT / CONTRADICT / UNKNOWN` cho từng thuộc tính. Đây là bước bị thiếu trong bản trước.
5. C3: có bác bỏ trực tiếp đối với một phần bắt buộc của claim → `Refuted`; hỗ trợ đầy đủ mọi phần bắt buộc → `Supported`; còn lại → `NEI/missing`. Không dùng bằng chứng bị A/B loại để bác bỏ. Nếu hồ sơ không parse được, ghi lỗi kỹ thuật riêng, không âm thầm coi là NEI hợp lệ.

Phạm vi xung đột phải liên quan tới thuộc tính/điều kiện đang xét; bất đồng về một thông số không liên quan không làm mọi claim của sản phẩm thành NEI.

## 2. Kiểu giá trị và luật C2

Hồ sơ cần `value_kind` (`exact`, `gt`, `ge`, `lt`, `le`, `interval`, `approx`, `version`), `value_role` (`measurement`, `declared_maximum`, `declared_minimum` hoặc `unknown`), đơn vị, biên đóng/mở, độ chính xác nguồn, điều kiện và mã trích dẫn. Số thập phân nên biểu diễn bằng Decimal; phiên bản Bluetooth là chuỗi.

Hai cách hiểu phải tách riêng:

- Mệnh đề về một đại lượng `x`: `x=24`, `x>24`, `x≤3`. Có thể xét miền giá trị.
- Mệnh đề về **mức cực đại hãng công bố** `M`: “thời lượng tối đa công bố là 20 giờ” có `M=20`. Không được biến thành tập `[0,20]` rồi dùng phép bao hàm để hỗ trợ một quảng cáo nâng mức tối đa lên 25 giờ. “Tối đa 20” chỉ được gán vai trò này khi ngữ cảnh rõ đang trích thông số cực đại; nếu thực sự chỉ là một cận trên về `x`, dùng luật miền của `x`. Mơ hồ → `UNKNOWN`.

Các luật sau giả định cùng phạm vi, đơn vị và điều kiện; `S/R/U` lần lượt là hỗ trợ/bác bỏ/chưa đủ.

| Bằng chứng | Claim | Quan hệ |
|---|---|---|
| `x=a` | `x=b` | S nếu a=b; R nếu a≠b |
| `x>a` | `x=b` | R nếu b≤a; U nếu b>a |
| `x≥a` | `x=b` | R nếu b<a; U nếu b≥a |
| `x≤u` (chỉ cận trên) | `x=b` | R nếu b>u; U nếu b≤u |
| `x<u` | `x=b` | R nếu b≥u; U nếu b<u |
| `x>a` | `x>b` | S nếu a≥b; U nếu a<b |
| `x=a` | Mệnh đề khoảng về x | S nếu a thuộc miền claim; R nếu không thuộc |
| Miền nguồn E, miền claim Q về cùng x | Bất đẳng thức/khoảng | S nếu E⊆Q; R nếu E∩Q=∅; U nếu còn giao nhưng không bao hàm |
| Mức tối đa công bố `M=a` | Mức tối đa công bố `M=b` | S nếu a=b; R nếu a≠b |
| Mức tối thiểu công bố `m=a` | Mức tối thiểu công bố `m=b` | S nếu a=b; R nếu a≠b |
| Hãng công bố lên đến u (nên x≤u) | x chính xác b | R nếu b>u; U nếu b≤u; không suy ra luôn đạt u |
| Hãng công bố khoảng a, không có biên sai số | Cùng thông số công bố “khoảng a” | S nếu cùng phạm vi/cách hiểu |
| “Khoảng a” không có biên | Số chính xác/“khoảng b” khác a | U, không tự tạo dung sai |
| “Khoảng a” có biên sai số rõ | Mệnh đề khoảng/số về cùng x | Dùng đúng miền và biên được nguồn cho phép |
| Phiên bản Bluetooth a | Phiên bản Bluetooth b | S nếu cùng chuỗi phiên bản chuẩn hóa; R nếu khác phiên bản xác định |
| Khác vai trò đại lượng mà không có phép suy ra hợp lệ | Bất kỳ | U |

Với miền khoảng, giữ biên mở/đóng: `(24,+∞)` không chứa 24; `[24,+∞)` chứa 24 nhưng không xác nhận `=24`. Khoảng đảo biên hoặc rỗng do trích xuất lỗi là lỗi hồ sơ, không lấy tập rỗng để suy ra mọi claim được hỗ trợ.

Nguồn/claim nêu “luôn”, “mọi chế độ” cần lượng từ/phạm vi riêng. Một phép thử ở một cấu hình không hỗ trợ mọi cấu hình. Bằng chứng cho thấy một trường hợp trái với khẳng định “luôn” có thể bác bỏ; chỉ biết giới hạn tối đa mà không có trường hợp trái thì chưa đủ.

Dung sai mặc định bằng 0 cho thông số chính xác; chỉ đổi khi có sai số/làm tròn có căn cứ trong nguồn, khóa trước val/test. Không tối ưu dung sai theo nhãn. Quy tắc gần đúng không được mở rộng từ cách diễn đạt giống nhau sang khẳng định một số chính xác.

## 3. Ca kiểm tra bắt buộc khi triển khai

| Ca | Bằng chứng / claim | Kết quả mong đợi |
|---|---|---|
| EX-18 | Tổng nghe `>24` / `=24`, cùng phạm vi phép thử | Refuted qua C2 |
| Biên EX-18 | `>24` / `=25` | NEI-thiếu, không mặc định Supported |
| Biên đóng | `≥24` / `=24` | NEI-thiếu, không Refuted |
| EX-20 | Sau sạc 15 phút, “lên đến 3” / “chính xác 3” | NEI-thiếu qua C2 |
| Vượt cận | “lên đến 3” / “chính xác 4” | Refuted nếu cùng điều kiện |
| EX-11 | Mức tối đa công bố 20 / 25, ANC bật | Refuted; không dùng bao hàm khoảng |
| EX-12 | Cùng thông tin “khoảng 1,5 giờ” sau sạc 5 phút | Supported cho câu đã giới hạn vào phép thử |
| EX-10 | Nguồn ANC bật / claim ANC tắt | NEI-thiếu qua B; không gọi là xung đột |
| EX-21 | Hai mức tối đa giả lập 20 và 24, cùng phạm vi | NEI-xung đột, C1 ưu tiên |
| EX-22 | Hai khối lượng hộp giả lập 32 và 34 g | NEI-xung đột |
| EX-23 | Hai phiên bản Bluetooth giả lập 5.2 và 5.3 | NEI-xung đột |

Ba ca cuối có sản phẩm `SIM-*`, do Codex soạn ngày 08/10/2026; không phải thông số hãng và không được tính vào đánh giá chính. Hồ sơ từng câu, hai phía nguồn và nguồn gốc nằm trong [examples.json](../evidence/2026-10-08/examples.json).

## 4. Ablation không tự mâu thuẫn

- `P−A(bộ phận)`: chỉ tắt kiểm tra bộ phận. Vẫn lọc sản phẩm/phiên bản/thị trường/thuộc tính/đơn vị và giữ B, C1–C3. Không gọi đây là bỏ toàn bộ A hoặc bỏ kiểm tra loại giá trị.
- `P−B`: tắt kiểm tra điều kiện và yêu cầu bao phủ chế độ, giữ A và C. Khi B bị tắt, đầu vào C có thể chứa nguồn sai chế độ; đó là tác động cần đo, không sửa C để bù.
- Dùng cùng hồ sơ trích xuất và quy tắc còn lại. Chỉ chạy ablation khi đã chọn ở Gate 4 và đủ thời gian; không phải yêu cầu MVP.
