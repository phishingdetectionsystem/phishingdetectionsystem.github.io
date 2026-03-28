from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from pydantic import BaseModel

from backend.app.services.prediction_service import predict_url

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ---------- HTML FORM ROUTE ----------
@router.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, url: str = Form(...)):
    result = predict_url(url)

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "url": url,
            "result": result,
        },
    )


# ---------- JSON API ROUTE ----------
class URLRequest(BaseModel):
    url: str


@router.post("/check-url")
async def check_url(data: URLRequest):
    result = predict_url(data.url)
    return JSONResponse(result)