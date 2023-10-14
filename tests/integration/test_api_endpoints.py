import unittest
import threading
import time
import requests
from user_stats_api import app, update_user_data


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

        time.sleep(2)

    def test_get_user_intervals(self):

        response = requests.get("http://127.0.0.1:5000/user_intervals")


        self.assertEqual(response.status_code, 200)



    def test_get_users_online(self):

        response = requests.get("http://127.0.0.1:5000/api/stats/users?date=2023-10-09T18:44")


        self.assertEqual(response.status_code, 200)


    def test_get_users_online_data(self):
        response = requests.get("http://127.0.0.1:5000/api/stats/users?date=2023-10-13T18:44")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['usersOnline'], 0)
    def test_invalid_date_format(self):
        response = requests.get("http://127.0.0.1:5000/api/stats/users?date=invalid_date_format")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("error", data)




if __name__ == '__main__':
    unittest.main()
