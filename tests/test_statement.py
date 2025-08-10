import pytest
import json 
import pandas as pd
from io import StringIO
from bank.statement import StatementGenerator

class TestStatementGenerator:

    def setup_method(self):
        self.sg = StatementGenerator(enable_logging=True)

    def test_annualized_interest_rate_AC001_202305(self):
        
        # AC001 transactions for May 2023
        ac001_transactions = {"AC001": [
            {"date": "20230501", "txn_id": "20230501-01", "type": "D", "amount": "100.00"},
            {"date": "20230601", "txn_id": "20230601-01", "type": "D", "amount": "150.00"},
            {"date": "20230626", "txn_id": "20230626-01", "type": "W", "amount": "20.00"},
            {"date": "20230626", "txn_id": "20230626-02", "type": "W", "amount": "100.00"},
            {"date": "20230726", "txn_id": "20230726-01", "type": "D", "amount": "350.00"}
        ]}

        # Interest rules applicable for May 2023 
        interest_rules = {
            "20230101": {"ruleid": "RULE01", "rate": 1.95},  # Effective from Jan 1
            "20230520": {"ruleid": "RULE02", "rate": 1.90},      # Effective from May 20
            "20230615": {"ruleid": "RULE03", "rate": 2.20},      # Effective from Jun 15
            "20230710": {"ruleid": "RULE04", "rate": 3.50}      # Effective from Jul 10
        }

        transactions_file = StringIO(json.dumps(ac001_transactions))
        interest_file = StringIO(json.dumps(interest_rules))

        year_month_input = pd.Period('2023-06', freq='M')
        account_input = "AC001"
        account_transactions_df, account_transactions_df2 = self.sg.generate_account_statement(account_input, transactions_file, year_month_input)
        interest_rule_df = self.sg.generate_interest_rules(interest_file)
        merged_df = self.sg.cross_join_transactions_interest(account_transactions_df2, interest_rule_df)
        merged_desired_month, merged_with_interest = self.sg.calculate_annualized_interest(merged_df, year_month_input)

        annualized_interest_rate = round(float(merged_with_interest['annualized_interest_rate'].sum()), 2)
        final_balance = merged_desired_month.iloc[-1, merged_desired_month.columns.get_loc('balance')] + annualized_interest_rate

        assert annualized_interest_rate == 0.39
        assert final_balance == 130.39

        
    # adding an edge case test where is it a net new accoutn that does not start on day 1 of the month but day 5 
    # it does not have a balance at the start of the month
    # this covers the edge case for the annualized interest rate calculation
    def test_annualized_interest_rate_AC002_202305(self):

        # AC002 transactions for May 2023
        ac002_transactions = {"AC002": [
            {"date": "20230505", "txn_id": "20230505-01", "type": "D", "amount": "100.00"},
            {"date": "20230515", "txn_id": "20230515-01", "type": "D", "amount": "150.00"},
            {"date": "20230520", "txn_id": "20230520-01", "type": "W", "amount": "50.00"},
            {"date": "20230625", "txn_id": "20230526-01", "type": "D", "amount": "200.00"}
        ]}

        # Interest rules applicable for May 2023 
        interest_rules = {
            "20230501": {"ruleid": "RULE01", "rate": 1.95},  # Effective from May 01
            "20230510": {"ruleid": "RULE02", "rate": 1.90},   # Effective from May 10
            "20230523": {"ruleid": "RULE02", "rate": 3.50},   # Effective from May 23,
            "20230607": {"ruleid": "RULE03", "rate": 8.80}   # Effective from Jun 08
        }

        transactions_file = StringIO(json.dumps(ac002_transactions))
        interest_file = StringIO(json.dumps(interest_rules))

        year_month_input = pd.Period('2023-05', freq='M')
        account_input = "AC002"
        account_transactions_df, account_transactions_df2 = self.sg.generate_account_statement(account_input, transactions_file, year_month_input)
        interest_rule_df = self.sg.generate_interest_rules(interest_file)
        merged_df = self.sg.cross_join_transactions_interest(account_transactions_df2, interest_rule_df)
        merged_desired_month, merged_with_interest = self.sg.calculate_annualized_interest(merged_df, year_month_input)

        annualized_interest_rate = round(float(merged_with_interest['annualized_interest_rate'].sum()), 2)
        final_balance = merged_desired_month.iloc[-1, merged_desired_month.columns.get_loc('balance')] + annualized_interest_rate

        assert annualized_interest_rate == 0.34
        assert final_balance == 200.34 

        # # pytest -vv -s --tb=long -k "annualized"