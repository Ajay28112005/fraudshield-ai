import numpy as np
from models.isolation_forest import FraudIsolationForest
from models.autoencoder import FraudAutoEncoder
from models.xgboost_classifier import FraudXGBoost

class FraudEnsemble:
    def __init__(self):
        self.isolation_forest = FraudIsolationForest()
        self.autoencoder = FraudAutoEncoder()
        self.xgboost = FraudXGBoost()

        self.weights = {
            "isolation_forest": 0.20,
            "autoencoder": 0.10,
            "xgboost": 0.70
        }

    def load_all_models(self):
        self.isolation_forest.load()
        self.autoencoder.load()
        self.xgboost.load()
        print("✅ All models loaded!")

    def predict(self, X):
        # Get scores from each model
        if_score = self.isolation_forest.predict(X)
        ae_score = self.autoencoder.predict(X)
        xgb_score = self.xgboost.predict(X)

        # Normalize autoencoder to 0-1
        ae_min = ae_score.min()
        ae_max = ae_score.max()
        ae_normalized = (ae_score - ae_min) / (
            ae_max - ae_min + 1e-10
        )

        # XGBoost is the primary signal (70% weight)
        final_score = (
            self.weights["isolation_forest"] * if_score +
            self.weights["autoencoder"] * ae_normalized +
            self.weights["xgboost"] * xgb_score
        )

        return {
            "isolation_forest": if_score,
            "autoencoder": ae_normalized,
            "xgboost": xgb_score,
            "ensemble": final_score
        }

    def predict_single(self, x):
        X = np.array(x).reshape(1, -1)
        scores = self.predict(X)
        return {k: float(np.mean(v)) for k, v in scores.items()}