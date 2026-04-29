from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from database.connection import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    amount = Column(Float)
    merchant = Column(String)
    location = Column(String)
    card_last_four = Column(String)
    timestamp = Column(DateTime, default=func.now())
    
    # Risk scores
    risk_score = Column(Float, default=0.0)
    is_fraud = Column(Boolean, default=False)
    
    # Model scores
    isolation_forest_score = Column(Float, default=0.0)
    autoencoder_score = Column(Float, default=0.0)
    xgboost_score = Column(Float, default=0.0)
    
    # Explanation
    fraud_reason = Column(Text, nullable=True)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, index=True)
    risk_score = Column(Float)
    alert_type = Column(String)
    message = Column(Text)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())