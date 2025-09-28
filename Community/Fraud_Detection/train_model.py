# train_model.py
import os, joblib, json
import pandas as pd
from sklearn.ensemble import IsolationForest
from utils.db import labeled_col
from dotenv import load_dotenv
load_dotenv()

MODEL_OUT = "model/isolation_forest_v1.joblib"

def load_training_data():
    # If you have labeled supervised data convert to features; for unsupervised we use features from raw.
    docs = list(labeled_col.find({}))
    if not docs:
        raise SystemExit("No labeled docs found in fraud_transactions_labeled")
    df = pd.DataFrame([d["features"] for d in docs])
    return df

def train():
    df = load_training_data()
    # IsolationForest expects numeric features — ensure preprocessing done upstream
    clf = IsolationForest(n_estimators=200, contamination=0.01, random_state=42)
    clf.fit(df)
    os.makedirs("model", exist_ok=True)
    joblib.dump({"model": clf, "feature_columns": df.columns.tolist()}, MODEL_OUT)
    print("Saved model to", MODEL_OUT)

if __name__ == "__main__":
    train()
