import json
import pandas as pd

 #  class provides methods to add or update interest rules and display them in a user-friendly format. 
 #  It ensures that only the latest rule for each date is stored, maintaining data integrity.
class InterestRateManager:

    def __init__(self, enable_logging= True):
        self.enable_logging = enable_logging

    def _log(self, message):
        if self.enable_logging:
            print(message)

    #Adds a new interest rule or updates an existing rule for a given date. 
    #Ensures only the latest rule for each day is kept.
    def upsert_interest_rule(self, file, interest_state_file, date_input, rule_id_input, rate_input):
        
        if date_input in interest_state_file.keys():
            self._log(f"Interest rule for the date {date_input} already exists. Updating the rule & rate.")
            interest_state_file[date_input].update({"ruleid": rule_id_input, "rate": float(rate_input)})
            self._log(f"Updated interest state file: {interest_state_file}")
            file.seek(0)
            json.dump(interest_state_file, file, indent = 4)
            file.truncate()
        else:
            self._log(f"Date does not exist. Initiating date and corresponding rule, rate.")
            interest_state_file[date_input] = {} #if this were a list then use append instead of update
            interest_state_file[date_input].update({"ruleid": rule_id_input, "rate": float(rate_input)})
            self._log(f"Updated interest state file: {interest_state_file}")
            file.seek(0)
            json.dump(interest_state_file, file, indent = 4)
            file.truncate()

    #Displays all interest rules in a formatted table, sorted by date.
    def display_interest_rules(self, interest_state_file):
        interest_rule_df = pd.DataFrame(interest_state_file).T.reset_index() #need to transpose and reset index if not it errors out saying 2 elements but given 3
        interest_rule_df.columns = ["Date", "Rule ID", "Rate (%)"]
        interest_rule_df['Date'] = pd.to_datetime(interest_rule_df['Date']).dt.date
        interest_rule_df = interest_rule_df.sort_values(by='Date', ascending=True, inplace=False)

        # alternative below without pandas #dont change this to self.log - this need to be displayed at all times
        header = "| Date    | Rule ID | Rate (%) |"
        print(header)
        for index, row in interest_rule_df.iterrows():
            date_str = row['Date'].strftime('%Y%m%d')
            print(f"| {date_str} | {row['Rule ID']} | {row['Rate (%)']:.2f} |")