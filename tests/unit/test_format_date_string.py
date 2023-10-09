import unittest
from user_stats_api import format_date_string  # Import the function you want to test

class TestYourCode(unittest.TestCase):

    def test_format_date_string(self):
        # Test a valid date string
        input_date = "2023-10-09T12:34"
        expected_output = "2023-10-09T12:34"
        self.assertEqual(format_date_string(input_date), expected_output)

        # Test an invalid date string (just to show an example)
        input_date = "2023-10-09 12:34"
        with self.assertRaises(ValueError):
            format_date_string(input_date)

    # You can add more unit tests for other functions here

if __name__ == '__main__':
    unittest.main()
