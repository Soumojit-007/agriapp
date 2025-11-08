def format_fert_prompt(crop, soil=None, symptoms=None, organicPreferred=False):
    """
    Builds a model-friendly fertilizer recommendation prompt.

    Args:
        crop (str): Name of the crop.
        soil (dict | None): Optional soil data (NPK, pH, etc.).
        symptoms (str | None): Optional crop symptoms.
        organicPreferred (bool): Whether organic fertilizers are preferred.

    Returns:
        str: Formatted prompt text for Gemini.
    """

    def _format_soil_value(k, v):
        if k.lower() == "ph":
            return f"pH: {v}"
        elif k.lower() in ["n", "p", "k"]:
            return f"{k.upper()}: {v} mg/kg"
        return f"{k.capitalize()}: {v}"

    soil_text = ", ".join(_format_soil_value(k, v) for k, v in soil.items()) if soil else "Not provided"
    symptoms_text = symptoms or "None provided"
    organic_text = "Yes" if organicPreferred else "No"

    prompt = (
        f"Provide a fertilizer recommendation based on the following details:\n\n"
        f"Crop: {crop}\n"
        f"Soil: {soil_text}\n"
        f"Symptoms: {symptoms_text}\n"
        f"OrganicPreferred: {organic_text}"
    )

    return prompt
