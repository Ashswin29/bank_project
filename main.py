
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#bank application main entry point
def main():
    first_run = True

    while True:
        if first_run:

            action =input("Welcome to AwesomeGIC Bank! What would you like to do?\n " \
            "1. T - Input transactions \n 2. I - Define interest rules \n 3. P - Print statement \n 4. Q - Quit \n").upper()

            first_run = False
        else:
            action = input("Is there anything else you'd like to do?\n " \
            "1. T - Input transactions \n 2. I - Define interest rules \n 3. P - Print statement \n 4. Q - Quit \n").upper()

        while action not in ['T', 'I', 'P', 'Q']:
            action = input("Invalid option. Please choose again:\n ")
            print("Your options are the following: \n"
                "1. T - Input transactions \n"
                "2. I - Define interest rules \n"
                "3. P - Print statement \n"
                "4. Q - Quit \n")
            
        if action == 'T': 
            from scripts.input_transactions import input_transactions
            input_transactions('state_files/transactions.json')
        elif action == 'I':
            from scripts.update_interest_rule import input_interest_rule
            input_interest_rule('state_files/interests_rule.json')
        elif action == 'P':
            from scripts.print_statement import print_statement
            print_statement("state_files/transactions.json", "state_files/interests_rule.json")
        elif action == 'Q':
            print("Thank you for banking with AwesomeGIC Bank! \n Have a nice day!")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()