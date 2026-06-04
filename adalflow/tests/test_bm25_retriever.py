import unittest
from adalflow.components.retriever.bm25_retriever import BM25Retriever
import os

class TestBM25Retriever(unittest.TestCase):
    def setUp(self):
        self.documents = [
            "The quick brown fox jumps over the lazy dog",
            "A quick brown dog outruns a slow fox",
            "The dog is lazy and the fox is quick",
            "Lazy dogs and quick foxes"
        ]
        self.retriever = BM25Retriever(top_k=2)
        self.retriever.build_index_from_documents(self.documents)

    def test_basic_retrieval(self):
        query = "quick fox"
        results = self.retriever(query)
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0].doc_indices), 2)
        # Verify indices are valid
        for idx in results[0].doc_indices:
            self.assertTrue(0 <= idx < len(self.documents))

    def test_list_query(self):
        queries = ["quick fox", "lazy dog"]
        results = self.retriever(queries)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].query, "quick fox")
        self.assertEqual(results[1].query, "lazy dog")

    def test_serialization(self):
        path = "test_bm25_index.json"
        self.retriever.save_to_file(path)

        retriever2 = BM25Retriever.load_from_file(path)
        self.assertEqual(retriever2.top_k, self.retriever.top_k)
        self.assertEqual(retriever2.total_documents, self.retriever.total_documents)

        query = "quick fox"
        results1 = self.retriever(query)
        results2 = retriever2(query)

        self.assertEqual(results1[0].doc_indices, results2[0].doc_indices)

        if os.path.exists(path):
            os.remove(path)

    def test_empty_query(self):
        query = "nonexistentword"
        results = self.retriever(query)
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0].doc_indices), 2)
        self.assertEqual(results[0].doc_scores, [0.0, 0.0])

if __name__ == "__main__":
    unittest.main()
