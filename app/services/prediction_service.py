import joblib
import numpy as np
import re
from pathlib import Path
from urllib.parse import urlparse

from backend.app.services.feature_extractor import extract_features

# ---------- MODEL ----------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "app" / "models" / "phishing_model.pkl"

model = joblib.load(MODEL_PATH)

# ---------- RULES ----------
SUSPICIOUS_WORDS = [
    "login", "verify", "secure", "account",
    "update", "bank", "payment", "confirm",
    "paypal", "security", "signin"
]


def rule_based_score(url):
    score = 0

    if len(url) > 75:
        score += 2

    if url.count(".") > 3:
        score += 2

    if url.count("-") >= 2:
        score += 2

    if "@" in url:
        score += 3

    if "%" in url or "//" in url[8:]:
        score += 2

    if re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url):
        score += 4

    lower_url = url.lower()
    for word in SUSPICIOUS_WORDS:
        if word in lower_url:
            score += 1

    return score


def predict_url(url: str):
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    features = extract_features(url)
    features = np.array(features).reshape(1, -1)

    if hasattr(model, "predict_proba"):
        ml_probability = model.predict_proba(features)[0][1]
    else:
        ml_probability = 0.50


    # normalize probability
    if ml_probability > 1:
        ml_probability = ml_probability / 100

    risk_score = rule_based_score(url)

    is_phishing = (ml_probability > 0.45 or risk_score >= 4)

    label = "Phishing" if is_phishing else "Safe"

    if risk_score >= 6:
        risk_level = "HIGH"
    elif risk_score >= 3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    recommendation = (
        "Avoid this website!"
        if is_phishing
        else "Looks safe."
    )

    return {
    "url": url,
    "prediction": label,
    "is_phishing": bool(is_phishing),
    "confidence": float(ml_probability * 100),
    "risk_level": risk_level,
    "rule_score": int(risk_score),
    "recommendation": recommendation
}

