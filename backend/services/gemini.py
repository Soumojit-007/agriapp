import json
import httpx
from core.config import settings

class GeminiError(Exception):
    """Custom exception for Gemini API-related errors."""
    pass


async def gemini_chat(system: str | list[dict], user: str = None, temperature: float = 0.2) -> str:
    """
    Sends messages to the Gemini API asynchronously and returns CLEAN TEXT (not parsed JSON).
    Routes will handle parsing & formatting themselves.
    """

    # ✅ Build prompt (Gemini 2.x expects user-only role messages)
    if isinstance(system, str) and isinstance(user, str):
        combined_prompt = f"{system.strip()}\n\nUser query:\n{user.strip()}"
        messages = [{"role": "user", "content": combined_prompt}]
    elif isinstance(system, list):
        messages = [
            {"role": ("user" if m["role"] == "system" else m["role"]), "content": m["content"]}
            for m in system
        ]
    else:
        raise GeminiError("Invalid input format for gemini_chat(). Must be (system: str, user: str) or list of dict messages.")

    api_key = getattr(settings, "GEMINI_API_KEY", None)
    model = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
    base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    if not api_key:
        raise GeminiError("Missing required environment variable: GEMINI_API_KEY")

    headers = {"Content-Type": "application/json"}

    # ✅ Convert to Gemini request structure
    contents = [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in messages]
    payload = {"contents": contents, "generationConfig": {"temperature": temperature}}

    try:
        async with httpx.AsyncClient(timeout=60, verify=False) as client:
            response = await client.post(f"{base_url}?key={api_key}", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        candidates = data.get("candidates", [])
        if not candidates:
            raise GeminiError(f"Unexpected Gemini response: {data}")

        text = (
            candidates[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )

        # ✅ Clean markdown wrappers but DO NOT parse
        text = text.replace("```json", "").replace("```", "").strip()

        return text  # ✅ Return raw clean string — parsing happens in route

    except httpx.TimeoutException:
        raise GeminiError("Gemini API request timed out.")

    except httpx.HTTPStatusError as e:
        try:
            error_detail = response.json().get("error", {}).get("message", str(e))
        except:
            error_detail = str(e)
        raise GeminiError(f"Gemini API HTTP error: {error_detail}")

    except Exception as e:
        raise GeminiError(f"Unexpected Gemini API error: {str(e)}")
