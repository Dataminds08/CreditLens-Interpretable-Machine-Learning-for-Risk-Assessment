import psycopg2
import pandas as pd
from src.fraud_detection_rules import FraudDetector

conn = psycopg2.connect(
    host="db.ekdyztchhvjkqdqzpqcf.supabase.co",
    database="postgres",
    user="postgres",
    password="postgres@123",
    port="5432"
)

# Example: Read data into a pandas DataFrame
query = "SELECT * FROM transactions;"
df = pd.read_sql(query, conn)

print(df.head())

f=FraudDetector(df)
f.apply_all_rules()
