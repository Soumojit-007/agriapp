from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from services.gemini import gemini_chat
from services.vision import to_base64
from core.logger import log_event
import json, re

router = APIRouter(prefix="/api", tags=["Diagnose"])

@router.post("/diagnose")
async def diagnose(
    image: UploadFile | None = File(default=None),
    symptom: str = Form(default="")
):
    try:
        # ---- Handle image ----
        img_bytes = None
        img_b64 = None
        
        if image:
            img_bytes = await image.read()
            if not img_bytes:
                raise HTTPException(status_code=400, detail="Uploaded image is empty.")
            img_b64 = to_base64(img_bytes)

        # ---- Prompt Construction ----
        system_prompt = (
            "You are an agricultural disease diagnosis expert.\n"
            "Analyze crops for diseases.\n"
            "If an image is provided, use it first. If only text, infer from symptoms.\n"
            "Return STRICT JSON ONLY:\n"
            "{\n"
            "  \"disease\": string or null,\n"
            "  \"confidence\": number (0-1),\n"
            "  \"treatment_steps\": string[],\n"
            "  \"pesticide_options\": string[]\n"
            "}\n"
        )

        user_prompt = (
            f"Symptoms: {symptom or 'None provided'}\n"
            f"Image (Base64): {img_b64 or 'No image provided'}"
        )

        # ---- FIXED: Ensure valid content input ----
        content_input = img_b64 if img_b64 else user_prompt

        # ---- Call Model ----
        response = await gemini_chat(system_prompt, content_input, temperature=0.25)

        # ---- Clean accidental formatting ----
        clean = re.sub(r"```[a-zA-Z]*|```", "", response).strip()

        try:
            parsed = json.loads(clean)
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Model returned invalid JSON. Raw model output:\n" + response
            )

        # ---- Log Entry (Safe) ----
        await log_event("diagnose_logs", {
            "symptom": symptom,
            "has_image": bool(img_b64),
            "image_base64": img_b64,
            "result": parsed
        })

        return {"result": parsed}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnosis error: {str(e)}")
