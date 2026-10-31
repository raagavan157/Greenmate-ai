import logging
from typing import Dict, Any, List, Optional
from config import settings

logger = logging.getLogger("greenmate.ai.chat")

SYSTEM_PROMPT = """
You are GreenMate AI Assistant, a friendly, knowledgeable, and practical botanist and plant care AI.
You help indoor and outdoor gardeners keep their plants healthy, identify species, diagnose health issues, explain watering schedules, sunlight needs, soil, and fertilizer.
Keep answers concise, actionable, and encouraging. Use bullet points for steps.
"""

def generate_chat_response(
    message: str,
    plant_context: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    msg_lower = message.strip().lower()

    # 1. Gemini Cloud AI Chat if key is configured
    if settings.GEMINI_API_KEY and not settings.GEMINI_API_KEY.startswith("your_"):
        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            conversation_text = SYSTEM_PROMPT + "\n\n"
            if plant_context:
                conversation_text += f"Current Plant Context: {plant_context}\n\n"
            
            if history:
                for turn in history[-6:]:
                    role = turn.get("role", "user")
                    content = turn.get("content", "")
                    conversation_text += f"{role.capitalize()}: {content}\n"

            conversation_text += f"User: {message}\nAssistant:"

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=conversation_text
            )
            return {
                "reply": response.text.strip(),
                "suggested_followups": [
                    "How often should I water it?",
                    "What light does it need?",
                    "Check for common pests",
                    "Add this plant to My Garden"
                ],
                "ai_source": "Gemini AI (Live Cloud Model)"
            }
        except Exception as e:
            logger.warning(f"Gemini Chat failed: {e}. Using botanical dialog engine.")

    # 2. Expert Botanical Dialog Engine
    reply = ""
    suggested = ["Watering tips", "Sunlight guide", "Diagnose symptoms", "Explore popular plants"]

    if any(k in msg_lower for k in ["water", "watering", "dry", "soak"]):
        reply = (
            "🌿 **Watering Best Practice:**\n\n"
            "• **The 2-Inch Check:** Always insert your finger 2 inches into the soil before watering.\n"
            "• **Golden Rule:** If the soil feels damp and cool, wait. If dry and crumbly, water deeply.\n"
            "• **Drainage:** Always ensure the pot has drainage holes. Empty the saucer after 15 minutes to prevent root rot."
        )
        suggested = ["How to fix root rot?", "What is bottom watering?", "Sunlight requirements"]

    elif any(k in msg_lower for k in ["light", "sun", "sunlight", "window", "dark"]):
        reply = (
            "☀️ **Sunlight Guidance:**\n\n"
            "• **Bright Indirect Light:** Ideal for Monsteras, Pothos, and Peace Lilies. Placed 3-5 feet from an East or West window.\n"
            "• **Direct Sun:** Essential for succulents, cacti, Aloe Vera, and herbs (6+ hours daily).\n"
            "• **Low Light:** Snake Plants and ZZ Plants tolerate dim corners, but thrive with occasional filtered light."
        )
        suggested = ["Best plants for low light", "Watering schedules", "Identify a plant"]

    elif any(k in msg_lower for k in ["yellow", "brown", "spot", "sick", "dying", "leaves falling", "droop"]):
        reply = (
            "🩺 **Health Assessment:**\n\n"
            "• **Yellowing leaves:** Most frequently caused by overwatering or poor drainage. Check if roots are mushy.\n"
            "• **Brown crispy tips:** Usually indicates low room humidity or tap water fluoride/chlorine sensitivity.\n"
            "• **Drooping foliage:** Peace Lilies and Fittonias droop when thirsty. Water thoroughly and they bounce back within hours.\n\n"
            "You can use our **Smart Plant Doctor** on the navigation bar to upload a photo for instant diagnostic analysis!"
        )
        suggested = ["Diagnose plant disease", "Watering tips", "Soil preparation"]

    elif any(k in msg_lower for k in ["fertilizer", "feed", "food", "nutrients"]):
        reply = (
            "🌱 **Fertilizing Advice:**\n\n"
            "• Feed houseplants only during active growing season (Spring & Summer).\n"
            "• Use a balanced 10-10-10 or 20-20-20 liquid houseplant feed diluted to half strength.\n"
            "• Never fertilize completely dry soil—pre-moisten with pure water first to prevent root burn."
        )
        suggested = ["Organic fertilizer recipes", "Watering frequency", "Winter care"]

    elif any(k in msg_lower for k in ["hello", "hi", "hey", "help"]):
        reply = (
            "Hello! I'm your **GreenMate AI Assistant** 🌿.\n\n"
            "I can help you with:\n"
            "• Identifying unknown plants from photos\n"
            "• Diagnosing pests, mildew, and yellow leaves\n"
            "• Creating customized watering schedules\n"
            "• Selecting the right indoor or outdoor plants for your home"
        )
        suggested = ["Identify a plant", "Plant care tips", "Diagnose plant disease", "My Garden"]

    elif any(k in msg_lower for k in ["monstera", "cheese plant"]):
        reply = (
            "🌿 **Monstera Deliciosa Care:**\n\n"
            "• **Light:** Bright indirect light to develop beautiful fenestrations (leaf holes).\n"
            "• **Watering:** Water every 1-2 weeks when top 2-3 inches are dry.\n"
            "• **Support:** Provide a moss pole for climbing aerial roots.\n"
            "• **Pro Tip:** Wipe leaves monthly with a damp cloth to maximize photosynthesis!"
        )
        suggested = ["Add Monstera to garden", "Monstera watering schedule", "Diagnose leaf spots"]

    elif any(k in msg_lower for k in ["snake plant", "sansevieria"]):
        reply = (
            "🌿 **Snake Plant Care:**\n\n"
            "• **Hardiness:** One of the most resilient indoor plants available.\n"
            "• **Light:** Tolerates low shade to bright sunny windows.\n"
            "• **Watering:** Water sparingly every 2-3 weeks. Allow soil to dry 100% between drinks.\n"
            "• **Warning:** Overwatering is the only thing that hurts a snake plant."
        )
        suggested = ["Low light plants", "Watering reminder", "Explore Plants"]

    else:
        reply = (
            f"Thanks for asking about that! For healthy plants, always balance three key elements: **adequate light**, "
            "**well-draining soil**, and **consistent watering based on soil dryness** rather than a rigid calendar.\n\n"
            "Would you like specific advice for a particular plant species or to diagnose a symptom?"
        )
        suggested = ["Identify a plant", "Diagnose symptoms", "Care guides", "Explore Plants"]

    return {
        "reply": reply,
        "suggested_followups": suggested,
        "ai_source": "GreenMate Botanical Conversational AI"
    }
