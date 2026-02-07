from ingestion.file_uploader import load_file
from analytics.risk_engine import assign_risk
from database.db_loader import load_to_db

file_path = "data/raw/sample_transactions.xlsx"

df = load_file(file_path)
df = assign_risk(df)
load_to_db(df, "sample_transactions.xlsx")

print("Pipeline executed successfully")
