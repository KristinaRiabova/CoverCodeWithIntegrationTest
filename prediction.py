from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import threading
import requests
import time
from data_loader import update_user_data, user_data_storage

date_format = "%Y-%m-%dT%H:%M"
user_data_storage = {}
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



@app.route('/api/predictions/users', methods=['GET'])
def get_users_online():
    date_str = format_date_string(request.args.get('date'))

    date = datetime.strptime(date_str, date_format)

    online_users = count_online_users(date)
    return jsonify({"usersOnline": online_users})


def count_online_users(target_date):
    online_users = 0

    for user_id, intervals in user_data_storage.items():
        for interval in intervals:
            start_time, end_time = interval

            if not isinstance(start_time, datetime):
                start_time = datetime.strptime(start_time, date_format)



            if start_time.weekday() == target_date.weekday() and \
               start_time.hour == target_date.hour and \
               start_time.minute == target_date.minute:
                online_users += 1

    return online_users


@app.route('/user_intervals', methods=['GET'])
def get_user_intervals():
    return jsonify(user_data_storage)

if __name__ == '__main__':
    data_update_thread = threading.Thread(target=update_user_data)
    data_update_thread.daemon = True
    data_update_thread.start()
    app.run(debug=True)
