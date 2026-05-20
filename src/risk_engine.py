RISK_TERMS = {
    "High": [
        "terminate immediately",
        "without notice",
        "unlimited liability",
        "sole discretion",
        "penalty",
        "material breach",
        "no refund",
        "non-compete",
        "exclusive",
    ],
    "Medium": [
        "termination",
        "liability",
        "indemnification",
        "warranty",
        "assignment",
        "confidentiality",
        "governing law",
        "breach",
    ],
    "Low": [
        "renewal",
        "notice",
        "payment",
        "invoice",
        "term",
    ],
}


def score_risk(text: str) -> dict:
    lower_text = text.lower()

    high_count = sum(lower_text.count(term) for term in RISK_TERMS["High"])
    medium_count = sum(lower_text.count(term) for term in RISK_TERMS["Medium"])
    low_count = sum(lower_text.count(term) for term in RISK_TERMS["Low"])

    score = (high_count * 12) + (medium_count * 5) + (low_count * 2)
    score = min(score, 100)

    if score >= 75 or high_count >= 4:
        level = "High"
    elif score >= 35 or medium_count >= 4:
        level = "Medium"
    else:
        level = "Low"

    return {
        "Risk Level": level,
        "Risk Score": score,
        "High Risk Terms": high_count,
        "Medium Risk Terms": medium_count,
        "Low Risk Terms": low_count,
    }


def risk_summary(risk_result: dict) -> str:
    level = risk_result["Risk Level"]
    score = risk_result["Risk Score"]

    if level == "High":
        return (
            f"High risk detected with a score of {score}/100. "
            "The document contains strong risk indicators such as strict termination, liability, penalty, exclusivity, or breach-related language."
        )

    if level == "Medium":
        return (
            f"Medium risk detected with a score of {score}/100. "
            "The document contains important clauses that should be reviewed carefully, including termination, liability, confidentiality, governing law, or indemnity."
        )

    return (
        f"Low risk detected with a score of {score}/100. "
        "The document has fewer risk indicators based on the current automated scan."
    )
