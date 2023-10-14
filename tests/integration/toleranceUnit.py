import unittest
from predTolerance import app, format_date_string, count_online_users, date_format, calculate_online_chance, datetime

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

    def test_get_users_online(self):
        global user_data_storage
        user_data_storage = {
            "user1": [["2025-09-27T19:00", "2025-09-27T19:30"]],
            "user2": [["2025-09-27T19:10", "2025-09-27T19:40"]]
        }

        response = self.app.get('/api/stats/users?date=2025-09-27-19:20')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["usersOnline"], 2)

    def test_get_users_online_no_users(self):
        user_data_storage.clear()
        response = self.app.get('/api/stats/users?date=2025-09-27-19:20')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["usersOnline"], 0)

    def test_predict_user_online(self):
        global user_data_storage

        user_data_storage = {
            "user1": [["2025-09-27T19:00", "2025-09-27T19:30"]],
        }

        response = self.app.get('/api/predictions/user?date=2025-09-27-19:20&tolerance=0.5&userId=user1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue("willBeOnline" in data)
        self.assertTrue("onlineChance" in data)

    def test_predict_user_online_invalid_tolerance(self):
        response = self.app.get('/api/predictions/user?date=2025-09-27-19:20&tolerance=abc&userId=user1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue("error" in data)



if __name__ == '__main__':
    unittest.main()
