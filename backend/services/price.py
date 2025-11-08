# import httpx
# from datetime import datetime, timedelta
# from core.config import settings
# import dotenv
# dotenv.load_dotenv()

# async def fetch_mandi_prices(crop: str, region: str):
#     """
#     Fetches mandi price data and performs flexible matching on region.
#     """

#     api_key = settings.AGMARKET_API_KEY
#     if not api_key:
#         raise ValueError("Missing AGMARKET_API_KEY in .env")

#     url = (
#         f"https://api.data.gov.in/resource/{settings.AGMARKNET_RESOURCE}"
#         f"?api-key={api_key}&format=json"
#         f"&filters[commodity]={crop}"
#         f"&limit=200"
#     )

#     async with httpx.AsyncClient(timeout=30) as client:
#         res = await client.get(url)
#         res.raise_for_status()
#         data = res.json()

#     records = data.get("records", [])

#     # ✅ Fuzzy match: region may refer to state, district, or market
#     region_lower = region.lower()
#     records = [
#         r for r in records
#         if region_lower in str(r.get("state", "")).lower()
#         or region_lower in str(r.get("district", "")).lower()
#         or region_lower in str(r.get("market", "")).lower()
#     ]

#     if not records:
#         return [], [], {}

#     # ✅ Sort safely even if arrival_date missing
#     records = sorted(records, key=lambda r: r.get("arrival_date", "") or "", reverse=True)

#     # ✅ Clean price values & take recent 7 days
#     history = []
#     for r in records[:7]:
#         price = r.get("modal_price")
#         if price and price not in ("NA", ""):
#             history.append({
#                 "date": r.get("arrival_date", "Unknown"),
#                 "price": int(float(price))
#             })

#     if not history:
#         return [], [], {}

#     # ✅ Generate simple forecast
#     avg_price = sum(x["price"] for x in history) // len(history)
#     forecast = [
#         {"date": (datetime.today() + timedelta(days=i * 7)).strftime("%Y-%m-%d"), "price": avg_price + i * 15}
#         for i in range(1, 3)
#     ]

#     # ✅ Suggest best mandi
#     best = {
#         "name": records[0].get("market", "Unknown Market"),
#         "expected_price": max(x["price"] for x in history)
#     }

#     return history, forecast, best








from datetime import datetime, timedelta

# Dummy price datasets for some crops
DUMMY_PRICE_DB = {
    "Tomato": [1500, 1600, 1550, 1700, 1750, 1680, 1800],
    "Potato": [1000, 1100, 1150, 1200, 1180, 1220, 1250],
    "Wheat":  [2200, 2250, 2300, 2280, 2350, 2400, 2450],
    "Onion":  [1400, 1380, 1450, 1500, 1480, 1520, 1580],
}

async def fetch_mandi_prices(crop: str, region: str):
    """
    Returns dummy mandi price history, forecast, and best mandi.
    Region is ignored for now (since dummy data is static).
    """

    crop = crop.capitalize()

    if crop not in DUMMY_PRICE_DB:
        # For unknown crops, generate a simple synthetic price pattern
        base = 1500
        history = [{"date": (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d"), "price": base + (i * 10)}
                   for i in range(7)]
    else:
        prices = DUMMY_PRICE_DB[crop]
        history = [
            {"date": (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d"), "price": prices[::-1][i]}
            for i in range(len(prices))
        ]

    # Simple forecast: gradual rise trend
    avg_price = sum(p["price"] for p in history) // len(history)
    forecast = [
        {"date": (datetime.today() + timedelta(days=7 * i)).strftime("%Y-%m-%d"), "price": avg_price + (i * 50)}
        for i in range(1, 3)
    ]

    # Fake mandi suggestion
    best_mandi = {
        "name": f"{region} Central Mandi",
        "expected_price": max(p["price"] for p in history)
    }

    return history, forecast, best_mandi
