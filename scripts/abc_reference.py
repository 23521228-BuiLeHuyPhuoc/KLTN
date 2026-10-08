#!/usr/bin/env python3
"""Hàm tham chiếu cho luật A–B–C1–C2–C3 (docs/QUY_TAC_ABC.md, bản 10/2026).

Đây là bản cài đặt *tham chiếu* để kiểm thử đặc tả. Nó KHÔNG đọc văn bản tự
do và KHÔNG phải pipeline P hoàn chỉnh: đầu vào là hồ sơ đã chuẩn hóa (ví dụ
tests/fixtures/examples_structured.json, nhập tay). Module P thật sẽ gọi hàm
`verdict` này sau bước trích xuất (xem docs/KE_HOACH_CHI_TIET_SINH_VIEN.md,
module M7). Chỉ dùng thư viện chuẩn.

Chính sách điều kiện (bước B):
- 'inherit_headline' (MẶC ĐỊNH, chính sách chung v3 dùng cho người gán, B0, B1
  và P — docs/HUONG_DAN_GAN_NHAN.md §4): claim không nêu một điều kiện mà nguồn
  gắn với thông số thì kế thừa điều kiện thử của chính thông số đó; điều kiện
  claim nêu rõ phải khớp; claim có lượng từ phổ quát ("luôn", "mọi chế độ")
  không được kế thừa (nguồn khác điều kiện chỉ còn dùng để tìm phản ví dụ).
  Nếu sau kế thừa còn nhiều chế độ: mọi cách đọc cùng bác bỏ → bác bỏ; mọi cách
  đọc cùng hỗ trợ → hỗ trợ; còn lại → UNKNOWN (NEI-missing).
- 'literal': chỉ dùng cho phân tích thành phần P−inherit; claim thiếu điều kiện
  mà nguồn có → nguồn bị loại, trừ khi claim có condition_ref.

Vai trò giá trị (value_role): 'measurement', 'declared_maximum',
'declared_minimum', 'unknown'; riêng claim có thêm 'stated_spec' cho con số
trần không kèm định tính ("pin 8 giờ"): được hiểu là nhắc lại thông số công bố
nên nhận vai trò của bản ghi nguồn tương ứng.

Ablation hỗ trợ: 'part' (bỏ kiểm bộ phận), 'B' (bỏ kiểm điều kiện),
'role' (coi mọi giá trị là đo đạc, bỏ phân biệt mức công bố).
"""
from decimal import Decimal, InvalidOperation
from itertools import combinations

S, R, U = 'SUPPORT', 'CONTRADICT', 'UNKNOWN'
CONFLICT = 'CONFLICT'
POLICIES = ('inherit_headline', 'literal')
ABLATIONS = ('part', 'B', 'role')
KINDS = ('exact', 'gt', 'ge', 'lt', 'le', 'interval', 'approx', 'version')
EVIDENCE_ROLES = ('measurement', 'declared_maximum', 'declared_minimum', 'unknown')
CLAIM_ROLES = EVIDENCE_ROLES + ('stated_spec',)
DECLARED = ('declared_maximum', 'declared_minimum')
UNIT_FACTORS = {('h', 'min'): Decimal(60), ('kg', 'g'): Decimal(1000)}


class RecordError(ValueError):
    """Hồ sơ hỏng (thiếu trường, enum lạ, khoảng đảo biên): lỗi kỹ thuật, không phải NEI."""


def dec(x):
    try:
        return Decimal(str(x).replace(',', '.'))
    except InvalidOperation as exc:
        raise RecordError(f'không đọc được số: {x!r}') from exc


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


# --- Kiểm hồ sơ: hồ sơ hỏng phải thành lỗi kỹ thuật, không thành nhãn ----------

def _check_value(v, roles, where):
    if not isinstance(v, dict) or v.get('kind') not in KINDS:
        raise RecordError(f'{where}: value.kind thiếu hoặc lạ: {v!r}')
    if v['kind'] == 'version':
        if not isinstance(v.get('v'), str) or not v['v'].strip():
            raise RecordError(f'{where}: phiên bản rỗng')
        return
    if v.get('role', 'measurement') not in roles:
        raise RecordError(f'{where}: value.role lạ: {v.get("role")!r}')
    if 'a' not in v or (v['kind'] == 'interval' and 'b' not in v):
        raise RecordError(f'{where}: thiếu biên giá trị')
    dec(v['a'])
    if 'b' in v:
        dec(v['b'])


def validate_claim(claim):
    if not isinstance(claim, dict) or not claim.get('product'):
        raise RecordError('claim: thiếu product')
    attrs = claim.get('attributes')
    if not isinstance(attrs, list) or not attrs:
        raise RecordError('claim: không có thuộc tính nào để kiểm')
    for i, a in enumerate(attrs):
        for k in ('attribute', 'unit', 'value'):
            if k not in a:
                raise RecordError(f'claim.attributes[{i}]: thiếu {k}')
        if not isinstance(a.get('conditions', {}), dict):
            raise RecordError(f'claim.attributes[{i}]: conditions phải là object')
        _check_value(a['value'], CLAIM_ROLES, f'claim.attributes[{i}]')


def validate_evidence(evidences):
    if not isinstance(evidences, list):
        raise RecordError('evidence: phải là danh sách')
    seen = set()
    for e in evidences:
        for k in ('id', 'product', 'attribute', 'unit', 'value'):
            if k not in e:
                raise RecordError(f'evidence {e.get("id")}: thiếu {k}')
        if e['id'] in seen:
            raise RecordError(f'evidence trùng id: {e["id"]}')
        seen.add(e['id'])
        if not isinstance(e.get('conditions', {}), dict):
            raise RecordError(f'evidence {e["id"]}: conditions phải là object')
        _check_value(e['value'], EVIDENCE_ROLES, f'evidence {e["id"]}')


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

def c2(ev, cl, ablate=()):
    """Quan hệ S/R/U giữa giá trị bằng chứng và giá trị claim (cùng đơn vị)."""
    ek, ck = ev['kind'], cl['kind']
    if ek == 'version' or ck == 'version':
        if ek == ck == 'version' and ev.get('op', 'eq') == cl.get('op', 'eq') == 'eq':
            norm = lambda s: s.strip().lower().removeprefix('bluetooth').strip()
            return S if norm(ev['v']) == norm(cl['v']) else R
        return U  # "5.0 trở lên", "5" so với "5.3": chưa có luật → U
    er, cr = ev.get('role', 'measurement'), cl.get('role', 'measurement')
    if er == 'stated_spec':
        raise RecordError('stated_spec chỉ dùng cho claim, không dùng cho bằng chứng')
    if cr == 'stated_spec':
        # Con số trần trong quảng cáo = nhắc lại thông số công bố (HUONG_DAN §5).
        cr = er if er in DECLARED else 'measurement'
    if 'role' in ablate:
        er = cr = 'measurement'
    if 'unknown' in (er, cr):
        return U
    if ek == 'approx' or ck == 'approx':
        if ek == ck == 'approx' and er == cr and dec(ev['a']) == dec(cl['a']):
            return S
        return U  # không tự tạo dung sai
    if er in DECLARED:
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
    if cr in DECLARED:
        return U  # đo đạc không suy ra mức công bố
    return relate_domains(domain(ev), domain(cl))


# --- A, B, C1, C3 -------------------------------------------------------------

SCOPE_KEYS = ('product', 'version', 'market', 'attribute')
FULL, REFUTE_ONLY = 'full', 'refute_only'


def passes_a(claim, attr, ev, ablate):
    for k in SCOPE_KEYS:
        want = attr.get(k, claim.get(k))
        if want is not None and ev.get(k) != want:
            return None
    if 'part' not in ablate and ev.get('part') != attr.get('part', claim.get('part')):
        return None
    return convert(ev['value'], ev['unit'], attr['unit'])


def passes_b(claim, attr, ev, policy, ablate):
    """FULL: dùng để hỗ trợ/bác bỏ; REFUTE_ONLY: chỉ làm phản ví dụ; None: loại."""
    if 'B' in ablate:
        return FULL
    cc, ec = attr.get('conditions', {}), ev.get('conditions', {})
    for k, v in cc.items():
        if ec.get(k) != v:
            return None  # sai chế độ hoặc nguồn không nêu → không dùng
    extra = set(ec) - set(cc)
    if not extra or claim.get('condition_ref'):
        return FULL
    if policy == 'literal':
        return None
    # Lượng từ phổ quát: không kế thừa; một chế độ cụ thể chỉ có thể là phản ví dụ.
    return REFUTE_ONLY if claim.get('universal') else FULL


def _combine(rels):
    if R in rels:
        return R
    if S in rels:
        return S
    return U


def judge_attr(claim, attr, evidences, policy, ablate):
    cands = []
    for ev in evidences:
        val = passes_a(claim, attr, ev, ablate)
        if val is None:
            continue
        use = passes_b(claim, attr, ev, policy, ablate)
        if use:
            cands.append((ev, val, use))
    if not cands:
        return U, 'không còn bằng chứng sau A/B'
    groups = {}
    for ev, val, use in cands:
        key = 'all' if 'B' in ablate else tuple(sorted(ev.get('conditions', {}).items()))
        groups.setdefault(key, []).append((ev, val, use))
    # C1: xung đột chỉ xét trong cùng phạm vi + cùng bộ điều kiện của thuộc tính này.
    for g in groups.values():
        for (e1, v1, _), (e2, v2, _) in combinations(g, 2):
            if R in (c2(v1, v2, ablate), c2(v2, v1, ablate)):
                return CONFLICT, f"{e1['id']} ↔ {e2['id']}"
    full = {k: g for k, g in groups.items() if any(u == FULL for *_, u in g)}
    # Phản ví dụ cho claim phổ quát: một chế độ cụ thể trái claim là đủ để bác bỏ.
    for g in groups.values():
        if any(u == REFUTE_ONLY for *_, u in g):
            if R in [c2(v, attr['value'], ablate) for _, v, _ in g]:
                return R, 'phản ví dụ cho claim phổ quát'
    if not full:
        return U, 'claim phổ quát: chưa có bằng chứng bao phủ mọi chế độ'
    per_group = [_combine([c2(v, attr['value'], ablate) for _, v, _ in g]) for g in full.values()]
    if len(per_group) > 1:
        if all(r == R for r in per_group):
            return R, 'mọi chế độ còn áp dụng đều bác bỏ'
        if all(r == S for r in per_group):
            return S, 'mọi chế độ còn áp dụng đều hỗ trợ'
        return U, 'claim không chỉ rõ chế độ; các chế độ cho kết luận khác nhau'
    rel = per_group[0]
    return rel, {R: 'C2 bác bỏ', S: 'C2 hỗ trợ', U: 'C2 chưa đủ'}[rel]


def verdict(claim, evidences, policy='inherit_headline', ablate=()):
    """Trả (nhãn, nei_type, vết). nhãn ∈ Supported/Refuted/NEI.

    C3 (tổng hợp nhiều thuộc tính, claim là phép hội):
    có thuộc tính bị bác bỏ → Refuted (xung đột ở thuộc tính KHÁC không cứu claim);
    nếu không, có thuộc tính xung đột → NEI-conflict; mọi thuộc tính hỗ trợ →
    Supported; còn lại → NEI-missing. Hồ sơ hỏng → RecordError (lỗi kỹ thuật).
    """
    if policy not in POLICIES:
        raise ValueError(policy)
    unknown = set(ablate) - set(ABLATIONS)
    if unknown:
        raise ValueError(f'ablation lạ: {sorted(unknown)}')
    validate_claim(claim)
    validate_evidence(evidences)
    trace = [judge_attr(claim, a, evidences, policy, set(ablate)) for a in claim['attributes']]
    rels = [t[0] for t in trace]
    if R in rels:
        return 'Refuted', None, trace
    if CONFLICT in rels:
        return 'NEI', 'conflict', trace
    if all(r == S for r in rels):
        return 'Supported', None, trace
    return 'NEI', 'missing', trace


def safe_verdict(claim, evidences, **kw):
    """Như verdict nhưng hồ sơ hỏng trả ('ERROR', thông điệp, []) để runner ghi lỗi kỹ thuật."""
    try:
        return verdict(claim, evidences, **kw)
    except RecordError as exc:
        return 'ERROR', str(exc), []


def label_of(result):
    lab, nt, _ = result
    if lab == 'ERROR':
        return 'ERROR'
    return f'NEI-{nt}' if lab == 'NEI' else lab
