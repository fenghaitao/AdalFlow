import os
import pytest

import math
from adalflow.eval import (
    AnswerMatchAcc,
    RetrieverEvaluator,
    LLMasJudge,
)
from adalflow.eval.functional import confidence_interval


def test_answer_match_acc():
    pred_answers = ["positive", "negative", "this is neutral"]
    gt_answers = ["positive", "negative", "neutral"]
    answer_match_acc = AnswerMatchAcc(type="exact_match")
    acc = answer_match_acc.compute(pred_answers, gt_answers)
    avg_acc, acc_list = acc.avg_score, acc.per_item_scores
    assert avg_acc == 2 / 3
    assert acc_list == [1.0, 1.0, 0.0]
    answer_match_acc = AnswerMatchAcc(type="fuzzy_match")
    acc = answer_match_acc.compute(pred_answers, gt_answers)
    avg_acc, acc_list = acc.avg_score, acc.per_item_scores
    assert avg_acc == 1.0
    assert acc_list == [1.0, 1.0, 1.0]


def test_retriever_recall():
    retrieved_contexts = [
        ["Apple is founded before Google."],
        [
            "Feburary has 28 days in common years.",
            "Feburary has 29 days in leap years.",
            "Feburary is the second month of the year.",
        ],
    ]
    gt_contexts = [
        [
            "Apple is founded in 1976.",
            "Google is founded in 1998.",
            "Apple is founded before Google.",
        ],
        ["Feburary has 28 days in common years", "Feburary has 29 days in leap years"],
    ]
    retriever_recall = RetrieverEvaluator()
    eval_rslt = retriever_recall.compute(retrieved_contexts, gt_contexts)
    print(eval_rslt)
    avg_recall = eval_rslt.get("avg_recall")
    recall_list = eval_rslt.get("recall_list")
    avg_precision = eval_rslt.get("avg_precision")
    precision_list = eval_rslt.get("precision_list")
    # avg_recall, recall_list = eval_rslt.avg_score, eval_rslt.per_item_scores
    assert avg_recall == 2 / 3
    assert recall_list == [1 / 3, 1.0]
    assert avg_precision == 0.8333333333333333
    assert precision_list == [1.0, 0.6666666666666666]


# def test_retriever_relevance():
#     retrieved_contexts = [
#         "Apple is founded before Google.",
#         "Feburary has 28 days in common years. Feburary has 29 days in leap years. Feburary is the second month of the year.",
#     ]
#     gt_contexts = [
#         [
#             "Apple is founded in 1976.",
#             "Google is founded in 1998.",
#             "Apple is founded before Google.",
#         ],
#         ["Feburary has 28 days in common years", "Feburary has 29 days in leap years"],
#     ]
#     retriever_relevance = RetrieverRelevance()
#     avg_relevance, relevance_list = retriever_relevance.compute(
#         retrieved_contexts, gt_contexts
#     )
#     assert 0.8 < avg_relevance < 0.81
#     assert relevance_list[0] == 1.0
#     assert 0.6 < relevance_list[1] < 0.61


# This test is skipped by default. To run this test locally, set the environment variable RUN_LOCAL_TESTS to True (export RUN_LOCAL_TESTS=true).
@pytest.mark.skipif(not os.getenv("RUN_LOCAL_TESTS"), reason="Skip unless on local")
def test_llm_as_judge():

    questions = [
        "Is Beijing in China?",
        "Is Apple founded before Google?",
        "Is earth flat?",
    ]
    pred_answers = ["Yes", "Yes, Appled is founded before Google", "Yes"]
    gt_answers = ["Yes", "Yes", "No"]
    judgement_query = (
        "For the question, does the predicted answer contain the ground truth answer?"
    )
    llm_judge = LLMasJudge()
    avg_judgement, judgement_list = llm_judge.compute(
        questions, gt_answers, pred_answers, judgement_query
    )
    assert avg_judgement == 2 / 3
    assert judgement_list == [True, True, False]


def test_confidence_interval():
    # Valid binary inputs
    judgements = [1, 1, 0, 1, 0, 1, 1]
    lower, upper = confidence_interval(judgements, confidence=0.95)
    assert 0.0 <= lower <= 1.0
    assert 0.0 <= upper <= 1.0
    assert lower <= upper

    # Verify analytical correctness
    mean_score = 5 / 7
    # variance with ddof=1: sum((x - 5/7)^2) / 6 = (5*(2/7)^2 + 2*(-5/7)^2) / 6 = 5/21
    # se = sqrt(5/21) / sqrt(7) = sqrt(5/147)
    std_err = math.sqrt((5 * (2 / 7) ** 2 + 2 * (5 / 7) ** 2) / 6) / math.sqrt(7)
    # Z for 0.95 is ~1.959963984540054
    expected_z = 1.959963984540054
    expected_moe = expected_z * std_err
    assert math.isclose(lower, max(0.0, mean_score - expected_moe), rel_tol=1e-6)
    assert math.isclose(upper, min(1.0, mean_score + expected_moe), rel_tol=1e-6)

    # Test confidence levels (higher confidence means wider interval)
    l90, u90 = confidence_interval(judgements, confidence=0.90)
    l99, u99 = confidence_interval(judgements, confidence=0.99)
    assert l99 <= l90
    assert u99 >= u90

    # Input validations
    with pytest.raises(ValueError, match="judgements must be a list"):
        confidence_interval((1, 0, 1))

    with pytest.raises(
        ValueError, match="judgements must contain only integers or floats"
    ):
        confidence_interval(["a", "b"])

    with pytest.raises(ValueError, match="confidence must be a number"):
        confidence_interval(judgements, confidence="0.95")

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval(judgements, confidence=1.5)

    with pytest.raises(ValueError, match="confidence must be between 0 and 1"):
        confidence_interval(judgements, confidence=-0.1)
