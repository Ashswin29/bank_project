import pytest
import sys
from bank.utils import InputValidator

class TestInputValidator:

    def setup_method(self):
        self.validator = InputValidator()

############ amount validation tests ############

    @pytest.mark.parametrize("input_amount, expected", [
        ("100", "100.00"),
        ("100.50", "100.50"),
        ("100.5", "100.50")
    ])
    def test_validate_amount_valid(self, input_amount, expected):
        result  = self.validator.validate_amount_input(input_amount)
        assert result == expected 

    @pytest.mark.parametrize("invalid_amount", [
        "111.123", #more than 2 decimal places
        "0", #must be greater than 0
        "-1", #must be greater than 0
    ])
    def test_validate_amount_invalid(self, invalid_amount):
        with pytest.raises(SystemExit):
            self.validator.validate_amount_input(invalid_amount)

############ date validation tests ##############

    @pytest.mark.parametrize("input_date", [
        "20230101", #valid date
        "20231231", #valid date
        "20240229"  #valid leap year date
    ])
    def test_validate_date_valid(self, input_date):
        self.validator.validate_date_input(input_date)

    @pytest.mark.parametrize("invalid_date", [
        "2023051",  #too short
        "20231301", #invalid month
        "20231245", #invalid day
    ])
    def test_validate_date_invalid(self, invalid_date):
        with pytest.raises(SystemExit):
            self.validator.validate_date_input(invalid_date)

########### type validation tests #########

    @pytest.mark.parametrize("valid_type, output_valid_type", [
        ("d", "D"), #valid deposit
        ("D", "D"), #valid deposit
        ("w", "W"), #valid withdrawal
        ("W", "W"), #valid withdrawal
    ])
    def test_validate_type_input(self, valid_type, output_valid_type):
        result = self.validator.validate_type_input(valid_type)
        assert result == output_valid_type

    @pytest.mark.parametrize("invalid_type", [
        "dw",  #too short
        "wd", #invalid month
        "i", #invalid day
    ])
    def test_validate_type_invalid(self, invalid_type):
        with pytest.raises(SystemExit):
            self.validator.validate_type_input(invalid_type)

########### rate validation tests #########

    @pytest.mark.parametrize("valid_rate, expected", [
        ("99.9", True), #valid rate
        ("3.45", True), #valid rate
        ("8.88888", True),  #valid rate
    ])
    def test_validate_rate_input(self, valid_rate, expected):
        result_bool = self.validator.validate_rate_input(valid_rate)
        assert result_bool == expected

    @pytest.mark.parametrize("invalid_rate", [
        "101",  #too short
        "-2", #invalid month
        "0", #invalid day
    ])
    def test_validate_rate_invalid(self, invalid_rate):
        with pytest.raises(SystemExit):
            self.validator.validate_rate_input(invalid_rate)