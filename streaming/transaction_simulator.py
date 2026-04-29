import random
import uuid
import numpy as np
from datetime import datetime

class TransactionSimulator:
    def __init__(self):
        self.merchants = [
            "Amazon", "Walmart", "Target", "Apple Store",
            "Gas Station", "Restaurant", "Hotel", "Airlines",
            "ATM Withdrawal", "Online Transfer"
        ]
        self.locations = [
            "New York", "Los Angeles", "Chicago", "Houston",
            "London", "Tokyo", "Dubai", "Unknown Location"
        ]

    def generate_normal(self) -> dict:
        return {
            "transaction_id": str(uuid.uuid4())[:8],
            "amount": round(random.uniform(5, 500), 2),
            "merchant": random.choice(self.merchants[:-2]),
            "location": random.choice(self.locations[:-1]),
            "timestamp": datetime.now().isoformat(),
            "hour": datetime.now().hour,
            "features": self._generate_features(is_fraud=False)
        }

    def generate_fraud(self) -> dict:
        return {
            "transaction_id": str(uuid.uuid4())[:8],
            "amount": round(random.uniform(3000, 15000), 2),
            "merchant": random.choice(["ATM Withdrawal", "Online Transfer"]),
            "location": "Unknown Location",
            "timestamp": datetime.now().isoformat(),
            "hour": random.choice([1, 2, 3, 4]),
            "features": self._generate_features(is_fraud=True)
        }

    def _generate_features(self, is_fraud: bool) -> list:
        if is_fraud:
            # Using REAL fraud feature means from creditcard dataset
            means = [-4.772, 3.624, -7.033, 4.542, -3.151,
                     -1.398, -5.569, 0.571, -2.581, -5.677,
                     -2.0, 1.5, -3.0, 0.5, -1.5,
                     0.3, -1.8, 0.8, -0.5, 0.2,
                     -0.3, 0.1, -0.8, 0.4, -0.2,
                     0.1, -0.3, 0.2, 8.0]
            features = [
                m + random.uniform(-0.5, 0.5)
                for m in means
            ]
        else:
            features = list(np.random.randn(29) * 0.3)
            features[28] = random.uniform(0, 2)

        return features

    def generate_stream(self, n=10, fraud_rate=0.2):
        transactions = []
        for _ in range(n):
            if random.random() < fraud_rate:
                transactions.append(self.generate_fraud())
            else:
                transactions.append(self.generate_normal())
        return transactions