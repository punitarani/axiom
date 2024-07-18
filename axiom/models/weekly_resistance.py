"""axiom/models/weekly_resistance.py"""

import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor


class WeeklyResistanceModel:
    def __init__(self, ticker: str):
        self.ticker: str = ticker
        self.high_pipeline: Pipeline | None = None
        self.low_pipeline: Pipeline | None = None

    def train(
        self,
        high_features: np.ndarray,
        high_targets: np.ndarray,
        low_features: np.ndarray,
        low_targets: np.ndarray,
    ):
        # High Model Training
        high_train_features, high_test_features, high_train_targets, high_test_targets = (
            train_test_split(high_features, high_targets, test_size=0.75, random_state=42)
        )

        high_pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("xgb", XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)),
            ]
        )

        high_pipeline.fit(high_train_features, high_train_targets)
        self.high_pipeline = high_pipeline

        # Low Model Training
        low_train_features, low_test_features, low_train_targets, low_test_targets = (
            train_test_split(low_features, low_targets, test_size=0.5, random_state=42)
        )

        low_pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("xgb", XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)),
            ]
        )

        low_pipeline.fit(low_train_features, low_train_targets)
        self.low_pipeline = low_pipeline

    def predict(self, highs: list[float], lows: list[float]) -> tuple[float, float]:
        highs = np.array(highs).reshape(1, -1)
        lows = np.array(lows).reshape(1, -1)

        next_week_high = self.high_pipeline.predict(highs)
        next_week_low = self.low_pipeline.predict(lows)

        return next_week_high[0], next_week_low[0]

    def save(self, high_pipeline_path: str, low_pipeline_path: str):
        joblib.dump(self.high_pipeline, high_pipeline_path)
        joblib.dump(self.low_pipeline, low_pipeline_path)

    @classmethod
    def load(
        cls, ticker: str, high_pipeline_path: str, low_pipeline_path: str
    ) -> "WeeklyResistanceModel":
        pipeline = cls(ticker)
        pipeline.high_pipeline = joblib.load(high_pipeline_path)
        pipeline.low_pipeline = joblib.load(low_pipeline_path)
        return pipeline
