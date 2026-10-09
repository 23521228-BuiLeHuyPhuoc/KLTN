"""Dựng lại đề cương Đọc_báo_cùng_HuP_4_.docx theo sổ tay bản 2 (SAV, B01–B52).

Khung lấy từ HuP4 ở commit 7107507: giữ styles, numbering, bảng quốc hiệu, tiêu đề
“ĐỀ CƯƠNG CHI TIẾT”, bốn hàng thông tin (tên đề tài giữ nguyên từng chữ, chỉ bỏ màu đỏ)
và hàng ký tên; bỏ ghi chú nội bộ đầu trang; thay hai khung nội dung.
Dùng: python3 scripts/build_proposal.py   (chạy từ gốc repo)
"""
import io
import re
import subprocess
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
NAME = 'Đọc_báo_cùng_HuP_4_.docx'
TEMPLATE_COMMIT = '7107507'
OUT = ROOT / NAME
TITLE_VI = 'Phương pháp kiểm chứng phát biểu quảng cáo dựa trên bằng chứng văn bản cho tai nghe không dây'
TITLE_EN = 'Text-evidence-based method for verifying advertising claims about wireless headphones'

_raw = subprocess.run(['git', '-C', str(ROOT), 'show', f'{TEMPLATE_COMMIT}:{NAME}'], capture_output=True, check=True).stdout
zin = zipfile.ZipFile(io.BytesIO(_raw))
doc = zin.read('word/document.xml').decode('utf-8')
rels = zin.read('word/_rels/document.xml.rels').decode('utf-8')

# ---------- mẫu XML lấy từ HuP4 ----------
FONT = '<w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman"/>'
LINE = '<w:spacing w:after="80" w:line="278.00000000000006" w:lineRule="auto"/>'
PPR = {
    'plain': '<w:spacing w:after="80" w:line="278.00000000000006" w:lineRule="auto"/><w:ind w:right="102"/><w:jc w:val="both"/>',
    'label': '<w:keepNext w:val="1"/><w:keepLines w:val="1"/><w:spacing w:after="80" w:before="160" w:line="278.00000000000006" w:lineRule="auto"/><w:ind w:right="102"/><w:jc w:val="both"/>',
    'h2': '<w:pStyle w:val="Heading2"/><w:keepNext w:val="1"/><w:spacing w:after="80" w:before="160" w:line="278.00000000000006" w:lineRule="auto"/><w:ind w:right="102"/><w:jc w:val="both"/>',
    # '-' cấp 1 (numId 5: ý chính của phương pháp; 7: ý thường; 3: kết quả mong đợi)
    'b5': '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="5"/></w:numPr>' + LINE + '<w:ind w:left="397" w:right="102" w:hanging="198"/><w:jc w:val="both"/>',
    'b7': '<w:keepLines w:val="1"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="7"/></w:numPr>' + LINE + '<w:ind w:left="397" w:right="102" w:hanging="198"/><w:jc w:val="both"/>',
    'b3': '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="3"/></w:numPr>' + LINE + '<w:ind w:left="397" w:right="102" w:hanging="198"/><w:jc w:val="both"/>',
    # giai đoạn ('-', numId 6) và việc trong giai đoạn ('+', numId 11)
    'gate': '<w:keepNext w:val="1"/><w:keepLines w:val="1"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="6"/></w:numPr><w:spacing w:after="80" w:before="160" w:line="278.00000000000006" w:lineRule="auto"/><w:ind w:left="397" w:right="102" w:hanging="198"/><w:jc w:val="both"/>',
    'item': '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="11"/></w:numPr>' + LINE + '<w:ind w:left="794" w:right="102" w:hanging="197.99999999999997"/><w:jc w:val="both"/>',
    'ref': '<w:keepLines w:val="1"/><w:spacing w:after="140" w:before="60" w:line="278.00000000000006" w:lineRule="auto"/><w:ind w:right="102"/>',
}
TC_MAR = '<w:tcMar><w:top w:w="{t}" w:type="dxa"/><w:left w:w="90.0" w:type="dxa"/><w:bottom w:w="{b}" w:type="dxa"/><w:right w:w="90.0" w:type="dxa"/></w:tcMar>'
TC = {
    'first': '<w:tcPr><w:gridSpan w:val="2"/><w:tcBorders><w:top w:color="000000" w:space="0" w:sz="4" w:val="single"/><w:bottom w:color="000000" w:space="0" w:sz="0" w:val="nil"/></w:tcBorders>' + TC_MAR.format(t='55.0', b='0.0') + '</w:tcPr>',
    'mid': '<w:tcPr><w:gridSpan w:val="2"/><w:tcBorders><w:top w:color="000000" w:space="0" w:sz="0" w:val="nil"/><w:bottom w:color="000000" w:space="0" w:sz="0" w:val="nil"/></w:tcBorders>' + TC_MAR.format(t='0.0', b='0.0') + '</w:tcPr>',
    'last': '<w:tcPr><w:gridSpan w:val="2"/><w:tcBorders><w:top w:color="000000" w:space="0" w:sz="0" w:val="nil"/><w:bottom w:color="000000" w:space="0" w:sz="4" w:val="single"/></w:tcBorders>' + TC_MAR.format(t='0.0', b='55.0') + '</w:tcPr>',
}
TR_PR = '<w:trPr><w:cantSplit w:val="0"/><w:tblHeader w:val="0"/></w:trPr>'

# ---------- hyperlink cho tài liệu tham khảo ----------
_next_rid = [max(int(n) for n in re.findall(r'Id="rId(\d+)"', rels)) + 1]
_new_rels = []


def rid_for(url):
    rid = f'rId{_next_rid[0]}'
    _next_rid[0] += 1
    _new_rels.append(
        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
        f'Target="{escape(url, {chr(34): "&quot;"})}" TargetMode="External"/>')
    return rid


def rpr(bold=False, italic=False, link=False, size=26):
    s = FONT
    if bold:
        s += '<w:b w:val="1"/><w:bCs w:val="1"/>'
    if italic:
        s += '<w:i w:val="1"/><w:iCs w:val="1"/>'
    if link:
        s += '<w:color w:val="1155cc"/><w:u w:val="single"/>'
    s += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/><w:rtl w:val="0"/>'
    return s


def run(text, **kw):
    return f'<w:r><w:rPr>{rpr(**kw)}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


TOKEN = re.compile(r'(\*\*.+?\*\*|\*[^*\s][^*]*?\*|https?://[^\s]+)')


def runs(text, base_bold=False):
    """Đánh dấu nhẹ trong chuỗi: **đậm**, *nghiêng*, URL thành hyperlink."""
    out = []
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            out.append(run(part[2:-2], bold=True))
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            out.append(run(part[1:-1], italic=True, bold=base_bold))
        elif part.startswith('http'):
            url = part.rstrip('.,;)')
            tail = part[len(url):]
            out.append(f'<w:hyperlink r:id="{rid_for(url)}">{run(url, link=True)}</w:hyperlink>')
            if tail:
                out.append(run(tail, bold=base_bold))
        else:
            out.append(run(part, bold=base_bold))
    return ''.join(out)


def para(kind, text, bold=False):
    keep_bold = '<w:b w:val="1"/><w:bCs w:val="1"/>' if bold or kind == 'h2' else ''
    p_rpr = f'<w:rPr>{FONT}{keep_bold}<w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>'
    return f'<w:p><w:pPr>{PPR[kind]}{p_rpr}</w:pPr>{runs(text, base_bold=bold or kind == "h2")}</w:p>'


def block(rows):
    """rows: danh sách hàng, mỗi hàng là danh sách đoạn XML. Khung chỉ viền ngoài như HuP4."""
    xml = []
    for i, ps in enumerate(rows):
        pos = 'first' if i == 0 else 'last' if i == len(rows) - 1 else 'mid'
        xml.append(f'<w:tr>{TR_PR}<w:tc>{TC[pos]}{"".join(ps)}</w:tc></w:tr>')
    return ''.join(xml)


def label_row(label, text=None, bullets=(), kind='b7'):
    head = f'**{label}**' + (f' {text}' if text else '')
    return [[para('label', head)]] + [[para(kind, b)] for b in bullets]


def section(title, intro, bullets, kind='b7'):
    rows = [[para('h2', title)] + ([para('b5', intro)] if intro else [])]
    rows += [[para(kind, b)] for b in bullets]
    return rows


# =====================================================================
# NỘI DUNG ĐỀ CƯƠNG (đồng bộ với deliverables/KE_HOACH_CHI_TIET_SINH_VIEN.md, mục 1–3)
# =====================================================================
B1 = []
B1 += label_row('Nội dung đề tài:', 'Nghiên cứu phương pháp kiểm chứng từng phát biểu thông số (claim) trong quảng cáo tiếng Việt về tai nghe không dây do mô hình ngôn ngữ lớn (LLM) tạo ra, dùng tài liệu văn bản chính thức của hãng làm bằng chứng. Mỗi claim được gán Supported (được nguồn hỗ trợ), Refuted (bị nguồn bác bỏ) hoặc NEI (chưa đủ thông tin), kèm mã đoạn nguồn và lý do. Người dùng dự kiến là người duyệt nội dung quảng cáo: claim Refuted/NEI được gắn cờ để sửa hoặc tìm thêm nguồn trước khi đăng.')
B1 += [[para('plain', '**Vấn đề trọng tâm:** lỗi chấp nhận nhầm do *lệch phạm vi thông số* — con số trong quảng cáo trùng con số trong nguồn nhưng khác điều kiện thử (chống ồn bật/tắt), khác bộ phận (tai nghe/hộp sạc), khác vai trò con số (mức tối đa công bố/giá trị luôn đạt) hoặc khác sản phẩm. Ví dụ: trang AirPods Max 2 chỉ công bố “lên đến 20 giờ … khi bật Chủ Động Khử Tiếng Ồn”; claim “20 giờ khi tắt chống ồn” trùng số nhưng không được nguồn hỗ trợ.')]]
B1 += [[para('plain', '**Đóng góp cốt lõi — phương pháp kiểm chứng nhận biết phạm vi thông số (SAV, Scope-Aware Verification)**, gồm hai thành phần trên cùng biểu diễn σ = ⟨sản phẩm, phiên bản, bộ phận, thuộc tính, điều kiện thử, vai trò con số, giá trị, đơn vị⟩: (1) **trích xuất σ có neo nguồn** — LLM phải kèm chuỗi nguyên văn cho giá trị, điều kiện và bộ phận; bộ kiểm tất định xác nhận chuỗi có trong đoạn, con số khớp và vai trò con số khớp từ chỉ vai trò, trường không neo được thì loại dữ kiện; (2) **bộ quyết định nhận biết phạm vi** — kiểm từng chiều σ với kết quả ba trạng thái, coi lệch phạm vi là bằng chứng không dùng được (dẫn tới NEI) thay vì bác bỏ, kế thừa điều kiện tiêu đề có kiểm soát, và chỉ so giá trị theo bảng vai trò × vai trò khi mọi chiều đã khớp.')]]
B1 += label_row('Mục tiêu:', None, [
    'M1. Đề xuất và đặc tả SAV: định nghĩa bộ phạm vi σ, quy tắc neo nguồn theo từng trường, quy tắc kiểm từng chiều, chính sách kế thừa điều kiện và bảng so sánh theo vai trò con số; cài đặt có kiểm thử đơn vị.',
    'M2. Xây dựng bước trích xuất σ có neo nguồn bằng LLM theo schema cố định và truy hồi bằng chứng BM25 lọc theo sản phẩm để SAV chạy trên văn bản nguồn thật.',
    'M3. Đánh giá SAV so với LLM có danh sách kiểm phạm vi (B2), LLM tự quyết định (B1) — cả hai nhận **cùng** hồ sơ σ đã neo — và LLM đọc văn bản thô (B0), với hai mô hình quyết định, trên tập claim quảng cáo LLM và tập chẩn đoán cặp tối thiểu theo từng chiều phạm vi; phân tích thành phần (gồm bỏ bước neo) và đánh giá trên hồ sơ chuẩn để tách lỗi trích xuất khỏi lỗi quyết định.',
    'M4. Chuẩn bị dữ liệu cần cho phép đo (sản phẩm hỗ trợ, không phải đóng góp): kho tài liệu chính thức có snapshot và mã băm cho 10 họ sản phẩm AirPods và Beats (tối thiểu 6), tập claim tiếng Việt có nguồn gốc truy vết, hướng dẫn gán nhãn dùng chung cho người gán, B0, B1 và SAV.',
])
B1 += [[para('plain', '**Phạm vi:** claim về thời lượng pin, thời gian sạc, phiên bản Bluetooth, chống nước/bụi, chống ồn và các thông số có số liệu trên tài liệu chính thức của hãng (AirPods của Apple và Beats; thêm hãng độc lập nếu thu được trang thông số văn bản). Đầu vào là claim đã tách thủ công và mã sản phẩm đang quảng cáo. Không thuộc phạm vi: tách claim tự động, tự nhận diện sản phẩm, kho gây nhiễu nhiều sản phẩm, mô hình thứ hai, giao diện web.')]]
B1 += [[para('plain', '**Giới hạn kết luận:** hệ thống kiểm mức độ được tài liệu chính thức hỗ trợ, không kiểm hiệu năng thực tế, không đưa kết luận pháp lý. NEI nghĩa là “chưa tìm thấy trong kho nguồn đã khóa”. Kết luận chỉ áp dụng cho các họ sản phẩm và kho nguồn đã chọn.')]]
B1 += [[para('plain', '**Đối tượng:** bài toán kiểm chứng phát biểu thông số sản phẩm dựa trên bằng chứng văn bản; biểu diễn phạm vi thông số; bộ quyết định tất định so với bộ quyết định bằng LLM.')]]

B1 += [[para('label', '**Phương pháp thực hiện:**'), para('h2', 'Cơ sở và điểm mới so với công trình liên quan'),
        para('b5', 'Khảo sát kiểm chứng quảng cáo [1], kiểm chứng chi tiết theo claim [2], kiểm chứng claim số [3], [13], [16], xung đột bằng chứng [5], kiểm chứng có cấu trúc/neuro-symbolic [14], [15], bằng chứng đối lập [12] và các bộ dữ liệu [7]–[11].')]]
B1 += [[para('b7', b)] for b in [
    '[1] đã dùng LLM trích xuất kết hợp quy tắc, nhưng so khớp ngữ nghĩa theo ngưỡng, gán nhãn cả bài, không có chiều điều kiện hay vai trò con số. CoVer [5] tổng hợp bằng quy tắc ở mức lập trường, không ở mức thông số.',
    '[3], QuanTemp [16] và Aarnes & Setty [13] xử lý claim số bằng mô hình học hoặc phân loại kiểu claim; con số không gắn bộ phận, điều kiện thử và vai trò công bố/quan sát.',
    'ProgramFC [14] và FOLK [15] phân rã claim thành chương trình/vị từ, nhưng từng bước vẫn do LLM trả lời tự do, không neo vào nguồn và không có schema phạm vi cố định.',
    '**Điểm mới của SAV:** vai trò con số và điều kiện thử là chiều phạm vi bắt buộc; hồ sơ do LLM trích được neo vào văn bản nguồn theo từng chiều trước khi quyết định; lệch phạm vi không bị suy thành bác bỏ; so sánh theo bảng vai trò × vai trò. Trong các tài liệu đã khảo sát chưa thấy cách làm này cho thông số sản phẩm; nhận định sẽ được kiểm lại khi đọc toàn văn các bài [12]–[16] ở giai đoạn 1.',
    '**Không phải đóng góp:** dùng BM25, gọi API LLM, xuất JSON, kết hợp LLM với Python, đổi miền sang tai nghe, kho dữ liệu và hướng dẫn nhãn.',
]]
B1 += [[para('h2', 'Câu hỏi nghiên cứu')]]
B1 += [[para('b7', b)] for b in [
    '**RQ1 (hỗ trợ):** BM25 lọc theo sản phẩm có đưa đủ bằng chứng cho SAV không? Đo evidence-set recall@k kèm số đoạn ứng viên N và k_eff = min(k, N) (TN1).',
    '**RQ2 (chính):** trên cùng hồ sơ σ đã neo, SAV có giảm tỷ lệ chấp nhận nhầm (FAR) so với LLM có danh sách kiểm phạm vi (B2) và LLM tự do (B1), đặc biệt trên claim lệch phạm vi, mà vẫn giữ Recall Supported, với cả hai mô hình quyết định? (TN2).',
    '**RQ3 (cơ chế):** thành phần nào tạo ra khác biệt — từng chiều của bộ quyết định và bước neo nguồn — và còn bao nhiêu khi bỏ hẳn lỗi trích xuất? (TN3 — tắt từng thành phần; TN4 — hồ sơ chuẩn).',
]]
B1 += section('Dữ liệu và nhãn chuẩn',
              'Thu tài liệu thông số chính thức (snapshot, URL, ngày truy cập, SHA-256), chia đoạn có mã; sinh quảng cáo bằng LLM có lưu prompt, tham số, đầu ra thô; tách claim thủ công.', [
    'Hai tập báo riêng: claim từ quảng cáo LLM thông thường, và tập chẩn đoán gồm biến thể cặp tối thiểu của câu cha (đổi điều kiện, bộ phận, vai trò con số, giá trị, sản phẩm) để đo SAV theo từng chiều phạm vi.',
    'Quy mô dự kiến, chốt sau pilot: dev 3 họ (30–40 claim thông thường, 20–30 biến thể); val 2 họ (12–15; 10–15); test 5 họ, ít nhất 2 họ Beats (40–60; 60–75, ≥ 12 mỗi loại thao tác). Tổng ≈ 170–235 claim, hơn một nửa là biến thể dùng lại bằng chứng của câu cha. Sàn test: R+NEI ≥ 40, S ≥ 20, ≥ 8 ca mỗi loại COND/PART/ROLE.',
    'Nhãn theo hướng dẫn dùng chung có phiên bản và mã băm: chỉ dùng tài liệu trong kho; claim và nguồn phải khớp sản phẩm, phiên bản, bộ phận, thuộc tính, đơn vị, điều kiện; mọi NEI-missing có nhật ký tìm nguồn. Claim nhiều thuộc tính: có bác bỏ → Refuted; có xung đột → NEI; mọi thuộc tính được hỗ trợ → Supported.',
    'Chia tập theo họ sản phẩm. Người gán thứ hai độc lập cho 40 claim, báo Cohen’s κ trước hòa giải; nếu không có người thứ hai, báo tự nhất quán và ghi rõ giới hạn.',
])
B1 += section('Quy trình xử lý',
              'Claim + mã sản phẩm → BM25 lấy top-k đoạn của đúng sản phẩm → LLM trích hồ sơ σ kèm chuỗi nguyên văn → kiểm neo nguồn (loại dữ kiện không neo được) → chuẩn hóa đơn vị → bộ quyết định → nhãn, mã bằng chứng, dữ kiện bị loại, dấu vết từng chiều.', [
    'A — phạm vi: sản phẩm, phiên bản, bộ phận, thuộc tính, đơn vị quy đổi được. B — điều kiện thử, có kế thừa điều kiện tiêu đề trừ claim nghĩa đen (“luôn”, “mọi chế độ”). Lệch ở A/B → đoạn không dùng được.',
    'C1 — xung đột chỉ xét trong cùng σ → NEI-conflict. C2 — so sánh theo vai trò × vai trò, dung sai mặc định 0 (ví dụ claim “luôn 20 giờ” gặp nguồn “lên đến 20 giờ” → chưa đủ; claim “lên đến 25 giờ” gặp “lên đến 20 giờ” → bác bỏ). C3 — tổng hợp nhãn.',
    'Lỗi JSON, hồ sơ thiếu, lỗi gọi mô hình được ghi là ERROR, không đổi thành NEI. Hồ sơ không chứa nhãn chuẩn hay thông tin lộ nhãn (có kiểm tự động).',
    'Đối chứng: B1 nhận đúng hồ sơ σ đã neo của SAV và cùng hướng dẫn nhãn rồi để LLM quyết định; B2 như B1 nhưng có thêm danh sách kiểm phạm vi (sản phẩm → bộ phận → điều kiện → vai trò con số → giá trị) và 3 ví dụ từ dev — đối chứng mạnh nhất bằng prompt, nên so sánh chính là SAV − B2; B0 đọc văn bản thô, chỉ để tham khảo. Phần quyết định của B0/B1/B2 chạy trên hai mô hình: một mô hình mở (họ Llama) và một mô hình thương mại cỡ nhỏ.',
])
B1 += section('Thiết kế thực nghiệm và tiêu chí đánh giá',
              'Mô hình, prompt, k, hướng dẫn nhãn, tập chia và mã nguồn được khóa bằng mã băm trước khi chạy test; val chạy một lần sau khóa.', [
    'TN1: recall@k của BM25 trên test. TN2: B0, B1, B2, SAV × hai mô hình quyết định trên toàn test; lượt 1 là bảng chính, lượt 2–3 trên min(30, n_test) claim chọn trước. TN3: SAV tắt lần lượt kiểm bộ phận, điều kiện, vai trò con số, kế thừa điều kiện và bước neo nguồn (P−ground), trên cùng lượt trích xuất 1. TN4: SAV, B1, B2 trên hồ sơ chuẩn viết tay cho tập chẩn đoán test.',
    'Chỉ số: FAR = (Refuted→Supported + NEI→Supported) / (số claim Refuted + NEI); Recall Supported; FAR theo loại thao tác; precision/recall/F1 từng nhãn, Macro-F1; ΔFAR, ΔRecall; số lượt gọi, token, thời gian, chi phí.',
    '**Điều kiện kết luận SAV có tác dụng trên mẫu (chốt trước test):** trên tập chẩn đoán test, ΔFAR = FAR_SAV − FAR_B2 < 0 ở lượt 1 với cả hai mô hình, cùng chiều ở các lượt lặp, cặp bất đồng nghiêng về SAV (McNemar ghép cặp), ΔRecall Supported ≥ −10 điểm phần trăm, và ablation tương ứng làm FAR tăng ở đúng loại thao tác. Thiếu một điều kiện → “chưa kết luận”. Bước neo nguồn có tác dụng khi P−ground có FAR cao hơn SAV trên hồ sơ trích và khoảng cách gần như mất trên hồ sơ chuẩn.',
    'Khi kết quả âm, TN4 phân biệt: trích xuất làm mất thông tin phạm vi, luật sai/thiếu, hoặc B2 đã đủ tốt. Mọi trường hợp đều được báo cáo.',
    'Bất định mô tả bằng bootstrap theo họ sản phẩm, kết quả từng họ và bỏ lần lượt từng họ; không tuyên bố ý nghĩa thống kê khi số họ ít.',
])
B1 += [[para('label', '**Kết quả mong đợi:**')]]
B1 += [[para('b3', b)] for b in [
    'Đặc tả và mã nguồn SAV (kiểm neo nguồn và bộ quyết định) có kiểm thử; bước trích xuất σ và truy hồi BM25 chạy trên tài liệu thật.',
    'Bảng TN1–TN4 trên test đã khóa, mọi số truy được về file kết quả; kết luận về RQ2–RQ3 theo đúng điều kiện chốt trước, kể cả khi không cải thiện.',
    'Kho nguồn, tập claim có nhãn và nguồn gốc truy vết, hướng dẫn gán nhãn có phiên bản; phân tích lỗi trên mẫu chọn trước.',
    'Luận văn, slide và gói tái lập (chương trình dòng lệnh trả nhãn, bằng chứng, lý do, dấu vết cho từng claim).',
]]

B2 = []
B2 += [[para('label', '**Kế hoạch thực hiện:** một sinh viên thực hiện; các giai đoạn nối tiếp, giai đoạn sau chỉ bắt đầu khi giai đoạn trước đạt mốc kiểm tra. Ước lượng ≈ 208–320 giờ (≈ 17–27 giờ/tuần). Danh sách 52 bước chi tiết ở sổ tay thực hiện kèm theo.')]]
GATES = [
    ('GĐ1 (09/10–18/10) — Khởi động và chốt tính mới', ['Đọc toàn văn các bài gần nhất, lập bảng đối chiếu, xác nhận điểm mới của SAV; chốt định nghĩa σ và câu hỏi nghiên cứu với GVHD.']),
    ('GĐ2 (19/10–22/10) — Môi trường', ['Cài môi trường, chọn mô hình LLM, chạy thử trên ví dụ có sẵn.']),
    ('GĐ3 (23/10–01/11) — Nguồn cho 2 họ pilot', ['Kiểm kê 10 họ AirPods và Beats; thu tài liệu chính thức, snapshot, trích văn bản, chia đoạn, kiểm độ phủ cho 2 họ pilot.']),
    ('GĐ4 (02/11–09/11) — Dữ liệu pilot', ['Sinh quảng cáo, tách claim, tạo biến thể cặp tối thiểu, gán nhãn và đo thời gian gán.']),
    ('GĐ5 (10/11–23/11) — Pipeline trên dev và pilot', ['Cài BM25, trích xuất σ có neo nguồn, bộ quyết định, B0/B1/B2, kiểm rò nhãn, runner; chạy pilot; chốt quy mô.']),
    ('GĐ6 (24/11–07/12) — Dữ liệu đủ quy mô', ['Mở rộng nguồn, claim, biến thể, nhãn cho mọi họ; kiểm độ tin cậy nhãn.']),
    ('GĐ7 (08/12–11/12) — Chia tập và khóa', ['Chia theo họ, viết hồ sơ chuẩn cho TN4, kiểm dữ liệu, khóa giao thức.']),
    ('GĐ8 (12/12–17/12) — Thực nghiệm và phân tích', ['Chạy TN1–TN4, tính chỉ số, phân tích lỗi, case study.']),
    ('GĐ9 (18/12–27/12) — Hoàn thiện luận văn', ['Hoàn thiện 5 chương (bản nháp Chương 1–3 viết dần từ GĐ1 và GĐ5).']),
    ('GĐ10 (28/12–31/12) — Bàn giao', ['Gói tái lập, slide, chuẩn bị bảo vệ.']),
]
for g, items in GATES:
    B2 += [[para('gate', g, bold=True)]] + [[para('item', it)] for it in items]
B2 += section('Rủi ro và phương án', None, [
    'Hãng thứ hai là Beats (trang chính thức riêng) nên nguồn chắc chắn có; giới hạn “hai thương hiệu cùng tập đoàn” được ghi rõ. Nếu tổng số họ < 6: giữ RQ2–RQ3 và tập chẩn đoán, hạ mức kết luận.',
    'Gán nhãn chậm hơn dự kiến: giảm claim thông thường ở test, giữ tập chẩn đoán và TN2–TN4.',
    'Trích xuất lỗi nhiều: kiểm neo loại dữ kiện bịa; nếu tỷ lệ loại > 20% trên dev thì sửa prompt/schema trước khi khóa (không nới kiểm neo); TN4 tách phần ảnh hưởng còn lại.',
    'Lịch chính thức của Khoa khác dự kiến: dời các giai đoạn theo thông báo, giữ nguyên thứ tự.',
])
B2 += [[para('b7', '**Cần GVHD xác nhận:** trọng tâm SAV và RQ1–RQ3; chính sách kế thừa điều kiện; quy mô chốt sau pilot; lịch so với hạn chính thức; ngân sách API.')]]

REFS = [
    '[1] T. T. Nguyen, H. Nguyen Thi Phuong, T. P. Le, and B. T. Nguyen, “Fact-checking for online advertisement posts,” in *Proc. PACLIC 38*, 2024, pp. 398–406. https://aclanthology.org/2024.paclic-1.40/',
    '[2] K. Mitra, D. Zhang, S. Rahman, and E. Hruschka, “FactLens: Benchmarking fine-grained fact verification,” in *Findings of ACL 2025*, 2025, pp. 18085–18096. https://doi.org/10.18653/v1/2025.findings-acl.929',
    '[3] P. Chungkham, V. V, V. Setty, and A. Anand, “Think right, not more: Test-time scaling for numerical claim verification,” in *Findings of EMNLP 2025*, 2025, pp. 24345–24363. https://doi.org/10.18653/v1/2025.findings-emnlp.1322',
    '[4] J. Sun, G. Warren, I. Shklovski, and I. Augenstein, “Explaining sources of uncertainty in automated fact-checking,” in *Proc. ACL 2026 (Long Papers)*, 2026, pp. 45510–45534. https://doi.org/10.18653/v1/2026.acl-long.2110',
    '[5] S. Zhang et al., “CoVer: Conflict-aware claim verification,” arXiv:2609.00508, 2026. https://arxiv.org/abs/2609.00508',
    '[6] F. B. Rashid and S. Hakak, “Fathom: A fast and modular RAG pipeline for fact-checking,” in *Proc. FEVER Workshop*, 2025, pp. 258–265. https://doi.org/10.18653/v1/2025.fever-1.20',
    '[7] J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, “FEVER: a large-scale dataset for Fact Extraction and VERification,” in *Proc. NAACL-HLT*, 2018, pp. 809–819. https://aclanthology.org/N18-1074/',
    '[8] M. Schlichtkrull, Z. Guo, and A. Vlachos, “AVeriTeC: A dataset for real-world claim verification with evidence from the web,” in *NeurIPS Datasets and Benchmarks*, 2023. https://arxiv.org/abs/2305.13117',
    '[9] T. T. Hoa et al., “ViFactCheck: A new benchmark dataset and methods for multi-domain news fact-checking in Vietnamese,” arXiv:2412.15308, 2024. https://arxiv.org/abs/2412.15308',
    '[10] H. T. Le et al., “ViWikiFC: Fact-checking for Vietnamese Wikipedia-based textual knowledge source,” arXiv:2405.07615, 2026. https://arxiv.org/abs/2405.07615v2',
    '[11] N. N.-P. Luong et al., “ViNumFCR: A novel Vietnamese benchmark for numerical reasoning fact checking on social media news,” in *Proc. INLG*, 2025, pp. 134–147. https://aclanthology.org/2025.inlg-main.9/',
    '[12] T. Schuster, A. Fisch, and R. Barzilay, “Get your vitamin C! Robust fact verification with contrastive evidence,” in *Proc. NAACL-HLT*, 2021, pp. 624–643. https://aclanthology.org/2021.naacl-main.52/',
    '[13] Aarnes and V. Setty, arXiv:2610.00689, 2026 (AACL-IJCNLP 2026 Findings). https://arxiv.org/abs/2610.00689',
    '[14] L. Pan, X. Wu, X. Lu, A. T. Luu, W. Y. Wang, M.-Y. Kan, and P. Nakov, “Fact-checking complex claims with program-guided reasoning,” in *Proc. ACL 2023*, 2023. https://aclanthology.org/2023.acl-long.386/',
    '[15] H. Wang and K. Shu, “Explainable claim verification via knowledge-grounded reasoning with large language models,” in *Findings of EMNLP 2023*, 2023. https://aclanthology.org/2023.findings-emnlp.416/',
    '[16] V. Venktesh, A. Anand, A. Anand, and V. Setty, “QuanTemp: A real-world open-domain benchmark for fact-checking numerical claims,” in *Proc. SIGIR 2024*, 2024. https://arxiv.org/abs/2403.17169',
]
B2 += [[para('label', '**Tài liệu tham khảo**')] + [para('ref', REFS[0])]]
B2 += [[para('ref', r)] for r in REFS[1:]]

# ---------- ráp vào document.xml ----------
body_start = doc.index('<w:body>') + len('<w:body>')
tbls = [m.span() for m in re.finditer(r'<w:tbl>.*?</w:tbl>', doc, flags=re.S)]
assert len(tbls) == 2, tbls
big_s, big_e = tbls[1]
big = doc[big_s:big_e]
rows = re.findall(r'<w:tr[ >].*?</w:tr>', big, flags=re.S)
assert len(rows) == 98, len(rows)
head = big[:big.index('<w:tr')]
# bỏ màu đỏ “phần thiết kế lại” ở hàng tên đề tài; giữ nguyên chữ
title_row = re.sub(r'<w:color w:val="[cC]00000"/>', '', rows[0])
_tt = ''.join(re.findall(r'<w:t[^>]*>([^<]*)', title_row))
assert TITLE_VI in _tt and TITLE_EN in _tt, _tt
info_rows = title_row + ''.join(rows[1:4])
sign = rows[97].replace('ngày 15 tháng 09 năm 2026', 'ngày ….. tháng 10 năm 2026')
new_big = head + info_rows + block(B1) + block(B2) + sign + '</w:tbl>'

pre = doc[:big_s]
off = tbls[0][1]
paras = list(re.finditer(r'<w:p[ >](?:(?!<w:p[ >]).)*?</w:p>', pre[off:], flags=re.S))
note_m = paras[-1]
assert 'Bản đề xuất điều chỉnh' in note_m.group(0)
pre = pre[:off + note_m.start()] + pre[off + note_m.end():]  # bỏ ghi chú nội bộ đầu trang
new_doc = pre + new_big + doc[big_e:]
new_doc = re.sub(r'<w:color w:val="[cC]00000"/>', '', new_doc)
new_rels = rels.replace('</Relationships>', ''.join(_new_rels) + '</Relationships>')

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == 'word/document.xml':
            data = new_doc.encode('utf-8')
        elif item.filename == 'word/_rels/document.xml.rels':
            data = new_rels.encode('utf-8')
        zout.writestr(item, data)
print('wrote', OUT, 'links', len(_new_rels))
