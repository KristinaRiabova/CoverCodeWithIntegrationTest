import requests
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import threading


user_data_storage = {}
date_format = "%Y-%m-%dT%H:%M"
app = Flask(__name__)


def format_date_string(date_string):
    dash_count = 0
    formatted_date_string = ''
    for char in date_string:
        if char == '-':
            dash_count += 1
        if dash_count == 3:
            formatted_date_string += 'T'
            dash_count = 0
        else:
            formatted_date_string += char
    return formatted_date_string



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
                            last_seen_str = ":".join(parts[:2])  # Keep only year, month, day, hour, and minute


                            last_seen_datetime = datetime.strptime(last_seen_str, "%Y-%m-%dT%H:%M")
                            if last_intervals and last_intervals[-1][1] is None:
                                last_intervals[-1][1] = last_seen_datetime
                            else:
                                user_data_storage[user_id].append([current_time, last_seen_datetime])

            else:
                print("Incorrect data format:", data)

            print("Wait 30 seconds before trying again...")
            time.sleep(30)
        except Exception as e:
            print("Error when updating data:", repr(e))

@app.route('/user_intervals', methods=['GET'])
def get_user_intervals():
    return jsonify(user_data_storage)


@app.route('/api/stats/users', methods=['GET'])
def get_users_online():

    date_str = format_date_string(request.args.get('date'))


    date = datetime.strptime(date_str, date_format)

    date = date.replace(second=0)

    online_users = count_online_users(date)
    return jsonify({"usersOnline": online_users})


def count_online_users(date):
    online_users = 0
    print(date)

    for user_id, intervals in user_data_storage.items():
        for interval in intervals:
            start_time, end_time = interval


            if not isinstance(start_time, datetime):
                start_time = datetime.strptime(start_time, date_format)
            if end_time and not isinstance(end_time, datetime):
                end_time = datetime.strptime(end_time, date_format)


            end_time = end_time or datetime.now()


            if end_time <= date <= start_time:
                online_users += 1

    return online_users



@app.route('/api/predictions/user', methods=['GET'])
def predict_user_online():
    try:
        date_str = request.args.get('date')
        tolerance = float(request.args.get('tolerance'))
        user_id = request.args.get('userId')


        specified_date = datetime.strptime(date_str, date_format)


        online_chance = calculate_online_chance(user_id, specified_date)


        will_be_online = online_chance > tolerance

        response_data = {
            "willBeOnline": will_be_online,
            "onlineChance": online_chance
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)})

def calculate_online_chance(user_id, specified_date):
    online_count = 0
    total_weeks = 0

    specified_weekday = specified_date.weekday()
    specified_time = specified_date.time()

    intervals = user_data_storage.get(user_id, [])

    for interval in intervals:
        if len(interval) == 2:
            interval_start, interval_end = interval

            if isinstance(interval_start, str):
                interval_start = datetime.strptime(interval_start, date_format)

            if interval_start.weekday() == specified_weekday and interval_start.time() == specified_time:
                online_count += 1

            if interval_end  <= specified_date <= interval_end is not None and interval_start:
                return 1.0

            total_weeks += 1

    if total_weeks == 0:
        return 0.0

    return float(online_count) / total_weeks


if __name__ == '__main__':

    data_update_thread = threading.Thread(target=update_user_data)
    data_update_thread.daemon = True
    data_update_thread.start()



    app.run(debug=True)