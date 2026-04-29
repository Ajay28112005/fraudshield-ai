import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from models.isolation_forest import FraudIsolationForest
import os

def load_data():
    path = "data/raw/transactions.csv"
    if not os.path.exists(path):
        print("❌ Dataset not found!")
        print("Download from: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
        print("Save as: data/raw/transactions.csv")
        return None, None
    
    print("Loading data...")
    df = pd.read_csv(path)
    print(f"✅ Loaded {len(df)} transactions")
    print(f"Fraud cases: {df['Class'].sum()} ({df['Class'].mean()*100:.2f}%)")
    
    # Features (drop Time and Class label)
    X = df.drop(["Time", "Class"], axis=1).values
    y = df["Class"].values
    return X, y

def main():
    X, y = load_data()
    if X is None:
        return
    
    # Use only normal transactions for training
    X_normal = X[y == 0]
    print(f"Training on {len(X_normal)} normal transactions")
    
    # Train model
    model = FraudIsolationForest()
    model.train(X_normal)
    
    # Test on full dataset
    scores = model.predict(X)
    
    # Evaluate
    from sklearn.metrics import roc_auc_score
    auc = roc_auc_score(y, scores)
    print(f"✅ ROC-AUC Score: {auc:.4f}")
    
    # Save model
    model.save()
    print("✅ Isolation Forest training complete!")

if __name__ == "__main__":
    main()