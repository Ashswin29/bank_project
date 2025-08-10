This is a **command line banking application** that allows users to:
- Input transactions (T): User will be prompted to input the following - <Date> <Account> <Type> <Amount>
- Define interest rules (I): User will be prompted to input the following - <Date> <RuleID> <Rate in %>
- Print account statements (P): <Account> <Year><Month>
- Quit application (Q): End the application

**Contraints** users need to be aware of when using the bank application:
- Date should be in YYYYMMdd format
- Account & Ruleid is string, free format
- Interest rate greater than 0 and less than 100
- Only the latest ruleid is kept for a particular day
- Amount must be greater than 0

**Features:**
- Input Transactions: Adds deposits and allows withdrawals
- Interest Rules: Allows one to add or update interest rules at a day granularity
- Print statement: Allows one to view transactions and (simple not cumulative)interest gained for the interested month.

**Main package**
- All the packages for the bank application is hosted under the bank folder. It consists of the following: Transaction class, Interest rule class, Statement class, Shared utility class 

**State files**
- The state files hosting the transactions and the interest rules are hosted under the state_files folder.

**Feature CLI**
- The CLI of the 3 individual features that make up the banking application (input_transactions, update_interest_rule and print_statement) are hosted under scripts

**Unified CLI entry point**
- The entry point to the banking application (unified CLI - main.py) where users are prompted for inputs

**Automated Testing**
- All the individual classes have been rigorously tested using pytest testing framework. 
