import pandas as pd


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def build_processing_summary(
    file_count: int,
    chunk_count: int,
    entity_count: int,
    clause_count: int,
    retrieval_method: str,
) -> pd.DataFrame:
    rows = [
        {"Metric": "Documents Processed", "Value": file_count},
        {"Metric": "Text Chunks Created", "Value": chunk_count},
        {"Metric": "Entities Extracted", "Value": entity_count},
        {"Metric": "Clauses Classified", "Value": clause_count},
        {"Metric": "Retrieval Method", "Value": retrieval_method.upper()},
    ]

    return pd.DataFrame(rows)
