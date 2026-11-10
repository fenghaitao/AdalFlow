import pytest
from adalflow.eval.functional import confidence_interval, longest_common_substring


def test_confidence_interval_basic():
    judgements = [1, 1, 0, 1, 0, 1, 1]
    lb, ub = confidence_interval(judgements, confidence=0.95)
    assert 0.0 <= lb <= ub <= 1.0
    assert abs(lb - 0.3528) < 0.001
    assert ub == 1.0


def test_confidence_interval_homogeneous():
    # All ones
    lb, ub = confidence_interval([1, 1, 1], confidence=0.95)
    assert lb == 1.0
    assert ub == 1.0

    # All zeros
    lb, ub = confidence_interval([0, 0, 0], confidence=0.95)
    assert lb == 0.0
    assert ub == 0.0


def test_confidence_interval_edge_cases():
    # Empty list
    assert confidence_interval([]) == (0.0, 1.0)

    # Single element
    assert confidence_interval([1]) == (0.0, 1.0)
    assert confidence_interval([0]) == (0.0, 1.0)


def test_confidence_interval_different_confidence_levels():
    judgements = [1, 0, 1, 1, 0, 1, 0, 1]
    lb90, ub90 = confidence_interval(judgements, confidence=0.90)
    lb99, ub99 = confidence_interval(judgements, confidence=0.99)
    # Higher confidence means wider interval (or equal when clipped)
    assert lb99 <= lb90
    assert ub99 >= ub90


def test_confidence_interval_validation():
    with pytest.raises(ValueError, match="judgements must be a list"):
        confidence_interval((1, 0))  # type: ignore

    with pytest.raises(
        ValueError, match="judgements must contain only integers or floats"
    ):
        confidence_interval(["1", "0"])  # type: ignore

    with pytest.raises(ValueError, match="confidence must be a number"):
        confidence_interval([1, 0], confidence="high")  # type: ignore

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval([1, 0], confidence=1.5)

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval([1, 0], confidence=0.0)


def test_longest_common_substring():
    assert longest_common_substring("abcdfghijk", "abedfghxyz") == "dfgh"
    assert longest_common_substring("", "abc") == ""
    assert longest_common_substring("apple", "apple") == "apple"
