import unittest
from datetime import datetime
from concrete_user import app, user_data_storage

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_user_historical_data(self):

        user_id = '02d4563d-5727-c811-b3b7-57a10f6be25a'
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
        user_data_storage[user_id] = [[current_time, None]]


        response = self.app.get('/api/stats/user?date=2023-01-01T12:00&userId=02d4563d-5727-c811-b3b7-57a10f6be25a')


        self.assertEqual(response.status_code, 200)


        response_data = response.get_json()


        self.assertTrue('wasUserOnline' in response_data)
        self.assertTrue('nearestOnlineTime' in response_data)


        self.assertFalse(response_data['wasUserOnline'])

    def test_get_user_historical_data_user_not_found(self):

        response = self.app.get('/api/stats/user?date=2023-01-01T12:00&userId=non_existing_user')


        self.assertEqual(response.status_code, 404)

    def test_get_user_intervals(self):

        response = self.app.get('/user_intervals')


        self.assertEqual(response.status_code, 200)


        response_data = response.get_json()


        self.assertTrue(isinstance(response_data, dict))

if __name__ == '__main__':
    unittest.main()