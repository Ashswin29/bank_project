import json 
import pandas as pd 
import datetime
import sys 

class StatementGenerator:

    def __init__(self, enable_logging = True):
        self.enable_logging = enable_logging

    def _log(self, message):
        if self.enable_logging:
            print(message)

    def modifying_amount(self, row):
        if row['type'] == 'D':
            return row['amount'] * 1
        else:
            return row['amount'] * -1


    def generate_account_statement(self, account_input, transactions_file, year_month_input_formatted):
        transactions_str = json.loads(transactions_file.read())

        if account_input in transactions_str.keys():
            print(f"Account {account_input} exists.")

            account_transactions_df = pd.json_normalize(transactions_str[account_input])
            account_transactions_df['date'] = pd.to_datetime(account_transactions_df['date'], format='%Y%m%d')
            account_transactions_df['month'] = account_transactions_df['date'].dt.to_period('M')

            print(account_transactions_df)

            if year_month_input_formatted in account_transactions_df['month'].values:

                account_transactions_df['year'] = account_transactions_df['date'].dt.to_period('Y')
                account_transactions_df['amount'] = account_transactions_df['amount'].astype(float)
                account_transactions_df = account_transactions_df.sort_values(by='date', ascending = True, inplace = False)
                account_transactions_df.rename(columns={"date": "transaction_date_start"}, inplace = True)
                account_transactions_df['transaction_date_end'] = account_transactions_df['transaction_date_start'].shift(-1).dt.date #- pd.Timedelta(days=1)
                account_transactions_df['transaction_date_end'] = account_transactions_df['transaction_date_end'].fillna(datetime.date(2100, 12, 31))
                account_transactions_df['transaction_date_end'] = pd.to_datetime(account_transactions_df['transaction_date_end'])
                account_transactions_df['amount'] = account_transactions_df.apply(self.modifying_amount, axis=1)
                account_transactions_df['balance'] = account_transactions_df['amount'].cumsum()

                new_column_order = ['transaction_date_start', 'transaction_date_end', 'amount', 'balance', 'month']
                account_transactions_df2 = account_transactions_df[new_column_order]

                self._log(f"Account transactions for {account_input}:\n{account_transactions_df2}")

                return account_transactions_df, account_transactions_df2
            else:
                print(f"No transactions found for account {account_input} in month {year_month_input_formatted}.")
                sys.exit(1)
        else:
            print(f"Account {account_input} does not exist.")
            sys.exit(1)

    def generate_interest_rules(self, interest_file):

        interest_str = json.loads(interest_file.read())
        interest_rule_df = pd.DataFrame(interest_str).T.reset_index()
        interest_rule_df.columns = ['date', 'rule_id', 'rate']
        interest_rule_df['date'] = pd.to_datetime(interest_rule_df['date'], format='%Y%m%d')
        interest_rule_df['month'] = interest_rule_df['date'].dt.to_period('M')
        interest_rule_df['year'] = interest_rule_df['date'].dt.to_period('Y')
        interest_rule_df['rate'] = interest_rule_df['rate'].astype(float)
        interest_rule_df = interest_rule_df.sort_values(by='date', ascending=True, inplace=False)
        interest_rule_df.rename(columns={"date": "interest_date_start"}, inplace = True)
        interest_rule_df['interest_date_end'] = interest_rule_df['interest_date_start'].shift(-1).dt.date #- pd.Timedelta(days=1)
        interest_rule_df['interest_date_end'] = interest_rule_df['interest_date_end'].fillna(datetime.date(2100, 12, 31))
        interest_rule_df['interest_date_end'] = pd.to_datetime(interest_rule_df['interest_date_end'])


        new_column_order = ['interest_date_start', 'interest_date_end', 'rule_id', 'rate', 'month']
        interest_rule_df = interest_rule_df[new_column_order]

        self._log(f"Interest rules:\n{interest_rule_df}")

        return interest_rule_df


    def cross_join_transactions_interest(self, account_transactions_df, interest_rule_df):
        merged = pd.merge(account_transactions_df, interest_rule_df, how='cross')
        mask = (merged['transaction_date_start'] <= merged['interest_date_end']) & \
               (merged['transaction_date_end'] >= merged['interest_date_start'])
        merged = merged.loc[mask]

        merged['period_start'] = merged[['transaction_date_start', 'interest_date_start']].max(axis=1)
        merged['period_end'] = merged[['transaction_date_end', 'interest_date_end']].min(axis=1) - pd.Timedelta(days=1)

        return merged
    
    def calculate_annualized_interest(self, merged, year_month_input_formatted):
        #now add the filter
        month_start = pd.Timestamp(year_month_input_formatted.start_time)
        month_end = pd.Timestamp(year_month_input_formatted.end_time)

        #same thought process of the mask fucntion provided by AI 
        mask2 = (merged['period_end'] >= month_start) & (merged['period_start'] <= month_end)
        merged_desired_month = merged.loc[mask2].copy()

        ending_balance = float(merged_desired_month.iloc[-1, merged_desired_month.columns.get_loc('balance')])
        if ending_balance < 0:
            self._log(f"Unable to compute interest since ending balance is negative: {ending_balance}")
            sys.exit(1)
        else:

            # then assign for the first rows period_start as first day of the month (only when the previous month has balance < 0) if not leave it as is
            # then assign for the last row the period_end as the last day of the month
            self._log(merged_desired_month[['period_start', 'period_end', 'amount', 'balance', 'rate']])

            # if this is the first ever transaction for the account and it doesnt start from the first day of the month, dont reassing the period_start, only reassign the period end
            if merged_desired_month.iloc[0]['period_end'] >= merged_desired_month.iloc[0]['period_start']:
                merged_desired_month.iloc[0, merged_desired_month.columns.get_loc('period_start')] = month_start#.date()
                merged_desired_month.iloc[-1, merged_desired_month.columns.get_loc('period_end')] = month_end#.date()
            else:
                merged_desired_month.iloc[-1, merged_desired_month.columns.get_loc('period_end')] = month_end#.date()

            #then compute the days in the period
            merged_desired_month['days_in_period'] = (merged_desired_month['period_end'] - merged_desired_month['period_start']).dt.days + 1 # calculate the number of days after assigning the first day and last day of the month
            self._log(merged_desired_month)

            merged_with_interest = merged_desired_month[merged_desired_month['days_in_period'] > 0].copy() #filter out 0 - these are days with multiple transactions - we take the last trasnaction for the day
            self._log(merged_with_interest)

            merged_with_interest['annualized_interest'] = merged_with_interest['balance'] * merged_with_interest['rate']/100 * merged_with_interest['days_in_period']
            merged_with_interest['annualized_interest_rate'] = merged_with_interest['balance'] * merged_with_interest['rate']/100 * merged_with_interest['days_in_period']/365

            self._log(merged_with_interest)

            self._log(f"The annualized interest for the month is: {merged_with_interest['annualized_interest'].sum()}")
            self._log(f"The annualized interest rate for the month is: {merged_with_interest['annualized_interest_rate'].sum()}")

            return merged_desired_month, merged_with_interest

    def display_account_statement(self, account_transactions_df, year_month_input_formatted, merged_desired_month, merged_with_interest):

        month_start = pd.Timestamp(year_month_input_formatted.start_time)
        month_end = pd.Timestamp(year_month_input_formatted.end_time)

        print_statement_df = account_transactions_df[['transaction_date_start', 'txn_id', 'type', 'amount', 'balance']]
        print_statement_df = print_statement_df.rename(columns={"transaction_date_start": "date"})

        print_statement_desired_month_df = print_statement_df[(print_statement_df['date'] >= month_start) & (print_statement_df['date'] <= month_end)].copy()

        header = "Date      | Txn ID           | Type | Amount   | Balance  "
        print(header)
        for index, row in print_statement_desired_month_df.iterrows():
            date_str = pd.to_datetime(row['date'], format='%Y%m%d').strftime('%Y%m%d')
            print(f"{date_str} | {row['txn_id']}       | {row['type']}    | {row['amount']:.2f}   | {row['balance']:.2f}")

        print(f"{month_end.date().strftime('%Y%m%d')} |                   | I    | {merged_with_interest['annualized_interest_rate'].sum():.2f}     | {(merged_desired_month.iloc[-1, merged_desired_month.columns.get_loc('balance')] + merged_with_interest['annualized_interest_rate'].sum()):.2f}")
