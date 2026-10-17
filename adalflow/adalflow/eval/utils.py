# from hotpotqa github
import re
import string
from collections import Counter

# Pre-compiled regex and translation table for high-performance string normalization
_ARTICLES_RE = re.compile(r"\b(a|an|the)\b")
_PUNC_TABLE = str.maketrans("", "", string.punctuation)


def normalize_answer(s: str) -> str:
    """Normalize text by lowering case, stripping punctuation, removing articles, and normalizing whitespace."""
    # Fast path: C-accelerated translate for punctuation removal and pre-compiled regex for articles
    s = _ARTICLES_RE.sub(" ", s.lower().translate(_PUNC_TABLE))
    return " ".join(s.split())


def f1_score(y: str, y_gt: str) -> float:
    if not isinstance(y, str) or not isinstance(y_gt, str):
        raise ValueError(f"y: {y},{type(y)}, y_gt: {y_gt},{type(y_gt)} must be string.")
    prediction_tokens = normalize_answer(y).split()
    ground_truth_tokens = normalize_answer(y_gt).split()

    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())

    if len(prediction_tokens) == len(ground_truth_tokens) == 0:
        # Unlike most tasks, QReCC and SQuAD-2.0 assign 1.0 in this edge case. We don't for uniformity.
        print(
            "\n#> F1 Metric: Rare edge case of len(prediction_tokens) == len(ground_truth_tokens) == 0.\n"
        )

    if num_same == 0:
        return 0

    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)

    return f1
