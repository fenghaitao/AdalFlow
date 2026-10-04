# from hotpotqa github
import re

import string
from collections import Counter


# Pre-compile regex and build translation table for high performance
_ARTICLES_RE = re.compile(r"\b(a|an|the)\b")
_PUNC_TABLE = str.maketrans("", "", string.punctuation)


def normalize_answer(s: str) -> str:
    """Normalize text by converting to lower case, removing punctuation, articles, and extra whitespace.

    Optimized by using module-level pre-compiled regex and str.translate for punctuation removal.
    """
    # 1. Lowercase and remove punctuation via fast C-implemented translate table
    s = s.lower().translate(_PUNC_TABLE)
    # 2. Remove articles 'a', 'an', 'the' using pre-compiled regex
    s = _ARTICLES_RE.sub(" ", s)
    # 3. Collapse multiple whitespace characters
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
