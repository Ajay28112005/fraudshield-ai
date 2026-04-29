import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class ClaudeExplainer:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def explain_fraud(self, transaction: dict, risk_analysis: dict) -> str:
        prompt = f"""You are a fraud detection expert. Analyze this flagged transaction and explain why it was flagged in simple, clear language.

Transaction Details:
- Amount: ${transaction.get('amount', 0):.2f}
- Merchant: {transaction.get('merchant', 'Unknown')}
- Location: {transaction.get('location', 'Unknown')}
- Time: {transaction.get('timestamp', 'Unknown')}

Risk Analysis:
- Overall Risk Score: {risk_analysis['risk_score']}/100
- Risk Level: {risk_analysis['risk_level']}
- Isolation Forest Score: {risk_analysis['model_scores']['isolation_forest']}/100
- AutoEncoder Score: {risk_analysis['model_scores']['autoencoder']}/100
- XGBoost Score: {risk_analysis['model_scores']['xgboost']}/100

Provide a brief 2-3 sentence explanation of why this transaction was flagged as potentially fraudulent. Be specific and mention the key risk factors."""

        message = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def explain_safe(self, transaction: dict, risk_analysis: dict) -> str:
        return f"Transaction of ${transaction.get('amount', 0):.2f} appears normal with a low risk score of {risk_analysis['risk_score']}/100."