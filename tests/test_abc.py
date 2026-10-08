"""Kiểm thử luật A–B–C (docs/QUY_TAC_ABC.md). Chạy: python3 -m unittest discover -s tests -v"""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from abc_reference import S, R, U, RecordError, c2, verdict, label_of  # noqa: E402

FIX = json.loads((ROOT / 'tests/fixtures/examples_structured.json').read_text())
EXAMPLES = json.loads((ROOT / 'evidence/2026-10-08/examples.json').read_text())['examples']


def M(a): return {'kind': 'exact', 'role': 'declared_maximum', 'a': a}
def X(a): return {'kind': 'exact', 'role': 'measurement', 'a': a}
def V(kind, a, **kw): return {'kind': kind, 'role': 'measurement', 'a': a, **kw}


def run(ex_id, which, policy):
    e = FIX['examples'][ex_id]
    return label_of(verdict(e[which], FIX['evidence_sets'][e['evidence_set']], policy))


def ev(i, val, cond=None, part='earbud'):
    return {'id': i, 'product': 'P', 'version': None, 'market': 'VN', 'part': part,
            'attribute': 'battery', 'unit': 'h', 'value': val, 'conditions': cond or {}}


def claim(val, cond=None, **kw):
    return {'product': 'P', 'version': None, 'market': 'VN', 'part': 'earbud', **kw,
            'attributes': [{'attribute': 'battery', 'unit': 'h', 'value': val, 'conditions': cond or {}}]}


class FixtureMatchesExamplesJson(unittest.TestCase):
    def test_expected_labels_copied_from_examples_json(self):
        for e in EXAMPLES:
            gold = e['label'] if e['label'] != 'NEI' else f"NEI-{e['nei_type']}"
            self.assertEqual(FIX['examples'][e['id']]['expected'], gold, e['id'])


class TwentyThreeExamples(unittest.TestCase):
    """Nhãn trong examples.json áp cho reviewed_claim (label_scope)."""

    def test_reviewed_claims_both_policies(self):
        for ex_id, e in FIX['examples'].items():
            for policy in ('literal', 'inherit_headline'):
                with self.subTest(ex=ex_id, policy=policy):
                    self.assertEqual(run(ex_id, 'claim_reviewed', policy), e['expected'])

    def test_original_claims_literal_policy_drift(self):
        """Phát hiện T3: đọc B theo nghĩa đen, 11 câu gốc đổi nhãn sang NEI."""
        drift = {i for i, e in FIX['examples'].items()
                 if run(i, 'claim_original', 'literal') != e['expected']}
        self.assertEqual(drift, {'EX-04', 'EX-06', 'EX-09', 'EX-11', 'EX-12', 'EX-13',
                                 'EX-14', 'EX-15', 'EX-17', 'EX-18', 'EX-19'})

    def test_original_claims_inherit_policy_only_market_drift(self):
        """Với luật DỰ THẢO D1 chỉ còn lệch do thị trường Moldova (D2)."""
        drift = {i for i, e in FIX['examples'].items()
                 if run(i, 'claim_original', 'inherit_headline') != e['expected']}
        self.assertEqual(drift, {'EX-13', 'EX-14', 'EX-15'})


class MandatoryCasesSection3(unittest.TestCase):
    """11 ca bắt buộc trong QUY_TAC_ABC.md §3."""

    def test_ex18_gt24_vs_eq24(self):
        self.assertEqual(c2(V('gt', '24'), X('24')), R)

    def test_ex18_boundary_gt24_vs_eq25(self):
        self.assertEqual(c2(V('gt', '24'), X('25')), U)

    def test_closed_boundary_ge24_vs_eq24(self):
        self.assertEqual(c2(V('ge', '24'), X('24')), U)

    def test_ex20_up_to_3_vs_exactly_3(self):
        self.assertEqual(c2(M('3'), X('3')), U)

    def test_exceeds_bound_up_to_3_vs_exactly_4(self):
        self.assertEqual(c2(M('3'), X('4')), R)

    def test_ex11_declared_max_20_vs_25(self):
        self.assertEqual(c2(M('20'), M('25')), R)

    def test_ex12_about_same(self):
        a = {'kind': 'approx', 'role': 'measurement', 'a': '1,5'}
        self.assertEqual(c2(a, dict(a, a='1.5')), S)

    def test_ex10_anc_on_vs_off_is_missing_not_conflict(self):
        res = verdict(claim(M('20'), {'anc': 'off'}), [ev('e', M('20'), {'anc': 'on'})])
        self.assertEqual(label_of(res), 'NEI-missing')

    def test_ex21_two_maxima_conflict(self):
        c = {'anc': 'on'}
        res = verdict(claim(M('20'), c), [ev('a', M('20'), c), ev('b', M('24'), c)])
        self.assertEqual(label_of(res), 'NEI-conflict')

    def test_ex22_two_weights_conflict(self):
        res = verdict(claim(X('32')), [ev('a', X('32')), ev('b', X('34'))])
        self.assertEqual(label_of(res), 'NEI-conflict')

    def test_ex23_two_versions_conflict(self):
        v = lambda s: {'kind': 'version', 'v': s}
        res = verdict(claim(v('5.2')), [ev('a', v('5.2')), ev('b', v('5.3'))])
        self.assertEqual(label_of(res), 'NEI-conflict')


class C2Table(unittest.TestCase):
    def test_rows(self):
        cases = [
            (X('5'), X('5'), S), (X('5'), X('6'), R),
            (V('ge', '24'), X('23'), R), (V('le', '3'), X('4'), R), (V('le', '3'), X('2'), U),
            (V('lt', '3'), X('3'), R), (V('lt', '3'), X('2'), U),
            (V('gt', '24'), V('gt', '20'), S), (V('gt', '20'), V('gt', '24'), U),
            (X('22'), V('interval', '20', b='24'), S), (X('25'), V('interval', '20', b='24'), R),
            (V('interval', '20', b='30'), V('interval', '25', b='40'), U),
            ({'kind': 'exact', 'role': 'declared_minimum', 'a': '2'},
             {'kind': 'exact', 'role': 'declared_minimum', 'a': '3'}, R),
            ({'kind': 'version', 'v': '5.3'}, {'kind': 'version', 'v': 'Bluetooth 5.3'}, S),
            (X('5'), {'kind': 'exact', 'role': 'unknown', 'a': '5'}, U),
            (X('20'), M('20'), U),  # đo đạc không suy ra mức công bố
        ]
        for e, q, want in cases:
            with self.subTest(e=e, q=q):
                self.assertEqual(c2(e, q), want)


class EdgeCases(unittest.TestCase):
    """Ca biên đặc tả chưa nói rõ; giá trị kỳ vọng là lựa chọn DỰ THẢO (QUYET_DINH D3)."""

    def test_open_interval_excludes_bound(self):
        self.assertEqual(c2(V('gt', '24'), V('interval', '0', b='24')), R)

    def test_inverted_interval_is_record_error(self):
        with self.assertRaises(RecordError):
            c2(V('interval', '30', b='20'), X('25'))

    def test_about_vs_exact_same_number_unknown(self):
        self.assertEqual(c2({'kind': 'approx', 'role': 'measurement', 'a': '1.5'}, X('1.5')), U)

    def test_bluetooth_ge_or_major_only_unknown(self):
        self.assertEqual(c2({'kind': 'version', 'v': '5.3'}, {'kind': 'version', 'v': '5.0', 'op': 'ge'}), U)

    def test_max_15_as_declared_vs_max_20_as_x_bound(self):
        # Đọc là mức công bố M: Refuted. Đọc là cận trên x≤15 vs x≤20: Supported (x≤15 ⇒ x≤20).
        self.assertEqual(c2(M('15'), M('20')), R)
        self.assertEqual(c2(V('le', '15'), V('le', '20')), S)

    def test_unit_conversion_minutes(self):
        e = dict(ev('e', X('0.5')), unit='h')
        c = claim(X('30'))
        c['attributes'][0]['unit'] = 'min'
        self.assertEqual(label_of(verdict(c, [e])), 'Supported')

    def test_universal_claim_does_not_inherit(self):
        e = ev('e', M('20'), {'anc': 'on', 'volume': '50'})
        self.assertEqual(label_of(verdict(claim(M('20'), {'anc': 'on'}, universal=True), [e], 'inherit_headline')), 'NEI-missing')
        self.assertEqual(label_of(verdict(claim(M('20'), {'anc': 'on'}), [e], 'inherit_headline')), 'Supported')

    def test_unspecified_mode_with_two_modes_is_missing_not_conflict(self):
        evs = [ev('on', M('20'), {'anc': 'on'}), ev('off', M('25'), {'anc': 'off'})]
        self.assertEqual(label_of(verdict(claim(M('20')), evs, 'inherit_headline')), 'NEI-missing')

    def test_refutation_beats_conflict_on_other_attribute(self):
        c = claim(X('32'))
        c['attributes'].append({'attribute': 'bt', 'unit': '-', 'value': {'kind': 'version', 'v': '5.0'}, 'conditions': {}})
        evs = [ev('a', X('32')), ev('b', X('34')), dict(ev('v', {'kind': 'version', 'v': '5.3'}), attribute='bt', unit='-')]
        self.assertEqual(label_of(verdict(c, evs)), 'Refuted')


class Ablations(unittest.TestCase):
    def test_minus_part_turns_ex03_into_conflict(self):
        e = FIX['examples']['EX-03']
        res = verdict(e['claim_reviewed'], FIX['evidence_sets']['a5'], ablate=('part',))
        self.assertEqual(label_of(res), 'NEI-conflict')

    def test_minus_b_lets_wrong_mode_through_ex10(self):
        e = FIX['examples']['EX-10']
        res = verdict(e['claim_reviewed'], FIX['evidence_sets']['mx'], ablate=('B',))
        self.assertEqual(label_of(res), 'Supported')  # sai: đúng là tác động P−B cần đo


if __name__ == '__main__':
    unittest.main()
