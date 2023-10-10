import unittest
from predTolerance import app, format_date_string, count_online_users, date_format,calculate_online_chance, datetime

class TestYourApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_format_date_string(self):
        formatted_date = format_date_string("2025-09-27-20:00")
        self.assertEqual(formatted_date, "2025-09-27T20:00")

    def test_calculate_online_chance(self):
        global user_data_storage
        user_data_storage = {
            "user1": [["2025-09-27T19:00", "2025-09-27T19:40"]]
        }
        specified_date = datetime.strptime("2025-09-27T19:50", date_format)
        online_chance = calculate_online_chance("user1", specified_date)
        self.assertEqual(online_chance, 0.0)



if __name__ == '__main__':
    unittest.main()