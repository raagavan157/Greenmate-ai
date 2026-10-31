import json
import logging
from typing import Dict, Any
from config import settings

logger = logging.getLogger("greenmate.ai.care")

def generate_personalized_care_plan(data: Dict[str, Any]) -> Dict[str, Any]:
    species = data.get("plant_species", "Houseplant")
    env = data.get("environment", "indoor")
    light = data.get("sunlight", "Medium Light")
    temp = data.get("temperature", "22°C - 26°C")
    water_pref = data.get("watering_preference", "Moderate")
    stage = data.get("growth_stage", "Mature")

    # 1. Try Gemini API
    if settings.GEMINI_API_KEY and not settings.GEMINI_API_KEY.startswith("your_"):
        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            prompt = f"""
You are a senior botanist and horticulturist.
Create a personalized care plan for:
Species: {species}
Environment: {env}
Sunlight: {light}
Temperature: {temp}
Watering Preference: {water_pref}
Growth Stage: {stage}

Return ONLY a JSON object:
{{
  "plant_species": "{species}",
  "environment": "{env}",
  "daily_care": ["Tip 1", "Tip 2", "Tip 3"],
  "weekly_watering": {{
    "frequency": "e.g. 1-2 times per week",
    "schedule_days": ["Wednesday", "Sunday"],
    "technique": "Water deeply until runoff appears, avoid wetting foliage."
  }},
  "monthly_fertilizer": {{
    "frequency": "Every 3-4 weeks",
    "ratio": "Balanced 10-10-10 or 20-20-20 at half strength",
    "best_time": "Morning during active growth"
  }},
  "seasonal_recommendations": {{
    "spring": "Resume active feeding and prune winter dieback.",
    "summer": "Increase watering frequency and mist if dry.",
    "autumn": "Taper off feeding and check for drafty windows.",
    "winter": "Reduce watering by 40% and move closer to sunlight."
  }},
  "custom_tips": ["Custom advice 1", "Custom advice 2"]
}}
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            raw = response.text.strip()
            if raw.startswith("```json"):
                raw = raw[7:]
            if raw.endswith("```"):
                raw = raw[:-3]
            plan = json.loads(raw.strip())
            plan["ai_source"] = "Gemini AI (Live Cloud Model)"
            return plan
        except Exception as e:
            logger.warning(f"Gemini Care Plan failed: {e}. Using expert botanical algorithm.")

    # 2. Expert Algorithmic Generation
    is_indoor = env.lower() == "indoor"
    watering_days = ["Wednesday", "Sunday"] if "frequent" in water_pref.lower() or "high" in water_pref.lower() else ["Saturday"]
    
    plan = {
        "plant_species": species,
        "environment": env,
        "daily_care": [
            f"Check soil surface moisture 1-2 inches deep before any watering.",
            f"Ensure {light.lower()} exposure without harsh midday glass magnification.",
            "Rotate pot by 90 degrees every week to maintain balanced, upright growth."
        ],
        "weekly_watering": {
            "frequency": "1-2 times per week" if is_indoor else "2-3 times per week",
            "schedule_days": watering_days,
            "technique": "Soak soil thoroughly until water emerges from drainage holes. Discard pooled saucer water."
        },
        "monthly_fertilizer": {
            "frequency": "Once every 3 to 4 weeks during active growth (March - October)",
            "ratio": "Balanced water-soluble organic plant food diluted to half strength",
            "best_time": "Apply to pre-moistened soil on warm mornings"
        },
        "seasonal_recommendations": {
            "spring": "Repot if roots circle the container. Inspect for early aphids and spider mites.",
            "summer": "Shield foliage from intense afternoon heat waves. Maintain ambient humidity.",
            "autumn": "Gradually reduce watering as daylight hours decline.",
            "winter": "Withhold fertilizer completely. Guard against cold window drafts and dry heating vents."
        },
        "custom_tips": [
            f"Because this specimen is kept {env}, clean leaf surfaces with a damp cloth to maximize light absorption.",
            f"Tailored specifically for the {stage.lower()} growth stage of {species}."
        ],
        "ai_source": "GreenMate Horticultural Care Engine"
    }
    return plan
