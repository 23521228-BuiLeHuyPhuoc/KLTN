#!/usr/bin/env python3
"""ĐÃ THAY THẾ ngày 08/10/2026 bởi redesign_plan_2026_10_08.py; script này không còn áp dụng
cho docx hiện tại và chỉ giữ lại để truy vết lịch sử.

Vá tại chỗ hai docx theo rà soát 08/10/2026 (nhánh review/opus-2026-10-08).

Lý do: update_thesis_docs.py --apply không tái lập được vì bản gốc nằm trong
scratch_test/ (bị .gitignore, không có trong repo), nên docx đã commit không
đạt các khẳng định mới của --check. Script này chỉ THÊM đoạn chữ đỏ (C00000)
hoặc thay văn bản trong ô/đoạn có sẵn; không thêm/xóa hàng bảng, không đổi
header/footer, hình, sectPr và hàng chữ ký đề cương.

Mặc định: xem trước + kiểm tra. --apply: ghi đè hai docx (đã có bản gốc trong Git).
"""
import argparse
import io
import sys
from pathlib import Path
from xml.dom import minidom
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_thesis_docs import (ROOT, REPORT, PROPOSAL, body, cell_at, children,  # noqa: E402
                                paragraph, set_cell, structure, text, validate_content)

MARK = 'Đề xuất điều chỉnh 08/10/2026'
DRAFT = '(DỰ THẢO — cần sinh viên/GVHD xác nhận)'


def append_red(cell, value):
    template = children(cell, 'w:p')[-1]
    cell.appendChild(paragraph(template, value, red=True, new=True))


def replace_para(p, value, red=True):
    p.parentNode.replaceChild(paragraph(p, value, red=red), p)


PROPOSAL_APPEND = {
    20: f'{MARK}: lưu quảng cáo thô (nguyên văn đầu ra LLM, SHA-256, prompt đã render, nhà cung cấp, mã mô hình trả về, tham số sinh) theo templates/llm_ad_sample.json; thu theo lô với tiêu chí dừng chốt trước, chỉ đọc số đếm nhãn; nhóm sinh thông thường tối thiểu 50% mỗi tập {DRAFT}.',
    24: f'{MARK}: bổ sung người thứ hai gán độc lập 30 claim chọn trước theo nhãn sơ bộ/nguồn gốc/họ, không thấy nhãn đầu hay dự đoán; báo đồng thuận và Cohen’s kappa (mức đồng thuận hai người sau khi trừ phần trùng do ngẫu nhiên) trước hòa giải. Người gán thứ hai: [SINH VIÊN ĐIỀN: họ tên/mã, ngày nhận việc]. Tự gán lại 20% vẫn giữ nhưng không thay thế bước này {DRAFT}.',
    29: f'{MARK}: báo số đoạn N của sản phẩm và k_eff = min(k, N) cho từng claim; tách recall@k của nhóm N > k vì nhóm N ≤ k lấy hết đoạn nên recall không phản ánh chất lượng xếp hạng {DRAFT}.',
    32: f'{MARK}: claim không nêu điều kiện thử thì kế thừa điều kiện thử của chính thông số nguồn; điều kiện claim nêu rõ vẫn phải khớp; claim “luôn/mọi chế độ” không kế thừa. Lý do: đọc nghĩa đen làm 11/23 câu ví dụ gốc đổi nhãn sang NEI (tests/test_abc.py) {DRAFT}.',
    38: f'{MARK}: mỗi cấu hình B0/B1/P chạy 3 lượt trên cùng phần mẫu; ghi run_manifest (nhà cung cấp, mã mô hình yêu cầu/trả về, tham số giải mã, mã băm prompt và hướng dẫn nhãn). Đầu vào B0/B1 qua scripts/check_input_leak.py để chặn rò nhãn {DRAFT}.',
    45: f'{MARK}: mô phỏng scripts/simulate_power.py (giả định FAR 0,30 so với 0,15) cho thấy với 4 họ test và 20 claim R+NEI, khoảng tin cậy cluster bootstrap của ΔFAR rộng khoảng 0,32 và chỉ khoảng 35% lần loại được 0; vì vậy RQ3 giữ mức thăm dò. Đây là mô phỏng, không phải kết quả {DRAFT}.',
    47: f'{MARK}: mọi nhãn NEI-thiếu kèm search_log (nguồn/truy vấn đã tìm, thời điểm, kết quả) theo templates/nei_search_log.json {DRAFT}.',
    64: f'{MARK}: đến 15/10 hoàn thành khóa schema/hướng dẫn nhãn, lô 0 (2 họ × 5 quảng cáo LLM) và đo thời gian gán nhãn trên 5 mẫu đầu; pilot 45 claim / 6 họ dời về 31/10 nếu năng suất đo được không cho phép. Chi tiết: docs/KE_HOACH_THUC_TE_2026-10-08.md {DRAFT}.',
    67: f'{MARK}: đầu ra Gate 2 đến 31/10 gồm pilot 45–60 claim / 6 họ, B0 và P chạy tối thiểu trên pilot, số đo năng suất gán nhãn và quyết định quy mô 120/12 hay 180 {DRAFT}.',
}

REPORT_AI_NOTE = ('Ghi nhận hỗ trợ AI — cập nhật 08/10/2026: các số liệu trong mục 3.1 được công cụ AI đối chiếu lại với PDF trong báo/ (khớp với bảng của tác giả). '
                  'Đây không phải xác nhận sinh viên đã tự kiểm. Sinh viên tự kiểm tối thiểu Bảng 1 của [2], Bảng 1 của [3], Bảng 2 của [5]: [SINH VIÊN ĐIỀN: ngày, trang, kết quả]. '
                  'Cách khai báo AI theo quy định khoa/GVHD: [SINH VIÊN ĐIỀN].')

REPORT_PROTOCOL = (f'{MARK} {DRAFT}: (1) người thứ hai gán độc lập 30 claim, chưa có người nhận việc; (2) NEI-thiếu kèm search_log; '
                   '(3) báo N đoạn và k_eff = min(k, N), tách recall nhóm N > k; (4) mỗi cấu hình chạy 3 lượt, ghi nhà cung cấp/mô hình/tham số; '
                   '(5) lưu quảng cáo thô của LLM kèm prompt và mã băm, nhóm sinh thông thường tối thiểu 50%; (6) tập test 4 họ chỉ đủ cho kết luận thăm dò (scripts/simulate_power.py). '
                   'Chi tiết: docs/GIAO_THUC_DANH_GIA.md §10–11 và docs/KE_HOACH_THUC_TE_2026-10-08.md.')

REPORT_GATE = (f'{MARK} {DRAFT}: đến 15/10 chỉ cam kết khóa schema/hướng dẫn nhãn, lô 0 gồm 2 họ × 5 quảng cáo LLM thông thường và đo phút gán nhãn/claim trên 5 mẫu đầu; '
               'pilot 45–60 claim / 6 họ và B0/P tối thiểu dời về 31/10. Lý do: đến 08/10 hồ sơ chưa có quảng cáo LLM nào có log, chưa có cấu hình máy/API.')


def patch_proposal(doc):
    b = body(doc)
    t = children(b, 'w:tbl')[1]
    assert len(children(t, 'w:tr')) == 98
    for row, value in PROPOSAL_APPEND.items():
        append_red(cell_at(t, row), value)
    for p in children(b, 'w:p'):
        if text(p).startswith('Bản rà soát ngày 08/10/2026'):
            replace_para(p, 'Bản đề xuất điều chỉnh ngày 08/10/2026, chờ GVHD xác nhận: chữ đỏ là phần thêm hoặc sửa; các mốc và quy mô là kế hoạch dự kiến, chưa được phê duyệt.')
            break
    else:
        raise ValueError('thiếu dòng đánh dấu bản rà soát')


def patch_report(doc):
    b = body(doc)
    ts = children(b, 'w:tbl')
    ps = children(b, 'w:p')
    find = lambda prefix: next(p for p in ps if text(p).startswith(prefix))
    tmpl = find('Đề tài kiểm chứng từng claim')
    # Giọng sinh viên "Đã đối chiếu" → ghi đúng là AI hỗ trợ, chờ xác nhận.
    for t in ts[2:8]:
        cell = cell_at(t, 3, 1)
        v = text(cell)
        if v.startswith('Đã đối chiếu '):
            set_cell(cell, 'Đối chiếu có hỗ trợ AI; chờ sinh viên xác nhận: ' + v.removeprefix('Đã đối chiếu '), red=True)
    b.insertBefore(paragraph(tmpl, REPORT_AI_NOTE, red=True, new=True), find('[1] Fact checking'))
    ex = find('Bộ minh họa hiện có 23 ví dụ')
    replace_para(ex, text(ex).replace('do Codex soạn', 'do công cụ AI (Codex) soạn'), red=False)
    b.insertBefore(paragraph(tmpl, REPORT_PROTOCOL, red=True, new=True), find('3.3.'))
    p = find('Cần xác nhận tài nguyên thực tế')
    replace_para(p, 'Tài nguyên thực tế: CPU [SINH VIÊN ĐIỀN]; RAM [SINH VIÊN ĐIỀN]; GPU/VRAM hoặc nhà cung cấp API, mô hình và ngân sách [SINH VIÊN ĐIỀN]; hệ điều hành và môi trường chạy [SINH VIÊN ĐIỀN]. Không suy ra cấu hình thí nghiệm từ máy dùng để sửa tài liệu.')
    p = find('Khó khăn thực tế cần xác nhận')
    replace_para(p, 'Khó khăn thực tế: đầu việc bị vướng [SINH VIÊN ĐIỀN]; thời điểm và nguyên nhân [SINH VIÊN ĐIỀN]; ảnh hưởng tới tiến độ [SINH VIÊN ĐIỀN]; biện pháp đã thử và nội dung cần giảng viên hỗ trợ [SINH VIÊN ĐIỀN]. Rủi ro dự kiến trong đề cương không được viết thành sự cố đã xảy ra.')
    status = ts[31]
    append_red(cell_at(status, 1, 1), 'Cập nhật 08/10: số liệu sáu bài đã được AI đối chiếu lại với PDF, khớp bảng tác giả; ngày sinh viên tự kiểm: [SINH VIÊN ĐIỀN].')
    append_red(cell_at(status, 3, 1), 'Cập nhật 08/10: tests/test_abc.py kiểm 23 ví dụ bằng hàm tham chiếu A–B–C; nhãn chỉ khớp với câu đã biên tập, câu gốc lệch 11/23 nếu đọc luật B nghĩa đen (đề xuất luật kế thừa điều kiện, chờ xác nhận).')
    append_red(cell_at(status, 4, 1), 'Cấu hình máy/API, mô hình ứng viên, log thử: [SINH VIÊN ĐIỀN].')
    b.insertBefore(paragraph(tmpl, REPORT_GATE, red=True, new=True), find('Gate 2 (16–31/10)'))
    for prefix in ('Hồ sơ sử dụng để lập báo cáo', 'Các thông tin cần chốt trước khi nộp'):
        p = find(prefix)
        replace_para(p, '[GHI CHÚ NỘI BỘ — SINH VIÊN XÓA TRƯỚC KHI NỘP] ' + text(p))


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
        assert 'chờ GVHD xác nhận' in text(d1)
    validate_content(name, d1)
    return [len(t) for t in structure(d1)]


def build(path, fn):
    src = path.read_bytes()
    with ZipFile(io.BytesIO(src)) as z:
        doc = minidom.parseString(z.read('word/document.xml'))
        if MARK in text(doc):
            raise SystemExit(f'{path.name}: đã vá trước đó, dừng để tránh vá hai lần')
        fn(doc)
        out = io.BytesIO()
        with ZipFile(out, 'w') as t:
            for e in z.infolist():
                t.writestr(e, doc.toxml(encoding='UTF-8') if e.filename == 'word/document.xml' else z.read(e.filename))
    return src, out.getvalue()


def main():
    if 'chờ GVHD xác nhận' in text(minidom.parseString(ZipFile(ROOT / PROPOSAL).read('word/document.xml'))):
        raise SystemExit('Đã thay bằng scripts/redesign_plan_2026_10_08.py; không chạy trên docx hiện tại.')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    results = []
    for name, fn in ((PROPOSAL, patch_proposal), (REPORT, patch_report)):
        src, new = build(ROOT / name, fn)
        rows = check(name, src, new)
        print(f'PASS: {name} — bảng/hàng {rows}, {len(src):,} → {len(new):,} byte')
        results.append((ROOT / name, new))
    if args.apply:
        for path, data in results:
            path.write_bytes(data)
        print('Đã ghi hai docx.')
    else:
        print('Xem trước. Dùng --apply để ghi.')


if __name__ == '__main__':
    main()
