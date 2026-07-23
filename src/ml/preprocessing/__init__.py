from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


class Preprocessor:
    """Data preprocessing utilities."""

    def normalize(self, data: np.ndarray) -> np.ndarray:
        from sklearn.preprocessing import StandardScaler

        return StandardScaler().fit_transform(data)

    def minmax_scale(self, data: np.ndarray) -> np.ndarray:
        from sklearn.preprocessing import MinMaxScaler

        return MinMaxScaler().fit_transform(data)

    def encode_categorical(self, data: pd.Series) -> np.ndarray:
        from sklearn.preprocessing import LabelEncoder

        return LabelEncoder().fit_transform(data)

    def one_hot_encode(self, data: pd.Series) -> pd.DataFrame:
        return pd.get_dummies(data, prefix=data.name)

    def train_test_split(self, x, y, test_size=0.2, random_state=42):
        from sklearn.model_selection import train_test_split as tts

        return tts(x, y, test_size=test_size, random_state=random_state)


class FeatureScaler:
    """Feature scaling with fitted transformers."""

    def __init__(self):
        self.scalers: dict[str, Any] = {}

    def fit_transform(self, x: np.ndarray, name: str = "default") -> np.ndarray:
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        self.scalers[name] = scaler
        return scaler.fit_transform(x)

    def transform(self, x: np.ndarray, name: str = "default") -> np.ndarray:
        scaler = self.scalers.get(name)
        if scaler is None:
            raise ValueError(f"Scaler '{name}' not fitted")
        return scaler.transform(x)
