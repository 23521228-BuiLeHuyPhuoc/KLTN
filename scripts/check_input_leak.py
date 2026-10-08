#!/usr/bin/env python3
"""Kiểm payload trước khi gửi cho B0/B1/P hoặc bước trích xuất (bản 10/2026).

Ba lớp kiểm (docs/KE_HOACH_CHI_TIET_SINH_VIEN.md, mục 3.2, W10.3 và module M9):
1. Danh sách CHO PHÉP theo loại payload (--kind b0|b1|p|extract): mọi khóa ngoài
   schema đều FAIL, kể cả khóa vô hại, để không lọt trường mới chưa được duyệt.
2. Danh sách CẤM ở mọi độ sâu: nhãn chuẩn, lý do người gán, nhật ký tìm nguồn,
   bằng chứng chuẩn, nguồn gốc mẫu (ordinary/variant), thao tác tạo biến thể,
   dấu vết quyết định của P.
3. Giá trị chuỗi và mã định danh: không được chứa tên nhãn hoặc tên nhóm mẫu,
   và claim_id/chunk_id phải là mã mờ (không mã hóa nhóm/biến thể/nhãn).

PASS chỉ nghĩa là payload qua ba lớp trên; nó KHÔNG chứng minh hết mọi đường
rò (ví dụ thứ tự mẫu theo nhãn, câu biến thể quá lộ). Các kiểm còn lại nằm ở
quy trình khóa test và đọc mẫu thủ công.

Dùng: python3 scripts/check_input_leak.py --kind b1 payload.json [...]
Không có --kind: chỉ chạy lớp 2 và 3 (tương thích bản cũ).
Mã thoát 1 nếu có vi phạm.
"""
import argparse
import json
import re
import sys

FORBIDDEN_KEYS = {
    # nhãn / đáp án / kết luận người gán
    'label', 'labels', 'gold', 'gold_label', 'expected', 'nei_type', 'reason', 'rationale',
    'verdict', 'prediction', 'predicted_label', 'annotator', 'reviewer', 'reviewer_code',
    'label_scope', 'label_status', 'label_review_status', 'label_proposed',
    'reviewed_claim', 'gold_evidence', 'gold_evidence_sets', 'evidence_set_gold', 'is_gold',
    'search_log', 'nei_search_log', 'production_label_ready', 'stop_reason',
    # nguồn gốc mẫu và thao tác tạo biến thể
    'origin', 'original_origin', 'group', 'sample_group', 'ordinary_llm', 'controlled_variant',
    'variant', 'variant_of', 'parent_id', 'parent_claim_id', 'mutation', 'mutation_type',
    'operation', 'edit_note', 'editor', 'revision_editor', 'requested_error_type',
    'dataset_eligible', 'dataset_exclusion_reason', 'split',
    # dấu vết quyết định của P
    'p_output', 'trace', 'relation', 'c2_relation', 'is_supported', 'is_contradicted',
}

VALUE = {'kind', 'role', 'a', 'b', 'closed', 'v', 'op'}
CLAIM_RECORD = {'product', 'version', 'market', 'part', 'condition_ref', 'universal', 'attributes'}
ATTRIBUTE = {'attribute', 'part', 'unit', 'value', 'conditions', 'quote', 'char_start', 'char_end'}
EVIDENCE_RECORD = {'id', 'chunk_id', 'source_id', 'product', 'version', 'market', 'part', 'attribute',
                   'unit', 'value', 'conditions', 'condition_ref', 'quote', 'char_start', 'char_end'}
PRODUCT_CONTEXT = {'product', 'version', 'market', 'brand'}
EVIDENCE_TEXT = {'chunk_id', 'source_id', 'text', 'heading_path', 'footnotes', 'locale', 'url', 'retrieved_at'}

# Cây schema: khóa → tập khóa con cho phép; '*' = tự do (vẫn chạy lớp 2 và 3).
SCHEMAS = {
    'b0': {'claim_id': None, 'claim_text': None, 'product_context': PRODUCT_CONTEXT,
           'evidence_texts': EVIDENCE_TEXT},
    'b1': {'claim_id': None, 'claim_text': None, 'product_context': PRODUCT_CONTEXT,
           'extraction_run_id': None, 'normalized_records_sha256': None,
           'normalized_records': {'claim_record', 'evidence_records'}},
    'extract': {'claim_id': None, 'claim_text': None, 'product_context': PRODUCT_CONTEXT,
                'evidence_texts': EVIDENCE_TEXT},
}
SCHEMAS['p'] = SCHEMAS['b1']
NESTED = {'claim_record': CLAIM_RECORD, 'attributes': ATTRIBUTE, 'evidence_records': EVIDENCE_RECORD,
          'value': VALUE, 'conditions': '*', 'heading_path': '*', 'footnotes': '*'}

LABEL_WORDS = re.compile(r'\b(supported|refuted|nei|not enough info|ordinary_llm|controlled_variant|'
                         r'nhãn chuẩn|biến thể)\b', re.IGNORECASE)
OPAQUE_ID = re.compile(r'^[a-z]{1,3}_[0-9a-f]{6,}$')
ID_KEYS = {'claim_id', 'chunk_id', 'id'}


def check_allowed(node, allowed, path):
    """Lớp 1: chỉ cho phép khóa có trong schema."""
    if allowed == '*' or allowed is None:
        return
    if isinstance(node, list):
        for i, v in enumerate(node):
            yield from check_allowed(v, allowed, f'{path}[{i}]')
        return
    if not isinstance(node, dict):
        return
    for k, v in node.items():
        if k not in allowed:
            yield f'{path}.{k}: khóa ngoài schema'
            continue
        child = allowed.get(k) if isinstance(allowed, dict) else NESTED.get(k)
        if child is None and k in NESTED:
            child = NESTED[k]
        yield from check_allowed(v, child, f'{path}.{k}')


def check_forbidden(node, path='$'):
    """Lớp 2 và 3: khóa cấm ở mọi độ sâu, giá trị chuỗi lộ nhãn, mã không mờ."""
    if isinstance(node, dict):
        for k, v in node.items():
            p = f'{path}.{k}'
            if k.lower() in FORBIDDEN_KEYS:
                yield f'{p}: khóa cấm'
            if k in ID_KEYS and isinstance(v, str) and not OPAQUE_ID.match(v):
                yield f'{p}: mã không mờ {v!r} (dùng dạng c_1a2b3c…)'
            yield from check_forbidden(v, p)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from check_forbidden(v, f'{path}[{i}]')
    elif isinstance(node, str) and LABEL_WORDS.search(node):
        yield f'{path}: chuỗi chứa từ nhãn/nhóm mẫu {LABEL_WORDS.search(node).group(0)!r}'


def problems(payload, kind=None):
    items = payload if isinstance(payload, list) else [payload]
    out = []
    for i, item in enumerate(items):
        base = f'$[{i}]' if isinstance(payload, list) else '$'
        if kind:
            out += list(check_allowed(item, SCHEMAS[kind], base))
        out += list(check_forbidden(item, base))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--kind', choices=sorted(SCHEMAS))
    ap.add_argument('paths', nargs='+')
    a = ap.parse_args(argv)
    bad = []
    for p in a.paths:
        with open(p, encoding='utf-8') as f:
            bad += [(p, hit) for hit in problems(json.load(f), a.kind)]
    for p, hit in bad:
        print(f'LEAK {p}: {hit}')
    print('FAIL' if bad else 'PASS (chỉ chứng nhận ba lớp kiểm trong docstring)')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
