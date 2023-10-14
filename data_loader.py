import requests
import time
from datetime import datetime

date_format = "%Y-%m-%dT%H:%M"
user_data_storage = {}

def update_user_data():
    while True:
        try:
            response = requests.get("https://sef.podkolzin.consulting/api/users/lastSeen?offset=0")
            data = response.json()

            if isinstance(data, dict) and 'data' in data:
                user_list = data['data']
                for user_info in user_list:
                    if isinstance(user_info, dict):
                        user_id = user_info.get('userId')
                        is_online = user_info.get('isOnline')
                        last_seen_str = user_info.get('lastSeenDate')

                        current_time = datetime.now().strftime(date_format)

                        if user_id not in user_data_storage:
                            user_data_storage[user_id] = []

                        last_intervals = user_data_storage[user_id]

                        if is_online:
                            if not last_intervals or (last_intervals and last_intervals[-1][1] is not None):
                                user_data_storage[user_id].append([current_time, None])
                        else:

                            parts = last_seen_str.split(':')
                            last_seen_str = ":".join(parts[:2])  


                            last_seen_datetime = datetime.strptime(last_seen_str, "%Y-%m-%dT%H:%M")
                            if last_intervals and last_intervals[-1][1] is None:
                                last_intervals[-1][1] = last_seen_datetime
                            else:
                                user_data_storage[user_id].append([current_time, last_seen_datetime])

            else:
                print("Некорректный формат данных:", data)

            print("Ожидание 30 секунд перед следующей попыткой...")
            time.sleep(30)
        except Exception as e:
            print("Ошибка при обновлении данных:", repr(e))
