#!/usr/bin/env python3
"""Chặn rò nhãn vàng/vết P trước khi nạp INPUT_JSON vào prompt B0/B1 (T4b, 08/10/2026).

Dùng: python3 scripts/check_input_leak.py input.json [...]  → exit 1 nếu có khóa cấm.
"""
import json
import sys

FORBIDDEN = {'label', 'gold', 'gold_label', 'expected', 'nei_type', 'reason', 'verdict',
             'p_output', 'trace', 'relation', 'c2_relation', 'prediction', 'annotator',
             'reviewed_claim', 'label_scope'}


def leaks(node, path='$'):
    if isinstance(node, dict):
        for k, v in node.items():
            if k.lower() in FORBIDDEN:
                yield f'{path}.{k}'
            yield from leaks(v, f'{path}.{k}')
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaks(v, f'{path}[{i}]')


def main(paths):
    bad = [(p, hit) for p in paths for hit in leaks(json.load(open(p, encoding='utf-8')))]
    for p, hit in bad:
        print(f'LEAK {p}: {hit}')
    print('FAIL' if bad else 'PASS')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
