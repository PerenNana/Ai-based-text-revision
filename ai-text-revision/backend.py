from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import json

app = FastAPI()

class TextRequest(BaseModel):
    text: str
    mode: str = "Style Improvements"


# Define the API endpoint for text revision(i.e. revise_text is ready to receive a post request)
@app.post("/revise")
async def assist_endpoint(request: TextRequest):

    """
    API endpoint for text revision
    :param request: request object containing text and mode
    :return: revised text
    """

    original_text = request.text
    mode = request.mode

    revised_text = await assist_report(original_text, mode)
    return {"revised_text": revised_text}


async def query_ollama(prompt: str) -> str:

    """
    Query the Ollama API
    :param prompt: prompt
    :return: response from Ollama
    """

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )
        try:
            data = json.loads(response.text)
            return data["response"]
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}\nRaw response: {response.text}"


async def assist_report(text: str, mode: str = "Style Improvements") -> str:

    """
    Assist report
    :param text: text to be corrected
    :param mode: mode of correction, improvement
    :return: revised text
    """

    if not text.strip():
        return""

    if mode == "Grammar Issues":
        prompt = (f"Correct the grammar, spelling and punctuation in the following text. "
                  f"Do not change the meaning or structure "
                  f"ONLY GIVE THE CORRECTED TEXT BACK WITHOUT 'Here is the corrected text':\n\n{text}")
    elif mode == "Style Improvements":
        prompt = (f"Improve the style of the following text. "
                  f"Do not change the meaning or structure "
                  f"ONLY GIVE THE CORRECTED TEXT BACK WITHOUT 'Here is the corrected text':\n\n{text}")
    elif mode == "Mixed Issues":
        prompt = (f"Correct the grammar, spelling and punctuation in the following text. "
                  f"Improve the style. Do not change the meaning or structure "
                  f"ONLY GIVE THE CORRECTED TEXT BACK WITHOUT 'Here is the corrected text':\n\n{text}")
    elif mode == "Social Style":
        prompt = (f"Formulate the following text casually, using emojis and modern expressions, ideal for friends. "
                  f"ONLY GIVE THE CORRECTED TEXT BACK WITHOUT 'Here is the formulated text':\n\n{text}")
    elif mode == "Elegant Style":
        prompt = (f"Formulate the following text stylishly and politely, using elegant language. "
                  f"ONLY GIVE THE CORRECTED TEXT BACK WITHOUT 'Here is the formulated text':\n\n{text}")
    elif mode == "Blended Style":
        prompt = (f"Formulate the following text in a friendly, charming, and readable manner a mix of informality and style using emojis. "
                  f"ONLY GIVE THE CORRECTED TEXT BACK WITHOUT 'Here is the corrected text':\n\n{text}")
    try:
        response = await query_ollama(prompt)
        return response.strip()
    except Exception as e:
        return f"Error from LLM: {e}"