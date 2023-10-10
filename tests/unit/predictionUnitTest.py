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

        target_date = datetime.strptime('2023-10-17T12:00', "%Y-%m-%dT%H:%M")

        result = count_online_users(target_date)

        self.assertEqual(result, 0)

    def test_get_users_online(self):

        response = self.app.get('/api/predictions/users?date=2023-10-10T12:00')


        self.assertEqual(response.status_code, 200)


        data = response.get_json()


        self.assertIn('usersOnline', data)



if __name__ == '__main__':
    unittest.main()