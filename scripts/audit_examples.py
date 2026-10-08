#!/usr/bin/env python3
"""Build a traceable example audit from the original DOCX and saved Apple pages.

This produces documentation fixtures, NOT a verified LLM-generated dataset.
Quotation text is copied from saved page.txt, never reconstructed from prose.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
from xml.dom import minidom
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'evidence/2026-10-08'
ORIGINAL = ROOT / 'scratch_test/docx-review-2026-10-08/originals/Đọc_báo_cùng_HuP_3_.docx'

# Search strings locate the excerpt; returned text retains original whitespace.
SPECS = {
    1: ('apple-airpods5-vn', ['Trọng Lượng (AirPods 5): 32,3 gram'], 'dimensions-section.png', 'Kích Thước Và Trọng Lượng → ul.data-containers.case, dưới hình hộp sạc 50,1 × 46,2 × 21,2 mm; không phải khối tai nghe'),
    2: ('apple-airpods5-vn', ['Trọng Lượng (AirPods 5): 32,3 gram'], 'dimensions-section.png', 'Khối hộp sạc: ul.data-containers.case; cùng tiêu đề chung “Mỗi Bên” nhưng nằm dưới hình hộp'),
    3: ('apple-airpods5-vn', ['Trọng Lượng: 4,3 gram'], 'dimensions-section.png', 'Khối tai nghe: ul.data-containers không có class case, dưới hình tai nghe 30,2 × 18,3 × 18,1 mm'),
    4: ('apple-airpods5-vn', ['Thời lượng pin lên đến 4 giờ với một lần sạc khi bật tính năng Chủ Động Khử Tiếng Ồn', 'Thời lượng pin lên đến 6 giờ với một lần sạc khi tắt kiểm soát tiếng ồn'], 'battery-section.png', 'Pin → AirPods 5 bản Hộp Sạc USB-C; chú thích 10'),
    5: ('apple-pro3-vn', ['Công nghệ không dây Bluetooth 5.3'], 'connectivity-section.png', 'Kết Nối'),
    6: ('apple-pro3-vn', ['Thời gian nghe lên đến 8 giờ với một lần sạc khi bật tính năng Chủ Động Khử Tiếng Ồn (lên đến 7,5 giờ khi bật Âm Thanh Không Gian và Theo Dõi Chuyển Động Đầu)'], 'battery-section.png', 'Pin → AirPods Pro 3; giữ cả ngoặc giới hạn 7,5 giờ; chú thích 13'),
    7: ('apple-pro3-vn', ['5 phút để trong hộp sạc có thể tăng thời gian nghe khoảng 1 giờ'], 'battery-section.png', 'Pin → AirPods Pro 3 với Hộp Sạc MagSafe (USB-C); chú thích 18; toàn trang lưu không nêu thời gian sạc đầy'),
    8: ('apple-pro3-vn', ['Công nghệ không dây Bluetooth 5.3'], 'connectivity-section.png', 'Kết Nối'),
    9: ('apple-max2-vn', ['Thời gian nghe lên đến 20 giờ với một lần sạc khi bật tính năng Chủ Động Khử Tiếng Ồn'], 'battery-section.png', 'Pin → AirPods Max 2 (sạc đầy); chú thích 10'),
    10: ('apple-max2-vn', ['Thời gian nghe lên đến 20 giờ với một lần sạc khi bật tính năng Chủ Động Khử Tiếng Ồn'], 'battery-section.png', 'Pin → AirPods Max 2 (sạc đầy); chú thích 10 chỉ nói ANC bật, không phải ANC tắt'),
    11: ('apple-max2-vn', ['Thời gian nghe lên đến 20 giờ với một lần sạc khi bật tính năng Chủ Động Khử Tiếng Ồn'], 'battery-section.png', 'Pin → AirPods Max 2 (sạc đầy); chú thích 10'),
    12: ('apple-max2-vn', ['5 phút sạc đem đến thời gian nghe khoảng 1,5 giờ'], 'battery-section.png', 'Pin → AirPods Max 2 (sạc đầy); chú thích 11'),
    13: ('apple-airpods4-md', ['Up to 5 hours of listening time on a single charge'], 'battery-section.png', 'Battery → AirPods 4 tiêu chuẩn; chú thích 8; thị trường Moldova, không suy ra trang Việt Nam'),
    14: ('apple-airpods4-md', ['Weight (AirPods 4 with Active Noise Cancellation): 34.7 grams'], 'dimensions-section.png', 'Size and Weight → khối hộp sạc, bản ANC; thị trường Moldova'),
    15: ('apple-airpods4-md', ['Weight (AirPods 4): 32.3 grams', 'Weight (AirPods 4 with Active Noise Cancellation): 34.7 grams'], 'dimensions-section.png', 'Size and Weight → khối hộp sạc, hai phiên bản riêng; thị trường Moldova'),
    16: ('apple-airpods4-md', ['Up to 5 hours of listening time on a single charge', 'Volume was set to 50% and Spatial Audio was off.'], 'battery-section.png', 'Battery → AirPods 4; chú thích 8, không có phép thử âm lượng 100%'),
    17: ('apple-airpods2-vn', ['Thời gian nghe hơn 24 giờ'], 'battery.png', 'Pin → tiêu đề riêng: AirPods với Hộp Sạc Lightning hoặc Hộp sạc không dây; dòng nghe >24; chú thích 3'),
    18: ('apple-airpods2-vn', ['Thời gian nghe hơn 24 giờ'], 'battery.png', 'Pin → tiêu đề riêng: AirPods với Hộp Sạc Lightning hoặc Hộp sạc không dây; dòng nghe >24; chú thích 3'),
    19: ('apple-airpods2-vn', ['15 phút để trong hộp sạc cung cấp thời gian nghe lên đến 3 giờ'], 'battery.png', 'Pin → AirPods với hộp sạc; chú thích 4'),
    20: ('apple-airpods2-vn', ['15 phút để trong hộp sạc cung cấp thời gian nghe lên đến 3 giờ'], 'battery.png', 'Pin → AirPods với hộp sạc; chú thích 4'),
}

CONDITIONS = {
    4: ('10', 'Âm lượng 50%; Âm Thanh Không Gian và Nhận Biết Cuộc Hội Thoại tắt. Claim ANC bật phải đối chiếu mức 4 giờ, không lấy mức 6 giờ ANC tắt.'),
    6: ('13', 'Âm lượng 50%, ANC bật; không áp dụng mức 8 giờ cho chế độ bật Âm Thanh Không Gian và Theo Dõi Chuyển Động Đầu (nguồn ghi 7,5 giờ).'),
    7: ('18', 'Thông tin sạc nhanh: âm lượng 50%, ANC bật, tai nghe cạn pin được sạc 5 phút; không phải thời gian sạc đầy.'),
    9: ('10', 'Âm lượng 50%, ANC bật, Âm Thanh Không Gian cố định; phụ thuộc điều kiện thực tế.'),
    10: ('10', 'Nguồn thử âm lượng 50%, ANC bật, Âm Thanh Không Gian cố định. Claim ANC tắt: không có bằng chứng cùng chế độ trong trang đã lưu.'),
    11: ('10', 'Âm lượng 50%, ANC bật, Âm Thanh Không Gian cố định; so mức tối đa công bố 25 với 20, không phải hai khoảng bao hàm.'),
    12: ('11', 'Âm lượng 50%, ANC bật, Âm Thanh Không Gian cố định, tai nghe cạn pin được sạc 5 phút.'),
    13: ('8', 'Âm lượng 50%, Spatial Audio tắt, bản tiêu chuẩn; các điều kiện thử khác giữ theo chú thích 8.'),
    16: ('8', 'Nguồn thử âm lượng 50%, Spatial Audio tắt; claim 100% không được kế thừa kết quả ở 50%.'),
    17: ('3', 'Âm lượng 50%; lặp chu kỳ sạc đầy và phát nhạc đến khi cả tai nghe và hộp cạn pin; không phải một lần sạc tai nghe.'),
    18: ('3', 'Cùng phạm vi phép thử tổng tai nghe+hộp, âm lượng 50%; >24 loại trừ =24.'),
    19: ('4', 'Âm lượng 50%; tai nghe cạn pin được sạc 15 phút trong hộp; thời lượng phụ thuộc thực tế.'),
    20: ('4', 'Cùng phép thử sạc 15 phút, âm lượng 50%; mức tối đa 3 giờ không bảo đảm chính xác 3 giờ.'),
}

NEI_TERMS = {
    7: (['sạc đầy', '60 phút', '5 phút', 'fully charged', 'full charge'], 'Thời gian cần để sạc đầy tai nghe, không phải số giờ nghe sau sạc nhanh'),
    10: (['tắt', 'Khử Tiếng Ồn', '20 giờ', 'noise control off'], 'Thời lượng nghe khi ANC tắt, không phải phép thử ANC bật'),
    16: (['Volume', '50%', '100%', 'single charge', 'Spatial Audio'], 'Thời lượng pin ở âm lượng 100%, không phải phép thử 50%'),
    20: (['15 phút', '3 giờ', 'chính xác', 'phụ thuộc', '50 phần trăm'], 'Bảo đảm chính xác 3 giờ sau sạc 15 phút, không chỉ cận tối đa'),
}


def elements(node, tag):
    return [c for c in node.childNodes if c.nodeType == c.ELEMENT_NODE and c.nodeName == tag]


def cell_text(node):
    return '\n'.join(''.join(t.firstChild.data if t.firstChild else '' for t in p.getElementsByTagName('w:t')) for p in elements(node, 'w:p'))


def quote_segment(page, phrase):
    pattern = r'\s+'.join(re.escape(word) for word in phrase.split())
    match = re.search(pattern, page, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f'Excerpt absent from captured source: {phrase}')
    return {'text': match.group(), 'start_offset': match.start(), 'end_offset': match.end(),
            'start_line': page.count('\n', 0, match.start()) + 1}


def build():
    with ZipFile(ORIGINAL) as archive:
        doc = minidom.parseString(archive.read('word/document.xml'))
    tables = elements(doc.getElementsByTagName('w:body')[0], 'w:tbl')
    result = []
    for n in range(1, 21):
        cells = [cell_text(elements(row, 'w:tc')[1]) for row in elements(tables[n+7], 'w:tr')]
        sid, phrases, screenshot, locator = SPECS[n]
        source_dir = BASE / sid
        metadata = json.loads((source_dir / 'metadata.json').read_text())
        page = (source_dir / 'page.txt').read_text()
        excerpts = [quote_segment(page, phrase) for phrase in phrases]
        original = cells[4].strip().strip('“”')
        revised = original
        if n == 4:
            revised = revised.replace('AirPods 5', 'AirPods 5 bản đi kèm Hộp Sạc USB-C', 1)
        if n in CONDITIONS:
            revised = 'Theo thông số công bố của Apple, ' + revised[0].lower() + revised[1:] if not revised.startswith('AirPods') else 'Theo thông số công bố của Apple, ' + revised
            if n == 6:
                revised = revised.rstrip('.') + ', ở âm lượng 50% và không bật đồng thời Âm Thanh Không Gian với Theo Dõi Chuyển Động Đầu.'
            revised = revised.rstrip('.') + '; các điều kiện thử khác theo chú thích Apple được dẫn trong hồ sơ mẫu.'
        if 13 <= n <= 16:
            revised = revised.replace('Theo thông số công bố của Apple,', 'Theo thông số Apple tại Moldova,') if n in CONDITIONS else 'Theo thông số Apple tại Moldova, ' + revised[0].lower() + revised[1:]
        condition = CONDITIONS.get(n)
        cond_ref = f'{sid}#footnote-{condition[0]}' if condition else None
        reason = cells[10]
        if n == 6:
            reason = 'Nhãn Supported áp dụng cho câu đã làm rõ phạm vi công bố và điều kiện: mức 8 giờ ANC bật; không lấy mức này cho cấu hình nguồn ghi 7,5 giờ. Câu cũ thiếu phạm vi này nên chưa đủ để coi Supported vô điều kiện.'
        if n in (17, 18):
            reason += ' Tiêu đề xác định tai nghe+hộp được lưu ở vị trí nguồn, không ghép vào câu trích nguyên văn.'
        if n in (1, 2, 3):
            reason += ' Đối chiếu khối DOM và ảnh toàn mục: 4,3 g thuộc tai nghe, 32,3 g thuộc hộp; không suy bộ phận chỉ từ tiêu đề chung “Mỗi Bên”.'
        entry = {
            'id': f'EX-{n:02}', 'title': cells[1], 'group': cells[2],
            'original_ad': cells[3], 'original_claim': original, 'reviewed_claim': revised,
            'original_origin': 'unknown_legacy', 'origin_verified_as_llm': False,
            'original_generation': {'model': None, 'prompt': None, 'run_id': None, 'timestamp': None},
            'revision_origin': 'assistant_documentation_edit' if revised != original else 'unchanged_claim',
            'revision_editor': 'Codex', 'revision_date': '2026-10-08',
            'dataset_eligible': False, 'dataset_exclusion_reason': 'Chưa xác minh nguồn gốc câu gốc; không phải log sinh LLM thí nghiệm.',
            'legacy_source_date_unverified': '2026-10-07', 'source_checked_date': '2026-10-08',
            'scope': cells[5], 'source_id': sid, 'url': metadata['final_url'],
            'locator': locator, 'quotes': excerpts,
            'source_snapshot': f'evidence/2026-10-08/{sid}/page.txt',
            'screenshot': f'evidence/2026-10-08/{sid}/{screenshot}',
            'full_screenshot': f'evidence/2026-10-08/{sid}/full-page.png',
            'condition_ref': cond_ref, 'conditions_summary': condition[1] if condition else 'Không áp dụng điều kiện pin; giữ đúng sản phẩm/phiên bản/bộ phận/thị trường.',
            'values': cells[8], 'label': cells[9].split(';')[0].split('—')[0].split('–')[0].strip(),
            'nei_type': 'missing' if cells[9].startswith('NEI') else None,
            'label_scope': 'reviewed_claim_only', 'reason': reason,
        }
        if n in NEI_TERMS:
            terms, missing = NEI_TERMS[n]
            # These are actual searches over the already saved text, not a
            # reconstructed history of website visits or a full-source survey.
            hits = {term: [i for i, line in enumerate(page.splitlines(), 1)
                           if term.casefold() in ' '.join(line.split()).casefold()]
                    for term in terms}
            entry['nei_search_log'] = {
                'status': 'limited_illustration_audit_not_pilot_ready',
                'reviewer': 'Codex (AI assistance); human confirmation pending',
                'review_date': '2026-10-08',
                'corpus_id': 'apple-illustrations-snapshot-2026-10-08',
                'corpus_scope': 'Only the single captured official page listed for this example',
                'missing_information': missing,
                'checked_sources': [{
                    'url': entry['url'], 'snapshot': entry['source_snapshot'],
                    'snapshot_sha256': hashlib.sha256((source_dir / 'page.txt').read_bytes()).hexdigest(),
                    'source_accessed_at': metadata['captured_at_utc'],
                    'review_scope': 'Saved page text, battery section and linked footnotes',
                    'queries_and_matching_line_numbers': hits,
                }],
                'source_type_checks': {
                    'specification': 'not_separately_checked' if n == 20 else 'checked_saved_page',
                    'manual': 'not_checked',
                    'support_or_official_pdf': 'checked_saved_support_page' if n == 20 else 'not_separately_checked',
                },
                'stop_reason': 'This audit verifies an illustration against its named snapshot, not an exhaustive search of manufacturer materials.',
                'coverage_limitations': [
                    'Other applicable official manuals/support documents have not been systematically searched for this claim.',
                    'Keyword hits alone neither prove nor disprove the claim; read their context.',
                ],
                'production_label_ready': False,
            }
        assert (ROOT / entry['screenshot']).is_file(), entry['screenshot']
        result.append(entry)
    synthetic = [
        ('pin', 'SIM-PIN-01', 'tai nghe', 'thời gian nghe tối đa công bố', 'giờ', '20', '24', 'ANC bật; âm lượng 50%; một lần sạc; cùng điều kiện thử'),
        ('khối lượng', 'SIM-MASS-01', 'hộp sạc USB-C', 'khối lượng công bố', 'g', '32', '34', 'khối lượng hộp không có tai nghe; cùng cấu hình'),
        ('Bluetooth', 'SIM-BT-01', 'hệ thống kết nối', 'phiên bản Bluetooth', '', '5.2', '5.3', 'cùng phần cứng/firmware'),
    ]
    for n, (kind, product, part, attr, unit, v1, v2, condition) in enumerate(synthetic, 21):
        scope = f'Sản phẩm giả định {product}; bản R1; thị trường TEST; bộ phận {part}; thuộc tính {attr}; hiệu lực 08/10/2026.'
        claim = f'{product} bản R1 có {attr} {v1} {unit}; {condition}.'
        evidence = [f'{scope} {condition}. Giá trị: {value} {unit}.'.replace(' .', '.') for value in (v1, v2)]
        result.append({
            'id': f'EX-{n:02}', 'title': f'EX-{n:02} — Xung đột {kind} (GIẢ LẬP)',
            'group': 'Hai nguồn giả lập cùng phạm vi, trái nhau; chưa có quy tắc ưu tiên',
            'original_ad': claim, 'original_claim': claim, 'reviewed_claim': claim,
            'original_origin': 'synthetic_test_fixture', 'origin_verified_as_llm': False,
            'original_generation': None, 'revision_origin': 'assistant_authored_test_fixture',
            'revision_editor': 'Codex', 'revision_date': '2026-10-08',
            'creation_request': 'Bổ sung ít nhất 2–3 ca xung đột, và ghi đúng nguồn gốc từng mẫu.',
            'dataset_eligible': False, 'dataset_exclusion_reason': 'Ca giả lập do trợ lý soạn để kiểm thử luật; không phải quảng cáo LLM trong thực nghiệm hoặc nguồn Apple.',
            'scope': scope, 'source_id': None, 'url': None, 'quotes': [{'text': s, 'fixture_id': f'EX-{n:02}-{i}'} for i, s in enumerate(evidence, 1)],
            'conditions_summary': condition, 'condition_ref': None, 'label': 'NEI', 'nei_type': 'conflict',
            'values': f'Nguồn giả lập 1: {v1} {unit}; nguồn giả lập 2: {v2} {unit}. Cùng phạm vi, điều kiện, hiệu lực và mức ưu tiên; không nguồn nào thay thế nguồn kia.',
            'label_scope': 'reviewed_claim_only',
            'reason': 'C1 phát hiện hai nguồn giả lập không tương thích về cùng thuộc tính và phạm vi, chưa có căn cứ giải quyết. Trả NEI-xung đột trước khi C2/C3 chấp nhận hay bác bỏ claim; lưu cả hai phía. Không gán thông số này cho Apple.',
        })
    return {'schema_version': 1, 'purpose': 'documentation_examples_not_experimental_dataset',
            'source_docx_sha256': hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(), 'examples': result}


def validate(data):
    assert len(data['examples']) == 23
    assert [e['id'] for e in data['examples']] == [f'EX-{n:02}' for n in range(1, 24)]
    for e in data['examples']:
        assert not e['dataset_eligible']
        assert not e['origin_verified_as_llm']
        if e['original_origin'] == 'unknown_legacy':
            page = (ROOT / e['source_snapshot']).read_text()
            for q in e['quotes']:
                assert page[q['start_offset']:q['end_offset']] == q['text'], e['id']
            for field in ('screenshot', 'full_screenshot'):
                assert (ROOT / e[field]).is_file(), e[field]
            if e['nei_type'] == 'missing':
                log = e['nei_search_log']
                assert log['production_label_ready'] is False
                assert len(log['checked_sources']) == 1
                source = log['checked_sources'][0]
                assert hashlib.sha256((ROOT / source['snapshot']).read_bytes()).hexdigest() == source['snapshot_sha256']
                for term, expected_lines in source['queries_and_matching_line_numbers'].items():
                    actual = [i for i, line in enumerate(page.splitlines(), 1)
                              if term.casefold() in ' '.join(line.split()).casefold()]
                    assert actual == expected_lines, (e['id'], term)
        else:
            assert e['nei_type'] == 'conflict' and e['url'] is None
            assert len(e['quotes']) == 2
    for metadata_file in BASE.glob('*/metadata.json'):
        metadata = json.loads(metadata_file.read_text())
        assert metadata['status'] == 200, metadata_file
        for name, expected in metadata['files'].items():
            content = (metadata_file.parent / name).read_bytes()
            assert len(content) == expected['bytes']
            assert hashlib.sha256(content).hexdigest() == expected['sha256'], name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    target = BASE / 'examples.json'
    data = json.loads(target.read_text()) if args.check else build()
    validate(data)
    if not args.check:
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PASS: 20 source-checked legacy examples + 3 synthetic conflicts; verbatim excerpts and capture hashes verified.')


if __name__ == '__main__':
    main()
