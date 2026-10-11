
import numpy as np


def confidence_interval(
    judgements: list[float], confidence: float = 0.95
) -> tuple[float, float]:
    """
    Calculate the confidence interval for a list of binary judgments.

    Args:
        judgements (List[float]): List of binary judgments (1/0).
        confidence (float): Confidence level (default 0.95).

    Returns:
        tuple: Lower and upper bounds of the confidence interval.
    """
    if not isinstance(judgements, list):
        raise ValueError("judgements must be a list")

    if not all(isinstance(j, (int, float)) for j in judgements):
        raise ValueError("judgements must contain only integers or floats")

    if not isinstance(confidence, (int, float)):
        raise ValueError("confidence must be a number")

    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")

    # Step 1: Calculate the mean
    mean_score = np.mean(judgements)

    # Step 2: Calculate the standard error (SE)
    standard_error = np.std(judgements, ddof=1) / np.sqrt(len(judgements))

    # Step 3: Use the Z-critical value for the confidence interval based on confidence level
    z_critical = np.percentile(
        np.random.normal(0, 1, 1000000), 100 * (1 - (1 - confidence) / 2)
    )

    # Step 4: Calculate the margin of error (MoE)
    margin_of_error = z_critical * standard_error

    # Step 5: Calculate the confidence interval
    # Confidence interval (clipped to [0, 1])
    lower_bound = max(0, mean_score - margin_of_error)
    upper_bound = min(1, mean_score + margin_of_error)

    return (lower_bound, upper_bound)


def longest_common_substring(s1: str, s2: str) -> str:
    """
    Find the longest common substring between two strings.
    """
    if not s1 or not s2:
        return ""
    if s1 == s2:
        return s1
    if len(s1) <= len(s2) and s1 in s2:
        return s1
    if len(s2) < len(s1) and s2 in s1:
        return s2

    # Optimize DP space from O(M*N) 2D matrix to O(N) 1D array
    m, n = len(s1), len(s2)
    dp = [0] * (n + 1)

    longest_length = 0
    ending_index_s1 = 0

    for i in range(1, m + 1):
        ch1 = s1[i - 1]
        for j in range(n, 0, -1):
            if ch1 == s2[j - 1]:
                val = dp[j - 1] + 1
                dp[j] = val
                if val > longest_length:
                    longest_length = val
                    ending_index_s1 = i - 1
            else:
                dp[j] = 0

    return s1[ending_index_s1 - longest_length + 1 : ending_index_s1 + 1]


if __name__ == "__main__":
    # Example binary judgments (True/False as 1/0)
    judgements = [1, 1, 0, 1, 0, 1, 1]  # Convert to 1/0
    score_range = confidence_interval(judgements, confidence=0.96)
    print(score_range)

    # Example longest common substring
    s1 = "abcdfghijk"
    s2 = "abedfghxyz"
    cs = longest_common_substring(s1, s2)
    print(cs)
