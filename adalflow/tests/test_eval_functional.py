import numpy as np
import pytest

from adalflow.eval.functional import confidence_interval, longest_common_substring


def test_confidence_interval_basic():
    judgements = [1, 1, 0, 1, 0, 1, 1]
    lower, upper = confidence_interval(judgements, confidence=0.95)

    # Expected mean ~0.7142857, std ~0.48795
    mean = np.mean(judgements)
    se = np.std(judgements, ddof=1) / np.sqrt(len(judgements))
    z_expected = 1.9599639845400536
    moe_expected = z_expected * se

    assert lower == pytest.approx(max(0, mean - moe_expected))
    assert upper == pytest.approx(min(1, mean + moe_expected))
    assert 0 <= lower <= upper <= 1


def test_confidence_interval_validation():
    with pytest.raises(ValueError, match="judgements must be a list"):
        confidence_interval("not a list")

    with pytest.raises(ValueError, match="judgements must contain only integers or floats"):
        confidence_interval([1, "a", 0])

    with pytest.raises(ValueError, match="confidence must be a number"):
        confidence_interval([1, 0, 1], confidence="high")

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval([1, 0, 1], confidence=1.5)

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval([1, 0, 1], confidence=0)


def test_confidence_interval_clipping():
    # Mean = 1, std = 0
    lower, upper = confidence_interval([1, 1, 1, 1], confidence=0.95)
    assert lower == 1.0
    assert upper == 1.0


def test_longest_common_substring():
    s1 = "abcdfghijk"
    s2 = "abedfghxyz"
    assert longest_common_substring(s1, s2) == "dfgh"
