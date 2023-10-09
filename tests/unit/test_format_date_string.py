import unittest
from user_stats_api import format_date_string

class TestYourCode(unittest.TestCase):

    def test_format_date_string(self):

        input_date = "2023-10-09T12:34"
        expected_output = "2023-10-09T12:34"
        self.assertEqual(format_date_string(input_date), expected_output)

        input_date = "2023-10-09 12:34"
        with self.assertRaises(ValueError):
            format_date_string(input_date)


if __name__ == '__main__':
    unittest.main()
