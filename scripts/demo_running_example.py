#!/usr/bin/env python3
"""Ví dụ xuyên suốt AirPods Max 2 (sổ tay mục 7): chạy mã tham chiếu P trên hồ sơ NHẬP TAY.

Không gọi mô hình, không phải đầu ra trích xuất tự động, không phải kết quả thí nghiệm.
Số liệu nguồn lấy từ evidence/2026-10-08/apple-max2-vn/page.txt (chụp 2026-10-08):
"Thời gian nghe lên đến 20 giờ ... khi bật tính năng Chủ Động Khử Tiếng Ồn" (chú thích 10:
âm lượng 50%, chống ồn bật, Âm Thanh Không Gian cố định); "5 phút sạc ... khoảng 1,5 giờ"
(chú thích 11); AirPods Max 2 gồm đệm tai 386,2 gram; Smart Case 134,5 gram; Bluetooth 5.3.
Câu claim là câu minh họa (EX-09/10/11 là unknown_legacy; các biến thể còn lại do sổ tay soạn).
Dùng: python3 scripts/demo_running_example.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from abc_reference import verdict, label_of  # noqa: E402

M = lambda a: {'kind': 'exact', 'role': 'declared_maximum', 'a': a}  # noqa: E731
X = lambda a: {'kind': 'exact', 'role': 'measurement', 'a': a}  # noqa: E731
BARE = lambda a: {'kind': 'exact', 'role': 'stated_spec', 'a': a}  # noqa: E731
FN10 = {'anc': 'on', 'volume': '50', 'spatial': 'fixed'}


def ev(i, part, attr, unit, val, cond):
    return {'id': i, 'product': 'AirPods Max', 'version': '2', 'market': 'VN', 'part': part,
            'attribute': attr, 'unit': unit, 'value': val, 'conditions': cond}


EVIDENCE = [
    ev('e_bat', 'headphone', 'battery_single', 'h', M('20'), FN10),
    ev('e_qc', 'headphone', 'quick_charge', 'h', {'kind': 'approx', 'role': 'measurement', 'a': '1.5'},
       {'charge_minutes': '5', **FN10}),
    ev('e_w', 'headphone', 'weight', 'g', X('386.2'), {}),
    ev('e_wc', 'case', 'weight', 'g', X('134.5'), {}),
    ev('e_bt', 'headphone', 'bluetooth', '-', {'kind': 'version', 'v': '5.3'}, {}),
]


def claim(attr, unit, val, cond=None, part='headphone', **kw):
    return {'product': 'AirPods Max', 'version': '2', 'market': None, 'part': part, **kw,
            'attributes': [{'attribute': attr, 'unit': unit, 'value': val, 'conditions': cond or {}}]}


CASES = [
    ('cha', 'AirPods Max 2 cho thời gian nghe lên đến 20 giờ với một lần sạc khi bật Chủ Động Khử Tiếng Ồn.',
     claim('battery_single', 'h', M('20'), {'anc': 'on'})),
    ('COND', 'AirPods Max 2 cho thời gian nghe lên đến 20 giờ với một lần sạc khi tắt Chủ Động Khử Tiếng Ồn.',
     claim('battery_single', 'h', M('20'), {'anc': 'off'})),
    ('VAL', 'AirPods Max 2 cho thời gian nghe lên đến 25 giờ với một lần sạc khi bật Chủ Động Khử Tiếng Ồn.',
     claim('battery_single', 'h', M('25'), {'anc': 'on'})),
    ('ROLE', 'AirPods Max 2 cho chính xác 20 giờ nghe với một lần sạc khi bật Chủ Động Khử Tiếng Ồn.',
     claim('battery_single', 'h', X('20'), {'anc': 'on'})),
    ('PART', 'Smart Case của AirPods Max 2 nặng 386,2 gram.',
     claim('weight', 'g', X('386.2'), part='case')),
    ('trần', 'AirPods Max 2 có thời lượng pin 20 giờ.', claim('battery_single', 'h', BARE('20'))),
    ('sạc nhanh', 'Sạc AirPods Max 2 trong 5 phút cho khoảng 1,5 giờ nghe.',
     claim('quick_charge', 'h', {'kind': 'approx', 'role': 'measurement', 'a': '1.5'}, {'charge_minutes': '5'})),
]
ABLATIONS = [(), ('part',), ('B',), ('role',)]


def main():
    head = ['loại', 'P'] + ['P−' + a[0] for a in ABLATIONS[1:]] + ['P−inherit', 'claim']
    print(' | '.join(head))
    for kind, text, c in CASES:
        row = [kind] + [label_of(verdict(c, EVIDENCE, ablate=a)) for a in ABLATIONS]
        row += [label_of(verdict(c, EVIDENCE, policy='literal')), text]
        print(' | '.join(row))


if __name__ == '__main__':
    main()
