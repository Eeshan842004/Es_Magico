import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from stats_utils import cluster_bootstrap_diff, cohen_kappa, confusion, recall_precision  # noqa: E402


def test_kappa_perfect_and_chance():
    assert cohen_kappa([1, 0, 1, 0], [1, 0, 1, 0]) == 1.0
    assert abs(cohen_kappa([1, 1, 0, 0], [1, 0, 1, 0])) < 1e-9  # exactly chance-level


def test_kappa_known_value():
    # 2x2: both FAIL=20, h FAIL/j PASS=5, h PASS/j FAIL=10, both PASS=15 -> kappa=0.4 (textbook)
    h = [1] * 20 + [1] * 5 + [0] * 10 + [0] * 15
    j = [1] * 20 + [0] * 5 + [1] * 10 + [0] * 15
    assert abs(cohen_kappa(h, j) - 0.4) < 1e-9


def test_kappa_undefined_is_nan():
    assert math.isnan(cohen_kappa([0, 0, 0], [0, 0, 0]))


def test_confusion_and_recall():
    c = confusion([1, 1, 0, 0], [1, 0, 1, 0])
    assert c == {"tp": 1, "fn": 1, "fp": 1, "tn": 1}
    assert recall_precision(c) == (0.5, 0.5)


def test_cluster_bootstrap_ci_contains_mean_and_is_ordered():
    v1 = [0.0, 0.2, 0.0, 0.4, 0.0, 0.2]
    v2 = [0.2, 0.4, 0.0, 0.6, 0.2, 0.2]
    m, lo, hi = cluster_bootstrap_diff(v1, v2, n_resamples=1000)
    assert lo <= m <= hi and m > 0
