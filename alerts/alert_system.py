from datetime import datetime
from alerts.risk_scorer import RiskScorer

class AlertSystem:
    def __init__(self):
        self.risk_scorer = RiskScorer()
        self.alerts = []

    def process_transaction(self, transaction: dict, ensemble_scores: dict) -> dict:
        # Get risk analysis
        risk_analysis = self.risk_scorer.analyze(ensemble_scores, features=transaction.get("features", []))
        
        result = {
            "transaction_id": transaction.get("transaction_id"),
            "amount": transaction.get("amount"),
            "timestamp": datetime.now().isoformat(),
            "risk_score": risk_analysis["risk_score"],
            "risk_level": risk_analysis["risk_level"],
            "is_fraud": risk_analysis["is_fraud"],
            "model_scores": risk_analysis["model_scores"],
            "alert": None
        }

        # Create alert if fraud detected
        if risk_analysis["is_fraud"]:
            alert = self.create_alert(transaction, risk_analysis)
            result["alert"] = alert
            self.alerts.append(alert)
            print(f"🚨 FRAUD ALERT: Transaction {transaction.get('transaction_id')} "
                  f"Risk Score: {risk_analysis['risk_score']}/100")
        else:
            print(f"✅ SAFE: Transaction {transaction.get('transaction_id')} "
                  f"Risk Score: {risk_analysis['risk_score']}/100")

        return result

    def create_alert(self, transaction: dict, risk_analysis: dict) -> dict:
        return {
            "alert_id": f"ALT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "transaction_id": transaction.get("transaction_id"),
            "amount": transaction.get("amount"),
            "risk_score": risk_analysis["risk_score"],
            "risk_level": risk_analysis["risk_level"],
            "model_scores": risk_analysis["model_scores"],
            "timestamp": datetime.now().isoformat(),
            "status": "OPEN"
        }

    def get_alerts(self) -> list:
        return self.alerts

    def get_stats(self) -> dict:
        total = len(self.alerts)
        critical = sum(1 for a in self.alerts if a["risk_level"] == "CRITICAL")
        high = sum(1 for a in self.alerts if a["risk_level"] == "HIGH")
        return {
            "total_alerts": total,
            "critical": critical,
            "high": high,
            "total_amount_blocked": sum(a["amount"] for a in self.alerts)
        }