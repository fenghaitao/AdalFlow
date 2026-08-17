import pytest
import os
import math
import numpy as np
from adalflow.components.retriever.bm25_retriever import BM25Retriever
from adalflow.core.types import Document


def test_bm25_retriever_basic():
    documents = ["hello world", "world is beautiful", "today is a good day"]
    retriever = BM25Retriever(top_k=1, documents=documents, use_tokenizer=False)

    res = retriever("hello")
    assert len(res) == 1
    assert res[0].doc_indices == [0]
    assert len(res[0].doc_scores) == 1
    assert res[0].doc_scores[0] > 0.0


def test_bm25_retriever_with_tokenizer():
    documents = ["hello world", "world is beautiful", "today is a good day"]
    retriever = BM25Retriever(top_k=2, documents=documents, use_tokenizer=True)

    res = retriever("world")
    assert len(res) == 1
    assert len(res[0].doc_indices) == 2
    assert 0 in res[0].doc_indices or 1 in res[0].doc_indices


def test_bm25_retriever_document_objects_and_map_func():
    docs = [
        Document(text="python programming language", id="1"),
        Document(text="java programming language", id="2"),
        Document(text="cooking recipes and food", id="3"),
    ]
    retriever = BM25Retriever(
        top_k=2,
        documents=docs,
        document_map_func=lambda d: d.text,
        use_tokenizer=False,
    )

    res = retriever("python")
    assert res[0].doc_indices[0] == 0


def test_bm25_get_batch_scores():
    documents = ["hello world", "world is beautiful", "today is a good day"]
    retriever = BM25Retriever(top_k=2, documents=documents, use_tokenizer=False)

    full_scores = retriever._get_scores(["world"])
    batch_scores = retriever._get_batch_scores(["world"], [0, 2])

    assert math.isclose(batch_scores[0], full_scores[0], abs_tol=1e-5)
    assert math.isclose(batch_scores[1], full_scores[2], abs_tol=1e-5)


def test_bm25_reset_and_rebuild():
    retriever = BM25Retriever(top_k=1, use_tokenizer=False)
    assert not retriever.indexed

    retriever.build_index_from_documents(["first document", "second document"])
    assert retriever.indexed

    res1 = retriever("first")
    assert res1[0].doc_indices == [0]

    retriever.reset_index()
    assert not retriever.indexed
    assert retriever._inverted_index is None
    assert retriever._doc_len_norm is None


def test_bm25_serialization(tmp_path):
    filepath = os.path.join(tmp_path, "bm25_index.json")
    documents = ["hello world", "world is beautiful", "today is a good day"]
    retriever = BM25Retriever(top_k=2, documents=documents, use_tokenizer=False)

    out_before = retriever("hello")
    retriever.save_to_file(filepath)

    retriever_loaded = BM25Retriever.load_from_file(filepath)
    out_after = retriever_loaded("hello")

    assert out_before[0].doc_indices == out_after[0].doc_indices
    assert np.allclose(out_before[0].doc_scores, out_after[0].doc_scores)
