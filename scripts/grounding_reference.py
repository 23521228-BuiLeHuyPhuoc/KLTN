"""Kiểm neo nguồn (grounding) cho hồ sơ σ do LLM trích — thành phần thứ hai của SAV.

Mỗi dữ kiện nguồn do LLM trích phải kèm `quotes`: chuỗi nguyên văn trong đoạn cho
giá trị (bắt buộc), từng điều kiện và bộ phận (nếu có). Hàm `ground` kiểm tất định:

1. chuỗi trích phải nằm trong đoạn (so sau khi chuẩn hóa khoảng trắng, chữ thường);
2. con số trong chuỗi trích giá trị phải bằng `value` của dữ kiện;
3. từ chỉ vai trò trong chuỗi trích (“lên đến”, “tối đa”, “up to” / “ít nhất”, “tối thiểu”,
   “at least”) phải khớp `role`; không có từ chỉ vai trò mà LLM ghi mức công bố → `unknown`;
4. điều kiện hoặc bộ phận không neo được → dữ kiện bị loại (không đoán, không bỏ điều kiện,
   vì bỏ điều kiện có thể gây chấp nhận nhầm).

Dữ kiện bị loại được trả về kèm lý do để ghi vào trace; SAV chỉ nhận dữ kiện đã neo.
"""
import re
import unicodedata
from decimal import Decimal

MAX_CUES = ('lên đến', 'lên tới', 'tối đa', 'up to')
MIN_CUES = ('ít nhất', 'tối thiểu', 'at least')
NUM = re.compile(r'\d+(?:[.,]\d+)?')


def norm(s):
    s = unicodedata.normalize('NFC', s or '').lower()
    return re.sub(r'\s+', ' ', s).strip()


def numbers(s):
    return [Decimal(x.replace(',', '.')) for x in NUM.findall(s or '')]


def _value_of(v):
    if isinstance(v, dict):
        return v.get('a')
    return v


def ground(record, chunk_text):
    """Trả (record_đã_neo | None, danh_sách_lý_do). Không sửa record gốc."""
    text = norm(chunk_text)
    quotes = record.get('quotes') or {}
    reasons = []
    q_val = quotes.get('value')
    if not q_val or norm(q_val) not in text:
        return None, ['value_not_in_chunk']
    target = _value_of(record.get('value'))
    if target is None or Decimal(str(target)) not in numbers(q_val):
        return None, ['value_mismatch_quote']
    for key, val in (record.get('conditions') or {}).items():
        q = quotes.get(f'conditions.{key}')
        if not q or norm(q) not in text:
            reasons.append(f'condition_not_grounded:{key}')
    if record.get('part') is not None and 'part' in quotes and norm(quotes['part']) not in text:
        reasons.append('part_not_grounded')
    if reasons:
        return None, reasons
    out = dict(record)
    value = dict(record['value']) if isinstance(record.get('value'), dict) else record.get('value')
    qv = norm(q_val)
    has_max = any(c in qv for c in MAX_CUES)
    has_min = any(c in qv for c in MIN_CUES)
    if isinstance(value, dict):
        role = value.get('role')
        if has_max and role != 'declared_maximum':
            value['role'] = 'declared_maximum'
            reasons.append('role_set_from_cue:declared_maximum')
        elif has_min and role != 'declared_minimum':
            value['role'] = 'declared_minimum'
            reasons.append('role_set_from_cue:declared_minimum')
        elif not has_max and not has_min and role in ('declared_maximum', 'declared_minimum'):
            value['role'] = 'unknown'
            reasons.append('role_without_cue:unknown')
        out['value'] = value
    return out, reasons


def ground_all(records, chunks):
    """records: dữ kiện có `chunk_id`; chunks: {chunk_id: text}. Trả (giữ, loại)."""
    kept, dropped = [], []
    for r in records:
        g, why = ground(r, chunks.get(r.get('chunk_id'), ''))
        if g is None:
            dropped.append({'id': r.get('id'), 'reasons': why})
        else:
            kept.append(g)
    return kept, dropped
