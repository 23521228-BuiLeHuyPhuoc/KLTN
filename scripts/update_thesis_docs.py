#!/usr/bin/env python3
"""Apply the 2026-10-08 thesis handoff, preserving the original DOCX packages.

Uses the Python standard library only. Default: preview; --apply: back up and
update; --check: validate the updated documents without writing anything.
Backups and the revision manifest live in the already ignored scratch_test/.
"""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
from xml.dom import Node, minidom
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "scratch_test" / "docx-review-2026-10-08"
REPORT = "Đọc_báo_cùng_HuP_3_.docx"
PROPOSAL = "Đọc_báo_cùng_HuP_4_.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

REFERENCES = [
    '[7] J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, “FEVER: a Large-scale Dataset for Fact Extraction and VERification,” NAACL-HLT, 2018, pp. 809–819. https://aclanthology.org/N18-1074/',
    '[8] M. Schlichtkrull, Z. Guo, and A. Vlachos, “AVeriTeC: A Dataset for Real-world Claim Verification with Evidence from the Web,” NeurIPS, Datasets and Benchmarks, 2023. https://arxiv.org/abs/2305.13117',
    '[9] Tran Thai Hoa et al., “ViFactCheck: A New Benchmark Dataset and Methods for Multi-domain News Fact-Checking in Vietnamese,” arXiv:2412.15308, 2024 (accepted at AAAI 2025). https://arxiv.org/abs/2412.15308',
    '[10] Hung Tuan Le et al., “ViWikiFC: Fact-Checking for Vietnamese Wikipedia-Based Textual Knowledge Source,” arXiv:2405.07615, v1: 13/05/2024; v2: 16/03/2026. https://arxiv.org/abs/2405.07615v2',
    '[11] Nhi Ngoc-Phuong Luong et al., “ViNumFCR: A Novel Vietnamese Benchmark for Numerical Reasoning Fact Checking on Social Media News,” INLG, 2025, pp. 134–147. https://aclanthology.org/2025.inlg-main.9/',
]

# Real XML row positions, counted from zero. Rows 0–96 are merged cells, not
# duplicate physical columns. The final signature row has two distinct cells.
PROPOSAL_ROWS = {
    4: 'Nội dung đề tài: Nghiên cứu phương pháp kiểm chứng phát biểu trong quảng cáo tai nghe không dây tiếng Việt do LLM tạo, dựa trên tài liệu văn bản chính thức. Thực nghiệm chính nhận phát biểu đã tách/rà soát thủ công và định danh sản phẩm được cung cấp; đánh giá truy hồi, trích xuất và quyết định nhãn Supported/Refuted/NEI. Không coi đây là đánh giá toàn trình từ quảng cáo thô; tách tự động và website chỉ là mở rộng nếu được triển khai, đo riêng.',
    5: 'Mục tiêu: Thu quảng cáo LLM có log và tài liệu tham chiếu để xây dựng dữ liệu kiểm chứng ở mức phát biểu đã tách, giữ liên kết với quảng cáo gốc. Không tự sửa nội dung claim sinh thông thường để khớp nguồn; thay đổi ý nghĩa/điều kiện phải ghi thành biến thể có kiểm soát.',
    6: 'Thiết lập quy trình tách/rà soát thủ công giữ nguyên nghĩa, chủ thể và điều kiện. Dùng cùng tập claim này cho B0/B1/P; không quy kết lỗi hoặc thành công của bước tách tự động khi chưa đánh giá bước đó. Kết quả chính chỉ phản ánh kiểm chứng claim đã tách.',
    9: 'So sánh P với B0 (LLM đọc văn bản bằng chứng) và B1 (LLM đọc hồ sơ trích xuất/chuẩn hóa). B0/B1 nhận đầy đủ cùng hướng dẫn nhãn bằng lời; P hiện thực tiêu chí ấy bằng code. P–B1 trên hồ sơ chung là so sánh cách ra quyết định; P–B0 còn khác biểu diễn đầu vào nên không cô lập riêng tác động luật cứng. Không suy từ kết quả này ra khả năng xử lý toàn bộ quảng cáo thô.',
    10: 'Phạm vi: kiểm chứng claim tiếng Việt đã tách/rà soát thủ công về pin, sạc, khối lượng, chống ồn và Bluetooth của tai nghe không dây. Thực nghiệm chính được cung cấp đúng định danh sản phẩm trước truy hồi; nguồn chính thức Việt/Anh đúng phiên bản/thị trường. Không đánh giá nhận diện sản phẩm từ quảng cáo thô, tách tự động hoặc trải nghiệm website trong kết quả chính.',
    13: 'Đối tượng: Khung gán nhãn và phương pháp kiểm chứng phát biểu quảng cáo tai nghe không dây tiếng Việt, gắn từng kết luận với nguồn gốc bằng chứng (provenance), đúng sản phẩm, phiên bản, thị trường, bộ phận, loại giá trị và điều kiện áp dụng.',
    16: 'Đóng góp dự kiến gồm: (1) bộ dữ liệu quảng cáo tai nghe tiếng Việt có provenance, hướng dẫn ba nhãn và bộ bằng chứng chuẩn; (2) đặc tả đối chiếu sản phẩm–phiên bản–bộ phận–điều kiện–loại giá trị, phân biệt thiếu bằng chứng với bác bỏ trực tiếp; (3) thực nghiệm có kiểm soát để đo FAR, Recall Supported và phân tích nguồn lỗi. Việc dùng Python quyết định nhãn không tự thân là tính mới; kết quả âm vẫn được báo cáo.',
    17: 'Tham khảo [3] về suy luận số, [4] về lý do bám nguồn, [5] về xung đột. FEVER [7], AVeriTeC [8], ViFactCheck [9], ViWikiFC [10], ViNumFCR [11] cung cấp bối cảnh nhãn, bằng chứng và nghiên cứu tiếng Việt; không bắt buộc tái tạo các hệ thống này.\nRQ1: BM25 tìm đủ bộ bằng chứng đến đâu? Đo evidence-set recall@k trên mẫu có bộ bằng chứng chuẩn và phân tích bỏ sót.\nRQ2: Lỗi đến từ truy hồi, trích xuất hay quyết định? Rà soát mẫu lỗi chọn trước test; E1/E2 là mở rộng.\nRQ3 (thăm dò ở quy mô tối thiểu): P thay đổi FAR và Recall Supported so với B1 thế nào? Báo chênh lệch, kết quả từng họ và độ bất định; không đặt điều kiện toàn bộ khoảng FAR dưới 0 làm cửa đạt/rớt. Không suy ra ưu thế tổng quát từ bốn họ test.',
    19: 'Quy mô dự kiến theo ba tầng, bao gồm pilot: tối thiểu 120 phát biểu / 12 họ sản phẩm; mục tiêu 180 phát biểu / 18–20 họ; mở rộng 300 phát biểu / 30 họ chỉ khi năng suất pilot và ngân sách cho phép. Đây là mục tiêu, chưa phải dữ liệu đã thu. Họ sản phẩm gồm các mẫu, phiên bản gần nhau của cùng dòng, không phải toàn bộ một hãng; chốt danh sách họ trước khi chia tập.',
    20: 'Lưu riêng quảng cáo LLM sinh thông thường và biến thể có kiểm soát. Mẫu LLM phải có mô hình/phiên bản, prompt, thời điểm, cấu hình sinh và đầu ra gốc; biến thể cần mẫu cha và thao tác sửa. Mẫu tự viết hoặc chưa rõ nguồn gốc phải ghi đúng trạng thái, không tính là quảng cáo LLM đã xác minh. Nhãn do người đọc nguồn gán, không suy từ thao tác sửa. Các EX minh họa và ca xung đột giả lập không tự động được tính vào quy mô dữ liệu chính.',
    18: 'Thu thập dữ liệu và nhãn tham chiếu\nNgười gán đọc toàn bộ bộ nguồn đã khóa, không dùng nhãn/dấu vết P hoặc chỉ top-k làm chuẩn. Hướng dẫn nhãn là tiêu chí của tác vụ, được chốt từ nguồn và ca dev trước khi xem dự đoán test; không định nghĩa “đúng” là “trùng P”. Giữ cả ca tự nhiên khó/ngoài mẫu luật, không bỏ vì P chưa xử lý được. B0/B1 được cung cấp cùng hướng dẫn bằng lời như người gán và đặc tả P.',
    21: 'Chốt trước dự đoán các ngưỡng vận hành: mỗi nhãn Supported/Refuted/NEI có ít nhất 10 mẫu ở dev, 3 ở val và 10 ở test; nhóm LLM sinh thông thường chiếm ít nhất 50% từng tập. Đây không phải bảo đảm công suất thống kê. Giữ phân bố quan sát của nhóm thông thường, không chọn/bỏ theo nhãn để cân bằng nó; dùng nhóm biến thể riêng để tăng độ phủ. Không đạt thì báo thiếu, thu thêm theo lô đã định trước hoặc hạ mức kết luận, không đổi nhãn hay lấy họ dev sang test. Báo mẫu số và từng nhóm; mẫu số dương nhưng ít vẫn tính được, phải cảnh báo bất ổn.',
    23: 'Mỗi claim lưu nhãn, lý do và mã đoạn đủ bằng chứng. NEI-thiếu phải gắn corpus_id/version và search_log: trang thông số, hướng dẫn sử dụng, trang hỗ trợ/PDF đã kiểm (hoặc chưa tìm được/không truy cập được), từ khóa Việt–Anh, ngày, mục/chú thích, kết quả và lý do dừng. Không thấy ở top-k không đủ gán NEI; thiếu bước rà nguồn thì chưa chốt nhãn. NEI chỉ tương đối với bộ nguồn X tại thời điểm Y, không khẳng định hãng không có thông tin ở nơi khác. NEI-xung đột lưu cả hai phía.',
    24: 'Dự kiến mời một người thứ hai gán độc lập 30 claim (chưa có người/log xác nhận), chọn ngẫu nhiên có phân tầng theo nhãn sơ bộ, nhóm nguồn gốc và họ trước khi xem dự đoán; có mẫu test nếu đã có danh sách chia. Người này đọc cùng hướng dẫn và nguồn, không thấy nhãn đầu, dự đoán/code P hay thao tác tạo biến thể. Lưu hai nhãn trước hòa giải, bảng bất đồng, tỷ lệ đồng thuận và Cohen’s kappa nếu xác định, cùng lý do chốt; không lấy kết quả P phân xử. Gán lại 20% sau 1–2 tuần chỉ đo tự nhất quán. Ba mươi mẫu không chứng minh toàn bộ nhãn đúng; không tìm được người thứ hai phải báo chưa có kiểm tra độc lập.',
    25: 'Chia theo họ: 12 họ dùng dev/val/test = 6/2/4; 18 họ dùng 7/4/7; 20 họ dùng 8/4/8; 30 họ có thể dùng 12/6/12. Pilot cố định 6 họ, toàn bộ ở dev trong mọi phương án. Biến thể cùng quảng cáo và phiên bản cùng họ ở cùng tập. Chốt danh sách ở Gate 2; báo số mẫu/nhãn thực tế, không chuyển pilot sang test. Chọn cấu hình trên dev; val kiểm tra một lượt cấu hình đã khóa, không tìm kiếm mô hình/k/dung sai trên hai họ val. Các tập cần đủ ba nhãn; test không dùng chỉnh luật/prompt.',
    26: 'Quy trình xử lý và bộ quyết định A–B–C\nTách quảng cáo thành phát biểu nhỏ theo hướng FactLens [2], giữ đủ sản phẩm, bộ phận và điều kiện. MVP dùng phát biểu đã rà soát thủ công để đánh giá truy hồi, trích xuất và quyết định. Tách tự động là chức năng mở rộng, được đánh giá riêng nếu triển khai.',
    27: 'BM25 chính chạy trong nguồn của sản phẩm được định danh đúng từ trước (product-filtered); đây là truy hồi có điều kiện, không phải tìm sản phẩm/toàn web. Giữ tiêu đề, dòng bảng và chú thích khi chia đoạn. Báo cạnh recall số tài liệu, N đoạn ứng viên sau lọc/khử trùng, k_eff=min(k,N), số đoạn của bộ bằng chứng chuẩn và tỷ lệ claim có N≤k; tách kết quả N>k khỏi ca lấy hết nguồn. Nếu đủ thời gian, chạy thêm BM25 bỏ lọc trên kho nhiều sản phẩm đã khóa, giữ query/k/chunking, chỉ đánh giá truy hồi riêng; A vẫn kiểm đúng sản phẩm.',
    29: 'Thử k = 3, 5, 8 trên dev, báo evidence-set recall@k theo từng họ và chi phí; chọn k nhỏ nhất đạt mức recall mục tiêu đã ghi trước lượt so sánh, nếu không mức nào đạt thì báo thiếu và chọn recall cao nhất (hòa thì k nhỏ hơn). Không chọn lại k trên val/test. Nguồn ít hơn k đoạn thì lấy toàn bộ và báo số đoạn thực tế.',
    31: 'A kiểm tra cùng sản phẩm, phiên bản, bộ phận, thuộc tính và tính tương thích của đơn vị; không dùng pin cả hộp để xác nhận pin riêng tai nghe. Xác định loại giá trị của từng bên để C dùng phép so sánh tương ứng; không loại bằng chứng chỉ vì một bên là giá trị chính xác còn bên kia là giới hạn hoặc khoảng.',
    32: 'B kiểm tra điều kiện thiết yếu của thuộc tính và chế độ claim nêu rõ. Thiếu điều kiện thiết yếu thì UNKNOWN, không suy diễn từ nguồn vào claim. Claim nói rõ “theo thông số công bố/điều kiện thử nghiệm của hãng” được gắn condition_ref tới chú thích tương ứng; không hiểu là bảo đảm mọi cách dùng. Claim có điều kiện riêng khác nguồn vẫn phải tìm bằng chứng cùng điều kiện. Khối lượng không cần chế độ chống ồn.',
    33: 'C có bước so sánh kiểu giá trị trước khi tổng hợp: (C1) sau lọc A/B, kiểm tra xung đột nguồn cùng phạm vi chưa giải quyết → NEI-xung đột; (C2) đối chiếu từng cặp theo các luật số/phiên bản dưới đây, trả hỗ trợ, bác bỏ hoặc chưa xác định; (C3) nếu không có xung đột nguồn, có bác bỏ trực tiếp → Refuted; hỗ trợ đủ toàn bộ claim → Supported; còn lại → NEI-thiếu. Hai nguồn khác chế độ không tự tạo xung đột. Lưu dấu vết cho từng bước.',
    35: 'Luật C2 khi cùng phạm vi/điều kiện, đã đổi đơn vị: (=a) so (=b): a=b hỗ trợ, khác nhau bác bỏ; (>a) so (=b): b≤a bác bỏ, b>a chưa đủ; (>a) so (>b): a≥b hỗ trợ, a<b chưa đủ; (≤u) so (=b): b>u bác bỏ, b≤u chưa đủ. Vì thế “hơn 24” bác bỏ “chính xác 24”; “lên đến 3” không xác nhận hoặc bác bỏ “chính xác 3”.\nPhân biệt giá trị quan sát x và mức tối đa công bố M: nguồn “tối đa 20”, claim “tối đa 25” cùng nói M nên bác bỏ, không dùng phép bao hàm [0,20]⊂[0,25] để hỗ trợ. Cùng mức tối đa thì hỗ trợ. Với mệnh đề khoảng về x: miền nguồn nằm trọn miền claim → hỗ trợ, rời nhau → bác bỏ, giao một phần → chưa đủ; giữ biên đóng/mở. Gần đúng cùng biểu thức và giá trị có thể hỗ trợ; không tự đặt dung sai cho hai số khác nhau. Bluetooth so chuỗi phiên bản, không tính sai số số thực. Trường hợp mơ hồ/ngoài luật → NEI; chi tiết và ca biên: docs/QUY_TAC_ABC.md.',
    36: 'Đổi đơn vị theo phép xác định; mặc định dung sai 0 khi so thông số chính xác. Chỉ dùng dung sai nếu nguồn nêu sai số hoặc quy tắc làm tròn có căn cứ, lưu căn cứ và khóa trên dev trước val/test. Không tối ưu dung sai theo F1 hoặc nhãn val. “Khoảng” không kèm biên không được tự biến thành ±5%; cách hiểu chưa rõ → NEI.',
    38: 'B0/B1 phải nhận cùng khối hướng dẫn đầy đủ, cùng phiên bản/hash: ba nhãn, phạm vi, điều kiện, so loại giá trị, dung sai và ưu tiên NEI-xung đột; không chỉ nhắc tên A–B–C. Khối dùng chung: docs/HUONG_DAN_GAN_NHAN.md; prompt được tạo từ cùng tệp và lưu nguyên văn. Ví dụ minh họa nếu dùng chỉ lấy từ dev, không cho nhãn test hoặc thao tác tạo biến thể vào prompt/hồ sơ. B1/P dùng cùng hồ sơ dữ kiện thuần đã lưu, không chứa nhãn hoặc quan hệ hỗ trợ/bác bỏ do P tính. Khóa hướng dẫn/prompt trên dev trước val/test.',
    39: 'Phần mở rộng: P−A chỉ bỏ kiểm tra bộ phận trong A, vẫn giữ sản phẩm, phiên bản, thuộc tính, đơn vị và toàn bộ luật loại giá trị của C; ghi tên đầy đủ P−A(bộ phận). P−B bỏ kiểm tra điều kiện và yêu cầu bao phủ chế độ, giữ A và C. Chỉ kết luận về thành phần thực sự tắt; không bắt buộc hai ablation để hoàn thành MVP.',
    40: 'Các thiết lập: E3 dùng bằng chứng BM25 và hồ sơ do LLM trích, là thực nghiệm chính bắt buộc. E1 dùng bằng chứng và hồ sơ đã kiểm tra thủ công; E2 dùng bằng chứng chuẩn nhưng hồ sơ do LLM trích, là hai thiết lập chẩn đoán tùy thời gian. B0 đọc văn bản nguồn; B1 và P dùng loại hồ sơ tương ứng.',
    41: 'E3 bắt buộc chạy B0/B1/P trên cùng tập kiểm tra. Nếu làm E1/E2, chọn trước tối đa 30 phát biểu hoặc toàn bộ test nếu nhỏ hơn, trải trên nhiều họ và đủ ba nhãn khi dữ liệu cho phép; lưu danh sách trước khi xem dự đoán. Với NEI do thiếu, giữ nguồn đã rà soát và trường chưa có, không tạo thông tin để ép thành bằng chứng chuẩn. Nếu bỏ E1/E2, trả lời RQ2 bằng rà soát nguồn, hồ sơ và dấu vết quyết định; không tuyên bố đã tách được tác động nhân quả từng bước.',
    44: 'Giả thuyết định hướng: P giảm FAR so với B1 mà Recall Supported không giảm quá 5 điểm phần trăm. Đây là ngưỡng đánh đổi thực hành chốt trước test, không phải kiểm định không-thua-kém hoặc chuẩn chung. Ở mức 12 họ, chỉ mô tả xu hướng quan sát nếu ΔFAR<0 và ΔRecall≥−5 điểm; ngoài ra báo không cải thiện/đánh đổi/không xác định theo dữ liệu.',
    45: 'RQ3 ở mức tối thiểu là thăm dò: báo ΔFAR=FAR(P)−FAR(B1), ΔRecall, mẫu số, số họ và kết quả từng họ; phân tích độ nhạy bỏ lần lượt một họ. Có thể kèm khoảng bootstrap ghép cặp theo họ 95% để mô tả bất định, nhưng bốn họ không bảo đảm độ bao phủ danh nghĩa; không dùng khoảng này làm cửa đạt/rớt hay khẳng định ưu thế. Lặp thiếu mẫu số → không xác định, báo tỷ lệ lặp hợp lệ; khóa seed/số lượt/cách xử lý trước test. Với 18–20 hoặc 30 họ cũng không mặc nhiên chuyển sang kết luận khẳng định: cần thiết kế và phân tích công suất phù hợp chốt trước test.',
    46: 'So sánh chính P–B1 ở E3 trên tập test hỗn hợp đã khóa; bắt buộc kèm hai bảng riêng cho LLM sinh thông thường và biến thể. Mỗi bảng ghi n_S/n_R/n_NEI, số họ, FAR, Recall Supported, Macro-F1 và tỷ lệ R→S, NEI→S; mẫu số 0 là không xác định, mẫu số <10 cảnh báo ít mẫu. Không suy kết quả hỗn hợp/biến thể thành tỷ lệ lỗi hoặc ưu thế trên quảng cáo LLM thông thường. Không chọn nhóm thuận lợi sau test; nếu nhóm thông thường không đủ mẫu thì nêu chưa đủ bằng chứng cho nhóm đó.',
    47: 'Đo evidence-set recall@k trên claim có ít nhất một bộ bằng chứng chuẩn đủ kết luận. Báo tổng thể và N>k, k_eff, phân bố N (min/trung vị/max) theo sản phẩm; N≤k là ca truy hồi lấy hết, không minh chứng năng lực xếp hạng. NEI-thiếu không tính là truy hồi thành công. Nếu làm unfiltered, kho ứng viên/quy tắc được khóa trước test; báo thêm tỷ lệ đoạn sai sản phẩm, không thay kết quả chính bằng thiết lập có lợi hơn.',
    48: 'Kiểm tra thủ công tối đa 30 kết quả, hoặc toàn bộ nếu test nhỏ hơn, chọn trước theo nhãn và họ: nguồn có đúng không, thông tin trích có khớp nguồn không, A–B–C có dùng đúng trường không. Mã hóa một hoặc nhiều nguồn lỗi truy hồi/trích xuất/quyết định theo hướng dẫn. Nếu có chức năng tách tự động, kiểm tra riêng tối đa 20 quảng cáo về bỏ sót, mất điều kiện và đổi nghĩa.',
    49: 'Mỗi lượt chạy lưu model ID/revision, nhà cung cấp/endpoint, ngày giờ/múi giờ, model thực tế/backend nếu API trả, temperature/top_p/seed/max_tokens, cấu hình local/quantization, prompt/hash, mã/chunking/corpus/hash, cache/retry và chi phí; trường không được cung cấp ghi unavailable, không đoán. Chọn trước min(30, số test) claim theo nhãn/nhóm/họ, chạy 3 lượt tổng cộng với cấu hình cố định: lượt 1 thuộc đánh giá chính, thêm 2 lượt trên phần chọn. Mỗi lượt trích xuất mới, B1/P dùng cùng hồ sơ của lượt đó; P tất định với hồ sơ cố định nhưng toàn trình có thể đổi do LLM trích. Báo kết quả từng lượt, trung bình/min–max và tỷ lệ đổi nhãn trên cùng phần mẫu, không chọn lượt tốt nhất hoặc coi ba lượt là ba lần tăng cỡ mẫu. Nếu không đủ ngân sách, chốt và công khai thiếu kiểm tra độ ổn định trước test.',
    51: 'Kết quả mong đợi:\nMVP bắt buộc: dữ liệu có nhãn và provenance, hướng dẫn nhãn, nguồn và mã đoạn, BM25, trích xuất JSON, ba bản B0/B1/P, đánh giá chính E3 và phân tích lỗi. Quy mô được chốt theo tầng 120/180/300 phát biểu sau pilot; báo số thực tế và phần chưa đạt.',
    53: 'Ba phiên bản B0, B1 và P hoạt động trên cùng dữ liệu và giao thức E3 là yêu cầu bắt buộc. P−A/P−B và E1/E2 là phần mở rộng, chỉ thực hiện sau khi dữ liệu, ba bản chính và đánh giá đã ổn định.',
    55: 'Website minh họa và chức năng tách tự động là tùy chọn sau MVP. Bàn giao tối thiểu chương trình dòng lệnh hoặc notebook tái lập được, trả nhãn, bằng chứng và lý do cho từng phát biểu; việc hoàn thành khóa luận không phụ thuộc tích hợp website copywriting.',
    57: 'Kế hoạch thực hiện: Một sinh viên phụ trách khảo sát, dữ liệu, lập trình, thực nghiệm và luận văn; triển khai theo sáu cổng nghiệm thu (Gate).\nTháng 09/2026 (15–30/09): kế hoạch chuẩn bị và đối chiếu minh chứng\nKhảo sát [1]–[6], soạn thiết kế dữ liệu và hướng dẫn nhãn. Chỉ ghi hoàn thành trong tháng 9 khi có phiên bản hoặc nhật ký xác nhận đến 30/09/2026; nội dung được bổ sung tháng 10 phải ghi riêng.',
    54: 'Báo cáo thực nghiệm chỉ kết luận về kiểm chứng claim đã tách/rà soát thủ công, sản phẩm đã định danh và bộ nguồn đã khóa; không tuyên bố đã kiểm chứng toàn trình quảng cáo thô. RQ3 tối thiểu thăm dò, báo cả không cải thiện/đánh đổi, hai nhóm nguồn gốc và dao động chạy lặp; tuân thủ một hướng dẫn nhãn chưa đủ chứng minh đúng ngoài miền đánh giá.',
    59: 'Bản thảo có EX-01–EX-20 ghi ngày nguồn 07/10/2026 chưa có snapshot tương ứng; đã kiểm lại nguồn và chụp ngày 08/10. Bổ sung EX-21–EX-23 giả lập xung đột để kiểm thử. Hai mươi mẫu cũ chưa rõ nguồn gốc sinh; cả 23 chưa được tính là dữ liệu LLM chuẩn hay minh chứng hoàn thành tháng 9.',
    60: 'Rà soát cấu hình máy hoặc quyền truy cập API, tối đa hai LLM khả thi, mã thử và nhật ký chạy. Phần chưa có hồ sơ xác nhận được chuyển thành đầu việc Gate 1; không ghi đã chọn mô hình hoặc đã chạy thành công khi chưa có log.',
    61: 'Tháng 10/2026 — Gate 1 (01–15/10): khóa thiết kế pilot\nChốt schema, hướng dẫn nhãn và hồ sơ nguồn; pilot 45–60 phát biểu thuộc đúng 6 họ sản phẩm trong mọi tầng quy mô. Lưu provenance LLM, nguồn chính thức, snapshot, ngày và mã đoạn. Toàn bộ sáu họ pilot giữ ở dev; không mở pilot thành tám họ rồi quay về mức tối thiểu.',
    62: 'Rà soát EX-01–EX-20, bổ sung provenance và các trường hợp còn thiếu; gắn quảng cáo gốc với claim. Kiểm tra sản phẩm, phiên bản, thị trường, bộ phận và điều kiện; nguồn chưa xác thực không được dùng làm nhãn chuẩn.',
    63: 'Chia nguồn theo mục hoặc dòng bảng, giữ tiêu đề và chú thích điều kiện; kiểm tra mã đoạn và liên kết tới snapshot. Ca xung đột giả lập dùng kiểm thử riêng, không thay bằng chứng thực tế.',
    64: 'Đầu ra Gate 1: hướng dẫn chung có phiên bản, pilot có provenance/nhãn/search_log NEI; kế hoạch mời người thứ hai (chưa xác nhận), cấu hình máy/API và log tối đa hai mô hình. Nếu chưa đủ 45 claim / 6 họ hợp lệ vào 15/10, ưu tiên tối thiểu và dừng mở rộng. Các EX hiện chỉ minh họa, không thay dữ liệu đã xác minh.',
    65: 'Gate 2 (16–31/10): BM25 và chương trình chạy tối thiểu\nHoàn thiện chia đoạn, chuẩn hóa Việt–Anh và BM25; thử k = 3, 5, 8 trên dev/pilot, đo recall@k theo họ và chi phí, lưu bộ bằng chứng bỏ sót. Ghi tiêu chí lựa chọn trước khi so sánh; cấu hình cuối khóa từ dev ở Gate 4, không tìm kiếm trên val.',
    66: 'Chạy được B0 và P tối thiểu: đầu vào claim → bằng chứng → JSON → nhãn và dấu vết. Kiểm tra schema và lỗi kỹ thuật riêng; lưu đầu ra, thời gian, số lần gọi và tài nguyên. Chốt môi trường khả thi trong ngân sách, không mặc định có API miễn phí.',
    67: 'Đầu ra Gate 2: mã và log pilot, năng suất gán nhãn, chi phí, cấu hình dev tạm thời, quyết định quy mô và số họ dev/val/test. Nếu dự phóng không đạt 180 phát biểu / 18–20 họ trước 20/11, chọn 120/12 với RQ3 thăm dò. Pilot vẫn sáu họ; chỉ chọn 300/30 khi còn đủ thời gian kiểm tra nhãn và khóa dữ liệu.',
    68: 'Tháng 11/2026 — Gate 3 (01–20/11): hoàn thiện dữ liệu và ba bản chính\nGán nhãn từ nguồn theo hướng dẫn chung; tổ chức người thứ hai gán độc lập 30 mẫu trước khi xem dự đoán, lưu bất đồng và hòa giải bằng chứng. Tách việc này khỏi gán lại 20% sau 1–2 tuần của cùng người. Chưa có người/log thì ghi chưa thực hiện, không viết thành kết quả đồng thuận.',
    69: 'Giữ họ pilot ở dev, mẫu cha/biến thể cùng tập; kiểm ngưỡng mỗi nhãn dev≥10, val≥3, test≥10 và LLM sinh thông thường≥50% từng tập. Lưu số thực tế và thiếu hụt, không lấy mẫu gần trùng hay đổi nhãn để đủ ngưỡng. Kiểm nhật ký tìm nguồn NEI trước khi khóa nhãn; danh sách chia và corpus có mã băm.',
    70: 'Hoàn thiện JSON extraction cho sản phẩm, phiên bản, bộ phận, thuộc tính, loại giá trị, giá trị, đơn vị, điều kiện và mã nguồn. Kiểm tra mẫu hồ sơ thủ công để phát hiện trường thiếu, bịa thông tin hoặc trích sai.',
    71: 'Chuẩn hóa đơn vị chỉ khi cùng đại lượng; giữ Bluetooth như chuỗi phiên bản; đặc tả gần đúng, tối đa, tối thiểu và khoảng. Dung sai phải có căn cứ và được chốt trước test, không tự nới để cải thiện điểm.',
    72: 'Hoàn thiện A: kiểm tra đúng sản phẩm, phiên bản, bộ phận và thuộc tính; chuẩn hóa loại giá trị từng bên để C đối chiếu. Lưu căn cứ loại nguồn sai phạm vi, không bỏ nguồn chỉ vì khác cách diễn đạt giới hạn số.',
    73: 'Hoàn thiện B: đối chiếu điều kiện cần thiết, phân biệt UNKNOWN với điều kiện không áp dụng; kiểm thử trường hợp nguồn chưa nói tới chế độ trong claim.',
    74: 'Hoàn thiện C1–C2–C3 và kiểm thử =, >, ≥, ≤, khoảng, gần đúng, mức tối đa công bố và phiên bản. Kiểm tra EX-18 → Refuted, EX-20 → NEI-thiếu và EX-21–23 → NEI-xung đột. Lưu dấu vết; ca giả lập không được tính như bằng chứng xung đột thực tế.',
    75: 'Hoàn thiện P và giao diện dòng lệnh/notebook chạy lại được. Ưu tiên dữ liệu, log và đánh giá; tích hợp website chỉ khi các đầu ra bắt buộc đã đạt.',
    76: 'Hoàn thiện B0/B1 với nguyên khối hướng dẫn nhãn chung; kiểm prompt không bị cắt bởi giới hạn ngữ cảnh. B1/P nhận hồ sơ dữ kiện chung, không có nhãn/dấu vết P. Đầu ra Gate 3: dữ liệu đã rà nguồn/nhãn, kết quả gán độc lập hoặc ghi thiếu, bảng đếm nhóm×nhãn×tập và ba bản chạy được.',
    77: 'Gate 4 (21–30/11): khóa giao thức và kiểm tra xuyên suốt\nChọn tối đa hai mô hình ứng viên theo khả thi tài nguyên, tỷ lệ JSON hợp lệ và độ đúng trích xuất trên dev; prompt/quy tắc/k chọn trên dev, dung sai theo nguồn. Ghi tiêu chí trước lượt so sánh và khóa cấu hình trước khi mở val. Val chỉ audit/smoke test một lượt, không chỉnh để tối đa điểm. Nếu lỗi buộc sửa, ghi nhiễm val và coi val đã dùng phát triển; không tiếp tục gọi val là kiểm định độc lập. Quyết định phần mở rộng theo ngân sách.',
    78: 'Giữ cùng claim, top-k, mô hình/nhà cung cấp/cấu hình và hướng dẫn nhãn giữa các bản. B1/P chia sẻ hồ sơ trong từng lượt; lỗi/các lượt retry được giữ, không chọn seed tốt nhất. Dự toán ngân sách cho 3 lượt trên phần mẫu đã chọn; chưa đủ ngân sách phải ghi thiếu kiểm tra dao động, không tự coi temperature=0 là bảo đảm tất định.',
    79: 'Đầu ra Gate 4 trước 30/11: khóa dữ liệu/corpus/hướng dẫn/prompt/model/provider/k/dung sai/quy tắc và hash; bảng đếm nhóm×nhãn, danh sách 30 mẫu gán độc lập, mẫu phân tích lỗi và phần mẫu chạy 3 lượt. Val audit một lượt, test chưa dùng chọn cấu hình. Quyết định có đo truy hồi unfiltered không; không đổi giao thức theo kết quả test.',
    80: 'Tháng 12/2026 — Gate 5 (01–15/12): thực nghiệm chính\nChạy B0/B1/P ở E3 trên test đã khóa, lưu dự đoán gốc và lỗi. Chỉ chạy P−A/P−B, E1/E2 nếu đã chọn ở Gate 4 và đủ ngân sách; không để chúng làm chậm đánh giá chính.',
    81: 'Lập bảng chỉ số toàn test và riêng từng nhóm nguồn gốc, ghi n_S/n_R/n_NEI, số họ, R→S/NEI→S, lỗi và mẫu số; 0 → không xác định, <10 → ít mẫu. Chạy thêm hai lượt trên phần mẫu khóa trước và báo dao động; không gộp lượt lặp thành claim mới. Nếu kèm bootstrap theo họ thì nêu giới hạn ít họ và lặp không xác định.',
    82: 'Đo recall@k với k đã khóa, k_eff, số tài liệu/đoạn mỗi sản phẩm và tỷ lệ N≤k; báo riêng N>k. NEI-thiếu không tính truy hồi thành công; đối chiếu search_log để phân biệt BM25 bỏ sót với thiếu trong corpus. Thiết lập bỏ lọc chỉ là phân tích bổ sung nếu đã chọn trước.',
    83: 'Phân tích mẫu đã chọn về sai sản phẩm, phiên bản, bộ phận, loại giá trị, điều kiện, nguồn thiếu hoặc xung đột; lần theo lỗi truy hồi, trích xuất và quyết định. Báo riêng dữ liệu sinh thông thường và biến thể có kiểm soát.',
    84: 'Đầu ra Gate 5: bảng B0/B1/P, dự đoán/log, truy hồi, lỗi và kết quả từng họ. RQ3 tối thiểu chỉ báo xu hướng/đánh đổi trên test, kèm độ bất định và phân tích bỏ từng họ; không đổi thành tuyên bố ưu thế thống kê khi thấy kết quả thuận lợi.',
    85: 'Nếu có website hoặc tách tự động, kiểm tra riêng khả năng nhập quảng cáo, chọn sản phẩm, hiển thị nhãn, nguồn, lý do và lỗi kỹ thuật. Đây là minh họa bổ sung, không thay thực nghiệm trên tập test.',
    86: 'Gate 6 (16–31/12): hoàn thiện luận văn và bàn giao\nBáo đúng phạm vi claim đã tách, nguồn khóa và các giới hạn nhãn/nhóm/lặp. Khai báo AI hỗ trợ đọc/soạn tài liệu và ca giả lập, tách khỏi việc sinh quảng cáo cho thí nghiệm; sinh viên tự kiểm và chịu trách nhiệm. Xác nhận mẫu/quy định AI với GVHD/khoa trước nộp (chưa có văn bản áp dụng được xác nhận). Bàn giao luận văn, mã/dữ liệu được phép chia sẻ, hướng dẫn/prompt/log và gói tái lập.',
    87: 'Sau 15/12 không thêm phương pháp mới hoặc chỉnh luật theo nhãn test. Nếu phải sửa lỗi phần mềm, ghi phiên bản, lý do và chạy lại đồng bộ các bản bị ảnh hưởng; hoàn tất kiểm tra bàn giao trước 31/12/2026.',
    88: 'Rủi ro và ngưỡng hành động (mốc quản lý dự kiến, chưa phải kết quả)\nĐến 15/10 chưa có pilot 45 phát biểu / 6 họ hợp lệ: chọn phạm vi tối thiểu. Tại Gate 2, nếu hơn 5% lượt gọi trong lô 20 mẫu lỗi API/JSON sau tối đa một lần thử lại, hoặc chi phí dự phóng vượt ngân sách đã ghi: sửa schema/prompt hay đổi mô hình trong tối đa hai ứng viên, lưu lỗi; chưa mở rộng dữ liệu. Nếu không có môi trường khả thi, báo giảng viên để điều chỉnh kế hoạch.',
    89: 'Nếu tự đồng thuận 20% mẫu dưới 80% hoặc có bất đồng người gán: rà nguồn/hướng dẫn, giữ lịch sử nhãn; đây không phải chứng minh nhãn đúng. Chưa có người thứ hai, chưa đạt ngưỡng nhãn/nhóm hoặc thiếu lặp phải báo giới hạn, không coi tự gán lại là thay thế. Ít họ test làm bất định kém ổn định; xung đột giả lập chỉ dùng kiểm thử. Giao thức chi tiết: docs/GIAO_THUC_DANH_GIA.md.',
    90: 'Nếu đến 20/11 dữ liệu/ba bản chính chưa đạt hoặc đến 30/11 smoke test còn lỗi cản trở: bỏ P−A/P−B, E1/E2 và website; giữ provenance, dữ liệu có nhãn, BM25, JSON, B0/B1/P và đánh giá chính. Nếu vẫn không đạt mức tối thiểu, báo phần thiếu và điều chỉnh với giảng viên; không tạo mẫu gần trùng hoặc bịa kết quả để đủ số. FAR/Recall không đạt giả thuyết vẫn là kết quả cần phân tích.',
}

REPORT_PARAGRAPHS = {
    8: 'Đề tài nghiên cứu kiểm chứng claim trong quảng cáo tai nghe không dây tiếng Việt do LLM tạo. Thực nghiệm chính nhận claim đã tách/rà soát thủ công và sản phẩm được định danh đúng, đối chiếu bộ nguồn chính thức đã khóa để trả Supported/Refuted/NEI. Chỉ đánh giá truy hồi–trích xuất–quyết định; chưa đánh giá toàn trình từ quảng cáo thô, tách tự động hoặc website. Đóng góp dự kiến là dữ liệu/provenance, tiêu chí nhãn và so sánh có kiểm soát, không phải riêng việc dùng Python.',
    10: 'Thời gian thực hiện bắt đầu từ 15/09/2026. Mốc chốt minh chứng: 30/09/2026. Báo cáo tách ba trạng thái: đã có minh chứng trong kỳ; có trong bản thảo nhưng chưa xác nhận thời điểm; chuyển sang cập nhật/thực hiện tháng 10. Hồ sơ hiện tại chưa đủ căn cứ xác nhận ngày hoàn thành của từng đầu việc tháng 9; không suy ra kết quả thực nghiệm từ kế hoạch.',
    14: '3. NỘI DUNG TRONG BẢN THẢO VÀ TRẠNG THÁI MINH CHỨNG',
    13: 'Các đầu việc chuẩn bị là cơ sở cho pilot và bộ kiểm chứng claim tối thiểu trong tháng 10; chưa chứng minh hiệu quả P hoặc toàn trình xử lý quảng cáo. Việc có bản tổng hợp do AI hỗ trợ không tự xác nhận sinh viên đã kiểm thủ công hoặc hoàn thành trong tháng 9.',
    47: 'Mỗi claim/đoạn có mã tra cứu; giữ tiêu đề, điều kiện và chú thích cùng thông số. Tách thủ công không được thêm điều kiện để làm câu đúng: nếu biên tập đổi nghĩa, lưu câu gốc và chuyển bản sửa sang nhóm biến thể. Nhãn tham chiếu do người đọc toàn bộ nguồn gán, không lấy đầu ra P làm chuẩn.',
    51: 'NEI — Chưa đủ bằng chứng trong bộ nguồn X, phiên bản/thời điểm Y: thiếu thông tin để hỗ trợ/bác bỏ hoặc có xung đột cùng phạm vi chưa giải quyết. NEI-thiếu phải có search_log các trang thông số/hướng dẫn/hỗ trợ/PDF, từ khóa Việt–Anh, mục/chú thích đã rà, kết quả và lý do dừng; không chỉ dựa top-k hay khẳng định toàn web không có thông tin. Thiếu bước rà bắt buộc thì chưa chốt nhãn dữ liệu chính.',
    54: '3.3. Bộ ví dụ gán nhãn — cập nhật sau kỳ báo cáo',
    90: 'Cần xác nhận tài nguyên thực tế bằng hồ sơ: CPU [chưa có]; RAM [chưa có]; GPU/VRAM hoặc điều kiện API và ngân sách [chưa có]; hệ điều hành và môi trường chạy [chưa có]. Không suy ra cấu hình thí nghiệm tháng 9 từ máy đang dùng để sửa tài liệu.',
    91: 'Cần ghi tối đa hai mô hình ứng viên: model ID/revision, nhà cung cấp/endpoint, ngày giờ/múi giờ, model/backend thực tế nếu có, temperature/top_p/seed/max_tokens, quantization/backend local, prompt/hash, mã thử và log. Chọn trước min(30, số test) claim, 3 lượt tổng cộng; mỗi lượt trích xuất mới và B1/P dùng chung hồ sơ lượt đó. Báo dao động trên cùng phần mẫu, không chọn lượt tốt nhất hoặc nhân cỡ mẫu. Đây là kế hoạch, chưa có log chạy; trường nhà cung cấp không trả ghi unavailable.',
    92: 'Trạng thái minh chứng tài nguyên và LLM: chưa được xác nhận. Nếu có log được tạo đến 30/09/2026, ghi đường dẫn và thời điểm thực tế; nếu thử từ 01/10 trở đi, đưa vào Gate 1–2 tháng 10 và không tính thành kết quả tháng 9.',
    94: 'Bảng đối chiếu dùng ba trạng thái nêu tại mục 1. Chưa có hồ sơ đủ định thời để xếp đầu việc vào “đã có minh chứng trong kỳ”; điều này không đồng nghĩa khẳng định sinh viên chưa làm. Những phần có trong bản thảo và cập nhật sau kỳ được ghi riêng.',
    97: 'Khó khăn thực tế cần xác nhận: đầu việc bị vướng [chưa có ghi nhận]; thời điểm và nguyên nhân [chưa xác nhận]; ảnh hưởng tới tiến độ [chưa xác nhận]; biện pháp đã thử và nội dung cần giảng viên hỗ trợ [chưa xác nhận]. Các rủi ro dự kiến trong đề cương không được viết thành sự cố đã xảy ra tháng 9.',
    99: 'Tháng 10 tổ chức theo Gate 1–2 của đề cương cập nhật. Mục tiêu là hoàn thiện hồ sơ, pilot và chương trình tối thiểu; các số lượng dưới đây là kế hoạch, không phải kết quả đã đạt.',
    100: 'Gate 1 (01–15/10): rà soát minh chứng tháng 9; khóa schema, hướng dẫn nhãn và lưu nguồn. EX-01–20 đã có snapshot kiểm lại 08/10 nhưng nguồn gốc câu gốc vẫn chưa xác định; EX-21–23 là ca xung đột giả lập. Không dùng các mẫu này để xác nhận đã thu quảng cáo LLM.',
    101: 'Đầu ra Gate 1: pilot 45–60 claim thuộc đúng 6 họ có provenance LLM, nguồn và nhãn; hồ sơ máy/API, log thử tối đa hai mô hình. Sáu họ ở dev trong mọi tầng quy mô. Nếu chưa đủ 45 claim / 6 họ hợp lệ đến 15/10, ưu tiên mức tối thiểu và dừng phần mở rộng.',
    102: 'Gate 2 (16–31/10): hoàn thiện BM25, thử k = 3, 5, 8 trên dev/pilot theo tiêu chí ghi trước; đo recall theo họ, kiểm tra JSON, chạy B0/P tối thiểu và lưu log/chi phí. Khóa mô hình, prompt và k trên dev trước 30/11; dung sai dựa nguồn, không tối ưu theo nhãn. Val chỉ audit/smoke test một lượt sau khóa, không tìm kiếm cấu hình trên hai họ val.',
    103: 'Quy mô: tối thiểu 120 claim / 12 họ, dev/val/test = 6/2/4; mục tiêu 180 / 18–20 họ tương ứng 7/4/7 hoặc 8/4/8; mở rộng 300/30 nếu đủ lực. Pilot cố định sáu họ trong dev. RQ3 ở mức tối thiểu là thăm dò: báo ΔFAR, ΔRecall, kết quả từng họ và bất định; không dùng toàn bộ khoảng FAR dưới 0 làm cửa đạt/rớt. ΔFAR<0, ΔRecall≥−5 điểm chỉ là xu hướng quan sát, không xác nhận ưu thế tổng quát.',
    104: 'Gate 3: hoàn thiện dữ liệu và B0/B1/P, dự kiến người thứ hai gán độc lập 30 mẫu, kiểm ngưỡng mỗi nhãn dev≥10/val≥3/test≥10 và nhóm thông thường≥50% từng tập. Gate 4 khóa hướng dẫn/prompt, bảng đếm nhóm×nhãn, phần mẫu chạy 3 lượt và metadata mô hình. Gate 5 báo kết quả chung và riêng hai nhóm, mẫu số/dao động, recall kèm số đoạn/k_eff và N≤k. Truy hồi bỏ lọc, E1/E2, ablation, tách tự động, website là mở rộng; chưa có kết quả thực hiện.',
    105: 'Báo cáo tháng 9 chỉ xác nhận minh chứng đến 30/09. Phần đối chiếu PDF, nguồn web và sửa tài liệu tháng 10 có AI (Codex) hỗ trợ, không tự là phần sinh viên đã kiểm; EX-21–23 do AI soạn giả lập, không phải dữ liệu hãng/thí nghiệm. Sinh viên cần tự rà nguồn, xác nhận nội dung và khai báo AI theo hướng dẫn GVHD/khoa (chưa xác nhận văn bản áp dụng). Chưa có kết quả P tốt hơn B0/B1 hoặc đánh giá toàn trình quảng cáo thô.',
    114: 'Đề cương: “Đọc_báo_cùng_HuP_4_.docx”, bản rà soát 08/10/2026; không phải minh chứng nội dung đã hoàn thành tháng 9.',
    115: 'Báo cáo: “Đọc_báo_cùng_HuP_3_.docx”; bài gốc trong báo/. Hồ sơ chưa có bản lưu 30/09 hoặc log thí nghiệm.',
    118: 'AI hỗ trợ đối chiếu nguồn 20 ví dụ và soạn ba ca xung đột giả lập ngày 08/10; còn cần sinh viên kiểm nguồn/nhãn và xác minh lịch sử tạo câu gốc trước khi dùng cho dữ liệu LLM.',
    119: 'Điền tài nguyên, mô hình và khó khăn còn chưa xác nhận; dẫn file/log đúng kỳ.',
}


def children(node, name):
    return [n for n in node.childNodes if n.nodeType == Node.ELEMENT_NODE and n.nodeName == name]


def text(node):
    return ''.join(t.firstChild.data if t.firstChild else '' for t in node.getElementsByTagName('w:t'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def paragraph(template, value, *, red=False, bold=None, new=False):
    """Keep paragraph/run properties; replace text without changing the styles part."""
    p = template.cloneNode(deep=True)
    if new:
        for attr in ('w14:paraId', 'w14:textId'):
            if p.hasAttribute(attr):
                p.removeAttribute(attr)
    runs = [r for r in p.getElementsByTagName('w:r') if r.getElementsByTagName('w:t')]
    # Prefer body text formatting over a short bold label at paragraph start.
    source = max(runs, key=lambda r: len(text(r)), default=None)
    props = children(source, 'w:rPr') if source else []
    rpr = props[0].cloneNode(deep=True) if props else p.ownerDocument.createElementNS(W, 'w:rPr')
    for node in list(p.childNodes):
        if node.nodeName != 'w:pPr':
            p.removeChild(node)
    for name, val in [('w:color', 'C00000' if red else None),
                      ('w:b', None if bold is None else str(int(bold))),
                      ('w:bCs', None if bold is None else str(int(bold)))]:
        if val is not None:
            for old in children(rpr, name):
                rpr.removeChild(old)
            prop = p.ownerDocument.createElementNS(W, name)
            prop.setAttributeNS(W, 'w:val', val)
            rpr.appendChild(prop)
    run = p.ownerDocument.createElementNS(W, 'w:r')
    run.appendChild(rpr)
    t = p.ownerDocument.createElementNS(W, 'w:t')
    t.setAttribute('xml:space', 'preserve')
    t.appendChild(p.ownerDocument.createTextNode(value))
    run.appendChild(t)
    p.appendChild(run)
    return p


def set_cell(cell, value, *, red=False):
    old = children(cell, 'w:p')
    if not old or children(cell, 'w:tbl'):
        raise ValueError('Expected a text-only cell')
    for i, line in enumerate(value.split('\n')):
        template = old[min(i, len(old) - 1)]
        p = paragraph(template, line, red=red, new=i >= len(old))
        cell.insertBefore(p, old[0])
    for p in old:
        cell.removeChild(p)


def keep_with_next(p):
    props = children(p, 'w:pPr')
    if not props:
        props = [p.ownerDocument.createElementNS(W, 'w:pPr')]
        p.insertBefore(props[0], p.firstChild)
    for old in children(props[0], 'w:keepNext'):
        props[0].removeChild(old)
    setting = p.ownerDocument.createElementNS(W, 'w:keepNext')
    setting.setAttributeNS(W, 'w:val', '1')
    style = children(props[0], 'w:pStyle')
    props[0].insertBefore(setting, style[-1].nextSibling if style else props[0].firstChild)


def body(doc):
    return doc.getElementsByTagName('w:body')[0]


def cell_at(table, row, column=0):
    return children(children(table, 'w:tr')[row], 'w:tc')[column]


def structure(doc):
    return [[len(children(r, 'w:tc')) for r in children(t, 'w:tr')]
            for t in children(body(doc), 'w:tbl')]


def audited_examples():
    path = ROOT / 'evidence/2026-10-08/examples.json'
    examples = json.loads(path.read_text(encoding='utf-8'))['examples']
    assert len(examples) == 23
    return examples


def fill_example(table, example):
    e = example
    fixture = e['original_origin'] == 'synthetic_test_fixture'
    origin = ('Do Codex soạn ngày 08/10/2026, ca GIẢ LẬP kiểm thử; không phải thông số Apple hoặc mẫu quảng cáo LLM thí nghiệm.' if fixture else
              'Nguồn gốc câu gốc: CHƯA XÁC ĐỊNH; chưa có model/prompt/log. Không suy ra là tự viết hay LLM sinh; chưa đưa vào dữ liệu LLM.')
    set_cell(cell_at(table, 1, 1), e['title'] + '\n' + origin)
    set_cell(cell_at(table, 2, 1), e['group'])
    set_cell(cell_at(table, 3, 0), 'Câu giả lập' if fixture else 'Câu gốc trong bản thảo (chưa rõ tác giả)')
    set_cell(cell_at(table, 3, 1), e['original_ad'])
    set_cell(cell_at(table, 4, 0), 'Câu rà soát dùng gán nhãn')
    set_cell(cell_at(table, 4, 1), e['reviewed_claim'])
    set_cell(cell_at(table, 5, 1), e['scope'])
    set_cell(cell_at(table, 6, 0), 'Hai đoạn GIẢ LẬP' if fixture else 'Đoạn nguồn nguyên văn (tiêu đề lưu riêng)')
    set_cell(cell_at(table, 6, 1), '\n'.join(('Nguồn giả lập ' + str(i) + ': ' if fixture else '') + '“' + q['text'] + '”' for i, q in enumerate(e['quotes'], 1)))
    if fixture:
        source = 'Không có URL hãng. Hai nguồn do trợ lý soạn theo yêu cầu bổ sung ca xung đột; cùng ngày hiệu lực và mức ưu tiên, không thay thế nhau. Hồ sơ: evidence/2026-10-08/examples.json. Chỉ dùng kiểm thử, không tính vào pilot/test.'
    else:
        lines = ', '.join(str(q['start_line']) for q in e['quotes'])
        shot = Path(e['screenshot']).name
        source = (e['url'] + '\nVị trí: ' + e['locator'] + '\nKiểm lại và chụp: 08/10/2026; ngày 07/10 kế thừa chưa có snapshot. '
                  + f'Hồ sơ: evidence/2026-10-08/{e["source_id"]}/; page.txt dòng {lines}; ảnh {shot}; full-page.png giữ toàn trang/chú thích.')
        if e['nei_type'] == 'missing':
            assert e['nei_search_log']['production_label_ready'] is False
            source += '\nsearch_log trong examples.json: mới rà trang/chú thích đã dẫn, chưa rà hệ thống các hướng dẫn và tài liệu hãng khác. NEI ở đây chỉ là minh họa trong nguồn này, chưa đủ quy trình nhãn dữ liệu chính.'
    set_cell(cell_at(table, 7, 1), source)
    values = e['values'] + '\nĐiều kiện: ' + e['conditions_summary']
    if e['condition_ref']:
        values += '\ncondition_ref: ' + e['condition_ref'] + '; chỉ áp dụng cho câu đã rà soát, không tự thêm điều kiện vào câu gốc.'
    set_cell(cell_at(table, 8, 1), values)
    set_cell(cell_at(table, 9, 0), 'Nhãn minh họa dự kiến')
    label = e['label'] + ({'missing': ' — NEI-thiếu', 'conflict': ' — NEI-xung đột'}.get(e['nei_type'], ''))
    set_cell(cell_at(table, 9, 1), label)
    set_cell(cell_at(table, 10, 1), e['reason'])


def revise_proposal(doc):
    tables = children(body(doc), 'w:tbl')
    assert len(tables) == 2 and len(children(tables[1], 'w:tr')) == 98
    assert text(cell_at(tables[1], 19)).startswith('Quy mô mục tiêu dự kiến là khoảng 300')
    assert text(cell_at(tables[1], 96)).startswith('[6]')
    for row, value in PROPOSAL_ROWS.items():
        set_cell(cell_at(tables[1], row), value, red=True)
    # Keep the existing [6] paragraph and its hyperlink; append five references.
    ref_cell = cell_at(tables[1], 96)
    template = children(ref_cell, 'w:p')[-1]
    for ref in REFERENCES:
        ref_cell.appendChild(paragraph(template, ref, red=True, bold=False, new=True))
    for p in children(body(doc), 'w:p'):
        if text(p).startswith('Bản rà soát:'):
            p.parentNode.replaceChild(paragraph(p, 'Bản rà soát ngày 08/10/2026: chữ đỏ là phần thêm hoặc sửa; các mốc và quy mô là kế hoạch dự kiến.', red=True), p)
            break
    else:
        raise ValueError('Missing proposal revision marker')


def revise_report(doc):
    b = body(doc)
    ps = children(b, 'w:p')
    tables = children(b, 'w:tbl')
    assert len(tables) == 29 and len(ps) == 122
    assert text(ps[92]).startswith('[Cần bổ sung] Cấu hình')
    assert text(ps[54]) == '3.3. Bộ ví dụ gán nhãn'
    for index, value in REPORT_PARAGRAPHS.items():
        b.replaceChild(paragraph(ps[index], value), ps[index])
    # Add notes at the actual positions in the document, including tables.
    ai_note = ('Ghi nhận hỗ trợ AI — cập nhật tháng 10: phần đối chiếu số liệu/trang PDF, tìm nguồn và biên tập trong lần rà soát 08/10/2026 có công cụ AI (Codex) hỗ trợ. '
               'Đây không phải xác nhận sinh viên đã tự mở và kiểm các bảng. Sinh viên cần kiểm trực tiếp tối thiểu Bảng 1 của [2], Bảng 1 của [3], Bảng 2 của [5], '
               'ghi ngày/vị trí/kết quả và rà các số còn lại trước khi nộp. AI không là tác giả nguồn hoặc người gán nhãn độc lập. '
               'Cách khai báo theo quy định khoa/GVHD còn cần xác nhận; không suy ra khai báo này đã được khoa chấp thuận.')
    b.insertBefore(paragraph(ps[9], ai_note, new=True), ps[16])
    example_heading = next(p for p in children(b, 'w:p') if text(p).startswith('3.3.'))
    protocol_notes = [
        'Kiểm soát thiên lệch: B0/B1 nhận nguyên khối hướng dẫn nhãn chung tại docs/HUONG_DAN_GAN_NHAN.md, cùng phiên bản/hash với tiêu chí người gán và P; không chỉ nhắc tên các bước. B1/P dùng cùng hồ sơ dữ kiện, không có nhãn/dấu vết P. Dự kiến người thứ hai gán độc lập 30 claim theo nhãn sơ bộ/nguồn gốc/họ, không thấy nhãn đầu hay dự đoán; lưu bất đồng trước hòa giải. Chưa có người và log xác nhận. Tự gán lại 20% không thay thế việc này; đồng thuận cũng không tự chứng minh nhãn đúng.',
        'Phân bố và báo cáo: nhóm LLM sinh thông thường giữ phân bố quan sát, tối thiểu 50% từng tập; bản sửa đổi ý nghĩa thuộc nhóm biến thể riêng. Ngưỡng mỗi nhãn dev≥10, val≥3, test≥10 là mốc vận hành, không bảo đảm công suất. Báo cả bảng chung và riêng nhóm, n_S/n_R/n_NEI, số họ, FAR/Recall/Macro-F1 và R→S/NEI→S; mẫu số 0 ghi không xác định, <10 cảnh báo ít mẫu. Không đủ thì báo thiếu, không chỉnh nhãn hoặc lấy họ dev sang test.',
        'Giới hạn truy hồi: BM25 chính đã biết đúng sản phẩm; báo số tài liệu, N đoạn, k_eff=min(k,N), tỷ lệ N≤k và recall riêng N>k. Kho ít đoạn có thể bị lấy hết, không chứng minh tìm đúng sản phẩm hoặc tìm toàn web. Nếu kịp, đo thêm bỏ lọc trên kho nhiều sản phẩm khóa trước, giữ query/k/chunking; không bắt buộc mở rộng suy luận LLM. Giao thức chọn mẫu, tìm nguồn NEI, chạy lặp và log: docs/GIAO_THUC_DANH_GIA.md.',
    ]
    for note in protocol_notes:
        b.insertBefore(paragraph(ps[9], note, new=True), example_heading)
    note = ('Bộ minh họa hiện có 23 ví dụ: EX-01–20 kế thừa bản thảo, đã kiểm lại năm trang Apple và lưu HTML, văn bản, ảnh chụp, mã băm ngày 08/10/2026; '
            'ngày 07/10 ghi trong bản cũ chưa có snapshot để xác nhận. EX-21–23 là ba ca xung đột GIẢ LẬP do Codex soạn trong lần rà soát này, không gán thông số cho Apple. '
            'Nguồn gốc 20 câu cũ CHƯA XÁC ĐỊNH: thiếu log không chứng minh là không do LLM sinh. Giữ câu cũ riêng và đánh dấu câu biên tập có kiểm soát; nhãn chỉ áp dụng cho câu đã rà soát. '
            'Các ví dụ không phải minh chứng hoàn thành tháng 9; chưa được tính vào dữ liệu LLM chuẩn/pilot/test. Hồ sơ từng mẫu: evidence/2026-10-08/examples.json; ảnh và nguồn: evidence/2026-10-08/README.md. '
            'Phải có model/phiên bản, prompt, cấu hình sinh, thời điểm và đầu ra gốc trước khi xác nhận quảng cáo LLM; biến thể cần mẫu cha và thao tác sửa.')
    b.insertBefore(paragraph(ps[9], note, new=True), example_heading.nextSibling)
    read_more = ('Đề xuất đọc thêm — bổ sung trong bản rà soát tháng 10: FEVER [7] về ba nhãn và bộ bằng chứng; '
                 'AVeriTeC [8] về nguồn web và rò rỉ thời gian; ViFactCheck [9] về kiểm chứng tin tiếng Việt; '
                 'ViWikiFC [10] về truy hồi và dự đoán nhãn từ Wikipedia tiếng Việt; ViNumFCR [11] về kiểm chứng số liệu tiếng Việt. '
                 'Đây là tài liệu bổ sung cho thiết kế nghiên cứu, không phải xác nhận đã đọc trong tháng 9.')
    b.insertBefore(paragraph(ps[9], read_more, new=True), ps[29])
    for ref in REFERENCES:
        b.insertBefore(paragraph(ps[112], ref, bold=False, new=True), ps[113])
    statuses = [
        'Có trong bản thảo, chưa xác nhận thời điểm: phần rà soát tháng 10 có AI hỗ trợ; chưa xác nhận sinh viên tự kiểm. Cần bản lưu/nhật ký đến 30/09 để xác nhận trong kỳ và xác nhận thủ công các bảng trước nộp.',
        'Có trong bản thảo, chưa xác nhận thời điểm: tiêu chí nguồn, hồ sơ dữ liệu và ba nhãn đã được mô tả; schema/hướng dẫn có phiên bản được chốt tại Gate 1 tháng 10.',
        'Cập nhật sau kỳ: EX-01–20 đã kiểm nguồn/ảnh ngày 08/10, nguồn gốc câu cũ chưa xác định; EX-21–23 giả lập xung đột. Chưa tính 23 ví dụ này là dữ liệu LLM chuẩn hoặc minh chứng tháng 9.',
        'Chuyển sang thực hiện/xác nhận tháng 10: hồ sơ chưa có cấu hình, mã thử, log hoặc số đo. Nếu tìm được log đúng kỳ thì cập nhật trạng thái theo ngày thực tế.',
    ]
    for ri, value in enumerate(statuses, 1):
        set_cell(cell_at(tables[28], ri, 1), value)
    examples = audited_examples()
    for table, example in zip(tables[8:28], examples[:20]):
        fill_example(table, example)
    for example in examples[20:]:
        heading = paragraph(ps[86], 'Ví dụ ' + example['title'], new=True)
        keep_with_next(heading)
        b.insertBefore(heading, ps[89])
        table = tables[27].cloneNode(deep=True)
        for p in table.getElementsByTagName('w:p'):
            for attr in ('w14:paraId', 'w14:textId'):
                if p.hasAttribute(attr):
                    p.removeAttribute(attr)
        fill_example(table, example)
        for p in children(table, 'w:tr')[0].getElementsByTagName('w:p'):
            keep_with_next(p)
        b.insertBefore(table, ps[89])
        b.insertBefore(paragraph(ps[9], '', new=True), ps[89])
    # Give exact experiment settings and avoid treating cited results as ours.
    set_cell(cell_at(tables[3], 3, 1), 'Đã đối chiếu báo/[2].pdf: Bảng 1, trang PDF 3 (18087), Pearson/Spearman tiêu chí sufficiency = 0,14/0,09; Bảng 6, trang PDF 10 (18094), Krippendorff’s alpha = 0,0486. Đây là độ khớp bộ chấm với người, không phải đồng thuận hai người hoặc Accuracy kiểm chứng. Mục 3.1, trang PDF 4: 733 claim gốc từ CoverBench, không phải số sub-claim.')
    set_cell(cell_at(tables[4], 3, 1), 'Đã đối chiếu báo/[3].pdf: Bảng 1, trang PDF 7, Llama-3.1-8B/QuanTemp, Macro-F1 Adaptive BoN 53,91 so với Top-1 44,80: chênh 9,11 điểm phần trăm. Không dùng “18,8%” ở abstract làm kết quả của cặp số này. Mục 4, trang PDF 6 xác nhận verifier là Llama-3.2-3B fine-tune LoRA, khác mô hình sinh. Đây là kết quả tác giả, chưa tái lập trong KLTN.')
    set_cell(cell_at(tables[5], 3, 1), 'Đã đối chiếu báo/[4].pdf: Bảng 1, trang PDF 7, Qwen2.5-14B/DRUID, CLUE-Span+Steering có Entropy-CCT 0,102; PromptBaseline −0,080. Đây là tương quan, không phải Accuracy/F1. Mục 5.1, trang PDF 6 và Phụ lục I.1, trang PDF 21: 12 người đánh giá 120 lời giải thích của 40 claim (20 DRUID, 20 HealthVer).')
    set_cell(cell_at(tables[6], 3, 1), 'Đã đối chiếu báo/[5].pdf: Bảng 2, trang PDF 9, ContraNote Conflict: CoVer Accuracy 86,0%, Macro-F1 68,0%; Confact Macro-F1 73,4%. Mục 6.4, trang PDF 8: tác giả báo so sánh CoVer với CONFACT/ConflictRes trên Conflict không có ý nghĩa theo McNemar, α=0,05. Không suy rộng nhận xét này sang mọi tập/chỉ số; KLTN không tự chạy lại kiểm định.')
    set_cell(cell_at(tables[7], 3, 1), 'Bảng 4 trên test: điểm AVeriTeC 0,2043 so với 0,2023, tăng 0,0020 điểm (0,20 điểm phần trăm; khoảng 0,99% tương đối). Thời gian giảm từ 33,88 xuống 22,73 giây/claim. Không dùng mô tả “0,99% tuyệt đối” trong abstract thay cho số liệu bảng.')
    for table in tables[2:8]:
        result = cell_at(table, 3, 1)
        value = text(result)
        if value.startswith('Đã đối chiếu '):
            value = value.removeprefix('Đã đối chiếu ')
        set_cell(result, 'Đối chiếu có hỗ trợ AI; chờ sinh viên xác nhận: ' + value)


def validate_content(name, doc):
    """Kiểm nội dung theo thiết kế 08/10/2026 (redesign_plan_2026_10_08.py).

    Đổi phía kiểm tra ngày 08/10/2026: chuỗi cũ ('đúng 6 họ' ở Gate 1 01–15/10, '7/4/7 hoặc 8/4/8',
    mức 300 là phương án) thuộc thiết kế đã thay; xem docs/DOI_CHIEU_THAY_DOI_KE_HOACH.md.
    """
    s = text(doc)
    if name == PROPOSAL:
        assert [len(t) for t in structure(doc)] == [1, 98]
        assert structure(doc)[1] == [1] * 97 + [2]
        for token in ['Bản đề xuất điều chỉnh, chờ GVHD xác nhận', '120', 'RQ1', 'RQ2', 'RQ3', 'MVP',
                      'Gate 1 (08–31/10)', 'Gate 2', 'Gate 3', 'Gate 4', 'Gate 5', 'Gate 6', '6/2/4', '7/4/7',
                      'FAR', 'Recall Supported', 'C2', 'thăm dò', 'đúng 6 họ', 'inherit_headline',
                      'ordinary_llm', 'controlled_variant', 'end-to-end', 'DỰ THẢO', 'ngoài Apple',
                      'cluster bootstrap', 'không phải khẳng định “đầu tiên”']:
            assert token in s, token
        for forbidden in ('Gate 1 (01–15/10)', '8/4/8', 'mở rộng 300 phát biểu / 30 họ chỉ khi'):
            assert forbidden not in s, forbidden
    else:
        assert len(structure(doc)) == 32
        for forbidden in ('[Cần bổ sung]', '[chưa có]', '[chưa xác nhận]', 'Chưa có danh sách và số lượng ví dụ',
                          'Hồ sơ sử dụng để lập báo cáo', 'GHI CHÚ NỘI BỘ', 'Gate 1 (01–15/10)'):
            assert forbidden not in s, forbidden
        assert 'Mốc chốt minh chứng: 30/09/2026' in s
        assert s.count('Nhãn minh họa dự kiến') == 23
        for i in range(1, 24):
            assert f'EX-{i:02}' in s
        for token in ('không phải minh chứng hoàn thành tháng 9', 'KHAI BÁO SỬ DỤNG CÔNG CỤ AI',
                      'inherit_headline', 'Moldova', 'SINH VIÊN ĐIỀN'):
            assert token in s, token
    for forbidden in ('6–8 họ', '8/2/4', 'bỏ kiểm tra bộ phận và loại giá trị', 'k cuối cùng chốt trên tập kiểm định'):
        assert forbidden not in s, forbidden
    for number in range(7, 12):
        assert f'[{number}]' in s
    for required in ('hướng dẫn nhãn', 'độc lập 30', 'search_log', 'k_eff', '3 lượt', 'nhà cung cấp', '50%', 'AI', 'quảng cáo thô'):
        assert required in s, required
    assert 'Đã đối chiếu báo/' not in s


def validate_package(original, updated, name):
    with ZipFile(io.BytesIO(original)) as before, ZipFile(io.BytesIO(updated)) as after:
        assert after.testzip() is None
        assert before.namelist() == after.namelist()
        for part in before.namelist():
            if part != 'word/document.xml':
                assert before.read(part) == after.read(part), f'Unexpected changed part: {part}'
            if part.endswith(('.xml', '.rels')):
                minidom.parseString(after.read(part))
        d0 = minidom.parseString(before.read('word/document.xml'))
        d1 = minidom.parseString(after.read('word/document.xml'))
    for tag in ('w:sectPr', 'w:drawing', 'w:pict'):
        assert [n.toxml() for n in d0.getElementsByTagName(tag)] == [n.toxml() for n in d1.getElementsByTagName(tag)], tag
    ts0, ts1 = (children(body(d), 'w:tbl') for d in (d0, d1))
    mapping = list(range(len(ts0))) if name == PROPOSAL else list(range(28)) + [31]
    for old_idx, new_idx in enumerate(mapping):
        assert structure(d0)[old_idx] == structure(d1)[new_idx]
        for tag in ('w:tblPr', 'w:tblGrid', 'w:trPr', 'w:tcPr'):
            assert [n.toxml() for n in ts0[old_idx].getElementsByTagName(tag)] == [n.toxml() for n in ts1[new_idx].getElementsByTagName(tag)], (old_idx, tag)
    if name == PROPOSAL:
        t0, t1 = (children(body(d), 'w:tbl')[1] for d in (d0, d1))
        assert children(t0, 'w:tr')[97].toxml() == children(t1, 'w:tr')[97].toxml()
    else:
        for table, e in zip(ts1[8:31], audited_examples()):
            assert text(cell_at(table, 4, 1)) == e['reviewed_claim']
            assert e['label'] in text(cell_at(table, 9, 1))
            for q in e['quotes']:
                assert q['text'] in text(cell_at(table, 6, 1)), e['id']
        # Legacy wording is preserved separately, not silently reattributed.
        for idx in range(8, 28):
            assert text(cell_at(ts0[idx], 3, 1)) == text(cell_at(ts1[idx], 3, 1))
    validate_content(name, d1)


def build(source, name):
    with ZipFile(io.BytesIO(source)) as archive:
        doc = minidom.parseString(archive.read('word/document.xml'))
        (revise_proposal if name == PROPOSAL else revise_report)(doc)
        output = io.BytesIO()
        with ZipFile(output, 'w') as target:
            for entry in archive.infolist():
                target.writestr(entry, doc.toxml(encoding='UTF-8') if entry.filename == 'word/document.xml' else archive.read(entry.filename))
    result = output.getvalue()
    validate_package(source, result, name)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    manifest_path = WORK / 'manifest.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    pending = []
    for name in (PROPOSAL, REPORT):
        path = ROOT / name
        current = path.read_bytes()
        backup = WORK / 'originals' / name
        original = backup.read_bytes() if backup.exists() else current
        if name in manifest:
            assert digest(original) == manifest[name]['original_sha256'], 'Backup changed'
        if args.check:
            if backup.exists():
                validate_package(original, current, name)
            else:
                with ZipFile(io.BytesIO(current)) as z:
                    validate_content(name, minidom.parseString(z.read('word/document.xml')))
            print(f'PASS: {name} — content, tables and Open XML')
            continue
        if backup.exists() and current != original:
            assert name in manifest and digest(current) == manifest[name]['updated_sha256'], 'Document has newer user edits; refusing to overwrite'
        updated = build(original, name)
        pending.append((name, path, backup, original, updated))
        print(f'VALIDATED: {name} — {len(original):,} → {len(updated):,} bytes')
    if args.check:
        return
    if not args.apply:
        print('Preview only. Use --apply to back up and update both documents.')
        return
    # Both documents have passed validation before touching either original.
    for name, path, backup, original, updated in pending:
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            with backup.open('xb') as f:
                f.write(original)
        current = path.read_bytes()
        if current != updated:
            prior = WORK / 'before-audit' / (digest(current)[:12] + '-' + name)
            prior.parent.mkdir(parents=True, exist_ok=True)
            if not prior.exists():
                with prior.open('xb') as f:
                    f.write(current)
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.docx-update-', suffix='.docx', delete=False) as f:
            f.write(updated)
            temp_path = Path(f.name)
        os.chmod(temp_path, path.stat().st_mode & 0o777)
        os.replace(temp_path, path)
        manifest[name] = {'original_sha256': digest(original), 'updated_sha256': digest(updated)}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Updated both documents. Backups: {WORK / "originals"}')


if __name__ == '__main__':
    main()
