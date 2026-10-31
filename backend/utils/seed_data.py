from typing import List, Dict, Any

SEED_PLANTS: List[Dict[str, Any]] = [
    {
        "_id": "plant_monstera_01",
        "name": "Monstera Deliciosa",
        "scientific_name": "Monstera deliciosa",
        "category": "Indoor Plants",
        "difficulty": "Easy",
        "sunlight": "Medium Light",
        "watering": "Water 1-2 times/week",
        "watering_interval_days": 5,
        "price": 499,
        "rating": 4.9,
        "reviews_count": 128,
        "image_url": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=800&q=80",
        "description": "Known as the Swiss Cheese Plant, Monstera Deliciosa is famous for its natural leaf-holes (fenestrations) and vibrant emerald green foliage. It purifies indoor air and brings an authentic tropical jungle vibe.",
        "soil_type": "Peat-based potting mix with perlite or orchid bark for superior drainage",
        "temperature_range": "18°C - 30°C (65°F - 85°F)",
        "humidity": "60% - 80% (misting recommended in dry seasons)",
        "care_instructions": [
            "Place in bright, filtered, indirect sunlight. Direct noon sun will scorch leaves.",
            "Water when the top 2-3 inches of soil feel dry to touch.",
            "Wipe leaves monthly with a damp cloth to remove dust and maximize photosynthesis.",
            "Provide a moss pole or trellis as aerial roots develop for vertical climbing."
        ]
    },
    {
        "_id": "plant_snake_02",
        "name": "Snake Plant",
        "scientific_name": "Sansevieria trifasciata",
        "category": "Indoor Plants",
        "difficulty": "Easy",
        "sunlight": "Low Light",
        "watering": "Water 1-2 times/week",
        "watering_interval_days": 10,
        "price": 399,
        "rating": 4.8,
        "reviews_count": 210,
        "image_url": "https://images.unsplash.com/photo-1593482892290-f54927ae1bf6?auto=format&fit=crop&w=800&q=80",
        "description": "Nearly indestructible and an exceptional air purifier, the Snake Plant (Mother-in-Law's Tongue) features upright, sword-like leaves with striking variegated gold and dark green bands.",
        "soil_type": "Fast-draining cactus or succulent blend",
        "temperature_range": "15°C - 32°C (60°F - 90°F)",
        "humidity": "Tolerates low humidity well (30% - 50%)",
        "care_instructions": [
            "Thrives in everything from dim bedroom corners to bright indirect sun.",
            "Water sparingly; allow soil to dry out completely between waterings.",
            "Avoid letting water sit in the center rosette to prevent crown rot.",
            "Fertilize once in spring and once in mid-summer with diluted houseplant feed."
        ]
    },
    {
        "_id": "plant_peace_lily_03",
        "name": "Peace Lily",
        "scientific_name": "Spathiphyllum wallisii",
        "category": "Flowers",
        "difficulty": "Moderate",
        "sunlight": "Medium Light",
        "watering": "Water 2-3 times/week",
        "watering_interval_days": 3,
        "price": 599,
        "rating": 4.7,
        "reviews_count": 94,
        "image_url": "https://images.unsplash.com/photo-1593691509543-c55fb32e7355?auto=format&fit=crop&w=800&q=80",
        "description": "Peace Lilies produce elegant white blooms and glossy, deep green foliage. They communicate their thirst clearly by drooping slightly when they need hydration, recovering quickly after watering.",
        "soil_type": "Rich, porous potting mix containing peat moss and vermiculite",
        "temperature_range": "18°C - 26°C (65°F - 80°F)",
        "humidity": "50% - 70%",
        "care_instructions": [
            "Keep soil consistently moist but never soggy.",
            "Sensitive to tap water chemicals; use filtered or rested room-temperature water.",
            "Maintain medium to bright indirect light to encourage recurring white blooms.",
            "Keep away from cold drafty windows and heating vents."
        ]
    },
    {
        "_id": "plant_lavender_04",
        "name": "Lavender",
        "scientific_name": "Lavandula angustifolia",
        "category": "Herbs",
        "difficulty": "Moderate",
        "sunlight": "Full Sun",
        "watering": "Water 1-2 times/week",
        "watering_interval_days": 6,
        "price": 449,
        "rating": 4.9,
        "reviews_count": 87,
        "image_url": "https://images.unsplash.com/photo-1528183429752-a97d0bf99b5a?auto=format&fit=crop&w=800&q=80",
        "description": "Celebrated worldwide for its soothing aroma and calming purple flower spikes. English Lavender is a beloved Mediterranean perennial that attracts pollinating bees and butterflies.",
        "soil_type": "Sandy, lean, alkaline soil with excellent drainage",
        "temperature_range": "15°C - 30°C (60°F - 86°F)",
        "humidity": "Low humidity (30% - 40%)",
        "care_instructions": [
            "Requires at least 6 to 8 hours of direct, unfiltered sunlight daily.",
            "Let soil dry thoroughly between waterings; overwatering is the #1 danger.",
            "Prune lightly after the main bloom flush in late summer to stimulate compact growth.",
            "Ensure container pots have generous drainage holes."
        ]
    },
    {
        "_id": "plant_aloe_05",
        "name": "Aloe Vera",
        "scientific_name": "Aloe barbadensis miller",
        "category": "Succulents",
        "difficulty": "Easy",
        "sunlight": "Full Sun",
        "watering": "Water 1-2 times/week",
        "watering_interval_days": 12,
        "price": 349,
        "rating": 4.9,
        "reviews_count": 340,
        "image_url": "https://images.unsplash.com/photo-1567689265664-1c48de61db0b?auto=format&fit=crop&w=800&q=80",
        "description": "A must-have medicinal succulent containing nutrient-rich cooling gel within thick serrated leaves. Known for treating burns, soothing skin, and thriving with minimal maintenance.",
        "soil_type": "Gritty, gravelly cactus potting mix",
        "temperature_range": "13°C - 27°C (55°F - 80°F)",
        "humidity": "Tolerates low humidity well",
        "care_instructions": [
            "Position on a sunny south or west facing windowsill.",
            "Drench thoroughly, then allow soil to dry out 100% before the next watering.",
            "Reduce watering to once a month during cold winter months.",
            "Repot every 2-3 years as pups (offsets) emerge around the mother plant."
        ]
    },
    {
        "_id": "plant_basil_06",
        "name": "Sweet Basil",
        "scientific_name": "Ocimum basilicum",
        "category": "Herbs",
        "difficulty": "Easy",
        "sunlight": "Full Sun",
        "watering": "Water 2-3 times/week",
        "watering_interval_days": 3,
        "price": 249,
        "rating": 4.8,
        "reviews_count": 115,
        "image_url": "https://images.unsplash.com/photo-1618164436241-4473940d1f5c?auto=format&fit=crop&w=800&q=80",
        "description": "The quintessential culinary herb. Sweet Basil provides tender, aromatic leaves perfect for fresh pestos, Italian sauces, and botanical tea infusions.",
        "soil_type": "Nutrient-rich, well-draining loamy garden soil",
        "temperature_range": "20°C - 32°C (68°F - 90°F)",
        "humidity": "40% - 60%",
        "care_instructions": [
            "Loves warm temperatures and at least 6 hours of bright direct sun.",
            "Pinch off flower buds immediately to keep the plant bushy and flavorful.",
            "Water deeply at the base to keep leaves dry and prevent fungal mildew.",
            "Harvest top leaf pairs regularly to trigger vigorous branching."
        ]
    },
    {
        "_id": "plant_tomato_07",
        "name": "Cherry Tomato Bush",
        "scientific_name": "Solanum lycopersicum var. cerasiforme",
        "category": "Vegetable Plants",
        "difficulty": "Moderate",
        "sunlight": "Full Sun",
        "watering": "Water 2-3 times/week",
        "watering_interval_days": 2,
        "price": 380,
        "rating": 4.9,
        "reviews_count": 89,
        "image_url": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=800&q=80",
        "description": "Prolific and sweet, cherry tomato plants thrive in patio planters or sunny garden beds, producing continuous clusters of juicy, bite-sized red fruits all season.",
        "soil_type": "Rich organic compost mixed with fertile loam",
        "temperature_range": "21°C - 30°C (70°F - 85°F)",
        "humidity": "50% - 70%",
        "care_instructions": [
            "Requires at least 6-8 hours of direct sunshine every day.",
            "Keep moisture regular and consistent to prevent blossom end rot and skin splitting.",
            "Support growing stems with a sturdy tomato cage or wooden stake.",
            "Feed bi-weekly with balanced organic potassium and calcium tomato fertilizer."
        ]
    },
    {
        "_id": "plant_tulsi_08",
        "name": "Holy Basil (Tulsi)",
        "scientific_name": "Ocimum tenuiflorum",
        "category": "Medicinal Plants",
        "difficulty": "Easy",
        "sunlight": "Full Sun",
        "watering": "Water 1-2 times/week",
        "watering_interval_days": 4,
        "price": 299,
        "rating": 5.0,
        "reviews_count": 412,
        "image_url": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=800&q=80",
        "description": "Venerated for thousands of years as an Ayurvedic adaptogen. Tulsi purifies surrounding air, boosts respiratory immunity, and emits a sacred herbal aroma.",
        "soil_type": "Well-drained fertile garden soil rich in vermicompost",
        "temperature_range": "20°C - 35°C (68°F - 95°F)",
        "humidity": "Moderate to high",
        "care_instructions": [
            "Place in a warm, sunny location receiving minimum 4-6 hours of sunshine.",
            "Water when top inch of soil is dry. Avoid water stagnation.",
            "Prune top leaves regularly to promote bushier lateral growth.",
            "Protect from extreme winter frosts."
        ]
    },
    {
        "_id": "plant_bonsai_09",
        "name": "Ficus Bonsai Tree",
        "scientific_name": "Ficus retusa",
        "category": "Trees",
        "difficulty": "Moderate",
        "sunlight": "Medium Light",
        "watering": "Water 1-2 times/week",
        "watering_interval_days": 4,
        "price": 899,
        "rating": 4.9,
        "reviews_count": 76,
        "image_url": "https://images.unsplash.com/photo-1512428813834-c702c7702b78?auto=format&fit=crop&w=800&q=80",
        "description": "A magnificent miniature tree with exposed aerial banyan roots and deep green polished leaves. Perfect living art piece symbolizing tranquility, patience, and balance.",
        "soil_type": "Specialized bonsai akadama and pumice substrate",
        "temperature_range": "16°C - 28°C (60°F - 82°F)",
        "humidity": "50% - 70%",
        "care_instructions": [
            "Position in bright indirect light; can tolerate morning direct sun.",
            "Never allow root ball to dry out completely. Water thoroughly until it drains out.",
            "Prune shoots back to 2 leaves once they have grown 6-8 leaves to preserve shape.",
            "Mist leaves periodically to encourage aerial root development."
        ]
    },
    {
        "_id": "plant_bougainvillea_10",
        "name": "Bougainvillea",
        "scientific_name": "Bougainvillea spectabilis",
        "category": "Outdoor Plants",
        "difficulty": "Easy",
        "sunlight": "Full Sun",
        "watering": "Water 1-2 times/week",
        "watering_interval_days": 7,
        "price": 349,
        "rating": 4.8,
        "reviews_count": 92,
        "image_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=800&q=80",
        "description": "Dazzling outdoor ornamental vine that bursts into cascading waves of vibrant magenta-pink paper-like bracts. Drought tolerant once established and exceptionally hardy.",
        "soil_type": "Gritty, well-drained slightly acidic soil",
        "temperature_range": "18°C - 38°C (65°F - 100°F)",
        "humidity": "Tolerates dry conditions well",
        "care_instructions": [
            "Needs maximum full sun (6+ hours) to produce intense colorful blooms.",
            "Allow soil to dry between waterings. Withholding slight water can trigger heavy flowering.",
            "Prune back after blooming cycle to maintain desired trellis or bush form.",
            "Handle root system gently during transplanting as roots are fragile."
        ]
    }
]

SEED_GUIDES: List[Dict[str, Any]] = [
    {
        "_id": "guide_watering_01",
        "title": "Watering Techniques",
        "subtitle": "Learn the right way to water your plants",
        "category": "Hydration",
        "read_time": "5 min read",
        "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=800&q=80",
        "summary": "Mastering the fine balance between dehydration and overwatering is the single most critical skill for plant longevity.",
        "content": """### The Golden Rule of Plant Watering

More houseplants die from overwatering than from neglect. Overwatering suffocates root systems by displacing oxygen in the soil, leading to fatal anaerobic bacteria growth known as root rot.

#### 1. The Finger Test & Moisture Meter
Before reaching for the watering can, insert your index finger 2 inches into the potting soil.
- If it feels cool and damp with soil clinging to your skin, wait another 2–3 days.
- If it feels dry, crumbly, and warm, your plant is ready for a thorough drink.

#### 2. Deep Drenching vs Shallow Sips
Always water deeply until water flows freely from the container's bottom drainage holes. This ensures the entire root ball is hydrated and flushes out built-up fertilizer salts. Never leave standing water in the catch saucer for more than 20 minutes.

#### 3. Bottom Watering
For delicate foliage prone to fungal mildew (like African Violets, Begonias, or Calatheas), fill a shallow tray with 1 inch of water and set the pot inside for 15–20 minutes. The soil wicks moisture upward through capillary action directly to roots.

#### 4. Seasonal Adjustments
Plants drink significantly more during active spring and summer growth. When daylight hours shrink in autumn and winter, decrease watering frequency by 30% to 50%."""
    },
    {
        "_id": "guide_sunlight_02",
        "title": "Sunlight Requirements",
        "subtitle": "Find the perfect light for each plant",
        "category": "Lighting",
        "read_time": "6 min read",
        "image_url": "https://images.unsplash.com/photo-1509423350716-97f9360b4e09?auto=format&fit=crop&w=800&q=80",
        "summary": "Light is plant food. Understand the subtle differences between direct sun, bright indirect light, and low-light tolerances.",
        "content": """### Understanding the Spectrum of Plant Light

Light drives photosynthesis, the fundamental metabolic process converting carbon dioxide and water into glucose and oxygen.

#### 1. Direct Sunlight (6+ Hours)
- **Best Windows:** Unobstructed South or West-facing windows.
- **Ideal Plants:** Cacti, Succulents, Aloe Vera, Lavender, Herbs, and Citrus.
- **Signs of Excess:** Scorched brown spots, crispy bleached foliage.

#### 2. Bright Indirect Light (The Holy Grail)
- **Best Windows:** East-facing windows with soft morning sun, or South/West windows filtered through sheer curtains.
- **Ideal Plants:** Monstera Deliciosa, Fiddle Leaf Fig, Philodendrons, Pothos, Peace Lilies.
- **How to Test:** Hold your hand 12 inches above a piece of white paper. If you cast a sharp, clearly defined shadow with soft edges, you have ideal bright indirect light.

#### 3. Low Light (Tolerated, Not Preferred)
- **Best Locations:** North-facing windows or rooms 10–15 feet away from natural light sources.
- **Ideal Plants:** ZZ Plant, Snake Plant, Cast Iron Plant, Aglaonema.
- **Signs of Starvation:** Leggy, stretched stems, pale undersized leaves, slow or halted growth."""
    },
    {
        "_id": "guide_soil_03",
        "title": "Soil Preparation",
        "subtitle": "Create healthy soil for better growth",
        "category": "Substrate",
        "read_time": "4 min read",
        "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?auto=format&fit=crop&w=800&q=80",
        "summary": "The secret to thriving foliage begins beneath the surface with microbial life, porosity, and balanced pH.",
        "content": """### Crafting the Perfect Potting Medium

Garden dirt from your backyard is too dense and compact for potted plants. Potted roots require porous soil structure with microscopic air pockets.

#### The Universal Aroid & Foliage Recipe:
- **40% High-Grade Coco Coir or Peat Moss:** Retains balanced moisture without waterlogging.
- **25% Perlite or Pumice:** Creates air channels and stops soil compaction.
- **20% Orchid Pine Bark:** Mimics the natural tropical forest floor.
- **15% Aged Worm Castings:** Delivers beneficial biological enzymes and slow-release organic nutrients.

#### Soil pH Matters:
Most tropical houseplants flourish in slightly acidic to neutral soil (pH 6.0 to 6.8). Herbs like Rosemary and Lavender prefer slightly alkaline conditions (pH 7.0 to 7.5). Test using a simple soil pH strip before major repotting."""
    },
    {
        "_id": "guide_fertilizer_04",
        "title": "Fertilizer Guidance",
        "subtitle": "Feed your plants for stronger growth",
        "category": "Nutrition",
        "read_time": "5 min read",
        "image_url": "https://images.unsplash.com/photo-1584467735871-8e85353a8413?auto=format&fit=crop&w=800&q=80",
        "summary": "Demystifying N-P-K ratios, liquid vs slow-release feeds, and avoiding fertilizer leaf burn.",
        "content": """### Fueling Foliage and Blooms

Plants synthesize carbon from air and light, but rely on soil for macro-nutrients: Nitrogen (N), Phosphorus (P), and Potassium (K).

#### The N-P-K Code:
- **Nitrogen (N):** Promotes lush, deep green leafy foliage and vigorous stem growth.
- **Phosphorus (P):** Stimulates robust root development, flower buds, and fruit formation.
- **Potassium (K):** Strengthens cellular walls, immune resistance, and drought tolerance.

#### How to Feed Safely:
1. **Dilute to Half Strength:** Commercial fertilizers are concentrated. Always dilute to 50% recommended strength to avoid burning tender roots.
2. **Never Feed Dry Soil:** Always hydrate your plant with pure water first, then apply fertilizer solution 10 minutes later.
3. **Feed in Growing Season Only:** Fertilize every 2 to 4 weeks between March and September. Stop feeding during dormant winter months."""
    },
    {
        "_id": "guide_disease_05",
        "title": "Disease Prevention",
        "subtitle": "Keep your plants safe and healthy",
        "category": "Health",
        "read_time": "7 min read",
        "image_url": "https://images.unsplash.com/photo-1598880940371-c756e015fea1?auto=format&fit=crop&w=800&q=80",
        "summary": "Proactive hygiene, airflow, quarantine protocols, and natural organic remedies for common plant ailments.",
        "content": """### Protecting Your Botanical Sanctuary

Prevention is 10 times easier than curing an entrenched pest outbreak or fungal infection.

#### 1. The 14-Day Quarantine Rule
Whenever you bring a new plant home from a nursery or grocery store, keep it isolated in a separate room for 14 days. Inspect leaf undersides, nodes, and soil for hidden spider mites, mealybugs, thrips, or fungus gnats.

#### 2. Air Circulation is Non-Negotiable
Stagnant, humid air creates a breeding ground for powdery mildew, black spot, and bacterial leaf blight. Position an oscillating fan on low speed nearby to gently stir air currents.

#### 3. Organic Neem Oil Spray Formula
- 1 Liter warm filtered water
- 1 Teaspoon cold-pressed 100% pure neem oil
- 1/2 Teaspoon mild organic liquid castile soap (acts as emulsifier)
Shake vigorously and spray undersides and tops of foliage every 10–14 days in the evening."""
    },
    {
        "_id": "guide_seasonal_06",
        "title": "Seasonal Plant Care",
        "subtitle": "Guide for changing seasons",
        "category": "Seasonal",
        "read_time": "5 min read",
        "image_url": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=800&q=80",
        "summary": "How to transition your indoor and outdoor botanical companions smoothly from spring through winter.",
        "content": """### Adapting to Nature's Rhythms

Indoor environments change drastically across the calendar year due to heating systems, air conditioning, and shifting solar angles.

#### Spring: The Awakening
- Begin repotting root-bound specimens into pots 1–2 inches larger.
- Resume gentle bi-weekly organic feeding.
- Trim off dead, yellowed, or spindly winter growth.

#### Summer: Peak Vigor
- Monitor moisture daily during heatwaves.
- Protect leaves near windowpanes from scorching mid-day rays.
- Group tropical plants together on pebble humidity trays.

#### Autumn: Preparing for Rest
- Bring outdoor container plants indoors before nighttime temperatures dip below 12°C (54°F).
- Treat with insecticidal soap before transitioning indoors.
- Gradually taper off fertilizer.

#### Winter: Dormancy Management
- Maximize available light by moving plants closer to south-facing windows.
- Run a cool-mist ultrasonic humidifier to counteract dry radiator heat.
- Keep foliage away from cold window glass and drafty door thresholds."""
    }
]

def seed_database(db):
    """Seed initial data if collections are empty."""
    plants_col = db.get_collection("plants")
    if plants_col.count_documents({}) == 0:
        for p in SEED_PLANTS:
            plants_col.insert_one(p)

    guides_col = db.get_collection("plant_guides")
    if guides_col.count_documents({}) == 0:
        for g in SEED_GUIDES:
            guides_col.insert_one(g)
