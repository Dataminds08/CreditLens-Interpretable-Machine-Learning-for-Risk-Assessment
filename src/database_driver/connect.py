import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="db.ekdyztchhvjkqdqzpqcf.supabase.co",
    database="postgres",
    user="postgres",
    password="postgres@123",
    port="5432"
)

# Example: Read data into a pandas DataFrame
query = "SELECT * FROM transactions LIMIT 10;"
df = pd.read_sql(query, conn)
print(df.head())
