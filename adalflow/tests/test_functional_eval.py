import pytest
from adalflow.eval.functional import confidence_interval, longest_common_substring


def test_confidence_interval_bounds():
    judgements = [1, 1, 0, 1, 0, 1, 1]
    lower, upper = confidence_interval(judgements, confidence=0.95)
    assert 0 <= lower <= upper <= 1
    assert pytest.approx(lower, 0.01) == 0.354
    assert upper == 1.0  # Clipped at 1.0


def test_confidence_interval_confidence_levels():
    judgements = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    # Wider interval for higher confidence
    lower_90, upper_90 = confidence_interval(judgements, confidence=0.90)
    lower_99, upper_99 = confidence_interval(judgements, confidence=0.99)
    assert lower_99 < lower_90
    assert upper_99 > upper_90


def test_confidence_interval_error_handling():
    with pytest.raises(ValueError, match="judgements must be a list"):
        confidence_interval("invalid")

    with pytest.raises(ValueError, match="judgements must contain only integers or floats"):
        confidence_interval(["a", "b"])

    with pytest.raises(ValueError, match="confidence must be a number"):
        confidence_interval([1, 0], confidence="high")

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval([1, 0], confidence=1.5)

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval([1, 0], confidence=0)


def test_longest_common_substring():
    s1 = "abcdfghijk"
    s2 = "abedfghxyz"
    assert longest_common_substring(s1, s2) == "dfgh"
