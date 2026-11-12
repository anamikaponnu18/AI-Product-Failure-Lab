
import random


def generate_personas(number=20, seed=42):

    random.seed(seed)

    # Consumer archetypes
    archetypes = [
        "Budget Conscious",
        "Trend Follower",
        "Early Adopter",
        "Practical Buyer",
        "Brand Loyalist",
        "Quality Seeker",
        "Eco Conscious",
        "Impulse Buyer",
        "Risk Averse",
        "Value Seeker"
    ]

    # Possible preferences
    preference_options = [
        "affordable",
        "quality",
        "technology",
        "convenience",
        "durability",
        "eco-friendly",
        "fashion",
        "innovation",
        "safety",
        "simplicity",
        "premium",
        "design"
    ]

    # Demographic options
    age_groups = [
        (18, 25),
        (26, 35),
        (36, 45),
        (46, 60),
        (61, 75)
    ]

    education_levels = [
        "High School",
        "Undergraduate",
        "Postgraduate",
        "Doctorate"
    ]

    occupations = [
        "Student",
        "Working Professional",
        "Entrepreneur",
        "Freelancer",
        "Homemaker",
        "Retired"
    ]

    income_levels = [
        "Low",
        "Medium",
        "High"
    ]

    personas = []

    for i in range(number):

        archetype = random.choice(archetypes)

        age_range = random.choice(age_groups)

        age = random.randint(
            age_range[0],
            age_range[1]
        )

        # Big Five personality traits
        big_five = {
            "openness": round(random.uniform(0, 1), 2),
            "conscientiousness": round(random.uniform(0, 1), 2),
            "extraversion": round(random.uniform(0, 1), 2),
            "agreeableness": round(random.uniform(0, 1), 2),
            "neuroticism": round(random.uniform(0, 1), 2)
        }

        # Generate consumer preferences
        preferences = random.sample(
            preference_options,
            k=random.randint(2, 4)
        )

        # Income and approximate spending budget
        income = random.choice(income_levels)

        if income == "Low":
            budget = random.randint(500, 3000)

        elif income == "Medium":
            budget = random.randint(3000, 15000)

        else:
            budget = random.randint(15000, 50000)

        persona = {
            "persona_id": i + 1,
            "age": age,
            "education": random.choice(education_levels),
            "occupation": random.choice(occupations),
            "income": income,
            "budget": budget,
            "archetype": archetype,
            "big_five": big_five,
            "preferences": preferences,
            "buying_behaviour": {
                "price_sensitivity": random.choice(
                    ["Low", "Medium", "High"]
                ),
                "purchase_frequency": random.choice(
                    ["Rare", "Occasional", "Frequent"]
                ),
                "decision_style": random.choice(
                    ["Emotional", "Analytical", "Spontaneous"]
                )
            }
        }

        personas.append(persona)

    return personas
