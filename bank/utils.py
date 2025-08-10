import sys
import datetime

class InputValidator:

    def __init__(self): #keep it as a utility class rather than container class - for validation methods
        pass


    #check for decimal places if it has any, if not it checks for amount being greater than 0
    #return reformatted amount with 2 decimal places
    def validate_amount_input(self,amount_str):
        if float(amount_str) > 0:
            if "." in amount_str:
                decimal = amount_str.split(".")[1] # assign it to a variable 
                if len(decimal) <= 2:
                    print("Valid amount format.")
                    return str("{:.2f}".format(float(amount_str)))
                else:
                    print("Invalid format: Amount should have a maximum of 2 decimal places.")
                    sys.exit(1)            
            else:
                return str("{:.2f}".format(float(amount_str)))
        else:
            print("Invalid amount: Amount must be greater than 0.")
            sys.exit(1)

    # validate the input date ensuring it follows the format YYYYMMdd
    def validate_date_input(self, date_str):
        format = "%Y%m%d"
        if len(date_str) == 8 and date_str.isdigit():
            try:
                datetime.datetime.strptime(date_str, format) #this will catch invalid date "20250230" or "20251301"
                print(f"Valid date format: {date_str}.")
            except ValueError:
                print(f"Invalid date format: {date_str}. Please use the format YYYYMMdd.")
                sys.exit(1)
        else:
            print(f"Invalid date format: {date_str}. Please use the format YYYYMMdd.")
            sys.exit(1)

    # validates the type and upper cases it for consistency
    def validate_type_input(self, type_str):
        if type_str.upper() not in ['D', 'W']:
            print(f"Invalid type {type_str} entered, it could be either D or W.")
            sys.exit(1)
        else:
            type_updated = type_str.upper()
            return type_updated

    def validate_rate_input(self, rate_input):
        rate_input = float(rate_input)
        if rate_input > 0 and rate_input <= 100:
            print(f"Rate {rate_input} is valid.")
            return True
        else:
            print(f"Invalid rate {rate_input} entered, it should be between 0 and 100.")
            sys.exit(1)
            # return False




