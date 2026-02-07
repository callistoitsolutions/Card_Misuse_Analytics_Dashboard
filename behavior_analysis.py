def customer_average(df):
    return df.groupby("customer_id")["amount"].mean()
