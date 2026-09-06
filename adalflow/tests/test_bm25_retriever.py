import os
import tempfile

import numpy as np
import pytest

from adalflow.components.retriever.bm25_retriever import BM25Retriever
from adalflow.core.types import Document


def test_bm25_retriever_basic_init():
    documents = [
        "hello world",
        "world is beautiful",
        "today is a good day",
    ]
    retriever = BM25Retriever(top_k=2, documents=documents, use_tokenizer=False)
    assert retriever.indexed is True
    assert retriever.total_documents == 3

    output = retriever("hello")
    assert len(output) == 1
    assert output[0].doc_indices[0] == 0
    assert output[0].doc_scores[0] > 0.0


def test_bm25_retriever_build_index_and_map_func():
    docs = [
        Document(text="python programming language", id="1"),
        Document(text="java programming language", id="2"),
        Document(text="fast food recipe", id="3"),
    ]
    retriever = BM25Retriever(top_k=2, use_tokenizer=False)
    assert retriever.indexed is False

    retriever.build_index_from_documents(docs, document_map_func=lambda d: d.text)
    assert retriever.indexed is True

    output = retriever("python")
    assert output[0].doc_indices[0] == 0


def test_bm25_retriever_batch_scores():
    documents = [
        "apple banana orange",
        "banana orange grape",
        "grape kiwi mango",
    ]
    retriever = BM25Retriever(top_k=2, documents=documents, use_tokenizer=False)
    tokens = retriever._split_function("banana")

    full_scores = retriever._get_scores(tokens)
    batch_scores = retriever._get_batch_scores(tokens, doc_ids=[0, 1])

    assert len(batch_scores) == 2
    np.testing.assert_allclose(batch_scores[0], full_scores[0])
    np.testing.assert_allclose(batch_scores[1], full_scores[1])


test_docs = [
    "renewable energy sources like wind and solar power play a crucial role",
    "solar panels convert sunlight into electricity efficiently",
    "wind turbines generate clean electricity from wind energy",
]


def test_bm25_retriever_save_and_load():
    retriever = BM25Retriever(top_k=2, documents=test_docs, use_tokenizer=True)
    out_orig = retriever("solar electricity")

    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = os.path.join(tmp_dir, "bm25_index.json")
        retriever.save_to_file(file_path)
        assert os.path.exists(file_path)

        loaded_retriever = BM25Retriever.load_from_file(file_path)
        assert loaded_retriever.indexed is True
        out_loaded = loaded_retriever("solar electricity")

        assert out_orig[0].doc_indices == out_loaded[0].doc_indices
        np.testing.assert_allclose(out_orig[0].doc_scores, out_loaded[0].doc_scores)


def test_bm25_retriever_reset_index():
    retriever = BM25Retriever(top_k=2, documents=test_docs, use_tokenizer=False)
    assert retriever.indexed is True
    assert retriever._inverted_index is not None

    retriever.reset_index()
    assert retriever.indexed is False
    assert retriever.total_documents == 0
    assert retriever._inverted_index is None
    assert retriever._doc_len_norm is None

    with pytest.raises(ValueError, match="Index is not built"):
        retriever("solar")
