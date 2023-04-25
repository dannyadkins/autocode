import os
import pickle
from typing import List, Any, Tuple
import numpy as np
import openai
from tqdm import tqdm

from retrieve import Embedding, retrieve_embeddings
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

def load_embed_store(store_key: str) -> Tuple[np.ndarray, List[Any]]:
    embeddings_path = f"data/embeddings/{store_key}_embeddings.npy"
    documents_path = f"data/embeddings/{store_key}_documents.pkl"

    if os.path.exists(embeddings_path) and os.path.exists(documents_path):
        embeddings = np.load(embeddings_path)
        with open(documents_path, "rb") as f:
            documents = pickle.load(f)
        return embeddings, documents
    else:
        raise FileNotFoundError(f"Embeddings or documents not found for store key: {store_key}")


def save_embed_store(store_key: str, embeddings: np.ndarray, documents: List[Any]):
    os.makedirs("embeddings", exist_ok=True)
    embeddings_path = f"data/embeddings/{store_key}_embeddings.npy"
    documents_path = f"data/embeddings/{store_key}_documents.pkl"

    np.save(embeddings_path, embeddings)
    with open(documents_path, "wb") as f:
        pickle.dump(documents, f)


def embed_documents(texts: List[str], model: str = "text-embedding-ada-002") -> np.ndarray:
    texts = [text.replace("\n", " ") for text in texts]
    response = openai.Embedding.create(input=texts, model=model)
    return np.array([embedding_data['embedding'] for embedding_data in response['data']])


def build_embedding_store(documents: List[Any], store_key: str, model: str = "text-embedding-ada-002"):
    embeddings = embed_documents(documents, model)
    save_embed_store(store_key, embeddings, documents)


def main():
    # Example usage
    documents = [
        "The quick brown fox jumps over the lazy dog",
        "I love artificial intelligence and natural language processing",
        "Deep learning is a powerful technique for solving complex problems",
        "DEEP LEARN SO COOL YEAH"
    ]

    store_key = "example"
    build_embedding_store(documents, store_key)

    embeddings, documents = load_embed_store(store_key)
    query = "What is deep learning?"
    query_embedding = embed_documents([query])  # Make sure it's a 1D array
    
    num_docs = 3
    retrieved_docs = retrieve_embeddings(query_embedding, embeddings, documents, num_docs, method='knn')
    print("Retrieved documents:")
    for doc in retrieved_docs:
        print(doc.document)


if __name__ == "__main__":
    main()