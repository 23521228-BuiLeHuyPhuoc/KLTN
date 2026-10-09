"""Kiểm thử neo nguồn σ (scripts/grounding_reference.py)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from grounding_reference import ground, ground_all  # noqa: E402

CHUNK = ('AirPods Max 2: Thời gian nghe lên đến 20 giờ với một lần sạc khi bật '
         'Chủ Động Khử Tiếng Ồn hoặc chế độ Xuyên Âm.')


def rec(value=20, role='declared_maximum', q='lên đến 20 giờ', cond=None, cq=None):
    r = {'id': 'e1', 'chunk_id': 'c1', 'part': 'headset', 'attribute': 'battery', 'unit': 'h',
         'value': {'kind': 'exact', 'role': role, 'a': value}, 'conditions': cond or {},
         'quotes': {'value': q}}
    for k, v in (cq or {}).items():
        r['quotes'][f'conditions.{k}'] = v
    return r


class GroundingTest(unittest.TestCase):
    def test_grounded_record_kept(self):
        g, why = ground(rec(cond={'anc': 'on'}, cq={'anc': 'bật Chủ Động Khử Tiếng Ồn'}), CHUNK)
        self.assertIsNotNone(g)
        self.assertEqual(why, [])

    def test_quote_not_in_chunk_dropped(self):
        g, why = ground(rec(q='lên đến 40 giờ', value=40), CHUNK)
        self.assertIsNone(g)
        self.assertEqual(why, ['value_not_in_chunk'])

    def test_value_differs_from_quote_dropped(self):
        g, why = ground(rec(value=24), CHUNK)
        self.assertIsNone(g)
        self.assertEqual(why, ['value_mismatch_quote'])

    def test_hallucinated_condition_dropped_not_removed(self):
        g, why = ground(rec(cond={'anc': 'off'}, cq={'anc': 'tắt chống ồn'}), CHUNK)
        self.assertIsNone(g)
        self.assertEqual(why, ['condition_not_grounded:anc'])

    def test_role_cue_overrides_wrong_role(self):
        g, why = ground(rec(role='measurement'), CHUNK)
        self.assertEqual(g['value']['role'], 'declared_maximum')
        self.assertIn('role_set_from_cue:declared_maximum', why)

    def test_declared_role_without_cue_becomes_unknown(self):
        g, why = ground(rec(q='20 giờ'), CHUNK)
        self.assertEqual(g['value']['role'], 'unknown')

    def test_ground_all_splits(self):
        kept, dropped = ground_all([rec(), rec(value=24)], {'c1': CHUNK})
        self.assertEqual(len(kept), 1)
        self.assertEqual(dropped[0]['reasons'], ['value_mismatch_quote'])


if __name__ == '__main__':
    unittest.main()
