# Giao thức dữ liệu và đánh giá — dự thảo chốt trước thực nghiệm

Cập nhật 08/10/2026 theo bảy nhận xét phương pháp. Đây là **kế hoạch**, chưa có dữ liệu thí nghiệm mới, người gán thứ hai hoặc kết quả chạy lặp được xác nhận. Trước test phải chốt phiên bản/hash và mọi điều chỉnh khả thi với GVHD; không thay tiêu chí sau khi thấy dự đoán.

## 1. Đơn vị đánh giá và câu hỏi được phép trả lời

Đầu vào chính là claim đã tách/rà soát thủ công, liên kết quảng cáo LLM gốc, và định danh đúng sản phẩm được cung cấp. Giữ nghĩa câu sinh thông thường; thêm điều kiện, đổi số/bộ phận/phiên bản là **biến thể**, không còn câu sinh thông thường nguyên nghĩa. Tập nguồn chính thức có phiên bản, thị trường và thời điểm khóa.

Đánh giá E3 gồm truy hồi có điều kiện theo sản phẩm → trích xuất JSON → quyết định nhãn. Không bao gồm sai sót tự nhận diện sản phẩm hay tách claim từ quảng cáo thô. Website không phải bằng chứng chất lượng thuật toán; nếu có tách tự động, phải đo riêng bỏ sót, đổi nghĩa/điều kiện và đánh giá toàn trình trước khi kết luận về toàn trình.

RQ3 tối thiểu vẫn thăm dò trên 12 họ chia 6/2/4; 18/20 họ dùng 7/4/7 hoặc 8/4/8. Pilot đúng 6 họ ở dev. Không đổi họ để cân bằng nhãn sau khi đã dùng phát triển. Chọn model/prompt/k trên dev, dung sai theo nguồn; val audit một lượt sau khóa, test không chọn cấu hình.

## 2. Cùng tiêu chí nhãn, không dùng P làm chuẩn

[HUONG_DAN_GAN_NHAN.md](HUONG_DAN_GAN_NHAN.md) là **khối ngữ nghĩa chung**: ba nhãn, phạm vi/điều kiện, giới hạn số, gần đúng/dung sai, phiên bản, xung đột và thiếu. [QUY_TAC_ABC.md](QUY_TAC_ABC.md) là đặc tả hiện thực, không là đầu ra đáp án.

Người gán được đọc toàn bộ nguồn đã khóa và lưu nhãn, đoạn dẫn, lý do. Không đọc dự đoán P/B1 để chọn nhãn. Hướng dẫn được hoàn thiện từ nguồn và ca dev, không từ việc ép nhãn khớp P. Giữ ca tự nhiên khó/không trùng mẫu luật; không loại sau khi biết P sai. Bất đồng với code có thể là lỗi code, lỗi trích, lỗi hướng dẫn hoặc lỗi nhãn, không mặc định nhãn phải theo code.

| Bản | Đầu vào dữ kiện | Tiêu chí quyết định |
|---|---|---|
| B0 | Cùng claim, product context, văn bản top-k kèm tiêu đề/chú thích/metadata | Toàn bộ hướng dẫn chung trong prompt, LLM gán nhãn |
| B1 | Cùng claim/context, hồ sơ dữ kiện trích/chuẩn hóa của lượt chạy | **Cùng nguyên khối hướng dẫn**, LLM gán nhãn |
| P | Chính hồ sơ và hash mà B1 nhận trong lượt đó | Code hiện thực tiêu chí chung |

Chỉ P–B1 gần với câu hỏi “luật cứng hay LLM quyết định trên cùng hồ sơ”. P–B0 còn khác biểu diễn/trích xuất nên không cô lập riêng tác động code. Cùng hướng dẫn giảm bất công về thông tin, không xóa được giới hạn của chuẩn nhãn tự xây hoặc chứng minh độ đúng ngoài miền.

Đã có [script tạo prompt](../scripts/build_eval_prompts.py) và [hai mẫu prompt](../templates/eval_prompts.json). Script kiểm B0/B1 chứa cùng **nguyên văn và SHA-256** hướng dẫn. Chưa có runner/model được gọi. Khi triển khai phải:

- Nạp prompt đã kiểm, lưu thông điệp thực gửi cùng hash; không âm thầm cắt hướng dẫn khi quá ngữ cảnh. Mô hình không đủ cửa sổ ngữ cảnh thì cấu hình đó không hợp lệ.
- Dùng cùng ví dụ few-shot từ dev nếu bổ sung; không lấy EX hoặc test làm few-shot rồi tính chúng vào test. Các ví dụ số trong hướng dẫn chỉ là minh họa giả định.
- Không đưa gold label, gold-evidence membership, source-search kết luận NEI, nhãn nguồn gốc mẫu, thao tác sửa hoặc dấu vết A–B–C vào B0/B1/P. Metadata sản phẩm/phiên bản/thị trường và dữ kiện nguồn là đầu vào hợp lệ; nhật ký gán nhãn không phải đầu vào.
- Giữ hồ sơ chung thuần dữ kiện, không chứa `is_supported`, `is_contradicted` hoặc kết quả kiểm luật của P. Trích xuất/chuẩn hóa có thể vẫn sai; đó là lỗi cần đo ở cả B1/P.

## 3. Kiểm tra nhãn độc lập

Mục tiêu: **30 claim** được một người thứ hai gán độc lập. Chưa có người nhận việc; không tự viết tên, ngày, số đồng thuận hoặc kappa. Việc mời và xác nhận phải do sinh viên thực hiện, không coi một lượt AI khác là người gán thứ hai.

1. Chuẩn bị hướng dẫn và 3–5 ví dụ luyện từ dev, ngoài mẫu kiểm tra. Người thứ hai cần hiểu được tài liệu Việt/Anh và phân biệt thuộc tính/điều kiện; không yêu cầu họ đọc code P.
2. Trước dự đoán, lấy mẫu theo seed ghi lại, phân tầng nhãn sơ bộ, hai nhóm nguồn gốc và nhiều họ; mục tiêu 10 mẫu mỗi nhãn sơ bộ khi có đủ. Nếu đã có split, lấy cả test, mục tiêu ít nhất 12/30 và trải trên các họ test khi khả thi. Không đổi mẫu vì hai người không đồng ý. Phân tầng dùng nhãn sơ bộ chỉ do người quản lý mẫu thực hiện; người gán thứ hai không thấy nhãn đó hoặc nhóm/thao tác biến thể.
3. Gói gán chỉ chứa mã ẩn, câu, ngữ cảnh cần thiết, cùng corpus đã khóa và hướng dẫn. Người thứ hai không thấy nhãn/lý do người đầu, dự đoán hoặc code P. Lưu nhãn, bằng chứng và giải thích vào [mẫu CSV](../templates/independent_annotation.csv).
4. Tính đồng thuận và bảng bất đồng **trước hòa giải**. Có thể báo Cohen’s kappa (không trọng số, ba nhãn); nếu mẫu làm mẫu số không xác định thì ghi không xác định. Báo cỡ mẫu, phân tầng, nhãn/họ/nhóm thực tế. Đồng thuận 30 mẫu không tự suy thành tỷ lệ đúng của toàn bộ dữ liệu; hai người vẫn có thể cùng hiểu sai.
5. Hòa giải bằng nguồn, không chạy P để quyết định ai đúng. Lưu cả hai nhãn ban đầu, lý do bất đồng và nhãn cuối; ca chưa thể chốt đưa vào trạng thái nhãn chờ duyệt, không ép NEI chỉ vì người gán bất đồng. Báo số ca chưa chốt, không âm thầm xóa mẫu khó.
6. Không dùng bất đồng trên test để tinh chỉnh P/prompt. Nếu buộc sửa tiêu chí ngữ nghĩa vì mẫu test trước khóa, ghi test đã ảnh hưởng thiết kế và giới hạn độc lập; không tuyên bố tập đó hoàn toàn chưa dùng phát triển. Sau khóa phải version lại nhãn, giữ bản cũ và đánh giá đồng bộ, không chỉ sửa ca P sai.

Gán lại 20% sau 1–2 tuần, ẩn nhãn cũ vẫn hữu ích nhưng chỉ là **tự nhất quán**. Nếu không tìm được người thứ hai hoặc chỉ làm được 20–29 mẫu, ghi số thực tế/thiếu hụt và hạn chế; không coi tự gán lại hoặc AI là thay thế, không gọi đã kiểm tra nhãn độc lập khi chưa có log.

## 4. Hai nhóm dữ liệu và ngưỡng vận hành

- `ordinary_llm`: sinh từ yêu cầu quảng cáo thông thường, không yêu cầu tạo lỗi; giữ output/log gốc và toàn bộ claim hợp lệ theo quy trình tách. Thu theo lô, số quảng cáo/ngân sách và tiêu chí dừng chốt trước, không giữ riêng mẫu thuận phương pháp hoặc cân nhãn bằng cách bỏ output.
- `controlled_variant`: sửa giá trị, phiên bản, bộ phận, điều kiện hoặc cách diễn đạt; có mẫu cha/thao tác/editor/time. Người gán đọc nguồn xác định nhãn, không lấy thao tác làm nhãn. Nếu prompt yêu cầu cố tình nói sai thì thuộc nhóm có kiểm soát, không gọi lỗi tự nhiên.
- `unknown_legacy`, câu tự viết không có log và `synthetic_test_fixture` không tính vào tập quảng cáo LLM chính. EX-01–23 hiện vẫn nằm ngoài dữ liệu chính. Mẫu cha và biến thể cùng họ/tập.

Các mốc sau là **đề xuất quản lý đã đặt trước kết quả**, không là ngưỡng bảo đảm công suất hay độ tin cậy:

| Tập | Supported tối thiểu | Refuted tối thiểu | NEI tối thiểu | Nhóm thông thường |
|---|---:|---:|---:|---:|
| Dev (có pilot) | 10 | 10 | 10 | ≥50% số claim trong tập |
| Val | 3 | 3 | 3 | ≥50% |
| Test | 10 | 10 | 10 | ≥50% |

Test cần ít nhất 30 claim theo ba sàn nhãn; dev cần 30, val cần 9, tổng sàn 69 nên không tự mâu thuẫn với mục tiêu 120 claim. Đây không phải chỉ định kích thước từng tập hoặc bảo đảm mọi cách chia theo họ đều đạt. Với pilot 45–60 claim và 12 họ, vẫn phải kiểm năng suất/phân bố thực tế ở Gate 2. Mong muốn mỗi nhãn test có mặt ở ít nhất hai họ; nếu không đạt, báo mức tập trung theo họ. Nhiều biến thể gần trùng không được dùng để giả tăng độ đa dạng.

**Không đặt quota nhãn để chọn lọc nhóm thông thường.** Độ phủ nhãn tối thiểu kiểm trên tập hỗn hợp; nhóm thông thường được giữ phân bố của quy trình sinh. Thu thêm theo lô đã định hoặc bổ sung biến thể có nhãn đọc nguồn, đồng thời giữ tỷ lệ thông thường ≥50%. Không tìm cách chạy đến khi P có lợi; không lấy họ dev/val sang test. Nếu không đạt trong ngân sách thì báo số thiếu và giảm mức kết luận, không làm giả dữ liệu/nhãn hoặc sửa ngưỡng sau khi thấy dự đoán.

Bảng kết quả bắt buộc gồm toàn test hỗn hợp **và hai bảng riêng**; mỗi bảng có:

- n_S, n_R, n_NEI, số họ và số lỗi kỹ thuật/không có dự đoán.
- FAR = (R→S + NEI→S)/(n_R+n_NEI); Recall Supported = S→S/n_S.
- Macro-F1, từng nhãn; riêng R→S/n_R và NEI→S/n_NEI để thấy tác động thay đổi hỗn hợp lỗi.
- Tử số/mẫu số nguyên bên cạnh phần trăm. Mẫu số 0 → `NA`, không ép 0; mẫu số dương <10 → tính được nhưng gắn “ít mẫu”, không dùng làm bằng chứng ưu thế riêng nhóm. Đây cũng là cảnh báo vận hành, không có bước nhảy khoa học giữa 9 và 10.

Không đòi mỗi nhóm đạt cả ba sàn nếu điều đó buộc bóp phân bố tự nhiên. Một nhóm có thể thiếu hẳn Refuted/NEI hoặc Supported; công khai chỉ số không xác định. Với n_S=10, một lỗi đã làm Recall đổi 10 điểm phần trăm; ngưỡng đánh đổi −5 điểm của RQ3 không khiến phép đo trở nên chính xác hơn.

So sánh chính P–B1 vẫn ở E3 trên hỗn hợp đã khóa, phản ánh đúng hỗn hợp đó. Nếu chỉ nhóm biến thể có lợi hoặc nhóm thông thường ít mẫu, không được kết luận P giảm lỗi quảng cáo LLM sinh thông thường. RQ3 tối thiểu là thăm dò, kết hợp từng họ, bỏ từng họ và bất định; không biến các sàn này thành kiểm định ưu thế.

## 5. Truy hồi có lọc sản phẩm

`product-filtered` là thiết lập chính hợp lệ cho ứng dụng đã biết sản phẩm, nhưng là giả định đầu vào thuận lợi. Với mỗi sản phẩm/claim, lưu số tài liệu, N đoạn ứng viên thực sau chia/khử trùng/lọc, top-k ID, k_eff=min(k,N), độ dài đoạn và số đoạn của bộ bằng chứng chuẩn. Báo bảng theo sản phẩm cùng min/trung vị/max N, tỷ lệ claim N≤k, recall@k tổng thể và riêng N>k (nhóm rỗng ghi NA).

Recall là tỷ lệ chứa **trọn ít nhất một bộ bằng chứng chuẩn**, không phải gặp một đoạn có cùng số. NEI-thiếu không tự coi là truy hồi đúng; NEI-xung đột cần đủ cả hai phía nếu đã định bộ bằng chứng tương ứng. Nếu N≤k, hệ thống lấy hết ứng viên; recall cao trong nhóm đó không nói lên khả năng xếp hạng. Vẫn có thể thiếu nếu bộ bằng chứng bị thất lạc khi xây kho/chia đoạn; báo đây là lỗi độ phủ nguồn/chunking, không che bằng mẫu số hẹp.

Phần mở rộng `unfiltered` nếu đã chọn tại Gate 4:

- Kho nhiều sản phẩm và phạm vi nguồn ứng viên được khóa trước test; chỉ tài liệu nguồn, không nhãn/claim gán nhãn hoặc search log có kết luận. Công bố chính xác những sản phẩm/tài liệu được đưa vào.
- Dùng cùng claim/query (vẫn có tên sản phẩm), cách chia đoạn, chuẩn hóa và k đã khóa; chỉ bỏ bộ lọc sản phẩm. Không bỏ tên sản phẩm khỏi query để làm khó khác tác vụ.
- Báo recall, N, tỷ lệ đoạn sai sản phẩm. Đo truy hồi riêng là đủ cho mở rộng này; nếu chạy cả P, A vẫn phải kiểm sản phẩm. Không dùng nguồn sai sản phẩm như một bác bỏ hợp lệ.
- So sánh với thiết lập chính, không thay bảng chính bằng bảng đẹp hơn. Không thực hiện thì ghi rõ; dữ liệu từ đúng sản phẩm không được mô tả là tìm kiếm toàn web.

## 6. Nhật ký tìm nguồn cho NEI-thiếu

[Mẫu nhật ký](../templates/nei_search_log.json) là khung trống, không phải việc đã thực hiện. Trước chốt nhãn, rà tối thiểu các loại nguồn: thông số, hướng dẫn sử dụng, hỗ trợ/PDF chính thức áp dụng. Loại nguồn không có/tìm chưa được/không truy cập được phải ghi đúng trạng thái và cách tìm, không giả vờ đã đọc.

Mỗi ca cần `claim_id`, phạm vi sản phẩm/phiên bản/thị trường/bộ phận/thuộc tính, `corpus_id/version/hash`, người/ngày rà và điều chưa có; từng lượt lưu URL yêu cầu/cuối, loại nguồn, trạng thái truy cập, snapshot/hash, từ khóa Việt–Anh và tên tương đương, mục/bảng/chú thích đã đọc, thông tin tìm được và lý do loại nguồn sai phạm vi. Kiểm cả nội dung theo mục, không chỉ tìm chuỗi đúng nguyên văn.

Lý do dừng phải cho biết đã hoàn tất những bước nào và còn hạn chế gì. Cố gắng dùng cùng độ sâu/quy trình cho mọi nhãn và nhóm, không tìm kỹ hơn chỉ vì cần xác nhận lỗi của một bản. Thiếu bước bắt buộc → nhãn `pending_review`, không coi là NEI chuẩn; ngoài phạm vi corpus/nguồn không truy cập cần được xử lý theo tiêu chí khóa trước và báo riêng số ca.

NEI trong corpus X là kết luận **có điều kiện**. Nếu có nguồn chính thức khác ngoài X giải quyết được claim, không tự động phủ nhận nhãn tương đối với X, nhưng cho thấy độ phủ X hạn chế. Phải ghi nguồn mới và version lại corpus/nhãn khi mở rộng, không ghi đè lịch sử hoặc chỉ cập nhật ca giúp P. Không tuyên bố “hãng không công bố” khi thực tế chỉ chưa tìm thấy trong các trang đã đọc.

EX-07/10/16/20 đã có `nei_search_log` trong [examples.json](../evidence/2026-10-08/examples.json): chỉ một trang đã lưu cùng chú thích, từ khóa/những dòng khớp và thiếu sót tìm nguồn. `production_label_ready=false`; không bịa rằng đã rà hết manual/support khác. Các log này làm rõ giới hạn minh họa, **chưa hoàn thành quy trình nhãn cho dữ liệu chính**. Không đưa search log/nhãn NEI của người gán vào mô hình, vì đó sẽ là rò đáp án.

## 7. Chạy lặp và metadata

[run_manifest.json](../templates/run_manifest.json) ghi model yêu cầu/thực trả, revision/checkpoint, nhà cung cấp/endpoint không chứa khóa, ngày giờ/múi giờ, temperature/top_p/max_tokens/seed và trạng thái có hỗ trợ, backend/fingerprint nếu được trả. Chạy local thêm engine/version, quantization, precision và phần cứng. Không biết trường nào thì ghi `unavailable` kèm lý do, không đoán; tên Llama giống nhau không chứng minh hai endpoint cấu hình giống nhau.

Lưu phiên bản code, corpus/index/chunking/query, split/sample list, hướng dẫn và prompt đã render cùng hash, ID các đoạn truy hồi, cấu hình cache/retry, request/response gốc và lỗi, token/chi phí/thời gian. Không lưu API key/token hay thông tin đăng nhập. Nhà cung cấp tự đổi model phải được ghi như thay đổi điều kiện, không ghép ngầm vào một kết quả duy nhất.

Kế hoạch mặc định **3 lượt tổng cộng trên min(30, n_test) claim**:

1. Khóa danh sách bằng seed và phân tầng nhãn/nhóm/họ khi có thể, trước khi xem dự đoán. Không chọn chỉ các ca B1 dao động hay ca P thắng. Ghi mọi tầng không đủ mẫu.
2. Lượt 1 chạy toàn test và là bảng kết quả chính đã định trước. Phần mẫu trên dùng đúng output lượt 1; chạy thêm lượt 2 và 3 cho phần đó, không chạy ba lượt thêm nữa.
3. Mỗi lượt bổ sung gọi trích xuất mới (không trả lại cache lượt trước). Trong một lượt, B1 và P dùng **cùng** `extraction_run_id` và `normalized_records_sha256`; B0 nhận cùng raw evidence và hướng dẫn. Giữ model/provider/decoding và kho nguồn; seed khác được chốt trước nếu hỗ trợ, nếu không thì ghi rõ.
4. P có cùng hồ sơ thì tất định; chạy lại riêng code P ba lần không đo được bất định LLM. Sự khác nhau giữa các lượt P có thể đến từ trích xuất. Muốn tách biến động quyết định B1 khỏi trích xuất cần một kiểm tra riêng giữ cố định hồ sơ, không được khẳng định đã tách hai nguồn biến động chỉ từ ba lượt toàn trình này.
5. Báo từng lượt trên **cùng phần mẫu**, trung bình, min–max, độ lệch chuẩn nếu tính và tỷ lệ claim đổi nhãn. Đối chiếu ΔFAR/ΔRecall của từng cặp B1/P cùng lượt. Không so toàn test lượt 1 với phần mẫu lượt 2 như cùng quần thể; không chọn lượt tốt nhất hoặc coi 30×3=90 claim độc lập.

Ba lượt là kiểm tra dao động sơ bộ theo ngân sách, không bảo đảm ước lượng phân bố hay công suất. Phân biệt bất định do chọn mẫu/họ với do chạy LLM. Nếu ngân sách không đủ, công khai giảm số lượt/phần mẫu **trước test**, không nói đã ổn định vì temperature=0 hoặc vì P là code. Kết quả âm và dao động đủ làm đảo chiều so sánh đều cần báo.

Việc không nên chỉ báo một điểm số cho phương pháp không tất định có nền tảng trong [Reimers & Gurevych, 2017](https://aclanthology.org/D17-1035/). Bài đó nghiên cứu LSTM sequence tagging, không chứng minh “ba lượt LLM là đủ”; con số ba ở đây là lựa chọn vận hành có giới hạn.

## 8. AI hỗ trợ và xác nhận của sinh viên

Bản rà soát 08/10 có AI (Codex) hỗ trợ đọc PDF/trang nguồn, kiểm số và biên tập tài liệu, tạo script/prompt mẫu và EX-21–23 giả lập. Tên model backend cụ thể của các phiên trợ lý không được tự phục dựng từ tên gọi người dùng. Hoạt động này tách khỏi quảng cáo LLM sẽ sinh theo giao thức thí nghiệm.

Câu khai báo trung thực hiện có thể dùng: “Phần tổng hợp/đối chiếu và biên tập trong bản rà soát tháng 10 có công cụ AI hỗ trợ; các ca xung đột EX-21–23 do AI soạn để minh họa. Các nguồn gốc được dẫn riêng. Sinh viên cần tự kiểm tra nguồn và chịu trách nhiệm nội dung; tình trạng xác nhận thủ công được ghi riêng.” Không tự đổi thành “tôi đã tự kiểm” khi chưa có xác nhận.

Danh sách tối thiểu cho sinh viên tự kiểm, đều **chưa xác nhận**:

| Bài/bảng | Trang PDF | Trường cần kiểm | Ảnh hỗ trợ |
|---|---:|---|---|
| [2], Bảng 1 | 3 | Cột Pearson/Spearman, hàng LLM sufficiency 0,14/0,09 | [Ảnh](../evidence/2026-10-08/papers/ref02-page03.png) |
| [3], Bảng 1 | 7 | Llama-3.1-8B/QuanTemp, Macro-F1 44,80 và 53,91; phân biệt verifier Llama-3.2-3B | [Ảnh](../evidence/2026-10-08/papers/ref03-page07.png) |
| [5], Bảng 2 | 9 | Cột Conflict, Accuracy/Macro-F1/Balanced Accuracy và CoVer/Confact | [Ảnh](../evidence/2026-10-08/papers/ref05-page09.png) |

Mở PDF gốc trong `báo/`, kiểm tiêu đề hàng/cột, đơn vị và điều kiện, ghi người/ngày/kết quả và sửa nếu thấy lệch; tiếp tục rà các số và nguồn còn lại trước khi nộp. Script kiểm chuỗi/ảnh không chứng nhận sinh viên đã đọc, một AI thứ hai cũng không thay xác nhận đó.

Đã tra và mở trang công khai của Khoa MMT&TT về [đăng ký KLTN HK1 2026–2027](https://nc.uit.edu.vn/giao-vu/thong-bao-v-v-dang-ky-kltn-hk1-nam-hoc-2026-2027.html) và [kế hoạch bảo vệ HK2 2025–2026](https://nc.uit.edu.vn/giao-vu/ke-hoach-to-chuc-bao-ve-khoa-luan-tot-nghiep-hk2-nam-hoc-2025-2026.html). Chưa xác minh được từ các trang này mẫu/quy định AI cụ thể áp dụng cho hồ sơ này; **không suy ra khoa không có quy định** hoặc đã chấp thuận cách dùng AI. Sinh viên cần xin văn bản/yêu cầu đúng kỳ từ GVHD/khoa và cập nhật khai báo trước nộp; không lấy chính sách của trường khác thay thế.

## 9. Các cổng trước khi công bố kết quả

- Gate 1–2: hướng dẫn chung, cách thu hai nhóm, log nguồn NEI, metadata mô hình, dự toán lặp; mời người thứ hai và ghi tình trạng thật.
- Gate 3: gán độc lập/hòa giải hoặc báo thiếu; bảng nhóm×nhãn×split; corpus/search log và các nhãn chờ duyệt; B0/B1 có đầy đủ hướng dẫn.
- Gate 4: khóa hash, danh sách phần mẫu/lượt chạy, tiêu chí thiếu mẫu, ngân sách và lựa chọn unfiltered; không thay theo test.
- Gate 5: bảng toàn test/hai nhóm/họ, mẫu số, truy hồi kèm N, kết quả phần mẫu ba lượt và lỗi kỹ thuật; giới hạn thăm dò.
- Gate 6: kết luận chỉ cho claim đã tách, không end-to-end; ghi AI hỗ trợ và phần sinh viên đã thực sự xác nhận; lưu bộ tài liệu/mã/log tái lập.
