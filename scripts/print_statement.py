import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
from bank.statement import StatementGenerator

def print_statement(transactions_file_path, interest_rule_file_path):

    statement_generator = StatementGenerator(enable_logging=False)

    account_input, year_month_input = input("Please enter account and month to generate the statement: \n" 
                                                    "<Account> <Year><Month>\n").split(" ")

    year_month_input_formatted = pd.to_datetime(year_month_input, format='%Y%m').to_period('M')


    #check if account exists and if it has trasactions for that month


    with open(transactions_file_path, 'r') as transactions_file:
        account_transactions_df, account_transactions_df2 = statement_generator.generate_account_statement(account_input, transactions_file, year_month_input_formatted)

    with open(interest_rule_file_path, 'r') as interest_file:
        interest_rule_df = statement_generator.generate_interest_rules(interest_file)

        merged_df = statement_generator.cross_join_transactions_interest(account_transactions_df2, interest_rule_df)

        merged_desired_month, merged_with_interest = statement_generator.calculate_annualized_interest(merged_df, year_month_input_formatted)

        statement_generator.display_account_statement(account_transactions_df, year_month_input_formatted, merged_desired_month, merged_with_interest)

if __name__ == "__main__":
    print_statement('state_files/transactions.json', 'state_files/interests_rule.json')