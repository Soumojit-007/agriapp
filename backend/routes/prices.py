from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from services.price import fetch_mandi_prices
from core.logger import log_event   # ✅ Added logging

router = APIRouter(prefix="/api", tags=["prices"])


class PriceResponse(BaseModel):
    history: List[Dict[str, Any]]
    forecast: List[Dict[str, Any]]
    best_mandi: Dict[str, Any]


@router.get("/prices", response_model=PriceResponse)
async def prices(
    crop: str = Query(..., description="Crop name"),
    region: str = Query(..., description="Region / district / mandi name"),
):
    """
    Returns price history + forecast + best mandi suggestion.
    """
    try:
        history, forecast, best = await fetch_mandi_prices(crop=crop, region=region)

        result = PriceResponse(
            history=history,
            forecast=forecast,
            best_mandi=best,
        )

        # ✅ Log request + result to MongoDB
        await log_event("prices_logs", {
            "crop": crop,
            "region": region,
            "history_count": len(history),
            "forecast_count": len(forecast),
            "best_mandi": best
        })

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Price data retrieval error: {str(e)}")
