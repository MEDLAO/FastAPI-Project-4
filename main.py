from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from lingua import LanguageDetectorBuilder
import os


app = FastAPI()

RAPIDAPI_SECRET = os.getenv("RAPIDAPI_SECRET")


# @app.middleware("http")
# async def enforce_rapidapi_usage(request: Request, call_next):
#     # Bypass authentication for the /welcome endpoint
#     if request.url.path == "/":
#         return await call_next(request)
#
#     rapidapi_proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")
#
#     if rapidapi_proxy_secret != RAPIDAPI_SECRET:
#         return JSONResponse(status_code=403, content={"error": "Access restricted to RapidAPI users only."})
#
#     return await call_next(request)


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


# Build detector for all available languages
detector = LanguageDetectorBuilder.from_all_languages().build()


class TextInput(BaseModel):
    text: str  # Accepts raw multi-line text


@app.post("/detect-language/")
async def detect_language(input_data: TextInput):
    """
    Language Detection API

    - Supports 75 languages.
    - Returns detected language and confidence scores.
    """
    try:
        raw_text = input_data.text.strip()

        # Detect primary language
        detected_lang = detector.detect_language_of(raw_text)

        # Get confidence scores (FIXED: Correctly extract values)
        confidence_scores = detector.compute_language_confidence_values(raw_text)
        confidence_dict = {str(confidence.language): confidence.value for confidence in confidence_scores}

        return {
            "detected_language": str(detected_lang),
            "confidence": confidence_dict
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error detecting language: {str(e)}")
