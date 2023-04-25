"""" 

This files takes in an embedding store key and a query and a num_docs, looks up embedded docs under that key in the cache, and returns the closest docs and their embeddings.  

TODO: Eventually integrate Pinecone when its too much for local storage. 

"""
from typing import List, Tuple, Any
import numpy as np
from sklearn import svm
from dataclasses import dataclass


@dataclass
class Embedding:
    index: int
    value: np.ndarray
    document: Any  # Change this to the appropriate type of your document content


def normalize_embeddings(embeddings: np.ndarray) -> np.ndarray:
    return embeddings / np.sqrt((embeddings ** 2).sum(1, keepdims=True))


def knn_retrieval(query: np.ndarray, embeddings: np.ndarray, documents: List[Any], num_docs: int) -> List[Embedding]:
    similarities = embeddings.dot(query.T)
    similarities = similarities.flatten()
    sorted_ix = np.argsort(-similarities)
    
    result = []
    for k in sorted_ix[:num_docs]:
        result.append(Embedding(k, similarities[k], np.array(documents)[k]))
    
    return result


def svm_retrieval(query: np.ndarray, embeddings: np.ndarray, documents: List[Any], num_docs: int, c: float = 0.1) -> List[Embedding]:
    query = query.reshape(1, -1)  # Reshape the query to have a shape of (1, n)
    x = np.concatenate([query, embeddings])
    y = np.zeros(len(x))
    y[0] = 1

    clf = svm.LinearSVC(class_weight='balanced', verbose=False, max_iter=10000, tol=1e-6, C=c)
    clf.fit(x, y)

    similarities = clf.decision_function(x)[1:]
    sorted_ix = np.argsort(-similarities)
    
    result = []
    for k in sorted_ix[:num_docs]:
        result.append(Embedding(k, similarities[k], np.array(documents)[k]))

    return result

def retrieve_embeddings(query: np.ndarray, embeddings: np.ndarray, documents: List[Any], num_docs: int, method: str = 'svm', c: float = 0.1) -> List[Embedding]:
    normalized_query = normalize_embeddings(query[np.newaxis, :])[0]
    normalized_embeddings = normalize_embeddings(embeddings)

    if method == 'knn':
        return knn_retrieval(normalized_query, normalized_embeddings, documents, num_docs)
    elif method == 'svm':
        return svm_retrieval(normalized_query, normalized_embeddings, documents, num_docs, c)
    else:
        raise ValueError(f"Invalid retrieval method: {method}. Choose either 'knn' or 'svm'.")
