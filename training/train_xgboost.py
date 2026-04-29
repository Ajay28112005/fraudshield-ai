import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from models.xgboost_classifier import FraudXGBoost
import os

def load_data():
    path = "data/raw/transactions.csv"
    if not os.path.exists(path):
        print("❌ Dataset not found!")
        print("Download from: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
        return None, None, None, None

    print("Loading data...")
    df = pd.read_csv(path)
    X = df.drop(["Time", "Class"], axis=1).values
    y = df["Class"].values

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    return X_train, X_val, y_train, y_val

def main():
    X_train, X_val, y_train, y_val = load_data()
    if X_train is None:
        return

    print(f"Training: {len(X_train)} | Validation: {len(X_val)}")

    model = FraudXGBoost()
    model.train(X_train, y_train, X_val, y_val)

    # Evaluate
    scores = model.predict(X_val)
    from sklearn.metrics import roc_auc_score, classification_report
    auc = roc_auc_score(y_val, scores)
    preds = (scores > 0.5).astype(int)
    print(f"✅ ROC-AUC Score: {auc:.4f}")
    print(classification_report(y_val, preds))

    model.save()
    print("✅ XGBoost training complete!")

if __name__ == "__main__":
    main()