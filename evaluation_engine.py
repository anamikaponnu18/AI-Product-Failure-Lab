
def evaluate_persona(persona, product):
    """
    Evaluate a product from the perspective of a synthetic
    consumer persona using rule-based scoring.
    """

    score = 5.0
    positives = []
    concerns = []
    improvements = []

    product_text = str(product).lower()

    # Extract persona characteristics
    age = persona.get("age", 25)
    income = persona.get("income", "Medium")
    archetype = persona.get("archetype", "Practical Buyer")

    personality = persona.get("big_five", {})
    preferences = persona.get("preferences", [])

    # 1. Affordability evaluation
    price = persona.get("budget", 5000)

    if isinstance(price, (int, float)):
        if price >= 5000:
            score += 1
            positives.append("The product may fit the consumer's budget.")
        else:
            score -= 1
            concerns.append("The product may be expensive for this consumer.")

    # 2. Personality-based evaluation
    openness = personality.get("openness", 0.5)
    conscientiousness = personality.get("conscientiousness", 0.5)
    extraversion = personality.get("extraversion", 0.5)
    agreeableness = personality.get("agreeableness", 0.5)
    neuroticism = personality.get("neuroticism", 0.5)

    if openness > 0.7:
        score += 1
        positives.append("The consumer is open to trying new products.")

    if conscientiousness > 0.7:
        score += 0.5
        positives.append("The consumer values practical and well-planned purchases.")

    if neuroticism > 0.7:
        score -= 0.5
        concerns.append("The consumer may be cautious about purchasing unfamiliar products.")

    # 3. Consumer archetype evaluation
    archetype_scores = {
        "Budget Conscious": -0.5,
        "Trend Follower": 1,
        "Early Adopter": 1.5,
        "Practical Buyer": 0.5,
        "Brand Loyalist": -0.5,
        "Quality Seeker": 1,
        "Eco Conscious": 0.5,
        "Impulse Buyer": 1,
        "Risk Averse": -1,
        "Value Seeker": 0.5
    }

    score += archetype_scores.get(archetype, 0)

    # 4. Preference matching
    matched_preferences = [
        preference for preference in preferences
        if str(preference).lower() in product_text
    ]

    if matched_preferences:
        score += min(len(matched_preferences), 2)
        positives.append(
            "The product matches some of the consumer's preferences."
        )
    else:
        concerns.append(
            "The product description does not clearly match the consumer's preferences."
        )

    # 5. Product information evaluation
    if len(product_text) > 100:
        positives.append("The product description provides useful information.")
    else:
        concerns.append("The product description needs more details.")

    if "quality" in product_text:
        positives.append("Product quality is highlighted.")

    if "affordable" in product_text or "budget" in product_text:
        positives.append("Affordability is highlighted.")

    # 6. Final score
    score = max(1, min(10, round(score)))

    # Determine stance
    if score >= 7:
        stance = "Positive"
        adoption = "High"
    elif score >= 4:
        stance = "Mixed"
        adoption = "Medium"
    else:
        stance = "Negative"
        adoption = "Low"

    # Improvement suggestions
    if not improvements:
        improvements = [
            "Provide clearer product information.",
            "Consider customer affordability.",
            "Highlight the product's main benefits."
        ]

    # Generate explanation
    reasoning = (
        f"This persona belongs to the {archetype} category. "
        f"Their estimated interest score is {score}/10. "
        f"The evaluation considers personality traits, "
        f"consumer preferences and affordability."
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
