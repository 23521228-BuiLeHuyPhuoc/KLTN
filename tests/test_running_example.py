"""Khóa kết quả ví dụ xuyên suốt (sổ tay mục 7) để tài liệu không lệch với mã tham chiếu."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import demo_running_example as d  # noqa: E402
from abc_reference import verdict, label_of  # noqa: E402

EXPECTED = {  # loại: (P, P−part, P−B, P−role, P−inherit)
    'cha': ('Supported', 'Supported', 'Supported', 'Supported', 'NEI-missing'),
    'COND': ('NEI-missing', 'NEI-missing', 'Supported', 'NEI-missing', 'NEI-missing'),
    'VAL': ('Refuted', 'Refuted', 'Refuted', 'Refuted', 'NEI-missing'),
    'ROLE': ('NEI-missing', 'NEI-missing', 'NEI-missing', 'Supported', 'NEI-missing'),
    'PART': ('Refuted', 'NEI-conflict', 'Refuted', 'Refuted', 'Refuted'),
    'trần': ('Supported', 'Supported', 'Supported', 'Supported', 'NEI-missing'),
    'sạc nhanh': ('Supported', 'Supported', 'Supported', 'Supported', 'NEI-missing'),
}


class RunningExample(unittest.TestCase):
    def test_table_in_handbook(self):
        for kind, _, c in d.CASES:
            got = tuple(label_of(verdict(c, d.EVIDENCE, ablate=a)) for a in d.ABLATIONS)
            got += (label_of(verdict(c, d.EVIDENCE, policy='literal')),)
            self.assertEqual(got, EXPECTED[kind], kind)


if __name__ == '__main__':
    unittest.main()
