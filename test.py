import unittest
from csv_to_sql.csv_to_sql import format_sql_row
from csv_to_sql.csv_to_sql import escape_sql_characters


class TestFormatFunctions(unittest.TestCase):
    def test_escape_sql_characters(self):
        # Test case 1: Normal case
        assert escape_sql_characters("Claire O'Connell") == "Claire O\\'Connell"
        
        # Test case 2: Special characters
        assert escape_sql_characters("Claire O\"Connell") == "Claire O\\\"Connell"
        assert escape_sql_characters("Claire O/Connell") == "Claire O\\/Connell"
        assert escape_sql_characters("Claire O%Connell") == "Claire O\\%Connell"
        assert escape_sql_characters("Claire O_Connell") == "Claire O\\_Connell"
 
        # Test case 3: NULL, TRUE, FALSE values
        assert escape_sql_characters("NULL") == "NULL"
        assert escape_sql_characters("null") == "null"
        assert escape_sql_characters("TRUE") == "TRUE"
        assert escape_sql_characters("true") == "true"
        assert escape_sql_characters("FALSE") == "FALSE"
        assert escape_sql_characters("false") == "false"
        
        # Test case 4: Empty string
        assert escape_sql_characters("") == ""
        
        # Test case 5: String with only spaces
        assert escape_sql_characters("   ") == "   "

    
    def test_format_sql_row(self):
        # Test case 1: Normal case
        assert format_sql_row(["52", "Rice", "20.7", "TRUE"]) == ["52", "E'Rice'", "20.7", "TRUE"]
        
        # Test case 2: Special characters
        assert format_sql_row(["52", "Ri'ce", "20.7", "TRUE"]) == ["52", r"E'Ri\'ce'", "20.7", "TRUE"]
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
