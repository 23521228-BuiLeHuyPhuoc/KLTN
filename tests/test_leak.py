"""Kiểm scripts/check_input_leak.py trên payload mẫu (không phải dữ liệu thật)."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_input_leak import problems  # noqa: E402

B1_OK = {
    'claim_id': 'c_3f9a1b2c',
    'claim_text': 'AirPods Max 2 cho thời gian nghe lên đến 20 giờ khi tắt Chủ Động Khử Tiếng Ồn.',
    'product_context': {'brand': 'Apple', 'product': 'AirPods Max', 'version': '2', 'market': 'VN'},
    'extraction_run_id': 'x_20261101a',
    'normalized_records_sha256': '0' * 64,
    'normalized_records': {
        'claim_record': {'product': 'AirPods Max', 'version': '2', 'market': None, 'part': 'headphone',
                         'condition_ref': False, 'universal': False,
                         'attributes': [{'attribute': 'battery_single', 'unit': 'h',
                                         'value': {'kind': 'exact', 'role': 'declared_maximum', 'a': '20'},
                                         'conditions': {'anc': 'off'}}]},
        'evidence_records': [{'id': 'e_51c0ffee', 'chunk_id': 'k_a1b2c3d4', 'source_id': 'apple-max2-vn',
                              'product': 'AirPods Max', 'version': '2', 'market': 'VN', 'part': 'headphone',
                              'attribute': 'battery_single', 'unit': 'h',
                              'value': {'kind': 'exact', 'role': 'declared_maximum', 'a': '20'},
                              'conditions': {'anc': 'on', 'volume': '50'}}],
    },
}
B0_OK = {
    'claim_id': 'c_3f9a1b2c', 'claim_text': B1_OK['claim_text'], 'product_context': B1_OK['product_context'],
    'evidence_texts': [{'chunk_id': 'k_a1b2c3d4', 'source_id': 'apple-max2-vn',
                        'heading_path': ['Pin', 'AirPods Max 2'],
                        'text': 'Thời gian nghe lên đến 20 giờ với một lần sạc khi bật tính năng Chủ Động Khử Tiếng Ồn',
                        'footnotes': ['10. Thử nghiệm ... âm lượng 50%'], 'locale': 'vi-VN'}],
}


class LeakChecks(unittest.TestCase):
    def test_clean_payloads_pass(self):
        self.assertEqual(problems(B1_OK, 'b1'), [])
        self.assertEqual(problems(B1_OK, 'p'), [])
        self.assertEqual(problems(B0_OK, 'b0'), [])
        self.assertEqual(problems([B0_OK, B0_OK], 'b0'), [])

    def test_gold_label_key_fails(self):
        bad = dict(B1_OK, label='NEI')
        self.assertTrue(any('khóa cấm' in p for p in problems(bad)))
        self.assertTrue(any('ngoài schema' in p for p in problems(bad, 'b1')))

    def test_variant_provenance_fails_at_any_depth(self):
        bad = copy.deepcopy(B1_OK)
        bad['normalized_records']['claim_record']['attributes'][0]['mutation_type'] = 'wrong_mode'
        self.assertTrue(any('mutation_type' in p for p in problems(bad)))

    def test_unknown_key_fails_with_schema(self):
        bad = copy.deepcopy(B0_OK)
        bad['evidence_texts'][0]['is_in_gold_set'] = True
        self.assertTrue(any('is_in_gold_set' in p for p in problems(bad, 'b0')))
        self.assertEqual(problems(bad), [])  # không có schema: lớp 2 không bắt khóa lạ này

    def test_label_word_in_value_fails(self):
        bad = copy.deepcopy(B0_OK)
        bad['evidence_texts'][0]['footnotes'] = ['annotator note: Refuted']
        self.assertTrue(any('từ nhãn' in p for p in problems(bad, 'b0')))

    def test_non_opaque_id_fails(self):
        bad = dict(B0_OK, claim_id='EX-10-variant-wrong_mode')
        self.assertTrue(any('mã không mờ' in p for p in problems(bad, 'b0')))

    def test_p_trace_fails(self):
        bad = copy.deepcopy(B1_OK)
        bad['normalized_records']['evidence_records'][0]['c2_relation'] = 'UNKNOWN'
        self.assertTrue(problems(bad, 'b1'))


if __name__ == '__main__':
    unittest.main()
