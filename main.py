from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from lingua import LanguageDetectorBuilder


app = FastAPI()

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
