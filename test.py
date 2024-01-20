import unittest
from csv_to_sql.csv_to_sql import format_sql_row


class TestFormatFunctions(unittest.TestCase):
    def test_format_sql_row(self):
        # Test case 1: Normal case
        assert format_sql_row(["52", "Rice", "20.7", "TRUE"]) == ["52", "E'Rice'", "20.7", "TRUE"]
        
        # Test case 2: Special characters
        assert format_sql_row(["52", "Ri'ce", "20.7", "TRUE"]) == ["52", r"E'Ri'ce'", "20.7", "TRUE"]
        assert format_sql_row(["52", "Ri\"ce", "20.7", "TRUE"]) == ["52", "E'Ri\\\"ce'", "20.7", "TRUE"]
        assert format_sql_row(["52", "Ri/ce", "20.7", "TRUE"]) == ["52", r"E'Ri\/ce'", "20.7", "TRUE"]
        assert format_sql_row(["52", "Ri%ce", "20.7", "TRUE"]) == ["52", r"E'Ri\%ce'", "20.7", "TRUE"]
        assert format_sql_row(["52", "Ri_ce", "20.7", "TRUE"]) == ["52", r"E'Ri\_ce'", "20.7", "TRUE"]
        
        # Test case 3: NULL, TRUE, FALSE values
        assert format_sql_row(["52", "NULL", "20.7", "TRUE"]) == ["52", "NULL", "20.7", "TRUE"]
        assert format_sql_row(["52", "null", "20.7", "TRUE"]) == ["52", "NULL", "20.7", "TRUE"]
        assert format_sql_row(["52", "TRUE", "20.7", "TRUE"]) == ["52", "TRUE", "20.7", "TRUE"]
        assert format_sql_row(["52", "true", "20.7", "TRUE"]) == ["52", "TRUE", "20.7", "TRUE"]
        assert format_sql_row(["52", "FALSE", "20.7", "TRUE"]) == ["52", "FALSE", "20.7", "TRUE"]
        assert format_sql_row(["52", "false", "20.7", "TRUE"]) == ["52", "FALSE", "20.7", "TRUE"]
        
        # Test case 4: Empty string
        assert format_sql_row(["52", "", "20.7", "TRUE"]) == ["52", "E''", "20.7", "TRUE"]
        
        # Test case 5: String with only spaces
        assert format_sql_row(["52", "   ", "20.7", "TRUE"]) == ["52", "E'   '", "20.7", "TRUE"]


if __name__ == "__main__":
    unittest.main()
