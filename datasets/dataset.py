import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

# Number of rows
c = 5000
m = 5000
t = 100000

# -------------------------
# Shared Fields (Customers & Merchants)
# -------------------------
locations = ["New York", "Los Angeles", "Chicago", "Houston", "Miami", 
             "Seattle", "Boston", "Dallas", "Denver", "Atlanta"]

# -------------------------
# Customers dataset
# -------------------------
customers = pd.DataFrame({
    "Customers_ID": range(1, c + 1),
    "Name": [fake.name() for _ in range(c)],
    "Email": [fake.email() for _ in range(c)],
    "Phone": [fake.msisdn()[:10] for _ in range(c)],
    "City": np.random.choice(locations, size=c),
    "Customer_Types_code": np.random.choice(["REG", "PREM", "VIP"], size=c)
})

# -------------------------
# Merchants dataset
# -------------------------
merchants = pd.DataFrame({
    "Merchant_ID": range(1, m + 1),
    "Name": [fake.company() for _ in range(m)],
    "Email": [fake.company_email() for _ in range(m)],
    "Phone": [fake.msisdn()[:10] for _ in range(m)],
    "City": np.random.choice(locations, size=m)
})

# -------------------------
# Transactions dataset
# -------------------------
payment_methods = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash"]
transaction_statuses = ["Completed", "Pending", "Failed", "Refunded"]
transaction_types = ["Purchase", "Refund", "Subscription", "Transfer"]

transactions = pd.DataFrame({
    "Transaction_ID": range(1, t + 1),
    "time_stamp": [
        fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        for _ in range(t)
    ],
    "amount_of_transaction": np.round(np.random.uniform(10.0, 5000.0, t), 2),
    "method_of_payment": np.random.choice(payment_methods, size=t),
    "transaction_status": np.random.choice(transaction_statuses, size=t),
    "transaction_type": np.random.choice(transaction_types, size=t),
    "Customers_ID": np.random.randint(1, t + 1, t),
    "Merchant_ID": np.random.randint(1, t + 1, t)
})

# -------------------------
# Save to CSV
# -------------------------
customers.to_csv("Customers.csv", index=False)
merchants.to_csv("Merchants.csv", index=False)
transactions.to_csv("Transactions.csv", index=False)

print("✅ CSV files created successfully:")
print("   - Customers.csv")
print("   - Merchants.csv")
print("   - Transactions.csv (with payment, status, and type fields)")
