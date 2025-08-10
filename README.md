This is a **command line banking application** that allows users to:

**What You Can Do**
Input Transactions (T):
Enter deposits or withdrawals. You’ll be asked for transaction details like date, account, and amount.

Define Interest Rules (I):
Set or update interest rates for your accounts. You’ll be prompted to enter the date, rule ID, and interest rate (as a percentage).

Print Account Statements (P):
View your transaction history and see the interest earned for a selected month.

Quit Application (Q):
Exit the program safely.

**User Guidelines & Constraints**
Date Format:
Enter dates as YYYYMMdd (e.g., 20250101 for January 1, 2025).

Account & Rule ID:
These are free-form text fields; you can use any string.

Interest Rate:
Must be greater than 0 and less than 100.

Rule Updates:
Only the latest rule for a given day is kept.

Transaction Amount:
Must be greater than 0.

**Features:**
- Input Transactions: Adds deposits and allows withdrawals
- Interest Rules: Add or update interest rates for specific days. Only one rule per day is stored.
- Print statement: See all your transactions and the interest earned for a chosen month. Interest is calculated simply (not compounded).

**Main package**
- All the packages for the bank application is hosted under the bank folder. It consists of the following: Transaction class, Interest rule class, Statement class, Shared utility class 

**State files**
- The state files hosting the transactions and the interest rules are hosted under the state_files folder.

**Feature CLI**
- The CLI of the 3 individual features that make up the banking application (input_transactions, update_interest_rule and print_statement) are hosted under scripts

**Unified CLI entry point**
- The entry point to the banking application (unified CLI - main.py) where users are prompted for inputs

**Automated Testing**
- All core classes are tested using the pytest framework to ensure reliability. 
