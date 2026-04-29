from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionInput(BaseModel):
    transaction_id: Optional[str] = None
    amount: float
    merchant: str = "Unknown"
    location: str = "Unknown"

class TransactionResponse(BaseModel):
    transaction_id: str
    amount: float
    risk_score: float
    risk_level: str
    is_fraud: bool
    model_scores: dict
    timestamp: str
    alert: Optional[dict] = None