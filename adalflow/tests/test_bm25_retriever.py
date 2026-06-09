
import pytest
from adalflow.components.retriever.bm25_retriever import BM25Retriever

def test_bm25_basic():
    # documents where terms are unique or at least < 50%
    documents = ["hello world", "beautiful day", "today good"]
    retriever = BM25Retriever(top_k=1, documents=documents, use_tokenizer=False)
    output = retriever("hello")
    assert output[0].doc_indices == [0]

    output = retriever("beautiful")
    assert output[0].doc_indices == [1]

def test_bm25_multi_query():
    documents = ["apple banana", "cherry dog", "elephant fox", "grape honey"]
    retriever = BM25Retriever(top_k=2, documents=documents, use_tokenizer=False)
    output = retriever(["apple", "cherry"])
    assert len(output) == 2
    assert output[0].query == "apple"
    assert 0 in output[0].doc_indices
    assert output[1].query == "cherry"
    assert 1 in output[1].doc_indices

def test_bm25_serialization(tmp_path):
    documents = ["hello world", "beautiful day", "today good"]
    retriever = BM25Retriever(top_k=1, documents=documents, use_tokenizer=False)
    path = tmp_path / "index.json"
    retriever.save_to_file(str(path))

    retriever2 = BM25Retriever.load_from_file(str(path))
    output = retriever2("hello")
    assert output[0].doc_indices == [0]
    assert retriever2.top_k == 1
    assert retriever2.indexed is True
