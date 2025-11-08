# import feedparser
# from datetime import datetime

# def fetch_policy_news(region: str):
#     """
#     Fetches agricultural policy/news from PIB RSS feed,
#     filters agriculture-related items, and returns structured summaries.
#     """

#     FEED_URL = "https://pib.gov.in/PressReleaseRSS.aspx"
#     feed = feedparser.parse(FEED_URL)

#     results = []

#     for entry in feed.entries[:12]:
#         title_lower = entry.title.lower()

#         if any(keyword in title_lower for keyword in ["agriculture", "farmer", "crop", "paddy", "fertilizer"]):
            
#             # ✅ Safe date parsing
#             if hasattr(entry, "published_parsed") and entry.published_parsed:
#                 date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
#             else:
#                 date = "Unknown"

#             results.append({
#                 "title": entry.title,
#                 "text": entry.summary,
#                 "date": date,
#                 "actions": f"Relevant for farmers in {region}. Review eligibility and local announcements."
#             })

#     return results[:5]  # Return top 5 relevant items


from datetime import datetime

def fetch_policy_news(region: str):
    """
    Temporary fallback policy/news data while PIB RSS is unavailable.
    Returns realistic agricultural policy updates with variety & depth.
    """

    MOCK_DATA = [
        {
            "title": "New Subsidy Scheme to Reduce Fertilizer Costs",
            "text": "Government launches subsidy support aimed at reducing production cost by making fertilizers cheaper for small and marginal farmers.",
            "date": "2025-01-22",
            "actions": f"Farmers in {region} should contact Krishi Vigyan Kendra for subsidy claim steps."
        },
        {
            "title": "PM-KISAN 16th Installment Disbursement Scheduled",
            "text": "The next installment under PM-KISAN will be released directly to farmers’ bank accounts.",
            "date": "2025-01-20",
            "actions": f"Ensure Aadhaar-bank linking is completed in {region} to avoid payment delay."
        },
        {
            "title": "Crop Insurance Deadline Extended Due to Weather Delay",
            "text": "The enrollment deadline for the PMFBY crop insurance scheme has been extended by 15 days for several districts.",
            "date": "2025-01-19",
            "actions": f"Farmers in {region} should visit nearest CSC center to enroll before the extended deadline."
        },
        {
            "title": "Free Soil Health Testing Drive Announced",
            "text": "A new soil testing initiative aims to help farmers understand nutrient levels for better crop planning.",
            "date": "2025-01-18",
            "actions": f"Farmers in {region} can get soil tested at local Agriculture Science Center."
        },
        {
            "title": "Organic Farming Support Program Expanded",
            "text": "Financial and training assistance will be provided to promote organic and residue-free cultivation.",
            "date": "2025-01-17",
            "actions": f"Farmers in {region} can apply through the state agricultural department portal."
        },
        {
            "title": "Minimum Support Price (MSP) Revision Announced",
            "text": "MSP for several rabi crops has been increased to improve farmer income and procurement fairness.",
            "date": "2025-01-15",
            "actions": f"Check local mandi boards in {region} for updated procurement schedule."
        },
        {
            "title": "Government to Provide Weather Advisory Alerts via SMS",
            "text": "New localized weather alerts will be sent to help reduce crop loss due to unexpected rainfall or heatwaves.",
            "date": "2025-01-12",
            "actions": f"Farmers in {region} must register mobile number with Kisan Call Center to receive SMS alerts."
        },
        {
            "title": "Subsidized Solar Pumps to Support Irrigation",
            "text": "Government introduces solar-powered irrigation pump support to reduce dependency on diesel.",
            "date": "2025-01-10",
            "actions": f"Applications in {region} open until next month — verify eligibility early."
        },
        {
            "title": "Training Campaign on Scientific Pest Management Launched",
            "text": "Workshops will be conducted for farmers to reduce pesticide misuse and resistance.",
            "date": "2025-01-09",
            "actions": f"Farmers in {region} can attend free demonstration sessions at Panchayat centers."
        },
        {
            "title": "New Warehouse Loan Scheme Approved",
            "text": "Warehouse collateral loans to help farmers store produce and avoid distress sale.",
            "date": "2025-01-07",
            "actions": f"Farmers in {region} must get produce quality-graded to qualify."
        }
    ]

    return MOCK_DATA  # ✅ return all, not just 5



















