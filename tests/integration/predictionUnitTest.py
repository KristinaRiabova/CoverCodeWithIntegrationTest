import unittest
from prediction import app, count_online_users
from datetime import datetime


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_count_online_users(self):
        global user_data_storage
        user_data_storage = {
            'user1': [['2023-10-10T12:00']]
        }

        target_date = datetime.strptime('2023-10-10T12:00', "%Y-%m-%dT%H:%M")

        result = count_online_users(target_date)

        self.assertEqual(result, 1)

    def test_count_online_users_no_data(self):
        global user_data_storage
        user_data_storage = {}

        target_date = datetime.strptime('2023-10-10T12:00', "%Y-%m-%dT%H:%M")

        result = count_online_users(target_date)

        self.assertEqual(result, 0)

    def test_get_users_online(self):
        response = self.app.get('/api/predictions/users?date=2023-10-10T12:00')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIn('usersOnline', data)

    def test_get_user_intervals(self):
        response = self.app.get('/user_intervals')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data, user_data_storage)

    def test_get_user_intervals_empty(self):
        global user_data_storage
        user_data_storage = {}

        response = self.app.get('/user_intervals')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data, {})

    def test_predict_user_online_no_data(self):
        response = self.app.get('/api/predictions/user',
                                query_string={'date': '2023-10-10T12:00', 'tolerance': 0.5, 'userId': 'user1'})

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertTrue("willBeOnline" in data)
        self.assertTrue("onlineChance" in data)
        self.assertFalse(data["willBeOnline"])
