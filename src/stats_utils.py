"""Small, dependency-light statistics used by agreement.py and analyze.py.

Kept separate and pure so they can be unit-tested without any data or API.
"""
from __future__ import annotations

import numpy as np


def cohen_kappa(a: list[int], b: list[int]) -> float:
    """Cohen's kappa for two binary raters (1 = FAIL, 0 = PASS, or any 0/1 coding).

    Returns NaN when kappa is undefined (both raters constant and identical):
    chance agreement is then 100%, so kappa = 0/0. We report NaN, not 1.0,
    because "no variation" is not evidence of agreement skill.
    """
    a_arr, b_arr = np.asarray(a), np.asarray(b)
    n = len(a_arr)
    if n == 0:
        return float("nan")
    po = float(np.mean(a_arr == b_arr))
    pa1, pb1 = a_arr.mean(), b_arr.mean()
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    if np.isclose(pe, 1.0):
        return float("nan")
    return float((po - pe) / (1 - pe))


def bootstrap_kappa_ci(a, b, n_resamples: int = 2000, seed: int = 42):
    """95% percentile bootstrap CI for kappa, resampling items. Skips undefined resamples."""
    rng = np.random.default_rng(seed)
    a_arr, b_arr = np.asarray(a), np.asarray(b)
    n = len(a_arr)
    vals = []
    for _ in range(n_resamples):
        idx = rng.integers(0, n, n)
        k = cohen_kappa(a_arr[idx], b_arr[idx])
        if not np.isnan(k):
            vals.append(k)
    if len(vals) < 20:
        return (float("nan"), float("nan"))
    return (float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5)))


def confusion(human: list[int], judge: list[int]) -> dict[str, int]:
    """Counts with FAIL=1 as the 'positive' class (the thing we want to catch)."""
    h, j = np.asarray(human), np.asarray(judge)
    return {
        "tp": int(np.sum((h == 1) & (j == 1))),  # both say FAIL
        "fn": int(np.sum((h == 1) & (j == 0))),  # judge MISSED a real failure (worst case)
        "fp": int(np.sum((h == 0) & (j == 1))),  # judge false alarm
        "tn": int(np.sum((h == 0) & (j == 0))),
    }


def recall_precision(c: dict[str, int]) -> tuple[float, float]:
    rec = c["tp"] / (c["tp"] + c["fn"]) if (c["tp"] + c["fn"]) else float("nan")
    prec = c["tp"] / (c["tp"] + c["fp"]) if (c["tp"] + c["fp"]) else float("nan")
    return rec, prec


def cluster_bootstrap_diff(rates_v1, rates_v2, n_resamples: int = 5000, seed: int = 42):
    """Paired cluster bootstrap over conversations.

    rates_v1[i], rates_v2[i] = per-conversation failure rate for conversation i
    (already averaged over its N samples). The conversation is the unit of
    resampling because samples within a conversation are not independent.
    Returns (mean_diff, ci_low, ci_high) for (v2 - v1).
    """
    d = np.asarray(rates_v2, dtype=float) - np.asarray(rates_v1, dtype=float)
    rng = np.random.default_rng(seed)
    n = len(d)
    means = np.array([d[rng.integers(0, n, n)].mean() for _ in range(n_resamples)])
    return float(d.mean()), float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))
