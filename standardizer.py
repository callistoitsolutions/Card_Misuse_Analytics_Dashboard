import yaml
import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "amount"
]

def standardize_columns(df):
    with open("config/column_mapping.yaml") as f:
        mapping = yaml.safe_load(f)

    df.columns = [c.lower().strip() for c in df.columns]

    new_df = pd.DataFrame()

    for standard_col, variants in mapping.items():
        for col in df.columns:
            if col in variants:
                new_df[standard_col] = df[col]
                break

    # 🔴 VALIDATION STEP (THIS FIXES YOUR ERROR)
    missing = [col for col in REQUIRED_COLUMNS if col not in new_df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns after standardization: {missing}. "
            f"Check column_mapping.yaml or uploaded file headers."
        )

    return new_df
