import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_model():
    model_path = BASE_DIR / "phishing_model.pkl"

    with open(model_path, "rb") as file:
        model = pickle.load(file)

    return model
