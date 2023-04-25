import numpy as np
import pandas as pd
import pickle
import random
from typing import List, Tuple
import torch
from sklearn.model_selection import train_test_split
from openai.embeddings_utils import get_embedding, cosine_similarity

class EmbeddingsOptimizer:
    def __init__(
        self,
        local_dataset_path: str,
        embedding_cache_path: str,
        default_embedding_engine: str,
        num_pairs_to_embed: int,
        test_fraction: float,
        random_seed: int,
        negatives_per_positive: int,
        modified_embedding_length: int,
        batch_size: int,
        max_epochs: int,
        learning_rate: float,
        dropout_fraction: float,
    ):
        self.local_dataset_path = local_dataset_path
        self.embedding_cache_path = embedding_cache_path
        self.default_embedding_engine = default_embedding_engine
        self.num_pairs_to_embed = num_pairs_to_embed
        self.test_fraction = test_fraction
        self.random_seed = random_seed
        self.negatives_per_positive = negatives_per_positive
        self.modified_embedding_length = modified_embedding_length
        self.batch_size = batch_size
        self.max_epochs = max_epochs
        self.learning_rate = learning_rate
        self.dropout_fraction = dropout_fraction

    def process_input_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # Customize this function to preprocess your own dataset
        # output should be a dataframe with 3 columns: text_1, text_2, label (1 for similar, -1 for dissimilar)
        df["label"] = df["gold_label"]
        df = df[df["label"].isin(["entailment"])]
        df["label"] = df["label"].apply(lambda x: {"entailment": 1, "contradiction": -1}[x])
        df = df.rename(columns={"sentence1": "text_1", "sentence2": "text_2"})
        df = df[["text_1", "text_2", "label"]]
        df = df.head(self.num_pairs_to_embed)
        return df

    def load_and_process_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.local_dataset_path)
        df = self.process_input_data(df)
        return df

    def split_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        train_df, test_df = train_test_split(
            df,
            test_size=self.test_fraction,
            stratify=df["label"],
            random_state=self.random_seed,
        )
        train_df.loc[:, "dataset"] = "train"
        test_df.loc[:, "dataset"] = "test"
        return train_df, test_df

    def dataframe_of_negatives(self, dataframe_of_positives: pd.DataFrame) -> pd.DataFrame:
        texts = set(dataframe_of_positives["text_1"].values) | set(
            dataframe_of_positives["text_2"].values
        )
        all_pairs = {(t1, t2) for t1 in texts for t2 in texts if t1 < t2}
        positive_pairs = set(
            tuple(text_pair)
            for text_pair in dataframe_of_positives[["text_1", "text_2"]].values
        )
        negative_pairs = all_pairs - positive_pairs
        df_of_negatives = pd.DataFrame(list(negative_pairs), columns=["text_
