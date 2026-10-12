import pytest
import math
from statistics import NormalDist
from adalflow.eval.functional import confidence_interval


def test_confidence_interval_basic():
    judgements = [1, 1, 0, 1, 0, 1, 1]
    lower, upper = confidence_interval(judgements, confidence=0.95)

    assert 0.0 <= lower <= upper <= 1.0

    # Manual verification
    mean = sum(judgements) / len(judgements)
    variance = sum((x - mean) ** 2 for x in judgements) / (len(judgements) - 1)
    se = math.sqrt(variance) / math.sqrt(len(judgements))
    z = NormalDist().inv_cdf(1 - (1 - 0.95) / 2)
    expected_lower = max(0.0, mean - z * se)
    expected_upper = min(1.0, mean + z * se)

    assert pytest.approx(lower, rel=1e-5) == expected_lower
    assert pytest.approx(upper, rel=1e-5) == expected_upper


def test_confidence_interval_different_confidence_levels():
    judgements = [1, 0, 1, 1, 0, 1, 0, 1]
    lower_90, upper_90 = confidence_interval(judgements, confidence=0.90)
    lower_95, upper_95 = confidence_interval(judgements, confidence=0.95)
    lower_99, upper_99 = confidence_interval(judgements, confidence=0.99)

    # Higher confidence level -> wider interval
    assert (upper_90 - lower_90) < (upper_95 - lower_95) < (upper_99 - lower_99)


def test_confidence_interval_clipping():
    # All 1s -> std error 0 -> bounds equal mean
    lower, upper = confidence_interval([1, 1, 1, 1], confidence=0.95)
    assert lower == 1.0
    assert upper == 1.0

    # All 0s -> std error 0 -> bounds equal mean
    lower, upper = confidence_interval([0, 0, 0, 0], confidence=0.95)
    assert lower == 0.0
    assert upper == 0.0


def test_confidence_interval_invalid_inputs():
    with pytest.raises(ValueError, match="judgements must be a list"):
        confidence_interval("not a list")

    with pytest.raises(ValueError, match="judgements must contain only integers or floats"):
        confidence_interval([1, "a", 0])

    with pytest.raises(ValueError, match="confidence must be a number"):
        confidence_interval([1, 0], confidence="high")

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval([1, 0], confidence=1.5)

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval([1, 0], confidence=-0.1)
