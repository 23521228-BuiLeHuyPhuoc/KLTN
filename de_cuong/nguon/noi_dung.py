# -*- coding: utf-8 -*-
"""Nội dung đề cương sửa theo nhận xét của Khoa (bản 10/2026, tên đề tài mới).

K(...) = giữ nguyên từ bản đã nộp (chữ đen); N(...) = thêm mới hoặc sửa (chữ đỏ).
{ref:khoa} = trích dẫn, được đánh số theo thứ tự xuất hiện đầu tiên (chuẩn IEEE).
"""
from pathlib import Path

HINH_1 = str(Path(__file__).with_name("hinh1_quy_trinh.png"))


def K(t, b=False, i=False):
    return ("K", t, b, i)


def N(t, b=False, i=False):
    return ("N", t, b, i)


TITLE_VI = "Phương pháp kiểm chứng tuyên bố về thông số kỹ thuật có điều kiện ràng buộc trong quảng cáo"
TITLE_EN = "A method for verifying conditional technical specification claims in advertisements"

GHI_CHU = ("Bản sửa theo nhận xét của Khoa (tháng 10/2026): chữ đỏ là phần thêm mới hoặc sửa so với "
           "đề cương đã nộp, phần bị lược bỏ không hiển thị. Trước khi nộp bản chính thức, xóa dòng này "
           "và chuyển chữ đỏ về màu đen.")

# ---------------------------------------------------------------------------
# Phần 1: Nội dung đề tài (từ dòng "Nội dung đề tài" đến hết "Kết quả mong đợi")
# Mỗi phần tử của SEC_NOI_DUNG là một hàng của bảng; mỗi hàng là danh sách đoạn.
# ---------------------------------------------------------------------------
SEC_NOI_DUNG = [
    [("text", [
        K("Nội dung đề tài:", b=True),
        K(" Nghiên cứu "),
        N("phương pháp kiểm chứng các tuyên bố về thông số kỹ thuật có điều kiện ràng buộc trong"),
        K(" nội dung quảng cáo "),
        N("tiếng Việt"),
        K(" do các mô hình ngôn ngữ lớn (LLM) tạo ra, sử dụng tài liệu "),
        N("thông số chính hãng"),
        K(" làm bằng chứng"),
        N(". Thông số có điều kiện ràng buộc là thông số mà giá trị công bố chỉ đúng khi thỏa điều kiện đi "
          "kèm, ví dụ thời lượng pin khi bật hoặc tắt chống ồn, thời gian sạc với bộ sạc đủ công suất hay độ "
          "sáng màn hình khi ở ngoài trời. Phương pháp đối chiếu tường minh điều kiện nêu trong tuyên bố với "
          "điều kiện trong tài liệu, rồi gán một trong bốn nhãn Đúng (Supported), Sai (Refuted), Lệch điều "
          "kiện (Misleading) hoặc Chưa đủ thông tin (NEI), kèm đoạn nguồn và lý do. Thực nghiệm được thực hiện "
          "trên quảng cáo về ba nhóm thiết bị điện tử tiêu dùng: điện thoại thông minh, tai nghe không dây và "
          "đồng hồ thông minh. Kết quả được xây dựng thành một tính năng mới cho website tạo nội dung quảng "
          "cáo CopyPro mà sinh viên đã phát triển trong đồ án chuyên ngành."),
    ])],

    # ----- 1. Tổng quan -----
    [("sub", [N("1. Tổng quan", b=True)]),
     ("text", [
        N("Bối cảnh. ", b=True, i=True),
        N("Các LLM ngày càng được dùng để viết nội dung quảng cáo nhưng có thể sinh thông tin không khớp với "
          "nguồn, gọi là ảo giác {ref:vihallu}. Với thông số kỹ thuật, một lỗi khó nhận ra là con số đúng "
          "nhưng bị tách khỏi điều kiện công bố. Ví dụ, trang thông số iPhone 17 ghi sạc lên đến 50% trong 20 "
          "phút “với bộ tiếp hợp 40W trở lên”, còn 3000 nit là độ sáng đỉnh khi ở ngoài trời trong khi độ "
          "sáng tối đa tiêu chuẩn là 1000 nit {ref:apple}. Quảng cáo viết “sạc 50% chỉ trong 20 phút” hay "
          "“màn hình sáng 3000 nit” giữ đúng con số nhưng bỏ điều kiện, khiến người mua hiểu sai. Một nghiên "
          "cứu được Ủy ban Thương mại Liên bang Hoa Kỳ (FTC) công bố cho thấy nhiều người xem quảng cáo có "
          "cụm từ “lên đến” vẫn tin rằng mình sẽ đạt mức tối đa {ref:ftc}. Tại Việt Nam, Luật Quảng cáo sửa "
          "đổi năm 2025 yêu cầu người có ảnh hưởng khi chuyển tải quảng cáo phải kiểm tra tài liệu liên quan "
          "đến sản phẩm (Điều 15a, khoản 3) {ref:law}, cho thấy việc đối chiếu quảng cáo với tài liệu sản "
          "phẩm đang được coi trọng. Quảng cáo do LLM tạo vì thế cũng cần được kiểm chứng với tài liệu "
          "chính hãng trước khi đăng."),
     ])],

    [("text", [
        N("Website CopyPro mà sinh viên xây dựng trong đồ án chuyên ngành cho thấy rõ vấn đề này. CopyPro tạo "
          "quảng cáo cho 10 ngành mặc định bằng nhiều LLM; phần mô tả yêu cầu gồm ngành, loại bài, giọng điệu, "
          "tên sản phẩm, từ khóa, đối tượng và thông tin bổ sung nhập tự do, không có trường nào chứa thông số "
          "sản phẩm. Vì vậy, nếu người dùng không tự dán thông số vào ô thông tin bổ sung thì con số trong bài "
          "do LLM tự sinh; khi thiếu tên sản phẩm, câu lệnh còn yêu cầu LLM “tự giả định hợp lý”, và một số "
          "mẫu bài chỉ dặn LLM không tự bịa số liệu. Sau khi tạo, CopyPro chấm điểm chất lượng (bài có số "
          "liệu được cộng điểm) và kiểm tra đạo văn, nhưng chưa kiểm tra số liệu có đúng với sản phẩm hay "
          "không."),
     ])],

    [("text", [
        N("Các nghiên cứu liên quan. ", b=True, i=True),
        N("Kiểm chứng thông tin tự động thường gồm bước truy hồi bằng chứng và bước dự đoán nhãn cho tuyên "
          "bố {ref:guo}. FEVER {ref:fever} dùng ba nhãn Supported, Refuted và Not Enough Info; AVeriTeC "
          "{ref:averitec} bổ sung nhãn Conflicting Evidence/Cherry-picking cho tuyên bố vừa có bằng chứng ủng "
          "hộ vừa có bằng chứng bác bỏ, hoặc đúng về mặt kỹ thuật nhưng gây hiểu nhầm do bỏ qua ngữ cảnh quan "
          "trọng. Với tiếng Việt, ViFactCheck {ref:vifactcheck} (tin tức đa lĩnh vực), ViWikiFC {ref:viwikifc} "
          "(Wikipedia) và ViNumFCR {ref:vinumfcr} (tuyên bố số liệu trên tin tức mạng xã hội) xây dựng dữ liệu "
          "kiểm chứng, còn SemViQA {ref:semviqa} kết hợp truy hồi bằng chứng theo ngữ nghĩa với phân loại "
          "nhãn hai bước."),
     ])],

    [("text", [
        N("Với tuyên bố chứa số liệu, {ref:thinkright} huấn luyện một mô hình kiểm định để chọn đường suy luận "
          "tốt nhất trong nhiều đường do LLM sinh, còn {ref:numpert} cho thấy độ chính xác của các mô hình "
          "ngôn ngữ, kể cả mô hình thương mại hàng đầu, có thể giảm đến 62% khi con số trong tuyên bố bị thay "
          "đổi có kiểm soát. FactLens {ref:factlens} đánh giá việc tách tuyên bố phức tạp thành các tuyên bố "
          "nhỏ để kiểm chứng. Với văn bản do LLM tạo, MiniCheck {ref:minicheck} kiểm tra các tuyên bố trong "
          "đầu ra có được tài liệu nền hỗ trợ hay không, ViHallu {ref:vihallu} cung cấp dữ liệu phát hiện ảo "
          "giác tiếng Việt. Gần nhất với đề tài, {ref:paclic} dùng LLM trích giấy phép, địa chỉ và dịch vụ "
          "trong bài quảng cáo dịch vụ làm đẹp và thẩm mỹ rồi so khớp với dữ liệu cấp phép của cơ quan y tế, "
          "còn {ref:jiang} phát hiện ảo giác trong thông tin sản phẩm do LLM bổ sung trên sàn thương mại điện "
          "tử. Các nghiên cứu về giải thích độ bất định {ref:clue}, xử lý bằng chứng xung đột {ref:cover} và "
          "truy hồi bằng chứng nhanh {ref:fathom} cung cấp kỹ thuật cho từng bước của quy trình kiểm chứng."),
     ])],

    [("text", [
        N("Hạn chế của các phương pháp hiện có. ", b=True, i=True),
        N("Các phương pháp trên chủ yếu xét mức khớp nội dung giữa tuyên bố và bằng chứng, chưa biểu diễn "
          "tường minh điều kiện ràng buộc của thông số kỹ thuật như chế độ đo, bộ phận hoặc phụ kiện đi kèm, "
          "phiên bản máy hay kiểu giá trị “lên đến”. Hệ quả là: (1) với tập ba nhãn như FEVER {ref:fever}, "
          "tuyên bố đúng con số nhưng thiếu điều kiện không có nhãn riêng nên có nguy cơ bị chấp nhận là "
          "Supported; (2) với tập nhãn có lớp gây hiểu nhầm, lớp này vẫn là điểm yếu, ví dụ Fathom "
          "{ref:fathom} đạt F1 bằng 0 ở nhãn Conflicting/Cherry-picking trên tập phát triển của AVeriTeC; "
          "(3) {ref:paclic} so khớp bằng ngưỡng độ tương đồng và chỉ gán một nhãn vi phạm hoặc không vi phạm "
          "cho cả bài quảng cáo, nên không chỉ ra nội dung nào sai và không xét điều kiện áp dụng; (4) "
          "{ref:jiang} xét ảo giác ở mức thuộc tính sản phẩm nhưng không biểu diễn điều kiện để giá trị thuộc "
          "tính đúng. Trong các tài liệu đã khảo sát, chưa thấy nghiên cứu kiểm chứng tuyên bố thông số có "
          "điều kiện ràng buộc trong quảng cáo tiếng Việt bằng phép đối chiếu tường minh điều kiện."),
     ])],

    # ----- 2. Phát biểu bài toán -----
    [("sub", [N("2. Phát biểu bài toán", b=True)]),
     ("text", [N("Đầu vào gồm một bài quảng cáo q do LLM tạo, mẫu sản phẩm s do người dùng chọn và kho tài liệu "
                 "chính hãng D(s) của mẫu đó. Tuyên bố có điều kiện ràng buộc là tuyên bố nêu giá trị của một "
                 "thuộc tính nằm trong danh sách thuộc tính có điều kiện ràng buộc của nhóm sản phẩm, tức các "
                 "thuộc tính mà hãng thường công bố kèm điều kiện. Với mỗi tuyên bố c thuộc loại này trong q, "
                 "hệ thống trả về nhãn y(c), đoạn nguồn e(c) trích từ D(s) và lý do r(c). Điều kiện mà tuyên "
                 "bố không nêu được hiểu theo cách hiểu thông thường ghi trong tệp cấu hình của nhóm sản phẩm "
                 "(ví dụ bộ phận chính, không mua thêm phụ kiện). Một giá trị được coi là khớp khi bằng giá trị "
                 "công bố sau chuẩn hóa, hoặc kém thuận lợi hơn giá trị đó (ví dụ nêu thời lượng pin thấp hơn). "
                 "Bốn nhãn được định nghĩa như sau:")]),
     ],
    [("dash", [N("Đúng: tài liệu có thông số cùng sản phẩm, thuộc tính và điều kiện với tuyên bố, giá trị khớp và "
                 "kiểu giá trị không bị đổi.")])],
    [("dash", [N("Sai: tài liệu có thông số cùng sản phẩm và thuộc tính, nhưng giá trị của tuyên bố mâu thuẫn với "
                 "giá trị công bố ở điều kiện của tuyên bố hoặc thuận lợi hơn mọi giá trị được công bố, đồng thời "
                 "không trùng giá trị nào ở điều kiện khác.")])],
    [("dash", [N("Lệch điều kiện: giá trị trong tuyên bố trùng giá trị được công bố ở một điều kiện khác với điều kiện "
                 "mà tuyên bố nêu hoặc được hiểu thông thường (bỏ hoặc đổi chế độ, bộ phận, phụ kiện, phiên bản, "
                 "điều kiện đo), hoặc tuyên bố biến mức tối đa “lên đến” thành mức chắc chắn đạt.")])],
    [("dash", [N("Chưa đủ thông tin: kho tài liệu không có thông số cùng sản phẩm và thuộc tính, không công bố giá "
                 "trị ở điều kiện mà tuyên bố nêu, hoặc ghi mâu thuẫn.")])],

    # ----- 3. Tính mới, đóng góp và cải tiến -----
    [("sub", [N("3. Tính mới, đóng góp và cải tiến so với các phương pháp kiểm chứng hiện có", b=True)]),
     ("text", [N("Đề tài không xây dựng lại một hệ thống kiểm chứng tổng quát mà tập trung khắc phục hạn chế "
                 "nêu trên cho tuyên bố có điều kiện ràng buộc.")]),
     ("text", [N("Tính mới.", b=True, i=True)]),
     ("dash", [N("Cụ thể hóa lớp tuyên bố gây hiểu nhầm (tương tự nhãn Cherry-picking của AVeriTeC "
                 "{ref:averitec}) thành nhãn Lệch điều kiện cho thông số kỹ thuật. Nhãn này được xác định bằng "
                 "phép đối chiếu điều kiện tường minh thay vì để LLM tự phán đoán.")]),
     ],
    [("dash", [N("Biểu diễn mỗi thông số, ở cả tuyên bố và tài liệu, thành bộ (sản phẩm và phiên bản, bộ phận, "
                 "thuộc tính, giá trị, đơn vị, điều kiện ràng buộc, kiểu giá trị). LLM trích xuất bộ này nhưng "
                 "mỗi trường phải kèm câu trích nguyên văn; Python kiểm tra câu trích có trong văn bản và con số "
                 "khớp với giá trị, trường không neo được vào nguồn thì bị loại. Neo nguồn loại bỏ giá trị và điều "
                 "kiện mà LLM tự thêm; bước kiểm tra đầy đủ theo các cách diễn đạt điều kiện ghi trong tệp cấu hình "
                 "phát hiện điều kiện bị LLM bỏ sót. Biểu diễn và bộ quyết định được thiết kế không gắn với một "
                 "nhóm sản phẩm cụ thể; khi thêm nhóm mới, phần cần bổ sung là danh sách thuộc tính và điều kiện "
                 "bắt buộc của nhóm đó.")])],
    [("text", [N("Đóng góp.", b=True, i=True)]),
     ("dash", [N("Phương pháp P kiểm chứng tuyên bố có điều kiện ràng buộc, gồm trích xuất có neo nguồn và bộ "
                 "quyết định bốn nhãn, được cài đặt thành mã nguồn có kiểm thử cho từng quy tắc.")]),
     ],
    [("dash", [N("Bộ dữ liệu tiếng Việt gồm các tuyên bố thông số có điều kiện ràng buộc trong quảng cáo do LLM "
                 "tạo, gán bốn nhãn kèm đoạn nguồn và lý do, cùng tập cặp tối thiểu dựa trên ý tưởng cặp tương "
                 "phản của VitaminC {ref:vitaminc} để đo riêng từng loại lệch điều kiện.")])],
    [("dash", [N("Kết quả đánh giá có đối chứng: so sánh P với bốn phương pháp đối chứng đại diện cho các cách kiểm "
                 "chứng hiện có và hai bản bỏ thành phần, trên cùng tuyên bố, cùng bằng chứng và cùng LLM.")])],
    [("dash", [N("Tính năng “Kiểm chứng thông số” trong CopyPro, giúp người viết quảng cáo phát hiện và sửa tuyên "
                 "bố sai hoặc lệch điều kiện trước khi đăng.")])],
    [("text", [N("Cải tiến so với các phương pháp hiện có.", b=True, i=True)]),
     ("dash", [N("So với cách kiểm chứng ba nhãn như FEVER {ref:fever} và các hệ thống tiếng Việt "
                 "{ref:vifactcheck}, {ref:semviqa}: thêm nhãn và bước đối chiếu điều kiện, nên tuyên bố đúng con "
                 "số nhưng sai điều kiện không còn bị chấp nhận là Đúng; kỳ vọng giảm FAR (tỷ lệ tuyên bố không "
                 "đúng bị chấp nhận là Đúng).")]),
     ],
    [("dash", [N("So với cách để LLM gán bốn nhãn chỉ bằng câu lệnh theo kiểu AVeriTeC {ref:averitec}: nhãn được "
                 "quyết định bằng quy tắc tường minh trên dữ liệu đã neo nguồn nên giải thích và kiểm thử được, trong "
                 "khi đối chứng cũng nhận cùng hướng dẫn gán nhãn dưới dạng văn bản; "
                 "kỳ vọng tăng F1 của nhãn Lệch điều kiện, lớp mà Fathom {ref:fathom} đạt F1 bằng 0.")])],
    [("dash", [N("So với hướng LLM trích thông tin kết hợp quy tắc của {ref:paclic}: kiểm chứng từng tuyên bố thay "
                 "vì một nhãn cho cả bài, so khớp theo điều kiện thay vì theo ngưỡng độ tương đồng, và kiểm tra "
                 "câu trích để LLM không thêm hoặc bỏ điều kiện.")])],
    [("dash", [N("So với phát hiện ảo giác ở mức thuộc tính {ref:jiang} và kiểm tra mức khớp với tài liệu nền "
                 "{ref:minicheck}: đưa điều kiện ràng buộc vào đơn vị so khớp, nên phân biệt được tuyên bố sai giá "
                 "trị với tuyên bố lệch điều kiện.")])],

    # ----- Mục tiêu -----
    [("label", [K("Mục tiêu:", b=True)]),
     ("dash", [N("M1. "),
               K("Thu thập các quảng cáo về "),
               N("điện thoại thông minh, tai nghe không dây và đồng hồ thông minh"),
               K(" do LLM tạo ra và tài liệu tham chiếu của đúng sản phẩm được quảng cáo để làm bằng chứng kiểm chứng"),
               N("; tách các tuyên bố về thông số có điều kiện ràng buộc, gán nhãn bốn lớp và tạo tập cặp tối "
                 "thiểu theo từng loại lệch điều kiện."),
               ])],
    [("dash", [N("M2. Đề xuất và cài đặt phương pháp P kiểm chứng tuyên bố có điều kiện ràng buộc, gồm trích xuất "
                 "bộ thông số có neo nguồn và bộ quyết định bốn nhãn dựa trên đối chiếu điều kiện.")])],
    [("dash", [N("M3. "),
               K("Xây dựng và so sánh P với "),
               N("các phương pháp đối chứng (B0–B3) và các bản bỏ thành phần"),
               K(", nhằm xác định "),
               N("phương pháp"),
               K(" có giúp giảm chấp nhận nhầm quảng cáo"),
               N(" và phát hiện tốt hơn tuyên bố lệch điều kiện"),
               K(" hay không."),
               ])],
    [("dash", [N("M4. Tích hợp tính năng kiểm chứng vào website CopyPro để người dùng xem nhãn, đoạn nguồn và "
                 "lý do của từng tuyên bố ngay sau khi tạo quảng cáo.")])],

    # ----- Phạm vi -----
    [("label_text", [
        K("Phạm vi:", b=True),
        K(" Kiểm chứng các "),
        N("tuyên bố về thông số kỹ thuật có điều kiện ràng buộc"),
        K(" trong quảng cáo tiếng Việt do LLM tạo về "),
        N("thiết bị điện tử tiêu dùng có tài liệu thông số chính hãng; thực nghiệm giới hạn ở ba nhóm đại diện: "
          "điện thoại thông minh, tai nghe không dây và đồng hồ thông minh"),
        K(", tập trung vào "),
        N("sáu nhóm thông số thường được công bố kèm điều kiện: thời lượng pin, dung lượng pin, sạc nhanh, "
          "kháng nước và bụi, màn hình (độ sáng, tần số quét) và zoom camera."),
        K(" Hệ thống chỉ sử dụng tài liệu văn bản của đúng sản phẩm làm bằng chứng"),
        N("; nhãn Chưa đủ thông tin nghĩa là không tìm thấy thông tin trong kho tài liệu đã thu thập."),
     ])],
    [("dash", [N("Điều kiện ràng buộc được xét gồm sáu loại: chế độ hoạt động (bật hoặc tắt chống ồn, chế độ tiết "
                 "kiệm pin), bộ phận (tai nghe hay hộp sạc), phụ kiện (bộ sạc có công suất nhất định), điều kiện đo "
                 "(độ sâu và thời gian ngâm nước, phần diện tích màn hình được đo), phiên bản sản phẩm và kiểu giá "
                 "trị (“lên đến”, “tối đa”, “điển hình”, “định mức”).")])],
    [("dash", [N("Lý do chọn thiết bị điện tử tiêu dùng trong các ngành CopyPro hỗ trợ: đây là nhóm có trang "
                 "thông số chính hãng công khai, ghi rõ con số và điều kiện đo. Quảng cáo ở các ngành như mỹ phẩm, "
                 "ẩm thực hay du lịch chủ yếu nêu cảm nhận, giá, ưu đãi hoặc số liệu từ thử nghiệm không công bố, "
                 "nên khó có bằng chứng văn bản chuẩn để đối chiếu.")])],
    [("dash", [N("Tiêu chí chọn nhóm sản phẩm: phương pháp áp dụng được cho một nhóm thiết bị điện tử tiêu dùng khi "
                 "(1) hãng có trang thông số chính thức bằng tiếng Việt để làm bằng chứng và (2) thông số là số liệu "
                 "đo được, được công bố kèm điều kiện ràng buộc. Nhóm được đưa vào thực nghiệm phải thỏa thêm: (3) "
                 "có chung các nhóm thông số pin, sạc và kháng nước để so sánh kết quả giữa các nhóm trên cùng loại "
                 "thông số; (4) có sản phẩm của cùng các hãng để nguồn bằng chứng đồng nhất.")])],
    [("dash", [N("Ba nhóm được chọn thỏa cả bốn tiêu chí. Với điện thoại, độ sáng cực đại 3200 nit của Xiaomi 15T "
                 "được công bố “trên 25% diện tích màn hình” {ref:xiaomi}; độ sáng tối đa 4500 nit của OPPO Find X8 "
                 "được ghi kèm điều kiện 1% APL, tức chỉ một vùng rất nhỏ của màn hình hiển thị sáng {ref:oppo}. Với tai nghe, Galaxy Buds3 Pro "
                 "phát nhạc lên đến 6 giờ khi bật chống ồn và 7 giờ khi tắt, đạt IP57 ở tai nghe nhưng hộp sạc "
                 "không có khả năng kháng nước {ref:samsung_buds}. Với đồng hồ, Apple Watch SE 3 dùng được lên đến "
                 "18 giờ ở chế độ thường và 32 giờ ở Chế Độ Nguồn Điện Thấp {ref:apple_watch}.")])],
    [("dash", [N("Sản phẩm: khoảng 12 mẫu (khoảng 5 điện thoại, 4 tai nghe không dây, 3 đồng hồ thông minh) "
                 "đang bán chính hãng tại Việt Nam của ít nhất ba hãng (dự kiến Apple, Samsung, Xiaomi, OPPO), ưu "
                 "tiên các trang có chú thích điều kiện đầy đủ.")])],
    [("dash", [N("Quảng cáo: do CopyPro tạo ở ngành Công nghệ bằng hai LLM có sẵn trên website (Gemini 2.5 Flash "
                 "và Llama 3.3 70B) với ba loại bài có sẵn (mô tả sản phẩm, bài đăng mạng xã hội, trang đích), ở "
                 "hai chế độ: chỉ nhập tên sản phẩm, và nhập thêm đoạn thông số chính hãng vào ô thông tin bổ sung.")])],
    [("dash", [N("Không thuộc phạm vi: tuyên bố về thông số không kèm điều kiện (ví dụ khối lượng, kích thước, "
                 "phiên bản Bluetooth), tuyên bố cảm tính (ví dụ “đẹp nhất”, “mượt mà”), so sánh với sản phẩm khác, "
                 "giá và khuyến mãi. Máy tính xách tay, máy tính bảng, tivi và đồ gia dụng không thuộc phạm vi thực "
                 "nghiệm: các nhóm này dùng được cùng cách biểu diễn và bộ quyết định nhưng cần định nghĩa thêm nhiều "
                 "thuộc tính và điều kiện bắt buộc riêng (ví dụ thông số thay đổi theo cấu hình máy, điện năng tiêu "
                 "thụ theo tiêu chuẩn đo); khối lượng gán nhãn khi đó vượt quá sức một người trong thời gian khóa "
                 "luận nên được để lại làm hướng mở rộng. Đề tài không đo hiệu năng thực tế và không đưa ra kết "
                 "luận pháp lý. Người dùng chọn mẫu sản phẩm khi kiểm chứng, hệ thống không tự nhận diện sản phẩm.")])],

    # ----- Đối tượng -----
    [("label_text", [
        K("Đối tượng:", b=True),
        K(" Các phương pháp kiểm chứng tuyên bố quảng cáo do LLM tạo bằng bằng chứng văn bản, tập trung phát "
          "hiện thông số không phù hợp với tài liệu của sản phẩm hoặc phiên bản được quảng cáo, cũng như các "
          "thông số được áp dụng sai điều kiện."),
        N(" Dữ liệu nghiên cứu là các tuyên bố về thông số có điều kiện ràng buộc trong quảng cáo tiếng Việt về "
          "điện thoại thông minh, tai nghe không dây, đồng hồ thông minh và trang thông số chính hãng tương ứng."),
     ])],

    # ----- Phương pháp thực hiện: Nội dung 1 -----
    [("label", [K("Phương pháp thực hiện:", b=True)]),
     ("sub", [N("Nội dung 1 (ứng với M1): Xây dựng dữ liệu kiểm chứng", b=True)]),
     ("dash", [N("Thu thập trang thông số chính hãng của các mẫu sản phẩm đã chọn, lưu đường dẫn, ngày truy "
                 "cập, bản chụp và mã băm để truy vết. "),
               K("Chia tài liệu thành các đoạn nhưng giữ thông số cùng điều kiện đi kèm.")]),
     ],
    [("dash", [N("Lập danh sách thuộc tính có điều kiện ràng buộc và điều kiện bắt buộc của từng thuộc tính cho "
                 "mỗi nhóm sản phẩm (ví dụ sạc nhanh cần công suất bộ sạc, độ sáng cần chế độ hiển thị, zoom cần "
                 "phân biệt quang học và kỹ thuật số, pin tai nghe cần chế độ chống ồn và có tính hộp sạc hay "
                 "không, pin đồng hồ cần chế độ sử dụng), lưu thành tệp cấu hình.")])],
    [("dash", [N("Sinh quảng cáo bằng CopyPro theo hai chế độ nêu ở phần phạm vi; lưu câu lệnh, mô hình, tham "
                 "số và đầu ra của mỗi lần sinh.")])],
    [("dash", [K("Tách nội dung quảng cáo thành các "),
               N("tuyên bố"),
               K(" nhỏ có thể kiểm chứng độc lập, đồng thời giữ lại ngữ cảnh"),
               N(" (sản phẩm, phiên bản, bộ phận, điều kiện)"),
               K(" để không làm thay đổi ý nghĩa ban đầu, giống như hướng kiểm chứng từng phát biểu nhỏ của "
                 "FactLens {ref:factlens}."),
               N(" Chỉ giữ các tuyên bố có thuộc tính nằm trong danh sách thuộc tính có điều kiện ràng buộc."),
               ])],
    [("dash", [N("Gán nhãn bốn lớp theo hướng dẫn viết trước; lưu đoạn bằng chứng và lý do. Gán lại ngẫu nhiên "
                 "20% số tuyên bố sau ít nhất 10 ngày với nhãn cũ được ẩn để đo độ nhất quán, và nhờ một người "
                 "thứ hai gán độc lập khoảng 60 tuyên bố theo cùng hướng dẫn để tính hệ số kappa của Cohen.")])],
    [("dash", [N("Tạo tập cặp tối thiểu: từ các tuyên bố Đúng, tạo biến thể bỏ điều kiện, đổi điều kiện, đổi bộ "
                 "phận, đổi kiểu giá trị (biến mức “lên đến” thành mức chắc chắn đạt), đổi giá trị và đổi phiên "
                 "bản; nhãn của mỗi biến thể được kiểm tra lại thủ công.")])],
    [("dash", [N("Chia dữ liệu theo mẫu sản phẩm thành tập phát triển (khoảng 4 mẫu, gồm 2 mẫu thử ban đầu, có "
                 "đủ ba nhóm) và tập kiểm tra cuối (các mẫu còn lại, nhóm sản phẩm và hãng nào cũng có mẫu) để "
                 "tránh rò rỉ thông tin giữa hai tập.")])],

    # ----- Nội dung 2 -----
    [("sub", [N("Nội dung 2 (ứng với M2): Phương pháp kiểm chứng có xét điều kiện ràng buộc (P)", b=True)]),
     ("dash", [K("Sử dụng BM25 làm phương pháp truy hồi nền để xếp hạng các đoạn tài liệu theo mức độ liên quan"),
               N(" {ref:bm25}"),
               K("; cách áp dụng BM25 được tham khảo từ giai đoạn đầu trong quy trình truy hồi bằng chứng của "
                 "Fathom {ref:fathom}."),
               N(" Chỉ tìm trong tài liệu của mẫu sản phẩm người dùng đã chọn."),
               ]),
     ],
    [("dash", [N("Trích xuất có neo nguồn: LLM chuyển tuyên bố và các đoạn bằng chứng thành bộ thông số (sản "
                 "phẩm và phiên bản, bộ phận, thuộc tính, giá trị, đơn vị, điều kiện ràng buộc, kiểu giá trị), mỗi "
                 "trường kèm câu trích nguyên văn. Python kiểm tra câu trích có trong văn bản gốc và con số trong "
                 "câu trích bằng giá trị đã trích; trường không đạt bị loại thay vì đoán. Sau đó kiểm tra đầy đủ: "
                 "điều kiện có trong văn bản (nhận theo các cách diễn đạt ghi trong tệp cấu hình) mà LLM bỏ sót "
                 "được bổ sung; nếu không xác định được thì kết luận Chưa đủ thông tin.")])],
    [("dash", [N("Tách và lọc tuyên bố tự động: LLM tách bài quảng cáo thành các tuyên bố, Python giữ lại tuyên "
                 "bố có thuộc tính trong tệp cấu hình. Bước này phục vụ tính năng trên CopyPro và được đánh giá "
                 "riêng bằng Precision và Recall so với tuyên bố tách thủ công.")])],
    [("dash", [K("Sử dụng Python để chuẩn hóa tên sản phẩm, phiên bản, giá trị và đơn vị đo về dạng biểu diễn "
                 "nhất quán trước khi so sánh"),
               N(", gồm cả từ chỉ kiểu giá trị như “lên đến”, “tối đa”, “điển hình”, “định mức”"),
               K("."),
               ])],
    [("dash", [N("Bộ quyết định bốn nhãn: A tìm thông số cùng sản phẩm và thuộc tính; B xác định điều kiện của tuyên "
                 "bố (điều kiện nêu rõ, hoặc cách hiểu thông thường với điều kiện không nêu) rồi đối chiếu với điều "
                 "kiện của từng thông số trong tài liệu, gồm chế độ hoạt động, bộ phận, phụ kiện, phiên bản, điều "
                 "kiện đo và kiểu giá trị; C so giá trị theo đơn vị và hướng thuận lợi của thuộc tính; D tổng hợp "
                 "nhãn theo thứ tự: không có thông số cùng sản phẩm và thuộc tính → Chưa đủ thông tin; mức tối đa "
                 "bị biến thành mức chắc chắn đạt → Lệch điều kiện; cùng điều kiện và giá trị khớp → Đúng; giá "
                 "trị trùng giá trị ở điều kiện khác → Lệch điều kiện; cùng điều kiện nhưng giá trị mâu thuẫn, "
                 "hoặc giá trị thuận lợi hơn mọi giá trị công bố → Sai; còn lại → Chưa đủ thông tin. Danh sách "
                 "thuộc tính và điều kiện bắt buộc của từng nhóm sản phẩm được lưu thành tệp cấu hình tách khỏi "
                 "các quy tắc A–D, nên thêm nhóm sản phẩm mới không phải sửa bộ quyết định.")])],
    [("dash", [N("Lý do trả về cho người dùng được sinh từ dấu vết của bộ quyết định (bước kết luận, đoạn "
                 "nguồn, điều kiện bị thiếu hoặc bị đổi), không để LLM viết tự do. Quy trình tổng thể được trình "
                 "bày ở Hình 1.")])],
    [("image", HINH_1),
     ("caption", [N("Hình 1. Quy trình kiểm chứng đề xuất; khối nền xám là thành phần mới của đề tài.", i=True)])],

    # ----- Nội dung 3 -----
    [("sub", [N("Nội dung 3 (ứng với M3): Thực nghiệm và đánh giá", b=True)]),
     ("dash", [K("Cài đặt và so sánh B0 (LLM đọc trực tiếp rồi gán nhãn"),
               N(" theo ba lớp Supported, Refuted, NEI, đại diện cho cách kiểm chứng phổ biến {ref:fever}"),
               K("), B1 (LLM nhận thông tin có cấu trúc rồi gán nhãn"),
               N(" theo bốn lớp, dùng cùng bộ thông số và cùng hướng dẫn gán nhãn với P để tách riêng tác động của bộ "
                 "quyết định"),
               K(") và P (LLM trích xuất thông tin"),
               N(" có neo nguồn"),
               K(", Python dùng "),
               N("bộ quyết định có đối chiếu điều kiện"),
               K(" để gán nhãn)."),
               ]),
     ],
    [("dash", [N("Bổ sung B2: LLM đọc bằng chứng và gán bốn nhãn theo hướng dẫn gán nhãn, có định nghĩa và ví dụ "
                 "cho nhãn Lệch điều kiện theo cách đặt nhãn của AVeriTeC {ref:averitec}, đại diện cho cách khắc "
                 "phục chỉ bằng câu lệnh; B3: mô hình phân loại ba nhãn tiếng Việt đã huấn luyện sẵn do nhóm SemViQA {ref:semviqa} "
                 "công bố, chạy trên cặp (tuyên bố, bằng chứng), đại diện cho hệ thống kiểm chứng tiếng Việt sẵn "
                 "có. Với B0 và B3 chỉ có ba nhãn, so sánh chính dựa trên FAR và các nhãn chung.")])],
    [("dash", [N("Phân tích thành phần: P−ĐK bỏ bước đối chiếu điều kiện (chỉ so giá trị), P−NN bỏ bước neo "
                 "nguồn. Mọi phương pháp dùng cùng tuyên bố, cùng top-k đoạn bằng chứng, cùng LLM và cùng cấu "
                 "hình.")])],
    [("dash", [K("Đánh giá bằng FAR (tỷ lệ chấp nhận nhầm), Precision (độ chính xác của dự đoán), Recall (khả "
                 "năng tìm đủ mẫu đúng) và F1 (chỉ số cân bằng giữa Precision và Recall)"),
               N(" của từng nhãn và Macro-F1; FAR là tỷ lệ tuyên bố bị gán Đúng trong số các tuyên bố có nhãn chuẩn "
                 "khác Đúng. Đo thêm Recall@k của BM25, độ đúng từng trường trích xuất, Precision và Recall của "
                 "bước tách tuyên bố tự động, thời gian và chi phí gọi LLM. Khoảng tin cậy 95% được ước lượng bằng "
                 "bootstrap theo cụm quảng cáo; chênh lệch FAR giữa P và từng đối chứng được kiểm định bằng "
                 "McNemar có hiệu chỉnh Holm cho nhiều phép so sánh."),
               ])],
    [("dash", [N("Giả thuyết: P có FAR thấp hơn B0–B3 và F1 của nhãn Lệch điều kiện cao hơn B1, B2, trong khi Recall "
                 "của nhãn Đúng không thấp hơn quá 5 điểm phần trăm so với đối chứng tốt nhất. Mô hình, câu lệnh và "
                 "giá trị k được chọn trên tập phát triển và khóa trước khi chạy tập kiểm tra; kết quả được báo "
                 "cáo cả khi không đạt giả thuyết.")])],
    [("dash", [N("Báo kết quả riêng cho tuyên bố từ quảng cáo thông thường và cho tập cặp tối thiểu, theo từng "
                 "loại biến đổi, từng nhóm sản phẩm, từng hãng và từng LLM sinh quảng cáo; báo thêm kết quả đầu–cuối "
                 "(tách tuyên bố tự động rồi kiểm chứng) trên quảng cáo của tập kiểm tra; phân tích lỗi theo nguồn "
                 "gốc: tách tuyên bố, truy hồi, trích xuất hay quyết định.")])],

    # ----- Nội dung 4 -----
    [("sub", [N("Nội dung 4 (ứng với M4): Tích hợp vào website CopyPro", b=True)]),
     ("dash", [N("Thêm chức năng “Kiểm chứng thông số” vào trang kết quả tạo nội dung: người dùng chọn mẫu "
                 "sản phẩm, hệ thống đánh dấu từng tuyên bố theo bốn nhãn, hiển thị đoạn nguồn chính hãng và lý "
                 "do, đặt cạnh điểm chất lượng và kết quả kiểm tra đạo văn hiện có; kết quả được lưu cùng nội dung "
                 "đã tạo.")]),
     ],
    [("dash", [N("Kiểm tra chức năng trên các quảng cáo thuộc tập kiểm tra và đo thời gian kiểm chứng một bài "
                 "quảng cáo.")])],

    # ----- Kết quả mong đợi -----
    [("label", [K("Kết quả mong đợi:", b=True)]),
     ("dash", [K("Bộ dữ liệu gồm các "),
               N("tuyên bố thông số có điều kiện ràng buộc từ"),
               K(" quảng cáo"),
               N(" do LLM tạo (khoảng 250–300 tuyên bố và 100–120 biến thể cặp tối thiểu của khoảng 12 mẫu "
                 "thuộc ba nhóm sản phẩm)"),
               K(", tài liệu làm bằng chứng và nhãn kiểm chứng"),
               N(" bốn lớp, kèm lý do, hướng dẫn gán nhãn và tệp điều kiện bắt buộc của ba nhóm sản phẩm"),
               K("."),
               ]),
     ],
    [("dash", [K("Hệ thống trả về nhãn "),
               N("Đúng (Supported), Sai (Refuted), Lệch điều kiện (Misleading) hoặc Chưa đủ thông tin (NEI)"),
               K(", kèm đoạn nguồn và lý do."),
               ])],
    [("dash", [N("Phương pháp P, các đối chứng B0–B3 và hai bản bỏ thành phần"),
               K(" hoạt động được trên cùng bộ dữ liệu"),
               N("; mã nguồn P có kiểm thử cho từng quy tắc của bộ quyết định"),
               K("."),
               ])],
    [("dash", [K("Báo cáo thực nghiệm xác định phương pháp P có giảm FAR (tỷ lệ chấp nhận nhầm) so với "),
               N("B0–B3 và có phát hiện tốt hơn tuyên bố Lệch điều kiện"),
               K(" mà không bỏ sót quá nhiều thông tin đúng hay không"),
               N("; báo cáo cả trường hợp không cải thiện"),
               K("."),
               ])],
    [("dash", [K("Website minh họa cho phép người dùng tạo quảng cáo và xem kết quả kiểm chứng"),
               N(": tính năng “Kiểm chứng thông số” được tích hợp vào CopyPro"),
               K("."),
               ])],
]

# ---------------------------------------------------------------------------
# Phần 2: Kế hoạch thực hiện, rủi ro, tài liệu tham khảo
# ---------------------------------------------------------------------------
SEC_KE_HOACH = [
    [("label_keep", [K("Kế hoạch thực hiện:", b=True), K(" Nhóm có 1 thành viên")]),
     ("month", [K("Tháng 09/2026:", b=True)]),
     ("plus", [K("Khảo sát các nghiên cứu về kiểm chứng thông tin, truy hồi bằng chứng, kiểm chứng phát biểu "
                 "chứa số liệu và suy luận có điều kiện.")]),
     ],
    [("plus", [K("Xây dựng tiêu chí chọn nguồn, cấu trúc lưu dữ liệu và hướng dẫn gán nhãn.")])],
    [("plus", [K("Soạn ít nhất 20 ví dụ gán nhãn minh họa cho các trường hợp đúng, sai đối tượng, sai điều kiện, "
                 "thiếu và xung đột bằng chứng. Khi tách thông tin quảng cáo, phải giữ lại sản phẩm, phiên bản, "
                 "thuộc tính và điều kiện cần thiết để phát biểu không thay đổi ý nghĩa.")])],
    [("plus", [K("Kiểm tra tài nguyên máy và thử các LLM mã nguồn mở có kích thước phù hợp để thử trên bộ "
                 "pilot.")])],

    [("month", [K("Tháng 10/2026:", b=True)]),
     ("plus", [N("Điều chỉnh đề tài theo nhận xét của Khoa: tập trung vào tuyên bố về thông số kỹ thuật có điều "
                 "kiện ràng buộc, mở rộng từ tai nghe không dây sang thiết bị điện tử tiêu dùng với ba nhóm thực "
                 "nghiệm có tiêu chí chọn rõ ràng, bổ sung tổng quan, hạn chế của các phương pháp hiện có, tính "
                 "mới và đóng góp; thống nhất tên đề tài với cán bộ hướng dẫn.")]),
     ],
    [("plus", [N("Khảo sát bổ sung các nghiên cứu về phát hiện ảo giác của LLM, kiểm chứng thông tin sản phẩm "
                 "và kiểm chứng tiếng Việt.")])],
    [("plus", [N("Chọn khoảng 12 mẫu thuộc ba nhóm sản phẩm của ít nhất ba hãng theo bốn tiêu chí đã nêu; thu "
                 "thập trang thông số chính hãng, lưu bản chụp và mã băm (ưu tiên 2 mẫu thử ban đầu: 1 điện thoại, "
                 "1 tai nghe). "),
               K("Chia tài liệu thành các đoạn nhưng giữ thông số cùng điều kiện đi kèm.")])],
    [("plus", [N("Định nghĩa điều kiện bắt buộc cho sáu nhóm thông số, lưu thành tệp cấu hình theo nhóm sản phẩm; "
                 "viết hướng dẫn gán nhãn bốn lớp; giữ các ví dụ minh họa về tai nghe và bổ sung ví dụ cho điện "
                 "thoại, đồng hồ thông minh.")])],
    [("plus", [K("Thu thập bộ pilot (bộ thử ban đầu) khoảng 60 "),
               N("tuyên bố có điều kiện ràng buộc từ quảng cáo do CopyPro tạo cho 2 mẫu thử ban đầu"),
               K(", kèm tài liệu và đường dẫn đến nguồn chính thức của đúng sản phẩm và phiên bản được quảng cáo."),
               ])],
    [("plus", [K("Gán nhãn thủ công và lưu lý do cho từng thông tin"),
               N(" theo bốn lớp; đo thời gian gán nhãn để chốt quy mô dữ liệu"),
               K("."),
               ])],
    [("plus", [K("Xây dựng mô-đun truy hồi BM25 để xếp hạng và chọn top-k đoạn nguồn liên quan.")])],
    [("plus", [K("Xây dựng B0 (LLM đọc trực tiếp thông tin và bằng chứng rồi tự gán nhãn).")])],
    [("plus", [K("Phân tích lỗi trên bộ pilot để điều chỉnh hướng dẫn nhãn và cấu trúc dữ liệu.")])],

    [("month", [K("Tháng 11/2026:", b=True)]),
     ("plus", [K("Mở rộng và hoàn thiện bộ dữ liệu chính theo quy mô khả thi sau khi chốt thử trên bộ pilot."),
               N(" Sinh quảng cáo cho các mẫu sản phẩm còn lại, tạo tập cặp tối thiểu, gán lại 20% số tuyên bố và "
                 "nhờ người thứ hai gán độc lập khoảng 60 tuyên bố."),
               ]),
     ],
    [("plus", [K("Chia dữ liệu theo "),
               N("mẫu sản phẩm"),
               K(" thành tập phát triển"),
               N(" và"),
               K(" tập kiểm tra cuối."),
               ])],
    [("plus", [K("Xây dựng chức năng dùng LLM trích xuất "),
               N("có neo nguồn cho "),
               K("sản phẩm, phiên bản, bộ phận, thông số, giá trị, đơn vị và điều kiện áp dụng"),
               N(" cùng kiểu giá trị; xây dựng bước tách tuyên bố tự động"),
               K("."),
               ])],
    [("plus", [K("Sử dụng Python để chuẩn hóa tên sản phẩm, phiên bản, giá trị và đơn vị đo về dạng biểu diễn "
                 "nhất quán trước khi so sánh.")])],
    [("plus", [N("Xây dựng bộ quyết định bốn nhãn: A kiểm tra khớp sản phẩm, phiên bản, bộ phận và thuộc tính; B "
                 "đối chiếu điều kiện ràng buộc; C so giá trị; D tổng hợp nhãn và sinh lý do; kiểm thử riêng từng "
                 "quy tắc.")])],
    [("plus", [K("Hoàn thiện P (LLM trích xuất thông tin, Python dùng "),
               N("bộ quyết định bốn nhãn"),
               K(" để gán nhãn)."),
               ])],
    [("plus", [K("Xây dựng B1 (LLM nhận thông tin đã được cấu trúc nhưng vẫn tự gán nhãn)"),
               N(", B2 và B3"),
               K("."),
               ])],
    [("plus", [K("Xây dựng các phiên bản "),
               N("bỏ đối chiếu điều kiện (P−ĐK) và bỏ neo nguồn (P−NN)"),
               K(" để đánh giá vai trò của từng thành phần"),
               K("."),
               ])],
    [("plus", [K("Để bảo đảm so sánh công bằng, "),
               N("các phương pháp"),
               K(" sử dụng cùng phát biểu, cùng top-k đoạn bằng chứng, cùng LLM và cùng cấu hình. B1 và P nhận "
                 "cùng thông tin đã được cấu trúc; điểm khác nhau là B1 để LLM quyết định nhãn, còn P sử dụng mã "
                 "Python và bộ quyết định "),
               N("bốn nhãn"),
               K("."),
               ])],
    [("plus", [K("Chọn mô hình, giá trị k và các ngưỡng trên tập "),
               N("phát triển"),
               K("; sau đó giữ cố định cấu hình."),
               ])],
    [("plus", [N("Bắt đầu tích hợp tính năng kiểm chứng vào CopyPro.")])],

    [("month", [K("Tháng 12/2026:", b=True)]),
     ("plus", [K("Chạy "),
               N("P, B0–B3, P−ĐK và P−NN trên tập kiểm tra cuối"),
               K(" để đánh giá vai trò của từng thành phần."),
               ]),
     ],
    [("plus", [K("Tính FAR (tỷ lệ chấp nhận nhầm), Precision (độ chính xác của dự đoán), Recall (khả năng tìm đủ "
                 "mẫu đúng), F1 và Macro-F1."),
               N(" Báo riêng F1 của nhãn Lệch điều kiện; ước lượng khoảng tin cậy bằng bootstrap và kiểm định "
                 "McNemar."),
               ])],
    [("plus", [K("So sánh khả năng tìm bằng chứng của BM25 bằng Recall@k (tỷ lệ tìm đủ bằng chứng trong k đoạn "
                 "đầu).")])],
    [("plus", [K("Phân tích các lỗi sai sản phẩm, sai phiên bản, sai điều kiện, thiếu bằng chứng"),
               N(" theo nguồn gốc truy hồi, trích xuất hoặc quyết định"),
               K("."),
               ])],
    [("plus", [K("Kiểm tra P có giảm chấp nhận nhầm so với "),
               N("B0–B3"),
               K(" mà không bỏ sót quá nhiều thông tin đúng hay không."),
               ])],
    [("plus", [K("Tích hợp phương pháp P vào "),
               N("CopyPro"),
               K(" để người dùng "),
               N("chọn mẫu sản phẩm"),
               K(" và xem nhãn, bằng chứng, lý do."),
               ])],
    [("plus", [K("Hoàn thiện luận văn, biểu đồ, bảng kết quả, hướng dẫn cài đặt và hướng dẫn chạy lại.")])],
    [("plus", [K("Kiểm tra toàn bộ mã nguồn, dữ liệu trước ngày 31/12/2026.")])],

    # ----- Rủi ro -----
    [("label", [N("Rủi ro và phương án dự phòng:", b=True)]),
     ("dash", [N("Quảng cáo do LLM tạo chứa ít tuyên bố có điều kiện ràng buộc: tăng số bài sinh cho mỗi mẫu và "
                 "đưa các thông số nổi bật (pin, sạc, kháng nước) vào ô từ khóa như người viết quảng cáo thường "
                 "làm; tập cặp tối thiểu bảo đảm đủ mẫu cho từng loại lệch điều kiện.")]),
     ],
    [("dash", [N("Trang thông số của một số hãng thiếu chú thích điều kiện, hiển thị bằng mã động hoặc ghi không "
                 "nhất quán: ưu tiên hãng có chú thích đầy đủ, chụp lại trang sau khi hiển thị xong; thông số không "
                 "có hoặc mâu thuẫn trong tài liệu được gán Chưa đủ thông tin và thống kê riêng.")])],
    [("dash", [N("Gán nhãn chậm hơn dự kiến: giảm số tuyên bố từ quảng cáo thông thường nhưng giữ tập cặp tối "
                 "thiểu và giữ đủ các hãng trong tập kiểm tra.")])],
    [("dash", [N("Giới hạn lượt gọi API: lưu bộ nhớ đệm kết quả gọi LLM, dùng các mô hình đã có trên CopyPro "
                 "cho cả sinh quảng cáo và kiểm chứng.")])],
    [("dash", [N("Không đủ thời gian cho cả ba nhóm sản phẩm: giảm số mẫu mỗi nhóm nhưng giữ đủ ba nhóm "
                 "trong tập kiểm tra để vẫn so sánh được giữa các nhóm.")])],
    [("dash", [N("Không tìm được người gán thứ hai: chỉ báo độ nhất quán khi gán lại và ghi rõ giới hạn này, không "
                 "gọi là độ đồng thuận giữa hai người.")])],
]

# ---------------------------------------------------------------------------
# Tài liệu tham khảo. OLD_NUM = số thứ tự trong bản đã nộp (giữ nguyên chữ, chỉ đổi số).
# Mỗi mục là danh sách (chữ, in nghiêng?).
# ---------------------------------------------------------------------------
OLD_NUM = {"paclic": 1, "factlens": 2, "thinkright": 3, "clue": 4, "cover": 5, "fathom": 6}

REFS = {
    "paclic": [
        ("T. T. Nguyen, H. Nguyen Thi Phuong, T. P. Le, and B. T. Nguyen, “Fact-checking for online advertisement posts,” in ", False),
        ("Proceedings of the 38th Pacific Asia Conference on Language, Information and Computation (PACLIC)", True),
        (", 2024, pp. 398–406. [Online]. Available: https://aclanthology.org/2024.paclic-1.40/", False),
    ],
    "factlens": [
        ("K. Mitra, D. Zhang, S. Rahman, and E. Hruschka, “FactLens: Benchmarking fine-grained fact verification,” in ", False),
        ("Findings of the Association for Computational Linguistics: ACL 2025", True),
        (", 2025, pp. 18085–18096. https://doi.org/10.18653/v1/2025.findings-acl.929", False),
    ],
    "thinkright": [
        ("P. Chungkham, V. V, V. Setty, and A. Anand, “Think right, not more: Test-time scaling for numerical claim verification,” in ", False),
        ("Findings of the Association for Computational Linguistics: EMNLP 2025", True),
        (", 2025, pp. 24345–24363. https://doi.org/10.18653/v1/2025.findings-emnlp.1322", False),
    ],
    "clue": [
        ("J. Sun, G. Warren, I. Shklovski, and I. Augenstein, “Explaining sources of uncertainty in automated fact-checking,” in ", False),
        ("Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (ACL)", True),
        (", 2026, pp. 45510–45534. https://doi.org/10.18653/v1/2026.acl-long.2110", False),
    ],
    "cover": [
        ("S. Zhang et al., “CoVer: Conflict-aware claim verification,” arXiv preprint arXiv:2609.00508, 2026. [Online]. Available: https://arxiv.org/abs/2609.00508", False),
    ],
    "fathom": [
        ("F. B. Rashid and S. Hakak, “Fathom: A fast and modular RAG pipeline for fact-checking,” in ", False),
        ("Proceedings of the Eighth Fact Extraction and VERification Workshop (FEVER)", True),
        (", 2025, pp. 258–265. https://doi.org/10.18653/v1/2025.fever-1.20", False),
    ],
    # ---- Tài liệu mới ----
    "vihallu": [
        ("A. T.-H. Nguyen, K. Q. Tran, T. V. Huynh, P. T.-H. Nguyen, C. T. Nguyen, and K. V. Nguyen, “DSC2025 – ViHallu challenge: Detecting hallucination in Vietnamese LLMs,” arXiv preprint arXiv:2601.04711, 2026. [Online]. Available: https://arxiv.org/abs/2601.04711", False),
    ],
    "apple": [
        ("Apple Việt Nam, “iPhone 17 – Thông số kỹ thuật.” [Online]. Available: https://www.apple.com/vn/iphone-17/specs/ (truy cập ngày 09/10/2026).", False),
    ],
    "ftc": [
        ("M. Hastak and D. Murphy, “Effects of a Bristol Windows advertisement with an ‘up to’ savings claim on consumer take-away and beliefs,” U.S. Federal Trade Commission, Washington, DC, USA, Staff Report, Jun. 2012. [Online]. Available: https://www.ftc.gov/reports/effects-bristol-windows-advertisement-savings-claim-consumer-take-away-beliefs", False),
    ],
    "law": [
        ("Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam, ", False),
        ("Luật sửa đổi, bổ sung một số điều của Luật Quảng cáo", True),
        (", Luật số 75/2025/QH15, thông qua ngày 16/06/2025, có hiệu lực từ ngày 01/01/2026.", False),
    ],
    "guo": [
        ("Z. Guo, M. Schlichtkrull, and A. Vlachos, “A survey on automated fact-checking,” ", False),
        ("Transactions of the Association for Computational Linguistics", True),
        (", vol. 10, pp. 178–206, 2022. [Online]. Available: https://aclanthology.org/2022.tacl-1.11/", False),
    ],
    "fever": [
        ("J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, “FEVER: A large-scale dataset for fact extraction and VERification,” in ", False),
        ("Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT)", True),
        (", 2018, pp. 809–819. [Online]. Available: https://aclanthology.org/N18-1074/", False),
    ],
    "averitec": [
        ("M. Schlichtkrull, Z. Guo, and A. Vlachos, “AVeriTeC: A dataset for real-world claim verification with evidence from the web,” in ", False),
        ("Advances in Neural Information Processing Systems 36 (Datasets and Benchmarks Track)", True),
        (", 2023. [Online]. Available: https://arxiv.org/abs/2305.13117", False),
    ],
    "vifactcheck": [
        ("T. T. Hoa, T. Q. Duy, K. Q. Tran, and K. V. Nguyen, “ViFactCheck: A new benchmark dataset and methods for multi-domain news fact-checking in Vietnamese,” in ", False),
        ("Proceedings of the AAAI Conference on Artificial Intelligence", True),
        (", vol. 39, no. 1, 2025, pp. 308–316. https://doi.org/10.1609/aaai.v39i1.32008", False),
    ],
    "viwikifc": [
        ("H. T. Le, L. T. To, M. T. Nguyen, and K. V. Nguyen, “ViWikiFC: Fact-checking for Vietnamese Wikipedia-based textual knowledge source,” arXiv preprint arXiv:2405.07615, 2024. [Online]. Available: https://arxiv.org/abs/2405.07615", False),
    ],
    "vinumfcr": [
        ("N. N.-P. Luong, A. T.-L. Le, T. V. Huynh, K. V. Nguyen, and N. L.-T. Nguyen, “ViNumFCR: A novel Vietnamese benchmark for numerical reasoning fact checking on social media news,” in ", False),
        ("Proceedings of the 18th International Natural Language Generation Conference (INLG)", True),
        (", 2025, pp. 134–147. [Online]. Available: https://aclanthology.org/2025.inlg-main.9/", False),
    ],
    "semviqa": [
        ("D. X. Tran, N. V. Nguyen, T. T. Thanh, A. T. Hoang, D. V. Tai, L. T. Di, and P.-L. Le, “SemViQA: A semantic question answering system for Vietnamese information fact-checking,” in ", False),
        ("Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 6: Industry Track)", True),
        (", 2026, pp. 1341–1358. https://doi.org/10.18653/v1/2026.acl-industry.94", False),
    ],
    "numpert": [
        ("P. R. Aarnes and V. Setty, “NumPert: Numerical perturbations to probe language models for veracity prediction,” in ", False),
        ("Proceedings of the 14th International Joint Conference on Natural Language Processing and the 4th Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics: Student Research Workshop", True),
        (", 2025, pp. 78–95. [Online]. Available: https://aclanthology.org/2025.ijcnlp-srw.8/", False),
    ],
    "minicheck": [
        ("L. Tang, P. Laban, and G. Durrett, “MiniCheck: Efficient fact-checking of LLMs on grounding documents,” in ", False),
        ("Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP)", True),
        (", 2024, pp. 8818–8847. [Online]. Available: https://aclanthology.org/2024.emnlp-main.499/", False),
    ],
    "jiang": [
        ("L. Jiang, K. Jiang, X. Chu, S. Gulati, and P. Garg, “Hallucination detection in LLM-enriched product listings,” in ", False),
        ("Proceedings of the Seventh Workshop on e-Commerce and NLP (ECNLP) @ LREC-COLING 2024", True),
        (", 2024, pp. 29–39. [Online]. Available: https://aclanthology.org/2024.ecnlp-1.4/", False),
    ],
    "vitaminc": [
        ("T. Schuster, A. Fisch, and R. Barzilay, “Get your vitamin C! Robust fact verification with contrastive evidence,” in ", False),
        ("Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT)", True),
        (", 2021, pp. 624–643. [Online]. Available: https://aclanthology.org/2021.naacl-main.52/", False),
    ],
    "xiaomi": [
        ("Xiaomi Việt Nam, “Xiaomi 15T – Thông số kỹ thuật.” [Online]. Available: https://www.mi.com/vn/product/xiaomi-15t/specs/ (truy cập ngày 09/10/2026).", False),
    ],
    "oppo": [
        ("OPPO Việt Nam, “OPPO Find X8 – Thông số kỹ thuật.” [Online]. Available: https://www.oppo.com/vn/smartphones/series-find-x/find-x8/specs/ (truy cập ngày 09/10/2026).", False),
    ],
    "samsung_buds": [
        ("Samsung Việt Nam, “Galaxy Buds3 Pro – Thông số kỹ thuật.” [Online]. Available: https://www.samsung.com/vn/audio-sound/galaxy-buds/galaxy-buds3-pro-silver-sm-r630nzaaxxv/ (truy cập ngày 09/10/2026).", False),
    ],
    "apple_watch": [
        ("Apple Việt Nam, “Pin Apple Watch.” [Online]. Available: https://www.apple.com/vn/watch/battery/ (truy cập ngày 09/10/2026).", False),
    ],
    "bm25": [
        ("S. Robertson and H. Zaragoza, “The probabilistic relevance framework: BM25 and beyond,” ", False),
        ("Foundations and Trends in Information Retrieval", True),
        (", vol. 3, no. 4, pp. 333–389, 2009.", False),
    ],
}
