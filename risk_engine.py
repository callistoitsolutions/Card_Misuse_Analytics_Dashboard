import yaml

def assign_risk(df):
    required = {"customer_id", "amount"}

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Risk engine missing required columns: {missing}")

    with open("config/rules.yaml") as f:
        rules = yaml.safe_load(f)

    avg = df.groupby("customer_id")["amount"].mean()

    df["_unusual"] = df["amount"] > (
        df["customer_id"].map(avg) * rules["unusual_multiplier"]
    )

    def classify(row):
        if row.get("is_fraud", 0) == 1 and row["_unusual"]:
            return "High Risk"
        elif row["_unusual"]:
            return "Medium Risk"
        return "Normal"

    df["risk_level"] = df.apply(classify, axis=1)

    df.drop(columns=["_unusual"], inplace=True)

    return df
