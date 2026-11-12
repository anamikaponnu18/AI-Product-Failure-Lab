
import re


def extract_product_price(product_text):
    """Extract a price when it is explicitly mentioned in the description."""

    patterns = [
        r"₹\s*([\d,]+(?:\.\d+)?)",
        r"Rs\.?\s*([\d,]+(?:\.\d+)?)",
        r"INR\s*([\d,]+(?:\.\d+)?)",
    ]

    for pattern in patterns:
        match = re.search(pattern, product_text, re.IGNORECASE)

        if match:
            return float(match.group(1).replace(",", ""))

    return None


def evaluate_persona(persona, product):

    product_text = str(product).lower()

    score = 5.0
    positives = []
    concerns = []
    improvements = []

    # Persona details
    age = persona.get("age", 25)
    occupation = persona.get("occupation", "")
    budget = persona.get("budget", 5000)
    archetype = persona.get("archetype", "Practical Buyer")

    personality = persona.get("big_five", {})
    preferences = persona.get("preferences", [])

    buying = persona.get("buying_behaviour", {})

    price_sensitivity = buying.get(
        "price_sensitivity", "Medium"
    )

    decision_style = buying.get(
        "decision_style", "Analytical"
    )

    # ------------------------------------------------
    # 1. PRICE AND AFFORDABILITY
    # ------------------------------------------------

    product_price = extract_product_price(product_text)

    if product_price is not None and budget > 0:

        affordability_ratio = budget / product_price

        if affordability_ratio >= 2:
            score += 1.5
            positives.append(
                "The product is comfortably within the consumer's budget."
            )

        elif affordability_ratio >= 1:
            score += 0.75
            positives.append(
                "The consumer can afford the product within their budget."
            )

        elif affordability_ratio >= 0.5:
            score -= 0.75
            concerns.append(
                "The product may be expensive relative to the consumer's budget."
            )

        else:
            score -= 1.75
            concerns.append(
                "The product price is significantly higher than the consumer's budget."
            )

        # Price sensitivity
        if price_sensitivity == "High" and affordability_ratio < 1.5:
            score -= 0.75
            concerns.append(
                "The consumer is highly sensitive to product pricing."
            )

        elif price_sensitivity == "Low" and affordability_ratio >= 1:
            score += 0.25

    else:
        concerns.append(
            "The product price is not clearly mentioned, so affordability cannot be assessed accurately."
        )
        improvements.append(
            "Mention the product price to improve affordability evaluation."
        )

    # ------------------------------------------------
    # 2. PREFERENCE MATCHING
    # ------------------------------------------------

    preference_keywords = {
        "technology": [
            "smart", "digital", "technology", "automated",
            "sensor", "app", "electronic"
        ],
        "quality": [
            "quality", "premium", "reliable", "well-made"
        ],
        "durability": [
            "durable", "long-lasting", "strong", "sturdy"
        ],
        "convenience": [
            "convenient", "easy", "portable", "reminder",
            "automatic", "user-friendly"
        ],
        "eco-friendly": [
            "eco-friendly", "biodegradable", "sustainable",
            "reusable", "environment", "plant-based"
        ],
        "safety": [
            "safety", "safe", "secure", "protection"
        ],
        "innovation": [
            "innovative", "innovation", "smart", "advanced",
            "unique", "technology"
        ],
        "fashion": [
            "fashion", "stylish", "design", "appearance"
        ],
        "affordable": [
            "affordable", "budget-friendly", "low-cost",
            "economical"
        ],
        "simplicity": [
            "simple", "easy", "basic", "convenient"
        ],
        "design": [
            "design", "stylish", "appearance", "modern"
        ],
        "premium": [
            "premium", "luxury", "high-end", "exclusive"
        ]
    }

    matched_preferences = []

    for preference in preferences:

        keywords = preference_keywords.get(
            str(preference).lower(),
            [str(preference).lower()]
        )

        if any(keyword in product_text for keyword in keywords):
            matched_preferences.append(preference)

    if matched_preferences:
        preference_score = min(
            len(matched_preferences) * 0.5, 1.5
        )

        score += preference_score

        positives.append(
            "The product matches consumer preferences: "
            + ", ".join(matched_preferences)
            + "."
        )

    else:
        score -= 0.75

        concerns.append(
            "The product does not strongly match this consumer's stated preferences."
        )

        improvements.append(
            "Highlight features that match different consumer preferences."
        )

    # ------------------------------------------------
    # 3. CONSUMER ARCHETYPE
    # ------------------------------------------------

    if archetype == "Early Adopter":

        if any(word in product_text for word in [
            "smart", "technology", "innovative",
            "digital", "advanced"
        ]):
            score += 0.75
            positives.append(
                "The innovative features may attract early adopters."
            )

    elif archetype == "Budget Conscious":

        if product_price is not None and product_price > budget:
            score -= 0.5
            concerns.append(
                "The price may discourage budget-conscious consumers."
            )

    elif archetype == "Quality Seeker":

        if any(word in product_text for word in [
            "quality", "durable", "reliable", "premium"
        ]):
            score += 0.75
            positives.append(
                "The product highlights features valued by quality-conscious buyers."
            )

    elif archetype == "Eco Conscious":

        if any(word in product_text for word in [
            "eco-friendly", "biodegradable", "sustainable",
            "reusable", "environment"
        ]):
            score += 0.75
            positives.append(
                "The sustainable features may attract environmentally conscious consumers."
            )

    elif archetype == "Risk Averse":

        if any(word in product_text for word in [
            "safe", "reliable", "tested", "warranty",
            "certified", "secure"
        ]):
            score += 0.5
            positives.append(
                "Safety and reliability information may build consumer confidence."
            )

        else:
            score -= 0.5
            concerns.append(
                "The cautious consumer may need more evidence of product reliability."
            )

    elif archetype == "Trend Follower":

        if any(word in product_text for word in [
            "trending", "modern", "smart", "stylish",
            "innovative", "fashion"
        ]):
            score += 0.5

    elif archetype == "Practical Buyer":

        if any(word in product_text for word in [
            "convenient", "useful", "practical",
            "durable", "easy"
        ]):
            score += 0.5

    # ------------------------------------------------
    # 4. PERSONALITY-BASED EVALUATION
    # ------------------------------------------------

    openness = personality.get("openness", 0.5)
    conscientiousness = personality.get(
        "conscientiousness", 0.5
    )
    extraversion = personality.get("extraversion", 0.5)
    agreeableness = personality.get("agreeableness", 0.5)
    neuroticism = personality.get("neuroticism", 0.5)

    innovative = any(word in product_text for word in [
        "smart", "innovative", "technology", "digital",
        "advanced", "unique"
    ])

    practical = any(word in product_text for word in [
        "convenient", "durable", "useful", "easy",
        "reusable", "efficient"
    ])

    sustainable = any(word in product_text for word in [
        "eco-friendly", "sustainable", "biodegradable",
        "reusable", "environment"
    ])

    safe = any(word in product_text for word in [
        "safe", "safety", "secure", "reliable",
        "tested", "certified"
    ])

    if openness > 0.7 and innovative:
        score += 0.5
        positives.append(
            "The consumer's openness to new experiences supports interest in innovative features."
        )

    if conscientiousness > 0.7 and practical:
        score += 0.5
        positives.append(
            "The product's practical features may appeal to this organized consumer."
        )

    if extraversion > 0.7 and any(word in product_text for word in [
        "social", "fashion", "trending", "stylish",
        "community"
    ]):
        score += 0.25

    if agreeableness > 0.7 and sustainable:
        score += 0.5
        positives.append(
            "The product's environmental benefits may appeal to this consumer."
        )

    if neuroticism > 0.7 and not safe:
        score -= 0.5
        concerns.append(
            "The consumer may hesitate without clear safety and reliability information."
        )

    # ------------------------------------------------
    # 5. AGE AND OCCUPATION SUITABILITY
    # ------------------------------------------------

    audience_matches = []

    occupation_keywords = {
        "Student": ["student", "college", "school", "university"],
        "Working Professional": [
            "working professional", "office", "professional",
            "workplace", "employee"
        ],
        "Entrepreneur": [
            "business", "entrepreneur", "startup", "restaurant"
        ],
        "Freelancer": ["freelancer", "remote work", "work from home"],
        "Homemaker": ["household", "home", "family"],
        "Retired": ["senior", "elderly", "retired"]
    }

    relevant_keywords = occupation_keywords.get(
        occupation, []
    )

    if any(keyword in product_text for keyword in relevant_keywords):
        score += 0.75

        positives.append(
            "The product's intended audience matches the consumer's occupation."
        )

        audience_matches.append(occupation)

    # Age-related suitability
    if age < 18 and any(word in product_text for word in [
        "children", "kids", "teenagers"
    ]):
        score += 0.5

    elif 18 <= age <= 35 and any(word in product_text for word in [
        "young adults", "students", "young professionals"
    ]):
        score += 0.5

    elif age >= 60 and any(word in product_text for word in [
        "senior", "elderly", "older adults"
    ]):
        score += 0.5

    # ------------------------------------------------
    # 6. PRODUCT DESCRIPTION QUALITY
    # ------------------------------------------------

    if len(product_text) > 150:
        positives.append(
            "The product description provides a reasonable level of detail."
        )

    else:
        score -= 0.5
        concerns.append(
            "The product description lacks sufficient detail."
        )

        improvements.append(
            "Provide more information about product features and benefits."
        )

    if not any(word in product_text for word in [
        "benefit", "designed", "helps", "aims",
        "improve", "provides", "reduces"
    ]):
        improvements.append(
            "Explain the main problem the product solves for consumers."
        )

    if not any(word in product_text for word in [
        "quality", "durable", "reliable", "tested",
        "warranty", "certified"
    ]):
        improvements.append(
            "Provide more information about product quality and reliability."
        )

    # ------------------------------------------------
    # 7. FINAL SCORE AND PREDICTION
    # ------------------------------------------------

    score = round(max(1, min(10, score)), 1)

    if score >= 7:
        stance = "Positive"
        adoption = "High"

    elif score >= 4:
        stance = "Mixed"
        adoption = "Medium"

    else:
        stance = "Negative"
        adoption = "Low"

    if not improvements:
        improvements.append(
            "Continue improving the product based on consumer feedback."
        )

    reasoning = (
        f"This persona belongs to the {archetype} category. "
        f"The estimated interest score is {score}/10. "
        f"The evaluation considers affordability, preferences, "
        f"personality, buying behaviour and product suitability."
    )

    return {
        "interest_score": score,
        "stance": stance,
        "adoption_likelihood": adoption,
        "positives": positives,
        "concerns": concerns,
        "improvements": improvements,
        "reasoning": reasoning,
        "persona": persona
    }
