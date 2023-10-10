import unittest
import threading
import time
import requests
from concrete_user import app

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_thread = threading.Thread(target=app.run, kwargs={'debug': False})
        cls.app_thread.daemon = True
        cls.app_thread.start()
        cls.wait_for_app_to_start()

    @classmethod
    def tearDownClass(cls):
        cls.app_thread.join(timeout=1)

    @classmethod
    def wait_for_app_to_start(cls):
        time.sleep(30)

    def test_get_user_historical_data(self):
        base_url = "http://localhost:5000/api/stats/user"
        params = {
            'date': '2023-10-10T16:10',
            'userId': '02d4563d-5727-c811-b3b7-57a10f6be25a'
        }
        response = requests.get(base_url, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn('wasUserOnline', data)
        self.assertIn('nearestOnlineTime', data)

    def test_get_user_historical_data_invalid_user(self):
        response = requests.get('http://localhost:5000/api/stats/user?date=2023-10-10T12:50&userId=invalid_user_id')
        self.assertEqual(response.status_code, 404)

    def test_get_user_intervals(self):
        response = requests.get('http://localhost:5000/user_intervals')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)

if __name__ == '__main__':
    unittest.main()