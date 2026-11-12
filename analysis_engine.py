
from collections import Counter


def summarize_results(results):

    # --------------------------------
    # CHECK EMPTY RESULTS
    # --------------------------------

    if not results:
        return {
            "average_interest": 0,
            "positive_pct": 0,
            "negative_pct": 0,
            "high_adoption_pct": 0,
            "stance_counts": {},
            "adoption_counts": {},
            "top_positives": [],
            "top_concerns": [],
            "top_improvements": [],
            "assessment": "No evaluation results available.",
            "risk_level": "Unknown"
        }

    total = len(results)

    # --------------------------------
    # INTEREST SCORE
    # --------------------------------

    scores = [
        result["interest_score"]
        for result in results
    ]

    average_interest = sum(scores) / total

    # --------------------------------
    # STANCE DISTRIBUTION
    # --------------------------------

    stance_counts = Counter(
        result["stance"]
        for result in results
    )

    positive_pct = (
        stance_counts.get("Positive", 0) / total
    ) * 100

    negative_pct = (
        stance_counts.get("Negative", 0) / total
    ) * 100

    # --------------------------------
    # ADOPTION LIKELIHOOD
    # --------------------------------

    adoption_counts = Counter(
        result["adoption_likelihood"]
        for result in results
    )

    high_adoption_pct = (
        adoption_counts.get("High", 0) / total
    ) * 100

    # --------------------------------
    # COMMON FEEDBACK
    # --------------------------------

    positives = []
    concerns = []
    improvements = []

    for result in results:

        positives.extend(
            result.get("positives", [])
        )

        concerns.extend(
            result.get("concerns", [])
        )

        improvements.extend(
            result.get("improvements", [])
        )

    top_positives = [
        item
        for item, count in Counter(positives).most_common(5)
    ]

    top_concerns = [
        item
        for item, count in Counter(concerns).most_common(5)
    ]

    top_improvements = [
        item
        for item, count in Counter(improvements).most_common(5)
    ]

    # --------------------------------
    # PRODUCT RISK ASSESSMENT
    # --------------------------------

    if average_interest >= 7 and negative_pct <= 25:

        assessment = (
            "The product demonstrates strong acceptance "
            "among simulated consumer personas. It shows "
            "promising potential, although real-world "
            "market validation is required."
        )

        risk_level = "Low"

    elif average_interest >= 5:

        assessment = (
            "The product demonstrates moderate acceptance. "
            "Some consumer groups may be interested, but "
            "improvements are needed to address concerns."
        )

        risk_level = "Medium"

    else:

        assessment = (
            "The product demonstrates relatively low acceptance "
            "among simulated personas. Significant improvements "
            "may be required before considering a market launch."
        )

        risk_level = "High"

    # --------------------------------
    # RETURN SUMMARY
    # --------------------------------

    return {
        "average_interest": round(average_interest, 2),
        "positive_pct": round(positive_pct, 2),
        "negative_pct": round(negative_pct, 2),
        "high_adoption_pct": round(high_adoption_pct, 2),
        "stance_counts": dict(stance_counts),
        "adoption_counts": dict(adoption_counts),
        "top_positives": top_positives,
        "top_concerns": top_concerns,
        "top_improvements": top_improvements,
        "assessment": assessment,
        "risk_level": risk_level
    }
