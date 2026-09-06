"""BM25 retriever implementation."""

import heapq
import logging
import math
from collections.abc import Callable, Sequence
from typing import Any

import numpy as np

from adalflow.core.component import Component
from adalflow.core.retriever import (
    Retriever,
)
from adalflow.core.tokenizer import Tokenizer
from adalflow.core.types import (
    RetrieverDocumentsType,
    RetrieverOutput,
    RetrieverOutputType,
    RetrieverStrQueriesType,
    RetrieverStrQueryType,
)
from adalflow.utils.file_io import load_standard_json, save_json

log = logging.getLogger(__name__)

PARAM_K1 = 1.5
PARAM_B = 0.75
PARAM_EPSILON = 0.25


# TODO: move the functions in core.functional
def split_text_by_word_fn(x: str) -> list[str]:
    x = x.lower()
    return x.split(" ")


def split_text_by_word_fn_then_lower_tokenized(x: str) -> list[str]:
    tokenizer = Tokenizer()
    words = x.lower().split(" ")
    tokens = [tokenizer.encode(word) for word in words]
    final_tokens: list[str] = []
    for token_list in tokens:
        for token in token_list:
            final_tokens.append(tokenizer.decode([token]))
    return final_tokens


def split_text_tokenized(x: str) -> list[str]:
    tokenizer = Tokenizer()
    # words = x.lower().split(" ")
    tokens = tokenizer.encode(x)
    # print(tokens)
    final_tokens: list[str] = []
    for token in tokens:
        final_tokens.append(tokenizer.decode([token]))
    # print(final_tokens)
    return final_tokens


class BM25Retriever(Retriever[str, RetrieverStrQueryType]):
    __doc__ = r"""Fast Implementation of Best Matching 25 ranking function.

    It expects str as the final document type after ``document_map_func`` if the given document is not already in the format of List[str].
    It expects Union[str, Sequence[str]] as the input in :meth:`retrieve` method.

    .. math::

        \text{idf}(q_i) = \log\left(\frac{N - n(q_i) + 0.5}{n(q_i) + 0.5}\right)

        \text{score}(q, d) = \sum_{i=1}^{n} \text{idf}(q_i) \cdot \frac{f(q_i, d) \cdot (k1 + 1)}{f(q_i, d) + k1 \cdot \left(1 - b + b \cdot \frac{|d|}{\text{avgdl}}\right)}

    Explanation:
        - IDF(q_i) is the inverse document frequency of term q_i, which measures how important the term is. To avoid division by zero, 0.5 is added to the denominator, also for diminishing the weight of terms that occur very frequently in the document set and increase the weight of terms that occur rarely.
        - f(q_i, d) is the term frequency of term q_i in document d, which measures how often the term occurs in the document. The term frequency is normalized by dividing the raw term frequency by the document length.
        - |d| is the length of the document d in words or tokens.
        - avgdl is the average document length in the corpus.
        - N is the total number of documents in the corpus.
        - n(q_i) is the number of documents containing term q_i.

    References:
        [1] https://en.wikipedia.org/wiki/Okapi_BM25
        [2] https://github.com/dorianbrown/rank_bm25
        [3] Improvements to BM25 and Language Models Examined: https://www.cs.otago.ac.nz/homepages/andrew/papers/2014-2.pdf

    Args:
        top_k : (int): The number of documents to return
        k1 : (float, optional): Constant used for influencing the term frequency saturation. After saturation is reached, additional
                presence for the term adds a significantly less additional score. According to [1]_, experiments suggest
                that 1.2 < k1 < 2 yields reasonably good results, although the optimal value depends on factors such as
                the type of documents or queries.
        b : (float, optional): Constant used for influencing the effects of different document lengths relative to average document length.
                When b is bigger, lengthier documents (compared to average) have more impact on its effect. According to
                [1]_, experiments suggest that 0.5 < b < 0.8 yields reasonably good results, although the optimal value
                depends on factors such as the type of documents or queries.
        epsilon: (float, optional): Used to adapt the negative idf score to epilon * average_idf. Default is 0.25

        documents: (List[Any], optional): The list of documents to build the index from. Default is None.
        document_map_func: (Callable, optional): The function to transform the document into `List[str]`.
            You don't need it if your documents are already in format `List[str]`.
        use_tokenizer: (bool, optional): Whether to use the default tokenizer to split the text into words. Default is True.

    Examples:

    .. code-block:: python

            from adalflow.components.retriever.bm25_retriever import BM25Retriever

            documents = ["hello world", "world is beautiful", "today is a good day"]

    1. Pass the documents from the __init__ method:

    .. code-block:: python

            retriever = BM25Retriever(top_k=1, documents=documents)
            output = retriever("hello")
            print(output)
            # Output:
            # [RetrieverOutput(doc_indices=[0], doc_scores=[0.6229580777634034], query=None, documents=None)]

    2. Pass the documents from the :meth:`build_index_from_documents` method:

    .. code-block:: python
            retriever = BM25Retriever(top_k=1)
            retriever.build_index_from_documents(documents)
            output = retriever("hello")

    3. Save the index to file and load it back:

    .. code-block:: python

            retriever.save_to_file("bm25_index.json")
            retriever2 = BM25Retriever.load_from_file("bm25_index.json")
            output = retriever2("hello")
            print(output)

    note:
    The retriever only fill in the ``doc_indices`` and ``doc_scores``. The ``documents`` needs to be filled in by the user.
    """

    def __init__(
        self,
        top_k: int = 5,
        k1: float = PARAM_K1,
        b: float = PARAM_B,
        epsilon: float = PARAM_EPSILON,
        documents: Sequence[Any] | None = None,
        document_map_func: Callable[[Any], str] | None = None,
        use_tokenizer: bool = True,
    ):
        r"""
        - nd: <token, freq> (n(q_i) in the formula)
        - t2d: <token, <doc_index, freq>> (f(q_i, d) in the formula)
        - idf: <token, idf> (idf(q_i) in the formula)
        - doc_len: list of document lengths (|d| in the formula)
        - avgdl: average document length in the corpus (avgdl in the formula)
        - total_documents: total number of documents in the corpus (N in the formula)
        """
        super().__init__()
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        self.top_k = top_k
        self._use_tokenizer = use_tokenizer
        self._split_function = (
            split_text_by_word_fn_then_lower_tokenized
            if use_tokenizer
            else split_text_by_word_fn
        )
        self.indexed = False  # this is important to check if the retrieve is possible
        self.index_keys = [
            "nd",
            "t2d",
            "idf",
            "doc_len",
            "avgdl",
            "total_documents",
            "top_k",
            "k1",
            "b",
            "epsilon",
            "indexed",
            "use_tokenizer",
        ]
        # initialize the index
        self.reset_index()
        self.documents = documents
        if documents:
            self.build_index_from_documents(documents, document_map_func)

    def reset_index(self):
        r"""Used for both initializing and resetting the index."""
        self.t2d: list[dict[str, int]] = []  # term freuqency in each document
        self.nd: dict[str, int] = {}  # number of documents containing the term
        self.idf: dict[str, float] = {}  # idf of each term
        self.doc_len: list[int] = []  # list of document lengths
        self.avgdl: float = 0  # average document length
        self.indexed: bool = (
            False  # this is important to check if the retrieve is possible
        )
        self.total_documents: int = 0
        self._inverted_index: dict[str, Any] | None = None
        self._doc_len_norm: np.ndarray | None = None

    def _build_inverted_index(self):
        """Construct inverted index and document length normalization factors for fast scoring."""
        inverted: dict[str, Any] = {}
        for doc_id, doc in enumerate(self.t2d):
            for term, freq in doc.items():
                if term not in inverted:
                    inverted[term] = ([], [])
                inverted[term][0].append(doc_id)
                inverted[term][1].append(float(freq))

        self._inverted_index = {
            term: (
                np.array(doc_ids, dtype=np.int32),
                np.array(freqs, dtype=np.float64),
            )
            for term, (doc_ids, freqs) in inverted.items()
        }
        if self.avgdl > 0 and self.total_documents > 0:
            doc_len = np.array(self.doc_len, dtype=np.float64)
            self._doc_len_norm = self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
        else:
            self._doc_len_norm = np.zeros(self.total_documents, dtype=np.float64)

    def _apply_split_function(self, documents: list[str]):
        if self._split_function is None:
            raise ValueError("split_function is not defined")
        if not documents:
            log.warning("No documents to split")
            return
        tokenized_documents = [self._split_function(doc) for doc in documents]

        return tokenized_documents

    def _initialize(self, corpus: list[list[str]]):
        r"""Initialize the term to document dictionary with the term frequencies in each document.
        The corpi is a list of tokenized documents."""

        self.total_documents = len(corpus)

        for document in corpus:
            self.doc_len.append(len(document))
            term_freq = {}
            for token in document:
                if token not in term_freq:
                    term_freq[token] = 0
                term_freq[token] += 1

            self.t2d.append(term_freq)

            for word, _ in term_freq.items():
                if word not in self.nd:
                    self.nd[word] = 0
                self.nd[word] += 1

        self.avgdl = sum(self.doc_len) / len(corpus)

    def _calc_idf(self):
        idf_sum = 0
        negative_idf = (
            []
        )  # idf can be negative if word is too common: more than half of the documents
        self.idf: dict[str, float] = {}
        for token, freq in self.nd.items():
            idf = math.log(self.total_documents - freq + 0.5) - math.log(freq + 0.5)
            self.idf[token] = idf
            idf_sum += idf
            if idf < 0:
                negative_idf.append(token)
        self.average_idf = idf_sum / len(self.nd)  # average idf for each term

        # replace negative idf with epsilon * average_idf
        # NOTE: we can still have negative idf if most terms are too common, especially when the corpus is small
        eps = self.epsilon * self.average_idf
        for token in negative_idf:
            self.idf[token] = eps

        self._build_inverted_index()

    def _get_scores(self, query: list[str]) -> list[float]:
        r"""Calculate the BM25 score for the query and the documents in the corpus

        Args:
            query: List[str]: The tokenized query
        """
        if self._inverted_index is None and self.indexed:
            self._build_inverted_index()

        if self._inverted_index is None or self.total_documents == 0:
            return [0.0] * self.total_documents

        score = np.zeros(self.total_documents)
        for q in query:
            if q in self._inverted_index:
                doc_ids, q_freq = self._inverted_index[q]
                idf = self.idf.get(q, 0.0)
                if idf != 0 and self._doc_len_norm is not None:
                    denom = q_freq + self._doc_len_norm[doc_ids]
                    score[doc_ids] += idf * (q_freq * (self.k1 + 1)) / denom
        return score.tolist()

    def _get_batch_scores(self, query: list[str], doc_ids: list[int]) -> list[float]:
        r"""Calculate the BM25 score for the query and the documents in the corpus

        Args:
            query: List[str]: The tokenized query
            doc_ids: List[int]: The list of document indexes to calculate the score
        """
        assert all(di < len(self.t2d) for di in doc_ids)
        if self._inverted_index is None and self.indexed:
            self._build_inverted_index()

        doc_ids_arr = np.array(doc_ids, dtype=np.int32)
        score = np.zeros(len(doc_ids))
        for q in query:
            idf = self.idf.get(q, 0.0)
            if idf != 0 and self._inverted_index and q in self._inverted_index and self._doc_len_norm is not None:
                q_freq = np.array([self.t2d[di].get(q, 0) for di in doc_ids], dtype=np.float64)
                denom = q_freq + self._doc_len_norm[doc_ids_arr]
                nonzero_mask = q_freq > 0
                if np.any(nonzero_mask):
                    score[nonzero_mask] += idf * (
                        q_freq[nonzero_mask] * (self.k1 + 1)
                    ) / denom[nonzero_mask]
        return score.tolist()

    def build_index_from_documents(
        self,
        documents: RetrieverDocumentsType,
        document_map_func: Callable[[Any], str] | None = None,
        **kwargs,
    ):
        r"""Built index from the `text` field of each document in the list of documents"""
        assert documents, "documents should not be empty"
        self.reset_index()
        self.documents = documents
        # the documents to be indexed
        if document_map_func:
            assert callable(document_map_func), "document_map_func should be callable"
            assert isinstance(
                document_map_func(documents[0]), str
            ), "document_map_func should return a string"
            list_of_documents_str = [document_map_func(doc) for doc in documents]
        else:
            list_of_documents_str = documents

        self.tokenized_documents = self._apply_split_function(list_of_documents_str)
        self._initialize(self.tokenized_documents)
        self._calc_idf()
        self.indexed = True

    def call(
        self, input: RetrieverStrQueriesType, top_k: int | None = None, **kwargs
    ) -> RetrieverOutputType:
        """
        Retrieve the top n documents for the query and return only the indexes of the documents.

        Args:
            input: Union[str, List[str]]: The query or list of queries
            top_k: Optional[int]: The number of documents to return
        """
        if not self.indexed:
            raise ValueError("Index is not built. Please build the index first.")

        top_k = top_k or self.top_k
        output: RetrieverOutputType = []
        if isinstance(input, str):
            input = [input]
        elif isinstance(input, list):
            pass
        else:
            raise ValueError("input should be a string or a list of strings")
        # process each query
        for query in input:
            tokens = self._split_function(query)
            scores = self._get_scores(tokens)
            top_k_idx = heapq.nlargest(top_k, range(len(scores)), scores.__getitem__)
            top_k_scores = [scores[i] for i in top_k_idx]
            output.append(
                RetrieverOutput(
                    doc_indices=top_k_idx, doc_scores=top_k_scores, query=query
                )
            )
        return output

    def save_to_file(self, path: str):
        index_dict = super().to_dict()
        # filter out index_dict[data] that is not in self.index_keys
        for key in list(index_dict["data"].keys()):
            if key not in self.index_keys:
                del index_dict["data"][key]
        try:
            save_json(index_dict, path)
        except Exception as e:
            log.error(f"Error saving the index to file: {e}")
            raise e

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BM25Retriever":
        instance = super().from_dict(data)
        Component.__init__(instance)
        instance.reset_index()
        for key, value in data.get("data", {}).items():
            setattr(instance, key, cls._restore_value(value))
        return instance

    @classmethod
    def load_from_file(cls, path: str):
        # create an instance of the class
        try:
            index_dict = load_standard_json(path)
            instance = cls.from_dict(index_dict)
            use_tok = getattr(instance, "use_tokenizer", getattr(instance, "_use_tokenizer", True))
            instance._use_tokenizer = use_tok
            # add the split function
            instance._split_function = (
                split_text_by_word_fn_then_lower_tokenized
                if use_tok
                else split_text_by_word_fn
            )
            return instance
        except Exception as e:
            log.error(f"Error loading the index from file: {e}")
            raise e

    def _extra_repr(self) -> str:
        s = f"top_k={self.top_k}, k1={self.k1}, b={self.b}, epsilon={self.epsilon}, use_tokenizer={self._use_tokenizer}"
        s += f", total_documents={self.total_documents}"
        return s
