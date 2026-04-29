from fastapi import APIRouter
from api.schemas.transaction import TransactionInput, TransactionResponse
from streaming.stream_processor import StreamProcessor
from streaming.transaction_simulator import TransactionSimulator
from data.loader import get_real_transactions
import uuid

router = APIRouter()

# Initialize processor once
processor = StreamProcessor(use_claude=False)
simulator = TransactionSimulator()

@router.post("/process")
def process_transaction(transaction: TransactionInput):
    t_dict = transaction.dict()
    # Process through ML pipeline
    result = processor.process_transaction(t_dict)
    return result

@router.get("/simulate")
def simulate_transactions(n: int = 10, fraud_rate: float = 0.2):
    try:
        # Use real Kaggle data
        transactions = get_real_transactions(n=n, fraud_rate=fraud_rate)
    except Exception as e:
        # Fallback to simulator if CSV not available
        print(f"Kaggle data error: {e}, falling back to simulator")
        transactions = simulator.generate_stream(n=n, fraud_rate=fraud_rate)

    results = processor.process_batch(transactions)
    return {
        "transactions": results,
        "stats": processor.get_stats()
    }

@router.get("/stats")
def get_stats():
    return processor.get_stats()

@router.get("/alerts")
def get_alerts():
    return {"alerts": processor.get_alerts()}