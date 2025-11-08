from fastapi import APIRouter
from random import randint
from core.logger import log_event

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.api_route("/", methods=["GET", "POST"])
async def get_dashboard():
    """
    Returns dashboard analytics for the agriculture assistant system.
    """

    metrics = {
        "queries_today": 57,
        "diagnoses": 23,
        "avg_latency_ms": 820,
    }

    trends = [{"day": f"D{i+1}", "queries": randint(20, 80)} for i in range(7)]

    maps = {
        "disease_hotspots": [
            {"district": "Nadia", "count": 12},
            {"district": "Murshidabad", "count": 8},
        ]
    }

    # ✅ Store dashboard access event
    await log_event("dashboard_logs", {"action": "view_dashboard"})

    return {
        "result": {
            "metrics": metrics,
            "trends": trends,
            "maps": maps
        }
    }
