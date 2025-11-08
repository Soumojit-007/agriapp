from fastapi import APIRouter, HTTPException
from core.schemas import AskIn
from services.gemini import gemini_chat
from core.logger import log_event
import json
import re

router = APIRouter(prefix="/api", tags=["Ask"])


@router.post("/ask")
async def ask(payload: AskIn):

    lang_info = f"(User language hint: {payload.lang})" if payload.lang else ""

    system_prompt = (
        "You are an agriculture assistant.\n"
        "Detect language, extract intent & entities, and give a short actionable answer.\n"
        "Return STRICT JSON ONLY with keys: intent, entities, answer, language.\n"
        "NO markdown. NO ``` blocks. NO extra text.\n"
        f"{lang_info}"
    )

    try:
        raw_response = await gemini_chat(system_prompt, payload.text, 0.2)

        clean = re.sub(r"```[\s\S]*?```", "", raw_response).strip()
        clean = clean.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(clean)

        # ✅ Store input + output in MongoDB
        await log_event("ask_logs", {
            "input_text": payload.text,
            "language_hint": payload.lang,
            "response": parsed
        })

        return {"result": parsed}

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail=f"Model returned non-JSON output:\n{raw_response}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")
