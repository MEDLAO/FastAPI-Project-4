import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bs4 import BeautifulSoup


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


class HTMLInput(BaseModel):
    html: str  # Accepts any HTML snippet or full document


def html_to_json(html: str) -> dict:
    """Convert any HTML snippet or full document to structured JSON."""
    try:
        soup = BeautifulSoup(html, "lxml")

        data = {
            "title": soup.title.string if soup.title else None,
            "meta": {
                meta.get("name", meta.get("property", "unknown")): meta.get("content", "")
                for meta in soup.find_all("meta")
            },
            "headings": {f"h{i}": [h.text.strip() for h in soup.find_all(f"h{i}")] for i in range(1, 7)},
            "text": soup.get_text(separator=" ", strip=True),
            "links": [{"text": a.text.strip(), "href": a.get("href")} for a in soup.find_all("a") if a.get("href")],
            "images": [{"alt": img.get("alt", ""), "src": img.get("src")} for img in soup.find_all("img")],
            "tables": [
                {
                    "headers": [th.text.strip() for th in table.find_all("th")],
                    "rows": [[td.text.strip() for td in row.find_all("td")] for row in table.find_all("tr") if row.find_all("td")]
                }
                for table in soup.find_all("table")
            ],
            "forms": [
                {
                    "action": form.get("action", ""),
                    "method": form.get("method", "get").lower(),
                    "inputs": [{"name": inp.get("name"), "type": inp.get("type", "text")} for inp in form.find_all("input")]
                }
                for form in soup.find_all("form")
            ],
            "divs": [
                {"class": div.get("class"), "text": div.get_text(strip=True)}
                for div in soup.find_all("div") if div.get_text(strip=True)
            ],
            "spans": [
                {"class": span.get("class"), "text": span.get_text(strip=True)}
                for span in soup.find_all("span") if span.get_text(strip=True)
            ],
        }
        return data

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Parsing error: {str(e)}")


@app.post("/convert")
async def convert_html_to_json(input_data: HTMLInput):
    """API endpoint to convert any HTML snippet or full page to JSON."""
    json_output = html_to_json(input_data.html)
    return {"json": json_output}
