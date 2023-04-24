# embeddings.py
from typing import List, Tuple, Union
import numpy as np
import pandas as pd
import pickle
import random
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

from openai.embeddings_utils import get_embedding, cosine_similarity


class CustomEmbeddings:
    def __init__(
        self,
        df: pd.DataFrame,
        process_input_data_func: callable,
        embedding_cache_path: str = "embedding_cache.pkl",
        default_embedding_engine: str = "babbage-similarity",
        test_fraction: float = 0.5,
        random_seed: int = 123,
    ):
        self.df = df
        self.process_input_data_func = process_input_data_func
        self.embedding_cache_path = embedding_cache_path
        self.default_embedding_engine = default_embedding_engine
        self.test_fraction = test_fraction
        self.random_seed = random_seed
        self.train_df = None
        self.test_df = None
        self.embedding_cache = {}

    def load_and_process_data(self):
        self.df = self.process_input_data_func(self.df)

    def split_data(self):
        self.train_df, self.test_df = train_test_split(
            self.df,
            test_size=self.test_fraction,
            stratify=self.df["label"],
            random_state=self.random_seed,
        )

    def load_embedding_cache(self):
        try:
            with open(self.embedding_cache_path, "rb") as f:
                self.embedding_cache = pickle.load(f)
        except FileNotFoundError:
            print("Embedding cache not found.")

    def save_embedding_cache(self):
        with open(self.embedding_cache_path, "wb") as embedding_cache_file:
            pickle.dump(self.embedding_cache, embedding_cache_file)

    def get_embedding_with_cache(
        self,
        text: str,
        engine: str = None,
    ) -> Union[np.ndarray, List[float]]:
        if engine is None:
            engine = self.default_embedding_engine

        if (text, engine) not in self.embedding_cache.keys():
            self.embedding_cache[(text, engine)] = get_embedding(text, engine)
            self.save_embedding_cache()

        return self.embedding_cache[(text, engine)]

    def compute_embeddings(self):
        for column in ["text_1", "text_2"]:
            self.df[f"{column}_embedding"] = self.df[column].apply(
                self.get_embedding_with_cache
            )

    def compute_cosine_similarities(self):
        self.df["cosine_similarity"] = self.df.apply(
            lambda row: cosine_similarity(
                row["text_1_embedding"], row["text_2_embedding"]
            ),
            axis=1,
        )

    def process_and_compute(self):
        self.load_and_process_data()
        self.split_data()
        self.load_embedding_cache()
        self.compute_embeddings()
        self.compute_cosine_similarities()

    # Other methods for generating synthetic negatives and optimizing the matrix should be added here.
