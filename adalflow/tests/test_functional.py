import unittest
import numpy as np
from adalflow.core.functional import get_top_k_indices_scores


class TestGetTopKIndicesScores(unittest.TestCase):
    def test_basic_list_input(self):
        scores = [1.0, 5.0, 2.0, 4.0, 3.0]
        indices, top_scores = get_top_k_indices_scores(scores, top_k=3)
        self.assertEqual(indices, [1, 3, 4])
        self.assertEqual(top_scores, [5.0, 4.0, 3.0])

    def test_basic_numpy_input(self):
        scores = np.array([10.5, 50.2, 20.1, 40.8, 30.0])
        indices, top_scores = get_top_k_indices_scores(scores, top_k=2)
        self.assertEqual(indices, [1, 3])
        self.assertEqual(top_scores, [50.2, 40.8])

    def test_edge_cases(self):
        # Empty inputs
        self.assertEqual(get_top_k_indices_scores([], 5), ([], []))
        self.assertEqual(get_top_k_indices_scores(np.array([]), 5), ([], []))

        # top_k <= 0
        self.assertEqual(get_top_k_indices_scores([1.0, 2.0, 3.0], 0), ([], []))
        self.assertEqual(get_top_k_indices_scores([1.0, 2.0, 3.0], -1), ([], []))

        # top_k >= len(scores)
        indices, top_scores = get_top_k_indices_scores([1.0, 3.0, 2.0], 3)
        self.assertEqual(indices, [1, 2, 0])
        self.assertEqual(top_scores, [3.0, 2.0, 1.0])

        indices, top_scores = get_top_k_indices_scores([1.0, 3.0, 2.0], 10)
        self.assertEqual(indices, [1, 2, 0])
        self.assertEqual(top_scores, [3.0, 2.0, 1.0])

    def test_negative_and_duplicates(self):
        scores = [-10.0, -2.0, -50.0, -5.0]
        indices, top_scores = get_top_k_indices_scores(scores, top_k=2)
        self.assertEqual(indices, [1, 3])
        self.assertEqual(top_scores, [-2.0, -5.0])

        # Duplicate values
        scores_dup = [5.0, 10.0, 10.0, 2.0]
        indices, top_scores = get_top_k_indices_scores(scores_dup, top_k=2)
        self.assertEqual(top_scores, [10.0, 10.0])
        self.assertEqual(set(indices), {1, 2})

    def test_small_array_threshold(self):
        # Small array (N <= 250, uses direct argsort path)
        np.random.seed(42)
        arr = np.random.randn(150)
        indices, top_scores = get_top_k_indices_scores(arr, top_k=10)
        expected_indices = np.argsort(arr)[-10:][::-1].tolist()
        expected_scores = arr[expected_indices].tolist()
        self.assertEqual(indices, expected_indices)
        self.assertEqual(top_scores, expected_scores)

    def test_large_array_argpartition(self):
        # Large array (N > 250, triggers argpartition path)
        np.random.seed(123)
        arr = np.random.randn(1000)
        indices, top_scores = get_top_k_indices_scores(arr, top_k=20)
        expected_indices = np.argsort(arr)[-20:][::-1].tolist()
        expected_scores = arr[expected_indices].tolist()
        self.assertEqual(indices, expected_indices)
        self.assertEqual(top_scores, expected_scores)

    def test_very_large_array(self):
        # Very large array (e.g., vocabulary size logits N=10,000)
        np.random.seed(456)
        arr = np.random.randn(10000)
        indices, top_scores = get_top_k_indices_scores(arr, top_k=50)
        expected_indices = np.argsort(arr)[-50:][::-1].tolist()
        expected_scores = arr[expected_indices].tolist()
        self.assertEqual(indices, expected_indices)
        self.assertEqual(top_scores, expected_scores)


if __name__ == "__main__":
    unittest.main()
