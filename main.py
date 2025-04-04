from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langdetect import detect, detect_langs
import os


app = FastAPI()

RAPIDAPI_SECRET = os.getenv("RAPIDAPI_SECRET")


@app.middleware("http")
async def enforce_rapidapi_usage(request: Request, call_next):
    # Allow "/" and "/health" to work without the header
    if request.url.path in ["/", "/health"]:
        return await call_next(request)

    rapidapi_proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")

    if rapidapi_proxy_secret != RAPIDAPI_SECRET:
        return JSONResponse(status_code=403, content={"error": "Access restricted to RapidAPI users only."})

    return await call_next(request)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/")
def read_root():
    welcome_message = (
        "Welcome!"
        "¡Bienvenido!"
        "欢迎!"
        "नमस्ते!"
        "مرحبًا!"
        "Olá!"
        "Здравствуйте!"
        "Bonjour!"
        "বাংলা!"
        "こんにちは!"
    )
    return {"message": welcome_message}


@app.post("/detect-language/")
async def detect_language(request: Request):
    try:
        # Read raw plain text body
        raw_text = await request.body()
        raw_text = raw_text.decode("utf-8").strip()

        if not raw_text:
            raise HTTPException(status_code=400, detail="Missing or empty input.")

        if len(raw_text) < 3:
            raise HTTPException(status_code=400, detail="Text too short for detection.")

        # Optional: Clean extra whitespace or line breaks
        clean_text = " ".join(raw_text.replace("\r", "").split())

        primary_language = detect(clean_text)
        confidence_list = detect_langs(clean_text)
        confidence_dict = {str(lang.lang): lang.prob for lang in confidence_list}

        return {
            "detected_language": primary_language,
            "confidence": confidence_dict
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Language detection failed: {str(e)}")
