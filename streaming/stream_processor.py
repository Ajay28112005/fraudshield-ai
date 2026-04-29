from alerts.alert_system import AlertSystem
from alerts.risk_scorer import RiskScorer
from explainability.claude_explainer import ClaudeExplainer

class StreamProcessor:
    def __init__(self, use_claude=False):
        self.risk_scorer = RiskScorer()
        self.alerts = []
        self.processed = 0
        self.fraud_count = 0
        self.use_claude = use_claude
        self.alert_system = AlertSystem()
        if use_claude:
            self.explainer = ClaudeExplainer()

    def process_transaction(self, transaction: dict, ensemble_scores: dict = None) -> dict:
        risk_analysis = self.risk_scorer.analyze(
            ensemble_scores or {},
            features=transaction.get("features", [])
        )

        result = {
            "transaction_id": transaction.get("transaction_id"),
            "amount": transaction.get("amount"),
            "timestamp": transaction.get("timestamp"),
            "risk_score": risk_analysis["risk_score"],
            "risk_level": risk_analysis["risk_level"],
            "is_fraud": risk_analysis["is_fraud"],
            "model_scores": risk_analysis["model_scores"],
            "alert": None
        }

        # Add Claude explanation if fraud
        if result["is_fraud"] and self.use_claude:
            explanation = self.explainer.explain_fraud(
                transaction, result
            )
            result["explanation"] = explanation

        self.processed += 1

        # Create alert if fraud detected
        if risk_analysis["is_fraud"]:
            self.fraud_count += 1
            alert = {
                "transaction_id": result["transaction_id"],
                "amount": result["amount"],
                "timestamp": result["timestamp"],
                "risk_score": result["risk_score"],
                "risk_level": result["risk_level"],
                "status": "OPEN"
            }
            self.alert_system.alerts.append(alert)
            result["alert"] = alert

        return result

    def process_batch(self, transactions: list) -> list:
        results = []
        for transaction in transactions:
            result = self.process_transaction(transaction)
            results.append(result)
        return results

    def get_alerts(self) -> list:
        return self.alert_system.alerts

    def get_stats(self) -> dict:
        alert_stats = self.alert_system.get_stats()
        return {
            "total_processed": self.processed,
            "fraud_detected": self.fraud_count,
            "fraud_rate": round(
                self.fraud_count / max(self.processed, 1) * 100, 2
            ),
            "total_alerts": alert_stats["total_alerts"],
            "amount_blocked": alert_stats["total_amount_blocked"]
        }