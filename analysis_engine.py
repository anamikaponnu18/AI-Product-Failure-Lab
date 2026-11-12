
# PRODUCT RISK ASSESSMENT

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
