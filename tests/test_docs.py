"""Kiểm hai docx: HuP3 (báo cáo cũ) theo kiểm tra 08/10; HuP4 (đề cương bản 2) theo sổ tay bản 2."""
import io
import re
import sys
import unittest
from pathlib import Path
from xml.dom import minidom
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import update_thesis_docs as u  # noqa: E402

TITLE_VI = 'Phương pháp kiểm chứng phát biểu quảng cáo dựa trên bằng chứng văn bản cho tai nghe không dây'
TITLE_EN = 'Text-evidence-based method for verifying advertising claims about wireless headphones'


def raw(name):
    with ZipFile(io.BytesIO((ROOT / name).read_bytes())) as z:
        assert z.testzip() is None
        for n in z.namelist():
            if n.endswith('.xml') or n.endswith('.rels'):
                minidom.parseString(z.read(n))
        return z.read('word/document.xml').decode('utf-8')


def text(xml):
    return ''.join(re.findall(r'<w:t[^>]*>([^<]*)', xml))


class DocsTest(unittest.TestCase):
    def test_report_unchanged_content(self):
        u.validate_content(u.REPORT, minidom.parseString(raw(u.REPORT)))

    def test_proposal_title_and_frame(self):
        s = text(raw(u.PROPOSAL))
        for must in (TITLE_VI, TITLE_EN, 'ĐỀ CƯƠNG CHI TIẾT', 'Cán bộ hướng dẫn', 'Thời gian thực hiện',
                     '15/09/2026', 'Sinh viên thực hiện', 'Xác nhận của CBHD', 'Tài liệu tham khảo'):
            self.assertIn(must, s)

    def test_proposal_matches_notebook(self):
        xml = raw(u.PROPOSAL)
        s = text(xml)
        for must in ('SAV', 'RQ1', 'RQ2', 'RQ3', 'TN1', 'TN2', 'TN3', 'TN4', '−10 điểm phần trăm',
                     'GĐ1', 'GĐ10', '≈ 222–350 giờ', 'Không phải đóng góp'):
            self.assertIn(must, s)
        for banned in ('DỰ THẢO', 'Bản đề xuất điều chỉnh', 'TN5', 'TN6', 'E1', 'E3', '120 phát biểu'):
            self.assertNotIn(banned, s)
        self.assertNotRegex(xml, r'w:color w:val="[cC]00000"')
        nb = (ROOT / 'deliverables/KE_HOACH_CHI_TIET_SINH_VIEN.md').read_text(encoding='utf-8')
        for shared in ('SAV', '≈ 222–350 giờ', '−10 điểm phần trăm', '09/10–18/10', '28/12–31/12'):
            self.assertIn(shared, nb)


class NotebookTest(unittest.TestCase):
    def setUp(self):
        self.nb = (ROOT / 'deliverables/KE_HOACH_CHI_TIET_SINH_VIEN.md').read_text(encoding='utf-8')

    def test_sections(self):
        for h in ('## 0. Tự đánh giá kế hoạch', '## 2. Tính mới của khóa luận',
                  '### 3.1 Bảng tổng kết toàn bộ công việc', '## 16. Ngoài phạm vi'):
            self.assertIn(h, self.nb)

    def test_linear_dependencies(self):
        rows = re.findall(r'^\| (B\d\d) \| \d+ \|[^|]*\|[^|]*\| ([^|]*) \|', self.nb, flags=re.M)
        self.assertEqual([r[0] for r in rows], [f'B{i:02d}' for i in range(1, 53)])
        for code, deps in rows:
            for d in re.findall(r'B\d\d', deps):
                self.assertLess(int(d[1:]), int(code[1:]), (code, d))

    def test_step_details_in_order(self):
        heads = re.findall(r'^#### (B\d\d) — ', self.nb, flags=re.M)
        self.assertEqual(heads, [f'B{i:02d}' for i in range(1, 53)])

    def test_schedule_not_overlapping(self):
        spans = re.findall(r'^\| \d+ \| [^|]+ \| (\d\d)/(\d\d)–(\d\d)/(\d\d) \| B', self.nb, flags=re.M)
        self.assertEqual(len(spans), 10)
        prev = None
        for d1, m1, d2, m2 in spans:
            start, end = (int(m1), int(d1)), (int(m2), int(d2))
            self.assertLessEqual(start, end)
            if prev:
                self.assertLess(prev, start)
            prev = end


if __name__ == '__main__':
    unittest.main()
