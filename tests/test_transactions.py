import pytest 
import json 
import tempfile
import os
from bank.transactions import TransactionManager


class TestTransactionManager:
    def setup_method(self):
        self.tm = TransactionManager(enable_logging=True)

############### test transaction id generation ####################

    def test_generate_txn_id_new_account(self):
        # initatiate an empty transaction file 
        transactions = {}
        txn_id = self.tm.generate_txn_id("20250505", transactions, "AC001")
        assert txn_id == "20250505-01"

    def test_generate_txn_id_existing_date_increment(self):
        #create the mock transaction file here and ensure its incrementing 
        transactions = {
            "AC001": [
                {"date": "20250505", "txn_id": "20250505-01", "type": "D", "amount": "100.00"},
                {"date": "20250505", "txn_id": "20250505-02", "type": "W", "amount": "50.00"}
            ]
        }
        txn_id = self.tm.generate_txn_id("20250505", transactions, "AC001")
        assert txn_id == "20250505-03"

    def test_generate_txn_id_new_date(self):
        #create the mock transaction file here and ensure its incrementing 
        transactions = {
            "AC001": [
                {"date": "20250505", "txn_id": "20250505-01", "type": "D", "amount": "100.00"},
                {"date": "20250505", "txn_id": "20250505-02", "type": "W", "amount": "50.00"}
            ]
        }
        txn_id = self.tm.generate_txn_id("20250506", transactions, "AC001")
        assert txn_id == "20250506-01"

############### test check current balance ####################
    # non-parametrized version
    # def test_check_current_balance(self):
    #     #create the mock transaction file here and ensure its incrementing 
    #     transactions = {
    #         "AC001": [
    #             {"date": "20250505", "txn_id": "20250505-01", "type": "D", "amount": "100.00"},
    #             {"date": "20250505", "txn_id": "20250505-02", "type": "W", "amount": "50.00"}
    #         ]
    #     }
    #     account_balance = self.tm.check_current_balance(transactions, "AC001")
    #     assert account_balance == 50.00

    @pytest.mark.parametrize("transactions, expected_balance", [
        ({"AC001": [
                {"date": "20250505", "txn_id": "20250505-01", "type": "D", "amount": "100.00"},
                {"date": "20250505", "txn_id": "20250505-02", "type": "W", "amount": "50.00"}
            ]}, 50.00),

            ({"AC001": [
                {"date": "20250505", "txn_id": "20250505-01", "type": "D", "amount": "100.00"},
                {"date": "20250505", "txn_id": "20250505-02", "type": "W", "amount": "50.00"},
                {"date": "20250506", "txn_id": "20250506-01", "type": "W", "amount": "40.00"}
            ]}, 10.00),
    ])
    def test_check_current_balance_paramterized(self, transactions, expected_balance):
        account_balance = self.tm.check_current_balance(transactions, "AC001")
        assert account_balance == expected_balance

    @pytest.mark.parametrize("transactions, transaction_type, withdrawal_amount, sufficent_balance", [
        ({"AC001": [
                {"date": "20250505", "txn_id": "20250505-01", "type": "D", "amount": "100.00"},
                {"date": "20250505", "txn_id": "20250505-02", "type": "W", "amount": "50.00"}
            ]}, "W", "40", True),
        ({"AC001": [
                {"date": "20250505", "txn_id": "20250505-01", "type": "D", "amount": "100.00"}
            ]}, "W", "101", False),
        ({"AC001": [
                {"date": "20250505", "txn_id": "20250505-01", "type": "D", "amount": "100.00"}
            ]}, "D", "101", True)
    ])
    def test_sufficient_balance_paramterized(self, transactions, transaction_type, withdrawal_amount, sufficent_balance):
        account_balance = self.tm.sufficient_balance_check(transaction_type, withdrawal_amount, "AC001", transactions)
        assert account_balance == sufficent_balance