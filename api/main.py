from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import transactions, alerts

app = FastAPI(
    title="FraudShield AI",
    description="Real-time fraud detection API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])

@app.get("/")
def root():
    return {"message": "FraudShield AI is running! 🛡️"}

@app.get("/health")
def health():
    return {"status": "healthy"}