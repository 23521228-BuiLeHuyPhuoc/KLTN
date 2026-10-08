"""Kiểm nội dung hai docx theo thiết kế 08/10/2026 và hàng chữ ký CBHD."""
import io
import sys
import unittest
from pathlib import Path
from xml.dom import minidom
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import update_thesis_docs as u  # noqa: E402


def load(name):
    with ZipFile(io.BytesIO((u.ROOT / name).read_bytes())) as z:
        assert z.testzip() is None
        return minidom.parseString(z.read('word/document.xml'))


class DocsTest(unittest.TestCase):
    def test_validate_content(self):
        for name in (u.PROPOSAL, u.REPORT):
            with self.subTest(name=name):
                u.validate_content(name, load(name))

    def test_header_and_signature(self):
        s = u.text(load(u.PROPOSAL))
        self.assertIn('Bản đề xuất điều chỉnh, chờ GVHD xác nhận', s)
        self.assertIn('Xác nhận của CBHD', s)
        self.assertIn('15/09/2026', s)


if __name__ == '__main__':
    unittest.main()
