import re
import pandas as pd


BUSINESS_TERMS = {
    "Termination": ["termination", "terminate", "terminated", "expiration", "expiry"],
    "Payment": ["payment", "fees", "invoice", "billing", "amount", "payable", "paid"],
    "Confidentiality": ["confidential", "confidentiality", "non-disclosure", "nda"],
    "Liability": ["liability", "damages", "losses", "limitation of liability"],
    "Indemnity": ["indemnify", "indemnification", "hold harmless"],
    "Governing Law": ["governing law", "jurisdiction", "court", "laws of"],
    "Intellectual Property": ["intellectual property", "copyright", "trademark", "patent", "license"],
    "Assignment": ["assignment", "assign", "transfer"],
    "Renewal": ["renewal", "renew", "extension"],
    "Warranty": ["warranty", "warranties", "representations"],
}


def extract_pattern_entities(text: str) -> pd.DataFrame:
    patterns = {
        "Date": r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b",
        "Monetary Value": r"(?:₹|\$|USD|INR|Rs\.?)\s?\d[\d,]*(?:\.\d+)?",
        "Percentage": r"\b\d+(?:\.\d+)?\s?%",
        "Email": r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
    }

    rows = []
    for label, pattern in patterns.items():
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            rows.append(
                {
                    "Entity": match,
                    "Category": label,
                    "Extraction Method": "Pattern Matching",
                }
            )

    return pd.DataFrame(rows)


def extract_business_terms(text: str) -> pd.DataFrame:
    rows = []
    lower_text = text.lower()

    for category, terms in BUSINESS_TERMS.items():
        matched_terms = [term for term in terms if term.lower() in lower_text]
        if matched_terms:
            rows.append(
                {
                    "Entity": ", ".join(sorted(set(matched_terms))),
                    "Category": category,
                    "Extraction Method": "Domain Dictionary",
                }
            )

    return pd.DataFrame(rows)


def extract_entities(text: str) -> pd.DataFrame:
    frames = [
        extract_pattern_entities(text),
        extract_business_terms(text),
    ]

    frames = [df for df in frames if not df.empty]

    if not frames:
        return pd.DataFrame(columns=["Entity", "Category", "Extraction Method"])

    df = pd.concat(frames, ignore_index=True)
    return df.drop_duplicates().reset_index(drop=True)
