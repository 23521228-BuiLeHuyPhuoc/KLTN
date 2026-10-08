#!/usr/bin/env python3
"""Locate audited facts on original PDF pages; optionally render audit images.

String checks are regression guards, not a substitute for reading table headers.
Human-readable interpretation and caveats: docs/KIEM_TRA_PHAN_BIEN_2026-10-08.md.
Requires Poppler (pdftotext, and pdftoppm only with --record).
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence/2026-10-08/papers'
CHECKS = [
    (2, 3, ['Table 1', '0.14', '0.09'], 'FactLens: Pearson/Spearman sufficiency'),
    (2, 4, ['733', 'CoverBench'], 'FactLens: original claims, section 3.1'),
    (2, 10, ['Table 6', 'Sufficiency', '0.0486'], 'FactLens: evaluator/human alpha, not inter-annotator alpha'),
    (3, 1, ['18.8'], 'VerifierFC: prose claim; NOT adopted as the Table 1 delta'),
    (3, 6, ['Llama-3.2-3B', 'LoRA', '18.8%'], 'VerifierFC: verifier model and prose result'),
    (3, 7, ['Table 1', '44.8', '53.91'], 'VerifierFC: Llama-3.1-8B/QuanTemp Macro-F1'),
    (4, 6, ['N=12', '120 explanations', '40 unique'], 'CLUE: human evaluation section 5.1'),
    (4, 7, ['Table 1', '-0.080', '0.102'], 'CLUE: Qwen/DRUID correlation'),
    (4, 21, ['I.1', 'Forty claims', '120'], 'CLUE: human evaluation appendix'),
    (5, 8, ['McNemar', '0.05', 'not significant'], 'CoVer: author-reported test on Conflict, section 6.4'),
    (5, 9, ['Table 2', '86.0', '68.0', '73.4'], 'CoVer: Conflict metrics, not all-metric superiority'),
]
REFS = {
    'ref07-fever': ['809–819', '2018'],
    'ref08-averitec': ['NeurIPS 2023', 'Schlichtkrull'],
    'ref09-vifactcheck': ["AAAI'2025", '2412.15308'],
    'ref10-viwikifc': ['16 Mar 2026', '[v2]', '13 May 2024'],
    'ref11-vinumfcr': ['134–147', '2025', 'Luong'],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', action='store_true', help='Save page images and source/page manifest')
    args = parser.parse_args()
    facts = []
    if args.record:
        OUT.mkdir(parents=True, exist_ok=True)
    for paper, page, needles, note in CHECKS:
        source = ROOT / 'báo' / f'[{paper}].pdf'
        content = subprocess.check_output(['pdftotext', '-f', str(page), '-l', str(page), '-layout', str(source), '-']).decode()
        normalized = ' '.join(content.split())
        for needle in needles:
            assert needle in normalized, (paper, page, needle)
        fact = {'source': str(source.relative_to(ROOT)), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'pdf_page_1_based': page, 'description': note, 'checked_tokens': needles}
        if args.record:
            prefix = OUT / f'ref{paper:02}-page{page:02}'
            subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-singlefile', '-scale-to', '1500', '-png', str(source), str(prefix)], check=True)
            png = prefix.with_suffix('.png')
            fact['screenshot'] = str(png.relative_to(ROOT))
            fact['screenshot_sha256'] = hashlib.sha256(png.read_bytes()).hexdigest()
        facts.append(fact)
        print(f'PASS: [{paper}] PDF p.{page}: {note}')
    for ref, needles in REFS.items():
        content = (OUT.parent / ref / 'page.txt').read_text()
        for needle in needles:
            assert needle in content, (ref, needle)
        print(f'PASS: {ref}: bibliography checked against captured primary page')
    if args.record:
        (OUT / 'manifest.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
