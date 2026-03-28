from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


class FeedbackRequest(BaseModel):
    url: HttpUrl
    actual_label: str = Field(..., pattern="^(phishing|legitimate)$")
    user_comment: Optional[str] = None
