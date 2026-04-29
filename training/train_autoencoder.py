import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from models.autoencoder import FraudAutoEncoder
import os

def load_data():
    path = "data/raw/transactions.csv"
    if not os.path.exists(path):
        print("❌ Dataset not found!")
        print("Download from: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
        return None, None
    
    print("Loading data...")
    df = pd.read_csv(path)
    X = df.drop(["Time", "Class"], axis=1).values
    y = df["Class"].values
    return X, y

def main():
    X, y = load_data()
    if X is None:
        return

    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train only on normal transactions
    X_normal = X_scaled[y == 0]
    print(f"Training on {len(X_normal)} normal transactions")

    # Train model
    model = FraudAutoEncoder(input_dim=X.shape[1])
    model.train(X_normal, epochs=50)

    # Evaluate
    scores = model.predict(X_scaled)
    from sklearn.metrics import roc_auc_score
    auc = roc_auc_score(y, scores)
    print(f"✅ ROC-AUC Score: {auc:.4f}")

    # Save
    model.save()
    print("✅ AutoEncoder training complete!")

if __name__ == "__main__":
    main()