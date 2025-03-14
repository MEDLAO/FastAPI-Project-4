import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from langdetect import detect, DetectorFactory


app = FastAPI()


RAPIDAPI_SECRET = os.getenv("RAPIDAPI_SECRET")


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


# Fix randomness in langdetect (for consistent results)
DetectorFactory.seed = 0


@app.get("/detect-language/")
def detect_language(text: str = Query(..., min_length=3)):
    try:
        language = detect(text)
        return {"language": language}
    except:
        return {"error": "Could not detect language"}
