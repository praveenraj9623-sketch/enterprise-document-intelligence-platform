import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


TRAINING_EXAMPLES = [
    ("Either party may terminate this agreement upon thirty days written notice.", "Termination"),
    ("This agreement shall terminate automatically upon material breach.", "Termination"),
    ("The client shall pay all invoices within thirty days.", "Payment"),
    ("Fees are payable monthly according to the invoice.", "Payment"),
    ("Each party must keep confidential information secure.", "Confidentiality"),
    ("Confidential information shall not be disclosed to third parties.", "Confidentiality"),
    ("Neither party shall be liable for indirect damages.", "Liability"),
    ("Total liability shall not exceed the amount paid.", "Liability"),
    ("The supplier shall indemnify the customer against third party claims.", "Indemnity"),
    ("The party shall hold harmless and indemnify the other party.", "Indemnity"),
    ("This agreement is governed by the laws of New York.", "Governing Law"),
    ("Courts in the stated jurisdiction shall resolve disputes.", "Governing Law"),
    ("All intellectual property rights remain with the owner.", "Intellectual Property"),
    ("The license grants limited use of software.", "Intellectual Property"),
    ("No party may assign this agreement without written consent.", "Assignment"),
    ("This contract may be transferred to an affiliate.", "Assignment"),
    ("The agreement renews automatically for another year.", "Renewal"),
    ("The parties may extend the term by written agreement.", "Renewal"),
    ("The company warrants that services will be performed professionally.", "Warranty"),
    ("No additional warranties are provided.", "Warranty"),
    ("The parties agree to cooperate in good faith.", "General"),
    ("This document contains general commercial terms.", "General"),
]


def build_classifier() -> Pipeline:
    texts = [x[0] for x in TRAINING_EXAMPLES]
    labels = [x[1] for x in TRAINING_EXAMPLES]

    model = Pipeline(
        [
            ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2))),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )

    model.fit(texts, labels)
    return model


def classify_chunks(chunks: list[str]) -> pd.DataFrame:
    if not chunks:
        return pd.DataFrame(
            columns=["Chunk ID", "Predicted Clause", "Confidence", "Text Preview"]
        )

    model = build_classifier()
    predictions = model.predict(chunks)
    probabilities = model.predict_proba(chunks).max(axis=1)

    rows = []
    for idx, chunk in enumerate(chunks):
        rows.append(
            {
                "Chunk ID": idx,
                "Predicted Clause": predictions[idx],
                "Confidence": round(float(probabilities[idx]), 3),
                "Text Preview": chunk[:300] + "...",
            }
        )

    return pd.DataFrame(rows)
