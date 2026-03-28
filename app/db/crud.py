from backend.app.db.database import SessionLocal
from backend.app.db.models import Prediction


def save_prediction(url: str, prediction: bool, confidence: float):
    db = SessionLocal()
    db_obj = Prediction(
        url=url,
        is_phishing=bool(prediction),
        confidence=float(confidence)
    )
    db.add(db_obj)
    db.commit()
    db.close()
