#!/usr/bin/env python3
"""Thiết kế lại kế hoạch trong hai docx (bản đề xuất điều chỉnh 08/10/2026, chờ GVHD xác nhận).

Thay review_patch_2026_10_08.py (chỉ nối thêm đoạn). Script này viết lại nội dung
các ô/đoạn của đề cương (HuP_4) và báo cáo tháng 09 (HuP_3) bằng chữ đỏ C00000,
không thêm/xóa hàng bảng, không đổi header/footer, hình, sectPr, thuộc tính bảng
và hàng chữ ký "Xác nhận của CBHD / 15/09/2026".

Mặc định: xem trước + kiểm tra. --apply: ghi đè hai docx (bản gốc có trong Git và
bản sao lưu sha256 ngoài repo). Chạy lại trên docx đã sửa sẽ dừng (chống vá hai lần).
"""
import argparse
import io
import json
import sys
from pathlib import Path
from xml.dom import minidom
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_thesis_docs import (ROOT, REPORT, PROPOSAL, body, cell_at, children,  # noqa: E402
                                paragraph, set_cell, structure, text, validate_content)

HEADER = 'Bản đề xuất điều chỉnh, chờ GVHD xác nhận'
D = '(DỰ THẢO — cần GVHD xác nhận)'

PROPOSAL_HEADER = (
    f'{HEADER} (08/10/2026). Chữ đỏ là phần thiết kế lại; chữ đen giữ từ bản đăng ký 15/09/2026. '
    'Các điểm cần GVHD xác nhận: (1) lịch Gate mới, Gate 1 kết thúc 31/10 thay vì 15/10; '
    '(2) cam kết MVP 120 phát biểu / 12 họ, 180/18 chỉ là mục tiêu nếu năng suất đo được cho phép; '
    '(3) luật inherit_headline cho claim không nêu điều kiện thử; (4) xử lý nguồn thị trường Moldova của EX-13–15; '
    '(5) mở rộng nguồn sang ít nhất một hãng ngoài Apple; (6) nhà cung cấp API chạy Llama và ngân sách; '
    '(7) người gán nhãn thứ hai cho 30 phát biểu; (8) RQ3 chỉ ở mức thăm dò. Chi tiết: docs/QUYET_DINH_CAN_CHOT.md.'
)

PROPOSAL_ROWS = {
    4: 'Nội dung đề tài: Nghiên cứu cách kiểm chứng từng phát biểu thông số trong quảng cáo tiếng Việt về tai nghe không dây do mô hình ngôn ngữ lớn (LLM) tạo ra, dùng tài liệu văn bản chính thức của đúng sản phẩm làm bằng chứng. Mỗi phát biểu được gán Supported (bằng chứng hỗ trợ đầy đủ), Refuted (bằng chứng bác bỏ trực tiếp) hoặc NEI (Not Enough Information: bộ nguồn đang xét chưa đủ để kết luận), kèm đoạn nguồn và lý do. Trọng tâm là so sánh có kiểm soát giữa bộ quyết định bằng quy tắc A–B–C (P) và LLM tự quyết định trên cùng hồ sơ dữ kiện (B1), xem P có giảm chấp nhận nhầm hay không. Đề tài đánh giá trên phát biểu đã tách và rà soát thủ công, không phải hệ thống end-to-end từ quảng cáo thô.',
    5: 'Mục tiêu (MVP — phải đạt): \nM1. Xây dựng bộ dữ liệu nhỏ có provenance (nguồn gốc truy vết được): quảng cáo LLM sinh thông thường kèm log đầy đủ, phát biểu tách thủ công, nhãn ba lớp, bộ bằng chứng chuẩn và nhật ký tìm nguồn (search_log) cho NEI; quy mô cam kết 120 phát biểu / 12 họ sản phẩm.',
    6: 'M2. Viết hướng dẫn nhãn dùng chung có phiên bản và mã băm, áp dụng như nhau cho người gán nhãn, B0, B1 và P; kiểm tra độ tin cậy nhãn bằng một người thứ hai gán độc lập 30 phát biểu và tự gán lại 20%.',
    7: 'M3. Cài đặt truy hồi BM25 (thuật toán xếp hạng văn bản theo từ khóa) có lọc theo sản phẩm, và báo recall@k (tỷ lệ phát biểu mà k đoạn đứng đầu chứa trọn ít nhất một bộ bằng chứng chuẩn) kèm số đoạn ứng viên N và k_eff = min(k, N).',
    8: 'M4. Cài đặt P: LLM trích hồ sơ JSON, Python quyết định bằng A–B–C (A: đúng sản phẩm/phiên bản/bộ phận/thuộc tính; B: đúng điều kiện áp dụng; C: xung đột, so sánh kiểu giá trị, tổng hợp nhãn), có kiểm thử đơn vị cho các ca biên.',
    9: 'M5. So sánh P với B1 (LLM nhận cùng hồ sơ JSON và cùng hướng dẫn rồi tự gán nhãn) và B0 (LLM đọc trực tiếp đoạn nguồn) trên tập test chia theo họ; báo FAR, Recall Supported, mẫu số nguyên và phân tích lỗi. Phần tùy chọn (chỉ làm khi MVP xong): ablation P−A(bộ phận), P−B; thiết lập chẩn đoán E1/E2; truy hồi không lọc; tách phát biểu tự động; website minh họa.',
    10: 'Phạm vi: Phát biểu về thời lượng pin, thời gian sạc, khối lượng, chống ồn và phiên bản Bluetooth trong quảng cáo tiếng Việt do LLM tạo. Nguồn bằng chứng là tài liệu văn bản chính thức của hãng (trang thông số, hướng dẫn sử dụng, trang hỗ trợ/PDF) cho đúng sản phẩm, phiên bản và thị trường; ưu tiên trang Việt Nam, chấp nhận trang tiếng Anh chính thức có ghi thị trường. Mục tiêu có ít nhất một hãng ngoài Apple trong 12 họ để tránh kết luận chỉ đúng với cách trình bày của một hãng; danh sách họ chốt ở Gate 2 ' + D + '.',
    13: 'Đối tượng: Bài toán kiểm chứng phát biểu thông số có điều kiện (ví dụ “40 giờ khi tắt chống ồn”) và bộ quyết định A–B–C, trong đó mỗi kết luận gắn với provenance của bằng chứng: sản phẩm, phiên bản, thị trường, bộ phận, loại giá trị và điều kiện áp dụng.',
    16: 'Đóng góp dự kiến (giới hạn, có thể kiểm tra): \n(C1) Bộ dữ liệu nhỏ quảng cáo tai nghe tiếng Việt do LLM sinh, có log sinh, nhãn ba lớp, bộ bằng chứng chuẩn, search_log cho NEI, tách riêng nhóm sinh thông thường (ordinary_llm) và nhóm biến thể có kiểm soát (controlled_variant). \n(C2) Đặc tả và cài đặt có kiểm thử cho việc so sánh kiểu giá trị (chính xác, cận trên/dưới, khoảng, gần đúng, mức tối đa công bố, phiên bản) và kế thừa điều kiện thử (inherit_headline); trong [1]–[11] đã đọc chưa thấy đặc tả tương đương cho miền thông số sản phẩm — đây là nhận định trong phạm vi đã đọc, không phải khẳng định “đầu tiên”. \n(C3) Thực nghiệm có kiểm soát P so với B1 trên cùng hồ sơ để tách tác động của bước quyết định, báo cả kết quả âm. Không nhận là đóng góp: việc dùng Python thay LLM để ra nhãn (đã có ở [1], [5]).',
    17: 'Tham khảo [3] về suy luận số, [4] về lý do bám nguồn, [5] về xung đột; FEVER [7], AVeriTeC [8], ViFactCheck [9], ViWikiFC [10], ViNumFCR [11] cho bối cảnh nhãn, bằng chứng và tiếng Việt. \nRQ1: Với nguồn đã lọc theo sản phẩm, BM25 tìm trọn bộ bằng chứng đến đâu? Báo recall@k tổng thể và riêng nhóm N > k. \nRQ2: Lỗi của B0/B1/P đến từ truy hồi, trích xuất hay quyết định? Mã hóa lỗi trên mẫu chọn trước. \nRQ3 (thăm dò): P thay đổi FAR và Recall Supported so với B1 thế nào trên test 4 họ? Báo chênh lệch, số đếm, kết quả từng họ, bỏ từng họ và khoảng cluster bootstrap (lấy mẫu lại theo cả họ); không tuyên bố ý nghĩa thống kê.',
    19: 'Quy mô ' + D + ': MVP cam kết 120 phát biểu / 12 họ, chia dev/val/test = 6/2/4. Mục tiêu 180 / 18 họ (7/4/7) chỉ khi năng suất đo ở lô 0 và pilot cho phép (công thức trong docs/KE_HOACH_CHI_TIET_SINH_VIEN.md). Mức 300 không nằm trong kế hoạch học kỳ này. Họ sản phẩm là một dòng mẫu và các phiên bản gần nhau, không phải cả hãng; mẫu cha và biến thể luôn cùng họ, cùng tập.',
    20: 'Hai nhóm dữ liệu được lưu và báo riêng: ordinary_llm (sinh từ yêu cầu quảng cáo thông thường, giữ quảng cáo thô, SHA-256, prompt đã render, nhà cung cấp, mã mô hình trả về, tham số sinh, thời điểm) và controlled_variant (sửa giá trị, phiên bản, bộ phận hoặc điều kiện từ mẫu cha, có ghi thao tác). Thu theo lô với tiêu chí dừng chốt trước, chỉ đọc số đếm nhãn; nhóm ordinary_llm chiếm tối thiểu 50% mỗi tập. EX-01–23 hiện có chỉ là ca minh họa/kiểm thử, không tính vào dữ liệu chính.',
    24: 'Kiểm tra nhãn: một hướng dẫn nhãn chung cho người gán, B0, B1 và P, khóa phiên bản trước val/test; người gán chính không xem dự đoán. Người thứ hai gán độc lập 30 phát biểu chọn trước theo nhãn sơ bộ, nhóm và họ, không thấy nhãn đầu, dự đoán hay code P; báo tỷ lệ đồng thuận và Cohen’s kappa (đồng thuận hai người sau khi trừ phần trùng do ngẫu nhiên) trước hòa giải. Tự gán lại 20% sau 1–2 tuần chỉ đo tự nhất quán. Người thứ hai: [SINH VIÊN ĐIỀN: họ tên, ngày nhận việc]; nếu không có, báo thiếu và hạ mức kết luận ' + D + '.',
    25: 'Chia theo họ: 12 họ dùng 6/2/4; 18 họ dùng 7/4/7. Pilot đúng 6 họ, toàn bộ ở dev. Chọn mô hình/prompt/k trên dev; val audit một lượt sau khi khóa; test không dùng để chỉnh. Báo số mẫu từng nhãn theo tập và nhóm; với test nhỏ, mọi tỷ lệ đi kèm tử số/mẫu số.',
    29: 'Thử k = 3, 5, 8 trên dev; chọn k nhỏ nhất đạt mức recall ghi trước, nếu không mức nào đạt thì chọn recall cao nhất. Với mỗi phát biểu lưu N (số đoạn ứng viên sau lọc sản phẩm) và k_eff = min(k, N); báo min/trung vị/max N và recall@k riêng nhóm N > k, vì khi N ≤ k hệ thống lấy hết đoạn nên recall cao không chứng tỏ xếp hạng tốt. Lọc theo sản phẩm là giả định thuận lợi; nêu rõ trong giới hạn.',
    32: 'B kiểm tra điều kiện thiết yếu (chế độ chống ồn, âm lượng, chu kỳ thử…). Luật inherit_headline ' + D + ': phát biểu không nêu điều kiện mà nguồn công bố kèm thì kế thừa điều kiện thử của chính thông số đó; điều kiện phát biểu nêu rõ vẫn phải khớp; phát biểu “luôn/mọi chế độ” không kế thừa; còn từ hai chế độ khác giá trị → NEI-thiếu. Lý do: đọc nghĩa đen làm 11/23 câu ví dụ gốc đổi nhãn sang NEI (tests/test_abc.py), trong khi quảng cáo LLM thật hiếm khi ghi điều kiện thử.',
    40: 'Thiết lập: E3 (bằng chứng BM25 + hồ sơ LLM trích) là thực nghiệm chính bắt buộc. E1 (bằng chứng và hồ sơ kiểm thủ công) và E2 (bằng chứng chuẩn + hồ sơ LLM) là chẩn đoán tùy chọn. B0 đọc văn bản nguồn; B1 và P dùng chung một hồ sơ và một mã băm trong mỗi lượt.',
    44: 'Giả thuyết định hướng (chốt trước test): P giảm FAR so với B1 mà Recall Supported không giảm quá 5 điểm phần trăm. FAR = (Refuted→Supported + NEI→Supported) / (n_Refuted + n_NEI); Recall Supported = Supported→Supported / n_Supported. Đây là ngưỡng đánh đổi thực hành, không phải kiểm định; với n_Supported khoảng 10, một lỗi đã làm Recall đổi 10 điểm.',
    45: 'RQ3 ở mức thăm dò: báo ΔFAR, ΔRecall, tử số/mẫu số, kết quả từng họ, bỏ lần lượt từng họ và khoảng cluster bootstrap 95%. Mô phỏng scripts/simulate_power.py (giả định, không phải số đo) cho thấy với 4 họ test và 20 phát biểu R+NEI, khoảng này chỉ loại được 0 trong khoảng một phần ba số lần; vì vậy không tuyên bố “P tốt hơn có ý nghĩa thống kê”. Nếu năng suất cho phép, nâng R+NEI của test lên ≥ 40. Báo bảng toàn test và bảng riêng ordinary_llm / controlled_variant; mẫu số 0 ghi NA, mẫu số dưới 10 gắn “ít mẫu”.',
    47: 'Đánh giá recall@k trên các phát biểu có bộ bằng chứng chuẩn; NEI-thiếu không tự tính là truy hồi đúng. NEI-thiếu là kết luận có điều kiện theo kho nguồn đã khóa: mỗi ca có search_log ghi loại nguồn đã rà, từ khóa Việt–Anh, URL, trạng thái truy cập; không viết “hãng không công bố” khi chỉ là chưa tìm thấy.',
    49: 'Ghi thời gian, số lần gọi LLM, token và chi phí; chạy 3 lượt trên min(30, n_test) phát biểu chọn trước bằng seed để ước lượng dao động, lượt 1 là bảng chính. Lưu run_manifest: nhà cung cấp, mã mô hình yêu cầu/trả về, tham số sinh, thời điểm; không lưu khóa API. Tên “Llama” giống nhau ở hai nhà cung cấp không chứng minh cùng cấu hình.',
    51: 'Kết quả mong đợi: \nMVP bắt buộc: dữ liệu 120 phát biểu / 12 họ có provenance và nhãn; hướng dẫn nhãn có phiên bản; người thứ hai gán 30 phát biểu (hoặc báo thiếu); BM25 có N, k_eff; trích xuất JSON; B0/B1/P chạy được; bảng E3 trên test; phân tích lỗi; gói tái lập. Mọi số lượng thực tế và phần chưa đạt được báo đúng.',
    53: 'B0, B1 và P chạy trên cùng phát biểu, cùng hướng dẫn và cùng giao thức E3 là bắt buộc. P−A(bộ phận), P−B, E1/E2, truy hồi không lọc, tách tự động và website là tùy chọn, chỉ bắt đầu sau Gate 4.',
    54: 'Báo cáo thực nghiệm mô tả P thay đổi FAR và Recall Supported so với B1/B0 thế nào, gồm cả trường hợp không cải thiện hoặc đánh đổi. Kết luận chỉ áp dụng cho phát biểu đã tách thủ công, kho nguồn đã khóa và các họ đã chọn; không phải đánh giá end-to-end.',
    57: 'Kế hoạch thực hiện ' + D + ': Một sinh viên thực hiện toàn bộ; lịch xây cho hai mức 12 giờ/tuần (cam kết MVP) và 20 giờ/tuần (có thể làm mục tiêu 180 và phần tùy chọn). Hạn nộp khóa luận HK1 2026–2027 chưa được Khoa công bố tại thời điểm soạn; kế hoạch lấy mốc 31/12/2026 theo thời gian thực hiện đã đăng ký và sẽ dời theo thông báo chính thức. \nTháng 09/2026 (15–30/09): khảo sát [1]–[6], thiết kế dữ liệu và hướng dẫn nhãn sơ bộ.',
    59: 'Sau 30/09 (ghi riêng, không tính là kết quả tháng 9): EX-01–20 được kiểm lại nguồn và chụp ngày 08/10; EX-21–23 là ca xung đột giả lập do AI soạn để kiểm thử; đặc tả A–B–C, hướng dẫn nhãn v1, mẫu log và 27 kiểm thử đơn vị được soạn với AI hỗ trợ. Nguồn gốc sinh của 20 câu cũ chưa xác định nên không dùng làm dữ liệu LLM.',
    60: 'Chưa có log chạy LLM đến 30/09. Hướng đã chọn: Llama qua API của một nhà cung cấp [SINH VIÊN ĐIỀN: tên nhà cung cấp, mã mô hình, ngân sách tối đa]; máy cá nhân chỉ chạy BM25 và Python.',
    61: 'Gate 1 (08–31/10): môi trường và lô 0 \nThu hồi khóa API cũ, tạo khóa mới; chọn nhà cung cấp và mô hình Llama; thử trích xuất JSON trên 5 ví dụ. Soạn prompt sinh quảng cáo có log và chạy lô 0: 2 họ dev × 5 quảng cáo ordinary_llm.',
    62: 'Tách và gán nhãn thủ công các phát biểu của lô 0, bấm giờ từng phát biểu để đo năng suất thật; lưu nguồn, snapshot, mã đoạn và search_log cho NEI. Chốt với GVHD các quyết định D1–D12 (inherit_headline, nguồn Moldova, hãng ngoài Apple, nhà cung cấp, quy mô).',
    63: 'Khóa hướng dẫn nhãn v1 (mã băm) trên ca dev; mời người gán thứ hai trước 20/10. Ca xung đột giả lập chỉ dùng kiểm thử.',
    64: 'Đầu ra Gate 1 (31/10): log lô 0 (quảng cáo thô, prompt, mô hình), số phát biểu kiểm chứng được mỗi quảng cáo, phút gán nhãn/phát biểu, hướng dẫn nhãn v1, tình trạng người thứ hai, biên bản quyết định với GVHD. Nếu chưa có API chạy được đến 24/10: báo GVHD ngay, dùng nhà cung cấp dự phòng.',
    65: 'Gate 2 (01–14/11): pilot và chương trình tối thiểu \nPilot đúng 6 họ dev, 45–60 phát biểu. Chia đoạn, BM25 lọc sản phẩm, thử k = 3, 5, 8, báo recall@k, N và k_eff theo họ.',
    66: 'Chạy được B0 và P tối thiểu: phát biểu → bằng chứng → JSON → nhãn và dấu vết; lỗi kỹ thuật ghi riêng, không đổi thành NEI.',
    67: 'Đầu ra Gate 2 (14/11): quyết định quy mô theo công thức năng suất — giữ 120/12 (6/2/4) hoặc nâng 180/18 (7/4/7); danh sách họ và chia tập; dự toán chi phí API. Nếu dự phóng không kịp 120 phát biểu trước 04/12: thu hẹp phần tùy chọn trước, báo GVHD.',
    68: 'Gate 3 (15/11–04/12): hoàn thiện dữ liệu và ba bản chính \nThu và gán nhãn đủ quy mô theo lô; giữ ordinary_llm ≥ 50%; bổ sung controlled_variant khi một nhãn thiếu theo tiêu chí dừng đã chốt.',
    69: 'Người thứ hai gán độc lập 30 phát biểu; tính đồng thuận và kappa trước hòa giải; tự gán lại 20% sau 1–2 tuần. Hoàn tất search_log cho mọi NEI.',
    70: 'Hoàn thiện trích xuất JSON (sản phẩm, phiên bản, bộ phận, thuộc tính, loại giá trị, giá trị, đơn vị, điều kiện, mã đoạn); kiểm thủ công một mẫu hồ sơ để phát hiện trường thiếu hoặc bịa.',
    71: 'Chuẩn hóa đơn vị chỉ khi cùng đại lượng; Bluetooth là chuỗi phiên bản; dung sai mặc định 0, chỉ nới khi nguồn nêu sai số.',
    72: 'A: đúng sản phẩm, phiên bản, thị trường, bộ phận, thuộc tính; lưu lý do loại nguồn.',
    73: 'B: điều kiện thiết yếu và luật inherit_headline đã chốt ở Gate 1; kiểm thử ca ANC bật/tắt, “luôn/mọi chế độ”.',
    74: 'C1–C2–C3: kiểm thử =, >, ≥, ≤, khoảng, gần đúng, mức tối đa công bố, phiên bản (đã có 27 kiểm thử đơn vị, bổ sung khi luật thay đổi).',
    75: 'P chạy bằng dòng lệnh/notebook tái lập được; website không thuộc MVP.',
    76: 'B1 dùng cùng hồ sơ và cùng hướng dẫn như P nhưng để LLM ra nhãn, không nhận nhãn hay dấu vết của P. Đầu ra Gate 3 (04/12): dữ liệu đã kiểm, bản chia tập, B0/B1/P chạy được trên dev.',
    77: 'Gate 4 (05–11/12): khóa giao thức \nKhóa mô hình, prompt, k, hướng dẫn nhãn, dữ liệu bằng mã băm; chọn trước danh sách 30 phát biểu cho 3 lượt chạy lặp và mẫu phân tích lỗi. Val chạy một lượt để kiểm tra, không chỉnh theo điểm.',
    78: 'B0/B1/P dùng cùng phát biểu, top-k và mô hình; quy định trước cách xử lý lỗi kỹ thuật, cache, thử lại và ngân sách.',
    79: 'Đầu ra Gate 4 (11/12): giao thức có mã băm, danh sách mẫu, smoke test trên dev/val. Viết song song chương mở đầu, liên quan và phương pháp từ đầu tháng 11.',
    80: 'Gate 5 (12–21/12): thực nghiệm chính \nChạy B0/B1/P ở E3 trên test đã khóa; lượt 2 và 3 trên 30 phát biểu đã chọn. Phần tùy chọn chỉ chạy khi đã chọn ở Gate 4.',
    81: 'Tính FAR, Recall Supported, Precision/Recall/F1 từng nhãn, Macro-F1, ma trận nhầm lẫn, cluster bootstrap theo họ; bảng toàn test, ordinary_llm và controlled_variant; tử số/mẫu số nguyên.',
    82: 'Đo recall@k với k đã khóa, kèm N và k_eff; tách NEI do BM25 bỏ sót với NEI đúng theo kho nguồn.',
    83: 'Phân tích lỗi trên mẫu đã chọn trước: sai sản phẩm, phiên bản, bộ phận, loại giá trị, điều kiện, thiếu hoặc xung đột nguồn; quy về truy hồi, trích xuất hay quyết định.',
    84: 'Đầu ra Gate 5 (21/12): bảng B0/B1/P, dự đoán và log gốc, kết quả từng họ, 3 lượt, lỗi kỹ thuật. RQ3 chỉ báo xu hướng thăm dò.',
    85: 'Nếu có website hoặc tách tự động, đánh giá riêng; không thay thực nghiệm trên test.',
    86: 'Gate 6 (22–31/12): hoàn thiện luận văn và bàn giao \nHoàn thiện chương kết quả, thảo luận, giới hạn; khai báo AI hỗ trợ; đóng gói mã, dữ liệu được phép chia sẻ, README, cấu hình chạy lại; slide bảo vệ.',
    87: 'Sau 21/12 không thêm phương pháp mới, không chỉnh luật theo nhãn test. Sửa lỗi phần mềm phải ghi phiên bản, lý do và chạy lại đồng bộ.',
    88: 'Rủi ro và hành động (mốc quản lý, chưa phải kết quả) \nAPI/nhà cung cấp: đến 24/10 chưa chạy được → nhà cung cấp dự phòng, báo GVHD. Tỷ lệ JSON lỗi > 5% trên lô 20 mẫu sau một lần thử lại → sửa schema/prompt, chưa mở rộng dữ liệu. Năng suất gán nhãn thấp hơn dự kiến → giữ 120/12, bỏ phần tùy chọn.',
    89: 'Không tìm được người thứ hai đến 31/10 → hỏi GVHD giới thiệu; nếu vẫn không có, báo thiếu, chỉ có tự nhất quán, hạ mức kết luận về nhãn. Tự đồng thuận < 80% → rà hướng dẫn trước khi khóa. Nguồn hãng ngoài Apple không truy cập/lưu được → ghi lý do, giữ Apple và nêu giới hạn tổng quát hóa.',
    90: 'Đến 04/12 dữ liệu hoặc ba bản chính chưa đạt → bỏ toàn bộ phần tùy chọn, giữ MVP; vẫn thiếu → báo phần thiếu với GVHD, không tạo mẫu gần trùng hay bịa kết quả. P không tốt hơn B1 vẫn là kết quả hợp lệ cần phân tích.',
}

PAPER_TABLES = {3: 2, 4: 3, 5: 4, 6: 5}  # chỉ số bảng → số bài
CHECK_NOTE = ' (Số liệu được trích với AI hỗ trợ; sinh viên tự kiểm trên PDF gốc: [SINH VIÊN ĐIỀN: ngày, kết quả].)'

AI_DECLARATION = ('Phần tổng hợp/đối chiếu và biên tập trong bản cập nhật tháng 10 có công cụ AI hỗ trợ; các ca xung đột '
                  'EX-21–23 do AI soạn để minh họa. Các nguồn gốc được dẫn riêng. Sinh viên cần tự kiểm tra nguồn và chịu '
                  'trách nhiệm nội dung; tình trạng xác nhận thủ công: [SINH VIÊN ĐIỀN: phần đã tự kiểm, ngày].')

REPORT_PARAS = {
    10: 'Thời gian thực hiện bắt đầu từ 15/09/2026. Mốc chốt minh chứng: 30/09/2026. Mục 2–4 chỉ ghi “hoàn thành trong kỳ” khi có bản lưu hoặc nhật ký đến 30/09; việc làm sau 30/09 được ghi rõ là “sau kỳ”. Ngày nộp báo cáo: [SINH VIÊN ĐIỀN].',
    29: 'Đọc thêm (sau kỳ): FEVER [7] về ba nhãn và bộ bằng chứng; AVeriTeC [8] về nguồn web và rò rỉ thời gian; ViFactCheck [9], ViWikiFC [10], ViNumFCR [11] về kiểm chứng tiếng Việt và số liệu. Các bài này dùng làm bối cảnh, không tái tạo hệ thống.',
    56: 'Bộ minh họa có 23 ví dụ (sau kỳ, không phải minh chứng hoàn thành tháng 9): EX-01–20 kế thừa bản thảo, nguồn Apple được kiểm lại và lưu ảnh, văn bản, mã băm ngày 08/10/2026; EX-21–23 là ca xung đột giả lập do AI soạn. Mỗi bảng tách câu gốc và câu rà soát. Nhãn ghi trong bảng áp cho câu rà soát; câu gốc giữ cùng nhãn nếu GVHD chấp nhận luật inherit_headline (dự thảo), trừ EX-13–15 phụ thuộc quyết định về nguồn thị trường Moldova. Nguồn gốc sinh của 20 câu cũ chưa xác định nên chưa dùng làm dữ liệu LLM.',
    98: 'Đến 30/09/2026 chưa có cấu hình máy, mã thử hay log chạy LLM được lưu; mục này chưa hoàn thành trong kỳ.',
    99: 'Sau kỳ, hướng chạy đã chọn là Llama qua API: nhà cung cấp [SINH VIÊN ĐIỀN], mã mô hình [SINH VIÊN ĐIỀN], ngân sách tối đa [SINH VIÊN ĐIỀN]; máy cá nhân [SINH VIÊN ĐIỀN: CPU/RAM/hệ điều hành] chỉ chạy BM25 và Python. Mỗi lần gọi lưu run_manifest (nhà cung cấp, mô hình trả về, tham số, thời điểm), không lưu khóa API.',
    100: 'Việc thử trích xuất trên 5 ví dụ và lô 0 sinh quảng cáo nằm trong Gate 1 tháng 10 (xem mục 5).',
    102: 'Trạng thái dùng ba mức: hoàn thành trong kỳ (có minh chứng đến 30/09), có trong bản thảo nhưng chưa xác nhận ngày, và thực hiện sau kỳ.',
    104: 'Vấn đề phương pháp phát hiện khi soạn ví dụ: (1) câu quảng cáo thường không nêu điều kiện thử, nếu đọc nghĩa đen thì 11/23 câu gốc chuyển sang NEI — đề xuất luật inherit_headline; (2) EX-13–15 dùng trang Apple thị trường Moldova; (3) tập test dự kiến nhỏ nên RQ3 chỉ thăm dò. Các điểm này đã đưa vào đề cương điều chỉnh, chờ GVHD xác nhận.',
    105: 'Khó khăn thực tế trong kỳ: [SINH VIÊN ĐIỀN: đầu việc bị vướng, nguyên nhân, ảnh hưởng, nội dung cần giảng viên hỗ trợ].',
    107: 'Tháng 10 theo Gate 1 của đề cương điều chỉnh (chờ GVHD xác nhận). Các số dưới đây là kế hoạch, chưa phải kết quả.',
    108: 'Gate 1 (08–31/10): thu hồi khóa API cũ; chọn nhà cung cấp và mô hình Llama; thử trích xuất JSON trên 5 ví dụ; chạy lô 0 gồm 2 họ × 5 quảng cáo ordinary_llm, lưu quảng cáo thô, prompt và log; tách, gán nhãn và bấm giờ; khóa hướng dẫn nhãn v1; mời người gán độc lập 30 phát biểu trước 20/10; ghi search_log cho NEI.',
    109: 'Đầu ra 31/10: log lô 0, số phát biểu/quảng cáo, phút gán nhãn/phát biểu, chi phí mỗi lần gọi, biên bản chốt quyết định với GVHD (luật điều kiện thử, nguồn Moldova, hãng ngoài Apple, quy mô).',
    110: 'Gate 2 (01–14/11): pilot đúng 6 họ dev (45–60 phát biểu); BM25 lọc sản phẩm với k = 3, 5, 8, báo recall@k kèm N và k_eff; chạy B0 và P tối thiểu; quyết định quy mô.',
    111: 'Quy mô cam kết 120 phát biểu / 12 họ (6/2/4), nhóm sinh thông thường ≥ 50%; 180/18 (7/4/7) chỉ khi năng suất đo được cho phép. RQ3 ở mức thăm dò; thực nghiệm chính chạy 3 lượt trên 30 phát biểu để xem dao động.',
    112: 'Các mốc sau: Gate 3 (15/11–04/12) dữ liệu và B1; Gate 4 (05–11/12) khóa giao thức; Gate 5 (12–21/12) thực nghiệm; Gate 6 (22–31/12) viết và bàn giao. Đánh giá trên phát biểu đã tách thủ công, không trên quảng cáo thô.',
    113: 'Chưa có kết quả so sánh P với B0/B1.',
    126: 'KHAI BÁO SỬ DỤNG CÔNG CỤ AI',
    127: AI_DECLARATION,
}
REPORT_DROP = range(128, 134)

T31 = {
    1: 'Có trong bản thảo, chưa xác nhận ngày: tổng hợp sáu bài [1]–[6]. Số liệu từng bài đã đối chiếu lại sau kỳ; sinh viên tự kiểm PDF gốc [SINH VIÊN ĐIỀN: ngày].',
    2: 'Có trong bản thảo, chưa xác nhận ngày: tiêu chí nguồn, cấu trúc dữ liệu, ba nhãn. Hướng dẫn nhãn có phiên bản được khóa ở Gate 1.',
    3: 'Sau kỳ: 23 ví dụ (20 kiểm nguồn ngày 08/10, 3 giả lập). Chưa tính là dữ liệu LLM.',
    4: 'Chưa hoàn thành trong kỳ: chưa có log LLM. Chuyển sang Gate 1 tháng 10.',
}

DRIFT_ORIGINAL = {'EX-04', 'EX-06', 'EX-09', 'EX-11', 'EX-12', 'EX-17', 'EX-18', 'EX-19'}
MARKET = {'EX-13', 'EX-14', 'EX-15'}


def replace_para(p, value, red=True):
    p.parentNode.replaceChild(paragraph(p, value, red=red), p)


def append_red(cell, value):
    cell.appendChild(paragraph(children(cell, 'w:p')[-1], value, red=True, new=True))


def redesign_proposal(doc):
    ps = children(body(doc), 'w:p')
    assert text(ps[3]).startswith('Bản rà soát ngày 08/10/2026'), text(ps[3])
    replace_para(ps[3], PROPOSAL_HEADER)
    table = children(body(doc), 'w:tbl')[1]
    for row, value in PROPOSAL_ROWS.items():
        assert row != 97
        set_cell(cell_at(table, row), value, red=True)


def report_sections(doc):
    """Đoạn văn cấp body theo thứ tự (cùng cách đánh số với bản dump)."""
    return children(body(doc), 'w:p')


def redesign_report(doc):
    ps = report_sections(doc)
    assert text(ps[126]) == 'Hồ sơ sử dụng để lập báo cáo', text(ps[126])
    assert text(ps[97]).startswith('3.4.')
    tables = children(body(doc), 'w:tbl')
    for idx in PAPER_TABLES:
        cell = cell_at(tables[idx], 3, 1)
        value = text(cell)
        assert value.startswith('Đã đối chiếu báo/'), value[:40]
        set_cell(cell, 'Theo báo/' + value[len('Đã đối chiếu báo/'):] + CHECK_NOTE, red=True)
    for row, value in T31.items():
        set_cell(cell_at(tables[31], row, 1), value, red=True)
    examples = json.loads((ROOT / 'evidence/2026-10-08/examples.json').read_text())['examples']
    for table, e in zip(tables[8:31], examples):
        if e['id'] in DRIFT_ORIGINAL:
            append_red(cell_at(table, 9, 1), 'Câu gốc: cùng nhãn nếu áp luật inherit_headline (dự thảo); đọc nghĩa đen điều kiện thử thì câu gốc là NEI-thiếu.')
        elif e['id'] in MARKET:
            append_red(cell_at(table, 9, 1), 'Câu gốc: nguồn là trang thị trường Moldova; nếu chỉ chấp nhận nguồn Việt Nam thì câu gốc là NEI-thiếu (chờ GVHD quyết định).')
    for i, value in REPORT_PARAS.items():
        replace_para(ps[i], value)
    for i in REPORT_DROP:
        ps[i].parentNode.removeChild(ps[i])


def check(name, before, after):
    with ZipFile(io.BytesIO(before)) as z0, ZipFile(io.BytesIO(after)) as z1:
        assert z1.testzip() is None, 'CRC'
        assert z0.namelist() == z1.namelist()
        for part in z0.namelist():
            if part != 'word/document.xml':
                assert z0.read(part) == z1.read(part), part
            if part.endswith(('.xml', '.rels')):
                minidom.parseString(z1.read(part))
        d0, d1 = (minidom.parseString(z.read('word/document.xml')) for z in (z0, z1))
    assert structure(d0) == structure(d1), 'số bảng/hàng/ô thay đổi'
    for tag in ('w:sectPr', 'w:drawing', 'w:pict', 'w:tblPr', 'w:tblGrid', 'w:trPr', 'w:tcPr'):
        assert [n.toxml() for n in d0.getElementsByTagName(tag)] == [n.toxml() for n in d1.getElementsByTagName(tag)], tag
    if name == PROPOSAL:
        r0, r1 = (children(children(body(d), 'w:tbl')[1], 'w:tr')[97].toxml() for d in (d0, d1))
        assert r0 == r1, 'hàng chữ ký bị đổi'
    validate_content(name, d1)
    return [len(t) for t in structure(d1)]


def build(path, fn):
    src = path.read_bytes()
    with ZipFile(io.BytesIO(src)) as z:
        doc = minidom.parseString(z.read('word/document.xml'))
        if HEADER in text(doc) or 'KHAI BÁO SỬ DỤNG CÔNG CỤ AI' in text(doc):
            raise SystemExit(f'{path.name}: đã thiết kế lại trước đó, dừng để tránh sửa hai lần')
        fn(doc)
        out = io.BytesIO()
        with ZipFile(out, 'w') as t:
            for e in z.infolist():
                t.writestr(e, doc.toxml(encoding='UTF-8') if e.filename == 'word/document.xml' else z.read(e.filename))
    return src, out.getvalue()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    results = []
    for name, fn in ((PROPOSAL, redesign_proposal), (REPORT, redesign_report)):
        src, new = build(ROOT / name, fn)
        rows = check(name, src, new)
        print(f'PASS: {name} — số hàng mỗi bảng {rows}, {len(src):,} → {len(new):,} byte')
        results.append((ROOT / name, new))
    if args.apply:
        for path, data in results:
            path.write_bytes(data)
        print('Đã ghi hai docx.')
    else:
        print('Xem trước. Dùng --apply để ghi.')


if __name__ == '__main__':
    main()
