# Đặc tả bộ quyết định P (A–B–C1–C2–C3) — bản 10/2026

Đặc tả này hiện thực hóa [hướng dẫn nhãn chung v2](HUONG_DAN_GAN_NHAN.md) thành thuật toán tất định. Khi đặc tả và hướng dẫn khác nhau, **hướng dẫn là chuẩn ngữ nghĩa**; phải sửa đặc tả/code hoặc tăng phiên bản hướng dẫn, không để hai bên lệch nhau. Mã tham chiếu: [`scripts/abc_reference.py`](../scripts/abc_reference.py); kiểm thử: [`tests/test_abc.py`](../tests/test_abc.py).

Trạng thái: mã tham chiếu chạy trên hồ sơ chuẩn hóa nhập tay. Chưa có bước trích xuất tự động, runner hay kết quả B0/B1/P (các module này là công việc W6–W8 trong [sổ tay](KE_HOACH_CHI_TIET_SINH_VIEN.md)). Các nhãn trong fixture là nhãn minh họa, không phải dự đoán của hệ thống.

## 1. Hợp đồng đầu vào/đầu ra

Đầu vào của `verdict(claim, evidences, policy='inherit_headline', ablate=())`:

- `claim`: `product`, `version`, `market` (null nếu claim không nêu), `part`, `condition_ref` (bool), `universal` (bool), `attributes` — danh sách thuộc tính; mỗi phần tử có `attribute`, `unit`, `value`, `conditions` (object), có thể có `part` riêng.
- `evidences`: danh sách bản ghi bằng chứng, mỗi bản ghi có `id` (duy nhất), `product`, `version`, `market`, `part`, `attribute`, `unit`, `value`, `conditions`.
- `value`: `kind ∈ {exact, gt, ge, lt, le, interval, approx, version}`; với số: `a` (và `b`, `closed` cho khoảng) dạng chuỗi thập phân; `role ∈ {measurement, declared_maximum, declared_minimum, unknown}`; riêng claim có thêm `stated_spec` (con số trần, hướng dẫn §5). Với phiên bản: `v`, `op ∈ {eq, ge}`.

Đầu ra: `(nhãn, nei_type, vết)` với nhãn ∈ {Supported, Refuted, NEI}; `nei_type ∈ {missing, conflict, None}`; vết là danh sách `(quan hệ, lý do)` từng thuộc tính. Hồ sơ hỏng ném `RecordError`; `safe_verdict` trả `('ERROR', thông điệp, [])`. Runner phải ghi ERROR là lỗi kỹ thuật, không đổi thành NEI.

Hồ sơ đầu vào phải **thuần dữ kiện**: không có nhãn chuẩn, lý do người gán, nhật ký tìm nguồn, nhóm mẫu, thao tác tạo biến thể hoặc kết quả kiểm luật (kiểm bằng [`check_input_leak.py`](../scripts/check_input_leak.py)).

## 2. Thuật toán

```text
verdict(claim, evidences):
  validate(claim, evidences)                       # lỗi → RecordError
  for attr in claim.attributes:
    cands = []
    for ev in evidences:
      A: bỏ ev nếu product/version/market/attribute khác (trường claim = null thì không ràng buộc),
         hoặc part khác, hoặc không đổi được đơn vị về attr.unit
      B: điều kiện claim nêu phải bằng điều kiện của ev, nếu không → bỏ
         điều kiện ev có mà claim không nêu:
           condition_ref → dùng đầy đủ
           policy literal → bỏ  (chỉ dùng cho ablation P−inherit)
           claim universal → chỉ dùng làm phản ví dụ (REFUTE_ONLY)
           còn lại → kế thừa, dùng đầy đủ (FULL)
      cands += ev
    nếu cands rỗng → UNKNOWN
    nhóm cands theo bộ điều kiện đầy đủ của ev
    C1: trong cùng nhóm, có cặp ev mâu thuẫn (C2 cho CONTRADICT) → CONFLICT
    phản ví dụ: nhóm REFUTE_ONLY có C2 = CONTRADICT → CONTRADICT
    C2 cho từng nhóm FULL: CONTRADICT nếu có ev bác bỏ, SUPPORT nếu có ev hỗ trợ, ngược lại UNKNOWN
    nhiều nhóm FULL: tất cả CONTRADICT → CONTRADICT; tất cả SUPPORT → SUPPORT; ngược lại UNKNOWN
  C3: có CONTRADICT → Refuted; có CONFLICT → NEI-conflict; tất cả SUPPORT → Supported; còn lại NEI-missing
```

Lưu ý thiết kế:

1. **Phạm vi xung đột** là một thuộc tính + một bộ điều kiện. Vì claim là phép hội, thuộc tính bị bác bỏ quyết định nhãn Refuted ngay cả khi thuộc tính khác xung đột (test `test_refutation_beats_conflict_on_other_attribute`). Trong cùng thuộc tính, C1 chạy trước C2 nên không có bác bỏ từ dữ liệu đang xung đột.
2. **Nhiều chế độ** (claim không nêu chế độ, nguồn có nhiều chế độ) không phải xung đột; dùng quy tắc “mọi cách đọc” của hướng dẫn §4.3.
3. **Lượng từ phổ quát** không được kế thừa điều kiện; chỉ có thể bị bác bỏ bởi phản ví dụ. P hiện chưa có luật xác nhận bao phủ “mọi chế độ” nên claim phổ quát không thể Supported qua kế thừa; đây là giới hạn được ghi nhận.
4. A không loại bằng chứng vì khác `value_kind`; loại giá trị được xử lý ở C2.
5. Dung sai mặc định 0; `approx` chỉ hỗ trợ `approx` cùng số; không tự tạo dung sai.

## 3. Bảng C2 (cùng phạm vi, điều kiện, đơn vị; S/R/U = hỗ trợ/bác bỏ/chưa đủ)

| Bằng chứng | Claim | Quan hệ |
|---|---|---|
| `x=a` | `x=b` | S nếu a=b; R nếu a≠b |
| `x>a` | `x=b` | R nếu b≤a; U nếu b>a |
| `x≥a` | `x=b` | R nếu b<a; U nếu b≥a |
| `x≤u` | `x=b` | R nếu b>u; U nếu b≤u |
| `x<u` | `x=b` | R nếu b≥u; U nếu b<u |
| `x>a` | `x>b` | S nếu a≥b; U nếu a<b |
| miền E | miền Q (cùng x) | S nếu E⊆Q; R nếu E∩Q=∅; U nếu giao mà không bao hàm |
| `M=a` (tối đa công bố) | `M=b` | S nếu a=b; R nếu a≠b |
| `m=a` (tối thiểu công bố) | `m=b` | S nếu a=b; R nếu a≠b |
| `M=u` | `x=b` | R nếu b>u; U nếu b≤u |
| `M=u` | miền Q về x (bất đẳng thức/khoảng) | S nếu `(−∞,u]⊆Q`; R nếu `(−∞,u]∩Q=∅`; U còn lại |
| `x=a` (đo đạc) | `M=b` | U (đo đạc không suy ra mức công bố) |
| bất kỳ vai trò | claim `stated_spec` = a | xử lý như claim cùng vai trò với bằng chứng (M nếu nguồn là M, x nếu nguồn là x) |
| `approx a` | `approx b` | S nếu a=b và cùng vai trò; U nếu khác |
| `approx a` | số chính xác/khoảng | U |
| phiên bản a | phiên bản b | S nếu cùng chuỗi chuẩn hóa; R nếu khác; U nếu có `op=ge` hoặc chỉ số chính |
| vai trò `unknown` | bất kỳ | U |

## 4. Ca kiểm tra bắt buộc (đều có trong `tests/test_abc.py`)

| Ca | Bằng chứng / claim | Mong đợi |
|---|---|---|
| EX-18 | tổng nghe `>24` / `=24` | Refuted qua C2 |
| biên EX-18 | `>24` / `=25` | NEI-missing |
| biên đóng | `≥24` / `=24` | NEI-missing |
| EX-20 | sau sạc 15 phút “lên đến 3” / “chính xác 3” | NEI-missing |
| vượt cận | “lên đến 3” / “chính xác 4” | Refuted |
| EX-11 | M=20 / M=25, chống ồn bật | Refuted, không dùng bao hàm |
| EX-12 | cùng “khoảng 1,5 giờ” sau sạc 5 phút | Supported |
| EX-10 | nguồn chống ồn bật / claim chống ồn tắt | NEI-missing qua B, không phải xung đột |
| nhiều chế độ | nguồn 4 h (bật) và 6 h (tắt) / claim “lên đến 10 giờ” không nêu chế độ | Refuted (mọi cách đọc bác bỏ) |
| nhiều chế độ | như trên / claim “lên đến 6 giờ” | NEI-missing |
| con số trần | nguồn M=6 / claim “pin 6 giờ” (`stated_spec`) | Supported |
| phổ quát | nguồn 4 h và 6 h / claim “luôn 6 giờ” | Refuted (phản ví dụ) |
| EX-21–23 | hai nguồn giả lập cùng phạm vi, khác giá trị | NEI-conflict |
| xung đột + bác bỏ | thuộc tính 1 xung đột, thuộc tính 2 bị bác bỏ | Refuted |
| xung đột + thiếu | thuộc tính 1 xung đột, thuộc tính 2 thiếu | NEI-conflict |
| hồ sơ hỏng | thiếu thuộc tính, kind lạ, số không đọc được, id trùng, khoảng đảo biên | ERROR |

EX-21–23 dùng sản phẩm `SIM-*` do AI soạn để kiểm thử; không phải thông số hãng và không tính vào đánh giá. EX-01–20 là ca minh họa có nguồn Apple đã đối chiếu nhưng câu gốc không có log sinh (`unknown_legacy`), nên chỉ dùng làm fixture/ví dụ, không vào tập dev/val/test.

Với chính sách chung, nhãn minh họa của cả 23 câu gốc (`original_claim`) khớp nhãn trong `examples.json` (test `test_original_claims_shared_policy_no_drift`). Đọc nghĩa đen (`literal`) làm 9 câu gốc chuyển sang NEI; đây là lý do giữ `literal` làm ablation P−inherit thay vì chính sách.

## 5. Phân tích thành phần (ablation) — phần cốt lõi của RQ3

Tất cả ablation chạy trên **đúng hồ sơ trích xuất của lượt 1** mà P và B1 đã dùng, nên không tốn lượt gọi LLM và chỉ thay đổi một thành phần của bộ quyết định:

| Mã | Tắt gì | Giữ nguyên | Câu hỏi trả lời |
|---|---|---|---|
| `P−part` | kiểm bộ phận ở A | sản phẩm/phiên bản/thuộc tính/đơn vị, B, C1–C3 | kiểm bộ phận ngăn bao nhiêu chấp nhận nhầm kiểu “khối lượng hộp ↔ tai nghe”? |
| `P−B` | toàn bộ kiểm điều kiện (mọi nguồn cùng nhóm) | A, C | kiểm điều kiện ngăn bao nhiêu lỗi “sai chế độ”? Khi tắt B, C1 có thể báo xung đột giả; đó là tác động cần đo, không sửa C để bù |
| `P−role` | phân biệt mức công bố với giá trị quan sát (mọi giá trị coi là đo đạc) | A, B, C1, C3 | phân biệt vai trò con số ngăn bao nhiêu lỗi “lên đến a” ↔ “chính xác a”? |
| `P−inherit` | kế thừa điều kiện thử (dùng `literal`) | A, C | chính sách kế thừa làm thay đổi Recall Supported và FAR thế nào? |

Kết quả ablation là bằng chứng nhân quả **trong phạm vi bộ quyết định** (cùng hồ sơ, chỉ đổi một luật). Nó không đo tác động của trích xuất; lỗi trích xuất được tách bằng thí nghiệm hồ sơ chuẩn TN4 (sổ tay mục 6.1). Phân tích lỗi thủ công chỉ mô tả, không thay ablation.
