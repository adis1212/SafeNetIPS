# train_model.py
from sklearn.ensemble import IsolationForest
import numpy as np
import pickle

# Example: Replace this with your real training data
X_train = np.random.randn(100, 4)

model = IsolationForest(contamination=0.1)
model.fit(X_train)

with open('intrusion_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved as intrusion_model.pkl")
