import torch
import torch.nn as nn
import numpy as np
import os

class AutoEncoder(nn.Module):
    def __init__(self, input_dim=29):
        super(AutoEncoder, self).__init__()
        
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4)
        )
        
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


class FraudAutoEncoder:
    def __init__(self, input_dim=29):
        self.device = torch.device("cpu")
        self.model = AutoEncoder(input_dim).to(self.device)
        self.threshold = None
        self.is_trained = False

    def train(self, X_train, epochs=50, batch_size=256):
        print("Training AutoEncoder...")
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        criterion = nn.MSELoss()
        
        X_tensor = torch.FloatTensor(X_train).to(self.device)
        
        for epoch in range(epochs):
            self.model.train()
            optimizer.zero_grad()
            output = self.model(X_tensor)
            loss = criterion(output, X_tensor)
            loss.backward()
            optimizer.step()
            
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.6f}")
        
        # Set threshold from training errors
        self.model.eval()
        with torch.no_grad():
            output = self.model(X_tensor)
            errors = torch.mean((output - X_tensor) ** 2, dim=1)
            self.threshold = float(errors.mean() + 2 * errors.std())
        
        self.is_trained = True
        print("✅ AutoEncoder trained!")

    def predict(self, X):
        self.model.eval()
        X_tensor = torch.FloatTensor(X).to(self.device)
        with torch.no_grad():
            output = self.model(X_tensor)
            errors = torch.mean((output - X_tensor) ** 2, dim=1)
        return errors.numpy()

    def save(self, path="saved_models/autoencoder.pth"):
        os.makedirs("saved_models", exist_ok=True)
        torch.save({
            "model_state": self.model.state_dict(),
            "threshold": self.threshold
        }, path)
        print(f"✅ AutoEncoder saved to {path}")

    def load(self, path="saved_models/autoencoder.pth"):
        data = torch.load(path, map_location=self.device)
        self.model.load_state_dict(data["model_state"])
        self.threshold = data["threshold"]
        self.is_trained = True
        print(f"✅ AutoEncoder loaded from {path}")