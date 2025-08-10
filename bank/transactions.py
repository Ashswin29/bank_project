import json
import pandas as pd
# it is a service class, not a data container (more practical for banking operations where there we will be processing many different transactions)
class TransactionManager:
    def __init__(self, enable_logging = True):
        self.enable_logging = enable_logging

    # internal method to log message
    def _log(self, message):
        if self.enable_logging:
            print(message)

    # calcualtes the current balance of the account, if D, then it adds else it subtracts
    def check_current_balance(self, transactions_file, account_number):
        account_balance = 0 

        for account_bal in transactions_file[account_number]:
            if account_bal['type'] == 'D':
                account_balance += float(account_bal['amount'])
            else:
                account_balance -= float(account_bal['amount'])

        self._log(f"Current account balance is {"{:.2f}".format(account_balance)}")
        return account_balance
    
    # check for balance if its a withdrawal
    def sufficient_balance_check(self, type_input, amount_input, account_input, transactions_state_file):
        account_balance = self.check_current_balance(transactions_state_file, account_input)

        if type_input == 'D':
            self._log("All good, no need to check for account balance since this is a deposit.")
            return True
        else:
            if float(amount_input) < account_balance:
                self._log(f"Have enough balance of {account_balance} to withdraw {amount_input}, logging the transaction")
                return True
            else:
                print(f"Not sufficient account balance to withdraw {amount_input} with an account balance of {account_balance}")
                return False
                # sys.exit(1)


    # generates a transaction id based on the existence of an account and previous transactions if the account exists
    # if the account does not exist, it will create a new transaction id with the date and 01 as the transaction number
    # if the account exists, it will check the date and then generate a new transaction id based on the latest transaction number
    # if the date does not exist, it will create a new transaction id with the date and 01 as the transaction number
    # if the date exists, it will generate a new transaction id based on the latest transaction number
    def generate_txn_id(self, date_str, transactions, account):

        if account not in transactions.keys():
            self._log(f"No previous transactions found for account {account}.")
            return f"{date_str}-01"

        else:

            existing_txn_ids_dict = {}

            for txn_ids in transactions[account]:
                txn_id = txn_ids['txn_id'].replace('\u2011', '-') # replace first to ensure the code point is 45
                if txn_id.split("-")[0] in existing_txn_ids_dict.keys():
                    existing_txn_ids_dict[txn_id.split("-")[0]].append(txn_id.split("-")[1])
                else:
                    existing_txn_ids_dict[txn_id.split("-")[0]] = [txn_id.split("-")[1]] # need to make this a list if not you cannot append
            self._log(f"The past transactions of this account are the following: {existing_txn_ids_dict}")

            if date_str in existing_txn_ids_dict.keys():
                # print(f"Transactions ID for the date {date_str}")
                # print(f"The new id will be {int(existing_txn_ids_dict[date_str][-1]) + 1}") # take the latest transaction by using -1

                new_id = str(int(existing_txn_ids_dict[date_str][-1]) + 1)

                if len(new_id) < 2:
                    new_id = "0" + new_id

                new_txn_id = f"{date_str}-{new_id}"
                self._log(f"Adding id to an existing transaction date: {new_txn_id}")

            else:
                new_txn_id = date_str + "-01"
                self._log(f"It is a new date instance. So the transaction id will be {new_txn_id}")

        return new_txn_id


    def log_transaction(self, transactions_state_file, account_input, date_input, txn_id, type_clean, amount_clean, file):
        if account_input not in transactions_state_file:
            transactions_state_file[account_input] = [] #if the account doesnt exist create an empty list for it first and then append
        transactions_state_file[account_input].append({
            "date": date_input,
            "txn_id": txn_id,
            "type": type_clean,
            "amount": amount_clean
        })
        file.seek(0)
        json.dump(transactions_state_file, file, indent=4)
        file.truncate()
        self._log(f"Transaction {txn_id} logged successfully for account {account_input}")

    def display_transaction_history(self, print_file, account_input):
        print_transactions_state_file = json.load(print_file)
        transacted_account = print_transactions_state_file[account_input]
        transacted_account_df = pd.json_normalize(transacted_account)
        header = "| Date    | Account | Type | Amount |"
        print(header)
        for idx, rows in transacted_account_df.iterrows():
            print(f"| {rows['date']} | {account_input} | {rows['type']} | {rows['amount']} |")

    # all the above functions are not normalizing data and operations are carried out on the json file directly
    # initialize pandas dataframe after logging the transaction to output the data - reread the file. 