from fastapi import APIRouter, Query, HTTPException
import json, re
from services.gemini import gemini_chat
from services.policy import fetch_policy_news
from core.logger import log_event   # ✅ logging added

router = APIRouter(prefix="/api", tags=["policy"])


@router.get("/policy")
async def policy(
    region: str = Query("West Bengal", description="Target region for policy/news updates"),
    lang: str = Query("bn", description="Language code for summary output (e.g., 'en', 'bn', 'hi')")
):

    try:
        items = fetch_policy_news(region)
        if not items:
            raise HTTPException(status_code=404, detail=f"No policy/news items found for region: {region}")

        system_prompt = (
            "You are an agricultural policy summarizer. "
            "Summarize the policy/news in the target language. "
            "Return STRICT JSON ONLY (no ``` or explanation): "
            "[{ \"title\": string, \"summary\": string, \"actions\": string }]"
        )

        user_input = f"Region={region}\nLanguage={lang}\nItems={items}"

        content = await gemini_chat(system_prompt, user_input, temperature=0.3)

        clean = re.sub(r"```[a-zA-Z]*|```", "", content).strip()

        try:
            parsed = json.loads(clean)
        except:
            raise HTTPException(
                status_code=500,
                detail="Model returned malformed JSON. Prompt formatting may need adjustment."
            )

        # ✅ Log request + result
        await log_event("policy_logs", {
            "region": region,
            "language": lang,
            "raw_items": items,
            "result": parsed
        })

        return {"result": parsed}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini policy summarization error: {str(e)}"
        )
