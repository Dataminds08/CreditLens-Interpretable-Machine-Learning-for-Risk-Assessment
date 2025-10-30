import pandas as pd

class FraudDetector:
    def __init__(self, df):
        self.df = df.copy()

    def check_duplicate_transaction(self):
        """Rule 1: Duplicate transaction from same customer at same time"""
        self.df['rule_duplicate'] = self.df.duplicated(
            subset=['customer_id', 'timestamp'], keep=False).astype(int)

    def check_multiple_same_amount(self, seconds=10):
        """Rule 2: n transactions same amount within 10 seconds from same customer & merchant"""
        self.df = self.df.sort_values(by=['customer_id', 'merchant_id', 'timestamp'])
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['rule_same_amount'] = 0

        for i in range(1, len(self.df)):
            prev = self.df.iloc[i - 1]
            curr = self.df.iloc[i]
            if (curr['customer_id'] == prev['customer_id'] and
                curr['merchant_id'] == prev['merchant_id'] and
                curr['amount'] == prev['amount'] and
                (curr['timestamp'] - prev['timestamp']).total_seconds() <= seconds):
                self.df.loc[self.df.index[i], 'rule_same_amount'] = 1

    def check_invalid_customer_info(self):
        """Rule 3: Invalid email or phone"""
        self.df['rule_invalid_customer'] = (
            ~self.df['email'].str.contains('@') |
            ~self.df['phone'].str.match(r'^\d{10}$')
        ).astype(int)

    def check_invalid_merchant(self):
        """Rule 4: Invalid merchant name/details"""
        self.df['rule_invalid_merchant'] = (
            self.df['merchant_name'].isna() |
            (self.df['merchant_name'].str.len() < 3)
        ).astype(int)

    def check_multiple_failures(self, minutes=10):
        """Rule 5: More than 3 failures within 10 minutes"""
        self.df = self.df.sort_values(by=['customer_id', 'timestamp'])
        self.df['rule_multiple_failures'] = 0
        for i in range(len(self.df)):
            subset = self.df[
                (self.df['customer_id'] == self.df.loc[i, 'customer_id']) &
                (self.df['status'] == 'failed') &
                (abs((self.df['timestamp'] - self.df.loc[i, 'timestamp']).dt.total_seconds()) <= minutes * 60)
            ]
            if len(subset) > 3:
                self.df.loc[self.df.index[i], 'rule_multiple_failures'] = 1

    def check_cash_transaction(self):
        """Rule 6: Transaction type is Cash"""
        self.df['rule_cash_transaction'] = (
            self.df['type'].str.lower() == 'cash'
        ).astype(int)

    def apply_all_rules(self):
        self.check_duplicate_transaction()
        self.check_multiple_same_amount()
        self.check_invalid_customer_info()
        self.check_invalid_merchant()
        self.check_multiple_failures()
        self.check_cash_transaction()
        return self.df