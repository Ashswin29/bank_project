import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bank.utils import InputValidator
from bank.interest_rules import InterestRateManager
import json

def input_interest_rule(interest_rule_file_path):

    #1. get the input from the user
    date_input, rule_id_input, rate_input = input("Please enter transactions details in the following order: \n" 
                                                    "<Date> <RuleID> <Rate in %>\n").split(" ")
    
    #2. initiate the interest rate manager and input validator 
    input_validator = InputValidator()
    interest_rate_manager = InterestRateManager(enable_logging=False)

    #3. validate the inputs
    input_validator.validate_date_input(date_input)
    input_validator.validate_rate_input(rate_input)

    #4. upsert and display the interest rules 
    with open(interest_rule_file_path, 'r+') as file:
        interest_state_file = json.load(file)

        interest_rate_manager.upsert_interest_rule(file, interest_state_file, date_input, rule_id_input, rate_input)

        interest_rate_manager.display_interest_rules(interest_state_file)

if __name__ == "__main__":
    input_interest_rule('state_files/interests_rule.json')