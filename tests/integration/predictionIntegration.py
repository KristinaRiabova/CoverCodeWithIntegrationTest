import unittest
import requests
import time
import threading
from prediction import app

class TestAppIntegration(unittest.TestCase):
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
        time.sleep(5)

    def test_api_predictions_users(self):

        response = requests.get('http://localhost:5000/api/predictions/users', params={'date': '2023-10-10T12:00'})


        self.assertEqual(response.status_code, 200)


        data = response.json()


        self.assertIn('usersOnline', data)



if __name__ == '__main__':
    unittest.main()