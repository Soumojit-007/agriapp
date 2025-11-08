from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import json, re
from services.gemini import gemini_chat
from services.fert import format_fert_prompt
from core.logger import log_event   # ✅ Added logging

router = APIRouter(prefix="/api", tags=["fertilizer"])


@router.get("/fertilizer")
async def fertilizer(
    crop: str = Query(..., description="Crop name"),
    soil: Optional[str] = Query(None, description="Soil info (string or JSON)"),
    symptoms: Optional[str] = Query("", description="Observed crop symptoms"),
    organicPreferred: bool = Query(False, description="Prefer organic fertilizers?")
):
    try:
        # ✅ Convert soil into dict safely
        if soil:
            try:
                soil = json.loads(soil)  # JSON input
            except:
                soil = {"type": soil}   # Plain text input

        system_prompt = (
            "You are an expert agronomist. Recommend a fertilizer plan.\n"
            "Return STRICT JSON ONLY:\n"
            "{\n"
            "  \"npk\": \"string\",\n"
            "  \"product_options\": [string],\n"
            "  \"dosage_per_ha\": \"string\",\n"
            "  \"notes\": \"string\"\n"
            "}"
        )

        user_prompt = format_fert_prompt(
            crop=crop,
            soil=soil,
            symptoms=symptoms,
            organicPreferred=organicPreferred,
        )

        content = await gemini_chat(system_prompt, user_prompt, temperature=0.2)

        clean = re.sub(r"```[a-zA-Z]*|```", "", content).strip()
        parsed = json.loads(clean)

        # ✅ Log input and result to MongoDB
        await log_event("fertilizer_logs", {
            "crop": crop,
            "soil": soil,
            "symptoms": symptoms,
            "organicPreferred": organicPreferred,
            "result": parsed
        })

        return {"result": parsed}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fertilizer API error: {str(e)}")
