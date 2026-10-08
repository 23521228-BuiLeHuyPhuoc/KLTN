#!/usr/bin/env python3
"""Hàm tham chiếu cho luật A–B–C1–C2–C3 (docs/QUY_TAC_ABC.md).

Đây là bản cài đặt *tham chiếu* để kiểm thử đặc tả, không phải pipeline P
chính thức và không đọc văn bản tự do: đầu vào là hồ sơ đã chuẩn hóa bằng tay
(tests/fixtures/examples_structured.json). Chỉ dùng thư viện chuẩn.

Hai chính sách điều kiện cho bước B:
- 'literal': claim thiếu điều kiện mà nguồn có → nguồn bị loại (UNKNOWN),
  trừ khi claim có condition_ref tới đúng chú thích.
- 'inherit_headline' (DỰ THẢO, xem docs/QUYET_DINH_CAN_CHOT.md D1): claim
  không nêu điều kiện thì kế thừa điều kiện thử của nguồn; điều kiện claim nêu
  rõ vẫn phải khớp; claim có lượng từ phổ quát ("luôn", "mọi chế độ") không
  được kế thừa.
"""
from decimal import Decimal
from itertools import combinations

S, R, U = 'SUPPORT', 'CONTRADICT', 'UNKNOWN'
CONFLICT = 'CONFLICT'
POLICIES = ('literal', 'inherit_headline')
UNIT_FACTORS = {('h', 'min'): Decimal(60), ('kg', 'g'): Decimal(1000)}


class RecordError(ValueError):
    """Hồ sơ hỏng (khoảng đảo biên, thiếu trường): lỗi kỹ thuật, không phải NEI."""


def dec(x):
    return Decimal(str(x).replace(',', '.'))


def convert(value, unit, target):
    """Đổi đơn vị cùng đại lượng; trả None nếu không đổi được."""
    if unit == target:
        return value
    if (unit, target) in UNIT_FACTORS:
        f = UNIT_FACTORS[(unit, target)]
        return {**value, **{k: str(dec(value[k]) * f) for k in ('a', 'b') if k in value}}
    if (target, unit) in UNIT_FACTORS:
        f = UNIT_FACTORS[(target, unit)]
        return {**value, **{k: str(dec(value[k]) / f) for k in ('a', 'b') if k in value}}
    return None


# --- Miền giá trị: (lo, lo_closed, hi, hi_closed); None = vô hạn -------------

def domain(v):
    k = v['kind']
    if k == 'exact':
        a = dec(v['a'])
        return (a, True, a, True)
    if k == 'gt':
        return (dec(v['a']), False, None, False)
    if k == 'ge':
        return (dec(v['a']), True, None, False)
    if k == 'lt':
        return (None, False, dec(v['a']), False)
    if k == 'le':
        return (None, False, dec(v['a']), True)
    if k == 'interval':
        lo_c, hi_c = v.get('closed', (True, True))
        d = (dec(v['a']), lo_c, dec(v['b']), hi_c)
        if d[0] > d[2] or (d[0] == d[2] and not (lo_c and hi_c)):
            raise RecordError(f'khoảng rỗng/đảo biên: {v}')
        return d
    raise RecordError(f'không có miền cho kind={k}')


def subset(e, q):
    elo, elc, ehi, ehc = e
    qlo, qlc, qhi, qhc = q
    lo_ok = qlo is None or (elo is not None and (elo > qlo or (elo == qlo and (qlc or not elc))))
    hi_ok = qhi is None or (ehi is not None and (ehi < qhi or (ehi == qhi and (qhc or not ehc))))
    return lo_ok and hi_ok


def disjoint(e, q):
    def before(x, y):  # x nằm hẳn bên trái y
        if x[2] is None or y[0] is None:
            return False
        return x[2] < y[0] or (x[2] == y[0] and not (x[3] and y[1]))
    return before(e, q) or before(q, e)


def relate_domains(e, q):
    if subset(e, q):
        return S
    if disjoint(e, q):
        return R
    return U


# --- C2 -----------------------------------------------------------------------

def c2(ev, cl):
    """Quan hệ S/R/U giữa giá trị bằng chứng và giá trị claim (cùng đơn vị)."""
    ek, ck = ev['kind'], cl['kind']
    er, cr = ev.get('role', 'measurement'), cl.get('role', 'measurement')
    if ek == 'version' or ck == 'version':
        if ek == ck == 'version' and ev.get('op', 'eq') == cl.get('op', 'eq') == 'eq':
            norm = lambda s: s.strip().lower().removeprefix('bluetooth').strip()
            return S if norm(ev['v']) == norm(cl['v']) else R
        return U  # "5.0 trở lên", "5" so với "5.3": chưa có luật → U
    if 'unknown' in (er, cr):
        return U
    if ek == 'approx' or ck == 'approx':
        if ek == ck == 'approx' and er == cr and dec(ev['a']) == dec(cl['a']):
            return S
        return U  # không tự tạo dung sai
    if er in ('declared_maximum', 'declared_minimum'):
        if cr == er:
            if ek == ck == 'exact':
                return S if dec(ev['a']) == dec(cl['a']) else R
            return U
        if cr == 'measurement':
            if ek != 'exact':
                return U
            a = dec(ev['a'])
            implied = (None, False, a, True) if er == 'declared_maximum' else (a, True, None, False)
            rel = relate_domains(implied, domain(cl))
            # Cận công bố không bao giờ xác nhận một giá trị cụ thể luôn đạt được.
            return U if rel == S and ck == 'exact' else rel
        return U
    if cr in ('declared_maximum', 'declared_minimum'):
        return U  # đo đạc không suy ra mức công bố
    return relate_domains(domain(ev), domain(cl))


# --- A, B, C1, C3 -------------------------------------------------------------

SCOPE_KEYS = ('product', 'version', 'market', 'attribute')


def passes_a(claim, attr, ev, ablate):
    for k in SCOPE_KEYS:
        want = attr.get(k, claim.get(k))
        if want is not None and ev.get(k) != want:
            return None
    if 'part' not in ablate and ev.get('part') != attr.get('part', claim.get('part')):
        return None
    return convert(ev['value'], ev['unit'], attr['unit'])


def passes_b(claim, attr, ev, policy, ablate):
    if 'B' in ablate:
        return True
    cc, ec = attr.get('conditions', {}), ev.get('conditions', {})
    for k, v in cc.items():
        if ec.get(k) != v:
            return False  # sai chế độ hoặc nguồn không nêu → không dùng
    extra = set(ec) - set(cc)
    if not extra or claim.get('condition_ref'):
        return True
    return policy == 'inherit_headline' and not claim.get('universal')


def judge_attr(claim, attr, evidences, policy, ablate):
    cands = []
    for ev in evidences:
        val = passes_a(claim, attr, ev, ablate)
        if val is not None and passes_b(claim, attr, ev, policy, ablate):
            cands.append((ev, val))
    if not cands:
        return U, 'không còn bằng chứng sau A/B'
    groups = {}
    for ev, val in cands:
        key = 'all' if 'B' in ablate else tuple(sorted(ev.get('conditions', {}).items()))
        groups.setdefault(key, []).append((ev, val))
    for g in groups.values():
        for (e1, v1), (e2, v2) in combinations(g, 2):
            if R in (c2(v1, v2), c2(v2, v1)):
                return CONFLICT, f"{e1['id']} ↔ {e2['id']}"
    if len(groups) > 1:
        return U, 'claim không chỉ rõ chế độ; nhiều chế độ còn áp dụng'
    rels = [c2(val, attr['value']) for _, val in cands]
    if R in rels:
        return R, 'C2 bác bỏ'
    if S in rels:
        return S, 'C2 hỗ trợ'
    return U, 'C2 chưa đủ'


def verdict(claim, evidences, policy='literal', ablate=()):
    """Trả (nhãn, nei_type, vết). nhãn ∈ Supported/Refuted/NEI."""
    if policy not in POLICIES:
        raise ValueError(policy)
    trace = [judge_attr(claim, a, evidences, policy, set(ablate)) for a in claim['attributes']]
    rels = [t[0] for t in trace]
    if R in rels:
        return 'Refuted', None, trace
    if CONFLICT in rels:
        return 'NEI', 'conflict', trace
    if all(r == S for r in rels):
        return 'Supported', None, trace
    return 'NEI', 'missing', trace


def label_of(result):
    lab, nt, _ = result
    return f'NEI-{nt}' if lab == 'NEI' else lab
