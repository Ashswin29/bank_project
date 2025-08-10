from unittest.mock import Mock, patch
import json
from bank.interest_rules import InterestRateManager

class TestInterestRateManager:
    def setup_method(self):
        self.irm = InterestRateManager()

    def test_upsert_interest_rule_new_date_logic(self):
        mock_file = Mock() # mimicking the json file
        interest_state_file = {}

        self.irm.upsert_interest_rule(
            mock_file, interest_state_file, "20250505", "rule001", "1.50"
        )

        # verify the state was updated correctly
        assert "20250505" in interest_state_file
        assert interest_state_file["20250505"]["ruleid"] == "rule001"
        assert interest_state_file["20250505"]["rate"] == 1.5

        # Verify file methods were called
        mock_file.seek.assert_called_with(0) #make sure it was called with argument 0
        mock_file.truncate.assert_called_once() #make sure it was called once       

    def test_upsert_interest_rule_existing_date_logic(self):
        mock_file = Mock() #back out the file I/O into a separate function, then we can avoid using mock file and its more modular
        interest_state_file = {
            "20250505": {"ruleid": "rule001", "rate": 1.5}
        }

        self.irm.upsert_interest_rule(
            mock_file, interest_state_file, "20250505", "rule002", "8.88"
        )

        # verify the state was updated correctly
        assert "20250505" in interest_state_file
        assert interest_state_file["20250505"]["ruleid"] == "rule002"
        assert interest_state_file["20250505"]["rate"] == 8.88

        #verify file methods were called
        mock_file.seek.assert_called_with(0) #make sure it was called with argument 0
        mock_file.truncate.assert_called_once() #make sure it was called once