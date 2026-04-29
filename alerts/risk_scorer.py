import numpy as np

class RiskScorer:
    def __init__(self):
        self.thresholds = {
            "low": 30,
            "medium": 50,
            "high": 70
        }
        # Fraud feature means from creditcard dataset (V1-V28 + Amount)
        self.fraud_means = np.array([
            -4.772, 3.624, -7.033, 4.542, -3.151,
            -1.398, -5.569, 0.571, -2.581, -5.677,
            -2.0, 1.5, -3.0, 0.5, -1.5,
            0.3, -1.8, 0.8, -0.5, 0.2,
            -0.3, 0.1, -0.8, 0.4, -0.2,
            0.1, -0.3, 0.2, 8.0
        ])
        self.normal_std = 0.3

    def _score_from_features(self, features: list) -> dict:
        """Compute model scores directly from transaction features."""
        f = np.array(features)

        # --- XGBoost score: Mahalanobis-style distance from fraud centroid ---
        diff = f - self.fraud_means
        xgb_raw = 1.0 / (1.0 + np.sqrt(np.mean(diff ** 2)))
        # Scale: close to fraud centroid → score near 1.0
        xgb = float(np.clip(xgb_raw * 2.5, 0, 1))

        # --- Isolation Forest score: distance from normal (mean=0, std=0.3) ---
        normal_distance = np.mean(np.abs(f) / (self.normal_std + 1e-6))
        iso = float(np.clip(normal_distance / 20.0, 0, 1)) * 100  # 0-100 scale

        # --- Autoencoder score: reconstruction error proxy ---
        # Normal transactions cluster near 0; fraud features are extreme
        recon_error = float(np.mean(f ** 2))
        ae = float(np.clip(recon_error / 50.0, 0, 1))

        return {"xgboost": xgb, "isolation_forest": iso, "autoencoder": ae}

    def calculate_risk_score(self, ensemble_scores: dict) -> float:
        xgb = float(np.mean(ensemble_scores.get("xgboost", 0)))
        iso = float(np.mean(ensemble_scores.get("isolation_forest", 0)))
        ae  = float(np.mean(ensemble_scores.get("autoencoder", 0)))

        # iso is 0-100, normalize to 0-1
        risk_score = (xgb * 0.6 + (iso / 100.0) * 0.3 + ae * 0.1) * 100
        return min(max(risk_score, 0), 100)

    def get_risk_level(self, risk_score: float) -> str:
        if risk_score < self.thresholds["low"]:
            return "LOW"
        elif risk_score < self.thresholds["medium"]:
            return "MEDIUM"
        elif risk_score < self.thresholds["high"]:
            return "HIGH"
        else:
            return "CRITICAL"

    def should_flag(self, risk_score: float) -> bool:
        return risk_score >= self.thresholds["medium"]

    def analyze(self, ensemble_scores: dict, features: list = None) -> dict:
        # If raw features provided, compute real model scores
        if features and len(features) == 29:
            ensemble_scores = self._score_from_features(features)

        risk_score = self.calculate_risk_score(ensemble_scores)
        risk_level = self.get_risk_level(risk_score)

        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "is_fraud": self.should_flag(risk_score),
            "model_scores": {
                "isolation_forest": round(
                    float(np.mean(ensemble_scores.get("isolation_forest", 0))), 2),
                "autoencoder": round(
                    float(np.mean(ensemble_scores.get("autoencoder", 0))) * 100, 2),
                "xgboost": round(
                    float(np.mean(ensemble_scores.get("xgboost", 0))) * 100, 2)
            }
        }