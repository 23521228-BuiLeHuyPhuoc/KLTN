#!/usr/bin/env python3
"""Mô phỏng độ chính xác ước lượng ΔFAR (B1 − P) trên tập test theo họ sản phẩm.

Mục đích (T4a, rà soát 08/10/2026): kiểm tra xem cỡ test dự kiến
(4 họ, sàn 10 R + 10 NEI…) có đủ để phân biệt hai hệ thống không.
Đây là mô phỏng với GIẢ ĐỊNH, không phải kết quả thí nghiệm.

- FAR: tỷ lệ claim R hoặc NEI bị gán nhầm thành Supported.
- Cluster bootstrap: lấy mẫu lại cả HỌ sản phẩm (không lấy từng claim) vì claim
  cùng họ tương quan; với ít họ, khoảng tin cậy rất rộng hoặc thiếu ổn định.
Chỉ dùng thư viện chuẩn; seed cố định để tái lập.
"""
import argparse
import math
import random


def logit(p): return math.log(p / (1 - p))
def expit(x): return 1 / (1 + math.exp(-x))


def simulate_test(rng, families, per_family, far_b1, far_p, sd_family, corr):
    """Trả danh sách theo họ: [(lỗi_B1, lỗi_P) cho từng claim R/NEI]."""
    data = []
    for _ in range(families):
        u = rng.gauss(0, sd_family)  # độ khó chung của họ
        rows = []
        for _ in range(per_family):
            z = rng.random()
            e_b1 = z < expit(logit(far_b1) + u)
            # Lỗi P tương quan với lỗi B1 trên cùng claim (dùng chung z với xác suất corr).
            z2 = z if rng.random() < corr else rng.random()
            e_p = z2 < expit(logit(far_p) + u)
            rows.append((e_b1, e_p))
        data.append(rows)
    return data


def delta(fams):
    rows = [r for f in fams for r in f]
    return sum(a - b for a, b in rows) / len(rows)


def cluster_ci(rng, data, reps, alpha):
    stats = sorted(delta([rng.choice(data) for _ in data]) for _ in range(reps))
    lo = stats[int(alpha / 2 * reps)]
    hi = stats[min(reps - 1, int((1 - alpha / 2) * reps))]
    return lo, hi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--families', type=int, nargs='+', default=[4, 6, 8])
    ap.add_argument('--per-family', type=int, default=5, help='claim R+NEI mỗi họ (sàn 20 / 4 họ = 5)')
    ap.add_argument('--far-b1', type=float, default=0.30)
    ap.add_argument('--far-p', type=float, default=0.15)
    ap.add_argument('--sd-family', type=float, default=0.5)
    ap.add_argument('--corr', type=float, default=0.5)
    ap.add_argument('--sims', type=int, default=400)
    ap.add_argument('--reps', type=int, default=400)
    ap.add_argument('--seed', type=int, default=20261008)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    print(f'Giả định: FAR_B1={a.far_b1}, FAR_P={a.far_p}, sd_họ={a.sd_family}, tương quan={a.corr}, '
          f'{a.sims} mô phỏng × {a.reps} bootstrap, seed={a.seed}')
    print('họ  claim_R+NEI  độ_rộng_CI95_TB  tỷ_lệ_CI_loại_0')
    for k in a.families:
        for per in sorted({a.per_family, a.per_family * 2}):
            widths, excl = [], 0
            for _ in range(a.sims):
                d = simulate_test(rng, k, per, a.far_b1, a.far_p, a.sd_family, a.corr)
                lo, hi = cluster_ci(rng, d, a.reps, 0.05)
                widths.append(hi - lo)
                excl += lo > 0
            print(f'{k:>3}  {k*per:>11}  {sum(widths)/len(widths):>15.3f}  {excl/a.sims:>15.2f}')


if __name__ == '__main__':
    main()
