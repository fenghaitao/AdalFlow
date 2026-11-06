import math

import pytest

from adalflow.eval.functional import confidence_interval, longest_common_substring


def test_confidence_interval_basic():
    judgements = [1, 1, 0, 1, 0, 1, 1]
    lower, upper = confidence_interval(judgements, confidence=0.95)
    # Check bounds are within [0, 1]
    assert 0 <= lower <= 1
    assert 0 <= upper <= 1
    assert lower < upper

    # Exact expected analytical calculations:
    mean_val = 5 / 7
    # variance with ddof=1: sum((x - 5/7)^2) / 6 = (5*(2/7)^2 + 2*(-5/7)^2) / 6 = (20/49 + 50/49) / 6 = 70 / (49*6) = 10 / 42 = 5/21
    # se = sqrt(5/21) / sqrt(7) = sqrt(5/147)
    std_err = math.sqrt((5 * (2 / 7) ** 2 + 2 * (5 / 7) ** 2) / 6) / math.sqrt(7)
    # Z for 0.95: 1.959963984540054
    expected_z = 1.959963984540054
    expected_moe = expected_z * std_err

    assert math.isclose(lower, max(0.0, mean_val - expected_moe), rel_tol=1e-6)
    assert math.isclose(upper, min(1.0, mean_val + expected_moe), rel_tol=1e-6)


def test_confidence_interval_different_confidence():
    judgements = [1, 0, 1, 0, 1, 0]
    lower_90, upper_90 = confidence_interval(judgements, confidence=0.90)
    lower_99, upper_99 = confidence_interval(judgements, confidence=0.99)

    # Higher confidence means wider interval
    assert (upper_99 - lower_99) > (upper_90 - lower_90)


def test_confidence_interval_validation():
    with pytest.raises(ValueError, match="judgements must be a list"):
        confidence_interval("invalid")

    with pytest.raises(ValueError, match="judgements must contain only integers or floats"):
        confidence_interval(["a", "b"])

    with pytest.raises(ValueError, match="confidence must be a number"):
        confidence_interval([1, 0, 1], confidence="high")

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval([1, 0, 1], confidence=1.5)

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval([1, 0, 1], confidence=0.0)


def test_longest_common_substring():
    s1 = "abcdfghijk"
    s2 = "abedfghxyz"
    assert longest_common_substring(s1, s2) == "dfgh"
