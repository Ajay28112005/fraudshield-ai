import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
import joblib
import os

class FraudXGBoost:
    def __init__(self):
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            scale_pos_weight=100,
            random_state=42,
            eval_metric="auc",
            use_label_encoder=False
        )
        self.scaler = StandardScaler()
        self.is_trained = False

    def train(self, X_train, y_train, X_val=None, y_val=None):
        print("Training XGBoost...")
        X_scaled = self.scaler.fit_transform(X_train)

        eval_set = None
        if X_val is not None:
            X_val_scaled = self.scaler.transform(X_val)
            eval_set = [(X_val_scaled, y_val)]

        self.model.fit(
            X_scaled, y_train,
            eval_set=eval_set,
            verbose=10
        )
        self.is_trained = True
        print("✅ XGBoost trained!")

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        proba = self.model.predict_proba(X_scaled)[:, 1]
        return proba

    def save(self, path="saved_models/xgboost.pkl"):
        os.makedirs("saved_models", exist_ok=True)
        joblib.dump({
            "model": self.model,
            "scaler": self.scaler
        }, path)
        print(f"✅ XGBoost saved to {path}")

    def load(self, path="saved_models/xgboost.pkl"):
        data = joblib.load(path)
        self.model = data["model"]
        self.scaler = data["scaler"]
        self.is_trained = True
        print(f"✅ XGBoost loaded from {path}")