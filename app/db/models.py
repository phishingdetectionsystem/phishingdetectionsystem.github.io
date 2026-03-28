from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime
from backend.app.db.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    is_phishing = Column(Boolean)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
