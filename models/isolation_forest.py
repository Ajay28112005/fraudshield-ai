import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

class FraudIsolationForest:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.02,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False

    def preprocess(self, X):
        return self.scaler.transform(X)

    def train(self, X_train):
        print("Training Isolation Forest...")
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled)
        self.is_trained = True
        print("✅ Isolation Forest trained!")

    def predict(self, X):
        X_scaled = self.preprocess(X)
        scores = self.model.decision_function(X_scaled)
        # Convert to 0-1 probability (higher = more fraudulent)
        normalized = 1 - (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)
        return normalized

    def save(self, path="saved_models/isolation_forest.pkl"):
        os.makedirs("saved_models", exist_ok=True)
        joblib.dump({"model": self.model, "scaler": self.scaler}, path)
        print(f"✅ Model saved to {path}")

    def load(self, path="saved_models/isolation_forest.pkl"):
        data = joblib.load(path)
        self.model = data["model"]
        self.scaler = data["scaler"]
        self.is_trained = True
        print(f"✅ Model loaded from {path}")