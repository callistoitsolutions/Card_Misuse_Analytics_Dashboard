import pandas as pd

def clean_data(df):
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    if 'is_fraud' not in df.columns:
        df['is_fraud'] = 0

    df.dropna(subset=['transaction_id', 'amount'], inplace=True)
    return df
