# Add the project root to Python path
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from bank.utils import InputValidator
from bank.transactions import TransactionManager
import json

def input_transactions(transactions_file_path):
    transaction_manager = TransactionManager(enable_logging=False)
    input_validator = InputValidator()

    #1. get the input from the user
    date_input, account_input, type_input, amount_input = input("Please enter transactions details in the following order: \n" 
                                            "<Date> <Account> <Type> <Amount>\n").split(" ")

    #2. validate the inputs 
    amount_clean = input_validator.validate_amount_input(amount_input)
    input_validator.validate_date_input(date_input)
    type_clean = input_validator.validate_type_input(type_input)

    #3. now check if the account exists and it it has sufficienct balance for withdrawal
    # else initialize a new account if it does not exist

    with open(transactions_file_path, 'r+') as file:
        transactions_state_file = json.load(file)

        if account_input in transactions_state_file.keys():
            print(f"Account {account_input} exists. Checking for sufficient balance if a withdrawal is requested.")

            sufficient_balance = transaction_manager.sufficient_balance_check(type_clean, amount_clean, account_input, transactions_state_file)

            if sufficient_balance:
                #generate a transaction id 
                txn_id = transaction_manager.generate_txn_id(date_input, transactions_state_file, account_input)

                #log the transaction
                transaction_manager.log_transaction(transactions_state_file, account_input, date_input, txn_id, type_clean, amount_clean, file)

                with open(transactions_file_path, 'r') as print_file:
                    transaction_manager.display_transaction_history(print_file, account_input)

            else:
                print(f"Insufficient balance to process the transaction.")
                sys.exit(1)

        else:
            print(f"Account {account_input} does not exists")

            if type_clean == "D":
                print(f"Since it is a deposit, initializing the account {account_input} and logging the transaction.")
                txn_id = transaction_manager.generate_txn_id(date_input, transactions_state_file, account_input)
                transaction_manager.log_transaction(transactions_state_file, account_input, date_input, txn_id, type_clean, amount_clean, file)
                with open(transactions_file_path, 'r') as print_file:
                    transaction_manager.display_transaction_history(print_file, account_input)
            else:
                print("Cannot withdraw from a non-existing account.")
                sys.exit(1)

if __name__ == "__main__":
    input_transactions('state_files/transactions.json')