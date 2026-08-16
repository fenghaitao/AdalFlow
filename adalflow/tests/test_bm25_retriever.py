import unittest
from adalflow.components.retriever.bm25_retriever import BM25Retriever
from adalflow.core.types import RetrieverOutput


class TestBM25Retriever(unittest.TestCase):

    def setUp(self):
        self.documents = [
            "hello world",
            "world is beautiful",
            "today is a good day",
            "hello adalflow framework retriever",
        ]
        self.retriever = BM25Retriever(top_k=2, documents=self.documents, use_tokenizer=False)

    def test_initialization_and_indexing(self):
        self.assertTrue(self.retriever.indexed)
        self.assertEqual(self.retriever.total_documents, 4)
        self.assertIsNotNone(self.retriever._doc_len_norm)
        self.assertIn("hello", self.retriever._inverted_index)

    def test_call_retrieval(self):
        output = self.retriever("hello")
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 1)
        self.assertIsInstance(output[0], RetrieverOutput)
        self.assertEqual(len(output[0].doc_indices), 2)
        # "hello" appears in doc 0 and doc 3
        self.assertIn(output[0].doc_indices[0], [0, 3])

    def test_unindexed_error(self):
        empty_retriever = BM25Retriever(top_k=2, use_tokenizer=False)
        with self.assertRaises(ValueError):
            empty_retriever("test")

    def test_reset_index(self):
        self.retriever.reset_index()
        self.assertFalse(self.retriever.indexed)
        self.assertEqual(self.retriever.total_documents, 0)
        self.assertIsNone(self.retriever._doc_len_norm)
        self.assertEqual(self.retriever._inverted_index, {})

    def test_with_tokenizer(self):
        tokenized_retriever = BM25Retriever(top_k=2, documents=self.documents, use_tokenizer=True)
        output = tokenized_retriever("hello")
        self.assertEqual(len(output[0].doc_indices), 2)


if __name__ == "__main__":
    unittest.main()
