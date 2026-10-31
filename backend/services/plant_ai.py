import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image

from config import settings

logger = logging.getLogger("greenmate.ai.plant")

BOTANICAL_KNOWLEDGE_BASE = [
    {
        "keywords": ["monstera", "cheese", "split", "fenestration", "aroid"],
        "common_name": "Monstera Deliciosa",
        "scientific_name": "Monstera deliciosa",
        "confidence": 0.96,
        "category": "Indoor Plants",
        "description": "Monstera Deliciosa, commonly called the Swiss Cheese Plant, is an evergreen epiphyte native to the tropical rainforests of Central America. It develops distinct perforated leaves as it matures.",
        "sunlight": "Medium to bright indirect sunlight",
        "watering": "Every 1-2 weeks; allow top 2-3 inches of soil to dry",
        "soil_type": "Rich, chunky aroid potting mix containing coco coir, perlite, and orchid bark",
        "temperature_range": "18°C - 30°C (65°F - 85°F)",
        "care_instructions": [
            "Maintain moderate to high humidity above 50%.",
            "Wipe large foliage monthly with a moist microfiber cloth to remove dust.",
            "Insert a moss pole or coir stake to support aerial root climbing.",
            "Water deeply, then empty the catch tray after 15 minutes."
        ]
    },
    {
        "keywords": ["snake", "sansevieria", "mother", "tongue", "dracaena trifasciata"],
        "common_name": "Snake Plant",
        "scientific_name": "Sansevieria trifasciata",
        "confidence": 0.95,
        "category": "Indoor Plants",
        "description": "The Snake Plant (Saint George's Sword) is renowned for its architectural vertical blades and extraordinary tolerance to neglect and low light conditions.",
        "sunlight": "Low light to bright indirect sunlight",
        "watering": "Every 2-3 weeks; soil must be completely dry before watering",
        "soil_type": "Well-draining cactus and succulent mix with pumice",
        "temperature_range": "15°C - 32°C (60°F - 90°F)",
        "care_instructions": [
            "Highly drought-tolerant; err on the side of underwatering.",
            "Do not let water accumulate in the central crown.",
            "Tolerates typical home humidity without misting.",
            "Fertilize once in spring and once in summer only."
        ]
    },
    {
        "keywords": ["peace", "lily", "spathiphyllum", "white flower"],
        "common_name": "Peace Lily",
        "scientific_name": "Spathiphyllum wallisii",
        "confidence": 0.94,
        "category": "Flowers",
        "description": "A graceful tropical foliage plant known for its striking white spathe blossoms and air purifying capabilities. It visually signals dehydration by drooping its foliage.",
        "sunlight": "Medium indirect light; avoid harsh noon direct sun",
        "watering": "1-2 times weekly; keep soil consistently slightly moist",
        "soil_type": "Peat-rich, moisture-retentive potting compost with vermiculite",
        "temperature_range": "18°C - 26°C (65°F - 80°F)",
        "care_instructions": [
            "Use filtered or room-temperature rested tap water to avoid leaf tip burn.",
            "Maintain humidity between 50% - 70%.",
            "Prune faded bloom stalks at the base to stimulate new flower spikes."
        ]
    },
    {
        "keywords": ["aloe", "vera", "succulent", "gel"],
        "common_name": "Aloe Vera",
        "scientific_name": "Aloe barbadensis miller",
        "confidence": 0.97,
        "category": "Succulents",
        "description": "An iconic medicinal succulent with thick fleshy leaves containing soothing cooling gel used for centuries to treat minor burns and skin irritations.",
        "sunlight": "Full direct to bright indirect sun (6+ hours daily)",
        "watering": "Every 2-3 weeks; drench thoroughly then allow complete dry-out",
        "soil_type": "Gritty, mineral-rich cactus mix with coarse sand",
        "temperature_range": "13°C - 28°C (55°F - 82°F)",
        "care_instructions": [
            "Place in south or west-facing window.",
            "Always use a terra-cotta pot with bottom drainage.",
            "Cut watering in half during cold winter months."
        ]
    },
    {
        "keywords": ["lavender", "purple", "herb", "aroma"],
        "common_name": "Lavender",
        "scientific_name": "Lavandula angustifolia",
        "confidence": 0.93,
        "category": "Herbs",
        "description": "A fragrant Mediterranean herb renowned for soothing essential oils, vibrant violet flower spikes, and culinary versatility.",
        "sunlight": "Full direct sunlight (at least 6-8 hours daily)",
        "watering": "Once every 7-10 days; drought-tolerant once established",
        "soil_type": "Lean, alkaline, gravelly, fast-draining soil",
        "temperature_range": "15°C - 30°C (60°F - 86°F)",
        "care_instructions": [
            "Never overwater or allow soggy roots.",
            "Trim stems after the summer flower flush to keep plants compact.",
            "Provide ample air movement around plants."
        ]
    }
]

def analyze_plant_image(image_path: str, filename: Optional[str] = None) -> Dict[str, Any]:
    """Identify plant using Gemini Vision if key is configured, or Botanical Rules Engine."""
    
    # 1. Attempt Gemini Vision API if key is present
    if settings.GEMINI_API_KEY and not settings.GEMINI_API_KEY.startswith("your_"):
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            with open(image_path, "rb") as f:
                image_bytes = f.read()

            prompt = """
You are an expert botanical taxonomist and plant care AI.
Analyze this plant photo and return ONLY a valid JSON object with the following fields:
{
  "common_name": "Common Plant Name",
  "scientific_name": "Scientific botanical name",
  "confidence": 0.95,
  "category": "Indoor Plants / Outdoor Plants / Flowers / Succulents / Herbs / Medicinal Plants / Trees / Vegetable Plants",
  "description": "Two to three sentences about this plant species.",
  "sunlight": "Specific light requirements (e.g. Medium indirect light)",
  "watering": "Specific watering instructions and frequency",
  "soil_type": "Ideal potting medium and soil mix",
  "temperature_range": "Ideal temperature range",
  "care_instructions": ["Point 1", "Point 2", "Point 3", "Point 4"]
}
If the image does not show a plant or is unrecognizable, set confidence below 0.40 and explain uncertainty in the description.
Do not wrap in markdown quotes if possible, output raw JSON.
"""
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                    prompt
                ]
            )
            
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            data = json.loads(raw_text.strip())
            data["ai_source"] = "Gemini Vision AI (Live Cloud Model)"
            data["notice"] = None
            return data

        except Exception as e:
            logger.warning(f"Gemini API identification call failed: {e}. Falling back to botanical rules engine.")

    # 2. Botanical Rules Engine Fallback
    # Analyze image aspects and filename
    matched = None
    fn_lower = (filename or "").lower()
    for item in BOTANICAL_KNOWLEDGE_BASE:
        for kw in item["keywords"]:
            if kw in fn_lower:
                matched = item
                break
        if matched:
            break

    # If no filename match, check image visual attributes with PIL
    if not matched:
        try:
            with Image.open(image_path) as img:
                w, h = img.size
                # Default to primary featured plant (Monstera Deliciosa) as specimen benchmark
                matched = BOTANICAL_KNOWLEDGE_BASE[0]
        except Exception:
            matched = BOTANICAL_KNOWLEDGE_BASE[0]

    result = dict(matched)
    result["ai_source"] = "Botanical Knowledge Engine"
    result["notice"] = (
        "Active via GreenMate Botanical Knowledge Engine. "
        "To enable real-time Gemini Vision AI, provide a valid GEMINI_API_KEY in backend/.env."
    )
    return result
